# Tidbvector
##  TiDBVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tidbvector/#llama_index.vector_stores.tidbvector.TiDBVectorStore "Permanent link")
Bases: 
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tidbvector/llama_index/vector_stores/tidbvector/base.py`  
| 
```
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
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
```
 | 
```
classTiDBVectorStore(BasePydanticVectorStore):
    stores_text: bool = True
    flat_metadata: bool = False

    _connection_string: str = PrivateAttr()
    _engine_args: Dict[str, Any] = PrivateAttr()
    _tidb: Any = PrivateAttr()

    def__init__(
        self,
        connection_string: str,
        table_name: str = DEFAULT_VECTOR_TABLE_NAME,
        distance_strategy: str = DEFAULT_DISTANCE_STRATEGY,
        vector_dimension: int = 1536,
        *,
        engine_args: Optional[Dict[str, Any]] = None,
        drop_existing_table: bool = False,
        **kwargs: Any,
    ) -> None:
"""
        Initialize a TiDB Vector Store in Llama Index with a flexible
        and standardized table structure for storing vector data
        which remains fixed regardless of the dynamic table name setting.

        The vector table schema includes:
        - 'id': a UUID for each entry.
        - 'embedding': stores vector data in a VectorType column.
        - 'document': a Text column for the original data or additional information.
        - 'meta': a JSON column for flexible metadata storage.
        - 'create_time' and 'update_time': timestamp columns for tracking data changes.

        This table structure caters to general use cases and
        complex scenarios where the table serves as a semantic layer for advanced
        data integration and analysis, leveraging SQL for join queries.

        Args:
            connection_string (str): The connection string for the TiDB database.
                format: "mysql+pymysql://root@34.212.137.91:4000/test".
            table_name (str, optional): The name of the table that will be used to
                store vector data. If you do not provide a table name,
                a default table named `llama_index_vector_store` will be created automatically
            distance_strategy: The strategy used for similarity search,
                defaults to "cosine", valid values: "l2", "cosine".
            vector_dimension: The dimension of the vector, defaults to 1536.
            engine_args (Optional[Dict[str, Any]], optional): Additional engine arguments. Defaults to None.
            drop_existing_table: Drop the existing TiDB table before initializing,
                defaults to False.
            **kwargs (Any): Additional keyword arguments.

        Raises:
            ImportError: If the tidbvec python package is not installed.

        """
        super().__init__(**kwargs)
        self._connection_string = connection_string
        self._engine_args = engine_args or {}
        try:
            fromtidb_vector.integrationsimport TiDBVectorClient
        except ImportError:
            raise ImportError(
                "Could not import tidbvec python package. "
                "Please install it with `pip install tidb-vector`."
            )

        self._tidb = TiDBVectorClient(
            connection_string=connection_string,
            table_name=table_name,
            distance_strategy=distance_strategy,
            vector_dimension=vector_dimension,
            engine_args=engine_args,
            drop_existing_table=drop_existing_table,
            **kwargs,
        )

    @property
    defclient(self) -> Any:
"""Get client."""
        return self._tidb

    defdrop_vectorstore(self) -> None:
"""
        Drop the tidb vector store from the TiDB database.
        """
        self._tidb.drop_table()

    @classmethod
    defclass_name(cls) -> str:
        return "TiDBVectorStore"

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
        Add nodes to the vector store.

        Args:
            nodes (List[BaseNode]): List of nodes to be added.
            **add_kwargs: Additional keyword arguments to be passed to the underlying storage.

        Returns:
            List[str]: List of node IDs that were added.

        """
        ids = []
        metadatas = []
        embeddings = []
        texts = []
        for node in nodes:
            ids.append(node.node_id)
            metadatas.append(node_to_metadata_dict(node, remove_text=True))
            embeddings.append(node.get_embedding())
            texts.append(node.get_content(metadata_mode=MetadataMode.NONE))

        self._tidb.insert(
            texts=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
            **add_kwargs,
        )

        return ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete all nodes of a document from the vector store.

        Args:
            ref_doc_id (str): The reference document ID to be deleted.
            **delete_kwargs: Additional keyword arguments to be passed to the delete method.

        Returns:
            None

        """
        delete_kwargs["filter"] = {"doc_id": ref_doc_id}
        self._tidb.delete(**delete_kwargs)

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Perform a similarity search with the given query embedding.

        Args:
            query (VectorStoreQuery): The query object containing the query data.
            **kwargs: Additional keyword arguments.

        Returns:
            VectorStoreQueryResult: The result of the similarity search.

        Raises:
            ValueError: If the query embedding is not provided.

        """
        if query.query_embedding is None:
            raise ValueError("Query embedding must be provided.")
        return self._similarity_search_with_score(
            query.query_embedding,
            query.similarity_top_k,
            query.filters,
            **kwargs,
        )

    def_similarity_search_with_score(
        self,
        embedding: List[float],
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""
        Performs a similarity search with scores based on the given condition.

        Args:
            embedding (List[float]): The embedding vector for similarity search.
            limit (int, optional): The maximum number of results to return. Defaults to 10.
            metadata_filters (Optional[MetadataFilters], optional): Filters to apply on metadata. Defaults to None.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            VectorStoreQueryResult: The result of the similarity search, including nodes, similarities, and ids.

        """
        filters = self._to_tidb_filters(metadata_filters)
        results = self._tidb.query(
            query_vector=embedding, k=limit, filter=filters, **kwargs
        )

        nodes = []
        similarities = []
        ids = []
        for row in results:
            try:
                node = metadata_dict_to_node(row.metadata)
                node.set_content(str(row.document))
            except Exception:
                # NOTE: deprecated legacy logic for backward compatibility
                _logger.warning(
                    "Failed to parse metadata dict, falling back to legacy logic."
                )
                node = TextNode(
                    id_=row.id,
                    text=row.document,
                    metadata=row.metadata,
                )
            similarities.append((1 - row.distance) if row.distance is not None else 0)
            ids.append(row.id)
            nodes.append(node)

        return VectorStoreQueryResult(
            nodes=nodes,
            similarities=similarities,
            ids=ids,
        )

    def_to_tidb_filters(
        self, metadata_filters: Optional[MetadataFilters] = None
    ) -> Optional[Dict[str, Any]]:
