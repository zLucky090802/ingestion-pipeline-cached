# Storage context
##  StorageContext `dataclass` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.storage.storage_context.StorageContext "Permanent link")
Storage context.
The storage context container is a utility container for storing nodes, indices, and vectors. It contains the following: - docstore: BaseDocumentStore - index_store: BaseIndexStore - vector_store: BasePydanticVectorStore - graph_store: GraphStore - property_graph_store: PropertyGraphStore (lazily initialized)
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `docstore`  |   |  _required_  |  
|  `index_store`  |   |  _required_  |  
|  `vector_stores`  |  `Dict[str, Annotated[BasePydanticVectorStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore "BasePydanticVectorStore \(llama_index.core.vector_stores.types.BasePydanticVectorStore\)"), SerializeAsAny]]`  |  _required_  |  
|  `graph_store`  |   |  _required_  |  
|  `property_graph_store`  |  `PropertyGraphStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore "PropertyGraphStore \(llama_index.core.graph_stores.types.PropertyGraphStore\)") | None`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/storage/storage_context.py`  
| 
```
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
```
 | 
```
@dataclass
classStorageContext:
"""
    Storage context.

    The storage context container is a utility container for storing nodes,
    indices, and vectors. It contains the following:
    - docstore: BaseDocumentStore
    - index_store: BaseIndexStore
    - vector_store: BasePydanticVectorStore
    - graph_store: GraphStore
    - property_graph_store: PropertyGraphStore (lazily initialized)

    """

    docstore: BaseDocumentStore
    index_store: BaseIndexStore
    vector_stores: Dict[str, SerializeAsAny[BasePydanticVectorStore]]
    graph_store: GraphStore
    property_graph_store: Optional[PropertyGraphStore] = None

    @classmethod
    deffrom_defaults(
        cls,
        docstore: Optional[BaseDocumentStore] = None,
        index_store: Optional[BaseIndexStore] = None,
        vector_store: Optional[BasePydanticVectorStore] = None,
        image_store: Optional[BasePydanticVectorStore] = None,
        vector_stores: Optional[Dict[str, BasePydanticVectorStore]] = None,
        graph_store: Optional[GraphStore] = None,
        property_graph_store: Optional[PropertyGraphStore] = None,
        persist_dir: Optional[str] = None,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> "StorageContext":
"""
        Create a StorageContext from defaults.

        Args:
            docstore (Optional[BaseDocumentStore]): document store
            index_store (Optional[BaseIndexStore]): index store
            vector_store (Optional[BasePydanticVectorStore]): vector store
            graph_store (Optional[GraphStore]): graph store
            image_store (Optional[BasePydanticVectorStore]): image store

        """
        if persist_dir is None:
            docstore = docstore or SimpleDocumentStore()
            index_store = index_store or SimpleIndexStore()
            graph_store = graph_store or SimpleGraphStore()
            image_store = image_store or SimpleVectorStore()

            if vector_store:
                vector_stores = {DEFAULT_VECTOR_STORE: vector_store}
            else:
                vector_stores = vector_stores or {
                    DEFAULT_VECTOR_STORE: SimpleVectorStore()
                }
            if image_store:
                # append image store to vector stores
                vector_stores[IMAGE_VECTOR_STORE_NAMESPACE] = image_store
        else:
            docstore = docstore or SimpleDocumentStore.from_persist_dir(
                persist_dir, fs=fs
            )
            index_store = index_store or SimpleIndexStore.from_persist_dir(
                persist_dir, fs=fs
            )
            graph_store = graph_store or SimpleGraphStore.from_persist_dir(
                persist_dir, fs=fs
            )

            try:
                property_graph_store = (
                    property_graph_store
                    or SimplePropertyGraphStore.from_persist_dir(persist_dir, fs=fs)
                )
            except FileNotFoundError:
                property_graph_store = None

            if vector_store:
                vector_stores = {DEFAULT_VECTOR_STORE: vector_store}
            elif vector_stores:
                vector_stores = vector_stores
            else:
                vector_stores = SimpleVectorStore.from_namespaced_persist_dir(
                    persist_dir, fs=fs
                )
            if image_store:
                # append image store to vector stores
                vector_stores[IMAGE_VECTOR_STORE_NAMESPACE] = image_store  # type: ignore

        return cls(
            docstore=docstore,
            index_store=index_store,
            vector_stores=vector_stores,  # type: ignore
            graph_store=graph_store,
            property_graph_store=property_graph_store,
        )

    defpersist(
        self,
        persist_dir: Union[str, os.PathLike] = DEFAULT_PERSIST_DIR,
        docstore_fname: str = DOCSTORE_FNAME,
        index_store_fname: str = INDEX_STORE_FNAME,
        vector_store_fname: str = VECTOR_STORE_FNAME,
        image_store_fname: str = IMAGE_STORE_FNAME,
        graph_store_fname: str = GRAPH_STORE_FNAME,
        pg_graph_store_fname: str = PG_FNAME,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> None:
"""
        Persist the storage context.

        Args:
            persist_dir (str): directory to persist the storage context

        """
        if fs is not None:
            persist_dir = str(persist_dir)  # NOTE: doesn't support Windows here
            docstore_path = concat_dirs(persist_dir, docstore_fname)
            index_store_path = concat_dirs(persist_dir, index_store_fname)
            graph_store_path = concat_dirs(persist_dir, graph_store_fname)
            pg_graph_store_path = concat_dirs(persist_dir, pg_graph_store_fname)
        else:
            persist_dir = Path(persist_dir)
            docstore_path = str(persist_dir / docstore_fname)
            index_store_path = str(persist_dir / index_store_fname)
            graph_store_path = str(persist_dir / graph_store_fname)
            pg_graph_store_path = str(persist_dir / pg_graph_store_fname)

        self.docstore.persist(persist_path=docstore_path, fs=fs)
        self.index_store.persist(persist_path=index_store_path, fs=fs)
        self.graph_store.persist(persist_path=graph_store_path, fs=fs)

        if self.property_graph_store:
            self.property_graph_store.persist(persist_path=pg_graph_store_path, fs=fs)

        # save each vector store under it's namespace
        for vector_store_name, vector_store in self.vector_stores.items():
            if fs is not None:
                vector_store_path = concat_dirs(
                    str(persist_dir),
                    f"{vector_store_name}{NAMESPACE_SEP}{vector_store_fname}",
                )
            else:
                vector_store_path = str(
                    Path(persist_dir)
                    / f"{vector_store_name}{NAMESPACE_SEP}{vector_store_fname}"
                )

            vector_store.persist(persist_path=vector_store_path, fs=fs)

    defto_dict(self) -> dict:
        all_simple = (
            isinstance(self.docstore, SimpleDocumentStore)
            and isinstance(self.index_store, SimpleIndexStore)
            and isinstance(self.graph_store, SimpleGraphStore)
            and isinstance(
                self.property_graph_store, (SimplePropertyGraphStore, type(None))
            )
            and all(
                isinstance(vs, SimpleVectorStore) for vs in self.vector_stores.values()
            )
        )
        if not all_simple:
            raise ValueError(
                "to_dict only available when using simple doc/index/vector stores"
            )

        assert isinstance(self.docstore, SimpleDocumentStore)
        assert isinstance(self.index_store, SimpleIndexStore)
        assert isinstance(self.graph_store, SimpleGraphStore)
        assert isinstance(
            self.property_graph_store, (SimplePropertyGraphStore, type(None))
        )

        return {
            VECTOR_STORE_KEY: {
                key: vector_store.to_dict()
                for key, vector_store in self.vector_stores.items()
                if isinstance(vector_store, SimpleVectorStore)
            },
            DOC_STORE_KEY: self.docstore.to_dict(),
            INDEX_STORE_KEY: self.index_store.to_dict(),
            GRAPH_STORE_KEY: self.graph_store.to_dict(),
            PG_STORE_KEY: (
                self.property_graph_store.to_dict()
                if self.property_graph_store
                else None
            ),
        }

    @classmethod
    deffrom_dict(cls, save_dict: dict) -> "StorageContext":
"""Create a StorageContext from dict."""
        docstore = SimpleDocumentStore.from_dict(save_dict[DOC_STORE_KEY])
        index_store = SimpleIndexStore.from_dict(save_dict[INDEX_STORE_KEY])
        graph_store = SimpleGraphStore.from_dict(save_dict[GRAPH_STORE_KEY])
        property_graph_store = (
            SimplePropertyGraphStore.from_dict(save_dict[PG_STORE_KEY])
            if save_dict[PG_STORE_KEY]
            else None
        )

        vector_stores: Dict[str, BasePydanticVectorStore] = {}
        for key, vector_store_dict in save_dict[VECTOR_STORE_KEY].items():
            vector_stores[key] = SimpleVectorStore.from_dict(vector_store_dict)

        return cls(
            docstore=docstore,
            index_store=index_store,
            vector_stores=vector_stores,
            graph_store=graph_store,
            property_graph_store=property_graph_store,
        )

    @property
    defvector_store(self) -> BasePydanticVectorStore:
"""Backwrds compatibility for vector_store property."""
        return self.vector_stores[DEFAULT_VECTOR_STORE]

    defadd_vector_store(
        self, vector_store: BasePydanticVectorStore, namespace: str
    ) -> None:
"""Add a vector store to the storage context."""
        self.vector_stores[namespace] = vector_store

```
 |  
| --- | --- |  
###  vector_store `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.storage.storage_context.StorageContext.vector_store "Permanent link")

```
vector_store: 

```

Backwrds compatibility for vector_store property.
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.storage.storage_context.StorageContext.from_defaults "Permanent link")

```
from_defaults(
    docstore: Optional[] = None,
    index_store: Optional[] = None,
    vector_store: Optional[] = None,
    image_store: Optional[] = None,
    vector_stores: Optional[
        [, ]
    ] = None,
    graph_store: Optional[] = None,
    property_graph_store: Optional[
        
    ] = None,
    persist_dir: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> 

```

Create a StorageContext from defaults.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `docstore`  |  `Optional[BaseDocumentStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/#llama_index.core.storage.docstore.types.BaseDocumentStore "BaseDocumentStore \(llama_index.core.storage.docstore.types.BaseDocumentStore\)")]`  |  document store  |  `None`  |  
|  `index_store`  |  `Optional[BaseIndexStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/#llama_index.core.storage.index_store.types.BaseIndexStore "BaseIndexStore \(llama_index.core.storage.index_store.types.BaseIndexStore\)")]`  |  index store  |  `None`  |  
|  `vector_store`  |  `Optional[BasePydanticVectorStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore "BasePydanticVectorStore \(llama_index.core.vector_stores.types.BasePydanticVectorStore\)")]`  |  vector store  |  `None`  |  
|  `graph_store`  |  `Optional[GraphStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.GraphStore "GraphStore \(llama_index.core.graph_stores.types.GraphStore\)")]`  |  graph store  |  `None`  |  
|  `image_store`  |  `Optional[BasePydanticVectorStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore "BasePydanticVectorStore \(llama_index.core.vector_stores.types.BasePydanticVectorStore\)")]`  |  image store  |  `None`  |  
Source code in `llama-index-core/llama_index/core/storage/storage_context.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    docstore: Optional[BaseDocumentStore] = None,
    index_store: Optional[BaseIndexStore] = None,
    vector_store: Optional[BasePydanticVectorStore] = None,
    image_store: Optional[BasePydanticVectorStore] = None,
    vector_stores: Optional[Dict[str, BasePydanticVectorStore]] = None,
    graph_store: Optional[GraphStore] = None,
    property_graph_store: Optional[PropertyGraphStore] = None,
    persist_dir: Optional[str] = None,
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> "StorageContext":
"""
    Create a StorageContext from defaults.

    Args:
        docstore (Optional[BaseDocumentStore]): document store
        index_store (Optional[BaseIndexStore]): index store
        vector_store (Optional[BasePydanticVectorStore]): vector store
        graph_store (Optional[GraphStore]): graph store
        image_store (Optional[BasePydanticVectorStore]): image store

    """
    if persist_dir is None:
        docstore = docstore or SimpleDocumentStore()
        index_store = index_store or SimpleIndexStore()
        graph_store = graph_store or SimpleGraphStore()
        image_store = image_store or SimpleVectorStore()

        if vector_store:
            vector_stores = {DEFAULT_VECTOR_STORE: vector_store}
        else:
            vector_stores = vector_stores or {
                DEFAULT_VECTOR_STORE: SimpleVectorStore()
            }
        if image_store:
            # append image store to vector stores
            vector_stores[IMAGE_VECTOR_STORE_NAMESPACE] = image_store
    else:
        docstore = docstore or SimpleDocumentStore.from_persist_dir(
            persist_dir, fs=fs
        )
        index_store = index_store or SimpleIndexStore.from_persist_dir(
            persist_dir, fs=fs
        )
        graph_store = graph_store or SimpleGraphStore.from_persist_dir(
            persist_dir, fs=fs
        )

        try:
            property_graph_store = (
                property_graph_store
                or SimplePropertyGraphStore.from_persist_dir(persist_dir, fs=fs)
            )
        except FileNotFoundError:
            property_graph_store = None

        if vector_store:
            vector_stores = {DEFAULT_VECTOR_STORE: vector_store}
        elif vector_stores:
            vector_stores = vector_stores
        else:
            vector_stores = SimpleVectorStore.from_namespaced_persist_dir(
                persist_dir, fs=fs
            )
        if image_store:
            # append image store to vector stores
            vector_stores[IMAGE_VECTOR_STORE_NAMESPACE] = image_store  # type: ignore

    return cls(
        docstore=docstore,
        index_store=index_store,
        vector_stores=vector_stores,  # type: ignore
        graph_store=graph_store,
        property_graph_store=property_graph_store,
    )

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.storage.storage_context.StorageContext.persist "Permanent link")

```
persist(
    persist_dir: Union[, PathLike] = DEFAULT_PERSIST_DIR,
    docstore_fname:  = DEFAULT_PERSIST_FNAME,
    index_store_fname:  = DEFAULT_PERSIST_FNAME,
    vector_store_fname:  = DEFAULT_PERSIST_FNAME,
    image_store_fname:  = IMAGE_STORE_FNAME,
    graph_store_fname:  = DEFAULT_PERSIST_FNAME,
    pg_graph_store_fname:  = DEFAULT_PG_PERSIST_FNAME,
    fs: Optional[AbstractFileSystem] = None,
) -> None

```

Persist the storage context.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `persist_dir`  |  directory to persist the storage context  |  `DEFAULT_PERSIST_DIR`  |  
Source code in `llama-index-core/llama_index/core/storage/storage_context.py`  
| 
```
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
```
 | 
```
defpersist(
    self,
    persist_dir: Union[str, os.PathLike] = DEFAULT_PERSIST_DIR,
    docstore_fname: str = DOCSTORE_FNAME,
    index_store_fname: str = INDEX_STORE_FNAME,
    vector_store_fname: str = VECTOR_STORE_FNAME,
    image_store_fname: str = IMAGE_STORE_FNAME,
    graph_store_fname: str = GRAPH_STORE_FNAME,
    pg_graph_store_fname: str = PG_FNAME,
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> None:
"""
    Persist the storage context.

    Args:
        persist_dir (str): directory to persist the storage context

    """
    if fs is not None:
        persist_dir = str(persist_dir)  # NOTE: doesn't support Windows here
        docstore_path = concat_dirs(persist_dir, docstore_fname)
        index_store_path = concat_dirs(persist_dir, index_store_fname)
        graph_store_path = concat_dirs(persist_dir, graph_store_fname)
        pg_graph_store_path = concat_dirs(persist_dir, pg_graph_store_fname)
    else:
        persist_dir = Path(persist_dir)
        docstore_path = str(persist_dir / docstore_fname)
        index_store_path = str(persist_dir / index_store_fname)
        graph_store_path = str(persist_dir / graph_store_fname)
        pg_graph_store_path = str(persist_dir / pg_graph_store_fname)

    self.docstore.persist(persist_path=docstore_path, fs=fs)
    self.index_store.persist(persist_path=index_store_path, fs=fs)
    self.graph_store.persist(persist_path=graph_store_path, fs=fs)

    if self.property_graph_store:
        self.property_graph_store.persist(persist_path=pg_graph_store_path, fs=fs)

    # save each vector store under it's namespace
    for vector_store_name, vector_store in self.vector_stores.items():
        if fs is not None:
            vector_store_path = concat_dirs(
                str(persist_dir),
                f"{vector_store_name}{NAMESPACE_SEP}{vector_store_fname}",
            )
        else:
            vector_store_path = str(
                Path(persist_dir)
                / f"{vector_store_name}{NAMESPACE_SEP}{vector_store_fname}"
            )

        vector_store.persist(persist_path=vector_store_path, fs=fs)

```
 |  
| --- | --- |  
###  from_dict `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.storage.storage_context.StorageContext.from_dict "Permanent link")

```
from_dict(save_dict: ) -> 

```

Create a StorageContext from dict.
Source code in `llama-index-core/llama_index/core/storage/storage_context.py`  
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
```
 | 
```
@classmethod
deffrom_dict(cls, save_dict: dict) -> "StorageContext":
"""Create a StorageContext from dict."""
    docstore = SimpleDocumentStore.from_dict(save_dict[DOC_STORE_KEY])
    index_store = SimpleIndexStore.from_dict(save_dict[INDEX_STORE_KEY])
    graph_store = SimpleGraphStore.from_dict(save_dict[GRAPH_STORE_KEY])
    property_graph_store = (
        SimplePropertyGraphStore.from_dict(save_dict[PG_STORE_KEY])
        if save_dict[PG_STORE_KEY]
        else None
    )

    vector_stores: Dict[str, BasePydanticVectorStore] = {}
    for key, vector_store_dict in save_dict[VECTOR_STORE_KEY].items():
        vector_stores[key] = SimpleVectorStore.from_dict(vector_store_dict)

    return cls(
        docstore=docstore,
        index_store=index_store,
        vector_stores=vector_stores,
        graph_store=graph_store,
        property_graph_store=property_graph_store,
    )

```
 |  
| --- | --- |  
###  add_vector_store [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.storage.storage_context.StorageContext.add_vector_store "Permanent link")

```
add_vector_store(
    vector_store: , namespace: 
) -> None

```

Add a vector store to the storage context.
Source code in `llama-index-core/llama_index/core/storage/storage_context.py`  
| 
```
273
274
275
276
277
```
 | 
```
defadd_vector_store(
    self, vector_store: BasePydanticVectorStore, namespace: str
) -> None:
"""Add a vector store to the storage context."""
    self.vector_stores[namespace] = vector_store

```
 |  
| --- | --- |  
options: members: - StorageContext
Top-level imports for LlamaIndex.
##  Response `dataclass` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Response "Permanent link")
Response object.
Returned if streaming=False.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `response`  |  `str | None`  |  _required_  |  
|  `source_nodes`  |  `List[NodeWithScore[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.NodeWithScore "NodeWithScore \(llama_index.core.schema.NodeWithScore\)")]`  |  Built-in mutable sequence. If no argument is given, the constructor creates a new empty list. The argument must be an iterable if specified.  |  `<dynamic>`  |  
|  `metadata`  |  `Dict[str, Any] | None`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/base/response/schema.py`  
| 
```
14
15
16
17
18
19
20
21
22
23
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
```
 | 
```
@dataclass
classResponse:
"""
    Response object.

    Returned if streaming=False.

    Attributes:
        response: The response text.

    """

    response: Optional[str]
    source_nodes: List[NodeWithScore] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None

    def__str__(self) -> str:
"""Convert to string representation."""
        return self.response or "None"

    defget_formatted_sources(self, length: int = 100) -> str:
"""Get formatted sources text."""
        texts = []
        for source_node in self.source_nodes:
            fmt_text_chunk = truncate_text(source_node.node.get_content(), length)
            doc_id = source_node.node.node_id or "None"
            source_text = f"> Source (Doc id: {doc_id}): {fmt_text_chunk}"
            texts.append(source_text)
        return "\n\n".join(texts)

```
 |  
| --- | --- |  
###  get_formatted_sources [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Response.get_formatted_sources "Permanent link")

```
get_formatted_sources(length:  = 100) -> 

```

Get formatted sources text.
Source code in `llama-index-core/llama_index/core/base/response/schema.py`  
| 
```
34
35
36
37
38
39
40
41
42
```
 | 
```
defget_formatted_sources(self, length: int = 100) -> str:
"""Get formatted sources text."""
    texts = []
    for source_node in self.source_nodes:
        fmt_text_chunk = truncate_text(source_node.node.get_content(), length)
        doc_id = source_node.node.node_id or "None"
        source_text = f"> Source (Doc id: {doc_id}): {fmt_text_chunk}"
        texts.append(source_text)
    return "\n\n".join(texts)

```
 |  
| --- | --- |  
##  IndexStructType [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.IndexStructType "Permanent link")
Bases: `str`, `Enum`
Index struct type. Identifier for a "type" of index.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `TREE`  |  `tree`  |  Tree index. See :ref:`Ref-Indices-Tree` for tree indices.  |  
| `LIST`  |  `list`  |  Summary index. See :ref:`Ref-Indices-List` for summary indices.  |  
| `KEYWORD_TABLE`  |  `keyword_table`  |  Keyword table index. See :ref:`Ref-Indices-Table` for keyword table indices.  |  
| `DICT`  |  `dict`  |  Faiss Vector Store Index. See :ref:`Ref-Indices-VectorStore` for more information on the faiss vector store index.  |  
| `SIMPLE_DICT`  |  `simple_dict`  |  Simple Vector Store Index. See :ref:`Ref-Indices-VectorStore` for more information on the simple vector store index.  |  
| `WEAVIATE`  |  `weaviate`  |  Weaviate Vector Store Index. See :ref:`Ref-Indices-VectorStore` for more information on the Weaviate vector store index.  |  
| `PINECONE`  |  `pinecone`  |  Pinecone Vector Store Index. See :ref:`Ref-Indices-VectorStore` for more information on the Pinecone vector store index.  |  
| `DEEPLAKE`  |  `deeplake`  |  DeepLake Vector Store Index. See :ref:`Ref-Indices-VectorStore` for more information on the Pinecone vector store index.  |  
| `QDRANT`  |  `qdrant`  |  Qdrant Vector Store Index. See :ref:`Ref-Indices-VectorStore` for more information on the Qdrant vector store index.  |  
| `LANCEDB`  |  `lancedb`  |  LanceDB Vector Store Index See :ref:`Ref-Indices-VectorStore` for more information on the LanceDB vector store index.  |  
| `MILVUS`  |  `milvus`  |  Milvus Vector Store Index. See :ref:`Ref-Indices-VectorStore` for more information on the Milvus vector store index.  |  
| `CHROMA`  |  `chroma`  |  Chroma Vector Store Index. See :ref:`Ref-Indices-VectorStore` for more information on the Chroma vector store index.  |  
| `OPENSEARCH`  |  `opensearch`  |  Opensearch Vector Store Index. See :ref:`Ref-Indices-VectorStore` for more information on the Opensearch vector store index.  |  
| `MYSCALE`  |  `myscale`  |  MyScale Vector Store Index. See :ref:`Ref-Indices-VectorStore` for more information on the MyScale vector store index.  |  
| `CLICKHOUSE`  |  `clickhouse`  |  ClickHouse Vector Store Index. See :ref:`Ref-Indices-VectorStore` for more information on the ClickHouse vector store index.  |  
| `EPSILLA`  |  `epsilla`  |  Epsilla Vector Store Index. See :ref:`Ref-Indices-VectorStore` for more information on the Epsilla vector store index.  |  
| `CHATGPT_RETRIEVAL_PLUGIN`  |  `chatgpt_retrieval_plugin`  |  ChatGPT retrieval plugin index.  |  
|  SQL Structured Store Index. See :ref:`Ref-Indices-StructStore` for more information on the SQL vector store index.  |  
| `DASHVECTOR`  |  `dashvector`  |  DashVector Vector Store Index. See :ref:`Ref-Indices-VectorStore` for more information on the Dashvecotor vector store index.  |  
|  Knowledge Graph index. See :ref:`Ref-Indices-Knowledge-Graph` for KG indices.  |  
| `DOCUMENT_SUMMARY`  |  `document_summary`  |  Document Summary Index. See :ref:`Ref-Indices-Document-Summary` for Summary Indices.  |  
Source code in `llama-index-core/llama_index/core/data_structs/struct_type.py`  
| 
```




 10
 11
 12
 13
 14
 15
 16
 17
 18
 19
 20
 21
 22
 23
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
```
 | 
```
classIndexStructType(str, Enum):
"""
    Index struct type. Identifier for a "type" of index.

    Attributes:
        TREE ("tree"): Tree index. See :ref:`Ref-Indices-Tree` for tree indices.
        LIST ("list"): Summary index. See :ref:`Ref-Indices-List` for summary indices.
        KEYWORD_TABLE ("keyword_table"): Keyword table index. See
            :ref:`Ref-Indices-Table`
            for keyword table indices.
        DICT ("dict"): Faiss Vector Store Index. See
            :ref:`Ref-Indices-VectorStore`
            for more information on the faiss vector store index.
        SIMPLE_DICT ("simple_dict"): Simple Vector Store Index. See
            :ref:`Ref-Indices-VectorStore`
            for more information on the simple vector store index.
        WEAVIATE ("weaviate"): Weaviate Vector Store Index.
            See :ref:`Ref-Indices-VectorStore`
            for more information on the Weaviate vector store index.
        PINECONE ("pinecone"): Pinecone Vector Store Index.
            See :ref:`Ref-Indices-VectorStore`
            for more information on the Pinecone vector store index.
        DEEPLAKE ("deeplake"): DeepLake Vector Store Index.
            See :ref:`Ref-Indices-VectorStore`
            for more information on the Pinecone vector store index.
        QDRANT ("qdrant"): Qdrant Vector Store Index.
            See :ref:`Ref-Indices-VectorStore`
            for more information on the Qdrant vector store index.
        LANCEDB ("lancedb"): LanceDB Vector Store Index
            See :ref:`Ref-Indices-VectorStore`
            for more information on the LanceDB vector store index.
        MILVUS ("milvus"): Milvus Vector Store Index.
            See :ref:`Ref-Indices-VectorStore`
            for more information on the Milvus vector store index.
        CHROMA ("chroma"): Chroma Vector Store Index.
            See :ref:`Ref-Indices-VectorStore`
            for more information on the Chroma vector store index.
        OPENSEARCH ("opensearch"): Opensearch Vector Store Index.
            See :ref:`Ref-Indices-VectorStore`
            for more information on the Opensearch vector store index.
        MYSCALE ("myscale"): MyScale Vector Store Index.
            See :ref:`Ref-Indices-VectorStore`
            for more information on the MyScale vector store index.
        CLICKHOUSE ("clickhouse"): ClickHouse Vector Store Index.
            See :ref:`Ref-Indices-VectorStore`
            for more information on the ClickHouse vector store index.
        EPSILLA ("epsilla"): Epsilla Vector Store Index.
            See :ref:`Ref-Indices-VectorStore`
            for more information on the Epsilla vector store index.
        CHATGPT_RETRIEVAL_PLUGIN ("chatgpt_retrieval_plugin"): ChatGPT
            retrieval plugin index.
        SQL ("SQL"): SQL Structured Store Index.
            See :ref:`Ref-Indices-StructStore`
            for more information on the SQL vector store index.
        DASHVECTOR ("dashvector"): DashVector Vector Store Index.
            See :ref:`Ref-Indices-VectorStore`
            for more information on the Dashvecotor vector store index.
        KG ("kg"): Knowledge Graph index.
            See :ref:`Ref-Indices-Knowledge-Graph` for KG indices.
        DOCUMENT_SUMMARY ("document_summary"): Document Summary Index.
            See :ref:`Ref-Indices-Document-Summary` for Summary Indices.

    """

    # TODO: refactor so these are properties on the base class

    NODE = "node"
    TREE = "tree"
    LIST = "list"
    KEYWORD_TABLE = "keyword_table"

    # faiss
    DICT = "dict"
    # simple
    SIMPLE_DICT = "simple_dict"
    WEAVIATE = "weaviate"
    PINECONE = "pinecone"
    QDRANT = "qdrant"
    LANCEDB = "lancedb"
    MILVUS = "milvus"
    CHROMA = "chroma"
    MYSCALE = "myscale"
    CLICKHOUSE = "clickhouse"
    VECTOR_STORE = "vector_store"
    OPENSEARCH = "opensearch"
    DASHVECTOR = "dashvector"
    CHATGPT_RETRIEVAL_PLUGIN = "chatgpt_retrieval_plugin"
    DEEPLAKE = "deeplake"
    EPSILLA = "epsilla"
    # multimodal
    MULTIMODAL_VECTOR_STORE = "multimodal"
    # for SQL index
    SQL = "sql"
    # for KG index
    KG = "kg"
    SIMPLE_KG = "simple_kg"
    SIMPLE_LPG = "simple_lpg"
    NEBULAGRAPH = "nebulagraph"
    FALKORDB = "falkordb"

    # EMPTY
    EMPTY = "empty"
    COMPOSITE = "composite"

    PANDAS = "pandas"

    DOCUMENT_SUMMARY = "document_summary"

    # Managed
    VECTARA = "vectara"
    POSTGRESML = "postgresml"

```
 |  
| --- | --- |  
##  MockEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.MockEmbedding "Permanent link")
Bases: 
Mock embedding.
Used for token prediction.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `embed_dim`  |  embedding dimension  |  _required_  |  
Source code in `llama-index-core/llama_index/core/embeddings/mock_embed_model.py`  
| 
```
10
11
12
13
14
15
16
17
18
19
20
21
22
23
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
```
 | 
```
classMockEmbedding(BaseEmbedding):
"""
    Mock embedding.

    Used for token prediction.

    Args:
        embed_dim (int): embedding dimension

    """

    embed_dim: int

    def__init__(self, embed_dim: int, **kwargs: Any) -> None:
"""Init params."""
        super().__init__(embed_dim=embed_dim, **kwargs)

    @classmethod
    defclass_name(cls) -> str:
        return "MockEmbedding"

    def_get_vector(self) -> List[float]:
        return [0.5] * self.embed_dim

    async def_aget_text_embedding(self, text: str) -> List[float]:
        return self._get_vector()

    async def_aget_query_embedding(self, query: str) -> List[float]:
        return self._get_vector()

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        return self._get_vector()

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        return self._get_vector()

```
 |  
| --- | --- |  
##  ComposableGraph [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.ComposableGraph "Permanent link")
Composable graph.
Source code in `llama-index-core/llama_index/core/indices/composability/graph.py`  
| 
```
 17
 18
 19
 20
 21
 22
 23
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
```
 | 
```
classComposableGraph:
"""Composable graph."""

    def__init__(
        self,
        all_indices: Dict[str, BaseIndex],
        root_id: str,
        storage_context: Optional[StorageContext] = None,
    ) -> None:
"""Init params."""
        self._all_indices = all_indices
        self._root_id = root_id
        self.storage_context = storage_context

    @property
    defroot_id(self) -> str:
        return self._root_id

    @property
    defall_indices(self) -> Dict[str, BaseIndex]:
        return self._all_indices

    @property
    defroot_index(self) -> BaseIndex:
        return self._all_indices[self._root_id]

    @property
    defindex_struct(self) -> IndexStruct:
        return self._all_indices[self._root_id].index_struct

    @classmethod
    deffrom_indices(
        cls,
        root_index_cls: Type[BaseIndex],
        children_indices: Sequence[BaseIndex],
        index_summaries: Optional[Sequence[str]] = None,
        storage_context: Optional[StorageContext] = None,
        **kwargs: Any,
    ) -> "ComposableGraph":  # type: ignore
"""Create composable graph using this index class as the root."""
        fromllama_index.coreimport Settings

        with Settings.callback_manager.as_trace("graph_construction"):
            if index_summaries is None:
                for index in children_indices:
                    if index.index_struct.summary is None:
                        raise ValueError(
                            "Summary must be set for children indices. "
                            "If the index does a summary "
                            "(through index.index_struct.summary), then "
                            "it must be specified with then `index_summaries` "
                            "argument in this function. We will support "
                            "automatically setting the summary in the future."
                        )
                index_summaries = [
                    index.index_struct.summary for index in children_indices
                ]
            else:
                # set summaries for each index
                for index, summary in zip(children_indices, index_summaries):
                    index.index_struct.summary = summary

            if len(children_indices) != len(index_summaries):
                raise ValueError("indices and index_summaries must have same length!")

            # construct index nodes
            index_nodes = []
            for index, summary in zip(children_indices, index_summaries):
                assert isinstance(index.index_struct, IndexStruct)
                index_node = IndexNode(
                    text=summary,
                    index_id=index.index_id,
                    relationships={
                        NodeRelationship.SOURCE: RelatedNodeInfo(
                            node_id=index.index_id, node_type=ObjectType.INDEX
                        )
                    },
                )
                index_nodes.append(index_node)

            # construct root index
            root_index = root_index_cls(
                nodes=index_nodes,
                storage_context=storage_context,
                **kwargs,
            )
            # type: ignore
            all_indices: List[BaseIndex] = [
                *cast(List[BaseIndex], children_indices),
                root_index,
            ]

            return cls(
                all_indices={index.index_id: index for index in all_indices},
                root_id=root_index.index_id,
                storage_context=storage_context,
            )

    defget_index(self, index_struct_id: Optional[str] = None) -> BaseIndex:
"""Get index from index struct id."""
        if index_struct_id is None:
            index_struct_id = self._root_id
        return self._all_indices[index_struct_id]

    defas_query_engine(self, **kwargs: Any) -> BaseQueryEngine:
        # NOTE: lazy import
        fromllama_index.core.query_engine.graph_query_engineimport (
            ComposableGraphQueryEngine,
        )

        return ComposableGraphQueryEngine(self, **kwargs)

```
 |  
