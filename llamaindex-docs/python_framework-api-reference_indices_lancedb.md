# Lancedb
##  LanceDBMultiModalIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/lancedb/#llama_index.indices.managed.lancedb.LanceDBMultiModalIndex "Permanent link")
Bases: `BaseManagedIndex`
Implementation of the MultiModal AI LakeHouse by LanceDB.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-lancedb/llama_index/indices/managed/lancedb/base.py`  
| 
```
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
```
 | 
```
classLanceDBMultiModalIndex(BaseManagedIndex):
"""
    Implementation of the MultiModal AI LakeHouse by LanceDB.
    """

    classConfig:
        arbitrary_types_allowed = True

    connection_config: Union[LocalConnectionConfig, CloudConnectionConfig]
    embedding_config: EmbeddingConfig
    indexing_config: IndexingConfig
    table_config: TableConfig

    _embedding_model: Optional[Union[LanceDBMultiModalModel, LanceDBTextModel]] = None
    _table_schema: Optional[Union[LanceModel, pa.Schema]] = None
    _connection: Optional[Union[DBConnection, AsyncConnection]] = None
    _table: Optional[Union[Table, AsyncTable]] = None
    _reranker: Optional[Reranker] = None

    def__init__(
        self,
        connection: Optional[Union[DBConnection, AsyncConnection]] = None,
        uri: Optional[str] = None,
        region: Optional[str] = None,
        api_key: Optional[str] = None,
        text_embedding_model: Optional[
            Literal[
                "bedrock-text",
                "cohere",
                "gemini-text",
                "instructor",
                "ollama",
                "openai",
                "sentence-transformers",
                "gte-text",
                "huggingface",
                "colbert",
                "jina",
                "watsonx",
                "voyageai",
            ]
        ] = None,
        multimodal_embedding_model: Optional[
            Literal["open-clip", "colpali", "jina", "imagebind"]
        ] = None,
        embedding_model_kwargs: Dict[str, Any] = None,
        table_name: str = DEFAULT_TABLE_NAME,
        indexing: Literal[
            "IVF_PQ",
            "IVF_HNSW_PQ",
            "IVF_HNSW_SQ",
            "FTS",
            "BTREE",
            "BITMAP",
            "LABEL_LIST",
            "NO_INDEXING",
        ] = "IVF_PQ",
        indexing_kwargs: Dict[str, Any] = None,
        reranker: Optional[Reranker] = None,
        use_async: bool = False,
        table_exists: bool = False,
    ) -> None:
        if embedding_model_kwargs is None:
            embedding_model_kwargs = {}
        if indexing_kwargs is None:
            indexing_kwargs = {}
        self._reranker = reranker
        if connection:
            assert isinstance(connection, (DBConnection, AsyncConnection)), (
                "You did not provide a valid LanceDB connection"
            )
            if use_async:
                assert isinstance(connection, AsyncConnection), (
                    "You set use_async to True, but you provided a synchronous connection"
                )
            else:
                assert isinstance(connection, DBConnection), (
                    "You set use_async to False, but you provided an asynchronous connection"
                )
            self._connection = connection
        elif uri and uri.startswith("db://"):
            self.connection_config = CloudConnectionConfig(
                uri=uri,
                api_key=api_key,
                region=region,
                use_async=use_async,
            )
        elif uri and not uri.startswith("db://"):
            self.connection_config = LocalConnectionConfig(
                uri=uri,
                use_async=use_async,
            )
        else:
            raise ValueError(
                "No connection has been passed and no URI has been set for local or remote connection"
            )
        self.embedding_config = EmbeddingConfig(
            text_embedding_model=text_embedding_model,
            multi_modal_embedding_model=multimodal_embedding_model,
            embedding_kwargs=embedding_model_kwargs,
        )
        self.indexing_config = IndexingConfig(
            indexing=indexing, indexing_kwargs=indexing_kwargs
        )
        self.table_config = TableConfig(
            table_name=table_name,
            table_exists=table_exists,
        )

    defcreate_index(self) -> None:
        if self._connection:
            return
        if self.connection_config.use_async:
            raise ValueError(
                "You are trying to establish a synchronous connection when use_async is set to True"
            )
        if isinstance(self.connection_config, LocalConnectionConfig):
            self._connection = lancedb.connect(uri=self.connection_config.uri)
        else:
            self._connection = lancedb.connect(
                uri=self.connection_config.uri,
                region=self.connection_config.region,
                api_key=self.connection_config.api_key,
            )

        self._connection = cast(DBConnection, self._connection)

        if self.embedding_config.text_embedding_model:
            self._embedding_model = get_lancedb_text_embedding_model(
                embedding_model=self.embedding_config.text_embedding_model,
                **self.embedding_config.embedding_kwargs,
            )

            classTextSchema(LanceModel):
                id: str
                metadata: str = Field(default=json.dumps({}))
                text: str = self._embedding_model.embedding_modxel.SourceField()
                vector: Vector(self._embedding_model.embedding_model.ndims()) = (
                    self._embedding_model.embedding_model.VectorField()
                )

            self._table_schema = TextSchema
        else:
            self._embedding_model = get_lancedb_multimodal_embedding_model(
                embedding_model=self.embedding_config.multi_modal_embedding_model,
                **self.embedding_config.embedding_kwargs,
            )

            classMultiModalSchema(LanceModel):
                id: str
                metadata: str = Field(default=json.dumps({}))
                label: str = Field(
                    default_factory=str,
                )
                image_uri: str = (
                    self._embedding_model.embedding_model.SourceField()
                )  # image uri as the source
                image_bytes: bytes = (
                    self._embedding_model.embedding_model.SourceField()
                )  # image bytes as the source
                vector: Vector(self._embedding_model.embedding_model.ndims()) = (
                    self._embedding_model.embedding_model.VectorField()
                )  # vector column
                vec_from_bytes: Vector(
                    self._embedding_model.embedding_model.ndims()
                ) = self._embedding_model.embedding_model.VectorField()  # Another vector column

            self._table_schema = MultiModalSchema

        if not self.table_config.table_exists:
            self._table = self._connection.create_table(
                self.table_config.table_name, schema=self._table_schema
            )
            if self.indexing_config.indexing != "NO_INDEXING":
                self._table.create_index(
                    index_type=self.indexing_config.indexing,
                    **self.indexing_config.indexing_kwargs,
                )
        else:
            self._table = self._connection.open_table(self.table_config.table_name)
            self._table_schema = self._table.schema

    async defacreate_index(self) -> None:
        if self._connection:
            return
        if not self.connection_config.use_async:
            raise ValueError(
                "You are trying to establish an asynchronous connection when use_async is set to False"
            )
        if isinstance(self.connection_config, LocalConnectionConfig):
            self._connection = await lancedb.connect_async(
                uri=self.connection_config.uri
            )
        else:
            self._connection = await lancedb.connect_async(
                uri=self.connection_config.uri,
                region=self.connection_config.region,
                api_key=self.connection_config.api_key,
            )
        self._connection = cast(AsyncConnection, self._connection)
        if self.embedding_config.text_embedding_model:
            self._embedding_model = get_lancedb_text_embedding_model(
                embedding_model=self.embedding_config.text_embedding_model,
                **self.embedding_config.embedding_kwargs,
            )

            classTextSchema(LanceModel):
                id: str
                metadata: str = Field(default=json.dumps({}))
                text: str = self._embedding_model.embedding_model.SourceField()
                vector: Vector(self._embedding_model.embedding_model.ndims()) = (
                    self._embedding_model.embedding_model.VectorField()
                )

            self._table_schema = TextSchema
        else:
            self._embedding_model = get_lancedb_multimodal_embedding_model(
                embedding_model=self.embedding_config.multi_modal_embedding_model,
                **self.embedding_config.embedding_kwargs,
            )
            self._embedding_model.validate_embedding_model()

            classMultiModalSchema(LanceModel):
                id: str
                metadata: str = Field(default=json.dumps({}))
                label: str = Field(
                    default_factory=str,
                )
                image_uri: str = (
                    self._embedding_model.embedding_model.SourceField()
                )  # image uri as the source
                image_bytes: bytes = (
                    self._embedding_model.embedding_model.SourceField()
                )  # image bytes as the source
                vector: Vector(self._embedding_model.embedding_model.ndims()) = (
                    self._embedding_model.embedding_model.VectorField()
                )  # vector column
                vec_from_bytes: Vector(
                    self._embedding_model.embedding_model.ndims()
                ) = self._embedding_model.embedding_model.VectorField()  # Another vector column

            self._table_schema = MultiModalSchema

        if not self.table_config.table_exists:
            self._table = await self._connection.create_table(
                self.table_config.table_name, schema=self._table_schema
            )
            if self.indexing_config.indexing != "NO_INDEXING":
                await self._table.create_index(
                    config=self.indexing_config.async_index_config,
                    column="vector",
                    **self.indexing_config.indexing_kwargs,
                )
        else:
            self._table = await self._connection.open_table(
                self.table_config.table_name
            )
            self._table_schema = await self._table.schema()

    @classmethod
    async deffrom_documents(
        cls,
        documents: Sequence[Union[Document, ImageDocument]],
        connection: Optional[DBConnection] = None,
        uri: Optional[str] = None,
        region: Optional[str] = None,
        api_key: Optional[str] = None,
        text_embedding_model: Optional[
            Literal[
                "bedrock-text",
                "cohere",
                "gemini-text",
                "instructor",
                "ollama",
                "openai",
                "sentence-transformers",
                "gte-text",
                "huggingface",
                "colbert",
                "jina",
                "watsonx",
                "voyageai",
            ]
        ] = None,
        multimodal_embedding_model: Optional[
            Literal["open-clip", "colpali", "jina", "imagebind"]
        ] = None,
        embedding_model_kwargs: Dict[str, Any] = None,
        table_name: str = DEFAULT_TABLE_NAME,
        indexing: Literal[
            "IVF_PQ",
            "IVF_HNSW_PQ",
            "IVF_HNSW_SQ",
            "FTS",
            "BTREE",
            "BITMAP",
            "LABEL_LIST",
            "NO_INDEXING",
        ] = "IVF_PQ",
        indexing_kwargs: Dict[str, Any] = None,
        reranker: Optional[Reranker] = None,
        use_async: bool = False,
        table_exists: bool = False,
    ) -> "LanceDBMultiModalIndex":
