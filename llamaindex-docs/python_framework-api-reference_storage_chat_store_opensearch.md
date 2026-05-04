# Opensearch
##  OpensearchChatStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/opensearch/#llama_index.storage.chat_store.opensearch.OpensearchChatStore "Permanent link")
Bases: 
OpenSearch chat store.
Stores chat messages as individual documents in an OpenSearch index, keyed by session_id with an integer index for ordering.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `opensearch_url`  |  OpenSearch endpoint URL.  |  `'https://localhost:9200'`  |  
|  `index`  |  Name of the OpenSearch index to store messages in.  |  `DEFAULT_INDEX_NAME`  |  
|  `os_client`  |  `Optional[Any]`  |  Optional pre-configured OpenSearch client.  |  `None`  |  
|  `os_async_client`  |  `Optional[Any]`  |  Optional pre-configured async OpenSearch client.  |  `None`  |  
|  `**kwargs`  |  Additional arguments passed to the OpenSearch client.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-opensearch/llama_index/storage/chat_store/opensearch/base.py`  
| 
```
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
classOpensearchChatStore(BaseChatStore):
"""
    OpenSearch chat store.

    Stores chat messages as individual documents in an OpenSearch index,
    keyed by session_id with an integer index for ordering.

    Args:
        opensearch_url: OpenSearch endpoint URL.
        index: Name of the OpenSearch index to store messages in.
        os_client: Optional pre-configured OpenSearch client.
        os_async_client: Optional pre-configured async OpenSearch client.
        **kwargs: Additional arguments passed to the OpenSearch client.

    """

    opensearch_url: str = Field(
        default="https://localhost:9200",
        description="OpenSearch URL.",
    )
    index: str = Field(
        default=DEFAULT_INDEX_NAME,
        description="OpenSearch index name for chat messages.",
    )

    _os_client: Any = PrivateAttr()
    _os_async_client: Any = PrivateAttr()

    def__init__(
        self,
        opensearch_url: str = "https://localhost:9200",
        index: str = DEFAULT_INDEX_NAME,
        os_client: Optional[Any] = None,
        os_async_client: Optional[Any] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize OpensearchChatStore."""
        super().__init__(opensearch_url=opensearch_url, index=index)

        self._os_client = os_client or OpenSearch(opensearch_url, **kwargs)
        self._os_async_client = os_async_client or AsyncOpenSearch(
            opensearch_url, **kwargs
        )

        self._ensure_index_exists()

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "OpensearchChatStore"

    def_ensure_index_exists(self) -> None:
"""Create the index if it does not already exist."""
        if not self._os_client.indices.exists(index=self.index):
            self._os_client.indices.create(index=self.index, body=CHAT_STORE_MAPPING)

    async def_aensure_index_exists(self) -> None:
"""Async: create the index if it does not already exist."""
        exists = await self._os_async_client.indices.exists(index=self.index)
        if not exists:
            await self._os_async_client.indices.create(
                index=self.index, body=CHAT_STORE_MAPPING
            )

    # ---- helpers ----

    def_search(self, query: Dict[str, Any], size: int = 10000) -> List[Dict]:
"""Run a search and return the list of hits."""
        resp = self._os_client.search(index=self.index, body=query, size=size)
        return resp["hits"]["hits"]

    async def_asearch(self, query: Dict[str, Any], size: int = 10000) -> List[Dict]:
"""Async: run a search and return the list of hits."""
        resp = await self._os_async_client.search(
            index=self.index, body=query, size=size
        )
        return resp["hits"]["hits"]

    def_delete_by_query(self, query: Dict[str, Any]) -> None:
"""Delete documents matching a query."""
        self._os_client.delete_by_query(
            index=self.index,
            body=query,
            refresh=True,
        )

    async def_adelete_by_query(self, query: Dict[str, Any]) -> None:
"""Async: delete documents matching a query."""
        await self._os_async_client.delete_by_query(
            index=self.index,
            body=query,
            refresh=True,
        )

    def_session_query(self, key: str) -> Dict[str, Any]:
"""Build a query to match all documents for a session."""
        return {"query": {"term": {"session_id": key}}}

    def_session_sorted_query(self, key: str, order: str = "asc") -> Dict[str, Any]:
"""Build a query for a session, sorted by index."""
        return {
            "query": {"term": {"session_id": key}},
            "sort": [{"index": {"order": order}}],
        }

    def_find_by_index_query(self, key: str, idx: int) -> Dict[str, Any]:
"""Build a query to match a single document by session + index."""
        return {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"session_id": key}},
                        {"term": {"index": idx}},
                    ]
                }
            }
        }

    def_shift_query(self, key: str, from_idx: int) -> Dict[str, Any]:
"""Build a query to find documents at or after a given index (desc)."""
        return {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"session_id": key}},
                        {"range": {"index": {"gte": from_idx}}},
                    ]
                }
            },
            "sort": [{"index": {"order": "desc"}}],
        }

    def_get_next_index(self, key: str) -> int:
"""Get the next available index for a session."""
        hits = self._search(self._session_sorted_query(key, order="desc"), size=1)
        if not hits:
            return 0
        return int(hits[0]["_source"]["index"]) + 1

    async def_aget_next_index(self, key: str) -> int:
"""Async: get the next available index for a session."""
        hits = await self._asearch(
            self._session_sorted_query(key, order="desc"), size=1
        )
        if not hits:
            return 0
        return int(hits[0]["_source"]["index"]) + 1

    def_index_doc(self, key: str, idx: int, message: ChatMessage) -> None:
"""Index a single message document."""
        self._os_client.index(
            index=self.index,
            body={
                "session_id": key,
                "index": idx,
                "message": _message_to_str(message),
            },
            refresh=True,
        )

    async def_aindex_doc(self, key: str, idx: int, message: ChatMessage) -> None:
"""Async: index a single message document."""
        await self._os_async_client.index(
            index=self.index,
            body={
                "session_id": key,
                "index": idx,
                "message": _message_to_str(message),
            },
            refresh=True,
        )

    def_reindex_session(self, key: str) -> None:
"""Re-number all documents in a session so indices are contiguous."""
        hits = self._search(self._session_sorted_query(key))
        # Delete all existing documents for this session
        self._delete_by_query(self._session_query(key))
        # Re-insert with corrected indices
        for new_idx, hit in enumerate(hits):
            msg = _str_to_message(hit["_source"]["message"])
            self._index_doc(key, new_idx, msg)

    async def_areindex_session(self, key: str) -> None:
"""Async: re-number all documents in a session so indices are contiguous."""
        hits = await self._asearch(self._session_sorted_query(key))
        # Delete all existing documents for this session
        await self._adelete_by_query(self._session_query(key))
        # Re-insert with corrected indices
        for new_idx, hit in enumerate(hits):
            msg = _str_to_message(hit["_source"]["message"])
            await self._aindex_doc(key, new_idx, msg)

    # ---- BaseChatStore interface ----

    defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Set messages for a key, replacing any existing messages."""
        # Delete existing messages for this session
        self._delete_by_query(self._session_query(key))

        # Insert new messages
        for idx, message in enumerate(messages):
            self._index_doc(key, idx, message)

    async defaset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Async: set messages for a key, replacing any existing messages."""
        await self._adelete_by_query(self._session_query(key))

        for idx, message in enumerate(messages):
            await self._aindex_doc(key, idx, message)

    defget_messages(self, key: str) -> List[ChatMessage]:
"""Get messages for a key, ordered by index."""
        hits = self._search(self._session_sorted_query(key))
        return [_str_to_message(hit["_source"]["message"]) for hit in hits]

    async defaget_messages(self, key: str) -> List[ChatMessage]:
"""Async: get messages for a key, ordered by index."""
        hits = await self._asearch(self._session_sorted_query(key))
        return [_str_to_message(hit["_source"]["message"]) for hit in hits]

    defadd_message(
        self, key: str, message: ChatMessage, idx: Optional[int] = None
    ) -> None:
"""
        Add a message for a key.

        If idx is None, appends to the end. Otherwise inserts at the given
        position and shifts subsequent messages.
        """
        if idx is None:
            idx = self._get_next_index(key)
            self._index_doc(key, idx, message)
        else:
            # Shift existing messages at >= idx up by one (reverse to avoid collisions)
            for hit in self._search(self._shift_query(key, idx)):
                self._os_client.update(
                    index=self.index,
                    id=hit["_id"],
                    body={"doc": {"index": hit["_source"]["index"] + 1}},
                    refresh=True,
                )
            self._index_doc(key, idx, message)

    async defasync_add_message(
        self, key: str, message: ChatMessage, idx: Optional[int] = None
    ) -> None:
"""Async: add a message for a key."""
        if idx is None:
            idx = await self._aget_next_index(key)
            await self._aindex_doc(key, idx, message)
        else:
            for hit in await self._asearch(self._shift_query(key, idx)):
                await self._os_async_client.update(
                    index=self.index,
                    id=hit["_id"],
                    body={"doc": {"index": hit["_source"]["index"] + 1}},
                    refresh=True,
                )
            await self._aindex_doc(key, idx, message)

    defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Delete all messages for a key. Returns the deleted messages."""
        messages = self.get_messages(key)
        self._delete_by_query(self._session_query(key))
        return messages if messages else None

    async defadelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Async: delete all messages for a key."""
        messages = await self.aget_messages(key)
        await self._adelete_by_query(self._session_query(key))
        return messages if messages else None

    defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""
        Delete a specific message by index for a key.

        After deletion, remaining messages are re-indexed to stay contiguous.
        """
        hits = self._search(self._find_by_index_query(key, idx), size=1)
        if not hits:
            return None

        deleted_message = _str_to_message(hits[0]["_source"]["message"])
        self._os_client.delete(index=self.index, id=hits[0]["_id"], refresh=True)
        self._reindex_session(key)
        return deleted_message

    async defadelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Async: delete a specific message by index for a key."""
        hits = await self._asearch(self._find_by_index_query(key, idx), size=1)
        if not hits:
            return None

        deleted_message = _str_to_message(hits[0]["_source"]["message"])
        await self._os_async_client.delete(
            index=self.index, id=hits[0]["_id"], refresh=True
        )
        await self._areindex_session(key)
        return deleted_message

    defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete the last message for a key."""
        hits = self._search(self._session_sorted_query(key, order="desc"), size=1)
        if not hits:
            return None

        last_message = _str_to_message(hits[0]["_source"]["message"])
        self._os_client.delete(index=self.index, id=hits[0]["_id"], refresh=True)
        return last_message

    async defadelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Async: delete the last message for a key."""
        hits = await self._asearch(
            self._session_sorted_query(key, order="desc"), size=1
        )
        if not hits:
            return None

        last_message = _str_to_message(hits[0]["_source"]["message"])
        await self._os_async_client.delete(
            index=self.index, id=hits[0]["_id"], refresh=True
        )
        return last_message

    defget_keys(self) -> List[str]:
"""Get all unique session keys."""
        query = {
            "size": 0,
            "aggs": {
                "unique_sessions": {"terms": {"field": "session_id", "size": 10000}}
            },
        }
        resp = self._os_client.search(index=self.index, body=query)
        buckets = resp["aggregations"]["unique_sessions"]["buckets"]
        return [bucket["key"] for bucket in buckets]

    async defaget_keys(self) -> List[str]:
"""Async: get all unique session keys."""
        query = {
            "size": 0,
            "aggs": {
                "unique_sessions": {"terms": {"field": "session_id", "size": 10000}}
            },
        }
        resp = await self._os_async_client.search(index=self.index, body=query)
        buckets = resp["aggregations"]["unique_sessions"]["buckets"]
        return [bucket["key"] for bucket in buckets]

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/opensearch/#llama_index.storage.chat_store.opensearch.OpensearchChatStore.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-opensearch/llama_index/storage/chat_store/opensearch/base.py`  
| 
```
80
81
82
83
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "OpensearchChatStore"

```
 |  
| --- | --- |  
###  set_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/opensearch/#llama_index.storage.chat_store.opensearch.OpensearchChatStore.set_messages "Permanent link")

```
set_messages(key: , messages: []) -> None

```

Set messages for a key, replacing any existing messages.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-opensearch/llama_index/storage/chat_store/opensearch/base.py`  
| 
```
228
229
230
231
232
233
234
235
```
 | 
```
defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Set messages for a key, replacing any existing messages."""
    # Delete existing messages for this session
    self._delete_by_query(self._session_query(key))

    # Insert new messages
    for idx, message in enumerate(messages):
        self._index_doc(key, idx, message)

```
 |  
| --- | --- |  
###  aset_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/opensearch/#llama_index.storage.chat_store.opensearch.OpensearchChatStore.aset_messages "Permanent link")

```
aset_messages(
    key: , messages: []
) -> None

```

Async: set messages for a key, replacing any existing messages.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-opensearch/llama_index/storage/chat_store/opensearch/base.py`  
| 
```
237
238
239
240
241
242
```
 | 
```
async defaset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Async: set messages for a key, replacing any existing messages."""
    await self._adelete_by_query(self._session_query(key))

    for idx, message in enumerate(messages):
        await self._aindex_doc(key, idx, message)

```
 |  
| --- | --- |  
###  get_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/opensearch/#llama_index.storage.chat_store.opensearch.OpensearchChatStore.get_messages "Permanent link")

```
get_messages(key: ) -> []

```

Get messages for a key, ordered by index.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-opensearch/llama_index/storage/chat_store/opensearch/base.py`  
| 
```
244
245
246
247
```
 | 
```
defget_messages(self, key: str) -> List[ChatMessage]:
"""Get messages for a key, ordered by index."""
    hits = self._search(self._session_sorted_query(key))
    return [_str_to_message(hit["_source"]["message"]) for hit in hits]

```
 |  
| --- | --- |  
###  aget_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/opensearch/#llama_index.storage.chat_store.opensearch.OpensearchChatStore.aget_messages "Permanent link")

```
aget_messages(key: ) -> []

```

Async: get messages for a key, ordered by index.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-opensearch/llama_index/storage/chat_store/opensearch/base.py`  
| 
```
249
250
251
252
```
 | 
```
async defaget_messages(self, key: str) -> List[ChatMessage]:
"""Async: get messages for a key, ordered by index."""
    hits = await self._asearch(self._session_sorted_query(key))
    return [_str_to_message(hit["_source"]["message"]) for hit in hits]

```
 |  
| --- | --- |  
###  add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/opensearch/#llama_index.storage.chat_store.opensearch.OpensearchChatStore.add_message "Permanent link")

```
add_message(
    key: ,
    message: ,
    idx: Optional[] = None,
) -> None

```

Add a message for a key.
If idx is None, appends to the end. Otherwise inserts at the given position and shifts subsequent messages.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-opensearch/llama_index/storage/chat_store/opensearch/base.py`  
| 
```
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
```
 | 
```
defadd_message(
    self, key: str, message: ChatMessage, idx: Optional[int] = None
) -> None:
"""
    Add a message for a key.

    If idx is None, appends to the end. Otherwise inserts at the given
    position and shifts subsequent messages.
    """
    if idx is None:
        idx = self._get_next_index(key)
        self._index_doc(key, idx, message)
    else:
        # Shift existing messages at >= idx up by one (reverse to avoid collisions)
        for hit in self._search(self._shift_query(key, idx)):
            self._os_client.update(
                index=self.index,
                id=hit["_id"],
                body={"doc": {"index": hit["_source"]["index"] + 1}},
                refresh=True,
            )
        self._index_doc(key, idx, message)

```
 |  
| --- | --- |  
###  async_add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/opensearch/#llama_index.storage.chat_store.opensearch.OpensearchChatStore.async_add_message "Permanent link")

```
async_add_message(
    key: ,
    message: ,
    idx: Optional[] = None,
) -> None

```

Async: add a message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-opensearch/llama_index/storage/chat_store/opensearch/base.py`  
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
285
286
287
288
289
290
291
292
```
 | 
```
async defasync_add_message(
    self, key: str, message: ChatMessage, idx: Optional[int] = None
) -> None:
"""Async: add a message for a key."""
    if idx is None:
        idx = await self._aget_next_index(key)
        await self._aindex_doc(key, idx, message)
    else:
        for hit in await self._asearch(self._shift_query(key, idx)):
            await self._os_async_client.update(
                index=self.index,
                id=hit["_id"],
                body={"doc": {"index": hit["_source"]["index"] + 1}},
                refresh=True,
            )
        await self._aindex_doc(key, idx, message)

```
 |  
| --- | --- |  
###  delete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/opensearch/#llama_index.storage.chat_store.opensearch.OpensearchChatStore.delete_messages "Permanent link")

```
delete_messages(key: ) -> Optional[[]]

```

Delete all messages for a key. Returns the deleted messages.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-opensearch/llama_index/storage/chat_store/opensearch/base.py`  
| 
```
294
295
296
297
298
```
 | 
```
defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Delete all messages for a key. Returns the deleted messages."""
    messages = self.get_messages(key)
    self._delete_by_query(self._session_query(key))
    return messages if messages else None

```
 |  
| --- | --- |  
###  adelete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/opensearch/#llama_index.storage.chat_store.opensearch.OpensearchChatStore.adelete_messages "Permanent link")

```
adelete_messages(key: ) -> Optional[[]]

```

Async: delete all messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-opensearch/llama_index/storage/chat_store/opensearch/base.py`  
| 
```
300
301
302
303
304
```
 | 
```
async defadelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Async: delete all messages for a key."""
    messages = await self.aget_messages(key)
    await self._adelete_by_query(self._session_query(key))
    return messages if messages else None

```
 |  
| --- | --- |  
###  delete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/opensearch/#llama_index.storage.chat_store.opensearch.OpensearchChatStore.delete_message "Permanent link")

```
delete_message(key: , idx: ) -> Optional[]

```

Delete a specific message by index for a key.
After deletion, remaining messages are re-indexed to stay contiguous.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-opensearch/llama_index/storage/chat_store/opensearch/base.py`  
| 
```
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
```
 | 
```
defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""
    Delete a specific message by index for a key.

    After deletion, remaining messages are re-indexed to stay contiguous.
    """
    hits = self._search(self._find_by_index_query(key, idx), size=1)
    if not hits:
        return None

    deleted_message = _str_to_message(hits[0]["_source"]["message"])
    self._os_client.delete(index=self.index, id=hits[0]["_id"], refresh=True)
    self._reindex_session(key)
    return deleted_message

```
 |  
| --- | --- |  
###  adelete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/opensearch/#llama_index.storage.chat_store.opensearch.OpensearchChatStore.adelete_message "Permanent link")

```
adelete_message(
    key: , idx: 
) -> Optional[]

```

Async: delete a specific message by index for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-opensearch/llama_index/storage/chat_store/opensearch/base.py`  
| 
```
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
```
 | 
```
async defadelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Async: delete a specific message by index for a key."""
    hits = await self._asearch(self._find_by_index_query(key, idx), size=1)
    if not hits:
        return None

    deleted_message = _str_to_message(hits[0]["_source"]["message"])
    await self._os_async_client.delete(
        index=self.index, id=hits[0]["_id"], refresh=True
    )
    await self._areindex_session(key)
    return deleted_message

```
 |  
| --- | --- |  
###  delete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/opensearch/#llama_index.storage.chat_store.opensearch.OpensearchChatStore.delete_last_message "Permanent link")

```
delete_last_message(key: ) -> Optional[]

```

Delete the last message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-opensearch/llama_index/storage/chat_store/opensearch/base.py`  
| 
```
334
335
336
337
338
339
340
341
342
```
 | 
```
defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete the last message for a key."""
    hits = self._search(self._session_sorted_query(key, order="desc"), size=1)
    if not hits:
        return None

    last_message = _str_to_message(hits[0]["_source"]["message"])
    self._os_client.delete(index=self.index, id=hits[0]["_id"], refresh=True)
    return last_message

```
 |  
| --- | --- |  
###  adelete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/opensearch/#llama_index.storage.chat_store.opensearch.OpensearchChatStore.adelete_last_message "Permanent link")

```
adelete_last_message(key: ) -> Optional[]

```

Async: delete the last message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-opensearch/llama_index/storage/chat_store/opensearch/base.py`  
| 
```
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
"""Async: delete the last message for a key."""
    hits = await self._asearch(
        self._session_sorted_query(key, order="desc"), size=1
    )
    if not hits:
        return None

    last_message = _str_to_message(hits[0]["_source"]["message"])
    await self._os_async_client.delete(
        index=self.index, id=hits[0]["_id"], refresh=True
    )
    return last_message

```
 |  
| --- | --- |  
###  get_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/opensearch/#llama_index.storage.chat_store.opensearch.OpensearchChatStore.get_keys "Permanent link")

```
get_keys() -> []

```

Get all unique session keys.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-opensearch/llama_index/storage/chat_store/opensearch/base.py`  
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
368
```
 | 
```
defget_keys(self) -> List[str]:
"""Get all unique session keys."""
    query = {
        "size": 0,
        "aggs": {
            "unique_sessions": {"terms": {"field": "session_id", "size": 10000}}
        },
    }
    resp = self._os_client.search(index=self.index, body=query)
    buckets = resp["aggregations"]["unique_sessions"]["buckets"]
    return [bucket["key"] for bucket in buckets]

```
 |  
| --- | --- |  
###  aget_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/opensearch/#llama_index.storage.chat_store.opensearch.OpensearchChatStore.aget_keys "Permanent link")

```
aget_keys() -> []

```

Async: get all unique session keys.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-opensearch/llama_index/storage/chat_store/opensearch/base.py`  
| 
```
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
async defaget_keys(self) -> List[str]:
"""Async: get all unique session keys."""
    query = {
        "size": 0,
        "aggs": {
            "unique_sessions": {"terms": {"field": "session_id", "size": 10000}}
        },
    }
    resp = await self._os_async_client.search(index=self.index, body=query)
    buckets = resp["aggregations"]["unique_sessions"]["buckets"]
    return [bucket["key"] for bucket in buckets]

```
 |  
| --- | --- |  
options: members: - OpensearchChatStore
