#!/usr/bin/env python3
"""
Pipeline Orchestrator for Multi-Agent Stock Analysis
Executes Agent 1 (sp500_evaluator) and Agent 2 (volatility_calculator) sequentially.
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()


def run_agent(agent_dir: str, script_name: str = "main.py"):
    dir_path = ROOT_DIR / agent_dir
    venv_python = dir_path / ".venv" / "bin" / "python"

    if not venv_python.exists():
        raise RuntimeError(f"Virtual environment not found at {venv_python}. Please set up venv.")

    print(f"\n🚀 Running {agent_dir} using its virtual environment...")
    result = subprocess.run([str(venv_python), script_name], cwd=str(dir_path))
    
    if result.returncode != 0:
        print(f"❌ Error running {agent_dir}")
        sys.exit(result.returncode)
    
    print(f"✅ {agent_dir} completed successfully.\n")


def main():
    print("=" * 80)
    print("Multi-Agent S&P 500 Evaluation & Volatility Analysis Pipeline")
    print("=" * 80)

    # Step 1: Run Agent 1
    run_agent("sp500_evaluator")

    # Step 2: Run Agent 2
    run_agent("volatility_calculator")

    print("=" * 80)
    print("Pipeline Execution Complete!")
    print("Agent 1 Output: sp500_evaluator/top_10_stocks.json")
    print("Agent 2 Output: volatility_calculator/volatility_report.json")
    print("=" * 80)


if __name__ == "__main__":
    main()
