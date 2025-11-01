import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load environment variables
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
RENDER_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"

# Initialize Flask app
flask_app = Flask(__name__)

# Initialize Telegram bot
application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# --- Telegram Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Luna AI is live and connected via webhook!")

application.add_handler(CommandHandler("start", start))

# --- Webhook Route ---

@flask_app.route("/webhook", methods=["POST"])
async def webhook():
    """Handle incoming Telegram updates."""
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "OK", 200

# --- Root Route ---

@flask_app.route("/", methods=["GET"])
def home():
    return "🌙 Luna AI Bot is running on Render Webhook!", 200

# --- Set Webhook Automatically ---

@flask_app.before_first_request
def set_webhook():
    webhook_url = f"{RENDER_URL}/webhook"
    application.bot.set_webhook(webhook_url)
    print(f"✅ Webhook set successfully: {webhook_url}")

# --- Run Flask Server ---

def main():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
