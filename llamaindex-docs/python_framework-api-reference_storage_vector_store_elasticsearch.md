# Elasticsearch
##  ElasticsearchStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/elasticsearch/#llama_index.vector_stores.elasticsearch.ElasticsearchStore "Permanent link")
Bases: 
Elasticsearch vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index_name`  |  Name of the Elasticsearch index.  |  _required_  |  
|  `es_client`  |  `Optional[Any]`  |  Optional. Pre-existing AsyncElasticsearch client.  |  `None`  |  
|  `es_url`  |  `Optional[str]`  |  Optional. Elasticsearch URL.  |  `None`  |  
|  `es_cloud_id`  |  `Optional[str]`  |  Optional. Elasticsearch cloud ID.  |  `None`  |  
|  `es_api_key`  |  `Optional[str]`  |  Optional. Elasticsearch API key.  |  `None`  |  
|  `es_user`  |  `Optional[str]`  |  Optional. Elasticsearch username.  |  `None`  |  
|  `es_password`  |  `Optional[str]`  |  Optional. Elasticsearch password.  |  `None`  |  
|  `text_field`  |  Optional. Name of the Elasticsearch field that stores the text.  |  `'content'`  |  
|  `vector_field`  |  Optional. Name of the Elasticsearch field that stores the embedding.  |  `'embedding'`  |  
|  `batch_size`  |  Optional. Batch size for bulk indexing. Defaults to 200.  |  `200`  |  
|  `distance_strategy`  |  `Optional[DISTANCE_STRATEGIES]`  |  Optional. Distance strategy to use for similarity search. Defaults to "COSINE".  |  `'COSINE'`  |  
|  `retrieval_strategy`  |  `Optional[AsyncRetrievalStrategy]`  |  Retrieval strategy to use. AsyncBM25Strategy / AsyncSparseVectorStrategy / AsyncDenseVectorStrategy / AsyncRetrievalStrategy. Defaults to AsyncDenseVectorStrategy.  |  `None`  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ConnectionError`  |  If AsyncElasticsearch client cannot connect to Elasticsearch.  |  
|  `ValueError`  |  If neither es_client nor es_url nor es_cloud_id is provided.  |  
Examples:
`pip install llama-index-vector-stores-elasticsearch`

```
fromllama_index.vector_storesimport ElasticsearchStore

# Additional setup for ElasticsearchStore class
index_name = "my_index"
es_url = "http://localhost:9200"
es_cloud_id = "<cloud-id>"  # Found within the deployment page
es_user = "elastic"
es_password = "<password>"  # Provided when creating deployment or can be reset
es_api_key = "<api-key>"  # Create an API key within Kibana (Security -> API Keys)

# Connecting to ElasticsearchStore locally
es_local = ElasticsearchStore(
    index_name=index_name,
    es_url=es_url,
)

# Connecting to Elastic Cloud with username and password
es_cloud_user_pass = ElasticsearchStore(
    index_name=index_name,
    es_cloud_id=es_cloud_id,
    es_user=es_user,
    es_password=es_password,
)

# Connecting to Elastic Cloud with API Key
es_cloud_api_key = ElasticsearchStore(
    index_name=index_name,
    es_cloud_id=es_cloud_id,
    es_api_key=es_api_key,
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-elasticsearch/llama_index/vector_stores/elasticsearch/base.py`  
| 
```
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
```
 | 
