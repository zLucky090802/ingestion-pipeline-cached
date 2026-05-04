[Skip to content](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/knowledgegraphdemo/#_top)
# Knowledge Graph Index 
This tutorial gives a basic overview of how to use our `KnowledgeGraphIndex`, which handles automated knowledge graph construction from unstructured text as well as entity-based querying.
If you would like to query knowledge graphs in more flexible ways, including pre-existing ones, please check out our `KnowledgeGraphQueryEngine` and other constructs.

```


%pip install llama-index-llms-openai


```


```

# My OpenAI Key



import os





os.environ["OPENAI_API_KEY"] ="INSERT OPENAI KEY"


```


```


import logging




import sys





logging.basicConfig(stream=sys.stdout, level=logging.INFO)


```

## Using Knowledge Graph
[Section titled “Using Knowledge Graph”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/knowledgegraphdemo/#using-knowledge-graph)
#### Building the Knowledge Graph
[Section titled “Building the Knowledge Graph”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/knowledgegraphdemo/#building-the-knowledge-graph)

```


from llama_index.core import SimpleDirectoryReader, KnowledgeGraphIndex




from llama_index.core.graph_stores import SimpleGraphStore





from llama_index.llms.openai import OpenAI




from llama_index.core import Settings




from IPython.display import Markdown, display


```


```

INFO:numexpr.utils:NumExpr defaulting to 8 threads.

```


```


documents = SimpleDirectoryReader(




"../../../../examples/paul_graham_essay/data"



).load_data()

```


```

# define LLM



# NOTE: at the time of demo, text-davinci-002 did not have rate-limit errors





llm = OpenAI(temperature=0, model="text-davinci-002")




Settings.llm = llm




Settings.chunk_size =512


```


```


from llama_index.core import StorageContext





graph_store = SimpleGraphStore()




storage_context = StorageContext.from_defaults(graph_store=graph_store)





# NOTE: can take a while!




index = KnowledgeGraphIndex.from_documents(




documents,




max_triplets_per_chunk=2,




storage_context=storage_context,



```


```

INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total embedding token usage: 0 tokens

```

#### [Optional] Try building the graph and manually add triplets!
[Section titled “[Optional] Try building the graph and manually add triplets!”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/knowledgegraphdemo/#optional-try-building-the-graph-and-manually-add-triplets)
#### Querying the Knowledge Graph
[Section titled “Querying the Knowledge Graph”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/knowledgegraphdemo/#querying-the-knowledge-graph)

```


query_engine = index.as_query_engine(




include_text=False, response_mode="tree_summarize"





response = query_engine.query(




"Tell me more about Interleaf",



```


```

INFO:llama_index.indices.knowledge_graph.retrievers:> Starting query: Tell me more about Interleaf


INFO:llama_index.indices.knowledge_graph.retrievers:> Query keywords: ['Interleaf', 'company', 'software', 'history']


ERROR:llama_index.indices.knowledge_graph.retrievers:Index was not constructed with embeddings, skipping embedding usage...


INFO:llama_index.indices.knowledge_graph.retrievers:> Extracted relationships: The following are knowledge triplets in max depth 2 in the form of `subject [predicate, object, predicate_next_hop, object_next_hop ...]`


INFO:llama_index.token_counter.token_counter:> [get_response] Total LLM token usage: 116 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total embedding token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total LLM token usage: 116 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total embedding token usage: 0 tokens

```


```


display(Markdown(f"<b>{response}</b>"))


```

**Interleaf was a software company that developed and published document preparation and desktop publishing software. It was founded in 1986 and was headquartered in Waltham, Massachusetts. The company was acquired by Quark, Inc. in 2000.**

```


query_engine = index.as_query_engine(




include_text=True, response_mode="tree_summarize"





response = query_engine.query(




"Tell me more about what the author worked on at Interleaf",



```


```

INFO:llama_index.indices.knowledge_graph.retrievers:> Starting query: Tell me more about what the author worked on at Interleaf


INFO:llama_index.indices.knowledge_graph.retrievers:> Query keywords: ['author', 'Interleaf', 'work']


ERROR:llama_index.indices.knowledge_graph.retrievers:Index was not constructed with embeddings, skipping embedding usage...


INFO:llama_index.indices.knowledge_graph.retrievers:> Extracted relationships: The following are knowledge triplets in max depth 2 in the form of `subject [predicate, object, predicate_next_hop, object_next_hop ...]`


INFO:llama_index.token_counter.token_counter:> [get_response] Total LLM token usage: 104 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total embedding token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total LLM token usage: 104 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total embedding token usage: 0 tokens

```


```


display(Markdown(f"<b>{response}</b>"))


```

**The author worked on a number of projects at Interleaf, including the development of the company's flagship product, the Interleaf Publisher.**
#### Query with embeddings
[Section titled “Query with embeddings”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/knowledgegraphdemo/#query-with-embeddings)

```


# NOTE: can take a while!




new_index = KnowledgeGraphIndex.from_documents(




documents,




max_triplets_per_chunk=2,




include_embeddings=True,



```


```

INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total embedding token usage: 0 tokens

```


```

# query using top 3 triplets plus keywords (duplicate triplets are removed)



query_engine = index.as_query_engine(




include_text=True,




response_mode="tree_summarize",




embedding_mode="hybrid",




similarity_top_k=5,





response = query_engine.query(




"Tell me more about what the author worked on at Interleaf",



```


```

INFO:llama_index.indices.knowledge_graph.retrievers:> Starting query: Tell me more about what the author worked on at Interleaf


INFO:llama_index.indices.knowledge_graph.retrievers:> Query keywords: ['author', 'Interleaf', 'work']


ERROR:llama_index.indices.knowledge_graph.retrievers:Index was not constructed with embeddings, skipping embedding usage...


INFO:llama_index.indices.knowledge_graph.retrievers:> Extracted relationships: The following are knowledge triplets in max depth 2 in the form of `subject [predicate, object, predicate_next_hop, object_next_hop ...]`


INFO:llama_index.token_counter.token_counter:> [get_response] Total LLM token usage: 104 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total embedding token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total LLM token usage: 104 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total embedding token usage: 0 tokens

```


```


display(Markdown(f"<b>{response}</b>"))


```

**The author worked on a number of projects at Interleaf, including the development of the company's flagship product, the Interleaf Publisher.**
#### Visualizing the Graph
[Section titled “Visualizing the Graph”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/knowledgegraphdemo/#visualizing-the-graph)

```

## create graph



from pyvis.network import Network





g = index.get_networkx_graph()




net = Network(notebook=True, cdn_resources="in_line", directed=True)



net.from_nx(g)



net.show("example.html")


```


```

example.html

```

#### [Optional] Try building the graph and manually add triplets!
[Section titled “[Optional] Try building the graph and manually add triplets!”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/knowledgegraphdemo/#optional-try-building-the-graph-and-manually-add-triplets-1)

```


from llama_index.core.node_parser import SentenceSplitter


```


```


node_parser = SentenceSplitter()


```


```


nodes = node_parser.get_nodes_from_documents(documents)


```


```

# initialize an empty index for now



index = KnowledgeGraphIndex(




```


```

INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total embedding token usage: 0 tokens

```


```

# add keyword mappings and nodes manually


# add triplets (subject, relationship, object)



# for node 0



node_0_tups = [




("author", "worked on", "writing"),




("author", "worked on", "programming"),





for tup in node_0_tups:




index.upsert_triplet_and_node(tup, nodes[0])




# for node 1



node_1_tups = [




("Interleaf", "made software for", "creating documents"),




("Interleaf", "added", "scripting language"),




("software", "generate", "web sites"),





for tup in node_1_tups:




index.upsert_triplet_and_node(tup, nodes[1])


```


```


query_engine = index.as_query_engine(




include_text=False, response_mode="tree_summarize"





response = query_engine.query(




"Tell me more about Interleaf",



```


```

INFO:llama_index.indices.knowledge_graph.retrievers:> Starting query: Tell me more about Interleaf


INFO:llama_index.indices.knowledge_graph.retrievers:> Query keywords: ['Interleaf', 'company', 'software', 'history']


ERROR:llama_index.indices.knowledge_graph.retrievers:Index was not constructed with embeddings, skipping embedding usage...


INFO:llama_index.indices.knowledge_graph.retrievers:> Extracted relationships: The following are knowledge triplets in max depth 2 in the form of `subject [predicate, object, predicate_next_hop, object_next_hop ...]`


INFO:llama_index.token_counter.token_counter:> [get_response] Total LLM token usage: 116 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total embedding token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total LLM token usage: 116 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total embedding token usage: 0 tokens

```


```


str(response)


```


```

'\nInterleaf was a software company that developed and published document preparation and desktop publishing software. It was founded in 1986 and was headquartered in Waltham, Massachusetts. The company was acquired by Quark, Inc. in 2000.'

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


