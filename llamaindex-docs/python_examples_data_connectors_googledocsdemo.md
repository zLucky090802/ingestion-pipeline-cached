[Skip to content](https://developers.llamaindex.ai/python/examples/data_connectors/googledocsdemo/#_top)
# Google Docs Reader 
Demonstrates our Google Docs data connector
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-readers-google


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


from llama_index.core import SummaryIndex




from llama_index.readers.google import GoogleDocsReader




from IPython.display import Markdown, display




import os


```


```

# make sure credentials.json file exists



document_ids = ["<document_id>"]




documents = GoogleDocsReader().load_data(document_ids=document_ids)


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


