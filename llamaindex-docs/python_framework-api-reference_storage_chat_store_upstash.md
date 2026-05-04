# Upstash
##  UpstashChatStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/upstash/#llama_index.storage.chat_store.upstash.UpstashChatStore "Permanent link")
Bases: 
Upstash chat store for storing and retrieving chat messages using Redis.
This class implements the BaseChatStore interface and provides methods for managing chat messages in an Upstash Redis database.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-upstash/llama_index/storage/chat_store/upstash/base.py`  
| 
```
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
```
 | 
```
classUpstashChatStore(BaseChatStore):
"""
    Upstash chat store for storing and retrieving chat messages using Redis.

    This class implements the BaseChatStore interface and provides methods
    for managing chat messages in an Upstash Redis database.
    """

    _sync_redis_client: SyncRedis = PrivateAttr()
    _async_redis_client: AsyncRedis = PrivateAttr()

    ttl: Optional[int] = Field(default=None, description="Time to live in seconds.")

    classConfig:
        arbitrary_types_allowed = True

    def__init__(
        self,
        redis_url: str = "",
        redis_token: str = "",
        ttl: Optional[int] = None,
    ):
"""
        Initialize the UpstashChatStore.

        Args:
            redis_url (str): The URL of the Upstash Redis instance.
            redis_token (str): The authentication token for the Upstash Redis instance.
            ttl (Optional[int]): Time to live in seconds for stored messages.

        Raises:
            ValueError: If redis_url or redis_token is empty.

        """
        if redis_url == "" or redis_token == "":
            raise ValueError("Please provide a valid URL and token")
        super().__init__(ttl=ttl)
        try:
            self._sync_redis_client = SyncRedis(url=redis_url, token=redis_token)
            self._async_redis_client = AsyncRedis(url=redis_url, token=redis_token)
        except Exception as error:
            logger.error(f"Upstash Redis client could not be initiated: {error}")

        # self.ttl = ttl

    @classmethod
    defclass_name(cls) -> str:
"""
        Get the class name.

        Returns:
            str: The name of the class.

        """
        return "UpstashChatStore"

    defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""
        Set messages for a key.

        Args:
            key (str): The key to store the messages under.
            messages (List[ChatMessage]): The list of messages to store.

        """
        self._sync_redis_client.delete(key)
        for message in messages:
            self.add_message(key, message)

        if self.ttl:
            self._sync_redis_client.expire(key, self.ttl)

    async defasync_set_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""
        Set messages for a key.

        Args:
            key (str): The key to store the messages under.
            messages (List[ChatMessage]): The list of messages to store.

        """
        await self._async_redis_client.delete(key)
        for message in messages:
            await self.async_add_message(key, message)

        if self.ttl:
            await self._async_redis_client.expire(key, self.ttl)

    defget_messages(self, key: str) -> List[ChatMessage]:
"""
        Get messages for a key.

        Args:
            key (str): The key to retrieve messages from.

        Returns:
            List[ChatMessage]: The list of retrieved messages.

        """
        items = self._sync_redis_client.lrange(key, 0, -1)
        if len(items) == 0:
            return []

        return [ChatMessage.parse_raw(item) for item in items]

    async defasync_get_messages(self, key: str) -> List[ChatMessage]:
"""
        Get messages for a key.

        Args:
            key (str): The key to retrieve messages from.

        Returns:
            List[ChatMessage]: The list of retrieved messages.

        """
        items = await self._async_redis_client.lrange(key, 0, -1)
        if len(items) == 0:
            return []

        return [ChatMessage.parse_raw(item) for item in items]

    defadd_message(
        self, key: str, message: ChatMessage, idx: Optional[int] = None
    ) -> None:
"""
        Add a message to a key.

        Args:
            key (str): The key to add the message to.
            message (ChatMessage): The message to add.
            idx (Optional[int]): The index at which to insert the message.

        """
        if idx is None:
            message_json = json.dumps(_message_to_dict(message))
            self._sync_redis_client.rpush(key, message_json)
        else:
            self._insert_element_at_index(key, message, idx)

        if self.ttl:
            self._sync_redis_client.expire(key, self.ttl)

    async defasync_add_message(
        self, key: str, message: ChatMessage, idx: Optional[int] = None
    ) -> None:
"""
        Add a message to a key.

        Args:
            key (str): The key to add the message to.
            message (ChatMessage): The message to add.
            idx (Optional[int]): The index at which to insert the message.

        """
        if idx is None:
            message_json = json.dumps(_message_to_dict(message))
            await self._async_redis_client.rpush(key, message_json)
        else:
            await self._async_insert_element_at_index(key, message, idx)

        if self.ttl:
            await self._async_redis_client.expire(key, self.ttl)

    defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""
        Delete messages for a key.

        Args:
            key (str): The key to delete messages from.

        Returns:
            Optional[List[ChatMessage]]: Always returns None in this implementation.

        """
        self._sync_redis_client.delete(key)
        return None

    async defasync_delete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""
        Delete messages for a key.

        Args:
            key (str): The key to delete messages from.

        Returns:
            Optional[List[ChatMessage]]: Always returns None in this implementation.

        """
        await self._async_redis_client.delete(key)
        return None

    defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""
        Delete a message from a key.

        Args:
            key (str): The key to delete the message from.
            idx (int): The index of the message to delete.

        Returns:
            Optional[ChatMessage]: The deleted message, or None if not found or an error occurred.

        """
        try:
            deleted_message = self._sync_redis_client.lindex(key, idx)
            if deleted_message is None:
                return None

            placeholder = f"{key}:{idx}:deleted"

            self._sync_redis_client.lset(key, idx, placeholder)
            self._sync_redis_client.lrem(key, 1, placeholder)
            if self.ttl:
                self._sync_redis_client.expire(key, self.ttl)

            return deleted_message

        except Exception as e:
            logger.error(f"Error deleting message at index {idx} from {key}: {e}")
            return None

    async defasync_delete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""
        Delete a message from a key.

        Args:
            key (str): The key to delete the message from.
            idx (int): The index of the message to delete.

        Returns:
            Optional[ChatMessage]: The deleted message, or None if not found or an error occurred.

        """
        try:
            deleted_message = await self._async_redis_client.lindex(key, idx)
            if deleted_message is None:
                return None

            placeholder = f"{key}:{idx}:deleted"

            await self._async_redis_client.lset(key, idx, placeholder)
            await self._async_redis_client.lrem(key, 1, placeholder)
            if self.ttl:
                await self._async_redis_client.expire(key, self.ttl)

            return deleted_message

        except Exception as e:
            logger.error(f"Error deleting message at index {idx} from {key}: {e}")
            return None

    defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""
        Delete the last message from a key.

        Args:
            key (str): The key to delete the last message from.

        Returns:
            Optional[ChatMessage]: The deleted message, or None if the list is empty.

        """
        deleted_message = self._sync_redis_client.rpop(key)
        return ChatMessage.parse_raw(deleted_message) if deleted_message else None

    async defasync_delete_last_message(self, key: str) -> Optional[ChatMessage]:
"""
        Delete the last message from a key.

        Args:
            key (str): The key to delete the last message from.

        Returns:
            Optional[ChatMessage]: The deleted message, or None if the list is empty.

        """
        deleted_message = await self._async_redis_client.rpop(key)
        if deleted_message:
            return ChatMessage.parse_raw(deleted_message)
        return None

    defget_keys(self) -> List[str]:
"""
        Get all keys.

        Returns:
            List[str]: A list of all keys in the Redis store.

        """
        keys = self._sync_redis_client.keys("*")
        return keys if isinstance(keys, list) else [keys]

    async defasync_get_keys(self) -> List[str]:
"""
        Get all keys.

        Returns:
            List[str]: A list of all keys in the Redis store.

        """
        keys = await self._async_redis_client.keys("*")
        return keys if isinstance(keys, list) else [keys]

    def_insert_element_at_index(
        self, key: str, message: ChatMessage, idx: int
    ) -> List[ChatMessage]:
"""
        Insert a message at a specific index.

        Args:
            key (str): The key of the list to insert into.
            message (ChatMessage): The message to insert.
            idx (int): The index at which to insert the message.

        Returns:
            List[ChatMessage]: The updated list of messages.

        """
        current_list = self.get_messages(key)
        current_list.insert(idx, message)

        self._sync_redis_client.delete(key)

        self.set_messages(key, current_list)

        return current_list

    async def_async_insert_element_at_index(
        self, key: str, message: ChatMessage, idx: int
    ) -> List[ChatMessage]:
"""
        Insert a message at a specific index.

        Args:
            key (str): The key of the list to insert into.
            message (ChatMessage): The message to insert.
            idx (int): The index at which to insert the message.

        Returns:
            List[ChatMessage]: The updated list of messages.

        """
        current_list = await self.async_get_messages(key)
        current_list.insert(idx, message)

        await self.async_delete_messages(key)

        await self.async_set_messages(key, current_list)

        return current_list

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/upstash/#llama_index.storage.chat_store.upstash.UpstashChatStore.class_name "Permanent link")

```
class_name() -> 

```

Get the class name.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The name of the class.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-upstash/llama_index/storage/chat_store/upstash/base.py`  
| 
```
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
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""
    Get the class name.

    Returns:
        str: The name of the class.

    """
    return "UpstashChatStore"

