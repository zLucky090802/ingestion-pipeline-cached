[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/llm/octoai/#_top)
LlamaIndex Framework
Integrations
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# OctoAI 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-llms-octoai




%pip install llama-index




%pip install octoai-sdk


```

Include your OctoAI API key below. You can get yours at [OctoAI](https://octo.ai).
[Here](https://octo.ai/docs/getting-started/how-to-create-an-octoai-access-token) are some instructions in case you need more guidance.

```


OCTOAI_API_KEY=""


```

#### Initialize the Integration with the default model
[Section titled “Initialize the Integration with the default model”](https://developers.llamaindex.ai/python/framework/integrations/llm/octoai/#initialize-the-integration-with-the-default-model)

```


from llama_index.llms.octoai import OctoAI





octoai = OctoAI(token=OCTOAI_API_KEY)


```

#### Call `complete` with a prompt
[Section titled “Call complete with a prompt”](https://developers.llamaindex.ai/python/framework/integrations/llm/octoai/#call-complete-with-a-prompt)

```


response = octoai.complete("Paul Graham is ")




print(response)


```

#### Call `chat` with a list of messages
[Section titled “Call chat with a list of messages”](https://developers.llamaindex.ai/python/framework/integrations/llm/octoai/#call-chat-with-a-list-of-messages)

```


from llama_index.core.llms import ChatMessage





messages = [




ChatMessage(




role="system",




content="Below is an instruction that describes a task. Write a response that appropriately completes the request.",





ChatMessage(role="user", content="Write a blog about Seattle"),





response = octoai.chat(messages)




print(response)


```

## Streaming
[Section titled “Streaming”](https://developers.llamaindex.ai/python/framework/integrations/llm/octoai/#streaming)
Using `stream_complete` endpoint

```


response = octoai.stream_complete("Paul Graham is ")




forin response:




print(r.delta, end="")


```

Using `stream_chat` with a list of messages

```


from llama_index.core.llms import ChatMessage





messages = [




ChatMessage(




role="system",




content="Below is an instruction that describes a task. Write a response that appropriately completes the request.",





ChatMessage(role="user", content="Write a blog about Seattle"),





response = octoai.stream_chat(messages)




forin response:




print(r.delta, end="")


```

## Configure Model
[Section titled “Configure Model”](https://developers.llamaindex.ai/python/framework/integrations/llm/octoai/#configure-model)

```

# To customize your API token, do this


# otherwise it will lookup OCTOAI_TOKEN from your env variable



octoai = OctoAI(




model="mistral-7b-instruct", max_tokens=128, token=OCTOAI_API_KEY






response = octoai.complete("Paul Graham is ")




print(response)


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


