# Tablestore
##  TablestoreVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tablestore/#llama_index.vector_stores.tablestore.TablestoreVectorStore "Permanent link")
Bases: 
Tablestore vector store.
In this vector store we store the text, its embedding and its metadata in Tablestore.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `tablestore_client`  |  `OTSClient`  |  External tablestore(ots) client. If this parameter is set, the following endpoint/instance_name/access_key_id/access_key_secret will be ignored.  |  `None`  |  
|  `endpoint`  |  Tablestore instance endpoint.  |  `None`  |  
|  `instance_name`  |  Tablestore instance name.  |  `None`  |  
|  `access_key_id`  |  Aliyun access key id.  |  `None`  |  
|  `access_key_secret`  |  Aliyun access key secret.  |  `None`  |  
|  `table_name`  |  Tablestore table name.  |  `'llama_index_vector_store_ots_v1'`  |  
|  `index_name`  |  Tablestore SearchIndex index name.  |  `'llama_index_vector_store_ots_index_v1'`  |  
|  `text_field`  |  Name of the Tablestore field that stores the text.  |  `'content'`  |  
|  `vector_field`  |  Name of the Tablestore field that stores the embedding.  |  `'embedding'`  |  
|  `ref_doc_id_field`  |  Name of the Tablestore field that stores the ref doc id.  |  `'ref_doc_id'`  |  
|  `vector_dimension`  |  The dimension of the embedding vectors.  |  `512`  |  
|  `vector_metric_type`  |  `VectorMetricType`  |  The similarity metric type to use.  |  `VM_COSINE`  |  
|  `metadata_mappings`  |  `list[FieldSchema]`  |  Custom metadata mapping is used to filter non-vector fields. See the following documentation for details: https://help.aliyun.com/zh/tablestore/developer-reference/create-search-indexes-by-using-python-sdk  |  `None`  |  
|  `kwargs`  |  Additional arguments to pass to the tablestore(ots) client.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `TablestoreVectorStore`  |  Vectorstore that supports add, delete, and query.  |  
Examples:
`pip install llama-index-vector-stores-tablestore`

