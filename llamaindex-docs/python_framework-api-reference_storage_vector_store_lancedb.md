# Lancedb
##  LanceDBVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/lancedb/#llama_index.vector_stores.lancedb.LanceDBVectorStore "Permanent link")
Bases: 
The LanceDB Vector Store.
Stores text and embeddings in LanceDB. The vector store will open an existing LanceDB dataset or create the dataset if it does not exist.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `uri`  |  `(str, required)`  |  Location where LanceDB will store its files.  |  `'/tmp/lancedb'`  |  
|  `table_name`  |  The table name where the embeddings will be stored. Defaults to "vectors".  |  `'vectors'`  |  
|  `vector_column_name`  |  The vector column name in the table if different from default. Defaults to "vector", in keeping with lancedb convention.  |  `'vector'`  |  
|  `nprobes`  |  The number of probes used. A higher number makes search more accurate but also slower. Defaults to 20.  |  
|  `refine_factor`  |  `Optional[int]`  |  (int, optional): Refine the results by reading extra elements and re-ranking them in memory. Defaults to None  |  `None`  |  
|  `text_key`  |  The key in the table that contains the text. Defaults to "text".  |  `DEFAULT_TEXT_KEY`  |  
|  `doc_id_key`  |  The key in the table that contains the document id. Defaults to "doc_id".  |  `DEFAULT_DOC_ID_KEY`  |  
|  `connection`  |  The connection to use for LanceDB. Defaults to None.  |  `None`  |  
|  `table`  |  The table to use for LanceDB. Defaults to None.  |  `None`  |  
|  `api_key`  |  The API key to use LanceDB cloud. Defaults to None. You can also set the `LANCE_API_KEY` environment variable.  |  `None`  |  
|  `region`  |  The region to use for your LanceDB cloud db. Defaults to None.  |  `None`  |  
|  `mode`  |  The mode to use for LanceDB. Defaults to "overwrite".  |  `'overwrite'`  |  
|  `query_type`  |  The type of query to use for LanceDB. Defaults to "vector".  |  `'vector'`  |  
|  `reranker`  |  The reranker to use for LanceDB. Defaults to None.  |  `None`  |  
|  `overfetch_factor`  |  The factor by which to fetch more results. Defaults to 1.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ImportError`  |  Unable to import `lancedb`.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `LanceDBVectorStore`  |  VectorStore that supports creating LanceDB datasets and querying it.  |  
Examples:
`pip install llama-index-vector-stores-lancedb`

```
fromllama_index.vector_stores.lancedbimport LanceDBVectorStore

vector_store = LanceDBVectorStore()  # native invocation

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-lancedb/llama_index/vector_stores/lancedb/base.py`  
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
```
 | 
