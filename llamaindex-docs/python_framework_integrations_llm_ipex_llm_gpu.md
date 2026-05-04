[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/llm/ipex_llm_gpu/#_top)
LlamaIndex Framework
Integrations
[IPEX-LLM on Intel GPU ](https://developers.llamaindex.ai/python/framework/integrations/llm/ipex_llm_gpu/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# IPEX-LLM on Intel GPU 
> [IPEX-LLM](https://github.com/intel-analytics/ipex-llm/) is a PyTorch library for running LLM on Intel CPU and GPU (e.g., local PC with iGPU, discrete GPU such as Arc, Flex and Max) with very low latency.
This example goes over how to use LlamaIndex to interact with [`ipex-llm`](https://github.com/intel-analytics/ipex-llm/) for text generation and chat on Intel GPU.
> **Note**
> You could refer to [here](https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/llms/llama-index-llms-ipex-llm/examples) for full examples of `IpexLLM`. Please note that for running on Intel GPU, please specify `-d 'xpu'` or `-d 'xpu:<device_id>'` in command argument when running the examples.
## Install Prerequisites
[Section titled “Install Prerequisites”](https://developers.llamaindex.ai/python/framework/integrations/llm/ipex_llm_gpu/#install-prerequisites)
To benefit from IPEX-LLM on Intel GPUs, there are several prerequisite steps for tools installation and environment preparation.
If you are a Windows user, visit the [Install IPEX-LLM on Windows with Intel GPU Guide](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_windows_gpu.html), and follow [**Install Prerequisites**](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_windows_gpu.html#install-prerequisites) to update GPU driver (optional) and install Conda.
If you are a Linux user, visit the [Install IPEX-LLM on Linux with Intel GPU](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_linux_gpu.html), and follow [**Install Prerequisites**](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_linux_gpu.html#install-prerequisites) to install GPU driver, Intel® oneAPI Base Toolkit 2024.0, and Conda.
## Install `llama-index-llms-ipex-llm`
[Section titled “Install llama-index-llms-ipex-llm”](https://developers.llamaindex.ai/python/framework/integrations/llm/ipex_llm_gpu/#install-llama-index-llms-ipex-llm)
After the prerequisites installation, you should have created a conda environment with all prerequisites installed, activate your conda environment and install `llama-index-llms-ipex-llm` as follows:
Terminal window
```


condaactivate<your-conda-env-name>





pipinstallllama-index-llms-ipex-llm[xpu]--extra-index-urlhttps://pytorch-extension.intel.com/release-whl/stable/xpu/us/


```

This step will also install `ipex-llm` and its dependencies.
> **Note**
> You can also use `https://pytorch-extension.intel.com/release-whl/stable/xpu/cn/` as the `extra-indel-url`.
## Runtime Configuration
[Section titled “Runtime Configuration”](https://developers.llamaindex.ai/python/framework/integrations/llm/ipex_llm_gpu/#runtime-configuration)
For optimal performance, it is recommended to set several environment variables based on your device:
### For Windows Users with Intel Core Ultra integrated GPU
[Section titled “For Windows Users with Intel Core Ultra integrated GPU”](https://developers.llamaindex.ai/python/framework/integrations/llm/ipex_llm_gpu/#for-windows-users-with-intel-core-ultra-integrated-gpu)
In Anaconda Prompt:

```

set SYCL_CACHE_PERSISTENT=1


set BIGDL_LLM_XMX_DISABLED=1

```

### For Linux Users with Intel Arc A-Series GPU
[Section titled “For Linux Users with Intel Arc A-Series GPU”](https://developers.llamaindex.ai/python/framework/integrations/llm/ipex_llm_gpu/#for-linux-users-with-intel-arc-a-series-gpu)
Terminal window
```

# Configure oneAPI environment variables. Required step for APT or offline installed oneAPI.


# Skip this step for PIP-installed oneAPI since the environment has already been configured in LD_LIBRARY_PATH.



source/opt/intel/oneapi/setvars.sh




# Recommended Environment Variables for optimal performance



export USE_XETLA=OFF




export SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS=1




export SYCL_CACHE_PERSISTENT=1


```

> **Note**
> For the first time that each model runs on Intel iGPU/Intel Arc A300-Series or Pro A60, it may take several minutes to compile.
> For other GPU type, please refer to [here](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Overview/install_gpu.html#runtime-configuration) for Windows users, and [here](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Overview/install_gpu.html#id5) for Linux users.
## `IpexLLM`
[Section titled “IpexLLM”](https://developers.llamaindex.ai/python/framework/integrations/llm/ipex_llm_gpu/#ipexllm)
Setting `device_map="xpu"` when initializing `IpexLLM` will put the LLM model on Intel GPU and benefit from IPEX-LLM optimizations.
> **Note**
> If you have multiple Intel GPUs available, you could set `device="xpu:<device_id>"`, in which `device_id` is counted from 0. `device="xpu"` is equal to `device="xpu:0"` by default.
Before loading the Zephyr model, you’ll need to define `completion_to_prompt` and `messages_to_prompt` for formatting prompts. Follow proper prompt format for zephyr-7b-alpha following the [model card](https://huggingface.co/HuggingFaceH4/zephyr-7b-alpha). This is essential for preparing inputs that the model can interpret accurately. Load the Zephyr model locally using IpexLLM using `IpexLLM.from_model_id`. It will load the model directly in its Huggingface format and convert it automatically to low-bit format for inference.

```

# Transform a string into input zephyr-specific input



defcompletion_to_prompt(completion):




returnf"<|system|>\n</s>\n<|user|>\n{completion}</s>\n<|assistant|>\n"





# Transform a list of chat messages into zephyr-specific input



defmessages_to_prompt(messages):




prompt =""




for message in messages:




if message.role =="system":




prompt +=f"<|system|>\n{message.content}</s>\n"




elif message.role =="user":




prompt +=f"<|user|>\n{message.content}</s>\n"




elif message.role =="assistant":




prompt +=f"<|assistant|>\n{message.content}</s>\n"





# ensure we start with a system prompt, insert blank if needed




ifnot prompt.startswith("<|system|>\n"):




prompt ="<|system|>\n</s>\n"+ prompt





# add final assistant prompt




prompt = prompt +"<|assistant|>\n"





return prompt





from llama_index.llms.ipex_llm import IpexLLM





llm = IpexLLM.from_model_id(




model_name="HuggingFaceH4/zephyr-7b-alpha",




tokenizer_name="HuggingFaceH4/zephyr-7b-alpha",




context_window=512,




max_new_tokens=128,




generate_kwargs={"do_sample": False},




completion_to_prompt=completion_to_prompt,




messages_to_prompt=messages_to_prompt,




device_map="xpu",



```

> Please note that in this example we’ll use [HuggingFaceH4/zephyr-7b-alpha](https://huggingface.co/HuggingFaceH4/zephyr-7b-alpha) model for demostration. It requires updating `transformers` and `tokenizers` packages.
> Terminal window
```

> 
pipinstall-Utransformers==4.37.0tokenizers==0.15.2

> 
```

You could then conduct the completion task or chat task as normal:

```


print("----------------- Complete ------------------")




completion_response = llm.complete("Once upon a time, ")




print(completion_response.text)




print("----------------- Stream Complete ------------------")




response_iter = llm.stream_complete("Once upon a time, there's a little girl")




for response in response_iter:




print(response.delta, end="", flush=True)




print("----------------- Chat ------------------")




from llama_index.core.llms import ChatMessage





message = ChatMessage(role="user", content="Explain Big Bang Theory briefly")




resp = llm.chat([message])




print(resp)




print("----------------- Stream Chat ------------------")




message = ChatMessage(role="user", content="What is AI?")




resp = llm.stream_chat([message], max_tokens=256)




forin resp:




print(r.delta, end="")


```

Alternatively, you might save the low-bit model to disk once and use `from_model_id_low_bit` instead of `from_model_id` to reload it for later use - even across different machines. It is space-efficient, as the low-bit model demands significantly less disk space than the original model. And `from_model_id_low_bit` is also more efficient than `from_model_id` in terms of speed and memory usage, as it skips the model conversion step.
To save the low-bit model, use `save_low_bit` as follows. Then load the model from saved lowbit model path. Also use `device_map` to load the model to xpu.
> Note that the saved path for the low-bit model only includes the model itself but not the tokenizers. If you wish to have everything in one place, you will need to manually download or copy the tokenizer files from the original model’s directory to the location where the low-bit model is saved.
Try stream completion using the loaded low-bit model.

```


saved_lowbit_model_path = (




"./zephyr-7b-alpha-low-bit"# path to save low-bit model





llm._model.save_low_bit(saved_lowbit_model_path)



del llm





llm_lowbit = IpexLLM.from_model_id_low_bit(




model_name=saved_lowbit_model_path,




tokenizer_name="HuggingFaceH4/zephyr-7b-alpha",




# tokenizer_name=saved_lowbit_model_path,  # copy the tokenizers to saved path if you want to use it this way




context_window=512,




max_new_tokens=64,




completion_to_prompt=completion_to_prompt,




generate_kwargs={"do_sample": False},




device_map="xpu",






response_iter = llm_lowbit.stream_complete("What is Large Language Model?")




for response in response_iter:




print(response.delta, end="", flush=True)


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


