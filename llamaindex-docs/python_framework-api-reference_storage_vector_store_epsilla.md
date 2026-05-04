# Epsilla
##  EpsillaVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/epsilla/#llama_index.vector_stores.epsilla.EpsillaVectorStore "Permanent link")
Bases: 
The Epsilla Vector Store.
In this vector store we store the text, its embedding and a few pieces of its metadata in a Epsilla collection. This implemnetation allows the use of an already existing collection. It also supports creating a new one if the collection does not exist or if `overwrite` is set to True.
As a prerequisite, you need to install `pyepsilla` package and have a running Epsilla vector database (for example, through our docker image) See the following documentation for how to run an Epsilla vector database: https://epsilla-inc.gitbook.io/epsilladb/quick-start
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `client`  |  Epsilla client to connect to.  |  _required_  |  
|  `collection_name`  |  `Optional[str]`  |  Which collection to use. Defaults to "llama_collection".  |  `'llama_collection'`  |  
|  `db_path`  |  `Optional[str]`  |  The path where the database will be persisted. Defaults to "/tmp/langchain-epsilla".  |  `DEFAULT_PERSIST_DIR`  |  
|  `db_name`  |  `Optional[str]`  |  Give a name to the loaded database. Defaults to "langchain_store".  |  `'llama_db'`  |  
|  `dimension`  |  `Optional[int]`  |  The dimension of the embeddings. If not provided, collection creation will be done on first insert. Defaults to None.  |  `None`  |  
|  `overwrite`  |  `Optional[bool]`  |  Whether to overwrite existing collection with same name. Defaults to False.  |  `False`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `EpsillaVectorStore`  |  Vectorstore that supports add, delete, and query.  |  
Examples:
`pip install llama-index-vector-stores-epsilla`

```
fromllama_index.vector_stores.epsillaimport EpsillaVectorStore
frompyepsillaimport vectordb

client = vectordb.Client()
vector_store = EpsillaVectorStore(client=client, db_path="/tmp/llamastore")

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-epsilla/llama_index/vector_stores/epsilla/base.py`  
| 
```
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
```
 | 
