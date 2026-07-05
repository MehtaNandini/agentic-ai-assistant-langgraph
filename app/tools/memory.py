import os
import json
from langchain_core.tools import tool

NOTES_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "notes.json")

@tool
def save_note(topic: str, content: str) -> str:
    """Saves a note to memory for future reference.
    
    Args:
        topic: The topic or title of the note.
        content: The information to save.
    """
    try:
        notes = {}
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r") as f:
                notes = json.load(f)
        
        notes[topic] = content
        
        with open(NOTES_FILE, "w") as f:
            json.dump(notes, f, indent=4)
            
        return f"Note saved successfully under topic '{topic}'."
    except Exception as e:
        return f"Error saving note: {e}"

@tool
def read_note(topic: str) -> str:
    """Reads a previously saved note by topic.
    
    Args:
        topic: The topic of the note to retrieve.
    """
    try:
        if not os.path.exists(NOTES_FILE):
            return "No notes found. Memory is empty."
            
        with open(NOTES_FILE, "r") as f:
            notes = json.load(f)
            
        if topic in notes:
            return notes[topic]
        return f"No note found for topic '{topic}'."
    except Exception as e:
        return f"Error reading note: {e}"
