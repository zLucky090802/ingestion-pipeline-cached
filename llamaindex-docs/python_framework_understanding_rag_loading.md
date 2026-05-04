[Skip to content](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/#_top)
LlamaIndex Framework
Learn
Building a RAG pipeline
Loading
[Loading Data (Ingestion)](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Loading Data (Ingestion)
Before your chosen LLM can act on your data, you first need to process the data and load it. This has parallels to data cleaning/feature engineering pipelines in the ML world, or ETL pipelines in the traditional data setting.
This ingestion pipeline typically consists of three main stages:
  1. Load the data
  2. Transform the data
  3. Index and store the data


We cover indexing/storage in [future](https://developers.llamaindex.ai/python/framework/understanding/rag/indexing) [sections](https://developers.llamaindex.ai/python/framework/understanding/rag/storing). In this guide we’ll mostly talk about loaders and transformations.
## Loaders
[Section titled “Loaders”](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/#loaders)
Before your chosen LLM can act on your data you need to load it. The way LlamaIndex does this is via data connectors, also called `Reader`. Data connectors ingest data from different data sources and format the data into `Document` objects. A `Document` is a collection of data (currently text, and in future, images and audio) and metadata about that data.
### Loading using SimpleDirectoryReader
[Section titled “Loading using SimpleDirectoryReader”](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/#loading-using-simpledirectoryreader)
The easiest reader to use is our SimpleDirectoryReader, which creates documents out of every file in a given directory. It is built in to LlamaIndex and can read a variety of formats including Markdown, PDFs, Word documents, PowerPoint decks, images, audio and video.

```


from llama_index.core import SimpleDirectoryReader





documents = SimpleDirectoryReader("./data").load_data()


```

### Using Readers from LlamaHub
[Section titled “Using Readers from LlamaHub”](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/#using-readers-from-llamahub)
Because there are so many possible places to get data, they are not all built-in. Instead, you download them from our registry of data connectors, [LlamaHub](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/llamahub).
In this example LlamaIndex downloads and installs the connector called [DatabaseReader](https://llamahub.ai/l/readers/llama-index-readers-database), which runs a query against a SQL database and returns every row of the results as a `Document`:

```


from llama_index.core import download_loader





from llama_index.readers.database import DatabaseReader





reader = DatabaseReader(




scheme=os.getenv("DB_SCHEME"),




host=os.getenv("DB_HOST"),




port=os.getenv("DB_PORT"),




user=os.getenv("DB_USER"),




password=os.getenv("DB_PASS"),




dbname=os.getenv("DB_NAME"),






query ="SELECT * FROM users"




documents = reader.load_data(query=query)


```

There are hundreds of connectors to use on [LlamaHub](https://llamahub.ai)!
### Creating Documents directly
[Section titled “Creating Documents directly”](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/#creating-documents-directly)
Instead of using a loader, you can also use a Document directly.

```


from llama_index.core import Document





doc = Document(text="text")


```

## Transformations
[Section titled “Transformations”](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/#transformations)
After the data is loaded, you then need to process and transform your data before putting it into a storage system. These transformations include chunking, extracting metadata, and embedding each chunk. This is necessary to make sure that the data can be retrieved, and used optimally by the LLM.
Transformation input/outputs are `Node` objects (a `Document` is a subclass of a `Node`). Transformations can also be stacked and reordered.
We have both a high-level and lower-level API for transforming documents.
### High-Level Transformation API
[Section titled “High-Level Transformation API”](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/#high-level-transformation-api)
Indexes have a `.from_documents()` method which accepts an array of Document objects and will correctly parse and chunk them up. However, sometimes you will want greater control over how your documents are split up.

```


from llama_index.core import VectorStoreIndex





vector_index = VectorStoreIndex.from_documents(documents)



vector_index.as_query_engine()

```

Under the hood, this splits your Document into Node objects, which are similar to Documents (they contain text and metadata) but have a relationship to their parent Document.
If you want to customize core components, like the text splitter, through this abstraction you can pass in a custom `transformations` list or apply to the global `Settings`:

```


from llama_index.core.node_parser import SentenceSplitter





text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=10)




# global



from llama_index.core import Settings





Settings.text_splitter = text_splitter




# per-index



index = VectorStoreIndex.from_documents(




documents, transformations=[text_splitter]



```

### Lower-Level Transformation API
[Section titled “Lower-Level Transformation API”](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/#lower-level-transformation-api)
You can also define these steps explicitly.
You can do this by either using our transformation modules (text splitters, metadata extractors, etc.) as standalone components, or compose them in our declarative [Transformation Pipeline interface](https://developers.llamaindex.ai/python/framework/module_guides/loading/ingestion_pipeline).
Let’s walk through the steps below.
#### Splitting Your Documents into Nodes
[Section titled “Splitting Your Documents into Nodes”](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/#splitting-your-documents-into-nodes)
A key step to process your documents is to split them into “chunks”/Node objects. The key idea is to process your data into bite-sized pieces that can be retrieved / fed to the LLM.
LlamaIndex has support for a wide range of [text splitters](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules), ranging from paragraph/sentence/token based splitters to file-based splitters like HTML, JSON.
These can be [used on their own or as part of an ingestion pipeline](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers).

```


from llama_index.core import SimpleDirectoryReader




from llama_index.core.ingestion import IngestionPipeline




from llama_index.core.node_parser import TokenTextSplitter





documents = SimpleDirectoryReader("./data").load_data()





pipeline = IngestionPipeline(transformations=[TokenTextSplitter(), ...])





nodes = pipeline.run(documents=documents)


```

### Adding Metadata
[Section titled “Adding Metadata”](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/#adding-metadata)
You can also choose to add metadata to your documents and nodes. This can be done either manually or with [automatic metadata extractors](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_metadata_extractor).
Here are guides on 1) [how to customize Documents](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_documents), and 2) [how to customize Nodes](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_nodes).

```


document = Document(




text="text",




metadata={"filename": "<doc_file_name>", "category": "<category>"},



```

### Adding Embeddings
[Section titled “Adding Embeddings”](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/#adding-embeddings)
To insert a node into a vector index, it should have an embedding. See our [ingestion pipeline](https://developers.llamaindex.ai/python/framework/module_guides/loading/ingestion_pipeline) or our [embeddings guide](https://developers.llamaindex.ai/python/framework/module_guides/models/embeddings) for more details.
### Creating and passing Nodes directly
[Section titled “Creating and passing Nodes directly”](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/#creating-and-passing-nodes-directly)
If you want to, you can create nodes directly and pass a list of Nodes directly to an indexer:

```


from llama_index.core.schema import TextNode





node1 = TextNode(text="<text_chunk>", id_="<node_id>")




node2 = TextNode(text="<text_chunk>", id_="<node_id>")





index = VectorStoreIndex([node1, node2])


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


