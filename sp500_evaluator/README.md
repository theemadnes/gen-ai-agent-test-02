# S&P 500 Evaluator Agent (Agent 1)

This agent evaluates S&P 500 companies and identifies the top 10 most valuable stocks based on market capitalization.

## Setup

A dedicated virtual environment is configured in `.venv`.

To recreate or update dependencies:
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Usage

Run the evaluator agent using its dedicated virtual environment:

```bash
.venv/bin/python main.py
```

## Output

The agent generates `top_10_stocks.json` containing:
- Symbol / Ticker
- Company Name
- Sector
- Market Capitalization (Numeric & Formatted)
- Current Price
