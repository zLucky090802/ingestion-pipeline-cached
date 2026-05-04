[Skip to content](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/q_and_a/#_top)
LlamaIndex Framework
Learn
Putting It All Together
Q And A
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Q&A patterns
## Semantic Search
[Section titled “Semantic Search”](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/q_and_a/#semantic-search)
The most basic example usage of LlamaIndex is through semantic search. We provide a simple in-memory vector store for you to get started, but you can also choose to use any one of our [vector store integrations](https://developers.llamaindex.ai/python/framework/community/integrations/vector_stores):

```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader





documents = SimpleDirectoryReader("data").load_data()




index = VectorStoreIndex.from_documents(documents)




query_engine = index.as_query_engine()




response = query_engine.query("What did the author do growing up?")




print(response)


```

**Tutorials**
  * [Basic Usage Pattern](https://developers.llamaindex.ai/python/framework/module_guides/querying)


**Guides**
  * [Example Notebook](https://developers.llamaindex.ai/python/examples/vector_stores/simpleindexdemo))


## Summarization
[Section titled “Summarization”](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/q_and_a/#summarization)
A summarization query requires the LLM to iterate through many if not most documents in order to synthesize an answer. For instance, a summarization query could look like one of the following:
  * “What is a summary of this collection of text?”
  * “Give me a summary of person X’s experience with the company.”


In general, a summary index would be suited for this use case. A summary index by default goes through all the data.
Empirically, setting `response_mode="tree_summarize"` also leads to better summarization results.

```


index = SummaryIndex.from_documents(documents)





query_engine = index.as_query_engine(response_mode="tree_summarize")




response = query_engine.query("<summarization_query>")


```

## Queries over Structured Data
[Section titled “Queries over Structured Data”](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/q_and_a/#queries-over-structured-data)
LlamaIndex supports queries over structured data, whether that’s a Pandas DataFrame or a SQL Database.
Here are some relevant resources:
**Tutorials**


**Guides**
  * [SQL Guide (Core)](https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/sqlindexdemo) ([Notebook](https://github.com/jerryjliu/llama_index/blob/main/docs../../examples/index_structs/struct_indices/SQLIndexDemo.ipynb))


## Routing over Heterogeneous Data
[Section titled “Routing over Heterogeneous Data”](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/q_and_a/#routing-over-heterogeneous-data)
LlamaIndex also supports routing over heterogeneous data sources with `RouterQueryEngine` - for instance, if you want to “route” a query to an underlying Document or a sub-index.
To do this, first build the sub-indices over different data sources. Then construct the corresponding query engines, and give each query engine a description to obtain a `QueryEngineTool`.

```


from llama_index.core import TreeIndex, VectorStoreIndex




from llama_index.core.tools import QueryEngineTool






# define sub-indices



index1 = VectorStoreIndex.from_documents(notion_docs)




index2 = VectorStoreIndex.from_documents(slack_docs)




# define query engines and tools



tool1 = QueryEngineTool.from_defaults(




query_engine=index1.as_query_engine(),




description="Use this query engine to do...",





tool2 = QueryEngineTool.from_defaults(




query_engine=index2.as_query_engine(),




description="Use this query engine for something else...",



```

Then, we define a `RouterQueryEngine` over them. By default, this uses a `LLMSingleSelector` as the router, which uses the LLM to choose the best sub-index to router the query to, given the descriptions.

```


from llama_index.core.query_engine import RouterQueryEngine





query_engine = RouterQueryEngine.from_defaults(




query_engine_tools=[tool1, tool2]






response = query_engine.query(




"In Notion, give me a summary of the product roadmap."



```

**Guides**
  * [Router Query Engine Guide](https://developers.llamaindex.ai/python/examples/query_engine/retrieverrouterqueryengine)


## Compare/Contrast Queries
[Section titled “Compare/Contrast Queries”](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/q_and_a/#comparecontrast-queries)
You can explicitly perform compare/contrast queries with a **query transformation** module within a ComposableGraph.

```


from llama_index.core.query.query_transform.base import DecomposeQueryTransform





decompose_transform = DecomposeQueryTransform(




service_context.llm, verbose=True



```

This module will help break down a complex query into a simpler one over your existing index structure.
**Guides**
  * [Query Transformations](https://developers.llamaindex.ai/python/framework/optimizing/advanced_retrieval/query_transformations)


You can also rely on the LLM to _infer_ whether to perform compare/contrast queries (see Multi Document Queries below).
## Multi Document Queries
[Section titled “Multi Document Queries”](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/q_and_a/#multi-document-queries)
Besides the explicit synthesis/routing flows described above, LlamaIndex can support more general multi-document queries as well. It can do this through our `SubQuestionQueryEngine` class. Given a query, this query engine will generate a “query plan” containing sub-queries against sub-documents before synthesizing the final answer.
To do this, first define an index for each document/data source, and wrap it with a `QueryEngineTool` (similar to above):

```


from llama_index.core.tools import QueryEngineTool





query_engine_tools = [




QueryEngineTool.from_defaults(




query_engine=sept_engine,




name="sept_22",




description="Provides information about Uber quarterly financials ending September 2022",





QueryEngineTool.from_defaults(




query_engine=june_engine,




name="june_22",




description="Provides information about Uber quarterly financials ending June 2022",





QueryEngineTool.from_defaults(




query_engine=march_engine,




name="march_22",




description="Provides information about Uber quarterly financials ending March 2022",




```

Then, we define a `SubQuestionQueryEngine` over these tools:

```


from llama_index.core.query_engine import SubQuestionQueryEngine





query_engine = SubQuestionQueryEngine.from_defaults(




query_engine_tools=query_engine_tools



```

This query engine can execute any number of sub-queries against any subset of query engine tools before synthesizing the final answer. This makes it especially well-suited for compare/contrast queries across documents as well as queries pertaining to a specific document.
**Guides**
  * [Sub Question Query Engine (Intro)](https://developers.llamaindex.ai/python/examples/query_engine/sub_question_query_engine)
  * [10Q Analysis (Uber)](https://developers.llamaindex.ai/python/examples/usecases/10k_sub_question)
  * [10K Analysis (Uber and Lyft)](https://developers.llamaindex.ai/python/examples/usecases/10k_sub_question)


## Multi-Step Queries
[Section titled “Multi-Step Queries”](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/q_and_a/#multi-step-queries)
LlamaIndex can also support iterative multi-step queries. Given a complex query, break it down into an initial subquestions, and sequentially generate subquestions based on returned answers until the final answer is returned.
For instance, given a question “Who was in the first batch of the accelerator program the author started?”, the module will first decompose the query into a simpler initial question “What was the accelerator program the author started?”, query the index, and then ask followup questions.
**Guides**
  * [Query Transformations](https://developers.llamaindex.ai/python/framework/optimizing/advanced_retrieval/query_transformations)
  * [Multi-Step Query Decomposition](https://developers.llamaindex.ai/python/examples/query_transformations/hydequerytransformdemo)


## Temporal Queries
[Section titled “Temporal Queries”](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/q_and_a/#temporal-queries)
LlamaIndex can support queries that require an understanding of time. It can do this in two ways:
  * Decide whether the query requires utilizing temporal relationships between nodes (prev/next relationships) in order to retrieve additional context to answer the question.
  * Sort by recency and filter outdated context.


**Guides**
  * [Prev/Next Postprocessing](https://developers.llamaindex.ai/python/examples/node_postprocessor/prevnextpostprocessordemo)
  * [Recency Postprocessing](https://developers.llamaindex.ai/python/examples/node_postprocessor/recencypostprocessordemo)


## Additional Resources
[Section titled “Additional Resources”](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/q_and_a/#additional-resources)
  * [A Guide to Extracting Terms and Definitions](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/q_and_a/terms_definitions_tutorial)


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


