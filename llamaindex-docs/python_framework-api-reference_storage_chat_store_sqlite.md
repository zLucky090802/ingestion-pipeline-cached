# Sqlite
##  SQLiteChatStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/sqlite/#llama_index.storage.chat_store.sqlite.SQLiteChatStore "Permanent link")
Bases: 
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-sqlite/llama_index/storage/chat_store/sqlite/base.py`  
| 
```
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
```
 | 
```
classSQLiteChatStore(BaseChatStore):
    table_name: Optional[str] = Field(
        default="chatstore", description="SQLite table name."
    )

    _table_class: TableProtocol = PrivateAttr()  # type: ignore
    _session: sessionmaker = PrivateAttr()  # type: ignore
    _async_session: async_sessionmaker = PrivateAttr()  # type: ignore

    def__init__(
        self,
        session: sessionmaker,
        async_session: async_sessionmaker,
        table_name: str,
    ):
        super().__init__(
            table_name=table_name.lower(),
        )

        # sqlalchemy model
        base = declarative_base()
        self._table_class = get_data_model(
            base,
            table_name,
        )
        self._session = session
        self._async_session = async_session
        self._initialize(base)

    @classmethod
    deffrom_params(
        cls,
        database: str,
        table_name: str = "chatstore",
        connection_string: Optional[str] = None,
        async_connection_string: Optional[str] = None,
        debug: bool = False,
    ) -> "SQLiteChatStore":
"""Return connection string from database parameters."""
        conn_str = connection_string or f"sqlite:///{database}"
        async_conn_str = async_connection_string or (f"sqlite+aiosqlite:///{database}")
        session, async_session = cls._connect(conn_str, async_conn_str, debug)
        return cls(
            session=session,
            async_session=async_session,
            table_name=table_name,
        )

    @classmethod
    deffrom_uri(
        cls,
        uri: str,
        table_name: str = "chatstore",
        debug: bool = False,
    ) -> "SQLiteChatStore":
"""Return connection string from database parameters."""
        params = params_from_uri(uri)
        return cls.from_params(
            **params,
            table_name=table_name,
            debug=debug,
        )

    @classmethod
    def_connect(
        cls, connection_string: str, async_connection_string: str, debug: bool
    ) -> tuple[sessionmaker, async_sessionmaker]:
        _engine = create_engine(connection_string, echo=debug)
        session = sessionmaker(_engine)

        _async_engine = create_async_engine(async_connection_string)
        async_session = async_sessionmaker(_async_engine, class_=AsyncSession)
        return session, async_session

    def_create_tables_if_not_exists(self, base) -> None:
        with self._session() as session, session.begin():
            base.metadata.create_all(session.connection())

    def_initialize(self, base) -> None:
        self._create_tables_if_not_exists(base)

    defset_messages(self, key: str, messages: list[ChatMessage]) -> None:
"""Set messages for a key."""
        with self._session() as session:
            session.execute(
                insert(self._table_class),
                [
                    {"key": key, "value": message.model_dump(mode="json")}
                    for message in messages
                ],
            )
            session.commit()

    async defaset_messages(self, key: str, messages: list[ChatMessage]) -> None:
"""Async version of Get messages for a key."""
        async with self._async_session() as session:
            await session.execute(
                insert(self._table_class),
                [
                    {"key": key, "value": message.model_dump(mode="json")}
                    for message in messages
                ],
            )
            await session.commit()

    defget_messages(self, key: str) -> list[ChatMessage]:
"""Get messages for a key."""
        with self._session() as session:
            result = session.execute(
                select(self._table_class)
                .where(self._table_class.key == key)
                .order_by(self._table_class.id)
            )
            result = result.scalars().all()
            if result:
                return [ChatMessage.model_validate(row.value) for row in result]
            return []

    async defaget_messages(self, key: str) -> list[ChatMessage]:
"""Async version of Get messages for a key."""
        async with self._async_session() as session:
            result = await session.execute(
                select(self._table_class)
                .where(self._table_class.key == key)
                .order_by(self._table_class.id)
            )
            result = result.scalars().all()
            if result:
                return [ChatMessage.model_validate(row.value) for row in result]
            return []

    defadd_message(self, key: str, message: ChatMessage) -> None:
"""Add a message for a key."""
        with self._session() as session:
            session.execute(
                insert(self._table_class),
                [{"key": key, "value": message.model_dump(mode="json")}],
            )
            session.commit()

    async defasync_add_message(self, key: str, message: ChatMessage) -> None:
"""Async version of Add a message for a key."""
        async with self._async_session() as session:
            await session.execute(
                insert(self._table_class),
                [{"key": key, "value": message.model_dump(mode="json")}],
            )
            await session.commit()

    defdelete_messages(self, key: str) -> Optional[list[ChatMessage]]:
"""Delete messages for a key."""
        with self._session() as session:
            session.execute(
                delete(self._table_class).where(self._table_class.key == key)
            )
            session.commit()
        return None

    async defadelete_messages(self, key: str) -> Optional[list[ChatMessage]]:
"""Async version of Delete messages for a key."""
        async with self._async_session() as session:
            await session.execute(
                delete(self._table_class).where(self._table_class.key == key)
            )
            await session.commit()
        return None

    defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
        with self._session() as session:
            # First, retrieve message
            result = session.execute(
                select(self._table_class.value).where(
                    self._table_class.key == key, self._table_class.id == idx
                )
            ).scalar_one_or_none()

            if result is None:
                return None

            session.execute(
                delete(self._table_class).where(
                    self._table_class.key == key, self._table_class.id == idx
                )
            )
            session.commit()

            return ChatMessage.model_validate(result)

    async defadelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Async version of Delete specific message for a key."""
        async with self._async_session() as session:
            # First, retrieve message
            result = (
                await session.execute(
                    select(self._table_class.value).where(
                        self._table_class.key == key, self._table_class.id == idx
                    )
                )
            ).scalar_one_or_none()

            if result is None:
                return None

            await session.execute(
                delete(self._table_class).where(
                    self._table_class.key == key, self._table_class.id == idx
                )
            )
            await session.commit()

            return ChatMessage.model_validate(result)

    defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete last message for a key."""
        with self._session() as session:
            # First, retrieve the current list of messages
            stmt = (
                select(self._table_class.id, self._table_class.value)
                .where(self._table_class.key == key)
                .order_by(self._table_class.id.desc())
                .limit(1)
            )
            result = session.execute(stmt).all()

            if not result:
                # If the key doesn't exist or the array is empty
                return None

            session.execute(
                delete(self._table_class).where(self._table_class.id == result[0][0])
            )
            session.commit()

            return ChatMessage.model_validate(result[0][1])

    async defadelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Async version of Delete last message for a key."""
        async with self._async_session() as session:
            # First, retrieve the current list of messages
            stmt = (
                select(self._table_class.id, self._table_class.value)
                .where(self._table_class.key == key)
                .order_by(self._table_class.id.desc())
                .limit(1)
            )
            result = (await session.execute(stmt)).all()

            if not result:
                # If the key doesn't exist or the array is empty
                return None

            await session.execute(
                delete(self._table_class).where(self._table_class.id == result[0][0])
            )
            await session.commit()

            return ChatMessage.model_validate(result[0][1])

    defget_keys(self) -> list[str]:
"""Get all keys."""
        with self._session() as session:
            stmt = select(self._table_class.key.distinct())

            return session.execute(stmt).scalars().all()

    async defaget_keys(self) -> list[str]:
"""Async version of Get all keys."""
        async with self._async_session() as session:
            stmt = select(self._table_class.key.distinct())

            return (await session.execute(stmt)).scalars().all()

```
 |  
| --- | --- |  
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/sqlite/#llama_index.storage.chat_store.sqlite.SQLiteChatStore.from_params "Permanent link")

```
from_params(
    database: ,
    table_name:  = "chatstore",
    connection_string: Optional[] = None,
    async_connection_string: Optional[] = None,
    debug:  = False,
) -> 

```

Return connection string from database parameters.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-sqlite/llama_index/storage/chat_store/sqlite/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_params(
    cls,
    database: str,
    table_name: str = "chatstore",
    connection_string: Optional[str] = None,
    async_connection_string: Optional[str] = None,
    debug: bool = False,
) -> "SQLiteChatStore":
"""Return connection string from database parameters."""
    conn_str = connection_string or f"sqlite:///{database}"
    async_conn_str = async_connection_string or (f"sqlite+aiosqlite:///{database}")
    session, async_session = cls._connect(conn_str, async_conn_str, debug)
    return cls(
        session=session,
        async_session=async_session,
        table_name=table_name,
    )

```
 |  
| --- | --- |  
###  from_uri `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/sqlite/#llama_index.storage.chat_store.sqlite.SQLiteChatStore.from_uri "Permanent link")

```
from_uri(
    uri: ,
    table_name:  = "chatstore",
    debug:  = False,
) -> 

```

Return connection string from database parameters.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-sqlite/llama_index/storage/chat_store/sqlite/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_uri(
    cls,
    uri: str,
    table_name: str = "chatstore",
    debug: bool = False,
) -> "SQLiteChatStore":
"""Return connection string from database parameters."""
    params = params_from_uri(uri)
    return cls.from_params(
        **params,
        table_name=table_name,
        debug=debug,
    )

```
 |  
| --- | --- |  
###  set_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/sqlite/#llama_index.storage.chat_store.sqlite.SQLiteChatStore.set_messages "Permanent link")

```
set_messages(key: , messages: []) -> None

```

Set messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-sqlite/llama_index/storage/chat_store/sqlite/base.py`  
| 
```
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
```
 | 
```
defset_messages(self, key: str, messages: list[ChatMessage]) -> None:
"""Set messages for a key."""
    with self._session() as session:
        session.execute(
            insert(self._table_class),
            [
                {"key": key, "value": message.model_dump(mode="json")}
                for message in messages
            ],
        )
        session.commit()

```
 |  
| --- | --- |  
###  aset_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/sqlite/#llama_index.storage.chat_store.sqlite.SQLiteChatStore.aset_messages "Permanent link")

```
aset_messages(
    key: , messages: []
) -> None

```

Async version of Get messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-sqlite/llama_index/storage/chat_store/sqlite/base.py`  
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
```
 | 
```
async defaset_messages(self, key: str, messages: list[ChatMessage]) -> None:
"""Async version of Get messages for a key."""
    async with self._async_session() as session:
        await session.execute(
            insert(self._table_class),
            [
                {"key": key, "value": message.model_dump(mode="json")}
                for message in messages
            ],
        )
        await session.commit()

```
 |  
| --- | --- |  
###  get_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/sqlite/#llama_index.storage.chat_store.sqlite.SQLiteChatStore.get_messages "Permanent link")

```
get_messages(key: ) -> []

```

Get messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-sqlite/llama_index/storage/chat_store/sqlite/base.py`  
| 
```
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
defget_messages(self, key: str) -> list[ChatMessage]:
"""Get messages for a key."""
    with self._session() as session:
        result = session.execute(
            select(self._table_class)
            .where(self._table_class.key == key)
            .order_by(self._table_class.id)
        )
        result = result.scalars().all()
        if result:
            return [ChatMessage.model_validate(row.value) for row in result]
        return []

```
 |  
| --- | --- |  
###  aget_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/sqlite/#llama_index.storage.chat_store.sqlite.SQLiteChatStore.aget_messages "Permanent link")

```
aget_messages(key: ) -> []

```

Async version of Get messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-sqlite/llama_index/storage/chat_store/sqlite/base.py`  
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
```
 | 
```
async defaget_messages(self, key: str) -> list[ChatMessage]:
"""Async version of Get messages for a key."""
    async with self._async_session() as session:
        result = await session.execute(
            select(self._table_class)
            .where(self._table_class.key == key)
            .order_by(self._table_class.id)
        )
        result = result.scalars().all()
        if result:
            return [ChatMessage.model_validate(row.value) for row in result]
        return []

```
 |  
| --- | --- |  
###  add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/sqlite/#llama_index.storage.chat_store.sqlite.SQLiteChatStore.add_message "Permanent link")

```
add_message(key: , message: ) -> None

```

Add a message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-sqlite/llama_index/storage/chat_store/sqlite/base.py`  
| 
```
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
defadd_message(self, key: str, message: ChatMessage) -> None:
"""Add a message for a key."""
    with self._session() as session:
        session.execute(
            insert(self._table_class),
            [{"key": key, "value": message.model_dump(mode="json")}],
        )
        session.commit()

```
 |  
| --- | --- |  
###  async_add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/sqlite/#llama_index.storage.chat_store.sqlite.SQLiteChatStore.async_add_message "Permanent link")

```
async_add_message(key: , message: ) -> None

```

Async version of Add a message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-sqlite/llama_index/storage/chat_store/sqlite/base.py`  
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
```
 | 
```
async defasync_add_message(self, key: str, message: ChatMessage) -> None:
"""Async version of Add a message for a key."""
    async with self._async_session() as session:
        await session.execute(
            insert(self._table_class),
            [{"key": key, "value": message.model_dump(mode="json")}],
        )
        await session.commit()

```
 |  
| --- | --- |  
###  delete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/sqlite/#llama_index.storage.chat_store.sqlite.SQLiteChatStore.delete_messages "Permanent link")

```
delete_messages(key: ) -> Optional[[]]

```

Delete messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-sqlite/llama_index/storage/chat_store/sqlite/base.py`  
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
```
 | 
```
defdelete_messages(self, key: str) -> Optional[list[ChatMessage]]:
"""Delete messages for a key."""
    with self._session() as session:
        session.execute(
            delete(self._table_class).where(self._table_class.key == key)
        )
        session.commit()
    return None

```
 |  
| --- | --- |  
###  adelete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/sqlite/#llama_index.storage.chat_store.sqlite.SQLiteChatStore.adelete_messages "Permanent link")

```
adelete_messages(key: ) -> Optional[[]]

```

Async version of Delete messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-sqlite/llama_index/storage/chat_store/sqlite/base.py`  
| 
```
286
287
288
289
290
291
292
293
```
 | 
```
async defadelete_messages(self, key: str) -> Optional[list[ChatMessage]]:
"""Async version of Delete messages for a key."""
    async with self._async_session() as session:
        await session.execute(
            delete(self._table_class).where(self._table_class.key == key)
        )
        await session.commit()
    return None

```
 |  
| --- | --- |  
###  delete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/sqlite/#llama_index.storage.chat_store.sqlite.SQLiteChatStore.delete_message "Permanent link")

```
delete_message(key: , idx: ) -> Optional[]

```

Delete specific message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-sqlite/llama_index/storage/chat_store/sqlite/base.py`  
| 
```
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
```
 | 
```
defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
    with self._session() as session:
        # First, retrieve message
        result = session.execute(
            select(self._table_class.value).where(
                self._table_class.key == key, self._table_class.id == idx
            )
        ).scalar_one_or_none()

        if result is None:
            return None

        session.execute(
            delete(self._table_class).where(
                self._table_class.key == key, self._table_class.id == idx
            )
        )
        session.commit()

        return ChatMessage.model_validate(result)

```
 |  
| --- | --- |  
###  adelete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/sqlite/#llama_index.storage.chat_store.sqlite.SQLiteChatStore.adelete_message "Permanent link")

```
adelete_message(
    key: , idx: 
) -> Optional[]

```

Async version of Delete specific message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-sqlite/llama_index/storage/chat_store/sqlite/base.py`  
| 
```
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
```
 | 
```
async defadelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Async version of Delete specific message for a key."""
    async with self._async_session() as session:
        # First, retrieve message
        result = (
            await session.execute(
                select(self._table_class.value).where(
                    self._table_class.key == key, self._table_class.id == idx
                )
            )
        ).scalar_one_or_none()

        if result is None:
            return None

        await session.execute(
            delete(self._table_class).where(
                self._table_class.key == key, self._table_class.id == idx
            )
        )
        await session.commit()

        return ChatMessage.model_validate(result)

