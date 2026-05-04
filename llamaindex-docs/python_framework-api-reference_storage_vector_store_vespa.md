# Vespa
##  VespaVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vespa/#llama_index.vector_stores.vespa.VespaVectorStore "Permanent link")
Bases: 
Vespa vector store.
Can be initialized in several ways: 1. (Default) Initialize Vespa vector store with default hybrid template and local (docker) deployment. 2. Initialize by providing an application package created in pyvespa (can be deployed locally or to Vespa cloud). 3. Initialize from previously deployed Vespa application by providing URL. (Local or cloud deployment).
The application must be set up with the following fields: - id: Document id - text: Text field - embedding: Field to store embedding vectors. - metadata: Metadata field (all metadata will be stored here)
The application must be set up with the following rank profiles: - bm25: For text search - semantic: For semantic search - fusion: For semantic hybrid search
When creating a VectorStoreIndex from VespaVectorStore, the index will add documents to the Vespa application. Be ware that the Vespa container will be reused if not deleted between deployments, to avoid data duplication. During query time, the index queries the Vespa application to get the top k most relevant hits.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `application_package`  |  `ApplicationPackage`  |  Application package  |  `hybrid_template`  |  
|  `deployment_target`  |  Deployment target, either `local` or `cloud`  |  `'local'`  |  
|  `port`  |  Port that Vespa application will run on. Only applicable if deployment_target is `local`  |  `8080`  |  
|  `default_schema_name`  |  Schema name in Vespa application  |  `'doc'`  |  
|  `namespace`  |  Namespace in Vespa application. See https://docs.vespa.ai/en/documents.html#namespace. Defaults to `default`.  |  `'default'`  |  
|  `embeddings_outside_vespa`  |  `bool`  |  Whether embeddings are created outside Vespa, or not.  |  `False`  |  
|  `url`  |  `Optional[str]`  |  URL of deployed Vespa application.  |  `None`  |  
|  `groupname`  |  `Optional[str]`  |  Group name in Vespa application, only applicable in `streaming` mode, see https://pyvespa.readthedocs.io/en/latest/examples/scaling-personal-ai-assistants-with-streaming-mode-cloud.html#A-summary-of-Vespa-streaming-mode  |  `None`  |  
|  `tenant`  |  `Optional[str]`  |  Tenant for Vespa application. Applicable only if deployment_target is `cloud`  |  `None`  |  
|  `key_location`  |  `Optional[str]`  |  Location of the control plane key used for signing HTTP requests to the Vespa Cloud.  |  `None`  |  
|  `key_content`  |  `Optional[str]`  |  Content of the control plane key used for signing HTTP requests to the Vespa Cloud. Use only when key file is not available.  |  `None`  |  
|  `auth_client_token_id`  |  `Optional[str]`  |  Use token based data plane authentication. This is the token name configured in the Vespa Cloud Console. This is used to configure Vespa services.xml. The token is given read and write permissions.  |  `None`  |  
|  `kwargs`  |  Additional kwargs for Vespa application  |  
Examples:
`pip install llama-index-vector-stores-vespa`

```
fromllama_index.coreimport VectorStoreIndex
fromllama_index.vector_stores.vespaimport VespaVectorStore

vector_store = VespaVectorStore()
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(nodes, storage_context=storage_context)
retriever = index.as_retriever()
retriever.retrieve("Who directed inception?")

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vespa/llama_index/vector_stores/vespa/base.py`  
| 
```
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
```
 | 
