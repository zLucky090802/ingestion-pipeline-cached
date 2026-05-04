[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#_top)
LlamaIndex Framework
Integrations
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# SambaNova Systems 
In this notebook you will know how to install, setup and use the [SambaNova Cloud](https://cloud.sambanova.ai/) and [SambaStudio](https://docs.sambanova.ai/sambastudio/latest/sambastudio-intro.html) platforms. Take a look and try it yourself!
# SambaNova Cloud
[Section titled “SambaNova Cloud”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#sambanova-cloud)
[SambaNova Cloud](https://cloud.sambanova.ai/) is a high-performance inference service that delivers rapid and precise results. Customers can seamlessly leverage SambaNova technology to enhance their user experience by integrating FastAPI inference APIs with their applications. This service provides an easy-to-use REST interface for streaming the inference results. Users are able to customize the inference parameters and pass the ML model on to the service.
## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#setup)
To access SambaNova Cloud model you will need to create a [SambaNovaCloud](https://cloud.sambanova.ai/apis) account, get an API key, install the `llama-index-llms-sambanova` integration package, and install the `SSEClient` Package.

```


%pip install llama-index-llms-sambanovasystems




%pip install sseclient-py


```

### Credentials
[Section titled “Credentials”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#credentials)
Get an API Key from [cloud.sambanova.ai](https://cloud.sambanova.ai/apis) and add it to your environment variables:
Terminal window
```


export SAMBANOVA_API_KEY="your-api-key-here"


```

If you don’t have it in your env variables, you can also add it in the pop-up input text.

```


import getpass




import os





ifnot os.getenv("SAMBANOVA_API_KEY"):




os.environ["SAMBANOVA_API_KEY"] = getpass.getpass(




"Enter your SambaNova Cloud API key: "



```

## Instantiation
[Section titled “Instantiation”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#instantiation)
Now we can instantiate our model object and generate chat completions:

```


from llama_index.llms.sambanovasystems import SambaNovaCloud





llm = SambaNovaCloud(




model="Meta-Llama-3.1-70B-Instruct",




context_window=100000,




max_tokens=1024,




temperature=0.7,




top_k=1,




top_p=0.01,



```

## Invocation
[Section titled “Invocation”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#invocation)
Given the following system and user messages, let’s explore different ways of calling a SambaNova Cloud model.

```


from llama_index.core.base.llms.types import (




ChatMessage,




MessageRole,






system_msg = ChatMessage(




role=MessageRole.SYSTEM,




content="You are a helpful assistant that translates English to French. Translate the user sentence.",





user_msg = ChatMessage(role=MessageRole.USER, content="I love programming.")





messages = [




system_msg,




user_msg,



```

### Chat
[Section titled “Chat”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#chat)

```


ai_msg = llm.chat(messages)



ai_msg.message

```


```


print(ai_msg.message.content)


```

### Complete
[Section titled “Complete”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#complete)

```


ai_msg = llm.complete(user_msg.content)



ai_msg

```


```


print(ai_msg.text)


```

## Streaming
[Section titled “Streaming”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#streaming)
### Chat
[Section titled “Chat”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#chat-1)

```


ai_stream_msgs = []




for stream in llm.stream_chat(messages):




ai_stream_msgs.append(stream)



ai_stream_msgs

```


```


print(ai_stream_msgs[-1])


```

### Complete
[Section titled “Complete”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#complete-1)

```


ai_stream_msgs = []




for stream in llm.stream_complete(user_msg.content):




ai_stream_msgs.append(stream)



ai_stream_msgs

```


```


print(ai_stream_msgs[-1])


```

## Async
[Section titled “Async”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#async)
### Chat
[Section titled “Chat”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#chat-2)

```


ai_msg =await llm.achat(messages)



ai_msg

```


```


print(ai_msg.message.content)


```

### Complete
[Section titled “Complete”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#complete-2)

```


ai_msg =await llm.acomplete(user_msg.content)



ai_msg

```


```


print(ai_msg.text)


```

## Async Streaming
[Section titled “Async Streaming”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#async-streaming)
Not supported yet. Coming soon!
# SambaStudio
[Section titled “SambaStudio”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#sambastudio)
[SambaStudio](https://docs.sambanova.ai/sambastudio/latest/sambastudio-intro.html) is a rich, GUI-based platform that provides the functionality to train, deploy, and manage models.
## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#setup-1)
To access SambaStudio models you will need to be a **SambaNova customer** , deploy an endpoint using the GUI or CLI, and use the URL and API Key to connect to the endpoint, as described in the [SambaStudio endpoint documentation](https://docs.sambanova.ai/sambastudio/latest/endpoints.html#_endpoint_api_keys). Then, install the `llama-index-llms-sambanova` integration package, and install the `SSEClient` Package.

```


%pip install llama-index-llms-sambanova




%pip install sseclient-py


```

### Credentials
[Section titled “Credentials”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#credentials-1)
An endpoint must be deployed in SambaStudio to get the URL and API Key. Once they’re available, include them to your environment variables:
Terminal window
```


export SAMBASTUDIO_URL="your-url-here"




export SAMBASTUDIO_API_KEY="your-api-key-here"


```


```


import getpass




import os





ifnot os.getenv("SAMBASTUDIO_URL"):




os.environ["SAMBASTUDIO_URL"] = getpass.getpass(




"Enter your SambaStudio endpoint's URL: "






ifnot os.getenv("SAMBASTUDIO_API_KEY"):




os.environ["SAMBASTUDIO_API_KEY"] = getpass.getpass(




"Enter your SambaStudio endpoint's API key: "



```

## Instantiation
[Section titled “Instantiation”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#instantiation-1)
Now we can instantiate our model object and generate chat completions:

```


from llama_index.llms.sambanovasystems import SambaStudio





llm = SambaStudio(




model="Meta-Llama-3-70B-Instruct-4096",




context_window=100000,




max_tokens=1024,




temperature=0.7,




top_k=1,




top_p=0.01,



```

## Invocation
[Section titled “Invocation”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#invocation-1)
Given the following system and user messages, let’s explore different ways of calling a SambaNova Cloud model.

```


from llama_index.core.base.llms.types import (




ChatMessage,




MessageRole,






system_msg = ChatMessage(




role=MessageRole.SYSTEM,




content="You are a helpful assistant that translates English to French. Translate the user sentence.",





user_msg = ChatMessage(role=MessageRole.USER, content="I love programming.")





messages = [




system_msg,




user_msg,



```

### Chat
[Section titled “Chat”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#chat-3)

```


ai_msg = llm.chat(messages)



ai_msg.message

```


```


print(ai_msg.message.content)


```

### Complete
[Section titled “Complete”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#complete-3)

```


ai_msg = llm.complete(user_msg.content)



ai_msg

```


```


print(ai_msg.text)


```

## Streaming
[Section titled “Streaming”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#streaming-1)
### Chat
[Section titled “Chat”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#chat-4)

```


ai_stream_msgs = []




for stream in llm.stream_chat(messages):




ai_stream_msgs.append(stream)



ai_stream_msgs

```


```


print(ai_stream_msgs[-1])


```

### Complete
[Section titled “Complete”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#complete-4)

```


ai_stream_msgs = []




for stream in llm.stream_complete(user_msg.content):




ai_stream_msgs.append(stream)



ai_stream_msgs

```


```


print(ai_stream_msgs[-1])


```

## Async
[Section titled “Async”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#async-1)
### Chat
[Section titled “Chat”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#chat-5)

```


ai_msg =await llm.achat(messages)



ai_msg

```


```


print(ai_msg.message.content)


```

### Complete
[Section titled “Complete”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#complete-5)

```


ai_msg =await llm.acomplete(user_msg.content)



ai_msg

```


```


print(ai_msg.text)


```

## Async Streaming
[Section titled “Async Streaming”](https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/#async-streaming-1)
Not supported yet. Coming soon!
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


