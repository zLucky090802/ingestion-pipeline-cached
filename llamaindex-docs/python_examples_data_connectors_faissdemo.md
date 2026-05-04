[Skip to content](https://developers.llamaindex.ai/python/examples/data_connectors/faissdemo/#_top)
# Faiss Reader 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-readers-faiss


```


```


!pip install llama-index


```


```


import logging




import sys





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


```


```


from llama_index.readers.faiss import FaissReader


```


```

# Build the Faiss index.


# A guide for how to get started with Faiss is here: https://github.com/facebookresearch/faiss/wiki/Getting-started


# We provide some example code below.




import faiss




# # Example Code


# d = 8


# docs = np.array([


#     [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],


#     [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],


#     [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],


#     [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],


#     [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]


# ])


# # id_to_text_map is used for query retrieval


# id_to_text_map = {


#     0: "aaaaaaaaa bbbbbbb cccccc",


#     1: "foooooo barrrrrr",


#     2: "tmp tmptmp tmp",


#     3: "hello world hello world",


#     4: "cat dog cat dog"



# # build the index


# index = faiss.IndexFlatL2(d)


# index.add(docs)




id_to_text_map = {




"id1": "text blob 1",




"id2": "text blob 2",





index =...


```


```


reader = FaissReader(index)


```


```

# To load data from the Faiss index, you must specify:


# k: top nearest neighbors


# query: a 2D embedding representation of your queries (rows are queries)




query1 = np.array([...])




query2 = np.array([...])




query = np.array([query1, query2])





documents = reader.load_data(query=query, id_to_text_map=id_to_text_map, k=k)


```

### Create index
[Section titled “Create index”](https://developers.llamaindex.ai/python/examples/data_connectors/faissdemo/#create-index)

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


