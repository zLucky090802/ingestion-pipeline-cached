# Alibabacloud opensearch
##  AlibabaCloudOpenSearchConfig [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_opensearch/#llama_index.vector_stores.alibabacloud_opensearch.AlibabaCloudOpenSearchConfig "Permanent link")
`Alibaba Cloud Opensearch` client configuration.
Attribute
endpoint (str) : The endpoint of opensearch instance, You can find it from the console of Alibaba Cloud OpenSearch. instance_id (str) : The identify of opensearch instance, You can find it from the console of Alibaba Cloud OpenSearch. username (str) : The username specified when purchasing the instance. password (str) : The password specified when purchasing the instance, After the instance is created, you can modify it on the console. tablename (str): The table name specified during instance configuration. namespace (str) : The instance data will be partitioned based on the "namespace" field. If the namespace is enabled, you need to specify the namespace field name during initialization, Otherwise, the queries cannot be executed correctly. field_mapping (dict[str, str]): The field mapping between llamaindex meta field and OpenSearch table filed name. OpenSearch has some rules for the field name, when the meta field name break the rules, can map to another name. output_fields (list[str]): Specify the field list returned when searching OpenSearch. id_field (str): The primary key field name in OpenSearch, default is `id`. embedding_field (list[float]): The field name which stored the embedding. text_field: The name of the field that stores the key text. search_config (dict, optional): The configuration used for searching the OpenSearch.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-alibabacloud-opensearch/llama_index/vector_stores/alibabacloud_opensearch/base.py`  
| 
```
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
classAlibabaCloudOpenSearchConfig:
"""
    `Alibaba Cloud Opensearch` client configuration.

    Attribute:
        endpoint (str) : The endpoint of opensearch instance, You can find it
         from the console of Alibaba Cloud OpenSearch.
        instance_id (str) : The identify of opensearch instance, You can find
         it from the console of Alibaba Cloud OpenSearch.
        username (str) : The username specified when purchasing the instance.
        password (str) : The password specified when purchasing the instance,
          After the instance is created, you can modify it on the console.
        tablename (str): The table name specified during instance configuration.
        namespace (str) : The instance data will be partitioned based on the "namespace"
         field. If the namespace is enabled, you need to specify the namespace field
         name during initialization, Otherwise, the queries cannot be executed
         correctly.
        field_mapping (dict[str, str]): The field mapping between llamaindex meta field
          and OpenSearch table filed name. OpenSearch has some rules for the field name,
          when the meta field name break the rules, can map to another name.
        output_fields (list[str]): Specify the field list returned when searching OpenSearch.
        id_field (str): The primary key field name in OpenSearch, default is `id`.
        embedding_field (list[float]): The field name which stored the embedding.
        text_field: The name of the field that stores the key text.
        search_config (dict, optional): The configuration used for searching the OpenSearch.

    """

    def__init__(
        self,
        endpoint: str,
        instance_id: str,
        username: str,
        password: str,
        table_name: str,
        namespace: str = "",
        field_mapping: Dict[str, str] = None,
        output_fields: Optional[List[str]] = None,
        id_field: str = "id",
        embedding_field: str = DEFAULT_EMBEDDING_KEY,
        text_field: str = DEFAULT_TEXT_KEY,
        search_config: dict = None,
    ) -> None:
        self.endpoint = endpoint
        self.instance_id = instance_id
        self.username = username
        self.password = password
        self.namespace = namespace
        self.table_name = table_name
        self.data_source_name = f"{self.instance_id}_{self.table_name}"
        self.field_mapping = field_mapping
        self.id_field = id_field
        self.embedding_field = embedding_field
        self.text_field = text_field
        self.search_config = search_config
        self.output_fields = output_fields

        if self.output_fields is None:
            self.output_fields = (
                list(self.field_mapping.values()) if self.field_mapping else []
            )
        if self.text_field not in self.output_fields:
            self.output_fields.append(self.text_field)

        self.inverse_field_mapping: Dict[str, str] = (
            {value: key for key, value in self.field_mapping.items()}
            if self.field_mapping
            else {}
        )

    def__getitem__(self, item: str) -> Any:
        return getattr(self, item)

```
 |  
| --- | --- |  
##  AlibabaCloudOpenSearchStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_opensearch/#llama_index.vector_stores.alibabacloud_opensearch.AlibabaCloudOpenSearchStore "Permanent link")
Bases: 
The AlibabaCloud OpenSearch Vector Store.
In this vector store we store the text, its embedding and its metadata in a OpenSearch table.
In order to use this you need to have a instance and configure a table. See the following documentation for details: https://help.aliyun.com/zh/open-search/vector-search-edition/product-overview
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `config`  |   |  The instance configuration  |  _required_  |  
Examples:
`pip install llama-index-vector-stores-alibabacloud_opensearch`

```
fromllama_index.vector_stores.alibabacloud_opensearchimport (
    AlibabaCloudOpenSearchConfig,
    AlibabaCloudOpenSearchStore,
)

# Config
config = AlibabaCloudOpenSearchConfig(
    endpoint="xxx",
    instance_id="ha-cn-******",
    username="****",
    password="****",
    table_name="your_table_name",
)

vector_store = AlibabaCloudOpenSearchStore(config)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-alibabacloud-opensearch/llama_index/vector_stores/alibabacloud_opensearch/base.py`  
| 
```
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
```
 | 
```
classAlibabaCloudOpenSearchStore(BasePydanticVectorStore):
"""
    The AlibabaCloud OpenSearch Vector Store.

    In this vector store we store the text, its embedding and its metadata
    in a OpenSearch table.

    In order to use this you need to have a instance and configure a table.
    See the following documentation for details:
    https://help.aliyun.com/zh/open-search/vector-search-edition/product-overview

    Args:
        config (AlibabaCloudOpenSearchConfig): The instance configuration

    Examples:
        `pip install llama-index-vector-stores-alibabacloud_opensearch`

        ```python
        from llama_index.vector_stores.alibabacloud_opensearch import (
            AlibabaCloudOpenSearchConfig,
            AlibabaCloudOpenSearchStore,


        # Config
        config = AlibabaCloudOpenSearchConfig(
            endpoint="xxx",
            instance_id="ha-cn-******",
            username="****",
            password="****",
            table_name="your_table_name",


        vector_store = AlibabaCloudOpenSearchStore(config)
        ```

    """

    stores_text: bool = True
    flat_metadata: bool = True

    _client: Any = PrivateAttr()
    _config: AlibabaCloudOpenSearchConfig = PrivateAttr()

    def__init__(self, config: AlibabaCloudOpenSearchConfig) -> None:
"""Initialize params."""
        super().__init__()

        self._config = config
        self._client = client.Client(
            models.Config(
                endpoint=config.endpoint,
                instance_id=config.instance_id,
                access_user_name=config.username,
                access_pass_word=config.password,
            )
        )

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "AlibabaCloudOpenSearchStore"

    @property
    defclient(self) -> Any:
