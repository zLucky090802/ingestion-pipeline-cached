# Postgres
##  PostgresKVStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/postgres/#llama_index.storage.kvstore.postgres.PostgresKVStore "Permanent link")
Bases: 
Postgres Key-Value store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `connection_string`  |  psycopg2 connection string  |  `None`  |  
|  `async_connection_string`  |  asyncpg connection string  |  `None`  |  
|  `table_name`  |  table name  |  _required_  |  
|  `schema_name`  |  `Optional[str]`  |  schema name  |  `'public'`  |  
|  `perform_setup`  |  `Optional[bool]`  |  perform table setup  |  `True`  |  
|  `debug`  |  `Optional[bool]`  |  debug mode  |  `False`  |  
|  `use_jsonb`  |  `Optional[bool]`  |  use JSONB data type for storage  |  `False`  |  
|  `create_engine_kwargs`  |  `Optional[Dict[str, Any]]`  |  extra keyword arguments forwarded to SQLAlchemy's create_engine/create_async_engine (for example, connect_args for timeouts and pooling).  |  `None`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-postgres/llama_index/storage/kvstore/postgres/base.py`  
| 
```
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
```
 | 
```
classPostgresKVStore(BaseKVStore):
"""
    Postgres Key-Value store.

    Args:
        connection_string (str): psycopg2 connection string
        async_connection_string (str): asyncpg connection string
        table_name (str): table name
        schema_name (Optional[str]): schema name
        perform_setup (Optional[bool]): perform table setup
        debug (Optional[bool]): debug mode
        use_jsonb (Optional[bool]): use JSONB data type for storage
        create_engine_kwargs (Optional[Dict[str, Any]]): extra keyword arguments forwarded to SQLAlchemy's create_engine/create_async_engine (for example, connect_args for timeouts and pooling).

    """

    connection_string: Optional[str]
    async_connection_string: Optional[str]
    table_name: str
    schema_name: str
    perform_setup: bool
    debug: bool
    use_jsonb: bool
    create_engine_kwargs: Dict[str, Any]
    _engine: Optional[sqlalchemy.engine.Engine] = PrivateAttr()
    _async_engine: Optional[sqlalchemy.ext.asyncio.AsyncEngine] = PrivateAttr()

    def__init__(
        self,
        table_name: str,
        connection_string: Optional[str] = None,
        async_connection_string: Optional[str] = None,
        schema_name: str = "public",
        create_engine_kwargs: Optional[Dict[str, Any]] = None,
        engine: Optional[sqlalchemy.engine.Engine] = None,
        async_engine: Optional[sqlalchemy.ext.asyncio.AsyncEngine] = None,
        perform_setup: bool = True,
        debug: bool = False,
        use_jsonb: bool = False,
    ) -> None:
        try:
            importasyncpg  # noqa
            importpsycopg2  # noqa
        except ImportError:
            raise ImportError(
                "`psycopg2-binary` and `asyncpg` packages should be pre installed"
            )

        table_name = table_name.lower()
        schema_name = schema_name.lower()
        self.connection_string = connection_string
        self.async_connection_string = async_connection_string
        self.table_name = table_name
        self.schema_name = schema_name
        self.perform_setup = perform_setup
        self.debug = debug
        self.use_jsonb = use_jsonb
        self.create_engine_kwargs = create_engine_kwargs or {}
        self._engine = engine
        self._async_engine = async_engine
        self._is_initialized = False

        if not self._async_engine and not self.async_connection_string:
            raise ValueError(
                "You should provide an asynchronous connection string, if you do not provide an asynchronous SqlAlchemy engine"
            )
        elif not self._engine and not self.connection_string:
            raise ValueError(
                "You should provide a synchronous connection string, if you do not provide a synchronous SqlAlchemy engine"
            )
        elif (
            not self._engine
            and not self._async_engine
            and (not self.connection_string or not self.connection_string)
        ):
            raise ValueError(
                "If a SqlAlchemy engine is not provided, you should provide a synchronous and an asynchronous connection string"
            )

        fromsqlalchemy.ormimport declarative_base

        # sqlalchemy model
        self._base = declarative_base()
        self._table_class = get_data_model(
            self._base,
            table_name,
            schema_name,
            use_jsonb=use_jsonb,
        )

    @classmethod
    deffrom_params(
        cls,
        host: Optional[str] = None,
        port: Optional[str] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        table_name: str = "kvstore",
        schema_name: str = "public",
        connection_string: Optional[str] = None,
        async_connection_string: Optional[str] = None,
        perform_setup: bool = True,
        debug: bool = False,
        use_jsonb: bool = False,
        create_engine_kwargs: Optional[Dict[str, Any]] = None,
    ) -> "PostgresKVStore":
"""Return connection string from database parameters."""
        conn_str = (
            connection_string
            or f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        )
        async_conn_str = async_connection_string or (
            f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
        )
        return cls(
            connection_string=conn_str,
            async_connection_string=async_conn_str,
            table_name=table_name,
            schema_name=schema_name,
            perform_setup=perform_setup,
            debug=debug,
            use_jsonb=use_jsonb,
            create_engine_kwargs=create_engine_kwargs,
        )

    @classmethod
    deffrom_uri(
        cls,
        uri: str,
        table_name: str = "kvstore",
        schema_name: str = "public",
        perform_setup: bool = True,
        debug: bool = False,
        use_jsonb: bool = False,
        create_engine_kwargs: Optional[Dict[str, Any]] = None,
    ) -> "PostgresKVStore":
"""Return connection string from database parameters."""
        params = params_from_uri(uri)
        return cls.from_params(
            **params,
            table_name=table_name,
            schema_name=schema_name,
            perform_setup=perform_setup,
            debug=debug,
            use_jsonb=use_jsonb,
            create_engine_kwargs=create_engine_kwargs,
        )

    def_connect(self) -> Any:
        fromsqlalchemyimport create_engine
        fromsqlalchemy.ext.asyncioimport AsyncSession, create_async_engine
        fromsqlalchemy.ormimport sessionmaker

        self._engine = self._engine or create_engine(
            self.connection_string, echo=self.debug, **self.create_engine_kwargs
        )
        self._session = sessionmaker(self._engine)

        self._async_engine = self._async_engine or create_async_engine(
            self.async_connection_string, **self.create_engine_kwargs
        )
        self._async_session = sessionmaker(self._async_engine, class_=AsyncSession)

    def_create_schema_if_not_exists(self) -> None:
        with self._session() as session, session.begin():
            inspector = inspect(session.connection())
            existing_schemas = inspector.get_schema_names()
            if self.schema_name not in existing_schemas:
                session.execute(CreateSchema(self.schema_name))

    def_create_tables_if_not_exists(self) -> None:
        with self._session() as session, session.begin():
            self._base.metadata.create_all(session.connection())

    def_initialize(self) -> None:
        if not self._is_initialized:
            self._connect()
            if self.perform_setup:
                self._create_schema_if_not_exists()
                self._create_tables_if_not_exists()
            self._is_initialized = True

    defput(
        self,
        key: str,
        val: dict,
        collection: str = DEFAULT_COLLECTION,
    ) -> None:
"""
        Put a key-value pair into the store.

        Args:
            key (str): key
            val (dict): value
            collection (str): collection name

        """
        self.put_all([(key, val)], collection=collection)

    async defaput(
        self,
        key: str,
        val: dict,
        collection: str = DEFAULT_COLLECTION,
    ) -> None:
"""
        Put a key-value pair into the store.

        Args:
            key (str): key
            val (dict): value
            collection (str): collection name

        """
        await self.aput_all([(key, val)], collection=collection)

    defput_all(
        self,
        kv_pairs: List[Tuple[str, dict]],
        collection: str = DEFAULT_COLLECTION,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
        fromsqlalchemy.dialects.postgresqlimport insert

        self._initialize()
        with self._session() as session:
            for i in range(0, len(kv_pairs), batch_size):
                batch = kv_pairs[i : i + batch_size]

                values_to_insert = [
                    {
                        "key": key,
                        "namespace": collection,
                        "value": value,
                    }
                    for key, value in batch
                ]

                stmt = insert(self._table_class).values(values_to_insert)
                stmt = stmt.on_conflict_do_update(
                    index_elements=["key", "namespace"],
                    set_={"value": stmt.excluded.value},
                )

                session.execute(stmt)
                session.commit()

    async defaput_all(
        self,
        kv_pairs: List[Tuple[str, dict]],
        collection: str = DEFAULT_COLLECTION,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
        fromsqlalchemy.dialects.postgresqlimport insert

        self._initialize()
        async with self._async_session() as session:
            for i in range(0, len(kv_pairs), batch_size):
                batch = kv_pairs[i : i + batch_size]

                values_to_insert = [
                    {
                        "key": key,
                        "namespace": collection,
                        "value": value,
                    }
                    for key, value in batch
                ]

                stmt = insert(self._table_class).values(values_to_insert)
                stmt = stmt.on_conflict_do_update(
                    index_elements=["key", "namespace"],
                    set_={"value": stmt.excluded.value},
                )

                await session.execute(stmt)
                await session.commit()

    defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> Optional[dict]:
"""
        Get a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        fromsqlalchemyimport select

        self._initialize()
        with self._session() as session:
            result = session.execute(
                select(self._table_class)
                .filter_by(key=key)
                .filter_by(namespace=collection)
            )
            result = result.scalars().first()
            if result:
                return result.value
        return None

    async defaget(
        self, key: str, collection: str = DEFAULT_COLLECTION
    ) -> Optional[dict]:
"""
        Get a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        fromsqlalchemyimport select

        self._initialize()
        async with self._async_session() as session:
            result = await session.execute(
                select(self._table_class)
                .filter_by(key=key)
                .filter_by(namespace=collection)
            )
            result = result.scalars().first()
            if result:
                return result.value
        return None

    defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
        Get all values from the store.

        Args:
            collection (str): collection name

        """
        fromsqlalchemyimport select

        self._initialize()
        with self._session() as session:
            results = session.execute(
                select(self._table_class).filter_by(namespace=collection)
            )
            results = results.scalars().all()
        return {result.key: result.value for result in results} if results else {}

    async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
        Get all values from the store.

        Args:
            collection (str): collection name

        """
        fromsqlalchemyimport select

        self._initialize()
        async with self._async_session() as session:
            results = await session.execute(
                select(self._table_class).filter_by(namespace=collection)
            )
            results = results.scalars().all()
        return {result.key: result.value for result in results} if results else {}

    defdelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
        Delete a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        fromsqlalchemyimport delete

        self._initialize()
        with self._session() as session:
            result = session.execute(
                delete(self._table_class)
                .filter_by(namespace=collection)
                .filter_by(key=key)
            )
            session.commit()
        return result.rowcount  0

    async defadelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
        Delete a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        fromsqlalchemyimport delete

        self._initialize()
        async with self._async_session() as session:
            async with session.begin():
                result = await session.execute(
                    delete(self._table_class)
                    .filter_by(namespace=collection)
                    .filter_by(key=key)
                )
        return result.rowcount  0

```
 |  
