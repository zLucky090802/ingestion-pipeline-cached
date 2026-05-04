[Skip to content](https://developers.llamaindex.ai/python/framework/understanding/using_llms/#_top)
LlamaIndex Framework
Learn
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Using LLMs
One of the first steps when building an LLM-based application is which LLM to use; they have different strengths and price points and you may wish to use more than one.
LlamaIndex provides a single interface to a large number of different LLMs. Using an LLM can be as simple as installing the appropriate integration:
Terminal window
```


pipinstallllama-index-llms-openai


```

And then calling it in a one-liner:

```


from llama_index.llms.openai import OpenAI





response = OpenAI().complete("William Shakespeare is ")




print(response)


```

Note that this requires an API key called `OPENAI_API_KEY` in your environment; see the [starter tutorial](https://developers.llamaindex.ai/python/framework/getting_started/starter_example) for more details.
`complete` is also available as an async method, `acomplete`.
You can also get a streaming response by calling `stream_complete`, which returns a generator that yields tokens as they are produced:

```

handle = OpenAI().stream_complete("William Shakespeare is ")



for token in handle:



print(token.delta, end="", flush=True)


```

`stream_complete` is also available as an async method, `astream_complete`.
## Chat interface
[Section titled “Chat interface”](https://developers.llamaindex.ai/python/framework/understanding/using_llms/#chat-interface)
The LLM class also implements a `chat` method, which allows you to have more sophisticated interactions:

```


messages = [




ChatMessage(role="system", content="You are a helpful assistant."),




ChatMessage(role="user", content="Tell me a joke."),





chat_response = llm.chat(messages)


```

For streaming responses (where tokens are yielded as they are generated), `stream_chat` and `astream_chat` are available.
**Synchronous (`stream_chat`):**
Use this in standard Python scripts or notebooks where blocking operations are acceptable. It returns a generator directly.

```


stream_response = llm.stream_chat(messages)





for token in stream_response:




print(token.delta, end="", flush=True)


```

**Asynchronous (`astream_chat`):**
When using async frameworks (like FastAPI), remember to `await` the method call and iterate over the returned async stream.

```


stream_response =await llm.astream_chat(messages)





asyncfor token in stream_response:




print(token.delta, end="", flush=True)


```

## Specifying models
[Section titled “Specifying models”](https://developers.llamaindex.ai/python/framework/understanding/using_llms/#specifying-models)
Many LLM integrations provide more than one model. You can specify a model by passing the `model` parameter to the LLM constructor:

```


llm = OpenAI(model="gpt-4o-mini")




response = llm.complete("Who is Laurie Voss?")




print(response)


```

## Multi-Modal LLMs
[Section titled “Multi-Modal LLMs”](https://developers.llamaindex.ai/python/framework/understanding/using_llms/#multi-modal-llms)
Some LLMs support multi-modal chat messages. This means that you can pass in a mix of text and other modalities (images, audio, video, etc.) and the LLM will handle it.
Currently, LlamaIndex supports text, images, and audio inside ChatMessages using content blocks.

```


from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock




from llama_index.llms.openai import OpenAI





llm = OpenAI(model="gpt-4o")





messages = [




ChatMessage(




role="user",




blocks=[




ImageBlock(path="image.png"),




TextBlock(text="Describe the image in a few sentences."),








resp = llm.chat(messages)




print(resp.message.content)


```

## Tool Calling
[Section titled “Tool Calling”](https://developers.llamaindex.ai/python/framework/understanding/using_llms/#tool-calling)
Some LLMs (OpenAI, Anthropic, Gemini, Ollama, etc.) support tool calling directly over API calls — this means tools and functions can be called without specific prompts and parsing mechanisms.

```


from llama_index.core.tools import FunctionTool




from llama_index.llms.openai import OpenAI






defgenerate_song(name: str, artist: str) -> Song:




"""Generates a song with provided name and artist."""




return {"name": name, "artist": artist}






tool = FunctionTool.from_defaults(fn=generate_song)





llm = OpenAI(model="gpt-4o")




response = llm.predict_and_call(




[tool],




"Pick a random song for me",





print(str(response))


```

For more details on even more advanced tool calling, check out the in-depth guide using [OpenAI](https://developers.llamaindex.ai/python/examples/llm/openai). The same approaches work for any LLM that supports tools/functions (e.g. Anthropic, Gemini, Ollama, etc.).
You can learn more about tools and agents in the [tools guide](https://developers.llamaindex.ai/python/framework/understanding/agent/tools).
## Available LLMs
[Section titled “Available LLMs”](https://developers.llamaindex.ai/python/framework/understanding/using_llms/#available-llms)
We support integrations with OpenAI, Anthropic, Mistral, DeepSeek, Hugging Face, and dozens more. Check out our [module guide to LLMs](https://developers.llamaindex.ai/python/framework/module_guides/models/llms) for a full list, including how to run a local model.
### Using a local LLM
[Section titled “Using a local LLM”](https://developers.llamaindex.ai/python/framework/understanding/using_llms/#using-a-local-llm)
LlamaIndex doesn’t just support hosted LLM APIs; you can also run a local model such as Meta’s Llama 3 locally. For example, if you have [Ollama](https://github.com/ollama/ollama) installed and running:

```


from llama_index.llms.ollama import Ollama





llm = Ollama(




model="llama3.3",




request_timeout=60.0,




# Manually set the context window to limit memory usage




context_window=8000,



```

See the [custom LLM’s How-To](https://developers.llamaindex.ai/python/framework/module_guides/models/llms/usage_custom) for more details on using and configuring LLM models.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


