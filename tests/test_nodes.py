import pytest
from unittest.mock import patch, MagicMock
from langchain_core.messages import HumanMessage, SystemMessage
from app.graph.nodes import planner_node, agent_node, reflect_node

@patch('app.graph.nodes.get_llm')
def test_planner_node_existing_plan(mock_get_llm):
    state = {
        "messages": [HumanMessage(content="Hello")],
        "plan": "Existing plan"
    }
    result = planner_node(state)
    # Should not re-plan
    assert result == {}

@patch('app.graph.nodes.get_llm')
def test_planner_node_new_plan(mock_get_llm):
    state = {
        "messages": [HumanMessage(content="Task to plan")],
        "plan": ""
    }
    
    mock_llm = MagicMock()
    mock_structured_llm = MagicMock()
    # Mock the return of structured output
    mock_plan = MagicMock()
    mock_plan.plan_steps = "1. Step 1\n2. Step 2"
    mock_structured_llm.invoke.return_value = mock_plan
    
    mock_llm.with_structured_output.return_value = mock_structured_llm
    mock_get_llm.return_value = mock_llm
    
    result = planner_node(state)
    assert result == {"plan": "1. Step 1\n2. Step 2"}

@patch('app.graph.nodes.get_llm')
def test_agent_node(mock_get_llm):
    state = {
        "messages": [HumanMessage(content="Do something")],
        "plan": "1. Do something"
    }
    
    mock_llm = MagicMock()
    mock_llm_with_tools = MagicMock()
    mock_llm_with_tools.invoke.return_value = "Agent response"
    
    mock_llm.bind_tools.return_value = mock_llm_with_tools
    mock_get_llm.return_value = mock_llm
    
    result = agent_node(state)
    assert "messages" in result
    assert result["messages"] == ["Agent response"]

@patch('app.graph.nodes.get_llm')
def test_reflect_node_incomplete(mock_get_llm):
    state = {
        "messages": [HumanMessage(content="Status")],
        "plan": "Plan"
    }
    
    mock_llm = MagicMock()
    mock_structured_llm = MagicMock()
    mock_reflection = MagicMock()
    mock_reflection.summary = "Work in progress"
    mock_reflection.is_complete = False
    mock_reflection.final_answer = ""
    
    mock_structured_llm.invoke.return_value = mock_reflection
    mock_llm.with_structured_output.return_value = mock_structured_llm
    mock_get_llm.return_value = mock_llm
    
    result = reflect_node(state)
    assert result == {
        "reasoning_summary": "Work in progress",
        "final_answer": ""
    }

@patch('app.graph.nodes.get_llm')
def test_reflect_node_complete(mock_get_llm):
    state = {
        "messages": [HumanMessage(content="Done")],
        "plan": "Plan"
    }
    
    mock_llm = MagicMock()
    mock_structured_llm = MagicMock()
    mock_reflection = MagicMock()
    mock_reflection.summary = "Finished"
    mock_reflection.is_complete = True
    mock_reflection.final_answer = "Final answer"
    
    mock_structured_llm.invoke.return_value = mock_reflection
    mock_llm.with_structured_output.return_value = mock_structured_llm
    mock_get_llm.return_value = mock_llm
    
    result = reflect_node(state)
    assert result == {
        "reasoning_summary": "Finished",
        "final_answer": "Final answer"
    }
