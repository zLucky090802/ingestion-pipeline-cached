[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/llm/grok/#_top)
LlamaIndex Framework
Integrations
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Grok 4 
Grok from xAI uses an OpenAI-compatible API, so you can use it with the OpenAILike integration class.

```


!pip install llama-index-llms-openai-like


```


```


grok_api_key ="xai-xxxxxxxx"


```


```


from llama_index.llms.openai_like import OpenAILike





llm = OpenAILike(




model="grok-4-0709",




api_base="https://api.x.ai/v1",




api_key=grok_api_key,




context_window=128000,




is_chat_model=True,




is_function_calling_model=False,






response = llm.complete("Hello World!")




print(str(response))


```


```

Hello World! 🌍 That's the universal greeting for programmers everywhere. What adventure brings you here today? 😊

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


