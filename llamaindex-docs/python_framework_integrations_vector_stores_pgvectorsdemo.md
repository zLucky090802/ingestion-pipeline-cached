[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/pgvectorsdemo/#_top)
LlamaIndex Framework
Integrations
Vector stores
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# pgvecto.rs 
Firstly, you will probably need to install dependencies :

```


%pip install llama-index-vector-stores-pgvecto-rs


```


```


%pip install llama-index "pgvecto_rs[sdk]"


```

Then start the pgvecto.rs server as the [official document suggests](https://github.com/tensorchord/pgvecto.rs#installation):

```


!docker run --name pgvecto-rs-demo -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432-d tensorchord/pgvecto-rs:latest


```

Setup the logger.

```


import logging




import os




import sys





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


```

#### Creating a pgvecto_rs client
[Section titled “Creating a pgvecto_rs client”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/pgvectorsdemo/#creating-a-pgvecto_rs-client)

```


from pgvecto_rs.sdk import PGVectoRs





URL="postgresql+psycopg://{username}:{password}@{host}:{port}/{db_name}".format(




port=os.getenv("DB_PORT", "5432"),




host=os.getenv("DB_HOST", "localhost"),




username=os.getenv("DB_USER", "postgres"),




password=os.getenv("DB_PASS", "mysecretpassword"),




db_name=os.getenv("DB_NAME", "postgres"),






client = PGVectoRs(




db_url=URL,




collection_name="example",




dimension=1536# Using OpenAI’s text-embedding-ada-002



```

#### Setup OpenAI
[Section titled “Setup OpenAI”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/pgvectorsdemo/#setup-openai)

```


import os





os.environ["OPENAI_API_KEY"] ="sk-..."


```

#### Load documents, build the PGVectoRsStore and VectorStoreIndex
[Section titled “Load documents, build the PGVectoRsStore and VectorStoreIndex”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/pgvectorsdemo/#load-documents-build-the-pgvectorsstore-and-vectorstoreindex)

```


from IPython.display import Markdown, display





from llama_index.core import SimpleDirectoryReader, VectorStoreIndex




from llama_index.vector_stores.pgvecto_rs import PGVectoRsStore


```

Download Data

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```


```

# load documents



documents = SimpleDirectoryReader("./data/paul_graham").load_data()


```


```

# initialize without metadata filter



from llama_index.core import StorageContext





vector_store = PGVectoRsStore(client=client)




storage_context = StorageContext.from_defaults(vector_store=vector_store)




index = VectorStoreIndex.from_documents(




documents, storage_context=storage_context



```

#### Query Index
[Section titled “Query Index”](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/pgvectorsdemo/#query-index)

```

# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine()




response = query_engine.query("What did the author do growing up?")


```


```

INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"


HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"


INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"


HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"

```


```


display(Markdown(f"<b>{response}</b>"))


```

**The author, growing up, worked on writing and programming. They wrote short stories and also tried writing programs on an IBM 1401 computer. They later got a microcomputer and started programming more extensively, writing simple games and a word processor.**
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


