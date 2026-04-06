# Football Match Prediction System

This project fetches football fixtures and statistics from a free API (`football-data.org` by default), stores them in SQLite, and generates Poisson-based match predictions with value bet detection.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FOOTBALL_API_KEY="your_football_data_api_key"
```

## Fetch data

```bash
python fetch_data.py --days-ahead 7 --competitions PL CL PD SA BL1 FL1
```

## Generate predictions

```bash
python predict.py --days-ahead 7 --lang zh
```

## Notes

- `sample_odds.csv` is the local odds input used for value-bet comparison. Replace it with bookmaker odds when available.
- Output is formatted for WhatsApp, with bilingual Chinese/English lines and emoji.
