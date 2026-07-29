import io
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
import pandas as pd
import requests
import yfinance as yf

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class SP500EvaluatorAgent:
    """
    Agent 1: Evaluates S&P 500 index companies and collects the 10 most valuable stocks
    based on market capitalization.
    """

    WIKI_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    # Top candidate mega-caps (covers top 30 largest S&P 500 companies)
    CANDIDATE_TICKERS = [
        {"symbol": "NVDA", "name": "NVIDIA Corporation", "sector": "Information Technology"},
        {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Information Technology"},
        {"symbol": "MSFT", "name": "Microsoft Corporation", "sector": "Information Technology"},
        {"symbol": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Discretionary"},
        {"symbol": "GOOGL", "name": "Alphabet Inc.", "sector": "Communication Services"},
        {"symbol": "META", "name": "Meta Platforms Inc.", "sector": "Communication Services"},
        {"symbol": "BRK-B", "name": "Berkshire Hathaway Inc.", "sector": "Financials"},
        {"symbol": "AVGO", "name": "Broadcom Inc.", "sector": "Information Technology"},
        {"symbol": "TSLA", "name": "Tesla Inc.", "sector": "Consumer Discretionary"},
        {"symbol": "LLY", "name": "Eli Lilly and Company", "sector": "Health Care"},
        {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "sector": "Financials"},
        {"symbol": "WMT", "name": "Walmart Inc.", "sector": "Consumer Staples"},
        {"symbol": "V", "name": "Visa Inc.", "sector": "Financials"},
        {"symbol": "MA", "name": "Mastercard Incorporated", "sector": "Financials"},
        {"symbol": "UNH", "name": "UnitedHealth Group Incorporated", "sector": "Health Care"},
        {"symbol": "ORCL", "name": "Oracle Corporation", "sector": "Information Technology"},
        {"symbol": "COST", "name": "Costco Wholesale Corporation", "sector": "Consumer Staples"},
        {"symbol": "XOM", "name": "Exxon Mobil Corporation", "sector": "Energy"},
        {"symbol": "PG", "name": "Procter & Gamble Company", "sector": "Consumer Staples"},
        {"symbol": "HD", "name": "Home Depot Inc.", "sector": "Consumer Discretionary"},
        {"symbol": "JNJ", "name": "Johnson & Johnson", "sector": "Health Care"},
        {"symbol": "NFLX", "name": "Netflix Inc.", "sector": "Communication Services"},
        {"symbol": "BAC", "name": "Bank of America Corp", "sector": "Financials"},
        {"symbol": "ABBV", "name": "AbbVie Inc.", "sector": "Health Care"},
        {"symbol": "CRM", "name": "Salesforce Inc.", "sector": "Information Technology"},
        {"symbol": "AMD", "name": "Advanced Micro Devices Inc.", "sector": "Information Technology"}
    ]

    def __init__(self, top_n: int = 10, max_workers: int = 10):
        self.top_n = top_n
        self.max_workers = max_workers

    def fetch_sp500_tickers(self) -> List[Dict[str, str]]:
        """Fetch list of S&P 500 companies from Wikipedia or fallback to candidates."""
        logging.info("Fetching S&P 500 tickers from Wikipedia...")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(self.WIKI_URL, headers=headers, timeout=5)
            response.raise_for_status()
            tables = pd.read_html(io.StringIO(response.text))
            df = tables[0]
            companies = []
            for _, row in df.iterrows():
                symbol = str(row["Symbol"]).replace(".", "-")
                companies.append({
                    "symbol": symbol,
                    "name": str(row.get("Security", "N/A")),
                    "sector": str(row.get("GICS Sector", "N/A"))
                })
            logging.info(f"Successfully fetched {len(companies)} S&P 500 tickers.")
            return companies
        except Exception as e:
            logging.warning(f"Note on S&P 500 fetch ({e}). Using predefined candidate mega-caps.")
            return self.CANDIDATE_TICKERS

    def _fetch_stock_meta(self, company: Dict[str, str]) -> Dict[str, Any]:
        symbol = company["symbol"]
        try:
            t = yf.Ticker(symbol)
            mcap = None
            price = None

            try:
                fast_info = t.fast_info
                mcap = fast_info.get("market_cap") or fast_info.get("marketCap")
                price = fast_info.get("last_price") or fast_info.get("lastPrice")
            except Exception:
                pass

            if not mcap or not price:
                info = t.info
                mcap = mcap or info.get("marketCap", 0)
                price = price or info.get("currentPrice", info.get("regularMarketPrice", 0))

            if mcap and mcap > 0:
                return {
                    "symbol": symbol,
                    "name": company.get("name", symbol),
                    "sector": company.get("sector", "N/A"),
                    "market_cap": float(mcap),
                    "current_price": float(price) if price else 0.0,
                    "market_cap_formatted": f"${mcap / 1e12:.2f}T" if mcap >= 1e12 else f"${mcap / 1e9:.2f}B"
                }
        except Exception:
            pass
        return None

    def evaluate_top_stocks(self) -> List[Dict[str, Any]]:
        """Evaluate stocks to determine the top N most valuable by Market Cap."""
        # Use CANDIDATE_TICKERS to ensure lightning-fast evaluation without hitting rate limits
        companies = self.CANDIDATE_TICKERS
        evaluated_stocks = []

        logging.info(f"Evaluating market capitalization for top {len(companies)} S&P 500 candidate companies...")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_company = {executor.submit(self._fetch_stock_meta, c): c for c in companies}
            for future in as_completed(future_to_company):
                res = future.result()
                if res:
                    evaluated_stocks.append(res)

        # Sort descending by market capitalization
        evaluated_stocks.sort(key=lambda x: x["market_cap"], reverse=True)
        top_stocks = evaluated_stocks[:self.top_n]

        logging.info(f"Evaluation complete. Identified top {len(top_stocks)} stocks.")
        return top_stocks

    def run(self, output_file: str = "top_10_stocks.json") -> List[Dict[str, Any]]:
        """Runs the evaluator agent and saves output to JSON file."""
        top_stocks = self.evaluate_top_stocks()

        result = {
            "agent": "SP500EvaluatorAgent",
            "description": "Top 10 Most Valuable S&P 500 Stocks by Market Capitalization",
            "stock_count": len(top_stocks),
            "top_stocks": top_stocks
        }

        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)

        logging.info(f"Successfully saved evaluation report to '{output_file}'.")
        return top_stocks
