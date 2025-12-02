from tools import get_current_time, get_my_address, get_my_personal_details

tool_descriptions = {
    "general_tool": "For general questions, facts,and web searches.",
    "get_my_address": "Use when asked about my personal address.",
    "get_my_personal_details": "Use when asked about my personal information, like name, age, or email.",
    "get_current_time": "Use when asked for the current time or date.",
}

def create_tool_prompt(user_query):
    """Create a prompt that helps the LLM choose the right tool."""
    tools_text = "\n".join([f"- {name}: {desc}" for name, desc in tool_descriptions.items()])
    prompt = f"""
    Given the user's query, which of the following tools is the most appropriate?

    Available tools:
    {tools_text}

    User query: "{user_query}"

    Respond with only the name of the tool that best fits the query. If no tool fits, respond with "none".
    Tool: """
    return prompt

def choose_tool(tool_decision):
    """Choose the tool based on the decision."""
    tools = {
        "get_current_time": get_current_time,
        "get_my_address": get_my_address,
        "get_my_personal_details": get_my_personal_details,
        "general_tool": "general_tool"  # Just a placeholder for general tool
    }

    if tool_decision in tools:
        if tool_decision == "general_tool":
            return "Executing general_tool..."  # Placeholder for the general tool's behavior
        return tools[tool_decision]()  # Executes the chosen tool function
    else:
        return "Error: Tool not found."

