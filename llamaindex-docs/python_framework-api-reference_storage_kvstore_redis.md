# Redis
##  RedisKVStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/redis/#llama_index.storage.kvstore.redis.RedisKVStore "Permanent link")
Bases: 
Redis KV Store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `redis_uri`  |  Redis URI  |  `'redis://127.0.0.1:6379'`  |  
|  `redis_client`  |  Redis client  |  `None`  |  
|  `async_redis_client`  |  Async Redis client  |  `None`  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If redis-py is not installed  |  
Examples:

```
>>> fromllama_index.storage.kvstore.redisimport RedisKVStore
>>> # Create a RedisKVStore
>>> redis_kv_store = RedisKVStore(
>>>     redis_url="redis://127.0.0.1:6379")

```

Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-redis/llama_index/storage/kvstore/redis/base.py`  
| 
```
 14
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
```
 | 
```
classRedisKVStore(BaseKVStore):
"""
    Redis KV Store.

    Args:
        redis_uri (str): Redis URI
        redis_client (Any): Redis client
        async_redis_client (Any): Async Redis client

    Raises:
            ValueError: If redis-py is not installed

    Examples:
        >>> from llama_index.storage.kvstore.redis import RedisKVStore
        >>> # Create a RedisKVStore
        >>> redis_kv_store = RedisKVStore(
        >>>     redis_url="redis://127.0.0.1:6379")

    """

    def__init__(
        self,
        redis_uri: Optional[str] = "redis://127.0.0.1:6379",
        redis_client: Optional[Redis] = None,
        async_redis_client: Optional[AsyncRedis] = None,
        **kwargs: Any,
    ) -> None:
        # user could inject customized redis client.
        # for instance, redis have specific TLS connection, etc.
        if redis_client is not None:
            self._redis_client = redis_client

            # create async client from sync client
            if async_redis_client is not None:
                self._async_redis_client = async_redis_client
            else:
                try:
                    self._async_redis_client = AsyncRedis.from_url(
                        self._redis_client.connection_pool.connection_kwargs["url"]
                    )
                except Exception:
                    print(
                        "Could not create async redis client from sync client, "
                        "pass in `async_redis_client` explicitly."
                    )
                    self._async_redis_client = None
        elif redis_uri is not None:
            # otherwise, try initializing redis client
            try:
                # connect to redis from url
                self._redis_client = Redis.from_url(redis_uri, **kwargs)
                self._async_redis_client = AsyncRedis.from_url(redis_uri, **kwargs)
            except ValueError as e:
                raise ValueError(f"Redis failed to connect: {e}")
        else:
            raise ValueError("Either 'redis_client' or redis_url must be provided.")

    defput(self, key: str, val: dict, collection: str = DEFAULT_COLLECTION) -> None:
"""
        Put a key-value pair into the store.

        Args:
            key (str): key
            val (dict): value
            collection (str): collection name

        """
        self._redis_client.hset(name=collection, key=key, value=json.dumps(val))

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
        await self._async_redis_client.hset(
            name=collection, key=key, value=json.dumps(val)
        )

    defput_all(
        self,
        kv_pairs: List[Tuple[str, dict]],
        collection: str = DEFAULT_COLLECTION,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
"""
        Put a dictionary of key-value pairs into the store.

        Args:
            kv_pairs (List[Tuple[str, dict]]): key-value pairs
            collection (str): collection name

        """
        with self._redis_client.pipeline() as pipe:
            cur_batch = 0
            for key, val in kv_pairs:
                pipe.hset(name=collection, key=key, value=json.dumps(val))
                cur_batch += 1

                if cur_batch >= batch_size:
                    cur_batch = 0
                    pipe.execute()

            if cur_batch  0:
                pipe.execute()

    defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> Optional[dict]:
"""
        Get a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        val_str = self._redis_client.hget(name=collection, key=key)
        if val_str is None:
            return None
        return json.loads(val_str)

    async defaget(
        self, key: str, collection: str = DEFAULT_COLLECTION
    ) -> Optional[dict]:
"""
        Get a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        val_str = await self._async_redis_client.hget(name=collection, key=key)
        if val_str is None:
            return None
        return json.loads(val_str)

    defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""Get all values from the store."""
        collection_kv_dict = {}
        for key, val_str in self._redis_client.hscan_iter(name=collection):
            value = dict(json.loads(val_str))
            collection_kv_dict[key.decode()] = value
        return collection_kv_dict

    async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""Get all values from the store."""
        collection_kv_dict = {}
        async for key, val_str in self._async_redis_client.hscan_iter(name=collection):
            value = dict(json.loads(val_str))
            collection_kv_dict[key.decode()] = value
        return collection_kv_dict

    defdelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
        Delete a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        deleted_num = self._redis_client.hdel(collection, key)
        return bool(deleted_num  0)

    async defadelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
        Delete a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        deleted_num = await self._async_redis_client.hdel(collection, key)
        return bool(deleted_num  0)

    @classmethod
    deffrom_host_and_port(
        cls,
        host: str,
        port: int,
    ) -> "RedisKVStore":
"""
        Load a RedisKVStore from a Redis host and port.

        Args:
            host (str): Redis host
            port (int): Redis port

        """
        url = f"redis://{host}:{port}".format(host=host, port=port)
        return cls(redis_uri=url)

    @classmethod
    deffrom_redis_client(cls, redis_client: Any) -> "RedisKVStore":
"""
        Load a RedisKVStore from a Redis Client.

        Args:
            redis_client (Redis): Redis client

        """
        return cls(redis_client=redis_client)

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/redis/#llama_index.storage.kvstore.redis.RedisKVStore.put "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-redis/llama_index/storage/kvstore/redis/base.py`  
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
```
 | 
```
defput(self, key: str, val: dict, collection: str = DEFAULT_COLLECTION) -> None:
"""
    Put a key-value pair into the store.

    Args:
        key (str): key
        val (dict): value
        collection (str): collection name

    """
    self._redis_client.hset(name=collection, key=key, value=json.dumps(val))

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/redis/#llama_index.storage.kvstore.redis.RedisKVStore.aput "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-redis/llama_index/storage/kvstore/redis/base.py`  
| 
```
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
```
 | 
```
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
    await self._async_redis_client.hset(
        name=collection, key=key, value=json.dumps(val)
    )

```
 |  
| --- | --- |  
###  put_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/redis/#llama_index.storage.kvstore.redis.RedisKVStore.put_all "Permanent link")

```
put_all(
    kv_pairs: [Tuple[, ]],
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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-redis/llama_index/storage/kvstore/redis/base.py`  
| 
```
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
```
 | 
```
defput_all(
    self,
    kv_pairs: List[Tuple[str, dict]],
    collection: str = DEFAULT_COLLECTION,
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> None:
"""
    Put a dictionary of key-value pairs into the store.

    Args:
        kv_pairs (List[Tuple[str, dict]]): key-value pairs
        collection (str): collection name

    """
    with self._redis_client.pipeline() as pipe:
        cur_batch = 0
        for key, val in kv_pairs:
            pipe.hset(name=collection, key=key, value=json.dumps(val))
            cur_batch += 1

            if cur_batch >= batch_size:
                cur_batch = 0
                pipe.execute()

        if cur_batch  0:
            pipe.execute()

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/redis/#llama_index.storage.kvstore.redis.RedisKVStore.get "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-redis/llama_index/storage/kvstore/redis/base.py`  
| 
```
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
    val_str = self._redis_client.hget(name=collection, key=key)
    if val_str is None:
        return None
    return json.loads(val_str)

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/redis/#llama_index.storage.kvstore.redis.RedisKVStore.aget "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-redis/llama_index/storage/kvstore/redis/base.py`  
| 
```
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
    val_str = await self._async_redis_client.hget(name=collection, key=key)
    if val_str is None:
        return None
    return json.loads(val_str)

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/redis/#llama_index.storage.kvstore.redis.RedisKVStore.get_all "Permanent link")

```
get_all(
    collection:  = DEFAULT_COLLECTION,
) -> [, ]

```

Get all values from the store.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-redis/llama_index/storage/kvstore/redis/base.py`  
| 
```
156
157
158
159
160
161
162
```
 | 
```
defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""Get all values from the store."""
    collection_kv_dict = {}
    for key, val_str in self._redis_client.hscan_iter(name=collection):
        value = dict(json.loads(val_str))
        collection_kv_dict[key.decode()] = value
    return collection_kv_dict

```
 |  
| --- | --- |  
###  aget_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/redis/#llama_index.storage.kvstore.redis.RedisKVStore.aget_all "Permanent link")

```
aget_all(
    collection:  = DEFAULT_COLLECTION,
) -> [, ]

```

Get all values from the store.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-redis/llama_index/storage/kvstore/redis/base.py`  
| 
```
164
165
166
167
168
169
170
```
 | 
```
async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""Get all values from the store."""
    collection_kv_dict = {}
    async for key, val_str in self._async_redis_client.hscan_iter(name=collection):
        value = dict(json.loads(val_str))
        collection_kv_dict[key.decode()] = value
    return collection_kv_dict

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/redis/#llama_index.storage.kvstore.redis.RedisKVStore.delete "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-redis/llama_index/storage/kvstore/redis/base.py`  
| 
```
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
    deleted_num = self._redis_client.hdel(collection, key)
    return bool(deleted_num  0)

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/redis/#llama_index.storage.kvstore.redis.RedisKVStore.adelete "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-redis/llama_index/storage/kvstore/redis/base.py`  
| 
```
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
    deleted_num = await self._async_redis_client.hdel(collection, key)
    return bool(deleted_num  0)

```
 |  
| --- | --- |  
###  from_host_and_port `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/redis/#llama_index.storage.kvstore.redis.RedisKVStore.from_host_and_port "Permanent link")

```
from_host_and_port(host: , port: ) -> 

```

Load a RedisKVStore from a Redis host and port.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `host`  |  Redis host  |  _required_  |  
|  `port`  |  Redis port  |  _required_  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-redis/llama_index/storage/kvstore/redis/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_host_and_port(
    cls,
    host: str,
    port: int,
) -> "RedisKVStore":
"""
    Load a RedisKVStore from a Redis host and port.

    Args:
        host (str): Redis host
        port (int): Redis port

    """
    url = f"redis://{host}:{port}".format(host=host, port=port)
    return cls(redis_uri=url)

```
 |  
| --- | --- |  
###  from_redis_client `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/redis/#llama_index.storage.kvstore.redis.RedisKVStore.from_redis_client "Permanent link")

```
from_redis_client(redis_client: ) -> 

```

Load a RedisKVStore from a Redis Client.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `redis_client`  |  `Redis`  |  Redis client  |  _required_  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-redis/llama_index/storage/kvstore/redis/base.py`  
| 
```
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
@classmethod
deffrom_redis_client(cls, redis_client: Any) -> "RedisKVStore":
"""
    Load a RedisKVStore from a Redis Client.

    Args:
        redis_client (Redis): Redis client

    """
    return cls(redis_client=redis_client)

```
 |  
| --- | --- |  
options: members: - RedisKVStore
