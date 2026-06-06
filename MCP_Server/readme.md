# Upbit Beginner MCP

초보 사용자를 위한 Upbit 시세·호가·마켓 정보 조회 MCP 시스템입니다.

본 프로젝트는 Upbit Quotation API를 MCP Server의 tool로 제공하고, MCP Client 또는 Web Backend가 해당 tool을 호출하여 코인 현재가, 호가창, 마켓 코드, 초보자용 요약 정보를 확인할 수 있도록 구현한 기말 프로젝트입니다.

단순히 Upbit API를 직접 호출하는 프로그램이 아니라, MCP Server가 외부 API 조회 기능을 tool로 노출하고, MCP Client가 `list_tools()`로 tool을 발견한 뒤 `call_tool()`로 실행하는 구조를 보여주는 것이 핵심입니다.

---

## 1. 프로젝트 주제

**초보 사용자를 위한 Upbit 시세·호가·마켓 정보 조회 MCP 시스템**

업비트를 처음 사용하는 사용자는 `KRW-BTC`와 같은 마켓 코드, 호가창의 의미, 최우선 매수/매도 호가, 24시간 거래대금, 변동률 등을 직관적으로 이해하기 어려울 수 있다고 생각했기 때문에 이번 기회로 이러한 정보를 MCP tool을 통해 조회하고, 초보자도 이해하기 쉬운 형태로 요약하여 제공하고자 했습니다.

---

## 2. 주요 기능
본 프로젝트는 Upbit API를 단순 호출하는 데 그치지 않고, MCP Server의 tool로 기능을 제공하고 MCP Client와 Web Backend가 이를 호출하는 구조를 구현했습니다.

이를 통해 다음을 확인할 수 있습니다.

* MCP Server가 외부 API 기능을 tool로 제공할 수 있음
* MCP Client가 `list_tools()`로 tool 목록을 조회할 수 있음
* MCP Client가 `call_tool()`로 실제 tool을 호출할 수 있음
* Web UI에서도 Backend를 통해 MCP tool 호출 결과를 확인할 수 있음

그 외에도 아래와 같은 기능을 가집니다.

* Upbit 마켓 코드 검색
* 코인 현재가 및 24시간 시세 정보 조회
* 주문장/호가창 상위 단계 조회
* 여러 코인 현재가 및 변동률 비교
* 초보자용 요약 정보 제공

  * 마켓 코드 설명
  * 가격 흐름 해석
  * 거래 활발도 해석
  * 호가 스프레드 해석
  * 24시간 고가/저가 기준 현재가 위치 설명
* CLI 기반 MCP client 데모
* Web UI 기반 MCP tool 호출 데모

---

## 3. MCP 작동 구조

### 3-1. CLI 실행 흐름

```text
사용자
  ↓
MCP Client
  ↓ list_tools(), call_tool()
Upbit MCP Server
  ↓
Upbit Quotation API
  ↓
Tool Result
  ↓
MCP Client 출력
```

CLI에서는 `clients/mcp_client.py`가 MCP Client 역할을 수행합니다.
이 클라이언트는 MCP Server에 연결한 뒤 tool 목록을 조회하고, 각 tool을 호출하여 결과를 출력합니다.

### 3-2. Web UI 실행 흐름

```text
Browser UI
  ↓
Starlette Web Backend
  ↓ MCP ClientSession
Upbit MCP Server
  ↓
Upbit Quotation API
  ↓
Tool Result
  ↓
Browser UI 표시
```

Web UI에서는 브라우저가 MCP Server에 직접 연결하지 않습니다.
대신 `web_app.py`가 Starlette 기반 Web Backend로 동작하며, 내부에서 MCP ClientSession을 생성하여 MCP Server의 tool을 호출합니다.
아래의 이미지는 전체적인 Web UI입니다.
<!-- 캡처 위치 1: Web UI 전체 화면 캡처 -->
<img width="1381" height="817" alt="image" src="https://github.com/user-attachments/assets/af6b315c-8438-480e-b49a-e666493a9342" />
<img width="1245" height="717" alt="image" src="https://github.com/user-attachments/assets/27007bc0-6153-40e4-ae9f-2497ce3569f6" />
<img width="1190" height="442" alt="image" src="https://github.com/user-attachments/assets/eb7c2f17-2740-4bc2-9c07-04e2d042f115" />

