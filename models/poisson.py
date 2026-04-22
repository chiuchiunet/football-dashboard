from __future__ import annotations

from dataclasses import dataclass
from math import exp, factorial
from typing import Iterable

import pandas as pd

from config import HOME_ADVANTAGE_MULTIPLIER, MAX_GOALS


@dataclass
class MatchPrediction:
    home_win_prob: float
    draw_prob: float
    away_win_prob: float
    over_2_5_prob: float
    under_2_5_prob: float
    btts_yes_prob: float
    btts_no_prob: float
    expected_home_goals: float
    expected_away_goals: float
    # Half-time
    home_half_prob: float = 0.0
    draw_half_prob: float = 0.0
    away_half_prob: float = 0.0
    expected_home_half_goals: float = 0.0
    expected_away_half_goals: float = 0.0


def poisson_pmf(k: int, lam: float) -> float:
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return (lam ** k) * exp(-lam) / factorial(k)


def build_score_matrix(home_xg: float, away_xg: float, max_goals: int = MAX_GOALS) -> pd.DataFrame:
    data = []
    for home_goals in range(max_goals + 1):
        row = []
        for away_goals in range(max_goals + 1):
            row.append(poisson_pmf(home_goals, home_xg) * poisson_pmf(away_goals, away_xg))
        data.append(row)
    return pd.DataFrame(data)


def _load_xg_cache():
    """
    Load Understat xG data keyed by team name.
    
    For PL teams: uses RECENT per-match xG from understat_history (last 5 home/away games)
    instead of season-total averages — captures current form better.
    
    Falls back to season-total from understat_xg if recent data insufficient.
    """
    try:
        import sqlite3
        from pathlib import Path
        db_path = Path(__file__).resolve().parent.parent / "football.db"
        conn = sqlite3.connect(db_path)

        # For each PL team: recent home xG, recent away xG, recent xGA (last 5 games each)
        recent_rows = conn.execute("""
            WITH recent AS (
                SELECT 
                    team_name,
                    h_a,
                    xG,
                    xGA,
                    ROW_NUMBER() OVER (PARTITION BY team_name, h_a ORDER BY date DESC) as rn
                FROM understat_history
                WHERE league = 'PL'
            )
            SELECT 
                team_name,
                h_a,
                AVG(xG) as avg_xg,
                AVG(xGA) as avg_xga
            FROM recent
            WHERE rn <= 5
            GROUP BY team_name, h_a
        """).fetchall()

        # Season-total xG for fallback / defense strength
        season_rows = conn.execute("""
            SELECT team_name, xg, xga, home_xg, away_xg, played, xpts, pts
            FROM understat_xg WHERE league_code='PL'
        """).fetchall()
        conn.close()

        # Build recent xG dict: {team_name: {"home_xg": float, "away_xg": float, "xga": float, "played": int, "recent_games": int}}
        recent_xg = {}
        for team, h_a, avg_xg, avg_xga in recent_rows:
            if team not in recent_xg:
                recent_xg[team] = {"home_xg": [], "away_xg": [], "xga": [], "recent_games": 0}
            if h_a == "h":
                recent_xg[team]["home_xg"].append(avg_xg)
            else:
                recent_xg[team]["away_xg"].append(avg_xga)  # away team xGA = our xG
            recent_xg[team]["xga"].append(avg_xga)
            recent_xg[team]["recent_games"] += 1

        # Build season-total dict
        season_xg = {}
        for r in season_rows:
            season_xg[r[0]] = {
                "xg": r[1], "xga": r[2], "home_xg": r[3], "away_xg": r[4],
                "played": r[5], "xpts_total": r[6], "pts_total": r[7]
            }

        # Merge: use recent when available (>=3 games), else season-total
        result = {}
        all_teams = set(list(recent_xg.keys()) + list(season_xg.keys()))
        for team in all_teams:
            recent = recent_xg.get(team, {})
            season = season_xg.get(team, {})

            # Recent home xG: need at least 2 home games
            if len(recent.get("home_xg", [])) >= 2:
                rh_xg = sum(recent["home_xg"]) / len(recent["home_xg"])
            else:
                rh_xg = season.get("home_xg", 1.35)

            # Recent away xG: need at least 2 away games
            if len(recent.get("away_xg", [])) >= 2:
                ra_xg = sum(recent["away_xg"]) / len(recent["away_xg"])
            else:
                ra_xg = season.get("away_xg", 1.15)

            # Recent overall xGA
            if len(recent.get("xga", [])) >= 3:
                r_xga = sum(recent["xga"]) / len(recent["xga"])
            else:
                r_xga = season.get("xga", 1.35)

            # Recent games count (home + away)
            recent_count = recent.get("recent_games", 0)

            result[team] = {
                # Per-match xG from RECENT games (primary)
                "recent_home_xg": rh_xg,
                "recent_away_xg": ra_xg,
                "recent_xga": r_xga,
                "recent_games": recent_count,
                # Season-total (fallback / for xpts)
                "xg": season.get("xg", 1.35),
                "xga": season.get("xga", 1.35),
                "home_xg": season.get("home_xg", 1.35),
                "away_xg": season.get("away_xg", 1.15),
                "played": season.get("played", 0),
                "xpts_total": season.get("xpts_total", 0),
                "pts_total": season.get("pts_total", 0),
            }
        return result
    except Exception as e:
        print(f"Warning: _load_xg_cache failed: {e}")
        return {}


