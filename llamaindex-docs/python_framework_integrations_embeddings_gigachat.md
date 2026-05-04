[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/gigachat/#_top)
LlamaIndex Framework
Integrations
Embeddings
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# GigaChat 

```


%pip install llama-index-embeddings-gigachat


```


```


!pip install llama-index


```


```


from llama_index.embeddings.gigachat import GigaChatEmbedding





gigachat_embedding = GigaChatEmbedding(




auth_data="your-auth-data",




scope="your-scope"# Set scope 'GIGACHAT_API_PERS' for personal use or 'GIGACHAT_API_CORP' for corporate use.






queries_embedding = gigachat_embedding._get_query_embeddings(




["This is a passage!", "This is another passage"]





print(queries_embedding)





text_embedding = gigachat_embedding._get_text_embedding("Where is blue?")




print(text_embedding)


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


