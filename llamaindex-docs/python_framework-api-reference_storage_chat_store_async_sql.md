# Async sql
##  SQLAlchemyChatStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/async_sql/#llama_index.core.storage.chat_store.sql.SQLAlchemyChatStore "Permanent link")
Bases: `AsyncDBChatStore`
Base class for SQLAlchemy-based chat stores.
This class provides a foundation for creating chat stores that use SQLAlchemy to interact with SQL databases. It handles common operations like managing sessions, creating tables, and CRUD operations on chat messages.
Enhanced with status tracking for better FIFO queue management for short-term memory.
This class is meant to replace all other chat store classes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `table_name`  |  Name of the table to store messages  |  _required_  |  
|  `async_database_uri`  |  SQLAlchemy async connection URI  |  `'sqlite+aiosqlite:///:memory:'`  |  
|  `db_schema`  |  `str | None`  |  Database schema name (for PostgreSQL and other databases that support schemas)  |  `None`  |  
Source code in `llama-index-core/llama_index/core/storage/chat_store/sql.py`  
| 
```
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
```
 | 
```
classSQLAlchemyChatStore(AsyncDBChatStore):
"""
    Base class for SQLAlchemy-based chat stores.

    This class provides a foundation for creating chat stores that use SQLAlchemy
    to interact with SQL databases. It handles common operations like managing
    sessions, creating tables, and CRUD operations on chat messages.

    Enhanced with status tracking for better FIFO queue management for short-term memory.

    This class is meant to replace all other chat store classes.
    """

    table_name: str = Field(description="Name of the table to store messages")
    async_database_uri: str = Field(
        default=DEFAULT_ASYNC_DATABASE_URI,
        description="SQLAlchemy async connection URI",
    )
    db_schema: Optional[str] = Field(
        default=None,
        description="Database schema name (for PostgreSQL and other databases that support schemas)",
    )

    _async_engine: Optional[AsyncEngine] = PrivateAttr(default=None)
    _async_session_factory: Optional[sessionmaker] = PrivateAttr(default=None)
    _metadata: MetaData = PrivateAttr(default_factory=MetaData)
    _table: Optional[Table] = PrivateAttr(default=None)
    _db_data: Optional[List[Dict[str, Any]]] = PrivateAttr(default=None)

    def__init__(
        self,
        table_name: str,
        async_database_uri: Optional[str] = DEFAULT_ASYNC_DATABASE_URI,
        async_engine: Optional[AsyncEngine] = None,
        db_data: Optional[List[Dict[str, Any]]] = None,
        db_schema: Optional[str] = None,
    ):
"""Initialize the SQLAlchemy chat store."""
        super().__init__(
            table_name=table_name,
            async_database_uri=async_database_uri or DEFAULT_ASYNC_DATABASE_URI,
            db_schema=db_schema,
        )
        self._async_engine = async_engine
        self._db_data = db_data

    @staticmethod
    def_is_in_memory_uri(uri: Optional[str]) -> bool:
"""Check if the URI points to an in-memory SQLite database."""
        # Handles both :memory: and empty path which also means in-memory for sqlite
        return uri == "sqlite+aiosqlite:///:memory:" or uri == "sqlite+aiosqlite://"

    def_is_sqlite_database(self) -> bool:
"""Check if the database is SQLite (which doesn't support schemas)."""
        if self._async_engine is not None:
            return str(self._async_engine.url).startswith("sqlite")
        return self.async_database_uri.startswith("sqlite")

    async def_initialize(self) -> Tuple[sessionmaker, Table]:
"""Initialize the chat store. Used to avoid HTTP connections in constructor."""
        if self._async_session_factory is not None and self._table is not None:
            return self._async_session_factory, self._table

        async_engine, async_session_factory = await self._setup_connections()
        table = await self._setup_tables(async_engine)

        # Restore data from in-memory database if provided
        if self._db_data:
            async with async_session_factory() as session:
                await session.execute(insert(table).values(self._db_data))
                await session.commit()

                # clear the data after it's inserted
                self._db_data = None

        return async_session_factory, table

    async def_setup_connections(
        self,
    ) -> Tuple[AsyncEngine, sessionmaker]:
"""Set up database connections and session factories."""
        # Create async engine and session factory if async URI is provided
        if self._async_session_factory is not None and self._async_engine is not None:
            return self._async_engine, self._async_session_factory
        elif self.async_database_uri or self._async_engine:
            self._async_engine = self._async_engine or create_async_engine(
                self.async_database_uri
            )
            if self.async_database_uri is None:
                self.async_database_uri = self._async_engine.url

            self._async_session_factory = sessionmaker(  # type: ignore
                bind=self._async_engine, expire_on_commit=False, class_=AsyncSession
            )

            return self._async_engine, self._async_session_factory  # type: ignore
        else:
            raise ValueError(
                "No async database URI or engine provided, cannot initialize DB sessionmaker"
            )

    async def_setup_tables(self, async_engine: AsyncEngine) -> Table:
"""Set up database tables."""
        # Create metadata with schema
        if self.db_schema is not None and not self._is_sqlite_database():
            # Only set schema for databases that support it
            self._metadata = MetaData(schema=self.db_schema)

            # Create schema if it doesn't exist (PostgreSQL, SQL Server, etc.)
            async with async_engine.begin() as conn:
                await conn.execute(
                    text(f'CREATE SCHEMA IF NOT EXISTS "{self.db_schema}"')
                )

        # Create messages table with status column
        self._table = Table(
            f"{self.table_name}",
            self._metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("key", String, nullable=False, index=True),
            Column("timestamp", BigInteger, nullable=False, index=True),
            Column("role", String, nullable=False),
            Column(
                "status",
                String,
                nullable=False,
                default=MessageStatus.ACTIVE.value,
                index=True,
            ),
            Column("data", JSON, nullable=False),
        )

        # Create tables in the database
        async with async_engine.begin() as conn:
            await conn.run_sync(self._metadata.create_all)

        return self._table

    async defget_messages(
        self,
        key: str,
        status: Optional[MessageStatus] = MessageStatus.ACTIVE,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[ChatMessage]:
"""
        Get all messages for a key with the specified status (async).

        Returns a list of messages.
        """
        session_factory, table = await self._initialize()

        query = select(table).where(table.c.key == key)

        if limit is not None:
            query = query.limit(limit)

        if offset is not None:
            query = query.offset(offset)

        if status is not None:
            query = query.where(table.c.status == status.value)

        async with session_factory() as session:
            result = await session.execute(
                query.order_by(table.c.timestamp, table.c.id)
            )
            rows = result.fetchall()

            return [ChatMessage.model_validate(row.data) for row in rows]

    async defcount_messages(
        self,
        key: str,
        status: Optional[MessageStatus] = MessageStatus.ACTIVE,
    ) -> int:
"""Count messages for a key with the specified status (async)."""
        session_factory, table = await self._initialize()

        query = select(table.c.id).where(table.c.key == key)

        if status is not None:
            query = query.where(table.c.status == status.value)

        async with session_factory() as session:
            result = await session.execute(query)
            rows = result.fetchall()
            return len(rows)

    async defadd_message(
        self,
        key: str,
        message: ChatMessage,
        status: MessageStatus = MessageStatus.ACTIVE,
    ) -> None:
"""Add a message for a key with the specified status (async)."""
        session_factory, table = await self._initialize()

        async with session_factory() as session:
            await session.execute(
                insert(table).values(
                    key=key,
                    timestamp=time.time_ns(),
                    role=message.role,
                    status=status.value,
                    data=message.model_dump(mode="json"),
                )
            )
            await session.commit()

    async defadd_messages(
        self,
        key: str,
        messages: List[ChatMessage],
        status: MessageStatus = MessageStatus.ACTIVE,
    ) -> None:
"""Add a list of messages in batch for the specified key and status (async)."""
        session_factory, table = await self._initialize()

        async with session_factory() as session:
            await session.execute(
                insert(table).values(
                    [
                        {
                            "key": key,
                            "timestamp": time.time_ns() + i,
                            "role": message.role,
                            "status": status.value,
                            "data": message.model_dump(mode="json"),
                        }
                        for i, message in enumerate(messages)
                    ]
                )
            )
            await session.commit()

    async defset_messages(
        self,
        key: str,
        messages: List[ChatMessage],
        status: MessageStatus = MessageStatus.ACTIVE,
    ) -> None:
"""Set all messages for a key (replacing existing ones) with the specified status (async)."""
        session_factory, table = await self._initialize()

        # First delete all existing messages
        await self.delete_messages(key)

        # Then add new messages
        current_time = time.time_ns()

        async with session_factory() as session:
            for i, message in enumerate(messages):
                await session.execute(
                    insert(table).values(
                        key=key,
                        # Preserve order with incremental timestamps
                        timestamp=current_time + i,
                        role=message.role,
                        status=status.value,
                        data=message.model_dump(mode="json"),
                    )
                )
            await session.commit()

    async defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete a specific message by ID and return it (async)."""
        session_factory, table = await self._initialize()

        async with session_factory() as session:
            # First get the message
            result = await session.execute(
                select(table).where(table.c.key == key, table.c.id == idx)
            )
            row = result.fetchone()

            if not row:
                return None

            # Store the message we're about to delete
            message = ChatMessage.model_validate(row.data)

            # Delete the message
            await session.execute(delete(table).where(table.c.id == idx))
            await session.commit()

            return message

    async defdelete_messages(
        self, key: str, status: Optional[MessageStatus] = None
    ) -> None:
"""Delete all messages for a key with the specified status (async)."""
        session_factory, table = await self._initialize()

        query = delete(table).where(table.c.key == key)

        if status is not None:
            query = query.where(table.c.status == status.value)

        async with session_factory() as session:
            await session.execute(query)
            await session.commit()

    async defdelete_oldest_messages(self, key: str, n: int) -> List[ChatMessage]:
"""Delete the oldest n messages for a key and return them (async)."""
        session_factory, table = await self._initialize()

        oldest_messages = []

        async with session_factory() as session:
            # First get the oldest n messages
            result = await session.execute(
                select(table)
                .where(
                    table.c.key == key,
                    table.c.status == MessageStatus.ACTIVE.value,
                )
                .order_by(table.c.timestamp, table.c.id)
                .limit(n)
            )
            rows = result.fetchall()

            if not rows:
                return []

            # Store the messages we're about to delete
            oldest_messages = [ChatMessage.model_validate(row.data) for row in rows]

            # Get the IDs to delete
            ids_to_delete = [row.id for row in rows]

            # Delete the messages
            await session.execute(delete(table).where(table.c.id.in_(ids_to_delete)))
            await session.commit()

        return oldest_messages

    async defarchive_oldest_messages(self, key: str, n: int) -> List[ChatMessage]:
"""Archive the oldest n messages for a key and return them (async)."""
        session_factory, table = await self._initialize()

        async with session_factory() as session:
            # First get the oldest n messages
            result = await session.execute(
                select(table)
                .where(
                    table.c.key == key,
                    table.c.status == MessageStatus.ACTIVE.value,
                )
                .order_by(table.c.timestamp, table.c.id)
                .limit(n)
            )
            rows = result.fetchall()

            if not rows:
                return []

            # Store the messages we're about to archive
            archived_messages = [ChatMessage.model_validate(row.data) for row in rows]

            # Get the IDs to archive
            ids_to_archive = [row.id for row in rows]

            # Update message status to archived
            await session.execute(
                update(table)
                .where(table.c.id.in_(ids_to_archive))
                .values(status=MessageStatus.ARCHIVED.value)
            )
            await session.commit()

        return archived_messages

    async defget_keys(self) -> List[str]:
"""Get all unique keys in the store (async)."""
        session_factory, table = await self._initialize()

        async with session_factory() as session:
            result = await session.execute(select(table.c.key).distinct())
            return [row[0] for row in result.fetchall()]

    async def_dump_db_data(self) -> List[Dict[str, Any]]:
"""Dump the data from the database."""
        session_factory, table = await self._initialize()

        async with session_factory() as session:
            result = await session.execute(select(table))
            rows = result.fetchall()
            return [
                {
                    "key": row.key,
                    "timestamp": row.timestamp,
                    "role": row.role,
                    "status": row.status,
                    "data": row.data,
                }
                for row in rows
            ]

    @model_serializer()
    defdump_store(self) -> dict:
"""
        Dump the store's configuration and data (if in-memory).

        Returns:
            A dictionary containing the store's configuration and potentially its data.

        """
        dump_data = {
            "table_name": self.table_name,
            "async_database_uri": self.async_database_uri,
            "db_schema": self.db_schema,
        }

        if self._is_in_memory_uri(self.async_database_uri):
            # switch to sync sqlite
            dump_data["db_data"] = asyncio_run(self._dump_db_data())

        return dump_data

    @classmethod
    defclass_name(cls) -> str:
"""Return the class name."""
        return "SQLAlchemyChatStore"

```
 |  
