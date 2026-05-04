# Databricks
##  DatabricksVectorSearch [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/databricks/#llama_index.vector_stores.databricks.DatabricksVectorSearch "Permanent link")
Bases: 
Vector store for Databricks Vector Search.
Install `databricks-vectorsearch` package using the following in a Databricks notebook: %pip install databricks-vectorsearch dbutils.library.restartPython()
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-databricks/llama_index/vector_stores/databricks/base.py`  
| 
```
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
```
 | 
```
classDatabricksVectorSearch(BasePydanticVectorStore):
"""
    Vector store for Databricks Vector Search.

    Install ``databricks-vectorsearch`` package using the following in a Databricks notebook:
    %pip install databricks-vectorsearch
    dbutils.library.restartPython()

    """

    stores_text: bool = True
    text_column: Optional[str]
    columns: Optional[List[str]]

    _index: VectorSearchIndex = PrivateAttr()
    _primary_key: str = PrivateAttr()
    _index_type: str = PrivateAttr()
    _delta_sync_index_spec: dict = PrivateAttr()
    _direct_access_index_spec: dict = PrivateAttr()
    _doc_id_to_pk: dict = PrivateAttr()

    def__init__(
        self,
        index: VectorSearchIndex,
        text_column: Optional[str] = None,
        columns: Optional[List[str]] = None,
    ) -> None:
        super().__init__(text_column=text_column, columns=columns)

        try:
            fromdatabricks.vector_search.clientimport VectorSearchIndex
        except ImportError:
            raise ImportError(
                "`databricks-vectorsearch` package not found: "
                "please run `pip install databricks-vectorsearch`"
            )
        if not isinstance(index, VectorSearchIndex):
            raise TypeError(
                f"index must be of type `VectorSearchIndex`, not {type(index)}"
            )

        self._index = index

        # unpack the index spec
        index_description = _DatabricksIndexDescription.parse_obj(
            self._index.describe()
        )

        self._primary_key = index_description.primary_key
        self._index_type = index_description.index_type
        self._delta_sync_index_spec = index_description.delta_sync_index_spec
        self._direct_access_index_spec = index_description.direct_access_index_spec
        self._doc_id_to_pk = {}

        if columns is None:
            columns = []
        if "doc_id" not in columns:
            columns = columns[:19] + ["doc_id"]

        # initialize the column name for the text column in the delta table
        if self._is_databricks_managed_embeddings():
            index_source_column = self._embedding_source_column_name()

            # check if input text column matches the source column of the index
            if text_column is not None and text_column != index_source_column:
                raise ValueError(
                    f"text_column '{text_column}' does not match with the "
                    f"source column of the index: '{index_source_column}'."
                )

            self.text_column = index_source_column
        else:
            if text_column is None:
                raise ValueError("text_column is required for self-managed embeddings.")
            self.text_column = text_column

        # Fold primary key and text column into columns if they're not empty.
        columns_to_add = set(columns or [])
        columns_to_add.add(self._primary_key)
        columns_to_add.add(self.text_column)
        columns_to_add -= {"", None}

        self.columns = list(columns_to_add)

        # If the index schema is known, all our columns should be in that index.
        # Validate specified columns are in the index
        index_schema = self._index_schema()

        if self._is_direct_access_index() and index_schema:
            missing_columns = columns_to_add - set(index_schema.keys())

            if missing_columns:
                raise ValueError(
                    f"columns missing from schema: {', '.join(missing_columns)}"
                )

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
        if self._is_databricks_managed_embeddings():
            raise ValueError(
                "Adding nodes is not supported for Databricks-managed embeddings."
            )

        # construct the entries to upsert
        entries = []
        ids = []
        for node in nodes:
            node_id = node.node_id
            metadata = node_to_metadata_dict(node, remove_text=True, flat_metadata=True)

            metadata_columns = self.columns or []

            # explicitly record doc_id as metadata (for delete)
            if "doc_id" not in metadata_columns:
                metadata_columns.append("doc_id")

            entry = {
                self._primary_key: node_id,
                self.text_column: node.get_content(),
                self._embedding_vector_column_name(): node.get_embedding(),
                **{
                    col: metadata.get(col)
                    for col in filter(
                        lambda column: column
                        not in (self._primary_key, self.text_column),
                        metadata_columns,
                    )
                },
            }
            doc_id = metadata.get("doc_id")
            self._doc_id_to_pk[doc_id] = list(
                set(self._doc_id_to_pk.get(doc_id, []) + [node_id])  # noqa: RUF005
            )  # associate this node_id with this doc_id

            entries.append(entry)
            ids.append(node_id)

        # attempt the upsert
        upsert_resp = self._index.upsert(
            entries,
        )

        # return the successful IDs
        response_status = upsert_resp.get("status")

        failed_ids = (
            set(upsert_resp["result"]["failed_primary_keys"] or [])
            if "result" in upsert_resp
            and "failed_primary_keys" in upsert_resp["result"]
            else set()
        )

        if response_status not in ("PARTIAL_SUCCESS", "FAILURE") or not failed_ids:
            return ids

        elif response_status == "PARTIAL_SUCCESS":
            _logger.warning(
                "failed to add %d out of %d texts to the index",
                len(failed_ids),
                len(ids),
            )

        elif response_status == "FAILURE":
            _logger.error("failed to add all %d texts to the index", len(ids))

        return list(filter(lambda id_: id_ not in failed_ids, ids))

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        primary_keys = self._doc_id_to_pk.get(
            ref_doc_id, None
        )  # get the node_ids associated with the doc_id
        if primary_keys is not None:
            self._index.delete(
                primary_keys=primary_keys,
            )
            self._doc_id_to_pk.pop(
                ref_doc_id
            )  # remove this doc_id from the doc_id-to-node_id map

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query index for top k most similar nodes."""
        if self._is_databricks_managed_embeddings():
            query_text = query.query_str
            query_vector = None
        else:
            query_text = None
            query_vector = cast(List[float], query.query_embedding)

        if query.mode not in (
            VectorStoreQueryMode.DEFAULT,
            VectorStoreQueryMode.HYBRID,
        ):
            raise ValueError(
                "Only DEFAULT and HYBRID modes are supported for Databricks Vector Search."
            )

        if query.filters is not None:
            filters = _to_databricks_filter(query.filters)
        else:
            filters = None

        search_resp = self._index.similarity_search(
            columns=self.columns,
            query_text=query_text,
            query_vector=query_vector,
            filters=filters,
            num_results=query.similarity_top_k,
        )

        columns = [
            col["name"] for col in search_resp.get("manifest", {}).get("columns", [])
        ]
        top_k_nodes = []
        top_k_ids = []
        top_k_scores = []
        for result in search_resp.get("result", {}).get("data_array", []):
            doc_id = result[columns.index(self._primary_key)]
            text_content = result[columns.index(self.text_column)]
            metadata = {
                col: value
                for col, value in zip(columns[:-1], result[:-1])
                if col not in [self._primary_key, self.text_column]
            }
            metadata[self._primary_key] = doc_id
            score = result[-1]
            node = TextNode(
                text=text_content, id_=doc_id, metadata=metadata
            )  # TODO star_char, end_char, relationships? https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/vector_stores/llama-index-vector-stores-pinecone/llama_index/vector_stores/pinecone/base.py

            top_k_ids.append(doc_id)
            top_k_nodes.append(node)
            top_k_scores.append(score)

        return VectorStoreQueryResult(
            nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
        )

    @property
    defclient(self) -> Any:
"""Return VectorStoreIndex."""
        return self._index

    # The remaining utilities (and snippets of the above) are taken from
    # https://github.com/langchain-ai/langchain/blob/master/libs/community/langchain_community/vectorstores/databricks_vector_search.py
    def_index_schema(self) -> Optional[dict]:
"""
        Return the index schema as a dictionary.
        Return None if no schema found.
        """
        if self._is_direct_access_index():
            schema_json = self._direct_access_index_spec.get("schema_json")
            if schema_json is not None:
                return json.loads(schema_json)
        return None

    def_embedding_vector_column_name(self) -> Optional[str]:
"""
        Return the name of the embedding vector column.
        None if the index is not a self-managed embedding index.
        """
        return self._embedding_vector_column().get("name")

    def_embedding_vector_column(self) -> dict:
"""
        Return the embedding vector column configs as a dictionary.
        Empty if the index is not a self-managed embedding index.
        """
        index_spec = (
            self._delta_sync_index_spec
            if self._is_delta_sync_index()
            else self._direct_access_index_spec
        )
        return next(iter(index_spec.get("embedding_vector_columns") or []), {})

    def_embedding_source_column_name(self) -> Optional[str]:
"""
        Return the name of the embedding source column.
        None if the index is not a Databricks-managed embedding index.
        """
        return self._embedding_source_column().get("name")

    def_embedding_source_column(self) -> dict:
"""
        Return the embedding source column configs as a dictionary.
        Empty if the index is not a Databricks-managed embedding index.
        """
        return next(
            iter(self._delta_sync_index_spec.get("embedding_source_columns") or []),
            {},
        )

    def_is_delta_sync_index(self) -> bool:
"""Return True if the index is a delta-sync index."""
        return self._index_type == _DatabricksIndexType.DELTA_SYNC

    def_is_direct_access_index(self) -> bool:
"""Return True if the index is a direct-access index."""
        return self._index_type == _DatabricksIndexType.DIRECT_ACCESS

    def_is_databricks_managed_embeddings(self) -> bool:
"""Return True if the embeddings are managed by Databricks Vector Search."""
        return (
            self._is_delta_sync_index()
            and self._embedding_source_column_name() is not None
        )

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/databricks/#llama_index.vector_stores.databricks.DatabricksVectorSearch.client "Permanent link")

```
client: 

```

Return VectorStoreIndex.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/databricks/#llama_index.vector_stores.databricks.DatabricksVectorSearch.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-databricks/llama_index/vector_stores/databricks/base.py`  
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
    if self._is_databricks_managed_embeddings():
        raise ValueError(
            "Adding nodes is not supported for Databricks-managed embeddings."
        )

    # construct the entries to upsert
    entries = []
    ids = []
    for node in nodes:
        node_id = node.node_id
        metadata = node_to_metadata_dict(node, remove_text=True, flat_metadata=True)

        metadata_columns = self.columns or []

        # explicitly record doc_id as metadata (for delete)
        if "doc_id" not in metadata_columns:
            metadata_columns.append("doc_id")

        entry = {
            self._primary_key: node_id,
            self.text_column: node.get_content(),
            self._embedding_vector_column_name(): node.get_embedding(),
            **{
                col: metadata.get(col)
                for col in filter(
                    lambda column: column
                    not in (self._primary_key, self.text_column),
                    metadata_columns,
                )
            },
        }
        doc_id = metadata.get("doc_id")
        self._doc_id_to_pk[doc_id] = list(
            set(self._doc_id_to_pk.get(doc_id, []) + [node_id])  # noqa: RUF005
        )  # associate this node_id with this doc_id

        entries.append(entry)
        ids.append(node_id)

    # attempt the upsert
    upsert_resp = self._index.upsert(
        entries,
    )

    # return the successful IDs
    response_status = upsert_resp.get("status")

    failed_ids = (
        set(upsert_resp["result"]["failed_primary_keys"] or [])
        if "result" in upsert_resp
        and "failed_primary_keys" in upsert_resp["result"]
        else set()
    )

    if response_status not in ("PARTIAL_SUCCESS", "FAILURE") or not failed_ids:
        return ids

    elif response_status == "PARTIAL_SUCCESS":
        _logger.warning(
            "failed to add %d out of %d texts to the index",
            len(failed_ids),
            len(ids),
        )

    elif response_status == "FAILURE":
        _logger.error("failed to add all %d texts to the index", len(ids))

    return list(filter(lambda id_: id_ not in failed_ids, ids))

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/databricks/#llama_index.vector_stores.databricks.DatabricksVectorSearch.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-databricks/llama_index/vector_stores/databricks/base.py`  
| 
```
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    primary_keys = self._doc_id_to_pk.get(
        ref_doc_id, None
    )  # get the node_ids associated with the doc_id
    if primary_keys is not None:
        self._index.delete(
            primary_keys=primary_keys,
        )
        self._doc_id_to_pk.pop(
            ref_doc_id
        )  # remove this doc_id from the doc_id-to-node_id map

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/databricks/#llama_index.vector_stores.databricks.DatabricksVectorSearch.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-databricks/llama_index/vector_stores/databricks/base.py`  
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""Query index for top k most similar nodes."""
    if self._is_databricks_managed_embeddings():
        query_text = query.query_str
        query_vector = None
    else:
        query_text = None
        query_vector = cast(List[float], query.query_embedding)

    if query.mode not in (
        VectorStoreQueryMode.DEFAULT,
        VectorStoreQueryMode.HYBRID,
    ):
        raise ValueError(
            "Only DEFAULT and HYBRID modes are supported for Databricks Vector Search."
        )

    if query.filters is not None:
        filters = _to_databricks_filter(query.filters)
    else:
        filters = None

    search_resp = self._index.similarity_search(
        columns=self.columns,
        query_text=query_text,
        query_vector=query_vector,
        filters=filters,
        num_results=query.similarity_top_k,
    )

    columns = [
        col["name"] for col in search_resp.get("manifest", {}).get("columns", [])
    ]
    top_k_nodes = []
    top_k_ids = []
    top_k_scores = []
    for result in search_resp.get("result", {}).get("data_array", []):
        doc_id = result[columns.index(self._primary_key)]
        text_content = result[columns.index(self.text_column)]
        metadata = {
            col: value
            for col, value in zip(columns[:-1], result[:-1])
            if col not in [self._primary_key, self.text_column]
        }
        metadata[self._primary_key] = doc_id
        score = result[-1]
        node = TextNode(
            text=text_content, id_=doc_id, metadata=metadata
        )  # TODO star_char, end_char, relationships? https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/vector_stores/llama-index-vector-stores-pinecone/llama_index/vector_stores/pinecone/base.py

        top_k_ids.append(doc_id)
        top_k_nodes.append(node)
        top_k_scores.append(score)

    return VectorStoreQueryResult(
        nodes=top_k_nodes, similarities=top_k_scores, ids=top_k_ids
    )

```
 |  
| --- | --- |  
options: members: - DatabricksVectorSearch
