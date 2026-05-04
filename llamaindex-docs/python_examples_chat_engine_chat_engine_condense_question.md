[Skip to content](https://developers.llamaindex.ai/python/examples/chat_engine/chat_engine_condense_question/#_top)
# Chat Engine - Condense Question Mode 
Condense question is a simple chat mode built on top of a query engine over your data.
For each chat interaction:
  * first generate a standalone question from conversation context and last message, then
  * query the query engine with the condensed question for a response.


This approach is simple, and works for questions directly related to the knowledge base. Since it _always_ queries the knowledge base, it can have difficulty answering meta questions like “what did I ask you before?”
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-llms-openai


```


```


!pip install llama-index


```

## Download Data
[Section titled “Download Data”](https://developers.llamaindex.ai/python/examples/chat_engine/chat_engine_condense_question/#download-data)

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```

## Get started in 5 lines of code
[Section titled “Get started in 5 lines of code”](https://developers.llamaindex.ai/python/examples/chat_engine/chat_engine_condense_question/#get-started-in-5-lines-of-code)
Load data and build index

```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader





data = SimpleDirectoryReader(input_dir="./data/paul_graham/").load_data()




index = VectorStoreIndex.from_documents(data)


```

Configure chat engine

```


chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)


```

Chat with your data

```


response = chat_engine.chat("What did Paul Graham do after YC?")


```


```

Querying with: What was the next step in Paul Graham's career after his involvement with Y Combinator?

```


```


print(response)


```


```

Paul Graham's next step in his career after his involvement with Y Combinator was to take up painting. He spent most of the rest of 2014 painting and then in March 2015 he started working on Lisp again.

```

Ask a follow up question

```


response = chat_engine.chat("What about after that?")


```


```

Querying with: What did Paul Graham do after he started working on Lisp again in March 2015?

```


```


print(response)


```


```

Paul Graham spent the rest of 2015 writing essays and working on his new dialect of Lisp, which he called Arc. He also looked for an apartment to buy and started planning a second still life painting from the same objects.

```


```


response = chat_engine.chat("Can you tell me more?")


```


```

Querying with: What did Paul Graham do after he started working on Lisp again in March 2015?

```


```


print(response)


```


```

Paul Graham spent the rest of 2015 writing essays and working on his new dialect of Lisp, which he called Arc. He also looked for an apartment to buy and started planning for a second still life painting.

```

Reset conversation state

```

chat_engine.reset()

```


```


response = chat_engine.chat("What about after that?")


```


```

Querying with: What happens after the current situation?

```


```


print(response)


```


```

After the current situation, the narrator resumes painting and experimenting with a new kind of still life. He also resumes his old life in New York, now that he is rich. He is able to take taxis and eat in restaurants, which is exciting for a while. He also starts to make connections with other people who are trying to paint in New York.

```

## Streaming Support
[Section titled “Streaming Support”](https://developers.llamaindex.ai/python/examples/chat_engine/chat_engine_condense_question/#streaming-support)

```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader




from llama_index.llms.openai import OpenAI





llm = OpenAI(model="gpt-3.5-turbo", temperature=0)





data = SimpleDirectoryReader(input_dir="../data/paul_graham/").load_data()





index = VectorStoreIndex.from_documents(data)


```


```


chat_engine = index.as_chat_engine(




chat_mode="condense_question", llm=llm, verbose=True



```


```


response = chat_engine.stream_chat("What did Paul Graham do after YC?")




for token in response.response_gen:




print(token, end="")


```


```

Querying with: What did Paul Graham do after leaving YC?


After leaving YC, Paul Graham started painting and focused on improving his skills in that area. He then started writing essays again and began working on Lisp.

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


