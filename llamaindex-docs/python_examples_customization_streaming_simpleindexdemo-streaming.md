[Skip to content](https://developers.llamaindex.ai/python/examples/customization/streaming/simpleindexdemo-streaming/#_top)
# Streaming 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


!pip install llama-index


```


```


import logging




import sys





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))





from llama_index.core import VectorStoreIndex, SimpleDirectoryReader


```


```

INFO:numexpr.utils:Note: NumExpr detected 12 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8.


Note: NumExpr detected 12 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8.


INFO:numexpr.utils:NumExpr defaulting to 8 threads.


NumExpr defaulting to 8 threads.




/Users/suo/miniconda3/envs/llama/lib/python3.9/site-packages/deeplake/util/check_latest_version.py:32: UserWarning: A newer version of deeplake (3.6.7) is available. It's recommended that you update to the latest version using `pip install -U deeplake`.



warnings.warn(


```

#### Download Data
[Section titled “Download Data”](https://developers.llamaindex.ai/python/examples/customization/streaming/simpleindexdemo-streaming/#download-data)

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```

#### Load documents, build the VectorStoreIndex
[Section titled “Load documents, build the VectorStoreIndex”](https://developers.llamaindex.ai/python/examples/customization/streaming/simpleindexdemo-streaming/#load-documents-build-the-vectorstoreindex)

```

# load documents



documents = SimpleDirectoryReader("./data/paul_graham").load_data()


```


```


index = VectorStoreIndex.from_documents(documents)


```

#### Query Index
[Section titled “Query Index”](https://developers.llamaindex.ai/python/examples/customization/streaming/simpleindexdemo-streaming/#query-index)

```

# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine(streaming=True, similarity_top_k=1)




response_stream = query_engine.query(




"What did the author do growing up?",



```


```

response_stream.print_response_stream()

```


```

The author grew up writing short stories and programming on an IBM 1401. He also nagged his father to buy him a TRS-80 microcomputer, on which he wrote simple games, a program to predict how high his model rockets would fly, and a word processor. He eventually went to college to study philosophy, but found it boring and switched to AI.

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


