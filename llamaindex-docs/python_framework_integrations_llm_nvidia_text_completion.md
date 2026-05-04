[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia_text_completion/#_top)
LlamaIndex Framework
Integrations
[NVIDIA LLM Text Completion API ](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia_text_completion/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# NVIDIA LLM Text Completion API 
The `llama-index-llms-nvidia` package extends the `NVIDIA` class to support the `/completions` API for code completion models such as:
  * `bigcode/starcoder2-7b`
  * `bigcode/starcoder2-15b`


## Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia_text_completion/#installation)

```


%pip install --upgrade --quiet llama-index-llms-nvidia


```

## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia_text_completion/#setup)
**To get started:**
  1. Create a free account with [NVIDIA](https://build.nvidia.com/), which hosts NVIDIA AI Foundation models.
  2. Click on your model of choice.
  3. Under Input select the Python tab, and click `Get API Key`. Then click `Generate Key`.
  4. Copy and save the generated key as NVIDIA_API_KEY. From there, you should have access to the endpoints.



```


import getpass




import os




# del os.environ['NVIDIA_API_KEY']  ## delete key and reset



if os.environ.get("NVIDIA_API_KEY", "").startswith("nvapi-"):




print("Valid NVIDIA_API_KEY already in environment. Delete to reset")




else:




nvapi_key = getpass.getpass("NVAPI Key (starts with nvapi-): ")




assert nvapi_key.startswith(




"nvapi-"




), f"{nvapi_key[:5]}... is not a valid key"




os.environ["NVIDIA_API_KEY"] = nvapi_key


```


```

# llama-parse is async-first, running the async code in a notebook requires the use of nest_asyncio



import nest_asyncio




nest_asyncio.apply()

```

## Working with the NVIDIA API Catalog
[Section titled “Working with the NVIDIA API Catalog”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia_text_completion/#working-with-the-nvidia-api-catalog)
### Usage of the `use_chat_completions` argument
[Section titled “Usage of the use_chat_completions argument”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia_text_completion/#usage-of-the-use_chat_completions-argument)
Set `None` (default) to decide per-invocation whether to use `/chat/completions` or `/completions` endpoints with query keyword arguments.
  * Set `False` to use the `/completions` endpoint.
  * Set `True` to use the `/chat/completions` endpoint.



```


from llama_index.llms.nvidia importNVIDIA





llm = NVIDIA(model="bigcode/starcoder2-15b", use_chat_completions=False)


```

### Available models
[Section titled “Available models”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia_text_completion/#available-models)
Use `is_chat_model` to filter available text completion models:

```


print([model for model in llm.available_models if model.is_chat_model])


```

## Working with NVIDIA NIMs
[Section titled “Working with NVIDIA NIMs”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia_text_completion/#working-with-nvidia-nims)
In addition to connecting to hosted [NVIDIA NIMs](https://ai.nvidia.com), this connector can be used to connect to local NIM instances. This helps you take your applications local when necessary.
For instructions on how to set up local NIM instances, refer to [NVIDIA NIM](https://developer.nvidia.com/nim).

```


from llama_index.llms.nvidia importNVIDIA




# Connect to a NIM running at localhost:8080



llm = NVIDIA(base_url="http://localhost:8080/v1")


```

### Complete: `.complete()`
[Section titled “Complete: .complete()”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia_text_completion/#complete-complete)
We can use `.complete()`/`.acomplete()` (which takes a string) to prompt a response from the selected model.
Let’s use our default model for this task.

```


print(llm.complete("# Function that does quicksort:"))


```

As expected, LlamaIndex returns a `CompletionResponse`.
#### Async Complete: `.acomplete()`
[Section titled “Async Complete: .acomplete()”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia_text_completion/#async-complete-acomplete)
There is also an async implementation which can be leveraged in the same way!

```


await llm.acomplete("# Function that does quicksort:")


```

#### Streaming
[Section titled “Streaming”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia_text_completion/#streaming)

```


x = llm.stream_complete(prompt="# Reverse string in python:", max_tokens=512)


```


```


forin x:




print(t.delta, end="")


```

#### Async Streaming
[Section titled “Async Streaming”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia_text_completion/#async-streaming)

```


x =await llm.astream_complete(




prompt="# Reverse program in python:", max_tokens=512



```


```


asyncforin x:




print(t.delta, end="")


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


