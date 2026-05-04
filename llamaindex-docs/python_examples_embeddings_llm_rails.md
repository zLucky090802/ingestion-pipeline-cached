[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/llm_rails/#_top)
LlamaIndex Framework
Integrations
Embeddings
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# LLMRails Embeddings 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-embeddings-llm-rails


```


```


!pip install llama-index


```


```

# imports




from llama_index.embeddings.llm_rails import LLMRailsEmbedding


```


```

# get credentials and create embeddings




import os





api_key = os.environ.get("API_KEY", "your-api-key")




model_id = os.environ.get("MODEL_ID", "your-model-id")






embed_model = LLMRailsEmbedding(model_id=model_id, api_key=api_key)





embeddings = embed_model.get_text_embedding(




"It is raining cats and dogs here!"



```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


