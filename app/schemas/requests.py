from pydantic import BaseModel, Field

class AgentRequest(BaseModel):
    task: str = Field(..., description="The task for the agent to execute")
    thread_id: str = Field("default", description="The conversation thread ID")
