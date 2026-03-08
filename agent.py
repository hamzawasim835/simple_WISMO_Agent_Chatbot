# importing necessary functionality
import os
import random
from dotenv import load_dotenv
from langchain_community import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from pathlib import Path

# Generic pathing logic
base_path = Path(__file__).parent 
data_file = base_path / "order_record.txt"

# Loading API key through .env file
load_dotenv()

# Tools go here
# Order Tracking
def get_order_status(orderID):
    # Loading data from .txt file into a dictionary
    datadict = {}
    with open(data_file, "r") as f:
        for line in f:
            (key, val) = line.split(",")
            datadict[key] = val

    # Searching the dictionary
    if (orderID.strip().upper() in datadict):
        status =  datadict[key]
        return status
    return ("Order not found.")

# Return Processing
class ReturnInput(BaseModel):
    order_id: str = Field(description="The ORDXXXXXX ID from the user")
    reason: str = Field(description="The user's reason for returning the item")
def process_returns(order_id: str, reason: str = "None Given"):
    datadict = {}
    path = data_file
    
    try:
        with open(path, "r") as f:
            for line in f:
                if "," in line:
                    key, val = line.strip().split(",")
                    datadict[key.strip().upper()] = val
    except FileNotFoundError:
        return "Error: Database file not found."

    clean_id = order_id.strip().upper()
    
    if clean_id in datadict:
        # Generate random 6-digit code correctly
        ret_suffix = "".join([str(random.randint(0, 9)) for _ in range(6)])
        return f"Return approved. Return ID: RET{ret_suffix}. Reason logged: {reason}"
    
    return f"Order {order_id} not found in our records."

tools = [
    Tool(
        name="get_order_status",  
        func=get_order_status,  
        description="checks dictionary and returns current order status",
    ),
    StructuredTool.from_function(
        func=process_returns,
        name="process_returns",
        description="Used to approve a return. Requires a valid Order ID and a Reason. If user" \
        "doesn't provide a reason, keep asking them for one until they give one",
        args_schema=ReturnInput # This is the magic ingredient
    )
]

# Pulling prompt template from hub
prompt = hub.pull("hwchase17/structured-chat-agent")

# Initializing memory
memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True)

# Initializing LLM
llm = ChatGoogleGenerativeAI(
    model = "gemini-3.1-flash-lite-preview",
    temperature=0
)

# Creating the ReAct agent using the create_react_agent function
agent = create_structured_chat_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

# Creating an agent executor from the agent and tools
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=False,
    memory=memory,
    handle_parsing_errors=True,
)


while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break

    # Add the user's message to the conversation memory
    memory.chat_memory.add_message(HumanMessage(content=user_input))

    # Invoke the agent with the user input and the current chat history
    response = agent_executor.invoke({"input": user_input})
    print("Bot:", response["output"])

    # Add the agent's response to the conversation memory
    memory.chat_memory.add_message(AIMessage(content=response["output"]))