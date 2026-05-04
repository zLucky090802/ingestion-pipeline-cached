[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/llm/databricks/#_top)
LlamaIndex Framework
Integrations
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Databricks 
Integrate with Databricks LLMs APIs.
## Pre-requisites
[Section titled “Pre-requisites”](https://developers.llamaindex.ai/python/framework/integrations/llm/databricks/#pre-requisites)
  * [Databricks personal access token](https://docs.databricks.com/en/dev-tools/auth/pat.html) to query and access Databricks model serving endpoints.
  * [Databricks workspace](https://docs.databricks.com/en/workspace/index.html) in a [supported region](https://docs.databricks.com/en/machine-learning/model-serving/model-serving-limits.html#regions) for Foundation Model APIs pay-per-token.


## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/framework/integrations/llm/databricks/#setup)
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


% pip install llama-index-llms-databricks


```


```


!pip install llama-index


```


```


from llama_index.llms.databricks import Databricks


```


```

None of PyTorch, TensorFlow >= 2.0, or Flax have been found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.

```

Terminal window
```


export DATABRICKS_TOKEN=<your api key>




export DATABRICKS_SERVING_ENDPOINT=<your api serving endpoint>


```

Alternatively, you can pass your API key and serving endpoint to the LLM when you init it:

```


llm = Databricks(




model="databricks-dbrx-instruct",




api_key="your_api_key",




api_base="https://[your-work-space].cloud.databricks.com/serving-endpoints/",



```

A list of available LLM models can be found [here](https://console.groq.com/docs/models).

```


response = llm.complete("Explain the importance of open source LLMs")


```


```


print(response)


```

#### Call `chat` with a list of messages
[Section titled “Call chat with a list of messages”](https://developers.llamaindex.ai/python/framework/integrations/llm/databricks/#call-chat-with-a-list-of-messages)

```


from llama_index.core.llms import ChatMessage





messages = [




ChatMessage(




role="system", content="You are a pirate with a colorful personality"





ChatMessage(role="user", content="What is your name"),





resp = llm.chat(messages)


```


```


print(resp)


```

### Streaming
[Section titled “Streaming”](https://developers.llamaindex.ai/python/framework/integrations/llm/databricks/#streaming)
Using `stream_complete` endpoint

```


response = llm.stream_complete("Explain the importance of open source LLMs")


```


```


forin response:




print(r.delta, end="")


```

Using `stream_chat` endpoint

```


from llama_index.core.llms import ChatMessage





messages = [




ChatMessage(




role="system", content="You are a pirate with a colorful personality"





ChatMessage(role="user", content="What is your name"),





resp = llm.stream_chat(messages)


```


```


forin resp:




print(r.delta, end="")


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


