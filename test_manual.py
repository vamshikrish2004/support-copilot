import time
from app.llm import analyze_query

messages = [
    "I paid twice, but my refund hasn't arrived",
    "Where is my order #1042? It was due 3 days ago",
    "This is the worst service ever, I want to speak to a manager",
    "it's not working",
    "What's the weather today?",
]

for m in messages:
    print("=" * 60)
    print("MESSAGE:", m)
    try:
        r = analyze_query(m)
        print("intent:", r.intent.value, "| urgency:", r.urgency.value, "| needs_human:", r.needs_human)
        print("summary:", r.issue_summary)
    except Exception as e:
        print("ERROR:", type(e).__name__, str(e)[:150])
    time.sleep(3)