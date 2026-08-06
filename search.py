import requests

SEARCH_URL = "https://api.dexscreener.com/latest/dex/search?q="


def search_token(query):

    try:

        response = requests.get(
            SEARCH_URL + query,
            timeout=10
        )

        if response.status_code != 200:
            return "❌ API indisponibil."

        data = response.json()

        pairs = data.get("pairs")

        if not pairs:
            return "❌ Nu am găsit niciun token."

        mesaj = f"🔍 Rezultate pentru: {query.upper()}\n\n"

        for pair in pairs[:5]:

            name = pair["baseToken"]["name"]
            symbol = pair["baseToken"]["symbol"]

            chain = pair["chainId"]

            price = pair.get("priceUsd", "0")

            liquidity = pair.get("liquidity", {}).get("usd", 0)

            volume = pair.get("volume", {}).get("h24", 0)

            mesaj += f"🪙 {name} ({symbol})\n"

            mesaj += f"🌐 {chain}\n"

            mesaj += f"💰 ${price}\n"

            mesaj += f"💧 Liquidity ${liquidity:,.0f}\n"

            mesaj += f"📈 Volume ${volume:,.0f}\n"

            mesaj += "\n"

        return mesaj

    except Exception as e:

        return f"❌ {e}"