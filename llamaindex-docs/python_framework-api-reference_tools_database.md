# Database
##  DatabaseToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/database/#llama_index.tools.database.DatabaseToolSpec "Permanent link")
Bases: , 
Simple Database tool.
Concatenates each row into Document used by LlamaIndex.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `sql_database`  |  `Optional[SQLDatabase[](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SQLDatabase "SQLDatabase \(llama_index.core.utilities.sql_wrapper.SQLDatabase\)")]`  |  SQL database to use, including table names to specify. See :ref:`Ref-Struct-Store` for more details.  |  `None`  |  
|  `engine`  |  `Optional[Engine]`  |  SQLAlchemy Engine object of the database connection.  |  `None`  |  
|  `uri`  |  `Optional[str]`  |  uri of the database connection.  |  `None`  |  
|  `scheme`  |  `Optional[str]`  |  scheme of the database connection.  |  `None`  |  
|  `host`  |  `Optional[str]`  |  host of the database connection.  |  `None`  |  
|  `port`  |  `Optional[int]`  |  port of the database connection.  |  `None`  |  
|  `user`  |  `Optional[str]`  |  user of the database connection.  |  `None`  |  
|  `password`  |  `Optional[str]`  |  password of the database connection.  |  `None`  |  
|  `dbname`  |  `Optional[str]`  |  dbname of the database connection.  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-database/llama_index/tools/database/base.py`  
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
138
139
```
 | 
```
classDatabaseToolSpec(BaseToolSpec, BaseReader):
"""
    Simple Database tool.

    Concatenates each row into Document used by LlamaIndex.

    Args:
        sql_database (Optional[SQLDatabase]): SQL database to use,
            including table names to specify.
            See :ref:`Ref-Struct-Store` for more details.



        engine (Optional[Engine]): SQLAlchemy Engine object of the database connection.



        uri (Optional[str]): uri of the database connection.



        scheme (Optional[str]): scheme of the database connection.
        host (Optional[str]): host of the database connection.
        port (Optional[int]): port of the database connection.
        user (Optional[str]): user of the database connection.
        password (Optional[str]): password of the database connection.
        dbname (Optional[str]): dbname of the database connection.

    """

    spec_functions = ["load_data", "describe_tables", "list_tables"]

    def__init__(
        self,
        sql_database: Optional[SQLDatabase] = None,
        engine: Optional[Engine] = None,
        uri: Optional[str] = None,
        scheme: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        dbname: Optional[str] = None,
        *args: Optional[Any],
        **kwargs: Optional[Any],
    ) -> None:
"""Initialize with parameters."""
        if sql_database:
            self.sql_database = sql_database
        elif engine:
            self.sql_database = SQLDatabase(engine, *args, **kwargs)
        elif uri:
            self.uri = uri
            self.sql_database = SQLDatabase.from_uri(uri, *args, **kwargs)
        elif scheme and host and port and user and password and dbname:
            uri = f"{scheme}://{user}:{password}@{host}:{port}/{dbname}"
            self.uri = uri
            self.sql_database = SQLDatabase.from_uri(uri, *args, **kwargs)
        else:
            raise ValueError(
                "You must provide either a SQLDatabase, "
                "a SQL Alchemy Engine, a valid connection URI, or a valid "
                "set of credentials."
            )
        self._metadata = MetaData()
        self._metadata.reflect(bind=self.sql_database.engine)

    defload_data(self, query: str) -> List[Document]:
"""
        Query and load data from the Database, returning a list of Documents.

        Args:
            query (str): an SQL query to filter tables and rows.

        Returns:
            List[Document]: A list of Document objects.

        """
        documents = []
        with self.sql_database.engine.connect() as connection:
            if query is None:
                raise ValueError("A query parameter is necessary to filter the data")
            else:
                result = connection.execute(text(query))

            for item in result.fetchall():
                # fetch each item
                doc_str = ", ".join([str(entry) for entry in item])
                documents.append(Document(text=doc_str))
        return documents

    deflist_tables(self) -> List[str]:
"""
        Returns a list of available tables in the database.
        To retrieve details about the columns of specific tables, use
        the describe_tables endpoint.
        """
        return [x.name for x in self._metadata.sorted_tables]

    defdescribe_tables(self, tables: Optional[List[str]] = None) -> str:
"""
        Describes the specified tables in the database.

        Args:
            tables (List[str]): A list of table names to retrieve details about

        """
        table_names = tables or [table.name for table in self._metadata.sorted_tables]
        table_schemas = []

        for table_name in table_names:
            table = next(
                (
                    table
                    for table in self._metadata.sorted_tables
                    if table.name == table_name
                ),
                None,
            )
            if table is None:
                raise NoSuchTableError(f"Table '{table_name}' does not exist.")
            schema = str(CreateTable(table).compile(self.sql_database._engine))
            table_schemas.append(f"{schema}\n")

        return "\n".join(table_schemas)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/database/#llama_index.tools.database.DatabaseToolSpec.load_data "Permanent link")

```
load_data(query: ) -> []

```

Query and load data from the Database, returning a list of Documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  an SQL query to filter tables and rows.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of Document objects.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-database/llama_index/tools/database/base.py`  
| 
```
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
```
 | 
```
defload_data(self, query: str) -> List[Document]:
"""
    Query and load data from the Database, returning a list of Documents.

    Args:
        query (str): an SQL query to filter tables and rows.

    Returns:
        List[Document]: A list of Document objects.

    """
    documents = []
    with self.sql_database.engine.connect() as connection:
        if query is None:
            raise ValueError("A query parameter is necessary to filter the data")
        else:
            result = connection.execute(text(query))

        for item in result.fetchall():
            # fetch each item
            doc_str = ", ".join([str(entry) for entry in item])
            documents.append(Document(text=doc_str))
    return documents

```
 |  
| --- | --- |  
###  list_tables [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/database/#llama_index.tools.database.DatabaseToolSpec.list_tables "Permanent link")

```
list_tables() -> []

```

Returns a list of available tables in the database. To retrieve details about the columns of specific tables, use the describe_tables endpoint.
Source code in `llama-index-integrations/tools/llama-index-tools-database/llama_index/tools/database/base.py`  
| 
```
106
107
108
109
110
111
112
```
 | 
```
deflist_tables(self) -> List[str]:
"""
    Returns a list of available tables in the database.
    To retrieve details about the columns of specific tables, use
    the describe_tables endpoint.
    """
    return [x.name for x in self._metadata.sorted_tables]

```
 |  
| --- | --- |  
###  describe_tables [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/database/#llama_index.tools.database.DatabaseToolSpec.describe_tables "Permanent link")

```
describe_tables(tables: Optional[[]] = None) -> 

```

Describes the specified tables in the database.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `tables`  |  `List[str]`  |  A list of table names to retrieve details about  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-database/llama_index/tools/database/base.py`  
| 
```
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
138
139
```
 | 
```
defdescribe_tables(self, tables: Optional[List[str]] = None) -> str:
"""
    Describes the specified tables in the database.

    Args:
        tables (List[str]): A list of table names to retrieve details about

    """
    table_names = tables or [table.name for table in self._metadata.sorted_tables]
    table_schemas = []

    for table_name in table_names:
        table = next(
            (
                table
                for table in self._metadata.sorted_tables
                if table.name == table_name
            ),
            None,
        )
        if table is None:
            raise NoSuchTableError(f"Table '{table_name}' does not exist.")
        schema = str(CreateTable(table).compile(self.sql_database._engine))
        table_schemas.append(f"{schema}\n")

    return "\n".join(table_schemas)

```
 |  
| --- | --- |  
options: members: - DatabaseToolSpec
