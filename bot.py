from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from keyboards import main_keyboard
from scanner import get_new_tokens
from trending import get_trending
from analyzer import analyze_token
from database import (
    init_database,
    add_token,
    get_tokens,
    delete_token,
)

# Creează baza de date la pornire
init_database()

# Stări utilizator
waiting_for_contract = set()
waiting_for_watchlist = set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 AI Coin Tracker\n\n"
        "Bine ai venit!\n\n"
        "Alege o opțiune folosind butoanele de mai jos.",
        reply_markup=main_keyboard,
    )


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    chat_id = update.effective_chat.id

    # ============================
    # AI ANALYZE
    # ============================

    if chat_id in waiting_for_contract:

        waiting_for_contract.remove(chat_id)

        rezultat = analyze_token(text)

        await update.message.reply_text(rezultat)

        return

    # ============================
    # WATCHLIST
    # ============================

    if chat_id in waiting_for_watchlist:

        waiting_for_watchlist.remove(chat_id)

        ok = add_token(chat_id, text)

        if ok:

            await update.message.reply_text(
                "✅ Token adăugat în Watchlist!"
            )

        else:

            await update.message.reply_text(
                "⚠️ Tokenul există deja în Watchlist."
            )

        return

    # ============================
    # MENIU
    # ============================

    if text == "🚀 Tokenuri Noi":

        await update.message.reply_text(
            get_new_tokens()
        )

    elif text == "📈 Trending":

        await update.message.reply_text(
            get_trending()
        )

    elif text == "🤖 AI Analyze":

        waiting_for_contract.add(chat_id)

        await update.message.reply_text(
            "📄 Trimite adresa contractului tokenului."
        )

    elif text == "❤️ Watchlist":

        tokens = get_tokens(chat_id)

        if len(tokens) == 0:

            waiting_for_watchlist.add(chat_id)

            await update.message.reply_text(
                "❤️ Watchlist este goală.\n\n"
                "Trimite adresa unui contract pentru a-l salva."
            )

        else:

            mesaj = "❤️ WATCHLIST\n\n"

            for token in tokens:

                mesaj += f"🪙 {token[0]}\n\n"

            mesaj += (
                "\nTrimite un contract nou pentru a-l adăuga."
            )

            waiting_for_watchlist.add(chat_id)

            await update.message.reply_text(mesaj)

    else:

        await update.message.reply_text(
            "❓ Folosește butoanele din meniu."
        )


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_buttons
    )
)

print("✅ AI Coin Tracker este pornit!")

app.run_polling()