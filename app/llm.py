from google import genai
from google.genai import types
from dotenv import load_dotenv
from .schemas import SupportAnalysis

load_dotenv()
client = genai.Client()  # reads GEMINI_API_KEY from .env

SYSTEM_PROMPT = """You are a customer-support assistant for an e-commerce company.
Analyze the customer's message. Summarize the issue, pick the intent and urgency,
write a professional and empathetic reply, and say whether a human should take over."""

def analyze_query(message: str) -> SupportAnalysis:
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=message,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=SupportAnalysis,
        ),
    )
    return SupportAnalysis.model_validate_json(response.text)

if __name__ == "__main__":
    result = analyze_query("I paid twice, but my refund hasn't arrived")
    print(result.model_dump_json(indent=2))