"""
        Generate a LanceDBMultiModalIndex from LlamaIndex Documents.
        """
        if embedding_model_kwargs is None:
            embedding_model_kwargs = {}
        if indexing_kwargs is None:
            indexing_kwargs = {}
        try:
            index = cls(
                connection,
                uri,
                region,
                api_key,
                text_embedding_model,
                multimodal_embedding_model,
                embedding_model_kwargs,
                table_name,
                indexing,
                indexing_kwargs,
                reranker,
                use_async,
                table_exists,
            )
        except ValueError as e:
            raise ValueError(
                f"Initialization of the index from documents are failed: {e}"
            )
        if use_async:
            await index.acreate_index()
        else:
            index.create_index()
        data: List[dict] = []
        if text_embedding_model:
            assert all(isinstance(document, Document) for document in documents)
            for document in documents:
                if document.text:
                    data.append(
                        {
                            "id": document.id_,
                            "text": document.text,
                            "metadata": json.dumps(document.metadata),
                        }
                    )
                else:
                    warnings.warn(
                        f"Document {document.doc_id} does not contain text and has thus been skipped",
                        UserWarning,
                    )
        else:
            assert all(isinstance(document, ImageDocument) for document in documents)
            for document in documents:
                label = json.dumps(document.metadata).get("image_label", None) or ""
                if document.image:
                    data.append(
                        {
                            "id": document.id_,
                            "image_bytes": document.image,
                            "image_uri": document.image_url or "",
                            "label": label,
                            "metadata": json.dumps(document.metadata),
                        }
                    )
                elif document.image_url:
                    image_bytes = httpx.get(document.image_url).content
                    data.append(
                        {
                            "id": document.id_,
                            "image_bytes": image_bytes,
                            "image_uri": document.image_url,
                            "label": label,
                            "metadata": json.dumps(document.metadata),
                        }
                    )
                elif document.image_path:
                    image_bytes = document.resolve_image().read()
                    data.append(
                        {
                            "id": document.id_,
                            "image_bytes": image_bytes,
                            "image_uri": document.image_url or "",
                            "label": label,
                            "metadata": json.dumps(document.metadata),
                        }
                    )
                else:
                    warnings.warn(
                        f"Document {document.doc_id} does not contain an image and has thus been skipped",
                        UserWarning,
                    )
        if use_async:
            await index._table.add(data)
        else:
            index._table.add(data)
        return index

    @classmethod
    async deffrom_data(
        cls,
        data: Union[List[dict], pa.Table, pl.DataFrame, pd.DataFrame],
        connection: Optional[DBConnection] = None,
        uri: Optional[str] = None,
        region: Optional[str] = None,
        api_key: Optional[str] = None,
        text_embedding_model: Optional[
            Literal[
                "bedrock-text",
                "cohere",
                "gemini-text",
                "instructor",
                "ollama",
                "openai",
                "sentence-transformers",
                "gte-text",
                "huggingface",
                "colbert",
                "jina",
                "watsonx",
                "voyageai",
            ]
        ] = None,
        multimodal_embedding_model: Optional[
            Literal["open-clip", "colpali", "jina", "imagebind"]
        ] = None,
        embedding_model_kwargs: Dict[str, Any] = {},
        table_name: str = DEFAULT_TABLE_NAME,
        indexing: Literal[
            "IVF_PQ",
            "IVF_HNSW_PQ",
            "IVF_HNSW_SQ",
            "FTS",
            "BTREE",
            "BITMAP",
            "LABEL_LIST",
            "NO_INDEXING",
        ] = "IVF_PQ",
        indexing_kwargs: Dict[str, Any] = {},
        reranker: Optional[Reranker] = None,
        use_async: bool = False,
        table_exists: bool = False,
    ) -> "LanceDBMultiModalIndex":
