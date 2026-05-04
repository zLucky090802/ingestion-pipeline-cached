# Azurecosmosnosql
##  AzureCosmosNoSqlKVStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azurecosmosnosql/#llama_index.storage.kvstore.azurecosmosnosql.AzureCosmosNoSqlKVStore "Permanent link")
Bases: , 
Creates an Azure Cosmos DB NoSql Chat Store.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azurecosmosnosql/llama_index/storage/kvstore/azurecosmosnosql/base.py`  
| 
```
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
```
 | 
```
classAzureCosmosNoSqlKVStore(BaseKVStore, ABC):
"""Creates an Azure Cosmos DB NoSql Chat Store."""

    _cosmos_client: CosmosClient = PrivateAttr()
    _database: DatabaseProxy = PrivateAttr()
    _container: ContainerProxy = PrivateAttr()

    def__init__(
        self,
        cosmos_client: CosmosClient,
        chat_db_name: str = DEFAULT_CHAT_DATABASE,
        chat_container_name: str = DEFAULT_CHAT_CONTAINER,
        cosmos_container_properties: Dict[str, Any] = None,
        cosmos_database_properties: Dict[str, Any] = None,
        **kwargs,
    ):
        self._cosmos_client = cosmos_client

        # Create the database if it already doesn't exist
        self._database = self._cosmos_client.create_database_if_not_exists(
            id=chat_db_name,
            offer_throughput=cosmos_database_properties.get("offer_throughput"),
            session_token=cosmos_database_properties.get("session_token"),
            initial_headers=cosmos_database_properties.get("initial_headers"),
            etag=cosmos_database_properties.get("etag"),
            match_condition=cosmos_database_properties.get("match_condition"),
        )

        # Create the collection if it already doesn't exist
        self._container = self._database.create_container_if_not_exists(
            id=chat_container_name,
            partition_key=cosmos_container_properties["partition_key"],
            indexing_policy=cosmos_container_properties.get("indexing_policy"),
            default_ttl=cosmos_container_properties.get("default_ttl"),
            offer_throughput=cosmos_container_properties.get("offer_throughput"),
            unique_key_policy=cosmos_container_properties.get("unique_key_policy"),
            conflict_resolution_policy=cosmos_container_properties.get(
                "conflict_resolution_policy"
            ),
            analytical_storage_ttl=cosmos_container_properties.get(
                "analytical_storage_ttl"
            ),
            computed_properties=cosmos_container_properties.get("computed_properties"),
            etag=cosmos_container_properties.get("etag"),
            match_condition=cosmos_container_properties.get("match_condition"),
            session_token=cosmos_container_properties.get("session_token"),
            initial_headers=cosmos_container_properties.get("initial_headers"),
        )

    @classmethod
    deffrom_connection_string(
        cls,
        connection_string: str,
        chat_db_name: str = DEFAULT_CHAT_DATABASE,
        chat_container_name: str = DEFAULT_CHAT_CONTAINER,
        cosmos_container_properties: Dict[str, Any] = None,
        cosmos_database_properties: Dict[str, Any] = None,
    ) -> "AzureCosmosNoSqlKVStore":
"""Creates an instance of Azure Cosmos DB NoSql KV Store using a connection string."""
        cosmos_client = CosmosClient.from_connection_string(connection_string)

        return cls(
            cosmos_client,
            chat_db_name,
            chat_container_name,
            cosmos_container_properties,
            cosmos_database_properties,
        )

    @classmethod
    deffrom_account_and_key(
        cls,
        endpoint: str,
        key: str,
        chat_db_name: str = DEFAULT_CHAT_DATABASE,
        chat_container_name: str = DEFAULT_CHAT_CONTAINER,
        cosmos_container_properties: Dict[str, Any] = None,
        cosmos_database_properties: Dict[str, Any] = None,
    ) -> "AzureCosmosNoSqlKVStore":
"""Initializes AzureCosmosNoSqlKVStore from an endpoint url and key."""
        cosmos_client = CosmosClient(endpoint, key)
        return cls(
            cosmos_client,
            chat_db_name,
            chat_container_name,
            cosmos_container_properties,
            cosmos_database_properties,
        )

    @classmethod
    deffrom_aad_token(
        cls,
        endpoint: str,
        chat_db_name: str = DEFAULT_CHAT_DATABASE,
        chat_container_name: str = DEFAULT_CHAT_CONTAINER,
        cosmos_container_properties: Dict[str, Any] = None,
        cosmos_database_properties: Dict[str, Any] = None,
    ) -> "AzureCosmosNoSqlKVStore":
