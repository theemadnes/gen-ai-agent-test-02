import json
from pathlib import Path
from agent import VolatilityCalculatorAgent


def main():
    agent = VolatilityCalculatorAgent(period_days=14)
    input_file = Path("../sp500_evaluator/top_10_stocks.json")
    if not input_file.exists() and Path("top_10_stocks.json").exists():
        input_file = Path("top_10_stocks.json")

    output_path = Path("volatility_report.json")

    print("=" * 70)
    print("Agent 2: Volatility Calculator Agent")
    print("=" * 70)

    try:
        results = agent.run(input_file=str(input_file), output_file=str(output_path))
    except Exception as e:
        print(f"Error executing Volatility Agent: {e}")
        return

    print(f"\n2-Week Volatility Indexes & Risk Analysis (Past 14 Days):")
    print("-" * 80)
    print(f"{'Ticker':<8} {'Company Name':<25} {'2W Return':<12} {'Daily Vol':<12} {'Ann Vol Index':<15}")
    print("-" * 80)

    for item in results:
        ret_str = f"{item['total_2week_return_pct']:+.2f}%"
        d_vol_str = f"{item['daily_volatility_pct']:.2f}%"
        a_vol_str = f"{item['annualized_volatility_index_pct']:.2f}%"
        print(f"{item['symbol']:<8} {item['name'][:24]:<25} {ret_str:<12} {d_vol_str:<12} {a_vol_str:<15}")

    print("-" * 80)
    print(f"Full volatility report saved to: {output_path.resolve()}\n")


if __name__ == "__main__":
    main()
