from app.tools.calculator import calculator
from app.tools.memory import save_note, read_note

def test_calculator():
    result = calculator.invoke({"expression": "25 * 4"})
    assert result == "100"

def test_memory():
    # Test saving a note
    save_res = save_note.invoke({"topic": "test_topic", "content": "This is a test."})
    assert "successfully" in save_res
    
    # Test reading the note
    read_res = read_note.invoke({"topic": "test_topic"})
    assert read_res == "This is a test."
