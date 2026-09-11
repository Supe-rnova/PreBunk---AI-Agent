import os
from dotenv import load_dotenv
load_dotenv()

for name in ["GEMINI_API_KEY", "TELEGRAM_BOT_TOKEN", "LANGFUSE_PUBLIC_KEY",
             "LANGFUSE_SECRET_KEY", "LANGFUSE_BASE_URL"]:
    print(("OK      " if os.getenv(name) else "MISSING ") + name)

from google import genai
client = genai.Client()  # reads GEMINI_API_KEY automatically
print("\nFlash models your key can use:")
for m in client.models.list():
    if "flash" in m.name:
        print("  ", m.name)
print()
for var in ["GEMINI_MODEL", "GEMINI_LITE_MODEL"]:
    model = os.getenv(var)
    try:
        reply = client.models.generate_content(model=model, contents="Say OK")
        print(f"{var} ({model}) says:", reply.text)
    except Exception as e:
        print(f"{var} ({model}) FAILED:", str(e)[:200])

from langfuse import get_client
print("Langfuse connected:", get_client().auth_check())