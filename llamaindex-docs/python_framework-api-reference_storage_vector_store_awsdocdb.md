# Awsdocdb
##  AWSDocDbVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/awsdocdb/#llama_index.vector_stores.awsdocdb.AWSDocDbVectorStore "Permanent link")
Bases: 
AWS DocumentDB Vector Store.
To use, you should have both: - the `pymongo` python package installed - a connection string associated with a DocumentDB Instance
Please refer to the official Vector Search documentation for more details: https://docs.aws.amazon.com/documentdb/latest/developerguide/vector-search.html
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-awsdocdb/llama_index/vector_stores/awsdocdb/base.py`  
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
```
 | 
```
classAWSDocDbVectorStore(BasePydanticVectorStore):
"""
    AWS DocumentDB Vector Store.

    To use, you should have both:
    - the ``pymongo`` python package installed
    - a connection string associated with a DocumentDB Instance

    Please refer to the official Vector Search documentation for more details:
    https://docs.aws.amazon.com/documentdb/latest/developerguide/vector-search.html

    """

    stores_text: bool = True
    flat_metadata: bool = True

    _docdb_client: MongoClient = PrivateAttr()
    _similarity_score: AWSDocDbVectorStoreSimilarityType = PrivateAttr()
    _collection: Any = PrivateAttr()
    _embedding_key: str = PrivateAttr()
    _id_key: str = PrivateAttr()
    _text_key: str = PrivateAttr()
    _metadata_key: str = PrivateAttr()
    _insert_kwargs: Dict = PrivateAttr()
    _index_crud: DocDbIndex = PrivateAttr()

    def__init__(
        self,
        docdb_client: Optional[Any] = None,
        db_name: str = "default_db",
        index_name: str = "default_index",
        collection_name: str = "default_collection",
        id_key: str = "id",
        embedding_key: str = "embedding",
        text_key: str = "text",
        metadata_key: str = "metadata",
        insert_kwargs: Optional[Dict] = None,
        similarity_score="cosine",
        **kwargs: Any,
    ) -> None:
"""
        Initialize the vector store.

        Args:
            docdb_client: A DocumentDB client.
            db_name: A DocumentDB database name.
            collection_name: A DocumentDB collection name.
            id_key: The data field to use as the id.
            embedding_key: A DocumentDB field that will contain
            the embedding for each document.
            text_key: A DocumentDB field that will contain the text for each document.
            metadata_key: A DocumentDB field that will contain
            the metadata for each document.
            insert_kwargs: The kwargs used during `insert`.

        """
        super().__init__()

        if docdb_client is not None:
            self._docdb_client = cast(MongoClient, docdb_client)
        else:
            raise ValueError("Must specify connection string to DocumentDB instance ")
        self._similarity_score = similarity_score
        self._collection = self._docdb_client[db_name][collection_name]
        self._embedding_key = embedding_key
        self._id_key = id_key
        self._text_key = text_key
        self._metadata_key = metadata_key
        self._insert_kwargs = insert_kwargs or {}
        self._index_crud = DocDbIndex(index_name, self._embedding_key, self._collection)

    @classmethod
    defclass_name(cls) -> str:
        return "AWSDocDbVectorStore"

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to index.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        Returns:
            A List of ids for successfully added nodes.

        """
        ids = []
        data_to_insert = []
        for node in nodes:
            metadata = node_to_metadata_dict(
                node, remove_text=True, flat_metadata=self.flat_metadata
            )

            entry = {
                self._id_key: node.node_id,
                self._embedding_key: node.get_embedding(),
                self._text_key: node.get_content(metadata_mode=MetadataMode.NONE) or "",
                self._metadata_key: metadata,
            }
            data_to_insert.append(entry)
            ids.append(node.node_id)
        logger.debug("Inserting data into DocumentDB: %s", data_to_insert)
        insert_result = self._collection.insert_many(
            data_to_insert, **self._insert_kwargs
        )
        logger.debug("Result of insert: %s", insert_result)
        return ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using by id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        if ref_doc_id is None:
            raise ValueError("No document id provided to delete.")
        self._collection.delete_one({self._metadata_key + ".ref_doc_id": ref_doc_id})

    @property
    defclient(self) -> Any:
"""Return DocDB client."""
        return self._docdb_client

    def_query(
        self, query: VectorStoreQuery, projection: Optional[Dict[str, int]] = None
    ) -> VectorStoreQueryResult:
        params: Dict[str, Any] = {
            "vector": query.query_embedding,
            "path": self._embedding_key,
            "similarity": self._similarity_score,
            "k": query.similarity_top_k,
        }
        if query.filters:
            params["filter"] = _to_mongodb_filter(query.filters)

        if projection is None:
            pipeline = [{"$search": {"vectorSearch": params}}]
        else:
            pipeline = [{"$search": {"vectorSearch": params}}, {"$project": projection}]
        logger.debug("Running query pipeline: %s", pipeline)
        cursor = self._collection.aggregate(pipeline)  # type: ignore
        top_k_nodes = []
        top_k_ids = []
        top_k_scores = []
        for res in cursor:
            text = res.pop(self._text_key)
            vector = res.pop(self._embedding_key)
            id = res.pop(self._id_key)
            metadata_dict = res.pop(self._metadata_key)
            score = similarity(query.query_embedding, vector, self._similarity_score)

            try:
                node = metadata_dict_to_node(metadata_dict)
                node.set_content(text)
            except Exception:
                # NOTE: deprecated legacy logic for backward compatibility
                metadata, node_info, relationships = legacy_metadata_dict_to_node(
                    metadata_dict
                )

                node = TextNode(
                    text=text,
                    id_=id,
                    metadata=metadata,
                    start_char_idx=node_info.get("start", None),
                    end_char_idx=node_info.get("end", None),
                    relationships=relationships,
                )

            top_k_ids.append(id)
            top_k_nodes.append(node)
            top_k_scores.append(score)
        result = VectorStoreQueryResult(
            nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
        )
        logger.debug("Result of query: %s", result)
        return result

    defquery(
        self,
        query: VectorStoreQuery,
        projection: Optional[Dict[str, int]] = None,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query: a VectorStoreQuery object.
            projection: a dictionary specifying which fields to return after the search

        Returns:
            A VectorStoreQueryResult containing the results of the query.

        """
        return self._query(query, projection=projection)

    defcreate_index(self, dimensions, similarity_score=None):
        score = self._similarity_score
        if similarity_score is not None:
            score = similarity
        return self._index_crud.create_index(dimensions, score)

    defdelete_index(self):
        return self._index_crud.delete_index()

    def__del__(self) -> None:
        self._docdb_client.close()

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/awsdocdb/#llama_index.vector_stores.awsdocdb.AWSDocDbVectorStore.client "Permanent link")

```
client: 