"""
        Generate a LanceDBMultiModalIndex from Pandas, Polars or PyArrow data.
        """
        try:
            index = cls(
                connection,
                uri,
                region,
                api_key,
                text_embedding_model,
                multimodal_embedding_model,
                embedding_model_kwargs,
                table_name,
                indexing,
                indexing_kwargs,
                reranker,
                use_async,
                table_exists,
            )
        except ValueError as e:
            raise ValueError(
                f"Initialization of the vector store from documents are failed: {e}"
            )
        if use_async:
            await index.acreate_index()
            await index._table.add(data)
        else:
            index.create_index()
            index._table.add(data)

        return index

    defas_retriever(self, **kwargs):
        if self.embedding_config.text_embedding_model:
            multimodal = False
        else:
            multimodal = True
        return LanceDBRetriever(
            table=self._table,
            multimodal=multimodal,
            **kwargs,
        )

    defas_query_engine(self, **kwargs):
        retriever = self.as_retriever()
        return LanceDBRetrieverQueryEngine(retriever=retriever, **kwargs)

    async defainsert_nodes(
        self, documents: Sequence[Union[Document, ImageDocument]], **kwargs: Any
    ) -> None:
        data: List[dict] = []
        if isinstance(self._embedding_model, LanceDBTextModel):
            assert all(isinstance(document, Document) for document in documents)
            for document in documents:
                if document.text:
                    data.append(
                        {
                            "id": document.id_,
                            "text": document.text,
                            "metadata": json.dumps(document.metadata),
                        }
                    )
                else:
                    warnings.warn(
                        f"Document {document.doc_id} does not contain text and has thus been skipped",
                        UserWarning,
                    )
        else:
            assert all(isinstance(document, ImageDocument) for document in documents)
            for document in documents:
                label = json.dumps(document.metadata).get("image_label", None) or ""
                if document.image:
                    data.append(
                        {
                            "id": document.id_,
                            "image_bytes": document.image,
                            "image_uri": document.image_url or "",
                            "label": label,
                            "metadata": json.dumps(document.metadata),
                        }
                    )
                elif document.image_url:
                    image_bytes = httpx.get(document.image_url).content
                    data.append(
                        {
                            "id": document.id_,
                            "image_bytes": image_bytes,
                            "image_uri": document.image_url,
                            "label": label,
                            "metadata": json.dumps(document.metadata),
                        }
                    )
                elif document.image_path:
                    image_bytes = document.resolve_image().read()
                    data.append(
                        {
                            "id": document.id_,
                            "image_bytes": image_bytes,
                            "image_uri": document.image_url or "",
                            "label": label,
                            "metadata": json.dumps(document.metadata),
                        }
                    )
                else:
                    warnings.warn(
                        f"Document {document.doc_id} does not contain an image and has thus been skipped",
                        UserWarning,
                    )

        if self.connection_config.use_async:
            self._table = cast(AsyncTable, self._table)
            await self._table.add(data)
        else:
            raise ValueError(
                "Attempting to add documents asynchronously with a synchronous connection!"
            )

    definsert_nodes(
        self, documents: Sequence[Union[Document, ImageDocument]], **kwargs: Any
    ) -> None:
        data: List[dict] = []
        if isinstance(self._embedding_model, LanceDBTextModel):
            assert all(isinstance(document, Document) for document in documents)
            for document in documents:
                if document.text:
                    data.append(
                        {
                            "id": document.id_,
                            "text": document.text,
                            "metadata": json.dumps(document.metadata),
                        }
                    )
                else:
                    warnings.warn(
                        f"Document {document.doc_id} does not contain text and has thus been skipped",
                        UserWarning,
                    )
        else:
            assert all(isinstance(document, ImageDocument) for document in documents)
            for document in documents:
                label = json.dumps(document.metadata).get("image_label", None) or ""
                if document.image:
                    data.append(
                        {
                            "id": document.id_,
                            "image_bytes": document.image,
                            "image_uri": document.image_url or "",
                            "label": label,
                            "metadata": json.dumps(document.metadata),
                        }
                    )
                elif document.image_url:
                    image_bytes = httpx.get(document.image_url).content
                    data.append(
                        {
                            "id": document.id_,
                            "image_bytes": image_bytes,
                            "image_uri": document.image_url,
                            "label": label,
                            "metadata": json.dumps(document.metadata),
                        }
                    )
                elif document.image_path:
                    image_bytes = document.resolve_image().read()
                    data.append(
                        {
                            "id": document.id_,
                            "image_bytes": image_bytes,
                            "image_uri": document.image_url or "",
                            "label": label,
                            "metadata": json.dumps(document.metadata),
                        }
                    )
                else:
                    warnings.warn(
                        f"Document {document.doc_id} does not contain an image and has thus been skipped",
                        UserWarning,
                    )

        if not self.connection_config.use_async:
            self._table = cast(Table, self._table)
            self._table.add(data)
        else:
            raise ValueError(
                "Attempting to add documents synchronously with an asynchronous connection!"
            )

    definsert_data(
        self, data: Union[List[dict], pl.DataFrame, pd.DataFrame, pa.Table]
    ) -> None:
        if not self.connection_config.use_async:
            self._table = cast(Table, self._table)
            self._table.add(data)
        else:
            raise ValueError(
                "Attempting to add data asynchronously with a synchronous connection!"
            )

    async defainsert_data(
        self, data: Union[List[dict], pl.DataFrame, pd.DataFrame, pa.Table]
    ) -> None:
        if self.connection_config.use_async:
            self._table = cast(AsyncTable, self._table)
            await self._table.add(data)
        else:
            raise ValueError(
                "Attempting to add data synchronously with an asynchronous connection!"
            )

    definsert(self, document: Union[Document, ImageDocument], **insert_kwargs):
        return self.insert_nodes(documents=[document], **insert_kwargs)

    async defainsert(self, document: Union[Document, ImageDocument], **insert_kwargs):
        return await self.ainsert_nodes(documents=[document], **insert_kwargs)

    defdelete_ref_doc(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        if not self.connection_config.use_async:
            self._table = cast(Table, self._table)
            self._table.delete(where="id = '" + ref_doc_id + "'")
        else:
            raise ValueError(
                "Attempting to delete data synchronously with an asynchronous connection!"
            )

    async defadelete_ref_doc(self, ref_doc_id: str, **delete_kwargs):
        if self.connection_config.use_async:
            self._table = cast(AsyncTable, self._table)
            await self._table.delete(where="id = '" + ref_doc_id + "'")
        else:
            raise ValueError(
                "Attempting to delete data asynchronously with a synchronous connection!"
            )

    defdelete_nodes(self, ref_doc_ids: List[str]) -> None:
        if not self.connection_config.use_async:
            self._table = cast(Table, self._table)
            delete_where = "id IN ('" + "', '".join(ref_doc_ids) + "')"
            self._table.delete(where=delete_where)
        else:
            raise ValueError(
                "Attempting to delete data synchronously with an asynchronous connection!"
            )

    async defadelete_nodes(self, ref_doc_ids: List[str]) -> None:
        if self.connection_config.use_async:
            self._table = cast(AsyncTable, self._table)
            delete_where = "id IN ('" + "', '".join(ref_doc_ids) + "')"
            await self._table.delete(where=delete_where)
        else:
            raise ValueError(
                "Attempting to delete data asynchronously with a synchronous connection!"
            )

    def_insert(self, nodes: Any, **insert_kwargs: Any) -> Any:
        raise NotImplementedError("_insert is not implemented.")

    defupdate(self, document: Any, **update_kwargs: Any) -> Any:
        raise NotImplementedError("update is not implemented.")

    defupdate_ref_doc(self, document: Any, **update_kwargs: Any) -> Any:
        raise NotImplementedError("update_ref_doc is not implemented.")

    async defaupdate_ref_doc(self, document: Any, **update_kwargs: Any) -> Any:
        raise NotImplementedError("aupdate_ref_doc is not implemented.")

    defrefresh(self, documents: Any, **update_kwargs: Any) -> Any:
        raise NotImplementedError("refresh is not implemented.")

    defrefresh_ref_docs(self, documents: Any, **update_kwargs: Any) -> Any:
        raise NotImplementedError("refresh_ref_docs is not implemented.")

    async defarefresh_ref_docs(self, documents: Any, **update_kwargs: Any) -> Any:
        raise NotImplementedError("arefresh_ref_docs is not implemented.")

```
 |  
| --- | --- |  
###  from_documents `async` `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/lancedb/#llama_index.indices.managed.lancedb.LanceDBMultiModalIndex.from_documents "Permanent link")

```
from_documents(
    documents: Sequence[Union[, ]],
    connection: Optional[DBConnection] = None,
    uri: Optional[] = None,
    region: Optional[] = None,
    api_key: Optional[] = None,
    text_embedding_model: Optional[
        Literal[
            "bedrock-text",
            "cohere",
            "gemini-text",
            "instructor",
            "ollama",
            "openai",
            "sentence-transformers",
            "gte-text",
            "huggingface",
            "colbert",
            "jina",
            "watsonx",
            "voyageai",
        ]
    ] = None,
    multimodal_embedding_model: Optional[
        Literal["open-clip", "colpali", "jina", "imagebind"]
    ] = None,
    embedding_model_kwargs: [, ] = None,
    table_name:  = DEFAULT_TABLE_NAME,
    indexing: Literal[
        "IVF_PQ",
        "IVF_HNSW_PQ",
        "IVF_HNSW_SQ",
        "FTS",
        "BTREE",
        "BITMAP",
        "LABEL_LIST",
        "NO_INDEXING",
    ] = "IVF_PQ",
    indexing_kwargs: [, ] = None,
    reranker: Optional[Reranker] = None,
    use_async:  = False,
    table_exists:  = False,
) -> 

```

Generate a LanceDBMultiModalIndex from LlamaIndex Documents.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-lancedb/llama_index/indices/managed/lancedb/base.py`  
| 
```
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
```
 | 
```
@classmethod
async deffrom_documents(
    cls,
    documents: Sequence[Union[Document, ImageDocument]],
    connection: Optional[DBConnection] = None,
    uri: Optional[str] = None,
    region: Optional[str] = None,
    api_key: Optional[str] = None,
    text_embedding_model: Optional[
        Literal[
            "bedrock-text",
            "cohere",
            "gemini-text",
            "instructor",
            "ollama",
            "openai",
            "sentence-transformers",
            "gte-text",
            "huggingface",
            "colbert",
            "jina",
            "watsonx",
            "voyageai",
        ]
    ] = None,
    multimodal_embedding_model: Optional[
        Literal["open-clip", "colpali", "jina", "imagebind"]
    ] = None,
    embedding_model_kwargs: Dict[str, Any] = None,
    table_name: str = DEFAULT_TABLE_NAME,
    indexing: Literal[
        "IVF_PQ",
        "IVF_HNSW_PQ",
        "IVF_HNSW_SQ",
        "FTS",
        "BTREE",
        "BITMAP",
        "LABEL_LIST",
        "NO_INDEXING",
    ] = "IVF_PQ",
    indexing_kwargs: Dict[str, Any] = None,
    reranker: Optional[Reranker] = None,
    use_async: bool = False,
    table_exists: bool = False,
) -> "LanceDBMultiModalIndex":
"""
    Generate a LanceDBMultiModalIndex from LlamaIndex Documents.
    """
    if embedding_model_kwargs is None:
        embedding_model_kwargs = {}
    if indexing_kwargs is None:
        indexing_kwargs = {}
    try:
        index = cls(
            connection,
            uri,
            region,
            api_key,
            text_embedding_model,
            multimodal_embedding_model,
            embedding_model_kwargs,
            table_name,
            indexing,
            indexing_kwargs,
            reranker,
            use_async,
            table_exists,
        )
    except ValueError as e:
        raise ValueError(
            f"Initialization of the index from documents are failed: {e}"
        )
    if use_async:
        await index.acreate_index()
    else:
        index.create_index()
    data: List[dict] = []
    if text_embedding_model:
        assert all(isinstance(document, Document) for document in documents)
        for document in documents:
            if document.text:
                data.append(
                    {
                        "id": document.id_,
                        "text": document.text,
                        "metadata": json.dumps(document.metadata),
                    }
                )
            else:
                warnings.warn(
                    f"Document {document.doc_id} does not contain text and has thus been skipped",
                    UserWarning,
                )
    else:
        assert all(isinstance(document, ImageDocument) for document in documents)
        for document in documents:
            label = json.dumps(document.metadata).get("image_label", None) or ""
            if document.image:
                data.append(
                    {
                        "id": document.id_,
                        "image_bytes": document.image,
                        "image_uri": document.image_url or "",
                        "label": label,
                        "metadata": json.dumps(document.metadata),
                    }
                )
            elif document.image_url:
                image_bytes = httpx.get(document.image_url).content
                data.append(
                    {
                        "id": document.id_,
                        "image_bytes": image_bytes,
                        "image_uri": document.image_url,
                        "label": label,
                        "metadata": json.dumps(document.metadata),
                    }
                )
            elif document.image_path:
                image_bytes = document.resolve_image().read()
                data.append(
                    {
                        "id": document.id_,
                        "image_bytes": image_bytes,
                        "image_uri": document.image_url or "",
                        "label": label,
                        "metadata": json.dumps(document.metadata),
                    }
                )
            else:
                warnings.warn(
                    f"Document {document.doc_id} does not contain an image and has thus been skipped",
                    UserWarning,
                )
    if use_async:
        await index._table.add(data)
    else:
        index._table.add(data)
    return index

```
 |  
| --- | --- |  
###  from_data `async` `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/lancedb/#llama_index.indices.managed.lancedb.LanceDBMultiModalIndex.from_data "Permanent link")

```
from_data(
    data: Union[[], Table, DataFrame, DataFrame],
    connection: Optional[DBConnection] = None,
    uri: Optional[] = None,
    region: Optional[] = None,
    api_key: Optional[] = None,
    text_embedding_model: Optional[
        Literal[
            "bedrock-text",
            "cohere",
            "gemini-text",
            "instructor",
            "ollama",
            "openai",
            "sentence-transformers",
            "gte-text",
            "huggingface",
            "colbert",
            "jina",
            "watsonx",
            "voyageai",
        ]
    ] = None,
    multimodal_embedding_model: Optional[
        Literal["open-clip", "colpali", "jina", "imagebind"]
    ] = None,
    embedding_model_kwargs: [, ] = {},
    table_name:  = DEFAULT_TABLE_NAME,
    indexing: Literal[
        "IVF_PQ",
        "IVF_HNSW_PQ",
        "IVF_HNSW_SQ",
        "FTS",
        "BTREE",
        "BITMAP",
        "LABEL_LIST",
        "NO_INDEXING",
    ] = "IVF_PQ",
    indexing_kwargs: [, ] = {},
    reranker: Optional[Reranker] = None,
    use_async:  = False,
    table_exists:  = False,
) -> 

```

Generate a LanceDBMultiModalIndex from Pandas, Polars or PyArrow data.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-lancedb/llama_index/indices/managed/lancedb/base.py`  
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
```
 | 
```
@classmethod
async deffrom_data(
    cls,
    data: Union[List[dict], pa.Table, pl.DataFrame, pd.DataFrame],
    connection: Optional[DBConnection] = None,
    uri: Optional[str] = None,
    region: Optional[str] = None,
    api_key: Optional[str] = None,
    text_embedding_model: Optional[
        Literal[
            "bedrock-text",
            "cohere",
            "gemini-text",
            "instructor",
            "ollama",
            "openai",
            "sentence-transformers",
            "gte-text",
            "huggingface",
            "colbert",
            "jina",
            "watsonx",
            "voyageai",
        ]
    ] = None,
    multimodal_embedding_model: Optional[
        Literal["open-clip", "colpali", "jina", "imagebind"]
    ] = None,
    embedding_model_kwargs: Dict[str, Any] = {},
    table_name: str = DEFAULT_TABLE_NAME,
    indexing: Literal[
        "IVF_PQ",
        "IVF_HNSW_PQ",
        "IVF_HNSW_SQ",
        "FTS",
        "BTREE",
        "BITMAP",
        "LABEL_LIST",
        "NO_INDEXING",
    ] = "IVF_PQ",
    indexing_kwargs: Dict[str, Any] = {},
    reranker: Optional[Reranker] = None,
    use_async: bool = False,
    table_exists: bool = False,
) -> "LanceDBMultiModalIndex":
"""
    Generate a LanceDBMultiModalIndex from Pandas, Polars or PyArrow data.
    """
    try:
        index = cls(
            connection,
            uri,
            region,
            api_key,
            text_embedding_model,
            multimodal_embedding_model,
            embedding_model_kwargs,
            table_name,
            indexing,
            indexing_kwargs,
            reranker,
            use_async,
            table_exists,
        )
    except ValueError as e:
        raise ValueError(
            f"Initialization of the vector store from documents are failed: {e}"
        )
    if use_async:
        await index.acreate_index()
        await index._table.add(data)
    else:
        index.create_index()
        index._table.add(data)

    return index

```
 |  
| --- | --- |  
##  LanceDBRetrieverQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/lancedb/#llama_index.indices.managed.lancedb.LanceDBRetrieverQueryEngine "Permanent link")
Bases: 
Source code in `llama-index-integrations/indices/llama-index-indices-managed-lancedb/llama_index/indices/managed/lancedb/query_engine.py`  
| 
```
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
```
 | 
```
classLanceDBRetrieverQueryEngine(RetrieverQueryEngine):
    def__init__(
        self,
        retriever: LanceDBRetriever,
        response_synthesizer: Optional[BaseSynthesizer] = None,
        node_postprocessors: List[BaseNodePostprocessor] = None,
        callback_manager: Optional[CallbackManager] = None,
    ):
        super().__init__(
            retriever, response_synthesizer, node_postprocessors, callback_manager
        )

    @override
    defretrieve(self, query_bundle: ExtendedQueryBundle) -> List[NodeWithScore]:
        nodes = self._retriever._retrieve(query_bundle)
        return self._apply_node_postprocessors(nodes, query_bundle=query_bundle)

    @override
    async defaretrieve(self, query_bundle: ExtendedQueryBundle) -> List[NodeWithScore]:
        nodes = await self._retriever._aretrieve(query_bundle)
        return self._apply_node_postprocessors(nodes, query_bundle=query_bundle)

    @override
    @dispatcher.span
    def_query(self, query_bundle: ExtendedQueryBundle) -> RESPONSE_TYPE:
"""Answer a query."""
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            nodes = self.retrieve(query_bundle)
            response = self._response_synthesizer.synthesize(
                query=query_bundle,
                nodes=nodes,
            )
            query_event.on_end(payload={EventPayload.RESPONSE: response})

        return response

    @override
    @dispatcher.span
    async def_aquery(self, query_bundle: ExtendedQueryBundle) -> RESPONSE_TYPE:
"""Answer a query."""
        with self.callback_manager.event(
            CBEventType.QUERY, payload={EventPayload.QUERY_STR: query_bundle.query_str}
        ) as query_event:
            nodes = await self.aretrieve(query_bundle)

            response = await self._response_synthesizer.asynthesize(
                query=query_bundle,
                nodes=nodes,
            )

            query_event.on_end(payload={EventPayload.RESPONSE: response})

        return response

    @override
    @dispatcher.span
    defquery(
        self,
        query_str: Optional[str] = None,
        query_image: Optional[
            Union[Image.Image, ImageBlock, ImageDocument, str]
        ] = None,
        query_image_path: Optional[os.PathLike[str]] = None,
    ) -> RESPONSE_TYPE:
"""
        Executes a query against the managed LanceDB index.

        Args:
            query_str (Optional[str]): The text query string to search for. Defaults to None.
            query_image (Optional[Union[Image.Image, ImageBlock, ImageDocument, str]]): An image or image-like object to use as part of the query. Can be a PIL Image, ImageBlock, ImageDocument, or a file path as a string. Defaults to None.
            query_image_path (Optional[os.PathLike[str]]): The file path to an image to use as part of the query. Defaults to None.

        Returns:
            RESPONSE_TYPE: The result of the query.

        Notes:
            - At least one of `query_str`, `query_image`, or `query_image_path` should be provided.

        """
        qb = ExtendedQueryBundle(
            query_str=query_str, image_path=query_image_path, image=query_image
        )
        dispatcher.event(QueryStartEvent(query=qb))
        with self.callback_manager.as_trace("query"):
            if not query_str:
                query_str = ""
            query_result = self._query(qb)
        dispatcher.event(QueryEndEvent(query=qb, response=query_result))
        return query_result

    @override
    @dispatcher.span
    async defaquery(
        self,
        query_str: Optional[str] = None,
        query_image: Optional[
            Union[Image.Image, ImageBlock, ImageDocument, str]
        ] = None,
        query_image_path: Optional[os.PathLike[str]] = None,
    ) -> RESPONSE_TYPE:
"""
        Asynchronously executes a query against the managed LanceDB index.

        Args:
            query_str (Optional[str]): The text query string to search for. Defaults to None.
            query_image (Optional[Union[Image.Image, ImageBlock, ImageDocument, str]]): An image or image-like object to use as part of the query. Can be a PIL Image, ImageBlock, ImageDocument, or a file path as a string. Defaults to None.
            query_image_path (Optional[os.PathLike[str]]): The file path to an image to use as part of the query. Defaults to None.

        Returns:
            RESPONSE_TYPE: The result of the query.

        Notes:
            - At least one of `query_str`, `query_image`, or `query_image_path` should be provided.

        """
        qb = ExtendedQueryBundle(
            query_str=query_str, image_path=query_image_path, image=query_image
        )
        dispatcher.event(QueryStartEvent(query=qb))
        with self.callback_manager.as_trace("query"):
            if not query_str:
                query_str = ""

            query_result = await self._aquery(qb)
        dispatcher.event(QueryEndEvent(query=qb, response=query_result))
        return query_result

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/lancedb/#llama_index.indices.managed.lancedb.LanceDBRetrieverQueryEngine.query "Permanent link")

```
query(
    query_str: Optional[] = None,
    query_image: Optional[
        Union[Image, , , ]
    ] = None,
    query_image_path: Optional[PathLike[]] = None,
) -> RESPONSE_TYPE

```

Executes a query against the managed LanceDB index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_str`  |  `Optional[str]`  |  The text query string to search for. Defaults to None.  |  `None`  |  
|  `query_image`  |  `Optional[Union[Image, ImageBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock "ImageBlock \(llama_index.core.llms.ImageBlock\)"), ImageDocument[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.ImageDocument "ImageDocument \(llama_index.core.schema.ImageDocument\)"), str]]`  |  An image or image-like object to use as part of the query. Can be a PIL Image, ImageBlock, ImageDocument, or a file path as a string. Defaults to None.  |  `None`  |  
|  `query_image_path`  |  `Optional[PathLike[str]]`  |  The file path to an image to use as part of the query. Defaults to None.  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `RESPONSE_TYPE`  |  `RESPONSE_TYPE`  |  The result of the query.  |  
Notes
  * At least one of `query_str`, `query_image`, or `query_image_path` should be provided.

Source code in `llama-index-integrations/indices/llama-index-indices-managed-lancedb/llama_index/indices/managed/lancedb/query_engine.py`  
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
```
 | 
```
@override
@dispatcher.span
defquery(
    self,
    query_str: Optional[str] = None,
    query_image: Optional[
        Union[Image.Image, ImageBlock, ImageDocument, str]
    ] = None,
    query_image_path: Optional[os.PathLike[str]] = None,
) -> RESPONSE_TYPE:
"""
    Executes a query against the managed LanceDB index.

    Args:
        query_str (Optional[str]): The text query string to search for. Defaults to None.
        query_image (Optional[Union[Image.Image, ImageBlock, ImageDocument, str]]): An image or image-like object to use as part of the query. Can be a PIL Image, ImageBlock, ImageDocument, or a file path as a string. Defaults to None.
        query_image_path (Optional[os.PathLike[str]]): The file path to an image to use as part of the query. Defaults to None.

    Returns:
        RESPONSE_TYPE: The result of the query.

    Notes:
        - At least one of `query_str`, `query_image`, or `query_image_path` should be provided.

    """
    qb = ExtendedQueryBundle(
        query_str=query_str, image_path=query_image_path, image=query_image
    )
    dispatcher.event(QueryStartEvent(query=qb))
    with self.callback_manager.as_trace("query"):
        if not query_str:
            query_str = ""
        query_result = self._query(qb)
    dispatcher.event(QueryEndEvent(query=qb, response=query_result))
    return query_result

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/lancedb/#llama_index.indices.managed.lancedb.LanceDBRetrieverQueryEngine.aquery "Permanent link")

```
aquery(
    query_str: Optional[] = None,
    query_image: Optional[
        Union[Image, , , ]
    ] = None,
    query_image_path: Optional[PathLike[]] = None,
) -> RESPONSE_TYPE

```

Asynchronously executes a query against the managed LanceDB index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_str`  |  `Optional[str]`  |  The text query string to search for. Defaults to None.  |  `None`  |  
|  `query_image`  |  `Optional[Union[Image, ImageBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock "ImageBlock \(llama_index.core.llms.ImageBlock\)"), ImageDocument[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.ImageDocument "ImageDocument \(llama_index.core.schema.ImageDocument\)"), str]]`  |  An image or image-like object to use as part of the query. Can be a PIL Image, ImageBlock, ImageDocument, or a file path as a string. Defaults to None.  |  `None`  |  
|  `query_image_path`  |  `Optional[PathLike[str]]`  |  The file path to an image to use as part of the query. Defaults to None.  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `RESPONSE_TYPE`  |  `RESPONSE_TYPE`  |  The result of the query.  |  
Notes
  * At least one of `query_str`, `query_image`, or `query_image_path` should be provided.

Source code in `llama-index-integrations/indices/llama-index-indices-managed-lancedb/llama_index/indices/managed/lancedb/query_engine.py`  
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
```
 | 
