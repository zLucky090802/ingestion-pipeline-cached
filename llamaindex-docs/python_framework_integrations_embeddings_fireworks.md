[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/fireworks/#_top)
LlamaIndex Framework
Integrations
Embeddings
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Fireworks Embeddings 
This guide shows you how to use Fireworks Embeddings through [Fireworks Endpoints](https://readme.fireworks.ai/).
First, let’s install LlamaIndex and the Fireworks dependencies

```


%pip install llama-index-embeddings-fireworks


```


```


!pip install llama-index


```

We can then query embeddings on Fireworks

```


from llama_index.embeddings.fireworks import FireworksEmbedding





embed_model = FireworksEmbedding(api_key="YOUR API KEY", embed_batch_size=10)


```


```

# Basic embedding example



embeddings = embed_model.get_text_embedding("How do I sail to the moon?")




print(len(embeddings), embeddings[:10])


```


```

768 [-0.67973792552948, 1.5226128101348877, -3.9547336101531982, 0.3112764358520508, -0.19723102450370789, 1.8839401006698608, -1.1595842838287354, -0.20612922310829163, 0.16740809381008148, -0.9071207046508789]

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