| --- | --- |  
###  from_indices `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.ComposableGraph.from_indices "Permanent link")

```
from_indices(
    root_index_cls: [],
    children_indices: Sequence[],
    index_summaries: Optional[Sequence[]] = None,
    storage_context: Optional[] = None,
    **kwargs: 
) -> 

```

Create composable graph using this index class as the root.
Source code in `llama-index-core/llama_index/core/indices/composability/graph.py`  
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
```
 | 
```
@classmethod
deffrom_indices(
    cls,
    root_index_cls: Type[BaseIndex],
    children_indices: Sequence[BaseIndex],
    index_summaries: Optional[Sequence[str]] = None,
    storage_context: Optional[StorageContext] = None,
    **kwargs: Any,
) -> "ComposableGraph":  # type: ignore
"""Create composable graph using this index class as the root."""
    fromllama_index.coreimport Settings

    with Settings.callback_manager.as_trace("graph_construction"):
        if index_summaries is None:
            for index in children_indices:
                if index.index_struct.summary is None:
                    raise ValueError(
                        "Summary must be set for children indices. "
                        "If the index does a summary "
                        "(through index.index_struct.summary), then "
                        "it must be specified with then `index_summaries` "
                        "argument in this function. We will support "
                        "automatically setting the summary in the future."
                    )
            index_summaries = [
                index.index_struct.summary for index in children_indices
            ]
        else:
            # set summaries for each index
            for index, summary in zip(children_indices, index_summaries):
                index.index_struct.summary = summary

        if len(children_indices) != len(index_summaries):
            raise ValueError("indices and index_summaries must have same length!")

        # construct index nodes
        index_nodes = []
        for index, summary in zip(children_indices, index_summaries):
            assert isinstance(index.index_struct, IndexStruct)
            index_node = IndexNode(
                text=summary,
                index_id=index.index_id,
                relationships={
                    NodeRelationship.SOURCE: RelatedNodeInfo(
                        node_id=index.index_id, node_type=ObjectType.INDEX
                    )
                },
            )
            index_nodes.append(index_node)

        # construct root index
        root_index = root_index_cls(
            nodes=index_nodes,
            storage_context=storage_context,
            **kwargs,
        )
        # type: ignore
        all_indices: List[BaseIndex] = [
            *cast(List[BaseIndex], children_indices),
            root_index,
        ]

        return cls(
            all_indices={index.index_id: index for index in all_indices},
            root_id=root_index.index_id,
            storage_context=storage_context,
        )

```
 |  
| --- | --- |  
###  get_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.ComposableGraph.get_index "Permanent link")

```
get_index(
    index_struct_id: Optional[] = None,
) -> 

```

Get index from index struct id.
Source code in `llama-index-core/llama_index/core/indices/composability/graph.py`  
| 
```
115
116
117
118
119
```
 | 
```
defget_index(self, index_struct_id: Optional[str] = None) -> BaseIndex:
"""Get index from index struct id."""
    if index_struct_id is None:
        index_struct_id = self._root_id
    return self._all_indices[index_struct_id]

```
 |  
| --- | --- |  
##  DocumentSummaryIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.DocumentSummaryIndex "Permanent link")
Bases: `BaseIndex[](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex "BaseIndex \(llama_index.core.indices.base.BaseIndex\)")[IndexDocumentSummary]`
Document Summary Index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `response_synthesizer`  |   |  A response synthesizer for generating summaries.  |  `None`  |  
|  `summary_query`  |  The query to use to generate the summary for each document.  |  `DEFAULT_SUMMARY_QUERY`  |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
|  `embed_summaries`  |  `bool`  |  Whether to embed the summaries. This is required for running the default embedding-based retriever. Defaults to True.  |  `True`  |  
Source code in `llama-index-core/llama_index/core/indices/document_summary/base.py`  
| 
```
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
```
 | 
```
classDocumentSummaryIndex(BaseIndex[IndexDocumentSummary]):
"""
    Document Summary Index.

    Args:
        response_synthesizer (BaseSynthesizer): A response synthesizer for generating
            summaries.
        summary_query (str): The query to use to generate the summary for each document.
        show_progress (bool): Whether to show tqdm progress bars.
            Defaults to False.
        embed_summaries (bool): Whether to embed the summaries.
            This is required for running the default embedding-based retriever.
            Defaults to True.

    """

    index_struct_cls = IndexDocumentSummary

    def__init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        objects: Optional[Sequence[IndexNode]] = None,
        index_struct: Optional[IndexDocumentSummary] = None,
        llm: Optional[LLM] = None,
        embed_model: Optional[BaseEmbedding] = None,
        storage_context: Optional[StorageContext] = None,
        response_synthesizer: Optional[BaseSynthesizer] = None,
        summary_query: str = DEFAULT_SUMMARY_QUERY,
        show_progress: bool = False,
        embed_summaries: bool = True,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        self._llm = llm or Settings.llm
        self._embed_model = embed_model or Settings.embed_model
        self._response_synthesizer = response_synthesizer or get_response_synthesizer(
            llm=self._llm, response_mode=ResponseMode.TREE_SUMMARIZE
        )
        self._summary_query = summary_query
        self._embed_summaries = embed_summaries

        super().__init__(
            nodes=nodes,
            index_struct=index_struct,
            storage_context=storage_context,
            show_progress=show_progress,
            objects=objects,
            **kwargs,
        )

    @property
    defvector_store(self) -> BasePydanticVectorStore:
        return self._vector_store

    defas_retriever(
        self,
        retriever_mode: Union[str, _RetrieverMode] = _RetrieverMode.EMBEDDING,
        **kwargs: Any,
    ) -> BaseRetriever:
"""
        Get retriever.

        Args:
            retriever_mode (Union[str, DocumentSummaryRetrieverMode]): A retriever mode.
                Defaults to DocumentSummaryRetrieverMode.EMBEDDING.

        """
        fromllama_index.core.indices.document_summary.retrieversimport (
            DocumentSummaryIndexEmbeddingRetriever,
            DocumentSummaryIndexLLMRetriever,
        )

        LLMRetriever = DocumentSummaryIndexLLMRetriever
        EmbeddingRetriever = DocumentSummaryIndexEmbeddingRetriever

        if retriever_mode == _RetrieverMode.EMBEDDING:
            if not self._embed_summaries:
                raise ValueError(
                    "Cannot use embedding retriever if embed_summaries is False"
                )

            return EmbeddingRetriever(
                self,
                object_map=self._object_map,
                embed_model=self._embed_model,
                **kwargs,
            )
        if retriever_mode == _RetrieverMode.LLM:
            return LLMRetriever(
                self, object_map=self._object_map, llm=self._llm, **kwargs
            )
        else:
            raise ValueError(f"Unknown retriever mode: {retriever_mode}")

    defget_document_summary(self, doc_id: str) -> str:
"""
        Get document summary by doc id.

        Args:
            doc_id (str): A document id.

        """
        if doc_id not in self._index_struct.doc_id_to_summary_id:
            raise ValueError(f"doc_id {doc_id} not in index")
        summary_id = self._index_struct.doc_id_to_summary_id[doc_id]
        return self.docstore.get_node(summary_id).get_content()

    def_add_nodes_to_index(
        self,
        index_struct: IndexDocumentSummary,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
    ) -> None:
"""Add nodes to index."""
        doc_id_to_nodes = defaultdict(list)
        for node in nodes:
            if node.ref_doc_id is None:
                raise ValueError(
                    "ref_doc_id of node cannot be None when building a document "
                    "summary index"
                )
            doc_id_to_nodes[node.ref_doc_id].append(node)

        summary_node_dict = {}
        items = doc_id_to_nodes.items()
        iterable_with_progress = get_tqdm_iterable(
            items, show_progress, "Summarizing documents"
        )

        for doc_id, nodes in iterable_with_progress:
            print(f"current doc id: {doc_id}")
            nodes_with_scores = [NodeWithScore(node=n) for n in nodes]
            # get the summary for each doc_id
            summary_response = self._response_synthesizer.synthesize(
                query=self._summary_query,
                nodes=nodes_with_scores,
            )
            summary_response = cast(Response, summary_response)
            docid_first_node = doc_id_to_nodes.get(doc_id, [TextNode()])[0]
            summary_node_dict[doc_id] = TextNode(
                text=summary_response.response,
                relationships={
                    NodeRelationship.SOURCE: RelatedNodeInfo(node_id=doc_id)
                },
                metadata=docid_first_node.metadata,
                excluded_embed_metadata_keys=docid_first_node.excluded_embed_metadata_keys,
                excluded_llm_metadata_keys=docid_first_node.excluded_llm_metadata_keys,
            )
            self.docstore.add_documents([summary_node_dict[doc_id]])
            logger.info(
                f"> Generated summary for doc {doc_id}: {summary_response.response}"
            )

        for doc_id, nodes in doc_id_to_nodes.items():
            index_struct.add_summary_and_nodes(summary_node_dict[doc_id], nodes)

        if self._embed_summaries:
            summary_nodes = list(summary_node_dict.values())
            id_to_embed_map = embed_nodes(
                summary_nodes, self._embed_model, show_progress=show_progress
            )

            summary_nodes_with_embedding = []
            for node in summary_nodes:
                node_with_embedding = node.model_copy()
                node_with_embedding.embedding = id_to_embed_map[node.node_id]
                summary_nodes_with_embedding.append(node_with_embedding)
            self._vector_store.add(summary_nodes_with_embedding)

    def_build_index_from_nodes(
        self,
        nodes: Sequence[BaseNode],
        **build_kwargs: Any,
    ) -> IndexDocumentSummary:
"""Build index from nodes."""
        # first get doc_id to nodes_dict, generate a summary for each doc_id,
        # then build the index struct
        index_struct = IndexDocumentSummary()
        self._add_nodes_to_index(index_struct, nodes, self._show_progress)
        return index_struct

    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Insert a document."""
        self._add_nodes_to_index(self._index_struct, nodes)

    def_delete_node(self, node_id: str, **delete_kwargs: Any) -> None:
        pass

    defdelete_nodes(
        self,
        node_ids: List[str],
        delete_from_docstore: bool = False,
        **delete_kwargs: Any,
    ) -> None:
"""
        Delete a list of nodes from the index.

        Args:
            node_ids (List[str]): A list of node_ids from the nodes to delete

        """
        index_nodes = self._index_struct.node_id_to_summary_id.keys()
        for node in node_ids:
            if node not in index_nodes:
                logger.warning(f"node_id {node} not found, will not be deleted.")
                node_ids.remove(node)

        self._index_struct.delete_nodes(node_ids)

        remove_summary_ids = [
            summary_id
            for summary_id in self._index_struct.summary_id_to_node_ids
            if len(self._index_struct.summary_id_to_node_ids[summary_id]) == 0
        ]

        remove_docs = [
            doc_id
            for doc_id in self._index_struct.doc_id_to_summary_id
            if self._index_struct.doc_id_to_summary_id[doc_id] in remove_summary_ids
        ]

        for doc_id in remove_docs:
            self.delete_ref_doc(doc_id)

    defdelete_ref_doc(
        self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
    ) -> None:
"""
        Delete a document from the index.
        All nodes in the index related to the document will be deleted.
        """
        ref_doc_info = self.docstore.get_ref_doc_info(ref_doc_id)
        if ref_doc_info is None:
            logger.warning(f"ref_doc_id {ref_doc_id} not found, nothing deleted.")
            return
        self._index_struct.delete(ref_doc_id)
        self._vector_store.delete(ref_doc_id)

        if delete_from_docstore:
            self.docstore.delete_ref_doc(ref_doc_id, raise_error=False)

        self._storage_context.index_store.add_index_struct(self._index_struct)

    @property
    defref_doc_info(self) -> Dict[str, RefDocInfo]:
"""Retrieve a dict mapping of ingested documents and their nodes+metadata."""
        ref_doc_ids = list(self._index_struct.doc_id_to_summary_id.keys())

        all_ref_doc_info = {}
        for ref_doc_id in ref_doc_ids:
            ref_doc_info = self.docstore.get_ref_doc_info(ref_doc_id)
            if not ref_doc_info:
                continue

            all_ref_doc_info[ref_doc_id] = ref_doc_info
        return all_ref_doc_info

```
 |  
| --- | --- |  
###  ref_doc_info `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.DocumentSummaryIndex.ref_doc_info "Permanent link")

```
ref_doc_info: [, ]

```

Retrieve a dict mapping of ingested documents and their nodes+metadata.
###  as_retriever [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.DocumentSummaryIndex.as_retriever "Permanent link")

```
as_retriever(
    retriever_mode: Union[, _RetrieverMode] = EMBEDDING,
    **kwargs: 
) -> 

```

Get retriever.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `retriever_mode`  |  `Union[str, DocumentSummaryRetrieverMode]`  |  A retriever mode. Defaults to DocumentSummaryRetrieverMode.EMBEDDING.  |  `EMBEDDING`  |  
Source code in `llama-index-core/llama_index/core/indices/document_summary/base.py`  
| 
```
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
```
 | 
```
defas_retriever(
    self,
    retriever_mode: Union[str, _RetrieverMode] = _RetrieverMode.EMBEDDING,
    **kwargs: Any,
) -> BaseRetriever:
"""
    Get retriever.

    Args:
        retriever_mode (Union[str, DocumentSummaryRetrieverMode]): A retriever mode.
            Defaults to DocumentSummaryRetrieverMode.EMBEDDING.

    """
    fromllama_index.core.indices.document_summary.retrieversimport (
        DocumentSummaryIndexEmbeddingRetriever,
        DocumentSummaryIndexLLMRetriever,
    )

    LLMRetriever = DocumentSummaryIndexLLMRetriever
    EmbeddingRetriever = DocumentSummaryIndexEmbeddingRetriever

    if retriever_mode == _RetrieverMode.EMBEDDING:
        if not self._embed_summaries:
            raise ValueError(
                "Cannot use embedding retriever if embed_summaries is False"
            )

        return EmbeddingRetriever(
            self,
            object_map=self._object_map,
            embed_model=self._embed_model,
            **kwargs,
        )
    if retriever_mode == _RetrieverMode.LLM:
        return LLMRetriever(
            self, object_map=self._object_map, llm=self._llm, **kwargs
        )
    else:
        raise ValueError(f"Unknown retriever mode: {retriever_mode}")

```
 |  
| --- | --- |  
###  get_document_summary [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.DocumentSummaryIndex.get_document_summary "Permanent link")

```
get_document_summary(doc_id: ) -> 

```

Get document summary by doc id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `doc_id`  |  A document id.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/document_summary/base.py`  
| 
```
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
defget_document_summary(self, doc_id: str) -> str:
"""
    Get document summary by doc id.

    Args:
        doc_id (str): A document id.

    """
    if doc_id not in self._index_struct.doc_id_to_summary_id:
        raise ValueError(f"doc_id {doc_id} not in index")
    summary_id = self._index_struct.doc_id_to_summary_id[doc_id]
    return self.docstore.get_node(summary_id).get_content()

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.DocumentSummaryIndex.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: [],
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Delete a list of nodes from the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `List[str]`  |  A list of node_ids from the nodes to delete  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/document_summary/base.py`  
| 
```
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
```
 | 
```
defdelete_nodes(
    self,
    node_ids: List[str],
    delete_from_docstore: bool = False,
    **delete_kwargs: Any,
) -> None:
"""
    Delete a list of nodes from the index.

    Args:
        node_ids (List[str]): A list of node_ids from the nodes to delete

    """
    index_nodes = self._index_struct.node_id_to_summary_id.keys()
    for node in node_ids:
        if node not in index_nodes:
            logger.warning(f"node_id {node} not found, will not be deleted.")
            node_ids.remove(node)

    self._index_struct.delete_nodes(node_ids)

    remove_summary_ids = [
        summary_id
        for summary_id in self._index_struct.summary_id_to_node_ids
        if len(self._index_struct.summary_id_to_node_ids[summary_id]) == 0
    ]

    remove_docs = [
        doc_id
        for doc_id in self._index_struct.doc_id_to_summary_id
        if self._index_struct.doc_id_to_summary_id[doc_id] in remove_summary_ids
    ]

    for doc_id in remove_docs:
        self.delete_ref_doc(doc_id)

```
 |  
| --- | --- |  
###  delete_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.DocumentSummaryIndex.delete_ref_doc "Permanent link")

```
delete_ref_doc(
    ref_doc_id: ,
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Delete a document from the index. All nodes in the index related to the document will be deleted.
Source code in `llama-index-core/llama_index/core/indices/document_summary/base.py`  
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
```
 | 
```
defdelete_ref_doc(
    self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
) -> None:
"""
    Delete a document from the index.
    All nodes in the index related to the document will be deleted.
    """
    ref_doc_info = self.docstore.get_ref_doc_info(ref_doc_id)
    if ref_doc_info is None:
        logger.warning(f"ref_doc_id {ref_doc_id} not found, nothing deleted.")
        return
    self._index_struct.delete(ref_doc_id)
    self._vector_store.delete(ref_doc_id)

    if delete_from_docstore:
        self.docstore.delete_ref_doc(ref_doc_id, raise_error=False)

    self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
##  KeywordTableIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.KeywordTableIndex "Permanent link")
Bases: `BaseKeywordTableIndex`
Keyword Table Index.
This index uses a GPT model to extract keywords from the text.
Source code in `llama-index-core/llama_index/core/indices/keyword_table/base.py`  
| 
```
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
```
 | 
```
classKeywordTableIndex(BaseKeywordTableIndex):
"""
    Keyword Table Index.

    This index uses a GPT model to extract keywords from the text.

    """

    def_extract_keywords(self, text: str) -> Set[str]:
"""Extract keywords from text."""
        response = self._llm.predict(
            self.keyword_extract_template,
            text=text,
        )
        return extract_keywords_given_response(response, start_token="KEYWORDS:")

    async def_async_extract_keywords(self, text: str) -> Set[str]:
"""Extract keywords from text."""
        response = await self._llm.apredict(
            self.keyword_extract_template,
            text=text,
        )
        return extract_keywords_given_response(response, start_token="KEYWORDS:")

```
 |  
| --- | --- |  
##  KnowledgeGraphIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.KnowledgeGraphIndex "Permanent link")
Bases: 
Knowledge Graph Index.
Build a KG by extracting triplets, and leveraging the KG during query-time.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `kg_triplet_extract_template`  |   |  The prompt to use for extracting triplets.  |  `None`  |  
|  `max_triplets_per_chunk`  |  The maximum number of triplets to extract.  |  
|  `storage_context`  |  `Optional[StorageContext[](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.storage.storage_context.StorageContext "StorageContext


  
      dataclass
   \(llama_index.core.storage.storage_context.StorageContext\)")]`  |  The storage context to use.  |  `None`  |  
|  `graph_store`  |  `Optional[GraphStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.GraphStore "GraphStore \(llama_index.core.graph_stores.types.GraphStore\)")]`  |  The graph store to use.  |  _required_  |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
|  `include_embeddings`  |  `bool`  |  Whether to include embeddings in the index. Defaults to False.  |  `False`  |  
|  `max_object_length`  |  The maximum length of the object in a triplet. Defaults to 128.  |  `128`  |  
|  `kg_triplet_extract_fn`  |  `Optional[Callable]`  |  The function to use for extracting triplets. Defaults to None.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/indices/knowledge_graph/base.py`  
| 
```
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
```
 | 
```
@deprecated.deprecated(
    version="0.10.53",
    reason=(
        "The KnowledgeGraphIndex class has been deprecated. "
        "Please use the new PropertyGraphIndex class instead. "
        "If a certain graph store integration is missing in the new class, "
        "please open an issue on the GitHub repository or contribute it!"
    ),
)
classKnowledgeGraphIndex(BaseIndex[KG]):
"""
    Knowledge Graph Index.

    Build a KG by extracting triplets, and leveraging the KG during query-time.

    Args:
        kg_triplet_extract_template (BasePromptTemplate): The prompt to use for
            extracting triplets.
        max_triplets_per_chunk (int): The maximum number of triplets to extract.
        storage_context (Optional[StorageContext]): The storage context to use.
        graph_store (Optional[GraphStore]): The graph store to use.
        show_progress (bool): Whether to show tqdm progress bars. Defaults to False.
        include_embeddings (bool): Whether to include embeddings in the index.
            Defaults to False.
        max_object_length (int): The maximum length of the object in a triplet.
            Defaults to 128.
        kg_triplet_extract_fn (Optional[Callable]): The function to use for
            extracting triplets. Defaults to None.

    """

    index_struct_cls = KG

    def__init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        objects: Optional[Sequence[IndexNode]] = None,
        index_struct: Optional[KG] = None,
        llm: Optional[LLM] = None,
        embed_model: Optional[BaseEmbedding] = None,
        storage_context: Optional[StorageContext] = None,
        kg_triplet_extract_template: Optional[BasePromptTemplate] = None,
        max_triplets_per_chunk: int = 10,
        include_embeddings: bool = False,
        show_progress: bool = False,
        max_object_length: int = 128,
        kg_triplet_extract_fn: Optional[Callable] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        # need to set parameters before building index in base class.
        self.include_embeddings = include_embeddings
        self.max_triplets_per_chunk = max_triplets_per_chunk
        self.kg_triplet_extract_template = (
            kg_triplet_extract_template or DEFAULT_KG_TRIPLET_EXTRACT_PROMPT
        )
        # NOTE: Partially format keyword extract template here.
        self.kg_triplet_extract_template = (
            self.kg_triplet_extract_template.partial_format(
                max_knowledge_triplets=self.max_triplets_per_chunk
            )
        )
        self._max_object_length = max_object_length
        self._kg_triplet_extract_fn = kg_triplet_extract_fn

        self._llm = llm or Settings.llm
        self._embed_model = embed_model or Settings.embed_model

        super().__init__(
            nodes=nodes,
            index_struct=index_struct,
            storage_context=storage_context,
            show_progress=show_progress,
            objects=objects,
            **kwargs,
        )

        # TODO: legacy conversion - remove in next release
        if (
            len(self.index_struct.table)  0
            and isinstance(self.graph_store, SimpleGraphStore)
            and len(self.graph_store._data.graph_dict) == 0
        ):
            logger.warning("Upgrading previously saved KG index to new storage format.")
            self.graph_store._data.graph_dict = self.index_struct.rel_map

    @property
    defgraph_store(self) -> GraphStore:
        return self._graph_store

    defas_retriever(
        self,
        retriever_mode: Optional[str] = None,
        embed_model: Optional[BaseEmbedding] = None,
        **kwargs: Any,
    ) -> BaseRetriever:
        fromllama_index.core.indices.knowledge_graph.retrieversimport (
            KGRetrieverMode,
            KGTableRetriever,
        )

        if len(self.index_struct.embedding_dict)  0 and retriever_mode is None:
            retriever_mode = KGRetrieverMode.HYBRID
        elif retriever_mode is None:
            retriever_mode = KGRetrieverMode.KEYWORD
        elif isinstance(retriever_mode, str):
            retriever_mode = KGRetrieverMode(retriever_mode)
        else:
            retriever_mode = retriever_mode

        return KGTableRetriever(
            self,
            object_map=self._object_map,
            llm=self._llm,
            embed_model=embed_model or self._embed_model,
            retriever_mode=retriever_mode,
            **kwargs,
        )

    def_extract_triplets(self, text: str) -> List[Tuple[str, str, str]]:
        if self._kg_triplet_extract_fn is not None:
            return self._kg_triplet_extract_fn(text)
        else:
            return self._llm_extract_triplets(text)

    def_llm_extract_triplets(self, text: str) -> List[Tuple[str, str, str]]:
"""Extract keywords from text."""
        response = self._llm.predict(
            self.kg_triplet_extract_template,
            text=text,
        )
        return self._parse_triplet_response(
            response, max_length=self._max_object_length
        )

    @staticmethod
    def_parse_triplet_response(
        response: str, max_length: int = 128
    ) -> List[Tuple[str, str, str]]:
        knowledge_strs = response.strip().split("\n")
        results = []
        for text in knowledge_strs:
            if "(" not in text or ")" not in text or text.index(")")  text.index("("):
                # skip empty lines and non-triplets
                continue
            triplet_part = text[text.index("(") + 1 : text.index(")")]
            tokens = triplet_part.split(",")
            if len(tokens) != 3:
                continue

            if any(len(s.encode("utf-8"))  max_length for s in tokens):
                # We count byte-length instead of len() for UTF-8 chars,
                # will skip if any of the tokens are too long.
                # This is normally due to a poorly formatted triplet
                # extraction, in more serious KG building cases
                # we'll need NLP models to better extract triplets.
                continue

            subj, pred, obj = map(str.strip, tokens)
            if not subj or not pred or not obj:
                # skip partial triplets
                continue

            # Strip double quotes and Capitalize triplets for disambiguation
            subj, pred, obj = (
                entity.strip('"').capitalize() for entity in [subj, pred, obj]
            )

            results.append((subj, pred, obj))
        return results

    def_build_index_from_nodes(
        self, nodes: Sequence[BaseNode], **build_kwargs: Any
    ) -> KG:
"""Build the index from nodes."""
        # do simple concatenation
        index_struct = self.index_struct_cls()
        nodes_with_progress = get_tqdm_iterable(
            nodes, self._show_progress, "Processing nodes"
        )
        for n in nodes_with_progress:
            triplets = self._extract_triplets(
                n.get_content(metadata_mode=MetadataMode.LLM)
            )
            logger.debug(f"> Extracted triplets: {triplets}")
            for triplet in triplets:
                subj, _, obj = triplet
                self.upsert_triplet(triplet)
                index_struct.add_node([subj, obj], n)

            if self.include_embeddings:
                triplet_texts = [str(t) for t in triplets]

                embed_outputs = self._embed_model.get_text_embedding_batch(
                    triplet_texts, show_progress=self._show_progress
                )
                for rel_text, rel_embed in zip(triplet_texts, embed_outputs):
                    index_struct.add_to_embedding_dict(rel_text, rel_embed)

        return index_struct

    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Insert a document."""
        for n in nodes:
            triplets = self._extract_triplets(
                n.get_content(metadata_mode=MetadataMode.LLM)
            )
            logger.debug(f"Extracted triplets: {triplets}")
            for triplet in triplets:
                subj, _, obj = triplet
                triplet_str = str(triplet)
                self.upsert_triplet(triplet)
                self._index_struct.add_node([subj, obj], n)
                if (
                    self.include_embeddings
                    and triplet_str not in self._index_struct.embedding_dict
                ):
                    rel_embedding = self._embed_model.get_text_embedding(triplet_str)
                    self._index_struct.add_to_embedding_dict(triplet_str, rel_embedding)

        # Update the storage context's index_store
        self._storage_context.index_store.add_index_struct(self._index_struct)

    defupsert_triplet(
        self, triplet: Tuple[str, str, str], include_embeddings: bool = False
    ) -> None:
"""
        Insert triplets and optionally embeddings.

        Used for manual insertion of KG triplets (in the form
        of (subject, relationship, object)).

        Args:
            triplet (tuple): Knowledge triplet
            embedding (Any, optional): Embedding option for the triplet. Defaults to None.

        """
        self._graph_store.upsert_triplet(*triplet)
        triplet_str = str(triplet)
        if include_embeddings:
            set_embedding = self._embed_model.get_text_embedding(triplet_str)
            self._index_struct.add_to_embedding_dict(str(triplet), set_embedding)
            self._storage_context.index_store.add_index_struct(self._index_struct)

    defadd_node(self, keywords: List[str], node: BaseNode) -> None:
"""
        Add node.

        Used for manual insertion of nodes (keyed by keywords).

        Args:
            keywords (List[str]): Keywords to index the node.
            node (Node): Node to be indexed.

        """
        self._index_struct.add_node(keywords, node)
        self._docstore.add_documents([node], allow_update=True)

    defupsert_triplet_and_node(
        self,
        triplet: Tuple[str, str, str],
        node: BaseNode,
        include_embeddings: bool = False,
    ) -> None:
"""
        Upsert KG triplet and node.

        Calls both upsert_triplet and add_node.
        Behavior is idempotent; if Node already exists,
        only triplet will be added.

        Args:
            keywords (List[str]): Keywords to index the node.
            node (Node): Node to be indexed.
            include_embeddings (bool): Option to add embeddings for triplets. Defaults to False

        """
        subj, _, obj = triplet
        self.upsert_triplet(triplet)
        self.add_node([subj, obj], node)
        triplet_str = str(triplet)
        if include_embeddings:
            set_embedding = self._embed_model.get_text_embedding(triplet_str)
            self._index_struct.add_to_embedding_dict(str(triplet), set_embedding)
            self._storage_context.index_store.add_index_struct(self._index_struct)

    def_delete_node(self, node_id: str, **delete_kwargs: Any) -> None:
"""Delete a node."""
        raise NotImplementedError("Delete is not supported for KG index yet.")

    @property
    defref_doc_info(self) -> Dict[str, RefDocInfo]:
"""Retrieve a dict mapping of ingested documents and their nodes+metadata."""
        node_doc_ids_sets = list(self._index_struct.table.values())
        node_doc_ids = list(set().union(*node_doc_ids_sets))
        nodes = self.docstore.get_nodes(node_doc_ids)

        all_ref_doc_info = {}
        for node in nodes:
            ref_node = node.source_node
            if not ref_node:
                continue

            ref_doc_info = self.docstore.get_ref_doc_info(ref_node.node_id)
            if not ref_doc_info:
                continue

            all_ref_doc_info[ref_node.node_id] = ref_doc_info
        return all_ref_doc_info

    defget_networkx_graph(self, limit: int = 100) -> Any:
"""
        Get networkx representation of the graph structure.

        Args:
            limit (int): Number of starting nodes to be included in the graph.

        NOTE: This function requires networkx to be installed.
        NOTE: This is a beta feature.

        """
        try:
            importnetworkxasnx
        except ImportError:
            raise ImportError(
                "Please install networkx to visualize the graph: `pip install networkx`"
            )

        g = nx.Graph()
        subjs = list(self.index_struct.table.keys())

        # add edges
        rel_map = self._graph_store.get_rel_map(subjs=subjs, depth=1, limit=limit)

        added_nodes = set()
        for keyword in rel_map:
            for path in rel_map[keyword]:
                subj = keyword
                for i in range(0, len(path), 2):
                    if i + 2 >= len(path):
                        break

                    if subj not in added_nodes:
                        g.add_node(subj)
                        added_nodes.add(subj)

                    rel = path[i + 1]
                    obj = path[i + 2]

                    g.add_edge(subj, obj, label=rel, title=rel)
                    subj = obj
        return g

    @property
    defquery_context(self) -> Dict[str, Any]:
        return {GRAPH_STORE_KEY: self._graph_store}

```
 |  
| --- | --- |  
###  ref_doc_info `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.KnowledgeGraphIndex.ref_doc_info "Permanent link")

```
ref_doc_info: [, ]

```

Retrieve a dict mapping of ingested documents and their nodes+metadata.
###  upsert_triplet [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.KnowledgeGraphIndex.upsert_triplet "Permanent link")

```
upsert_triplet(
    triplet: Tuple[, , ],
    include_embeddings:  = False,
) -> None

```

Insert triplets and optionally embeddings.
Used for manual insertion of KG triplets (in the form of (subject, relationship, object)).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `triplet`  |  `tuple`  |  Knowledge triplet  |  _required_  |  
|  `embedding`  |  Embedding option for the triplet. Defaults to None.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/knowledge_graph/base.py`  
| 
```
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
```
 | 
```
defupsert_triplet(
    self, triplet: Tuple[str, str, str], include_embeddings: bool = False
) -> None:
"""
    Insert triplets and optionally embeddings.

    Used for manual insertion of KG triplets (in the form
    of (subject, relationship, object)).

    Args:
        triplet (tuple): Knowledge triplet
        embedding (Any, optional): Embedding option for the triplet. Defaults to None.

    """
    self._graph_store.upsert_triplet(*triplet)
    triplet_str = str(triplet)
    if include_embeddings:
        set_embedding = self._embed_model.get_text_embedding(triplet_str)
        self._index_struct.add_to_embedding_dict(str(triplet), set_embedding)
        self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  add_node [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.KnowledgeGraphIndex.add_node "Permanent link")

```
add_node(keywords: [], node: ) -> None

```

Add node.
Used for manual insertion of nodes (keyed by keywords).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `keywords`  |  `List[str]`  |  Keywords to index the node.  |  _required_  |  
|  `node`  |  `Node`  |  Node to be indexed.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/knowledge_graph/base.py`  
| 
```
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
```
 | 
```
defadd_node(self, keywords: List[str], node: BaseNode) -> None:
"""
    Add node.

    Used for manual insertion of nodes (keyed by keywords).

    Args:
        keywords (List[str]): Keywords to index the node.
        node (Node): Node to be indexed.

    """
    self._index_struct.add_node(keywords, node)
    self._docstore.add_documents([node], allow_update=True)

```
 |  
| --- | --- |  
###  upsert_triplet_and_node [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.KnowledgeGraphIndex.upsert_triplet_and_node "Permanent link")

```
upsert_triplet_and_node(
    triplet: Tuple[, , ],
    node: ,
    include_embeddings:  = False,
) -> None

