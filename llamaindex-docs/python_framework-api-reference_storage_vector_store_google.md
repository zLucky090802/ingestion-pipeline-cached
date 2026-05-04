# Google
##  GoogleVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/google/#llama_index.vector_stores.google.GoogleVectorStore "Permanent link")
Bases: 
Google GenerativeAI Vector Store.
Currently, it computes the embedding vectors on the server side.
Examples:
google_vector_store = GoogleVectorStore.from_corpus( corpus_id="my-corpus-id", include_metadata=True, metadata_keys=['file_name', 'creation_date'] ) index = VectorStoreIndex.from_vector_store( vector_store=google_vector_store )
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
|   |  The corpus ID that this vector store instance will read and write to.  |  
| `include_metadata`  |  `bool`  |  Indicates whether to include custom metadata in the query results. Defaults to False.  |  
| `metadata_keys`  |  `Optional[List[str]]`  |  Specifies which metadata keys to include in the query results if include_metadata is set to True. If None, all metadata keys are included. Defaults to None.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-google/llama_index/vector_stores/google/base.py`  
| 
```
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
```
 | 
```
classGoogleVectorStore(BasePydanticVectorStore):
"""
    Google GenerativeAI Vector Store.

    Currently, it computes the embedding vectors on the server side.

    Examples:
        google_vector_store = GoogleVectorStore.from_corpus(
            corpus_id="my-corpus-id",
            include_metadata=True,
            metadata_keys=['file_name', 'creation_date']

        index = VectorStoreIndex.from_vector_store(
            vector_store=google_vector_store


    Attributes:
        corpus_id: The corpus ID that this vector store instance will read and
            write to.
        include_metadata (bool): Indicates whether to include custom metadata in the query
            results. Defaults to False.
        metadata_keys (Optional[List[str]]): Specifies which metadata keys to include in the
            query results if include_metadata is set to True. If None, all metadata keys
            are included. Defaults to None.

    """

    # Semantic Retriever stores the document node's text as string and embeds
    # the vectors on the server automatically.
    stores_text: bool = True
    is_embedding_query: bool = False

    # This is not the Google's corpus name but an ID generated in the LlamaIndex
    # world.
    corpus_id: str = Field(frozen=True)
"""Corpus ID that this instance of the vector store is using."""

    # Configuration options for handling metadata in query results
    include_metadata: bool = False
    metadata_keys: Optional[List[str]] = None

    _client: Any = PrivateAttr()

    def__init__(self, *, client: Any, **kwargs: Any):
"""
        Raw constructor.

        Use the class method `from_corpus` or `create_corpus` instead.

        Args:
            client: The low-level retriever class from google.ai.generativelanguage.

        """
        try:
            importgoogle.ai.generativelanguageasgenai
        except ImportError:
            raise ImportError(_import_err_msg)

        super().__init__(**kwargs)

        assert isinstance(client, genai.RetrieverServiceClient)
        self._client = client

    @classmethod
    deffrom_corpus(
        cls,
        *,
        corpus_id: str,
        include_metadata: bool = False,
        metadata_keys: Optional[List[str]] = None,
    ) -> "GoogleVectorStore":
"""
        Create an instance that points to an existing corpus.

        Args:
            corpus_id (str): ID of an existing corpus on Google's server.
            include_metadata (bool, optional): Specifies whether to include custom metadata in the
                query results. Defaults to False, meaning metadata will not be included.
            metadata_keys (Optional[List[str]], optional): Specifies which metadata keys to include
                in the query results if include_metadata is set to True. If None, all metadata keys
                are included. Defaults to None.

        Returns:
            An instance of the vector store that points to the specified corpus.

        Raises:
            NoSuchCorpusException if no such corpus is found.

        """
        try:
            importllama_index.vector_stores.google.genai_extensionasgenaix
        except ImportError:
            raise ImportError(_import_err_msg)

        _logger.debug(f"\n\nGoogleVectorStore.from_corpus(corpus_id={corpus_id})")
        client = genaix.build_semantic_retriever()
        if genaix.get_corpus(corpus_id=corpus_id, client=client) is None:
            raise NoSuchCorpusException(corpus_id=corpus_id)

        return cls(
            corpus_id=corpus_id,
            client=client,
            include_metadata=include_metadata,
            metadata_keys=metadata_keys,
        )

    @classmethod
    defcreate_corpus(
        cls, *, corpus_id: Optional[str] = None, display_name: Optional[str] = None
    ) -> "GoogleVectorStore":
