def execute_tool(tool_name):
    """Execute the specified tool and return its result"""
    from tools import get_current_time, get_my_address, get_my_personal_details

    tools = {
        "get_current_time": get_current_time,
        "get_my_address": get_my_address,
        "get_my_personal_details": get_my_personal_details
    }

    if tool_name in tools:
        return tools[tool_name]()
    else:
        return f"Error: Tool '{tool_name}' not found."