| --- | --- |  
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/postgres/#llama_index.storage.kvstore.postgres.PostgresKVStore.from_params "Permanent link")

```
from_params(
    host: Optional[] = None,
    port: Optional[] = None,
    database: Optional[] = None,
    user: Optional[] = None,
    password: Optional[] = None,
    table_name:  = "kvstore",
    schema_name:  = "public",
    connection_string: Optional[] = None,
    async_connection_string: Optional[] = None,
    perform_setup:  = True,
    debug:  = False,
    use_jsonb:  = False,
    create_engine_kwargs: Optional[[, ]] = None,
) -> 

```

Return connection string from database parameters.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-postgres/llama_index/storage/kvstore/postgres/base.py`  
| 
```
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
    table_name: str = "kvstore",
    schema_name: str = "public",
    connection_string: Optional[str] = None,
    async_connection_string: Optional[str] = None,
    perform_setup: bool = True,
    debug: bool = False,
    use_jsonb: bool = False,
    create_engine_kwargs: Optional[Dict[str, Any]] = None,
) -> "PostgresKVStore":
"""Return connection string from database parameters."""
    conn_str = (
        connection_string
        or f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )
    async_conn_str = async_connection_string or (
        f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
    )
    return cls(
        connection_string=conn_str,
        async_connection_string=async_conn_str,
        table_name=table_name,
        schema_name=schema_name,
        perform_setup=perform_setup,
        debug=debug,
        use_jsonb=use_jsonb,
        create_engine_kwargs=create_engine_kwargs,
    )