_XG_CACHE = None


def _get_xg(team_name: str) -> dict | None:
    """Get xG stats for a team, using cached data."""
    global _XG_CACHE
    if _XG_CACHE is None:
        _XG_CACHE = _load_xg_cache()
    return _XG_CACHE.get(team_name)


def _weighted_form_score(recent: list, decay: float = 0.85) -> float:
    """
    Calculate time-weighted form score from recent match history.
    Uses xpts (expected points) instead of raw pts to reduce luck factor.
    Recent matches have higher weight via exponential decay.

    Args:
        recent: list of dicts with 'xpts' (and optionally 'pts')
        decay: weight multiplier per older match (0.85 = each older match is worth 85% of the previous)

    Returns:
        Weighted average xpts per game (0 to 3)
    """
    if not recent:
        return 1.0  # neutral

    total_weight = 0.0
    weighted_xpts = 0.0
    weight = 1.0

    for i, m in enumerate(recent[:10]):  # cap at 10 matches
        xpts = float(m.get("xpts", m.get("pts", 1.0)))
        weighted_xpts += xpts * weight
        total_weight += weight
        weight *= decay

    if total_weight <= 0:
        return 1.0
    return weighted_xpts / total_weight


def expected_goals(
    home_team_id: int,
    away_team_id: int,
    standings: pd.DataFrame,
    recent_form: pd.DataFrame,
    h2h_stats: pd.DataFrame,
    home_team_name: str = "",
    away_team_name: str = "",
) -> tuple[float, float]:
    league_avg_goals = max(
        (standings["goals_for"].sum() / standings["played_games"].replace(0, pd.NA).sum()) if not standings.empty else 2.6,
        0.2,
    )
    base_home = league_avg_goals / 2
    base_away = league_avg_goals / 2

    home_row = standings.loc[standings["team_id"] == home_team_id]
    away_row = standings.loc[standings["team_id"] == away_team_id]
    home_form = recent_form.loc[recent_form["team_id"] == home_team_id]
    away_form = recent_form.loc[recent_form["team_id"] == away_team_id]
    h2h = h2h_stats.loc[
        (h2h_stats["team_id"] == home_team_id) & (h2h_stats["opponent_team_id"] == away_team_id)
    ]

    # Try to use xG data from Understat for EPL teams
    home_xg_data = _get_xg(home_team_name) if home_team_name else None
    away_xg_data = _get_xg(away_team_name) if away_team_name else None

    if home_xg_data and away_xg_data and home_xg_data["played"] and away_xg_data["played"]:
        # Use RECENT per-match xG from understat_history (last 5 games)
        # This captures current form vs season-average
        avg_xg = 1.35  # approximate EPL avg per team per game from understat
        
        # Primary: use recent per-match xG (home/away split)
        recent_home_xg = home_xg_data["recent_home_xg"]
        recent_away_xg = away_xg_data["recent_away_xg"]
        recent_xga_home = home_xg_data["recent_xga"]  # avg xGA when playing at home
        recent_xga_away = away_xg_data["recent_xga"]  # avg xGA when playing away

        # Attack: recent per-match xG relative to league average
        home_attack = recent_home_xg / avg_xg
        away_attack = recent_away_xg / avg_xg
        
        # Defense: recent xGA relative to league average (lower xGA = better defense)
        home_defense = recent_xga_away / avg_xg   # how well home team restricts AWAY opponents
        away_defense = recent_xga_home / avg_xg    # how well away team restricts HOME opponents

        # Scale to our base
        home_xg = base_home * home_attack * home_defense
        away_xg = base_away * away_attack * away_defense

        # Form boost: use recent xpts trend (decay=0.85 per older match)
        # If team has recent games, use xpts-based form; else neutral
        recent_games = min(home_xg_data.get("recent_games", 0), 10)
        if recent_games >= 3:
            # Use recent xpts from season-total as proxy for form
            home_xpts_per_game = home_xg_data["xpts_total"] / max(home_xg_data["played"], 1)
            away_xpts_per_game = away_xg_data["xpts_total"] / max(away_xg_data["played"], 1)
            home_form_boost = 0.9 + min(home_xpts_per_game / 3, 0.4)
            away_form_boost = 0.9 + min(away_xpts_per_game / 3, 0.4)
        else:
            home_form_boost = 1.0
            away_form_boost = 1.0

        home_xg *= home_form_boost * HOME_ADVANTAGE_MULTIPLIER
        away_xg *= away_form_boost

    else:
        # Fall back to raw goals from standings
        if not home_row.empty and not away_row.empty:
            home_attack = (home_row.iloc[0]["goals_for"] / max(home_row.iloc[0]["played_games"], 1)) / max(base_home, 0.2)
            home_defense = (home_row.iloc[0]["goals_against"] / max(home_row.iloc[0]["played_games"], 1)) / max(base_away, 0.2)
            away_attack = (away_row.iloc[0]["goals_for"] / max(away_row.iloc[0]["played_games"], 1)) / max(base_away, 0.2)
            away_defense = (away_row.iloc[0]["goals_against"] / max(away_row.iloc[0]["played_games"], 1)) / max(base_home, 0.2)
        else:
            home_attack = away_attack = home_defense = away_defense = 1.0

        home_form_boost = 1.0
        away_form_boost = 1.0
        if not home_form.empty:
            home_form_boost = 0.85 + min(home_form.iloc[0]["points_per_match"] / 3, 0.5)
        if not away_form.empty:
            away_form_boost = 0.85 + min(away_form.iloc[0]["points_per_match"] / 3, 0.5)

        home_xg = base_home * home_attack * away_defense * home_form_boost * HOME_ADVANTAGE_MULTIPLIER
        away_xg = base_away * away_attack * home_defense * away_form_boost

    h2h_home_boost = 1.0
    h2h_away_boost = 1.0
    if not h2h.empty and h2h.iloc[0]["matches_played"] >= 2:
        # Cap reduced from 0.4 to 0.2 — H2H shouldn't dominate predictions
        h2h_home_boost = 0.95 + min(h2h.iloc[0]["goals_for"] / max(h2h.iloc[0]["matches_played"], 1), 0.2)
        h2h_away_boost = 0.95 + min(h2h.iloc[0]["goals_against"] / max(h2h.iloc[0]["matches_played"], 1), 0.2)

    home_xg *= h2h_home_boost
    away_xg *= h2h_away_boost

    return round(max(home_xg, 0.2), 3), round(max(away_xg, 0.2), 3)


