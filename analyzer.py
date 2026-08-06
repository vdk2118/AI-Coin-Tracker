import requests

DEX_URL = "https://api.dexscreener.com/latest/dex/tokens/"


def calculate_ai_score(liquidity, volume, marketcap):

    score = 0
    strengths = []
    risks = []

    # Liquidity
    if liquidity >= 500000:
        score += 30
        strengths.append("💧 Lichiditate foarte mare")
    elif liquidity >= 100000:
        score += 20
        strengths.append("💧 Lichiditate bună")
    elif liquidity >= 50000:
        score += 10
    else:
        risks.append("⚠️ Lichiditate mică")

    # Volume
    if volume >= 1000000:
        score += 30
        strengths.append("📈 Volum foarte mare")
    elif volume >= 250000:
        score += 20
        strengths.append("📈 Volum bun")
    elif volume >= 50000:
        score += 10
    else:
        risks.append("⚠️ Volum redus")

    # Market Cap
    if marketcap >= 10000000:
        score += 20
        strengths.append("🏦 Market Cap mare")
    elif marketcap >= 1000000:
        score += 15
    elif marketcap >= 250000:
        score += 10
    else:
        risks.append("⚠️ Market Cap mic")

    # Bonus
    if liquidity > 100000 and volume > 250000:
        score += 10

    if marketcap > 1000000 and liquidity > 100000:
        score += 10

    if score > 100:
        score = 100

    return score, strengths, risks


def analyze_token(contract):

    try:

        response = requests.get(
            DEX_URL + contract,
            timeout=10
        )

        if response.status_code != 200:
            return "❌ API indisponibil."

        data = response.json()

        if not data.get("pairs"):
            return "❌ Tokenul nu a fost găsit."

        pair = data["pairs"][0]

        name = pair["baseToken"]["name"]
        symbol = pair["baseToken"]["symbol"]
        chain = pair["chainId"]

        price = float(pair.get("priceUsd") or 0)

        liquidity = float(
            pair.get("liquidity", {}).get("usd") or 0
        )

        volume = float(
            pair.get("volume", {}).get("h24") or 0
        )

        marketcap = float(
            pair.get("marketCap") or 0
        )

        score, strengths, risks = calculate_ai_score(
            liquidity,
            volume,
            marketcap
        )

        if score >= 80:
            verdict = "🟢 Foarte Puternic"

        elif score >= 60:
            verdict = "🟡 Promițător"

        elif score >= 40:
            verdict = "🟠 Risc Mediu"

        else:
            verdict = "🔴 Risc Ridicat"

        mesaj = ""

        mesaj += "🤖 AI REPORT\n\n"

        mesaj += f"🪙 {name} ({symbol})\n"
        mesaj += f"🌐 Chain: {chain}\n\n"

        mesaj += f"💰 Preț: ${price:,.8f}\n"
        mesaj += f"💧 Lichiditate: ${liquidity:,.0f}\n"
        mesaj += f"📈 Volum 24h: ${volume:,.0f}\n"
        mesaj += f"🏦 Market Cap: ${marketcap:,.0f}\n\n"

        mesaj += f"⭐ AI Score: {score}/100\n"
        mesaj += f"{verdict}\n\n"

        mesaj += "✅ Puncte Forte\n"

        if len(strengths) == 0:
            mesaj += "• Niciun punct puternic detectat\n"

        for item in strengths:
            mesaj += f"{item}\n"

        mesaj += "\n⚠️ Riscuri\n"

        if len(risks) == 0:
            mesaj += "• Nu au fost detectate riscuri evidente\n"

        for item in risks:
            mesaj += f"{item}\n"

        mesaj += "\n📋 Concluzie\n"

        if score >= 80:
            mesaj += (
                "Tokenul îndeplinește mai multe criterii urmărite. "
                "Totuși, analizează și alte informații înainte de orice decizie."
            )

        elif score >= 60:
            mesaj += (
                "Tokenul are câteva caracteristici interesante, dar merită analizat în continuare."
            )

        else:
            mesaj += (
                "Indicatorii analizați sugerează un nivel de risc mai ridicat. "
                "Este recomandată prudență."
            )

        return mesaj

    except Exception as e:

        return f"❌ Eroare:\n{e}"