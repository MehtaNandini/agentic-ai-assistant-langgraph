from app.graph.workflow import app as graph_app, should_continue, is_done
from langchain_core.messages import AIMessage

def test_graph_compiles():
    # Simple test to ensure the graph compiles
    assert graph_app is not None

def test_should_continue_with_tools():
    # Simulate state with tool calls
    state = {
        "messages": [
            AIMessage(content="", tool_calls=[{"name": "calculator", "args": {"expression": "2+2"}, "id": "123"}])
        ]
    }
    result = should_continue(state)
    assert result == "tools"

def test_should_continue_without_tools():
    # Simulate state without tool calls
    state = {
        "messages": [
            AIMessage(content="Hello world")
        ]
    }
    result = should_continue(state)
    assert result == "reflect"

def test_is_done_with_final_answer():
    state = {
        "messages": [],
        "final_answer": "This is the final answer."
    }
    result = is_done(state)
    assert result == "__end__"

def test_is_done_without_final_answer():
    state = {
        "messages": [],
        "final_answer": ""
    }
    result = is_done(state)
    assert result == "planner"
