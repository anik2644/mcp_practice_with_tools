from tools import get_current_time, get_my_address, get_my_personal_details

tool_descriptions = {
    "general_tool": "For general questions, facts, recommendations, and web searches.",
    "get_my_address": "Use when asked about my location or address.",
    "get_my_personal_details": "Use when asked about my personal information, like name, age, or email.",
    "get_current_time": "Use when asked for the current time or date.",
}
def create_tool_prompt(user_query):
    """Create a prompt that helps the LLM choose the right tool."""
    tools_text = "\n".join([f"- {name}: {desc}" for name, desc in tool_descriptions.items()])

    prompt = f"""Given the user's query, which of the following tools is the most appropriate?

Available tools:
{tools_text}

User query: "{user_query}"

Respond with only the name of the tool.
Tool:"""
    return prompt

def choose_tool(tool_decision):
    """Choose the tool based on the decision"""
    tools = {
        "get_current_time": get_current_time,
        "get_my_address": get_my_address,
        "get_my_personal_details": get_my_personal_details
    }

    if tool_decision in tools:
        return tools[tool_decision]()
    else:
        return "Error: Tool not found."
