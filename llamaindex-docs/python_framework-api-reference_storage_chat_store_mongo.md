# Mongo
##  MongoChatStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/mongo/#llama_index.storage.chat_store.mongo.MongoChatStore "Permanent link")
Bases: 
MongoDB chat store implementation.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-mongo/llama_index/storage/chat_store/mongo/base.py`  
| 
```
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
```
 | 
```
classMongoChatStore(BaseChatStore):
"""MongoDB chat store implementation."""

    mongo_uri: str = Field(
        default="mongodb://localhost:27017", description="MongoDB URI."
    )
    db_name: str = Field(default="default", description="MongoDB database name.")
    collection_name: str = Field(
        default="sessions", description="MongoDB collection name."
    )
    ttl_seconds: Optional[int] = Field(
        default=None, description="Time to live in seconds."
    )
    _mongo_client: Optional[MongoClient] = PrivateAttr()
    _async_client: Optional[AsyncMongoClient] = PrivateAttr()

    def__init__(
        self,
        mongo_uri: str = "mongodb://localhost:27017",
        db_name: str = "default",
        collection_name: str = "sessions",
        mongo_client: Optional[MongoClient] = None,
        amongo_client: Optional[AsyncMongoClient] = None,
        ttl_seconds: Optional[int] = None,
        collection: Optional[Collection] = None,
        async_collection: Optional[AsyncCollection] = None,
        **kwargs: Any,
    ) -> None:
"""
        Initialize the MongoDB chat store.

        Args:
            mongo_uri: MongoDB connection URI
            db_name: Database name
            collection_name: Collection name for storing chat messages
            mongo_client: Optional pre-configured MongoDB client
            amongo_client: Optional pre-configured async MongoDB client
            ttl_seconds: Optional time-to-live for messages in seconds
            **kwargs: Additional arguments to pass to MongoDB client

        """
        super().__init__(ttl=ttl_seconds)

        self._mongo_client = mongo_client or MongoClient(mongo_uri, **kwargs)
        self._async_client = amongo_client or AsyncMongoClient(mongo_uri, **kwargs)

        # append_metadata was added in PyMongo 4.14.0, but is a valid database name on earlier versions
        if callable(self._mongo_client.append_metadata):
            self._mongo_client.append_metadata(
                DriverInfo(name="llama-index", version=version("llama-index"))
            )
        if callable(self._async_client.append_metadata):
            self._async_client.append_metadata(
                DriverInfo(name="llama-index", version=version("llama-index"))
            )

        if collection:
            self._collection = collection
        else:
            self._collection = self._mongo_client[db_name][collection_name]

        if async_collection:
            self._async_collection = async_collection
        else:
            self._async_collection = self._async_client[db_name][collection_name]

        # Create TTL index if ttl is specified
        if ttl_seconds:
            self._collection.create_index("created_at", expireAfterSeconds=ttl_seconds)

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "MongoChatStore"

    defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""
        Set messages for a key.

        Args:
            key: Key to set messages for
            messages: List of ChatMessage objects

        """
        # Delete existing messages for this key
        self._collection.delete_many({"session_id": key})

        # Insert new messages
        if messages:
            current_time = datetime.now()
            message_dicts = [
                {
                    "session_id": key,
                    "index": i,
                    "message": _message_to_dict(msg),
                    "created_at": current_time,
                }
                for i, msg in enumerate(messages)
            ]
            self._collection.insert_many(message_dicts)

    async defaset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""
        Set messages for a key asynchronously.

        Args:
            key: Key to set messages for
            messages: List of ChatMessage objects

        """
        # Delete existing messages for this key
        await self._async_collection.delete_many({"session_id": key})

        # Insert new messages
        if messages:
            current_time = datetime.now()
            message_dicts = [
                {
                    "session_id": key,
                    "index": i,
                    "message": _message_to_dict(msg),
                    "created_at": current_time,
                }
                for i, msg in enumerate(messages)
            ]
            await self._async_collection.insert_many(message_dicts)

    defget_messages(self, key: str) -> List[ChatMessage]:
"""
        Get messages for a key.

        Args:
            key: Key to get messages for

        """
        # Find all messages for this key, sorted by index
        docs = list(self._collection.find({"session_id": key}, sort=[("index", 1)]))

        # Convert to ChatMessage objects
        return [_dict_to_message(doc["message"]) for doc in docs]

    async defaget_messages(self, key: str) -> List[ChatMessage]:
"""
        Get messages for a key asynchronously.

        Args:
            key: Key to get messages for

        """
        # Find all messages for this key, sorted by index
        cursor = self._async_collection.find({"session_id": key}).sort("index", 1)

        # Convert to list and then to ChatMessage objects
        docs = await cursor.to_list(length=None)
        return [_dict_to_message(doc["message"]) for doc in docs]

    defadd_message(
        self, key: str, message: ChatMessage, idx: Optional[int] = None
    ) -> None:
"""
        Add a message for a key.

        Args:
            key: Key to add message for
            message: ChatMessage object to add

        """
        if idx is None:
            # Get the current highest index
            highest_idx_doc = self._collection.find_one(
                {"session_id": key}, sort=[("index", -1)]
            )
            idx = 0 if highest_idx_doc is None else highest_idx_doc["index"] + 1

        # Insert the new message with current timestamp
        self._collection.insert_one(
            {
                "session_id": key,
                "index": idx,
                "message": _message_to_dict(message),
                "created_at": datetime.now(),
            }
        )

    async defasync_add_message(
        self, key: str, message: ChatMessage, idx: Optional[int] = None
    ) -> None:
"""
        Add a message for a key asynchronously.

        Args:
            key: Key to add message for
            message: ChatMessage object to add

        """
        if idx is None:
            # Get the current highest index
            highest_idx_doc = await self._async_collection.find_one(
                {"session_id": key}, sort=[("index", -1)]
            )
            idx = 0 if highest_idx_doc is None else highest_idx_doc["index"] + 1

        # Insert the new message with current timestamp
        await self._async_collection.insert_one(
            {
                "session_id": key,
                "index": idx,
                "message": _message_to_dict(message),
                "created_at": datetime.now(),
            }
        )

    defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""
        Delete messages for a key.

        Args:
            key: Key to delete messages for

        """
        # Get messages before deleting
        messages = self.get_messages(key)

        # Delete all messages for this key
        self._collection.delete_many({"session_id": key})

        return messages

    async defadelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""
        Delete messages for a key asynchronously.

        Args:
            key: Key to delete messages for

        """
        # Get messages before deleting
        messages = await self.aget_messages(key)

        # Delete all messages for this key
        await self._async_collection.delete_many({"session_id": key})

        return messages

    defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""
        Delete specific message for a key.

        Args:
            key: Key to delete message for
            idx: Index of message to delete

        """
        # Find the message to delete
        doc = self._collection.find_one({"session_id": key, "index": idx})
        if doc is None:
            return None

        # Delete the message
        self._collection.delete_one({"session_id": key, "index": idx})

        # Reindex remaining messages
        self._collection.update_many(
            {"session_id": key, "index": {"$gt": idx}}, {"$inc": {"index": -1}}
        )

        return _dict_to_message(doc["message"])

    async defadelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""
        Delete specific message for a key asynchronously.

        Args:
            key: Key to delete message for
            idx: Index of message to delete

        """
        # Find the message to delete
        doc = await self._async_collection.find_one({"session_id": key, "index": idx})
        if doc is None:
            return None

        # Delete the message
        await self._async_collection.delete_one({"session_id": key, "index": idx})

        # Reindex remaining messages
        await self._async_collection.update_many(
            {"session_id": key, "index": {"$gt": idx}}, {"$inc": {"index": -1}}
        )

        return _dict_to_message(doc["message"])

    defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""
        Delete last message for a key.

        Args:
            key: Key to delete last message for

        """
        # Find the last message
        last_msg_doc = self._collection.find_one(
            {"session_id": key}, sort=[("index", -1)]
        )

        if last_msg_doc is None:
            return None

        # Delete the last message
        self._collection.delete_one({"_id": last_msg_doc["_id"]})

        return _dict_to_message(last_msg_doc["message"])

    async defadelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""
        Delete last message for a key asynchronously.

        Args:
            key: Key to delete last message for

        """
        # Find the last message
        last_msg_doc = await self._async_collection.find_one(
            {"session_id": key}, sort=[("index", -1)]
        )

        if last_msg_doc is None:
            return None

        # Delete the last message
        await self._async_collection.delete_one({"_id": last_msg_doc["_id"]})

        return _dict_to_message(last_msg_doc["message"])

    defget_keys(self) -> List[str]:
"""
        Get all keys (session IDs).

        Returns:
            List of session IDs

        """
        # Get distinct session IDs
        return self._collection.distinct("session_id")

    async defaget_keys(self) -> List[str]:
"""
        Get all keys (session IDs) asynchronously.

        Returns:
            List of session IDs

        """
        # Get distinct session IDs
        return await self._async_collection.distinct("session_id")

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/mongo/#llama_index.storage.chat_store.mongo.MongoChatStore.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-mongo/llama_index/storage/chat_store/mongo/base.py`  
| 
```
94
95
96
97
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "MongoChatStore"

```
 |  
| --- | --- |  
###  set_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/mongo/#llama_index.storage.chat_store.mongo.MongoChatStore.set_messages "Permanent link")

```
set_messages(key: , messages: []) -> None

```

Set messages for a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  Key to set messages for  |  _required_  |  
|  `messages`  |  `List[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.llms.ChatMessage\)")]`  |  List of ChatMessage objects  |  _required_  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-mongo/llama_index/storage/chat_store/mongo/base.py`  
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
```
 | 
```
defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""
    Set messages for a key.

    Args:
        key: Key to set messages for
        messages: List of ChatMessage objects

    """
    # Delete existing messages for this key
    self._collection.delete_many({"session_id": key})

    # Insert new messages
    if messages:
        current_time = datetime.now()
        message_dicts = [
            {
                "session_id": key,
                "index": i,
                "message": _message_to_dict(msg),
                "created_at": current_time,
            }
            for i, msg in enumerate(messages)
        ]
        self._collection.insert_many(message_dicts)

```
 |  
| --- | --- |  
###  aset_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/mongo/#llama_index.storage.chat_store.mongo.MongoChatStore.aset_messages "Permanent link")

```
aset_messages(
    key: , messages: []
) -> None

```

