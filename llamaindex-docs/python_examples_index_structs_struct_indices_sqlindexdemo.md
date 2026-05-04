[Skip to content](https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/sqlindexdemo/#_top)
# Text-to-SQL Guide (Query Engine + Retriever) 
This is a basic guide to LlamaIndex’s Text-to-SQL capabilities.
  1. We first show how to perform text-to-SQL over a toy dataset: this will do “retrieval” (sql query over db) and “synthesis”.
  2. We then show how to buid a TableIndex over the schema to dynamically retrieve relevant tables during query-time.
  3. Next, we show how to use query-time rows and columns retrievers to enhance Text-to-SQL context.
  4. We finally show you how to define a text-to-SQL retriever on its own.


**NOTE:** Any Text-to-SQL application should be aware that executing arbitrary SQL queries can be a security risk. It is recommended to take precautions as needed, such as using restricted roles, read-only databases, sandboxing, etc.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-core llama-index-llms-openai llama-index-embeddings-openai


```


```


import os




import openai


```


```


os.environ["OPENAI_API_KEY"] ="sk-.."


```


```

# import logging


# import sys



# logging.basicConfig(stream=sys.stdout, level=logging.INFO)


# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

```


```


from IPython.display import Markdown, display


```

### Create Database Schema
[Section titled “Create Database Schema”](https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/sqlindexdemo/#create-database-schema)
We use `sqlalchemy`, a popular SQL database toolkit, to create an empty `city_stats` Table

```


from sqlalchemy import (




create_engine,




MetaData,




Table,




Column,




String,




Integer,




select,



```


```


engine = create_engine("sqlite:///:memory:")




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

### Define SQL Database
[Section titled “Define SQL Database”](https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/sqlindexdemo/#define-sql-database)
We first define our `SQLDatabase` abstraction (a light wrapper around SQLAlchemy).

```


from llama_index.core import SQLDatabase




from llama_index.llms.openai import OpenAI


```


```


llm = OpenAI(temperature=0.1, model="gpt-4.1-mini")


```


```


sql_database = SQLDatabase(engine, include_tables=["city_stats"])


```

We add some testing data to our SQL database.

```


from sqlalchemy import insert





sql_database = SQLDatabase(engine, include_tables=["city_stats"])





rows = [




{"city_name": "Toronto", "population": 2930000, "country": "Canada"},




{"city_name": "Tokyo", "population": 13960000, "country": "Japan"},





"city_name": "Chicago",




"population": 2679000,




"country": "United States",






"city_name": "New York",




"population": 8258000,




"country": "United States",





{"city_name": "Seoul", "population": 9776000, "country": "South Korea"},




{"city_name": "Busan", "population": 3334000, "country": "South Korea"},





for row in rows:




stmt = insert(city_stats_table).values(**row)




with engine.begin() as connection:




cursor = connection.execute(stmt)


```


```

# view current table



stmt = select(




city_stats_table.c.city_name,




city_stats_table.c.population,




city_stats_table.c.country,



).select_from(city_stats_table)




with engine.connect() as connection:




results = connection.execute(stmt).fetchall()




print(results)


```


```

[('Toronto', 2930000, 'Canada'), ('Tokyo', 13960000, 'Japan'), ('Chicago', 2679000, 'United States'), ('New York', 8258000, 'United States'), ('Seoul', 9776000, 'South Korea'), ('Busan', 3334000, 'South Korea')]

```

### Query Index
[Section titled “Query Index”](https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/sqlindexdemo/#query-index)
We first show how we can execute a raw SQL query, which directly executes over the table.

```


from sqlalchemy import text





with engine.connect() as con:




rows = con.execute(text("SELECT city_name from city_stats"))




for row in rows:




print(row)


```


```

('Busan',)


('Chicago',)


('New York',)


('Seoul',)


('Tokyo',)


('Toronto',)

```

## Part 1: Text-to-SQL Query Engine
[Section titled “Part 1: Text-to-SQL Query Engine”](https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/sqlindexdemo/#part-1-text-to-sql-query-engine)
Once we have constructed our SQL database, we can use the NLSQLTableQueryEngine to construct natural language queries that are synthesized into SQL queries.
Note that we need to specify the tables we want to use with this query engine. If we don’t the query engine will pull all the schema context, which could overflow the context window of the LLM.

```


from llama_index.core.query_engine import NLSQLTableQueryEngine





query_engine = NLSQLTableQueryEngine(




sql_database=sql_database, tables=["city_stats"], llm=llm





query_str ="Which city has the highest population?"




response = query_engine.query(query_str)


```


```


display(Markdown(f"<b>{response}</b>"))


```

**Tokyo has the highest population among all cities, with a population of 13,960,000.**
This query engine should be used in any case where you can specify the tables you want to query over beforehand, or the total size of all the table schema plus the rest of the prompt fits your context window.
## Part 2: Query-Time Retrieval of Tables for Text-to-SQL
[Section titled “Part 2: Query-Time Retrieval of Tables for Text-to-SQL”](https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/sqlindexdemo/#part-2-query-time-retrieval-of-tables-for-text-to-sql)
If we don’t know ahead of time which table we would like to use, and the total size of the table schema overflows your context window size, we should store the table schema in an index so that during query time we can retrieve the right schema.
The way we can do this is using the SQLTableNodeMapping object, which takes in a SQLDatabase and produces a Node object for each SQLTableSchema object passed into the ObjectIndex constructor.

```


from llama_index.core.indices.struct_store.sql_query import (




SQLTableRetrieverQueryEngine,





from llama_index.core.objects import (




SQLTableNodeMapping,




ObjectIndex,




SQLTableSchema,





from llama_index.core import VectorStoreIndex




from llama_index.core.embeddings.openai import OpenAIEmbedding




# set Logging to DEBUG for more detailed outputs



table_node_mapping = SQLTableNodeMapping(sql_database)




table_schema_objs = [




(SQLTableSchema(table_name="city_stats"))




# add a SQLTableSchema for each table





obj_index = ObjectIndex.from_objects(




table_schema_objs,




table_node_mapping,




VectorStoreIndex,




embed_model=OpenAIEmbedding(model="text-embedding-3-small"),





query_engine = SQLTableRetrieverQueryEngine(




sql_database, obj_index.as_retriever(similarity_top_k=1)



```

Now we can take our SQLTableRetrieverQueryEngine and query it for our response.

```


response = query_engine.query("Which city has the highest population?")




display(Markdown(f"<b>{response}</b>"))


```

**Tokyo has the highest population among all cities, with a population of 13,960,000.**

```

# you can also fetch the raw result from SQLAlchemy!



response.metadata["result"]


```


```

[('Tokyo', 13960000)]

```

You can also add additional context information for each table schema you define.

```

# manually set context text



city_stats_text = (




"This table gives information regarding the population and country of a"




" given city.\nThe user will query with codewords, where 'foo' corresponds"




" to population and 'bar'corresponds to city."






table_node_mapping = SQLTableNodeMapping(sql_database)




table_schema_objs = [




(SQLTableSchema(table_name="city_stats", context_str=city_stats_text))



```

## Part 3: Query-Time Retrieval of Rows and Columns for Text-to-SQL
[Section titled “Part 3: Query-Time Retrieval of Rows and Columns for Text-to-SQL”](https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/sqlindexdemo/#part-3-query-time-retrieval-of-rows-and-columns-for-text-to-sql)
One challenge arises when asking a question like: “How many cities are in the US?” In such cases, the generated query might only look for cities where the country is listed as “US,” potentially missing entries labeled “United States.” To address this issue, you can apply query-time row retrieval, query-time column retrieval, or a combination of both.
### Query-Time Rows Retrieval
[Section titled “Query-Time Rows Retrieval”](https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/sqlindexdemo/#query-time-rows-retrieval)
In query-time rows retrieval, we embed the rows of each table, resulting in one index per table.

```


from llama_index.core.schema import TextNode





with engine.connect() as connection:




results = connection.execute(stmt).fetchall()





city_nodes = [TextNode(text=str(t)) forin results]





city_rows_index = VectorStoreIndex(




city_nodes, embed_model=OpenAIEmbedding(model="text-embedding-3-small")





city_rows_retriever = city_rows_index.as_retriever(similarity_top_k=1)





city_rows_retriever.retrieve("US")


```


```

[NodeWithScore(node=TextNode(id_='8ae10176-afd8-40ee-a97b-b24f66235489', embedding=None, metadata={}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text="('Chicago', 2679000, 'United States')", mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}'), score=0.7843469586763699)]

```

Then, the rows retriever of each table can be provided to the SQLTableRetrieverQueryEngine.

```


rows_retrievers = {




"city_stats": city_rows_retriever,





query_engine = SQLTableRetrieverQueryEngine(




sql_database,




obj_index.as_retriever(similarity_top_k=1),




rows_retrievers=rows_retrievers,



```

During querying, the row retrievers are used to identify the rows most semantically similar to the input query. These retrieved rows are then incorporated as context to enhance the performance of the text-to-SQL generation.

```


response = query_engine.query("How many cities are in the US?")


```


```


display(Markdown(f"<b>{response}</b>"))


```

**There are 2 cities in the United States according to the data in the city_stats table.**
### Query-Time Columns Retrieval
[Section titled “Query-Time Columns Retrieval”](https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/sqlindexdemo/#query-time-columns-retrieval)
While query-time row retrieval enhances text-to-SQL generation, it embeds each row individually, even when many rows share repeated values—such as those in categorical. This can lead to token inefficiency and unnecessary overhead. Moreover, in tables with a large number of columns, the retriever may surface only a subset of relevant values, potentially omitting others that are important for accurate query generation.
To address this issue, query-time column retrieval can be used. This approach indexes each distinct value within selected columns, creating a separate index for each column in the table.

```


city_cols_retrievers = {}





for column_name in ["city_name", "country"]:




stmt = select(city_stats_table.c[column_name]).distinct()




with engine.connect() as connection:




values = connection.execute(stmt).fetchall()




nodes = [TextNode(text=t[0]) forin values]





column_index = VectorStoreIndex(




nodes, embed_model=OpenAIEmbedding(model="text-embedding-3-small")





column_retriever = column_index.as_retriever(similarity_top_k=1)





city_cols_retrievers[column_name] = column_retriever


```

Then, columns retrievers of each table can be provided to the SQLTableRetrieverQueryEngine.

```


cols_retrievers = {




"city_stats": city_cols_retrievers,





query_engine = SQLTableRetrieverQueryEngine(




sql_database,




obj_index.as_retriever(similarity_top_k=1),




rows_retrievers=rows_retrievers,




cols_retrievers=cols_retrievers,




llm=llm,



```

During querying, the columns retrievers are used to identify the values of columns that are the most semantically similar to the input query. These retrieved values are then incorporated as context to enhance the performance of the text-to-SQL generation.

```


response = query_engine.query("How many cities are in the US?")


```


```


display(Markdown(f"<b>{response}</b>"))


```

**There are 2 cities in the United States.**
## Part 4: Text-to-SQL Retriever
[Section titled “Part 4: Text-to-SQL Retriever”](https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/sqlindexdemo/#part-4-text-to-sql-retriever)
So far our text-to-SQL capability is packaged in a query engine and consists of both retrieval and synthesis.
You can use the SQL retriever on its own. We show you some different parameters you can try, and also show how to plug it into our `RetrieverQueryEngine` to get roughly the same results.

```


from llama_index.core.retrievers import NLSQLRetriever




# default retrieval (return_raw=True)



nl_sql_retriever = NLSQLRetriever(




sql_database, tables=["city_stats"], llm=llm, return_raw=True



```


```


results = nl_sql_retriever.retrieve(




"Return the top 5 cities (along with their populations) with the highest population."



```


```


from llama_index.core.response.notebook_utils import display_source_node





forin results:




display_source_node(n)


```

**Node ID:** f640a54f-7413-4dc0-9135-cd63c7ca8f45**Similarity:** None**Text:** [(‘Tokyo’, 13960000), (‘Seoul’, 9776000), (‘New York’, 8258000), (‘Busan’, 3334000), (‘Toronto’, …

```

# default retrieval (return_raw=False)



nl_sql_retriever = NLSQLRetriever(




sql_database, tables=["city_stats"], return_raw=False



```


```


results = nl_sql_retriever.retrieve(




"Return the top 5 cities (along with their populations) with the highest population."



```


```


# NOTE: all the content is in the metadata




forin results:




display_source_node(n, show_source_metadata=True)


```

**Node ID:** 05c61a90-598e-4c29-a6b4-b27f2579819e**Similarity:** None**Text:** **Metadata:** {‘city_name’: ‘Tokyo’, ‘population’: 13960000}
**Node ID:** c7f5fc4c-9754-4946-92c6-54a0d2b40fd9**Similarity:** None**Text:** **Metadata:** {‘city_name’: ‘Seoul’, ‘population’: 9776000}
**Node ID:** 3a00e201-f3b5-430e-af0e-aa4c34a71131**Similarity:** None**Text:** **Metadata:** {‘city_name’: ‘New York’, ‘population’: 8258000}
**Node ID:** ee911f7f-8aae-4bad-a52d-c0bdfab63942**Similarity:** None**Text:** **Metadata:** {‘city_name’: ‘Busan’, ‘population’: 3334000}
**Node ID:** dca6b482-52e4-41e0-992f-a58109e6f3f6**Similarity:** None**Text:** **Metadata:** {‘city_name’: ‘Toronto’, ‘population’: 2930000}
### Plug into our `RetrieverQueryEngine`
[Section titled “Plug into our RetrieverQueryEngine”](https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/sqlindexdemo/#plug-into-our-retrieverqueryengine)
We compose our SQL Retriever with our standard `RetrieverQueryEngine` to synthesize a response. The result is roughly similar to our packaged `Text-to-SQL` query engines.

```


from llama_index.core.query_engine import RetrieverQueryEngine





query_engine = RetrieverQueryEngine.from_args(nl_sql_retriever, llm=llm)


```


```


response = query_engine.query(




"Return the top 5 cities (along with their populations) with the highest population."



```


```


print(str(response))


```


```

The top 5 cities with the highest populations are:



1. Tokyo - 13,960,000


2. Seoul - 9,776,000


3. New York - 8,258,000


4. Busan - 3,334,000


5. Toronto - 2,930,000

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


