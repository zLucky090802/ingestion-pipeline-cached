[Skip to content](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/nebulagraphkgindexdemo/#_top)
# Nebula Graph Store 

```


%pip install llama-index-llms-openai




%pip install llama-index-embeddings-openai




%pip install llama-index-graph-stores-nebula




%pip install llama-index-llms-azure-openai


```


```

# For OpenAI




import os





os.environ["OPENAI_API_KEY"] ="INSERT OPENAI KEY"





import logging




import sys




from llama_index.llms.openai import OpenAI




from llama_index.core import Settings





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




# define LLM



# NOTE: at the time of demo, text-davinci-002 did not have rate-limit errors




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






from llama_index.core import StorageContext




from llama_index.graph_stores.nebula import NebulaGraphStore





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




model="<foo-bar-model>",




engine="<foo-bar-deployment>",




temperature=0,




api_key=openai.api_key,




api_type=openai.api_type,




api_base=openai.api_base,




api_version=openai.api_version,





# You need to deploy your own embedding model as well as your own chat completion model



embedding_model = OpenAIEmbedding(




model="text-embedding-ada-002",




deployment_name="<foo-bar-deployment>",




api_key=openai.api_key,




api_base=openai.api_base,




api_type=openai.api_type,




api_version=openai.api_version,






Settings.llm = llm




Settings.chunk_size = chunk_size




Settings.embed_model = embedding_model


```

## Using Knowledge Graph with NebulaGraphStore
[Section titled “Using Knowledge Graph with NebulaGraphStore”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/nebulagraphkgindexdemo/#using-knowledge-graph-with-nebulagraphstore)
#### Building the Knowledge Graph
[Section titled “Building the Knowledge Graph”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/nebulagraphkgindexdemo/#building-the-knowledge-graph)

```


from llama_index.core import KnowledgeGraphIndex, SimpleDirectoryReader




from llama_index.core import StorageContext




from llama_index.graph_stores.nebula import NebulaGraphStore






from llama_index.llms.openai import OpenAI




from IPython.display import Markdown, display


```


```


documents = SimpleDirectoryReader(




"../../../../examples/paul_graham_essay/data"



).load_data()

```

## Prepare for NebulaGraph
[Section titled “Prepare for NebulaGraph”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/nebulagraphkgindexdemo/#prepare-for-nebulagraph)

```


%pip install nebula3-python





os.environ["NEBULA_USER"] ="root"



os.environ[



"NEBULA_PASSWORD"




] ="<password>"# replace with your password, by default it is "nebula"



os.environ[



"NEBULA_ADDRESS"




] ="127.0.0.1:9669"# assumed we have NebulaGraph 3.5.0 or newer installed locally




# Assume that the graph has already been created


# Create a NebulaGraph cluster with:


# Option 0: `curl -fsSL nebula-up.siwei.io/install.sh | bash`


# Option 1: NebulaGraph Docker Extension https://hub.docker.com/extensions/weygu/nebulagraph-dd-ext


# and that the graph space is called "paul_graham_essay"


# If not, create it with the following commands from NebulaGraph's console:


# CREATE SPACE paul_graham_essay(vid_type=FIXED_STRING(256), partition_num=1, replica_factor=1);


# :sleep 10;


# USE paul_graham_essay;


# CREATE TAG entity(name string);


# CREATE EDGE relationship(relationship string);


# CREATE TAG INDEX entity_index ON entity(name(256));




space_name ="paul_graham_essay"




edge_types, rel_prop_names = ["relationship"], [




"relationship"




# default, could be omit if create from an empty kg




tags = ["entity"# default, could be omit if create from an empty kg


```

## Instantiate GPTNebulaGraph KG Indexes
[Section titled “Instantiate GPTNebulaGraph KG Indexes”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/nebulagraphkgindexdemo/#instantiate-gptnebulagraph-kg-indexes)

```


graph_store = NebulaGraphStore(




space_name=space_name,




edge_types=edge_types,




rel_prop_names=rel_prop_names,




tags=tags,






storage_context = StorageContext.from_defaults(graph_store=graph_store)





# NOTE: can take a while!




index = KnowledgeGraphIndex.from_documents(




documents,




storage_context=storage_context,




max_triplets_per_chunk=2,




space_name=space_name,




edge_types=edge_types,




rel_prop_names=rel_prop_names,




tags=tags,



```

#### Querying the Knowledge Graph
[Section titled “Querying the Knowledge Graph”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/nebulagraphkgindexdemo/#querying-the-knowledge-graph)

```


query_engine = index.as_query_engine()





response = query_engine.query("Tell me more about Interleaf")


```


```

INFO:llama_index.indices.knowledge_graph.retrievers:> Starting query: Tell me more about Interleaf


INFO:llama_index.indices.knowledge_graph.retrievers:> Query keywords: ['Interleaf', 'history', 'software', 'company']


ERROR:llama_index.indices.knowledge_graph.retrievers:Index was not constructed with embeddings, skipping embedding usage...


INFO:llama_index.indices.knowledge_graph.retrievers:> Querying with idx: 6aa6a716-7390-4783-955b-8169fab25bb1: worth trying.



Our teacher, professor Ulivi, was a nice guy. He could see I w...


INFO:llama_index.indices.knowledge_graph.retrievers:> Querying with idx: 79f2a1b4-80bb-416f-a259-ebfc3136b2fe: on a map of New York City: if you zoom in on the Upper East Side, there's a t...


INFO:llama_index.indices.knowledge_graph.retrievers:> Querying with idx: 1e707b8c-b62a-4c1a-a908-c79e77b9692b: buyers pay a lot for such work. [6]



There were plenty of earnest students to...


INFO:llama_index.indices.knowledge_graph.retrievers:> Querying with idx: 31c2f53c-928a-4ed0-88fc-df92dba47c33: for example, that the reason the color changes suddenly at a certain point is...


INFO:llama_index.indices.knowledge_graph.retrievers:> Querying with idx: f51d8a1c-06bc-45aa-bed1-1714ae4e5fb9: the software is an online store builder and you're hosting the stores, if you...


INFO:llama_index.indices.knowledge_graph.retrievers:> Querying with idx: 008052a0-a64b-4e3c-a2af-4963896bfc19: Engineering that seemed to be at least as big as the group that actually wrot...


INFO:llama_index.indices.knowledge_graph.retrievers:> Querying with idx: b1f5a610-9e0a-4e3e-ba96-514ae7d63a84: closures stored in a hash table on the server.



It helped to have studied art...


INFO:llama_index.indices.knowledge_graph.retrievers:> Querying with idx: f7cc82a7-76e0-4a06-9f50-d681404c5bce: of Robert's apartment in Cambridge. His roommate was away for big chunks of t...


INFO:llama_index.indices.knowledge_graph.retrievers:> Querying with idx: db626325-035a-4f67-87c0-1e770b80f4a6: want to be online, and still don't, not the fancy ones. That's not how they s...


INFO:llama_index.indices.knowledge_graph.retrievers:> Querying with idx: 73e76f4b-0ebe-4af6-9c2d-6affae81373b: But in the long term the growth rate takes care of the absolute number. If we...


INFO:llama_index.indices.knowledge_graph.retrievers:> Extracted relationships: The following are knowledge triplets in max depth 2 in the form of `subject [predicate, object, predicate_next_hop, object_next_hop ...]`


software ['is', 'web app', 'common', 'now']


software ['is', 'web app', "wasn't clear", 'it was possible']


software ['generate', 'web sites']


software ['worked', 'via web']


software ['is', 'web app']


software ['has', 'three main parts']


software ['is', 'online store builder']


Lisp ['has dialects', 'because']


Lisp ['rare', 'C++']


Lisp ['is', 'language']


Lisp ['has dialects', '']


Lisp ['has dialects', 'because one of the distinctive features of the language is that it has dialects']


Lisp ['was regarded as', 'language of AI']


Lisp ['defined by', 'writing an interpreter']


Lisp ['was meant to be', 'formal model of computation']


Interleaf ['added', 'scripting language']


Interleaf ['made software for', 'creating documents']


Interleaf ['was how I learned that', 'low end software tends to eat high end software']


Interleaf ['was', 'on the way down']


Interleaf ['on the way down', '1993']


RISD ['was', 'art school']


RISD ['counted me as', 'transfer sophomore']


RISD ['was', 'supposed to be the best art school in the country']


RISD ['was', 'the best art school in the country']


Robert ['wrote', 'shopping cart', 'written by', 'robert']


Robert ['wrote', 'shopping cart', 'written by', 'Robert']


Robert ['wrote', 'shopping cart']


Robert Morris ['offered', 'unsolicited advice']


Yorkville ['is', 'tiny corner']


Yorkville ["wasn't", 'rich']


online ['is not', 'publishing online']


online ['is not', 'publishing online', 'means', 'you treat the online version as the primary version']


web app ['common', 'now']


web app ["wasn't clear", 'it was possible']


editor ['written by', 'author']


shopping cart ['written by', 'Robert', 'wrote', 'shopping cart']


shopping cart ['written by', 'Robert']


shopping cart ['written by', 'robert', 'wrote', 'shopping cart']


shopping cart ['written by', 'robert']


Robert ['wrote', 'shopping cart', 'written by', 'Robert']


Robert ['wrote', 'shopping cart', 'written by', 'robert']


Robert ['wrote', 'shopping cart']


Lisp ['defined by', 'writing an interpreter']


Lisp ['has dialects', 'because']


Lisp ['was meant to be', 'formal model of computation']


Lisp ['rare', 'C++']


Lisp ['is', 'language']


Lisp ['has dialects', '']


Lisp ['has dialects', 'because one of the distinctive features of the language is that it has dialects']


Lisp ['was regarded as', 'language of AI']


Y Combinator ['would have said', 'Stop being so stressed out']


Y Combinator ['helps', 'founders']


Y Combinator ['is', 'investment firm']


company ['reaches breakeven', 'when yahoo buys it']


company ['gave', 'business advice']


company ['reaches breakeven', 'when Yahoo buys it']


software ['worked', 'via web']


software ['is', 'web app', "wasn't clear", 'it was possible']


software ['generate', 'web sites']


software ['has', 'three main parts']


software ['is', 'online store builder']


software ['is', 'web app']


software ['is', 'web app', 'common', 'now']


Y Combinator ['would have said', 'Stop being so stressed out']


Y Combinator ['is', 'investment firm']


Y Combinator ['helps', 'founders']


company ['gave', 'business advice']


company ['reaches breakeven', 'when Yahoo buys it']


company ['reaches breakeven', 'when yahoo buys it']


INFO:llama_index.token_counter.token_counter:> [get_response] Total LLM token usage: 5916 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total embedding token usage: 0 tokens

```


```


display(Markdown(f"<b>{response}</b>"))


```

**Interleaf was a software company that made software for creating documents. Their software was inspired by Emacs, and included a scripting language that was a dialect of Lisp. The company was started in the 1990s, and eventually went out of business.**

```


response = query_engine.query(




"Tell me more about what the author worked on at Interleaf"



```


```

INFO:llama_index.indices.knowledge_graph.retrievers:> Starting query: Tell me more about what the author worked on at Interleaf


INFO:llama_index.indices.knowledge_graph.retrievers:> Query keywords: ['Interleaf', 'author', 'work']


ERROR:llama_index.indices.knowledge_graph.retrievers:Index was not constructed with embeddings, skipping embedding usage...


INFO:llama_index.indices.knowledge_graph.retrievers:> Querying with idx: 6aa6a716-7390-4783-955b-8169fab25bb1: worth trying.



Our teacher, professor Ulivi, was a nice guy. He could see I w...


INFO:llama_index.indices.knowledge_graph.retrievers:> Querying with idx: 79f2a1b4-80bb-416f-a259-ebfc3136b2fe: on a map of New York City: if you zoom in on the Upper East Side, there's a t...


INFO:llama_index.indices.knowledge_graph.retrievers:> Querying with idx: 1e707b8c-b62a-4c1a-a908-c79e77b9692b: buyers pay a lot for such work. [6]



There were plenty of earnest students to...


INFO:llama_index.indices.knowledge_graph.retrievers:> Querying with idx: 31c2f53c-928a-4ed0-88fc-df92dba47c33: for example, that the reason the color changes suddenly at a certain point is...


INFO:llama_index.indices.knowledge_graph.retrievers:> Querying with idx: b1f5a610-9e0a-4e3e-ba96-514ae7d63a84: closures stored in a hash table on the server.



It helped to have studied art...


INFO:llama_index.indices.knowledge_graph.retrievers:> Querying with idx: 6cda9196-dcdb-4441-8f27-ff3f18779c4c: so easy. And that implies that HN was a mistake. Surely the biggest source of...


INFO:llama_index.indices.knowledge_graph.retrievers:> Querying with idx: a467cf4c-19cf-490f-92ad-ce03c8d91231: I've noticed in my life is how well it has worked, for me at least, to work o...


INFO:llama_index.indices.knowledge_graph.retrievers:> Extracted relationships: The following are knowledge triplets in max depth 2 in the form of `subject [predicate, object, predicate_next_hop, object_next_hop ...]`


software ['is', 'web app', 'common', 'now']


software ['is', 'web app', "wasn't clear", 'it was possible']


software ['generate', 'web sites']


software ['worked', 'via web']


software ['is', 'web app']


software ['has', 'three main parts']


software ['is', 'online store builder']


Lisp ['has dialects', 'because']


Lisp ['rare', 'C++']


Lisp ['is', 'language']


Lisp ['has dialects', '']


Lisp ['has dialects', 'because one of the distinctive features of the language is that it has dialects']


Lisp ['was regarded as', 'language of AI']


Lisp ['defined by', 'writing an interpreter']


Lisp ['was meant to be', 'formal model of computation']


Interleaf ['added', 'scripting language']


Interleaf ['made software for', 'creating documents']


Interleaf ['was how I learned that', 'low end software tends to eat high end software']


Interleaf ['was', 'on the way down']


Interleaf ['on the way down', '1993']


RISD ['was', 'art school']


RISD ['counted me as', 'transfer sophomore']


RISD ['was', 'supposed to be the best art school in the country']


RISD ['was', 'the best art school in the country']


Robert ['wrote', 'shopping cart', 'written by', 'robert']


Robert ['wrote', 'shopping cart', 'written by', 'Robert']


Robert ['wrote', 'shopping cart']


Robert Morris ['offered', 'unsolicited advice']


Yorkville ['is', 'tiny corner']


Yorkville ["wasn't", 'rich']


shopping cart ['written by', 'Robert', 'wrote', 'shopping cart']


shopping cart ['written by', 'robert', 'wrote', 'shopping cart']


shopping cart ['written by', 'Robert']


shopping cart ['written by', 'robert']


online ['is not', 'publishing online', 'means', 'you treat the online version as the primary version']


online ['is not', 'publishing online']


software ['has', 'three main parts']


software ['generate', 'web sites']


software ['is', 'web app', 'common', 'now']


software ['is', 'online store builder']


software ['is', 'web app']


software ['is', 'web app', "wasn't clear", 'it was possible']


software ['worked', 'via web']


editor ['written by', 'author']


YC ['is', 'work', 'is unprestigious', '']


YC ['grew', 'more exciting']


YC ['founded in', 'Berkeley']


YC ['founded in', '2005']


YC ['founded in', '1982']


YC ['is', 'full-time job']


YC ['is', 'engaging work']


YC ['is', 'batch model']


YC ['is', 'Summer Founders Program']


YC ['was', 'coffee shop']


YC ['invests in', 'startups']


YC ['is', 'fund']


YC ['started to notice', 'other advantages']


YC ['grew', 'quickly']


YC ['controlled by', 'founders']


YC ['is', 'work']


YC ['became', 'full-time job']


YC ['is self-funded', 'by Heroku']


YC ['is', 'hard work']


YC ['funds', 'startups']


YC ['controlled by', 'LLC']


Robert ['wrote', 'shopping cart']


Robert ['wrote', 'shopping cart', 'written by', 'Robert']


Robert ['wrote', 'shopping cart', 'written by', 'robert']


Lisp ['was meant to be', 'formal model of computation']


Lisp ['defined by', 'writing an interpreter']


Lisp ['was regarded as', 'language of AI']


Lisp ['has dialects', 'because']


Lisp ['has dialects', '']


Lisp ['has dialects', 'because one of the distinctive features of the language is that it has dialects']


Lisp ['rare', 'C++']


Lisp ['is', 'language']


party ['was', 'clever idea']


Y Combinator ['would have said', 'Stop being so stressed out']


Y Combinator ['is', 'investment firm']


Y Combinator ['helps', 'founders']


Robert Morris ['offered', 'unsolicited advice']


work ['is unprestigious', '']


Jessica Livingston ['is', 'woman']


Jessica Livingston ['decided', 'compile book']


HN ['edge case', 'bizarre']


HN ['edge case', 'when you both write essays and run a forum']


INFO:llama_index.token_counter.token_counter:> [get_response] Total LLM token usage: 4651 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total embedding token usage: 0 tokens

```


```


display(Markdown(f"<b>{response}</b>"))


```

The author worked on a software that allowed users to create documents, which was inspired by Emacs. The software had a scripting language that was a dialect of Lisp, and the author was responsible for writing things in this language.
**The author also worked on a software that allowed users to generate web sites. This software was a web app and was written in a dialect of Lisp. The author was also responsible for writing things in this language.**
## Visualizing the Graph RAG
[Section titled “Visualizing the Graph RAG”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/nebulagraphkgindexdemo/#visualizing-the-graph-rag)
If we visualize the Graph based RAG, starting from the term `['Interleaf', 'history', 'Software', 'Company'] `, we could see how those connected context looks like, and it’s a different form of Info./Knowledge:
  * Refined and Concise Form
  * Fine-grained Segmentation
  * Interconnected-sturcutred nature



```


%pip install ipython-ngql networkx pyvis




%load_ext ngql


```


```


%ngql --address 127.0.0.1 --port 9669--user root --password password


```


```

Connection Pool Created


INFO:nebula3.logger:Get connection to ('127.0.0.1', 9669)


Get connection to ('127.0.0.1', 9669)

```


```

.dataframe tbody tr th {



vertical-align: top;





.dataframe thead th {



text-align: right;



```
  
| Name  |  
| --- |  
| 0  | Apple_Vision_Pro  |  
| 1  | basketballplayer  |  
| 2  | demo_ai_ops  |  
| 3  | demo_basketballplayer  |  
| 4  | demo_data_lineage  |  
| 5  | demo_fifa_2022  |  
| 6  | demo_fraud_detection  |  
| 7  | demo_identity_resolution  |  
| 8  | demo_movie_recommendation  |  
| 9  | demo_sns  |  
| 10  | guardians  |  
| 11  | k8s  |  
| 12  | langchain  |  
| 13  | llamaindex  |  
| 14  | paul_graham_essay  |  
| 15  | squid_game  |  
| 16  | test  |  

```


%%ngql




USE paul_graham_essay;




MATCH p=(n)-[*1..2]-()




WHEREid(n) IN ['Interleaf', 'history', 'Software', 'Company']




RETURNLIMIT100;


```


```

INFO:nebula3.logger:Get connection to ('127.0.0.1', 9669)


Get connection to ('127.0.0.1', 9669)

```


```

.dataframe tbody tr th {



vertical-align: top;





.dataframe thead th {



text-align: right;



```
  
| 0  | ("Interleaf" :entity{name: "Interleaf"})-[:rel...  |  
| --- | --- |  
| 1  | ("Interleaf" :entity{name: "Interleaf"})-[:rel...  |  
| 2  | ("Interleaf" :entity{name: "Interleaf"})-[:rel...  |  
| 3  | ("Interleaf" :entity{name: "Interleaf"})-[:rel...  |  

```


%ng_draw


```


```

nebulagraph_draw.html

```

#### Query with embeddings
[Section titled “Query with embeddings”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/nebulagraphkgindexdemo/#query-with-embeddings)

```


# NOTE: can take a while!





index = KnowledgeGraphIndex.from_documents(




documents,




storage_context=storage_context,




max_triplets_per_chunk=2,




space_name=space_name,




edge_types=edge_types,




rel_prop_names=rel_prop_names,




tags=tags,




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


display(Markdown(f"<b>{response}</b>"))


```

#### Query with more global(cross node) context
[Section titled “Query with more global(cross node) context”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/nebulagraphkgindexdemo/#query-with-more-globalcross-node-context)

```


query_engine = index.as_query_engine(




include_text=True,




response_mode="tree_summarize",




embedding_mode="hybrid",




similarity_top_k=5,




explore_global_knowledge=True,






response = query_engine.query("Tell me more about what the author and Lisp")


```

#### Visualizing the Graph
[Section titled “Visualizing the Graph”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/nebulagraphkgindexdemo/#visualizing-the-graph)

```

## create graph



from pyvis.network import Network





g = index.get_networkx_graph()




net = Network(notebook=True, cdn_resources="in_line", directed=True)



net.from_nx(g)



net.show("example.html")


```

#### [Optional] Try building the graph and manually add triplets!
[Section titled “[Optional] Try building the graph and manually add triplets!”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/nebulagraphkgindexdemo/#optional-try-building-the-graph-and-manually-add-triplets)

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

# not yet implemented



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


str(response)


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


