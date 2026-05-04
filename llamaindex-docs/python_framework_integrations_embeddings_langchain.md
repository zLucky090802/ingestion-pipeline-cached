[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/langchain/#_top)
LlamaIndex Framework
Integrations
Embeddings
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# LangChain Embeddings 
This guide shows you how to use embedding models from [LangChain](https://python.langchain.com/docs/integrations/text_embedding/).
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-embeddings-langchain


```


```


!pip install llama-index


```


```


from langchain.embeddings import HuggingFaceEmbeddings




from llama_index.embeddings.langchain import LangchainEmbedding





lc_embed_model = HuggingFaceEmbeddings(




model_name="sentence-transformers/all-mpnet-base-v2"





embed_model = LangchainEmbedding(lc_embed_model)


```


```

# Basic embedding example



embeddings = embed_model.get_text_embedding(




"It is raining cats and dogs here!"





print(len(embeddings), embeddings[:10])


```


```

768 [-0.005906202830374241, 0.04911914840340614, -0.04757878929376602, -0.04320324584841728, 0.02837090566754341, -0.017371710389852524, -0.04422023147344589, -0.019035547971725464, 0.04941621795296669, -0.03839121758937836]

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


