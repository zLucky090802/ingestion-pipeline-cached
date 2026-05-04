# Index
##  BaseKVStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/#llama_index.core.storage.kvstore.types.BaseKVStore "Permanent link")
Bases: 
Base key-value store.
Source code in `llama-index-core/llama_index/core/storage/kvstore/types.py`  
| 
```
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
```
 | 
```
classBaseKVStore(ABC):
"""Base key-value store."""

    @abstractmethod
    defput(self, key: str, val: dict, collection: str = DEFAULT_COLLECTION) -> None:
        pass

    @abstractmethod
    async defaput(
        self, key: str, val: dict, collection: str = DEFAULT_COLLECTION
    ) -> None:
        pass

    defput_all(
        self,
        kv_pairs: List[Tuple[str, dict]],
        collection: str = DEFAULT_COLLECTION,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
        # by default, support a batch size of 1
        if batch_size != 1:
            raise NotImplementedError("Batching not supported by this key-value store.")
        else:
            for key, val in kv_pairs:
                self.put(key, val, collection=collection)

    async defaput_all(
        self,
        kv_pairs: List[Tuple[str, dict]],
        collection: str = DEFAULT_COLLECTION,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
        # by default, support a batch size of 1
        if batch_size != 1:
            raise NotImplementedError("Batching not supported by this key-value store.")
        else:
            for key, val in kv_pairs:
                await self.aput(key, val, collection=collection)

    @abstractmethod
    defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> Optional[dict]:
        pass

    @abstractmethod
    async defaget(
        self, key: str, collection: str = DEFAULT_COLLECTION
    ) -> Optional[dict]:
        pass

    @abstractmethod
    defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
        pass

    @abstractmethod
    async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
        pass

    @abstractmethod
    defdelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
        pass

    @abstractmethod
    async defadelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
        pass

```
 |  
| --- | --- |  
##  BaseInMemoryKVStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/#llama_index.core.storage.kvstore.types.BaseInMemoryKVStore "Permanent link")
Bases: 
Base in-memory key-value store.
Source code in `llama-index-core/llama_index/core/storage/kvstore/types.py`  
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
```
 | 
```
classBaseInMemoryKVStore(BaseKVStore):
"""Base in-memory key-value store."""

    @abstractmethod
    defpersist(
        self, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
    ) -> None:
        pass

    @classmethod
    @abstractmethod
    deffrom_persist_path(cls, persist_path: str) -> "BaseInMemoryKVStore":
"""Create a BaseInMemoryKVStore from a persist directory."""

```
 |  
| --- | --- |  
###  from_persist_path `abstractmethod` `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/#llama_index.core.storage.kvstore.types.BaseInMemoryKVStore.from_persist_path "Permanent link")

```
from_persist_path(persist_path: ) -> 

```

Create a BaseInMemoryKVStore from a persist directory.
Source code in `llama-index-core/llama_index/core/storage/kvstore/types.py`  
| 
```
86
87
88
89
```
 | 
```
@classmethod
@abstractmethod
deffrom_persist_path(cls, persist_path: str) -> "BaseInMemoryKVStore":
"""Create a BaseInMemoryKVStore from a persist directory."""

```
 |  
| --- | --- |  
##  MutableMappingKVStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/#llama_index.core.storage.kvstore.types.MutableMappingKVStore "Permanent link")
Bases: `Generic[MutableMappingT]`, 
MutableMapping Key-Value store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `mapping_factory`  |  `Callable[[], MutableMapping[str, dict]`  |  the mutable mapping factory  |  _required_  |  
Source code in `llama-index-core/llama_index/core/storage/kvstore/types.py`  
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
```
 | 
```
classMutableMappingKVStore(Generic[MutableMappingT], BaseKVStore):
"""
    MutableMapping Key-Value store.

    Args:
        mapping_factory (Callable[[], MutableMapping[str, dict]): the mutable mapping factory

    """

    def__init__(self, mapping_factory: Callable[[], MutableMappingT]) -> None:
"""Initialize a MutableMappingKVStore."""
        self._collections_mappings: Dict[str, MutableMappingT] = {}
        self._mapping_factory = mapping_factory

    def__getstate__(self) -> dict:
        state = self.__dict__.copy()
        state["factory_fn"] = {"fn": self._mapping_factory}
        del state["_mapping_factory"]
        return state

    def__setstate__(self, state: dict) -> None:
        self._collections_mappings = state["_collections_mappings"]
        self._mapping_factory = state["factory_fn"]["fn"]

    def_get_collection_mapping(self, collection: str) -> MutableMappingT:
"""Get a collection mapping. Create one if it does not exist."""
        if collection not in self._collections_mappings:
            self._collections_mappings[collection] = self._mapping_factory()
        return self._collections_mappings[collection]

    defput(self, key: str, val: dict, collection: str = DEFAULT_COLLECTION) -> None:
"""Put a key-value pair into the store."""
        self._get_collection_mapping(collection)[key] = val.copy()

    async defaput(
        self, key: str, val: dict, collection: str = DEFAULT_COLLECTION
    ) -> None:
"""Put a key-value pair into the store."""
        self.put(key, val, collection=collection)

    defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> Optional[dict]:
"""Get a value from the store."""
        mapping = self._get_collection_mapping(collection)

        if key not in mapping:
            return None
        return mapping[key].copy()

    async defaget(
        self, key: str, collection: str = DEFAULT_COLLECTION
    ) -> Optional[dict]:
"""Get a value from the store."""
        return self.get(key, collection=collection)

    defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""Get all values from the store."""
        return dict(self._get_collection_mapping(collection))

    async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""Get all values from the store."""
        return self.get_all(collection=collection)

    defdelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""Delete a value from the store."""
        try:
            self._get_collection_mapping(collection).pop(key)
            return True
        except KeyError:
            return False

    async defadelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""Delete a value from the store."""
        return self.delete(key, collection=collection)

    # this method is here to avoid TypeChecker shows an error
    defpersist(
        self, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
    ) -> None:
"""Persist the store."""
        raise NotImplementedError(
            "Use subclasses of MutableMappingKVStore (such as SimpleKVStore) to call this method"
        )

    # this method is here to avoid TypeChecker shows an error
    deffrom_persist_path(cls, persist_path: str) -> "MutableMappingKVStore":
"""Create a MutableMappingKVStore from a persist directory."""
        raise NotImplementedError(
            "Use subclasses of MutableMappingKVStore (such as SimpleKVStore) to call this method"
        )

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/#llama_index.core.storage.kvstore.types.MutableMappingKVStore.put "Permanent link")

```
put(
    key: ,
    val: ,
    collection:  = DEFAULT_COLLECTION,
) -> None

```

Put a key-value pair into the store.
Source code in `llama-index-core/llama_index/core/storage/kvstore/types.py`  
| 
```
125
126
127
```
 | 
```
defput(self, key: str, val: dict, collection: str = DEFAULT_COLLECTION) -> None:
"""Put a key-value pair into the store."""
    self._get_collection_mapping(collection)[key] = val.copy()

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/#llama_index.core.storage.kvstore.types.MutableMappingKVStore.aput "Permanent link")

```
aput(
    key: ,
    val: ,
    collection:  = DEFAULT_COLLECTION,
) -> None

```

Put a key-value pair into the store.
Source code in `llama-index-core/llama_index/core/storage/kvstore/types.py`  
| 
```
129
130
131
132
133
```
 | 
```
async defaput(
    self, key: str, val: dict, collection: str = DEFAULT_COLLECTION
) -> None:
"""Put a key-value pair into the store."""
    self.put(key, val, collection=collection)

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/#llama_index.core.storage.kvstore.types.MutableMappingKVStore.get "Permanent link")

```
get(
    key: , collection:  = DEFAULT_COLLECTION
) -> Optional[]

```

