[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/upstage/#_top)
LlamaIndex Framework
Integrations
Embeddings
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Upstage Embeddings 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-embeddings-upstage==0.2.1


```


```


!pip install llama-index


```


```


import os





os.environ["UPSTAGE_API_KEY"] ="YOUR_API_KEY"


```


```


from llama_index.embeddings.upstage import UpstageEmbedding




from llama_index.core import Settings





embed_model = UpstageEmbedding()




Settings.embed_model = embed_model


```

## Using Upstage Embeddings
[Section titled “Using Upstage Embeddings”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/upstage/#using-upstage-embeddings)
Note, you may have to update your openai client: `pip install -U openai`

```

# get API key and create embeddings



from llama_index.embeddings.upstage import UpstageEmbedding





embed_model = UpstageEmbedding()





embeddings = embed_model.get_text_embedding(




"Upstage new Embeddings models is great."



```


```


print(embeddings[:5])


```


```

[0.02535058930516243, 0.007272760849446058, 0.015372460708022118, -0.007840132340788841, 0.0017625312320888042]

```


```


print(len(embeddings))


```


```


embeddings = embed_model.get_query_embedding(




"What are some great Embeddings model?"



```


```


print(embeddings[:5])


```


```

[0.03518765792250633, 0.01018011849373579, 0.013282101601362228, -0.008568626828491688, -0.005505830980837345]

```


```


print(len(embeddings))


```


```

# embed documents



embeddings = embed_model.get_text_embedding_batch(





"Upstage new Embeddings models is awesome.",




"Upstage LLM is also awesome.",




```


```


print(len(embeddings))


```


```


print(embeddings[0][:5])


```


```

[0.028246860951185226, 0.008945596404373646, 0.01719627156853676, -0.005711239762604237, 0.0016300849383696914]

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