```

Return DocDB client.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/awsdocdb/#llama_index.vector_stores.awsdocdb.AWSDocDbVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  A List of ids for successfully added nodes.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-awsdocdb/llama_index/vector_stores/awsdocdb/base.py`  
| 
```
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

    Returns:
        A List of ids for successfully added nodes.

    """
    ids = []
    data_to_insert = []
    for node in nodes:
        metadata = node_to_metadata_dict(
            node, remove_text=True, flat_metadata=self.flat_metadata
        )

        entry = {
            self._id_key: node.node_id,
            self._embedding_key: node.get_embedding(),
            self._text_key: node.get_content(metadata_mode=MetadataMode.NONE) or "",
            self._metadata_key: metadata,
        }
        data_to_insert.append(entry)
        ids.append(node.node_id)
    logger.debug("Inserting data into DocumentDB: %s", data_to_insert)
    insert_result = self._collection.insert_many(
        data_to_insert, **self._insert_kwargs
    )
    logger.debug("Result of insert: %s", insert_result)
    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/awsdocdb/#llama_index.vector_stores.awsdocdb.AWSDocDbVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using by id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-awsdocdb/llama_index/vector_stores/awsdocdb/base.py`  
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using by id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    if ref_doc_id is None:
        raise ValueError("No document id provided to delete.")
    self._collection.delete_one({self._metadata_key + ".ref_doc_id": ref_doc_id})

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/awsdocdb/#llama_index.vector_stores.awsdocdb.AWSDocDbVectorStore.query "Permanent link")

```
query(
    query: ,
    projection: Optional[[, ]] = None,
    **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  a VectorStoreQuery object.  |  _required_  |  
|  `projection`  |  `Optional[Dict[str, int]]`  |  a dictionary specifying which fields to return after the search  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  A VectorStoreQueryResult containing the results of the query.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-awsdocdb/llama_index/vector_stores/awsdocdb/base.py`  
| 
```
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
```
 | 
```
defquery(
    self,
    query: VectorStoreQuery,
    projection: Optional[Dict[str, int]] = None,
    **kwargs: Any,
) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query: a VectorStoreQuery object.
        projection: a dictionary specifying which fields to return after the search

    Returns:
        A VectorStoreQueryResult containing the results of the query.

    """
    return self._query(query, projection=projection)

```
 |  
| --- | --- |  
options: members: - AWSDocDbVectorStore
