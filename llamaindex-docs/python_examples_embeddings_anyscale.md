[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/anyscale/#_top)
LlamaIndex Framework
Integrations
Embeddings
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Anyscale Embeddings 
This guide shows you how to use Anyscale Embeddings through [Anyscale Endpoints](https://docs.endpoints.anyscale.com/).
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-embeddings-anyscale


```


```


!pip install llama-index


```


```


from llama_index.embeddings.anyscale import AnyscaleEmbedding





embed_model = AnyscaleEmbedding(




api_key=ANYSCALE_ENDPOINT_TOKEN, embed_batch_size=10



```


```

# Basic embedding example



embeddings = embed_model.get_text_embedding(




"It is raining cats and dogs here!"





print(len(embeddings), embeddings[:10])


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


