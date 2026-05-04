# Azure
##  AzureChatStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore "Permanent link")
Bases: 
Azure chat store leveraging Azure Table Storage or Cosmos DB.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
| 
```
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
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
```
 | 
```
classAzureChatStore(BaseChatStore):
"""Azure chat store leveraging Azure Table Storage or Cosmos DB."""

    _table_service_client: TableServiceClient = PrivateAttr()
    _atable_service_client: AsyncTableServiceClient = PrivateAttr()

    chat_table_name: str = Field(default=DEFAULT_CHAT_TABLE)
    metadata_table_name: str = Field(default=DEFAULT_METADATA_TABLE)
    metadata_partition_key: str = Field(default=None)
    service_mode: ServiceMode = Field(default=ServiceMode.STORAGE)

    def__init__(
        self,
        table_service_client: TableServiceClient,
        atable_service_client: Optional[AsyncTableServiceClient] = None,
        chat_table_name: str = DEFAULT_CHAT_TABLE,
        metadata_table_name: str = DEFAULT_METADATA_TABLE,
        metadata_partition_key: str = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
    ):
        sanitized_chat_table_name = sanitize_table_name(chat_table_name)

        super().__init__(
            chat_table_name=sanitized_chat_table_name,
            metadata_table_name=sanitize_table_name(metadata_table_name),
            metadata_partition_key=(
                sanitized_chat_table_name
                if metadata_partition_key is None
                else metadata_partition_key
            ),
            service_mode=service_mode,
        )

        self._table_service_client = table_service_client
        self._atable_service_client = atable_service_client

    @classmethod
    deffrom_connection_string(
        cls,
        connection_string: str,
        chat_table_name: str = DEFAULT_CHAT_TABLE,
        metadata_table_name: str = DEFAULT_METADATA_TABLE,
        metadata_partition_key: str = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
    ):
"""Creates an instance of AzureChatStore using a connection string."""
        table_service_client = TableServiceClient.from_connection_string(
            connection_string
        )
        atable_service_client = AsyncTableServiceClient.from_connection_string(
            connection_string
        )

        return cls(
            table_service_client,
            atable_service_client,
            chat_table_name,
            metadata_table_name,
            metadata_partition_key,
            service_mode,
        )

    @classmethod
    deffrom_account_and_key(
        cls,
        account_name: str,
        account_key: str,
        endpoint: Optional[str] = None,
        chat_table_name: str = DEFAULT_CHAT_TABLE,
        metadata_table_name: str = DEFAULT_METADATA_TABLE,
        metadata_partition_key: str = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
    ) -> "AzureChatStore":
"""Initializes AzureChatStore from an account name and key."""
        if endpoint is None:
            endpoint = f"https://{account_name}.table.core.windows.net"
        credential = AzureNamedKeyCredential(account_name, account_key)
        return cls._from_clients(
            endpoint,
            credential,
            chat_table_name,
            metadata_table_name,
            metadata_partition_key,
            service_mode,
        )

    @classmethod
    deffrom_account_and_id(
        cls,
        account_name: str,
        endpoint: Optional[str] = None,
        chat_table_name: str = DEFAULT_CHAT_TABLE,
        metadata_table_name: str = DEFAULT_METADATA_TABLE,
        metadata_partition_key: str = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
    ) -> "AzureChatStore":
"""Initializes AzureChatStore from an account name and managed ID."""
        fromazure.identityimport DefaultAzureCredential

        if endpoint is None:
            endpoint = f"https://{account_name}.table.core.windows.net"
        credential = DefaultAzureCredential()
        return cls._from_clients(
            endpoint,
            credential,
            chat_table_name,
            metadata_table_name,
            metadata_partition_key,
            service_mode,
        )

    @classmethod
    deffrom_sas_token(
        cls,
        endpoint: str,
        sas_token: str,
        chat_table_name: str = DEFAULT_CHAT_TABLE,
        metadata_table_name: str = DEFAULT_METADATA_TABLE,
        metadata_partition_key: str = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
    ) -> "AzureChatStore":
"""Creates an AzureChatStore instance using a SAS token."""
        credential = AzureSasCredential(sas_token)
        return cls._from_clients(
            endpoint,
            credential,
            chat_table_name,
            metadata_table_name,
            metadata_partition_key,
            service_mode,
        )

    @classmethod
    deffrom_aad_token(
        cls,
        endpoint: str,
        chat_table_name: str = DEFAULT_CHAT_TABLE,
        metadata_table_name: str = DEFAULT_METADATA_TABLE,
        metadata_partition_key: str = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
    ) -> "AzureChatStore":
"""Creates an AzureChatStore using an Azure Active Directory token."""
        fromazure.identityimport DefaultAzureCredential

        credential = DefaultAzureCredential()
        return cls._from_clients(
            endpoint,
            credential,
            chat_table_name,
            metadata_table_name,
            metadata_partition_key,
            service_mode,
        )

    defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Set messages for a key."""
        asyncio_run(self.aset_messages(key, messages))

    async defaset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Asynchronoulsy set messages for a key."""
        # Delete existing messages and insert new messages in one transaction
        chat_client = await self._atable_service_client.create_table_if_not_exists(
            self.chat_table_name
        )
        entities = chat_client.query_entities(f"PartitionKey eq '{key}'")
        all_entities = []
        async for entity in entities:
            all_entities.append(entity)

        delete_operations = (
            (TransactionOperation.DELETE, entity) for entity in all_entities
        )
        create_operations = (
            (
                TransactionOperation.CREATE,
                serialize(
                    self.service_mode,
                    {
                        "PartitionKey": key,
                        "RowKey": self._to_row_key(idx),
                        **message.dict(),
                    },
                ),
            )
            for idx, message in enumerate(messages)
        )
        await chat_client.submit_transaction(
            chain(delete_operations, create_operations)
        )

        # Update metadata
        metadata_client = await self._atable_service_client.create_table_if_not_exists(
            self.metadata_table_name
        )
        messages_len = len(messages)
        await metadata_client.upsert_entity(
            {
                "PartitionKey": self.metadata_partition_key,
                "RowKey": key,
                "LastMessageRowKey": self._to_row_key(messages_len - 1),
                "MessageCount": messages_len,
            },
            UpdateMode.REPLACE,
        )

    defget_messages(self, key: str) -> List[ChatMessage]:
"""Get messages for a key."""
        return asyncio_run(self.aget_messages(key))

    async defaget_messages(self, key: str) -> List[ChatMessage]:
"""Asynchronously get messages for a key."""
        chat_client = await self._atable_service_client.create_table_if_not_exists(
            self.chat_table_name
        )
        entities = chat_client.query_entities(f"PartitionKey eq '{key}'")
        messages = []

        async for entity in entities:
            messages.append(
                ChatMessage.model_validate(deserialize(self.service_mode, entity))
            )

        return messages

    defadd_message(self, key: str, message: ChatMessage, idx: int = None):
"""Add a message for a key."""
        asyncio_run(self.async_add_message(key, message, idx))

    async defasync_add_message(self, key: str, message: ChatMessage, idx: int = None):
        metadata_client = await self._atable_service_client.create_table_if_not_exists(
            self.metadata_table_name
        )
        metadata = await self._get_or_default_metadata(metadata_client, key)
        next_index = int(metadata["MessageCount"])

        if idx is not None and idx  next_index:
            raise ValueError(f"Index out of bounds: {idx}")
        elif idx is None:
            idx = next_index

        # Insert the new message
        chat_client = await self._atable_service_client.create_table_if_not_exists(
            self.chat_table_name
        )
        await chat_client.create_entity(
            serialize(
                self.service_mode,
                {
                    "PartitionKey": key,
                    "RowKey": self._to_row_key(idx),
                    **message.dict(),
                },
            )
        )

        metadata["LastMessageRowKey"] = self._to_row_key(idx)
        metadata["MessageCount"] = next_index + 1
        # Update medatada
        await metadata_client.upsert_entity(metadata, UpdateMode.MERGE)

    defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
        # Delete all messages for the key
        return asyncio_run(self.adelete_messages(key))

    async defadelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Asynchronously delete all messages for a key."""
        chat_client = await self._atable_service_client.create_table_if_not_exists(
            self.chat_table_name
        )
        entities = chat_client.query_entities(f"PartitionKey eq '{key}'")
        all_entities = []
        async for entity in entities:
            all_entities.append(entity)

        await chat_client.submit_transaction(
            (TransactionOperation.DELETE, entity) for entity in all_entities
        )

        metadata_client = await self._atable_service_client.create_table_if_not_exists(
            self.metadata_table_name
        )
        await metadata_client.upsert_entity(
            self._get_default_metadata(key), UpdateMode.REPLACE
        )

    defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
        return asyncio_run(self.adelete_message(key, idx))

    async defadelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Asynchronously delete specific message for a key."""
        # Fetch metadata to get the message count
        metadata_client = await self._atable_service_client.create_table_if_not_exists(
            self.metadata_table_name
        )
        metadata = await metadata_client.get_entity(
            partition_key=self.metadata_partition_key, row_key=key
        )

        # Index out of bounds
        message_count = int(metadata["MessageCount"])
        if idx >= message_count:
            return None

        # Delete the message
        chat_client = await self._atable_service_client.create_table_if_not_exists(
            self.chat_table_name
        )
        await chat_client.delete_entity(
            partition_key=key, row_key=self._to_row_key(idx)
        )

        # Update metadata if last message was deleted
        if idx == message_count - 1:
            metadata["LastMessageRowKey"] = self._to_row_key(idx - 1)
            metadata["MessageCount"] = message_count - 1
            await metadata_client.upsert_entity(metadata, mode=UpdateMode.MERGE)

    defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete last message for a key."""
        return asyncio_run(self.adelete_last_message(key))

    async defadelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Async delete last message for a key."""
        metadata_client = await self._atable_service_client.create_table_if_not_exists(
            self.metadata_table_name
        )
        # Retrieve metadata to get the last message row key
        metadata = await metadata_client.get_entity(
            partition_key=self.metadata_partition_key, row_key=key
        )
        last_row_key = metadata["LastMessageRowKey"]

        chat_client = await self._atable_service_client.create_table_if_not_exists(
            self.chat_table_name
        )
        # Delete the last message
        await chat_client.delete_entity(partition_key=key, row_key=last_row_key)

        # Update metadata
        last_row_key_num = int(last_row_key)
        metadata["LastMessageRowKey"] = self._to_row_key(
            last_row_key_num - 1 if last_row_key_num  0 else 0
        )
        metadata["MessageCount"] = int(metadata["MessageCount"]) - 1
        await metadata_client.upsert_entity(metadata, UpdateMode.MERGE)

    defget_keys(self) -> List[str]:
"""Get all keys."""
        return asyncio_run(self.aget_keys())

    async defaget_keys(self) -> List[str]:
"""Asynchronously get all keys."""
        metadata_client = await self._atable_service_client.create_table_if_not_exists(
            self.metadata_table_name
        )
        entities = metadata_client.query_entities(
            f"PartitionKey eq '{self.metadata_partition_key}'"
        )

        keys = []
        async for entity in entities:
            keys.append(entity["RowKey"])

        return keys

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "AzureChatStore"

    @classmethod
    def_from_clients(
        cls,
        endpoint: str,
        credential: Any,
        chat_table_name: str = DEFAULT_CHAT_TABLE,
        metadata_table_name: str = DEFAULT_METADATA_TABLE,
        metadata_partition_key: str = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
    ) -> "AzureChatStore":
"""Create table service clients."""
        table_service_client = TableServiceClient(
            endpoint=endpoint, credential=credential
        )
        atable_service_client = AsyncTableServiceClient(
            endpoint=endpoint, credential=credential
        )

        return cls(
            table_service_client,
            atable_service_client,
            chat_table_name,
            metadata_table_name,
            metadata_partition_key,
            service_mode,
        )

    def_to_row_key(self, idx: int) -> str:
"""Generate a row key from an index."""
        return f"{idx:010}"

    def_get_default_metadata(self, key: str) -> dict:
"""Generate default metadata for a key."""
        return {
            "PartitionKey": self.metadata_partition_key,
            "RowKey": key,
            "LastMessageRowKey": self._to_row_key(0),
            "MessageCount": 0,
        }

    async def_get_or_default_metadata(
        self, metadata_client: AsyncTableClient, key: str
    ) -> dict:
"""
        Retrieve metadata if it exists, otherwise return default metadata
        structure.
        """
        try:
            return await metadata_client.get_entity(
                partition_key=self.metadata_partition_key, row_key=key
            )
        except ResourceNotFoundError:
            return self._get_default_metadata(key)

```
 |  
