[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/myscaleindexdemo/#_top)
LlamaIndex Framework
Integrations
Vector stores
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# MyScale Vector Store 
In this notebook we are going to show a quick demo of using the MyScaleVectorStore.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-vector-stores-myscale


```


```


!pip install llama-index


```

#### Creating a MyScale Client
[Section titled “Creating a MyScale Client”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/myscaleindexdemo/#creating-a-myscale-client)

```


import logging




import sys





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


```


```


from os import environ




import clickhouse_connect





environ["OPENAI_API_KEY"] ="sk-*"




# initialize client



client = clickhouse_connect.get_client(




host="YOUR_CLUSTER_HOST",




port=8443,




username="YOUR_USERNAME",




password="YOUR_CLUSTER_PASSWORD",



```

#### Load documents, build and store the VectorStoreIndex with MyScaleVectorStore
[Section titled “Load documents, build and store the VectorStoreIndex with MyScaleVectorStore”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/myscaleindexdemo/#load-documents-build-and-store-the-vectorstoreindex-with-myscalevectorstore)
Here we will use a set of Paul Graham essays to provide the text to turn into embeddings, store in a `MyScaleVectorStore` and query to find context for our LLM QnA loop.

```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader




from llama_index.vector_stores.myscale import MyScaleVectorStore




from IPython.display import Markdown, display


```


```

# load documents



documents = SimpleDirectoryReader("../data/paul_graham").load_data()




print("Document ID:", documents[0].doc_id)




print("Number of Documents: ", len(documents))


```


```

Document ID: a5f2737c-ed18-4e5d-ab9a-75955edb816d


Number of Documents:  1

```

Download Data

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```

You can process your files individually using [SimpleDirectoryReader](https://developers.llamaindex.ai/examples/data_connectors/simple_directory_reader.ipynb):

```


loader = SimpleDirectoryReader("./data/paul_graham/")




documents = loader.load_data()




forfilein loader.input_files:




print(file)




# Here is where you would do any preprocessing


```


```

../data/paul_graham/paul_graham_essay.txt

```


```

# initialize with metadata filter and store indexes



from llama_index.core import StorageContext





for document in documents:




document.metadata = {"user_id": "123", "favorite_color": "blue"}




vector_store = MyScaleVectorStore(myscale_client=client)




storage_context = StorageContext.from_defaults(vector_store=vector_store)




index = VectorStoreIndex.from_documents(




documents, storage_context=storage_context



```

#### Query Index
[Section titled “Query Index”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/myscaleindexdemo/#query-index)
Now MyScale vector store supports filter search and hybrid search
You can learn more about [query_engine](https://developers.llamaindex.ai/module_guides/deploying/query_engine/index.md) and [retriever](https://developers.llamaindex.ai/module_guides/querying/retriever/index.md).

```


import textwrap





from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters




# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine(




filters=MetadataFilters(




filters=[




ExactMatchFilter(key="user_id", value="123"),






similarity_top_k=2,




vector_store_query_mode="hybrid",





response = query_engine.query("What did the author learn?")




print(textwrap.fill(str(response), 100))


```

#### Clear All Indexes
[Section titled “Clear All Indexes”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/myscaleindexdemo/#clear-all-indexes)

```


for document in documents:




index.delete_ref_doc(document.doc_id)


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


