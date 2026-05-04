# Moorcheh
##  MoorchehVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/moorcheh/#llama_index.vector_stores.moorcheh.MoorchehVectorStore "Permanent link")
Bases: 
Moorcheh Vector Store.
In this vector store, embeddings and docs are stored within a Moorcheh namespace. During query time, the index uses Moorcheh to query for the top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  `Optional[str]`  |  API key for Moorcheh. If not provided, will look for MOORCHEH_API_KEY environment variable.  |  `None`  |  
|  `namespace`  |  Namespace name to use for this vector store.  |  `None`  |  
|  `namespace_type`  |  Type of namespace - "text" or "vector".  |  `'text'`  |  
|  `vector_dimension`  |  `Optional[int]`  |  Vector dimension for vector namespace.  |  `None`  |  
|  `batch_size`  |  Batch size for adding nodes. Defaults to DEFAULT_EMBED_BATCH_SIZE.  |  
|  `**kwargs`  |  Additional arguments to pass to MoorchehClient.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-moorcheh/llama_index/vector_stores/moorcheh/base.py`  
| 
```
 31
 32
 33
 34
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
```
 | 
```
classMoorchehVectorStore(BasePydanticVectorStore):
"""
    Moorcheh Vector Store.

    In this vector store, embeddings and docs are stored within a Moorcheh namespace.
    During query time, the index uses Moorcheh to query for the top k most similar nodes.

    Args:
        api_key (Optional[str]): API key for Moorcheh.
            If not provided, will look for MOORCHEH_API_KEY environment variable.
        namespace (str): Namespace name to use for this vector store.
        namespace_type (str): Type of namespace - "text" or "vector".
        vector_dimension (Optional[int]): Vector dimension for vector namespace.
        batch_size (int): Batch size for adding nodes. Defaults to DEFAULT_EMBED_BATCH_SIZE.
        **kwargs: Additional arguments to pass to MoorchehClient.

    """

    # Default values and capabilities
    DEFAULT_NAMESPACE: ClassVar[str] = "llamaindex_default"
    DEFAULT_EMBED_BATCH_SIZE: ClassVar[int] = 64  # customize as needed

    stores_text: bool = True
    flat_metadata: bool = True

    api_key: Optional[str]
    namespace: Optional[str]
    namespace_type: Optional[Literal["text", "vector"]] = None
    vector_dimension: Optional[int]
    add_sparse_vector: Optional[bool]
    ai_model: Optional[str]
    batch_size: int
    sparse_embedding_model: Optional[BaseSparseEmbedding] = None

    def__init__(
        self,
        api_key: Optional[str] = None,
        namespace: Optional[str] = None,
        namespace_type: Optional[str] = "text",
        vector_dimension: Optional[int] = None,
        add_sparse_vector: Optional[bool] = False,
        tokenizer: Optional[Callable] = None,
        ai_model: Optional[str] = "anthropic.claude-3-7-sonnet-20250219-v1:0",
        batch_size: int = 64,
        sparse_embedding_model: Optional[BaseSparseEmbedding] = None,
    ) -> None:
        # Initialize store attributes
        if add_sparse_vector:
            if sparse_embedding_model is not None:
                sparse_embedding_model = sparse_embedding_model
            elif tokenizer is not None:
                sparse_embedding_model = DefaultMoorchehSparseEmbedding(
                    tokenizer=tokenizer
                )
            else:
                sparse_embedding_model = DefaultMoorchehSparseEmbedding()
        else:
            sparse_embedding_model = None

        super().__init__(
            api_key=api_key,
            namespace=namespace,
            namespace_type=namespace_type,
            vector_dimension=vector_dimension,
            add_sparse_vector=add_sparse_vector,
            batch_size=batch_size,
            sparse_embedding_model=sparse_embedding_model,
            ai_model=ai_model,
        )

        # Fallback to env var if API key not provided
        if not self.api_key:
            self.api_key = os.getenv("MOORCHEH_API_KEY")
        if not self.api_key:
            raise ValueError("`api_key` is required for Moorcheh client initialization")

        if not self.namespace:
            raise ValueError(
                "`namespace` is required for Moorcheh client initialization"
            )

        # Initialize Moorcheh client
        logger.debug("Initializing MoorchehClient")
        self._client = MoorchehClient(api_key=self.api_key)
        self.is_embedding_query = False
        self._sparse_embedding_model = sparse_embedding_model
        self.namespace = namespace

        logger.debug("Listing namespaces...")
        try:
            namespaces_response = self._client.list_namespaces()
            namespaces = [
                namespace["namespace_name"]
                for namespace in namespaces_response.get("namespaces", [])
            ]
            logger.debug("Found namespaces.")
        except Exception as e:
            logger.debug("Failed to list namespaces: {e}")
            raise

        # Check if the namespace exists
        if self.namespace in namespaces:
            logger.debug(
                "Namespace '{self.namespace}' already exists. No action required."
            )
        else:
            logger.debug("Namespace '{self.namespace}' not found. Creating it.")
            # If the namespace doesn't exist, create it
            try:
                self._client.create_namespace(
                    namespace_name=self.namespace,
                    type=self.namespace_type,
                    vector_dimension=self.vector_dimension,
                )
                logger.debug("Namespace '{self.namespace}' created.")
            except Exception as e:
                logger.debug("Failed to create namespace: {e}")
                raise

    # _client: MoorchehClient = PrivateAttr()

    @property
    defclient(self) -> MoorchehClient:
"""Return initialized Moorcheh client."""
        return self._client

    @classmethod
    defclass_name(cls) -> str:
"""Return class name."""
        return "MoorchehVectorStore"

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""Add nodes to Moorcheh."""
        if not nodes:
            return []

        if self.namespace_type == "text":
            return self._add_text_nodes(nodes, **add_kwargs)
        else:
            return self._add_vector_nodes(nodes, **add_kwargs)

    def_add_text_nodes(self, nodes: List[BaseNode], **kwargs: Any) -> List[str]:
"""Add text documents to a text namespace."""
        documents = []
        ids = []
        sparse_inputs = []

        for node in nodes:
            node_id = node.node_id or str(uuid.uuid4())
            ids.append(node_id)

            document = {
                "id": node_id,
                "text": node.get_content(metadata_mode=MetadataMode.NONE),
            }

            # Add metadata if present
            if node.metadata:
                document["metadata"] = node.metadata

            if self.add_sparse_vector and self._sparse_embedding_model is not None:
                sparse_inputs.append(node.get_content(metadata_mode=MetadataMode.EMBED))

            documents.append(document)

            if sparse_inputs:
                sparse_vectors = self._sparse_embedding_model.get_text_embedding_batch(
                    sparse_inputs
                )
                for i, sparse_vector in enumerate(sparse_vectors):
                    documents[i][SPARSE_VECTOR_KEY] = {
                        "indices": list(sparse_vector.keys()),
                        "values": list(sparse_vector.values()),
                    }

        # Process in batches
        for i in range(0, len(documents), self.batch_size):
            batch = documents[i : i + self.batch_size]
            try:
                result = self._client.upload_documents(
                    namespace_name=self.namespace, documents=batch
                )
                logger.debug(f"Uploaded batch of {len(batch)} documents")
            except MoorchehError as e:
                logger.error(f"Error uploading documents batch: {e}")
                raise

        logger.info(
            f"Added {len(documents)} text documents to namespace {self.namespace}"
        )
        return ids

    def_add_vector_nodes(self, nodes: List[BaseNode], **kwargs: Any) -> List[str]:
"""Add vector nodes to vector namespace."""
        vectors = []
        ids = []
        sparse_inputs = []

        if all(node.embedding is None for node in nodes):
            raise ValueError("No embeddings could be found within your nodes")
        for node in nodes:
            if node.embedding is None:
                warnings.warn(
                    f"Node {node.node_id} has no embedding for vector namespace",
                    UserWarning,
                )

            node_id = node.node_id or str(uuid.uuid4())
            ids.append(node_id)

            vector = {
                "id": node_id,
                "vector": node.embedding,
            }

            # Add metadata, including text content
            metadata = dict(node.metadata) if node.metadata else {}
            metadata["text"] = metadata.pop(
                "text", node.get_content(metadata_mode=MetadataMode.NONE)
            )
            vector["metadata"] = metadata

            if self.add_sparse_vector and self._sparse_embedding_model is not None:
                sparse_inputs.append(node.get_content(metadata_mode=MetadataMode.EMBED))

            vectors.append(vector)

            if sparse_inputs:
                sparse_vectors = self._sparse_embedding_model.get_text_embedding_batch(
                    sparse_inputs
                )
                for i, sparse_vector in enumerate(sparse_vectors):
                    documents[i][SPARSE_VECTOR_KEY] = {
                        "indices": list(sparse_vector.keys()),
                        "values": list(sparse_vector.values()),
                    }
        # Process in batches
        for i in range(0, len(vectors), self.batch_size):
            batch = vectors[i : i + self.batch_size]
            try:
                result = self._client.upload_vectors(
                    namespace_name=self.namespace, vectors=batch
                )
                logger.debug(f"Uploaded batch of {len(batch)} vectors")
            except MoorchehError as e:
                logger.error(f"Error uploading vectors batch: {e}")
                raise

        logger.info(f"Added {len(vectors)} vectors to namespace {self.namespace}")
        return ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        try:
            if self.namespace_type == "text":
                result = self._client.delete_documents(
                    namespace_name=self.namespace, ids=[ref_doc_id]
                )
            else:
                result = self._client.delete_vectors(
                    namespace_name=self.namespace, ids=[ref_doc_id]
                )
            logger.info(
                f"Deleted document {ref_doc_id} from namespace {self.namespace}"
            )
        except MoorchehError as e:
            logger.error(f"Error deleting document {ref_doc_id}: {e}")
            raise

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query Moorcheh vector store.

        Args:
            query (VectorStoreQuery): query object

        Returns:
            VectorStoreQueryResult: query result

        """
        moorcheh_sparse_vector = None
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
                moorcheh_sparse_vector = {
                    "indices": list(sparse_vector.keys()),
                    "values": [v * (1 - query.alpha) for v in sparse_vector.values()],
                }
            else:
                moorcheh_sparse_vector = {
                    "indices": list(sparse_vector.keys()),
                    "values": list(sparse_vector.values()),
                }
