# Mongodb
##  MongoDBKVStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/mongodb/#llama_index.storage.kvstore.mongodb.MongoDBKVStore "Permanent link")
Bases: 
MongoDB Key-Value store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `mongo_client`  |  MongoDB client  |  _required_  |  
|  `uri`  |  `Optional[str]`  |  MongoDB URI  |  `None`  |  
|  `host`  |  `Optional[str]`  |  MongoDB host  |  `None`  |  
|  `port`  |  `Optional[int]`  |  MongoDB port  |  `None`  |  
|  `db_name`  |  `Optional[str]`  |  MongoDB database name  |  `None`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-mongodb/llama_index/storage/kvstore/mongodb/base.py`  
| 
```
 15
 16
 17
 18
 19
 20
 21
 22
 23
 24
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
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
```
 | 
```
classMongoDBKVStore(BaseKVStore):
"""
    MongoDB Key-Value store.

    Args:
        mongo_client (Any): MongoDB client
        uri (Optional[str]): MongoDB URI
        host (Optional[str]): MongoDB host
        port (Optional[int]): MongoDB port
        db_name (Optional[str]): MongoDB database name

    """

    def__init__(
        self,
        mongo_client: Any,
        mongo_aclient: Optional[Any] = None,
        uri: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        db_name: Optional[str] = None,
    ) -> None:
"""Init a MongoDBKVStore."""
        try:
            frompymongoimport MongoClient, AsyncMongoClient
            frompymongo.driver_infoimport DriverInfo
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        self._client = cast(MongoClient, mongo_client)
        self._aclient = cast(AsyncMongoClient, mongo_aclient) if mongo_aclient else None

        self._uri = uri
        self._host = host
        self._port = port

        self._db_name = db_name or "db_docstore"
        self._db = self._client[self._db_name]
        self._adb = self._aclient[self._db_name] if self._aclient else None

        # append_metadata was added in PyMongo 4.14.0, but is a valid database name on earlier versions
        if callable(self._client.append_metadata):
            self._client.append_metadata(
                DriverInfo(name="llama-index", version=version("llama-index"))
            )
        if callable(self._aclient.append_metadata):
            self._aclient.append_metadata(
                DriverInfo(name="llama-index", version=version("llama-index"))
            )

    @classmethod
    deffrom_uri(
        cls,
        uri: str,
        db_name: Optional[str] = None,
    ) -> "MongoDBKVStore":
"""
        Load a MongoDBKVStore from a MongoDB URI.

        Args:
            uri (str): MongoDB URI
            db_name (Optional[str]): MongoDB database name

        """
        try:
            frompymongoimport MongoClient, AsyncMongoClient
            frompymongo.driver_infoimport DriverInfo
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        mongo_client: MongoClient = MongoClient(uri, appname=APP_NAME)
        mongo_aclient: AsyncMongoClient = AsyncMongoClient(uri)

        # append_metadata was added in PyMongo 4.14.0, but is a valid database name on earlier versions
        if callable(mongo_client.append_metadata):
            mongo_client.append_metadata(
                DriverInfo(name="llama-index", version=version("llama-index"))
            )
        if callable(mongo_aclient.append_metadata):
            mongo_aclient.append_metadata(
                DriverInfo(name="llama-index", version=version("llama-index"))
            )

        return cls(
            mongo_client=mongo_client,
            mongo_aclient=mongo_aclient,
            db_name=db_name,
            uri=uri,
        )

    @classmethod
    deffrom_host_and_port(
        cls,
        host: str,
        port: int,
        db_name: Optional[str] = None,
    ) -> "MongoDBKVStore":
