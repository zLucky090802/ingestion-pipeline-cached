[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/openai/#_top)
LlamaIndex Framework
Integrations
Embeddings
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# OpenAI Embeddings 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-embeddings-openai


```


```


!pip install llama-index


```


```


import os





os.environ["OPENAI_API_KEY"] ="sk-..."


```


```


from llama_index.embeddings.openai import OpenAIEmbedding




from llama_index.core import Settings





embed_model = OpenAIEmbedding(embed_batch_size=10)




Settings.embed_model = embed_model


```

## Using OpenAI `text-embedding-3-large` and `text-embedding-3-small`
[Section titled “Using OpenAI text-embedding-3-large and text-embedding-3-small”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/openai/#using-openai-text-embedding-3-large-and-text-embedding-3-small)
Note, you may have to update your openai client: `pip install -U openai`

```

# get API key and create embeddings



from llama_index.embeddings.openai import OpenAIEmbedding





embed_model = OpenAIEmbedding(model="text-embedding-3-large")





embeddings = embed_model.get_text_embedding(




"Open AI new Embeddings models is great."



```


```


print(embeddings[:5])


```


```

[-0.011500772088766098, 0.02457442320883274, -0.01760469563305378, -0.017763426527380943, 0.029841400682926178]

```


```


print(len(embeddings))


```


```

# get API key and create embeddings



from llama_index.embeddings.openai import OpenAIEmbedding





embed_model = OpenAIEmbedding(




model="text-embedding-3-small",






embeddings = embed_model.get_text_embedding(




"Open AI new Embeddings models is awesome."



```


```


print(len(embeddings))


```

## Change the dimension of output embeddings
[Section titled “Change the dimension of output embeddings”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/openai/#change-the-dimension-of-output-embeddings)
Note: Make sure you have the latest OpenAI client

```

# get API key and create embeddings



from llama_index.embeddings.openai import OpenAIEmbedding






embed_model = OpenAIEmbedding(




model="text-embedding-3-large",




dimensions=512,






embeddings = embed_model.get_text_embedding(




"Open AI new Embeddings models with different dimensions is awesome."





print(len(embeddings))


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


