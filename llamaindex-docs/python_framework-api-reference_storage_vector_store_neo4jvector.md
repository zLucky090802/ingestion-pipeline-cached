# Neo4jvector
##  Neo4jVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/neo4jvector/#llama_index.vector_stores.neo4jvector.Neo4jVectorStore "Permanent link")
Bases: 
Neo4j Vector Store.
Examples:
`pip install llama-index-vector-stores-neo4jvector`

```
fromllama_index.vector_stores.neo4jvectorimport Neo4jVectorStore

username = "neo4j"
password = "pleaseletmein"
url = "bolt://localhost:7687"
embed_dim = 1536

neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-neo4jvector/llama_index/vector_stores/neo4jvector/base.py`  
| 
```
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
```
 | 
```
classNeo4jVectorStore(BasePydanticVectorStore):
"""
    Neo4j Vector Store.

    Examples:
        `pip install llama-index-vector-stores-neo4jvector`


        ```python
        from llama_index.vector_stores.neo4jvector import Neo4jVectorStore

        username = "neo4j"
        password = "pleaseletmein"
        url = "bolt://localhost:7687"
        embed_dim = 1536

        neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim)
        ```

    """

    stores_text: bool = True
    flat_metadata: bool = True

    distance_strategy: str
    index_name: str
    keyword_index_name: str
    hybrid_search: bool
    node_label: str
    embedding_node_property: str
    text_node_property: str
    retrieval_query: str
    embedding_dimension: int

    _driver: neo4j.GraphDatabase.driver = PrivateAttr()
    _database: str = PrivateAttr()
    _support_metadata_filter: bool = PrivateAttr()
    _is_enterprise: bool = PrivateAttr()

    def__init__(
        self,
        username: str,
        password: str,
        url: str,
        embedding_dimension: int,
        database: str = "neo4j",
        index_name: str = "vector",
        keyword_index_name: str = "keyword",
        node_label: str = "Chunk",
        embedding_node_property: str = "embedding",
        text_node_property: str = "text",
        distance_strategy: str = "cosine",
        hybrid_search: bool = False,
        retrieval_query: str = "",
        user_agent: str = "LLAMAINDEX-VECTOR",
        **kwargs: Any,
    ) -> None:
        super().__init__(
            distance_strategy=distance_strategy,
            index_name=index_name,
            keyword_index_name=keyword_index_name,
            hybrid_search=hybrid_search,
            node_label=node_label,
            embedding_node_property=embedding_node_property,
            text_node_property=text_node_property,
            retrieval_query=retrieval_query,
            embedding_dimension=embedding_dimension,
        )

        if distance_strategy not in ["cosine", "euclidean"]:
            raise ValueError("distance_strategy must be either 'euclidean' or 'cosine'")

        self._driver = neo4j.GraphDatabase.driver(
            url, auth=(username, password), user_agent=user_agent
        )
        self._database = database

        # Verify connection
        try:
            self._driver.verify_connectivity()
        except neo4j.exceptions.ServiceUnavailable:
            raise ValueError(
                "Could not connect to Neo4j database. "
                "Please ensure that the url is correct"
            )
        except neo4j.exceptions.AuthError:
            raise ValueError(
                "Could not connect to Neo4j database. "
                "Please ensure that the username and password are correct"
            )

        # Verify if the version support vector index
        self._verify_version()

        # Verify that required values are not null
        check_if_not_null(
            [
                "index_name",
                "node_label",
                "embedding_node_property",
                "text_node_property",
            ],
            [index_name, node_label, embedding_node_property, text_node_property],
        )

        index_already_exists = self.retrieve_existing_index()
        if not index_already_exists:
            self.create_new_index()
        if hybrid_search:
            fts_node_label = self.retrieve_existing_fts_index()
            # If the FTS index doesn't exist yet
            if not fts_node_label:
                self.create_new_keyword_index()
            else:  # Validate that FTS and Vector index use the same information
                if not fts_node_label == self.node_label:
                    raise ValueError(
                        "Vector and keyword index don't index the same node label"
                    )

    @property
    defclient(self) -> neo4j.GraphDatabase.driver:
        return self._driver

    def_verify_version(self) -> None:
"""
        Check if the connected Neo4j database version supports vector indexing.

        Queries the Neo4j database to retrieve its version and compares it
        against a target version (5.11.0) that is known to support vector
        indexing. Raises a ValueError if the connected Neo4j version is
        not supported.
        """
        db_data = self.database_query("CALL dbms.components()")
        version = db_data[0]["versions"][0]
        if "aura" in version:
            version_tuple = (*tuple(map(int, version.split("-")[0].split("."))), 0)
        else:
            version_tuple = tuple(map(int, version.split(".")))

        target_version = (5, 11, 0)

        if version_tuple  target_version:
            raise ValueError(
                "Version index is only supported in Neo4j version 5.11 or greater"
            )

        # Flag for metadata filtering
        metadata_target_version = (5, 18, 0)
        if version_tuple  metadata_target_version:
            self._support_metadata_filter = False
        else:
            self._support_metadata_filter = True
        # Flag for enterprise
        self._is_enterprise = db_data[0]["edition"] == "enterprise"
        # Flag for call parameter
        call_param_required_version = (5, 23, 0)
        if version_tuple  call_param_required_version:
            self._call_param_required = False
        else:
            self._call_param_required = True

    defcreate_new_index(self) -> None:
"""
        This method constructs a Cypher query and executes it
        to create a new vector index in Neo4j.
        """
        index_query = (
            f"CREATE VECTOR INDEX {self.index_name} "
            f"FOR (n:{self.node_label}) "
            f"ON n.{self.embedding_node_property} "
            "OPTIONS { indexConfig: {"
            "`vector.dimensions`: toInteger($embedding_dimension), "
            "`vector.similarity_function`: $similarity_metric"
            "}"
            "}"
        )

        parameters = {
            "embedding_dimension": self.embedding_dimension,
            "similarity_metric": self.distance_strategy,
        }
        self.database_query(index_query, params=parameters)

    defretrieve_existing_index(self) -> bool:
"""
        Check if the vector index exists in the Neo4j database
        and returns its embedding dimension.

        This method queries the Neo4j database for existing indexes
        and attempts to retrieve the dimension of the vector index
        with the specified name. If the index exists, its dimension is returned.
        If the index doesn't exist, `None` is returned.

        Returns:
            int or None: The embedding dimension of the existing index if found.

        """
        index_information = self.database_query(
            "SHOW INDEXES YIELD name, type, labelsOrTypes, properties, options "
            "WHERE type = 'VECTOR' AND (name = $index_name "
            "OR (labelsOrTypes[0] = $node_label AND "
            "properties[0] = $embedding_node_property)) "
            "RETURN name, labelsOrTypes, properties, options ",
            params={
                "index_name": self.index_name,
                "node_label": self.node_label,
                "embedding_node_property": self.embedding_node_property,
            },
        )
        # sort by index_name
        index_information = sort_by_index_name(index_information, self.index_name)
        try:
            self.index_name = index_information[0]["name"]
            self.node_label = index_information[0]["labelsOrTypes"][0]
            self.embedding_node_property = index_information[0]["properties"][0]
            index_config = index_information[0]["options"]["indexConfig"]
            if "vector.dimensions" in index_config:
                self.embedding_dimension = index_config["vector.dimensions"]

            return True
        except IndexError:
            return False

    defretrieve_existing_fts_index(self) -> Optional[str]:
"""
        Check if the fulltext index exists in the Neo4j database.

        This method queries the Neo4j database for existing fts indexes
        with the specified name.

        Returns:
            (Tuple): keyword index information

        """
        index_information = self.database_query(
            "SHOW INDEXES YIELD name, type, labelsOrTypes, properties, options "
            "WHERE type = 'FULLTEXT' AND (name = $keyword_index_name "
            "OR (labelsOrTypes = [$node_label] AND "
            "properties = $text_node_property)) "
            "RETURN name, labelsOrTypes, properties, options ",
            params={
                "keyword_index_name": self.keyword_index_name,
                "node_label": self.node_label,
                "text_node_property": self.text_node_property,
            },
        )
        # sort by index_name
        index_information = sort_by_index_name(index_information, self.index_name)
        try:
            self.keyword_index_name = index_information[0]["name"]
            self.text_node_property = index_information[0]["properties"][0]
            return index_information[0]["labelsOrTypes"][0]
        except IndexError:
            return None

    defcreate_new_keyword_index(self, text_node_properties: List[str] = []) -> None:
"""
        This method constructs a Cypher query and executes it
        to create a new full text index in Neo4j.
        """
        node_props = text_node_properties or [self.text_node_property]
        fts_index_query = (
            f"CREATE FULLTEXT INDEX {self.keyword_index_name} "
            f"FOR (n:`{self.node_label}`) ON EACH "
            f"[{', '.join(['n.`'+el+'`'forelinnode_props])}]"
        )
        self.database_query(fts_index_query)

    defdatabase_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        params = params or {}
        try:
            data, _, _ = self._driver.execute_query(
                query, database_=self._database, parameters_=params
            )
            return [r.data() for r in data]
        except neo4j.exceptions.Neo4jError as e:
            if not (
                (
                    (  # isCallInTransactionError
                        e.code == "Neo.DatabaseError.Statement.ExecutionFailed"
                        or e.code
                        == "Neo.DatabaseError.Transaction.TransactionStartFailed"
                    )
                    and "in an implicit transaction" in e.message
                )
                or (  # isPeriodicCommitError
                    e.code == "Neo.ClientError.Statement.SemanticError"
                    and (
                        "in an open transaction is not possible" in e.message
                        or "tried to execute in an explicit transaction" in e.message
                    )
                )
            ):
                raise
        # Fallback to allow implicit transactions
        with self._driver.session(database=self._database) as session:
            data = session.run(neo4j.Query(text=query), params)
            return [r.data() for r in data]

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
        ids = [r.node_id for r in nodes]
        import_query = (
            "UNWIND $data AS row "
            f"{'CALL (row) { 'ifself._call_param_requiredelse'CALL { WITH row '}"
            f"MERGE (c:`{self.node_label}` {{id: row.id}}) "
            "WITH c, row "
            f"CALL db.create.setNodeVectorProperty(c, "
            f"'{self.embedding_node_property}', row.embedding) "
            f"SET c.`{self.text_node_property}` = row.text "
            "SET c += row.metadata } IN TRANSACTIONS OF 1000 ROWS"
        )

        self.database_query(
            import_query,
            params={"data": clean_params(nodes)},
        )

        return ids

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        if query.filters:
            # Verify that 5.18 or later is used
            if not self._support_metadata_filter:
                raise ValueError(
                    "Metadata filtering is only supported in "
                    "Neo4j version 5.18 or greater"
                )
            # Metadata filtering and hybrid doesn't work
            if self.hybrid_search:
                raise ValueError(
                    "Metadata filtering can't be use in combination with "
                    "a hybrid search approach"
                )
            parallel_query = (
                "CYPHER runtime = parallel parallelRuntimeSupport=all "
                if self._is_enterprise
                else ""
            )
            base_index_query = parallel_query + (
                f"MATCH (n:`{self.node_label}`) WHERE "
                f"n.`{self.embedding_node_property}` IS NOT NULL AND "
            )
            if self.embedding_dimension:
                base_index_query += (
                    f"size(n.`{self.embedding_node_property}`) = "
                    f"toInteger({self.embedding_dimension}) AND "
                )
            base_cosine_query = (
                " WITH n as node, vector.similarity.cosine("
                f"n.`{self.embedding_node_property}`, "
                "$embedding) AS score ORDER BY score DESC LIMIT toInteger($k) "
            )
            filter_snippets, filter_params = construct_metadata_filter(query.filters)
            index_query = base_index_query + filter_snippets + base_cosine_query
        else:
            index_query = _get_search_index_query(self.hybrid_search)
            filter_params = {}

        default_retrieval = (
            f"RETURN node.`{self.text_node_property}` AS text, score, "
            "node.id AS id, "
            f"node {{.*, `{self.text_node_property}`: Null, "
            f"`{self.embedding_node_property}`: Null, id: Null }} AS metadata"
        )

        retrieval_query = self.retrieval_query or default_retrieval
        read_query = index_query + retrieval_query

        parameters = {
            "index": self.index_name,
            "k": query.similarity_top_k,
            "embedding": query.query_embedding,
            "keyword_index": self.keyword_index_name,
            "query": remove_lucene_chars(query.query_str),
            **filter_params,
        }

        results = self.database_query(read_query, params=parameters)

        nodes = []
        similarities = []
        ids = []
        for record in results:
            # Handle missing metadata
            metadata = record.setdefault("metadata", {})
            metadata.setdefault("_node_type", "TextNode")
            metadata.setdefault("_node_content", "{}")

            node = metadata_dict_to_node(record["metadata"])
            node.set_content(str(record["text"]))
            nodes.append(node)
            similarities.append(record["score"])
            ids.append(record["id"])

        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        self.database_query(
            f"MATCH (n:`{self.node_label}`) WHERE n.ref_doc_id = $id DETACH DELETE n",
            params={"id": ref_doc_id},
        )

```
 |  