| --- | --- |  
###  get_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/async_sql/#llama_index.core.storage.chat_store.sql.SQLAlchemyChatStore.get_messages "Permanent link")

```
get_messages(
    key: ,
    status: Optional[MessageStatus] = ACTIVE,
    limit: Optional[] = None,
    offset: Optional[] = None,
) -> []

```

Get all messages for a key with the specified status (async).
Returns a list of messages.
Source code in `llama-index-core/llama_index/core/storage/chat_store/sql.py`  
| 
```
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
```
 | 
```
async defget_messages(
    self,
    key: str,
    status: Optional[MessageStatus] = MessageStatus.ACTIVE,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[ChatMessage]:
"""
    Get all messages for a key with the specified status (async).

    Returns a list of messages.
    """
    session_factory, table = await self._initialize()

    query = select(table).where(table.c.key == key)

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if status is not None:
        query = query.where(table.c.status == status.value)

    async with session_factory() as session:
        result = await session.execute(
            query.order_by(table.c.timestamp, table.c.id)
        )
        rows = result.fetchall()

        return [ChatMessage.model_validate(row.data) for row in rows]

```
 |  
| --- | --- |  
###  count_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/async_sql/#llama_index.core.storage.chat_store.sql.SQLAlchemyChatStore.count_messages "Permanent link")

