# Yugabytedb
##  YugabyteDBChatStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/yugabytedb/#llama_index.storage.chat_store.yugabytedb.YugabyteDBChatStore "Permanent link")
Bases: 
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-yugabytedb/llama_index/storage/chat_store/yugabytedb/base.py`  
| 
```
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
```
 | 
```
classYugabyteDBChatStore(BaseChatStore):
    table_name: Optional[str] = Field(
        default="chatstore", description="YugabyteDB table name."
    )
    schema_name: Optional[str] = Field(
        default="public", description="YugabyteDB schema name."
    )

    _table_class: Optional[Any] = PrivateAttr()
    _session: Optional[sessionmaker] = PrivateAttr()

    def__init__(
        self,
        session: sessionmaker,
        table_name: str,
        schema_name: str = "public",
        use_jsonb: bool = False,
    ):
        super().__init__(
            table_name=table_name.lower(),
            schema_name=schema_name.lower(),
        )

        # sqlalchemy model
        base = declarative_base()
        self._table_class = get_data_model(
            base,
            table_name,
            schema_name,
            use_jsonb=use_jsonb,
        )
        self._session = session
        self._initialize(base)

    @classmethod
    deffrom_params(
        cls,
        host: Optional[str] = None,
        port: Optional[str] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        load_balance: Optional[bool] = False,
        topology_keys: Optional[str] = None,
        yb_servers_refresh_interval: Optional[int] = 300,
        fallback_to_topology_keys_only: Optional[bool] = False,
        failed_host_ttl_seconds: Optional[int] = 5,
        table_name: str = "chatstore",
        schema_name: str = "public",
        connection_string: Optional[str] = None,
        debug: bool = False,
        use_jsonb: bool = False,
    ) -> "YugabyteDBChatStore":
"""
        Return connection string from database parameters.

        Args:
            host (str): YugabyteDB host.
            port (str): YugabyteDB port.
            database (str): YugabyteDB database name.
            user (str): YugabyteDB user.
            password (str): YugabyteDB password.
            load_balance (bool, optional): Enables uniform load balancing. Defaults to False.
            topology_keys (str, optional): Enables topology-aware load balancing.
                Specify comma-separated geo-locations in the form of cloud.region.zone:priority.
                Ignored if load_balance is false. Defaults to None.
            yb_servers_refresh_interval (int, optional): The interval in seconds to refresh the servers list;
                ignored if load_balance is false. Defaults to 300.
            fallback_to_topology_keys_only (bool, optional): If set to true and topology_keys are specified,
                the driver only tries to connect to nodes specified in topology_keys
                Defaults to False.
            failed_host_ttl_seconds (int, optional): Time, in seconds, to wait before trying to connect to failed nodes.
                Defaults to 5.
            connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to yugabytedb db.
            table_name (str): Table name.
            schema_name (str): Schema name.
            debug (bool, optional): Debug mode. Defaults to False.
            use_jsonb (bool, optional): Use JSONB instead of JSON. Defaults to False.

        """
        fromurllib.parseimport urlencode

        query_params = {"load_balance": str(load_balance)}

        if topology_keys is not None:
            query_params["topology_keys"] = topology_keys
        if yb_servers_refresh_interval is not None:
            query_params["yb_servers_refresh_interval"] = yb_servers_refresh_interval
        if fallback_to_topology_keys_only:
            query_params["fallback_to_topology_keys_only"] = (
                fallback_to_topology_keys_only
            )
        if failed_host_ttl_seconds is not None:
            query_params["failed_host_ttl_seconds"] = failed_host_ttl_seconds

        query_str = urlencode(query_params)

        conn_str = (
            connection_string
            or f"yugabytedb+psycopg2://{user}:{password}@{host}:{port}/{database}?{query_str}"
        )

        session = cls._connect(conn_str, debug)
        return cls(
            session=session,
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
    ) -> "YugabyteDBChatStore":
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
        cls, connection_string: str, debug: bool
    ) -> tuple[sessionmaker, sessionmaker]:
        _engine = create_engine(connection_string, echo=debug)

        return sessionmaker(_engine)

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
            stmt = (
                insert(self._table_class)
                .values(
                    key=bindparam("key"), value=cast(bindparam("value"), ARRAY(JSONB))
                )
                .on_conflict_do_update(
                    index_elements=["key"],
                    set_={"value": cast(bindparam("value"), ARRAY(JSONB))},
                )
            )

            params = {
                "key": key,
                "value": [message.model_dump_json() for message in messages],
            }

            # Execute the bulk upsert
            session.execute(stmt, params)
            session.commit()

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

    defadd_message(self, key: str, message: ChatMessage) -> None:
"""Add a message for a key."""
        with self._session() as session:
            stmt = (
                insert(self._table_class)
                .values(
                    key=bindparam("key"), value=cast(bindparam("value"), ARRAY(JSONB))
                )
                .on_conflict_do_update(
                    index_elements=["key"],
                    set_={"value": cast(bindparam("value"), ARRAY(JSONB))},
                )
            )
            params = {"key": key, "value": [message.model_dump_json()]}
            session.execute(stmt, params)
            session.commit()

    defdelete_messages(self, key: str) -> Optional[list[ChatMessage]]:
"""Delete messages for a key."""
        with self._session() as session:
            session.execute(delete(self._table_class).filter_by(key=key))
            session.commit()
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

    defget_keys(self) -> list[str]:
"""Get all keys."""
        with self._session() as session:
            stmt = select(self._table_class.key)

            return session.execute(stmt).scalars().all()

```
 |  
| --- | --- |  
###  from_params `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/yugabytedb/#llama_index.storage.chat_store.yugabytedb.YugabyteDBChatStore.from_params "Permanent link")

```
from_params(
    host: Optional[] = None,
    port: Optional[] = None,
    database: Optional[] = None,
    user: Optional[] = None,
    password: Optional[] = None,
    load_balance: Optional[] = False,
    topology_keys: Optional[] = None,
    yb_servers_refresh_interval: Optional[] = 300,
    fallback_to_topology_keys_only: Optional[] = False,
    failed_host_ttl_seconds: Optional[] = 5,
    table_name:  = "chatstore",
    schema_name:  = "public",
    connection_string: Optional[] = None,
    debug:  = False,
    use_jsonb:  = False,
) -> 

```

Return connection string from database parameters.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `host`  |  YugabyteDB host.  |  `None`  |  
|  `port`  |  YugabyteDB port.  |  `None`  |  
|  `database`  |  YugabyteDB database name.  |  `None`  |  
|  `user`  |  YugabyteDB user.  |  `None`  |  
|  `password`  |  YugabyteDB password.  |  `None`  |  
|  `load_balance`  |  `bool`  |  Enables uniform load balancing. Defaults to False.  |  `False`  |  
|  `topology_keys`  |  Enables topology-aware load balancing. Specify comma-separated geo-locations in the form of cloud.region.zone:priority. Ignored if load_balance is false. Defaults to None.  |  `None`  |  
|  `yb_servers_refresh_interval`  |  The interval in seconds to refresh the servers list; ignored if load_balance is false. Defaults to 300.  |  `300`  |  
|  `fallback_to_topology_keys_only`  |  `bool`  |  If set to true and topology_keys are specified, the driver only tries to connect to nodes specified in topology_keys Defaults to False.  |  `False`  |  
|  `failed_host_ttl_seconds`  |  Time, in seconds, to wait before trying to connect to failed nodes. Defaults to 5.  |  
|  `connection_string`  |  `Union[str, URL]`  |  Connection string to yugabytedb db.  |  `None`  |  
|  `table_name`  |  Table name.  |  `'chatstore'`  |  
|  `schema_name`  |  Schema name.  |  `'public'`  |  
|  `debug`  |  `bool`  |  Debug mode. Defaults to False.  |  `False`  |  
|  `use_jsonb`  |  `bool`  |  Use JSONB instead of JSON. Defaults to False.  |  `False`  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-yugabytedb/llama_index/storage/chat_store/yugabytedb/base.py`  
| 
```
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
    load_balance: Optional[bool] = False,
    topology_keys: Optional[str] = None,
    yb_servers_refresh_interval: Optional[int] = 300,
    fallback_to_topology_keys_only: Optional[bool] = False,
    failed_host_ttl_seconds: Optional[int] = 5,
    table_name: str = "chatstore",
    schema_name: str = "public",
    connection_string: Optional[str] = None,
    debug: bool = False,
    use_jsonb: bool = False,
) -> "YugabyteDBChatStore":
"""
    Return connection string from database parameters.

    Args:
        host (str): YugabyteDB host.
        port (str): YugabyteDB port.
        database (str): YugabyteDB database name.
        user (str): YugabyteDB user.
        password (str): YugabyteDB password.
        load_balance (bool, optional): Enables uniform load balancing. Defaults to False.
        topology_keys (str, optional): Enables topology-aware load balancing.
            Specify comma-separated geo-locations in the form of cloud.region.zone:priority.
            Ignored if load_balance is false. Defaults to None.
        yb_servers_refresh_interval (int, optional): The interval in seconds to refresh the servers list;
            ignored if load_balance is false. Defaults to 300.
        fallback_to_topology_keys_only (bool, optional): If set to true and topology_keys are specified,
            the driver only tries to connect to nodes specified in topology_keys
            Defaults to False.
        failed_host_ttl_seconds (int, optional): Time, in seconds, to wait before trying to connect to failed nodes.
            Defaults to 5.
        connection_string (Union[str, sqlalchemy.engine.URL]): Connection string to yugabytedb db.
        table_name (str): Table name.
        schema_name (str): Schema name.
        debug (bool, optional): Debug mode. Defaults to False.
        use_jsonb (bool, optional): Use JSONB instead of JSON. Defaults to False.

    """
    fromurllib.parseimport urlencode

    query_params = {"load_balance": str(load_balance)}

    if topology_keys is not None:
        query_params["topology_keys"] = topology_keys
    if yb_servers_refresh_interval is not None:
        query_params["yb_servers_refresh_interval"] = yb_servers_refresh_interval
    if fallback_to_topology_keys_only:
        query_params["fallback_to_topology_keys_only"] = (
            fallback_to_topology_keys_only
        )
    if failed_host_ttl_seconds is not None:
        query_params["failed_host_ttl_seconds"] = failed_host_ttl_seconds

    query_str = urlencode(query_params)

    conn_str = (
        connection_string
        or f"yugabytedb+psycopg2://{user}:{password}@{host}:{port}/{database}?{query_str}"
    )

    session = cls._connect(conn_str, debug)
    return cls(
        session=session,
        table_name=table_name,
        schema_name=schema_name,
        use_jsonb=use_jsonb,
    )

