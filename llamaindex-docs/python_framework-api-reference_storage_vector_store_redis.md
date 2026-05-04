# Redis
##  RedisVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore "Permanent link")
Bases: 
RedisVectorStore.
The RedisVectorStore takes a user-defined schema object and a Redis connection client or URL string. The schema is optional, but useful for: - Defining a custom index name, key prefix, and key separator. - Defining _additional_ metadata fields to use as query filters. - Setting custom specifications on fields to improve search quality, e.g which vector index algorithm to use.
Other Notes: - All embeddings and docs are stored in Redis. During query time, the index uses Redis to query for the top k most similar nodes. - Redis & LlamaIndex expect at least 4 _required_ fields for any schema, default or custom, `id`, `doc_id`, `text`, `vector`.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `schema`  |  `IndexSchema`  |  Redis index schema object.  |  `None`  |  
|  `redis_client`  |  `Redis`  |  Redis client connection.  |  `None`  |  
|  `redis_url`  |  Redis server URL. Defaults to "redis://localhost:6379".  |  `None`  |  
|  `overwrite`  |  `bool`  |  Whether to overwrite the index if it already exists. Defaults to False.  |  `False`  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If your Redis server does not have search or JSON enabled.  |  
|  `ValueError`  |  If a Redis connection failed to be established.  |  
|  `ValueError`  |  If an invalid schema is provided.  |  
Example
from redisvl.schema import IndexSchema from llama_index.vector_stores.redis import RedisVectorStore
### Use default schema[#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore--use-default-schema "Permanent link")
rds = RedisVectorStore(redis_url="redis://localhost:6379")
### Use custom schema from dict[#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore--use-custom-schema-from-dict "Permanent link")
schema = IndexSchema.from_dict({ "index": {"name": "my-index", "prefix": "docs"}, "fields": [ {"name": "id", "type": "tag"}, {"name": "doc_id", "type": "tag}, {"name": "text", "type": "text"}, {"name": "vector", "type": "vector", "attrs": {"dims": 1536, "algorithm": "flat"}} ] }) vector_store = RedisVectorStore( schema=schema, redis_url="redis://localhost:6379" )
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
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
866
867
868
869
870
871
872
873
874
875
876
877
878
879
880
881
882
883
884
885
886
887
888
889
890
891
892
893
894
895
896
897
898
899
900
901
902
903
904
905
906
907
908
909
910
911
912
913
914
915
916
917
918
919
920
921
922
923
924
925
926
927
928
929
930
931
932
933
934
935
936
937
```
 | 
```
classRedisVectorStore(BasePydanticVectorStore):
"""
    RedisVectorStore.

    The RedisVectorStore takes a user-defined schema object and a Redis connection
    client or URL string. The schema is optional, but useful for:
    - Defining a custom index name, key prefix, and key separator.
    - Defining *additional* metadata fields to use as query filters.
    - Setting custom specifications on fields to improve search quality, e.g
    which vector index algorithm to use.

    Other Notes:
    - All embeddings and docs are stored in Redis. During query time, the index
    uses Redis to query for the top k most similar nodes.
    - Redis & LlamaIndex expect at least 4 *required* fields for any schema, default or custom,
    `id`, `doc_id`, `text`, `vector`.

    Args:
        schema (IndexSchema, optional): Redis index schema object.
        redis_client (Redis, optional): Redis client connection.
        redis_url (str, optional): Redis server URL.
            Defaults to "redis://localhost:6379".
        overwrite (bool, optional): Whether to overwrite the index if it already exists.
            Defaults to False.

    Raises:
        ValueError: If your Redis server does not have search or JSON enabled.
        ValueError: If a Redis connection failed to be established.
        ValueError: If an invalid schema is provided.

    Example:
        from redisvl.schema import IndexSchema
        from llama_index.vector_stores.redis import RedisVectorStore

        # Use default schema
        rds = RedisVectorStore(redis_url="redis://localhost:6379")

        # Use custom schema from dict
        schema = IndexSchema.from_dict({
            "index": {"name": "my-index", "prefix": "docs"},
            "fields": [
                {"name": "id", "type": "tag"},
                {"name": "doc_id", "type": "tag},
                {"name": "text", "type": "text"},
                {"name": "vector", "type": "vector", "attrs": {"dims": 1536, "algorithm": "flat"}}


        vector_store = RedisVectorStore(
            schema=schema,
            redis_url="redis://localhost:6379"


    """

    stores_text: bool = True
    stores_node: bool = True
    flat_metadata: bool = False
    created_async_index: bool = False
    legacy_filters: bool = False

    _index: SearchIndex = PrivateAttr()
    _async_index: AsyncSearchIndex = PrivateAttr()
    _tokenizer: Any = PrivateAttr()
    _redis_client: Any = PrivateAttr()
    _redis_client_async: Any = PrivateAttr()
    _prefix: str = PrivateAttr()
    _index_name: str = PrivateAttr()
    _index_args: Dict[str, Any] = PrivateAttr()
    _metadata_fields: List[str] = PrivateAttr()
    _overwrite: bool = PrivateAttr()
    _return_fields: List[str] = PrivateAttr()

    def__init__(
        self,
        schema: Optional[IndexSchema] = None,
        redis_client: Optional[Redis] = None,
        redis_client_async: Optional[RedisAsync] = None,
        redis_url: Optional[str] = None,
        overwrite: bool = False,
        return_fields: Optional[List[str]] = None,
        legacy_filters: Optional[bool] = False,
        **kwargs: Any,
    ) -> None:
        super().__init__()
        # check for indicators of old schema
        self._flag_old_kwargs(**kwargs)
        self.legacy_filters = legacy_filters
        # Setup schema
        if not schema:
            logger.info("Using default RedisVectorStore schema.")
            schema = RedisVectorStoreSchema()

        self._validate_schema(schema)
        self._return_fields = return_fields or [
            NODE_ID_FIELD_NAME,
            DOC_ID_FIELD_NAME,
            TEXT_FIELD_NAME,
            NODE_CONTENT_FIELD_NAME,
        ]
        self._overwrite = overwrite
        self._index = SearchIndex(
            schema=schema, redis_client=redis_client, redis_url=redis_url
        )
        self._redis_client_async = redis_client_async
        if redis_client or redis_url:
            if redis_url and not redis_client:
                redis_client = Redis.from_url(redis_url)
            self._redis_client = redis_client
            self.create_index()
            if not self._redis_client_async:
                self._redis_client_async = redis_async.Redis(
                    host=redis_client.connection_pool.connection_kwargs["host"],
                    port=redis_client.connection_pool.connection_kwargs["port"],
                    **{
                        k: v
                        for k, v in redis_client.connection_pool.connection_kwargs.items()
                        if k not in ["host", "port"]
                    },
                )
        if not redis_client and not redis_url and not redis_client_async:
            raise Exception(
                "Either redis_client, redis_url, or redis_client_async need to be defined"
            )
        self._async_index = AsyncSearchIndex(
            schema=schema, redis_client=self._redis_client_async
        )

    def_flag_old_kwargs(self, **kwargs):
        old_kwargs = [
            "index_name",
            "index_prefix",
            "prefix_ending",
            "index_args",
            "metadata_fields",
        ]
        for kwarg in old_kwargs:
            if kwarg in kwargs:
                raise ValueError(
                    f"Deprecated kwarg, {kwarg}, found upon initialization. "
                    "RedisVectorStore now requires an IndexSchema object. "
                    "See the documentation for a complete example: https://docs.llamaindex.ai/en/stable/examples/vector_stores/RedisIndexDemo/"
                )

    def_validate_schema(self, schema: IndexSchema) -> str:
        base_schema = RedisVectorStoreSchema()
        for name, field in base_schema.fields.items():
            if (name not in schema.fields) or (
                not schema.fields[name].type == field.type
            ):
                raise ValueError(
                    f"Required field {name} must be present in the index "
                    f"and of type {schema.fields[name].type}"
                )

    @property
    defclient(self) -> "Redis":
"""Return the redis client instance."""
        if self._async_index:
            return self._async_index.client
        return self._index.client

    @property
    defindex_name(self) -> str:
"""Return the name of the index based on the schema."""
        return self._index.name

    @property
    defschema(self) -> IndexSchema:
"""Return the index schema."""
        if self._async_index:
            return self._async_index.schema
        return self._index.schema

    defset_return_fields(self, return_fields: List[str]) -> None:
"""Update the return fields for the query response."""
        self._return_fields = return_fields

    defindex_exists(self) -> bool:
"""
        Check whether the index exists in Redis.

        Returns:
            bool: True or False.

        """
        return self._index.exists()

    async defasync_index_exists(self) -> bool:
"""
        Check whether the index exists in Redis.

        Returns:
            bool: True or False.

        """
        if not self.created_async_index:
            await self.async_create_index()
        return True

    defcreate_index(self, overwrite: Optional[bool] = None) -> None:
"""Create an index in Redis."""
        if overwrite is None:
            overwrite = self._overwrite
        # Create index honoring overwrite policy
        if overwrite:
            self._index.create(overwrite=overwrite, drop=True)
        else:
            self._index.create()

    async defasync_create_index(self, overwrite: Optional[bool] = None) -> None:
"""Create an async index in Redis."""
        if overwrite is None:
            overwrite = self._overwrite
        # Create index honoring overwrite policy
        if overwrite:
            await self._async_index.create(overwrite=True, drop=True)
        else:
            await self._async_index.create()
        self.created_async_index = True

    async defasync_add(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
        Add nodes to the index.

        Args:
            nodes (List[BaseNode]): List of nodes with embeddings

        Returns:
            List[str]: List of ids of the documents added to the index.

        Raises:
            ValueError: If the index already exists and overwrite is False.

        """
        # Check to see if empty document list was passed
        await self.async_index_exists()
        if len(nodes) == 0:
            return []

        # Now check for the scenario where user is trying to index embeddings that don't align with schema
        embedding_len = len(nodes[0].get_embedding())
        expected_dims = self._async_index.schema.fields[VECTOR_FIELD_NAME].attrs.dims
        if expected_dims != embedding_len:
            raise ValueError(
                f"Attempting to index embeddings of dim {embedding_len} "
                f"which doesn't match the index schema expectation of {expected_dims}. "
                "Please review the Redis integration example to learn how to customize schema. "
                ""
            )

        data: List[Dict[str, Any]] = []
        for node in nodes:
            embedding = node.get_embedding()
            record = {
                NODE_ID_FIELD_NAME: node.node_id,
                DOC_ID_FIELD_NAME: node.ref_doc_id,
                TEXT_FIELD_NAME: node.get_content(metadata_mode=MetadataMode.NONE),
                VECTOR_FIELD_NAME: array_to_buffer(embedding, dtype="FLOAT32"),
            }
            # parse and append metadata
            additional_metadata = node_to_metadata_dict(
                node, remove_text=True, flat_metadata=self.flat_metadata
            )
            data.append({**record, **additional_metadata})

        # Load nodes to Redis
        for mapping in data:
            mapping.pop(
                "sub_dicts", None
            )  # Remove if present from VectorMemory to avoid serialization issues
        keys = await self._async_index.load(
            data, id_field=NODE_ID_FIELD_NAME, **add_kwargs
        )
        logger.info(f"Added {len(keys)} documents to index {self._async_index.name}")
        return [
            key.strip(self._async_index.prefix + self._async_index.key_separator)
            for key in keys
        ]

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
        Add nodes to the index.

        Args:
            nodes (List[BaseNode]): List of nodes with embeddings

        Returns:
            List[str]: List of ids of the documents added to the index.

        Raises:
            ValueError: If the index already exists and overwrite is False.

        """
        # Check to see if empty document list was passed
        if len(nodes) == 0:
            return []

        # Now check for the scenario where user is trying to index embeddings that don't align with schema
        embedding_len = len(nodes[0].get_embedding())
        expected_dims = self._index.schema.fields[VECTOR_FIELD_NAME].attrs.dims
        if expected_dims != embedding_len:
            raise ValueError(
                f"Attempting to index embeddings of dim {embedding_len} "
                f"which doesn't match the index schema expectation of {expected_dims}. "
                "Please review the Redis integration example to learn how to customize schema. "
                ""
            )

        data: List[Dict[str, Any]] = []
        for node in nodes:
            embedding = node.get_embedding()
            record = {
                NODE_ID_FIELD_NAME: node.node_id,
                DOC_ID_FIELD_NAME: node.ref_doc_id,
                TEXT_FIELD_NAME: node.get_content(metadata_mode=MetadataMode.NONE),
                VECTOR_FIELD_NAME: array_to_buffer(embedding, dtype="FLOAT32"),
            }
            # parse and append metadata
            additional_metadata = node_to_metadata_dict(
                node, remove_text=True, flat_metadata=self.flat_metadata
            )
            data.append({**record, **additional_metadata})

        # Load nodes to Redis
        keys = self._index.load(data, id_field=NODE_ID_FIELD_NAME, **add_kwargs)
        logger.info(f"Added {len(keys)} documents to index {self._index.name}")
        return [
            key.strip(self._index.prefix + self._index.key_separator) for key in keys
        ]

    def_build_node_id_filter_expression(self, node_ids: list[str]) -> FilterExpression:
"""Build a Redis filter expression for one or more node IDs."""
        if not node_ids:
            raise ValueError("node_ids must be provided.")

        node_id_filter = Tag(NODE_ID_FIELD_NAME) == node_ids[0]
        for node_id in node_ids[1:]:
            node_id_filter = node_id_filter | (Tag(NODE_ID_FIELD_NAME) == node_id)
        return node_id_filter

    def_build_node_id_filter_string(self, node_ids: list[str]) -> str:
"""Build a Redis filter string for one or more node IDs."""
        tokenizer = TokenEscaper()
        values = "|".join(tokenizer.escape(str(node_id)) for node_id in node_ids)
        return f"(@{NODE_ID_FIELD_NAME}:{{{values}}})"

    def_has_unindexed_filters(
        self, metadata_filters: Optional[MetadataFilters]
    ) -> bool:
"""Return True when any requested filter field is missing from the schema."""
        if not metadata_filters or not metadata_filters.filters:
            return False

        for metadata_filter in metadata_filters.filters:
            if isinstance(metadata_filter, MetadataFilters):
                if self._has_unindexed_filters(metadata_filter):
                    return True
                continue
            if not self._index.schema.fields.get(metadata_filter.key):
                return True

        return False

    def_build_selection_filter(
        self,
        node_ids: Optional[list[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> str | FilterExpression:
"""Build a legacy or modern Redis selector; combine inputs with AND, or return match-all when none are provided."""
        if self.legacy_filters:
            selector_parts = []
            if node_ids:
                selector_parts.append(self._build_node_id_filter_string(node_ids))
            if filters:
                selector_parts.append(self._to_redis_filters(filters))
            return " ".join(selector_parts) if selector_parts else "*"

        selector = FilterExpression("*")
        if node_ids:
            selector = selector  self._build_node_id_filter_expression(node_ids)
        if filters:
            selector = selector  self._create_redis_filter_expression(filters)
        return selector

    def_get_filter_query(
        self,
        node_ids: Optional[list[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> Optional[FilterQuery]:
"""Build a filter query sized to fetch all matching documents."""
        selector = self._build_selection_filter(node_ids=node_ids, filters=filters)
        total = self._index.query(CountQuery(selector))
        if total == 0:
            return None
        return FilterQuery(
            filter_expression=selector,
            return_fields=self._return_fields,
            num_results=total,
        )

    async def_aget_filter_query(
        self,
        node_ids: Optional[list[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> Optional[FilterQuery]:
"""Build an async filter query sized to fetch all matching documents."""
        selector = self._build_selection_filter(node_ids=node_ids, filters=filters)
        total = await self._async_index.query(CountQuery(selector))
        if total == 0:
            return None
        return FilterQuery(
            filter_expression=selector,
            return_fields=self._return_fields,
            num_results=total,
        )

    defget_nodes(
        self,
        node_ids: Optional[list[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> list[BaseNode]:
"""Get nodes by node_ids or filters; at least one selector is required."""
        if not node_ids and not filters:
            raise ValueError("Either node_ids or filters must be provided.")
        if filters and self._has_unindexed_filters(filters):
            logger.warning(f"{NO_INDEXED_FILTERS} Node lookup returns no matches.")
            return []
        filter_query = self._get_filter_query(node_ids=node_ids, filters=filters)
        if filter_query is None:
            return []
        results = self._index.query(filter_query)
        return self._process_query_results(results, filter_query).nodes or []

    async defaget_nodes(
        self,
        node_ids: Optional[list[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> list[BaseNode]:
"""Async get nodes by node_ids or filters; at least one selector is required."""
        await self.async_index_exists()
        if not node_ids and not filters:
            raise ValueError("Either node_ids or filters must be provided.")
        if filters and self._has_unindexed_filters(filters):
            logger.warning(f"{NO_INDEXED_FILTERS} Node lookup returns no matches.")
            return []
        filter_query = await self._aget_filter_query(node_ids=node_ids, filters=filters)
        if filter_query is None:
            return []
        results = await self._async_index.query(filter_query)
        return self._process_query_results(results, filter_query).nodes or []

    def_delete_with_filter_query(self, filter_query: Optional[FilterQuery]) -> None:
"""Delete documents matching the provided filter query."""
        if filter_query is None:
            return

        docs_to_delete = self._index.search(filter_query.query, filter_query.params)
        with self._index.client.pipeline(transaction=False) as pipe:
            for doc in docs_to_delete.docs:
                pipe.delete(doc.id)
            pipe.execute()

        logger.info(
            f"Deleted {len(docs_to_delete.docs)} documents from index {self._index.name}"
        )

    async def_adelete_with_filter_query(
        self, filter_query: Optional[FilterQuery]
    ) -> None:
"""Asynchronously delete documents matching the provided filter query."""
        if filter_query is None:
            return

        docs_to_delete = await self._async_index.search(
            filter_query.query, filter_query.params
        )
        async with self._async_index.client.pipeline(transaction=False) as pipe:
            for doc in docs_to_delete.docs:
                await pipe.delete(doc.id)
            await pipe.execute()

        logger.info(
            f"Deleted {len(docs_to_delete.docs)} documents from index {self._async_index.name}"
        )

    defdelete_nodes(
        self,
        node_ids: Optional[list[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""Delete by node_ids or filters; unindexed filters are treated as a no-op."""
        if not node_ids and not filters:
            return
        if filters and self._has_unindexed_filters(filters):
            logger.warning(f"{NO_INDEXED_FILTERS} Delete operation is a no-op.")
            return

        filter_query = self._get_filter_query(node_ids=node_ids, filters=filters)
        self._delete_with_filter_query(filter_query)

    async defadelete_nodes(
        self,
        node_ids: Optional[list[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""Async delete by node_ids or filters; unindexed filters are treated as a no-op."""
        if not node_ids and not filters:
            return

        await self.async_index_exists()
        if filters and self._has_unindexed_filters(filters):
            logger.warning(f"{NO_INDEXED_FILTERS} Delete operation is a no-op.")
            return

        filter_query = await self._aget_filter_query(node_ids=node_ids, filters=filters)
        await self._adelete_with_filter_query(filter_query)

    async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using the ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        await self.async_index_exists()
        await self.adelete_nodes(
            filters=MetadataFilters(
                filters=[MetadataFilter(key=DOC_ID_FIELD_NAME, value=ref_doc_id)]
            )
        )

    defdelete(self, ref_doc_id: str) -> None:
"""
        Delete nodes using the ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        self.delete_nodes(
            filters=MetadataFilters(
                filters=[MetadataFilter(key=DOC_ID_FIELD_NAME, value=ref_doc_id)]
            )
        )

    defdelete_index(self) -> None:
"""Delete the index and all documents."""
        logger.info(f"Deleting index {self._index.name}")
        self._index.delete(drop=True)

    async defasync_delete_index(self) -> None:
"""Delete the index and all documents."""
        logger.info(f"Deleting index {self._async_index.name}")
        await self._async_index.delete(drop=True)

    @staticmethod
    def_to_redis_filter(field: BaseField, filter: MetadataFilter) -> FilterExpression:
"""
        Translate a standard metadata filter to a Redis specific filter expression.

        Args:
            field (BaseField): The field to be filtered on, must have a type attribute.
            filter (MetadataFilter): The filter to apply, must have operator and value attributes.

        Returns:
            FilterExpression: A Redis-specific filter expression constructed from the input.

        Raises:
            ValueError: If the field type is unsupported or if the operator is not supported for the field type.

        """
        # Check for unsupported field type
        if field.type not in REDIS_LLAMA_FIELD_SPEC:
            raise ValueError(f"Unsupported field type {field.type} for {field.name}")

        field_info = REDIS_LLAMA_FIELD_SPEC[field.type]

        # Check for unsupported operator
        if filter.operator not in field_info["operators"]:
            raise ValueError(
                f"Filter operator {filter.operator} not supported for {field.name} of type {field.type}"
            )

        # Create field instance and apply the operator function
        field_instance = field_info["class"](field.name)
        return field_info["operators"][filter.operator](field_instance, filter.value)

    def_create_redis_filter_expression(
        self, metadata_filters: MetadataFilters
    ) -> FilterExpression:
"""
        Build a Redis FilterExpression from metadata filters, combining nested filters recursively.

        Args:
            metadata_filters (MetadataFilters): Metadata filters to translate.

        Returns:
            FilterExpression: The translated Redis filter expression.

        """
        if not metadata_filters or not metadata_filters.filters:
            return FilterExpression("*")

        filter_expressions = []
        for filter in metadata_filters.filters:
            if isinstance(filter, MetadataFilters):
                filter_expressions.append(self._create_redis_filter_expression(filter))
                continue

            field = self._index.schema.fields.get(filter.key)
            if not field:
                logger.warning(
                    f"{filter.key} field was not included as part of the index schema, and thus cannot be used as a filter condition."
                )
                continue
            filter_expressions.append(self._to_redis_filter(field, filter))

        if not filter_expressions:
            return FilterExpression("*")

        filter_expression = filter_expressions[0]
        for redis_filter in filter_expressions[1:]:
            if metadata_filters.condition == "and":
                filter_expression = filter_expression  redis_filter
            else:
                filter_expression = filter_expression | redis_filter
        return filter_expression

    def_to_redis_filters(self, metadata_filters: MetadataFilters) -> str:
        tokenizer = TokenEscaper()

        filter_strings = []
        filter_in_strings = {}
        for filter in metadata_filters.legacy_filters():
            # adds quotes around the value to ensure that the filter is treated as an
            #   exact
            field = self._index.schema.fields.get(filter.key)
            if not field:
                logger.warning(
                    f"{filter.key} field was not included as part of the index schema, and thus cannot be used as a filter condition."
                )
                continue
            if filter.operator == FilterOperator.IN:
                if len(filter.value.split())  1:
                    filter.value = f'"{filter.value}"'
                if filter.key in filter_in_strings:
                    filter_in_strings[filter.key].append(filter.value)
                else:
                    filter_in_strings[filter.key] = [filter.value]
            else:
                filter_string = (
                    f"@{filter.key}:{{{tokenizer.escape(str(filter.value))}}}"
                )
                filter_strings.append(filter_string)
        for key, value_list in filter_in_strings.items():
            values = "|".join(value_list)
            filter_string = f"@{key}:{{{tokenizer.escape(str(values))}}}"
            filter_strings.append(filter_string)
        # A space can be used for the AND operator: https://redis.io/docs/latest/develop/interact/search-and-query/query/combined/
        filter_strings_base = [f"({filter_string})" for filter_string in filter_strings]
        joined_filter_strings = " ".join(filter_strings_base)
        return f"({joined_filter_strings})"

    def_build_filter_expression(
        self, filters: Optional[MetadataFilters]
    ) -> str | FilterExpression:
"""Return the filter expression respecting legacy flag."""
        if self.legacy_filters:
            return self._to_redis_filters(filters)
        return self._create_redis_filter_expression(filters)

    def_to_redis_query(self, query: VectorStoreQuery) -> VectorQuery:
"""Creates a RedisQuery from a VectorStoreQuery."""
        filter_expression = self._build_filter_expression(query.filters)
        return_fields = self._return_fields.copy()
        return VectorQuery(
            vector=query.query_embedding,
            vector_field_name=VECTOR_FIELD_NAME,
            num_results=query.similarity_top_k,
            filter_expression=filter_expression,
            return_fields=return_fields,
        )

    def_to_filter_query(self, query: VectorStoreQuery) -> FilterQuery:
"""Create a filter-only Redis query."""
        filter_expression = self._build_filter_expression(query.filters)
        return FilterQuery(
            filter_expression=filter_expression,
            return_fields=self._return_fields,
            num_results=query.similarity_top_k,
        )

    def_extract_node_and_score(self, doc, redis_query: Any):
"""Extract a node and (optional) score from a document."""
        try:
            node = metadata_dict_to_node(
                {NODE_CONTENT_FIELD_NAME: doc[NODE_CONTENT_FIELD_NAME]}
            )
            node.text = doc.get(TEXT_FIELD_NAME, node.get_content())
        except Exception:
            # Handle legacy metadata format
            node = TextNode(
                text=doc.get(TEXT_FIELD_NAME, ""),
                id_=doc.get(NODE_ID_FIELD_NAME),
                embedding=None,
                relationships={
                    NodeRelationship.SOURCE: RelatedNodeInfo(
                        node_id=doc.get(DOC_ID_FIELD_NAME)
                    )
                },
            )
        score = None
        if hasattr(redis_query, "DISTANCE_ID") and redis_query.DISTANCE_ID in doc:
            score = 1 - float(doc[redis_query.DISTANCE_ID])
        return node, score

    def_process_query_results(
        self, results, redis_query: VectorQuery
    ) -> VectorStoreQueryResult:
"""Processes query results and returns a VectorStoreQueryResult."""
        ids, nodes, scores = [], [], []
        for doc in results:
            node, score = self._extract_node_and_score(doc, redis_query)
            ids.append(doc.get(NODE_ID_FIELD_NAME))
            nodes.append(node)
            if score is not None:
                scores.append(score)
        logger.info(f"Found {len(nodes)} results for query with id {ids}")
        similarities = scores if scores else None
        return VectorStoreQueryResult(nodes=nodes, ids=ids, similarities=similarities)

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query the index.

        Args:
            query (VectorStoreQuery): query object

        Returns:
            VectorStoreQueryResult: query result

        Raises:
            ValueError: If query.query_embedding is None.
            redis.exceptions.RedisError: If there is an error querying the index.
            redis.exceptions.TimeoutError: If there is a timeout querying the index.

        """
        if query.query_embedding is None and not query.filters:
            raise ValueError(
                "Either query_embedding or metadata filters are required for querying."
            )

        if query.filters and self._has_unindexed_filters(query.filters):
            logger.warning(f"{NO_INDEXED_FILTERS} Query returns no matches.")
            return VectorStoreQueryResult(nodes=[], ids=[])

        if query.query_embedding is None:
            redis_query = self._to_filter_query(query)
        else:
            redis_query = self._to_redis_query(query)

        logger.info(f"Querying index {self._index.name} with query {redis_query!s}")

        try:
            results = self._index.query(redis_query)
        except RedisTimeoutError as e:
            logger.error(f"Query timed out on {self._index.name}: {e}")
            raise
        except RedisError as e:
            logger.error(f"Error querying {self._index.name}: {e}")
            raise

        return self._process_query_results(results, redis_query)

    async defaquery(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
"""
        Query the index.

        Args:
            query (VectorStoreQuery): query object

        Returns:
            VectorStoreQueryResult: query result

        Raises:
            ValueError: If query.query_embedding is None.
            redis.exceptions.RedisError: If there is an error querying the index.
            redis.exceptions.TimeoutError: If there is a timeout querying the index.

        """
        await self.async_index_exists()
        if query.query_embedding is None and not query.filters:
            raise ValueError(
                "Either query_embedding or metadata filters are required for querying."
            )

        if query.filters and self._has_unindexed_filters(query.filters):
            logger.warning(f"{NO_INDEXED_FILTERS} Query returns no matches.")
            return VectorStoreQueryResult(nodes=[], ids=[])

        if query.query_embedding is None:
            redis_query = self._to_filter_query(query)
        else:
            redis_query = self._to_redis_query(query)
        logger.info(f"Querying index {self._index.name} with query {redis_query!s}")
        try:
            results = await self._async_index.query(redis_query)
        except RedisTimeoutError as e:
            logger.error(f"Query timed out on {self._index.name}: {e}")
            raise
        except RedisError as e:
            logger.error(f"Error querying {self._index.name}: {e}")
            raise

        return self._process_query_results(results, redis_query)

    defpersist(
        self,
        persist_path: Optional[str] = None,
        fs: Optional[fsspec.AbstractFileSystem] = None,
        in_background: bool = True,
    ) -> None:
"""
        Persist the vector store to disk.

        For Redis, more notes here: https://redis.io/docs/management/persistence/

        Args:
            persist_path (str): Path to persist the vector store to. (doesn't apply)
            in_background (bool, optional): Persist in background. Defaults to True.
            fs (fsspec.AbstractFileSystem, optional): Filesystem to persist to.
                (doesn't apply)

        Raises:
            redis.exceptions.RedisError: If there is an error
                                         persisting the index to disk.

        """
        try:
            if in_background:
                logger.info("Saving index to disk in background")
                self._index.client.bgsave()
            else:
                logger.info("Saving index to disk")
                self._index.client.save()

        except RedisError as e:
            logger.error(f"Error saving index to disk: {e}")
            raise

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.client "Permanent link")

```
client: Redis

```

Return the redis client instance.
###  index_name `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.index_name "Permanent link")

```
index_name: 

```

Return the name of the index based on the schema.
###  schema `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.schema "Permanent link")

```
schema: IndexSchema

```

Return the index schema.
###  set_return_fields [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.set_return_fields "Permanent link")

```
set_return_fields(return_fields: []) -> None

```

Update the return fields for the query response.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
257
258
259
```
 | 
```
defset_return_fields(self, return_fields: List[str]) -> None:
"""Update the return fields for the query response."""
    self._return_fields = return_fields

```
 |  
| --- | --- |  
###  index_exists [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.index_exists "Permanent link")

```
index_exists() -> 

```

Check whether the index exists in Redis.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `bool`  |  `bool`  |  True or False.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
261
262
263
264
265
266
267
268
269
```
 | 
```
defindex_exists(self) -> bool:
"""
    Check whether the index exists in Redis.

    Returns:
        bool: True or False.

    """
    return self._index.exists()

```
 |  
| --- | --- |  
###  async_index_exists [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.async_index_exists "Permanent link")

```
async_index_exists() -> 

```

Check whether the index exists in Redis.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `bool`  |  `bool`  |  True or False.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
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
async defasync_index_exists(self) -> bool:
"""
    Check whether the index exists in Redis.

    Returns:
        bool: True or False.

    """
    if not self.created_async_index:
        await self.async_create_index()
    return True

```
 |  
| --- | --- |  
###  create_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.create_index "Permanent link")

```
create_index(overwrite: Optional[] = None) -> None

```

Create an index in Redis.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
283
284
285
286
287
288
289
290
291
```
 | 
```
defcreate_index(self, overwrite: Optional[bool] = None) -> None:
"""Create an index in Redis."""
    if overwrite is None:
        overwrite = self._overwrite
    # Create index honoring overwrite policy
    if overwrite:
        self._index.create(overwrite=overwrite, drop=True)
    else:
        self._index.create()

```
 |  
| --- | --- |  
###  async_create_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.async_create_index "Permanent link")

```
async_create_index(
    overwrite: Optional[] = None,
) -> None

```

Create an async index in Redis.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
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
```
 | 
```
async defasync_create_index(self, overwrite: Optional[bool] = None) -> None:
"""Create an async index in Redis."""
    if overwrite is None:
        overwrite = self._overwrite
    # Create index honoring overwrite policy
    if overwrite:
        await self._async_index.create(overwrite=True, drop=True)
    else:
        await self._async_index.create()
    self.created_async_index = True

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.async_add "Permanent link")

```
async_add(
    nodes: [], **add_kwargs: 
) -> []

```

Add nodes to the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes with embeddings  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: List of ids of the documents added to the index.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If the index already exists and overwrite is False.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
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
```
 | 
```
async defasync_add(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
    Add nodes to the index.

    Args:
        nodes (List[BaseNode]): List of nodes with embeddings

    Returns:
        List[str]: List of ids of the documents added to the index.

    Raises:
        ValueError: If the index already exists and overwrite is False.

    """
    # Check to see if empty document list was passed
    await self.async_index_exists()
    if len(nodes) == 0:
        return []

    # Now check for the scenario where user is trying to index embeddings that don't align with schema
    embedding_len = len(nodes[0].get_embedding())
    expected_dims = self._async_index.schema.fields[VECTOR_FIELD_NAME].attrs.dims
    if expected_dims != embedding_len:
        raise ValueError(
            f"Attempting to index embeddings of dim {embedding_len} "
            f"which doesn't match the index schema expectation of {expected_dims}. "
            "Please review the Redis integration example to learn how to customize schema. "
            ""
        )

    data: List[Dict[str, Any]] = []
    for node in nodes:
        embedding = node.get_embedding()
        record = {
            NODE_ID_FIELD_NAME: node.node_id,
            DOC_ID_FIELD_NAME: node.ref_doc_id,
            TEXT_FIELD_NAME: node.get_content(metadata_mode=MetadataMode.NONE),
            VECTOR_FIELD_NAME: array_to_buffer(embedding, dtype="FLOAT32"),
        }
        # parse and append metadata
        additional_metadata = node_to_metadata_dict(
            node, remove_text=True, flat_metadata=self.flat_metadata
        )
        data.append({**record, **additional_metadata})

    # Load nodes to Redis
    for mapping in data:
        mapping.pop(
            "sub_dicts", None
        )  # Remove if present from VectorMemory to avoid serialization issues
    keys = await self._async_index.load(
        data, id_field=NODE_ID_FIELD_NAME, **add_kwargs
    )
    logger.info(f"Added {len(keys)} documents to index {self._async_index.name}")
    return [
        key.strip(self._async_index.prefix + self._async_index.key_separator)
        for key in keys
    ]

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes with embeddings  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: List of ids of the documents added to the index.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If the index already exists and overwrite is False.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
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
```
 | 
```
defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
    Add nodes to the index.

    Args:
        nodes (List[BaseNode]): List of nodes with embeddings

    Returns:
        List[str]: List of ids of the documents added to the index.

    Raises:
        ValueError: If the index already exists and overwrite is False.

    """
    # Check to see if empty document list was passed
    if len(nodes) == 0:
        return []

    # Now check for the scenario where user is trying to index embeddings that don't align with schema
    embedding_len = len(nodes[0].get_embedding())
    expected_dims = self._index.schema.fields[VECTOR_FIELD_NAME].attrs.dims
    if expected_dims != embedding_len:
        raise ValueError(
            f"Attempting to index embeddings of dim {embedding_len} "
            f"which doesn't match the index schema expectation of {expected_dims}. "
            "Please review the Redis integration example to learn how to customize schema. "
            ""
        )

    data: List[Dict[str, Any]] = []
    for node in nodes:
        embedding = node.get_embedding()
        record = {
            NODE_ID_FIELD_NAME: node.node_id,
            DOC_ID_FIELD_NAME: node.ref_doc_id,
            TEXT_FIELD_NAME: node.get_content(metadata_mode=MetadataMode.NONE),
            VECTOR_FIELD_NAME: array_to_buffer(embedding, dtype="FLOAT32"),
        }
        # parse and append metadata
        additional_metadata = node_to_metadata_dict(
            node, remove_text=True, flat_metadata=self.flat_metadata
        )
        data.append({**record, **additional_metadata})

    # Load nodes to Redis
    keys = self._index.load(data, id_field=NODE_ID_FIELD_NAME, **add_kwargs)
    logger.info(f"Added {len(keys)} documents to index {self._index.name}")
    return [
        key.strip(self._index.prefix + self._index.key_separator) for key in keys
    ]

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Get nodes by node_ids or filters; at least one selector is required.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
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
defget_nodes(
    self,
    node_ids: Optional[list[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> list[BaseNode]:
"""Get nodes by node_ids or filters; at least one selector is required."""
    if not node_ids and not filters:
        raise ValueError("Either node_ids or filters must be provided.")
    if filters and self._has_unindexed_filters(filters):
        logger.warning(f"{NO_INDEXED_FILTERS} Node lookup returns no matches.")
        return []
    filter_query = self._get_filter_query(node_ids=node_ids, filters=filters)
    if filter_query is None:
        return []
    results = self._index.query(filter_query)
    return self._process_query_results(results, filter_query).nodes or []

```
 |  
| --- | --- |  
###  aget_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.aget_nodes "Permanent link")

```
aget_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Async get nodes by node_ids or filters; at least one selector is required.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
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
```
 | 
```
async defaget_nodes(
    self,
    node_ids: Optional[list[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> list[BaseNode]:
"""Async get nodes by node_ids or filters; at least one selector is required."""
    await self.async_index_exists()
    if not node_ids and not filters:
        raise ValueError("Either node_ids or filters must be provided.")
    if filters and self._has_unindexed_filters(filters):
        logger.warning(f"{NO_INDEXED_FILTERS} Node lookup returns no matches.")
        return []
    filter_query = await self._aget_filter_query(node_ids=node_ids, filters=filters)
    if filter_query is None:
        return []
    results = await self._async_index.query(filter_query)
    return self._process_query_results(results, filter_query).nodes or []

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Delete by node_ids or filters; unindexed filters are treated as a no-op.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
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
defdelete_nodes(
    self,
    node_ids: Optional[list[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""Delete by node_ids or filters; unindexed filters are treated as a no-op."""
    if not node_ids and not filters:
        return
    if filters and self._has_unindexed_filters(filters):
        logger.warning(f"{NO_INDEXED_FILTERS} Delete operation is a no-op.")
        return

    filter_query = self._get_filter_query(node_ids=node_ids, filters=filters)
    self._delete_with_filter_query(filter_query)

```
 |  
| --- | --- |  
###  adelete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.adelete_nodes "Permanent link")

```
adelete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Async delete by node_ids or filters; unindexed filters are treated as a no-op.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
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
```
 | 
```
async defadelete_nodes(
    self,
    node_ids: Optional[list[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""Async delete by node_ids or filters; unindexed filters are treated as a no-op."""
    if not node_ids and not filters:
        return

    await self.async_index_exists()
    if filters and self._has_unindexed_filters(filters):
        logger.warning(f"{NO_INDEXED_FILTERS} Delete operation is a no-op.")
        return

    filter_query = await self._aget_filter_query(node_ids=node_ids, filters=filters)
    await self._adelete_with_filter_query(filter_query)

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.adelete "Permanent link")

```
adelete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using the ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
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
```
 | 
```
async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using the ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    await self.async_index_exists()
    await self.adelete_nodes(
        filters=MetadataFilters(
            filters=[MetadataFilter(key=DOC_ID_FIELD_NAME, value=ref_doc_id)]
        )
    )

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.delete "Permanent link")

```
delete(ref_doc_id: ) -> None

```

Delete nodes using the ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str) -> None:
"""
    Delete nodes using the ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    self.delete_nodes(
        filters=MetadataFilters(
            filters=[MetadataFilter(key=DOC_ID_FIELD_NAME, value=ref_doc_id)]
        )
    )

```
 |  
| --- | --- |  
###  delete_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.delete_index "Permanent link")

```
delete_index() -> None

```

Delete the index and all documents.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
632
633
634
635
```
 | 
```
defdelete_index(self) -> None:
"""Delete the index and all documents."""
    logger.info(f"Deleting index {self._index.name}")
    self._index.delete(drop=True)

```
 |  
| --- | --- |  
###  async_delete_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.async_delete_index "Permanent link")

```
async_delete_index() -> None

```

Delete the index and all documents.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
637
638
639
640
```
 | 
```
async defasync_delete_index(self) -> None:
"""Delete the index and all documents."""
    logger.info(f"Deleting index {self._async_index.name}")
    await self._async_index.delete(drop=True)

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  query object  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  query result  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If query.query_embedding is None.  |  
|  `RedisError`  |  If there is an error querying the index.  |  
|  `TimeoutError`  |  If there is a timeout querying the index.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query the index.

    Args:
        query (VectorStoreQuery): query object

    Returns:
        VectorStoreQueryResult: query result

    Raises:
        ValueError: If query.query_embedding is None.
        redis.exceptions.RedisError: If there is an error querying the index.
        redis.exceptions.TimeoutError: If there is a timeout querying the index.

    """
    if query.query_embedding is None and not query.filters:
        raise ValueError(
            "Either query_embedding or metadata filters are required for querying."
        )

    if query.filters and self._has_unindexed_filters(query.filters):
        logger.warning(f"{NO_INDEXED_FILTERS} Query returns no matches.")
        return VectorStoreQueryResult(nodes=[], ids=[])

    if query.query_embedding is None:
        redis_query = self._to_filter_query(query)
    else:
        redis_query = self._to_redis_query(query)

    logger.info(f"Querying index {self._index.name} with query {redis_query!s}")

    try:
        results = self._index.query(redis_query)
    except RedisTimeoutError as e:
        logger.error(f"Query timed out on {self._index.name}: {e}")
        raise
    except RedisError as e:
        logger.error(f"Error querying {self._index.name}: {e}")
        raise

    return self._process_query_results(results, redis_query)

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.aquery "Permanent link")

```
aquery(
    query: , **kwargs: 
) -> 

```

Query the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  query object  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  query result  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If query.query_embedding is None.  |  
|  `RedisError`  |  If there is an error querying the index.  |  
|  `TimeoutError`  |  If there is a timeout querying the index.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
861
862
863
864
865
866
867
868
869
870
871
872
873
874
875
876
877
878
879
880
881
882
883
884
885
886
887
888
889
890
891
892
893
894
895
896
897
898
899
900
901
902
903
```
 | 
```
async defaquery(
    self, query: VectorStoreQuery, **kwargs: Any
) -> VectorStoreQueryResult:
"""
    Query the index.

    Args:
        query (VectorStoreQuery): query object

    Returns:
        VectorStoreQueryResult: query result

    Raises:
        ValueError: If query.query_embedding is None.
        redis.exceptions.RedisError: If there is an error querying the index.
        redis.exceptions.TimeoutError: If there is a timeout querying the index.

    """
    await self.async_index_exists()
    if query.query_embedding is None and not query.filters:
        raise ValueError(
            "Either query_embedding or metadata filters are required for querying."
        )

    if query.filters and self._has_unindexed_filters(query.filters):
        logger.warning(f"{NO_INDEXED_FILTERS} Query returns no matches.")
        return VectorStoreQueryResult(nodes=[], ids=[])

    if query.query_embedding is None:
        redis_query = self._to_filter_query(query)
    else:
        redis_query = self._to_redis_query(query)
    logger.info(f"Querying index {self._index.name} with query {redis_query!s}")
    try:
        results = await self._async_index.query(redis_query)
    except RedisTimeoutError as e:
        logger.error(f"Query timed out on {self._index.name}: {e}")
        raise
    except RedisError as e:
        logger.error(f"Error querying {self._index.name}: {e}")
        raise

    return self._process_query_results(results, redis_query)

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.RedisVectorStore.persist "Permanent link")

```
persist(
    persist_path: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
    in_background:  = True,
) -> None

```

Persist the vector store to disk.
For Redis, more notes here: https://redis.io/docs/management/persistence/
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `persist_path`  |  Path to persist the vector store to. (doesn't apply)  |  `None`  |  
|  `in_background`  |  `bool`  |  Persist in background. Defaults to True.  |  `True`  |  
|  `AbstractFileSystem`  |  Filesystem to persist to. (doesn't apply)  |  `None`  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `RedisError`  |  If there is an error persisting the index to disk.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
905
906
907
908
909
910
911
912
913
914
915
916
917
918
919
920
921
922
923
924
925
926
927
928
929
930
931
932
933
934
935
936
937
```
 | 
```
defpersist(
    self,
    persist_path: Optional[str] = None,
    fs: Optional[fsspec.AbstractFileSystem] = None,
    in_background: bool = True,
) -> None:
"""
    Persist the vector store to disk.

    For Redis, more notes here: https://redis.io/docs/management/persistence/

    Args:
        persist_path (str): Path to persist the vector store to. (doesn't apply)
        in_background (bool, optional): Persist in background. Defaults to True.
        fs (fsspec.AbstractFileSystem, optional): Filesystem to persist to.
            (doesn't apply)

    Raises:
        redis.exceptions.RedisError: If there is an error
                                     persisting the index to disk.

    """
    try:
        if in_background:
            logger.info("Saving index to disk in background")
            self._index.client.bgsave()
        else:
            logger.info("Saving index to disk")
            self._index.client.save()

    except RedisError as e:
        logger.error(f"Error saving index to disk: {e}")
        raise

```
 |  
| --- | --- |  
##  TokenEscaper [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/redis/#llama_index.vector_stores.redis.TokenEscaper "Permanent link")
Escape punctuation within an input string. Taken from RedisOM Python.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-redis/llama_index/vector_stores/redis/base.py`  
| 
```
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
```
 | 
```
classTokenEscaper:
"""
    Escape punctuation within an input string. Taken from RedisOM Python.
    """

    # Characters that RediSearch requires us to escape during queries.
    # Source: https://redis.io/docs/stack/search/reference/escaping/#the-rules-of-text-field-tokenization
    DEFAULT_ESCAPED_CHARS = r"[,.<>{}\[\]\\\"\':;!@#$%^&*()\-+=~\/ ]"

    def__init__(self, escape_chars_re: Optional[Pattern] = None):
        if escape_chars_re:
            self.escaped_chars_re = escape_chars_re
        else:
            self.escaped_chars_re = re.compile(self.DEFAULT_ESCAPED_CHARS)

    defescape(self, value: str) -> str:
        defescape_symbol(match: re.Match) -> str:
            value = match.group(0)
            return f"\\{value}"

        return self.escaped_chars_re.sub(escape_symbol, value)

```
 |  
| --- | --- |  
options: members: - RedisVectorStore
