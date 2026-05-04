[Skip to content](https://developers.llamaindex.ai/python/examples/docstore/docstoredemo/#_top)
# Docstore Demo 
This guide shows you how to directly use our `DocumentStore` abstraction. By putting nodes in the docstore, this allows you to define multiple indices over the same underlying docstore, instead of duplicating data across indices.
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


import logging




import sys





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


```


```


from llama_index.core import SimpleDirectoryReader




from llama_index.core import VectorStoreIndex, SimpleKeywordTableIndex




from llama_index.core import SummaryIndex




from llama_index.core import ComposableGraph




from llama_index.llms.openai import OpenAI




from llama_index.core import Settings


```

#### Download Data
[Section titled “Download Data”](https://developers.llamaindex.ai/python/examples/docstore/docstoredemo/#download-data)

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```

#### Load Documents
[Section titled “Load Documents”](https://developers.llamaindex.ai/python/examples/docstore/docstoredemo/#load-documents)

```


reader = SimpleDirectoryReader("./data/paul_graham/")




documents = reader.load_data()


```

#### Parse into Nodes
[Section titled “Parse into Nodes”](https://developers.llamaindex.ai/python/examples/docstore/docstoredemo/#parse-into-nodes)

```


from llama_index.core.node_parser import SentenceSplitter





nodes = SentenceSplitter().get_nodes_from_documents(documents)


```

#### Add to Docstore
[Section titled “Add to Docstore”](https://developers.llamaindex.ai/python/examples/docstore/docstoredemo/#add-to-docstore)

```


from llama_index.core.storage.docstore import SimpleDocumentStore





docstore = SimpleDocumentStore()



docstore.add_documents(nodes)

```

#### Define Multiple Indexes
[Section titled “Define Multiple Indexes”](https://developers.llamaindex.ai/python/examples/docstore/docstoredemo/#define-multiple-indexes)
Each index uses the same underlying Node.

```


from llama_index.core import StorageContext






storage_context = StorageContext.from_defaults(docstore=docstore)




summary_index = SummaryIndex(nodes, storage_context=storage_context)




vector_index = VectorStoreIndex(nodes, storage_context=storage_context)




keyword_table_index = SimpleKeywordTableIndex(




nodes, storage_context=storage_context



```


```


# NOTE: the docstore still has the same nodes




len(storage_context.docstore.docs)


```

#### Test out some Queries
[Section titled “Test out some Queries”](https://developers.llamaindex.ai/python/examples/docstore/docstoredemo/#test-out-some-queries)

```


llm = OpenAI(temperature=0, model="gpt-3.5-turbo")





Settings.llm = llm




Settings.chunk_size =1024


```


```

WARNING:llama_index.llm_predictor.base:Unknown max input size for gpt-3.5-turbo, using defaults.


Unknown max input size for gpt-3.5-turbo, using defaults.

```


```


query_engine = summary_index.as_query_engine()




response = query_engine.query("What is a summary of this document?")


```


```


query_engine = vector_index.as_query_engine()




response = query_engine.query("What did the author do growing up?")


```


```


query_engine = keyword_table_index.as_query_engine()




response = query_engine.query("What did the author do after his time at YC?")


```


```


print(response)


```


```

After his time at YC, the author decided to take a break and focus on painting. He spent most of 2014 painting and then, in November, he ran out of steam and stopped. He then moved to Florence, Italy to attend the Accademia di Belle Arti di Firenze, where he studied painting and drawing. He also started painting still lives in his bedroom at night. In March 2015, he started working on Lisp again and wrote a new Lisp, called Bel, in itself in Arc. He wrote essays through 2020, but also started to think about other things he could work on. He wrote an essay for himself to answer the question of how he should choose what to do next and then wrote a more detailed version for others to read. He also created the Y Combinator logo, which was an inside joke referencing the Viaweb logo, a white V on a red circle, so he made the YC logo a white Y on an orange square. He also created a fund for YC for a couple of years, but after Heroku got bought, he had enough money to go back to being self-funded. He also disliked the term "deal flow" because it implies that the number of new startups at any given time

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


