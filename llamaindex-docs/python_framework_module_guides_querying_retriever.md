[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/#_top)
LlamaIndex Framework
Component Guides
Querying
Retriever
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Retriever
## Concept
[Section titled “Concept”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/#concept)
Retrievers are responsible for fetching the most relevant context given a user query (or chat message).
It can be built on top of [indexes](https://developers.llamaindex.ai/python/framework/module_guides/indexing), but can also be defined independently. It is used as a key building block in [query engines](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine) (and [Chat Engines](https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines)) for retrieving relevant context.
## Usage Pattern
[Section titled “Usage Pattern”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/#usage-pattern)
Get started with:

```


retriever = index.as_retriever()




nodes = retriever.retrieve("Who is Paul Graham?")


```

## Get Started
[Section titled “Get Started”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/#get-started)
Get a retriever from index:

```


retriever = index.as_retriever()


```

Retrieve relevant context for a question:

```


nodes = retriever.retrieve("Who is Paul Graham?")


```

> Note: To learn how to build an index, see [Indexing](https://developers.llamaindex.ai/python/framework/module_guides/indexing)
## High-Level API
[Section titled “High-Level API”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/#high-level-api)
### Selecting a Retriever
[Section titled “Selecting a Retriever”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/#selecting-a-retriever)
You can select the index-specific retriever class via `retriever_mode`. For example, with a `SummaryIndex`:

```


retriever = summary_index.as_retriever(




retriever_mode="llm",



```

This creates a [SummaryIndexLLMRetriever](https://developers.llamaindex.ai/python/framework/api_reference/retrievers/summary) on top of the summary index.
See [**Retriever Modes**](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retriever_modes) for a full list of (index-specific) retriever modes and the retriever classes they map to.
### Configuring a Retriever
[Section titled “Configuring a Retriever”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/#configuring-a-retriever)
In the same way, you can pass kwargs to configure the selected retriever.
> Note: take a look at the API reference for the selected retriever class’ constructor parameters for a list of valid kwargs.
For example, if we selected the “llm” retriever mode, we might do the following:

```


retriever = summary_index.as_retriever(




retriever_mode="llm",




choice_batch_size=5,



```

## Low-Level Composition API
[Section titled “Low-Level Composition API”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/#low-level-composition-api)
You can use the low-level composition API if you need more granular control.
To achieve the same outcome as above, you can directly import and construct the desired retriever class:

```


from llama_index.core.retrievers import SummaryIndexLLMRetriever





retriever = SummaryIndexLLMRetriever(




index=summary_index,




choice_batch_size=5,



```

## Examples
[Section titled “Examples”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/#examples)
See more examples in the [retrievers guide](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retrievers).
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