```

Upsert KG triplet and node.
Calls both upsert_triplet and add_node. Behavior is idempotent; if Node already exists, only triplet will be added.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `keywords`  |  `List[str]`  |  Keywords to index the node.  |  _required_  |  
|  `node`  |  `Node`  |  Node to be indexed.  |  _required_  |  
|  `include_embeddings`  |  `bool`  |  Option to add embeddings for triplets. Defaults to False  |  `False`  |  
Source code in `llama-index-core/llama_index/core/indices/knowledge_graph/base.py`  
| 
```
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
defupsert_triplet_and_node(
    self,
    triplet: Tuple[str, str, str],
    node: BaseNode,
    include_embeddings: bool = False,
) -> None:
"""
    Upsert KG triplet and node.

    Calls both upsert_triplet and add_node.
    Behavior is idempotent; if Node already exists,
    only triplet will be added.

    Args:
        keywords (List[str]): Keywords to index the node.
        node (Node): Node to be indexed.
        include_embeddings (bool): Option to add embeddings for triplets. Defaults to False

    """
    subj, _, obj = triplet
    self.upsert_triplet(triplet)
    self.add_node([subj, obj], node)
    triplet_str = str(triplet)
    if include_embeddings:
        set_embedding = self._embed_model.get_text_embedding(triplet_str)
        self._index_struct.add_to_embedding_dict(str(triplet), set_embedding)
        self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  get_networkx_graph [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.KnowledgeGraphIndex.get_networkx_graph "Permanent link")

```
get_networkx_graph(limit:  = 100) -> 

```

Get networkx representation of the graph structure.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `limit`  |  Number of starting nodes to be included in the graph.  |  `100`  |  
NOTE: This function requires networkx to be installed. NOTE: This is a beta feature.
Source code in `llama-index-core/llama_index/core/indices/knowledge_graph/base.py`  
| 
```
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
```
 | 
```
defget_networkx_graph(self, limit: int = 100) -> Any:
"""
    Get networkx representation of the graph structure.

    Args:
        limit (int): Number of starting nodes to be included in the graph.

    NOTE: This function requires networkx to be installed.
    NOTE: This is a beta feature.

    """
    try:
        importnetworkxasnx
    except ImportError:
        raise ImportError(
            "Please install networkx to visualize the graph: `pip install networkx`"
        )

    g = nx.Graph()
    subjs = list(self.index_struct.table.keys())

    # add edges
    rel_map = self._graph_store.get_rel_map(subjs=subjs, depth=1, limit=limit)

    added_nodes = set()
    for keyword in rel_map:
        for path in rel_map[keyword]:
            subj = keyword
            for i in range(0, len(path), 2):
                if i + 2 >= len(path):
                    break

                if subj not in added_nodes:
                    g.add_node(subj)
                    added_nodes.add(subj)

                rel = path[i + 1]
                obj = path[i + 2]

                g.add_edge(subj, obj, label=rel, title=rel)
                subj = obj
    return g

```
 |  
| --- | --- |  
##  PropertyGraphIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.PropertyGraphIndex "Permanent link")
Bases: `BaseIndex[](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex "BaseIndex \(llama_index.core.indices.base.BaseIndex\)")[IndexLPG]`
An index for a property graph.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `Optional[Sequence[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "BaseNode \(llama_index.core.schema.BaseNode\)")]]`  |  A list of nodes to insert into the index.  |  `None`  |  
|  `llm`  |  `Optional[LLM[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM "LLM \(llama_index.core.llms.LLM\)")]`  |  The language model to use for extracting triplets. Defaults to `Settings.llm`.  |  `None`  |  
|  `kg_extractors`  |  `Optional[List[TransformComponent[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.TransformComponent "TransformComponent \(llama_index.core.schema.TransformComponent\)")]]`  |  A list of transformations to apply to the nodes to extract triplets. Defaults to `[SimpleLLMPathExtractor(llm=llm), ImplicitEdgeExtractor()]`.  |  `None`  |  
|  `property_graph_store`  |  `Optional[PropertyGraphStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore "PropertyGraphStore \(llama_index.core.graph_stores.types.PropertyGraphStore\)")]`  |  The property graph store to use. If not provided, a new `SimplePropertyGraphStore` will be created.  |  `None`  |  
|  `vector_store`  |  `Optional[BasePydanticVectorStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore "BasePydanticVectorStore \(llama_index.core.vector_stores.types.BasePydanticVectorStore\)")]`  |  The vector store index to use, if the graph store does not support vector queries.  |  `None`  |  
|  `use_async`  |  `bool`  |  Whether to use async for transformations. Defaults to `True`.  |  `True`  |  
|  `embed_model`  |  `Optional[EmbedType]`  |  The embedding model to use for embedding nodes. If not provided, `Settings.embed_model` will be used if `embed_kg_nodes=True`.  |  `None`  |  
|  `embed_kg_nodes`  |  `bool`  |  Whether to embed the KG nodes. Defaults to `True`.  |  `True`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.CallbackManager\)")]`  |  The callback manager to use.  |  `None`  |  
|  `transformations`  |  `Optional[List[TransformComponent[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.TransformComponent "TransformComponent \(llama_index.core.schema.TransformComponent\)")]]`  |  A list of transformations to apply to the nodes before inserting them into the index. These are applied prior to the `kg_extractors`.  |  `None`  |  
|  `storage_context`  |  `Optional[StorageContext[](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.storage.storage_context.StorageContext "StorageContext


  
      dataclass
   \(llama_index.core.storage.storage_context.StorageContext\)")]`  |  The storage context to use.  |  `None`  |  
|  `show_progress`  |  `bool`  |  Whether to show progress bars for transformations. Defaults to `False`.  |  `False`  |  
Source code in `llama-index-core/llama_index/core/indices/property_graph/base.py`  
| 
```
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
```
 | 
```
classPropertyGraphIndex(BaseIndex[IndexLPG]):
"""
    An index for a property graph.

    Args:
        nodes (Optional[Sequence[BaseNode]]):
            A list of nodes to insert into the index.
        llm (Optional[LLM]):
            The language model to use for extracting triplets. Defaults to `Settings.llm`.
        kg_extractors (Optional[List[TransformComponent]]):
            A list of transformations to apply to the nodes to extract triplets.
            Defaults to `[SimpleLLMPathExtractor(llm=llm), ImplicitEdgeExtractor()]`.
        property_graph_store (Optional[PropertyGraphStore]):
            The property graph store to use. If not provided, a new `SimplePropertyGraphStore` will be created.
        vector_store (Optional[BasePydanticVectorStore]):
            The vector store index to use, if the graph store does not support vector queries.
        use_async (bool):
            Whether to use async for transformations. Defaults to `True`.
        embed_model (Optional[EmbedType]):
            The embedding model to use for embedding nodes.
            If not provided, `Settings.embed_model` will be used if `embed_kg_nodes=True`.
        embed_kg_nodes (bool):
            Whether to embed the KG nodes. Defaults to `True`.
        callback_manager (Optional[CallbackManager]):
            The callback manager to use.
        transformations (Optional[List[TransformComponent]]):
            A list of transformations to apply to the nodes before inserting them into the index.
            These are applied prior to the `kg_extractors`.
        storage_context (Optional[StorageContext]):
            The storage context to use.
        show_progress (bool):
            Whether to show progress bars for transformations. Defaults to `False`.

    """

    index_struct_cls = IndexLPG

    def__init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        llm: Optional[LLM] = None,
        kg_extractors: Optional[List[TransformComponent]] = None,
        property_graph_store: Optional[PropertyGraphStore] = None,
        # vector related params
        vector_store: Optional[BasePydanticVectorStore] = None,
        use_async: bool = True,
        embed_model: Optional[EmbedType] = None,
        embed_kg_nodes: bool = True,
        # parent class params
        callback_manager: Optional[CallbackManager] = None,
        transformations: Optional[List[TransformComponent]] = None,
        storage_context: Optional[StorageContext] = None,
        show_progress: bool = False,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        storage_context = storage_context or StorageContext.from_defaults(
            property_graph_store=property_graph_store
        )

        # lazily initialize the graph store on the storage context
        if property_graph_store is not None:
            storage_context.property_graph_store = property_graph_store
        elif storage_context.property_graph_store is None:
            storage_context.property_graph_store = SimplePropertyGraphStore()

        if vector_store is not None:
            storage_context.vector_stores[DEFAULT_VECTOR_STORE] = vector_store

        if embed_kg_nodes and (
            storage_context.property_graph_store.supports_vector_queries
            or embed_kg_nodes
        ):
            self._embed_model = (
                resolve_embed_model(embed_model)
                if embed_model
                else Settings.embed_model
            )
        else:
            self._embed_model = None  # type: ignore

        self._kg_extractors = kg_extractors or [
            SimpleLLMPathExtractor(llm=llm or Settings.llm),
            ImplicitPathExtractor(),
        ]
        self._use_async = use_async
        self._llm = llm
        self._embed_kg_nodes = embed_kg_nodes
        self._override_vector_store = (
            vector_store is not None
            or not storage_context.property_graph_store.supports_vector_queries
        )

        super().__init__(
            nodes=nodes,
            callback_manager=callback_manager,
            storage_context=storage_context,
            transformations=transformations,
            show_progress=show_progress,
            **kwargs,
        )

    @classmethod
    deffrom_existing(
        cls: Type["PropertyGraphIndex"],
        property_graph_store: PropertyGraphStore,
        vector_store: Optional[BasePydanticVectorStore] = None,
        # general params
        llm: Optional[LLM] = None,
        kg_extractors: Optional[List[TransformComponent]] = None,
        # vector related params
        use_async: bool = True,
        embed_model: Optional[EmbedType] = None,
        embed_kg_nodes: bool = True,
        # parent class params
        callback_manager: Optional[CallbackManager] = None,
        transformations: Optional[List[TransformComponent]] = None,
        storage_context: Optional[StorageContext] = None,
        show_progress: bool = False,
        **kwargs: Any,
    ) -> "PropertyGraphIndex":
"""Create an index from an existing property graph store (and optional vector store)."""
        return cls(
            nodes=[],  # no nodes to insert
            property_graph_store=property_graph_store,
            vector_store=vector_store,
            llm=llm,
            kg_extractors=kg_extractors,
            use_async=use_async,
            embed_model=embed_model,
            embed_kg_nodes=embed_kg_nodes,
            callback_manager=callback_manager,
            transformations=transformations,
            storage_context=storage_context,
            show_progress=show_progress,
            **kwargs,
        )

    @property
    defproperty_graph_store(self) -> PropertyGraphStore:
"""Get the labelled property graph store."""
        assert self.storage_context.property_graph_store is not None

        return self.storage_context.property_graph_store

    @property
    defvector_store(self) -> Optional[BasePydanticVectorStore]:
        if self._embed_kg_nodes and self._override_vector_store:
            return self.storage_context.vector_store
        else:
            return None

    def_insert_nodes(self, nodes: Sequence[BaseNode]) -> Sequence[BaseNode]:
"""Insert nodes to the index struct."""
        if len(nodes) == 0:
            return nodes

        # run transformations on nodes to extract triplets
        if self._use_async:
            nodes = asyncio.run(
                arun_transformations(
                    nodes, self._kg_extractors, show_progress=self._show_progress
                )
            )
        else:
            nodes = run_transformations(
                nodes, self._kg_extractors, show_progress=self._show_progress
            )

        # ensure all nodes have nodes and/or relations in metadata
        assert all(
            node.metadata.get(KG_NODES_KEY) is not None
            or node.metadata.get(KG_RELATIONS_KEY) is not None
            for node in nodes
        )

        kg_nodes_to_insert: List[LabelledNode] = []
        kg_rels_to_insert: List[Relation] = []
        for node in nodes:
            # remove nodes and relations from metadata
            kg_nodes = node.metadata.pop(KG_NODES_KEY, [])
            kg_rels = node.metadata.pop(KG_RELATIONS_KEY, [])

            # add source id to properties
            for kg_node in kg_nodes:
                kg_node.properties[TRIPLET_SOURCE_KEY] = node.id_
            for kg_rel in kg_rels:
                kg_rel.properties[TRIPLET_SOURCE_KEY] = node.id_

            # add nodes and relations to insert lists
            kg_nodes_to_insert.extend(kg_nodes)
            kg_rels_to_insert.extend(kg_rels)

        # filter out duplicate kg nodes
        kg_node_ids = {node.id for node in kg_nodes_to_insert}
        existing_kg_nodes = self.property_graph_store.get(ids=list(kg_node_ids))
        existing_kg_node_ids = {node.id for node in existing_kg_nodes}
        kg_nodes_to_insert = [
            node for node in kg_nodes_to_insert if node.id not in existing_kg_node_ids
        ]

        # filter out duplicate llama nodes
        existing_nodes = self.property_graph_store.get_llama_nodes(
            [node.id_ for node in nodes]
        )
        existing_node_hashes = {node.hash for node in existing_nodes}
        nodes = [node for node in nodes if node.hash not in existing_node_hashes]

        # embed nodes (if needed)
        if self._embed_kg_nodes:
            # embed llama-index nodes
            node_texts = [
                node.get_content(metadata_mode=MetadataMode.EMBED) for node in nodes
            ]

            if self._use_async:
                embeddings = asyncio.run(
                    self._embed_model.aget_text_embedding_batch(
                        node_texts, show_progress=self._show_progress
                    )
                )
            else:
                embeddings = self._embed_model.get_text_embedding_batch(
                    node_texts, show_progress=self._show_progress
                )

            for node, embedding in zip(nodes, embeddings):
                node.embedding = embedding

            # embed kg nodes
            kg_node_texts = [str(kg_node) for kg_node in kg_nodes_to_insert]

            if self._use_async:
                kg_embeddings = asyncio.run(
                    self._embed_model.aget_text_embedding_batch(
                        kg_node_texts, show_progress=self._show_progress
                    )
                )
            else:
                kg_embeddings = self._embed_model.get_text_embedding_batch(
                    kg_node_texts,
                    show_progress=self._show_progress,
                )

            for kg_node, embedding in zip(kg_nodes_to_insert, kg_embeddings):
                kg_node.embedding = embedding

        # if graph store doesn't support vectors, or the vector index was provided, use it
        if self.vector_store is not None and len(kg_nodes_to_insert)  0:
            self._insert_nodes_to_vector_index(kg_nodes_to_insert)

        if len(nodes)  0:
            self.property_graph_store.upsert_llama_nodes(nodes)

        if len(kg_nodes_to_insert)  0:
            self.property_graph_store.upsert_nodes(kg_nodes_to_insert)

        # important: upsert relations after nodes
        if len(kg_rels_to_insert)  0:
            self.property_graph_store.upsert_relations(kg_rels_to_insert)

        # refresh schema if needed
        if self.property_graph_store.supports_structured_queries:
            self.property_graph_store.get_schema(refresh=True)

        return nodes

    def_insert_nodes_to_vector_index(self, nodes: List[LabelledNode]) -> None:
"""Insert vector nodes."""
        assert self.vector_store is not None

        llama_nodes: List[TextNode] = []
        for node in nodes:
            if node.embedding is not None:
                llama_nodes.append(
                    TextNode(
                        text=str(node),
                        metadata={VECTOR_SOURCE_KEY: node.id, **node.properties},
                        embedding=[*node.embedding],
                    )
                )
                if not self.vector_store.stores_text:
                    llama_nodes[-1].id_ = node.id

            # clear the embedding to save memory, its not used now
            node.embedding = None

        self.vector_store.add(llama_nodes)

    def_build_index_from_nodes(
        self, nodes: Optional[Sequence[BaseNode]], **build_kwargs: Any
    ) -> IndexLPG:
"""Build index from nodes."""
        nodes = self._insert_nodes(nodes or [])

        # this isn't really used or needed
        return IndexLPG()

    defas_retriever(
        self,
        sub_retrievers: Optional[List["BasePGRetriever"]] = None,
        include_text: bool = True,
        **kwargs: Any,
    ) -> BaseRetriever:
"""
        Return a retriever for the index.

        Args:
            sub_retrievers (Optional[List[BasePGRetriever]]):
                A list of sub-retrievers to use. If not provided, a default list will be used:
                `[LLMSynonymRetriever, VectorContextRetriever]` if the graph store supports vector queries.
            include_text (bool):
                Whether to include source-text in the retriever results.
            **kwargs:
                Additional kwargs to pass to the retriever.

        """
        fromllama_index.core.indices.property_graph.retrieverimport (
            PGRetriever,
        )
        fromllama_index.core.indices.property_graph.sub_retrievers.vectorimport (
            VectorContextRetriever,
        )
        fromllama_index.core.indices.property_graph.sub_retrievers.llm_synonymimport (
            LLMSynonymRetriever,
        )

        if sub_retrievers is None:
            sub_retrievers = [
                LLMSynonymRetriever(
                    graph_store=self.property_graph_store,
                    include_text=include_text,
                    llm=self._llm,
                    **kwargs,
                ),
            ]

            if self._embed_model and (
                self.property_graph_store.supports_vector_queries or self.vector_store
            ):
                sub_retrievers.append(
                    VectorContextRetriever(
                        graph_store=self.property_graph_store,
                        vector_store=self.vector_store,
                        include_text=include_text,
                        embed_model=self._embed_model,
                        **kwargs,
                    )
                )

        return PGRetriever(sub_retrievers, use_async=self._use_async, **kwargs)

    def_delete_node(self, node_id: str, **delete_kwargs: Any) -> None:
"""Delete a node."""
        self.property_graph_store.delete(ids=[node_id])

    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Index-specific logic for inserting nodes to the index struct."""
        self._insert_nodes(nodes)

    @property
    defref_doc_info(self) -> Dict[str, RefDocInfo]:
"""Retrieve a dict mapping of ingested documents and their nodes+metadata."""
        raise NotImplementedError(
            "Ref doc info not implemented for PropertyGraphIndex. "
            "All inserts are already upserts."
        )

```
 |  
| --- | --- |  
###  property_graph_store `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.PropertyGraphIndex.property_graph_store "Permanent link")

```
property_graph_store: 

```

Get the labelled property graph store.
###  ref_doc_info `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.PropertyGraphIndex.ref_doc_info "Permanent link")

```
ref_doc_info: [, ]

```

Retrieve a dict mapping of ingested documents and their nodes+metadata.
###  from_existing `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.PropertyGraphIndex.from_existing "Permanent link")

```
from_existing(
    property_graph_store: ,
    vector_store: Optional[] = None,
    llm: Optional[] = None,
    kg_extractors: Optional[
        []
    ] = None,
    use_async:  = True,
    embed_model: Optional[EmbedType] = None,
    embed_kg_nodes:  = True,
    callback_manager: Optional[] = None,
    transformations: Optional[
        []
    ] = None,
    storage_context: Optional[] = None,
    show_progress:  = False,
    **kwargs: 
) -> 

```

Create an index from an existing property graph store (and optional vector store).
Source code in `llama-index-core/llama_index/core/indices/property_graph/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_existing(
    cls: Type["PropertyGraphIndex"],
    property_graph_store: PropertyGraphStore,
    vector_store: Optional[BasePydanticVectorStore] = None,
    # general params
    llm: Optional[LLM] = None,
    kg_extractors: Optional[List[TransformComponent]] = None,
    # vector related params
    use_async: bool = True,
    embed_model: Optional[EmbedType] = None,
    embed_kg_nodes: bool = True,
    # parent class params
    callback_manager: Optional[CallbackManager] = None,
    transformations: Optional[List[TransformComponent]] = None,
    storage_context: Optional[StorageContext] = None,
    show_progress: bool = False,
    **kwargs: Any,
) -> "PropertyGraphIndex":
"""Create an index from an existing property graph store (and optional vector store)."""
    return cls(
        nodes=[],  # no nodes to insert
        property_graph_store=property_graph_store,
        vector_store=vector_store,
        llm=llm,
        kg_extractors=kg_extractors,
        use_async=use_async,
        embed_model=embed_model,
        embed_kg_nodes=embed_kg_nodes,
        callback_manager=callback_manager,
        transformations=transformations,
        storage_context=storage_context,
        show_progress=show_progress,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  as_retriever [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.PropertyGraphIndex.as_retriever "Permanent link")

```
as_retriever(
    sub_retrievers: Optional[[]] = None,
    include_text:  = True,
    **kwargs: 
) -> 

