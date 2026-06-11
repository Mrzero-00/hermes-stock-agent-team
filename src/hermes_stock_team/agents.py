from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

from .models import IndustrySignal, MarketRegime, StockCandidate, Universe


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


class ResearchAgent:
    def summarize(self, snapshot: dict[str, Any]) -> dict[str, Any]:
        industry_scores: dict[str, list[float]] = defaultdict(list)
        ticker_scores: dict[str, list[float]] = defaultdict(list)
        evidence: list[dict[str, str]] = []
        stale_data_warnings: list[str] = []
        as_of = datetime.fromisoformat(snapshot["as_of"]).replace(tzinfo=timezone.utc)

        for item in snapshot.get("news", []):
            score = (item["sentiment"] * 0.45) + (item["catalyst_strength"] * 0.55)
            industry_scores[item["industry"]].append(score)
            ticker_scores[item["ticker"]].append(score)
            evidence.append(
                {
                    "ticker": item["ticker"],
                    "industry": item["industry"],
                    "title": item["title"],
                    "source_url": item.get("source_url", ""),
                    "published_at": item.get("published_at", ""),
                }
            )
            published_at = item.get("published_at")
            if published_at:
                published_date = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
                if (as_of - published_date).days >= 3:
                    stale_data_warnings.append(f"{item['ticker']} news item is stale: {published_at}")

        return {
            "industry_news_score": {
                industry: sum(scores) / len(scores)
                for industry, scores in industry_scores.items()
            },
            "ticker_news_score": {
                ticker: sum(scores) / len(scores)
                for ticker, scores in ticker_scores.items()
            },
            "evidence": evidence,
            "stale_data_warnings": stale_data_warnings,
        }


class MarketAgent:
    def analyze(self, snapshot: dict[str, Any]) -> MarketRegime:
        market = snapshot["market"]
        rates = snapshot["rates"]
        trend_score = (market["sp500_trend_score"] + market["nasdaq_trend_score"]) / 2
        volatility_penalty = _clamp((market["vix_level"] - 12) / 25)
        curve_pressure = 0.08 if rates["us_2y_yield"] > rates["us_10y_yield"] else 0.0
        macro_score = _clamp((trend_score * 0.55) + (market["breadth_score"] * 0.35) - volatility_penalty - curve_pressure)

        if macro_score >= 0.62:
            regime = "risk_on"
        elif macro_score <= 0.40:
            regime = "risk_off"
        else:
            regime = "neutral"

        notes = [
            f"Index trend score is {trend_score:.2f}.",
            f"VIX is {market['vix_level']:.1f}.",
            f"2Y/10Y yields are {rates['us_2y_yield']:.2f}%/{rates['us_10y_yield']:.2f}%.",
        ]
        return MarketRegime(risk_regime=regime, macro_score=macro_score, notes=notes)


class IndustryAgent:
    def rank(self, universe: Universe, research: dict[str, Any], regime: MarketRegime) -> list[IndustrySignal]:
        ranked: list[IndustrySignal] = []
        industry_news = research["industry_news_score"]
        macro_multiplier = {"risk_on": 1.08, "neutral": 1.0, "risk_off": 0.86}[regime.risk_regime]

        for industry in universe.industries:
            news_score = industry_news.get(industry.name, 0.45)
            catalyst_density = min(1.0, len(industry.momentum_keywords) / 4)
            score = _clamp(((news_score * 0.62) + (catalyst_density * 0.38)) * macro_multiplier)
            ranked.append(
                IndustrySignal(
                    industry=industry.name,
                    score=round(score * 100, 1),
                    catalyst_count=len(industry.momentum_keywords),
                    notes=[f"Momentum themes: {', '.join(industry.momentum_keywords)}"],
                )
            )

        return sorted(ranked, key=lambda item: item.score, reverse=True)


class StockAnalysisAgent:
    def rank(
        self,
        universe: Universe,
        snapshot: dict[str, Any],
        research: dict[str, Any],
        industries: list[IndustrySignal],
        risk_policy: dict[str, Any],
    ) -> list[StockCandidate]:
        industry_lookup = {industry.name: industry for industry in universe.industries}
        industry_scores = {item.industry: item.score / 100 for item in industries}
        ticker_news = research["ticker_news_score"]
        fundamentals = snapshot["fundamentals"]
        candidates: list[StockCandidate] = []

        for industry_signal in industries:
            industry = industry_lookup[industry_signal.industry]
            for ticker in industry.tickers:
                if ticker not in fundamentals:
                    continue

                metrics = fundamentals[ticker]
                if metrics["liquidity_score"] < risk_policy["min_liquidity_score"]:
                    continue

                score = (
                    industry_scores[industry.name] * 0.24
                    + ticker_news.get(ticker, 0.50) * 0.22
                    + metrics["growth_score"] * 0.22
                    + metrics["quality_score"] * 0.18
                    + metrics["valuation_score"] * 0.14
                )
                conviction = round(_clamp(score) * 100)
                price = float(metrics["price"])
                action = "buy_watch" if conviction >= risk_policy["min_conviction_for_buy"] else "watch"
                target_multiplier = 1 + risk_policy["take_profit_pct"] * (0.75 + conviction / 400)
                stop_multiplier = 1 - risk_policy["stop_loss_pct"]

                candidates.append(
                    StockCandidate(
                        ticker=ticker,
                        industry=industry.name,
                        action=action,
                        conviction=conviction,
                        price=price,
                        entry_price=round(price * 0.99, 2),
                        stop_loss=round(price * stop_multiplier, 2),
                        target_sell_price=round(price * target_multiplier, 2),
                        thesis=[
                            f"Industry momentum score {industry_signal.score:.1f}.",
                            f"Growth/quality scores {metrics['growth_score']:.2f}/{metrics['quality_score']:.2f}.",
                        ],
                        risks=[
                            "Valuation compression if rates rise.",
                            "Catalyst may already be priced in.",
                        ],
                    )
                )

        return sorted(candidates, key=lambda item: item.conviction, reverse=True)


class RiskAgent:
    def build_paper_orders(self, candidates: list[StockCandidate], risk_policy: dict[str, Any]) -> list[dict[str, Any]]:
        if risk_policy.get("paper_trading_only", True) is not True:
            return []

        orders: list[dict[str, Any]] = []
        for candidate in candidates:
            if candidate.action != "buy_watch":
                continue
            orders.append(
                {
                    "mode": "paper",
                    "ticker": candidate.ticker,
                    "side": "buy",
                    "max_position_weight": risk_policy["max_position_weight"],
                    "limit_price": candidate.entry_price,
                    "stop_loss": candidate.stop_loss,
                    "target_sell_price": candidate.target_sell_price,
                    "requires_human_approval": True,
                }
            )
        return orders