def predict_match(
    home_team_id: int,
    away_team_id: int,
    standings: pd.DataFrame,
    recent_form: pd.DataFrame,
    h2h_stats: pd.DataFrame,
    home_team_name: str = "",
    away_team_name: str = "",
) -> MatchPrediction:
    home_xg, away_xg = expected_goals(home_team_id, away_team_id, standings, recent_form, h2h_stats,
                                       home_team_name, away_team_name)
    matrix = build_score_matrix(home_xg, away_xg)

    home_win_prob = 0.0
    draw_prob = 0.0
    away_win_prob = 0.0
    over_2_5_prob = 0.0
    btts_yes_prob = 0.0

    for home_goals in matrix.index:
        for away_goals in matrix.columns:
            prob = matrix.iloc[home_goals, away_goals]
            if home_goals > away_goals:
                home_win_prob += prob
            elif home_goals == away_goals:
                draw_prob += prob
            else:
                away_win_prob += prob
            if (home_goals + away_goals) >= 3:
                over_2_5_prob += prob
            if home_goals > 0 and away_goals > 0:
                btts_yes_prob += prob

    under_2_5_prob = max(0.0, 1 - over_2_5_prob)
    btts_no_prob = max(0.0, 1 - btts_yes_prob)

    # Half-time prediction using scaled xG (~45% of full-match for first half)
    half_scaling = 0.45
    home_half_xg = home_xg * half_scaling
    away_half_xg = away_xg * half_scaling

    # Build half-time score matrix
    half_matrix = build_score_matrix(home_half_xg, away_half_xg)

    home_half_prob = 0.0
    draw_half_prob = 0.0
    away_half_prob = 0.0

    for home_goals in half_matrix.index:
        for away_goals in half_matrix.columns:
            prob = half_matrix.iloc[home_goals, away_goals]
            if home_goals > away_goals:
                home_half_prob += prob
            elif home_goals == away_goals:
                draw_half_prob += prob
            else:
                away_half_prob += prob

    return MatchPrediction(
        home_win_prob=home_win_prob,
        draw_prob=draw_prob,
        away_win_prob=away_win_prob,
        over_2_5_prob=over_2_5_prob,
        under_2_5_prob=under_2_5_prob,
        btts_yes_prob=btts_yes_prob,
        btts_no_prob=btts_no_prob,
        expected_home_goals=home_xg,
        expected_away_goals=away_xg,
        home_half_prob=home_half_prob,
        draw_half_prob=draw_half_prob,
        away_half_prob=away_half_prob,
        expected_home_half_goals=home_half_xg,
        expected_away_half_goals=away_half_xg,
    )

