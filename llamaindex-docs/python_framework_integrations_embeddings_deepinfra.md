[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/deepinfra/#_top)
LlamaIndex Framework
Integrations
Embeddings
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# DeepInfra 
With this integration, you can use the DeepInfra embeddings model to get embeddings for your text data. Here is the link to the [embeddings models](https://deepinfra.com/models/embeddings).
First, you need to sign up on the [DeepInfra website](https://deepinfra.com/) and get the API token. You can copy `model_ids` from the model cards and start using them in your code.
### Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/deepinfra/#installation)

```


!pip install llama-index llama-index-embeddings-deepinfra


```

### Initialization
[Section titled “Initialization”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/deepinfra/#initialization)

```


from dotenv import load_dotenv, find_dotenv




from llama_index.embeddings.deepinfra import DeepInfraEmbeddingModel





_ = load_dotenv(find_dotenv())





model = DeepInfraEmbeddingModel(




model_id="BAAI/bge-large-en-v1.5"# Use custom model ID




api_token="YOUR_API_TOKEN"# Optionally provide token here




normalize=True# Optional normalization




text_prefix="text: "# Optional text prefix




query_prefix="query: "# Optional query prefix



```

### Synchronous Requests
[Section titled “Synchronous Requests”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/deepinfra/#synchronous-requests)
#### Get Text Embedding
[Section titled “Get Text Embedding”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/deepinfra/#get-text-embedding)

```


response = model.get_text_embedding("hello world")




print(response)


```

#### Batch Requests
[Section titled “Batch Requests”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/deepinfra/#batch-requests)

```


texts = ["hello world", "goodbye world"]




response_batch = model.get_text_embedding_batch(texts)




print(response_batch)


```

#### Query Requests
[Section titled “Query Requests”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/deepinfra/#query-requests)

```


query_response = model.get_query_embedding("hello world")




print(query_response)


```

### Asynchronous Requests
[Section titled “Asynchronous Requests”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/deepinfra/#asynchronous-requests)
#### Get Text Embedding
[Section titled “Get Text Embedding”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/deepinfra/#get-text-embedding-1)

```


asyncdefmain():




text ="hello world"




async_response =await model.aget_text_embedding(text)




print(async_response)






if__name__=="__main__":




import asyncio





asyncio.run(main())


```

For any questions or feedback, please contact us at feedback@deepinfra.com.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


