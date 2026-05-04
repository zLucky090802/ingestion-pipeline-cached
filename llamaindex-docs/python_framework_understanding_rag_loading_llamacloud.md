[Skip to content](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/llamacloud/#_top)
LlamaIndex Framework
Learn
Building a RAG pipeline
Loading
[Loading from LlamaCloud](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/llamacloud/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Loading from LlamaCloud
Our enterprise service, [LlamaCloud](https://cloud.llamaindex.ai/), allows you to store and query your data in a fully-managed, scalable, and secure environment. For a full explanation of how to use LlamaCloud, see the [LlamaCloud documentation](https://docs.cloud.llamaindex.ai/), in particular the [framework integration guide](https://docs.cloud.llamaindex.ai/llamacloud/guides/framework_integration).
## Using LlamaCloud from LlamaIndex
[Section titled “Using LlamaCloud from LlamaIndex”](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/llamacloud/#using-llamacloud-from-llamaindex)
You can use LlamaCloud to connect to your data stores and automatically index them. Once an index is created, you can use it in just a few lines of code:

```


import os




from llama_cloud_services import LlamaCloudIndex





os.environ["LLAMA_CLOUD_API_KEY"] ="llx-..."





index = LlamaCloudIndex("my_first_index", project_name="Default")




query_engine = index.as_query_engine()




answer = query_engine.query("Example query")


```

It’s also possible to programmatically load documents into a LlamaCloud index; check the [documentation](https://docs.cloud.llamaindex.ai/llamacloud/guides/framework_integration) for more details.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


