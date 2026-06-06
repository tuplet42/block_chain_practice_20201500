from __future__ import annotations

from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("upbit-beginner-mcp")

UPBIT_BASE = "https://api.upbit.com/v1"


async def _get_json(path: str, params: dict[str, Any] | None = None) -> Any:
    """Upbit API GET 요청 공통 함수"""
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(
            f"{UPBIT_BASE}{path}",
            params=params or {},
            headers={"accept": "application/json"},
        )
        response.raise_for_status()
        return response.json()


async def _get_market_map() -> dict[str, dict[str, Any]]:
    """마켓 코드를 key로 하는 마켓 정보 dict 생성"""
    markets = await _get_json("/market/all", {"is_details": "true"})
    return {item["market"]: item for item in markets}


def _normalize_market(market: str) -> str:
    """
    krw-btc처럼 입력해도 KRW-BTC로 변환합니다.
    BTC처럼 코인 심볼만 입력한 경우 초보자를 위해 KRW-BTC로 자동 보정합니다.
    """
    market = market.strip().upper()

    if "-" not in market:
        return f"KRW-{market}"

    return market


def _format_warning(market_info: dict[str, Any] | None) -> str:
    """초보자용 유의/주의 정보 문자열 생성"""
    if not market_info:
        return "마켓 상세 정보를 찾지 못했습니다."

    warning = market_info.get("market_warning", "NONE")
    event = market_info.get("market_event")

    warning_text = "해당 없음" if warning == "NONE" else str(warning)

    if isinstance(event, dict):
        caution = event.get("caution", {})
        caution_items = []

        if isinstance(caution, dict):
            for key, value in caution.items():
                if value:
                    caution_items.append(key)

        if caution_items:
            return (
                f"유의/주의 정보: {warning_text}, 주의 항목: {', '.join(caution_items)}"
            )

    return f"유의/주의 정보: {warning_text}"


def _market_code_explanation(market: str, korean_name: str, english_name: str) -> str:
    """KRW-BTC 같은 마켓 코드의 의미를 초보자용으로 설명합니다."""
    if "-" not in market:
        return f"{market} 마켓 코드 형식을 확인하기 어렵습니다."

    quote, symbol = market.split("-", 1)

    quote_desc = {
        "KRW": "원화",
        "BTC": "비트코인",
        "USDT": "테더",
    }.get(quote, quote)

    return (
        f"{market}는 {quote_desc}({quote})로 "
        f"{korean_name}({symbol}, {english_name})을 거래하는 마켓입니다."
    )


def _change_explanation(change_rate: float) -> str:
    """전일 대비 변동률을 문장으로 설명합니다."""
    if change_rate > 0:
        return f"전일 종가보다 {change_rate:.2f}% 상승한 상태입니다."
    if change_rate < 0:
        return f"전일 종가보다 {abs(change_rate):.2f}% 하락한 상태입니다."
    return "전일 종가와 거의 같은 수준입니다."


def _liquidity_explanation(acc_trade_price_24h: float) -> str:
    """24시간 거래대금을 기준으로 거래 활발도를 설명합니다."""
    if acc_trade_price_24h >= 100_000_000_000:
        return "24시간 거래대금이 1,000억 원 이상으로 매우 활발한 마켓입니다."
    if acc_trade_price_24h >= 10_000_000_000:
        return "24시간 거래대금이 100억 원 이상으로 비교적 활발한 마켓입니다."
    if acc_trade_price_24h >= 1_000_000_000:
        return "24시간 거래대금이 10억 원 이상으로 보통 수준의 거래가 있는 마켓입니다."
    return "24시간 거래대금이 10억 원 미만으로 거래가 많지 않은 편입니다."


def _spread_explanation(spread_rate: float) -> str:
    """호가 스프레드율을 초보자용으로 설명합니다."""
    if spread_rate < 0.1:
        return "매수/매도 호가 차이가 작은 편입니다."
    if spread_rate < 0.5:
        return "매수/매도 호가 차이가 보통 수준입니다."
    return "매수/매도 호가 차이가 큰 편이므로 시장가 거래 시 체결 가격 차이에 유의해야 합니다."


def _price_position_explanation(
    trade_price: float,
    low_price: float,
    high_price: float,
) -> str:
    """현재가가 24시간 고가/저가 범위에서 어디쯤인지 설명합니다."""
    if high_price <= low_price:
        return "24시간 고가와 저가 차이가 작아 현재 위치를 판단하기 어렵습니다."

    position = (trade_price - low_price) / (high_price - low_price)

    if position < 0.3:
        return "현재가는 24시간 저가에 가까운 편입니다."
    if position < 0.7:
        return "현재가는 24시간 고가와 저가 사이의 중간 구간에 있습니다."
    return "현재가는 24시간 고가에 가까운 편입니다."


