import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import pandas as pd

from config import DB_PATH


SCHEMA_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS competitions (
        code TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        area_name TEXT,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS teams (
        team_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        short_name TEXT,
        tla TEXT,
        venue TEXT,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS matches (
        match_id INTEGER PRIMARY KEY,
        competition_code TEXT NOT NULL,
        utc_date TEXT NOT NULL,
        status TEXT NOT NULL,
        stage TEXT,
        matchday INTEGER,
        home_team_id INTEGER NOT NULL,
        away_team_id INTEGER NOT NULL,
        home_team_name TEXT NOT NULL,
        away_team_name TEXT NOT NULL,
        home_score INTEGER,
        away_score INTEGER,
        winner TEXT,
        last_updated TEXT,
        raw_json TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS standings (
        competition_code TEXT NOT NULL,
        season_start TEXT,
        team_id INTEGER NOT NULL,
        position INTEGER,
        played_games INTEGER,
        won INTEGER,
        draw INTEGER,
        lost INTEGER,
        goals_for INTEGER,
        goals_against INTEGER,
        goal_difference INTEGER,
        points INTEGER,
        form TEXT,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (competition_code, team_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS team_form (
        team_id INTEGER NOT NULL,
        competition_code TEXT NOT NULL,
        form_window INTEGER NOT NULL,
        matches_played INTEGER NOT NULL,
        wins INTEGER NOT NULL,
        draws INTEGER NOT NULL,
        losses INTEGER NOT NULL,
        goals_for REAL NOT NULL,
        goals_against REAL NOT NULL,
        points_per_match REAL NOT NULL,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (team_id, competition_code, form_window)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS h2h_stats (
        team_id INTEGER NOT NULL,
        opponent_team_id INTEGER NOT NULL,
        matches_played INTEGER NOT NULL,
        wins INTEGER NOT NULL,
        draws INTEGER NOT NULL,
        losses INTEGER NOT NULL,
        goals_for REAL NOT NULL,
        goals_against REAL NOT NULL,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (team_id, opponent_team_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS team_name_mapping (
        source TEXT NOT NULL,
        source_name TEXT NOT NULL,
        canonical_name TEXT NOT NULL,
        team_id INTEGER,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (source, source_name)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS h2h_historical (
        source TEXT NOT NULL,
        division TEXT NOT NULL,
        season TEXT NOT NULL,
        match_date TEXT NOT NULL,
        home_team_name TEXT NOT NULL,
        away_team_name TEXT NOT NULL,
        home_team_id INTEGER,
        away_team_id INTEGER,
        home_goals INTEGER,
        away_goals INTEGER,
        result TEXT,
        source_url TEXT NOT NULL,
        imported_at TEXT DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (source, division, season, match_date, home_team_name, away_team_name)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS bookmaker_odds (
        match_id INTEGER PRIMARY KEY,
        bookmaker TEXT NOT NULL,
        home_win_odds REAL,
        draw_odds REAL,
        away_win_odds REAL,
        over_2_5_odds REAL,
        under_2_5_odds REAL,
        btts_yes_odds REAL,
        btts_no_odds REAL,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS predictions (
        prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER NOT NULL,
        generated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        model TEXT NOT NULL,
        home_win_prob REAL NOT NULL,
        draw_prob REAL NOT NULL,
        away_win_prob REAL NOT NULL,
        over_2_5_prob REAL NOT NULL,
        under_2_5_prob REAL NOT NULL,
        btts_yes_prob REAL NOT NULL,
        btts_no_prob REAL NOT NULL,
        expected_home_goals REAL NOT NULL,
        expected_away_goals REAL NOT NULL,
        recommended_bets TEXT,
        output_text TEXT
    )
    """,
]


class Database:
    def __init__(self, db_path: Path | str = DB_PATH):
        self.db_path = str(db_path)

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def initialize(self) -> None:
        with self.connect() as conn:
            for statement in SCHEMA_STATEMENTS:
                conn.execute(statement)

    def upsert_dataframe(self, table: str, frame: pd.DataFrame, key_columns: Sequence[str]) -> None:
        if frame.empty:
            return
        columns = list(frame.columns)
        placeholders = ", ".join(["?"] * len(columns))
        update_columns = [column for column in columns if column not in key_columns]
        update_sql = ", ".join([f"{column}=excluded.{column}" for column in update_columns])
        sql = f"""
            INSERT INTO {table} ({", ".join(columns)})
            VALUES ({placeholders})
            ON CONFLICT ({", ".join(key_columns)}) DO UPDATE SET {update_sql}
        """
        with self.connect() as conn:
            conn.executemany(sql, frame.itertuples(index=False, name=None))

    def insert_many(self, table: str, rows: Iterable[Mapping]) -> None:
        rows = list(rows)
        if not rows:
            return
        columns = list(rows[0].keys())
        sql = f"""
            INSERT INTO {table} ({", ".join(columns)})
            VALUES ({", ".join(["?"] * len(columns))})
        """
        values = [tuple(row[column] for column in columns) for row in rows]
        with self.connect() as conn:
            conn.executemany(sql, values)

    def read_sql(self, query: str, params: Sequence | None = None) -> pd.DataFrame:
        with self.connect() as conn:
            return pd.read_sql_query(query, conn, params=params)
