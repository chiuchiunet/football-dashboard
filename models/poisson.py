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


def expected_goals(
    home_team_id: int,
    away_team_id: int,
    standings: pd.DataFrame,
    recent_form: pd.DataFrame,
    h2h_stats: pd.DataFrame,
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

    h2h_home_boost = 1.0
    h2h_away_boost = 1.0
    if not h2h.empty and h2h.iloc[0]["matches_played"] >= 2:
        h2h_home_boost = 0.9 + min(h2h.iloc[0]["goals_for"] / max(h2h.iloc[0]["matches_played"], 1), 0.4)
        h2h_away_boost = 0.9 + min(h2h.iloc[0]["goals_against"] / max(h2h.iloc[0]["matches_played"], 1), 0.4)

    home_xg = base_home * home_attack * away_defense * home_form_boost * HOME_ADVANTAGE_MULTIPLIER
    away_xg = base_away * away_attack * home_defense * away_form_boost

    home_xg *= h2h_home_boost
    away_xg *= h2h_away_boost

    return round(max(home_xg, 0.2), 3), round(max(away_xg, 0.2), 3)


def predict_match(
    home_team_id: int,
    away_team_id: int,
    standings: pd.DataFrame,
    recent_form: pd.DataFrame,
    h2h_stats: pd.DataFrame,
) -> MatchPrediction:
    home_xg, away_xg = expected_goals(home_team_id, away_team_id, standings, recent_form, h2h_stats)
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
    )