```
@override
@dispatcher.span
async defaquery(
    self,
    query_str: Optional[str] = None,
    query_image: Optional[
        Union[Image.Image, ImageBlock, ImageDocument, str]
    ] = None,
    query_image_path: Optional[os.PathLike[str]] = None,
) -> RESPONSE_TYPE:
"""
    Asynchronously executes a query against the managed LanceDB index.

    Args:
        query_str (Optional[str]): The text query string to search for. Defaults to None.
        query_image (Optional[Union[Image.Image, ImageBlock, ImageDocument, str]]): An image or image-like object to use as part of the query. Can be a PIL Image, ImageBlock, ImageDocument, or a file path as a string. Defaults to None.
        query_image_path (Optional[os.PathLike[str]]): The file path to an image to use as part of the query. Defaults to None.

    Returns:
        RESPONSE_TYPE: The result of the query.

    Notes:
        - At least one of `query_str`, `query_image`, or `query_image_path` should be provided.

    """
    qb = ExtendedQueryBundle(
        query_str=query_str, image_path=query_image_path, image=query_image
    )
    dispatcher.event(QueryStartEvent(query=qb))
    with self.callback_manager.as_trace("query"):
        if not query_str:
            query_str = ""

        query_result = await self._aquery(qb)
    dispatcher.event(QueryEndEvent(query=qb, response=query_result))
    return query_result

```
 |  
