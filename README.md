# Multi-Agent S&P 500 & Volatility Analysis Pipeline

This project consists of two specialized, autonomous Python agents that run in their own isolated virtual environments and work together in a data pipeline:

1. **Agent 1 (`sp500_evaluator`)**: Evaluates S&P 500 index companies, retrieves real-time market capitalization data, and identifies the **top 10 most valuable stocks**. Outputs `top_10_stocks.json`.
2. **Agent 2 (`volatility_calculator`)**: Ingests Agent 1's output, fetches historical stock price data over the **past 2 weeks (14 days)**, and calculates daily standard deviation, annualized volatility indexes, and range-based volatility metrics (e.g., Parkinson Volatility). Outputs `volatility_report.json`.

---

## Project Directory Structure

```
gen-ai-agent-test-02/
│
├── sp500_evaluator/             # Agent 1 Directory
│   ├── .venv/                   # Agent 1 Python Virtual Environment
│   ├── agent.py                 # SP500EvaluatorAgent implementation
│   ├── main.py                  # CLI runner for Agent 1
│   ├── requirements.txt         # Agent 1 dependencies (yfinance, pandas, lxml, etc.)
│   ├── top_10_stocks.json       # Generated output artifact
│   └── README.md
│
├── volatility_calculator/       # Agent 2 Directory
│   ├── .venv/                   # Agent 2 Python Virtual Environment
│   ├── agent.py                 # VolatilityCalculatorAgent implementation
│   ├── main.py                  # CLI runner for Agent 2
│   ├── requirements.txt         # Agent 2 dependencies (yfinance, pandas, numpy, etc.)
│   ├── volatility_report.json   # Generated output artifact
│   └── README.md
│
└── run_pipeline.py              # Root orchestrator script to run both agents end-to-end
```

---

## Quick Start / Usage

### Run Full Pipeline End-to-End
Execute the orchestrator script to run both agents in sequence:
```bash
python3 run_pipeline.py
```

### Running Agents Individually

#### Agent 1: S&P 500 Evaluator
```bash
cd sp500_evaluator
.venv/bin/python main.py
```

#### Agent 2: Volatility Calculator
```bash
cd volatility_calculator
.venv/bin/python main.py
```

---

## Agent Output Examples

### `sp500_evaluator/top_10_stocks.json`
```json
{
  "agent": "SP500EvaluatorAgent",
  "description": "Top 10 Most Valuable S&P 500 Stocks by Market Capitalization",
  "stock_count": 10,
  "top_stocks": [
    {
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "sector": "Information Technology",
      "market_cap": 4990000000000.0,
      "current_price": 245.5,
      "market_cap_formatted": "$4.99T"
    }, ...
  ]
}
```

### `volatility_calculator/volatility_report.json`
```json
{
  "agent": "VolatilityCalculatorAgent",
  "timeframe": "Past 14 Days (2 Weeks)",
  "stock_count": 10,
  "volatility_report": [
    {
      "symbol": "TSLA",
      "name": "Tesla Inc.",
      "sector": "Consumer Discretionary",
      "market_cap_formatted": "$1.21T",
      "period_start_date": "2026-07-15",
      "period_end_date": "2026-07-28",
      "trading_days": 10,
      "start_price": 210.5,
      "end_price": 235.0,
      "total_2week_return_pct": 11.64,
      "daily_volatility_pct": 2.85,
      "annualized_volatility_index_pct": 45.24,
      "parkinson_volatility_index_pct": 42.10,
      "max_daily_gain_pct": 5.40,
      "max_daily_loss_pct": -2.10
    }, ...
  ]
}
```