---

## 4. 프로젝트 구조

```text
finalproject/
├── README.md
├── pyproject.toml
├── web_app.py
├── servers/
│   └── server.py
├── clients/
│   └── mcp_client.py
└── web/
    └── index.html
```

| 경로                      | 설명                                                          |
| ----------------------- | ----------------------------------------------------------- |
| `servers/server.py`     | Upbit API를 호출하는 MCP Server                                  |
| `clients/mcp_client.py` | MCP Server에 연결하여 tool discovery와 tool call을 수행하는 CLI Client |
| `web_app.py`            | Web UI 요청을 받아 MCP ClientSession을 실행하는 Starlette Backend     |
| `web/index.html`        | 브라우저 기반 데모 화면                                               |
| `pyproject.toml`        | 프로젝트 의존성 및 Python 버전 설정                                     |

---

## 5. 제공 MCP Tool

| Tool                                         | 설명                                                 |
| -------------------------------------------- | -------------------------------------------------- |
| `search_upbit_market(keyword, quote, limit)` | 코인 한글명, 영문명, 심볼, 마켓 코드를 기준으로 Upbit 마켓을 검색합니다.      |
| `get_beginner_coin_summary(market)`          | 현재가, 변동률, 거래대금, 호가 스프레드, 시장 경보 정보와 초보자용 해석을 제공합니다. |
| `get_upbit_orderbook(market, depth)`         | 지정한 Upbit 마켓의 주문장/호가창 상위 n단계를 조회합니다.               |
| `compare_upbit_markets(markets)`             | 여러 Upbit 마켓의 현재가, 24시간 변동률, 24시간 거래대금을 비교합니다.      |

---

## 6. 사용 API

Upbit의 정보들을 조회할 수 있어야 하기 때문에 Upbit Quotation API를 사용하였고, 사용한 주요 API는 다음과 같습니다.

| Upbit API        | 사용 목적                                  |
| ---------------- | -------------------------------------- |
| `/v1/market/all` | 전체 마켓 목록, 한글명, 영문명, 시장 경보 정보 조회        |
| `/v1/ticker`     | 현재가, 전일 대비 변동률, 24시간 거래량, 24시간 거래대금 조회 |
| `/v1/orderbook`  | 매수/매도 호가창 데이터 조회                       |

이 프로젝트에서는 공개 시세 조회 API만 사용하므로 별도의 API Key가 필요하지 않습니다.

---

## 7. 설치 방법

### 7-1. Python 버전

Python 3.11 또는 3.12 사용을 권장합니다.

`pyproject.toml` 예시:

```toml
[project]
name = "upbit-beginner-mcp"
version = "0.1.0"
description = "Beginner-friendly Upbit MCP server"
requires-python = ">=3.11,<3.13"
dependencies = [
    "mcp",
    "httpx",
    "starlette",
    "uvicorn",
]
```

### 7-2. 의존성 설치

프로젝트 루트에서 실행합니다.
아래 명령어를 통해 uv 가상환경을 pyproject.toml을 이용하여 생성할 수 있습니다.

```bash
uv sync
```

---

## 8. CLI 실행 방법

프로젝트 루트에서 다음 명령어를 실행합니다.

```bash
uv run python clients/mcp_client.py upbit
```

정상 실행 시 다음 흐름이 출력됩니다.

```text
[1/3] MCP 세션 초기화
client ↔ server 연결 완료

[2/3] Tool discovery
MCP Server가 제공하는 tool 목록 출력

[3/3] Tool call 실행
각 tool 호출 결과 출력
```
<img width="580" height="250" alt="image" src="https://github.com/user-attachments/assets/feafb6c3-264e-4ef8-ae4f-0d2ca0817699" />

<!-- 캡처 위치 2: CLI에서 Tool discovery가 보이는 부분 -->

<!-- 추천 파일명: assets/screenshots/cli-tool-discovery.png -->

<img width="776" height="514" alt="image" src="https://github.com/user-attachments/assets/3edc3d4c-a627-4518-991d-f21051807e9c" />


