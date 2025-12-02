from llm_response import LLMResponse
from tool_selector import create_tool_prompt
from tool_executor import execute_tool
import asyncio
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from mcp_use import MCPAgent, MCPClient
import os

async def process_user_query_with_fallback(user_query):
    """Main function to process user queries with tool usage or fall back to MCP chat"""
    print(f"\nUser: {user_query}")

    # Initialize LLMResponse object
    llm = LLMResponse()

    # Step 1: Decide which tool to use
    tool_prompt = create_tool_prompt(user_query)
    tool_decision = llm.get_response(tool_prompt)

    # Ensure only the tool name is extracted (remove any description or extra text)
    tool_decision = tool_decision.strip().split(":")[0].strip().lower()

    print(f"Tool decision: {tool_decision}")

    # Step 2: Execute tool if one was chosen, or fall back to general_tool if no specific tool is found
    if tool_decision in ["get_current_time", "get_my_address", "get_my_personal_details"]:
        # Execute the chosen specific tool
        print(f"Executing tool: {tool_decision}")
        tool_result = execute_tool(tool_decision)
        print(f"Tool result: {tool_result}")
        context = f"I found this information: {tool_result}"
        final_response = llm.get_response(user_query, context)
    elif tool_decision == "find_hotels":
        # Execute the airbnb_search tool directly
        print("Executing airbnb_search tool for hotels...")
        tool_result = execute_tool("airbnb_search")
        print(f"Executed tool: airbnb_search")
        print(f"Tool result: {tool_result}")
        context = f"I found this information: {tool_result}"
        final_response = llm.get_response(user_query, context)
    else:
        # If no specific tool is chosen, fall back to MCP chat
        print("No specific tool chosen. Using general_tool for fallback...")
        final_response = await run_memory_chat(user_query)

    return final_response

async def run_memory_chat(user_query):
    """Run a chat using MCPAgent's built-in conversation memory."""
    load_dotenv()
    print("Initializing MCP chat...")

    # Initialize the MCP client and the LLM endpoint
    client = MCPClient.from_config_file("browser_mcp.json")
    llm_endpoint = HuggingFaceEndpoint(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        temperature=0.3,
        max_new_tokens=1024,
    )
    llm = ChatHuggingFace(llm=llm_endpoint)

    # Initialize the MCP agent
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True,
    )

    try:
        # Run the agent with the provided user query
        response = await agent.run(user_query)
        return response

    except Exception as e:
        # Handle any errors during the query processing
        print(f"\nError: {e}")
        return "Sorry, I encountered an error while processing your query."

    finally:
        # Ensure proper cleanup with a check before closing
        if client and client.sessions:
            await client.close_all_sessions()
        else:
            print("No active client sessions to close.")

# Test the system
if __name__ == "__main__":
    print("=== Testing Agentic AI System ===\n")
    test_queries = [
        "What time is it?",
        "Where do I live?",
        "Can you tell me about myself?",
        "give me some hotel names in New York City",
        "Who is Nelson Mandela?"
    ]

    print("=== Testing Basic Version ===")
    for query in test_queries:
        # Use asyncio for MCP fallback chat
        asyncio.run(process_user_query_with_fallback(query))

    print("\n=== Interactive Mode ===")
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break
        asyncio.run(process_user_query_with_fallback(user_input))
