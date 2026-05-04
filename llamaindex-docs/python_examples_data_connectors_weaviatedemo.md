[Skip to content](https://developers.llamaindex.ai/python/examples/data_connectors/weaviatedemo/#_top)
# Weaviate Reader 

```


%pip install llama-index-readers-weaviate


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


import weaviate




from llama_index.readers.weaviate import WeaviateReader


```


```

# See https://weaviate.io/developers/weaviate/client-libraries/python


# for more details on authentication



resource_owner_config = weaviate.AuthClientPassword(




username="<username>",




password="<password>",





# initialize reader



reader = WeaviateReader(




"https://<cluster-id>.semi.network/",




auth_client_secret=resource_owner_config,



```

You have two options for the Weaviate reader: 1) directly specify the class_name and properties, or 2) input the raw graphql_query. Examples are shown below.

```

# 1) load data using class_name and properties


# docs = reader.load_data(


#    class_name="Author", properties=["name", "description"], separate_documents=True





documents = reader.load_data(




class_name="<class_name>",




properties=["property1", "property2", "..."],




separate_documents=True,



```


```

# 2) example GraphQL query


# query = """



#   Get {


#     Author {


#       name


#       description


#     }


#   }



# """


# docs = reader.load_data(graphql_query=query, separate_documents=True)




query ="""





Get {




<class_name> {




<property1>




<property2>










documents = reader.load_data(graphql_query=query, separate_documents=True)


```

### Create index
[Section titled “Create index”](https://developers.llamaindex.ai/python/examples/data_connectors/weaviatedemo/#create-index)

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


