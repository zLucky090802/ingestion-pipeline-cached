# Azure
##  AzureKVStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore "Permanent link")
Bases: 
Provides a key-value store interface for Azure Table Storage and Cosmos DB. This class supports both synchronous and asynchronous operations on Azure Table Storage and Cosmos DB. It supports connecting to the service using different credentials and manages table creation and data serialization to conform to the storage requirements.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
| 
```
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
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
```
 | 
```
classAzureKVStore(BaseKVStore):
"""
    Provides a key-value store interface for Azure Table Storage and Cosmos
    DB. This class supports both synchronous and asynchronous operations on
    Azure Table Storage and Cosmos DB. It supports connecting to the service
    using different credentials and manages table creation and data
    serialization to conform to the storage requirements.
    """

    partition_key: str

    def__init__(
        self,
        table_service_client: Any,
        atable_service_client: Optional[Any] = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
        partition_key: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
"""Initializes the AzureKVStore with Azure Table Storage clients."""
        try:
            fromazure.data.tablesimport TableServiceClient
            fromazure.data.tables.aioimport (
                TableServiceClient as AsyncTableServiceClient,
            )
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        self.service_mode = service_mode
        self.partition_key = (
            DEFAULT_PARTITION_KEY if partition_key is None else partition_key
        )

        super().__init__(*args, **kwargs)

        self._table_service_client = cast(TableServiceClient, table_service_client)
        self._atable_service_client = cast(
            Optional[AsyncTableServiceClient], atable_service_client
        )

    @classmethod
    deffrom_connection_string(
        cls,
        connection_string: str,
        service_mode: ServiceMode = ServiceMode.STORAGE,
        partition_key: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> "AzureKVStore":
"""Creates an instance of AzureKVStore using a connection string."""
        try:
            fromazure.data.tablesimport TableServiceClient
            fromazure.data.tables.aioimport (
                TableServiceClient as AsyncTableServiceClient,
            )
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        table_service_client = TableServiceClient.from_connection_string(
            connection_string
        )
        atable_service_client = AsyncTableServiceClient.from_connection_string(
            connection_string
        )
        return cls(
            table_service_client,
            atable_service_client,
            service_mode,
            partition_key,
            *args,
            **kwargs,
        )

    @classmethod
    deffrom_account_and_key(
        cls,
        account_name: str,
        account_key: str,
        endpoint: Optional[str] = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
        partition_key: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> "AzureKVStore":
"""Creates an instance of AzureKVStore from an account name and key."""
        try:
            fromazure.core.credentialsimport AzureNamedKeyCredential
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        if endpoint is None:
            endpoint = f"https://{account_name}.table.core.windows.net"
        credential = AzureNamedKeyCredential(account_name, account_key)
        return cls._from_clients(
            endpoint, credential, service_mode, partition_key, *args, **kwargs
        )

    @classmethod
    deffrom_account_and_id(
        cls,
        account_name: str,
        endpoint: Optional[str] = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
        partition_key: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> "AzureKVStore":
"""Creates an instance of AzureKVStore from an account name and managed ID."""
        try:
            fromazure.identityimport DefaultAzureCredential
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        if endpoint is None:
            endpoint = f"https://{account_name}.table.core.windows.net"
        credential = DefaultAzureCredential()
        return cls._from_clients(
            endpoint, credential, service_mode, partition_key, *args, **kwargs
        )

    @classmethod
    deffrom_sas_token(
        cls,
        endpoint: str,
        sas_token: str,
        service_mode: ServiceMode = ServiceMode.STORAGE,
        partition_key: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> "AzureKVStore":
"""Creates an instance of AzureKVStore using a SAS token."""
        try:
            fromazure.core.credentialsimport AzureSasCredential
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        credential = AzureSasCredential(sas_token)
        return cls._from_clients(
            endpoint, credential, service_mode, partition_key, *args, **kwargs
        )

    @classmethod
    deffrom_aad_token(
        cls,
        endpoint: str,
        service_mode: ServiceMode = ServiceMode.STORAGE,
        partition_key: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> "AzureKVStore":
"""
        Creates an instance of AzureKVStore using Azure Active Directory
        (AAD) tokens.
        """
        try:
            fromazure.identityimport DefaultAzureCredential
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        credential = DefaultAzureCredential()
        return cls._from_clients(
            endpoint, credential, service_mode, partition_key, *args, **kwargs
        )

    defput(
        self,
        key: str,
        val: dict,
        collection: str = None,
    ) -> None:
"""Inserts or replaces a key-value pair in the specified table."""
        try:
            fromazure.data.tablesimport UpdateMode
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        table_name = (
            DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
        )
        table_client = self._table_service_client.create_table_if_not_exists(table_name)
        table_client.upsert_entity(
            {
                "PartitionKey": self.partition_key,
                "RowKey": key,
                **serialize(self.service_mode, val),
            },
            UpdateMode.REPLACE,
        )

    async defaput(
        self,
        key: str,
        val: dict,
        collection: str = None,
    ) -> None:
"""Inserts or replaces a key-value pair in the specified table."""
        try:
            fromazure.data.tablesimport UpdateMode
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        if self._atable_service_client is None:
            raise ValueError(MISSING_ASYNC_CLIENT_ERROR_MSG)

        table_name = (
            DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
        )
        atable_client = await self._atable_service_client.create_table_if_not_exists(
            table_name
        )
        await atable_client.upsert_entity(
            {
                "PartitionKey": self.partition_key,
                "RowKey": key,
                **serialize(self.service_mode, val),
            },
            mode=UpdateMode.REPLACE,
        )

    defput_all(
        self,
        kv_pairs: List[Tuple[str, dict]],
        collection: str = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
"""
        Inserts or replaces multiple key-value pairs in the specified table.
        """
        try:
            fromazure.data.tablesimport TransactionOperation
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        table_name = (
            DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
        )
        table_client = self._table_service_client.create_table_if_not_exists(table_name)

        entities = [
            {
                "PartitionKey": self.partition_key,
                "RowKey": key,
                **serialize(self.service_mode, val),
            }
            for key, val in kv_pairs
        ]

        entities_len = len(entities)
        for start in range(0, entities_len, batch_size):
            table_client.submit_transaction(
                (TransactionOperation.UPSERT, entities[i])
                for i in range(start, min(start + batch_size, entities_len))
            )

    async defaput_all(
        self,
        kv_pairs: List[Tuple[str, dict]],
        collection: str = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
"""
        Inserts or replaces multiple key-value pairs in the specified table.
        """
        try:
            fromazure.data.tablesimport TransactionOperation
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        if self._atable_service_client is None:
            raise ValueError(MISSING_ASYNC_CLIENT_ERROR_MSG)

        table_name = (
            DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
        )

        atable_client = await self._atable_service_client.create_table_if_not_exists(
            table_name
        )

        entities = [
            {
                "PartitionKey": self.partition_key,
                "RowKey": key,
                **serialize(self.service_mode, val),
            }
            for key, val in kv_pairs
        ]

        entities_len = len(entities)
        for start in range(0, entities_len, batch_size):
            await atable_client.submit_transaction(
                (TransactionOperation.UPSERT, entities[i])
                for i in range(start, min(start + batch_size, entities_len))
            )

    defget(
        self,
        key: str,
        collection: str = None,
        select: Optional[Union[str, List[str]]] = None,
    ) -> Optional[dict]:
"""Retrieves a value by key from the specified table."""
        try:
            fromazure.core.exceptionsimport ResourceNotFoundError
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        table_name = (
            DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
        )

        table_client = self._table_service_client.create_table_if_not_exists(table_name)
        try:
            entity = table_client.get_entity(
                partition_key=self.partition_key, row_key=key, select=select
            )
            return deserialize(self.service_mode, entity)
        except ResourceNotFoundError:
            return None

    async defaget(
        self,
        key: str,
        collection: str = None,
        select: Optional[Union[str, List[str]]] = None,
    ) -> Optional[dict]:
"""Retrieves a value by key from the specified table."""
        try:
            fromazure.core.exceptionsimport ResourceNotFoundError
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        if self._atable_service_client is None:
            raise ValueError(MISSING_ASYNC_CLIENT_ERROR_MSG)

        table_name = (
            DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
        )
        atable_client = await self._atable_service_client.create_table_if_not_exists(
            table_name
        )
        try:
            entity = await atable_client.get_entity(
                partition_key=self.partition_key, row_key=key, select=select
            )
            return deserialize(self.service_mode, entity)
        except ResourceNotFoundError:
            return None

    defget_all(
        self,
        collection: str = None,
        select: Optional[Union[str, List[str]]] = None,
    ) -> Dict[str, dict]:
"""
        Retrieves all key-value pairs from a specified partition in the table.
        """
        table_name = (
            DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
        )
        table_client = self._table_service_client.create_table_if_not_exists(table_name)
        entities = table_client.list_entities(
            filter=f"PartitionKey eq '{self.partition_key}'",
            select=select,
        )
        return {
            entity["RowKey"]: deserialize(self.service_mode, entity)
            for entity in entities
        }

    async defaget_all(
        self,
        collection: str = None,
        select: Optional[Union[str, List[str]]] = None,
    ) -> Dict[str, dict]:
"""
        Retrieves all key-value pairs from a specified partition in the table.
        """
        if self._atable_service_client is None:
            raise ValueError(MISSING_ASYNC_CLIENT_ERROR_MSG)
        table_name = (
            DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
        )
        atable_client = await self._atable_service_client.create_table_if_not_exists(
            table_name
        )
        entities = atable_client.list_entities(
            filter=f"PartitionKey eq '{self.partition_key}'",
            select=select,
        )
        return {
            entity["RowKey"]: deserialize(self.service_mode, entity)
            async for entity in entities
        }

    defdelete(
        self,
        key: str,
        collection: str = None,
    ) -> bool:
"""
        Deletes a specific key-value pair from the store based on the
        provided key and partition key.
        """
        table_name = (
            DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
        )
        table_client = self._table_service_client.create_table_if_not_exists(table_name)
        table_client.delete_entity(partition_key=self.partition_key, row_key=key)
        return True

    async defadelete(
        self,
        key: str,
        collection: str = None,
    ) -> bool:
"""Asynchronously deletes a specific key-value pair from the store."""
        if self._atable_service_client is None:
            raise ValueError(MISSING_ASYNC_CLIENT_ERROR_MSG)
        table_name = (
            DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
        )
        atable_client = await self._atable_service_client.create_table_if_not_exists(
            table_name
        )
        await atable_client.delete_entity(partition_key=self.partition_key, row_key=key)
        return True

    defquery(
        self,
        query_filter: str,
        collection: str = None,
        select: Optional[Union[str, List[str]]] = None,
    ) -> Generator[dict, None, None]:
"""Retrieves a value by key from the specified table."""
        try:
            fromazure.core.exceptionsimport ResourceNotFoundError
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        table_name = (
            DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
        )

        table_client = self._table_service_client.create_table_if_not_exists(table_name)
        try:
            entities = table_client.query_entities(
                query_filter=query_filter, select=select
            )

            return (deserialize(self.service_mode, entity) for entity in entities)
        except ResourceNotFoundError:
            return None

    async defaquery(
        self,
        query_filter: str,
        collection: str = None,
        select: Optional[Union[str, List[str]]] = None,
    ) -> Optional[AsyncGenerator[dict, None]]:
"""Asynchronously retrieves a value by key from the specified table."""
        try:
            fromazure.core.exceptionsimport ResourceNotFoundError
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        if self._atable_service_client is None:
            raise ValueError(MISSING_ASYNC_CLIENT_ERROR_MSG)

        table_name = (
            DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
        )
        atable_client = await self._atable_service_client.create_table_if_not_exists(
            table_name
        )
        try:
            entities = atable_client.query_entities(
                query_filter=query_filter, select=select
            )

            return (deserialize(self.service_mode, entity) async for entity in entities)

        except ResourceNotFoundError:
            return None

    @classmethod
    def_from_clients(
        cls, endpoint: str, credential: Any, *args: Any, **kwargs: Any
    ) -> "AzureKVStore":
"""
        Private method to create synchronous and asynchronous table service
        clients.
        """
        try:
            fromazure.data.tablesimport TableServiceClient
            fromazure.data.tables.aioimport (
                TableServiceClient as AsyncTableServiceClient,
            )
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        table_client = TableServiceClient(endpoint=endpoint, credential=credential)
        atable_client = AsyncTableServiceClient(
            endpoint=endpoint, credential=credential
        )
        return cls(table_client, atable_client, *args, **kwargs)

```
 |  
