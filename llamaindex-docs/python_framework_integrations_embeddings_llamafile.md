[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/llamafile/#_top)
LlamaIndex Framework
Integrations
Embeddings
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Llamafile Embeddings 
One of the simplest ways to run an LLM locally is using a [llamafile](https://github.com/Mozilla-Ocho/llamafile). llamafiles bundle model weights and a [specially-compiled](https://github.com/Mozilla-Ocho/llamafile?tab=readme-ov-file#technical-details) version of [`llama.cpp`](https://github.com/ggerganov/llama.cpp) into a single file that can run on most computers any additional dependencies. They also come with an embedded inference server that provides an [API](https://github.com/Mozilla-Ocho/llamafile/blob/main/llama.cpp/server/README.md#api-endpoints) for interacting with your model.
## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/llamafile/#setup)
  1. Download a llamafile from [HuggingFace](https://huggingface.co/models?other=llamafile)
  2. Make the file executable
  3. Run the file


Here’s a simple bash script that shows all 3 setup steps:
Terminal window
```

# Download a llamafile from HuggingFace



wgethttps://huggingface.co/jartine/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/TinyLlama-1.1B-Chat-v1.0.Q5_K_M.llamafile




# Make the file executable. On Windows, instead just rename the file to end in ".exe".



chmod+xTinyLlama-1.1B-Chat-v1.0.Q5_K_M.llamafile




# Start the model server. Listens at http://localhost:8080 by default.



./TinyLlama-1.1B-Chat-v1.0.Q5_K_M.llamafile--server--nobrowser--embedding


```

Your model’s inference server listens at localhost:8080 by default.

```


%pip install llama-index-embeddings-llamafile


```


```


!pip install llama-index


```


```


from llama_index.embeddings.llamafile import LlamafileEmbedding





embedding = LlamafileEmbedding(




base_url="http://localhost:8080",






pass_embedding = embedding.get_text_embedding_batch(




["This is a passage!", "This is another passage"], show_progress=True





print(len(pass_embedding), len(pass_embedding[0]))





query_embedding = embedding.get_query_embedding("Where is blue?")




print(len(query_embedding))




print(query_embedding[:10])


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


