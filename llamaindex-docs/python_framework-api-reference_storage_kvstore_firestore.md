# Firestore
##  FirestoreKVStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/firestore/#llama_index.storage.kvstore.firestore.FirestoreKVStore "Permanent link")
Bases: 
Firestore Key-Value store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `project`  |  The project which the client acts on behalf of.  |  `None`  |  
|  `database`  |  The database name that the client targets.  |  `DEFAULT_FIRESTORE_DATABASE`  |  
|  `credentials`  |  `Credentials`  |  The OAuth2 Credentials to access Firestore. If not passed, falls back to the default inferred from the environment.  |  `None`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-firestore/llama_index/storage/kvstore/firestore/base.py`  
| 
```
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
```
 | 
```
classFirestoreKVStore(BaseKVStore):
"""
    Firestore Key-Value store.

    Args:
        project (str): The project which the client acts on behalf of.
        database (str): The database name that the client targets.
        credentials (google.auth.credentials.Credentials): The OAuth2
            Credentials to access Firestore. If not passed, falls back
            to the default inferred from the environment.

    """

    def__init__(
        self,
        project: Optional[str] = None,
        database: str = DEFAULT_FIRESTORE_DATABASE,
        credentials: Optional[Credentials] = None,
    ) -> None:
        client_info = DEFAULT_CLIENT_INFO
        client_info.user_agent = USER_AGENT
        self._adb = AsyncClient(
            project=project,
            database=database,
            client_info=client_info,
            credentials=credentials,
        )
        self._db = Client(
            project=project,
            database=database,
            client_info=client_info,
            credentials=credentials,
        )

    deffirestore_collection(self, collection: str) -> str:
        return collection.replace("/", SLASH_REPLACEMENT)

    defreplace_field_name_set(self, val: Dict[str, Any]) -> Dict[str, Any]:
        val = val.copy()
        for k, v in FIELD_NAME_REPLACE_SET.items():
            if k in val:
                val[v] = val[k]
                val.pop(k)
        return val

    defreplace_field_name_get(self, val: Dict[str, Any]) -> Dict[str, Any]:
        val = val.copy()
        for k, v in FIELD_NAME_REPLACE_GET.items():
            if k in val:
                val[v] = val[k]
                val.pop(k)
        return val

    defput(
        self,
        key: str,
        val: dict,
        collection: str = DEFAULT_COLLECTION,
    ) -> None:
"""
        Put a key-value pair into the Firestore collection.

        Args:
            key (str): key
            val (dict): value
            collection (str): collection name

        """
        collection_id = self.firestore_collection(collection)
        val = self.replace_field_name_set(val)
        doc = self._db.collection(collection_id).document(key)
        doc.set(val, merge=True)

    async defaput(
        self,
        key: str,
        val: dict,
        collection: str = DEFAULT_COLLECTION,
    ) -> None:
"""
        Put a key-value pair into the Firestore collection.

        Args:
            key (str): key
            val (dict): value
            collection (str): collection name

        """
        collection_id = self.firestore_collection(collection)
        val = self.replace_field_name_set(val)
        doc = self._adb.collection(collection_id).document(key)
        await doc.set(val, merge=True)

    defput_all(
        self,
        kv_pairs: List[Tuple[str, dict]],
        collection: str = DEFAULT_COLLECTION,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
        batch = self._db.batch()
        for i, (key, val) in enumerate(kv_pairs, start=1):
            collection_id = self.firestore_collection(collection)
            val = self.replace_field_name_set(val)
            batch.set(self._db.collection(collection_id).document(key), val, merge=True)
            if i % batch_size == 0:
                batch.commit()
                batch = self._db.batch()
        batch.commit()

    async defaput_all(
        self,
        kv_pairs: List[Tuple[str, dict]],
        collection: str = DEFAULT_COLLECTION,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
"""
        Put a dictionary of key-value pairs into the Firestore collection.

        Args:
            kv_pairs (List[Tuple[str, dict]]): key-value pairs
            collection (str): collection name

        """
        batch = self._adb.batch()
        for i, (key, val) in enumerate(kv_pairs, start=1):
            collection_id = self.firestore_collection(collection)
            doc = self._adb.collection(collection_id).document(key)
            val = self.replace_field_name_set(val)
            batch.set(doc, val, merge=True)
            if i % batch_size == 0:
                await batch.commit()
                batch = self._adb.batch()
        await batch.commit()

    defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> Optional[dict]:
"""
        Get a key-value pair from the Firestore.

        Args:
            key (str): key
            collection (str): collection name

        """
        collection_id = self.firestore_collection(collection)
        result = self._db.collection(collection_id).document(key).get().to_dict()
        if not result:
            return None

        return self.replace_field_name_get(result)

    async defaget(
        self, key: str, collection: str = DEFAULT_COLLECTION
    ) -> Optional[dict]:
"""
        Get a key-value pair from the Firestore.

        Args:
            key (str): key
            collection (str): collection name

        """
        collection_id = self.firestore_collection(collection)
        result = (
            await self._adb.collection(collection_id).document(key).get()
        ).to_dict()
        if not result:
            return None

        return self.replace_field_name_get(result)

    defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
        Get all values from the Firestore collection.

        Args:
            collection (str): collection name

        """
        collection_id = self.firestore_collection(collection)
        docs = self._db.collection(collection_id).list_documents()
        output = {}
        for doc in docs:
            key = doc.id
            val = self.replace_field_name_get(doc.get().to_dict())
            output[key] = val
        return output

    async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
        Get all values from the Firestore collection.

        Args:
            collection (str): collection name

        """
        collection_id = self.firestore_collection(collection)
        docs = self._adb.collection(collection_id).list_documents()
        output = {}
        async for doc in docs:
            key = doc.id
            data = (await doc.get()).to_dict()
            if data is None:
                continue
            val = self.replace_field_name_get(data)
            output[key] = val
        return output

    defdelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
        Delete a value from the Firestore.

        Args:
            key (str): key
            collection (str): collection name

        """
        collection_id = self.firestore_collection(collection)
        doc = self._db.collection(collection_id).document(key)
        doc.delete()
        return True

    async defadelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
        Delete a value from the Firestore.

        Args:
            key (str): key
            collection (str): collection name

        """
        collection_id = self.firestore_collection(collection)
        doc = self._adb.collection(collection_id).document(key)
        await doc.delete()
        return True

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/firestore/#llama_index.storage.kvstore.firestore.FirestoreKVStore.put "Permanent link")

```
put(
    key: ,
    val: ,
    collection:  = DEFAULT_COLLECTION,
) -> None

```

Put a key-value pair into the Firestore collection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  _required_  |  
|  `val`  |  `dict`  |  value  |  _required_  |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-firestore/llama_index/storage/kvstore/firestore/base.py`  
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
89
90
91
92
93
94
95
96
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
    Put a key-value pair into the Firestore collection.

    Args:
        key (str): key
        val (dict): value
        collection (str): collection name

    """
    collection_id = self.firestore_collection(collection)
    val = self.replace_field_name_set(val)
    doc = self._db.collection(collection_id).document(key)
    doc.set(val, merge=True)

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/firestore/#llama_index.storage.kvstore.firestore.FirestoreKVStore.aput "Permanent link")

```
aput(
    key: ,
    val: ,
    collection:  = DEFAULT_COLLECTION,
) -> None

```

Put a key-value pair into the Firestore collection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  _required_  |  
|  `val`  |  `dict`  |  value  |  _required_  |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-firestore/llama_index/storage/kvstore/firestore/base.py`  
| 
```
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
    Put a key-value pair into the Firestore collection.

    Args:
        key (str): key
        val (dict): value
        collection (str): collection name

    """
    collection_id = self.firestore_collection(collection)
    val = self.replace_field_name_set(val)
    doc = self._adb.collection(collection_id).document(key)
    await doc.set(val, merge=True)

```
 |  
| --- | --- |  
###  aput_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/firestore/#llama_index.storage.kvstore.firestore.FirestoreKVStore.aput_all "Permanent link")

```
aput_all(
    kv_pairs: [Tuple[, ]],
    collection:  = DEFAULT_COLLECTION,
    batch_size:  = DEFAULT_BATCH_SIZE,
) -> None

```

Put a dictionary of key-value pairs into the Firestore collection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `kv_pairs`  |  `List[Tuple[str, dict]]`  |  key-value pairs  |  _required_  |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-firestore/llama_index/storage/kvstore/firestore/base.py`  
| 
```
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
    Put a dictionary of key-value pairs into the Firestore collection.

    Args:
        kv_pairs (List[Tuple[str, dict]]): key-value pairs
        collection (str): collection name

    """
    batch = self._adb.batch()
    for i, (key, val) in enumerate(kv_pairs, start=1):
        collection_id = self.firestore_collection(collection)
        doc = self._adb.collection(collection_id).document(key)
        val = self.replace_field_name_set(val)
        batch.set(doc, val, merge=True)
        if i % batch_size == 0:
            await batch.commit()
            batch = self._adb.batch()
    await batch.commit()

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/firestore/#llama_index.storage.kvstore.firestore.FirestoreKVStore.get "Permanent link")

```
get(
    key: , collection:  = DEFAULT_COLLECTION
) -> Optional[]

```

Get a key-value pair from the Firestore.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  _required_  |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-firestore/llama_index/storage/kvstore/firestore/base.py`  
| 
```
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
```
 | 
```
defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> Optional[dict]:
"""
    Get a key-value pair from the Firestore.

    Args:
        key (str): key
        collection (str): collection name

    """
    collection_id = self.firestore_collection(collection)
    result = self._db.collection(collection_id).document(key).get().to_dict()
    if not result:
        return None

    return self.replace_field_name_get(result)

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/firestore/#llama_index.storage.kvstore.firestore.FirestoreKVStore.aget "Permanent link")

```
aget(
    key: , collection:  = DEFAULT_COLLECTION
) -> Optional[]

```

Get a key-value pair from the Firestore.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  _required_  |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-firestore/llama_index/storage/kvstore/firestore/base.py`  
| 
```
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
```
 | 
```
async defaget(
    self, key: str, collection: str = DEFAULT_COLLECTION
) -> Optional[dict]:
"""
    Get a key-value pair from the Firestore.

    Args:
        key (str): key
        collection (str): collection name

    """
    collection_id = self.firestore_collection(collection)
    result = (
        await self._adb.collection(collection_id).document(key).get()
    ).to_dict()
    if not result:
        return None

    return self.replace_field_name_get(result)

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/firestore/#llama_index.storage.kvstore.firestore.FirestoreKVStore.get_all "Permanent link")

```
get_all(
    collection:  = DEFAULT_COLLECTION,
) -> [, ]

```

Get all values from the Firestore collection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-firestore/llama_index/storage/kvstore/firestore/base.py`  
| 
```
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
```
 | 
```
defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
    Get all values from the Firestore collection.

    Args:
        collection (str): collection name

    """
    collection_id = self.firestore_collection(collection)
    docs = self._db.collection(collection_id).list_documents()
    output = {}
    for doc in docs:
        key = doc.id
        val = self.replace_field_name_get(doc.get().to_dict())
        output[key] = val
    return output

```
 |  
| --- | --- |  
###  aget_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/firestore/#llama_index.storage.kvstore.firestore.FirestoreKVStore.aget_all "Permanent link")

```
aget_all(
    collection:  = DEFAULT_COLLECTION,
) -> [, ]

```

Get all values from the Firestore collection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-firestore/llama_index/storage/kvstore/firestore/base.py`  
| 
```
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
async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
    Get all values from the Firestore collection.

    Args:
        collection (str): collection name

    """
    collection_id = self.firestore_collection(collection)
    docs = self._adb.collection(collection_id).list_documents()
    output = {}
    async for doc in docs:
        key = doc.id
        data = (await doc.get()).to_dict()
        if data is None:
            continue
        val = self.replace_field_name_get(data)
        output[key] = val
    return output

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/firestore/#llama_index.storage.kvstore.firestore.FirestoreKVStore.delete "Permanent link")

```
delete(
    key: , collection:  = DEFAULT_COLLECTION
) -> 

```

Delete a value from the Firestore.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  _required_  |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-firestore/llama_index/storage/kvstore/firestore/base.py`  
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
```
 | 
```
defdelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
    Delete a value from the Firestore.

    Args:
        key (str): key
        collection (str): collection name

    """
    collection_id = self.firestore_collection(collection)
    doc = self._db.collection(collection_id).document(key)
    doc.delete()
    return True

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/firestore/#llama_index.storage.kvstore.firestore.FirestoreKVStore.adelete "Permanent link")

```
adelete(
    key: , collection:  = DEFAULT_COLLECTION
) -> 

```

Delete a value from the Firestore.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  _required_  |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-firestore/llama_index/storage/kvstore/firestore/base.py`  
| 
```
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
```
 | 
```
async defadelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
    Delete a value from the Firestore.

    Args:
        key (str): key
        collection (str): collection name

    """
    collection_id = self.firestore_collection(collection)
    doc = self._adb.collection(collection_id).document(key)
    await doc.delete()
    return True

```
 |  
| --- | --- |  
options: members: - FirestoreKVStore