| --- | --- |  
###  from_connection_string `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore.from_connection_string "Permanent link")

```
from_connection_string(
    connection_string: ,
    service_mode: ServiceMode = STORAGE,
    partition_key: Optional[] = None,
    *args: ,
    **kwargs: 
) -> 

```

Creates an instance of AzureKVStore using a connection string.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_connection_string(
    cls,
    connection_string: str,
    service_mode: ServiceMode = ServiceMode.STORAGE,
    partition_key: Optional[str] = None,
    *args: Any,
    **kwargs: Any,
) -> "AzureKVStore":
"""Creates an instance of AzureKVStore using a connection string."""
    try:
        fromazure.data.tablesimport TableServiceClient
        fromazure.data.tables.aioimport (
            TableServiceClient as AsyncTableServiceClient,
        )
    except ImportError:
        raise ImportError(IMPORT_ERROR_MSG)

    table_service_client = TableServiceClient.from_connection_string(
        connection_string
    )
    atable_service_client = AsyncTableServiceClient.from_connection_string(
        connection_string
    )
    return cls(
        table_service_client,
        atable_service_client,
        service_mode,
        partition_key,
        *args,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  from_account_and_key `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore.from_account_and_key "Permanent link")

```
from_account_and_key(
    account_name: ,
    account_key: ,
    endpoint: Optional[] = None,
    service_mode: ServiceMode = STORAGE,
    partition_key: Optional[] = None,
    *args: ,
    **kwargs: 
) -> 

```

Creates an instance of AzureKVStore from an account name and key.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_account_and_key(
    cls,
    account_name: str,
    account_key: str,
    endpoint: Optional[str] = None,
    service_mode: ServiceMode = ServiceMode.STORAGE,
    partition_key: Optional[str] = None,
    *args: Any,
    **kwargs: Any,
) -> "AzureKVStore":
"""Creates an instance of AzureKVStore from an account name and key."""
    try:
        fromazure.core.credentialsimport AzureNamedKeyCredential
    except ImportError:
        raise ImportError(IMPORT_ERROR_MSG)

    if endpoint is None:
        endpoint = f"https://{account_name}.table.core.windows.net"
    credential = AzureNamedKeyCredential(account_name, account_key)
    return cls._from_clients(
        endpoint, credential, service_mode, partition_key, *args, **kwargs
    )

```
 |  
| --- | --- |  
###  from_account_and_id `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore.from_account_and_id "Permanent link")

```
from_account_and_id(
    account_name: ,
    endpoint: Optional[] = None,
    service_mode: ServiceMode = STORAGE,
    partition_key: Optional[] = None,
    *args: ,
    **kwargs: 
) -> 

```

Creates an instance of AzureKVStore from an account name and managed ID.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_account_and_id(
    cls,
    account_name: str,
    endpoint: Optional[str] = None,
    service_mode: ServiceMode = ServiceMode.STORAGE,
    partition_key: Optional[str] = None,
    *args: Any,
    **kwargs: Any,
) -> "AzureKVStore":
"""Creates an instance of AzureKVStore from an account name and managed ID."""
    try:
        fromazure.identityimport DefaultAzureCredential
    except ImportError:
        raise ImportError(IMPORT_ERROR_MSG)

    if endpoint is None:
        endpoint = f"https://{account_name}.table.core.windows.net"
    credential = DefaultAzureCredential()
    return cls._from_clients(
        endpoint, credential, service_mode, partition_key, *args, **kwargs
    )

```
 |  
| --- | --- |  
###  from_sas_token `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore.from_sas_token "Permanent link")

