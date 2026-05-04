# Weaviate
##  WeaviateVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/weaviate/#llama_index.vector_stores.weaviate.WeaviateVectorStore "Permanent link")
Bases: 
Weaviate vector store.
In this vector store, embeddings and docs are stored within a Weaviate collection.
During query time, the index uses Weaviate to query for the top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `weaviate_client`  |  `Optional[Any]`  |  Either a WeaviateClient (synchronous) or WeaviateAsyncClient (asynchronous) instance from `weaviate-client` package  |  `None`  |  
|  `index_name`  |  `Optional[str]`  |  name for Weaviate classes  |  `None`  |  
Examples:
`pip install llama-index-vector-stores-weaviate`

```
importweaviate

resource_owner_config = weaviate.AuthClientPassword(
    username="<username>",
    password="<password>",
)
client = weaviate.Client(
    "https://llama-test-ezjahb4m.weaviate.network",
    auth_client_secret=resource_owner_config,
)

vector_store = WeaviateVectorStore(
    weaviate_client=client, index_name="LlamaIndex"
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-weaviate/llama_index/vector_stores/weaviate/base.py`  
| 
```
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
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
```
 | 
```
classWeaviateVectorStore(BasePydanticVectorStore):
"""
    Weaviate vector store.

    In this vector store, embeddings and docs are stored within a
    Weaviate collection.

    During query time, the index uses Weaviate to query for the top
    k most similar nodes.

    Args:
        weaviate_client (Optional[Any]): Either a WeaviateClient (synchronous) or WeaviateAsyncClient (asynchronous)
            instance from `weaviate-client` package
        index_name (Optional[str]): name for Weaviate classes

    Examples:
        `pip install llama-index-vector-stores-weaviate`

        ```python
        import weaviate

        resource_owner_config = weaviate.AuthClientPassword(
            username="<username>",
            password="<password>",

        client = weaviate.Client(
            "https://llama-test-ezjahb4m.weaviate.network",
            auth_client_secret=resource_owner_config,


        vector_store = WeaviateVectorStore(
            weaviate_client=client, index_name="LlamaIndex"

        ```

    """

    stores_text: bool = True

    index_name: str
    url: Optional[str]
    text_key: str
    auth_config: Dict[str, Any] = Field(default_factory=dict)
    client_kwargs: Dict[str, Any] = Field(default_factory=dict)

    _client: weaviate.WeaviateClient = PrivateAttr()
    _aclient: weaviate.WeaviateAsyncClient = PrivateAttr()

    _collection_initialized: bool = PrivateAttr()
    _is_self_created_weaviate_client: bool = PrivateAttr()  # States if the Weaviate client was created within this class and therefore closing it lies in our responsibility
    _custom_batch: Optional[BatchWrapper] = PrivateAttr()
    _property_types: Optional[Dict[str, Any]] = PrivateAttr()

    def__init__(
        self,
        weaviate_client: Optional[Any] = None,
        class_prefix: Optional[str] = None,
        index_name: Optional[str] = None,
        text_key: str = DEFAULT_TEXT_KEY,
        auth_config: Optional[Any] = None,
        client_kwargs: Optional[Dict[str, Any]] = None,
        url: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        # validate class prefix starts with a capital letter
        if class_prefix is not None:
            _logger.warning("class_prefix is deprecated, please use index_name")
            # legacy, kept for backward compatibility
            index_name = f"{class_prefix}_Node"

        index_name = index_name or f"LlamaIndex_{uuid4().hex}"
        if not index_name[0].isupper():
            raise ValueError(
                "Index name must start with a capital letter, e.g. 'LlamaIndex'"
            )

        super().__init__(
            url=url,
            index_name=index_name,
            text_key=text_key,
            auth_config=auth_config.__dict__ if auth_config else {},
            client_kwargs=client_kwargs or {},
        )

        if isinstance(weaviate_client, weaviate.WeaviateClient):
            self._client = weaviate_client
            self._aclient = None
            self._is_self_created_weaviate_client = False
        elif isinstance(weaviate_client, weaviate.WeaviateAsyncClient):
            self._client = None
            self._aclient = weaviate_client
            self._is_self_created_weaviate_client = False
        elif weaviate_client is None:
            if isinstance(auth_config, dict):
                auth_config = weaviate.auth.AuthApiKey(auth_config)

            client_kwargs = client_kwargs or {}
            self._client = weaviate.WeaviateClient(
                auth_client_secret=auth_config, **client_kwargs
            )
            self._client.connect()
            self._is_self_created_weaviate_client = True
        else:  # weaviate_client neither one of the expected types nor None
            raise ValueError(
                f"Unsupported weaviate_client of type {type(weaviate_client)}. Either provide an instance of `WeaviateClient` or `WeaviateAsyncClient` or set `weaviate_client` to None to have a sync client automatically created using the setting provided in `auth_config` and `client_kwargs`."
            )
        # validate custom batch
        self._custom_batch = (
            client_kwargs.get("custom_batch") if client_kwargs else None
        )
        if self._custom_batch and not isinstance(self._custom_batch, BatchWrapper):
            raise ValueError(
                "client_kwargs['custom_batch'] must be an instance of client.batch.dynamic() or client.batch.fixed_size()"
            )

        self._property_types = None

        # create default schema if does not exist
        if self._client is not None:
            if not class_schema_exists(self._client, index_name):
                create_default_schema(self._client, index_name)
            self._collection_initialized = True
        else:
            #  need to do lazy init for async clients
            self._collection_initialized = False

    def__del__(self) -> None:
        if self._is_self_created_weaviate_client:
            self.client.close()

    @classmethod
    defclass_name(cls) -> str:
        return "WeaviateVectorStore"

    @property
    defclient(self) -> weaviate.WeaviateClient:
"""Get the synchronous Weaviate client, if available."""
        if self._client is None:
            raise SyncClientNotProvidedError
        return self._client

    @property
    defasync_client(self) -> weaviate.WeaviateAsyncClient:
"""Get the asynchronous Weaviate client, if available."""
        if self._aclient is None:
            raise AsyncClientNotProvidedError
        return self._aclient

    def_get_property_types(self) -> Dict[str, Any]:
"""
        Get property name to data type mapping from the collection schema.

        The mapping is cached after the first fetch. This is used to coerce
        filter values to match the schema's expected data types, preventing
        type mismatches (e.g. int vs number, numeric string vs text).
        """
        if self._property_types is None:
            try:
                collection = self.client.collections.get(self.index_name)
                config = collection.config.get()
                self._property_types = {
                    prop.name: prop.data_type for prop in config.properties
                }
            except Exception as e:
                _logger.warning(
                    "Failed to fetch property types for collection "
                    f"'{self.index_name}': {e}. Filter value coercion will "
                    "be skipped for this call and retried on the next."
                )
                return {}
        return self._property_types

    async def_aget_property_types(self) -> Dict[str, Any]:
"""
        Get property name to data type mapping from the collection schema (async).

        The mapping is cached after the first fetch.
        """
        if self._property_types is None:
            try:
                collection = self.async_client.collections.get(self.index_name)
                config = await collection.config.get()
                self._property_types = {
                    prop.name: prop.data_type for prop in config.properties
                }
            except Exception as e:
                _logger.warning(
                    "Failed to fetch property types for collection "
                    f"'{self.index_name}': {e}. Filter value coercion will "
                    "be skipped for this call and retried on the next."
                )
                return {}
        return self._property_types

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
        ids = [r.node_id for r in nodes]
        provided_batch = self._custom_batch
        if not provided_batch:
            provided_batch = self.client.batch.dynamic()
        with provided_batch as batch:
            for node in nodes:
                data_object = get_data_object(node=node, text_key=self.text_key)
                batch.add_object(
                    collection=self.index_name,
                    properties=data_object.properties,
                    uuid=data_object.uuid,
                    vector=data_object.vector,
                )
        return ids

    async defasync_add(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to index.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        Raises:
            AsyncClientNotProvidedError: If trying to use async methods without aclient

        """
        if len(nodes)  0 and not self._collection_initialized:
            if not await aclass_schema_exists(self.async_client, self.index_name):
                await acreate_default_schema(self.async_client, self.index_name)

        ids = [r.node_id for r in nodes]

        collection = self.async_client.collections.get(self.index_name)

        response = await collection.data.insert_many(
            [get_data_object(node=node, text_key=self.text_key) for node in nodes]
        )
        return ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        collection = self.client.collections.get(self.index_name)

        where_filter = wvc.query.Filter.by_property("ref_doc_id").equal(ref_doc_id)

        if "filter" in delete_kwargs and delete_kwargs["filter"] is not None:
            where_filter = where_filter  _to_weaviate_filter(
                delete_kwargs["filter"], self._get_property_types()
            )

        collection.data.delete_many(where=where_filter)

    async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        Raises:
            AsyncClientNotProvidedError: If trying to use async methods without aclient

        """
        collection = self.async_client.collections.get(self.index_name)

        where_filter = wvc.query.Filter.by_property("ref_doc_id").equal(ref_doc_id)

        if "filter" in delete_kwargs and delete_kwargs["filter"] is not None:
            property_types = await self._aget_property_types()
            where_filter = where_filter  _to_weaviate_filter(
                delete_kwargs["filter"], property_types
            )

        result = await collection.data.delete_many(where=where_filter)

    defdelete_index(self) -> None:
"""
        Delete the index associated with the client.

        Raises:
        - Exception: If the deletion fails, for some reason.

        """
        if not class_schema_exists(self.client, self.index_name):
            _logger.warning(
                f"Index '{self.index_name}' does not exist. No action taken."
            )
            return
        try:
            self.client.collections.delete(self.index_name)
            _logger.info(f"Successfully deleted index '{self.index_name}'.")
        except Exception as e:
            _logger.error(f"Failed to delete index '{self.index_name}': {e}")
            raise Exception(f"Failed to delete index '{self.index_name}': {e}")

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Deletes nodes.

        Args:
            node_ids (Optional[List[str]], optional): IDs of nodes to delete. Defaults to None.
            filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

        """
        if not node_ids and not filters:
            return

        collection = self.client.collections.get(self.index_name)

        if node_ids:
            filter = wvc.query.Filter.by_id().contains_any(node_ids or [])

        if filters:
            property_types = self._get_property_types()
            if node_ids:
                filter = filter  _to_weaviate_filter(filters, property_types)
            else:
                filter = _to_weaviate_filter(filters, property_types)

        collection.data.delete_many(where=filter, **delete_kwargs)

    async defadelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Deletes nodes.

        Args:
            node_ids (Optional[List[str]], optional): IDs of nodes to delete. Defaults to None.
            filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

        Raises:
            AsyncClientNotProvidedError: If trying to use async methods without aclient

        """
        if not node_ids and not filters:
            return

        collection = self.async_client.collections.get(self.index_name)

        if node_ids:
            filter = wvc.query.Filter.by_id().contains_any(node_ids or [])

        if filters:
            property_types = await self._aget_property_types()
            if node_ids:
                filter = filter  _to_weaviate_filter(filters, property_types)
            else:
                filter = _to_weaviate_filter(filters, property_types)

        await collection.data.delete_many(where=filter, **delete_kwargs)

    defclear(self) -> None:
"""Clears index."""
        self.delete_index()

    async defaclear(self) -> None:
"""
        Delete the index associated with the client.

        Raises:
        - Exception: If the deletion fails, for some reason.
        - AsyncClientNotProvidedError: If trying to use async methods without aclient

        """
        if not await aclass_schema_exists(self.async_client, self.index_name):
            _logger.warning(
                f"Index '{self.index_name}' does not exist. No action taken."
            )
            return
        try:
            await self.async_client.collections.delete(self.index_name)
            _logger.info(f"Successfully deleted index '{self.index_name}'.")
        except Exception as e:
            _logger.error(f"Failed to delete index '{self.index_name}': {e}")
            raise Exception(f"Failed to delete index '{self.index_name}': {e}")

    defget_query_parameters(
        self,
        query: VectorStoreQuery,
        property_types: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ):
        filters = None

        # list of documents to constrain search
        if query.doc_ids:
            filters = wvc.query.Filter.by_property("doc_id").contains_any(query.doc_ids)

        if query.node_ids:
            filters = wvc.query.Filter.by_property("id").contains_any(query.node_ids)

        return_metatada = wvc.query.MetadataQuery(distance=True, score=True)

        vector = query.query_embedding
        alpha = 1
        if query.mode == VectorStoreQueryMode.HYBRID:
            _logger.debug(f"Using hybrid search with alpha {query.alpha}")
            if vector is not None and query.query_str:
                alpha = query.alpha or 0.5

        if query.filters is not None:
            filters = _to_weaviate_filter(query.filters, property_types)
        elif "filter" in kwargs and kwargs["filter"] is not None:
            filters = kwargs["filter"]

        limit = query.similarity_top_k
        _logger.debug(f"Using limit of {query.similarity_top_k}")

        query_parameters = {
            "query": query.query_str,
            "vector": vector,
            "alpha": alpha,
            "limit": limit,
            "filters": filters,
            "return_metadata": return_metatada,
            "include_vector": True,
        }
        query_parameters.update(kwargs)
        return query_parameters

    defparse_query_result(
        self, query_result: Any, query: VectorStoreQuery
    ) -> VectorStoreQueryResult:
        entries = query_result.objects

        similarity_key = "score"
        similarities = []
        nodes: List[BaseNode] = []
        node_ids = []

        for i, entry in enumerate(entries):
            if i  query.similarity_top_k:
                entry_as_dict = entry.__dict__
                similarities.append(get_node_similarity(entry_as_dict, similarity_key))
                nodes.append(to_node(entry_as_dict, text_key=self.text_key))
                node_ids.append(nodes[-1].node_id)
            else:
                break

        return VectorStoreQueryResult(
            nodes=nodes, ids=node_ids, similarities=similarities
        )

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query index for top k most similar nodes."""
        collection = self.client.collections.get(self.index_name)
        property_types = self._get_property_types()
        query_parameters = self.get_query_parameters(
            query, property_types=property_types, **kwargs
        )

        # execute query
        try:
            query_result = collection.query.hybrid(**query_parameters)
        except weaviate.exceptions.WeaviateQueryError as e:
            raise ValueError(f"Invalid query, got errors: {e.message}")

        # parse results
        return self.parse_query_result(query_result, query)

    async defaquery(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Raises:
            AsyncClientNotProvidedError: If trying to use async methods without aclient

        """
        collection = self.async_client.collections.get(self.index_name)
        property_types = await self._aget_property_types()
        query_parameters = self.get_query_parameters(
            query, property_types=property_types, **kwargs
        )

        # execute query
        try:
            query_result = await collection.query.hybrid(**query_parameters)
        except weaviate.exceptions.WeaviateQueryError as e:
            raise ValueError(f"Invalid query, got errors: {e.message}")

        # parse results
        return self.parse_query_result(query_result, query)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/weaviate/#llama_index.vector_stores.weaviate.WeaviateVectorStore.client "Permanent link")

```
client: WeaviateClient

```

Get the synchronous Weaviate client, if available.
###  async_client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/weaviate/#llama_index.vector_stores.weaviate.WeaviateVectorStore.async_client "Permanent link")

```
async_client: WeaviateAsyncClient

```

Get the asynchronous Weaviate client, if available.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/weaviate/#llama_index.vector_stores.weaviate.WeaviateVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-weaviate/llama_index/vector_stores/weaviate/base.py`  
| 
```
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
    ids = [r.node_id for r in nodes]
    provided_batch = self._custom_batch
    if not provided_batch:
        provided_batch = self.client.batch.dynamic()
    with provided_batch as batch:
        for node in nodes:
            data_object = get_data_object(node=node, text_key=self.text_key)
            batch.add_object(
                collection=self.index_name,
                properties=data_object.properties,
                uuid=data_object.uuid,
                vector=data_object.vector,
            )
    return ids

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/weaviate/#llama_index.vector_stores.weaviate.WeaviateVectorStore.async_add "Permanent link")

```
async_add(
    nodes: [], **add_kwargs: 
) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|   |  If trying to use async methods without aclient  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-weaviate/llama_index/vector_stores/weaviate/base.py`  
| 
```
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
```
 | 
```
async defasync_add(
    self,
    nodes: List[BaseNode],
    **add_kwargs: Any,
) -> List[str]:
"""
    Add nodes to index.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings

    Raises:
        AsyncClientNotProvidedError: If trying to use async methods without aclient

    """
    if len(nodes)  0 and not self._collection_initialized:
        if not await aclass_schema_exists(self.async_client, self.index_name):
            await acreate_default_schema(self.async_client, self.index_name)

    ids = [r.node_id for r in nodes]

    collection = self.async_client.collections.get(self.index_name)

    response = await collection.data.insert_many(
        [get_data_object(node=node, text_key=self.text_key) for node in nodes]
    )
    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/weaviate/#llama_index.vector_stores.weaviate.WeaviateVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-weaviate/llama_index/vector_stores/weaviate/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    collection = self.client.collections.get(self.index_name)

    where_filter = wvc.query.Filter.by_property("ref_doc_id").equal(ref_doc_id)

    if "filter" in delete_kwargs and delete_kwargs["filter"] is not None:
        where_filter = where_filter  _to_weaviate_filter(
            delete_kwargs["filter"], self._get_property_types()
        )

    collection.data.delete_many(where=where_filter)

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/weaviate/#llama_index.vector_stores.weaviate.WeaviateVectorStore.adelete "Permanent link")

```
adelete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|   |  If trying to use async methods without aclient  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-weaviate/llama_index/vector_stores/weaviate/base.py`  
| 
```
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
```
 | 
```
async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    Raises:
        AsyncClientNotProvidedError: If trying to use async methods without aclient

    """
    collection = self.async_client.collections.get(self.index_name)

    where_filter = wvc.query.Filter.by_property("ref_doc_id").equal(ref_doc_id)

    if "filter" in delete_kwargs and delete_kwargs["filter"] is not None:
        property_types = await self._aget_property_types()
        where_filter = where_filter  _to_weaviate_filter(
            delete_kwargs["filter"], property_types
        )

    result = await collection.data.delete_many(where=where_filter)

```
 |  
| --- | --- |  
###  delete_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/weaviate/#llama_index.vector_stores.weaviate.WeaviateVectorStore.delete_index "Permanent link")

```
delete_index() -> None

```

Delete the index associated with the client.
Raises: - Exception: If the deletion fails, for some reason.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-weaviate/llama_index/vector_stores/weaviate/base.py`  
| 
```
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
```
 | 
```
defdelete_index(self) -> None:
"""
    Delete the index associated with the client.

    Raises:
    - Exception: If the deletion fails, for some reason.

    """
    if not class_schema_exists(self.client, self.index_name):
        _logger.warning(
            f"Index '{self.index_name}' does not exist. No action taken."
        )
        return
    try:
        self.client.collections.delete(self.index_name)
        _logger.info(f"Successfully deleted index '{self.index_name}'.")
    except Exception as e:
        _logger.error(f"Failed to delete index '{self.index_name}': {e}")
        raise Exception(f"Failed to delete index '{self.index_name}': {e}")

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/weaviate/#llama_index.vector_stores.weaviate.WeaviateVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Deletes nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  IDs of nodes to delete. Defaults to None.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters. Defaults to None.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-weaviate/llama_index/vector_stores/weaviate/base.py`  
| 
```
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
defdelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Deletes nodes.

    Args:
        node_ids (Optional[List[str]], optional): IDs of nodes to delete. Defaults to None.
        filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

    """
    if not node_ids and not filters:
        return

    collection = self.client.collections.get(self.index_name)

    if node_ids:
        filter = wvc.query.Filter.by_id().contains_any(node_ids or [])

    if filters:
        property_types = self._get_property_types()
        if node_ids:
            filter = filter  _to_weaviate_filter(filters, property_types)
        else:
            filter = _to_weaviate_filter(filters, property_types)

    collection.data.delete_many(where=filter, **delete_kwargs)

```
 |  
| --- | --- |  
###  adelete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/weaviate/#llama_index.vector_stores.weaviate.WeaviateVectorStore.adelete_nodes "Permanent link")

```
adelete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Deletes nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  IDs of nodes to delete. Defaults to None.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters. Defaults to None.  |  `None`  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|   |  If trying to use async methods without aclient  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-weaviate/llama_index/vector_stores/weaviate/base.py`  
| 
```
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
```
 | 
```
async defadelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Deletes nodes.

    Args:
        node_ids (Optional[List[str]], optional): IDs of nodes to delete. Defaults to None.
        filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

    Raises:
        AsyncClientNotProvidedError: If trying to use async methods without aclient

    """
    if not node_ids and not filters:
        return

    collection = self.async_client.collections.get(self.index_name)

    if node_ids:
        filter = wvc.query.Filter.by_id().contains_any(node_ids or [])

    if filters:
        property_types = await self._aget_property_types()
        if node_ids:
            filter = filter  _to_weaviate_filter(filters, property_types)
        else:
            filter = _to_weaviate_filter(filters, property_types)

    await collection.data.delete_many(where=filter, **delete_kwargs)

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/weaviate/#llama_index.vector_stores.weaviate.WeaviateVectorStore.clear "Permanent link")

```
clear() -> None

```

Clears index.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-weaviate/llama_index/vector_stores/weaviate/base.py`  
| 
```
551
552
553
```
 | 
```
defclear(self) -> None:
"""Clears index."""
    self.delete_index()

```
 |  
| --- | --- |  
###  aclear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/weaviate/#llama_index.vector_stores.weaviate.WeaviateVectorStore.aclear "Permanent link")

```
aclear() -> None

```

Delete the index associated with the client.
Raises: - Exception: If the deletion fails, for some reason. - AsyncClientNotProvidedError: If trying to use async methods without aclient
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-weaviate/llama_index/vector_stores/weaviate/base.py`  
| 
```
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
```
 | 
```
async defaclear(self) -> None:
"""
    Delete the index associated with the client.

    Raises:
    - Exception: If the deletion fails, for some reason.
    - AsyncClientNotProvidedError: If trying to use async methods without aclient

    """
    if not await aclass_schema_exists(self.async_client, self.index_name):
        _logger.warning(
            f"Index '{self.index_name}' does not exist. No action taken."
        )
        return
    try:
        await self.async_client.collections.delete(self.index_name)
        _logger.info(f"Successfully deleted index '{self.index_name}'.")
    except Exception as e:
        _logger.error(f"Failed to delete index '{self.index_name}': {e}")
        raise Exception(f"Failed to delete index '{self.index_name}': {e}")

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/weaviate/#llama_index.vector_stores.weaviate.WeaviateVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-weaviate/llama_index/vector_stores/weaviate/base.py`  
| 
```
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query index for top k most similar nodes."""
    collection = self.client.collections.get(self.index_name)
    property_types = self._get_property_types()
    query_parameters = self.get_query_parameters(
        query, property_types=property_types, **kwargs
    )

    # execute query
    try:
        query_result = collection.query.hybrid(**query_parameters)
    except weaviate.exceptions.WeaviateQueryError as e:
        raise ValueError(f"Invalid query, got errors: {e.message}")

    # parse results
    return self.parse_query_result(query_result, query)

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/weaviate/#llama_index.vector_stores.weaviate.WeaviateVectorStore.aquery "Permanent link")

```
aquery(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Raises:  
| Type  | Description  |  
| --- | --- |  
|   |  If trying to use async methods without aclient  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-weaviate/llama_index/vector_stores/weaviate/base.py`  
| 
```
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
```
 | 
```
async defaquery(
    self, query: VectorStoreQuery, **kwargs: Any
) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Raises:
        AsyncClientNotProvidedError: If trying to use async methods without aclient

    """
    collection = self.async_client.collections.get(self.index_name)
    property_types = await self._aget_property_types()
    query_parameters = self.get_query_parameters(
        query, property_types=property_types, **kwargs
    )

    # execute query
    try:
        query_result = await collection.query.hybrid(**query_parameters)
    except weaviate.exceptions.WeaviateQueryError as e:
        raise ValueError(f"Invalid query, got errors: {e.message}")

    # parse results
    return self.parse_query_result(query_result, query)

```
 |  
| --- | --- |  
##  AsyncClientNotProvidedError [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/weaviate/#llama_index.vector_stores.weaviate.AsyncClientNotProvidedError "Permanent link")
Bases: `Exception`
Exception raised when the async weaviate client was not provided via the `weaviate_client` parameter.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-weaviate/llama_index/vector_stores/weaviate/_exceptions.py`  
| 
```
12
13
14
15
16
17
18
19
20
```
 | 
```
classAsyncClientNotProvidedError(Exception):
"""Exception raised when the async weaviate client was not provided via  the `weaviate_client` parameter."""

    def__init__(
        self,
        message="Async method called without WeaviateAsyncClient provided. Pass the async weaviate client to be used via `weaviate_client` to the constructor of WeaviateVectorStore.",
    ) -> None:
        self.message = message
        super().__init__(self.message)

```
 |  
| --- | --- |  
##  SyncClientNotProvidedError [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/weaviate/#llama_index.vector_stores.weaviate.SyncClientNotProvidedError "Permanent link")
Bases: `Exception`
Exception raised when no synchronous weaviate client was provided via the `weaviate_client` parameter.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-weaviate/llama_index/vector_stores/weaviate/_exceptions.py`  
| 
```
1
2
3
4
5
6
7
8
9
```
 | 
```
classSyncClientNotProvidedError(Exception):
"""Exception raised when no synchronous weaviate client was provided via  the `weaviate_client` parameter."""

    def__init__(
        self,
        message="Sync method called without a synchronous WeaviateClient provided. Either switch to using async methods together with a provided WeaviateAsyncClient or provide a synchronous WeaviateClient via `weaviate_client` to the constructor of WeaviateVectorStore.",
    ) -> None:
        self.message = message
        super().__init__(self.message)

```
 |  
| --- | --- |  
options: members: - WeaviateVectorStore
