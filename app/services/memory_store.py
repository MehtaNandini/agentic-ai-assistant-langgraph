import os
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "memory.db")

def get_checkpointer():
    """Returns a SqliteSaver checkpointer for LangGraph."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return SqliteSaver(conn)