```
importtablestore

# create a vector store that does not support filtering non-vector fields
vector_store = TablestoreVectorStore(
    endpoint="<end_point>",
    instance_name="<instance_name>",
    access_key_id="<access_key_id>",
    access_key_secret="<access_key_secret>",
    vector_dimension=512,
)

# create a vector store that support filtering non-vector fields
vector_store_with_meta_data = TablestoreVectorStore(
    endpoint="<end_point>",
    instance_name="<instance_name>",
    access_key_id="<access_key_id>",
    access_key_secret="<access_key_secret>",
    vector_dimension=512,
    # optional: custom metadata mapping is used to filter non-vector fields.
    metadata_mappings=[
        tablestore.FieldSchema(
            "type",  # non-vector fields
            tablestore.FieldType.KEYWORD,
            index=True,
            enable_sort_and_agg=True,
        ),
        tablestore.FieldSchema(
            "time", # non-vector fields
            tablestore.FieldType.LONG,
            index=True,
            enable_sort_and_agg=True,
        ),
    ],
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tablestore/llama_index/vector_stores/tablestore/base.py`  
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
```
 | 
```
classTablestoreVectorStore(BasePydanticVectorStore):
"""
    Tablestore vector store.

    In this vector store we store the text, its embedding and
    its metadata in Tablestore.

    Args:
        tablestore_client (OTSClient, optional): External tablestore(ots) client.
                If this parameter is set, the following endpoint/instance_name/access_key_id/access_key_secret will be ignored.
        endpoint (str, optional): Tablestore instance endpoint.
        instance_name (str, optional): Tablestore instance name.
        access_key_id (str, optional): Aliyun access key id.
        access_key_secret (str, optional): Aliyun access key secret.
        table_name (str, optional): Tablestore table name.
        index_name (str, optional): Tablestore SearchIndex index name.
        text_field (str, optional): Name of the Tablestore field that stores the text.
        vector_field (str, optional): Name of the Tablestore field that stores the embedding.
        ref_doc_id_field (str, optional): Name of the Tablestore field that stores the ref doc id.
        vector_dimension (int): The dimension of the embedding vectors.
        vector_metric_type (VectorMetricType, optional): The similarity metric type to use.
        metadata_mappings (list[FieldSchema], optional): Custom metadata mapping is used to filter non-vector fields.
                See the following documentation for details:
                https://help.aliyun.com/zh/tablestore/developer-reference/create-search-indexes-by-using-python-sdk
        kwargs (Any): Additional arguments to pass to the tablestore(ots) client.

    Returns:
        TablestoreVectorStore: Vectorstore that supports add, delete, and query.

    Examples:
        `pip install llama-index-vector-stores-tablestore`
        ```python
        import tablestore

        # create a vector store that does not support filtering non-vector fields
        vector_store = TablestoreVectorStore(
            endpoint="<end_point>",
            instance_name="<instance_name>",
            access_key_id="<access_key_id>",
            access_key_secret="<access_key_secret>",
            vector_dimension=512,


        # create a vector store that support filtering non-vector fields
        vector_store_with_meta_data = TablestoreVectorStore(
            endpoint="<end_point>",
            instance_name="<instance_name>",
            access_key_id="<access_key_id>",
            access_key_secret="<access_key_secret>",
            vector_dimension=512,
            # optional: custom metadata mapping is used to filter non-vector fields.
            metadata_mappings=[
                tablestore.FieldSchema(
                    "type",  # non-vector fields
                    tablestore.FieldType.KEYWORD,
                    index=True,
                    enable_sort_and_agg=True,

                tablestore.FieldSchema(
                    "time", # non-vector fields
                    tablestore.FieldType.LONG,
                    index=True,
                    enable_sort_and_agg=True,



        ```

    """

    stores_text: bool = True

    _vector_dimension: int = PrivateAttr(default=512)
    _logger: Any = PrivateAttr(default=None)
    _tablestore_client: tablestore.OTSClient = PrivateAttr(default=None)
    _table_name: str = PrivateAttr(default="llama_index_vector_store_ots_v1")
    _index_name: str = PrivateAttr(default="llama_index_vector_store_ots_index_v1")
    _text_field: str = PrivateAttr(default="content")
    _vector_field: str = PrivateAttr(default="embedding")
    _ref_doc_id_field: str = PrivateAttr(default="ref_doc_id")
    _metadata_mappings: List[tablestore.FieldSchema] = PrivateAttr(default=None)

    def__init__(
        self,
        tablestore_client: Optional[tablestore.OTSClient] = None,
        endpoint: Optional[str] = None,
        instance_name: Optional[str] = None,
        access_key_id: Optional[str] = None,
        access_key_secret: Optional[str] = None,
        table_name: str = "llama_index_vector_store_ots_v1",
        index_name: str = "llama_index_vector_store_ots_index_v1",
        text_field: str = "content",
        vector_field: str = "embedding",
        ref_doc_id_field: str = "ref_doc_id",
        vector_dimension: int = 512,
        vector_metric_type: tablestore.VectorMetricType = tablestore.VectorMetricType.VM_COSINE,
        metadata_mappings: Optional[List[tablestore.FieldSchema]] = None,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        super().__init__()
        self._logger = getLogger(__name__)
        if not tablestore_client:
            self._tablestore_client = tablestore.OTSClient(
                endpoint,
                access_key_id,
                access_key_secret,
                instance_name,
                retry_policy=tablestore.WriteRetryPolicy(),
                **kwargs,  # pass additional arguments
            )
        else:
            self._tablestore_client = tablestore_client
        self._vector_dimension = vector_dimension
        self._table_name = table_name
        self._index_name = index_name
        self._text_field = text_field
        self._vector_field = vector_field
        self._ref_doc_id_field = ref_doc_id_field

        self._metadata_mappings = [
            tablestore.FieldSchema(
                text_field,
                tablestore.FieldType.TEXT,
                index=True,
                enable_sort_and_agg=False,
                store=False,
                analyzer=tablestore.AnalyzerType.MAXWORD,
            ),
            tablestore.FieldSchema(
                ref_doc_id_field,
                tablestore.FieldType.KEYWORD,
                index=True,
                enable_sort_and_agg=True,
                store=False,
            ),
            tablestore.FieldSchema(
                vector_field,
                tablestore.FieldType.VECTOR,
                vector_options=tablestore.VectorOptions(
                    data_type=tablestore.VectorDataType.VD_FLOAT_32,
                    dimension=vector_dimension,
                    metric_type=vector_metric_type,
                ),
            ),
        ]
        if metadata_mappings:
            for mapping in metadata_mappings:
                if (
                    mapping.field_name == text_field
                    or mapping.field_name == vector_field
                    or mapping.field_name == ref_doc_id_field
                ):
                    continue
                self._metadata_mappings.append(mapping)

    defcreate_table_if_not_exist(self) -> None:
"""Create table if not exist."""
        table_list = self._tablestore_client.list_table()
        if self._table_name in table_list:
            self._logger.info(
                "Tablestore system table[%s] already exists", self._table_name
            )
            return
        self._logger.info(
            "Tablestore system table[%s] does not exist, try to create the table.",
            self._table_name,
        )

        schema_of_primary_key = [("id", "STRING")]
        table_meta = tablestore.TableMeta(self._table_name, schema_of_primary_key)
        table_options = tablestore.TableOptions()
        reserved_throughput = tablestore.ReservedThroughput(
            tablestore.CapacityUnit(0, 0)
        )
        try:
            self._tablestore_client.create_table(
                table_meta, table_options, reserved_throughput
            )
            self._logger.info(
                "Tablestore create table[%s] successfully.", self._table_name
            )
        except tablestore.OTSClientError as e:
            traceback.print_exc()
            self._logger.exception(
                "Tablestore create system table[%s] failed with client error, http_status:%d, error_message:%s",
                self._table_name,
                e.get_http_status(),
                e.get_error_message(),
            )
        except tablestore.OTSServiceError as e:
            traceback.print_exc()
            self._logger.exception(
                "Tablestore create system table[%s] failed with client error, http_status:%d, error_code:%s, error_message:%s, request_id:%s",
                self._table_name,
                e.get_http_status(),
                e.get_error_code(),
                e.get_error_message(),
                e.get_request_id(),
            )

    defcreate_search_index_if_not_exist(self) -> None:
"""Create search index if not exist."""
        search_index_list = self._tablestore_client.list_search_index(
            table_name=self._table_name
        )
        if self._index_name in [t[1] for t in search_index_list]:
            self._logger.info(
                "Tablestore system index[%s] already exists", self._index_name
            )
            return
        index_meta = tablestore.SearchIndexMeta(self._metadata_mappings)
        self._tablestore_client.create_search_index(
            self._table_name, self._index_name, index_meta
        )
        self._logger.info(
            "Tablestore create system index[%s] successfully.", self._index_name
        )

    defdelete_table_if_exists(self):
"""Delete table if exists."""
        search_index_list = self._tablestore_client.list_search_index(
            table_name=self._table_name
        )
        for resp_tuple in search_index_list:
            self._tablestore_client.delete_search_index(resp_tuple[0], resp_tuple[1])
            self._logger.info(
                "Tablestore delete index[%s] successfully.", self._index_name
            )
        self._tablestore_client.delete_table(self._table_name)
        self._logger.info(
            "Tablestore delete system table[%s] successfully.", self._index_name
        )

    defdelete_search_index(self, table_name, index_name) -> None:
        self._tablestore_client.delete_search_index(table_name, index_name)
        self._logger.info("Tablestore delete index[%s] successfully.", self._index_name)

    def_write_row(
        self,
        row_id: str,
        content: str,
        embedding_vector: List[float],
        metadata: Dict[str, Any],
    ) -> None:
        primary_key = [("id", row_id)]
        attribute_columns = [
            (self._text_field, content),
            (self._vector_field, json.dumps(embedding_vector)),
        ]
        for k, v in metadata.items():
            item = (k, v)
            attribute_columns.append(item)
        row = tablestore.Row(primary_key, attribute_columns)

        try:
            self._tablestore_client.put_row(self._table_name, row)
            self._logger.debug(
                "Tablestore put row successfully. id:%s, content:%s, meta_data:%s",
                row_id,
                content,
                metadata,
            )
        except tablestore.OTSClientError as e:
            self._logger.exception(
                "Tablestore put row failed with client error:%s, id:%s, content:%s, meta_data:%s",
                e,
                row_id,
                content,
                metadata,
            )
        except tablestore.OTSServiceError as e:
            self._logger.exception(
                "Tablestore put row failed with client error:%s, id:%s, content:%s, meta_data:%s, http_status:%d, error_code:%s, error_message:%s, request_id:%s",
                e,
                row_id,
                content,
                metadata,
                e.get_http_status(),
                e.get_error_code(),
                e.get_error_message(),
                e.get_request_id(),
            )

    def_delete_row(self, row_id: str) -> None:
        primary_key = [("id", row_id)]
        try:
            self._tablestore_client.delete_row(self._table_name, primary_key, None)
            self._logger.info("Tablestore delete row successfully. id:%s", row_id)
        except tablestore.OTSClientError as e:
            self._logger.exception(
                "Tablestore delete row failed with client error:%s, id:%s", e, row_id
            )
        except tablestore.OTSServiceError as e:
            self._logger.exception(
                "Tablestore delete row failed with client error:%s, id:%s, http_status:%d, error_code:%s, error_message:%s, request_id:%s",
                e,
                row_id,
                e.get_http_status(),
                e.get_error_code(),
                e.get_error_message(),
                e.get_request_id(),
            )

    def_delete_all(self) -> None:
        inclusive_start_primary_key = [("id", tablestore.INF_MIN)]
        exclusive_end_primary_key = [("id", tablestore.INF_MAX)]
        total = 0
        try:
            while True:
                (
                    consumed,
                    next_start_primary_key,
                    row_list,
                    next_token,
                ) = self._tablestore_client.get_range(
                    self._table_name,
                    tablestore.Direction.FORWARD,
                    inclusive_start_primary_key,
                    exclusive_end_primary_key,
                    [],
                    5000,
                    max_version=1,
                )
                for row in row_list:
                    self._tablestore_client.delete_row(
                        self._table_name, row.primary_key, None
                    )
                    total += 1
                if next_start_primary_key is not None:
                    inclusive_start_primary_key = next_start_primary_key
                else:
                    break
        except tablestore.OTSClientError as e:
            self._logger.exception(
                "Tablestore delete row failed with client error:%s", e
            )
        except tablestore.OTSServiceError as e:
            self._logger.exception(
                "Tablestore delete row failed with client error:%s, http_status:%d, error_code:%s, error_message:%s, request_id:%s",
                e,
                e.get_http_status(),
                e.get_error_code(),
                e.get_error_message(),
                e.get_request_id(),
            )
        self._logger.info("delete all rows count:%d", total)

    def_search(
        self, query: VectorStoreQuery, knn_top_k: int
    ) -> VectorStoreQueryResult:
        filter_query = self._parse_filters(query.filters)
        query_mode = query.mode
        query_str = query.query_str
        query_embedding = query.query_embedding
        ots_text_query = tablestore.BoolQuery(
            must_queries=[
                filter_query,
                tablestore.MatchQuery(field_name=self._text_field, text=query_str),
            ],
            must_not_queries=[],
            filter_queries=[],
            should_queries=[],
        )
        ots_vector_query = tablestore.KnnVectorQuery(
            field_name=self._vector_field,
            top_k=knn_top_k,
            float32_query_vector=query_embedding,
            filter=filter_query,
        )
        if query_mode == VectorStoreQueryMode.HYBRID:
            if query_str is None:
                raise ValueError("query_str cannot be None")
            ots_query = tablestore.BoolQuery(
                must_queries=[],
                must_not_queries=[],
                filter_queries=[],
                should_queries=[
                    ots_text_query,
                    ots_vector_query,
                ],
                minimum_should_match=1,
            )
        elif query_mode == VectorStoreQueryMode.TEXT_SEARCH:
            if query_str is None:
                raise ValueError("query_str cannot be None")
            ots_query = ots_text_query
        else:
            ots_query = ots_vector_query
        sort = tablestore.Sort(
            sorters=[tablestore.ScoreSort(sort_order=tablestore.SortOrder.DESC)]
        )
        search_query = tablestore.SearchQuery(
            ots_query, limit=query.similarity_top_k, get_total_count=False, sort=sort
        )
        try:
            search_response = self._tablestore_client.search(
                table_name=self._table_name,
                index_name=self._index_name,
                search_query=search_query,
                columns_to_get=tablestore.ColumnsToGet(
                    return_type=tablestore.ColumnReturnType.ALL
                ),
            )
            self._logger.info(
                "Tablestore search successfully. request_id:%s",
                search_response.request_id,
            )
            return self._to_query_result(search_response)
        except tablestore.OTSClientError as e:
            self._logger.exception("Tablestore search failed with client error:%s", e)
        except tablestore.OTSServiceError as e:
            self._logger.exception(
                "Tablestore search failed with client error:%s, http_status:%d, error_code:%s, error_message:%s, request_id:%s",
                e,
                e.get_http_status(),
                e.get_error_code(),
                e.get_error_message(),
                e.get_request_id(),
            )

    def_filter(
        self,
        filters: Optional[MetadataFilters] = None,
        return_type: Optional[
            tablestore.ColumnReturnType
        ] = tablestore.ColumnReturnType.ALL,
        limit: Optional[int] = 100,
    ) -> List:
        if filters is None:
            return []
        filter_query = self._parse_filters(filters)
        search_query = tablestore.SearchQuery(
            filter_query, limit=1, get_total_count=False
        )
        all_rows = []
        try:
            # first round
            search_response = self._tablestore_client.search(
                table_name=self._table_name,
                index_name=self._index_name,
                search_query=search_query,
                columns_to_get=tablestore.ColumnsToGet(return_type=return_type),
            )
            all_rows.extend(search_response.rows)
            # loop
            while search_response.next_token:
                search_query.next_token = search_response.next_token
                search_response = self._tablestore_client.search(
                    table_name=self._table_name,
                    index_name=self._index_name,
                    search_query=search_query,
                    columns_to_get=tablestore.ColumnsToGet(return_type=return_type),
                )
                all_rows.extend(search_response.rows)
            return all_rows
        except tablestore.OTSClientError as e:
            self._logger.exception("Tablestore search failed with client error:%s", e)
        except tablestore.OTSServiceError as e:
            self._logger.exception(
                "Tablestore search failed with client error:%s, http_status:%d, error_code:%s, error_message:%s, request_id:%s",
                e,
                e.get_http_status(),
                e.get_error_code(),
                e.get_error_message(),
                e.get_request_id(),
            )

    def_to_get_nodes_result(self, rows) -> List[TextNode]:
        nodes = []
        for row in rows:
            node_id = row[0][0][1]
            meta_data = {}
            text = None
            embedding = None
            for col in row[1]:
                key = col[0]
                val = col[1]
                if key == self._text_field:
                    text = val
                    continue
                if key == self._vector_field:
                    embedding = json.loads(val)
                    continue
                meta_data[key] = val
            node = TextNode(
                id_=node_id,
                text=text,
                metadata=meta_data,
                embedding=embedding,
            )
            nodes.append(node)
        return nodes

    def_get_row(self, row_id: str) -> Optional[TextNode]:
        primary_key = [("id", row_id)]
        try:
            _, row, _ = self._tablestore_client.get_row(
                self._table_name, primary_key, None, None, 1
            )
            self._logger.debug("Tablestore get row successfully. id:%s", row_id)
            if row is None:
                return None
            node_id = row.primary_key[0][1]
            meta_data = {}
            text = None
            embedding = None
            for col in row.attribute_columns:
                key = col[0]
                val = col[1]
                if key == self._text_field:
                    text = val
                    continue
                if key == self._vector_field:
                    embedding = json.loads(val)
                    continue
                meta_data[key] = val
            return TextNode(
                id_=node_id,
                text=text,
                metadata=meta_data,
                embedding=embedding,
            )
        except tablestore.OTSClientError as e:
            self._logger.exception(
                "Tablestore get row failed with client error:%s, id:%s", e, row_id
            )
        except tablestore.OTSServiceError as e:
            self._logger.exception(
                "Tablestore get row failed with client error:%s, "
                "id:%s, http_status:%d, error_code:%s, error_message:%s, request_id:%s",
                e,
                row_id,
                e.get_http_status(),
                e.get_error_code(),
                e.get_error_message(),
                e.get_request_id(),
            )

    def_to_query_result(self, search_response) -> VectorStoreQueryResult:
        nodes = []
        ids = []
        similarities = []
        for hit in search_response.search_hits:
            row = hit.row
            score = hit.score
            node_id = row[0][0][1]
            meta_data = {}
            text = None
            embedding = None
            for col in row[1]:
                key = col[0]
                val = col[1]
                if key == self._text_field:
                    text = val
                    continue
                if key == self._vector_field:
                    embedding = json.loads(val)
                    continue
                meta_data[key] = val
            node = TextNode(
                id_=node_id,
                text=text,
                metadata=meta_data,
                embedding=embedding,
            )
            ids.append(node_id)
            nodes.append(node)
            similarities.append(score)
        return VectorStoreQueryResult(nodes=nodes, ids=ids, similarities=similarities)

    def_parse_filters_recursively(
        self, filters: MetadataFilters
    ) -> tablestore.BoolQuery:
"""Parse (possibly nested) MetadataFilters to equivalent tablestore search expression."""
        bool_query = tablestore.BoolQuery(
            must_queries=[],
            must_not_queries=[],
            filter_queries=[],
            should_queries=[],
            minimum_should_match=None,
        )
        if filters.condition is FilterCondition.AND:
            bool_clause = bool_query.must_queries
        elif filters.condition is FilterCondition.OR:
            bool_clause = bool_query.should_queries
        else:
            raise ValueError(f"Unsupported filter condition: {filters.condition}")

        for filter_item in filters.filters:
            if isinstance(filter_item, MetadataFilter):
                bool_clause.append(self._parse_filter(filter_item))
            elif isinstance(filter_item, MetadataFilters):
                bool_clause.append(self._parse_filters_recursively(filter_item))
            else:
                raise ValueError(f"Unsupported filter type: {type(filter_item)}")

        return bool_query

    def_parse_filters(self, filters: Optional[MetadataFilters]) -> tablestore.Query:
"""Parse MetadataFilters to equivalent OpenSearch expression."""
        if filters is None:
            return tablestore.MatchAllQuery()
        return self._parse_filters_recursively(filters=filters)

    @staticmethod
    def_parse_filter(filter_item: MetadataFilter) -> tablestore.Query:
        key = filter_item.key
        val = filter_item.value
        op = filter_item.operator

        if op == FilterOperator.EQ:
            return tablestore.TermQuery(field_name=key, column_value=val)
        elif op == FilterOperator.GT:
            return tablestore.RangeQuery(
                field_name=key, range_from=val, include_lower=False
            )
        elif op == FilterOperator.GTE:
            return tablestore.RangeQuery(
                field_name=key, range_from=val, include_lower=True
            )
        elif op == FilterOperator.LT:
            return tablestore.RangeQuery(
                field_name=key, range_to=val, include_upper=False
            )
        elif op == FilterOperator.LTE:
            return tablestore.RangeQuery(
                field_name=key, range_to=val, include_upper=True
            )
        elif op == FilterOperator.NE:
            bq = tablestore.BoolQuery(
                must_queries=[],
                must_not_queries=[],
                filter_queries=[],
                should_queries=[],
                minimum_should_match=None,
            )
            bq.must_not_queries.append(
                tablestore.TermQuery(field_name=key, column_value=val)
            )
            return bq
        elif op in [FilterOperator.IN, FilterOperator.ANY]:
            return tablestore.TermsQuery(field_name=key, column_values=val)
        elif op == FilterOperator.NIN:
            bq = tablestore.BoolQuery(
                must_queries=[],
                must_not_queries=[],
                filter_queries=[],
                should_queries=[],
                minimum_should_match=None,
            )
            bq.must_not_queries.append(
                tablestore.TermsQuery(field_name=key, column_values=val)
            )
            return bq
        elif op == FilterOperator.ALL:
            bq = tablestore.BoolQuery(
                must_queries=[],
                must_not_queries=[],
                filter_queries=[],
                should_queries=[],
                minimum_should_match=None,
            )
            for val_item in val:
                bq.must_queries.append(
                    tablestore.TermQuery(field_name=key, column_value=val_item)
                )
            return bq
        elif op == FilterOperator.TEXT_MATCH:
            return tablestore.MatchQuery(field_name=key, text=val)
        elif op == FilterOperator.CONTAINS:
            return tablestore.WildcardQuery(field_name=key, value=f"*{val}*")
        else:
            raise ValueError(f"Unsupported filter operator: {filter_item.operator}")

    @property
    defclient(self) -> Any:
"""Get client."""
        return self._tablestore_client

    defadd(self, nodes: List[BaseNode], **kwargs: Any) -> List[str]:
"""Add nodes to vector store."""
        if len(nodes) == 0:
            return []
        ids = []
        for node in nodes:
            if len(node.get_embedding()) != self._vector_dimension:
                raise RuntimeError(
                    "node embedding size:%d is not the same as vector store dim:%d"
                    % (len(node.get_embedding()), self._vector_dimension)
                )
            self._write_row(
                row_id=node.node_id,
                content=node.text,
                embedding_vector=node.get_embedding(),
                metadata=node.metadata,
            )
            ids.append(node.node_id)
        return ids

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""Delete nodes from vector store."""
        if node_ids is None and filters is None:
            raise RuntimeError("node_ids and filters cannot be None at the same time.")
        if node_ids is not None and filters is not None:
            raise RuntimeError("node_ids and filters cannot be set at the same time.")
        if filters is not None:
            rows = self._filter(
                filters=filters, return_type=tablestore.ColumnReturnType.NONE
            )
            for row in rows:
                self._delete_row(row[0][0][1])
        if node_ids is not None:
            for node_id in node_ids:
                self._delete_row(node_id)

    defget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> List[BaseNode]:
"""Get nodes from vector store."""
        if node_ids is None and filters is None:
            raise RuntimeError("node_ids and filters cannot be None at the same time.")
        if node_ids is not None and filters is not None:
            raise RuntimeError("node_ids and filters cannot be set at the same time.")
        if filters is not None:
            rows = self._filter(
                filters=filters, return_type=tablestore.ColumnReturnType.ALL
            )
            return self._to_get_nodes_result(rows)
        if node_ids is not None:
            nodes = []
            for node_id in node_ids:
                nodes.append(self._get_row(node_id))
            return nodes
        return []

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""Delete nodes using with ref_doc_id."""
        rows = self._filter(
            filters=MetadataFilters(
                filters=[
                    MetadataFilter(
                        key=self._ref_doc_id_field,
                        value=ref_doc_id,
                        operator=FilterOperator.EQ,
                    ),
                ],
                condition=FilterCondition.AND,
            ),
            return_type=tablestore.ColumnReturnType.NONE,
        )
        for row in rows:
            self._delete_row(row[0][0][1])

    defclear(self) -> None:
"""Clear all nodes from configured vector store."""
        self._delete_all()

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query vector store."""
        knn_top_k = query.similarity_top_k
        if "knn_top_k" in kwargs:
            knn_top_k = kwargs["knn_top_k"]
        return self._search(query=query, knn_top_k=knn_top_k)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tablestore/#llama_index.vector_stores.tablestore.TablestoreVectorStore.client "Permanent link")

```
client: 

```

Get client.
###  create_table_if_not_exist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tablestore/#llama_index.vector_stores.tablestore.TablestoreVectorStore.create_table_if_not_exist "Permanent link")

```
create_table_if_not_exist() -> None

```

Create table if not exist.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tablestore/llama_index/vector_stores/tablestore/base.py`  
| 
```
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
```
 | 
```
defcreate_table_if_not_exist(self) -> None:
"""Create table if not exist."""
    table_list = self._tablestore_client.list_table()
    if self._table_name in table_list:
        self._logger.info(
            "Tablestore system table[%s] already exists", self._table_name
        )
        return
    self._logger.info(
        "Tablestore system table[%s] does not exist, try to create the table.",
        self._table_name,
    )

    schema_of_primary_key = [("id", "STRING")]
    table_meta = tablestore.TableMeta(self._table_name, schema_of_primary_key)
    table_options = tablestore.TableOptions()
    reserved_throughput = tablestore.ReservedThroughput(
        tablestore.CapacityUnit(0, 0)
    )
    try:
        self._tablestore_client.create_table(
            table_meta, table_options, reserved_throughput
        )
        self._logger.info(
            "Tablestore create table[%s] successfully.", self._table_name
        )
    except tablestore.OTSClientError as e:
        traceback.print_exc()
        self._logger.exception(
            "Tablestore create system table[%s] failed with client error, http_status:%d, error_message:%s",
            self._table_name,
            e.get_http_status(),
            e.get_error_message(),
        )
    except tablestore.OTSServiceError as e:
        traceback.print_exc()
        self._logger.exception(
            "Tablestore create system table[%s] failed with client error, http_status:%d, error_code:%s, error_message:%s, request_id:%s",
            self._table_name,
            e.get_http_status(),
            e.get_error_code(),
            e.get_error_message(),
            e.get_request_id(),
        )

```
 |  
| --- | --- |  
###  create_search_index_if_not_exist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tablestore/#llama_index.vector_stores.tablestore.TablestoreVectorStore.create_search_index_if_not_exist "Permanent link")

```
create_search_index_if_not_exist() -> None

```

Create search index if not exist.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tablestore/llama_index/vector_stores/tablestore/base.py`  
| 
```
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
```
 | 
```
defcreate_search_index_if_not_exist(self) -> None:
"""Create search index if not exist."""
    search_index_list = self._tablestore_client.list_search_index(
        table_name=self._table_name
    )
    if self._index_name in [t[1] for t in search_index_list]:
        self._logger.info(
            "Tablestore system index[%s] already exists", self._index_name
        )
        return
    index_meta = tablestore.SearchIndexMeta(self._metadata_mappings)
    self._tablestore_client.create_search_index(
        self._table_name, self._index_name, index_meta
    )
    self._logger.info(
        "Tablestore create system index[%s] successfully.", self._index_name
    )

```
 |  
| --- | --- |  
###  delete_table_if_exists [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tablestore/#llama_index.vector_stores.tablestore.TablestoreVectorStore.delete_table_if_exists "Permanent link")

```
delete_table_if_exists()

```

Delete table if exists.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tablestore/llama_index/vector_stores/tablestore/base.py`  
| 
```
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
```
 | 
```
defdelete_table_if_exists(self):
"""Delete table if exists."""
    search_index_list = self._tablestore_client.list_search_index(
        table_name=self._table_name
    )
    for resp_tuple in search_index_list:
        self._tablestore_client.delete_search_index(resp_tuple[0], resp_tuple[1])
        self._logger.info(
            "Tablestore delete index[%s] successfully.", self._index_name
        )
    self._tablestore_client.delete_table(self._table_name)
    self._logger.info(
        "Tablestore delete system table[%s] successfully.", self._index_name
    )

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tablestore/#llama_index.vector_stores.tablestore.TablestoreVectorStore.add "Permanent link")

```
add(nodes: [], **kwargs: ) -> []

```

Add nodes to vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tablestore/llama_index/vector_stores/tablestore/base.py`  
| 
```
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
```
 | 
```
defadd(self, nodes: List[BaseNode], **kwargs: Any) -> List[str]:
"""Add nodes to vector store."""
    if len(nodes) == 0:
        return []
    ids = []
    for node in nodes:
        if len(node.get_embedding()) != self._vector_dimension:
            raise RuntimeError(
                "node embedding size:%d is not the same as vector store dim:%d"
                % (len(node.get_embedding()), self._vector_dimension)
            )
        self._write_row(
            row_id=node.node_id,
            content=node.text,
            embedding_vector=node.get_embedding(),
            metadata=node.metadata,
        )
        ids.append(node.node_id)
    return ids

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tablestore/#llama_index.vector_stores.tablestore.TablestoreVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Delete nodes from vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tablestore/llama_index/vector_stores/tablestore/base.py`  
| 
```
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
```
 | 
```
defdelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""Delete nodes from vector store."""
    if node_ids is None and filters is None:
        raise RuntimeError("node_ids and filters cannot be None at the same time.")
    if node_ids is not None and filters is not None:
        raise RuntimeError("node_ids and filters cannot be set at the same time.")
    if filters is not None:
        rows = self._filter(
            filters=filters, return_type=tablestore.ColumnReturnType.NONE
        )
        for row in rows:
            self._delete_row(row[0][0][1])
    if node_ids is not None:
        for node_id in node_ids:
            self._delete_row(node_id)

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tablestore/#llama_index.vector_stores.tablestore.TablestoreVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Get nodes from vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tablestore/llama_index/vector_stores/tablestore/base.py`  
| 
```
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
```
 | 
```
defget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> List[BaseNode]:
"""Get nodes from vector store."""
    if node_ids is None and filters is None:
        raise RuntimeError("node_ids and filters cannot be None at the same time.")
    if node_ids is not None and filters is not None:
        raise RuntimeError("node_ids and filters cannot be set at the same time.")
    if filters is not None:
        rows = self._filter(
            filters=filters, return_type=tablestore.ColumnReturnType.ALL
        )
        return self._to_get_nodes_result(rows)
    if node_ids is not None:
        nodes = []
        for node_id in node_ids:
            nodes.append(self._get_row(node_id))
        return nodes
    return []

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tablestore/#llama_index.vector_stores.tablestore.TablestoreVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tablestore/llama_index/vector_stores/tablestore/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""Delete nodes using with ref_doc_id."""
    rows = self._filter(
        filters=MetadataFilters(
            filters=[
                MetadataFilter(
                    key=self._ref_doc_id_field,
                    value=ref_doc_id,
                    operator=FilterOperator.EQ,
                ),
            ],
            condition=FilterCondition.AND,
        ),
        return_type=tablestore.ColumnReturnType.NONE,
    )
    for row in rows:
        self._delete_row(row[0][0][1])

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tablestore/#llama_index.vector_stores.tablestore.TablestoreVectorStore.clear "Permanent link")

```
clear() -> None

```

Clear all nodes from configured vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tablestore/llama_index/vector_stores/tablestore/base.py`  
| 
```
784
785
786
```
 | 
```
defclear(self) -> None:
"""Clear all nodes from configured vector store."""
    self._delete_all()

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tablestore/#llama_index.vector_stores.tablestore.TablestoreVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tablestore/llama_index/vector_stores/tablestore/base.py`  
| 
```
788
789
790
791
792
793
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query vector store."""
    knn_top_k = query.similarity_top_k
    if "knn_top_k" in kwargs:
        knn_top_k = kwargs["knn_top_k"]
    return self._search(query=query, knn_top_k=knn_top_k)

```
 |  
| --- | --- |  
options: members: - TablestoreVectorStore