```
classVespaVectorStore(BasePydanticVectorStore):
"""
    Vespa vector store.

    Can be initialized in several ways:
    1. (Default) Initialize Vespa vector store with default hybrid template and local (docker) deployment.
    2. Initialize by providing an application package created in pyvespa (can be deployed locally or to Vespa cloud).
    3. Initialize from previously deployed Vespa application by providing URL. (Local or cloud deployment).

    The application must be set up with the following fields:
    - id: Document id
    - text: Text field
    - embedding: Field to store embedding vectors.
    - metadata: Metadata field (all metadata will be stored here)

    The application must be set up with the following rank profiles:
    - bm25: For text search
    - semantic: For semantic search
    - fusion: For semantic hybrid search

    When creating a VectorStoreIndex from VespaVectorStore, the index will add documents to the Vespa application.
    Be ware that the Vespa container will be reused if not deleted between deployments, to avoid data duplication.
    During query time, the index queries the Vespa application to get the top k most relevant hits.

    Args:
            application_package (ApplicationPackage): Application package
            deployment_target (str): Deployment target, either `local` or `cloud`
            port (int): Port that Vespa application will run on. Only applicable if deployment_target is `local`
            default_schema_name (str): Schema name in Vespa application
            namespace (str): Namespace in Vespa application. See https://docs.vespa.ai/en/documents.html#namespace. Defaults to `default`.
            embeddings_outside_vespa (bool): Whether embeddings are created outside Vespa, or not.
            url (Optional[str]): URL of deployed Vespa application.
            groupname (Optional[str]): Group name in Vespa application, only applicable in `streaming` mode, see https://pyvespa.readthedocs.io/en/latest/examples/scaling-personal-ai-assistants-with-streaming-mode-cloud.html#A-summary-of-Vespa-streaming-mode
            tenant (Optional[str]): Tenant for Vespa application. Applicable only if deployment_target is `cloud`
            key_location (Optional[str]): Location of the control plane key used for signing HTTP requests to the Vespa Cloud.
            key_content (Optional[str]): Content of the control plane key used for signing HTTP requests to the Vespa Cloud. Use only when key file is not available.
            auth_client_token_id (Optional[str]): Use token based data plane authentication. This is the token name configured in the Vespa Cloud Console. This is used to configure Vespa services.xml. The token is given read and write permissions.
            kwargs (Any): Additional kwargs for Vespa application

    Examples:
        `pip install llama-index-vector-stores-vespa`

        ```python
        from llama_index.core import VectorStoreIndex
        from llama_index.vector_stores.vespa import VespaVectorStore

        vector_store = VespaVectorStore()
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex(nodes, storage_context=storage_context)
        retriever = index.as_retriever()
        retriever.retrieve("Who directed inception?")

        ```

    """

    stores_text: bool = True
    is_embedding_query: bool = False
    flat_metadata: bool = True

    application_package: ApplicationPackage
    deployment_target: str
    default_schema_name: str
    namespace: str
    embeddings_outside_vespa: bool
    port: int
    url: Optional[str]
    groupname: Optional[str]
    tenant: Optional[str]
    application: Optional[str]
    key_location: Optional[str]
    key_content: Optional[str]
    auth_client_token_id: Optional[str]
    kwargs: dict

    _app: Vespa = PrivateAttr()

    def__init__(
        self,
        application_package: ApplicationPackage = hybrid_template,
        namespace: str = "default",
        default_schema_name: str = "doc",
        deployment_target: str = "local",  # "local" or "cloud"
        port: int = 8080,
        embeddings_outside_vespa: bool = False,
        url: Optional[str] = None,
        groupname: Optional[str] = None,
        tenant: Optional[str] = None,
        application: Optional[str] = "hybridsearch",
        key_location: Optional[str] = None,
        key_content: Optional[str] = None,
        auth_client_token_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        # Verify that application_package is an instance of ApplicationPackage
        if not isinstance(application_package, ApplicationPackage):
            raise ValueError(
                "application_package must be an instance of vespa.package.ApplicationPackage"
            )
        if application_package == hybrid_template:
            logger.info(
                "Using default hybrid template. Please make sure that the Vespa application is set up with the correct schema and rank profile."
            )
        # Initialize all parameters
        super().__init__(
            application_package=application_package,
            namespace=namespace,
            default_schema_name=default_schema_name,
            deployment_target=deployment_target,
            port=port,
            embeddings_outside_vespa=embeddings_outside_vespa,
            url=url,
            groupname=groupname,
            tenant=tenant,
            application=application,
            key_location=key_location,
            key_content=key_content,
            auth_client_token_id=auth_client_token_id,
            kwargs=kwargs,
        )

        if self.url is None:
            self._app = self._deploy()
        else:
            self._app = self._try_get_running_app()

    @classmethod
    defclass_name(cls) -> str:
        return "VespaVectorStore"

    @property
    defclient(self) -> Vespa:
"""Get client."""
        return self._app

    def_try_get_running_app(self) -> Vespa:
        app = Vespa(url=f"{self.url}:{self.port}")
        status = app.get_application_status()
        if status.status_code == 200:
            return app
        else:
            raise ConnectionError(
                f"Vespa application not running on url {self.url} and port {self.port}. Please start Vespa application first."
            )

    def_deploy(self) -> Vespa:
        if self.deployment_target == "cloud":
            app = self._deploy_app_cloud()
        elif self.deployment_target == "local":
            app = self._deploy_app_local()
        else:
            raise ValueError(
                f"Deployment target {self.deployment_target} not supported. Please choose either `local` or `cloud`."
            )
        return app

    def_deploy_app_local(self) -> Vespa:
        logger.info(f"Deploying Vespa application {self.application} to Vespa Docker.")
        return VespaDocker(port=8080).deploy(self.application_package)

    def_deploy_app_cloud(self) -> Vespa:
        logger.info(f"Deploying Vespa application {self.application} to Vespa Cloud.")
        return VespaCloud(
            tenant=self.tenant,
            application=self.application,
            application_package=self.application_package,
            key_location=self.key_location,
            key_content=self.key_content,
            auth_client_token_id=self.auth_client_token_id,
            **self.kwargs,
        ).deploy()

    defadd(
        self,
        nodes: List[BaseNode],
        schema: Optional[str] = None,
        callback: Optional[Callable[[VespaResponse, str], None]] = callback,
    ) -> List[str]:
"""
        Add nodes to vector store.

        Args:
            nodes (List[BaseNode]): List of nodes to add
            schema (Optional[str]): Schema name in Vespa application to add nodes to. Defaults to `default_schema_name`.

        """
        # Create vespa iterable from nodes
        ids = []
        data_to_insert = []
        for node in nodes:
            metadata = node_to_metadata_dict(
                node, remove_text=False, flat_metadata=self.flat_metadata
            )
            logger.debug(f"Metadata: {metadata}")
            entry = {
                "id": node.node_id,
                "fields": {
                    "id": node.node_id,
                    "text": node.get_content(metadata_mode=MetadataMode.NONE) or "",
                    "metadata": json.dumps(metadata),
                },
            }
            if self.embeddings_outside_vespa:
                entry["fields"]["embedding"] = node.get_embedding()
            data_to_insert.append(entry)
            ids.append(node.node_id)

        self._app.feed_iterable(
            data_to_insert,
            schema=schema or self.default_schema_name,
            namespace=self.namespace,
            operation_type="feed",
            callback=callback,
        )
        return ids

    async defasync_add(
        self,
        nodes: List[BaseNode],
        schema: Optional[str] = None,
        callback: Optional[Callable[[VespaResponse, str], None]] = callback,
        max_connections: int = 10,
        num_concurrent_requests: int = 1000,
        total_timeout: int = 60,
        **kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to vector store asynchronously.

        Args:
            nodes (List[BaseNode]): List of nodes to add
            schema (Optional[str]): Schema name in Vespa application to add nodes to. Defaults to `default_schema_name`.
            max_connections (int): Maximum number of connections to Vespa application
            num_concurrent_requests (int): Maximum number of concurrent requests
            total_timeout (int): Total timeout for all requests
            kwargs (Any): Additional kwargs for Vespa application

        """
        semaphore = asyncio.Semaphore(num_concurrent_requests)
        ids = []
        data_to_insert = []
        for node in nodes:
            metadata = node_to_metadata_dict(
                node, remove_text=False, flat_metadata=self.flat_metadata
            )
            logger.debug(f"Metadata: {metadata}")
            entry = {
                "id": node.node_id,
                "fields": {
                    "id": node.node_id,
                    "text": node.get_content(metadata_mode=MetadataMode.NONE) or "",
                    "metadata": json.dumps(metadata),
                },
            }
            if self.embeddings_outside_vespa:
                entry["fields"]["embedding"] = node.get_embedding()
            data_to_insert.append(entry)
            ids.append(node.node_id)

        async with self._app.asyncio(
            connections=max_connections, total_timeout=total_timeout
        ) as async_app:
            tasks = []
            for doc in data_to_insert:
                async with semaphore:
                    task = asyncio.create_task(
                        async_app.feed_data_point(
                            data_id=doc["id"],
                            fields=doc["fields"],
                            schema=schema or self.default_schema_name,
                            namespace=self.namespace,
                            timeout=10,
                        )
                    )
                    tasks.append(task)

            results = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
            for result in results:
                if result.exception():
                    raise result.exception
        return ids

    defdelete(
        self,
        ref_doc_id: str,
        namespace: Optional[str] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Delete nodes using with ref_doc_id.
        """
        response: VespaResponse = self._app.delete_data(
            schema=self.default_schema_name,
            namespace=namespace or self.namespace,
            data_id=ref_doc_id,
            kwargs=delete_kwargs,
        )
        if not response.is_successful():
            raise ValueError(
                f"Delete request failed: {response.status_code}, response payload: {response.json}"
            )
        logger.info(f"Deleted node with id {ref_doc_id}")

    async defadelete(
        self,
        ref_doc_id: str,
        namespace: Optional[str] = None,
        **delete_kwargs: Any,
    ) -> None:
"""
        Delete nodes using with ref_doc_id.
        NOTE: this is not implemented for all vector stores. If not implemented,
        it will just call delete synchronously.
        """
        logger.info("Async delete not implemented. Will call delete synchronously.")
        self.delete(ref_doc_id, **delete_kwargs)

    def_create_query_body(
        self,
        query: VectorStoreQuery,
        sources_str: str,
        rank_profile: Optional[str] = None,
        create_embedding: bool = True,
        vector_top_k: int = 10,
    ) -> dict:
"""
        Create query parameters for Vespa.

        Args:
            query (VectorStoreQuery): VectorStoreQuery object
            sources_str (str): Sources string
            rank_profile (Optional[str]): Rank profile to use. If not provided, default rank profile is used.
            create_embedding (bool): Whether to create embedding
            vector_top_k (int): Number of top k vectors to return

        Returns:
            dict: Query parameters

        """
        logger.info(f"Query: {query}")
        if query.filters:
            logger.warning("Filter support not implemented yet. Will be ignored.")
        if query.alpha:
            logger.warning(
                "Alpha support not implemented. Must be defined in Vespa rank profile. "
                "See for example https://pyvespa.readthedocs.io/en/latest/examples/evaluating-with-snowflake-arctic-embed.html"
            )

        if query.query_embedding is None and not create_embedding:
            raise ValueError(
                "Input embedding must be provided if embeddings are not created outside Vespa"
            )

        base_params = {
            "hits": query.similarity_top_k,
            "ranking.profile": rank_profile
            or self._get_default_rank_profile(query.mode),
            "query": query.query_str,
            "tracelevel": 9,
        }
        logger.debug(query.mode)
        if query.mode in [
            VectorStoreQueryMode.TEXT_SEARCH,
            VectorStoreQueryMode.DEFAULT,
        ]:
            query_params = {"yql": f"select * from {sources_str} where userQuery()"}
        elif query.mode in [
            VectorStoreQueryMode.SEMANTIC_HYBRID,
            VectorStoreQueryMode.HYBRID,
        ]:
            if not query.embedding_field:
                embedding_field = "embedding"
                logger.warning(
                    f"Embedding field not provided. Using default embedding field {embedding_field}"
                )
            query_params = {
                "yql": f"select * from {sources_str} where {self._build_query_filter(query.mode,embedding_field,vector_top_k,query.similarity_top_k)}",
                "input.query(q)": (
                    f"embed({query.query_str})"
                    if create_embedding
                    else query.query_embedding
                ),
            }
        else:
            raise NotImplementedError(
                f"Query mode {query.mode} not implemented for Vespa yet. Contributions are welcome!"
            )

        return {**base_params, **query_params}

    def_get_default_rank_profile(self, mode):
        return {
            VectorStoreQueryMode.TEXT_SEARCH: "bm25",
            VectorStoreQueryMode.SEMANTIC_HYBRID: "fusion",
            VectorStoreQueryMode.HYBRID: "fusion",
            VectorStoreQueryMode.DEFAULT: "bm25",
        }.get(mode)

    def_build_query_filter(
        self, mode, embedding_field, vector_top_k, similarity_top_k
    ):
"""
        Build query filter for Vespa query.
        The part after "select * from {sources_str} where" in the query.
        """
        if mode in [
            VectorStoreQueryMode.SEMANTIC_HYBRID,
            VectorStoreQueryMode.HYBRID,
        ]:
            return f"rank({{targetHits:{vector_top_k}}}nearestNeighbor({embedding_field},q), userQuery()) limit {similarity_top_k}"
        else:
            raise ValueError(f"Query mode {mode} not supported.")

    defquery(
        self,
        query: VectorStoreQuery,
        sources: Optional[List[str]] = None,
        rank_profile: Optional[str] = None,
        vector_top_k: int = 10,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""Query vector store."""
        logger.debug(f"Query: {query}")
        sources_str = ",".join(sources) if sources else "sources *"
        mode = query.mode
        body = self._create_query_body(
            query=query,
            sources_str=sources_str,
            rank_profile=rank_profile,
            create_embedding=not self.embeddings_outside_vespa,
            vector_top_k=vector_top_k,
        )
        logger.info(f"Vespa Query body:\n{body}")
        with self._app.syncio() as session:
            response = session.query(
                body=body,
            )
        if not response.is_successful():
            raise ValueError(
                f"Query request failed: {response.status_code}, response payload: {response.get_json()}"
            )
        logger.debug("Response:")
        logger.debug(response.json)
        logger.debug("Hits:")
        logger.debug(response.hits)
        nodes = []
        ids: List[str] = []
        similarities: List[float] = []
        for hit in response.hits:
            response_fields: dict = hit.get("fields", {})
            metadata = response_fields.get("metadata", {})
            metadata = json.loads(metadata)
            logger.debug(f"Metadata: {metadata}")
            node = metadata_dict_to_node(metadata)
            text = response_fields.get("body", "")
            node.set_content(text)
            nodes.append(node)
            ids.append(response_fields.get("id"))
            similarities.append(hit["relevance"])
        return VectorStoreQueryResult(nodes=nodes, ids=ids, similarities=similarities)

    async defaquery(
        self,
        query: VectorStoreQuery,
        sources: Optional[List[str]] = None,
        rank_profile: Optional[str] = None,
        vector_top_k: int = 10,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
"""
        Asynchronously query vector store.
        NOTE: this is not implemented for all vector stores. If not implemented,
        it will just call query synchronously.
        """
        logger.info("Async query not implemented. Will call query synchronously.")
        return self.query(
            query=query,
            sources=sources,
            rank_profile=rank_profile,
            vector_top_k=vector_top_k,
            **kwargs,
        )

    defpersist(
        self,
    ) -> None:
        return NotImplemented("Persist is not implemented for VespaVectorStore")

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vespa/#llama_index.vector_stores.vespa.VespaVectorStore.client "Permanent link")

```
client: 

