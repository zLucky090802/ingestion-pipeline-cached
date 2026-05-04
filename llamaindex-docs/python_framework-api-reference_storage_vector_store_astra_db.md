# Astra db
##  AstraDBVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/astra_db/#llama_index.vector_stores.astra_db.AstraDBVectorStore "Permanent link")
Bases: 
Astra DB Vector Store.
An abstraction of a Astra DB collection with vector-similarity-search. Documents, and their embeddings, are stored in an Astra DB collection equipped with a vector index. The collection, if necessary, is created when the vector store is initialized.
All Astra operations are done through the AstraPy library.
Visit https://astra.datastax.com/signup to create an account and get started.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection_name`  |  collection name to use. If not existing, it will be created.  |  _required_  |  
|  `token`  |  The Astra DB Application Token to use.  |  _required_  |  
|  `api_endpoint`  |  The Astra DB JSON API endpoint for your database.  |  _required_  |  
|  `embedding_dimension`  |  length of the embedding vectors in use.  |  _required_  |  
|  `keyspace`  |  `Optional[str]`  |  The keyspace to use. If not provided, 'default_keyspace'  |  `None`  |  
|  `namespace`  |  `Optional[str]`  |  [DEPRECATED] The keyspace to use. If not provided, 'default_keyspace'  |  `None`  |  
Examples:
`pip install llama-index-vector-stores-astra`

```
fromllama_index.vector_stores.astraimport AstraDBVectorStore

# Create the Astra DB Vector Store object
astra_db_store = AstraDBVectorStore(
    collection_name="astra_v_store",
    token=token,
    api_endpoint=api_endpoint,
    embedding_dimension=1536,
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-astra-db/llama_index/vector_stores/astra_db/base.py`  
| 
```
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
```
 | 
