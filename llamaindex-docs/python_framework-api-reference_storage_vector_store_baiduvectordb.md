# Baiduvectordb
##  BaiduVectorDB [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/baiduvectordb/#llama_index.vector_stores.baiduvectordb.BaiduVectorDB "Permanent link")
Bases: 
Baidu VectorDB as a vector store.
In order to use this you need to have a database instance. See the following documentation for details: https://cloud.baidu.com/doc/VDB/index.html
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `endpoint`  |  `Optional[str]`  |  endpoint of Baidu VectorDB  |  _required_  |  
|  `account`  |  `Optional[str]`  |  The account for Baidu VectorDB. Default value is "root"  |  `DEFAULT_ACCOUNT`  |  
|  `api_key`  |  `Optional[str]`  |  The Api-Key for Baidu VectorDB  |  _required_  |  
|  `database_name`  |  `Optional[str]`  |  The database name for Baidu VectorDB  |  `DEFAULT_DATABASE_NAME`  |  
|  `table_params`  |  `Optional[TableParams[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/baiduvectordb/#llama_index.vector_stores.baiduvectordb.TableParams "TableParams \(llama_index.vector_stores.baiduvectordb.base.TableParams\)")]`  |  The table parameters for BaiduVectorDB  |  `TableParams[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/baiduvectordb/#llama_index.vector_stores.baiduvectordb.TableParams "TableParams \(llama_index.vector_stores.baiduvectordb.base.TableParams\)")(dimension=1536)`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-baiduvectordb/llama_index/vector_stores/baiduvectordb/base.py`  
| 
```
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
```
 | 
```
classBaiduVectorDB(BasePydanticVectorStore):
"""
    Baidu VectorDB as a vector store.

    In order to use this you need to have a database instance.
    See the following documentation for details:
    https://cloud.baidu.com/doc/VDB/index.html

    Args:
        endpoint (Optional[str]): endpoint of Baidu VectorDB
        account (Optional[str]): The account for Baidu VectorDB. Default value is "root"
        api_key (Optional[str]): The Api-Key for Baidu VectorDB
        database_name(Optional[str]): The database name for Baidu VectorDB
        table_params (Optional[TableParams]): The table parameters for BaiduVectorDB

    """

    user_defined_fields: List[TableField] = Field(default_factory=list)
    batch_size: int

    _vdb_client: Any = PrivateAttr()
    _database: Any = PrivateAttr()
    _table: Any = PrivateAttr()

    def__init__(
        self,
        endpoint: str,
        api_key: str,
        account: str = DEFAULT_ACCOUNT,
        database_name: str = DEFAULT_DATABASE_NAME,
        table_params: TableParams = TableParams(dimension=1536),
        batch_size: int = 1000,
        stores_text: bool = True,
        **kwargs: Any,
    ):