```

Get client.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vespa/#llama_index.vector_stores.vespa.VespaVectorStore.add "Permanent link")

```
add(
    nodes: [],
    schema: Optional[] = None,
    callback: Optional[
        Callable[[VespaResponse, ], None]
    ] = callback,
) -> []

```

Add nodes to vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes to add  |  _required_  |  
|  `schema`  |  `Optional[str]`  |  Schema name in Vespa application to add nodes to. Defaults to `default_schema_name`.  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vespa/llama_index/vector_stores/vespa/base.py`  
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
```
 | 
```
defadd(
    self,
    nodes: List[BaseNode],
    schema: Optional[str] = None,
    callback: Optional[Callable[[VespaResponse, str], None]] = callback,
) -> List[str]:
"""
    Add nodes to vector store.

    Args:
        nodes (List[BaseNode]): List of nodes to add
        schema (Optional[str]): Schema name in Vespa application to add nodes to. Defaults to `default_schema_name`.

    """
    # Create vespa iterable from nodes
    ids = []
    data_to_insert = []
    for node in nodes:
        metadata = node_to_metadata_dict(
            node, remove_text=False, flat_metadata=self.flat_metadata
        )
        logger.debug(f"Metadata: {metadata}")
        entry = {
            "id": node.node_id,
            "fields": {
                "id": node.node_id,
                "text": node.get_content(metadata_mode=MetadataMode.NONE) or "",
                "metadata": json.dumps(metadata),
            },
        }
        if self.embeddings_outside_vespa:
            entry["fields"]["embedding"] = node.get_embedding()
        data_to_insert.append(entry)
        ids.append(node.node_id)

    self._app.feed_iterable(
        data_to_insert,
        schema=schema or self.default_schema_name,
        namespace=self.namespace,
        operation_type="feed",
        callback=callback,
    )
    return ids

