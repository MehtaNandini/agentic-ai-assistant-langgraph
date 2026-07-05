import os
from langchain_core.tools import tool

@tool
def read_local_file(file_path: str) -> str:
    """Reads the contents of a local file.
    
    Args:
        file_path: The relative or absolute path to the file to read.
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File not found at {file_path}"
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file: {e}"
