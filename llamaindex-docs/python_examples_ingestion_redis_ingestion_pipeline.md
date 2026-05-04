[Skip to content](https://developers.llamaindex.ai/python/examples/ingestion/redis_ingestion_pipeline/#_top)
# Redis Ingestion Pipeline 
This walkthrough shows how to use Redis for both the vector store, cache, and docstore in an Ingestion Pipeline.
## Dependencies
[Section titled “Dependencies”](https://developers.llamaindex.ai/python/examples/ingestion/redis_ingestion_pipeline/#dependencies)
Install and start redis, setup OpenAI API key

```


%pip install llama-index-storage-docstore-redis




%pip install llama-index-vector-stores-redis




%pip install llama-index-embeddings-huggingface


```


```


!docker run -d --name redis-stack -p 6379:6379-p 8001:8001 redis/redis-stack:latest


```


```

338c889086e8649aa80dfb79ebff4fffc98d72fc6d988ac158c6662e9e0cf04b

```


```


import os





os.environ["OPENAI_API_KEY"] ="sk-..."




os.environ["TOKENIZERS_PARALLELISM"] ="false"


```

## Create Seed Data
[Section titled “Create Seed Data”](https://developers.llamaindex.ai/python/examples/ingestion/redis_ingestion_pipeline/#create-seed-data)

```

# Make some test data



!rm -rf test_redis_data




!mkdir -p test_redis_data




!echo "This is a test file: one!" test_redis_data/test1.txt




!echo "This is a test file: two!" test_redis_data/test2.txt


```


```


from llama_index.core import SimpleDirectoryReader




# load documents with deterministic IDs



documents = SimpleDirectoryReader(




"./test_redis_data", filename_as_id=True



).load_data()

```

## Run the Redis-Based Ingestion Pipeline
[Section titled “Run the Redis-Based Ingestion Pipeline”](https://developers.llamaindex.ai/python/examples/ingestion/redis_ingestion_pipeline/#run-the-redis-based-ingestion-pipeline)
With a vector store attached, the pipeline will handle upserting data into your vector store.
However, if you only want to handle duplcates, you can change the strategy to `DUPLICATES_ONLY`.

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






embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")





custom_schema = IndexSchema.from_dict(





"index": {"name": "redis_vector_store", "prefix": "doc"},




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







```


```


pipeline = IngestionPipeline(




transformations=[




SentenceSplitter(),




embed_model,





docstore=RedisDocumentStore.from_host_and_port(




"localhost", 6379, namespace="document_store"





vector_store=RedisVectorStore(




schema=custom_schema,




redis_url="redis://localhost:6379",





cache=IngestionCache(




cache=RedisCache.from_host_and_port("localhost", 6379),




collection="redis_cache",





docstore_strategy=DocstoreStrategy.UPSERTS,



```


```


nodes = pipeline.run(documents=documents)




print(f"Ingested {len(nodes)} Nodes")


```


```

Ingested 2 Nodes

```

## Confirm documents are ingested
[Section titled “Confirm documents are ingested”](https://developers.llamaindex.ai/python/examples/ingestion/redis_ingestion_pipeline/#confirm-documents-are-ingested)
We can create a vector index using our vector store, and quickly ask which documents are seen.

```


from llama_index.core import VectorStoreIndex





index = VectorStoreIndex.from_vector_store(




pipeline.vector_store, embed_model=embed_model



```


```


print(




index.as_query_engine(similarity_top_k=10).query(




"What documents do you see?"




```


```

I see two documents.

```

## Add data and Ingest
[Section titled “Add data and Ingest”](https://developers.llamaindex.ai/python/examples/ingestion/redis_ingestion_pipeline/#add-data-and-ingest)
Here, we can update an existing file, as well as add a new one!

```


!echo "This is a test file: three!" test_redis_data/test3.txt




!echo "This is a NEW test file: one!" test_redis_data/test1.txt


```


```


documents = SimpleDirectoryReader(




"./test_redis_data", filename_as_id=True



).load_data()




nodes = pipeline.run(documents=documents)





print(f"Ingested {len(nodes)} Nodes")


```


```

13:32:07 redisvl.index.index INFO   Index already exists, not overwriting.


Ingested 2 Nodes

```


```


index = VectorStoreIndex.from_vector_store(




pipeline.vector_store, embed_model=embed_model






response = index.as_query_engine(similarity_top_k=10).query(




"What documents do you see?"






print(response)





for node in response.source_nodes:




print(node.get_text())


```


```

You see three documents: test3.txt, test1.txt, and test2.txt.


This is a test file: three!


This is a NEW test file: one!


This is a test file: two!

```

As we can see, the data was deduplicated and upserted correctly! Only three nodes are in the index, even though we ran the full pipeline twice.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


