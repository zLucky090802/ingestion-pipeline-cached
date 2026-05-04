# Singlestore
##  SingleStoreReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/singlestore/#llama_index.readers.singlestore.SingleStoreReader "Permanent link")
Bases: 
SingleStore reader.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `scheme`  |  Database Scheme.  |  _required_  |  
|  `host`  |  Database Host.  |  _required_  |  
|  `port`  |  Database Port.  |  _required_  |  
|  `user`  |  Database User.  |  _required_  |  
|  `password`  |  Database Password.  |  _required_  |  
|  `dbname`  |  Database Name.  |  _required_  |  
|  `table_name`  |  Table Name.  |  _required_  |  
|  `content_field`  |  Content Field.  |  `'text'`  |  
|  `vector_field`  |  Vector Field.  |  `'embedding'`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-singlestore/llama_index/readers/singlestore/base.py`  
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
classSingleStoreReader(BaseReader):
"""
    SingleStore reader.

    Args:
        scheme (str): Database Scheme.
        host (str): Database Host.
        port (str): Database Port.
        user (str): Database User.
        password (str): Database Password.
        dbname (str): Database Name.
        table_name (str): Table Name.
        content_field (str): Content Field.
        vector_field (str): Vector Field.

    """

    def__init__(
        self,
        scheme: str,
        host: str,
        port: str,
        user: str,
        password: str,
        dbname: str,
        table_name: str,
        content_field: str = "text",
        vector_field: str = "embedding",
    ):
"""Initialize with parameters."""
        self.scheme = scheme
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.table_name = table_name
        self.content_field = content_field
        self.vector_field = vector_field

        try:
            importpymysql

            pymysql.install_as_MySQLdb()
        except ImportError:
            pass

        self.DatabaseReader = DatabaseReader
        self.reader = self.DatabaseReader(
            scheme=self.scheme,
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname=self.dbname,
        )

    defload_data(self, search_embedding: str, top_k: int = 5) -> List[Document]:
"""
        Load data from SingleStore.

        Args:
            search_embedding (str): The embedding to search.
            top_k (int): Number of results to return.

        Returns:
            List[Document]: A list of documents.

        """
        query = f"""
        SELECT {self.content_field}, DOT_PRODUCT_F64({self.vector_field}, JSON_ARRAY_PACK_F64(\'{search_embedding}\')) AS score
        FROM {self.table_name}
        ORDER BY score
        DESC LIMIT {top_k}
        """

        return self.reader.load_data(query=query)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/singlestore/#llama_index.readers.singlestore.SingleStoreReader.load_data "Permanent link")

```
load_data(
    search_embedding: , top_k:  = 5
) -> []

```

Load data from SingleStore.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `search_embedding`  |  The embedding to search.  |  _required_  |  
|  `top_k`  |  Number of results to return.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-singlestore/llama_index/readers/singlestore/base.py`  
| 
```
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
defload_data(self, search_embedding: str, top_k: int = 5) -> List[Document]:
"""
    Load data from SingleStore.

    Args:
        search_embedding (str): The embedding to search.
        top_k (int): Number of results to return.

    Returns:
        List[Document]: A list of documents.

    """
    query = f"""
    SELECT {self.content_field}, DOT_PRODUCT_F64({self.vector_field}, JSON_ARRAY_PACK_F64(\'{search_embedding}\')) AS score
    FROM {self.table_name}
    ORDER BY score
    DESC LIMIT {top_k}
    """

    return self.reader.load_data(query=query)

```
 |  
| --- | --- |  
options: members: - SingleStoreReader
