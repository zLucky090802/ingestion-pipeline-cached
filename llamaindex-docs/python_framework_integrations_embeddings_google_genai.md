[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/google_genai/#_top)
LlamaIndex Framework
Integrations
Embeddings
[Google GenAI Embeddings ](https://developers.llamaindex.ai/python/framework/integrations/embeddings/google_genai/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Google GenAI Embeddings 
Using Google’s `google-genai` package, LlamaIndex provides a `GoogleGenAIEmbedding` class that allows you to embed text using Google’s GenAI models from both the Gemini and Vertex AI APIs using the latest `gemini-embedding-2-preview` model.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-embeddings-google-genai


```


```


import os





os.environ["GOOGLE_API_KEY"] ="..."


```

## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/google_genai/#setup)
`GoogleGenAIEmbedding` is a wrapper around the `google-genai` package, which means it supports both Gemini and Vertex AI APIs out of the box.
You can pass in the `api_key` directly, or pass in a `vertexai_config` to use the Vertex AI API.
Other options include `embed_batch_size`, `model_name`, and `embedding_config`.

```


from llama_index.embeddings.google_genai import GoogleGenAIEmbedding




from google.genai.types import EmbedContentConfig





embed_model = GoogleGenAIEmbedding(




model_name="gemini-embedding-2-preview",




embed_batch_size=100,




# can pass in the api key directly




# api_key="...",




# or pass in a vertexai_config




# vertexai_config={




#     "project": "...",




#     "location": "...",





# can also pass in an embedding_config




# embedding_config=EmbedContentConfig(...)



```

## Usage
[Section titled “Usage”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/google_genai/#usage)
### Sync
[Section titled “Sync”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/google_genai/#sync)

```


embeddings = embed_model.get_text_embedding("Google Gemini Embeddings.")




print(embeddings[:5])




print(f"Dimension of embeddings: {len(embeddings)}")


```


```

[0.031099992, 0.02192731, -0.06523498, 0.016788177, 0.0392835]


Dimension of embeddings: 768

```


```


embeddings = embed_model.get_query_embedding("Query Google Gemini Embeddings.")




print(embeddings[:5])




print(f"Dimension of embeddings: {len(embeddings)}")


```


```

[0.022199392, 0.03671178, -0.06874573, 0.02195774, 0.05475164]


Dimension of embeddings: 768

```


```


embeddings = embed_model.get_text_embedding_batch(





"Google Gemini Embeddings.",




"Google is awesome.",




"Llamaindex is awesome.",






print(f"Got {len(embeddings)} embeddings")




print(f"Dimension of embeddings: {len(embeddings[0])}")


```


```

Got 3 embeddings


Dimension of embeddings: 768

```

### Async
[Section titled “Async”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/google_genai/#async)

```


embeddings =await embed_model.aget_text_embedding("Google Gemini Embeddings.")




print(embeddings[:5])




print(f"Dimension of embeddings: {len(embeddings)}")


```


```

[0.031099992, 0.02192731, -0.06523498, 0.016788177, 0.0392835]


Dimension of embeddings: 768

```


```


embeddings =await embed_model.aget_query_embedding(




"Query Google Gemini Embeddings."





print(embeddings[:5])




print(f"Dimension of embeddings: {len(embeddings)}")


```


```

[0.022199392, 0.03671178, -0.06874573, 0.02195774, 0.05475164]


Dimension of embeddings: 768

```


```


embeddings =await embed_model.aget_text_embedding_batch(





"Google Gemini Embeddings.",




"Google is awesome.",




"Llamaindex is awesome.",






print(f"Got {len(embeddings)} embeddings")




print(f"Dimension of embeddings: {len(embeddings[0])}")


```


```

Got 3 embeddings


Dimension of embeddings: 768

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