@mcp.tool()
async def search_upbit_market(
    keyword: str = "비트코인",
    quote: str = "KRW",
    limit: int = 10,
) -> str:
    """
    코인 한글명, 영문명, 마켓 코드로 Upbit 마켓을 검색합니다.
    초보자가 KRW-BTC 같은 마켓 코드를 찾을 때 사용합니다.
    정확히 일치하는 결과를 먼저 보여주고, 그다음 관련 결과를 보여줍니다.
    """
    raw_keyword = keyword.strip()
    keyword_lower = raw_keyword.lower()
    quote = quote.strip().upper()
    limit = max(1, min(int(limit), 30))

    markets = await _get_json("/market/all", {"is_details": "true"})

    exact_results = []
    related_results = []

    for item in markets:
        market = item.get("market", "")
        korean_name = item.get("korean_name", "")
        english_name = item.get("english_name", "")
        symbol = market.split("-", 1)[1] if "-" in market else market

        if quote and not market.startswith(f"{quote}-"):
            continue

        is_exact = (
            raw_keyword == korean_name
            or keyword_lower == english_name.lower()
            or keyword_lower == symbol.lower()
            or keyword_lower == market.lower()
        )

        if is_exact:
            exact_results.append(item)
            continue

        target = f"{market} {korean_name} {english_name} {symbol}".lower()
        if keyword_lower in target:
            related_results.append(item)

    if not exact_results and not related_results:
        return (
            f"'{raw_keyword}'에 해당하는 {quote} 마켓을 찾지 못했습니다.\n"
            f"예시 입력: 비트코인, bitcoin, BTC, 이더리움, ETH"
        )

    lines = [f"'{raw_keyword}' 검색 결과 ({quote} 마켓 기준, 최대 {limit}개)"]

    count = 0

    if exact_results:
        lines.append("")
        lines.append("[정확히 일치]")
        for item in exact_results[:limit]:
            lines.append(
                f"- {item['market']}: {item['korean_name']} / {item['english_name']} "
                f"({_format_warning(item)})"
            )
            count += 1

    remaining = max(0, limit - count)

    if related_results and remaining > 0:
        lines.append("")
        lines.append("[관련 결과]")
        for item in related_results[:remaining]:
            lines.append(
                f"- {item['market']}: {item['korean_name']} / {item['english_name']} "
                f"({_format_warning(item)})"
            )

    return "\n".join(lines)


@mcp.tool()
async def get_upbit_orderbook(market: str = "KRW-BTC", depth: int = 5) -> str:
    """
    Upbit 마켓의 주문장/호가창 상위 n단계를 조회합니다.
    """
    market = _normalize_market(market)
    depth = max(1, min(int(depth), 15))

    data = await _get_json("/orderbook", {"markets": market})
    if not data:
        return f"호가 정보를 찾지 못했습니다: {market}"

    orderbook = data[0]
    units = orderbook.get("orderbook_units", [])[:depth]

    if not units:
        return f"{market} 호가창 데이터가 비어 있습니다."

    lines = [f"{market} 호가창 상위 {depth}단계"]
    lines.append("매도호가 | 매도잔량 | 매수호가 | 매수잔량")

    for unit in units:
        lines.append(
            f"{unit['ask_price']:,.0f} | {unit['ask_size']:.8f} | "
            f"{unit['bid_price']:,.0f} | {unit['bid_size']:.8f}"
        )

    return "\n".join(lines)


