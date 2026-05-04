[Skip to content](https://developers.llamaindex.ai/python/examples/agent/openai_agent_with_query_engine/#_top)
# Agent with Query Engine Tools 
## Build Query Engine Tools
[Section titled “Build Query Engine Tools”](https://developers.llamaindex.ai/python/examples/agent/openai_agent_with_query_engine/#build-query-engine-tools)
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index


```


```


import os





os.environ["OPENAI_API_KEY"] ="sk-..."


```


```


from llama_index.llms.openai import OpenAI




from llama_index.embeddings.openai import OpenAIEmbedding




from llama_index.core import Settings





Settings.llm = OpenAI(model="gpt-4o-mini")




Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")


```


```


from llama_index.core import StorageContext, load_index_from_storage





try:




storage_context = StorageContext.from_defaults(




persist_dir="./storage/lyft"





lyft_index = load_index_from_storage(storage_context)





storage_context = StorageContext.from_defaults(




persist_dir="./storage/uber"





uber_index = load_index_from_storage(storage_context)





index_loaded =True




except:




index_loaded =False


```

Download Data

```


!mkdir -p 'data/10k/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/10k/uber_2021.pdf'-O 'data/10k/uber_2021.pdf'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/10k/lyft_2021.pdf'-O 'data/10k/lyft_2021.pdf'


```


```


from llama_index.core import SimpleDirectoryReader, VectorStoreIndex





ifnot index_loaded:




# load data




lyft_docs = SimpleDirectoryReader(




input_files=["./data/10k/lyft_2021.pdf"]




).load_data()




uber_docs = SimpleDirectoryReader(




input_files=["./data/10k/uber_2021.pdf"]




).load_data()





# build index




lyft_index = VectorStoreIndex.from_documents(lyft_docs)




uber_index = VectorStoreIndex.from_documents(uber_docs)





# persist index




lyft_index.storage_context.persist(persist_dir="./storage/lyft")




uber_index.storage_context.persist(persist_dir="./storage/uber")


```


```


lyft_engine = lyft_index.as_query_engine(similarity_top_k=3)




uber_engine = uber_index.as_query_engine(similarity_top_k=3)


```


```


from llama_index.core.tools import QueryEngineTool





query_engine_tools = [




QueryEngineTool.from_defaults(




query_engine=lyft_engine,




name="lyft_10k",




description=(




"Provides information about Lyft financials for year 2021. "




"Use a detailed plain text question as input to the tool."






QueryEngineTool.from_defaults(




query_engine=uber_engine,




name="uber_10k",




description=(




"Provides information about Uber financials for year 2021. "




"Use a detailed plain text question as input to the tool."





```

## Setup Agent
[Section titled “Setup Agent”](https://developers.llamaindex.ai/python/examples/agent/openai_agent_with_query_engine/#setup-agent)
For LLMs like OpenAI that have a function calling API, we should use the `FunctionAgent`.
For other LLMs, we can use the `ReActAgent`.

```


from llama_index.core.agent.workflow import FunctionAgent, ReActAgent




from llama_index.core.workflow import Context





agent = FunctionAgent(tools=query_engine_tools, llm=OpenAI(model="gpt-4o"))




# context to hold the session/state



ctx = Context(agent)


```

## Let’s Try It Out!
[Section titled “Let’s Try It Out!”](https://developers.llamaindex.ai/python/examples/agent/openai_agent_with_query_engine/#lets-try-it-out)

```


from llama_index.core.agent.workflow import ToolCallResult, AgentStream





handler = agent.run("What's the revenue for Lyft in 2021 vs Uber?", ctx=ctx)





asyncfor ev in handler.stream_events():




ifisinstance(ev, ToolCallResult):




print(




f"Call {ev.tool_name} with args {ev.tool_kwargs}\nReturned: {ev.tool_output}"





elifisinstance(ev, AgentStream):




print(ev.delta, end="", flush=True)





response =await handler


```


```

Call lyft_10k with args {'input': "What was Lyft's revenue for the year 2021?"}


Returned: Lyft's revenue for the year 2021 was $3,208,323,000.


Call uber_10k with args {'input': "What was Uber's revenue for the year 2021?"}


Returned: Uber's revenue for the year 2021 was $17.455 billion.


In 2021, Lyft's revenue was approximately $3.21 billion, while Uber's revenue was significantly higher at $17.455 billion.

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


