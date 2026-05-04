# Chroma
##  ChromaVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/chroma/#llama_index.vector_stores.chroma.ChromaVectorStore "Permanent link")
Bases: 
Chroma vector store.
In this vector store, embeddings are stored within a ChromaDB collection.
During query time, the index uses ChromaDB to query for the top k most similar nodes.
Supports MMR (Maximum Marginal Relevance) search mode for improved diversity in search results.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `chroma_collection`  |  `Collection`  |  ChromaDB collection instance  |  `None`  |  
Examples:
`uv add llama-index-vector-stores-chroma`

```
importchromadb
fromllama_index.vector_stores.chromaimport ChromaVectorStore

# Create a Chroma client and collection
chroma_client = chromadb.EphemeralClient()
chroma_collection = chroma_client.create_collection("example_collection")

# Set up the ChromaVectorStore and StorageContext
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Use MMR mode with threshold
query_engine = index.as_query_engine(
    vector_store_query_mode="mmr",
    vector_store_kwargs={"mmr_threshold": 0.5}
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-chroma/llama_index/vector_stores/chroma/base.py`  
| 
```
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
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
```
 | 
```
classChromaVectorStore(BasePydanticVectorStore):
"""
    Chroma vector store.

    In this vector store, embeddings are stored within a ChromaDB collection.

    During query time, the index uses ChromaDB to query for the top
    k most similar nodes.

    Supports MMR (Maximum Marginal Relevance) search mode for improved diversity
    in search results.

    Args:
        chroma_collection (chromadb.api.models.Collection.Collection):
            ChromaDB collection instance

    Examples:
        `uv add llama-index-vector-stores-chroma`

        ```python
        import chromadb
        from llama_index.vector_stores.chroma import ChromaVectorStore

        # Create a Chroma client and collection
        chroma_client = chromadb.EphemeralClient()
        chroma_collection = chroma_client.create_collection("example_collection")

        # Set up the ChromaVectorStore and StorageContext
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

        # Use MMR mode with threshold
        query_engine = index.as_query_engine(
            vector_store_query_mode="mmr",
            vector_store_kwargs={"mmr_threshold": 0.5}

        ```

    """

    stores_text: bool = True
    flat_metadata: bool = True

    collection_name: Optional[str]
    host: Optional[str]
    port: Optional[Union[str, int]]
    ssl: bool
    headers: Optional[Dict[str, str]]
    persist_dir: Optional[str]
    collection_kwargs: Dict[str, Any] = Field(default_factory=dict)

    _collection: Collection = PrivateAttr()

    def__init__(
        self,
        chroma_collection: Optional[Any] = None,
        collection_name: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[Union[str, int]] = None,
        ssl: bool = False,
        headers: Optional[Dict[str, str]] = None,
        persist_dir: Optional[str] = None,
        collection_kwargs: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        collection_kwargs = collection_kwargs or {}

        super().__init__(
            host=host,
            port=port,
            ssl=ssl,
            headers=headers,
            collection_name=collection_name,
            persist_dir=persist_dir,
            collection_kwargs=collection_kwargs or {},
        )
        if chroma_collection is None:
            client = chromadb.HttpClient(host=host, port=port, ssl=ssl, headers=headers)
            self._collection = client.get_or_create_collection(
                name=collection_name, **collection_kwargs
            )
        else:
            self._collection = cast(Collection, chroma_collection)

    @classmethod
    deffrom_collection(cls, collection: Any) -> "ChromaVectorStore":
        try:
            fromchromadbimport Collection
        except ImportError:
            raise ImportError(import_err_msg)

        if not isinstance(collection, Collection):
            raise Exception("argument is not chromadb collection instance")

        return cls(chroma_collection=collection)

    @classmethod
    deffrom_params(
        cls,
        collection_name: str,
        host: Optional[str] = None,
        port: Optional[Union[str, int]] = None,
        ssl: bool = False,
        headers: Optional[Dict[str, str]] = None,
        persist_dir: Optional[str] = None,
        collection_kwargs: dict = {},
        **kwargs: Any,
    ) -> "ChromaVectorStore":
        if persist_dir:
            client = chromadb.PersistentClient(path=persist_dir)
            collection = client.get_or_create_collection(
                name=collection_name, **collection_kwargs
            )
        elif host and port:
            client = chromadb.HttpClient(host=host, port=port, ssl=ssl, headers=headers)
            collection = client.get_or_create_collection(
                name=collection_name, **collection_kwargs
            )
        else:
            raise ValueError(
                "Either `persist_dir` or (`host`,`port`) must be specified"
            )
        return cls(
            chroma_collection=collection,
            host=host,
            port=port,
            ssl=ssl,
            headers=headers,
            persist_dir=persist_dir,
            collection_kwargs=collection_kwargs,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "ChromaVectorStore"

    defget_nodes(
        self,
        node_ids: Optional[List[str]],
        filters: Optional[List[MetadataFilters]] = None,
    ) -> List[BaseNode]:
"""
        Get nodes from index.

        Args:
            node_ids (List[str]): list of node ids
            filters (List[MetadataFilters]): list of metadata filters

        """
        if not self._collection:
            raise ValueError("Collection not initialized")

        node_ids = node_ids or None

        if filters:
            where = _to_chroma_filter(filters)
        else:
            where = None

        result = self._get(None, where=where, ids=node_ids)

        return result.nodes

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
        Add nodes to index.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        """
        if not self._collection:
            raise ValueError("Collection not initialized")

        max_chunk_size = MAX_CHUNK_SIZE
        node_chunks = chunk_list(nodes, max_chunk_size)

        all_ids = []
        for node_chunk in node_chunks:
            embeddings = []
            metadatas = []
            ids = []
            documents = []
            for node in node_chunk:
                embeddings.append(node.get_embedding())
                metadata_dict = node_to_metadata_dict(
                    node, remove_text=True, flat_metadata=self.flat_metadata
                )
                for key in metadata_dict:
                    if metadata_dict[key] is None:
                        metadata_dict[key] = ""
                metadatas.append(metadata_dict)
                ids.append(node.node_id)
                documents.append(node.get_content(metadata_mode=MetadataMode.NONE))

            self._collection.add(
                embeddings=embeddings,
                ids=ids,
                metadatas=metadatas,
                documents=documents,
            )
            all_ids.extend(ids)

        return all_ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        self._collection.delete(where={"document_id": ref_doc_id})

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[List[MetadataFilters]] = None,
    ) -> None:
"""
        Delete nodes from index.

        Args:
            node_ids (List[str]): list of node ids
            filters (List[MetadataFilters]): list of metadata filters

        """
        if not self._collection:
            raise ValueError("Collection not initialized")

        node_ids = node_ids or []

        if filters:
            where = _to_chroma_filter(filters)
            self._collection.delete(ids=node_ids, where=where)

        else:
            self._collection.delete(ids=node_ids)

    defclear(self) -> None:
"""Clear the collection."""
        ids = self._collection.get()["ids"]
        self._collection.delete(ids=ids)

    @property
    defclient(self) -> Any:
"""Return client."""
        return self._collection

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query (VectorStoreQuery): Query object containing:
                - query_embedding (List[float]): query embedding
                - similarity_top_k (int): top k most similar nodes
                - filters (Optional[MetadataFilters]): metadata filters to apply
                - mode (VectorStoreQueryMode): query mode (default or MMR)
            **kwargs: Additional keyword arguments passed to ChromaDB query method.
                For MMR mode, supports:
                - mmr_threshold (Optional[float]): MMR threshold between 0 and 1
                - mmr_prefetch_factor (Optional[float]): Factor to multiply similarity_top_k
                for prefetching candidates (default: 4.0)
                - mmr_prefetch_k (Optional[int]): Explicit number of candidates to prefetch
                (cannot be used with mmr_prefetch_factor)
                For ChromaDB-specific parameters:
                - where (dict): ChromaDB where clause (use query.filters instead for standard filtering)
                - include (List[str]): ChromaDB include parameter
                - where_document (dict): ChromaDB where_document parameter

        Returns:
            VectorStoreQueryResult: Query result containing matched nodes, similarities, and IDs.

        Raises:
            ValueError: If MMR parameters are invalid or if both query.filters and
                    where kwargs are specified.

        """
        if query.filters is not None:
            if "where" in kwargs:
                raise ValueError(
                    "Cannot specify metadata filters via both query and kwargs. "
                    "Use kwargs only for chroma specific items that are "
                    "not supported via the generic query interface."
                )
            where = _to_chroma_filter(query.filters)
        else:
            where = kwargs.pop("where", None)

        if not query.query_embedding:
            return self._get(limit=query.similarity_top_k, where=where, **kwargs)

        # Handle MMR mode
        if query.mode == VectorStoreQueryMode.MMR:
            return self._mmr_search(query, where, **kwargs)

        return self._query(
            query_embeddings=query.query_embedding,
            n_results=query.similarity_top_k,
            where=where,
            **kwargs,
        )

    def_query(
        self, query_embeddings: List["float"], n_results: int, where: dict, **kwargs
    ) -> VectorStoreQueryResult:
        if where:
            results = self._collection.query(
                query_embeddings=query_embeddings,
                n_results=n_results,
                where=where,
                **kwargs,
            )
        else:
            results = self._collection.query(
                query_embeddings=query_embeddings,
                n_results=n_results,
                **kwargs,
            )

        logger.debug(f"> Top {len(results['documents'][0])} nodes:")
        nodes = []
        similarities = []
        ids = []
        for node_id, text, metadata, distance in zip(
            results["ids"][0],
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            try:
                node = metadata_dict_to_node(metadata, text=text)
            except Exception:
                # NOTE: deprecated legacy logic for backward compatibility
                metadata, node_info, relationships = legacy_metadata_dict_to_node(
                    metadata
                )

                node = TextNode(
                    text=text or "",
                    id_=node_id,
                    metadata=metadata,
                    start_char_idx=node_info.get("start", None),
                    end_char_idx=node_info.get("end", None),
                    relationships=relationships,
                )

            nodes.append(node)

            similarity_score = math.exp(-distance)
            similarities.append(similarity_score)

            logger.debug(
                f"> [Node {node_id}] [Similarity score: {similarity_score}] "
                f"{truncate_text(str(text),100)}"
            )
            ids.append(node_id)

        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

    def_mmr_search(
        self, query: VectorStoreQuery, where: dict, **kwargs
    ) -> VectorStoreQueryResult:
"""
        Perform MMR search using ChromaDB.

        Args:
            query: VectorStoreQuery object containing the query parameters
            where: ChromaDB filter conditions
            **kwargs: Additional keyword arguments including mmr_threshold

        Returns:
            VectorStoreQueryResult: Query result with MMR-applied nodes

        """
        # Extract MMR parameters
        mmr_threshold = kwargs.get("mmr_threshold")

        # Validate MMR parameters
        if mmr_threshold is not None and (
            not isinstance(mmr_threshold, (int, float))
            or mmr_threshold  0
            or mmr_threshold  1
        ):
            raise ValueError("mmr_threshold must be a float between 0 and 1")

        # Validate prefetch parameters (check before popping)
        raw_prefetch_factor = kwargs.get("mmr_prefetch_factor")
        raw_prefetch_k = kwargs.get("mmr_prefetch_k")
        if raw_prefetch_factor is not None and raw_prefetch_k is not None:
            raise ValueError(
                "'mmr_prefetch_factor' and 'mmr_prefetch_k' "
                "cannot coexist in a call to query()"
            )

        # Strip MMR-only kwargs so they aren't forwarded to Chroma
        mmr_threshold = kwargs.pop("mmr_threshold", None)
        prefetch_k_override = kwargs.pop("mmr_prefetch_k", None)
        prefetch_factor = kwargs.pop("mmr_prefetch_factor", DEFAULT_MMR_PREFETCH_FACTOR)

        # Calculate prefetch size (get more candidates than needed for MMR)
        if prefetch_k_override is not None:
            prefetch_k = int(prefetch_k_override)
        else:
            prefetch_k = int(query.similarity_top_k * prefetch_factor)

        # Ensure prefetch_k is at least as large as similarity_top_k
        prefetch_k = max(prefetch_k, query.similarity_top_k)

        logger.debug(
            f"MMR search: prefetching {prefetch_k} candidates for {query.similarity_top_k} final results"
        )

        # Query ChromaDB for more candidates than needed (kwargs now safe)
        if where:
            prefetch_results = self._collection.query(
                query_embeddings=query.query_embedding,
                n_results=prefetch_k,
                where=where,
                include=["embeddings", "documents", "metadatas", "distances"],
                **kwargs,
            )
        else:
            prefetch_results = self._collection.query(
                query_embeddings=query.query_embedding,
                n_results=prefetch_k,
                include=["embeddings", "documents", "metadatas", "distances"],
                **kwargs,
            )

        # Extract embeddings and metadata for MMR processing
        prefetch_embeddings = []
        prefetch_ids = []
        prefetch_metadata = []
        prefetch_documents = []
        prefetch_distances = []

        # Process prefetch results
        for i in range(len(prefetch_results["ids"][0])):
            node_id = prefetch_results["ids"][0][i]
            text = prefetch_results["documents"][0][i]
            metadata = prefetch_results["metadatas"][0][i]
            distance = prefetch_results["distances"][0][i]

            # Get the actual embedding from ChromaDB results
            if "embeddings" in prefetch_results and prefetch_results["embeddings"]:
                embedding = prefetch_results["embeddings"][0][i]
            else:
                # Fallback: if embeddings not available, we'll use distance-based approach
                embedding = None

            # Store for MMR processing
            prefetch_embeddings.append(embedding)
            prefetch_ids.append(node_id)
            prefetch_metadata.append(metadata)
            prefetch_documents.append(text)
            prefetch_distances.append(distance)

        if not prefetch_embeddings:
            logger.warning("No results found during MMR prefetch")
            return VectorStoreQueryResult(nodes=[], similarities=[], ids=[])

        # Check if we have valid embeddings for MMR
        valid_embeddings = [emb for emb in prefetch_embeddings if emb is not None]

        if len(valid_embeddings)  query.similarity_top_k:
            logger.warning(
                f"Not enough valid embeddings for MMR: {len(valid_embeddings)}{query.similarity_top_k}"
            )
            # Fallback to regular similarity search
            return self._query(
                query_embeddings=query.query_embedding,
                n_results=query.similarity_top_k,
                where=where,
                **kwargs,
            )

        # Apply MMR algorithm using the core utility function
        mmr_similarities, mmr_indices = get_top_k_mmr_embeddings(
            query_embedding=query.query_embedding,
            embeddings=valid_embeddings,
            similarity_top_k=query.similarity_top_k,
            embedding_ids=list(range(len(valid_embeddings))),
            mmr_threshold=mmr_threshold,
        )

        # Build final results based on MMR selection
        final_nodes = []
        final_similarities = []
        final_ids = []

        # Create a mapping from valid embedding indices to original prefetch indices
        valid_indices = [
            i for i, emb in enumerate(prefetch_embeddings) if emb is not None
        ]

        for mmr_index in mmr_indices:
            if mmr_index  len(valid_indices):
                original_index = valid_indices[mmr_index]
                if original_index  len(prefetch_ids):
                    node_id = prefetch_ids[original_index]
                    text = prefetch_documents[original_index]
                    metadata = prefetch_metadata[original_index]
                    distance = prefetch_distances[original_index]

                    # Create node (reusing logic from _query method)
                    try:
                        node = metadata_dict_to_node(metadata, text=text)
                    except Exception:
                        # NOTE: deprecated legacy logic for backward compatibility
                        metadata, node_info, relationships = (
                            legacy_metadata_dict_to_node(metadata)
                        )

                        node = TextNode(
                            text=text or "",
                            id_=node_id,
                            metadata=metadata,
                            start_char_idx=node_info.get("start", None),
                            end_char_idx=node_info.get("end", None),
                            relationships=relationships,
                        )

                    final_nodes.append(node)
                    final_similarities.append(math.exp(-distance))
                    final_ids.append(node_id)

        logger.debug(
            f"MMR search completed: {len(final_nodes)} results selected from {len(prefetch_embeddings)} candidates"
        )

        return VectorStoreQueryResult(
            nodes=final_nodes, similarities=final_similarities, ids=final_ids
        )

    def_get(
        self, limit: Optional[int], where: dict, **kwargs
    ) -> VectorStoreQueryResult:
        if where:
            results = self._collection.get(
                limit=limit,
                where=where,
                **kwargs,
            )
        else:
            results = self._collection.get(
                limit=limit,
                **kwargs,
            )

        logger.debug(f"> Top {len(results['documents'])} nodes:")
        nodes = []
        ids = []

        if not results["ids"]:
            results["ids"] = [[]]

        for node_id, text, metadata in zip(
            results["ids"], results["documents"], results["metadatas"]
        ):
            try:
                node = metadata_dict_to_node(metadata, text=text)
            except Exception:
                # NOTE: deprecated legacy logic for backward compatibility
                metadata, node_info, relationships = legacy_metadata_dict_to_node(
                    metadata
                )

                node = TextNode(
                    text=text or "",
                    id_=node_id,
                    metadata=metadata,
                    start_char_idx=node_info.get("start", None),
                    end_char_idx=node_info.get("end", None),
                    relationships=relationships,
                )

            nodes.append(node)

            logger.debug(
                f"> [Node {node_id}] [Similarity score: N/A - using get()] "
                f"{truncate_text(str(text),100)}"
            )
            ids.append(node_id)

        return VectorStoreQueryResult(nodes=nodes, ids=ids)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/chroma/#llama_index.vector_stores.chroma.ChromaVectorStore.client "Permanent link")

```
client: 

```

Return client.
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/chroma/#llama_index.vector_stores.chroma.ChromaVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]],
    filters: Optional[[]] = None,
) -> []

```

Get nodes from index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `List[str]`  |  list of node ids  |  _required_  |  
|  `filters`  |  `List[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  list of metadata filters  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-chroma/llama_index/vector_stores/chroma/base.py`  
| 
```
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
```
 | 
```
defget_nodes(
    self,
    node_ids: Optional[List[str]],
    filters: Optional[List[MetadataFilters]] = None,
) -> List[BaseNode]:
"""
    Get nodes from index.

    Args:
        node_ids (List[str]): list of node ids
        filters (List[MetadataFilters]): list of metadata filters

    """
    if not self._collection:
        raise ValueError("Collection not initialized")

    node_ids = node_ids or None

    if filters:
        where = _to_chroma_filter(filters)
    else:
        where = None

    result = self._get(None, where=where, ids=node_ids)

    return result.nodes

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/chroma/#llama_index.vector_stores.chroma.ChromaVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-chroma/llama_index/vector_stores/chroma/base.py`  
| 
```
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
```
 | 
```
defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
    Add nodes to index.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings

    """
    if not self._collection:
        raise ValueError("Collection not initialized")

    max_chunk_size = MAX_CHUNK_SIZE
    node_chunks = chunk_list(nodes, max_chunk_size)

    all_ids = []
    for node_chunk in node_chunks:
        embeddings = []
        metadatas = []
        ids = []
        documents = []
        for node in node_chunk:
            embeddings.append(node.get_embedding())
            metadata_dict = node_to_metadata_dict(
                node, remove_text=True, flat_metadata=self.flat_metadata
            )
            for key in metadata_dict:
                if metadata_dict[key] is None:
                    metadata_dict[key] = ""
            metadatas.append(metadata_dict)
            ids.append(node.node_id)
            documents.append(node.get_content(metadata_mode=MetadataMode.NONE))

        self._collection.add(
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas,
            documents=documents,
        )
        all_ids.extend(ids)

    return all_ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/chroma/#llama_index.vector_stores.chroma.ChromaVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-chroma/llama_index/vector_stores/chroma/base.py`  
| 
```
326
327
328
329
330
331
332
333
334
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    self._collection.delete(where={"document_id": ref_doc_id})

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/chroma/#llama_index.vector_stores.chroma.ChromaVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[[]] = None,
) -> None

```

Delete nodes from index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `List[str]`  |  list of node ids  |  `None`  |  
|  `filters`  |  `List[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  list of metadata filters  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-chroma/llama_index/vector_stores/chroma/base.py`  
| 
```
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
```
 | 
```
defdelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[List[MetadataFilters]] = None,
) -> None:
"""
    Delete nodes from index.

    Args:
        node_ids (List[str]): list of node ids
        filters (List[MetadataFilters]): list of metadata filters

    """
    if not self._collection:
        raise ValueError("Collection not initialized")

    node_ids = node_ids or []

    if filters:
        where = _to_chroma_filter(filters)
        self._collection.delete(ids=node_ids, where=where)

    else:
        self._collection.delete(ids=node_ids)

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/chroma/#llama_index.vector_stores.chroma.ChromaVectorStore.clear "Permanent link")

```
clear() -> None

```

Clear the collection.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-chroma/llama_index/vector_stores/chroma/base.py`  
| 
```
361
362
363
364
```
 | 
```
defclear(self) -> None:
"""Clear the collection."""
    ids = self._collection.get()["ids"]
    self._collection.delete(ids=ids)

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/chroma/#llama_index.vector_stores.chroma.ChromaVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  Query object containing: - query_embedding (List[float]): query embedding - similarity_top_k (int): top k most similar nodes - filters (Optional[MetadataFilters]): metadata filters to apply - mode (VectorStoreQueryMode): query mode (default or MMR)  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments passed to ChromaDB query method. For MMR mode, supports: - mmr_threshold (Optional[float]): MMR threshold between 0 and 1 - mmr_prefetch_factor (Optional[float]): Factor to multiply similarity_top_k for prefetching candidates (default: 4.0) - mmr_prefetch_k (Optional[int]): Explicit number of candidates to prefetch (cannot be used with mmr_prefetch_factor) For ChromaDB-specific parameters: - where (dict): ChromaDB where clause (use query.filters instead for standard filtering) - include (List[str]): ChromaDB include parameter - where_document (dict): ChromaDB where_document parameter  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  Query result containing matched nodes, similarities, and IDs.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If MMR parameters are invalid or if both query.filters and where kwargs are specified.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-chroma/llama_index/vector_stores/chroma/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query (VectorStoreQuery): Query object containing:
            - query_embedding (List[float]): query embedding
            - similarity_top_k (int): top k most similar nodes
            - filters (Optional[MetadataFilters]): metadata filters to apply
            - mode (VectorStoreQueryMode): query mode (default or MMR)
        **kwargs: Additional keyword arguments passed to ChromaDB query method.
            For MMR mode, supports:
            - mmr_threshold (Optional[float]): MMR threshold between 0 and 1
            - mmr_prefetch_factor (Optional[float]): Factor to multiply similarity_top_k
            for prefetching candidates (default: 4.0)
            - mmr_prefetch_k (Optional[int]): Explicit number of candidates to prefetch
            (cannot be used with mmr_prefetch_factor)
            For ChromaDB-specific parameters:
            - where (dict): ChromaDB where clause (use query.filters instead for standard filtering)
            - include (List[str]): ChromaDB include parameter
            - where_document (dict): ChromaDB where_document parameter

    Returns:
        VectorStoreQueryResult: Query result containing matched nodes, similarities, and IDs.

    Raises:
        ValueError: If MMR parameters are invalid or if both query.filters and
                where kwargs are specified.

    """
    if query.filters is not None:
        if "where" in kwargs:
            raise ValueError(
                "Cannot specify metadata filters via both query and kwargs. "
                "Use kwargs only for chroma specific items that are "
                "not supported via the generic query interface."
            )
        where = _to_chroma_filter(query.filters)
    else:
        where = kwargs.pop("where", None)

    if not query.query_embedding:
        return self._get(limit=query.similarity_top_k, where=where, **kwargs)

    # Handle MMR mode
    if query.mode == VectorStoreQueryMode.MMR:
        return self._mmr_search(query, where, **kwargs)

    return self._query(
        query_embeddings=query.query_embedding,
        n_results=query.similarity_top_k,
        where=where,
        **kwargs,
    )

```
 |  
| --- | --- |  
options: members: - ChromaVectorStore
