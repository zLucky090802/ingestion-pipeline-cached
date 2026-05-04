[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/indexing/#_top)
LlamaIndex Framework
Component Guides
Indexing
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Indexing
## Concept
[Section titled “Concept”](https://developers.llamaindex.ai/python/framework/module_guides/indexing/#concept)
An `Index` is a data structure that allows us to quickly retrieve relevant context for a user query. For LlamaIndex, it’s the core foundation for retrieval-augmented generation (RAG) use-cases.
At a high-level, `Indexes` are built from [Documents](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes). They are used to build [Query Engines](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine) and [Chat Engines](https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines) which enables question & answer and chat over your data.
Under the hood, `Indexes` store data in `Node` objects (which represent chunks of the original documents), and expose a [Retriever](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever) interface that supports additional configuration and automation.
The most common index by far is the `VectorStoreIndex`; the best place to start is the [VectorStoreIndex usage guide](https://developers.llamaindex.ai/python/framework/module_guides/indexing/vector_store_index).
For other indexes, check out our guide to [how each index works](https://developers.llamaindex.ai/python/framework/module_guides/indexing/index_guide) to help you decide which one matches your use-case.
## Other Index resources
[Section titled “Other Index resources”](https://developers.llamaindex.ai/python/framework/module_guides/indexing/#other-index-resources)
See the [modules guide](https://developers.llamaindex.ai/python/framework/module_guides/indexing/modules).
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


