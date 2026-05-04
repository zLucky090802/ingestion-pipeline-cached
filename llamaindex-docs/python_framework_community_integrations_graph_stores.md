[Skip to content](https://developers.llamaindex.ai/python/framework/community/integrations/graph_stores/#_top)
LlamaIndex Framework
Open Source Community
Integrations
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Using Graph Stores
## `Neo4jGraphStore`
[Section titled “Neo4jGraphStore”](https://developers.llamaindex.ai/python/framework/community/integrations/graph_stores/#neo4jgraphstore)
`Neo4j` is supported as a graph store integration. You can persist, visualize, and query graphs using LlamaIndex and Neo4j. Furthermore, existing Neo4j graphs are directly supported using `text2cypher` and the `KnowledgeGraphQueryEngine`.
If you’ve never used Neo4j before, you can download the desktop client [here](https://neo4j.com/download/).
Once you open the client, create a new project and install the `apoc` integration. Full instructions [here](https://neo4j.com/labs/apoc/4.1/installation/). Just click on your project, select `Plugins` on the left side menu, install APOC and restart your server.
See the example of using the [Neo4j Graph Store](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neo4jkgindexdemo).
## `NebulaGraphStore`
[Section titled “NebulaGraphStore”](https://developers.llamaindex.ai/python/framework/community/integrations/graph_stores/#nebulagraphstore)
We support a `NebulaGraphStore` integration, for persisting graphs directly in Nebula! Furthermore, you can generate cypher queries and return natural language responses for your Nebula graphs using the `KnowledgeGraphQueryEngine`.
See the associated guides below:
  * [Knowledge Graph Query Engine](https://developers.llamaindex.ai/python/examples/query_engine/knowledge_graph_query_engine)


## `FalkorDBGraphStore`
[Section titled “FalkorDBGraphStore”](https://developers.llamaindex.ai/python/framework/community/integrations/graph_stores/#falkordbgraphstore)
We support a `FalkorDBGraphStore` integration, for persisting graphs directly in FalkorDB! Furthermore, you can generate cypher queries and return natural language responses for your FalkorDB graphs using the `KnowledgeGraphQueryEngine`.
See the associated guides below:
  * [FalkorDB Graph Store](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/falkordbgraphdemo)


## `Amazon Neptune Graph Stores`
[Section titled “Amazon Neptune Graph Stores”](https://developers.llamaindex.ai/python/framework/community/integrations/graph_stores/#amazon-neptune-graph-stores)
We support `Amazon Neptune` integrations for both [Neptune Database](https://docs.aws.amazon.com/neptune/latest/userguide/feature-overview.html) and [Neptune Analytics](https://docs.aws.amazon.com/neptune-analytics/latest/userguide/what-is-neptune-analytics.html) as a graph store integration.
See the associated guides below:
  * [Amazon Neptune Graph Store](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/neptunedatabasekgindexdemo).


## `TiDB Graph Store`
[Section titled “TiDB Graph Store”](https://developers.llamaindex.ai/python/framework/community/integrations/graph_stores/#tidb-graph-store)
We support a `TiDBGraphStore` integration, for persisting graphs directly in [TiDB](https://docs.pingcap.com/tidb/stable/overview)!
See the associated guides below:


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


