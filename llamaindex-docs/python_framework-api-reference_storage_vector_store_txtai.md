# Txtai
##  TxtaiVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/txtai/#llama_index.vector_stores.txtai.TxtaiVectorStore "Permanent link")
Bases: 
txtai Vector Store.

```
Embeddings are stored within a txtai index.

During query time, the index uses txtai to query for the top
k embeddings, and returns the corresponding indices.

```

Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `txtai_index`  |  txtai index instance  |  _required_  |  
Examples:
`pip install llama-index-vector-stores-txtai`
```python import txtai from llama_index.vector_stores.txtai import TxtaiVectorStore
### Create txtai ann index[#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/txtai/#llama_index.vector_stores.txtai.TxtaiVectorStore--create-txtai-ann-index "Permanent link")
txtai_index = txtai.ann.ANNFactory.create({"backend": "numpy"})
vector_store = TxtaiVectorStore(txtai_index=txtai_index)
```
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-txtai/llama_index/vector_stores/txtai/base.py`  
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
```
 | 
```
classTxtaiVectorStore(BasePydanticVectorStore):
"""
    txtai Vector Store.

        Embeddings are stored within a txtai index.

        During query time, the index uses txtai to query for the top
        k embeddings, and returns the corresponding indices.

    Args:
            txtai_index (txtai.ann.ANN): txtai index instance

    Examples:
            `pip install llama-index-vector-stores-txtai`

            ```python
            import txtai
            from llama_index.vector_stores.txtai import TxtaiVectorStore

            # Create txtai ann index
            txtai_index = txtai.ann.ANNFactory.create({"backend": "numpy"})

            vector_store = TxtaiVectorStore(txtai_index=txtai_index)
    ```

    """

    stores_text: bool = False

    _txtai_index = PrivateAttr()

    def__init__(
        self,
        txtai_index: Any,
    ) -> None:
"""Initialize params."""
        try:
            importtxtai
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        super().__init__()

        self._txtai_index = cast(txtai.ann.ANN, txtai_index)

    @classmethod
    deffrom_persist_dir(
        cls,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> "TxtaiVectorStore":
        persist_path = os.path.join(
            persist_dir,
            f"{DEFAULT_VECTOR_STORE}{NAMESPACE_SEP}{DEFAULT_PERSIST_FNAME}",
        )
        # only support local storage for now
        if fs and not isinstance(fs, LocalFileSystem):
            raise NotImplementedError("txtai only supports local storage for now.")
        return cls.from_persist_path(persist_path=persist_path, fs=None)

    @classmethod
    deffrom_persist_path(
        cls,
        persist_path: str,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> "TxtaiVectorStore":
        try:
            importtxtai
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        if fs and not isinstance(fs, LocalFileSystem):
            raise NotImplementedError("txtai only supports local storage for now.")

        if not os.path.exists(persist_path):
            raise ValueError(f"No existing {__name__} found at {persist_path}.")

        logger.info(f"Loading {__name__} config from {persist_path}.")
        parent_directory = Path(persist_path).parent
        config_path = parent_directory / "config.json"
        jsonconfig = config_path.exists()
        # Determine if config is json or pickle
        config_path = config_path if jsonconfig else parent_directory / "config"
        # Load configuration
        with open(config_path, "r" if jsonconfig else "rb") as f:
            config = json.load(f) if jsonconfig else pickle.load(f)

        logger.info(f"Loading {__name__} from {persist_path}.")
        txtai_index = txtai.ann.ANNFactory.create(config)
        txtai_index.load(persist_path)
        return cls(txtai_index=txtai_index)

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
        text_embedding_np = np.array(
            [node.get_embedding() for node in nodes], dtype="float32"
        )

        # Check if the ann index is already created
        # If not create the index with node embeddings
        if self._txtai_index.backend is None:
            self._txtai_index.index(text_embedding_np)
        else:
            self._txtai_index.append(text_embedding_np)

        indx_size = self._txtai_index.count()
        return [str(idx) for idx in range(indx_size - len(nodes) + 1, indx_size + 1)]

    @property
    defclient(self) -> Any:
"""Return the txtai index."""
        return self._txtai_index

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
        if fs and not isinstance(fs, LocalFileSystem):
            raise NotImplementedError("txtai only supports local storage for now.")

        dirpath = Path(persist_path).parent
        dirpath.mkdir(exist_ok=True)

        jsonconfig = self._txtai_index.config.get("format", "pickle") == "json"
        # Determine if config is json or pickle
        config_path = dirpath / "config.json" if jsonconfig else dirpath / "config"

        # Write configuration
        with open(
            config_path,
            "w" if jsonconfig else "wb",
            encoding="utf-8" if jsonconfig else None,
        ) as f:
            if jsonconfig:
                # Write config as JSON
                json.dump(self._txtai_index.config, f, default=str)
            else:
                fromtxtai.versionimport __pickle__

                # Write config as pickle format
                pickle.dump(self._txtai_index.config, f, protocol=__pickle__)

        self._txtai_index.save(persist_path)

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        self._txtai_index.delete([int(ref_doc_id)])

    defquery(
        self,
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query (VectorStoreQuery): query to search for in the index

        """
        if query.filters is not None:
            raise ValueError("Metadata filters not implemented for txtai yet.")

        query_embedding = cast(List[float], query.query_embedding)
        query_embedding_np = np.array(query_embedding, dtype="float32")[np.newaxis, :]
        search_result = self._txtai_index.search(
            query_embedding_np, query.similarity_top_k
        )[0]
        # if empty, then return an empty response
        if len(search_result) == 0:
            return VectorStoreQueryResult(similarities=[], ids=[])

        filtered_dists = []
        filtered_node_idxs = []
        for dist, idx in search_result:
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
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/txtai/#llama_index.vector_stores.txtai.TxtaiVectorStore.client "Permanent link")

```
client: 

