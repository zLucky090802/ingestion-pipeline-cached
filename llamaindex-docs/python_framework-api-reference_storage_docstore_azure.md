# Azure
##  AzureDocumentStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/azure/#llama_index.storage.docstore.azure.AzureDocumentStore "Permanent link")
Bases: `KVDocumentStore`
Azure Document (Node) store. An Azure Table store for Document and Node objects.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-azure/llama_index/storage/docstore/azure/base.py`  
| 
```
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
```
 | 
```
classAzureDocumentStore(KVDocumentStore):
"""
    Azure Document (Node) store.
    An Azure Table store for Document and Node objects.
    """

    _kvstore: AzureKVStore

    def__init__(
        self,
        azure_kvstore: AzureKVStore,
        namespace: Optional[str] = None,
        node_collection_suffix: Optional[str] = None,
        ref_doc_collection_suffix: Optional[str] = None,
        metadata_collection_suffix: Optional[str] = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
"""Initialize an AzureDocumentStore."""
        super().__init__(
            azure_kvstore,
            namespace,
            batch_size,
            node_collection_suffix,
            ref_doc_collection_suffix,
            metadata_collection_suffix,
        )

    @classmethod
    deffrom_connection_string(
        cls,
        connection_string: str,
        namespace: Optional[str] = None,
        node_collection_suffix: Optional[str] = None,
        ref_doc_collection_suffix: Optional[str] = None,
        metadata_collection_suffix: Optional[str] = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
        partition_key: Optional[str] = None,
        **kwargs,
    ) -> "AzureDocumentStore":
"""Initialize an AzureDocumentStore from an Azure connection string."""
        azure_kvstore = AzureKVStore.from_connection_string(
            connection_string,
            service_mode=service_mode,
            partition_key=partition_key,
        )
        return cls(
            azure_kvstore,
            namespace,
            node_collection_suffix,
            ref_doc_collection_suffix,
            metadata_collection_suffix,
            **kwargs,
        )

    @classmethod
    deffrom_account_and_key(
        cls,
        account_name: str,
        account_key: str,
        namespace: Optional[str] = None,
        node_collection_suffix: Optional[str] = None,
        ref_doc_collection_suffix: Optional[str] = None,
        metadata_collection_suffix: Optional[str] = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
        partition_key: Optional[str] = None,
        **kwargs,
    ) -> "AzureDocumentStore":
"""Initialize an AzureDocumentStore from an account name and key."""
        azure_kvstore = AzureKVStore.from_account_and_key(
            account_name,
            account_key,
            service_mode=service_mode,
            partition_key=partition_key,
        )
        return cls(
            azure_kvstore,
            namespace,
            node_collection_suffix,
            ref_doc_collection_suffix,
            metadata_collection_suffix,
            **kwargs,
        )

    @classmethod
    deffrom_account_and_id(
        cls,
        account_name: str,
        namespace: Optional[str] = None,
        node_collection_suffix: Optional[str] = None,
        ref_doc_collection_suffix: Optional[str] = None,
        metadata_collection_suffix: Optional[str] = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
        partition_key: Optional[str] = None,
        **kwargs,
    ) -> "AzureDocumentStore":
"""Initialize an AzureDocumentStore from an account name and managed ID."""
        azure_kvstore = AzureKVStore.from_account_and_id(
            account_name,
            service_mode=service_mode,
            partition_key=partition_key,
        )
        return cls(
            azure_kvstore,
            namespace,
            node_collection_suffix,
            ref_doc_collection_suffix,
            metadata_collection_suffix,
            **kwargs,
        )

    @classmethod
    deffrom_sas_token(
        cls,
        endpoint: str,
        sas_token: str,
        namespace: Optional[str] = None,
        node_collection_suffix: Optional[str] = None,
        ref_doc_collection_suffix: Optional[str] = None,
        metadata_collection_suffix: Optional[str] = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
        partition_key: Optional[str] = None,
        **kwargs,
    ) -> "AzureDocumentStore":
"""Initialize an AzureDocumentStore from a SAS token."""
        azure_kvstore = AzureKVStore.from_sas_token(
            endpoint,
            sas_token,
            service_mode=service_mode,
            partition_key=partition_key,
        )
        return cls(
            azure_kvstore,
            namespace,
            node_collection_suffix,
            ref_doc_collection_suffix,
            metadata_collection_suffix,
            **kwargs,
        )

    @classmethod
    deffrom_aad_token(
        cls,
        endpoint: str,
        namespace: Optional[str] = None,
        node_collection_suffix: Optional[str] = None,
        ref_doc_collection_suffix: Optional[str] = None,
        metadata_collection_suffix: Optional[str] = None,
        service_mode: ServiceMode = ServiceMode.STORAGE,
        partition_key: Optional[str] = None,
        **kwargs,
    ) -> "AzureDocumentStore":
"""Initialize an AzureDocumentStore from an AAD token."""
        azure_kvstore = AzureKVStore.from_aad_token(
            endpoint,
            service_mode=service_mode,
            partition_key=partition_key,
        )
        return cls(
            azure_kvstore,
            namespace,
            node_collection_suffix,
            ref_doc_collection_suffix,
            metadata_collection_suffix,
            **kwargs,
        )

    def_extract_doc_metadatas(
        self, ref_doc_kv_pairs: List[Tuple[str, dict]]
    ) -> List[Tuple[str, Optional[dict]]]:
"""Prepare reference document key-value pairs."""
        doc_metadatas: List[Tuple[str, dict]] = [
            (doc_id, {"metadata": doc_dict.get("metadata")})
            for doc_id, doc_dict in ref_doc_kv_pairs
        ]
        return doc_metadatas

    defadd_documents(
        self,
        docs: Sequence[BaseNode],
        allow_update: bool = True,
        batch_size: Optional[int] = None,
        store_text: bool = True,
    ) -> None:
"""Add documents to the store."""
        batch_size = batch_size or self._batch_size

        node_kv_pairs, metadata_kv_pairs, ref_doc_kv_pairs = super()._prepare_kv_pairs(
            docs, allow_update, store_text
        )

        # Change ref_doc_kv_pairs
        ref_doc_kv_pairs = self._extract_doc_metadatas(ref_doc_kv_pairs)

        self._kvstore.put_all(
            node_kv_pairs,
            collection=self._node_collection,
            batch_size=batch_size,
        )

        self._kvstore.put_all(
            metadata_kv_pairs,
            collection=self._metadata_collection,
            batch_size=batch_size,
        )

        self._kvstore.put_all(
            ref_doc_kv_pairs,
            collection=self._ref_doc_collection,
            batch_size=batch_size,
        )

    async defasync_add_documents(
        self,
        docs: Sequence[BaseNode],
        allow_update: bool = True,
        batch_size: Optional[int] = None,
        store_text: bool = True,
    ) -> None:
"""Add documents to the store."""
        batch_size = batch_size or self._batch_size

        (
            node_kv_pairs,
            metadata_kv_pairs,
            ref_doc_kv_pairs,
        ) = await super()._async_prepare_kv_pairs(docs, allow_update, store_text)

        # Change ref_doc_kv_pairs
        ref_doc_kv_pairs = self._extract_doc_metadatas(ref_doc_kv_pairs)

        await asyncio.gather(
            self._kvstore.aput_all(
                node_kv_pairs,
                collection=self._node_collection,
                batch_size=batch_size,
            ),
            self._kvstore.aput_all(
                metadata_kv_pairs,
                collection=self._metadata_collection,
                batch_size=batch_size,
            ),
            self._kvstore.aput_all(
                ref_doc_kv_pairs,
                collection=self._ref_doc_collection,
                batch_size=batch_size,
            ),
        )

    defget_ref_doc_info(self, ref_doc_id: str) -> Optional[RefDocInfo]:
"""Get the RefDocInfo for a given ref_doc_id."""
        ref_doc_infos = self._kvstore.query(
            f"PartitionKey eq '{self._kvstore.partition_key}' and ref_doc_id eq '{ref_doc_id}'",
            self._metadata_collection,
            select="RowKey",
        )

        node_ids = [doc["RowKey"] for doc in ref_doc_infos]
        if not node_ids:
            return None

        doc_metadata = self._kvstore.get(
            ref_doc_id, collection=self._ref_doc_collection, select="metadata"
        )

        ref_doc_info_dict = {
            "node_ids": node_ids,
            "metadata": doc_metadata.get("metadata"),
        }

        # TODO: deprecated legacy support
        return self._remove_legacy_info(ref_doc_info_dict)

    async defaget_ref_doc_info(self, ref_doc_id: str) -> Optional[RefDocInfo]:
"""Get the RefDocInfo for a given ref_doc_id."""
        metadatas = await self._kvstore.aquery(
            f"PartitionKey eq '{self._kvstore.partition_key}' and RowKey eq '{ref_doc_id}'",
            self._metadata_collection,
            select="RowKey",
        )

        node_ids = [metadata["RowKey"] async for metadata in metadatas]

        if not node_ids:
            return None

        doc_metadata = await self._kvstore.aget(
            ref_doc_id, collection=self._ref_doc_collection, select="metadata"
        )

        ref_doc_info_dict = {
            "node_ids": node_ids,
            "metadata": doc_metadata.get("metadata") if doc_metadata else None,
        }

        # TODO: deprecated legacy support
        return self._remove_legacy_info(ref_doc_info_dict)

    defget_all_ref_doc_info(self) -> Optional[Dict[str, RefDocInfo]]:
"""
        Get a mapping of ref_doc_id -> RefDocInfo for all ingested documents.
        """
        ref_doc_infos = self._kvstore.query(
            f"PartitionKey eq '{self._kvstore.partition_key}'",
            self._metadata_collection,
            select=["RowKey", "ref_doc_id"],
        )

        # TODO: deprecated legacy support
        all_ref_doc_infos = defaultdict(lambda: {"node_ids": [], "metadata": None})
        for ref_doc_info in ref_doc_infos:
            ref_doc_id = ref_doc_info["ref_doc_id"]
            ref_doc_info_dict = all_ref_doc_infos[ref_doc_id]
            ref_doc_info_dict["node_ids"].append(ref_doc_info["RowKey"])

            if ref_doc_info_dict["metadata"] is None:
                ref_doc = self._kvstore.get(
                    ref_doc_id, collection=self._ref_doc_collection, select="metadata"
                )
                ref_doc_info_dict["metadata"] = ref_doc.get("metadata")

        for ref_doc_id, ref_doc_info_dict in all_ref_doc_infos.items():
            all_ref_doc_infos[ref_doc_id] = self._remove_legacy_info(ref_doc_info_dict)

        return all_ref_doc_infos

    async defaget_all_ref_doc_info(self) -> Optional[Dict[str, RefDocInfo]]:
"""
        Get a mapping of ref_doc_id -> RefDocInfo for all ingested documents.
        """
        ref_doc_infos = await self._kvstore.aquery(
            f"PartitionKey eq '{self._kvstore.partition_key}'",
            self._metadata_collection,
            select=["RowKey", "ref_doc_id"],
        )

        # TODO: deprecated legacy support
        all_ref_doc_infos = defaultdict(lambda: {"node_ids": [], "metadata": None})
        async for ref_doc_info in ref_doc_infos:
            ref_doc_id = ref_doc_info["ref_doc_id"]
            ref_doc_info_dict = all_ref_doc_infos[ref_doc_id]
            ref_doc_info_dict["node_ids"].append(ref_doc_info["RowKey"])

            if ref_doc_info_dict["metadata"] is None:
                ref_doc = await self._kvstore.aget(
                    ref_doc_id, collection=self._ref_doc_collection, select="metadata"
                )
                ref_doc_info_dict["metadata"] = ref_doc.get("metadata")

        for ref_doc_id, ref_doc_info_dict in all_ref_doc_infos.items():
            all_ref_doc_infos[ref_doc_id] = self._remove_legacy_info(ref_doc_info_dict)

        return all_ref_doc_infos

    def_remove_from_ref_doc_node(self, doc_id: str) -> None:
"""
        Helper function to remove node doc_id from ref_doc_collection.
        If ref_doc has no more doc_ids, delete it from the collection.
        """
        self._kvstore.delete(doc_id, collection=self._metadata_collection)

    async def_aremove_from_ref_doc_node(self, doc_id: str) -> None:
"""
        Helper function to remove node doc_id from ref_doc_collection.
        If ref_doc has no more doc_ids, delete it from the collection.
        """
        await self._kvstore.adelete(doc_id, collection=self._metadata_collection)

```
 |  
| --- | --- |  
###  from_connection_string `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/azure/#llama_index.storage.docstore.azure.AzureDocumentStore.from_connection_string "Permanent link")

```
from_connection_string(
    connection_string: ,
    namespace: Optional[] = None,
    node_collection_suffix: Optional[] = None,
    ref_doc_collection_suffix: Optional[] = None,
    metadata_collection_suffix: Optional[] = None,
    service_mode: ServiceMode = STORAGE,
    partition_key: Optional[] = None,
    **kwargs
) -> 

```

Initialize an AzureDocumentStore from an Azure connection string.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-azure/llama_index/storage/docstore/azure/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_connection_string(
    cls,
    connection_string: str,
    namespace: Optional[str] = None,
    node_collection_suffix: Optional[str] = None,
    ref_doc_collection_suffix: Optional[str] = None,
    metadata_collection_suffix: Optional[str] = None,
    service_mode: ServiceMode = ServiceMode.STORAGE,
    partition_key: Optional[str] = None,
    **kwargs,
) -> "AzureDocumentStore":
"""Initialize an AzureDocumentStore from an Azure connection string."""
    azure_kvstore = AzureKVStore.from_connection_string(
        connection_string,
        service_mode=service_mode,
        partition_key=partition_key,
    )
    return cls(
        azure_kvstore,
        namespace,
        node_collection_suffix,
        ref_doc_collection_suffix,
        metadata_collection_suffix,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  from_account_and_key `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/azure/#llama_index.storage.docstore.azure.AzureDocumentStore.from_account_and_key "Permanent link")

```
from_account_and_key(
    account_name: ,
    account_key: ,
    namespace: Optional[] = None,
    node_collection_suffix: Optional[] = None,
    ref_doc_collection_suffix: Optional[] = None,
    metadata_collection_suffix: Optional[] = None,
    service_mode: ServiceMode = STORAGE,
    partition_key: Optional[] = None,
    **kwargs
) -> 

```

Initialize an AzureDocumentStore from an account name and key.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-azure/llama_index/storage/docstore/azure/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_account_and_key(
    cls,
    account_name: str,
    account_key: str,
    namespace: Optional[str] = None,
    node_collection_suffix: Optional[str] = None,
    ref_doc_collection_suffix: Optional[str] = None,
    metadata_collection_suffix: Optional[str] = None,
    service_mode: ServiceMode = ServiceMode.STORAGE,
    partition_key: Optional[str] = None,
    **kwargs,
) -> "AzureDocumentStore":
"""Initialize an AzureDocumentStore from an account name and key."""
    azure_kvstore = AzureKVStore.from_account_and_key(
        account_name,
        account_key,
        service_mode=service_mode,
        partition_key=partition_key,
    )
    return cls(
        azure_kvstore,
        namespace,
        node_collection_suffix,
        ref_doc_collection_suffix,
        metadata_collection_suffix,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  from_account_and_id `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/azure/#llama_index.storage.docstore.azure.AzureDocumentStore.from_account_and_id "Permanent link")

```
from_account_and_id(
    account_name: ,
    namespace: Optional[] = None,
    node_collection_suffix: Optional[] = None,
    ref_doc_collection_suffix: Optional[] = None,
    metadata_collection_suffix: Optional[] = None,
    service_mode: ServiceMode = STORAGE,
    partition_key: Optional[] = None,
    **kwargs
) -> 

```

Initialize an AzureDocumentStore from an account name and managed ID.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-azure/llama_index/storage/docstore/azure/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_account_and_id(
    cls,
    account_name: str,
    namespace: Optional[str] = None,
    node_collection_suffix: Optional[str] = None,
    ref_doc_collection_suffix: Optional[str] = None,
    metadata_collection_suffix: Optional[str] = None,
    service_mode: ServiceMode = ServiceMode.STORAGE,
    partition_key: Optional[str] = None,
    **kwargs,
) -> "AzureDocumentStore":
"""Initialize an AzureDocumentStore from an account name and managed ID."""
    azure_kvstore = AzureKVStore.from_account_and_id(
        account_name,
        service_mode=service_mode,
        partition_key=partition_key,
    )
    return cls(
        azure_kvstore,
        namespace,
        node_collection_suffix,
        ref_doc_collection_suffix,
        metadata_collection_suffix,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  from_sas_token `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/azure/#llama_index.storage.docstore.azure.AzureDocumentStore.from_sas_token "Permanent link")

```
from_sas_token(
    endpoint: ,
    sas_token: ,
    namespace: Optional[] = None,
    node_collection_suffix: Optional[] = None,
    ref_doc_collection_suffix: Optional[] = None,
    metadata_collection_suffix: Optional[] = None,
    service_mode: ServiceMode = STORAGE,
    partition_key: Optional[] = None,
    **kwargs
) -> 

```

Initialize an AzureDocumentStore from a SAS token.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-azure/llama_index/storage/docstore/azure/base.py`  
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
```
 | 
```
@classmethod
deffrom_sas_token(
    cls,
    endpoint: str,
    sas_token: str,
    namespace: Optional[str] = None,
    node_collection_suffix: Optional[str] = None,
    ref_doc_collection_suffix: Optional[str] = None,
    metadata_collection_suffix: Optional[str] = None,
    service_mode: ServiceMode = ServiceMode.STORAGE,
    partition_key: Optional[str] = None,
    **kwargs,
) -> "AzureDocumentStore":
"""Initialize an AzureDocumentStore from a SAS token."""
    azure_kvstore = AzureKVStore.from_sas_token(
        endpoint,
        sas_token,
        service_mode=service_mode,
        partition_key=partition_key,
    )
    return cls(
        azure_kvstore,
        namespace,
        node_collection_suffix,
        ref_doc_collection_suffix,
        metadata_collection_suffix,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  from_aad_token `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/azure/#llama_index.storage.docstore.azure.AzureDocumentStore.from_aad_token "Permanent link")

```
from_aad_token(
    endpoint: ,
    namespace: Optional[] = None,
    node_collection_suffix: Optional[] = None,
    ref_doc_collection_suffix: Optional[] = None,
    metadata_collection_suffix: Optional[] = None,
    service_mode: ServiceMode = STORAGE,
    partition_key: Optional[] = None,
    **kwargs
) -> 

```

Initialize an AzureDocumentStore from an AAD token.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-azure/llama_index/storage/docstore/azure/base.py`  
| 
```
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
@classmethod
deffrom_aad_token(
    cls,
    endpoint: str,
    namespace: Optional[str] = None,
    node_collection_suffix: Optional[str] = None,
    ref_doc_collection_suffix: Optional[str] = None,
    metadata_collection_suffix: Optional[str] = None,
    service_mode: ServiceMode = ServiceMode.STORAGE,
    partition_key: Optional[str] = None,
    **kwargs,
) -> "AzureDocumentStore":
"""Initialize an AzureDocumentStore from an AAD token."""
    azure_kvstore = AzureKVStore.from_aad_token(
        endpoint,
        service_mode=service_mode,
        partition_key=partition_key,
    )
    return cls(
        azure_kvstore,
        namespace,
        node_collection_suffix,
        ref_doc_collection_suffix,
        metadata_collection_suffix,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  add_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/azure/#llama_index.storage.docstore.azure.AzureDocumentStore.add_documents "Permanent link")

```
add_documents(
    docs: Sequence[],
    allow_update:  = True,
    batch_size: Optional[] = None,
    store_text:  = True,
) -> None

```

Add documents to the store.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-azure/llama_index/storage/docstore/azure/base.py`  
| 
```
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
defadd_documents(
    self,
    docs: Sequence[BaseNode],
    allow_update: bool = True,
    batch_size: Optional[int] = None,
    store_text: bool = True,
) -> None:
"""Add documents to the store."""
    batch_size = batch_size or self._batch_size

    node_kv_pairs, metadata_kv_pairs, ref_doc_kv_pairs = super()._prepare_kv_pairs(
        docs, allow_update, store_text
    )

    # Change ref_doc_kv_pairs
    ref_doc_kv_pairs = self._extract_doc_metadatas(ref_doc_kv_pairs)

    self._kvstore.put_all(
        node_kv_pairs,
        collection=self._node_collection,
        batch_size=batch_size,
    )

    self._kvstore.put_all(
        metadata_kv_pairs,
        collection=self._metadata_collection,
        batch_size=batch_size,
    )

    self._kvstore.put_all(
        ref_doc_kv_pairs,
        collection=self._ref_doc_collection,
        batch_size=batch_size,
    )

```
 |  
| --- | --- |  
###  async_add_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/azure/#llama_index.storage.docstore.azure.AzureDocumentStore.async_add_documents "Permanent link")

```
async_add_documents(
    docs: Sequence[],
    allow_update:  = True,
    batch_size: Optional[] = None,
    store_text:  = True,
) -> None

```

Add documents to the store.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-azure/llama_index/storage/docstore/azure/base.py`  
| 
```
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
```
 | 
```
async defasync_add_documents(
    self,
    docs: Sequence[BaseNode],
    allow_update: bool = True,
    batch_size: Optional[int] = None,
    store_text: bool = True,
) -> None:
"""Add documents to the store."""
    batch_size = batch_size or self._batch_size

    (
        node_kv_pairs,
        metadata_kv_pairs,
        ref_doc_kv_pairs,
    ) = await super()._async_prepare_kv_pairs(docs, allow_update, store_text)

    # Change ref_doc_kv_pairs
    ref_doc_kv_pairs = self._extract_doc_metadatas(ref_doc_kv_pairs)

    await asyncio.gather(
        self._kvstore.aput_all(
            node_kv_pairs,
            collection=self._node_collection,
            batch_size=batch_size,
        ),
        self._kvstore.aput_all(
            metadata_kv_pairs,
            collection=self._metadata_collection,
            batch_size=batch_size,
        ),
        self._kvstore.aput_all(
            ref_doc_kv_pairs,
            collection=self._ref_doc_collection,
            batch_size=batch_size,
        ),
    )

```
 |  
| --- | --- |  
###  get_ref_doc_info [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/azure/#llama_index.storage.docstore.azure.AzureDocumentStore.get_ref_doc_info "Permanent link")

```
get_ref_doc_info(ref_doc_id: ) -> Optional[]

```

Get the RefDocInfo for a given ref_doc_id.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-azure/llama_index/storage/docstore/azure/base.py`  
| 
```
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
```
 | 
```
defget_ref_doc_info(self, ref_doc_id: str) -> Optional[RefDocInfo]:
"""Get the RefDocInfo for a given ref_doc_id."""
    ref_doc_infos = self._kvstore.query(
        f"PartitionKey eq '{self._kvstore.partition_key}' and ref_doc_id eq '{ref_doc_id}'",
        self._metadata_collection,
        select="RowKey",
    )

    node_ids = [doc["RowKey"] for doc in ref_doc_infos]
    if not node_ids:
        return None

    doc_metadata = self._kvstore.get(
        ref_doc_id, collection=self._ref_doc_collection, select="metadata"
    )

    ref_doc_info_dict = {
        "node_ids": node_ids,
        "metadata": doc_metadata.get("metadata"),
    }

    # TODO: deprecated legacy support
    return self._remove_legacy_info(ref_doc_info_dict)

```
 |  
| --- | --- |  
###  aget_ref_doc_info [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/azure/#llama_index.storage.docstore.azure.AzureDocumentStore.aget_ref_doc_info "Permanent link")

```
aget_ref_doc_info(ref_doc_id: ) -> Optional[]

```

Get the RefDocInfo for a given ref_doc_id.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-azure/llama_index/storage/docstore/azure/base.py`  
| 
```
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
```
 | 
```
async defaget_ref_doc_info(self, ref_doc_id: str) -> Optional[RefDocInfo]:
"""Get the RefDocInfo for a given ref_doc_id."""
    metadatas = await self._kvstore.aquery(
        f"PartitionKey eq '{self._kvstore.partition_key}' and RowKey eq '{ref_doc_id}'",
        self._metadata_collection,
        select="RowKey",
    )

    node_ids = [metadata["RowKey"] async for metadata in metadatas]

    if not node_ids:
        return None

    doc_metadata = await self._kvstore.aget(
        ref_doc_id, collection=self._ref_doc_collection, select="metadata"
    )

    ref_doc_info_dict = {
        "node_ids": node_ids,
        "metadata": doc_metadata.get("metadata") if doc_metadata else None,
    }

    # TODO: deprecated legacy support
    return self._remove_legacy_info(ref_doc_info_dict)

```
 |  
| --- | --- |  
###  get_all_ref_doc_info [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/azure/#llama_index.storage.docstore.azure.AzureDocumentStore.get_all_ref_doc_info "Permanent link")

```
get_all_ref_doc_info() -> Optional[[, ]]

```

Get a mapping of ref_doc_id -> RefDocInfo for all ingested documents.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-azure/llama_index/storage/docstore/azure/base.py`  
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
342
343
344
345
346
347
348
349
350
```
 | 
```
defget_all_ref_doc_info(self) -> Optional[Dict[str, RefDocInfo]]:
"""
    Get a mapping of ref_doc_id -> RefDocInfo for all ingested documents.
    """
    ref_doc_infos = self._kvstore.query(
        f"PartitionKey eq '{self._kvstore.partition_key}'",
        self._metadata_collection,
        select=["RowKey", "ref_doc_id"],
    )

    # TODO: deprecated legacy support
    all_ref_doc_infos = defaultdict(lambda: {"node_ids": [], "metadata": None})
    for ref_doc_info in ref_doc_infos:
        ref_doc_id = ref_doc_info["ref_doc_id"]
        ref_doc_info_dict = all_ref_doc_infos[ref_doc_id]
        ref_doc_info_dict["node_ids"].append(ref_doc_info["RowKey"])

        if ref_doc_info_dict["metadata"] is None:
            ref_doc = self._kvstore.get(
                ref_doc_id, collection=self._ref_doc_collection, select="metadata"
            )
            ref_doc_info_dict["metadata"] = ref_doc.get("metadata")

    for ref_doc_id, ref_doc_info_dict in all_ref_doc_infos.items():
        all_ref_doc_infos[ref_doc_id] = self._remove_legacy_info(ref_doc_info_dict)

    return all_ref_doc_infos

```
 |  
| --- | --- |  
###  aget_all_ref_doc_info [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/azure/#llama_index.storage.docstore.azure.AzureDocumentStore.aget_all_ref_doc_info "Permanent link")

```
aget_all_ref_doc_info() -> Optional[[, ]]

```

Get a mapping of ref_doc_id -> RefDocInfo for all ingested documents.
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-azure/llama_index/storage/docstore/azure/base.py`  
| 
```
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
async defaget_all_ref_doc_info(self) -> Optional[Dict[str, RefDocInfo]]:
"""
    Get a mapping of ref_doc_id -> RefDocInfo for all ingested documents.
    """
    ref_doc_infos = await self._kvstore.aquery(
        f"PartitionKey eq '{self._kvstore.partition_key}'",
        self._metadata_collection,
        select=["RowKey", "ref_doc_id"],
    )

    # TODO: deprecated legacy support
    all_ref_doc_infos = defaultdict(lambda: {"node_ids": [], "metadata": None})
    async for ref_doc_info in ref_doc_infos:
        ref_doc_id = ref_doc_info["ref_doc_id"]
        ref_doc_info_dict = all_ref_doc_infos[ref_doc_id]
        ref_doc_info_dict["node_ids"].append(ref_doc_info["RowKey"])

        if ref_doc_info_dict["metadata"] is None:
            ref_doc = await self._kvstore.aget(
                ref_doc_id, collection=self._ref_doc_collection, select="metadata"
            )
            ref_doc_info_dict["metadata"] = ref_doc.get("metadata")

    for ref_doc_id, ref_doc_info_dict in all_ref_doc_infos.items():
        all_ref_doc_infos[ref_doc_id] = self._remove_legacy_info(ref_doc_info_dict)

    return all_ref_doc_infos

```
 |  
| --- | --- |  
options: members: - AzureDocumentStore