```
classLanceDBVectorStore(BasePydanticVectorStore):
"""
    The LanceDB Vector Store.

    Stores text and embeddings in LanceDB. The vector store will open an existing
        LanceDB dataset or create the dataset if it does not exist.

    Args:
        uri (str, required): Location where LanceDB will store its files.
        table_name (str, optional): The table name where the embeddings will be stored.
            Defaults to "vectors".
        vector_column_name (str, optional): The vector column name in the table if different from default.
            Defaults to "vector", in keeping with lancedb convention.
        nprobes (int, optional): The number of probes used.
            A higher number makes search more accurate but also slower.
            Defaults to 20.
        refine_factor: (int, optional): Refine the results by reading extra elements
            and re-ranking them in memory.
            Defaults to None
        text_key (str, optional): The key in the table that contains the text.
            Defaults to "text".
        doc_id_key (str, optional): The key in the table that contains the document id.
            Defaults to "doc_id".
        connection (Any, optional): The connection to use for LanceDB.
            Defaults to None.
        table (Any, optional): The table to use for LanceDB.
            Defaults to None.
        api_key (str, optional): The API key to use LanceDB cloud.
            Defaults to None. You can also set the `LANCE_API_KEY` environment variable.
        region (str, optional): The region to use for your LanceDB cloud db.
            Defaults to None.
        mode (str, optional): The mode to use for LanceDB.
            Defaults to "overwrite".
        query_type (str, optional): The type of query to use for LanceDB.
            Defaults to "vector".
        reranker (Any, optional): The reranker to use for LanceDB.
            Defaults to None.
        overfetch_factor (int, optional): The factor by which to fetch more results.
            Defaults to 1.

    Raises:
        ImportError: Unable to import `lancedb`.

    Returns:
        LanceDBVectorStore: VectorStore that supports creating LanceDB datasets and
            querying it.

    Examples:
        `pip install llama-index-vector-stores-lancedb`

        ```python
        from llama_index.vector_stores.lancedb import LanceDBVectorStore

        vector_store = LanceDBVectorStore()  # native invocation
        ```

    """

    stores_text: bool = True
    flat_metadata: bool = True
    uri: Optional[str]
    vector_column_name: Optional[str]
    nprobes: Optional[int]
    refine_factor: Optional[int]
    text_key: Optional[str]
    doc_id_key: Optional[str]
    api_key: Optional[str]
    region: Optional[str]
    mode: Optional[str]
    query_type: Optional[str]
    overfetch_factor: Optional[int]

    _table_name: Optional[str] = PrivateAttr()
    _connection: lancedb.DBConnection = PrivateAttr()
    _table: Any = PrivateAttr()
    _metadata_keys: Any = PrivateAttr()
    _fts_index_ready: bool = PrivateAttr()
    _reranker: Any = PrivateAttr()

    def__init__(
        self,
        uri: Optional[str] = "/tmp/lancedb",
        table_name: Optional[str] = "vectors",
        vector_column_name: str = "vector",
        nprobes: int = 20,
        refine_factor: Optional[int] = None,
        text_key: str = DEFAULT_TEXT_KEY,
        doc_id_key: str = DEFAULT_DOC_ID_KEY,
        connection: Optional[Any] = None,
        table: Optional[Any] = None,
        api_key: Optional[str] = None,
        region: Optional[str] = None,
        mode: str = "overwrite",
        query_type: str = "vector",
        reranker: Optional[Any] = None,
        overfetch_factor: int = 1,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        super().__init__(
            uri=uri,
            table_name=table_name,
            vector_column_name=vector_column_name,
            nprobes=nprobes,
            refine_factor=refine_factor,
            text_key=text_key,
            doc_id_key=doc_id_key,
            mode=mode,
            query_type=query_type,
            overfetch_factor=overfetch_factor,
            api_key=api_key,
            region=region,
            **kwargs,
        )

        self._table_name = table_name
        self._metadata_keys = None
        self._fts_index_ready = False

        if isinstance(reranker, lancedb.rerankers.Reranker):
            self._reranker = reranker
        elif reranker is None:
            self._reranker = None
        else:
            raise ValueError(
                "`reranker` has to be a lancedb.rerankers.Reranker object."
            )

        if isinstance(connection, lancedb.db.LanceDBConnection):
            self._connection = connection
        elif isinstance(connection, str):
            raise ValueError(
                "`connection` has to be a lancedb.db.LanceDBConnection object."
            )
        else:
            if api_key is None and os.getenv("LANCE_API_KEY") is None:
                if uri.startswith("db://"):
                    raise ValueError("API key is required for LanceDB cloud.")
                else:
                    self._connection = lancedb.connect(uri)
            else:
                if "db://" not in uri:
                    self._connection = lancedb.connect(uri)
                    warnings.warn(
                        "api key provided with local uri. The data will be stored locally"
                    )
                self._connection = lancedb.connect(
                    uri, api_key=api_key or os.getenv("LANCE_API_KEY"), region=region
                )

        if table is not None:
            try:
                assert isinstance(
                    table, (lancedb.db.LanceTable, lancedb.remote.table.RemoteTable)
                )
                self._table = table
                self._table_name = (
                    table.name if hasattr(table, "name") else "remote_table"
                )
            except AssertionError:
                raise ValueError(
                    "`table` has to be a lancedb.db.LanceTable or lancedb.remote.table.RemoteTable object."
                )
        else:
            if self._table_exists():
                self._table = self._connection.open_table(table_name)
            elif self.mode in ["create", "overwrite"]:
                _logger.warning(
                    f"Table {table_name} doesn't exist yet. Please add some data to create it."
                )
                self._table = None
            else:
                raise TableNotFoundError(
                    f"Table {self._table_name} doesn't exist, mode must be either 'create' or 'overwrite' to create it dynamically"
                )

    @property
    defclient(self) -> None:
"""Get client."""
        return self._connection

    @property
    deftable(
        self,
    ) -> Optional[Union[lancedb.db.LanceTable, lancedb.remote.table.RemoteTable]]:
"""Get table."""
        if self._table is None:
            raise TableNotFoundError(
                f"Table {self._table_name} is not initialized. Please create it or add some data first."
            )
        return self._table

    @classmethod
    deffrom_table(cls, table: Any) -> "LanceDBVectorStore":
"""Create instance from table."""
        try:
            if not isinstance(
                table, (lancedb.db.LanceTable, lancedb.remote.table.RemoteTable)
            ):
                raise Exception("argument is not lancedb table instance")
            return cls(table=table, connection=table._conn)
        except Exception as e:
            print("ldb version", lancedb.__version__)
            raise

    def_add_reranker(self, reranker: lancedb.rerankers.Reranker) -> None:
"""Add a reranker to an existing vector store."""
        if reranker is None:
            raise ValueError(
                "`reranker` has to be a lancedb.rerankers.Reranker object."
            )
        self._reranker = reranker

    def_table_exists(self, tbl_name: Optional[str] = None) -> bool:
        table_name = tbl_name or self._table_name
        if table_name is None:
            return False

        # Use page_token pagination to iterate through all table names.
        page_token: Optional[str] = None
        seen_page_tokens: set[Optional[str]] = set()
        while page_token not in seen_page_tokens:
            seen_page_tokens.add(page_token)
            # table_names() defaults to limit=10 in LanceDB.
            page = list(self._connection.table_names(page_token))

            if table_name in page:
                return True
            if not page:
                return False

            next_page_token = page[-1]
            if next_page_token == page_token:
                return False
            page_token = next_page_token

        return False

    defcreate_index(
        self,
        scalar: Optional[bool] = False,
        col_name: Optional[str] = None,
        num_partitions: Optional[int] = 256,
        num_sub_vectors: Optional[int] = 96,
        index_cache_size: Optional[int] = None,
        metric: Optional[str] = "L2",
        **kwargs: Any,
    ) -> None:
"""
        Create a scalar(for non-vector cols) or a vector index on a table.
        Make sure your vector column has enough data before creating an index on it.

        Args:
            scalar: Create a scalar index on a column. Defaults to False
            col_name: The column name to create the scalar index on. Defaults to None
            num_partitions: Number of partitions to use for the index. Defaults to 256
            num_sub_vectors: Number of sub-vectors to use for the index. Defaults to 96
            index_cache_size: The size of the index cache. Defaults to None
            metric: Provide the metric to use for vector index. Defaults to 'L2'
                    choice of metrics: 'L2', 'dot', 'cosine'
            **kwargs: Additional keyword arguments. See lancedb.db.LanceTable.create_index docs
        Returns:
            None

        """
        if not scalar:
            self.table.create_index(
                metric=metric,
                vector_column_name=self.vector_column_name,
                num_partitions=num_partitions,
                num_sub_vectors=num_sub_vectors,
                index_cache_size=index_cache_size,
                **kwargs,
            )
        else:
            if col_name is None:
                raise ValueError("Column name is required for scalar index creation.")
            self.table.create_scalar_index(col_name)

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
        if not nodes:
            _logger.debug("No nodes to add. Skipping the database operation.")
            return []
        data = []
        ids = []

        for node in nodes:
            metadata = node_to_metadata_dict(
                node, remove_text=False, flat_metadata=self.flat_metadata
            )
            if not self._metadata_keys:
                self._metadata_keys = list(metadata.keys())
            append_data = {
                "id": node.node_id,
                self.doc_id_key: node.ref_doc_id,
                self.vector_column_name: node.get_embedding(),
                self.text_key: node.get_content(metadata_mode=MetadataMode.NONE),
                "metadata": metadata,
            }
            data.append(append_data)
            ids.append(node.node_id)

        if self._table is None:
            _logger.info(f"Create new table {self._table_name} adding data.")
            self._table = self._connection.create_table(
                self._table_name, data, mode=self.mode
            )
        else:
            self._table.add(data)

        # new data requires re-creating the fts index
        self._fts_index_ready = False

        return ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        self.table.delete(f'{self.doc_id_key} = "' + ref_doc_id + '"')

    defdelete_nodes(self, node_ids: List[str], **delete_kwargs: Any) -> None:
"""
        Delete nodes using with node_ids.

        Args:
            node_ids (List[str]): The list of node_ids to delete.

        """
        self.table.delete('id in ("' + '","'.join(node_ids) + '")')

    defget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **kwargs: Any,
    ) -> List[BaseNode]:
"""
        Get nodes from the vector store.
        """
        if isinstance(self.table, lancedb.remote.table.RemoteTable):
            raise ValueError("get_nodes is not supported for LanceDB cloud yet.")

        if filters is not None:
            if "where" in kwargs:
                raise ValueError(
                    "Cannot specify filter via both query and kwargs. "
                    "Use kwargs only for lancedb specific items that are "
                    "not supported via the generic query interface."
                )
            where = _to_lance_filter(filters, self._metadata_keys)
        else:
            where = kwargs.pop("where", None)

        if node_ids is not None:
            where = f'id in ("' + '","'.join(node_ids) + '")'

        results = self.table.search().where(where).to_pandas()

        nodes = []

        for _, item in results.iterrows():
            try:
                node = metadata_dict_to_node(item.metadata)
                node.embedding = list(item[self.vector_column_name])
            except Exception:
                # deprecated legacy logic for backward compatibility
                _logger.debug(
                    "Failed to parse Node metadata, fallback to legacy logic."
                )
                if item.metadata:
                    metadata, node_info, _relation = legacy_metadata_dict_to_node(
                        item.metadata, text_key=self.text_key
                    )
                else:
                    metadata, node_info = {}, {}
                node = TextNode(
                    text=item[self.text_key] or "",
                    id_=item.id,
                    metadata=metadata,
                    start_char_idx=node_info.get("start"),
                    end_char_idx=node_info.get("end"),
                    relationships={
                        NodeRelationship.SOURCE: RelatedNodeInfo(
                            node_id=item[self.doc_id_key]
                        ),
                    },
                )

            nodes.append(node)

        return nodes

    defquery(
        self,
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""Query index for top k most similar nodes."""
        if query.filters is not None:
            if "where" in kwargs:
                raise ValueError(
                    "Cannot specify filter via both query and kwargs. "
                    "Use kwargs only for lancedb specific items that are "
                    "not supported via the generic query interface."
                )
            where = _to_lance_filter(query.filters, self._metadata_keys)
        else:
            where = kwargs.pop("where", None)

        query_type = kwargs.pop("query_type", self.query_type)

        _logger.info(f"query_type :, {query_type}")

        if query_type == "vector":
            _query = query.query_embedding
        else:
            if not isinstance(self.table, lancedb.db.LanceTable):
                raise ValueError(
                    "creating FTS index is not supported for LanceDB Cloud yet. "
                    "Please use a local table for FTS/Hybrid search."
                )
            if not self._fts_index_ready:
                self.table.create_fts_index(self.text_key, replace=True)
                self._fts_index_ready = True

            if query_type == "hybrid":
                _query = (query.query_embedding, query.query_str)
            elif query_type == "fts":
                _query = query.query_str
            else:
                raise ValueError(f"Invalid query type: {query_type}")

        if query_type == "hybrid":
            lance_query = (
                self.table.search(
                    vector_column_name=self.vector_column_name, query_type="hybrid"
                )
                .vector(query.query_embedding)
                .text(query.query_str)
            )
        else:
            lance_query = self.table.search(
                query=_query,
                vector_column_name=self.vector_column_name,
            )
        lance_query.limit(query.similarity_top_k * self.overfetch_factor).where(where)

        if query_type != "fts":
            lance_query.nprobes(self.nprobes)
            if query_type == "hybrid" and self._reranker is not None:
                _logger.info(f"using {self._reranker} for reranking results.")
                lance_query.rerank(reranker=self._reranker)

        if self.refine_factor is not None:
            lance_query.refine_factor(self.refine_factor)

        results = lance_query.to_pandas()

        if len(results) == 0:
            raise Warning("query results are empty..")

        nodes = []

        for _, item in results.iterrows():
            try:
                node = metadata_dict_to_node(item.metadata)
                node.embedding = list(item[self.vector_column_name])
            except Exception:
                # deprecated legacy logic for backward compatibility
                _logger.debug(
                    "Failed to parse Node metadata, fallback to legacy logic."
                )
                if item.metadata:
                    metadata, node_info, _relation = legacy_metadata_dict_to_node(
                        item.metadata, text_key=self.text_key
                    )
                else:
                    metadata, node_info = {}, {}
                node = TextNode(
                    text=item[self.text_key] or "",
                    id_=item.id,
                    metadata=metadata,
                    start_char_idx=node_info.get("start"),
                    end_char_idx=node_info.get("end"),
                    relationships={
                        NodeRelationship.SOURCE: RelatedNodeInfo(
                            node_id=item[self.doc_id_key]
                        ),
                    },
                )

            nodes.append(node)

        return VectorStoreQueryResult(
            nodes=nodes,
            similarities=_to_llama_similarities(results),
            ids=results["id"].tolist(),
        )

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/lancedb/#llama_index.vector_stores.lancedb.LanceDBVectorStore.client "Permanent link")

```
client: None

