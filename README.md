# Agentic AI System

This project implements an intelligent conversational agent capable of processing user queries through multiple tools and fallback to a memory-based chat system. It integrates with an LLM (Large Language Model) and uses various tools for specific tasks like fetching current time, personal details, and even searching for hotels. If no specific tool is applicable, the system falls back to general conversation using memory.

## Features

- **Multi-tool Support**: The agent selects an appropriate tool based on the user query. Tools include `get_current_time`, `get_my_address`, `find_hotels`, and others.
- **Fallback to MCP Chat**: If no specific tool is found, the agent switches to an interactive chat powered by memory for general queries.
- **Memory-based Conversations**: Utilizes `MCPAgent` to maintain the context of conversations.
- **Integration with HuggingFace Models**: The system integrates with HuggingFace models for sophisticated natural language understanding.

## Technologies Used

- **Python**: The core language used to build the system.
- **LangChain**: A framework for building language-based applications, used for integrating large language models (LLMs).
- **HuggingFace API**: Provides access to powerful pre-trained models like `zephyr-7b-beta`.
- **MCPAgent**: A memory-based conversational agent.
- **dotenv**: Manages environment variables for API key management and configuration.
- **asyncio**: Used for asynchronous operations to handle multiple queries concurrently.

## Prerequisites

To run this project locally, you need the following:

- Python 3.7 or later
- Environment setup for HuggingFace (token and model repo access)