Set messages for a key asynchronously.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  Key to set messages for  |  _required_  |  
|  `messages`  |  `List[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.llms.ChatMessage\)")]`  |  List of ChatMessage objects  |  _required_  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-mongo/llama_index/storage/chat_store/mongo/base.py`  
| 
```
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
```
 | 
```
async defaset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""
    Set messages for a key asynchronously.

    Args:
        key: Key to set messages for
        messages: List of ChatMessage objects

    """
    # Delete existing messages for this key
    await self._async_collection.delete_many({"session_id": key})

    # Insert new messages
    if messages:
        current_time = datetime.now()
        message_dicts = [
            {
                "session_id": key,
                "index": i,
                "message": _message_to_dict(msg),
                "created_at": current_time,
            }
            for i, msg in enumerate(messages)
        ]
        await self._async_collection.insert_many(message_dicts)

```
 |  
| --- | --- |  
###  get_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/mongo/#llama_index.storage.chat_store.mongo.MongoChatStore.get_messages "Permanent link")

```
get_messages(key: ) -> []

```

Get messages for a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  Key to get messages for  |  _required_  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-mongo/llama_index/storage/chat_store/mongo/base.py`  
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
```
 | 
```
defget_messages(self, key: str) -> List[ChatMessage]:
"""
    Get messages for a key.

    Args:
        key: Key to get messages for

    """
    # Find all messages for this key, sorted by index
    docs = list(self._collection.find({"session_id": key}, sort=[("index", 1)]))

    # Convert to ChatMessage objects
    return [_dict_to_message(doc["message"]) for doc in docs]

```
 |  
| --- | --- |  
###  aget_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/mongo/#llama_index.storage.chat_store.mongo.MongoChatStore.aget_messages "Permanent link")

```
aget_messages(key: ) -> []

```

Get messages for a key asynchronously.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  Key to get messages for  |  _required_  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-mongo/llama_index/storage/chat_store/mongo/base.py`  
| 
```
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
async defaget_messages(self, key: str) -> List[ChatMessage]:
"""
    Get messages for a key asynchronously.

    Args:
        key: Key to get messages for

    """
    # Find all messages for this key, sorted by index
    cursor = self._async_collection.find({"session_id": key}).sort("index", 1)

    # Convert to list and then to ChatMessage objects
    docs = await cursor.to_list(length=None)
    return [_dict_to_message(doc["message"]) for doc in docs]

```
 |  
| --- | --- |  
###  add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/mongo/#llama_index.storage.chat_store.mongo.MongoChatStore.add_message "Permanent link")

```
add_message(
    key: ,
    message: ,
    idx: Optional[] = None,
) -> None

```

Add a message for a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  Key to add message for  |  _required_  |  
|  `message`  |   |  ChatMessage object to add  |  _required_  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-mongo/llama_index/storage/chat_store/mongo/base.py`  
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
defadd_message(
    self, key: str, message: ChatMessage, idx: Optional[int] = None
) -> None:
"""
    Add a message for a key.

    Args:
        key: Key to add message for
        message: ChatMessage object to add

    """
    if idx is None:
        # Get the current highest index
        highest_idx_doc = self._collection.find_one(
            {"session_id": key}, sort=[("index", -1)]
        )
        idx = 0 if highest_idx_doc is None else highest_idx_doc["index"] + 1

    # Insert the new message with current timestamp
    self._collection.insert_one(
        {
            "session_id": key,
            "index": idx,
            "message": _message_to_dict(message),
            "created_at": datetime.now(),
        }
    )

```
 |  
| --- | --- |  
###  async_add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/mongo/#llama_index.storage.chat_store.mongo.MongoChatStore.async_add_message "Permanent link")

```
async_add_message(
    key: ,
    message: ,
    idx: Optional[] = None,
) -> None

```

Add a message for a key asynchronously.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  Key to add message for  |  _required_  |  
|  `message`  |   |  ChatMessage object to add  |  _required_  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-mongo/llama_index/storage/chat_store/mongo/base.py`  
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
```
 | 
```
async defasync_add_message(
    self, key: str, message: ChatMessage, idx: Optional[int] = None
) -> None:
"""
    Add a message for a key asynchronously.

    Args:
        key: Key to add message for
        message: ChatMessage object to add

    """
    if idx is None:
        # Get the current highest index
        highest_idx_doc = await self._async_collection.find_one(
            {"session_id": key}, sort=[("index", -1)]
        )
        idx = 0 if highest_idx_doc is None else highest_idx_doc["index"] + 1

    # Insert the new message with current timestamp
    await self._async_collection.insert_one(
        {
            "session_id": key,
            "index": idx,
            "message": _message_to_dict(message),
            "created_at": datetime.now(),
        }
    )

```
 |  
| --- | --- |  
###  delete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/mongo/#llama_index.storage.chat_store.mongo.MongoChatStore.delete_messages "Permanent link")

```
delete_messages(key: ) -> Optional[[]]

```

Delete messages for a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  Key to delete messages for  |  _required_  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-mongo/llama_index/storage/chat_store/mongo/base.py`  
| 
```
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
defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""
    Delete messages for a key.

    Args:
        key: Key to delete messages for

    """
    # Get messages before deleting
    messages = self.get_messages(key)

    # Delete all messages for this key
    self._collection.delete_many({"session_id": key})

    return messages

```
 |  
| --- | --- |  
###  adelete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/mongo/#llama_index.storage.chat_store.mongo.MongoChatStore.adelete_messages "Permanent link")

```
adelete_messages(key: ) -> Optional[[]]

```

Delete messages for a key asynchronously.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  Key to delete messages for  |  _required_  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-mongo/llama_index/storage/chat_store/mongo/base.py`  
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
```
 | 
```
async defadelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""
    Delete messages for a key asynchronously.

    Args:
        key: Key to delete messages for

    """
    # Get messages before deleting
    messages = await self.aget_messages(key)

    # Delete all messages for this key
    await self._async_collection.delete_many({"session_id": key})

    return messages

```
 |  
| --- | --- |  
###  delete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/mongo/#llama_index.storage.chat_store.mongo.MongoChatStore.delete_message "Permanent link")

```
delete_message(key: , idx: ) -> Optional[]

```

Delete specific message for a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  Key to delete message for  |  _required_  |  
|  `idx`  |  Index of message to delete  |  _required_  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-mongo/llama_index/storage/chat_store/mongo/base.py`  
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
defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""
    Delete specific message for a key.

    Args:
        key: Key to delete message for
        idx: Index of message to delete

    """
    # Find the message to delete
    doc = self._collection.find_one({"session_id": key, "index": idx})
    if doc is None:
        return None

    # Delete the message
    self._collection.delete_one({"session_id": key, "index": idx})

    # Reindex remaining messages
    self._collection.update_many(
        {"session_id": key, "index": {"$gt": idx}}, {"$inc": {"index": -1}}
    )

    return _dict_to_message(doc["message"])

