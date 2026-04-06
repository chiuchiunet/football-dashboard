from __future__ import annotations

from typing import Iterable

import pandas as pd


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def format_predictions_whatsapp(predictions: pd.DataFrame, language: str = "zh") -> str:
    if predictions.empty:
        return "⚠️ 暫時冇可用賽事預測 / No predictions available."

    blocks = []
    header = "⚽ 足球賽事預測\nFootball Match Predictions"
    blocks.append(header)

    for _, row in predictions.iterrows():
        if language == "zh":
            lines = [
                f"📅 {row['kickoff_hk']}",
                f"🏟️ {row['competition_code']} | {row['home_team_name']} vs {row['away_team_name']}",
                f"🔢 模型入球: {row['expected_home_goals']:.2f} - {row['expected_away_goals']:.2f}",
                f"📊 勝和負: 主勝 {pct(row['home_win_prob'])} | 和 {pct(row['draw_prob'])} | 客勝 {pct(row['away_win_prob'])}",
                f"🎯 大細2.5: 大 {pct(row['over_2_5_prob'])} | 細 {pct(row['under_2_5_prob'])}",
                f"🤝 BTTS: Yes {pct(row['btts_yes_prob'])} | No {pct(row['btts_no_prob'])}",
                f"💎 Value Bets: {row['recommended_bets'] or '暫無'}",
            ]
        else:
            lines = [
                f"📅 {row['kickoff_hk']}",
                f"🏟️ {row['competition_code']} | {row['home_team_name']} vs {row['away_team_name']}",
                f"🔢 Model xG: {row['expected_home_goals']:.2f} - {row['expected_away_goals']:.2f}",
                f"📊 1X2: Home {pct(row['home_win_prob'])} | Draw {pct(row['draw_prob'])} | Away {pct(row['away_win_prob'])}",
                f"🎯 O/U 2.5: Over {pct(row['over_2_5_prob'])} | Under {pct(row['under_2_5_prob'])}",
                f"🤝 BTTS: Yes {pct(row['btts_yes_prob'])} | No {pct(row['btts_no_prob'])}",
                f"💎 Value Bets: {row['recommended_bets'] or 'None'}",
            ]
        blocks.append("\n".join(lines))

    return "\n\n".join(blocks)

