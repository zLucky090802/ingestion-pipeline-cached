[Skip to content](https://developers.llamaindex.ai/python/examples/tools/mcp_toolbox/#_top)
# Using MCP Toolbox with LlamaIndex 
Integrate your databases with LlamaIndex agents using MCP Toolbox.
## Overview
[Section titled “Overview”](https://developers.llamaindex.ai/python/examples/tools/mcp_toolbox/#overview)
[MCP Toolbox for Databases](https://github.com/googleapis/genai-toolbox) is an open source MCP server for databases. It was designed with enterprise-grade and production-quality in mind. It enables you to develop tools easier, faster, and more securely by handling the complexities such as connection pooling, authentication, and more.
Toolbox Tools can be seamlessly integrated with LlamaIndex applications. For more information on [getting started](https://googleapis.github.io/genai-toolbox/getting-started/local_quickstart/) or [configuring](https://googleapis.github.io/genai-toolbox/getting-started/configure/) MCP Toolbox, see the [documentation](https://googleapis.github.io/genai-toolbox/getting-started/introduction/).
## Configure and deploy
[Section titled “Configure and deploy”](https://developers.llamaindex.ai/python/examples/tools/mcp_toolbox/#configure-and-deploy)
Toolbox is an open source server that you deploy and manage yourself. For more instructions on deploying and configuring, see the official Toolbox documentation:


### Install client SDK
[Section titled “Install client SDK”](https://developers.llamaindex.ai/python/examples/tools/mcp_toolbox/#install-client-sdk)
Install the LlamaIndex compatible MCP Toolbox SDK package before getting started:

```


pip install toolbox-llamaindex


```

### Loading Toolbox Tools
[Section titled “Loading Toolbox Tools”](https://developers.llamaindex.ai/python/examples/tools/mcp_toolbox/#loading-toolbox-tools)
Once your Toolbox server is configured and up and running, you can load tools from your server:

```


import asyncio




import os




from llama_index.core.agent.workflow import AgentWorkflow




from llama_index.core.workflow import Context




from llama_index.llms.google_genai import GoogleGenAI




from toolbox_llamaindex import ToolboxClient





prompt ="""




You're a helpful hotel assistant. You handle hotel searching, booking and




cancellations. When the user searches for a hotel, mention it's name, id,




location and price tier. Always mention hotel ids while performing any




searches. This is very important for any operations. For any bookings or




cancellations, please provide the appropriate confirmation. Be sure to




update checkin or checkout dates if mentioned by the user.




Don't ask for confirmations from the user.






queries = [




"Find hotels in Basel with Basel in it's name.",




"Can you book the Hilton Basel for me?",




"Oh wait, this is too expensive. Please cancel it and book the Hyatt Regency instead.",




"My check in dates would be from April 10, 2024 to April 19, 2024.",







asyncdefrun_application():




llm = GoogleGenAI(




api_key=os.getenv("GOOGLE_API_KEY"),




model="gemini-2.0-flash-001",






# llm = GoogleGenAI(




#     model="gemini-2.0-flash-001",




#     vertexai_config={"project": "project-id", "location": "us-central1"},






# Load the tools from the Toolbox server




asyncwith ToolboxClient("http://127.0.0.1:5000") as client:




tools =await client.aload_toolset()





agent = AgentWorkflow.from_tools_or_functions(




tools,




llm=llm,






for tool in tools:




print(tool.metadata)





ctx = Context(agent)





for query in queries:




response =await agent.run(user_msg=query, ctx=ctx)




print()




print(f"---- {query} ----")




print(str(response))






await run_application()


```


```

ToolMetadata(description='Book a hotel by its ID. If the hotel is successfully booked, returns a NULL, raises an error if not.\n\nArgs:\n    hotel_id (str): The ID of the hotel to book.', name='book-hotel', fn_schema=<class 'toolbox_core.utils.book-hotel'>, return_direct=False)


ToolMetadata(description='Cancel a hotel by its ID.\n\nArgs:\n    hotel_id (str): The ID of the hotel to cancel.', name='cancel-hotel', fn_schema=<class 'toolbox_core.utils.cancel-hotel'>, return_direct=False)


ToolMetadata(description='Search for hotels based on location.\n\nArgs:\n    location (str): The location of the hotel.', name='search-hotels-by-location', fn_schema=<class 'toolbox_core.utils.search-hotels-by-location'>, return_direct=False)


ToolMetadata(description='Search for hotels based on name.\n\nArgs:\n    name (str): The name of the hotel.', name='search-hotels-by-name', fn_schema=<class 'toolbox_core.utils.search-hotels-by-name'>, return_direct=False)


ToolMetadata(description="Update a hotel's check-in and check-out dates by its ID. Returns a message indicating  whether the hotel was successfully updated or not.\n\nArgs:\n    hotel_id (str): The ID of the hotel to update.\n    checkin_date (str): The new check-in date of the hotel.\n    checkout_date (str): The new check-out date of the hotel.", name='update-hotel', fn_schema=<class 'toolbox_core.utils.update-hotel'>, return_direct=False)



---- Find hotels in Basel with Basel in it's name. ----


OK. I found three hotels in Basel with Basel in the name: Holiday Inn Basel, Hilton Basel, and Hyatt Regency Basel.




---- Can you book the Hilton Basel for me? ----


OK. I have booked the Hilton Basel for you.




---- Oh wait, this is too expensive. Please cancel it and book the Hyatt Regency instead. ----


OK. I have booked the Hyatt Regency Basel for you.




---- My check in dates would be from April 10, 2024 to April 19, 2024. ----


OK. I have updated your check-in date to April 10, 2024 and your check-out date to April 19, 2024 for the Hyatt Regency Basel.

```

### Advanced Toolbox Features
[Section titled “Advanced Toolbox Features”](https://developers.llamaindex.ai/python/examples/tools/mcp_toolbox/#advanced-toolbox-features)
Toolbox has a variety of features to make developing Gen AI tools for databases. For more information, read more about the following features:
  * [Authenticated Parameters](https://googleapis.github.io/genai-toolbox/resources/tools/#authenticated-parameters): bind tool inputs to values from OIDC tokens automatically, making it easy to run sensitive queries without potentially leaking data
  * [Authorized Invocations](https://googleapis.github.io/genai-toolbox/resources/tools/#authorized-invocations): restrict access to use a tool based on the users Auth token
  * [OpenTelemetry](https://googleapis.github.io/genai-toolbox/how-to/export_telemetry/): get metrics and tracing from Toolbox with OpenTelemetry


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