```

Get client.
###  table `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/lancedb/#llama_index.vector_stores.lancedb.LanceDBVectorStore.table "Permanent link")

```
table: Optional[Union[LanceTable, RemoteTable]]

```

Get table.
###  from_table `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/lancedb/#llama_index.vector_stores.lancedb.LanceDBVectorStore.from_table "Permanent link")

```
from_table(table: ) -> 

```

Create instance from table.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-lancedb/llama_index/vector_stores/lancedb/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_table(cls, table: Any) -> "LanceDBVectorStore":
"""Create instance from table."""
    try:
        if not isinstance(
            table, (lancedb.db.LanceTable, lancedb.remote.table.RemoteTable)
        ):
            raise Exception("argument is not lancedb table instance")
        return cls(table=table, connection=table._conn)
    except Exception as e:
        print("ldb version", lancedb.__version__)
        raise

```
 |  
| --- | --- |  
###  create_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/lancedb/#llama_index.vector_stores.lancedb.LanceDBVectorStore.create_index "Permanent link")

```
create_index(
    scalar: Optional[] = False,
    col_name: Optional[] = None,
    num_partitions: Optional[] = 256,
    num_sub_vectors: Optional[] = 96,
    index_cache_size: Optional[] = None,
    metric: Optional[] = "L2",
    **kwargs: 
) -> None

