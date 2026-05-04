[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/storing/vector_stores/#_top)
LlamaIndex Framework
Component Guides
Storing
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Vector Stores
Vector stores contain embedding vectors of ingested document chunks (and sometimes the document chunks as well).
## Simple Vector Store
[Section titled “Simple Vector Store”](https://developers.llamaindex.ai/python/framework/module_guides/storing/vector_stores/#simple-vector-store)
By default, LlamaIndex uses a simple in-memory vector store that’s great for quick experimentation. They can be persisted to (and loaded from) disk by calling `vector_store.persist()` (and `SimpleVectorStore.from_persist_path(...)` respectively).
## Vector Store Options & Feature Support
[Section titled “Vector Store Options & Feature Support”](https://developers.llamaindex.ai/python/framework/module_guides/storing/vector_stores/#vector-store-options--feature-support)
LlamaIndex supports over 20 different vector store options. We are actively adding more integrations and improving feature coverage for each.  
| Vector Store  | Type  | Metadata Filtering  | Hybrid Search  | Delete  | Store Documents  | Async  |  
| --- | --- | --- | --- | --- | --- | --- |  
| Alibaba Cloud OpenSearch  | cloud  | ✓  | ✓  | ✓  | ✓  |  
| Apache Cassandra®  | self-hosted / cloud  | ✓  | ✓  | ✓  |  
| Astra DB  | cloud  | ✓  | ✓  | ✓  |  
| Azure AI Search  | cloud  | ✓  | ✓  | ✓  | ✓  |  
| Azure CosmosDB Mongo vCore  | cloud  | ✓  | ✓  |  
| Azure CosmosDB NoSql  | cloud  | ✓  | ✓  |  
| BaiduVectorDB  | cloud  | ✓  | ✓  | ✓  |  
| ChatGPT Retrieval Plugin  | aggregator  | ✓  | ✓  |  
| Chroma  | self-hosted  | ✓  | ✓  | ✓  |  
| Couchbase  | self-hosted / cloud  | ✓  | ✓  | ✓  | ✓  |  
| DashVector  | cloud  | ✓  | ✓  | ✓  | ✓  |  
| Databricks  | cloud  | ✓  | ✓  | ✓  |  
| Deeplake  | self-hosted / cloud  | ✓  | ✓  | ✓  |  
| DocArray  | aggregator  | ✓  | ✓  | ✓  |  
| DuckDB  | in-memory / self-hosted  | ✓  | ✓  | ✓  |  
| DynamoDB  | cloud  | ✓  |  
| Elasticsearch  | self-hosted / cloud  | ✓  | ✓  | ✓  | ✓  | ✓  |  
| FAISS  | in-memory  |  
| Google AlloyDB  | cloud  | ✓  | ✓  | ✓  | ✓  |  
| Google Cloud SQL Postgres  | cloud  | ✓  | ✓  | ✓  | ✓  |  
| Hnswlib  | in-memory  |  
| txtai  | in-memory  |  
| Jaguar  | self-hosted / cloud  | ✓  | ✓  | ✓  | ✓  |  
| LanceDB  | cloud  | ✓  | ✓  | ✓  |  
| Lantern  | self-hosted / cloud  | ✓  | ✓  | ✓  | ✓  | ✓  |  
| MongoDB Atlas  | self-hosted / cloud  | ✓  | ✓  | ✓  | ✓  |  
| MyScale  | cloud  | ✓  | ✓  | ✓  | ✓  |  
| Milvus / Zilliz  | self-hosted / cloud  | ✓  | ✓  | ✓  | ✓  |  
| Neo4jVector  | self-hosted / cloud  | ✓  | ✓  | ✓  |  
| OpenSearch  | self-hosted / cloud  | ✓  | ✓  | ✓  | ✓  | ✓  |  
| Pinecone  | cloud  | ✓  | ✓  | ✓  | ✓  |  
| Postgres  | self-hosted / cloud  | ✓  | ✓  | ✓  | ✓  | ✓  |  
| pgvecto.rs  | self-hosted / cloud  | ✓  | ✓  | ✓  | ✓  |  
| Qdrant  | self-hosted / cloud  | ✓  | ✓  | ✓  | ✓  | ✓  |  
| Redis  | self-hosted / cloud  | ✓  | ✓  | ✓  |  
| S3  | cloud  | ✓  | ✓  | ✓  | ✓* (using asyncio.to_thread)  |  
| Simple  | in-memory  | ✓  | ✓  |  
| SingleStore  | self-hosted / cloud  | ✓  | ✓  | ✓  |  
| Supabase  | self-hosted / cloud  | ✓  | ✓  | ✓  |  
| Tablestore  | cloud  | ✓  | ✓  | ✓  | ✓  |  
| Tair  | cloud  | ✓  | ✓  | ✓  |  
| TiDB  | cloud  | ✓  | ✓  | ✓  |  
| TencentVectorDB  | cloud  | ✓  | ✓  | ✓  | ✓  |  
| Timescale  | ✓  | ✓  | ✓  | ✓  |  
| Typesense  | self-hosted / cloud  | ✓  | ✓  | ✓  |  
| Upstash  | cloud  | ✓  |  
| VectorX DB  | cloud  | ✓  | ✓  | ✓  | ✓  | ✓  |  
| Vearch  | self-hosted  | ✓  | ✓  | ✓  |  
| Vespa  | self-hosted / cloud  | ✓  | ✓  | ✓  | ✓  |  
| Vertex AI Vector Search  | cloud  | ✓  | ✓  | ✓  |  
| Weaviate  | self-hosted / cloud  | ✓  | ✓  | ✓  | ✓  |  
| WordLift  | cloud  | ✓  | ✓  | ✓  | ✓  | ✓  |  
For more details, see [Vector Store Integrations](https://developers.llamaindex.ai/python/framework/community/integrations/vector_stores).
## Example Notebooks
[Section titled “Example Notebooks”](https://developers.llamaindex.ai/python/framework/module_guides/storing/vector_stores/#example-notebooks)
  * [Alibaba Cloud OpenSearch](https://developers.llamaindex.ai/python/examples/vector_stores/alibabacloudopensearchindexdemo)
  * [Async Index Creation](https://developers.llamaindex.ai/python/examples/vector_stores/asyncindexcreationdemo)
  * [Azure Cosmos DB Mongo vCore](https://developers.llamaindex.ai/python/examples/vector_stores/azurecosmosdbmongodbvcoredemo)
  * [Azure Cosmos DB NoSql](https://developers.llamaindex.ai/python/examples/vector_stores/azurecosmosdbnosqldemo)
  * [Google AlloyDB for PostgreSQL](https://developers.llamaindex.ai/python/examples/vector_stores/alloydbvectorstoredemo)
  * [Google Cloud SQL for PostgreSQL](https://developers.llamaindex.ai/python/examples/vector_stores/cloudsqlpgvectorstoredemo)
  * [Milvus Full-Text Search](https://developers.llamaindex.ai/python/examples/vector_stores/milvusfulltextsearchdemo)
  * [Milvus Hybrid Search](https://developers.llamaindex.ai/python/examples/vector_stores/milvushybridindexdemo)
  * [Pinecone Hybrid Search](https://developers.llamaindex.ai/python/examples/vector_stores/pineconeindexdemo-hybrid)
  * [Qdrant Hybrid Search](https://developers.llamaindex.ai/python/examples/vector_stores/qdrant_hybrid)
  * [Vertex AI Vector Search](https://developers.llamaindex.ai/python/examples/vector_stores/vertexaivectorsearchdemo)
  * [Weaviate Hybrid Search](https://developers.llamaindex.ai/python/examples/vector_stores/weaviateindexdemo-hybrid)


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


