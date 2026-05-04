# Azurecosmosnosql
##  AzureCosmosDBNoSqlVectorSearch [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azurecosmosnosql/#llama_index.vector_stores.azurecosmosnosql.AzureCosmosDBNoSqlVectorSearch "Permanent link")
Bases: 
Azure CosmosDB NoSQL vCore Vector Store.
To use, you should have both: -the `azure-cosmos` python package installed -from llama_index.vector_stores.azurecosmosnosql import AzureCosmosDBNoSqlVectorSearch
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurecosmosnosql/llama_index/vector_stores/azurecosmosnosql/base.py`  
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
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
```
 | 
```
classAzureCosmosDBNoSqlVectorSearch(BasePydanticVectorStore):
"""
    Azure CosmosDB NoSQL vCore Vector Store.

    To use, you should have both:
    -the ``azure-cosmos`` python package installed
    -from llama_index.vector_stores.azurecosmosnosql import AzureCosmosDBNoSqlVectorSearch
    """

    stores_text: bool = True
    flat_metadata: bool = True

    _cosmos_client: Any = PrivateAttr()
    _database_name: Any = PrivateAttr()
    _container_name: Any = PrivateAttr()
    _embedding_key: Any = PrivateAttr()
    _vector_embedding_policy: Any = PrivateAttr()
    _indexing_policy: Any = PrivateAttr()
    _cosmos_container_properties: Any = PrivateAttr()
    _cosmos_database_properties: Any = PrivateAttr()
    _create_container: Any = PrivateAttr()
    _database: Any = PrivateAttr()
    _container: Any = PrivateAttr()
    _id_key: Any = PrivateAttr()
    _text_key: Any = PrivateAttr()
    _metadata_key: Any = PrivateAttr()

    def__init__(
        self,
        cosmos_client: CosmosClient,
        vector_embedding_policy: Dict[str, Any],
        indexing_policy: Dict[str, Any],
        cosmos_container_properties: Dict[str, Any],
        cosmos_database_properties: Optional[Dict[str, Any]] = None,
        database_name: str = "vectorSearchDB",
        container_name: str = "vectorSearchContainer",
        create_container: bool = True,
        id_key: str = "id",
        text_key: str = "text",
        metadata_key: str = "metadata",
        **kwargs: Any,
    ) -> None:
"""
        Initialize the vector store.

        Args:
            cosmos_client: Client used to connect to azure cosmosdb no sql account.
            database_name: Name of the database to be created.
            container_name: Name of the container to be created.
            embedding: Text embedding model to use.
            vector_embedding_policy: Vector Embedding Policy for the container.
            indexing_policy: Indexing Policy for the container.
            cosmos_container_properties: Container Properties for the container.
            cosmos_database_properties: Database Properties for the container.

        """
        super().__init__()

        if cosmos_client is not None:
            self._cosmos_client = cast(CosmosClient, cosmos_client)

        if create_container:
            if (
                indexing_policy["vectorIndexes"] is None
                or len(indexing_policy["vectorIndexes"]) == 0
            ):
                raise ValueError(
                    "vectorIndexes cannot be null or empty in the indexing_policy."
                )
            if (
                vector_embedding_policy is None
                or len(vector_embedding_policy["vectorEmbeddings"]) == 0
            ):
                raise ValueError(
                    "vectorEmbeddings cannot be null "
                    "or empty in the vector_embedding_policy."
                )
            if (
                cosmos_container_properties is None
                or cosmos_container_properties["partition_key"] is None
            ):
                raise ValueError(
                    "partition_key cannot be null or empty for a container."
                )

        self._database_name = database_name
        self._container_name = container_name
        self._vector_embedding_policy = vector_embedding_policy
        self._indexing_policy = indexing_policy
        self._cosmos_container_properties = cosmos_container_properties
        self._cosmos_database_properties = cosmos_database_properties
        self._id_key = id_key
        self._text_key = text_key
        self._metadata_key = metadata_key
        self._embedding_key = self._vector_embedding_policy["vectorEmbeddings"][0][
            "path"
        ][1:]

        self._database = self._cosmos_client.create_database_if_not_exists(
            id=self._database_name,
            offer_throughput=self._cosmos_database_properties.get("offer_throughput"),
            session_token=self._cosmos_database_properties.get("session_token"),
            initial_headers=self._cosmos_database_properties.get("initial_headers"),
            etag=self._cosmos_database_properties.get("etag"),
            match_condition=self._cosmos_database_properties.get("match_condition"),
        )

        # Create the collection if it already doesn't exist
        self._container = self._database.create_container_if_not_exists(
            id=self._container_name,
            partition_key=self._cosmos_container_properties["partition_key"],
            indexing_policy=self._indexing_policy,
            default_ttl=self._cosmos_container_properties.get("default_ttl"),
            offer_throughput=self._cosmos_container_properties.get("offer_throughput"),
            unique_key_policy=self._cosmos_container_properties.get(
                "unique_key_policy"
            ),
            conflict_resolution_policy=self._cosmos_container_properties.get(
                "conflict_resolution_policy"
            ),
            analytical_storage_ttl=self._cosmos_container_properties.get(
                "analytical_storage_ttl"
            ),
            computed_properties=self._cosmos_container_properties.get(
                "computed_properties"
            ),
            etag=self._cosmos_container_properties.get("etag"),
            match_condition=self._cosmos_container_properties.get("match_condition"),
            session_token=self._cosmos_container_properties.get("session_token"),
            initial_headers=self._cosmos_container_properties.get("initial_headers"),
            vector_embedding_policy=self._vector_embedding_policy,
        )

    @classmethod
    deffrom_host_and_key(
        cls,
        host: str,
        key: str,
        vector_embedding_policy: Dict[str, Any],
        indexing_policy: Dict[str, Any],
        cosmos_container_properties: Dict[str, Any],
        cosmos_database_properties: Optional[Dict[str, Any]] = None,
        database_name: str = "vectorSearchDB",
        container_name: str = "vectorSearchContainer",
        create_container: bool = True,
        id_key: str = "id",
        text_key: str = "text",
        metadata_key: str = "metadata",
        **kwargs: Any,
    ) -> "AzureCosmosDBNoSqlVectorSearch":
"""Initialize the vector store using the cosmosDB host and key."""
        cosmos_client = CosmosClient(host, key, user_agent=USER_AGENT)
        return cls(
            cosmos_client,
            vector_embedding_policy,
            indexing_policy,
            cosmos_container_properties,
            cosmos_database_properties,
            database_name,
            container_name,
            create_container,
            id_key,
            text_key,
            metadata_key,
            **kwargs,
        )

    @classmethod
    deffrom_connection_string(
        cls,
        connection_string: str,
        vector_embedding_policy: Dict[str, Any],
        indexing_policy: Dict[str, Any],
        cosmos_container_properties: Dict[str, Any],
        cosmos_database_properties: Optional[Dict[str, Any]] = None,
        database_name: str = "vectorSearchDB",
        container_name: str = "vectorSearchContainer",
        create_container: bool = True,
        id_key: str = "id",
        text_key: str = "text",
        metadata_key: str = "metadata",
        **kwargs: Any,
    ) -> "AzureCosmosDBNoSqlVectorSearch":
"""Initialize the vector store using the cosmosDB connection string."""
        cosmos_client = CosmosClient.from_connection_string(
            connection_string, user_agent=USER_AGENT
        )
        return cls(
            cosmos_client,
            vector_embedding_policy,
            indexing_policy,
            cosmos_container_properties,
            cosmos_database_properties,
            database_name,
            container_name,
            create_container,
            id_key,
            text_key,
            metadata_key,
            **kwargs,
        )

    @classmethod
    deffrom_uri_and_managed_identity(
        cls,
        cosmos_uri: str,
        vector_embedding_policy: Dict[str, Any],
        indexing_policy: Dict[str, Any],
        cosmos_container_properties: Dict[str, Any],
        cosmos_database_properties: Optional[Dict[str, Any]] = None,
        database_name: str = "vectorSearchDB",
        container_name: str = "vectorSearchContainer",
        create_container: bool = True,
        id_key: str = "id",
        text_key: str = "text",
        metadata_key: str = "metadata",
        **kwargs: Any,
    ) -> "AzureCosmosDBNoSqlVectorSearch":
"""Initialize the vector store using the cosmosDB uri and managed identity."""
        cosmos_client = CosmosClient(
            cosmos_uri, ClientSecretCredential, user_agent=USER_AGENT
        )
        return cls(
            cosmos_client,
            vector_embedding_policy,
            indexing_policy,
            cosmos_container_properties,
            cosmos_database_properties,
            database_name,
            container_name,
            create_container,
            id_key,
            text_key,
            metadata_key,
            **kwargs,
        )

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to index.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        Returns:
            A List of ids for successfully added nodes.

        """
        ids = []
        data_to_insert = []

        if not nodes:
            raise Exception("Texts can not be null or empty")

        for node in nodes:
            metadata = node_to_metadata_dict(
                node, remove_text=True, flat_metadata=self.flat_metadata
            )

            entry = {
                self._id_key: node.node_id,
                self._embedding_key: node.get_embedding(),
                self._text_key: node.get_content(metadata_mode=MetadataMode.NONE) or "",
                self._metadata_key: metadata,
            }
            data_to_insert.append(entry)
            ids.append(node.node_id)

        for item in data_to_insert:
            self._container.upsert_item(item)

        return ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        items = self._container.query_items(
            query=f"SELECT c.id, c.id AS partitionKey FROM c WHERE c.{self._metadata_key}.ref_doc_id = '{ref_doc_id}'",
            enable_cross_partition_query=True,
        )
        for item in items:
            self._container.delete_item(item["id"], partition_key=item["partitionKey"])

    @property
    defclient(self) -> Any:
"""Return CosmosDB client."""
        return self._cosmos_client

    def_query(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        params: Dict[str, Any] = {
            "vector": query.query_embedding,
            "path": self._embedding_key,
            "k": query.similarity_top_k,
        }

        pre_filter = kwargs.get("pre_filter", {})

        query = "SELECT "

        # If limit_offset_clause is not specified, add TOP clause
        if pre_filter is None or pre_filter.get("limit_offset_clause") is None:
            query += f"TOP {params.get('k',2)} "

        query += (
            "c.id, c.text, c.metadata, "
            f"VectorDistance(c.{self._embedding_key}, @embeddings) AS SimilarityScore FROM c"
        )

        # Add where_clause if specified
        if pre_filter is not None and pre_filter.get("where_clause") is not None:
            query += " {}".format(pre_filter["where_clause"])

        query += f" ORDER BY VectorDistance(c.{self._embedding_key}, @embeddings)"

        # Add limit_offset_clause if specified
        if pre_filter is not None and pre_filter.get("limit_offset_clause") is not None:
            query += " {}".format(pre_filter["limit_offset_clause"])
        parameters = [
            {"name": "@embeddings", "value": params["vector"]},
        ]

        top_k_nodes = []
        top_k_ids = []
        top_k_scores = []

        for item in self._container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True,
        ):
            node = metadata_dict_to_node(item[self._metadata_key])
            node.set_content(item[self._text_key])

            node_id = item[self._id_key]
            node_score = item["SimilarityScore"]

            top_k_ids.append(node_id)
            top_k_nodes.append(node)
            top_k_scores.append(node_score)

        return VectorStoreQueryResult(
            nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
        )

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query: a VectorStoreQuery object.

        Returns:
            A VectorStoreQueryResult containing the results of the query.

        """
        return self._query(query, **kwargs)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azurecosmosnosql/#llama_index.vector_stores.azurecosmosnosql.AzureCosmosDBNoSqlVectorSearch.client "Permanent link")

```
client: 

