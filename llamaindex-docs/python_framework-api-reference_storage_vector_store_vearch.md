# Vearch
##  VearchVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vearch/#llama_index.vector_stores.vearch.VearchVectorStore "Permanent link")
Bases: 
Vearch vector store
embeddings are stored within a Vearch table. when query, the index uses Vearch to query for the top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `chroma_collection`  |  `Collection`  |  ChromaDB collection instance  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vearch/llama_index/vector_stores/vearch/base.py`  
| 
```
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
354
355
356
```
 | 
```
classVearchVectorStore(BasePydanticVectorStore):
"""
    Vearch vector store:
        embeddings are stored within a Vearch table.
        when query, the index uses Vearch to query for the top
        k most similar nodes.

    Args:
        chroma_collection (chromadb.api.models.Collection.Collection):
            ChromaDB collection instance

    """

    flat_metadata: bool = True
    stores_text: bool = True

    using_db_name: str
    using_table_name: str
    url: str
    _vearch: vearch_cluster.VearchCluster = PrivateAttr()

    def__init__(
        self,
        path_or_url: Optional[str] = None,
        table_name: str = _DEFAULT_TABLE_NAME,
        db_name: str = _DEFAULT_CLUSTER_DB_NAME,
        **kwargs: Any,
    ) -> None:
"""Initialize vearch vector store."""
        if path_or_url is None:
            raise ValueError("Please input url of cluster")

        if not db_name:
            db_name = _DEFAULT_CLUSTER_DB_NAME
            db_name += "_"
            db_name += str(uuid.uuid4()).split("-")[-1]

        if not table_name:
            table_name = _DEFAULT_TABLE_NAME
            table_name += "_"
            table_name += str(uuid.uuid4()).split("-")[-1]

        super().__init__(
            using_db_name=db_name,
            using_table_name=table_name,
            url=path_or_url,
        )
        self._vearch = vearch_cluster.VearchCluster(path_or_url)

    @classmethod
    defclass_name(cls) -> str:
        return "VearchVectorStore"

    @property
    defclient(self) -> Any:
"""Get client."""
        return self._vearch

    def_get_matadata_field(self, metadatas: Optional[List[dict]] = None) -> None:
        field_list = []
        if metadatas:
            for key, value in metadatas[0].items():
                if isinstance(value, int):
                    field_list.append({"field": key, "type": "int"})
                    continue
                if isinstance(value, str):
                    field_list.append({"field": key, "type": "str"})
                    continue
                if isinstance(value, float):
                    field_list.append({"field": key, "type": "float"})
                    continue
                else:
                    raise ValueError("Please check data type,support int, str, float")
        self.field_list = field_list

    def_add_texts(
        self,
        ids: Iterable[str],
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        embeddings: Optional[List[List[float]]] = None,
        **kwargs: Any,
    ) -> List[str]:
"""
        Returns:
            List of ids from adding the texts into the vectorstore.

        """
        if embeddings is None:
            raise ValueError("embeddings is None")
        self._get_matadata_field(metadatas)
        dbs_list = self._vearch.list_dbs()
        if self.using_db_name not in dbs_list:
            create_db_code = self._vearch.create_db(self.using_db_name)
            if not create_db_code:
                raise ValueError("create db failed!!!")
        space_list = self._vearch.list_spaces(self.using_db_name)
        if self.using_table_name not in space_list:
            create_space_code = self._create_space(len(embeddings[0]))
            if not create_space_code:
                raise ValueError("create space failed!!!")
        docid = []
        if embeddings is not None and metadatas is not None:
            meta_field_list = [i["field"] for i in self.field_list]
            for text, metadata, embed, id_d in zip(texts, metadatas, embeddings, ids):
                profiles: typing.Dict[str, Any] = {}
                profiles["ref_doc_id"] = id_d
                profiles["text"] = text
                for f in meta_field_list:
                    profiles[f] = metadata[f]
                embed_np = np.array(embed)
                profiles["text_embedding"] = {
                    "feature": (embed_np / np.linalg.norm(embed_np)).tolist()
                }
                insert_res = self._vearch.insert_one(
                    self.using_db_name, self.using_table_name, profiles
                )
                if insert_res["status"] == 200:
                    docid.append(insert_res["_id"])
                    continue
                else:
                    retry_insert = self._vearch.insert_one(
                        self.using_db_name, self.using_table_name, profiles
                    )
                    docid.append(retry_insert["_id"])
                    continue
        return docid

    def_create_space(
        self,
        dim: int = 1024,
    ) -> int:
