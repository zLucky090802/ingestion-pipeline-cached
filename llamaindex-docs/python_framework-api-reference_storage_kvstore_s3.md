# S3
##  S3DBKVStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/s3/#llama_index.storage.kvstore.s3.S3DBKVStore "Permanent link")
Bases: 
S3 Key-Value store. Stores key-value pairs in a S3 bucket. Can optionally specify a path to a folder where KV data is stored. The KV data is further divided into collections, which are subfolders in the path. Each key-value pair is stored as a JSON file.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `s3_bucket`  |  boto3 S3 Bucket instance  |  _required_  |  
|  `path`  |  `Optional[str]`  |  path to folder in S3 bucket where KV data is stored  |  `'./'`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-s3/llama_index/storage/kvstore/s3/base.py`  
| 
```
 10
 11
 12
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
```
 | 
```
classS3DBKVStore(BaseKVStore):
"""
    S3 Key-Value store.
    Stores key-value pairs in a S3 bucket. Can optionally specify a path to a folder
        where KV data is stored.
    The KV data is further divided into collections, which are subfolders in the path.
    Each key-value pair is stored as a JSON file.

    Args:
        s3_bucket (Any): boto3 S3 Bucket instance
        path (Optional[str]): path to folder in S3 bucket where KV data is stored

    """

    def__init__(
        self,
        bucket: Any,
        path: Optional[str] = "./",
    ) -> None:
"""Init a S3DBKVStore."""
        self._bucket = bucket
        self._path = path or "./"

    @classmethod
    deffrom_s3_location(
        cls,
        bucket_name: str,
        path: Optional[str] = None,
    ) -> "S3DBKVStore":
"""
        Load a S3DBKVStore from a S3 URI.

        Args:
            bucket_name (str): S3 bucket name
            path (Optional[str]): path to folder in S3 bucket where KV data is stored

        """
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(bucket_name)
        return cls(
            bucket,
            path=path,
        )

    def_get_object_key(self, collection: str, key: str) -> str:
        return str(PurePath(f"{self._path}/{collection}/{key}.json"))

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
        obj_key = self._get_object_key(collection, key)
        self._bucket.put_object(
            Key=obj_key,
            Body=json.dumps(val),
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
        raise NotImplementedError

    defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> Optional[dict]:
"""
        Get a value from the store.

        Args:
            key (str): key
            collection (str): collection name

        """
        obj_key = self._get_object_key(collection, key)
        try:
            obj = next(iter(self._bucket.objects.filter(Prefix=obj_key).limit(1)))
        except StopIteration:
            return None
        body = obj.get()["Body"].read()
        return json.loads(body)

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
        collection_path = str(PurePath(f"{self._path}/{collection}/"))
        collection_kv_dict = {}
        for obj in self._bucket.objects.filter(Prefix=collection_path):
            body = obj.get()["Body"].read()
            json_filename = os.path.split(obj.key)[-1]
            key = os.path.splitext(json_filename)[0]
            value = json.loads(body)
            collection_kv_dict[key] = value
        return collection_kv_dict

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
        obj_key = self._get_object_key(collection, key)
        matched_objs = list(self._bucket.objects.filter(Prefix=obj_key).limit(1))
        if len(matched_objs) == 0:
            return False
        obj = matched_objs[0]
        obj.delete()
        return True

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
###  from_s3_location `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/s3/#llama_index.storage.kvstore.s3.S3DBKVStore.from_s3_location "Permanent link")

```
from_s3_location(
    bucket_name: , path: Optional[] = None
) -> 

```

Load a S3DBKVStore from a S3 URI.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `bucket_name`  |  S3 bucket name  |  _required_  |  
|  `path`  |  `Optional[str]`  |  path to folder in S3 bucket where KV data is stored  |  `None`  |  
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-s3/llama_index/storage/kvstore/s3/base.py`  
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
```
 | 
```
@classmethod
deffrom_s3_location(
    cls,
    bucket_name: str,
    path: Optional[str] = None,
) -> "S3DBKVStore":
"""
    Load a S3DBKVStore from a S3 URI.

    Args:
        bucket_name (str): S3 bucket name
        path (Optional[str]): path to folder in S3 bucket where KV data is stored

    """
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    return cls(
        bucket,
        path=path,
    )

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/s3/#llama_index.storage.kvstore.s3.S3DBKVStore.put "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-s3/llama_index/storage/kvstore/s3/base.py`  
| 
```
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
    obj_key = self._get_object_key(collection, key)
    self._bucket.put_object(
        Key=obj_key,
        Body=json.dumps(val),
    )

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/s3/#llama_index.storage.kvstore.s3.S3DBKVStore.aput "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-s3/llama_index/storage/kvstore/s3/base.py`  
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
    raise NotImplementedError

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/s3/#llama_index.storage.kvstore.s3.S3DBKVStore.get "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-s3/llama_index/storage/kvstore/s3/base.py`  
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
defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> Optional[dict]:
"""
    Get a value from the store.

    Args:
        key (str): key
        collection (str): collection name

    """
    obj_key = self._get_object_key(collection, key)
    try:
        obj = next(iter(self._bucket.objects.filter(Prefix=obj_key).limit(1)))
    except StopIteration:
        return None
    body = obj.get()["Body"].read()
    return json.loads(body)

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/s3/#llama_index.storage.kvstore.s3.S3DBKVStore.aget "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-s3/llama_index/storage/kvstore/s3/base.py`  
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
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/s3/#llama_index.storage.kvstore.s3.S3DBKVStore.get_all "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-s3/llama_index/storage/kvstore/s3/base.py`  
| 
```
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
```
 | 
```
defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""
    Get all values from the store.

    Args:
        collection (str): collection name

    """
    collection_path = str(PurePath(f"{self._path}/{collection}/"))
    collection_kv_dict = {}
    for obj in self._bucket.objects.filter(Prefix=collection_path):
        body = obj.get()["Body"].read()
        json_filename = os.path.split(obj.key)[-1]
        key = os.path.splitext(json_filename)[0]
        value = json.loads(body)
        collection_kv_dict[key] = value
    return collection_kv_dict

```
 |  
| --- | --- |  
###  aget_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/s3/#llama_index.storage.kvstore.s3.S3DBKVStore.aget_all "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-s3/llama_index/storage/kvstore/s3/base.py`  
| 
```
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
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/s3/#llama_index.storage.kvstore.s3.S3DBKVStore.delete "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-s3/llama_index/storage/kvstore/s3/base.py`  
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
    obj_key = self._get_object_key(collection, key)
    matched_objs = list(self._bucket.objects.filter(Prefix=obj_key).limit(1))
    if len(matched_objs) == 0:
        return False
    obj = matched_objs[0]
    obj.delete()
    return True

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/s3/#llama_index.storage.kvstore.s3.S3DBKVStore.adelete "Permanent link")

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
Source code in `llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-s3/llama_index/storage/kvstore/s3/base.py`  
| 
```
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
options: members: - S3DBKVStore
