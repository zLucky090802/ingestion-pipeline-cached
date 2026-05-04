# Gel
##  GelChatStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/gel/#llama_index.storage.chat_store.gel.GelChatStore "Permanent link")
Bases: 
Chat store implementation using Gel database.
Stores and retrieves chat messages using Gel as the backend storage.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-gel/llama_index/storage/chat_store/gel/base.py`  
| 
```
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
```
 | 
```
classGelChatStore(BaseChatStore):
"""
    Chat store implementation using Gel database.

    Stores and retrieves chat messages using Gel as the backend storage.
    """

    record_type: str
    _sync_client: Optional[gel.Client] = PrivateAttr()
    _async_client: Optional[gel.AsyncIOClient] = PrivateAttr()

    def__init__(
        self,
        record_type: str = "Record",
    ):
"""
        Initialize GelChatStore.

        Args:
            record_type: The name of the record type in Gel schema.

        """
        super().__init__(record_type=record_type)

        self._sync_client = None
        self._async_client = None

    defget_sync_client(self):
"""Get or initialize a synchronous Gel client."""
        if self._async_client is not None:
            raise RuntimeError(
                "GelChatStore has already been used in async mode. "
                "If you were intentionally trying to use different IO modes at the same time, "
                "please create a new instance instead."
            )
        if self._sync_client is None:
            self._sync_client = gel.create_client()

            try:
                self._sync_client.ensure_connected()
            except gel.errors.ClientConnectionError as e:
                _logger.error(NO_PROJECT_MESSAGE)
                raise

            try:
                self._sync_client.query(f"select {self.record_type};")
            except gel.errors.InvalidReferenceError as e:
                _logger.error(
                    Template(MISSING_RECORD_TYPE_TEMPLATE).render(
                        record_type=self.record_type
                    )
                )
                raise

        return self._sync_client

    async defget_async_client(self):
"""Get or initialize an asynchronous Gel client."""
        if self._sync_client is not None:
            raise RuntimeError(
                "GelChatStore has already been used in sync mode. "
                "If you were intentionally trying to use different IO modes at the same time, "
                "please create a new instance instead."
            )
        if self._async_client is None:
            self._async_client = gel.create_async_client()

            try:
                await self._async_client.ensure_connected()
            except gel.errors.ClientConnectionError as e:
                _logger.error(NO_PROJECT_MESSAGE)
                raise

            try:
                await self._async_client.query(f"select {self.record_type};")
            except gel.errors.InvalidReferenceError as e:
                _logger.error(
                    Template(MISSING_RECORD_TYPE_TEMPLATE).render(
                        record_type=self.record_type
                    )
                )
                raise

        return self._async_client

    defset_messages(self, key: str, messages: list[ChatMessage]) -> None:
"""Set messages for a key."""
        client = self.get_sync_client()
        client.query(
            SET_MESSAGES_QUERY,
            key=key,
            value=[message.model_dump_json() for message in messages],
        )

    async defaset_messages(self, key: str, messages: list[ChatMessage]) -> None:
"""Async version of Get messages for a key."""
        client = await self.get_async_client()
        await client.query(
            SET_MESSAGES_QUERY,
            key=key,
            value=[message.model_dump_json() for message in messages],
        )

    defget_messages(self, key: str) -> list[ChatMessage]:
"""Get messages for a key."""
        client = self.get_sync_client()
        result = client.query_single(GET_MESSAGES_QUERY, key=key) or []
        return [ChatMessage.model_validate_json(message) for message in result]

    async defaget_messages(self, key: str) -> list[ChatMessage]:
"""Async version of Get messages for a key."""
        client = await self.get_async_client()
        result = await client.query_single(GET_MESSAGES_QUERY, key=key) or []
        return [ChatMessage.model_validate_json(message) for message in result]

    defadd_message(self, key: str, message: ChatMessage) -> None:
"""Add a message for a key."""
        client = self.get_sync_client()
        client.query(ADD_MESSAGE_QUERY, key=key, value=[message.model_dump_json()])

    async defasync_add_message(self, key: str, message: ChatMessage) -> None:
