[Skip to content](https://developers.llamaindex.ai/python/examples/data_connectors/obsidianreaderdemo/#_top)
# Obsidian Reader 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-readers-obsidian


```


```


!pip install llama-index


```


```


%env OPENAI_API_KEY=sk-************


```


```


import logging




import sys





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


```


```


from llama_index.readers.obsidian import ObsidianReader




from llama_index.core import VectorStoreIndex


```


```


documents = ObsidianReader(




"/Users/hursh/vault"




).load_data()  # Returns list of documents


```


```


index = VectorStoreIndex.from_documents(




documents




# Initialize index with documents


```


```

# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine()




res = query_engine.query("What is the meaning of life?")


```


```

> [query] Total LLM token usage: 920 tokens


> [query] Total embedding token usage: 7 tokens

```


```

res.response

```


```

'\nThe meaning of life is subjective and can vary from person to person. It is ultimately up to each individual to decide what they believe is the purpose and value of life. Some may find meaning in their faith, while others may find it in their relationships, work, or hobbies. Ultimately, it is up to each individual to decide what brings them joy and fulfillment and to pursue that path.'

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


