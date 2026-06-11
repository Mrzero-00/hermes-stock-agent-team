from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol

from .models import Industry, Universe


class MarketDataSource(Protocol):
    def load_snapshot(self) -> dict[str, Any]:
        """Return a normalized market snapshot."""


class JsonMarketDataSource:
    def __init__(self, snapshot_path: Path) -> None:
        self.snapshot_path = snapshot_path

    def load_snapshot(self) -> dict[str, Any]:
        return json.loads(self.snapshot_path.read_text(encoding="utf-8"))


def load_universe(path: Path) -> Universe:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return Universe(
        base_currency=raw["base_currency"],
        markets=raw["markets"],
        industries=[
            Industry(
                name=item["name"],
                momentum_keywords=item["momentum_keywords"],
                tickers=item["tickers"],
            )
            for item in raw["industries"]
        ],
    )


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
