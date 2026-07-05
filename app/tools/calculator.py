from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression.
    
    Args:
        expression: A string containing a mathematical expression to evaluate (e.g. '2 + 2' or '25 * 4')
    """
    try:
        # Warning: eval is dangerous in production. Used here for demonstration/portfolio purposes.
        allowed_names = {"__builtins__": None}
        result = eval(expression, allowed_names, {})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"