```
from_sas_token(
    endpoint: ,
    sas_token: ,
    service_mode: ServiceMode = STORAGE,
    partition_key: Optional[] = None,
    *args: ,
    **kwargs: 
) -> 

```

Creates an instance of AzureKVStore using a SAS token.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_sas_token(
    cls,
    endpoint: str,
    sas_token: str,
    service_mode: ServiceMode = ServiceMode.STORAGE,
    partition_key: Optional[str] = None,
    *args: Any,
    **kwargs: Any,
) -> "AzureKVStore":
"""Creates an instance of AzureKVStore using a SAS token."""
    try:
        fromazure.core.credentialsimport AzureSasCredential
    except ImportError:
        raise ImportError(IMPORT_ERROR_MSG)

    credential = AzureSasCredential(sas_token)
    return cls._from_clients(
        endpoint, credential, service_mode, partition_key, *args, **kwargs
    )

```
 |  
| --- | --- |  
###  from_aad_token `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore.from_aad_token "Permanent link")

```
from_aad_token(
    endpoint: ,
    service_mode: ServiceMode = STORAGE,
    partition_key: Optional[] = None,
    *args: ,
    **kwargs: 
) -> 

```

Creates an instance of AzureKVStore using Azure Active Directory (AAD) tokens.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_aad_token(
    cls,
    endpoint: str,
    service_mode: ServiceMode = ServiceMode.STORAGE,
    partition_key: Optional[str] = None,
    *args: Any,
    **kwargs: Any,
) -> "AzureKVStore":
"""
    Creates an instance of AzureKVStore using Azure Active Directory
    (AAD) tokens.
    """
    try:
        fromazure.identityimport DefaultAzureCredential
    except ImportError:
        raise ImportError(IMPORT_ERROR_MSG)

    credential = DefaultAzureCredential()
    return cls._from_clients(
        endpoint, credential, service_mode, partition_key, *args, **kwargs
    )

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore.put "Permanent link")

