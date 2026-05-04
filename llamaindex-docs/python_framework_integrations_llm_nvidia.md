[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia/#_top)
LlamaIndex Framework
Integrations
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# NVIDIA NIMs 
The `llama-index-llms-nvidia` package contains LlamaIndex integrations for chat models and embeddings powered by [NVIDIA AI Foundation Models](https://www.nvidia.com/en-us/ai-data-science/foundation-models/), and hosted on the [NVIDIA API Catalog](https://build.nvidia.com/). NVIDIA AI Foundation models are community- and NVIDIA-built models that are optimized to deliver the best performance on NVIDIA-accelerated infrastructure. You can use the API to query live endpoints that are available on the NVIDIA API Catalog to get quick results from a DGX-hosted cloud compute environment, or you can download models from NVIDIA’s API catalog with NVIDIA NIM, which is included with the NVIDIA AI Enterprise license. The ability to run models on-premises gives your enterprise ownership of your customizations and full control of your IP and AI application.
NIMs can be exported from NVIDIA’s API catalog using the NVIDIA AI Enterprise license and run on-premises or in the cloud,
NIMs are packaged as container images on a per model basis and are distributed as NGC container images through the NVIDIA NGC Catalog. At their core, NIMs provide easy, consistent, and familiar APIs for running inference on an AI model.
# NVIDIA’s LLM connector
[Section titled “NVIDIA’s LLM connector”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia/#nvidias-llm-connector)
This example goes over how to use LlamaIndex to interact with and develop LLM-powered systems using the publicly-accessible AI Foundation endpoints.
With this connector, you’ll be able to connect to and generate from compatible models available as hosted [NVIDIA NIMs](https://ai.nvidia.com), such as:
  * Google’s [gemma-7b](https://build.nvidia.com/google/gemma-7b)
  * Mistal AI’s [mistral-7b-instruct-v0.2](https://build.nvidia.com/mistralai/mistral-7b-instruct-v2)
  * And more!


## Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia/#installation)

```


%pip install --upgrade --quiet llama-index-llms-nvidia llama-index-embeddings-nvidia llama-index-readers-file


```

## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia/#setup)
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

## Working with NVIDIA API Catalog
[Section titled “Working with NVIDIA API Catalog”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia/#working-with-nvidia-api-catalog)

```


from llama_index.llms.nvidia importNVIDIA




from llama_index.core.llms import ChatMessage, MessageRole





llm = NVIDIA()





messages = [




ChatMessage(




role=MessageRole.SYSTEM, content=("You are a helpful assistant.")





ChatMessage(




role=MessageRole.USER,




content=("What are the most popular house pets in North America?"),






llm.chat(messages)

```

## Working with NVIDIA NIMs
[Section titled “Working with NVIDIA NIMs”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia/#working-with-nvidia-nims)
In addition to connecting to hosted [NVIDIA NIMs](https://ai.nvidia.com), this connector can be used to connect to local microservice instances. This helps you take your applications local when necessary.
For instructions on how to setup local microservice instances, see <https://developer.nvidia.com/blog/nvidia-nim-offers-optimized-inference-microservices-for-deploying-ai-models-at-scale/>

```


from llama_index.llms.nvidia importNVIDIA




# connect to an chat NIM running at localhost:8080, spcecifying a specific model



llm = NVIDIA(




base_url="http://localhost:8080/v1", model="meta/llama3-8b-instruct"



```

## Loading a specific model
[Section titled “Loading a specific model”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia/#loading-a-specific-model)
Now we can load our `NVIDIA` LLM by passing in the model name, as found in the docs - located [here](https://docs.api.nvidia.com/nim/reference/)
> NOTE: The default model is `meta/llama3-8b-instruct`.

```

# default model



llm = NVIDIA()



llm.model

```

We can observe which model our `llm` object is currently associated with the `.model` attribute.

```


llm = NVIDIA(model="mistralai/mistral-7b-instruct-v0.2")



llm.model

```

## Basic Functionality
[Section titled “Basic Functionality”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia/#basic-functionality)
Now we can explore the different ways you can use the connector within the LlamaIndex ecosystem!
Before we begin, lets set up a list of `ChatMessage` objects - which is the expected input for some of the methods.
We’ll follow the same basic pattern for each example:
  1. We’ll point our `NVIDIA` LLM to our desired model
  2. We’ll examine how to use the endpoint to achieve the desired task!


### Complete: `.complete()`
[Section titled “Complete: .complete()”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia/#complete-complete)
We can use `.complete()`/`.acomplete()` (which takes a string) to prompt a response from the selected model.
Let’s use our default model for this task.

```


completion_llm = NVIDIA()


```

We can verify this is the expected default by checking the `.model` attribute.

```

completion_llm.model

```

Let’s call `.complete()` on our model with a string, in this case `"Hello!"`, and observe the response.

```


completion_llm.complete("Hello!")


```

As is expected by LlamaIndex - we get a `CompletionResponse` in response.
#### Async Complete: `.acomplete()`
[Section titled “Async Complete: .acomplete()”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia/#async-complete-acomplete)
There is also an async implementation which can be leveraged in the same way!

```


await completion_llm.acomplete("Hello!")


```

#### Chat: `.chat()`
[Section titled “Chat: .chat()”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia/#chat-chat)
Now we can try the same thing using the `.chat()` method. This method expects a list of chat messages - so we’ll use the one we created above.
We’ll use the `mistralai/mixtral-8x7b-instruct-v0.1` model for the example.

```


chat_llm = NVIDIA(model="mistralai/mixtral-8x7b-instruct-v0.1")


```

All we need to do now is call `.chat()` on our list of `ChatMessages` and observe our response.
You’ll also notice that we can pass in a few additional key-word arguments that can influence the generation - in this case, we’ve used the `seed` parameter to influence our generation and the `stop` parameter to indicate we want the model to stop generating once it reaches a certain token!
> NOTE: You can find information about what additional kwargs are supported by the model’s endpoint by referencing the API documentation for the selected model. Mixtral’s is located [here](https://docs.api.nvidia.com/nim/reference/mistralai-mixtral-8x7b-instruct-infer) as an example!

```


chat_llm.chat(messages, seed=4, stop=["cat", "cats", "Cat", "Cats"])


```

As expected, we receive a `ChatResponse` in response.
#### Async Chat: (`achat`)
[Section titled “Async Chat: (achat)”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia/#async-chat-achat)
We also have an async implementation of the `.chat()` method which can be called in the following way.

```


await chat_llm.achat(messages)


```

### Stream: `.stream_chat()`
[Section titled “Stream: .stream_chat()”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia/#stream-stream_chat)
We can also use the models found on `build.nvidia.com` for streaming use-cases!
Let’s select another model and observe this behaviour. We’ll use Google’s `gemma-7b` model for this task.

```


stream_llm = NVIDIA(model="google/gemma-7b")


```

Let’s call our model with `.stream_chat()`, which again expects a list of `ChatMessage` objects, and capture the response.

```


streamed_response = stream_llm.stream_chat(messages)


```


```

streamed_response

```

As we can see, the response is a generator with the streamed response.
Let’s take a look at the final response once the generation is complete.

```


last_element =None




for last_element in streamed_response:




pass





print(last_element)


```

#### Async Stream: `.astream_chat()`
[Section titled “Async Stream: .astream_chat()”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia/#async-stream-astream_chat)
We have the equivalent async method for streaming as well, which can be used in a similar way to the sync implementation.

```


streamed_response =await stream_llm.astream_chat(messages)


```


```

streamed_response

```


```


last_element =None




asyncfor last_element in streamed_response:




pass





print(last_element)


```

## Streaming Query Engine Responses
[Section titled “Streaming Query Engine Responses”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia/#streaming-query-engine-responses)
Let’s look at a slightly more involved example using a query engine!
We’ll start by loading some data (we’ll be using the [Hitchhiker’s Guide to the Galaxy](https://web.eecs.utk.edu/~hqi/deeplearning/project/hhgttg.txt)).
### Loading Data
[Section titled “Loading Data”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia/#loading-data)
Let’s first create a directory where our data can live.

```


!mkdir -p 'data/hhgttg'


```

We’ll download our data from the above source.

```


!wget 'https://web.eecs.utk.edu/~hqi/deeplearning/project/hhgttg.txt'-O 'data/hhgttg/hhgttg.txt'


```

We’ll need to have an embedding model for this step! We’ll use NVIDIA `NV-Embed-QA` model to achieve this, and save it in our `Settings`.

```


from llama_index.embeddings.nvidia import NVIDIAEmbedding




from llama_index.core import Settings





embedder = NVIDIAEmbedding(model="NV-Embed-QA", truncate="END")




Settings.embed_model = embedder


```

Now we can load our document and create an index leveraging the above

```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader





documents = SimpleDirectoryReader("data/hhgttg").load_data()




index = VectorStoreIndex.from_documents(documents)


```

Now we can create a simple query engine and set our `streaming` parameter to `True`.

```


streaming_qe = index.as_query_engine(streaming=True)


```

Let’s send a query to our query engine, and then stream the response.

```


streaming_response = streaming_qe.query(




"What is the significance of the number 42?",



```


```

streaming_response.print_response_stream()

```

### Tool calling
[Section titled “Tool calling”](https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia/#tool-calling)
Starting in v0.2.1, NVIDIA supports tool calling.
NVIDIA provides integration with the variety of models on build.nvidia.com as well as local NIMs. Not all these models are trained for tool calling. Be sure to select a model that does have tool calling for your experimention and applications.
You can get a list of models that are known to support tool calling with,
`NOTE:` For more examples refer : [nvidia_agent.ipynb](https://developers.llamaindex.ai/python/framework/integrations/llm/agent/nvidia_agent.ipynb)

```


tool_models = [




model




for model in NVIDIA().available_models




if model.is_function_calling_model



```

With a tool capable model,

```


from llama_index.core.tools import FunctionTool






defmultiply(a: int, b: int) -> int:




"""Multiple two integers and returns the result integer"""




return* b






multiply_tool = FunctionTool.from_defaults(fn=multiply)






defadd(a: int, b: int) -> int:




"""Add two integers and returns the result integer"""




return+ b






add_tool = FunctionTool.from_defaults(fn=add)





llm = NVIDIA("meta/llama-3.1-70b-instruct")




from llama_index.core.agent import FunctionAgent





agent_worker = FunctionAgent(




tools=[multiply_tool, add_tool],




llm=llm,






response =await agent.run("What is (121 * 3) + 42?")




print(str(response))


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


