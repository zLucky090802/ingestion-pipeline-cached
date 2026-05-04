[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/yandexgpt/#_top)
LlamaIndex Framework
Integrations
Embeddings
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# YandexGPT 

```


%pip install llama-index-embeddings-yandexgpt


```


```


!pip install llama-index


```


```


from llama_index.embeddings.yandexgpt import YandexGPTEmbedding





yandexgpt_embedding = YandexGPTEmbedding(




api_key="your-api-key", folder_id="your-folder-id"






text_embedding = yandexgpt_embedding._get_text_embeddings(




["This is a passage!", "This is another passage"]





print(text_embedding)





query_embedding = yandexgpt_embedding._get_query_embedding("Where is blue?")




print(query_embedding)


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