```

Create a scalar(for non-vector cols) or a vector index on a table. Make sure your vector column has enough data before creating an index on it.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `scalar`  |  `Optional[bool]`  |  Create a scalar index on a column. Defaults to False  |  `False`  |  
|  `col_name`  |  `Optional[str]`  |  The column name to create the scalar index on. Defaults to None  |  `None`  |  
|  `num_partitions`  |  `Optional[int]`  |  Number of partitions to use for the index. Defaults to 256  |  `256`  |  
|  `num_sub_vectors`  |  `Optional[int]`  |  Number of sub-vectors to use for the index. Defaults to 96  |  
|  `index_cache_size`  |  `Optional[int]`  |  The size of the index cache. Defaults to None  |  `None`  |  
|  `metric`  |  `Optional[str]`  |  Provide the metric to use for vector index. Defaults to 'L2' choice of metrics: 'L2', 'dot', 'cosine'  |  `'L2'`  |  
|  `**kwargs`  |  Additional keyword arguments. See lancedb.db.LanceTable.create_index docs  |  
Returns: None
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-lancedb/llama_index/vector_stores/lancedb/base.py`  
| 
```
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
```
 | 
```
defcreate_index(
    self,
    scalar: Optional[bool] = False,
    col_name: Optional[str] = None,
    num_partitions: Optional[int] = 256,
    num_sub_vectors: Optional[int] = 96,
    index_cache_size: Optional[int] = None,
    metric: Optional[str] = "L2",
    **kwargs: Any,
) -> None:
"""
    Create a scalar(for non-vector cols) or a vector index on a table.
    Make sure your vector column has enough data before creating an index on it.

    Args:
        scalar: Create a scalar index on a column. Defaults to False
        col_name: The column name to create the scalar index on. Defaults to None
        num_partitions: Number of partitions to use for the index. Defaults to 256
        num_sub_vectors: Number of sub-vectors to use for the index. Defaults to 96
        index_cache_size: The size of the index cache. Defaults to None
        metric: Provide the metric to use for vector index. Defaults to 'L2'
                choice of metrics: 'L2', 'dot', 'cosine'
        **kwargs: Additional keyword arguments. See lancedb.db.LanceTable.create_index docs
    Returns:
        None

    """
    if not scalar:
        self.table.create_index(
            metric=metric,
            vector_column_name=self.vector_column_name,
            num_partitions=num_partitions,
            num_sub_vectors=num_sub_vectors,
            index_cache_size=index_cache_size,
            **kwargs,
        )
    else:
        if col_name is None:
            raise ValueError("Column name is required for scalar index creation.")
        self.table.create_scalar_index(col_name)

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/lancedb/#llama_index.vector_stores.lancedb.LanceDBVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-lancedb/llama_index/vector_stores/lancedb/base.py`  
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    self.table.delete(f'{self.doc_id_key} = "' + ref_doc_id + '"')

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/lancedb/#llama_index.vector_stores.lancedb.LanceDBVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: [], **delete_kwargs: 
) -> None

