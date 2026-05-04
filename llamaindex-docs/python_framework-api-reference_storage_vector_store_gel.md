# Gel
##  GelVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/gel/#llama_index.vector_stores.gel.GelVectorStore "Permanent link")
Bases: 
Gel-backed vector store implementation.
Stores and retrieves vectors using Gel database with pgvector extension.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-gel/llama_index/vector_stores/gel/base.py`  
| 
```
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
```
 | 
```
classGelVectorStore(BasePydanticVectorStore):
"""
    Gel-backed vector store implementation.

    Stores and retrieves vectors using Gel database with pgvector extension.
    """

    stores_text: bool = True
    collection_name: str
    record_type: str

    _sync_client: gel.Client = PrivateAttr()
    _async_client: gel.AsyncIOClient = PrivateAttr()

    def__init__(
        self,
        collection_name: str = "default",
        record_type: str = "Record",
    ):
"""
        Initialize GelVectorStore.

        Args:
            collection_name: Name of the collection to store vectors in
            record_type: The record type name in Gel schema

        """
        super().__init__(
            collection_name=collection_name,
            record_type=record_type,
        )

        self._sync_client = None
        self._async_client = None

    defget_sync_client(self):
"""Get or initialize a synchronous Gel client."""
        if self._async_client is not None:
            raise RuntimeError(
                "GelVectorStore has already been used in async mode. "
                "If you were intentionally trying to use different IO modes at the same time, "
                "please create a new instance instead."
            )
        if self._sync_client is None:
            self._sync_client = gel.create_client()

            try:
                self._sync_client.ensure_connected()
            except gel.errors.ClientConnectionError as e:
                _logger.error(NO_PROJECT_MESSAGE)
                raise

            try:
                self._sync_client.query(f"select {self.record_type};")
            except gel.errors.InvalidReferenceError as e:
                _logger.error(
                    Template(MISSING_RECORD_TYPE_TEMPLATE).render(
                        record_type=self.record_type
                    )
                )
                raise

        return self._sync_client

    async defget_async_client(self):
"""Get or initialize an asynchronous Gel client."""
        if self._sync_client is not None:
            raise RuntimeError(
                "GelVectorStore has already been used in sync mode. "
                "If you were intentionally trying to use different IO modes at the same time, "
                "please create a new instance instead."
            )
        if self._async_client is None:
            self._async_client = gel.create_async_client()

            try:
                await self._async_client.ensure_connected()
            except gel.errors.ClientConnectionError as e:
                _logger.error(NO_PROJECT_MESSAGE)
                raise

            try:
                await self._async_client.query(f"select {self.record_type};")
            except gel.errors.InvalidReferenceError as e:
                _logger.error(
                    Template(MISSING_RECORD_TYPE_TEMPLATE).render(
                        record_type=self.record_type
                    )
                )
                raise

        return self._async_client

    @property
    defclient(self) -> Any:
"""Get client."""
        return self.get_sync_client()

    defget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> List[BaseNode]:
"""Get nodes from vector store."""
        assert filters is None, "Filters are not supported in get_nodes"
        if node_ids is None:
            return []

        client = self.get_sync_client()

        results = client.query(
            SELECT_BY_DOC_ID_QUERY.render(record_type=self.record_type),
            external_ids=node_ids,
        )
        return [
            TextNode(
                id_=result.external_id,
                text=result.text,
                metadata=json.loads(result.metadata),
                embedding=result.embedding,
            )
            for result in results
        ]

    async defaget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> List[BaseNode]:
"""Async version of get_nodes."""
        assert filters is None, "Filters are not supported in get_nodes"
        if node_ids is None:
            return []

        client = await self.get_async_client()

        results = await client.query(
            SELECT_BY_DOC_ID_QUERY.render(record_type=self.record_type),
            external_ids=node_ids,
        )
        return [
            TextNode(
                id_=result.external_id,
                text=result.text,
                metadata=json.loads(result.metadata),
                embedding=result.embedding,
            )
            for result in results
        ]

    defadd(
        self,
        nodes: Sequence[BaseNode],
        **kwargs: Any,
    ) -> List[str]:
"""Add nodes to vector store."""
        inserted_ids = []

        client = self.get_sync_client()

        for node in nodes:
            result = client.query(
                INSERT_QUERY.render(record_type=self.record_type),
                collection_name=self.collection_name,
                external_id=node.id_,
                text=node.get_content(),
                embedding=node.embedding,
                metadata=json.dumps(node.metadata),
            )
            inserted_ids.append(result[0].external_id)

        return inserted_ids

    async defasync_add(self, nodes: Sequence[BaseNode], **kwargs: Any) -> List[str]:
"""Async version of add."""
        inserted_ids = []

        client = await self.get_async_client()

        for node in nodes:
            result = await client.query(
                INSERT_QUERY.render(record_type=self.record_type),
                collection_name=self.collection_name,
                external_id=node.id_,
                text=node.get_content(),
                embedding=node.embedding,
                metadata=json.dumps(node.metadata),
            )
            inserted_ids.append(result[0].external_id)

        return inserted_ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""Delete nodes using with ref_doc_id."""
        client = self.get_sync_client()

        result = client.query(
            DELETE_BY_IDS_QUERY.render(record_type=self.record_type),
            collection_name=self.collection_name,
            external_ids=[ref_doc_id],
        )

    async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""Async version of delete."""
        client = await self.get_async_client()

        result = await client.query(
            DELETE_BY_IDS_QUERY.render(record_type=self.record_type),
            collection_name=self.collection_name,
            external_ids=[ref_doc_id],
        )

    defclear(self) -> None:
"""Clear all nodes from configured vector store."""
        client = self.get_sync_client()

        result = client.query(
            DELETE_ALL_QUERY.render(record_type=self.record_type),
            collection_name=self.collection_name,
        )

    async defaclear(self) -> None:
"""Clear all nodes from configured vector store."""
        client = await self.get_async_client()

        result = await client.query(
            DELETE_ALL_QUERY.render(record_type=self.record_type),
            collection_name=self.collection_name,
        )

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query vector store."""
        assert query.query_embedding is not None, "query_embedding is required"

        filter_clause = (
            "filter " + get_filter_clause(query.filters) if query.filters else ""
        )

        assert query.mode == VectorStoreQueryMode.DEFAULT

        rendered_query = COSINE_SIMILARITY_QUERY.render(
            record_type=self.record_type, filter_clause=filter_clause
        )

        client = self.get_sync_client()

        results = client.query(
            rendered_query,
            query_embedding=query.query_embedding,
            collection_name=self.collection_name,
            limit=query.similarity_top_k,
        )

        return VectorStoreQueryResult(
            nodes=[
                TextNode(
                    id_=result.external_id,
                    text=result.text,
                    metadata=json.loads(result.metadata),
                    embedding=result.embedding,
                )
                for result in results
            ],
            similarities=[result.cosine_similarity for result in results],
            ids=[result.external_id for result in results],
        )

    async defaquery(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
"""Async version of query."""
        assert query.query_embedding is not None, "query_embedding is required"

        filter_clause = (
            "filter " + get_filter_clause(query.filters) if query.filters else ""
        )

        assert query.mode == VectorStoreQueryMode.DEFAULT

        rendered_query = COSINE_SIMILARITY_QUERY.render(
            record_type=self.record_type, filter_clause=filter_clause
        )

        client = await self.get_async_client()

        results = await client.query(
            rendered_query,
            query_embedding=query.query_embedding,
            collection_name=self.collection_name,
            limit=query.similarity_top_k,
        )

        return VectorStoreQueryResult(
            nodes=[
                TextNode(
                    id_=result.external_id,
                    text=result.text,
                    metadata=json.loads(result.metadata),
                    embedding=result.embedding,
                )
                for result in results
            ],
            similarities=[result.cosine_similarity for result in results],
            ids=[result.external_id for result in results],
        )

    defpersist(self, persist_path: str, fs) -> None:
        _logger.warning("GelVectorStore.persist() is a no-op")

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/gel/#llama_index.vector_stores.gel.GelVectorStore.client "Permanent link")

```
client: 

```

Get client.
###  get_sync_client [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/gel/#llama_index.vector_stores.gel.GelVectorStore.get_sync_client "Permanent link")

```
get_sync_client()

```

Get or initialize a synchronous Gel client.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-gel/llama_index/vector_stores/gel/base.py`  
| 
```
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
```
 | 
```
defget_sync_client(self):
"""Get or initialize a synchronous Gel client."""
    if self._async_client is not None:
        raise RuntimeError(
            "GelVectorStore has already been used in async mode. "
            "If you were intentionally trying to use different IO modes at the same time, "
            "please create a new instance instead."
        )
    if self._sync_client is None:
        self._sync_client = gel.create_client()

        try:
            self._sync_client.ensure_connected()
        except gel.errors.ClientConnectionError as e:
            _logger.error(NO_PROJECT_MESSAGE)
            raise

        try:
            self._sync_client.query(f"select {self.record_type};")
        except gel.errors.InvalidReferenceError as e:
            _logger.error(
                Template(MISSING_RECORD_TYPE_TEMPLATE).render(
                    record_type=self.record_type
                )
            )
            raise

    return self._sync_client

```
 |  
| --- | --- |  
###  get_async_client [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/gel/#llama_index.vector_stores.gel.GelVectorStore.get_async_client "Permanent link")

```
get_async_client()

```

Get or initialize an asynchronous Gel client.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-gel/llama_index/vector_stores/gel/base.py`  
| 
```
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
```
 | 
```
async defget_async_client(self):
"""Get or initialize an asynchronous Gel client."""
    if self._sync_client is not None:
        raise RuntimeError(
            "GelVectorStore has already been used in sync mode. "
            "If you were intentionally trying to use different IO modes at the same time, "
            "please create a new instance instead."
        )
    if self._async_client is None:
        self._async_client = gel.create_async_client()

        try:
            await self._async_client.ensure_connected()
        except gel.errors.ClientConnectionError as e:
            _logger.error(NO_PROJECT_MESSAGE)
            raise

        try:
            await self._async_client.query(f"select {self.record_type};")
        except gel.errors.InvalidReferenceError as e:
            _logger.error(
                Template(MISSING_RECORD_TYPE_TEMPLATE).render(
                    record_type=self.record_type
                )
            )
            raise

    return self._async_client

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/gel/#llama_index.vector_stores.gel.GelVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Get nodes from vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-gel/llama_index/vector_stores/gel/base.py`  
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
```
 | 
```
defget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> List[BaseNode]:
"""Get nodes from vector store."""
    assert filters is None, "Filters are not supported in get_nodes"
    if node_ids is None:
        return []

    client = self.get_sync_client()

    results = client.query(
        SELECT_BY_DOC_ID_QUERY.render(record_type=self.record_type),
        external_ids=node_ids,
    )
    return [
        TextNode(
            id_=result.external_id,
            text=result.text,
            metadata=json.loads(result.metadata),
            embedding=result.embedding,
        )
        for result in results
    ]

```
 |  
| --- | --- |  
###  aget_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/gel/#llama_index.vector_stores.gel.GelVectorStore.aget_nodes "Permanent link")

```
aget_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Async version of get_nodes.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-gel/llama_index/vector_stores/gel/base.py`  
| 
```
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
```
 | 
```
async defaget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> List[BaseNode]:
"""Async version of get_nodes."""
    assert filters is None, "Filters are not supported in get_nodes"
    if node_ids is None:
        return []

    client = await self.get_async_client()

    results = await client.query(
        SELECT_BY_DOC_ID_QUERY.render(record_type=self.record_type),
        external_ids=node_ids,
    )
    return [
        TextNode(
            id_=result.external_id,
            text=result.text,
            metadata=json.loads(result.metadata),
            embedding=result.embedding,
        )
        for result in results
    ]

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/gel/#llama_index.vector_stores.gel.GelVectorStore.add "Permanent link")

```
add(nodes: Sequence[], **kwargs: ) -> []

```

Add nodes to vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-gel/llama_index/vector_stores/gel/base.py`  
| 
```
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
```
 | 
```
defadd(
    self,
    nodes: Sequence[BaseNode],
    **kwargs: Any,
) -> List[str]:
"""Add nodes to vector store."""
    inserted_ids = []

    client = self.get_sync_client()

    for node in nodes:
        result = client.query(
            INSERT_QUERY.render(record_type=self.record_type),
            collection_name=self.collection_name,
            external_id=node.id_,
            text=node.get_content(),
            embedding=node.embedding,
            metadata=json.dumps(node.metadata),
        )
        inserted_ids.append(result[0].external_id)

    return inserted_ids

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/gel/#llama_index.vector_stores.gel.GelVectorStore.async_add "Permanent link")

```
async_add(
    nodes: Sequence[], **kwargs: 
) -> []

```

Async version of add.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-gel/llama_index/vector_stores/gel/base.py`  
| 
```
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
```
 | 
```
async defasync_add(self, nodes: Sequence[BaseNode], **kwargs: Any) -> List[str]:
"""Async version of add."""
    inserted_ids = []

    client = await self.get_async_client()

    for node in nodes:
        result = await client.query(
            INSERT_QUERY.render(record_type=self.record_type),
            collection_name=self.collection_name,
            external_id=node.id_,
            text=node.get_content(),
            embedding=node.embedding,
            metadata=json.dumps(node.metadata),
        )
        inserted_ids.append(result[0].external_id)

    return inserted_ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/gel/#llama_index.vector_stores.gel.GelVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-gel/llama_index/vector_stores/gel/base.py`  
| 
```
400
401
402
403
404
405
406
407
408
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""Delete nodes using with ref_doc_id."""
    client = self.get_sync_client()

    result = client.query(
        DELETE_BY_IDS_QUERY.render(record_type=self.record_type),
        collection_name=self.collection_name,
        external_ids=[ref_doc_id],
    )

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/gel/#llama_index.vector_stores.gel.GelVectorStore.adelete "Permanent link")

