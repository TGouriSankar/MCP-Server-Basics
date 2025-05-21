import asyncio
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
import os
from dotenv import load_dotenv; load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

async def main():
    client = MCPClient(config= {"mcpServers":{
    "playwright": {
        "command": "npx",
        "args": ["@playwright/mcp@latest"],
        "env": {"DISPLAY": ":1"}
    }}})
    # Create LLM
    llm = ChatGroq(model="llama-3.1-8b-instant")
    # Create agent with tools
    agent = MCPAgent(llm=llm, client=client)
    # Run the query
    # result = await agent.run("Find the best restaurant in hyderabad")
    # print(result)
    try:
        while True:
            user_input = input("Enter ur Query >> ").strip()
            if user_input.lower() in ["exit","quit"]:
                print("Thanks you...")
                break
            if user_input.lower() in ["cls","clear"]:
                print("Clearing the memory")
                agent.clear_conversation_history()
                continue
            result = await agent.run(user_input)
            print(result)
    finally:
        print("checking")


if __name__ == "__main__":
    asyncio.run(main())