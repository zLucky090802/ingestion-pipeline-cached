# Index
Base interface class for storing chat history per user.
##  BaseChatStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/#llama_index.core.storage.chat_store.base.BaseChatStore "Permanent link")
Bases: 
Source code in `llama-index-core/llama_index/core/storage/chat_store/base.py`  
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
75
76
77
78
```
 | 
```
classBaseChatStore(BaseComponent):
    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "BaseChatStore"

    @abstractmethod
    defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Set messages for a key."""
        ...

    @abstractmethod
    defget_messages(self, key: str) -> List[ChatMessage]:
"""Get messages for a key."""
        ...

    @abstractmethod
    defadd_message(self, key: str, message: ChatMessage) -> None:
"""Add a message for a key."""
        ...

    @abstractmethod
    defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Delete messages for a key."""
        ...

    @abstractmethod
    defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
        ...

    @abstractmethod
    defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete last message for a key."""
        ...

    @abstractmethod
    defget_keys(self) -> List[str]:
"""Get all keys."""
        ...

    async defaset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Async version of Get messages for a key."""
        await asyncio.to_thread(self.set_messages, key, messages)

    async defaget_messages(self, key: str) -> List[ChatMessage]:
"""Async version of Get messages for a key."""
        return await asyncio.to_thread(self.get_messages, key)

    async defasync_add_message(self, key: str, message: ChatMessage) -> None:
"""Async version of Add a message for a key."""
        await asyncio.to_thread(self.add_message, key, message)

    async defadelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Async version of Delete messages for a key."""
        return await asyncio.to_thread(self.delete_messages, key)

    async defadelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Async version of Delete specific message for a key."""
        return await asyncio.to_thread(self.delete_message, key, idx)

    async defadelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Async version of Delete last message for a key."""
        return await asyncio.to_thread(self.delete_last_message, key)

    async defaget_keys(self) -> List[str]:
"""Async version of Get all keys."""
        return await asyncio.to_thread(self.get_keys)

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/#llama_index.core.storage.chat_store.base.BaseChatStore.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-core/llama_index/core/storage/chat_store/base.py`  
| 
```
12
13
14
15
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "BaseChatStore"

```
 |  
| --- | --- |  
###  set_messages `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/#llama_index.core.storage.chat_store.base.BaseChatStore.set_messages "Permanent link")

```
set_messages(key: , messages: []) -> None

```

Set messages for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/base.py`  
| 
```
17
18
19
20
```
 | 
```
@abstractmethod
defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Set messages for a key."""
    ...

```
 |  
| --- | --- |  
###  get_messages `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/#llama_index.core.storage.chat_store.base.BaseChatStore.get_messages "Permanent link")

```
get_messages(key: ) -> []

```

Get messages for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/base.py`  
| 
```
22
23
24
25
```
 | 
```
@abstractmethod
defget_messages(self, key: str) -> List[ChatMessage]:
"""Get messages for a key."""
    ...

```
 |  
| --- | --- |  
###  add_message `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/#llama_index.core.storage.chat_store.base.BaseChatStore.add_message "Permanent link")

```
add_message(key: , message: ) -> None

```

Add a message for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/base.py`  
| 
```
27
28
29
30
```
 | 
```
@abstractmethod
defadd_message(self, key: str, message: ChatMessage) -> None:
"""Add a message for a key."""
    ...

```
 |  
| --- | --- |  
###  delete_messages `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/#llama_index.core.storage.chat_store.base.BaseChatStore.delete_messages "Permanent link")

```
delete_messages(key: ) -> Optional[[]]

```

Delete messages for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/base.py`  
| 
```
32
33
34
35
```
 | 
```
@abstractmethod
defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Delete messages for a key."""
    ...

```
 |  
| --- | --- |  
###  delete_message `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/#llama_index.core.storage.chat_store.base.BaseChatStore.delete_message "Permanent link")

```
delete_message(key: , idx: ) -> Optional[]

```

Delete specific message for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/base.py`  
| 
```
37
38
39
40
```
 | 
```
@abstractmethod
defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
    ...

```
 |  
| --- | --- |  
###  delete_last_message `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/#llama_index.core.storage.chat_store.base.BaseChatStore.delete_last_message "Permanent link")

```
delete_last_message(key: ) -> Optional[]

```

Delete last message for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/base.py`  
| 
```
42
43
44
45
```
 | 
```
@abstractmethod
defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete last message for a key."""
    ...

