[Skip to content](https://developers.llamaindex.ai/python/examples/data_connectors/mongodemo/#_top)
# MongoDB Reader 
Demonstrates our MongoDB data connector

```


%pip install llama-index-readers-mongodb


```


```


import logging




import sys





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


```

If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙 and pymongo.

```


!pip install llama-index pymongo


```


```


from llama_index.core import SummaryIndex




from llama_index.readers.mongodb import SimpleMongoReader




from IPython.display import Markdown, display




import os


```


```


host ="<host>"




port ="<port>"




db_name ="<db_name>"




collection_name ="<collection_name>"



# query_dict is passed into db.collection.find()



query_dict = {}




field_names = ["text"]




reader = SimpleMongoReader(host, port)




documents = reader.load_data(




db_name, collection_name, field_names, query_dict=query_dict



```


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


