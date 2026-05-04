# Azurecosmosmongo
##  AzureCosmosDBMongoDBVectorSearch [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azurecosmosmongo/#llama_index.vector_stores.azurecosmosmongo.AzureCosmosDBMongoDBVectorSearch "Permanent link")
Bases: 
Azure CosmosDB MongoDB vCore Vector Store.
To use, you should have both: - the `pymongo` python package installed - a connection string associated with an Azure Cosmodb MongoDB vCore Cluster
Examples:
`pip install llama-index-vector-stores-azurecosmosmongo`

```
importpymongo
fromllama_index.vector_stores.azurecosmosmongoimport AzureCosmosDBMongoDBVectorSearch

# Set up the connection string with your Azure CosmosDB MongoDB URI
connection_string = "YOUR_AZURE_COSMOSDB_MONGODB_URI"
mongodb_client = pymongo.MongoClient(connection_string)

# Create an instance of AzureCosmosDBMongoDBVectorSearch
vector_store = AzureCosmosDBMongoDBVectorSearch(
    mongodb_client=mongodb_client,
    db_name="demo_vectordb",
    collection_name="paul_graham_essay",
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurecosmosmongo/llama_index/vector_stores/azurecosmosmongo/base.py`  
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
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
```
 | 
```
classAzureCosmosDBMongoDBVectorSearch(BasePydanticVectorStore):
"""
    Azure CosmosDB MongoDB vCore Vector Store.

    To use, you should have both:
    - the ``pymongo`` python package installed
    - a connection string associated with an Azure Cosmodb MongoDB vCore Cluster

    Examples:
        `pip install llama-index-vector-stores-azurecosmosmongo`

        ```python
        import pymongo
        from llama_index.vector_stores.azurecosmosmongo import AzureCosmosDBMongoDBVectorSearch

        # Set up the connection string with your Azure CosmosDB MongoDB URI
        connection_string = "YOUR_AZURE_COSMOSDB_MONGODB_URI"
        mongodb_client = pymongo.MongoClient(connection_string)

        # Create an instance of AzureCosmosDBMongoDBVectorSearch
        vector_store = AzureCosmosDBMongoDBVectorSearch(
            mongodb_client=mongodb_client,
            db_name="demo_vectordb",
            collection_name="paul_graham_essay",

        ```

    """

    stores_text: bool = True
    flat_metadata: bool = True

    _collection: Any = PrivateAttr()
    _index_name: str = PrivateAttr()
    _embedding_key: str = PrivateAttr()
    _id_key: str = PrivateAttr()
    _text_key: str = PrivateAttr()
    _metadata_key: str = PrivateAttr()
    _insert_kwargs: dict = PrivateAttr()
    _db_name: str = PrivateAttr()
    _collection_name: str = PrivateAttr()
    _cosmos_search_kwargs: dict = PrivateAttr()
    _mongodb_client: Any = PrivateAttr()

    def__init__(
        self,
        mongodb_client: Optional[Any] = None,
        db_name: str = "default_db",
        collection_name: str = "default_collection",
        index_name: str = "default_vector_search_index",
        id_key: str = "id",
        embedding_key: str = "content_vector",
        text_key: str = "text",
        metadata_key: str = "metadata",
        cosmos_search_kwargs: Optional[Dict] = None,
        insert_kwargs: Optional[Dict] = None,
        **kwargs: Any,
    ) -> None:
