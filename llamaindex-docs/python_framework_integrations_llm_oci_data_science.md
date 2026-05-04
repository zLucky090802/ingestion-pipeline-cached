[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/#_top)
LlamaIndex Framework
Integrations
[Oracle Cloud Infrastructure Data Science ](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Oracle Cloud Infrastructure Data Science 
Oracle Cloud Infrastructure [(OCI) Data Science](https://www.oracle.com/artificial-intelligence/data-science) is a fully managed, serverless platform for data science teams to build, train, and manage machine learning models in Oracle Cloud Infrastructure.
It offers [AI Quick Actions](https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions.htm), which can be used to deploy, evaluate, and fine-tune foundation LLM models in OCI Data Science. AI Quick Actions target users who want to quickly leverage the capabilities of AI. They aim to expand the reach of foundation models to a broader set of users by providing a streamlined, code-free, and efficient environment for working with foundation models. AI Quick Actions can be accessed from the Data Science Notebook.
Detailed documentation on how to deploy LLM models in OCI Data Science using AI Quick Actions is available [here](https://github.com/oracle-samples/oci-data-science-ai-samples/blob/main/ai-quick-actions/model-deployment-tips.md) and [here](https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions-model-deploy.htm).
This notebook explains how to use OCI’s Data Science models with LlamaIndex.
## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/#setup)
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-llms-oci-data-science


```


```


!pip install llama-index


```

You will also need to install the [oracle-ads](https://accelerated-data-science.readthedocs.io/en/latest/index.html) SDK.

```


!pip install -U oracle-ads


```

## Authentication
[Section titled “Authentication”](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/#authentication)
The authentication methods supported for LlamaIndex are equivalent to those used with other OCI services and follow the standard SDK authentication methods, specifically API Key, session token, instance principal, and resource principal. More details can be found [here](https://accelerated-data-science.readthedocs.io/en/latest/user_guide/cli/authentication.html). Make sure to have the required [policies](https://docs.oracle.com/en-us/iaas/data-science/using/model-dep-policies-auth.htm) to access the OCI Data Science Model Deployment endpoint. The [oracle-ads](https://accelerated-data-science.readthedocs.io/en/latest/index.html) helps to simplify the authentication within OCI Data Science.
## Basic Usage
[Section titled “Basic Usage”](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/#basic-usage)
Using LLMs offered by OCI Data Science AI with LlamaIndex only requires you to initialize the `OCIDataScience` interface with your Data Science Model Deployment endpoint and model ID. By default the all deployed models in AI Quick Actions get `odsc-model` ID. However this ID cna be changed during the deployment.
#### Call `complete` with a prompt
[Section titled “Call complete with a prompt”](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/#call-complete-with-a-prompt)

```


import ads




from llama_index.llms.oci_data_science import OCIDataScience





ads.set_auth(auth="security_token", profile="<replace-with-your-profile>")





llm = OCIDataScience(




model="odsc-llm",




endpoint="https://<MD_OCID>/predict",





response = llm.complete("Tell me a joke")





print(response)


```

### Call `chat` with a list of messages
[Section titled “Call chat with a list of messages”](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/#call-chat-with-a-list-of-messages)

```


import ads




from llama_index.llms.oci_data_science import OCIDataScience




from llama_index.core.base.llms.types import ChatMessage





ads.set_auth(auth="security_token", profile="<replace-with-your-profile>")





llm = OCIDataScience(




model="odsc-llm",




endpoint="https://<MD_OCID>/predict",





response = llm.chat(





ChatMessage(role="user", content="Tell me a joke"),




ChatMessage(




role="assistant", content="Why did the chicken cross the road?"





ChatMessage(role="user", content="I don't know, why?"),







print(response)


```

## Streaming
[Section titled “Streaming”](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/#streaming)
**Using Dedicated Streaming endpoint**

```


from llama_index.llms.oci_data_science import OCIDataScience




import ads





ads.set_auth(auth="security_token", profile="OC1")





llm = OCIDataScience(




endpoint="https://<MD_OCID>/predictWithResponseStream",




model="odsc-llm",






prompt ="What is the capital of France?"




response = llm.stream_complete(prompt)




for chunk in response:




print(chunk.delta, end="")


```

### Using `stream_complete` endpoint
[Section titled “Using stream_complete endpoint”](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/#using-stream_complete-endpoint)

```


import ads




from llama_index.llms.oci_data_science import OCIDataScience





ads.set_auth(auth="security_token", profile="<replace-with-your-profile>")





llm = OCIDataScience(




model="odsc-llm",




endpoint="https://<MD_OCID>/predict",






for chunk in llm.stream_complete("Tell me a joke"):




print(chunk.delta, end="")


```

### Using `stream_chat` endpoint
[Section titled “Using stream_chat endpoint”](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/#using-stream_chat-endpoint)

```


import ads




from llama_index.llms.oci_data_science import OCIDataScience




from llama_index.core.base.llms.types import ChatMessage





ads.set_auth(auth="security_token", profile="<replace-with-your-profile>")





llm = OCIDataScience(




model="odsc-llm",




endpoint="https://<MD_OCID>/predict",





response = llm.stream_chat(





ChatMessage(role="user", content="Tell me a joke"),




ChatMessage(




role="assistant", content="Why did the chicken cross the road?"





ChatMessage(role="user", content="I don't know, why?"),







for chunk in response:




print(chunk.delta, end="")


```

## Async
[Section titled “Async”](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/#async)
### Call `acomplete` with a prompt
[Section titled “Call acomplete with a prompt”](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/#call-acomplete-with-a-prompt)

```


import ads




from llama_index.llms.oci_data_science import OCIDataScience





ads.set_auth(auth="security_token", profile="<replace-with-your-profile>")





llm = OCIDataScience(




model="odsc-llm",




endpoint="https://<MD_OCID>/predict",





response =await llm.acomplete("Tell me a joke")





print(response)


```

### Call `achat` with a list of messages
[Section titled “Call achat with a list of messages”](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/#call-achat-with-a-list-of-messages)

```


import ads




from llama_index.llms.oci_data_science import OCIDataScience




from llama_index.core.base.llms.types import ChatMessage





ads.set_auth(auth="security_token", profile="<replace-with-your-profile>")





llm = OCIDataScience(




model="odsc-llm",




endpoint="https://<MD_OCID>/predict",





response =await llm.achat(





ChatMessage(role="user", content="Tell me a joke"),




ChatMessage(




role="assistant", content="Why did the chicken cross the road?"





ChatMessage(role="user", content="I don't know, why?"),







print(response)


```

### Using `astream_complete` endpoint
[Section titled “Using astream_complete endpoint”](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/#using-astream_complete-endpoint)

```


import ads




from llama_index.llms.oci_data_science import OCIDataScience





ads.set_auth(auth="security_token", profile="<replace-with-your-profile>")





llm = OCIDataScience(




model="odsc-llm",




endpoint="https://<MD_OCID>/predict",






asyncfor chunk inawait llm.astream_complete("Tell me a joke"):




print(chunk.delta, end="")


```

### Using `astream_chat` endpoint
[Section titled “Using astream_chat endpoint”](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/#using-astream_chat-endpoint)

```


import ads




from llama_index.llms.oci_data_science import OCIDataScience




from llama_index.core.base.llms.types import ChatMessage





ads.set_auth(auth="security_token", profile="<replace-with-your-profile>")





llm = OCIDataScience(




model="odsc-llm",




endpoint="https://<MD_OCID>/predict",





response =await llm.stream_chat(





ChatMessage(role="user", content="Tell me a joke"),




ChatMessage(




role="assistant", content="Why did the chicken cross the road?"





ChatMessage(role="user", content="I don't know, why?"),







asyncfor chunk in response:




print(chunk.delta, end="")


```

## Configure Model
[Section titled “Configure Model”](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/#configure-model)

```


import ads




from llama_index.llms.oci_data_science import OCIDataScience





ads.set_auth(auth="security_token", profile="<replace-with-your-profile>")





llm = OCIDataScience(




model="odsc-llm",




endpoint="https://<MD_OCID>/predict",




temperature=0.2,




max_tokens=500,




timeout=120,




context_window=2500,




additional_kwargs={




"top_p": 0.75,




"logprobs": True,




"top_logprobs": 3,






response = llm.chat(





ChatMessage(role="user", content="Tell me a joke"),






print(response)


```

## Function Calling
[Section titled “Function Calling”](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/#function-calling)
The [AI Quick Actions](https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions.htm) offers prebuilt service containers that make deploying and serving a large language model very easy. Either one of vLLM (a high-throughput and memory-efficient inference and serving engine for LLMs) or TGI (a high-performance text generation server for the popular open-source LLMs) is used in the service container to host the model, the end point created supports the OpenAI API protocol. This allows the model deployment to be used as a drop-in replacement for applications using OpenAI API. If the deployed model supports function calling, then integration with LlamaIndex tools, through the predict_and_call function on the llm allows to attach any tools and let the LLM decide which tools to call (if any).

```


import ads




from llama_index.llms.oci_data_science import OCIDataScience




from llama_index.core.tools import FunctionTool





ads.set_auth(auth="security_token", profile="<replace-with-your-profile>")





llm = OCIDataScience(




model="odsc-llm",




endpoint="https://<MD_OCID>/predict",




temperature=0.2,




max_tokens=500,




timeout=120,




context_window=2500,




additional_kwargs={




"top_p": 0.75,




"logprobs": True,




"top_logprobs": 3,








defmultiply(a: float, b: float) -> float:




print(f"---> {a}{b}")




return* b






defadd(a: float, b: float) -> float:




print(f"---> {a}{b}")




return+ b






defsubtract(a: float, b: float) -> float:




print(f"---> {a}{b}")




return- b






defdivide(a: float, b: float) -> float:




print(f"---> {a}{b}")




return/ b






multiply_tool = FunctionTool.from_defaults(fn=multiply)




add_tool = FunctionTool.from_defaults(fn=add)




sub_tool = FunctionTool.from_defaults(fn=subtract)




divide_tool = FunctionTool.from_defaults(fn=divide)





response = llm.predict_and_call(




[multiply_tool, add_tool, sub_tool, divide_tool],




user_msg="Calculate the result of `8 + 2 - 6`.",




verbose=True,






print(response)


```

### Using `FunctionAgent`
[Section titled “Using FunctionAgent”](https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/#using-functionagent)

```


import ads




from llama_index.llms.oci_data_science import OCIDataScience




from llama_index.core.tools import FunctionTool




from llama_index.core.agent.workflow import FunctionAgent





ads.set_auth(auth="security_token", profile="<replace-with-your-profile>")





llm = OCIDataScience(




model="odsc-llm",




endpoint="https://<MD_OCID>/predict",




temperature=0.2,




max_tokens=500,




timeout=120,




context_window=2500,




additional_kwargs={




"top_p": 0.75,




"logprobs": True,




"top_logprobs": 3,








defmultiply(a: float, b: float) -> float:




print(f"---> {a}{b}")




return* b






defadd(a: float, b: float) -> float:




print(f"---> {a}{b}")




return+ b






defsubtract(a: float, b: float) -> float:




print(f"---> {a}{b}")




return- b






defdivide(a: float, b: float) -> float:




print(f"---> {a}{b}")




return/ b






multiply_tool = FunctionTool.from_defaults(fn=multiply)




add_tool = FunctionTool.from_defaults(fn=add)




sub_tool = FunctionTool.from_defaults(fn=subtract)




divide_tool = FunctionTool.from_defaults(fn=divide)





agent = FunctionAgent(




tools=[multiply_tool, add_tool, sub_tool, divide_tool],




llm=llm,





response =await agent.run(




"Calculate the result of `8 + 2 - 6`. Use tools. Return the calculated result."






print(response)


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