"""
        Converts metadata filters to TiDB filters.

        Args:
            metadata_filters (Optional[MetadataFilters]): The metadata filters to be converted.

        Returns:
            Optional[Dict[str, Any]]: The converted TiDB filters.

        Raises:
            ValueError: If an unsupported operator is encountered.

        """
        if metadata_filters is None:
            return None

        condition = "$and"
        if metadata_filters.condition == FilterCondition.OR:
            condition = "$or"

        filters = []
        for filter in metadata_filters.filters:
            if filter.operator == FilterOperator.EQ:
                filters.append({filter.key: {"$eq": filter.value}})
            elif filter.operator == FilterOperator.NE:
                filters.append({filter.key: {"$ne": filter.value}})
            elif filter.operator == FilterOperator.GT:
                filters.append({filter.key: {"$gt": filter.value}})
            elif filter.operator == FilterOperator.GTE:
                filters.append({filter.key: {"$gte": filter.value}})
            elif filter.operator == FilterOperator.LT:
                filters.append({filter.key: {"$lt": filter.value}})
            elif filter.operator == FilterOperator.LTE:
                filters.append({filter.key: {"$lte": filter.value}})
            elif filter.operator == FilterOperator.IN:
                filters.append({filter.key: {"$in": filter.value}})
            elif filter.operator == FilterOperator.NIN:
                filters.append({filter.key: {"$nin": filter.value}})
            else:
                raise ValueError(f"Unsupported operator: {filter.operator}")

        return {condition: filters}

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tidbvector/#llama_index.vector_stores.tidbvector.TiDBVectorStore.client "Permanent link")

```
client: 

```

Get client.
###  drop_vectorstore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tidbvector/#llama_index.vector_stores.tidbvector.TiDBVectorStore.drop_vectorstore "Permanent link")

```
drop_vectorstore() -> None

```

Drop the tidb vector store from the TiDB database.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tidbvector/llama_index/vector_stores/tidbvector/base.py`  
| 
```
104
105
106
107
108
```
 | 
```
defdrop_vectorstore(self) -> None:
"""
    Drop the tidb vector store from the TiDB database.
    """
    self._tidb.drop_table()

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tidbvector/#llama_index.vector_stores.tidbvector.TiDBVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to the vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes to be added.  |  _required_  |  
|  `**add_kwargs`  |  Additional keyword arguments to be passed to the underlying storage.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: List of node IDs that were added.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tidbvector/llama_index/vector_stores/tidbvector/base.py`  
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
140
141
142
143
144
```
 | 
```
defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
    Add nodes to the vector store.

    Args:
        nodes (List[BaseNode]): List of nodes to be added.
        **add_kwargs: Additional keyword arguments to be passed to the underlying storage.

    Returns:
        List[str]: List of node IDs that were added.

    """
    ids = []
    metadatas = []
    embeddings = []
    texts = []
    for node in nodes:
        ids.append(node.node_id)
        metadatas.append(node_to_metadata_dict(node, remove_text=True))
        embeddings.append(node.get_embedding())
        texts.append(node.get_content(metadata_mode=MetadataMode.NONE))

    self._tidb.insert(
        texts=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
        **add_kwargs,
    )

    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tidbvector/#llama_index.vector_stores.tidbvector.TiDBVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete all nodes of a document from the vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The reference document ID to be deleted.  |  _required_  |  
|  `**delete_kwargs`  |  Additional keyword arguments to be passed to the delete method.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `None`  |  None  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tidbvector/llama_index/vector_stores/tidbvector/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete all nodes of a document from the vector store.

    Args:
        ref_doc_id (str): The reference document ID to be deleted.
        **delete_kwargs: Additional keyword arguments to be passed to the delete method.

    Returns:
        None

    """
    delete_kwargs["filter"] = {"doc_id": ref_doc_id}
    self._tidb.delete(**delete_kwargs)

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tidbvector/#llama_index.vector_stores.tidbvector.TiDBVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Perform a similarity search with the given query embedding.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  The query object containing the query data.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  The result of the similarity search.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If the query embedding is not provided.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tidbvector/llama_index/vector_stores/tidbvector/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Perform a similarity search with the given query embedding.

    Args:
        query (VectorStoreQuery): The query object containing the query data.
        **kwargs: Additional keyword arguments.

    Returns:
        VectorStoreQueryResult: The result of the similarity search.

    Raises:
        ValueError: If the query embedding is not provided.

    """
    if query.query_embedding is None:
        raise ValueError("Query embedding must be provided.")
    return self._similarity_search_with_score(
        query.query_embedding,
        query.similarity_top_k,
        query.filters,
        **kwargs,
    )

```
 |  
| --- | --- |  
options: members: - TiDBVectorStore
