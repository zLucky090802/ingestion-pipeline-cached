[Skip to content](https://developers.llamaindex.ai/python/examples/data_connectors/twitterdemo/#_top)
# Twitter Reader 

```


%pip install llama-index-readers-twitter


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


from llama_index.core import VectorStoreIndex




from llama_index.readers.twitter import TwitterTweetReader




from IPython.display import Markdown, display




import os


```


```

# create an app in https://developer.twitter.com/en/apps



BEARER_TOKEN="<bearer_token>"


```


```

# create reader, specify twitter handles



reader = TwitterTweetReader(BEARER_TOKEN)




documents = reader.load_data(["@twitter_handle1"])


```


```


index = VectorStoreIndex.from_documents(documents)


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


