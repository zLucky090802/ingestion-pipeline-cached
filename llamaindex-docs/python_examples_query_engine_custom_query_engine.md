[Skip to content](https://developers.llamaindex.ai/python/examples/query_engine/custom_query_engine/#_top)
# Defining a Custom Query Engine 
You can (and should) define your custom query engines in order to plug into your downstream LlamaIndex workflows, whether you’re building RAG, agents, or other applications.
We provide a `CustomQueryEngine` that makes it easy to define your own queries.
## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/examples/query_engine/custom_query_engine/#setup)
We first load some sample data and index it.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-llms-openai


```


```


!pip install llama-index


```


```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader


```

Download Data

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```


```

# load documents



documents = SimpleDirectoryReader("./data//paul_graham/").load_data()


```


```


index = VectorStoreIndex.from_documents(documents)




retriever = index.as_retriever()


```

## Building a Custom Query Engine
[Section titled “Building a Custom Query Engine”](https://developers.llamaindex.ai/python/examples/query_engine/custom_query_engine/#building-a-custom-query-engine)
We build a custom query engine that simulates a RAG pipeline. First perform retrieval, and then synthesis.
To define a `CustomQueryEngine`, you just have to define some initialization parameters as attributes and implement the `custom_query` function.
By default, the `custom_query` can return a `Response` object (which the response synthesizer returns), but it can also just return a string. These are options 1 and 2 respectively.

```


from llama_index.core.query_engine import CustomQueryEngine




from llama_index.core.retrievers import BaseRetriever




from llama_index.core import get_response_synthesizer




from llama_index.core.response_synthesizers import BaseSynthesizer


```

### Option 1 (`RAGQueryEngine`)
[Section titled “Option 1 (RAGQueryEngine)”](https://developers.llamaindex.ai/python/examples/query_engine/custom_query_engine/#option-1-ragqueryengine)

```


classRAGQueryEngine(CustomQueryEngine):




"""RAG Query Engine."""





retriever: BaseRetriever




response_synthesizer: BaseSynthesizer





defcustom_query(self, query_str: str):




nodes =self.retriever.retrieve(query_str)




response_obj =self.response_synthesizer.synthesize(query_str, nodes)




return response_obj


```

### Option 2 (`RAGStringQueryEngine`)
[Section titled “Option 2 (RAGStringQueryEngine)”](https://developers.llamaindex.ai/python/examples/query_engine/custom_query_engine/#option-2-ragstringqueryengine)

```

# Option 2: return a string (we use a raw LLM call for illustration)




from llama_index.llms.openai import OpenAI




from llama_index.core import PromptTemplate





qa_prompt = PromptTemplate(




"Context information is below.\n"




"---------------------\n"




"{context_str}\n"




"---------------------\n"




"Given the context information and not prior knowledge, "




"answer the query.\n"




"Query: {query_str}\n"




"Answer: "







classRAGStringQueryEngine(CustomQueryEngine):




"""RAG String Query Engine."""





retriever: BaseRetriever




response_synthesizer: BaseSynthesizer




llm: OpenAI




qa_prompt: PromptTemplate





defcustom_query(self, query_str: str):




nodes =self.retriever.retrieve(query_str)





context_str ="\n\n".join([n.node.get_content() forin nodes])




response =self.llm.complete(




qa_prompt.format(context_str=context_str, query_str=query_str)






returnstr(response)


```

## Trying it out
[Section titled “Trying it out”](https://developers.llamaindex.ai/python/examples/query_engine/custom_query_engine/#trying-it-out)
We now try it out on our sample data.
### Trying Option 1 (`RAGQueryEngine`)
[Section titled “Trying Option 1 (RAGQueryEngine)”](https://developers.llamaindex.ai/python/examples/query_engine/custom_query_engine/#trying-option-1-ragqueryengine)

```


synthesizer = get_response_synthesizer(response_mode="compact")




query_engine = RAGQueryEngine(




retriever=retriever, response_synthesizer=synthesizer



```


```


response = query_engine.query("What did the author do growing up?")


```


```


print(str(response))


```


```

The author worked on writing and programming outside of school before college. They wrote short stories and tried writing programs on an IBM 1401 computer using an early version of Fortran. They also mentioned getting a microcomputer, building it themselves, and writing simple games and programs on it.

```


```


print(response.source_nodes[0].get_content())


```

### Trying Option 2 (`RAGStringQueryEngine`)
[Section titled “Trying Option 2 (RAGStringQueryEngine)”](https://developers.llamaindex.ai/python/examples/query_engine/custom_query_engine/#trying-option-2-ragstringqueryengine)

```


llm = OpenAI(model="gpt-3.5-turbo")





query_engine = RAGStringQueryEngine(




retriever=retriever,




response_synthesizer=synthesizer,




llm=llm,




qa_prompt=qa_prompt,



```


```


response = query_engine.query("What did the author do growing up?")


```


```


print(str(response))


```


```

The author worked on writing and programming before college. They wrote short stories and started programming on the IBM 1401 computer in 9th grade. They later got a microcomputer and continued programming, writing simple games and a word processor.

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


