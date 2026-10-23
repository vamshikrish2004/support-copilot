import time
from google import genai
from google.genai import types, errors
from dotenv import load_dotenv
from .tools import check_order_status, create_ticket, escalate_to_human

load_dotenv()
client = genai.Client()

MODEL = "gemini-flash-lite-latest"

AGENT_PROMPT = """You are a customer-support assistant for an e-commerce company.
You can use tools:
- check_order_status: when the customer asks about an order and gives an order number.
- create_ticket: always use this for refund problems (double charges, missing refunds), damaged items, wrong items, missing packages and delays.
- escalate_to_human: when the customer is very angry, asks for a manager, or the issue is serious.
Rules: never invent order details. Only use facts returned by the tools.
If the customer's message is vague, ask a clarifying question instead of using a tool.
Always finish with a short, polite reply to the customer."""


def run_agent(message: str, retries: int = 4):
    """Returns (reply_text, list_of_tools_used)."""
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=message,
                config=types.GenerateContentConfig(
                    system_instruction=AGENT_PROMPT,
                    tools=[check_order_status, create_ticket, escalate_to_human],
                ),
            )
            tools_used = []
            for content in response.automatic_function_calling_history or []:
                for part in content.parts or []:
                    if part.function_call:
                        tools_used.append(part.function_call.name)
            return response.text, tools_used
        except errors.ServerError:
            # Only retry temporary server problems (503). Quota errors (429) stop immediately.
            if attempt == retries - 1:
                raise
            wait = 3 * 2 ** attempt
            print(f"  (server busy, retrying in {wait}s)")
            time.sleep(wait)