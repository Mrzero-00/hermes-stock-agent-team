# Hermes Stock Agent Team Architecture

This project is a runnable MVP for a Codex/Hermes-style stock agent team. The first version produces a research brief from sample data. It does not place live trades.

## Components

- `ResearchAgent`: turns news and catalysts into ticker/industry evidence scores.
- `MarketAgent`: classifies the macro and market-risk regime.
- `IndustryAgent`: ranks industries by catalyst density and market fit.
- `StockAnalysisAgent`: ranks tickers and estimates entry, stop, and target sell prices.
- `RiskAgent`: converts only high-conviction ideas into paper orders.
- `StockAgentOrchestrator`: owns the end-to-end loop.

## Data Flow

```text
market snapshot + universe + risk policy
  -> research scores
  -> market regime
  -> industry ranking
  -> stock ranking
  -> paper orders
  -> markdown/json report
```

## Extension Points

- Replace `JsonMarketDataSource` with API-backed providers.
- Add source citations to `ResearchAgent` outputs.
- Add valuation models per sector.
- Add a broker adapter behind `Broker`.
- Add an approval service before live orders.

## Automation Roadmap

1. Scheduled research brief generation.
2. External data connectors for news, rates, filings, and prices.
3. Backtesting and paper trading.
4. Portfolio/risk dashboard.
5. Broker integration in paper mode.
6. Live mode only after manual approval, audit logs, and max-loss kill switches.
