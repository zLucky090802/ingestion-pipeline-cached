# Simple
##  SimpleChatStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/simple/#llama_index.core.storage.chat_store.simple_chat_store.SimpleChatStore "Permanent link")
Bases: 
Simple chat store. Async methods provide same functionality as sync methods in this class.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `store`  |  `Dict[str, List[Annotated[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.llms.ChatMessage\)"), WrapSerializer]]]`  |  dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs dict(iterable) -> new dictionary initialized as if via: d = {} for k, v in iterable: d[k] = v dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list. For example: dict(one=1, two=2)  |  `<class 'dict'>`  |  
Source code in `llama-index-core/llama_index/core/storage/chat_store/simple_chat_store.py`  
| 
```
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
```
 | 
```
classSimpleChatStore(BaseChatStore):
"""Simple chat store. Async methods provide same functionality as sync methods in this class."""

    store: Dict[str, List[AnnotatedChatMessage]] = Field(default_factory=dict)

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "SimpleChatStore"

    defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Set messages for a key."""
        self.store[key] = messages

    defget_messages(self, key: str) -> List[ChatMessage]:
"""Get messages for a key."""
        return self.store.get(key, [])

    defadd_message(
        self, key: str, message: ChatMessage, idx: Optional[int] = None
    ) -> None:
"""Add a message for a key."""
        if idx is None:
            self.store.setdefault(key, []).append(message)
        else:
            self.store.setdefault(key, []).insert(idx, message)

    defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Delete messages for a key."""
        if key not in self.store:
            return None
        return self.store.pop(key)

    defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
        if key not in self.store:
            return None
        if idx >= len(self.store[key]):
            return None
        return self.store[key].pop(idx)

    defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete last message for a key."""
        if key not in self.store:
            return None
        return self.store[key].pop()

    defget_keys(self) -> List[str]:
"""Get all keys."""
        return list(self.store.keys())

    defpersist(
        self,
        persist_path: str = "chat_store.json",
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> None:
"""Persist the docstore to a file."""
        fs = fs or fsspec.filesystem("file")
        dirpath = os.path.dirname(persist_path)
        if not fs.exists(dirpath):
            fs.makedirs(dirpath)

        with fs.open(persist_path, "w") as f:
            f.write(self.json())

    @classmethod
    deffrom_persist_path(
        cls,
        persist_path: str = "chat_store.json",
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> "SimpleChatStore":
"""Create a SimpleChatStore from a persist path."""
        fs = fs or fsspec.filesystem("file")
        if not fs.exists(persist_path):
            return cls()
        with fs.open(persist_path, "r") as f:
            data = json.load(f)

        if isinstance(data, str):
            return cls.model_validate_json(data)
        else:
            return cls.model_validate(data)

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/simple/#llama_index.core.storage.chat_store.simple_chat_store.SimpleChatStore.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-core/llama_index/core/storage/chat_store/simple_chat_store.py`  
| 
```
36
37
38
39
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "SimpleChatStore"

```
 |  
| --- | --- |  
###  set_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/simple/#llama_index.core.storage.chat_store.simple_chat_store.SimpleChatStore.set_messages "Permanent link")

```
set_messages(key: , messages: []) -> None

```

Set messages for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/simple_chat_store.py`  
| 
```
41
42
43
```
 | 
```
defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Set messages for a key."""
    self.store[key] = messages

```
 |  
| --- | --- |  
###  get_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/simple/#llama_index.core.storage.chat_store.simple_chat_store.SimpleChatStore.get_messages "Permanent link")

```
get_messages(key: ) -> []

```

Get messages for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/simple_chat_store.py`  
| 
```
45
46
47
```
 | 
```
defget_messages(self, key: str) -> List[ChatMessage]:
"""Get messages for a key."""
    return self.store.get(key, [])

```
 |  
| --- | --- |  
###  add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/simple/#llama_index.core.storage.chat_store.simple_chat_store.SimpleChatStore.add_message "Permanent link")

```
add_message(
    key: ,
    message: ,
    idx: Optional[] = None,
) -> None

```

Add a message for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/simple_chat_store.py`  
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
```
 | 
```
defadd_message(
    self, key: str, message: ChatMessage, idx: Optional[int] = None
) -> None:
"""Add a message for a key."""
    if idx is None:
        self.store.setdefault(key, []).append(message)
    else:
        self.store.setdefault(key, []).insert(idx, message)

```
 |  
| --- | --- |  
###  delete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/simple/#llama_index.core.storage.chat_store.simple_chat_store.SimpleChatStore.delete_messages "Permanent link")

```
delete_messages(key: ) -> Optional[[]]

```

Delete messages for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/simple_chat_store.py`  
| 
```
58
59
60
61
62
```
 | 
```
defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Delete messages for a key."""
    if key not in self.store:
        return None
    return self.store.pop(key)