"""Async version of Add a message for a key."""
        client = await self.get_async_client()
        await client.query(
            ADD_MESSAGE_QUERY, key=key, value=[message.model_dump_json()]
        )

    defdelete_messages(self, key: str) -> Optional[list[ChatMessage]]:
"""Delete messages for a key."""
        client = self.get_sync_client()
        client.query(DELETE_MESSAGES_QUERY, key=key)

    async defadelete_messages(self, key: str) -> Optional[list[ChatMessage]]:
"""Async version of Delete messages for a key."""
        client = await self.get_async_client()
        await client.query(DELETE_MESSAGES_QUERY, key=key)

    defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
        client = self.get_sync_client()
        result = client.query_single(DELETE_MESSAGE_QUERY, key=key, idx=idx)
        return ChatMessage.model_validate_json(result) if result else None

    async defadelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Async version of Delete specific message for a key."""
        client = await self.get_async_client()
        result = await client.query_single(DELETE_MESSAGE_QUERY, key=key, idx=idx)
        return ChatMessage.model_validate_json(result) if result else None

    defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete last message for a key."""
        client = self.get_sync_client()
        result = client.query_single(DELETE_LAST_MESSAGE_QUERY, key=key)
        return ChatMessage.model_validate_json(result) if result else None

    async defadelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Async version of Delete last message for a key."""
        client = await self.get_async_client()
        result = await client.query_single(DELETE_LAST_MESSAGE_QUERY, key=key)
        return ChatMessage.model_validate_json(result) if result else None

    defget_keys(self) -> list[str]:
"""Get all keys."""
        client = self.get_sync_client()
        return client.query(GET_KEYS_QUERY)

    async defaget_keys(self) -> list[str]:
"""Async version of Get all keys."""
        client = await self.get_async_client()
        return await client.query(GET_KEYS_QUERY)

```
 |  
| --- | --- |  
###  get_sync_client [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/gel/#llama_index.storage.chat_store.gel.GelChatStore.get_sync_client "Permanent link")

```
get_sync_client()

```

Get or initialize a synchronous Gel client.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-gel/llama_index/storage/chat_store/gel/base.py`  
| 
```
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
```
 | 
```
defget_sync_client(self):
"""Get or initialize a synchronous Gel client."""
    if self._async_client is not None:
        raise RuntimeError(
            "GelChatStore has already been used in async mode. "
            "If you were intentionally trying to use different IO modes at the same time, "
            "please create a new instance instead."
        )
    if self._sync_client is None:
        self._sync_client = gel.create_client()

        try:
            self._sync_client.ensure_connected()
        except gel.errors.ClientConnectionError as e:
            _logger.error(NO_PROJECT_MESSAGE)
            raise

        try:
            self._sync_client.query(f"select {self.record_type};")
        except gel.errors.InvalidReferenceError as e:
            _logger.error(
                Template(MISSING_RECORD_TYPE_TEMPLATE).render(
                    record_type=self.record_type
                )
            )
            raise

    return self._sync_client

```
 |  
| --- | --- |  
###  get_async_client [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/gel/#llama_index.storage.chat_store.gel.GelChatStore.get_async_client "Permanent link")

```
get_async_client()

```

Get or initialize an asynchronous Gel client.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-gel/llama_index/storage/chat_store/gel/base.py`  
| 
```
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
```
 | 
```
async defget_async_client(self):
"""Get or initialize an asynchronous Gel client."""
    if self._sync_client is not None:
        raise RuntimeError(
            "GelChatStore has already been used in sync mode. "
            "If you were intentionally trying to use different IO modes at the same time, "
            "please create a new instance instead."
        )
    if self._async_client is None:
        self._async_client = gel.create_async_client()

        try:
            await self._async_client.ensure_connected()
        except gel.errors.ClientConnectionError as e:
            _logger.error(NO_PROJECT_MESSAGE)
            raise

        try:
            await self._async_client.query(f"select {self.record_type};")
        except gel.errors.InvalidReferenceError as e:
            _logger.error(
                Template(MISSING_RECORD_TYPE_TEMPLATE).render(
                    record_type=self.record_type
                )
            )
            raise

    return self._async_client

```
 |  
| --- | --- |  
###  set_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/gel/#llama_index.storage.chat_store.gel.GelChatStore.set_messages "Permanent link")

```
set_messages(key: , messages: []) -> None

```

Set messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-gel/llama_index/storage/chat_store/gel/base.py`  
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
```
 | 
```
defset_messages(self, key: str, messages: list[ChatMessage]) -> None:
"""Set messages for a key."""
    client = self.get_sync_client()
    client.query(
        SET_MESSAGES_QUERY,
        key=key,
        value=[message.model_dump_json() for message in messages],
    )

```
 |  
| --- | --- |  
###  aset_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/gel/#llama_index.storage.chat_store.gel.GelChatStore.aset_messages "Permanent link")

```
aset_messages(
    key: , messages: []
) -> None

```

Async version of Get messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-gel/llama_index/storage/chat_store/gel/base.py`  
| 
```
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
async defaset_messages(self, key: str, messages: list[ChatMessage]) -> None:
"""Async version of Get messages for a key."""
    client = await self.get_async_client()
    await client.query(
        SET_MESSAGES_QUERY,
        key=key,
        value=[message.model_dump_json() for message in messages],
    )

```
 |  
| --- | --- |  
###  get_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/gel/#llama_index.storage.chat_store.gel.GelChatStore.get_messages "Permanent link")

```
get_messages(key: ) -> []

```

Get messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-gel/llama_index/storage/chat_store/gel/base.py`  
| 
```
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
    client = self.get_sync_client()
    result = client.query_single(GET_MESSAGES_QUERY, key=key) or []
    return [ChatMessage.model_validate_json(message) for message in result]

```
 |  
| --- | --- |  
###  aget_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/gel/#llama_index.storage.chat_store.gel.GelChatStore.aget_messages "Permanent link")

```
aget_messages(key: ) -> []

```

Async version of Get messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-gel/llama_index/storage/chat_store/gel/base.py`  
| 
```
246
247
248
249
250
```
 | 
```
async defaget_messages(self, key: str) -> list[ChatMessage]:
"""Async version of Get messages for a key."""
    client = await self.get_async_client()
    result = await client.query_single(GET_MESSAGES_QUERY, key=key) or []
    return [ChatMessage.model_validate_json(message) for message in result]

```
 |  
| --- | --- |  
###  add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/gel/#llama_index.storage.chat_store.gel.GelChatStore.add_message "Permanent link")

```
add_message(key: , message: ) -> None

```

Add a message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-gel/llama_index/storage/chat_store/gel/base.py`  
| 
```
252
253
254
255
```
 | 
```
defadd_message(self, key: str, message: ChatMessage) -> None:
"""Add a message for a key."""
    client = self.get_sync_client()
    client.query(ADD_MESSAGE_QUERY, key=key, value=[message.model_dump_json()])

```
 |  
| --- | --- |  
###  async_add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/gel/#llama_index.storage.chat_store.gel.GelChatStore.async_add_message "Permanent link")

```
async_add_message(key: , message: ) -> None

```

Async version of Add a message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-gel/llama_index/storage/chat_store/gel/base.py`  
| 
```
257
258
259
260
261
262
```
 | 
```
async defasync_add_message(self, key: str, message: ChatMessage) -> None:
"""Async version of Add a message for a key."""
    client = await self.get_async_client()
    await client.query(
        ADD_MESSAGE_QUERY, key=key, value=[message.model_dump_json()]
    )

```
 |  
| --- | --- |  
###  delete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/gel/#llama_index.storage.chat_store.gel.GelChatStore.delete_messages "Permanent link")

```
delete_messages(key: ) -> Optional[[]]

```

Delete messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-gel/llama_index/storage/chat_store/gel/base.py`  
| 
```
264
265
266
267
```
 | 
```
defdelete_messages(self, key: str) -> Optional[list[ChatMessage]]:
"""Delete messages for a key."""
    client = self.get_sync_client()
    client.query(DELETE_MESSAGES_QUERY, key=key)

```
 |  
| --- | --- |  
###  adelete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/gel/#llama_index.storage.chat_store.gel.GelChatStore.adelete_messages "Permanent link")

```
adelete_messages(key: ) -> Optional[[]]

```

Async version of Delete messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-gel/llama_index/storage/chat_store/gel/base.py`  
| 
```
269
270
271
272
```
 | 
```
async defadelete_messages(self, key: str) -> Optional[list[ChatMessage]]:
"""Async version of Delete messages for a key."""
    client = await self.get_async_client()
    await client.query(DELETE_MESSAGES_QUERY, key=key)

```
 |  
| --- | --- |  
###  delete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/gel/#llama_index.storage.chat_store.gel.GelChatStore.delete_message "Permanent link")

```
delete_message(key: , idx: ) -> Optional[]

```

Delete specific message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-gel/llama_index/storage/chat_store/gel/base.py`  
| 
```
274
275
276
277
278
```
 | 
```
defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
    client = self.get_sync_client()
    result = client.query_single(DELETE_MESSAGE_QUERY, key=key, idx=idx)
    return ChatMessage.model_validate_json(result) if result else None

```
 |  
| --- | --- |  
###  adelete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/gel/#llama_index.storage.chat_store.gel.GelChatStore.adelete_message "Permanent link")

```
adelete_message(
    key: , idx: 
) -> Optional[]

```

Async version of Delete specific message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-gel/llama_index/storage/chat_store/gel/base.py`  
| 
```
280
281
282
283
284
```
 | 
```
async defadelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Async version of Delete specific message for a key."""
    client = await self.get_async_client()
    result = await client.query_single(DELETE_MESSAGE_QUERY, key=key, idx=idx)
    return ChatMessage.model_validate_json(result) if result else None

