# Vectorx
##  VectorXVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vectorx/#llama_index.vector_stores.vectorx.VectorXVectorStore "Permanent link")
Bases: 
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vectorx/llama_index/vector_stores/vectorx/base.py`  
| 
```
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
```
 | 
```
classVectorXVectorStore(BasePydanticVectorStore):
    stores_text: bool = True
    flat_metadata: bool = False

    api_token: Optional[str]
    encryption_key: Optional[str]
    index_name: Optional[str]
    space_type: Optional[str]
    dimension: Optional[int]
    insert_kwargs: Optional[Dict]
    add_sparse_vector: bool
    text_key: str
    batch_size: int
    remove_text_from_metadata: bool

    _vectorx_index: Any = PrivateAttr()

    def__init__(
        self,
        vectorx_index: Optional[Any] = None,
        api_token: Optional[str] = None,
        encryption_key: Optional[str] = None,
        index_name: Optional[str] = None,
        space_type: Optional[str] = "cosine",
        dimension: Optional[int] = None,
        insert_kwargs: Optional[Dict] = None,
        add_sparse_vector: bool = False,
        text_key: str = DEFAULT_TEXT_KEY,
        batch_size: int = DEFAULT_BATCH_SIZE,
        remove_text_from_metadata: bool = False,
        **kwargs: Any,
    ) -> None:
        insert_kwargs = insert_kwargs or {}

        super().__init__(
            index_name=index_name,
            api_token=api_token,
            encryption_key=encryption_key,
            space_type=space_type,
            dimension=dimension,
            insert_kwargs=insert_kwargs,
            add_sparse_vector=add_sparse_vector,
            text_key=text_key,
            batch_size=batch_size,
            remove_text_from_metadata=remove_text_from_metadata,
        )

        # Use existing vectorx_index or initialize a new one
        self._vectorx_index = vectorx_index or self._initialize_vectorx_index(
            api_token, encryption_key, index_name, dimension, space_type
        )

    @classmethod
    def_initialize_vectorx_index(
        cls,
        api_token: Optional[str],
        encryption_key: Optional[str],
        index_name: Optional[str],
        dimension: Optional[int] = None,
        space_type: Optional[str] = "cosine",
    ) -> Any:
"""Initialize VectorX index using the current API."""
        try:
            fromvecx.vectorximport VectorX
        except ImportError as e:
            raise ImportError(
                "Could not import `vecx` package. "
                "Please install it with `pip install vecx`."
            ) frome

        # Initialize VectorX client
        vx = VectorX(token=api_token)

        try:
            # Try to get existing index
            index = vx.get_index(name=index_name, key=encryption_key)
            _logger.info(f"Retrieved existing index: {index_name}")
            return index
        except Exception as e:
            if dimension is None:
                raise ValueError(
                    "Must provide dimension when creating a new index"
                ) frome

            # Create a new index if it doesn't exist
            _logger.info(f"Creating new index: {index_name}")
            vx.create_index(
                name=index_name,
                dimension=dimension,
                key=encryption_key,
                space_type=space_type,
            )
            return vx.get_index(name=index_name, key=encryption_key)

    @classmethod
    deffrom_params(
        cls,
        api_token: Optional[str] = None,
        encryption_key: Optional[str] = None,
        index_name: Optional[str] = None,
        dimension: Optional[int] = None,
        space_type: str = "cosine",
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> "VectorXVectorStore":
"""Create VectorXVectorStore from parameters."""
        vectorx_index = cls._initialize_vectorx_index(
            api_token, encryption_key, index_name, dimension, space_type
        )

        return cls(
            vectorx_index=vectorx_index,
            api_token=api_token,
            encryption_key=encryption_key,
            index_name=index_name,
            dimension=dimension,
            space_type=space_type,
            batch_size=batch_size,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "VectorXVectorStore"

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

        for node in nodes:
            node_id = node.node_id
            metadata = node_to_metadata_dict(node)

            # Filter values must be simple key-value pairs
            filter_data = {}
            if "file_name" in metadata:
                filter_data["file_name"] = metadata["file_name"]
            if "doc_id" in metadata:
                filter_data["doc_id"] = metadata["doc_id"]
            if "category" in metadata:
                filter_data["category"] = metadata["category"]
            if "difficulty" in metadata:
                filter_data["difficulty"] = metadata["difficulty"]
            if "language" in metadata:
                filter_data["language"] = metadata["language"]
            if "field" in metadata:
                filter_data["field"] = metadata["field"]
            if "type" in metadata:
                filter_data["type"] = metadata["type"]
            if "feature" in metadata:
                filter_data["feature"] = metadata["feature"]

            entry = {
                "id": node_id,
                "vector": node.get_embedding(),
                "meta": metadata,
                "filter": filter_data,
            }

            ids.append(node_id)
            entries.append(entry)

        # Batch insert to avoid hitting API limits
        batch_size = self.batch_size
        for i in range(0, len(entries), batch_size):
            batch = entries[i : i + batch_size]
            self._vectorx_index.upsert(batch)

        return ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The id of the document to delete.

        """
        try:
            self._vectorx_index.delete_with_filter({"doc_id": ref_doc_id})
        except Exception as e:
            _logger.error(f"Error deleting vectors for doc_id {ref_doc_id}: {e}")

    @property
    defclient(self) -> Any:
"""Return vectorX index client."""
        return self._vectorx_index

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query: VectorStoreQuery object containing query parameters

        """
        if not hasattr(self._vectorx_index, "dimension"):
            # Get dimension from index if available, otherwise try to infer from query
            try:
                dimension = self._vectorx_index.describe()["dimension"]
            except Exception:
                if query.query_embedding is not None:
                    dimension = len(query.query_embedding)
                else:
                    raise ValueError("Could not determine vector dimension")
        else:
            dimension = self._vectorx_index.dimension

        query_embedding = [0.0] * dimension  # Default empty vector
        filters = {}

        # Apply any metadata filters if provided
        if query.filters is not None:
            for filter_item in query.filters.filters:
                # Case 1: MetadataFilter object
                if (
                    hasattr(filter_item, "key")
                    and hasattr(filter_item, "value")
                    and hasattr(filter_item, "operator")
                ):
                    op_symbol = reverse_operator_map.get(filter_item.operator)
                    if not op_symbol:
                        raise ValueError(
                            f"Unsupported filter operator: {filter_item.operator}"
                        )

                    if filter_item.key not in filters:
                        filters[filter_item.key] = {}

                    filters[filter_item.key][op_symbol] = filter_item.value

                # Case 2: Raw dict, e.g. {"category": {"$eq": "programming"}}
                elif isinstance(filter_item, dict):
                    for key, op_dict in filter_item.items():
                        if isinstance(op_dict, dict):
                            for op, val in op_dict.items():
                                if key not in filters:
                                    filters[key] = {}
                                filters[key][op] = val
                else:
                    raise ValueError(f"Unsupported filter format: {filter_item}")

        _logger.info(f"Final structured filters: {filters}")

        # Use the query embedding if provided
        if query.query_embedding is not None:
            query_embedding = cast(List[float], query.query_embedding)
            if query.alpha is not None and query.mode == VectorStoreQueryMode.HYBRID:
                # Apply alpha scaling in hybrid mode
                query_embedding = [v * query.alpha for v in query_embedding]

        # Execute query
        try:
            results = self._vectorx_index.query(
                vector=query_embedding,
                top_k=query.similarity_top_k,
                filter=filters if filters else None,
                include_vectors=True,
            )
        except Exception as e:
            _logger.error(f"Error querying VectorX: {e}")
            raise

        # Process results
        nodes = []
        similarities = []
        ids = []

        for result in results:
            node_id = result["id"]
            score = result["similarity"]

            # Get metadata from result
            metadata = result.get("meta", {})

            # Create node from metadata
            if self.flat_metadata:
                node = metadata_dict_to_node(
                    metadata=metadata,
                    text=metadata.pop(self.text_key, None),
                    id_=node_id,
                )
            else:
                metadata_dict, node_info, relationships = legacy_metadata_dict_to_node(
                    metadata=metadata,
                    text_key=self.text_key,
                )

                # Create TextNode with the extracted metadata
                # Step 1: Get the JSON string from "_node_content"
                _node_content_str = metadata.get("_node_content", "{}")

                # Step 2: Convert JSON string to Python dict
                try:
                    node_content = json.loads(_node_content_str)
                except json.JSONDecodeError:
                    node_content = {}

                # Step 3: Get the text
                text = node_content.get(self.text_key, "")
                node = TextNode(
                    text=text,
                    metadata=metadata_dict,
                    relationships=relationships,
                    node_id=node_id,
                )

                # Add any node_info properties to the node
                for key, val in node_info.items():
                    if hasattr(node, key):
                        setattr(node, key, val)

            # If embedding was returned in the results, add it to the node
            if "vector" in result:
                node.embedding = result["vector"]

            nodes.append(node)
            similarities.append(score)
            ids.append(node_id)

        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vectorx/#llama_index.vector_stores.vectorx.VectorXVectorStore.client "Permanent link")

```
client: 

```

Return vectorX index client.
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vectorx/#llama_index.vector_stores.vectorx.VectorXVectorStore.from_params "Permanent link")

```
from_params(
    api_token: Optional[] = None,
    encryption_key: Optional[] = None,
    index_name: Optional[] = None,
    dimension: Optional[] = None,
    space_type:  = "cosine",
    batch_size:  = DEFAULT_BATCH_SIZE,
) -> 

```

Create VectorXVectorStore from parameters.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vectorx/llama_index/vector_stores/vectorx/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_params(
    cls,
    api_token: Optional[str] = None,
    encryption_key: Optional[str] = None,
    index_name: Optional[str] = None,
    dimension: Optional[int] = None,
    space_type: str = "cosine",
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> "VectorXVectorStore":
"""Create VectorXVectorStore from parameters."""
    vectorx_index = cls._initialize_vectorx_index(
        api_token, encryption_key, index_name, dimension, space_type
    )

    return cls(
        vectorx_index=vectorx_index,
        api_token=api_token,
        encryption_key=encryption_key,
        index_name=index_name,
        dimension=dimension,
        space_type=space_type,
        batch_size=batch_size,
    )

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vectorx/#llama_index.vector_stores.vectorx.VectorXVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vectorx/llama_index/vector_stores/vectorx/base.py`  
| 
```
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

    for node in nodes:
        node_id = node.node_id
        metadata = node_to_metadata_dict(node)

        # Filter values must be simple key-value pairs
        filter_data = {}
        if "file_name" in metadata:
            filter_data["file_name"] = metadata["file_name"]
        if "doc_id" in metadata:
            filter_data["doc_id"] = metadata["doc_id"]
        if "category" in metadata:
            filter_data["category"] = metadata["category"]
        if "difficulty" in metadata:
            filter_data["difficulty"] = metadata["difficulty"]
        if "language" in metadata:
            filter_data["language"] = metadata["language"]
        if "field" in metadata:
            filter_data["field"] = metadata["field"]
        if "type" in metadata:
            filter_data["type"] = metadata["type"]
        if "feature" in metadata:
            filter_data["feature"] = metadata["feature"]

        entry = {
            "id": node_id,
            "vector": node.get_embedding(),
            "meta": metadata,
            "filter": filter_data,
        }

        ids.append(node_id)
        entries.append(entry)

    # Batch insert to avoid hitting API limits
    batch_size = self.batch_size
    for i in range(0, len(entries), batch_size):
        batch = entries[i : i + batch_size]
        self._vectorx_index.upsert(batch)

    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vectorx/#llama_index.vector_stores.vectorx.VectorXVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vectorx/llama_index/vector_stores/vectorx/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The id of the document to delete.

    """
    try:
        self._vectorx_index.delete_with_filter({"doc_id": ref_doc_id})
    except Exception as e:
        _logger.error(f"Error deleting vectors for doc_id {ref_doc_id}: {e}")

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vectorx/#llama_index.vector_stores.vectorx.VectorXVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  VectorStoreQuery object containing query parameters  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vectorx/llama_index/vector_stores/vectorx/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query: VectorStoreQuery object containing query parameters

    """
    if not hasattr(self._vectorx_index, "dimension"):
        # Get dimension from index if available, otherwise try to infer from query
        try:
            dimension = self._vectorx_index.describe()["dimension"]
        except Exception:
            if query.query_embedding is not None:
                dimension = len(query.query_embedding)
            else:
                raise ValueError("Could not determine vector dimension")
    else:
        dimension = self._vectorx_index.dimension

    query_embedding = [0.0] * dimension  # Default empty vector
    filters = {}

    # Apply any metadata filters if provided
    if query.filters is not None:
        for filter_item in query.filters.filters:
            # Case 1: MetadataFilter object
            if (
                hasattr(filter_item, "key")
                and hasattr(filter_item, "value")
                and hasattr(filter_item, "operator")
            ):
                op_symbol = reverse_operator_map.get(filter_item.operator)
                if not op_symbol:
                    raise ValueError(
                        f"Unsupported filter operator: {filter_item.operator}"
                    )

                if filter_item.key not in filters:
                    filters[filter_item.key] = {}

                filters[filter_item.key][op_symbol] = filter_item.value

            # Case 2: Raw dict, e.g. {"category": {"$eq": "programming"}}
            elif isinstance(filter_item, dict):
                for key, op_dict in filter_item.items():
                    if isinstance(op_dict, dict):
                        for op, val in op_dict.items():
                            if key not in filters:
                                filters[key] = {}
                            filters[key][op] = val
            else:
                raise ValueError(f"Unsupported filter format: {filter_item}")

    _logger.info(f"Final structured filters: {filters}")

    # Use the query embedding if provided
    if query.query_embedding is not None:
        query_embedding = cast(List[float], query.query_embedding)
        if query.alpha is not None and query.mode == VectorStoreQueryMode.HYBRID:
            # Apply alpha scaling in hybrid mode
            query_embedding = [v * query.alpha for v in query_embedding]

    # Execute query
    try:
        results = self._vectorx_index.query(
            vector=query_embedding,
            top_k=query.similarity_top_k,
            filter=filters if filters else None,
            include_vectors=True,
        )
    except Exception as e:
        _logger.error(f"Error querying VectorX: {e}")
        raise

    # Process results
    nodes = []
    similarities = []
    ids = []

    for result in results:
        node_id = result["id"]
        score = result["similarity"]

        # Get metadata from result
        metadata = result.get("meta", {})

        # Create node from metadata
        if self.flat_metadata:
            node = metadata_dict_to_node(
                metadata=metadata,
                text=metadata.pop(self.text_key, None),
                id_=node_id,
            )
        else:
            metadata_dict, node_info, relationships = legacy_metadata_dict_to_node(
                metadata=metadata,
                text_key=self.text_key,
            )

            # Create TextNode with the extracted metadata
            # Step 1: Get the JSON string from "_node_content"
            _node_content_str = metadata.get("_node_content", "{}")

            # Step 2: Convert JSON string to Python dict
            try:
                node_content = json.loads(_node_content_str)
            except json.JSONDecodeError:
                node_content = {}

            # Step 3: Get the text
            text = node_content.get(self.text_key, "")
            node = TextNode(
                text=text,
                metadata=metadata_dict,
                relationships=relationships,
                node_id=node_id,
            )

            # Add any node_info properties to the node
            for key, val in node_info.items():
                if hasattr(node, key):
                    setattr(node, key, val)

        # If embedding was returned in the results, add it to the node
        if "vector" in result:
            node.embedding = result["vector"]

        nodes.append(node)
        similarities.append(score)
        ids.append(node_id)

    return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
options: members: - VectorXVectorStore
