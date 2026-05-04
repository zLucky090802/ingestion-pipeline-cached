[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/rocksetindexdemo/#_top)
LlamaIndex Framework
Integrations
Vector stores
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Rockset Vector Store 
As a real-time search and analytics database, Rockset uses indexing to deliver scalable and performant personalization, product search, semantic search, chatbot applications, and more. Since Rockset is purpose-built for real-time, you can build these responsive applications on constantly updating, streaming data. By integrating Rockset with LlamaIndex, you can easily use LLMs on your own real-time data for production-ready vector search applications.
We’ll walk through a demonstration of how to use Rockset as a vector store in LlamaIndex.
## Tutorial
[Section titled “Tutorial”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/rocksetindexdemo/#tutorial)
In this example, we’ll use OpenAI’s `text-embedding-ada-002` model to generate embeddings and Rockset as vector store to store embeddings. We’ll ingest text from a file and ask questions about the content.
### Setting Up Your Environment
[Section titled “Setting Up Your Environment”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/rocksetindexdemo/#setting-up-your-environment)
  1. Create a [collection](https://rockset.com/docs/collections) from the Rockset console with the [Write API](https://rockset.com/docs/write-api/) as your source. Name your collection `llamaindex_demo`. Configure the following [ingest transformation](https://rockset.com/docs/ingest-transformation) with [`VECTOR_ENFORCE`](https://rockset.com/docs/vector-functions) to define your embeddings field and take advantage of performance and storage optimizations:



```

SELECT



_input.*EXCEPT(_meta),




VECTOR_ENFORCE(




_input.embedding,




1536,




'float'




) as embedding




FROM _input


```

  1. Create an [API key](https://rockset.com/docs/iam) from the Rockset console and set the `ROCKSET_API_KEY` environment variable. Find your API server [here](http://rockset.com/docs/rest-api#introduction) and set the `ROCKSET_API_SERVER` environment variable. Set the `OPENAI_API_KEY` environment variable.
  2. Install the dependencies.


Terminal window
```


pip3installllama_indexrockset


```

  1. LlamaIndex allows you to ingest data from a variety of sources. For this example, we’ll read from a text file named `constitution.txt`, which is a transcript of the American Constitution, found [here](https://www.archives.gov/founding-docs/constitution-transcript).


### Data ingestion
[Section titled “Data ingestion”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/rocksetindexdemo/#data-ingestion)
Use LlamaIndex’s `SimpleDirectoryReader` class to convert the text file to a list of `Document` objects.

```


%pip install llama-index-llms-openai




%pip install llama-index-vector-stores-rocksetdb


```


```


from llama_index.core import SimpleDirectoryReader





docs = SimpleDirectoryReader(




input_files=["{path to}/consitution.txt"]



).load_data()

```

Instantiate the LLM and service context.

```


from llama_index.core import Settings




from llama_index.llms.openai import OpenAI





Settings.llm = OpenAI(temperature=0.8, model="gpt-3.5-turbo")


```

Instantiate the vector store and storage context.

```


from llama_index.core import StorageContext




from llama_index.vector_stores.rocksetdb import RocksetVectorStore





vector_store = RocksetVectorStore(collection="llamaindex_demo")




storage_context = StorageContext.from_defaults(vector_store=vector_store)


```

Add documents to the `llamaindex_demo` collection and create an index.

```


from llama_index.core import VectorStoreIndex





index = VectorStoreIndex.from_documents(




docs,




storage_context=storage_context,



```

### Querying
[Section titled “Querying”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/rocksetindexdemo/#querying)
Ask a question about your document and generate a response.

```


response = index.as_query_engine().query("What is the duty of the president?")





print(str(response))


```

Run the program.

```

$ python3 main.py


The duty of the president is to faithfully execute the Office of President of the United States, preserve, protect and defend the Constitution of the United States, serve as the Commander in Chief of the Army and Navy, grant reprieves and pardons for offenses against the United States (except in cases of impeachment), make treaties and appoint ambassadors and other public ministers, take care that the laws be faithfully executed, and commission all the officers of the United States.

```

## Metadata Filtering
[Section titled “Metadata Filtering”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/rocksetindexdemo/#metadata-filtering)
Metadata filtering allows you to retrieve relevant documents that match specific filters.
  1. Add nodes to your vector store and create an index.



```


from llama_index.vector_stores.rocksetdb import RocksetVectorStore




from llama_index.core import VectorStoreIndex, StorageContext




from llama_index.core.vector_stores.types import NodeWithEmbedding




from llama_index.core.schema import TextNode





nodes = [




NodeWithEmbedding(




node=TextNode(




text="Apples are blue",




metadata={"type": "fruit"},





embedding=[],






index = VectorStoreIndex(




nodes,




storage_context=StorageContext.from_defaults(




vector_store=RocksetVectorStore(collection="llamaindex_demo")




```

  1. Define metadata filters.



```


from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters





filters = MetadataFilters(




filters=[ExactMatchFilter(key="type", value="fruit")]



```

  1. Retrieve relevant documents that satisfy the filters.



```


retriever = index.as_retriever(filters=filters)




retriever.retrieve("What colors are apples?")


```

## Creating an Index from an Existing Collection
[Section titled “Creating an Index from an Existing Collection”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/rocksetindexdemo/#creating-an-index-from-an-existing-collection)
You can create indices with data from existing collections.

```


from llama_index.core import VectorStoreIndex




from llama_index.vector_stores.rocksetdb import RocksetVectorStore





vector_store = RocksetVectorStore(collection="llamaindex_demo")





index = VectorStoreIndex.from_vector_store(vector_store)


```

## Creating an Index from a New Collection
[Section titled “Creating an Index from a New Collection”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/rocksetindexdemo/#creating-an-index-from-a-new-collection)
You can also create a new Rockset collection to use as a vector store.

```


from llama_index.vector_stores.rocksetdb import RocksetVectorStore





vector_store = RocksetVectorStore.with_new_collection(




collection="llamaindex_demo"# name of new collection




dimensions=1536# specifies length of vectors in ingest tranformation (optional)




# other RocksetVectorStore args






index = VectorStoreIndex(




nodes,




storage_context=StorageContext.from_defaults(vector_store=vector_store),



```

## Configuration
[Section titled “Configuration”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/rocksetindexdemo/#configuration)
  * **collection** : Name of the collection to query (required).



```


RocksetVectorStore(collection="my_collection")


```

  * **workspace** : Name of the workspace containing the collection. Defaults to `"commons"`.



```


RocksetVectorStore(worksapce="my_workspace")


```

  * **api_key** : The API key to use to authenticate Rockset requests. Ignored if `client` is passed in. Defaults to the `ROCKSET_API_KEY` environment variable.



```


RocksetVectorStore(api_key="<my key>")


```

  * **api_server** : The API server to use for Rockset requests. Ignored if `client` is passed in. Defaults to the `ROCKSET_API_KEY` environment variable or `"https://api.use1a1.rockset.com"` if the `ROCKSET_API_SERVER` is not set.



```


from rockset import Regions




RocksetVectorStore(api_server=Regions.euc1a1)


```

  * **client** : Rockset client object to use to execute Rockset requests. If not specified, a client object is internally constructed with the `api_key` parameter (or `ROCKSET_API_SERVER` environment variable) and the `api_server` parameter (or `ROCKSET_API_SERVER` environment variable).



```


from rockset import RocksetClient




RocksetVectorStore(client=RocksetClient(api_key="<my key>"))


```

  * **embedding_col** : The name of the database field containing embeddings. Defaults to `"embedding"`.



```


RocksetVectorStore(embedding_col="my_embedding")


```

  * **metadata_col** : The name of the database field containing node data. Defaults to `"metadata"`.



```


RocksetVectorStore(metadata_col="node")


```

  * **distance_func** : The metric to measure vector relationship. Defaults to cosine similarity.



```


RocksetVectorStore(distance_func=RocksetVectorStore.DistanceFunc.DOT_PRODUCT)


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


