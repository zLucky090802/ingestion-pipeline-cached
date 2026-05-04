# Pinecone
##  PineconeVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/pinecone/#llama_index.vector_stores.pinecone.PineconeVectorStore "Permanent link")
Bases: 
Pinecone Vector Store.
In this vector store, embeddings and docs are stored within a Pinecone index.
During query time, the index uses Pinecone to query for the top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `pinecone_index`  |  `Optional[Union[Index, Index]]`  |  Pinecone index instance,  |  `None`  |  
|  `insert_kwargs`  |  `Optional[Dict]`  |  insert kwargs during `upsert` call.  |  `None`  |  
|  `add_sparse_vector`  |  `bool`  |  whether to add sparse vector to index.  |  `False`  |  
|  `tokenizer`  |  `Optional[Callable]`  |  tokenizer to use to generate sparse  |  `None`  |  
|  `default_empty_query_vector`  |  `Optional[List[float]]`  |  default empty query vector. Defaults to None. If not None, then this vector will be used as the query vector if the query is empty.  |  `None`  |  
Examples:
`pip install llama-index-vector-stores-pinecone`

```
importos
fromllama_index.vector_stores.pineconeimport PineconeVectorStore
frompineconeimport Pinecone, ServerlessSpec

# Set up Pinecone API key
os.environ["PINECONE_API_KEY"] = "<Your Pinecone API key, from app.pinecone.io>"
api_key = os.environ["PINECONE_API_KEY"]

# Create Pinecone Vector Store
pc = Pinecone(api_key=api_key)

pc.create_index(
    name="quickstart",
    dimension=1536,
    metric="dotproduct",
    spec=ServerlessSpec(cloud="aws", region="us-west-2"),
)

pinecone_index = pc.Index("quickstart")

vector_store = PineconeVectorStore(
    pinecone_index=pinecone_index,
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-pinecone/llama_index/vector_stores/pinecone/base.py`  
| 
```
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
```
 | 