```

Return CosmosDB client.
###  from_host_and_key `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azurecosmosnosql/#llama_index.vector_stores.azurecosmosnosql.AzureCosmosDBNoSqlVectorSearch.from_host_and_key "Permanent link")

```
from_host_and_key(
    host: ,
    key: ,
    vector_embedding_policy: [, ],
    indexing_policy: [, ],
    cosmos_container_properties: [, ],
    cosmos_database_properties: Optional[
        [, ]
    ] = None,
    database_name:  = "vectorSearchDB",
    container_name:  = "vectorSearchContainer",
    create_container:  = True,
    id_key:  = "id",
    text_key:  = "text",
    metadata_key:  = "metadata",
    **kwargs: 
) -> 

```

Initialize the vector store using the cosmosDB host and key.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurecosmosnosql/llama_index/vector_stores/azurecosmosnosql/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_host_and_key(
    cls,
    host: str,
    key: str,
    vector_embedding_policy: Dict[str, Any],
    indexing_policy: Dict[str, Any],
    cosmos_container_properties: Dict[str, Any],
    cosmos_database_properties: Optional[Dict[str, Any]] = None,
    database_name: str = "vectorSearchDB",
    container_name: str = "vectorSearchContainer",
    create_container: bool = True,
    id_key: str = "id",
    text_key: str = "text",
    metadata_key: str = "metadata",
    **kwargs: Any,
) -> "AzureCosmosDBNoSqlVectorSearch":
"""Initialize the vector store using the cosmosDB host and key."""
    cosmos_client = CosmosClient(host, key, user_agent=USER_AGENT)
    return cls(
        cosmos_client,
        vector_embedding_policy,
        indexing_policy,
        cosmos_container_properties,
        cosmos_database_properties,
        database_name,
        container_name,
        create_container,
        id_key,
        text_key,
        metadata_key,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  from_connection_string `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azurecosmosnosql/#llama_index.vector_stores.azurecosmosnosql.AzureCosmosDBNoSqlVectorSearch.from_connection_string "Permanent link")

```
from_connection_string(
    connection_string: ,
    vector_embedding_policy: [, ],
    indexing_policy: [, ],
    cosmos_container_properties: [, ],
    cosmos_database_properties: Optional[
        [, ]
    ] = None,
    database_name:  = "vectorSearchDB",
    container_name:  = "vectorSearchContainer",
    create_container:  = True,
    id_key:  = "id",
    text_key:  = "text",
    metadata_key:  = "metadata",
    **kwargs: 
) -> 

```

Initialize the vector store using the cosmosDB connection string.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurecosmosnosql/llama_index/vector_stores/azurecosmosnosql/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_connection_string(
    cls,
    connection_string: str,
    vector_embedding_policy: Dict[str, Any],
    indexing_policy: Dict[str, Any],
    cosmos_container_properties: Dict[str, Any],
    cosmos_database_properties: Optional[Dict[str, Any]] = None,
    database_name: str = "vectorSearchDB",
    container_name: str = "vectorSearchContainer",
    create_container: bool = True,
    id_key: str = "id",
    text_key: str = "text",
    metadata_key: str = "metadata",
    **kwargs: Any,
) -> "AzureCosmosDBNoSqlVectorSearch":
"""Initialize the vector store using the cosmosDB connection string."""
    cosmos_client = CosmosClient.from_connection_string(
        connection_string, user_agent=USER_AGENT
    )
    return cls(
        cosmos_client,
        vector_embedding_policy,
        indexing_policy,
        cosmos_container_properties,
        cosmos_database_properties,
        database_name,
        container_name,
        create_container,
        id_key,
        text_key,
        metadata_key,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  from_uri_and_managed_identity `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azurecosmosnosql/#llama_index.vector_stores.azurecosmosnosql.AzureCosmosDBNoSqlVectorSearch.from_uri_and_managed_identity "Permanent link")

```
from_uri_and_managed_identity(
    cosmos_uri: ,
    vector_embedding_policy: [, ],
    indexing_policy: [, ],
    cosmos_container_properties: [, ],
    cosmos_database_properties: Optional[
        [, ]
    ] = None,
    database_name:  = "vectorSearchDB",
    container_name:  = "vectorSearchContainer",
    create_container:  = True,
    id_key:  = "id",
    text_key:  = "text",
    metadata_key:  = "metadata",
    **kwargs: 
) -> 

```

Initialize the vector store using the cosmosDB uri and managed identity.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurecosmosnosql/llama_index/vector_stores/azurecosmosnosql/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_uri_and_managed_identity(
    cls,
    cosmos_uri: str,
    vector_embedding_policy: Dict[str, Any],
    indexing_policy: Dict[str, Any],
    cosmos_container_properties: Dict[str, Any],
    cosmos_database_properties: Optional[Dict[str, Any]] = None,
    database_name: str = "vectorSearchDB",
    container_name: str = "vectorSearchContainer",
    create_container: bool = True,
    id_key: str = "id",
    text_key: str = "text",
    metadata_key: str = "metadata",
    **kwargs: Any,
) -> "AzureCosmosDBNoSqlVectorSearch":
"""Initialize the vector store using the cosmosDB uri and managed identity."""
    cosmos_client = CosmosClient(
        cosmos_uri, ClientSecretCredential, user_agent=USER_AGENT
    )
    return cls(
        cosmos_client,
        vector_embedding_policy,
        indexing_policy,
        cosmos_container_properties,
        cosmos_database_properties,
        database_name,
        container_name,
        create_container,
        id_key,
        text_key,
        metadata_key,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azurecosmosnosql/#llama_index.vector_stores.azurecosmosnosql.AzureCosmosDBNoSqlVectorSearch.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  A List of ids for successfully added nodes.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurecosmosnosql/llama_index/vector_stores/azurecosmosnosql/base.py`  
| 
```
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
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
```
 | 
```
defadd(
    self,
    nodes: List[BaseNode],
    **add_kwargs: Any,
) -> List[str]:
"""
    Add nodes to index.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings

    Returns:
        A List of ids for successfully added nodes.

    """
    ids = []
    data_to_insert = []

    if not nodes:
        raise Exception("Texts can not be null or empty")

    for node in nodes:
        metadata = node_to_metadata_dict(
            node, remove_text=True, flat_metadata=self.flat_metadata
        )

        entry = {
            self._id_key: node.node_id,
            self._embedding_key: node.get_embedding(),
            self._text_key: node.get_content(metadata_mode=MetadataMode.NONE) or "",
            self._metadata_key: metadata,
        }
        data_to_insert.append(entry)
        ids.append(node.node_id)

    for item in data_to_insert:
        self._container.upsert_item(item)

    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azurecosmosnosql/#llama_index.vector_stores.azurecosmosnosql.AzureCosmosDBNoSqlVectorSearch.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurecosmosnosql/llama_index/vector_stores/azurecosmosnosql/base.py`  
| 
```
306
307
308
309
310
311
312
313
314
315
316
317
318
319
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    items = self._container.query_items(
        query=f"SELECT c.id, c.id AS partitionKey FROM c WHERE c.{self._metadata_key}.ref_doc_id = '{ref_doc_id}'",
        enable_cross_partition_query=True,
    )
    for item in items:
        self._container.delete_item(item["id"], partition_key=item["partitionKey"])

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azurecosmosnosql/#llama_index.vector_stores.azurecosmosnosql.AzureCosmosDBNoSqlVectorSearch.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  a VectorStoreQuery object.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  A VectorStoreQueryResult containing the results of the query.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurecosmosnosql/llama_index/vector_stores/azurecosmosnosql/base.py`  
| 
```
382
383
384
385
386
387
388
389
390
391
392
393
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query: a VectorStoreQuery object.

    Returns:
        A VectorStoreQueryResult containing the results of the query.

    """
    return self._query(query, **kwargs)

```
 |  
| --- | --- |  
options: members: - AzureCosmosDBMongoDBVectorSearch
