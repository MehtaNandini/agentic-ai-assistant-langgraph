from app.graph.state import AgentState
from app.services.llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from pydantic import BaseModel, Field

from app.tools.calculator import calculator
from app.tools.file_reader import read_local_file
from app.tools.memory import save_note, read_note
from app.tools.web_search import web_search

TOOLS = [calculator, read_local_file, save_note, read_note, web_search]

class Plan(BaseModel):
    plan_steps: str = Field(description="A numbered list of steps to solve the task")

class Reflection(BaseModel):
    summary: str = Field(description="A safe, high-level summary of the current progress and reasoning.")
    is_complete: bool = Field(description="A boolean value (true or false, NOT a string). True if the task is completely resolved and we have a final answer.")
    final_answer: str = Field(description="The final answer to the user, if complete.")

def planner_node(state: AgentState) -> dict:
    """Creates a plan for the task if one doesn't exist."""
    llm = get_llm()
    # If plan already exists, don't re-plan unless requested
    if state.get("plan"):
        return {}
        
    messages = state.get("messages", [])
    sys_msg = SystemMessage(content="You are an expert planner. Break down the user's task into logical steps. Return ONLY the plan steps.")
    
    planner = llm.with_structured_output(Plan)
    result = planner.invoke([sys_msg] + messages)
    
    return {"plan": result.plan_steps}

def agent_node(state: AgentState) -> dict:
    """The main agent that decides which tools to call or what to say."""
    llm = get_llm()
    llm_with_tools = llm.bind_tools(TOOLS)
    
    plan_text = state.get('plan', 'No plan yet.')
    sys_msg = SystemMessage(
        content=f"You are a helpful AI assistant. You have a plan: {plan_text}. "
                f"Execute the steps using the provided tools. You MUST use the actual tool-calling function mechanism to invoke tools. "
                f"DO NOT output raw JSON strings or dictionaries in your text response. "
                f"If you have finished the plan, explain the final result clearly in plain text."
    )
    
    response = llm_with_tools.invoke([sys_msg] + state["messages"])
    return {"messages": [response]}

def reflect_node(state: AgentState) -> dict:
    """Reflects on the progress and decides if we are done, while summarizing reasoning."""
    llm = get_llm()
    sys_msg = SystemMessage(
        content="Review the conversation history and the plan. Provide a brief summary of what has been done so far. "
                "If the task is fully resolved and the assistant provided the final answer, set is_complete to true and provide the final_answer. "
                "CRITICAL INSTRUCTIONS TO PREVENT ERRORS: "
                "1. The is_complete field MUST be a strict boolean literal (true or false). "
                "2. Keep the summary extremely short (1-2 sentences maximum). "
                "3. Do NOT use any quotation marks (' or \") inside the summary or final_answer text, as it breaks JSON parsing."
    )
    
    reflector = llm.with_structured_output(Reflection)
    try:
        result = reflector.invoke([sys_msg] + state["messages"])
        
        return {
            "reasoning_summary": result.summary,
            "final_answer": result.final_answer if result.is_complete else ""
        }
    except Exception as e:
        # Fallback if LLM generates malformed JSON
        print(f"Warning: Reflection structured output failed: {e}")
        # Try to infer if we should be done based on the last message
        last_msg = state["messages"][-1]
        is_done = not hasattr(last_msg, "tool_calls") or len(last_msg.tool_calls) == 0
        return {
            "reasoning_summary": "Reflection parsing failed, but continuing workflow.",
            "final_answer": last_msg.content if is_done else ""
        }
