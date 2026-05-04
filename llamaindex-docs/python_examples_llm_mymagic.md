[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/llm/mymagic/#_top)
LlamaIndex Framework
Integrations
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# MyMagic AI LLM 
## Introduction
[Section titled “Introduction”](https://developers.llamaindex.ai/python/framework/integrations/llm/mymagic/#introduction)
This notebook demonstrates how to use MyMagicAI for batch inference on massive data stored in cloud buckets. The only enpoints implemented are `complete` and `acomplete` which can work on many use cases including Completion, Summariation and Extraction. To use this notebook, you need an API key (Personal Access Token) from MyMagicAI and data stored in cloud buckets. Sign up by clicking Get Started at [MyMagicAI’s website](https://mymagic.ai/) to get your API key.
## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/framework/integrations/llm/mymagic/#setup)
To set up your bucket and grant MyMagic API a secure access to your cloud storage, please visit [MyMagic docs](https://docs.mymagic.ai/) for reference. If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-llms-mymagic


```


```


!pip install llama-index


```


```


from llama_index.llms.mymagic import MyMagicAI


```


```


llm = MyMagicAI(




api_key="your-api-key",




storage_provider="s3"# s3, gcs




bucket_name="your-bucket-name",




session="your-session-name"# files should be located in this folder on which batch inference will be run




role_arn="your-role-arn",




system_prompt="your-system-prompt",




region="your-bucket-region",




return_output=False# Whether you want MyMagic API to return the output json




input_json_file=None# name of the input file (stored on the bucket)




list_inputs=None# Option to provide inputs as a list in case of small batch




structured_output=None# json schema of the output



```

Note: if return_output is set True above, max_tokens should be set to at least 100

```


resp = llm.complete(




question="your-question",




model="chhoose-model"# currently we support mistral7b, llama7b, mixtral8x7b, codellama70b, llama70b, more to come...




max_tokens=5# number of tokens to generate, default is 10



```


```

# The response indicated that the final output is stored in your bucket or raises an exception if the job failed



print(resp)


```

## Asynchronous Requests by using `acomplete` endpoint
[Section titled “Asynchronous Requests by using acomplete endpoint”](https://developers.llamaindex.ai/python/framework/integrations/llm/mymagic/#asynchronous-requests-by-using-acomplete-endpoint)
For asynchronous operations, use the following approach.

```


import asyncio


```


```


asyncdefmain():




response =await llm.acomplete(




question="your-question",




model="choose-model"# supported models constantly updated and are listed at docs.mymagic.ai




max_tokens=5# number of tokens to generate, default is 10






print("Async completion response:", response)


```


```


await main()


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


