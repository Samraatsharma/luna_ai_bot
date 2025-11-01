import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import google.generativeai as genai

# --- Load Environment Variables ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
RENDER_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"

# --- Configure Gemini ---
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Initialize Flask ---
flask_app = Flask(__name__)

# --- Initialize Telegram Bot ---
application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# --- Commands ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌙 Hello, I'm Luna — your AI assistant powered by Gemini! Ask me anything ✨")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💡 Just send me any question, and I'll reply intelligently using Gemini AI!")

# --- Chat Handler (Gemini AI Reply) ---

async def chat_with_luna(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.message.from_user.first_name

    try:
        response = model.generate_content(user_message)
        ai_reply = response.text if response.text else "⚠️ Sorry, I couldn’t generate a proper response."
    except Exception as e:
        ai_reply = f"❌ Oops, something went wrong: {str(e)}"

    await update.message.reply_text(f"✨ {user_name}, {ai_reply}")

# --- Telegram Handlers ---
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_luna))

# --- Webhook Route ---
@flask_app.route("/webhook", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "OK", 200

# --- Root Route ---
@flask_app.route("/", methods=["GET"])
def home():
    return "🌍 Luna AI (Gemini-powered) is running on Render Webhook!", 200

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