```
count_messages(
    key: , status: Optional[MessageStatus] = ACTIVE
) -> 

```

Count messages for a key with the specified status (async).
Source code in `llama-index-core/llama_index/core/storage/chat_store/sql.py`  
| 
```
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
async defcount_messages(
    self,
    key: str,
    status: Optional[MessageStatus] = MessageStatus.ACTIVE,
) -> int:
"""Count messages for a key with the specified status (async)."""
    session_factory, table = await self._initialize()

    query = select(table.c.id).where(table.c.key == key)

    if status is not None:
        query = query.where(table.c.status == status.value)

    async with session_factory() as session:
        result = await session.execute(query)
        rows = result.fetchall()
        return len(rows)

```
 |  
| --- | --- |  
###  add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/async_sql/#llama_index.core.storage.chat_store.sql.SQLAlchemyChatStore.add_message "Permanent link")

```
add_message(
    key: ,
    message: ,
    status: MessageStatus = ACTIVE,
) -> None

```

Add a message for a key with the specified status (async).
Source code in `llama-index-core/llama_index/core/storage/chat_store/sql.py`  
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
```
 | 
```
async defadd_message(
    self,
    key: str,
    message: ChatMessage,
    status: MessageStatus = MessageStatus.ACTIVE,
) -> None:
"""Add a message for a key with the specified status (async)."""
    session_factory, table = await self._initialize()

    async with session_factory() as session:
        await session.execute(
            insert(table).values(
                key=key,
                timestamp=time.time_ns(),
                role=message.role,
                status=status.value,
                data=message.model_dump(mode="json"),
            )
        )
        await session.commit()