| --- | --- |  
###  create_new_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/neo4jvector/#llama_index.vector_stores.neo4jvector.Neo4jVectorStore.create_new_index "Permanent link")

```
create_new_index() -> None

```

This method constructs a Cypher query and executes it to create a new vector index in Neo4j.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-neo4jvector/llama_index/vector_stores/neo4jvector/base.py`  
| 
```
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
```
 | 
```
defcreate_new_index(self) -> None:
"""
    This method constructs a Cypher query and executes it
    to create a new vector index in Neo4j.
    """
    index_query = (
        f"CREATE VECTOR INDEX {self.index_name} "
        f"FOR (n:{self.node_label}) "
        f"ON n.{self.embedding_node_property} "
        "OPTIONS { indexConfig: {"
        "`vector.dimensions`: toInteger($embedding_dimension), "
        "`vector.similarity_function`: $similarity_metric"
        "}"
        "}"
    )

    parameters = {
        "embedding_dimension": self.embedding_dimension,
        "similarity_metric": self.distance_strategy,
    }
    self.database_query(index_query, params=parameters)

```
 |  
| --- | --- |  
###  retrieve_existing_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/neo4jvector/#llama_index.vector_stores.neo4jvector.Neo4jVectorStore.retrieve_existing_index "Permanent link")

```
retrieve_existing_index() -> 