```
put(key: , val: , collection:  = None) -> None

```

Inserts or replaces a key-value pair in the specified table.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
| 
```
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
defput(
    self,
    key: str,
    val: dict,
    collection: str = None,
) -> None:
"""Inserts or replaces a key-value pair in the specified table."""
    try:
        fromazure.data.tablesimport UpdateMode
    except ImportError:
        raise ImportError(IMPORT_ERROR_MSG)

    table_name = (
        DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
    )
    table_client = self._table_service_client.create_table_if_not_exists(table_name)
    table_client.upsert_entity(
        {
            "PartitionKey": self.partition_key,
            "RowKey": key,
            **serialize(self.service_mode, val),
        },
        UpdateMode.REPLACE,
    )

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore.aput "Permanent link")

```
aput(key: , val: , collection:  = None) -> None

```

Inserts or replaces a key-value pair in the specified table.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
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
async defaput(
    self,
    key: str,
    val: dict,
    collection: str = None,
) -> None:
"""Inserts or replaces a key-value pair in the specified table."""
    try:
        fromazure.data.tablesimport UpdateMode
    except ImportError:
        raise ImportError(IMPORT_ERROR_MSG)

    if self._atable_service_client is None:
        raise ValueError(MISSING_ASYNC_CLIENT_ERROR_MSG)

    table_name = (
        DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
    )
    atable_client = await self._atable_service_client.create_table_if_not_exists(
        table_name
    )
    await atable_client.upsert_entity(
        {
            "PartitionKey": self.partition_key,
            "RowKey": key,
            **serialize(self.service_mode, val),
        },
        mode=UpdateMode.REPLACE,
    )

```
 |  
