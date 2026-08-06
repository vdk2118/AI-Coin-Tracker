import requests

URL = "https://api.dexscreener.com/token-profiles/latest/v1"


def get_new_tokens():

    try:

        response = requests.get(URL, timeout=10)

        if response.status_code != 200:
            return "❌ Nu pot obține tokenurile noi."

        tokens = response.json()

        if not tokens:
            return "❌ Nu există tokenuri noi."

        mesaj = "🚀 TOKENURI NOI\n\n"

        for token in tokens[:10]:

            # Încearcă mai multe câmpuri pentru nume
            name = (
                token.get("tokenName")
                or token.get("name")
                or token.get("header")
                or token.get("title")
            )

            symbol = (
                token.get("tokenSymbol")
                or token.get("symbol")
                or ""
            )

            chain = token.get("chainId", "Necunoscut")

            contract = (
                token.get("tokenAddress")
                or token.get("address")
                or ""
            )

            description = token.get("description", "")

            # Dacă nu există nume, afișează o parte din contract
            if not name:
                if contract:
                    name = f"Contract: {contract[:10]}..."
                else:
                    name = "Fără nume"

            mesaj += f"🪙 {name}"

            if symbol:
                mesaj += f" ({symbol})"

            mesaj += "\n"
            mesaj += f"🌐 Chain: {chain}\n"

            if contract:
                mesaj += f"📄 {contract[:18]}...\n"

            if description:
                mesaj += f"📝 {description[:100]}\n"

            mesaj += "\n"

        return mesaj

    except Exception as e:
        return f"❌ Eroare:\n{e}"