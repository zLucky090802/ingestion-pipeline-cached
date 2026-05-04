[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/usage_pattern/#_top)
LlamaIndex Framework
Component Guides
Deploying
Query Engine
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Usage Pattern
## Get Started
[Section titled “Get Started”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/usage_pattern/#get-started)
Build a query engine from index:

```


query_engine = index.as_query_engine()


```

Ask a question over your data

```


response = query_engine.query("Who is Paul Graham?")


```

## Configuring a Query Engine
[Section titled “Configuring a Query Engine”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/usage_pattern/#configuring-a-query-engine)
### High-Level API
[Section titled “High-Level API”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/usage_pattern/#high-level-api)
You can directly build and configure a query engine from an index in 1 line of code:

```


query_engine = index.as_query_engine(




response_mode="tree_summarize",




verbose=True,



```

> Note: While the high-level API optimizes for ease-of-use, it does _NOT_ expose full range of configurability.
See [**Response Modes**](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/response_modes) for a full list of response modes and what they do.
### Low-Level Composition API
[Section titled “Low-Level Composition API”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/usage_pattern/#low-level-composition-api)
You can use the low-level composition API if you need more granular control. Concretely speaking, you would explicitly construct a `QueryEngine` object instead of calling `index.as_query_engine(...)`.
> Note: You may need to look at API references or example notebooks.

```


from llama_index.core import VectorStoreIndex, get_response_synthesizer




from llama_index.core.retrievers import VectorIndexRetriever




from llama_index.core.query_engine import RetrieverQueryEngine




# build index



index = VectorStoreIndex.from_documents(documents)




# configure retriever



retriever = VectorIndexRetriever(




index=index,




similarity_top_k=2,





# configure response synthesizer



response_synthesizer = get_response_synthesizer(




response_mode="tree_summarize",





# assemble query engine



query_engine = RetrieverQueryEngine(




retriever=retriever,




response_synthesizer=response_synthesizer,





# query



response = query_engine.query("What did the author do growing up?")




print(response)


```

### Streaming
[Section titled “Streaming”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/usage_pattern/#streaming)
To enable streaming, you simply need to pass in a `streaming=True` flag

```


query_engine = index.as_query_engine(




streaming=True,





streaming_response = query_engine.query(




"What did the author do growing up?",




streaming_response.print_response_stream()

```

  * Read the full [streaming guide](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/streaming)
  * See an [end-to-end example](https://developers.llamaindex.ai/python/examples/customization/streaming/simpleindexdemo-streaming)


## Defining a Custom Query Engine
[Section titled “Defining a Custom Query Engine”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/usage_pattern/#defining-a-custom-query-engine)
You can also define a custom query engine. Simply subclass the `CustomQueryEngine` class, define any attributes you’d want to have (similar to defining a Pydantic class), and implement a `custom_query` function that returns either a `Response` object or a string.

```


from llama_index.core.query_engine import CustomQueryEngine




from llama_index.core.retrievers import BaseRetriever




from llama_index.core import get_response_synthesizer




from llama_index.core.response_synthesizers import BaseSynthesizer






classRAGQueryEngine(CustomQueryEngine):




"""RAG Query Engine."""





retriever: BaseRetriever




response_synthesizer: BaseSynthesizer





defcustom_query(self, query_str: str):




nodes =self.retriever.retrieve(query_str)




response_obj =self.response_synthesizer.synthesize(query_str, nodes)




return response_obj


```

See the [Custom Query Engine guide](https://developers.llamaindex.ai/python/examples/query_engine/custom_query_engine) for more details.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


