[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/awadbdemo/#_top)
LlamaIndex Framework
Integrations
Vector stores
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Awadb Vector Store 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-embeddings-huggingface




%pip install llama-index-vector-stores-awadb


```


```


!pip install llama-index


```

## Creating an Awadb index
[Section titled “Creating an Awadb index”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/awadbdemo/#creating-an-awadb-index)

```


import logging




import sys





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


```

#### Load documents, build the VectorStoreIndex
[Section titled “Load documents, build the VectorStoreIndex”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/awadbdemo/#load-documents-build-the-vectorstoreindex)

```


from llama_index.core import (




SimpleDirectoryReader,




VectorStoreIndex,




StorageContext,





from IPython.display import Markdown, display




import openai





openai.api_key =""


```


```

INFO:numexpr.utils:Note: NumExpr detected 12 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8.


Note: NumExpr detected 12 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8.


INFO:numexpr.utils:NumExpr defaulting to 8 threads.


NumExpr defaulting to 8 threads.

```

#### Download Data
[Section titled “Download Data”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/awadbdemo/#download-data)

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```

#### Load Data
[Section titled “Load Data”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/awadbdemo/#load-data)

```

# load documents



documents = SimpleDirectoryReader("./data/paul_graham/").load_data()


```


```


from llama_index.embeddings.huggingface import HuggingFaceEmbedding




from llama_index.vector_stores.awadb import AwaDBVectorStore





embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")





vector_store = AwaDBVectorStore()




storage_context = StorageContext.from_defaults(vector_store=vector_store)





index = VectorStoreIndex.from_documents(




documents, storage_context=storage_context, embed_model=embed_model



```

#### Query Index
[Section titled “Query Index”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/awadbdemo/#query-index)

```

# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine()




response = query_engine.query("What did the author do growing up?")


```


```


display(Markdown(f"<b>{response}</b>"))


```

**Growing up, the author wrote short stories, experimented with programming on an IBM 1401, nagged his father to buy a TRS-80 computer, wrote simple games, a program to predict how high his model rockets would fly, and a word processor. He also studied philosophy in college, switched to AI, and worked on building the infrastructure of the web. He wrote essays and published them online, had dinners for a group of friends every Thursday night, painted, and bought a building in Cambridge.**

```

# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine()




response = query_engine.query(




"What did the author do after his time at Y Combinator?"



```


```


display(Markdown(f"<b>{response}</b>"))


```

**After his time at Y Combinator, the author wrote essays, worked on Lisp, and painted. He also visited his mother in Oregon and helped her get out of a nursing home.**
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