```
classEpsillaVectorStore(BasePydanticVectorStore):
"""
    The Epsilla Vector Store.

    In this vector store we store the text, its embedding and
    a few pieces of its metadata in a Epsilla collection. This implemnetation
    allows the use of an already existing collection.
    It also supports creating a new one if the collection does not
    exist or if `overwrite` is set to True.

    As a prerequisite, you need to install ``pyepsilla`` package
    and have a running Epsilla vector database (for example, through our docker image)
    See the following documentation for how to run an Epsilla vector database:
    https://epsilla-inc.gitbook.io/epsilladb/quick-start

    Args:
        client (Any): Epsilla client to connect to.
        collection_name (Optional[str]): Which collection to use.
                    Defaults to "llama_collection".
        db_path (Optional[str]): The path where the database will be persisted.
                    Defaults to "/tmp/langchain-epsilla".
        db_name (Optional[str]): Give a name to the loaded database.
                    Defaults to "langchain_store".
        dimension (Optional[int]): The dimension of the embeddings. If not provided,
                    collection creation will be done on first insert. Defaults to None.
        overwrite (Optional[bool]): Whether to overwrite existing collection with same
                    name. Defaults to False.

    Returns:
        EpsillaVectorStore: Vectorstore that supports add, delete, and query.

    Examples:
        `pip install llama-index-vector-stores-epsilla`

        ```python
        from llama_index.vector_stores.epsilla import EpsillaVectorStore
        from pyepsilla import vectordb

        client = vectordb.Client()
        vector_store = EpsillaVectorStore(client=client, db_path="/tmp/llamastore")
        ```

    """

    stores_text: bool = True
    flat_metadata: bool = False

    _client: vectordb.Client = PrivateAttr()
    _collection_name: str = PrivateAttr()
    _collection_created: bool = PrivateAttr()

    def__init__(
        self,
        client: Any,
        collection_name: str = "llama_collection",
        db_path: Optional[str] = DEFAULT_PERSIST_DIR,  # sub folder
        db_name: Optional[str] = "llama_db",
        dimension: Optional[int] = None,
        overwrite: bool = False,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        super().__init__()

        if not isinstance(client, vectordb.Client):
            raise TypeError(
                f"client should be an instance of pyepsilla.vectordb.Client, "
                f"got {type(client)}"
            )

        self._client: vectordb.Client = client
        self._collection_name = collection_name
        self._client.load_db(db_name, db_path)
        self._client.use_db(db_name)
        self._collection_created = False

        status_code, response = self._client.list_tables()
        if status_code != 200:
            self._handle_error(msg=response["message"])
        table_list = response["result"]

        if self._collection_name in table_list and overwrite is False:
            self._collection_created = True

        if self._collection_name in table_list and overwrite is True:
            status_code, response = self._client.drop_table(
                table_name=self._collection_name
            )
            if status_code != 200:
                self._handle_error(msg=response["message"])
            logger.debug(
                f"Successfully removed old collection: {self._collection_name}"
            )
            if dimension is not None:
                self._create_collection(dimension)

        if self._collection_name not in table_list and dimension is not None:
            self._create_collection(dimension)

    @classmethod
    defclass_name(cls) -> str:
        return "EpsillaVectorStore"

    @property
    defclient(self) -> Any:
"""Return the Epsilla client."""
        return self._client

    def_handle_error(self, msg: str) -> None:
"""Handle error."""
        logger.error(f"Failed to get records: {msg}")
        raise Exception(f"Error: {msg}.")

    def_create_collection(self, dimension: int) -> None:
"""
        Create collection.

        Args:
            dimension (int): The dimension of the embeddings.

        """
        fields: List[dict] = [
            {"name": "id", "dataType": "STRING", "primaryKey": True},
            {"name": DEFAULT_DOC_ID_KEY, "dataType": "STRING"},
            {"name": DEFAULT_TEXT_KEY, "dataType": "STRING"},
            {
                "name": DEFAULT_EMBEDDING_KEY,
                "dataType": "VECTOR_FLOAT",
                "dimensions": dimension,
            },
            {"name": "metadata", "dataType": "JSON"},
        ]
        status_code, response = self._client.create_table(
            table_name=self._collection_name, table_fields=fields
        )
        if status_code != 200:
            self._handle_error(msg=response["message"])
        self._collection_created = True
        logger.debug(f"Successfully created collection: {self._collection_name}")

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to Epsilla vector store.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        Returns:
            List[str]: List of ids inserted.

        """
        # If the collection doesn't exist yet, create the collection
        if not self._collection_created and len(nodes)  0:
            dimension = len(nodes[0].get_embedding())
            self._create_collection(dimension)

        elif len(nodes) == 0:
            return []

        ids = []
        records = []
        for node in nodes:
            ids.append(node.node_id)
            text = node.get_content(metadata_mode=MetadataMode.NONE)
            metadata_dict = node_to_metadata_dict(node, remove_text=True)
            metadata = metadata_dict["_node_content"]
            record = {
                "id": node.node_id,
                DEFAULT_DOC_ID_KEY: node.ref_doc_id,
                DEFAULT_TEXT_KEY: text,
                DEFAULT_EMBEDDING_KEY: node.get_embedding(),
                "metadata": metadata,
            }
            records.append(record)

        status_code, response = self._client.insert(
            table_name=self._collection_name, records=records
        )
        if status_code != 200:
            self._handle_error(msg=response["message"])

        return ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        raise NotImplementedError("Delete with filtering will be coming soon.")

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query (VectorStoreQuery): query.

        Returns:
            Vector store query result.

        """
        if not self._collection_created:
            raise ValueError("Please initialize a collection first.")

        if query.mode != VectorStoreQueryMode.DEFAULT:
            raise NotImplementedError(f"Epsilla does not support {query.mode} yet.")

        if query.filters is not None:
            raise NotImplementedError("Epsilla does not support Metadata filters yet.")

        if query.doc_ids is not None and len(query.doc_ids)  0:
            raise NotImplementedError("Epsilla does not support filters yet.")

        status_code, response = self._client.query(
            table_name=self._collection_name,
            query_field=DEFAULT_EMBEDDING_KEY,
            query_vector=query.query_embedding,
            limit=query.similarity_top_k,
            with_distance=True,
        )
        if status_code != 200:
            self._handle_error(msg=response["message"])

        results = response["result"]
        logger.debug(
            f"Successfully searched embedding in collection: {self._collection_name}"
            f" Num Results: {len(results)}"
        )

        nodes = []
        similarities = []
        ids = []
        for res in results:
            try:
                node = metadata_dict_to_node({"_node_content": res["metadata"]})
                node.text = res[DEFAULT_TEXT_KEY]
            except Exception:
                # NOTE: deprecated legacy logic for backward compatibility
                metadata, node_info, relationships = legacy_metadata_dict_to_node(
                    res["metadata"]
                )
                node = TextNode(
                    id=res["id"],
                    text=res[DEFAULT_TEXT_KEY],
                    metadata=metadata,
                    start_char_idx=node_info.get("start", None),
                    end_char_idx=node_info.get("end", None),
                    relationships=relationships,
                )
            nodes.append(node)
            similarities.append(res["@distance"])
            ids.append(res["id"])

        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/epsilla/#llama_index.vector_stores.epsilla.EpsillaVectorStore.client "Permanent link")

```
client: 