| --- | --- |  
###  from_connection_string `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.from_connection_string "Permanent link")

```
from_connection_string(
    connection_string: ,
    chat_table_name:  = DEFAULT_CHAT_TABLE,
    metadata_table_name:  = DEFAULT_METADATA_TABLE,
    metadata_partition_key:  = None,
    service_mode: ServiceMode = STORAGE,
)

```

Creates an instance of AzureChatStore using a connection string.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_connection_string(
    cls,
    connection_string: str,
    chat_table_name: str = DEFAULT_CHAT_TABLE,
    metadata_table_name: str = DEFAULT_METADATA_TABLE,
    metadata_partition_key: str = None,
    service_mode: ServiceMode = ServiceMode.STORAGE,
):
"""Creates an instance of AzureChatStore using a connection string."""
    table_service_client = TableServiceClient.from_connection_string(
        connection_string
    )
    atable_service_client = AsyncTableServiceClient.from_connection_string(
        connection_string
    )

    return cls(
        table_service_client,
        atable_service_client,
        chat_table_name,
        metadata_table_name,
        metadata_partition_key,
        service_mode,
    )

```
 |  
| --- | --- |  
###  from_account_and_key `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.from_account_and_key "Permanent link")

```
from_account_and_key(
    account_name: ,
    account_key: ,
    endpoint: Optional[] = None,
    chat_table_name:  = DEFAULT_CHAT_TABLE,
    metadata_table_name:  = DEFAULT_METADATA_TABLE,
    metadata_partition_key:  = None,
    service_mode: ServiceMode = STORAGE,
) -> 

```

