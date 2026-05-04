# Cassandra
##  CassandraDatabaseToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/cassandra/#llama_index.tools.cassandra.CassandraDatabaseToolSpec "Permanent link")
Bases: 
Base tool for interacting with an Apache Cassandra database.
Source code in `llama-index-integrations/tools/llama-index-tools-cassandra/llama_index/tools/cassandra/base.py`  
| 
```
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
```
 | 
```
classCassandraDatabaseToolSpec(BaseToolSpec):
"""Base tool for interacting with an Apache Cassandra database."""

    db: CassandraDatabase = Field(exclude=True)

    spec_functions = [
        "cassandra_db_query",
        "cassandra_db_schema",
        "cassandra_db_select_table_data",
    ]

    def__init__(self, db: CassandraDatabase) -> None:
"""DB session in context."""
        self.db = db

    defcassandra_db_query(self, query: str) -> List[Document]:
"""
        Execute a CQL query and return the results as a list of Documents.

        Args:
            query (str): A CQL query to execute.

        Returns:
            List[Document]: A list of Document objects, each containing data from a row.

        """
        documents = []
        result = self.db.run_no_throw(query, fetch="Cursor")
        for row in result:
            doc_str = ", ".join([str(value) for value in row])
            documents.append(Document(text=doc_str))
        return documents

    defcassandra_db_schema(self, keyspace: str) -> List[Document]:
"""
        Input to this tool is a keyspace name, output is a table description
            of Apache Cassandra tables.
            If the query is not correct, an error message will be returned.
            If an error is returned, report back to the user that the keyspace
            doesn't exist and stop.

        Args:
            keyspace (str): The name of the keyspace for which to return the schema.

        Returns:
            List[Document]: A list of Document objects, each containing a table description.

        """
        return [Document(text=self.db.get_keyspace_tables_str(keyspace))]

    defcassandra_db_select_table_data(
        self, keyspace: str, table: str, predicate: str, limit: int
    ) -> List[Document]:
"""
        Tool for getting data from a table in an Apache Cassandra database.
            Use the WHERE clause to specify the predicate for the query that uses the
            primary key. A blank predicate will return all rows. Avoid this if possible.
            Use the limit to specify the number of rows to return. A blank limit will
            return all rows.

        Args:
            keyspace (str): The name of the keyspace containing the table.
            table (str): The name of the table for which to return data.
            predicate (str): The predicate for the query that uses the primary key.
            limit (int): The maximum number of rows to return.

        Returns:
            List[Document]: A list of Document objects, each containing a row of data.

        """
        return [
            Document(text=self.db.get_table_data(keyspace, table, predicate, limit))
        ]

```
 |  
| --- | --- |  
###  cassandra_db_query [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/cassandra/#llama_index.tools.cassandra.CassandraDatabaseToolSpec.cassandra_db_query "Permanent link")

```
cassandra_db_query(query: ) -> []

```

Execute a CQL query and return the results as a list of Documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  A CQL query to execute.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of Document objects, each containing data from a row.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-cassandra/llama_index/tools/cassandra/base.py`  
| 
```
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
```
 | 
```
defcassandra_db_query(self, query: str) -> List[Document]:
"""
    Execute a CQL query and return the results as a list of Documents.

    Args:
        query (str): A CQL query to execute.

    Returns:
        List[Document]: A list of Document objects, each containing data from a row.

    """
    documents = []
    result = self.db.run_no_throw(query, fetch="Cursor")
    for row in result:
        doc_str = ", ".join([str(value) for value in row])
        documents.append(Document(text=doc_str))
    return documents

```
 |  
| --- | --- |  
###  cassandra_db_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/cassandra/#llama_index.tools.cassandra.CassandraDatabaseToolSpec.cassandra_db_schema "Permanent link")

```
cassandra_db_schema(keyspace: ) -> []

```

Input to this tool is a keyspace name, output is a table description of Apache Cassandra tables. If the query is not correct, an error message will be returned. If an error is returned, report back to the user that the keyspace doesn't exist and stop.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `keyspace`  |  The name of the keyspace for which to return the schema.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of Document objects, each containing a table description.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-cassandra/llama_index/tools/cassandra/base.py`  
| 
```
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
```
 | 
```
defcassandra_db_schema(self, keyspace: str) -> List[Document]:
"""
    Input to this tool is a keyspace name, output is a table description
        of Apache Cassandra tables.
        If the query is not correct, an error message will be returned.
        If an error is returned, report back to the user that the keyspace
        doesn't exist and stop.

    Args:
        keyspace (str): The name of the keyspace for which to return the schema.

    Returns:
        List[Document]: A list of Document objects, each containing a table description.

    """
    return [Document(text=self.db.get_keyspace_tables_str(keyspace))]

```
 |  
| --- | --- |  
###  cassandra_db_select_table_data [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/cassandra/#llama_index.tools.cassandra.CassandraDatabaseToolSpec.cassandra_db_select_table_data "Permanent link")

```
cassandra_db_select_table_data(
    keyspace: , table: , predicate: , limit: 
) -> []

```

Tool for getting data from a table in an Apache Cassandra database. Use the WHERE clause to specify the predicate for the query that uses the primary key. A blank predicate will return all rows. Avoid this if possible. Use the limit to specify the number of rows to return. A blank limit will return all rows.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `keyspace`  |  The name of the keyspace containing the table.  |  _required_  |  
|  `table`  |  The name of the table for which to return data.  |  _required_  |  
|  `predicate`  |  The predicate for the query that uses the primary key.  |  _required_  |  
|  `limit`  |  The maximum number of rows to return.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of Document objects, each containing a row of data.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-cassandra/llama_index/tools/cassandra/base.py`  
| 
```
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
```
 | 
```
defcassandra_db_select_table_data(
    self, keyspace: str, table: str, predicate: str, limit: int
) -> List[Document]:
"""
    Tool for getting data from a table in an Apache Cassandra database.
        Use the WHERE clause to specify the predicate for the query that uses the
        primary key. A blank predicate will return all rows. Avoid this if possible.
        Use the limit to specify the number of rows to return. A blank limit will
        return all rows.

    Args:
        keyspace (str): The name of the keyspace containing the table.
        table (str): The name of the table for which to return data.
        predicate (str): The predicate for the query that uses the primary key.
        limit (int): The maximum number of rows to return.

    Returns:
        List[Document]: A list of Document objects, each containing a row of data.

    """
    return [
        Document(text=self.db.get_table_data(keyspace, table, predicate, limit))
    ]

```
 |  
| --- | --- |  
options: members: - CassandraDatabaseToolSpec
