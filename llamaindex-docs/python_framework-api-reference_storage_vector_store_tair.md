# Tair
##  TairVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tair/#llama_index.vector_stores.tair.TairVectorStore "Permanent link")
Bases: 
Initialize TairVectorStore.
Two index types are available: FLAT & HNSW.
index args for HNSW
  * ef_construct
  * M
  * ef_search


Detailed info for these arguments can be found here: https://www.alibabacloud.com/help/en/tair/latest/tairvector#section-c76-ull-5mk
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index_name`  |  Name of the index.  |  _required_  |  
|  `index_type`  |  Type of the index. Defaults to 'HNSW'.  |  `'HNSW'`  |  
|  `index_args`  |  `Dict[str, Any]`  |  Arguments for the index. Defaults to None.  |  `None`  |  
|  `tair_url`  |  URL for the Tair instance.  |  _required_  |  
|  `overwrite`  |  `bool`  |  Whether to overwrite the index if it already exists. Defaults to False.  |  `False`  |  
|  `kwargs`  |  Additional arguments to pass to the Tair client.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If tair-py is not installed  |  
|  `ValueError`  |  If failed to connect to Tair instance  |  
Examples:
`pip install llama-index-vector-stores-tair`

```
fromllama_index.core.vector_stores.tairimport TairVectorStore

