import os
from dotenv import load_dotenv
load_dotenv()

from app.graph.workflow import app

def run():
    print("Setting up graph...")
    print("Sending message...")
    try:
        config = {"configurable": {"thread_id": "test_groq_4"}}
        state = {"messages": [("user", "Calculate 15% of 1250, and then multiply the result by 3.")]}
        print("Invoking...")
        result = app.invoke(state, config)
        print("RESULT PLAN:", result.get("plan"))
        print("RESULT REASONING:", result.get("reasoning_summary"))
        print("RESULT FINAL:", result.get("final_answer"))
    except Exception as e:
        print("ERROR:", e)

if __name__ == "__main__":
    run()