```

Return the Epsilla client.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/epsilla/#llama_index.vector_stores.epsilla.EpsillaVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to Epsilla vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: List of ids inserted.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-epsilla/llama_index/vector_stores/epsilla/base.py`  
| 
```
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
defadd(
    self,
    nodes: List[BaseNode],
    **add_kwargs: Any,
) -> List[str]:
"""
    Add nodes to Epsilla vector store.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings

    Returns:
        List[str]: List of ids inserted.

    """
    # If the collection doesn't exist yet, create the collection
    if not self._collection_created and len(nodes)  0:
        dimension = len(nodes[0].get_embedding())
        self._create_collection(dimension)

    elif len(nodes) == 0:
        return []

    ids = []
    records = []
    for node in nodes:
        ids.append(node.node_id)
        text = node.get_content(metadata_mode=MetadataMode.NONE)
        metadata_dict = node_to_metadata_dict(node, remove_text=True)
        metadata = metadata_dict["_node_content"]
        record = {
            "id": node.node_id,
            DEFAULT_DOC_ID_KEY: node.ref_doc_id,
            DEFAULT_TEXT_KEY: text,
            DEFAULT_EMBEDDING_KEY: node.get_embedding(),
            "metadata": metadata,
        }
        records.append(record)

    status_code, response = self._client.insert(
        table_name=self._collection_name, records=records
    )
    if status_code != 200:
        self._handle_error(msg=response["message"])

    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/epsilla/#llama_index.vector_stores.epsilla.EpsillaVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-epsilla/llama_index/vector_stores/epsilla/base.py`  
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    raise NotImplementedError("Delete with filtering will be coming soon.")

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/epsilla/#llama_index.vector_stores.epsilla.EpsillaVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  query.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  Vector store query result.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-epsilla/llama_index/vector_stores/epsilla/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query (VectorStoreQuery): query.

    Returns:
        Vector store query result.

    """
    if not self._collection_created:
        raise ValueError("Please initialize a collection first.")

    if query.mode != VectorStoreQueryMode.DEFAULT:
        raise NotImplementedError(f"Epsilla does not support {query.mode} yet.")

    if query.filters is not None:
        raise NotImplementedError("Epsilla does not support Metadata filters yet.")

    if query.doc_ids is not None and len(query.doc_ids)  0:
        raise NotImplementedError("Epsilla does not support filters yet.")

    status_code, response = self._client.query(
        table_name=self._collection_name,
        query_field=DEFAULT_EMBEDDING_KEY,
        query_vector=query.query_embedding,
        limit=query.similarity_top_k,
        with_distance=True,
    )
    if status_code != 200:
        self._handle_error(msg=response["message"])

    results = response["result"]
    logger.debug(
        f"Successfully searched embedding in collection: {self._collection_name}"
        f" Num Results: {len(results)}"
    )

    nodes = []
    similarities = []
    ids = []
    for res in results:
        try:
            node = metadata_dict_to_node({"_node_content": res["metadata"]})
            node.text = res[DEFAULT_TEXT_KEY]
        except Exception:
            # NOTE: deprecated legacy logic for backward compatibility
            metadata, node_info, relationships = legacy_metadata_dict_to_node(
                res["metadata"]
            )
            node = TextNode(
                id=res["id"],
                text=res[DEFAULT_TEXT_KEY],
                metadata=metadata,
                start_char_idx=node_info.get("start", None),
                end_char_idx=node_info.get("end", None),
                relationships=relationships,
            )
        nodes.append(node)
        similarities.append(res["@distance"])
        ids.append(res["id"])

    return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
options: members: - EpsillaVectorStore
