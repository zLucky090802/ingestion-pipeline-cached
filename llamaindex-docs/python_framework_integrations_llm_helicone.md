[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/llm/helicone/#_top)
LlamaIndex Framework
Integrations
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Helicone AI Gateway 
Helicone is an OpenAI-compatible AI Gateway that routes requests to many providers with observability, control, and caching. Learn more on the [Helicone docs](https://docs.helicone.ai/) and see available [models](https://www.helicone.ai/models).
If you’re opening this Notebook on Colab, you’ll likely need to install the integration packages below.
Notes:
  * Only your Helicone API key is required (`HELICONE_API_KEY`); no provider keys are needed.
  * Default base URL is `https://ai-gateway.helicone.ai/v1`. Override with `api_base` or `HELICONE_API_BASE`.



```


%pip install llama-index-llms-helicone


```


```


!pip install llama-index


```


```


from llama_index.llms.helicone import Helicone




from llama_index.core.llms import ChatMessage


```

## Call `chat` with ChatMessage List
[Section titled “Call chat with ChatMessage List”](https://developers.llamaindex.ai/python/framework/integrations/llm/helicone/#call-chat-with-chatmessage-list)
You need to either set env var `HELICONE_API_KEY` or pass `api_key` in the constructor.

```

# import os


# os.environ["HELICONE_API_KEY"] = "<your-helicone-api-key>"




llm = Helicone(




api_key="<your-helicone-api-key>"# or set HELICONE_API_KEY




model="gpt-4o-mini"# routed via the Helicone AI Gateway




max_tokens=256,



```


```


message = ChatMessage(role="user", content="Tell me a joke")




resp = llm.chat([message])




print(resp)


```

### Streaming
[Section titled “Streaming”](https://developers.llamaindex.ai/python/framework/integrations/llm/helicone/#streaming)

```


message = ChatMessage(role="user", content="Tell me a story in 200 words")




resp = llm.stream_chat([message])




forin resp:




print(r.delta, end="")


```

## API Support (Chat only; no legacy Completions)
[Section titled “API Support (Chat only; no legacy Completions)”](https://developers.llamaindex.ai/python/framework/integrations/llm/helicone/#api-support-chat-only-no-legacy-completions)
Helicone supports OpenAI-compatible Chat Completions and the newer Responses API. The legacy Completions API is not supported.
In LlamaIndex, use `llm.chat(...)` and `llm.stream_chat(...)`.
## Model Configuration
[Section titled “Model Configuration”](https://developers.llamaindex.ai/python/framework/integrations/llm/helicone/#model-configuration)

```

# Choose any OpenAI-compatible model routed by Helicone.


# See https://www.helicone.ai/models for options.



# If HELICONE_API_KEY is set in your environment, you can omit api_key here.



llm = Helicone(model="gpt-4o-mini")




message = ChatMessage(




role="user", content="Write one sentence about Rust dragons coding."





resp = llm.chat([message])




print(resp)


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


