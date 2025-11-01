import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

try:
    # ✅ Use a model that actually exists
    model = genai.GenerativeModel("models/gemini-2.5-flash")

    # Test message
    response = model.generate_content("Hey Gemini 👋 can you hear me?")
    print("✅ Gemini replied:", response.text)

except Exception as e:
    print("❌ Gemini Error:", e)
