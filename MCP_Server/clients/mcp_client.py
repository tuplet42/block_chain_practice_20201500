from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]

SERVERS = {
    "upbit": ROOT / "servers" / "server.py",
}

DEFAULT_CALLS = {
    "upbit": [
        ("search_upbit_market", {"keyword": "비트코인", "quote": "KRW", "limit": 5}),
        ("get_beginner_coin_summary", {"market": "KRW-BTC"}),
        ("get_upbit_orderbook", {"market": "KRW-BTC", "depth": 5}),
        ("compare_upbit_markets", {"markets": "KRW-BTC,KRW-ETH,KRW-XRP"}),
    ],
}


def extract_text(result: Any) -> str:
    parts: list[str] = []
    for item in result.content:
        text = getattr(item, "text", None)
        parts.append(text if text is not None else str(item))
    return "\n".join(parts).strip()


def line(title: str = "") -> str:
    width = 72
    if not title:
        return "─" * width

    label = f" {title} "
    return label + "─" * max(0, width - len(label))


def print_tool_card(index: int, name: str, description: str | None) -> None:
    print(f"  {index}. {name}")
    if description:
        print(f"     └─ {description}")


def print_result(text: str, *, error: bool = False) -> None:
    prefix = "❌" if error else "✅"
    print(f"{prefix} MCP Server 응답")
    print(line())
    print(text or "응답 본문이 비어 있습니다.")
    print(line())


async def run_demo(server_name: str) -> None:
    server_path = SERVERS[server_name]

    params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
        cwd=ROOT,
        env=None,
    )

    print(line(f"{server_name.upper()} MCP DEMO"))
    print(f"📁 Project: {ROOT}")
    print(f"🖥️  Server : {server_path.relative_to(ROOT)}")
    print("🔌 Transport: stdio")

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            print("\n[1/3] MCP 세션 초기화")
            await session.initialize()
            print("✅ client ↔ server 연결 완료")

            print("\n[2/3] Tool discovery")
            tools = await session.list_tools()
            for i, tool in enumerate(tools.tools, 1):
                print_tool_card(i, tool.name, tool.description)

            print("\n[3/3] Tool call 실행")
            for tool_name, arguments in DEFAULT_CALLS[server_name]:
                print(f"\n▶ 호출: {tool_name}({arguments})")

                result = await session.call_tool(tool_name, arguments)

                is_error = bool(
                    getattr(result, "isError", False)
                    or getattr(result, "is_error", False)
                )

                print_result(extract_text(result), error=is_error)

    print(
        "\n🎯 데모 완료: client가 server의 tool을 발견하고 호출하는 MCP 흐름을 확인했습니다."
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Upbit 초보자용 MCP stdio client demo",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "server",
        choices=sorted(SERVERS),
        help="실행할 MCP server",
    )

    args = parser.parse_args()
    asyncio.run(run_demo(args.server))


if __name__ == "__main__":
    main()
