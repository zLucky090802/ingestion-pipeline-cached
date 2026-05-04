[Skip to content](https://developers.llamaindex.ai/python/examples/observability/promptlayerhandler/#_top)
# PromptLayer Handler 
[PromptLayer](https://promptlayer.com) is an LLMOps tool to help manage prompts, check out the [features](https://docs.promptlayer.com/introduction). Currently we only support OpenAI for this integration.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙 and PromptLayer.

```


!pip install llama-index




!pip install promptlayer


```

## Configure API keys
[Section titled “Configure API keys”](https://developers.llamaindex.ai/python/examples/observability/promptlayerhandler/#configure-api-keys)

```


import os





os.environ["OPENAI_API_KEY"] ="sk-..."




os.environ["PROMPTLAYER_API_KEY"] ="pl_..."


```

## Download Data
[Section titled “Download Data”](https://developers.llamaindex.ai/python/examples/observability/promptlayerhandler/#download-data)

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```


```

Will not apply HSTS. The HSTS database must be a regular and non-world-writable file.


ERROR: could not open HSTS store at '/home/loganm/.wget-hsts'. HSTS will be disabled.


--2023-11-29 21:09:27--  https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt


Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.110.133, 185.199.109.133, 185.199.108.133, ...


Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.110.133|:443... connected.


HTTP request sent, awaiting response... 200 OK


Length: 75042 (73K) [text/plain]


Saving to: ‘data/paul_graham/paul_graham_essay.txt’



data/paul_graham/pa 100%[===================>]  73.28K  --.-KB/s    in 0.04s



2023-11-29 21:09:28 (1.76 MB/s) - ‘data/paul_graham/paul_graham_essay.txt’ saved [75042/75042]

```


```


from llama_index.core import SimpleDirectoryReader





docs = SimpleDirectoryReader("./data/paul_graham/").load_data()


```

## Callback Manager Setup
[Section titled “Callback Manager Setup”](https://developers.llamaindex.ai/python/examples/observability/promptlayerhandler/#callback-manager-setup)

```


from llama_index.core import set_global_handler




# pl_tags are optional, to help you organize your prompts and apps



set_global_handler("promptlayer", pl_tags=["paul graham", "essay"])


```

## Trigger the callback with a query
[Section titled “Trigger the callback with a query”](https://developers.llamaindex.ai/python/examples/observability/promptlayerhandler/#trigger-the-callback-with-a-query)

```


from llama_index.core import VectorStoreIndex





index = VectorStoreIndex.from_documents(docs)




query_engine = index.as_query_engine()


```


```


response = query_engine.query("What did the author do growing up?")


```

## Access [promptlayer.com](https://promptlayer.com) to see stats
[Section titled “Access promptlayer.com to see stats”](https://developers.llamaindex.ai/python/examples/observability/promptlayerhandler/#access-promptlayercom-to-see-stats)
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