"""Init params."""
        super().__init__(
            user_defined_fields=table_params.filter_fields,
            batch_size=batch_size,
            stores_text=stores_text,
            **kwargs,
        )

        self._init_client(endpoint, account, api_key)
        self._create_database_if_not_exists(database_name)
        self._create_table(table_params)

    @classmethod
    defclass_name(cls) -> str:
        return "BaiduVectorDB"

    @classmethod
    deffrom_params(
        cls,
        endpoint: str,
        api_key: str,
        account: str = DEFAULT_ACCOUNT,
        database_name: str = DEFAULT_DATABASE_NAME,
        table_params: TableParams = TableParams(dimension=1536),
        batch_size: int = 1000,
        **kwargs: Any,
    ) -> "BaiduVectorDB":
        _try_import()
        return cls(
            endpoint=endpoint,
            account=account,
            api_key=api_key,
            database_name=database_name,
            table_params=table_params,
            batch_size=batch_size,
            **kwargs,
        )

    def_init_client(self, endpoint: str, account: str, api_key: str) -> None:
        importpymochow
        frompymochow.configurationimport Configuration
        frompymochow.auth.bce_credentialsimport BceCredentials

        logger.debug("Connecting to Baidu VectorDB...")
        config = Configuration(
            credentials=BceCredentials(account, api_key),
            endpoint=endpoint,
            connection_timeout_in_mills=DEFAULT_TIMEOUT_IN_MILLS,
        )
        self._vdb_client = pymochow.MochowClient(config)
        logger.debug("Baidu VectorDB client initialized.")

    def_create_database_if_not_exists(self, database_name: str) -> None:
        db_list = self._vdb_client.list_databases()

        if database_name in [db.database_name for db in db_list]:
            logger.debug(f"Database '{database_name}' already exists.")
            self._database = self._vdb_client.database(database_name)
        else:
            logger.debug(f"Creating database '{database_name}'.")
            self._database = self._vdb_client.create_database(database_name)
            logger.debug(f"Database '{database_name}' created.")

    def_create_table(self, table_params: TableParams) -> None:
        importpymochow

        if table_params is None:
            raise ValueError(VALUE_NONE_ERROR.format("table_params"))

        try:
            self._table = self._database.describe_table(table_params.table_name)
            logger.debug(f"Table '{table_params.table_name}' already exists.")
            if table_params.drop_exists:
                logger.debug(f"Dropping table '{table_params.table_name}'.")
                self._database.drop_table(table_params.table_name)
                # wait for table to be fully dropped
                start_time = time.time()
                loop_count = 0
                while time.time() - start_time  DEFAULT_WAIT_TIMEOUT:
                    loop_count += 1
                    logger.debug(
                        f"Waiting for table {table_params.table_name} to be dropped,"
                        f" attempt {loop_count}"
                    )
                    time.sleep(1)
                    tables = self._database.list_table()
                    table_names = {table.table_name for table in tables}
                    if table_params.table_name not in table_names:
                        logger.debug(f"Table '{table_params.table_name}' dropped.")
                        break
                else:
                    raise TimeoutError(
                        f"Table {table_params.table_name} was not dropped within"
                        f" {DEFAULT_WAIT_TIMEOUT} seconds"
                    )
                self._create_table_in_db(table_params)
        except pymochow.exception.ServerError:
            self._create_table_in_db(table_params)

    def_create_table_in_db(
        self,
        table_params: TableParams,
    ) -> None:
        frompymochow.model.enumimport FieldType, TableState
        frompymochow.model.schemaimport Field, Schema, SecondaryIndex, VectorIndex
        frompymochow.model.tableimport Partition

        logger.debug(f"Creating table '{table_params.table_name}'.")
        index_type = self._get_index_type(table_params.index_type)
        metric_type = self._get_metric_type(table_params.metric_type)
        vector_params = self._get_index_params(index_type, table_params)
        fields = []
        fields.append(
            Field(
                FIELD_ID,
                FieldType.STRING,
                primary_key=True,
                partition_key=True,
                auto_increment=False,
                not_null=True,
            )
        )
        fields.append(Field(DEFAULT_DOC_ID_KEY, FieldType.STRING))
        fields.append(Field(FIELD_METADATA, FieldType.STRING))
        fields.append(Field(DEFAULT_TEXT_KEY, FieldType.STRING))
        fields.append(
            Field(
                FIELD_VECTOR, FieldType.FLOAT_VECTOR, dimension=table_params.dimension
            )
        )
        for field in table_params.filter_fields:
            fields.append(Field(field.name, FieldType(field.data_type), not_null=True))

        indexes = []
        indexes.append(
            VectorIndex(
                index_name=INDEX_VECTOR,
                index_type=index_type,
                field=FIELD_VECTOR,
                metric_type=metric_type,
                params=vector_params,
            )
        )
        for field in table_params.filter_fields:
            index_name = field.name + INDEX_SUFFIX
            indexes.append(SecondaryIndex(index_name=index_name, field=field.name))

        schema = Schema(fields=fields, indexes=indexes)
        self._table = self._database.create_table(
            table_name=table_params.table_name,
            replication=table_params.replication,
            partition=Partition(partition_num=table_params.partition),
            schema=schema,
            enable_dynamic_field=True,
        )
        # wait for table to be ready
        start_time = time.time()
        loop_count = 0
        while time.time() - start_time  DEFAULT_WAIT_TIMEOUT:
            loop_count += 1
            logger.debug(
                f"Waiting for table {table_params.table_name} to become ready,"
                f" attempt {loop_count}"
            )
            time.sleep(1)
            table = self._database.describe_table(table_params.table_name)
            if table.state == TableState.NORMAL:
                logger.debug(f"Table '{table_params.table_name}' is ready.")
                break
        else:
            raise TimeoutError(
                f"Table {table_params.table_name} did not become ready within"
                f" {DEFAULT_WAIT_TIMEOUT} seconds"
            )

    @staticmethod
    def_get_index_params(index_type: Any, table_params: TableParams) -> None:
        frompymochow.model.enumimport IndexType
        frompymochow.model.schemaimport HNSWParams

        vector_params = (
            {} if table_params.vector_params is None else table_params.vector_params
        )

        if index_type == IndexType.HNSW:
            return HNSWParams(
                m=vector_params.get("M", DEFAULT_HNSW_M),
                efconstruction=vector_params.get(
                    "efConstruction", DEFAULT_HNSW_EF_CONSTRUCTION
                ),
            )
        return None

    @staticmethod
    def_get_index_type(index_type_value: str) -> Any:
        frompymochow.model.enumimport IndexType

        index_type_value = index_type_value or IndexType.HNSW
        try:
            return IndexType(index_type_value)
        except ValueError:
            support_index_types = [d.value for d in IndexType.__members__.values()]
            raise ValueError(
                NOT_SUPPORT_INDEX_TYPE_ERROR.format(
                    index_type_value, support_index_types
                )
            )

    @staticmethod
    def_get_metric_type(metric_type_value: str) -> Any:
        frompymochow.model.enumimport MetricType

        metric_type_value = metric_type_value or MetricType.L2
        try:
            return MetricType(metric_type_value.upper())
        except ValueError:
            support_metric_types = [d.value for d in MetricType.__members__.values()]
            raise ValueError(
                NOT_SUPPORT_METRIC_TYPE_ERROR.format(
                    metric_type_value, support_metric_types
                )
            )

    @property
    defclient(self) -> Any:
"""Get client."""
        return self._vdb_client

    defclear(self) -> None:
"""
        Clear all nodes from Baidu VectorDB table.
        This method deletes the table.
        """
        return asyncio.get_event_loop().run_until_complete(self.aclear())

    async defaclear(self) -> None:
"""
        Asynchronously clear all nodes from Baidu VectorDB table.
        This method deletes the table.
        """
        importpymochow

        try:
            # Check if table exists
            table_name = self._table.table_name
            self._database.describe_table(table_name)
            # Table exists, drop it
            logger.debug(f"Dropping table '{table_name}'.")
            self._database.drop_table(table_name)
            # Wait for table to be fully dropped
            start_time = time.time()
            loop_count = 0
            while time.time() - start_time  DEFAULT_WAIT_TIMEOUT:
                loop_count += 1
                logger.debug(
                    f"Waiting for table {table_name} to be dropped, attempt {loop_count}"
                )
                await asyncio.sleep(1)
                tables = self._database.list_table()
                table_names = {table.table_name for table in tables}
                if table_name not in table_names:
                    logger.debug(f"Table '{table_name}' dropped.")
                    break
            else:
                raise TimeoutError(
                    f"Table {table_name} was not dropped within {DEFAULT_WAIT_TIMEOUT}"
                    " seconds"
                )
        except (pymochow.exception.ServerError, AttributeError):
            # Table doesn't exist or _table not properly initialized, nothing to delete
            logger.debug("Table does not exist, nothing to clear.")

    defadd(
        self,
        nodes: List[BaseNode],
        *,
        rebuild_index: bool = True,
        rebuild_timeout: Optional[int] = None,
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to Baidu VectorDB table.

        Args:
            nodes: List of nodes with embeddings.
            rebuild_index: Optional. Whether to rebuild the vector index
                          after adding nodes. Defaults to True.
            rebuild_timeout: Optional. Timeout for rebuilding the index in seconds.
                             If None, it will wait indefinitely. Defaults to None.

        Returns:
            List of node IDs that were added to the table.

        """
        return asyncio.get_event_loop().run_until_complete(
            self.async_add(
                nodes,
                rebuild_index=rebuild_index,
                rebuild_timeout=rebuild_timeout,
                **add_kwargs,
            )
        )

    async defasync_add(
        self,
        nodes: List[BaseNode],
        *,
        rebuild_index: bool = True,
        rebuild_timeout: Optional[int] = None,
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Asynchronous method to add nodes to Baidu VectorDB table.

        Args:
            nodes: List of nodes with embeddings.
            rebuild_index: Optional. Whether to rebuild the vector index
                          after adding nodes. Defaults to True.
            rebuild_timeout: Optional. Timeout for rebuilding the index in seconds.
                             If None, it will wait indefinitely. Defaults to None.

        Returns:
            List of node IDs that were added to the table.

        """
        if len(nodes) == 0:
            return []

        frompymochow.model.tableimport Row
        frompymochow.model.enumimport IndexState

        ids = []
        rows = []
        for i, node in enumerate(nodes):
            logger.debug(f"Processing node {i+1}/{len(nodes)}, id: {node.node_id}")
            row = Row(id=node.node_id, vector=node.get_embedding())
            if node.ref_doc_id is not None:
                row._data[DEFAULT_DOC_ID_KEY] = node.ref_doc_id
            if node.metadata is not None:
                row._data[FIELD_METADATA] = json.dumps(node.metadata)
                for field in self.user_defined_fields:
                    v = node.metadata.get(field.name)
                    if v is not None:
                        row._data[field.name] = v
            if isinstance(node, TextNode) and node.text is not None:
                row._data[DEFAULT_TEXT_KEY] = node.text

            rows.append(row)
            ids.append(node.node_id)

            if len(rows) >= self.batch_size:
                logger.debug(f"Upserting {len(rows)} rows to the table.")
                self._table.upsert(rows=rows)
                rows = []

        if len(rows)  0:
            logger.debug(f"Upserting remaining {len(rows)} rows to the table.")
            self._table.upsert(rows=rows)

        if rebuild_index:
            logger.debug(f"Rebuilding index '{INDEX_VECTOR}'.")
            self._table.rebuild_index(INDEX_VECTOR)
            start_time = time.time()
            loop_count = 0
            while True:
                loop_count += 1
                logger.debug(
                    f"Waiting for index {INDEX_VECTOR} to be ready, attempt"
                    f" {loop_count}"
                )
                await asyncio.sleep(1)
                index = self._table.describe_index(INDEX_VECTOR)
                if index.state == IndexState.NORMAL:
                    logger.debug(f"Index '{INDEX_VECTOR}' is ready.")
                    break
                if (
                    rebuild_timeout is not None
                    and time.time() - start_time  rebuild_timeout
                ):
                    raise TimeoutError(
                        f"Index {INDEX_VECTOR} did not become ready within"
                        f" {rebuild_timeout} seconds"
                    )

        return ids

    # Baidu VectorDB Not support delete with filter right now, will support it later.
    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id or ids.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        raise NotImplementedError("Not support.")

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query (VectorStoreQuery): contains
                query_embedding (List[float]): query embedding
                similarity_top_k (int): top k most similar nodes
                filters (Optional[MetadataFilters]): filter result

        Returns:
            VectorStoreQueryResult: Query result containing nodes, similarities, and ids.

        """
        return asyncio.get_event_loop().run_until_complete(self.aquery(query, **kwargs))

    async defaquery(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
"""
        Asynchronously query index for top k most similar nodes.

        Args:
            query (VectorStoreQuery): contains
                query_embedding (List[float]): query embedding
                similarity_top_k (int): top k most similar nodes
                filters (Optional[MetadataFilters]): filter result

        Returns:
            VectorStoreQueryResult: Query result containing nodes, similarities, and ids.

        """
        frompymochow.model.tableimport AnnSearch, HNSWSearchParams

        search_filter = None
        if query.filters is not None:
            search_filter = self._build_filter_condition(query.filters, **kwargs)
        logger.debug(
            f"Querying with top_k={query.similarity_top_k} and filter='{search_filter}'"
        )
        anns = AnnSearch(
            vector_field=FIELD_VECTOR,
            vector_floats=query.query_embedding,
            params=HNSWSearchParams(ef=DEFAULT_HNSW_EF, limit=query.similarity_top_k),
            filter=search_filter,
        )
        res = self._table.search(anns=anns, retrieve_vector=True)
        rows = res.rows
        if rows is None or len(rows) == 0:
            logger.debug("Query returned no results.")
            return VectorStoreQueryResult(nodes=[], similarities=[], ids=[])

        logger.debug(f"Query returned {len(rows)} results.")
        nodes = []
        similarities = []
        ids = []
        for row in rows:
            similarities.append(row.get("distance"))
            row_data = row.get("row", {})
            ids.append(row_data.get(FIELD_ID))

            meta_str = row_data.get(FIELD_METADATA)
            meta = {} if meta_str is None else json.loads(meta_str)
            doc_id = row_data.get(DEFAULT_DOC_ID_KEY)

            node = TextNode(
                id_=row_data.get(FIELD_ID),
                text=row_data.get(DEFAULT_TEXT_KEY),
                embedding=row_data.get(FIELD_VECTOR),
                metadata=meta,
            )
            if doc_id is not None:
                node.relationships = {
                    NodeRelationship.SOURCE: RelatedNodeInfo(node_id=doc_id)
                }

            nodes.append(node)

        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

    @staticmethod
    def_build_filter_condition(standard_filters: MetadataFilters) -> str:
        filters_list = []

        for filter in standard_filters.filters:
            value = (
                f"'{filter.value}'"
                if isinstance(filter.value, (str, bool))
                else filter.value
            )

            if filter.operator:
                if filter.operator.value in ["<", ">", "<=", ">=", "!="]:
                    condition = f"{filter.key}{filter.operator.value}{value}"
                elif filter.operator.value in ["=="]:
                    condition = f"{filter.key} == {value}"
                else:
                    raise ValueError(
                        f"Filter operator {filter.operator} not supported."
                    )
            else:
                condition = f"{filter.key}{value}"

            filters_list.append(condition)

        return f" {standard_filters.condition.value.upper()} ".join(filters_list)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/baiduvectordb/#llama_index.vector_stores.baiduvectordb.BaiduVectorDB.client "Permanent link")

```
client: 

```

Get client.
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/baiduvectordb/#llama_index.vector_stores.baiduvectordb.BaiduVectorDB.clear "Permanent link")

```
clear() -> None

```

Clear all nodes from Baidu VectorDB table. This method deletes the table.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-baiduvectordb/llama_index/vector_stores/baiduvectordb/base.py`  
| 
```
394
395
396
397
398
399
```
 | 
```
defclear(self) -> None:
"""
    Clear all nodes from Baidu VectorDB table.
    This method deletes the table.
    """
    return asyncio.get_event_loop().run_until_complete(self.aclear())

```
 |  
| --- | --- |  
###  aclear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/baiduvectordb/#llama_index.vector_stores.baiduvectordb.BaiduVectorDB.aclear "Permanent link")

```
aclear() -> None

```

Asynchronously clear all nodes from Baidu VectorDB table. This method deletes the table.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-baiduvectordb/llama_index/vector_stores/baiduvectordb/base.py`  
| 
```
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
```
 | 
```
async defaclear(self) -> None:
"""
    Asynchronously clear all nodes from Baidu VectorDB table.
    This method deletes the table.
    """
    importpymochow

    try:
        # Check if table exists
        table_name = self._table.table_name
        self._database.describe_table(table_name)
        # Table exists, drop it
        logger.debug(f"Dropping table '{table_name}'.")
        self._database.drop_table(table_name)
        # Wait for table to be fully dropped
        start_time = time.time()
        loop_count = 0
        while time.time() - start_time  DEFAULT_WAIT_TIMEOUT:
            loop_count += 1
            logger.debug(
                f"Waiting for table {table_name} to be dropped, attempt {loop_count}"
            )
            await asyncio.sleep(1)
            tables = self._database.list_table()
            table_names = {table.table_name for table in tables}
            if table_name not in table_names:
                logger.debug(f"Table '{table_name}' dropped.")
                break
        else:
            raise TimeoutError(
                f"Table {table_name} was not dropped within {DEFAULT_WAIT_TIMEOUT}"
                " seconds"
            )
    except (pymochow.exception.ServerError, AttributeError):
        # Table doesn't exist or _table not properly initialized, nothing to delete
        logger.debug("Table does not exist, nothing to clear.")

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/baiduvectordb/#llama_index.vector_stores.baiduvectordb.BaiduVectorDB.add "Permanent link")

```
add(
    nodes: [],
    *,
    rebuild_index:  = True,
    rebuild_timeout: Optional[] = None,
    **add_kwargs: 
) -> []

```

Add nodes to Baidu VectorDB table.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes with embeddings.  |  _required_  |  
|  `rebuild_index`  |  `bool`  |  Optional. Whether to rebuild the vector index after adding nodes. Defaults to True.  |  `True`  |  
|  `rebuild_timeout`  |  `Optional[int]`  |  Optional. Timeout for rebuilding the index in seconds. If None, it will wait indefinitely. Defaults to None.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List of node IDs that were added to the table.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-baiduvectordb/llama_index/vector_stores/baiduvectordb/base.py`  
| 
```
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
```
 | 
```
defadd(
    self,
    nodes: List[BaseNode],
    *,
    rebuild_index: bool = True,
    rebuild_timeout: Optional[int] = None,
    **add_kwargs: Any,
) -> List[str]:
"""
    Add nodes to Baidu VectorDB table.

    Args:
        nodes: List of nodes with embeddings.
        rebuild_index: Optional. Whether to rebuild the vector index
                      after adding nodes. Defaults to True.
        rebuild_timeout: Optional. Timeout for rebuilding the index in seconds.
                         If None, it will wait indefinitely. Defaults to None.

    Returns:
        List of node IDs that were added to the table.

    """
    return asyncio.get_event_loop().run_until_complete(
        self.async_add(
            nodes,
            rebuild_index=rebuild_index,
            rebuild_timeout=rebuild_timeout,
            **add_kwargs,
        )
    )

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/baiduvectordb/#llama_index.vector_stores.baiduvectordb.BaiduVectorDB.async_add "Permanent link")

```
async_add(
    nodes: [],
    *,
    rebuild_index:  = True,
    rebuild_timeout: Optional[] = None,
    **add_kwargs: 
) -> []

```

Asynchronous method to add nodes to Baidu VectorDB table.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes with embeddings.  |  _required_  |  
|  `rebuild_index`  |  `bool`  |  Optional. Whether to rebuild the vector index after adding nodes. Defaults to True.  |  `True`  |  
|  `rebuild_timeout`  |  `Optional[int]`  |  Optional. Timeout for rebuilding the index in seconds. If None, it will wait indefinitely. Defaults to None.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List of node IDs that were added to the table.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-baiduvectordb/llama_index/vector_stores/baiduvectordb/base.py`  
| 
```
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
```
 | 
```
async defasync_add(
    self,
    nodes: List[BaseNode],
    *,
    rebuild_index: bool = True,
    rebuild_timeout: Optional[int] = None,
    **add_kwargs: Any,
) -> List[str]:
"""
    Asynchronous method to add nodes to Baidu VectorDB table.

    Args:
        nodes: List of nodes with embeddings.
        rebuild_index: Optional. Whether to rebuild the vector index
                      after adding nodes. Defaults to True.
        rebuild_timeout: Optional. Timeout for rebuilding the index in seconds.
                         If None, it will wait indefinitely. Defaults to None.

    Returns:
        List of node IDs that were added to the table.

    """
    if len(nodes) == 0:
        return []

    frompymochow.model.tableimport Row
    frompymochow.model.enumimport IndexState

    ids = []
    rows = []
    for i, node in enumerate(nodes):
        logger.debug(f"Processing node {i+1}/{len(nodes)}, id: {node.node_id}")
        row = Row(id=node.node_id, vector=node.get_embedding())
        if node.ref_doc_id is not None:
            row._data[DEFAULT_DOC_ID_KEY] = node.ref_doc_id
        if node.metadata is not None:
            row._data[FIELD_METADATA] = json.dumps(node.metadata)
            for field in self.user_defined_fields:
                v = node.metadata.get(field.name)
                if v is not None:
                    row._data[field.name] = v
        if isinstance(node, TextNode) and node.text is not None:
            row._data[DEFAULT_TEXT_KEY] = node.text

        rows.append(row)
        ids.append(node.node_id)

        if len(rows) >= self.batch_size:
            logger.debug(f"Upserting {len(rows)} rows to the table.")
            self._table.upsert(rows=rows)
            rows = []

    if len(rows)  0:
        logger.debug(f"Upserting remaining {len(rows)} rows to the table.")
        self._table.upsert(rows=rows)

    if rebuild_index:
        logger.debug(f"Rebuilding index '{INDEX_VECTOR}'.")
        self._table.rebuild_index(INDEX_VECTOR)
        start_time = time.time()
        loop_count = 0
        while True:
            loop_count += 1
            logger.debug(
                f"Waiting for index {INDEX_VECTOR} to be ready, attempt"
                f" {loop_count}"
            )
            await asyncio.sleep(1)
            index = self._table.describe_index(INDEX_VECTOR)
            if index.state == IndexState.NORMAL:
                logger.debug(f"Index '{INDEX_VECTOR}' is ready.")
                break
            if (
                rebuild_timeout is not None
                and time.time() - start_time  rebuild_timeout
            ):
                raise TimeoutError(
                    f"Index {INDEX_VECTOR} did not become ready within"
                    f" {rebuild_timeout} seconds"
                )

    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/baiduvectordb/#llama_index.vector_stores.baiduvectordb.BaiduVectorDB.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id or ids.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-baiduvectordb/llama_index/vector_stores/baiduvectordb/base.py`  
| 
```
553
554
555
556
557
558
559
560
561
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id or ids.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    raise NotImplementedError("Not support.")

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/baiduvectordb/#llama_index.vector_stores.baiduvectordb.BaiduVectorDB.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  contains query_embedding (List[float]): query embedding similarity_top_k (int): top k most similar nodes filters (Optional[MetadataFilters]): filter result  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  Query result containing nodes, similarities, and ids.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-baiduvectordb/llama_index/vector_stores/baiduvectordb/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query (VectorStoreQuery): contains
            query_embedding (List[float]): query embedding
            similarity_top_k (int): top k most similar nodes
            filters (Optional[MetadataFilters]): filter result

    Returns:
        VectorStoreQueryResult: Query result containing nodes, similarities, and ids.

    """
    return asyncio.get_event_loop().run_until_complete(self.aquery(query, **kwargs))

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/baiduvectordb/#llama_index.vector_stores.baiduvectordb.BaiduVectorDB.aquery "Permanent link")

```
aquery(
    query: , **kwargs: 
) -> 

```

Asynchronously query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  contains query_embedding (List[float]): query embedding similarity_top_k (int): top k most similar nodes filters (Optional[MetadataFilters]): filter result  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  Query result containing nodes, similarities, and ids.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-baiduvectordb/llama_index/vector_stores/baiduvectordb/base.py`  
| 
```
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
```
 | 
```
async defaquery(
    self, query: VectorStoreQuery, **kwargs: Any
) -> VectorStoreQueryResult:
"""
    Asynchronously query index for top k most similar nodes.

    Args:
        query (VectorStoreQuery): contains
            query_embedding (List[float]): query embedding
            similarity_top_k (int): top k most similar nodes
            filters (Optional[MetadataFilters]): filter result

    Returns:
        VectorStoreQueryResult: Query result containing nodes, similarities, and ids.

    """
    frompymochow.model.tableimport AnnSearch, HNSWSearchParams

    search_filter = None
    if query.filters is not None:
        search_filter = self._build_filter_condition(query.filters, **kwargs)
    logger.debug(
        f"Querying with top_k={query.similarity_top_k} and filter='{search_filter}'"
    )
    anns = AnnSearch(
        vector_field=FIELD_VECTOR,
        vector_floats=query.query_embedding,
        params=HNSWSearchParams(ef=DEFAULT_HNSW_EF, limit=query.similarity_top_k),
        filter=search_filter,
    )
    res = self._table.search(anns=anns, retrieve_vector=True)
    rows = res.rows
    if rows is None or len(rows) == 0:
        logger.debug("Query returned no results.")
        return VectorStoreQueryResult(nodes=[], similarities=[], ids=[])

    logger.debug(f"Query returned {len(rows)} results.")
    nodes = []
    similarities = []
    ids = []
    for row in rows:
        similarities.append(row.get("distance"))
        row_data = row.get("row", {})
        ids.append(row_data.get(FIELD_ID))

        meta_str = row_data.get(FIELD_METADATA)
        meta = {} if meta_str is None else json.loads(meta_str)
        doc_id = row_data.get(DEFAULT_DOC_ID_KEY)

        node = TextNode(
            id_=row_data.get(FIELD_ID),
            text=row_data.get(DEFAULT_TEXT_KEY),
            embedding=row_data.get(FIELD_VECTOR),
            metadata=meta,
        )
        if doc_id is not None:
            node.relationships = {
                NodeRelationship.SOURCE: RelatedNodeInfo(node_id=doc_id)
            }

        nodes.append(node)

    return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
##  TableParams [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/baiduvectordb/#llama_index.vector_stores.baiduvectordb.TableParams "Permanent link")
Baidu VectorDB table params.
See the following documentation for details: https://cloud.baidu.com/doc/VDB/s/mlrsob0p6
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `dimension int`  |  The dimension of vector.  |  _required_  |  
|  `replication int`  |  The number of replicas in the table.  |  _required_  |  
|  `partition int`  |  The number of partitions in the table.  |  _required_  |  
|  `index_type`  |  `Optional[str]`  |  HNSW, FLAT... Default value is "HNSW"  |  `DEFAULT_INDEX_TYPE`  |  
|  `metric_type`  |  `Optional[str]`  |  L2, COSINE, IP. Default value is "L2"  |  `DEFAULT_METRIC_TYPE`  |  
|  `drop_exists`  |  `Optional[bool]`  |  Delete the existing Table. Default value is False.  |  `False`  |  
|  `vector_params`  |  `Optional[Dict]`  |  if HNSW set parameters: `M` and `efConstruction`, for example `{'M': 16, efConstruction: 200}` default is HNSW  |  `None`  |  
|  `filter_fields`  |  `Optional[List[TableField]]`  |  Optional[List[str]]: Set the fields for filtering, The  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-baiduvectordb/llama_index/vector_stores/baiduvectordb/base.py`  
| 
```
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
```
 | 
```
classTableParams:
"""
    Baidu VectorDB table params.

    See the following documentation for details:
    https://cloud.baidu.com/doc/VDB/s/mlrsob0p6

    Args:
        dimension int: The dimension of vector.
        replication int: The number of replicas in the table.
        partition int: The number of partitions in the table.
        index_type (Optional[str]): HNSW, FLAT... Default value is "HNSW"
        metric_type (Optional[str]): L2, COSINE, IP. Default value is "L2"
        drop_exists (Optional[bool]): Delete the existing Table. Default value is False.
        vector_params (Optional[Dict]):
          if HNSW set parameters: `M` and `efConstruction`, for example `{'M': 16, efConstruction: 200}`
          default is HNSW
        filter_fields: Optional[List[str]]: Set the fields for filtering, The
        fields used for filtering must have a value in every row of the table
        and cannot be null.
          for example: ['author', 'age']
          This can be used when calling the query method：
             store.add([
                TextNode(..., metadata={'age'=23, 'name'='name1'})


             query = VectorStoreQuery(...)
             store.query(query, filter="age > 20 and age < 40 and name = 'name1'")

    """

    def__init__(
        self,
        dimension: int,
        table_name: str = DEFAULT_TABLE_NAME,
        replication: int = DEFAULT_REPLICA,
        partition: int = DEFAULT_PARTITION,
        index_type: str = DEFAULT_INDEX_TYPE,
        metric_type: str = DEFAULT_METRIC_TYPE,
        drop_exists: Optional[bool] = False,
        vector_params: Optional[Dict] = None,
        filter_fields: Optional[List[TableField]] = None,
    ):
        if filter_fields is None:
            filter_fields = []
        self.dimension = dimension
        self.table_name = table_name
        self.replication = replication
        self.partition = partition
        self.index_type = index_type
        self.metric_type = metric_type
        self.drop_exists = drop_exists
        self.vector_params = vector_params
        self.filter_fields = filter_fields

```
 |  
| --- | --- |  
options: members: - BaiduVectorDB