"""
        Initialize the vector store.

        Args:
            mongodb_client: An Azure CosmoDB MongoDB client (type: MongoClient, shown any for lazy import).
            db_name: An Azure CosmosDB MongoDB database name.
            collection_name: An Azure CosmosDB collection name.
            index_name: An Azure CosmosDB MongoDB vCore Vector Search index name.
            id_key: The data field to use as the id.
            embedding_key: An Azure CosmosDB MongoDB field that will contain
            the embedding for each document.
            text_key: An Azure CosmosDB MongoDB field that will contain the text for each document.
            metadata_key: An Azure CosmosDB MongoDB field that will contain
            the metadata for each document.
            cosmos_search_kwargs: An Azure CosmosDB MongoDB field that will
            contain search options, such as kind, numLists, similarity, and dimensions.
            insert_kwargs: The kwargs used during `insert`.

        """
        super().__init__()

        if mongodb_client is not None:
            self._mongodb_client = cast(pymongo.MongoClient, mongodb_client)
        else:
            if "AZURE_COSMOSDB_MONGODB_URI" not in os.environ:
                raise ValueError(
                    "Must specify Azure cosmodb 'AZURE_COSMOSDB_MONGODB_URI' via env variable "
                    "if not directly passing in client."
                )
            self._mongodb_client = pymongo.MongoClient(
                os.environ["AZURE_COSMOSDB_MONGODB_URI"],
                appname="LLAMAINDEX_PYTHON",
            )

        self._collection = self._mongodb_client[db_name][collection_name]
        self._index_name = index_name
        self._embedding_key = embedding_key
        self._id_key = id_key
        self._text_key = text_key
        self._metadata_key = metadata_key
        self._insert_kwargs = insert_kwargs or {}
        self._db_name = db_name
        self._collection_name = collection_name
        self._cosmos_search_kwargs = cosmos_search_kwargs or {}
        self._create_vector_search_index()

    def_create_vector_search_index(self) -> None:
        db = self._mongodb_client[self._db_name]

        create_index_commands = {}
        kind = self._cosmos_search_kwargs.get("kind", "vector-hnsw")

        if kind == "vector-ivf":
            create_index_commands = self._get_vector_index_ivf(kind)
        elif kind == "vector-hnsw":
            create_index_commands = self._get_vector_index_hnsw(kind)
        elif kind == "vector-diskann":
            create_index_commands = self._get_vector_index_diskann(kind)
        db.command(create_index_commands)

    def_get_vector_index_ivf(
        self,
        kind: str,
    ) -> Dict[str, Any]:
        indexes = {
            "name": self._index_name,
            "key": {self._embedding_key: "cosmosSearch"},
            "cosmosSearchOptions": {
                "kind": kind,
                "numLists": self._cosmos_search_kwargs.get("numLists", 1),
                "similarity": self._cosmos_search_kwargs.get("similarity", "COS"),
                "dimensions": self._cosmos_search_kwargs.get("dimensions", 1536),
            },
        }
        if self._cosmos_search_kwargs.get("compression", None) == "half":
            indexes["cosmosSearchOptions"]["compression"] = "half"
        return {
            "createIndexes": self._collection_name,
            "indexes": [indexes],
        }

    def_get_vector_index_hnsw(
        self,
        kind: str,
    ) -> Dict[str, Any]:
        indexes = {
            "name": self._index_name,
            "key": {self._embedding_key: "cosmosSearch"},
            "cosmosSearchOptions": {
                "kind": kind,
                "m": self._cosmos_search_kwargs.get("m", 2),
                "efConstruction": self._cosmos_search_kwargs.get("efConstruction", 64),
                "similarity": self._cosmos_search_kwargs.get("similarity", "COS"),
                "dimensions": self._cosmos_search_kwargs.get("dimensions", 1536),
            },
        }
        if self._cosmos_search_kwargs.get("compression", None) == "half":
            indexes["cosmosSearchOptions"]["compression"] = "half"
        return {
            "createIndexes": self._collection_name,
            "indexes": [indexes],
        }

    def_get_vector_index_diskann(
        self,
        kind: str,
    ) -> Dict[str, Any]:
        indexes = {
            "name": self._index_name,
            "key": {self._embedding_key: "cosmosSearch"},
            "cosmosSearchOptions": {
                "kind": kind,
                "maxDegree": self._cosmos_search_kwargs.get("maxDegree", 32),
                "lBuild": self._cosmos_search_kwargs.get("lBuild", 50),
                "similarity": self._cosmos_search_kwargs.get("similarity", "COS"),
                "dimensions": self._cosmos_search_kwargs.get("dimensions", 1536),
            },
        }
        if self._cosmos_search_kwargs.get("compression", None) == "pq":
            indexes["cosmosSearchOptions"]["compression"] = "pq"
            indexes["cosmosSearchOptions"]["pqCompressedDims"] = (
                self._cosmos_search_kwargs.get(
                    "pqCompressedDims",
                    self._cosmos_search_kwargs.get("dimensions", 1536),
                ),
            )
            indexes["cosmosSearchOptions"]["pqSampleSize"] = (
                self._cosmos_search_kwargs.get("pqSampleSize", 1000),
            )
        return {
            "createIndexes": self._collection_name,
            "indexes": [indexes],
        }

    defcreate_filter_index(
        self,
        property_to_filter: str,
        index_name: str,
    ) -> dict[str, Any]:
        db = self._mongodb_client[self._db_name]
        command = {
            "createIndexes": self._collection.name,
            "indexes": [
                {
                    "key": {property_to_filter: 1},
                    "name": index_name,
                }
            ],
        }

        create_index_responses: dict[str, Any] = db.command(command)
        return create_index_responses

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
        logger.debug("Inserting data into MongoDB: %s", data_to_insert)
        insert_result = self._collection.insert_many(
            data_to_insert, **self._insert_kwargs
        )
        logger.debug("Result of insert: %s", insert_result)
        return ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        # delete by filtering on the doc_id metadata
        self._collection.delete_one(
            filter={self._metadata_key + ".ref_doc_id": ref_doc_id}, **delete_kwargs
        )

    @property
    defclient(self) -> Any:
"""Return MongoDB client."""
        return self._mongodb_client

    def_query(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        pipeline: List[dict[str, Any]] = []
        kind = self._cosmos_search_kwargs.get("kind", "vector-hnsw")
        if kind == "vector-ivf":
            pipeline = self._get_pipeline_vector_ivf(
                query, kwargs.get("oversampling", 1.0), kwargs.get("pre_filter", {})
            )
        elif kind == "vector-hnsw":
            pipeline = self._get_pipeline_vector_hnsw(
                query,
                kwargs.get("ef_search", 40),
                kwargs.get("oversampling", 1.0),
                kwargs.get("pre_filter", {}),
            )
        elif kind == "vector-diskann":
            pipeline = self._get_pipeline_vector_diskann(
                query,
                kwargs.get("lSearch", 40),
                kwargs.get("oversampling", 1.0),
                kwargs.get("pre_filter", {}),
            )

        logger.debug("Running query pipeline: %s", pipeline)
        cursor = self._collection.aggregate(pipeline)  # type: ignore

        top_k_nodes = []
        top_k_ids = []
        top_k_scores = []
        for res in cursor:
            text = res["document"].pop(self._text_key)
            score = res.pop("similarityScore")
            id = res["document"].pop(self._id_key)
            metadata_dict = res["document"].pop(self._metadata_key)

            try:
                node = metadata_dict_to_node(metadata_dict)
                node.set_content(text)
            except Exception:
                # NOTE: deprecated legacy logic for backward compatibility
                metadata, node_info, relationships = legacy_metadata_dict_to_node(
                    metadata_dict
                )

                node = TextNode(
                    text=text,
                    id_=id,
                    metadata=metadata,
                    start_char_idx=node_info.get("start", None),
                    end_char_idx=node_info.get("end", None),
                    relationships=relationships,
                )
            top_k_ids.append(id)
            top_k_nodes.append(node)
            top_k_scores.append(score)
        result = VectorStoreQueryResult(
            nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
        )
        logger.debug("Result of query: %s", result)
        return result

    def_get_pipeline_vector_ivf(
        self, query: VectorStoreQuery, oversampling: float, pre_filter: Optional[Dict]
    ) -> List[dict[str, Any]]:
        params = {
            "vector": query.query_embedding,
            "path": self._embedding_key,
            "k": query.similarity_top_k,
            "oversampling": oversampling,
        }
        if pre_filter:
            params["filter"] = pre_filter

        pipeline: List[dict[str, Any]] = [
            {
                "$search": {
                    "cosmosSearch": params,
                    "returnStoredSource": True,
                }
            },
            {
                "$project": {
                    "similarityScore": {"$meta": "searchScore"},
                    "document": "$$ROOT",
                }
            },
        ]
        return pipeline

    def_get_pipeline_vector_hnsw(
        self,
        query: VectorStoreQuery,
        ef_search: int,
        oversampling: float,
        pre_filter: Optional[Dict],
    ) -> List[dict[str, Any]]:
        params = {
            "vector": query.query_embedding,
            "path": self._embedding_key,
            "k": query.similarity_top_k,
            "efSearch": ef_search,
            "oversampling": oversampling,
        }
        if pre_filter:
            params["filter"] = pre_filter

        pipeline: List[dict[str, Any]] = [
            {
                "$search": {
                    "cosmosSearch": params,
                }
            },
            {
                "$project": {
                    "similarityScore": {"$meta": "searchScore"},
                    "document": "$$ROOT",
                }
            },
        ]
        return pipeline

    def_get_pipeline_vector_diskann(
        self,
        query: VectorStoreQuery,
        l_search: int,
        oversampling: float,
        pre_filter: Optional[Dict],
    ) -> List[dict[str, Any]]:
        params = {
            "vector": query.query_embedding,
            "path": self._embedding_key,
            "k": query.similarity_top_k,
            "lSearch": l_search,
            "oversampling": oversampling,
        }
        if pre_filter:
            params["filter"] = pre_filter

        pipeline: List[dict[str, Any]] = [
            {
                "$search": {
                    "cosmosSearch": params,
                }
            },
            {
                "$project": {
                    "similarityScore": {"$meta": "searchScore"},
                    "document": "$$ROOT",
                }
            },
        ]
        return pipeline

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
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azurecosmosmongo/#llama_index.vector_stores.azurecosmosmongo.AzureCosmosDBMongoDBVectorSearch.client "Permanent link")

```
client: 

```

Return MongoDB client.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azurecosmosmongo/#llama_index.vector_stores.azurecosmosmongo.AzureCosmosDBMongoDBVectorSearch.add "Permanent link")

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
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurecosmosmongo/llama_index/vector_stores/azurecosmosmongo/base.py`  
| 
```
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
    logger.debug("Inserting data into MongoDB: %s", data_to_insert)
    insert_result = self._collection.insert_many(
        data_to_insert, **self._insert_kwargs
    )
    logger.debug("Result of insert: %s", insert_result)
    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azurecosmosmongo/#llama_index.vector_stores.azurecosmosmongo.AzureCosmosDBMongoDBVectorSearch.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurecosmosmongo/llama_index/vector_stores/azurecosmosmongo/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    # delete by filtering on the doc_id metadata
    self._collection.delete_one(
        filter={self._metadata_key + ".ref_doc_id": ref_doc_id}, **delete_kwargs
    )

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/azurecosmosmongo/#llama_index.vector_stores.azurecosmosmongo.AzureCosmosDBMongoDBVectorSearch.query "Permanent link")

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
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-azurecosmosmongo/llama_index/vector_stores/azurecosmosmongo/base.py`  
| 
```
447
448
449
450
451
452
453
454
455
456
457
458
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