```
 |  
| --- | --- |  
###  add_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/async_sql/#llama_index.core.storage.chat_store.sql.SQLAlchemyChatStore.add_messages "Permanent link")

```
add_messages(
    key: ,
    messages: [],
    status: MessageStatus = ACTIVE,
) -> None

```

Add a list of messages in batch for the specified key and status (async).
Source code in `llama-index-core/llama_index/core/storage/chat_store/sql.py`  
| 
```
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
```
 | 
```
async defadd_messages(
    self,
    key: str,
    messages: List[ChatMessage],
    status: MessageStatus = MessageStatus.ACTIVE,
) -> None:
"""Add a list of messages in batch for the specified key and status (async)."""
    session_factory, table = await self._initialize()

    async with session_factory() as session:
        await session.execute(
            insert(table).values(
                [
                    {
                        "key": key,
                        "timestamp": time.time_ns() + i,
                        "role": message.role,
                        "status": status.value,
                        "data": message.model_dump(mode="json"),
                    }
                    for i, message in enumerate(messages)
                ]
            )
        )
        await session.commit()

```
 |  
| --- | --- |  
###  set_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/async_sql/#llama_index.core.storage.chat_store.sql.SQLAlchemyChatStore.set_messages "Permanent link")

```
set_messages(
    key: ,
    messages: [],
    status: MessageStatus = ACTIVE,
) -> None

