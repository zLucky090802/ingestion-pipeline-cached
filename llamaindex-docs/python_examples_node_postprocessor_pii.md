[Skip to content](https://developers.llamaindex.ai/python/examples/node_postprocessor/pii/#_top)
# PII Masking 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-llms-openai




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





from llama_index.core.postprocessor import (




PIINodePostprocessor,




NERPIINodePostprocessor,





from llama_index.llms.huggingface import HuggingFaceLLM




from llama_index.core import Document, VectorStoreIndex




from llama_index.core.schema import TextNode


```


```

INFO:numexpr.utils:Note: NumExpr detected 16 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8.


Note: NumExpr detected 16 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8.


INFO:numexpr.utils:NumExpr defaulting to 8 threads.


NumExpr defaulting to 8 threads.




/home/loganm/miniconda3/envs/llama-index/lib/python3.11/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html



from .autonotebook import tqdm as notebook_tqdm


```


```

# load documents



text ="""




Hello Paulo Santos. The latest statement for your credit card account \



1111-0000-1111-0000 was mailed to 123 Any Street, Seattle, WA 98109.




node = TextNode(text=text)


```

### Option 1: Use NER Model for PII Masking
[Section titled “Option 1: Use NER Model for PII Masking”](https://developers.llamaindex.ai/python/examples/node_postprocessor/pii/#option-1-use-ner-model-for-pii-masking)
Use a Hugging Face NER model for PII Masking

```


processor = NERPIINodePostprocessor()


```


```


from llama_index.core.schema import NodeWithScore





new_nodes = processor.postprocess_nodes([NodeWithScore(node=node)])


```


```

No model was supplied, defaulted to dbmdz/bert-large-cased-finetuned-conll03-english and revision f2482bf (https://huggingface.co/dbmdz/bert-large-cased-finetuned-conll03-english).


Using a pipeline without specifying a model name and revision in production is not recommended.


/home/loganm/miniconda3/envs/llama-index/lib/python3.11/site-packages/transformers/pipelines/token_classification.py:169: UserWarning: `grouped_entities` is deprecated and will be removed in version v5.0.0, defaulted to `aggregation_strategy="AggregationStrategy.SIMPLE"` instead.



warnings.warn(


```


```

# view redacted text



new_nodes[0].node.get_text()


```


```

'Hello [ORG_6]. The latest statement for your credit card account 1111-0000-1111-0000 was mailed to 123 [ORG_108] [LOC_112], [LOC_120], [LOC_129] 98109.'

```


```

# get mapping in metadata



# NOTE: this is not sent to the LLM!




new_nodes[0].node.metadata["__pii_node_info__"]


```


```

{'[ORG_6]': 'Paulo Santos',



'[ORG_108]': 'Any',




'[LOC_112]': 'Street',




'[LOC_120]': 'Seattle',




'[LOC_129]': 'WA'}


```

### Option 2: Use LLM for PII Masking
[Section titled “Option 2: Use LLM for PII Masking”](https://developers.llamaindex.ai/python/examples/node_postprocessor/pii/#option-2-use-llm-for-pii-masking)
NOTE: You should be using a _local_ LLM model for PII masking. The example shown is using OpenAI, but normally you’d use an LLM running locally, possibly from huggingface. Examples for local LLMs are [here](https://gpt-index.readthedocs.io/en/latest/how_to/customization/custom_llms.html#example-using-a-huggingface-llm).

```


from llama_index.llms.openai import OpenAI





processor = PIINodePostprocessor(llm=OpenAI())


```


```


from llama_index.core.schema import NodeWithScore





new_nodes = processor.postprocess_nodes([NodeWithScore(node=node)])


```


```

# view redacted text



new_nodes[0].node.get_text()


```


```

'Hello [NAME]. The latest statement for your credit card account [CREDIT_CARD_NUMBER] was mailed to [ADDRESS].'

```


```

# get mapping in metadata



# NOTE: this is not sent to the LLM!




new_nodes[0].node.metadata["__pii_node_info__"]


```


```

{'NAME': 'Paulo Santos',



'CREDIT_CARD_NUMBER': '1111-0000-1111-0000',




'ADDRESS': '123 Any Street, Seattle, WA 98109'}


```

### Option 3: Use Presidio for PII Masking
[Section titled “Option 3: Use Presidio for PII Masking”](https://developers.llamaindex.ai/python/examples/node_postprocessor/pii/#option-3-use-presidio-for-pii-masking)
Use presidio to identify and anonymize PII

```

# load documents



text ="""




Hello Paulo Santos. The latest statement for your credit card account \




4095-2609-9393-4932 was mailed to Seattle, WA 98109. \




IBAN GB90YNTU67299444055881 and social security number is 474-49-7577 were verified on the system. \



Further communications will be sent to paulo@presidio.site




presidio_node = TextNode(text=text)


```


```


from llama_index.postprocessor.presidio import PresidioPIINodePostprocessor





processor = PresidioPIINodePostprocessor()


```


```


from llama_index.core.schema import NodeWithScore





presidio_new_nodes = processor.postprocess_nodes(




[NodeWithScore(node=presidio_node)]



```


```

# view redacted text



presidio_new_nodes[0].node.get_text()


```


```

'\nHello <PERSON_1>. The latest statement for your credit card account <CREDIT_CARD_1> was mailed to <LOCATION_2>, <LOCATION_1>. IBAN <IBAN_CODE_1> and social security number is <US_SSN_1> were verified on the system. Further communications will be sent to <EMAIL_ADDRESS_1> \n'

```


```

# get mapping in metadata



# NOTE: this is not sent to the LLM!




presidio_new_nodes[0].node.metadata["__pii_node_info__"]


```


```

{'<EMAIL_ADDRESS_1>': 'paulo@presidio.site',



'<US_SSN_1>': '474-49-7577',




'<IBAN_CODE_1>': 'GB90YNTU67299444055881',




'<LOCATION_1>': 'WA 98109',




'<LOCATION_2>': 'Seattle',




'<CREDIT_CARD_1>': '4095-2609-9393-4932',




'<PERSON_1>': 'Paulo Santos'}


```

### Feed Nodes to Index
[Section titled “Feed Nodes to Index”](https://developers.llamaindex.ai/python/examples/node_postprocessor/pii/#feed-nodes-to-index)

```

# feed into index



index = VectorStoreIndex([n.node forin new_nodes])


```


```

INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total LLM token usage: 0 tokens


> [build_index_from_nodes] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total embedding token usage: 30 tokens


> [build_index_from_nodes] Total embedding token usage: 30 tokens

```


```


response = index.as_query_engine().query(




"What address was the statement mailed to?"





print(str(response))


```


```

INFO:llama_index.token_counter.token_counter:> [retrieve] Total LLM token usage: 0 tokens


> [retrieve] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [retrieve] Total embedding token usage: 8 tokens


> [retrieve] Total embedding token usage: 8 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total LLM token usage: 71 tokens


> [get_response] Total LLM token usage: 71 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total embedding token usage: 0 tokens


> [get_response] Total embedding token usage: 0 tokens



[ADDRESS]

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