```
 |  
| --- | --- |  
###  delete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/gel/#llama_index.storage.chat_store.gel.GelChatStore.delete_last_message "Permanent link")

```
delete_last_message(key: ) -> Optional[]

```

Delete last message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-gel/llama_index/storage/chat_store/gel/base.py`  
| 
```
286
287
288
289
290
```
 | 
```
defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete last message for a key."""
    client = self.get_sync_client()
    result = client.query_single(DELETE_LAST_MESSAGE_QUERY, key=key)
    return ChatMessage.model_validate_json(result) if result else None

```
 |  
| --- | --- |  
###  adelete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/gel/#llama_index.storage.chat_store.gel.GelChatStore.adelete_last_message "Permanent link")

```
adelete_last_message(key: ) -> Optional[]

```

Async version of Delete last message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-gel/llama_index/storage/chat_store/gel/base.py`  
| 
```
292
293
294
295
296
```
 | 
```
async defadelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Async version of Delete last message for a key."""
    client = await self.get_async_client()
    result = await client.query_single(DELETE_LAST_MESSAGE_QUERY, key=key)
    return ChatMessage.model_validate_json(result) if result else None

```
 |  
| --- | --- |  
###  get_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/gel/#llama_index.storage.chat_store.gel.GelChatStore.get_keys "Permanent link")

```
get_keys() -> []

```

Get all keys.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-gel/llama_index/storage/chat_store/gel/base.py`  
| 
```
298
299
300
301
```
 | 
```
defget_keys(self) -> list[str]:
"""Get all keys."""
    client = self.get_sync_client()
    return client.query(GET_KEYS_QUERY)

```
 |  
| --- | --- |  
###  aget_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/gel/#llama_index.storage.chat_store.gel.GelChatStore.aget_keys "Permanent link")

```
aget_keys() -> []

```

Async version of Get all keys.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-gel/llama_index/storage/chat_store/gel/base.py`  
| 
```
303
304
305
306
```
 | 
```
async defaget_keys(self) -> list[str]:
"""Async version of Get all keys."""
    client = await self.get_async_client()
    return await client.query(GET_KEYS_QUERY)

```
 |  
| --- | --- |  
options: members: - GelChatStore
