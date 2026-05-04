[Skip to content](https://developers.llamaindex.ai/python/examples/customization/llms/simpleindexdemo-huggingface_camel/#_top)
# HuggingFace LLM - Camel-5b 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-llms-huggingface


```


```


!pip install llama-index


```


```


import logging




import sys





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))





from llama_index.core import VectorStoreIndex, SimpleDirectoryReader




from llama_index.llms.huggingface import HuggingFaceLLM




from llama_index.core import Settings


```


```

INFO:numexpr.utils:Note: NumExpr detected 16 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8.


Note: NumExpr detected 16 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8.


INFO:numexpr.utils:NumExpr defaulting to 8 threads.


NumExpr defaulting to 8 threads.




/home/loganm/miniconda3/envs/gpt_index/lib/python3.11/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html



from .autonotebook import tqdm as notebook_tqdm


```

#### Download Data
[Section titled “Download Data”](https://developers.llamaindex.ai/python/examples/customization/llms/simpleindexdemo-huggingface_camel/#download-data)

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```

#### Load documents, build the VectorStoreIndex
[Section titled “Load documents, build the VectorStoreIndex”](https://developers.llamaindex.ai/python/examples/customization/llms/simpleindexdemo-huggingface_camel/#load-documents-build-the-vectorstoreindex)

```

# load documents



documents = SimpleDirectoryReader("./data/paul_graham/").load_data()


```


```

# setup prompts - specific to StableLM



from llama_index.core import PromptTemplate




# This will wrap the default prompts that are internal to llama-index


# taken from https://huggingface.co/Writer/camel-5b-hf



query_wrapper_prompt = PromptTemplate(




"Below is an instruction that describes a task. "




"Write a response that appropriately completes the request.\n\n"




"### Instruction:\n{query_str}\n\n### Response:"



```


```


import torch





llm = HuggingFaceLLM(




context_window=2048,




max_new_tokens=256,




generate_kwargs={"temperature": 0.25, "do_sample": False},




query_wrapper_prompt=query_wrapper_prompt,




tokenizer_name="Writer/camel-5b-hf",




model_name="Writer/camel-5b-hf",




device_map="auto",




tokenizer_kwargs={"max_length": 2048},




# uncomment this if using CUDA to reduce memory usage




# model_kwargs={"torch_dtype": torch.float16}






Settings.chunk_size =512




Settings.llm = llm


```


```

Loading checkpoint shards: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 3/3 [00:43<00:00, 14.34s/it]

```


```


index = VectorStoreIndex.from_documents(documents)


```


```

INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total LLM token usage: 0 tokens


> [build_index_from_nodes] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total embedding token usage: 27212 tokens


> [build_index_from_nodes] Total embedding token usage: 27212 tokens

```

#### Query Index
[Section titled “Query Index”](https://developers.llamaindex.ai/python/examples/customization/llms/simpleindexdemo-huggingface_camel/#query-index)

```

# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine()




response = query_engine.query("What did the author do growing up?")


```


```

INFO:llama_index.token_counter.token_counter:> [retrieve] Total LLM token usage: 0 tokens


> [retrieve] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [retrieve] Total embedding token usage: 8 tokens


> [retrieve] Total embedding token usage: 8 tokens




Token indices sequence length is longer than the specified maximum sequence length for this model (954 > 512). Running this sequence through the model will result in indexing errors


Setting `pad_token_id` to `eos_token_id`:50256 for open-end generation.




INFO:llama_index.token_counter.token_counter:> [get_response] Total LLM token usage: 1026 tokens


> [get_response] Total LLM token usage: 1026 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total embedding token usage: 0 tokens


> [get_response] Total embedding token usage: 0 tokens

```


```


print(response)


```


```

The author grew up in a small town in England, attended a prestigious private school, and then went to Cambridge University, where he studied computer science. Afterward, he worked on web infrastructure, wrote essays, and then realized he could write about startups. He then started giving talks, wrote a book, and started interviewing founders for a book on startups.

```

#### Query Index - Streaming
[Section titled “Query Index - Streaming”](https://developers.llamaindex.ai/python/examples/customization/llms/simpleindexdemo-huggingface_camel/#query-index---streaming)

```


query_engine = index.as_query_engine(streaming=True)


```


```

# set Logging to DEBUG for more detailed outputs



response_stream = query_engine.query("What did the author do growing up?")


```


```

INFO:llama_index.token_counter.token_counter:> [retrieve] Total LLM token usage: 0 tokens


> [retrieve] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [retrieve] Total embedding token usage: 8 tokens


> [retrieve] Total embedding token usage: 8 tokens




Setting `pad_token_id` to `eos_token_id`:50256 for open-end generation.




INFO:llama_index.token_counter.token_counter:> [get_response] Total LLM token usage: 0 tokens


> [get_response] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total embedding token usage: 0 tokens


> [get_response] Total embedding token usage: 0 tokens

```


```

# can be slower to start streaming since llama-index often involves many LLM calls


response_stream.print_response_stream()

```


```

The author grew up in a small town in England, attended a prestigious private school, and then went to Cambridge University, where he studied computer science. Afterward, he worked on web infrastructure, wrote essays, and then realized he could write about startups. He then started giving talks, wrote a book, and started interviewing founders for a book on startups.<|endoftext|>

```


```

# can also get a normal response object



response = response_stream.get_response()




print(response)


```


```

# can also iterate over the generator yourself



generated_text =""




for text in response.response_gen:




generated_text += text


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


