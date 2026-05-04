[Skip to content](https://developers.llamaindex.ai/python/examples/node_postprocessor/recencypostprocessordemo/#_top)
# Recency Filtering 
Showcase capabilities of recency-weighted node postprocessor

```


import os





os.environ["OPENAI_API_KEY"] ="sk-..."


```


```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader




from llama_index.core.postprocessor import (




FixedRecencyPostprocessor,




EmbeddingRecencyPostprocessor,





from llama_index.core.node_parser import SentenceSplitter




from llama_index.core.storage.docstore import SimpleDocumentStore




from llama_index.core.response.notebook_utils import display_response


```

### Parse Documents into Nodes, add to Docstore
[Section titled “Parse Documents into Nodes, add to Docstore”](https://developers.llamaindex.ai/python/examples/node_postprocessor/recencypostprocessordemo/#parse-documents-into-nodes-add-to-docstore)
In this example, there are 3 different versions of PG’s essay. They are largely identical **except** for one specific section, which details the amount of funding they raised for Viaweb.
V1: 50k, V2: 30k, V3: 10K
V1: 2020-01-01, V2: 2020-02-03, V3: 2022-04-12
The idea is to encourage index to fetch the most recent info (which is V3)

```

# load documents



from llama_index.core import StorageContext






defget_file_metadata(file_name: str):




"""Get file metadata."""




if"v1"in file_name:




return {"date": "2020-01-01"}




elif"v2"in file_name:




return {"date": "2020-02-03"}




elif"v3"in file_name:




return {"date": "2022-04-12"}




else:




raiseValueError("invalid file")






documents = SimpleDirectoryReader(




input_files=[




"test_versioned_data/paul_graham_essay_v1.txt",




"test_versioned_data/paul_graham_essay_v2.txt",




"test_versioned_data/paul_graham_essay_v3.txt",





file_metadata=get_file_metadata,



).load_data()



# define settings



from llama_index.core import Settings





Settings.text_splitter = SentenceSplitter(chunk_size=512)




# use node parser to parse into nodes



nodes = Settings.text_splitter.get_nodes_from_documents(documents)




# add to docstore



docstore = SimpleDocumentStore()



docstore.add_documents(nodes)




storage_context = StorageContext.from_defaults(docstore=docstore)


```


```


print(documents[2].get_text())


```

### Build Index
[Section titled “Build Index”](https://developers.llamaindex.ai/python/examples/node_postprocessor/recencypostprocessordemo/#build-index)

```

# build index



index = VectorStoreIndex(nodes, storage_context=storage_context)


```


```

INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total embedding token usage: 84471 tokens

```

### Define Recency Postprocessors
[Section titled “Define Recency Postprocessors”](https://developers.llamaindex.ai/python/examples/node_postprocessor/recencypostprocessordemo/#define-recency-postprocessors)

```


node_postprocessor = FixedRecencyPostprocessor()


```


```


node_postprocessor_emb = EmbeddingRecencyPostprocessor()


```

### Query Index
[Section titled “Query Index”](https://developers.llamaindex.ai/python/examples/node_postprocessor/recencypostprocessordemo/#query-index)

```

# naive query




query_engine = index.as_query_engine(




similarity_top_k=3,





response = query_engine.query(




"How much did the author raise in seed funding from Idelle's husband"




" (Julian) for Viaweb?",



```


```

INFO:llama_index.token_counter.token_counter:> [query] Total LLM token usage: 1813 tokens


INFO:llama_index.token_counter.token_counter:> [query] Total embedding token usage: 22 tokens

```


```

# query using fixed recency node postprocessor




query_engine = index.as_query_engine(




similarity_top_k=3, node_postprocessors=[node_postprocessor]





response = query_engine.query(




"How much did the author raise in seed funding from Idelle's husband"




" (Julian) for Viaweb?",



```


```

# query using embedding-based node postprocessor




query_engine = index.as_query_engine(




similarity_top_k=3, node_postprocessors=[node_postprocessor_emb]





response = query_engine.query(




"How much did the author raise in seed funding from Idelle's husband"




" (Julian) for Viaweb?",



```


```

INFO:llama_index.token_counter.token_counter:> [query] Total LLM token usage: 541 tokens


INFO:llama_index.token_counter.token_counter:> [query] Total embedding token usage: 22 tokens

```

### Query Index (Lower-Level Usage)
[Section titled “Query Index (Lower-Level Usage)”](https://developers.llamaindex.ai/python/examples/node_postprocessor/recencypostprocessordemo/#query-index-lower-level-usage)
In this example we first get the full set of nodes from a query call, and then send to node postprocessor, and then finally synthesize response through a summary index.

```


from llama_index.core import SummaryIndex


```


```


query_str = (




"How much did the author raise in seed funding from Idelle's husband"




" (Julian) for Viaweb?"



```


```


query_engine = index.as_query_engine(




similarity_top_k=3, response_mode="no_text"





init_response = query_engine.query(




query_str,





resp_nodes = [n.node forin init_response.source_nodes]


```


```

INFO:llama_index.token_counter.token_counter:> [query] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [query] Total embedding token usage: 22 tokens

```


```


summary_index = SummaryIndex(resp_nodes)




query_engine = summary_index.as_query_engine(




node_postprocessors=[node_postprocessor]





response = query_engine.query(query_str)


```


```

INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total embedding token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [query] Total LLM token usage: 541 tokens


INFO:llama_index.token_counter.token_counter:> [query] Total embedding token usage: 0 tokens

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