```
 |  
| --- | --- |  
###  from_uri `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/postgres/#llama_index.storage.kvstore.postgres.PostgresKVStore.from_uri "Permanent link")

```
from_uri(
    uri: ,
    table_name:  = "kvstore",
    schema_name:  = "public",
    perform_setup:  = True,
    debug:  = False,
    use_jsonb:  = False,
    create_engine_kwargs: Optional[[, ]] = None,
) -> 

```

Return connection string from database parameters.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-postgres/llama_index/storage/kvstore/postgres/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_uri(
    cls,
    uri: str,
    table_name: str = "kvstore",
    schema_name: str = "public",
    perform_setup: bool = True,
    debug: bool = False,
    use_jsonb: bool = False,
    create_engine_kwargs: Optional[Dict[str, Any]] = None,
) -> "PostgresKVStore":
"""Return connection string from database parameters."""
    params = params_from_uri(uri)
    return cls.from_params(
        **params,
        table_name=table_name,
        schema_name=schema_name,
        perform_setup=perform_setup,
        debug=debug,
        use_jsonb=use_jsonb,
        create_engine_kwargs=create_engine_kwargs,
    )

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/postgres/#llama_index.storage.kvstore.postgres.PostgresKVStore.put "Permanent link")

```
put(
    key: ,
    val: ,
    collection:  = DEFAULT_COLLECTION,
) -> None

```

