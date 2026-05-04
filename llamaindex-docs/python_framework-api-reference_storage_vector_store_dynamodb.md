# Dynamodb
##  DynamoDBVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/dynamodb/#llama_index.vector_stores.dynamodb.DynamoDBVectorStore "Permanent link")
Bases: 
DynamoDB Vector Store.
In this vector store, embeddings are stored within dynamodb table. This class was implemented with reference to SimpleVectorStore.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `dynamodb_kvstore`  |   |  data store  |  _required_  |  
|  `namespace`  |  `Optional[str]`  |  namespace  |  `None`  |  
Examples:
`pip install llama-index-vector-stores-dynamodb`

```
fromllama_index.vector_stores.dynamodbimport DynamoDBVectorStore

vector_store = DynamoDBVectorStore.from_table_name(table_name="my_table")

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-dynamodb/llama_index/vector_stores/dynamodb/base.py`  
| 
```
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
```
 | 
```
classDynamoDBVectorStore(BasePydanticVectorStore):
"""
    DynamoDB Vector Store.

    In this vector store, embeddings are stored within dynamodb table.
    This class was implemented with reference to SimpleVectorStore.

    Args:
        dynamodb_kvstore (DynamoDBKVStore): data store
        namespace (Optional[str]): namespace

    Examples:
        `pip install llama-index-vector-stores-dynamodb`

        ```python
        from llama_index.vector_stores.dynamodb import DynamoDBVectorStore

        vector_store = DynamoDBVectorStore.from_table_name(table_name="my_table")
        ```

    """

    stores_text: bool = False

    _kvstore: DynamoDBKVStore = PrivateAttr()
    _collection_embedding: str = PrivateAttr()
    _collection_text_id_to_doc_id: str = PrivateAttr()
    _key_value: str = PrivateAttr()

    def__init__(
        self, dynamodb_kvstore: DynamoDBKVStore, namespace: str | None = None
    ) -> None:
"""Initialize params."""
        super().__init__()

        self._kvstore = dynamodb_kvstore
        namespace = namespace or DEFAULT_NAMESPACE
        self._collection_embedding = f"{namespace}/embedding"
        self._collection_text_id_to_doc_id = f"{namespace}/text_id_to_doc_id"
        self._key_value = "value"

    @classmethod
    deffrom_table_name(
        cls, table_name: str, namespace: str | None = None
    ) -> DynamoDBVectorStore:
"""Load from DynamoDB table name."""
        dynamodb_kvstore = DynamoDBKVStore.from_table_name(table_name=table_name)
        return cls(dynamodb_kvstore=dynamodb_kvstore, namespace=namespace)

    @classmethod
    defclass_name(cls) -> str:
        return "DynamoDBVectorStore"

    @property
    defclient(self) -> None:
"""Get client."""
        return

    defget(self, text_id: str) -> List[float]:
"""Get embedding."""
        item = self._kvstore.get(key=text_id, collection=self._collection_embedding)
        item = cast(Dict[str, List[float]], item)
        return item[self._key_value]

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""Add nodes to index."""
        response = []
        for node in nodes:
            self._kvstore.put(
                key=node.node_id,
                val={self._key_value: node.get_embedding()},
                collection=self._collection_embedding,
            )
            self._kvstore.put(
                key=node.node_id,
                val={self._key_value: node.ref_doc_id},
                collection=self._collection_text_id_to_doc_id,
            )
            response.append(node.node_id)
        return response

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        text_ids_to_delete = set()
        for text_id, item in self._kvstore.get_all(
            collection=self._collection_text_id_to_doc_id
        ).items():
            if ref_doc_id == item[self._key_value]:
                text_ids_to_delete.add(text_id)

        for text_id in text_ids_to_delete:
            self._kvstore.delete(key=text_id, collection=self._collection_embedding)
            self._kvstore.delete(
                key=text_id, collection=self._collection_text_id_to_doc_id
            )

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Get nodes for response."""
        if query.filters is not None:
            raise ValueError(
                "Metadata filters not implemented for SimpleVectorStore yet."
            )

        # TODO: consolidate with get_query_text_embedding_similarities
        items = self._kvstore.get_all(collection=self._collection_embedding).items()

        if query.node_ids:
            available_ids = set(query.node_ids)

            node_ids = [k for k, _ in items if k in available_ids]
            embeddings = [v[self._key_value] for k, v in items if k in available_ids]
        else:
            node_ids = [k for k, _ in items]
            embeddings = [v[self._key_value] for k, v in items]

        query_embedding = cast(List[float], query.query_embedding)
        if query.mode in LEARNER_MODES:
            top_similarities, top_ids = get_top_k_embeddings_learner(
                query_embedding=query_embedding,
                embeddings=embeddings,
                similarity_top_k=query.similarity_top_k,
                embedding_ids=node_ids,
            )
        elif query.mode == VectorStoreQueryMode.DEFAULT:
            top_similarities, top_ids = get_top_k_embeddings(
                query_embedding=query_embedding,
                embeddings=embeddings,
                similarity_top_k=query.similarity_top_k,
                embedding_ids=node_ids,
            )
        else:
            raise ValueError(f"Invalid query mode: {query.mode}")

        return VectorStoreQueryResult(similarities=top_similarities, ids=top_ids)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/dynamodb/#llama_index.vector_stores.dynamodb.DynamoDBVectorStore.client "Permanent link")

```
client: None

