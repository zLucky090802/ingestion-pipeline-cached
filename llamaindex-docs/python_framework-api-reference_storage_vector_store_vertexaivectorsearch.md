# Vertexaivectorsearch
##  VertexAIVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vertexaivectorsearch/#llama_index.vector_stores.vertexaivectorsearch.VertexAIVectorStore "Permanent link")
Bases: 
Vertex AI Vector Search vector store.
In this vector store, embeddings are stored in Vertex AI Vector Store and docs are stored within Cloud Storage bucket.
During query time, the index uses Vertex AI Vector Search to query for the top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `project_id (str) `  |  The Google Cloud Project ID.  |  _required_  |  
|  `region (str)     `  |  The default location making the API calls. It must be the same location as where Vector Search index created and must be regional.  |  _required_  |  
|  `index_id (str)   `  |  The fully qualified resource name of the created index in Vertex AI Vector Search.  |  _required_  |  
|  `endpoint_id`  |  The fully qualified resource name of the created index endpoint in Vertex AI Vector Search.  |  `None`  |  
|  `gcs_bucket_name`  |  `Optional[str]`  |  
```
           The location where the vectors will be stored for
           the index to be created in batch mode.

```
 |  `None`  |  
|  `credentials_path`  |  `Optional[str]`  |  
```
           The path of the Google credentials on the local file
           system.

```
 |  `None`  |  
Examples:
`pip install llama-index-vector-stores-vertexaivectorsearch`

```
from
vector_store = VertexAIVectorStore(
    project_id=PROJECT_ID,
    region=REGION,
    index_id="<index_resource_name>"
    endpoint_id="<index_endpoint_resource_name>"
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vertexaivectorsearch/llama_index/vector_stores/vertexaivectorsearch/base.py`  
| 
```
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
```
 | 
