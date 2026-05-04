[Skip to content](https://developers.llamaindex.ai/python/examples/property_graph/property_graph_custom_retriever/#_top)
# Defining a Custom Property Graph Retriever 
This guide shows you how to define a custom retriever against a property graph.
It is more involved than using our out-of-the-box graph retrievers, but allows you to have granular control over the retrieval process so that it’s better tailored for your application.
We show you how to define an advanced retrieval flow by directly leveraging the property graph store. We’ll execute both vector search and text-to-cypher retrieval, and then combine the results through a reranking module.

```


%pip install llama-index




%pip install llama-index-graph-stores-neo4j




%pip install llama-index-postprocessor-cohere-rerank


```

## Setup and Build the Property Graph
[Section titled “Setup and Build the Property Graph”](https://developers.llamaindex.ai/python/examples/property_graph/property_graph_custom_retriever/#setup-and-build-the-property-graph)

```


import nest_asyncio




nest_asyncio.apply()

```


```


import os





os.environ["OPENAI_API_KEY"] ="sk-..."


```

#### Load Paul Graham Essay
[Section titled “Load Paul Graham Essay”](https://developers.llamaindex.ai/python/examples/property_graph/property_graph_custom_retriever/#load-paul-graham-essay)

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```


```


from llama_index.core import SimpleDirectoryReader





documents = SimpleDirectoryReader("./data/paul_graham/").load_data()


```


```

/Users/loganmarkewich/Library/Caches/pypoetry/virtualenvs/llama-index-bXUwlEfH-py3.11/lib/python3.11/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html



from .autonotebook import tqdm as notebook_tqdm


```

#### Define Default LLMs
[Section titled “Define Default LLMs”](https://developers.llamaindex.ai/python/examples/property_graph/property_graph_custom_retriever/#define-default-llms)

```


from llama_index.embeddings.openai import OpenAIEmbedding




from llama_index.llms.openai import OpenAI





llm = OpenAI(model="gpt-3.5-turbo", temperature=0.3)




embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")


```


```

/Users/loganmarkewich/Library/Caches/pypoetry/virtualenvs/llama-index-bXUwlEfH-py3.11/lib/python3.11/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html



from .autonotebook import tqdm as notebook_tqdm


```

#### Setup Neo4j
[Section titled “Setup Neo4j”](https://developers.llamaindex.ai/python/examples/property_graph/property_graph_custom_retriever/#setup-neo4j)
To launch Neo4j locally, first ensure you have docker installed. Then, you can launch the database with the following docker command

```

docker run \



-p 7474:7474 -p 7687:7687 \




-v $PWD/data:/data -v $PWD/plugins:/plugins \




--name neo4j-apoc \




-e NEO4J_apoc_export_file_enabled=true \




-e NEO4J_apoc_import_file_enabled=true \




-e NEO4J_apoc_import_file_use__neo4j__config=true \




-e NEO4JLABS_PLUGINS=\[\"apoc\"\] \




neo4j:latest


```

From here, you can open the db at <http://localhost:7474/>. On this page, you will be asked to sign in. Use the default username/password of neo4j and neo4j.

```


from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore





graph_store = Neo4jPropertyGraphStore(




username="neo4j",




password="llamaindex",




url="bolt://localhost:7687",



```

#### Build the Property Graph
[Section titled “Build the Property Graph”](https://developers.llamaindex.ai/python/examples/property_graph/property_graph_custom_retriever/#build-the-property-graph)

```


from llama_index.core import PropertyGraphIndex





index = PropertyGraphIndex.from_documents(




documents,




llm=llm,




embed_model=embed_model,




property_graph_store=graph_store,




show_progress=True,



```

## Define Custom Retriever
[Section titled “Define Custom Retriever”](https://developers.llamaindex.ai/python/examples/property_graph/property_graph_custom_retriever/#define-custom-retriever)
Now we define a custom retriever by subclassing `CustomPGRetriever`.
#### 1. Initialization
[Section titled “1. Initialization”](https://developers.llamaindex.ai/python/examples/property_graph/property_graph_custom_retriever/#1-initialization)
We initialize two pre-existing property graph retrievers: the `VectorContextRetriever` and the `TextToCypherRetriever`, as well as the cohere reranker.
#### 2. Define `custom_retrieve`
[Section titled “2. Define custom_retrieve”](https://developers.llamaindex.ai/python/examples/property_graph/property_graph_custom_retriever/#2-define-custom_retrieve)
We then define the `custom_retrieve` function. It passes nodes through the two retrievers and gets back a final ranked list.
The return type here can be a string, `TextNode`, `NodeWithScore`, or a list of one of those types.

```


from llama_index.core.retrievers import (




CustomPGRetriever,




VectorContextRetriever,




TextToCypherRetriever,





from llama_index.core.graph_stores import PropertyGraphStore




from llama_index.core.vector_stores.types import VectorStore




from llama_index.core.embeddings import BaseEmbedding




from llama_index.core.prompts import PromptTemplate




from llama_index.core.llms importLLM




from llama_index.postprocessor.cohere_rerank import CohereRerank






from typing import Optional, Any, Union






classMyCustomRetriever(CustomPGRetriever):




"""Custom retriever with cohere reranking."""





definit(




self,




## vector context retriever params




embed_model: Optional[BaseEmbedding] =None,




vector_store: Optional[VectorStore] =None,




similarity_top_k: int=4,




path_depth: int=1,




## text-to-cypher params




llm: Optional[LLM] =None,




text_to_cypher_template: Optional[Union[PromptTemplate, str]] =None,




## cohere reranker params




cohere_api_key: Optional[str] =None,




cohere_top_n: int=2,




**kwargs: Any,




) -> None:




"""Uses any kwargs passed in from class constructor."""





self.vector_retriever = VectorContextRetriever(




self.graph_store,




include_text=self.include_text,




embed_model=embed_model,




vector_store=vector_store,




similarity_top_k=similarity_top_k,




path_depth=path_depth,






self.cypher_retriever = TextToCypherRetriever(




self.graph_store,




llm=llm,




text_to_cypher_template=text_to_cypher_template




## NOTE: you can attach other parameters here if you'd like






self.reranker = CohereRerank(




api_key=cohere_api_key, top_n=cohere_top_n






defcustom_retrieve(self, query_str: str) -> str:




"""Define custom retriever with reranking.





Could return `str`, `TextNode`, `NodeWithScore`, or a list of those.





nodes_1 =self.vector_retriever.retrieve(query_str)




nodes_2 =self.cypher_retriever.retrieve(query_str)




reranked_nodes =self.reranker.postprocess_nodes(




nodes_1 + nodes_2, query_str=query_str






## TMP: please change




final_text ="\n\n".join(




[n.get_content(metadata_mode="llm") forin reranked_nodes]






return final_text





# optional async method




# async def acustom_retrieve(self, query_str: str) -> str:




#     ...


```

## Test out the Custom Retriever
[Section titled “Test out the Custom Retriever”](https://developers.llamaindex.ai/python/examples/property_graph/property_graph_custom_retriever/#test-out-the-custom-retriever)
Now let’s initialize and test out the custom retriever against our data!
To build a full RAG pipeline, we use the `RetrieverQueryEngine` to combine our retriever with the LLM synthesis module - this is also used under the hood for the property graph index.

```


custom_sub_retriever = MyCustomRetriever(




index.property_graph_store,




include_text=True,




vector_store=index.vector_store,




cohere_api_key="...",



```


```


from llama_index.core.query_engine import RetrieverQueryEngine





query_engine = RetrieverQueryEngine.from_args(




index.as_retriever(sub_retrievers=[custom_sub_retriever]), llm=llm



```

#### Try out a ‘baseline’
[Section titled “Try out a ‘baseline’”](https://developers.llamaindex.ai/python/examples/property_graph/property_graph_custom_retriever/#try-out-a-baseline)
We compare against a baseline retriever that’s the vector context only.

```


base_retriever = VectorContextRetriever(




index.property_graph_store, include_text=True





base_query_engine = index.as_query_engine(sub_retrievers=[base_retriever])


```

### Try out some Queries
[Section titled “Try out some Queries”](https://developers.llamaindex.ai/python/examples/property_graph/property_graph_custom_retriever/#try-out-some-queries)

```


response = query_engine.query("Did the author like programming?")




print(str(response))


```


```

The author found working on programming challenging but satisfying, as indicated by the intense effort put into the project and the sense of accomplishment derived from solving complex problems while working on the code.

```


```


response = base_query_engine.query("Did the author like programming?")




print(str(response))


```


```

The author enjoyed programming, as evidenced by their early experiences with computers, such as writing simple games, creating programs for predicting rocket flights, and developing a word processor. These experiences indicate a genuine interest and enjoyment in programming activities.

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


