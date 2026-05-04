# Redis
##  RedisChatStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/redis/#llama_index.storage.chat_store.redis.RedisChatStore "Permanent link")
Bases: 
Redis chat store.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-redis/llama_index/storage/chat_store/redis/base.py`  
| 
```
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
```
 | 
```
classRedisChatStore(BaseChatStore):
"""Redis chat store."""

    redis_url: str = Field(default="redis://localhost:6379", description="Redis URL.")
    ttl: Optional[int] = Field(default=None, description="Time to live in seconds.")

    _redis_client: Optional[Redis] = PrivateAttr()
    _aredis_client: Optional[AsyncRedis] = PrivateAttr()

    def__init__(
        self,
        redis_url: str = "redis://localhost:6379",
        redis_client: Optional[Redis] = None,
        aredis_client: Optional[AsyncRedis] = None,
        ttl: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize."""
        super().__init__(ttl=ttl)

        self._redis_client = redis_client or self._get_client(redis_url, **kwargs)
        self._aredis_client = aredis_client or self._aget_client(redis_url, **kwargs)

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "RedisChatStore"

    defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Set messages for a key."""
        self._redis_client.delete(key)
        for message in messages:
            self.add_message(key, message)

        if self.ttl:
            self._redis_client.expire(key, self.ttl)

    async defaset_messages(self, key: str, messages: List[ChatMessage]) -> None:
        await self._aredis_client.delete(key)
        for message in messages:
            await self.async_add_message(key, message)

        if self.ttl:
            await self._aredis_client.expire(key, self.ttl)

    defget_messages(self, key: str) -> List[ChatMessage]:
"""Get messages for a key."""
        items = self._redis_client.lrange(key, 0, -1)
        if len(items) == 0:
            return []
        return [ChatMessage.model_validate_json(item) for item in items]

    async defaget_messages(self, key: str) -> List[ChatMessage]:
"""Get messages for a key."""
        items = await self._aredis_client.lrange(key, 0, -1)
        if len(items) == 0:
            return []
        return [ChatMessage.model_validate_json(item) for item in items]

    defadd_message(
        self, key: str, message: ChatMessage, idx: Optional[int] = None
    ) -> None:
"""Add a message for a key."""
        if idx is None:
            self._redis_client.rpush(key, message.model_dump_json())
        else:
            self._insert_element_at_index(key, idx, message)

        if self.ttl:
            self._redis_client.expire(key, self.ttl)

    async defasync_add_message(
        self, key: str, message: ChatMessage, idx: Optional[int] = None
    ) -> None:
"""Add a message for a key."""
        if idx is None:
            await self._aredis_client.rpush(key, message.model_dump_json())
        else:
            await self._ainsert_element_at_index(key, idx, message)

        if self.ttl:
            await self._aredis_client.expire(key, self.ttl)

    defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Delete messages for a key."""
        self._redis_client.delete(key)
        return None

    async defadelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Delete messages for a key."""
        await self._aredis_client.delete(key)
        return None

    defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
        current_list = self._redis_client.lrange(key, 0, -1)
        if 0 <= idx  len(current_list):
            removed_item = current_list.pop(idx)

            self._redis_client.delete(key)
            self._redis_client.lpush(key, *current_list)
            return removed_item
        else:
            return None

    async defadelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
        current_list = await self._aredis_client.lrange(key, 0, -1)
        if 0 <= idx  len(current_list):
            removed_item = current_list.pop(idx)

            await self._aredis_client.delete(key)
            await self._aredis_client.lpush(key, *current_list)
            return removed_item
        else:
            return None

    defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete last message for a key."""
        return self._redis_client.rpop(key)

    defget_keys(self) -> List[str]:
"""Get all keys."""
        return [key.decode("utf-8") for key in self._redis_client.keys("*")]

    def_insert_element_at_index(
        self, key: str, index: int, message: ChatMessage
    ) -> List[ChatMessage]:
        # Step 1: Retrieve the current list
        current_list = self.get_messages(key)
        # Step 2: Insert the new element at the desired index in the local list
        current_list.insert(index, message)

        # Step 3: Push the modified local list back to Redis
        self._redis_client.delete(key)  # Remove the existing list
        self.set_messages(key, current_list)
        return self.get_messages(key)

    async def_ainsert_element_at_index(
        self, key: str, index: int, message: ChatMessage
    ) -> List[ChatMessage]:
        # Step 1: Retrieve the current list
        current_list = await self.aget_messages(key)
        # Step 2: Insert the new element at the desired index in the local list
        current_list.insert(index, message)

        # Step 3: Push the modified local list back to Redis
        await self._aredis_client.delete(key)  # Remove the existing list
        await self.aset_messages(key, current_list)
        return await self.aget_messages(key)

    def_redis_cluster_client(self, redis_url: str, **kwargs: Any) -> "Redis":
        return RedisCluster.from_url(redis_url, **kwargs)  # type: ignore

    def_aredis_cluster_client(self, redis_url: str, **kwargs: Any) -> "AsyncRedis":
        return AsyncRedisCluster.from_url(redis_url, **kwargs)

    def_check_for_cluster(self, redis_client: Union["Redis", "AsyncRedis"]) -> bool:
        try:
            cluster_info = redis_client.info("cluster")
            return cluster_info["cluster_enabled"] == 1
        except redis.exceptions.RedisError:
            return False

    def_redis_sentinel_parser(
        self, redis_url: str, **kwargs
    ) -> Tuple[str, List[Tuple[str, int]]]:
"""
        Helper method to parse an (un-official) redis+sentinel url
        and create a Sentinel connection to fetch the final redis client
        connection to a replica-master for read-write operations.

        If username and/or password for authentication is given the
        same credentials are used for the Redis Sentinel as well as Redis Server.
        With this implementation using a redis url only it is not possible
        to use different data for authentication on booth systems.
        """
        parsed_url = urlparse(redis_url)
        # sentinel needs list with (host, port) tuple, use default port if none available
        sentinel_list = [(parsed_url.hostname or "localhost", parsed_url.port or 26379)]
        if parsed_url.path:
            # "/mymaster/0" first part is service name, optional second part is db number
            path_parts = parsed_url.path.split("/")
            service_name = path_parts[1] or "mymaster"
            if len(path_parts)  2:
                kwargs["db"] = path_parts[2]
        else:
            service_name = "mymaster"

        sentinel_args = {}
        if parsed_url.password:
            sentinel_args["password"] = parsed_url.password
            kwargs["password"] = parsed_url.password
        if parsed_url.username:
            sentinel_args["username"] = parsed_url.username
            kwargs["username"] = parsed_url.username

        # check for all SSL related properties and copy them into sentinel_kwargs too,
        # add client_name also
        for arg in kwargs:
            if arg.startswith("ssl") or arg == "client_name":
                sentinel_args[arg] = kwargs[arg]

        return sentinel_args, sentinel_list, service_name, kwargs

    def_redis_sentinel_client(self, redis_url: str, **kwargs: Any) -> "Redis":
        (
            sentinel_args,
            sentinel_list,
            service_name,
            kwargs,
        ) = self._redis_sentinel_parser(redis_url, **kwargs)
        # sentinel user/pass is part of sentinel_kwargs, user/pass for redis server
        # connection as direct parameter in kwargs
        sentinel_client = Sentinel(
            sentinel_list, sentinel_kwargs=sentinel_args, **kwargs
        )

        # redis server might have password but not sentinel - fetch this error and try
        # again without pass, everything else cannot be handled here -> user needed
        try:
            sentinel_client.execute_command("ping")
        except redis.exceptions.AuthenticationError:
            exception_info = sys.exc_info()
            exception = exception_info[1] or None
            if exception is not None and "no password is set" in exception.args[0]:
                logging.warning(
                    msg="Redis sentinel connection configured with password but Sentinel \
    answered NO PASSWORD NEEDED - Please check Sentinel configuration"
                )
                sentinel_client = Sentinel(sentinel_list, **kwargs)
            else:
                raise

        return sentinel_client.master_for(service_name)

    def_aredis_sentinel_client(self, redis_url: str, **kwargs: Any) -> "AsyncRedis":
        (
            sentinel_args,
            sentinel_list,
            service_name,
            kwargs,
        ) = self._redis_sentinel_parser(redis_url, **kwargs)
        sentinel_client = AsyncSentinel(
            sentinel_list, sentinel_kwargs=sentinel_args, **kwargs
        )

        try:
            asyncio.run(sentinel_client.execute_command("ping"))
        except redis.exceptions.AuthenticationError:
            exception_info = sys.exc_info()
            exception = exception_info[1] or None
            if exception is not None and "no password is set" in exception.args[0]:
                logging.warning(
                    msg="Redis sentinel connection configured with password but Sentinel \
    answered NO PASSWORD NEEDED - Please check Sentinel configuration"
                )
                sentinel_client = AsyncSentinel(sentinel_list, **kwargs)
            else:
                raise

        return sentinel_client.master_for(service_name)

    def_get_client(self, redis_url: str, **kwargs: Any) -> "Redis":
"""
        Get a redis client from the connection url given. This helper accepts
        urls for Redis server (TCP with/without TLS or UnixSocket) as well as
        Redis Sentinel connections.

        Redis Cluster is not supported.

        Before creating a connection the existence of the database driver is checked
        an and ValueError raised otherwise

        To use, you should have the ``redis`` python package installed.

        Example:
            .. code-block:: python

                redis_client = get_client(
                    redis_url="redis://username:password@localhost:6379"


        To use a redis replication setup with multiple redis server and redis sentinels
        set "redis_url" to "redis+sentinel://" scheme. With this url format a path is
        needed holding the name of the redis service within the sentinels to get the
        correct redis server connection. The default service name is "mymaster". The
        optional second part of the path is the redis db number to connect to.

        An optional username or password is used for booth connections to the rediserver
        and the sentinel, different passwords for server and sentinel are not supported.
        And as another constraint only one sentinel instance can be given:

        Example:
            .. code-block:: python

                redis_client = get_client(
                    redis_url="redis+sentinel://username:password@sentinelhost:26379/mymaster/0"


        """
        # Initialize with necessary components.
        redis_client: "Redis"
        # check if normal redis:// or redis+sentinel:// url
        if redis_url.startswith("redis+sentinel"):
            redis_client = self._redis_sentinel_client(redis_url, **kwargs)
        elif redis_url.startswith(
            "rediss+sentinel"
        ):  # sentinel with TLS support enables
            kwargs["ssl"] = True
            if "ssl_cert_reqs" not in kwargs:
                kwargs["ssl_cert_reqs"] = "none"
            redis_client = self._redis_sentinel_client(redis_url, **kwargs)
        else:
            # connect to redis server from url, reconnect with cluster client if needed
            redis_client = Redis.from_url(redis_url, **kwargs)
            if self._check_for_cluster(redis_client):
                redis_client.close()
                redis_client = self._redis_cluster_client(redis_url, **kwargs)
        return redis_client

    def_aget_client(self, redis_url: str, **kwargs: Any) -> "AsyncRedis":
        aredis_client: "AsyncRedis"
        # check if normal redis:// or redis+sentinel:// url
        if redis_url.startswith("redis+sentinel"):
            aredis_client = self._aredis_sentinel_client(redis_url, **kwargs)
        elif redis_url.startswith(
            "rediss+sentinel"
        ):  # sentinel with TLS support enables
            kwargs["ssl"] = True
            if "ssl_cert_reqs" not in kwargs:
                kwargs["ssl_cert_reqs"] = "none"
            aredis_client = self._aredis_sentinel_client(redis_url, **kwargs)
        else:
            # connect to redis server from url, reconnect with cluster client if needed
            aredis_client = AsyncRedis.from_url(redis_url, **kwargs)
            redis_client = Redis.from_url(redis_url, **kwargs)
            is_cluster = self._check_for_cluster(redis_client)
            redis_client.close()

            if is_cluster:
                asyncio.create_task(aredis_client.close())
                aredis_client = self._aredis_cluster_client(redis_url, **kwargs)
        return aredis_client

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/redis/#llama_index.storage.chat_store.redis.RedisChatStore.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-redis/llama_index/storage/chat_store/redis/base.py`  
| 
```
42
43
44
45
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "RedisChatStore"

```
 |  
| --- | --- |  
###  set_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/redis/#llama_index.storage.chat_store.redis.RedisChatStore.set_messages "Permanent link")

```
set_messages(key: , messages: []) -> None

```

Set messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-redis/llama_index/storage/chat_store/redis/base.py`  
| 
```
47
48
49
50
51
52
53
54
```
 | 
```
defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Set messages for a key."""
    self._redis_client.delete(key)
    for message in messages:
        self.add_message(key, message)

    if self.ttl:
        self._redis_client.expire(key, self.ttl)

```
 |  
| --- | --- |  
###  get_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/redis/#llama_index.storage.chat_store.redis.RedisChatStore.get_messages "Permanent link")

```
get_messages(key: ) -> []

```

Get messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-redis/llama_index/storage/chat_store/redis/base.py`  
| 
```
64
65
66
67
68
69
```
 | 
```
defget_messages(self, key: str) -> List[ChatMessage]:
"""Get messages for a key."""
    items = self._redis_client.lrange(key, 0, -1)
    if len(items) == 0:
        return []
    return [ChatMessage.model_validate_json(item) for item in items]

```
 |  
| --- | --- |  
###  aget_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/redis/#llama_index.storage.chat_store.redis.RedisChatStore.aget_messages "Permanent link")

```
aget_messages(key: ) -> []

```

Get messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-redis/llama_index/storage/chat_store/redis/base.py`  
| 
```
71
72
73
74
75
76
```
 | 
```
async defaget_messages(self, key: str) -> List[ChatMessage]:
"""Get messages for a key."""
    items = await self._aredis_client.lrange(key, 0, -1)
    if len(items) == 0:
        return []
    return [ChatMessage.model_validate_json(item) for item in items]

```
 |  
| --- | --- |  
###  add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/redis/#llama_index.storage.chat_store.redis.RedisChatStore.add_message "Permanent link")

```
add_message(
    key: ,
    message: ,
    idx: Optional[] = None,
) -> None

```

Add a message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-redis/llama_index/storage/chat_store/redis/base.py`  
| 
```
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
```
 | 
```
defadd_message(
    self, key: str, message: ChatMessage, idx: Optional[int] = None
) -> None:
"""Add a message for a key."""
    if idx is None:
        self._redis_client.rpush(key, message.model_dump_json())
    else:
        self._insert_element_at_index(key, idx, message)

    if self.ttl:
        self._redis_client.expire(key, self.ttl)

```
 |  
| --- | --- |  
###  async_add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/redis/#llama_index.storage.chat_store.redis.RedisChatStore.async_add_message "Permanent link")

```
async_add_message(
    key: ,
    message: ,
    idx: Optional[] = None,
) -> None

```

Add a message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-redis/llama_index/storage/chat_store/redis/base.py`  
| 
```
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
```
 | 
```
async defasync_add_message(
    self, key: str, message: ChatMessage, idx: Optional[int] = None
) -> None:
"""Add a message for a key."""
    if idx is None:
        await self._aredis_client.rpush(key, message.model_dump_json())
    else:
        await self._ainsert_element_at_index(key, idx, message)

    if self.ttl:
        await self._aredis_client.expire(key, self.ttl)

```
 |  
| --- | --- |  
###  delete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/redis/#llama_index.storage.chat_store.redis.RedisChatStore.delete_messages "Permanent link")

```
delete_messages(key: ) -> Optional[[]]

```

Delete messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-redis/llama_index/storage/chat_store/redis/base.py`  
| 
```
102
103
104
105
```
 | 
```
defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Delete messages for a key."""
    self._redis_client.delete(key)
    return None

```
 |  
| --- | --- |  
###  adelete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/redis/#llama_index.storage.chat_store.redis.RedisChatStore.adelete_messages "Permanent link")

```
adelete_messages(key: ) -> Optional[[]]

```

Delete messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-redis/llama_index/storage/chat_store/redis/base.py`  
| 
```
107
108
109
110
```
 | 
```
async defadelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Delete messages for a key."""
    await self._aredis_client.delete(key)
    return None

```
 |  
| --- | --- |  
###  delete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/redis/#llama_index.storage.chat_store.redis.RedisChatStore.delete_message "Permanent link")

```
delete_message(key: , idx: ) -> Optional[]

```

Delete specific message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-redis/llama_index/storage/chat_store/redis/base.py`  
| 
```
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
```
 | 
```
defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
    current_list = self._redis_client.lrange(key, 0, -1)
    if 0 <= idx  len(current_list):
        removed_item = current_list.pop(idx)

        self._redis_client.delete(key)
        self._redis_client.lpush(key, *current_list)
        return removed_item
    else:
        return None

```
 |  
| --- | --- |  
###  adelete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/redis/#llama_index.storage.chat_store.redis.RedisChatStore.adelete_message "Permanent link")

```
adelete_message(
    key: , idx: 
) -> Optional[]

```

Delete specific message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-redis/llama_index/storage/chat_store/redis/base.py`  
| 
```
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
```
 | 
```
async defadelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
    current_list = await self._aredis_client.lrange(key, 0, -1)
    if 0 <= idx  len(current_list):
        removed_item = current_list.pop(idx)

        await self._aredis_client.delete(key)
        await self._aredis_client.lpush(key, *current_list)
        return removed_item
    else:
        return None

```
 |  
| --- | --- |  
###  delete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/redis/#llama_index.storage.chat_store.redis.RedisChatStore.delete_last_message "Permanent link")

```
delete_last_message(key: ) -> Optional[]

```

Delete last message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-redis/llama_index/storage/chat_store/redis/base.py`  
| 
```
136
137
138
```
 | 
```
defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete last message for a key."""
    return self._redis_client.rpop(key)

```
 |  
| --- | --- |  
###  get_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/redis/#llama_index.storage.chat_store.redis.RedisChatStore.get_keys "Permanent link")

```
get_keys() -> []

```

Get all keys.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-redis/llama_index/storage/chat_store/redis/base.py`  
| 
```
140
141
142
```
 | 
```
defget_keys(self) -> List[str]:
"""Get all keys."""
    return [key.decode("utf-8") for key in self._redis_client.keys("*")]

```
 |  
| --- | --- |  
options: members: - RedisChatStore
