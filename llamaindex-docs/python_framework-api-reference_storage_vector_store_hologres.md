# Hologres
##  HologresVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/hologres/#llama_index.vector_stores.hologres.HologresVectorStore "Permanent link")
Bases: 
Hologres Vector Store.
Hologres is a one-stop real-time data warehouse, which can support high performance OLAP analysis and high QPS online services. Hologres supports vector processing and allows you to use vector data to show the characteristics of unstructured data. https://www.alibabacloud.com/help/en/hologres/user-guide/introduction-to-vector-processing
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-hologres/llama_index/vector_stores/hologres/base.py`  
| 
```
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
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
```
 | 
```
classHologresVectorStore(BasePydanticVectorStore):
"""
    Hologres Vector Store.

    Hologres is a one-stop real-time data warehouse, which can support high performance OLAP analysis and high QPS online services.
    Hologres supports vector processing and allows you to use vector data
    to show the characteristics of unstructured data.
    https://www.alibabacloud.com/help/en/hologres/user-guide/introduction-to-vector-processing

    """

    # Hologres storage instance
    _storage: HologresVector = PrivateAttr()

    # Hologres vector db stores the document node's text as string.
    stores_text: bool = True

    def__init__(self, hologres_storage: HologresVector):
"""
        Construct from a Hologres storage instance.
        You can use from_connection_string instead.
        """
        super().__init__()
        self._storage = hologres_storage

    @classmethod
    deffrom_connection_string(
        cls,
        connection_string: str,
        table_name: str,
        table_schema: Dict[str, str] = {"document": "text"},
        embedding_dimension: int = 1536,
        pre_delete_table: bool = False,
    ) -> "HologresVectorStore":
"""
        Create Hologres Vector Store from connection string.

        Args:
            connection_string: connection string of hologres database
            table_name: table name to persist data
            table_schema: table column schemam
            embedding_dimension: dimension size of embedding vector
            pre_delete_table: whether to erase data from table on creation

        """
        hologres_storage = HologresVector(
            connection_string,
            ndims=embedding_dimension,
            table_name=table_name,
            table_schema=table_schema,
            pre_delete_table=pre_delete_table,
        )
        return cls(hologres_storage=hologres_storage)

    @classmethod
    deffrom_param(
        cls,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
        table_name: str,
        table_schema: Dict[str, str] = {"document": "text"},
        embedding_dimension: int = 1536,
        pre_delete_table: bool = False,
    ) -> "HologresVectorStore":
