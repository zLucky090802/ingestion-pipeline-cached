[Skip to content](https://developers.llamaindex.ai/python/examples/data_connectors/notiondemo/#_top)
# Notion Reader 
Demonstrates our Notion data connector

```


%pip install llama-index-readers-notion


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


from llama_index.core import SummaryIndex




from llama_index.readers.notion import NotionPageReader




from IPython.display import Markdown, display




import os


```


```


integration_token = os.getenv("NOTION_INTEGRATION_TOKEN")




page_ids = ["<page_id>"]




documents = NotionPageReader(integration_token=integration_token).load_data(




page_ids=page_ids



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

You can also pass the id of a database to index all the pages in that database:

```


database_ids = ["<database-id>"]




# https://developers.notion.com/docs/working-with-databases for how to find your database id




documents = NotionPageReader(integration_token=integration_token).load_data(




database_ids=database_ids






print(documents)


```


```

# set Logging to DEBUG for more detailed outputs



index = SummaryIndex.from_documents(documents)




query_engine = index.as_query_engine()




response = query_engine.query("<query_text>")




display(Markdown(f"<b>{response}</b>"))


```

To list all databases in your Notion workspace:

```


reader = NotionPageReader(integration_token=integration_token)




databases = reader.list_databases()




print(databases)


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


