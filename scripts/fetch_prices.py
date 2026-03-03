import requests
from datetime import datetime

URL = "https://api.coingecko.com/api/v3/simple/price"

params = {
    "ids": "bitcoin,ethereum",
    "vs_currencies": "krw"
}

response = requests.get(URL, params=params)
data = response.json()

btc = data["bitcoin"]["krw"]
eth = data["ethereum"]["krw"]

now = datetime.now().strftime("%Y-%m-%d %H:%M")

table = f"""
## Today's Prices (KRW)

_Last updated: {now}_

| Coin | Price (KRW) |
|------|-------------|
| Bitcoin (BTC) | ₩{btc:,} |
| Ethereum (ETH) | ₩{eth:,} |
"""

start = "<!-- PRICE_TABLE_START -->"
end = "<!-- PRICE_TABLE_END -->"

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

before = content.split(start)[0]
after = content.split(end)[1]

new_content = before + start + table + end + after

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)

print("README updated with KRW prices.")
