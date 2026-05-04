[Skip to content](https://developers.llamaindex.ai/python/framework/getting_started/starter_example_local/#_top)
LlamaIndex Framework
Getting Started
[Starter Tutorial (Using Local LLMs)](https://developers.llamaindex.ai/python/framework/getting_started/starter_example_local/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Starter Tutorial (Using Local LLMs)
This tutorial will show you how to get started building agents with LlamaIndex. We’ll start with a basic example and then show how to add RAG (Retrieval-Augmented Generation) capabilities.
We will use [`BAAI/bge-base-en-v1.5`](https://huggingface.co/BAAI/bge-base-en-v1.5) as our embedding model and `llama3.1 8B` served through `Ollama`.
## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/framework/getting_started/starter_example_local/#setup)
Ollama is a tool to help you get set up with LLMs locally with minimal setup.
Follow the [README](https://github.com/jmorganca/ollama) to learn how to install it.
To download the Llama3 model just do `ollama pull llama3.1`.
**NOTE** : You will need a machine with at least ~32GB of RAM.
As explained in our [installation guide](https://developers.llamaindex.ai/python/framework/getting_started/installation), `llama-index` is actually a collection of packages. To run Ollama and Huggingface, we will need to install those integrations:
Terminal window
```


pipinstallllama-index-llms-ollamallama-index-embeddings-huggingface


```

The package names spell out the imports, which is very helpful for remembering how to import them or install them!

```


from llama_index.llms.ollama import Ollama




from llama_index.embeddings.huggingface import HuggingFaceEmbedding


```

More integrations are all listed on <https://llamahub.ai>.
## Basic Agent Example
[Section titled “Basic Agent Example”](https://developers.llamaindex.ai/python/framework/getting_started/starter_example_local/#basic-agent-example)
Let’s start with a simple example using an agent that can perform basic multiplication by calling a tool. Create a file called `starter.py`:

```


import asyncio




from llama_index.core.agent.workflow import FunctionAgent




from llama_index.llms.ollama import Ollama





# Define a simple calculator tool



defmultiply(a: float, b: float) -> float:




"""Useful for multiplying two numbers."""




return* b





# Create an agent workflow with our calculator tool



agent = FunctionAgent(




tools=[multiply],




llm=Ollama(




model="llama3.1",




request_timeout=360.0,




# Manually set the context window to limit memory usage




context_window=8000,





system_prompt="You are a helpful assistant that can multiply two numbers.",







asyncdefmain():




# Run the agent




response =await agent.run("What is 1234 * 4567?")




print(str(response))





# Run the agent



if__name__=="__main__":




asyncio.run(main())


```

This will output something like: `The answer to 1234 * 4567 is 5635678.`
What happened is:
  * The agent was given a question: `What is 1234 * 4567?`
  * Under the hood, this question, plus the schema of the tools (name, docstring, and arguments) were passed to the LLM
  * The agent selected the `multiply` tool and wrote the arguments to the tool
  * The agent received the result from the tool and interpolated it into the final response


## Adding Chat History
[Section titled “Adding Chat History”](https://developers.llamaindex.ai/python/framework/getting_started/starter_example_local/#adding-chat-history)
The `AgentWorkflow` is also able to remember previous messages. This is contained inside the `Context` of the `AgentWorkflow`.
If the `Context` is passed in, the agent will use it to continue the conversation.

```


from llama_index.core.workflow import Context




# create context



ctx = Context(agent)




# run agent with context



response =await agent.run("My name is Logan", ctx=ctx)




response =await agent.run("What is my name?", ctx=ctx)


```

## Adding RAG Capabilities
[Section titled “Adding RAG Capabilities”](https://developers.llamaindex.ai/python/framework/getting_started/starter_example_local/#adding-rag-capabilities)
Now let’s enhance our agent by adding the ability to search through documents. First, let’s get some example data using our terminal:
Terminal window
```


mkdirdata




wgethttps://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt-Odata/paul_graham_essay.txt


```

Your directory structure should look like this now:

```
├── starter.py └── data    └── paul_graham_essay.txt
```

Now we can create a tool for searching through documents using LlamaIndex. By default, our `VectorStoreIndex` will use a `text-embedding-ada-002` embeddings from OpenAI to embed and retrieve the text.
Our modified `starter.py` should look like this:

```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings




from llama_index.core.agent.workflow import AgentWorkflow




from llama_index.llms.ollama import Ollama




from llama_index.embeddings.huggingface import HuggingFaceEmbedding




import asyncio




import os




# Settings control global defaults



Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")




Settings.llm = Ollama(




model="llama3.1",




request_timeout=360.0,




# Manually set the context window to limit memory usage




context_window=8000,





# Create a RAG tool using LlamaIndex



documents = SimpleDirectoryReader("data").load_data()




index = VectorStoreIndex.from_documents(




documents,




# we can optionally override the embed_model here




# embed_model=Settings.embed_model,





query_engine = index.as_query_engine(




# we can optionally override the llm here




# llm=Settings.llm,







defmultiply(a: float, b: float) -> float:




"""Useful for multiplying two numbers."""




return* b






asyncdefsearch_documents(query: str) -> str:




"""Useful for answering natural language questions about an personal essay written by Paul Graham."""




response =await query_engine.aquery(query)




returnstr(response)





# Create an enhanced workflow with both tools



agent = AgentWorkflow.from_tools_or_functions(




[multiply, search_documents],




llm=Settings.llm,




system_prompt="""You are a helpful assistant that can perform calculations




and search through documents to answer questions.""",






# Now we can ask questions about the documents or do calculations



asyncdefmain():




response =await agent.run(




"What did the author do in college? Also, what's 7 * 8?"





print(response)





# Run the agent



if__name__=="__main__":




asyncio.run(main())


```

The agent can now seamlessly switch between using the calculator and searching through documents to answer questions.
## Storing the RAG Index
[Section titled “Storing the RAG Index”](https://developers.llamaindex.ai/python/framework/getting_started/starter_example_local/#storing-the-rag-index)
To avoid reprocessing documents every time, you can persist the index to disk:

```

# Save the index



index.storage_context.persist("storage")




# Later, load the index



from llama_index.core import StorageContext, load_index_from_storage





storage_context = StorageContext.from_defaults(persist_dir="storage")




index = load_index_from_storage(




storage_context,




# we can optionally override the embed_model here




# it's important to use the same embed_model as the one used to build the index




# embed_model=Settings.embed_model,





query_engine = index.as_query_engine(




# we can optionally override the llm here




# llm=Settings.llm,



```


```


index = VectorStoreIndex.from_vector_store(




vector_store,




# it's important to use the same embed_model as the one used to build the index




# embed_model=Settings.embed_model,



```

## What’s Next?
[Section titled “What’s Next?”](https://developers.llamaindex.ai/python/framework/getting_started/starter_example_local/#whats-next)
This is just the beginning of what you can do with LlamaIndex agents! You can:
  * Add more tools to your agent
  * Use different LLMs
  * Customize the agent’s behavior using system prompts
  * Add streaming capabilities
  * Implement human-in-the-loop workflows
  * Use multiple agents to collaborate on tasks


Some helpful next links:
  * See more advanced agent examples in our [Agent documentation](https://developers.llamaindex.ai/python/framework/understanding/agent)
  * Learn more about [high-level concepts](https://developers.llamaindex.ai/python/framework/getting_started/concepts)
  * Explore how to [customize things](https://developers.llamaindex.ai/python/framework/getting_started/faq)
  * Check out the [component guides](https://developers.llamaindex.ai/python/framework/module_guides)


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


