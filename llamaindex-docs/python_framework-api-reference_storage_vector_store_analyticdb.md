# Analyticdb
##  AnalyticDBVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/analyticdb/#llama_index.vector_stores.analyticdb.AnalyticDBVectorStore "Permanent link")
Bases: 
AnalyticDB vector store.
In this vector store, embeddings and docs are stored within a single table.
During query time, the index uses AnalyticDB to query for the top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `region_id`  |  _required_  |  
|  `instance_id`  |  _required_  |  
|  `account`  |  _required_  |  
|  `account_password`  |  _required_  |  
|  `namespace`  |  `'llama_index'`  |  
|  `namespace_password`  |  `None`  |  
|  `embedding_dimension`  |  `1536`  |  
|  `metrics`  |  `'cosine'`  |  
|  `collection`  |  `'llama_collection'`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-analyticdb/llama_index/vector_stores/analyticdb/base.py`  
| 
```
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
```
 | 
```
classAnalyticDBVectorStore(BasePydanticVectorStore):
"""
    AnalyticDB vector store.

    In this vector store, embeddings and docs are stored within a
    single table.

    During query time, the index uses AnalyticDB to query for the top
    k most similar nodes.

    Args:
        region_id: str
        instance_id: str
        account: str
        account_password: str
        namespace: str
        namespace_password: str
        embedding_dimension: int
        metrics: str
        collection: str

    """

    stores_text: bool = True
    flat_metadata: bool = False

    region_id: str
    instance_id: str
    account: str
    account_password: str
    namespace: str
    namespace_password: str
    embedding_dimension: int
    metrics: str
    collection: str

    _client: Any = PrivateAttr()
    _is_initialized: bool = PrivateAttr(default=False)

    def__init__(
        self,
        client: Any,
        region_id: str,
        instance_id: str,
        account: str,
        account_password: str,
        namespace: str = "llama_index",
        collection: str = "llama_collection",
        namespace_password: str = None,
        embedding_dimension: int = 1536,
        metrics: str = "cosine",
    ):
        try:
            fromalibabacloud_gpdb20160503.clientimport Client
        except ImportError:
            raise ImportError(_import_err_msg)

        if client is not None:
            if not isinstance(client, Client):
                raise ValueError(
                    "client must be of type alibabacloud_gpdb20160503.client.Client"
                )
        else:
            raise ValueError("client not specified")
        if not namespace_password:
            namespace_password = account_password
        super().__init__(
            region_id=region_id,
            instance_id=instance_id,
            account=account,
            account_password=account_password,
            namespace=namespace,
            collection=collection,
            namespace_password=namespace_password,
            embedding_dimension=embedding_dimension,
            metrics=metrics,
        )
        self._client = client

    @classmethod
    def_initialize_client(
        cls,
        access_key_id: str,
        access_key_secret: str,
        region_id: str,
        read_timeout: int = 60000,
    ) -> Any:
"""
        Initialize ADB client.
        """
        try:
            fromalibabacloud_gpdb20160503.clientimport Client
            fromalibabacloud_tea_openapiimport models as open_api_models
        except ImportError:
            raise ImportError(_import_err_msg)

        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            region_id=region_id,
            read_timeout=read_timeout,
            user_agent="llama-index",
        )
        return Client(config)

    @classmethod
    deffrom_params(
        cls,
        access_key_id: str,
        access_key_secret: str,
        region_id: str,
        instance_id: str,
        account: str,
        account_password: str,
        namespace: str = "llama_index",
        collection: str = "llama_collection",
        namespace_password: str = None,
        embedding_dimension: int = 1536,
        metrics: str = "cosine",
        read_timeout: int = 60000,
    ) -> "AnalyticDBVectorStore":
        client = cls._initialize_client(
            access_key_id, access_key_secret, region_id, read_timeout
        )
        return cls(
            client=client,
            region_id=region_id,
            instance_id=instance_id,
            account=account,
            account_password=account_password,
            namespace=namespace,
            collection=collection,
            namespace_password=namespace_password,
            embedding_dimension=embedding_dimension,
            metrics=metrics,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "AnalyticDBVectorStore"

    @property
    defclient(self) -> Any:
        return self._client

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
        Add nodes to the vector store.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        """
        fromalibabacloud_gpdb20160503import models as gpdb_20160503_models

        self._initialize()
        ids = []
        rows: List[gpdb_20160503_models.UpsertCollectionDataRequestRows] = []
        for node in nodes:
            ids.append(node.node_id)
            node_metadata_dict = node_to_metadata_dict(
                node,
                remove_text=True,
                flat_metadata=self.flat_metadata,
            )
            metadata = {
                "node_id": node.node_id,
                "ref_doc_id": node.ref_doc_id,
                "content": node.get_content(metadata_mode=MetadataMode.NONE),
                "metadata_": json.dumps(node_metadata_dict),
            }
            rows.append(
                gpdb_20160503_models.UpsertCollectionDataRequestRows(
                    vector=node.get_embedding(),
                    metadata=metadata,
                )
            )
        _logger.debug("adding nodes to vector store...")
        request = gpdb_20160503_models.UpsertCollectionDataRequest(
            dbinstance_id=self.instance_id,
            region_id=self.region_id,
            namespace=self.namespace,
            namespace_password=self.namespace_password,
            collection=self.collection,
            rows=rows,
        )
        response = self._client.upsert_collection_data(request)
        _logger.info(
            f"successfully adding nodes to vector store, size: {len(nodes)},"
            f"response body:{response.body}"
        )
        return ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete a node from the vector store.

        Args:
            ref_doc_id: str: the doc_id of the document to delete.

        """
        fromalibabacloud_gpdb20160503import models as gpdb_20160503_models

        self._initialize()
        collection_data = '{"ref_doc_id": ["%s"]}' % ref_doc_id
        request = gpdb_20160503_models.DeleteCollectionDataRequest(
            dbinstance_id=self.instance_id,
            region_id=self.region_id,
            namespace=self.namespace,
            namespace_password=self.namespace_password,
            collection=self.collection,
            collection_data=collection_data,
        )
        _logger.debug(f"deleting nodes from vector store of ref_doc_id: {ref_doc_id}")
        response = self._client.delete_collection_data(request)
        _logger.info(
            f"successfully delete nodes from vector store, response body: {response.body}"
        )

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query the vector store for top k most similar nodes.

        Args:
            query: VectorStoreQuery: the query to execute.

        Returns:
            VectorStoreQueryResult: the result of the query.

        """
        fromalibabacloud_gpdb20160503import models as gpdb_20160503_models

        self._initialize()
        vector = (
            query.query_embedding
            if query.mode in (VectorStoreQueryMode.DEFAULT, VectorStoreQueryMode.HYBRID)
            else None
        )
        content = (
            query.query_str
            if query.mode in (VectorStoreQueryMode.SPARSE, VectorStoreQueryMode.HYBRID)
            else None
        )
        request = gpdb_20160503_models.QueryCollectionDataRequest(
            dbinstance_id=self.instance_id,
            region_id=self.region_id,
            namespace=self.namespace,
            namespace_password=self.namespace_password,
            collection=self.collection,
            include_values=kwargs.pop("include_values", True),
            metrics=self.metrics,
            vector=vector,
            content=content,
            top_k=query.similarity_top_k,
            filter=_recursively_parse_adb_filter(query.filters),
        )
        response = self._client.query_collection_data(request)
        nodes = []
        similarities = []
        ids = []
        for match in response.body.matches.match:
            node = metadata_dict_to_node(
                json.loads(match.metadata.get("metadata_")),
                match.metadata.get("content"),
            )
            nodes.append(node)
            similarities.append(match.score)
            ids.append(match.metadata.get("node_id"))
        return VectorStoreQueryResult(
            nodes=nodes,
            similarities=similarities,
            ids=ids,
        )

    defdelete_collection(self):
        fromalibabacloud_gpdb20160503import models as gpdb_20160503_models

        request = gpdb_20160503_models.DeleteCollectionRequest(
            dbinstance_id=self.instance_id,
            region_id=self.region_id,
            namespace=self.namespace,
            namespace_password=self.namespace_password,
            collection=self.collection,
        )
        self._client.delete_collection(request)
        _logger.debug(f"collection {self.collection} deleted")

    def_initialize(self) -> None:
        if not self._is_initialized:
            self._initialize_vector_database()
            self._create_namespace_if_not_exists()
            self._create_collection_if_not_exists()
            self._is_initialized = True

    def_initialize_vector_database(self):
        fromalibabacloud_gpdb20160503import models as gpdb_20160503_models

        request = gpdb_20160503_models.InitVectorDatabaseRequest(
            dbinstance_id=self.instance_id,
            region_id=self.region_id,
            manager_account=self.account,
            manager_account_password=self.account_password,
        )
        response = self._client.init_vector_database(request)
        _logger.debug(
            f"successfully initialize vector database, response body:{response.body}"
        )

    def_create_namespace_if_not_exists(self):
        fromalibabacloud_gpdb20160503import models as gpdb_20160503_models
        fromTea.exceptionsimport TeaException

        try:
            request = gpdb_20160503_models.DescribeNamespaceRequest(
                dbinstance_id=self.instance_id,
                region_id=self.region_id,
                namespace=self.namespace,
                manager_account=self.account,
                manager_account_password=self.account_password,
            )
            self._client.describe_namespace(request)
            _logger.debug(f"namespace {self.namespace} already exists")
        except TeaException as e:
            if e.statusCode == 404:
                _logger.debug(f"namespace {self.namespace} does not exist, creating...")
                request = gpdb_20160503_models.CreateNamespaceRequest(
                    dbinstance_id=self.instance_id,
                    region_id=self.region_id,
                    manager_account=self.account,
                    manager_account_password=self.account_password,
                    namespace=self.namespace,
                    namespace_password=self.namespace_password,
                )
                self._client.create_namespace(request)
                _logger.debug(f"namespace {self.namespace} created")
            else:
                raise ValueError(f"failed to create namespace {self.namespace}: {e}")

    def_create_collection_if_not_exists(self):
        fromalibabacloud_gpdb20160503import models as gpdb_20160503_models
        fromTea.exceptionsimport TeaException

        try:
            request = gpdb_20160503_models.DescribeCollectionRequest(
                dbinstance_id=self.instance_id,
                region_id=self.region_id,
                namespace=self.namespace,
                namespace_password=self.namespace_password,
                collection=self.collection,
            )
            self._client.describe_collection(request)
            _logger.debug(f"collection {self.collection} already exists")
        except TeaException as e:
            if e.statusCode == 404:
                _logger.debug(
                    f"collection {self.namespace} does not exist, creating..."
                )
                metadata = '{"node_id":"text","ref_doc_id":"text","content":"text","metadata_":"jsonb"}'
                full_text_retrieval_fields = "content"
                request = gpdb_20160503_models.CreateCollectionRequest(
                    dbinstance_id=self.instance_id,
                    region_id=self.region_id,
                    manager_account=self.account,
                    manager_account_password=self.account_password,
                    namespace=self.namespace,
                    collection=self.collection,
                    dimension=self.embedding_dimension,
                    metrics=self.metrics,
                    metadata=metadata,
                    full_text_retrieval_fields=full_text_retrieval_fields,
                )
                self._client.create_collection(request)
                _logger.debug(f"collection {self.namespace} created")
            else:
                raise ValueError(f"failed to create collection {self.collection}: {e}")

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/analyticdb/#llama_index.vector_stores.analyticdb.AnalyticDBVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to the vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-analyticdb/llama_index/vector_stores/analyticdb/base.py`  
| 
```
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
```
 | 
```
defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
    Add nodes to the vector store.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings

    """
    fromalibabacloud_gpdb20160503import models as gpdb_20160503_models

    self._initialize()
    ids = []
    rows: List[gpdb_20160503_models.UpsertCollectionDataRequestRows] = []
    for node in nodes:
        ids.append(node.node_id)
        node_metadata_dict = node_to_metadata_dict(
            node,
            remove_text=True,
            flat_metadata=self.flat_metadata,
        )
        metadata = {
            "node_id": node.node_id,
            "ref_doc_id": node.ref_doc_id,
            "content": node.get_content(metadata_mode=MetadataMode.NONE),
            "metadata_": json.dumps(node_metadata_dict),
        }
        rows.append(
            gpdb_20160503_models.UpsertCollectionDataRequestRows(
                vector=node.get_embedding(),
                metadata=metadata,
            )
        )
    _logger.debug("adding nodes to vector store...")
    request = gpdb_20160503_models.UpsertCollectionDataRequest(
        dbinstance_id=self.instance_id,
        region_id=self.region_id,
        namespace=self.namespace,
        namespace_password=self.namespace_password,
        collection=self.collection,
        rows=rows,
    )
    response = self._client.upsert_collection_data(request)
    _logger.info(
        f"successfully adding nodes to vector store, size: {len(nodes)},"
        f"response body:{response.body}"
    )
    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/analyticdb/#llama_index.vector_stores.analyticdb.AnalyticDBVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete a node from the vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  str: the doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-analyticdb/llama_index/vector_stores/analyticdb/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete a node from the vector store.

    Args:
        ref_doc_id: str: the doc_id of the document to delete.

    """
    fromalibabacloud_gpdb20160503import models as gpdb_20160503_models

    self._initialize()
    collection_data = '{"ref_doc_id": ["%s"]}' % ref_doc_id
    request = gpdb_20160503_models.DeleteCollectionDataRequest(
        dbinstance_id=self.instance_id,
        region_id=self.region_id,
        namespace=self.namespace,
        namespace_password=self.namespace_password,
        collection=self.collection,
        collection_data=collection_data,
    )
    _logger.debug(f"deleting nodes from vector store of ref_doc_id: {ref_doc_id}")
    response = self._client.delete_collection_data(request)
    _logger.info(
        f"successfully delete nodes from vector store, response body: {response.body}"
    )

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/analyticdb/#llama_index.vector_stores.analyticdb.AnalyticDBVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query the vector store for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  VectorStoreQuery: the query to execute.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  the result of the query.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-analyticdb/llama_index/vector_stores/analyticdb/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query the vector store for top k most similar nodes.

    Args:
        query: VectorStoreQuery: the query to execute.

    Returns:
        VectorStoreQueryResult: the result of the query.

    """
    fromalibabacloud_gpdb20160503import models as gpdb_20160503_models

    self._initialize()
    vector = (
        query.query_embedding
        if query.mode in (VectorStoreQueryMode.DEFAULT, VectorStoreQueryMode.HYBRID)
        else None
    )
    content = (
        query.query_str
        if query.mode in (VectorStoreQueryMode.SPARSE, VectorStoreQueryMode.HYBRID)
        else None
    )
    request = gpdb_20160503_models.QueryCollectionDataRequest(
        dbinstance_id=self.instance_id,
        region_id=self.region_id,
        namespace=self.namespace,
        namespace_password=self.namespace_password,
        collection=self.collection,
        include_values=kwargs.pop("include_values", True),
        metrics=self.metrics,
        vector=vector,
        content=content,
        top_k=query.similarity_top_k,
        filter=_recursively_parse_adb_filter(query.filters),
    )
    response = self._client.query_collection_data(request)
    nodes = []
    similarities = []
    ids = []
    for match in response.body.matches.match:
        node = metadata_dict_to_node(
            json.loads(match.metadata.get("metadata_")),
            match.metadata.get("content"),
        )
        nodes.append(node)
        similarities.append(match.score)
        ids.append(match.metadata.get("node_id"))
    return VectorStoreQueryResult(
        nodes=nodes,
        similarities=similarities,
        ids=ids,
    )

```
 |  
| --- | --- |  
options: members: - AnalyticDBVectorStore
