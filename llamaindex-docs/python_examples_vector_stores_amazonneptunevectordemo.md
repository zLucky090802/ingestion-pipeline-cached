[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/amazonneptunevectordemo/#_top)
LlamaIndex Framework
Integrations
Vector stores
[Amazon Neptune - Neptune Analytics vector store ](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/amazonneptunevectordemo/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Amazon Neptune - Neptune Analytics vector store 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-vector-stores-neptune


```

## Initiate Neptune Analytics vector wrapper
[Section titled “Initiate Neptune Analytics vector wrapper”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/amazonneptunevectordemo/#initiate-neptune-analytics-vector-wrapper)

```


from llama_index.vector_stores.neptune import NeptuneAnalyticsVectorStore





graph_identifier =""




embed_dim =1536





neptune_vector_store = NeptuneAnalyticsVectorStore(




graph_identifier=graph_identifier, embedding_dimension=1536



```

## Load documents, build the VectorStoreIndex
[Section titled “Load documents, build the VectorStoreIndex”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/amazonneptunevectordemo/#load-documents-build-the-vectorstoreindex)

```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader




from IPython.display import Markdown, display


```

Download Data

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```


```

# load documents



documents = SimpleDirectoryReader("./data/paul_graham").load_data()


```


```


from llama_index.core import StorageContext





storage_context = StorageContext.from_defaults(




vector_store=neptune_vector_store





index = VectorStoreIndex.from_documents(




documents, storage_context=storage_context



```


```


query_engine = index.as_query_engine()




response = query_engine.query("What happened at interleaf?")




display(Markdown(f"<b>{response}</b>"))


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


