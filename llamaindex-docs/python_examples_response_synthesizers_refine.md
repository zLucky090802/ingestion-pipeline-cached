[Skip to content](https://developers.llamaindex.ai/python/examples/response_synthesizers/refine/#_top)
# Refine 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-llms-openai


```


```


!pip install llama-index


```

### Download Data
[Section titled “Download Data”](https://developers.llamaindex.ai/python/examples/response_synthesizers/refine/#download-data)

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```

## Load Data
[Section titled “Load Data”](https://developers.llamaindex.ai/python/examples/response_synthesizers/refine/#load-data)

```


from llama_index.core import SimpleDirectoryReader


```


```


reader = SimpleDirectoryReader(




input_files=["./data/paul_graham/paul_graham_essay.txt"]



```


```


docs = reader.load_data()


```


```


text = docs[0].text


```

## Summarize
[Section titled “Summarize”](https://developers.llamaindex.ai/python/examples/response_synthesizers/refine/#summarize)

```


from llama_index.llms.openai import OpenAI





llm = OpenAI(model="gpt-3.5-turbo")


```


```


from llama_index.core.response_synthesizers import Refine





summarizer = Refine(llm=llm, verbose=True)


```


```


response = summarizer.get_response("who is Paul Graham?", [text])


```


```

> Refine context: making fakes for a local antique dealer. She'd ...


> Refine context: look legit, and the key to looking legit is hig...


> Refine context: me 8 years to realize it. Even then it took me ...


> Refine context: was one thing rarer than Rtm offering advice, i...

```


```


print(response)


```


```

Paul Graham is an individual who has played a crucial role in shaping the internet infrastructure and has also pursued a career as a writer. At one point, he received advice from a friend that urged him not to let Y Combinator be his final noteworthy achievement. This advice prompted him to reflect on his future with Y Combinator and ultimately led him to pass on the responsibility to others. He approached Jessica and Sam Altman to assume leadership positions in Y Combinator, aiming to secure its continued success.

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


