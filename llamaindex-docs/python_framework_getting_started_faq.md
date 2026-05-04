[Skip to content](https://developers.llamaindex.ai/python/framework/getting_started/faq/#_top)
LlamaIndex Framework
Getting Started
[Frequently Asked Questions (FAQ)](https://developers.llamaindex.ai/python/framework/getting_started/faq/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Frequently Asked Questions (FAQ)
In this section, we start with the code you wrote for the [starter example](https://developers.llamaindex.ai/python/framework/getting_started/starter_example) and show you the most common ways you might want to customize it for your use case:

```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader





documents = SimpleDirectoryReader("data").load_data()




index = VectorStoreIndex.from_documents(documents)




query_engine = index.as_query_engine()




response = query_engine.query("What did the author do growing up?")




print(response)


```

## **“I want to parse my documents into smaller chunks"**
[Section titled ““I want to parse my documents into smaller chunks"”](https://developers.llamaindex.ai/python/framework/getting_started/faq/#i-want-to-parse-my-documents-into-smaller-chunks)

```

# Global settings



from llama_index.core import Settings





Settings.chunk_size =512




# Local settings



from llama_index.core.node_parser import SentenceSplitter





index = VectorStoreIndex.from_documents(




documents, transformations=[SentenceSplitter(chunk_size=512)]



```

## **"I want to use a different vector store”**
[Section titled “"I want to use a different vector store””](https://developers.llamaindex.ai/python/framework/getting_started/faq/#i-want-to-use-a-different-vector-store)
First, you can install the vector store you want to use. For example, to use Chroma as the vector store, you can install it using pip:
Terminal window
```


pipinstallllama-index-vector-stores-chroma


```

To learn more about all integrations available, check out [LlamaHub](https://llamahub.ai).
Then, you can use it in your code:

```


import chromadb




from llama_index.vector_stores.chroma import ChromaVectorStore




from llama_index.core import StorageContext





chroma_client = chromadb.PersistentClient()




chroma_collection = chroma_client.create_collection("quickstart")




vector_store = ChromaVectorStore(chroma_collection=chroma_collection)




storage_context = StorageContext.from_defaults(vector_store=vector_store)


```

`StorageContext` defines the storage backend for where the documents, embeddings, and indexes are stored. You can learn more about [storage](https://developers.llamaindex.ai/python/framework/module_guides/storing) and [how to customize it](https://developers.llamaindex.ai/python/framework/module_guides/storing/customization).

```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader





documents = SimpleDirectoryReader("data").load_data()




index = VectorStoreIndex.from_documents(




documents, storage_context=storage_context





query_engine = index.as_query_engine()




response = query_engine.query("What did the author do growing up?")




print(response)


```

## **”I want to retrieve more context when I query”**
[Section titled “”I want to retrieve more context when I query””](https://developers.llamaindex.ai/python/framework/getting_started/faq/#i-want-to-retrieve-more-context-when-i-query)

```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader





documents = SimpleDirectoryReader("data").load_data()




index = VectorStoreIndex.from_documents(documents)




query_engine = index.as_query_engine(similarity_top_k=5)




response = query_engine.query("What did the author do growing up?")




print(response)


```

`as_query_engine` builds a default `retriever` and `query engine` on top of the index. You can configure the retriever and query engine by passing in keyword arguments. Here, we configure the retriever to return the top 5 most similar documents (instead of the default of 2). You can learn more about [retrievers](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retrievers) and [query engines](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever).
## **”I want to use a different LLM”**
[Section titled “”I want to use a different LLM””](https://developers.llamaindex.ai/python/framework/getting_started/faq/#i-want-to-use-a-different-llm)

```

# Global settings



from llama_index.core import Settings




from llama_index.llms.ollama import Ollama





Settings.llm = Ollama(




model="mistral",




request_timeout=60.0,




# Manually set the context window to limit memory usage




context_window=8000,





# Local settings


index.as_query_engine(



llm=Ollama(




model="mistral",




request_timeout=60.0,




# Manually set the context window to limit memory usage




context_window=8000,




```

You can learn more about [customizing LLMs](https://developers.llamaindex.ai/python/framework/module_guides/models/llms).
## **”I want to use a different response mode”**
[Section titled “”I want to use a different response mode””](https://developers.llamaindex.ai/python/framework/getting_started/faq/#i-want-to-use-a-different-response-mode)

```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader





documents = SimpleDirectoryReader("data").load_data()




index = VectorStoreIndex.from_documents(documents)




query_engine = index.as_query_engine(response_mode="tree_summarize")




response = query_engine.query("What did the author do growing up?")




print(response)


```

You can learn more about [query engines](https://developers.llamaindex.ai/python/framework/module_guides/querying) and [response modes](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/response_modes).
## **”I want to stream the response back”**
[Section titled “”I want to stream the response back””](https://developers.llamaindex.ai/python/framework/getting_started/faq/#i-want-to-stream-the-response-back)

```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader





documents = SimpleDirectoryReader("data").load_data()




index = VectorStoreIndex.from_documents(documents)




query_engine = index.as_query_engine(streaming=True)




response = query_engine.query("What did the author do growing up?")



response.print_response_stream()

```

You can learn more about [streaming responses](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/streaming).
## **”I want a chatbot instead of Q &A”**
[Section titled “”I want a chatbot instead of Q&A””](https://developers.llamaindex.ai/python/framework/getting_started/faq/#i-want-a-chatbot-instead-of-qa)

```


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader





documents = SimpleDirectoryReader("data").load_data()




index = VectorStoreIndex.from_documents(documents)




query_engine = index.as_chat_engine()




response = query_engine.chat("What did the author do growing up?")




print(response)





response = query_engine.chat("Oh interesting, tell me more.")




print(response)


```

Learn more about the [chat engine](https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines/usage_pattern).
## Next Steps
[Section titled “Next Steps”](https://developers.llamaindex.ai/python/framework/getting_started/faq/#next-steps)
  * Want a thorough walkthrough of (almost) everything you can configure? Get started with [Understanding LlamaIndex](https://developers.llamaindex.ai/python/framework/understanding).
  * Want more in-depth understanding of specific modules? Check out the [component guides](https://developers.llamaindex.ai/python/framework/module_guides).


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


