import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import get_tools

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def get_chat_model(temperature=1):
    """
    Initialize and return a simple chat model without agent functionality.
    """
    return ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=temperature,
        groq_api_key=GROQ_API_KEY
    )

def get_llm(temperature=1):
    """
    Initialize and return the LLM model.
    """
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=temperature,
        groq_api_key=GROQ_API_KEY
    )
    
    # Get tools
    tools = get_tools()
    
    # Create prompt template for ReAct agent
    template = """You are a helpful AI assistant with access to tools. Use them when needed to provide accurate and up-to-date information.
When asked about current events or real-time information, always use the web_search tool to ensure accuracy.

Tools available:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Previous conversation history:
{chat_history}

Begin!

Question: {input}
{agent_scratchpad}"""

    prompt = ChatPromptTemplate.from_template(template)
    
    # Create ReAct agent
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    # Create agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent_executor 