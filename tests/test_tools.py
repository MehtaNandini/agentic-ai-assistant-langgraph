import os
from unittest.mock import patch, mock_open

from app.tools.calculator import calculator
from app.tools.memory import save_note, read_note
from app.tools.file_reader import read_local_file
from app.tools.web_search import web_search

def test_calculator_success():
    result = calculator.invoke({"expression": "25 * 4"})
    assert result == "100"

def test_calculator_error():
    result = calculator.invoke({"expression": "25 * abc"})
    assert "Error evaluating expression" in result

@patch('app.tools.memory.NOTES_FILE', new_callable=lambda: '')
def test_memory(mock_notes_file, tmp_path):
    # Use a temporary file for tests
    mock_notes_file = str(tmp_path / "test_notes.json")
    with patch('app.tools.memory.NOTES_FILE', mock_notes_file):
        # Test saving a note
        save_res = save_note.invoke({"topic": "test_topic", "content": "This is a test."})
        assert "successfully" in save_res
        
        # Test reading the note
        read_res = read_note.invoke({"topic": "test_topic"})
        assert read_res == "This is a test."

def test_file_reader_success(tmp_path):
    # Create a temporary file
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("hello world", encoding="utf-8")
    
    result = read_local_file.invoke({"file_path": str(p)})
    assert result == "hello world"

def test_file_reader_not_found():
    result = read_local_file.invoke({"file_path": "non_existent_file.txt"})
    assert "Error: File not found" in result

@patch('app.tools.web_search.DDGS')
def test_web_search_success(mock_ddgs):
    # Mock the DDGS instance and its text method
    mock_instance = mock_ddgs.return_value.__enter__.return_value
    mock_instance.text.return_value = [
        {"title": "Test Title", "body": "Test Body", "href": "http://test.com"}
    ]
    
    result = web_search.invoke({"query": "test query"})
    assert "Test Title" in result
    assert "Test Body" in result
    assert "http://test.com" in result

@patch('app.tools.web_search.DDGS')
def test_web_search_no_results(mock_ddgs):
    # Mock the DDGS instance returning empty list
    mock_instance = mock_ddgs.return_value.__enter__.return_value
    mock_instance.text.return_value = []
    
    result = web_search.invoke({"query": "test query"})
    assert "No results found" in result