```

Return a retriever for the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `sub_retrievers`  |  `Optional[List[BasePGRetriever[](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/auto_merging/#llama_index.core.retrievers.BasePGRetriever "BasePGRetriever \(llama_index.core.indices.property_graph.sub_retrievers.base.BasePGRetriever\)")]]`  |  A list of sub-retrievers to use. If not provided, a default list will be used: `[LLMSynonymRetriever, VectorContextRetriever]` if the graph store supports vector queries.  |  `None`  |  
|  `include_text`  |  `bool`  |  Whether to include source-text in the retriever results.  |  `True`  |  
|  `**kwargs`  |  Additional kwargs to pass to the retriever.  |  
Source code in `llama-index-core/llama_index/core/indices/property_graph/base.py`  
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
```
 | 
```
defas_retriever(
    self,
    sub_retrievers: Optional[List["BasePGRetriever"]] = None,
    include_text: bool = True,
    **kwargs: Any,
) -> BaseRetriever:
"""
    Return a retriever for the index.

    Args:
        sub_retrievers (Optional[List[BasePGRetriever]]):
            A list of sub-retrievers to use. If not provided, a default list will be used:
            `[LLMSynonymRetriever, VectorContextRetriever]` if the graph store supports vector queries.
        include_text (bool):
            Whether to include source-text in the retriever results.
        **kwargs:
            Additional kwargs to pass to the retriever.

    """
    fromllama_index.core.indices.property_graph.retrieverimport (
        PGRetriever,
    )
    fromllama_index.core.indices.property_graph.sub_retrievers.vectorimport (
        VectorContextRetriever,
    )
    fromllama_index.core.indices.property_graph.sub_retrievers.llm_synonymimport (
        LLMSynonymRetriever,
    )

    if sub_retrievers is None:
        sub_retrievers = [
            LLMSynonymRetriever(
                graph_store=self.property_graph_store,
                include_text=include_text,
                llm=self._llm,
                **kwargs,
            ),
        ]

        if self._embed_model and (
            self.property_graph_store.supports_vector_queries or self.vector_store
        ):
            sub_retrievers.append(
                VectorContextRetriever(
                    graph_store=self.property_graph_store,
                    vector_store=self.vector_store,
                    include_text=include_text,
                    embed_model=self._embed_model,
                    **kwargs,
                )
            )

    return PGRetriever(sub_retrievers, use_async=self._use_async, **kwargs)

```
 |  
| --- | --- |  
##  RAKEKeywordTableIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.RAKEKeywordTableIndex "Permanent link")
Bases: `BaseKeywordTableIndex`
RAKE Keyword Table Index.
This index uses a RAKE keyword extractor to extract keywords from the text.
Source code in `llama-index-core/llama_index/core/indices/keyword_table/rake_base.py`  
| 
```
18
19
20
21
22
23
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
```
 | 
```
classRAKEKeywordTableIndex(BaseKeywordTableIndex):
"""
    RAKE Keyword Table Index.

    This index uses a RAKE keyword extractor to extract keywords from the text.

    """

    def_extract_keywords(self, text: str) -> Set[str]:
"""Extract keywords from text."""
        return rake_extract_keywords(text, max_keywords=self.max_keywords_per_chunk)

    defas_retriever(
        self,
        retriever_mode: Union[
            str, KeywordTableRetrieverMode
        ] = KeywordTableRetrieverMode.RAKE,
        **kwargs: Any,
    ) -> BaseRetriever:
        return super().as_retriever(retriever_mode=retriever_mode, **kwargs)

```
 |  
| --- | --- |  
##  SimpleKeywordTableIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SimpleKeywordTableIndex "Permanent link")
Bases: `BaseKeywordTableIndex`
Simple Keyword Table Index.
This index uses a simple regex extractor to extract keywords from the text.
Source code in `llama-index-core/llama_index/core/indices/keyword_table/simple_base.py`  
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
```
 | 
```
classSimpleKeywordTableIndex(BaseKeywordTableIndex):
"""
    Simple Keyword Table Index.

    This index uses a simple regex extractor to extract keywords from the text.

    """

    def_extract_keywords(self, text: str) -> Set[str]:
"""Extract keywords from text."""
        return simple_extract_keywords(text, self.max_keywords_per_chunk)

    defas_retriever(
        self,
        retriever_mode: Union[
            str, KeywordTableRetrieverMode
        ] = KeywordTableRetrieverMode.SIMPLE,
        **kwargs: Any,
    ) -> BaseRetriever:
        return super().as_retriever(retriever_mode=retriever_mode, **kwargs)

```
 |  
| --- | --- |  
##  SummaryIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SummaryIndex "Permanent link")
Bases: `BaseIndex[](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex "BaseIndex \(llama_index.core.indices.base.BaseIndex\)")[IndexList]`
Summary Index.
The summary index is a simple data structure where nodes are stored in a sequence. During index construction, the document texts are chunked up, converted to nodes, and stored in a list.
During query time, the summary index iterates through the nodes with some optional filter parameters, and synthesizes an answer from all the nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `text_qa_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A Question-Answer Prompt (see :ref:`Prompt-Templates`). NOTE: this is a deprecated field.  |  _required_  |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
Source code in `llama-index-core/llama_index/core/indices/list/base.py`  
| 
```
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
```
 | 
```
classSummaryIndex(BaseIndex[IndexList]):
"""
    Summary Index.

    The summary index is a simple data structure where nodes are stored in
    a sequence. During index construction, the document texts are
    chunked up, converted to nodes, and stored in a list.

    During query time, the summary index iterates through the nodes
    with some optional filter parameters, and synthesizes an
    answer from all the nodes.

    Args:
        text_qa_template (Optional[BasePromptTemplate]): A Question-Answer Prompt
            (see :ref:`Prompt-Templates`).
            NOTE: this is a deprecated field.
        show_progress (bool): Whether to show tqdm progress bars. Defaults to False.

    """

    index_struct_cls = IndexList

    def__init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        objects: Optional[Sequence[IndexNode]] = None,
        index_struct: Optional[IndexList] = None,
        show_progress: bool = False,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        super().__init__(
            nodes=nodes,
            index_struct=index_struct,
            show_progress=show_progress,
            objects=objects,
            **kwargs,
        )

    defas_retriever(
        self,
        retriever_mode: Union[str, ListRetrieverMode] = ListRetrieverMode.DEFAULT,
        llm: Optional[LLM] = None,
        embed_model: Optional[BaseEmbedding] = None,
        **kwargs: Any,
    ) -> BaseRetriever:
        fromllama_index.core.indices.list.retrieversimport (
            SummaryIndexEmbeddingRetriever,
            SummaryIndexLLMRetriever,
            SummaryIndexRetriever,
        )

        if retriever_mode == ListRetrieverMode.DEFAULT:
            return SummaryIndexRetriever(self, object_map=self._object_map, **kwargs)
        elif retriever_mode == ListRetrieverMode.EMBEDDING:
            embed_model = embed_model or Settings.embed_model
            return SummaryIndexEmbeddingRetriever(
                self, object_map=self._object_map, embed_model=embed_model, **kwargs
            )
        elif retriever_mode == ListRetrieverMode.LLM:
            llm = llm or Settings.llm
            return SummaryIndexLLMRetriever(
                self, object_map=self._object_map, llm=llm, **kwargs
            )
        else:
            raise ValueError(f"Unknown retriever mode: {retriever_mode}")

    def_build_index_from_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **build_kwargs: Any,
    ) -> IndexList:
"""
        Build the index from documents.

        Args:
            documents (List[BaseDocument]): A list of documents.

        Returns:
            IndexList: The created summary index.

        """
        index_struct = IndexList()
        nodes_with_progress = get_tqdm_iterable(
            nodes, show_progress, "Processing nodes"
        )
        for n in nodes_with_progress:
            index_struct.add_node(n)
        return index_struct

    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Insert a document."""
        for n in nodes:
            self._index_struct.add_node(n)

    def_delete_node(self, node_id: str, **delete_kwargs: Any) -> None:
"""Delete a node."""
        cur_node_ids = self._index_struct.nodes
        cur_nodes = self._docstore.get_nodes(cur_node_ids)
        nodes_to_keep = [n for n in cur_nodes if n.node_id != node_id]
        self._index_struct.nodes = [n.node_id for n in nodes_to_keep]

    @property
    defref_doc_info(self) -> Dict[str, RefDocInfo]:
"""Retrieve a dict mapping of ingested documents and their nodes+metadata."""
        node_doc_ids = self._index_struct.nodes
        nodes = self.docstore.get_nodes(node_doc_ids)

        all_ref_doc_info = {}
        for node in nodes:
            ref_node = node.source_node
            if not ref_node:
                continue

            ref_doc_info = self.docstore.get_ref_doc_info(ref_node.node_id)
            if not ref_doc_info:
                continue

            all_ref_doc_info[ref_node.node_id] = ref_doc_info
        return all_ref_doc_info

```
 |  
| --- | --- |  
###  ref_doc_info `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SummaryIndex.ref_doc_info "Permanent link")

```
ref_doc_info: [, ]

```

Retrieve a dict mapping of ingested documents and their nodes+metadata.
##  TreeIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.TreeIndex "Permanent link")
Bases: `BaseIndex[](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex "BaseIndex \(llama_index.core.indices.base.BaseIndex\)")[IndexGraph]`
Tree Index.
The tree index is a tree-structured index, where each node is a summary of the children nodes. During index construction, the tree is constructed in a bottoms-up fashion until we end up with a set of root_nodes.
There are a few different options during query time (see :ref:`Ref-Query`). The main option is to traverse down the tree from the root nodes. A secondary answer is to directly synthesize the answer from the root nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `summary_template`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A Summarization Prompt (see :ref:`Prompt-Templates`).  |  `None`  |  
|  `insert_prompt`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  An Tree Insertion Prompt (see :ref:`Prompt-Templates`).  |  `None`  |  
|  `num_children`  |  The number of children each node should have.  |  
|  `build_tree`  |  `bool`  |  Whether to build the tree during index construction.  |  `True`  |  
|  `show_progress`  |  `bool`  |  Whether to show progress bars. Defaults to False.  |  `False`  |  
Source code in `llama-index-core/llama_index/core/indices/tree/base.py`  
| 
```
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
```
 | 
```
classTreeIndex(BaseIndex[IndexGraph]):
"""
    Tree Index.

    The tree index is a tree-structured index, where each node is a summary of
    the children nodes. During index construction, the tree is constructed
    in a bottoms-up fashion until we end up with a set of root_nodes.

    There are a few different options during query time (see :ref:`Ref-Query`).
    The main option is to traverse down the tree from the root nodes.
    A secondary answer is to directly synthesize the answer from the root nodes.

    Args:
        summary_template (Optional[BasePromptTemplate]): A Summarization Prompt
            (see :ref:`Prompt-Templates`).
        insert_prompt (Optional[BasePromptTemplate]): An Tree Insertion Prompt
            (see :ref:`Prompt-Templates`).
        num_children (int): The number of children each node should have.
        build_tree (bool): Whether to build the tree during index construction.
        show_progress (bool): Whether to show progress bars. Defaults to False.

    """

    index_struct_cls = IndexGraph

    def__init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        objects: Optional[Sequence[IndexNode]] = None,
        index_struct: Optional[IndexGraph] = None,
        llm: Optional[LLM] = None,
        summary_template: Optional[BasePromptTemplate] = None,
        insert_prompt: Optional[BasePromptTemplate] = None,
        num_children: int = 10,
        build_tree: bool = True,
        use_async: bool = False,
        show_progress: bool = False,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        # need to set parameters before building index in base class.
        self.num_children = num_children
        self.summary_template = summary_template or DEFAULT_SUMMARY_PROMPT
        self.insert_prompt: BasePromptTemplate = insert_prompt or DEFAULT_INSERT_PROMPT
        self.build_tree = build_tree
        self._use_async = use_async
        self._llm = llm or Settings.llm
        super().__init__(
            nodes=nodes,
            index_struct=index_struct,
            show_progress=show_progress,
            objects=objects,
            **kwargs,
        )

    defas_retriever(
        self,
        retriever_mode: Union[str, TreeRetrieverMode] = TreeRetrieverMode.SELECT_LEAF,
        embed_model: Optional[BaseEmbedding] = None,
        **kwargs: Any,
    ) -> BaseRetriever:
        # NOTE: lazy import
        fromllama_index.core.indices.tree.all_leaf_retrieverimport (
            TreeAllLeafRetriever,
        )
        fromllama_index.core.indices.tree.select_leaf_embedding_retrieverimport (
            TreeSelectLeafEmbeddingRetriever,
        )
        fromllama_index.core.indices.tree.select_leaf_retrieverimport (
            TreeSelectLeafRetriever,
        )
        fromllama_index.core.indices.tree.tree_root_retrieverimport (
            TreeRootRetriever,
        )

        self._validate_build_tree_required(TreeRetrieverMode(retriever_mode))

        if retriever_mode == TreeRetrieverMode.SELECT_LEAF:
            return TreeSelectLeafRetriever(self, object_map=self._object_map, **kwargs)
        elif retriever_mode == TreeRetrieverMode.SELECT_LEAF_EMBEDDING:
            embed_model = embed_model or Settings.embed_model
            return TreeSelectLeafEmbeddingRetriever(
                self, embed_model=embed_model, object_map=self._object_map, **kwargs
            )
        elif retriever_mode == TreeRetrieverMode.ROOT:
            return TreeRootRetriever(self, object_map=self._object_map, **kwargs)
        elif retriever_mode == TreeRetrieverMode.ALL_LEAF:
            return TreeAllLeafRetriever(self, object_map=self._object_map, **kwargs)
        else:
            raise ValueError(f"Unknown retriever mode: {retriever_mode}")

    def_validate_build_tree_required(self, retriever_mode: TreeRetrieverMode) -> None:
"""Check if index supports modes that require trees."""
        if retriever_mode in REQUIRE_TREE_MODES and not self.build_tree:
            raise ValueError(
                "Index was constructed without building trees, "
                f"but retriever mode {retriever_mode} requires trees."
            )

    def_build_index_from_nodes(
        self, nodes: Sequence[BaseNode], **build_kwargs: Any
    ) -> IndexGraph:
"""Build the index from nodes."""
        index_builder = GPTTreeIndexBuilder(
            self.num_children,
            self.summary_template,
            llm=self._llm,
            use_async=self._use_async,
            show_progress=self._show_progress,
            docstore=self._docstore,
        )
        return index_builder.build_from_nodes(nodes, build_tree=self.build_tree)

    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Insert a document."""
        # TODO: allow to customize insert prompt
        inserter = TreeIndexInserter(
            self.index_struct,
            llm=self._llm,
            num_children=self.num_children,
            insert_prompt=self.insert_prompt,
            summary_prompt=self.summary_template,
            docstore=self._docstore,
        )
        inserter.insert(nodes)

    def_delete_node(self, node_id: str, **delete_kwargs: Any) -> None:
"""Delete a node."""
        raise NotImplementedError("Delete not implemented for tree index.")

    @property
    defref_doc_info(self) -> Dict[str, RefDocInfo]:
"""Retrieve a dict mapping of ingested documents and their nodes+metadata."""
        node_doc_ids = list(self.index_struct.all_nodes.values())
        nodes = self.docstore.get_nodes(node_doc_ids)

        all_ref_doc_info = {}
        for node in nodes:
            ref_node = node.source_node
            if not ref_node:
                continue

            ref_doc_info = self.docstore.get_ref_doc_info(ref_node.node_id)
            if not ref_doc_info:
                continue

            all_ref_doc_info[ref_node.node_id] = ref_doc_info
        return all_ref_doc_info

```
 |  
| --- | --- |  
###  ref_doc_info `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.TreeIndex.ref_doc_info "Permanent link")

```
ref_doc_info: [, ]

```

Retrieve a dict mapping of ingested documents and their nodes+metadata.
##  VectorStoreIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.VectorStoreIndex "Permanent link")
Bases: `BaseIndex[](https://developers.llamaindex.ai/python/framework-api-reference/indices/#llama_index.core.indices.base.BaseIndex "BaseIndex \(llama_index.core.indices.base.BaseIndex\)")[IndexDict]`
Vector Store Index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `use_async`  |  `bool`  |  Whether to use asynchronous calls. Defaults to False.  |  `False`  |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
|  `store_nodes_override`  |  `bool`  |  set to True to always store Node objects in index store and document store even if vector store keeps text. Defaults to False  |  `False`  |  
Source code in `llama-index-core/llama_index/core/indices/vector_store/base.py`  
| 
```
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
```
 | 
```
classVectorStoreIndex(BaseIndex[IndexDict]):
"""
    Vector Store Index.

    Args:
        use_async (bool): Whether to use asynchronous calls. Defaults to False.
        show_progress (bool): Whether to show tqdm progress bars. Defaults to False.
        store_nodes_override (bool): set to True to always store Node objects in index
            store and document store even if vector store keeps text. Defaults to False

    """

    index_struct_cls = IndexDict

    def__init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        # vector store index params
        use_async: bool = False,
        store_nodes_override: bool = False,
        embed_model: Optional[EmbedType] = None,
        insert_batch_size: int = 2048,
        # parent class params
        objects: Optional[Sequence[IndexNode]] = None,
        index_struct: Optional[IndexDict] = None,
        storage_context: Optional[StorageContext] = None,
        callback_manager: Optional[CallbackManager] = None,
        transformations: Optional[List[TransformComponent]] = None,
        show_progress: bool = False,
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        self._use_async = use_async
        self._store_nodes_override = store_nodes_override
        self._embed_model = resolve_embed_model(
            embed_model or Settings.embed_model, callback_manager=callback_manager
        )

        self._insert_batch_size = insert_batch_size
        super().__init__(
            nodes=nodes,
            index_struct=index_struct,
            storage_context=storage_context,
            show_progress=show_progress,
            objects=objects,
            callback_manager=callback_manager,
            transformations=transformations,
            **kwargs,
        )

    @classmethod
    deffrom_vector_store(
        cls,
        vector_store: BasePydanticVectorStore,
        embed_model: Optional[EmbedType] = None,
        **kwargs: Any,
    ) -> "VectorStoreIndex":
        if not vector_store.stores_text:
            raise ValueError(
                "Cannot initialize from a vector store that does not store text."
            )

        kwargs.pop("storage_context", None)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        return cls(
            nodes=[],
            embed_model=embed_model,
            storage_context=storage_context,
            **kwargs,
        )

    @property
    defvector_store(self) -> BasePydanticVectorStore:
        return self._vector_store

    defas_retriever(self, **kwargs: Any) -> BaseRetriever:
        # NOTE: lazy import
        fromllama_index.core.indices.vector_store.retrieversimport (
            VectorIndexRetriever,
        )

        return VectorIndexRetriever(
            self,
            node_ids=list(self.index_struct.nodes_dict.values()),
            callback_manager=self._callback_manager,
            object_map=self._object_map,
            **kwargs,
        )

    def_get_node_with_embedding(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
    ) -> List[BaseNode]:
"""
        Get tuples of id, node, and embedding.

        Allows us to store these nodes in a vector store.
        Embeddings are called in batches.

        """
        id_to_embed_map = embed_nodes(
            nodes, self._embed_model, show_progress=show_progress
        )

        results = []
        for node in nodes:
            embedding = id_to_embed_map[node.node_id]
            result = node.model_copy()
            result.embedding = embedding
            results.append(result)
        return results

    async def_aget_node_with_embedding(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
    ) -> List[BaseNode]:
"""
        Asynchronously get tuples of id, node, and embedding.

        Allows us to store these nodes in a vector store.
        Embeddings are called in batches.

        """
        id_to_embed_map = await async_embed_nodes(
            nodes=nodes,
            embed_model=self._embed_model,
            show_progress=show_progress,
        )

        results = []
        for node in nodes:
            embedding = id_to_embed_map[node.node_id]
            result = node.model_copy()
            result.embedding = embedding
            results.append(result)
        return results

    async def_async_add_nodes_to_index(
        self,
        index_struct: IndexDict,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **insert_kwargs: Any,
    ) -> None:
"""Asynchronously add nodes to index."""
        if not nodes:
            return

        for nodes_batch in iter_batch(nodes, self._insert_batch_size):
            nodes_batch = await self._aget_node_with_embedding(
                nodes_batch, show_progress
            )
            new_ids = await self._vector_store.async_add(nodes_batch, **insert_kwargs)

            # if the vector store doesn't store text, we need to add the nodes to the
            # index struct and document store
            if not self._vector_store.stores_text or self._store_nodes_override:
                for node, new_id in zip(nodes_batch, new_ids):
                    # NOTE: remove embedding from node to avoid duplication
                    node_without_embedding = node.model_copy()
                    node_without_embedding.embedding = None

                    index_struct.add_node(node_without_embedding, text_id=new_id)
                    await self._docstore.async_add_documents(
                        [node_without_embedding], allow_update=True
                    )
            else:
                # NOTE: if the vector store keeps text,
                # we only need to add image and index nodes
                for node, new_id in zip(nodes_batch, new_ids):
                    if isinstance(node, (ImageNode, IndexNode)):
                        # NOTE: remove embedding from node to avoid duplication
                        node_without_embedding = node.model_copy()
                        node_without_embedding.embedding = None

                        index_struct.add_node(node_without_embedding, text_id=new_id)
                        await self._docstore.async_add_documents(
                            [node_without_embedding], allow_update=True
                        )

    def_add_nodes_to_index(
        self,
        index_struct: IndexDict,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **insert_kwargs: Any,
    ) -> None:
"""Add document to index."""
        if not nodes:
            return

        for nodes_batch in iter_batch(nodes, self._insert_batch_size):
            nodes_batch = self._get_node_with_embedding(nodes_batch, show_progress)
            new_ids = self._vector_store.add(nodes_batch, **insert_kwargs)

            if not self._vector_store.stores_text or self._store_nodes_override:
                # NOTE: if the vector store doesn't store text,
                # we need to add the nodes to the index struct and document store
                for node, new_id in zip(nodes_batch, new_ids):
                    # NOTE: remove embedding from node to avoid duplication
                    node_without_embedding = node.model_copy()
                    node_without_embedding.embedding = None

                    index_struct.add_node(node_without_embedding, text_id=new_id)
                    self._docstore.add_documents(
                        [node_without_embedding], allow_update=True
                    )
            else:
                # NOTE: if the vector store keeps text,
                # we only need to add image and index nodes
                for node, new_id in zip(nodes_batch, new_ids):
                    if isinstance(node, (ImageNode, IndexNode)):
                        # NOTE: remove embedding from node to avoid duplication
                        node_without_embedding = node.model_copy()
                        node_without_embedding.embedding = None

                        index_struct.add_node(node_without_embedding, text_id=new_id)
                        self._docstore.add_documents(
                            [node_without_embedding], allow_update=True
                        )

    def_build_index_from_nodes(
        self,
        nodes: Sequence[BaseNode],
        **insert_kwargs: Any,
    ) -> IndexDict:
"""Build index from nodes."""
        index_struct = self.index_struct_cls()
        if self._use_async:
            tasks = [
                self._async_add_nodes_to_index(
                    index_struct,
                    nodes,
                    show_progress=self._show_progress,
                    **insert_kwargs,
                )
            ]
            run_async_tasks(tasks)
        else:
            self._add_nodes_to_index(
                index_struct,
                nodes,
                show_progress=self._show_progress,
                **insert_kwargs,
            )
        return index_struct

    defbuild_index_from_nodes(
        self,
        nodes: Sequence[BaseNode],
        **insert_kwargs: Any,
    ) -> IndexDict:
"""
        Build the index from nodes.

        NOTE: Overrides BaseIndex.build_index_from_nodes.
            VectorStoreIndex only stores nodes in document store
            if vector store does not store text
        """
        # Filter out the nodes that don't have content
        content_nodes = [
            node
            for node in nodes
            if node.get_content(metadata_mode=MetadataMode.EMBED) != ""
        ]

        # Report if some nodes are missing content
        if len(content_nodes) != len(nodes):
            print("Some nodes are missing content, skipping them...")

        return self._build_index_from_nodes(content_nodes, **insert_kwargs)

    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Insert a document."""
        self._add_nodes_to_index(self._index_struct, nodes, **insert_kwargs)

    def_validate_serializable(self, nodes: Sequence[BaseNode]) -> None:
"""Validate that the nodes are serializable."""
        for node in nodes:
            if isinstance(node, IndexNode):
                try:
                    node.dict()
                except ValueError:
                    self._object_map[node.index_id] = node.obj
                    node.obj = None

    async defainsert_nodes(
        self, nodes: Sequence[BaseNode], **insert_kwargs: Any
    ) -> None:
"""
        Insert nodes.

        NOTE: overrides BaseIndex.ainsert_nodes.
            VectorStoreIndex only stores nodes in document store
            if vector store does not store text
        """
        self._validate_serializable(nodes)

        with self._callback_manager.as_trace("insert_nodes"):
            await self._async_add_nodes_to_index(
                self._index_struct, nodes, **insert_kwargs
            )
            self._storage_context.index_store.add_index_struct(self._index_struct)

    definsert_nodes(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""
        Insert nodes.

        NOTE: overrides BaseIndex.insert_nodes.
            VectorStoreIndex only stores nodes in document store
            if vector store does not store text
        """
        self._validate_serializable(nodes)

        with self._callback_manager.as_trace("insert_nodes"):
            self._insert(nodes, **insert_kwargs)
            self._storage_context.index_store.add_index_struct(self._index_struct)

    def_delete_node(self, node_id: str, **delete_kwargs: Any) -> None:
        pass

    async defadelete_nodes(
        self,
        node_ids: List[str],
        delete_from_docstore: bool = False,
        **delete_kwargs: Any,
    ) -> None:
"""
        Delete a list of nodes from the index.

        Args:
            node_ids (List[str]): A list of node_ids from the nodes to delete

        """
        # delete nodes from vector store
        await self._vector_store.adelete_nodes(node_ids, **delete_kwargs)

        # delete from docstore only if needed
        if (
            not self._vector_store.stores_text or self._store_nodes_override
        ) and delete_from_docstore:
            for node_id in node_ids:
                self._index_struct.delete(node_id)
                await self._docstore.adelete_document(node_id, raise_error=False)
            self._storage_context.index_store.add_index_struct(self._index_struct)

    defdelete_nodes(
        self,
        node_ids: List[str],
        delete_from_docstore: bool = False,
        **delete_kwargs: Any,
    ) -> None:
"""
        Delete a list of nodes from the index.

        Args:
            node_ids (List[str]): A list of node_ids from the nodes to delete

        """
        # delete nodes from vector store
        self._vector_store.delete_nodes(node_ids, **delete_kwargs)

        # delete from docstore only if needed
        if (
            not self._vector_store.stores_text or self._store_nodes_override
        ) and delete_from_docstore:
            for node_id in node_ids:
                self._index_struct.delete(node_id)
                self._docstore.delete_document(node_id, raise_error=False)
            self._storage_context.index_store.add_index_struct(self._index_struct)

    def_delete_from_index_struct(self, ref_doc_id: str) -> None:
        # delete from index_struct only if needed
        if not self._vector_store.stores_text or self._store_nodes_override:
            ref_doc_info = self._docstore.get_ref_doc_info(ref_doc_id)
            if ref_doc_info is not None:
                for node_id in ref_doc_info.node_ids:
                    self._index_struct.delete(node_id)

    def_delete_from_docstore(self, ref_doc_id: str) -> None:
        # delete from docstore only if needed
        if not self._vector_store.stores_text or self._store_nodes_override:
            self._docstore.delete_ref_doc(ref_doc_id, raise_error=False)

    defdelete_ref_doc(
        self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
    ) -> None:
"""Delete a document and it's nodes by using ref_doc_id."""
        self._vector_store.delete(ref_doc_id, **delete_kwargs)
        self._delete_from_index_struct(ref_doc_id)
        if delete_from_docstore:
            self._delete_from_docstore(ref_doc_id)
        self._storage_context.index_store.add_index_struct(self._index_struct)

    async def_adelete_from_index_struct(self, ref_doc_id: str) -> None:
"""Delete from index_struct only if needed."""
        if not self._vector_store.stores_text or self._store_nodes_override:
            ref_doc_info = await self._docstore.aget_ref_doc_info(ref_doc_id)
            if ref_doc_info is not None:
                for node_id in ref_doc_info.node_ids:
                    self._index_struct.delete(node_id)

    async def_adelete_from_docstore(self, ref_doc_id: str) -> None:
"""Delete from docstore only if needed."""
        if not self._vector_store.stores_text or self._store_nodes_override:
            await self._docstore.adelete_ref_doc(ref_doc_id, raise_error=False)

    async defadelete_ref_doc(
        self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
    ) -> None:
"""Delete a document and it's nodes by using ref_doc_id."""
        tasks = [
            self._vector_store.adelete(ref_doc_id, **delete_kwargs),
            self._adelete_from_index_struct(ref_doc_id),
        ]
        if delete_from_docstore:
            tasks.append(self._adelete_from_docstore(ref_doc_id))

        await asyncio.gather(*tasks)

        self._storage_context.index_store.add_index_struct(self._index_struct)

    @property
    defref_doc_info(self) -> Dict[str, RefDocInfo]:
"""Retrieve a dict mapping of ingested documents and their nodes+metadata."""
        if not self._vector_store.stores_text or self._store_nodes_override:
            node_doc_ids = list(self.index_struct.nodes_dict.values())
            nodes = self.docstore.get_nodes(node_doc_ids)

            all_ref_doc_info = {}
            for node in nodes:
                ref_node = node.source_node
                if not ref_node:
                    continue

                ref_doc_info = self.docstore.get_ref_doc_info(ref_node.node_id)
                if not ref_doc_info:
                    continue

                all_ref_doc_info[ref_node.node_id] = ref_doc_info
            return all_ref_doc_info
        else:
            raise NotImplementedError(
                "Vector store integrations that store text in the vector store are "
                "not supported by ref_doc_info yet."
            )

```
 |  
| --- | --- |  
###  ref_doc_info `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.VectorStoreIndex.ref_doc_info "Permanent link")

```
ref_doc_info: [, ]

```

Retrieve a dict mapping of ingested documents and their nodes+metadata.
###  build_index_from_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.VectorStoreIndex.build_index_from_nodes "Permanent link")

```
build_index_from_nodes(
    nodes: Sequence[], **insert_kwargs: 
) -> IndexDict

```

Build the index from nodes.
Overrides BaseIndex.build_index_from_nodes.
VectorStoreIndex only stores nodes in document store if vector store does not store text
Source code in `llama-index-core/llama_index/core/indices/vector_store/base.py`  
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
309
```
 | 
```
defbuild_index_from_nodes(
    self,
    nodes: Sequence[BaseNode],
    **insert_kwargs: Any,
) -> IndexDict:
"""
    Build the index from nodes.

    NOTE: Overrides BaseIndex.build_index_from_nodes.
        VectorStoreIndex only stores nodes in document store
        if vector store does not store text
    """
    # Filter out the nodes that don't have content
    content_nodes = [
        node
        for node in nodes
        if node.get_content(metadata_mode=MetadataMode.EMBED) != ""
    ]

    # Report if some nodes are missing content
    if len(content_nodes) != len(nodes):
        print("Some nodes are missing content, skipping them...")

    return self._build_index_from_nodes(content_nodes, **insert_kwargs)

```
 |  
| --- | --- |  
###  ainsert_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.VectorStoreIndex.ainsert_nodes "Permanent link")

```
ainsert_nodes(
    nodes: Sequence[], **insert_kwargs: 
) -> None

```

Insert nodes.
overrides BaseIndex.ainsert_nodes.
VectorStoreIndex only stores nodes in document store if vector store does not store text
Source code in `llama-index-core/llama_index/core/indices/vector_store/base.py`  
| 
```
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
```
 | 
```
async defainsert_nodes(
    self, nodes: Sequence[BaseNode], **insert_kwargs: Any
) -> None:
"""
    Insert nodes.

    NOTE: overrides BaseIndex.ainsert_nodes.
        VectorStoreIndex only stores nodes in document store
        if vector store does not store text
    """
    self._validate_serializable(nodes)

    with self._callback_manager.as_trace("insert_nodes"):
        await self._async_add_nodes_to_index(
            self._index_struct, nodes, **insert_kwargs
        )
        self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  insert_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.VectorStoreIndex.insert_nodes "Permanent link")

```
insert_nodes(
    nodes: Sequence[], **insert_kwargs: 
) -> None

```

Insert nodes.
overrides BaseIndex.insert_nodes.
VectorStoreIndex only stores nodes in document store if vector store does not store text
Source code in `llama-index-core/llama_index/core/indices/vector_store/base.py`  
| 
```
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
```
 | 