"""
        Load a MongoDBKVStore from a MongoDB host and port.

        Args:
            host (str): MongoDB host
            port (int): MongoDB port
            db_name (Optional[str]): MongoDB database name

        """
        try:
            frompymongoimport MongoClient, AsyncMongoClient
            frompymongo.driver_infoimport DriverInfo
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        mongo_client: MongoClient = MongoClient(host, port, appname=APP_NAME)
        mongo_aclient: AsyncMongoClient = AsyncMongoClient(host, port, appname=APP_NAME)

        # append_metadata was added in PyMongo 4.14.0, but is a valid database name on earlier versions
        if callable(mongo_client.append_metadata):
            mongo_client.append_metadata(
                DriverInfo(name="llama-index", version=version("llama-index"))
            )
        if callable(mongo_aclient.append_metadata):
            mongo_aclient.append_metadata(
                DriverInfo(name="llama-index", version=version("llama-index"))
            )

        return cls(
            mongo_client=mongo_client,
            mongo_aclient=mongo_aclient,
            db_name=db_name,
            host=host,
            port=port,
        )

    def_check_async_client(self) -> None:
        if self._adb is None:
            raise ValueError("MongoDBKVStore was not initialized with an async client")

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
        frompymongoimport UpdateOne

        # Prepare documents with '_id' set to the key for batch insertion
        docs = [{"_id": key, **value} for key, value in kv_pairs]

        # Insert documents in batches
        for batch in (
            docs[i : i + batch_size] for i in range(0, len(docs), batch_size)
        ):
            new_docs = []
            for doc in batch:
                new_docs.append(
                    UpdateOne({"_id": doc["_id"]}, {"$set": doc}, upsert=True)
                )

            self._db[collection].bulk_write(new_docs)

    async defaput_all(
        self,
        kv_pairs: List[Tuple[str, dict]],
        collection: str = DEFAULT_COLLECTION,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
        frompymongoimport UpdateOne

        self._check_async_client()

        # Prepare documents with '_id' set to the key for batch insertion
        docs = [{"_id": key, **value} for key, value in kv_pairs]

        # Insert documents in batches
        for batch in (
            docs[i : i + batch_size] for i in range(0, len(docs), batch_size)
        ):
            new_docs = []
            for doc in batch:
                new_docs.append(
                    UpdateOne({"_id": doc["_id"]}, {"$set": doc}, upsert=True)
                )

            await self._adb[collection].bulk_write(new_docs)

    defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> Optional[dict]:
"""
        Get a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        result = self._db[collection].find_one({"_id": key})
        if result is not None:
            result.pop("_id")
            return result
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
        self._check_async_client()

        result = await self._adb[collection].find_one({"_id": key})
        if result is not None:
            result.pop("_id")
            return result
        return None

    defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
        Get all values from the store.

        Args:
            collection (str): collection name

        """
        results = self._db[collection].find()
        output = {}
        for result in results:
            key = result.pop("_id")
            output[key] = result
        return output

    async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
        Get all values from the store.

        Args:
            collection (str): collection name

        """
        self._check_async_client()

        results = self._adb[collection].find()
        output = {}
        for result in await results.to_list(length=None):
            key = result.pop("_id")
            output[key] = result
        return output

    defdelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
        Delete a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        result = self._db[collection].delete_one({"_id": key})
        return result.deleted_count  0

    async defadelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
        Delete a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        self._check_async_client()

        result = await self._adb[collection].delete_one({"_id": key})
        return result.deleted_count  0

```
 |  
| --- | --- |  
###  from_uri `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/mongodb/#llama_index.storage.kvstore.mongodb.MongoDBKVStore.from_uri "Permanent link")

```
from_uri(
    uri: , db_name: Optional[] = None
) -> 

```

Load a MongoDBKVStore from a MongoDB URI.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `uri`  |  MongoDB URI  |  _required_  |  
|  `db_name`  |  `Optional[str]`  |  MongoDB database name  |  `None`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-mongodb/llama_index/storage/kvstore/mongodb/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_uri(
    cls,
    uri: str,
    db_name: Optional[str] = None,
) -> "MongoDBKVStore":
"""
    Load a MongoDBKVStore from a MongoDB URI.

    Args:
        uri (str): MongoDB URI
        db_name (Optional[str]): MongoDB database name

    """
    try:
        frompymongoimport MongoClient, AsyncMongoClient
        frompymongo.driver_infoimport DriverInfo
    except ImportError:
        raise ImportError(IMPORT_ERROR_MSG)

    mongo_client: MongoClient = MongoClient(uri, appname=APP_NAME)
    mongo_aclient: AsyncMongoClient = AsyncMongoClient(uri)

    # append_metadata was added in PyMongo 4.14.0, but is a valid database name on earlier versions
    if callable(mongo_client.append_metadata):
        mongo_client.append_metadata(
            DriverInfo(name="llama-index", version=version("llama-index"))
        )
    if callable(mongo_aclient.append_metadata):
        mongo_aclient.append_metadata(
            DriverInfo(name="llama-index", version=version("llama-index"))
        )

    return cls(
        mongo_client=mongo_client,
        mongo_aclient=mongo_aclient,
        db_name=db_name,
        uri=uri,
    )

```
 |  
| --- | --- |  
###  from_host_and_port `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/mongodb/#llama_index.storage.kvstore.mongodb.MongoDBKVStore.from_host_and_port "Permanent link")

```
from_host_and_port(
    host: , port: , db_name: Optional[] = None
) -> 

```

Load a MongoDBKVStore from a MongoDB host and port.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `host`  |  MongoDB host  |  _required_  |  
|  `port`  |  MongoDB port  |  _required_  |  
|  `db_name`  |  `Optional[str]`  |  MongoDB database name  |  `None`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-mongodb/llama_index/storage/kvstore/mongodb/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_host_and_port(
    cls,
    host: str,
    port: int,
    db_name: Optional[str] = None,
) -> "MongoDBKVStore":
"""
    Load a MongoDBKVStore from a MongoDB host and port.

    Args:
        host (str): MongoDB host
        port (int): MongoDB port
        db_name (Optional[str]): MongoDB database name

    """
    try:
        frompymongoimport MongoClient, AsyncMongoClient
        frompymongo.driver_infoimport DriverInfo
    except ImportError:
        raise ImportError(IMPORT_ERROR_MSG)

    mongo_client: MongoClient = MongoClient(host, port, appname=APP_NAME)
    mongo_aclient: AsyncMongoClient = AsyncMongoClient(host, port, appname=APP_NAME)

    # append_metadata was added in PyMongo 4.14.0, but is a valid database name on earlier versions
    if callable(mongo_client.append_metadata):
        mongo_client.append_metadata(
            DriverInfo(name="llama-index", version=version("llama-index"))
        )
    if callable(mongo_aclient.append_metadata):
        mongo_aclient.append_metadata(
            DriverInfo(name="llama-index", version=version("llama-index"))
        )

    return cls(
        mongo_client=mongo_client,
        mongo_aclient=mongo_aclient,
        db_name=db_name,
        host=host,
        port=port,
    )

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/mongodb/#llama_index.storage.kvstore.mongodb.MongoDBKVStore.put "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-mongodb/llama_index/storage/kvstore/mongodb/base.py`  
| 
```
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
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/mongodb/#llama_index.storage.kvstore.mongodb.MongoDBKVStore.aput "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-mongodb/llama_index/storage/kvstore/mongodb/base.py`  
| 
```
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
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/mongodb/#llama_index.storage.kvstore.mongodb.MongoDBKVStore.get "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-mongodb/llama_index/storage/kvstore/mongodb/base.py`  
| 
```
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
    result = self._db[collection].find_one({"_id": key})
    if result is not None:
        result.pop("_id")
        return result
    return None

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/mongodb/#llama_index.storage.kvstore.mongodb.MongoDBKVStore.aget "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-mongodb/llama_index/storage/kvstore/mongodb/base.py`  
| 
```
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
async defaget(
    self, key: str, collection: str = DEFAULT_COLLECTION
) -> Optional[dict]:
"""
    Get a value from the store.

    Args:
        key (str): key
        collection (str): collection name

    """
    self._check_async_client()

    result = await self._adb[collection].find_one({"_id": key})
    if result is not None:
        result.pop("_id")
        return result
    return None

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/mongodb/#llama_index.storage.kvstore.mongodb.MongoDBKVStore.get_all "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-mongodb/llama_index/storage/kvstore/mongodb/base.py`  
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
279
280
281
```
 | 
```
defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
    Get all values from the store.

    Args:
        collection (str): collection name

    """
    results = self._db[collection].find()
    output = {}
    for result in results:
        key = result.pop("_id")
        output[key] = result
    return output

```
 |  
| --- | --- |  
###  aget_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/mongodb/#llama_index.storage.kvstore.mongodb.MongoDBKVStore.aget_all "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-mongodb/llama_index/storage/kvstore/mongodb/base.py`  
| 
```
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
async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
    Get all values from the store.

    Args:
        collection (str): collection name

    """
    self._check_async_client()

    results = self._adb[collection].find()
    output = {}
    for result in await results.to_list(length=None):
        key = result.pop("_id")
        output[key] = result
    return output

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/mongodb/#llama_index.storage.kvstore.mongodb.MongoDBKVStore.delete "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-mongodb/llama_index/storage/kvstore/mongodb/base.py`  
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
    result = self._db[collection].delete_one({"_id": key})
    return result.deleted_count  0

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/mongodb/#llama_index.storage.kvstore.mongodb.MongoDBKVStore.adelete "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-mongodb/llama_index/storage/kvstore/mongodb/base.py`  
| 
```
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
    self._check_async_client()

    result = await self._adb[collection].delete_one({"_id": key})
    return result.deleted_count  0

```
 |  
| --- | --- |  
options: members: - MongoDBKVStore
