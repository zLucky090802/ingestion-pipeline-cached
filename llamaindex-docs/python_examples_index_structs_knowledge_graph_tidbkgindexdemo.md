[Skip to content](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/tidbkgindexdemo/#_top)
# TiDB Graph Store 

```


%pip install llama-index-llms-openai




%pip install llama-index-graph-stores-tidb




%pip install llama-index-embeddings-openai




%pip install llama-index-llms-azure-openai


```


```

# For OpenAI




import os





os.environ["OPENAI_API_KEY"] ="sk-xxxxxxx"





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




import openai




from llama_index.llms.azure_openai import AzureOpenAI




from llama_index.embeddings.openai import OpenAIEmbedding





import logging




import sys




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

## Using Knowledge Graph with TiDB
[Section titled “Using Knowledge Graph with TiDB”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/tidbkgindexdemo/#using-knowledge-graph-with-tidb)
### Prepare a TiDB cluster
[Section titled “Prepare a TiDB cluster”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/tidbkgindexdemo/#prepare-a-tidb-cluster)
  * [TiDB Cloud](https://tidb.cloud/) [Recommended], a fully managed TiDB service that frees you from the complexity of database operations.
  * [TiUP](https://docs.pingcap.com/tidb/stable/tiup-overview), use `tiup playground“ to create a local TiDB cluster for testing.


#### Get TiDB connection string
[Section titled “Get TiDB connection string”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/tidbkgindexdemo/#get-tidb-connection-string)
For example: `mysql+pymysql://user:password@host:4000/dbname`, in TiDBGraphStore we use pymysql as the db driver, so the connection string should be `mysql+pymysql://...`.
If you are using a TiDB Cloud serverless cluster with public endpoint, it requires TLS connection, so the connection string should be like `mysql+pymysql://user:password@host:4000/dbname?ssl_verify_cert=true&ssl_verify_identity=true`.
Replace `user`, `password`, `host`, `dbname` with your own values.
### Initialize TiDBGraphStore
[Section titled “Initialize TiDBGraphStore”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/tidbkgindexdemo/#initialize-tidbgraphstore)

```


from llama_index.graph_stores.tidb import TiDBGraphStore





graph_store = TiDBGraphStore(




db_connection_string="mysql+pymysql://user:password@host:4000/dbname"



```

### Instantiate TiDB KG Indexes
[Section titled “Instantiate TiDB KG Indexes”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/tidbkgindexdemo/#instantiate-tidb-kg-indexes)

```


from llama_index.core import (




KnowledgeGraphIndex,




SimpleDirectoryReader,




StorageContext,






documents = SimpleDirectoryReader(




"../../../examples/data/paul_graham/"



).load_data()

```


```


storage_context = StorageContext.from_defaults(graph_store=graph_store)





# NOTE: can take a while!




index = KnowledgeGraphIndex.from_documents(




documents=documents,




storage_context=storage_context,




max_triplets_per_chunk=2,



```

#### Querying the Knowledge Graph
[Section titled “Querying the Knowledge Graph”](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/tidbkgindexdemo/#querying-the-knowledge-graph)

```


query_engine = index.as_query_engine(




include_text=False, response_mode="tree_summarize"





response = query_engine.query(




"Tell me more about Interleaf",



```


```

INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"


WARNING:llama_index.core.indices.knowledge_graph.retrievers:Index was not constructed with embeddings, skipping embedding usage...


INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"

```


```


from IPython.display import Markdown, display





display(Markdown(f"<b>{response}</b>"))


```

**Interleaf was a software company that developed a scripting language and was known for its software products. It was inspired by Emacs and faced challenges due to Moore’s law. Over time, Interleaf’s prominence declined.**
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


