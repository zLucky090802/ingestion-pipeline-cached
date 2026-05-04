# Duckdb
##  DuckDBKVStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/duckdb/#llama_index.storage.kvstore.duckdb.DuckDBKVStore "Permanent link")
Bases: 
DuckDB KV Store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `duckdb_uri`  |  DuckDB URI  |  _required_  |  
|  `duckdb_client`  |  DuckDB client  |  _required_  |  
|  `async_duckdb_client`  |  Async DuckDB client  |  _required_  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If duckdb-py is not installed  |  
Examples:

```
>>> fromllama_index.storage.kvstore.duckdbimport DuckDBKVStore
>>> # Create a DuckDBKVStore
>>> duckdb_kv_store = DuckDBKVStore(
>>>     duckdb_url="duckdb://127.0.0.1:6379")

```

Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-duckdb/llama_index/storage/kvstore/duckdb/base.py`  
| 
```
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
```
 | 
```
classDuckDBKVStore(BaseKVStore):
"""
    DuckDB KV Store.

    Args:
        duckdb_uri (str): DuckDB URI
        duckdb_client (Any): DuckDB client
        async_duckdb_client (Any): Async DuckDB client

    Raises:
            ValueError: If duckdb-py is not installed

    Examples:
        >>> from llama_index.storage.kvstore.duckdb import DuckDBKVStore
        >>> # Create a DuckDBKVStore
        >>> duckdb_kv_store = DuckDBKVStore(
        >>>     duckdb_url="duckdb://127.0.0.1:6379")

    """

    database_name: str
    table_name: str
    persist_dir: str

    _shared_conn: Optional[duckdb.DuckDBPyConnection] = None

    _is_initialized: bool = False

    def__init__(
        self,
        database_name: str = ":memory:",
        table_name: str = "keyvalue",
        # https://duckdb.org/docs/extensions/full_text_search
        persist_dir: str = "./storage",
        client: Optional[duckdb.DuckDBPyConnection] = None,
        **kwargs: Any,  # noqa: ARG002
    ) -> None:
"""Init params."""
        if client is not None:
            self._shared_conn = client.cursor()

        self.database_name = database_name
        self.table_name = table_name
        self.persist_dir = persist_dir

        self._thread_local = threading.local()

        _ = self._initialize_table(self.client, self.table_name)

    @classmethod
    deffrom_vector_store(
        cls, duckdb_vector_store, table_name: str = "keyvalue"
    ) -> "DuckDBKVStore":
"""
        Load a DuckDBKVStore from a DuckDB Client.

        Args:
            client (DuckDB): DuckDB client

        """
        fromllama_index.vector_stores.duckdb.baseimport DuckDBVectorStore

        assert isinstance(duckdb_vector_store, DuckDBVectorStore)

        return cls(
            database_name=duckdb_vector_store.database_name,
            table_name=table_name,
            persist_dir=duckdb_vector_store.persist_dir,
            client=duckdb_vector_store.client,
        )

    @property
    defclient(self) -> duckdb.DuckDBPyConnection:
"""Return client."""
        if self._shared_conn is None:
            self._shared_conn = self._connect(self.database_name, self.persist_dir)

        if not hasattr(self._thread_local, "conn") or self._thread_local.conn is None:
            self._thread_local.conn = self._shared_conn.cursor()

        return self._thread_local.conn

    @classmethod
    def_connect(
        cls, database_name: str, persist_dir: str
    ) -> duckdb.DuckDBPyConnection:
"""Connect to the DuckDB database -- create the data persistence directory if it doesn't exist."""
        database_connection = database_name

        if database_name != ":memory:":
            persist_path = Path(persist_dir)

            if not persist_path.exists():
                persist_path.mkdir(parents=True, exist_ok=True)

            database_connection = str(persist_path / database_name)

        return duckdb.connect(database_connection)

    @property
    deftable(self) -> duckdb.DuckDBPyRelation:
"""Return the table for the connection to the DuckDB database."""
        return self.client.table(self.table_name)

    @classmethod
    def_initialize_table(
        cls, conn: duckdb.DuckDBPyConnection, table_name: str
    ) -> duckdb.DuckDBPyRelation:
"""Initialize the DuckDB Database, extensions, and documents table."""
        home_dir = Path.home()
        conn.execute(f"SET home_directory='{home_dir}';")
        conn.install_extension("json")
        conn.load_extension("json")

        _ = (
            conn.begin()
            .execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name}
                key VARCHAR,
                collection VARCHAR,
                value JSON,
                PRIMARY KEY (key, collection)


            CREATE INDEX IF NOT EXISTS collection_idx ON {table_name} (collection);
        """)
            .commit()
        )

        table = conn.table(table_name)

        required_columns = ["key", "value"]
        table_columns = table.describe().columns

        for column in required_columns:
            if column not in table_columns:
                raise DuckDBTableIncorrectColumnsError(
                    table_name, required_columns, table_columns
                )

        return table

    @override
    defput(self, key: str, val: dict, collection: str = DEFAULT_COLLECTION) -> None:
"""
        Put a key-value pair into the store.

        Args:
            key (str): key
            val (dict): value
            collection (str): collection name

        """
        self.put_all([(key, val)], collection)

    @override
    async defaput(
        self, key: str, val: dict, collection: str = DEFAULT_COLLECTION
    ) -> None:
"""
        Put a key-value pair into the store.

        Args:
            key (str): key
            val (dict): value
            collection (str): collection name

        """
        await asyncio.to_thread(self.put, key, val, collection)

    @override
    defput_all(
        self,
        kv_pairs: list[tuple[str, dict]],
        collection: str = DEFAULT_COLLECTION,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
"""
        Put a dictionary of key-value pairs into the store.

        Args:
            kv_pairs (List[Tuple[str, dict]]): key-value pairs
            collection (str): collection name

        """
        if len(kv_pairs) == 0:
            return

        rows = [
            {"key": key, "collection": collection, "value": json.dumps(value)}
            for key, value in kv_pairs
        ]
        arrow_table = pyarrow.Table.from_pylist(rows)

        _ = self.client.sql(
            query=f"""
            INSERT OR REPLACE INTO {self.table.alias}
            SELECT * from arrow_table;
