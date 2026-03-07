# importing necessary functionality
import os
import random
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI

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
            status =  datadict[key]
            return status
    return ("Order not found.")

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
prompt = hub.pull("hwchase17/structured-chat-agent")

# Initializing memory
memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True)

# Initializing LLM
llm = ChatGoogleGenerativeAI(
    model = "gemini-3-flash-preview",
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