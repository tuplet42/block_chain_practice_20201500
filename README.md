# block_chain_practice_20201500

# This repository contains:
- GitHub Pages homepage
- Bitcoin and Ethereum price table
- CoinGecko API integration

# Overall Structures : 
block_chain_practice_20201500/
├── README.md
├── steps.md
├── index.html
└── scripts/
    └── fetch_prices.py

## File Descriptions

| File | Language | Purpose | When It Runs | API Usage | Output |
|------|----------|----------|-------------|-----------|--------|
| `scripts/fetch_prices.py` | Python | Fetches BTC & ETH prices in KRW from CoinGecko and updates the Markdown table in README | Manually executed (Codespaces / local) | Server-side request using `requests` | Updates static table in `README.md` |
| `index.html` | HTML + JavaScript | Displays real-time BTC & ETH prices on the website | Runs automatically in the browser | Client-side `fetch()` call to CoinGecko API | Dynamically updates webpage every 10 seconds |

<!-- PRICE_TABLE_START -->
## Today's Prices Examples(KRW)

_Last updated: 2026-03-03 07:34_

| Coin | Price (KRW) |
|------|-------------|
| Bitcoin (BTC) | ₩99,970,726 |
| Ethereum (ETH) | ₩2,931,210 |
<!-- PRICE_TABLE_END -->
