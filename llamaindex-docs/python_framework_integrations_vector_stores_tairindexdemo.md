[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/tairindexdemo/#_top)
LlamaIndex Framework
Integrations
Vector stores
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Tair Vector Store 
In this notebook we are going to show a quick demo of using the TairVectorStore.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-vector-stores-tair


```


```


!pip install llama-index


```


```


import os




import sys




import logging




import textwrap





import warnings





warnings.filterwarnings("ignore")




# stop huggingface warnings



os.environ["TOKENIZERS_PARALLELISM"] ="false"




# Uncomment to see debug logs


# logging.basicConfig(stream=sys.stdout, level=logging.INFO)


# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))




from llama_index.core import (




GPTVectorStoreIndex,




SimpleDirectoryReader,




Document,





from llama_index.vector_stores.tair import TairVectorStore




from IPython.display import Markdown, display


```

### Setup OpenAI
[Section titled “Setup OpenAI”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/tairindexdemo/#setup-openai)
Lets first begin by adding the openai api key. This will allow us to access openai for embeddings and to use chatgpt.

```


import os





os.environ["OPENAI_API_KEY"] ="sk-<your key here>"


```

### Download Data
[Section titled “Download Data”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/tairindexdemo/#download-data)

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```

### Read in a dataset
[Section titled “Read in a dataset”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/tairindexdemo/#read-in-a-dataset)

```

# load documents



documents = SimpleDirectoryReader("./data/paul_graham").load_data()




print(




"Document ID:",




documents[0].doc_id,




"Document Hash:",




documents[0].doc_hash,



```

### Build index from documents
[Section titled “Build index from documents”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/tairindexdemo/#build-index-from-documents)
Let’s build a vector index with `GPTVectorStoreIndex`, using `TairVectorStore` as its backend. Replace `tair_url` with the actual url of your Tair instance.

```


from llama_index.core import StorageContext





tair_url ="redis://{username}:{password}@r-bp****************.redis.rds.aliyuncs.com:{port}"





vector_store = TairVectorStore(




tair_url=tair_url, index_name="pg_essays", overwrite=True





storage_context = StorageContext.from_defaults(vector_store=vector_store)




index = GPTVectorStoreIndex.from_documents(




documents, storage_context=storage_context



```

### Query the data
[Section titled “Query the data”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/tairindexdemo/#query-the-data)
Now we can use the index as knowledge base and ask questions to it.

```


query_engine = index.as_query_engine()




response = query_engine.query("What did the author learn?")




print(textwrap.fill(str(response), 100))


```


```


response = query_engine.query("What was a hard moment for the author?")




print(textwrap.fill(str(response), 100))


```

### Deleting documents
[Section titled “Deleting documents”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/tairindexdemo/#deleting-documents)
To delete a document from the index, use `delete` method.

```


document_id = documents[0].doc_id



document_id

```


```


info = vector_store.client.tvs_get_index("pg_essays")




print("Number of documents", int(info["data_count"]))


```


```

vector_store.delete(document_id)

```


```


info = vector_store.client.tvs_get_index("pg_essays")




print("Number of documents", int(info["data_count"]))


```

### Deleting index
[Section titled “Deleting index”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/tairindexdemo/#deleting-index)
Delete the entire index using `delete_index` method.

```

vector_store.delete_index()

```


```


print("Check index existence:", vector_store.client._index_exists())


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


