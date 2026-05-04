# Simple
##  SimpleIndexStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/simple/#llama_index.core.storage.index_store.SimpleIndexStore "Permanent link")
Bases: `KVIndexStore`
Simple in-memory Index store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `simple_kvstore`  |   |  simple key-value store  |  `None`  |  
Source code in `llama-index-core/llama_index/core/storage/index_store/simple_index_store.py`  
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
```
 | 
```
classSimpleIndexStore(KVIndexStore):
"""
    Simple in-memory Index store.

    Args:
        simple_kvstore (SimpleKVStore): simple key-value store

    """

    def__init__(
        self,
        simple_kvstore: Optional[SimpleKVStore] = None,
    ) -> None:
"""Init a SimpleIndexStore."""
        simple_kvstore = simple_kvstore or SimpleKVStore()
        super().__init__(simple_kvstore)

    @classmethod
    deffrom_persist_dir(
        cls,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> "SimpleIndexStore":
"""Create a SimpleIndexStore from a persist directory."""
        if fs is not None:
            persist_path = concat_dirs(persist_dir, DEFAULT_PERSIST_FNAME)
        else:
            persist_path = os.path.join(persist_dir, DEFAULT_PERSIST_FNAME)
        return cls.from_persist_path(persist_path, fs=fs)

    @classmethod
    deffrom_persist_path(
        cls,
        persist_path: str,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> "SimpleIndexStore":
"""Create a SimpleIndexStore from a persist path."""
        fs = fs or fsspec.filesystem("file")
        simple_kvstore = SimpleKVStore.from_persist_path(persist_path, fs=fs)
        return cls(simple_kvstore)

    defpersist(
        self,
        persist_path: str = DEFAULT_PERSIST_PATH,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> None:
"""Persist the store."""
        if isinstance(self._kvstore, (MutableMappingKVStore, BaseInMemoryKVStore)):
            self._kvstore.persist(persist_path, fs=fs)

    @classmethod
    deffrom_dict(cls, save_dict: dict) -> "SimpleIndexStore":
        simple_kvstore = SimpleKVStore.from_dict(save_dict)
        return cls(simple_kvstore)

    defto_dict(self) -> dict:
        assert isinstance(self._kvstore, SimpleKVStore)
        return self._kvstore.to_dict()

```
 |  
| --- | --- |  
###  from_persist_dir `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/simple/#llama_index.core.storage.index_store.SimpleIndexStore.from_persist_dir "Permanent link")

```
from_persist_dir(
    persist_dir:  = DEFAULT_PERSIST_DIR,
    fs: Optional[AbstractFileSystem] = None,
) -> 

```

Create a SimpleIndexStore from a persist directory.
Source code in `llama-index-core/llama_index/core/storage/index_store/simple_index_store.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_persist_dir(
    cls,
    persist_dir: str = DEFAULT_PERSIST_DIR,
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> "SimpleIndexStore":
"""Create a SimpleIndexStore from a persist directory."""
    if fs is not None:
        persist_path = concat_dirs(persist_dir, DEFAULT_PERSIST_FNAME)
    else:
        persist_path = os.path.join(persist_dir, DEFAULT_PERSIST_FNAME)
    return cls.from_persist_path(persist_path, fs=fs)

```
 |  
| --- | --- |  
###  from_persist_path `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/simple/#llama_index.core.storage.index_store.SimpleIndexStore.from_persist_path "Permanent link")

```
from_persist_path(
    persist_path: ,
    fs: Optional[AbstractFileSystem] = None,
) -> 

```

Create a SimpleIndexStore from a persist path.
Source code in `llama-index-core/llama_index/core/storage/index_store/simple_index_store.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_persist_path(
    cls,
    persist_path: str,
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> "SimpleIndexStore":
"""Create a SimpleIndexStore from a persist path."""
    fs = fs or fsspec.filesystem("file")
    simple_kvstore = SimpleKVStore.from_persist_path(persist_path, fs=fs)
    return cls(simple_kvstore)

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/simple/#llama_index.core.storage.index_store.SimpleIndexStore.persist "Permanent link")

```
persist(
    persist_path:  = DEFAULT_PERSIST_PATH,
    fs: Optional[AbstractFileSystem] = None,
) -> None

```

Persist the store.
Source code in `llama-index-core/llama_index/core/storage/index_store/simple_index_store.py`  
| 
```
60
61
62
63
64
65
66
67
```
 | 
```
defpersist(
    self,
    persist_path: str = DEFAULT_PERSIST_PATH,
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> None:
"""Persist the store."""
    if isinstance(self._kvstore, (MutableMappingKVStore, BaseInMemoryKVStore)):
        self._kvstore.persist(persist_path, fs=fs)

```
 |  
| --- | --- |  
options: members: - SimpleIndexStore
