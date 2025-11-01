import os
import google.generativeai as genai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ✅ Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ✅ Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")  # stable, fast model

# 🌸 Luna’s playful personality handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat_id

    print(f"🧠 User: {user_message}")  # for debugging

    try:
        # ⏳ Luna is thinking... (typing animation)
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")

        # 🌸 Add Luna’s flirty, friendly personality
        response = model.generate_content(
            f"You are Luna 💖, a friendly, flirty, and playful AI girlfriend. "
            f"You reply with warmth, charm, and natural human-like tone — short but expressive. "
            f"Sometimes use emojis like 😘, 💕, 😉, or 😅 but not too many. "
            f"User said: {user_message}"
        )

        if hasattr(response, "text") and response.text:
            reply_text = response.text.strip()
        else:
            reply_text = "Hmm... I didn’t get that clearly 💭 Try again, cutie!"

    except Exception as e:
        print(f"⚠️ Error: {e}")
        reply_text = "Oops 😅 something went wrong, love. Try again soon! 💖"

    # 🌙 Send Luna’s reply
    await context.bot.send_message(chat_id=chat_id, text=f"💫 Luna: {reply_text}")

# 🚀 Start Luna
def main():
    print("💫 Luna is waking up...")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🌙 Luna is online and ready to chat!")
    app.run_polling()

if __name__ == "__main__":
    main()