```

Delete nodes using with node_ids.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `List[str]`  |  The list of node_ids to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-lancedb/llama_index/vector_stores/lancedb/base.py`  
| 
```
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
defdelete_nodes(self, node_ids: List[str], **delete_kwargs: Any) -> None:
"""
    Delete nodes using with node_ids.

    Args:
        node_ids (List[str]): The list of node_ids to delete.

    """
    self.table.delete('id in ("' + '","'.join(node_ids) + '")')

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/lancedb/#llama_index.vector_stores.lancedb.LanceDBVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **kwargs: 
) -> []

```

Get nodes from the vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-lancedb/llama_index/vector_stores/lancedb/base.py`  
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
```
 | 
```
defget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **kwargs: Any,
) -> List[BaseNode]:
"""
    Get nodes from the vector store.
    """
    if isinstance(self.table, lancedb.remote.table.RemoteTable):
        raise ValueError("get_nodes is not supported for LanceDB cloud yet.")

    if filters is not None:
        if "where" in kwargs:
            raise ValueError(
                "Cannot specify filter via both query and kwargs. "
                "Use kwargs only for lancedb specific items that are "
                "not supported via the generic query interface."
            )
        where = _to_lance_filter(filters, self._metadata_keys)
    else:
        where = kwargs.pop("where", None)

    if node_ids is not None:
        where = f'id in ("' + '","'.join(node_ids) + '")'

    results = self.table.search().where(where).to_pandas()

    nodes = []

    for _, item in results.iterrows():
        try:
            node = metadata_dict_to_node(item.metadata)
            node.embedding = list(item[self.vector_column_name])
        except Exception:
            # deprecated legacy logic for backward compatibility
            _logger.debug(
                "Failed to parse Node metadata, fallback to legacy logic."
            )
            if item.metadata:
                metadata, node_info, _relation = legacy_metadata_dict_to_node(
                    item.metadata, text_key=self.text_key
                )
            else:
                metadata, node_info = {}, {}
            node = TextNode(
                text=item[self.text_key] or "",
                id_=item.id,
                metadata=metadata,
                start_char_idx=node_info.get("start"),
                end_char_idx=node_info.get("end"),
                relationships={
                    NodeRelationship.SOURCE: RelatedNodeInfo(
                        node_id=item[self.doc_id_key]
                    ),
                },
            )

        nodes.append(node)

    return nodes

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/lancedb/#llama_index.vector_stores.lancedb.LanceDBVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-lancedb/llama_index/vector_stores/lancedb/base.py`  
| 
```
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
```
 | 
