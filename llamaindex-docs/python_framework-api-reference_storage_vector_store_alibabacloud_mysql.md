# Alibabacloud mysql
##  AlibabaCloudMySQLVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_mysql/#llama_index.vector_stores.alibabacloud_mysql.AlibabaCloudMySQLVectorStore "Permanent link")
Bases: 
Alibaba Cloud MySQL Vector Store.
Examples:

```
fromllama_index.vector_stores.alibabacloud_mysqlimport AlibabaCloudMySQLVectorStore

# Create AlibabaCloudMySQLVectorStore instance
vector_store = AlibabaCloudMySQLVectorStore(
    table_name="llama_index_vectorstore",
    host="localhost",
    port=3306,
    user="llamaindex",
    password="password",
    database="vectordb",
    embed_dim=1536,  # OpenAI embedding dimension
    default_m=6,
    distance_method="COSINE"
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-alibabacloud-mysql/llama_index/vector_stores/alibabacloud_mysql/base.py`  
| 
```
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
```
 | 
```
classAlibabaCloudMySQLVectorStore(BasePydanticVectorStore):
"""
    Alibaba Cloud MySQL Vector Store.

    Examples:
        ```python
        from llama_index.vector_stores.alibabacloud_mysql import AlibabaCloudMySQLVectorStore

        # Create AlibabaCloudMySQLVectorStore instance
        vector_store = AlibabaCloudMySQLVectorStore(
            table_name="llama_index_vectorstore",
            host="localhost",
            port=3306,
            user="llamaindex",
            password="password",
            database="vectordb",
            embed_dim=1536,  # OpenAI embedding dimension
            default_m=6,
            distance_method="COSINE"

        ```

    """

    stores_text: bool = True
    flat_metadata: bool = False

    connection_string: str
    table_name: str = "llama_index_table"
    database: str
    embed_dim: int = 1536
    default_m: int = 6
    distance_method: Literal["EUCLIDEAN", "COSINE"] = "COSINE"
    perform_setup: bool = True
    debug: bool = False

    _engine: Any = PrivateAttr()
    _async_engine: Any = PrivateAttr()
    _session: Any = PrivateAttr()
    _async_session: Any = PrivateAttr()
    _table_class: Any = PrivateAttr()
    _is_initialized: bool = PrivateAttr(default=False)

    def_validate_identifier(self, name: str) -> str:
        # 只允许字母、数字、下划线（符合 SQL 标识符规范）
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", name):
            raise ValueError(f"Invalid identifier: {name}")
        return name

    def_validate_positive_int(self, value: int, param_name: str) -> int:
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"Expected positive int for {param_name}, got {value}")
        return value

    def_validate_table_name(self, table_name: str) -> str:
        return self._validate_identifier(table_name)

    def__init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
        table_name: str = "llama_index_table",
        embed_dim: int = 1536,
        default_m: int = 6,
        distance_method: Literal["EUCLIDEAN", "COSINE"] = "COSINE",
        perform_setup: bool = True,
        debug: bool = False,
    ) -> None:
"""
        Constructor.

        Args:
            host (str): Host of Alibaba Cloud MySQL connection.
            port (int): Port of Alibaba Cloud MySQL connection.
            user (str): Alibaba Cloud MySQL username.
            password (str): Alibaba Cloud MySQL password.
            database (str): Alibaba Cloud MySQL DB name.
            table_name (str, optional): Table name for the vector store. Defaults to "llama_index_table".
            embed_dim (int, optional): Embedding dimensions. Defaults to 1536.
            default_m (int, optional): Default M value for the vector index. Defaults to 6.
            distance_method (Literal["EUCLIDEAN", "COSINE"], optional): Vector distance type. Defaults to COSINE.
            perform_setup (bool, optional): If DB should be set up. Defaults to True.
            debug (bool, optional): If debug logging should be enabled. Defaults to False.

        """
        # Validate table_name, embed_dim, and default_m
        self._validate_table_name(table_name)
        self._validate_positive_int(embed_dim, "embed_dim")
        self._validate_positive_int(default_m, "default_m")

        # Create connection string
        password_safe = quote_plus(password)
        connection_string = (
            f"mysql+pymysql://{user}:{password_safe}@{host}:{port}/{database}"
        )

        super().__init__(
            connection_string=connection_string,
            table_name=table_name,
            database=database,
            embed_dim=embed_dim,
            default_m=default_m,
            distance_method=distance_method,
            perform_setup=perform_setup,
            debug=debug,
        )

        # Private attrs
        self._engine = None
        self._async_engine = None
        self._session = None
        self._async_session = None
        self._table_class = None
        self._is_initialized = False

        self._initialize()

    @classmethod
    defclass_name(cls) -> str:
        return "AlibabaCloudMySQLVectorStore"

    @classmethod
    deffrom_params(
        cls,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
        table_name: str = "llama_index_table",
        embed_dim: int = 1536,
        default_m: int = 6,
        distance_method: Literal["EUCLIDEAN", "COSINE"] = "COSINE",
        perform_setup: bool = True,
        debug: bool = False,
    ) -> "AlibabaCloudMySQLVectorStore":
"""
        Construct from params.

        Args:
            host (str): Host of Alibaba Cloud MySQL connection.
            port (int): Port of Alibaba Cloud MySQL connection.
            user (str): Alibaba Cloud MySQL username.
            password (str): Alibaba Cloud MySQL password.
            database (str): Alibaba Cloud MySQL DB name.
            table_name (str, optional): Table name for the vector store. Defaults to "llama_index_table".
            embed_dim (int, optional): Embedding dimensions. Defaults to 1536.
            default_m (int, optional): Default M value for the vector index. Defaults to 6.
            distance_method (Literal["EUCLIDEAN", "COSINE"], optional): Vector distance type. Defaults to COSINE.
            perform_setup (bool, optional): If DB should be set up. Defaults to True.
            debug (bool, optional): If debug logging should be enabled. Defaults to False.

        Returns:
            AlibabaCloudMySQLVectorStore: Instance of AlibabaCloudMySQLVectorStore constructed from params.

        """
        return cls(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            table_name=table_name,
            embed_dim=embed_dim,
            default_m=default_m,
            distance_method=distance_method,
            perform_setup=perform_setup,
            debug=debug,
        )

    @property
    defclient(self) -> Any:
"""Return the SQLAlchemy engine."""
        if not self._is_initialized:
            return None
        return self._engine

    def_connect(self) -> None:
"""Create SQLAlchemy engines and sessions."""
        fromsqlalchemyimport create_engine
        fromsqlalchemy.ext.asyncioimport create_async_engine, AsyncSession
        fromsqlalchemy.ormimport sessionmaker

        # Create sync engine
        self._engine = create_engine(
            self.connection_string,
            echo=self.debug,
        )

        # Create async engine
        async_connection_string = self.connection_string.replace(
            "mysql+pymysql://", "mysql+aiomysql://"
        )
        self._async_engine = create_async_engine(
            async_connection_string,
            echo=self.debug,
        )

        # Create session makers
        self._session = sessionmaker(self._engine)
        self._async_session = sessionmaker(self._async_engine, class_=AsyncSession)

    def_check_vector_support(self) -> None:
"""Check if the MySQL server supports vector operations."""
        fromsqlalchemyimport text

        with self._session() as session:
            try:
                # Check MySQL version
                # Try to execute a simple vector function to verify support
                result = session.execute(
                    text("SELECT VEC_FromText('[1,2,3]') IS NOT NULL as vector_support")
                )
                vector_result = result.fetchone()
                if not vector_result or not vector_result[0]:
                    raise ValueError(
                        "RDS MySQL Vector functions are not available."
                        " Please ensure you're using RDS MySQL 8.0.36+ with Vector support."
                    )

                # Check rds_release_date >= 20251031
                result = session.execute(text("SHOW VARIABLES LIKE 'rds_release_date'"))
                rds_release_result = result.fetchone()

                if not rds_release_result:
                    raise ValueError(
                        "Unable to retrieve rds_release_date variable. "
                        "Your MySQL instance may not Alibaba Cloud RDS MySQL instance."
                    )

                rds_release_date = rds_release_result[1]
                if int(rds_release_date)  20251031:
                    raise ValueError(
                        f"Alibaba Cloud MySQL rds_release_date must be 20251031 or later, found: {rds_release_date}."
                    )

            except Exception as e:
                if "FUNCTION" in str(e) and "VEC_FromText" in str(e):
                    raise ValueError(
                        "RDS MySQL Vector functions are not available."
                        " Please ensure you're using RDS MySQL 8.0.36+ with Vector support."
                    ) frome
                raise

    def_create_table_if_not_exists(self) -> None:
        fromsqlalchemyimport text

        with self._session() as session:
            # Create table with VECTOR data type for Alibaba Cloud MySQL
            stmt = text(f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                id VARCHAR(36) PRIMARY KEY,
                node_id VARCHAR(255) NOT NULL,
                text LONGTEXT,
                metadata JSON,
                embedding VECTOR({self.embed_dim}) NOT NULL,
                INDEX `node_id_index` (node_id),
                VECTOR INDEX (embedding) M={self.default_m} DISTANCE={self.distance_method}
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
)
            session.execute(stmt)
            session.commit()

    def_initialize(self) -> None:
        if not self._is_initialized:
            self._connect()
            if self.perform_setup:
                self._check_vector_support()
                self._create_table_if_not_exists()
            self._is_initialized = True

    def_node_to_table_row(self, node: BaseNode) -> Dict[str, Any]:
        return {
            "node_id": node.node_id,
            "text": node.get_content(metadata_mode=MetadataMode.NONE),
            "embedding": node.get_embedding(),
            "metadata": node_to_metadata_dict(
                node,
                remove_text=True,
                flat_metadata=self.flat_metadata,
            ),
        }

    def_to_mysql_operator(self, operator: FilterOperator) -> str:
        if operator == FilterOperator.EQ:
            return "="
        elif operator == FilterOperator.GT:
            return ">"
        elif operator == FilterOperator.LT:
            return "<"
        elif operator == FilterOperator.NE:
            return "!="
        elif operator == FilterOperator.GTE:
            return ">="
        elif operator == FilterOperator.LTE:
            return "<="
        elif operator == FilterOperator.IN:
            return "IN"
        elif operator == FilterOperator.NIN:
            return "NOT IN"
        else:
            _logger.warning("Unsupported operator: %s, fallback to '='", operator)
            return "="

    def_build_filter_clause(
        self, filter_: MetadataFilter, global_param_counter: List[int]
    ) -> tuple[str, dict]:
        params = {}

        if filter_.operator in [FilterOperator.IN, FilterOperator.NIN]:
            # For IN/NIN operators, we need multiple placeholders
            placeholders = []
            for i in range(len(filter_.value)):
                param_name = f"param_{global_param_counter[0]}"
                global_param_counter[0] += 1
                placeholders.append(f":{param_name}")
                params[param_name] = filter_.value[i]
            filter_value = f"({','.join(placeholders)})"
        elif isinstance(filter_.value, (list, tuple)):
            # For list/tuple values, we also need multiple placeholders
            placeholders = []
            for i in range(len(filter_.value)):
                param_name = f"param_{global_param_counter[0]}"
                global_param_counter[0] += 1
                placeholders.append(f":{param_name}")
                params[param_name] = filter_.value[i]
            filter_value = f"({','.join(placeholders)})"
        else:
            # For single value, create a single parameter
            param_name = f"param_{global_param_counter[0]}"
            global_param_counter[0] += 1
            filter_value = f":{param_name}"
            params[param_name] = filter_.value

        clause = f"JSON_VALUE(metadata, '$.{filter_.key}') {self._to_mysql_operator(filter_.operator)}{filter_value}"
        return clause, params

    def_filters_to_where_clause(
        self, filters: MetadataFilters, global_param_counter: List[int]
    ) -> tuple[str, dict]:
        conditions = {
            FilterCondition.OR: "OR",
            FilterCondition.AND: "AND",
        }
        if filters.condition not in conditions:
            raise ValueError(
                f"Unsupported condition: {filters.condition}. "
                f"Must be one of {list(conditions.keys())}"
            )

        clauses: List[str] = []
        all_params = {}

        for filter_ in filters.filters:
            if isinstance(filter_, MetadataFilter):
                clause, filter_params = self._build_filter_clause(
                    filter_, global_param_counter
                )
                clauses.append(clause)
                all_params.update(filter_params)
                continue

            if isinstance(filter_, MetadataFilters):
                subclause, subparams = self._filters_to_where_clause(
                    filter_, global_param_counter
                )
                if subclause:
                    clauses.append(f"({subclause})")
                    all_params.update(subparams)
                continue

            raise ValueError(
                f"Unsupported filter type: {type(filter_)}. Must be one of {MetadataFilter}, {MetadataFilters}"
            )

        return f" {conditions[filters.condition]} ".join(clauses), all_params

    def_db_rows_to_query_result(
        self, rows: List[DBEmbeddingRow]
    ) -> VectorStoreQueryResult:
        nodes = []
        similarities = []
        ids = []
        for db_embedding_row in rows:
            node = metadata_dict_to_node(db_embedding_row.metadata)
            node.set_content(str(db_embedding_row.text))

            similarities.append(db_embedding_row.similarity)
            ids.append(db_embedding_row.node_id)
            nodes.append(node)

        return VectorStoreQueryResult(
            nodes=nodes,
            similarities=similarities,
            ids=ids,
        )

    defget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> List[BaseNode]:
"""Get nodes from vector store."""
        self._initialize()

        nodes: List[BaseNode] = []
        with self._session() as session:
            if node_ids:
                # Using parameterized query to prevent SQL injection
                placeholders = ",".join([f":node_id_{i}" for i in range(len(node_ids))])
                params = {f"node_id_{i}": node_id for i, node_id in enumerate(node_ids)}
                stmt = sqlalchemy.text(
                    f"""SELECT text, metadata FROM `{self.table_name}` WHERE node_id IN ({placeholders})"""
                )
                result = session.execute(stmt, params)
            else:
                stmt = sqlalchemy.text(
                    f"""SELECT text, metadata FROM `{self.table_name}`"""
                )
                result = session.execute(stmt)

            for item in result:
                node = metadata_dict_to_node(
                    json.loads(item[1]) if isinstance(item[1], str) else item[1]
                )
                node.set_content(str(item[0]))
                nodes.append(node)

        return nodes

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
        self._initialize()

        ids = []
        with self._session() as session:
            for node in nodes:
                ids.append(node.node_id)
                item = self._node_to_table_row(node)

                stmt = sqlalchemy.text(f"""
                INSERT INTO `{self.table_name}` (id, node_id, text, embedding, metadata)
                VALUES (
                    UUID(),
                    :node_id,
                    :text,
                    VEC_FromText(:embedding),
                    :metadata

                ON DUPLICATE KEY UPDATE
                    text = VALUES(text),
                    embedding = VALUES(embedding),
                    metadata = VALUES(metadata)
)

                session.execute(
                    stmt,
                    {
                        "node_id": item["node_id"],
                        "text": item["text"],
                        "embedding": json.dumps(item["embedding"]),
                        "metadata": json.dumps(item["metadata"]),
                    },
                )
            session.commit()

        return ids

    async defasync_add(
        self,
        nodes: Sequence[BaseNode],
        **kwargs: Any,
    ) -> List[str]:
"""
        Async wrapper around :meth:`add`.
        """
        self._initialize()

        if not nodes:
            return []

        ids: List[str] = []
        async with self._async_session() as session:
            for node in nodes:
                ids.append(node.node_id)
                item = self._node_to_table_row(node)

                stmt = sqlalchemy.text(f"""
                INSERT INTO `{self.table_name}` (id, node_id, text, embedding, metadata)
                VALUES (
                    UUID(),
                    :node_id,
                    :text,
                    VEC_FromText(:embedding),
                    :metadata

                ON DUPLICATE KEY UPDATE
                    text = VALUES(text),
                    embedding = VALUES(embedding),
                    metadata = VALUES(metadata)
)

                await session.execute(
                    stmt,
                    {
                        "node_id": item["node_id"],
                        "text": item["text"],
                        "embedding": json.dumps(item["embedding"]),
                        "metadata": json.dumps(item["metadata"]),
                    },
                )
            await session.commit()

        return ids

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        if query.mode != VectorStoreQueryMode.DEFAULT:
            raise NotImplementedError(f"Query mode {query.mode} not available.")

        self._initialize()

        # Using specified distance function for vector similarity search
        distance_func = (
            "VEC_DISTANCE_COSINE"
            if self.distance_method == "COSINE"
            else "VEC_DISTANCE_EUCLIDEAN"
        )

        where_clause = ""
        params = {
            "query_embedding": json.dumps(query.query_embedding),
            "limit": query.similarity_top_k,
        }

        if query.filters:
            # Use a global counter to ensure unique parameter names
            global_param_counter = [0]  # Use a list to make it mutable
            where_clause, filter_params = self._filters_to_where_clause(
                query.filters, global_param_counter
            )
            where_clause = f"WHERE {where_clause}"
            params.update(filter_params)

        stmt = sqlalchemy.text(f"""
        SELECT
            node_id,
            text,
            embedding,
            metadata,
{distance_func}(embedding, VEC_FromText(:query_embedding)) AS distance
        FROM `{self.table_name}`
{where_clause}
        ORDER BY distance
        LIMIT :limit
        """)

        with self._session() as session:
            result = session.execute(stmt, params)
            results = result.fetchall()

        rows = []
        for item in results:
            rows.append(
                DBEmbeddingRow(
                    node_id=item[0],
                    text=item[1],
                    metadata=json.loads(item[3])
                    if isinstance(item[3], str)
                    else item[3],
                    similarity=(1 - item[4]) if item[4] is not None else 0,
                )
            )

        return self._db_rows_to_query_result(rows)

    async defaquery(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
"""Async wrapper around :meth:`query`."""
        if query.mode != VectorStoreQueryMode.DEFAULT:
            raise NotImplementedError(f"Query mode {query.mode} not available.")

        self._initialize()

        # Using specified distance function for vector similarity search
        distance_func = (
            "VEC_DISTANCE_COSINE"
            if self.distance_method == "COSINE"
            else "VEC_DISTANCE_EUCLIDEAN"
        )

        where_clause = ""
        params = {
            "query_embedding": json.dumps(query.query_embedding),
            "limit": query.similarity_top_k,
        }

        if query.filters:
            # Use a global counter to ensure unique parameter names
            global_param_counter = [0]  # Use a list to make it mutable
            where_clause, filter_params = self._filters_to_where_clause(
                query.filters, global_param_counter
            )
            where_clause = f"WHERE {where_clause}"
            params.update(filter_params)

        stmt = sqlalchemy.text(f"""
        SELECT
            node_id,
            text,
            embedding,
            metadata,
{distance_func}(embedding, VEC_FromText(:query_embedding)) AS distance
        FROM `{self.table_name}`
{where_clause}
        ORDER BY distance
        LIMIT :limit
        """)

        async with self._async_session() as session:
            result = await session.execute(stmt, params)
            results = result.fetchall()

        rows = []
        for item in results:
            rows.append(
                DBEmbeddingRow(
                    node_id=item[0],
                    text=item[1],
                    metadata=json.loads(item[3])
                    if isinstance(item[3], str)
                    else item[3],
                    similarity=(1 - item[4]) if item[4] is not None else 0,
                )
            )

        return self._db_rows_to_query_result(rows)

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        self._initialize()

        with self._session() as session:
            # Delete based on ref_doc_id in metadata
            stmt = sqlalchemy.text(
                f"""DELETE FROM `{self.table_name}` WHERE JSON_EXTRACT(metadata, '$.ref_doc_id') = :doc_id"""
            )
            session.execute(stmt, {"doc_id": ref_doc_id})
            session.commit()

    async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""Async wrapper around :meth:`delete`."""
        self._initialize()

        async with self._async_session() as session:
            # Delete based on ref_doc_id in metadata
            stmt = sqlalchemy.text(
                f"""DELETE FROM `{self.table_name}` WHERE JSON_EXTRACT(metadata, '$.ref_doc_id') = :doc_id"""
            )
            await session.execute(stmt, {"doc_id": ref_doc_id})
            await session.commit()

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
        self._initialize()

        with self._session() as session:
            if node_ids:
                # Using parameterized query to prevent SQL injection
                placeholders = ",".join([f":node_id_{i}" for i in range(len(node_ids))])
                params = {f"node_id_{i}": node_id for i, node_id in enumerate(node_ids)}
                stmt = sqlalchemy.text(
                    f"""DELETE FROM `{self.table_name}` WHERE node_id IN ({placeholders})"""
                )
                session.execute(stmt, params)
                session.commit()

    async defadelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""Async wrapper around :meth:`delete_nodes`."""
        self._initialize()

        async with self._async_session() as session:
            if node_ids:
                # Using parameterized query to prevent SQL injection
                placeholders = ",".join([f":node_id_{i}" for i in range(len(node_ids))])
                params = {f"node_id_{i}": node_id for i, node_id in enumerate(node_ids)}
                stmt = sqlalchemy.text(
                    f"""DELETE FROM `{self.table_name}` WHERE node_id IN ({placeholders})"""
                )
                await session.execute(stmt, params)
                await session.commit()

    defcount(self) -> int:
        self._initialize()

        with self._session() as session:
            stmt = sqlalchemy.text(
                f"""SELECT COUNT(*) as count FROM `{self.table_name}`"""
            )
            result = session.execute(stmt)
            row = result.fetchone()

        return row[0] if row else 0

    defdrop(self) -> None:
        self._initialize()

        with self._session() as session:
            stmt = sqlalchemy.text(f"""DROP TABLE IF EXISTS `{self.table_name}`""")
            session.execute(stmt)
            session.commit()

        self.close()

    defclear(self) -> None:
        self._initialize()

        with self._session() as session:
            stmt = sqlalchemy.text(f"""DELETE FROM `{self.table_name}`""")
            session.execute(stmt)
            session.commit()

    async defaclear(self) -> None:
"""Async wrapper around :meth:`clear`."""
        self._initialize()

        async with self._async_session() as session:
            stmt = sqlalchemy.text(f"""DELETE FROM `{self.table_name}`""")
            await session.execute(stmt)
            await session.commit()

    defclose(self) -> None:
        if not self._is_initialized:
            return
        if self._engine:
            self._engine.dispose()
        if self._async_engine:
            importasyncio

            try:
                # Try to run the async disposal
                loop = asyncio.get_event_loop()
                if not loop.is_running():
                    asyncio.run(self._async_engine.dispose())
                else:
                    # If already in a running loop, create a new thread to run the disposal
                    importconcurrent.futures

                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(
                            asyncio.run, self._async_engine.dispose()
                        )
                        future.result()
            except RuntimeError:
                # If no event loop exists, create one
                asyncio.run(self._async_engine.dispose())
        self._is_initialized = False

    async defaclose(self) -> None:
        if not self._is_initialized:
            return
        if self._engine:
            self._engine.dispose()
        if self._async_engine:
            await self._async_engine.dispose()
        self._is_initialized = False

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_mysql/#llama_index.vector_stores.alibabacloud_mysql.AlibabaCloudMySQLVectorStore.client "Permanent link")

```
client: 

```

Return the SQLAlchemy engine.
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_mysql/#llama_index.vector_stores.alibabacloud_mysql.AlibabaCloudMySQLVectorStore.from_params "Permanent link")

```
from_params(
    host: ,
    port: ,
    user: ,
    password: ,
    database: ,
    table_name:  = "llama_index_table",
    embed_dim:  = 1536,
    default_m:  = 6,
    distance_method: Literal[
        "EUCLIDEAN", "COSINE"
    ] = "COSINE",
    perform_setup:  = True,
    debug:  = False,
) -> 

```

Construct from params.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `host`  |  Host of Alibaba Cloud MySQL connection.  |  _required_  |  
|  `port`  |  Port of Alibaba Cloud MySQL connection.  |  _required_  |  
|  `user`  |  Alibaba Cloud MySQL username.  |  _required_  |  
|  `password`  |  Alibaba Cloud MySQL password.  |  _required_  |  
|  `database`  |  Alibaba Cloud MySQL DB name.  |  _required_  |  
|  `table_name`  |  Table name for the vector store. Defaults to "llama_index_table".  |  `'llama_index_table'`  |  
|  `embed_dim`  |  Embedding dimensions. Defaults to 1536.  |  `1536`  |  
|  `default_m`  |  Default M value for the vector index. Defaults to 6.  |  
|  `distance_method`  |  `Literal['EUCLIDEAN', 'COSINE']`  |  Vector distance type. Defaults to COSINE.  |  `'COSINE'`  |  
|  `perform_setup`  |  `bool`  |  If DB should be set up. Defaults to True.  |  `True`  |  
|  `debug`  |  `bool`  |  If debug logging should be enabled. Defaults to False.  |  `False`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `AlibabaCloudMySQLVectorStore`  |   |  Instance of AlibabaCloudMySQLVectorStore constructed from params.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-alibabacloud-mysql/llama_index/vector_stores/alibabacloud_mysql/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_params(
    cls,
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
    table_name: str = "llama_index_table",
    embed_dim: int = 1536,
    default_m: int = 6,
    distance_method: Literal["EUCLIDEAN", "COSINE"] = "COSINE",
    perform_setup: bool = True,
    debug: bool = False,
) -> "AlibabaCloudMySQLVectorStore":
"""
    Construct from params.

    Args:
        host (str): Host of Alibaba Cloud MySQL connection.
        port (int): Port of Alibaba Cloud MySQL connection.
        user (str): Alibaba Cloud MySQL username.
        password (str): Alibaba Cloud MySQL password.
        database (str): Alibaba Cloud MySQL DB name.
        table_name (str, optional): Table name for the vector store. Defaults to "llama_index_table".
        embed_dim (int, optional): Embedding dimensions. Defaults to 1536.
        default_m (int, optional): Default M value for the vector index. Defaults to 6.
        distance_method (Literal["EUCLIDEAN", "COSINE"], optional): Vector distance type. Defaults to COSINE.
        perform_setup (bool, optional): If DB should be set up. Defaults to True.
        debug (bool, optional): If debug logging should be enabled. Defaults to False.

    Returns:
        AlibabaCloudMySQLVectorStore: Instance of AlibabaCloudMySQLVectorStore constructed from params.

    """
    return cls(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        table_name=table_name,
        embed_dim=embed_dim,
        default_m=default_m,
        distance_method=distance_method,
        perform_setup=perform_setup,
        debug=debug,
    )

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_mysql/#llama_index.vector_stores.alibabacloud_mysql.AlibabaCloudMySQLVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Get nodes from vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-alibabacloud-mysql/llama_index/vector_stores/alibabacloud_mysql/base.py`  
| 
```
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
```
 | 
```
defget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> List[BaseNode]:
"""Get nodes from vector store."""
    self._initialize()

    nodes: List[BaseNode] = []
    with self._session() as session:
        if node_ids:
            # Using parameterized query to prevent SQL injection
            placeholders = ",".join([f":node_id_{i}" for i in range(len(node_ids))])
            params = {f"node_id_{i}": node_id for i, node_id in enumerate(node_ids)}
            stmt = sqlalchemy.text(
                f"""SELECT text, metadata FROM `{self.table_name}` WHERE node_id IN ({placeholders})"""
            )
            result = session.execute(stmt, params)
        else:
            stmt = sqlalchemy.text(
                f"""SELECT text, metadata FROM `{self.table_name}`"""
            )
            result = session.execute(stmt)

        for item in result:
            node = metadata_dict_to_node(
                json.loads(item[1]) if isinstance(item[1], str) else item[1]
            )
            node.set_content(str(item[0]))
            nodes.append(node)

    return nodes

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_mysql/#llama_index.vector_stores.alibabacloud_mysql.AlibabaCloudMySQLVectorStore.async_add "Permanent link")

```
async_add(
    nodes: Sequence[], **kwargs: 
) -> []

```

Async wrapper around :meth:`add`.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-alibabacloud-mysql/llama_index/vector_stores/alibabacloud_mysql/base.py`  
| 
```
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
```
 | 
```
async defasync_add(
    self,
    nodes: Sequence[BaseNode],
    **kwargs: Any,
) -> List[str]:
"""
    Async wrapper around :meth:`add`.
    """
    self._initialize()

    if not nodes:
        return []

    ids: List[str] = []
    async with self._async_session() as session:
        for node in nodes:
            ids.append(node.node_id)
            item = self._node_to_table_row(node)

            stmt = sqlalchemy.text(f"""
            INSERT INTO `{self.table_name}` (id, node_id, text, embedding, metadata)
            VALUES (
                UUID(),
                :node_id,
                :text,
                VEC_FromText(:embedding),
                :metadata

            ON DUPLICATE KEY UPDATE
                text = VALUES(text),
                embedding = VALUES(embedding),
                metadata = VALUES(metadata)
)

            await session.execute(
                stmt,
                {
                    "node_id": item["node_id"],
                    "text": item["text"],
                    "embedding": json.dumps(item["embedding"]),
                    "metadata": json.dumps(item["metadata"]),
                },
            )
        await session.commit()

    return ids

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_mysql/#llama_index.vector_stores.alibabacloud_mysql.AlibabaCloudMySQLVectorStore.aquery "Permanent link")

```
aquery(
    query: , **kwargs: 
) -> 

```

Async wrapper around :meth:`query`.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-alibabacloud-mysql/llama_index/vector_stores/alibabacloud_mysql/base.py`  
| 
```
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
```
 | 
```
async defaquery(
    self, query: VectorStoreQuery, **kwargs: Any
) -> VectorStoreQueryResult:
"""Async wrapper around :meth:`query`."""
    if query.mode != VectorStoreQueryMode.DEFAULT:
        raise NotImplementedError(f"Query mode {query.mode} not available.")

    self._initialize()

    # Using specified distance function for vector similarity search
    distance_func = (
        "VEC_DISTANCE_COSINE"
        if self.distance_method == "COSINE"
        else "VEC_DISTANCE_EUCLIDEAN"
    )

    where_clause = ""
    params = {
        "query_embedding": json.dumps(query.query_embedding),
        "limit": query.similarity_top_k,
    }

    if query.filters:
        # Use a global counter to ensure unique parameter names
        global_param_counter = [0]  # Use a list to make it mutable
        where_clause, filter_params = self._filters_to_where_clause(
            query.filters, global_param_counter
        )
        where_clause = f"WHERE {where_clause}"
        params.update(filter_params)

    stmt = sqlalchemy.text(f"""
    SELECT
        node_id,
        text,
        embedding,
        metadata,
{distance_func}(embedding, VEC_FromText(:query_embedding)) AS distance
    FROM `{self.table_name}`
{where_clause}
    ORDER BY distance
    LIMIT :limit
    """)

    async with self._async_session() as session:
        result = await session.execute(stmt, params)
        results = result.fetchall()

    rows = []
    for item in results:
        rows.append(
            DBEmbeddingRow(
                node_id=item[0],
                text=item[1],
                metadata=json.loads(item[3])
                if isinstance(item[3], str)
                else item[3],
                similarity=(1 - item[4]) if item[4] is not None else 0,
            )
        )

    return self._db_rows_to_query_result(rows)

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_mysql/#llama_index.vector_stores.alibabacloud_mysql.AlibabaCloudMySQLVectorStore.adelete "Permanent link")

```
adelete(ref_doc_id: , **delete_kwargs: ) -> None

```

Async wrapper around :meth:`delete`.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-alibabacloud-mysql/llama_index/vector_stores/alibabacloud_mysql/base.py`  
| 
```
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
async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""Async wrapper around :meth:`delete`."""
    self._initialize()

    async with self._async_session() as session:
        # Delete based on ref_doc_id in metadata
        stmt = sqlalchemy.text(
            f"""DELETE FROM `{self.table_name}` WHERE JSON_EXTRACT(metadata, '$.ref_doc_id') = :doc_id"""
        )
        await session.execute(stmt, {"doc_id": ref_doc_id})
        await session.commit()

```
 |  
| --- | --- |  
###  adelete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_mysql/#llama_index.vector_stores.alibabacloud_mysql.AlibabaCloudMySQLVectorStore.adelete_nodes "Permanent link")

```
adelete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Async wrapper around :meth:`delete_nodes`.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-alibabacloud-mysql/llama_index/vector_stores/alibabacloud_mysql/base.py`  
| 
```
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
```
 | 
```
async defadelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""Async wrapper around :meth:`delete_nodes`."""
    self._initialize()

    async with self._async_session() as session:
        if node_ids:
            # Using parameterized query to prevent SQL injection
            placeholders = ",".join([f":node_id_{i}" for i in range(len(node_ids))])
            params = {f"node_id_{i}": node_id for i, node_id in enumerate(node_ids)}
            stmt = sqlalchemy.text(
                f"""DELETE FROM `{self.table_name}` WHERE node_id IN ({placeholders})"""
            )
            await session.execute(stmt, params)
            await session.commit()

```
 |  
| --- | --- |  
###  aclear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_mysql/#llama_index.vector_stores.alibabacloud_mysql.AlibabaCloudMySQLVectorStore.aclear "Permanent link")

```
aclear() -> None

```

Async wrapper around :meth:`clear`.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-alibabacloud-mysql/llama_index/vector_stores/alibabacloud_mysql/base.py`  
| 
```
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
async defaclear(self) -> None:
"""Async wrapper around :meth:`clear`."""
    self._initialize()

    async with self._async_session() as session:
        stmt = sqlalchemy.text(f"""DELETE FROM `{self.table_name}`""")
        await session.execute(stmt)
        await session.commit()

```
 |  
| --- | --- |  
options: members: - AlibabaCloudMySQLVectorStore