| --- | --- |  
###  put_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore.put_all "Permanent link")

```
put_all(
    kv_pairs: [Tuple[, ]],
    collection:  = None,
    batch_size:  = DEFAULT_BATCH_SIZE,
) -> None

```

Inserts or replaces multiple key-value pairs in the specified table.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
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
281
282
283
284
285
```
 | 
```
defput_all(
    self,
    kv_pairs: List[Tuple[str, dict]],
    collection: str = None,
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> None:
"""
    Inserts or replaces multiple key-value pairs in the specified table.
    """
    try:
        fromazure.data.tablesimport TransactionOperation
    except ImportError:
        raise ImportError(IMPORT_ERROR_MSG)

    table_name = (
        DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
    )
    table_client = self._table_service_client.create_table_if_not_exists(table_name)

    entities = [
        {
            "PartitionKey": self.partition_key,
            "RowKey": key,
            **serialize(self.service_mode, val),
        }
        for key, val in kv_pairs
    ]

    entities_len = len(entities)
    for start in range(0, entities_len, batch_size):
        table_client.submit_transaction(
            (TransactionOperation.UPSERT, entities[i])
            for i in range(start, min(start + batch_size, entities_len))
        )

```
 |  
| --- | --- |  
###  aput_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore.aput_all "Permanent link")

```
aput_all(
    kv_pairs: [Tuple[, ]],
    collection:  = None,
    batch_size:  = DEFAULT_BATCH_SIZE,
) -> None

```

Inserts or replaces multiple key-value pairs in the specified table.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
| 
```
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
```
 | 
```
async defaput_all(
    self,
    kv_pairs: List[Tuple[str, dict]],
    collection: str = None,
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> None:
"""
    Inserts or replaces multiple key-value pairs in the specified table.
    """
    try:
        fromazure.data.tablesimport TransactionOperation
    except ImportError:
        raise ImportError(IMPORT_ERROR_MSG)

    if self._atable_service_client is None:
        raise ValueError(MISSING_ASYNC_CLIENT_ERROR_MSG)

    table_name = (
        DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
    )

    atable_client = await self._atable_service_client.create_table_if_not_exists(
        table_name
    )

    entities = [
        {
            "PartitionKey": self.partition_key,
            "RowKey": key,
            **serialize(self.service_mode, val),
        }
        for key, val in kv_pairs
    ]

    entities_len = len(entities)
    for start in range(0, entities_len, batch_size):
        await atable_client.submit_transaction(
            (TransactionOperation.UPSERT, entities[i])
            for i in range(start, min(start + batch_size, entities_len))
        )

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore.get "Permanent link")

```
get(
    key: ,
    collection:  = None,
    select: Optional[Union[, []]] = None,
) -> Optional[]

```

Retrieves a value by key from the specified table.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
| 
```
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
```
 | 
```
defget(
    self,
    key: str,
    collection: str = None,
    select: Optional[Union[str, List[str]]] = None,
) -> Optional[dict]:
"""Retrieves a value by key from the specified table."""
    try:
        fromazure.core.exceptionsimport ResourceNotFoundError
    except ImportError:
        raise ImportError(IMPORT_ERROR_MSG)

    table_name = (
        DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
    )

    table_client = self._table_service_client.create_table_if_not_exists(table_name)
    try:
        entity = table_client.get_entity(
            partition_key=self.partition_key, row_key=key, select=select
        )
        return deserialize(self.service_mode, entity)
    except ResourceNotFoundError:
        return None

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore.aget "Permanent link")

```
aget(
    key: ,
    collection:  = None,
    select: Optional[Union[, []]] = None,
) -> Optional[]

```

Retrieves a value by key from the specified table.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
| 
```
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
async defaget(
    self,
    key: str,
    collection: str = None,
    select: Optional[Union[str, List[str]]] = None,
) -> Optional[dict]:
"""Retrieves a value by key from the specified table."""
    try:
        fromazure.core.exceptionsimport ResourceNotFoundError
    except ImportError:
        raise ImportError(IMPORT_ERROR_MSG)

    if self._atable_service_client is None:
        raise ValueError(MISSING_ASYNC_CLIENT_ERROR_MSG)

    table_name = (
        DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
    )
    atable_client = await self._atable_service_client.create_table_if_not_exists(
        table_name
    )
    try:
        entity = await atable_client.get_entity(
            partition_key=self.partition_key, row_key=key, select=select
        )
        return deserialize(self.service_mode, entity)
    except ResourceNotFoundError:
        return None

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore.get_all "Permanent link")

