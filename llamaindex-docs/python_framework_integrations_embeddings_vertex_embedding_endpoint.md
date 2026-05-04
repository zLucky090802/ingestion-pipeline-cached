[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/vertex_embedding_endpoint/#_top)
LlamaIndex Framework
Integrations
Embeddings
[Interacting with Embeddings deployed in Vertex AI Endpoint with LlamaIndex ](https://developers.llamaindex.ai/python/framework/integrations/embeddings/vertex_embedding_endpoint/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Interacting with Embeddings deployed in Vertex AI Endpoint with LlamaIndex 
A Vertex AI endpoint is a managed resource that enables the deployment of machine learning models, such as embeddings, for making predictions on new data.
This notebook demonstrates how to interact with embedding endpoints using the `VertexEndpointEmbedding` class, leveraging the LlamaIndex.
## Setting Up
[Section titled “Setting Up”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/vertex_embedding_endpoint/#setting-up)
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-embeddings-vertex-endpoint


```


```


! pip install llama-index


```

You need to specify the endpoint information (endpoint ID, project ID, and region) to interact with the model deployed in Vertex AI.

```


ENDPOINT_ID="<-YOUR-ENDPOINT-ID->"




PROJECT_ID="<-YOUR-PROJECT-ID->"




LOCATION="<-YOUR-GCP-REGION->"


```

Credentials should be provided to connect to the endpoint. You can either:
  * Use a service account JSON file by specifying the `service_account_file` parameter.
  * Provide the service account information directly through the `service_account_info` parameter.


**Example using a service account file:**

```


from llama_index.embeddings.vertex_endpoint import VertexEndpointEmbedding





SERVICE_ACCOUNT_FILE="<-YOUR-SERVICE-ACCOUNT-FILE-PATH->.json"





embed_model = VertexEndpointEmbedding(




endpoint_id=ENDPOINT_ID,




project_id=PROJECT_ID,




location=LOCATION,




service_account_file=SERVICE_ACCOUNT_FILE,



```

**Example using direct service account info:** :

```


from llama_index.embeddings.vertex_endpoint import VertexEndpointEmbedding





SERVICE_ACCOUNT_INFO= {




"private_key": "<-PRIVATE-KEY->",




"client_email": "<-SERVICE-ACCOUNT-EMAIL->",




"token_uri": "https://oauth2.googleapis.com/token",






embed_model = VertexEndpointEmbedding(




endpoint_id=ENDPOINT_ID,




project_id=PROJECT_ID,




location=LOCATION,




service_account_info=SERVICE_ACCOUNT_INFO,



```

## Basic Usage
[Section titled “Basic Usage”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/vertex_embedding_endpoint/#basic-usage)
### Call `get_text_embedding`
[Section titled “Call get_text_embedding”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/vertex_embedding_endpoint/#call-get_text_embedding)

```


embeddings = embed_model.get_text_embedding(




"Vertex AI is a managed machine learning (ML) platform provided by Google Cloud. It allows data scientists and developers to build, deploy, and scale machine learning models efficiently, leveraging Google's ML infrastructure."



```


```


embeddings[:10]


```


```

[0.011612358,



0.01030837,




-0.04710829,




-0.030719217,




0.027658276,




-0.031597693,




0.012065322,




-0.037609763,




0.02321099,




0.012868305]


```

### Call `get_text_embedding_batch`
[Section titled “Call get_text_embedding_batch”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/vertex_embedding_endpoint/#call-get_text_embedding_batch)

```


embeddings = embed_model.get_text_embedding_batch(





"Vertex AI is a managed machine learning (ML) platform provided by Google Cloud. It allows data scientists and developers to build, deploy, and scale machine learning models efficiently, leveraging Google's ML infrastructure.",




"Vertex is integrated with llamaIndex",




```


```


len(embeddings)


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