```
 |  
| --- | --- |  
###  set_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/upstash/#llama_index.storage.chat_store.upstash.UpstashChatStore.set_messages "Permanent link")

```
set_messages(key: , messages: []) -> None

```

Set messages for a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key to store the messages under.  |  _required_  |  
|  `messages`  |  `List[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.llms.ChatMessage\)")]`  |  The list of messages to store.  |  _required_  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-upstash/llama_index/storage/chat_store/upstash/base.py`  
| 
```
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
```
 | 
```
defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""
    Set messages for a key.

    Args:
        key (str): The key to store the messages under.
        messages (List[ChatMessage]): The list of messages to store.

    """
    self._sync_redis_client.delete(key)
    for message in messages:
        self.add_message(key, message)

    if self.ttl:
        self._sync_redis_client.expire(key, self.ttl)

```
 |  
| --- | --- |  
###  async_set_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/upstash/#llama_index.storage.chat_store.upstash.UpstashChatStore.async_set_messages "Permanent link")

```
async_set_messages(
    key: , messages: []
) -> None

```

Set messages for a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key to store the messages under.  |  _required_  |  
|  `messages`  |  `List[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.llms.ChatMessage\)")]`  |  The list of messages to store.  |  _required_  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-upstash/llama_index/storage/chat_store/upstash/base.py`  
| 
```
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
```
 | 
```
async defasync_set_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""
    Set messages for a key.

    Args:
        key (str): The key to store the messages under.
        messages (List[ChatMessage]): The list of messages to store.

    """
    await self._async_redis_client.delete(key)
    for message in messages:
        await self.async_add_message(key, message)

    if self.ttl:
        await self._async_redis_client.expire(key, self.ttl)

```
 |  
| --- | --- |  
###  get_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/upstash/#llama_index.storage.chat_store.upstash.UpstashChatStore.get_messages "Permanent link")

```
get_messages(key: ) -> []

```

Get messages for a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key to retrieve messages from.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.llms.ChatMessage\)")]`  |  List[ChatMessage]: The list of retrieved messages.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-upstash/llama_index/storage/chat_store/upstash/base.py`  
| 
```
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
```
 | 
```
defget_messages(self, key: str) -> List[ChatMessage]:
"""
    Get messages for a key.

    Args:
        key (str): The key to retrieve messages from.

    Returns:
        List[ChatMessage]: The list of retrieved messages.

    """
    items = self._sync_redis_client.lrange(key, 0, -1)
    if len(items) == 0:
        return []

    return [ChatMessage.parse_raw(item) for item in items]

```
 |  
| --- | --- |  
###  async_get_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/upstash/#llama_index.storage.chat_store.upstash.UpstashChatStore.async_get_messages "Permanent link")

```
async_get_messages(key: ) -> []

```

Get messages for a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key to retrieve messages from.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.llms.ChatMessage\)")]`  |  List[ChatMessage]: The list of retrieved messages.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-upstash/llama_index/storage/chat_store/upstash/base.py`  
| 
```
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
```
 | 
```
async defasync_get_messages(self, key: str) -> List[ChatMessage]:
"""
    Get messages for a key.

    Args:
        key (str): The key to retrieve messages from.

    Returns:
        List[ChatMessage]: The list of retrieved messages.

    """
    items = await self._async_redis_client.lrange(key, 0, -1)
    if len(items) == 0:
        return []

    return [ChatMessage.parse_raw(item) for item in items]

```
 |  
| --- | --- |  
###  add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/upstash/#llama_index.storage.chat_store.upstash.UpstashChatStore.add_message "Permanent link")

```
add_message(
    key: ,
    message: ,
    idx: Optional[] = None,
) -> None

```

Add a message to a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key to add the message to.  |  _required_  |  
|  `message`  |   |  The message to add.  |  _required_  |  
|  `idx`  |  `Optional[int]`  |  The index at which to insert the message.  |  `None`  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-upstash/llama_index/storage/chat_store/upstash/base.py`  
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
168
169
170
171
```
 | 
```
defadd_message(
    self, key: str, message: ChatMessage, idx: Optional[int] = None
) -> None:
"""
    Add a message to a key.

    Args:
        key (str): The key to add the message to.
        message (ChatMessage): The message to add.
        idx (Optional[int]): The index at which to insert the message.

    """
    if idx is None:
        message_json = json.dumps(_message_to_dict(message))
        self._sync_redis_client.rpush(key, message_json)
    else:
        self._insert_element_at_index(key, message, idx)

    if self.ttl:
        self._sync_redis_client.expire(key, self.ttl)

```
 |  
| --- | --- |  
###  async_add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/upstash/#llama_index.storage.chat_store.upstash.UpstashChatStore.async_add_message "Permanent link")

```
async_add_message(
    key: ,
    message: ,
    idx: Optional[] = None,
) -> None

```

Add a message to a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key to add the message to.  |  _required_  |  
|  `message`  |   |  The message to add.  |  _required_  |  
|  `idx`  |  `Optional[int]`  |  The index at which to insert the message.  |  `None`  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-upstash/llama_index/storage/chat_store/upstash/base.py`  
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
```
 | 
```
async defasync_add_message(
    self, key: str, message: ChatMessage, idx: Optional[int] = None
) -> None:
"""
    Add a message to a key.

    Args:
        key (str): The key to add the message to.
        message (ChatMessage): The message to add.
        idx (Optional[int]): The index at which to insert the message.

    """
    if idx is None:
        message_json = json.dumps(_message_to_dict(message))
        await self._async_redis_client.rpush(key, message_json)
    else:
        await self._async_insert_element_at_index(key, message, idx)

    if self.ttl:
        await self._async_redis_client.expire(key, self.ttl)

```
 |  
| --- | --- |  
###  delete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/upstash/#llama_index.storage.chat_store.upstash.UpstashChatStore.delete_messages "Permanent link")

```
delete_messages(key: ) -> Optional[[]]

```

Delete messages for a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key to delete messages from.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Optional[List[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.llms.ChatMessage\)")]]`  |  Optional[List[ChatMessage]]: Always returns None in this implementation.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-upstash/llama_index/storage/chat_store/upstash/base.py`  
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
```
 | 
```
defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""
    Delete messages for a key.

    Args:
        key (str): The key to delete messages from.

    Returns:
        Optional[List[ChatMessage]]: Always returns None in this implementation.

    """
    self._sync_redis_client.delete(key)
    return None