```
classPineconeVectorStore(BasePydanticVectorStore):
"""
    Pinecone Vector Store.

    In this vector store, embeddings and docs are stored within a
    Pinecone index.

    During query time, the index uses Pinecone to query for the top
    k most similar nodes.

    Args:
        pinecone_index (Optional[Union[pinecone.Pinecone.Index, pinecone.Index]]): Pinecone index instance,
        pinecone.Pinecone.Index for clients >= 3.0.0; pinecone.Index for older clients.
        insert_kwargs (Optional[Dict]): insert kwargs during `upsert` call.
        add_sparse_vector (bool): whether to add sparse vector to index.
        tokenizer (Optional[Callable]): tokenizer to use to generate sparse
        default_empty_query_vector (Optional[List[float]]): default empty query vector.
            Defaults to None. If not None, then this vector will be used as the query
            vector if the query is empty.

    Examples:
        `pip install llama-index-vector-stores-pinecone`

        ```python
        import os
        from llama_index.vector_stores.pinecone import PineconeVectorStore
        from pinecone import Pinecone, ServerlessSpec

        # Set up Pinecone API key
        os.environ["PINECONE_API_KEY"] = "<Your Pinecone API key, from app.pinecone.io>"
        api_key = os.environ["PINECONE_API_KEY"]

        # Create Pinecone Vector Store
        pc = Pinecone(api_key=api_key)

        pc.create_index(
            name="quickstart",
            dimension=1536,
            metric="dotproduct",
            spec=ServerlessSpec(cloud="aws", region="us-west-2"),


        pinecone_index = pc.Index("quickstart")

        vector_store = PineconeVectorStore(
            pinecone_index=pinecone_index,

        ```

    """

    stores_text: bool = True
    flat_metadata: bool = False

    api_key: Optional[str]
    index_name: Optional[str]
    environment: Optional[str]
    namespace: Optional[str]
    insert_kwargs: Optional[Dict]
    add_sparse_vector: bool
    text_key: str
    batch_size: int
    remove_text_from_metadata: bool

    _pinecone_index: pinecone.db_data.index.Index = PrivateAttr()
    _sparse_embedding_model: Optional[BaseSparseEmbedding] = PrivateAttr()

    def__init__(
        self,
        pinecone_index: Optional[pinecone.db_data.index.Index] = None,
        api_key: Optional[str] = None,
        index_name: Optional[str] = None,
        environment: Optional[str] = None,
        namespace: Optional[str] = None,
        insert_kwargs: Optional[Dict] = None,
        add_sparse_vector: bool = False,
        tokenizer: Optional[Callable] = None,
        text_key: str = DEFAULT_TEXT_KEY,
        batch_size: int = DEFAULT_BATCH_SIZE,
        remove_text_from_metadata: bool = False,
        default_empty_query_vector: Optional[List[float]] = None,
        sparse_embedding_model: Optional[BaseSparseEmbedding] = None,
        **kwargs: Any,
    ) -> None:
        insert_kwargs = insert_kwargs or {}

        if add_sparse_vector:
            if sparse_embedding_model is not None:
                sparse_embedding_model = sparse_embedding_model
            elif tokenizer is not None:
                sparse_embedding_model = DefaultPineconeSparseEmbedding(
                    tokenizer=tokenizer
                )
            else:
                sparse_embedding_model = DefaultPineconeSparseEmbedding()
        else:
            sparse_embedding_model = None

        super().__init__(
            index_name=index_name,
            environment=environment,
            api_key=api_key,
            namespace=namespace,
            insert_kwargs=insert_kwargs,
            add_sparse_vector=add_sparse_vector,
            text_key=text_key,
            batch_size=batch_size,
            remove_text_from_metadata=remove_text_from_metadata,
        )

        self._sparse_embedding_model = sparse_embedding_model

        if isinstance(pinecone_index, str):
            raise ValueError(
                "`pinecone_index` cannot be of type `str`; should be an instance of pinecone.data.index.Index"
            )

        self._pinecone_index = pinecone_index or self._initialize_pinecone_client(
            api_key, index_name, environment, **kwargs
        )

    @classmethod
    def_initialize_pinecone_client(
        cls,
        api_key: Optional[str],
        index_name: Optional[str],
        environment: Optional[str],
        **kwargs: Any,
    ) -> Any:
"""
        Initialize Pinecone client.
        """
        if not index_name:
            raise ValueError(
                "`index_name` is required for Pinecone client initialization"
            )

        pinecone_instance = pinecone.Pinecone(api_key=api_key, source_tag="llamaindex")
        return pinecone_instance.Index(index_name)

    @classmethod
    deffrom_params(
        cls,
        api_key: Optional[str] = None,
        index_name: Optional[str] = None,
        environment: Optional[str] = None,
        namespace: Optional[str] = None,
        insert_kwargs: Optional[Dict] = None,
        add_sparse_vector: bool = False,
        tokenizer: Optional[Callable] = None,
        text_key: str = DEFAULT_TEXT_KEY,
        batch_size: int = DEFAULT_BATCH_SIZE,
        remove_text_from_metadata: bool = False,
        default_empty_query_vector: Optional[List[float]] = None,
        **kwargs: Any,
    ) -> "PineconeVectorStore":
        pinecone_index = cls._initialize_pinecone_client(
            api_key, index_name, environment, **kwargs
        )

        return cls(
            pinecone_index=pinecone_index,
            api_key=api_key,
            index_name=index_name,
            environment=environment,
            namespace=namespace,
            insert_kwargs=insert_kwargs,
            add_sparse_vector=add_sparse_vector,
            tokenizer=tokenizer,
            text_key=text_key,
            batch_size=batch_size,
            remove_text_from_metadata=remove_text_from_metadata,
            default_empty_query_vector=default_empty_query_vector,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "PinconeVectorStore"

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to index.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        """
        ids = []
        entries = []
        sparse_inputs = []
        for node in nodes:
            node_id = node.node_id

            metadata = node_to_metadata_dict(
                node,
                remove_text=self.remove_text_from_metadata,
                flat_metadata=self.flat_metadata,
            )

            if self.add_sparse_vector and self._sparse_embedding_model is not None:
                sparse_inputs.append(node.get_content(metadata_mode=MetadataMode.EMBED))

            if node.ref_doc_id is not None:
                node_id = f"{node.ref_doc_id}#{node_id}"

            ids.append(node_id)

            entry = {
                ID_KEY: node_id,
                VECTOR_KEY: node.get_embedding(),
                METADATA_KEY: metadata,
            }
            entries.append(entry)

        # batch sparse embedding generation
        if sparse_inputs:
            sparse_vectors = self._sparse_embedding_model.get_text_embedding_batch(
                sparse_inputs
            )
            for i, sparse_vector in enumerate(sparse_vectors):
                entries[i][SPARSE_VECTOR_KEY] = {
                    "indices": list(sparse_vector.keys()),
                    "values": list(sparse_vector.values()),
                }

        self._pinecone_index.upsert(
            entries,
            namespace=self.namespace,
            batch_size=self.batch_size,
            **self.insert_kwargs,
        )
        return ids

    defget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[List[MetadataFilters]] = None,
        limit: int = 100,
        include_values: bool = False,
    ) -> List[BaseNode]:
        filter = None
        if filters is not None:
            filter = _to_pinecone_filter(filters)

        if node_ids is not None:
            raise ValueError(
                "Getting nodes by node id not supported by Pinecone at the time of writing."
            )

        if node_ids is None and filters is None:
            raise ValueError("Filters must be specified")

        # Pinecone requires a query vector, so default to 0s if not provided
        query_vector = [0.0] * self._pinecone_index.describe_index_stats()["dimension"]

        response = self._pinecone_index.query(
            top_k=limit,
            vector=query_vector,
            namespace=self.namespace,
            filter=filter,
            include_values=include_values,
            include_metadata=True,
        )

        nodes = [metadata_dict_to_node(match.metadata) for match in response.matches]
        if include_values:
            for node, match in zip(nodes, response.matches):
                node.embedding = match.values

        return nodes

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        try:
            # delete by filtering on the doc_id metadata
            self._pinecone_index.delete(
                filter={"doc_id": {"$eq": ref_doc_id}},
                namespace=self.namespace,
                **delete_kwargs,
            )
        except Exception:
            # fallback to deleting by prefix for serverless
            # TODO: this is a bit of a hack, we should find a better way to handle this
            id_gen = self._pinecone_index.list(
                prefix=ref_doc_id, namespace=self.namespace
            )
            ids_to_delete = list(id_gen)
            if ids_to_delete:
                self._pinecone_index.delete(
                    ids=ids_to_delete, namespace=self.namespace, **delete_kwargs
                )

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Deletes nodes using their ids.

        Args:
            node_ids (Optional[List[str]], optional): List of node IDs. Defaults to None.
            filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

        """
        node_ids = node_ids or []

        if filters is not None:
            filter = _to_pinecone_filter(filters)
        else:
            filter = None

        self._pinecone_index.delete(
            ids=node_ids, namespace=self.namespace, filter=filter, **delete_kwargs
        )

    defclear(self) -> None:
"""Clears the index."""
        self._pinecone_index.delete(namespace=self.namespace, delete_all=True)

    @property
    defclient(self) -> Any:
"""Return Pinecone client."""
        return self._pinecone_index

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query_embedding (List[float]): query embedding
            similarity_top_k (int): top k most similar nodes

        """
        pinecone_sparse_vector = None
        if (
            query.mode in (VectorStoreQueryMode.SPARSE, VectorStoreQueryMode.HYBRID)
            and self._sparse_embedding_model is not None
        ):
            if query.query_str is None:
                raise ValueError(
                    "query_str must be specified if mode is SPARSE or HYBRID."
                )
            sparse_vector = self._sparse_embedding_model.get_query_embedding(
                query.query_str
            )
            if query.alpha is not None:
                pinecone_sparse_vector = {
                    "indices": list(sparse_vector.keys()),
                    "values": [v * (1 - query.alpha) for v in sparse_vector.values()],
                }
            else:
                pinecone_sparse_vector = {
                    "indices": list(sparse_vector.keys()),
                    "values": list(sparse_vector.values()),
                }

        # pinecone requires a query embedding, so default to 0s if not provided
        if query.query_embedding is not None:
            dimension = len(query.query_embedding)
        else:
            dimension = self._pinecone_index.describe_index_stats()["dimension"]
        query_embedding = [0.0] * dimension

        if query.mode in (VectorStoreQueryMode.DEFAULT, VectorStoreQueryMode.HYBRID):
            query_embedding = cast(List[float], query.query_embedding)
            if query.alpha is not None:
                query_embedding = [v * query.alpha for v in query_embedding]

        if query.filters is not None:
            if "filter" in kwargs or "pinecone_query_filters" in kwargs:
                raise ValueError(
                    "Cannot specify filter via both query and kwargs. "
                    "Use kwargs only for pinecone specific items that are "
                    "not supported via the generic query interface."
                )
            filter = _to_pinecone_filter(query.filters)
        elif "pinecone_query_filters" in kwargs:
            filter = kwargs.pop("pinecone_query_filters")
        else:
            filter = kwargs.pop("filter", {})

        response = self._pinecone_index.query(
            vector=query_embedding,
            sparse_vector=pinecone_sparse_vector,
            top_k=query.similarity_top_k,
            include_values=kwargs.pop("include_values", True),
            include_metadata=kwargs.pop("include_metadata", True),
            namespace=self.namespace,
            filter=filter,
            **kwargs,
        )

        top_k_nodes = []
        top_k_ids = []
        top_k_scores = []
        for match in response.matches:
            try:
                node = metadata_dict_to_node(match.metadata)
                node.embedding = match.values
            except Exception:
                # NOTE: deprecated legacy logic for backward compatibility
                _logger.debug(
                    "Failed to parse Node metadata, fallback to legacy logic."
                )
                metadata, node_info, relationships = legacy_metadata_dict_to_node(
                    match.metadata, text_key=self.text_key
                )

                text = match.metadata[self.text_key]
                id = match.id
                node = TextNode(
                    text=text,
                    id_=id,
                    metadata=metadata,
                    start_char_idx=node_info.get("start", None),
                    end_char_idx=node_info.get("end", None),
                    relationships=relationships,
                )
            top_k_ids.append(match.id)
            top_k_nodes.append(node)
            top_k_scores.append(match.score)

        return VectorStoreQueryResult(
            nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
        )

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/pinecone/#llama_index.vector_stores.pinecone.PineconeVectorStore.client "Permanent link")

```
client: 

```

Return Pinecone client.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/pinecone/#llama_index.vector_stores.pinecone.PineconeVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-pinecone/llama_index/vector_stores/pinecone/base.py`  
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
        nodes: List[BaseNode]: list of nodes with embeddings

    """
    ids = []
    entries = []
    sparse_inputs = []
    for node in nodes:
        node_id = node.node_id

        metadata = node_to_metadata_dict(
            node,
            remove_text=self.remove_text_from_metadata,
            flat_metadata=self.flat_metadata,
        )

        if self.add_sparse_vector and self._sparse_embedding_model is not None:
            sparse_inputs.append(node.get_content(metadata_mode=MetadataMode.EMBED))

        if node.ref_doc_id is not None:
            node_id = f"{node.ref_doc_id}#{node_id}"

        ids.append(node_id)

        entry = {
            ID_KEY: node_id,
            VECTOR_KEY: node.get_embedding(),
            METADATA_KEY: metadata,
        }
        entries.append(entry)

    # batch sparse embedding generation
    if sparse_inputs:
        sparse_vectors = self._sparse_embedding_model.get_text_embedding_batch(
            sparse_inputs
        )
        for i, sparse_vector in enumerate(sparse_vectors):
            entries[i][SPARSE_VECTOR_KEY] = {
                "indices": list(sparse_vector.keys()),
                "values": list(sparse_vector.values()),
            }

    self._pinecone_index.upsert(
        entries,
        namespace=self.namespace,
        batch_size=self.batch_size,
        **self.insert_kwargs,
    )
    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/pinecone/#llama_index.vector_stores.pinecone.PineconeVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-pinecone/llama_index/vector_stores/pinecone/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    try:
        # delete by filtering on the doc_id metadata
        self._pinecone_index.delete(
            filter={"doc_id": {"$eq": ref_doc_id}},
            namespace=self.namespace,
            **delete_kwargs,
        )
    except Exception:
        # fallback to deleting by prefix for serverless
        # TODO: this is a bit of a hack, we should find a better way to handle this
        id_gen = self._pinecone_index.list(
            prefix=ref_doc_id, namespace=self.namespace
        )
        ids_to_delete = list(id_gen)
        if ids_to_delete:
            self._pinecone_index.delete(
                ids=ids_to_delete, namespace=self.namespace, **delete_kwargs
            )

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/pinecone/#llama_index.vector_stores.pinecone.PineconeVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Deletes nodes using their ids.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  List of node IDs. Defaults to None.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters. Defaults to None.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-pinecone/llama_index/vector_stores/pinecone/base.py`  
| 
```
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
    Deletes nodes using their ids.

    Args:
        node_ids (Optional[List[str]], optional): List of node IDs. Defaults to None.
        filters (Optional[MetadataFilters], optional): Metadata filters. Defaults to None.

    """
    node_ids = node_ids or []

    if filters is not None:
        filter = _to_pinecone_filter(filters)
    else:
        filter = None

    self._pinecone_index.delete(
        ids=node_ids, namespace=self.namespace, filter=filter, **delete_kwargs
    )

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/pinecone/#llama_index.vector_stores.pinecone.PineconeVectorStore.clear "Permanent link")

```
clear() -> None

```

Clears the index.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-pinecone/llama_index/vector_stores/pinecone/base.py`  
| 
```
442
443
444
```
 | 
```
defclear(self) -> None:
"""Clears the index."""
    self._pinecone_index.delete(namespace=self.namespace, delete_all=True)

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/pinecone/#llama_index.vector_stores.pinecone.PineconeVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_embedding`  |  `List[float]`  |  query embedding  |  _required_  |  
|  `similarity_top_k`  |  top k most similar nodes  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-pinecone/llama_index/vector_stores/pinecone/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query_embedding (List[float]): query embedding
        similarity_top_k (int): top k most similar nodes

    """
    pinecone_sparse_vector = None
    if (
        query.mode in (VectorStoreQueryMode.SPARSE, VectorStoreQueryMode.HYBRID)
        and self._sparse_embedding_model is not None
    ):
        if query.query_str is None:
            raise ValueError(
                "query_str must be specified if mode is SPARSE or HYBRID."
            )
        sparse_vector = self._sparse_embedding_model.get_query_embedding(
            query.query_str
        )
        if query.alpha is not None:
            pinecone_sparse_vector = {
                "indices": list(sparse_vector.keys()),
                "values": [v * (1 - query.alpha) for v in sparse_vector.values()],
            }
        else:
            pinecone_sparse_vector = {
                "indices": list(sparse_vector.keys()),
                "values": list(sparse_vector.values()),
            }

    # pinecone requires a query embedding, so default to 0s if not provided
    if query.query_embedding is not None:
        dimension = len(query.query_embedding)
    else:
        dimension = self._pinecone_index.describe_index_stats()["dimension"]
    query_embedding = [0.0] * dimension

    if query.mode in (VectorStoreQueryMode.DEFAULT, VectorStoreQueryMode.HYBRID):
        query_embedding = cast(List[float], query.query_embedding)
        if query.alpha is not None:
            query_embedding = [v * query.alpha for v in query_embedding]

    if query.filters is not None:
        if "filter" in kwargs or "pinecone_query_filters" in kwargs:
            raise ValueError(
                "Cannot specify filter via both query and kwargs. "
                "Use kwargs only for pinecone specific items that are "
                "not supported via the generic query interface."
            )
        filter = _to_pinecone_filter(query.filters)
    elif "pinecone_query_filters" in kwargs:
        filter = kwargs.pop("pinecone_query_filters")
    else:
        filter = kwargs.pop("filter", {})

    response = self._pinecone_index.query(
        vector=query_embedding,
        sparse_vector=pinecone_sparse_vector,
        top_k=query.similarity_top_k,
        include_values=kwargs.pop("include_values", True),
        include_metadata=kwargs.pop("include_metadata", True),
        namespace=self.namespace,
        filter=filter,
        **kwargs,
    )

    top_k_nodes = []
    top_k_ids = []
    top_k_scores = []
    for match in response.matches:
        try:
            node = metadata_dict_to_node(match.metadata)
            node.embedding = match.values
        except Exception:
            # NOTE: deprecated legacy logic for backward compatibility
            _logger.debug(
                "Failed to parse Node metadata, fallback to legacy logic."
            )
            metadata, node_info, relationships = legacy_metadata_dict_to_node(
                match.metadata, text_key=self.text_key
            )

            text = match.metadata[self.text_key]
            id = match.id
            node = TextNode(
                text=text,
                id_=id,
                metadata=metadata,
                start_char_idx=node_info.get("start", None),
                end_char_idx=node_info.get("end", None),
                relationships=relationships,
            )
        top_k_ids.append(match.id)
        top_k_nodes.append(node)
        top_k_scores.append(match.score)

    return VectorStoreQueryResult(
        nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
    )

```
 |  
| --- | --- |  
options: members: - PineconeVectorStore
