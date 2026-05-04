# ApertureDB
##  ApertureDBVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/ApertureDB/#llama_index.vector_stores.ApertureDB.ApertureDBVectorStore "Permanent link")
Bases: 
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-ApertureDB/llama_index/vector_stores/ApertureDB/base.py`  
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
```
 | 
```
classApertureDBVectorStore(BasePydanticVectorStore):
    stores_text: bool = True
    flat_metadata: bool = True
    logger: logging.Logger = logging.getLogger(__name__)

    _client = PrivateAttr()
    _execute_query = PrivateAttr()

"""
    ApertureDB vectorstore.

    This VectorStore uses DescriptorSet to store the embeddings and metadata.

    Query is run with FindDescriptor to find k most similar embeddings.

    Args:
        embeddings (Embeddings): Embedding function.

        descriptor_set (str, optional): Descriptor set name. Defaults to "llamaindex".

        dimensions (Optional[int], optional):   Number of dimensions of the embeddings.
            Defaults to None.

        engine (str, optional): Engine to use.
            Defaults to "HNSW" for new descriptorsets.

        metric (str, optional): Metric to use. Defaults to "CS" for new descriptorsets.

        log_level (int, optional): Logging level. Defaults to logging.WARN.
        overwrite (bool, optional): Default set to True. Will overwrite existing descriptor set.
    Example:

        ```python
            # Get the data for running the example
            # mkdir -p 'data/paul_graham/'
            # wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'

            from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
            from llama_index.core import StorageContext
            from llama_index.vector_stores.ApertureDB import ApertureDBVectorStore

            adb_client = ApertureDBVectorStore(dimensions=1536)
            storage_context = StorageContext.from_defaults(vector_store=adb_client)


            documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
            index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

            query_engine = index.as_query_engine()

            def run_queries(query_engine):
                query_str = [
                    "What did the author do growing up?",
                    "What did the author do after his time at Viaweb?"

                for qs in query_str:
                    response = query_engine.query(qs)
                    print(f"{qs=}\r\n")
                    print(response)

            run_queries(query_engine)

            # Delete the first document from the index.
            # This particular example folder has just 1 document.
            # Deleting it would cause the queries to return empty results.
            index.delete(documents[0].doc_id)

            run_queries(query_engine)
    """

    @override
    def__init__(
        self,
        descriptor_set: str = DESCRIPTOR_SET,
        embeddings: Any = None,
        dimensions: Optional[int] = None,
        engine: Optional[str] = None,
        metric: Optional[str] = None,
        log_level: int = logging.WARN,
        properties: Optional[Dict] = None,
        overwrite: bool = True,
        **kwargs: Any,
    ) -> None:
        # ApertureDB imports
        try:
            fromaperturedb.Utilsimport Utils
            fromaperturedb.CommonLibraryimport create_connector, execute_query
            fromaperturedb.Descriptorsimport Descriptors

        except ImportError:
            raise ImportError(
                "ApertureDB is not installed. Please install it using "
                "'pip install --upgrade aperturedb'"
            )

        super().__init__(**kwargs)

        self.logger.setLevel(log_level)
        self._descriptor_set = descriptor_set
        self._dimensions = dimensions
        self._engine = engine
        self._metric = metric
        self._properties = properties
        self._overwrite = overwrite
        # TODO: Either standardize this or remove it.
        self._embedding_function = embeddings

        ## Returns a client for the database
        self._client = create_connector()
        self._descriptors = Descriptors(self._client)
        self._execute_query = execute_query
        self._utils = Utils(self._client)

        try:
            self._utils.status()
        except Exception:
            self.logger.exception("Failed to connect to ApertureDB")
            raise

        self._find_or_add_descriptor_set()  ## Call to find or add a descriptor set

    @classmethod
    defclass_name(cls) -> str:
        return "ApertureDBVectorStore"

    @property
    defclient(self) -> Any:
"""Get client."""
        return self._client

    def_find_or_add_descriptor_set(self) -> None:
"""
        Checks if the descriptor set exists, if not, creates it.
        """
        descriptor_set = self._descriptor_set
        find_ds_query = [
            {
                "FindDescriptorSet": {
                    "with_name": descriptor_set,
                    "engines": True,
                    "metrics": True,
                    "dimensions": True,
                    "results": {"all_properties": True},
                }
            }
        ]
        _, response, _ = self._execute_query(
            client=self._client, query=find_ds_query, blobs=[]
        )
        n_entities = (
            len(response[0]["FindDescriptorSet"]["entities"])
            if "entities" in response[0]["FindDescriptorSet"]
            else 0
        )
        assert n_entities <= 1, "Multiple descriptor sets with the same name"

        if n_entities == 1:  # Descriptor set exists already
            e = response[0]["FindDescriptorSet"]["entities"][0]
            self.logger.info(f"Descriptor set {descriptor_set} already exists")

            engines = e["_engines"]
            assert len(engines) == 1, "Only one engine is supported"

            if self._engine is None:
                self._engine = engines[0]
            elif self._engine != engines[0]:
                self.logger.error(f"Engine mismatch: {self._engine} != {engines[0]}")

            metrics = e["_metrics"]
            assert len(metrics) == 1, "Only one metric is supported"
            if self._metric is None:
                self._metric = metrics[0]
            elif self._metric != metrics[0]:
                self.logger.error(f"Metric mismatch: {self._metric} != {metrics[0]}")

            dimensions = e["_dimensions"]
            if self._dimensions is None:
                self._dimensions = dimensions
            elif self._dimensions != dimensions:
                self.logger.error(
                    f"Dimensions mismatch: {self._dimensions} != {dimensions}"
                )

            self._properties = {
                k[len(PROPERTY_PREFIX) :]: v
                for k, v in e.items()
                if k.startswith(PROPERTY_PREFIX)
            }

        else:
            self.logger.info(
                f"Descriptor set {descriptor_set} does not exist. Creating it"
            )
            if self._engine is None:
                self._engine = ENGINE
            if self._metric is None:
                self._metric = METRIC
            if self._dimensions is None:
                assert self._embedding_function is not None, (
                    "Dimensions or embedding function must be provided"
                )
                self._dimensions = len(
                    self._embedding_function.get_text_embedding("test")
                )

            properties = (
                {PROPERTY_PREFIX + k: v for k, v in self._properties.items()}
                if self._properties is not None
                else None
            )

            self._utils.add_descriptorset(
                name=descriptor_set,
                dim=self._dimensions,
                engine=self._engine,
                metric=self._metric,
                properties=properties,
            )

            # Create indexes
            self._utils.create_entity_index("_Descriptor", "_create_txn")
            self._utils.create_entity_index("_DescriptorSet", "_name")
            self._utils.create_entity_index("_Descriptor", UNIQUEID_PROPERTY)

    defadd(
        self,
        nodes: List[TextNode],
        **kwargs: Any,
    ) -> List[str]:
"""
        Adds a list of nodes as Descriptors to the Descriptorset.

        Args:
            nodes: List[TextNode] List of text nodes
            kwargs: Additional arguments to pass to add

        """
        ids = []
        data = []

        for node in nodes:
            metadata = node_to_metadata_dict(
                node, remove_text=False, flat_metadata=self.flat_metadata
            )

            properties = {
                UNIQUEID_PROPERTY: node.node_id,
                "text": node.get_content(metadata_mode=MetadataMode.NONE) or "",
                "metadata": json.dumps(metadata),
            }
            for k, v in metadata.items():
                properties[PROPERTY_PREFIX + k] = v

            command = {
                "AddDescriptor": {
                    "set": self._descriptor_set,
                    "properties": properties,  ## Can add arbitrary key value pairs here.
                    "if_not_found": {UNIQUEID_PROPERTY: ["==", node.node_id]},
                }
            }

            query = [command]
            blobs = [
                np.array(node.embedding, dtype=np.float32).tobytes()
            ]  ## And convert the already calculated embeddings into blobs here
            data.append((query, blobs))
            ids.append(node.node_id)

        loader = ParallelLoader(self._client)
        loader.ingest(data, batchsize=BATCHSIZE)

        return ids

    defdelete_vector_store(self, descriptor_set_name: str) -> None:
"""
        Delete a descriptor set from ApertureDB.

        Args:
            descriptor_set_name: The name of the descriptor set to delete.

        """
        self._utils.remove_descriptorset(descriptor_set_name)

    defget_descriptor_set(self) -> List[str]:
"""
        Return a list of existing descriptor sets in ApertureDB.
        """
        return self._utils.get_descriptorset_list()

    defquery(self, query: VectorStoreQuery) -> VectorStoreQueryResult:
"""
        Return nodes as response.
        """

        defconvert_filters_to_constraints(query_filters: MetadataFilters) -> Dict:
            if query_filters is None:
                return None
            constraints = Constraints()
            for filter in query_filters.filters:
                key = f"{PROPERTY_PREFIX}{filter.key}"
                if filter.operator == FilterOperator.EQ:
                    constraints = constraints.equal(
                        key,
                        filter.value,
                    )
                elif filter.operator == FilterOperator.GT:
                    constraints = constraints.greater(
                        key,
                        filter.value,
                    )
                elif filter.operator == FilterOperator.LT:
                    constraints = constraints.less(
                        key,
                        filter.value,
                    )
                elif filter.operator == FilterOperator.GTE:
                    constraints = constraints.greaterequal(
                        key,
                        filter.value,
                    )
                elif filter.operator == FilterOperator.LTE:
                    constraints = constraints.lessequal(
                        key,
                        filter.value,
                    )
                else:
                    raise ValueError(f"Unsupported mode: {filter.mode}")
            return constraints

        constraints = convert_filters_to_constraints(query.filters)
        ## VectorStoreQuery has query_embedding, similarity_top_k and mode
        self._descriptors.find_similar(
            set=self._descriptor_set,
            constraints=constraints,
            vector=query.query_embedding,
            k_neighbors=query.similarity_top_k,
            distances=True,
        )

        nodes = []
        ids: List[str] = []
        similarities: List[float] = []

        for d in self._descriptors:
            metadata = json.loads(d["metadata"])
            node = metadata_dict_to_node(metadata)

            text = d.get("text")

            node.set_content(text)

            nodes.append(node)
            ids.append(d.get("id"))
            similarities.append(d["_distance"])

        return VectorStoreQueryResult(nodes=nodes, ids=ids, similarities=similarities)

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete embeddings (if present) from the vectorstore confined the given ref_doc_id.
        They should additionally be confined to the descriptor set in use.

        Args:
            ref_doc_id: The document ID to delete.
            delete_kwargs: Additional arguments to pass to delete

        Returns:
            None

        """
        ref_property_key_name = "ref_doc_id"
        query = [
            {
                "DeleteDescriptor": {
                    "constraints": {
                        PROPERTY_PREFIX + ref_property_key_name: ["==", ref_doc_id]
                    },
                    "set": self._descriptor_set,
                }
            }
        ]

        result, _ = self._utils.execute(query)
        assert len(result) == 1, f"Failed to delete descriptor {result=}"
        assert result[0]["DeleteDescriptor"]["status"] == 0, (
            f"Failed to delete descriptor {result=}"
        )

    defclear(self) -> None:
"""
        Delete all descriptors in the specified descriptor set.
        """
        query = [
            {
                "DeleteDescriptor": {
                    "set": self._descriptor_set,
                }
            }
        ]

        result, _ = self._utils.execute(query)
        assert len(result) == 1, f"Failed to delete descriptor {result=}"
        assert result[0]["DeleteDescriptor"]["status"] == 0, (
            f"Failed to delete descriptor {result=}"
        )

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> List[str]:
"""Delete nodes from vector store."""
        return super().delete_nodes(node_ids, filters, **delete_kwargs)

    defget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> List[TextNode]:
"""Get nodes from vector store."""
        return super().get_nodes(node_ids, filters)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/ApertureDB/#llama_index.vector_stores.ApertureDB.ApertureDBVectorStore.client "Permanent link")

```
client: 

```

Get client.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/ApertureDB/#llama_index.vector_stores.ApertureDB.ApertureDBVectorStore.add "Permanent link")

```
add(nodes: [], **kwargs: ) -> []

```

Adds a list of nodes as Descriptors to the Descriptorset.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[TextNode] List of text nodes  |  _required_  |  
|  `kwargs`  |  Additional arguments to pass to add  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-ApertureDB/llama_index/vector_stores/ApertureDB/base.py`  
| 
```
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
```
 | 
```
defadd(
    self,
    nodes: List[TextNode],
    **kwargs: Any,
) -> List[str]:
"""
    Adds a list of nodes as Descriptors to the Descriptorset.

    Args:
        nodes: List[TextNode] List of text nodes
        kwargs: Additional arguments to pass to add

    """
    ids = []
    data = []

    for node in nodes:
        metadata = node_to_metadata_dict(
            node, remove_text=False, flat_metadata=self.flat_metadata
        )

        properties = {
            UNIQUEID_PROPERTY: node.node_id,
            "text": node.get_content(metadata_mode=MetadataMode.NONE) or "",
            "metadata": json.dumps(metadata),
        }
        for k, v in metadata.items():
            properties[PROPERTY_PREFIX + k] = v

        command = {
            "AddDescriptor": {
                "set": self._descriptor_set,
                "properties": properties,  ## Can add arbitrary key value pairs here.
                "if_not_found": {UNIQUEID_PROPERTY: ["==", node.node_id]},
            }
        }

        query = [command]
        blobs = [
            np.array(node.embedding, dtype=np.float32).tobytes()
        ]  ## And convert the already calculated embeddings into blobs here
        data.append((query, blobs))
        ids.append(node.node_id)

    loader = ParallelLoader(self._client)
    loader.ingest(data, batchsize=BATCHSIZE)

    return ids

```
 |  
| --- | --- |  
###  delete_vector_store [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/ApertureDB/#llama_index.vector_stores.ApertureDB.ApertureDBVectorStore.delete_vector_store "Permanent link")

```
delete_vector_store(descriptor_set_name: ) -> None

```

Delete a descriptor set from ApertureDB.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `descriptor_set_name`  |  The name of the descriptor set to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-ApertureDB/llama_index/vector_stores/ApertureDB/base.py`  
| 
```
323
324
325
326
327
328
329
330
331
```
 | 
```
defdelete_vector_store(self, descriptor_set_name: str) -> None:
"""
    Delete a descriptor set from ApertureDB.

    Args:
        descriptor_set_name: The name of the descriptor set to delete.

    """
    self._utils.remove_descriptorset(descriptor_set_name)

```
 |  
| --- | --- |  
###  get_descriptor_set [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/ApertureDB/#llama_index.vector_stores.ApertureDB.ApertureDBVectorStore.get_descriptor_set "Permanent link")

```
get_descriptor_set() -> []

```

Return a list of existing descriptor sets in ApertureDB.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-ApertureDB/llama_index/vector_stores/ApertureDB/base.py`  
| 
```
333
334
335
336
337
```
 | 
```
defget_descriptor_set(self) -> List[str]:
"""
    Return a list of existing descriptor sets in ApertureDB.
    """
    return self._utils.get_descriptorset_list()

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/ApertureDB/#llama_index.vector_stores.ApertureDB.ApertureDBVectorStore.query "Permanent link")

```
query(query: ) -> 

```

Return nodes as response.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-ApertureDB/llama_index/vector_stores/ApertureDB/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery) -> VectorStoreQueryResult:
"""
    Return nodes as response.
    """

    defconvert_filters_to_constraints(query_filters: MetadataFilters) -> Dict:
        if query_filters is None:
            return None
        constraints = Constraints()
        for filter in query_filters.filters:
            key = f"{PROPERTY_PREFIX}{filter.key}"
            if filter.operator == FilterOperator.EQ:
                constraints = constraints.equal(
                    key,
                    filter.value,
                )
            elif filter.operator == FilterOperator.GT:
                constraints = constraints.greater(
                    key,
                    filter.value,
                )
            elif filter.operator == FilterOperator.LT:
                constraints = constraints.less(
                    key,
                    filter.value,
                )
            elif filter.operator == FilterOperator.GTE:
                constraints = constraints.greaterequal(
                    key,
                    filter.value,
                )
            elif filter.operator == FilterOperator.LTE:
                constraints = constraints.lessequal(
                    key,
                    filter.value,
                )
            else:
                raise ValueError(f"Unsupported mode: {filter.mode}")
        return constraints

    constraints = convert_filters_to_constraints(query.filters)
    ## VectorStoreQuery has query_embedding, similarity_top_k and mode
    self._descriptors.find_similar(
        set=self._descriptor_set,
        constraints=constraints,
        vector=query.query_embedding,
        k_neighbors=query.similarity_top_k,
        distances=True,
    )

    nodes = []
    ids: List[str] = []
    similarities: List[float] = []

    for d in self._descriptors:
        metadata = json.loads(d["metadata"])
        node = metadata_dict_to_node(metadata)

        text = d.get("text")

        node.set_content(text)

        nodes.append(node)
        ids.append(d.get("id"))
        similarities.append(d["_distance"])

    return VectorStoreQueryResult(nodes=nodes, ids=ids, similarities=similarities)

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/ApertureDB/#llama_index.vector_stores.ApertureDB.ApertureDBVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete embeddings (if present) from the vectorstore confined the given ref_doc_id. They should additionally be confined to the descriptor set in use.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The document ID to delete.  |  _required_  |  
|  `delete_kwargs`  |  Additional arguments to pass to delete  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `None`  |  None  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-ApertureDB/llama_index/vector_stores/ApertureDB/base.py`  
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete embeddings (if present) from the vectorstore confined the given ref_doc_id.
    They should additionally be confined to the descriptor set in use.

    Args:
        ref_doc_id: The document ID to delete.
        delete_kwargs: Additional arguments to pass to delete

    Returns:
        None

    """
    ref_property_key_name = "ref_doc_id"
    query = [
        {
            "DeleteDescriptor": {
                "constraints": {
                    PROPERTY_PREFIX + ref_property_key_name: ["==", ref_doc_id]
                },
                "set": self._descriptor_set,
            }
        }
    ]

    result, _ = self._utils.execute(query)
    assert len(result) == 1, f"Failed to delete descriptor {result=}"
    assert result[0]["DeleteDescriptor"]["status"] == 0, (
        f"Failed to delete descriptor {result=}"
    )

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/ApertureDB/#llama_index.vector_stores.ApertureDB.ApertureDBVectorStore.clear "Permanent link")

```
clear() -> None