"""Get client."""
        return self._client

    defadd(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to vector store.

        Args:
            nodes (List[BaseNode]): list of nodes with embeddings

        """
        return asyncio.get_event_loop().run_until_complete(
            self.async_add(nodes, **add_kwargs)
        )

    async defasync_add(
        self,
        nodes: List[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Asynchronously add nodes with embedding to vector store.

        Args:
            nodes (List[BaseNode]): list of nodes with embeddings

        """
        for i in range(0, len(nodes), DEFAULT_BATCH_SIZE):
            docs = []
            for node in nodes[i:DEFAULT_BATCH_SIZE]:
                doc = {
                    self._config.id_field: node.node_id,
                    self._config.embedding_field: node.embedding,
                }
                if self._config.text_field:
                    doc[self._config.text_field] = node.get_text()

                meta_fields = node_to_metadata_dict(
                    node, remove_text=False, flat_metadata=self.flat_metadata
                )

                if self._config.field_mapping:
                    for key, value in meta_fields.items():
                        doc[self._config.field_mapping.get(key, key)] = value
                else:
                    doc.update(meta_fields)
                docs.append(doc)

            try:
                await self._async_send_data("add", docs)
            except Exception as e:
                logging.error(f"Add to {self._config.instance_id} failed: {e}")
                raise RuntimeError(f"Fail to add docs, error:{e}")
        return [node.node_id for node in nodes]

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        return asyncio.get_event_loop().run_until_complete(
            self.adelete(ref_doc_id, **delete_kwargs)
        )

    async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Asynchronously delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        filter = f"{DEFAULT_DOC_ID_KEY}='{ref_doc_id}'"
        request = models.FetchRequest(table_name=self._config.table_name, filter=filter)

        response = self._client.fetch(request)
        json_response = json.loads(response.body)
        err_msg = json_response.get("errorMsg", None)
        if err_msg:
            raise RuntimeError(f"Failed to query doc by {filter}: {err_msg}")

        docs = []
        for doc in json_response["result"]:
            docs.append({"id": doc["id"]})
        await self._async_send_data("delete", docs)

    async def_async_send_data(self, cmd: str, fields_list: List[dict]) -> None:
"""
        Asynchronously send data.

        Args:
            cmd (str): data operator, add: upsert the doc, delete: delete the doc
            fields_list (list[dict]): doc fields list

        """
        docs = []
        for fields in fields_list:
            docs.append({"cmd": cmd, "fields": fields})
        request = models.PushDocumentsRequest({}, docs)
        await self._client.push_documents_async(
            self._config.data_source_name, self._config.id_field, request
        )

    defquery(
        self,
        query: VectorStoreQuery,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""Query vector store."""
        return asyncio.get_event_loop().run_until_complete(self.aquery(query, **kwargs))

    async defaquery(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> VectorStoreQueryResult:
"""
        Asynchronously query vector store.
        """
        if query.mode != VectorStoreQueryMode.DEFAULT:
            raise ValueError(
                f"Alibaba Cloud OpenSearch does not support {query.mode} yet."
            )

        request = self._gen_query_request(query)
        response = await self._client.query_async(request)
        json_response = json.loads(response.body)
        logging.debug(f"query result: {json_response}")

        err_msg = json_response.get("errorMsg", None)
        if err_msg:
            raise RuntimeError(
                f"query doc from Alibaba Cloud OpenSearch instance:{self._config.instance_id} failed:"
                f"{err_msg}"
            )

        ids = []
        nodes = []
        similarities = []
        for doc in json_response["result"]:
            try:
                node = metadata_dict_to_node(
                    {
                        "_node_content": doc["fields"].get(
                            self._config.field_mapping.get(
                                "_node_content", "_node_content"
                            ),
                            None,
                        ),
                        "_node_type": doc["fields"].get(
                            self._config.field_mapping.get("_node_type", "_node_type"),
                            None,
                        ),
                    }
                )
            except Exception:
                text = doc["fields"][self._config.text_field]
                metadata = {
                    self._config.inverse_field_mapping.get(key, key): doc["fields"].get(
                        key
                    )
                    for key in self._config.output_fields
                }
                node = TextNode(id_=doc["id"], text=text, metadata=metadata)

            ids.append(doc["id"])
            nodes.append(node)
            similarities.append(doc["score"])

        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

    def_gen_query_request(self, query: VectorStoreQuery) -> models.QueryRequest:
"""
        Generate the OpenSearch query request.

        Args:
            query (VectorStoreQuery): The vector store query

        Return:
            OpenSearch query request

        """
        filter = _to_ha3_engine_filter(query.filters)
        request = models.QueryRequest(
            table_name=self._config.table_name,
            namespace=self._config.namespace,
            vector=query.query_embedding,
            top_k=query.similarity_top_k,
            filter=filter,
            include_vector=True,
            output_fields=self._config.output_fields,
        )

        if self._config.search_config:
            request.order = self._config.search_config.get("order", "ASC")
            score_threshold: float = self._config.search_config.get(
                "score_threshold", None
            )
            if score_threshold is not None:
                request.score_threshold = score_threshold
            search_params = self._config.search_config.get("search_params", None)
            if search_params is not None:
                request.search_params = json.dumps(search_params)
        return request

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_opensearch/#llama_index.vector_stores.alibabacloud_opensearch.AlibabaCloudOpenSearchStore.client "Permanent link")

```
client: 

```

Get client.
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_opensearch/#llama_index.vector_stores.alibabacloud_opensearch.AlibabaCloudOpenSearchStore.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-alibabacloud-opensearch/llama_index/vector_stores/alibabacloud_opensearch/base.py`  
| 
```
211
212
213
214
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "AlibabaCloudOpenSearchStore"

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_opensearch/#llama_index.vector_stores.alibabacloud_opensearch.AlibabaCloudOpenSearchStore.add "Permanent link")

```
add(nodes: [], **add_kwargs: ) -> []

```

Add nodes to vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-alibabacloud-opensearch/llama_index/vector_stores/alibabacloud_opensearch/base.py`  
| 
```
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
```
 | 
```
defadd(
    self,
    nodes: List[BaseNode],
    **add_kwargs: Any,
) -> List[str]:
"""
    Add nodes to vector store.

    Args:
        nodes (List[BaseNode]): list of nodes with embeddings

    """
    return asyncio.get_event_loop().run_until_complete(
        self.async_add(nodes, **add_kwargs)
    )

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_opensearch/#llama_index.vector_stores.alibabacloud_opensearch.AlibabaCloudOpenSearchStore.async_add "Permanent link")

```
async_add(
    nodes: [], **add_kwargs: 
) -> []

```

Asynchronously add nodes with embedding to vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-alibabacloud-opensearch/llama_index/vector_stores/alibabacloud_opensearch/base.py`  
| 
```
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
```
 | 
```
async defasync_add(
    self,
    nodes: List[BaseNode],
    **add_kwargs: Any,
) -> List[str]:
"""
    Asynchronously add nodes with embedding to vector store.

    Args:
        nodes (List[BaseNode]): list of nodes with embeddings

    """
    for i in range(0, len(nodes), DEFAULT_BATCH_SIZE):
        docs = []
        for node in nodes[i:DEFAULT_BATCH_SIZE]:
            doc = {
                self._config.id_field: node.node_id,
                self._config.embedding_field: node.embedding,
            }
            if self._config.text_field:
                doc[self._config.text_field] = node.get_text()

            meta_fields = node_to_metadata_dict(
                node, remove_text=False, flat_metadata=self.flat_metadata
            )

            if self._config.field_mapping:
                for key, value in meta_fields.items():
                    doc[self._config.field_mapping.get(key, key)] = value
            else:
                doc.update(meta_fields)
            docs.append(doc)

        try:
            await self._async_send_data("add", docs)
        except Exception as e:
            logging.error(f"Add to {self._config.instance_id} failed: {e}")
            raise RuntimeError(f"Fail to add docs, error:{e}")
    return [node.node_id for node in nodes]

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_opensearch/#llama_index.vector_stores.alibabacloud_opensearch.AlibabaCloudOpenSearchStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-alibabacloud-opensearch/llama_index/vector_stores/alibabacloud_opensearch/base.py`  
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
```
 | 
```
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    return asyncio.get_event_loop().run_until_complete(
        self.adelete(ref_doc_id, **delete_kwargs)
    )

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_opensearch/#llama_index.vector_stores.alibabacloud_opensearch.AlibabaCloudOpenSearchStore.adelete "Permanent link")

```
adelete(ref_doc_id: , **delete_kwargs: ) -> None

```

Asynchronously delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-alibabacloud-opensearch/llama_index/vector_stores/alibabacloud_opensearch/base.py`  
| 
```
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
async defadelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Asynchronously delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    filter = f"{DEFAULT_DOC_ID_KEY}='{ref_doc_id}'"
    request = models.FetchRequest(table_name=self._config.table_name, filter=filter)

    response = self._client.fetch(request)
    json_response = json.loads(response.body)
    err_msg = json_response.get("errorMsg", None)
    if err_msg:
        raise RuntimeError(f"Failed to query doc by {filter}: {err_msg}")

    docs = []
    for doc in json_response["result"]:
        docs.append({"id": doc["id"]})
    await self._async_send_data("delete", docs)

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_opensearch/#llama_index.vector_stores.alibabacloud_opensearch.AlibabaCloudOpenSearchStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-alibabacloud-opensearch/llama_index/vector_stores/alibabacloud_opensearch/base.py`  
| 
```
328
329
330
331
332
333
334
```
 | 
```
defquery(
    self,
    query: VectorStoreQuery,
    **kwargs: Any,
) -> VectorStoreQueryResult:
"""Query vector store."""
    return asyncio.get_event_loop().run_until_complete(self.aquery(query, **kwargs))

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/alibabacloud_opensearch/#llama_index.vector_stores.alibabacloud_opensearch.AlibabaCloudOpenSearchStore.aquery "Permanent link")

```
aquery(
    query: , **kwargs: 
) -> 

```

Asynchronously query vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-alibabacloud-opensearch/llama_index/vector_stores/alibabacloud_opensearch/base.py`  
| 
```
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
```
 | 
```
async defaquery(
    self, query: VectorStoreQuery, **kwargs: Any
) -> VectorStoreQueryResult:
"""
    Asynchronously query vector store.
    """
    if query.mode != VectorStoreQueryMode.DEFAULT:
        raise ValueError(
            f"Alibaba Cloud OpenSearch does not support {query.mode} yet."
        )

    request = self._gen_query_request(query)
    response = await self._client.query_async(request)
    json_response = json.loads(response.body)
    logging.debug(f"query result: {json_response}")

    err_msg = json_response.get("errorMsg", None)
    if err_msg:
        raise RuntimeError(
            f"query doc from Alibaba Cloud OpenSearch instance:{self._config.instance_id} failed:"
            f"{err_msg}"
        )

    ids = []
    nodes = []
    similarities = []
    for doc in json_response["result"]:
        try:
            node = metadata_dict_to_node(
                {
                    "_node_content": doc["fields"].get(
                        self._config.field_mapping.get(
                            "_node_content", "_node_content"
                        ),
                        None,
                    ),
                    "_node_type": doc["fields"].get(
                        self._config.field_mapping.get("_node_type", "_node_type"),
                        None,
                    ),
                }
            )
        except Exception:
            text = doc["fields"][self._config.text_field]
            metadata = {
                self._config.inverse_field_mapping.get(key, key): doc["fields"].get(
                    key
                )
                for key in self._config.output_fields
            }
            node = TextNode(id_=doc["id"], text=text, metadata=metadata)

        ids.append(doc["id"])
        nodes.append(node)
        similarities.append(doc["score"])

    return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

```
 |  
| --- | --- |  
options: members: - AlibabaCloudOpenSearch