```
 |  
| --- | --- |  
###  adelete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/mongo/#llama_index.storage.chat_store.mongo.MongoChatStore.adelete_message "Permanent link")

```
adelete_message(
    key: , idx: 
) -> Optional[]

```

Delete specific message for a key asynchronously.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  Key to delete message for  |  _required_  |  
|  `idx`  |  Index of message to delete  |  _required_  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-mongo/llama_index/storage/chat_store/mongo/base.py`  
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
307
308
309
310
311
312
313
314
```
 | 
```
async defadelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""
    Delete specific message for a key asynchronously.

    Args:
        key: Key to delete message for
        idx: Index of message to delete

    """
    # Find the message to delete
    doc = await self._async_collection.find_one({"session_id": key, "index": idx})
    if doc is None:
        return None

    # Delete the message
    await self._async_collection.delete_one({"session_id": key, "index": idx})

    # Reindex remaining messages
    await self._async_collection.update_many(
        {"session_id": key, "index": {"$gt": idx}}, {"$inc": {"index": -1}}
    )

    return _dict_to_message(doc["message"])

```
 |  
| --- | --- |  
###  delete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/mongo/#llama_index.storage.chat_store.mongo.MongoChatStore.delete_last_message "Permanent link")

```
delete_last_message(key: ) -> Optional[]

```

Delete last message for a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  Key to delete last message for  |  _required_  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-mongo/llama_index/storage/chat_store/mongo/base.py`  
| 
```
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
```
 | 
```
defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""
    Delete last message for a key.

    Args:
        key: Key to delete last message for

    """
    # Find the last message
    last_msg_doc = self._collection.find_one(
        {"session_id": key}, sort=[("index", -1)]
    )

    if last_msg_doc is None:
        return None

    # Delete the last message
    self._collection.delete_one({"_id": last_msg_doc["_id"]})

    return _dict_to_message(last_msg_doc["message"])

```
 |  
| --- | --- |  
###  adelete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/mongo/#llama_index.storage.chat_store.mongo.MongoChatStore.adelete_last_message "Permanent link")

```
adelete_last_message(key: ) -> Optional[]

```

Delete last message for a key asynchronously.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  Key to delete last message for  |  _required_  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-mongo/llama_index/storage/chat_store/mongo/base.py`  
| 
```
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
```
 | 
```
async defadelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""
    Delete last message for a key asynchronously.

    Args:
        key: Key to delete last message for

    """
    # Find the last message
    last_msg_doc = await self._async_collection.find_one(
        {"session_id": key}, sort=[("index", -1)]
    )

    if last_msg_doc is None:
        return None

    # Delete the last message
    await self._async_collection.delete_one({"_id": last_msg_doc["_id"]})

    return _dict_to_message(last_msg_doc["message"])

```
 |  
| --- | --- |  
###  get_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/mongo/#llama_index.storage.chat_store.mongo.MongoChatStore.get_keys "Permanent link")

```
get_keys() -> []

```

Get all keys (session IDs).
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List of session IDs  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-mongo/llama_index/storage/chat_store/mongo/base.py`  
| 
```
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
defget_keys(self) -> List[str]:
"""
    Get all keys (session IDs).

    Returns:
        List of session IDs

    """
    # Get distinct session IDs
    return self._collection.distinct("session_id")

```
 |  
| --- | --- |  
###  aget_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/mongo/#llama_index.storage.chat_store.mongo.MongoChatStore.aget_keys "Permanent link")

```
aget_keys() -> []

```

Get all keys (session IDs) asynchronously.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List of session IDs  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-mongo/llama_index/storage/chat_store/mongo/base.py`  
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
```
 | 
```
async defaget_keys(self) -> List[str]:
"""
    Get all keys (session IDs) asynchronously.

    Returns:
        List of session IDs

    """
    # Get distinct session IDs
    return await self._async_collection.distinct("session_id")

```
 |  
| --- | --- |  
options: members: - MongoChatStore
