from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from config import DEFAULT_LANGUAGE, LOCAL_TZ, MIN_VALUE_EDGE
from database import Database
from models.poisson import predict_match
from output_formatter import format_predictions_whatsapp


def implied_probability(odds: float | None) -> float | None:
    if odds is None or pd.isna(odds) or odds <= 1:
        return None
    return 1 / odds


def find_value_bets(prediction: dict, odds_row: pd.Series | None, min_edge: float = MIN_VALUE_EDGE) -> str:
    if odds_row is None:
        return ""
    markets = {
        "Home Win": ("home_win_prob", odds_row.get("home_win_odds")),
        "Draw": ("draw_prob", odds_row.get("draw_odds")),
        "Away Win": ("away_win_prob", odds_row.get("away_win_odds")),
        "Over 2.5": ("over_2_5_prob", odds_row.get("over_2_5_odds")),
        "Under 2.5": ("under_2_5_prob", odds_row.get("under_2_5_odds")),
        "BTTS Yes": ("btts_yes_prob", odds_row.get("btts_yes_odds")),
        "BTTS No": ("btts_no_prob", odds_row.get("btts_no_odds")),
    }
    value_bets = []
    for label, (prob_key, odds) in markets.items():
        implied = implied_probability(odds)
        if implied is None:
            continue
        edge = prediction[prob_key] - implied
        if edge >= min_edge:
            value_bets.append(f"{label} @{odds:.2f} (+{edge * 100:.1f}%)")
    return ", ".join(value_bets)


def load_prediction_inputs(db: Database, days_ahead: int) -> pd.DataFrame:
    query = """
        SELECT m.*, o.bookmaker, o.home_win_odds, o.draw_odds, o.away_win_odds,
               o.over_2_5_odds, o.under_2_5_odds, o.btts_yes_odds, o.btts_no_odds
        FROM matches m
        LEFT JOIN bookmaker_odds o ON o.match_id = m.match_id
        WHERE m.status IN ('SCHEDULED', 'TIMED')
          AND datetime(m.utc_date) <= datetime('now', ?)
        ORDER BY datetime(m.utc_date) ASC
    """
    return db.read_sql(query, params=[f"+{days_ahead} days"])


def build_predictions(days_ahead: int = 7) -> pd.DataFrame:
    db = Database()
    db.initialize()
    matches = load_prediction_inputs(db, days_ahead)
    if matches.empty:
        return pd.DataFrame()

    standings = db.read_sql("SELECT * FROM standings")
    team_form = db.read_sql("SELECT * FROM team_form")
    h2h_stats = db.read_sql("SELECT * FROM h2h_stats")

    rows = []
    for _, match in matches.iterrows():
        competition_standings = standings.loc[standings["competition_code"] == match["competition_code"]]
        competition_form = team_form.loc[team_form["competition_code"] == match["competition_code"]]
        prediction = predict_match(
            int(match["home_team_id"]),
            int(match["away_team_id"]),
            competition_standings,
            competition_form,
            h2h_stats,
            home_team_name=str(match["home_team_name"]),
            away_team_name=str(match["away_team_name"]),
        )
        prediction_dict = prediction.__dict__.copy()
        value_bets = find_value_bets(prediction_dict, match)
        kickoff_hk = pd.Timestamp(match["utc_date"], tz="UTC").tz_convert(LOCAL_TZ).strftime("%Y-%m-%d %H:%M")
        output_row = {
            "match_id": int(match["match_id"]),
            "kickoff_hk": kickoff_hk,
            "competition_code": match["competition_code"],
            "home_team_name": match["home_team_name"],
            "away_team_name": match["away_team_name"],
            "recommended_bets": value_bets,
            **prediction_dict,
        }
        rows.append(output_row)

    output = pd.DataFrame(rows)

    insert_frame = output.copy()
    insert_frame["model"] = "poisson"
    insert_frame["output_text"] = None
    insert_frame = insert_frame[[
        "match_id", "model", "home_win_prob", "draw_prob", "away_win_prob", "over_2_5_prob",
        "under_2_5_prob", "btts_yes_prob", "btts_no_prob", "expected_home_goals",
        "expected_away_goals", "recommended_bets", "output_text"
    ]]
    db.insert_many("predictions", insert_frame.to_dict(orient="records"))

    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Poisson-based football predictions.")
    parser.add_argument("--days-ahead", type=int, default=7)
    parser.add_argument("--lang", default=DEFAULT_LANGUAGE, choices=["zh", "en"])
    parser.add_argument("--html", action="store_true", help="Generate HTML dashboard")
    args = parser.parse_args()

    predictions = build_predictions(days_ahead=args.days_ahead)
    
    if args.html:
        from generate_html import generate_html as gen_html
        html = gen_html(predictions, title="⚽ 足球預測報告")
        output_path = Path(__file__).resolve().parent / "web" / "index.html"
        output_path.write_text(html, encoding="utf-8")
        print(f"✅ HTML Dashboard written to: {output_path}")
        print(f"📊 Total predictions: {len(predictions)}")
    else:
        print(format_predictions_whatsapp(predictions, language=args.lang))


if __name__ == "__main__":
    main()