"""Creates an AzureCosmosNoSqlKVStore using an Azure Active Directory token."""
        fromazure.identityimport DefaultAzureCredential

        credential = DefaultAzureCredential()
        return cls._from_clients(
            endpoint,
            credential,
            chat_db_name,
            chat_container_name,
            cosmos_container_properties,
            cosmos_database_properties,
        )

    defput(self, key: str, val: dict, collection: str = DEFAULT_COLLECTION) -> None:
"""
        Put a key-value pair into the store.

        Args:
            key (str): key
            val (dict): value
            collection (str): collection name

        """
        self._container.create_item(
            body={
                "id": key,
                "messages": val,
            }
        )

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
        response = self._container.read_item(key)
        if response is not None:
            messages = response.get("messages")
        else:
            messages = {}
        return messages

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
        items = self._container.read_all_items()
        output = {}
        for item in items:
            key = item.get("id")
            output[key] = item
        return output

    async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
        Get all values from the store.

        Args:
            collection (str): collection name

        """
        raise NotImplementedError

    defdelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
        try:
            self._container.delete_item(key)
            return True
        except Exception as e:
            logger.error(f"Error deleting item {e} with key {key}")
            return False

    async defadelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""
        Delete a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        raise NotImplementedError

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "AzureCosmosNoSqlKVStore"

    @classmethod
    def_from_clients(
        cls,
        endpoint: str,
        credential: Any,
        chat_db_name: str = DEFAULT_CHAT_DATABASE,
        chat_container_name: str = DEFAULT_CHAT_CONTAINER,
        cosmos_container_properties: Dict[str, Any] = None,
        cosmos_database_properties: Dict[str, Any] = None,
    ) -> "AzureCosmosNoSqlKVStore":
"""Create cosmos db service clients."""
        cosmos_client = CosmosClient(url=endpoint, credential=credential)
        return cls(
            cosmos_client,
            chat_db_name,
            chat_container_name,
            cosmos_container_properties,
            cosmos_database_properties,
        )

```
 |  
| --- | --- |  
###  from_connection_string `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azurecosmosnosql/#llama_index.storage.kvstore.azurecosmosnosql.AzureCosmosNoSqlKVStore.from_connection_string "Permanent link")

```
from_connection_string(
    connection_string: ,
    chat_db_name:  = DEFAULT_CHAT_DATABASE,
    chat_container_name:  = DEFAULT_CHAT_CONTAINER,
    cosmos_container_properties: [, ] = None,
    cosmos_database_properties: [, ] = None,
) -> 

```

Creates an instance of Azure Cosmos DB NoSql KV Store using a connection string.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azurecosmosnosql/llama_index/storage/kvstore/azurecosmosnosql/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_connection_string(
    cls,
    connection_string: str,
    chat_db_name: str = DEFAULT_CHAT_DATABASE,
    chat_container_name: str = DEFAULT_CHAT_CONTAINER,
    cosmos_container_properties: Dict[str, Any] = None,
    cosmos_database_properties: Dict[str, Any] = None,
) -> "AzureCosmosNoSqlKVStore":
"""Creates an instance of Azure Cosmos DB NoSql KV Store using a connection string."""
    cosmos_client = CosmosClient.from_connection_string(connection_string)

    return cls(
        cosmos_client,
        chat_db_name,
        chat_container_name,
        cosmos_container_properties,
        cosmos_database_properties,
    )

```
 |  
| --- | --- |  
###  from_account_and_key `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azurecosmosnosql/#llama_index.storage.kvstore.azurecosmosnosql.AzureCosmosNoSqlKVStore.from_account_and_key "Permanent link")

```
from_account_and_key(
    endpoint: ,
    key: ,
    chat_db_name:  = DEFAULT_CHAT_DATABASE,
    chat_container_name:  = DEFAULT_CHAT_CONTAINER,
    cosmos_container_properties: [, ] = None,
    cosmos_database_properties: [, ] = None,
) -> 

```

Initializes AzureCosmosNoSqlKVStore from an endpoint url and key.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azurecosmosnosql/llama_index/storage/kvstore/azurecosmosnosql/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_account_and_key(
    cls,
    endpoint: str,
    key: str,
    chat_db_name: str = DEFAULT_CHAT_DATABASE,
    chat_container_name: str = DEFAULT_CHAT_CONTAINER,
    cosmos_container_properties: Dict[str, Any] = None,
    cosmos_database_properties: Dict[str, Any] = None,
) -> "AzureCosmosNoSqlKVStore":
"""Initializes AzureCosmosNoSqlKVStore from an endpoint url and key."""
    cosmos_client = CosmosClient(endpoint, key)
    return cls(
        cosmos_client,
        chat_db_name,
        chat_container_name,
        cosmos_container_properties,
        cosmos_database_properties,
    )

```
 |  
| --- | --- |  
###  from_aad_token `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azurecosmosnosql/#llama_index.storage.kvstore.azurecosmosnosql.AzureCosmosNoSqlKVStore.from_aad_token "Permanent link")

```
from_aad_token(
    endpoint: ,
    chat_db_name:  = DEFAULT_CHAT_DATABASE,
    chat_container_name:  = DEFAULT_CHAT_CONTAINER,
    cosmos_container_properties: [, ] = None,
    cosmos_database_properties: [, ] = None,
) -> 

```

Creates an AzureCosmosNoSqlKVStore using an Azure Active Directory token.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azurecosmosnosql/llama_index/storage/kvstore/azurecosmosnosql/base.py`  
| 
```
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
deffrom_aad_token(
    cls,
    endpoint: str,
    chat_db_name: str = DEFAULT_CHAT_DATABASE,
    chat_container_name: str = DEFAULT_CHAT_CONTAINER,
    cosmos_container_properties: Dict[str, Any] = None,
    cosmos_database_properties: Dict[str, Any] = None,
) -> "AzureCosmosNoSqlKVStore":
"""Creates an AzureCosmosNoSqlKVStore using an Azure Active Directory token."""
    fromazure.identityimport DefaultAzureCredential

    credential = DefaultAzureCredential()
    return cls._from_clients(
        endpoint,
        credential,
        chat_db_name,
        chat_container_name,
        cosmos_container_properties,
        cosmos_database_properties,
    )

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azurecosmosnosql/#llama_index.storage.kvstore.azurecosmosnosql.AzureCosmosNoSqlKVStore.put "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azurecosmosnosql/llama_index/storage/kvstore/azurecosmosnosql/base.py`  
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
    self._container.create_item(
        body={
            "id": key,
            "messages": val,
        }
    )

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azurecosmosnosql/#llama_index.storage.kvstore.azurecosmosnosql.AzureCosmosNoSqlKVStore.aput "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azurecosmosnosql/llama_index/storage/kvstore/azurecosmosnosql/base.py`  
| 
```
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
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azurecosmosnosql/#llama_index.storage.kvstore.azurecosmosnosql.AzureCosmosNoSqlKVStore.get "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azurecosmosnosql/llama_index/storage/kvstore/azurecosmosnosql/base.py`  
| 
```
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
    response = self._container.read_item(key)
    if response is not None:
        messages = response.get("messages")
    else:
        messages = {}
    return messages

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azurecosmosnosql/#llama_index.storage.kvstore.azurecosmosnosql.AzureCosmosNoSqlKVStore.aget "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azurecosmosnosql/llama_index/storage/kvstore/azurecosmosnosql/base.py`  
| 
```
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
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azurecosmosnosql/#llama_index.storage.kvstore.azurecosmosnosql.AzureCosmosNoSqlKVStore.get_all "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azurecosmosnosql/llama_index/storage/kvstore/azurecosmosnosql/base.py`  
| 
```
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
```
 | 
```
defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
    Get all values from the store.

    Args:
        collection (str): collection name

    """
    items = self._container.read_all_items()
    output = {}
    for item in items:
        key = item.get("id")
        output[key] = item
    return output

```
 |  
| --- | --- |  
###  aget_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azurecosmosnosql/#llama_index.storage.kvstore.azurecosmosnosql.AzureCosmosNoSqlKVStore.aget_all "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azurecosmosnosql/llama_index/storage/kvstore/azurecosmosnosql/base.py`  
| 
```
205
206
207
208
209
210
211
212
213
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
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azurecosmosnosql/#llama_index.storage.kvstore.azurecosmosnosql.AzureCosmosNoSqlKVStore.adelete "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azurecosmosnosql/llama_index/storage/kvstore/azurecosmosnosql/base.py`  
| 
```
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
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/azurecosmosnosql/#llama_index.storage.kvstore.azurecosmosnosql.AzureCosmosNoSqlKVStore.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-azurecosmosnosql/llama_index/storage/kvstore/azurecosmosnosql/base.py`  
| 
```
234
235
236
237
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "AzureCosmosNoSqlKVStore"

```
 |  
| --- | --- |  
options: members: - AzureCosmosNoSqlKVStore