| --- | --- |  
##  LanceDBRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/lancedb/#llama_index.indices.managed.lancedb.LanceDBRetriever "Permanent link")
Bases: 
Source code in `llama-index-integrations/indices/llama-index-indices-managed-lancedb/llama_index/indices/managed/lancedb/retriever.py`  
| 
```
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
```
 | 
```
classLanceDBRetriever(BaseRetriever):
    def__init__(
        self, table: Union[AsyncTable, Table], multimodal: bool, **kwargs: Any
    ):
        self.table = table
        self.multimodal = multimodal
        callback_manager = kwargs.get("callback_manager")
        verbose = kwargs.get("verbose", False)
        super().__init__(callback_manager, verbose)

    def_retrieve(self, query_bundle: ExtendedQueryBundle) -> List[NodeWithScore]:
        if not self.multimodal:
            return query_text(table=self.table, query=query_bundle.query_str)
        else:
            if not query_bundle.image and not query_bundle.image_path:
                raise ValueError(
                    "No image or image_path has been provided, but retrieval is set to multi-modal."
                )
            elif query_bundle.image:
                return query_multimodal(table=self.table, query=query_bundle.image)
            elif query_bundle.image_path:
                img = ImageBlock(path=query_bundle.image_path)
                return query_multimodal(table=self.table, query=img)
            else:
                return []

    async def_aretrieve(
        self, query_bundle: ExtendedQueryBundle
    ) -> List[NodeWithScore]:
        if not self.multimodal:
            return await aquery_text(table=self.table, query=query_bundle.query_str)
        else:
            if not query_bundle.image and not query_bundle.image_path:
                raise ValueError(
                    "No image or image_path has been provided, but retrieval is set to multi-modal."
                )
            elif query_bundle.image:
                return await aquery_multimodal(
                    table=self.table, query=query_bundle.image
                )
            elif query_bundle.image_path:
                img = ImageBlock(path=query_bundle.image_path)
                return await aquery_multimodal(table=self.table, query=img)
            else:
                return []

    @override
    defretrieve(
        self,
        query_str: Optional[str] = None,
        query_image: Optional[
            Union[Image.Image, ImageBlock, ImageDocument, str]
        ] = None,
        query_image_path: Optional[os.PathLike[str]] = None,
    ) -> List[NodeWithScore]:
"""
        Retrieves nodes relevant to the given query.

        Args:
            query_str (Optional[str]): The text query string. Required if the retriever is not multimodal.
            query_image (Optional[Union[Image.Image, ImageBlock, ImageDocument, str]]): The image query, which can be a PIL Image, ImageBlock, ImageDocument, or a string path/URL. Used if the retriever is multimodal.
            query_image_path (Optional[os.PathLike[str]]): The file path to the image query. Used if the retriever is multimodal.

        Returns:
            List[NodeWithScore]: A list of nodes with associated relevance scores.

        Raises:
            ValueError: If none of the query parameters are provided.
            ValueError: If a text query is not provided for a non-multimodal retriever.
            ValueError: If neither an image nor image path is provided for a multimodal retriever.

        """
        if not query_str and not query_image and not query_image_path:
            raise ValueError(
                "At least one among query_str, query_image and query_image_path needs to be set"
            )
        if not self.multimodal:
            if query_str:
                query_bundle = ExtendedQueryBundle(query_str=query_str)
            else:
                raise ValueError(
                    "No query_str provided, but the retriever is not multimodal"
                )
        else:
            if query_image:
                query_bundle = ExtendedQueryBundle(query_str="", image=query_image)
            elif query_image_path:
                query_bundle = ExtendedQueryBundle(
                    query_str="", image_path=query_image_path
                )
            else:
                raise ValueError(
                    "No query_image or query_image_path provided, but the retriever is multimodal"
                )

        return self._retrieve(query_bundle=query_bundle)

    @override
    async defaretrieve(
        self,
        query_str: Optional[str] = None,
        query_image: Optional[
            Union[Image.Image, ImageBlock, ImageDocument, str]
        ] = None,
        query_image_path: Optional[os.PathLike[str]] = None,
    ) -> List[NodeWithScore]:
"""
        Asynchronously retrieves nodes relevant to the given query.

        Args:
            query_str (Optional[str]): The text query string. Required if the retriever is not multimodal.
            query_image (Optional[Union[Image.Image, ImageBlock, ImageDocument, str]]): The image query, which can be a PIL Image, ImageBlock, ImageDocument, or a string path/URL. Used if the retriever is multimodal.
            query_image_path (Optional[os.PathLike[str]]): The file path to the image query. Used if the retriever is multimodal.

        Returns:
            List[NodeWithScore]: A list of nodes with associated relevance scores.

        Raises:
            ValueError: If none of the query parameters are provided.
            ValueError: If a text query is not provided for a non-multimodal retriever.
            ValueError: If neither an image nor image path is provided for a multimodal retriever.

        """
        if not query_str and not query_image and not query_image_path:
            raise ValueError(
                "At least one among query_str, query_image and query_image_path needs to be set"
            )
        if not self.multimodal:
            if query_str:
                query_bundle = ExtendedQueryBundle(query_str=query_str)
            else:
                raise ValueError(
                    "No query_str provided, but the retriever is not multimodal"
                )
        else:
            if query_image:
                query_bundle = ExtendedQueryBundle(query_str="", image=query_image)
            elif query_image_path:
                query_bundle = ExtendedQueryBundle(
                    query_str="", image_path=query_image_path
                )
            else:
                raise ValueError(
                    "No query_image or query_image_path provided, but the retriever is multimodal"
                )
        return await self._aretrieve(query_bundle=query_bundle)

```
 |  