```
classAstraDBVectorStore(BasePydanticVectorStore):
"""
    Astra DB Vector Store.

    An abstraction of a Astra DB collection with
    vector-similarity-search. Documents, and their embeddings, are stored
    in an Astra DB collection equipped with a vector index.
    The collection, if necessary, is created when the vector store is initialized.

    All Astra operations are done through the AstraPy library.

    Visit https://astra.datastax.com/signup to create an account and get started.

    Args:
        collection_name (str): collection name to use. If not existing, it will be created.
        token (str): The Astra DB Application Token to use.
        api_endpoint (str): The Astra DB JSON API endpoint for your database.
        embedding_dimension (int): length of the embedding vectors in use.
        keyspace (Optional[str]): The keyspace to use. If not provided, 'default_keyspace'
        namespace (Optional[str]): [DEPRECATED] The keyspace to use. If not provided, 'default_keyspace'

    Examples:
        `pip install llama-index-vector-stores-astra`

        ```python
        from llama_index.vector_stores.astra import AstraDBVectorStore

        # Create the Astra DB Vector Store object
        astra_db_store = AstraDBVectorStore(
            collection_name="astra_v_store",
            token=token,
            api_endpoint=api_endpoint,
            embedding_dimension=1536,

        ```

    """

    stores_text: bool = True
    flat_metadata: bool = True

    _embedding_dimension: int = PrivateAttr()
    _database: Any = PrivateAttr()
    _collection: Any = PrivateAttr()

    def__init__(
        self,
        *,
        collection_name: str,
        token: str,
        api_endpoint: str,
        embedding_dimension: int,
        keyspace: Optional[str] = None,
        namespace: Optional[str] = None,
        ttl_seconds: Optional[int] = None,
    ) -> None:
        super().__init__()

        # Set all the required class parameters
        self._embedding_dimension = embedding_dimension

        if ttl_seconds is not None:
            warn(
                (
                    "Parameter `ttl_seconds` is not supported for "
                    "`AstraDBVectorStore` and will be ignored."
                ),
                UserWarning,
                stacklevel=2,
            )

        _logger.debug("Creating the Astra DB client and database instances")

        # Choose the keyspace param
        keyspace_param = keyspace or namespace

        # Build the Database object
        self._database = DataAPIClient(
            caller_name=getattr(llama_index, "__name__", "llama_index"),
            caller_version=getattr(llama_index.core, "__version__", None),
        ).get_database(
            api_endpoint,
            token=token,
            keyspace=keyspace_param,
        )

        fromastrapy.exceptionsimport DataAPIException

        collection_indexing = {"deny": NON_INDEXED_FIELDS}

        try:
            _logger.debug("Creating the Astra DB collection")
            # Create and connect to the newly created collection
            self._collection = self._database.create_collection(
                name=collection_name,
                dimension=embedding_dimension,
                indexing=collection_indexing,
                check_exists=False,
            )
        except DataAPIException as e:
            # possibly the collection is preexisting and has legacy
            # indexing settings: verify
            preexisting = [
                coll_descriptor
                for coll_descriptor in self._database.list_collections()
                if coll_descriptor.name == collection_name
            ]
            if preexisting:
                # if it has no "indexing", it is a legacy collection;
                # otherwise it's unexpected: warn and proceed at user's risk
                pre_col_idx_opts = preexisting[0].options.indexing or {}
                if not pre_col_idx_opts:
                    warn(
                        (
                            f"Collection '{collection_name}' is detected as "
                            "having indexing turned on for all fields "
                            "(either created manually or by older versions "
                            "of this plugin). This implies stricter "
                            "limitations on the amount of text"
                            " each entry can store. Consider indexing anew on a"
                            " fresh collection to be able to store longer texts."
                        ),
                        UserWarning,
                        stacklevel=2,
                    )
                    self._collection = self._database.get_collection(
                        collection_name,
                    )
                else:
                    # check if the indexing options match entirely
                    if pre_col_idx_opts == collection_indexing:
                        raise
                    else:
                        options_json = json.dumps(pre_col_idx_opts)
                        warn(
                            (
                                f"Collection '{collection_name}' has unexpected 'indexing'"
                                f" settings (options.indexing = {options_json})."
                                " This can result in odd behaviour when running "
                                " metadata filtering and/or unwarranted limitations"
                                " on storing long texts. Consider indexing anew on a"
                                " fresh collection."
                            ),
                            UserWarning,
                            stacklevel=2,
                        )
                        self._collection = self._database.get_collection(
                            collection_name,
                        )
            else:
                # other exception
                raise

    @classmethod
    deffrom_params(
        cls,
        collection_name: str,
        token: str,
        api_endpoint: str,
        embedding_dimension: int,
        keyspace: Optional[str] = None,
        namespace: Optional[str] = None,
        ttl_seconds: Optional[int] = None,
        **kwargs: Any,
    ) -> "AstraDBVectorStore":
"""
        Create an AstraDBVectorStore from parameters.

        Args:
            collection_name (str): collection name to use. If not existing, it will be created.
            token (str): The Astra DB Application Token to use.
            api_endpoint (str): The Astra DB JSON API endpoint for your database.
            embedding_dimension (int): length of the embedding vectors in use.
            keyspace (Optional[str]): The keyspace to use. If not provided, 'default_keyspace'
            namespace (Optional[str]): [DEPRECATED] The keyspace to use. If not provided, 'default_keyspace'
            ttl_seconds (Optional[int]): TTL in seconds (not supported, will be ignored).

        Returns:
            AstraDBVectorStore: A new instance of AstraDBVectorStore.

        """
        return cls(
            collection_name=collection_name,
            token=token,
            api_endpoint=api_endpoint,
            embedding_dimension=embedding_dimension,
            keyspace=keyspace,
            namespace=namespace,
            ttl_seconds=ttl_seconds,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Return the class name."""
        return "AstraDBVectorStore"

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to index.

        Args:
            nodes: List[BaseNode]: list of node with embeddings

        """
        # Initialize list of documents to insert
        documents_to_insert: List[Dict[str, Any]] = []

        # Process each node individually
        for node in nodes:
            # Get the metadata
            metadata = node_to_metadata_dict(
                node,
                remove_text=True,
                flat_metadata=self.flat_metadata,
            )

            # One dictionary of node data per node
            documents_to_insert.append(
                {
                    "_id": node.node_id,
                    "content": node.get_content(metadata_mode=MetadataMode.NONE),
                    "metadata": metadata,
                    "$vector": node.get_embedding(),
                }
            )

        # Log the number of documents being added
        _logger.debug(f"Adding {len(documents_to_insert)} documents to the collection")

        # perform an AstraPy insert_many, catching exceptions for overwriting docs
        ids_to_replace: List[int]
        try:
            self._collection.insert_many(
                documents_to_insert,
                ordered=False,
            )
            ids_to_replace = []
        except InsertManyException as err:
            inserted_ids_set = set(err.partial_result.inserted_ids)
            ids_to_replace = [
                document["_id"]
                for document in documents_to_insert
                if document["_id"] not in inserted_ids_set
            ]
            _logger.debug(
                f"Detected {len(ids_to_replace)} non-inserted documents, trying replace_one"
            )

        # if necessary, replace docs for the non-inserted ids
        if ids_to_replace:
            documents_to_replace = [
                document
                for document in documents_to_insert
                if document["_id"] in ids_to_replace
            ]

            with ThreadPoolExecutor(
                max_workers=REPLACE_DOCUMENTS_MAX_THREADS
            ) as executor:

                def_replace_document(document: Dict[str, Any]) -> UpdateResult:
                    return self._collection.replace_one(
                        {"_id": document["_id"]},
                        document,
                    )

                replace_results = executor.map(
                    _replace_document,
                    documents_to_replace,
                )

            replaced_count = sum(r_res.update_info["n"] for r_res in replace_results)
            if replaced_count != len(ids_to_replace):
                missing = len(ids_to_replace) - replaced_count
                raise ValueError(
                    "AstraDBVectorStore.add could not insert all requested "
                    f"documents ({missing} failed replace_one calls)"
                )

        # Return the list of ids
        return [str(n["_id"]) for n in documents_to_insert]

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The id of the document to delete.

        """
        _logger.debug("Deleting a document from the Astra DB collection")

        if delete_kwargs:
            args_desc = ", ".join(
                f"'{kwarg}'" for kwarg in sorted(delete_kwargs.keys())
            )
            warn(
                (
                    "AstraDBVectorStore.delete call got unsupported "
                    f"named argument(s): {args_desc}."
                ),
                UserWarning,
                stacklevel=2,
            )

        self._collection.delete_one({"_id": ref_doc_id})

    defget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        limit: int = 100,
    ) -> List[BaseNode]:
"""
        Get nodes by node IDs or filters.

        Args:
            node_ids (Optional[List[str]]): List of node IDs to retrieve.
            filters (Optional[MetadataFilters]): Metadata filters to apply.
            limit (int): Maximum number of nodes to retrieve. Defaults to 100.

        Returns:
            List[BaseNode]: List of retrieved nodes.

        """
        if node_ids is not None and filters is not None:
            raise ValueError("Cannot specify both node_ids and filters")

        if node_ids is None and filters is None:
            raise ValueError("Must specify either node_ids or filters")

        # Build the filter query
        if node_ids is not None:
            # Query by node IDs
            if len(node_ids) == 1:
                filter_query = {"_id": node_ids[0]}
            else:
                filter_query = {"_id": {"$in": node_ids}}
        else:
            # Query by metadata filters
            filter_query = self._query_filters_to_dict(filters)

        # Perform the query
        matches = list(
            self._collection.find(
                filter=filter_query,
                projection={"*": True},
                limit=limit,
            )
        )

        # Convert to nodes
        nodes = []
        for match in matches:
            # Check whether we have a llama-generated node content field
            if "_node_content" not in match["metadata"]:
                match["metadata"]["_node_content"] = json.dumps(match)

            # Create a new node object from the node metadata
            node = metadata_dict_to_node(match["metadata"], text=match["content"])
            nodes.append(node)

        return nodes

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Delete nodes by node IDs or filters.

        Args:
            node_ids (Optional[List[str]]): List of node IDs to delete.
            filters (Optional[MetadataFilters]): Metadata filters to apply for deletion.

        """
        if delete_kwargs:
            args_desc = ", ".join(
                f"'{kwarg}'" for kwarg in sorted(delete_kwargs.keys())
            )
            warn(
                (
                    "AstraDBVectorStore.delete_nodes call got unsupported "
                    f"named argument(s): {args_desc}."
                ),
                UserWarning,
                stacklevel=2,
            )

        if node_ids is not None and filters is not None:
            raise ValueError("Cannot specify both node_ids and filters")

        if node_ids is None and filters is None:
            raise ValueError("Must specify either node_ids or filters")

        # Build the filter query
        if node_ids is not None:
            # Delete by node IDs
            if len(node_ids) == 1:
                delete_result = self._collection.delete_one({"_id": node_ids[0]})
                _logger.debug(f"Deleted {delete_result.deleted_count} documents")
            else:
                delete_result = self._collection.delete_many({"_id": {"$in": node_ids}})
                _logger.debug(f"Deleted {delete_result.deleted_count} documents")
        else:
            # Delete by metadata filters
            filter_query = self._query_filters_to_dict(filters)
            delete_result = self._collection.delete_many(filter_query)
            _logger.debug(f"Deleted {delete_result.deleted_count} documents")

    @property
    defclient(self) -> Any:
"""Return the underlying Astra DB `astrapy.Collection` object."""
        return self._collection

    @staticmethod
    def_query_filters_to_dict(query_filters: MetadataFilters) -> Dict[str, Any]:
        # Allow only legacy ExactMatchFilter and MetadataFilter with FilterOperator.EQ
        if not all(
            (
                isinstance(f, ExactMatchFilter)
                or (isinstance(f, MetadataFilter) and f.operator == FilterOperator.EQ)
            )
            for f in query_filters.filters
        ):
            raise NotImplementedError(
                "Only filters with operator=FilterOperator.EQ are supported"
            )
        # nested filters, i.e. f being of type MetadataFilters, is excluded above:
        return {f"metadata.{f.key}": f.value for f in query_filters.filters}  # type: ignore[union-attr]

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query index for top k most similar nodes."""
        # Get the currently available query modes
        _available_query_modes = [
            VectorStoreQueryMode.DEFAULT,
            VectorStoreQueryMode.MMR,
        ]

        # Reject query if not available
        if query.mode not in _available_query_modes:
            raise NotImplementedError(f"Query mode {query.mode} not available.")

        # Get the query embedding
        query_embedding = cast(List[float], query.query_embedding)

        # Process the metadata filters as needed
        if query.filters is not None:
            query_metadata = self._query_filters_to_dict(query.filters)
        else:
            query_metadata = {}

        matches: List[Dict[str, Any]]

        # Get the scores depending on the query mode
        if query.mode == VectorStoreQueryMode.DEFAULT:
            # Call the vector_find method of AstraPy
            matches = list(
                self._collection.find(
                    filter=query_metadata,
                    projection={"*": True},
                    limit=query.similarity_top_k,
                    sort={"$vector": query_embedding},
                    include_similarity=True,
                )
            )

            # Get the scores associated with each
            top_k_scores = [match["$similarity"] for match in matches]
        elif query.mode == VectorStoreQueryMode.MMR:
            # Querying a larger number of vectors and then doing MMR on them.
            if (
                kwargs.get("mmr_prefetch_factor") is not None
                and kwargs.get("mmr_prefetch_k") is not None
            ):
                raise ValueError(
                    "'mmr_prefetch_factor' and 'mmr_prefetch_k' "
                    "cannot coexist in a call to query()"
                )
            else:
                if kwargs.get("mmr_prefetch_k") is not None:
                    prefetch_k0 = int(kwargs["mmr_prefetch_k"])
                else:
                    prefetch_k0 = int(
                        query.similarity_top_k
                        * kwargs.get("mmr_prefetch_factor", DEFAULT_MMR_PREFETCH_FACTOR)
                    )
            # Get the most we can possibly need to fetch
            prefetch_k = max(prefetch_k0, query.similarity_top_k)

            # Call AstraPy to fetch them (similarity from DB not needed here)
            prefetch_matches = list(
                self._collection.find(
                    filter=query_metadata,
                    projection={"*": True},
                    limit=prefetch_k,
                    sort={"$vector": query_embedding},
                )
            )

            # Get the MMR threshold
            mmr_threshold = query.mmr_threshold or kwargs.get("mmr_threshold")

            # If we have found documents, we can proceed
            if prefetch_matches:
                zipped_indices, zipped_embeddings = zip(
                    *enumerate(match["$vector"] for match in prefetch_matches)
                )
                pf_match_indices, pf_match_embeddings = (
                    list(zipped_indices),
                    list(zipped_embeddings),
                )
            else:
                pf_match_indices, pf_match_embeddings = [], []

            # Call the Llama utility function to get the top  k
            mmr_similarities, mmr_indices = get_top_k_mmr_embeddings(
                query_embedding,
                pf_match_embeddings,
                similarity_top_k=query.similarity_top_k,
                embedding_ids=pf_match_indices,
                mmr_threshold=mmr_threshold,
            )

            # Finally, build the final results based on the mmr values
            matches = [prefetch_matches[mmr_index] for mmr_index in mmr_indices]
            top_k_scores = mmr_similarities

        # We have three lists to return
        top_k_nodes = []
        top_k_ids = []

        # Get every match
        for match in matches:
            # Check whether we have a llama-generated node content field
            if "_node_content" not in match["metadata"]:
                match["metadata"]["_node_content"] = json.dumps(match)

            # Create a new node object from the node metadata
            node = metadata_dict_to_node(match["metadata"], text=match["content"])

            # Append to the respective lists
            top_k_nodes.append(node)
            top_k_ids.append(match["_id"])

        # return our final result
        return VectorStoreQueryResult(
            nodes=top_k_nodes,
            similarities=top_k_scores,
            ids=top_k_ids,
        )

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/astra_db/#llama_index.vector_stores.astra_db.AstraDBVectorStore.client "Permanent link")

```
client: 

```

Return the underlying Astra DB `astrapy.Collection` object.
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/astra_db/#llama_index.vector_stores.astra_db.AstraDBVectorStore.from_params "Permanent link")

```
from_params(
    collection_name: ,
    token: ,
    api_endpoint: ,
    embedding_dimension: ,
    keyspace: Optional[] = None,
    namespace: Optional[] = None,
    ttl_seconds: Optional[] = None,
    **kwargs: 
) -> 

```

Create an AstraDBVectorStore from parameters.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection_name`  |  collection name to use. If not existing, it will be created.  |  _required_  |  
|  `token`  |  The Astra DB Application Token to use.  |  _required_  |  
|  `api_endpoint`  |  The Astra DB JSON API endpoint for your database.  |  _required_  |  
|  `embedding_dimension`  |  length of the embedding vectors in use.  |  _required_  |  
|  `keyspace`  |  `Optional[str]`  |  The keyspace to use. If not provided, 'default_keyspace'  |  `None`  |  
|  `namespace`  |  `Optional[str]`  |  [DEPRECATED] The keyspace to use. If not provided, 'default_keyspace'  |  `None`  |  
|  `ttl_seconds`  |  `Optional[int]`  |  TTL in seconds (not supported, will be ignored).  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `AstraDBVectorStore`  |   |  A new instance of AstraDBVectorStore.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-astra-db/llama_index/vector_stores/astra_db/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_params(
    cls,
    collection_name: str,
    token: str,
    api_endpoint: str,
    embedding_dimension: int,
    keyspace: Optional[str] = None,
    namespace: Optional[str] = None,
    ttl_seconds: Optional[int] = None,
    **kwargs: Any,
) -> "AstraDBVectorStore":
"""
    Create an AstraDBVectorStore from parameters.

    Args:
        collection_name (str): collection name to use. If not existing, it will be created.
        token (str): The Astra DB Application Token to use.
        api_endpoint (str): The Astra DB JSON API endpoint for your database.
        embedding_dimension (int): length of the embedding vectors in use.
        keyspace (Optional[str]): The keyspace to use. If not provided, 'default_keyspace'
        namespace (Optional[str]): [DEPRECATED] The keyspace to use. If not provided, 'default_keyspace'
        ttl_seconds (Optional[int]): TTL in seconds (not supported, will be ignored).

    Returns:
        AstraDBVectorStore: A new instance of AstraDBVectorStore.

    """
    return cls(
        collection_name=collection_name,
        token=token,
        api_endpoint=api_endpoint,
        embedding_dimension=embedding_dimension,
        keyspace=keyspace,
        namespace=namespace,
        ttl_seconds=ttl_seconds,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/astra_db/#llama_index.vector_stores.astra_db.AstraDBVectorStore.class_name "Permanent link")

```
class_name() -> 

```

Return the class name.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-astra-db/llama_index/vector_stores/astra_db/base.py`  
| 
```
239
240
241
242
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Return the class name."""
    return "AstraDBVectorStore"

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/astra_db/#llama_index.vector_stores.astra_db.AstraDBVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of node with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-astra-db/llama_index/vector_stores/astra_db/base.py`  
| 
```
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
        nodes: List[BaseNode]: list of node with embeddings

    """
    # Initialize list of documents to insert
    documents_to_insert: List[Dict[str, Any]] = []

    # Process each node individually
    for node in nodes:
        # Get the metadata
        metadata = node_to_metadata_dict(
            node,
            remove_text=True,
            flat_metadata=self.flat_metadata,
        )

        # One dictionary of node data per node
        documents_to_insert.append(
            {
                "_id": node.node_id,
                "content": node.get_content(metadata_mode=MetadataMode.NONE),
                "metadata": metadata,
                "$vector": node.get_embedding(),
            }
        )

    # Log the number of documents being added
    _logger.debug(f"Adding {len(documents_to_insert)} documents to the collection")

    # perform an AstraPy insert_many, catching exceptions for overwriting docs
    ids_to_replace: List[int]
    try:
        self._collection.insert_many(
            documents_to_insert,
            ordered=False,
        )
        ids_to_replace = []
    except InsertManyException as err:
        inserted_ids_set = set(err.partial_result.inserted_ids)
        ids_to_replace = [
            document["_id"]
            for document in documents_to_insert
            if document["_id"] not in inserted_ids_set
        ]
        _logger.debug(
            f"Detected {len(ids_to_replace)} non-inserted documents, trying replace_one"
        )

    # if necessary, replace docs for the non-inserted ids
    if ids_to_replace:
        documents_to_replace = [
            document
            for document in documents_to_insert
            if document["_id"] in ids_to_replace
        ]

        with ThreadPoolExecutor(
            max_workers=REPLACE_DOCUMENTS_MAX_THREADS
        ) as executor:

            def_replace_document(document: Dict[str, Any]) -> UpdateResult:
                return self._collection.replace_one(
                    {"_id": document["_id"]},
                    document,
                )

            replace_results = executor.map(
                _replace_document,
                documents_to_replace,
            )

        replaced_count = sum(r_res.update_info["n"] for r_res in replace_results)
        if replaced_count != len(ids_to_replace):
            missing = len(ids_to_replace) - replaced_count
            raise ValueError(
                "AstraDBVectorStore.add could not insert all requested "
                f"documents ({missing} failed replace_one calls)"
            )

    # Return the list of ids
    return [str(n["_id"]) for n in documents_to_insert]

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/astra_db/#llama_index.vector_stores.astra_db.AstraDBVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-astra-db/llama_index/vector_stores/astra_db/base.py`  
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
354
355
356
357
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The id of the document to delete.

    """
    _logger.debug("Deleting a document from the Astra DB collection")

    if delete_kwargs:
        args_desc = ", ".join(
            f"'{kwarg}'" for kwarg in sorted(delete_kwargs.keys())
        )
        warn(
            (
                "AstraDBVectorStore.delete call got unsupported "
                f"named argument(s): {args_desc}."
            ),
            UserWarning,
            stacklevel=2,
        )

    self._collection.delete_one({"_id": ref_doc_id})

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/astra_db/#llama_index.vector_stores.astra_db.AstraDBVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    limit:  = 100,
) -> []

```

Get nodes by node IDs or filters.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  List of node IDs to retrieve.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters to apply.  |  `None`  |  
|  `limit`  |  Maximum number of nodes to retrieve. Defaults to 100.  |  `100`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[BaseNode]: List of retrieved nodes.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-astra-db/llama_index/vector_stores/astra_db/base.py`  
| 
```
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
```
 | 
```
defget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    limit: int = 100,
) -> List[BaseNode]:
"""
    Get nodes by node IDs or filters.

    Args:
        node_ids (Optional[List[str]]): List of node IDs to retrieve.
        filters (Optional[MetadataFilters]): Metadata filters to apply.
        limit (int): Maximum number of nodes to retrieve. Defaults to 100.

    Returns:
        List[BaseNode]: List of retrieved nodes.

    """
    if node_ids is not None and filters is not None:
        raise ValueError("Cannot specify both node_ids and filters")

    if node_ids is None and filters is None:
        raise ValueError("Must specify either node_ids or filters")

    # Build the filter query
    if node_ids is not None:
        # Query by node IDs
        if len(node_ids) == 1:
            filter_query = {"_id": node_ids[0]}
        else:
            filter_query = {"_id": {"$in": node_ids}}
    else:
        # Query by metadata filters
        filter_query = self._query_filters_to_dict(filters)

    # Perform the query
    matches = list(
        self._collection.find(
            filter=filter_query,
            projection={"*": True},
            limit=limit,
        )
    )

    # Convert to nodes
    nodes = []
    for match in matches:
        # Check whether we have a llama-generated node content field
        if "_node_content" not in match["metadata"]:
            match["metadata"]["_node_content"] = json.dumps(match)

        # Create a new node object from the node metadata
        node = metadata_dict_to_node(match["metadata"], text=match["content"])
        nodes.append(node)

    return nodes

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/astra_db/#llama_index.vector_stores.astra_db.AstraDBVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Delete nodes by node IDs or filters.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  List of node IDs to delete.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters to apply for deletion.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-astra-db/llama_index/vector_stores/astra_db/base.py`  
| 
```
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
```
 | 
```
defdelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Delete nodes by node IDs or filters.

    Args:
        node_ids (Optional[List[str]]): List of node IDs to delete.
        filters (Optional[MetadataFilters]): Metadata filters to apply for deletion.

    """
    if delete_kwargs:
        args_desc = ", ".join(
            f"'{kwarg}'" for kwarg in sorted(delete_kwargs.keys())
        )
        warn(
            (
                "AstraDBVectorStore.delete_nodes call got unsupported "
                f"named argument(s): {args_desc}."
            ),
            UserWarning,
            stacklevel=2,
        )

    if node_ids is not None and filters is not None:
        raise ValueError("Cannot specify both node_ids and filters")

    if node_ids is None and filters is None:
        raise ValueError("Must specify either node_ids or filters")

    # Build the filter query
    if node_ids is not None:
        # Delete by node IDs
        if len(node_ids) == 1:
            delete_result = self._collection.delete_one({"_id": node_ids[0]})
            _logger.debug(f"Deleted {delete_result.deleted_count} documents")
        else:
            delete_result = self._collection.delete_many({"_id": {"$in": node_ids}})
            _logger.debug(f"Deleted {delete_result.deleted_count} documents")
    else:
        # Delete by metadata filters
        filter_query = self._query_filters_to_dict(filters)
        delete_result = self._collection.delete_many(filter_query)
        _logger.debug(f"Deleted {delete_result.deleted_count} documents")

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/astra_db/#llama_index.vector_stores.astra_db.AstraDBVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-astra-db/llama_index/vector_stores/astra_db/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query index for top k most similar nodes."""
    # Get the currently available query modes
    _available_query_modes = [
        VectorStoreQueryMode.DEFAULT,
        VectorStoreQueryMode.MMR,
    ]

    # Reject query if not available
    if query.mode not in _available_query_modes:
        raise NotImplementedError(f"Query mode {query.mode} not available.")

    # Get the query embedding
    query_embedding = cast(List[float], query.query_embedding)

    # Process the metadata filters as needed
    if query.filters is not None:
        query_metadata = self._query_filters_to_dict(query.filters)
    else:
        query_metadata = {}

    matches: List[Dict[str, Any]]

    # Get the scores depending on the query mode
    if query.mode == VectorStoreQueryMode.DEFAULT:
        # Call the vector_find method of AstraPy
        matches = list(
            self._collection.find(
                filter=query_metadata,
                projection={"*": True},
                limit=query.similarity_top_k,
                sort={"$vector": query_embedding},
                include_similarity=True,
            )
        )

        # Get the scores associated with each
        top_k_scores = [match["$similarity"] for match in matches]
    elif query.mode == VectorStoreQueryMode.MMR:
        # Querying a larger number of vectors and then doing MMR on them.
        if (
            kwargs.get("mmr_prefetch_factor") is not None
            and kwargs.get("mmr_prefetch_k") is not None
        ):
            raise ValueError(
                "'mmr_prefetch_factor' and 'mmr_prefetch_k' "
                "cannot coexist in a call to query()"
            )
        else:
            if kwargs.get("mmr_prefetch_k") is not None:
                prefetch_k0 = int(kwargs["mmr_prefetch_k"])
            else:
                prefetch_k0 = int(
                    query.similarity_top_k
                    * kwargs.get("mmr_prefetch_factor", DEFAULT_MMR_PREFETCH_FACTOR)
                )
        # Get the most we can possibly need to fetch
        prefetch_k = max(prefetch_k0, query.similarity_top_k)

        # Call AstraPy to fetch them (similarity from DB not needed here)
        prefetch_matches = list(
            self._collection.find(
                filter=query_metadata,
                projection={"*": True},
                limit=prefetch_k,
                sort={"$vector": query_embedding},
            )
        )

        # Get the MMR threshold
        mmr_threshold = query.mmr_threshold or kwargs.get("mmr_threshold")

        # If we have found documents, we can proceed
        if prefetch_matches:
            zipped_indices, zipped_embeddings = zip(
                *enumerate(match["$vector"] for match in prefetch_matches)
            )
            pf_match_indices, pf_match_embeddings = (
                list(zipped_indices),
                list(zipped_embeddings),
            )
        else:
            pf_match_indices, pf_match_embeddings = [], []

        # Call the Llama utility function to get the top  k
        mmr_similarities, mmr_indices = get_top_k_mmr_embeddings(
            query_embedding,
            pf_match_embeddings,
            similarity_top_k=query.similarity_top_k,
            embedding_ids=pf_match_indices,
            mmr_threshold=mmr_threshold,
        )

        # Finally, build the final results based on the mmr values
        matches = [prefetch_matches[mmr_index] for mmr_index in mmr_indices]
        top_k_scores = mmr_similarities

    # We have three lists to return
    top_k_nodes = []
    top_k_ids = []

    # Get every match
    for match in matches:
        # Check whether we have a llama-generated node content field
        if "_node_content" not in match["metadata"]:
            match["metadata"]["_node_content"] = json.dumps(match)

        # Create a new node object from the node metadata
        node = metadata_dict_to_node(match["metadata"], text=match["content"])

        # Append to the respective lists
        top_k_nodes.append(node)
        top_k_ids.append(match["_id"])

    # return our final result
    return VectorStoreQueryResult(
        nodes=top_k_nodes,
        similarities=top_k_scores,
        ids=top_k_ids,
    )

```
 |  
| --- | --- |  
options: members: - AstraDBVectorStore
