from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from app.graph.state import AgentState
from app.graph.nodes import planner_node, agent_node, reflect_node, TOOLS
from app.services.memory_store import get_checkpointer

def should_continue(state: AgentState) -> str:
    """Decides whether to continue calling tools or go to reflection."""
    messages = state["messages"]
    last_message = messages[-1]
    
    if last_message.tool_calls:
        return "tools"
    return "reflect"

def is_done(state: AgentState) -> str:
    """Decides if the workflow is complete."""
    if state.get("final_answer"):
        return END
    return "planner" # loop back if not done (or could go to agent directly, but planner acts as a no-op if plan exists)

# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("planner", planner_node)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(TOOLS))
workflow.add_node("reflect", reflect_node)

# Add edges
workflow.add_edge(START, "planner")
workflow.add_edge("planner", "agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", "reflect": "reflect"})
workflow.add_edge("tools", "agent")
workflow.add_conditional_edges("reflect", is_done, {END: END, "planner": "planner"})

# Compile with checkpointer
checkpointer = get_checkpointer()
app = workflow.compile(checkpointer=checkpointer)
