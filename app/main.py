from fastapi import FastAPI, HTTPException
from app.schemas.requests import AgentRequest
from app.schemas.responses import AgentResponse, ToolCallSchema
from app.graph.workflow import app as graph_app
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI(
    title="Agentic AI Assistant API",
    description="API for running multi-step AI agent tasks using LangGraph",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/run-agent", response_model=AgentResponse)
def run_agent(request: AgentRequest):
    try:
        config = {"configurable": {"thread_id": request.thread_id}}
        
        # Initial input state
        input_state = {
            "messages": [HumanMessage(content=request.task)]
        }
        
        # Run the graph
        final_state = graph_app.invoke(input_state, config=config)
        
        # Extract necessary fields for response
        final_answer = final_state.get("final_answer", "")
        plan = final_state.get("plan", "")
        reasoning_summary = final_state.get("reasoning_summary", "")
        
        # Extract tool calls from messages
        tool_calls = []
        for msg in final_state.get("messages", []):
            if isinstance(msg, AIMessage) and hasattr(msg, 'tool_calls'):
                for tc in msg.tool_calls:
                    tool_calls.append(ToolCallSchema(
                        tool_name=tc.get('name', 'unknown'),
                        tool_input=tc.get('args', {})
                    ))
                    
        return AgentResponse(
            final_answer=final_answer,
            plan=plan,
            tool_calls=tool_calls,
            reasoning_summary=reasoning_summary
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
