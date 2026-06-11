from __future__ import annotations

from pathlib import Path

from .agents import IndustryAgent, MarketAgent, ResearchAgent, RiskAgent, StockAnalysisAgent
from .data_sources import JsonMarketDataSource, load_json, load_universe
from .models import PortfolioBrief


class StockAgentOrchestrator:
    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        self.universe = load_universe(project_root / "config" / "universe.json")
        self.risk_policy = load_json(project_root / "config" / "risk_policy.json")
        self.data_source = JsonMarketDataSource(project_root / "data" / "sample_market_snapshot.json")
        self.research_agent = ResearchAgent()
        self.market_agent = MarketAgent()
        self.industry_agent = IndustryAgent()
        self.stock_agent = StockAnalysisAgent()
        self.risk_agent = RiskAgent()

    def run(self, top_n: int = 5) -> PortfolioBrief:
        snapshot = self.data_source.load_snapshot()
        research = self.research_agent.summarize(snapshot)
        market = self.market_agent.analyze(snapshot)
        industries = self.industry_agent.rank(self.universe, research, market)
        candidates = self.stock_agent.rank(
            self.universe,
            snapshot,
            research,
            industries,
            self.risk_policy,
        )[:top_n]
        paper_orders = self.risk_agent.build_paper_orders(candidates, self.risk_policy)

        return PortfolioBrief(
            as_of=snapshot["as_of"],
            risk_regime=market.risk_regime,
            top_industries=industries[:3],
            candidates=candidates,
            evidence=research["evidence"],
            stale_data_warnings=research["stale_data_warnings"],
            paper_orders=paper_orders,
        )
