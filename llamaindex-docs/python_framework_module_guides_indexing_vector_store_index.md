[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/indexing/vector_store_index/#_top)
LlamaIndex Framework
Component Guides
Indexing
[Using VectorStoreIndex](https://developers.llamaindex.ai/python/framework/module_guides/indexing/vector_store_index/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Using VectorStoreIndex
Vector Stores are a key component of retrieval-augmented generation (RAG) and so you will end up using them in nearly every application you make using LlamaIndex, either directly or indirectly.
Vector stores accept a list of [`Node` objects](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes) and build an index from them
## Loading data into the index
[Section titled “Loading data into the index”](https://developers.llamaindex.ai/python/framework/module_guides/indexing/vector_store_index/#loading-data-into-the-index)
### Basic usage
[Section titled “Basic usage”](https://developers.llamaindex.ai/python/framework/module_guides/indexing/vector_store_index/#basic-usage)
The simplest way to use a Vector Store is to load a set of documents and build an index from them using `from_documents`:

```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader




# Load documents and build index



documents = SimpleDirectoryReader(




"../../examples/data/paul_graham"



).load_data()



index = VectorStoreIndex.from_documents(documents)


```

When you use `from_documents`, your Documents are split into chunks and parsed into [`Node` objects](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes), lightweight abstractions over text strings that keep track of metadata and relationships.
For more on how to load documents, see [Understanding Loading](https://developers.llamaindex.ai/python/framework/module_guides/loading).
By default, VectorStoreIndex stores everything in memory. See [Using Vector Stores](https://developers.llamaindex.ai/python/framework/module_guides/indexing/vector_store_index/#using-vector-stores) below for more on how to use persistent vector stores.
This is especially helpful when you are inserting into a remotely hosted vector database.
### Using the ingestion pipeline to create nodes
[Section titled “Using the ingestion pipeline to create nodes”](https://developers.llamaindex.ai/python/framework/module_guides/indexing/vector_store_index/#using-the-ingestion-pipeline-to-create-nodes)
If you want more control over how your documents are indexed, we recommend using the ingestion pipeline. This allows you to customize the chunking, metadata, and embedding of the nodes.

```


from llama_index.core import Document




from llama_index.embeddings.openai import OpenAIEmbedding




from llama_index.core.node_parser import SentenceSplitter




from llama_index.core.extractors import TitleExtractor




from llama_index.core.ingestion import IngestionPipeline, IngestionCache




# create the pipeline with transformations



pipeline = IngestionPipeline(




transformations=[




SentenceSplitter(chunk_size=25, chunk_overlap=0),




TitleExtractor(),




OpenAIEmbedding(),






# run the pipeline



nodes = pipeline.run(documents=[Document.example()])


```

### Creating and managing nodes directly
[Section titled “Creating and managing nodes directly”](https://developers.llamaindex.ai/python/framework/module_guides/indexing/vector_store_index/#creating-and-managing-nodes-directly)
If you want total control over your index you can [create and define nodes manually](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_nodes) and pass them directly to the index constructor:

```


from llama_index.core.schema import TextNode





node1 = TextNode(text="<text_chunk>", id_="<node_id>")




node2 = TextNode(text="<text_chunk>", id_="<node_id>")




nodes = [node1, node2]




index = VectorStoreIndex(nodes)


```

#### Handling Document Updates
[Section titled “Handling Document Updates”](https://developers.llamaindex.ai/python/framework/module_guides/indexing/vector_store_index/#handling-document-updates)
When managing your index directly, you will want to deal with data sources that change over time. `Index` classes have **insertion** , **deletion** , **update** , and **refresh** operations and you can learn more about them below:
  * [Metadata Extraction](https://developers.llamaindex.ai/python/framework/module_guides/indexing/metadata_extraction)
  * [Document Management](https://developers.llamaindex.ai/python/framework/module_guides/indexing/document_management)


## Storing the vector index
[Section titled “Storing the vector index”](https://developers.llamaindex.ai/python/framework/module_guides/indexing/vector_store_index/#storing-the-vector-index)
LlamaIndex supports [dozens of vector stores](https://developers.llamaindex.ai/python/framework/module_guides/storing/vector_stores). You can specify which one to use by passing in a `StorageContext`, on which in turn you specify the `vector_store` argument, as in this example using Pinecone:

```


import pinecone




from llama_index.core import (




VectorStoreIndex,




SimpleDirectoryReader,




StorageContext,





from llama_index.vector_stores.pinecone import PineconeVectorStore




# init pinecone



pinecone.init(api_key="<api_key>", environment="<environment>")



pinecone.create_index(



"quickstart", dimension=1536, metric="euclidean", pod_type="p1"





# construct vector store and customize storage context



storage_context = StorageContext.from_defaults(




vector_store=PineconeVectorStore(pinecone.Index("quickstart"))





# Load documents and build index



documents = SimpleDirectoryReader(




"../../examples/data/paul_graham"



).load_data()



index = VectorStoreIndex.from_documents(




documents, storage_context=storage_context



```

For more examples of how to use VectorStoreIndex, see our [vector store index usage examples notebook](https://developers.llamaindex.ai/python/framework/module_guides/indexing/vector_store_guide).
For examples of how to use VectorStoreIndex with specific vector stores, check out [vector stores](https://developers.llamaindex.ai/python/framework/module_guides/storing/vector_stores) under the Storing section.
## Composable Retrieval
[Section titled “Composable Retrieval”](https://developers.llamaindex.ai/python/framework/module_guides/indexing/vector_store_index/#composable-retrieval)
The `VectorStoreIndex` (and any other index/retriever) is capable of retrieving generic objects, including
  * references to nodes
  * query engines
  * retrievers
  * query pipelines


If these objects are retrieved, they will be automatically ran using the provided query.
For example:

```


from llama_index.core.schema import IndexNode





query_engine = other_index.as_query_engine




obj = IndexNode(




text="A query engine describing X, Y, and Z.",




obj=query_engine,




index_id="my_query_engine",






index = VectorStoreIndex(nodes=nodes, objects=[obj])




retriever = index.as_retriever(verbose=True)


```

If the index node containing the query engine is retrieved, the query engine will be ran and the resulting response returned as a node.
For more details, checkout [the guide](https://developers.llamaindex.ai/python/examples/retrievers/composable_retrievers)
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


