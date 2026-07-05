# Architecture: Agentic AI Assistant

This document outlines the architecture of the `agentic-ai-assistant-langgraph` project.

## High-Level Design

```mermaid
graph TD
    User([User]) --> UI[Streamlit UI]
    UI -->|HTTP POST| API[FastAPI Backend]
    API --> Agent[LangGraph Agent]
    
    subgraph LangGraph Agent
        AgentState[(State)]
        AgentNode[Agent Node]
        ToolNode[Tool Execution Node]
        
        AgentNode -->|Decide Tool| ToolNode
        ToolNode -->|Tool Result| AgentNode
        AgentNode -->|Final Answer| EndNode[End]
    end
    
    ToolNode -.-> Tools[Tools]
    
    subgraph Tools
        Calc[Calculator]
        File[Local File Reader]
        Mem[Memory/Notes Saver]
        Search[Web Search]
    end
    
    Agent --> DB[(SQLite Memory)]
```

## Components

1. **Streamlit UI (`ui/streamlit_app.py`)**: A lightweight chat interface. It displays the final answer, agent plan, tool calls, and intermediate reasoning.
2. **FastAPI Backend (`app/main.py`)**: Provides endpoints (`/run-agent` and `/health`). It wraps the LangGraph workflow and ensures that chain-of-thought is safely summarized before sending it to the client.
3. **LangGraph Agent (`app/graph/workflow.py`)**: The core AI logic. It uses a state graph to iterate between planning, tool execution, and reflection until a final answer is produced.
4. **Tools (`app/tools/`)**: A collection of specific capabilities that the agent can invoke to interact with the world and gather context.
5. **Memory Store (`app/services/memory_store.py`)**: Utilizes SQLite via LangGraph's checkpointer to persist conversation history across interactions.
