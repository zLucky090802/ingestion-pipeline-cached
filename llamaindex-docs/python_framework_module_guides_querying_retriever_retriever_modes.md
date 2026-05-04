[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retriever_modes/#_top)
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
# Retriever Modes
Here we show the mapping from `retriever_mode` configuration to the selected retriever class.
> Note that `retriever_mode` can mean different thing for different index classes.
## Vector Index
[Section titled “Vector Index”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retriever_modes/#vector-index)
Specifying `retriever_mode` has no effect (silently ignored). `vector_index.as_retriever(...)` always returns a VectorIndexRetriever.
## Summary Index
[Section titled “Summary Index”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retriever_modes/#summary-index)
  * `default`: SummaryIndexRetriever
  * `embedding`: SummaryIndexEmbeddingRetriever
  * `llm`: SummaryIndexLLMRetriever


## Tree Index
[Section titled “Tree Index”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retriever_modes/#tree-index)
  * `select_leaf`: TreeSelectLeafRetriever
  * `select_leaf_embedding`: TreeSelectLeafEmbeddingRetriever
  * `all_leaf`: TreeAllLeafRetriever
  * `root`: TreeRootRetriever


## Keyword Table Index
[Section titled “Keyword Table Index”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retriever_modes/#keyword-table-index)
  * `default`: KeywordTableGPTRetriever
  * `simple`: KeywordTableSimpleRetriever
  * `rake`: KeywordTableRAKERetriever


## Knowledge Graph Index
[Section titled “Knowledge Graph Index”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retriever_modes/#knowledge-graph-index)
  * `keyword`: KGTableRetriever
  * `embedding`: KGTableRetriever
  * `hybrid`: KGTableRetriever


## Document Summary Index
[Section titled “Document Summary Index”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retriever_modes/#document-summary-index)
  * `llm`: DocumentSummaryIndexLLMRetriever
  * `embedding`: DocumentSummaryIndexEmbeddingRetrievers


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


