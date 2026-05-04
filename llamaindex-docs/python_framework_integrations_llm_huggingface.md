[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/llm/huggingface/#_top)
LlamaIndex Framework
Integrations
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Hugging Face LLMs 
There are many ways to interface with LLMs from [Hugging Face](https://huggingface.co/), either locally or via Hugging Face’s [Inference Providers](https://huggingface.co/docs/inference-providers). Hugging Face itself provides several Python packages to enable access, which LlamaIndex wraps into `LLM` entities:
  * The [`transformers`](https://github.com/huggingface/transformers) package: use `llama_index.llms.HuggingFaceLLM`
  * The [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers), [wrapped by `huggingface_hub[inference]`](https://github.com/huggingface/huggingface_hub): use `llama_index.llms.HuggingFaceInferenceAPI`


There are _many_ possible permutations of these two, so this notebook only details a few. Let’s use Hugging Face’s [Text Generation task](https://huggingface.co/tasks/text-generation) as our example.
In the below line, we install the packages necessary for this demo:
  * `transformers[torch]` is needed for `HuggingFaceLLM`
  * `huggingface_hub[inference]` is needed for `HuggingFaceInferenceAPI`
  * The quotes are needed for Z shell (`zsh`)



```


%pip install llama-index-llms-huggingface # for local inference




%pip install llama-index-llms-huggingface-api # for remote inference


```


```


!pip install "transformers[torch]""huggingface_hub[inference]"


```

If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


!pip install llama-index


```

Now that we’re set up, let’s play around:
# Setup Hugging Face Account
[Section titled “Setup Hugging Face Account”](https://developers.llamaindex.ai/python/framework/integrations/llm/huggingface/#setup-hugging-face-account)
First, you need to create a Hugging Face account and get a token. You can sign up [here](https://huggingface.co/join). Then you’ll need to create a token [here](https://huggingface.co/settings/tokens).
Terminal window
```


export HUGGING_FACE_TOKEN=hf_your_token_here


```


```


import os




from typing import List, Optional





from llama_index.llms.huggingface import HuggingFaceLLM




from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI





HF_TOKEN: Optional[str] = os.getenv("HUGGING_FACE_TOKEN")




# NOTE: None default will fall back on Hugging Face's token storage



# when this token gets used within HuggingFaceInferenceAPI

```

## Use a model via Inference Providers
[Section titled “Use a model via Inference Providers”](https://developers.llamaindex.ai/python/framework/integrations/llm/huggingface/#use-a-model-via-inference-providers)
The easiest way to use an open source model is to use the Hugging Face [Inference Providers](https://huggingface.co/docs/inference-providers). Let’s use the DeepSeek R1 model, which is great for complex tasks.
With inference providers, you can use the model on serverless infrastructure from inference providers.

```


remotely_run = HuggingFaceInferenceAPI(




model_name="deepseek-ai/DeepSeek-R1-0528",




token=HF_TOKEN,




provider="auto"# this will use the best provider available



```

We can also specify our preferred inference provider. Let’s use the [`together` provider](https://huggingface.co/togethercomputer).

```


remotely_run = HuggingFaceInferenceAPI(




model_name="Qwen/Qwen3-235B-A22B",




token=HF_TOKEN,




provider="together"# this will use the best provider available



```

## Use an open source model locally
[Section titled “Use an open source model locally”](https://developers.llamaindex.ai/python/framework/integrations/llm/huggingface/#use-an-open-source-model-locally)
First, we’ll use an open source model that’s optimized for local inference. This model is downloaded (if first invocation) to the local Hugging Face model cache, and actually runs the model on your local machine’s hardware.
We’ll use the [Gemma 3N E4B](https://huggingface.co/google/gemma-3n-E4B-it) model, which is optimized for local inference.

```


locally_run = HuggingFaceLLM(model_name="google/gemma-3n-E4B-it")


```

## Use a dedicated Inference Endpoint
[Section titled “Use a dedicated Inference Endpoint”](https://developers.llamaindex.ai/python/framework/integrations/llm/huggingface/#use-a-dedicated-inference-endpoint)
We can also spin up a dedicated Inference Endpoint for a model and use that to run the model.

```


endpoint_server = HuggingFaceInferenceAPI(




model="https://(<your-endpoint>.eu-west-1.aws.endpoints.huggingface.cloud"



```

## Use a local inference engine (vLLM or TGI)
[Section titled “Use a local inference engine (vLLM or TGI)”](https://developers.llamaindex.ai/python/framework/integrations/llm/huggingface/#use-a-local-inference-engine-vllm-or-tgi)
We can also use a local inference engine like [vLLM](https://github.com/vllm-project/vllm) or [TGI](https://github.com/huggingface/text-generation-inference) to run the model.

```

# You can also connect to a model being served by a local or remote


# Text Generation Inference server



tgi_server = HuggingFaceInferenceAPI(model="http://localhost:8080")


```

Underlying a completion with `HuggingFaceInferenceAPI` is Hugging Face’s [Text Generation task](https://huggingface.co/tasks/text-generation).

```


completion_response = remotely_run_recommended.complete("To infinity, and")




print(completion_response)


```


```


beyond!



The Infinity Wall Clock is a unique and stylish way to keep track of time. The clock is made of a durable, high-quality plastic and features a bright LED display. The Infinity Wall Clock is powered by batteries and can be mounted on any wall. It is a great addition to any home or office.

```

## Setting a tokenizer
[Section titled “Setting a tokenizer”](https://developers.llamaindex.ai/python/framework/integrations/llm/huggingface/#setting-a-tokenizer)
If you are modifying the LLM, you should also change the global tokenizer to match!

```


from llama_index.core import set_global_tokenizer




from transformers import AutoTokenizer




set_global_tokenizer(



AutoTokenizer.from_pretrained("HuggingFaceH4/zephyr-7b-alpha").encode



```

If you’re curious, other Hugging Face Inference API tasks wrapped are:
  * `llama_index.llms.HuggingFaceInferenceAPI.chat`: [Conversational task](https://huggingface.co/tasks/conversational)
  * `llama_index.embeddings.HuggingFaceInferenceAPIEmbedding`: [Feature Extraction task](https://huggingface.co/tasks/feature-extraction)


And yes, Hugging Face embedding models are supported with:
  * `transformers[torch]`: wrapped by `HuggingFaceEmbedding`
  * `huggingface_hub[inference]`: wrapped by `HuggingFaceInferenceAPIEmbedding`


Both of the above two subclass `llama_index.embeddings.base.BaseEmbedding`.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


