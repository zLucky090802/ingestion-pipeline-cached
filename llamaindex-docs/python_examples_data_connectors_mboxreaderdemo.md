[Skip to content](https://developers.llamaindex.ai/python/examples/data_connectors/mboxreaderdemo/#_top)
# Mbox Reader 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-readers-mbox


```


```


!pip install llama-index


```


```


%env OPENAI_API_KEY=sk-************


```


```


from llama_index.readers.mbox import MboxReader




from llama_index.core import VectorStoreIndex


```


```


documents = MboxReader().load_data(




"mbox_data_dir", max_count=1000




# Returns list of documents


```


```


index = VectorStoreIndex.from_documents(




documents




# Initialize index with documents


```


```


query_engine = index.as_query_engine()




res = query_engine.query("When did i have that call with the London office?")


```


```

> [query] Total LLM token usage: 100 tokens


> [query] Total embedding token usage: 10 tokens

```


```

res.response

```


```

> There is a call scheduled with the London office at 12am GMT on the 10th of February.

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


