# Nile
##  NileVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/nile/#llama_index.vector_stores.nile.NileVectorStore "Permanent link")
Bases: 
Nile (Multi-tenant Postgres) Vector Store.
Examples:
`pip install llama-index-vector-stores-nile`

```
fromllama_index.vector_stores.nileimport NileVectorStore

# Create NileVectorStore instance
vector_store = NileVectorStore.from_params(
    service_url="postgresql://user:password@us-west-2.db.thenile.dev:5432/niledb",
    table_name="test_table",
    tenant_aware=True,
    num_dimensions=1536
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-nile/llama_index/vector_stores/nile/base.py`  
| 
```
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
```
 | 
```
classNileVectorStore(BasePydanticVectorStore):
"""
    Nile (Multi-tenant Postgres) Vector Store.

    Examples:
        `pip install llama-index-vector-stores-nile`

        ```python
        from llama_index.vector_stores.nile import NileVectorStore

        # Create NileVectorStore instance
        vector_store = NileVectorStore.from_params(
            service_url="postgresql://user:password@us-west-2.db.thenile.dev:5432/niledb",
            table_name="test_table",
            tenant_aware=True,
            num_dimensions=1536

        ```

    """

    stores_text: bool = True
    flat_metadata: bool = False

    service_url: str
    table_name: str
    num_dimensions: int
    tenant_aware: bool

    _sync_conn: Any = PrivateAttr()
    _async_conn: Any = PrivateAttr()

    def_create_clients(self) -> None:
        self._sync_conn = psycopg.connect(self.service_url)
        self._async_conn = psycopg.connect(self.service_url)

    def_create_tables(self) -> None:
        _logger.info(
            f"Creating tables for {self.table_name} with {self.num_dimensions} dimensions"
        )
        with self._sync_conn.cursor() as cursor:
            if self.tenant_aware:
                query = sql.SQL(
"""
                        CREATE TABLE IF NOT EXISTS {table_name}
                        (id UUID DEFAULT (gen_random_uuid()), tenant_id UUID, embedding VECTOR({num_dimensions}), content TEXT, metadata JSONB)

                ).format(
                    table_name=sql.Identifier(self.table_name),
                    num_dimensions=sql.Literal(self.num_dimensions),
                )
                cursor.execute(query)
            else:
                query = sql.SQL(
"""
                        CREATE TABLE IF NOT EXISTS {table_name}
                        (id UUID DEFAULT (gen_random_uuid()), embedding VECTOR({num_dimensions}), content TEXT, metadata JSONB)

                ).format(
                    table_name=sql.Identifier(self.table_name),
                    num_dimensions=sql.Literal(self.num_dimensions),
                )
                cursor.execute(query)
        self._sync_conn.commit()

    def__init__(
        self,
        service_url: str,
        table_name: str,
        tenant_aware: bool = False,
        num_dimensions: int = DEFAULT_EMBEDDING_DIM,
    ) -> None:
        super().__init__(
            service_url=service_url,
            table_name=table_name,
            num_dimensions=num_dimensions,
            tenant_aware=tenant_aware,
        )

        self._create_clients()
        self._create_tables()

    @classmethod
    defclass_name(cls) -> str:
        return "NileVectorStore"

    @property
    defclient(self) -> Any:
        return self._sync_conn

    async defclose(self) -> None:
        self._sync_conn.close()
        await self._async_conn.close()

    @classmethod
    deffrom_params(
        cls,
        service_url: str,
        table_name: str,
        tenant_aware: bool = False,
        num_dimensions: int = DEFAULT_EMBEDDING_DIM,
    ) -> "NileVectorStore":
        return cls(
            service_url=service_url,
            table_name=table_name,
            tenant_aware=tenant_aware,
            num_dimensions=num_dimensions,
        )

    # We extract tenant_id from the node metadata.
    def_node_to_row(self, node: BaseNode) -> Any:
        metadata = node_to_metadata_dict(
            node,
            remove_text=True,
            flat_metadata=self.flat_metadata,
        )
        tenant_id = node.metadata.get("tenant_id", None)
        return [
            tenant_id,
            metadata,
            node.get_content(metadata_mode=MetadataMode.NONE),
            node.embedding,
        ]

    def_insert_row(self, cursor: Any, row: Any) -> str:
        _logger.debug(f"Inserting row into {self.table_name} with tenant_id {row[0]}")
        if self.tenant_aware:
            if row[0] is None:
                # Nile would fail the insert itself, but this saves the DB call and easier to test
                raise ValueError("tenant_id cannot be None if tenant_aware is True")
            query = sql.SQL(
"""
                           INSERT INTO {} (tenant_id, metadata, content, embedding) VALUES (%(tenant_id)s, %(metadata)s, %(content)s, %(embedding)s) returning id

            ).format(sql.Identifier(self.table_name))
            cursor.execute(
                query,
                {
                    "tenant_id": row[0],
                    "metadata": json.dumps(row[1]),
                    "content": row[2],
                    "embedding": row[3],
                },
            )
        else:
            query = sql.SQL(
"""
                           INSERT INTO {} (metadata, content, embedding) VALUES (%(metadata)s, %(content)s, %(embedding)s) returning id

            ).format(sql.Identifier(self.table_name))
            cursor.execute(
                query,
                {
                    "metadata": json.dumps(row[0]),
                    "content": row[1],
                    "embedding": row[2],
                },
            )
        id = cursor.fetchone()[0]
        self._sync_conn.commit()
        return id

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
        rows_to_insert = [self._node_to_row(node) for node in nodes]
        ids = []
        with self._sync_conn.cursor() as cursor:
            for row in rows_to_insert:
                # this will throw an error if tenant_id is None and tenant_aware is True, which is what we want
                ids.append(
                    self._insert_row(cursor, row)
                )  # commit is called in _insert_row
        return ids

    async defasync_add(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
        rows_to_insert = [self._node_to_row(node) for node in nodes]
        ids = []
        async with self._async_conn.cursor() as cursor:
            for row in rows_to_insert:
                ids.append(self._insert_row(cursor, row))
            await self._async_conn.commit()
        return ids

    def_set_tenant_context(self, cursor: Any, tenant_id: Any) -> None:
        if self.tenant_aware:
            cursor.execute(
                sql.SQL(""" set local nile.tenant_id = {} """).format(
                    sql.Literal(tenant_id)
                )
            )

    def_to_postgres_operator(self, operator: FilterOperator) -> str:
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
        elif operator == FilterOperator.CONTAINS:
            return "@>"
        elif operator == FilterOperator.TEXT_MATCH:
            return "LIKE"
        elif operator == FilterOperator.TEXT_MATCH_INSENSITIVE:
            return "ILIKE"
        else:
            _logger.warning(f"Unknown operator: {operator}, fallback to '='")
            return "="

    def_create_where_clause(self, filters: MetadataFilters) -> Tuple[sql.SQL, dict]:
        where_clauses = []
        params = {}
        param_counter = 0

        if filters is None:
            return sql.SQL(""), params

        _logger.debug(f"Filters: {filters}")

        for filter in filters.filters:
            param_counter += 1
            param_name = f"param_{param_counter}"

            if isinstance(filter, MetadataFilters):
                raise ValueError("Nested MetadataFilters are not supported yet")

            if isinstance(filter, MetadataFilter):
                key_param = f"key_{param_counter}"
                params[key_param] = filter.key

                if filter.operator in [FilterOperator.IN, FilterOperator.NIN]:
                    params[param_name] = filter.value
                    where_clauses.append(
                        sql.SQL("metadata->>%({})s {} %({})s").format(
                            sql.Identifier(key_param),
                            sql.SQL(self._to_postgres_operator(filter.operator)),
                            sql.Identifier(param_name),
                        )
                    )
                elif filter.operator in [FilterOperator.CONTAINS]:
                    params[param_name] = filter.value
                    where_clauses.append(
                        sql.SQL("metadata->%({})s @> %({})s::jsonb").format(
                            sql.Identifier(key_param), sql.Identifier(param_name)
                        )
                    )
                elif (
                    filter.operator == FilterOperator.TEXT_MATCH
                    or filter.operator == FilterOperator.TEXT_MATCH_INSENSITIVE
                ):
                    # Safely handle text match operations
                    params[param_name] = (
                        f"%{filter.value}%"  # Add wildcards in parameter, not in SQL
                    )
                    where_clauses.append(
                        sql.SQL("metadata->>%({})s {} %({})s").format(
                            sql.Identifier(key_param),
                            sql.SQL(self._to_postgres_operator(filter.operator)),
                            sql.Identifier(param_name),
                        )
                    )
                else:
                    params[param_name] = filter.value
                    where_clauses.append(
                        sql.SQL("metadata->>%({})s {} %({})s").format(
                            sql.Identifier(key_param),
                            sql.SQL(self._to_postgres_operator(filter.operator)),
                            sql.Identifier(param_name),
                        )
                    )

        _logger.debug(f"Where clauses: {where_clauses}")

        if len(where_clauses) == 0:
            return sql.SQL(""), params
        else:
            # Ensure the condition is either 'AND' or 'OR'
            safe_condition = "AND"
            if hasattr(filters, "condition") and filters.condition.upper() in [
                "AND",
                "OR",
            ]:
                safe_condition = filters.condition.upper()

            return (
                sql.SQL(" WHERE {}").format(
                    sql.SQL(f" {safe_condition} ").join(where_clauses)
                ),
                params,
            )

    def_execute_query(
        self,
        cursor: Any,
        query_embedding: VectorStoreQuery,
        tenant_id: Any = None,
        ivfflat_probes: Any = None,
        hnsw_ef_search: Any = None,
    ) -> List[Any]:
        _logger.info(f"Querying {self.table_name} with tenant_id {tenant_id}")
        self._set_tenant_context(cursor, tenant_id)
        if ivfflat_probes is not None:
            cursor.execute(
                sql.SQL("""SET ivfflat.probes = {}""").format(
                    sql.Literal(ivfflat_probes)
                )
            )
        if hnsw_ef_search is not None:
            cursor.execute(
                sql.SQL("""SET hnsw.ef_search = {}""").format(
                    sql.Literal(hnsw_ef_search)
                )
            )
        where_clause, where_params = self._create_where_clause(query_embedding.filters)
        query_params = {
            "query_embedding": query_embedding.query_embedding,
            **where_params,  # Merge the where clause parameters
        }

        query = sql.SQL(
"""
            SELECT
            id, metadata, content, %(query_embedding)s::vector<=>embedding as distance
            FROM
            {table_name}
            {where_clause}
            ORDER BY distance
            LIMIT {limit}

        ).format(
            table_name=sql.Identifier(self.table_name),
            where_clause=where_clause,
            limit=sql.Literal(query_embedding.similarity_top_k),
        )
        cursor.execute(query, query_params)
        return cursor.fetchall()

    def_process_query_results(self, results: List[Any]) -> VectorStoreQueryResult:
        nodes = []
        similarities = []
        ids = []
        for row in results:
            node = metadata_dict_to_node(row[1])
            node.set_content(row[2])
            nodes.append(node)
            similarities.append(row[3])
            ids.append(row[0])
        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

    # NOTE: Maybe handle tenant_id specified in filter vs. kwargs
    # NOTE: Add support for additional query modes
    defquery(
        self, query_embedding: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
        # get and validate tenant_id
        tenant_id = kwargs.get("tenant_id")
        ivfflat_probes = kwargs.get("ivfflat_probes")
        hnsw_ef_search = kwargs.get("hnsw_ef_search")
        if self.tenant_aware and tenant_id is None:
            raise ValueError(
                "tenant_id must be specified in kwargs if tenant_aware is True"
            )
        # check query mode
        if query_embedding.mode != VectorStoreQueryMode.DEFAULT:
            raise ValueError("Only DEFAULT mode is currently supported")
        # query
        with self._sync_conn.cursor() as cursor:
            self._set_tenant_context(cursor, tenant_id)
            results = self._execute_query(
                cursor, query_embedding, tenant_id, ivfflat_probes, hnsw_ef_search
            )
        self._sync_conn.commit()
        return self._process_query_results(results)

    async defaquery(
        self, query_embedding: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
        tenant_id = kwargs.get("tenant_id")
        if self.tenant_aware and tenant_id is None:
            raise ValueError(
                "tenant_id must be specified in kwargs if tenant_aware is True"
            )
        async with self._async_conn.cursor() as cursor:
            results = self._execute_query(cursor, query_embedding, tenant_id)
        await self._async_conn.commit()
        return self._process_query_results(results)

    defcreate_tenant(self, tenant_name: str) -> uuid.UUID:
"""
        Create a new tenant and return the tenant_id.

        Parameters
        ----------
            tenant_name (str): The name of the tenant to create.

        Returns
        -------
            tenant_id (uuid.UUID): The id of the newly created tenant.

        """
        with self._sync_conn.cursor() as cursor:
            cursor.execute(
"""
                           INSERT INTO tenants (name) VALUES (%(tenant_name)s) returning id
,
                {"tenant_name": tenant_name},
            )
            tenant_id = cursor.fetchone()[0]
            self._sync_conn.commit()
            return tenant_id

    defcreate_index(self, index_type: IndexType, **kwargs: Any) -> None:
"""
        Create an index of the specified type. Run this after populating the table.
        We intentionally throw an error if the index already exists.
        Since you may want to try a different type or parameters, we recommend dropping the index first.

        Parameters
        ----------
            index_type (IndexType): The type of index to create.
            m (optional int): The number of neighbors to consider during construction for PGVECTOR_HSNW index.
            ef_construction (optional int): The construction parameter for PGVECTOR_HSNW index.
            nlists (optional int): The number of lists for PGVECTOR_IVFFLAT index.

        """
        _logger.info(f"Creating index of type {index_type} for {self.table_name}")
        if index_type == IndexType.PGVECTOR_HNSW:
            m = kwargs.get("m")
            ef_construction = kwargs.get("ef_construction")
            if m is None or ef_construction is None:
                raise ValueError(
                    "m and ef_construction must be specified in kwargs for PGVECTOR_HSNW index"
                )
            query = sql.SQL(
"""
                            CREATE INDEX {index_name} ON {table_name} USING hnsw (embedding vector_cosine_ops) WITH (m = {m}, ef_construction = {ef_construction});

            ).format(
                table_name=sql.Identifier(self.table_name),
                index_name=sql.Identifier(f"{self.table_name}_embedding_idx"),
                m=sql.Literal(m),
                ef_construction=sql.Literal(ef_construction),
            )
            with self._sync_conn.cursor() as cursor:
                try:
                    cursor.execute(query)
                    self._sync_conn.commit()
                except psycopg.errors.DuplicateTable:
                    self._sync_conn.rollback()
                    raise psycopg.errors.DuplicateTable(
                        f"Index {self.table_name}_embedding_idx already exists"
                    )
        elif index_type == IndexType.PGVECTOR_IVFFLAT:
            nlists = kwargs.get("nlists")
            if nlists is None:
                raise ValueError(
                    "nlist must be specified in kwargs for PGVECTOR_IVFFLAT index"
                )
            query = sql.SQL(
"""
                CREATE INDEX {index_name} ON {table_name} USING ivfflat (embedding vector_cosine_ops) WITH (lists = {nlists});

            ).format(
                table_name=sql.Identifier(self.table_name),
                index_name=sql.Identifier(f"{self.table_name}_embedding_idx"),
                nlists=sql.Literal(nlists),
            )
            with self._sync_conn.cursor() as cursor:
                try:
                    cursor.execute(query)
                    self._sync_conn.commit()
                except psycopg.errors.DuplicateTable:
                    self._sync_conn.rollback()
                    raise psycopg.errors.DuplicateTable(
                        f"Index {self.table_name}_embedding_idx already exists"
                    )
        else:
            raise ValueError(f"Unknown index type: {index_type}")

    defdrop_index(self) -> None:
        _logger.info(f"Dropping index for {self.table_name}")
        query = sql.SQL(
"""
            DROP INDEX IF EXISTS {index_name};

        ).format(index_name=sql.Identifier(f"{self.table_name}_embedding_idx"))
        with self._sync_conn.cursor() as cursor:
            cursor.execute(query)
            self._sync_conn.commit()

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        tenant_id = delete_kwargs.get("tenant_id")
        _logger.info(f"Deleting document {ref_doc_id} with tenant_id {tenant_id}")
        if self.tenant_aware and tenant_id is None:
            raise ValueError(
                "tenant_id must be specified in delete_kwargs if tenant_aware is True"
            )
        with self._sync_conn.cursor() as cursor:
            self._set_tenant_context(cursor, tenant_id)
            cursor.execute(
                sql.SQL(
                    "DELETE FROM {} WHERE metadata->>'doc_id' = %(ref_doc_id)s"
                ).format(sql.Identifier(self.table_name)),
                {"ref_doc_id": ref_doc_id},
            )
        self._sync_conn.commit()

    async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        tenant_id = delete_kwargs.get("tenant_id")
        _logger.info(f"Deleting document {ref_doc_id} with tenant_id {tenant_id}")
        if self.tenant_aware and tenant_id is None:
            raise ValueError(
                "tenant_id must be specified in delete_kwargs if tenant_aware is True"
            )
        async with self._async_conn.cursor() as cursor:
            self._set_tenant_context(cursor, tenant_id)
            cursor.execute(
                sql.SQL(
                    "DELETE FROM {} WHERE metadata->>'doc_id' = %(ref_doc_id)s"
                ).format(sql.Identifier(self.table_name)),
                {"ref_doc_id": ref_doc_id},
            )
        await self._async_conn.commit()

```
 |  
| --- | --- |  
###  create_tenant [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/nile/#llama_index.vector_stores.nile.NileVectorStore.create_tenant "Permanent link")

```
create_tenant(tenant_name: ) -> 

```

Create a new tenant and return the tenant_id.
##### Parameters[#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/nile/#llama_index.vector_stores.nile.NileVectorStore.create_tenant--parameters "Permanent link")

```
tenant_name (str): The name of the tenant to create.

```

##### Returns[#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/nile/#llama_index.vector_stores.nile.NileVectorStore.create_tenant--returns "Permanent link")

```
tenant_id (uuid.UUID): The id of the newly created tenant.

```
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-nile/llama_index/vector_stores/nile/base.py`  
| 
```
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
```
 | 
```
defcreate_tenant(self, tenant_name: str) -> uuid.UUID:
"""
    Create a new tenant and return the tenant_id.

    Parameters
    ----------
        tenant_name (str): The name of the tenant to create.

    Returns
    -------
        tenant_id (uuid.UUID): The id of the newly created tenant.

    """
    with self._sync_conn.cursor() as cursor:
        cursor.execute(
"""
                       INSERT INTO tenants (name) VALUES (%(tenant_name)s) returning id
,
            {"tenant_name": tenant_name},
        )
        tenant_id = cursor.fetchone()[0]
        self._sync_conn.commit()
        return tenant_id

```
 |  
| --- | --- |  
###  create_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/nile/#llama_index.vector_stores.nile.NileVectorStore.create_index "Permanent link")

```
create_index(index_type: , **kwargs: ) -> None

```

Create an index of the specified type. Run this after populating the table. We intentionally throw an error if the index already exists. Since you may want to try a different type or parameters, we recommend dropping the index first.
##### Parameters[#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/nile/#llama_index.vector_stores.nile.NileVectorStore.create_index--parameters "Permanent link")

```
index_type (IndexType): The type of index to create.
m (optional int): The number of neighbors to consider during construction for PGVECTOR_HSNW index.
ef_construction (optional int): The construction parameter for PGVECTOR_HSNW index.
nlists (optional int): The number of lists for PGVECTOR_IVFFLAT index.

```
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-nile/llama_index/vector_stores/nile/base.py`  
| 
```
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
```
 | 
```
defcreate_index(self, index_type: IndexType, **kwargs: Any) -> None:
"""
    Create an index of the specified type. Run this after populating the table.
    We intentionally throw an error if the index already exists.
    Since you may want to try a different type or parameters, we recommend dropping the index first.

    Parameters
    ----------
        index_type (IndexType): The type of index to create.
        m (optional int): The number of neighbors to consider during construction for PGVECTOR_HSNW index.
        ef_construction (optional int): The construction parameter for PGVECTOR_HSNW index.
        nlists (optional int): The number of lists for PGVECTOR_IVFFLAT index.

    """
    _logger.info(f"Creating index of type {index_type} for {self.table_name}")
    if index_type == IndexType.PGVECTOR_HNSW:
        m = kwargs.get("m")
        ef_construction = kwargs.get("ef_construction")
        if m is None or ef_construction is None:
            raise ValueError(
                "m and ef_construction must be specified in kwargs for PGVECTOR_HSNW index"
            )
        query = sql.SQL(
"""
                        CREATE INDEX {index_name} ON {table_name} USING hnsw (embedding vector_cosine_ops) WITH (m = {m}, ef_construction = {ef_construction});

        ).format(
            table_name=sql.Identifier(self.table_name),
            index_name=sql.Identifier(f"{self.table_name}_embedding_idx"),
            m=sql.Literal(m),
            ef_construction=sql.Literal(ef_construction),
        )
        with self._sync_conn.cursor() as cursor:
            try:
                cursor.execute(query)
                self._sync_conn.commit()
            except psycopg.errors.DuplicateTable:
                self._sync_conn.rollback()
                raise psycopg.errors.DuplicateTable(
                    f"Index {self.table_name}_embedding_idx already exists"
                )
    elif index_type == IndexType.PGVECTOR_IVFFLAT:
        nlists = kwargs.get("nlists")
        if nlists is None:
            raise ValueError(
                "nlist must be specified in kwargs for PGVECTOR_IVFFLAT index"
            )
        query = sql.SQL(
"""
            CREATE INDEX {index_name} ON {table_name} USING ivfflat (embedding vector_cosine_ops) WITH (lists = {nlists});

        ).format(
            table_name=sql.Identifier(self.table_name),
            index_name=sql.Identifier(f"{self.table_name}_embedding_idx"),
            nlists=sql.Literal(nlists),
        )
        with self._sync_conn.cursor() as cursor:
            try:
                cursor.execute(query)
                self._sync_conn.commit()
            except psycopg.errors.DuplicateTable:
                self._sync_conn.rollback()
                raise psycopg.errors.DuplicateTable(
                    f"Index {self.table_name}_embedding_idx already exists"
                )
    else:
        raise ValueError(f"Unknown index type: {index_type}")

```
 |  
| --- | --- |  
##  IndexType [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/nile/#llama_index.vector_stores.nile.IndexType "Permanent link")
Bases: `Enum`
Supported Index types. These are just used by a helper function to create indices.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-nile/llama_index/vector_stores/nile/base.py`  
| 
```
33
34
35
36
37
```
 | 
```
classIndexType(enum.Enum):
"""Supported Index types. These are just used by a helper function to create indices."""

    PGVECTOR_IVFFLAT = 1
    PGVECTOR_HNSW = 2

```
 |  
| --- | --- |  
options: members: - NileVectorStore