@mcp.tool()
async def get_beginner_coin_summary(market: str = "KRW-BTC") -> str:
    """
    초보자를 위한 Upbit 코인 요약 정보를 반환합니다.
    현재가, 변동률, 거래대금, 호가 스프레드, 유의/주의 정보,
    마켓 코드 설명과 간단한 해석을 한 번에 보여줍니다.
    """
    market = _normalize_market(market)

    market_map = await _get_market_map()
    market_info = market_map.get(market)

    ticker_data = await _get_json("/ticker", {"markets": market})
    if not ticker_data:
        return f"현재가 정보를 찾지 못했습니다: {market}"

    orderbook_data = await _get_json("/orderbook", {"markets": market})
    if not orderbook_data:
        return f"호가 정보를 찾지 못했습니다: {market}"

    ticker = ticker_data[0]
    orderbook = orderbook_data[0]
    first_unit = orderbook["orderbook_units"][0]

    trade_price = ticker.get("trade_price", 0)
    prev_closing_price = ticker.get("prev_closing_price", 0)
    signed_change_rate = ticker.get("signed_change_rate", 0) * 100
    signed_change_price = ticker.get("signed_change_price", 0)
    acc_trade_price_24h = ticker.get("acc_trade_price_24h", 0)
    acc_trade_volume_24h = ticker.get("acc_trade_volume_24h", 0)
    high_price = ticker.get("high_price", 0)
    low_price = ticker.get("low_price", 0)

    ask_price = first_unit["ask_price"]
    bid_price = first_unit["bid_price"]
    spread = ask_price - bid_price
    spread_rate = (spread / trade_price * 100) if trade_price else 0

    korean_name = market_info.get("korean_name") if market_info else "알 수 없음"
    english_name = market_info.get("english_name") if market_info else "Unknown"

    change_sign = "+" if signed_change_rate > 0 else ""

    market_code_text = _market_code_explanation(market, korean_name, english_name)
    change_text = _change_explanation(signed_change_rate)
    liquidity_text = _liquidity_explanation(acc_trade_price_24h)
    spread_text = _spread_explanation(spread_rate)
    position_text = _price_position_explanation(
        trade_price,
        low_price,
        high_price,
    )

    return (
        f"{market} 초보자용 요약\n\n"
        f"1. 기본 정보\n"
        f"- 코인명: {korean_name} / {english_name}\n"
        f"- 마켓 코드: {market}\n"
        f"- 현재가: {trade_price:,.0f} KRW\n"
        f"- 전일 종가: {prev_closing_price:,.0f} KRW\n\n"
        f"2. 24시간 시세 정보\n"
        f"- 전일 대비 변동률: {change_sign}{signed_change_rate:.2f}%\n"
        f"- 전일 대비 가격 변화: {signed_change_price:,.0f} KRW\n"
        f"- 24시간 고가: {high_price:,.0f} KRW\n"
        f"- 24시간 저가: {low_price:,.0f} KRW\n"
        f"- 24시간 거래대금: {acc_trade_price_24h:,.0f} KRW\n"
        f"- 24시간 거래량: {acc_trade_volume_24h:,.8f}\n\n"
        f"3. 호가 요약\n"
        f"- 최우선 매도호가: {ask_price:,.0f} KRW\n"
        f"- 최우선 매수호가: {bid_price:,.0f} KRW\n"
        f"- 호가 스프레드: {spread:,.0f} KRW\n"
        f"- 호가 스프레드율: {spread_rate:.4f}%\n\n"
        f"4. 시장 경보 정보\n"
        f"- {_format_warning(market_info)}\n\n"
        f"5. 초보자 해석\n"
        f"- 마켓 코드 설명: {market_code_text}\n"
        f"- 가격 흐름: {change_text}\n"
        f"- 거래 활발도: {liquidity_text}\n"
        f"- 호가 해석: 바로 매수하려면 최우선 매도호가를, "
        f"바로 매도하려면 최우선 매수호가를 참고할 수 있습니다.\n"
        f"- 스프레드 해석: {spread_text}\n"
        f"- 24시간 가격 위치: {position_text}\n\n"
        f"※ 본 정보는 투자 조언이 아니라 Upbit 시세 조회용 정보입니다."
    )


@mcp.tool()
async def compare_upbit_markets(markets: str = "KRW-BTC,KRW-ETH,KRW-XRP") -> str:
    """
    여러 Upbit 마켓의 현재가, 변동률, 24시간 거래대금을 비교합니다.
    예: KRW-BTC,KRW-ETH,KRW-XRP
    """
    market_list = [_normalize_market(m) for m in markets.split(",") if m.strip()]
    market_list = market_list[:10]

    if not market_list:
        return "비교할 마켓을 입력해주세요. 예: KRW-BTC,KRW-ETH"

    data = await _get_json("/ticker", {"markets": ",".join(market_list)})
    if not data:
        return "현재가 정보를 조회하지 못했습니다."

    market_map = await _get_market_map()

    lines = ["Upbit 마켓 비교"]
    lines.append("마켓 | 코인명 | 현재가 | 24h 변동률 | 24h 거래대금")

    for item in data:
        market = item["market"]
        info = market_map.get(market, {})
        korean_name = info.get("korean_name", "알 수 없음")

        price = item.get("trade_price", 0)
        change_rate = item.get("signed_change_rate", 0) * 100
        volume_price = item.get("acc_trade_price_24h", 0)

        sign = "+" if change_rate > 0 else ""

        lines.append(
            f"{market} | {korean_name} | {price:,.0f} KRW | "
            f"{sign}{change_rate:.2f}% | {volume_price:,.0f} KRW"
        )

    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
