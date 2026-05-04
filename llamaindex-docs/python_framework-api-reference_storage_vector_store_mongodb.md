# Mongodb
##  MongoDBAtlasVectorSearch [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch "Permanent link")
Bases: 
MongoDB Atlas Vector Store.
To use, you should have both: - the `pymongo` python package installed - a connection string associated with a MongoDB Atlas Cluster that has an Atlas Vector Search index
To get started head over to the [Atlas quick start](https://www.mongodb.com/docs/atlas/getting-started/).
Once your store is created, be sure to enable indexing in the Atlas GUI.
Please refer to the [documentation](https://www.mongodb.com/docs/atlas/atlas-vector-search/create-index/) to get more details on how to define an Atlas Vector Search index. You can name the index {ATLAS_VECTOR_SEARCH_INDEX_NAME} and create the index on the namespace {DB_NAME}.{COLLECTION_NAME}.
Finally, write the following definition in the JSON editor on MongoDB Atlas:

```
{
    "name": "vector_index",
    "type": "vectorSearch",
    "fields":[
        {
        "type": "vector",
        "path": "embedding",
        "numDimensions": 1536,
        "similarity": "cosine"
        }
    ]
}

```

Optionally, you can use the experimental convenience methods on this class to manage the vector search index and the full text index.
Examples:
`pip install llama-index-vector-stores-mongodb`

```
importpymongo
fromllama_index.vector_stores.mongodbimport MongoDBAtlasVectorSearch

# Ensure you have the MongoDB URI with appropriate credentials
mongo_uri = "mongodb+srv://<username>:<password>@<host>?retryWrites=true&w=majority"
mongodb_client = pymongo.MongoClient(mongo_uri)
async_mongodb_client = pymongo.AsyncMongoClient(mongo_uri)

# Create an instance of MongoDBAtlasVectorSearch
vector_store = MongoDBAtlasVectorSearch(
    mongodb_client=mongodb_client,
    async_mongodb_client=async_mongodb_client,
)

```


```
# Create a vector search index programmatically
vector_store.create_vector_search_index(path="embedding", dimensions=1536, similarity="cosine")

# Create a text search index programmatically
vector_store.create_fulltext_search_index("foo")

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mongodb/llama_index/vector_stores/mongodb/base.py`  
| 
```
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
```
 | 
```
classMongoDBAtlasVectorSearch(BasePydanticVectorStore):
"""
    MongoDB Atlas Vector Store.

    To use, you should have both:
    - the ``pymongo`` python package installed
    - a connection string associated with a MongoDB Atlas Cluster
    that has an Atlas Vector Search index

    To get started head over to the [Atlas quick start](https://www.mongodb.com/docs/atlas/getting-started/).

    Once your store is created, be sure to enable indexing in the Atlas GUI.

    Please refer to the [documentation](https://www.mongodb.com/docs/atlas/atlas-vector-search/create-index/)
    to get more details on how to define an Atlas Vector Search index. You can name the index {ATLAS_VECTOR_SEARCH_INDEX_NAME}
    and create the index on the namespace {DB_NAME}.{COLLECTION_NAME}.

    Finally, write the following definition in the JSON editor on MongoDB Atlas:

    ```

        "name": "vector_index",
        "type": "vectorSearch",
        "fields":[

            "type": "vector",
            "path": "embedding",
            "numDimensions": 1536,
            "similarity": "cosine"



    ```

    Optionally, you can use the experimental convenience methods on this class to manage the vector search
    index and the full text index.


    Examples:
        `pip install llama-index-vector-stores-mongodb`

        ```python
        import pymongo
        from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch

        # Ensure you have the MongoDB URI with appropriate credentials
        mongo_uri = "mongodb+srv://<username>:<password>@<host>?retryWrites=true&w=majority"
        mongodb_client = pymongo.MongoClient(mongo_uri)
        async_mongodb_client = pymongo.AsyncMongoClient(mongo_uri)

        # Create an instance of MongoDBAtlasVectorSearch
        vector_store = MongoDBAtlasVectorSearch(
            mongodb_client=mongodb_client,
            async_mongodb_client=async_mongodb_client,

        ```

        ```python
        # Create a vector search index programmatically
        vector_store.create_vector_search_index(path="embedding", dimensions=1536, similarity="cosine")

        # Create a text search index programmatically
        vector_store.create_fulltext_search_index("foo")
        ```

    """

    stores_text: bool = True
    flat_metadata: bool = False

    _mongodb_client: MongoClient = PrivateAttr(default=None)
    _async_mongodb_client: AsyncMongoClient = PrivateAttr(default=None)
    _collection: Collection = PrivateAttr(default=None)
    _async_collection: AsyncCollection = PrivateAttr(default=None)
    _db_name: str = PrivateAttr()
    _vector_index_name: str = PrivateAttr()
    _embedding_key: str = PrivateAttr()
    _id_key: str = PrivateAttr()
    _text_key: str = PrivateAttr()
    _metadata_key: str = PrivateAttr()
    _fulltext_index_name: str = PrivateAttr()
    _insert_kwargs: Dict = PrivateAttr()
    _index_name: str = PrivateAttr()  # DEPRECATED
    _oversampling_factor: int = PrivateAttr()
    _metadata_delete_index_name: str = PrivateAttr()
    _metadata_index_created: bool = PrivateAttr(default=False)

    def__init__(
        self,
        mongodb_client: Optional[MongoClient] = None,
        async_mongodb_client: Optional[AsyncMongoClient] = None,
        db_name: str = "default_db",
        collection_name: str = "default_collection",
        vector_index_name: str = "vector_index",
        id_key: str = "_id",
        embedding_key: str = "embedding",
        text_key: str = "text",
        metadata_key: str = "metadata",
        fulltext_index_name: str = "fulltext_index",
        metadata_delete_index_name: str = "metadata_delete_index",
        configure_at_start: bool = False,
        index_name: str = None,
        insert_kwargs: Optional[Dict] = None,
        oversampling_factor: int = 10,
        **kwargs: Any,
    ) -> None:
"""
        Initialize the vector store.

        Args:
            mongodb_client: A MongoDB client.
            async_mongodb_client: An Async MongoDB client.
            db_name: A MongoDB database name.
            collection_name: A MongoDB collection name.
            vector_index_name: A MongoDB Atlas *Vector* Search index name. ($vectorSearch)
            id_key: The data field to use as the id.
            embedding_key: A MongoDB field that will contain
            the embedding for each document.
            text_key: A MongoDB field that will contain the text for each document.
            metadata_key: A MongoDB field that will contain
            the metadata for each document.
            insert_kwargs: The kwargs used during `insert`.
            fulltext_index_name: A MongoDB Atlas *full-text* Search index name. ($search)
            metadata_delete_index_name: A MongoDB Atlas *metadata delete* index name.
            configure_at_start: If True, will attempt to create non-search indexes at initialization.
            oversampling_factor: This times n_results is 'ef' in the HNSW algorithm.
                'ef' determines the number of nearest neighbor candidates to consider during the search phase.
                A higher value leads to more accuracy, but is slower. Default = 10
            index_name: DEPRECATED: Please use vector_index_name.

        """
        super().__init__()

        if mongodb_client is not None:
            self._mongodb_client = cast(MongoClient, mongodb_client)
        else:
            if "MONGODB_URI" not in os.environ:
                raise ValueError(
                    "Must specify MONGODB_URI via env variable "
                    "if not directly passing in mongodb_client."
                )
            self._mongodb_client = MongoClient(
                os.environ["MONGODB_URI"],
                driver=DriverInfo(
                    name="llama-index", version=version("llama-index-core")
                ),
            )

        if async_mongodb_client is not None:
            self._async_mongodb_client = cast(AsyncMongoClient, async_mongodb_client)
        else:
            if "MONGODB_URI" not in os.environ:
                raise ValueError(
                    "Must specify MONGODB_URI via env variable "
                    "if not directly passing in async_mongodb_client."
                )
            self._async_mongodb_client = AsyncMongoClient(
                os.environ["MONGODB_URI"],
                driver=DriverInfo(
                    name="llama-index", version=version("llama-index-core")
                ),
            )

        if index_name is not None:
            logger.warning("index_name is deprecated. Please use vector_index_name")
            if vector_index_name is None:
                vector_index_name = index_name
            else:
                logger.warning(
                    "vector_index_name and index_name both specified. Will use vector_index_name"
                )

        self._db_name = db_name

        self._collection: Collection = self._mongodb_client[db_name][collection_name]
        self._async_collection: AsyncCollection = self._async_mongodb_client[db_name][
            collection_name
        ]

        self._vector_index_name = vector_index_name
        self._embedding_key = embedding_key
        self._id_key = id_key
        self._text_key = text_key
        self._metadata_key = metadata_key
        self._fulltext_index_name = fulltext_index_name
        self._insert_kwargs = insert_kwargs or {}
        self._oversampling_factor = oversampling_factor
        self._metadata_delete_index_name = metadata_delete_index_name
        self._metadata_index_created = False

        # Check if collection exists using a method that works with restricted permissions
        self._ensure_collection_exists(db_name, collection_name)

        if configure_at_start:
            # Create index for metadata deletion if it doesn't exist
            self._collection.create_index(
                [(f"{self._metadata_key}.ref_doc_id", 1)],
                name=self._metadata_delete_index_name,
            )
            self._metadata_index_created = True

    def_ensure_collection_exists(self, db_name: str, collection_name: str) -> None:
"""
        Ensure collection exists using permission-friendly methods.

        First tries listCollections, then falls back to a query-based check if that fails.

        Args:
            db_name: Database name
            collection_name: Collection name

        """
        db = self._mongodb_client[db_name]

        # Try the traditional listCollections method first
        try:
            if collection_name not in db.list_collection_names():
                db.create_collection(collection_name)
            return
        except Exception as e:
            logger.debug(f"listCollections failed: {e}. Using query-based approach.")

        # Fallback: Use find_one to test if we can access the collection
        # This works even with restricted permissions and doesn't require listCollections
        try:
            collection = db[collection_name]
            # This will succeed whether the collection exists or not
            # MongoDB creates collections lazily on first write operation
            collection.find_one({}, {"_id": 1})
            logger.debug(f"Collection '{collection_name}' accessible via query method")
        except Exception as e:
            logger.warning(
                f"Unable to verify collection '{collection_name}' access: {e}. "
                "Proceeding anyway - MongoDB will create collection on first write if needed."
            )

    def_create_data_to_insert(
        self, nodes: List[BaseNode]
    ) -> Tuple[List[str], List[dict]]:
        data_to_insert = []
        ids = []
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

        return ids, data_to_insert

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
        ids, data_to_insert = self._create_data_to_insert(nodes)

        logger.debug("Inserting data into MongoDB: %s", data_to_insert)
        insert_result = self._collection.insert_many(
            data_to_insert, **self._insert_kwargs
        )

        logger.debug("Result of insert: %s", insert_result)
        return ids

    async defasync_add(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
        Asynchronously add nodes to index.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        Returns:
            A List of ids for successfully added nodes.

        """
        ids, data_to_insert = self._create_data_to_insert(nodes)

        logger.debug("Inserting data into MongoDB: %s", data_to_insert)
        insert_result = await self._async_collection.insert_many(
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
        # Ensure filter has an appropriate index for performance
        # Create index on metadata.ref_doc_id if it doesn't exist
        if not self._metadata_index_created:
            self._collection.create_index(
                [(f"{self._metadata_key}.ref_doc_id", 1)],
                name=self._metadata_delete_index_name,
            )
            self._metadata_index_created = True

        # delete by filtering on the doc_id metadata
        self._collection.delete_many(
            filter={self._metadata_key + ".ref_doc_id": ref_doc_id}, **delete_kwargs
        )

    async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Asynchronously delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        # Ensure filter has an appropriate index for performance
        # Create index on metadata.ref_doc_id if it doesn't exist
        if not self._metadata_index_created:
            await self._async_collection.create_index(
                [(f"{self._metadata_key}.ref_doc_id", 1)],
                name=self._metadata_delete_index_name,
            )
            self._metadata_index_created = True

        # delete by filtering on the doc_id metadata
        await self._async_collection.delete_many(
            filter={self._metadata_key + ".ref_doc_id": ref_doc_id}, **delete_kwargs
        )

    @property
    defclient(self) -> MongoClient:
"""Return MongoDB client."""
        return self._mongodb_client

    @property
    defasync_client(self) -> AsyncMongoClient:
"""Return Async MongoDB client."""
        return self._async_mongodb_client

    @property
    defcollection(self) -> Collection:
"""Return pymongo Collection."""
        return self._collection

    @property
    defasync_collection(self) -> AsyncCollection:
"""Return pymongo AsyncCollection."""
        return self._async_collection

    def_create_query_pipeline(self, query: VectorStoreQuery) -> List[Dict]:
        hybrid_top_k = query.hybrid_top_k or query.similarity_top_k
        sparse_top_k = query.sparse_top_k or query.similarity_top_k
        dense_top_k = query.similarity_top_k

        if query.mode == VectorStoreQueryMode.DEFAULT:
            if not query.query_embedding:
                raise ValueError("query_embedding in VectorStoreQueryMode.DEFAULT")
            # Atlas Vector Search, potentially with filter
            logger.debug(f"Running {query.mode} mode query pipeline")
            filter = filters_to_mql(query.filters, metadata_key=self._metadata_key)
            pipeline = [
                vector_search_stage(
                    query_vector=query.query_embedding,
                    search_field=self._embedding_key,
                    index_name=self._vector_index_name,
                    limit=dense_top_k,
                    filter=filter,
                    oversampling_factor=self._oversampling_factor,
                ),
                {"$set": {"score": {"$meta": "vectorSearchScore"}}},
            ]

        elif query.mode == VectorStoreQueryMode.TEXT_SEARCH:
            # Atlas Full-Text Search, potentially with filter
            if not query.query_str:
                raise ValueError("query_str in VectorStoreQueryMode.TEXT_SEARCH ")
            logger.debug(f"Running {query.mode} mode query pipeline")
            filter = filters_to_mql(query.filters, metadata_key=self._metadata_key)
            pipeline = fulltext_search_stage(
                query=query.query_str,
                search_field=self._text_key,
                index_name=self._fulltext_index_name,
                operator="text",
                filter=filter,
                limit=sparse_top_k,
            )
            pipeline.append({"$set": {"score": {"$meta": "searchScore"}}})

        elif query.mode == VectorStoreQueryMode.HYBRID:
            # Combines Vector and Full-Text searches with Reciprocal Rank Fusion weighting
            logger.debug(f"Running {query.mode} mode query pipeline")
            scores_fields = ["vector_score", "fulltext_score"]
            filter = filters_to_mql(query.filters, metadata_key=self._metadata_key)
            pipeline = []
            # Vector Search pipeline
            if query.query_embedding:
                vector_pipeline = [
                    vector_search_stage(
                        query_vector=query.query_embedding,
                        search_field=self._embedding_key,
                        index_name=self._vector_index_name,
                        limit=dense_top_k,
                        filter=filter,
                        oversampling_factor=self._oversampling_factor,
                    )
                ]
                vector_pipeline.extend(reciprocal_rank_stage("vector_score"))
                combine_pipelines(pipeline, vector_pipeline, self._collection.name)

            # Full-Text Search pipeline
            if query.query_str:
                text_pipeline = fulltext_search_stage(
                    query=query.query_str,
                    search_field=self._text_key,
                    index_name=self._fulltext_index_name,
                    operator="text",
                    filter=filter,
                    limit=sparse_top_k,
                )
                text_pipeline.extend(reciprocal_rank_stage("fulltext_score"))
                combine_pipelines(pipeline, text_pipeline, self._collection.name)

            # Compute weighted sum and sort pipeline
            alpha = (
                query.alpha or 0.5
            )  # If no alpha is given, equal weighting is applied
            pipeline += final_hybrid_stage(
                scores_fields=scores_fields, limit=hybrid_top_k, alpha=alpha
            )

            # Remove embeddings unless requested.
            if (
                query.output_fields is None
                or self._embedding_key not in query.output_fields
            ):
                pipeline.append({"$project": {self._embedding_key: 0}})

        else:
            raise NotImplementedError(
                f"{VectorStoreQueryMode.DEFAULT} (vector), "
                f"{VectorStoreQueryMode.HYBRID} and {VectorStoreQueryMode.TEXT_SEARCH} "
                f"are available. {query.mode} is not."
            )

        return pipeline

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
r"""
        Query index for top k most similar nodes.

        The type of search to be performed is based on the VectorStoreQuery.mode.
        Choose from DEFAULT (vector), HYBRID (hybrid), or TEXT_SEARCH (full-text).
        When the mode is one of HYBRID or TEXT_SEARCH,
        VectorStoreQuery.query_str is used for the full-text search.
        See MongoDB Atlas documentation for full details on these.

        For details on VectorStoreQueryMode.DEFAULT == 'default',
        which does vector search, see:
            https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/

        For details on VectorStoreQueryMode.TEXT_SEARCH == "text_search",
        which performs full-text search, see:
            https://www.mongodb.com/docs/atlas/atlas-search/aggregation-stages/search/#mongodb-pipeline-pipe.-search

        For details on VectorStoreQueryMode.HYBRID == "hybrid",
        which combines the two with Reciprocal Rank Fusion, see the following.
            https://www.mongodb.com/docs/atlas/atlas-vector-search/tutorials/reciprocal-rank-fusion/

        In the scoring algorithm used, Reciprocal Rank Fusion,
            scores := \frac{1}{rank + penalty} with rank in [1,2,..,n]

        Args:
            query: a VectorStoreQuery object.

        Returns:
            A VectorStoreQueryResult containing the results of the query.

        """
        # Build aggregation pipeline
        pipeline = self._create_query_pipeline(query)

        # Execution
        logger.debug("Running query pipeline: %s", pipeline)
        cursor = self._collection.aggregate(pipeline)  # type: ignore

        # Post-processing
        top_k_nodes = []
        top_k_ids = []
        top_k_scores = []
        for res in cursor:
            text = res.pop(self._text_key)
            score = res.pop("score")
            id = res.pop(self._id_key)
            metadata_dict = res.pop(self._metadata_key)

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

    async defaquery(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
r"""
        Query index for top k most similar nodes.

        The type of search to be performed is based on the VectorStoreQuery.mode.
        Choose from DEFAULT (vector), HYBRID (hybrid), or TEXT_SEARCH (full-text).
        When the mode is one of HYBRID or TEXT_SEARCH,
        VectorStoreQuery.query_str is used for the full-text search.
        See MongoDB Atlas documentation for full details on these.

        For details on VectorStoreQueryMode.DEFAULT == 'default',
        which does vector search, see:
            https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/

        For details on VectorStoreQueryMode.TEXT_SEARCH == "text_search",
        which performs full-text search, see:
            https://www.mongodb.com/docs/atlas/atlas-search/aggregation-stages/search/#mongodb-pipeline-pipe.-search

        For details on VectorStoreQueryMode.HYBRID == "hybrid",
        which combines the two with Reciprocal Rank Fusion, see the following.
            https://www.mongodb.com/docs/atlas/atlas-vector-search/tutorials/reciprocal-rank-fusion/

        In the scoring algorithm used, Reciprocal Rank Fusion,
            scores := \frac{1}{rank + penalty} with rank in [1,2,..,n]

        Args:
            query: a VectorStoreQuery object.

        Returns:
            A VectorStoreQueryResult containing the results of the query.

        """
        # Build aggregation pipeline
        pipeline = self._create_query_pipeline(query)

        # Execution
        logger.debug("Running query pipeline: %s", pipeline)
        cursor = await self._async_collection.aggregate(pipeline)  # type: ignore

        # Post-processing
        top_k_nodes = []
        top_k_ids = []
        top_k_scores = []
        async for res in cursor:
            text = res.pop(self._text_key)
            score = res.pop("score")
            id = res.pop(self._id_key)
            metadata_dict = res.pop(self._metadata_key)

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

    defcreate_vector_search_index(
        self,
        dimensions: int,
        path: str,
        similarity: str,
        filters: Optional[List[str]] = None,
        *,
        wait_until_complete: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
"""
        Experimental Utility function to create the vector search index for this store.

        Args:
            dimensions (int): Number of dimensions in embedding
            path (str): field with vector embedding
            similarity (str): The similarity score used for the index
            filters (List[str]): Fields/paths to index to allow filtering in $vectorSearch
            wait_until_complete (Optional[float]): If provided, number of seconds to wait
                until search index is ready.
            kwargs: Keyword arguments supplying any additional options to SearchIndexModel.

        """
        return create_vector_search_index(
            self.collection,
            self._vector_index_name,
            dimensions,
            path,
            similarity,
            filters,
            wait_until_complete=wait_until_complete,
            **kwargs,
        )

    defdrop_vector_search_index(
        self,
        *,
        wait_until_complete: Optional[float] = None,
    ) -> None:
"""
        Drop the created vector search index for this store.

        Args:
            wait_until_complete (Optional[float]): If provided, number of seconds to wait
                until search index is ready.

        """
        return drop_vector_search_index(
            self.collection,
            self._vector_index_name,
            wait_until_complete=wait_until_complete,
        )

    defupdate_vector_search_index(
        self,
        dimensions: int,
        path: str,
        similarity: str,
        filters: Optional[List[str]] = None,
        *,
        wait_until_complete: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
"""
        Update the vector search index for this store.

        Replace the existing index definition with the provided definition.

        Args:
            dimensions (int): Number of dimensions in embedding
            path (str): field with vector embedding
            similarity (str): The similarity score used for the index.
            filters (List[str]): Fields/paths to index to allow filtering in $vectorSearch
            wait_until_complete (Optional[float]): If provided, number of seconds to wait
                until search index is ready.
            kwargs: Keyword arguments supplying any additional options to SearchIndexModel.

        """
        return update_vector_search_index(
            self.collection,
            self._vector_index_name,
            dimensions,
            path,
            similarity,
            filters,
            wait_until_complete=wait_until_complete,
            **kwargs,
        )

    defcreate_fulltext_search_index(
        self,
        field: str,
        field_type: str = "string",
        *,
        wait_until_complete: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
"""
        Experimental Utility function to create the Atlas Search index for this store.

        Args:
            field (str): Field to index
            wait_until_complete (Optional[float]): If provided, number of seconds to wait
                until search index is ready
            kwargs: Keyword arguments supplying any additional options to SearchIndexModel.

        """
        return create_fulltext_search_index(
            self.collection,
            self._fulltext_index_name,
            field,
            field_type,
            wait_until_complete=wait_until_complete,
            **kwargs,
        )

    async defacreate_vector_search_index(
        self,
        dimensions: int,
        path: str,
        similarity: str,
        filters: Optional[List[str]] = None,
        *,
        wait_until_complete: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
"""
        Experimental Utility function to create the vector search index for this store.

        Args:
            dimensions (int): Number of dimensions in embedding
            path (str): field with vector embedding
            similarity (str): The similarity score used for the index
            filters (List[str]): Fields/paths to index to allow filtering in $vectorSearch
            wait_until_complete (Optional[float]): If provided, number of seconds to wait
                until search index is ready.
            kwargs: Keyword arguments supplying any additional options to SearchIndexModel.

        """
        return await acreate_vector_search_index(
            self.async_collection,
            self._vector_index_name,
            dimensions,
            path,
            similarity,
            filters,
            wait_until_complete=wait_until_complete,
            **kwargs,
        )

    async defadrop_vector_search_index(
        self,
        *,
        wait_until_complete: Optional[float] = None,
    ) -> None:
"""
        Drop the created vector search index for this store.

        Args:
            wait_until_complete (Optional[float]): If provided, number of seconds to wait
                until search index is ready.

        """
        return await adrop_vector_search_index(
            self.async_collection,
            self._vector_index_name,
            wait_until_complete=wait_until_complete,
        )

    async defaupdate_vector_search_index(
        self,
        dimensions: int,
        path: str,
        similarity: str,
        filters: Optional[List[str]] = None,
        *,
        wait_until_complete: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
"""
        Update the vector search index for this store.

        Replace the existing index definition with the provided definition.

        Args:
            dimensions (int): Number of dimensions in embedding
            path (str): field with vector embedding
            similarity (str): The similarity score used for the index.
            filters (List[str]): Fields/paths to index to allow filtering in $vectorSearch
            wait_until_complete (Optional[float]): If provided, number of seconds to wait
                until search index is ready.
            kwargs: Keyword arguments supplying any additional options to SearchIndexModel.

        """
        return await aupdate_vector_search_index(
            self.async_collection,
            self._vector_index_name,
            dimensions,
            path,
            similarity,
            filters,
            wait_until_complete=wait_until_complete,
            **kwargs,
        )

    async defacreate_fulltext_search_index(
        self,
        field: str,
        field_type: str = "string",
        *,
        wait_until_complete: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
"""
        Experimental Utility function to create the Atlas Search index for this store.

        Args:
            field (str): Field to index
            wait_until_complete (Optional[float]): If provided, number of seconds to wait
                until search index is ready
            kwargs: Keyword arguments supplying any additional options to SearchIndexModel.

        """
        return await acreate_fulltext_search_index(
            self.async_collection,
            self._fulltext_index_name,
            field,
            field_type,
            wait_until_complete=wait_until_complete,
            **kwargs,
        )

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.client "Permanent link")

```
client: MongoClient

```

Return MongoDB client.
###  async_client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.async_client "Permanent link")

```
async_client: AsyncMongoClient

```

Return Async MongoDB client.
###  collection `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.collection "Permanent link")

```
collection: Collection

```

Return pymongo Collection.
###  async_collection `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.async_collection "Permanent link")

```
async_collection: AsyncCollection

```

Return pymongo AsyncCollection.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.add "Permanent link")

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
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mongodb/llama_index/vector_stores/mongodb/base.py`  
| 
```
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
    ids, data_to_insert = self._create_data_to_insert(nodes)

    logger.debug("Inserting data into MongoDB: %s", data_to_insert)
    insert_result = self._collection.insert_many(
        data_to_insert, **self._insert_kwargs
    )

    logger.debug("Result of insert: %s", insert_result)
    return ids

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.async_add "Permanent link")

```
async_add(
    nodes: [], **add_kwargs: 
) -> []

```

Asynchronously add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  A List of ids for successfully added nodes.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mongodb/llama_index/vector_stores/mongodb/base.py`  
| 
```
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
```
 | 
```
async defasync_add(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
    Asynchronously add nodes to index.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings

    Returns:
        A List of ids for successfully added nodes.

    """
    ids, data_to_insert = self._create_data_to_insert(nodes)

    logger.debug("Inserting data into MongoDB: %s", data_to_insert)
    insert_result = await self._async_collection.insert_many(
        data_to_insert, **self._insert_kwargs
    )

    logger.debug("Result of insert: %s", insert_result)
    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mongodb/llama_index/vector_stores/mongodb/base.py`  
| 
```
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
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    # Ensure filter has an appropriate index for performance
    # Create index on metadata.ref_doc_id if it doesn't exist
    if not self._metadata_index_created:
        self._collection.create_index(
            [(f"{self._metadata_key}.ref_doc_id", 1)],
            name=self._metadata_delete_index_name,
        )
        self._metadata_index_created = True

    # delete by filtering on the doc_id metadata
    self._collection.delete_many(
        filter={self._metadata_key + ".ref_doc_id": ref_doc_id}, **delete_kwargs
    )

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.adelete "Permanent link")

```
adelete(ref_doc_id: , **delete_kwargs: ) -> None

```

Asynchronously delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mongodb/llama_index/vector_stores/mongodb/base.py`  
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
393
394
395
396
397
```
 | 
```
async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Asynchronously delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    # Ensure filter has an appropriate index for performance
    # Create index on metadata.ref_doc_id if it doesn't exist
    if not self._metadata_index_created:
        await self._async_collection.create_index(
            [(f"{self._metadata_key}.ref_doc_id", 1)],
            name=self._metadata_delete_index_name,
        )
        self._metadata_index_created = True

    # delete by filtering on the doc_id metadata
    await self._async_collection.delete_many(
        filter={self._metadata_key + ".ref_doc_id": ref_doc_id}, **delete_kwargs
    )

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
The type of search to be performed is based on the VectorStoreQuery.mode. Choose from DEFAULT (vector), HYBRID (hybrid), or TEXT_SEARCH (full-text). When the mode is one of HYBRID or TEXT_SEARCH, VectorStoreQuery.query_str is used for the full-text search. See MongoDB Atlas documentation for full details on these.
For details on VectorStoreQueryMode.DEFAULT == 'default', which does vector search, see: https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/
For details on VectorStoreQueryMode.TEXT_SEARCH == "text_search", which performs full-text search, see: https://www.mongodb.com/docs/atlas/atlas-search/aggregation-stages/search/#mongodb-pipeline-pipe.-search
For details on VectorStoreQueryMode.HYBRID == "hybrid", which combines the two with Reciprocal Rank Fusion, see the following. https://www.mongodb.com/docs/atlas/atlas-vector-search/tutorials/reciprocal-rank-fusion/
In the scoring algorithm used, Reciprocal Rank Fusion, scores := \frac{1}{rank + penalty} with rank in [1,2,..,n]
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  a VectorStoreQuery object.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  A VectorStoreQueryResult containing the results of the query.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mongodb/llama_index/vector_stores/mongodb/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
r"""
    Query index for top k most similar nodes.

    The type of search to be performed is based on the VectorStoreQuery.mode.
    Choose from DEFAULT (vector), HYBRID (hybrid), or TEXT_SEARCH (full-text).
    When the mode is one of HYBRID or TEXT_SEARCH,
    VectorStoreQuery.query_str is used for the full-text search.
    See MongoDB Atlas documentation for full details on these.

    For details on VectorStoreQueryMode.DEFAULT == 'default',
    which does vector search, see:
        https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/

    For details on VectorStoreQueryMode.TEXT_SEARCH == "text_search",
    which performs full-text search, see:
        https://www.mongodb.com/docs/atlas/atlas-search/aggregation-stages/search/#mongodb-pipeline-pipe.-search

    For details on VectorStoreQueryMode.HYBRID == "hybrid",
    which combines the two with Reciprocal Rank Fusion, see the following.
        https://www.mongodb.com/docs/atlas/atlas-vector-search/tutorials/reciprocal-rank-fusion/

    In the scoring algorithm used, Reciprocal Rank Fusion,
        scores := \frac{1}{rank + penalty} with rank in [1,2,..,n]

    Args:
        query: a VectorStoreQuery object.

    Returns:
        A VectorStoreQueryResult containing the results of the query.

    """
    # Build aggregation pipeline
    pipeline = self._create_query_pipeline(query)

    # Execution
    logger.debug("Running query pipeline: %s", pipeline)
    cursor = self._collection.aggregate(pipeline)  # type: ignore

    # Post-processing
    top_k_nodes = []
    top_k_ids = []
    top_k_scores = []
    for res in cursor:
        text = res.pop(self._text_key)
        score = res.pop("score")
        id = res.pop(self._id_key)
        metadata_dict = res.pop(self._metadata_key)

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

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.aquery "Permanent link")

```
aquery(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
The type of search to be performed is based on the VectorStoreQuery.mode. Choose from DEFAULT (vector), HYBRID (hybrid), or TEXT_SEARCH (full-text). When the mode is one of HYBRID or TEXT_SEARCH, VectorStoreQuery.query_str is used for the full-text search. See MongoDB Atlas documentation for full details on these.
For details on VectorStoreQueryMode.DEFAULT == 'default', which does vector search, see: https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/
For details on VectorStoreQueryMode.TEXT_SEARCH == "text_search", which performs full-text search, see: https://www.mongodb.com/docs/atlas/atlas-search/aggregation-stages/search/#mongodb-pipeline-pipe.-search
For details on VectorStoreQueryMode.HYBRID == "hybrid", which combines the two with Reciprocal Rank Fusion, see the following. https://www.mongodb.com/docs/atlas/atlas-vector-search/tutorials/reciprocal-rank-fusion/
In the scoring algorithm used, Reciprocal Rank Fusion, scores := \frac{1}{rank + penalty} with rank in [1,2,..,n]
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  a VectorStoreQuery object.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  A VectorStoreQueryResult containing the results of the query.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mongodb/llama_index/vector_stores/mongodb/base.py`  
| 
```
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
```
 | 
```
async defaquery(
    self, query: VectorStoreQuery, **kwargs: Any
) -> VectorStoreQueryResult:
r"""
    Query index for top k most similar nodes.

    The type of search to be performed is based on the VectorStoreQuery.mode.
    Choose from DEFAULT (vector), HYBRID (hybrid), or TEXT_SEARCH (full-text).
    When the mode is one of HYBRID or TEXT_SEARCH,
    VectorStoreQuery.query_str is used for the full-text search.
    See MongoDB Atlas documentation for full details on these.

    For details on VectorStoreQueryMode.DEFAULT == 'default',
    which does vector search, see:
        https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/

    For details on VectorStoreQueryMode.TEXT_SEARCH == "text_search",
    which performs full-text search, see:
        https://www.mongodb.com/docs/atlas/atlas-search/aggregation-stages/search/#mongodb-pipeline-pipe.-search

    For details on VectorStoreQueryMode.HYBRID == "hybrid",
    which combines the two with Reciprocal Rank Fusion, see the following.
        https://www.mongodb.com/docs/atlas/atlas-vector-search/tutorials/reciprocal-rank-fusion/

    In the scoring algorithm used, Reciprocal Rank Fusion,
        scores := \frac{1}{rank + penalty} with rank in [1,2,..,n]

    Args:
        query: a VectorStoreQuery object.

    Returns:
        A VectorStoreQueryResult containing the results of the query.

    """
    # Build aggregation pipeline
    pipeline = self._create_query_pipeline(query)

    # Execution
    logger.debug("Running query pipeline: %s", pipeline)
    cursor = await self._async_collection.aggregate(pipeline)  # type: ignore

    # Post-processing
    top_k_nodes = []
    top_k_ids = []
    top_k_scores = []
    async for res in cursor:
        text = res.pop(self._text_key)
        score = res.pop("score")
        id = res.pop(self._id_key)
        metadata_dict = res.pop(self._metadata_key)

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

```
 |  
| --- | --- |  
###  create_vector_search_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.create_vector_search_index "Permanent link")

```
create_vector_search_index(
    dimensions: ,
    path: ,
    similarity: ,
    filters: Optional[[]] = None,
    *,
    wait_until_complete: Optional[float] = None,
    **kwargs: 
) -> None

```

Experimental Utility function to create the vector search index for this store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `dimensions`  |  Number of dimensions in embedding  |  _required_  |  
|  `path`  |  field with vector embedding  |  _required_  |  
|  `similarity`  |  The similarity score used for the index  |  _required_  |  
|  `filters`  |  `List[str]`  |  Fields/paths to index to allow filtering in $vectorSearch  |  `None`  |  
|  `wait_until_complete`  |  `Optional[float]`  |  If provided, number of seconds to wait until search index is ready.  |  `None`  |  
|  `kwargs`  |  Keyword arguments supplying any additional options to SearchIndexModel.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mongodb/llama_index/vector_stores/mongodb/base.py`  
| 
```
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
```
 | 
```
defcreate_vector_search_index(
    self,
    dimensions: int,
    path: str,
    similarity: str,
    filters: Optional[List[str]] = None,
    *,
    wait_until_complete: Optional[float] = None,
    **kwargs: Any,
) -> None:
"""
    Experimental Utility function to create the vector search index for this store.

    Args:
        dimensions (int): Number of dimensions in embedding
        path (str): field with vector embedding
        similarity (str): The similarity score used for the index
        filters (List[str]): Fields/paths to index to allow filtering in $vectorSearch
        wait_until_complete (Optional[float]): If provided, number of seconds to wait
            until search index is ready.
        kwargs: Keyword arguments supplying any additional options to SearchIndexModel.

    """
    return create_vector_search_index(
        self.collection,
        self._vector_index_name,
        dimensions,
        path,
        similarity,
        filters,
        wait_until_complete=wait_until_complete,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  drop_vector_search_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.drop_vector_search_index "Permanent link")

```
drop_vector_search_index(
    *, wait_until_complete: Optional[float] = None
) -> None

```

Drop the created vector search index for this store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `wait_until_complete`  |  `Optional[float]`  |  If provided, number of seconds to wait until search index is ready.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mongodb/llama_index/vector_stores/mongodb/base.py`  
| 
```
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
```
 | 
```
defdrop_vector_search_index(
    self,
    *,
    wait_until_complete: Optional[float] = None,
) -> None:
"""
    Drop the created vector search index for this store.

    Args:
        wait_until_complete (Optional[float]): If provided, number of seconds to wait
            until search index is ready.

    """
    return drop_vector_search_index(
        self.collection,
        self._vector_index_name,
        wait_until_complete=wait_until_complete,
    )

```
 |  
| --- | --- |  
###  update_vector_search_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.update_vector_search_index "Permanent link")

```
update_vector_search_index(
    dimensions: ,
    path: ,
    similarity: ,
    filters: Optional[[]] = None,
    *,
    wait_until_complete: Optional[float] = None,
    **kwargs: 
) -> None

```

Update the vector search index for this store.
Replace the existing index definition with the provided definition.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `dimensions`  |  Number of dimensions in embedding  |  _required_  |  
|  `path`  |  field with vector embedding  |  _required_  |  
|  `similarity`  |  The similarity score used for the index.  |  _required_  |  
|  `filters`  |  `List[str]`  |  Fields/paths to index to allow filtering in $vectorSearch  |  `None`  |  
|  `wait_until_complete`  |  `Optional[float]`  |  If provided, number of seconds to wait until search index is ready.  |  `None`  |  
|  `kwargs`  |  Keyword arguments supplying any additional options to SearchIndexModel.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mongodb/llama_index/vector_stores/mongodb/base.py`  
| 
```
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
```
 | 
```
defupdate_vector_search_index(
    self,
    dimensions: int,
    path: str,
    similarity: str,
    filters: Optional[List[str]] = None,
    *,
    wait_until_complete: Optional[float] = None,
    **kwargs: Any,
) -> None:
"""
    Update the vector search index for this store.

    Replace the existing index definition with the provided definition.

    Args:
        dimensions (int): Number of dimensions in embedding
        path (str): field with vector embedding
        similarity (str): The similarity score used for the index.
        filters (List[str]): Fields/paths to index to allow filtering in $vectorSearch
        wait_until_complete (Optional[float]): If provided, number of seconds to wait
            until search index is ready.
        kwargs: Keyword arguments supplying any additional options to SearchIndexModel.

    """
    return update_vector_search_index(
        self.collection,
        self._vector_index_name,
        dimensions,
        path,
        similarity,
        filters,
        wait_until_complete=wait_until_complete,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  create_fulltext_search_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.create_fulltext_search_index "Permanent link")

```
create_fulltext_search_index(
    field: ,
    field_type:  = "string",
    *,
    wait_until_complete: Optional[float] = None,
    **kwargs: 
) -> None

```

Experimental Utility function to create the Atlas Search index for this store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `field`  |  Field to index  |  _required_  |  
|  `wait_until_complete`  |  `Optional[float]`  |  If provided, number of seconds to wait until search index is ready  |  `None`  |  
|  `kwargs`  |  Keyword arguments supplying any additional options to SearchIndexModel.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mongodb/llama_index/vector_stores/mongodb/base.py`  
| 
```
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
```
 | 
```
defcreate_fulltext_search_index(
    self,
    field: str,
    field_type: str = "string",
    *,
    wait_until_complete: Optional[float] = None,
    **kwargs: Any,
) -> None:
"""
    Experimental Utility function to create the Atlas Search index for this store.

    Args:
        field (str): Field to index
        wait_until_complete (Optional[float]): If provided, number of seconds to wait
            until search index is ready
        kwargs: Keyword arguments supplying any additional options to SearchIndexModel.

    """
    return create_fulltext_search_index(
        self.collection,
        self._fulltext_index_name,
        field,
        field_type,
        wait_until_complete=wait_until_complete,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  acreate_vector_search_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.acreate_vector_search_index "Permanent link")

```
acreate_vector_search_index(
    dimensions: ,
    path: ,
    similarity: ,
    filters: Optional[[]] = None,
    *,
    wait_until_complete: Optional[float] = None,
    **kwargs: 
) -> None

```

Experimental Utility function to create the vector search index for this store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `dimensions`  |  Number of dimensions in embedding  |  _required_  |  
|  `path`  |  field with vector embedding  |  _required_  |  
|  `similarity`  |  The similarity score used for the index  |  _required_  |  
|  `filters`  |  `List[str]`  |  Fields/paths to index to allow filtering in $vectorSearch  |  `None`  |  
|  `wait_until_complete`  |  `Optional[float]`  |  If provided, number of seconds to wait until search index is ready.  |  `None`  |  
|  `kwargs`  |  Keyword arguments supplying any additional options to SearchIndexModel.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mongodb/llama_index/vector_stores/mongodb/base.py`  
| 
```
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
```
 | 
```
async defacreate_vector_search_index(
    self,
    dimensions: int,
    path: str,
    similarity: str,
    filters: Optional[List[str]] = None,
    *,
    wait_until_complete: Optional[float] = None,
    **kwargs: Any,
) -> None:
"""
    Experimental Utility function to create the vector search index for this store.

    Args:
        dimensions (int): Number of dimensions in embedding
        path (str): field with vector embedding
        similarity (str): The similarity score used for the index
        filters (List[str]): Fields/paths to index to allow filtering in $vectorSearch
        wait_until_complete (Optional[float]): If provided, number of seconds to wait
            until search index is ready.
        kwargs: Keyword arguments supplying any additional options to SearchIndexModel.

    """
    return await acreate_vector_search_index(
        self.async_collection,
        self._vector_index_name,
        dimensions,
        path,
        similarity,
        filters,
        wait_until_complete=wait_until_complete,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  adrop_vector_search_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.adrop_vector_search_index "Permanent link")

```
adrop_vector_search_index(
    *, wait_until_complete: Optional[float] = None
) -> None

```

Drop the created vector search index for this store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `wait_until_complete`  |  `Optional[float]`  |  If provided, number of seconds to wait until search index is ready.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mongodb/llama_index/vector_stores/mongodb/base.py`  
| 
```
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
```
 | 
```
async defadrop_vector_search_index(
    self,
    *,
    wait_until_complete: Optional[float] = None,
) -> None:
"""
    Drop the created vector search index for this store.

    Args:
        wait_until_complete (Optional[float]): If provided, number of seconds to wait
            until search index is ready.

    """
    return await adrop_vector_search_index(
        self.async_collection,
        self._vector_index_name,
        wait_until_complete=wait_until_complete,
    )

```
 |  
| --- | --- |  
###  aupdate_vector_search_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.aupdate_vector_search_index "Permanent link")

```
aupdate_vector_search_index(
    dimensions: ,
    path: ,
    similarity: ,
    filters: Optional[[]] = None,
    *,
    wait_until_complete: Optional[float] = None,
    **kwargs: 
) -> None

```

Update the vector search index for this store.
Replace the existing index definition with the provided definition.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `dimensions`  |  Number of dimensions in embedding  |  _required_  |  
|  `path`  |  field with vector embedding  |  _required_  |  
|  `similarity`  |  The similarity score used for the index.  |  _required_  |  
|  `filters`  |  `List[str]`  |  Fields/paths to index to allow filtering in $vectorSearch  |  `None`  |  
|  `wait_until_complete`  |  `Optional[float]`  |  If provided, number of seconds to wait until search index is ready.  |  `None`  |  
|  `kwargs`  |  Keyword arguments supplying any additional options to SearchIndexModel.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mongodb/llama_index/vector_stores/mongodb/base.py`  
| 
```
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
```
 | 
```
async defaupdate_vector_search_index(
    self,
    dimensions: int,
    path: str,
    similarity: str,
    filters: Optional[List[str]] = None,
    *,
    wait_until_complete: Optional[float] = None,
    **kwargs: Any,
) -> None:
"""
    Update the vector search index for this store.

    Replace the existing index definition with the provided definition.

    Args:
        dimensions (int): Number of dimensions in embedding
        path (str): field with vector embedding
        similarity (str): The similarity score used for the index.
        filters (List[str]): Fields/paths to index to allow filtering in $vectorSearch
        wait_until_complete (Optional[float]): If provided, number of seconds to wait
            until search index is ready.
        kwargs: Keyword arguments supplying any additional options to SearchIndexModel.

    """
    return await aupdate_vector_search_index(
        self.async_collection,
        self._vector_index_name,
        dimensions,
        path,
        similarity,
        filters,
        wait_until_complete=wait_until_complete,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  acreate_fulltext_search_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/mongodb/#llama_index.vector_stores.mongodb.MongoDBAtlasVectorSearch.acreate_fulltext_search_index "Permanent link")

```
acreate_fulltext_search_index(
    field: ,
    field_type:  = "string",
    *,
    wait_until_complete: Optional[float] = None,
    **kwargs: 
) -> None

```

Experimental Utility function to create the Atlas Search index for this store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `field`  |  Field to index  |  _required_  |  
|  `wait_until_complete`  |  `Optional[float]`  |  If provided, number of seconds to wait until search index is ready  |  `None`  |  
|  `kwargs`  |  Keyword arguments supplying any additional options to SearchIndexModel.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-mongodb/llama_index/vector_stores/mongodb/base.py`  
| 
```
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
```
 | 
```
async defacreate_fulltext_search_index(
    self,
    field: str,
    field_type: str = "string",
    *,
    wait_until_complete: Optional[float] = None,
    **kwargs: Any,
) -> None:
"""
    Experimental Utility function to create the Atlas Search index for this store.

    Args:
        field (str): Field to index
        wait_until_complete (Optional[float]): If provided, number of seconds to wait
            until search index is ready
        kwargs: Keyword arguments supplying any additional options to SearchIndexModel.

    """
    return await acreate_fulltext_search_index(
        self.async_collection,
        self._fulltext_index_name,
        field,
        field_type,
        wait_until_complete=wait_until_complete,
        **kwargs,
    )

```
 |  
| --- | --- |  
options: members: - MongoDBAtlasVectorSearch
