from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

names = [
    "gemini-3.8-flash",
    "gemini-3.1-flash-lite",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-3.5-flash",
]

for name in names:
    try:
        r = client.models.generate_content(model=name, contents="Say hello in one word.")
        print("WORKS:", name, "->", r.text.strip())
    except Exception as e:
        print("FAILED:", name, "->", type(e).__name__, str(e)[:150])