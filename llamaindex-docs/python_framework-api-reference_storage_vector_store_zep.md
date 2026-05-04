# Zep
##  ZepVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/zep/#llama_index.vector_stores.zep.ZepVectorStore "Permanent link")
Bases: 
Zep Vector Store for storing and retrieving embeddings.
Zep supports both normalized and non-normalized embeddings. Cosine similarity is used to compute distance and the returned score is normalized to be between 0 and 1.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection_name`  |  Name of the Zep collection in which to store embeddings.  |  _required_  |  
|  `api_url`  |  URL of the Zep API.  |  _required_  |  
|  `api_key`  |  Key for the Zep API. Defaults to None.  |  `None`  |  
|  `collection_description`  |  Description of the collection. Defaults to None.  |  `None`  |  
|  `collection_metadata`  |  `dict`  |  Metadata of the collection. Defaults to None.  |  `None`  |  
|  `embedding_dimensions`  |  Dimensions of the embeddings. Defaults to None.  |  `None`  |  
|  `is_auto_embedded`  |  `bool`  |  Whether the embeddings are auto-embedded. Defaults to False.  |  `False`  |  
Examples:
`pip install llama-index-vector-stores-zep`

```
fromllama_index.vector_stores.zepimport ZepVectorStore

vector_store = ZepVectorStore(
    api_url="<api_url>",
    api_key="<api_key>",
    collection_name="<unique_collection_name>",  # Can either be an existing collection or a new one
    embedding_dimensions=1536,  # Optional, required if creating a new collection
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-zep/llama_index/vector_stores/zep/base.py`  
| 
```
 24
 25
 26
 27
 28
 29
 30
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
```
 | 
```
classZepVectorStore(BasePydanticVectorStore):
"""
    Zep Vector Store for storing and retrieving embeddings.

    Zep supports both normalized and non-normalized embeddings. Cosine similarity is
    used to compute distance and the returned score is normalized to be between 0 and 1.

    Args:
        collection_name (str): Name of the Zep collection in which to store embeddings.
        api_url (str): URL of the Zep API.
        api_key (str, optional): Key for the Zep API. Defaults to None.
        collection_description (str, optional): Description of the collection.
            Defaults to None.
        collection_metadata (dict, optional): Metadata of the collection.
            Defaults to None.
        embedding_dimensions (int, optional): Dimensions of the embeddings.
            Defaults to None.
        is_auto_embedded (bool, optional): Whether the embeddings are auto-embedded.
            Defaults to False.

    Examples:
        `pip install llama-index-vector-stores-zep`

        ```python
        from llama_index.vector_stores.zep import ZepVectorStore

        vector_store = ZepVectorStore(
            api_url="<api_url>",
            api_key="<api_key>",
            collection_name="<unique_collection_name>",  # Can either be an existing collection or a new one
            embedding_dimensions=1536,  # Optional, required if creating a new collection

        ```

    """

    stores_text: bool = True
    flat_metadata: bool = False

    _client: ZepClient = PrivateAttr()
    _collection: DocumentCollection = PrivateAttr()

    def__init__(
        self,
        collection_name: str,
        api_url: str,
        api_key: Optional[str] = None,
        collection_description: Optional[str] = None,
        collection_metadata: Optional[Dict[str, Any]] = None,
        embedding_dimensions: Optional[int] = None,
        is_auto_embedded: bool = False,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        super().__init__()

        self._client = ZepClient(base_url=api_url, api_key=api_key)
        collection: Union[DocumentCollection, None] = None

        try:
            collection = self._client.document.get_collection(name=collection_name)
        except zep_python.NotFoundError:
            if embedding_dimensions is None:
                raise ValueError(
                    "embedding_dimensions must be specified if collection does not"
                    " exist"
                )
            logger.info(
                f"Collection {collection_name} does not exist, "
                f"will try creating one with dimensions={embedding_dimensions}"
            )

            collection = self._client.document.add_collection(
                name=collection_name,
                embedding_dimensions=embedding_dimensions,
                is_auto_embedded=is_auto_embedded,
                description=collection_description,
                metadata=collection_metadata,
            )

        assert collection is not None
        self._collection = collection

    @classmethod
    defclass_name(cls) -> str:
        return "ZepVectorStore"

    @property
    defclient(self) -> Any:
"""Get client."""
        return self._client

    def_prepare_documents(
        self, nodes: List[BaseNode]
    ) -> Tuple[List["ZepDocument"], List[str]]:
        docs: List["ZepDocument"] = []
        ids: List[str] = []

        for node in nodes:
            metadata_dict: Dict[str, Any] = node_to_metadata_dict(
                node, remove_text=True, flat_metadata=self.flat_metadata
            )

            if len(node.get_content()) == 0:
                raise ValueError("No content to add to Zep")

            docs.append(
                ZepDocument(
                    document_id=node.node_id,
                    content=node.get_content(metadata_mode=MetadataMode.NONE),
                    embedding=node.get_embedding(),
                    metadata=metadata_dict,
                )
            )
            ids.append(node.node_id)

        return docs, ids

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
        Add nodes to the collection.

        Args:
            nodes (List[BaseNode]): List of nodes with embeddings.

        Returns:
            List[str]: List of IDs of the added documents.

        """
        if not isinstance(self._collection, DocumentCollection):
            raise ValueError("Collection not initialized")

        if self._collection.is_auto_embedded:
            raise ValueError("Collection is auto embedded, cannot add embeddings")

        docs, ids = self._prepare_documents(nodes)

        self._collection.add_documents(docs)

        return ids

    async defasync_add(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Asynchronously add nodes to the collection.

        Args:
            nodes (List[BaseNode]): List of nodes with embeddings.

        Returns:
            List[str]: List of IDs of the added documents.

        """
        if not isinstance(self._collection, DocumentCollection):
            raise ValueError("Collection not initialized")

        if self._collection.is_auto_embedded:
            raise ValueError("Collection is auto embedded, cannot add embeddings")

        docs, ids = self._prepare_documents(nodes)

        await self._collection.aadd_documents(docs)

        return ids

    defdelete(self, ref_doc_id: Optional[str] = None, **delete_kwargs: Any) -> None:  # type: ignore
"""
        Delete a document from the collection.

        Args:
            ref_doc_id (Optional[str]): ID of the document to delete.
                Not currently supported.
            delete_kwargs: Must contain "uuid" key with UUID of the document to delete.

        """
        if not isinstance(self._collection, DocumentCollection):
            raise ValueError("Collection not initialized")

        if ref_doc_id and len(ref_doc_id)  0:
            raise NotImplementedError(
                "Delete by ref_doc_id not yet implemented for Zep."
            )

        if "uuid" in delete_kwargs:
            self._collection.delete_document(uuid=delete_kwargs["uuid"])
        else:
            raise ValueError("uuid must be specified")

    async defadelete(
        self, ref_doc_id: Optional[str] = None, **delete_kwargs: Any
    ) -> None:  # type: ignore
"""
        Asynchronously delete a document from the collection.

        Args:
            ref_doc_id (Optional[str]): ID of the document to delete.
                Not currently supported.
            delete_kwargs: Must contain "uuid" key with UUID of the document to delete.

        """
        if not isinstance(self._collection, DocumentCollection):
            raise ValueError("Collection not initialized")

        if ref_doc_id and len(ref_doc_id)  0:
            raise NotImplementedError(
                "Delete by ref_doc_id not yet implemented for Zep."
            )

        if "uuid" in delete_kwargs:
            await self._collection.adelete_document(uuid=delete_kwargs["uuid"])
        else:
            raise ValueError("uuid must be specified")

    def_parse_query_result(
        self, results: List["ZepDocument"]
    ) -> VectorStoreQueryResult:
        similarities: List[float] = []
        ids: List[str] = []
        nodes: List[TextNode] = []

        for d in results:
            node = metadata_dict_to_node(d.metadata or {})
            node.set_content(d.content)

            nodes.append(node)

            if d.score is None:
                d.score = 0.0
            similarities.append(d.score)

            if d.document_id is None:
                d.document_id = ""
            ids.append(d.document_id)

        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

    def_to_zep_filters(self, filters: MetadataFilters) -> Dict[str, Any]:
"""Convert filters to Zep filters. Filters are ANDed together."""
        filter_conditions: List[Dict[str, Any]] = []

        for f in filters.legacy_filters():
            filter_conditions.append({"jsonpath": f'$[*] ? (@.{f.key} == "{f.value}")'})

        return {"where": {"and": filter_conditions}}

    defquery(
        self,
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""
        Query the index for the top k most similar nodes to the given query.

        Args:
            query (VectorStoreQuery): Query object containing either a query string
                or a query embedding.

        Returns:
            VectorStoreQueryResult: Result of the query, containing the most similar
                nodes, their similarities, and their IDs.

        """
        if not isinstance(self._collection, DocumentCollection):
            raise ValueError("Collection not initialized")

        if query.query_embedding is None and query.query_str is None:
            raise ValueError("query must have one of query_str or query_embedding")

        # If we have an embedding, we shouldn't use the query string
        # Zep does not allow both to be set
        if query.query_embedding:
            query.query_str = None

        metadata_filters = None
        if query.filters is not None:
            metadata_filters = self._to_zep_filters(query.filters)

        results = self._collection.search(
            text=query.query_str,
            embedding=query.query_embedding,
            metadata=metadata_filters,
            limit=query.similarity_top_k,
        )

        return self._parse_query_result(results)

    async defaquery(
        self,
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""
        Asynchronously query the index for the top k most similar nodes to the
            given query.

        Args:
            query (VectorStoreQuery): Query object containing either a query string or
                a query embedding.

        Returns:
            VectorStoreQueryResult: Result of the query, containing the most similar
                nodes, their similarities, and their IDs.

        """
        if not isinstance(self._collection, DocumentCollection):
            raise ValueError("Collection not initialized")

        if query.query_embedding is None and query.query_str is None:
            raise ValueError("query must have one of query_str or query_embedding")

        # If we have an embedding, we shouldn't use the query string
        # Zep does not allow both to be set
        if query.query_embedding:
            query.query_str = None

        metadata_filters = None
        if query.filters is not None:
            metadata_filters = self._to_zep_filters(query.filters)

        results = await self._collection.asearch(
            text=query.query_str,
            embedding=query.query_embedding,
            metadata=metadata_filters,
            limit=query.similarity_top_k,
        )

        return self._parse_query_result(results)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/zep/#llama_index.vector_stores.zep.ZepVectorStore.client "Permanent link")

```
client: 

```

Get client.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/zep/#llama_index.vector_stores.zep.ZepVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to the collection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes with embeddings.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: List of IDs of the added documents.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-zep/llama_index/vector_stores/zep/base.py`  
| 
```
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
```
 | 
```
defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
    Add nodes to the collection.

    Args:
        nodes (List[BaseNode]): List of nodes with embeddings.

    Returns:
        List[str]: List of IDs of the added documents.

    """
    if not isinstance(self._collection, DocumentCollection):
        raise ValueError("Collection not initialized")

    if self._collection.is_auto_embedded:
        raise ValueError("Collection is auto embedded, cannot add embeddings")

    docs, ids = self._prepare_documents(nodes)

    self._collection.add_documents(docs)

    return ids

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/zep/#llama_index.vector_stores.zep.ZepVectorStore.async_add "Permanent link")

```
async_add(
    nodes: [], **add_kwargs: 
) -> []

```

Asynchronously add nodes to the collection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes with embeddings.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: List of IDs of the added documents.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-zep/llama_index/vector_stores/zep/base.py`  
| 
```
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
```
 | 
```
async defasync_add(
    self,
    nodes: List[BaseNode],
    **add_kwargs: Any,
) -> List[str]:
"""
    Asynchronously add nodes to the collection.

    Args:
        nodes (List[BaseNode]): List of nodes with embeddings.

    Returns:
        List[str]: List of IDs of the added documents.

    """
    if not isinstance(self._collection, DocumentCollection):
        raise ValueError("Collection not initialized")

    if self._collection.is_auto_embedded:
        raise ValueError("Collection is auto embedded, cannot add embeddings")

    docs, ids = self._prepare_documents(nodes)

    await self._collection.aadd_documents(docs)

    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/zep/#llama_index.vector_stores.zep.ZepVectorStore.delete "Permanent link")

```
delete(
    ref_doc_id: Optional[] = None, **delete_kwargs: 
) -> None

```

Delete a document from the collection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  `Optional[str]`  |  ID of the document to delete. Not currently supported.  |  `None`  |  
|  `delete_kwargs`  |  Must contain "uuid" key with UUID of the document to delete.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-zep/llama_index/vector_stores/zep/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: Optional[str] = None, **delete_kwargs: Any) -> None:  # type: ignore
"""
    Delete a document from the collection.

    Args:
        ref_doc_id (Optional[str]): ID of the document to delete.
            Not currently supported.
        delete_kwargs: Must contain "uuid" key with UUID of the document to delete.

    """
    if not isinstance(self._collection, DocumentCollection):
        raise ValueError("Collection not initialized")

    if ref_doc_id and len(ref_doc_id)  0:
        raise NotImplementedError(
            "Delete by ref_doc_id not yet implemented for Zep."
        )

    if "uuid" in delete_kwargs:
        self._collection.delete_document(uuid=delete_kwargs["uuid"])
    else:
        raise ValueError("uuid must be specified")

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/zep/#llama_index.vector_stores.zep.ZepVectorStore.adelete "Permanent link")

```
adelete(
    ref_doc_id: Optional[] = None, **delete_kwargs: 
) -> None

```

Asynchronously delete a document from the collection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  `Optional[str]`  |  ID of the document to delete. Not currently supported.  |  `None`  |  
|  `delete_kwargs`  |  Must contain "uuid" key with UUID of the document to delete.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-zep/llama_index/vector_stores/zep/base.py`  
| 
```
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
```
 | 
```
async defadelete(
    self, ref_doc_id: Optional[str] = None, **delete_kwargs: Any
) -> None:  # type: ignore
"""
    Asynchronously delete a document from the collection.

    Args:
        ref_doc_id (Optional[str]): ID of the document to delete.
            Not currently supported.
        delete_kwargs: Must contain "uuid" key with UUID of the document to delete.

    """
    if not isinstance(self._collection, DocumentCollection):
        raise ValueError("Collection not initialized")

    if ref_doc_id and len(ref_doc_id)  0:
        raise NotImplementedError(
            "Delete by ref_doc_id not yet implemented for Zep."
        )

    if "uuid" in delete_kwargs:
        await self._collection.adelete_document(uuid=delete_kwargs["uuid"])
    else:
        raise ValueError("uuid must be specified")

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/zep/#llama_index.vector_stores.zep.ZepVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query the index for the top k most similar nodes to the given query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  Query object containing either a query string or a query embedding.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  Result of the query, containing the most similar nodes, their similarities, and their IDs.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-zep/llama_index/vector_stores/zep/base.py`  
| 
```
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
defquery(
    self,
    query: VectorStoreQuery,
    **kwargs: Any,
) -> VectorStoreQueryResult:
"""
    Query the index for the top k most similar nodes to the given query.

    Args:
        query (VectorStoreQuery): Query object containing either a query string
            or a query embedding.

    Returns:
        VectorStoreQueryResult: Result of the query, containing the most similar
            nodes, their similarities, and their IDs.

    """
    if not isinstance(self._collection, DocumentCollection):
        raise ValueError("Collection not initialized")

    if query.query_embedding is None and query.query_str is None:
        raise ValueError("query must have one of query_str or query_embedding")

    # If we have an embedding, we shouldn't use the query string
    # Zep does not allow both to be set
    if query.query_embedding:
        query.query_str = None

    metadata_filters = None
    if query.filters is not None:
        metadata_filters = self._to_zep_filters(query.filters)

    results = self._collection.search(
        text=query.query_str,
        embedding=query.query_embedding,
        metadata=metadata_filters,
        limit=query.similarity_top_k,
    )

    return self._parse_query_result(results)

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/zep/#llama_index.vector_stores.zep.ZepVectorStore.aquery "Permanent link")

```
aquery(
    query: , **kwargs: 
) -> 

```

Asynchronously query the index for the top k most similar nodes to the given query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  Query object containing either a query string or a query embedding.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  Result of the query, containing the most similar nodes, their similarities, and their IDs.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-zep/llama_index/vector_stores/zep/base.py`  
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
```
 | 
```
async defaquery(
    self,
    query: VectorStoreQuery,
    **kwargs: Any,
) -> VectorStoreQueryResult:
"""
    Asynchronously query the index for the top k most similar nodes to the
        given query.

    Args:
        query (VectorStoreQuery): Query object containing either a query string or
            a query embedding.

    Returns:
        VectorStoreQueryResult: Result of the query, containing the most similar
            nodes, their similarities, and their IDs.

    """
    if not isinstance(self._collection, DocumentCollection):
        raise ValueError("Collection not initialized")

    if query.query_embedding is None and query.query_str is None:
        raise ValueError("query must have one of query_str or query_embedding")

    # If we have an embedding, we shouldn't use the query string
    # Zep does not allow both to be set
    if query.query_embedding:
        query.query_str = None

    metadata_filters = None
    if query.filters is not None:
        metadata_filters = self._to_zep_filters(query.filters)

    results = await self._collection.asearch(
        text=query.query_str,
        embedding=query.query_embedding,
        metadata=metadata_filters,
        limit=query.similarity_top_k,
    )

    return self._parse_query_result(results)

```
 |  
| --- | --- |  
options: members: - ZepVectorStore
