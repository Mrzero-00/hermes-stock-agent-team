from __future__ import annotations

import argparse
from pathlib import Path

from .orchestrator import StockAgentOrchestrator
from .reporting import to_json, to_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Hermes stock agent team MVP.")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Path to the hermes-stock-agent-team project root.",
    )
    parser.add_argument("--top-n", type=int, default=5, help="Number of stock candidates to include.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    brief = StockAgentOrchestrator(args.project_root).run(top_n=args.top_n)
    if args.format == "json":
        print(to_json(brief))
    else:
        print(to_markdown(brief))


if __name__ == "__main__":
    main()
