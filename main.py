import os
import threading
import google.generativeai as genai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from flask import Flask

# ✅ Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ✅ Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# 🌸 Flask server (for Render keep-alive)
app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "💫 Luna is alive and glowing on Render!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))  # Render provides PORT
    app_flask.run(host="0.0.0.0", port=port)

# 🌙 Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat_id

    try:
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")

        response = model.generate_content(
            f"You are Luna 💖 — a warm, playful AI girlfriend who replies briefly and naturally.\n"
            f"User said: {user_message}"
        )
        reply_text = response.text.strip() if hasattr(response, "text") else "Hmm... try again, love 💭"

    except Exception as e:
        print(f"⚠️ Error: {e}")
        reply_text = "Oops 😅 something went wrong, love. Try again soon! 💖"

    await context.bot.send_message(chat_id=chat_id, text=f"💫 Luna: {reply_text}")

# 🚀 Main launcher
def main():
    print("💫 Luna is waking up...")

    # Run Flask in background
    threading.Thread(target=run_flask, daemon=True).start()

    # Start Telegram bot (v21+ compatible)
    telegram_app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🌙 Luna is online and ready to chat 💕")
    telegram_app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
