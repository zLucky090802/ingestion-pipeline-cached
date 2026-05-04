# Snowflake
##  SnowflakeReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/snowflake/#llama_index.readers.snowflake.SnowflakeReader "Permanent link")
Bases: 
Initializes a new instance of the SnowflakeReader.
This class establishes a connection to Snowflake using SQLAlchemy, executes query and concatenates each row into Document used by LlamaIndex.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `engine`  |  `Optional[Engine]`  |  SQLAlchemy Engine object of the database connection.  |  
| `account`  |  `Optional[str]`  |  Snowflake account identifier.  |  
|  `Optional[str]`  |  Snowflake account username.  |  
| `password`  |  `Optional[str]`  |  Password for the Snowflake account.  |  
| `database`  |  `Optional[str]`  |  Snowflake database name.  |  
| `schema`  |  `Optional[str]`  |  Snowflake schema name.  |  
| `warehouse`  |  `Optional[str]`  |  Snowflake warehouse name.  |  
| `proxy`  |  `Optional[str]`  |  Proxy setting for the connection.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-snowflake/llama_index/readers/snowflake/base.py`  
| 
```
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
 62
 63
 64
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
```
 | 
```
classSnowflakeReader(BaseReader):
"""
    Initializes a new instance of the SnowflakeReader.

    This class establishes a connection to Snowflake using SQLAlchemy, executes query
    and concatenates each row into Document used by LlamaIndex.

    Attributes:
        engine (Optional[Engine]): SQLAlchemy Engine object of the database connection.



        account (Optional[str]): Snowflake account identifier.
        user (Optional[str]): Snowflake account username.
        password (Optional[str]): Password for the Snowflake account.
        database (Optional[str]): Snowflake database name.
        schema (Optional[str]): Snowflake schema name.
        warehouse (Optional[str]): Snowflake warehouse name.
        proxy (Optional[str]): Proxy setting for the connection.

    """

    def__init__(
        self,
        account: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        schema: Optional[str] = None,
        warehouse: Optional[str] = None,
        role: Optional[str] = None,
        proxy: Optional[str] = None,
        engine: Optional[Engine] = None,
    ) -> None:
"""
        Initializes the SnowflakeReader with optional connection details, proxy configuration, or an engine directly.

        Args:
            account (Optional[str]): Snowflake account identifier.
            user (Optional[str]): Snowflake account username.
            password (Optional[str]): Password for the Snowflake account.
            database (Optional[str]): Snowflake database name.
            schema (Optional[str]): Snowflake schema name.
            warehouse (Optional[str]): Snowflake warehouse name.
            role (Optional[str]): Snowflake role name.
            proxy (Optional[str]): Proxy setting for the connection.
            engine (Optional[Engine]): Existing SQLAlchemy engine.

        """
        fromsnowflake.sqlalchemyimport URL

        if engine is None:
            connect_args = {}
            if proxy:
                connect_args["proxy"] = proxy

            # Create an SQLAlchemy engine for Snowflake
            self.engine = create_engine(
                URL(
                    account=account or "",
                    user=user or "",
                    password=password or "",
                    database=database or "",
                    schema=schema or "",
                    warehouse=warehouse or "",
                    role=role or "",
                ),
                connect_args=connect_args,
            )
        else:
            self.engine = engine

        # Create a sessionmaker bound to the engine
        self.Session = sessionmaker(bind=self.engine)

    defexecute_query(self, query_string: str) -> List[Any]:
"""
        Executes a SQL query and returns the fetched results.

        Args:
            query_string (str): The SQL query to be executed.

        Returns:
            List[Any]: The fetched results from the query.

        """
        # Create a session and execute the query
        session = self.Session()
        try:
            result = session.execute(text(query_string))
            return result.fetchall()
        finally:
            # Ensure the session is closed after query execution
            session.close()

    defload_data(self, query: str) -> List[Document]:
"""
        Query and load data from the Database, returning a list of Documents.

        Args:
            query (str): Query parameter to filter tables and rows.

        Returns:
            List[Document]: A list of Document objects.

        """
        documents = []

        if query is None:
            raise ValueError("A query parameter is necessary to filter the data")

        try:
            result = self.execute_query(query)

            for item in result:
                # fetch each item
                doc_str = ", ".join([str(entry) for entry in item])
                documents.append(Document(text=doc_str))
            return documents
        except Exception as e:
            logger.error(
                f"An error occurred while loading the data: {e}", exc_info=True
            )

```
 |  
| --- | --- |  
###  execute_query [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/snowflake/#llama_index.readers.snowflake.SnowflakeReader.execute_query "Permanent link")

```
execute_query(query_string: ) -> []

```

Executes a SQL query and returns the fetched results.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_string`  |  The SQL query to be executed.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[Any]`  |  List[Any]: The fetched results from the query.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-snowflake/llama_index/readers/snowflake/base.py`  
| 
```
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
```
 | 
```
defexecute_query(self, query_string: str) -> List[Any]:
"""
    Executes a SQL query and returns the fetched results.

    Args:
        query_string (str): The SQL query to be executed.

    Returns:
        List[Any]: The fetched results from the query.

    """
    # Create a session and execute the query
    session = self.Session()
    try:
        result = session.execute(text(query_string))
        return result.fetchall()
    finally:
        # Ensure the session is closed after query execution
        session.close()

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/snowflake/#llama_index.readers.snowflake.SnowflakeReader.load_data "Permanent link")

```
load_data(query: ) -> []

```

Query and load data from the Database, returning a list of Documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Query parameter to filter tables and rows.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of Document objects.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-snowflake/llama_index/readers/snowflake/base.py`  
| 
```
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
```
 | 
```
defload_data(self, query: str) -> List[Document]:
"""
    Query and load data from the Database, returning a list of Documents.

    Args:
        query (str): Query parameter to filter tables and rows.

    Returns:
        List[Document]: A list of Document objects.

    """
    documents = []

    if query is None:
        raise ValueError("A query parameter is necessary to filter the data")

    try:
        result = self.execute_query(query)

        for item in result:
            # fetch each item
            doc_str = ", ".join([str(entry) for entry in item])
            documents.append(Document(text=doc_str))
        return documents
    except Exception as e:
        logger.error(
            f"An error occurred while loading the data: {e}", exc_info=True
        )

```
 |  
| --- | --- |  
options: members: - SnowflakeReader
