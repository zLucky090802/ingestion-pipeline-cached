# Simple
Simple vector store index.
##  SimpleVectorStoreData `dataclass` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/simple/#llama_index.core.vector_stores.simple.SimpleVectorStoreData "Permanent link")
Bases: `DataClassJsonMixin`
Simple Vector Store Data container.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `embedding_dict`  |  `Dict[str, List[float]]`  |  dict mapping node_ids to embeddings.  |  `<class 'dict'>`  |  
|  `text_id_to_ref_doc_id`  |  `Dict[str, str]`  |  dict mapping text_ids/node_ids to ref_doc_ids.  |  `<class 'dict'>`  |  
|  `metadata_dict`  |  `Dict[str, Any]`  |  dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs dict(iterable) -> new dictionary initialized as if via: d = {} for k, v in iterable: d[k] = v dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list. For example: dict(one=1, two=2)  |  `<class 'dict'>`  |  
Source code in `llama-index-core/llama_index/core/vector_stores/simple.py`  
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
```
 | 
```
@dataclass
classSimpleVectorStoreData(DataClassJsonMixin):
"""
    Simple Vector Store Data container.

    Args:
        embedding_dict (Optional[dict]): dict mapping node_ids to embeddings.
        text_id_to_ref_doc_id (Optional[dict]):
            dict mapping text_ids/node_ids to ref_doc_ids.

    """

    embedding_dict: Dict[str, List[float]] = field(default_factory=dict)
    text_id_to_ref_doc_id: Dict[str, str] = field(default_factory=dict)
    metadata_dict: Dict[str, Any] = field(default_factory=dict)

