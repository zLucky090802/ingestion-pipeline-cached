[Skip to content](https://developers.llamaindex.ai/python/framework/community/llama_packs/#_top)
LlamaIndex Framework
Open Source Community
Llama Packs
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Llama Packs 🦙📦
## Concept
[Section titled “Concept”](https://developers.llamaindex.ai/python/framework/community/llama_packs/#concept)
Llama Packs are a community-driven hub of **prepackaged modules/templates** you can use to kickstart your LLM app.
This directly tackles a big pain point in building LLM apps; every use case requires cobbling together custom components and a lot of tuning/dev time. Our goal is to accelerate that through a community led effort.
They can be used in two ways:
  * On one hand, they are **prepackaged modules** that can be initialized with parameters and run out of the box to achieve a given use case (whether that’s a full RAG flow, application template, or more). You can also import submodules (e.g. LLMs, query engines) to use directly.
  * On the other hand, LlamaPacks are **templates** that you can inspect, modify, and use.


**All packs are found on[LlamaHub](https://llamahub.ai/).** Go to the dropdown menu and select “LlamaPacks” to filter by packs.
**Please check the README of each pack for details on how to use**. [Example pack here](https://llamahub.ai/l/llama_packs-voyage_query_engine).
See our [launch blog post](https://blog.llamaindex.ai/introducing-llama-packs-e14f453b913a) for more details.
## Usage Pattern
[Section titled “Usage Pattern”](https://developers.llamaindex.ai/python/framework/community/llama_packs/#usage-pattern)
You can use Llama Packs through either the CLI or Python.
CLI:
Terminal window
```


llamaindex-clidownload-llamapack<pack_name>--download-dir<pack_directory>


```

Python:

```


from llama_index.core.llama_pack import download_llama_pack




# download and install dependencies



pack_cls = download_llama_pack("<pack_name>", "<pack_directory>")


```

You can use the pack in different ways, either to inspect modules, run it e2e, or customize the templates.

```

# every pack is initialized with different args



pack = pack_cls(*args, **kwargs)




# get modules



modules = pack.get_modules()



display(modules)



# run (every pack will have different args)



output = pack.run(*args, **kwargs)


```

Importantly, you can/should also go into `pack_directory` to inspect the source files/customize it. That’s part of the point!
## Module Guides
[Section titled “Module Guides”](https://developers.llamaindex.ai/python/framework/community/llama_packs/#module-guides)
Some example module guides are given below. Remember, go on [LlamaHub](https://llamahub.ai) to access the full range of packs.
  * [LlamaPacks Example](https://developers.llamaindex.ai/python/examples/llama_hub/llama_packs_example)


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


