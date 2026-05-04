# openGauss
##  OpenGaussStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/openGauss/#llama_index.vector_stores.openGauss.OpenGaussStore "Permanent link")
Bases: 
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-openGauss/llama_index/vector_stores/openGauss/base.py`  
| 
```
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
```
 | 
```
classOpenGaussStore(PGVectorStore):
    def__init__(
        self,
        connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
        async_connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
        table_name: Optional[str] = None,
        schema_name: Optional[str] = None,
        hybrid_search: bool = False,
        text_search_config: str = "english",
        embed_dim: int = 1536,
        cache_ok: bool = False,
        perform_setup: bool = True,
        debug: bool = False,
        use_jsonb: bool = False,
        hnsw_kwargs: Optional[Dict[str, Any]] = None,
        create_engine_kwargs: Optional[Dict[str, Any]] = None,
        initialization_fail_on_error: bool = False,
        engine: Optional[sqlalchemy.engine.Engine] = None,
        async_engine: Optional[sqlalchemy.ext.asyncio.AsyncEngine] = None,
        indexed_metadata_keys: Optional[Set[Tuple[str, PGType]]] = None,
    ) -> None:
"""
        Constructor.

        Args:
            connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to postgres db.
            async_connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to async pg db.
            table_name (str): Table name.
            schema_name (str): Schema name.
            hybrid_search (bool, optional): Enable hybrid search. Defaults to False.
            text_search_config (str, optional): Text search configuration. Defaults to "english".
            embed_dim (int, optional): Embedding dimensions. Defaults to 1536.
            cache_ok (bool, optional): Enable cache. Defaults to False.
            perform_setup (bool, optional): If db should be set up. Defaults to True.
            debug (bool, optional): Debug mode. Defaults to False.
            use_jsonb (bool, optional): Use JSONB instead of JSON. Defaults to False.
            hnsw_kwargs (Optional[Dict[str, Any]], optional): HNSW kwargs, a dict that
                contains "hnsw_ef_construction", "hnsw_ef_search", "hnsw_m", and optionally "hnsw_dist_method". Defaults to None,
                which turns off HNSW search.
            create_engine_kwargs (Optional[Dict[str, Any]], optional): Engine parameters to pass to create_engine. Defaults to None.
            engine (Optional[sqlalchemy.engine.Engine], optional): SQLAlchemy engine instance to use. Defaults to None.
            async_engine (Optional[sqlalchemy.ext.asyncio.AsyncEngine], optional): SQLAlchemy async engine instance to use. Defaults to None.
            indexed_metadata_keys (Optional[List[Tuple[str, str]]], optional): Set of metadata keys with their type to index. Defaults to None.

        """
        super().__init__(
            connection_string=str(connection_string),
            async_connection_string=str(async_connection_string),
            table_name=table_name,
            schema_name=schema_name,
            hybrid_search=hybrid_search,
            text_search_config=text_search_config,
            embed_dim=embed_dim,
            cache_ok=cache_ok,
            perform_setup=perform_setup,
            debug=debug,
            use_jsonb=use_jsonb,
            hnsw_kwargs=hnsw_kwargs,
            create_engine_kwargs=create_engine_kwargs or {},
            initialization_fail_on_error=initialization_fail_on_error,
            use_halfvec=False,
            indexed_metadata_keys=indexed_metadata_keys,
        )
        self._table_class = get_data_model(
            self._base,
            table_name,
            schema_name,
            hybrid_search,
            text_search_config,
            cache_ok,
            embed_dim=embed_dim,
            use_jsonb=use_jsonb,
            indexed_metadata_keys=indexed_metadata_keys,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "OpenGaussStore"

    @classmethod
    deffrom_params(
        cls,
        host: Optional[str] = None,
        port: Optional[str] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        table_name: str = "llamaindex",
        schema_name: str = "public",
        connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
        async_connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
        hybrid_search: bool = False,
        text_search_config: str = "english",
        embed_dim: int = 1536,
        cache_ok: bool = False,
        perform_setup: bool = True,
        debug: bool = False,
        use_jsonb: bool = False,
        hnsw_kwargs: Optional[Dict[str, Any]] = None,
        create_engine_kwargs: Optional[Dict[str, Any]] = None,
        indexed_metadata_keys: Optional[Set[Tuple[str, PGType]]] = None,
    ) -> "OpenGaussStore":
"""
        Construct from params.

        Args:
            host (Optional[str], optional): Host of postgres connection. Defaults to None.
            port (Optional[str], optional): Port of postgres connection. Defaults to None.
            database (Optional[str], optional): Postgres DB name. Defaults to None.
            user (Optional[str], optional): Postgres username. Defaults to None.
            password (Optional[str], optional): Postgres password. Defaults to None.
            table_name (str): Table name. Defaults to "llamaindex".
            schema_name (str): Schema name. Defaults to "public".
            connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to postgres db
            async_connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to async pg db
            hybrid_search (bool, optional): Enable hybrid search. Defaults to False.
            text_search_config (str, optional): Text search configuration. Defaults to "english".
            embed_dim (int, optional): Embedding dimensions. Defaults to 1536.
            cache_ok (bool, optional): Enable cache. Defaults to False.
            perform_setup (bool, optional): If db should be set up. Defaults to True.
            debug (bool, optional): Debug mode. Defaults to False.
            use_jsonb (bool, optional): Use JSONB instead of JSON. Defaults to False.
            hnsw_kwargs (Optional[Dict[str, Any]], optional): HNSW kwargs, a dict that
                contains "hnsw_ef_construction", "hnsw_ef_search", "hnsw_m", and optionally "hnsw_dist_method". Defaults to None,
                which turns off HNSW search.
            create_engine_kwargs (Optional[Dict[str, Any]], optional): Engine parameters to pass to create_engine. Defaults to None.
            indexed_metadata_keys (Optional[Set[Tuple[str, str]]], optional): Set of metadata keys to index. Defaults to None.

        Returns:
            PGVectorStore: Instance of PGVectorStore constructed from params.

        """
        conn_str = (
            connection_string
            or f"opengauss+psycopg2://{user}:{password}@{host}:{port}/{database}"
        )
        async_conn_str = async_connection_string or (
            f"opengauss+asyncpg://{user}:{password}@{host}:{port}/{database}"
        )
        return cls(
            connection_string=conn_str,
            async_connection_string=async_conn_str,
            table_name=table_name,
            schema_name=schema_name,
            hybrid_search=hybrid_search,
            text_search_config=text_search_config,
            embed_dim=embed_dim,
            cache_ok=cache_ok,
            perform_setup=perform_setup,
            debug=debug,
            use_jsonb=use_jsonb,
            hnsw_kwargs=hnsw_kwargs,
            create_engine_kwargs=create_engine_kwargs,
            indexed_metadata_keys=indexed_metadata_keys,
        )

    def_initialize(self) -> None:
        fail_on_error = self.initialization_fail_on_error
        if not self._is_initialized:
            self._connect()
            if self.perform_setup:
                try:
                    self._create_schema_if_not_exists()
                except Exception as e:
                    _logger.warning(f"PG Setup: Error creating schema: {e}")
                    if fail_on_error:
                        raise
                try:
                    self._create_tables_if_not_exists()
                except Exception as e:
                    _logger.warning(f"PG Setup: Error creating tables: {e}")
                    if fail_on_error:
                        raise
                if self.hnsw_kwargs is not None:
                    try:
                        self._create_hnsw_index()
                    except Exception as e:
                        _logger.warning(f"PG Setup: Error creating HNSW index: {e}")
                        if fail_on_error:
                            raise
            self._is_initialized = True

    def_connect(self) -> Any:
        fromsqlalchemyimport create_engine, event
        fromsqlalchemy.ext.asyncioimport AsyncSession, create_async_engine
        fromsqlalchemy.ormimport sessionmaker
        fromopengauss_sqlalchemy.register_asyncimport register_vector

        self._engine = self._engine or create_engine(
            self.connection_string, echo=self.debug, **self.create_engine_kwargs
        )
        self._session = sessionmaker(self._engine)

        self._async_engine = self._async_engine or create_async_engine(
            self.async_connection_string, **self.create_engine_kwargs
        )

        @event.listens_for(self._async_engine.sync_engine, "connect")
        def_connect_event(dbapi_connection, connection_record):
            dbapi_connection.run_async(register_vector)

        self._async_session = sessionmaker(self._async_engine, class_=AsyncSession)  # type: ignore

    def_query_with_score(
        self,
        embedding: Optional[List[float]],
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
        **kwargs: Any,
    ) -> List[DBEmbeddingRow]:
        stmt = self._build_query(embedding, limit, metadata_filters)
        with self._session() as session, session.begin():
            fromsqlalchemyimport text

            if kwargs.get("ivfflat_probes"):
                ivfflat_probes = kwargs.get("ivfflat_probes")
                session.execute(
                    text(f"SET ivfflat_probes = :ivfflat_probes"),
                    {"ivfflat_probes": ivfflat_probes},
                )
            if self.hnsw_kwargs:
                hnsw_ef_search = (
                    kwargs.get("hnsw_ef_search") or self.hnsw_kwargs["hnsw_ef_search"]
                )
                session.execute(
                    text(f"SET hnsw_ef_search = :hnsw_ef_search"),
                    {"hnsw_ef_search": hnsw_ef_search},
                )

            res = session.execute(
                stmt,
            )
            return [
                DBEmbeddingRow(
                    node_id=item.node_id,
                    text=item.text,
                    metadata=item.metadata_,
                    similarity=(1 - item.distance) if item.distance is not None else 0,
                )
                for item in res.all()
            ]

    async def_aquery_with_score(
        self,
        embedding: Optional[List[float]],
        limit: int = 10,
        metadata_filters: Optional[MetadataFilters] = None,
        **kwargs: Any,
    ) -> List[DBEmbeddingRow]:
        stmt = self._build_query(embedding, limit, metadata_filters)
        async with self._async_session() as async_session, async_session.begin():
            fromsqlalchemyimport text

            if self.hnsw_kwargs:
                hnsw_ef_search = (
                    kwargs.get("hnsw_ef_search") or self.hnsw_kwargs["hnsw_ef_search"]
                )
                await async_session.execute(
                    text(f"SET hnsw_ef_search = {hnsw_ef_search}"),
                )
            if kwargs.get("ivfflat_probes"):
                ivfflat_probes = kwargs.get("ivfflat_probes")
                await async_session.execute(
                    text(f"SET ivfflat_probes = :ivfflat_probes"),
                    {"ivfflat_probes": ivfflat_probes},
                )

            res = await async_session.execute(stmt)
            return [
                DBEmbeddingRow(
                    node_id=item.node_id,
                    text=item.text,
                    metadata=item.metadata_,
                    similarity=(1 - item.distance) if item.distance is not None else 0,
                )
                for item in res.all()
            ]

```
 |  
| --- | --- |  
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/openGauss/#llama_index.vector_stores.openGauss.OpenGaussStore.from_params "Permanent link")

```
from_params(
    host: Optional[] = None,
    port: Optional[] = None,
    database: Optional[] = None,
    user: Optional[] = None,
    password: Optional[] = None,
    table_name:  = "llamaindex",
    schema_name:  = "public",
    connection_string: Optional[Union[, ]] = None,
    async_connection_string: Optional[
        Union[, ]
    ] = None,
    hybrid_search:  = False,
    text_search_config:  = "english",
    embed_dim:  = 1536,
    cache_ok:  = False,
    perform_setup:  = True,
    debug:  = False,
    use_jsonb:  = False,
    hnsw_kwargs: Optional[[, ]] = None,
    create_engine_kwargs: Optional[[, ]] = None,
    indexed_metadata_keys: Optional[
        [Tuple[, PGType]]
    ] = None,
) -> 

```

Construct from params.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `host`  |  `Optional[str]`  |  Host of postgres connection. Defaults to None.  |  `None`  |  
|  `port`  |  `Optional[str]`  |  Port of postgres connection. Defaults to None.  |  `None`  |  
|  `database`  |  `Optional[str]`  |  Postgres DB name. Defaults to None.  |  `None`  |  
|  `user`  |  `Optional[str]`  |  Postgres username. Defaults to None.  |  `None`  |  
|  `password`  |  `Optional[str]`  |  Postgres password. Defaults to None.  |  `None`  |  
|  `table_name`  |  Table name. Defaults to "llamaindex".  |  `'llamaindex'`  |  
|  `schema_name`  |  Schema name. Defaults to "public".  |  `'public'`  |  
|  `connection_string`  |  `Union[str, URL]`  |  Connection string to postgres db  |  `None`  |  
|  `async_connection_string`  |  `Union[str, URL]`  |  Connection string to async pg db  |  `None`  |  
|  `hybrid_search`  |  `bool`  |  Enable hybrid search. Defaults to False.  |  `False`  |  
|  `text_search_config`  |  Text search configuration. Defaults to "english".  |  `'english'`  |  
|  `embed_dim`  |  Embedding dimensions. Defaults to 1536.  |  `1536`  |  
|  `cache_ok`  |  `bool`  |  Enable cache. Defaults to False.  |  `False`  |  
|  `perform_setup`  |  `bool`  |  If db should be set up. Defaults to True.  |  `True`  |  
|  `debug`  |  `bool`  |  Debug mode. Defaults to False.  |  `False`  |  
|  `use_jsonb`  |  `bool`  |  Use JSONB instead of JSON. Defaults to False.  |  `False`  |  
|  `hnsw_kwargs`  |  `Optional[Dict[str, Any]]`  |  HNSW kwargs, a dict that contains "hnsw_ef_construction", "hnsw_ef_search", "hnsw_m", and optionally "hnsw_dist_method". Defaults to None, which turns off HNSW search.  |  `None`  |  
|  `create_engine_kwargs`  |  `Optional[Dict[str, Any]]`  |  Engine parameters to pass to create_engine. Defaults to None.  |  `None`  |  
|  `indexed_metadata_keys`  |  `Optional[Set[Tuple[str, str]]]`  |  Set of metadata keys to index. Defaults to None.  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `PGVectorStore`  |   |  Instance of PGVectorStore constructed from params.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-openGauss/llama_index/vector_stores/openGauss/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_params(
    cls,
    host: Optional[str] = None,
    port: Optional[str] = None,
    database: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    table_name: str = "llamaindex",
    schema_name: str = "public",
    connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
    async_connection_string: Optional[Union[str, sqlalchemy.engine.URL]] = None,
    hybrid_search: bool = False,
    text_search_config: str = "english",
    embed_dim: int = 1536,
    cache_ok: bool = False,
    perform_setup: bool = True,
    debug: bool = False,
    use_jsonb: bool = False,
    hnsw_kwargs: Optional[Dict[str, Any]] = None,
    create_engine_kwargs: Optional[Dict[str, Any]] = None,
    indexed_metadata_keys: Optional[Set[Tuple[str, PGType]]] = None,
) -> "OpenGaussStore":
"""
    Construct from params.

    Args:
        host (Optional[str], optional): Host of postgres connection. Defaults to None.
        port (Optional[str], optional): Port of postgres connection. Defaults to None.
        database (Optional[str], optional): Postgres DB name. Defaults to None.
        user (Optional[str], optional): Postgres username. Defaults to None.
        password (Optional[str], optional): Postgres password. Defaults to None.
        table_name (str): Table name. Defaults to "llamaindex".
        schema_name (str): Schema name. Defaults to "public".
        connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to postgres db
        async_connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to async pg db
        hybrid_search (bool, optional): Enable hybrid search. Defaults to False.
        text_search_config (str, optional): Text search configuration. Defaults to "english".
        embed_dim (int, optional): Embedding dimensions. Defaults to 1536.
        cache_ok (bool, optional): Enable cache. Defaults to False.
        perform_setup (bool, optional): If db should be set up. Defaults to True.
        debug (bool, optional): Debug mode. Defaults to False.
        use_jsonb (bool, optional): Use JSONB instead of JSON. Defaults to False.
        hnsw_kwargs (Optional[Dict[str, Any]], optional): HNSW kwargs, a dict that
            contains "hnsw_ef_construction", "hnsw_ef_search", "hnsw_m", and optionally "hnsw_dist_method". Defaults to None,
            which turns off HNSW search.
        create_engine_kwargs (Optional[Dict[str, Any]], optional): Engine parameters to pass to create_engine. Defaults to None.
        indexed_metadata_keys (Optional[Set[Tuple[str, str]]], optional): Set of metadata keys to index. Defaults to None.

    Returns:
        PGVectorStore: Instance of PGVectorStore constructed from params.

    """
    conn_str = (
        connection_string
        or f"opengauss+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )
    async_conn_str = async_connection_string or (
        f"opengauss+asyncpg://{user}:{password}@{host}:{port}/{database}"
    )
    return cls(
        connection_string=conn_str,
        async_connection_string=async_conn_str,
        table_name=table_name,
        schema_name=schema_name,
        hybrid_search=hybrid_search,
        text_search_config=text_search_config,
        embed_dim=embed_dim,
        cache_ok=cache_ok,
        perform_setup=perform_setup,
        debug=debug,
        use_jsonb=use_jsonb,
        hnsw_kwargs=hnsw_kwargs,
        create_engine_kwargs=create_engine_kwargs,
        indexed_metadata_keys=indexed_metadata_keys,
    )

```
 |  
| --- | --- |  
options: members: - OpenGaussStore