# Create a TairVectorStore
vector_store = TairVectorStore(
    tair_url="redis://{username}:{password}@r-bp****************.redis.rds.aliyuncs.com:{port}",
    index_name="my_index",
    index_type="HNSW",
    index_args={"M": 16, "ef_construct": 200},
    overwrite=True
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tair/llama_index/vector_stores/tair/base.py`  
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
```
 | 
```
classTairVectorStore(BasePydanticVectorStore):
"""
    Initialize TairVectorStore.

    Two index types are available: FLAT & HNSW.

    index args for HNSW:
        - ef_construct
        - M
        - ef_search

    Detailed info for these arguments can be found here:
    https://www.alibabacloud.com/help/en/tair/latest/tairvector#section-c76-ull-5mk

    Args:
        index_name (str): Name of the index.
        index_type (str): Type of the index. Defaults to 'HNSW'.
        index_args (Dict[str, Any]): Arguments for the index. Defaults to None.
        tair_url (str): URL for the Tair instance.
        overwrite (bool): Whether to overwrite the index if it already exists.
            Defaults to False.
        kwargs (Any): Additional arguments to pass to the Tair client.

    Raises:
        ValueError: If tair-py is not installed
        ValueError: If failed to connect to Tair instance

    Examples:
        `pip install llama-index-vector-stores-tair`

        ```python
        from llama_index.core.vector_stores.tair import TairVectorStore

        # Create a TairVectorStore
        vector_store = TairVectorStore(
            tair_url="redis://{username}:{password}@r-bp****************.redis.rds.aliyuncs.com:{port}",
            index_name="my_index",
            index_type="HNSW",
            index_args={"M": 16, "ef_construct": 200},
            overwrite=True

        ```

    """

    stores_text: bool = True
    stores_node: bool = True
    flat_metadata: bool = False

    _tair_client: Tair = PrivateAttr()
    _index_name: str = PrivateAttr()
    _index_type: str = PrivateAttr()
    _metric_type: str = PrivateAttr()
    _overwrite: bool = PrivateAttr()
    _index_args: Dict[str, Any] = PrivateAttr()
    _query_args: Dict[str, Any] = PrivateAttr()
    _dim: int = PrivateAttr()

    def__init__(
        self,
        tair_url: str,
        index_name: str,
        index_type: str = "HNSW",
        index_args: Optional[Dict[str, Any]] = None,
        overwrite: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__()
        try:
            self._tair_client = Tair.from_url(tair_url, **kwargs)
        except ValueError as e:
            raise ValueError(f"Tair failed to connect: {e}")

        # index identifiers
        self._index_name = index_name
        self._index_type = index_type
        self._metric_type = "L2"
        self._overwrite = overwrite
        self._index_args = {}
        self._query_args = {}
        if index_type == "HNSW":
            if index_args is not None:
                ef_construct = index_args.get("ef_construct", 500)
                M = index_args.get("M", 24)
                ef_search = index_args.get("ef_search", 400)
            else:
                ef_construct = 500
                M = 24
                ef_search = 400

            self._index_args = {"ef_construct": ef_construct, "M": M}
            self._query_args = {"ef_search": ef_search}

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "TairVectorStore"

    @property
    defclient(self) -> "Tair":
"""Return the Tair client instance."""
        return self._tair_client

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
        Add nodes to the index.

        Args:
            nodes (List[BaseNode]): List of nodes with embeddings

        Returns:
            List[str]: List of ids of the documents added to the index.

        """
        # check to see if empty document list was passed
        if len(nodes) == 0:
            return []

        # set vector dim for creation if index doesn't exist
        self._dim = len(nodes[0].get_embedding())

        if self._index_exists():
            if self._overwrite:
                self.delete_index()
                self._create_index()
            else:
                logging.info(f"Adding document to existing index {self._index_name}")
        else:
            self._create_index()

        ids = []
        for node in nodes:
            attributes = {
                "id": node.node_id,
                "doc_id": node.ref_doc_id,
                "text": node.get_content(metadata_mode=MetadataMode.NONE),
            }
            metadata_dict = node_to_metadata_dict(
                node, remove_text=True, flat_metadata=self.flat_metadata
            )
            attributes.update(metadata_dict)

            ids.append(node.node_id)
            self._tair_client.tvs_hset(
                self._index_name,
                f"{node.ref_doc_id}#{node.node_id}",
                vector=node.get_embedding(),
                is_binary=False,
                **attributes,
            )

        _logger.info(f"Added {len(ids)} documents to index {self._index_name}")
        return ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete a document.

        Args:
            doc_id (str): document id

        """
        iter = self._tair_client.tvs_scan(self._index_name, "%s#*" % ref_doc_id)
        for k in iter:
            self._tair_client.tvs_del(self._index_name, k)

    defdelete_index(self) -> None:
"""Delete the index and all documents."""
        _logger.info(f"Deleting index {self._index_name}")
        self._tair_client.tvs_del_index(self._index_name)

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query the index.

        Args:
            query (VectorStoreQuery): query object

        Returns:
            VectorStoreQueryResult: query result

        Raises:
            ValueError: If query.query_embedding is None.

        """
        filter_expr = None
        if query.filters is not None:
            filter_expr = _to_filter_expr(query.filters)

        if not query.query_embedding:
            raise ValueError("Query embedding is required for querying.")

        _logger.info(f"Querying index {self._index_name}")

        query_args = self._query_args
        if self._index_type == "HNSW" and "ef_search" in kwargs:
            query_args["ef_search"] = kwargs["ef_search"]

        results = self._tair_client.tvs_knnsearch(
            self._index_name,
            query.similarity_top_k,
            query.query_embedding,
            False,
            filter_str=filter_expr,
            **query_args,
        )
        results = [(k.decode(), float(s)) for k, s in results]

        ids = []
        nodes = []
        scores = []
        pipe = self._tair_client.pipeline(transaction=False)
        for key, score in results:
            scores.append(score)
            pipe.tvs_hmget(self._index_name, key, "id", "doc_id", "text")
        metadatas = pipe.execute()
        for i, m in enumerate(metadatas):
            # TODO: properly get the _node_conent
            doc_id = m[0].decode()
            node = TextNode(
                text=m[2].decode(),
                id_=doc_id,
                embedding=None,
                relationships={
                    NodeRelationship.SOURCE: RelatedNodeInfo(node_id=m[1].decode())
                },
            )
            ids.append(doc_id)
            nodes.append(node)
        _logger.info(f"Found {len(nodes)} results for query with id {ids}")

        return VectorStoreQueryResult(nodes=nodes, ids=ids, similarities=scores)

    def_create_index(self) -> None:
        _logger.info(f"Creating index {self._index_name}")
        self._tair_client.tvs_create_index(
            self._index_name,
            self._dim,
            distance_type=self._metric_type,
            index_type=self._index_type,
            data_type=tairvector.DataType.Float32,
            **self._index_args,
        )

    def_index_exists(self) -> bool:
        index = self._tair_client.tvs_get_index(self._index_name)
        return index is not None

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tair/#llama_index.vector_stores.tair.TairVectorStore.client "Permanent link")

```
client: 

```

Return the Tair client instance.
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tair/#llama_index.vector_stores.tair.TairVectorStore.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tair/llama_index/vector_stores/tair/base.py`  
| 
```
134
135
136
137
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "TairVectorStore"

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tair/#llama_index.vector_stores.tair.TairVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes with embeddings  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: List of ids of the documents added to the index.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tair/llama_index/vector_stores/tair/base.py`  
| 
```
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
```
 | 
```
defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
    Add nodes to the index.

    Args:
        nodes (List[BaseNode]): List of nodes with embeddings

    Returns:
        List[str]: List of ids of the documents added to the index.

    """
    # check to see if empty document list was passed
    if len(nodes) == 0:
        return []

    # set vector dim for creation if index doesn't exist
    self._dim = len(nodes[0].get_embedding())

    if self._index_exists():
        if self._overwrite:
            self.delete_index()
            self._create_index()
        else:
            logging.info(f"Adding document to existing index {self._index_name}")
    else:
        self._create_index()

    ids = []
    for node in nodes:
        attributes = {
            "id": node.node_id,
            "doc_id": node.ref_doc_id,
            "text": node.get_content(metadata_mode=MetadataMode.NONE),
        }
        metadata_dict = node_to_metadata_dict(
            node, remove_text=True, flat_metadata=self.flat_metadata
        )
        attributes.update(metadata_dict)

        ids.append(node.node_id)
        self._tair_client.tvs_hset(
            self._index_name,
            f"{node.ref_doc_id}#{node.node_id}",
            vector=node.get_embedding(),
            is_binary=False,
            **attributes,
        )

    _logger.info(f"Added {len(ids)} documents to index {self._index_name}")
    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tair/#llama_index.vector_stores.tair.TairVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete a document.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `doc_id`  |  document id  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tair/llama_index/vector_stores/tair/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete a document.

    Args:
        doc_id (str): document id

    """
    iter = self._tair_client.tvs_scan(self._index_name, "%s#*" % ref_doc_id)
    for k in iter:
        self._tair_client.tvs_del(self._index_name, k)

```
 |  
| --- | --- |  
###  delete_index [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tair/#llama_index.vector_stores.tair.TairVectorStore.delete_index "Permanent link")

```
delete_index() -> None

```

Delete the index and all documents.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tair/llama_index/vector_stores/tair/base.py`  
| 
```
207
208
209
210
```
 | 
```
defdelete_index(self) -> None:
"""Delete the index and all documents."""
    _logger.info(f"Deleting index {self._index_name}")
    self._tair_client.tvs_del_index(self._index_name)

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/tair/#llama_index.vector_stores.tair.TairVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query the index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  query object  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  query result  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If query.query_embedding is None.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-tair/llama_index/vector_stores/tair/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query the index.

    Args:
        query (VectorStoreQuery): query object

    Returns:
        VectorStoreQueryResult: query result

    Raises:
        ValueError: If query.query_embedding is None.

    """
    filter_expr = None
    if query.filters is not None:
        filter_expr = _to_filter_expr(query.filters)

    if not query.query_embedding:
        raise ValueError("Query embedding is required for querying.")

    _logger.info(f"Querying index {self._index_name}")

    query_args = self._query_args
    if self._index_type == "HNSW" and "ef_search" in kwargs:
        query_args["ef_search"] = kwargs["ef_search"]

    results = self._tair_client.tvs_knnsearch(
        self._index_name,
        query.similarity_top_k,
        query.query_embedding,
        False,
        filter_str=filter_expr,
        **query_args,
    )
    results = [(k.decode(), float(s)) for k, s in results]

    ids = []
    nodes = []
    scores = []
    pipe = self._tair_client.pipeline(transaction=False)
    for key, score in results:
        scores.append(score)
        pipe.tvs_hmget(self._index_name, key, "id", "doc_id", "text")
    metadatas = pipe.execute()
    for i, m in enumerate(metadatas):
        # TODO: properly get the _node_conent
        doc_id = m[0].decode()
        node = TextNode(
            text=m[2].decode(),
            id_=doc_id,
            embedding=None,
            relationships={
                NodeRelationship.SOURCE: RelatedNodeInfo(node_id=m[1].decode())
            },
        )
        ids.append(doc_id)
        nodes.append(node)
    _logger.info(f"Found {len(nodes)} results for query with id {ids}")

    return VectorStoreQueryResult(nodes=nodes, ids=ids, similarities=scores)

```
 |  
| --- | --- |  
options: members: - TairVectorStore
