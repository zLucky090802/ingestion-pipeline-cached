# Bigquery
##  BigQueryVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/bigquery/#llama_index.vector_stores.bigquery.BigQueryVectorStore "Permanent link")
Bases: 
Vector store index using Google BigQuery.
Provides integration with BigQuery for storing and querying vector embeddings. For more information, visit: https://cloud.google.com/bigquery/docs/vector-search-intro
Required IAM Permissions
  * `roles/bigquery.dataOwner` (BigQuery Data Owner)
  * `roles/bigquery.dataEditor` (BigQuery Data Editor)


Examples:
`pip install llama-index-vector-stores-bigquery`

```
fromgoogle.cloud.bigqueryimport Client
fromllama_index.vector_stores.bigqueryimport BigQueryVectorStore

client = Client()

vector_store = BigQueryVectorStore(
    table_id="my_bigquery_table",
    dataset_id="my_bigquery_dataset",
    bigquery_client=client,
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-bigquery/llama_index/vector_stores/bigquery/base.py`  
| 
```
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
```
 | 
```
classBigQueryVectorStore(BasePydanticVectorStore):
"""
    Vector store index using Google BigQuery.

    Provides integration with BigQuery for storing and querying vector embeddings.
    For more information, visit: https://cloud.google.com/bigquery/docs/vector-search-intro

    Required IAM Permissions:
        - `roles/bigquery.dataOwner` (BigQuery Data Owner)
        - `roles/bigquery.dataEditor` (BigQuery Data Editor)

    Examples:
        `pip install llama-index-vector-stores-bigquery`

        ```python
        from google.cloud.bigquery import Client
        from llama_index.vector_stores.bigquery import BigQueryVectorStore

        client = Client()

        vector_store = BigQueryVectorStore(
            table_id="my_bigquery_table",
            dataset_id="my_bigquery_dataset",
            bigquery_client=client,

        ```

    """

    stores_text: bool = True
    distance_type: DistanceType = DistanceType.EUCLIDEAN

    _table: bigquery.Table = PrivateAttr()
    _dataset: bigquery.Dataset = PrivateAttr()
    _client: bigquery.Client = PrivateAttr()
    _full_table_id: str = PrivateAttr()

    def__init__(
        self,
        table_id: str,
        dataset_id: str,
        project_id: Optional[str] = None,
        region: Optional[str] = None,
        distance_type: Optional[DistanceType] = DistanceType.EUCLIDEAN,
        auth_credentials: Optional[credentials.Credentials] = None,
        bigquery_client: Optional[bigquery.Client] = None,
        **kwargs: Any,
    ):
"""
        Initialize a BigQuery Vector store.

        If a `bigquery_client` is provided, it will be used directly. Otherwise, a client will be initialized using
        the optional `project_id`, `region`, and/or `auth_credentials`. If none are provided, default credentials
        will be used. For details on authentication, visit:
        https://googleapis.dev/python/google-api-core/latest/auth.html

        Args:
            table_id: The ID of the BigQuery table to use for vector storage.
            dataset_id: The ID of the dataset containing the table.
            project_id: The GCP project ID. If not provided, it will be inferred from the client or environment.
            region: Optionally specify a default location for datasets / tables.
            distance_type: Optionally specify a distance type to use `EUCLIDEAN`, `COSINE`, or `DOT_PRODUCT`.
            auth_credentials: Optional credentials object used to authenticate with BigQuery.
            bigquery_client: An existing BigQuery client instance. If not provided, one will be created.
            **kwargs: Additional keyword arguments passed to the parent class.

        """
        super().__init__(
            **kwargs,
        )

        self._client: bigquery.Client = bigquery_client or self._initialize_client(
            project_id, region, auth_credentials
        )
        self._dataset: bigquery.Dataset = self._create_dataset_if_not_exists(dataset_id)
        self._table: bigquery.Table = self._create_table_if_not_exists(table_id)
        self._full_table_id: str = (
            f"{self._client.project}.{self._dataset.dataset_id}.{self._table.table_id}"
        )
        self.distance_type: DistanceType = DistanceType(distance_type)

    @classmethod
    deffrom_params(
        cls,
        table_id: str,
        dataset_id: str,
        project_id: Optional[str] = None,
        region: Optional[str] = None,
        distance_type: Optional[DistanceType] = DistanceType.EUCLIDEAN,
        auth_credentials: Optional[credentials.Credentials] = None,
        bigquery_client: Optional[bigquery.Client] = None,
    ) -> "BigQueryVectorStore":
"""
        Initialize a BigQuery Vector store.

        Args:
            table_id: The ID of the BigQuery table to use for vector storage.
            dataset_id: The ID of the dataset containing the table.
            project_id: The GCP project ID. If not provided, it will be inferred from the client or environment.
            region: Optionally specify a default location for datasets / tables.
            distance_type: Optionally specify a distance type to use `EUCLIDEAN`, `COSINE`, or `DOT_PRODUCT`.
            auth_credentials: Optional credentials object used to authenticate with BigQuery.
            bigquery_client: An existing BigQuery client instance. If not provided, one will be created.

        Returns:
            BigQueryVectorStore

        """
        return cls(
            table_id=table_id,
            dataset_id=dataset_id,
            project_id=project_id,
            region=region,
            distance_type=distance_type,
            auth_credentials=auth_credentials,
            bigquery_client=bigquery_client,
        )

    @property
    defclient(self) -> Union[bigquery.Client, None]:
"""Return the BigQuery client."""
        if not self._client:
            return None
        return self._client

    @staticmethod
    def_initialize_client(
        project_id: Union[str, None],
        region: Union[str, None],
        auth_credentials: Union[credentials.Credentials, None],
    ) -> bigquery.Client:
"""
        Initialize a new BigQuery client using the provided `project_id`, `region` and/or `auth_credentials`.
        Defaults will be used in place of missing arguments. For details on authentication, see:
        https://googleapis.dev/python/google-api-core/latest/auth.html

        Args:
            project_id: GCP project ID for the new client, or None to use default project resolution.
            region: GCP region for the new client, or None to use default region.
            auth_credentials: Credentials to authenticate the new client, or None to use default credentials.

        Returns:
            An initialized BigQuery client.

        """
        return bigquery.Client(
            project=project_id or None,
            location=region or None,
            credentials=auth_credentials or None,
        )

    @staticmethod
    def_bigquery_row_to_node(row: _BigQueryRow) -> BaseNode:
"""
        Convert a BigQuery row to a BaseNode object.

        Args:
            row: A row retrieved from BigQuery containing node_id, text,
                metadata, embedding, and optional distance.

        Returns:
            Node object.

        """
        node_id: str = row.node_id
        text: str = row.text
        metadata: Dict[str, Any] = row.metadata
        embedding: List[float] = row.embedding
        _: Union[float, None] = row.distance

        try:
            node = metadata_dict_to_node(metadata)
            node.set_content(text)
            node.embedding = embedding
        except (ValueError, TypeError) as e:
            node = TextNode(
                id_=node_id,
                text=text,
                metadata=metadata,
                embedding=embedding,
            )
            _logger.warning(
                f"Failed to construct node {node_id} from metadata. Falling back to manual construction. Error: {e}"
            )

        return node

    def_create_dataset_if_not_exists(self, dataset_id: str) -> bigquery.Dataset:
"""
        Create a BigQuery dataset if it does not already exist.

        For more details on creating datasets, visit:
        https://cloud.google.com/bigquery/docs/datasets#create-dataset

        Args:
            dataset_id: The ID of the dataset to create.

        Returns:
            Dataset ID.

        """
        dataset_ref = bigquery.dataset.DatasetReference(
            project=self._client.project, dataset_id=dataset_id
        )

        return self._client.create_dataset(dataset_ref, exists_ok=True)

    def_create_table_if_not_exists(self, table_id) -> bigquery.Table:
"""
        Create a BigQuery table if it does not already exist.

        For more information on creating tables, visit:
        https://cloud.google.com/bigquery/docs/tables#create-table

        Args:
            table_id: The ID of the table to create.

        Returns:
            BigQuery table instance.

        """
        schema = [
            bigquery.SchemaField("node_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("text", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("metadata", "JSON"),
            bigquery.SchemaField("embedding", "FLOAT", mode="REPEATED"),
        ]

        table_ref = bigquery.TableReference.from_string(
            f"{self._client.project}.{self._dataset.dataset_id}.{table_id}"
        )
        to_create = bigquery.Table(table_ref, schema=schema)

        return self._client.create_table(to_create, exists_ok=True)

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
        Add nodes to index.

        Args:
            nodes: List of nodes with embeddings.

        Returns:
            List of node IDs that were added.

        """
        node_ids: List[str] = []
        json_records: List[Dict[str, Any]] = []

        for node in nodes:
            record = {
                "node_id": node.node_id,
                "text": node.get_content(metadata_mode=MetadataMode.NONE),
                "embedding": node.get_embedding(),
                "metadata": node_to_metadata_dict(
                    node, remove_text=True, flat_metadata=False
                ),
            }
            node_ids.append(node.node_id)
            json_records.append(record)

        job_config = bigquery.LoadJobConfig(schema=self._table.schema)
        job = self._client.load_table_from_json(
            json_rows=json_records, destination=self._table, job_config=job_config
        )
        job.result()

        return node_ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id : The doc_id of the document to delete.

        """
        query = f"""
        DELETE FROM `{self._full_table_id}`
        WHERE  SAFE.JSON_VALUE(metadata, '$."doc_id"') = @to_delete;
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter(
                    name="to_delete", type_="STRING", value=ref_doc_id
                ),
            ]
        )

        self._client.query_and_wait(query, job_config=job_config)

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query the vector store using BigQuery's VECTOR_SEARCH to retrieve the top-k most similar nodes.

        When `MetadataFilters` are provided and the table is indexed on relevant columns, BigQuery attempts to optimize
        the search with pre-filtering before nearest neighbor search. If filters don't align with an index,
        post-filtering is applied after similarity search, potentially returning fewer than `similarity_top_k results`.
        Consider increasing `similarity_top_k` when post-filtering is expected.

        For more information on pre-filtering and post-filtering, see:
        https://cloud.google.com/bigquery/docs/vector-index#pre-filters_and_post-filters

        Assumes embeddings are normalized for similarity scoring.

        Args:
            query: Contains the query embedding, similarity_top_k value, and optional metadata filters.

        Returns:
            VectorStoreQueryResult

        """
        where_clause, query_params = build_where_clause_and_params(
            filters=query.filters, node_ids=query.node_ids
        )

        base_table_query = f"""
        SELECT
            node_id,
            text,
            metadata,
            embedding
        FROM `{self._full_table_id}`
        """

        if where_clause:
            base_table_query += f" WHERE {where_clause}"

        query_table_query = f"SELECT {query.query_embedding} AS input_embedding"

        vector_search_query = f"""
        SELECT  base.node_id   AS node_id,
                base.text      AS text,
                base.metadata  AS metadata,
                base.embedding AS embedding,
                distance
        FROM
            VECTOR_SEARCH(
{base_table_query}), 'embedding',
{query_table_query}), 'input_embedding',
                top_k => @top_k,
                distance_type => @distance_type

        """

        query_params.extend(
            [
                bigquery.ScalarQueryParameter(
                    "top_k", type_="INTEGER", value=query.similarity_top_k
                ),
                bigquery.ScalarQueryParameter(
                    "distance_type", type_="STRING", value=self.distance_type
                ),
            ]
        )
        job_config = bigquery.QueryJobConfig(
            query_parameters=query_params,
        )
        rows: bigquery.table.RowIterator = self._client.query_and_wait(
            vector_search_query, job_config=job_config
        )

        top_k_nodes: List[BaseNode] = []
        top_k_scores: List[float] = []
        top_k_ids: List[str] = []

        for record in rows:
            row = _BigQueryRow(
                node_id=record.node_id,
                text=record.text,
                metadata=record.metadata,
                embedding=record.embedding,
                distance=record.distance,
            )
            node = self._bigquery_row_to_node(row)
            node_id = record.node_id
            # Assumes embeddings are normalized.
            score = (
                1 / (1 + record.distance)
                if self.distance_type == DistanceType.EUCLIDEAN
                else (1 + record.distance) / 2
            )

            top_k_nodes.append(node)
            top_k_scores.append(score)
            top_k_ids.append(node_id)

        return VectorStoreQueryResult(
            nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
        )

    defget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> List[BaseNode]:
"""
        Retrieve nodes from BigQuery using node IDs, metadata filters, or both.

        If both `node_ids` and `filters` are provided, only nodes that satisfy
        both conditions will be returned.

        Args:
            node_ids: Optional list of node IDs for retrieval.
            filters : Optional MetadataFilters filters for retrieval.

        Returns:
            A list of matching nodes.

        Raises:
            ValueError: If neither `node_ids` nor `filters` is provided.

        """
        if not (node_ids or filters):
            raise ValueError(
                "get_nodes requires at least one filtering parameter: "
                "'node_ids', 'filters', or both. Received neither."
            )

        where_clause, query_params = build_where_clause_and_params(node_ids, filters)

        query = f"""
        SELECT  node_id,
                text,
                embedding,
                metadata
        FROM    `{self._full_table_id}`
        WHERE   {where_clause};
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=query_params,
        )
        rows: bigquery.table.RowIterator = self._client.query_and_wait(
            query, job_config=job_config
        )

        nodes: List[BaseNode] = []
        for record in rows:
            row = _BigQueryRow(
                node_id=record.node_id,
                text=record.text,
                metadata=record.metadata,
                embedding=record.embedding,
                distance=record.distance,
            )
            node = self._bigquery_row_to_node(row)

            nodes.append(node)

        return nodes

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Delete nodes from BigQuery based on node IDs, metadata filters, or both.

        If both `node_ids` and `filters` are provided, only nodes matching both
        criteria will be deleted.

        Args:
            node_ids: Optional list of node IDs to delete.
            filters : Optional MetadataFilters filters for deletion.

        Raises:
            ValueError: If neither `node_ids` nor `filters` are provided.

        """
        if not (node_ids or filters):
            raise ValueError(
                "delete_nodes requires at least one filtering parameter: "
                "'node_ids', 'filters', or both. Received neither."
            )

        where_clause, query_params = build_where_clause_and_params(node_ids, filters)

        query = f"""
        DELETE FROM `{self._full_table_id}`
        WHERE {where_clause};
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=query_params,
        )
        self._client.query_and_wait(query, job_config=job_config)

    defclear(self) -> None:
"""
        Clears the index.

        This truncates the underlying table in BigQuery.
        """
        query = f"""TRUNCATE TABLE `{self._full_table_id}`;"""
        self._client.query_and_wait(query)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/bigquery/#llama_index.vector_stores.bigquery.BigQueryVectorStore.client "Permanent link")

```
client: Union[Client, None]

```

Return the BigQuery client.
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/bigquery/#llama_index.vector_stores.bigquery.BigQueryVectorStore.from_params "Permanent link")

```
from_params(
    table_id: ,
    dataset_id: ,
    project_id: Optional[] = None,
    region: Optional[] = None,
    distance_type: Optional[DistanceType] = EUCLIDEAN,
    auth_credentials: Optional[Credentials] = None,
    bigquery_client: Optional[Client] = None,
) -> 

```

Initialize a BigQuery Vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `table_id`  |  The ID of the BigQuery table to use for vector storage.  |  _required_  |  
|  `dataset_id`  |  The ID of the dataset containing the table.  |  _required_  |  
|  `project_id`  |  `Optional[str]`  |  The GCP project ID. If not provided, it will be inferred from the client or environment.  |  `None`  |  
|  `region`  |  `Optional[str]`  |  Optionally specify a default location for datasets / tables.  |  `None`  |  
|  `distance_type`  |  `Optional[DistanceType]`  |  Optionally specify a distance type to use `EUCLIDEAN`, `COSINE`, or `DOT_PRODUCT`.  |  `EUCLIDEAN`  |  
|  `auth_credentials`  |  `Optional[Credentials]`  |  Optional credentials object used to authenticate with BigQuery.  |  `None`  |  
|  `bigquery_client`  |  `Optional[Client]`  |  An existing BigQuery client instance. If not provided, one will be created.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  BigQueryVectorStore  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-bigquery/llama_index/vector_stores/bigquery/base.py`  
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
```
 | 
```
@classmethod
deffrom_params(
    cls,
    table_id: str,
    dataset_id: str,
    project_id: Optional[str] = None,
    region: Optional[str] = None,
    distance_type: Optional[DistanceType] = DistanceType.EUCLIDEAN,
    auth_credentials: Optional[credentials.Credentials] = None,
    bigquery_client: Optional[bigquery.Client] = None,
) -> "BigQueryVectorStore":
"""
    Initialize a BigQuery Vector store.

    Args:
        table_id: The ID of the BigQuery table to use for vector storage.
        dataset_id: The ID of the dataset containing the table.
        project_id: The GCP project ID. If not provided, it will be inferred from the client or environment.
        region: Optionally specify a default location for datasets / tables.
        distance_type: Optionally specify a distance type to use `EUCLIDEAN`, `COSINE`, or `DOT_PRODUCT`.
        auth_credentials: Optional credentials object used to authenticate with BigQuery.
        bigquery_client: An existing BigQuery client instance. If not provided, one will be created.

    Returns:
        BigQueryVectorStore

    """
    return cls(
        table_id=table_id,
        dataset_id=dataset_id,
        project_id=project_id,
        region=region,
        distance_type=distance_type,
        auth_credentials=auth_credentials,
        bigquery_client=bigquery_client,
    )

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/bigquery/#llama_index.vector_stores.bigquery.BigQueryVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes with embeddings.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List of node IDs that were added.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-bigquery/llama_index/vector_stores/bigquery/base.py`  
| 
```
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
```
 | 
```
defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
    Add nodes to index.

    Args:
        nodes: List of nodes with embeddings.

    Returns:
        List of node IDs that were added.

    """
    node_ids: List[str] = []
    json_records: List[Dict[str, Any]] = []

    for node in nodes:
        record = {
            "node_id": node.node_id,
            "text": node.get_content(metadata_mode=MetadataMode.NONE),
            "embedding": node.get_embedding(),
            "metadata": node_to_metadata_dict(
                node, remove_text=True, flat_metadata=False
            ),
        }
        node_ids.append(node.node_id)
        json_records.append(record)

    job_config = bigquery.LoadJobConfig(schema=self._table.schema)
    job = self._client.load_table_from_json(
        json_rows=json_records, destination=self._table, job_config=job_config
    )
    job.result()

    return node_ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/bigquery/#llama_index.vector_stores.bigquery.BigQueryVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id `  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-bigquery/llama_index/vector_stores/bigquery/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id : The doc_id of the document to delete.

    """
    query = f"""
    DELETE FROM `{self._full_table_id}`
    WHERE  SAFE.JSON_VALUE(metadata, '$."doc_id"') = @to_delete;
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                name="to_delete", type_="STRING", value=ref_doc_id
            ),
        ]
    )

    self._client.query_and_wait(query, job_config=job_config)

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/bigquery/#llama_index.vector_stores.bigquery.BigQueryVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query the vector store using BigQuery's VECTOR_SEARCH to retrieve the top-k most similar nodes.
When `MetadataFilters` are provided and the table is indexed on relevant columns, BigQuery attempts to optimize the search with pre-filtering before nearest neighbor search. If filters don't align with an index, post-filtering is applied after similarity search, potentially returning fewer than `similarity_top_k results`. Consider increasing `similarity_top_k` when post-filtering is expected.
For more information on pre-filtering and post-filtering, see: https://cloud.google.com/bigquery/docs/vector-index#pre-filters_and_post-filters
Assumes embeddings are normalized for similarity scoring.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  Contains the query embedding, similarity_top_k value, and optional metadata filters.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  VectorStoreQueryResult  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-bigquery/llama_index/vector_stores/bigquery/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query the vector store using BigQuery's VECTOR_SEARCH to retrieve the top-k most similar nodes.

    When `MetadataFilters` are provided and the table is indexed on relevant columns, BigQuery attempts to optimize
    the search with pre-filtering before nearest neighbor search. If filters don't align with an index,
    post-filtering is applied after similarity search, potentially returning fewer than `similarity_top_k results`.
    Consider increasing `similarity_top_k` when post-filtering is expected.

    For more information on pre-filtering and post-filtering, see:
    https://cloud.google.com/bigquery/docs/vector-index#pre-filters_and_post-filters

    Assumes embeddings are normalized for similarity scoring.

    Args:
        query: Contains the query embedding, similarity_top_k value, and optional metadata filters.

    Returns:
        VectorStoreQueryResult

    """
    where_clause, query_params = build_where_clause_and_params(
        filters=query.filters, node_ids=query.node_ids
    )

    base_table_query = f"""
    SELECT
        node_id,
        text,
        metadata,
        embedding
    FROM `{self._full_table_id}`
    """

    if where_clause:
        base_table_query += f" WHERE {where_clause}"

    query_table_query = f"SELECT {query.query_embedding} AS input_embedding"

    vector_search_query = f"""
    SELECT  base.node_id   AS node_id,
            base.text      AS text,
            base.metadata  AS metadata,
            base.embedding AS embedding,
            distance
    FROM
        VECTOR_SEARCH(
{base_table_query}), 'embedding',
{query_table_query}), 'input_embedding',
            top_k => @top_k,
            distance_type => @distance_type
    );
    """

    query_params.extend(
        [
            bigquery.ScalarQueryParameter(
                "top_k", type_="INTEGER", value=query.similarity_top_k
            ),
            bigquery.ScalarQueryParameter(
                "distance_type", type_="STRING", value=self.distance_type
            ),
        ]
    )
    job_config = bigquery.QueryJobConfig(
        query_parameters=query_params,
    )
    rows: bigquery.table.RowIterator = self._client.query_and_wait(
        vector_search_query, job_config=job_config
    )

    top_k_nodes: List[BaseNode] = []
    top_k_scores: List[float] = []
    top_k_ids: List[str] = []

    for record in rows:
        row = _BigQueryRow(
            node_id=record.node_id,
            text=record.text,
            metadata=record.metadata,
            embedding=record.embedding,
            distance=record.distance,
        )
        node = self._bigquery_row_to_node(row)
        node_id = record.node_id
        # Assumes embeddings are normalized.
        score = (
            1 / (1 + record.distance)
            if self.distance_type == DistanceType.EUCLIDEAN
            else (1 + record.distance) / 2
        )

        top_k_nodes.append(node)
        top_k_scores.append(score)
        top_k_ids.append(node_id)

    return VectorStoreQueryResult(
        nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
    )

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/bigquery/#llama_index.vector_stores.bigquery.BigQueryVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Retrieve nodes from BigQuery using node IDs, metadata filters, or both.
If both `node_ids` and `filters` are provided, only nodes that satisfy both conditions will be returned.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  Optional list of node IDs for retrieval.  |  `None`  |  
|  `filters `  |  Optional MetadataFilters filters for retrieval.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  A list of matching nodes.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If neither `node_ids` nor `filters` is provided.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-bigquery/llama_index/vector_stores/bigquery/base.py`  
| 
```
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
```
 | 
```
defget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> List[BaseNode]:
"""
    Retrieve nodes from BigQuery using node IDs, metadata filters, or both.

    If both `node_ids` and `filters` are provided, only nodes that satisfy
    both conditions will be returned.

    Args:
        node_ids: Optional list of node IDs for retrieval.
        filters : Optional MetadataFilters filters for retrieval.

    Returns:
        A list of matching nodes.

    Raises:
        ValueError: If neither `node_ids` nor `filters` is provided.

    """
    if not (node_ids or filters):
        raise ValueError(
            "get_nodes requires at least one filtering parameter: "
            "'node_ids', 'filters', or both. Received neither."
        )

    where_clause, query_params = build_where_clause_and_params(node_ids, filters)

    query = f"""
    SELECT  node_id,
            text,
            embedding,
            metadata
    FROM    `{self._full_table_id}`
    WHERE   {where_clause};
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=query_params,
    )
    rows: bigquery.table.RowIterator = self._client.query_and_wait(
        query, job_config=job_config
    )

    nodes: List[BaseNode] = []
    for record in rows:
        row = _BigQueryRow(
            node_id=record.node_id,
            text=record.text,
            metadata=record.metadata,
            embedding=record.embedding,
            distance=record.distance,
        )
        node = self._bigquery_row_to_node(row)

        nodes.append(node)

    return nodes

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/bigquery/#llama_index.vector_stores.bigquery.BigQueryVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Delete nodes from BigQuery based on node IDs, metadata filters, or both.
If both `node_ids` and `filters` are provided, only nodes matching both criteria will be deleted.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `Optional[List[str]]`  |  Optional list of node IDs to delete.  |  `None`  |  
|  `filters `  |  Optional MetadataFilters filters for deletion.  |  _required_  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If neither `node_ids` nor `filters` are provided.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-bigquery/llama_index/vector_stores/bigquery/base.py`  
| 
```
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
    Delete nodes from BigQuery based on node IDs, metadata filters, or both.

    If both `node_ids` and `filters` are provided, only nodes matching both
    criteria will be deleted.

    Args:
        node_ids: Optional list of node IDs to delete.
        filters : Optional MetadataFilters filters for deletion.

    Raises:
        ValueError: If neither `node_ids` nor `filters` are provided.

    """
    if not (node_ids or filters):
        raise ValueError(
            "delete_nodes requires at least one filtering parameter: "
            "'node_ids', 'filters', or both. Received neither."
        )

    where_clause, query_params = build_where_clause_and_params(node_ids, filters)

    query = f"""
    DELETE FROM `{self._full_table_id}`
    WHERE {where_clause};
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=query_params,
    )
    self._client.query_and_wait(query, job_config=job_config)

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/bigquery/#llama_index.vector_stores.bigquery.BigQueryVectorStore.clear "Permanent link")

```
clear() -> None

```

Clears the index.
This truncates the underlying table in BigQuery.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-bigquery/llama_index/vector_stores/bigquery/base.py`  
| 
```
540
541
542
543
544
545
546
547
```
 | 
```
defclear(self) -> None:
"""
    Clears the index.

    This truncates the underlying table in BigQuery.
    """
    query = f"""TRUNCATE TABLE `{self._full_table_id}`;"""
    self._client.query_and_wait(query)

```
 |  
| --- | --- |  
options: members: - BigQueryVectorStore
