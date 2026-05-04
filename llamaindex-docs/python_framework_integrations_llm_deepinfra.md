[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/llm/deepinfra/#_top)
LlamaIndex Framework
Integrations
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# DeepInfra 
## Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/framework/integrations/llm/deepinfra/#installation)
First, install the necessary package:
Terminal window
```


%pipinstallllama-index-llms-deepinfra


```


```


%pip install llama-index-llms-deepinfra


```

## Initialization
[Section titled “Initialization”](https://developers.llamaindex.ai/python/framework/integrations/llm/deepinfra/#initialization)
Set up the `DeepInfraLLM` class with your API key and desired parameters:

```


from llama_index.llms.deepinfra import DeepInfraLLM




import asyncio





llm = DeepInfraLLM(




model="mistralai/Mixtral-8x22B-Instruct-v0.1"# Default model name




api_key="your-deepinfra-api-key"# Replace with your DeepInfra API key




temperature=0.5,




max_tokens=50,




additional_kwargs={"top_p": 0.9},



```

## Synchronous Complete
[Section titled “Synchronous Complete”](https://developers.llamaindex.ai/python/framework/integrations/llm/deepinfra/#synchronous-complete)
Generate a text completion synchronously using the `complete` method:

```


response = llm.complete("Hello World!")




print(response.text)


```

## Synchronous Stream Complete
[Section titled “Synchronous Stream Complete”](https://developers.llamaindex.ai/python/framework/integrations/llm/deepinfra/#synchronous-stream-complete)
Generate a streaming text completion synchronously using the `stream_complete` method:

```


content =""




for completion in llm.stream_complete("Once upon a time"):




content += completion.delta




print(completion.delta, end="")


```

## Synchronous Chat
[Section titled “Synchronous Chat”](https://developers.llamaindex.ai/python/framework/integrations/llm/deepinfra/#synchronous-chat)
Generate a chat response synchronously using the `chat` method:

```


from llama_index.core.base.llms.types import ChatMessage





messages = [




ChatMessage(role="user", content="Tell me a joke."),





chat_response = llm.chat(messages)




print(chat_response.message.content)


```

## Synchronous Stream Chat
[Section titled “Synchronous Stream Chat”](https://developers.llamaindex.ai/python/framework/integrations/llm/deepinfra/#synchronous-stream-chat)
Generate a streaming chat response synchronously using the `stream_chat` method:

```


messages = [




ChatMessage(role="system", content="You are a helpful assistant."),




ChatMessage(role="user", content="Tell me a story."),





content =""




for chat_response in llm.stream_chat(messages):




content += chat_response.message.delta




print(chat_response.message.delta, end="")


```

## Asynchronous Complete
[Section titled “Asynchronous Complete”](https://developers.llamaindex.ai/python/framework/integrations/llm/deepinfra/#asynchronous-complete)
Generate a text completion asynchronously using the `acomplete` method:

```


asyncdefasync_complete():




response =await llm.acomplete("Hello Async World!")




print(response.text)





asyncio.run(async_complete())

```

## Asynchronous Stream Complete
[Section titled “Asynchronous Stream Complete”](https://developers.llamaindex.ai/python/framework/integrations/llm/deepinfra/#asynchronous-stream-complete)
Generate a streaming text completion asynchronously using the `astream_complete` method:

```


asyncdefasync_stream_complete():




content =""




response =await llm.astream_complete("Once upon an async time")




asyncfor completion in response:




content += completion.delta




print(completion.delta, end="")





asyncio.run(async_stream_complete())

```

## Asynchronous Chat
[Section titled “Asynchronous Chat”](https://developers.llamaindex.ai/python/framework/integrations/llm/deepinfra/#asynchronous-chat)
Generate a chat response asynchronously using the `achat` method:

```


asyncdefasync_chat():




messages = [




ChatMessage(role="user", content="Tell me an async joke."),





chat_response =await llm.achat(messages)




print(chat_response.message.content)





asyncio.run(async_chat())

```

## Asynchronous Stream Chat
[Section titled “Asynchronous Stream Chat”](https://developers.llamaindex.ai/python/framework/integrations/llm/deepinfra/#asynchronous-stream-chat)
Generate a streaming chat response asynchronously using the `astream_chat` method:

```


asyncdefasync_stream_chat():




messages = [




ChatMessage(role="system", content="You are a helpful assistant."),




ChatMessage(role="user", content="Tell me an async story."),





content =""




response =await llm.astream_chat(messages)




asyncfor chat_response in response:




content += chat_response.message.delta




print(chat_response.message.delta, end="")





asyncio.run(async_stream_chat())

```

For any questions or feedback, please contact us at feedback@deepinfra.com.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


