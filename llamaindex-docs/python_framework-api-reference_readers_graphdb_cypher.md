# Graphdb cypher
##  GraphDBCypherReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/graphdb_cypher/#llama_index.readers.graphdb_cypher.GraphDBCypherReader "Permanent link")
Bases: 
Graph database Cypher reader.
Combines all Cypher query results into the Document type used by LlamaIndex.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `uri`  |  Graph Database URI  |  _required_  |  
|  `username`  |  Username  |  _required_  |  
|  `password`  |  Password  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-graphdb-cypher/llama_index/readers/graphdb_cypher/base.py`  
| 
```
10
11
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
classGraphDBCypherReader(BaseReader):
"""
    Graph database Cypher reader.

    Combines all Cypher query results into the Document type used by LlamaIndex.

    Args:
        uri (str): Graph Database URI
        username (str): Username
        password (str): Password

    """

    def__init__(self, uri: str, username: str, password: str, database: str) -> None:
"""Initialize with parameters."""
        try:
            fromneo4jimport GraphDatabase, basic_auth

        except ImportError:
            raise ImportError(
                "`neo4j` package not found, please run `pip install neo4j`"
            )
        if uri:
            if uri is None:
                raise ValueError("`uri` must be provided.")
            self.client = GraphDatabase.driver(
                uri=uri, auth=basic_auth(username, password)
            )
            self.database = database

    defload_data(
        self, query: str, parameters: Optional[Dict] = None
    ) -> List[Document]:
"""
        Run the Cypher with optional parameters and turn results into documents.

        Args:
            query (str): Graph Cypher query string.
            parameters (Optional[Dict]): optional query parameters.

        Returns:
            List[Document]: A list of documents.

        """
        if parameters is None:
            parameters = {}

        records, summary, keys = self.client.execute_query(
            query, parameters, database_=self.database
        )

        return [Document(text=yaml.dump(entry.data())) for entry in records]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/graphdb_cypher/#llama_index.readers.graphdb_cypher.GraphDBCypherReader.load_data "Permanent link")

```
load_data(
    query: , parameters: Optional[] = None
) -> []

```

Run the Cypher with optional parameters and turn results into documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Graph Cypher query string.  |  _required_  |  
|  `parameters`  |  `Optional[Dict]`  |  optional query parameters.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-graphdb-cypher/llama_index/readers/graphdb_cypher/base.py`  
| 
```
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
defload_data(
    self, query: str, parameters: Optional[Dict] = None
) -> List[Document]:
"""
    Run the Cypher with optional parameters and turn results into documents.

    Args:
        query (str): Graph Cypher query string.
        parameters (Optional[Dict]): optional query parameters.

    Returns:
        List[Document]: A list of documents.

    """
    if parameters is None:
        parameters = {}

    records, summary, keys = self.client.execute_query(
        query, parameters, database_=self.database
    )

    return [Document(text=yaml.dump(entry.data())) for entry in records]

```
 |  
| --- | --- |  
options: members: - GraphDBCypherReader