```

Return the txtai index.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/txtai/#llama_index.vector_stores.txtai.TxtaiVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-txtai/llama_index/vector_stores/txtai/base.py`  
| 
```
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
    text_embedding_np = np.array(
        [node.get_embedding() for node in nodes], dtype="float32"
    )

    # Check if the ann index is already created
    # If not create the index with node embeddings
    if self._txtai_index.backend is None:
        self._txtai_index.index(text_embedding_np)
    else:
        self._txtai_index.append(text_embedding_np)

    indx_size = self._txtai_index.count()
    return [str(idx) for idx in range(indx_size - len(nodes) + 1, indx_size + 1)]

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/txtai/#llama_index.vector_stores.txtai.TxtaiVectorStore.persist "Permanent link")

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
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-txtai/llama_index/vector_stores/txtai/base.py`  
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
    if fs and not isinstance(fs, LocalFileSystem):
        raise NotImplementedError("txtai only supports local storage for now.")

    dirpath = Path(persist_path).parent
    dirpath.mkdir(exist_ok=True)

    jsonconfig = self._txtai_index.config.get("format", "pickle") == "json"
    # Determine if config is json or pickle
    config_path = dirpath / "config.json" if jsonconfig else dirpath / "config"

    # Write configuration
    with open(
        config_path,
        "w" if jsonconfig else "wb",
        encoding="utf-8" if jsonconfig else None,
    ) as f:
        if jsonconfig:
            # Write config as JSON
            json.dump(self._txtai_index.config, f, default=str)
        else:
            fromtxtai.versionimport __pickle__

            # Write config as pickle format
            pickle.dump(self._txtai_index.config, f, protocol=__pickle__)

    self._txtai_index.save(persist_path)

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/txtai/#llama_index.vector_stores.txtai.TxtaiVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-txtai/llama_index/vector_stores/txtai/base.py`  
| 
```
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
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    self._txtai_index.delete([int(ref_doc_id)])

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/txtai/#llama_index.vector_stores.txtai.TxtaiVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  query to search for in the index  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-txtai/llama_index/vector_stores/txtai/base.py`  
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
        query (VectorStoreQuery): query to search for in the index

    """
    if query.filters is not None:
        raise ValueError("Metadata filters not implemented for txtai yet.")

    query_embedding = cast(List[float], query.query_embedding)
    query_embedding_np = np.array(query_embedding, dtype="float32")[np.newaxis, :]
    search_result = self._txtai_index.search(
        query_embedding_np, query.similarity_top_k
    )[0]
    # if empty, then return an empty response
    if len(search_result) == 0:
        return VectorStoreQueryResult(similarities=[], ids=[])

    filtered_dists = []
    filtered_node_idxs = []
    for dist, idx in search_result:
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
options: members: - TxtaiVectorStore
