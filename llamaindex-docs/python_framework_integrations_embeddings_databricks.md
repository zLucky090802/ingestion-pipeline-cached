[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/databricks/#_top)
LlamaIndex Framework
Integrations
Embeddings
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Databricks Embeddings 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index




%pip install llama-index-embeddings-databricks


```


```


import os




from llama_index.core import Settings




from llama_index.embeddings.databricks import DatabricksEmbedding


```


```

# Set up the DatabricksEmbedding class with the required model, API key and serving endpoint



os.environ["DATABRICKS_TOKEN"] ="<MY TOKEN>"




os.environ["DATABRICKS_SERVING_ENDPOINT"] ="<MY ENDPOINT>"




embed_model = DatabricksEmbedding(model="databricks-bge-large-en")




Settings.embed_model = embed_model


```


```

# Embed some text



embeddings = embed_model.get_text_embedding(




"The DatabricksEmbedding integration works great."



```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


