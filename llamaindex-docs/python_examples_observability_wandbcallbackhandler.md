[Skip to content](https://developers.llamaindex.ai/python/examples/observability/wandbcallbackhandler/#_top)
# Wandb Callback Handler 
[Weights & Biases Prompts](https://docs.wandb.ai/guides/prompts) is a suite of LLMOps tools built for the development of LLM-powered applications.
The `WandbCallbackHandler` is integrated with W&B Prompts to visualize and inspect the execution flow of your index construction, or querying over your index and more. You can use this handler to persist your created indices as W&B Artifacts allowing you to version control your indices.

```


%pip install llama-index-callbacks-wandb




%pip install llama-index-llms-openai


```


```


import os




from getpass import getpass





if os.getenv("OPENAI_API_KEY") isNone:




os.environ["OPENAI_API_KEY"] = getpass(




"Paste your OpenAI key from:"




" https://platform.openai.com/account/api-keys\n"





assert os.getenv("OPENAI_API_KEY", "").startswith(




"sk-"




), "This doesn't look like a valid OpenAI API key"




print("OpenAI API key configured")


```


```

OpenAI API key configured

```


```


from llama_index.core.callbacks import CallbackManager




from llama_index.core.callbacks import LlamaDebugHandler




from llama_index.callbacks.wandb import WandbCallbackHandler




from llama_index.core import (




VectorStoreIndex,




SimpleDirectoryReader,




SimpleKeywordTableIndex,




StorageContext,





from llama_index.llms.openai import OpenAI


```

## Setup LLM
[Section titled “Setup LLM”](https://developers.llamaindex.ai/python/examples/observability/wandbcallbackhandler/#setup-llm)

```


from llama_index.core import Settings





Settings.llm = OpenAI(model="gpt-4", temperature=0)


```

## W&B Callback Manager Setup
[Section titled “W&B Callback Manager Setup”](https://developers.llamaindex.ai/python/examples/observability/wandbcallbackhandler/#wb-callback-manager-setup)
**Option 1** : Set Global Evaluation Handler

```


import llama_index.core




from llama_index.core import set_global_handler





set_global_handler("wandb", run_args={"project": "llamaindex"})




wandb_callback = llama_index.core.global_handler


```

**Option 2** : Manually Configure Callback Handler
Also configure a debugger handler for extra notebook visibility.

```


llama_debug = LlamaDebugHandler(print_trace_on_end=True)




# wandb.init args



run_args =dict(




project="llamaindex",






wandb_callback = WandbCallbackHandler(run_args=run_args)





Settings.callback_manager = CallbackManager([llama_debug, wandb_callback])


```

> After running the above cell, you will get the W&B run page URL. Here you will find a trace table with all the events tracked using [Weights and Biases’ Prompts](https://docs.wandb.ai/guides/prompts) feature.
## 1. Indexing
[Section titled “1. Indexing”](https://developers.llamaindex.ai/python/examples/observability/wandbcallbackhandler/#1-indexing)
Download Data

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```


```


docs = SimpleDirectoryReader("./data/paul_graham/").load_data()


```


```


index = VectorStoreIndex.from_documents(docs)


```


```

**********


Trace: index_construction



|_node_parsing ->  0.295179 seconds




|_chunking ->  0.293976 seconds




|_embedding ->  0.494492 seconds




|_embedding ->  0.346162 seconds



**********




[34m[1mwandb[0m: Logged trace tree to W&B.

```

### 1.1 Persist Index as W&B Artifacts
[Section titled “1.1 Persist Index as W&B Artifacts”](https://developers.llamaindex.ai/python/examples/observability/wandbcallbackhandler/#11-persist-index-as-wb-artifacts)

```


wandb_callback.persist_index(index, index_name="simple_vector_store")


```


```

[34m[1mwandb[0m: Adding directory to artifact (/Users/loganmarkewich/llama_index/docs/examples/callbacks/wandb/run-20230801_152955-ds93prxa/files/storage)... Done. 0.0s

```

### 1.2 Download Index from W&B Artifacts
[Section titled “1.2 Download Index from W&B Artifacts”](https://developers.llamaindex.ai/python/examples/observability/wandbcallbackhandler/#12-download-index-from-wb-artifacts)

```


from llama_index.core import load_index_from_storage





storage_context = wandb_callback.load_storage_context(




artifact_url="ayut/llamaindex/simple_vector_store:v0"





# Load the index and initialize a query engine



index = load_index_from_storage(




storage_context,



```


```

[34m[1mwandb[0m:   3 of 3 files downloaded.




**********


Trace: index_construction


**********

```

## 2. Query Over Index
[Section titled “2. Query Over Index”](https://developers.llamaindex.ai/python/examples/observability/wandbcallbackhandler/#2-query-over-index)

```


query_engine = index.as_query_engine()




response = query_engine.query("What did the author do growing up?")




print(response, sep="\n")


```


```

**********


Trace: query



|_query ->  2.695958 seconds




|_retrieve ->  0.806379 seconds




|_embedding ->  0.802871 seconds




|_synthesize ->  1.8893 seconds




|_llm ->  1.842434 seconds



**********




[34m[1mwandb[0m: Logged trace tree to W&B.




The text does not provide information on what the author did growing up.

```

## Close W&B Callback Handler
[Section titled “Close W&B Callback Handler”](https://developers.llamaindex.ai/python/examples/observability/wandbcallbackhandler/#close-wb-callback-handler)
When we are done tracking our events we can close the wandb run.

```

wandb_callback.finish()

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