```
 |  
| --- | --- |  
###  async_add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vespa/#llama_index.vector_stores.vespa.VespaVectorStore.async_add "Permanent link")

```
async_add(
    nodes: [],
    schema: Optional[] = None,
    callback: Optional[
        Callable[[VespaResponse, ], None]
    ] = callback,
    max_connections:  = 10,
    num_concurrent_requests:  = 1000,
    total_timeout:  = 60,
    **kwargs: 
) -> []

```

Add nodes to vector store asynchronously.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |   |  List of nodes to add  |  _required_  |  
|  `schema`  |  `Optional[str]`  |  Schema name in Vespa application to add nodes to. Defaults to `default_schema_name`.  |  `None`  |  
|  `max_connections`  |  Maximum number of connections to Vespa application  |  
|  `num_concurrent_requests`  |  Maximum number of concurrent requests  |  `1000`  |  
|  `total_timeout`  |  Total timeout for all requests  |  
|  `kwargs`  |  Additional kwargs for Vespa application  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vespa/llama_index/vector_stores/vespa/base.py`  
| 
```
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
```
 | 
```
async defasync_add(
    self,
    nodes: List[BaseNode],
    schema: Optional[str] = None,
    callback: Optional[Callable[[VespaResponse, str], None]] = callback,
    max_connections: int = 10,
    num_concurrent_requests: int = 1000,
    total_timeout: int = 60,
    **kwargs: Any,
) -> List[str]:
"""
    Add nodes to vector store asynchronously.

    Args:
        nodes (List[BaseNode]): List of nodes to add
        schema (Optional[str]): Schema name in Vespa application to add nodes to. Defaults to `default_schema_name`.
        max_connections (int): Maximum number of connections to Vespa application
        num_concurrent_requests (int): Maximum number of concurrent requests
        total_timeout (int): Total timeout for all requests
        kwargs (Any): Additional kwargs for Vespa application

    """
    semaphore = asyncio.Semaphore(num_concurrent_requests)
    ids = []
    data_to_insert = []
    for node in nodes:
        metadata = node_to_metadata_dict(
            node, remove_text=False, flat_metadata=self.flat_metadata
        )
        logger.debug(f"Metadata: {metadata}")
        entry = {
            "id": node.node_id,
            "fields": {
                "id": node.node_id,
                "text": node.get_content(metadata_mode=MetadataMode.NONE) or "",
                "metadata": json.dumps(metadata),
            },
        }
        if self.embeddings_outside_vespa:
            entry["fields"]["embedding"] = node.get_embedding()
        data_to_insert.append(entry)
        ids.append(node.node_id)

    async with self._app.asyncio(
        connections=max_connections, total_timeout=total_timeout
    ) as async_app:
        tasks = []
        for doc in data_to_insert:
            async with semaphore:
                task = asyncio.create_task(
                    async_app.feed_data_point(
                        data_id=doc["id"],
                        fields=doc["fields"],
                        schema=schema or self.default_schema_name,
                        namespace=self.namespace,
                        timeout=10,
                    )
                )
                tasks.append(task)

        results = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
        for result in results:
            if result.exception():
                raise result.exception
    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vespa/#llama_index.vector_stores.vespa.VespaVectorStore.delete "Permanent link")

```
delete(
    ref_doc_id: ,
    namespace: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Delete nodes using with ref_doc_id.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vespa/llama_index/vector_stores/vespa/base.py`  
| 
```
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
```
 | 
```
defdelete(
    self,
    ref_doc_id: str,
    namespace: Optional[str] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Delete nodes using with ref_doc_id.
    """
    response: VespaResponse = self._app.delete_data(
        schema=self.default_schema_name,
        namespace=namespace or self.namespace,
        data_id=ref_doc_id,
        kwargs=delete_kwargs,
    )
    if not response.is_successful():
        raise ValueError(
            f"Delete request failed: {response.status_code}, response payload: {response.json}"
        )
    logger.info(f"Deleted node with id {ref_doc_id}")

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vespa/#llama_index.vector_stores.vespa.VespaVectorStore.adelete "Permanent link")

```
adelete(
    ref_doc_id: ,
    namespace: Optional[] = None,
    **delete_kwargs: 
) -> None

```

Delete nodes using with ref_doc_id. NOTE: this is not implemented for all vector stores. If not implemented, it will just call delete synchronously.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vespa/llama_index/vector_stores/vespa/base.py`  
| 
```
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
```
 | 
```
async defadelete(
    self,
    ref_doc_id: str,
    namespace: Optional[str] = None,
    **delete_kwargs: Any,
) -> None:
"""
    Delete nodes using with ref_doc_id.
    NOTE: this is not implemented for all vector stores. If not implemented,
    it will just call delete synchronously.
    """
    logger.info("Async delete not implemented. Will call delete synchronously.")
    self.delete(ref_doc_id, **delete_kwargs)

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vespa/#llama_index.vector_stores.vespa.VespaVectorStore.query "Permanent link")

```
query(
    query: ,
    sources: Optional[[]] = None,
    rank_profile: Optional[] = None,
    vector_top_k:  = 10,
    **kwargs: 
) -> 

```

Query vector store.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vespa/llama_index/vector_stores/vespa/base.py`  
| 
```
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
```
 | 
```
defquery(
    self,
    query: VectorStoreQuery,
    sources: Optional[List[str]] = None,
    rank_profile: Optional[str] = None,
    vector_top_k: int = 10,
    **kwargs: Any,
) -> VectorStoreQueryResult:
"""Query vector store."""
    logger.debug(f"Query: {query}")
    sources_str = ",".join(sources) if sources else "sources *"
    mode = query.mode
    body = self._create_query_body(
        query=query,
        sources_str=sources_str,
        rank_profile=rank_profile,
        create_embedding=not self.embeddings_outside_vespa,
        vector_top_k=vector_top_k,
    )
    logger.info(f"Vespa Query body:\n{body}")
    with self._app.syncio() as session:
        response = session.query(
            body=body,
        )
    if not response.is_successful():
        raise ValueError(
            f"Query request failed: {response.status_code}, response payload: {response.get_json()}"
        )
    logger.debug("Response:")
    logger.debug(response.json)
    logger.debug("Hits:")
    logger.debug(response.hits)
    nodes = []
    ids: List[str] = []
    similarities: List[float] = []
    for hit in response.hits:
        response_fields: dict = hit.get("fields", {})
        metadata = response_fields.get("metadata", {})
        metadata = json.loads(metadata)
        logger.debug(f"Metadata: {metadata}")
        node = metadata_dict_to_node(metadata)
        text = response_fields.get("body", "")
        node.set_content(text)
        nodes.append(node)
        ids.append(response_fields.get("id"))
        similarities.append(hit["relevance"])
    return VectorStoreQueryResult(nodes=nodes, ids=ids, similarities=similarities)

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/vespa/#llama_index.vector_stores.vespa.VespaVectorStore.aquery "Permanent link")

```
aquery(
    query: ,
    sources: Optional[[]] = None,
    rank_profile: Optional[] = None,
    vector_top_k:  = 10,
    **kwargs: 
) -> 

```

Asynchronously query vector store. NOTE: this is not implemented for all vector stores. If not implemented, it will just call query synchronously.
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-vespa/llama_index/vector_stores/vespa/base.py`  
| 
```
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
```
 | 
```
async defaquery(
    self,
    query: VectorStoreQuery,
    sources: Optional[List[str]] = None,
    rank_profile: Optional[str] = None,
    vector_top_k: int = 10,
    **kwargs: Any,
) -> VectorStoreQueryResult:
"""
    Asynchronously query vector store.
    NOTE: this is not implemented for all vector stores. If not implemented,
    it will just call query synchronously.
    """
    logger.info("Async query not implemented. Will call query synchronously.")
    return self.query(
        query=query,
        sources=sources,
        rank_profile=rank_profile,
        vector_top_k=vector_top_k,
        **kwargs,
    )

```
 |  
| --- | --- |  
options: members: - VespaVectorStore
