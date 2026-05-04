# Postgres
##  PostgresChatStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/postgres/#llama_index.storage.chat_store.postgres.PostgresChatStore "Permanent link")
Bases: 
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-postgres/llama_index/storage/chat_store/postgres/base.py`  
| 
```
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
```
 | 
```
classPostgresChatStore(BaseChatStore):
    table_name: Optional[str] = Field(
        default="chatstore", description="Postgres table name."
    )
    schema_name: Optional[str] = Field(
        default="public", description="Postgres schema name."
    )

    _table_class: Optional[Any] = PrivateAttr()
    _session: Optional[sessionmaker] = PrivateAttr()
    _async_session: Optional[sessionmaker] = PrivateAttr()

    def__init__(
        self,
        session: sessionmaker,
        async_session: sessionmaker,
        table_name: str,
        schema_name: str = "public",
        use_jsonb: bool = False,
    ):
        super().__init__(
            table_name=table_name.lower(),
            schema_name=schema_name.lower(),
        )

        # Check if legacy table (with 'data_' prefix) exists
        use_legacy_table_name = self._check_legacy_table_exists(
            session, self.table_name, self.schema_name
        )

        # sqlalchemy model
        base = declarative_base()
        self._table_class = get_data_model(
            base,
            self.table_name,
            self.schema_name,
            use_jsonb=use_jsonb,
            use_legacy_table_name=use_legacy_table_name,
        )
        self._session = session
        self._async_session = async_session
        self._initialize(base)

    @classmethod
    deffrom_params(
        cls,
        host: Optional[str] = None,
        port: Optional[str] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        table_name: str = "chatstore",
        schema_name: str = "public",
        connection_string: Optional[str] = None,
        async_connection_string: Optional[str] = None,
        debug: bool = False,
        use_jsonb: bool = False,
    ) -> "PostgresChatStore":
"""Return connection string from database parameters."""
        conn_str = (
            connection_string
            or f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"
        )
        async_conn_str = async_connection_string or (
            f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
        )
        session, async_session = cls._connect(conn_str, async_conn_str, debug)
        return cls(
            session=session,
            async_session=async_session,
            table_name=table_name,
            schema_name=schema_name,
            use_jsonb=use_jsonb,
        )

    @classmethod
    deffrom_uri(
        cls,
        uri: str,
        table_name: str = "chatstore",
        schema_name: str = "public",
        debug: bool = False,
        use_jsonb: bool = False,
    ) -> "PostgresChatStore":
"""Return connection string from database parameters."""
        params = params_from_uri(uri)
        return cls.from_params(
            **params,
            table_name=table_name,
            schema_name=schema_name,
            debug=debug,
            use_jsonb=use_jsonb,
        )

    @classmethod
    def_connect(
        cls, connection_string: str, async_connection_string: str, debug: bool
    ) -> tuple[sessionmaker, sessionmaker]:
        _engine = create_engine(connection_string, echo=debug)
        session = sessionmaker(_engine)

        _async_engine = create_async_engine(async_connection_string)
        async_session = sessionmaker(_async_engine, class_=AsyncSession)
        return session, async_session

    def_check_legacy_table_exists(
        self, session: sessionmaker, table_name: str, schema_name: str
    ) -> bool:
"""
        Check if a legacy table with 'data_' prefix exists.

        Args:
            session: SQLAlchemy sessionmaker instance
            table_name: The base table name (without prefix)
            schema_name: The database schema name

        Returns:
            bool: True if the legacy table exists
                  indicating we should use the legacy naming for backward compatibility.

        """
        legacy_table_name = f"data_{table_name}"

        with session() as sess, sess.begin():
            inspector = inspect(sess.connection())
            existing_tables = inspector.get_table_names(schema=schema_name)
            return legacy_table_name in existing_tables

    def_create_schema_if_not_exists(self) -> None:
        with self._session() as session, session.begin():
            # Check if the specified schema exists with "CREATE" statement
            check_schema_statement = text(
                f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{self.schema_name}'"
            )
            result = session.execute(check_schema_statement).fetchone()

            # If the schema does not exist, then create it
            if not result:
                create_schema_statement = text(
                    f"CREATE SCHEMA IF NOT EXISTS {self.schema_name}"
                )
                session.execute(create_schema_statement)

            session.commit()

    def_create_tables_if_not_exists(self, base) -> None:
        with self._session() as session, session.begin():
            base.metadata.create_all(session.connection())

    def_initialize(self, base) -> None:
        self._create_schema_if_not_exists()
        self._create_tables_if_not_exists(base)

    defset_messages(self, key: str, messages: list[ChatMessage]) -> None:
