[Skip to content](https://developers.llamaindex.ai/python/examples/response_synthesizers/tree_summarize/#_top)
# Tree Summarize 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


!pip install llama-index


```

## Download Data
[Section titled “Download Data”](https://developers.llamaindex.ai/python/examples/response_synthesizers/tree_summarize/#download-data)

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```

## Load Data
[Section titled “Load Data”](https://developers.llamaindex.ai/python/examples/response_synthesizers/tree_summarize/#load-data)

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
[Section titled “Summarize”](https://developers.llamaindex.ai/python/examples/response_synthesizers/tree_summarize/#summarize)

```


from llama_index.core.response_synthesizers import TreeSummarize


```


```


summarizer = TreeSummarize(verbose=True)


```


```


response =await summarizer.aget_response("who is Paul Graham?", [text])


```


```

6 text chunks after repacking


1 text chunks after repacking

```


```


print(response)


```


```

Paul Graham is a computer scientist, writer, artist, entrepreneur, investor, and essayist. He is best known for his work in artificial intelligence, Lisp programming, and writing the book On Lisp, as well as for co-founding the startup accelerator Y Combinator and for his essays on technology, business, and start-ups. He is also the creator of the programming language Arc and the Lisp dialect Bel.

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