Initializes AzureChatStore from an account name and key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_account_and_key(
    cls,
    account_name: str,
    account_key: str,
    endpoint: Optional[str] = None,
    chat_table_name: str = DEFAULT_CHAT_TABLE,
    metadata_table_name: str = DEFAULT_METADATA_TABLE,
    metadata_partition_key: str = None,
    service_mode: ServiceMode = ServiceMode.STORAGE,
) -> "AzureChatStore":
"""Initializes AzureChatStore from an account name and key."""
    if endpoint is None:
        endpoint = f"https://{account_name}.table.core.windows.net"
    credential = AzureNamedKeyCredential(account_name, account_key)
    return cls._from_clients(
        endpoint,
        credential,
        chat_table_name,
        metadata_table_name,
        metadata_partition_key,
        service_mode,
    )

```
 |  
| --- | --- |  
###  from_account_and_id `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.from_account_and_id "Permanent link")

```
from_account_and_id(
    account_name: ,
    endpoint: Optional[] = None,
    chat_table_name:  = DEFAULT_CHAT_TABLE,
    metadata_table_name:  = DEFAULT_METADATA_TABLE,
    metadata_partition_key:  = None,
    service_mode: ServiceMode = STORAGE,
) -> 

```

Initializes AzureChatStore from an account name and managed ID.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_account_and_id(
    cls,
    account_name: str,
    endpoint: Optional[str] = None,
    chat_table_name: str = DEFAULT_CHAT_TABLE,
    metadata_table_name: str = DEFAULT_METADATA_TABLE,
    metadata_partition_key: str = None,
    service_mode: ServiceMode = ServiceMode.STORAGE,
) -> "AzureChatStore":
"""Initializes AzureChatStore from an account name and managed ID."""
    fromazure.identityimport DefaultAzureCredential

    if endpoint is None:
        endpoint = f"https://{account_name}.table.core.windows.net"
    credential = DefaultAzureCredential()
    return cls._from_clients(
        endpoint,
        credential,
        chat_table_name,
        metadata_table_name,
        metadata_partition_key,
        service_mode,
    )

