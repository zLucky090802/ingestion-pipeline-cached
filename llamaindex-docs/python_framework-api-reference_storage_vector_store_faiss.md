# Faiss
##  FaissVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/faiss/#llama_index.vector_stores.faiss.FaissVectorStore "Permanent link")
Bases: 
Faiss Vector Store.
Embeddings are stored within a Faiss index.
During query time, the index uses Faiss to query for the top k embeddings, and returns the corresponding indices.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `faiss_index`  |  `Index`  |  Faiss index instance  |  _required_  |  
Examples:
`pip install llama-index-vector-stores-faiss faiss-cpu`

```
fromllama_index.vector_stores.faissimport FaissVectorStore
importfaiss

# create a faiss index
d = 1536  # dimension
faiss_index = faiss.IndexFlatL2(d)

vector_store = FaissVectorStore(faiss_index=faiss_index)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-faiss/llama_index/vector_stores/faiss/base.py`  
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
```
 | 
```
classFaissVectorStore(BasePydanticVectorStore):
"""
    Faiss Vector Store.

    Embeddings are stored within a Faiss index.

    During query time, the index uses Faiss to query for the top
    k embeddings, and returns the corresponding indices.

    Args:
        faiss_index (faiss.Index): Faiss index instance

    Examples:
        `pip install llama-index-vector-stores-faiss faiss-cpu`

        ```python
        from llama_index.vector_stores.faiss import FaissVectorStore
        import faiss

        # create a faiss index
        d = 1536  # dimension
        faiss_index = faiss.IndexFlatL2(d)

        vector_store = FaissVectorStore(faiss_index=faiss_index)
        ```

    """

    stores_text: bool = False

    _faiss_index = PrivateAttr()

    def__init__(
        self,
        faiss_index: Any,
    ) -> None:
"""Initialize params."""
        import_err_msg = """
            `faiss` package not found. For instructions on
            how to install `faiss` please visit
            https://github.com/facebookresearch/faiss/wiki/Installing-Faiss
        """
        try:
            importfaiss
        except ImportError:
            raise ImportError(import_err_msg)

        super().__init__()

        self._faiss_index = cast(faiss.Index, faiss_index)

    @classmethod
    deffrom_persist_dir(
        cls,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> "FaissVectorStore":
        persist_path = os.path.join(
            persist_dir,
            f"{DEFAULT_VECTOR_STORE}{NAMESPACE_SEP}{DEFAULT_PERSIST_FNAME}",
        )
        # only support local storage for now
        if fs and not isinstance(fs, LocalFileSystem):
            raise NotImplementedError("FAISS only supports local storage for now.")
        return cls.from_persist_path(persist_path=persist_path, fs=None)

    @classmethod
    deffrom_persist_path(
        cls,
        persist_path: str,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> "FaissVectorStore":
        importfaiss

        # I don't think FAISS supports fsspec, it requires a path in the SWIG interface
        # TODO: copy to a temp file and load into memory from there
        if fs and not isinstance(fs, LocalFileSystem):
            raise NotImplementedError("FAISS only supports local storage for now.")

        if not os.path.exists(persist_path):
            raise ValueError(f"No existing {__name__} found at {persist_path}.")

        logger.info(f"Loading {__name__} from {persist_path}.")
        faiss_index = faiss.read_index(persist_path)
        return cls(faiss_index=faiss_index)

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to index.

        NOTE: in the Faiss vector store, we do not store text in Faiss.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        """
        new_ids = []
        for node in nodes:
            text_embedding = node.get_embedding()
            text_embedding_np = np.array(text_embedding, dtype="float32")[np.newaxis, :]
            new_id = str(self._faiss_index.ntotal)
            self._faiss_index.add(text_embedding_np)
            new_ids.append(new_id)
        return new_ids

    @property
    defclient(self) -> Any:
"""Return the faiss index."""
        return self._faiss_index

    defpersist(
        self,
        persist_path: str = DEFAULT_PERSIST_PATH,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> None:
"""
        Save to file.

        This method saves the vector store to disk.

        Args:
            persist_path (str): The save_path of the file.

        """
        # I don't think FAISS supports fsspec, it requires a path in the SWIG interface
        # TODO: write to a temporary file and then copy to the final destination
        if fs and not isinstance(fs, LocalFileSystem):
            raise NotImplementedError("FAISS only supports local storage for now.")
        importfaiss

        dirpath = os.path.dirname(persist_path)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        faiss.write_index(self._faiss_index, persist_path)

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        raise NotImplementedError("Delete not yet implemented for Faiss index.")

    defquery(
        self,
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query_embedding (List[float]): query embedding
            similarity_top_k (int): top k most similar nodes

        """
        if query.filters is not None:
            raise ValueError("Metadata filters not implemented for Faiss yet.")

        query_embedding = cast(List[float], query.query_embedding)
        query_embedding_np = np.array(query_embedding, dtype="float32")[np.newaxis, :]
        dists, indices = self._faiss_index.search(
            query_embedding_np, query.similarity_top_k
        )
        dists = list(dists[0])
        # if empty, then return an empty response
        if len(indices) == 0:
            return VectorStoreQueryResult(similarities=[], ids=[])

        # returned dimension is 1 x k
        node_idxs = indices[0]

        filtered_dists = []
        filtered_node_idxs = []
        for dist, idx in zip(dists, node_idxs):
            if idx  0:
                continue
            filtered_dists.append(dist)
            filtered_node_idxs.append(str(idx))

        return VectorStoreQueryResult(
            similarities=filtered_dists, ids=filtered_node_idxs
        )

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/faiss/#llama_index.vector_stores.faiss.FaissVectorStore.client "Permanent link")

```
client: 

```

Return the faiss index.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/faiss/#llama_index.vector_stores.faiss.FaissVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
NOTE: in the Faiss vector store, we do not store text in Faiss.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-faiss/llama_index/vector_stores/faiss/base.py`  
| 
```
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

    NOTE: in the Faiss vector store, we do not store text in Faiss.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings

    """
    new_ids = []
    for node in nodes:
        text_embedding = node.get_embedding()
        text_embedding_np = np.array(text_embedding, dtype="float32")[np.newaxis, :]
        new_id = str(self._faiss_index.ntotal)
        self._faiss_index.add(text_embedding_np)
        new_ids.append(new_id)
    return new_ids

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/faiss/#llama_index.vector_stores.faiss.FaissVectorStore.persist "Permanent link")

```
persist(
    persist_path:  = DEFAULT_PERSIST_PATH,
    fs: Optional[AbstractFileSystem] = None,
) -> None

```

Save to file.
This method saves the vector store to disk.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `persist_path`  |  The save_path of the file.  |  `DEFAULT_PERSIST_PATH`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-faiss/llama_index/vector_stores/faiss/base.py`  
| 
```
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
```
 | 
```
defpersist(
    self,
    persist_path: str = DEFAULT_PERSIST_PATH,
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> None:
"""
    Save to file.

    This method saves the vector store to disk.

    Args:
        persist_path (str): The save_path of the file.

    """
    # I don't think FAISS supports fsspec, it requires a path in the SWIG interface
    # TODO: write to a temporary file and then copy to the final destination
    if fs and not isinstance(fs, LocalFileSystem):
        raise NotImplementedError("FAISS only supports local storage for now.")
    importfaiss

    dirpath = os.path.dirname(persist_path)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    faiss.write_index(self._faiss_index, persist_path)

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/faiss/#llama_index.vector_stores.faiss.FaissVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-faiss/llama_index/vector_stores/faiss/base.py`  
| 
```
173
174
175
176
177
178
179
180
181
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    raise NotImplementedError("Delete not yet implemented for Faiss index.")

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/faiss/#llama_index.vector_stores.faiss.FaissVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_embedding`  |  `List[float]`  |  query embedding  |  _required_  |  
|  `similarity_top_k`  |  top k most similar nodes  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-faiss/llama_index/vector_stores/faiss/base.py`  
| 
```
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
        query_embedding (List[float]): query embedding
        similarity_top_k (int): top k most similar nodes

    """
    if query.filters is not None:
        raise ValueError("Metadata filters not implemented for Faiss yet.")

    query_embedding = cast(List[float], query.query_embedding)
    query_embedding_np = np.array(query_embedding, dtype="float32")[np.newaxis, :]
    dists, indices = self._faiss_index.search(
        query_embedding_np, query.similarity_top_k
    )
    dists = list(dists[0])
    # if empty, then return an empty response
    if len(indices) == 0:
        return VectorStoreQueryResult(similarities=[], ids=[])

    # returned dimension is 1 x k
    node_idxs = indices[0]

    filtered_dists = []
    filtered_node_idxs = []
    for dist, idx in zip(dists, node_idxs):
        if idx  0:
            continue
        filtered_dists.append(dist)
        filtered_node_idxs.append(str(idx))

    return VectorStoreQueryResult(
        similarities=filtered_dists, ids=filtered_node_idxs
    )

```
 |  
| --- | --- |  
##  FaissMapVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/faiss/#llama_index.vector_stores.faiss.FaissMapVectorStore "Permanent link")
Bases: 
Faiss Map Vector Store.
This wraps the base Faiss vector store and adds handling for the Faiss IDMap and IDMap2 indexes. This allows for update/delete functionality through node_id and faiss_id mapping.
Embeddings are stored within a Faiss index.
During query time, the index uses Faiss to query for the top k embeddings, and returns the corresponding indices.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `faiss_index`  |  `IndexIDMap or IndexIDMap2`  |  Faiss id map index instance  |  _required_  |  
Examples:
`pip install llama-index-vector-stores-faiss faiss-cpu`

```
fromllama_index.vector_stores.faissimport FaissMapVectorStore
importfaiss

# create a faiss index
d = 1536  # dimension
faiss_index = faiss.IndexFlatL2(d)

# wrap it in an IDMap or IDMap2
id_map_index = faiss.IndexIDMap2(faiss_index)

vector_store = FaissMapVectorStore(faiss_index=id_map_index)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-faiss/llama_index/vector_stores/faiss/map_store.py`  
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
```
 | 
```
classFaissMapVectorStore(FaissVectorStore):
"""
    Faiss Map Vector Store.

    This wraps the base Faiss vector store and adds handling for
    the Faiss IDMap and IDMap2 indexes. This allows for
    update/delete functionality through node_id and faiss_id mapping.

    Embeddings are stored within a Faiss index.

    During query time, the index uses Faiss to query for the top
    k embeddings, and returns the corresponding indices.

    Args:
        faiss_index (faiss.IndexIDMap or faiss.IndexIDMap2): Faiss id map index instance

    Examples:
        `pip install llama-index-vector-stores-faiss faiss-cpu`

        ```python
        from llama_index.vector_stores.faiss import FaissMapVectorStore
        import faiss

        # create a faiss index
        d = 1536  # dimension
        faiss_index = faiss.IndexFlatL2(d)

        # wrap it in an IDMap or IDMap2
        id_map_index = faiss.IndexIDMap2(faiss_index)

        vector_store = FaissMapVectorStore(faiss_index=id_map_index)
        ```

    """

    # _node_id_to_faiss_id_map is used to map the node id to the faiss id
    _node_id_to_faiss_id_map = PrivateAttr()
    # _faiss_id_to_node_id_map is used to map the faiss id to the node id
    _faiss_id_to_node_id_map = PrivateAttr()

    def__init__(
        self,
        faiss_index: Any,
    ) -> None:
"""Initialize params."""
        import_err_msg = """
            `faiss` package not found. For instructions on
            how to install `faiss` please visit
            https://github.com/facebookresearch/faiss/wiki/Installing-Faiss
        """
        try:
            importfaiss
        except ImportError:
            raise ImportError(import_err_msg)

        if not isinstance(faiss_index, faiss.IndexIDMap) and not isinstance(
            faiss_index, faiss.IndexIDMap2
        ):
            raise ValueError(
                "FaissVectorMapStore requires a faiss.IndexIDMap or faiss.IndexIDMap2 index. "
                "Please create an IndexIDMap2 index and pass it to the FaissVectorMapStore."
            )
        super().__init__(faiss_index=faiss_index)
        self._node_id_to_faiss_id_map = {}
        self._faiss_id_to_node_id_map = {}

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to index.

        NOTE: in the Faiss vector store, we do not store text in Faiss.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        """
        new_ids = []
        for node in nodes:
            text_embedding = node.get_embedding()
            text_embedding_np = np.array(text_embedding, dtype="float32")[np.newaxis, :]
            self._node_id_to_faiss_id_map[node.id_] = self._faiss_index.ntotal
            self._faiss_id_to_node_id_map[self._faiss_index.ntotal] = node.id_
            self._faiss_index.add_with_ids(
                text_embedding_np, np.array([self._faiss_index.ntotal], dtype=np.int64)
            )
            new_ids.append(node.id_)
        return new_ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        # only handle delete on node_ids
        if ref_doc_id in self._node_id_to_faiss_id_map:
            faiss_id = self._node_id_to_faiss_id_map[ref_doc_id]
            # remove the faiss id from the faiss index
            self._faiss_index.remove_ids(np.array([faiss_id], dtype=np.int64))
            # remove the node id from the node id map
            if ref_doc_id in self._node_id_to_faiss_id_map:
                del self._node_id_to_faiss_id_map[ref_doc_id]
            # remove the faiss id from the faiss id map
            if faiss_id in self._faiss_id_to_node_id_map:
                del self._faiss_id_to_node_id_map[faiss_id]

    defdelete_nodes(
        self,
        node_ids: Optional[List[str]] = None,
        filters: Optional[MetadataFilters] = None,
        **delete_kwargs: Any,
    ) -> None:
"""Delete nodes from vector store."""
        if filters is not None:
            raise NotImplementedError("Metadata filters not implemented for Faiss yet.")

        if node_ids is None:
            raise ValueError("node_ids must be provided to delete nodes.")

        faiss_ids = []
        for node_id in node_ids:
            # get the faiss id from the node_id_map
            faiss_id = self._node_id_to_faiss_id_map.get(node_id)
            if faiss_id is not None:
                faiss_ids.append(faiss_id)
        if not faiss_ids:
            return

        self._faiss_index.remove_ids(np.array(faiss_ids, dtype=np.int64))

        # cleanup references
        for node_id in node_ids:
            # get the faiss id from the node_id_map
            faiss_id = self._node_id_to_faiss_id_map.get(node_id)
            if faiss_id is not None and faiss_id in self._faiss_id_to_node_id_map:
                del self._faiss_id_to_node_id_map[faiss_id]
            if node_id in self._node_id_to_faiss_id_map:
                del self._node_id_to_faiss_id_map[node_id]

    defquery(
        self,
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query_embedding (List[float]): query embedding
            similarity_top_k (int): top k most similar nodes

        """
        if query.filters is not None:
            raise ValueError("Metadata filters not implemented for Faiss yet.")

        query_embedding = cast(List[float], query.query_embedding)
        query_embedding_np = np.array(query_embedding, dtype="float32")[np.newaxis, :]
        dists, indices = self._faiss_index.search(
            query_embedding_np, query.similarity_top_k
        )
        dists = list(dists[0])
        # if empty, then return an empty response
        if len(indices) == 0:
            return VectorStoreQueryResult(similarities=[], ids=[])

        # returned dimension is 1 x k
        node_idxs = indices[0]

        filtered_dists = []
        filtered_node_idxs = []
        for dist, idx in zip(dists, node_idxs):
            if idx  0:
                continue
            filtered_dists.append(dist)
            filtered_node_idxs.append(self._faiss_id_to_node_id_map[idx])

        return VectorStoreQueryResult(
            similarities=filtered_dists, ids=filtered_node_idxs
        )

    defpersist(
        self,
        persist_path: str = DEFAULT_PERSIST_PATH,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> None:
"""
        Save to file.

        This method saves the vector store to disk.

        Args:
            persist_path (str): The save_path of the file.

        """
        super().persist(persist_path=persist_path, fs=fs)
        dirpath = os.path.dirname(persist_path)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        id_map = {}
        id_map["node_id_to_faiss_id_map"] = self._node_id_to_faiss_id_map
        id_map["faiss_id_to_node_id_map"] = self._faiss_id_to_node_id_map
        # save the id map as JSON for safe deserialization
        id_map_path = os.path.join(dirpath, DEFAULT_ID_MAP_NAME)
        with open(id_map_path, "w") as f:
            json.dump(id_map, f)

    @classmethod
    deffrom_persist_dir(
        cls,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> "FaissMapVectorStore":
        persist_path = os.path.join(
            persist_dir,
            f"{DEFAULT_VECTOR_STORE}{NAMESPACE_SEP}{DEFAULT_PERSIST_FNAME}",
        )
        # only support local storage for now
        if fs and not isinstance(fs, LocalFileSystem):
            raise NotImplementedError("FAISS only supports local storage for now.")
        return cls.from_persist_path(persist_path=persist_path, fs=None)

    @classmethod
    deffrom_persist_path(
        cls,
        persist_path: str,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> "FaissMapVectorStore":
        importfaiss

        # I don't think FAISS supports fsspec, it requires a path in the SWIG interface
        # TODO: copy to a temp file and load into memory from there
        if fs and not isinstance(fs, LocalFileSystem):
            raise NotImplementedError("FAISS only supports local storage for now.")

        if not os.path.exists(persist_path):
            raise ValueError(f"No existing {__name__} found at {persist_path}.")

        dirpath = os.path.dirname(persist_path)
        id_map_path = os.path.join(dirpath, DEFAULT_ID_MAP_NAME)
        if not os.path.exists(persist_path):
            raise ValueError(f"No existing {__name__} found at {persist_path}.")

        faiss_index = faiss.read_index(persist_path)
        with open(id_map_path, "r") as f:
            raw = f.read()
        try:
            id_map = json.loads(raw)
        except json.JSONDecodeError:
            # Fallback for files persisted with the old str() format
            id_map = ast.literal_eval(raw)

        map_vs = cls(faiss_index=faiss_index)
        map_vs._node_id_to_faiss_id_map = {
            k: int(v) for k, v in id_map["node_id_to_faiss_id_map"].items()
        }
        map_vs._faiss_id_to_node_id_map = {
            int(k): v for k, v in id_map["faiss_id_to_node_id_map"].items()
        }
        return map_vs

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/faiss/#llama_index.vector_stores.faiss.FaissMapVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
NOTE: in the Faiss vector store, we do not store text in Faiss.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-faiss/llama_index/vector_stores/faiss/map_store.py`  
| 
```
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

    NOTE: in the Faiss vector store, we do not store text in Faiss.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings

    """
    new_ids = []
    for node in nodes:
        text_embedding = node.get_embedding()
        text_embedding_np = np.array(text_embedding, dtype="float32")[np.newaxis, :]
        self._node_id_to_faiss_id_map[node.id_] = self._faiss_index.ntotal
        self._faiss_id_to_node_id_map[self._faiss_index.ntotal] = node.id_
        self._faiss_index.add_with_ids(
            text_embedding_np, np.array([self._faiss_index.ntotal], dtype=np.int64)
        )
        new_ids.append(node.id_)
    return new_ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/faiss/#llama_index.vector_stores.faiss.FaissMapVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-faiss/llama_index/vector_stores/faiss/map_store.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    # only handle delete on node_ids
    if ref_doc_id in self._node_id_to_faiss_id_map:
        faiss_id = self._node_id_to_faiss_id_map[ref_doc_id]
        # remove the faiss id from the faiss index
        self._faiss_index.remove_ids(np.array([faiss_id], dtype=np.int64))
        # remove the node id from the node id map
        if ref_doc_id in self._node_id_to_faiss_id_map:
            del self._node_id_to_faiss_id_map[ref_doc_id]
        # remove the faiss id from the faiss id map
        if faiss_id in self._faiss_id_to_node_id_map:
            del self._faiss_id_to_node_id_map[faiss_id]

```
 |  
| --- | --- |  
###  delete_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/faiss/#llama_index.vector_stores.faiss.FaissMapVectorStore.delete_nodes "Permanent link")

```
delete_nodes(
    node_ids: Optional[[]] = None,
    filters: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Delete nodes from vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-faiss/llama_index/vector_stores/faiss/map_store.py`  
| 
```
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
```
 | 
```
defdelete_nodes(
    self,
    node_ids: Optional[List[str]] = None,
    filters: Optional[MetadataFilters] = None,
    **delete_kwargs: Any,
) -> None:
"""Delete nodes from vector store."""
    if filters is not None:
        raise NotImplementedError("Metadata filters not implemented for Faiss yet.")

    if node_ids is None:
        raise ValueError("node_ids must be provided to delete nodes.")

    faiss_ids = []
    for node_id in node_ids:
        # get the faiss id from the node_id_map
        faiss_id = self._node_id_to_faiss_id_map.get(node_id)
        if faiss_id is not None:
            faiss_ids.append(faiss_id)
    if not faiss_ids:
        return

    self._faiss_index.remove_ids(np.array(faiss_ids, dtype=np.int64))

    # cleanup references
    for node_id in node_ids:
        # get the faiss id from the node_id_map
        faiss_id = self._node_id_to_faiss_id_map.get(node_id)
        if faiss_id is not None and faiss_id in self._faiss_id_to_node_id_map:
            del self._faiss_id_to_node_id_map[faiss_id]
        if node_id in self._node_id_to_faiss_id_map:
            del self._node_id_to_faiss_id_map[node_id]

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/faiss/#llama_index.vector_stores.faiss.FaissMapVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_embedding`  |  `List[float]`  |  query embedding  |  _required_  |  
|  `similarity_top_k`  |  top k most similar nodes  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-faiss/llama_index/vector_stores/faiss/map_store.py`  
| 
```
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
        query_embedding (List[float]): query embedding
        similarity_top_k (int): top k most similar nodes

    """
    if query.filters is not None:
        raise ValueError("Metadata filters not implemented for Faiss yet.")

    query_embedding = cast(List[float], query.query_embedding)
    query_embedding_np = np.array(query_embedding, dtype="float32")[np.newaxis, :]
    dists, indices = self._faiss_index.search(
        query_embedding_np, query.similarity_top_k
    )
    dists = list(dists[0])
    # if empty, then return an empty response
    if len(indices) == 0:
        return VectorStoreQueryResult(similarities=[], ids=[])

    # returned dimension is 1 x k
    node_idxs = indices[0]

    filtered_dists = []
    filtered_node_idxs = []
    for dist, idx in zip(dists, node_idxs):
        if idx  0:
            continue
        filtered_dists.append(dist)
        filtered_node_idxs.append(self._faiss_id_to_node_id_map[idx])

    return VectorStoreQueryResult(
        similarities=filtered_dists, ids=filtered_node_idxs
    )

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/faiss/#llama_index.vector_stores.faiss.FaissMapVectorStore.persist "Permanent link")

```
persist(
    persist_path:  = DEFAULT_PERSIST_PATH,
    fs: Optional[AbstractFileSystem] = None,
) -> None

```

Save to file.
This method saves the vector store to disk.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `persist_path`  |  The save_path of the file.  |  `DEFAULT_PERSIST_PATH`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-faiss/llama_index/vector_stores/faiss/map_store.py`  
| 
```
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
```
 | 
```
defpersist(
    self,
    persist_path: str = DEFAULT_PERSIST_PATH,
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> None:
"""
    Save to file.

    This method saves the vector store to disk.

    Args:
        persist_path (str): The save_path of the file.

    """
    super().persist(persist_path=persist_path, fs=fs)
    dirpath = os.path.dirname(persist_path)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    id_map = {}
    id_map["node_id_to_faiss_id_map"] = self._node_id_to_faiss_id_map
    id_map["faiss_id_to_node_id_map"] = self._faiss_id_to_node_id_map
    # save the id map as JSON for safe deserialization
    id_map_path = os.path.join(dirpath, DEFAULT_ID_MAP_NAME)
    with open(id_map_path, "w") as f:
        json.dump(id_map, f)

```
 |  
| --- | --- |  
options: members: - FaissVectorStore
