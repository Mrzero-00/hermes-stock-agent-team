from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


RiskRegime = Literal["risk_on", "neutral", "risk_off"]
Action = Literal["buy_watch", "watch", "avoid"]


@dataclass(frozen=True)
class Industry:
    name: str
    momentum_keywords: list[str]
    tickers: list[str]


@dataclass(frozen=True)
class Universe:
    base_currency: str
    markets: list[str]
    industries: list[Industry]


@dataclass(frozen=True)
class MarketRegime:
    risk_regime: RiskRegime
    macro_score: float
    notes: list[str]


@dataclass(frozen=True)
class IndustrySignal:
    industry: str
    score: float
    catalyst_count: int
    notes: list[str]


@dataclass(frozen=True)
class StockCandidate:
    ticker: str
    industry: str
    action: Action
    conviction: int
    price: float
    entry_price: float
    stop_loss: float
    target_sell_price: float
    thesis: list[str]
    risks: list[str]


@dataclass(frozen=True)
class PortfolioBrief:
    as_of: str
    risk_regime: RiskRegime
    top_industries: list[IndustrySignal]
    candidates: list[StockCandidate]
    evidence: list[dict[str, str]] = field(default_factory=list)
    stale_data_warnings: list[str] = field(default_factory=list)
    paper_orders: list[dict[str, Any]] = field(default_factory=list)
    disclaimer: str = (
        "Educational research scaffold only. This is not financial advice and live trading is disabled."
    )