```
definsert_nodes(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""
    Insert nodes.

    NOTE: overrides BaseIndex.insert_nodes.
        VectorStoreIndex only stores nodes in document store
        if vector store does not store text
    """
    self._validate_serializable(nodes)

    with self._callback_manager.as_trace("insert_nodes"):
        self._insert(nodes, **insert_kwargs)
        self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  adelete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.VectorStoreIndex.adelete_nodes "Permanent link")

```
adelete_nodes(
    node_ids: [],
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Delete a list of nodes from the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `List[str]`  |  A list of node_ids from the nodes to delete  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/vector_store/base.py`  
| 
```
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
```
 | 
```
async defadelete_nodes(
    self,
    node_ids: List[str],
    delete_from_docstore: bool = False,
    **delete_kwargs: Any,
) -> None:
"""
    Delete a list of nodes from the index.

    Args:
        node_ids (List[str]): A list of node_ids from the nodes to delete

    """
    # delete nodes from vector store
    await self._vector_store.adelete_nodes(node_ids, **delete_kwargs)

    # delete from docstore only if needed
    if (
        not self._vector_store.stores_text or self._store_nodes_override
    ) and delete_from_docstore:
        for node_id in node_ids:
            self._index_struct.delete(node_id)
            await self._docstore.adelete_document(node_id, raise_error=False)
        self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.VectorStoreIndex.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: [],
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Delete a list of nodes from the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `node_ids`  |  `List[str]`  |  A list of node_ids from the nodes to delete  |  _required_  |  
Source code in `llama-index-core/llama_index/core/indices/vector_store/base.py`  
| 
```
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
```
 | 
```
defdelete_nodes(
    self,
    node_ids: List[str],
    delete_from_docstore: bool = False,
    **delete_kwargs: Any,
) -> None:
"""
    Delete a list of nodes from the index.

    Args:
        node_ids (List[str]): A list of node_ids from the nodes to delete

    """
    # delete nodes from vector store
    self._vector_store.delete_nodes(node_ids, **delete_kwargs)

    # delete from docstore only if needed
    if (
        not self._vector_store.stores_text or self._store_nodes_override
    ) and delete_from_docstore:
        for node_id in node_ids:
            self._index_struct.delete(node_id)
            self._docstore.delete_document(node_id, raise_error=False)
        self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  delete_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.VectorStoreIndex.delete_ref_doc "Permanent link")

```
delete_ref_doc(
    ref_doc_id: ,
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Delete a document and it's nodes by using ref_doc_id.
Source code in `llama-index-core/llama_index/core/indices/vector_store/base.py`  
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
```
 | 
```
defdelete_ref_doc(
    self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
) -> None:
"""Delete a document and it's nodes by using ref_doc_id."""
    self._vector_store.delete(ref_doc_id, **delete_kwargs)
    self._delete_from_index_struct(ref_doc_id)
    if delete_from_docstore:
        self._delete_from_docstore(ref_doc_id)
    self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
###  adelete_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.VectorStoreIndex.adelete_ref_doc "Permanent link")

```
adelete_ref_doc(
    ref_doc_id: ,
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Delete a document and it's nodes by using ref_doc_id.
Source code in `llama-index-core/llama_index/core/indices/vector_store/base.py`  
| 
```
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
```
 | 
```
async defadelete_ref_doc(
    self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
) -> None:
"""Delete a document and it's nodes by using ref_doc_id."""
    tasks = [
        self._vector_store.adelete(ref_doc_id, **delete_kwargs),
        self._adelete_from_index_struct(ref_doc_id),
    ]
    if delete_from_docstore:
        tasks.append(self._adelete_from_docstore(ref_doc_id))

    await asyncio.gather(*tasks)

    self._storage_context.index_store.add_index_struct(self._index_struct)

```
 |  
| --- | --- |  
##  SQLDocumentContextBuilder [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SQLDocumentContextBuilder "Permanent link")
Builder that builds context for a given set of SQL tables.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `sql_database`  |  `Optional[SQLDatabase[](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SQLDatabase "SQLDatabase \(llama_index.core.utilities.sql_wrapper.SQLDatabase\)")]`  |  SQL database to use,  |  _required_  |  
|  `text_splitter`  |  `Optional[TextSplitter[](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/#llama_index.core.node_parser.interface.TextSplitter "TextSplitter \(llama_index.core.node_parser.interface.TextSplitter\)")]`  |  Text Splitter to use.  |  `None`  |  
|  `table_context_prompt`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A Table Context Prompt (see :ref:`Prompt-Templates`).  |  `None`  |  
|  `refine_table_context_prompt`  |  `Optional[BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")]`  |  A Refine Table Context Prompt (see :ref:`Prompt-Templates`).  |  `None`  |  
|  `table_context_task`  |  `Optional[str]`  |  The query to perform on the table context. A default query string is used if none is provided by the user.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/indices/common/struct_store/base.py`  
| 
```
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
```
 | 
```
classSQLDocumentContextBuilder:
"""
    Builder that builds context for a given set of SQL tables.

    Args:
        sql_database (Optional[SQLDatabase]): SQL database to use,
        text_splitter (Optional[TextSplitter]): Text Splitter to use.
        table_context_prompt (Optional[BasePromptTemplate]): A
            Table Context Prompt (see :ref:`Prompt-Templates`).
        refine_table_context_prompt (Optional[BasePromptTemplate]):
            A Refine Table Context Prompt (see :ref:`Prompt-Templates`).
        table_context_task (Optional[str]): The query to perform
            on the table context. A default query string is used
            if none is provided by the user.

    """

    def__init__(
        self,
        sql_database: SQLDatabase,
        llm: Optional[LLM] = None,
        text_splitter: Optional[TextSplitter] = None,
        table_context_prompt: Optional[BasePromptTemplate] = None,
        refine_table_context_prompt: Optional[BasePromptTemplate] = None,
        table_context_task: Optional[str] = None,
    ) -> None:
"""Initialize params."""
        # TODO: take in an entire index instead of forming a response builder
        if sql_database is None:
            raise ValueError("sql_database must be provided.")
        self._sql_database = sql_database
        self._text_splitter = text_splitter
        self._llm = llm or Settings.llm
        self._prompt_helper = Settings._prompt_helper or PromptHelper.from_llm_metadata(
            self._llm.metadata,
        )
        self._callback_manager = Settings.callback_manager
        self._table_context_prompt = (
            table_context_prompt or DEFAULT_TABLE_CONTEXT_PROMPT
        )
        self._refine_table_context_prompt = (
            refine_table_context_prompt or DEFAULT_REFINE_TABLE_CONTEXT_PROMPT_SEL
        )
        self._table_context_task = table_context_task or DEFAULT_TABLE_CONTEXT_QUERY

    defbuild_all_context_from_documents(
        self,
        documents_dict: Dict[str, List[BaseNode]],
    ) -> Dict[str, str]:
"""Build context for all tables in the database."""
        context_dict = {}
        for table_name in self._sql_database.get_usable_table_names():
            context_dict[table_name] = self.build_table_context_from_documents(
                documents_dict[table_name], table_name
            )
        return context_dict

    defbuild_table_context_from_documents(
        self,
        documents: Sequence[BaseNode],
        table_name: str,
    ) -> str:
"""Build context from documents for a single table."""
        schema = self._sql_database.get_single_table_info(table_name)
        prompt_with_schema = self._table_context_prompt.partial_format(schema=schema)
        prompt_with_schema.metadata["prompt_type"] = PromptType.QUESTION_ANSWER
        refine_prompt_with_schema = self._refine_table_context_prompt.partial_format(
            schema=schema
        )
        refine_prompt_with_schema.metadata["prompt_type"] = PromptType.REFINE

        text_splitter = (
            self._text_splitter
            or self._prompt_helper.get_text_splitter_given_prompt(
                prompt_with_schema, llm=self._llm
            )
        )
        # we use the ResponseBuilder to iteratively go through all texts
        response_builder = get_response_synthesizer(
            llm=self._llm,
            text_qa_template=prompt_with_schema,
            refine_template=refine_prompt_with_schema,
        )
        with self._callback_manager.event(
            CBEventType.CHUNKING,
            payload={EventPayload.DOCUMENTS: documents},
        ) as event:
            text_chunks = []
            for doc in documents:
                chunks = text_splitter.split_text(
                    doc.get_content(metadata_mode=MetadataMode.LLM)
                )
                text_chunks.extend(chunks)

            event.on_end(
                payload={EventPayload.CHUNKS: text_chunks},
            )

        # feed in the "query_str" or the task
        table_context = response_builder.get_response(
            text_chunks=text_chunks, query_str=self._table_context_task
        )
        return cast(str, table_context)

```
 |  
| --- | --- |  
###  build_all_context_from_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SQLDocumentContextBuilder.build_all_context_from_documents "Permanent link")

```
build_all_context_from_documents(
    documents_dict: [, []]
) -> [, ]

```

Build context for all tables in the database.
Source code in `llama-index-core/llama_index/core/indices/common/struct_store/base.py`  
| 
```
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
```
 | 
```
defbuild_all_context_from_documents(
    self,
    documents_dict: Dict[str, List[BaseNode]],
) -> Dict[str, str]:
"""Build context for all tables in the database."""
    context_dict = {}
    for table_name in self._sql_database.get_usable_table_names():
        context_dict[table_name] = self.build_table_context_from_documents(
            documents_dict[table_name], table_name
        )
    return context_dict

```
 |  
| --- | --- |  
###  build_table_context_from_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SQLDocumentContextBuilder.build_table_context_from_documents "Permanent link")

```
build_table_context_from_documents(
    documents: Sequence[], table_name: 
) -> 

```

Build context from documents for a single table.
Source code in `llama-index-core/llama_index/core/indices/common/struct_store/base.py`  
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
```
 | 
```
defbuild_table_context_from_documents(
    self,
    documents: Sequence[BaseNode],
    table_name: str,
) -> str:
"""Build context from documents for a single table."""
    schema = self._sql_database.get_single_table_info(table_name)
    prompt_with_schema = self._table_context_prompt.partial_format(schema=schema)
    prompt_with_schema.metadata["prompt_type"] = PromptType.QUESTION_ANSWER
    refine_prompt_with_schema = self._refine_table_context_prompt.partial_format(
        schema=schema
    )
    refine_prompt_with_schema.metadata["prompt_type"] = PromptType.REFINE

    text_splitter = (
        self._text_splitter
        or self._prompt_helper.get_text_splitter_given_prompt(
            prompt_with_schema, llm=self._llm
        )
    )
    # we use the ResponseBuilder to iteratively go through all texts
    response_builder = get_response_synthesizer(
        llm=self._llm,
        text_qa_template=prompt_with_schema,
        refine_template=refine_prompt_with_schema,
    )
    with self._callback_manager.event(
        CBEventType.CHUNKING,
        payload={EventPayload.DOCUMENTS: documents},
    ) as event:
        text_chunks = []
        for doc in documents:
            chunks = text_splitter.split_text(
                doc.get_content(metadata_mode=MetadataMode.LLM)
            )
            text_chunks.extend(chunks)

        event.on_end(
            payload={EventPayload.CHUNKS: text_chunks},
        )

    # feed in the "query_str" or the task
    table_context = response_builder.get_response(
        text_chunks=text_chunks, query_str=self._table_context_task
    )
    return cast(str, table_context)

```
 |  
| --- | --- |  
##  PromptHelper [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.PromptHelper "Permanent link")
Bases: 
Prompt helper.
General prompt helper that can help deal with LLM context window token limitations.
At its core, it calculates available context size by starting with the context window size of an LLM and reserve token space for the prompt template, and the output.
It provides utility for "repacking" text chunks (retrieved from index) to maximally make use of the available context window (and thereby reducing the number of LLM calls needed), or truncating them so that they fit in a single LLM call.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `context_window`  |  Context window for the LLM.  |  `DEFAULT_CONTEXT_WINDOW`  |  
|  `num_output`  |  Number of outputs for the LLM.  |  `DEFAULT_NUM_OUTPUTS`  |  
|  `chunk_overlap_ratio`  |  `float`  |  Chunk overlap as a ratio of chunk size  |  `DEFAULT_CHUNK_OVERLAP_RATIO`  |  
|  `chunk_size_limit`  |  `int | None`  |  Maximum chunk size to use.  |  `None`  |  
|  `tokenizer`  |  `Optional[Callable[[str], List]]`  |  Tokenizer to use.  |  `None`  |  
|  `separator`  |  Separator for text splitter  |  `' '`  |  
Source code in `llama-index-core/llama_index/core/indices/prompt_helper.py`  
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
```
 | 
```
classPromptHelper(BaseComponent):
"""
    Prompt helper.

    General prompt helper that can help deal with LLM context window token limitations.

    At its core, it calculates available context size by starting with the context
    window size of an LLM and reserve token space for the prompt template, and the
    output.

    It provides utility for "repacking" text chunks (retrieved from index) to maximally
    make use of the available context window (and thereby reducing the number of LLM
    calls needed), or truncating them so that they fit in a single LLM call.

    Args:
        context_window (int):                   Context window for the LLM.
        num_output (int):                       Number of outputs for the LLM.
        chunk_overlap_ratio (float):            Chunk overlap as a ratio of chunk size
        chunk_size_limit (Optional[int]):         Maximum chunk size to use.
        tokenizer (Optional[Callable[[str], List]]): Tokenizer to use.
        separator (str):                        Separator for text splitter

    """

    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description="The maximum context size that will get sent to the LLM.",
    )
    num_output: int = Field(
        default=DEFAULT_NUM_OUTPUTS,
        description="The amount of token-space to leave in input for generation.",
    )
    chunk_overlap_ratio: float = Field(
        default=DEFAULT_CHUNK_OVERLAP_RATIO,
        description="The percentage token amount that each chunk should overlap.",
        ge=0.0,
        le=1.0,
    )
    chunk_size_limit: Optional[int] = Field(description="The maximum size of a chunk.")
    separator: str = Field(
        default=" ", description="The separator when chunking tokens."
    )

    _token_counter: TokenCounter = PrivateAttr()

    def__init__(
        self,
        context_window: int = DEFAULT_CONTEXT_WINDOW,
        num_output: int = DEFAULT_NUM_OUTPUTS,
        chunk_overlap_ratio: float = DEFAULT_CHUNK_OVERLAP_RATIO,
        chunk_size_limit: Optional[int] = None,
        tokenizer: Optional[Callable[[str], List]] = None,
        separator: str = " ",
    ) -> None:
"""Init params."""
        super().__init__(
            context_window=context_window,
            num_output=num_output,
            chunk_overlap_ratio=chunk_overlap_ratio,
            chunk_size_limit=chunk_size_limit,
            separator=separator,
        )

        # TODO: make configurable
        self._token_counter = TokenCounter(tokenizer=tokenizer)

    @classmethod
    deffrom_llm_metadata(
        cls,
        llm_metadata: LLMMetadata,
        chunk_overlap_ratio: float = DEFAULT_CHUNK_OVERLAP_RATIO,
        chunk_size_limit: Optional[int] = None,
        tokenizer: Optional[Callable[[str], List]] = None,
        separator: str = " ",
    ) -> "PromptHelper":
"""
        Create from llm predictor.

        This will autofill values like context_window and num_output.

        """
        context_window = llm_metadata.context_window

        if llm_metadata.num_output == -1:
            num_output = DEFAULT_NUM_OUTPUTS
        else:
            num_output = llm_metadata.num_output

        return cls(
            context_window=context_window,
            num_output=num_output,
            chunk_overlap_ratio=chunk_overlap_ratio,
            chunk_size_limit=chunk_size_limit,
            tokenizer=tokenizer,
            separator=separator,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "PromptHelper"

    def_get_available_context_size(self, num_prompt_tokens: int) -> int:
"""
        Get available context size.

        This is calculated as:
            available context window = total context window
                - input (partially filled prompt)
                - output (room reserved for response)

        Notes:
        - Available context size is further clamped to be non-negative.

        """
        context_size_tokens = self.context_window - num_prompt_tokens - self.num_output
        if context_size_tokens  0:
            raise ValueError(
                f"Calculated available context size {context_size_tokens} was"
                " not non-negative."
            )
        return context_size_tokens

    def_get_tools_from_llm(
        self, llm: Optional[LLM] = None, tools: Optional[List["BaseTool"]] = None
    ) -> List["BaseTool"]:
        fromllama_index.core.program.function_programimport get_function_tool

        tools = tools or []
        if isinstance(llm, StructuredLLM):
            tools.append(get_function_tool(llm.output_cls))

        return tools

    def_get_available_chunk_size(
        self,
        prompt: BasePromptTemplate,
        num_chunks: int = 1,
        padding: int = 5,
        llm: Optional[LLM] = None,
        tools: Optional[List["BaseTool"]] = None,
    ) -> int:
"""
        Get available chunk size.

        This is calculated as:
            available chunk size = available context window  // number_chunks
                - padding

        Notes:
        - By default, we use padding of 5 (to save space for formatting needs).
        - Available chunk size is further clamped to chunk_size_limit if specified.

        """
        tools = self._get_tools_from_llm(llm=llm, tools=tools)

        if isinstance(prompt, SelectorPromptTemplate):
            prompt = prompt.select(llm=llm)

        if isinstance(prompt, ChatPromptTemplate):
            messages: List[ChatMessage] = prompt.message_templates

            # account for partial formatting
            partial_messages = []
            for message in messages:
                partial_message = deepcopy(message)

                # TODO: This does not count tokens in non-text blocks
                prompt_kwargs = prompt.kwargs or {}
                partial_message.blocks = format_content_blocks(
                    partial_message.blocks, **prompt_kwargs
                )

                # add to list of partial messages
                partial_messages.append(partial_message)

            num_prompt_tokens = self._token_counter.estimate_tokens_in_messages(
                partial_messages
            )
        else:
            prompt_str = get_empty_prompt_txt(prompt)
            num_prompt_tokens = self._token_counter.get_string_tokens(prompt_str)

        num_prompt_tokens += self._token_counter.estimate_tokens_in_tools(
            [x.metadata.to_openai_tool() for x in tools]
        )

        # structured llms cannot have system prompts currently -- check the underlying llm
        if isinstance(llm, StructuredLLM):
            num_prompt_tokens += self._token_counter.get_string_tokens(
                llm.llm.system_prompt or ""
            )
        elif llm is not None:
            num_prompt_tokens += self._token_counter.get_string_tokens(
                llm.system_prompt or ""
            )

        available_context_size = self._get_available_context_size(num_prompt_tokens)
        result = available_context_size // num_chunks - padding
        if self.chunk_size_limit is not None:
            result = min(result, self.chunk_size_limit)
        return result

    defget_text_splitter_given_prompt(
        self,
        prompt: BasePromptTemplate,
        num_chunks: int = 1,
        padding: int = DEFAULT_PADDING,
        llm: Optional[LLM] = None,
        tools: Optional[List["BaseTool"]] = None,
    ) -> TokenTextSplitter:
"""
        Get text splitter configured to maximally pack available context window,
        taking into account of given prompt, and desired number of chunks.
        """
        chunk_size = self._get_available_chunk_size(
            prompt, num_chunks, padding=padding, llm=llm, tools=tools
        )
        if chunk_size <= 0:
            raise ValueError(f"Chunk size {chunk_size} is not positive.")
        chunk_overlap = int(self.chunk_overlap_ratio * chunk_size)
        return TokenTextSplitter(
            separator=self.separator,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            tokenizer=self._token_counter.tokenizer,
        )

    deftruncate(
        self,
        prompt: BasePromptTemplate,
        text_chunks: Sequence[str],
        padding: int = DEFAULT_PADDING,
        llm: Optional[LLM] = None,
        tools: Optional[List["BaseTool"]] = None,
    ) -> List[str]:
"""Truncate text chunks to fit available context window."""
        text_splitter = self.get_text_splitter_given_prompt(
            prompt,
            num_chunks=len(text_chunks),
            padding=padding,
            llm=llm,
            tools=tools,
        )
        return [truncate_text(chunk, text_splitter) for chunk in text_chunks]

    defrepack(
        self,
        prompt: BasePromptTemplate,
        text_chunks: Sequence[str],
        padding: int = DEFAULT_PADDING,
        llm: Optional[LLM] = None,
        tools: Optional[List["BaseTool"]] = None,
    ) -> List[str]:
"""
        Repack text chunks to fit available context window.

        This will combine text chunks into consolidated chunks
        that more fully "pack" the prompt template given the context_window.

        """
        text_splitter = self.get_text_splitter_given_prompt(
            prompt, padding=padding, llm=llm, tools=tools
        )
        combined_str = "\n\n".join([c.strip() for c in text_chunks if c.strip()])
        return text_splitter.split_text(combined_str)

```
 |  
| --- | --- |  
###  from_llm_metadata `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.PromptHelper.from_llm_metadata "Permanent link")

```
from_llm_metadata(
    llm_metadata: ,
    chunk_overlap_ratio: float = DEFAULT_CHUNK_OVERLAP_RATIO,
    chunk_size_limit: Optional[] = None,
    tokenizer: Optional[Callable[[], ]] = None,
    separator:  = " ",
) -> 

```

Create from llm predictor.
This will autofill values like context_window and num_output.
Source code in `llama-index-core/llama_index/core/indices/prompt_helper.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_llm_metadata(
    cls,
    llm_metadata: LLMMetadata,
    chunk_overlap_ratio: float = DEFAULT_CHUNK_OVERLAP_RATIO,
    chunk_size_limit: Optional[int] = None,
    tokenizer: Optional[Callable[[str], List]] = None,
    separator: str = " ",
) -> "PromptHelper":
"""
    Create from llm predictor.

    This will autofill values like context_window and num_output.

    """
    context_window = llm_metadata.context_window

    if llm_metadata.num_output == -1:
        num_output = DEFAULT_NUM_OUTPUTS
    else:
        num_output = llm_metadata.num_output

    return cls(
        context_window=context_window,
        num_output=num_output,
        chunk_overlap_ratio=chunk_overlap_ratio,
        chunk_size_limit=chunk_size_limit,
        tokenizer=tokenizer,
        separator=separator,
    )

```
 |  
| --- | --- |  
###  get_text_splitter_given_prompt [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.PromptHelper.get_text_splitter_given_prompt "Permanent link")

```
get_text_splitter_given_prompt(
    prompt: ,
    num_chunks:  = 1,
    padding:  = DEFAULT_PADDING,
    llm: Optional[] = None,
    tools: Optional[[]] = None,
) -> 

```

Get text splitter configured to maximally pack available context window, taking into account of given prompt, and desired number of chunks.
Source code in `llama-index-core/llama_index/core/indices/prompt_helper.py`  
| 
```
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
```
 | 
```
defget_text_splitter_given_prompt(
    self,
    prompt: BasePromptTemplate,
    num_chunks: int = 1,
    padding: int = DEFAULT_PADDING,
    llm: Optional[LLM] = None,
    tools: Optional[List["BaseTool"]] = None,
) -> TokenTextSplitter:
"""
    Get text splitter configured to maximally pack available context window,
    taking into account of given prompt, and desired number of chunks.
    """
    chunk_size = self._get_available_chunk_size(
        prompt, num_chunks, padding=padding, llm=llm, tools=tools
    )
    if chunk_size <= 0:
        raise ValueError(f"Chunk size {chunk_size} is not positive.")
    chunk_overlap = int(self.chunk_overlap_ratio * chunk_size)
    return TokenTextSplitter(
        separator=self.separator,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        tokenizer=self._token_counter.tokenizer,
    )

```
 |  
| --- | --- |  
###  truncate [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.PromptHelper.truncate "Permanent link")

```
truncate(
    prompt: ,
    text_chunks: Sequence[],
    padding:  = DEFAULT_PADDING,
    llm: Optional[] = None,
    tools: Optional[[]] = None,
) -> []

```

Truncate text chunks to fit available context window.
Source code in `llama-index-core/llama_index/core/indices/prompt_helper.py`  
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
```
 | 
```
deftruncate(
    self,
    prompt: BasePromptTemplate,
    text_chunks: Sequence[str],
    padding: int = DEFAULT_PADDING,
    llm: Optional[LLM] = None,
    tools: Optional[List["BaseTool"]] = None,
) -> List[str]:
"""Truncate text chunks to fit available context window."""
    text_splitter = self.get_text_splitter_given_prompt(
        prompt,
        num_chunks=len(text_chunks),
        padding=padding,
        llm=llm,
        tools=tools,
    )
    return [truncate_text(chunk, text_splitter) for chunk in text_chunks]

```
 |  
| --- | --- |  
###  repack [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.PromptHelper.repack "Permanent link")

```
repack(
    prompt: ,
    text_chunks: Sequence[],
    padding:  = DEFAULT_PADDING,
    llm: Optional[] = None,
    tools: Optional[[]] = None,
) -> []

```

Repack text chunks to fit available context window.
This will combine text chunks into consolidated chunks that more fully "pack" the prompt template given the context_window.
Source code in `llama-index-core/llama_index/core/indices/prompt_helper.py`  
| 
```
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
defrepack(
    self,
    prompt: BasePromptTemplate,
    text_chunks: Sequence[str],
    padding: int = DEFAULT_PADDING,
    llm: Optional[LLM] = None,
    tools: Optional[List["BaseTool"]] = None,
) -> List[str]:
"""
    Repack text chunks to fit available context window.

    This will combine text chunks into consolidated chunks
    that more fully "pack" the prompt template given the context_window.

    """
    text_splitter = self.get_text_splitter_given_prompt(
        prompt, padding=padding, llm=llm, tools=tools
    )
    combined_str = "\n\n".join([c.strip() for c in text_chunks if c.strip()])
    return text_splitter.split_text(combined_str)

```
 |  
| --- | --- |  
##  BasePromptTemplate [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.BasePromptTemplate "Permanent link")
Bases: `BaseModel`, 
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `metadata`  |  `Dict[str, Any]`  |  _required_  |  
|  `template_vars`  |  `List[str]`  |  _required_  |  
|  `kwargs`  |  `Dict[str, str]`  |  _required_  |  
|  `output_parser`  |  `BaseOutputParser[](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/#llama_index.core.types.BaseOutputParser "BaseOutputParser \(llama_index.core.types.BaseOutputParser\)") | None`  |  _required_  |  
|  `template_var_mappings`  |  `Dict[str, Any] | None`  |  Template variable mappings (Optional).  |  `<class 'dict'>`  |  
|  `function_mappings`  |  `Dict[str, Annotated[Callable, WithJsonSchema, WithJsonSchema, PlainSerializer]] | None`  |  Function mappings (Optional). This is a mapping from template variable names to functions that take in the current kwargs and return a string.  |  `<class 'dict'>`  |  
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
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
```
 | 
```
classBasePromptTemplate(BaseModel, ABC):  # type: ignore[no-redef]
    model_config = ConfigDict(arbitrary_types_allowed=True)
    metadata: Dict[str, Any]
    template_vars: List[str]
    kwargs: Dict[str, str]
    output_parser: Optional[BaseOutputParser]
    template_var_mappings: Optional[Dict[str, Any]] = Field(
        default_factory=dict,  # type: ignore
        description="Template variable mappings (Optional).",
    )
    function_mappings: Optional[Dict[str, AnnotatedCallable]] = Field(
        default_factory=dict,  # type: ignore
        description=(
            "Function mappings (Optional). This is a mapping from template "
            "variable names to functions that take in the current kwargs and "
            "return a string."
        ),
    )

    def_map_template_vars(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
"""For keys in template_var_mappings, swap in the right keys."""
        template_var_mappings = self.template_var_mappings or {}
        return {template_var_mappings.get(k, k): v for k, v in kwargs.items()}

    def_map_function_vars(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
"""
        For keys in function_mappings, compute values and combine w/ kwargs.

        Users can pass in functions instead of fixed values as format variables.
        For each function, we call the function with the current kwargs,
        get back the value, and then use that value in the template
        for the corresponding format variable.

        """
        function_mappings = self.function_mappings or {}
        # first generate the values for the functions
        new_kwargs = {}
        for k, v in function_mappings.items():
            # TODO: figure out what variables to pass into each function
            # is it the kwargs specified during query time? just the fixed kwargs?
            # all kwargs?
            new_kwargs[k] = v(**kwargs)

        # then, add the fixed variables only if not in new_kwargs already
        # (implying that function mapping will override fixed variables)
        for k, v in kwargs.items():
            if k not in new_kwargs:
                new_kwargs[k] = v

        return new_kwargs

    def_map_all_vars(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
"""
        Map both template and function variables.

        We (1) first call function mappings to compute functions,
        and then (2) call the template_var_mappings.

        """
        # map function
        new_kwargs = self._map_function_vars(kwargs)
        # map template vars (to point to existing format vars in string template)
        return self._map_template_vars(new_kwargs)

    @abstractmethod
    defpartial_format(self, **kwargs: Any) -> "BasePromptTemplate": ...

    @abstractmethod
    defformat(self, llm: Optional[BaseLLM] = None, **kwargs: Any) -> str: ...

    @abstractmethod
    defformat_messages(
        self, llm: Optional[BaseLLM] = None, **kwargs: Any
    ) -> List[ChatMessage]: ...

    @abstractmethod
    defget_template(self, llm: Optional[BaseLLM] = None) -> str: ...

```
 |  
| --- | --- |  
##  ChatPromptTemplate [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.ChatPromptTemplate "Permanent link")
Bases: 
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `message_templates`  |  `List[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  _required_  |  
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
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
```
 | 
```
classChatPromptTemplate(BasePromptTemplate):  # type: ignore[no-redef]
    message_templates: List[ChatMessage]

    def__init__(
        self,
        message_templates: Sequence[ChatMessage],
        prompt_type: str = PromptType.CUSTOM,
        output_parser: Optional[BaseOutputParser] = None,
        metadata: Optional[Dict[str, Any]] = None,
        template_var_mappings: Optional[Dict[str, Any]] = None,
        function_mappings: Optional[Dict[str, Callable]] = None,
        **kwargs: Any,
    ):
        if metadata is None:
            metadata = {}
        metadata["prompt_type"] = prompt_type

        template_vars = []
        for message_template in message_templates:
            template_vars.extend(message_template.get_template_vars())

        super().__init__(
            message_templates=message_templates,
            kwargs=kwargs,
            metadata=metadata,
            output_parser=output_parser,
            template_vars=template_vars,
            template_var_mappings=template_var_mappings,
            function_mappings=function_mappings,
        )

    @classmethod
    deffrom_messages(
        cls,
        message_templates: Union[List[Tuple[str, str]], List[ChatMessage]],
        **kwargs: Any,
    ) -> "ChatPromptTemplate":
"""From messages."""
        if isinstance(message_templates[0], tuple):
            message_templates = [
                ChatMessage.from_str(role=role, content=content)  # type: ignore[arg-type]
                for role, content in message_templates
            ]
        return cls(message_templates=message_templates, **kwargs)  # type: ignore[arg-type]

    defpartial_format(self, **kwargs: Any) -> "ChatPromptTemplate":
        prompt = deepcopy(self)
        prompt.kwargs.update(kwargs)
        return prompt

    defformat(
        self,
        llm: Optional[BaseLLM] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        **kwargs: Any,
    ) -> str:
        del llm  # unused
        messages = self.format_messages(**kwargs)

        if messages_to_prompt is not None:
            return messages_to_prompt(messages)

        return default_messages_to_prompt(messages)

    defformat_messages(
        self, llm: Optional[BaseLLM] = None, **kwargs: Any
    ) -> List[ChatMessage]:
        del llm  # unused
"""Format the prompt into a list of chat messages."""
        all_kwargs = {
            **self.kwargs,
            **kwargs,
        }
        mapped_all_kwargs = self._map_all_vars(all_kwargs)

        messages: List[ChatMessage] = []
        for message_template in self.message_templates:
            # Handle messages with multiple blocks
            if message_template.blocks:
                template_vars = message_template.get_template_vars()
                relevant_kwargs = {
                    k: v for k, v in mapped_all_kwargs.items() if k in template_vars
                }
                formatted_message = message_template.format_vars(**relevant_kwargs)
                messages.append(formatted_message)
            else:
                # Handle empty messages (if any)
                messages.append(message_template.model_copy())

        if self.output_parser is not None:
            messages = self.output_parser.format_messages(messages)

        return messages

    defget_template(self, llm: Optional[BaseLLM] = None) -> str:
        return default_messages_to_prompt(self.message_templates)

```
 |  
| --- | --- |  
###  from_messages `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.ChatPromptTemplate.from_messages "Permanent link")

```
from_messages(
    message_templates: Union[
        [Tuple[, ]], []
    ],
    **kwargs: 
) -> 

```

From messages.
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_messages(
    cls,
    message_templates: Union[List[Tuple[str, str]], List[ChatMessage]],
    **kwargs: Any,
) -> "ChatPromptTemplate":
"""From messages."""
    if isinstance(message_templates[0], tuple):
        message_templates = [
            ChatMessage.from_str(role=role, content=content)  # type: ignore[arg-type]
            for role, content in message_templates
        ]
    return cls(message_templates=message_templates, **kwargs)  # type: ignore[arg-type]

```
 |  
| --- | --- |  
##  PromptTemplate [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.PromptTemplate "Permanent link")
Bases: 
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `template`  |  _required_  |  
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
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
```
 | 
```
classPromptTemplate(BasePromptTemplate):  # type: ignore[no-redef]
    template: str

    def__init__(
        self,
        template: str,
        prompt_type: str = PromptType.CUSTOM,
        output_parser: Optional[BaseOutputParser] = None,
        metadata: Optional[Dict[str, Any]] = None,
        template_var_mappings: Optional[Dict[str, Any]] = None,
        function_mappings: Optional[Dict[str, Callable]] = None,
        **kwargs: Any,
    ) -> None:
        if metadata is None:
            metadata = {}
        metadata["prompt_type"] = prompt_type

        template_vars = get_template_vars(template)

        super().__init__(
            template=template,
            template_vars=template_vars,
            kwargs=kwargs,
            metadata=metadata,
            output_parser=output_parser,
            template_var_mappings=template_var_mappings,
            function_mappings=function_mappings,
        )

    defpartial_format(self, **kwargs: Any) -> "PromptTemplate":
"""Partially format the prompt."""
        # NOTE: this is a hack to get around deepcopy failing on output parser
        output_parser = self.output_parser
        self.output_parser = None

        # get function and fixed kwargs, and add that to a copy
        # of the current prompt object
        prompt = deepcopy(self)
        prompt.kwargs.update(kwargs)

        # NOTE: put the output parser back
        prompt.output_parser = output_parser
        self.output_parser = output_parser
        return prompt

    defformat(
        self,
        llm: Optional[BaseLLM] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        **kwargs: Any,
    ) -> str:
"""Format the prompt into a string."""
        del llm  # unused
        all_kwargs = {
            **self.kwargs,
            **kwargs,
        }

        mapped_all_kwargs = self._map_all_vars(all_kwargs)
        prompt = format_string(self.template, **mapped_all_kwargs)

        if self.output_parser is not None:
            prompt = self.output_parser.format(prompt)

        if completion_to_prompt is not None:
            prompt = completion_to_prompt(prompt)

        return prompt

    defformat_messages(
        self, llm: Optional[BaseLLM] = None, **kwargs: Any
    ) -> List[ChatMessage]:
"""Format the prompt into a list of chat messages."""
        del llm  # unused
        prompt = self.format(**kwargs)
        return prompt_to_messages(prompt)

    defget_template(self, llm: Optional[BaseLLM] = None) -> str:
        return self.template

```
 |  
| --- | --- |  
###  partial_format [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.PromptTemplate.partial_format "Permanent link")

```
partial_format(**kwargs: ) -> 

```

Partially format the prompt.
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
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
```
 | 
```
defpartial_format(self, **kwargs: Any) -> "PromptTemplate":
"""Partially format the prompt."""
    # NOTE: this is a hack to get around deepcopy failing on output parser
    output_parser = self.output_parser
    self.output_parser = None

    # get function and fixed kwargs, and add that to a copy
    # of the current prompt object
    prompt = deepcopy(self)
    prompt.kwargs.update(kwargs)

    # NOTE: put the output parser back
    prompt.output_parser = output_parser
    self.output_parser = output_parser
    return prompt

```
 |  
| --- | --- |  
###  format [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.PromptTemplate.format "Permanent link")

```
format(
    llm: Optional[BaseLLM] = None,
    completion_to_prompt: Optional[
        Callable[[], ]
    ] = None,
    **kwargs: 
) -> 

```

Format the prompt into a string.
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
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
```
 | 
```
defformat(
    self,
    llm: Optional[BaseLLM] = None,
    completion_to_prompt: Optional[Callable[[str], str]] = None,
    **kwargs: Any,
) -> str:
"""Format the prompt into a string."""
    del llm  # unused
    all_kwargs = {
        **self.kwargs,
        **kwargs,
    }

    mapped_all_kwargs = self._map_all_vars(all_kwargs)
    prompt = format_string(self.template, **mapped_all_kwargs)

    if self.output_parser is not None:
        prompt = self.output_parser.format(prompt)

    if completion_to_prompt is not None:
        prompt = completion_to_prompt(prompt)

    return prompt

```
 |  
| --- | --- |  
###  format_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.PromptTemplate.format_messages "Permanent link")

```
format_messages(
    llm: Optional[BaseLLM] = None, **kwargs: 
) -> []

```

Format the prompt into a list of chat messages.
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
204
205
206
207
208
209
210
```
 | 
```
defformat_messages(
    self, llm: Optional[BaseLLM] = None, **kwargs: Any
) -> List[ChatMessage]:
"""Format the prompt into a list of chat messages."""
    del llm  # unused
    prompt = self.format(**kwargs)
    return prompt_to_messages(prompt)

```
 |  
| --- | --- |  
##  SelectorPromptTemplate [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SelectorPromptTemplate "Permanent link")
Bases: 
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `default_template`  |   |  _required_  |  
|  `conditionals`  |  `Sequence[Tuple[Callable[list, bool], BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.base.BasePromptTemplate\)")]] | None`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
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
```
 | 
```
classSelectorPromptTemplate(BasePromptTemplate):  # type: ignore[no-redef]
    default_template: SerializeAsAny[BasePromptTemplate]
    conditionals: Optional[
        Sequence[Tuple[Callable[[BaseLLM], bool], BasePromptTemplate]]
    ] = None

    def__init__(
        self,
        default_template: BasePromptTemplate,
        conditionals: Optional[
            Sequence[Tuple[Callable[[BaseLLM], bool], BasePromptTemplate]]
        ] = None,
    ):
        metadata = default_template.metadata
        kwargs = default_template.kwargs
        template_vars = default_template.template_vars
        output_parser = default_template.output_parser
        super().__init__(
            default_template=default_template,
            conditionals=conditionals,
            metadata=metadata,
            kwargs=kwargs,
            template_vars=template_vars,
            output_parser=output_parser,
        )

    defselect(self, llm: Optional[BaseLLM] = None) -> BasePromptTemplate:
        # ensure output parser is up to date
        self.default_template.output_parser = self.output_parser

        if llm is None:
            return self.default_template

        if self.conditionals is not None:
            for condition, prompt in self.conditionals:
                if condition(llm):
                    # ensure output parser is up to date
                    prompt.output_parser = self.output_parser
                    return prompt

        return self.default_template

    defpartial_format(self, **kwargs: Any) -> "SelectorPromptTemplate":
        default_template = self.default_template.partial_format(**kwargs)
        if self.conditionals is None:
            conditionals = None
        else:
            conditionals = [
                (condition, prompt.partial_format(**kwargs))
                for condition, prompt in self.conditionals
            ]
        return SelectorPromptTemplate(
            default_template=default_template, conditionals=conditionals
        )

    defformat(self, llm: Optional[BaseLLM] = None, **kwargs: Any) -> str:
"""Format the prompt into a string."""
        prompt = self.select(llm=llm)
        return prompt.format(**kwargs)

    defformat_messages(
        self, llm: Optional[BaseLLM] = None, **kwargs: Any
    ) -> List[ChatMessage]:
"""Format the prompt into a list of chat messages."""
        prompt = self.select(llm=llm)
        return prompt.format_messages(**kwargs)

    defget_template(self, llm: Optional[BaseLLM] = None) -> str:
        prompt = self.select(llm=llm)
        return prompt.get_template(llm=llm)

```
 |  
| --- | --- |  
###  format [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SelectorPromptTemplate.format "Permanent link")

```
format(llm: Optional[BaseLLM] = None, **kwargs: ) -> 

```

Format the prompt into a string.
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
369
370
371
372
```
 | 
```
defformat(self, llm: Optional[BaseLLM] = None, **kwargs: Any) -> str:
"""Format the prompt into a string."""
    prompt = self.select(llm=llm)
    return prompt.format(**kwargs)

```
 |  
| --- | --- |  
###  format_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SelectorPromptTemplate.format_messages "Permanent link")

```
format_messages(
    llm: Optional[BaseLLM] = None, **kwargs: 
) -> []

```

Format the prompt into a list of chat messages.
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
374
375
376
377
378
379
```
 | 
```
defformat_messages(
    self, llm: Optional[BaseLLM] = None, **kwargs: Any
) -> List[ChatMessage]:
"""Format the prompt into a list of chat messages."""
    prompt = self.select(llm=llm)
    return prompt.format_messages(**kwargs)

```
 |  
| --- | --- |  
##  SimpleDirectoryReader [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SimpleDirectoryReader "Permanent link")
Bases: , , 
Simple directory reader.
Load files from file directory. Automatically select the best file reader given file extensions.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `input_dir`  |  `Union[Path, str]`  |  Path to the directory.  |  `None`  |  
|  `input_files`  |  `List`  |  List of file paths to read (Optional; overrides input_dir, exclude)  |  `None`  |  
|  `exclude`  |  `List`  |  glob of python file paths to exclude (Optional)  |  `None`  |  
|  `exclude_hidden`  |  `bool`  |  Whether to exclude hidden files (dotfiles).  |  `True`  |  
|  `exclude_empty`  |  `bool`  |  Whether to exclude empty files (Optional).  |  `False`  |  
|  `encoding`  |  Encoding of the files. Default is utf-8.  |  `'utf-8'`  |  
|  `errors`  |  how encoding and decoding errors are to be handled, see https://docs.python.org/3/library/functions.html#open  |  `'ignore'`  |  
|  `recursive`  |  `bool`  |  Whether to recursively search in subdirectories. False by default.  |  `False`  |  
|  `filename_as_id`  |  `bool`  |  Whether to use the filename as the document id. False by default.  |  `False`  |  
|  `required_exts`  |  `Optional[List[str]]`  |  List of required extensions. Default is None.  |  `None`  |  
|  `file_extractor`  |  `Optional[Dict[str, BaseReader[](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.BaseReader "BaseReader \(llama_index.core.readers.base.BaseReader\)")]]`  |  A mapping of file extension to a BaseReader class that specifies how to convert that file to text. If not specified, use default from DEFAULT_FILE_READER_CLS.  |  `None`  |  
|  `num_files_limit`  |  `Optional[int]`  |  Maximum number of files to read. Default is None.  |  `None`  |  
|  `file_metadata`  |  `Optional[Callable[[str], Dict]]`  |  A function that takes in a filename and returns a Dict of metadata for the Document. Default is None.  |  `None`  |  
|  `raise_on_error`  |  `bool`  |  Whether to raise an error if a file cannot be read.  |  `False`  |  
|  `Optional[AbstractFileSystem]`  |  File system to use. Defaults  |  `None`  |  
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
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
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
870
871
872
873
```
 | 
```
classSimpleDirectoryReader(BaseReader, ResourcesReaderMixin, FileSystemReaderMixin):
"""
    Simple directory reader.

    Load files from file directory.
    Automatically select the best file reader given file extensions.

    Args:
        input_dir (Union[Path, str]): Path to the directory.
        input_files (List): List of file paths to read
            (Optional; overrides input_dir, exclude)
        exclude (List): glob of python file paths to exclude (Optional)
        exclude_hidden (bool): Whether to exclude hidden files (dotfiles).
        exclude_empty (bool): Whether to exclude empty files (Optional).
        encoding (str): Encoding of the files.
            Default is utf-8.
        errors (str): how encoding and decoding errors are to be handled,
              see https://docs.python.org/3/library/functions.html#open
        recursive (bool): Whether to recursively search in subdirectories.
            False by default.
        filename_as_id (bool): Whether to use the filename as the document id.
            False by default.
        required_exts (Optional[List[str]]): List of required extensions.
            Default is None.
        file_extractor (Optional[Dict[str, BaseReader]]): A mapping of file
            extension to a BaseReader class that specifies how to convert that file
            to text. If not specified, use default from DEFAULT_FILE_READER_CLS.
        num_files_limit (Optional[int]): Maximum number of files to read.
            Default is None.
        file_metadata (Optional[Callable[[str], Dict]]): A function that takes
            in a filename and returns a Dict of metadata for the Document.
            Default is None.
        raise_on_error (bool): Whether to raise an error if a file cannot be read.
        fs (Optional[fsspec.AbstractFileSystem]): File system to use. Defaults
        to using the local file system. Can be changed to use any remote file system
        exposed via the fsspec interface.

    """

    supported_suffix_fn: Callable = _try_loading_included_file_formats

    def__init__(
        self,
        input_dir: Optional[Union[Path, str]] = None,
        input_files: Optional[list] = None,
        exclude: Optional[list] = None,
        exclude_hidden: bool = True,
        exclude_empty: bool = False,
        errors: str = "ignore",
        recursive: bool = False,
        encoding: str = "utf-8",
        filename_as_id: bool = False,
        required_exts: Optional[list[str]] = None,
        file_extractor: Optional[dict[str, BaseReader]] = None,
        num_files_limit: Optional[int] = None,
        file_metadata: Optional[Callable[[str], dict]] = None,
        raise_on_error: bool = False,
        fs: fsspec.AbstractFileSystem | None = None,
    ) -> None:
"""Initialize with parameters."""
        super().__init__()

        if not input_dir and not input_files:
            raise ValueError("Must provide either `input_dir` or `input_files`.")

        self.fs = fs or get_default_fs()
        self.errors = errors
        self.encoding = encoding

        self.exclude = exclude
        self.recursive = recursive
        self.exclude_hidden = exclude_hidden
        self.exclude_empty = exclude_empty
        self.required_exts = required_exts
        self.num_files_limit = num_files_limit
        self.raise_on_error = raise_on_error
        _Path = Path if is_default_fs(self.fs) else PurePosixPath

        if input_files:
            self.input_files = []
            for path in input_files:
                if not self.fs.isfile(path):
                    raise ValueError(f"File {path} does not exist.")
                input_file = _Path(path)
                self.input_files.append(input_file)
        elif input_dir:
            if not self.fs.isdir(input_dir):
                raise ValueError(f"Directory {input_dir} does not exist.")
            self.input_dir = _Path(input_dir)
            self.exclude = exclude
            self.input_files = self._add_files(self.input_dir)

        self.file_extractor = file_extractor or {}
        self.file_metadata = file_metadata or _DefaultFileMetadataFunc(self.fs)
        self.filename_as_id = filename_as_id

    defis_hidden(self, path: Path | PurePosixPath) -> bool:
        return any(
            part.startswith(".") and part not in [".", ".."] for part in path.parts
        )

    defis_empty_file(self, path: Path | PurePosixPath) -> bool:
        return self.fs.isfile(str(path)) and self.fs.info(str(path)).get("size", 0) == 0

    def_is_directory(self, path: Path | PurePosixPath) -> bool:
"""
        Check if a path is a directory, with special handling for S3 filesystems.

        For S3 filesystems, directories are often represented as 0-byte objects
        ending with '/'. This method provides more reliable directory detection
        than fs.isdir() alone.
        """
        try:
            # First try the standard isdir check
            if self.fs.isdir(path):
                return True

            # For non-default filesystems (like S3), also check for directory placeholders
            if not is_default_fs(self.fs):
                try:
                    info = self.fs.info(str(path))
                    # Check if it's a 0-byte object ending with '/'
                    # This is how S3 typically represents directory placeholders
                    if (
                        info.get("size", 0) == 0
                        and str(path).endswith("/")
                        and info.get("type") != "file"
                    ):
                        return True
                except Exception:
                    # If we can't get info, fall back to the original isdir check
                    pass

            return False
        except Exception:
            # If anything fails, assume it's not a directory to be safe
            return False

    def_add_files(self, input_dir: Path | PurePosixPath) -> list[Path | PurePosixPath]:
"""Add files."""
        all_files: set[Path | PurePosixPath] = set()
        rejected_files: set[Path | PurePosixPath] = set()
        rejected_dirs: set[Path | PurePosixPath] = set()
        # Default to POSIX paths for non-default file systems (e.g. S3)
        _Path = Path if is_default_fs(self.fs) else PurePosixPath

        if self.exclude is not None:
            for excluded_pattern in self.exclude:
                if self.recursive:
                    # Recursive glob
                    excluded_glob = _Path(input_dir) / _Path("**") / excluded_pattern
                else:
                    # Non-recursive glob
                    excluded_glob = _Path(input_dir) / excluded_pattern
                for file in self.fs.glob(str(excluded_glob)):
                    if self.fs.isdir(file):
                        rejected_dirs.add(_Path(str(file)))
                    else:
                        rejected_files.add(_Path(str(file)))

        file_refs: list[Union[Path, PurePosixPath]] = []
        limit = (
            self.num_files_limit
            if self.num_files_limit is not None and self.num_files_limit  0
            else None
        )
        c = 0
        depth = 1000 if self.recursive else 1
        for root, _, files in self.fs.walk(
            str(input_dir), topdown=True, maxdepth=depth
        ):
            for file in files:
                c += 1
                if limit and c  limit:
                    break
                file_refs.append(_Path(root, file))

        for ref in file_refs:
            # Manually check if file is hidden or directory instead of
            # in glob for backwards compatibility.
            is_dir = self._is_directory(ref)
            skip_because_hidden = self.exclude_hidden and self.is_hidden(ref)
            skip_because_empty = self.exclude_empty and self.is_empty_file(ref)
            skip_because_bad_ext = (
                self.required_exts is not None and ref.suffix not in self.required_exts
            )
            skip_because_excluded = ref in rejected_files
            if not skip_because_excluded:
                if is_dir:
                    ref_parent_dir = ref
                else:
                    ref_parent_dir = self.fs._parent(ref)
                for rejected_dir in rejected_dirs:
                    if str(ref_parent_dir).startswith(str(rejected_dir)):
                        skip_because_excluded = True
                        logger.debug(
                            "Skipping %s because it in parent dir %s which is in %s",
                            ref,
                            ref_parent_dir,
                            rejected_dir,
                        )
                        break

            if (
                is_dir
                or skip_because_hidden
                or skip_because_bad_ext
                or skip_because_excluded
                or skip_because_empty
            ):
                continue
            else:
                all_files.add(ref)

        new_input_files = sorted(all_files)

        if len(new_input_files) == 0:
            raise ValueError(f"No files found in {input_dir}.")

        # print total number of files added
        logger.debug(
            f"> [SimpleDirectoryReader] Total files added: {len(new_input_files)}"
        )

        return new_input_files

    def_exclude_metadata(self, documents: list[Document]) -> list[Document]:
"""
        Exclude metadata from documents.

        Args:
            documents (List[Document]): List of documents.

        """
        for doc in documents:
            # Keep only metadata['file_path'] in both embedding and llm content
            # str, which contain extreme important context that about the chunks.
            # Dates is provided for convenience of postprocessor such as
            # TimeWeightedPostprocessor, but excluded for embedding and LLMprompts
            doc.excluded_embed_metadata_keys.extend(
                [
                    "file_name",
                    "file_type",
                    "file_size",
                    "creation_date",
                    "last_modified_date",
                    "last_accessed_date",
                ]
            )
            doc.excluded_llm_metadata_keys.extend(
                [
                    "file_name",
                    "file_type",
                    "file_size",
                    "creation_date",
                    "last_modified_date",
                    "last_accessed_date",
                ]
            )

        return documents

    deflist_resources(self, *args: Any, **kwargs: Any) -> list[str]:
"""List files in the given filesystem."""
        return [str(x) for x in self.input_files]

    defget_resource_info(self, resource_id: str, *args: Any, **kwargs: Any) -> dict:
        info_result = self.fs.info(resource_id)

        creation_date = _format_file_timestamp(
            info_result.get("created"), include_time=True
        )
        last_modified_date = _format_file_timestamp(
            info_result.get("mtime"), include_time=True
        )

        info_dict = {
            "file_path": resource_id,
            "file_size": info_result.get("size"),
            "creation_date": creation_date,
            "last_modified_date": last_modified_date,
        }

        # Ignore None values
        return {
            meta_key: meta_value
            for meta_key, meta_value in info_dict.items()
            if meta_value is not None
        }

    defload_resource(
        self, resource_id: str, *args: Any, **kwargs: Any
    ) -> list[Document]:
        file_metadata = kwargs.get("file_metadata", self.file_metadata)
        file_extractor = kwargs.get("file_extractor", self.file_extractor)
        filename_as_id = kwargs.get("filename_as_id", self.filename_as_id)
        encoding = kwargs.get("encoding", self.encoding)
        errors = kwargs.get("errors", self.errors)
        raise_on_error = kwargs.get("raise_on_error", self.raise_on_error)
        fs = kwargs.get("fs", self.fs)

        _Path = Path if is_default_fs(fs) else PurePosixPath

        return SimpleDirectoryReader.load_file(
            input_file=_Path(resource_id),
            file_metadata=file_metadata,
            file_extractor=file_extractor,
            filename_as_id=filename_as_id,
            encoding=encoding,
            errors=errors,
            raise_on_error=raise_on_error,
            fs=fs,
            **kwargs,
        )

    async defaload_resource(
        self, resource_id: str, *args: Any, **kwargs: Any
    ) -> list[Document]:
        file_metadata = kwargs.get("file_metadata", self.file_metadata)
        file_extractor = kwargs.get("file_extractor", self.file_extractor)
        filename_as_id = kwargs.get("filename_as_id", self.filename_as_id)
        encoding = kwargs.get("encoding", self.encoding)
        errors = kwargs.get("errors", self.errors)
        raise_on_error = kwargs.get("raise_on_error", self.raise_on_error)
        fs = kwargs.get("fs", self.fs)
        _Path = Path if is_default_fs(fs) else PurePosixPath

        return await SimpleDirectoryReader.aload_file(
            input_file=_Path(resource_id),
            file_metadata=file_metadata,
            file_extractor=file_extractor,
            filename_as_id=filename_as_id,
            encoding=encoding,
            errors=errors,
            raise_on_error=raise_on_error,
            fs=fs,
            **kwargs,
        )

    defread_file_content(self, input_file: Path, **kwargs: Any) -> bytes:
"""Read file content."""
        fs: fsspec.AbstractFileSystem = kwargs.get("fs", self.fs)
        with fs.open(input_file, errors=self.errors, encoding=self.encoding) as f:
            # default mode is 'rb', we can cast the return value of f.read()
            return cast(bytes, f.read())

    @staticmethod
    defload_file(
        input_file: Path | PurePosixPath,
        file_metadata: Callable[[str], dict],
        file_extractor: dict[str, BaseReader],
        filename_as_id: bool = False,
        encoding: str = "utf-8",
        errors: str = "ignore",
        raise_on_error: bool = False,
        fs: fsspec.AbstractFileSystem | None = None,
    ) -> list[Document]:
"""
        Static method for loading file.

        NOTE: necessarily as a static method for parallel processing.

        Args:
            input_file (Path): File path to read
            file_metadata ([Callable[[str], Dict]]): A function that takes
                in a filename and returns a Dict of metadata for the Document.
            file_extractor (Dict[str, BaseReader]): A mapping of file
                extension to a BaseReader class that specifies how to convert that file
                to text.
            filename_as_id (bool): Whether to use the filename as the document id.
            encoding (str): Encoding of the files.
                Default is utf-8.
            errors (str): how encoding and decoding errors are to be handled,
                see https://docs.python.org/3/library/functions.html#open
            raise_on_error (bool): Whether to raise an error if a file cannot be read.
            fs (Optional[fsspec.AbstractFileSystem]): File system to use. Defaults
                to using the local file system. Can be changed to use any remote file system

        Returns:
            List[Document]: loaded documents

        """
        # TODO: make this less redundant
        default_file_reader_cls = SimpleDirectoryReader.supported_suffix_fn()
        default_file_reader_suffix = list(default_file_reader_cls.keys())
        metadata: dict | None = None
        documents: list[Document] = []

        if file_metadata is not None:
            metadata = file_metadata(str(input_file))

        file_suffix = input_file.suffix.lower()
        if file_suffix in default_file_reader_suffix or file_suffix in file_extractor:
            # use file readers
            if file_suffix not in file_extractor:
                # instantiate file reader if not already
                reader_cls = default_file_reader_cls[file_suffix]
                file_extractor[file_suffix] = reader_cls()
            reader = file_extractor[file_suffix]

            # load data -- catch all errors except for ImportError
            try:
                kwargs: dict[str, Any] = {"extra_info": metadata}
                if fs and not is_default_fs(fs):
                    kwargs["fs"] = fs
                docs = reader.load_data(input_file, **kwargs)
            except ImportError as e:
                # ensure that ImportError is raised so user knows
                # about missing dependencies
                raise ImportError(str(e))
            except Exception as e:
                if raise_on_error:
                    raise Exception("Error loading file") frome
                # otherwise, just skip the file and report the error
                print(
                    f"Failed to load file {input_file} with error: {e}. Skipping...",
                    flush=True,
                )
                return []

            # iterate over docs if needed
            if filename_as_id:
                for i, doc in enumerate(docs):
                    doc.id_ = f"{input_file!s}_part_{i}"

            documents.extend(docs)
        else:
            # do standard read
            fs = fs or get_default_fs()
            with fs.open(input_file, errors=errors, encoding=encoding) as f:
                data = cast(bytes, f.read()).decode(encoding, errors=errors)

            doc = Document(text=data, metadata=metadata or {})  # type: ignore
            if filename_as_id:
                doc.id_ = str(input_file)

            documents.append(doc)

        return documents

    @staticmethod
    async defaload_file(
        input_file: Path | PurePosixPath,
        file_metadata: Callable[[str], dict],
        file_extractor: dict[str, BaseReader],
        filename_as_id: bool = False,
        encoding: str = "utf-8",
        errors: str = "ignore",
        raise_on_error: bool = False,
        fs: fsspec.AbstractFileSystem | None = None,
    ) -> list[Document]:
"""Load file asynchronously."""
        # TODO: make this less redundant
        default_file_reader_cls = SimpleDirectoryReader.supported_suffix_fn()
        default_file_reader_suffix = list(default_file_reader_cls.keys())
        metadata: dict | None = None
        documents: list[Document] = []

        if file_metadata is not None:
            metadata = file_metadata(str(input_file))

        file_suffix = input_file.suffix.lower()
        if file_suffix in default_file_reader_suffix or file_suffix in file_extractor:
            # use file readers
            if file_suffix not in file_extractor:
                # instantiate file reader if not already
                reader_cls = default_file_reader_cls[file_suffix]
                file_extractor[file_suffix] = reader_cls()
            reader = file_extractor[file_suffix]

            # load data -- catch all errors except for ImportError
            try:
                kwargs: dict[str, Any] = {"extra_info": metadata}
                if fs and not is_default_fs(fs):
                    kwargs["fs"] = fs
                docs = await reader.aload_data(input_file, **kwargs)
            except ImportError as e:
                # ensure that ImportError is raised so user knows
                # about missing dependencies
                raise ImportError(str(e))
            except Exception as e:
                if raise_on_error:
                    raise
                # otherwise, just skip the file and report the error
                print(
                    f"Failed to load file {input_file} with error: {e}. Skipping...",
                    flush=True,
                )
                return []

            # iterate over docs if needed
            if filename_as_id:
                for i, doc in enumerate(docs):
                    doc.id_ = f"{input_file!s}_part_{i}"

            documents.extend(docs)
        else:
            # do standard read
            fs = fs or get_default_fs()
            with fs.open(input_file, errors=errors, encoding=encoding) as f:
                data = cast(bytes, f.read()).decode(encoding, errors=errors)

            doc = Document(text=data, metadata=metadata or {})  # type: ignore
            if filename_as_id:
                doc.id_ = str(input_file)

            documents.append(doc)

        return documents

    defload_data(
        self,
        show_progress: bool = False,
        num_workers: int | None = None,
        fs: fsspec.AbstractFileSystem | None = None,
    ) -> list[Document]:
"""
        Load data from the input directory.

        Args:
            show_progress (bool): Whether to show tqdm progress bars. Defaults to False.
            num_workers  (Optional[int]): Number of workers to parallelize data-loading over.
            fs (Optional[fsspec.AbstractFileSystem]): File system to use. If fs was specified
                in the constructor, it will override the fs parameter here.

        Returns:
            List[Document]: A list of documents.

        """
        documents = []

        fs = fs or self.fs
        load_file_with_args = partial(
            SimpleDirectoryReader.load_file,
            file_metadata=self.file_metadata,
            file_extractor=self.file_extractor,
            filename_as_id=self.filename_as_id,
            encoding=self.encoding,
            errors=self.errors,
            raise_on_error=self.raise_on_error,
            fs=fs,
        )

        if num_workers and num_workers  1:
            num_cpus = multiprocessing.cpu_count()
            if num_workers  num_cpus:
                warnings.warn(
                    "Specified num_workers exceed number of CPUs in the system. "
                    "Setting `num_workers` down to the maximum CPU count.",
                    stacklevel=2,
                )
                num_workers = num_cpus

            with multiprocessing.get_context("spawn").Pool(num_workers) as pool:
                map_iterator = cast(
                    Iterable[list[Document]],
                    get_tqdm_iterable(
                        pool.imap(load_file_with_args, self.input_files),
                        show_progress=show_progress,
                        desc="Loading files",
                        total=len(self.input_files),
                    ),
                )
                for result in map_iterator:
                    documents.extend(result)

        else:
            files_to_process = cast(
                list[Union[Path, PurePosixPath]],
                get_tqdm_iterable(
                    self.input_files,
                    show_progress=show_progress,
                    desc="Loading files",
                ),
            )
            for input_file in files_to_process:
                documents.extend(load_file_with_args(input_file))

        return self._exclude_metadata(documents)

    async defaload_data(
        self,
        show_progress: bool = False,
        num_workers: int | None = None,
        fs: fsspec.AbstractFileSystem | None = None,
    ) -> list[Document]:
"""
        Load data from the input directory.

        Args:
            show_progress (bool): Whether to show tqdm progress bars. Defaults to False.
            num_workers  (Optional[int]): Number of workers to parallelize data-loading over.
            fs (Optional[fsspec.AbstractFileSystem]): File system to use. If fs was specified
                in the constructor, it will override the fs parameter here.

        Returns:
            List[Document]: A list of documents.

        """
        files_to_process = self.input_files
        fs = fs or self.fs

        coroutines = [
            SimpleDirectoryReader.aload_file(
                input_file,
                self.file_metadata,
                self.file_extractor,
                self.filename_as_id,
                self.encoding,
                self.errors,
                self.raise_on_error,
                fs,
            )
            for input_file in files_to_process
        ]

        if num_workers:
            document_lists = await run_jobs(
                coroutines, show_progress=show_progress, workers=num_workers
            )
        elif show_progress:
            _asyncio = get_asyncio_module(show_progress=show_progress)
            document_lists = await _asyncio.gather(*coroutines)
        else:
            document_lists = await asyncio.gather(*coroutines)
        documents = [doc for doc_list in document_lists for doc in doc_list]

        return self._exclude_metadata(documents)

    defiter_data(
        self, show_progress: bool = False
    ) -> Generator[list[Document], Any, Any]:
"""
        Load data iteratively from the input directory.

        Args:
            show_progress (bool): Whether to show tqdm progress bars. Defaults to False.

        Returns:
            Generator[List[Document]]: A list of documents.

        """
        files_to_process = cast(
            list[Union[Path, PurePosixPath]],
            get_tqdm_iterable(
                self.input_files,
                show_progress=show_progress,
                desc="Loading files",
            ),
        )
        for input_file in files_to_process:
            documents = SimpleDirectoryReader.load_file(
                input_file=input_file,
                file_metadata=self.file_metadata,
                file_extractor=self.file_extractor,
                filename_as_id=self.filename_as_id,
                encoding=self.encoding,
                errors=self.errors,
                raise_on_error=self.raise_on_error,
                fs=self.fs,
            )

            documents = self._exclude_metadata(documents)

            if len(documents)  0:
                yield documents

```
 |  
| --- | --- |  
###  list_resources [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SimpleDirectoryReader.list_resources "Permanent link")

```
list_resources(*args: , **kwargs: ) -> []

```

List files in the given filesystem.
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
470
471
472
```
 | 
```
deflist_resources(self, *args: Any, **kwargs: Any) -> list[str]:
"""List files in the given filesystem."""
    return [str(x) for x in self.input_files]

```
 |  
| --- | --- |  
###  read_file_content [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SimpleDirectoryReader.read_file_content "Permanent link")

```
read_file_content(input_file: , **kwargs: ) -> bytes

```

Read file content.
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
547
548
549
550
551
552
```
 | 
```
defread_file_content(self, input_file: Path, **kwargs: Any) -> bytes:
"""Read file content."""
    fs: fsspec.AbstractFileSystem = kwargs.get("fs", self.fs)
    with fs.open(input_file, errors=self.errors, encoding=self.encoding) as f:
        # default mode is 'rb', we can cast the return value of f.read()
        return cast(bytes, f.read())

```
 |  
| --- | --- |  
###  load_file `staticmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SimpleDirectoryReader.load_file "Permanent link")

```
load_file(
    input_file:  | PurePosixPath,
    file_metadata: Callable[[], ],
    file_extractor: [, ],
    filename_as_id:  = False,
    encoding:  = "utf-8",
    errors:  = "ignore",
    raise_on_error:  = False,
    fs: AbstractFileSystem | None = None,
) -> []

```

Static method for loading file.
NOTE: necessarily as a static method for parallel processing.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `input_file`  |  `Path`  |  File path to read  |  _required_  |  
|  `file_metadata`  |  `[Callable[[str], Dict]]`  |  A function that takes in a filename and returns a Dict of metadata for the Document.  |  _required_  |  
|  `file_extractor`  |  `Dict[str, BaseReader[](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.BaseReader "BaseReader \(llama_index.core.readers.base.BaseReader\)")]`  |  A mapping of file extension to a BaseReader class that specifies how to convert that file to text.  |  _required_  |  
|  `filename_as_id`  |  `bool`  |  Whether to use the filename as the document id.  |  `False`  |  
|  `encoding`  |  Encoding of the files. Default is utf-8.  |  `'utf-8'`  |  
|  `errors`  |  how encoding and decoding errors are to be handled, see https://docs.python.org/3/library/functions.html#open  |  `'ignore'`  |  
|  `raise_on_error`  |  `bool`  |  Whether to raise an error if a file cannot be read.  |  `False`  |  
|  `Optional[AbstractFileSystem]`  |  File system to use. Defaults to using the local file system. Can be changed to use any remote file system  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: loaded documents  |  
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
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
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
```
 | 
```
@staticmethod
defload_file(
    input_file: Path | PurePosixPath,
    file_metadata: Callable[[str], dict],
    file_extractor: dict[str, BaseReader],
    filename_as_id: bool = False,
    encoding: str = "utf-8",
    errors: str = "ignore",
    raise_on_error: bool = False,
    fs: fsspec.AbstractFileSystem | None = None,
) -> list[Document]:
"""
    Static method for loading file.

    NOTE: necessarily as a static method for parallel processing.

    Args:
        input_file (Path): File path to read
        file_metadata ([Callable[[str], Dict]]): A function that takes
            in a filename and returns a Dict of metadata for the Document.
        file_extractor (Dict[str, BaseReader]): A mapping of file
            extension to a BaseReader class that specifies how to convert that file
            to text.
        filename_as_id (bool): Whether to use the filename as the document id.
        encoding (str): Encoding of the files.
            Default is utf-8.
        errors (str): how encoding and decoding errors are to be handled,
            see https://docs.python.org/3/library/functions.html#open
        raise_on_error (bool): Whether to raise an error if a file cannot be read.
        fs (Optional[fsspec.AbstractFileSystem]): File system to use. Defaults
            to using the local file system. Can be changed to use any remote file system

    Returns:
        List[Document]: loaded documents

    """
    # TODO: make this less redundant
    default_file_reader_cls = SimpleDirectoryReader.supported_suffix_fn()
    default_file_reader_suffix = list(default_file_reader_cls.keys())
    metadata: dict | None = None
    documents: list[Document] = []

    if file_metadata is not None:
        metadata = file_metadata(str(input_file))

    file_suffix = input_file.suffix.lower()
    if file_suffix in default_file_reader_suffix or file_suffix in file_extractor:
        # use file readers
        if file_suffix not in file_extractor:
            # instantiate file reader if not already
            reader_cls = default_file_reader_cls[file_suffix]
            file_extractor[file_suffix] = reader_cls()
        reader = file_extractor[file_suffix]

        # load data -- catch all errors except for ImportError
        try:
            kwargs: dict[str, Any] = {"extra_info": metadata}
            if fs and not is_default_fs(fs):
                kwargs["fs"] = fs
            docs = reader.load_data(input_file, **kwargs)
        except ImportError as e:
            # ensure that ImportError is raised so user knows
            # about missing dependencies
            raise ImportError(str(e))
        except Exception as e:
            if raise_on_error:
                raise Exception("Error loading file") frome
            # otherwise, just skip the file and report the error
            print(
                f"Failed to load file {input_file} with error: {e}. Skipping...",
                flush=True,
            )
            return []

        # iterate over docs if needed
        if filename_as_id:
            for i, doc in enumerate(docs):
                doc.id_ = f"{input_file!s}_part_{i}"

        documents.extend(docs)
    else:
        # do standard read
        fs = fs or get_default_fs()
        with fs.open(input_file, errors=errors, encoding=encoding) as f:
            data = cast(bytes, f.read()).decode(encoding, errors=errors)

        doc = Document(text=data, metadata=metadata or {})  # type: ignore
        if filename_as_id:
            doc.id_ = str(input_file)

        documents.append(doc)

    return documents

```
 |  
| --- | --- |  
###  aload_file `async` `staticmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SimpleDirectoryReader.aload_file "Permanent link")

```
aload_file(
    input_file:  | PurePosixPath,
    file_metadata: Callable[[], ],
    file_extractor: [, ],
    filename_as_id:  = False,
    encoding:  = "utf-8",
    errors:  = "ignore",
    raise_on_error:  = False,
    fs: AbstractFileSystem | None = None,
) -> []

```

Load file asynchronously.
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
```
 | 
```
@staticmethod
async defaload_file(
    input_file: Path | PurePosixPath,
    file_metadata: Callable[[str], dict],
    file_extractor: dict[str, BaseReader],
    filename_as_id: bool = False,
    encoding: str = "utf-8",
    errors: str = "ignore",
    raise_on_error: bool = False,
    fs: fsspec.AbstractFileSystem | None = None,
) -> list[Document]:
"""Load file asynchronously."""
    # TODO: make this less redundant
    default_file_reader_cls = SimpleDirectoryReader.supported_suffix_fn()
    default_file_reader_suffix = list(default_file_reader_cls.keys())
    metadata: dict | None = None
    documents: list[Document] = []

    if file_metadata is not None:
        metadata = file_metadata(str(input_file))

    file_suffix = input_file.suffix.lower()
    if file_suffix in default_file_reader_suffix or file_suffix in file_extractor:
        # use file readers
        if file_suffix not in file_extractor:
            # instantiate file reader if not already
            reader_cls = default_file_reader_cls[file_suffix]
            file_extractor[file_suffix] = reader_cls()
        reader = file_extractor[file_suffix]

        # load data -- catch all errors except for ImportError
        try:
            kwargs: dict[str, Any] = {"extra_info": metadata}
            if fs and not is_default_fs(fs):
                kwargs["fs"] = fs
            docs = await reader.aload_data(input_file, **kwargs)
        except ImportError as e:
            # ensure that ImportError is raised so user knows
            # about missing dependencies
            raise ImportError(str(e))
        except Exception as e:
            if raise_on_error:
                raise
            # otherwise, just skip the file and report the error
            print(
                f"Failed to load file {input_file} with error: {e}. Skipping...",
                flush=True,
            )
            return []

        # iterate over docs if needed
        if filename_as_id:
            for i, doc in enumerate(docs):
                doc.id_ = f"{input_file!s}_part_{i}"

        documents.extend(docs)
    else:
        # do standard read
        fs = fs or get_default_fs()
        with fs.open(input_file, errors=errors, encoding=encoding) as f:
            data = cast(bytes, f.read()).decode(encoding, errors=errors)

        doc = Document(text=data, metadata=metadata or {})  # type: ignore
        if filename_as_id:
            doc.id_ = str(input_file)

        documents.append(doc)

    return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SimpleDirectoryReader.load_data "Permanent link")

```
load_data(
    show_progress:  = False,
    num_workers:  | None = None,
    fs: AbstractFileSystem | None = None,
) -> []

```

Load data from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
|  `num_workers`  |  `Optional[int]`  |  Number of workers to parallelize data-loading over.  |  `None`  |  
|  `Optional[AbstractFileSystem]`  |  File system to use. If fs was specified in the constructor, it will override the fs parameter here.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
```
 | 
```
defload_data(
    self,
    show_progress: bool = False,
    num_workers: int | None = None,
    fs: fsspec.AbstractFileSystem | None = None,
) -> list[Document]:
"""
    Load data from the input directory.

    Args:
        show_progress (bool): Whether to show tqdm progress bars. Defaults to False.
        num_workers  (Optional[int]): Number of workers to parallelize data-loading over.
        fs (Optional[fsspec.AbstractFileSystem]): File system to use. If fs was specified
            in the constructor, it will override the fs parameter here.

    Returns:
        List[Document]: A list of documents.

    """
    documents = []

    fs = fs or self.fs
    load_file_with_args = partial(
        SimpleDirectoryReader.load_file,
        file_metadata=self.file_metadata,
        file_extractor=self.file_extractor,
        filename_as_id=self.filename_as_id,
        encoding=self.encoding,
        errors=self.errors,
        raise_on_error=self.raise_on_error,
        fs=fs,
    )

    if num_workers and num_workers  1:
        num_cpus = multiprocessing.cpu_count()
        if num_workers  num_cpus:
            warnings.warn(
                "Specified num_workers exceed number of CPUs in the system. "
                "Setting `num_workers` down to the maximum CPU count.",
                stacklevel=2,
            )
            num_workers = num_cpus

        with multiprocessing.get_context("spawn").Pool(num_workers) as pool:
            map_iterator = cast(
                Iterable[list[Document]],
                get_tqdm_iterable(
                    pool.imap(load_file_with_args, self.input_files),
                    show_progress=show_progress,
                    desc="Loading files",
                    total=len(self.input_files),
                ),
            )
            for result in map_iterator:
                documents.extend(result)

    else:
        files_to_process = cast(
            list[Union[Path, PurePosixPath]],
            get_tqdm_iterable(
                self.input_files,
                show_progress=show_progress,
                desc="Loading files",
            ),
        )
        for input_file in files_to_process:
            documents.extend(load_file_with_args(input_file))

    return self._exclude_metadata(documents)

```
 |  
| --- | --- |  
###  aload_data [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SimpleDirectoryReader.aload_data "Permanent link")

```
aload_data(
    show_progress:  = False,
    num_workers:  | None = None,
    fs: AbstractFileSystem | None = None,
) -> []

```

Load data from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
|  `num_workers`  |  `Optional[int]`  |  Number of workers to parallelize data-loading over.  |  `None`  |  
|  `Optional[AbstractFileSystem]`  |  File system to use. If fs was specified in the constructor, it will override the fs parameter here.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
```
 | 
```
async defaload_data(
    self,
    show_progress: bool = False,
    num_workers: int | None = None,
    fs: fsspec.AbstractFileSystem | None = None,
) -> list[Document]:
"""
    Load data from the input directory.

    Args:
        show_progress (bool): Whether to show tqdm progress bars. Defaults to False.
        num_workers  (Optional[int]): Number of workers to parallelize data-loading over.
        fs (Optional[fsspec.AbstractFileSystem]): File system to use. If fs was specified
            in the constructor, it will override the fs parameter here.

    Returns:
        List[Document]: A list of documents.

    """
    files_to_process = self.input_files
    fs = fs or self.fs

    coroutines = [
        SimpleDirectoryReader.aload_file(
            input_file,
            self.file_metadata,
            self.file_extractor,
            self.filename_as_id,
            self.encoding,
            self.errors,
            self.raise_on_error,
            fs,
        )
        for input_file in files_to_process
    ]

    if num_workers:
        document_lists = await run_jobs(
            coroutines, show_progress=show_progress, workers=num_workers
        )
    elif show_progress:
        _asyncio = get_asyncio_module(show_progress=show_progress)
        document_lists = await _asyncio.gather(*coroutines)
    else:
        document_lists = await asyncio.gather(*coroutines)
    documents = [doc for doc_list in document_lists for doc in doc_list]

    return self._exclude_metadata(documents)

```
 |  
| --- | --- |  
###  iter_data [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SimpleDirectoryReader.iter_data "Permanent link")

```
iter_data(
    show_progress:  = False,
) -> Generator[[], , ]

```

Load data iteratively from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  Generator[List[Document]]: A list of documents.  |  
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
870
871
872
873
```
 | 
```
defiter_data(
    self, show_progress: bool = False
) -> Generator[list[Document], Any, Any]:
"""
    Load data iteratively from the input directory.

    Args:
        show_progress (bool): Whether to show tqdm progress bars. Defaults to False.

    Returns:
        Generator[List[Document]]: A list of documents.

    """
    files_to_process = cast(
        list[Union[Path, PurePosixPath]],
        get_tqdm_iterable(
            self.input_files,
            show_progress=show_progress,
            desc="Loading files",
        ),
    )
    for input_file in files_to_process:
        documents = SimpleDirectoryReader.load_file(
            input_file=input_file,
            file_metadata=self.file_metadata,
            file_extractor=self.file_extractor,
            filename_as_id=self.filename_as_id,
            encoding=self.encoding,
            errors=self.errors,
            raise_on_error=self.raise_on_error,
            fs=self.fs,
        )

        documents = self._exclude_metadata(documents)

        if len(documents)  0:
            yield documents

```
 |  
| --- | --- |  
##  Document [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Document "Permanent link")
Bases: 
Generic interface for a data document.
This document connects to data sources.
Source code in `llama-index-core/llama_index/core/schema.py`  
| 
```
1088
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
1113
1114
1115
1116
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
1136
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
1153
1154
1155
1156
1157
1158
1159
1160
1161
1162
1163
1164
1165
1166
1167
1168
1169
1170
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
1188
1189
1190
1191
1192
1193
1194
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
1206
1207
1208
1209
1210
1211
1212
1213
1214
1215
1216
1217
1218
1219
1220
1221
1222
1223
1224
1225
1226
1227
1228
1229
1230
1231
1232
1233
1234
1235
1236
1237
1238
1239
1240
1241
1242
1243
1244
1245
1246
1247
1248
1249
1250
1251
1252
1253
1254
1255
1256
1257
1258
1259
1260
1261
1262
1263
1264
1265
1266
1267
1268
1269
1270
1271
1272
1273
1274
1275
1276
1277
1278
1279
1280
1281
1282
1283
1284
1285
1286
1287
1288
1289
1290
1291
1292
1293
1294
1295
1296
1297
```
 | 
```
classDocument(Node):
"""
    Generic interface for a data document.

    This document connects to data sources.
    """

    def__init__(self, **data: Any) -> None:
"""
        Keeps backward compatibility with old 'Document' versions.

        If 'text' was passed, store it in 'text_resource'.
        If 'doc_id' was passed, store it in 'id_'.
        If 'extra_info' was passed, store it in 'metadata'.
        """
        if "doc_id" in data:
            value = data.pop("doc_id")
            if "id_" in data:
                msg = "'doc_id' is deprecated and 'id_' will be used instead"
                logging.warning(msg)
            else:
                data["id_"] = value

        if "extra_info" in data:
            value = data.pop("extra_info")
            if "metadata" in data:
                msg = "'extra_info' is deprecated and 'metadata' will be used instead"
                logging.warning(msg)
            else:
                data["metadata"] = value

        if data.get("text"):
            text = data.pop("text")
            if "text_resource" in data:
                text_resource = (
                    data["text_resource"]
                    if isinstance(data["text_resource"], MediaResource)
                    else MediaResource.model_validate(data["text_resource"])
                )
                if (text_resource.text or "").strip() != text.strip():
                    msg = (
                        "'text' is deprecated and 'text_resource' will be used instead"
                    )
                    logging.warning(msg)
            else:
                data["text_resource"] = MediaResource(text=text)

        super().__init__(**data)

    @model_serializer(mode="wrap")
    defcustom_model_dump(
        self, handler: SerializerFunctionWrapHandler, info: SerializationInfo
    ) -> Dict[str, Any]:
"""For full backward compatibility with the text field, we customize the model serializer."""
        data = super().custom_model_dump(handler, info)
        exclude_set = set(info.exclude or [])
        if "text" not in exclude_set:
            data["text"] = self.text
        return data

    @property
    deftext(self) -> str:
"""Provided for backward compatibility, it returns the content of text_resource."""
        return self.get_content()

    @classmethod
    defget_type(cls) -> str:
"""Get Document type."""
        return ObjectType.DOCUMENT

    @property
    defdoc_id(self) -> str:
"""Get document ID."""
        return self.id_

    @doc_id.setter
    defdoc_id(self, id_: str) -> None:
        self.id_ = id_

    def__str__(self) -> str:
        source_text_truncated = truncate_text(
            self.get_content().strip(), TRUNCATE_LENGTH
        )
        source_text_wrapped = textwrap.fill(
            f"Text: {source_text_truncated}\n", width=WRAP_WIDTH
        )
        return f"Doc ID: {self.doc_id}\n{source_text_wrapped}"

    @deprecated(
        version="0.12.2",
        reason="'get_doc_id' is deprecated, access the 'id_' property instead.",
    )
    defget_doc_id(self) -> str:  # pragma: nocover
        return self.id_

    defto_langchain_format(self) -> LCDocument:
"""Convert struct to LangChain document format."""
        fromllama_index.core.bridge.langchainimport (
            Document as LCDocument,  # type: ignore
        )

        metadata = self.metadata or {}
        return LCDocument(page_content=self.text, metadata=metadata, id=self.id_)

    @classmethod
    deffrom_langchain_format(cls, doc: LCDocument) -> Document:
"""Convert struct from LangChain document format."""
        if doc.id:
            return cls(text=doc.page_content, metadata=doc.metadata, id_=doc.id)
        return cls(text=doc.page_content, metadata=doc.metadata)

    defto_haystack_format(self) -> HaystackDocument:
"""Convert struct to Haystack document format."""
        fromhaystackimport Document as HaystackDocument  # type: ignore

        return HaystackDocument(
            content=self.text, meta=self.metadata, embedding=self.embedding, id=self.id_
        )

    @classmethod
    deffrom_haystack_format(cls, doc: HaystackDocument) -> Document:
"""Convert struct from Haystack document format."""
        return cls(
            text=doc.content, metadata=doc.meta, embedding=doc.embedding, id_=doc.id
        )

    defto_embedchain_format(self) -> Dict[str, Any]:
"""Convert struct to EmbedChain document format."""
        return {
            "doc_id": self.id_,
            "data": {"content": self.text, "meta_data": self.metadata},
        }

    @classmethod
    deffrom_embedchain_format(cls, doc: Dict[str, Any]) -> Document:
"""Convert struct from EmbedChain document format."""
        return cls(
            text=doc["data"]["content"],
            metadata=doc["data"]["meta_data"],
            id_=doc["doc_id"],
        )

    defto_semantic_kernel_format(self) -> MemoryRecord:
"""Convert struct to Semantic Kernel document format."""
        importnumpyasnp
        fromsemantic_kernel.memory.memory_recordimport MemoryRecord  # type: ignore

        return MemoryRecord(
            id=self.id_,
            text=self.text,
            additional_metadata=self.get_metadata_str(),
            embedding=np.array(self.embedding) if self.embedding else None,
        )

    @classmethod
    deffrom_semantic_kernel_format(cls, doc: MemoryRecord) -> Document:
"""Convert struct from Semantic Kernel document format."""
        return cls(
            text=doc._text,
            metadata={"additional_metadata": doc._additional_metadata},
            embedding=doc._embedding.tolist() if doc._embedding is not None else None,
            id_=doc._id,
        )

    defto_vectorflow(self, client: Any) -> None:
"""Send a document to vectorflow, since they don't have a document object."""
        # write document to temp file
        importtempfile

        with tempfile.NamedTemporaryFile() as f:
            f.write(self.text.encode("utf-8"))
            f.flush()
            client.embed(f.name)

    @classmethod
    defexample(cls) -> Document:
        return Document(
            text=SAMPLE_TEXT,
            metadata={"filename": "README.md", "category": "codebase"},
        )

    @classmethod
    defclass_name(cls) -> str:
        return "Document"

    defto_cloud_document(self) -> CloudDocument:
"""Deprecated: Convert to LlamaCloud document type with <1.0 llama-cloud SDK."""
        fromllama_cloud.types.cloud_documentimport CloudDocument  # type: ignore

        return CloudDocument(
            text=self.text,
            metadata=self.metadata,
            excluded_embed_metadata_keys=self.excluded_embed_metadata_keys,
            excluded_llm_metadata_keys=self.excluded_llm_metadata_keys,
            id=self.id_,
        )

    @classmethod
    deffrom_cloud_document(
        cls,
        doc: CloudDocument,
    ) -> Document:
"""Convert from LlamaCloud document type."""
        return Document(
            text=doc.text,
            metadata=doc.metadata,
            excluded_embed_metadata_keys=doc.excluded_embed_metadata_keys,
            excluded_llm_metadata_keys=doc.excluded_llm_metadata_keys,
            id_=doc.id,
        )

```
 |  
| --- | --- |  
###  text `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Document.text "Permanent link")

```
text: 

```

Provided for backward compatibility, it returns the content of text_resource.
###  doc_id `property` `writable` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Document.doc_id "Permanent link")

```
doc_id: 

```

Get document ID.
###  custom_model_dump [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Document.custom_model_dump "Permanent link")

```
custom_model_dump(
    handler: SerializerFunctionWrapHandler,
    info: SerializationInfo,
) -> [, ]

```

For full backward compatibility with the text field, we customize the model serializer.
Source code in `llama-index-core/llama_index/core/schema.py`  
| 
```
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
```
 | 
```
@model_serializer(mode="wrap")
defcustom_model_dump(
    self, handler: SerializerFunctionWrapHandler, info: SerializationInfo
) -> Dict[str, Any]:
"""For full backward compatibility with the text field, we customize the model serializer."""
    data = super().custom_model_dump(handler, info)
    exclude_set = set(info.exclude or [])
    if "text" not in exclude_set:
        data["text"] = self.text
    return data

```
 |  
| --- | --- |  
###  get_type `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Document.get_type "Permanent link")

```
get_type() -> 

```

Get Document type.
Source code in `llama-index-core/llama_index/core/schema.py`  
| 
```
1153
1154
1155
1156
```
 | 
```
@classmethod
defget_type(cls) -> str:
"""Get Document type."""
    return ObjectType.DOCUMENT

```
 |  
| --- | --- |  
###  to_langchain_format [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Document.to_langchain_format "Permanent link")

```
to_langchain_format() -> Document

```

Convert struct to LangChain document format.
Source code in `llama-index-core/llama_index/core/schema.py`  
| 
```
1183
1184
1185
1186
1187
1188
1189
1190
```
 | 
```
defto_langchain_format(self) -> LCDocument:
"""Convert struct to LangChain document format."""
    fromllama_index.core.bridge.langchainimport (
        Document as LCDocument,  # type: ignore
    )

    metadata = self.metadata or {}
    return LCDocument(page_content=self.text, metadata=metadata, id=self.id_)

```
 |  
| --- | --- |  
###  from_langchain_format `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Document.from_langchain_format "Permanent link")

```
from_langchain_format(doc: Document) -> 

```

Convert struct from LangChain document format.
Source code in `llama-index-core/llama_index/core/schema.py`  
| 
```
1192
1193
1194
1195
1196
1197
```
 | 
```
@classmethod
deffrom_langchain_format(cls, doc: LCDocument) -> Document:
"""Convert struct from LangChain document format."""
    if doc.id:
        return cls(text=doc.page_content, metadata=doc.metadata, id_=doc.id)
    return cls(text=doc.page_content, metadata=doc.metadata)

```
 |  
| --- | --- |  
###  to_haystack_format [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Document.to_haystack_format "Permanent link")

```
to_haystack_format() -> Document

```

Convert struct to Haystack document format.
Source code in `llama-index-core/llama_index/core/schema.py`  
| 
```
1199
1200
1201
1202
1203
1204
1205
```
 | 
```
defto_haystack_format(self) -> HaystackDocument:
"""Convert struct to Haystack document format."""
    fromhaystackimport Document as HaystackDocument  # type: ignore

    return HaystackDocument(
        content=self.text, meta=self.metadata, embedding=self.embedding, id=self.id_
    )

```
 |  
| --- | --- |  
###  from_haystack_format `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Document.from_haystack_format "Permanent link")

```
from_haystack_format(doc: Document) -> 

```

Convert struct from Haystack document format.
Source code in `llama-index-core/llama_index/core/schema.py`  
| 
```
1207
1208
1209
1210
1211
1212
```
 | 
```
@classmethod
deffrom_haystack_format(cls, doc: HaystackDocument) -> Document:
"""Convert struct from Haystack document format."""
    return cls(
        text=doc.content, metadata=doc.meta, embedding=doc.embedding, id_=doc.id
    )

```
 |  
| --- | --- |  
###  to_embedchain_format [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Document.to_embedchain_format "Permanent link")

```
to_embedchain_format() -> [, ]

```

Convert struct to EmbedChain document format.
Source code in `llama-index-core/llama_index/core/schema.py`  
| 
```
1214
1215
1216
1217
1218
1219
```
 | 
```
defto_embedchain_format(self) -> Dict[str, Any]:
"""Convert struct to EmbedChain document format."""
    return {
        "doc_id": self.id_,
        "data": {"content": self.text, "meta_data": self.metadata},
    }

```
 |  
| --- | --- |  
###  from_embedchain_format `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Document.from_embedchain_format "Permanent link")

```
from_embedchain_format(doc: [, ]) -> 

```

Convert struct from EmbedChain document format.
Source code in `llama-index-core/llama_index/core/schema.py`  
| 
```
1221
1222
1223
1224
1225
1226
1227
1228
```
 | 
```
@classmethod
deffrom_embedchain_format(cls, doc: Dict[str, Any]) -> Document:
"""Convert struct from EmbedChain document format."""
    return cls(
        text=doc["data"]["content"],
        metadata=doc["data"]["meta_data"],
        id_=doc["doc_id"],
    )

```
 |  
| --- | --- |  
###  to_semantic_kernel_format [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Document.to_semantic_kernel_format "Permanent link")

```
to_semantic_kernel_format() -> MemoryRecord

```

Convert struct to Semantic Kernel document format.
Source code in `llama-index-core/llama_index/core/schema.py`  
| 
```
1230
1231
1232
1233
1234
1235
1236
1237
1238
1239
1240
```
 | 
```
defto_semantic_kernel_format(self) -> MemoryRecord:
"""Convert struct to Semantic Kernel document format."""
    importnumpyasnp
    fromsemantic_kernel.memory.memory_recordimport MemoryRecord  # type: ignore

    return MemoryRecord(
        id=self.id_,
        text=self.text,
        additional_metadata=self.get_metadata_str(),
        embedding=np.array(self.embedding) if self.embedding else None,
    )

```
 |  
| --- | --- |  
###  from_semantic_kernel_format `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Document.from_semantic_kernel_format "Permanent link")

```
from_semantic_kernel_format(doc: MemoryRecord) -> 

```

Convert struct from Semantic Kernel document format.
Source code in `llama-index-core/llama_index/core/schema.py`  
| 
```
1242
1243
1244
1245
1246
1247
1248
1249
1250
```
 | 
```
@classmethod
deffrom_semantic_kernel_format(cls, doc: MemoryRecord) -> Document:
"""Convert struct from Semantic Kernel document format."""
    return cls(
        text=doc._text,
        metadata={"additional_metadata": doc._additional_metadata},
        embedding=doc._embedding.tolist() if doc._embedding is not None else None,
        id_=doc._id,
    )

```
 |  
| --- | --- |  
###  to_vectorflow [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Document.to_vectorflow "Permanent link")

```
to_vectorflow(client: ) -> None

```

Send a document to vectorflow, since they don't have a document object.
Source code in `llama-index-core/llama_index/core/schema.py`  
| 
```
1252
1253
1254
1255
1256
1257
1258
1259
1260
```
 | 
```
defto_vectorflow(self, client: Any) -> None:
"""Send a document to vectorflow, since they don't have a document object."""
    # write document to temp file
    importtempfile

    with tempfile.NamedTemporaryFile() as f:
        f.write(self.text.encode("utf-8"))
        f.flush()
        client.embed(f.name)

```
 |  
| --- | --- |  
###  to_cloud_document [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Document.to_cloud_document "Permanent link")

```
to_cloud_document() -> CloudDocument

```

Deprecated: Convert to LlamaCloud document type with <1.0 llama-cloud SDK.
Source code in `llama-index-core/llama_index/core/schema.py`  
| 
```
1273
1274
1275
1276
1277
1278
1279
1280
1281
1282
1283
```
 | 
```
defto_cloud_document(self) -> CloudDocument:
"""Deprecated: Convert to LlamaCloud document type with <1.0 llama-cloud SDK."""
    fromllama_cloud.types.cloud_documentimport CloudDocument  # type: ignore

    return CloudDocument(
        text=self.text,
        metadata=self.metadata,
        excluded_embed_metadata_keys=self.excluded_embed_metadata_keys,
        excluded_llm_metadata_keys=self.excluded_llm_metadata_keys,
        id=self.id_,
    )

```
 |  
| --- | --- |  
###  from_cloud_document `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Document.from_cloud_document "Permanent link")

```
from_cloud_document(doc: CloudDocument) -> 

```

Convert from LlamaCloud document type.
Source code in `llama-index-core/llama_index/core/schema.py`  
| 
```
1285
1286
1287
1288
1289
1290
1291
1292
1293
1294
1295
1296
1297
```
 | 
```
@classmethod
deffrom_cloud_document(
    cls,
    doc: CloudDocument,
) -> Document:
"""Convert from LlamaCloud document type."""
    return Document(
        text=doc.text,
        metadata=doc.metadata,
        excluded_embed_metadata_keys=doc.excluded_embed_metadata_keys,
        excluded_llm_metadata_keys=doc.excluded_llm_metadata_keys,
        id_=doc.id,
    )

```
 |  
| --- | --- |  
##  QueryBundle `dataclass` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.QueryBundle "Permanent link")
Bases: `DataClassJsonMixin`
Query bundle.
This dataclass contains the original query string and associated transformations.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_str`  |  the original user-specified query string. This is currently used by all non embedding-based queries.  |  _required_  |  
|  `custom_embedding_strs`  |  `Optional[List[str]]`  |  list of strings used for embedding the query. This is currently used by all embedding-based queries.  |  `None`  |  
|  `embedding`  |  `Optional[List[float]]`  |  the stored embedding for the query.  |  `None`  |  
|  `image_path`  |  `Optional[str]`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/schema.py`  
| 
```
1439
1440
1441
1442
1443
1444
1445
1446
1447
1448
1449
1450
1451
1452
1453
1454
1455
1456
1457
1458
1459
1460
1461
1462
1463
1464
1465
1466
1467
1468
1469
1470
1471
1472
1473
1474
1475
1476
1477
1478
1479
1480
```
 | 
```
@dataclass
classQueryBundle(DataClassJsonMixin):
"""
    Query bundle.

    This dataclass contains the original query string and associated transformations.

    Args:
        query_str (str): the original user-specified query string.
            This is currently used by all non embedding-based queries.
        custom_embedding_strs (list[str]): list of strings used for embedding the query.
            This is currently used by all embedding-based queries.
        embedding (list[float]): the stored embedding for the query.

    """

    query_str: str
    # using single image path as query input
    image_path: Optional[str] = None
    custom_embedding_strs: Optional[List[str]] = None
    embedding: Optional[List[float]] = None

    @property
    defembedding_strs(self) -> List[str]:
"""Use custom embedding strs if specified, otherwise use query str."""
        if self.custom_embedding_strs is None:
            if len(self.query_str) == 0:
                return []
            return [self.query_str]
        else:
            return self.custom_embedding_strs

    @property
    defembedding_image(self) -> List[ImageType]:
"""Use image path for image retrieval."""
        if self.image_path is None:
            return []
        return [self.image_path]

    def__str__(self) -> str:
"""Convert to string representation."""
        return self.query_str

```
 |  
| --- | --- |  
###  embedding_strs `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.QueryBundle.embedding_strs "Permanent link")

```
embedding_strs: []

```

Use custom embedding strs if specified, otherwise use query str.
###  embedding_image `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.QueryBundle.embedding_image "Permanent link")

```
embedding_image: [ImageType]

```

Use image path for image retrieval.
##  ServiceContext [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.ServiceContext "Permanent link")
Service Context container.
NOTE: Deprecated, use llama_index.settings.Settings instead or pass in modules to local functions/methods/interfaces.
Source code in `llama-index-core/llama_index/core/service_context.py`  
| 
```
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
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
```
 | 
```
classServiceContext:
"""
    Service Context container.

    NOTE: Deprecated, use llama_index.settings.Settings instead or pass in
    modules to local functions/methods/interfaces.

    """

    def__init__(self, **kwargs: Any) -> None:
        raise ValueError(
            "ServiceContext is deprecated. Use llama_index.settings.Settings instead, "
            "or pass in modules to local functions/methods/interfaces.\n"
            "See the docs for updated usage/migration: \n"
            "https://docs.llamaindex.ai/en/stable/module_guides/supporting_modules/service_context_migration/"
        )

    @classmethod
    deffrom_defaults(
        cls,
        **kwargs: Any,
    ) -> "ServiceContext":
"""
        Create a ServiceContext from defaults.

        NOTE: Deprecated, use llama_index.settings.Settings instead or pass in
        modules to local functions/methods/interfaces.

        """
        raise ValueError(
            "ServiceContext is deprecated. Use llama_index.settings.Settings instead, "
            "or pass in modules to local functions/methods/interfaces.\n"
            "See the docs for updated usage/migration: \n"
            "https://docs.llamaindex.ai/en/stable/module_guides/supporting_modules/service_context_migration/"
        )

```
 |  
| --- | --- |  
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.ServiceContext.from_defaults "Permanent link")

```
from_defaults(**kwargs: ) -> 

```

Create a ServiceContext from defaults.
NOTE: Deprecated, use llama_index.settings.Settings instead or pass in modules to local functions/methods/interfaces.
Source code in `llama-index-core/llama_index/core/service_context.py`  
| 
```
21
22
23
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    **kwargs: Any,
) -> "ServiceContext":
"""
    Create a ServiceContext from defaults.

    NOTE: Deprecated, use llama_index.settings.Settings instead or pass in
    modules to local functions/methods/interfaces.

    """
    raise ValueError(
        "ServiceContext is deprecated. Use llama_index.settings.Settings instead, "
        "or pass in modules to local functions/methods/interfaces.\n"
        "See the docs for updated usage/migration: \n"
        "https://docs.llamaindex.ai/en/stable/module_guides/supporting_modules/service_context_migration/"
    )

```
 |  
| --- | --- |  
##  StorageContext `dataclass` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.StorageContext "Permanent link")
Storage context.
The storage context container is a utility container for storing nodes, indices, and vectors. It contains the following: - docstore: BaseDocumentStore - index_store: BaseIndexStore - vector_store: BasePydanticVectorStore - graph_store: GraphStore - property_graph_store: PropertyGraphStore (lazily initialized)
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `docstore`  |   |  _required_  |  
|  `index_store`  |   |  _required_  |  
|  `vector_stores`  |  `Dict[str, Annotated[BasePydanticVectorStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore "BasePydanticVectorStore \(llama_index.core.vector_stores.types.BasePydanticVectorStore\)"), SerializeAsAny]]`  |  _required_  |  
|  `graph_store`  |   |  _required_  |  
|  `property_graph_store`  |  `PropertyGraphStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.PropertyGraphStore "PropertyGraphStore \(llama_index.core.graph_stores.types.PropertyGraphStore\)") | None`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/storage/storage_context.py`  
| 
```
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
```
 | 
```
@dataclass
classStorageContext:
"""
    Storage context.

    The storage context container is a utility container for storing nodes,
    indices, and vectors. It contains the following:
    - docstore: BaseDocumentStore
    - index_store: BaseIndexStore
    - vector_store: BasePydanticVectorStore
    - graph_store: GraphStore
    - property_graph_store: PropertyGraphStore (lazily initialized)

    """

    docstore: BaseDocumentStore
    index_store: BaseIndexStore
    vector_stores: Dict[str, SerializeAsAny[BasePydanticVectorStore]]
    graph_store: GraphStore
    property_graph_store: Optional[PropertyGraphStore] = None

    @classmethod
    deffrom_defaults(
        cls,
        docstore: Optional[BaseDocumentStore] = None,
        index_store: Optional[BaseIndexStore] = None,
        vector_store: Optional[BasePydanticVectorStore] = None,
        image_store: Optional[BasePydanticVectorStore] = None,
        vector_stores: Optional[Dict[str, BasePydanticVectorStore]] = None,
        graph_store: Optional[GraphStore] = None,
        property_graph_store: Optional[PropertyGraphStore] = None,
        persist_dir: Optional[str] = None,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> "StorageContext":
"""
        Create a StorageContext from defaults.

        Args:
            docstore (Optional[BaseDocumentStore]): document store
            index_store (Optional[BaseIndexStore]): index store
            vector_store (Optional[BasePydanticVectorStore]): vector store
            graph_store (Optional[GraphStore]): graph store
            image_store (Optional[BasePydanticVectorStore]): image store

        """
        if persist_dir is None:
            docstore = docstore or SimpleDocumentStore()
            index_store = index_store or SimpleIndexStore()
            graph_store = graph_store or SimpleGraphStore()
            image_store = image_store or SimpleVectorStore()

            if vector_store:
                vector_stores = {DEFAULT_VECTOR_STORE: vector_store}
            else:
                vector_stores = vector_stores or {
                    DEFAULT_VECTOR_STORE: SimpleVectorStore()
                }
            if image_store:
                # append image store to vector stores
                vector_stores[IMAGE_VECTOR_STORE_NAMESPACE] = image_store
        else:
            docstore = docstore or SimpleDocumentStore.from_persist_dir(
                persist_dir, fs=fs
            )
            index_store = index_store or SimpleIndexStore.from_persist_dir(
                persist_dir, fs=fs
            )
            graph_store = graph_store or SimpleGraphStore.from_persist_dir(
                persist_dir, fs=fs
            )

            try:
                property_graph_store = (
                    property_graph_store
                    or SimplePropertyGraphStore.from_persist_dir(persist_dir, fs=fs)
                )
            except FileNotFoundError:
                property_graph_store = None

            if vector_store:
                vector_stores = {DEFAULT_VECTOR_STORE: vector_store}
            elif vector_stores:
                vector_stores = vector_stores
            else:
                vector_stores = SimpleVectorStore.from_namespaced_persist_dir(
                    persist_dir, fs=fs
                )
            if image_store:
                # append image store to vector stores
                vector_stores[IMAGE_VECTOR_STORE_NAMESPACE] = image_store  # type: ignore

        return cls(
            docstore=docstore,
            index_store=index_store,
            vector_stores=vector_stores,  # type: ignore
            graph_store=graph_store,
            property_graph_store=property_graph_store,
        )

    defpersist(
        self,
        persist_dir: Union[str, os.PathLike] = DEFAULT_PERSIST_DIR,
        docstore_fname: str = DOCSTORE_FNAME,
        index_store_fname: str = INDEX_STORE_FNAME,
        vector_store_fname: str = VECTOR_STORE_FNAME,
        image_store_fname: str = IMAGE_STORE_FNAME,
        graph_store_fname: str = GRAPH_STORE_FNAME,
        pg_graph_store_fname: str = PG_FNAME,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> None:
"""
        Persist the storage context.

        Args:
            persist_dir (str): directory to persist the storage context

        """
        if fs is not None:
            persist_dir = str(persist_dir)  # NOTE: doesn't support Windows here
            docstore_path = concat_dirs(persist_dir, docstore_fname)
            index_store_path = concat_dirs(persist_dir, index_store_fname)
            graph_store_path = concat_dirs(persist_dir, graph_store_fname)
            pg_graph_store_path = concat_dirs(persist_dir, pg_graph_store_fname)
        else:
            persist_dir = Path(persist_dir)
            docstore_path = str(persist_dir / docstore_fname)
            index_store_path = str(persist_dir / index_store_fname)
            graph_store_path = str(persist_dir / graph_store_fname)
            pg_graph_store_path = str(persist_dir / pg_graph_store_fname)

        self.docstore.persist(persist_path=docstore_path, fs=fs)
        self.index_store.persist(persist_path=index_store_path, fs=fs)
        self.graph_store.persist(persist_path=graph_store_path, fs=fs)

        if self.property_graph_store:
            self.property_graph_store.persist(persist_path=pg_graph_store_path, fs=fs)

        # save each vector store under it's namespace
        for vector_store_name, vector_store in self.vector_stores.items():
            if fs is not None:
                vector_store_path = concat_dirs(
                    str(persist_dir),
                    f"{vector_store_name}{NAMESPACE_SEP}{vector_store_fname}",
                )
            else:
                vector_store_path = str(
                    Path(persist_dir)
                    / f"{vector_store_name}{NAMESPACE_SEP}{vector_store_fname}"
                )

            vector_store.persist(persist_path=vector_store_path, fs=fs)

    defto_dict(self) -> dict:
        all_simple = (
            isinstance(self.docstore, SimpleDocumentStore)
            and isinstance(self.index_store, SimpleIndexStore)
            and isinstance(self.graph_store, SimpleGraphStore)
            and isinstance(
                self.property_graph_store, (SimplePropertyGraphStore, type(None))
            )
            and all(
                isinstance(vs, SimpleVectorStore) for vs in self.vector_stores.values()
            )
        )
        if not all_simple:
            raise ValueError(
                "to_dict only available when using simple doc/index/vector stores"
            )

        assert isinstance(self.docstore, SimpleDocumentStore)
        assert isinstance(self.index_store, SimpleIndexStore)
        assert isinstance(self.graph_store, SimpleGraphStore)
        assert isinstance(
            self.property_graph_store, (SimplePropertyGraphStore, type(None))
        )

        return {
            VECTOR_STORE_KEY: {
                key: vector_store.to_dict()
                for key, vector_store in self.vector_stores.items()
                if isinstance(vector_store, SimpleVectorStore)
            },
            DOC_STORE_KEY: self.docstore.to_dict(),
            INDEX_STORE_KEY: self.index_store.to_dict(),
            GRAPH_STORE_KEY: self.graph_store.to_dict(),
            PG_STORE_KEY: (
                self.property_graph_store.to_dict()
                if self.property_graph_store
                else None
            ),
        }

    @classmethod
    deffrom_dict(cls, save_dict: dict) -> "StorageContext":
"""Create a StorageContext from dict."""
        docstore = SimpleDocumentStore.from_dict(save_dict[DOC_STORE_KEY])
        index_store = SimpleIndexStore.from_dict(save_dict[INDEX_STORE_KEY])
        graph_store = SimpleGraphStore.from_dict(save_dict[GRAPH_STORE_KEY])
        property_graph_store = (
            SimplePropertyGraphStore.from_dict(save_dict[PG_STORE_KEY])
            if save_dict[PG_STORE_KEY]
            else None
        )

        vector_stores: Dict[str, BasePydanticVectorStore] = {}
        for key, vector_store_dict in save_dict[VECTOR_STORE_KEY].items():
            vector_stores[key] = SimpleVectorStore.from_dict(vector_store_dict)

        return cls(
            docstore=docstore,
            index_store=index_store,
            vector_stores=vector_stores,
            graph_store=graph_store,
            property_graph_store=property_graph_store,
        )

    @property
    defvector_store(self) -> BasePydanticVectorStore:
"""Backwrds compatibility for vector_store property."""
        return self.vector_stores[DEFAULT_VECTOR_STORE]

    defadd_vector_store(
        self, vector_store: BasePydanticVectorStore, namespace: str
    ) -> None:
"""Add a vector store to the storage context."""
        self.vector_stores[namespace] = vector_store

```
 |  
| --- | --- |  
###  vector_store `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.StorageContext.vector_store "Permanent link")

```
vector_store: 

```

Backwrds compatibility for vector_store property.
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.StorageContext.from_defaults "Permanent link")

```
from_defaults(
    docstore: Optional[] = None,
    index_store: Optional[] = None,
    vector_store: Optional[] = None,
    image_store: Optional[] = None,
    vector_stores: Optional[
        [, ]
    ] = None,
    graph_store: Optional[] = None,
    property_graph_store: Optional[
        
    ] = None,
    persist_dir: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
) -> 

```

Create a StorageContext from defaults.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `docstore`  |  `Optional[BaseDocumentStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/#llama_index.core.storage.docstore.types.BaseDocumentStore "BaseDocumentStore \(llama_index.core.storage.docstore.types.BaseDocumentStore\)")]`  |  document store  |  `None`  |  
|  `index_store`  |  `Optional[BaseIndexStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/#llama_index.core.storage.index_store.types.BaseIndexStore "BaseIndexStore \(llama_index.core.storage.index_store.types.BaseIndexStore\)")]`  |  index store  |  `None`  |  
|  `vector_store`  |  `Optional[BasePydanticVectorStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore "BasePydanticVectorStore \(llama_index.core.vector_stores.types.BasePydanticVectorStore\)")]`  |  vector store  |  `None`  |  
|  `graph_store`  |  `Optional[GraphStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/graph_stores/#llama_index.core.graph_stores.types.GraphStore "GraphStore \(llama_index.core.graph_stores.types.GraphStore\)")]`  |  graph store  |  `None`  |  
|  `image_store`  |  `Optional[BasePydanticVectorStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore "BasePydanticVectorStore \(llama_index.core.vector_stores.types.BasePydanticVectorStore\)")]`  |  image store  |  `None`  |  
Source code in `llama-index-core/llama_index/core/storage/storage_context.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    docstore: Optional[BaseDocumentStore] = None,
    index_store: Optional[BaseIndexStore] = None,
    vector_store: Optional[BasePydanticVectorStore] = None,
    image_store: Optional[BasePydanticVectorStore] = None,
    vector_stores: Optional[Dict[str, BasePydanticVectorStore]] = None,
    graph_store: Optional[GraphStore] = None,
    property_graph_store: Optional[PropertyGraphStore] = None,
    persist_dir: Optional[str] = None,
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> "StorageContext":
"""
    Create a StorageContext from defaults.

    Args:
        docstore (Optional[BaseDocumentStore]): document store
        index_store (Optional[BaseIndexStore]): index store
        vector_store (Optional[BasePydanticVectorStore]): vector store
        graph_store (Optional[GraphStore]): graph store
        image_store (Optional[BasePydanticVectorStore]): image store

    """
    if persist_dir is None:
        docstore = docstore or SimpleDocumentStore()
        index_store = index_store or SimpleIndexStore()
        graph_store = graph_store or SimpleGraphStore()
        image_store = image_store or SimpleVectorStore()

        if vector_store:
            vector_stores = {DEFAULT_VECTOR_STORE: vector_store}
        else:
            vector_stores = vector_stores or {
                DEFAULT_VECTOR_STORE: SimpleVectorStore()
            }
        if image_store:
            # append image store to vector stores
            vector_stores[IMAGE_VECTOR_STORE_NAMESPACE] = image_store
    else:
        docstore = docstore or SimpleDocumentStore.from_persist_dir(
            persist_dir, fs=fs
        )
        index_store = index_store or SimpleIndexStore.from_persist_dir(
            persist_dir, fs=fs
        )
        graph_store = graph_store or SimpleGraphStore.from_persist_dir(
            persist_dir, fs=fs
        )

        try:
            property_graph_store = (
                property_graph_store
                or SimplePropertyGraphStore.from_persist_dir(persist_dir, fs=fs)
            )
        except FileNotFoundError:
            property_graph_store = None

        if vector_store:
            vector_stores = {DEFAULT_VECTOR_STORE: vector_store}
        elif vector_stores:
            vector_stores = vector_stores
        else:
            vector_stores = SimpleVectorStore.from_namespaced_persist_dir(
                persist_dir, fs=fs
            )
        if image_store:
            # append image store to vector stores
            vector_stores[IMAGE_VECTOR_STORE_NAMESPACE] = image_store  # type: ignore

    return cls(
        docstore=docstore,
        index_store=index_store,
        vector_stores=vector_stores,  # type: ignore
        graph_store=graph_store,
        property_graph_store=property_graph_store,
    )

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.StorageContext.persist "Permanent link")

```
persist(
    persist_dir: Union[, PathLike] = DEFAULT_PERSIST_DIR,
    docstore_fname:  = DEFAULT_PERSIST_FNAME,
    index_store_fname:  = DEFAULT_PERSIST_FNAME,
    vector_store_fname:  = DEFAULT_PERSIST_FNAME,
    image_store_fname:  = IMAGE_STORE_FNAME,
    graph_store_fname:  = DEFAULT_PERSIST_FNAME,
    pg_graph_store_fname:  = DEFAULT_PG_PERSIST_FNAME,
    fs: Optional[AbstractFileSystem] = None,
) -> None

```

Persist the storage context.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `persist_dir`  |  directory to persist the storage context  |  `DEFAULT_PERSIST_DIR`  |  
Source code in `llama-index-core/llama_index/core/storage/storage_context.py`  
| 
```
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
```
 | 
```
defpersist(
    self,
    persist_dir: Union[str, os.PathLike] = DEFAULT_PERSIST_DIR,
    docstore_fname: str = DOCSTORE_FNAME,
    index_store_fname: str = INDEX_STORE_FNAME,
    vector_store_fname: str = VECTOR_STORE_FNAME,
    image_store_fname: str = IMAGE_STORE_FNAME,
    graph_store_fname: str = GRAPH_STORE_FNAME,
    pg_graph_store_fname: str = PG_FNAME,
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> None:
"""
    Persist the storage context.

    Args:
        persist_dir (str): directory to persist the storage context

    """
    if fs is not None:
        persist_dir = str(persist_dir)  # NOTE: doesn't support Windows here
        docstore_path = concat_dirs(persist_dir, docstore_fname)
        index_store_path = concat_dirs(persist_dir, index_store_fname)
        graph_store_path = concat_dirs(persist_dir, graph_store_fname)
        pg_graph_store_path = concat_dirs(persist_dir, pg_graph_store_fname)
    else:
        persist_dir = Path(persist_dir)
        docstore_path = str(persist_dir / docstore_fname)
        index_store_path = str(persist_dir / index_store_fname)
        graph_store_path = str(persist_dir / graph_store_fname)
        pg_graph_store_path = str(persist_dir / pg_graph_store_fname)

    self.docstore.persist(persist_path=docstore_path, fs=fs)
    self.index_store.persist(persist_path=index_store_path, fs=fs)
    self.graph_store.persist(persist_path=graph_store_path, fs=fs)

    if self.property_graph_store:
        self.property_graph_store.persist(persist_path=pg_graph_store_path, fs=fs)

    # save each vector store under it's namespace
    for vector_store_name, vector_store in self.vector_stores.items():
        if fs is not None:
            vector_store_path = concat_dirs(
                str(persist_dir),
                f"{vector_store_name}{NAMESPACE_SEP}{vector_store_fname}",
            )
        else:
            vector_store_path = str(
                Path(persist_dir)
                / f"{vector_store_name}{NAMESPACE_SEP}{vector_store_fname}"
            )

        vector_store.persist(persist_path=vector_store_path, fs=fs)

```
 |  
| --- | --- |  
###  from_dict `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.StorageContext.from_dict "Permanent link")

```
from_dict(save_dict: ) -> 

```

Create a StorageContext from dict.
Source code in `llama-index-core/llama_index/core/storage/storage_context.py`  
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
```
 | 
```
@classmethod
deffrom_dict(cls, save_dict: dict) -> "StorageContext":
"""Create a StorageContext from dict."""
    docstore = SimpleDocumentStore.from_dict(save_dict[DOC_STORE_KEY])
    index_store = SimpleIndexStore.from_dict(save_dict[INDEX_STORE_KEY])
    graph_store = SimpleGraphStore.from_dict(save_dict[GRAPH_STORE_KEY])
    property_graph_store = (
        SimplePropertyGraphStore.from_dict(save_dict[PG_STORE_KEY])
        if save_dict[PG_STORE_KEY]
        else None
    )

    vector_stores: Dict[str, BasePydanticVectorStore] = {}
    for key, vector_store_dict in save_dict[VECTOR_STORE_KEY].items():
        vector_stores[key] = SimpleVectorStore.from_dict(vector_store_dict)

    return cls(
        docstore=docstore,
        index_store=index_store,
        vector_stores=vector_stores,
        graph_store=graph_store,
        property_graph_store=property_graph_store,
    )

```
 |  
| --- | --- |  
###  add_vector_store [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.StorageContext.add_vector_store "Permanent link")

```
add_vector_store(
    vector_store: , namespace: 
) -> None

```

Add a vector store to the storage context.
Source code in `llama-index-core/llama_index/core/storage/storage_context.py`  
| 
```
273
274
275
276
277
```
 | 
```
defadd_vector_store(
    self, vector_store: BasePydanticVectorStore, namespace: str
) -> None:
"""Add a vector store to the storage context."""
    self.vector_stores[namespace] = vector_store

```
 |  
| --- | --- |  
##  SQLDatabase [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SQLDatabase "Permanent link")
SQL Database.
This class provides a wrapper around the SQLAlchemy engine to interact with a SQL database. It provides methods to execute SQL commands, insert data into tables, and retrieve information about the database schema. It also supports optional features such as including or excluding specific tables, sampling rows for table info, including indexes in table info, and supporting views.
Based on langchain SQLDatabase. https://github.com/langchain-ai/langchain/blob/e355606b1100097665207ca259de6dc548d44c78/libs/langchain/langchain/utilities/sql_database.py#L39
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `engine`  |  `Engine`  |  The SQLAlchemy engine instance to use for database operations.  |  _required_  |  
|  `schema`  |  `Optional[str]`  |  The name of the schema to use, if any.  |  `None`  |  
|  `metadata`  |  `Optional[MetaData]`  |  The metadata instance to use, if any.  |  `None`  |  
|  `ignore_tables`  |  `Optional[List[str]]`  |  List of table names to ignore. If set, include_tables must be None.  |  `None`  |  
|  `include_tables`  |  `Optional[List[str]]`  |  List of table names to include. If set, ignore_tables must be None.  |  `None`  |  
|  `sample_rows_in_table_info`  |  The number of sample rows to include in table info.  |  
|  `indexes_in_table_info`  |  `bool`  |  Whether to include indexes in table info.  |  `False`  |  
|  `custom_table_info`  |  `Optional[dict]`  |  Custom table info to use.  |  `None`  |  
|  `view_support`  |  `bool`  |  Whether to support views.  |  `False`  |  
|  `max_string_length`  |  The maximum string length to use.  |  `300`  |  
Source code in `llama-index-core/llama_index/core/utilities/sql_wrapper.py`  
| 
```
 11
 12
 13
 14
 15
 16
 17
 18
 19
 20
 21
 22
 23
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
```
 | 
```
classSQLDatabase:
"""
    SQL Database.

    This class provides a wrapper around the SQLAlchemy engine to interact with a SQL
    database.
    It provides methods to execute SQL commands, insert data into tables, and retrieve
    information about the database schema.
    It also supports optional features such as including or excluding specific tables,
    sampling rows for table info,
    including indexes in table info, and supporting views.

    Based on langchain SQLDatabase.
    https://github.com/langchain-ai/langchain/blob/e355606b1100097665207ca259de6dc548d44c78/libs/langchain/langchain/utilities/sql_database.py#L39

    Args:
        engine (Engine): The SQLAlchemy engine instance to use for database operations.
        schema (Optional[str]): The name of the schema to use, if any.
        metadata (Optional[MetaData]): The metadata instance to use, if any.
        ignore_tables (Optional[List[str]]): List of table names to ignore. If set,
            include_tables must be None.
        include_tables (Optional[List[str]]): List of table names to include. If set,
            ignore_tables must be None.
        sample_rows_in_table_info (int): The number of sample rows to include in table
            info.
        indexes_in_table_info (bool): Whether to include indexes in table info.
        custom_table_info (Optional[dict]): Custom table info to use.
        view_support (bool): Whether to support views.
        max_string_length (int): The maximum string length to use.

    """

    def__init__(
        self,
        engine: Engine,
        schema: Optional[str] = None,
        metadata: Optional[MetaData] = None,
        ignore_tables: Optional[List[str]] = None,
        include_tables: Optional[List[str]] = None,
        sample_rows_in_table_info: int = 3,
        indexes_in_table_info: bool = False,
        custom_table_info: Optional[dict] = None,
        view_support: bool = False,
        max_string_length: int = 300,
    ):
"""Create engine from database URI."""
        self._engine = engine
        self._schema = schema
        if include_tables and ignore_tables:
            raise ValueError("Cannot specify both include_tables and ignore_tables")

        self._inspector = inspect(self._engine)

        # including view support by adding the views as well as tables to the all
        # tables list if view_support is True
        self._all_tables = set(
            self._inspector.get_table_names(schema=schema)
            + (self._inspector.get_view_names(schema=schema) if view_support else [])
        )

        self._include_tables = set(include_tables) if include_tables else set()
        if self._include_tables:
            missing_tables = self._include_tables - self._all_tables
            if missing_tables:
                raise ValueError(
                    f"include_tables {missing_tables} not found in database"
                )
        self._ignore_tables = set(ignore_tables) if ignore_tables else set()
        if self._ignore_tables:
            missing_tables = self._ignore_tables - self._all_tables
            if missing_tables:
                raise ValueError(
                    f"ignore_tables {missing_tables} not found in database"
                )
        usable_tables = self.get_usable_table_names()
        self._usable_tables = set(usable_tables) if usable_tables else self._all_tables

        if not isinstance(sample_rows_in_table_info, int):
            raise TypeError("sample_rows_in_table_info must be an integer")

        self._sample_rows_in_table_info = sample_rows_in_table_info
        self._indexes_in_table_info = indexes_in_table_info

        self._custom_table_info = custom_table_info
        if self._custom_table_info:
            if not isinstance(self._custom_table_info, dict):
                raise TypeError(
                    "table_info must be a dictionary with table names as keys and the "
                    "desired table info as values"
                )
            # only keep the tables that are also present in the database
            intersection = set(self._custom_table_info).intersection(self._all_tables)
            self._custom_table_info = {
                table: info
                for table, info in self._custom_table_info.items()
                if table in intersection
            }

        self._max_string_length = max_string_length

        self._metadata = metadata or MetaData()
        # including view support if view_support = true
        self._metadata.reflect(
            views=view_support,
            bind=self._engine,
            only=list(self._usable_tables),
            schema=self._schema,
        )

    @property
    defengine(self) -> Engine:
"""Return SQL Alchemy engine."""
        return self._engine

    @property
    defmetadata_obj(self) -> MetaData:
"""Return SQL Alchemy metadata."""
        return self._metadata

    @classmethod
    deffrom_uri(
        cls, database_uri: str, engine_args: Optional[dict] = None, **kwargs: Any
    ) -> "SQLDatabase":
"""Construct a SQLAlchemy engine from URI."""
        _engine_args = engine_args or {}
        return cls(create_engine(database_uri, **_engine_args), **kwargs)

    @property
    defdialect(self) -> str:
"""Return string representation of dialect to use."""
        return self._engine.dialect.name

    defget_usable_table_names(self) -> Iterable[str]:
"""Get names of tables available."""
        if self._include_tables:
            return sorted(self._include_tables)
        return sorted(self._all_tables - self._ignore_tables)

    defget_table_columns(self, table_name: str) -> List[Any]:
"""Get table columns."""
        return self._inspector.get_columns(table_name)

    defget_single_table_info(self, table_name: str) -> str:
"""Get table info for a single table."""
        # same logic as table_info, but with specific table names
        template = "Table '{table_name}' has columns: {columns}, "
        try:
            # try to retrieve table comment
            table_comment = self._inspector.get_table_comment(
                table_name, schema=self._schema
            )["text"]
            if table_comment:
                template += f"with comment: ({table_comment}) "
        except NotImplementedError:
            # get_table_comment raises NotImplementedError for a dialect that does not support comments.
            pass

        template += "{foreign_keys}."
        columns = []
        for column in self._inspector.get_columns(table_name, schema=self._schema):
            if column.get("comment"):
                columns.append(
                    f"{column['name']} ({column['type']!s}): '{column.get('comment')}'"
                )
            else:
                columns.append(f"{column['name']} ({column['type']!s})")

        column_str = ", ".join(columns)
        foreign_keys = []
        for foreign_key in self._inspector.get_foreign_keys(
            table_name, schema=self._schema
        ):
            foreign_keys.append(
                f"{foreign_key['constrained_columns']} -> "
                f"{foreign_key['referred_table']}.{foreign_key['referred_columns']}"
            )
        foreign_key_str = (
            foreign_keys
            and " and foreign keys: {}".format(", ".join(foreign_keys))
            or ""
        )
        return template.format(
            table_name=table_name, columns=column_str, foreign_keys=foreign_key_str
        )

    definsert_into_table(self, table_name: str, data: dict) -> None:
"""Insert data into a table."""
        table = self._metadata.tables[table_name]
        stmt = insert(table).values(**data)
        with self._engine.begin() as connection:
            connection.execute(stmt)

    deftruncate_word(self, content: Any, *, length: int, suffix: str = "...") -> str:
"""
        Truncate a string to a certain number of words, based on the max string
        length.
        """
        if not isinstance(content, str) or length <= 0:
            return content

        if len(content) <= length:
            return content

        return content[: length - len(suffix)].rsplit(" ", 1)[0] + suffix

    def_add_schema_prefix(self, command: str) -> str:
"""
        Add schema prefix to table names in FROM/JOIN clauses.

        Preserves CTE (Common Table Expression) names and already
        schema-qualified identifiers so they are not double-prefixed.
        """
        # Collect CTE names defined in WITH clauses
        cte_names: Set[str] = set()
        # First CTE: WITH [RECURSIVE] name AS (
        for m in re.finditer(
            r"\bWITH\s+(?:RECURSIVE\s+)?(\w+)\s+AS\s*\(", command, re.IGNORECASE
        ):
            cte_names.add(m.group(1).lower())
        # Subsequent CTEs: ), name AS (
        for m in re.finditer(r"\)\s*,\s*(\w+)\s+AS\s*\(", command, re.IGNORECASE):
            cte_names.add(m.group(1).lower())

        def_replace(match: re.Match) -> str:
            keyword = match.group(1)
            table_ref = match.group(2)
            # Skip CTE references and already schema-qualified names
            if table_ref.lower() in cte_names or "." in table_ref:
                return match.group(0)
            return f"{keyword}{self._schema}.{table_ref}"

        return re.sub(
            r"\b((?:FROM|JOIN)\s+)(\w+(?:\.\w+)?)",
            _replace,
            command,
            flags=re.IGNORECASE,
        )

    defrun_sql(self, command: str) -> Tuple[str, Dict]:
"""
        Execute a SQL statement and return a string representing the results.

        If the statement returns rows, a string of the results is returned.
        If the statement returns no rows, an empty string is returned.
        """
        with self._engine.begin() as connection:
            try:
                if self._schema:
                    command = self._add_schema_prefix(command)
                cursor = connection.execute(text(command))
            except (ProgrammingError, OperationalError) as exc:
                raise NotImplementedError(
                    f"Statement {command!r} is invalid SQL.\nError: {exc.orig}"
                ) fromexc
            if cursor.returns_rows:
                result = cursor.fetchall()
                # truncate the results to the max string length
                # we can't use str(result) directly because it automatically truncates long strings
                truncated_results = []
                for row in result:
                    # truncate each column, then convert the row to a tuple
                    truncated_row = tuple(
                        self.truncate_word(column, length=self._max_string_length)
                        for column in row
                    )
                    truncated_results.append(truncated_row)
                return str(truncated_results), {
                    "result": truncated_results,
                    "col_keys": list(cursor.keys()),
                }
        return "", {}

```
 |  
| --- | --- |  
###  engine `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SQLDatabase.engine "Permanent link")

```
engine: Engine

```

Return SQL Alchemy engine.
###  metadata_obj `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SQLDatabase.metadata_obj "Permanent link")

```
metadata_obj: MetaData

```

Return SQL Alchemy metadata.
###  dialect `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SQLDatabase.dialect "Permanent link")

```
dialect: 

```

Return string representation of dialect to use.
###  from_uri `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SQLDatabase.from_uri "Permanent link")

```
from_uri(
    database_uri: ,
    engine_args: Optional[] = None,
    **kwargs: 
) -> 

```

Construct a SQLAlchemy engine from URI.
Source code in `llama-index-core/llama_index/core/utilities/sql_wrapper.py`  
| 
```
130
131
132
133
134
135
136
```
 | 
```
@classmethod
deffrom_uri(
    cls, database_uri: str, engine_args: Optional[dict] = None, **kwargs: Any
) -> "SQLDatabase":
"""Construct a SQLAlchemy engine from URI."""
    _engine_args = engine_args or {}
    return cls(create_engine(database_uri, **_engine_args), **kwargs)

```
 |  
| --- | --- |  
###  get_usable_table_names [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SQLDatabase.get_usable_table_names "Permanent link")

```
get_usable_table_names() -> Iterable[]

```

Get names of tables available.
Source code in `llama-index-core/llama_index/core/utilities/sql_wrapper.py`  
| 
```
143
144
145
146
147
```
 | 
```
defget_usable_table_names(self) -> Iterable[str]:
"""Get names of tables available."""
    if self._include_tables:
        return sorted(self._include_tables)
    return sorted(self._all_tables - self._ignore_tables)

```
 |  
| --- | --- |  
###  get_table_columns [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SQLDatabase.get_table_columns "Permanent link")

```
get_table_columns(table_name: ) -> []

```

Get table columns.
Source code in `llama-index-core/llama_index/core/utilities/sql_wrapper.py`  
| 
```
149
150
151
```
 | 
```
defget_table_columns(self, table_name: str) -> List[Any]:
"""Get table columns."""
    return self._inspector.get_columns(table_name)

```
 |  
| --- | --- |  
###  get_single_table_info [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SQLDatabase.get_single_table_info "Permanent link")

```
get_single_table_info(table_name: ) -> 

```

Get table info for a single table.
Source code in `llama-index-core/llama_index/core/utilities/sql_wrapper.py`  
| 
```
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
```
 | 
```
defget_single_table_info(self, table_name: str) -> str:
"""Get table info for a single table."""
    # same logic as table_info, but with specific table names
    template = "Table '{table_name}' has columns: {columns}, "
    try:
        # try to retrieve table comment
        table_comment = self._inspector.get_table_comment(
            table_name, schema=self._schema
        )["text"]
        if table_comment:
            template += f"with comment: ({table_comment}) "
    except NotImplementedError:
        # get_table_comment raises NotImplementedError for a dialect that does not support comments.
        pass

    template += "{foreign_keys}."
    columns = []
    for column in self._inspector.get_columns(table_name, schema=self._schema):
        if column.get("comment"):
            columns.append(
                f"{column['name']} ({column['type']!s}): '{column.get('comment')}'"
            )
        else:
            columns.append(f"{column['name']} ({column['type']!s})")

    column_str = ", ".join(columns)
    foreign_keys = []
    for foreign_key in self._inspector.get_foreign_keys(
        table_name, schema=self._schema
    ):
        foreign_keys.append(
            f"{foreign_key['constrained_columns']} -> "
            f"{foreign_key['referred_table']}.{foreign_key['referred_columns']}"
        )
    foreign_key_str = (
        foreign_keys
        and " and foreign keys: {}".format(", ".join(foreign_keys))
        or ""
    )
    return template.format(
        table_name=table_name, columns=column_str, foreign_keys=foreign_key_str
    )

```
 |  
| --- | --- |  
###  insert_into_table [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SQLDatabase.insert_into_table "Permanent link")

```
insert_into_table(table_name: , data: ) -> None

```

Insert data into a table.
Source code in `llama-index-core/llama_index/core/utilities/sql_wrapper.py`  
| 
```
196
197
198
199
200
201
```
 | 
```
definsert_into_table(self, table_name: str, data: dict) -> None:
"""Insert data into a table."""
    table = self._metadata.tables[table_name]
    stmt = insert(table).values(**data)
    with self._engine.begin() as connection:
        connection.execute(stmt)

```
 |  
| --- | --- |  
###  truncate_word [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SQLDatabase.truncate_word "Permanent link")

```
truncate_word(
    content: , *, length: , suffix:  = "..."
) -> 

```

Truncate a string to a certain number of words, based on the max string length.
Source code in `llama-index-core/llama_index/core/utilities/sql_wrapper.py`  
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
```
 | 
```
deftruncate_word(self, content: Any, *, length: int, suffix: str = "...") -> str:
"""
    Truncate a string to a certain number of words, based on the max string
    length.
    """
    if not isinstance(content, str) or length <= 0:
        return content

    if len(content) <= length:
        return content

    return content[: length - len(suffix)].rsplit(" ", 1)[0] + suffix

```
 |  
| --- | --- |  
###  run_sql [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.SQLDatabase.run_sql "Permanent link")

```
run_sql(command: ) -> Tuple[, ]

```

Execute a SQL statement and return a string representing the results.
If the statement returns rows, a string of the results is returned. If the statement returns no rows, an empty string is returned.
Source code in `llama-index-core/llama_index/core/utilities/sql_wrapper.py`  
| 
```
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
```
 | 
```
defrun_sql(self, command: str) -> Tuple[str, Dict]:
"""
    Execute a SQL statement and return a string representing the results.

    If the statement returns rows, a string of the results is returned.
    If the statement returns no rows, an empty string is returned.
    """
    with self._engine.begin() as connection:
        try:
            if self._schema:
                command = self._add_schema_prefix(command)
            cursor = connection.execute(text(command))
        except (ProgrammingError, OperationalError) as exc:
            raise NotImplementedError(
                f"Statement {command!r} is invalid SQL.\nError: {exc.orig}"
            ) fromexc
        if cursor.returns_rows:
            result = cursor.fetchall()
            # truncate the results to the max string length
            # we can't use str(result) directly because it automatically truncates long strings
            truncated_results = []
            for row in result:
                # truncate each column, then convert the row to a tuple
                truncated_row = tuple(
                    self.truncate_word(column, length=self._max_string_length)
                    for column in row
                )
                truncated_results.append(truncated_row)
            return str(truncated_results), {
                "result": truncated_results,
                "col_keys": list(cursor.keys()),
            }
    return "", {}

```
 |  
| --- | --- |  
##  set_global_handler [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.set_global_handler "Permanent link")

```
set_global_handler(
    eval_mode: , **eval_params: 
) -> None

```

Set global eval handlers.
Source code in `llama-index-core/llama_index/core/callbacks/global_handlers.py`  
| 
```
 6
 7
 8
 9
10
11
12
```
 | 
```
defset_global_handler(eval_mode: str, **eval_params: Any) -> None:
"""Set global eval handlers."""
    importllama_index.core

    handler = create_global_handler(eval_mode, **eval_params)
    if handler:
        llama_index.core.global_handler = handler

```
 |  
| --- | --- |  
##  load_graph_from_storage [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.load_graph_from_storage "Permanent link")

```
load_graph_from_storage(
    storage_context: ,
    root_id: ,
    **kwargs: 
) -> 

```

Load composable graph from storage context.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `storage_context`  |   |  storage context containing docstore, index store and vector store.  |  _required_  |  
|  `root_id`  |  ID of the root index of the graph.  |  _required_  |  
|  `**kwargs`  |  Additional keyword args to pass to the index constructors.  |  
Source code in `llama-index-core/llama_index/core/indices/loading.py`  
| 
```
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
```
 | 
```
defload_graph_from_storage(
    storage_context: StorageContext,
    root_id: str,
    **kwargs: Any,
) -> ComposableGraph:
"""
    Load composable graph from storage context.

    Args:
        storage_context (StorageContext): storage context containing
            docstore, index store and vector store.
        root_id (str): ID of the root index of the graph.
        **kwargs: Additional keyword args to pass to the index constructors.

    """
    indices = load_indices_from_storage(storage_context, index_ids=None, **kwargs)
    all_indices = {index.index_id: index for index in indices}
    return ComposableGraph(all_indices=all_indices, root_id=root_id)

```
 |  
| --- | --- |  
##  load_index_from_storage [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.load_index_from_storage "Permanent link")

```
load_index_from_storage(
    storage_context: ,
    index_id: Optional[] = None,
    **kwargs: 
) -> 

```

Load index from storage context.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `storage_context`  |   |  storage context containing docstore, index store and vector store.  |  _required_  |  
|  `index_id`  |  `Optional[str]`  |  ID of the index to load. Defaults to None, which assumes there's only a single index in the index store and load it.  |  `None`  |  
|  `**kwargs`  |  Additional keyword args to pass to the index constructors.  |  
Source code in `llama-index-core/llama_index/core/indices/loading.py`  
| 
```
12
13
14
15
16
17
18
19
20
21
22
23
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
```
 | 
```
defload_index_from_storage(
    storage_context: StorageContext,
    index_id: Optional[str] = None,
    **kwargs: Any,
) -> BaseIndex:
"""
    Load index from storage context.

    Args:
        storage_context (StorageContext): storage context containing
            docstore, index store and vector store.
        index_id (Optional[str]): ID of the index to load.
            Defaults to None, which assumes there's only a single index
            in the index store and load it.
        **kwargs: Additional keyword args to pass to the index constructors.

    """
    index_ids: Optional[Sequence[str]]
    if index_id is None:
        index_ids = None
    else:
        index_ids = [index_id]

    indices = load_indices_from_storage(storage_context, index_ids=index_ids, **kwargs)

    if len(indices) == 0:
        raise ValueError(
            "No index in storage context, check if you specified the right persist_dir."
        )
    elif len(indices)  1:
        raise ValueError(
            f"Expected to load a single index, but got {len(indices)} instead. "
            "Please specify index_id."
        )

    return indices[0]

```
 |  
| --- | --- |  
##  load_indices_from_storage [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.load_indices_from_storage "Permanent link")

```
load_indices_from_storage(
    storage_context: ,
    index_ids: Optional[Sequence[]] = None,
    **kwargs: 
) -> []

```

Load multiple indices from storage context.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `storage_context`  |   |  storage context containing docstore, index store and vector store.  |  _required_  |  
|  `index_id`  |  `Optional[Sequence[str]]`  |  IDs of the indices to load. Defaults to None, which loads all indices in the index store.  |  _required_  |  
|  `**kwargs`  |  Additional keyword args to pass to the index constructors.  |  
Source code in `llama-index-core/llama_index/core/indices/loading.py`  
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
```
 | 
```
defload_indices_from_storage(
    storage_context: StorageContext,
    index_ids: Optional[Sequence[str]] = None,
    **kwargs: Any,
) -> List[BaseIndex]:
"""
    Load multiple indices from storage context.

    Args:
        storage_context (StorageContext): storage context containing
            docstore, index store and vector store.
        index_id (Optional[Sequence[str]]): IDs of the indices to load.
            Defaults to None, which loads all indices in the index store.
        **kwargs: Additional keyword args to pass to the index constructors.

    """
    if index_ids is None:
        logger.info("Loading all indices.")
        index_structs = storage_context.index_store.index_structs()
    else:
        logger.info(f"Loading indices with ids: {index_ids}")
        index_structs = []
        for index_id in index_ids:
            index_struct = storage_context.index_store.get_index_struct(index_id)
            if index_struct is None:
                raise ValueError(f"Failed to load index with ID {index_id}")
            index_structs.append(index_struct)

    indices = []
    for index_struct in index_structs:
        type_ = index_struct.get_type()
        index_cls = INDEX_STRUCT_TYPE_TO_INDEX_CLASS[type_]
        index = index_cls(
            index_struct=index_struct, storage_context=storage_context, **kwargs
        )
        indices.append(index)
    return indices

```
 |  
| --- | --- |  
##  download_loader [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.download_loader "Permanent link")

```
download_loader(
    loader_class: ,
    loader_hub_url:  = "",
    refresh_cache:  = False,
    use_gpt_index_import:  = False,
    custom_path: Optional[] = None,
) -> []

```

Download a single loader from the Loader Hub.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `loader_class`  |  The name of the loader class you want to download, such as `SimpleWebPageReader`.  |  _required_  |  
|  `refresh_cache`  |  `bool`  |  If true, the local cache will be skipped and the loader will be fetched directly from the remote repo.  |  `False`  |  
|  `use_gpt_index_import`  |  `bool`  |  If true, the loader files will use llama_index as the base dependency. By default (False), the loader files use llama_index as the base dependency. NOTE: this is a temporary workaround while we fully migrate all usages to llama_index.  |  `False`  |  
|  `custom_path`  |  `Optional[str]`  |  Custom dirpath to download loader into.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Type[BaseReader[](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.BaseReader "BaseReader \(llama_index.core.readers.base.BaseReader\)")]`  |  A Loader.  |  
Source code in `llama-index-core/llama_index/core/readers/download.py`  
| 
```
19
20
21
22
23
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
```
 | 
```
@deprecated(
    "`download_loader()` is deprecated. "
    "Please install tool using pip install directly instead."
)
defdownload_loader(
    loader_class: str,
    loader_hub_url: str = "",
    refresh_cache: bool = False,
    use_gpt_index_import: bool = False,
    custom_path: Optional[str] = None,
) -> Type[BaseReader]:  # pragma: no cover
"""
    Download a single loader from the Loader Hub.

    Args:
        loader_class: The name of the loader class you want to download,
            such as `SimpleWebPageReader`.
        refresh_cache: If true, the local cache will be skipped and the
            loader will be fetched directly from the remote repo.
        use_gpt_index_import: If true, the loader files will use
            llama_index as the base dependency. By default (False),
            the loader files use llama_index as the base dependency.
            NOTE: this is a temporary workaround while we fully migrate all usages
            to llama_index.
        custom_path: Custom dirpath to download loader into.

    Returns:
        A Loader.

    """
    # maintain during deprecation period
    del loader_hub_url
    del refresh_cache
    del use_gpt_index_import
    del custom_path

    mappings_path = os.path.join(
        os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
        ),
        "command_line/mappings.json",
    )
    with open(mappings_path) as f:
        mappings = json.load(f)

    if loader_class in mappings:
        new_import_parent = mappings[loader_class]
        new_install_parent = new_import_parent.replace(".", "-").replace("_", "-")
    else:
        raise ValueError(f"Failed to find python package for class {loader_class}")

    reader_cls = download_integration(
        module_str=new_install_parent,
        module_import_str=new_import_parent,
        cls_name=loader_class,
    )
    if not issubclass(reader_cls, BaseReader):
        raise ValueError(
            f"Loader class {loader_class} must be a subclass of BaseReader."
        )

    return reader_cls

```
 |  
| --- | --- |  
##  get_response_synthesizer [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.get_response_synthesizer "Permanent link")

```
get_response_synthesizer(
    llm: Optional[] = None,
    prompt_helper: Optional[] = None,
    text_qa_template: Optional[] = None,
    refine_template: Optional[] = None,
    summary_template: Optional[] = None,
    simple_template: Optional[] = None,
    response_mode:  = ,
    callback_manager: Optional[] = None,
    use_async:  = False,
    streaming:  = False,
    structured_answer_filtering:  = False,
    output_cls: Optional[[BaseModel]] = None,
    program_factory: Optional[
        Callable[[], ]
    ] = None,
    verbose:  = False,
) -> 

```

Get a response synthesizer.
Source code in `llama-index-core/llama_index/core/response_synthesizers/factory.py`  
| 
```
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
```
 | 
```
defget_response_synthesizer(
    llm: Optional[LLM] = None,
    prompt_helper: Optional[PromptHelper] = None,
    text_qa_template: Optional[BasePromptTemplate] = None,
    refine_template: Optional[BasePromptTemplate] = None,
    summary_template: Optional[BasePromptTemplate] = None,
    simple_template: Optional[BasePromptTemplate] = None,
    response_mode: ResponseMode = ResponseMode.COMPACT,
    callback_manager: Optional[CallbackManager] = None,
    use_async: bool = False,
    streaming: bool = False,
    structured_answer_filtering: bool = False,
    output_cls: Optional[Type[BaseModel]] = None,
    program_factory: Optional[
        Callable[[BasePromptTemplate], BasePydanticProgram]
    ] = None,
    verbose: bool = False,
) -> BaseSynthesizer:
"""Get a response synthesizer."""
    text_qa_template = text_qa_template or DEFAULT_TEXT_QA_PROMPT_SEL
    refine_template = refine_template or DEFAULT_REFINE_PROMPT_SEL
    simple_template = simple_template or DEFAULT_SIMPLE_INPUT_PROMPT
    summary_template = summary_template or DEFAULT_TREE_SUMMARIZE_PROMPT_SEL

    callback_manager = callback_manager or Settings.callback_manager
    llm = llm or Settings.llm
    prompt_helper = (
        prompt_helper
        or Settings._prompt_helper
        or PromptHelper.from_llm_metadata(
            llm.metadata,
        )
    )

    if response_mode == ResponseMode.REFINE:
        return Refine(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            text_qa_template=text_qa_template,
            refine_template=refine_template,
            output_cls=output_cls,
            streaming=streaming,
            structured_answer_filtering=structured_answer_filtering,
            program_factory=program_factory,
            verbose=verbose,
        )
    elif response_mode == ResponseMode.COMPACT:
        return CompactAndRefine(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            text_qa_template=text_qa_template,
            refine_template=refine_template,
            output_cls=output_cls,
            streaming=streaming,
            structured_answer_filtering=structured_answer_filtering,
            program_factory=program_factory,
            verbose=verbose,
        )
    elif response_mode == ResponseMode.TREE_SUMMARIZE:
        return TreeSummarize(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            summary_template=summary_template,
            output_cls=output_cls,
            streaming=streaming,
            use_async=use_async,
            verbose=verbose,
        )
    elif response_mode == ResponseMode.SIMPLE_SUMMARIZE:
        return SimpleSummarize(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            text_qa_template=text_qa_template,
            streaming=streaming,
        )
    elif response_mode == ResponseMode.GENERATION:
        return Generation(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            simple_template=simple_template,
            streaming=streaming,
        )
    elif response_mode == ResponseMode.ACCUMULATE:
        return Accumulate(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            text_qa_template=text_qa_template,
            output_cls=output_cls,
            streaming=streaming,
            use_async=use_async,
        )
    elif response_mode == ResponseMode.COMPACT_ACCUMULATE:
        return CompactAndAccumulate(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            text_qa_template=text_qa_template,
            output_cls=output_cls,
            streaming=streaming,
            use_async=use_async,
        )
    elif response_mode == ResponseMode.NO_TEXT:
        return NoText(
            callback_manager=callback_manager,
            streaming=streaming,
        )
    elif response_mode == ResponseMode.CONTEXT_ONLY:
        return ContextOnly(
            callback_manager=callback_manager,
            streaming=streaming,
        )
    else:
        raise ValueError(f"Unknown mode: {response_mode}")

```
 |  
| --- | --- |  
##  set_global_service_context [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.set_global_service_context "Permanent link")

```
set_global_service_context(
    service_context: Optional[],
) -> None

```

Helper function to set the global service context.
Source code in `llama-index-core/llama_index/core/service_context.py`  
| 
```
41
42
43
44
45
46
47
48
```
 | 
```
defset_global_service_context(service_context: Optional[ServiceContext]) -> None:
"""Helper function to set the global service context."""
    raise ValueError(
        "ServiceContext is deprecated. Use llama_index.settings.Settings instead, "
        "or pass in modules to local functions/methods/interfaces.\n"
        "See the docs for updated usage/migration: \n"
        "https://docs.llamaindex.ai/en/stable/module_guides/supporting_modules/service_context_migration/"
    )

```
 |  
| --- | --- |  
options: members: - load_index_from_storage - load_indices_from_storage
