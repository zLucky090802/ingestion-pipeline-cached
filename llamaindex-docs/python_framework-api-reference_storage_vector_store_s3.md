# S3
##  S3VectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/s3/#llama_index.vector_stores.s3.S3VectorStore "Permanent link")
Bases: 
S3 Vector Store.
Uses the S3Vectors service to store and query vectors directly in S3.
It is recommended to create a vector bucket in S3 first.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index_name`  |  The name of the index.  |  _required_  |  
|  `bucket_name_or_arn`  |  The name or ARN of the vector bucket.  |  _required_  |  
|  `data_type`  |  The data type of the vectors. Only supports "float32" for now.  |  `'float32'`  |  
|  `insert_batch_size`  |  The batch size for inserting vectors.  |  `500`  |  
|  `sync_session`  |  `Optional[Session]`  |  The session to use for the synchronous client.  |  `None`  |  
Examples:
`pip install llama-index-vector-stores-s3`

```
fromllama_index.vector_stores.s3import S3VectorStore

vector_store = S3VectorStore.create_index_from_bucket(
    bucket_name_or_arn="my-vector-bucket",
    index_name="my-index",
    dimension=1536,
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-s3/llama_index/vector_stores/s3/base.py`  
| 
```
 35
 36
 37
 38
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
```
 | 
```
classS3VectorStore(BasePydanticVectorStore):
"""
    S3 Vector Store.

    Uses the S3Vectors service to store and query vectors directly in S3.

    It is recommended to create a vector bucket in S3 first.

    Args:
        index_name (str): The name of the index.
        bucket_name_or_arn (str): The name or ARN of the vector bucket.
        data_type (str): The data type of the vectors. Only supports "float32" for now.
        insert_batch_size (int): The batch size for inserting vectors.
        sync_session (Optional[boto3.Session]): The session to use for the synchronous client.

    Examples:
        `pip install llama-index-vector-stores-s3`

        ```python
        from llama_index.vector_stores.s3 import S3VectorStore

        vector_store = S3VectorStore.create_index_from_bucket(
            bucket_name_or_arn="my-vector-bucket",
            index_name="my-index",
            dimension=1536,

        ```

    """

    stores_text: bool = True
    flat_metadata: bool = False

    index_name_or_arn: str = Field(description="The name or ARN of the index.")
    bucket_name_or_arn: str = Field(description="The name or ARN of the bucket.")
    data_type: str = Field(description="The data type of the vectors.")
    insert_batch_size: int = Field(description="The batch size for inserting vectors.")
    text_field: Optional[str] = Field(
        default=None, description="The field to use as the text field in the metadata."
    )
    distance_metric: str = Field(
        default="cosine", description="The distance metric used by the index."
    )

    _session: boto3.Session = PrivateAttr()

    def__init__(
        self,
        index_name_or_arn: str,
        bucket_name_or_arn: str,
        data_type: str = "float32",
        insert_batch_size: int = 500,
        text_field: Optional[str] = None,
        distance_metric: str = "cosine",
        sync_session: Optional[boto3.Session] = None,
        async_session: Optional[Any] = None,
    ) -> None:
"""Init params."""
        if async_session is not None:
            raise NotImplementedError(
                "Async sessions are not supported yet by aioboto3/aiobotocore"
            )

        if insert_batch_size  500:
            raise ValueError("Insert batch size must be less than or equal to 500")

        super().__init__(
            index_name_or_arn=index_name_or_arn,
            bucket_name_or_arn=bucket_name_or_arn,
            data_type=data_type,
            insert_batch_size=insert_batch_size,
            text_field=text_field,
            distance_metric=distance_metric,
        )
        self._session = sync_session or boto3.Session()

    @classmethod
    defcreate_index_from_bucket(
        cls,
        bucket_name_or_arn: str,
        index_name: str,
        dimension: int,
        distance_metric: str = "cosine",
        data_type: str = "float32",
        insert_batch_size: int = 500,
        non_filterable_metadata_keys: Optional[List[str]] = None,
        sync_session: Optional[boto3.Session] = None,
        async_session: Optional[Any] = None,
    ) -> "S3VectorStore":
"""
        Create an index in S3Vectors.
        """
        # node content and node type should never be filterable by default
        non_filterable_metadata_keys = non_filterable_metadata_keys or []
        if "_node_content" not in non_filterable_metadata_keys:
            non_filterable_metadata_keys.append("_node_content")
        if "_node_type" not in non_filterable_metadata_keys:
            non_filterable_metadata_keys.append("_node_type")

        bucket_name, bucket_arn = cls.get_name_or_arn(bucket_name_or_arn)

        sync_session = sync_session or boto3.Session()
        kwargs = {
            "indexName": index_name,
            "dimension": dimension,
            "dataType": data_type,
            "distanceMetric": distance_metric,
            "metadataConfiguration": {
                "nonFilterableMetadataKeys": non_filterable_metadata_keys,
            },
        }
        if bucket_arn is not None:
            kwargs["vectorBucketArn"] = bucket_arn
        else:
            kwargs["vectorBucketName"] = bucket_name

        sync_session.client("s3vectors").create_index(**kwargs)

        return cls(
            sync_session=sync_session,
            async_session=async_session,
            data_type=data_type,
            index_name_or_arn=index_name,
            bucket_name_or_arn=bucket_name_or_arn,
            insert_batch_size=insert_batch_size,
            distance_metric=distance_metric,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "S3VectorStore"

    @staticmethod
    defget_name_or_arn(name_or_arn: str) -> Tuple[str, str]:
"""
        Get the name or ARN.
        """
        if "arn:" in name_or_arn:
            return None, name_or_arn
        return name_or_arn, None

    def_parse_response(self, response: dict) -> List[BaseNode]:
"""
        Parse the response from S3Vectors.
        """
        if self.text_field is None:
            return [
                metadata_dict_to_node(v["metadata"])
                for v in response.get("vectors", [])
            ]
        else:
            nodes = []
            for v in response.get("vectors", []):
                if self.text_field not in v["metadata"]:
                    raise ValueError(
                        f"Text field {self.text_field} not found in returned metadata"
                    )

                text = v["metadata"].pop(self.text_field)
                nodes.append(TextNode(text=text, metadata=v["metadata"]))
            return nodes

    defget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> List[BaseNode]:
"""
        Get nodes from the index.

        Args:
            node_ids (Optional[List[str]]): List of node IDs to retrieve.
            filters (Optional[MetadataFilters]): Metadata filters to apply.

        Returns:
            List[BaseNode]: List of nodes retrieved from the index.

        """
        if node_ids is None:
            raise ValueError("node_ids is required")

        if filters is not None:
            raise NotImplementedError("Filters are not supported yet")

        index_name, index_arn = self.get_name_or_arn(self.index_name_or_arn)

        kwargs = {
            "keys": node_ids,
            "vectorBucketName": self.bucket_name_or_arn,
            "returnMetadata": True,
        }
        if index_arn is not None:
            kwargs["indexArn"] = index_arn
        else:
            kwargs["indexName"] = index_name

        response = self._session.client("s3vectors").get_vectors(**kwargs)
        return self._parse_response(response)

    async defaget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> List[BaseNode]:
"""
        Asynchronous method to get nodes from the index.

        Args:
            node_ids (Optional[List[str]]): List of node IDs to retrieve.
            filters (Optional[MetadataFilters]): Metadata filters to apply.

        Returns:
            List[BaseNode]: List of nodes retrieved from the index.

        """
        return await asyncio.to_thread(
            self.get_nodes, node_ids=node_ids, filters=filters
        )

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
        Add nodes to index.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        """
        index_name, index_arn = self.get_name_or_arn(self.index_name_or_arn)

        # limit to 5 requests per second
        # Poor-mans token bucket
        start_time = time.time()
        available_requests = 5
        added_ids = []
        for node_batch in iter_batch(nodes, self.insert_batch_size):
            vectors = []
            for node in node_batch:
                node_metadata = node_to_metadata_dict(node)

                # delete fields that aren't used to save space
                node_metadata.pop("document_id", None)
                node_metadata.pop("doc_id", None)
                node_metadata.pop("embedding", None)

                vectors.append(
                    {
                        "key": str(node.id_),
                        "data": {"float32": node.embedding},
                        "metadata": {**node_metadata},
                    }
                )

            kwargs = {
                "vectors": vectors,
                "vectorBucketName": self.bucket_name_or_arn,
            }
            if index_arn is not None:
                kwargs["indexArn"] = index_arn
            else:
                kwargs["indexName"] = index_name

            self._session.client("s3vectors").put_vectors(**kwargs)

            # Update the token bucket
            elapsed_time = time.time() - start_time
            if elapsed_time  1:
                available_requests = 5
            else:
                available_requests -= 1

            if available_requests == 0:
                time.sleep(1)
                available_requests = 5

            added_ids.extend([v["key"] for v in vectors])

        return added_ids

    async defasync_add(self, nodes: List[BaseNode], **kwargs: Any) -> List[str]:
"""
        Asynchronous method to add nodes to Qdrant index.

        Args:
            nodes: List[BaseNode]: List of nodes with embeddings.

        Returns:
            List of node IDs that were added to the index.

        Raises:
            ValueError: If trying to using async methods without aclient

        """
        return await asyncio.to_thread(self.add, nodes, **kwargs)

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.
            delete_kwargs (Any): Additional arguments to pass to the list_vectors method.

        """
        index_name, index_arn = self.get_name_or_arn(self.index_name_or_arn)
        next_token = None
        while True:
            kwargs = {
                "vectorBucketName": self.bucket_name_or_arn,
                "returnMetadata": True,
                **delete_kwargs,
            }
            if index_arn is not None:
                kwargs["indexArn"] = index_arn
            else:
                kwargs["indexName"] = index_name

            response = self._session.client("s3vectors").list_vectors(**kwargs)

            nodes_to_delete = [
                v["key"]
                for v in response.get("vectors", [])
                if v["metadata"]["ref_doc_id"] == ref_doc_id
            ]

            kwargs = {
                "vectorBucketName": self.bucket_name_or_arn,
                "keys": nodes_to_delete,
            }
            if index_arn is not None:
                kwargs["indexArn"] = index_arn
            else:
                kwargs["indexName"] = index_name

            self._session.client("s3vectors").delete_vectors(**kwargs)

            next_token = response.get("nextToken")
            if next_token is None:
                break

    async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Asynchronous method to delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        return await asyncio.to_thread(self.delete, ref_doc_id, **delete_kwargs)

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Delete nodes using with node_ids.

        Args:
            node_ids (Optional[List[str]): List of node IDs to delete.
            filters (Optional[MetadataFilters]): Metadata filters to apply.

        """
        if filters is not None:
            raise NotImplementedError("Deleting by filters is not supported yet")

        if node_ids is None:
            raise ValueError("node_ids is required")

        index_name, index_arn = self.get_name_or_arn(self.index_name_or_arn)
        kwargs = {
            "vectorBucketName": self.bucket_name_or_arn,
            "keys": node_ids,
        }
        if index_arn is not None:
            kwargs["indexArn"] = index_arn
        else:
            kwargs["indexName"] = index_name
        self._session.client("s3vectors").delete_vectors(**kwargs)

    async defadelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Asynchronous method to delete nodes using with node_ids.

        Args:
            node_ids (Optional[List[str]): List of node IDs to delete.
            filters (Optional[MetadataFilters]): Metadata filters to apply.

        """
        return await asyncio.to_thread(
            self.delete_nodes, node_ids=node_ids, filters=filters, **delete_kwargs
        )

    defclear(self) -> None:
"""
        Clear the index.
        """
        index_name, index_arn = self.get_name_or_arn(self.index_name_or_arn)
        kwargs = {
            "vectorBucketName": self.bucket_name_or_arn,
        }
        if index_arn is not None:
            kwargs["indexArn"] = index_arn
        else:
            kwargs["indexName"] = index_name
        self._session.client("s3vectors").delete_index(**kwargs)

    async defaclear(self) -> None:
"""
        Asynchronous method to clear the index.
        """
        return await asyncio.to_thread(self.clear)

    @property
    defclient(self) -> Any:
"""Return the Qdrant client."""
        return self._session.client("s3vectors")

    defquery(
        self,
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query (VectorStoreQuery): query

        """
        if query.mode != VectorStoreQueryMode.DEFAULT:
            raise NotImplementedError(
                "Only DEFAULT query mode is supported for S3VectorStore"
            )

        index_name, index_arn = self.get_name_or_arn(self.index_name_or_arn)
        kwargs = {
            "vectorBucketName": self.bucket_name_or_arn,
            "queryVector": {self.data_type: query.query_embedding},
            "topK": query.similarity_top_k,
            "filter": self._build_filter(query.filters),
            "returnDistance": True,
            "returnMetadata": True,
        }
        if index_arn is not None:
            kwargs["indexArn"] = index_arn
        else:
            kwargs["indexName"] = index_name
        response = self._session.client("s3vectors").query_vectors(**kwargs)

        nodes = self._parse_response(response)

        return VectorStoreQueryResult(
            nodes=nodes,
            similarities=self._convert_distances_to_similarities(
                response.get("vectors", [])
            ),
            ids=[v["key"] for v in response.get("vectors", [])],
        )

    async defaquery(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
"""
        Asynchronous method to query index for top k most similar nodes.

        Args:
            query (VectorStoreQuery): query

        """
        return await asyncio.to_thread(self.query, query, **kwargs)

    def_build_filter(self, filters: Optional[MetadataFilters]) -> Optional[dict]:
"""
        Build a filter for the query.
        """
        if filters is None:
            return None

        def_convert_single_filter(filter_obj) -> dict:
"""Convert a single MetadataFilter to S3 Vectors format."""
            if not isinstance(filter_obj, MetadataFilter):
                raise ValueError(f"Expected MetadataFilter, got {type(filter_obj)}")

            key = filter_obj.key
            value = filter_obj.value
            operator = filter_obj.operator

            # Map LlamaIndex operators to S3 Vectors operators
            operator_map = {
                FilterOperator.EQ: "$eq",
                FilterOperator.NE: "$ne",
                FilterOperator.GT: "$gt",
                FilterOperator.GTE: "$gte",
                FilterOperator.LT: "$lt",
                FilterOperator.LTE: "$lte",
                FilterOperator.IN: "$in",
                FilterOperator.NIN: "$nin",
            }

            if operator == FilterOperator.IS_EMPTY:
                # For IS_EMPTY, we use $exists with false
                return {key: {"$exists": False}}
            elif operator in operator_map:
                return {key: {operator_map[operator]: value}}
            else:
                # Unsupported operators - for now, we'll raise an error
                # Could potentially map TEXT_MATCH, ANY, ALL, CONTAINS if S3 Vectors supports them
                raise ValueError(f"Unsupported filter operator: {operator}")

        def_convert_filters_recursively(filters_obj) -> dict:
"""Recursively convert MetadataFilters to S3 Vectors format."""
            if isinstance(filters_obj, MetadataFilter):
                return _convert_single_filter(filters_obj)
            elif isinstance(filters_obj, MetadataFilters):
                filter_list = []

                for f in filters_obj.filters:
                    converted_filter = _convert_filters_recursively(f)
                    filter_list.append(converted_filter)

                # Handle the condition
                if len(filter_list) == 1:
                    return filter_list[0]
                elif filters_obj.condition == FilterCondition.AND:
                    return {"$and": filter_list}
                elif filters_obj.condition == FilterCondition.OR:
                    return {"$or": filter_list}
                elif filters_obj.condition == FilterCondition.NOT:
                    # S3 Vectors doesn't have explicit $not
                    # We would need to implement a custom filter that negates the logic
                    raise ValueError(
                        "NOT condition is not supported for S3 Vectors filters"
                    )
                else:
                    raise ValueError(
                        f"Unexpected filter condition: {filters_obj.condition}"
                    )
            else:
                raise ValueError(f"Unexpected filter type: {type(filters_obj)}")

        return _convert_filters_recursively(filters)

    def_convert_distances_to_similarities(self, vectors: List[dict]) -> List[float]:
"""
        Convert distances to similarity scores (0-1 scale, where 1 is most similar).

        Args:
            vectors: List of vector results containing distance values

        Returns:
            List of similarity scores normalized to [0, 1] where 1 is most similar

        """
        similarities = []

        for vector in vectors:
            distance = float(vector.get("distance", 0))

            if self.distance_metric.lower() == "cosine":
                # Cosine distance is typically in range [0, 2] where 0 is most similar
                # Convert to similarity: similarity = 1 - (distance / 2)
                # But if distance is already normalized to [0, 1], use: similarity = 1 - distance
                similarity = max(0.0, min(1.0, 1.0 - distance))
            elif self.distance_metric.lower() == "euclidean":
                # Euclidean distance ranges from 0 to infinity
                # Use: similarity = 1 / (1 + distance) which maps [0, ∞) to (0, 1]
                similarity = 1.0 / (1.0 + distance)
            else:
                # For unknown metrics, assume cosine-like behavior
                similarity = max(0.0, min(1.0, 1.0 - distance))

            similarities.append(similarity)

        return similarities

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/s3/#llama_index.vector_stores.s3.S3VectorStore.client "Permanent link")

```
client: 

```

Return the Qdrant client.
###  create_index_from_bucket `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/s3/#llama_index.vector_stores.s3.S3VectorStore.create_index_from_bucket "Permanent link")

```
create_index_from_bucket(
    bucket_name_or_arn: ,
    index_name: ,
    dimension: ,
    distance_metric:  = "cosine",
    data_type:  = "float32",
    insert_batch_size:  = 500,
    non_filterable_metadata_keys: Optional[
        []
    ] = None,
    sync_session: Optional[Session] = None,
    async_session: Optional[] = None,
) -> 

```

Create an index in S3Vectors.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-s3/llama_index/vector_stores/s3/base.py`  
| 
```
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
```
 | 
```
@classmethod
defcreate_index_from_bucket(
    cls,
    bucket_name_or_arn: str,
    index_name: str,
    dimension: int,
    distance_metric: str = "cosine",
    data_type: str = "float32",
    insert_batch_size: int = 500,
    non_filterable_metadata_keys: Optional[List[str]] = None,
    sync_session: Optional[boto3.Session] = None,
    async_session: Optional[Any] = None,
) -> "S3VectorStore":
"""
    Create an index in S3Vectors.
    """
    # node content and node type should never be filterable by default
    non_filterable_metadata_keys = non_filterable_metadata_keys or []
    if "_node_content" not in non_filterable_metadata_keys:
        non_filterable_metadata_keys.append("_node_content")
    if "_node_type" not in non_filterable_metadata_keys:
        non_filterable_metadata_keys.append("_node_type")

    bucket_name, bucket_arn = cls.get_name_or_arn(bucket_name_or_arn)

    sync_session = sync_session or boto3.Session()
    kwargs = {
        "indexName": index_name,
        "dimension": dimension,
        "dataType": data_type,
        "distanceMetric": distance_metric,
        "metadataConfiguration": {
            "nonFilterableMetadataKeys": non_filterable_metadata_keys,
        },
    }
    if bucket_arn is not None:
        kwargs["vectorBucketArn"] = bucket_arn
    else:
        kwargs["vectorBucketName"] = bucket_name

    sync_session.client("s3vectors").create_index(**kwargs)

    return cls(
        sync_session=sync_session,
        async_session=async_session,
        data_type=data_type,
        index_name_or_arn=index_name,
        bucket_name_or_arn=bucket_name_or_arn,
        insert_batch_size=insert_batch_size,
        distance_metric=distance_metric,
    )

```
 |  
| --- | --- |  
###  get_name_or_arn `staticmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/s3/#llama_index.vector_stores.s3.S3VectorStore.get_name_or_arn "Permanent link")

```
get_name_or_arn(name_or_arn: ) -> Tuple[, ]

```

Get the name or ARN.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-s3/llama_index/vector_stores/s3/base.py`  
| 
```
167
168
169
170
171
172
173
174
```
 | 
```
@staticmethod
defget_name_or_arn(name_or_arn: str) -> Tuple[str, str]:
"""
    Get the name or ARN.
    """
    if "arn:" in name_or_arn:
        return None, name_or_arn
    return name_or_arn, None

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/s3/#llama_index.vector_stores.s3.S3VectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Get nodes from the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  List of node IDs to retrieve.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters to apply.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[BaseNode]: List of nodes retrieved from the index.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-s3/llama_index/vector_stores/s3/base.py`  
| 
```
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
```
 | 
```
defget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> List[BaseNode]:
"""
    Get nodes from the index.

    Args:
        node_ids (Optional[List[str]]): List of node IDs to retrieve.
        filters (Optional[MetadataFilters]): Metadata filters to apply.

    Returns:
        List[BaseNode]: List of nodes retrieved from the index.

    """
    if node_ids is None:
        raise ValueError("node_ids is required")

    if filters is not None:
        raise NotImplementedError("Filters are not supported yet")

    index_name, index_arn = self.get_name_or_arn(self.index_name_or_arn)

    kwargs = {
        "keys": node_ids,
        "vectorBucketName": self.bucket_name_or_arn,
        "returnMetadata": True,
    }
    if index_arn is not None:
        kwargs["indexArn"] = index_arn
    else:
        kwargs["indexName"] = index_name

    response = self._session.client("s3vectors").get_vectors(**kwargs)
    return self._parse_response(response)

```
 |  
| --- | --- |  
###  aget_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/s3/#llama_index.vector_stores.s3.S3VectorStore.aget_nodes "Permanent link")

```
aget_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Asynchronous method to get nodes from the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  List of node IDs to retrieve.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters to apply.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[BaseNode]: List of nodes retrieved from the index.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-s3/llama_index/vector_stores/s3/base.py`  
| 
```
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
```
 | 
```
async defaget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> List[BaseNode]:
"""
    Asynchronous method to get nodes from the index.

    Args:
        node_ids (Optional[List[str]]): List of node IDs to retrieve.
        filters (Optional[MetadataFilters]): Metadata filters to apply.

    Returns:
        List[BaseNode]: List of nodes retrieved from the index.

    """
    return await asyncio.to_thread(
        self.get_nodes, node_ids=node_ids, filters=filters
    )

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/s3/#llama_index.vector_stores.s3.S3VectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-s3/llama_index/vector_stores/s3/base.py`  
| 
```
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
```
 | 
```
defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
    Add nodes to index.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings

    """
    index_name, index_arn = self.get_name_or_arn(self.index_name_or_arn)

    # limit to 5 requests per second
    # Poor-mans token bucket
    start_time = time.time()
    available_requests = 5
    added_ids = []
    for node_batch in iter_batch(nodes, self.insert_batch_size):
        vectors = []
        for node in node_batch:
            node_metadata = node_to_metadata_dict(node)

            # delete fields that aren't used to save space
            node_metadata.pop("document_id", None)
            node_metadata.pop("doc_id", None)
            node_metadata.pop("embedding", None)

            vectors.append(
                {
                    "key": str(node.id_),
                    "data": {"float32": node.embedding},
                    "metadata": {**node_metadata},
                }
            )

        kwargs = {
            "vectors": vectors,
            "vectorBucketName": self.bucket_name_or_arn,
        }
        if index_arn is not None:
            kwargs["indexArn"] = index_arn
        else:
            kwargs["indexName"] = index_name

        self._session.client("s3vectors").put_vectors(**kwargs)

        # Update the token bucket
        elapsed_time = time.time() - start_time
        if elapsed_time  1:
            available_requests = 5
        else:
            available_requests -= 1

        if available_requests == 0:
            time.sleep(1)
            available_requests = 5

        added_ids.extend([v["key"] for v in vectors])

    return added_ids

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/s3/#llama_index.vector_stores.s3.S3VectorStore.async_add "Permanent link")

```
async_add(
    nodes: [], **kwargs: 
) -> []

```

Asynchronous method to add nodes to Qdrant index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: List of nodes with embeddings.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List of node IDs that were added to the index.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If trying to using async methods without aclient  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-s3/llama_index/vector_stores/s3/base.py`  
| 
```
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
```
 | 
```
async defasync_add(self, nodes: List[BaseNode], **kwargs: Any) -> List[str]:
"""
    Asynchronous method to add nodes to Qdrant index.

    Args:
        nodes: List[BaseNode]: List of nodes with embeddings.

    Returns:
        List of node IDs that were added to the index.

    Raises:
        ValueError: If trying to using async methods without aclient

    """
    return await asyncio.to_thread(self.add, nodes, **kwargs)

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/s3/#llama_index.vector_stores.s3.S3VectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
|  `delete_kwargs`  |  Additional arguments to pass to the list_vectors method.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-s3/llama_index/vector_stores/s3/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.
        delete_kwargs (Any): Additional arguments to pass to the list_vectors method.

    """
    index_name, index_arn = self.get_name_or_arn(self.index_name_or_arn)
    next_token = None
    while True:
        kwargs = {
            "vectorBucketName": self.bucket_name_or_arn,
            "returnMetadata": True,
            **delete_kwargs,
        }
        if index_arn is not None:
            kwargs["indexArn"] = index_arn
        else:
            kwargs["indexName"] = index_name

        response = self._session.client("s3vectors").list_vectors(**kwargs)

        nodes_to_delete = [
            v["key"]
            for v in response.get("vectors", [])
            if v["metadata"]["ref_doc_id"] == ref_doc_id
        ]

        kwargs = {
            "vectorBucketName": self.bucket_name_or_arn,
            "keys": nodes_to_delete,
        }
        if index_arn is not None:
            kwargs["indexArn"] = index_arn
        else:
            kwargs["indexName"] = index_name

        self._session.client("s3vectors").delete_vectors(**kwargs)

        next_token = response.get("nextToken")
        if next_token is None:
            break

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/s3/#llama_index.vector_stores.s3.S3VectorStore.adelete "Permanent link")

```
adelete(ref_doc_id: , **delete_kwargs: ) -> None

```

Asynchronous method to delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-s3/llama_index/vector_stores/s3/base.py`  
| 
```
374
375
376
377
378
379
380
381
382
```
 | 
```
async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Asynchronous method to delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    return await asyncio.to_thread(self.delete, ref_doc_id, **delete_kwargs)

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/s3/#llama_index.vector_stores.s3.S3VectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Delete nodes using with node_ids.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]`  |  List of node IDs to delete.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters to apply.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-s3/llama_index/vector_stores/s3/base.py`  
| 
```
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
    Delete nodes using with node_ids.

    Args:
        node_ids (Optional[List[str]): List of node IDs to delete.
        filters (Optional[MetadataFilters]): Metadata filters to apply.

    """
    if filters is not None:
        raise NotImplementedError("Deleting by filters is not supported yet")

    if node_ids is None:
        raise ValueError("node_ids is required")

    index_name, index_arn = self.get_name_or_arn(self.index_name_or_arn)
    kwargs = {
        "vectorBucketName": self.bucket_name_or_arn,
        "keys": node_ids,
    }
    if index_arn is not None:
        kwargs["indexArn"] = index_arn
    else:
        kwargs["indexName"] = index_name
    self._session.client("s3vectors").delete_vectors(**kwargs)

```
 |  
| --- | --- |  
###  adelete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/s3/#llama_index.vector_stores.s3.S3VectorStore.adelete_nodes "Permanent link")

```
adelete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Asynchronous method to delete nodes using with node_ids.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]`  |  List of node IDs to delete.  |  `None`  |  
|  `filters`  |  `Optional[MetadataFilters[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.MetadataFilters "MetadataFilters \(llama_index.core.vector_stores.types.MetadataFilters\)")]`  |  Metadata filters to apply.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-s3/llama_index/vector_stores/s3/base.py`  
| 
```
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
```
 | 
```
async defadelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Asynchronous method to delete nodes using with node_ids.

    Args:
        node_ids (Optional[List[str]): List of node IDs to delete.
        filters (Optional[MetadataFilters]): Metadata filters to apply.

    """
    return await asyncio.to_thread(
        self.delete_nodes, node_ids=node_ids, filters=filters, **delete_kwargs
    )

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/s3/#llama_index.vector_stores.s3.S3VectorStore.clear "Permanent link")

```
clear() -> None

```

Clear the index.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-s3/llama_index/vector_stores/s3/base.py`  
| 
```
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
```
 | 
```
defclear(self) -> None:
"""
    Clear the index.
    """
    index_name, index_arn = self.get_name_or_arn(self.index_name_or_arn)
    kwargs = {
        "vectorBucketName": self.bucket_name_or_arn,
    }
    if index_arn is not None:
        kwargs["indexArn"] = index_arn
    else:
        kwargs["indexName"] = index_name
    self._session.client("s3vectors").delete_index(**kwargs)

```
 |  
| --- | --- |  
###  aclear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/s3/#llama_index.vector_stores.s3.S3VectorStore.aclear "Permanent link")

```
aclear() -> None

```

Asynchronous method to clear the index.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-s3/llama_index/vector_stores/s3/base.py`  
| 
```
447
448
449
450
451
```
 | 
```
async defaclear(self) -> None:
"""
    Asynchronous method to clear the index.
    """
    return await asyncio.to_thread(self.clear)

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/s3/#llama_index.vector_stores.s3.S3VectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  query  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-s3/llama_index/vector_stores/s3/base.py`  
| 
```
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
```
 | 
```
defquery(
    self,
    query: VectorStoreQuery,
    **kwargs: Any,
) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query (VectorStoreQuery): query

    """
    if query.mode != VectorStoreQueryMode.DEFAULT:
        raise NotImplementedError(
            "Only DEFAULT query mode is supported for S3VectorStore"
        )

    index_name, index_arn = self.get_name_or_arn(self.index_name_or_arn)
    kwargs = {
        "vectorBucketName": self.bucket_name_or_arn,
        "queryVector": {self.data_type: query.query_embedding},
        "topK": query.similarity_top_k,
        "filter": self._build_filter(query.filters),
        "returnDistance": True,
        "returnMetadata": True,
    }
    if index_arn is not None:
        kwargs["indexArn"] = index_arn
    else:
        kwargs["indexName"] = index_name
    response = self._session.client("s3vectors").query_vectors(**kwargs)

    nodes = self._parse_response(response)

    return VectorStoreQueryResult(
        nodes=nodes,
        similarities=self._convert_distances_to_similarities(
            response.get("vectors", [])
        ),
        ids=[v["key"] for v in response.get("vectors", [])],
    )

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/s3/#llama_index.vector_stores.s3.S3VectorStore.aquery "Permanent link")

```
aquery(
    query: , **kwargs: 
) -> 

```

Asynchronous method to query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  query  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-s3/llama_index/vector_stores/s3/base.py`  
| 
```
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
```
 | 
```
async defaquery(
    self, query: VectorStoreQuery, **kwargs: Any
) -> VectorStoreQueryResult:
"""
    Asynchronous method to query index for top k most similar nodes.

    Args:
        query (VectorStoreQuery): query

    """
    return await asyncio.to_thread(self.query, query, **kwargs)

```
 |  
| --- | --- |  
options: members: - S3VectorStore
