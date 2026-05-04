[Skip to content](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neo4jkgindexdemo/#_top)
# Neo4j Graph Store 

```


%pip install llama-index-llms-openai




%pip install llama-index-graph-stores-neo4j




%pip install llama-index-embeddings-openai




%pip install llama-index-llms-azure-openai


```


```

# For OpenAI




import os





os.environ["OPENAI_API_KEY"] ="API_KEY_HERE"





import logging




import sys




from llama_index.llms.openai import OpenAI




from llama_index.core import Settings





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




# define LLM



llm = OpenAI(temperature=0, model="gpt-3.5-turbo")




Settings.llm = llm




Settings.chunk_size =512


```


```

# For Azure OpenAI



import os




import json




import openai




from llama_index.llms.azure_openai import AzureOpenAI




from llama_index.embeddings.openai import OpenAIEmbedding




from llama_index.core import (




VectorStoreIndex,




SimpleDirectoryReader,




KnowledgeGraphIndex,






import logging




import sys





from IPython.display import Markdown, display




logging.basicConfig(



stream=sys.stdout, level=logging.INFO




# logging.DEBUG for more verbose output




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))





openai.api_type ="azure"




openai.api_base ="https://<foo-bar>.openai.azure.com"




openai.api_version ="2022-12-01"




os.environ["OPENAI_API_KEY"] ="<your-openai-key>"




openai.api_key = os.getenv("OPENAI_API_KEY")





llm = AzureOpenAI(




deployment_name="<foo-bar-deployment>",




temperature=0,




openai_api_version=openai.api_version,




model_kwargs={




"api_key": openai.api_key,




"api_base": openai.api_base,




"api_type": openai.api_type,




"api_version": openai.api_version,






# You need to deploy your own embedding model as well as your own chat completion model



embedding_llm = OpenAIEmbedding(




model="text-embedding-ada-002",




deployment_name="<foo-bar-deployment>",




api_key=openai.api_key,




api_base=openai.api_base,




api_type=openai.api_type,




api_version=openai.api_version,






Settings.llm = llm




Settings.embed_model = embedding_llm




Settings.chunk_size =512


```

## Using Knowledge Graph with Neo4jGraphStore
[Section titled “Using Knowledge Graph with Neo4jGraphStore”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neo4jkgindexdemo/#using-knowledge-graph-with-neo4jgraphstore)
#### Building the Knowledge Graph
[Section titled “Building the Knowledge Graph”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neo4jkgindexdemo/#building-the-knowledge-graph)

```


from llama_index.core import KnowledgeGraphIndex, SimpleDirectoryReader




from llama_index.core import StorageContext




from llama_index.graph_stores.neo4j import Neo4jGraphStore






from llama_index.llms.openai import OpenAI




from IPython.display import Markdown, display


```


```


documents = SimpleDirectoryReader(




"../../../../examples/paul_graham_essay/data"



).load_data()

```

## Prepare for Neo4j
[Section titled “Prepare for Neo4j”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neo4jkgindexdemo/#prepare-for-neo4j)

```


%pip install neo4j





username ="neo4j"




password ="retractor-knot-thermocouples"




url ="bolt://44.211.44.239:7687"




database ="neo4j"


```


```

Requirement already satisfied: neo4j in /home/tomaz/anaconda3/envs/snakes/lib/python3.9/site-packages (5.11.0)


Requirement already satisfied: pytz in /home/tomaz/anaconda3/envs/snakes/lib/python3.9/site-packages (from neo4j) (2023.3)


Note: you may need to restart the kernel to use updated packages.

```

## Instantiate Neo4jGraph KG Indexes
[Section titled “Instantiate Neo4jGraph KG Indexes”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neo4jkgindexdemo/#instantiate-neo4jgraph-kg-indexes)

```


graph_store = Neo4jGraphStore(




username=username,




password=password,




url=url,




database=database,






storage_context = StorageContext.from_defaults(graph_store=graph_store)





# NOTE: can take a while!




index = KnowledgeGraphIndex.from_documents(




documents,




storage_context=storage_context,




max_triplets_per_chunk=2,



```

#### Querying the Knowledge Graph
[Section titled “Querying the Knowledge Graph”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neo4jkgindexdemo/#querying-the-knowledge-graph)
First, we can query and send only the triplets to the LLM.

```


query_engine = index.as_query_engine(




include_text=False, response_mode="tree_summarize"






response = query_engine.query("Tell me more about Interleaf")


```


```

INFO:llama_index.indices.knowledge_graph.retriever:> Starting query: Tell me more about Interleaf


INFO:llama_index.indices.knowledge_graph.retriever:> Query keywords: ['Interleaf']


ERROR:llama_index.indices.knowledge_graph.retriever:Index was not constructed with embeddings, skipping embedding usage...


INFO:llama_index.indices.knowledge_graph.retriever:> Extracted relationships: The following are knowledge sequence in max depth 2 in the form of `subject [predicate, object, predicate_next_hop, object_next_hop ...]`


Interleaf ['IS_ABOUT', 'what not to do']


Interleaf ['ADDED', 'scripting language']


Interleaf ['MADE', 'software for creating documents']

```


```


display(Markdown(f"<b>{response}</b>"))


```

**Interleaf is a subject that is related to “what not to do” and “scripting language”. It is also associated with the predicates “ADDED” and “MADE”, with the objects being “scripting language” and “software for creating documents” respectively.**
For more detailed answers, we can also send the text from where the retrieved tripets were extracted.

```


query_engine = index.as_query_engine(




include_text=True, response_mode="tree_summarize"





response = query_engine.query(




"Tell me more about what the author worked on at Interleaf"



```


```

INFO:llama_index.indices.knowledge_graph.retriever:> Starting query: Tell me more about what the author worked on at Interleaf


INFO:llama_index.indices.knowledge_graph.retriever:> Query keywords: ['Interleaf', 'worked', 'author']


ERROR:llama_index.indices.knowledge_graph.retriever:Index was not constructed with embeddings, skipping embedding usage...


INFO:llama_index.indices.knowledge_graph.retriever:> Querying with idx: c3fd9444-6c20-4cdc-9598-8f0e9ed0b85d: each student had. But the Accademia wasn't teaching me anything except Italia...


INFO:llama_index.indices.knowledge_graph.retriever:> Querying with idx: f4bfad23-0cde-4425-99f9-9229ca0a5cc5: learned some useful things at Interleaf, though they were mostly about what n...


INFO:llama_index.indices.knowledge_graph.retriever:> Extracted relationships: The following are knowledge sequence in max depth 2 in the form of `subject [predicate, object, predicate_next_hop, object_next_hop ...]`


Interleaf ['IS_ABOUT', 'what not to do']


Interleaf ['ADDED', 'scripting language']


Interleaf ['MADE', 'software for creating documents']

```


```


display(Markdown(f"<b>{response}</b>"))


```

**At Interleaf, the author worked on software for creating documents. The company had added a scripting language, inspired by Emacs, and the author was hired as a Lisp hacker to write things in it. However, the author admits to being a bad employee and not fully understanding the software, as it was primarily written in C. Despite this, the author was paid well and managed to save enough money to go back to RISD and pay off their college loans. The author also learned some valuable lessons at Interleaf, particularly about what not to do in technology companies.**
#### Query with embeddings
[Section titled “Query with embeddings”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neo4jkgindexdemo/#query-with-embeddings)

```

# Clean dataset first


graph_store.query(



MATCH (n) DETACH DELETE n






# NOTE: can take a while!




index = KnowledgeGraphIndex.from_documents(




documents,




storage_context=storage_context,




max_triplets_per_chunk=2,




include_embeddings=True,






query_engine = index.as_query_engine(




include_text=True,




response_mode="tree_summarize",




embedding_mode="hybrid",




similarity_top_k=5,



```


```

# query using top 3 triplets plus keywords (duplicate triplets are removed)



response = query_engine.query(




"Tell me more about what the author worked on at Interleaf"



```


```

INFO:llama_index.indices.knowledge_graph.retriever:> Starting query: Tell me more about what the author worked on at Interleaf


INFO:llama_index.indices.knowledge_graph.retriever:> Query keywords: ['Interleaf', 'worked', 'author']


INFO:llama_index.indices.knowledge_graph.retriever:> Querying with idx: e0067958-8b62-4186-b78c-a07281531e40: each student had. But the Accademia wasn't teaching me anything except Italia...


INFO:llama_index.indices.knowledge_graph.retriever:> Querying with idx: 38459cd5-bc20-428d-a2db-9dc2e716bd15: learned some useful things at Interleaf, though they were mostly about what n...


INFO:llama_index.indices.knowledge_graph.retriever:> Querying with idx: 6be24830-85d5-49d1-8caa-d297cd0e8b14: It had been so long since I'd painted anything that I'd half forgotten why I ...


INFO:llama_index.indices.knowledge_graph.retriever:> Querying with idx: 2ec81827-d6d5-470d-8851-b97b8d8d80b4: Robert Morris showed it to me when I visited him in Cambridge, where he was n...


INFO:llama_index.indices.knowledge_graph.retriever:> Querying with idx: 46b8b977-4176-4622-8d4d-ee3ab16132b4: in decent shape at painting and drawing from the RISD foundation that summer,...


INFO:llama_index.indices.knowledge_graph.retriever:> Querying with idx: 71363c09-ec6b-47c8-86ac-e18be46f1cc2: as scare-quotes. At the time this bothered me, but now it seems amusingly acc...


INFO:llama_index.indices.knowledge_graph.retriever:> Querying with idx: 2dded283-d876-4014-8352-056fccace896: of my old life. Idelle was in New York at least, and there were other people ...


INFO:llama_index.indices.knowledge_graph.retriever:> Querying with idx: de937aec-ebee-4348-9f23-c94d0a5d7436: and I had a lot of time to think on those flights. On one of them I realized ...


INFO:llama_index.indices.knowledge_graph.retriever:> Querying with idx: 33936f7a-0f89-48c7-af9a-171372b4b4b0: What I Worked On



February 2021



Before college the two main things I worked ...


INFO:llama_index.indices.knowledge_graph.retriever:> Extracted relationships: The following are knowledge sequence in max depth 2 in the form of `subject [predicate, object, predicate_next_hop, object_next_hop ...]`


('Interleaf', 'made', 'software for creating documents')


Interleaf ['MADE', 'software for creating documents']


('Interleaf', 'added', 'scripting language')


('Interleaf', 'is about', 'what not to do')


Interleaf ['ADDED', 'scripting language']


Interleaf ['IS_ABOUT', 'what not to do']


('I', 'worked on', 'programming')


('I', 'worked on', 'writing')

```


```


display(Markdown(f"<b>{response}</b>"))


```

**At Interleaf, the author worked on writing scripts in a Lisp dialect for the company’s software, which was used for creating documents.**
#### [Optional] Try building the graph and manually add triplets!
[Section titled “[Optional] Try building the graph and manually add triplets!”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neo4jkgindexdemo/#optional-try-building-the-graph-and-manually-add-triplets)

```


from llama_index.core.node_parser import SentenceSplitter


```


```


node_parser = SentenceSplitter()


```


```


nodes = node_parser.get_nodes_from_documents(documents)


```


```

# initialize an empty index for now



index = KnowledgeGraphIndex.from_documents([], storage_context=storage_context)


```


```

# add keyword mappings and nodes manually


# add triplets (subject, relationship, object)



# for node 0



node_0_tups = [




("author", "worked on", "writing"),




("author", "worked on", "programming"),





for tup in node_0_tups:




index.upsert_triplet_and_node(tup, nodes[0])




# for node 1



node_1_tups = [




("Interleaf", "made software for", "creating documents"),




("Interleaf", "added", "scripting language"),




("software", "generate", "web sites"),





for tup in node_1_tups:




index.upsert_triplet_and_node(tup, nodes[1])


```


```


query_engine = index.as_query_engine(




include_text=False, response_mode="tree_summarize"






response = query_engine.query("Tell me more about Interleaf")


```


```

INFO:llama_index.indices.knowledge_graph.retriever:> Starting query: Tell me more about Interleaf


INFO:llama_index.indices.knowledge_graph.retriever:> Query keywords: ['Solutions', 'Interleaf', 'Software', 'Information', 'Technology']


ERROR:llama_index.indices.knowledge_graph.retriever:Index was not constructed with embeddings, skipping embedding usage...


INFO:llama_index.indices.knowledge_graph.retriever:> Extracted relationships: The following are knowledge sequence in max depth 2 in the form of `subject [predicate, object, predicate_next_hop, object_next_hop ...]`


Interleaf ['MADE_SOFTWARE_FOR', 'creating documents']


Interleaf ['IS_ABOUT', 'what not to do']


Interleaf ['ADDED', 'scripting language']


Interleaf ['MADE', 'software for creating documents']

```


```


display(Markdown(f"<b>{response}</b>"))


```

**Interleaf is a software company that specializes in creating documents. It has added a scripting language to its software to make it easier for users to create documents. It also provides advice on what not to do when creating documents.**
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