"""
        Create Cluster VectorStore space.

        Args:
            dim:dimension of vector.

        Return:
            code,0 failed for ,1 for success.

        """
        type_dict = {"int": "integer", "str": "string", "float": "float"}
        space_config = {
            "name": self.using_table_name,
            "partition_num": 1,
            "replica_num": 1,
            "engine": {
                "index_size": 1,
                "retrieval_type": "HNSW",
                "retrieval_param": {
                    "metric_type": "InnerProduct",
                    "nlinks": -1,
                    "efConstruction": -1,
                },
            },
        }
        tmp_proer = {
            "ref_doc_id": {"type": "string"},
            "text": {"type": "string"},
            "text_embedding": {
                "type": "vector",
                "index": True,
                "dimension": dim,
                "store_type": "MemoryOnly",
            },
        }
        for item in self.field_list:
            tmp_proer[item["field"]] = {"type": type_dict[item["type"]]}
        space_config["properties"] = tmp_proer

        return self._vearch.create_space(self.using_db_name, space_config)

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
        if not self._vearch:
            raise ValueError("Vearch Engine is not initialized")

        embeddings = []
        metadatas = []
        ids = []
        texts = []
        for node in nodes:
            embeddings.append(node.get_embedding())
            metadatas.append(
                node_to_metadata_dict(
                    node, remove_text=True, flat_metadata=self.flat_metadata
                )
            )
            ids.append(node.node_id)
            texts.append(node.get_content(metadata_mode=MetadataMode.NONE) or "")

        return self._add_texts(
            ids=ids,
            texts=texts,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    defquery(
        self,
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query : vector store query.

        Returns:
            VectorStoreQueryResult: Query results.

        """
        meta_filters = {}
        if query.filters is not None:
            for filter_ in query.filters.legacy_filters():
                meta_filters[filter_.key] = filter_.value
        if self.flag:
            meta_field_list = self._vearch.get_space(
                self.using_db_name, self.using_table_name
            )
            meta_field_list.remove("text_embedding")
        embed = query.query_embedding
        if embed is None:
            raise ValueError("query.query_embedding is None")
        k = query.similarity_top_k
        query_data = {
            "query": {
                "sum": [
                    {
                        "field": "text_embedding",
                        "feature": (embed / np.linalg.norm(embed)).tolist(),
                    }
                ],
            },
            "retrieval_param": {"metric_type": "InnerProduct", "efSearch": 64},
            "size": k,
            "fields": meta_field_list,
        }
        query_result = self._vearch.search(
            self.using_db_name, self.using_table_name, query_data
        )
        res = query_result["hits"]["hits"]
        nodes = []
        similarities = []
        ids = []
        for item in res:
            content = ""
            meta_data = {}
            node_id = ""
            score = item["_score"]
            item = item["_source"]
            for item_key in item:
                if item_key == "text":
                    content = item[item_key]
                    continue
                elif item_key == "_id":
                    node_id = item[item_key]
                    ids.append(node_id)
                    continue
                meta_data[item_key] = item[item_key]
            similarities.append(score)
            try:
                node = metadata_dict_to_node(meta_data)
                node.set_content(content)
            except Exception:
                metadata, node_info, relationships = legacy_metadata_dict_to_node(
                    meta_data
                )
                node = TextNode(
                    text=content,
                    id_=node_id,
                    metadata=metadata,
                    start_char_idx=node_info.get("start", None),
                    end_char_idx=node_info.get("end", None),
                    relationships=relationships,
                )
            nodes.append(node)
        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

    def_delete(
        self,
        ids: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
"""
        Delete the documents which have the specified ids.

        Args:
            ids: The ids of the embedding vectors.
            **kwargs: Other keyword arguments that subclasses might use.

        Returns:
            Optional[bool]: True if deletion is successful.
            False otherwise, None if not implemented.

        """
        if ids is None or len(ids) == 0:
            return
        for _id in ids:
            queries = {
                "query": {
                    "filter": [{"term": {"ref_doc_id": [_id], "operator": "and"}}]
                },
                "size": 10000,
            }
            self._vearch.delete_by_query(
                self, self.using_db_name, self.using_table_name, queries
            )

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        Returns:
            None

        """
        if len(ref_doc_id) == 0:
            return
        ids: List[str] = []
        ids.append(ref_doc_id)
        self._delete(ids)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vearch/#llama_index.vector_stores.vearch.VearchVectorStore.client "Permanent link")

```
client: 

```

Get client.
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vearch/#llama_index.vector_stores.vearch.VearchVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query `  |  vector store query.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `VectorStoreQueryResult`  |   |  Query results.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vearch/llama_index/vector_stores/vearch/base.py`  
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
        query : vector store query.

    Returns:
        VectorStoreQueryResult: Query results.

    """
    meta_filters = {}
    if query.filters is not None:
        for filter_ in query.filters.legacy_filters():
            meta_filters[filter_.key] = filter_.value
    if self.flag:
        meta_field_list = self._vearch.get_space(
            self.using_db_name, self.using_table_name
        )
        meta_field_list.remove("text_embedding")
    embed = query.query_embedding
    if embed is None:
        raise ValueError("query.query_embedding is None")
    k = query.similarity_top_k
    query_data = {
        "query": {
            "sum": [
                {
                    "field": "text_embedding",
                    "feature": (embed / np.linalg.norm(embed)).tolist(),
                }
            ],
        },
        "retrieval_param": {"metric_type": "InnerProduct", "efSearch": 64},
        "size": k,
        "fields": meta_field_list,
    }
    query_result = self._vearch.search(
        self.using_db_name, self.using_table_name, query_data
    )
    res = query_result["hits"]["hits"]
    nodes = []
    similarities = []
    ids = []
    for item in res:
        content = ""
        meta_data = {}
        node_id = ""
        score = item["_score"]
        item = item["_source"]
        for item_key in item:
            if item_key == "text":
                content = item[item_key]
                continue
            elif item_key == "_id":
                node_id = item[item_key]
                ids.append(node_id)
                continue
            meta_data[item_key] = item[item_key]
        similarities.append(score)
        try:
            node = metadata_dict_to_node(meta_data)
            node.set_content(content)
        except Exception:
            metadata, node_info, relationships = legacy_metadata_dict_to_node(
                meta_data
            )
            node = TextNode(
                text=content,
                id_=node_id,
                metadata=metadata,
                start_char_idx=node_info.get("start", None),
                end_char_idx=node_info.get("end", None),
                relationships=relationships,
            )
        nodes.append(node)
    return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vearch/#llama_index.vector_stores.vearch.VearchVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `None`  |  None  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vearch/llama_index/vector_stores/vearch/base.py`  
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    Returns:
        None

    """
    if len(ref_doc_id) == 0:
        return
    ids: List[str] = []
    ids.append(ref_doc_id)
    self._delete(ids)

```
 |  
| --- | --- |  
options: members: - VearchVectorStore
