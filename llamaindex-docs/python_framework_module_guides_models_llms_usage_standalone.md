[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/models/llms/usage_standalone/#_top)
LlamaIndex Framework
Component Guides
Models
Llms
[Using LLMs as standalone modules](https://developers.llamaindex.ai/python/framework/module_guides/models/llms/usage_standalone/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Using LLMs as standalone modules
You can use our LLM modules on their own.
## Text Completion Example
[Section titled “Text Completion Example”](https://developers.llamaindex.ai/python/framework/module_guides/models/llms/usage_standalone/#text-completion-example)

```


from llama_index.llms.openai import OpenAI




# non-streaming



completion = OpenAI().complete("Paul Graham is ")




print(completion)




# using streaming endpoint



from llama_index.llms.openai import OpenAI





llm = OpenAI()




completions = llm.stream_complete("Paul Graham is ")




for completion in completions:




print(completion.delta, end="")


```

## Chat Example
[Section titled “Chat Example”](https://developers.llamaindex.ai/python/framework/module_guides/models/llms/usage_standalone/#chat-example)

```


from llama_index.core.llms import ChatMessage




from llama_index.llms.openai import OpenAI





messages = [




ChatMessage(




role="system", content="You are a pirate with a colorful personality"





ChatMessage(role="user", content="What is your name"),





resp = OpenAI().chat(messages)




print(resp)


```

Check out our [modules section](https://developers.llamaindex.ai/python/framework/module_guides/models/llms/modules) for usage guides for each LLM.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