```
 |  
| --- | --- |  
###  from_sas_token `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.from_sas_token "Permanent link")

```
from_sas_token(
    endpoint: ,
    sas_token: ,
    chat_table_name:  = DEFAULT_CHAT_TABLE,
    metadata_table_name:  = DEFAULT_METADATA_TABLE,
    metadata_partition_key:  = None,
    service_mode: ServiceMode = STORAGE,
) -> 

```

Creates an AzureChatStore instance using a SAS token.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_sas_token(
    cls,
    endpoint: str,
    sas_token: str,
    chat_table_name: str = DEFAULT_CHAT_TABLE,
    metadata_table_name: str = DEFAULT_METADATA_TABLE,
    metadata_partition_key: str = None,
    service_mode: ServiceMode = ServiceMode.STORAGE,
) -> "AzureChatStore":
"""Creates an AzureChatStore instance using a SAS token."""
    credential = AzureSasCredential(sas_token)
    return cls._from_clients(
        endpoint,
        credential,
        chat_table_name,
        metadata_table_name,
        metadata_partition_key,
        service_mode,
    )

```
 |  
| --- | --- |  
###  from_aad_token `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.from_aad_token "Permanent link")

```
from_aad_token(
    endpoint: ,
    chat_table_name:  = DEFAULT_CHAT_TABLE,
    metadata_table_name:  = DEFAULT_METADATA_TABLE,
    metadata_partition_key:  = None,
    service_mode: ServiceMode = STORAGE,
) -> 

```

