from dotenv import load_dotenv
import asyncio
import os

from llama_index.core import Settings
from llama_index.llms.groq import Groq
from llama_index.core.agent.workflow import (
    ReActAgent,
    AgentStream,
    ToolCallResult,
    FunctionAgent,
)
from llama_index.core.workflow import Context
import subprocess

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')
llm = Groq(
    model='llama-3.1-8b-instant',
    api_key=api_key
)

Settings.llm = llm



def multiply(a:int, b:int) -> int:
    """Multiplies two integers."""
    return a * b

def add(a:int, b:int) -> int:
    """Adds to integers"""
    return a + b
    
def open_screenshot() -> str:
    """Opens a screenshot aplication on my computer to capture a screen shot """
    try:
        subprocess.run(['cmd','/c', 'start', 'ms-screenclip:'], check=True)
        return 'Screenshot application opened successfully'
    except subprocess.CalledProcessError as e:
        return f'An error ocurred while trying to open the screanshot application: {e}'

async def main():
    
    llm = Settings.llm
   
    # define tools
    
    #define the ReactAgent
    
    # agent = ReActAgent(
    #     llm=llm,
    #     tools=[multiply, add, open_screenshot]
    # )
    
    agent = FunctionAgent(
        llm=llm,
        tools=[multiply, add, open_screenshot],
        allow_parallel_tool_calls=True,
    )
    
    # create context for agent
    context = Context(agent)
    
    # run agent
    handler =  agent.run(
        'What is the sum of 5 and 10, and then multiply the result by 2?, also open the screenshot aplication on my pc',
        ctx = context,
    )
    
    #stream the response
    async for ev in handler.stream_events():
        if isinstance(ev, ToolCallResult):
            print(f'tool call result: {ev.tool_name} returned {ev.tool_output}')
        if isinstance(ev, AgentStream):
            print(ev.delta, end='', flush= True)
    
    #get final response 
    print('Agent response: ', handler)
 
 
   
if __name__ == "__main__":
    asyncio.run(main())
