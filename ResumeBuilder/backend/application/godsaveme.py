from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: API Key not found.")
else:
    client = genai.Client(api_key=api_key)
    print("\n🔍 Scanning available models (names only)...")
    
    try:
        # We just print the name directly. No filtering.
        for model in client.models.list():
            # The name comes as "models/gemini-1.5-flash
            # We strip the "models/" part for clarity
            clean_name = model.name.replace("models/", "")
            print(f"   • {clean_name}")
            
    except Exception as e:
        print(f"❌ Error: {e}")