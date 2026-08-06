from telegram import ReplyKeyboardMarkup

keyboard = [
    ["🚀 Tokenuri Noi", "📈 Trending"],
    ["🤖 AI Analyze", "❤️ Watchlist"],
]

main_keyboard = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)