Creates an AzureChatStore using an Azure Active Directory token.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
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
179
180
181
182
183
184
185
```
 | 
```
@classmethod
deffrom_aad_token(
    cls,
    endpoint: str,
    chat_table_name: str = DEFAULT_CHAT_TABLE,
    metadata_table_name: str = DEFAULT_METADATA_TABLE,
    metadata_partition_key: str = None,
    service_mode: ServiceMode = ServiceMode.STORAGE,
) -> "AzureChatStore":
"""Creates an AzureChatStore using an Azure Active Directory token."""
    fromazure.identityimport DefaultAzureCredential

    credential = DefaultAzureCredential()
    return cls._from_clients(
        endpoint,
        credential,
        chat_table_name,
        metadata_table_name,
        metadata_partition_key,
        service_mode,
    )

```
 |  
| --- | --- |  
###  set_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.set_messages "Permanent link")

```
set_messages(key: , messages: []) -> None

```

Set messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
| 
```
187
188
189
```
 | 
```
defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Set messages for a key."""
    asyncio_run(self.aset_messages(key, messages))

```
 |  
| --- | --- |  
###  aset_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.aset_messages "Permanent link")

```
aset_messages(
    key: , messages: []
) -> None

```

Asynchronoulsy set messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
| 
```
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
```
 | 
```
async defaset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Asynchronoulsy set messages for a key."""
    # Delete existing messages and insert new messages in one transaction
    chat_client = await self._atable_service_client.create_table_if_not_exists(
        self.chat_table_name
    )
    entities = chat_client.query_entities(f"PartitionKey eq '{key}'")
    all_entities = []
    async for entity in entities:
        all_entities.append(entity)

    delete_operations = (
        (TransactionOperation.DELETE, entity) for entity in all_entities
    )
    create_operations = (
        (
            TransactionOperation.CREATE,
            serialize(
                self.service_mode,
                {
                    "PartitionKey": key,
                    "RowKey": self._to_row_key(idx),
                    **message.dict(),
                },
            ),
        )
        for idx, message in enumerate(messages)
    )
    await chat_client.submit_transaction(
        chain(delete_operations, create_operations)
    )

    # Update metadata
    metadata_client = await self._atable_service_client.create_table_if_not_exists(
        self.metadata_table_name
    )
    messages_len = len(messages)
    await metadata_client.upsert_entity(
        {
            "PartitionKey": self.metadata_partition_key,
            "RowKey": key,
            "LastMessageRowKey": self._to_row_key(messages_len - 1),
            "MessageCount": messages_len,
        },
        UpdateMode.REPLACE,
    )

```
 |  
| --- | --- |  
###  get_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.get_messages "Permanent link")

```
get_messages(key: ) -> []

```

Get messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
| 
```
238
239
240
```
 | 
```
defget_messages(self, key: str) -> List[ChatMessage]:
"""Get messages for a key."""
    return asyncio_run(self.aget_messages(key))

```
 |  
| --- | --- |  
###  aget_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.aget_messages "Permanent link")

```
aget_messages(key: ) -> []

```

Asynchronously get messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
| 
```
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
async defaget_messages(self, key: str) -> List[ChatMessage]:
"""Asynchronously get messages for a key."""
    chat_client = await self._atable_service_client.create_table_if_not_exists(
        self.chat_table_name
    )
    entities = chat_client.query_entities(f"PartitionKey eq '{key}'")
    messages = []

    async for entity in entities:
        messages.append(
            ChatMessage.model_validate(deserialize(self.service_mode, entity))
        )

    return messages

```
 |  
| --- | --- |  
###  add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.add_message "Permanent link")

```
add_message(
    key: , message: , idx:  = None
)

```

Add a message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
| 
```
257
258
259
```
 | 
```
defadd_message(self, key: str, message: ChatMessage, idx: int = None):
"""Add a message for a key."""
    asyncio_run(self.async_add_message(key, message, idx))

```
 |  
| --- | --- |  
###  adelete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.adelete_messages "Permanent link")

```
adelete_messages(key: ) -> Optional[[]]

