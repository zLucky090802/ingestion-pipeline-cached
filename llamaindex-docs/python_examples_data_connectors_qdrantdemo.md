[Skip to content](https://developers.llamaindex.ai/python/examples/data_connectors/qdrantdemo/#_top)
# Qdrant Reader 

```


%pip install llama-index-readers-qdrant


```


```


import logging




import sys





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


```

If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


!pip install llama-index


```


```


from llama_index.readers.qdrant import QdrantReader


```


```


reader = QdrantReader(host="localhost")


```


```

# the query_vector is an embedding representation of your query_vector


# Example query vector:


#   query_vector=[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]




query_vector = [n1, n2, n3, ...]


```


```


# NOTE: Required args are collection_name, query_vector.



# See the Python client: https://github.com/qdrant/qdrant_client


# for more details.



documents = reader.load_data(




collection_name="demo", query_vector=query_vector, limit=5



```

### Create index
[Section titled “Create index”](https://developers.llamaindex.ai/python/examples/data_connectors/qdrantdemo/#create-index)

```


index = SummaryIndex.from_documents(documents)


```


```

# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine()




response = query_engine.query("<query_text>")


```


```


display(Markdown(f"<b>{response}</b>"))


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