```
get_all(
    collection:  = None,
    select: Optional[Union[, []]] = None,
) -> [, ]

```

Retrieves all key-value pairs from a specified partition in the table.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
| 
```
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
```
 | 
```
defget_all(
    self,
    collection: str = None,
    select: Optional[Union[str, List[str]]] = None,
) -> Dict[str, dict]:
"""
    Retrieves all key-value pairs from a specified partition in the table.
    """
    table_name = (
        DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
    )
    table_client = self._table_service_client.create_table_if_not_exists(table_name)
    entities = table_client.list_entities(
        filter=f"PartitionKey eq '{self.partition_key}'",
        select=select,
    )
    return {
        entity["RowKey"]: deserialize(self.service_mode, entity)
        for entity in entities
    }

```
 |  
| --- | --- |  
###  aget_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore.aget_all "Permanent link")

```
aget_all(
    collection:  = None,
    select: Optional[Union[, []]] = None,
) -> [, ]

```

Retrieves all key-value pairs from a specified partition in the table.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
| 
```
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
```
 | 
```
async defaget_all(
    self,
    collection: str = None,
    select: Optional[Union[str, List[str]]] = None,
) -> Dict[str, dict]:
"""
    Retrieves all key-value pairs from a specified partition in the table.
    """
    if self._atable_service_client is None:
        raise ValueError(MISSING_ASYNC_CLIENT_ERROR_MSG)
    table_name = (
        DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
    )
    atable_client = await self._atable_service_client.create_table_if_not_exists(
        table_name
    )
    entities = atable_client.list_entities(
        filter=f"PartitionKey eq '{self.partition_key}'",
        select=select,
    )
    return {
        entity["RowKey"]: deserialize(self.service_mode, entity)
        async for entity in entities
    }

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore.delete "Permanent link")

```
delete(key: , collection:  = None) -> 