```

Check if the vector index exists in the Neo4j database and returns its embedding dimension.
This method queries the Neo4j database for existing indexes and attempts to retrieve the dimension of the vector index with the specified name. If the index exists, its dimension is returned. If the index doesn't exist, `None` is returned.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `bool`  |  int or None: The embedding dimension of the existing index if found.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-neo4jvector/llama_index/vector_stores/neo4jvector/base.py`  
| 
```
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
```
 | 
```
defretrieve_existing_index(self) -> bool:
"""
    Check if the vector index exists in the Neo4j database
    and returns its embedding dimension.

    This method queries the Neo4j database for existing indexes
    and attempts to retrieve the dimension of the vector index
    with the specified name. If the index exists, its dimension is returned.
    If the index doesn't exist, `None` is returned.

    Returns:
        int or None: The embedding dimension of the existing index if found.

    """
    index_information = self.database_query(
        "SHOW INDEXES YIELD name, type, labelsOrTypes, properties, options "
        "WHERE type = 'VECTOR' AND (name = $index_name "
        "OR (labelsOrTypes[0] = $node_label AND "
        "properties[0] = $embedding_node_property)) "
        "RETURN name, labelsOrTypes, properties, options ",
        params={
            "index_name": self.index_name,
            "node_label": self.node_label,
            "embedding_node_property": self.embedding_node_property,
        },
    )
    # sort by index_name
    index_information = sort_by_index_name(index_information, self.index_name)
    try:
        self.index_name = index_information[0]["name"]
        self.node_label = index_information[0]["labelsOrTypes"][0]
        self.embedding_node_property = index_information[0]["properties"][0]
        index_config = index_information[0]["options"]["indexConfig"]
        if "vector.dimensions" in index_config:
            self.embedding_dimension = index_config["vector.dimensions"]

        return True
    except IndexError:
        return False

```
 |  
