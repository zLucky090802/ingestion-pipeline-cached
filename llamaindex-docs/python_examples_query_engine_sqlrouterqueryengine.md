[Skip to content](https://developers.llamaindex.ai/python/examples/query_engine/sqlrouterqueryengine/#_top)
# SQL Router Query Engine 
In this tutorial, we define a custom router query engine that can route to either a SQL database or a vector database.
**NOTE:** Any Text-to-SQL application should be aware that executing arbitrary SQL queries can be a security risk. It is recommended to take precautions as needed, such as using restricted roles, read-only databases, sandboxing, etc.
### Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/examples/query_engine/sqlrouterqueryengine/#setup)
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-readers-wikipedia


```


```


!pip install llama-index


```


```


# NOTE: This is ONLY necessary in jupyter notebook.



# Details: Jupyter runs an event-loop behind the scenes.


#          This results in nested event-loops when we start an event-loop to make async queries.


#          This is normally not allowed, we use nest_asyncio to allow it for convenience.



import nest_asyncio




nest_asyncio.apply()

```


```


import logging




import sys





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))





from llama_index.core import VectorStoreIndex, SQLDatabase




from llama_index.readers.wikipedia import WikipediaReader


```


```

INFO:numexpr.utils:Note: NumExpr detected 12 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8.


Note: NumExpr detected 12 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8.


INFO:numexpr.utils:NumExpr defaulting to 8 threads.


NumExpr defaulting to 8 threads.




/Users/jerryliu/Programming/gpt_index/.venv/lib/python3.10/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html



from .autonotebook import tqdm as notebook_tqdm


```

### Create Database Schema + Test Data
[Section titled “Create Database Schema + Test Data”](https://developers.llamaindex.ai/python/examples/query_engine/sqlrouterqueryengine/#create-database-schema--test-data)
Here we introduce a toy scenario where there are 100 tables (too big to fit into the prompt)

```


