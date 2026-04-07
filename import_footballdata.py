#!/usr/bin/env python3
"""匯入 Football-Data.co.uk 英超 E0.csv 到 SQLite。"""

from __future__ import annotations

import argparse
import csv
import io
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests

DB_PATH = Path(__file__).resolve().parent / "football.db"
DEFAULT_CSV_URL = "https://www.football-data.co.uk/mmz4281/2025/E0.csv"
SOURCE = "football-data.co.uk"

# Football-Data.co.uk 用短名；呢度對返 football-data.org / 現有 DB 名稱。
FOOTBALL_DATA_TEAM_MAPPING = {
    "Arsenal": "Arsenal FC",
    "Aston Villa": "Aston Villa FC",
    "Bournemouth": "AFC Bournemouth",
    "Brentford": "Brentford FC",
    "Brighton": "Brighton & Hove Albion FC",
    "Burnley": "Burnley FC",
    "Chelsea": "Chelsea FC",
    "Crystal Palace": "Crystal Palace FC",
    "Everton": "Everton FC",
    "Fulham": "Fulham FC",
    "Ipswich": "Ipswich Town FC",
    "Leeds": "Leeds United FC",
    "Leicester": "Leicester City FC",
    "Liverpool": "Liverpool FC",
    "Man City": "Manchester City FC",
    "Man United": "Manchester United FC",
    "Newcastle": "Newcastle United FC",
    "Nott'm Forest": "Nottingham Forest FC",
    "Nottingham Forest": "Nottingham Forest FC",
    "Southampton": "Southampton FC",
    "Sunderland": "Sunderland AFC",
    "Tottenham": "Tottenham Hotspur FC",
    "West Ham": "West Ham United FC",
    "Wolves": "Wolverhampton Wanderers FC",
}


def ensure_tables(conn: sqlite3.Connection) -> None:
    """建立匯入需要用到嘅 table。"""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS team_name_mapping (
            source TEXT NOT NULL,
            source_name TEXT NOT NULL,
            canonical_name TEXT NOT NULL,
            team_id INTEGER,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (source, source_name)
        )
        """
    )
    conn.execute(
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
        """
    )


def infer_season_from_url(url: str) -> str:
    """由 URL path 估 season 代碼，估唔到就用 unknown。"""
    match = re.search(r"/mmz4281/([^/]+)/", urlparse(url).path)
    return match.group(1) if match else "unknown"


def parse_match_date(value: str) -> str:
    """將 CSV 日期轉成 ISO date，兼容 dd/mm/yy 同 dd/mm/yyyy。"""
    value = (value or "").strip()
    for fmt in ("%d/%m/%y", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            continue
    raise ValueError(f"未能解析賽事日期: {value!r}")


def load_team_ids(conn: sqlite3.Connection) -> dict[str, int]:
    """讀取現有 teams table，方便 mapping source name 去 team_id。"""
    rows = conn.execute("SELECT team_id, name FROM teams").fetchall()
    return {name: int(team_id) for team_id, name in rows}


def upsert_team_mapping(conn: sqlite3.Connection, team_ids: dict[str, int]) -> None:
    """寫入 Football-Data.co.uk team name mapping，可重跑。"""
    rows = [
        (SOURCE, source_name, canonical_name, team_ids.get(canonical_name))
        for source_name, canonical_name in FOOTBALL_DATA_TEAM_MAPPING.items()
    ]
    conn.executemany(
        """
        INSERT INTO team_name_mapping (source, source_name, canonical_name, team_id, updated_at)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT (source, source_name) DO UPDATE SET
            canonical_name=excluded.canonical_name,
            team_id=excluded.team_id,
            updated_at=CURRENT_TIMESTAMP
        """,
        rows,
    )


def download_csv(url: str) -> str:
    """下載 CSV；如果 URL 唔係 CSV 回應就直接報錯。"""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    text = response.text
    if not text.lstrip().startswith("Div,"):
        raise RuntimeError(
            "Football-Data.co.uk 回應唔似 E0.csv；"
            f"status={response.status_code}, content-type={response.headers.get('content-type')!r}"
        )
    return text


def build_historical_rows(csv_text: str, url: str, mappings: dict[str, tuple[str, int | None]]) -> list[tuple]:
    """將 Football-Data.co.uk CSV rows 轉成 h2h_historical rows。"""
    season = infer_season_from_url(url)
    reader = csv.DictReader(io.StringIO(csv_text))
    rows = []
    for row in reader:
        home = (row.get("HomeTeam") or "").strip()
        away = (row.get("AwayTeam") or "").strip()
        if not home or not away or not row.get("Date"):
            continue

        home_goals = row.get("FTHG")
        away_goals = row.get("FTAG")
        rows.append(
            (
                SOURCE,
                (row.get("Div") or "E0").strip(),
                season,
                parse_match_date(row["Date"]),
                home,
                away,
                mappings.get(home, (home, None))[1],
                mappings.get(away, (away, None))[1],
                int(home_goals) if home_goals not in (None, "") else None,
                int(away_goals) if away_goals not in (None, "") else None,
                (row.get("FTR") or "").strip() or None,
                url,
            )
        )
    return rows


def import_football_data(url: str = DEFAULT_CSV_URL, db_path: Path = DB_PATH) -> int:
    """下載並匯入 Football-Data.co.uk E0.csv，回傳寫入行數。"""
    csv_text = download_csv(url)
    with sqlite3.connect(db_path) as conn:
        ensure_tables(conn)
        team_ids = load_team_ids(conn)
        upsert_team_mapping(conn, team_ids)
        mapping_rows = conn.execute(
            """
            SELECT source_name, canonical_name, team_id
            FROM team_name_mapping
            WHERE source = ?
            """,
            (SOURCE,),
        ).fetchall()
        mappings = {source_name: (canonical_name, team_id) for source_name, canonical_name, team_id in mapping_rows}
        rows = build_historical_rows(csv_text, url, mappings)
        conn.executemany(
            """
            INSERT INTO h2h_historical (
                source, division, season, match_date,
                home_team_name, away_team_name,
                home_team_id, away_team_id,
                home_goals, away_goals, result, source_url, imported_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT (source, division, season, match_date, home_team_name, away_team_name) DO UPDATE SET
                home_team_id=excluded.home_team_id,
                away_team_id=excluded.away_team_id,
                home_goals=excluded.home_goals,
                away_goals=excluded.away_goals,
                result=excluded.result,
                source_url=excluded.source_url,
                imported_at=CURRENT_TIMESTAMP
            """,
            rows,
        )
        conn.commit()
        return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="匯入 Football-Data.co.uk 英超 E0.csv 到 football.db。")
    parser.add_argument("--url", default=DEFAULT_CSV_URL, help="Football-Data.co.uk E0.csv URL")
    parser.add_argument("--db", type=Path, default=DB_PATH, help="SQLite football.db 路徑")
    args = parser.parse_args()

    try:
        imported = import_football_data(args.url, args.db)
    except Exception as exc:
        print(f"匯入失敗：{exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print(f"已匯入 {imported} 筆 Football-Data.co.uk H2H 賽事")


if __name__ == "__main__":
    main()