```
 |  
| --- | --- |  
###  async_delete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/upstash/#llama_index.storage.chat_store.upstash.UpstashChatStore.async_delete_messages "Permanent link")

```
async_delete_messages(
    key: ,
) -> Optional[[]]

```

Delete messages for a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key to delete messages from.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Optional[List[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.llms.ChatMessage\)")]]`  |  Optional[List[ChatMessage]]: Always returns None in this implementation.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-upstash/llama_index/storage/chat_store/upstash/base.py`  
| 
```
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
```
 | 
```
async defasync_delete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""
    Delete messages for a key.

    Args:
        key (str): The key to delete messages from.

    Returns:
        Optional[List[ChatMessage]]: Always returns None in this implementation.

    """
    await self._async_redis_client.delete(key)
    return None

```
 |  
| --- | --- |  
###  delete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/upstash/#llama_index.storage.chat_store.upstash.UpstashChatStore.delete_message "Permanent link")

```
delete_message(key: , idx: ) -> Optional[]

```

Delete a message from a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key to delete the message from.  |  _required_  |  
|  `idx`  |  The index of the message to delete.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Optional[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.llms.ChatMessage\)")]`  |  Optional[ChatMessage]: The deleted message, or None if not found or an error occurred.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-upstash/llama_index/storage/chat_store/upstash/base.py`  
| 
```
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
```
 | 
```
defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""
    Delete a message from a key.

    Args:
        key (str): The key to delete the message from.
        idx (int): The index of the message to delete.

    Returns:
        Optional[ChatMessage]: The deleted message, or None if not found or an error occurred.

    """
    try:
        deleted_message = self._sync_redis_client.lindex(key, idx)
        if deleted_message is None:
            return None

        placeholder = f"{key}:{idx}:deleted"

        self._sync_redis_client.lset(key, idx, placeholder)
        self._sync_redis_client.lrem(key, 1, placeholder)
        if self.ttl:
            self._sync_redis_client.expire(key, self.ttl)

        return deleted_message

    except Exception as e:
        logger.error(f"Error deleting message at index {idx} from {key}: {e}")
        return None