from sqlalchemy import (




create_engine,




MetaData,




Table,




Column,




String,




Integer,




select,




column,



```


```


engine = create_engine("sqlite:///:memory:", future=True)




metadata_obj = MetaData()


```


```

# create city SQL table



table_name ="city_stats"




city_stats_table = Table(




table_name,




metadata_obj,




Column("city_name", String(16), primary_key=True),




Column("population", Integer),




Column("country", String(16), nullable=False),





metadata_obj.create_all(engine)

```


```

# print tables


metadata_obj.tables.keys()

```


```

dict_keys(['city_stats'])

```

We introduce some test data into the `city_stats` table

```


from sqlalchemy import insert





rows = [




{"city_name": "Toronto", "population": 2930000, "country": "Canada"},




{"city_name": "Tokyo", "population": 13960000, "country": "Japan"},




{"city_name": "Berlin", "population": 3645000, "country": "Germany"},





for row in rows:




stmt = insert(city_stats_table).values(**row)




with engine.begin() as connection:




cursor = connection.execute(stmt)


```


```


with engine.connect() as connection:




cursor = connection.exec_driver_sql("SELECT * FROM city_stats")




print(cursor.fetchall())


```


```

[('Toronto', 2930000, 'Canada'), ('Tokyo', 13960000, 'Japan'), ('Berlin', 3645000, 'Germany')]

```

### Load Data
[Section titled “Load Data”](https://developers.llamaindex.ai/python/examples/query_engine/sqlrouterqueryengine/#load-data)
We first show how to convert a Document into a set of Nodes, and insert into a DocumentStore.

```

# install wikipedia python package



!pip install wikipedia


```


```

Requirement already satisfied: wikipedia in /Users/jerryliu/Programming/gpt_index/.venv/lib/python3.10/site-packages (1.4.0)


Requirement already satisfied: requests<3.0.0,>=2.0.0 in /Users/jerryliu/Programming/gpt_index/.venv/lib/python3.10/site-packages (from wikipedia) (2.28.2)


Requirement already satisfied: beautifulsoup4 in /Users/jerryliu/Programming/gpt_index/.venv/lib/python3.10/site-packages (from wikipedia) (4.12.2)


Requirement already satisfied: idna<4,>=2.5 in /Users/jerryliu/Programming/gpt_index/.venv/lib/python3.10/site-packages (from requests<3.0.0,>=2.0.0->wikipedia) (3.4)


Requirement already satisfied: charset-normalizer<4,>=2 in /Users/jerryliu/Programming/gpt_index/.venv/lib/python3.10/site-packages (from requests<3.0.0,>=2.0.0->wikipedia) (3.1.0)


Requirement already satisfied: certifi>=2017.4.17 in /Users/jerryliu/Programming/gpt_index/.venv/lib/python3.10/site-packages (from requests<3.0.0,>=2.0.0->wikipedia) (2022.12.7)


Requirement already satisfied: urllib3<1.27,>=1.21.1 in /Users/jerryliu/Programming/gpt_index/.venv/lib/python3.10/site-packages (from requests<3.0.0,>=2.0.0->wikipedia) (1.26.15)


Requirement already satisfied: soupsieve>1.2 in /Users/jerryliu/Programming/gpt_index/.venv/lib/python3.10/site-packages (from beautifulsoup4->wikipedia) (2.4.1)



[1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip available: [0m[31;49m22.3.1[0m[39;49m -> [0m[32;49m23.1.2[0m


[1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m

```


```


cities = ["Toronto", "Berlin", "Tokyo"]




wiki_docs = WikipediaReader().load_data(pages=cities)


```

### Build SQL Index
[Section titled “Build SQL Index”](https://developers.llamaindex.ai/python/examples/query_engine/sqlrouterqueryengine/#build-sql-index)

```


sql_database = SQLDatabase(engine, include_tables=["city_stats"])


```


```


from llama_index.core.query_engine import NLSQLTableQueryEngine


```


```


sql_query_engine = NLSQLTableQueryEngine(




sql_database=sql_database,




tables=["city_stats"],



```


```

INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total LLM token usage: 0 tokens


> [build_index_from_nodes] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total embedding token usage: 0 tokens


> [build_index_from_nodes] Total embedding token usage: 0 tokens




/Users/jerryliu/Programming/gpt_index/.venv/lib/python3.10/site-packages/langchain/sql_database.py:227: UserWarning: This method is deprecated - please use `get_usable_table_names`.



warnings.warn(


```

### Build Vector Index
[Section titled “Build Vector Index”](https://developers.llamaindex.ai/python/examples/query_engine/sqlrouterqueryengine/#build-vector-index)

```

# build a separate vector index per city


# You could also choose to define a single vector index across all docs, and annotate each chunk by metadata



vector_indices = []




for wiki_doc in wiki_docs:




vector_index = VectorStoreIndex.from_documents([wiki_doc])




vector_indices.append(vector_index)


```


```

INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total LLM token usage: 0 tokens


> [build_index_from_nodes] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total embedding token usage: 20744 tokens


> [build_index_from_nodes] Total embedding token usage: 20744 tokens


INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total LLM token usage: 0 tokens


> [build_index_from_nodes] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total embedding token usage: 21947 tokens


> [build_index_from_nodes] Total embedding token usage: 21947 tokens


INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total LLM token usage: 0 tokens


> [build_index_from_nodes] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total embedding token usage: 12786 tokens


> [build_index_from_nodes] Total embedding token usage: 12786 tokens

```

### Define Query Engines, Set as Tools
[Section titled “Define Query Engines, Set as Tools”](https://developers.llamaindex.ai/python/examples/query_engine/sqlrouterqueryengine/#define-query-engines-set-as-tools)

```


vector_query_engines = [index.as_query_engine() for index in vector_indices]


```


```


from llama_index.core.tools import QueryEngineTool






sql_tool = QueryEngineTool.from_defaults(




query_engine=sql_query_engine,




description=(




"Useful for translating a natural language query into a SQL query over"




" a table containing: city_stats, containing the population/country of"




" each city"






vector_tools = []




for city, query_engine inzip(cities, vector_query_engines):




vector_tool = QueryEngineTool.from_defaults(




query_engine=query_engine,




description=f"Useful for answering semantic questions about {city}",





vector_tools.append(vector_tool)


```

### Define Router Query Engine
[Section titled “Define Router Query Engine”](https://developers.llamaindex.ai/python/examples/query_engine/sqlrouterqueryengine/#define-router-query-engine)

```


from llama_index.core.query_engine import RouterQueryEngine




from llama_index.core.selectors import LLMSingleSelector





query_engine = RouterQueryEngine(




selector=LLMSingleSelector.from_defaults(),




query_engine_tools=([sql_tool] + vector_tools),



```


```


response = query_engine.query("Which city has the highest population?")




print(str(response))


```


```

INFO:llama_index.query_engine.router_query_engine:Selecting query engine 0: Useful for translating a natural language query into a SQL query over a table containing: city_stats, containing the population/country of each city.


Selecting query engine 0: Useful for translating a natural language query into a SQL query over a table containing: city_stats, containing the population/country of each city.


INFO:llama_index.indices.struct_store.sql_query:> Table desc str: Schema of table city_stats:


Table 'city_stats' has columns: city_name (VARCHAR(16)), population (INTEGER), country (VARCHAR(16)) and foreign keys: .



> Table desc str: Schema of table city_stats:


Table 'city_stats' has columns: city_name (VARCHAR(16)), population (INTEGER), country (VARCHAR(16)) and foreign keys: .



INFO:llama_index.token_counter.token_counter:> [query] Total LLM token usage: 347 tokens


> [query] Total LLM token usage: 347 tokens


INFO:llama_index.token_counter.token_counter:> [query] Total embedding token usage: 0 tokens


> [query] Total embedding token usage: 0 tokens



Tokyo has the highest population, with 13,960,000 people.


```


```


response = query_engine.query("Tell me about the historical museums in Berlin")




print(str(response))


```


```

INFO:llama_index.query_engine.router_query_engine:Selecting query engine 2: Useful for answering semantic questions about Berlin.


Selecting query engine 2: Useful for answering semantic questions about Berlin.


INFO:llama_index.token_counter.token_counter:> [retrieve] Total LLM token usage: 0 tokens


> [retrieve] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [retrieve] Total embedding token usage: 8 tokens


> [retrieve] Total embedding token usage: 8 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total LLM token usage: 2031 tokens


> [get_response] Total LLM token usage: 2031 tokens


INFO:llama_index.token_counter.token_counter:> [get_response] Total embedding token usage: 0 tokens


> [get_response] Total embedding token usage: 0 tokens



Berlin is home to many historical museums, including the Altes Museum, Neues Museum, Alte Nationalgalerie, Pergamon Museum, and Bode Museum, which are all located on Museum Island. The Gemäldegalerie (Painting Gallery) focuses on the paintings of the "old masters" from the 13th to the 18th centuries, while the Neue Nationalgalerie (New National Gallery, built by Ludwig Mies van der Rohe) specializes in 20th-century European painting. The Hamburger Bahnhof, in Moabit, exhibits a major collection of modern and contemporary art. The expanded Deutsches Historisches Museum reopened in the Zeughaus with an overview of German history spanning more than a millennium. The Bauhaus Archive is a museum of 20th-century design from the famous Bauhaus school. Museum Berggruen houses the collection of noted 20th century collector Heinz Berggruen, and features an extensive assortment of works by Picasso, Matisse, Cézanne, and Giacometti, among others. The Kupferstichkabinett Berlin (Museum of Prints and Drawings) is part of the Staatlichen Museen z

```


```


response = query_engine.query("Which countries are each city from?")




print(str(response))


```


```

INFO:llama_index.query_engine.router_query_engine:Selecting query engine 0: Useful for translating a natural language query into a SQL query over a table containing: city_stats, containing the population/country of each city.


Selecting query engine 0: Useful for translating a natural language query into a SQL query over a table containing: city_stats, containing the population/country of each city.


INFO:llama_index.indices.struct_store.sql_query:> Table desc str: Schema of table city_stats:


Table 'city_stats' has columns: city_name (VARCHAR(16)), population (INTEGER), country (VARCHAR(16)) and foreign keys: .



> Table desc str: Schema of table city_stats:


Table 'city_stats' has columns: city_name (VARCHAR(16)), population (INTEGER), country (VARCHAR(16)) and foreign keys: .



INFO:llama_index.token_counter.token_counter:> [query] Total LLM token usage: 334 tokens


> [query] Total LLM token usage: 334 tokens


INFO:llama_index.token_counter.token_counter:> [query] Total embedding token usage: 0 tokens


> [query] Total embedding token usage: 0 tokens



Toronto is from Canada, Tokyo is from Japan, and Berlin is from Germany.


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


