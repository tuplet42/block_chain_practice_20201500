from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from starlette.applications import Starlette
from starlette.responses import FileResponse, JSONResponse
from starlette.routing import Route
from starlette.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parent
SERVER_PATH = ROOT / "servers" / "server.py"


def extract_text(result: Any) -> str:
    parts: list[str] = []
    for item in result.content:
        text = getattr(item, "text", None)
        parts.append(text if text is not None else str(item))
    return "\n".join(parts).strip()


async def call_mcp_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
        cwd=ROOT,
        env=None,
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            tool_names = [tool.name for tool in tools.tools]

            result = await session.call_tool(tool_name, arguments)

            is_error = bool(
                getattr(result, "isError", False) or getattr(result, "is_error", False)
            )

            return {
                "server": str(SERVER_PATH.relative_to(ROOT)),
                "tool": tool_name,
                "arguments": arguments,
                "discovered_tools": tool_names,
                "is_error": is_error,
                "result": extract_text(result),
            }


async def homepage(request):
    return FileResponse(ROOT / "web" / "index.html")


async def api_tools(request):
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
        cwd=ROOT,
        env=None,
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()

            return JSONResponse(
                {
                    "server": str(SERVER_PATH.relative_to(ROOT)),
                    "tools": [
                        {
                            "name": tool.name,
                            "description": tool.description,
                        }
                        for tool in tools.tools
                    ],
                }
            )


async def api_market_search(request):
    keyword = request.query_params.get("keyword", "비트코인")
    quote = request.query_params.get("quote", "KRW")
    limit = int(request.query_params.get("limit", "5"))

    data = await call_mcp_tool(
        "search_upbit_market",
        {
            "keyword": keyword,
            "quote": quote,
            "limit": limit,
        },
    )
    return JSONResponse(data)


async def api_summary(request):
    market = request.query_params.get("market", "KRW-BTC")

    data = await call_mcp_tool(
        "get_beginner_coin_summary",
        {
            "market": market,
        },
    )
    return JSONResponse(data)


async def api_orderbook(request):
    market = request.query_params.get("market", "KRW-BTC")
    depth = int(request.query_params.get("depth", "5"))

    data = await call_mcp_tool(
        "get_upbit_orderbook",
        {
            "market": market,
            "depth": depth,
        },
    )
    return JSONResponse(data)


async def api_compare(request):
    markets = request.query_params.get("markets", "KRW-BTC,KRW-ETH,KRW-XRP")

    data = await call_mcp_tool(
        "compare_upbit_markets",
        {
            "markets": markets,
        },
    )
    return JSONResponse(data)


routes = [
    Route("/", homepage),
    Route("/api/tools", api_tools),
    Route("/api/market/search", api_market_search),
    Route("/api/summary", api_summary),
    Route("/api/orderbook", api_orderbook),
    Route("/api/compare", api_compare),
]

app = Starlette(debug=True, routes=routes)
app.mount("/web", StaticFiles(directory=ROOT / "web"), name="web")
