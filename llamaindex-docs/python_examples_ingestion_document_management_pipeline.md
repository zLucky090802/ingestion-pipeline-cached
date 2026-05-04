[Skip to content](https://developers.llamaindex.ai/python/examples/ingestion/document_management_pipeline/#_top)
# Ingestion Pipeline + Document Management 
Attaching a `docstore` to the ingestion pipeline will enable document management.
Using the `document.doc_id` or `node.ref_doc_id` as a grounding point, the ingestion pipeline will actively look for duplicate documents.
It works by
  * Storing a map of `doc_id` -> `document_hash`
  * If a duplicate `doc_id` is detected, and the hash has changed, the document will be re-processed
  * If the hash has not changed, the document will be skipped in the pipeline


If we do not attach a vector store, we can only check for and remove duplicate inputs.
If a vector store is attached, we can also handle upserts! We have [another guide](https://developers.llamaindex.ai/en/stable/examples/ingestion/redis_ingestion_pipeline) for upserts and vector stores.
## Create Seed Data
[Section titled “Create Seed Data”](https://developers.llamaindex.ai/python/examples/ingestion/document_management_pipeline/#create-seed-data)

```


%pip install llama-index-storage-docstore-redis




%pip install llama-index-storage-docstore-mongodb




%pip install llama-index-embeddings-huggingface


```


```

# Make some test data



!mkdir -p data




!echo "This is a test file: one!" data/test1.txt




!echo "This is a test file: two!" data/test2.txt


```


```


from llama_index.core import SimpleDirectoryReader




# load documents with deterministic IDs



documents = SimpleDirectoryReader("./data", filename_as_id=True).load_data()


```


```

/home/loganm/.cache/pypoetry/virtualenvs/llama-index-4a-wkI5X-py3.11/lib/python3.11/site-packages/deeplake/util/check_latest_version.py:32: UserWarning: A newer version of deeplake (3.8.9) is available. It's recommended that you update to the latest version using `pip install -U deeplake`.



warnings.warn(


```

## Create Pipeline with Document Store
[Section titled “Create Pipeline with Document Store”](https://developers.llamaindex.ai/python/examples/ingestion/document_management_pipeline/#create-pipeline-with-document-store)

```


from llama_index.embeddings.huggingface import HuggingFaceEmbedding




from llama_index.core.ingestion import IngestionPipeline




from llama_index.core.storage.docstore import SimpleDocumentStore




from llama_index.storage.docstore.redis import RedisDocumentStore




from llama_index.storage.docstore.mongodb import MongoDocumentStore




from llama_index.core.node_parser import SentenceSplitter






pipeline = IngestionPipeline(




transformations=[




SentenceSplitter(),




HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5"),





docstore=SimpleDocumentStore(),



```


```


nodes = pipeline.run(documents=documents)


```


```

Docstore strategy set to upserts, but no vector store. Switching to duplicates_only strategy.

```


```


print(f"Ingested {len(nodes)} Nodes")


```


```

Ingested 2 Nodes

```

### [Optional] Save/Load Pipeline
[Section titled “[Optional] Save/Load Pipeline”](https://developers.llamaindex.ai/python/examples/ingestion/document_management_pipeline/#optional-saveload-pipeline)
Saving the pipeline will save both the internal cache and docstore.
**NOTE:** If you were using remote caches/docstores, this step is not needed

```


pipeline.persist("./pipeline_storage")


```


```


pipeline = IngestionPipeline(




transformations=[




SentenceSplitter(),




HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5"),






# restore the pipeline



pipeline.load("./pipeline_storage")


```

## Test the Document Management
[Section titled “Test the Document Management”](https://developers.llamaindex.ai/python/examples/ingestion/document_management_pipeline/#test-the-document-management)
Here, we can create a new document, as well as edit an existing document, to test the document management.
Both the new document and edited document will be ingested, while the unchanged document will be skipped

```


!echo "This is a test file: three!" data/test3.txt




!echo "This is a NEW test file: one!" data/test1.txt


```


```


documents = SimpleDirectoryReader("./data", filename_as_id=True).load_data()


```


```


nodes = pipeline.run(documents=documents)


```


```

Docstore strategy set to upserts, but no vector store. Switching to duplicates_only strategy.

```


```


print(f"Ingested {len(nodes)} Nodes")


```


```

Ingested 2 Nodes

```

Lets confirm which nodes were ingested:

```


for node in nodes:




print(f"Node: {node.text}")


```


```

Node: This is a NEW test file: one!


Node: This is a test file: three!

```

We can also verify the docstore has only three documents tracked

```


print(len(pipeline.docstore.docs))


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