```

Deletes a specific key-value pair from the store based on the provided key and partition key.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
| 
```
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
```
 | 
```
defdelete(
    self,
    key: str,
    collection: str = None,
) -> bool:
"""
    Deletes a specific key-value pair from the store based on the
    provided key and partition key.
    """
    table_name = (
        DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
    )
    table_client = self._table_service_client.create_table_if_not_exists(table_name)
    table_client.delete_entity(partition_key=self.partition_key, row_key=key)
    return True

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore.adelete "Permanent link")

```
adelete(key: , collection:  = None) -> 

```

Asynchronously deletes a specific key-value pair from the store.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
| 
```
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
457
458
459
```
 | 
```
async defadelete(
    self,
    key: str,
    collection: str = None,
) -> bool:
"""Asynchronously deletes a specific key-value pair from the store."""
    if self._atable_service_client is None:
        raise ValueError(MISSING_ASYNC_CLIENT_ERROR_MSG)
    table_name = (
        DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
    )
    atable_client = await self._atable_service_client.create_table_if_not_exists(
        table_name
    )
    await atable_client.delete_entity(partition_key=self.partition_key, row_key=key)
    return True

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore.query "Permanent link")

```
query(
    query_filter: ,
    collection:  = None,
    select: Optional[Union[, []]] = None,
) -> Generator[, None, None]

```

Retrieves a value by key from the specified table.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
| 
```
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
```
 | 
```
defquery(
    self,
    query_filter: str,
    collection: str = None,
    select: Optional[Union[str, List[str]]] = None,
) -> Generator[dict, None, None]:
"""Retrieves a value by key from the specified table."""
    try:
        fromazure.core.exceptionsimport ResourceNotFoundError
    except ImportError:
        raise ImportError(IMPORT_ERROR_MSG)

    table_name = (
        DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
    )

    table_client = self._table_service_client.create_table_if_not_exists(table_name)
    try:
        entities = table_client.query_entities(
            query_filter=query_filter, select=select
        )

        return (deserialize(self.service_mode, entity) for entity in entities)
    except ResourceNotFoundError:
        return None

```
 |  
| --- | --- |  
###  aquery [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azure/#llama_index.storage.kvstore.azure.AzureKVStore.aquery "Permanent link")

```
aquery(
    query_filter: ,
    collection:  = None,
    select: Optional[Union[, []]] = None,
) -> Optional[AsyncGenerator[, None]]

```

Asynchronously retrieves a value by key from the specified table.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azure/llama_index/storage/kvstore/azure/base.py`  
| 
```
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
```
 | 
```
async defaquery(
    self,
    query_filter: str,
    collection: str = None,
    select: Optional[Union[str, List[str]]] = None,
) -> Optional[AsyncGenerator[dict, None]]:
"""Asynchronously retrieves a value by key from the specified table."""
    try:
        fromazure.core.exceptionsimport ResourceNotFoundError
    except ImportError:
        raise ImportError(IMPORT_ERROR_MSG)

    if self._atable_service_client is None:
        raise ValueError(MISSING_ASYNC_CLIENT_ERROR_MSG)

    table_name = (
        DEFAULT_COLLECTION if not collection else sanitize_table_name(collection)
    )
    atable_client = await self._atable_service_client.create_table_if_not_exists(
        table_name
    )
    try:
        entities = atable_client.query_entities(
            query_filter=query_filter, select=select
        )

        return (deserialize(self.service_mode, entity) async for entity in entities)

    except ResourceNotFoundError:
        return None

```
 |  
| --- | --- |  
options: members: - AzureKVStore
