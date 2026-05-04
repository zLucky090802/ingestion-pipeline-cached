[Skip to content](https://developers.llamaindex.ai/python/examples/ingestion/ingestion_gdrive/#_top)
# Building a Live RAG Pipeline over Google Drive Files 
In this guide we show you how to build a “live” RAG pipeline over Google Drive files.
This pipeline will index Google Drive files and dump them to a Redis vector store. Afterwards, every time you rerun the ingestion pipeline, the pipeline will propagate **incremental updates** , so that only changed documents are updated in the vector store. This means that we don’t re-index all the documents!
We use the following [data source](https://drive.google.com/drive/folders/1RFhr3-KmOZCR5rtp4dlOMNl3LKe1kOA5?usp=sharing) - you will need to copy these files and upload them to your own Google Drive directory!
**NOTE** : You will also need to setup a service account and credentials.json. See our LlamaHub page for the Google Drive loader for more details: <https://llamahub.ai/l/readers/llama-index-readers-google?from=readers>
## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/examples/ingestion/ingestion_gdrive/#setup)
We install required packages and launch the Redis Docker image.

```


%pip install llama-index-storage-docstore-redis




%pip install llama-index-vector-stores-redis




%pip install llama-index-embeddings-huggingface




%pip install llama-index-readers-google


```


```

# if creating a new container



!docker run -d --name redis-stack -p 6379:6379-p 8001:8001 redis/redis-stack:latest



# # if starting an existing container


# !docker start -a redis-stack

```


```

d32273cc1267d3221afa780db0edcd6ce5eee08ae88886f645410b9a220d4916

```


```


import os





os.environ["OPENAI_API_KEY"] ="sk-..."


```

## Define Ingestion Pipeline
[Section titled “Define Ingestion Pipeline”](https://developers.llamaindex.ai/python/examples/ingestion/ingestion_gdrive/#define-ingestion-pipeline)
Here we define the ingestion pipeline. Given a set of documents, we will run sentence splitting/embedding transformations, and then load them into a Redis docstore/vector store.
The vector store is for indexing the data + storing the embeddings, the docstore is for tracking duplicates.

```


from llama_index.embeddings.huggingface import HuggingFaceEmbedding




from llama_index.core.ingestion import (




DocstoreStrategy,




IngestionPipeline,




IngestionCache,





from llama_index.storage.kvstore.redis import RedisKVStore as RedisCache




from llama_index.storage.docstore.redis import RedisDocumentStore




from llama_index.core.node_parser import SentenceSplitter




from llama_index.vector_stores.redis import RedisVectorStore





from redisvl.schema import IndexSchema


```


```


embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")


```


```

model.safetensors:   0%|          | 0.00/133M [00:00<?, ?B/s]





tokenizer_config.json:   0%|          | 0.00/366 [00:00<?, ?B/s]





vocab.txt:   0%|          | 0.00/232k [00:00<?, ?B/s]





tokenizer.json:   0%|          | 0.00/711k [00:00<?, ?B/s]





special_tokens_map.json:   0%|          | 0.00/125 [00:00<?, ?B/s]





1_Pooling/config.json:   0%|          | 0.00/190 [00:00<?, ?B/s]

```


```


custom_schema = IndexSchema.from_dict(





"index": {"name": "gdrive", "prefix": "doc"},




# customize fields that are indexed




"fields": [




# required fields for llamaindex




{"type": "tag", "name": "id"},




{"type": "tag", "name": "doc_id"},




{"type": "text", "name": "text"},




# custom vector field for bge-small-en-v1.5 embeddings





"type": "vector",




"name": "vector",




"attrs": {




"dims": 384,




"algorithm": "hnsw",




"distance_metric": "cosine",










vector_store = RedisVectorStore(




schema=custom_schema,




redis_url="redis://localhost:6379",



```


```

# Optional: clear vector store if exists



if vector_store.index_exists():




vector_store.delete_index()


```


```

# Set up the ingestion cache layer



cache = IngestionCache(




cache=RedisCache.from_host_and_port("localhost", 6379),




collection="redis_cache",



```


```


pipeline = IngestionPipeline(




transformations=[




SentenceSplitter(),




embed_model,





docstore=RedisDocumentStore.from_host_and_port(




"localhost", 6379, namespace="document_store"





vector_store=vector_store,




cache=cache,




docstore_strategy=DocstoreStrategy.UPSERTS,



```

### Define our Vector Store Index
[Section titled “Define our Vector Store Index”](https://developers.llamaindex.ai/python/examples/ingestion/ingestion_gdrive/#define-our-vector-store-index)
We define our index to wrap the underlying vector store.

```


from llama_index.core import VectorStoreIndex





index = VectorStoreIndex.from_vector_store(




pipeline.vector_store, embed_model=embed_model



```

## Load Initial Data
[Section titled “Load Initial Data”](https://developers.llamaindex.ai/python/examples/ingestion/ingestion_gdrive/#load-initial-data)
Here we load data from our [Google Drive Loader](https://llamahub.ai/l/readers/llama-index-readers-google?from=readers) on LlamaHub.
The loaded docs are the header sections of our [Use Cases from our documentation](https://docs.llamaindex.ai/en/latest/use_cases/q_and_a/root.html).

```


from llama_index.readers.google import GoogleDriveReader


```


```


loader = GoogleDriveReader()


```


```


defload_data(folder_id: str):




docs = loader.load_data(folder_id=folder_id)




for doc in docs:




doc.id_ = doc.metadata["file_name"]




return docs






docs = load_data(folder_id="1RFhr3-KmOZCR5rtp4dlOMNl3LKe1kOA5")



# print(docs)

```


```


nodes = pipeline.run(documents=docs)




print(f"Ingested {len(nodes)} Nodes")


```

Since this is our first time starting up the vector store, we see that we’ve transformed/ingested all the documents into it (by chunking, and then by embedding).
### Ask Questions over Initial Data
[Section titled “Ask Questions over Initial Data”](https://developers.llamaindex.ai/python/examples/ingestion/ingestion_gdrive/#ask-questions-over-initial-data)

```


query_engine = index.as_query_engine()


```


```


response = query_engine.query("What are the sub-types of question answering?")


```


```


print(str(response))


```


```

The sub-types of question answering mentioned in the context are semantic search and summarization.

```

## Modify and Reload the Data
[Section titled “Modify and Reload the Data”](https://developers.llamaindex.ai/python/examples/ingestion/ingestion_gdrive/#modify-and-reload-the-data)
Let’s try modifying our ingested data!
We modify the “Q&A” doc to include an extra “structured analytics” block of text. See our [updated document](https://docs.google.com/document/d/1QQMKNAgyplv2IUOKNClEBymOFaASwmsZFoLmO_IeSTw/edit?usp=sharing) as a reference.
Now let’s rerun the ingestion pipeline.

```


docs = load_data(folder_id="1RFhr3-KmOZCR5rtp4dlOMNl3LKe1kOA5")




nodes = pipeline.run(documents=docs)




print(f"Ingested {len(nodes)} Nodes")


```

Notice how only one node is ingested. This is beacuse only one document changed, while the other documents stayed the same. This means that we only need to re-transform and re-embed one document!
### Ask Questions over New Data
[Section titled “Ask Questions over New Data”](https://developers.llamaindex.ai/python/examples/ingestion/ingestion_gdrive/#ask-questions-over-new-data)

```


query_engine = index.as_query_engine()


```


```


response = query_engine.query("What are the sub-types of question answering?")


```


```


print(str(response))


```


```

The sub-types of question answering mentioned in the context are semantic search, summarization, and structured analytics.

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


