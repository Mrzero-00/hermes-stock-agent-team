from __future__ import annotations

from typing import Any, Protocol


class Broker(Protocol):
    def submit_order(self, order: dict[str, Any]) -> dict[str, Any]:
        """Submit an order and return broker response."""


class PaperBroker:
    def submit_order(self, order: dict[str, Any]) -> dict[str, Any]:
        return {"status": "accepted_paper", "order": order}


class LiveBrokerDisabled:
    def submit_order(self, order: dict[str, Any]) -> dict[str, Any]:
        raise RuntimeError(
            "Live trading is disabled. Implement a reviewed broker adapter and turn off paper_trading_only explicitly."
        )
