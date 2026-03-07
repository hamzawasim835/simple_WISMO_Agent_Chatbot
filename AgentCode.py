# importing necessary functionality
import os
import random
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import (
    AgentExecutor,
    create_react_agent,
)
from langchain_core.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# Loading API key through .env file
load_dotenv()

# Tools go here
def get_order_status(orderID):
    # Loading data from .txt file into a dictionary
    datadict = {}
    with open("E:\Workshop\ECED\Inonest\AI\Single_Agent_WISMO\order_record.txt") as f:
        for line in f:
            (key, val) = line.split(",")
            datadict[key] = val

    # Searching the dictionary
    for key in datadict:
        if (key == orderID.strip().upper()):
            print(datadict[key])
            return True
    print("Order not found.")
    return False

def process_returns(orderID, Reason):
    # Loading data into dict
    datadict = {}
    with open("E:\Workshop\ECED\Inonest\AI\Single_Agent_WISMO\order_record.txt") as f:
        for line in f:
            (key, val) = line.split(",")
            datadict[key] = val
    
    # Locating target, processing return
    for key in datadict:
        if (key == orderID.strip().upper()):
            print("Return request apporved :) ")
            
            # Creating and printing return number
            n = 6
            li = random.sample(range(0, 9), n)
            retcode = "RET"
            for i in li:
                retcode += i
            
            return retcode, Reason

tools = [
    Tool(
        name="get_order_status",  
        func=get_order_status,  
        description="checks dictionary and returns current order status",
    ),
    Tool(
        name="process_returns",  
        func=process_returns,  
        description="useful for processing returns. Checks dictionary to see" \
        "if order is there, then approves refund and returns a return id",
    ),
]

# Pulling prompt template from hub
prompt = hub.pull("hwchase17/react")

# Initializing LLM
llm = ChatGoogleGenerativeAI(
    model = "gemini-3.1-flash-lite-preview",
    temperature=0
)

# Creating the ReAct agent using the create_react_agent function
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
    stop_sequence=True,
)

# Creating an agent executor from the agent and tools
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=False,
)

# Looping logic chat logic goes here
while True:
    query = input("You: ")
    if query.lower() == "exit":
        break

    result = agent_executor.invoke({"input": query})
    #response = result.content

    print(f"AI: {result}")