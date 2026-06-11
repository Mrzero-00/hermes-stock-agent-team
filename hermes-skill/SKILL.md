---
name: hermes-stock-agent-team
description: Run and extend the local Hermes stock agent team for advisory-only market, industry, and stock research briefs. Use when asked for stock research automation, daily market briefs, sector momentum, watchlists, target sell prices, or future paper-trading integration.
---

# Hermes Stock Agent Team

Use this skill to operate the local stock research agent project at:

`/Users/sonsang-il/Desktop/claude/projects/hermes-stock-agent-team`

This project is advisory-only. It must not place live trades.

## Core Workflow

1. Change into the project directory.
2. Run tests before claiming the pipeline works:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

3. Generate a Korean-friendly research brief:

```bash
PYTHONPATH=src python3 -m hermes_stock_team.cli --format markdown --top-n 5
```

4. For structured automation output, use JSON:

```bash
PYTHONPATH=src python3 -m hermes_stock_team.cli --format json --top-n 5
```

## Agent Roles

- `ResearchAgent`: news, catalysts, source URLs, timestamps, stale-data warnings.
- `MarketAgent`: rates, volatility, trend, breadth, market regime.
- `IndustryAgent`: sector/industry momentum ranking.
- `StockAnalysisAgent`: ticker conviction, entry, stop-loss, target sell price.
- `RiskAgent`: paper-order candidates only.
- `StockAgentOrchestrator`: executes the full loop.

## Safety Rules

- Treat every output as research, not financial advice.
- Do not enable live trading by default.
- Do not bypass `LiveBrokerDisabled`.
- Keep `config/risk_policy.json` set to `paper_trading_only: true` unless the user explicitly requests a reviewed broker integration.
- Require human approval for any future broker order.
- Warn if data is stale or sources are missing.

## Extension Roadmap

Add capabilities in this order:

1. Real news/RSS provider.
2. Rates and macro data provider.
3. Price/fundamental data provider.
4. Scheduled daily brief.
5. Backtesting.
6. Paper broker.
7. Live broker only after audit logs, max-loss limits, and manual approval.
