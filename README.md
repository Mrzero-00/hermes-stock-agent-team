# Hermes Stock Agent Team

Codex와 Hermes 스타일의 성장형 주식 에이전트팀을 만들기 위한 실행 가능한 MVP입니다. 현재 버전은 샘플 데이터를 사용해 리서치, 시장 분석, 산업 모멘텀 분석, 종목 분석, 목표 매도가와 페이퍼 주문 후보를 생성합니다.

실거래는 의도적으로 비활성화되어 있습니다.

## Quick Start

```bash
cd /Users/sonsang-il/Desktop/claude/projects/hermes-stock-agent-team
PYTHONPATH=src python3 -m unittest discover -s tests
python3 -m hermes_stock_team.cli --format markdown
python3 -m hermes_stock_team.cli --format json
```

If you do not install the package, run with:

```bash
PYTHONPATH=src python3 -m hermes_stock_team.cli --format markdown
```

## Agent Team

- Research Agent: 뉴스, 금리, 실적, 촉매를 수집하고 점수화합니다.
- Market Agent: 금리, 변동성, 지수 추세, 시장 폭을 기반으로 시장 국면을 판단합니다.
- Industry Momentum Agent: 현재 모멘텀이 강한 산업을 정렬합니다.
- Stock Analysis Agent: 산업 내 종목을 분석하고 진입가, 손절가, 목표 매도가를 산출합니다.
- Orchestrator Agent: 전체 루프를 실행하고 리스크 정책을 적용합니다.

## Current Output

- 시장 국면
- 상위 산업
- 종목별 conviction score
- 진입가, 손절가, 목표 매도가
- 페이퍼 주문 후보

## Next Integrations

- News API, RSS, SEC filings, earnings transcripts
- FRED or central bank data for rates and macro indicators
- Price/fundamental provider
- Backtesting engine
- Broker API in paper mode
- Human approval and audit log before live trading

## Safety

This project is an educational research scaffold, not financial advice. Any live trading integration should require separate review, paper trading evidence, max-loss limits, and manual approval.
