# Rocksetdb
##  RocksetVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/rocksetdb/#llama_index.vector_stores.rocksetdb.RocksetVectorStore "Permanent link")
Bases: 
Rockset Vector Store.
Examples:
`pip install llama-index-vector-stores-rocksetdb`

```
fromllama_index.vector_stores.rocksetdbimport RocksetVectorStore

# Set up RocksetVectorStore with necessary configurations
vector_store = RocksetVectorStore(
    collection="my_collection",
    api_key="your_rockset_api_key",
    api_server="https://api.use1a1.rockset.com",
    embedding_col="my_embedding",
    metadata_col="node",
    distance_func=RocksetVectorStore.DistanceFunc.DOT_PRODUCT
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-rocksetdb/llama_index/vector_stores/rocksetdb/base.py`  
| 
```
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
```
 | 
```
classRocksetVectorStore(BasePydanticVectorStore):
"""
    Rockset Vector Store.

    Examples:
        `pip install llama-index-vector-stores-rocksetdb`

        ```python
        from llama_index.vector_stores.rocksetdb import RocksetVectorStore

        # Set up RocksetVectorStore with necessary configurations
        vector_store = RocksetVectorStore(
            collection="my_collection",
            api_key="your_rockset_api_key",
            api_server="https://api.use1a1.rockset.com",
            embedding_col="my_embedding",
            metadata_col="node",
            distance_func=RocksetVectorStore.DistanceFunc.DOT_PRODUCT

        ```

    """

    stores_text: bool = True
    is_embedding_query: bool = True
    flat_metadata: bool = False

    classDistanceFunc(Enum):
        COSINE_SIM = "COSINE_SIM"
        EUCLIDEAN_DIST = "EUCLIDEAN_DIST"
        DOT_PRODUCT = "DOT_PRODUCT"

    rockset: ModuleType
    rs: Any
    workspace: str
    collection: str
    text_key: str
    embedding_col: str
    metadata_col: str
    distance_func: DistanceFunc
    distance_order: str

    def__init__(
        self,
        collection: str,
        client: Any | None = None,
        text_key: str = DEFAULT_TEXT_KEY,
        embedding_col: str = DEFAULT_EMBEDDING_KEY,
        metadata_col: str = "metadata",
        workspace: str = "commons",
        api_server: str | None = None,
        api_key: str | None = None,
        distance_func: DistanceFunc = DistanceFunc.COSINE_SIM,
    ) -> None:
"""
        Rockset Vector Store Data container.

        Args:
            collection (str): The name of the collection of vectors
            client (Optional[Any]): Rockset client object
            text_key (str): The key to the text of nodes
                (default: llama_index.core.vector_stores.utils.DEFAULT_TEXT_KEY)
            embedding_col (str): The DB column containing embeddings
                (default: llama_index.core.vector_stores.utils.DEFAULT_EMBEDDING_KEY))
            metadata_col (str): The DB column containing node metadata
                (default: "metadata")
            workspace (str): The workspace containing the collection of vectors
                (default: "commons")
            api_server (Optional[str]): The Rockset API server to use
            api_key (Optional[str]): The Rockset API key to use
            distance_func (RocksetVectorStore.DistanceFunc): The metric to measure
                vector relationship
                (default: RocksetVectorStore.DistanceFunc.COSINE_SIM)

        """
        super().__init__(
            rockset=_get_rockset(),
            rs=_get_client(api_key, api_server, client),
            collection=collection,
            text_key=text_key,
            embedding_col=embedding_col,
            metadata_col=metadata_col,
            workspace=workspace,
            distance_func=distance_func,
            distance_order=(
                "ASC" if distance_func is distance_func.EUCLIDEAN_DIST else "DESC"
            ),
        )

        try:
            self.rs.set_application("llama_index")
        except AttributeError:
            # set_application method does not exist.
            # rockset version < 2.1.0
            pass

    @classmethod
    defclass_name(cls) -> str:
        return "RocksetVectorStore"

    @property
    defclient(self) -> Any:
        return self.rs

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
        Stores vectors in the collection.

        Args:
            nodes (List[BaseNode]): List of nodes with embeddings

        Returns:
            Stored node IDs (List[str])

        """
        return [
            row["_id"]
            for row in self.rs.Documents.add_documents(
                collection=self.collection,
                workspace=self.workspace,
                data=[
                    {
                        self.embedding_col: node.get_embedding(),
                        "_id": node.node_id,
                        self.metadata_col: node_to_metadata_dict(
                            node, text_field=self.text_key
                        ),
                    }
                    for node in nodes
                ],
            ).data
        ]

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Deletes nodes stored in the collection by their ref_doc_id.

        Args:
            ref_doc_id (str): The ref_doc_id of the document
                whose nodes are to be deleted

        """
        self.rs.Documents.delete_documents(
            collection=self.collection,
            workspace=self.workspace,
            data=[
                self.rockset.models.DeleteDocumentsRequestData(id=row["_id"])
                for row in self.rs.sql(
                    f"""
                        SELECT


{self.workspace}"."{self.collection}" x
                        WHERE
{self.metadata_col}.ref_doc_id=:ref_doc_id
,
                    params={"ref_doc_id": ref_doc_id},
                ).results
            ],
        )

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Gets nodes relevant to a query.

        Args:
            query (llama_index.core.vector_stores.types.VectorStoreQuery): The query
            similarity_col (Optional[str]): The column to select the cosine
                similarity as (default: "_similarity")

        Returns:
            query results (llama_index.core.vector_stores.types.VectorStoreQueryResult)

        """
        similarity_col = kwargs.get("similarity_col", "_similarity")
        res = self.rs.sql(
            f"""
                SELECT
                    _id,
{self.metadata_col}
{
f''', {self.distance_func.value}(
{query.query_embedding},
{self.embedding_col}

{similarity_col}'''
ifquery.query_embedding
else""
}
                FROM
{self.workspace}"."{self.collection}" x
{
"WHERE"
ifquery.node_ids
or(query.filtersandlen(query.filters.legacy_filters())0)
else""
}{
f'''({
" OR ".join([f"_id='{node_id}'"fornode_idinquery.node_ids])
})'''
ifquery.node_ids
else""
}{
f''' {"AND"ifquery.node_idselse""} ({
" AND ".join(
[
f"x.{self.metadata_col}.{filter.key}=:{filter.key}"
forfilterinquery.filters.legacy_filters()
]
)
})'''
ifquery.filters
else""
}
                ORDER BY
{similarity_col}{self.distance_order}
                LIMIT
{query.similarity_top_k}
,
            params=(
                {filter.key: filter.value for filter in query.filters.legacy_filters()}
                if query.filters
                else {}
            ),
        )

        similarities: List[float] | None = [] if query.query_embedding else None
        nodes, ids = [], []
        for row in res.results:
            if similarities is not None:
                similarities.append(row[similarity_col])
            nodes.append(metadata_dict_to_node(row[self.metadata_col]))
            ids.append(row["_id"])

        return VectorStoreQueryResult(similarities=similarities, nodes=nodes, ids=ids)

    @classmethod
    defwith_new_collection(
        cls: Type[T], dimensions: int | None = None, **rockset_vector_store_args: Any
    ) -> RocksetVectorStore:
"""
        Creates a new collection and returns its RocksetVectorStore.

        Args:
            dimensions (Optional[int]): The length of the vectors to enforce
                in the collection's ingest transformation. By default, the
                collection will do no vector enforcement.
            collection (str): The name of the collection to be created
            client (Optional[Any]): Rockset client object
            workspace (str): The workspace containing the collection to be
                created (default: "commons")
            text_key (str): The key to the text of nodes
                (default: llama_index.core.vector_stores.utils.DEFAULT_TEXT_KEY)
            embedding_col (str): The DB column containing embeddings
                (default: llama_index.core.vector_stores.utils.DEFAULT_EMBEDDING_KEY))
            metadata_col (str): The DB column containing node metadata
                (default: "metadata")
            api_server (Optional[str]): The Rockset API server to use
            api_key (Optional[str]): The Rockset API key to use
            distance_func (RocksetVectorStore.DistanceFunc): The metric to measure
                vector relationship
                (default: RocksetVectorStore.DistanceFunc.COSINE_SIM)

        """
        client = rockset_vector_store_args["client"] = _get_client(
            api_key=rockset_vector_store_args.get("api_key"),
            api_server=rockset_vector_store_args.get("api_server"),
            client=rockset_vector_store_args.get("client"),
        )
        collection_args = {
            "workspace": rockset_vector_store_args.get("workspace", "commons"),
            "name": rockset_vector_store_args.get("collection"),
        }
        embeddings_col = rockset_vector_store_args.get(
            "embeddings_col", DEFAULT_EMBEDDING_KEY
        )
        if dimensions:
            collection_args["field_mapping_query"] = (
                _get_rockset().model.field_mapping_query.FieldMappingQuery(
                    sql=f"""
                    SELECT
                        *, VECTOR_ENFORCE(
{embeddings_col},
{dimensions},
                            'float'
{embeddings_col}
                    FROM
                        _input

                )
            )

        client.Collections.create_s3_collection(**collection_args)  # create collection
        while (
            client.Collections.get(
                collection=rockset_vector_store_args.get("collection")
            ).data.status
            != "READY"
        ):  # wait until collection is ready
            sleep(0.1)
            # TODO: add async, non-blocking method collection creation

        return cls(
            **dict(
                filter(  # filter out None args
                    lambda arg: arg[1] is not None, rockset_vector_store_args.items()
                )
            )
        )

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/rocksetdb/#llama_index.vector_stores.rocksetdb.RocksetVectorStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Stores vectors in the collection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes with embeddings  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  Stored node IDs (List[str])  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-rocksetdb/llama_index/vector_stores/rocksetdb/base.py`  
| 
```
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
defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
"""
    Stores vectors in the collection.

    Args:
        nodes (List[BaseNode]): List of nodes with embeddings

    Returns:
        Stored node IDs (List[str])

    """
    return [
        row["_id"]
        for row in self.rs.Documents.add_documents(
            collection=self.collection,
            workspace=self.workspace,
            data=[
                {
                    self.embedding_col: node.get_embedding(),
                    "_id": node.node_id,
                    self.metadata_col: node_to_metadata_dict(
                        node, text_field=self.text_key
                    ),
                }
                for node in nodes
            ],
        ).data
    ]

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/rocksetdb/#llama_index.vector_stores.rocksetdb.RocksetVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Deletes nodes stored in the collection by their ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The ref_doc_id of the document whose nodes are to be deleted  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-rocksetdb/llama_index/vector_stores/rocksetdb/base.py`  
| 
```
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
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Deletes nodes stored in the collection by their ref_doc_id.

    Args:
        ref_doc_id (str): The ref_doc_id of the document
            whose nodes are to be deleted

    """
    self.rs.Documents.delete_documents(
        collection=self.collection,
        workspace=self.workspace,
        data=[
            self.rockset.models.DeleteDocumentsRequestData(id=row["_id"])
            for row in self.rs.sql(
                f"""
                    SELECT

                    FROM
{self.workspace}"."{self.collection}" x
                    WHERE
{self.metadata_col}.ref_doc_id=:ref_doc_id
,
                params={"ref_doc_id": ref_doc_id},
            ).results
        ],
    )

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/rocksetdb/#llama_index.vector_stores.rocksetdb.RocksetVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Gets nodes relevant to a query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  The query  |  _required_  |  
|  `similarity_col`  |  `Optional[str]`  |  The column to select the cosine similarity as (default: "_similarity")  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  query results (llama_index.core.vector_stores.types.VectorStoreQueryResult)  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-rocksetdb/llama_index/vector_stores/rocksetdb/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Gets nodes relevant to a query.

    Args:
        query (llama_index.core.vector_stores.types.VectorStoreQuery): The query
        similarity_col (Optional[str]): The column to select the cosine
            similarity as (default: "_similarity")

    Returns:
        query results (llama_index.core.vector_stores.types.VectorStoreQueryResult)

    """
    similarity_col = kwargs.get("similarity_col", "_similarity")
    res = self.rs.sql(
        f"""
            SELECT
                _id,
{self.metadata_col}
{
f''', {self.distance_func.value}(
{query.query_embedding},
{self.embedding_col}

{similarity_col}'''
ifquery.query_embedding
else""
}
            FROM
{self.workspace}"."{self.collection}" x
{
"WHERE"
ifquery.node_ids
or(query.filtersandlen(query.filters.legacy_filters())0)
else""
}{
f'''({
" OR ".join([f"_id='{node_id}'"fornode_idinquery.node_ids])
})'''
ifquery.node_ids
else""
}{
f''' {"AND"ifquery.node_idselse""} ({
" AND ".join(
[
f"x.{self.metadata_col}.{filter.key}=:{filter.key}"
forfilterinquery.filters.legacy_filters()
]
)
})'''
ifquery.filters
else""
}
            ORDER BY
{similarity_col}{self.distance_order}
            LIMIT
{query.similarity_top_k}
        """,
        params=(
            {filter.key: filter.value for filter in query.filters.legacy_filters()}
            if query.filters
            else {}
        ),
    )

    similarities: List[float] | None = [] if query.query_embedding else None
    nodes, ids = [], []
    for row in res.results:
        if similarities is not None:
            similarities.append(row[similarity_col])
        nodes.append(metadata_dict_to_node(row[self.metadata_col]))
        ids.append(row["_id"])

    return VectorStoreQueryResult(similarities=similarities, nodes=nodes, ids=ids)

```
 |  
| --- | --- |  
###  with_new_collection `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/rocksetdb/#llama_index.vector_stores.rocksetdb.RocksetVectorStore.with_new_collection "Permanent link")

```
with_new_collection(
    dimensions:  | None = None,
    **rockset_vector_store_args: 
) -> 

```

Creates a new collection and returns its RocksetVectorStore.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `dimensions`  |  `Optional[int]`  |  The length of the vectors to enforce in the collection's ingest transformation. By default, the collection will do no vector enforcement.  |  `None`  |  
|  `collection`  |  The name of the collection to be created  |  _required_  |  
|  `client`  |  `Optional[Any]`  |  Rockset client object  |  _required_  |  
|  `workspace`  |  The workspace containing the collection to be created (default: "commons")  |  _required_  |  
|  `text_key`  |  The key to the text of nodes (default: llama_index.core.vector_stores.utils.DEFAULT_TEXT_KEY)  |  _required_  |  
|  `embedding_col`  |  The DB column containing embeddings (default: llama_index.core.vector_stores.utils.DEFAULT_EMBEDDING_KEY))  |  _required_  |  
|  `metadata_col`  |  The DB column containing node metadata (default: "metadata")  |  _required_  |  
|  `api_server`  |  `Optional[str]`  |  The Rockset API server to use  |  _required_  |  
|  `api_key`  |  `Optional[str]`  |  The Rockset API key to use  |  _required_  |  
|  `distance_func`  |  `DistanceFunc`  |  The metric to measure vector relationship (default: RocksetVectorStore.DistanceFunc.COSINE_SIM)  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-rocksetdb/llama_index/vector_stores/rocksetdb/base.py`  
| 
```
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
```
 | 
```
@classmethod
defwith_new_collection(
    cls: Type[T], dimensions: int | None = None, **rockset_vector_store_args: Any
) -> RocksetVectorStore:
"""
    Creates a new collection and returns its RocksetVectorStore.

    Args:
        dimensions (Optional[int]): The length of the vectors to enforce
            in the collection's ingest transformation. By default, the
            collection will do no vector enforcement.
        collection (str): The name of the collection to be created
        client (Optional[Any]): Rockset client object
        workspace (str): The workspace containing the collection to be
            created (default: "commons")
        text_key (str): The key to the text of nodes
            (default: llama_index.core.vector_stores.utils.DEFAULT_TEXT_KEY)
        embedding_col (str): The DB column containing embeddings
            (default: llama_index.core.vector_stores.utils.DEFAULT_EMBEDDING_KEY))
        metadata_col (str): The DB column containing node metadata
            (default: "metadata")
        api_server (Optional[str]): The Rockset API server to use
        api_key (Optional[str]): The Rockset API key to use
        distance_func (RocksetVectorStore.DistanceFunc): The metric to measure
            vector relationship
            (default: RocksetVectorStore.DistanceFunc.COSINE_SIM)

    """
    client = rockset_vector_store_args["client"] = _get_client(
        api_key=rockset_vector_store_args.get("api_key"),
        api_server=rockset_vector_store_args.get("api_server"),
        client=rockset_vector_store_args.get("client"),
    )
    collection_args = {
        "workspace": rockset_vector_store_args.get("workspace", "commons"),
        "name": rockset_vector_store_args.get("collection"),
    }
    embeddings_col = rockset_vector_store_args.get(
        "embeddings_col", DEFAULT_EMBEDDING_KEY
    )
    if dimensions:
        collection_args["field_mapping_query"] = (
            _get_rockset().model.field_mapping_query.FieldMappingQuery(
                sql=f"""
                SELECT
                    *, VECTOR_ENFORCE(
{embeddings_col},
{dimensions},
                        'float'
                    ) AS {embeddings_col}
                FROM
                    _input

            )
        )

    client.Collections.create_s3_collection(**collection_args)  # create collection
    while (
        client.Collections.get(
            collection=rockset_vector_store_args.get("collection")
        ).data.status
        != "READY"
    ):  # wait until collection is ready
        sleep(0.1)
        # TODO: add async, non-blocking method collection creation

    return cls(
        **dict(
            filter(  # filter out None args
                lambda arg: arg[1] is not None, rockset_vector_store_args.items()
            )
        )
    )

```
 |  
| --- | --- |  
options: members: - RocksetVectorStore