```
adelete(ref_doc_id: , **delete_kwargs: ) -> None

```

Async version of delete.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-gel/llama_index/vector_stores/gel/base.py`  
| 
```
410
411
412
413
414
415
416
417
418
```
 | 
```
async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""Async version of delete."""
    client = await self.get_async_client()

    result = await client.query(
        DELETE_BY_IDS_QUERY.render(record_type=self.record_type),
        collection_name=self.collection_name,
        external_ids=[ref_doc_id],
    )

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/gel/#llama_index.vector_stores.gel.GelVectorStore.clear "Permanent link")

```
clear() -> None

```

Clear all nodes from configured vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-gel/llama_index/vector_stores/gel/base.py`  
| 
```
420
421
422
423
424
425
426
427
```
 | 
```
defclear(self) -> None:
"""Clear all nodes from configured vector store."""
    client = self.get_sync_client()

    result = client.query(
        DELETE_ALL_QUERY.render(record_type=self.record_type),
        collection_name=self.collection_name,
    )

```
 |  
| --- | --- |  
###  aclear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/gel/#llama_index.vector_stores.gel.GelVectorStore.aclear "Permanent link")

```
aclear() -> None

```

Clear all nodes from configured vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-gel/llama_index/vector_stores/gel/base.py`  
| 
```
429
430
431
432
433
434
435
436
```
 | 
```
async defaclear(self) -> None:
"""Clear all nodes from configured vector store."""
    client = await self.get_async_client()

    result = await client.query(
        DELETE_ALL_QUERY.render(record_type=self.record_type),
        collection_name=self.collection_name,
    )

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/gel/#llama_index.vector_stores.gel.GelVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-gel/llama_index/vector_stores/gel/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query vector store."""
    assert query.query_embedding is not None, "query_embedding is required"

    filter_clause = (
        "filter " + get_filter_clause(query.filters) if query.filters else ""
    )

    assert query.mode == VectorStoreQueryMode.DEFAULT

    rendered_query = COSINE_SIMILARITY_QUERY.render(
        record_type=self.record_type, filter_clause=filter_clause
    )

    client = self.get_sync_client()

    results = client.query(
        rendered_query,
        query_embedding=query.query_embedding,
        collection_name=self.collection_name,
        limit=query.similarity_top_k,
    )

    return VectorStoreQueryResult(
        nodes=[
            TextNode(
                id_=result.external_id,
                text=result.text,
                metadata=json.loads(result.metadata),
                embedding=result.embedding,
            )
            for result in results
        ],
        similarities=[result.cosine_similarity for result in results],
        ids=[result.external_id for result in results],
    )

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/gel/#llama_index.vector_stores.gel.GelVectorStore.aquery "Permanent link")

```
aquery(
    query: , **kwargs: 
) -> 

```