<!-- 캡처 위치 3: CLI에서 get_beginner_coin_summary 또는 get_upbit_orderbook 결과가 보이는 부분 -->

<!-- 추천 파일명: assets/screenshots/cli-tool-call.png -->

<img width="559" height="370" alt="image" src="https://github.com/user-attachments/assets/781f7708-48bc-4393-a2e7-56728d93f482" />


---

## 9. Web UI 실행 방법

Web UI를 실행하려면 프로젝트 루트에서 다음 명령어를 실행합니다.

```bash
uv run uvicorn web_app:app --host 127.0.0.1 --port 8765
```

브라우저에서 다음 주소로 접속합니다.

```text
http://127.0.0.1:8765
```

Web UI에서 확인할 수 있는 기능은 다음과 같습니다.

* Tool 목록 조회 
<img width="598" height="694" alt="image" src="https://github.com/user-attachments/assets/f5cc50de-6b0b-48e0-bd17-4ee26513651d" />


* Upbit 마켓 코드 검색 - 빠르게 찾을 수 있도록 비트코인, 이더리움, 리플(XRP)를 설정했으나 도지코인 등 다른 코인들도 검색할 수 있고, 그 결과를 아래의 결과창에서 확인할 수 있습니다.
<img width="1193" height="437" alt="image" src="https://github.com/user-attachments/assets/2c7eb46c-52dd-41ea-b970-1c618b9d2353" />
<img width="1196" height="434" alt="image" src="https://github.com/user-attachments/assets/b2677b3e-8144-420a-80c7-c73e9ce7164b" />
<img width="1205" height="439" alt="image" src="https://github.com/user-attachments/assets/5e8758d4-1f22-4c75-8196-e4479e7c1399" />
<img width="1194" height="437" alt="image" src="https://github.com/user-attachments/assets/ad0742f9-1e49-492d-b79c-6fd3b4cfdeb0" />


* 초보자용 코인 요약 조회 - BTC, ETH, XRP, SOL, DOGE, ADA의 6개 코인에 대해 요약조회를 할 수 있고, 그 결과를 아래의 결과창에서 확인할 수 있습니다. 이 예시는 BTC 요약 조회 결과입니다.
<img width="590" height="386" alt="image" src="https://github.com/user-attachments/assets/60ddc983-60fa-4cbb-8bd6-84cdb93aaad6" />
<img width="1174" height="817" alt="image" src="https://github.com/user-attachments/assets/1c62988f-0ef1-4699-9a4b-679a08b4f08a" />


* 호가창 조회 - 원하는 코인의 마켓 코드를 입력하고, 호가 단계를 입력하여 조회할 수 있습니다. 디폴트 호가 단계는 5이며, 그 결과를 아래의 결과창에서 확인할 수 있습니다. 이 예시는 BTC의 호가창 결과입니다.
<img width="598" height="385" alt="image" src="https://github.com/user-attachments/assets/99cf3f34-3d30-4d42-a2fb-e4a7311a1f47" />
<img width="1161" height="403" alt="image" src="https://github.com/user-attachments/assets/d29a9301-6d9a-4598-8c09-1d107b7fbd12" />


* 여러 코인 비교 - 비교하고픈 코인의 마켓 코드를 BTC, ETH, XRP, SOL, DOGE, ADA의 6개 코인에 대해 입력해서 비교할 수 있습니다. 그 결과를 아래의 결과창에서 확인할 수 있고, 이 예시는 전부 입력했을 때의 결과입니다.
<img width="1197" height="768" alt="image" src="https://github.com/user-attachments/assets/c64927b2-b754-438c-a0e0-2404e2f3320a" />

* 빠른 실행 - 아래의 사진처럼 코인을 선택해서 선택 코인에 대해 요약, 호가창을 확인할 수 있고, 주요 코인으로 설정해둔 비트코인, 이더리움, 솔라나를 비교한 주요 코인 비교를 확인할 수 있습니다. 마찬가지로 결과창에서 확인 가능합니다.
<img width="182" height="111" alt="image" src="https://github.com/user-attachments/assets/e41304db-a057-4f6f-b023-736bd94cab5f" />

