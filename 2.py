from dotenv import load_dotenv
import asyncio


from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import (
    ReActAgent,
    AgentStream,
    ToolCallResult,
    FunctionAgent,
)
from llama_index.core.workflow import Context
import subprocess

load_dotenv()


# LlamaIndex settings
Settings.llm = OpenAI(model="gpt-4o-mini")


# define the tools
def multiply(a: int, b: int) -> int:
    """Multiplies two integers and returns the result integer"""
    return a * b


def add(a: int, b: int) -> int:
    """Adds two integers and returns the result integer"""
    return a + b


def open_screenshot() -> str:
    """Opens the screeshot application on my computer to capture a screen screenshot"""
    try:
        subprocess.run(["open", "-a", "Screenshot"], check=True)
        return "Screenshot application opened successfully."
    except subprocess.CalledProcessError as e:
        return f"An error occurred while trying to open the screenshot application: {e}"


async def main():

    llm = Settings.llm

    # define the ReactAgent
    # agent = ReActAgent(llm=llm, tools=[multiply, add, open_screenshot])
    agent = FunctionAgent(
        llm=llm, tools=[multiply, add, open_screenshot], allow_parallel_tool_calls=True
    )

    # create a context for the agent
    context = Context(agent)

    # Run the agent with a sample query (asynchronous execution can be implemented as needed)
    handler = agent.run(
        "What is the sum of 5 and 10, and then multiply the result by 2? Also, open the screenshot application on my Mac.",
        ctx=context,
    )

    # stream the response
    async for ev in handler.stream_events():
        if isinstance(ev, ToolCallResult):
            print(f"Tool Call Result: {ev.tool_name} returned {ev.tool_output}")
        if isinstance(ev, AgentStream):
            print(ev.delta, end="", flush=True)

    # Get final response
    final_response = await handler
    print("Agent Response:", final_response)


if __name__ == "__main__":
    asyncio.run(main())
