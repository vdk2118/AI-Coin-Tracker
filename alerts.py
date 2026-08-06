import requests

DEX_NEW = "https://api.dexscreener.com/token-profiles/latest/v1"

# Tokenurile deja verificate
seen_tokens = set()


def get_hot_tokens():

    try:

        response = requests.get(DEX_NEW, timeout=10)

        if response.status_code != 200:
            return []

        data = response.json()

        rezultate = []

        for token in data:

            contract = token.get("tokenAddress", "")

            if contract in seen_tokens:
                continue

            seen_tokens.add(contract)

            rezultate.append({
                "name": token.get("tokenName", "Unknown"),
                "symbol": token.get("tokenSymbol", ""),
                "chain": token.get("chainId", ""),
                "contract": contract
            })

        return rezultate

    except:

        return []