```
classElasticsearchStore(BasePydanticVectorStore):
"""
    Elasticsearch vector store.

    Args:
        index_name: Name of the Elasticsearch index.
        es_client: Optional. Pre-existing AsyncElasticsearch client.
        es_url: Optional. Elasticsearch URL.
        es_cloud_id: Optional. Elasticsearch cloud ID.
        es_api_key: Optional. Elasticsearch API key.
        es_user: Optional. Elasticsearch username.
        es_password: Optional. Elasticsearch password.
        text_field: Optional. Name of the Elasticsearch field that stores the text.
        vector_field: Optional. Name of the Elasticsearch field that stores the
                    embedding.
        batch_size: Optional. Batch size for bulk indexing. Defaults to 200.
        distance_strategy: Optional. Distance strategy to use for similarity search.
                        Defaults to "COSINE".
        retrieval_strategy: Retrieval strategy to use. AsyncBM25Strategy /
            AsyncSparseVectorStrategy / AsyncDenseVectorStrategy / AsyncRetrievalStrategy.
            Defaults to AsyncDenseVectorStrategy.

    Raises:
        ConnectionError: If AsyncElasticsearch client cannot connect to Elasticsearch.
        ValueError: If neither es_client nor es_url nor es_cloud_id is provided.

    Examples:
        `pip install llama-index-vector-stores-elasticsearch`

        ```python
        from llama_index.vector_stores import ElasticsearchStore

        # Additional setup for ElasticsearchStore class
        index_name = "my_index"
        es_url = "http://localhost:9200"
        es_cloud_id = "<cloud-id>"  # Found within the deployment page
        es_user = "elastic"
        es_password = "<password>"  # Provided when creating deployment or can be reset
        es_api_key = "<api-key>"  # Create an API key within Kibana (Security -> API Keys)

        # Connecting to ElasticsearchStore locally
        es_local = ElasticsearchStore(
            index_name=index_name,
            es_url=es_url,


        # Connecting to Elastic Cloud with username and password
        es_cloud_user_pass = ElasticsearchStore(
            index_name=index_name,
            es_cloud_id=es_cloud_id,
            es_user=es_user,
            es_password=es_password,


        # Connecting to Elastic Cloud with API Key
        es_cloud_api_key = ElasticsearchStore(
            index_name=index_name,
            es_cloud_id=es_cloud_id,
            es_api_key=es_api_key,

        ```

    """

    classConfig:
        # allow pydantic to tolarate its inability to validate AsyncRetrievalStrategy
        arbitrary_types_allowed = True

    stores_text: bool = True
    index_name: str
    es_client: Optional[Any]
    es_url: Optional[str]
    es_cloud_id: Optional[str]
    es_api_key: Optional[str]
    es_user: Optional[str]
    es_password: Optional[str]
    text_field: str = "content"
    vector_field: str = "embedding"
    batch_size: int = 200
    distance_strategy: Optional[DISTANCE_STRATEGIES] = "COSINE"
    retrieval_strategy: AsyncRetrievalStrategy

    _store = PrivateAttr()

    def__init__(
        self,
        index_name: str,
        es_client: Optional[Any] = None,
        es_url: Optional[str] = None,
        es_cloud_id: Optional[str] = None,
        es_api_key: Optional[str] = None,
        es_user: Optional[str] = None,
        es_password: Optional[str] = None,
        text_field: str = "content",
        vector_field: str = "embedding",
        batch_size: int = 200,
        distance_strategy: Optional[DISTANCE_STRATEGIES] = "COSINE",
        retrieval_strategy: Optional[AsyncRetrievalStrategy] = None,
        metadata_mappings: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        nest_asyncio.apply()

        if not es_client:
            es_client = get_elasticsearch_client(
                url=es_url,
                cloud_id=es_cloud_id,
                api_key=es_api_key,
                username=es_user,
                password=es_password,
            )

        if retrieval_strategy is None:
            retrieval_strategy = AsyncDenseVectorStrategy(
                distance=DistanceMetric[distance_strategy]
            )

        base_metadata_mappings = {
            "document_id": {"type": "keyword"},
            "doc_id": {"type": "keyword"},
            "ref_doc_id": {"type": "keyword"},
        }

        metadata_mappings = metadata_mappings or {}
        metadata_mappings.update(base_metadata_mappings)

        super().__init__(
            index_name=index_name,
            es_client=es_client,
            es_url=es_url,
            es_cloud_id=es_cloud_id,
            es_api_key=es_api_key,
            es_user=es_user,
            es_password=es_password,
            text_field=text_field,
            vector_field=vector_field,
            batch_size=batch_size,
            distance_strategy=distance_strategy,
            retrieval_strategy=retrieval_strategy,
        )

        self._store = AsyncVectorStore(
            user_agent=get_user_agent(),
            client=es_client,
            index=index_name,
            retrieval_strategy=retrieval_strategy,
            text_field=text_field,
            vector_field=vector_field,
            metadata_mappings=metadata_mappings,
        )

        # Disable query embeddings when using Sparse vectors or BM25.
        # ELSER generates its own embeddings server-side
        if not isinstance(retrieval_strategy, AsyncDenseVectorStrategy):
            self.is_embedding_query = False

    @property
    defclient(self) -> Any:
"""Get async elasticsearch client."""
        return self._store.client

    defclose(self) -> None:
        return asyncio.get_event_loop().run_until_complete(self._store.close())

    defadd(
        self,
        nodes: List[BaseNode],
        *,
        create_index_if_not_exists: bool = True,
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to Elasticsearch index.

        Args:
            nodes: List of nodes with embeddings.
            create_index_if_not_exists: Optional. Whether to create
                                        the Elasticsearch index if it
                                        doesn't already exist.
                                        Defaults to True.

        Returns:
            List of node IDs that were added to the index.

        Raises:
            ImportError: If elasticsearch['async'] python package is not installed.
            BulkIndexError: If AsyncElasticsearch async_bulk indexing fails.

        """
        return asyncio.get_event_loop().run_until_complete(
            self.async_add(
                nodes,
                create_index_if_not_exists=create_index_if_not_exists,
                **add_kwargs,
            )
        )

    async defasync_add(
        self,
        nodes: List[BaseNode],
        *,
        create_index_if_not_exists: bool = True,
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Asynchronous method to add nodes to Elasticsearch index.

        Args:
            nodes: List of nodes with embeddings.
            create_index_if_not_exists: Optional. Whether to create
                                        the AsyncElasticsearch index if it
                                        doesn't already exist.
                                        Defaults to True.

        Returns:
            List of node IDs that were added to the index.

        Raises:
            ImportError: If elasticsearch python package is not installed.
            BulkIndexError: If AsyncElasticsearch async_bulk indexing fails.

        """
        if len(nodes) == 0:
            return []

        embeddings: Optional[List[List[float]]] = None
        texts: List[str] = []
        metadatas: List[dict] = []
        ids: List[str] = []
        for node in nodes:
            ids.append(node.node_id)
            texts.append(node.get_content(metadata_mode=MetadataMode.NONE))
            metadatas.append(node_to_metadata_dict(node, remove_text=True))

        # Generate embeddings when using dense vectors. They are not needed
        # for other strategies.
        if isinstance(self.retrieval_strategy, AsyncDenseVectorStrategy):
            embeddings = []
            for node in nodes:
                embeddings.append(node.get_embedding())

            if not self._store.num_dimensions:
                self._store.num_dimensions = len(embeddings[0])

        return await self._store.add_texts(
            texts=texts,
            metadatas=metadatas,
            vectors=embeddings,
            ids=ids,
            create_index_if_not_exists=create_index_if_not_exists,
            bulk_kwargs=add_kwargs,
        )

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete node from Elasticsearch index.

        Args:
            ref_doc_id: ID of the node to delete.
            delete_kwargs: Optional. Additional arguments to
                        pass to Elasticsearch delete_by_query.

        Raises:
            Exception: If Elasticsearch delete_by_query fails.

        """
        return asyncio.get_event_loop().run_until_complete(
            self.adelete(ref_doc_id, **delete_kwargs)
        )

    async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Async delete node from Elasticsearch index.

        Args:
            ref_doc_id: ID of the node to delete.
            delete_kwargs: Optional. Additional arguments to
                        pass to AsyncElasticsearch delete_by_query.

        Raises:
            Exception: If AsyncElasticsearch delete_by_query fails.

        """
        await self._store.delete(
            query={"term": {"metadata.ref_doc_id": ref_doc_id}}, **delete_kwargs
        )

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Delete nodes from vector store using node IDs and filters.

        Args:
            node_ids: Optional list of node IDs to delete.
            filters: Optional metadata filters to select nodes to delete.
            delete_kwargs: Optional additional arguments to pass to delete operation.

        """
        return asyncio.get_event_loop().run_until_complete(
            self.adelete_nodes(node_ids, filters, **delete_kwargs)
        )

    async defadelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Asynchronously delete nodes from vector store using node IDs and filters.

        Args:
            node_ids (Optional[List[str]], optional): List of node IDs. Defaults to None.
            filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.
            delete_kwargs (Any, optional): Optional additional arguments to pass to delete operation.

        """
        if not node_ids and not filters:
            return

        if node_ids and not filters:
            await self._store.delete(ids=node_ids, **delete_kwargs)
            return

        query = {"bool": {"must": []}}

        if node_ids:
            query["bool"]["must"].append({"terms": {"_id": node_ids}})

        if filters:
            es_filter = _to_elasticsearch_filter(filters)
            if "bool" in es_filter and "must" in es_filter["bool"]:
                query["bool"]["must"].extend(es_filter["bool"]["must"])
            else:
                query["bool"]["must"].append(es_filter)

        await self._store.delete(query=query, **delete_kwargs)

    defquery(
        self,
        query: VectorStoreQuery,
        custom_query: Optional[
            Callable[[Dict, Union[VectorStoreQuery, None]], Dict]
        ] = None,
        es_filter: Optional[List[Dict]] = None,
        metadata_keyword_suffix: str = ".keyword",
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query_embedding (List[float]): query embedding
            custom_query: Optional. custom query function that takes in the es query
                        body and returns a modified query body.
                        This can be used to add additional query
                        parameters to the Elasticsearch query.
            es_filter: Optional. Elasticsearch filter to apply to the
                        query. If filter is provided in the query,
                        this filter will be ignored.
            metadata_keyword_suffix (str): The suffix to append to the metadata field of the keyword type.

        Returns:
            VectorStoreQueryResult: Result of the query.

        Raises:
            Exception: If Elasticsearch query fails.

        """
        return asyncio.get_event_loop().run_until_complete(
            self.aquery(query, custom_query, es_filter, **kwargs)
        )

    async defaquery(
        self,
        query: VectorStoreQuery,
        custom_query: Optional[
            Callable[[Dict, Union[VectorStoreQuery, None]], Dict]
        ] = None,
        es_filter: Optional[List[Dict]] = None,
        metadata_keyword_suffix: str = ".keyword",
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""
        Asynchronous query index for top k most similar nodes.

        Args:
            query_embedding (VectorStoreQuery): query embedding
            custom_query: Optional. custom query function that takes in the es query
                        body and returns a modified query body.
                        This can be used to add additional query
                        parameters to the AsyncElasticsearch query.
            es_filter: Optional. AsyncElasticsearch filter to apply to the
                        query. If filter is provided in the query,
                        this filter will be ignored.
            metadata_keyword_suffix (str): The suffix to append to the metadata field of the keyword type.

        Returns:
            VectorStoreQueryResult: Result of the query.

        Raises:
            Exception: If AsyncElasticsearch query fails.

        """
        _mode_must_match_retrieval_strategy(query.mode, self.retrieval_strategy)

        if query.filters is not None and len(query.filters.legacy_filters())  0:
            filter = [_to_elasticsearch_filter(query.filters, metadata_keyword_suffix)]
        else:
            filter = es_filter or []

        hits = await self._store.search(
            query=query.query_str,
            query_vector=query.query_embedding,
            k=query.similarity_top_k,
            num_candidates=query.similarity_top_k * 10,
            filter=filter,
            custom_query=custom_query,
        )

        top_k_nodes = []
        top_k_ids = []
        top_k_scores = []

        for hit in hits:
            node = convert_es_hit_to_node(hit, self.text_field)
            top_k_nodes.append(node)
            top_k_ids.append(hit["_id"])
            top_k_scores.append(hit["_score"])

        return VectorStoreQueryResult(
            nodes=top_k_nodes,
            ids=top_k_ids,
            similarities=_to_llama_similarities(top_k_scores),
        )

    defget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> List[BaseNode]:
"""
        Get nodes from Elasticsearch index.

        Args:
            node_ids (Optional[List[str]]): List of node IDs to retrieve.
            filters (Optional[MetadataFilters]): Metadata filters to apply.

        Returns:
            List[BaseNode]: List of nodes retrieved from the index.

        """
        return asyncio.get_event_loop().run_until_complete(
            self.aget_nodes(node_ids, filters)
        )

    async defaget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> List[BaseNode]:
"""
        Asynchronously get nodes from Elasticsearch index.

        Args:
            node_ids (Optional[List[str]]): List of node IDs to retrieve.
            filters (Optional[MetadataFilters]): Metadata filters to apply.

        Returns:
            List[BaseNode]: List of nodes retrieved from the index.

        Raises:
            ValueError: If neither node_ids nor filters is provided.

        """
        if not node_ids and not filters:
            raise ValueError("Either node_ids or filters must be provided.")

        query = {"bool": {"must": []}}

        if node_ids is not None:
            query["bool"]["must"].append({"terms": {"_id": node_ids}})

        if filters:
            es_filter = _to_elasticsearch_filter(filters)
            if "bool" in es_filter and "must" in es_filter["bool"]:
                query["bool"]["must"].extend(es_filter["bool"]["must"])
            else:
                query["bool"]["must"].append(es_filter)

        response = await self._store.client.search(
            index=self.index_name,
            body={"query": query, "size": 10000},
        )

        hits = response.get("hits", {}).get("hits", [])
        nodes = []

        for hit in hits:
            nodes.append(convert_es_hit_to_node(hit, self.text_field))

        return nodes

    defclear(self) -> None:
"""
        Clear all nodes from Elasticsearch index.
        This method deletes and recreates the index.
        """
        return asyncio.get_event_loop().run_until_complete(self.aclear())

    async defaclear(self) -> None:
"""
        Asynchronously clear all nodes from Elasticsearch index.
        This method deletes and recreates the index.
        """
        if await self._store.client.indices.exists(index=self.index_name):
            await self._store.client.indices.delete(index=self.index_name)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/elasticsearch/#llama_index.vector_stores.elasticsearch.ElasticsearchStore.client "Permanent link")

```
client: 

```

Get async elasticsearch client.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/elasticsearch/#llama_index.vector_stores.elasticsearch.ElasticsearchStore.add "Permanent link")

```
add(
    nodes: [],
    *,
    create_index_if_not_exists:  = True,
    **add_kwargs: 
) -> []

```

Add nodes to Elasticsearch index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes with embeddings.  |  _required_  |  
|  `create_index_if_not_exists`  |  `bool`  |  Optional. Whether to create the Elasticsearch index if it doesn't already exist. Defaults to True.  |  `True`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List of node IDs that were added to the index.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ImportError`  |  If elasticsearch['async'] python package is not installed.  |  
|  `BulkIndexError`  |  If AsyncElasticsearch async_bulk indexing fails.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-elasticsearch/llama_index/vector_stores/elasticsearch/base.py`  
| 
```
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
```
 | 
```
defadd(
    self,
    nodes: List[BaseNode],
    *,
    create_index_if_not_exists: bool = True,
    **add_kwargs: Any,
) -> List[str]:
"""
    Add nodes to Elasticsearch index.

    Args:
        nodes: List of nodes with embeddings.
        create_index_if_not_exists: Optional. Whether to create
                                    the Elasticsearch index if it
                                    doesn't already exist.
                                    Defaults to True.

    Returns:
        List of node IDs that were added to the index.

    Raises:
        ImportError: If elasticsearch['async'] python package is not installed.
        BulkIndexError: If AsyncElasticsearch async_bulk indexing fails.

    """
    return asyncio.get_event_loop().run_until_complete(
        self.async_add(
            nodes,
            create_index_if_not_exists=create_index_if_not_exists,
            **add_kwargs,
        )
    )

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/elasticsearch/#llama_index.vector_stores.elasticsearch.ElasticsearchStore.async_add "Permanent link")

```
async_add(
    nodes: [],
    *,
    create_index_if_not_exists:  = True,
    **add_kwargs: 
) -> []

```

Asynchronous method to add nodes to Elasticsearch index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes with embeddings.  |  _required_  |  
|  `create_index_if_not_exists`  |  `bool`  |  Optional. Whether to create the AsyncElasticsearch index if it doesn't already exist. Defaults to True.  |  `True`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List of node IDs that were added to the index.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ImportError`  |  If elasticsearch python package is not installed.  |  
|  `BulkIndexError`  |  If AsyncElasticsearch async_bulk indexing fails.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-elasticsearch/llama_index/vector_stores/elasticsearch/base.py`  
| 
```
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
```
 | 
```
async defasync_add(
    self,
    nodes: List[BaseNode],
    *,
    create_index_if_not_exists: bool = True,
    **add_kwargs: Any,
) -> List[str]:
"""
    Asynchronous method to add nodes to Elasticsearch index.

    Args:
        nodes: List of nodes with embeddings.
        create_index_if_not_exists: Optional. Whether to create
                                    the AsyncElasticsearch index if it
                                    doesn't already exist.
                                    Defaults to True.

    Returns:
        List of node IDs that were added to the index.

    Raises:
        ImportError: If elasticsearch python package is not installed.
        BulkIndexError: If AsyncElasticsearch async_bulk indexing fails.

    """
    if len(nodes) == 0:
        return []

    embeddings: Optional[List[List[float]]] = None
    texts: List[str] = []
    metadatas: List[dict] = []
    ids: List[str] = []
    for node in nodes:
        ids.append(node.node_id)
        texts.append(node.get_content(metadata_mode=MetadataMode.NONE))
        metadatas.append(node_to_metadata_dict(node, remove_text=True))

    # Generate embeddings when using dense vectors. They are not needed
    # for other strategies.
    if isinstance(self.retrieval_strategy, AsyncDenseVectorStrategy):
        embeddings = []
        for node in nodes:
            embeddings.append(node.get_embedding())

        if not self._store.num_dimensions:
            self._store.num_dimensions = len(embeddings[0])

    return await self._store.add_texts(
        texts=texts,
        metadatas=metadatas,
        vectors=embeddings,
        ids=ids,
        create_index_if_not_exists=create_index_if_not_exists,
        bulk_kwargs=add_kwargs,
    )

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/elasticsearch/#llama_index.vector_stores.elasticsearch.ElasticsearchStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete node from Elasticsearch index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  ID of the node to delete.  |  _required_  |  
|  `delete_kwargs`  |  Optional. Additional arguments to pass to Elasticsearch delete_by_query.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `Exception`  |  If Elasticsearch delete_by_query fails.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-elasticsearch/llama_index/vector_stores/elasticsearch/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete node from Elasticsearch index.

    Args:
        ref_doc_id: ID of the node to delete.
        delete_kwargs: Optional. Additional arguments to
                    pass to Elasticsearch delete_by_query.

    Raises:
        Exception: If Elasticsearch delete_by_query fails.

    """
    return asyncio.get_event_loop().run_until_complete(
        self.adelete(ref_doc_id, **delete_kwargs)
    )

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/elasticsearch/#llama_index.vector_stores.elasticsearch.ElasticsearchStore.adelete "Permanent link")

```
adelete(ref_doc_id: , **delete_kwargs: ) -> None

```

Async delete node from Elasticsearch index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  ID of the node to delete.  |  _required_  |  
|  `delete_kwargs`  |  Optional. Additional arguments to pass to AsyncElasticsearch delete_by_query.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `Exception`  |  If AsyncElasticsearch delete_by_query fails.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-elasticsearch/llama_index/vector_stores/elasticsearch/base.py`  
| 
```
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
```
 | 
```
async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Async delete node from Elasticsearch index.

    Args:
        ref_doc_id: ID of the node to delete.
        delete_kwargs: Optional. Additional arguments to
                    pass to AsyncElasticsearch delete_by_query.

    Raises:
        Exception: If AsyncElasticsearch delete_by_query fails.

    """
    await self._store.delete(
        query={"term": {"metadata.ref_doc_id": ref_doc_id}}, **delete_kwargs
    )

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/elasticsearch/#llama_index.vector_stores.elasticsearch.ElasticsearchStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Delete nodes from vector store using node IDs and filters.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  Optional list of node IDs to delete.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Optional metadata filters to select nodes to delete.  |  `None`  |  
|  `delete_kwargs`  |  Optional additional arguments to pass to delete operation.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-elasticsearch/llama_index/vector_stores/elasticsearch/base.py`  
| 
```
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
    Delete nodes from vector store using node IDs and filters.

    Args:
        node_ids: Optional list of node IDs to delete.
        filters: Optional metadata filters to select nodes to delete.
        delete_kwargs: Optional additional arguments to pass to delete operation.

    """
    return asyncio.get_event_loop().run_until_complete(
        self.adelete_nodes(node_ids, filters, **delete_kwargs)
    )

```
 |  
| --- | --- |  
###  adelete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/elasticsearch/#llama_index.vector_stores.elasticsearch.ElasticsearchStore.adelete_nodes "Permanent link")

```
adelete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Asynchronously delete nodes from vector store using node IDs and filters.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  List of node IDs. Defaults to None.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters. Defaults to None.  |  `None`  |  
|  `delete_kwargs`  |  Optional additional arguments to pass to delete operation.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-elasticsearch/llama_index/vector_stores/elasticsearch/base.py`  
| 
```
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
    Asynchronously delete nodes from vector store using node IDs and filters.

    Args:
        node_ids (Optional[List[str]], optional): List of node IDs. Defaults to None.
        filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.
        delete_kwargs (Any, optional): Optional additional arguments to pass to delete operation.

    """
    if not node_ids and not filters:
        return

    if node_ids and not filters:
        await self._store.delete(ids=node_ids, **delete_kwargs)
        return

    query = {"bool": {"must": []}}

    if node_ids:
        query["bool"]["must"].append({"terms": {"_id": node_ids}})

    if filters:
        es_filter = _to_elasticsearch_filter(filters)
        if "bool" in es_filter and "must" in es_filter["bool"]:
            query["bool"]["must"].extend(es_filter["bool"]["must"])
        else:
            query["bool"]["must"].append(es_filter)

    await self._store.delete(query=query, **delete_kwargs)

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/elasticsearch/#llama_index.vector_stores.elasticsearch.ElasticsearchStore.query "Permanent link")

```
query(
    query: ,
    custom_query: Optional[
        Callable[
            [, Union[, None]], 
        ]
    ] = None,
    es_filter: Optional[[]] = None,
    metadata_keyword_suffix:  = ".keyword",
    **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_embedding`  |  `List[float]`  |  query embedding  |  _required_  |  
|  `custom_query`  |  `Optional[Callable[[Dict, Union[VectorStoreQuery[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.VectorStoreQuery "VectorStoreQuery


  
      dataclass
   \(llama_index.core.vector_stores.types.VectorStoreQuery\)"), None]], Dict]]`  |  Optional. custom query function that takes in the es query body and returns a modified query body. This can be used to add additional query parameters to the Elasticsearch query.  |  `None`  |  
|  `es_filter`  |  `Optional[List[Dict]]`  |  Optional. Elasticsearch filter to apply to the query. If filter is provided in the query, this filter will be ignored.  |  `None`  |  
|  `metadata_keyword_suffix`  |  The suffix to append to the metadata field of the keyword type.  |  `'.keyword'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  Result of the query.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `Exception`  |  If Elasticsearch query fails.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-elasticsearch/llama_index/vector_stores/elasticsearch/base.py`  
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
```
 | 
```
defquery(
    self,
    query: VectorStoreQuery,
    custom_query: Optional[
        Callable[[Dict, Union[VectorStoreQuery, None]], Dict]
    ] = None,
    es_filter: Optional[List[Dict]] = None,
    metadata_keyword_suffix: str = ".keyword",
    **kwargs: Any,
) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query_embedding (List[float]): query embedding
        custom_query: Optional. custom query function that takes in the es query
                    body and returns a modified query body.
                    This can be used to add additional query
                    parameters to the Elasticsearch query.
        es_filter: Optional. Elasticsearch filter to apply to the
                    query. If filter is provided in the query,
                    this filter will be ignored.
        metadata_keyword_suffix (str): The suffix to append to the metadata field of the keyword type.

    Returns:
        VectorStoreQueryResult: Result of the query.

    Raises:
        Exception: If Elasticsearch query fails.

    """
    return asyncio.get_event_loop().run_until_complete(
        self.aquery(query, custom_query, es_filter, **kwargs)
    )

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/elasticsearch/#llama_index.vector_stores.elasticsearch.ElasticsearchStore.aquery "Permanent link")

```
aquery(
    query: ,
    custom_query: Optional[
        Callable[
            [, Union[, None]], 
        ]
    ] = None,
    es_filter: Optional[[]] = None,
    metadata_keyword_suffix:  = ".keyword",
    **kwargs: 
) -> 

```

Asynchronous query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_embedding`  |   |  query embedding  |  _required_  |  
|  `custom_query`  |  `Optional[Callable[[Dict, Union[VectorStoreQuery[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.VectorStoreQuery "VectorStoreQuery


  
      dataclass
   \(llama_index.core.vector_stores.types.VectorStoreQuery\)"), None]], Dict]]`  |  Optional. custom query function that takes in the es query body and returns a modified query body. This can be used to add additional query parameters to the AsyncElasticsearch query.  |  `None`  |  
|  `es_filter`  |  `Optional[List[Dict]]`  |  Optional. AsyncElasticsearch filter to apply to the query. If filter is provided in the query, this filter will be ignored.  |  `None`  |  
|  `metadata_keyword_suffix`  |  The suffix to append to the metadata field of the keyword type.  |  `'.keyword'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  Result of the query.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `Exception`  |  If AsyncElasticsearch query fails.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-elasticsearch/llama_index/vector_stores/elasticsearch/base.py`  
| 
```
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
```
 | 
```
async defaquery(
    self,
    query: VectorStoreQuery,
    custom_query: Optional[
        Callable[[Dict, Union[VectorStoreQuery, None]], Dict]
    ] = None,
    es_filter: Optional[List[Dict]] = None,
    metadata_keyword_suffix: str = ".keyword",
    **kwargs: Any,
) -> VectorStoreQueryResult:
"""
    Asynchronous query index for top k most similar nodes.

    Args:
        query_embedding (VectorStoreQuery): query embedding
        custom_query: Optional. custom query function that takes in the es query
                    body and returns a modified query body.
                    This can be used to add additional query
                    parameters to the AsyncElasticsearch query.
        es_filter: Optional. AsyncElasticsearch filter to apply to the
                    query. If filter is provided in the query,
                    this filter will be ignored.
        metadata_keyword_suffix (str): The suffix to append to the metadata field of the keyword type.

    Returns:
        VectorStoreQueryResult: Result of the query.

    Raises:
        Exception: If AsyncElasticsearch query fails.

    """
    _mode_must_match_retrieval_strategy(query.mode, self.retrieval_strategy)

    if query.filters is not None and len(query.filters.legacy_filters())  0:
        filter = [_to_elasticsearch_filter(query.filters, metadata_keyword_suffix)]
    else:
        filter = es_filter or []

    hits = await self._store.search(
        query=query.query_str,
        query_vector=query.query_embedding,
        k=query.similarity_top_k,
        num_candidates=query.similarity_top_k * 10,
        filter=filter,
        custom_query=custom_query,
    )

    top_k_nodes = []
    top_k_ids = []
    top_k_scores = []

    for hit in hits:
        node = convert_es_hit_to_node(hit, self.text_field)
        top_k_nodes.append(node)
        top_k_ids.append(hit["_id"])
        top_k_scores.append(hit["_score"])

    return VectorStoreQueryResult(
        nodes=top_k_nodes,
        ids=top_k_ids,
        similarities=_to_llama_similarities(top_k_scores),
    )

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/elasticsearch/#llama_index.vector_stores.elasticsearch.ElasticsearchStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Get nodes from Elasticsearch index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  List of node IDs to retrieve.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters to apply.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[BaseNode]: List of nodes retrieved from the index.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-elasticsearch/llama_index/vector_stores/elasticsearch/base.py`  
| 
```
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
```
 | 
```
defget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> List[BaseNode]:
"""
    Get nodes from Elasticsearch index.

    Args:
        node_ids (Optional[List[str]]): List of node IDs to retrieve.
        filters (Optional[MetadataFilters]): Metadata filters to apply.

    Returns:
        List[BaseNode]: List of nodes retrieved from the index.

    """
    return asyncio.get_event_loop().run_until_complete(
        self.aget_nodes(node_ids, filters)
    )

```
 |  
| --- | --- |  
###  aget_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/elasticsearch/#llama_index.vector_stores.elasticsearch.ElasticsearchStore.aget_nodes "Permanent link")

```
aget_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Asynchronously get nodes from Elasticsearch index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  List of node IDs to retrieve.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters to apply.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[BaseNode]: List of nodes retrieved from the index.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If neither node_ids nor filters is provided.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-elasticsearch/llama_index/vector_stores/elasticsearch/base.py`  
| 
```
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
```
 | 
```
async defaget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> List[BaseNode]:
"""
    Asynchronously get nodes from Elasticsearch index.

    Args:
        node_ids (Optional[List[str]]): List of node IDs to retrieve.
        filters (Optional[MetadataFilters]): Metadata filters to apply.

    Returns:
        List[BaseNode]: List of nodes retrieved from the index.

    Raises:
        ValueError: If neither node_ids nor filters is provided.

    """
    if not node_ids and not filters:
        raise ValueError("Either node_ids or filters must be provided.")

    query = {"bool": {"must": []}}

    if node_ids is not None:
        query["bool"]["must"].append({"terms": {"_id": node_ids}})

    if filters:
        es_filter = _to_elasticsearch_filter(filters)
        if "bool" in es_filter and "must" in es_filter["bool"]:
            query["bool"]["must"].extend(es_filter["bool"]["must"])
        else:
            query["bool"]["must"].append(es_filter)

    response = await self._store.client.search(
        index=self.index_name,
        body={"query": query, "size": 10000},
    )

    hits = response.get("hits", {}).get("hits", [])
    nodes = []

    for hit in hits:
        nodes.append(convert_es_hit_to_node(hit, self.text_field))

    return nodes

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/elasticsearch/#llama_index.vector_stores.elasticsearch.ElasticsearchStore.clear "Permanent link")

```
clear() -> None

```

Clear all nodes from Elasticsearch index. This method deletes and recreates the index.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-elasticsearch/llama_index/vector_stores/elasticsearch/base.py`  
| 
```
631
632
633
634
635
636
```
 | 
```
defclear(self) -> None:
"""
    Clear all nodes from Elasticsearch index.
    This method deletes and recreates the index.
    """
    return asyncio.get_event_loop().run_until_complete(self.aclear())

```
 |  
| --- | --- |  
###  aclear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/elasticsearch/#llama_index.vector_stores.elasticsearch.ElasticsearchStore.aclear "Permanent link")

```
aclear() -> None

```

Asynchronously clear all nodes from Elasticsearch index. This method deletes and recreates the index.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-elasticsearch/llama_index/vector_stores/elasticsearch/base.py`  
| 
```
638
639
640
641
642
643
644
```
 | 
```
async defaclear(self) -> None:
"""
    Asynchronously clear all nodes from Elasticsearch index.
    This method deletes and recreates the index.
    """
    if await self._store.client.indices.exists(index=self.index_name):
        await self._store.client.indices.delete(index=self.index_name)

```
 |  
| --- | --- |  
options: members: - ElasticsearchStore
