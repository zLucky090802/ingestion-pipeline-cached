# Dynamodb
##  DynamoDBKVStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/dynamodb/#llama_index.storage.kvstore.dynamodb.DynamoDBKVStore "Permanent link")
Bases: 
DynamoDB Key-Value store. Stores key-value pairs in a DynamoDB Table. The DynamoDB Table must have both a hash key and a range key, and their types must be string.
You can specify a custom URL for DynamoDB by setting the `DYNAMODB_URL` environment variable. This is useful if you're using a local instance of DynamoDB for development or testing. If `DYNAMODB_URL` is not set, the application will use the default AWS DynamoDB service.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `table`  |  DynamoDB Table Service Resource  |  _required_  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-dynamodb/llama_index/storage/kvstore/dynamodb/base.py`  
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
```
 | 
```
classDynamoDBKVStore(BaseKVStore):
"""
    DynamoDB Key-Value store.
    Stores key-value pairs in a DynamoDB Table.
    The DynamoDB Table must have both a hash key and a range key,
        and their types must be string.

    You can specify a custom URL for DynamoDB by setting the `DYNAMODB_URL`
    environment variable. This is useful if you're using a local instance of
    DynamoDB for development or testing. If `DYNAMODB_URL` is not set, the
    application will use the default AWS DynamoDB service.

    Args:
        table (Any): DynamoDB Table Service Resource

    """

    def__init__(self, table: Any):
"""Init a DynamoDBKVStore."""
        self._table = table
        self._boto3_key = Key
        self._key_hash, self._key_range = parse_schema(table)

    @classmethod
    deffrom_table_name(cls, table_name: str) -> DynamoDBKVStore:
"""
        Load a DynamoDBKVStore from a DynamoDB table name.

        Args:
            table_name (str): DynamoDB table name

        """
        # Get the DynamoDB URL from environment variable
        dynamodb_url = os.getenv("DYNAMODB_URL")

        # Create a session
        session = boto3.Session()

        # If the DynamoDB URL is set, use it as the endpoint URL
        if dynamodb_url:
            ddb = session.resource("dynamodb", endpoint_url=dynamodb_url)
        else:
            # Otherwise, let boto3 use its default configuration
            ddb = session.resource("dynamodb")
        return cls(table=ddb.Table(table_name))

    defput(self, key: str, val: dict, collection: str = DEFAULT_COLLECTION) -> None:
"""
        Put a key-value pair into the store.

        Args:
            key (str): key
            val (dict): value
            collection (str): collection name

        """
        item = {k: convert_float_to_decimal(v) for k, v in val.items()}
        item[self._key_hash] = collection
        item[self._key_range] = key
        self._table.put_item(Item=item)

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

    defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> dict | None:
"""
        Get a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        resp = self._table.get_item(
            Key={self._key_hash: collection, self._key_range: key}
        )
        if (item := resp.get("Item")) is None:
            return None
        else:
            return {
                k: convert_decimal_to_int_or_float(v)
                for k, v in item.items()
                if k not in {self._key_hash, self._key_range}
            }

    async defaget(self, key: str, collection: str = DEFAULT_COLLECTION) -> dict | None:
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
        result = {}
        last_evaluated_key = None
        is_first = True
        while last_evaluated_key is not None or is_first:
            if is_first:
                is_first = False
            option = {
                "KeyConditionExpression": self._boto3_key(self._key_hash).eq(collection)
            }
            if last_evaluated_key is not None:
                option["ExclusiveStartKey"] = last_evaluated_key
            resp = self._table.query(**option)
            for item in resp.get("Items", []):
                item.pop(self._key_hash)
                key = item.pop(self._key_range)
                result[key] = {
                    k: convert_decimal_to_int_or_float(v) for k, v in item.items()
                }
            last_evaluated_key = resp.get("LastEvaluatedKey")
        return result

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
        resp = self._table.delete_item(
            Key={self._key_hash: collection, self._key_range: key},
            ReturnValues="ALL_OLD",
        )

        if (item := resp.get("Attributes")) is None:
            return False
        else:
            return len(item)  0

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
###  from_table_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/dynamodb/#llama_index.storage.kvstore.dynamodb.DynamoDBKVStore.from_table_name "Permanent link")

```
from_table_name(table_name: ) -> 

```

Load a DynamoDBKVStore from a DynamoDB table name.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `table_name`  |  DynamoDB table name  |  _required_  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-dynamodb/llama_index/storage/kvstore/dynamodb/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_table_name(cls, table_name: str) -> DynamoDBKVStore:
"""
    Load a DynamoDBKVStore from a DynamoDB table name.

    Args:
        table_name (str): DynamoDB table name

    """
    # Get the DynamoDB URL from environment variable
    dynamodb_url = os.getenv("DYNAMODB_URL")

    # Create a session
    session = boto3.Session()

    # If the DynamoDB URL is set, use it as the endpoint URL
    if dynamodb_url:
        ddb = session.resource("dynamodb", endpoint_url=dynamodb_url)
    else:
        # Otherwise, let boto3 use its default configuration
        ddb = session.resource("dynamodb")
    return cls(table=ddb.Table(table_name))

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/dynamodb/#llama_index.storage.kvstore.dynamodb.DynamoDBKVStore.put "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-dynamodb/llama_index/storage/kvstore/dynamodb/base.py`  
| 
```
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
    item = {k: convert_float_to_decimal(v) for k, v in val.items()}
    item[self._key_hash] = collection
    item[self._key_range] = key
    self._table.put_item(Item=item)

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/dynamodb/#llama_index.storage.kvstore.dynamodb.DynamoDBKVStore.aput "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-dynamodb/llama_index/storage/kvstore/dynamodb/base.py`  
| 
```
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
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/dynamodb/#llama_index.storage.kvstore.dynamodb.DynamoDBKVStore.get "Permanent link")

```
get(
    key: , collection:  = DEFAULT_COLLECTION
) ->  | None

```

Get a value from the store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  _required_  |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-dynamodb/llama_index/storage/kvstore/dynamodb/base.py`  
| 
```
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
```
 | 
```
defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> dict | None:
"""
    Get a value from the store.

    Args:
        key (str): key
        collection (str): collection name

    """
    resp = self._table.get_item(
        Key={self._key_hash: collection, self._key_range: key}
    )
    if (item := resp.get("Item")) is None:
        return None
    else:
        return {
            k: convert_decimal_to_int_or_float(v)
            for k, v in item.items()
            if k not in {self._key_hash, self._key_range}
        }

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/dynamodb/#llama_index.storage.kvstore.dynamodb.DynamoDBKVStore.aget "Permanent link")

```
aget(
    key: , collection:  = DEFAULT_COLLECTION
) ->  | None

```

Get a value from the store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  _required_  |  
|  `collection`  |  collection name  |  `DEFAULT_COLLECTION`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-dynamodb/llama_index/storage/kvstore/dynamodb/base.py`  
| 
```
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
async defaget(self, key: str, collection: str = DEFAULT_COLLECTION) -> dict | None:
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
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/dynamodb/#llama_index.storage.kvstore.dynamodb.DynamoDBKVStore.get_all "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-dynamodb/llama_index/storage/kvstore/dynamodb/base.py`  
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
```
 | 
```
defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
    Get all values from the store.

    Args:
        collection (str): collection name

    """
    result = {}
    last_evaluated_key = None
    is_first = True
    while last_evaluated_key is not None or is_first:
        if is_first:
            is_first = False
        option = {
            "KeyConditionExpression": self._boto3_key(self._key_hash).eq(collection)
        }
        if last_evaluated_key is not None:
            option["ExclusiveStartKey"] = last_evaluated_key
        resp = self._table.query(**option)
        for item in resp.get("Items", []):
            item.pop(self._key_hash)
            key = item.pop(self._key_range)
            result[key] = {
                k: convert_decimal_to_int_or_float(v) for k, v in item.items()
            }
        last_evaluated_key = resp.get("LastEvaluatedKey")
    return result

```
 |  
| --- | --- |  
###  aget_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/dynamodb/#llama_index.storage.kvstore.dynamodb.DynamoDBKVStore.aget_all "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-dynamodb/llama_index/storage/kvstore/dynamodb/base.py`  
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
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/dynamodb/#llama_index.storage.kvstore.dynamodb.DynamoDBKVStore.delete "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-dynamodb/llama_index/storage/kvstore/dynamodb/base.py`  
| 
```
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
    resp = self._table.delete_item(
        Key={self._key_hash: collection, self._key_range: key},
        ReturnValues="ALL_OLD",
    )

    if (item := resp.get("Attributes")) is None:
        return False
    else:
        return len(item)  0

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/dynamodb/#llama_index.storage.kvstore.dynamodb.DynamoDBKVStore.adelete "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-dynamodb/llama_index/storage/kvstore/dynamodb/base.py`  
| 
```
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
options: members: - DynamoDBKVStore