,
        )

    @override
    async defaput_all(
        self,
        kv_pairs: list[tuple[str, dict]],
        collection: str = DEFAULT_COLLECTION,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
"""
        Put a dictionary of key-value pairs into the store.

        Args:
            kv_pairs (List[Tuple[str, dict]]): key-value pairs
            collection (str): collection name

        """
        await asyncio.to_thread(self.put_all, kv_pairs, collection, batch_size)

    @override
    defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> Optional[dict]:
"""
        Get a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        expression: Expression = (
            ColumnExpression("collection")
            .__eq__(ConstantExpression(collection))
            .__and__(ColumnExpression("key").__eq__(ConstantExpression(key)))
        )
        row_result = self.table.filter(filter_expr=expression).fetchone()

        if row_result is None:
            return None

        return json.loads(row_result[2])

    @override
    async defaget(
        self, key: str, collection: str = DEFAULT_COLLECTION
    ) -> Optional[dict]:
"""
        Get a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        return await asyncio.to_thread(self.get, key, collection)

    @override
    defget_all(self, collection: str = DEFAULT_COLLECTION) -> dict[str, dict]:
"""Get all values from the store."""
        filter_expr: Expression = ColumnExpression("collection").__eq__(
            ConstantExpression(collection)
        )

        table: pyarrow.Table = self.table.filter(
            filter_expr=filter_expr
        ).fetch_arrow_table()

        as_list = table.to_pylist()

        return {row["key"]: json.loads(row["value"]) for row in as_list}

    @override
    async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> dict[str, dict]:
"""Get all values from the store."""
        return self.get_all(collection)

    @override
    defdelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
        Delete a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        filter_expression = (
            ColumnExpression("collection")
            .__eq__(ConstantExpression(collection))
            .__and__(ColumnExpression("key").__eq__(ConstantExpression(key)))
        )

        command = f"DELETE FROM {self.table.alias} WHERE {filter_expression}"
        _ = self.client.execute(command)
        return True

    @override
    async defadelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
        Delete a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        return self.delete(key, collection)

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/duckdb/#llama_index.storage.kvstore.duckdb.DuckDBKVStore.client "Permanent link")

```
client: DuckDBPyConnection

```

Return client.
###  table `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/duckdb/#llama_index.storage.kvstore.duckdb.DuckDBKVStore.table "Permanent link")

```
table: DuckDBPyRelation

```

Return the table for the connection to the DuckDB database.
###  from_vector_store `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/duckdb/#llama_index.storage.kvstore.duckdb.DuckDBKVStore.from_vector_store "Permanent link")

```
from_vector_store(
    duckdb_vector_store, table_name:  = "keyvalue"
) -> 

```

Load a DuckDBKVStore from a DuckDB Client.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `client`  |  `DuckDB`  |  DuckDB client  |  _required_  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-duckdb/llama_index/storage/kvstore/duckdb/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_vector_store(
    cls, duckdb_vector_store, table_name: str = "keyvalue"
) -> "DuckDBKVStore":
"""
    Load a DuckDBKVStore from a DuckDB Client.

    Args:
        client (DuckDB): DuckDB client

    """
    fromllama_index.vector_stores.duckdb.baseimport DuckDBVectorStore

    assert isinstance(duckdb_vector_store, DuckDBVectorStore)

    return cls(
        database_name=duckdb_vector_store.database_name,
        table_name=table_name,
        persist_dir=duckdb_vector_store.persist_dir,
        client=duckdb_vector_store.client,
    )

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/duckdb/#llama_index.storage.kvstore.duckdb.DuckDBKVStore.put "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-duckdb/llama_index/storage/kvstore/duckdb/base.py`  
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
```
 | 
```
@override
defput(self, key: str, val: dict, collection: str = DEFAULT_COLLECTION) -> None:
"""
    Put a key-value pair into the store.

    Args:
        key (str): key
        val (dict): value
        collection (str): collection name

    """
    self.put_all([(key, val)], collection)

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/duckdb/#llama_index.storage.kvstore.duckdb.DuckDBKVStore.aput "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-duckdb/llama_index/storage/kvstore/duckdb/base.py`  
| 
```
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
```
 | 
```
@override
async defaput(
    self, key: str, val: dict, collection: str = DEFAULT_COLLECTION
) -> None:
"""
    Put a key-value pair into the store.

    Args:
        key (str): key
        val (dict): value
        collection (str): collection name

    """
    await asyncio.to_thread(self.put, key, val, collection)

```
 |  
| --- | --- |  
###  put_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/duckdb/#llama_index.storage.kvstore.duckdb.DuckDBKVStore.put_all "Permanent link")

```
put_all(
    kv_pairs: [tuple[, ]],
    collection:  = DEFAULT_COLLECTION,
    batch_size:  = DEFAULT_BATCH_SIZE,
) -> None

```

Put a dictionary of key-value pairs into the store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `kv_pairs`  |  `List[Tuple[str, dict]]`  |  key-value pairs  |  _required_  |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-duckdb/llama_index/storage/kvstore/duckdb/base.py`  
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
```
 | 
```
@override
defput_all(
    self,
    kv_pairs: list[tuple[str, dict]],
    collection: str = DEFAULT_COLLECTION,
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> None:
"""
    Put a dictionary of key-value pairs into the store.

    Args:
        kv_pairs (List[Tuple[str, dict]]): key-value pairs
        collection (str): collection name

    """
    if len(kv_pairs) == 0:
        return

    rows = [
        {"key": key, "collection": collection, "value": json.dumps(value)}
        for key, value in kv_pairs
    ]
    arrow_table = pyarrow.Table.from_pylist(rows)

    _ = self.client.sql(
        query=f"""
        INSERT OR REPLACE INTO {self.table.alias}
        SELECT * from arrow_table;
        """,
    )

```
 |  
| --- | --- |  
###  aput_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/duckdb/#llama_index.storage.kvstore.duckdb.DuckDBKVStore.aput_all "Permanent link")

```
aput_all(
    kv_pairs: [tuple[, ]],
    collection:  = DEFAULT_COLLECTION,
    batch_size:  = DEFAULT_BATCH_SIZE,
) -> None

```

Put a dictionary of key-value pairs into the store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `kv_pairs`  |  `List[Tuple[str, dict]]`  |  key-value pairs  |  _required_  |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-duckdb/llama_index/storage/kvstore/duckdb/base.py`  
| 
```
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
```
 | 
```
@override
async defaput_all(
    self,
    kv_pairs: list[tuple[str, dict]],
    collection: str = DEFAULT_COLLECTION,
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> None:
"""
    Put a dictionary of key-value pairs into the store.

    Args:
        kv_pairs (List[Tuple[str, dict]]): key-value pairs
        collection (str): collection name

    """
    await asyncio.to_thread(self.put_all, kv_pairs, collection, batch_size)

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/duckdb/#llama_index.storage.kvstore.duckdb.DuckDBKVStore.get "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-duckdb/llama_index/storage/kvstore/duckdb/base.py`  
| 
```
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
```
 | 
```
@override
defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> Optional[dict]:
"""
    Get a value from the store.

    Args:
        key (str): key
        collection (str): collection name

    """
    expression: Expression = (
        ColumnExpression("collection")
        .__eq__(ConstantExpression(collection))
        .__and__(ColumnExpression("key").__eq__(ConstantExpression(key)))
    )
    row_result = self.table.filter(filter_expr=expression).fetchone()

    if row_result is None:
        return None

    return json.loads(row_result[2])

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/duckdb/#llama_index.storage.kvstore.duckdb.DuckDBKVStore.aget "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-duckdb/llama_index/storage/kvstore/duckdb/base.py`  
| 
```
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
```
 | 
```
@override
async defaget(
    self, key: str, collection: str = DEFAULT_COLLECTION
) -> Optional[dict]:
"""
    Get a value from the store.

    Args:
        key (str): key
        collection (str): collection name

    """
    return await asyncio.to_thread(self.get, key, collection)

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/duckdb/#llama_index.storage.kvstore.duckdb.DuckDBKVStore.get_all "Permanent link")

```
get_all(
    collection:  = DEFAULT_COLLECTION,
) -> [, ]

```

Get all values from the store.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-duckdb/llama_index/storage/kvstore/duckdb/base.py`  
| 
```
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
@override
defget_all(self, collection: str = DEFAULT_COLLECTION) -> dict[str, dict]:
"""Get all values from the store."""
    filter_expr: Expression = ColumnExpression("collection").__eq__(
        ConstantExpression(collection)
    )

    table: pyarrow.Table = self.table.filter(
        filter_expr=filter_expr
    ).fetch_arrow_table()

    as_list = table.to_pylist()

    return {row["key"]: json.loads(row["value"]) for row in as_list}

```
 |  
| --- | --- |  
###  aget_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/duckdb/#llama_index.storage.kvstore.duckdb.DuckDBKVStore.aget_all "Permanent link")

```
aget_all(
    collection:  = DEFAULT_COLLECTION,
) -> [, ]

```

Get all values from the store.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-duckdb/llama_index/storage/kvstore/duckdb/base.py`  
| 
```
308
309
310
311
```
 | 
```
@override
async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> dict[str, dict]:
"""Get all values from the store."""
    return self.get_all(collection)

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/duckdb/#llama_index.storage.kvstore.duckdb.DuckDBKVStore.delete "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-duckdb/llama_index/storage/kvstore/duckdb/base.py`  
| 
```
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
```
 | 
```
@override
defdelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
    Delete a value from the store.

    Args:
        key (str): key
        collection (str): collection name

    """
    filter_expression = (
        ColumnExpression("collection")
        .__eq__(ConstantExpression(collection))
        .__and__(ColumnExpression("key").__eq__(ConstantExpression(key)))
    )

    command = f"DELETE FROM {self.table.alias} WHERE {filter_expression}"
    _ = self.client.execute(command)
    return True

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/duckdb/#llama_index.storage.kvstore.duckdb.DuckDBKVStore.adelete "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-duckdb/llama_index/storage/kvstore/duckdb/base.py`  
| 
```
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
```
 | 
```
@override
async defadelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
    Delete a value from the store.

    Args:
        key (str): key
        collection (str): collection name

    """
    return self.delete(key, collection)

```
 |  
| --- | --- |  
options: members: - DuckDBKVStore