---

## 10. 예시 질의와 Tool 매핑

본 프로젝트는 실제 LLM API를 연결하지 않고, MCP Client가 LLM Host 역할을 대신하여 tool을 직접 호출하는 방식으로 구현했습니다.

다만 실제 LLM과 연결할 경우 다음과 같은 자연어 질의를 MCP tool 호출로 변환할 수 있을 것입니다.

| 자연어 질의                | 호출되는 MCP Tool                                              |
| --------------------- | ---------------------------------------------------------- |
| “비트코인 마켓 코드가 뭐야?”     | `search_upbit_market(keyword="비트코인", quote="KRW")`         |
| “비트코인 초보자용 요약 보여줘”    | `get_beginner_coin_summary(market="KRW-BTC")`              |
| “비트코인 호가창 5단계 보여줘”    | `get_upbit_orderbook(market="KRW-BTC", depth=5)`           |
| “비트코인, 이더리움, 리플 비교해줘” | `compare_upbit_markets(markets="KRW-BTC,KRW-ETH,KRW-XRP")` |
| “이더리움 마켓 코드 찾아줘”      | `search_upbit_market(keyword="이더리움", quote="KRW")`         |

---

## 12. 초보자용 요약에서 제공하는 해석

`get_beginner_coin_summary` tool은 단순 시세 데이터만 보여주지 않고, 초보자를 위해 다음과 같은 해석을 추가로 제공합니다.

| 항목         | 설명                                  |
| ---------- | ----------------------------------- |
| 마켓 코드 설명   | `KRW-BTC`가 어떤 의미인지 설명합니다.           |
| 가격 흐름      | 전일 종가 대비 상승/하락 상태를 문장으로 설명합니다.      |
| 거래 활발도     | 24시간 거래대금을 기준으로 거래가 활발한 편인지 설명합니다.  |
| 호가 해석      | 최우선 매도호가와 최우선 매수호가의 의미를 설명합니다.      |
| 스프레드 해석    | 매수/매도 호가 차이가 작은지 큰지 설명합니다.          |
| 24시간 가격 위치 | 현재가가 24시간 고가/저가 범위에서 어느 위치인지 설명합니다. |

본 해석은 투자 판단을 대신하는 것이 아니라, Upbit 시세 정보를 이해하기 쉽게 정리하기 위한 참고 설명입니다.

---

## 13. 에러 처리 및 주의사항

### 13-1. 잘못된 마켓 코드

잘못된 마켓 코드를 입력하면 현재가 또는 호가 정보를 찾지 못했다는 메시지를 반환합니다.

예:

```text
현재가 정보를 찾지 못했습니다: KRW-UNKNOWN
```

### 13-2. 검색 결과가 없는 경우

검색어에 해당하는 마켓이 없으면 예시 입력을 함께 안내합니다.

```text
'abc'에 해당하는 KRW 마켓을 찾지 못했습니다.
예시 입력: 비트코인, bitcoin, BTC, 이더리움, ETH
```

### 13-3. API Key

앞서 언급했듯이 Upbit 공개 시세 조회 API만 사용하므로 API Key가 필요하지 않으므로 코드에 API Key를 하드코딩하지 않았습니다.

---

## 14. 트러블슈팅

### 14-1. Python 버전 문제

MCP 실행 시 오류를 해결하다가 Python 3.14 환경에서 문제가 발생할 수 있다는 의견이 있었으므로
Python 3.11 또는 3.12 사용을 권장합니다.
pyproject.toml파일에 이미 Python 버전을 명시해뒀지만, uv sync 명령어 실행 후 Python 버전 확인 시 3.11 또는 3.12가 아니라면 아래 절차를 따라주시길 바랍니다.

```bash
uv python install 3.11
uv venv --python 3.11
uv sync
```

현재 Python 버전 확인:

```bash
uv run python --version
```

### 14-2. Web UI 포트 충돌

`8765` 포트가 이미 사용 중이면 아래 예시처럼 다른 포트를 사용할 수 있습니다.

```bash
uv run uvicorn web_app:app --host 127.0.0.1 --port 8766
```

접속 주소:

```text
http://127.0.0.1:8766
```
