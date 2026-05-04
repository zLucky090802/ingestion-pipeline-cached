[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retrievers/#_top)
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
# Retriever Modules
We are actively adding more tailored retrieval guides. In the meanwhile, please take a look at the [API References](https://developers.llamaindex.ai/python/framework-api-reference/retrievers).
## Index Retrievers
[Section titled “Index Retrievers”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retrievers/#index-retrievers)
Please see [the retriever modes](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retriever_modes) for more details on how to get a retriever from any given index.
If you want to import the corresponding retrievers directly, please check out our [API reference](https://developers.llamaindex.ai/python/framework-api-reference/retrievers).
## Comprehensive Retriever Guides
[Section titled “Comprehensive Retriever Guides”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retrievers/#comprehensive-retriever-guides)
Check out our comprehensive guides on various retriever modules, many of which cover advanced concepts (auto-retrieval, routing, ensembling, and more).
### Advanced Retrieval and Search
[Section titled “Advanced Retrieval and Search”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retrievers/#advanced-retrieval-and-search)
These guides contain advanced retrieval techniques. Some are common like keyword/hybrid search, reranking, and more. Some are specific to LLM + RAG workflows, like small-to-big and auto-merging retrieval.
  * [Define Custom Retriever](https://developers.llamaindex.ai/python/examples/query_engine/customretrievers)
  * [BM25 Hybrid Retriever](https://developers.llamaindex.ai/python/examples/retrievers/bm25_retriever)
  * [Simple Query Fusion](https://developers.llamaindex.ai/python/examples/retrievers/simple_fusion)
  * [Reciprocal Rerank Fusion](https://developers.llamaindex.ai/python/examples/retrievers/reciprocal_rerank_fusion)
  * [Auto Merging Retriever](https://developers.llamaindex.ai/python/examples/retrievers/auto_merging_retriever)
  * [Metadata Replacement](https://developers.llamaindex.ai/python/examples/node_postprocessor/metadatareplacementdemo)
  * [Composable Retrievers](https://developers.llamaindex.ai/python/examples/retrievers/composable_retrievers)


### Auto-Retrieval
[Section titled “Auto-Retrieval”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retrievers/#auto-retrieval)
These retrieval techniques perform **semi-structured** queries, combining semantic search with structured filtering.
  * [Auto-Retrieval (with Pinecone)](https://developers.llamaindex.ai/python/examples/vector_stores/pinecone_auto_retriever)
  * [Auto-Retrieval (with Lantern)](https://developers.llamaindex.ai/python/examples/vector_stores/lanternautoretriever)
  * [Auto-Retrieval (with Chroma)](https://developers.llamaindex.ai/python/examples/vector_stores/chroma_auto_retriever)
  * [Auto-Retrieval (with BagelDB)](https://developers.llamaindex.ai/python/examples/vector_stores/bagelautoretriever)
  * [Auto-Retrieval (with Vectara)](https://developers.llamaindex.ai/python/examples/retrievers/vectara_auto_retriever)
  * [Multi-Doc Auto-Retrieval](https://developers.llamaindex.ai/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval)


### Knowledge Graph Retrievers
[Section titled “Knowledge Graph Retrievers”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retrievers/#knowledge-graph-retrievers)
  * [Knowledge Graph RAG Retriever](https://developers.llamaindex.ai/python/examples/query_engine/knowledge_graph_rag_query_engine)


### Composed Retrievers
[Section titled “Composed Retrievers”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retrievers/#composed-retrievers)
These are retrieval techniques that are composed on top of other retrieval techniques - providing higher-level capabilities like hierarchical retrieval and query decomposition.
  * [Recursive Table Retrieval](https://developers.llamaindex.ai/python/examples/query_engine/pdf_tables/recursive_retriever)
  * [Recursive Node Retrieval](https://developers.llamaindex.ai/python/examples/retrievers/recursive_retriever_nodes)
  * [Ensemble Retriever](https://developers.llamaindex.ai/python/examples/retrievers/ensemble_retrieval)
  * [Multi-Doc Auto-Retrieval](https://developers.llamaindex.ai/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval)


### Managed Retrievers
[Section titled “Managed Retrievers”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retrievers/#managed-retrievers)


### Other Retrievers
[Section titled “Other Retrievers”](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retrievers/#other-retrievers)
These are guides that don’t fit neatly into a category but should be highlighted regardless.
  * [DeepMemory (Activeloop)](https://developers.llamaindex.ai/python/examples/retrievers/deep_memory)


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


