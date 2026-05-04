[Skip to content](https://developers.llamaindex.ai/python/examples/docstore/mongodocstoredemo/#_top)
# MongoDB Demo 
This guide shows you how to directly use our `DocumentStore` abstraction backed by MongoDB. By putting nodes in the docstore, this allows you to define multiple indices over the same underlying docstore, instead of duplicating data across indices.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-storage-docstore-mongodb




%pip install llama-index-storage-index-store-mongodb




%pip install llama-index-llms-openai


```


```


!pip install llama-index


```


```


import nest_asyncio




nest_asyncio.apply()

```


```


import logging




import sys




import os





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


```


```


from llama_index.core import SimpleDirectoryReader, StorageContext




from llama_index.core import VectorStoreIndex, SimpleKeywordTableIndex




from llama_index.core import SummaryIndex




from llama_index.core import ComposableGraph




from llama_index.llms.openai import OpenAI




from llama_index.core.response.notebook_utils import display_response




from llama_index.core import Settings


```

#### Download Data
[Section titled “Download Data”](https://developers.llamaindex.ai/python/examples/docstore/mongodocstoredemo/#download-data)

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```

#### Load Documents
[Section titled “Load Documents”](https://developers.llamaindex.ai/python/examples/docstore/mongodocstoredemo/#load-documents)

```


reader = SimpleDirectoryReader("./data/paul_graham/")




documents = reader.load_data()


```

#### Parse into Nodes
[Section titled “Parse into Nodes”](https://developers.llamaindex.ai/python/examples/docstore/mongodocstoredemo/#parse-into-nodes)

```


from llama_index.core.node_parser import SentenceSplitter





nodes = SentenceSplitter().get_nodes_from_documents(documents)


```

#### Add to Docstore
[Section titled “Add to Docstore”](https://developers.llamaindex.ai/python/examples/docstore/mongodocstoredemo/#add-to-docstore)

```


MONGO_URI= os.environ["MONGO_URI"]


```


```


from llama_index.storage.docstore.mongodb import MongoDocumentStore




from llama_index.storage.index_store.mongodb import MongoIndexStore


```


```


storage_context = StorageContext.from_defaults(




docstore=MongoDocumentStore.from_uri(uri=MONGO_URI),




index_store=MongoIndexStore.from_uri(uri=MONGO_URI),



```


```

storage_context.docstore.add_documents(nodes)

```

#### Define Multiple Indexes
[Section titled “Define Multiple Indexes”](https://developers.llamaindex.ai/python/examples/docstore/mongodocstoredemo/#define-multiple-indexes)
Each index uses the same underlying Node.

```


summary_index = SummaryIndex(nodes, storage_context=storage_context)


```


```


vector_index = VectorStoreIndex(nodes, storage_context=storage_context)


```


```


keyword_table_index = SimpleKeywordTableIndex(




nodes, storage_context=storage_context



```


```


# NOTE: the docstore still has the same nodes




len(storage_context.docstore.docs)


```

#### Test out saving and loading
[Section titled “Test out saving and loading”](https://developers.llamaindex.ai/python/examples/docstore/mongodocstoredemo/#test-out-saving-and-loading)

```


# NOTE: docstore and index_store is persisted in MongoDB by default




# NOTE: here only need to persist simple vector store to disk



storage_context.persist()

```


```

# note down index IDs



list_id = summary_index.index_id




vector_id = vector_index.index_id




keyword_id = keyword_table_index.index_id


```


```


from llama_index.core import load_index_from_storage




# re-create storage context



storage_context = StorageContext.from_defaults(




docstore=MongoDocumentStore.from_uri(uri=MONGO_URI),




index_store=MongoIndexStore.from_uri(uri=MONGO_URI),





# load indices



summary_index = load_index_from_storage(




storage_context=storage_context, index_id=list_id





vector_index = load_index_from_storage(




storage_context=storage_context, index_id=vector_id





keyword_table_index = load_index_from_storage(




storage_context=storage_context, index_id=keyword_id



```

#### Test out some Queries
[Section titled “Test out some Queries”](https://developers.llamaindex.ai/python/examples/docstore/mongodocstoredemo/#test-out-some-queries)

```


chatgpt = OpenAI(temperature=0, model="gpt-3.5-turbo")





Settings.llm = chatgpt




Settings.chunk_size =1024


```


```


query_engine = summary_index.as_query_engine()




list_response = query_engine.query("What is a summary of this document?")


```


```

display_response(list_response)

```


```


query_engine = vector_index.as_query_engine()




vector_response = query_engine.query("What did the author do growing up?")


```


```

display_response(vector_response)

```


```


query_engine = keyword_table_index.as_query_engine()




keyword_response = query_engine.query(




"What did the author do after his time at YC?"



```


```

display_response(keyword_response)

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


