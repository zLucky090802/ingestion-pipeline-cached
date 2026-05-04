# Lantern
##  LanternVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/lantern/#llama_index.vector_stores.lantern.LanternVectorStore "Permanent link")
Bases: 
Latern vector store.
Examples:
`pip install llama-index-vector-stores-lantern`

```
fromllama_index.vector_stores.lanternimport LanternVectorStore

# Set up connection details
connection_string = "postgresql://postgres:postgres@localhost:5432"
db_name = "postgres"
url = make_url(connection_string)

# Create an instance of LanternVectorStore
vector_store = LanternVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name="your_table_name",
    embed_dim=1536,  # openai embedding dimension
    m=16,  # HNSW M parameter
    ef_construction=128,  # HNSW ef construction parameter
    ef=64,  # HNSW ef search parameter
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-lantern/llama_index/vector_stores/lantern/base.py`  
| 
```
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
```
 | 
```
classLanternVectorStore(BasePydanticVectorStore):
"""
    Latern vector store.

    Examples:
        `pip install llama-index-vector-stores-lantern`

        ```python
        from llama_index.vector_stores.lantern import LanternVectorStore

        # Set up connection details
        connection_string = "postgresql://postgres:postgres@localhost:5432"
        db_name = "postgres"
        url = make_url(connection_string)

        # Create an instance of LanternVectorStore
        vector_store = LanternVectorStore.from_params(
            database=db_name,
            host=url.host,
            password=url.password,
            port=url.port,
            user=url.username,
            table_name="your_table_name",
            embed_dim=1536,  # openai embedding dimension
            m=16,  # HNSW M parameter
            ef_construction=128,  # HNSW ef construction parameter
            ef=64,  # HNSW ef search parameter

        ```

    """

    stores_text: bool = True
    flat_metadata: bool = False

    connection_string: str
    async_connection_string: str
    table_name: str
    schema_name: str
    embed_dim: int
    hybrid_search: bool
    text_search_config: str
    cache_ok: bool
    perform_setup: bool
    debug: bool

    _base: Any = PrivateAttr()
    _table_class: Any = PrivateAttr()
    _engine: Any = PrivateAttr()
    _session: Any = PrivateAttr()
    _async_engine: Any = PrivateAttr()
    _async_session: Any = PrivateAttr()
    _is_initialized: bool = PrivateAttr(default=False)

    def__init__(
        self,
        connection_string: str,
        async_connection_string: str,
        table_name: str,
        schema_name: str,
        hybrid_search: bool = False,
        text_search_config: str = "english",
        embed_dim: int = 1536,
        m: int = 16,
        ef_construction: int = 128,
        ef: int = 64,
        cache_ok: bool = False,
        perform_setup: bool = True,
        debug: bool = False,
    ) -> None:
        table_name = table_name.lower()
        schema_name = schema_name.lower()

        if hybrid_search and text_search_config is None:
            raise ValueError(
                "Sparse vector index creation requires "
                "a text search configuration specification."
            )

        fromsqlalchemy.ormimport declarative_base

        super().__init__(
            connection_string=connection_string,
            async_connection_string=async_connection_string,
            table_name=table_name,
            schema_name=schema_name,
            hybrid_search=hybrid_search,
            text_search_config=text_search_config,
            embed_dim=embed_dim,
            cache_ok=cache_ok,
            perform_setup=perform_setup,
            debug=debug,
        )

        # sqlalchemy model
        self._base = declarative_base()
        self._table_class = get_data_model(
            self._base,
            table_name,
            schema_name,
            hybrid_search,
            text_search_config,
            cache_ok,
            embed_dim=embed_dim,
            m=m,
            ef_construction=ef_construction,
            ef=ef,
        )

    async defclose(self) -> None:
        if not self._is_initialized:
            return

        if self._engine:
            self._engine.dispose()
        if self._async_engine:
            await self._async_engine.dispose()

    @classmethod
    defclass_name(cls) -> str:
        return "LanternStore"

    @classmethod
    deffrom_params(
        cls,
        host: Optional[str] = None,
        port: Optional[str] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        table_name: str = "llamaindex",
        schema_name: str = "public",
        connection_string: Optional[str] = None,
        async_connection_string: Optional[str] = None,
        hybrid_search: bool = False,
        text_search_config: str = "english",
        embed_dim: int = 1536,
        m: int = 16,
        ef_construction: int = 128,
        ef: int = 64,
        cache_ok: bool = False,
        perform_setup: bool = True,
        debug: bool = False,
    ) -> "LanternVectorStore":
"""Return connection string from database parameters."""
        conn_str = (
            connection_string
            or f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        )
        async_conn_str = async_connection_string or (
            f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
        )
        return cls(
            connection_string=conn_str,
            async_connection_string=async_conn_str,
            table_name=table_name,
            schema_name=schema_name,
            hybrid_search=hybrid_search,
            text_search_config=text_search_config,
            embed_dim=embed_dim,
            m=m,
            ef_construction=ef_construction,
            ef=ef,
            cache_ok=cache_ok,
            perform_setup=perform_setup,
            debug=debug,
        )

    @property
    defclient(self) -> Any:
        if not self._is_initialized:
            return None
        return self._engine

    def_connect(self) -> Any:
        fromsqlalchemyimport create_engine
        fromsqlalchemy.ext.asyncioimport AsyncSession, create_async_engine
        fromsqlalchemy.ormimport sessionmaker

        self._engine = create_engine(self.connection_string, echo=self.debug)
        self._session = sessionmaker(self._engine)

        self._async_engine = create_async_engine(self.async_connection_string)
        self._async_session = sessionmaker(self._async_engine, class_=AsyncSession)  # type: ignore

    def_create_schema_if_not_exists(self) -> None:
        with self._session() as session, session.begin():
            fromsqlalchemyimport text

            statement = text(f"CREATE SCHEMA IF NOT EXISTS {self.schema_name}")
            session.execute(statement)
            session.commit()

    def_create_tables_if_not_exists(self) -> None:
        with self._session() as session, session.begin():
            self._base.metadata.create_all(session.connection())

    def_create_extension(self) -> None:
        importsqlalchemy

        with self._session() as session, session.begin():
            statement = sqlalchemy.text("CREATE EXTENSION IF NOT EXISTS lantern")
            session.execute(statement)
            session.commit()

    def_initialize(self) -> None:
        if not self._is_initialized:
            self._connect()
            if self.perform_setup:
                self._create_extension()
                self._create_schema_if_not_exists()
                self._create_tables_if_not_exists()
            self._is_initialized = True

    def_node_to_table_row(self, node: BaseNode) -> Any:
        return self._table_class(
            node_id=node.node_id,
            embedding=node.get_embedding(),
            text=node.get_content(metadata_mode=MetadataMode.NONE),
            metadata_=node_to_metadata_dict(
                node,
                remove_text=True,
                flat_metadata=self.flat_metadata,
            ),
        )

    defadd(self, nodes: List[BaseNode]) -> List[str]:
        self._initialize()
        ids = []
        with self._session() as session, session.begin():
            for node in nodes:
                ids.append(node.node_id)
                item = self._node_to_table_row(node)
                session.add(item)
            session.commit()
        return ids

    async defasync_add(self, nodes: List[BaseNode], **kwargs: Any) -> List[str]:
        self._initialize()
        ids = []
        async with self._async_session() as session, session.begin():
            for node in nodes:
                ids.append(node.node_id)
                item = self._node_to_table_row(node)
                session.add(item)
            await session.commit()
        return ids

    def_apply_filters_and_limit(
        self,
        stmt: "Select",
        limit: int,
        metadata_filters: Optional[MetadataFilters] = None,
    ) -> Any:
        importsqlalchemy

        if metadata_filters:
            for filter_ in metadata_filters.legacy_filters():
                bind_parameter = f"value_{filter_.key}"
                stmt = stmt.where(  # type: ignore
                    sqlalchemy.text(f"metadata_->>'{filter_.key}' = :{bind_parameter}")
                )
                stmt = stmt.params(  # type: ignore
                    **{bind_parameter: str(filter_.value)}
                )
        return stmt.limit(limit)  # type: ignore

    def_build_query(
        self,
        embedding: Optional[List[float]],
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
    ) -> Any:
        fromsqlalchemyimport func, select

        stmt = select(  # type: ignore
            self._table_class,
            func.cos_dist(self._table_class.embedding, embedding),
        ).order_by(self._table_class.embedding.op("<=>")(embedding))

        return self._apply_filters_and_limit(stmt, limit, metadata_filters)

    def_prepare_query(self, session: Any, limit: int) -> None:
        fromsqlalchemyimport text

        session.execute(text("SET enable_seqscan=OFF"))  # always use index
        session.execute(text(f"SET hnsw.init_k={limit}"))  # always use index

    async def_aprepare_query(self, session: Any, limit: int) -> None:
        fromsqlalchemyimport text

        await session.execute(text("SET enable_seqscan=OFF"))  # always use index
        await session.execute(text(f"SET hnsw.init_k={limit}"))  # always use index

    def_query_with_score(
        self,
        embedding: Optional[List[float]],
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
    ) -> List[DBEmbeddingRow]:
        stmt = self._build_query(embedding, limit, metadata_filters)
        with self._session() as session, session.begin():
            self._prepare_query(session, limit)
            res = session.execute(
                stmt,
            )
            return [
                DBEmbeddingRow(
                    node_id=item.node_id,
                    text=item.text,
                    metadata=item.metadata_,
                    similarity=(1 - distance) if distance is not None else 0,
                )
                for item, distance in res.all()
            ]

    async def_aquery_with_score(
        self,
        embedding: Optional[List[float]],
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
    ) -> List[DBEmbeddingRow]:
        stmt = self._build_query(embedding, limit, metadata_filters)
        async with self._async_session() as async_session, async_session.begin():
            await self._aprepare_query(async_session, limit)
            res = await async_session.execute(stmt)
            return [
                DBEmbeddingRow(
                    node_id=item.node_id,
                    text=item.text,
                    metadata=item.metadata_,
                    similarity=(1 - distance) if distance is not None else 0,
                )
                for item, distance in res.all()
            ]

    def_build_sparse_query(
        self,
        query_str: Optional[str],
        limit: int,
        metadata_filters: Optional[MetadataFilters] = None,
    ) -> Any:
        fromsqlalchemyimport select, type_coerce
        fromsqlalchemy.sqlimport func, text
        fromsqlalchemy.typesimport UserDefinedType

        classREGCONFIG(UserDefinedType):
            # The TypeDecorator.cache_ok class-level flag indicates if this custom TypeDecorator is safe to be used as part of a cache key.
            # If the TypeDecorator is not guaranteed to produce the same bind/result behavior and SQL generation every time,
            # this flag should be set to False; otherwise if the class produces the same behavior each time, it may be set to True.
            cache_ok = True

            defget_col_spec(self, **kw: Any) -> str:
                return "regconfig"

        if query_str is None:
            raise ValueError("query_str must be specified for a sparse vector query.")

        ts_query = func.plainto_tsquery(
            type_coerce(self.text_search_config, REGCONFIG), query_str
        )
        stmt = (
            select(  # type: ignore
                self._table_class,
                func.ts_rank(self._table_class.text_search_tsv, ts_query).label("rank"),
            )
            .where(self._table_class.text_search_tsv.op("@@")(ts_query))
            .order_by(text("rank desc"))
        )

        # type: ignore
        return self._apply_filters_and_limit(stmt, limit, metadata_filters)

    async def_async_sparse_query_with_rank(
        self,
        query_str: Optional[str] = None,
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
    ) -> List[DBEmbeddingRow]:
        stmt = self._build_sparse_query(query_str, limit, metadata_filters)
        async with self._async_session() as async_session, async_session.begin():
            res = await async_session.execute(stmt)
            return [
                DBEmbeddingRow(
                    node_id=item.node_id,
                    text=item.text,
                    metadata=item.metadata_,
                    similarity=rank,
                )
                for item, rank in res.all()
            ]

    def_sparse_query_with_rank(
        self,
        query_str: Optional[str] = None,
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
    ) -> List[DBEmbeddingRow]:
        stmt = self._build_sparse_query(query_str, limit, metadata_filters)
        with self._session() as session, session.begin():
            res = session.execute(stmt)
            return [
                DBEmbeddingRow(
                    node_id=item.node_id,
                    text=item.text,
                    metadata=item.metadata_,
                    similarity=rank,
                )
                for item, rank in res.all()
            ]

    async def_async_hybrid_query(
        self, query: VectorStoreQuery
    ) -> List[DBEmbeddingRow]:
        importasyncio

        if query.alpha is not None:
            _logger.warning("postgres hybrid search does not support alpha parameter.")

        sparse_top_k = query.sparse_top_k or query.similarity_top_k

        results = await asyncio.gather(
            self._aquery_with_score(
                query.query_embedding, query.similarity_top_k, query.filters
            ),
            self._async_sparse_query_with_rank(
                query.query_str, sparse_top_k, query.filters
            ),
        )

        dense_results, sparse_results = results
        all_results = dense_results + sparse_results
        return _dedup_results(all_results)

    def_hybrid_query(self, query: VectorStoreQuery) -> List[DBEmbeddingRow]:
        if query.alpha is not None:
            _logger.warning("postgres hybrid search does not support alpha parameter.")

        sparse_top_k = query.sparse_top_k or query.similarity_top_k

        dense_results = self._query_with_score(
            query.query_embedding, query.similarity_top_k, query.filters
        )

        sparse_results = self._sparse_query_with_rank(
            query.query_str, sparse_top_k, query.filters
        )

        all_results = dense_results + sparse_results
        return _dedup_results(all_results)

    def_db_rows_to_query_result(
        self, rows: List[DBEmbeddingRow]
    ) -> VectorStoreQueryResult:
        nodes = []
        similarities = []
        ids = []
        for db_embedding_row in rows:
            try:
                node = metadata_dict_to_node(db_embedding_row.metadata)
                node.set_content(str(db_embedding_row.text))
            except Exception:
                # NOTE: deprecated legacy logic for backward compatibility
                node = TextNode(
                    id_=db_embedding_row.node_id,
                    text=db_embedding_row.text,
                    metadata=db_embedding_row.metadata,
                )
            similarities.append(db_embedding_row.similarity)
            ids.append(db_embedding_row.node_id)
            nodes.append(node)

        return VectorStoreQueryResult(
            nodes=nodes,
            similarities=similarities,
            ids=ids,
        )

    async defaquery(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
        self._initialize()
        if query.mode == VectorStoreQueryMode.HYBRID:
            results = await self._async_hybrid_query(query)
        elif query.mode in [
            VectorStoreQueryMode.SPARSE,
            VectorStoreQueryMode.TEXT_SEARCH,
        ]:
            sparse_top_k = query.sparse_top_k or query.similarity_top_k
            results = await self._async_sparse_query_with_rank(
                query.query_str, sparse_top_k, query.filters
            )
        elif query.mode == VectorStoreQueryMode.DEFAULT:
            results = await self._aquery_with_score(
                query.query_embedding, query.similarity_top_k, query.filters
            )
        else:
            raise ValueError(f"Invalid query mode: {query.mode}")

        return self._db_rows_to_query_result(results)

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        self._initialize()
        if query.mode == VectorStoreQueryMode.HYBRID:
            results = self._hybrid_query(query)
        elif query.mode in [
            VectorStoreQueryMode.SPARSE,
            VectorStoreQueryMode.TEXT_SEARCH,
        ]:
            sparse_top_k = query.sparse_top_k or query.similarity_top_k
            results = self._sparse_query_with_rank(
                query.query_str, sparse_top_k, query.filters
            )
        elif query.mode == VectorStoreQueryMode.DEFAULT:
            results = self._query_with_score(
                query.query_embedding, query.similarity_top_k, query.filters
            )
        else:
            raise ValueError(f"Invalid query mode: {query.mode}")

        return self._db_rows_to_query_result(results)

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        fromsqlalchemyimport text

        self._initialize()
        with self._session() as session, session.begin():
            # Use parameterized query with bind parameters
            stmt = text(
                f"DELETE FROM {self.schema_name}.data_{self.table_name} "
                "WHERE (metadata_->>'doc_id')::text = :ref_doc_id"
            ).bindparams(ref_doc_id=ref_doc_id)

            session.execute(stmt)
            session.commit()

```
 |  
| --- | --- |  
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/lantern/#llama_index.vector_stores.lantern.LanternVectorStore.from_params "Permanent link")

```
from_params(
    host: Optional[] = None,
    port: Optional[] = None,
    database: Optional[] = None,
    user: Optional[] = None,
    password: Optional[] = None,
    table_name:  = "llamaindex",
    schema_name:  = "public",
    connection_string: Optional[] = None,
    async_connection_string: Optional[] = None,
    hybrid_search:  = False,
    text_search_config:  = "english",
    embed_dim:  = 1536,
    m:  = 16,
    ef_construction:  = 128,
    ef:  = 64,
    cache_ok:  = False,
    perform_setup:  = True,
    debug:  = False,
) -> 

```

Return connection string from database parameters.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-lantern/llama_index/vector_stores/lantern/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_params(
    cls,
    host: Optional[str] = None,
    port: Optional[str] = None,
    database: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    table_name: str = "llamaindex",
    schema_name: str = "public",
    connection_string: Optional[str] = None,
    async_connection_string: Optional[str] = None,
    hybrid_search: bool = False,
    text_search_config: str = "english",
    embed_dim: int = 1536,
    m: int = 16,
    ef_construction: int = 128,
    ef: int = 64,
    cache_ok: bool = False,
    perform_setup: bool = True,
    debug: bool = False,
) -> "LanternVectorStore":
"""Return connection string from database parameters."""
    conn_str = (
        connection_string
        or f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )
    async_conn_str = async_connection_string or (
        f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
    )
    return cls(
        connection_string=conn_str,
        async_connection_string=async_conn_str,
        table_name=table_name,
        schema_name=schema_name,
        hybrid_search=hybrid_search,
        text_search_config=text_search_config,
        embed_dim=embed_dim,
        m=m,
        ef_construction=ef_construction,
        ef=ef,
        cache_ok=cache_ok,
        perform_setup=perform_setup,
        debug=debug,
    )

```
 |  
| --- | --- |  
options: members: - LanternVectorStore
