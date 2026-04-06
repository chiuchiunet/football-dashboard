import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "football.db"

API_PROVIDER = os.getenv("FOOTBALL_API_PROVIDER", "football-data")
API_BASE_URL = os.getenv("FOOTBALL_API_BASE_URL", "https://api.football-data.org/v4")
API_KEY = os.getenv("FOOTBALL_API_KEY", "")

DEFAULT_COMPETITIONS = [
    "PL",    # Premier League
    "CL",    # Champions League
    "PD",    # La Liga
    "SA",    # Serie A
    "BL1",   # Bundesliga
    "FL1",   # Ligue 1
]

DEFAULT_LOOKBACK_MATCHES = int(os.getenv("DEFAULT_LOOKBACK_MATCHES", "10"))
FORM_MATCH_COUNT = int(os.getenv("FORM_MATCH_COUNT", "5"))
HOME_ADVANTAGE_MULTIPLIER = float(os.getenv("HOME_ADVANTAGE_MULTIPLIER", "1.08"))
MAX_GOALS = int(os.getenv("MAX_GOALS", "7"))
MIN_VALUE_EDGE = float(os.getenv("MIN_VALUE_EDGE", "0.05"))

LOCAL_TZ = os.getenv("FOOTBALL_LOCAL_TZ", "Asia/Hong_Kong")
DEFAULT_LANGUAGE = os.getenv("FOOTBALL_OUTPUT_LANG", "zh")

ODDS_FILE = os.getenv("FOOTBALL_ODDS_FILE", str(BASE_DIR / "sample_odds.csv"))