```

Delete all descriptors in the specified descriptor set.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-ApertureDB/llama_index/vector_stores/ApertureDB/base.py`  
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
```
 | 
```
defclear(self) -> None:
"""
    Delete all descriptors in the specified descriptor set.
    """
    query = [
        {
            "DeleteDescriptor": {
                "set": self._descriptor_set,
            }
        }
    ]

    result, _ = self._utils.execute(query)
    assert len(result) == 1, f"Failed to delete descriptor {result=}"
    assert result[0]["DeleteDescriptor"]["status"] == 0, (
        f"Failed to delete descriptor {result=}"
    )

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/ApertureDB/#llama_index.vector_stores.ApertureDB.ApertureDBVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> []

```

Delete nodes from vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-ApertureDB/llama_index/vector_stores/ApertureDB/base.py`  
| 
```
456
457
458
459
460
461
462
463
```
 | 
```
defdelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> List[str]:
"""Delete nodes from vector store."""
    return super().delete_nodes(node_ids, filters, **delete_kwargs)

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/ApertureDB/#llama_index.vector_stores.ApertureDB.ApertureDBVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Get nodes from vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-ApertureDB/llama_index/vector_stores/ApertureDB/base.py`  
| 
```
465
466
467
468
469
470
471
```
 | 
```
defget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> List[TextNode]:
"""Get nodes from vector store."""
    return super().get_nodes(node_ids, filters)

```
 |  
| --- | --- |  
options: members: - ApertureDBVectorStore