Put a key-value pair into the store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  _required_  |  
|  `val`  |  `dict`  |  value  |  _required_  |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-postgres/llama_index/storage/kvstore/postgres/base.py`  
| 
```
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
```
 | 
```
defput(
    self,
    key: str,
    val: dict,
    collection: str = DEFAULT_COLLECTION,
) -> None:
"""
    Put a key-value pair into the store.

    Args:
        key (str): key
        val (dict): value
        collection (str): collection name

    """
    self.put_all([(key, val)], collection=collection)

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/postgres/#llama_index.storage.kvstore.postgres.PostgresKVStore.aput "Permanent link")

```
aput(
    key: ,
    val: ,
    collection:  = DEFAULT_COLLECTION,
) -> None

```

Put a key-value pair into the store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  _required_  |  
|  `val`  |  `dict`  |  value  |  _required_  |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-postgres/llama_index/storage/kvstore/postgres/base.py`  
| 
```
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
```
 | 
```
async defaput(
    self,
    key: str,
    val: dict,
    collection: str = DEFAULT_COLLECTION,
) -> None:
"""
    Put a key-value pair into the store.

    Args:
        key (str): key
        val (dict): value
        collection (str): collection name

    """
    await self.aput_all([(key, val)], collection=collection)

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/postgres/#llama_index.storage.kvstore.postgres.PostgresKVStore.get "Permanent link")

```
get(
    key: , collection:  = DEFAULT_COLLECTION
) -> Optional[]

```

