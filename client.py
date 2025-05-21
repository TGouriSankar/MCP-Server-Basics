# client.py

import asyncio
import os
from dotenv import load_dotenv
from fastmcp import Client
from langchain_community.tools import AsyncTool
from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq

# Load .env (must contain GROQ_API_KEY)
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

async def main():
    # Initialize Groq LLM
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)

    # Connect to your running MCP server over stdio
    async with Client("mcp_leave.py") as mcp_client:

        # Async wrappers around MCP calls
        async def _get_balance(eid: str) -> str:
            resp = await mcp_client.call_tool(
                "get_leave_balance", {"employee_id": eid}
            )
            return resp.result

        async def _apply_leave(eid: str, dates: list[str]) -> str:
            resp = await mcp_client.call_tool(
                "apply_leave",
                {"employee_id": eid, "leave_dates": dates}
            )
            return resp.result

        async def _get_history(eid: str) -> str:
            resp = await mcp_client.call_tool(
                "get_leave_history", {"employee_id": eid}
            )
            return resp.result

        # Wrap them as AsyncTool instances
        tools = [
            AsyncTool(
                name="get_leave_balance",
                func=_get_balance,
                description="Check remaining leave days for an employee ID"
            ),
            AsyncTool(
                name="apply_leave",
                func=_apply_leave,
                description="Apply leave for given dates (list of YYYY-MM-DD)"
            ),
            AsyncTool(
                name="get_leave_history",
                func=_get_history,
                description="Fetch past leave dates for an employee ID"
            ),
        ]

        # Build and run the LangChain agent
        agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
        )

        # Ask something
        answer = await agent.arun("How many leave days does E001 have left?")
        print("Agent:", answer)

if __name__ == "__main__":
    asyncio.run(main())
