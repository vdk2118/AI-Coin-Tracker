import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

DEXSCREENER_API = "https://api.dexscreener.com"
GECKO_API = "https://api.geckoterminal.com/api/v2"

BOT_NAME = "AI Coin Tracker PRO"

AI_SCORE_MAX = 100

MIN_LIQUIDITY = 50000
MIN_VOLUME = 100000
MIN_MARKET_CAP = 250000

CHECK_INTERVAL = 60

DATABASE_NAME = "data.db"