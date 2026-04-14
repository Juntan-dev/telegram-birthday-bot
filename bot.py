from datetime import datetime, time
from zoneinfo import ZoneInfo
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing")

GROUP_CHAT_ID = -4925926064
TIMEZONE = ZoneInfo("Asia/Kuala_Lumpur")

BIRTHDAYS = {
    "Lauren": "07-03",
    "Edison": "15-04",
    "Kevin": "23-04",
    "Tracy": "30-04",
    "Alfred": "29-05",
    "Kang Lin": "19-06",
    "Justin": "23-07",
    "Alice": "04-08",
    "Kayden": "05-08",
    "Khloe": "10-09",
    "Andrew": "11-09",
    "Jun Jie": "14-09",
    "Wen Kang": "27-09",
    "Komi": "28-11"
}

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running")

    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        f"Chat ID is: {chat_id}",
        allow_sending_without_reply=True
    )
    print("CHAT ID:", chat_id)

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot is working ✅",
        allow_sending_without_reply=True
    )

async def check_birthdays(context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now(TIMEZONE).strftime("%d-%m")

    birthday_people = [
        name for name, date in BIRTHDAYS.items() if date == today
    ]

    if birthday_people:
        names = ", ".join(birthday_people)
        await context.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=f"🎉 Today is {names}'s birthday! Wish them!"
        )

def main():
    threading.Thread(target=run_dummy_server, daemon=True).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CommandHandler("test", test))

    app.job_queue.run_once(check_birthdays, when=5)
    app.job_queue.run_daily(
        check_birthdays,
        time=time(hour=9, minute=0, tzinfo=TIMEZONE)
    )

    app.run_polling()

if __name__ == "__main__":
    main()