```
 |  
| --- | --- |  
###  delete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/simple/#llama_index.core.storage.chat_store.simple_chat_store.SimpleChatStore.delete_message "Permanent link")

```
delete_message(key: , idx: ) -> Optional[]

```

Delete specific message for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/simple_chat_store.py`  
| 
```
64
65
66
67
68
69
70
```
 | 
```
defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
    if key not in self.store:
        return None
    if idx >= len(self.store[key]):
        return None
    return self.store[key].pop(idx)

```
 |  
| --- | --- |  
###  delete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/simple/#llama_index.core.storage.chat_store.simple_chat_store.SimpleChatStore.delete_last_message "Permanent link")

```
delete_last_message(key: ) -> Optional[]

```

Delete last message for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/simple_chat_store.py`  
| 
```
72
73
74
75
76
```
 | 
```
defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete last message for a key."""
    if key not in self.store:
        return None
    return self.store[key].pop()

```
 |  
| --- | --- |  
###  get_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/simple/#llama_index.core.storage.chat_store.simple_chat_store.SimpleChatStore.get_keys "Permanent link")

```
get_keys() -> []

```

Get all keys.
Source code in `llama-index-core/llama_index/core/storage/chat_store/simple_chat_store.py`  
| 
```
78
79
80
```
 | 
```
defget_keys(self) -> List[str]:
"""Get all keys."""
    return list(self.store.keys())

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/simple/#llama_index.core.storage.chat_store.simple_chat_store.SimpleChatStore.persist "Permanent link")

```
persist(
    persist_path:  = "chat_store.json",
    fs: Optional[AbstractFileSystem] = None,
) -> None

```

Persist the docstore to a file.
Source code in `llama-index-core/llama_index/core/storage/chat_store/simple_chat_store.py`  
| 
```
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
```
 | 
```
defpersist(
    self,
    persist_path: str = "chat_store.json",
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> None:
"""Persist the docstore to a file."""
    fs = fs or fsspec.filesystem("file")
    dirpath = os.path.dirname(persist_path)
    if not fs.exists(dirpath):
        fs.makedirs(dirpath)

    with fs.open(persist_path, "w") as f:
        f.write(self.json())

```
 |  
| --- | --- |  
###  from_persist_path `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/simple/#llama_index.core.storage.chat_store.simple_chat_store.SimpleChatStore.from_persist_path "Permanent link")

```
from_persist_path(
    persist_path:  = "chat_store.json",
    fs: Optional[AbstractFileSystem] = None,
) -> 

```

Create a SimpleChatStore from a persist path.
Source code in `llama-index-core/llama_index/core/storage/chat_store/simple_chat_store.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_persist_path(
    cls,
    persist_path: str = "chat_store.json",
    fs: Optional[fsspec.AbstractFileSystem] = None,
) -> "SimpleChatStore":
"""Create a SimpleChatStore from a persist path."""
    fs = fs or fsspec.filesystem("file")
    if not fs.exists(persist_path):
        return cls()
    with fs.open(persist_path, "r") as f:
        data = json.load(f)

    if isinstance(data, str):
        return cls.model_validate_json(data)
    else:
        return cls.model_validate(data)

```
 |  
| --- | --- |  
options: members: - SimpleChatStore