```

Asynchronously delete all messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
| 
```
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
```
 | 
```
async defadelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Asynchronously delete all messages for a key."""
    chat_client = await self._atable_service_client.create_table_if_not_exists(
        self.chat_table_name
    )
    entities = chat_client.query_entities(f"PartitionKey eq '{key}'")
    all_entities = []
    async for entity in entities:
        all_entities.append(entity)

    await chat_client.submit_transaction(
        (TransactionOperation.DELETE, entity) for entity in all_entities
    )

    metadata_client = await self._atable_service_client.create_table_if_not_exists(
        self.metadata_table_name
    )
    await metadata_client.upsert_entity(
        self._get_default_metadata(key), UpdateMode.REPLACE
    )

```
 |  
| --- | --- |  
###  delete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.delete_message "Permanent link")

```
delete_message(key: , idx: ) -> Optional[]

```

Delete specific message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
| 
```
318
319
320
```
 | 
```
defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
    return asyncio_run(self.adelete_message(key, idx))

```
 |  
| --- | --- |  
###  adelete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.adelete_message "Permanent link")

```
adelete_message(
    key: , idx: 
) -> Optional[]

```

Asynchronously delete specific message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
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
348
349
```
 | 
```
async defadelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Asynchronously delete specific message for a key."""
    # Fetch metadata to get the message count
    metadata_client = await self._atable_service_client.create_table_if_not_exists(
        self.metadata_table_name
    )
    metadata = await metadata_client.get_entity(
        partition_key=self.metadata_partition_key, row_key=key
    )

    # Index out of bounds
    message_count = int(metadata["MessageCount"])
    if idx >= message_count:
        return None

    # Delete the message
    chat_client = await self._atable_service_client.create_table_if_not_exists(
        self.chat_table_name
    )
    await chat_client.delete_entity(
        partition_key=key, row_key=self._to_row_key(idx)
    )

    # Update metadata if last message was deleted
    if idx == message_count - 1:
        metadata["LastMessageRowKey"] = self._to_row_key(idx - 1)
        metadata["MessageCount"] = message_count - 1
        await metadata_client.upsert_entity(metadata, mode=UpdateMode.MERGE)

```
 |  
| --- | --- |  
###  delete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.delete_last_message "Permanent link")

```
delete_last_message(key: ) -> Optional[]

```

Delete last message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
| 
```
351
352
353
```
 | 
```
defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete last message for a key."""
    return asyncio_run(self.adelete_last_message(key))

```
 |  
| --- | --- |  
###  adelete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.adelete_last_message "Permanent link")

```
adelete_last_message(key: ) -> Optional[]

```

Async delete last message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
| 
```
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
async defadelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Async delete last message for a key."""
    metadata_client = await self._atable_service_client.create_table_if_not_exists(
        self.metadata_table_name
    )
    # Retrieve metadata to get the last message row key
    metadata = await metadata_client.get_entity(
        partition_key=self.metadata_partition_key, row_key=key
    )
    last_row_key = metadata["LastMessageRowKey"]

    chat_client = await self._atable_service_client.create_table_if_not_exists(
        self.chat_table_name
    )
    # Delete the last message
    await chat_client.delete_entity(partition_key=key, row_key=last_row_key)

    # Update metadata
    last_row_key_num = int(last_row_key)
    metadata["LastMessageRowKey"] = self._to_row_key(
        last_row_key_num - 1 if last_row_key_num  0 else 0
    )
    metadata["MessageCount"] = int(metadata["MessageCount"]) - 1
    await metadata_client.upsert_entity(metadata, UpdateMode.MERGE)

```
 |  
| --- | --- |  
###  get_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.get_keys "Permanent link")

```
get_keys() -> []

```

Get all keys.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
| 
```
380
381
382
```
 | 
```
defget_keys(self) -> List[str]:
"""Get all keys."""
    return asyncio_run(self.aget_keys())

```
 |  
| --- | --- |  
###  aget_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.aget_keys "Permanent link")

```
aget_keys() -> []

```

Asynchronously get all keys.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
| 
```
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
```
 | 
```
async defaget_keys(self) -> List[str]:
"""Asynchronously get all keys."""
    metadata_client = await self._atable_service_client.create_table_if_not_exists(
        self.metadata_table_name
    )
    entities = metadata_client.query_entities(
        f"PartitionKey eq '{self.metadata_partition_key}'"
    )

    keys = []
    async for entity in entities:
        keys.append(entity["RowKey"])

    return keys

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azure/#llama_index.storage.chat_store.azure.AzureChatStore.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azure/llama_index/storage/chat_store/azure/base.py`  
| 
```
399
400
401
402
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "AzureChatStore"

```
 |  
| --- | --- |  
options: members: - AzureChatStore
