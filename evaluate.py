import json
import os
import time
from google.genai import errors
from app.agent import run_agent, MODEL

TEST_FILE = "data/test_cases.json"
RESULTS_FILE = "data/results.json"
PAUSE_SECONDS = 6


def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def is_correct(expected_tool, tools_used):
    if expected_tool == "none":
        return len(tools_used) == 0
    return expected_tool in tools_used


def main():
    cases = load_json(TEST_FILE, [])
    results = load_json(RESULTS_FILE, {})  # keyed by case id (as string)

    for case in cases:
        key = str(case["id"])
        if key in results:
            continue  # already done, skip

        print(f"Case {case['id']}: {case['message']}")
        start = time.time()
        try:
            reply, tools_used = run_agent(case["message"])
        except errors.ClientError as e:
            print("  Quota or client error. Stopping. Run again later to continue.")
            print("  ", str(e)[:120])
            break
        except Exception as e:
            print("  Error:", type(e).__name__, str(e)[:120])
            break
        latency = round(time.time() - start, 2)

        results[key] = {
            "id": case["id"],
            "category": case["category"],
            "message": case["message"],
            "expected_tool": case["expected_tool"],
            "tools_used": tools_used,
            "correct": is_correct(case["expected_tool"], tools_used),
            "latency_seconds": latency,
            "reply": reply,
            "model": MODEL,
        }
        save_json(RESULTS_FILE, results)  # save after every case
        print(f"  tools={tools_used} correct={results[key]['correct']} ({latency}s)")
        time.sleep(PAUSE_SECONDS)

    # Summary
    done = list(results.values())
    if not done:
        print("No results yet.")
        return
    total = len(done)
    right = sum(r["correct"] for r in done)
    print("\n" + "=" * 50)
    print(f"Completed {total}/{len(cases)} cases")
    print(f"Overall tool accuracy: {right}/{total} = {right / total:.0%}")
    categories = sorted({r["category"] for r in done})
    for c in categories:
        group = [r for r in done if r["category"] == c]
        ok = sum(r["correct"] for r in group)
        print(f"  {c}: {ok}/{len(group)}")
    avg_latency = sum(r["latency_seconds"] for r in done) / total
    print(f"Average latency: {avg_latency:.1f}s")
    wrong = [r for r in done if not r["correct"]]
    if wrong:
        print("\nWrong cases:")
        for r in wrong:
            print(f"  #{r['id']} expected={r['expected_tool']} got={r['tools_used']} | {r['message']}")


if __name__ == "__main__":
    main()