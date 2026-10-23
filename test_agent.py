import time
from app.agent import run_agent

messages = [
    "Where is my order #1042? It was due 3 days ago",
    "This is the worst service ever, I want to speak to a manager",
    "What's the weather today?",
    "it's not working",
]

for m in messages:
    print("=" * 60)
    print("MESSAGE:", m)
    try:
        reply, tools_used = run_agent(m)
        print("TOOLS USED:", tools_used)
        print("REPLY:", reply)
    except Exception as e:
        print("ERROR:", type(e).__name__, str(e)[:200])
    time.sleep(3)