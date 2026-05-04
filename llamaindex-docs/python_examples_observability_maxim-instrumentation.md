[Skip to content](https://developers.llamaindex.ai/python/examples/observability/maxim-instrumentation/#_top)
# Cookbook LlamaIndex Integration by Maxim AI (Instrumentation Module) 
This is a simple cookbook that demonstrates how to use the [LlamaIndex Maxim integration](https://www.getmaxim.ai/docs/sdk/python/integrations/llamaindex/llamaindex) using the [instrumentation module](https://docs.llamaindex.ai/en/stable/module_guides/observability/instrumentation/) by LlamaIndex (available in llama-index v0.10.20 and later).

```

# Install required packages



# pip install llama-index


# pip install llama-index-llms-openai


# pip install llama-index-embeddings-openai


# pip install llama-index-tools-wikipedia


# pip install llama-index-tools-requests


# pip install maxim-py


# pip install python-dotenv

```


```


import os




from dotenv import load_dotenv




# Load environment variables from .env file


load_dotenv()



# Get environment variables



MAXIM_API_KEY= os.getenv("MAXIM_API_KEY")




MAXIM_LOG_REPO_ID= os.getenv("MAXIM_LOG_REPO_ID")




OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")




# Verify required environment variables are set



ifnotMAXIM_API_KEY:




raiseValueError("MAXIM_API_KEY environment variable is required")




ifnotMAXIM_LOG_REPO_ID:




raiseValueError("MAXIM_LOG_REPO_ID environment variable is required")




ifnotOPENAI_API_KEY:




raiseValueError("OPENAI_API_KEY environment variable is required")





print("✅ Environment variables loaded successfully")




print(




f"MAXIM_API_KEY: {'*'* (len(MAXIM_API_KEY) -4) +MAXIM_API_KEY[-4:] ifMAXIM_API_KEYelse'Not set'}"





print(f"MAXIM_LOG_REPO_ID: {MAXIM_LOG_REPO_ID}")




print(




f"OPENAI_API_KEY: {'*'* (len(OPENAI_API_KEY) -4) +OPENAI_API_KEY[-4:] ifOPENAI_API_KEYelse'Not set'}"



```

## Maxim Configuration
[Section titled “Maxim Configuration”](https://developers.llamaindex.ai/python/examples/observability/maxim-instrumentation/#maxim-configuration)

```


import asyncio




from maxim import Config, Maxim




from maxim.logger import LoggerConfig




from maxim.logger.llamaindex import instrument_llamaindex




# Initialize Maxim logger



maxim = Maxim(Config(api_key=os.getenv("MAXIM_API_KEY")))




logger = maxim.logger(LoggerConfig(id=os.getenv("MAXIM_LOG_REPO_ID")))




# Instrument LlamaIndex with Maxim observability


# Set debug=True to see detailed logs during development


instrument_llamaindex(logger)




print("✅ Maxim instrumentation enabled for LlamaIndex")


```

## Simple FunctionAgent with Observability
[Section titled “Simple FunctionAgent with Observability”](https://developers.llamaindex.ai/python/examples/observability/maxim-instrumentation/#simple-functionagent-with-observability)

```


from llama_index.core.agent import FunctionAgent




from llama_index.core.tools import FunctionTool




from llama_index.llms.openai import OpenAI





# Define simple calculator tools



defadd_numbers(a: float, b: float) -> float:




"""Add two numbers together."""




return+ b






defmultiply_numbers(a: float, b: float) -> float:




"""Multiply two numbers together."""




return* b






defdivide_numbers(a: float, b: float) -> float:




"""Divide first number by second number."""




if==0:




raiseValueError("Cannot divide by zero")




return/ b





# Create function tools



add_tool = FunctionTool.from_defaults(fn=add_numbers)




multiply_tool = FunctionTool.from_defaults(fn=multiply_numbers)




divide_tool = FunctionTool.from_defaults(fn=divide_numbers)




# Initialize LLM



llm = OpenAI(model="gpt-4o-mini", temperature=0)




# Create FunctionAgent



agent = FunctionAgent(




tools=[add_tool, multiply_tool, divide_tool],




llm=llm,




verbose=True,




system_prompt="""You are a helpful calculator assistant.




Use the provided tools to perform mathematical calculations.




Always explain your reasoning step by step.""",





# Test the agent with a complex calculation



import asyncio






asyncdeftest_function_agent():




print("🔍 Testing FunctionAgent with Maxim observability...")





query ="What is (15 + 25) multiplied by 2, then divided by 8?"





print(f"\n📝 Query: {query}")





# This will be automatically logged by Maxim instrumentation




# FunctionAgent.run() is async, so we need to await it




response =await agent.run(query)





print(f"\n🤖 Response: {response}")




print("\n✅ Check your Maxim dashboard for detailed trace information!")





# Run the async function



await test_function_agent()


```

## Multi Modal Requests
[Section titled “Multi Modal Requests”](https://developers.llamaindex.ai/python/examples/observability/maxim-instrumentation/#multi-modal-requests)

```


from llama_index.core.agent.workflow import FunctionAgent




from llama_index.core.llms import ChatMessage, ImageBlock, TextBlock




from llama_index.llms.openai import OpenAI




import requests




fromPILimport Image




import io




import base64





# Tool for image analysis



defdescribe_image_content(description: str) -> str:




"""Analyze and describe what's in an image based on the model's vision."""




returnf"Image analysis complete: {description}"





# Math tools for the agent



defadd(a: int, b: int) -> int:




"""Add two numbers together."""




return+ b






defmultiply(a: int, b: int) -> int:




"""Multiply two numbers together."""




return* b





# Create multi-modal agent with vision-capable model



multimodal_llm = OpenAI(model="gpt-4o-mini"# Vision-capable model





multimodal_agent = FunctionAgent(




tools=[add, multiply, describe_image_content],




llm=multimodal_llm,




system_prompt="You are a helpful assistant that can analyze images and perform calculations.",







asyncdeftest_multimodal_agent():




print("🔍 Testing Multi-Modal Agent with Maxim observability...")





# Create a simple test image (you can replace this with an actual image path)




# For demo purposes, we'll create a simple mathematical equation image





# You can replace this with a real image path if available




# For now, we'll use text-based interaction




# text_query = "Calculate 15 + 25 and then multiply the result by 3"





# response = await multimodal_agent.run(text_query)




# print(f"\n🤖 Text Response: {response}")





# If you have an image, you can use this pattern:




msg = ChatMessage(




role="user",




blocks=[




TextBlock(




text="What do you see in this image? If there are numbers, perform calculations."





ImageBlock(




url="https://www.shutterstock.com/image-photo/simple-mathematical-equation-260nw-350386472.jpg"




),  # Replace with actual image path






response =await multimodal_agent.run(msg)





exceptExceptionas e:




print(




f"Note: Multi-modal features require actual image files. Error: {e}"





print(




"The agent structure is set up correctly for when you have images to process!"






print("\n✅ Check Maxim dashboard for multi-modal agent traces!")





# Run the test



await test_multimodal_agent()


```

## Multiple Agents
[Section titled “Multiple Agents”](https://developers.llamaindex.ai/python/examples/observability/maxim-instrumentation/#multiple-agents)

```


from llama_index.core.agent.workflow import AgentWorkflow, FunctionAgent




from llama_index.llms.openai import OpenAI




from llama_index.core.tools import FunctionTool  # Import FunctionTool





# Research agent tools



defresearch_topic(topic: str) -> str:




"""Research a given topic and return key findings."""




# Mock research results - in production, this would call real APIs




research_data = {




"climate change": "Climate change refers to long-term shifts in global temperatures and weather patterns, primarily caused by human activities since the 1800s.",




"renewable energy": "Renewable energy comes from sources that are naturally replenishing like solar, wind, hydro, and geothermal power.",




"artificial intelligence": "AI involves creating computer systems that can perform tasks typically requiring human intelligence.",




"sustainability": "Sustainability involves meeting present needs without compromising the ability of future generations to meet their needs.",






topic_lower = topic.lower()




for key, info in research_data.items():




if key in topic_lower:




returnf"Research findings on {topic}: {info} Additional context includes recent developments and policy implications."





returnf"Research completed on {topic}. This is an emerging area requiring further investigation and analysis."





# Analysis agent tools



defanalyze_data(research_data: str) -> str:




"""Analyze research data and provide insights."""




if"climate change"in research_data.lower():




return"Analysis indicates climate change requires immediate action through carbon reduction, renewable energy adoption, and international cooperation."




elif"renewable energy"in research_data.lower():




return"Analysis shows renewable energy is becoming cost-competitive with fossil fuels and offers long-term economic and environmental benefits."




elif"artificial intelligence"in research_data.lower():




return"Analysis reveals AI has transformative potential across industries but requires careful consideration of ethical implications and regulation."




else:




return"Analysis suggests this topic has significant implications requiring strategic planning and stakeholder engagement."





# Report writing agent tools



defwrite_report(analysis: str, topic: str) -> str:




"""Write a comprehensive report based on analysis."""




returnf"""



═══════════════════════════════════════



COMPREHENSIVE RESEARCH REPORT: {topic.upper()}



═══════════════════════════════════════



EXECUTIVE SUMMARY:



{analysis}




KEY FINDINGS:


- Evidence-based analysis indicates significant implications


- Multiple stakeholder perspectives must be considered


- Implementation requires coordinated approach


- Long-term monitoring and evaluation necessary



RECOMMENDATIONS:


1. Develop comprehensive strategy framework


2. Engage key stakeholders early in process


3. Establish clear metrics and milestones


4. Create feedback mechanisms for continuous improvement


5. Allocate appropriate resources and timeline



NEXT STEPS:


- Schedule stakeholder consultations


- Develop detailed implementation plan


- Establish monitoring and evaluation framework


- Begin pilot program if applicable



This report provides a foundation for informed decision-decision making and strategic planning.





# Initialize LLM



llm = OpenAI(model="gpt-4o-mini", temperature=0)




# Create individual agents using the modern API



research_agent = FunctionAgent(




name="research_agent",




description="This agent researches a given topic and returns key findings.",




tools=[FunctionTool.from_defaults(fn=research_topic)],




llm=llm,




system_prompt="You are a research specialist. Use the research tool to gather comprehensive information on requested topics.",






analysis_agent = FunctionAgent(




name="analysis_agent",




description="This agent analyzes research data and provides actionable insights.",




tools=[FunctionTool.from_defaults(fn=analyze_data)],




llm=llm,




system_prompt="You are a data analyst. Analyze research findings and provide actionable insights.",






report_agent = FunctionAgent(




name="report_agent",




description="This agent creates comprehensive, well-structured reports based on analysis.",




tools=[FunctionTool.from_defaults(fn=write_report)],




llm=llm,




system_prompt="You are a report writer. Create comprehensive, well-structured reports based on analysis.",





# Create AgentWorkflow



multi_agent_workflow = AgentWorkflow(




agents=[research_agent, analysis_agent, report_agent],




root_agent="research_agent",







asyncdeftest_agent_workflow():




print("🔍 Testing AgentWorkflow with Maxim observability...")





query ="""I need a comprehensive report on renewable energy.




Please research the current state of renewable energy,




analyze the key findings, and create a structured report




with recommendations for implementation."""





print(f"\n📝 Query: {query}")




print("🔄 This will coordinate multiple agents...")





# This will create a complex trace showing:




# - Multi-agent coordination




# - Agent handoffs and communication




# - Sequential tool execution




# - Individual agent performances




response =await multi_agent_workflow.run(query)





print(f"\n🤖 Multi-Agent Response:\n{response}")




print(




"\n✅ Check Maxim dashboard for comprehensive multi-agent workflow traces!"






# Run the async function



await test_agent_workflow()


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


