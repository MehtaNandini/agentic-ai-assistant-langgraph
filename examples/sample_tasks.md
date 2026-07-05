# Sample Tasks for the Agent

Copy and paste these tasks into the Streamlit UI to test the agent's capabilities.

## 1. Calculator & Web Search Integration
> "Calculate 25 multiplied by 14, then search the web for the capital of France, and finally provide a summary of both results."

**Expected Agent Behavior:**
1. Plan to use the calculator tool and the web search tool.
2. Execute `calculator(expression="25 * 14")`.
3. Execute `web_search(query="capital of France")`.
4. Reflect and synthesize the final answer.

## 2. Memory Usage
> "Save a note under the topic 'My Favorite Color' saying 'Blue'."

*Then, in the next prompt:*
> "What is my favorite color based on your memory?"

**Expected Agent Behavior:**
1. Plan to use `save_note` tool.
2. In the next turn, plan to use `read_note` tool.

## 3. Local File Reader
> "Read the contents of `README.md` and summarize what this project is about."

**Expected Agent Behavior:**
1. Plan to use `read_local_file(file_path="README.md")`.
2. Reflect and summarize the read content.
