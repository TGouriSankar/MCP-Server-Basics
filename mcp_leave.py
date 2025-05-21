from fastmcp import FastMCP
from typing import List
from dotenv import load_dotenv
import os

# Load environment variables (e.g., GROQ_API_KEY)
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')  # required by ChatGroq :contentReference[oaicite:1]{index=1}

# In-memory mock database
employee_leaves = {
    "E001": {"balance": 18, "history": ["2024-12-25", "2025-01-01"]},
    "E002": {"balance": 20, "history": []}
}

# Create FastMCP instance
mcp = FastMCP(name="LeaveManager")  # core object :contentReference[oaicite:2]{index=2}

# Tool: Check leave balance
@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    data = employee_leaves.get(employee_id)
    if data:
        return f"{employee_id} has {data['balance']} leave days remaining."
    return "Employee ID not found."

# Tool: Apply for leave
@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    if employee_id not in employee_leaves:
        return "Employee ID not found."
    days = len(leave_dates)
    if employee_leaves[employee_id]["balance"] < days:
        return f"Insufficient balance: requested {days}, available {employee_leaves[employee_id]['balance']}."
    employee_leaves[employee_id]["balance"] -= days
    employee_leaves[employee_id]["history"].extend(leave_dates)
    return f"Leave applied for {days} day(s). New balance: {employee_leaves[employee_id]['balance']}."

# Tool: Get leave history
@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    data = employee_leaves.get(employee_id)
    if data:
        h = ', '.join(data['history']) if data['history'] else "No leaves taken."
        return f"Leave history for {employee_id}: {h}"
    return "Employee ID not found."

# Resource: Personalized greeting
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello, {name}! How can I assist you with leave management today?"

if __name__ == "__main__":
    # Run with default stdio transport; for SSE/web: mcp.run(transport="sse", host="0.0.0.0", port=8000)
    mcp.run()  # no llm arg :contentReference[oaicite:3]{index=3}


# from mcp.server.fastmcp import FastMCP
# from typing import List
# from langchain_groq import ChatGroq
# from dotenv import load_dotenv; load_dotenv()
# import os

# # In-memory mock database with 20 leave days to start
# employee_leaves = {
#     "E001": {"balance": 18, "history": ["2024-12-25", "2025-01-01"]},
#     "E002": {"balance": 20, "history": []}
# }

# os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

# # Create MCP server
# mcp = FastMCP("LeaveManager")

# #create llm chart
# llm = ChatGroq(model="llama-3.1-8b-instant")

# # Tool: Check Leave Balance
# @mcp.tool()
# def get_leave_balance(employee_id: str) -> str:
#     """Check how many leave days are left for the employee"""
#     data = employee_leaves.get(employee_id)
#     if data:
#         return f"{employee_id} has {data['balance']} leave days remaining."
#     return "Employee ID not found."

# # Tool: Apply for Leave with specific dates
# @mcp.tool()
# def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
#     """
#     Apply leave for specific dates (e.g., ["2025-04-17", "2025-05-01"])
#     """
#     if employee_id not in employee_leaves:
#         return "Employee ID not found."

#     requested_days = len(leave_dates)
#     available_balance = employee_leaves[employee_id]["balance"]

#     if available_balance < requested_days:
#         return f"Insufficient leave balance. You requested {requested_days} day(s) but have only {available_balance}."

#     # Deduct balance and add to history
#     employee_leaves[employee_id]["balance"] -= requested_days
#     employee_leaves[employee_id]["history"].extend(leave_dates)

#     return f"Leave applied for {requested_days} day(s). Remaining balance: {employee_leaves[employee_id]['balance']}."


# # Resource: Leave history
# @mcp.tool()
# def get_leave_history(employee_id: str) -> str:
#     """Get leave history for the employee"""
#     data = employee_leaves.get(employee_id)
#     if data:
#         history = ', '.join(data['history']) if data['history'] else "No leaves taken."
#         return f"Leave history for {employee_id}: {history}"
#     return "Employee ID not found."

# # Resource: Greeting
# @mcp.resource("greeting://{name}")
# def get_greeting(name: str) -> str:
#     """Get a personalized greeting"""
#     return f"Hello, {name}! How can I assist you with leave management today?"

# if __name__ == "__main__":
#     mcp.run()