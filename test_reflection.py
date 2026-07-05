import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from app.graph.nodes import reflect_node
from langchain_core.messages import HumanMessage, AIMessage

def run():
    state = {
        "messages": [
            HumanMessage(content="Search the web for the latest major news regarding Python 3.13 and summarize the top 2 features."),
            AIMessage(content="The top 2 features of Python 3.13 are the new interactive shell (REPL) and experimental support for a free-threaded build (disabling the GIL).")
        ],
        "plan": "1. Search for Python 3.13 news. 2. Summarize top 2 features."
    }
    print("Testing reflect_node...")
    try:
        result = reflect_node(state)
        print("RESULT:", result)
        print("is_complete boolean status (implied):", bool(result.get("final_answer")))
    except Exception as e:
        print("ERROR:", e)

if __name__ == "__main__":
    run()
