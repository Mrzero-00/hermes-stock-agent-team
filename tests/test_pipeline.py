from __future__ import annotations

import unittest
from pathlib import Path

from hermes_stock_team.orchestrator import StockAgentOrchestrator
from hermes_stock_team.reporting import to_markdown
from hermes_stock_team.broker import LiveBrokerDisabled


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class PipelineTest(unittest.TestCase):
    def test_orchestrator_generates_ranked_candidates(self) -> None:
        brief = StockAgentOrchestrator(PROJECT_ROOT).run(top_n=4)

        self.assertEqual(brief.as_of, "2026-06-11")
        self.assertTrue(brief.top_industries)
        self.assertEqual(len(brief.candidates), 4)
        self.assertGreaterEqual(brief.candidates[0].conviction, brief.candidates[-1].conviction)
        self.assertTrue(brief.evidence)
        self.assertTrue(all(candidate.target_sell_price > candidate.price for candidate in brief.candidates))
        self.assertTrue(all(candidate.stop_loss < candidate.price for candidate in brief.candidates))


    def test_report_includes_paper_orders_not_live_orders(self) -> None:
        brief = StockAgentOrchestrator(PROJECT_ROOT).run(top_n=5)
        report = to_markdown(brief)

        self.assertIn("페이퍼 주문 후보", report)
        self.assertIn("근거 출처", report)
        self.assertIn("Educational research scaffold", report)
        self.assertTrue(all(order["mode"] == "paper" for order in brief.paper_orders))
        self.assertTrue(all(order["requires_human_approval"] is True for order in brief.paper_orders))


    def test_live_broker_is_unreachable_by_default(self) -> None:
        broker = LiveBrokerDisabled()

        with self.assertRaisesRegex(RuntimeError, "Live trading is disabled"):
            broker.submit_order({"ticker": "NVDA", "side": "buy"})


if __name__ == "__main__":
    unittest.main()