| --- | --- |  
###  retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/lancedb/#llama_index.indices.managed.lancedb.LanceDBRetriever.retrieve "Permanent link")

```
retrieve(
    query_str: Optional[] = None,
    query_image: Optional[
        Union[Image, , , ]
    ] = None,
    query_image_path: Optional[PathLike[]] = None,
) -> []

```

Retrieves nodes relevant to the given query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_str`  |  `Optional[str]`  |  The text query string. Required if the retriever is not multimodal.  |  `None`  |  
|  `query_image`  |  `Optional[Union[Image, ImageBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock "ImageBlock \(llama_index.core.llms.ImageBlock\)"), ImageDocument[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.ImageDocument "ImageDocument \(llama_index.core.schema.ImageDocument\)"), str]]`  |  The image query, which can be a PIL Image, ImageBlock, ImageDocument, or a string path/URL. Used if the retriever is multimodal.  |  `None`  |  
|  `query_image_path`  |  `Optional[PathLike[str]]`  |  The file path to the image query. Used if the retriever is multimodal.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[NodeWithScore[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.NodeWithScore "NodeWithScore \(llama_index.core.schema.NodeWithScore\)")]`  |  List[NodeWithScore]: A list of nodes with associated relevance scores.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If none of the query parameters are provided.  |  
|  `ValueError`  |  If a text query is not provided for a non-multimodal retriever.  |  
|  `ValueError`  |  If neither an image nor image path is provided for a multimodal retriever.  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-lancedb/llama_index/indices/managed/lancedb/retriever.py`  
| 
```
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
```
 | 
```
@override
defretrieve(
    self,
    query_str: Optional[str] = None,
    query_image: Optional[
        Union[Image.Image, ImageBlock, ImageDocument, str]
    ] = None,
    query_image_path: Optional[os.PathLike[str]] = None,
) -> List[NodeWithScore]:
"""
    Retrieves nodes relevant to the given query.

    Args:
        query_str (Optional[str]): The text query string. Required if the retriever is not multimodal.
        query_image (Optional[Union[Image.Image, ImageBlock, ImageDocument, str]]): The image query, which can be a PIL Image, ImageBlock, ImageDocument, or a string path/URL. Used if the retriever is multimodal.
        query_image_path (Optional[os.PathLike[str]]): The file path to the image query. Used if the retriever is multimodal.

    Returns:
        List[NodeWithScore]: A list of nodes with associated relevance scores.

    Raises:
        ValueError: If none of the query parameters are provided.
        ValueError: If a text query is not provided for a non-multimodal retriever.
        ValueError: If neither an image nor image path is provided for a multimodal retriever.

    """
    if not query_str and not query_image and not query_image_path:
        raise ValueError(
            "At least one among query_str, query_image and query_image_path needs to be set"
        )
    if not self.multimodal:
        if query_str:
            query_bundle = ExtendedQueryBundle(query_str=query_str)
        else:
            raise ValueError(
                "No query_str provided, but the retriever is not multimodal"
            )
    else:
        if query_image:
            query_bundle = ExtendedQueryBundle(query_str="", image=query_image)
        elif query_image_path:
            query_bundle = ExtendedQueryBundle(
                query_str="", image_path=query_image_path
            )
        else:
            raise ValueError(
                "No query_image or query_image_path provided, but the retriever is multimodal"
            )

    return self._retrieve(query_bundle=query_bundle)