"""
        if query.mode != VectorStoreQueryMode.DEFAULT:
            logger.warning(
                f"Moorcheh does not support query mode {query.mode}. "
                "Using default mode instead."

        """

        # Prepare search parameters
        search_kwargs = {
            "namespaces": [self.namespace],
            "top_k": query.similarity_top_k,
        }

        # Add similarity threshold if provided
        # if query.similarity_top_k is not None:
        #    search_kwargs["threshold"] = query.similarity_top_k

        # Handle query input
        if query.query_str is not None:
            search_kwargs["query"] = query.query_str
        elif query.query_embedding is not None:
            search_kwargs["query"] = query.query_embedding
        else:
            raise ValueError("Either query_str or query_embedding must be provided")

        # TODO: Add metadata filter support when available in Moorcheh SDK
        if query.filters is not None:
            logger.warning(
                "Metadata filters are not yet supported by Moorcheh integration"
            )

        try:
            # Execute search
            search_result = self._client.search(**search_kwargs)

            # Parse results
            nodes = []
            similarities = []
            ids = []

            results = search_result.get("results", [])
            for result in results:
                node_id = result.get("id")
                score = result.get("score", 0.0)

                if node_id is None:
                    logger.warning("Found result with no ID, skipping")
                    continue

                ids.append(node_id)
                similarities.append(score)

                # Extract text and metadata
                if self.namespace_type == "text":
                    text = result.get("text", "")
                    metadata = result.get("metadata", {})
                else:
                    # For vector namespace, text is stored in metadata
                    metadata = result.get("metadata", {})
                    text = metadata.pop("text", "")  # Remove text from metadata

                # Create node
                node = TextNode(
                    text=text,
                    id_=node_id,
                    metadata=metadata,
                )
                nodes.append(node)

            return VectorStoreQueryResult(
                nodes=nodes,
                similarities=similarities,
                ids=ids,
            )

        except MoorchehError as e:
            logger.error(f"Error executing query: {e}")
            raise

    defget_generative_answer(
        self,
        query: str,
        top_k: int = 5,
        ai_model: str = "anthropic.claude-3-7-sonnet-20250219-v1:0",
        llm: Optional[LLM] = None,
        **kwargs: Any,
    ) -> str:
"""
        Get a generative AI answer using Moorcheh's built-in RAG capability.

        This method leverages Moorcheh's information-theoretic approach
        to provide context-aware answers directly from the API.

        Args:
            query (str): The query string.
            top_k (int): Number of top results to use for context.
            **kwargs: Additional keyword arguments passed to Moorcheh.

        Returns:
            str: Generated answer string.

        """
        try:
            # incorporate llama_index llms
            if llm:
                vs_query = VectorStoreQuery(query_str=query, similarity_top_k=top_k)
                result = self.query(vs_query)
                context = "\n\n".join([node.text for node in result.nodes])
                prompt = f"""Use the context below to answer the question. Context:  {context} Question: {query} Answer:"""
                return llm.complete(prompt).text
            else:
                result = self._client.get_generative_answer(
                    namespace=self.namespace,
                    query=query,
                    top_k=top_k,
                    ai_model=ai_model,
                    **kwargs,
                )
                return result.get("answer", "")
        except MoorchehError as e:
            logger.error(f"Error getting generative answer: {e}")
            raise

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/moorcheh/#llama_index.vector_stores.moorcheh.MoorchehVectorStore.client "Permanent link")

```
client: MoorchehClient

```

Return initialized Moorcheh client.
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/moorcheh/#llama_index.vector_stores.moorcheh.MoorchehVectorStore.class_name "Permanent link")

```
class_name() -> 

```

Return class name.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-moorcheh/llama_index/vector_stores/moorcheh/base.py`  
| 
```
157
158
159
160
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Return class name."""
    return "MoorchehVectorStore"

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/moorcheh/#llama_index.vector_stores.moorcheh.MoorchehVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to Moorcheh.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-moorcheh/llama_index/vector_stores/moorcheh/base.py`  
| 
```
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
```
 | 
```
defadd(
    self,
    nodes: List[BaseNode],
    **add_kwargs: Any,
) -> List[str]:
"""Add nodes to Moorcheh."""
    if not nodes:
        return []

    if self.namespace_type == "text":
        return self._add_text_nodes(nodes, **add_kwargs)
    else:
        return self._add_vector_nodes(nodes, **add_kwargs)

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/moorcheh/#llama_index.vector_stores.moorcheh.MoorchehVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-moorcheh/llama_index/vector_stores/moorcheh/base.py`  
| 
```
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
        if self.namespace_type == "text":
            result = self._client.delete_documents(
                namespace_name=self.namespace, ids=[ref_doc_id]
            )
        else:
            result = self._client.delete_vectors(
                namespace_name=self.namespace, ids=[ref_doc_id]
            )
        logger.info(
            f"Deleted document {ref_doc_id} from namespace {self.namespace}"
        )
    except MoorchehError as e:
        logger.error(f"Error deleting document {ref_doc_id}: {e}")
        raise

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/moorcheh/#llama_index.vector_stores.moorcheh.MoorchehVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query Moorcheh vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  query object  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  query result  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-moorcheh/llama_index/vector_stores/moorcheh/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query Moorcheh vector store.

    Args:
        query (VectorStoreQuery): query object

    Returns:
        VectorStoreQueryResult: query result

    """
    moorcheh_sparse_vector = None
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
            moorcheh_sparse_vector = {
                "indices": list(sparse_vector.keys()),
                "values": [v * (1 - query.alpha) for v in sparse_vector.values()],
            }
        else:
            moorcheh_sparse_vector = {
                "indices": list(sparse_vector.keys()),
                "values": list(sparse_vector.values()),
            }