```
 |  
| --- | --- |  
###  get_keys `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/#llama_index.core.storage.chat_store.base.BaseChatStore.get_keys "Permanent link")

```
get_keys() -> []

```

Get all keys.
Source code in `llama-index-core/llama_index/core/storage/chat_store/base.py`  
| 
```
47
48
49
50
```
 | 
```
@abstractmethod
defget_keys(self) -> List[str]:
"""Get all keys."""
    ...

```
 |  
| --- | --- |  
###  aset_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/#llama_index.core.storage.chat_store.base.BaseChatStore.aset_messages "Permanent link")

```
aset_messages(
    key: , messages: []
) -> None

```

Async version of Get messages for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/base.py`  
| 
```
52
53
54
```
 | 
```
async defaset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Async version of Get messages for a key."""
    await asyncio.to_thread(self.set_messages, key, messages)

```
 |  
| --- | --- |  
###  aget_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/#llama_index.core.storage.chat_store.base.BaseChatStore.aget_messages "Permanent link")

```
aget_messages(key: ) -> []

```

Async version of Get messages for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/base.py`  
| 
```
56
57
58
```
 | 
```
async defaget_messages(self, key: str) -> List[ChatMessage]:
"""Async version of Get messages for a key."""
    return await asyncio.to_thread(self.get_messages, key)

```
 |  
| --- | --- |  
###  async_add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/#llama_index.core.storage.chat_store.base.BaseChatStore.async_add_message "Permanent link")

```
async_add_message(key: , message: ) -> None

```

Async version of Add a message for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/base.py`  
| 
```
60
61
62
```
 | 
```
async defasync_add_message(self, key: str, message: ChatMessage) -> None:
"""Async version of Add a message for a key."""
    await asyncio.to_thread(self.add_message, key, message)

```
 |  
| --- | --- |  
###  adelete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/#llama_index.core.storage.chat_store.base.BaseChatStore.adelete_messages "Permanent link")

```
adelete_messages(key: ) -> Optional[[]]

```

Async version of Delete messages for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/base.py`  
| 
```
64
65
66
```
 | 
```
async defadelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Async version of Delete messages for a key."""
    return await asyncio.to_thread(self.delete_messages, key)

```
 |  
| --- | --- |  
###  adelete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/#llama_index.core.storage.chat_store.base.BaseChatStore.adelete_message "Permanent link")

```
adelete_message(
    key: , idx: 
) -> Optional[]

```

Async version of Delete specific message for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/base.py`  
| 
```
68
69
70
```
 | 
```
async defadelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Async version of Delete specific message for a key."""
    return await asyncio.to_thread(self.delete_message, key, idx)

```
 |  
| --- | --- |  
###  adelete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/#llama_index.core.storage.chat_store.base.BaseChatStore.adelete_last_message "Permanent link")

```
adelete_last_message(key: ) -> Optional[]

```

Async version of Delete last message for a key.
Source code in `llama-index-core/llama_index/core/storage/chat_store/base.py`  
| 
```
72
73
74
```
 | 
```
async defadelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Async version of Delete last message for a key."""
    return await asyncio.to_thread(self.delete_last_message, key)

```
 |  
| --- | --- |  
###  aget_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/#llama_index.core.storage.chat_store.base.BaseChatStore.aget_keys "Permanent link")

```
aget_keys() -> []

```

Async version of Get all keys.
Source code in `llama-index-core/llama_index/core/storage/chat_store/base.py`  
| 
```
76
77
78
```
 | 
```
async defaget_keys(self) -> List[str]:
"""Async version of Get all keys."""
    return await asyncio.to_thread(self.get_keys)

```
 |  
| --- | --- |  
options: members: - BaseChatStore