"""
        Create an instance that points to a newly created corpus.

        Examples:
            store = GoogleVectorStore.create_corpus()
            print(f"Created corpus with ID: {store.corpus_id})

            store = GoogleVectorStore.create_corpus(
                display_name="My first corpus"


            store = GoogleVectorStore.create_corpus(
                corpus_id="my-corpus-1",
                display_name="My first corpus"


        Args:
            corpus_id: ID of the new corpus to be created. If not provided,
                Google server will provide one for you.
            display_name: Title of the corpus. If not provided, Google server
                will provide one for you.

        Returns:
            An instance of the vector store that points to the specified corpus.

        Raises:
            An exception if the corpus already exists or the user hits the
            quota limit.

        """
        try:
            importllama_index.vector_stores.google.genai_extensionasgenaix
        except ImportError:
            raise ImportError(_import_err_msg)

        _logger.debug(
            f"\n\nGoogleVectorStore.create_corpus(new_corpus_id={corpus_id}, new_display_name={display_name})"
        )

        client = genaix.build_semantic_retriever()
        new_corpus_id = corpus_id or str(uuid.uuid4())
        new_corpus = genaix.create_corpus(
            corpus_id=new_corpus_id, display_name=display_name, client=client
        )
        name = genaix.EntityName.from_str(new_corpus.name)
        return cls(corpus_id=name.corpus_id, client=client)

    @classmethod
    defclass_name(cls) -> str:
        return "GoogleVectorStore"

    @property
    defclient(self) -> Any:
        return self._client

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
        Add nodes with embedding to vector store.

        If a node has a source node, the source node's ID will be used to create
        a document. Otherwise, a default document for that corpus will be used
        to house the node.

        Furthermore, if the source node has a metadata field "file_name", it
        will be used as the title of the document. If the source node has no
        such field, Google server will assign a title to the document.

        Example:
            store = GoogleVectorStore.from_corpus(corpus_id="123")
            store.add([
                TextNode(
                    text="Hello, my darling",
                    relationships={
                        NodeRelationship.SOURCE: RelatedNodeInfo(
                            node_id="doc-456",
                            metadata={"file_name": "Title for doc-456"},



                TextNode(
                    text="Goodbye, my baby",
                    relationships={
                        NodeRelationship.SOURCE: RelatedNodeInfo(
                            node_id="doc-456",
                            metadata={"file_name": "Title for doc-456"},





        The above code will create one document with ID `doc-456` and title
        `Title for doc-456`. This document will house both nodes.

        """
        try:
            importllama_index.vector_stores.google.genai_extensionasgenaix

            importgoogle.ai.generativelanguageasgenai
        except ImportError:
            raise ImportError(_import_err_msg)

        _logger.debug(f"\n\nGoogleVectorStore.add(nodes={nodes})")

        client = cast(genai.RetrieverServiceClient, self.client)

        created_node_ids: List[str] = []
        for nodeGroup in _group_nodes_by_source(nodes):
            source = nodeGroup.source_node
            document_id = source.node_id
            document = genaix.get_document(
                corpus_id=self.corpus_id, document_id=document_id, client=client
            )

            if not document:
                genaix.create_document(
                    corpus_id=self.corpus_id,
                    display_name=source.metadata.get("file_name", None),
                    document_id=document_id,
                    metadata=source.metadata,
                    client=client,
                )

            created_chunks = genaix.batch_create_chunk(
                corpus_id=self.corpus_id,
                document_id=document_id,
                texts=[node.get_content() for node in nodeGroup.nodes],
                metadatas=[node.metadata for node in nodeGroup.nodes],
                client=client,
            )
            created_node_ids.extend([chunk.name for chunk in created_chunks])

        return created_node_ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes by ref_doc_id.

        Both the underlying nodes and the document will be deleted from Google
        server.

        Args:
            ref_doc_id: The document ID to be deleted.

        """
        try:
            importllama_index.vector_stores.google.genai_extensionasgenaix

            importgoogle.ai.generativelanguageasgenai
        except ImportError:
            raise ImportError(_import_err_msg)

        _logger.debug(f"\n\nGoogleVectorStore.delete(ref_doc_id={ref_doc_id})")

        client = cast(genai.RetrieverServiceClient, self.client)
        genaix.delete_document(
            corpus_id=self.corpus_id, document_id=ref_doc_id, client=client
        )

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query vector store.

        Example:
            store = GoogleVectorStore.from_corpus(corpus_id="123")
            store.query(
                query=VectorStoreQuery(
                    query_str="What is the meaning of life?",
                    # Only nodes with this author.
                    filters=MetadataFilters(
                        filters=[
                            ExactMatchFilter(
                                key="author",
                                value="Arthur Schopenhauer",



                    # Only from these docs. If not provided,
                    # the entire corpus is searched.
                    doc_ids=["doc-456"],
                    similarity_top_k=3,



        Args:
            query: See `llama_index.core.vector_stores.types.VectorStoreQuery`.

        """
        try:
            importllama_index.vector_stores.google.genai_extensionasgenaix

            importgoogle.ai.generativelanguageasgenai
        except ImportError:
            raise ImportError(_import_err_msg)

        _logger.debug(f"\n\nGoogleVectorStore.query(query={query})")

        query_str = query.query_str
        if query_str is None:
            raise ValueError("VectorStoreQuery.query_str should not be None.")

        client = cast(genai.RetrieverServiceClient, self.client)

        relevant_chunks: List[genai.RelevantChunk] = []
        if query.doc_ids is None:
            # The chunks from query_corpus should be sorted in reverse order by
            # relevant score.
            relevant_chunks = genaix.query_corpus(
                corpus_id=self.corpus_id,
                query=query_str,
                filter=_convert_filter(query.filters),
                k=query.similarity_top_k,
                client=client,
            )
        else:
            for doc_id in query.doc_ids:
                relevant_chunks.extend(
                    genaix.query_document(
                        corpus_id=self.corpus_id,
                        document_id=doc_id,
                        query=query_str,
                        filter=_convert_filter(query.filters),
                        k=query.similarity_top_k,
                        client=client,
                    )
                )
            # Make sure the chunks are reversed sorted according to relevant
            # scores even across multiple documents.
            relevant_chunks.sort(key=lambda c: c.chunk_relevance_score, reverse=True)

        nodes = []
        include_metadata = self.include_metadata
        metadata_keys = self.metadata_keys
        for chunk in relevant_chunks:
            metadata = {}
            if include_metadata:
                for custom_metadata in chunk.chunk.custom_metadata:
                    # Use getattr to safely extract values
                    value = getattr(custom_metadata, "string_value", None)
                    if (
                        value is None
                    ):  # If string_value is not set, check for numeric_value
                        value = getattr(custom_metadata, "numeric_value", None)
                    # Add to the metadata dictionary only those keys that are present in metadata_keys
                    if value is not None and (
                        metadata_keys is None or custom_metadata.key in metadata_keys
                    ):
                        metadata[custom_metadata.key] = value

            text_node = TextNode(
                text=chunk.chunk.data.string_value,
                id=_extract_chunk_id(chunk.chunk.name),
                metadata=metadata,  # Adding metadata to the node
            )
            nodes.append(text_node)

        return VectorStoreQueryResult(
            nodes=nodes,
            ids=[_extract_chunk_id(chunk.chunk.name) for chunk in relevant_chunks],
            similarities=[chunk.chunk_relevance_score for chunk in relevant_chunks],
        )

```
 |  
| --- | --- |  
###  corpus_id `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/google/#llama_index.vector_stores.google.GoogleVectorStore.corpus_id "Permanent link")

```
corpus_id:  = (frozen=True)

```

Corpus ID that this instance of the vector store is using.
###  from_corpus `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/google/#llama_index.vector_stores.google.GoogleVectorStore.from_corpus "Permanent link")

```
from_corpus(
    *,
    corpus_id: ,
    include_metadata:  = False,
    metadata_keys: Optional[[]] = None
) -> 

```

Create an instance that points to an existing corpus.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `corpus_id`  |  ID of an existing corpus on Google's server.  |  _required_  |  
|  `include_metadata`  |  `bool`  |  Specifies whether to include custom metadata in the query results. Defaults to False, meaning metadata will not be included.  |  `False`  |  
|  `metadata_keys`  |  `Optional[List[str]]`  |  Specifies which metadata keys to include in the query results if include_metadata is set to True. If None, all metadata keys are included. Defaults to None.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  An instance of the vector store that points to the specified corpus.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-google/llama_index/vector_stores/google/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_corpus(
    cls,
    *,
    corpus_id: str,
    include_metadata: bool = False,
    metadata_keys: Optional[List[str]] = None,
) -> "GoogleVectorStore":
"""
    Create an instance that points to an existing corpus.

    Args:
        corpus_id (str): ID of an existing corpus on Google's server.
        include_metadata (bool, optional): Specifies whether to include custom metadata in the
            query results. Defaults to False, meaning metadata will not be included.
        metadata_keys (Optional[List[str]], optional): Specifies which metadata keys to include
            in the query results if include_metadata is set to True. If None, all metadata keys
            are included. Defaults to None.

    Returns:
        An instance of the vector store that points to the specified corpus.

    Raises:
        NoSuchCorpusException if no such corpus is found.

    """
    try:
        importllama_index.vector_stores.google.genai_extensionasgenaix
    except ImportError:
        raise ImportError(_import_err_msg)

    _logger.debug(f"\n\nGoogleVectorStore.from_corpus(corpus_id={corpus_id})")
    client = genaix.build_semantic_retriever()
    if genaix.get_corpus(corpus_id=corpus_id, client=client) is None:
        raise NoSuchCorpusException(corpus_id=corpus_id)

    return cls(
        corpus_id=corpus_id,
        client=client,
        include_metadata=include_metadata,
        metadata_keys=metadata_keys,
    )

```
 |  
| --- | --- |  
###  create_corpus `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/google/#llama_index.vector_stores.google.GoogleVectorStore.create_corpus "Permanent link")

```
create_corpus(
    *,
    corpus_id: Optional[] = None,
    display_name: Optional[] = None
) -> 

```

Create an instance that points to a newly created corpus.
Examples:
store = GoogleVectorStore.create_corpus() print(f"Created corpus with ID: {store.corpus_id})
store = GoogleVectorStore.create_corpus( display_name="My first corpus" )
store = GoogleVectorStore.create_corpus( corpus_id="my-corpus-1", display_name="My first corpus" )
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `corpus_id`  |  `Optional[str]`  |  ID of the new corpus to be created. If not provided, Google server will provide one for you.  |  `None`  |  
|  `display_name`  |  `Optional[str]`  |  Title of the corpus. If not provided, Google server will provide one for you.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  An instance of the vector store that points to the specified corpus.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-google/llama_index/vector_stores/google/base.py`  
| 
```
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
```
 | 
```
@classmethod
defcreate_corpus(
    cls, *, corpus_id: Optional[str] = None, display_name: Optional[str] = None
) -> "GoogleVectorStore":
"""
    Create an instance that points to a newly created corpus.

    Examples:
        store = GoogleVectorStore.create_corpus()
        print(f"Created corpus with ID: {store.corpus_id})

        store = GoogleVectorStore.create_corpus(
            display_name="My first corpus"


        store = GoogleVectorStore.create_corpus(
            corpus_id="my-corpus-1",
            display_name="My first corpus"


    Args:
        corpus_id: ID of the new corpus to be created. If not provided,
            Google server will provide one for you.
        display_name: Title of the corpus. If not provided, Google server
            will provide one for you.

    Returns:
        An instance of the vector store that points to the specified corpus.

    Raises:
        An exception if the corpus already exists or the user hits the
        quota limit.

    """
    try:
        importllama_index.vector_stores.google.genai_extensionasgenaix
    except ImportError:
        raise ImportError(_import_err_msg)

    _logger.debug(
        f"\n\nGoogleVectorStore.create_corpus(new_corpus_id={corpus_id}, new_display_name={display_name})"
    )

    client = genaix.build_semantic_retriever()
    new_corpus_id = corpus_id or str(uuid.uuid4())
    new_corpus = genaix.create_corpus(
        corpus_id=new_corpus_id, display_name=display_name, client=client
    )
    name = genaix.EntityName.from_str(new_corpus.name)
    return cls(corpus_id=name.corpus_id, client=client)

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/google/#llama_index.vector_stores.google.GoogleVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes with embedding to vector store.
If a node has a source node, the source node's ID will be used to create a document. Otherwise, a default document for that corpus will be used to house the node.
Furthermore, if the source node has a metadata field "file_name", it will be used as the title of the document. If the source node has no such field, Google server will assign a title to the document.
Example
store = GoogleVectorStore.from_corpus(corpus_id="123") store.add([ TextNode( text="Hello, my darling", relationships={ NodeRelationship.SOURCE: RelatedNodeInfo( node_id="doc-456", metadata={"file_name": "Title for doc-456"}, ) }, ), TextNode( text="Goodbye, my baby", relationships={ NodeRelationship.SOURCE: RelatedNodeInfo( node_id="doc-456", metadata={"file_name": "Title for doc-456"}, ) }, ), ])
The above code will create one document with ID `doc-456` and title `Title for doc-456`. This document will house both nodes.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-google/llama_index/vector_stores/google/base.py`  
| 
```
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
```
 | 
```
defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
    Add nodes with embedding to vector store.

    If a node has a source node, the source node's ID will be used to create
    a document. Otherwise, a default document for that corpus will be used
    to house the node.

    Furthermore, if the source node has a metadata field "file_name", it
    will be used as the title of the document. If the source node has no
    such field, Google server will assign a title to the document.

    Example:
        store = GoogleVectorStore.from_corpus(corpus_id="123")
        store.add([
            TextNode(
                text="Hello, my darling",
                relationships={
                    NodeRelationship.SOURCE: RelatedNodeInfo(
                        node_id="doc-456",
                        metadata={"file_name": "Title for doc-456"},



            TextNode(
                text="Goodbye, my baby",
                relationships={
                    NodeRelationship.SOURCE: RelatedNodeInfo(
                        node_id="doc-456",
                        metadata={"file_name": "Title for doc-456"},





    The above code will create one document with ID `doc-456` and title
    `Title for doc-456`. This document will house both nodes.

    """
    try:
        importllama_index.vector_stores.google.genai_extensionasgenaix

        importgoogle.ai.generativelanguageasgenai
    except ImportError:
        raise ImportError(_import_err_msg)

    _logger.debug(f"\n\nGoogleVectorStore.add(nodes={nodes})")

    client = cast(genai.RetrieverServiceClient, self.client)

    created_node_ids: List[str] = []
    for nodeGroup in _group_nodes_by_source(nodes):
        source = nodeGroup.source_node
        document_id = source.node_id
        document = genaix.get_document(
            corpus_id=self.corpus_id, document_id=document_id, client=client
        )

        if not document:
            genaix.create_document(
                corpus_id=self.corpus_id,
                display_name=source.metadata.get("file_name", None),
                document_id=document_id,
                metadata=source.metadata,
                client=client,
            )

        created_chunks = genaix.batch_create_chunk(
            corpus_id=self.corpus_id,
            document_id=document_id,
            texts=[node.get_content() for node in nodeGroup.nodes],
            metadatas=[node.metadata for node in nodeGroup.nodes],
            client=client,
        )
        created_node_ids.extend([chunk.name for chunk in created_chunks])

    return created_node_ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/google/#llama_index.vector_stores.google.GoogleVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes by ref_doc_id.
Both the underlying nodes and the document will be deleted from Google server.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The document ID to be deleted.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-google/llama_index/vector_stores/google/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes by ref_doc_id.

    Both the underlying nodes and the document will be deleted from Google
    server.

    Args:
        ref_doc_id: The document ID to be deleted.

    """
    try:
        importllama_index.vector_stores.google.genai_extensionasgenaix

        importgoogle.ai.generativelanguageasgenai
    except ImportError:
        raise ImportError(_import_err_msg)

    _logger.debug(f"\n\nGoogleVectorStore.delete(ref_doc_id={ref_doc_id})")

    client = cast(genai.RetrieverServiceClient, self.client)
    genaix.delete_document(
        corpus_id=self.corpus_id, document_id=ref_doc_id, client=client
    )

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/google/#llama_index.vector_stores.google.GoogleVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query vector store.
Example
store = GoogleVectorStore.from_corpus(corpus_id="123") store.query( query=VectorStoreQuery( query_str="What is the meaning of life?", # Only nodes with this author. filters=MetadataFilters( filters=[ ExactMatchFilter( key="author", value="Arthur Schopenhauer", ) ] ), # Only from these docs. If not provided, # the entire corpus is searched. doc_ids=["doc-456"], similarity_top_k=3, ) )
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  See `llama_index.core.vector_stores.types.VectorStoreQuery`.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-google/llama_index/vector_stores/google/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query vector store.

    Example:
        store = GoogleVectorStore.from_corpus(corpus_id="123")
        store.query(
            query=VectorStoreQuery(
                query_str="What is the meaning of life?",
                # Only nodes with this author.
                filters=MetadataFilters(
                    filters=[
                        ExactMatchFilter(
                            key="author",
                            value="Arthur Schopenhauer",



                # Only from these docs. If not provided,
                # the entire corpus is searched.
                doc_ids=["doc-456"],
                similarity_top_k=3,



    Args:
        query: See `llama_index.core.vector_stores.types.VectorStoreQuery`.

    """
    try:
        importllama_index.vector_stores.google.genai_extensionasgenaix

        importgoogle.ai.generativelanguageasgenai
    except ImportError:
        raise ImportError(_import_err_msg)

    _logger.debug(f"\n\nGoogleVectorStore.query(query={query})")

    query_str = query.query_str
    if query_str is None:
        raise ValueError("VectorStoreQuery.query_str should not be None.")

    client = cast(genai.RetrieverServiceClient, self.client)

    relevant_chunks: List[genai.RelevantChunk] = []
    if query.doc_ids is None:
        # The chunks from query_corpus should be sorted in reverse order by
        # relevant score.
        relevant_chunks = genaix.query_corpus(
            corpus_id=self.corpus_id,
            query=query_str,
            filter=_convert_filter(query.filters),
            k=query.similarity_top_k,
            client=client,
        )
    else:
        for doc_id in query.doc_ids:
            relevant_chunks.extend(
                genaix.query_document(
                    corpus_id=self.corpus_id,
                    document_id=doc_id,
                    query=query_str,
                    filter=_convert_filter(query.filters),
                    k=query.similarity_top_k,
                    client=client,
                )
            )
        # Make sure the chunks are reversed sorted according to relevant
        # scores even across multiple documents.
        relevant_chunks.sort(key=lambda c: c.chunk_relevance_score, reverse=True)

    nodes = []
    include_metadata = self.include_metadata
    metadata_keys = self.metadata_keys
    for chunk in relevant_chunks:
        metadata = {}
        if include_metadata:
            for custom_metadata in chunk.chunk.custom_metadata:
                # Use getattr to safely extract values
                value = getattr(custom_metadata, "string_value", None)
                if (
                    value is None
                ):  # If string_value is not set, check for numeric_value
                    value = getattr(custom_metadata, "numeric_value", None)
                # Add to the metadata dictionary only those keys that are present in metadata_keys
                if value is not None and (
                    metadata_keys is None or custom_metadata.key in metadata_keys
                ):
                    metadata[custom_metadata.key] = value

        text_node = TextNode(
            text=chunk.chunk.data.string_value,
            id=_extract_chunk_id(chunk.chunk.name),
            metadata=metadata,  # Adding metadata to the node
        )
        nodes.append(text_node)

    return VectorStoreQueryResult(
        nodes=nodes,
        ids=[_extract_chunk_id(chunk.chunk.name) for chunk in relevant_chunks],
        similarities=[chunk.chunk_relevance_score for chunk in relevant_chunks],
    )

```
 |  
| --- | --- |  
##  set_google_config [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/google/#llama_index.vector_stores.google.set_google_config "Permanent link")

```
set_google_config(
    *,
    api_endpoint: Optional[] = None,
    user_agent: Optional[] = None,
    page_size: Optional[] = None,
    auth_credentials: Optional[Credentials] = None,
    **kwargs: 
) -> None

```

Set the configuration for Google Generative AI API.
Parameters are optional, Normally, the defaults should work fine. If provided, they will override the default values in the Config class. See the docstring in `genai_extension.py` for more details. auth_credentials: Optional["credentials.Credentials"] = None, Use this to pass Google Auth credentials such as using a service account. Refer to for auth credentials documentation: https://developers.google.com/identity/protocols/oauth2/service-account#creatinganaccount.
Example
from google.oauth2 import service_account credentials = service_account.Credentials.from_service_account_file( "/path/to/service.json", scopes=[ "https://www.googleapis.com/auth/cloud-platform", "https://www.googleapis.com/auth/generative-language.retriever", ], ) set_google_config(auth_credentials=credentials)
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-google/llama_index/vector_stores/google/base.py`  
| 
```
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
```
 | 
```
defset_google_config(
    *,
    api_endpoint: Optional[str] = None,
    user_agent: Optional[str] = None,
    page_size: Optional[int] = None,
    auth_credentials: Optional["credentials.Credentials"] = None,
    **kwargs: Any,
) -> None:
"""
    Set the configuration for Google Generative AI API.

    Parameters are optional, Normally, the defaults should work fine.
    If provided, they will override the default values in the Config class.
    See the docstring in `genai_extension.py` for more details.
    auth_credentials: Optional["credentials.Credentials"] = None,
    Use this to pass Google Auth credentials such as using a service account.
    Refer to for auth credentials documentation:
    https://developers.google.com/identity/protocols/oauth2/service-account#creatinganaccount.

    Example:
        from google.oauth2 import service_account
        credentials = service_account.Credentials.from_service_account_file(
            "/path/to/service.json",
            scopes=[
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/generative-language.retriever",


        set_google_config(auth_credentials=credentials)

    """
    try:
        importllama_index.vector_stores.google.genai_extensionasgenaix
    except ImportError:
        raise ImportError(_import_err_msg)

    config_attrs = {
        "api_endpoint": api_endpoint,
        "user_agent": user_agent,
        "page_size": page_size,
        "auth_credentials": auth_credentials,
        "testing": kwargs.get("testing"),
    }
    attrs = {k: v for k, v in config_attrs.items() if v is not None}
    config = genaix.Config(**attrs)
    genaix.set_config(config)

```
 |  
| --- | --- |  
options: members: - GoogleVectorStore
