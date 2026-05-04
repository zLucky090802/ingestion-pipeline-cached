# Gel
##  GelKVStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/gel/#llama_index.storage.kvstore.gel.GelKVStore "Permanent link")
Bases: 
Gel Key-Value store.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-gel/llama_index/storage/kvstore/gel/base.py`  
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
```
 | 
```
classGelKVStore(BaseKVStore):
"""Gel Key-Value store."""

    def__init__(self, record_type: str = "Record") -> None:
"""
        Initialize GelKVStore.

        Args:
            record_type: The name of the record type in Gel schema.

        """
        self.record_type = record_type

        self._sync_client = None
        self._async_client = None

    defget_sync_client(self):
"""
        Get or initialize a synchronous Gel client.

        Ensures the client is connected and the record type exists.

        Returns:
            A connected synchronous Gel client.

        """
        if self._async_client is not None:
            raise RuntimeError(
                "GelKVStore has already been used in async mode. "
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
"""
        Get or initialize an asynchronous Gel client.

        Ensures the client is connected and the record type exists.

        Returns:
            A connected asynchronous Gel client.

        """
        if self._sync_client is not None:
            raise RuntimeError(
                "GelKVStore has already been used in sync mode. "
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
        client = self.get_sync_client()
        client.query(
            PUT_QUERY,
            key=key,
            namespace=collection,
            value=json.dumps(val),
        )

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
        client = await self.get_async_client()
        await client.query(
            PUT_QUERY,
            key=key,
            namespace=collection,
            value=json.dumps(val),
        )

    defput_all(
        self,
        kv_pairs: List[Tuple[str, dict]],
        collection: str = DEFAULT_COLLECTION,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
"""
        Store multiple key-value pairs in batches.

        Args:
            kv_pairs: List of (key, value) tuples to store.
            collection: Namespace for the keys.
            batch_size: Number of pairs to store in each batch.

        """
        for chunk in (
            kv_pairs[pos : pos + batch_size]
            for pos in range(0, len(kv_pairs), batch_size)
        ):
            client = self.get_sync_client()
            client.query(
                PUT_ALL_QUERY,
                data=json.dumps([{"key": key, "value": value} for key, value in chunk]),
                namespace=collection,
            )

    async defaput_all(
        self,
        kv_pairs: List[Tuple[str, dict]],
        collection: str = DEFAULT_COLLECTION,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
"""
        Async version of put_all.

        Args:
            kv_pairs: List of (key, value) tuples to store.
            collection: Namespace for the keys.
            batch_size: Number of pairs to store in each batch.

        """
        for chunk in (
            kv_pairs[pos : pos + batch_size]
            for pos in range(0, len(kv_pairs), batch_size)
        ):
            client = await self.get_async_client()
            await client.query(
                PUT_ALL_QUERY,
                data=json.dumps([{"key": key, "value": value} for key, value in chunk]),
                namespace=collection,
            )

    defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> Optional[dict]:
"""
        Get a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        client = self.get_sync_client()
        result = client.query_single(
            GET_QUERY,
            key=key,
            namespace=collection,
        )
        return json.loads(result) if result is not None else None

    async defaget(
        self, key: str, collection: str = DEFAULT_COLLECTION
    ) -> Optional[dict]:
"""
        Get a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        client = await self.get_async_client()
        result = await client.query_single(
            GET_QUERY,
            key=key,
            namespace=collection,
        )
        return json.loads(result) if result is not None else None

    defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
        Get all values from the store.

        Args:
            collection (str): collection name

        """
        client = self.get_sync_client()
        results = client.query(
            GET_ALL_QUERY,
            namespace=collection,
        )
        return {result.key: json.loads(result.value) for result in results}

    async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
        Get all values from the store.

        Args:
            collection (str): collection name

        """
        client = await self.get_async_client()
        results = await client.query(
            GET_ALL_QUERY,
            namespace=collection,
        )
        return {result.key: json.loads(result.value) for result in results}

    defdelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
        Delete a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        client = self.get_sync_client()
        result = client.query(
            DELETE_QUERY,
            key=key,
            namespace=collection,
        )
        return len(result)  0

    async defadelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
        Delete a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        client = await self.get_async_client()
        result = await client.query(
            DELETE_QUERY,
            key=key,
            namespace=collection,
        )
        return len(result)  0

```
 |  
| --- | --- |  
###  get_sync_client [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/gel/#llama_index.storage.kvstore.gel.GelKVStore.get_sync_client "Permanent link")

```
get_sync_client()

```

Get or initialize a synchronous Gel client.
Ensures the client is connected and the record type exists.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  A connected synchronous Gel client.  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-gel/llama_index/storage/kvstore/gel/base.py`  
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
```
 | 
```
defget_sync_client(self):
"""
    Get or initialize a synchronous Gel client.

    Ensures the client is connected and the record type exists.

    Returns:
        A connected synchronous Gel client.

    """
    if self._async_client is not None:
        raise RuntimeError(
            "GelKVStore has already been used in async mode. "
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
###  get_async_client [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/gel/#llama_index.storage.kvstore.gel.GelKVStore.get_async_client "Permanent link")

```
get_async_client()

