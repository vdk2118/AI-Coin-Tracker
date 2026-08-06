import requests

URL = "https://api.dexscreener.com/token-boosts/latest/v1"


def get_trending():

    try:

        response = requests.get(URL, timeout=10)

        if response.status_code != 200:
            return "❌ Nu pot obține date."

        tokens = response.json()

        if len(tokens) == 0:
            return "Nu există tokenuri în Trending."

        mesaj = "📈 TRENDING MEMECOINS\n\n"

        for token in tokens[:10]:

            name = token.get("tokenName", "Necunoscut")
            chain = token.get("chainId", "")
            amount = token.get("amount", 0)

            mesaj += f"🪙 {name}\n"
            mesaj += f"🌐 {chain}\n"
            mesaj += f"🔥 Boost: {amount}\n\n"

        return mesaj

    except Exception as e:

        return f"❌ Eroare:\n{e}"