Get a value from the store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  _required_  |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-postgres/llama_index/storage/kvstore/postgres/base.py`  
| 
```
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
```
 | 
```
defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> Optional[dict]:
"""
    Get a value from the store.

    Args:
        key (str): key
        collection (str): collection name

    """
    fromsqlalchemyimport select

    self._initialize()
    with self._session() as session:
        result = session.execute(
            select(self._table_class)
            .filter_by(key=key)
            .filter_by(namespace=collection)
        )
        result = result.scalars().first()
        if result:
            return result.value
    return None

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/postgres/#llama_index.storage.kvstore.postgres.PostgresKVStore.aget "Permanent link")

```
aget(
    key: , collection:  = DEFAULT_COLLECTION
) -> Optional[]

```

Get a value from the store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  _required_  |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-postgres/llama_index/storage/kvstore/postgres/base.py`  
| 
```
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
```
 | 
```
async defaget(
    self, key: str, collection: str = DEFAULT_COLLECTION
) -> Optional[dict]:
"""
    Get a value from the store.

    Args:
        key (str): key
        collection (str): collection name

    """
    fromsqlalchemyimport select

    self._initialize()
    async with self._async_session() as session:
        result = await session.execute(
            select(self._table_class)
            .filter_by(key=key)
            .filter_by(namespace=collection)
        )
        result = result.scalars().first()
        if result:
            return result.value
    return None

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/postgres/#llama_index.storage.kvstore.postgres.PostgresKVStore.get_all "Permanent link")

```
get_all(
    collection:  = DEFAULT_COLLECTION,
) -> [, ]

```

Get all values from the store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-postgres/llama_index/storage/kvstore/postgres/base.py`  
| 
```
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
```
 | 
```
defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
    Get all values from the store.

    Args:
        collection (str): collection name

    """
    fromsqlalchemyimport select

    self._initialize()
    with self._session() as session:
        results = session.execute(
            select(self._table_class).filter_by(namespace=collection)
        )
        results = results.scalars().all()
    return {result.key: result.value for result in results} if results else {}

```
 |  
| --- | --- |  
###  aget_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/postgres/#llama_index.storage.kvstore.postgres.PostgresKVStore.aget_all "Permanent link")

```
aget_all(
    collection:  = DEFAULT_COLLECTION,
) -> [, ]

```

Get all values from the store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-postgres/llama_index/storage/kvstore/postgres/base.py`  
| 
```
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
```
 | 
```
async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
    Get all values from the store.

    Args:
        collection (str): collection name

    """
    fromsqlalchemyimport select

    self._initialize()
    async with self._async_session() as session:
        results = await session.execute(
            select(self._table_class).filter_by(namespace=collection)
        )
        results = results.scalars().all()
    return {result.key: result.value for result in results} if results else {}

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/postgres/#llama_index.storage.kvstore.postgres.PostgresKVStore.delete "Permanent link")

```
delete(
    key: , collection:  = DEFAULT_COLLECTION
) -> 

```

Delete a value from the store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  _required_  |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-postgres/llama_index/storage/kvstore/postgres/base.py`  
| 
```
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
```
 | 
```
defdelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
    Delete a value from the store.

    Args:
        key (str): key
        collection (str): collection name

    """
    fromsqlalchemyimport delete

    self._initialize()
    with self._session() as session:
        result = session.execute(
            delete(self._table_class)
            .filter_by(namespace=collection)
            .filter_by(key=key)
        )
        session.commit()
    return result.rowcount  0

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/postgres/#llama_index.storage.kvstore.postgres.PostgresKVStore.adelete "Permanent link")

```
adelete(
    key: , collection:  = DEFAULT_COLLECTION
) -> 

```

Delete a value from the store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  _required_  |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-postgres/llama_index/storage/kvstore/postgres/base.py`  
| 
```
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
```
 | 
```
async defadelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
    Delete a value from the store.

    Args:
        key (str): key
        collection (str): collection name

    """
    fromsqlalchemyimport delete

    self._initialize()
    async with self._async_session() as session:
        async with session.begin():
            result = await session.execute(
                delete(self._table_class)
                .filter_by(namespace=collection)
                .filter_by(key=key)
            )
    return result.rowcount  0

```
 |  
| --- | --- |  
options: members: - PostgresKVStore
