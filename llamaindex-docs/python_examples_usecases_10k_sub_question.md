[Skip to content](https://developers.llamaindex.ai/python/examples/usecases/10k_sub_question/#_top)
# 10K Analysis 
In this demo, we explore answering complex queries by decomposing them into simpler sub-queries.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-llms-openai


```


```


!pip install llama-index


```


```


import nest_asyncio




nest_asyncio.apply()

```


```


from llama_index.core import SimpleDirectoryReader, VectorStoreIndex




from llama_index.llms.openai import OpenAI





from llama_index.core.tools import QueryEngineTool, ToolMetadata




from llama_index.core.query_engine import SubQuestionQueryEngine


```


```

/Users/suo/miniconda3/envs/llama/lib/python3.9/site-packages/deeplake/util/check_latest_version.py:32: UserWarning: A newer version of deeplake (3.6.7) is available. It's recommended that you update to the latest version using `pip install -U deeplake`.



warnings.warn(


```

## Configure LLM service
[Section titled “Configure LLM service”](https://developers.llamaindex.ai/python/examples/usecases/10k_sub_question/#configure-llm-service)

```


import os





os.environ["OPENAI_API_KEY"] ="YOUR_API_KEY"


```


```


from llama_index.core import Settings





Settings.llm = OpenAI(temperature=0.2, model="gpt-3.5-turbo")


```

## Download Data
[Section titled “Download Data”](https://developers.llamaindex.ai/python/examples/usecases/10k_sub_question/#download-data)

```


!mkdir -p 'data/10k/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/10k/uber_2021.pdf'-O 'data/10k/uber_2021.pdf'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/10k/lyft_2021.pdf'-O 'data/10k/lyft_2021.pdf'


```

## Load data
[Section titled “Load data”](https://developers.llamaindex.ai/python/examples/usecases/10k_sub_question/#load-data)

```


lyft_docs = SimpleDirectoryReader(




input_files=["./data/10k/lyft_2021.pdf"]



).load_data()



uber_docs = SimpleDirectoryReader(




input_files=["./data/10k/uber_2021.pdf"]



).load_data()

```

## Build indices
[Section titled “Build indices”](https://developers.llamaindex.ai/python/examples/usecases/10k_sub_question/#build-indices)

```


lyft_index = VectorStoreIndex.from_documents(lyft_docs)


```


```


uber_index = VectorStoreIndex.from_documents(uber_docs)


```

## Build query engines
[Section titled “Build query engines”](https://developers.llamaindex.ai/python/examples/usecases/10k_sub_question/#build-query-engines)

```


lyft_engine = lyft_index.as_query_engine(similarity_top_k=3)


```


```


uber_engine = uber_index.as_query_engine(similarity_top_k=3)


```


```


query_engine_tools = [




QueryEngineTool(




query_engine=lyft_engine,




metadata=ToolMetadata(




name="lyft_10k",




description=(




"Provides information about Lyft financials for year 2021"







QueryEngineTool(




query_engine=uber_engine,




metadata=ToolMetadata(




name="uber_10k",




description=(




"Provides information about Uber financials for year 2021"









s_engine = SubQuestionQueryEngine.from_defaults(




query_engine_tools=query_engine_tools



```

## Run queries
[Section titled “Run queries”](https://developers.llamaindex.ai/python/examples/usecases/10k_sub_question/#run-queries)

```


response = s_engine.query(




"Compare and contrast the customer segments and geographies that grew the"




" fastest"



```


```

Generated 4 sub questions.


[36;1m[1;3m[uber_10k] Q: What customer segments grew the fastest for Uber


[0m[33;1m[1;3m[uber_10k] Q: What geographies grew the fastest for Uber


[0m[38;5;200m[1;3m[lyft_10k] Q: What customer segments grew the fastest for Lyft


[0m[32;1m[1;3m[lyft_10k] Q: What geographies grew the fastest for Lyft


[0m[33;1m[1;3m[uber_10k] A:


Uber experienced the fastest growth in five metropolitan areas—Chicago, Miami, and New York City in the United States, Sao Paulo in Brazil, and London in the United Kingdom. Additionally, Uber experienced growth in suburban and rural areas, though the network is smaller and less liquid in these areas.


[0m[38;5;200m[1;3m[lyft_10k] A:


Lyft has seen the fastest growth in its ridesharing marketplace, Express Drive, Lyft Rentals, Light Vehicles, Public Transit, and Lyft Autonomous customer segments. These customer segments have seen increased demand due to the convenience and high-quality experience they offer drivers and riders, as well as the investments Lyft has made in its proprietary technology, M&A and strategic partnerships, and brand and marketing efforts.


[0m[32;1m[1;3m[lyft_10k] A:


Lyft has grown rapidly in cities across the United States and in select cities in Canada. The ridesharing market grew rapidly prior to the COVID-19 pandemic, and it is uncertain to what extent market acceptance will continue to grow after the pandemic. The market for Lyft's other offerings, such as its network of Light Vehicles, is also new and unproven, and it is uncertain whether demand for bike and scooter sharing will continue to grow.


[0m[36;1m[1;3m[uber_10k] A: in 2021?



The customer segments that grew the fastest for Uber in 2021 were Riders and Eaters, who use the platform for ridesharing services and meal preparation, grocery, and other delivery services, respectively. Additionally, Uber One, Uber Pass, Eats Pass, and Rides Pass membership programs grew significantly in 2021, with over 6 million members.


```


```


print(response)


```


```

Uber and Lyft both experienced the fastest growth in their respective customer segments and geographies in 2021.



For Uber, the fastest growing customer segments were Riders and Eaters, who use the platform for ridesharing services and meal preparation, grocery, and other delivery services, respectively. Additionally, Uber One, Uber Pass, Eats Pass, and Rides Pass membership programs grew significantly in 2021, with over 6 million members. Uber experienced the fastest growth in five metropolitan areas—Chicago, Miami, and New York City in the United States, Sao Paulo in Brazil, and London in the United Kingdom. Additionally, Uber experienced growth in suburban and rural areas, though the network is smaller and less liquid in these areas.



For Lyft, the fastest growing customer segments were ridesharing, Express Drive, Lyft Rentals, Light Vehicles, Public Transit, and Lyft Autonomous. Lyft has grown rapidly in cities across the United States and in select cities in Canada. The ridesharing market grew rapidly prior to the COVID-19 pandemic, and it is uncertain to what extent market acceptance will continue to grow after the pandemic. The market for Lyft's other offerings, such as its network of Light Vehicles, is also new and unproven, and it is uncertain whether demand for bike and scooter sharing will continue to grow.



Overall, Uber and Lyft experienced the fastest growth in different customer segments and geographies. Uber experienced the fastest growth in Riders and Eaters, as well as in five metropolitan areas, while Lyft experienced the fastest growth in ridesharing, Express Drive, Lyft Rentals, Light Vehicles, Public Transit, and Lyft Autonomous, as well as in cities across the United States and in select cities in Canada.

```


```


response = s_engine.query(




"Compare revenue growth of Uber and Lyft from 2020 to 2021"



```


```

Generated 2 sub questions.


[36;1m[1;3m[uber_10k] Q: What is the revenue growth of Uber from 2020 to 2021


[0m[33;1m[1;3m[lyft_10k] Q: What is the revenue growth of Lyft from 2020 to 2021


[0m[33;1m[1;3m[lyft_10k] A:


The revenue of Lyft grew by 36% from 2020 to 2021.


[0m[36;1m[1;3m[uber_10k] A:


The revenue growth of Uber from 2020 to 2021 was 57%, or 54% on a constant currency basis.


```


```


print(response)


```


```

The revenue growth of Uber from 2020 to 2021 was 57%, or 54% on a constant currency basis, while the revenue of Lyft grew by 36% from 2020 to 2021. Therefore, Uber had a higher revenue growth than Lyft from 2020 to 2021.

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


