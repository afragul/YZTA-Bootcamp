# model_listesi.py (proje kokunde)
import os
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("SENIN HESABINDA KULLANILABILIR MODELLER:\n")
for m in client.models.list():
    if "generateContent" in getattr(m, "supported_actions", []):
        print(f"  {m.name}")