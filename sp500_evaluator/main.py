import json
import sys
from pathlib import Path
from agent import SP500EvaluatorAgent


def main():
    agent = SP500EvaluatorAgent(top_n=10)
    output_path = Path("top_10_stocks.json")
    
    print("=" * 60)
    print("Agent 1: S&P 500 Evaluator Agent")
    print("=" * 60)
    
    stocks = agent.run(output_file=str(output_path))
    
    print(f"\nCollected Top {len(stocks)} Most Valuable Stocks in S&P 500:")
    print("-" * 65)
    print(f"{'Rank':<5} {'Ticker':<8} {'Company Name':<28} {'Market Cap':<12}")
    print("-" * 65)
    
    for idx, s in enumerate(stocks, 1):
        print(f"{idx:<5} {s['symbol']:<8} {s['name'][:27]:<28} {s['market_cap_formatted']:<12}")
        
    print("-" * 65)
    print(f"Output saved to: {output_path.resolve()}\n")


if __name__ == "__main__":
    main()