"""Set messages for a key."""
        with self._session() as session:
            stmt = text(
                f"""
                INSERT INTO {self.schema_name}.{self._table_class.__tablename__} (key, value)
                VALUES (:key, :value)
                ON CONFLICT (key)
                DO UPDATE SET
                value = EXCLUDED.value;

            )

            params = {
                "key": key,
                "value": [message.model_dump_json() for message in messages],
            }

            # Execute the bulk upsert
            session.execute(stmt, params)
            session.commit()

    async defaset_messages(self, key: str, messages: list[ChatMessage]) -> None:
"""Async version of Get messages for a key."""
        async with self._async_session() as session:
            stmt = text(
                f"""
                INSERT INTO {self.schema_name}.{self._table_class.__tablename__} (key, value)
                VALUES (:key, :value)
                ON CONFLICT (key)
                DO UPDATE SET
                value = EXCLUDED.value;

            )

            params = {
                "key": key,
                "value": [message.model_dump_json() for message in messages],
            }

            # Execute the bulk upsert
            await session.execute(stmt, params)
            await session.commit()

    defget_messages(self, key: str) -> list[ChatMessage]:
"""Get messages for a key."""
        with self._session() as session:
            result = session.execute(select(self._table_class).filter_by(key=key))
            result = result.scalars().first()
            if result:
                return [
                    ChatMessage.model_validate(removed_message)
                    for removed_message in result.value
                ]
            return []

    async defaget_messages(self, key: str) -> list[ChatMessage]:
"""Async version of Get messages for a key."""
        async with self._async_session() as session:
            result = await session.execute(select(self._table_class).filter_by(key=key))
            result = result.scalars().first()
            if result:
                return [
                    ChatMessage.model_validate(removed_message)
                    for removed_message in result.value
                ]
            return []

    defadd_message(self, key: str, message: ChatMessage) -> None:
"""Add a message for a key."""
        with self._session() as session:
            stmt = text(
                f"""
                INSERT INTO {self.schema_name}.{self._table_class.__tablename__} (key, value)
                VALUES (:key, :value)
                ON CONFLICT (key)
                DO UPDATE SET
                    value = array_cat({self._table_class.__tablename__}.value, :value);

            )
            params = {"key": key, "value": [message.model_dump_json()]}
            session.execute(stmt, params)
            session.commit()

    async defasync_add_message(self, key: str, message: ChatMessage) -> None:
"""Async version of Add a message for a key."""
        async with self._async_session() as session:
            stmt = text(
                f"""
                INSERT INTO {self.schema_name}.{self._table_class.__tablename__} (key, value)
                VALUES (:key, :value)
                ON CONFLICT (key)
                DO UPDATE SET
                    value = array_cat({self._table_class.__tablename__}.value, :value);

            )
            params = {"key": key, "value": [message.model_dump_json()]}
            await session.execute(stmt, params)
            await session.commit()

    defdelete_messages(self, key: str) -> Optional[list[ChatMessage]]:
"""Delete messages for a key."""
        with self._session() as session:
            session.execute(delete(self._table_class).filter_by(key=key))
            session.commit()
        return None

    async defadelete_messages(self, key: str) -> Optional[list[ChatMessage]]:
"""Async version of Delete messages for a key."""
        async with self._async_session() as session:
            await session.execute(delete(self._table_class).filter_by(key=key))
            await session.commit()
        return None

    defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
        with self._session() as session:
            # First, retrieve the current list of messages
            stmt = select(self._table_class.value).where(self._table_class.key == key)
            result = session.execute(stmt).scalar_one_or_none()

            if result is None or idx  0 or idx >= len(result):
                # If the key doesn't exist or the index is out of bounds
                return None

            # Remove the message at the given index
            removed_message = result[idx]

            stmt = text(
                f"""
                UPDATE {self._table_class.__tablename__}
                SET value = array_cat(
{self._table_class.__tablename__}.value[: :idx],
{self._table_class.__tablename__}.value[:idx+2:]

                WHERE key = :key;

            )

            params = {"key": key, "idx": idx}
            session.execute(stmt, params)
            session.commit()

            return ChatMessage.model_validate(removed_message)

    async defadelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Async version of Delete specific message for a key."""
        async with self._async_session() as session:
            # First, retrieve the current list of messages
            stmt = select(self._table_class.value).where(self._table_class.key == key)
            result = (await session.execute(stmt)).scalar_one_or_none()

            if result is None or idx  0 or idx >= len(result):
                # If the key doesn't exist or the index is out of bounds
                return None

            # Remove the message at the given index
            removed_message = result[idx]

            stmt = text(
                f"""
                UPDATE {self._table_class.__tablename__}
                SET value = array_cat(
{self._table_class.__tablename__}.value[: :idx],
{self._table_class.__tablename__}.value[:idx+2:]

                WHERE key = :key;

            )

            params = {"key": key, "idx": idx}
            await session.execute(stmt, params)
            await session.commit()

            return ChatMessage.model_validate(removed_message)

    defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete last message for a key."""
        with self._session() as session:
            # First, retrieve the current list of messages
            stmt = select(self._table_class.value).where(self._table_class.key == key)
            result = session.execute(stmt).scalar_one_or_none()

            if result is None or len(result) == 0:
                # If the key doesn't exist or the array is empty
                return None

            # Remove the message at the given index
            removed_message = result[-1]

            stmt = text(
                f"""
                UPDATE {self._table_class.__tablename__}
                SET value = value[1:array_length(value, 1) - 1]
                WHERE key = :key;

            )
            params = {"key": key}
            session.execute(stmt, params)
            session.commit()

            return ChatMessage.model_validate(removed_message)

    async defadelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Async version of Delete last message for a key."""
        async with self._async_session() as session:
            # First, retrieve the current list of messages
            stmt = select(self._table_class.value).where(self._table_class.key == key)
            result = (await session.execute(stmt)).scalar_one_or_none()

            if result is None or len(result) == 0:
                # If the key doesn't exist or the array is empty
                return None

            # Remove the message at the given index
            removed_message = result[-1]

            stmt = text(
                f"""
                        UPDATE {self._table_class.__tablename__}
                        SET value = value[1:array_length(value, 1) - 1]
                        WHERE key = :key;

            )
            params = {"key": key}
            await session.execute(stmt, params)
            await session.commit()

            return ChatMessage.model_validate(removed_message)

    defget_keys(self) -> list[str]:
"""Get all keys."""
        with self._session() as session:
            stmt = select(self._table_class.key)

            return session.execute(stmt).scalars().all()

    async defaget_keys(self) -> list[str]:
"""Async version of Get all keys."""
        async with self._async_session() as session:
            stmt = select(self._table_class.key)

            return (await session.execute(stmt)).scalars().all()

```
 |  
| --- | --- |  
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/postgres/#llama_index.storage.chat_store.postgres.PostgresChatStore.from_params "Permanent link")

```
from_params(
    host: Optional[] = None,
    port: Optional[] = None,
    database: Optional[] = None,
    user: Optional[] = None,
    password: Optional[] = None,
    table_name:  = "chatstore",
    schema_name:  = "public",
    connection_string: Optional[] = None,
    async_connection_string: Optional[] = None,
    debug:  = False,
    use_jsonb:  = False,
) -> 

```

Return connection string from database parameters.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-postgres/llama_index/storage/chat_store/postgres/base.py`  
| 
```
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
    table_name: str = "chatstore",
    schema_name: str = "public",
    connection_string: Optional[str] = None,
    async_connection_string: Optional[str] = None,
    debug: bool = False,
    use_jsonb: bool = False,
) -> "PostgresChatStore":
"""Return connection string from database parameters."""
    conn_str = (
        connection_string
        or f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"
    )
    async_conn_str = async_connection_string or (
        f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
    )
    session, async_session = cls._connect(conn_str, async_conn_str, debug)
    return cls(
        session=session,
        async_session=async_session,
        table_name=table_name,
        schema_name=schema_name,
        use_jsonb=use_jsonb,
    )

```
 |  
| --- | --- |  
###  from_uri `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/postgres/#llama_index.storage.chat_store.postgres.PostgresChatStore.from_uri "Permanent link")

```
from_uri(
    uri: ,
    table_name:  = "chatstore",
    schema_name:  = "public",
    debug:  = False,
    use_jsonb:  = False,
) -> 

```

Return connection string from database parameters.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-postgres/llama_index/storage/chat_store/postgres/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_uri(
    cls,
    uri: str,
    table_name: str = "chatstore",
    schema_name: str = "public",
    debug: bool = False,
    use_jsonb: bool = False,
) -> "PostgresChatStore":
"""Return connection string from database parameters."""
    params = params_from_uri(uri)
    return cls.from_params(
        **params,
        table_name=table_name,
        schema_name=schema_name,
        debug=debug,
        use_jsonb=use_jsonb,
    )

```
 |  
| --- | --- |  
###  set_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/postgres/#llama_index.storage.chat_store.postgres.PostgresChatStore.set_messages "Permanent link")

```
set_messages(key: , messages: []) -> None

```

Set messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-postgres/llama_index/storage/chat_store/postgres/base.py`  
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
```
 | 
```
defset_messages(self, key: str, messages: list[ChatMessage]) -> None:
"""Set messages for a key."""
    with self._session() as session:
        stmt = text(
            f"""
            INSERT INTO {self.schema_name}.{self._table_class.__tablename__} (key, value)
            VALUES (:key, :value)
            ON CONFLICT (key)
            DO UPDATE SET
            value = EXCLUDED.value;

        )

        params = {
            "key": key,
            "value": [message.model_dump_json() for message in messages],
        }

        # Execute the bulk upsert
        session.execute(stmt, params)
        session.commit()

```
 |  
| --- | --- |  
###  aset_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/postgres/#llama_index.storage.chat_store.postgres.PostgresChatStore.aset_messages "Permanent link")

```
aset_messages(
    key: , messages: []
) -> None

```

Async version of Get messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-postgres/llama_index/storage/chat_store/postgres/base.py`  
| 
```
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
```
 | 
```
async defaset_messages(self, key: str, messages: list[ChatMessage]) -> None:
"""Async version of Get messages for a key."""
    async with self._async_session() as session:
        stmt = text(
            f"""
            INSERT INTO {self.schema_name}.{self._table_class.__tablename__} (key, value)
            VALUES (:key, :value)
            ON CONFLICT (key)
            DO UPDATE SET
            value = EXCLUDED.value;

        )

        params = {
            "key": key,
            "value": [message.model_dump_json() for message in messages],
        }

        # Execute the bulk upsert
        await session.execute(stmt, params)
        await session.commit()

```
 |  
| --- | --- |  
###  get_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/postgres/#llama_index.storage.chat_store.postgres.PostgresChatStore.get_messages "Permanent link")

```
get_messages(key: ) -> []

```

Get messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-postgres/llama_index/storage/chat_store/postgres/base.py`  
| 
```
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
```
 | 
```
defget_messages(self, key: str) -> list[ChatMessage]:
"""Get messages for a key."""
    with self._session() as session:
        result = session.execute(select(self._table_class).filter_by(key=key))
        result = result.scalars().first()
        if result:
            return [
                ChatMessage.model_validate(removed_message)
                for removed_message in result.value
            ]
        return []

```
 |  
| --- | --- |  
###  aget_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/postgres/#llama_index.storage.chat_store.postgres.PostgresChatStore.aget_messages "Permanent link")

```
aget_messages(key: ) -> []

```

Async version of Get messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-postgres/llama_index/storage/chat_store/postgres/base.py`  
| 
```
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
async defaget_messages(self, key: str) -> list[ChatMessage]:
"""Async version of Get messages for a key."""
    async with self._async_session() as session:
        result = await session.execute(select(self._table_class).filter_by(key=key))
        result = result.scalars().first()
        if result:
            return [
                ChatMessage.model_validate(removed_message)
                for removed_message in result.value
            ]
        return []

```
 |  
| --- | --- |  
###  add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/postgres/#llama_index.storage.chat_store.postgres.PostgresChatStore.add_message "Permanent link")

```
add_message(key: , message: ) -> None

```

Add a message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-postgres/llama_index/storage/chat_store/postgres/base.py`  
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
```
 | 
```
defadd_message(self, key: str, message: ChatMessage) -> None:
"""Add a message for a key."""
    with self._session() as session:
        stmt = text(
            f"""
            INSERT INTO {self.schema_name}.{self._table_class.__tablename__} (key, value)
            VALUES (:key, :value)
            ON CONFLICT (key)
            DO UPDATE SET
                value = array_cat({self._table_class.__tablename__}.value, :value);

        )
        params = {"key": key, "value": [message.model_dump_json()]}
        session.execute(stmt, params)
        session.commit()

```
 |  
| --- | --- |  
###  async_add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/postgres/#llama_index.storage.chat_store.postgres.PostgresChatStore.async_add_message "Permanent link")

```
async_add_message(key: , message: ) -> None

```

Async version of Add a message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-postgres/llama_index/storage/chat_store/postgres/base.py`  
| 
```
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
```
 | 
```
async defasync_add_message(self, key: str, message: ChatMessage) -> None:
"""Async version of Add a message for a key."""
    async with self._async_session() as session:
        stmt = text(
            f"""
            INSERT INTO {self.schema_name}.{self._table_class.__tablename__} (key, value)
            VALUES (:key, :value)
            ON CONFLICT (key)
            DO UPDATE SET
                value = array_cat({self._table_class.__tablename__}.value, :value);

        )
        params = {"key": key, "value": [message.model_dump_json()]}
        await session.execute(stmt, params)
        await session.commit()

```
 |  
| --- | --- |  
###  delete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/postgres/#llama_index.storage.chat_store.postgres.PostgresChatStore.delete_messages "Permanent link")

```
delete_messages(key: ) -> Optional[[]]

```

Delete messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-postgres/llama_index/storage/chat_store/postgres/base.py`  
| 
```
324
325
326
327
328
329
```
 | 
```
defdelete_messages(self, key: str) -> Optional[list[ChatMessage]]:
"""Delete messages for a key."""
    with self._session() as session:
        session.execute(delete(self._table_class).filter_by(key=key))
        session.commit()
    return None

```
 |  
| --- | --- |  
###  adelete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/postgres/#llama_index.storage.chat_store.postgres.PostgresChatStore.adelete_messages "Permanent link")

```
adelete_messages(key: ) -> Optional[[]]

```

Async version of Delete messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-postgres/llama_index/storage/chat_store/postgres/base.py`  
| 
```
331
332
333
334
335
336
```
 | 
```
async defadelete_messages(self, key: str) -> Optional[list[ChatMessage]]:
"""Async version of Delete messages for a key."""
    async with self._async_session() as session:
        await session.execute(delete(self._table_class).filter_by(key=key))
        await session.commit()
    return None

```
 |  
| --- | --- |  
###  delete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/postgres/#llama_index.storage.chat_store.postgres.PostgresChatStore.delete_message "Permanent link")

```
delete_message(key: , idx: ) -> Optional[]

```

Delete specific message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-postgres/llama_index/storage/chat_store/postgres/base.py`  
| 
```
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
```
 | 
```
defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
    with self._session() as session:
        # First, retrieve the current list of messages
        stmt = select(self._table_class.value).where(self._table_class.key == key)
        result = session.execute(stmt).scalar_one_or_none()

        if result is None or idx  0 or idx >= len(result):
            # If the key doesn't exist or the index is out of bounds
            return None

        # Remove the message at the given index
        removed_message = result[idx]

        stmt = text(
            f"""
            UPDATE {self._table_class.__tablename__}
            SET value = array_cat(
{self._table_class.__tablename__}.value[: :idx],
{self._table_class.__tablename__}.value[:idx+2:]

            WHERE key = :key;

        )

        params = {"key": key, "idx": idx}
        session.execute(stmt, params)
        session.commit()

        return ChatMessage.model_validate(removed_message)

```
 |  
| --- | --- |  
###  adelete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/postgres/#llama_index.storage.chat_store.postgres.PostgresChatStore.adelete_message "Permanent link")

```
adelete_message(
    key: , idx: 
) -> Optional[]

```

Async version of Delete specific message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-postgres/llama_index/storage/chat_store/postgres/base.py`  
| 
```
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
```
 | 
```
async defadelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Async version of Delete specific message for a key."""
    async with self._async_session() as session:
        # First, retrieve the current list of messages
        stmt = select(self._table_class.value).where(self._table_class.key == key)
        result = (await session.execute(stmt)).scalar_one_or_none()

        if result is None or idx  0 or idx >= len(result):
            # If the key doesn't exist or the index is out of bounds
            return None

        # Remove the message at the given index
        removed_message = result[idx]

        stmt = text(
            f"""
            UPDATE {self._table_class.__tablename__}
            SET value = array_cat(
{self._table_class.__tablename__}.value[: :idx],
{self._table_class.__tablename__}.value[:idx+2:]

            WHERE key = :key;

        )

        params = {"key": key, "idx": idx}
        await session.execute(stmt, params)
        await session.commit()

        return ChatMessage.model_validate(removed_message)

```
 |  
| --- | --- |  
###  delete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/postgres/#llama_index.storage.chat_store.postgres.PostgresChatStore.delete_last_message "Permanent link")

```
delete_last_message(key: ) -> Optional[]

```

Delete last message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-postgres/llama_index/storage/chat_store/postgres/base.py`  
| 
```
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
```
 | 
```
defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete last message for a key."""
    with self._session() as session:
        # First, retrieve the current list of messages
        stmt = select(self._table_class.value).where(self._table_class.key == key)
        result = session.execute(stmt).scalar_one_or_none()

        if result is None or len(result) == 0:
            # If the key doesn't exist or the array is empty
            return None

        # Remove the message at the given index
        removed_message = result[-1]

        stmt = text(
            f"""
            UPDATE {self._table_class.__tablename__}
            SET value = value[1:array_length(value, 1) - 1]
            WHERE key = :key;

        )
        params = {"key": key}
        session.execute(stmt, params)
        session.commit()

        return ChatMessage.model_validate(removed_message)

```
 |  
| --- | --- |  
###  adelete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/postgres/#llama_index.storage.chat_store.postgres.PostgresChatStore.adelete_last_message "Permanent link")

```
adelete_last_message(key: ) -> Optional[]

```

Async version of Delete last message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-postgres/llama_index/storage/chat_store/postgres/base.py`  
| 
```
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
```
 | 
```
async defadelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Async version of Delete last message for a key."""
    async with self._async_session() as session:
        # First, retrieve the current list of messages
        stmt = select(self._table_class.value).where(self._table_class.key == key)
        result = (await session.execute(stmt)).scalar_one_or_none()

        if result is None or len(result) == 0:
            # If the key doesn't exist or the array is empty
            return None

        # Remove the message at the given index
        removed_message = result[-1]

        stmt = text(
            f"""
                    UPDATE {self._table_class.__tablename__}
                    SET value = value[1:array_length(value, 1) - 1]
                    WHERE key = :key;

        )
        params = {"key": key}
        await session.execute(stmt, params)
        await session.commit()

        return ChatMessage.model_validate(removed_message)

```
 |  
| --- | --- |  
###  get_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/postgres/#llama_index.storage.chat_store.postgres.PostgresChatStore.get_keys "Permanent link")

```
get_keys() -> []

```

Get all keys.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-postgres/llama_index/storage/chat_store/postgres/base.py`  
| 
```
454
455
456
457
458
459
```
 | 
```
defget_keys(self) -> list[str]:
"""Get all keys."""
    with self._session() as session:
        stmt = select(self._table_class.key)

        return session.execute(stmt).scalars().all()

```
 |  
| --- | --- |  
###  aget_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/postgres/#llama_index.storage.chat_store.postgres.PostgresChatStore.aget_keys "Permanent link")

```
aget_keys() -> []

```

Async version of Get all keys.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-postgres/llama_index/storage/chat_store/postgres/base.py`  
| 
```
461
462
463
464
465
466
```
 | 
```
async defaget_keys(self) -> list[str]:
"""Async version of Get all keys."""
    async with self._async_session() as session:
        stmt = select(self._table_class.key)

        return (await session.execute(stmt)).scalars().all()

```
 |  
| --- | --- |  
options: members: - PostgresChatStore
