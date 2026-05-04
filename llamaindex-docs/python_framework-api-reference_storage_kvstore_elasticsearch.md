# Elasticsearch
##  ElasticsearchKVStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/elasticsearch/#llama_index.storage.kvstore.elasticsearch.ElasticsearchKVStore "Permanent link")
Bases: 
Elasticsearch Key-Value store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index_name`  |  Name of the Elasticsearch index.  |  _required_  |  
|  `es_client`  |  `Optional[Any]`  |  Optional. Pre-existing AsyncElasticsearch client.  |  _required_  |  
|  `es_url`  |  `Optional[str]`  |  Optional. Elasticsearch URL.  |  `None`  |  
|  `es_cloud_id`  |  `Optional[str]`  |  Optional. Elasticsearch cloud ID.  |  `None`  |  
|  `es_api_key`  |  `Optional[str]`  |  Optional. Elasticsearch API key.  |  `None`  |  
|  `es_user`  |  `Optional[str]`  |  Optional. Elasticsearch username.  |  `None`  |  
|  `es_password`  |  `Optional[str]`  |  Optional. Elasticsearch password.  |  `None`  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ConnectionError`  |  If AsyncElasticsearch client cannot connect to Elasticsearch.  |  
|  `ValueError`  |  If neither es_client nor es_url nor es_cloud_id is provided.  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-elasticsearch/llama_index/storage/kvstore/elasticsearch/base.py`  
| 
```
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
```
 | 
```
classElasticsearchKVStore(BaseKVStore):
"""
    Elasticsearch Key-Value store.

    Args:
        index_name: Name of the Elasticsearch index.
        es_client: Optional. Pre-existing AsyncElasticsearch client.
        es_url: Optional. Elasticsearch URL.
        es_cloud_id: Optional. Elasticsearch cloud ID.
        es_api_key: Optional. Elasticsearch API key.
        es_user: Optional. Elasticsearch username.
        es_password: Optional. Elasticsearch password.


    Raises:
        ConnectionError: If AsyncElasticsearch client cannot connect to Elasticsearch.
        ValueError: If neither es_client nor es_url nor es_cloud_id is provided.

    """

    es_client: Optional[Any]
    es_url: Optional[str]
    es_cloud_id: Optional[str]
    es_api_key: Optional[str]
    es_user: Optional[str]
    es_password: Optional[str]

    def__init__(
        self,
        index_name: str,
        es_client: Optional[Any],
        es_url: Optional[str] = None,
        es_cloud_id: Optional[str] = None,
        es_api_key: Optional[str] = None,
        es_user: Optional[str] = None,
        es_password: Optional[str] = None,
    ) -> None:
        nest_asyncio.apply()

"""Init a ElasticsearchKVStore."""
        try:
            fromelasticsearchimport AsyncElasticsearch
        except ImportError:
            raise ImportError(IMPORT_ERROR_MSG)

        if es_client is not None:
            self._client = es_client.options(
                headers={"user-agent": self.get_user_agent()}
            )
        elif es_url is not None or es_cloud_id is not None:
            self._client: AsyncElasticsearch = _get_elasticsearch_client(
                es_url=es_url,
                username=es_user,
                password=es_password,
                cloud_id=es_cloud_id,
                api_key=es_api_key,
            )
        else:
            raise ValueError(
"""Either provide a pre-existing AsyncElasticsearch or valid \
                credentials for creating a new connection."""
            )

    @property
    defclient(self) -> Any:
"""Get async elasticsearch client."""
        return self._client

    @staticmethod
    defget_user_agent() -> str:
"""Get user agent for elasticsearch client."""
        return "llama_index-py-vs"

    async def_create_index_if_not_exists(self, index_name: str) -> None:
"""
        Create the AsyncElasticsearch index if it doesn't already exist.

        Args:
            index_name: Name of the AsyncElasticsearch index to create.

        """
        if await self.client.indices.exists(index=index_name):
            logger.debug(f"Index {index_name} already exists. Skipping creation.")

        else:
            index_settings = {"mappings": {"_source": {"enabled": True}}}

            logger.debug(
                f"Creating index {index_name} with mappings {index_settings['mappings']}"
            )
            await self.client.indices.create(index=index_name, **index_settings)

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
        self.put_all([(key, val)], collection=collection)

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
        await self.aput_all([(key, val)], collection=collection)

    defput_all(
        self,
        kv_pairs: List[Tuple[str, dict]],
        collection: str = DEFAULT_COLLECTION,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
        return asyncio.get_event_loop().run_until_complete(
            self.aput_all(kv_pairs, collection, batch_size)
        )

    async defaput_all(
        self,
        kv_pairs: List[Tuple[str, dict]],
        collection: str = DEFAULT_COLLECTION,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
        await self._create_index_if_not_exists(collection)

        # Prepare documents with '_id' set to the key for batch insertion
        docs = [{"_id": key, **value} for key, value in kv_pairs]

        # Insert documents in batches
        for batch in (
            docs[i : i + batch_size] for i in range(0, len(docs), batch_size)
        ):
            requests = []
            for doc in batch:
                doc_id = doc["_id"]
                doc.pop("_id")
                logger.debug(doc)
                request = {
                    "_op_type": "index",
                    "_index": collection,
                    **doc,
                    "_id": doc_id,
                }
                requests.append(request)
            await async_bulk(self.client, requests, chunk_size=batch_size, refresh=True)

    defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> Optional[dict]:
"""
        Get a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        return asyncio.get_event_loop().run_until_complete(self.aget(key, collection))

    async defaget(
        self, key: str, collection: str = DEFAULT_COLLECTION
    ) -> Optional[dict]:
"""
        Get a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        await self._create_index_if_not_exists(collection)

        try:
            response = await self._client.get(index=collection, id=key, source=True)
            return response.body["_source"]
        except elasticsearch.NotFoundError:
            return None

    defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
        Get all values from the store.

        Args:
            collection (str): collection name

        """
        return asyncio.get_event_loop().run_until_complete(self.aget_all(collection))

    async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
        Get all values from the store.

        Args:
            collection (str): collection name

        """
        await self._create_index_if_not_exists(collection)

        result = {}
        q = {"query": {"match_all": {}}}
        async for doc in async_scan(client=self._client, index=collection, query=q):
            doc_id = doc["_id"]
            content = doc["_source"]
            result[doc_id] = content
        return result

    defdelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
        Delete a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        return asyncio.get_event_loop().run_until_complete(
            self.adelete(key, collection)
        )

    async defadelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
        Delete a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        await self._create_index_if_not_exists(collection)

        try:
            response = await self._client.delete(index=collection, id=key)
            return response.body["result"] == "deleted"
        except elasticsearch.NotFoundError:
            return False

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/elasticsearch/#llama_index.storage.kvstore.elasticsearch.ElasticsearchKVStore.client "Permanent link")

```
client: 

```

Get async elasticsearch client.
###  get_user_agent `staticmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/elasticsearch/#llama_index.storage.kvstore.elasticsearch.ElasticsearchKVStore.get_user_agent "Permanent link")

```
get_user_agent() -> 

```

Get user agent for elasticsearch client.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-elasticsearch/llama_index/storage/kvstore/elasticsearch/base.py`  
| 
```
148
149
150
151
```
 | 
```
@staticmethod
defget_user_agent() -> str:
"""Get user agent for elasticsearch client."""
    return "llama_index-py-vs"

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/elasticsearch/#llama_index.storage.kvstore.elasticsearch.ElasticsearchKVStore.put "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-elasticsearch/llama_index/storage/kvstore/elasticsearch/base.py`  
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
    self.put_all([(key, val)], collection=collection)

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/elasticsearch/#llama_index.storage.kvstore.elasticsearch.ElasticsearchKVStore.aput "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-elasticsearch/llama_index/storage/kvstore/elasticsearch/base.py`  
| 
```
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
    await self.aput_all([(key, val)], collection=collection)

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/elasticsearch/#llama_index.storage.kvstore.elasticsearch.ElasticsearchKVStore.get "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-elasticsearch/llama_index/storage/kvstore/elasticsearch/base.py`  
| 
```
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
    return asyncio.get_event_loop().run_until_complete(self.aget(key, collection))

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/elasticsearch/#llama_index.storage.kvstore.elasticsearch.ElasticsearchKVStore.aget "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-elasticsearch/llama_index/storage/kvstore/elasticsearch/base.py`  
| 
```
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
async defaget(
    self, key: str, collection: str = DEFAULT_COLLECTION
) -> Optional[dict]:
"""
    Get a value from the store.

    Args:
        key (str): key
        collection (str): collection name

    """
    await self._create_index_if_not_exists(collection)

    try:
        response = await self._client.get(index=collection, id=key, source=True)
        return response.body["_source"]
    except elasticsearch.NotFoundError:
        return None

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/elasticsearch/#llama_index.storage.kvstore.elasticsearch.ElasticsearchKVStore.get_all "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-elasticsearch/llama_index/storage/kvstore/elasticsearch/base.py`  
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
```
 | 
```
defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
    Get all values from the store.

    Args:
        collection (str): collection name

    """
    return asyncio.get_event_loop().run_until_complete(self.aget_all(collection))

```
 |  
| --- | --- |  
###  aget_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/elasticsearch/#llama_index.storage.kvstore.elasticsearch.ElasticsearchKVStore.aget_all "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-elasticsearch/llama_index/storage/kvstore/elasticsearch/base.py`  
| 
```
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
```
 | 
```
async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
    Get all values from the store.

    Args:
        collection (str): collection name

    """
    await self._create_index_if_not_exists(collection)

    result = {}
    q = {"query": {"match_all": {}}}
    async for doc in async_scan(client=self._client, index=collection, query=q):
        doc_id = doc["_id"]
        content = doc["_source"]
        result[doc_id] = content
    return result

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/elasticsearch/#llama_index.storage.kvstore.elasticsearch.ElasticsearchKVStore.delete "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-elasticsearch/llama_index/storage/kvstore/elasticsearch/base.py`  
| 
```
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
defdelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
    Delete a value from the store.

    Args:
        key (str): key
        collection (str): collection name

    """
    return asyncio.get_event_loop().run_until_complete(
        self.adelete(key, collection)
    )

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/elasticsearch/#llama_index.storage.kvstore.elasticsearch.ElasticsearchKVStore.adelete "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-elasticsearch/llama_index/storage/kvstore/elasticsearch/base.py`  
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
    await self._create_index_if_not_exists(collection)

    try:
        response = await self._client.delete(index=collection, id=key)
        return response.body["result"] == "deleted"
    except elasticsearch.NotFoundError:
        return False

```
 |  
| --- | --- |  
options: members: - ElasticsearchKVStore