"""
        Create Hologres Vector Store from database configurations.

        Args:
            host: host
            port: port number
            user: hologres user
            password: hologres password
            database: hologres database
            table_name: hologres table name
            table_schema: table column schemam
            embedding_dimension: dimension size of embedding vector
            pre_delete_table: whether to erase data from table on creation

        """
        connection_string = HologresVector.connection_string_from_db_params(
            host, port, database, user, password
        )
        return cls.from_connection_string(
            connection_string=connection_string,
            table_name=table_name,
            embedding_dimension=embedding_dimension,
            table_schema=table_schema,
            pre_delete_table=pre_delete_table,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "HologresVectorStore"

    @property
    defclient(self) -> Any:
        return self._storage

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to hologres index.

        Embedding data will be saved to `vector` column and text will be saved to `document` column.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        """
        embeddings = []
        node_ids = []
        schema_data_list = []
        meta_data_list = []

        for node in nodes:
            text_embedding = node.get_embedding()
            embeddings.append(text_embedding)
            node_ids.append(node.node_id)
            meta_data_list.append(node.metadata)
            schema_data_list.append(
                {"document": node.get_content(metadata_mode=MetadataMode.NONE)}
            )

        self._storage.upsert_vectors(
            embeddings, node_ids, meta_data_list, schema_data_list
        )
        return node_ids

    defquery(
        self,
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query_embedding (List[float]): query embedding
            similarity_top_k (int): top k most similar nodes

        """
        query_embedding = cast(List[float], query.query_embedding)
        top_k = query.similarity_top_k

        query_results: List[dict[str, Any]] = self._storage.search(
            query_embedding,
            k=top_k,
            select_columns=["document", "vector"],
            metadata_filters=query.filters,
        )

        # if empty, then return an empty response
        if len(query_results) == 0:
            return VectorStoreQueryResult(similarities=[], ids=[])

        nodes = []
        similarities = []
        ids = []

        for result in query_results:
            node = TextNode(
                text=result["document"],
                id_=result["id"],
                embedding=result["vector"],
                metadata=result["metadata"],
            )
            nodes.append(node)
            ids.append(result["id"])
            similarities.append(math.exp(-result["distance"]))

        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        self._storage.delete_vectors(metadata_filters={"doc_id": ref_doc_id})

```
 |  
| --- | --- |  
###  from_connection_string `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/hologres/#llama_index.vector_stores.hologres.HologresVectorStore.from_connection_string "Permanent link")

```
from_connection_string(
    connection_string: ,
    table_name: ,
    table_schema: [, ] = {"document": "text"},
    embedding_dimension:  = 1536,
    pre_delete_table:  = False,
) -> 

```

Create Hologres Vector Store from connection string.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `connection_string`  |  connection string of hologres database  |  _required_  |  
|  `table_name`  |  table name to persist data  |  _required_  |  
|  `table_schema`  |  `Dict[str, str]`  |  table column schemam  |  `{'document': 'text'}`  |  
|  `embedding_dimension`  |  dimension size of embedding vector  |  `1536`  |  
|  `pre_delete_table`  |  `bool`  |  whether to erase data from table on creation  |  `False`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-hologres/llama_index/vector_stores/hologres/base.py`  
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
```
 | 
```
@classmethod
deffrom_connection_string(
    cls,
    connection_string: str,
    table_name: str,
    table_schema: Dict[str, str] = {"document": "text"},
    embedding_dimension: int = 1536,
    pre_delete_table: bool = False,
) -> "HologresVectorStore":
"""
    Create Hologres Vector Store from connection string.

    Args:
        connection_string: connection string of hologres database
        table_name: table name to persist data
        table_schema: table column schemam
        embedding_dimension: dimension size of embedding vector
        pre_delete_table: whether to erase data from table on creation

    """
    hologres_storage = HologresVector(
        connection_string,
        ndims=embedding_dimension,
        table_name=table_name,
        table_schema=table_schema,
        pre_delete_table=pre_delete_table,
    )
    return cls(hologres_storage=hologres_storage)

```
 |  
| --- | --- |  
###  from_param `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/hologres/#llama_index.vector_stores.hologres.HologresVectorStore.from_param "Permanent link")

```
from_param(
    host: ,
    port: ,
    user: ,
    password: ,
    database: ,
    table_name: ,
    table_schema: [, ] = {"document": "text"},
    embedding_dimension:  = 1536,
    pre_delete_table:  = False,
) -> 

```

Create Hologres Vector Store from database configurations.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `host`  |  host  |  _required_  |  
|  `port`  |  port number  |  _required_  |  
|  `user`  |  hologres user  |  _required_  |  
|  `password`  |  hologres password  |  _required_  |  
|  `database`  |  hologres database  |  _required_  |  
|  `table_name`  |  hologres table name  |  _required_  |  
|  `table_schema`  |  `Dict[str, str]`  |  table column schemam  |  `{'document': 'text'}`  |  
|  `embedding_dimension`  |  dimension size of embedding vector  |  `1536`  |  
|  `pre_delete_table`  |  `bool`  |  whether to erase data from table on creation  |  `False`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-hologres/llama_index/vector_stores/hologres/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_param(
    cls,
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
    table_name: str,
    table_schema: Dict[str, str] = {"document": "text"},
    embedding_dimension: int = 1536,
    pre_delete_table: bool = False,
) -> "HologresVectorStore":
"""
    Create Hologres Vector Store from database configurations.

    Args:
        host: host
        port: port number
        user: hologres user
        password: hologres password
        database: hologres database
        table_name: hologres table name
        table_schema: table column schemam
        embedding_dimension: dimension size of embedding vector
        pre_delete_table: whether to erase data from table on creation

    """
    connection_string = HologresVector.connection_string_from_db_params(
        host, port, database, user, password
    )
    return cls.from_connection_string(
        connection_string=connection_string,
        table_name=table_name,
        embedding_dimension=embedding_dimension,
        table_schema=table_schema,
        pre_delete_table=pre_delete_table,
    )

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/hologres/#llama_index.vector_stores.hologres.HologresVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to hologres index.
Embedding data will be saved to `vector` column and text will be saved to `document` column.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-hologres/llama_index/vector_stores/hologres/base.py`  
| 
```
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
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
```
 | 
```
defadd(
    self,
    nodes: List[BaseNode],
    **add_kwargs: Any,
) -> List[str]:
"""
    Add nodes to hologres index.

    Embedding data will be saved to `vector` column and text will be saved to `document` column.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings

    """
    embeddings = []
    node_ids = []
    schema_data_list = []
    meta_data_list = []

    for node in nodes:
        text_embedding = node.get_embedding()
        embeddings.append(text_embedding)
        node_ids.append(node.node_id)
        meta_data_list.append(node.metadata)
        schema_data_list.append(
            {"document": node.get_content(metadata_mode=MetadataMode.NONE)}
        )

    self._storage.upsert_vectors(
        embeddings, node_ids, meta_data_list, schema_data_list
    )
    return node_ids

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/hologres/#llama_index.vector_stores.hologres.HologresVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_embedding`  |  `List[float]`  |  query embedding  |  _required_  |  
|  `similarity_top_k`  |  top k most similar nodes  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-hologres/llama_index/vector_stores/hologres/base.py`  
| 
```
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
```
 | 
```
defquery(
    self,
    query: VectorStoreQuery,
    **kwargs: Any,
) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query_embedding (List[float]): query embedding
        similarity_top_k (int): top k most similar nodes

    """
    query_embedding = cast(List[float], query.query_embedding)
    top_k = query.similarity_top_k

    query_results: List[dict[str, Any]] = self._storage.search(
        query_embedding,
        k=top_k,
        select_columns=["document", "vector"],
        metadata_filters=query.filters,
    )

    # if empty, then return an empty response
    if len(query_results) == 0:
        return VectorStoreQueryResult(similarities=[], ids=[])

    nodes = []
    similarities = []
    ids = []

    for result in query_results:
        node = TextNode(
            text=result["document"],
            id_=result["id"],
            embedding=result["vector"],
            metadata=result["metadata"],
        )
        nodes.append(node)
        ids.append(result["id"])
        similarities.append(math.exp(-result["distance"]))

    return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/hologres/#llama_index.vector_stores.hologres.HologresVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-hologres/llama_index/vector_stores/hologres/base.py`  
| 
```
200
201
202
203
204
205
206
207
208
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    self._storage.delete_vectors(metadata_filters={"doc_id": ref_doc_id})

```
 |  
| --- | --- |  
options: members: - HologresVectorStore
