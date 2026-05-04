[Skip to content](https://developers.llamaindex.ai/python/examples/query_engine/pydantic_query_engine/#_top)
# Query Engine with Pydantic Outputs 
Every query engine has support for integrated structured responses using the following `response_mode`s in `RetrieverQueryEngine`:
  * `refine`
  * `compact`
  * `tree_summarize`
  * `accumulate` (beta, requires extra parsing to convert to objects)
  * `compact_accumulate` (beta, requires extra parsing to convert to objects)


In this notebook, we walk through a small example demonstrating the usage.
Under the hood, every LLM response will be a pydantic object. If that response needs to be refined or summarized, it is converted into a JSON string for the next response. Then, the final response is returned as a pydantic object.
**NOTE:** This can technically work with any LLM, but non-openai is support is still in development and considered beta.
## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/examples/query_engine/pydantic_query_engine/#setup)
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-llms-anthropic




%pip install llama-index-llms-openai


```


```


!pip install llama-index


```


```


import os




import openai





os.environ["OPENAI_API_KEY"] ="sk-..."




openai.api_key = os.environ["OPENAI_API_KEY"]


```

Download Data

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```


```


from llama_index.core import SimpleDirectoryReader





documents = SimpleDirectoryReader("./data/paul_graham").load_data()


```

### Create our Pydanitc Output Object
[Section titled “Create our Pydanitc Output Object”](https://developers.llamaindex.ai/python/examples/query_engine/pydantic_query_engine/#create-our-pydanitc-output-object)

```


from typing import List




from pydantic import BaseModel






classBiography(BaseModel):




"""Data model for a biography."""





name: str




best_known_for: List[str]




extra_info: str


```

## Create the Index + Query Engine (OpenAI)
[Section titled “Create the Index + Query Engine (OpenAI)”](https://developers.llamaindex.ai/python/examples/query_engine/pydantic_query_engine/#create-the-index--query-engine-openai)
When using OpenAI, the function calling API will be leveraged for reliable structured outputs.

```


from llama_index.core import VectorStoreIndex




from llama_index.llms.openai import OpenAI





llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)





index = VectorStoreIndex.from_documents(




documents,



```


```


query_engine = index.as_query_engine(




output_cls=Biography, response_mode="compact", llm=llm



```


```


response = query_engine.query("Who is Paul Graham?")


```


```


print(response.name)




print(response.best_known_for)




print(response.extra_info)


```


```

Paul Graham


['working on Bel', 'co-founding Viaweb', 'creating the programming language Arc']


Paul Graham is a computer scientist, entrepreneur, and writer. He is best known for his work on Bel, a programming language, and for co-founding Viaweb, an early web application company that was later acquired by Yahoo. Graham also created the programming language Arc. He has written numerous essays on topics such as startups, programming, and life.

```


```

# get the full pydanitc object



print(type(response.response))


```


```

<class '__main__.Biography'>

```

## Create the Index + Query Engine (Non-OpenAI, Beta)
[Section titled “Create the Index + Query Engine (Non-OpenAI, Beta)”](https://developers.llamaindex.ai/python/examples/query_engine/pydantic_query_engine/#create-the-index--query-engine-non-openai-beta)
When using an LLM that does not support function calling, we rely on the LLM to write the JSON itself, and we parse the JSON into the proper pydantic object.

```


import os





os.environ["ANTHROPIC_API_KEY"] ="sk-..."


```


```


from llama_index.core import VectorStoreIndex




from llama_index.llms.anthropic import Anthropic





llm = Anthropic(model="claude-instant-1.2", temperature=0.1)





index = VectorStoreIndex.from_documents(




documents,



```


```


query_engine = index.as_query_engine(




output_cls=Biography, response_mode="tree_summarize", llm=llm



```


```


response = query_engine.query("Who is Paul Graham?")


```


```


print(response.name)




print(response.best_known_for)




print(response.extra_info)


```


```

Paul Graham


['Co-founder of Y Combinator', 'Essayist and programmer']


He is known for creating Viaweb, one of the first web application builders, and for founding Y Combinator, one of the world's top startup accelerators. Graham has also written extensively about technology, investing, and philosophy.

```


```

# get the full pydanitc object



print(type(response.response))


```


```

<class '__main__.Biography'>

```

## Accumulate Examples (Beta)
[Section titled “Accumulate Examples (Beta)”](https://developers.llamaindex.ai/python/examples/query_engine/pydantic_query_engine/#accumulate-examples-beta)
Accumulate with pydantic objects requires some extra parsing. This is still a beta feature, but it’s still possible to get accumulate pydantic objects.

```


from typing import List




from pydantic import BaseModel






classCompany(BaseModel):




"""Data model for a companies mentioned."""





company_name: str




context_info: str


```


```


from llama_index.core import VectorStoreIndex,




from llama_index.llms.openai import OpenAI





llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)





index = VectorStoreIndex.from_documents(




documents,



```


```


query_engine = index.as_query_engine(




output_cls=Company, response_mode="accumulate", llm=llm



```


```


response = query_engine.query("What companies are mentioned in the text?")


```

In accumulate, responses are separated by a default separator, and prepended with a prefix.

```


companies = []




# split by the default separator



for response_str instr(response).split("\n---------------------\n"):




# remove the prefix --  every response starts like `Response 1: {...}`




# so, we find the first bracket and remove everything before it




response_str = response_str[response_str.find("{") :]




companies.append(Company.parse_raw(response_str))


```


```


print(companies)


```


```

[Company(company_name='Yahoo', context_info='Yahoo bought us'), Company(company_name='Yahoo', context_info="I'd been meaning to since Yahoo bought us")]

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


