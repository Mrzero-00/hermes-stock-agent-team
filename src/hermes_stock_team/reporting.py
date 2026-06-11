from __future__ import annotations

import json
from dataclasses import asdict

from .models import PortfolioBrief


def to_json(brief: PortfolioBrief) -> str:
    return json.dumps(asdict(brief), indent=2, ensure_ascii=False)


def to_markdown(brief: PortfolioBrief) -> str:
    lines = [
        f"# Hermes Stock Agent Brief ({brief.as_of})",
        "",
        f"- 시장 국면: `{brief.risk_regime}`",
        f"- 주의: {brief.disclaimer}",
        "",
        "## 모멘텀 상위 산업",
    ]

    for item in brief.top_industries:
        lines.append(f"- {item.industry}: {item.score:.1f}/100 ({'; '.join(item.notes)})")

    if brief.stale_data_warnings:
        lines.extend(["", "## 데이터 신선도 경고"])
        for warning in brief.stale_data_warnings:
            lines.append(f"- {warning}")

    lines.extend(["", "## 종목 후보"])
    for candidate in brief.candidates:
        lines.extend(
            [
                f"### {candidate.ticker} ({candidate.industry})",
                f"- 액션: `{candidate.action}`",
                f"- 확신도: {candidate.conviction}/100",
                f"- 현재가 / 진입가 / 손절가 / 목표 매도가: {candidate.price:.2f} / {candidate.entry_price:.2f} / {candidate.stop_loss:.2f} / {candidate.target_sell_price:.2f}",
                f"- 투자 아이디어: {' '.join(candidate.thesis)}",
                f"- 리스크: {' '.join(candidate.risks)}",
            ]
        )

    lines.extend(["", "## 근거 출처"])
    for item in brief.evidence[:8]:
        lines.append(f"- {item['ticker']}: {item['title']} ({item['published_at']}, {item['source_url']})")

    lines.extend(["", "## 페이퍼 주문 후보"])
    if not brief.paper_orders:
        lines.append("- 없음.")
    for order in brief.paper_orders:
        lines.append(
            f"- {order['ticker']} 매수 지정가 {order['limit_price']:.2f}, 손절 {order['stop_loss']:.2f}, 목표 매도가 {order['target_sell_price']:.2f}"
        )

    return "\n".join(lines) + "\n"