Get a value from the store.
Source code in `llama-index-core/llama_index/core/storage/kvstore/types.py`  
| 
```
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
defget(self, key: str, collection: str = DEFAULT_COLLECTION) -> Optional[dict]:
"""Get a value from the store."""
    mapping = self._get_collection_mapping(collection)

    if key not in mapping:
        return None
    return mapping[key].copy()

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/#llama_index.core.storage.kvstore.types.MutableMappingKVStore.aget "Permanent link")

```
aget(
    key: , collection:  = DEFAULT_COLLECTION
) -> Optional[]

```

Get a value from the store.
Source code in `llama-index-core/llama_index/core/storage/kvstore/types.py`  
| 
```
143
144
145
146
147
```
 | 
```
async defaget(
    self, key: str, collection: str = DEFAULT_COLLECTION
) -> Optional[dict]:
"""Get a value from the store."""
    return self.get(key, collection=collection)

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/#llama_index.core.storage.kvstore.types.MutableMappingKVStore.get_all "Permanent link")

```
get_all(
    collection:  = DEFAULT_COLLECTION,
) -> [, ]

```

Get all values from the store.
Source code in `llama-index-core/llama_index/core/storage/kvstore/types.py`  
| 
```
149
150
151
```
 | 
```
defget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""Get all values from the store."""
    return dict(self._get_collection_mapping(collection))

```
 |  
| --- | --- |  
###  aget_all [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/#llama_index.core.storage.kvstore.types.MutableMappingKVStore.aget_all "Permanent link")

```
aget_all(
    collection:  = DEFAULT_COLLECTION,
) -> [, ]

```

Get all values from the store.
Source code in `llama-index-core/llama_index/core/storage/kvstore/types.py`  
| 
```
153
154
155
```
 | 
```
async defaget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
"""Get all values from the store."""
    return self.get_all(collection=collection)

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/#llama_index.core.storage.kvstore.types.MutableMappingKVStore.delete "Permanent link")

```
delete(
    key: , collection:  = DEFAULT_COLLECTION
) -> 

```

Delete a value from the store.
Source code in `llama-index-core/llama_index/core/storage/kvstore/types.py`  
| 
```
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
defdelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""Delete a value from the store."""
    try:
        self._get_collection_mapping(collection).pop(key)
        return True
    except KeyError:
        return False

```
 |  
| --- | --- |  
###  adelete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/#llama_index.core.storage.kvstore.types.MutableMappingKVStore.adelete "Permanent link")

```
adelete(
    key: , collection:  = DEFAULT_COLLECTION
) -> 

```

Delete a value from the store.
Source code in `llama-index-core/llama_index/core/storage/kvstore/types.py`  
| 
```
165
166
167
```
 | 
```
async defadelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
"""Delete a value from the store."""
    return self.delete(key, collection=collection)

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/#llama_index.core.storage.kvstore.types.MutableMappingKVStore.persist "Permanent link")

```
persist(
    persist_path: ,
    fs: Optional[AbstractFileSystem] = None,
) -> None

```

Persist the store.
Source code in `llama-index-core/llama_index/core/storage/kvstore/types.py`  
| 
```
170
171
172
173
174
175
176
```
 | 
```
defpersist(
    self, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
) -> None:
"""Persist the store."""
    raise NotImplementedError(
        "Use subclasses of MutableMappingKVStore (such as SimpleKVStore) to call this method"
    )

```
 |  
| --- | --- |  
###  from_persist_path [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/#llama_index.core.storage.kvstore.types.MutableMappingKVStore.from_persist_path "Permanent link")

```
from_persist_path(
    persist_path: ,
) -> 

```

Create a MutableMappingKVStore from a persist directory.
Source code in `llama-index-core/llama_index/core/storage/kvstore/types.py`  
| 
```
179
180
181
182
183
```
 | 
```
deffrom_persist_path(cls, persist_path: str) -> "MutableMappingKVStore":
"""Create a MutableMappingKVStore from a persist directory."""
    raise NotImplementedError(
        "Use subclasses of MutableMappingKVStore (such as SimpleKVStore) to call this method"
    )

```
 |  
| --- | --- |
