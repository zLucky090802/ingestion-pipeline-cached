# Tencentvectordb
##  TencentVectorDB [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tencentvectordb/#llama_index.vector_stores.tencentvectordb.TencentVectorDB "Permanent link")
Bases: 
Tencent Vector Store.
In this vector store, embeddings and docs are stored within a Collection. If the Collection does not exist, it will be automatically created.
In order to use this you need to have a database instance. See the following documentation for details: https://cloud.tencent.com/document/product/1709/94951
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url`  |  `Optional[str]`  |  url of Tencent vector database  |  _required_  |  
|  `username`  |  `Optional[str]`  |  The username for Tencent vector database. Default value is "root"  |  `DEFAULT_USERNAME`  |  
|  `key`  |  `Optional[str]`  |  The Api-Key for Tencent vector database  |  _required_  |  
|  `collection_params`  |  `Optional[CollectionParams[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tencentvectordb/#llama_index.vector_stores.tencentvectordb.CollectionParams "CollectionParams \(llama_index.vector_stores.tencentvectordb.base.CollectionParams\)")]`  |  The collection parameters for vector database  |  `CollectionParams[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tencentvectordb/#llama_index.vector_stores.tencentvectordb.CollectionParams "CollectionParams \(llama_index.vector_stores.tencentvectordb.base.CollectionParams\)")(dimension=1536)`  |  
Examples:
`pip install llama-index-vector-stores-tencentvectordb`

```
fromllama_index.vector_stores.tencentvectordbimport TencentVectorDB, CollectionParams

# Setup
url = "http://10.0.X.X"
key = "eC4bLRy2va******************************"
collection_params = CollectionParams(dimension=1536, drop_exists=True)

# Create an instance of TencentVectorDB
vector_store = TencentVectorDB(url=url, key=key, collection_params=collection_params)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tencentvectordb/llama_index/vector_stores/tencentvectordb/base.py`  
| 
```
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
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
```
 | 
```
classTencentVectorDB(BasePydanticVectorStore):
"""
    Tencent Vector Store.

    In this vector store, embeddings and docs are stored within a Collection.
    If the Collection does not exist, it will be automatically created.

    In order to use this you need to have a database instance.
    See the following documentation for details:
    https://cloud.tencent.com/document/product/1709/94951

    Args:
        url (Optional[str]): url of Tencent vector database
        username (Optional[str]): The username for Tencent vector database. Default value is "root"
        key (Optional[str]): The Api-Key for Tencent vector database
        collection_params (Optional[CollectionParams]): The collection parameters for vector database

    Examples:
        `pip install llama-index-vector-stores-tencentvectordb`

        ```python
        from llama_index.vector_stores.tencentvectordb import TencentVectorDB, CollectionParams

        # Setup
        url = "http://10.0.X.X"
        key = "eC4bLRy2va******************************"
        collection_params = CollectionParams(dimension=1536, drop_exists=True)

        # Create an instance of TencentVectorDB
        vector_store = TencentVectorDB(url=url, key=key, collection_params=collection_params)
        ```

    """

    stores_text: bool = True
    filter_fields: List[FilterField] = []

    batch_size: int
    _tencent_client: Any = PrivateAttr()
    _database: Any = PrivateAttr()
    _collection: Any = PrivateAttr()
    _filter_fields: List[FilterField] = PrivateAttr()

    def__init__(
        self,
        url: str,
        key: str,
        username: str = DEFAULT_USERNAME,
        database_name: str = DEFAULT_DATABASE_NAME,
        read_consistency: str = READ_EVENTUAL_CONSISTENCY,
        collection_params: CollectionParams = CollectionParams(dimension=1536),
        batch_size: int = 512,
        **kwargs: Any,
    ):
"""Init params."""
        super().__init__(batch_size=batch_size)
        self._init_client(url, username, key, read_consistency)
        self._create_database_if_not_exists(database_name)
        self._create_collection(database_name, collection_params)
        self._init_filter_fields()

    def_init_filter_fields(self) -> None:
        fields = vars(self._collection).get("indexes", [])
        for field in fields:
            if field["fieldName"] not in [FIELD_ID, DEFAULT_DOC_ID_KEY, FIELD_VECTOR]:
                self._filter_fields.append(
                    FilterField(name=field["fieldName"], data_type=field["fieldType"])
                )

    @classmethod
    defclass_name(cls) -> str:
        return "TencentVectorDB"

    @classmethod
    deffrom_params(
        cls,
        url: str,
        key: str,
        username: str = DEFAULT_USERNAME,
        database_name: str = DEFAULT_DATABASE_NAME,
        read_consistency: str = READ_EVENTUAL_CONSISTENCY,
        collection_params: CollectionParams = CollectionParams(dimension=1536),
        batch_size: int = 512,
        **kwargs: Any,
    ) -> "TencentVectorDB":
        _try_import()
        return cls(
            url=url,
            username=username,
            key=key,
            database_name=database_name,
            read_consistency=read_consistency,
            collection_params=collection_params,
            batch_size=batch_size,
            **kwargs,
        )

    def_init_client(
        self, url: str, username: str, key: str, read_consistency: str
    ) -> None:
        importtcvectordb
        fromtcvectordb.model.enumimport ReadConsistency

        if read_consistency is None:
            raise ValueError(VALUE_RANGE_ERROR.format(read_consistency))

        try:
            v_read_consistency = ReadConsistency(read_consistency)
        except ValueError:
            raise ValueError(
                VALUE_RANGE_ERROR.format(READ_CONSISTENCY, READ_CONSISTENCY_VALUES)
            )

        self._tencent_client = tcvectordb.VectorDBClient(
            url=url,
            username=username,
            key=key,
            read_consistency=v_read_consistency,
            timeout=DEFAULT_TIMEOUT,
        )

    def_create_database_if_not_exists(self, database_name: str) -> None:
        db_list = self._tencent_client.list_databases()

        if database_name in [db.database_name for db in db_list]:
            self._database = self._tencent_client.database(database_name)
        else:
            self._database = self._tencent_client.create_database(database_name)

    def_create_collection(
        self, database_name: str, collection_params: CollectionParams
    ) -> None:
        importtcvectordb

        collection_name: str = self._compute_collection_name(
            database_name, collection_params
        )
        collection_description = collection_params._collection_description

        if collection_params is None:
            raise ValueError(VALUE_NONE_ERROR.format("collection_params"))

        try:
            self._collection = self._database.describe_collection(collection_name)
            if collection_params.drop_exists:
                self._database.drop_collection(collection_name)
                self._create_collection_in_db(
                    collection_name, collection_description, collection_params
                )
        except tcvectordb.exceptions.VectorDBException:
            self._create_collection_in_db(
                collection_name, collection_description, collection_params
            )

    @staticmethod
    def_compute_collection_name(
        database_name: str, collection_params: CollectionParams
    ) -> str:
        if database_name == DEFAULT_DATABASE_NAME:
            return collection_params._collection_name
        if collection_params._collection_name != DEFAULT_COLLECTION_NAME:
            return collection_params._collection_name
        else:
            return database_name + "_" + DEFAULT_COLLECTION_NAME

    def_create_collection_in_db(
        self,
        collection_name: str,
        collection_description: str,
        collection_params: CollectionParams,
    ) -> None:
        fromtcvectordb.model.enumimport FieldType, IndexType
        fromtcvectordb.model.indeximport FilterIndex, Index, VectorIndex

        index_type = self._get_index_type(collection_params.index_type)
        metric_type = self._get_metric_type(collection_params.metric_type)
        index_param = self._get_index_params(index_type, collection_params)
        index = Index(
            FilterIndex(
                name=FIELD_ID,
                field_type=FieldType.String,
                index_type=IndexType.PRIMARY_KEY,
            ),
            FilterIndex(
                name=DEFAULT_DOC_ID_KEY,
                field_type=FieldType.String,
                index_type=IndexType.FILTER,
            ),
            VectorIndex(
                name=FIELD_VECTOR,
                dimension=collection_params.dimension,
                index_type=index_type,
                metric_type=metric_type,
                params=index_param,
            ),
        )
        for field in collection_params.filter_fields:
            index.add(field.to_vdb_filter())

        self._collection = self._database.create_collection(
            name=collection_name,
            shard=collection_params.shard,
            replicas=collection_params.replicas,
            description=collection_description,
            index=index,
        )

    @staticmethod
    def_get_index_params(index_type: Any, collection_params: CollectionParams) -> None:
        fromtcvectordb.model.enumimport IndexType
        fromtcvectordb.model.indeximport (
            HNSWParams,
            IVFFLATParams,
            IVFPQParams,
            IVFSQ4Params,
            IVFSQ8Params,
            IVFSQ16Params,
        )

        vector_params = (
            {}
            if collection_params.vector_params is None
            else collection_params.vector_params
        )

        if index_type == IndexType.HNSW:
            return HNSWParams(
                m=vector_params.get("M", DEFAULT_HNSW_M),
                efconstruction=vector_params.get("efConstruction", DEFAULT_HNSW_EF),
            )
        elif index_type == IndexType.IVF_FLAT:
            return IVFFLATParams(nlist=vector_params.get("nlist", DEFAULT_IVF_NLIST))
        elif index_type == IndexType.IVF_PQ:
            return IVFPQParams(
                m=vector_params.get("M", DEFAULT_IVF_PQ_M),
                nlist=vector_params.get("nlist", DEFAULT_IVF_NLIST),
            )
        elif index_type == IndexType.IVF_SQ4:
            return IVFSQ4Params(nlist=vector_params.get("nlist", DEFAULT_IVF_NLIST))
        elif index_type == IndexType.IVF_SQ8:
            return IVFSQ8Params(nlist=vector_params.get("nlist", DEFAULT_IVF_NLIST))
        elif index_type == IndexType.IVF_SQ16:
            return IVFSQ16Params(nlist=vector_params.get("nlist", DEFAULT_IVF_NLIST))
        return None

    @staticmethod
    def_get_index_type(index_type_value: str) -> Any:
        fromtcvectordb.model.enumimport IndexType

        index_type_value = index_type_value or IndexType.HNSW
        try:
            return IndexType(index_type_value)
        except ValueError:
            support_index_types = [d.value for d in IndexType.__members__.values()]
            raise ValueError(
                NOT_SUPPORT_INDEX_TYPE_ERROR.format(
                    index_type_value, support_index_types
                )
            )

    @staticmethod
    def_get_metric_type(metric_type_value: str) -> Any:
        fromtcvectordb.model.enumimport MetricType

        metric_type_value = metric_type_value or MetricType.COSINE
        try:
            return MetricType(metric_type_value.upper())
        except ValueError:
            support_metric_types = [d.value for d in MetricType.__members__.values()]
            raise ValueError(
                NOT_SUPPORT_METRIC_TYPE_ERROR.format(
                    metric_type_value, support_metric_types
                )
            )

    @property
    defclient(self) -> Any:
"""Get client."""
        return self._tencent_client

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to index.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        """
        fromtcvectordb.model.documentimport Document

        ids = []
        entries = []
        for node in nodes:
            document = Document(id=node.node_id, vector=node.get_embedding())
            if node.ref_doc_id is not None:
                document.__dict__[DEFAULT_DOC_ID_KEY] = node.ref_doc_id
            if node.metadata is not None:
                document.__dict__[FIELD_METADATA] = json.dumps(node.metadata)
                for field in self._filter_fields:
                    v = node.metadata.get(field.name)
                    if field.match_value(v):
                        document.__dict__[field.name] = v
            if isinstance(node, TextNode) and node.text is not None:
                document.__dict__[DEFAULT_TEXT_KEY] = node.text

            entries.append(document)
            ids.append(node.node_id)

            if len(entries) >= self.batch_size:
                self._collection.upsert(
                    documents=entries, build_index=True, timeout=DEFAULT_TIMEOUT
                )
                entries = []

        if len(entries)  0:
            self._collection.upsert(
                documents=entries, build_index=True, timeout=DEFAULT_TIMEOUT
            )

        return ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id or ids.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        if ref_doc_id is None or len(ref_doc_id) == 0:
            return

        fromtcvectordb.model.documentimport Filter

        delete_ids = ref_doc_id if isinstance(ref_doc_id, list) else [ref_doc_id]
        self._collection.delete(
            filter=Filter(Filter.In(DEFAULT_DOC_ID_KEY, delete_ids))
        )

    defquery_by_ids(self, ids: List[str]) -> List[Dict]:
        return self._collection.query(document_ids=ids, limit=len(ids))

    deftruncate(self) -> None:
        self._database.truncate_collection(self._collection.collection_name)

    defdescribe_collection(self) -> Any:
        return self._database.describe_collection(self._collection.collection_name)

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query (VectorStoreQuery): contains
                query_embedding (List[float]): query embedding
                similarity_top_k (int): top k most similar nodes
                doc_ids (Optional[List[str]]): filter by doc_id
                filters (Optional[MetadataFilters]): filter result
            kwargs.filter (Optional[str|Filter]):

            if `kwargs` in kwargs:
               using filter: `age > 20 and author in (...) and ...`
            elif query.filters:
               using filter: " and ".join([f'{f.key} = "{f.value}"' for f in query.filters.filters])
            elif query.doc_ids:
               using filter: `doc_id in (query.doc_ids)`

        """
        search_filter = self._to_vdb_filter(query, **kwargs)
        results = self._collection.search(
            vectors=[query.query_embedding],
            limit=query.similarity_top_k,
            retrieve_vector=True,
            output_fields=query.output_fields,
            filter=search_filter,
        )
        if len(results) == 0:
            return VectorStoreQueryResult(nodes=[], similarities=[], ids=[])

        nodes = []
        similarities = []
        ids = []
        for doc in results[0]:
            ids.append(doc.get(FIELD_ID))
            similarities.append(doc.get("score"))

            meta_str = doc.get(FIELD_METADATA)
            meta = {} if meta_str is None else json.loads(meta_str)
            doc_id = doc.get(DEFAULT_DOC_ID_KEY)

            node = TextNode(
                id_=doc.get(FIELD_ID),
                text=doc.get(DEFAULT_TEXT_KEY),
                embedding=doc.get(FIELD_VECTOR),
                metadata=meta,
            )
            if doc_id is not None:
                node.relationships = {
                    NodeRelationship.SOURCE: RelatedNodeInfo(node_id=doc_id)
                }

            nodes.append(node)

        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

    @staticmethod
    def_to_vdb_filter(query: VectorStoreQuery, **kwargs: Any) -> Any:
        fromtcvectordb.model.documentimport Filter

        search_filter = None
        if "filter" in kwargs:
            search_filter = kwargs.pop("filter")
            search_filter = (
                search_filter
                if type(search_filter) is Filter
                else Filter(search_filter)
            )
        elif query.filters is not None and len(query.filters.legacy_filters())  0:
            search_filter = " and ".join(
                [f'{f.key} = "{f.value}"' for f in query.filters.legacy_filters()]
            )
            search_filter = Filter(search_filter)
        elif query.doc_ids is not None:
            search_filter = Filter(Filter.In(DEFAULT_DOC_ID_KEY, query.doc_ids))

        return search_filter

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tencentvectordb/#llama_index.vector_stores.tencentvectordb.TencentVectorDB.client "Permanent link")

```
client: 

```

Get client.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tencentvectordb/#llama_index.vector_stores.tencentvectordb.TencentVectorDB.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tencentvectordb/llama_index/vector_stores/tencentvectordb/base.py`  
| 
```
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
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
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

    """
    fromtcvectordb.model.documentimport Document

    ids = []
    entries = []
    for node in nodes:
        document = Document(id=node.node_id, vector=node.get_embedding())
        if node.ref_doc_id is not None:
            document.__dict__[DEFAULT_DOC_ID_KEY] = node.ref_doc_id
        if node.metadata is not None:
            document.__dict__[FIELD_METADATA] = json.dumps(node.metadata)
            for field in self._filter_fields:
                v = node.metadata.get(field.name)
                if field.match_value(v):
                    document.__dict__[field.name] = v
        if isinstance(node, TextNode) and node.text is not None:
            document.__dict__[DEFAULT_TEXT_KEY] = node.text

        entries.append(document)
        ids.append(node.node_id)

        if len(entries) >= self.batch_size:
            self._collection.upsert(
                documents=entries, build_index=True, timeout=DEFAULT_TIMEOUT
            )
            entries = []

    if len(entries)  0:
        self._collection.upsert(
            documents=entries, build_index=True, timeout=DEFAULT_TIMEOUT
        )

    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tencentvectordb/#llama_index.vector_stores.tencentvectordb.TencentVectorDB.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id or ids.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tencentvectordb/llama_index/vector_stores/tencentvectordb/base.py`  
| 
```
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id or ids.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    if ref_doc_id is None or len(ref_doc_id) == 0:
        return

    fromtcvectordb.model.documentimport Filter

    delete_ids = ref_doc_id if isinstance(ref_doc_id, list) else [ref_doc_id]
    self._collection.delete(
        filter=Filter(Filter.In(DEFAULT_DOC_ID_KEY, delete_ids))
    )

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tencentvectordb/#llama_index.vector_stores.tencentvectordb.TencentVectorDB.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  contains query_embedding (List[float]): query embedding similarity_top_k (int): top k most similar nodes doc_ids (Optional[List[str]]): filter by doc_id filters (Optional[MetadataFilters]): filter result  |  _required_  |  
|  `kwargs.filter`  |  `Optional[str | Filter]`  |  _required_  |  
|  `if `kwargs` in kwargs`  |  using filter: `age > 20 and author in (...) and ...`  |  _required_  |  
|  `elif query.filters`  |  using filter: " and ".join([f'{f.key} = "{f.value}"' for f in query.filters.filters])  |  _required_  |  
|  `elif query.doc_ids`  |  using filter: `doc_id in (query.doc_ids)`  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tencentvectordb/llama_index/vector_stores/tencentvectordb/base.py`  
| 
```
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query (VectorStoreQuery): contains
            query_embedding (List[float]): query embedding
            similarity_top_k (int): top k most similar nodes
            doc_ids (Optional[List[str]]): filter by doc_id
            filters (Optional[MetadataFilters]): filter result
        kwargs.filter (Optional[str|Filter]):

        if `kwargs` in kwargs:
           using filter: `age > 20 and author in (...) and ...`
        elif query.filters:
           using filter: " and ".join([f'{f.key} = "{f.value}"' for f in query.filters.filters])
        elif query.doc_ids:
           using filter: `doc_id in (query.doc_ids)`

    """
    search_filter = self._to_vdb_filter(query, **kwargs)
    results = self._collection.search(
        vectors=[query.query_embedding],
        limit=query.similarity_top_k,
        retrieve_vector=True,
        output_fields=query.output_fields,
        filter=search_filter,
    )
    if len(results) == 0:
        return VectorStoreQueryResult(nodes=[], similarities=[], ids=[])

    nodes = []
    similarities = []
    ids = []
    for doc in results[0]:
        ids.append(doc.get(FIELD_ID))
        similarities.append(doc.get("score"))

        meta_str = doc.get(FIELD_METADATA)
        meta = {} if meta_str is None else json.loads(meta_str)
        doc_id = doc.get(DEFAULT_DOC_ID_KEY)

        node = TextNode(
            id_=doc.get(FIELD_ID),
            text=doc.get(DEFAULT_TEXT_KEY),
            embedding=doc.get(FIELD_VECTOR),
            metadata=meta,
        )
        if doc_id is not None:
            node.relationships = {
                NodeRelationship.SOURCE: RelatedNodeInfo(node_id=doc_id)
            }

        nodes.append(node)

    return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
##  CollectionParams [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tencentvectordb/#llama_index.vector_stores.tencentvectordb.CollectionParams "Permanent link")
Tencent vector DB Collection params. See the following documentation for details: https://cloud.tencent.com/document/product/1709/95826.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `dimension int`  |  The dimension of vector.  |  _required_  |  
|  `shard int`  |  The number of shards in the collection.  |  _required_  |  
|  `replicas int`  |  The number of replicas in the collection.  |  _required_  |  
|  `index_type`  |  `Optional[str]`  |  HNSW, IVF_FLAT, IVF_PQ, IVF_SQ8... Default value is "HNSW"  |  `DEFAULT_INDEX_TYPE`  |  
|  `metric_type`  |  `Optional[str]`  |  L2, COSINE, IP. Default value is "COSINE"  |  `DEFAULT_METRIC_TYPE`  |  
|  `drop_exists`  |  `Optional[bool]`  |  Delete the existing Collection. Default value is False.  |  `False`  |  
|  `vector_params`  |  `Optional[Dict]`  |  if HNSW set parameters: `M` and `efConstruction`, for example `{'M': 16, efConstruction: 200}` if IVF_FLAT or IVF_SQ8 set parameter: `nlist` if IVF_PQ set parameters: `M` and `nlist` default is HNSW  |  `None`  |  
|  `filter_fields`  |  `Optional[List[FilterField]]`  |  Optional[List[FilterField]]: Set the fields for filtering for example: [FilterField(name='author'), FilterField(name='age', data_type=uint64)] This can be used when calling the query method： store.add([ TextNode(..., metadata={'age'=23, 'name'='name1'}) ]) ... query = VectorStoreQuery(...) store.query(query, filter="age > 20 and age < 40 and name in (\"name1\", \"name2\")")  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tencentvectordb/llama_index/vector_stores/tencentvectordb/base.py`  
| 
```
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
```
 | 
```
classCollectionParams:
r"""
    Tencent vector DB Collection params.
    See the following documentation for details:
    https://cloud.tencent.com/document/product/1709/95826.

    Args:
        dimension int: The dimension of vector.
        shard int: The number of shards in the collection.
        replicas int: The number of replicas in the collection.
        index_type (Optional[str]): HNSW, IVF_FLAT, IVF_PQ, IVF_SQ8... Default value is "HNSW"
        metric_type (Optional[str]): L2, COSINE, IP. Default value is "COSINE"
        drop_exists (Optional[bool]): Delete the existing Collection. Default value is False.
        vector_params (Optional[Dict]):
          if HNSW set parameters: `M` and `efConstruction`, for example `{'M': 16, efConstruction: 200}`
          if IVF_FLAT or IVF_SQ8 set parameter: `nlist`
          if IVF_PQ set parameters: `M` and `nlist`
          default is HNSW
        filter_fields: Optional[List[FilterField]]: Set the fields for filtering
          for example: [FilterField(name='author'), FilterField(name='age', data_type=uint64)]
          This can be used when calling the query method：
             store.add([
                TextNode(..., metadata={'age'=23, 'name'='name1'})


             query = VectorStoreQuery(...)
             store.query(query, filter="age > 20 and age < 40 and name in (\"name1\", \"name2\")")

    """

    def__init__(
        self,
        dimension: int,
        collection_name: str = DEFAULT_COLLECTION_NAME,
        collection_description: str = DEFAULT_COLLECTION_DESC,
        shard: int = DEFAULT_SHARD,
        replicas: int = DEFAULT_REPLICAS,
        index_type: str = DEFAULT_INDEX_TYPE,
        metric_type: str = DEFAULT_METRIC_TYPE,
        drop_exists: Optional[bool] = False,
        vector_params: Optional[Dict] = None,
        filter_fields: Optional[List[FilterField]] = [],
    ):
        self._collection_name = collection_name
        self._collection_description = collection_description
        self.dimension = dimension
        self.shard = shard
        self.replicas = replicas
        self.index_type = index_type
        self.metric_type = metric_type
        self.vector_params = vector_params
        self.drop_exists = drop_exists
        self._filter_fields = filter_fields or []

    @property
    deffilter_fields(self) -> List[FilterField]:
"""Get the filter fields for the collection."""
        return self._filter_fields

```
 |  
| --- | --- |  
###  filter_fields `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tencentvectordb/#llama_index.vector_stores.tencentvectordb.CollectionParams.filter_fields "Permanent link")

```
filter_fields: [FilterField]

```

Get the filter fields for the collection.
options: members: - TencentVectorDB