```
 |  
| --- | --- |  
###  aretrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/lancedb/#llama_index.indices.managed.lancedb.LanceDBRetriever.aretrieve "Permanent link")

```
aretrieve(
    query_str: Optional[] = None,
    query_image: Optional[
        Union[Image, , , ]
    ] = None,
    query_image_path: Optional[PathLike[]] = None,
) -> []

```

Asynchronously retrieves nodes relevant to the given query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_str`  |  `Optional[str]`  |  The text query string. Required if the retriever is not multimodal.  |  `None`  |  
|  `query_image`  |  `Optional[Union[Image, ImageBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock "ImageBlock \(llama_index.core.llms.ImageBlock\)"), ImageDocument[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.ImageDocument "ImageDocument \(llama_index.core.schema.ImageDocument\)"), str]]`  |  The image query, which can be a PIL Image, ImageBlock, ImageDocument, or a string path/URL. Used if the retriever is multimodal.  |  `None`  |  
|  `query_image_path`  |  `Optional[PathLike[str]]`  |  The file path to the image query. Used if the retriever is multimodal.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[NodeWithScore[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.NodeWithScore "NodeWithScore \(llama_index.core.schema.NodeWithScore\)")]`  |  List[NodeWithScore]: A list of nodes with associated relevance scores.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If none of the query parameters are provided.  |  
|  `ValueError`  |  If a text query is not provided for a non-multimodal retriever.  |  
|  `ValueError`  |  If neither an image nor image path is provided for a multimodal retriever.  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-lancedb/llama_index/indices/managed/lancedb/retriever.py`  
| 
```
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
```
 | 
