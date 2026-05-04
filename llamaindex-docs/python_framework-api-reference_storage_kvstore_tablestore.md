# Tablestore
##  TablestoreKVStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/tablestore/#llama_index.storage.kvstore.tablestore.TablestoreKVStore "Permanent link")
Bases: 
Tablestore Key-Value Store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `tablestore_client`  |  `OTSClient`  |  External tablestore(ots) client. If this parameter is set, the following endpoint/instance_name/access_key_id/access_key_secret will be ignored.  |  `None`  |  
|  `endpoint`  |  Tablestore instance endpoint.  |  `None`  |  
|  `instance_name`  |  Tablestore instance name.  |  `None`  |  
|  `access_key_id`  |  Aliyun access key id.  |  `None`  |  
|  `access_key_secret`  |  Aliyun access key secret.  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `TablestoreKVStore`  |  A Tablestore kv store object.  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-tablestore/llama_index/storage/kvstore/tablestore/base.py`  
| 
```
 13
 14
 15
 16
 17
 18
 19
 20
 21
 22
 23
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
```
 | 
```
classTablestoreKVStore(BaseKVStore):
"""
    Tablestore Key-Value Store.

    Args:
        tablestore_client (OTSClient, optional): External tablestore(ots) client.
                If this parameter is set, the following endpoint/instance_name/access_key_id/access_key_secret will be ignored.
        endpoint (str, optional): Tablestore instance endpoint.
        instance_name (str, optional): Tablestore instance name.
        access_key_id (str, optional): Aliyun access key id.
        access_key_secret (str, optional): Aliyun access key secret.

    Returns:
        TablestoreKVStore: A Tablestore kv store object.

    """

    def__init__(
        self,
        tablestore_client: Optional[tablestore.OTSClient] = None,
        endpoint: Optional[str] = None,
        instance_name: Optional[str] = None,
        access_key_id: Optional[str] = None,
        access_key_secret: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__()
        if not tablestore_client:
            self._tablestore_client = tablestore.OTSClient(
                endpoint,
                access_key_id,
                access_key_secret,
                instance_name,
                retry_policy=tablestore.WriteRetryPolicy(),
                **kwargs,  # pass additional arguments
            )
        else:
            self._tablestore_client = tablestore_client

        self._update_collection()

    @staticmethod
    def_flatten_dict_to_json_strings(original_dict) -> dict:
        result_dict = {}
        for key, value in original_dict.items():
            if isinstance(
                value, (bool, bytearray, float, int, six.binary_type, six.text_type)
            ):
                result_dict[key] = value
            else:
                result_dict[key] = json.dumps(value, ensure_ascii=False)
        return result_dict

    def_update_collection(self) -> List[str]:
"""Update collection."""
        self._collections = self._tablestore_client.list_table()
        return self._collections

    def_create_collection_if_not_exist(self, collection: str) -> None:
"""Create table if not exist."""
        if collection in self._collections:
            return

        table_list = self._tablestore_client.list_table()
        if collection in table_list:
            logger.info(f"Tablestore kv store table[{collection}] already exists")
            return
        logger.info(
            f"Tablestore kv store table[{collection}] does not exist, try to create the table.",
        )

        table_meta = tablestore.TableMeta(collection, [("pk", "STRING")])
        reserved_throughput = tablestore.ReservedThroughput(
            tablestore.CapacityUnit(0, 0)
        )
        self._tablestore_client.create_table(
            table_meta, tablestore.TableOptions(), reserved_throughput
        )
        self._update_collection()
        sleep(5)
        logger.info(f"Tablestore create kv store table[{collection}] successfully.")

    defput(self, key: str, val: dict, collection: str = DEFAULT_COLLECTION) -> None:
"""
        Put a key-value pair into the store.

        Args:
            key (str): key
            val (dict): value
            collection (str): collection name

        """
        val = self._flatten_dict_to_json_strings(val)
        self._create_collection_if_not_exist(collection)
        primary_key = [("pk", key)]
        attribute_columns = list(val.items())
        row = tablestore.Row(primary_key, attribute_columns)
        self._tablestore_client.put_row(collection, row)

    async defaput(
        self, key: str, val: dict, collection: str = DEFAULT_COLLECTION
    ) -> None:
"""
        Put a key-value pair into the store.

        Args:
            key (str): key
            val (dict): value
            collection (str): collection name

        """
        raise NotImplementedError

    defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> Optional[dict]:
"""
        Get a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        self._create_collection_if_not_exist(collection)
        primary_key = [("pk", key)]
        try:
            _, row, _ = self._tablestore_client.get_row(
                collection, primary_key, None, None, 1
            )
            if row is None:
                return None
            return self._parse_row(row)
        except tablestore.OTSServiceError as e:
            logger.error(
                f"get row failed, http_status:{e.get_http_status()}, error_code:{e.get_error_code()}, error_message:{e.get_error_message()}, request_id:{e.get_request_id()}"
            )
            if (
                e.get_error_code() == "OTSParameterInvalid"
                and "table not exist" in e.get_error_message()
            ):
                return None

    async defaget(
        self, key: str, collection: str = DEFAULT_COLLECTION
    ) -> Optional[dict]:
"""
        Get a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        raise NotImplementedError

    defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
        Get all values from the store.

        Args:
            collection (str): collection name

        """
        self._create_collection_if_not_exist(collection)
        inclusive_start_primary_key = [("pk", tablestore.INF_MIN)]
        exclusive_end_primary_key = [("pk", tablestore.INF_MAX)]
        limit = 5000
        columns_to_get = []
        (
            consumed,
            next_start_primary_key,
            row_list,
            next_token,
        ) = self._tablestore_client.get_range(
            collection,
            tablestore.Direction.FORWARD,
            inclusive_start_primary_key,
            exclusive_end_primary_key,
            columns_to_get,
            limit,
            max_version=1,
        )
        ret_dict = {}
        self._parse_rows(ret_dict, row_list)
        while next_start_primary_key is not None:
            inclusive_start_primary_key = next_start_primary_key
            (
                consumed,
                next_start_primary_key,
                row_list,
                next_token,
            ) = self._tablestore_client.get_range(
                collection,
                tablestore.Direction.FORWARD,
                inclusive_start_primary_key,
                exclusive_end_primary_key,
                columns_to_get,
                limit,
                max_version=1,
            )
            self._parse_rows(ret_dict, row_list)

        return ret_dict

    def_parse_rows(self, return_result: dict, row_list: Optional[list]) -> None:
        if row_list:
            for row in row_list:
                ret = self._parse_row(row)
                return_result[row.primary_key[0][1]] = ret

    def_delete_rows(self, row_list: Optional[list], collection: str) -> None:
        if row_list:
            for row in row_list:
                key = row.primary_key[0][1]
                self.delete(key=key, collection=collection)

    @staticmethod
    def_parse_row(row: Any) -> dict[str, Any]:
        ret = {}
        for col in row.attribute_columns:
            k = col[0]
            v = col[1]
            if isinstance(v, str):
                try:
                    ret[k] = json.loads(v)
                    if not (isinstance(ret[k], (dict, list, tuple))):
                        ret[k] = v
                except json.JSONDecodeError:
                    ret[k] = v
            else:
                ret[k] = v
        return ret

    async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
        Get all values from the store.

        Args:
            collection (str): collection name

        """
        raise NotImplementedError

    defdelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
        Delete a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        primary_key = [("pk", key)]
        _, return_row = self._tablestore_client.delete_row(
            collection, primary_key, None
        )
        return True

    async defadelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
        Delete a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        raise NotImplementedError

    # noinspection DuplicatedCode
    defdelete_all(self, collection: str = DEFAULT_COLLECTION) -> None:
        self._create_collection_if_not_exist(collection)
        inclusive_start_primary_key = [("pk", tablestore.INF_MIN)]
        exclusive_end_primary_key = [("pk", tablestore.INF_MAX)]
        limit = 5000
        columns_to_get = []
        (
            consumed,
            next_start_primary_key,
            row_list,
            next_token,
        ) = self._tablestore_client.get_range(
            collection,
            tablestore.Direction.FORWARD,
            inclusive_start_primary_key,
            exclusive_end_primary_key,
            columns_to_get,
            limit,
            max_version=1,
        )
        ret_dict = {}
        self._delete_rows(row_list, collection)
        while next_start_primary_key is not None:
            inclusive_start_primary_key = next_start_primary_key
            (
                consumed,
                next_start_primary_key,
                row_list,
                next_token,
            ) = self._tablestore_client.get_range(
                collection,
                tablestore.Direction.FORWARD,
                inclusive_start_primary_key,
                exclusive_end_primary_key,
                columns_to_get,
                limit,
                max_version=1,
            )
            self._delete_rows(row_list, collection)

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/tablestore/#llama_index.storage.kvstore.tablestore.TablestoreKVStore.put "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-tablestore/llama_index/storage/kvstore/tablestore/base.py`  
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
```
 | 
```
defput(self, key: str, val: dict, collection: str = DEFAULT_COLLECTION) -> None:
"""
    Put a key-value pair into the store.

    Args:
        key (str): key
        val (dict): value
        collection (str): collection name

    """
    val = self._flatten_dict_to_json_strings(val)
    self._create_collection_if_not_exist(collection)
    primary_key = [("pk", key)]
    attribute_columns = list(val.items())
    row = tablestore.Row(primary_key, attribute_columns)
    self._tablestore_client.put_row(collection, row)

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/tablestore/#llama_index.storage.kvstore.tablestore.TablestoreKVStore.aput "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-tablestore/llama_index/storage/kvstore/tablestore/base.py`  
| 
```
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
```
 | 
```
async defaput(
    self, key: str, val: dict, collection: str = DEFAULT_COLLECTION
) -> None:
"""
    Put a key-value pair into the store.

    Args:
        key (str): key
        val (dict): value
        collection (str): collection name

    """
    raise NotImplementedError

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/tablestore/#llama_index.storage.kvstore.tablestore.TablestoreKVStore.get "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-tablestore/llama_index/storage/kvstore/tablestore/base.py`  
| 
```
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
    self._create_collection_if_not_exist(collection)
    primary_key = [("pk", key)]
    try:
        _, row, _ = self._tablestore_client.get_row(
            collection, primary_key, None, None, 1
        )
        if row is None:
            return None
        return self._parse_row(row)
    except tablestore.OTSServiceError as e:
        logger.error(
            f"get row failed, http_status:{e.get_http_status()}, error_code:{e.get_error_code()}, error_message:{e.get_error_message()}, request_id:{e.get_request_id()}"
        )
        if (
            e.get_error_code() == "OTSParameterInvalid"
            and "table not exist" in e.get_error_message()
        ):
            return None

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/tablestore/#llama_index.storage.kvstore.tablestore.TablestoreKVStore.aget "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-tablestore/llama_index/storage/kvstore/tablestore/base.py`  
| 
```
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
    raise NotImplementedError

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/tablestore/#llama_index.storage.kvstore.tablestore.TablestoreKVStore.get_all "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-tablestore/llama_index/storage/kvstore/tablestore/base.py`  
| 
```
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
```
 | 
```
defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
    Get all values from the store.

    Args:
        collection (str): collection name

    """
    self._create_collection_if_not_exist(collection)
    inclusive_start_primary_key = [("pk", tablestore.INF_MIN)]
    exclusive_end_primary_key = [("pk", tablestore.INF_MAX)]
    limit = 5000
    columns_to_get = []
    (
        consumed,
        next_start_primary_key,
        row_list,
        next_token,
    ) = self._tablestore_client.get_range(
        collection,
        tablestore.Direction.FORWARD,
        inclusive_start_primary_key,
        exclusive_end_primary_key,
        columns_to_get,
        limit,
        max_version=1,
    )
    ret_dict = {}
    self._parse_rows(ret_dict, row_list)
    while next_start_primary_key is not None:
        inclusive_start_primary_key = next_start_primary_key
        (
            consumed,
            next_start_primary_key,
            row_list,
            next_token,
        ) = self._tablestore_client.get_range(
            collection,
            tablestore.Direction.FORWARD,
            inclusive_start_primary_key,
            exclusive_end_primary_key,
            columns_to_get,
            limit,
            max_version=1,
        )
        self._parse_rows(ret_dict, row_list)

    return ret_dict

```
 |  
| --- | --- |  
###  aget_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/tablestore/#llama_index.storage.kvstore.tablestore.TablestoreKVStore.aget_all "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-tablestore/llama_index/storage/kvstore/tablestore/base.py`  
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
```
 | 
```
async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
    Get all values from the store.

    Args:
        collection (str): collection name

    """
    raise NotImplementedError

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/tablestore/#llama_index.storage.kvstore.tablestore.TablestoreKVStore.delete "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-tablestore/llama_index/storage/kvstore/tablestore/base.py`  
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
    primary_key = [("pk", key)]
    _, return_row = self._tablestore_client.delete_row(
        collection, primary_key, None
    )
    return True

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/tablestore/#llama_index.storage.kvstore.tablestore.TablestoreKVStore.adelete "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-tablestore/llama_index/storage/kvstore/tablestore/base.py`  
| 
```
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
async defadelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
    Delete a value from the store.

    Args:
        key (str): key
        collection (str): collection name

    """
    raise NotImplementedError

```
 |  
| --- | --- |  
options: members: - TablestoreKVStore