```

Set all messages for a key (replacing existing ones) with the specified status (async).
Source code in `llama-index-core/llama_index/core/storage/chat_store/sql.py`  
| 
```
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
```
 | 
```
async defset_messages(
    self,
    key: str,
    messages: List[ChatMessage],
    status: MessageStatus = MessageStatus.ACTIVE,
) -> None:
"""Set all messages for a key (replacing existing ones) with the specified status (async)."""
    session_factory, table = await self._initialize()

    # First delete all existing messages
    await self.delete_messages(key)

    # Then add new messages
    current_time = time.time_ns()

    async with session_factory() as session:
        for i, message in enumerate(messages):
            await session.execute(
                insert(table).values(
                    key=key,
                    # Preserve order with incremental timestamps
                    timestamp=current_time + i,
                    role=message.role,
                    status=status.value,
                    data=message.model_dump(mode="json"),
                )
            )
        await session.commit()

```
 |  
| --- | --- |  
###  delete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/async_sql/#llama_index.core.storage.chat_store.sql.SQLAlchemyChatStore.delete_message "Permanent link")

```
delete_message(key: , idx: ) -> Optional[]

```

Delete a specific message by ID and return it (async).
Source code in `llama-index-core/llama_index/core/storage/chat_store/sql.py`  
| 
```
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
```
 | 
```
async defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete a specific message by ID and return it (async)."""
    session_factory, table = await self._initialize()

    async with session_factory() as session:
        # First get the message
        result = await session.execute(
            select(table).where(table.c.key == key, table.c.id == idx)
        )
        row = result.fetchone()

        if not row:
            return None

        # Store the message we're about to delete
        message = ChatMessage.model_validate(row.data)

        # Delete the message
        await session.execute(delete(table).where(table.c.id == idx))
        await session.commit()

        return message

```
 |  
| --- | --- |  
###  delete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/async_sql/#llama_index.core.storage.chat_store.sql.SQLAlchemyChatStore.delete_messages "Permanent link")

```
delete_messages(
    key: , status: Optional[MessageStatus] = None
) -> None

```

Delete all messages for a key with the specified status (async).
Source code in `llama-index-core/llama_index/core/storage/chat_store/sql.py`  
| 
```
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
```
 | 
```
async defdelete_messages(
    self, key: str, status: Optional[MessageStatus] = None
) -> None:
"""Delete all messages for a key with the specified status (async)."""
    session_factory, table = await self._initialize()

    query = delete(table).where(table.c.key == key)

    if status is not None:
        query = query.where(table.c.status == status.value)

    async with session_factory() as session:
        await session.execute(query)
        await session.commit()

```
 |  
| --- | --- |  
###  delete_oldest_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/async_sql/#llama_index.core.storage.chat_store.sql.SQLAlchemyChatStore.delete_oldest_messages "Permanent link")

```
delete_oldest_messages(
    key: , n: 
) -> []

```

Delete the oldest n messages for a key and return them (async).
Source code in `llama-index-core/llama_index/core/storage/chat_store/sql.py`  
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
368
369
370
```
 | 
```
async defdelete_oldest_messages(self, key: str, n: int) -> List[ChatMessage]:
"""Delete the oldest n messages for a key and return them (async)."""
    session_factory, table = await self._initialize()

    oldest_messages = []

    async with session_factory() as session:
        # First get the oldest n messages
        result = await session.execute(
            select(table)
            .where(
                table.c.key == key,
                table.c.status == MessageStatus.ACTIVE.value,
            )
            .order_by(table.c.timestamp, table.c.id)
            .limit(n)
        )
        rows = result.fetchall()

        if not rows:
            return []

        # Store the messages we're about to delete
        oldest_messages = [ChatMessage.model_validate(row.data) for row in rows]

        # Get the IDs to delete
        ids_to_delete = [row.id for row in rows]

        # Delete the messages
        await session.execute(delete(table).where(table.c.id.in_(ids_to_delete)))
        await session.commit()

    return oldest_messages

```
 |  
| --- | --- |  
###  archive_oldest_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/async_sql/#llama_index.core.storage.chat_store.sql.SQLAlchemyChatStore.archive_oldest_messages "Permanent link")

```
archive_oldest_messages(
    key: , n: 
) -> []

```

Archive the oldest n messages for a key and return them (async).
Source code in `llama-index-core/llama_index/core/storage/chat_store/sql.py`  
| 
```
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
```
 | 
```
async defarchive_oldest_messages(self, key: str, n: int) -> List[ChatMessage]:
"""Archive the oldest n messages for a key and return them (async)."""
    session_factory, table = await self._initialize()

    async with session_factory() as session:
        # First get the oldest n messages
        result = await session.execute(
            select(table)
            .where(
                table.c.key == key,
                table.c.status == MessageStatus.ACTIVE.value,
            )
            .order_by(table.c.timestamp, table.c.id)
            .limit(n)
        )
        rows = result.fetchall()

        if not rows:
            return []

        # Store the messages we're about to archive
        archived_messages = [ChatMessage.model_validate(row.data) for row in rows]

        # Get the IDs to archive
        ids_to_archive = [row.id for row in rows]

        # Update message status to archived
        await session.execute(
            update(table)
            .where(table.c.id.in_(ids_to_archive))
            .values(status=MessageStatus.ARCHIVED.value)
        )
        await session.commit()

    return archived_messages

```
 |  
| --- | --- |  
###  get_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/async_sql/#llama_index.core.storage.chat_store.sql.SQLAlchemyChatStore.get_keys "Permanent link")

```
get_keys() -> []

```

Get all unique keys in the store (async).
Source code in `llama-index-core/llama_index/core/storage/chat_store/sql.py`  
| 
```
408
409
410
411
412
413
414
```
 | 
```
async defget_keys(self) -> List[str]:
"""Get all unique keys in the store (async)."""
    session_factory, table = await self._initialize()

    async with session_factory() as session:
        result = await session.execute(select(table.c.key).distinct())
        return [row[0] for row in result.fetchall()]

```
 |  
| --- | --- |  
###  dump_store [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/async_sql/#llama_index.core.storage.chat_store.sql.SQLAlchemyChatStore.dump_store "Permanent link")

```
dump_store() -> 

```

Dump the store's configuration and data (if in-memory).
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `dict`  |  A dictionary containing the store's configuration and potentially its data.  |  
Source code in `llama-index-core/llama_index/core/storage/chat_store/sql.py`  
| 
```
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
```
 | 
```
@model_serializer()
defdump_store(self) -> dict:
"""
    Dump the store's configuration and data (if in-memory).

    Returns:
        A dictionary containing the store's configuration and potentially its data.

    """
    dump_data = {
        "table_name": self.table_name,
        "async_database_uri": self.async_database_uri,
        "db_schema": self.db_schema,
    }

    if self._is_in_memory_uri(self.async_database_uri):
        # switch to sync sqlite
        dump_data["db_data"] = asyncio_run(self._dump_db_data())

    return dump_data

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/async_sql/#llama_index.core.storage.chat_store.sql.SQLAlchemyChatStore.class_name "Permanent link")

```
class_name() -> 

```

Return the class name.
Source code in `llama-index-core/llama_index/core/storage/chat_store/sql.py`  
| 
```
455
456
457
458
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Return the class name."""
    return "SQLAlchemyChatStore"

```
 |  
| --- | --- |  
options: members: - AsyncDBChatStore - SQLAlchemyChatStore
