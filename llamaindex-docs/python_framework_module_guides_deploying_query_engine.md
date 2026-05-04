[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/#_top)
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
# Query Engine
## Concept
[Section titled “Concept”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/#concept)
Query engine is a generic interface that allows you to ask question over your data.
A query engine takes in a natural language query, and returns a rich response. It is most often (but not always) built on one or many [indexes](https://developers.llamaindex.ai/python/framework/module_guides/indexing) via [retrievers](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever). You can compose multiple query engines to achieve more advanced capability.
## Usage Pattern
[Section titled “Usage Pattern”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/#usage-pattern)
Get started with:

```


query_engine = index.as_query_engine()




response = query_engine.query("Who is Paul Graham.")


```

To stream response:

```


query_engine = index.as_query_engine(streaming=True)




streaming_response = query_engine.query("Who is Paul Graham.")



streaming_response.print_response_stream()

```

See the full [usage pattern](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/usage_pattern) for more details.
## Modules
[Section titled “Modules”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/#modules)
Find all the modules in the [modules guide](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/modules).
## Supporting Modules
[Section titled “Supporting Modules”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/#supporting-modules)
There are also [supporting modules](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/supporting_modules).
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


