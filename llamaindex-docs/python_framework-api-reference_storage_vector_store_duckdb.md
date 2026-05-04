# Duckdb
##  DuckDBVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/duckdb/#llama_index.vector_stores.duckdb.DuckDBVectorStore "Permanent link")
Bases: 
DuckDB vector store.
In this vector store, embeddings are stored within a DuckDB database.
During query time, the index uses DuckDB to query for the top k most similar nodes.
Examples:
`pip install llama-index-vector-stores-duckdb`

```
fromllama_index.vector_stores.duckdbimport DuckDBVectorStore

# in-memory
vector_store = DuckDBVectorStore()

# persist to disk
vector_store = DuckDBVectorStore("pg.duckdb", persist_dir="./persist/")

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-duckdb/llama_index/vector_stores/duckdb/base.py`  
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
```
 | 
```
classDuckDBVectorStore(BasePydanticVectorStore):
"""
    DuckDB vector store.

    In this vector store, embeddings are stored within a DuckDB database.

    During query time, the index uses DuckDB to query for the top
    k most similar nodes.

    Examples:
        `pip install llama-index-vector-stores-duckdb`

        ```python
        from llama_index.vector_stores.duckdb import DuckDBVectorStore

        # in-memory
        vector_store = DuckDBVectorStore()

        # persist to disk
        vector_store = DuckDBVectorStore("pg.duckdb", persist_dir="./persist/")
        ```

    """

    stores_text: bool = True
    flat_metadata: bool = True

    database_name: str
    table_name: str
    # schema_name: Optional[str] # TODO: support schema name
    embed_dim: Optional[int]
    # hybrid_search: Optional[bool] # TODO: support hybrid search
    text_search_config: Optional[dict]
    persist_dir: str

    _shared_conn: Optional[duckdb.DuckDBPyConnection] = PrivateAttr(default=None)
    _thread_local: threading.local = PrivateAttr(default_factory=threading.local)

    _is_initialized: bool = PrivateAttr(default=False)
    _database_path: Optional[str] = PrivateAttr()

    def__init__(
        self,
        database_name: str = ":memory:",
        table_name: str = "documents",
        embed_dim: Optional[int] = None,
        # https://duckdb.org/docs/extensions/full_text_search
        text_search_config: Optional[dict] = None,
        persist_dir: str = "./storage",
        client: Optional[duckdb.DuckDBPyConnection] = None,
        **kwargs: Any,  # noqa: ARG002
    ) -> None:
"""Init params."""
        if text_search_config is None:
            text_search_config = DEFAULT_TEXT_SEARCH_CONFIG

        fields = {
            "database_name": database_name,
            "table_name": table_name,
            "embed_dim": embed_dim,
            "text_search_config": text_search_config,
            "persist_dir": persist_dir,
        }

        if client is not None:
            self._shared_conn = client

        super().__init__(stores_text=True, **fields)

        _ = self._initialize_table(self.client, self.table_name, self.embed_dim)

    @classmethod
    deffrom_local(
        cls,
        database_path: str,
        table_name: str = "documents",
        # schema_name: Optional[str] = "main",
        embed_dim: Optional[int] = None,
        # hybrid_search: Optional[bool] = False,
        text_search_config: Optional[dict] = None,
        **kwargs: Any,
    ) -> "DuckDBVectorStore":
