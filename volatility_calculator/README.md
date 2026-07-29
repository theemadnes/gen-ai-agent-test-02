# Volatility Calculator Agent (Agent 2)

This agent reads the top stocks evaluated by Agent 1 (`SP500EvaluatorAgent`), downloads their historical price data over the past 2 weeks (14 days), and calculates key volatility indexes and metrics.

## Setup

A dedicated virtual environment is configured in `.venv`.

To recreate or update dependencies:
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Usage

Ensure Agent 1 has generated `top_10_stocks.json`, then run:

```bash
.venv/bin/python main.py
```

## Metrics Calculated

1. **Daily Volatility (%)**: Standard deviation of daily percentage price returns over the past 2 weeks.
2. **Annualized Volatility Index (%)**: $\sigma_{\text{daily}} \times \sqrt{252}$ representing annualized price volatility.
3. **Parkinson Volatility Index (%)**: Range-based volatility metric using intraday High and Low prices.
4. **2-Week Return (%)**: Total price return percentage over the 14-day window.
5. **Max Gain & Loss (%)**: Largest single-day gain and loss in the 2-week period.