"""
    if query.mode != VectorStoreQueryMode.DEFAULT:
        logger.warning(
            f"Moorcheh does not support query mode {query.mode}. "
            "Using default mode instead."

    """

    # Prepare search parameters
    search_kwargs = {
        "namespaces": [self.namespace],
        "top_k": query.similarity_top_k,
    }

    # Add similarity threshold if provided
    # if query.similarity_top_k is not None:
    #    search_kwargs["threshold"] = query.similarity_top_k

    # Handle query input
    if query.query_str is not None:
        search_kwargs["query"] = query.query_str
    elif query.query_embedding is not None:
        search_kwargs["query"] = query.query_embedding
    else:
        raise ValueError("Either query_str or query_embedding must be provided")

    # TODO: Add metadata filter support when available in Moorcheh SDK
    if query.filters is not None:
        logger.warning(
            "Metadata filters are not yet supported by Moorcheh integration"
        )

    try:
        # Execute search
        search_result = self._client.search(**search_kwargs)

        # Parse results
        nodes = []
        similarities = []
        ids = []

        results = search_result.get("results", [])
        for result in results:
            node_id = result.get("id")
            score = result.get("score", 0.0)

            if node_id is None:
                logger.warning("Found result with no ID, skipping")
                continue

            ids.append(node_id)
            similarities.append(score)

            # Extract text and metadata
            if self.namespace_type == "text":
                text = result.get("text", "")
                metadata = result.get("metadata", {})
            else:
                # For vector namespace, text is stored in metadata
                metadata = result.get("metadata", {})
                text = metadata.pop("text", "")  # Remove text from metadata

            # Create node
            node = TextNode(
                text=text,
                id_=node_id,
                metadata=metadata,
            )
            nodes.append(node)

        return VectorStoreQueryResult(
            nodes=nodes,
            similarities=similarities,
            ids=ids,
        )

    except MoorchehError as e:
        logger.error(f"Error executing query: {e}")
        raise

```
 |  
| --- | --- |  
###  get_generative_answer [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/moorcheh/#llama_index.vector_stores.moorcheh.MoorchehVectorStore.get_generative_answer "Permanent link")

```
get_generative_answer(
    query: ,
    top_k:  = 5,
    ai_model:  = "anthropic.claude-3-7-sonnet-20250219-v1:0",
    llm: Optional[] = None,
    **kwargs: 
) -> 

```

Get a generative AI answer using Moorcheh's built-in RAG capability.
This method leverages Moorcheh's information-theoretic approach to provide context-aware answers directly from the API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The query string.  |  _required_  |  
|  `top_k`  |  Number of top results to use for context.  |  
|  `**kwargs`  |  Additional keyword arguments passed to Moorcheh.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Generated answer string.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-moorcheh/llama_index/vector_stores/moorcheh/base.py`  
| 
```
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
```
 | 
```
defget_generative_answer(
    self,
    query: str,
    top_k: int = 5,
    ai_model: str = "anthropic.claude-3-7-sonnet-20250219-v1:0",
    llm: Optional[LLM] = None,
    **kwargs: Any,
) -> str:
"""
    Get a generative AI answer using Moorcheh's built-in RAG capability.

    This method leverages Moorcheh's information-theoretic approach
    to provide context-aware answers directly from the API.

    Args:
        query (str): The query string.
        top_k (int): Number of top results to use for context.
        **kwargs: Additional keyword arguments passed to Moorcheh.

    Returns:
        str: Generated answer string.

    """
    try:
        # incorporate llama_index llms
        if llm:
            vs_query = VectorStoreQuery(query_str=query, similarity_top_k=top_k)
            result = self.query(vs_query)
            context = "\n\n".join([node.text for node in result.nodes])
            prompt = f"""Use the context below to answer the question. Context:  {context} Question: {query} Answer:"""
            return llm.complete(prompt).text
        else:
            result = self._client.get_generative_answer(
                namespace=self.namespace,
                query=query,
                top_k=top_k,
                ai_model=ai_model,
                **kwargs,
            )
            return result.get("answer", "")
    except MoorchehError as e:
        logger.error(f"Error getting generative answer: {e}")
        raise

```
 |  
| --- | --- |  
options: members: - MoorchehVectorStore
