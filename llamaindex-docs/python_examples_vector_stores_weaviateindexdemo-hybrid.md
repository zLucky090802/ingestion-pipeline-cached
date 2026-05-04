[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/weaviateindexdemo-hybrid/#_top)
LlamaIndex Framework
Integrations
Vector stores
[Weaviate Vector Store - Hybrid Search ](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/weaviateindexdemo-hybrid/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Weaviate Vector Store - Hybrid Search 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-vector-stores-weaviate


```


```


!pip install llama-index


```


```


import logging




import sys





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


```

## Creating a Weaviate Client
[Section titled “Creating a Weaviate Client”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/weaviateindexdemo-hybrid/#creating-a-weaviate-client)

```


import os




import openai





os.environ["OPENAI_API_KEY"] =""




openai.api_key = os.environ["OPENAI_API_KEY"]


```


```


import weaviate


```


```

# Connect to cloud instance



cluster_url =""




api_key =""





client = weaviate.connect_to_wcs(




cluster_url=cluster_url,




auth_credentials=weaviate.auth.AuthApiKey(api_key),





# Connect to local instance


# client = weaviate.connect_to_local()

```


```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader




from llama_index.vector_stores.weaviate import WeaviateVectorStore




from llama_index.core.response.notebook_utils import display_response


```

## Download Data
[Section titled “Download Data”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/weaviateindexdemo-hybrid/#download-data)

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```

## Load documents
[Section titled “Load documents”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/weaviateindexdemo-hybrid/#load-documents)

```

# load documents



documents = SimpleDirectoryReader("./data/paul_graham/").load_data()


```

## Build the VectorStoreIndex with WeaviateVectorStore
[Section titled “Build the VectorStoreIndex with WeaviateVectorStore”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/weaviateindexdemo-hybrid/#build-the-vectorstoreindex-with-weaviatevectorstore)

```


from llama_index.core import StorageContext






vector_store = WeaviateVectorStore(weaviate_client=client)




storage_context = StorageContext.from_defaults(vector_store=vector_store)




index = VectorStoreIndex.from_documents(




documents, storage_context=storage_context






# NOTE: you may also choose to define a index_name manually.



# index_name = "test_prefix"


# vector_store = WeaviateVectorStore(weaviate_client=client, index_name=index_name)

```

## Query Index with Default Vector Search
[Section titled “Query Index with Default Vector Search”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/weaviateindexdemo-hybrid/#query-index-with-default-vector-search)

```

# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine(similarity_top_k=2)




response = query_engine.query("What did the author do growing up?")


```


```

display_response(response)

```

## Query Index with Hybrid Search
[Section titled “Query Index with Hybrid Search”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/weaviateindexdemo-hybrid/#query-index-with-hybrid-search)
Use hybrid search with bm25 and vector. `alpha` parameter determines weighting (alpha = 0 -> bm25, alpha=1 -> vector search).
### By default, `alpha=0.75` is used (very similar to vector search)
[Section titled “By default, alpha=0.75 is used (very similar to vector search)”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/weaviateindexdemo-hybrid/#by-default-alpha075-is-used-very-similar-to-vector-search)

```

# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine(




vector_store_query_mode="hybrid", similarity_top_k=2





response = query_engine.query(




"What did the author do growing up?",



```


```

display_response(response)

```

### Set `alpha=0.` to favor bm25
[Section titled “Set alpha=0. to favor bm25”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/weaviateindexdemo-hybrid/#set-alpha0-to-favor-bm25)

```

# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine(




vector_store_query_mode="hybrid", similarity_top_k=2, alpha=0.0





response = query_engine.query(




"What did the author do growing up?",



```


```

display_response(response)

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