Async version of query.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-gel/llama_index/vector_stores/gel/base.py`  
| 
```
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
```
 | 
```
async defaquery(
    self, query: VectorStoreQuery, **kwargs: Any
) -> VectorStoreQueryResult:
"""Async version of query."""
    assert query.query_embedding is not None, "query_embedding is required"

    filter_clause = (
        "filter " + get_filter_clause(query.filters) if query.filters else ""
    )

    assert query.mode == VectorStoreQueryMode.DEFAULT

    rendered_query = COSINE_SIMILARITY_QUERY.render(
        record_type=self.record_type, filter_clause=filter_clause
    )

    client = await self.get_async_client()

    results = await client.query(
        rendered_query,
        query_embedding=query.query_embedding,
        collection_name=self.collection_name,
        limit=query.similarity_top_k,
    )

    return VectorStoreQueryResult(
        nodes=[
            TextNode(
                id_=result.external_id,
                text=result.text,
                metadata=json.loads(result.metadata),
                embedding=result.embedding,
            )
            for result in results
        ],
        similarities=[result.cosine_similarity for result in results],
        ids=[result.external_id for result in results],
    )

```
 |  
| --- | --- |  
##  get_filter_clause [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/gel/#llama_index.vector_stores.gel.get_filter_clause "Permanent link")

```
get_filter_clause(filters: ) -> 

```

Convert metadata filters to Gel query filter clause.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-gel/llama_index/vector_stores/gel/base.py`  
| 
```
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
```
 | 
```
defget_filter_clause(filters: MetadataFilters) -> str:
"""Convert metadata filters to Gel query filter clause."""
    subclauses = []
    for filter in filters.filters:
        if isinstance(filter, MetadataFilters):
            subclause = get_filter_clause(filter)
        elif isinstance(filter, MetadataFilter):
            formatted_value = (
                f'"{filter.value}"' if isinstance(filter.value, str) else filter.value
            )
            if filter.operator == FilterOperator.EQ.value:
                subclause = (
                    f'<str>json_get(.metadata, "{filter.key}") = {formatted_value}'
                )
            elif filter.operator == FilterOperator.GT.value:
                subclause = (
                    f'<str>json_get(.metadata, "{filter.key}") > {formatted_value}'
                )
            elif filter.operator == FilterOperator.LT.value:
                subclause = (
                    f'<str>json_get(.metadata, "{filter.key}") < {formatted_value}'
                )
            elif filter.operator == FilterOperator.NE.value:
                subclause = (
                    f'<str>json_get(.metadata, "{filter.key}") != {formatted_value}'
                )
            elif filter.operator == FilterOperator.GTE.value:
                subclause = (
                    f'<str>json_get(.metadata, "{filter.key}") >= {formatted_value}'
                )
            elif filter.operator == FilterOperator.LTE.value:
                subclause = (
                    f'<str>json_get(.metadata, "{filter.key}") <= {formatted_value}'
                )
            elif filter.operator == FilterOperator.IN.value:
                subclause = f'<str>json_get(.metadata, "{filter.key}") in array_unpack({formatted_value})'
            elif filter.operator == FilterOperator.NIN.value:
                subclause = f'<str>json_get(.metadata, "{filter.key}") not in array_unpack({formatted_value})'
            elif filter.operator == FilterOperator.ANY.value:
                subclause = f'any(<str>json_get(.metadata, "{filter.key}") = array_unpack({formatted_value}))'
            elif filter.operator == FilterOperator.ALL.value:
                subclause = f'all(<str>json_get(.metadata, "{filter.key}") = array_unpack({formatted_value}))'
            elif filter.operator == FilterOperator.TEXT_MATCH.value:
                subclause = (
                    f'<str>json_get(.metadata, "{filter.key}") like {formatted_value}'
                )
            elif filter.operator == FilterOperator.CONTAINS.value:
                subclause = f'contains(<str>json_get(.metadata, "{filter.key}"), {formatted_value})'
            elif filter.operator == FilterOperator.IS_EMPTY.value:
                subclause = f'not exists <str>json_get(.metadata, "{filter.key}")'
            else:
                raise ValueError(f"Unknown operator: {filter.operator}")

        subclauses.append(subclause)

    if filters.condition == FilterCondition.AND:
        filter_clause = " and ".join(subclauses)
        return "(" + filter_clause + ")" if len(subclauses)  1 else filter_clause
    elif filters.condition == FilterCondition.OR:
        filter_clause = " or ".join(subclauses)
        return "(" + filter_clause + ")" if len(subclauses)  1 else filter_clause
    else:
        raise ValueError(f"Unknown condition: {filters.condition}")

```
 |  
| --- | --- |  
options: members: - GelVectorStore