| --- | --- |  
###  retrieve_existing_fts_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/neo4jvector/#llama_index.vector_stores.neo4jvector.Neo4jVectorStore.retrieve_existing_fts_index "Permanent link")

```
retrieve_existing_fts_index() -> Optional[]

```

Check if the fulltext index exists in the Neo4j database.
This method queries the Neo4j database for existing fts indexes with the specified name.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Tuple`  |  keyword index information  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-neo4jvector/llama_index/vector_stores/neo4jvector/base.py`  
| 
```
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
```
 | 
```
defretrieve_existing_fts_index(self) -> Optional[str]:
"""
    Check if the fulltext index exists in the Neo4j database.

    This method queries the Neo4j database for existing fts indexes
    with the specified name.

    Returns:
        (Tuple): keyword index information

    """
    index_information = self.database_query(
        "SHOW INDEXES YIELD name, type, labelsOrTypes, properties, options "
        "WHERE type = 'FULLTEXT' AND (name = $keyword_index_name "
        "OR (labelsOrTypes = [$node_label] AND "
        "properties = $text_node_property)) "
        "RETURN name, labelsOrTypes, properties, options ",
        params={
            "keyword_index_name": self.keyword_index_name,
            "node_label": self.node_label,
            "text_node_property": self.text_node_property,
        },
    )
    # sort by index_name
    index_information = sort_by_index_name(index_information, self.index_name)
    try:
        self.keyword_index_name = index_information[0]["name"]
        self.text_node_property = index_information[0]["properties"][0]
        return index_information[0]["labelsOrTypes"][0]
    except IndexError:
        return None

```
 |  
| --- | --- |  
###  create_new_keyword_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/neo4jvector/#llama_index.vector_stores.neo4jvector.Neo4jVectorStore.create_new_keyword_index "Permanent link")

```
create_new_keyword_index(
    text_node_properties: [] = [],
) -> None

```

This method constructs a Cypher query and executes it to create a new full text index in Neo4j.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-neo4jvector/llama_index/vector_stores/neo4jvector/base.py`  
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
```
 | 
```
defcreate_new_keyword_index(self, text_node_properties: List[str] = []) -> None:
"""
    This method constructs a Cypher query and executes it
    to create a new full text index in Neo4j.
    """
    node_props = text_node_properties or [self.text_node_property]
    fts_index_query = (
        f"CREATE FULLTEXT INDEX {self.keyword_index_name} "
        f"FOR (n:`{self.node_label}`) ON EACH "
        f"[{', '.join(['n.`'+el+'`'forelinnode_props])}]"
    )
    self.database_query(fts_index_query)

```
 |  
| --- | --- |  
options: members: - Neo4jVectorStore