```
defquery(
    self,
    query: VectorStoreQuery,
    **kwargs: Any,
) -> VectorStoreQueryResult:
"""Query index for top k most similar nodes."""
    if query.filters is not None:
        if "where" in kwargs:
            raise ValueError(
                "Cannot specify filter via both query and kwargs. "
                "Use kwargs only for lancedb specific items that are "
                "not supported via the generic query interface."
            )
        where = _to_lance_filter(query.filters, self._metadata_keys)
    else:
        where = kwargs.pop("where", None)

    query_type = kwargs.pop("query_type", self.query_type)

    _logger.info(f"query_type :, {query_type}")

    if query_type == "vector":
        _query = query.query_embedding
    else:
        if not isinstance(self.table, lancedb.db.LanceTable):
            raise ValueError(
                "creating FTS index is not supported for LanceDB Cloud yet. "
                "Please use a local table for FTS/Hybrid search."
            )
        if not self._fts_index_ready:
            self.table.create_fts_index(self.text_key, replace=True)
            self._fts_index_ready = True

        if query_type == "hybrid":
            _query = (query.query_embedding, query.query_str)
        elif query_type == "fts":
            _query = query.query_str
        else:
            raise ValueError(f"Invalid query type: {query_type}")

    if query_type == "hybrid":
        lance_query = (
            self.table.search(
                vector_column_name=self.vector_column_name, query_type="hybrid"
            )
            .vector(query.query_embedding)
            .text(query.query_str)
        )
    else:
        lance_query = self.table.search(
            query=_query,
            vector_column_name=self.vector_column_name,
        )
    lance_query.limit(query.similarity_top_k * self.overfetch_factor).where(where)

    if query_type != "fts":
        lance_query.nprobes(self.nprobes)
        if query_type == "hybrid" and self._reranker is not None:
            _logger.info(f"using {self._reranker} for reranking results.")
            lance_query.rerank(reranker=self._reranker)

    if self.refine_factor is not None:
        lance_query.refine_factor(self.refine_factor)

    results = lance_query.to_pandas()

    if len(results) == 0:
        raise Warning("query results are empty..")

    nodes = []

    for _, item in results.iterrows():
        try:
            node = metadata_dict_to_node(item.metadata)
            node.embedding = list(item[self.vector_column_name])
        except Exception:
            # deprecated legacy logic for backward compatibility
            _logger.debug(
                "Failed to parse Node metadata, fallback to legacy logic."
            )
            if item.metadata:
                metadata, node_info, _relation = legacy_metadata_dict_to_node(
                    item.metadata, text_key=self.text_key
                )
            else:
                metadata, node_info = {}, {}
            node = TextNode(
                text=item[self.text_key] or "",
                id_=item.id,
                metadata=metadata,
                start_char_idx=node_info.get("start"),
                end_char_idx=node_info.get("end"),
                relationships={
                    NodeRelationship.SOURCE: RelatedNodeInfo(
                        node_id=item[self.doc_id_key]
                    ),
                },
            )

        nodes.append(node)

    return VectorStoreQueryResult(
        nodes=nodes,
        similarities=_to_llama_similarities(results),
        ids=results["id"].tolist(),
    )

```
 |  
| --- | --- |  
options: members: - LanceDBVectorStore