```
 |  
| --- | --- |  
###  delete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/sqlite/#llama_index.storage.chat_store.sqlite.SQLiteChatStore.delete_last_message "Permanent link")

```
delete_last_message(key: ) -> Optional[]

```

Delete last message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-sqlite/llama_index/storage/chat_store/sqlite/base.py`  
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
357
358
359
360
361
362
```
 | 
```
defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete last message for a key."""
    with self._session() as session:
        # First, retrieve the current list of messages
        stmt = (
            select(self._table_class.id, self._table_class.value)
            .where(self._table_class.key == key)
            .order_by(self._table_class.id.desc())
            .limit(1)
        )
        result = session.execute(stmt).all()

        if not result:
            # If the key doesn't exist or the array is empty
            return None

        session.execute(
            delete(self._table_class).where(self._table_class.id == result[0][0])
        )
        session.commit()

        return ChatMessage.model_validate(result[0][1])

```
 |  
| --- | --- |  
###  adelete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/sqlite/#llama_index.storage.chat_store.sqlite.SQLiteChatStore.adelete_last_message "Permanent link")

```
adelete_last_message(key: ) -> Optional[]

```

Async version of Delete last message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-sqlite/llama_index/storage/chat_store/sqlite/base.py`  
| 
```
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
```
 | 
```
async defadelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Async version of Delete last message for a key."""
    async with self._async_session() as session:
        # First, retrieve the current list of messages
        stmt = (
            select(self._table_class.id, self._table_class.value)
            .where(self._table_class.key == key)
            .order_by(self._table_class.id.desc())
            .limit(1)
        )
        result = (await session.execute(stmt)).all()

        if not result:
            # If the key doesn't exist or the array is empty
            return None

        await session.execute(
            delete(self._table_class).where(self._table_class.id == result[0][0])
        )
        await session.commit()

        return ChatMessage.model_validate(result[0][1])

```
 |  
| --- | --- |  
###  get_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/sqlite/#llama_index.storage.chat_store.sqlite.SQLiteChatStore.get_keys "Permanent link")

```
get_keys() -> []

```

Get all keys.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-sqlite/llama_index/storage/chat_store/sqlite/base.py`  
| 
```
387
388
389
390
391
392
```
 | 
```
defget_keys(self) -> list[str]:
"""Get all keys."""
    with self._session() as session:
        stmt = select(self._table_class.key.distinct())

        return session.execute(stmt).scalars().all()

```
 |  
| --- | --- |  
###  aget_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/sqlite/#llama_index.storage.chat_store.sqlite.SQLiteChatStore.aget_keys "Permanent link")

```
aget_keys() -> []

```

Async version of Get all keys.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-sqlite/llama_index/storage/chat_store/sqlite/base.py`  
| 
```
394
395
396
397
398
399
```
 | 
```
async defaget_keys(self) -> list[str]:
"""Async version of Get all keys."""
    async with self._async_session() as session:
        stmt = select(self._table_class.key.distinct())

        return (await session.execute(stmt)).scalars().all()

```
 |  
| --- | --- |  
options: members: - SQLiteChatStore