```

Get client.
###  from_table_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/dynamodb/#llama_index.vector_stores.dynamodb.DynamoDBVectorStore.from_table_name "Permanent link")

```
from_table_name(
    table_name: , namespace:  | None = None
) -> 

```

Load from DynamoDB table name.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-dynamodb/llama_index/vector_stores/dynamodb/base.py`  
| 
```
74
75
76
77
78
79
80
```
 | 
```
@classmethod
deffrom_table_name(
    cls, table_name: str, namespace: str | None = None
) -> DynamoDBVectorStore:
"""Load from DynamoDB table name."""
    dynamodb_kvstore = DynamoDBKVStore.from_table_name(table_name=table_name)
    return cls(dynamodb_kvstore=dynamodb_kvstore, namespace=namespace)

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/dynamodb/#llama_index.vector_stores.dynamodb.DynamoDBVectorStore.get "Permanent link")

```
get(text_id: ) -> [float]

```

Get embedding.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-dynamodb/llama_index/vector_stores/dynamodb/base.py`  
| 
```
91
92
93
94
95
```
 | 
```
defget(self, text_id: str) -> List[float]:
"""Get embedding."""
    item = self._kvstore.get(key=text_id, collection=self._collection_embedding)
    item = cast(Dict[str, List[float]], item)
    return item[self._key_value]

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/dynamodb/#llama_index.vector_stores.dynamodb.DynamoDBVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-dynamodb/llama_index/vector_stores/dynamodb/base.py`  
| 
```
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
```
 | 
```
defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""Add nodes to index."""
    response = []
    for node in nodes:
        self._kvstore.put(
            key=node.node_id,
            val={self._key_value: node.get_embedding()},
            collection=self._collection_embedding,
        )
        self._kvstore.put(
            key=node.node_id,
            val={self._key_value: node.ref_doc_id},
            collection=self._collection_text_id_to_doc_id,
        )
        response.append(node.node_id)
    return response

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/dynamodb/#llama_index.vector_stores.dynamodb.DynamoDBVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-dynamodb/llama_index/vector_stores/dynamodb/base.py`  
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    text_ids_to_delete = set()
    for text_id, item in self._kvstore.get_all(
        collection=self._collection_text_id_to_doc_id
    ).items():
        if ref_doc_id == item[self._key_value]:
            text_ids_to_delete.add(text_id)

    for text_id in text_ids_to_delete:
        self._kvstore.delete(key=text_id, collection=self._collection_embedding)
        self._kvstore.delete(
            key=text_id, collection=self._collection_text_id_to_doc_id
        )

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/dynamodb/#llama_index.vector_stores.dynamodb.DynamoDBVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Get nodes for response.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-dynamodb/llama_index/vector_stores/dynamodb/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Get nodes for response."""
    if query.filters is not None:
        raise ValueError(
            "Metadata filters not implemented for SimpleVectorStore yet."
        )

    # TODO: consolidate with get_query_text_embedding_similarities
    items = self._kvstore.get_all(collection=self._collection_embedding).items()

    if query.node_ids:
        available_ids = set(query.node_ids)

        node_ids = [k for k, _ in items if k in available_ids]
        embeddings = [v[self._key_value] for k, v in items if k in available_ids]
    else:
        node_ids = [k for k, _ in items]
        embeddings = [v[self._key_value] for k, v in items]

    query_embedding = cast(List[float], query.query_embedding)
    if query.mode in LEARNER_MODES:
        top_similarities, top_ids = get_top_k_embeddings_learner(
            query_embedding=query_embedding,
            embeddings=embeddings,
            similarity_top_k=query.similarity_top_k,
            embedding_ids=node_ids,
        )
    elif query.mode == VectorStoreQueryMode.DEFAULT:
        top_similarities, top_ids = get_top_k_embeddings(
            query_embedding=query_embedding,
            embeddings=embeddings,
            similarity_top_k=query.similarity_top_k,
            embedding_ids=node_ids,
        )
    else:
        raise ValueError(f"Invalid query mode: {query.mode}")

    return VectorStoreQueryResult(similarities=top_similarities, ids=top_ids)

```
 |  
| --- | --- |  
options: members: - DynamoDBVectorStore
