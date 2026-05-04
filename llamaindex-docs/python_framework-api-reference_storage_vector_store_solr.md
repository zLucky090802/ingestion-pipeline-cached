# Solr
##  ApacheSolrVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.ApacheSolrVectorStore "Permanent link")
Bases: 
A LlamaIndex vector store implementation for Apache Solr.
This vector store provides integration with Apache Solr, supporting both dense vector similarity search (KNN) and sparse text search (BM25).
Key Features:
  * Dense vector embeddings with KNN similarity search
  * Sparse text search with BM25 scoring and field boosting
  * Metadata filtering with various operators
  * Async/sync operations
  * Automatic query escaping and field preprocessing


Field Mapping: the vector store maps LlamaIndex node attributes to Solr fields:
  * `nodeid_field`: Maps to `node.id_` (required)
  * `content_field`: Maps to `node.get_content()` (optional)
  * `embedding_field`: Maps to `node.get_embedding()` (optional)
  * `docid_field`: Maps to `node.ref_doc_id` (optional)
  * `metadata fields`: Mapped via `metadata_to_solr_field_mapping`


Query Modes:
  * `DEFAULT`: Dense vector KNN search using embeddings
  * `TEXT_SEARCH`: Sparse BM25 text search with field boosting

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/base.py`  
| 
```
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
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
```
 | 
```
classApacheSolrVectorStore(BasePydanticVectorStore):
"""
    A LlamaIndex vector store implementation for Apache Solr.

    This vector store provides integration with Apache Solr, supporting
    both dense vector similarity search (KNN) and sparse text search (BM25).

    Key Features:

    * Dense vector embeddings with KNN similarity search
    * Sparse text search with BM25 scoring and field boosting
    * Metadata filtering with various operators
    * Async/sync operations
    * Automatic query escaping and field preprocessing

    Field Mapping: the vector store maps LlamaIndex node attributes
    to Solr fields:

    * ``nodeid_field``: Maps to ``node.id_`` (required)
    * ``content_field``: Maps to ``node.get_content()`` (optional)
    * ``embedding_field``: Maps to ``node.get_embedding()`` (optional)
    * ``docid_field``: Maps to ``node.ref_doc_id`` (optional)
    * ``metadata fields``: Mapped via ``metadata_to_solr_field_mapping``

    Query Modes:

    * ``DEFAULT``: Dense vector KNN search using embeddings
    * ``TEXT_SEARCH``: Sparse BM25 text search with field boosting
    """

    # Core client properties
    sync_client: SkipValidation[Any] = Field(
        ...,
        exclude=True,
        description="Synchronous Solr client instance for blocking operations.",
    )
    async_client: SkipValidation[Any] = Field(
        ...,
        exclude=True,
        description="Asynchronous Solr client instance for non-blocking operations.",
    )

    # Essential field mappings
    nodeid_field: str = Field(
        ...,
        description=(
            "Solr field name that uniquely identifies a node (required). Must be unique across all documents and maps to the LlamaIndex `node.id_`."
        ),
    )
    docid_field: Optional[str] = Field(
        default=None,
        description=(
            "Solr field name for the document ID (optional). Maps to `node.ref_doc_id` and is required for document-level operations like deletion."
        ),
    )
    content_field: Optional[str] = Field(
        default=None,
        description=(
            "Solr field name for storing the node's text content (optional). Maps to `node.get_content()`; required for BM25 / text search."
        ),
    )
    embedding_field: Optional[str] = Field(
        default=None,
        description=(
            "Solr field name for storing embedding vectors (optional). Maps to `node.get_embedding()`; required for vector similarity (KNN) search."
        ),
    )
    metadata_to_solr_field_mapping: Optional[list[tuple[str, str]]] = Field(
        default=None,
        description=(
            "Mapping from node metadata keys to Solr field names (optional). Each tuple is (metadata_key, solr_field). Enables structured metadata filtering."
        ),
    )

    # Configuration options
    text_search_fields: Optional[Annotated[Sequence[BoostedTextField], MinLen(1)]] = (
        Field(
            default=None,
            description=(
                "Fields used for BM25 text search with optional boosting. Sequence of BoostedTextField; required for TEXT_SEARCH mode."
            ),
        )
    )
    output_fields: Annotated[Sequence[str], MinLen(1)] = Field(
        default=["*", "score"],
        description=(
            "Default fields to return in query results. Include 'score' automatically for relevance; use '*' for all stored fields or list specific ones."
        ),
    )

    # Serialization configuration
    model_config: ClassVar[ConfigDict] = ConfigDict(
        arbitrary_types_allowed=True, frozen=True
    )

    # Required for LlamaIndex API compatibility
    stores_text: bool = True
    stores_node: bool = True
    flat_metadata: bool = False

    @field_validator("output_fields")
    @classmethod
    def_validate_output_fields(cls, value: Sequence[str]) -> list[str]:
"""
        Ensure 'score' field is always included in output_fields during initialization.

        Args:
            value (Sequence[str]): The original output fields
        Returns:
            Modified output fields with 'score' always included

        """
        result = list(value)
        if "score" not in result:
            result.append("score")
        return result

    @field_validator("text_search_fields", mode="before")
    def_validate_text_search_fields(
        cls, v: Optional[list[Union[str, BoostedTextField]]]
    ) -> Optional[list[BoostedTextField]]:
"""Validate and convert text search fields to BoostedTextField instances."""
        if v is None:
            return None

        defto_boosted(item: Union[str, BoostedTextField]) -> BoostedTextField:
            if isinstance(item, str):
                return BoostedTextField(field=item)
            return item

        return [to_boosted(item) for item in v]

    @property
    defclient(self) -> Any:
"""Return synchronous Solr client."""
        return self.sync_client

    @property
    defaclient(self) -> Any:
"""Return asynchronous Solr client."""
        return self.async_client

    def_build_dense_query(
        self, query: VectorStoreQuery, solr_query: SolrQueryDict
    ) -> SolrQueryDict:
"""
        Build a dense vector KNN query for Solr.

        Args:
            query: The vector store query containing embedding and parameters
            solr_query: The base Solr query dictionary to build upon
        Returns:
            Updated Solr query dictionary with dense vector search parameters
        Raises:
            ValueError: If no embedding field is specified in either query or vector store

        """
        if query.embedding_field is not None:
            embedding_field = query.embedding_field
            logger.debug("Using embedding field from query: %s", embedding_field)

        elif self.embedding_field is not None:
            embedding_field = self.embedding_field
            logger.debug("Using embedding field from vector store: %s", embedding_field)

        else:
            raise ValueError(
                "No embedding field name specified in query or vector store. "
                "Either set 'embedding_field' on the VectorStoreQuery or configure "
                "'embedding_field' when initializing ApacheSolrVectorStore"
            )

        if query.query_embedding is None:
            logger.warning(
                "`query.query_embedding` is None, retrieval results will not be meaningful."
            )

        solr_query["q"] = (
            f"{{!knn f={embedding_field} topK={query.similarity_top_k}}}{query.query_embedding}"
        )
        rows_value = None or query.similarity_top_k
        solr_query["rows"] = str(rows_value)
        return solr_query

    def_build_bm25_query(
        self, query: VectorStoreQuery, solr_query: SolrQueryDict
    ) -> SolrQueryDict:
"""
        Build a BM25 text search query for Solr.

        Args:
            query: The vector store query containing the query string and parameters
            solr_query: The base Solr query dictionary to build upon
        Returns:
            Updated Solr query dictionary with BM25 search parameters
        Raises:
            ValueError: If no text search fields are available or query string is None

        """
        if query.query_str is None:
            raise ValueError("Query string cannot be None for BM25 search")

        # Use text_search_fields from the vector store
        if self.text_search_fields is None:
            raise ValueError(
                "text_search_fields must be specified in the vector store config for BM25 search"
            )

        user_query = escape_query_characters(
            query.query_str, translation_table=ESCAPE_RULES_NESTED_LUCENE_DISMAX
        )

        # Join the search fields with spaces for the Solr qf parameter
        search_fields_str = " ".join(
            [
                text_search_field.get_query_str()
                for text_search_field in self.text_search_fields
            ]
        )
        solr_query["q"] = (
            f"{{!dismax deftype=lucene, qf='{search_fields_str}' v='{user_query}'}}"
        )
        # Use rows from query if provided, otherwise fall back to similarity_top_k
        rows_value = None or query.sparse_top_k
        solr_query["rows"] = str(rows_value)
        return solr_query

    def_to_solr_query(self, query: VectorStoreQuery) -> SolrQueryDict:
"""Generate a KNN Solr query."""
        solr_query: SolrQueryDict = {"q": "*:*", "fq": []}

        if (
            query.mode == VectorStoreQueryMode.DEFAULT
            and query.query_embedding is not None
        ):
            solr_query = self._build_dense_query(query, solr_query)

        elif query.mode == VectorStoreQueryMode.TEXT_SEARCH:
            solr_query = self._build_bm25_query(query, solr_query)

        if query.doc_ids is not None:
            if self.docid_field is None:
                raise ValueError(
                    "`docid_field` must be passed during initialization to filter on docid"
                )
            solr_query["fq"].append(
                f"{self.docid_field}:({' OR '.join(query.doc_ids)})"
            )
        if query.node_ids is not None and len(query.node_ids)  0:
            solr_query["fq"].append(
                f"{self.nodeid_field}:({' OR '.join(query.node_ids)})"
            )
        if query.output_fields is not None:
            # Use output fields from query, ensuring score is always included
            output_fields = self._validate_output_fields(query.output_fields)
            solr_query["fl"] = ",".join(output_fields)
            logger.info("Using output fields from query: %s", output_fields)
        else:
            # Use default output fields from vector store, ensuring score is always included
            solr_query["fl"] = ",".join(self.output_fields)
            logger.info(
                "Using default output fields from vector store: %s", self.output_fields
            )

        if query.filters:
            filter_queries = recursively_unpack_filters(query.filters)
            solr_query["fq"].extend(filter_queries)

        logger.debug(
            "Converted input query into Solr query dictionary, input=%s, output=%s",
            query,
            solr_query,
        )
        return solr_query

    def_process_query_results(
        self, results: list[dict[str, Any]]
    ) -> VectorStoreQueryResult:
"""
        Convert Solr search results to LlamaIndex VectorStoreQueryResult format.
        This method transforms raw Solr documents into LlamaIndex TextNode objects
        and packages them with similarity scores and metadata into a structured
        query result. It handles field mapping, metadata extraction.

        Args:
            results: List of Solr document dictionaries from search response.
                Each dictionary contains field values as returned by Solr.

        Returns:
            A :py:class:`VectorStoreQueryResult` containing:
            * ``nodes``: List of :py:class:`TextNode` objects with content and metadata
            * ``ids``: List of node IDs corresponding to each node
            * ``similarities``: List of similarity scores (if available)

        Raises:
            ValueError: If the number of similarity scores doesn't match the
                number of nodes (partial scoring is not supported).

        Note:
            * Metadata fields are automatically identified by excluding known
              system fields (``nodeid_field``, ``content_field``, etc.)
            * The 'score' field from Solr is extracted as similarity scores
            * Missing optional fields (``content``, ``embedding``) are handled gracefully

        """
        ids, nodes, similarities = [], [], []
        for result in results:
            metadata_fields = result.keys() - {
                self.nodeid_field,
                self.content_field,
                self.embedding_field,
                self.docid_field,
                "score",
            }

            ids.append(result[self.nodeid_field])

            node = TextNode(
                id_=result[self.nodeid_field],
                # input must be a string, if missing use empty string
                text=result[self.content_field] if self.content_field else "",
                embedding=(
                    result[self.embedding_field] if self.embedding_field else None
                ),
                metadata={f: result[f] for f in metadata_fields},
            )
            nodes.append(node)
            if "score" in result:
                similarities.append(result["score"])

        if len(similarities) == 0:
            return VectorStoreQueryResult(nodes=nodes, ids=ids)
        elif 0  len(similarities)  len(nodes):
            raise ValueError(
                "The number of similarities (scores) does not match the number of nodes"
            )
        else:
            return VectorStoreQueryResult(
                nodes=nodes, ids=ids, similarities=similarities
            )

    def_validate_query_mode(self, query: VectorStoreQuery) -> None:
"""
        Validate that the query mode is supported by this vector store.

        This method ensures that the requested query mode is compatible with
        the current Solr vector store implementation.

        Supported Modes:
        * ``DEFAULT``: Dense vector similarity search using KNN with embeddings
        * ``TEXT_SEARCH``: Sparse text search using BM25 with field boosting

        Args:
            query:
                The vector store query containing the mode to validate. The mode is
                checked against supported :py:class:`VectorStoreQueryMode` values.

        Raises:
            ValueError: If the query mode is not supported. Unsupported modes
                include any future modes not yet implemented in the Solr backend.

        Note:
            This validation occurs before query execution to provide clear
            error messages for unsupported operations. Future versions may
            support additional query modes like hybrid search.

        """
        if (
            query.mode == VectorStoreQueryMode.DEFAULT
            or query.mode == VectorStoreQueryMode.TEXT_SEARCH
        ):
            return
        else:
            raise ValueError(
                f"ApacheSolrVectorStore does not support {query.mode} yet."
            )

    defquery(
        self, query: VectorStoreQuery, **search_kwargs: Any
    ) -> VectorStoreQueryResult:
"""
        Execute a synchronous search query against the Solr vector store.

        This method supports both dense vector similarity search (KNN) and sparse
        text search (BM25) depending on the query mode and parameters. It handles
        query validation, Solr query construction, execution, and result processing.

        Query Types:

        * Dense Vector Search: Uses ``query_embedding`` for KNN similarity search
        * Text Search: Uses ``query_str`` for BM25 text search with field boosting
        * Filtered Search: Combines vector/text search with metadata filters

        Supported Filter Operations:

        * ``EQ``, ``NE``: Equality and inequality comparisons
        * ``GT``, ``GTE``, ``LT``, ``LTE``: Numeric range comparisons
        * ``IN``, ``NIN``: List membership tests
        * ``TEXT_MATCH``, ``TEXT_MATCH_INSENSITIVE``: Exact text matching

        Unsupported Filter Operations:

        * ``ANY``, ``ALL``: Complex logical operations
        * ``CONTAINS``: Substring matching

        Args:
            query:
                The vector store query containing search parameters:

                * ``query_embedding``: Dense vector for similarity search (DEFAULT mode)
                * ``query_str``: Text string for BM25 search (TEXT_SEARCH mode)
                * ``mode``: ``VectorStoreQueryMode`` (DEFAULT or TEXT_SEARCH)
                * ``similarity_top_k``: Number of results for vector search
                * ``sparse_top_k``: Number of results for text search
                * ``filters``: Optional metadata filters for constraining results
                * ``doc_ids``: Optional list of document IDs to filter by
                * ``node_ids``: Optional list of node IDs to filter by
                * ``output_fields``: Optional list of fields to return
            **search_kwargs: Extra keyword arguments (ignored for compatibility)

        Returns:
            VectorStoreQueryResult containing:

            * nodes: List of TextNode objects with content and metadata
            * ids: List of corresponding node IDs
            * similarities: List of similarity scores (when available)

        Raises:
            ValueError: If the query mode is unsupported, or if required fields
                are missing (e.g., ``embedding_field`` for vector search, ``docid_field``
                for document filtering)

        Note:
            This method performs synchronous I/O operations. For better performance
            in async contexts, use the :py:meth:`aquery` method instead.

        """
        del search_kwargs  # unused

        self._validate_query_mode(query)
        solr_query = self._to_solr_query(query)
        results = self.sync_client.search(solr_query)
        return self._process_query_results(results.response.docs)

    async defaquery(
        self, query: VectorStoreQuery, **search_kwargs: Any
    ) -> VectorStoreQueryResult:
"""
        Execute an asynchronous search query against the Solr vector store.

        This method supports both dense vector similarity search (KNN) and sparse
        text search (BM25) depending on the query mode and parameters. It handles
        query validation, Solr query construction, execution, and result processing.

        Query Types:

        * Dense Vector Search: Uses ``query_embedding`` for KNN similarity search
        * Text Search: Uses ``query_str`` for BM25 text search with field boosting
        * Filtered Search: Combines vector/text search with metadata filters

        Supported Filter Operations:

        * ``EQ``, ``NE``: Equality and inequality comparisons
        * ``GT``, ``GTE``, ``LT``, ``LTE``: Numeric range comparisons
        * ``IN``, ``NIN``: List membership tests
        * ``TEXT_MATCH``, ``TEXT_MATCH_INSENSITIVE``: Exact text matching

        Unsupported Filter Operations:

        * ``ANY``, ``ALL``: Complex logical operations
        * ``CONTAINS``: Substring matching

        Args:
            query:
                The vector store query containing search parameters:

                * ``query_embedding``: Dense vector for similarity search (DEFAULT mode)
                * ``query_str``: Text string for BM25 search (TEXT_SEARCH mode)
                * ``mode``: ``VectorStoreQueryMode`` (DEFAULT or TEXT_SEARCH)
                * ``similarity_top_k``: Number of results for vector search
                * ``sparse_top_k``: Number of results for text search
                * ``filters``: Optional metadata filters for constraining results
                * ``doc_ids``: Optional list of document IDs to filter by
                * ``node_ids``: Optional list of node IDs to filter by
                * ``output_fields``: Optional list of fields to return
            **search_kwargs: Extra keyword arguments (ignored for compatibility)

        Returns:
            VectorStoreQueryResult containing:

            * nodes: List of TextNode objects with content and metadata
            * ids: List of corresponding node IDs
            * similarities: List of similarity scores (when available)

        Raises:
            ValueError: If the query mode is unsupported, or if required fields
                are missing (e.g., ``embedding_field`` for vector search, ``docid_field``
                for document filtering)

        """
        del search_kwargs  # unused

        self._validate_query_mode(query)
        solr_query = self._to_solr_query(query)
        results = await self.async_client.search(solr_query)
        return self._process_query_results(results.response.docs)

    def_get_data_from_node(self, node: BaseNode) -> dict[str, Any]:
"""
        Transform a LlamaIndex node into a Solr document dictionary.
        This method maps LlamaIndex node attributes to Solr fields based on the
        vector store configuration. It handles content extraction, embedding
        mapping, metadata processing.

        Args:
            node: LlamaIndex BaseNode containing content, metadata,
                to be stored in Solr.

        Returns:
            Dictionary representing a Solr document with mapped fields:
                - id: Always maps to node.node_id (required)
                - content_field: Maps to node.get_content() (if configured)
                - embedding_field: Maps to node.get_embedding() (if configured)
                - docid_field: Maps to node.ref_doc_id (if configured)
                - metadata fields: Mapped via metadata_to_solr_field_mapping

        Field Mapping Process:
            1. Always includes node ID as 'id' field
            2. Extracts content if content_field is configured
            3. Extracts embedding if embedding_field is configured
            4. Includes document ID if docid_field is configured
            5. Maps metadata using configured field mappings with preprocessing

        Note:
            This is an internal method used by add() and async_add() operations.
            The returned dictionary must be compatible with the Solr schema.

        """
        data: dict[str, Any] = {self.nodeid_field: node.node_id}
        if self.content_field is not None:
            data[self.content_field] = node.get_content()
        if self.embedding_field is not None:
            data[self.embedding_field] = node.get_embedding()
        if self.docid_field is not None:
            data[self.docid_field] = node.ref_doc_id
        if self.metadata_to_solr_field_mapping is not None:
            for metadata_key, solr_key in self.metadata_to_solr_field_mapping:
                if metadata_key in node.metadata:
                    data[solr_key] = node.metadata[metadata_key]
        return data

    def_get_data_from_nodes(
        self, nodes: Sequence[BaseNode]
    ) -> tuple[list[str], list[dict[str, Any]]]:
        # helper to avoid double iteration, it gets expensive at large batch sizes
        logger.debug("Extracting data from %d nodes", len(nodes))
        data: list[dict[str, Any]] = []
        node_ids: list[str] = []
        for node in nodes:
            node_ids.append(node.id_)
            data.append(self._get_data_from_node(node))
        return node_ids, data

    defadd(self, nodes: Sequence[BaseNode], **add_kwargs: Any) -> list[str]:
"""
        Synchronously add nodes (documents) to a Solr collection.

        Mapping from Solr fields to :py:class:`llama_index.core.schema.BaseNode` attributes
        should be as follows:

        * ``nodeid_field`` -> ``node_id``
        * ``content_field`` -> ``content``
        * ``embedding_field`` -> ``embedding``
        * ``docid_field`` -> ``ref_doc_id``

        All other fields corresponding to the Solr collection should be packed as a single
        ``dict`` in the ``metadata`` field.

        Args:
            nodes: The nodes (documents) to be added to the Solr collection.
            **add_kwargs:
                Extra keyword arguments.

        Returns:
            A list of node IDs for each node added to the store.

        """
        del add_kwargs  # unused

        if not nodes:
            raise ValueError("Call to 'add' with no contents")

        start = time.perf_counter()
        node_ids, data = self._get_data_from_nodes(nodes)
        self.sync_client.add(data)
        logger.info(
            "Added %d documents to Solr in %0.2f seconds",
            len(data),
            time.perf_counter() - start,
        )
        return node_ids

    async defasync_add(
        self,
        nodes: Sequence[BaseNode],
        **add_kwargs: Any,
    ) -> list[str]:
"""
        Asynchronously add nodes (documents) to a Solr collection.

        Mapping from Solr fields to :py:class:`llama_index.core.schema.BaseNode` attributes
        should be as follows:

        * ``nodeid_field`` -> ``node_id``
        * ``content_field`` -> ``content``
        * ``embedding_field`` -> ``embedding``
        * ``docid_field`` -> ``ref_doc_id``

        All other fields corresponding to the Solr collection should be packed as a single
        ``dict`` in the ``metadata`` field.

        Args:
            nodes: The nodes (documents) to be added to the Solr collection.
            **add_kwargs:
                Extra keyword arguments.

        Returns:
            A list of node IDs for each node added to the store.

        Raises:
            ValueError: If called with an empty list of nodes.

        """
        del add_kwargs  # unused

        if not nodes:
            raise ValueError("Call to 'async_add' with no contents")

        start = time.perf_counter()
        node_ids, data = self._get_data_from_nodes(nodes)
        await self.async_client.add(data)
        logger.info(
            "Added %d documents to Solr in %0.2f seconds",
            len(data),
            time.perf_counter() - start,
        )
        return node_ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Synchronously delete a node from the collection using its reference document ID.

        Args:
            ref_doc_id: The reference document ID of the node to be deleted.
            **delete_kwargs:
                Extra keyword arguments, ignored by this implementation. These are added
                solely for interface compatibility.

        Raises:
            ValueError:
                If a ``docid_field`` was not passed to this vector store at
                initialization.

        """
        del delete_kwargs  # unused

        logger.debug("Deleting documents from Solr using query: %s", ref_doc_id)
        self.sync_client.delete_by_id([ref_doc_id])

    async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Asynchronously delete a node from the collection using its reference document ID.

        Args:
            ref_doc_id: The reference document ID of the node to be deleted.
            **delete_kwargs:
                Extra keyword arguments, ignored by this implementation. These are added
                solely for interface compatibility.

        Raises:
            ValueError:
                If a ``docid_field`` was not passed to this vector store at
                initialization.

        """
        del delete_kwargs  # unused

        logger.debug("Deleting documents from Solr using query: %s", ref_doc_id)
        await self.async_client.delete_by_id([ref_doc_id])

    def_build_delete_nodes_query(
        self,
        node_ids: Optional[list[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> str:
        if not node_ids and not filters:
            raise ValueError(
                "At least one of `node_ids` or `filters` must be passed to `delete_nodes`"
            )

        queries: list[str] = []
        if node_ids:
            queries.append(f"{self.nodeid_field}:({' OR '.join(node_ids)})")
        if filters is not None:
            queries.extend(recursively_unpack_filters(filters))

        if not queries:
            raise ValueError(
                "Neither `node_ids` nor non-empty `filters` were passed to `delete_nodes`"
            )
        elif len(queries) == 1:
            return queries[0]
        return f"({' AND '.join(qforqinqueriesifq)})"

    defdelete_nodes(
        self,
        node_ids: Optional[list[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Synchronously delete nodes from vector store based on node ids.

        Args:
            node_ids: The node IDs to delete.
            filters: The filters to be applied to the node when deleting.
            **delete_kwargs:
                Extra keyword arguments, ignored by this implementation. These are added
                solely for interface compatibility.

        """
        del delete_kwargs  # unused

        has_filters = filters is not None and len(filters.filters)  0
        # we can efficiently delete by ID if no filters are specified

        if node_ids and not has_filters:
            logger.debug("Deleting %d nodes from Solr by ID", len(node_ids))
            self.sync_client.delete_by_id(node_ids)

        # otherwise, build a query to delete by IDs+filters
        else:
            query_string = self._build_delete_nodes_query(node_ids, filters)
            logger.debug(
                "Deleting nodes from Solr using query: %s", query_string
            )  # pragma: no cover
            self.sync_client.delete_by_query(query_string)

    async defadelete_nodes(
        self,
        node_ids: Optional[list[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Asynchronously delete nodes from vector store based on node ids.

        Args:
            node_ids: The node IDs to delete.
            filters: The filters to be applied to the node when deleting.
            **delete_kwargs:
                Extra keyword arguments, ignored by this implementation. These are added
                solely for interface compatibility.

        """
        del delete_kwargs  # unused

        has_filters = filters is not None and len(filters.filters)  0
        # we can efficiently delete by ID if no filters are specified
        if node_ids and not has_filters:
            logger.debug("Deleting %d nodes from Solr by ID", len(node_ids))
            await self.async_client.delete_by_id(node_ids)

        # otherwise, build a query to delete by IDs+filters
        else:
            query_string = self._build_delete_nodes_query(node_ids, filters)
            logger.debug("Deleting nodes from Solr using query: %s", query_string)
            await self.async_client.delete_by_query(query_string)

    defclear(self) -> None:
"""
        Delete all documents from the Solr collection synchronously.
        This action is not reversible!
        """
        self.sync_client.clear_collection()

    async defaclear(self) -> None:
"""
        Delete all documents from the Solr collection asynchronously.
        This action is not reversible!
        """
        await self.async_client.clear_collection()

    defclose(self) -> None:
"""Close the Solr client synchronously."""
        self.sync_client.close()
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No running loop: create a temporary loop and close cleanly
            asyncio.run(self.async_client.close())
        else:
            # Running loop: schedule async close (not awaited)
            loop.create_task(self.async_client.close())  # noqa: RUF006

    async defaclose(self) -> None:
"""Explicit aclose for callers running inside an event loop."""
        self.sync_client.close()
        await self.async_client.close()

    def__del__(self) -> None:
"""
        Clean up the client for shutdown.
        This action is not reversible, and should only be called one time.
        """
        try:
            self.close()
        except RuntimeError as exc:
            logger.debug(
                "No running event loop, nothing to close, type=%s err='%s'",
                type(exc),
                exc,
            )
        except Exception as exc:
            logger.warning(
                "Failed to close the async Solr client, type=%s err='%s'",
                type(exc),
                exc,
            )

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.ApacheSolrVectorStore.client "Permanent link")

```
client: 

```

Return synchronous Solr client.
###  aclient `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.ApacheSolrVectorStore.aclient "Permanent link")

```
aclient: 

```

Return asynchronous Solr client.
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.ApacheSolrVectorStore.query "Permanent link")

```
query(
    query: , **search_kwargs: 
) -> 

```

Execute a synchronous search query against the Solr vector store.
This method supports both dense vector similarity search (KNN) and sparse text search (BM25) depending on the query mode and parameters. It handles query validation, Solr query construction, execution, and result processing.
Query Types:
  * Dense Vector Search: Uses `query_embedding` for KNN similarity search
  * Text Search: Uses `query_str` for BM25 text search with field boosting
  * Filtered Search: Combines vector/text search with metadata filters


Supported Filter Operations:
  * `EQ`, `NE`: Equality and inequality comparisons
  * `GT`, `GTE`, `LT`, `LTE`: Numeric range comparisons
  * `IN`, `NIN`: List membership tests
  * `TEXT_MATCH`, `TEXT_MATCH_INSENSITIVE`: Exact text matching


Unsupported Filter Operations:
  * `ANY`, `ALL`: Complex logical operations
  * `CONTAINS`: Substring matching


Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  The vector store query containing search parameters:
  * `query_embedding`: Dense vector for similarity search (DEFAULT mode)
  * `query_str`: Text string for BM25 search (TEXT_SEARCH mode)
  * `mode`: `VectorStoreQueryMode` (DEFAULT or TEXT_SEARCH)
  * `similarity_top_k`: Number of results for vector search
  * `sparse_top_k`: Number of results for text search
  * `filters`: Optional metadata filters for constraining results
  * `doc_ids`: Optional list of document IDs to filter by
  * `node_ids`: Optional list of node IDs to filter by
  * `output_fields`: Optional list of fields to return

 |  _required_  |  
|  `**search_kwargs`  |  Extra keyword arguments (ignored for compatibility)  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  VectorStoreQueryResult containing:  |  
|   | 
  * nodes: List of TextNode objects with content and metadata

 |  
|   | 
  * ids: List of corresponding node IDs

 |  
|   | 
  * similarities: List of similarity scores (when available)

 |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If the query mode is unsupported, or if required fields are missing (e.g., `embedding_field` for vector search, `docid_field` for document filtering)  |  
Note
This method performs synchronous I/O operations. For better performance in async contexts, use the :py:meth:`aquery` method instead.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/base.py`  
| 
```
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
```
 | 
```
defquery(
    self, query: VectorStoreQuery, **search_kwargs: Any
) -> VectorStoreQueryResult:
"""
    Execute a synchronous search query against the Solr vector store.

    This method supports both dense vector similarity search (KNN) and sparse
    text search (BM25) depending on the query mode and parameters. It handles
    query validation, Solr query construction, execution, and result processing.

    Query Types:

    * Dense Vector Search: Uses ``query_embedding`` for KNN similarity search
    * Text Search: Uses ``query_str`` for BM25 text search with field boosting
    * Filtered Search: Combines vector/text search with metadata filters

    Supported Filter Operations:

    * ``EQ``, ``NE``: Equality and inequality comparisons
    * ``GT``, ``GTE``, ``LT``, ``LTE``: Numeric range comparisons
    * ``IN``, ``NIN``: List membership tests
    * ``TEXT_MATCH``, ``TEXT_MATCH_INSENSITIVE``: Exact text matching

    Unsupported Filter Operations:

    * ``ANY``, ``ALL``: Complex logical operations
    * ``CONTAINS``: Substring matching

    Args:
        query:
            The vector store query containing search parameters:

            * ``query_embedding``: Dense vector for similarity search (DEFAULT mode)
            * ``query_str``: Text string for BM25 search (TEXT_SEARCH mode)
            * ``mode``: ``VectorStoreQueryMode`` (DEFAULT or TEXT_SEARCH)
            * ``similarity_top_k``: Number of results for vector search
            * ``sparse_top_k``: Number of results for text search
            * ``filters``: Optional metadata filters for constraining results
            * ``doc_ids``: Optional list of document IDs to filter by
            * ``node_ids``: Optional list of node IDs to filter by
            * ``output_fields``: Optional list of fields to return
        **search_kwargs: Extra keyword arguments (ignored for compatibility)

    Returns:
        VectorStoreQueryResult containing:

        * nodes: List of TextNode objects with content and metadata
        * ids: List of corresponding node IDs
        * similarities: List of similarity scores (when available)

    Raises:
        ValueError: If the query mode is unsupported, or if required fields
            are missing (e.g., ``embedding_field`` for vector search, ``docid_field``
            for document filtering)

    Note:
        This method performs synchronous I/O operations. For better performance
        in async contexts, use the :py:meth:`aquery` method instead.

    """
    del search_kwargs  # unused

    self._validate_query_mode(query)
    solr_query = self._to_solr_query(query)
    results = self.sync_client.search(solr_query)
    return self._process_query_results(results.response.docs)

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.ApacheSolrVectorStore.aquery "Permanent link")

```
aquery(
    query: , **search_kwargs: 
) -> 

```

Execute an asynchronous search query against the Solr vector store.
This method supports both dense vector similarity search (KNN) and sparse text search (BM25) depending on the query mode and parameters. It handles query validation, Solr query construction, execution, and result processing.
Query Types:
  * Dense Vector Search: Uses `query_embedding` for KNN similarity search
  * Text Search: Uses `query_str` for BM25 text search with field boosting
  * Filtered Search: Combines vector/text search with metadata filters


Supported Filter Operations:
  * `EQ`, `NE`: Equality and inequality comparisons
  * `GT`, `GTE`, `LT`, `LTE`: Numeric range comparisons
  * `IN`, `NIN`: List membership tests
  * `TEXT_MATCH`, `TEXT_MATCH_INSENSITIVE`: Exact text matching


Unsupported Filter Operations:
  * `ANY`, `ALL`: Complex logical operations
  * `CONTAINS`: Substring matching


Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  The vector store query containing search parameters:
  * `query_embedding`: Dense vector for similarity search (DEFAULT mode)
  * `query_str`: Text string for BM25 search (TEXT_SEARCH mode)
  * `mode`: `VectorStoreQueryMode` (DEFAULT or TEXT_SEARCH)
  * `similarity_top_k`: Number of results for vector search
  * `sparse_top_k`: Number of results for text search
  * `filters`: Optional metadata filters for constraining results
  * `doc_ids`: Optional list of document IDs to filter by
  * `node_ids`: Optional list of node IDs to filter by
  * `output_fields`: Optional list of fields to return

 |  _required_  |  
|  `**search_kwargs`  |  Extra keyword arguments (ignored for compatibility)  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  VectorStoreQueryResult containing:  |  
|   | 
  * nodes: List of TextNode objects with content and metadata

 |  
|   | 
  * ids: List of corresponding node IDs

 |  
|   | 
  * similarities: List of similarity scores (when available)

 |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If the query mode is unsupported, or if required fields are missing (e.g., `embedding_field` for vector search, `docid_field` for document filtering)  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/base.py`  
| 
```
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
```
 | 
```
async defaquery(
    self, query: VectorStoreQuery, **search_kwargs: Any
) -> VectorStoreQueryResult:
"""
    Execute an asynchronous search query against the Solr vector store.

    This method supports both dense vector similarity search (KNN) and sparse
    text search (BM25) depending on the query mode and parameters. It handles
    query validation, Solr query construction, execution, and result processing.

    Query Types:

    * Dense Vector Search: Uses ``query_embedding`` for KNN similarity search
    * Text Search: Uses ``query_str`` for BM25 text search with field boosting
    * Filtered Search: Combines vector/text search with metadata filters

    Supported Filter Operations:

    * ``EQ``, ``NE``: Equality and inequality comparisons
    * ``GT``, ``GTE``, ``LT``, ``LTE``: Numeric range comparisons
    * ``IN``, ``NIN``: List membership tests
    * ``TEXT_MATCH``, ``TEXT_MATCH_INSENSITIVE``: Exact text matching

    Unsupported Filter Operations:

    * ``ANY``, ``ALL``: Complex logical operations
    * ``CONTAINS``: Substring matching

    Args:
        query:
            The vector store query containing search parameters:

            * ``query_embedding``: Dense vector for similarity search (DEFAULT mode)
            * ``query_str``: Text string for BM25 search (TEXT_SEARCH mode)
            * ``mode``: ``VectorStoreQueryMode`` (DEFAULT or TEXT_SEARCH)
            * ``similarity_top_k``: Number of results for vector search
            * ``sparse_top_k``: Number of results for text search
            * ``filters``: Optional metadata filters for constraining results
            * ``doc_ids``: Optional list of document IDs to filter by
            * ``node_ids``: Optional list of node IDs to filter by
            * ``output_fields``: Optional list of fields to return
        **search_kwargs: Extra keyword arguments (ignored for compatibility)

    Returns:
        VectorStoreQueryResult containing:

        * nodes: List of TextNode objects with content and metadata
        * ids: List of corresponding node IDs
        * similarities: List of similarity scores (when available)

    Raises:
        ValueError: If the query mode is unsupported, or if required fields
            are missing (e.g., ``embedding_field`` for vector search, ``docid_field``
            for document filtering)

    """
    del search_kwargs  # unused

    self._validate_query_mode(query)
    solr_query = self._to_solr_query(query)
    results = await self.async_client.search(solr_query)
    return self._process_query_results(results.response.docs)

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.ApacheSolrVectorStore.add "Permanent link")

```
add(
    nodes: Sequence[], **add_kwargs: 
) -> []

```

Synchronously add nodes (documents) to a Solr collection.
Mapping from Solr fields to :py:class:`llama_index.core.schema.BaseNode` attributes should be as follows:
  * `nodeid_field` -> `node_id`
  * `content_field` -> `content`
  * `embedding_field` -> `embedding`
  * `docid_field` -> `ref_doc_id`


All other fields corresponding to the Solr collection should be packed as a single `dict` in the `metadata` field.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `Sequence[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "BaseNode \(llama_index.core.schema.BaseNode\)")]`  |  The nodes (documents) to be added to the Solr collection.  |  _required_  |  
|  `**add_kwargs`  |  Extra keyword arguments.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `list[str]`  |  A list of node IDs for each node added to the store.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/base.py`  
| 
```
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
```
 | 
```
defadd(self, nodes: Sequence[BaseNode], **add_kwargs: Any) -> list[str]:
"""
    Synchronously add nodes (documents) to a Solr collection.

    Mapping from Solr fields to :py:class:`llama_index.core.schema.BaseNode` attributes
    should be as follows:

    * ``nodeid_field`` -> ``node_id``
    * ``content_field`` -> ``content``
    * ``embedding_field`` -> ``embedding``
    * ``docid_field`` -> ``ref_doc_id``

    All other fields corresponding to the Solr collection should be packed as a single
    ``dict`` in the ``metadata`` field.

    Args:
        nodes: The nodes (documents) to be added to the Solr collection.
        **add_kwargs:
            Extra keyword arguments.

    Returns:
        A list of node IDs for each node added to the store.

    """
    del add_kwargs  # unused

    if not nodes:
        raise ValueError("Call to 'add' with no contents")

    start = time.perf_counter()
    node_ids, data = self._get_data_from_nodes(nodes)
    self.sync_client.add(data)
    logger.info(
        "Added %d documents to Solr in %0.2f seconds",
        len(data),
        time.perf_counter() - start,
    )
    return node_ids

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.ApacheSolrVectorStore.async_add "Permanent link")

```
async_add(
    nodes: Sequence[], **add_kwargs: 
) -> []

```

Asynchronously add nodes (documents) to a Solr collection.
Mapping from Solr fields to :py:class:`llama_index.core.schema.BaseNode` attributes should be as follows:
  * `nodeid_field` -> `node_id`
  * `content_field` -> `content`
  * `embedding_field` -> `embedding`
  * `docid_field` -> `ref_doc_id`


All other fields corresponding to the Solr collection should be packed as a single `dict` in the `metadata` field.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `Sequence[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "BaseNode \(llama_index.core.schema.BaseNode\)")]`  |  The nodes (documents) to be added to the Solr collection.  |  _required_  |  
|  `**add_kwargs`  |  Extra keyword arguments.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `list[str]`  |  A list of node IDs for each node added to the store.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If called with an empty list of nodes.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/base.py`  
| 
```
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
async defasync_add(
    self,
    nodes: Sequence[BaseNode],
    **add_kwargs: Any,
) -> list[str]:
"""
    Asynchronously add nodes (documents) to a Solr collection.

    Mapping from Solr fields to :py:class:`llama_index.core.schema.BaseNode` attributes
    should be as follows:

    * ``nodeid_field`` -> ``node_id``
    * ``content_field`` -> ``content``
    * ``embedding_field`` -> ``embedding``
    * ``docid_field`` -> ``ref_doc_id``

    All other fields corresponding to the Solr collection should be packed as a single
    ``dict`` in the ``metadata`` field.

    Args:
        nodes: The nodes (documents) to be added to the Solr collection.
        **add_kwargs:
            Extra keyword arguments.

    Returns:
        A list of node IDs for each node added to the store.

    Raises:
        ValueError: If called with an empty list of nodes.

    """
    del add_kwargs  # unused

    if not nodes:
        raise ValueError("Call to 'async_add' with no contents")

    start = time.perf_counter()
    node_ids, data = self._get_data_from_nodes(nodes)
    await self.async_client.add(data)
    logger.info(
        "Added %d documents to Solr in %0.2f seconds",
        len(data),
        time.perf_counter() - start,
    )
    return node_ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.ApacheSolrVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Synchronously delete a node from the collection using its reference document ID.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The reference document ID of the node to be deleted.  |  _required_  |  
|  `**delete_kwargs`  |  Extra keyword arguments, ignored by this implementation. These are added solely for interface compatibility.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If a `docid_field` was not passed to this vector store at initialization.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Synchronously delete a node from the collection using its reference document ID.

    Args:
        ref_doc_id: The reference document ID of the node to be deleted.
        **delete_kwargs:
            Extra keyword arguments, ignored by this implementation. These are added
            solely for interface compatibility.

    Raises:
        ValueError:
            If a ``docid_field`` was not passed to this vector store at
            initialization.

    """
    del delete_kwargs  # unused

    logger.debug("Deleting documents from Solr using query: %s", ref_doc_id)
    self.sync_client.delete_by_id([ref_doc_id])

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.ApacheSolrVectorStore.adelete "Permanent link")

```
adelete(ref_doc_id: , **delete_kwargs: ) -> None

```

Asynchronously delete a node from the collection using its reference document ID.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The reference document ID of the node to be deleted.  |  _required_  |  
|  `**delete_kwargs`  |  Extra keyword arguments, ignored by this implementation. These are added solely for interface compatibility.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If a `docid_field` was not passed to this vector store at initialization.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/base.py`  
| 
```
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
```
 | 
```
async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Asynchronously delete a node from the collection using its reference document ID.

    Args:
        ref_doc_id: The reference document ID of the node to be deleted.
        **delete_kwargs:
            Extra keyword arguments, ignored by this implementation. These are added
            solely for interface compatibility.

    Raises:
        ValueError:
            If a ``docid_field`` was not passed to this vector store at
            initialization.

    """
    del delete_kwargs  # unused

    logger.debug("Deleting documents from Solr using query: %s", ref_doc_id)
    await self.async_client.delete_by_id([ref_doc_id])

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.ApacheSolrVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Synchronously delete nodes from vector store based on node ids.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[list[str]]`  |  The node IDs to delete.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  The filters to be applied to the node when deleting.  |  `None`  |  
|  `**delete_kwargs`  |  Extra keyword arguments, ignored by this implementation. These are added solely for interface compatibility.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/base.py`  
| 
```
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
```
 | 
```
defdelete_nodes(
    self,
    node_ids: Optional[list[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Synchronously delete nodes from vector store based on node ids.

    Args:
        node_ids: The node IDs to delete.
        filters: The filters to be applied to the node when deleting.
        **delete_kwargs:
            Extra keyword arguments, ignored by this implementation. These are added
            solely for interface compatibility.

    """
    del delete_kwargs  # unused

    has_filters = filters is not None and len(filters.filters)  0
    # we can efficiently delete by ID if no filters are specified

    if node_ids and not has_filters:
        logger.debug("Deleting %d nodes from Solr by ID", len(node_ids))
        self.sync_client.delete_by_id(node_ids)

    # otherwise, build a query to delete by IDs+filters
    else:
        query_string = self._build_delete_nodes_query(node_ids, filters)
        logger.debug(
            "Deleting nodes from Solr using query: %s", query_string
        )  # pragma: no cover
        self.sync_client.delete_by_query(query_string)

```
 |  
| --- | --- |  
###  adelete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.ApacheSolrVectorStore.adelete_nodes "Permanent link")

```
adelete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Asynchronously delete nodes from vector store based on node ids.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[list[str]]`  |  The node IDs to delete.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  The filters to be applied to the node when deleting.  |  `None`  |  
|  `**delete_kwargs`  |  Extra keyword arguments, ignored by this implementation. These are added solely for interface compatibility.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/base.py`  
| 
```
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
```
 | 
```
async defadelete_nodes(
    self,
    node_ids: Optional[list[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Asynchronously delete nodes from vector store based on node ids.

    Args:
        node_ids: The node IDs to delete.
        filters: The filters to be applied to the node when deleting.
        **delete_kwargs:
            Extra keyword arguments, ignored by this implementation. These are added
            solely for interface compatibility.

    """
    del delete_kwargs  # unused

    has_filters = filters is not None and len(filters.filters)  0
    # we can efficiently delete by ID if no filters are specified
    if node_ids and not has_filters:
        logger.debug("Deleting %d nodes from Solr by ID", len(node_ids))
        await self.async_client.delete_by_id(node_ids)

    # otherwise, build a query to delete by IDs+filters
    else:
        query_string = self._build_delete_nodes_query(node_ids, filters)
        logger.debug("Deleting nodes from Solr using query: %s", query_string)
        await self.async_client.delete_by_query(query_string)

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.ApacheSolrVectorStore.clear "Permanent link")

```
clear() -> None

```

Delete all documents from the Solr collection synchronously. This action is not reversible!
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/base.py`  
| 
```
816
817
818
819
820
821
```
 | 
```
defclear(self) -> None:
"""
    Delete all documents from the Solr collection synchronously.
    This action is not reversible!
    """
    self.sync_client.clear_collection()

```
 |  
| --- | --- |  
###  aclear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.ApacheSolrVectorStore.aclear "Permanent link")

```
aclear() -> None

```

Delete all documents from the Solr collection asynchronously. This action is not reversible!
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/base.py`  
| 
```
823
824
825
826
827
828
```
 | 
```
async defaclear(self) -> None:
"""
    Delete all documents from the Solr collection asynchronously.
    This action is not reversible!
    """
    await self.async_client.clear_collection()

```
 |  
| --- | --- |  
###  close [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.ApacheSolrVectorStore.close "Permanent link")

```
close() -> None

```

Close the Solr client synchronously.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/base.py`  
| 
```
830
831
832
833
834
835
836
837
838
839
840
```
 | 
```
defclose(self) -> None:
"""Close the Solr client synchronously."""
    self.sync_client.close()
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # No running loop: create a temporary loop and close cleanly
        asyncio.run(self.async_client.close())
    else:
        # Running loop: schedule async close (not awaited)
        loop.create_task(self.async_client.close())  # noqa: RUF006

```
 |  
| --- | --- |  
###  aclose [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.ApacheSolrVectorStore.aclose "Permanent link")

```
aclose() -> None

```

Explicit aclose for callers running inside an event loop.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/base.py`  
| 
```
842
843
844
845
```
 | 
```
async defaclose(self) -> None:
"""Explicit aclose for callers running inside an event loop."""
    self.sync_client.close()
    await self.async_client.close()

```
 |  
| --- | --- |  
##  AsyncSolrClient [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.AsyncSolrClient "Permanent link")
Bases: `_BaseSolrClient`
A Solr client that wraps :py:class:`aiosolr.Client`.
See `aiosolr <https://github.com/youversion/aiosolr>`_ for implementation details.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/client/async_.py`  
| 
```
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
```
 | 
```
classAsyncSolrClient(_BaseSolrClient):
"""
    A Solr client that wraps :py:class:`aiosolr.Client`.

    See `aiosolr <https://github.com/youversion/aiosolr>`_ for implementation details.
    """

    async def_build_client(self) -> aiosolr.Client:
        try:
            logger.info("Initializing aiosolr client for URL: %s", self.base_url)
            # aiosolr.Client builds URLs for various actions in a hardcoded manner; for
            # URLs with ports (such as localhost URLs), we need to pass the parsed version
            # for external URLs, we need to pass the connection URL directly
            parsed_url = urlparse(self.base_url)
            *_, collection = parsed_url.path.split("/")
            if parsed_url.port is not None:
                args = {
                    "host": parsed_url.hostname,
                    "port": parsed_url.port,
                    "scheme": parsed_url.scheme,
                    "collection": collection,
                    **self._client_kwargs,
                }
            else:
                args = {
                    "connection_url": self._base_url,
                    **self._client_kwargs,
                }

            if sys.version_info  (3, 10):
                args["timeout"] = self._request_timeout_sec
            else:
                args["read_timeout"] = self._request_timeout_sec
                args["write_timeout"] = self._request_timeout_sec

            logger.debug("Initializing AIOSolr client with args: %s", self._base_url)
            client = aiosolr.Client(**args)
            await client.setup()
            # should not happen
            if client.session is None:  # pragma: no cover
                raise ValueError("AIOSolr client session was not created after setup")

            if self._headers:
                client.session.headers.update(self._headers)
                logger.debug(
                    "Updated AIOSolr client default headers with keys: %s",
                    list(self._headers.keys()),
                )
            return client

        except RuntimeError as exc:  # pragma: no cover
            raise ValueError(
                f"AIOSolr client cannot be initialized (likely due to running in "
                f"non-async context), type={type(exc)} err={exc}"
            ) fromexc

    async def_get_client(self) -> aiosolr.Client:
        # defer session creation until actually required
        if not self._client:
            self._client = await self._build_client()
        return self._client

    async defsearch(
        self, query_params: Mapping[str, Any], **kwargs: Any
    ) -> SolrSelectResponse:
"""
        Asynchronously search Solr with the input query, returning any matching documents.

        No validation is done on the input query dictionary.

        Args:
            query_params: A query dictionary to be sent to Solr.
            **kwargs:
                Additional keyword arguments to pass to :py:meth:`aiosolr.Client.query`.

        Returns:
            The deserialized response from Solr.

        """
        try:
            logger.info("Searching Solr with query='%s'", query_params)
            client = await self._get_client()
            results = await client.query(**query_params, **kwargs)
            response = SolrSelectResponse.from_aiosolr_response(results)
            logger.info(
                "Solr response received (path=select): status=%s qtime=%s hits=%s",
                response.response_header.status,
                response.response_header.q_time,
                response.response.num_found,
            )
            return response
        except aiosolr.SolrError as err:
            raise ValueError(
                f"Error during Aiosolr call, type={type(err)} err={err}"
            ) fromerr
        except ValidationError as err:
            raise ValueError(
                f"Unexpected response format from Solr: err={err.json()}"
            ) fromerr

    async defadd(
        self, documents: Sequence[Mapping[str, Any]], **kwargs: Any
    ) -> SolrUpdateResponse:
"""
        Asynchronously add documents to the Solr collection.

        No validation is done on the input documents.

        Args:
            documents:
                The documents to be added to the Solr collection. These documents should
                be serializable to JSON.
            **kwargs:
                Additional keyword arguments to be passed to :py:meth:`aiosolr.Client.add`.

        Returns:
            The deserialized update response from Solr.

        """
        logger.debug("Preparing documents for insertion into Solr collection")
        start = time.perf_counter()
        updated_docs = [prepare_document_for_solr(doc) for doc in documents]
        logger.debug(
            "Prepared %d documents, took %.2g seconds",
            len(documents),
            time.perf_counter() - start,
        )

        try:
            logger.info("Adding %d documents to the Solr collection", len(documents))
            client = await self._get_client()
            results = await client.update(data=updated_docs, **kwargs)
            response = SolrUpdateResponse.from_aiosolr_response(results)
            logger.info(
                "Solr response received (path=update): status=%s",
                response.response_header.status,
            )
            return response
        except aiosolr.SolrError as err:
            raise ValueError(
                f"Error during Aiosolr call, type={type(err)} err={err}"
            ) fromerr
        except ValidationError as err:
            raise ValueError(
                f"Unexpected response format from Solr: err={err.json()}"
            ) fromerr

    async def_delete(
        self, delete_command: Union[list[str], dict[str, Any]], **kwargs: Any
    ) -> SolrUpdateResponse:
        try:
            client = await self._get_client()
            delete_query = {"delete": delete_command}
            results = await client.update(data=delete_query, **kwargs)
            response = SolrUpdateResponse.from_aiosolr_response(results)
            logger.info(
                "Solr response received (path=update): status=%s qtime=%s",
                response.response_header.status,
                response.response_header.q_time,
            )
            return response
        except aiosolr.SolrError as err:
            raise ValueError(
                f"Error during Aiosolr call, type={type(err)} err={err}"
            ) fromerr
        except ValidationError as err:
            raise ValueError(
                f"Unexpected response format from Solr: err={err.json()}"
            ) fromerr

    async defdelete_by_query(
        self, query_string: str, **kwargs: Any
    ) -> SolrUpdateResponse:
"""
        Asynchronously delete documents from the Solr collection using a query string.

        No validation is done on the input query string.

        Args:
            query_string: A query string matching the documents that should be deleted.
            **kwargs:
                Additional keyword arguments to be passed to
                :py:meth:`aiosolr.Client.update`.

        Returns:
            The deserialized response from Solr.

        """
        logger.info(
            "Deleting documents from Solr matching query '%s', collection url=%s",
            query_string,
            self._base_url,
        )
        return await self._delete({"query": query_string}, **kwargs)

    async defdelete_by_id(
        self, ids: Sequence[str], **kwargs: Any
    ) -> SolrUpdateResponse:
"""
        Asynchronously delete documents from the Solr collection using their IDs.

        If the set of IDs is known, this is generally more efficient than using
        :py:meth:`.delete_by_query`.

        Args:
            ids: A sequence of document IDs to be deleted.
            **kwargs:
                Additional keyword arguments to be passed to
                :py:meth:`aiosolr.Client.update`.

        Returns:
            The deserialized response from Solr.

        Raises:
            ValueError: If the list of IDs is empty.

        """
        if not ids:
            raise ValueError("The list of IDs to delete cannot be empty")

        logger.info(
            "Deleting %d documents from the Solr collection by ID, collection url=%s",
            len(ids),
            self._base_url,
        )
        return await self._delete(list(ids), **kwargs)

    async defclear_collection(self, **kwargs) -> SolrUpdateResponse:
"""
        Asynchronously delete all documents from the Solr collection.

        Args:
            **kwargs:
                Optional keyword arguments to be passed to
                :py:meth:`aiosolr.Client.update`.

        Returns:
            The deserialized response from Solr.

        """
        return await self.delete_by_query(SolrConstants.QUERY_ALL, **kwargs)

    async defclose(self) -> None:
"""Close the ``aiosolr`` client, if it exists."""
        if self._client is not None:
            await cast(aiosolr.Client, self._client).close()

    def__del__(self) -> None:
"""Destroy the client, ensuring the session gets closed if it's not already."""
        tasks: set[Task] = set()
        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():
                task = loop.create_task(self.close())
                tasks.add(task)
                task.add_done_callback(tasks.discard)
            else:  # pragma: no cover
                loop.run_until_complete(self.close())
                return
        except RuntimeError as exc:
            logger.debug(
                "No running event loop, nothing to close, type=%s err='%s'",
                type(exc),
                exc,
            )
        # last resort catch for interpreter shutdown, not reasonably testable
        except Exception as exc:  # pragma: no cover
            logger.warning(
                "Failed to close the async Solr client, type=%s err='%s'",
                type(exc),
                exc,
            )

```
 |  
| --- | --- |  
###  search [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.AsyncSolrClient.search "Permanent link")

```
search(
    query_params: Mapping[, ], **kwargs: 
) -> SolrSelectResponse

```

Asynchronously search Solr with the input query, returning any matching documents.
No validation is done on the input query dictionary.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_params`  |  `Mapping[str, Any]`  |  A query dictionary to be sent to Solr.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments to pass to :py:meth:`aiosolr.Client.query`.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `SolrSelectResponse`  |  The deserialized response from Solr.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/client/async_.py`  
| 
```
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
```
 | 
```
async defsearch(
    self, query_params: Mapping[str, Any], **kwargs: Any
) -> SolrSelectResponse:
"""
    Asynchronously search Solr with the input query, returning any matching documents.

    No validation is done on the input query dictionary.

    Args:
        query_params: A query dictionary to be sent to Solr.
        **kwargs:
            Additional keyword arguments to pass to :py:meth:`aiosolr.Client.query`.

    Returns:
        The deserialized response from Solr.

    """
    try:
        logger.info("Searching Solr with query='%s'", query_params)
        client = await self._get_client()
        results = await client.query(**query_params, **kwargs)
        response = SolrSelectResponse.from_aiosolr_response(results)
        logger.info(
            "Solr response received (path=select): status=%s qtime=%s hits=%s",
            response.response_header.status,
            response.response_header.q_time,
            response.response.num_found,
        )
        return response
    except aiosolr.SolrError as err:
        raise ValueError(
            f"Error during Aiosolr call, type={type(err)} err={err}"
        ) fromerr
    except ValidationError as err:
        raise ValueError(
            f"Unexpected response format from Solr: err={err.json()}"
        ) fromerr

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.AsyncSolrClient.add "Permanent link")

```
add(
    documents: Sequence[Mapping[, ]], **kwargs: 
) -> SolrUpdateResponse

```

Asynchronously add documents to the Solr collection.
No validation is done on the input documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `documents`  |  `Sequence[Mapping[str, Any]]`  |  The documents to be added to the Solr collection. These documents should be serializable to JSON.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments to be passed to :py:meth:`aiosolr.Client.add`.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `SolrUpdateResponse`  |  The deserialized update response from Solr.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/client/async_.py`  
| 
```
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
```
 | 
```
async defadd(
    self, documents: Sequence[Mapping[str, Any]], **kwargs: Any
) -> SolrUpdateResponse:
"""
    Asynchronously add documents to the Solr collection.

    No validation is done on the input documents.

    Args:
        documents:
            The documents to be added to the Solr collection. These documents should
            be serializable to JSON.
        **kwargs:
            Additional keyword arguments to be passed to :py:meth:`aiosolr.Client.add`.

    Returns:
        The deserialized update response from Solr.

    """
    logger.debug("Preparing documents for insertion into Solr collection")
    start = time.perf_counter()
    updated_docs = [prepare_document_for_solr(doc) for doc in documents]
    logger.debug(
        "Prepared %d documents, took %.2g seconds",
        len(documents),
        time.perf_counter() - start,
    )

    try:
        logger.info("Adding %d documents to the Solr collection", len(documents))
        client = await self._get_client()
        results = await client.update(data=updated_docs, **kwargs)
        response = SolrUpdateResponse.from_aiosolr_response(results)
        logger.info(
            "Solr response received (path=update): status=%s",
            response.response_header.status,
        )
        return response
    except aiosolr.SolrError as err:
        raise ValueError(
            f"Error during Aiosolr call, type={type(err)} err={err}"
        ) fromerr
    except ValidationError as err:
        raise ValueError(
            f"Unexpected response format from Solr: err={err.json()}"
        ) fromerr

```
 |  
| --- | --- |  
###  delete_by_query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.AsyncSolrClient.delete_by_query "Permanent link")

```
delete_by_query(
    query_string: , **kwargs: 
) -> SolrUpdateResponse

```

Asynchronously delete documents from the Solr collection using a query string.
No validation is done on the input query string.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_string`  |  A query string matching the documents that should be deleted.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments to be passed to :py:meth:`aiosolr.Client.update`.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `SolrUpdateResponse`  |  The deserialized response from Solr.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/client/async_.py`  
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
```
 | 
```
async defdelete_by_query(
    self, query_string: str, **kwargs: Any
) -> SolrUpdateResponse:
"""
    Asynchronously delete documents from the Solr collection using a query string.

    No validation is done on the input query string.

    Args:
        query_string: A query string matching the documents that should be deleted.
        **kwargs:
            Additional keyword arguments to be passed to
            :py:meth:`aiosolr.Client.update`.

    Returns:
        The deserialized response from Solr.

    """
    logger.info(
        "Deleting documents from Solr matching query '%s', collection url=%s",
        query_string,
        self._base_url,
    )
    return await self._delete({"query": query_string}, **kwargs)

```
 |  
| --- | --- |  
###  delete_by_id [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.AsyncSolrClient.delete_by_id "Permanent link")

```
delete_by_id(
    ids: Sequence[], **kwargs: 
) -> SolrUpdateResponse

```

Asynchronously delete documents from the Solr collection using their IDs.
If the set of IDs is known, this is generally more efficient than using :py:meth:`.delete_by_query`.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ids`  |  `Sequence[str]`  |  A sequence of document IDs to be deleted.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments to be passed to :py:meth:`aiosolr.Client.update`.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `SolrUpdateResponse`  |  The deserialized response from Solr.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If the list of IDs is empty.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/client/async_.py`  
| 
```
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
```
 | 
```
async defdelete_by_id(
    self, ids: Sequence[str], **kwargs: Any
) -> SolrUpdateResponse:
"""
    Asynchronously delete documents from the Solr collection using their IDs.

    If the set of IDs is known, this is generally more efficient than using
    :py:meth:`.delete_by_query`.

    Args:
        ids: A sequence of document IDs to be deleted.
        **kwargs:
            Additional keyword arguments to be passed to
            :py:meth:`aiosolr.Client.update`.

    Returns:
        The deserialized response from Solr.

    Raises:
        ValueError: If the list of IDs is empty.

    """
    if not ids:
        raise ValueError("The list of IDs to delete cannot be empty")

    logger.info(
        "Deleting %d documents from the Solr collection by ID, collection url=%s",
        len(ids),
        self._base_url,
    )
    return await self._delete(list(ids), **kwargs)

```
 |  
| --- | --- |  
###  clear_collection [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.AsyncSolrClient.clear_collection "Permanent link")

```
clear_collection(**kwargs) -> SolrUpdateResponse

```

Asynchronously delete all documents from the Solr collection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `**kwargs`  |  Optional keyword arguments to be passed to :py:meth:`aiosolr.Client.update`.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `SolrUpdateResponse`  |  The deserialized response from Solr.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/client/async_.py`  
| 
```
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
```
 | 
```
async defclear_collection(self, **kwargs) -> SolrUpdateResponse:
"""
    Asynchronously delete all documents from the Solr collection.

    Args:
        **kwargs:
            Optional keyword arguments to be passed to
            :py:meth:`aiosolr.Client.update`.

    Returns:
        The deserialized response from Solr.

    """
    return await self.delete_by_query(SolrConstants.QUERY_ALL, **kwargs)

```
 |  
| --- | --- |  
###  close [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.AsyncSolrClient.close "Permanent link")

```
close() -> None

```

Close the `aiosolr` client, if it exists.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/client/async_.py`  
| 
```
268
269
270
271
```
 | 
```
async defclose(self) -> None:
"""Close the ``aiosolr`` client, if it exists."""
    if self._client is not None:
        await cast(aiosolr.Client, self._client).close()

```
 |  
| --- | --- |  
##  SyncSolrClient [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.SyncSolrClient "Permanent link")
Bases: `_BaseSolrClient`
A synchronous Solr client that wraps :py:class:`pysolr.Solr`.
See `pysolr <https://github.com/django-haystack/pysolr/blob/master/pysolr.py>`_ for implementation details.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/client/sync.py`  
| 
```
 23
 24
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
```
 | 
```
classSyncSolrClient(_BaseSolrClient):
"""
    A synchronous Solr client that wraps :py:class:`pysolr.Solr`.

    See `pysolr <https://github.com/django-haystack/pysolr/blob/master/pysolr.py>`_ for
    implementation details.
    """

    def_get_client(self) -> pysolr.Solr:
        if self._client is None:
            self._client = self._build_client()
        return self._client

    def_build_client(self) -> pysolr.Solr:
        logger.info("Initializing pysolr client for URL: %s", self.base_url)
        client = pysolr.Solr(
            url=self.base_url, timeout=self._request_timeout_sec, **self._client_kwargs
        )
        if self._headers:
            session = client.get_session()
            session.headers.update(self._headers)
            logger.debug(
                "Updated pysolr client default headers with keys: %s",
                list(self._headers.keys()),
            )
        return client

    defclose(self) -> None:
"""Close the underlying Solr client session."""
        if self._client:
            logger.debug("Closing the Solr client session")
            # pysolr doesn't expose a close method, so we directly close the underlying session
            self._client.get_session().close()
            self._client = None

    defsearch(
        self, query_params: Mapping[str, Any], **kwargs: Any
    ) -> SolrSelectResponse:
"""
        Search Solr with the input query, returning any matching documents.

        No validation is done on the input query dictionary.

        Args:
            query_params: A query dictionary to be sent to Solr.
            **kwargs:
                Additional keyword arguments to pass to :py:meth:`pysolr.Solr.search`.

        Returns:
            The deserialized response from Solr.

        """
        try:
            logger.info("Searching Solr with query='%s'", query_params)
            results = self._get_client().search(**query_params, **kwargs)
            response = SolrSelectResponse.from_pysolr_results(results)
            logger.info(
                "Solr response received (path=select): status=%s qtime=%s hits=%s",
                response.response_header.status,
                response.response_header.q_time,
                response.response.num_found,
            )
            return response
        except pysolr.SolrError as err:
            raise ValueError(
                f"Error during Pysolr call, type={type(err)} err={err}"
            ) fromerr
        except ValidationError as err:
            raise ValueError(
                f"Unexpected response format from Solr: err={err.json()}"
            ) fromerr

    defadd(
        self, documents: Sequence[Mapping[str, Any]], **kwargs: Any
    ) -> SolrUpdateResponse:
"""
        Add documents to the Solr collection.

        No validation is done on the input documents.

        Args:
            documents:
                The documents to be added to the Solr collection. These documents should
                be serializable to JSON.
            **kwargs:
                Additional keyword arguments to pass to :py:meth:`pysolr.Solr.add`.

        """
        logger.debug("Preparing documents for insertion into Solr collection")
        start = time.perf_counter()
        updated_docs = [prepare_document_for_solr(doc) for doc in documents]
        logger.debug(
            "Prepared %d documents, took %.2g seconds",
            len(documents),
            time.perf_counter() - start,
        )

        try:
            logger.info("Adding %d documents to the Solr collection", len(documents))
            # pysolr.Solr.add is not typed, but in code tracing it will always be this
            res_text = str(self._get_client().add(updated_docs, **kwargs))
            # update responses in pysolr are always in XML format
            # response = SolrUpdateResponse.from_xml(res_text)
            response = SolrUpdateResponse.model_validate_json(res_text)
            logger.info(
                "Solr response received (path=update): status=%s qtime=%s",
                response.response_header.status,
                response.response_header.q_time,
            )
            return response
        except pysolr.SolrError as err:
            raise ValueError(
                f"Error during Pysolr call, type={type(err)} err={err}"
            ) fromerr
        except ValidationError as err:
            raise ValueError(
                f"Unexpected response format from Solr: err={err.json()}"
            ) fromerr

    def_delete(
        self, query_string: Optional[str], ids: Optional[list[str]], **kwargs: Any
    ) -> SolrUpdateResponse:
        try:
            res_text = self._get_client().delete(q=query_string, id=ids, **kwargs)
            # update responses in pysolr are always in XML format
            response = SolrUpdateResponse.from_xml(res_text)
            logger.info(
                "Solr response received (path=update): status=%s qtime=%s",
                response.response_header.status,
                response.response_header.q_time,
            )
            return response
        except pysolr.SolrError as err:
            raise ValueError(
                f"Error during Pysolr call, type={type(err)} err={err}"
            ) fromerr
        except ParseError as err:
            raise ValueError(
                f"Error parsing XML response from Solr: err={err}"
            ) fromerr
        except ValidationError as err:
            raise ValueError(
                f"Unexpected response format from Solr: err={err.json()}"
            ) fromerr

    defdelete_by_query(self, query_string: str, **kwargs: Any) -> SolrUpdateResponse:
"""
        Delete documents from the Solr collection using a query string.

        Args:
            query_string: A query string matching the documents that should be deleted.
            **kwargs:
                Additional keyword arguments to pass to :py:meth:`pysolr.Solr.delete`.

        Returns:
            The deserialized response from Solr.

        """
        logger.info(
            "Deleting documents from Solr matching query '%s', collection url=%s",
            query_string,
            self._base_url,
        )
        return self._delete(query_string=query_string, ids=None, **kwargs)

    defdelete_by_id(self, ids: Sequence[str], **kwargs: Any) -> SolrUpdateResponse:
"""
        Delete documents from the Solr collection using their IDs.

        If the set of IDs is known, this is generally more efficient than using
        :py:meth:`.delete_by_query`.

        Args:
            ids: A sequence of document IDs to be deleted.
            **kwargs:
                Additional keyword arguments to pass to :py:meth:`pysolr.Solr.delete`.

        Returns:
            The deserialized response from Solr.

        Raises:
            ValueError: If the list of IDs is empty.

        """
        if not ids:
            raise ValueError("The list of IDs to delete cannot be empty")

        logger.info(
            "Deleting %d documents from the Solr collection by ID, collection url=%s",
            len(ids),
            self._base_url,
        )
        return self._delete(query_string=None, ids=list(ids), **kwargs)

    defclear_collection(self, **kwargs: Any) -> SolrUpdateResponse:
"""
        Delete all documents from the Solr collection.

        Args:
            **kwargs:
                Optional keyword arguments to be passed to
                :py:meth:`pysolr.Solr.delete`.


        Returns:
            The deserialized response from Solr.

        """
        logger.warning("The Solr collection is being cleared")
        return self.delete_by_query(SolrConstants.QUERY_ALL, **kwargs)

```
 |  
| --- | --- |  
###  close [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.SyncSolrClient.close "Permanent link")

```
close() -> None

```

Close the underlying Solr client session.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/client/sync.py`  
| 
```
50
51
52
53
54
55
56
```
 | 
```
defclose(self) -> None:
"""Close the underlying Solr client session."""
    if self._client:
        logger.debug("Closing the Solr client session")
        # pysolr doesn't expose a close method, so we directly close the underlying session
        self._client.get_session().close()
        self._client = None

```
 |  
| --- | --- |  
###  search [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.SyncSolrClient.search "Permanent link")

```
search(
    query_params: Mapping[, ], **kwargs: 
) -> SolrSelectResponse

```

Search Solr with the input query, returning any matching documents.
No validation is done on the input query dictionary.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_params`  |  `Mapping[str, Any]`  |  A query dictionary to be sent to Solr.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments to pass to :py:meth:`pysolr.Solr.search`.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `SolrSelectResponse`  |  The deserialized response from Solr.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/client/sync.py`  
| 
```
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
```
 | 
```
defsearch(
    self, query_params: Mapping[str, Any], **kwargs: Any
) -> SolrSelectResponse:
"""
    Search Solr with the input query, returning any matching documents.

    No validation is done on the input query dictionary.

    Args:
        query_params: A query dictionary to be sent to Solr.
        **kwargs:
            Additional keyword arguments to pass to :py:meth:`pysolr.Solr.search`.

    Returns:
        The deserialized response from Solr.

    """
    try:
        logger.info("Searching Solr with query='%s'", query_params)
        results = self._get_client().search(**query_params, **kwargs)
        response = SolrSelectResponse.from_pysolr_results(results)
        logger.info(
            "Solr response received (path=select): status=%s qtime=%s hits=%s",
            response.response_header.status,
            response.response_header.q_time,
            response.response.num_found,
        )
        return response
    except pysolr.SolrError as err:
        raise ValueError(
            f"Error during Pysolr call, type={type(err)} err={err}"
        ) fromerr
    except ValidationError as err:
        raise ValueError(
            f"Unexpected response format from Solr: err={err.json()}"
        ) fromerr

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.SyncSolrClient.add "Permanent link")

```
add(
    documents: Sequence[Mapping[, ]], **kwargs: 
) -> SolrUpdateResponse

```

Add documents to the Solr collection.
No validation is done on the input documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `documents`  |  `Sequence[Mapping[str, Any]]`  |  The documents to be added to the Solr collection. These documents should be serializable to JSON.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments to pass to :py:meth:`pysolr.Solr.add`.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/client/sync.py`  
| 
```
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
```
 | 
```
defadd(
    self, documents: Sequence[Mapping[str, Any]], **kwargs: Any
) -> SolrUpdateResponse:
"""
    Add documents to the Solr collection.

    No validation is done on the input documents.

    Args:
        documents:
            The documents to be added to the Solr collection. These documents should
            be serializable to JSON.
        **kwargs:
            Additional keyword arguments to pass to :py:meth:`pysolr.Solr.add`.

    """
    logger.debug("Preparing documents for insertion into Solr collection")
    start = time.perf_counter()
    updated_docs = [prepare_document_for_solr(doc) for doc in documents]
    logger.debug(
        "Prepared %d documents, took %.2g seconds",
        len(documents),
        time.perf_counter() - start,
    )

    try:
        logger.info("Adding %d documents to the Solr collection", len(documents))
        # pysolr.Solr.add is not typed, but in code tracing it will always be this
        res_text = str(self._get_client().add(updated_docs, **kwargs))
        # update responses in pysolr are always in XML format
        # response = SolrUpdateResponse.from_xml(res_text)
        response = SolrUpdateResponse.model_validate_json(res_text)
        logger.info(
            "Solr response received (path=update): status=%s qtime=%s",
            response.response_header.status,
            response.response_header.q_time,
        )
        return response
    except pysolr.SolrError as err:
        raise ValueError(
            f"Error during Pysolr call, type={type(err)} err={err}"
        ) fromerr
    except ValidationError as err:
        raise ValueError(
            f"Unexpected response format from Solr: err={err.json()}"
        ) fromerr

```
 |  
| --- | --- |  
###  delete_by_query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.SyncSolrClient.delete_by_query "Permanent link")

```
delete_by_query(
    query_string: , **kwargs: 
) -> SolrUpdateResponse

```

Delete documents from the Solr collection using a query string.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_string`  |  A query string matching the documents that should be deleted.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments to pass to :py:meth:`pysolr.Solr.delete`.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `SolrUpdateResponse`  |  The deserialized response from Solr.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/client/sync.py`  
| 
```
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
```
 | 
```
defdelete_by_query(self, query_string: str, **kwargs: Any) -> SolrUpdateResponse:
"""
    Delete documents from the Solr collection using a query string.

    Args:
        query_string: A query string matching the documents that should be deleted.
        **kwargs:
            Additional keyword arguments to pass to :py:meth:`pysolr.Solr.delete`.

    Returns:
        The deserialized response from Solr.

    """
    logger.info(
        "Deleting documents from Solr matching query '%s', collection url=%s",
        query_string,
        self._base_url,
    )
    return self._delete(query_string=query_string, ids=None, **kwargs)

```
 |  
| --- | --- |  
###  delete_by_id [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.SyncSolrClient.delete_by_id "Permanent link")

```
delete_by_id(
    ids: Sequence[], **kwargs: 
) -> SolrUpdateResponse

```

Delete documents from the Solr collection using their IDs.
If the set of IDs is known, this is generally more efficient than using :py:meth:`.delete_by_query`.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ids`  |  `Sequence[str]`  |  A sequence of document IDs to be deleted.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments to pass to :py:meth:`pysolr.Solr.delete`.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `SolrUpdateResponse`  |  The deserialized response from Solr.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If the list of IDs is empty.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/client/sync.py`  
| 
```
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
```
 | 
```
defdelete_by_id(self, ids: Sequence[str], **kwargs: Any) -> SolrUpdateResponse:
"""
    Delete documents from the Solr collection using their IDs.

    If the set of IDs is known, this is generally more efficient than using
    :py:meth:`.delete_by_query`.

    Args:
        ids: A sequence of document IDs to be deleted.
        **kwargs:
            Additional keyword arguments to pass to :py:meth:`pysolr.Solr.delete`.

    Returns:
        The deserialized response from Solr.

    Raises:
        ValueError: If the list of IDs is empty.

    """
    if not ids:
        raise ValueError("The list of IDs to delete cannot be empty")

    logger.info(
        "Deleting %d documents from the Solr collection by ID, collection url=%s",
        len(ids),
        self._base_url,
    )
    return self._delete(query_string=None, ids=list(ids), **kwargs)

```
 |  
| --- | --- |  
###  clear_collection [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.SyncSolrClient.clear_collection "Permanent link")

```
clear_collection(**kwargs: ) -> SolrUpdateResponse

```

Delete all documents from the Solr collection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `**kwargs`  |  Optional keyword arguments to be passed to :py:meth:`pysolr.Solr.delete`.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `SolrUpdateResponse`  |  The deserialized response from Solr.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/client/sync.py`  
| 
```
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
```
 | 
```
defclear_collection(self, **kwargs: Any) -> SolrUpdateResponse:
"""
    Delete all documents from the Solr collection.

    Args:
        **kwargs:
            Optional keyword arguments to be passed to
            :py:meth:`pysolr.Solr.delete`.


    Returns:
        The deserialized response from Solr.

    """
    logger.warning("The Solr collection is being cleared")
    return self.delete_by_query(SolrConstants.QUERY_ALL, **kwargs)

```
 |  
| --- | --- |  
##  BoostedTextField [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.BoostedTextField "Permanent link")
Bases: `BaseModel`
A text field with an optional boost value for Solr queries.
This model represents a Solr field that can have a multiplicative boost factor applied to increase or decrease its relevance in search results. Boost factors greater than 1.0 increase relevance, while factors between 0.0 and 1.0 decrease it.
Attributes: field: The Solr field name to include in the search. boost_factor: The boost multiplier to apply. Defaults to 1.0 (no boost). Values > 1.0 increase relevance, 0.0 < values < 1.0 decrease it.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/types.py`  
| 
```
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
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
```
 | 
```
classBoostedTextField(BaseModel):
"""
    A text field with an optional boost value for Solr queries.

    This model represents a Solr field that can have a multiplicative boost
    factor applied to increase or decrease its relevance in search results.
    Boost factors greater than 1.0 increase relevance, while factors between
    0.0 and 1.0 decrease it.

    Attributes:
    field: The Solr field name to include in the search.
    boost_factor: The boost multiplier to apply. Defaults
        to 1.0 (no boost). Values > 1.0 increase relevance, 0.0 < values < 1.0
        decrease it.

    """

    field: str
    boost_factor: float = 1.0

    defget_query_str(self) -> str:  # pragma: no cover
"""
        Return Solr query syntax representation for this field.

        If the boost factor is 1.0 (default) the field term is returned as-is;
        otherwise the canonical Solr boost syntax ``field^boost_factor`` is produced.
        """
        if self.boost_factor != 1.0:
            return f"{self.field}^{self.boost_factor}"
        return self.field

```
 |  
| --- | --- |  
###  get_query_str [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/solr/#llama_index.vector_stores.solr.BoostedTextField.get_query_str "Permanent link")

```
get_query_str() -> 

```

Return Solr query syntax representation for this field.
If the boost factor is 1.0 (default) the field term is returned as-is; otherwise the canonical Solr boost syntax `field^boost_factor` is produced.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-solr/llama_index/vector_stores/solr/types.py`  
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
```
 | 
```
defget_query_str(self) -> str:  # pragma: no cover
"""
    Return Solr query syntax representation for this field.

    If the boost factor is 1.0 (default) the field term is returned as-is;
    otherwise the canonical Solr boost syntax ``field^boost_factor`` is produced.
    """
    if self.boost_factor != 1.0:
        return f"{self.field}^{self.boost_factor}"
    return self.field

```
 |  
| --- | --- |  
options: members:
