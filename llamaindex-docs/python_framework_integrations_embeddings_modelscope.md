[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/modelscope/#_top)
LlamaIndex Framework
Integrations
Embeddings
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# ModelScope Embeddings 
In this notebook, we show how to use the ModelScope Embeddings in LlamaIndex. Check out the [ModelScope site](https://www.modelscope.cn/).
If you’re opening this Notebook on colab, you will need to install LlamaIndex 🦙 and the modelscope.

```


!pip install llama-index-embeddings-modelscope


```

## Basic Usage
[Section titled “Basic Usage”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/modelscope/#basic-usage)

```


import sys




from llama_index.embeddings.modelscope.base import ModelScopeEmbedding





model = ModelScopeEmbedding(




model_name="iic/nlp_gte_sentence-embedding_chinese-base",




model_revision="master",






rsp = model.get_query_embedding("Hello, who are you?")




print(rsp)





rsp = model.get_text_embedding("Hello, who are you?")




print(rsp)


```

#### Generate Batch Embedding
[Section titled “Generate Batch Embedding”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/modelscope/#generate-batch-embedding)

```


from llama_index.embeddings.modelscope.base import ModelScopeEmbedding





model = ModelScopeEmbedding(




model_name="iic/nlp_gte_sentence-embedding_chinese-base",




model_revision="master",






rsp = model.get_text_embedding_batch(




["Hello, who are you?", "I am a student."]





print(rsp)


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