```
 |  
| --- | --- |  
###  from_uri `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/yugabytedb/#llama_index.storage.chat_store.yugabytedb.YugabyteDBChatStore.from_uri "Permanent link")

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
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-yugabytedb/llama_index/storage/chat_store/yugabytedb/base.py`  
| 
```
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
) -> "YugabyteDBChatStore":
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
###  set_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/yugabytedb/#llama_index.storage.chat_store.yugabytedb.YugabyteDBChatStore.set_messages "Permanent link")

```
set_messages(key: , messages: []) -> None

```

Set messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-yugabytedb/llama_index/storage/chat_store/yugabytedb/base.py`  
| 
```
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
```
 | 
```
defset_messages(self, key: str, messages: list[ChatMessage]) -> None:
"""Set messages for a key."""
    with self._session() as session:
        stmt = (
            insert(self._table_class)
            .values(
                key=bindparam("key"), value=cast(bindparam("value"), ARRAY(JSONB))
            )
            .on_conflict_do_update(
                index_elements=["key"],
                set_={"value": cast(bindparam("value"), ARRAY(JSONB))},
            )
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
###  get_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/yugabytedb/#llama_index.storage.chat_store.yugabytedb.YugabyteDBChatStore.get_messages "Permanent link")

```
get_messages(key: ) -> []

```

Get messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-yugabytedb/llama_index/storage/chat_store/yugabytedb/base.py`  
| 
```
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
###  add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/yugabytedb/#llama_index.storage.chat_store.yugabytedb.YugabyteDBChatStore.add_message "Permanent link")

```
add_message(key: , message: ) -> None

```

Add a message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-yugabytedb/llama_index/storage/chat_store/yugabytedb/base.py`  
| 
```
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
```
 | 
```
defadd_message(self, key: str, message: ChatMessage) -> None:
"""Add a message for a key."""
    with self._session() as session:
        stmt = (
            insert(self._table_class)
            .values(
                key=bindparam("key"), value=cast(bindparam("value"), ARRAY(JSONB))
            )
            .on_conflict_do_update(
                index_elements=["key"],
                set_={"value": cast(bindparam("value"), ARRAY(JSONB))},
            )
        )
        params = {"key": key, "value": [message.model_dump_json()]}
        session.execute(stmt, params)
        session.commit()

```
 |  
| --- | --- |  
###  delete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/yugabytedb/#llama_index.storage.chat_store.yugabytedb.YugabyteDBChatStore.delete_messages "Permanent link")

```
delete_messages(key: ) -> Optional[[]]

```

Delete messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-yugabytedb/llama_index/storage/chat_store/yugabytedb/base.py`  
| 
```
284
285
286
287
288
289
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
###  delete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/yugabytedb/#llama_index.storage.chat_store.yugabytedb.YugabyteDBChatStore.delete_message "Permanent link")

```
delete_message(key: , idx: ) -> Optional[]

```

Delete specific message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-yugabytedb/llama_index/storage/chat_store/yugabytedb/base.py`  
| 
```
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
###  delete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/yugabytedb/#llama_index.storage.chat_store.yugabytedb.YugabyteDBChatStore.delete_last_message "Permanent link")

```
delete_last_message(key: ) -> Optional[]

```

Delete last message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-yugabytedb/llama_index/storage/chat_store/yugabytedb/base.py`  
| 
```
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
###  get_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/yugabytedb/#llama_index.storage.chat_store.yugabytedb.YugabyteDBChatStore.get_keys "Permanent link")

```
get_keys() -> []

```

Get all keys.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-yugabytedb/llama_index/storage/chat_store/yugabytedb/base.py`  
| 
```
349
350
351
352
353
354
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
options: members: - YugabyteDBChatStore