```
@override
async defaretrieve(
    self,
    query_str: Optional[str] = None,
    query_image: Optional[
        Union[Image.Image, ImageBlock, ImageDocument, str]
    ] = None,
    query_image_path: Optional[os.PathLike[str]] = None,
) -> List[NodeWithScore]:
"""
    Asynchronously retrieves nodes relevant to the given query.

    Args:
        query_str (Optional[str]): The text query string. Required if the retriever is not multimodal.
        query_image (Optional[Union[Image.Image, ImageBlock, ImageDocument, str]]): The image query, which can be a PIL Image, ImageBlock, ImageDocument, or a string path/URL. Used if the retriever is multimodal.
        query_image_path (Optional[os.PathLike[str]]): The file path to the image query. Used if the retriever is multimodal.

    Returns:
        List[NodeWithScore]: A list of nodes with associated relevance scores.

    Raises:
        ValueError: If none of the query parameters are provided.
        ValueError: If a text query is not provided for a non-multimodal retriever.
        ValueError: If neither an image nor image path is provided for a multimodal retriever.

    """
    if not query_str and not query_image and not query_image_path:
        raise ValueError(
            "At least one among query_str, query_image and query_image_path needs to be set"
        )
    if not self.multimodal:
        if query_str:
            query_bundle = ExtendedQueryBundle(query_str=query_str)
        else:
            raise ValueError(
                "No query_str provided, but the retriever is not multimodal"
            )
    else:
        if query_image:
            query_bundle = ExtendedQueryBundle(query_str="", image=query_image)
        elif query_image_path:
            query_bundle = ExtendedQueryBundle(
                query_str="", image_path=query_image_path
            )
        else:
            raise ValueError(
                "No query_image or query_image_path provided, but the retriever is multimodal"
            )
    return await self._aretrieve(query_bundle=query_bundle)

```
 |  
| --- | --- |  
options: members: - LanceDBMultiModalIndex