"""Load a DuckDB vector store from a local file."""
        db_path = Path(database_path)

        return cls(
            database_name=db_path.name,
            table_name=table_name,
            embed_dim=embed_dim,
            text_search_config=text_search_config,
            persist_dir=str(db_path.parent),
            **kwargs,
        )

    @classmethod
    deffrom_params(
        cls,
        database_name: str = ":memory:",
        table_name: str = "documents",
        # schema_name: Optional[str] = "main",
        embed_dim: Optional[int] = None,
        # hybrid_search: Optional[bool] = False,
        text_search_config: Optional[dict] = None,
        persist_dir: str = "./storage",
        **kwargs: Any,
    ) -> "DuckDBVectorStore":
        return cls(
            database_name=database_name,
            table_name=table_name,
            # schema_name=schema_name,
            embed_dim=embed_dim,
            # hybrid_search=hybrid_search,
            text_search_config=text_search_config,
            persist_dir=persist_dir,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "DuckDBVectorStore"

    @property
    defclient(self) -> duckdb.DuckDBPyConnection:
"""Return client."""
        if self._shared_conn is None:
            self._shared_conn = self._connect(self.database_name, self.persist_dir)

        if not hasattr(self._thread_local, "conn") or self._thread_local.conn is None:
            self._thread_local.conn = self._shared_conn.cursor()

        return self._thread_local.conn

    @classmethod
    def_connect(
        cls, database_name: str, persist_dir: str
    ) -> duckdb.DuckDBPyConnection:
"""Connect to the DuckDB database -- create the data persistence directory if it doesn't exist."""
        database_connection = database_name

        if database_name != ":memory:":
            persist_path = Path(persist_dir)

            if not persist_path.exists():
                persist_path.mkdir(parents=True, exist_ok=True)

            database_connection = str(persist_path / database_name)

        return duckdb.connect(database_connection)

    @property
    deftable(self) -> duckdb.DuckDBPyRelation:
"""Return the table for the connection to the DuckDB database."""
        return self.client.table(self.table_name)

    @classmethod
    def_get_embedding_type(cls, embed_dim: Optional[int]) -> str:
        return f"FLOAT[{embed_dim}]" if embed_dim is not None else "FLOAT[]"

    @classmethod
    def_initialize_table(
        cls, conn: duckdb.DuckDBPyConnection, table_name: str, embed_dim: Optional[int]
    ) -> None:
"""Initialize the DuckDB Database, extensions, and documents table."""
        home_dir = Path.home()
        conn.execute(f"SET home_directory='{home_dir}';")
        conn.install_extension("json")
        conn.load_extension("json")
        conn.install_extension("fts")
        conn.load_extension("fts")

        embedding_type = cls._get_embedding_type(embed_dim)

        conn.begin().execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name}
                node_id VARCHAR PRIMARY KEY,
                text TEXT,
                embedding {embedding_type},
                metadata_ JSON

        """).commit()

        table = conn.table(table_name)

        required_columns = ["node_id", "text", "embedding", "metadata_"]
        table_columns = table.describe().columns

        for column in required_columns:
            if column not in table_columns:
                raise DuckDBTableIncorrectColumnsError(
                    table_name, required_columns, table_columns
                )

    def_node_to_arrow_row(self, node: BaseNode) -> dict:
        return {
            "node_id": node.node_id,
            "text": node.get_content(metadata_mode=MetadataMode.NONE),
            "embedding": node.get_embedding(),
            "metadata_": node_to_metadata_dict(
                node, remove_text=True, flat_metadata=self.flat_metadata
            ),
        }

    def_arrow_row_to_node(self, row_dict: dict) -> BaseNode:
        node = metadata_dict_to_node(
            metadata=json.loads(row_dict["metadata_"]), text=row_dict["text"]
        )
        node.embedding = row_dict["embedding"]

        return node

    def_arrow_row_to_query_result(self, rows: list[dict]) -> VectorStoreQueryResult:
        nodes = []
        similarities = []
        ids = []

        for row in rows:
            node = self._arrow_row_to_node(row)
            nodes.append(node)
            ids.append(row["node_id"])
            similarities.append(row["score"])

        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

    @override
    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:  # noqa: ARG002
"""Query the vector store for top k most similar nodes."""
        filter_expression = self._build_metadata_filter_expressions(
            metadata_filters=query.filters
        )

        inner_query = self.table.select(
            StarExpression(),
            FunctionExpression(
                "array_cosine_similarity"
                if self.embed_dim is not None
                else "list_cosine_similarity",
                ColumnExpression("embedding"),
                ConstantExpression(query.query_embedding).cast(
                    self._get_embedding_type(self.embed_dim)
                ),
            ).alias("score"),
        ).filter(filter_expression)

        outer_query = (
            inner_query.select(
                ColumnExpression("node_id"),
                ColumnExpression("text"),
                ColumnExpression("embedding"),
                ColumnExpression("metadata_"),
                ColumnExpression("score"),
            )
            .filter(
                ColumnExpression("score").isnotnull(),
            )
            .sort(
                ColumnExpression("score").desc(),
            )
            .limit(
                query.similarity_top_k,
            )
        )

        command = outer_query.sql_query()

        rows = self.client.execute(command).arrow().to_pylist()

        return self._arrow_row_to_query_result(rows)

    @override
    async defaquery(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:  # noqa: ARG002
"""Query the vector store for top k most similar nodes."""
        return await asyncio.to_thread(self.query, query, **kwargs)

    @override
    defadd(self, nodes: Sequence[BaseNode], **add_kwargs: Any) -> list[str]:  # noqa: ARG002
"""Add nodes to the vector store."""
        rows: list[dict[str, Any]] = [self._node_to_arrow_row(node) for node in nodes]

        arrow_table = pyarrow.Table.from_pylist(rows)
        self.client.from_arrow(arrow_table).insert_into(self.table.alias)
        return [node.node_id for node in nodes]

    @override
    async defasync_add(
        self, nodes: Sequence[BaseNode], **add_kwargs: Any
    ) -> list[str]:  # noqa: ARG002
"""Add nodes to the vector store."""
        return await asyncio.to_thread(self.add, nodes, **add_kwargs)

    @override
    defget_nodes(
        self,
        node_ids: Optional[list[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **get_kwargs: Any,
    ) -> list[BaseNode]:  # noqa: ARG002
"""Get nodes using node_ids and/or filters. If both are provided, both are considered."""
        filter_expression = self._build_node_id_metadata_filter_expression(
            node_ids=node_ids,
            filters=filters,
        )

        command = self.table.filter(filter_expression).sql_query()

        rows = self.client.execute(command).arrow().to_pylist()

        return [self._arrow_row_to_node(row) for row in rows]

    @override
    async defaget_nodes(
        self,
        node_ids: Optional[list[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **get_kwargs: Any,
    ) -> list[BaseNode]:  # noqa: ARG002
"""Get nodes using node_ids and/or filters. If both are provided, both are considered."""
        return await asyncio.to_thread(self.get_nodes, node_ids, filters, **get_kwargs)

    @override
    defdelete_nodes(
        self,
        node_ids: Optional[list[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:  # noqa: ARG002
"""Delete nodes using node_ids and/or filters. If both are provided, both are considered."""
        filter_expression = self._build_node_id_metadata_filter_expression(
            node_ids=node_ids,
            filters=filters,
        )

        command = f"DELETE FROM {self.table.alias} WHERE {filter_expression}"

        self.client.execute(command)

    @override
    async defadelete_nodes(
        self,
        node_ids: Optional[list[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:  # noqa: ARG002
"""Delete nodes using node_ids and/or filters. If both are provided, both are considered."""
        return await asyncio.to_thread(
            self.delete_nodes, node_ids, filters, **delete_kwargs
        )

    @override
    defclear(self, **clear_kwargs: Any) -> None:  # noqa: ARG002
"""Clear the vector store."""
        command = f"DELETE FROM {self.table.alias}"

        self.client.execute(command)

    @override
    async defaclear(self, **clear_kwargs: Any) -> None:  # noqa: ARG002
"""Clear the vector store."""
        return await asyncio.to_thread(self.clear, **clear_kwargs)

    @override
    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:  # noqa: ARG002
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        where_clause = self._build_metadata_filter_expression(
            "ref_doc_id", ref_doc_id, FilterOperator.EQ
        )

        command = f"DELETE FROM {self.table.alias} WHERE {where_clause}"

        self.client.execute(command)

    @override
    async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:  # noqa: ARG002
"""
        Delete nodes using with ref_doc_id.

        """
        return await asyncio.to_thread(self.delete, ref_doc_id, **delete_kwargs)

    def_build_node_id_metadata_filter_expression(
        self,
        node_ids: Optional[list[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> Expression:
        filter_expression = Expression(True)

        if filters is not None:
            filter_expression = self._build_metadata_filter_expressions(
                metadata_filters=filters
            )

        if node_ids is not None:
            node_id_expression = FunctionExpression(
                "list_contains",
                ConstantExpression(node_ids),
                ColumnExpression("node_id"),
            )

            filter_expression = filter_expression.__and__(node_id_expression)

        return filter_expression

    def_build_metadata_filter_expression(
        self, key: str, value: Any, operator: FilterOperator
    ) -> Expression:
        metadata_column = ColumnExpression(f"metadata_.{key}")

        sample_value = value[0] if isinstance(value, list) else value
        value_type = filter_value_type_to_duckdb_type.get(type(sample_value))

        metadata_type_expression = FunctionExpression(
            "json_type",
            ColumnExpression("metadata_"),
            ConstantExpression(f"$.{key}"),
        )

        if value_type is None:
            # If the value is a JSON Null, we want to swap the 'Null' for an actual null
            metadata_column = CaseExpression(
                condition=metadata_type_expression.__eq__(ConstantExpression("NULL")),
                value=ConstantExpression(None),
            ).otherwise(metadata_column)

        if value_type == VARCHAR:
            # If the value is a string, it means the column is a JSON string
            # and so we need to unpack it otherwise we'll get back a JSON string (a string wrapped in quotes)
            # https://github.com/duckdb/duckdb/issues/17681
            metadata_column = FunctionExpression(
                "json_extract_string",
                ColumnExpression("metadata_"),
                ConstantExpression(f"$.{key}"),
            )

        metadata_value = ConstantExpression(value)

        return self._build_filter_expression(metadata_column, metadata_value, operator)

    def_build_filter_expression(
        self, column: Expression, value: Expression, operator: FilterOperator
    ) -> Expression:
"""
        Build a filter expression for a given column and value.

        Args:
            column: The key in the document to use in the filter.
            value: The value to use in the filter.
            operator: The filter operator to use.

        """
        if operator_func := li_filter_to_py_operator.get(operator):
            # We have a straightforward operator, and DuckDB can handle just take the Python operator
            # i.e. FilterOperator.EQ -> `==` (operator.eq)
            # i.e. FilterOperator.GTE -> `>=` (operator.ge)
            # ...
            return operator_func(column, value)

        if operator == FilterOperator.IN:
            # Given a list of values, check to see if the document's value is in the list
            return FunctionExpression(
                "list_contains",  # list_contains(list_to_look_in, element_to_find)
                value,
                column,
            )

        if operator == FilterOperator.NIN:
            # Given a list of values, check to see if the document's value is not in the list
            return FunctionExpression(
                "list_contains",  # list_contains(list_to_look_in, element_to_find)
                value,
                column,
            ).__eq__(ConstantExpression(False))

        if operator == FilterOperator.CONTAINS:
            # filter_value is in the document value
            # This will never be true so long as the DuckDB vector store
            # requires flat metadata
            return Expression(False)
            # return FunctionExpression(
            #     "list_contains", # list_contains(list_to_look_in, element_to_find)
            #     value,
            #     column,
            # )
        if operator == FilterOperator.ANY:
            # Check if the intersection of the two lists has at least one element
            return FunctionExpression(
                "list_has_any",
                column,
                value,
            )

        if operator == FilterOperator.ALL:
            # Check if all of the provided values are in the document's value
            return FunctionExpression(
                "list_has_all",  # list_has_all(list, sub-list)
                column,
                value,
            )

        if operator == FilterOperator.TEXT_MATCH:
            return FunctionExpression(
                "contains",
                column,
                value,
            )

        if operator == FilterOperator.TEXT_MATCH_INSENSITIVE:
            return FunctionExpression(
                "contains",
                FunctionExpression(
                    "lower",
                    column,
                ),
                FunctionExpression(
                    "lower",
                    value,
                ),
            )

        if operator == FilterOperator.IS_EMPTY:
            # column is null or the array is empty
            return column.isnull().__or__(
                CaseExpression(
                    condition=FunctionExpression("typeof", column).__eq__(
                        ConstantExpression("ARRAY")
                    ),
                    value=FunctionExpression("length", column).__eq__(
                        ConstantExpression(0)
                    ),
                )
            )

        raise NotImplementedError(f"Unsupported operator: {operator}")

    def_build_metadata_filter_expressions(
        self, metadata_filters: Optional[MetadataFilters] = None
    ) -> Expression:
        expressions: list[Expression] = []

        if metadata_filters is None or len(metadata_filters.filters) == 0:
            return Expression(True)

        for metadata_filter in metadata_filters.filters:
            if isinstance(metadata_filter, MetadataFilter):
                expressions.append(
                    self._build_metadata_filter_expression(
                        metadata_filter.key,
                        metadata_filter.value,
                        metadata_filter.operator,
                    )
                )
            elif isinstance(metadata_filter, MetadataFilters):
                expressions.append(
                    self._build_metadata_filter_expressions(metadata_filter)
                )
            else:
                raise NotImplementedError(
                    f"Unsupported metadata filter: {metadata_filter}"
                )

        final_expression: Expression = expressions[0]

        for expression in expressions[1:]:
            # We will do an implicit AND for NOT conditions
            if metadata_filters.condition in [FilterCondition.AND, FilterCondition.NOT]:
                final_expression = final_expression.__and__(expression)
                continue

            if metadata_filters.condition == FilterCondition.OR:
                final_expression = final_expression.__or__(expression)
                continue

            raise NotImplementedError(
                f"Unsupported condition: {metadata_filters.condition}"
            )

        if metadata_filters.condition == FilterCondition.NOT:
            final_expression = final_expression.__invert__()

        return final_expression

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/duckdb/#llama_index.vector_stores.duckdb.DuckDBVectorStore.client "Permanent link")

```
client: DuckDBPyConnection

```

Return client.
###  table `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/duckdb/#llama_index.vector_stores.duckdb.DuckDBVectorStore.table "Permanent link")

```
table: DuckDBPyRelation

```

Return the table for the connection to the DuckDB database.
###  from_local `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/duckdb/#llama_index.vector_stores.duckdb.DuckDBVectorStore.from_local "Permanent link")

```
from_local(
    database_path: ,
    table_name:  = "documents",
    embed_dim: Optional[] = None,
    text_search_config: Optional[] = None,
    **kwargs: 
) -> 

```

Load a DuckDB vector store from a local file.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-duckdb/llama_index/vector_stores/duckdb/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_local(
    cls,
    database_path: str,
    table_name: str = "documents",
    # schema_name: Optional[str] = "main",
    embed_dim: Optional[int] = None,
    # hybrid_search: Optional[bool] = False,
    text_search_config: Optional[dict] = None,
    **kwargs: Any,
) -> "DuckDBVectorStore":
"""Load a DuckDB vector store from a local file."""
    db_path = Path(database_path)

    return cls(
        database_name=db_path.name,
        table_name=table_name,
        embed_dim=embed_dim,
        text_search_config=text_search_config,
        persist_dir=str(db_path.parent),
        **kwargs,
    )

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/duckdb/#llama_index.vector_stores.duckdb.DuckDBVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query the vector store for top k most similar nodes.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-duckdb/llama_index/vector_stores/duckdb/base.py`  
| 
```
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
```
 | 
```
@override
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:  # noqa: ARG002
"""Query the vector store for top k most similar nodes."""
    filter_expression = self._build_metadata_filter_expressions(
        metadata_filters=query.filters
    )

    inner_query = self.table.select(
        StarExpression(),
        FunctionExpression(
            "array_cosine_similarity"
            if self.embed_dim is not None
            else "list_cosine_similarity",
            ColumnExpression("embedding"),
            ConstantExpression(query.query_embedding).cast(
                self._get_embedding_type(self.embed_dim)
            ),
        ).alias("score"),
    ).filter(filter_expression)

    outer_query = (
        inner_query.select(
            ColumnExpression("node_id"),
            ColumnExpression("text"),
            ColumnExpression("embedding"),
            ColumnExpression("metadata_"),
            ColumnExpression("score"),
        )
        .filter(
            ColumnExpression("score").isnotnull(),
        )
        .sort(
            ColumnExpression("score").desc(),
        )
        .limit(
            query.similarity_top_k,
        )
    )

    command = outer_query.sql_query()

    rows = self.client.execute(command).arrow().to_pylist()

    return self._arrow_row_to_query_result(rows)

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/duckdb/#llama_index.vector_stores.duckdb.DuckDBVectorStore.aquery "Permanent link")

```
aquery(
    query: , **kwargs: 
) -> 

```

Query the vector store for top k most similar nodes.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-duckdb/llama_index/vector_stores/duckdb/base.py`  
| 
```
356
357
358
359
360
361
```
 | 
```
@override
async defaquery(
    self, query: VectorStoreQuery, **kwargs: Any
) -> VectorStoreQueryResult:  # noqa: ARG002
"""Query the vector store for top k most similar nodes."""
    return await asyncio.to_thread(self.query, query, **kwargs)

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/duckdb/#llama_index.vector_stores.duckdb.DuckDBVectorStore.add "Permanent link")

```
add(
    nodes: Sequence[], **add_kwargs: 
) -> []

```

Add nodes to the vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-duckdb/llama_index/vector_stores/duckdb/base.py`  
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
```
 | 
```
@override
defadd(self, nodes: Sequence[BaseNode], **add_kwargs: Any) -> list[str]:  # noqa: ARG002
"""Add nodes to the vector store."""
    rows: list[dict[str, Any]] = [self._node_to_arrow_row(node) for node in nodes]

    arrow_table = pyarrow.Table.from_pylist(rows)
    self.client.from_arrow(arrow_table).insert_into(self.table.alias)
    return [node.node_id for node in nodes]

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/duckdb/#llama_index.vector_stores.duckdb.DuckDBVectorStore.async_add "Permanent link")

```
async_add(
    nodes: Sequence[], **add_kwargs: 
) -> []

```

Add nodes to the vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-duckdb/llama_index/vector_stores/duckdb/base.py`  
| 
```
372
373
374
375
376
377
```
 | 
```
@override
async defasync_add(
    self, nodes: Sequence[BaseNode], **add_kwargs: Any
) -> list[str]:  # noqa: ARG002
"""Add nodes to the vector store."""
    return await asyncio.to_thread(self.add, nodes, **add_kwargs)

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/duckdb/#llama_index.vector_stores.duckdb.DuckDBVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **get_kwargs: 
) -> []

```

Get nodes using node_ids and/or filters. If both are provided, both are considered.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-duckdb/llama_index/vector_stores/duckdb/base.py`  
| 
```
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
```
 | 
```
@override
defget_nodes(
    self,
    node_ids: Optional[list[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **get_kwargs: Any,
) -> list[BaseNode]:  # noqa: ARG002
"""Get nodes using node_ids and/or filters. If both are provided, both are considered."""
    filter_expression = self._build_node_id_metadata_filter_expression(
        node_ids=node_ids,
        filters=filters,
    )

    command = self.table.filter(filter_expression).sql_query()

    rows = self.client.execute(command).arrow().to_pylist()

    return [self._arrow_row_to_node(row) for row in rows]

```
 |  
| --- | --- |  
###  aget_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/duckdb/#llama_index.vector_stores.duckdb.DuckDBVectorStore.aget_nodes "Permanent link")

```
aget_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **get_kwargs: 
) -> []

```

Get nodes using node_ids and/or filters. If both are provided, both are considered.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-duckdb/llama_index/vector_stores/duckdb/base.py`  
| 
```
398
399
400
401
402
403
404
405
406
```
 | 
```
@override
async defaget_nodes(
    self,
    node_ids: Optional[list[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **get_kwargs: Any,
) -> list[BaseNode]:  # noqa: ARG002
"""Get nodes using node_ids and/or filters. If both are provided, both are considered."""
    return await asyncio.to_thread(self.get_nodes, node_ids, filters, **get_kwargs)

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/duckdb/#llama_index.vector_stores.duckdb.DuckDBVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Delete nodes using node_ids and/or filters. If both are provided, both are considered.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-duckdb/llama_index/vector_stores/duckdb/base.py`  
| 
```
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
```
 | 
```
@override
defdelete_nodes(
    self,
    node_ids: Optional[list[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:  # noqa: ARG002
"""Delete nodes using node_ids and/or filters. If both are provided, both are considered."""
    filter_expression = self._build_node_id_metadata_filter_expression(
        node_ids=node_ids,
        filters=filters,
    )

    command = f"DELETE FROM {self.table.alias} WHERE {filter_expression}"

    self.client.execute(command)

```
 |  
| --- | --- |  
###  adelete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/duckdb/#llama_index.vector_stores.duckdb.DuckDBVectorStore.adelete_nodes "Permanent link")

```
adelete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Delete nodes using node_ids and/or filters. If both are provided, both are considered.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-duckdb/llama_index/vector_stores/duckdb/base.py`  
| 
```
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
```
 | 
```
@override
async defadelete_nodes(
    self,
    node_ids: Optional[list[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:  # noqa: ARG002
"""Delete nodes using node_ids and/or filters. If both are provided, both are considered."""
    return await asyncio.to_thread(
        self.delete_nodes, node_ids, filters, **delete_kwargs
    )

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/duckdb/#llama_index.vector_stores.duckdb.DuckDBVectorStore.clear "Permanent link")

```
clear(**clear_kwargs: ) -> None

```

Clear the vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-duckdb/llama_index/vector_stores/duckdb/base.py`  
| 
```
437
438
439
440
441
442
```
 | 
```
@override
defclear(self, **clear_kwargs: Any) -> None:  # noqa: ARG002
"""Clear the vector store."""
    command = f"DELETE FROM {self.table.alias}"

    self.client.execute(command)

```
 |  
| --- | --- |  
###  aclear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/duckdb/#llama_index.vector_stores.duckdb.DuckDBVectorStore.aclear "Permanent link")

```
aclear(**clear_kwargs: ) -> None

```

Clear the vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-duckdb/llama_index/vector_stores/duckdb/base.py`  
| 
```
444
445
446
447
```
 | 
```
@override
async defaclear(self, **clear_kwargs: Any) -> None:  # noqa: ARG002
"""Clear the vector store."""
    return await asyncio.to_thread(self.clear, **clear_kwargs)

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/duckdb/#llama_index.vector_stores.duckdb.DuckDBVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-duckdb/llama_index/vector_stores/duckdb/base.py`  
| 
```
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
@override
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:  # noqa: ARG002
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    where_clause = self._build_metadata_filter_expression(
        "ref_doc_id", ref_doc_id, FilterOperator.EQ
    )

    command = f"DELETE FROM {self.table.alias} WHERE {where_clause}"

    self.client.execute(command)

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/duckdb/#llama_index.vector_stores.duckdb.DuckDBVectorStore.adelete "Permanent link")

```
adelete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-duckdb/llama_index/vector_stores/duckdb/base.py`  
| 
```
466
467
468
469
470
471
472
```
 | 
```
@override
async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:  # noqa: ARG002
"""
    Delete nodes using with ref_doc_id.

    """
    return await asyncio.to_thread(self.delete, ref_doc_id, **delete_kwargs)

```
 |  
| --- | --- |  
options: members: - DuckDBVectorStore