```
 |  
| --- | --- |  
###  async_delete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/upstash/#llama_index.storage.chat_store.upstash.UpstashChatStore.async_delete_message "Permanent link")

```
async_delete_message(
    key: , idx: 
) -> Optional[]

```

Delete a message from a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key to delete the message from.  |  _required_  |  
|  `idx`  |  The index of the message to delete.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Optional[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.llms.ChatMessage\)")]`  |  Optional[ChatMessage]: The deleted message, or None if not found or an error occurred.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-upstash/llama_index/storage/chat_store/upstash/base.py`  
| 
```
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
```
 | 
```
async defasync_delete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""
    Delete a message from a key.

    Args:
        key (str): The key to delete the message from.
        idx (int): The index of the message to delete.

    Returns:
        Optional[ChatMessage]: The deleted message, or None if not found or an error occurred.

    """
    try:
        deleted_message = await self._async_redis_client.lindex(key, idx)
        if deleted_message is None:
            return None

        placeholder = f"{key}:{idx}:deleted"

        await self._async_redis_client.lset(key, idx, placeholder)
        await self._async_redis_client.lrem(key, 1, placeholder)
        if self.ttl:
            await self._async_redis_client.expire(key, self.ttl)

        return deleted_message

    except Exception as e:
        logger.error(f"Error deleting message at index {idx} from {key}: {e}")
        return None

```
 |  
| --- | --- |  
###  delete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/upstash/#llama_index.storage.chat_store.upstash.UpstashChatStore.delete_last_message "Permanent link")

```
delete_last_message(key: ) -> Optional[]

```

Delete the last message from a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key to delete the last message from.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Optional[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.llms.ChatMessage\)")]`  |  Optional[ChatMessage]: The deleted message, or None if the list is empty.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-upstash/llama_index/storage/chat_store/upstash/base.py`  
| 
```
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
```
 | 
```
defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""
    Delete the last message from a key.

    Args:
        key (str): The key to delete the last message from.

    Returns:
        Optional[ChatMessage]: The deleted message, or None if the list is empty.

    """
    deleted_message = self._sync_redis_client.rpop(key)
    return ChatMessage.parse_raw(deleted_message) if deleted_message else None

```
 |  
| --- | --- |  
###  async_delete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/upstash/#llama_index.storage.chat_store.upstash.UpstashChatStore.async_delete_last_message "Permanent link")

```
async_delete_last_message(
    key: ,
) -> Optional[]

```

Delete the last message from a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key to delete the last message from.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Optional[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.llms.ChatMessage\)")]`  |  Optional[ChatMessage]: The deleted message, or None if the list is empty.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-upstash/llama_index/storage/chat_store/upstash/base.py`  
| 
```
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
```
 | 
```
async defasync_delete_last_message(self, key: str) -> Optional[ChatMessage]:
"""
    Delete the last message from a key.

    Args:
        key (str): The key to delete the last message from.

    Returns:
        Optional[ChatMessage]: The deleted message, or None if the list is empty.

    """
    deleted_message = await self._async_redis_client.rpop(key)
    if deleted_message:
        return ChatMessage.parse_raw(deleted_message)
    return None

```
 |  
| --- | --- |  
###  get_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/upstash/#llama_index.storage.chat_store.upstash.UpstashChatStore.get_keys "Permanent link")

```
get_keys() -> []

```

Get all keys.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: A list of all keys in the Redis store.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-upstash/llama_index/storage/chat_store/upstash/base.py`  
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
```
 | 
```
defget_keys(self) -> List[str]:
"""
    Get all keys.

    Returns:
        List[str]: A list of all keys in the Redis store.

    """
    keys = self._sync_redis_client.keys("*")
    return keys if isinstance(keys, list) else [keys]

```
 |  
| --- | --- |  
###  async_get_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/upstash/#llama_index.storage.chat_store.upstash.UpstashChatStore.async_get_keys "Permanent link")

```
async_get_keys() -> []

```

Get all keys.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: A list of all keys in the Redis store.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-upstash/llama_index/storage/chat_store/upstash/base.py`  
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
```
 | 
```
async defasync_get_keys(self) -> List[str]:
"""
    Get all keys.

    Returns:
        List[str]: A list of all keys in the Redis store.

    """
    keys = await self._async_redis_client.keys("*")
    return keys if isinstance(keys, list) else [keys]

```
 |  
| --- | --- |  
options: members: - UpstashChatStore