```
 |  
| --- | --- |  
##  SimpleVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/simple/#llama_index.core.vector_stores.simple.SimpleVectorStore "Permanent link")
Bases: 
Simple Vector Store.
In this vector store, embeddings are stored within a simple, in-memory dictionary.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `simple_vector_store_data_dict`  |  `Optional[dict]`  |  data dict containing the embeddings and doc_ids. See SimpleVectorStoreData for more details.  |  _required_  |  
|  `stores_text`  |  `bool`  |  `False`  |  
|  `data`  |   |  Simple Vector Store Data container. Args: embedding_dict (Optional[dict]): dict mapping node_ids to embeddings. text_id_to_ref_doc_id (Optional[dict]): dict mapping text_ids/node_ids to ref_doc_ids.  |  `<dynamic>`  |  
Source code in `llama-index-core/llama_index/core/vector_stores/simple.py`  
| 
```
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
```
 | 
```
classSimpleVectorStore(BasePydanticVectorStore):
"""
    Simple Vector Store.

    In this vector store, embeddings are stored within a simple, in-memory dictionary.

    Args:
        simple_vector_store_data_dict (Optional[dict]): data dict
            containing the embeddings and doc_ids. See SimpleVectorStoreData
            for more details.

    """

    stores_text: bool = False

    data: SimpleVectorStoreData = Field(default_factory=SimpleVectorStoreData)
    _fs: fsspec.AbstractFileSystem = PrivateAttr()

    def__init__(
        self,
        data: Optional[SimpleVectorStoreData] = None,
        fs: Optional[fsspec.AbstractFileSystem] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        super().__init__(data=data or SimpleVectorStoreData())  # type: ignore[call-arg]
        self._fs = fs or fsspec.filesystem("file")

    @classmethod
    deffrom_persist_dir(
        cls,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        namespace: str = DEFAULT_VECTOR_STORE,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> "SimpleVectorStore":
"""Load from persist dir."""
        persist_fname = f"{namespace}{NAMESPACE_SEP}{DEFAULT_PERSIST_FNAME}"

        if fs is not None:
            persist_path = concat_dirs(persist_dir, persist_fname)
        else:
            persist_path = os.path.join(persist_dir, persist_fname)
        return cls.from_persist_path(persist_path, fs=fs)

    @classmethod
    deffrom_namespaced_persist_dir(
        cls,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> Dict[str, BasePydanticVectorStore]:
"""Load from namespaced persist dir."""
        listing_fn = os.listdir if fs is None else fs.listdir

        vector_stores: Dict[str, BasePydanticVectorStore] = {}

        try:
            for fname in listing_fn(persist_dir):
                if fname.endswith(DEFAULT_PERSIST_FNAME):
                    namespace = fname.split(NAMESPACE_SEP)[0]

                    # handle backwards compatibility with stores that were persisted
                    if namespace == DEFAULT_PERSIST_FNAME:
                        vector_stores[DEFAULT_VECTOR_STORE] = cls.from_persist_dir(
                            persist_dir=persist_dir, fs=fs
                        )
                    else:
                        vector_stores[namespace] = cls.from_persist_dir(
                            persist_dir=persist_dir, namespace=namespace, fs=fs
                        )
        except Exception:
            # failed to listdir, so assume there is only one store
            try:
                vector_stores[DEFAULT_VECTOR_STORE] = cls.from_persist_dir(
                    persist_dir=persist_dir, fs=fs, namespace=DEFAULT_VECTOR_STORE
                )
            except Exception:
                # no namespace backwards compat
                vector_stores[DEFAULT_VECTOR_STORE] = cls.from_persist_dir(
                    persist_dir=persist_dir, fs=fs
                )

        return vector_stores

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "SimpleVectorStore"

    @property
    defclient(self) -> None:
"""Get client."""
        return

    @property
    def_data(self) -> SimpleVectorStoreData:
"""Backwards compatibility."""
        return self.data

    defget(self, text_id: str) -> List[float]:
"""Get embedding."""
        return self.data.embedding_dict[text_id]

    defget_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
    ) -> List[BaseNode]:
"""Get nodes."""
        raise NotImplementedError("SimpleVectorStore does not store nodes directly.")

    defadd(
        self,
        nodes: Sequence[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""Add nodes to index."""
        for node in nodes:
            self.data.embedding_dict[node.node_id] = node.get_embedding()
            self.data.text_id_to_ref_doc_id[node.node_id] = node.ref_doc_id or "None"

            metadata = node_to_metadata_dict(
                node, remove_text=True, flat_metadata=False
            )
            metadata.pop("_node_content", None)
            self.data.metadata_dict[node.node_id] = metadata
        return [node.node_id for node in nodes]

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        text_ids_to_delete = set()
        for text_id, ref_doc_id_ in self.data.text_id_to_ref_doc_id.items():
            if ref_doc_id == ref_doc_id_:
                text_ids_to_delete.add(text_id)

        for text_id in text_ids_to_delete:
            del self.data.embedding_dict[text_id]
            del self.data.text_id_to_ref_doc_id[text_id]
            # Handle metadata_dict not being present in stores that were persisted
            # without metadata, or, not being present for nodes stored
            # prior to metadata functionality.
            if self.data.metadata_dict is not None:
                self.data.metadata_dict.pop(text_id, None)

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
        filter_fn = build_metadata_filter_fn(
            lambda node_id: self.data.metadata_dict[node_id], filters
        )

        if node_ids is not None:
            node_id_set = set(node_ids)

            defnode_filter_fn(node_id: str) -> bool:
                return node_id in node_id_set and filter_fn(node_id)

        else:

            defnode_filter_fn(node_id: str) -> bool:
                return filter_fn(node_id)

        for node_id in list(self.data.embedding_dict.keys()):
            if node_filter_fn(node_id):
                del self.data.embedding_dict[node_id]
                del self.data.text_id_to_ref_doc_id[node_id]
                self.data.metadata_dict.pop(node_id, None)

    defclear(self) -> None:
"""Clear the store."""
        self.data = SimpleVectorStoreData()

    defquery(
        self,
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""Get nodes for response."""
        # Prevent metadata filtering on stores that were persisted without metadata.
        if (
            query.filters is not None
            and self.data.embedding_dict
            and not self.data.metadata_dict
        ):
            raise ValueError(
                "Cannot filter stores that were persisted without metadata. "
                "Please rebuild the store with metadata to enable filtering."
            )
        # Prefilter nodes based on the query filter and node ID restrictions.
        query_filter_fn = build_metadata_filter_fn(
            lambda node_id: self.data.metadata_dict[node_id], query.filters
        )

        if query.node_ids is not None:
            available_ids = set(query.node_ids)

            defnode_filter_fn(node_id: str) -> bool:
                return node_id in available_ids

        else:

            defnode_filter_fn(node_id: str) -> bool:
                return True

        node_ids = []
        embeddings = []
        # TODO: consolidate with get_query_text_embedding_similarities
        for node_id, embedding in self.data.embedding_dict.items():
            if node_filter_fn(node_id) and query_filter_fn(node_id):
                node_ids.append(node_id)
                embeddings.append(embedding)

        query_embedding = cast(List[float], query.query_embedding)

        if query.mode in LEARNER_MODES:
            top_similarities, top_ids = get_top_k_embeddings_learner(
                query_embedding,
                embeddings,
                similarity_top_k=query.similarity_top_k,
                embedding_ids=node_ids,
            )
        elif query.mode == MMR_MODE:
            mmr_threshold = kwargs.get("mmr_threshold")
            top_similarities, top_ids = get_top_k_mmr_embeddings(
                query_embedding,
                embeddings,
                similarity_top_k=query.similarity_top_k,
                embedding_ids=node_ids,
                mmr_threshold=mmr_threshold,
            )
        elif query.mode == VectorStoreQueryMode.DEFAULT:
            top_similarities, top_ids = get_top_k_embeddings(
                query_embedding,
                embeddings,
                similarity_top_k=query.similarity_top_k,
                embedding_ids=node_ids,
            )
        else:
            raise ValueError(f"Invalid query mode: {query.mode}")

        return VectorStoreQueryResult(
            similarities=top_similarities,
            ids=top_ids,
        )

    defpersist(
        self,
        persist_path: str = os.path.join(DEFAULT_PERSIST_DIR, DEFAULT_PERSIST_FNAME),
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> None:
"""Persist the SimpleVectorStore to a directory."""
        fs = fs or self._fs
        dirpath = os.path.dirname(persist_path)
        if not fs.exists(dirpath):
            fs.makedirs(dirpath)

        with fs.open(persist_path, "w") as f:
            json.dump(self.data.to_dict(), f)

    @classmethod
    deffrom_persist_path(
        cls, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
    ) -> "SimpleVectorStore":
"""Create a SimpleKVStore from a persist directory."""
        fs = fs or fsspec.filesystem("file")
        if not fs.exists(persist_path):
            raise ValueError(
                f"No existing {__name__} found at {persist_path}, skipping load."
            )

        logger.debug(f"Loading {__name__} from {persist_path}.")
        with fs.open(persist_path, "rb") as f:
            data_dict = json.load(f)
            data = SimpleVectorStoreData.from_dict(data_dict)
        return cls(data)

    @classmethod
    deffrom_dict(cls, data: Dict[str, Any], **kwargs: Any) -> "SimpleVectorStore":
        save_data = SimpleVectorStoreData.from_dict(data)
        return cls(save_data)

    defto_dict(self, **kwargs: Any) -> Dict[str, Any]:
        return self.data.to_dict()

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/simple/#llama_index.core.vector_stores.simple.SimpleVectorStore.client "Permanent link")

```
client: None

```

Get client.
###  from_persist_dir `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/simple/#llama_index.core.vector_stores.simple.SimpleVectorStore.from_persist_dir "Permanent link")

```
from_persist_dir(
    persist_dir:  = DEFAULT_PERSIST_DIR,
    namespace:  = DEFAULT_VECTOR_STORE,
    fs: Optional[AbstractFileSystem] = None,
) -> 

```

Load from persist dir.
Source code in `llama-index-core/llama_index/core/vector_stores/simple.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_persist_dir(
    cls,
    persist_dir: str = DEFAULT_PERSIST_DIR,
    namespace: str = DEFAULT_VECTOR_STORE,
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> "SimpleVectorStore":
"""Load from persist dir."""
    persist_fname = f"{namespace}{NAMESPACE_SEP}{DEFAULT_PERSIST_FNAME}"

    if fs is not None:
        persist_path = concat_dirs(persist_dir, persist_fname)
    else:
        persist_path = os.path.join(persist_dir, persist_fname)
    return cls.from_persist_path(persist_path, fs=fs)

```
 |  
| --- | --- |  
###  from_namespaced_persist_dir `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/simple/#llama_index.core.vector_stores.simple.SimpleVectorStore.from_namespaced_persist_dir "Permanent link")

```
from_namespaced_persist_dir(
    persist_dir:  = DEFAULT_PERSIST_DIR,
    fs: Optional[AbstractFileSystem] = None,
) -> [, ]

```

Load from namespaced persist dir.
Source code in `llama-index-core/llama_index/core/vector_stores/simple.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_namespaced_persist_dir(
    cls,
    persist_dir: str = DEFAULT_PERSIST_DIR,
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> Dict[str, BasePydanticVectorStore]:
"""Load from namespaced persist dir."""
    listing_fn = os.listdir if fs is None else fs.listdir

    vector_stores: Dict[str, BasePydanticVectorStore] = {}

    try:
        for fname in listing_fn(persist_dir):
            if fname.endswith(DEFAULT_PERSIST_FNAME):
                namespace = fname.split(NAMESPACE_SEP)[0]

                # handle backwards compatibility with stores that were persisted
                if namespace == DEFAULT_PERSIST_FNAME:
                    vector_stores[DEFAULT_VECTOR_STORE] = cls.from_persist_dir(
                        persist_dir=persist_dir, fs=fs
                    )
                else:
                    vector_stores[namespace] = cls.from_persist_dir(
                        persist_dir=persist_dir, namespace=namespace, fs=fs
                    )
    except Exception:
        # failed to listdir, so assume there is only one store
        try:
            vector_stores[DEFAULT_VECTOR_STORE] = cls.from_persist_dir(
                persist_dir=persist_dir, fs=fs, namespace=DEFAULT_VECTOR_STORE
            )
        except Exception:
            # no namespace backwards compat
            vector_stores[DEFAULT_VECTOR_STORE] = cls.from_persist_dir(
                persist_dir=persist_dir, fs=fs
            )

    return vector_stores

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/simple/#llama_index.core.vector_stores.simple.SimpleVectorStore.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/vector_stores/simple.py`  
| 
```
147
148
149
150
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "SimpleVectorStore"

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/simple/#llama_index.core.vector_stores.simple.SimpleVectorStore.get "Permanent link")

```
get(text_id: ) -> [float]

```

Get embedding.
Source code in `llama-index-core/llama_index/core/vector_stores/simple.py`  
| 
```
162
163
164
```
 | 
```
defget(self, text_id: str) -> List[float]:
"""Get embedding."""
    return self.data.embedding_dict[text_id]

```
 |  
| --- | --- |  
###  get_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/simple/#llama_index.core.vector_stores.simple.SimpleVectorStore.get_nodes "Permanent link")

```
get_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
) -> []

```

Get nodes.
Source code in `llama-index-core/llama_index/core/vector_stores/simple.py`  
| 
```
166
167
168
169
170
171
172
```
 | 
```
defget_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
) -> List[BaseNode]:
"""Get nodes."""
    raise NotImplementedError("SimpleVectorStore does not store nodes directly.")

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/simple/#llama_index.core.vector_stores.simple.SimpleVectorStore.add "Permanent link")

```
add(
    nodes: Sequence[], **add_kwargs: 
) -> []

```

Add nodes to index.
Source code in `llama-index-core/llama_index/core/vector_stores/simple.py`  
| 
```
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
```
 | 
```
defadd(
    self,
    nodes: Sequence[BaseNode],
    **add_kwargs: Any,
) -> List[str]:
"""Add nodes to index."""
    for node in nodes:
        self.data.embedding_dict[node.node_id] = node.get_embedding()
        self.data.text_id_to_ref_doc_id[node.node_id] = node.ref_doc_id or "None"

        metadata = node_to_metadata_dict(
            node, remove_text=True, flat_metadata=False
        )
        metadata.pop("_node_content", None)
        self.data.metadata_dict[node.node_id] = metadata
    return [node.node_id for node in nodes]

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/simple/#llama_index.core.vector_stores.simple.SimpleVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/vector_stores/simple.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    text_ids_to_delete = set()
    for text_id, ref_doc_id_ in self.data.text_id_to_ref_doc_id.items():
        if ref_doc_id == ref_doc_id_:
            text_ids_to_delete.add(text_id)

    for text_id in text_ids_to_delete:
        del self.data.embedding_dict[text_id]
        del self.data.text_id_to_ref_doc_id[text_id]
        # Handle metadata_dict not being present in stores that were persisted
        # without metadata, or, not being present for nodes stored
        # prior to metadata functionality.
        if self.data.metadata_dict is not None:
            self.data.metadata_dict.pop(text_id, None)

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/simple/#llama_index.core.vector_stores.simple.SimpleVectorStore.clear "Permanent link")

```
clear() -> None

```

Clear the store.
Source code in `llama-index-core/llama_index/core/vector_stores/simple.py`  
| 
```
240
241
242
```
 | 
```
defclear(self) -> None:
"""Clear the store."""
    self.data = SimpleVectorStoreData()

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/simple/#llama_index.core.vector_stores.simple.SimpleVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Get nodes for response.
Source code in `llama-index-core/llama_index/core/vector_stores/simple.py`  
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
```
 | 
```
defquery(
    self,
    query: VectorStoreQuery,
    **kwargs: Any,
) -> VectorStoreQueryResult:
"""Get nodes for response."""
    # Prevent metadata filtering on stores that were persisted without metadata.
    if (
        query.filters is not None
        and self.data.embedding_dict
        and not self.data.metadata_dict
    ):
        raise ValueError(
            "Cannot filter stores that were persisted without metadata. "
            "Please rebuild the store with metadata to enable filtering."
        )
    # Prefilter nodes based on the query filter and node ID restrictions.
    query_filter_fn = build_metadata_filter_fn(
        lambda node_id: self.data.metadata_dict[node_id], query.filters
    )

    if query.node_ids is not None:
        available_ids = set(query.node_ids)

        defnode_filter_fn(node_id: str) -> bool:
            return node_id in available_ids

    else:

        defnode_filter_fn(node_id: str) -> bool:
            return True

    node_ids = []
    embeddings = []
    # TODO: consolidate with get_query_text_embedding_similarities
    for node_id, embedding in self.data.embedding_dict.items():
        if node_filter_fn(node_id) and query_filter_fn(node_id):
            node_ids.append(node_id)
            embeddings.append(embedding)

    query_embedding = cast(List[float], query.query_embedding)

    if query.mode in LEARNER_MODES:
        top_similarities, top_ids = get_top_k_embeddings_learner(
            query_embedding,
            embeddings,
            similarity_top_k=query.similarity_top_k,
            embedding_ids=node_ids,
        )
    elif query.mode == MMR_MODE:
        mmr_threshold = kwargs.get("mmr_threshold")
        top_similarities, top_ids = get_top_k_mmr_embeddings(
            query_embedding,
            embeddings,
            similarity_top_k=query.similarity_top_k,
            embedding_ids=node_ids,
            mmr_threshold=mmr_threshold,
        )
    elif query.mode == VectorStoreQueryMode.DEFAULT:
        top_similarities, top_ids = get_top_k_embeddings(
            query_embedding,
            embeddings,
            similarity_top_k=query.similarity_top_k,
            embedding_ids=node_ids,
        )
    else:
        raise ValueError(f"Invalid query mode: {query.mode}")

    return VectorStoreQueryResult(
        similarities=top_similarities,
        ids=top_ids,
    )

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/simple/#llama_index.core.vector_stores.simple.SimpleVectorStore.persist "Permanent link")

```
persist(
    persist_path:  = (
        DEFAULT_PERSIST_DIR, DEFAULT_PERSIST_FNAME
    ),
    fs: Optional[AbstractFileSystem] = None,
) -> None

```

Persist the SimpleVectorStore to a directory.
Source code in `llama-index-core/llama_index/core/vector_stores/simple.py`  
| 
```
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
```
 | 
```
defpersist(
    self,
    persist_path: str = os.path.join(DEFAULT_PERSIST_DIR, DEFAULT_PERSIST_FNAME),
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> None:
"""Persist the SimpleVectorStore to a directory."""
    fs = fs or self._fs
    dirpath = os.path.dirname(persist_path)
    if not fs.exists(dirpath):
        fs.makedirs(dirpath)

    with fs.open(persist_path, "w") as f:
        json.dump(self.data.to_dict(), f)

```
 |  
| --- | --- |  
###  from_persist_path `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/simple/#llama_index.core.vector_stores.simple.SimpleVectorStore.from_persist_path "Permanent link")

```
from_persist_path(
    persist_path: ,
    fs: Optional[AbstractFileSystem] = None,
) -> 

```

Create a SimpleKVStore from a persist directory.
Source code in `llama-index-core/llama_index/core/vector_stores/simple.py`  
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
```
 | 
```
@classmethod
deffrom_persist_path(
    cls, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
) -> "SimpleVectorStore":
"""Create a SimpleKVStore from a persist directory."""
    fs = fs or fsspec.filesystem("file")
    if not fs.exists(persist_path):
        raise ValueError(
            f"No existing {__name__} found at {persist_path}, skipping load."
        )

    logger.debug(f"Loading {__name__} from {persist_path}.")
    with fs.open(persist_path, "rb") as f:
        data_dict = json.load(f)
        data = SimpleVectorStoreData.from_dict(data_dict)
    return cls(data)

```
 |  
| --- | --- |  
options: members: - SimpleVectorStore
