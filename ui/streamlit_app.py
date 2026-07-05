import streamlit as st
import requests
import json
import uuid

# Configuration
API_URL = "http://localhost:8000/run-agent"

st.set_page_config(page_title="Agentic AI Assistant", page_icon="🤖", layout="wide")

st.title("🤖 Agentic AI Assistant")
st.markdown("A LangGraph-powered AI assistant that plans, uses tools, and reflects to solve tasks.")

# Initialize session state for thread_id and history
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "details" in msg:
            with st.expander("View Agent Process Details"):
                st.markdown(f"**Plan:**\n{msg['details'].get('plan', 'N/A')}")
                st.markdown(f"**Reasoning Summary:**\n{msg['details'].get('reasoning_summary', 'N/A')}")
                if msg['details'].get('tool_calls'):
                    st.markdown("**Tools Used:**")
                    st.json(msg['details']['tool_calls'])

# User input
if prompt := st.chat_input("Enter your task..."):
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Call backend API
    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking..."):
            try:
                response = requests.post(
                    API_URL, 
                    json={"task": prompt, "thread_id": st.session_state.thread_id},
                    timeout=120
                )
                if response.status_code == 200:
                    data = response.json()
                    
                    # Display final answer
                    st.markdown(data.get("final_answer", ""))
                    
                    # Expandable details section
                    with st.expander("View Agent Process Details"):
                        st.markdown(f"**Plan:**\n{data.get('plan', 'N/A')}")
                        st.markdown(f"**Reasoning Summary:**\n{data.get('reasoning_summary', 'N/A')}")
                        if data.get('tool_calls'):
                            st.markdown("**Tools Used:**")
                            st.json(data['tool_calls'])
                            
                    # Add to history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": data.get("final_answer", ""),
                        "details": data
                    })
                else:
                    st.error(f"Error from backend: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to API: {e}. Is the backend running?")
