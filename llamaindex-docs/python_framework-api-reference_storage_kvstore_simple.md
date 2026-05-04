# Simple
##  SimpleKVStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/simple/#llama_index.core.storage.kvstore.SimpleKVStore "Permanent link")
Bases: `MutableMappingKVStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/#llama_index.core.storage.kvstore.types.MutableMappingKVStore "MutableMappingKVStore \(llama_index.core.storage.kvstore.types.MutableMappingKVStore\)")[dict]`
Simple in-memory Key-Value store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `data`  |  `Optional[DATA_TYPE]`  |  data to initialize the store with  |  `None`  |  
Source code in `llama-index-core/llama_index/core/storage/kvstore/simple_kvstore.py`  
| 
```
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
```
 | 
```
classSimpleKVStore(MutableMappingKVStore[dict]):
"""
    Simple in-memory Key-Value store.

    Args:
        data (Optional[DATA_TYPE]): data to initialize the store with

    """

    def__init__(
        self,
        data: Optional[DATA_TYPE] = None,
    ) -> None:
"""Init a SimpleKVStore."""
        super().__init__(mapping_factory=dict)

        if data is not None:
            self._collections_mappings = data.copy()

    defpersist(
        self, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
    ) -> None:
"""Persist the store."""
        fs = fs or fsspec.filesystem("file")
        dirpath = os.path.dirname(persist_path)
        if not fs.exists(dirpath):
            fs.makedirs(dirpath)

        with fs.open(persist_path, "w") as f:
            f.write(json.dumps(self._collections_mappings))

    @classmethod
    deffrom_persist_path(
        cls, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
    ) -> "SimpleKVStore":
"""Load a SimpleKVStore from a persist path and filesystem."""
        fs = fs or fsspec.filesystem("file")
        logger.debug(f"Loading {__name__} from {persist_path}.")
        with fs.open(persist_path, "rb") as f:
            data = json.load(f)
        return cls(data)

    defto_dict(self) -> dict:
"""Save the store as dict."""
        return self._collections_mappings.copy()

    @classmethod
    deffrom_dict(cls, save_dict: dict) -> "SimpleKVStore":
"""Load a SimpleKVStore from dict."""
        return cls(save_dict)

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/simple/#llama_index.core.storage.kvstore.SimpleKVStore.persist "Permanent link")

```
persist(
    persist_path: ,
    fs: Optional[AbstractFileSystem] = None,
) -> None

```

Persist the store.
Source code in `llama-index-core/llama_index/core/storage/kvstore/simple_kvstore.py`  
| 
```
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
```
 | 
```
defpersist(
    self, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
) -> None:
"""Persist the store."""
    fs = fs or fsspec.filesystem("file")
    dirpath = os.path.dirname(persist_path)
    if not fs.exists(dirpath):
        fs.makedirs(dirpath)

    with fs.open(persist_path, "w") as f:
        f.write(json.dumps(self._collections_mappings))

```
 |  
| --- | --- |  
###  from_persist_path `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/simple/#llama_index.core.storage.kvstore.SimpleKVStore.from_persist_path "Permanent link")

```
from_persist_path(
    persist_path: ,
    fs: Optional[AbstractFileSystem] = None,
) -> 

```

Load a SimpleKVStore from a persist path and filesystem.
Source code in `llama-index-core/llama_index/core/storage/kvstore/simple_kvstore.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_persist_path(
    cls, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
) -> "SimpleKVStore":
"""Load a SimpleKVStore from a persist path and filesystem."""
    fs = fs or fsspec.filesystem("file")
    logger.debug(f"Loading {__name__} from {persist_path}.")
    with fs.open(persist_path, "rb") as f:
        data = json.load(f)
    return cls(data)

```
 |  
| --- | --- |  
###  to_dict [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/simple/#llama_index.core.storage.kvstore.SimpleKVStore.to_dict "Permanent link")

```
to_dict() -> 

```

Save the store as dict.
Source code in `llama-index-core/llama_index/core/storage/kvstore/simple_kvstore.py`  
| 
```
58
59
60
```
 | 
```
defto_dict(self) -> dict:
"""Save the store as dict."""
    return self._collections_mappings.copy()

```
 |  
| --- | --- |  
###  from_dict `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/kvstore/simple/#llama_index.core.storage.kvstore.SimpleKVStore.from_dict "Permanent link")

```
from_dict(save_dict: ) -> 

```

Load a SimpleKVStore from dict.
Source code in `llama-index-core/llama_index/core/storage/kvstore/simple_kvstore.py`  
| 
```
62
63
64
65
```
 | 
```
@classmethod
deffrom_dict(cls, save_dict: dict) -> "SimpleKVStore":
"""Load a SimpleKVStore from dict."""
    return cls(save_dict)

```
 |  
| --- | --- |  
options: members: - SimpleKVStore
