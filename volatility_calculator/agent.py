import json
import logging
import math
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
import yfinance as yf

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class VolatilityCalculatorAgent:
    """
    Agent 2: Calculates volatility indexes and risk metrics for the top stocks 
    over the past 2 weeks (14 calendar days / ~10 trading days).
    """

    def __init__(self, period_days: int = 14):
        self.period_days = period_days

    def calculate_stock_volatility(self, symbol: str, df_history: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """Calculate volatility metrics for a single stock given historical price DataFrame."""
        if df_history.empty or len(df_history) < 2:
            logging.warning(f"Insufficient historical price data for ticker {symbol}")
            return None

        # Sort chronologically
        df = df_history.sort_index().copy()

        # Handle multi-level columns if necessary
        close = df["Close"]
        if isinstance(close, pd.DataFrame):
            close = close.squeeze()

        # Calculate daily returns
        daily_returns = close.pct_change().dropna()
        if len(daily_returns) < 1:
            return None

        # Standard deviation of daily returns
        daily_std_dev = float(daily_returns.std())
        
        # Annualized Volatility Index (%): daily_std * sqrt(252 trading days)
        annualized_volatility = float(daily_std_dev * math.sqrt(252))

        # Overall 2-week performance
        start_price = float(close.iloc[0])
        end_price = float(close.iloc[-1])
        total_2week_return = float(((end_price - start_price) / start_price) * 100)

        # Parkinson Volatility Index (high-low price range volatility measure)
        parkinson_vol = None
        if "High" in df.columns and "Low" in df.columns:
            high = df["High"]
            low = df["Low"]
            if isinstance(high, pd.DataFrame):
                high = high.squeeze()
                low = low.squeeze()
            hl_ratio = np.log(high / low)
            parkinson_daily = np.sqrt((1 / (4 * np.log(2))) * (hl_ratio ** 2).mean())
            parkinson_vol = float(parkinson_daily * math.sqrt(252))

        return {
            "period_start_date": str(df.index[0].strftime("%Y-%m-%d")),
            "period_end_date": str(df.index[-1].strftime("%Y-%m-%d")),
            "trading_days": len(close),
            "start_price": round(start_price, 2),
            "end_price": round(end_price, 2),
            "total_2week_return_pct": round(total_2week_return, 2),
            "daily_volatility_pct": round(daily_std_dev * 100, 2),
            "annualized_volatility_index_pct": round(annualized_volatility * 100, 2),
            "parkinson_volatility_index_pct": round(parkinson_vol * 100, 2) if parkinson_vol is not None else None,
            "max_daily_gain_pct": round(float(daily_returns.max() * 100), 2),
            "max_daily_loss_pct": round(float(daily_returns.min() * 100), 2)
        }

    def process_stocks(self, stocks_input: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processes stock list from Agent 1 and calculates volatility metrics."""
        symbols = [s["symbol"] for s in stocks_input if "symbol" in s]
        if not symbols:
            raise ValueError("No valid stock symbols provided in input data.")

        logging.info(f"Downloading past {self.period_days}-day stock prices for: {symbols}")

        results = []
        for stock_meta in stocks_input:
            symbol = stock_meta["symbol"]
            try:
                # Fetch 2-week history directly per ticker for precision
                df = yf.Ticker(symbol).history(period=f"{self.period_days}d")
                vol_metrics = self.calculate_stock_volatility(symbol, df)
                
                if vol_metrics:
                    record = {
                        "symbol": symbol,
                        "name": stock_meta.get("name", symbol),
                        "sector": stock_meta.get("sector", "N/A"),
                        "market_cap_formatted": stock_meta.get("market_cap_formatted", "N/A"),
                        **vol_metrics
                    }
                    results.append(record)
            except Exception as e:
                logging.error(f"Failed calculating volatility for {symbol}: {e}")

        # Rank stocks by annualized volatility index descending (highest volatility first)
        results.sort(key=lambda x: x["annualized_volatility_index_pct"], reverse=True)
        return results

    def run(self, input_file: str = "../sp500_evaluator/top_10_stocks.json", output_file: str = "volatility_report.json") -> List[Dict[str, Any]]:
        input_path = Path(input_file)
        if not input_path.exists():
            # Try checking current directory if relative path differs
            if Path(input_path.name).exists():
                input_path = Path(input_path.name)
            else:
                raise FileNotFoundError(f"Input file '{input_file}' not found. Please run Agent 1 first.")

        logging.info(f"Reading input stocks from '{input_path}'...")
        with open(input_path, "r") as f:
            data = json.load(f)

        top_stocks = data.get("top_stocks", data if isinstance(data, list) else [])
        volatility_results = self.process_stocks(top_stocks)

        report = {
            "agent": "VolatilityCalculatorAgent",
            "timeframe": f"Past {self.period_days} Days (2 Weeks)",
            "stock_count": len(volatility_results),
            "volatility_report": volatility_results
        }

        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

        logging.info(f"Volatility analysis report saved to '{output_file}'.")
        return volatility_results
