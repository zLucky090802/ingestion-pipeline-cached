[Skip to content](https://developers.llamaindex.ai/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval/#_top)
# Structured Hierarchical Retrieval 
Doing RAG well over multiple documents is hard. A general framework is given a user query, first select the relevant documents before selecting the content inside.
But selecting the documents can be tough - how can we dynamically select documents based on different properties depending on the user query?
In this notebook we show you our multi-document RAG architecture:
  * Represent each document as a concise **metadata** dictionary containing different properties: an extracted summary along with structured metadata.
  * Store this metadata dictionary as filters within a vector database.
  * Given a user query, first do **auto-retrieval** - infer the relevant semantic query and the set of filters to query this data (effectively combining text-to-SQL and semantic search).



```


%pip install llama-index-readers-github




%pip install llama-index-vector-stores-weaviate




%pip install llama-index-llms-openai


```


```


!pip install llama-index llama-hub


```

## Setup and Download Data
[Section titled “Setup and Download Data”](https://developers.llamaindex.ai/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval/#setup-and-download-data)
In this section, we’ll load in LlamaIndex Github issues.

```


import nest_asyncio




nest_asyncio.apply()

```


```


import os





os.environ["GITHUB_TOKEN"] ="ghp_..."




os.environ["OPENAI_API_KEY"] ="sk-..."


```


```


import os





from llama_index.readers.github import (




GitHubRepositoryIssuesReader,




GitHubIssuesClient,






github_client = GitHubIssuesClient()




loader = GitHubRepositoryIssuesReader(




github_client,




owner="run-llama",




repo="llama_index",




verbose=True,






orig_docs = loader.load_data()





limit =100





docs = []




for idx, doc inenumerate(orig_docs):




doc.metadata["index_id"] =int(doc.id_)




if idx >= limit:




break




docs.append(doc)


```


```

Found 100 issues in the repo page 1


Resulted in 100 documents


Found 100 issues in the repo page 2


Resulted in 200 documents


Found 100 issues in the repo page 3


Resulted in 300 documents


Found 64 issues in the repo page 4


Resulted in 364 documents


No more issues found, stopping

```

## Setup the Vector Store and Index
[Section titled “Setup the Vector Store and Index”](https://developers.llamaindex.ai/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval/#setup-the-vector-store-and-index)

```


import weaviate




# cloud



auth_config = weaviate.AuthApiKey(




api_key="XRa15cDIkYRT7AkrpqT6jLfE4wropK1c1TGk"





client = weaviate.Client(




"https://llama-index-test-v0oggsoz.weaviate.network",




auth_client_secret=auth_config,






class_name ="LlamaIndex_docs"


```


```

# optional: delete schema


client.schema.delete_class(class_name)

```


```


from llama_index.vector_stores.weaviate import WeaviateVectorStore




from llama_index.core import VectorStoreIndex, StorageContext





vector_store = WeaviateVectorStore(




weaviate_client=client, index_name=class_name





storage_context = StorageContext.from_defaults(vector_store=vector_store)


```


```


doc_index = VectorStoreIndex.from_documents(




docs, storage_context=storage_context



```

## Create IndexNodes for retrieval and filtering
[Section titled “Create IndexNodes for retrieval and filtering”](https://developers.llamaindex.ai/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval/#create-indexnodes-for-retrieval-and-filtering)

```


from llama_index.core import SummaryIndex




from llama_index.core.async_utils import run_jobs




from llama_index.llms.openai import OpenAI




from llama_index.core.schema import IndexNode




from llama_index.core.vector_stores import (




FilterOperator,




MetadataFilter,




MetadataFilters,







asyncdefaprocess_doc(doc, include_summary: bool=True):




"""Process doc."""




metadata = doc.metadata





date_tokens = metadata["created_at"].split("T")[0].split("-")




year =int(date_tokens[0])




month =int(date_tokens[1])




day =int(date_tokens[2])





assignee = (




""if"assignee"notin doc.metadata else doc.metadata["assignee"]





size =""




iflen(doc.metadata["labels"]) 0:




size_arr = [l forin doc.metadata["labels"] if"size:"in l]




size = size_arr[0].split(":")[1] iflen(size_arr) 0else""




new_metadata = {




"state": metadata["state"],




"year": year,




"month": month,




"day": day,




"assignee": assignee,




"size": size,






# now extract out summary




summary_index = SummaryIndex.from_documents([doc])




query_str ="Give a one-sentence concise summary of this issue."




query_engine = summary_index.as_query_engine(




llm=OpenAI(model="gpt-3.5-turbo")





summary_txt =await query_engine.aquery(query_str)




summary_txt =str(summary_txt)





index_id = doc.metadata["index_id"]




# filter for the specific doc id




filters = MetadataFilters(




filters=[




MetadataFilter(




key="index_id", operator=FilterOperator.EQ, value=int(index_id)








# create an index node using the summary text




index_node = IndexNode(




text=summary_txt,




metadata=new_metadata,




obj=doc_index.as_retriever(filters=filters),




index_id=doc.id_,






return index_node






asyncdefaprocess_docs(docs):




"""Process metadata on docs."""





index_nodes = []




tasks = []




for doc in docs:




task = aprocess_doc(doc)




tasks.append(task)





index_nodes =await run_jobs(tasks, show_progress=True, workers=3)





return index_nodes


```


```


index_nodes =await aprocess_docs(docs)


```


```


1%|          | 1/100 [00:00<00:55,  1.78it/s]/home/loganm/llama_index_proper/llama_index/.venv/lib/python3.11/site-packages/openai/_resource.py:38: ResourceWarning: unclosed <socket.socket fd=71, family=2, type=1, proto=6, laddr=('172.25.21.0', 40832), raddr=('104.18.7.192', 443)>




self._delete = client.delete



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=73 read=idle write=<idle, bufsize=0>>



_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=71 read=idle write=<idle, bufsize=0>>



_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback



12%|█▏        | 12/100 [00:04<00:31,  2.79it/s]/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=76 read=idle write=<idle, bufsize=0>>




_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=77 read=idle write=<idle, bufsize=0>>



_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=78 read=idle write=<idle, bufsize=0>>



_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/llama_index_proper/llama_index/.venv/lib/python3.11/site-packages/openai/resources/chat/completions.py:1337: ResourceWarning: unclosed <socket.socket fd=81, family=2, type=1, proto=6, laddr=('172.25.21.0', 40848), raddr=('104.18.7.192', 443)>



completions.create,



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=81 read=idle write=<idle, bufsize=0>>



_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=82 read=idle write=<idle, bufsize=0>>



_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=83 read=idle write=<idle, bufsize=0>>



_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=84 read=idle write=<idle, bufsize=0>>



_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback



21%|██        | 21/100 [00:06<00:22,  3.58it/s]/home/loganm/llama_index_proper/llama_index/.venv/lib/python3.11/site-packages/openai/_resource.py:34: ResourceWarning: unclosed <socket.socket fd=81, family=2, type=1, proto=6, laddr=('172.25.21.0', 40866), raddr=('104.18.7.192', 443)>




self._get = client.get



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/llama_index_proper/llama_index/.venv/lib/python3.11/site-packages/openai/_resource.py:34: ResourceWarning: unclosed <socket.socket fd=82, family=2, type=1, proto=6, laddr=('172.25.21.0', 40868), raddr=('104.18.7.192', 443)>



self._get = client.get



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=86 read=idle write=<idle, bufsize=0>>



_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback



38%|███▊      | 38/100 [00:12<00:24,  2.54it/s]/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=90 read=idle write=<idle, bufsize=0>>




_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=92 read=idle write=<idle, bufsize=0>>



_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/llama_index_proper/llama_index/.venv/lib/python3.11/site-packages/openai/_resource.py:34: ResourceWarning: unclosed <socket.socket fd=94, family=2, type=1, proto=6, laddr=('172.25.21.0', 40912), raddr=('104.18.7.192', 443)>



self._get = client.get



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=94 read=idle write=<idle, bufsize=0>>



_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback



50%|█████     | 50/100 [00:17<00:19,  2.51it/s]/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=95 read=idle write=<idle, bufsize=0>>




_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=96 read=idle write=<idle, bufsize=0>>



_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=97 read=idle write=<idle, bufsize=0>>



_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback



73%|███████▎  | 73/100 [00:24<00:07,  3.42it/s]/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=101 read=idle write=<idle, bufsize=0>>




_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=102 read=idle write=<idle, bufsize=0>>



_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback



82%|████████▏ | 82/100 [00:27<00:06,  2.94it/s]/home/loganm/miniconda3/envs/llama_index/lib/python3.11/functools.py:76: ResourceWarning: unclosed <socket.socket fd=102, family=2, type=1, proto=6, laddr=('172.25.21.0', 40998), raddr=('104.18.7.192', 443)>




return partial(update_wrapper, wrapped=wrapped,



ResourceWarning: Enable tracemalloc to get the object allocation traceback



92%|█████████▏| 92/100 [00:32<00:03,  2.15it/s]/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=106 read=idle write=<idle, bufsize=0>>




_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback


/home/loganm/miniconda3/envs/llama_index/lib/python3.11/asyncio/selector_events.py:835: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=111 read=idle write=<idle, bufsize=0>>



_warn(f"unclosed transport {self!r}", ResourceWarning, source=self)



ResourceWarning: Enable tracemalloc to get the object allocation traceback


100%|██████████| 100/100 [00:36<00:00,  2.71it/s]

```


```


index_nodes[5].metadata


```


```

{'state': 'open',



'year': 2024,




'month': 1,




'day': 13,




'assignee': '',




'size': 'XL'}


```

## Create the Top-Level AutoRetriever
[Section titled “Create the Top-Level AutoRetriever”](https://developers.llamaindex.ai/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval/#create-the-top-level-autoretriever)
We load both the summarized metadata as well as the original docs into the vector database.
  1. **Summarized Metadata** : This goes into the `LlamaIndex_auto` collection.
  2. **Original Docs** : This goes into the `LlamaIndex_docs` collection.


By storing both the summarized metadata as well as the original documents, we can execute our structured, hierarchical retrieval strategies.
We load into a vector database that supports auto-retrieval.
### Load Summarized Metadata
[Section titled “Load Summarized Metadata”](https://developers.llamaindex.ai/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval/#load-summarized-metadata)
This goes into `LlamaIndex_auto`

```


import weaviate




# cloud



auth_config = weaviate.AuthApiKey(




api_key="XRa15cDIkYRT7AkrpqT6jLfE4wropK1c1TGk"





client = weaviate.Client(




"https://llama-index-test-v0oggsoz.weaviate.network",




auth_client_secret=auth_config,






class_name ="LlamaIndex_auto"


```


```

# optional: delete schema


client.schema.delete_class(class_name)

```


```


from llama_index.vector_stores.weaviate import WeaviateVectorStore




from llama_index.core import VectorStoreIndex, StorageContext





vector_store_auto = WeaviateVectorStore(




weaviate_client=client, index_name=class_name





storage_context_auto = StorageContext.from_defaults(




vector_store=vector_store_auto



```


```

# Since "index_nodes" are concise summaries, we can directly feed them as objects into VectorStoreIndex



index = VectorStoreIndex(




objects=index_nodes, storage_context=storage_context_auto



```

## Setup Composable Auto-Retriever
[Section titled “Setup Composable Auto-Retriever”](https://developers.llamaindex.ai/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval/#setup-composable-auto-retriever)
In this section we setup our auto-retriever. There’s a few steps that we need to perform.
  1. **Define the Schema** : Define the vector db schema (e.g. the metadata fields). This will be put into the LLM input prompt when it’s deciding what metadata filters to infer.
  2. **Instantiate the VectorIndexAutoRetriever class** : This creates a retriever on top of our summarized metadata index, and takes in the defined schema as input.
  3. **Define a wrapper retriever** : This allows us to postprocess each node into an `IndexNode`, with an index id linking back source document. This will allow us to do recursive retrieval in the next section (which depends on IndexNode objects linking to downstream retrievers/query engines/other Nodes). **NOTE** : We are working on improving this abstraction.


Running this retriever will retrieve based on our text summaries and metadat of our top-level `IndeNode` objects. Then, their underlying retrievers will be used to retrieve content from the specific github issue.
### 1. Define the Schema
[Section titled “1. Define the Schema”](https://developers.llamaindex.ai/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval/#1-define-the-schema)

```


from llama_index.core.vector_stores import MetadataInfo, VectorStoreInfo






vector_store_info = VectorStoreInfo(




content_info="Github Issues",




metadata_info=[




MetadataInfo(




name="state",




description="Whether the issue is `open` or `closed`",




type="string",





MetadataInfo(




name="year",




description="The year issue was created",




type="integer",





MetadataInfo(




name="month",




description="The month issue was created",




type="integer",





MetadataInfo(




name="day",




description="The day issue was created",




type="integer",





MetadataInfo(




name="assignee",




description="The assignee of the ticket",




type="string",





MetadataInfo(




name="size",




description="How big the issue is (XS, S, M, L, XL, XXL)",




type="string",





```

### 2. Instantiate VectorIndexAutoRetriever
[Section titled “2. Instantiate VectorIndexAutoRetriever”](https://developers.llamaindex.ai/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval/#2-instantiate-vectorindexautoretriever)

```


from llama_index.core.retrievers import VectorIndexAutoRetriever





retriever = VectorIndexAutoRetriever(




index,




vector_store_info=vector_store_info,




similarity_top_k=2,




empty_query_top_k=10# if only metadata filters are specified, this is the limit




verbose=True,



```

## Try It Out
[Section titled “Try It Out”](https://developers.llamaindex.ai/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval/#try-it-out)
Now we can start retrieving relevant context over Github Issues!
To complete the RAG pipeline setup we’ll combine our recursive retriever with our `RetrieverQueryEngine` to generate a response in addition to the retrieved nodes.
### Try Out Retrieval
[Section titled “Try Out Retrieval”](https://developers.llamaindex.ai/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval/#try-out-retrieval)

```


from llama_index.core import QueryBundle





nodes = retriever.retrieve(QueryBundle("Tell me about some issues on 01/11"))


```


```

Using query str: issues


Using filters: [('day', '==', '11'), ('month', '==', '01')]


[1;3;38;2;11;159;203mRetrieval entering 9995: VectorIndexRetriever


[0m[1;3;38;2;237;90;200mRetrieving from object VectorIndexRetriever with query issues


[0m[1;3;38;2;11;159;203mRetrieval entering 9985: VectorIndexRetriever


[0m[1;3;38;2;237;90;200mRetrieving from object VectorIndexRetriever with query issues


```

The result is the source chunks in the relevant docs.
Let’s look at the date attached to the source chunk (was present in the original metadata).

```


print(f"Number of source nodes: {len(nodes)}")




nodes[0].node.metadata


```


```

Number of source nodes: 2







{'state': 'open',



'created_at': '2024-01-11T20:37:34Z',




'url': 'https://api.github.com/repos/run-llama/llama_index/issues/9995',




'source': 'https://github.com/run-llama/llama_index/pull/9995',




'labels': ['size:XXL'],




'index_id': 9995}


```

### Plug into `RetrieverQueryEngine`
[Section titled “Plug into RetrieverQueryEngine”](https://developers.llamaindex.ai/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval/#plug-into-retrieverqueryengine)
We plug into RetrieverQueryEngine to synthesize a result.

```


from llama_index.core.query_engine import RetrieverQueryEngine




from llama_index.llms.openai import OpenAI





llm = OpenAI(model="gpt-3.5-turbo")





query_engine = RetrieverQueryEngine.from_args(retriever, llm=llm)


```


```


response = query_engine.query("Tell me about some issues on 01/11")


```


```

Using query str: issues


Using filters: [('day', '==', '11'), ('month', '==', '01')]


[1;3;38;2;11;159;203mRetrieval entering 9995: VectorIndexRetriever


[0m[1;3;38;2;237;90;200mRetrieving from object VectorIndexRetriever with query issues


[0m[1;3;38;2;11;159;203mRetrieval entering 9985: VectorIndexRetriever


[0m[1;3;38;2;237;90;200mRetrieving from object VectorIndexRetriever with query issues


```


```


print(str(response))


```


```

There are two issues that were created on 01/11. The first issue is related to ensuring backwards compatibility with the new Pinecone client version bifurcation. The second issue is a feature request to implement the Language Agent Tree Search (LATS) agent in llama-index.

```


```


response = query_engine.query(




"Tell me about some open issues related to agents"



```


```

Using query str: agents


Using filters: [('state', '==', 'open')]


[1;3;38;2;11;159;203mRetrieval entering 10058: VectorIndexRetriever


[0m[1;3;38;2;237;90;200mRetrieving from object VectorIndexRetriever with query agents


[0m[1;3;38;2;11;159;203mRetrieval entering 9899: VectorIndexRetriever


[0m[1;3;38;2;237;90;200mRetrieving from object VectorIndexRetriever with query agents


```


```


print(str(response))


```


```

There are two open issues related to agents. One issue is about adding context for agents, updating a stale link, and adding a notebook to demo a react agent with context. The other issue is a feature request for parallelism when using the top agent from a multi-document agent while comparing multiple documents.

```

## Concluding Thoughts
[Section titled “Concluding Thoughts”](https://developers.llamaindex.ai/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval/#concluding-thoughts)
This shows you how to create a structured retrieval layer over your document summaries, allowing you to dynamically pull in the relevant documents based on the user query.
You may notice similarities between this and our [multi-document agents](https://docs.llamaindex.ai/en/stable/examples/agent/multi_document_agents.html). Both architectures are aimed for powerful multi-document retrieval.
The goal of this notebook is to show you how to apply structured querying in a multi-document setting. You can actually apply this auto-retrieval algorithm to our multi-agent setup too. The multi-agent setup is primarily focused on adding agentic reasoning across documents and per documents, alloinwg multi-part queries using chain-of-thought.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


