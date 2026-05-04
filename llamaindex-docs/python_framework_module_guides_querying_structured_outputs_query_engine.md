[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/querying/structured_outputs/query_engine/#_top)
LlamaIndex Framework
Component Guides
Querying
Structured Outputs
[(Deprecated) Query Engines + Pydantic Outputs](https://developers.llamaindex.ai/python/framework/module_guides/querying/structured_outputs/query_engine/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# (Deprecated) Query Engines + Pydantic Outputs
Using `index.as_query_engine()` and it’s underlying `RetrieverQueryEngine`, we can support structured pydantic outputs without an additional LLM calls (in contrast to a typical output parser.)
Every query engine has support for integrated structured responses using the following `response_mode`s in `RetrieverQueryEngine`:
  * `refine`
  * `compact`
  * `tree_summarize`
  * `accumulate` (beta, requires extra parsing to convert to objects)
  * `compact_accumulate` (beta, requires extra parsing to convert to objects)


Under the hood, this uses `OpenAIPydanitcProgam` or `LLMTextCompletionProgram` depending on which LLM you’ve setup. If there are intermediate LLM responses (i.e. during `refine` or `tree_summarize` with multiple LLM calls), the pydantic object is injected into the next LLM prompt as a JSON object.
## Usage Pattern
[Section titled “Usage Pattern”](https://developers.llamaindex.ai/python/framework/module_guides/querying/structured_outputs/query_engine/#usage-pattern)
First, you need to define the object you want to extract.

```


from typing import List




from pydantic import BaseModel






classBiography(BaseModel):




"""Data model for a biography."""





name: str




best_known_for: List[str]




extra_info: str


```

Then, you create your query engine.

```


query_engine = index.as_query_engine(




response_mode="tree_summarize", output_cls=Biography



```

Lastly, you can get a response and inspect the output.

```


response = query_engine.query("Who is Paul Graham?")





print(response.name)



# > 'Paul Graham'



print(response.best_known_for)



# > ['working on Bel', 'co-founding Viaweb', 'creating the programming language Arc']



print(response.extra_info)



# > "Paul Graham is a computer scientist, entrepreneur, and writer. He is best known      for ..."

```

## Modules
[Section titled “Modules”](https://developers.llamaindex.ai/python/framework/module_guides/querying/structured_outputs/query_engine/#modules)
Detailed usage is available in the notebooks below:
  * [Structured Outputs with a Query Engine](https://developers.llamaindex.ai/python/examples/query_engine/pydantic_query_engine)
  * [Structured Outputs with a Tree Summarize](https://developers.llamaindex.ai/python/examples/response_synthesizers/pydantic_tree_summarize)


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


