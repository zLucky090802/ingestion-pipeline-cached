[Skip to content](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/falkordbgraphdemo/#_top)
# FalkorDB Graph Store 
This notebook walks through configuring `FalkorDB` to be the backend for graph storage in LlamaIndex.

```


%pip install llama-index-llms-openai




%pip install llama-index-graph-stores-falkordb


```


```

# My OpenAI Key



import os





os.environ["OPENAI_API_KEY"] ="API_KEY_HERE"


```


```


import logging




import sys





logging.basicConfig(stream=sys.stdout, level=logging.INFO)


```

## Using Knowledge Graph with FalkorDBGraphStore
[Section titled “Using Knowledge Graph with FalkorDBGraphStore”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/falkordbgraphdemo/#using-knowledge-graph-with-falkordbgraphstore)
### Start FalkorDB
[Section titled “Start FalkorDB”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/falkordbgraphdemo/#start-falkordb)
The easiest way to start FalkorDB as a Graph database is using the [falkordb](https://hub.docker.com/r/falkordb/falkordb:edge) docker image.
To follow every step of this tutorial, launch the image as follows:
Terminal window
```


dockerrun-p6379:6379-it--rmfalkordb/falkordb:edge


```


```


from llama_index.graph_stores.falkordb import FalkorDBGraphStore





graph_store = FalkorDBGraphStore(




"redis://localhost:6379", decode_responses=True



```


```

INFO:numexpr.utils:NumExpr defaulting to 8 threads.

```

#### Building the Knowledge Graph
[Section titled “Building the Knowledge Graph”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/falkordbgraphdemo/#building-the-knowledge-graph)

```


from llama_index.core import SimpleDirectoryReader, KnowledgeGraphIndex





from llama_index.llms.openai import OpenAI




from llama_index.core import Settings




from IPython.display import Markdown, display


```


```


documents = SimpleDirectoryReader(




"../../../../examples/paul_graham_essay/data"



).load_data()

```


```

# define LLM




llm = OpenAI(temperature=0, model="gpt-3.5-turbo")




Settings.llm = llm




Settings.chunk_size =512


```


```


from llama_index.core import StorageContext





storage_context = StorageContext.from_defaults(graph_store=graph_store)





# NOTE: can take a while!




index = KnowledgeGraphIndex.from_documents(




documents,




max_triplets_per_chunk=2,




storage_context=storage_context,



```

#### Querying the Knowledge Graph
[Section titled “Querying the Knowledge Graph”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/falkordbgraphdemo/#querying-the-knowledge-graph)
First, we can query and send only the triplets to the LLM.

```


query_engine = index.as_query_engine(




include_text=False, response_mode="tree_summarize"





response = query_engine.query(




"Tell me more about Interleaf",



```


```


display(Markdown(f"<b>{response}</b>"))


```

**Interleaf is a software company that was founded in 1981. It specialized in developing and selling desktop publishing software. The company’s flagship product was called Interleaf, which was a powerful tool for creating and publishing complex documents. Interleaf’s software was widely used in industries such as aerospace, defense, and government, where there was a need for creating technical documentation and manuals. The company was acquired by BroadVision in 2000.**
For more detailed answers, we can also send the text from where the retrieved tripets were extracted.

```


query_engine = index.as_query_engine(




include_text=True, response_mode="tree_summarize"





response = query_engine.query(




"Tell me more about Interleaf",



```


```


display(Markdown(f"<b>{response}</b>"))


```

**Interleaf was a company that had smart people and built impressive technology. However, it faced challenges and eventually got crushed by Moore’s Law. The exponential growth in the power of commodity processors, particularly Intel processors, in the 1990s led to the consolidation of high-end, special-purpose hardware and software companies. Interleaf was one of the casualties of this trend. While the company had talented individuals and advanced technology, it was unable to compete with the rapid advancements in processor power.**
#### Visualizing the Graph
[Section titled “Visualizing the Graph”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/falkordbgraphdemo/#visualizing-the-graph)

```


%pip install pyvis


```


```

## create graph



from pyvis.network import Network





g = index.get_networkx_graph()




net = Network(notebook=True, cdn_resources="in_line", directed=True)



net.from_nx(g)



net.show("falkordbgraph_draw.html")


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