```

Get or initialize an asynchronous Gel client.
Ensures the client is connected and the record type exists.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  A connected asynchronous Gel client.  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-gel/llama_index/storage/kvstore/gel/base.py`  
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
```
 | 
```
async defget_async_client(self):
"""
    Get or initialize an asynchronous Gel client.

    Ensures the client is connected and the record type exists.

    Returns:
        A connected asynchronous Gel client.

    """
    if self._sync_client is not None:
        raise RuntimeError(
            "GelKVStore has already been used in sync mode. "
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
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/gel/#llama_index.storage.kvstore.gel.GelKVStore.put "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-gel/llama_index/storage/kvstore/gel/base.py`  
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
    client = self.get_sync_client()
    client.query(
        PUT_QUERY,
        key=key,
        namespace=collection,
        value=json.dumps(val),
    )

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/gel/#llama_index.storage.kvstore.gel.GelKVStore.aput "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-gel/llama_index/storage/kvstore/gel/base.py`  
| 
```
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
    client = await self.get_async_client()
    await client.query(
        PUT_QUERY,
        key=key,
        namespace=collection,
        value=json.dumps(val),
    )

```
 |  
| --- | --- |  
###  put_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/gel/#llama_index.storage.kvstore.gel.GelKVStore.put_all "Permanent link")

```
put_all(
    kv_pairs: [Tuple[, ]],
    collection:  = DEFAULT_COLLECTION,
    batch_size:  = DEFAULT_BATCH_SIZE,
) -> None

```

Store multiple key-value pairs in batches.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `kv_pairs`  |  `List[Tuple[str, dict]]`  |  List of (key, value) tuples to store.  |  _required_  |  
|  `collection`  |  Namespace for the keys.  |  `DEFAULT_COLLECTION`  |  
|  `batch_size`  |  Number of pairs to store in each batch.  |  `DEFAULT_BATCH_SIZE`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-gel/llama_index/storage/kvstore/gel/base.py`  
| 
```
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
    Store multiple key-value pairs in batches.

    Args:
        kv_pairs: List of (key, value) tuples to store.
        collection: Namespace for the keys.
        batch_size: Number of pairs to store in each batch.

    """
    for chunk in (
        kv_pairs[pos : pos + batch_size]
        for pos in range(0, len(kv_pairs), batch_size)
    ):
        client = self.get_sync_client()
        client.query(
            PUT_ALL_QUERY,
            data=json.dumps([{"key": key, "value": value} for key, value in chunk]),
            namespace=collection,
        )

```
 |  
| --- | --- |  
###  aput_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/gel/#llama_index.storage.kvstore.gel.GelKVStore.aput_all "Permanent link")

```
aput_all(
    kv_pairs: [Tuple[, ]],
    collection:  = DEFAULT_COLLECTION,
    batch_size:  = DEFAULT_BATCH_SIZE,
) -> None

```

Async version of put_all.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `kv_pairs`  |  `List[Tuple[str, dict]]`  |  List of (key, value) tuples to store.  |  _required_  |  
|  `collection`  |  Namespace for the keys.  |  `DEFAULT_COLLECTION`  |  
|  `batch_size`  |  Number of pairs to store in each batch.  |  `DEFAULT_BATCH_SIZE`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-gel/llama_index/storage/kvstore/gel/base.py`  
| 
```
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
```
 | 
```
async defaput_all(
    self,
    kv_pairs: List[Tuple[str, dict]],
    collection: str = DEFAULT_COLLECTION,
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> None:
"""
    Async version of put_all.

    Args:
        kv_pairs: List of (key, value) tuples to store.
        collection: Namespace for the keys.
        batch_size: Number of pairs to store in each batch.

    """
    for chunk in (
        kv_pairs[pos : pos + batch_size]
        for pos in range(0, len(kv_pairs), batch_size)
    ):
        client = await self.get_async_client()
        await client.query(
            PUT_ALL_QUERY,
            data=json.dumps([{"key": key, "value": value} for key, value in chunk]),
            namespace=collection,
        )

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/gel/#llama_index.storage.kvstore.gel.GelKVStore.get "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-gel/llama_index/storage/kvstore/gel/base.py`  
| 
```
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
    client = self.get_sync_client()
    result = client.query_single(
        GET_QUERY,
        key=key,
        namespace=collection,
    )
    return json.loads(result) if result is not None else None

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/gel/#llama_index.storage.kvstore.gel.GelKVStore.aget "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-gel/llama_index/storage/kvstore/gel/base.py`  
| 
```
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
    client = await self.get_async_client()
    result = await client.query_single(
        GET_QUERY,
        key=key,
        namespace=collection,
    )
    return json.loads(result) if result is not None else None

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/gel/#llama_index.storage.kvstore.gel.GelKVStore.get_all "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-gel/llama_index/storage/kvstore/gel/base.py`  
| 
```
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
defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
    Get all values from the store.

    Args:
        collection (str): collection name

    """
    client = self.get_sync_client()
    results = client.query(
        GET_ALL_QUERY,
        namespace=collection,
    )
    return {result.key: json.loads(result.value) for result in results}

```
 |  
| --- | --- |  
###  aget_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/gel/#llama_index.storage.kvstore.gel.GelKVStore.aget_all "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-gel/llama_index/storage/kvstore/gel/base.py`  
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
369
370
371
```
 | 
```
async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
    Get all values from the store.

    Args:
        collection (str): collection name

    """
    client = await self.get_async_client()
    results = await client.query(
        GET_ALL_QUERY,
        namespace=collection,
    )
    return {result.key: json.loads(result.value) for result in results}

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/gel/#llama_index.storage.kvstore.gel.GelKVStore.delete "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-gel/llama_index/storage/kvstore/gel/base.py`  
| 
```
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
    client = self.get_sync_client()
    result = client.query(
        DELETE_QUERY,
        key=key,
        namespace=collection,
    )
    return len(result)  0

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/gel/#llama_index.storage.kvstore.gel.GelKVStore.adelete "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-gel/llama_index/storage/kvstore/gel/base.py`  
| 
```
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
    client = await self.get_async_client()
    result = await client.query(
        DELETE_QUERY,
        key=key,
        namespace=collection,
    )
    return len(result)  0

```
 |  
| --- | --- |  
options: members: - GelKVStore
