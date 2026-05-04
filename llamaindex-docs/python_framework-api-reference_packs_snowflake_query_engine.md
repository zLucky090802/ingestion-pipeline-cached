# Snowflake query engine
##  SnowflakeQueryEnginePack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/snowflake_query_engine/#llama_index.packs.snowflake_query_engine.SnowflakeQueryEnginePack "Permanent link")
Bases: 
Snowflake query engine pack. It uses snowflake-sqlalchemy to connect to Snowflake, then calls NLSQLTableQueryEngine to query data.
Source code in `llama-index-packs/llama-index-packs-snowflake-query-engine/llama_index/packs/snowflake_query_engine/base.py`  
| 
```
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
```
 | 
```
classSnowflakeQueryEnginePack(BaseLlamaPack):
"""
    Snowflake query engine pack.
    It uses snowflake-sqlalchemy to connect to Snowflake, then calls
    NLSQLTableQueryEngine to query data.
    """

    def__init__(
        self,
        user: str,
        password: str,
        account: str,
        database: str,
        schema: str,
        warehouse: str,
        role: str,
        tables: List[str],
        **kwargs: Any,
    ) -> None:
"""Init params."""
        # workaround for https://github.com/snowflakedb/snowflake-sqlalchemy/issues/380.
        try:
            snowflake_sqlalchemy_20_monkey_patches()
        except Exception:
            raise ImportError("Please run `pip install snowflake-sqlalchemy`")

        if not os.environ.get("OPENAI_API_KEY", None):
            raise ValueError("OpenAI API Token is missing or blank.")

        snowflake_uri = f"snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}&role={role}"

        engine = create_engine(snowflake_uri)

        self._sql_database = SQLDatabase(engine)
        self.tables = tables

        self.query_engine = NLSQLTableQueryEngine(
            sql_database=self._sql_database, tables=self.tables
        )

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "sql_database": self._sql_database,
            "query_engine": self.query_engine,
        }

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/snowflake_query_engine/#llama_index.packs.snowflake_query_engine.SnowflakeQueryEnginePack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-snowflake-query-engine/llama_index/packs/snowflake_query_engine/base.py`  
| 
```
52
53
54
55
56
57
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "sql_database": self._sql_database,
        "query_engine": self.query_engine,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/snowflake_query_engine/#llama_index.packs.snowflake_query_engine.SnowflakeQueryEnginePack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-snowflake-query-engine/llama_index/packs/snowflake_query_engine/base.py`  
| 
```
59
60
61
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - SnowflakeQueryEnginePack
