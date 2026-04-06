from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pandas as pd
import requests

from config import API_BASE_URL, API_KEY, DEFAULT_COMPETITIONS, FORM_MATCH_COUNT, LOCAL_TZ, ODDS_FILE
from database import Database


class FootballDataClient:
    def __init__(self, api_key: str = API_KEY, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"X-Auth-Token": api_key})

    def get(self, path: str, **params) -> dict:
        response = self.session.get(f"{self.base_url}{path}", params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def competitions(self, code: str) -> dict:
        return self.get(f"/competitions/{code}")

    def matches(self, code: str, date_from: str, date_to: str, status: str | None = None) -> dict:
        params = {"dateFrom": date_from, "dateTo": date_to}
        if status:
            params["status"] = status
        return self.get(f"/competitions/{code}/matches", **params)

    def standings(self, code: str) -> dict:
        return self.get(f"/competitions/{code}/standings")


def utc_date_range(days_ahead: int) -> tuple[str, str]:
    now = datetime.now(timezone.utc)
    return now.date().isoformat(), (now + timedelta(days=days_ahead)).date().isoformat()


def normalize_matches(competition_code: str, payload: dict) -> pd.DataFrame:
    rows = []
    for match in payload.get("matches", []):
        rows.append(
            {
                "match_id": match["id"],
                "competition_code": competition_code,
                "utc_date": match["utcDate"],
                "status": match["status"],
                "stage": match.get("stage"),
                "matchday": match.get("matchday"),
                "home_team_id": match["homeTeam"]["id"],
                "away_team_id": match["awayTeam"]["id"],
                "home_team_name": match["homeTeam"]["name"],
                "away_team_name": match["awayTeam"]["name"],
                "home_score": match.get("score", {}).get("fullTime", {}).get("home"),
                "away_score": match.get("score", {}).get("fullTime", {}).get("away"),
                "winner": match.get("score", {}).get("winner"),
                "last_updated": match.get("lastUpdated"),
                "raw_json": json.dumps(match),
            }
        )
    return pd.DataFrame(rows)


def extract_teams(matches_frame: pd.DataFrame) -> pd.DataFrame:
    if matches_frame.empty:
        return pd.DataFrame(columns=["team_id", "name", "short_name", "tla", "venue"])
    home = matches_frame[["home_team_id", "home_team_name"]].rename(columns={"home_team_id": "team_id", "home_team_name": "name"})
    away = matches_frame[["away_team_id", "away_team_name"]].rename(columns={"away_team_id": "team_id", "away_team_name": "name"})
    teams = pd.concat([home, away], ignore_index=True).drop_duplicates(subset=["team_id"]).copy()
    teams["short_name"] = teams["name"]
    teams["tla"] = None
    teams["venue"] = None
    return teams


def normalize_standings(competition_code: str, payload: dict) -> pd.DataFrame:
    rows = []
    season = payload.get("season", {})
    for table in payload.get("standings", []):
        if table.get("type") not in {"TOTAL", "HOME", "AWAY"}:
            continue
        if table.get("type") != "TOTAL":
            continue
        for entry in table.get("table", []):
            rows.append(
                {
                    "competition_code": competition_code,
                    "season_start": season.get("startDate"),
                    "team_id": entry["team"]["id"],
                    "position": entry.get("position"),
                    "played_games": entry.get("playedGames"),
                    "won": entry.get("won"),
                    "draw": entry.get("draw"),
                    "lost": entry.get("lost"),
                    "goals_for": entry.get("goalsFor"),
                    "goals_against": entry.get("goalsAgainst"),
                    "goal_difference": entry.get("goalDifference"),
                    "points": entry.get("points"),
                    "form": entry.get("form"),
                }
            )
    return pd.DataFrame(rows)


def compute_recent_form(matches: pd.DataFrame, competition_code: str, form_window: int = FORM_MATCH_COUNT) -> pd.DataFrame:
    finished = matches.loc[matches["status"] == "FINISHED"].copy()
    if finished.empty:
        return pd.DataFrame(columns=[
            "team_id", "competition_code", "form_window", "matches_played", "wins", "draws",
            "losses", "goals_for", "goals_against", "points_per_match"
        ])

    finished["utc_date"] = pd.to_datetime(finished["utc_date"], utc=True)
    records = []

    for team_id in pd.unique(pd.concat([finished["home_team_id"], finished["away_team_id"]], ignore_index=True)):
        team_matches = finished[(finished["home_team_id"] == team_id) | (finished["away_team_id"] == team_id)].sort_values("utc_date", ascending=False).head(form_window)
        wins = draws = losses = goals_for = goals_against = 0
        for _, match in team_matches.iterrows():
            is_home = match["home_team_id"] == team_id
            gf = match["home_score"] if is_home else match["away_score"]
            ga = match["away_score"] if is_home else match["home_score"]
            goals_for += gf
            goals_against += ga
            if gf > ga:
                wins += 1
            elif gf == ga:
                draws += 1
            else:
                losses += 1
        count = len(team_matches)
        ppm = ((wins * 3) + draws) / count if count else 0
        records.append(
            {
                "team_id": int(team_id),
                "competition_code": competition_code,
                "form_window": form_window,
                "matches_played": count,
                "wins": wins,
                "draws": draws,
                "losses": losses,
                "goals_for": goals_for / count if count else 0,
                "goals_against": goals_against / count if count else 0,
                "points_per_match": ppm,
            }
        )
    return pd.DataFrame(records)


def compute_h2h_stats(matches: pd.DataFrame) -> pd.DataFrame:
    finished = matches.loc[matches["status"] == "FINISHED"].copy()
    if finished.empty:
        return pd.DataFrame(columns=[
            "team_id", "opponent_team_id", "matches_played", "wins", "draws", "losses", "goals_for", "goals_against"
        ])
    records = []
    grouped = finished.groupby(["home_team_id", "away_team_id"], dropna=False)
    for (home_id, away_id), group in grouped:
        home_wins = int((group["home_score"] > group["away_score"]).sum())
        draws = int((group["home_score"] == group["away_score"]).sum())
        away_wins = int((group["home_score"] < group["away_score"]).sum())
        matches_played = len(group)
        home_goals = group["home_score"].sum()
        away_goals = group["away_score"].sum()
        records.append({
            "team_id": int(home_id),
            "opponent_team_id": int(away_id),
            "matches_played": matches_played,
            "wins": home_wins,
            "draws": draws,
            "losses": away_wins,
            "goals_for": home_goals / matches_played,
            "goals_against": away_goals / matches_played,
        })
        records.append({
            "team_id": int(away_id),
            "opponent_team_id": int(home_id),
            "matches_played": matches_played,
            "wins": away_wins,
            "draws": draws,
            "losses": home_wins,
            "goals_for": away_goals / matches_played,
            "goals_against": home_goals / matches_played,
        })
    return pd.DataFrame(records)


def load_odds_file(path: str = ODDS_FILE) -> pd.DataFrame:
    odds_path = pd.io.common.stringify_path(path)
    if not pd.io.common.file_exists(odds_path):
        return pd.DataFrame(columns=[
            "match_id", "bookmaker", "home_win_odds", "draw_odds", "away_win_odds",
            "over_2_5_odds", "under_2_5_odds", "btts_yes_odds", "btts_no_odds"
        ])
    if odds_path.endswith(".json"):
        frame = pd.read_json(odds_path)
    else:
        frame = pd.read_csv(odds_path)
    return frame


def run_fetch(days_ahead: int = 7, competitions: list[str] | None = None) -> None:
    competitions = competitions or DEFAULT_COMPETITIONS
    db = Database()
    db.initialize()
    client = FootballDataClient()
    date_from, date_to = utc_date_range(days_ahead)

    all_matches = []
    all_standings = []

    for code in competitions:
        competition_meta = client.competitions(code)
        competition_frame = pd.DataFrame([{
            "code": competition_meta["code"],
            "name": competition_meta["name"],
            "area_name": competition_meta.get("area", {}).get("name"),
        }])
        db.upsert_dataframe("competitions", competition_frame, ["code"])

        upcoming = normalize_matches(code, client.matches(code, date_from, date_to))
        history = normalize_matches(code, client.matches(code, (datetime.now(timezone.utc) - timedelta(days=180)).date().isoformat(), date_to))
        combined = pd.concat([upcoming, history], ignore_index=True).drop_duplicates(subset=["match_id"])
        standings = normalize_standings(code, client.standings(code))
        recent_form = compute_recent_form(combined, code)

        all_matches.append(combined)
        all_standings.append(standings)

        db.upsert_dataframe("matches", combined, ["match_id"])
        db.upsert_dataframe("teams", extract_teams(combined), ["team_id"])
        db.upsert_dataframe("standings", standings, ["competition_code", "team_id"])
        db.upsert_dataframe("team_form", recent_form, ["team_id", "competition_code", "form_window"])

    if all_matches:
        h2h = compute_h2h_stats(pd.concat(all_matches, ignore_index=True))
        db.upsert_dataframe("h2h_stats", h2h, ["team_id", "opponent_team_id"])

    odds = load_odds_file()
    if not odds.empty:
        db.upsert_dataframe("bookmaker_odds", odds, ["match_id"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch football data and store it in SQLite.")
    parser.add_argument("--days-ahead", type=int, default=7)
    parser.add_argument("--competitions", nargs="*", default=DEFAULT_COMPETITIONS)
    args = parser.parse_args()
    run_fetch(days_ahead=args.days_ahead, competitions=args.competitions)


if __name__ == "__main__":
    main()
