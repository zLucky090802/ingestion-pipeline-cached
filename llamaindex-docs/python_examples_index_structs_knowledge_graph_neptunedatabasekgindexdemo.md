[Skip to content](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neptunedatabasekgindexdemo/#_top)
# Amazon Neptune Graph Store 

```


%pip install boto3




%pip install llama-index-llms-bedrock




%pip install llama-index-graph-stores-neptune




%pip install llama-index-embeddings-bedrock


```

## Using Knowledge Graph with NeptuneDatabaseGraphStore
[Section titled “Using Knowledge Graph with NeptuneDatabaseGraphStore”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neptunedatabasekgindexdemo/#using-knowledge-graph-with-neptunedatabasegraphstore)
### Add the required imports
[Section titled “Add the required imports”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neptunedatabasekgindexdemo/#add-the-required-imports)

```


from llama_index.llms.bedrock import Bedrock




from llama_index.embeddings.bedrock import BedrockEmbedding




from llama_index.core import (




StorageContext,




SimpleDirectoryReader,




KnowledgeGraphIndex,




Settings,





from llama_index.graph_stores.neptune import (




NeptuneAnalyticsGraphStore,




NeptuneDatabaseGraphStore,





from IPython.display import Markdown, display


```

### Configure the LLM to use, in this case Amazon Bedrock and Claude 2.1
[Section titled “Configure the LLM to use, in this case Amazon Bedrock and Claude 2.1”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neptunedatabasekgindexdemo/#configure-the-llm-to-use-in-this-case-amazon-bedrock-and-claude-21)

```


llm = Bedrock(model="anthropic.claude-v2")




embed_model = BedrockEmbedding(model="amazon.titan-embed-text-v1")





Settings.llm = llm




Settings.embed_model = embed_model




Settings.chunk_size =512


```

### Building the Knowledge Graph
[Section titled “Building the Knowledge Graph”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neptunedatabasekgindexdemo/#building-the-knowledge-graph)
### Read in the sample file
[Section titled “Read in the sample file”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neptunedatabasekgindexdemo/#read-in-the-sample-file)

```


documents = SimpleDirectoryReader(




"../../../../examples/paul_graham_essay/data"



).load_data()

```

### Instantiate Neptune KG Indexes
[Section titled “Instantiate Neptune KG Indexes”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neptunedatabasekgindexdemo/#instantiate-neptune-kg-indexes)
When using Amazon Neptune you can choose to use either Neptune Database or Neptune Analytics.
Neptune Database is a serverless graph database designed for optimal scalability and availability. It provides a solution for graph database workloads that need to scale to 100,000 queries per second, Multi-AZ high availability, and multi-Region deployments. You can use Neptune Database for social networking, fraud alerting, and Customer 360 applications.
Neptune Analytics is an analytics database engine that can quickly analyze large amounts of graph data in memory to get insights and find trends. Neptune Analytics is a solution for quickly analyzing existing graph databases or graph datasets stored in a data lake. It uses popular graph analytic algorithms and low-latency analytic queries.
#### Using Neptune Database
[Section titled “Using Neptune Database”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neptunedatabasekgindexdemo/#using-neptune-database)
If you can choose to use [Neptune Database](https://docs.aws.amazon.com/neptune/latest/userguide/feature-overview.html) to store your KG index you can create the graph store as shown below.

```


graph_store = NeptuneDatabaseGraphStore(




host="<GRAPH NAME>.<CLUSTER ID>.<REGION>.neptune.amazonaws.com", port=8182



```

#### Neptune Analytics
[Section titled “Neptune Analytics”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neptunedatabasekgindexdemo/#neptune-analytics)
If you can choose to use [Neptune Analytics](https://docs.aws.amazon.com/neptune-analytics/latest/userguide/what-is-neptune-analytics.html) to store your KG index you can create the graph store as shown below.

```


graph_store = NeptuneAnalyticsGraphStore(




graph_identifier="<INSERT GRAPH IDENIFIER>"



```


```


storage_context = StorageContext.from_defaults(graph_store=graph_store)





# NOTE: can take a while!




index = KnowledgeGraphIndex.from_documents(




documents,




storage_context=storage_context,




max_triplets_per_chunk=2,



```

#### Querying the Knowledge Graph
[Section titled “Querying the Knowledge Graph”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neptunedatabasekgindexdemo/#querying-the-knowledge-graph)
First, we can query and send only the triplets to the LLM.

```


query_engine = index.as_query_engine(




include_text=False, response_mode="tree_summarize"






response = query_engine.query("Tell me more about Interleaf")


```


```


display(Markdown(f"<b>{response}</b>"))


```

For more detailed answers, we can also send the text from where the retrieved tripets were extracted.

```


query_engine = index.as_query_engine(




include_text=True, response_mode="tree_summarize"





response = query_engine.query(




"Tell me more about what the author worked on at Interleaf"



```


```


display(Markdown(f"<b>{response}</b>"))


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


