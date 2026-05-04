[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/llm/nebius/#_top)
LlamaIndex Framework
Integrations
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Nebius LLMs 
This notebook demonstrates how to use LLMs from [Nebius AI Studio](https://studio.nebius.ai/) with LlamaIndex. Nebius AI Studio implements all state-of-the-art LLMs available for commercial use.
First, let’s install LlamaIndex and dependencies of Nebius AI Studio.

```


%pip install llama-index-llms-nebius llama-index


```

Upload your Nebius AI Studio key from system variables below or simply insert it. You can get it by registering for free at [Nebius AI Studio](https://auth.eu.nebius.com/ui/login) and issuing the key at [API Keys section](https://studio.nebius.ai/settings/api-keys).”

```


import os





NEBIUS_API_KEY= os.getenv("NEBIUS_API_KEY"# NEBIUS_API_KEY = ""


```


```


from llama_index.llms.nebius import NebiusLLM





llm = NebiusLLM(




api_key=NEBIUS_API_KEY, model="meta-llama/Llama-3.3-70B-Instruct-fast"



```


```

None of PyTorch, TensorFlow >= 2.0, or Flax have been found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.

```

#### Call `complete` with a prompt
[Section titled “Call complete with a prompt”](https://developers.llamaindex.ai/python/framework/integrations/llm/nebius/#call-complete-with-a-prompt)

```


response = llm.complete("Amsterdam is the capital of ")




print(response)


```


```

The Netherlands! Amsterdam is indeed the capital and largest city of the Netherlands.

```

#### Call `chat` with a list of messages
[Section titled “Call chat with a list of messages”](https://developers.llamaindex.ai/python/framework/integrations/llm/nebius/#call-chat-with-a-list-of-messages)

```


from llama_index.core.llms import ChatMessage





messages = [




ChatMessage(role="system", content="You are a helpful AI assistant."),




ChatMessage(




role="user",




content="Answer briefly: who is Wall-e?",






response = llm.chat(messages)




print(response)


```


```

assistant: WALL-E is a small waste-collecting robot and the main character in the 2008 Pixar animated film of the same name.

```

### Streaming
[Section titled “Streaming”](https://developers.llamaindex.ai/python/framework/integrations/llm/nebius/#streaming)
#### Using `stream_complete` endpoint
[Section titled “Using stream_complete endpoint”](https://developers.llamaindex.ai/python/framework/integrations/llm/nebius/#using-stream_complete-endpoint)

```


response = llm.stream_complete("Amsterdam is the capital of ")




forin response:




print(r.delta, end="")


```


```

The Netherlands! Amsterdam is indeed the capital and largest city of the Netherlands.

```

#### Using `stream_chat` with a list of messages
[Section titled “Using stream_chat with a list of messages”](https://developers.llamaindex.ai/python/framework/integrations/llm/nebius/#using-stream_chat-with-a-list-of-messages)

```


from llama_index.core.llms import ChatMessage





messages = [




ChatMessage(role="system", content="You are a helpful AI assistant."),




ChatMessage(




role="user",




content="Answer briefly: who is Wall-e?",






response = llm.stream_chat(messages)




forin response:




print(r.delta, end="")


```


```

WALL-E is a small waste-collecting robot and the main character in the 2008 Pixar animated film of the same name.

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