```
classVertexAIVectorStore(BasePydanticVectorStore):
"""
    Vertex AI Vector Search vector store.

    In this vector store, embeddings are stored in Vertex AI Vector Store and
    docs are stored within Cloud Storage bucket.

    During query time, the index uses Vertex AI Vector Search to query for the
    top k most similar nodes.

    Args:
        project_id (str) : The Google Cloud Project ID.
        region (str)     : The default location making the API calls.
                           It must be the same location as where Vector Search
                           index created and must be regional.
        index_id (str)   : The fully qualified resource name of the created
                           index in Vertex AI Vector Search.
        endpoint_id (str): The fully qualified resource name of the created
                           index endpoint in Vertex AI Vector Search.
        gcs_bucket_name (Optional[str]):
                           The location where the vectors will be stored for
                           the index to be created in batch mode.
        credentials_path (Optional[str]):
                           The path of the Google credentials on the local file
                           system.

    Examples:
        `pip install llama-index-vector-stores-vertexaivectorsearch`

        ```python
        from
        vector_store = VertexAIVectorStore(
            project_id=PROJECT_ID,
            region=REGION,
            index_id="<index_resource_name>"
            endpoint_id="<index_endpoint_resource_name>"

        ```

    """

    stores_text: bool = True
    remove_text_from_metadata: bool = True
    flat_metadata: bool = False

    text_key: str

    project_id: str
    region: str

    # API version - defaults to v1 for backward compatibility
    api_version: Literal["v1", "v2"] = Field(default="v1")

    # v1-exclusive parameters
    index_id: Optional[str] = None
    endpoint_id: Optional[str] = None
    gcs_bucket_name: Optional[str] = None

    # v2-exclusive parameters
    collection_id: Optional[str] = None

    # V2 Hybrid Search parameters
    enable_hybrid: bool = Field(default=False)
    text_search_fields: Optional[List[str]] = Field(default=None)
    embedding_field: str = Field(default="embedding")

    # Ranker configuration
    hybrid_ranker: Literal["rrf", "vertex"] = Field(default="rrf")
    default_hybrid_alpha: float = Field(default=0.5, ge=0.0, le=1.0)

    # SemanticSearch configuration
    semantic_task_type: str = Field(default="RETRIEVAL_QUERY")

    # VertexRanker-specific parameters
    vertex_ranker_model: str = Field(default="semantic-ranker-default@latest")
    vertex_ranker_title_field: Optional[str] = Field(default=None)
    vertex_ranker_content_field: Optional[str] = Field(default=None)

    # Shared parameters
    batch_size: int = 100
    credentials_path: Optional[str] = None

    _index: MatchingEngineIndex = PrivateAttr()
    _endpoint: MatchingEngineIndexEndpoint = PrivateAttr()
    _index_metadata: dict = PrivateAttr()
    _stream_update: bool = PrivateAttr()
    _staging_bucket: storage.Bucket = PrivateAttr()
    # _document_storage: GCSDocumentStorage = PrivateAttr()

    def__init__(
        self,
        project_id: Optional[str] = None,
        region: Optional[str] = None,
        index_id: Optional[str] = None,
        endpoint_id: Optional[str] = None,
        gcs_bucket_name: Optional[str] = None,
        credentials_path: Optional[str] = None,
        text_key: str = DEFAULT_TEXT_KEY,
        remove_text_from_metadata: bool = True,
        api_version: str = "v1",
        collection_id: Optional[str] = None,
        batch_size: int = 100,
        # V2 Hybrid Search parameters
        enable_hybrid: bool = False,
        text_search_fields: Optional[List[str]] = None,
        embedding_field: str = "embedding",
        hybrid_ranker: Literal["rrf", "vertex"] = "rrf",
        default_hybrid_alpha: float = 0.5,
        semantic_task_type: str = "RETRIEVAL_QUERY",
        vertex_ranker_model: str = "semantic-ranker-default@latest",
        vertex_ranker_title_field: Optional[str] = None,
        vertex_ranker_content_field: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            project_id=project_id,
            region=region,
            index_id=index_id,
            endpoint_id=endpoint_id,
            gcs_bucket_name=gcs_bucket_name,
            credentials_path=credentials_path,
            text_key=text_key,
            remove_text_from_metadata=remove_text_from_metadata,
            api_version=api_version,
            collection_id=collection_id,
            batch_size=batch_size,
            enable_hybrid=enable_hybrid,
            text_search_fields=text_search_fields,
            embedding_field=embedding_field,
            hybrid_ranker=hybrid_ranker,
            default_hybrid_alpha=default_hybrid_alpha,
            semantic_task_type=semantic_task_type,
            vertex_ranker_model=vertex_ranker_model,
            vertex_ranker_title_field=vertex_ranker_title_field,
            vertex_ranker_content_field=vertex_ranker_content_field,
        )

"""Initialize params."""
        # Validate parameters based on API version
        self._validate_parameters()

        # Only initialize v1 resources if using v1 API
        if self.api_version == "v1":
            _sdk_manager = VectorSearchSDKManager(
                project_id=project_id, region=region, credentials_path=credentials_path
            )

            # get index and endpoint resource names including metadata
            self._index = _sdk_manager.get_index(index_id=index_id)
            self._endpoint = _sdk_manager.get_endpoint(endpoint_id=endpoint_id)
            self._index_metadata = self._index.to_dict()

            # get index update method from index metadata
            self._stream_update = False
            if self._index_metadata["indexUpdateMethod"] == "STREAM_UPDATE":
                self._stream_update = True

            # get bucket object when available
            if self.gcs_bucket_name:
                self._staging_bucket = _sdk_manager.get_gcs_bucket(
                    bucket_name=gcs_bucket_name
                )
            else:
                self._staging_bucket = None
        else:
            # v2 initialization will be handled separately
            # Set private attributes to None for now
            self._index = None
            self._endpoint = None
            self._index_metadata = {}
            self._stream_update = False
            self._staging_bucket = None

    def_validate_parameters(self) -> None:
"""Validate parameters based on API version."""
        if self.api_version == "v1":
            # v1 requires index_id and endpoint_id
            if not self.index_id:
                raise ValueError(
                    "index_id is required for v1.0 API. "
                    "Please provide a valid index ID."
                )
            if not self.endpoint_id:
                raise ValueError(
                    "endpoint_id is required for v1.0 API. "
                    "Please provide a valid endpoint ID."
                )
            # v2-exclusive parameters must not be set in v1
            if self.collection_id is not None:
                raise ValueError(
                    "Parameter 'collection_id' is only valid for api_version='v2'. "
                    "For v1, use index_id and endpoint_id instead."
                )
        elif self.api_version == "v2":
            # v2 requires collection_id
            if not self.collection_id:
                raise ValueError(
                    "collection_id is required for v2.0 API. "
                    "Please provide a valid collection ID."
                )
            # v1-exclusive parameters must not be set in v2
            if self.index_id is not None:
                raise ValueError(
                    "Parameter 'index_id' is only valid for api_version='v1'. "
                    "For v2, use collection_id instead."
                )
            if self.endpoint_id is not None:
                raise ValueError(
                    "Parameter 'endpoint_id' is only valid for api_version='v1'. "
                    "For v2, use collection_id instead."
                )
            if self.gcs_bucket_name is not None:
                raise ValueError(
                    "Parameter 'gcs_bucket_name' is only valid for api_version='v1'. "
                    "v2 does not require a staging bucket."
                )

        # Hybrid search validation (applies to both v1 and v2, but some features are v2-only)
        if self.enable_hybrid and self.api_version != "v2":
            raise ValueError(
                "enable_hybrid=True is only supported for api_version='v2'. "
                "V1 hybrid search uses HybridQuery with find_neighbors() directly."
            )

        if self.hybrid_ranker == "vertex":
            if (
                self.vertex_ranker_title_field is None
                and self.vertex_ranker_content_field is None
            ):
                _logger.warning(
                    "VertexRanker works best with title_field and/or content_field configured. "
                    "Consider setting vertex_ranker_title_field or vertex_ranker_content_field."
                )

    @classmethod
    deffrom_params(
        cls,
        project_id: Optional[str] = None,
        region: Optional[str] = None,
        index_id: Optional[str] = None,
        endpoint_id: Optional[str] = None,
        gcs_bucket_name: Optional[str] = None,
        credentials_path: Optional[str] = None,
        text_key: str = DEFAULT_TEXT_KEY,
        **kwargs: Any,
    ) -> "VertexAIVectorStore":
"""Create VertexAIVectorStore from config."""
        return cls(
            project_id=project_id,
            region=region,
            index_id=index_id,
            endpoint_id=endpoint_id,
            gcs_bucket_name=gcs_bucket_name,
            credentials_path=credentials_path,
            text_key=text_key,
            api_version="v1",  # Always defaults to v1 for backward compatibility
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "VertexAIVectorStore"

    @property
    defclient(self) -> Any:
"""Get client."""
        return self._index

    @property
    defindex(self) -> Any:
"""Get client."""
        return self._index

    @property
    defendpoint(self) -> Any:
"""Get client."""
        return self._endpoint

    @property
    defstaging_bucket(self) -> Any:
"""Get client."""
        return self._staging_bucket

    defadd(
        self,
        nodes: List[BaseNode],
        is_complete_overwrite: bool = False,
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to index.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        """
        if FeatureFlags.should_use_v2(self.api_version):
            # No fallback - v2 requires v2 SDK
            return self._add_v2(
                nodes, is_complete_overwrite=is_complete_overwrite, **add_kwargs
            )
        else:
            return self._add_v1(
                nodes, is_complete_overwrite=is_complete_overwrite, **add_kwargs
            )

    def_add_v1(
        self,
        nodes: List[BaseNode],
        is_complete_overwrite: bool = False,
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to index using v1 API.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        """
        ids = []
        embeddings = []
        metadatas = []
        for node in nodes:
            node_id = node.node_id
            metadata = node_to_metadata_dict(
                node, remove_text=False, flat_metadata=False
            )
            embedding = node.get_embedding()

            ids.append(node_id)
            embeddings.append(embedding)
            metadatas.append(metadata)

        data_points = utils.to_data_points(ids, embeddings, metadatas)
        # self._document_storage.add_documents(list(zip(ids, nodes)))

        if self._stream_update:
            utils.stream_update_index(index=self._index, data_points=data_points)
        else:
            if self._staging_bucket is None:
                raise ValueError(
                    "To update a Vector Search index a staging bucket must be defined."
                )
            utils.batch_update_index(
                index=self._index,
                data_points=data_points,
                staging_bucket=self._staging_bucket,
                is_complete_overwrite=is_complete_overwrite,
            )
        return ids

    def_add_v2(
        self,
        nodes: List[BaseNode],
        is_complete_overwrite: bool = False,
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to index using v2 API.

        This will be implemented in _v2_operations.py.
        """
        # Import v2 operations module lazily
        fromllama_index.vector_stores.vertexaivectorsearchimport _v2_operations

        return _v2_operations.add_v2(
            self, nodes, is_complete_overwrite=is_complete_overwrite, **add_kwargs
        )

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        if FeatureFlags.should_use_v2(self.api_version):
            # No fallback - v2 requires v2 SDK
            return self._delete_v2(ref_doc_id, **delete_kwargs)
        else:
            return self._delete_v1(ref_doc_id, **delete_kwargs)

    def_delete_v1(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id (v1 API).

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        # get datapoint ids by filter
        filter = {"ref_doc_id": ref_doc_id}
        ids = utils.get_datapoints_by_filter(
            index=self.index, endpoint=self.endpoint, metadata=filter
        )
        # remove datapoints
        self._index.remove_datapoints(datapoint_ids=ids)

    def_delete_v2(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id (v2 API).

        This will be implemented in _v2_operations.py.
        """
        # Import v2 operations module lazily
        fromllama_index.vector_stores.vertexaivectorsearchimport _v2_operations

        return _v2_operations.delete_v2(self, ref_doc_id, **delete_kwargs)

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query index for top k most similar nodes."""
        if FeatureFlags.should_use_v2(self.api_version):
            # No fallback - v2 requires v2 SDK
            return self._query_v2(query, **kwargs)
        else:
            return self._query_v1(query, **kwargs)

    def_query_v1(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
"""Query index for top k most similar nodes (v1 API)."""
        query_embedding = None
        if query.mode == VectorStoreQueryMode.DEFAULT:
            query_embedding = [cast(List[float], query.query_embedding)]

        if query.filters is not None:
            if "filter" in kwargs and kwargs["filter"] is not None:
                raise ValueError(
                    "Cannot specify filter via both query and kwargs. "
                    "Use kwargs only for Vertex AI Vector Search specific items that are "
                    "not supported via the generic query interface such as numeric filters."
                )
            filter, num_filter = utils.to_vectorsearch_filter(query.filters)
        else:
            filter = None
            num_filter = None

        matches = utils.find_neighbors(
            index=self._index,
            endpoint=self._endpoint,
            embeddings=query_embedding,
            top_k=query.similarity_top_k,
            filter=filter,
            numeric_filter=num_filter,
        )

        top_k_nodes = []
        top_k_ids = []
        top_k_scores = []

        for match in matches:
            node = utils.to_node(match, self.text_key)
            top_k_ids.append(match.id)
            top_k_scores.append(match.distance)
            top_k_nodes.append(node)

        return VectorStoreQueryResult(
            nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
        )

    def_query_v2(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
"""Query index for top k most similar nodes (v2 API)."""
        # Import v2 operations module lazily
        fromllama_index.vector_stores.vertexaivectorsearchimport _v2_operations

        return _v2_operations.query_v2(self, query, **kwargs)

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **kwargs: Any,
    ) -> None:
"""
        Delete nodes by IDs or filters.

        Args:
            node_ids: List of node IDs to delete
            filters: Metadata filters to select nodes for deletion

        """
        if FeatureFlags.should_use_v2(self.api_version):
            # No fallback - v2 requires v2 SDK
            return self._delete_nodes_v2(node_ids, filters, **kwargs)
        else:
            return self._delete_nodes_v1(node_ids, filters, **kwargs)

    def_delete_nodes_v1(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **kwargs: Any,
    ) -> None:
"""Delete nodes by IDs or filters (v1 API)."""
        if node_ids is not None:
            # Delete by node IDs
            self._index.remove_datapoints(datapoint_ids=node_ids)
        else:
            # v1 doesn't have efficient filter-based deletion
            # Would need to query first then delete
            raise NotImplementedError(
                "Filter-based deletion not implemented for v1. "
                "Use delete() with ref_doc_id or provide node_ids."
            )

    def_delete_nodes_v2(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **kwargs: Any,
    ) -> None:
"""Delete nodes by IDs or filters (v2 API)."""
        # Import v2 operations module lazily
        fromllama_index.vector_stores.vertexaivectorsearchimport _v2_operations

        return _v2_operations.delete_nodes_v2(self, node_ids, filters, **kwargs)

    defclear(self) -> None:
"""Clear all nodes from the vector store."""
        if FeatureFlags.should_use_v2(self.api_version):
            # No fallback - v2 requires v2 SDK
            return self._clear_v2()
        else:
            return self._clear_v1()

    def_clear_v1(self) -> None:
"""Clear all nodes from the vector store (v1 API)."""
        raise NotImplementedError(
            "Clear operation not supported in v1. "
            "Please recreate the index or use delete operations."
        )

    def_clear_v2(self) -> None:
"""Clear all nodes from the vector store (v2 API)."""
        # Import v2 operations module lazily
        fromllama_index.vector_stores.vertexaivectorsearchimport _v2_operations

        return _v2_operations.clear_v2(self)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vertexaivectorsearch/#llama_index.vector_stores.vertexaivectorsearch.VertexAIVectorStore.client "Permanent link")

```
client: 

```

Get client.
###  index `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vertexaivectorsearch/#llama_index.vector_stores.vertexaivectorsearch.VertexAIVectorStore.index "Permanent link")

```
index: 

```

Get client.
###  endpoint `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vertexaivectorsearch/#llama_index.vector_stores.vertexaivectorsearch.VertexAIVectorStore.endpoint "Permanent link")

```
endpoint: 

```

Get client.
###  staging_bucket `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vertexaivectorsearch/#llama_index.vector_stores.vertexaivectorsearch.VertexAIVectorStore.staging_bucket "Permanent link")

```
staging_bucket: 

```

Get client.
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vertexaivectorsearch/#llama_index.vector_stores.vertexaivectorsearch.VertexAIVectorStore.from_params "Permanent link")

```
from_params(
    project_id: Optional[] = None,
    region: Optional[] = None,
    index_id: Optional[] = None,
    endpoint_id: Optional[] = None,
    gcs_bucket_name: Optional[] = None,
    credentials_path: Optional[] = None,
    text_key:  = DEFAULT_TEXT_KEY,
    **kwargs: 
) -> 

```

Create VertexAIVectorStore from config.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vertexaivectorsearch/llama_index/vector_stores/vertexaivectorsearch/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_params(
    cls,
    project_id: Optional[str] = None,
    region: Optional[str] = None,
    index_id: Optional[str] = None,
    endpoint_id: Optional[str] = None,
    gcs_bucket_name: Optional[str] = None,
    credentials_path: Optional[str] = None,
    text_key: str = DEFAULT_TEXT_KEY,
    **kwargs: Any,
) -> "VertexAIVectorStore":
"""Create VertexAIVectorStore from config."""
    return cls(
        project_id=project_id,
        region=region,
        index_id=index_id,
        endpoint_id=endpoint_id,
        gcs_bucket_name=gcs_bucket_name,
        credentials_path=credentials_path,
        text_key=text_key,
        api_version="v1",  # Always defaults to v1 for backward compatibility
        **kwargs,
    )

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vertexaivectorsearch/#llama_index.vector_stores.vertexaivectorsearch.VertexAIVectorStore.add "Permanent link")

```
add(
    nodes: [],
    is_complete_overwrite:  = False,
    **add_kwargs: 
) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vertexaivectorsearch/llama_index/vector_stores/vertexaivectorsearch/base.py`  
| 
```
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
```
 | 
```
defadd(
    self,
    nodes: List[BaseNode],
    is_complete_overwrite: bool = False,
    **add_kwargs: Any,
) -> List[str]:
"""
    Add nodes to index.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings

    """
    if FeatureFlags.should_use_v2(self.api_version):
        # No fallback - v2 requires v2 SDK
        return self._add_v2(
            nodes, is_complete_overwrite=is_complete_overwrite, **add_kwargs
        )
    else:
        return self._add_v1(
            nodes, is_complete_overwrite=is_complete_overwrite, **add_kwargs
        )

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vertexaivectorsearch/#llama_index.vector_stores.vertexaivectorsearch.VertexAIVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vertexaivectorsearch/llama_index/vector_stores/vertexaivectorsearch/base.py`  
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    if FeatureFlags.should_use_v2(self.api_version):
        # No fallback - v2 requires v2 SDK
        return self._delete_v2(ref_doc_id, **delete_kwargs)
    else:
        return self._delete_v1(ref_doc_id, **delete_kwargs)

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vertexaivectorsearch/#llama_index.vector_stores.vertexaivectorsearch.VertexAIVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vertexaivectorsearch/llama_index/vector_stores/vertexaivectorsearch/base.py`  
| 
```
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
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query index for top k most similar nodes."""
    if FeatureFlags.should_use_v2(self.api_version):
        # No fallback - v2 requires v2 SDK
        return self._query_v2(query, **kwargs)
    else:
        return self._query_v1(query, **kwargs)

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vertexaivectorsearch/#llama_index.vector_stores.vertexaivectorsearch.VertexAIVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **kwargs: 
) -> None

```

Delete nodes by IDs or filters.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  List of node IDs to delete  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters to select nodes for deletion  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vertexaivectorsearch/llama_index/vector_stores/vertexaivectorsearch/base.py`  
| 
```
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
```
 | 
```
defdelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **kwargs: Any,
) -> None:
"""
    Delete nodes by IDs or filters.

    Args:
        node_ids: List of node IDs to delete
        filters: Metadata filters to select nodes for deletion

    """
    if FeatureFlags.should_use_v2(self.api_version):
        # No fallback - v2 requires v2 SDK
        return self._delete_nodes_v2(node_ids, filters, **kwargs)
    else:
        return self._delete_nodes_v1(node_ids, filters, **kwargs)

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vertexaivectorsearch/#llama_index.vector_stores.vertexaivectorsearch.VertexAIVectorStore.clear "Permanent link")

```
clear() -> None

```

Clear all nodes from the vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vertexaivectorsearch/llama_index/vector_stores/vertexaivectorsearch/base.py`  
| 
```
568
569
570
571
572
573
574
```
 | 
```
defclear(self) -> None:
"""Clear all nodes from the vector store."""
    if FeatureFlags.should_use_v2(self.api_version):
        # No fallback - v2 requires v2 SDK
        return self._clear_v2()
    else:
        return self._clear_v1()

```
 |  
| --- | --- |  
options: members: - VertexAIVectorStore
