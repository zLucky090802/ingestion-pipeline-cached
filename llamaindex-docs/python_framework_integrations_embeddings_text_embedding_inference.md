[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/text_embedding_inference/#_top)
LlamaIndex Framework
Integrations
Embeddings
[Text Embedding Inference ](https://developers.llamaindex.ai/python/framework/integrations/embeddings/text_embedding_inference/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Text Embedding Inference 
This notebook demonstrates how to configure `TextEmbeddingInference` embeddings.
The first step is to deploy the embeddings server. For detailed instructions, see the [official repository for Text Embeddings Inference](https://github.com/huggingface/text-embeddings-inference). Or [tei-gaudi repository](https://github.com/huggingface/tei-gaudi) if you are deploying on Habana Gaudi/Gaudi 2.
Once deployed, the code below will connect to and submit embeddings for inference.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-embeddings-text-embeddings-inference


```


```


!pip install llama-index


```


```


from llama_index.embeddings.text_embeddings_inference import (




TextEmbeddingsInference,







embed_model = TextEmbeddingsInference(




model_name="BAAI/bge-large-en-v1.5"# required for formatting inference text,




timeout=60# timeout in seconds




embed_batch_size=10# batch size for embedding



```


```


embeddings = embed_model.get_text_embedding("Hello World!")




print(len(embeddings))




print(embeddings[:5])


```


```

1024


[0.010597229, 0.05895996, 0.022445679, -0.012046814, -0.03164673]

```


```


embeddings =await embed_model.aget_text_embedding("Hello World!")




print(len(embeddings))




print(embeddings[:5])


```


```

1024


[0.010597229, 0.05895996, 0.022445679, -0.012046814, -0.03164673]

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


