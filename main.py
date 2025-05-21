from mcp.server.fastmcp import FastMCP
from typing import List
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# In-memory mock database
employee_leaves = {
    "E001": {"balance": 18, "history": ["2024-12-25", "2025-01-01"]},
    "E002": {"balance": 20, "history": []},
    "E003": {"balance": 15, "history": ["2025-02-14"]}
}

# Initialize Groq LLM
llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0.7,
    groq_api_key=os.getenv('GROQ_API_KEY')
)

# Create MCP server
mcp = FastMCP("LeaveManagementChatbot")

def welcome_message():
    """Provides a welcome message for the chatbot"""
    return (
        "Welcome to the Leave Management Chatbot!\n"
        "I can help you with:\n"
        "- Checking your leave balance (provide your employee ID)\n"
        "- Applying for leave (provide dates)\n"
        "- Viewing your leave history\n\n"
        "How may I assist you today?"
    )

# Tool: Check Leave Balance
@mcp.tool()
def check_balance(employee_id: str) -> str:
    """Check remaining leave days for an employee"""
    if employee_id not in employee_leaves:
        return "Employee ID not found. Please check your ID and try again."
    return f"Employee {employee_id} has {employee_leaves[employee_id]['balance']} days remaining."

# Tool: Apply for Leave
@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    """
    Apply for leave on specific dates (format: YYYY-MM-DD)
    Example: ["2025-06-15", "2025-06-16"]
    """
    if employee_id not in employee_leaves:
        return "Employee ID not found."
    
    balance = employee_leaves[employee_id]["balance"]
    requested_days = len(leave_dates)
    
    if requested_days > balance:
        return (
            f"Sorry, you only have {balance} days left but requested {requested_days}.\n"
            "Please adjust your request or contact HR."
        )
    
    # Update records
    employee_leaves[employee_id]["balance"] -= requested_days
    employee_leaves[employee_id]["history"].extend(leave_dates)
    
    return (
        f"Leave approved for {requested_days} day(s): {', '.join(leave_dates)}\n"
        f"Your new balance: {employee_leaves[employee_id]['balance']} days"
    )

# Tool: View Leave History
@mcp.tool()
def view_history(employee_id: str) -> str:
    """View an employee's leave history"""
    if employee_id not in employee_leaves:
        return "Employee ID not found."
    
    history = employee_leaves[employee_id]["history"]
    if not history:
        return f"No leave history found for employee {employee_id}."
    
    return (
        f"Leave history for {employee_id}:\n"
        + "\n".join(f"- {date}" for date in history)
        + f"\n\nRemaining balance: {employee_leaves[employee_id]['balance']} days"
    )

def handle_command(command: str) -> str:
    """Handle user commands and route to appropriate functions"""
    command = command.lower().strip()
    
    if command.startswith("check balance"):
        employee_id = command.split()[-1]
        return check_balance(employee_id)
    elif command.startswith("apply leave"):
        parts = command.split()
        employee_id = parts[2]
        dates = parts[3:]
        return apply_leave(employee_id, dates)
    elif command.startswith("view history"):
        employee_id = command.split()[-1]
        return view_history(employee_id)
    elif command in ["help", "menu"]:
        return welcome_message()
    else:
        return "I didn't understand that. Type 'help' to see available commands."

def run_chatbot():
    print("Leave Management Chatbot initialized. Type 'exit' to quit.\n")
    print(welcome_message())
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
            
        if not user_input:
            continue
            
        # Process the input
        response = handle_command(user_input)
        print("\nBot:", response)

if __name__ == "__main__":
    run_chatbot()


# import asyncio
# import os
# from dotenv import load_dotenv
# from client import ChatGroq
# from mcp_use import MCPAgent, MCPClient

# async def main():
#     # Load environment variables
#     load_dotenv()
#     os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

#     # Create configuration dictionary
#     config = "browser_mcp.json"

#     # Create MCPClient from configuration dictionary
#     client = MCPClient.from_config_file(config)

#     # Create LLM
#     llm = ChatGroq(model="llama-3.1-8b-instant")

#     # Create agent with the client
#     agent = MCPAgent(llm=llm, client=client, max_steps=30,memory_enabled=True)

#     try:
#         while True:
#             user_input = input("Enter a query: ")
#             if user_input.lower() in ["exit", "quit"]:
#                 print("Exiting...")
#                 break
#             if user_input.lower() in ["clear","cls"]:
#                 agent.clear_conversation_history()
#                 print("Memory cleared.")
#                 continue
#             try:
#                 result = await agent.run(user_input)
#                 print(f"\nResult: {result}")
#             except Exception as e:
#                 print(f"\nError: {e}")
#     finally:
#        if client and client.sessions:
#           await client.close_all_sessions()


# if __name__ == "__main__":
#     asyncio.run(main())

