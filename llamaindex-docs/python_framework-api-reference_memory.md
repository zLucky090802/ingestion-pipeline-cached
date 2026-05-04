# Index
##  BaseMemory [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseMemory "Permanent link")
Bases: 
Base class for all memory types.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
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
```
 | 
```
classBaseMemory(BaseComponent):
"""Base class for all memory types."""

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "BaseMemory"

    @classmethod
    @abstractmethod
    deffrom_defaults(
        cls,
        **kwargs: Any,
    ) -> "BaseMemory":
"""Create a chat memory from defaults."""

    @abstractmethod
    defget(self, input: Optional[str] = None, **kwargs: Any) -> List[ChatMessage]:
"""Get chat history."""

    async defaget(
        self, input: Optional[str] = None, **kwargs: Any
    ) -> List[ChatMessage]:
"""Get chat history."""
        return await asyncio.to_thread(self.get, input=input, **kwargs)

    @abstractmethod
    defget_all(self) -> List[ChatMessage]:
"""Get all chat history."""

    async defaget_all(self) -> List[ChatMessage]:
"""Get all chat history."""
        return await asyncio.to_thread(self.get_all)

    @abstractmethod
    defput(self, message: ChatMessage) -> None:
"""Put chat history."""

    async defaput(self, message: ChatMessage) -> None:
"""Put chat history."""
        await asyncio.to_thread(self.put, message)

    defput_messages(self, messages: List[ChatMessage]) -> None:
"""Put chat history."""
        for message in messages:
            self.put(message)

    async defaput_messages(self, messages: List[ChatMessage]) -> None:
"""Put chat history."""
        await asyncio.to_thread(self.put_messages, messages)

    @abstractmethod
    defset(self, messages: List[ChatMessage]) -> None:
"""Set chat history."""

    async defaset(self, messages: List[ChatMessage]) -> None:
"""Set chat history."""
        await asyncio.to_thread(self.set, messages)

    @abstractmethod
    defreset(self) -> None:
"""Reset chat history."""

    async defareset(self) -> None:
"""Reset chat history."""
        await asyncio.to_thread(self.reset)

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseMemory.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
17
18
19
20
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "BaseMemory"

```
 |  
| --- | --- |  
###  from_defaults `abstractmethod` `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseMemory.from_defaults "Permanent link")

```
from_defaults(**kwargs: ) -> 

```

Create a chat memory from defaults.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
22
23
24
25
26
27
28
```
 | 
```
@classmethod
@abstractmethod
deffrom_defaults(
    cls,
    **kwargs: Any,
) -> "BaseMemory":
"""Create a chat memory from defaults."""

```
 |  
| --- | --- |  
###  get `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseMemory.get "Permanent link")

```
get(
    input: Optional[] = None, **kwargs: 
) -> []

```

Get chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
30
31
32
```
 | 
```
@abstractmethod
defget(self, input: Optional[str] = None, **kwargs: Any) -> List[ChatMessage]:
"""Get chat history."""

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseMemory.aget "Permanent link")

```
aget(
    input: Optional[] = None, **kwargs: 
) -> []

```

Get chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
34
35
36
37
38
```
 | 
```
async defaget(
    self, input: Optional[str] = None, **kwargs: Any
) -> List[ChatMessage]:
"""Get chat history."""
    return await asyncio.to_thread(self.get, input=input, **kwargs)

```
 |  
| --- | --- |  
###  get_all `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseMemory.get_all "Permanent link")

```
get_all() -> []

```

Get all chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
40
41
42
```
 | 
```
@abstractmethod
defget_all(self) -> List[ChatMessage]:
"""Get all chat history."""

```
 |  
| --- | --- |  
###  aget_all [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseMemory.aget_all "Permanent link")

```
aget_all() -> []

```

Get all chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
44
45
46
```
 | 
```
async defaget_all(self) -> List[ChatMessage]:
"""Get all chat history."""
    return await asyncio.to_thread(self.get_all)

```
 |  
| --- | --- |  
###  put `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseMemory.put "Permanent link")

```
put(message: ) -> None

```

Put chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
48
49
50
```
 | 
```
@abstractmethod
defput(self, message: ChatMessage) -> None:
"""Put chat history."""

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseMemory.aput "Permanent link")

```
aput(message: ) -> None

```

Put chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
52
53
54
```
 | 
```
async defaput(self, message: ChatMessage) -> None:
"""Put chat history."""
    await asyncio.to_thread(self.put, message)

```
 |  
| --- | --- |  
###  put_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseMemory.put_messages "Permanent link")

```
put_messages(messages: []) -> None

```

Put chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
56
57
58
59
```
 | 
```
defput_messages(self, messages: List[ChatMessage]) -> None:
"""Put chat history."""
    for message in messages:
        self.put(message)

```
 |  
| --- | --- |  
###  aput_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseMemory.aput_messages "Permanent link")

```
aput_messages(messages: []) -> None

```

Put chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
61
62
63
```
 | 
```
async defaput_messages(self, messages: List[ChatMessage]) -> None:
"""Put chat history."""
    await asyncio.to_thread(self.put_messages, messages)

```
 |  
| --- | --- |  
###  set `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseMemory.set "Permanent link")

```
set(messages: []) -> None

```

Set chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
65
66
67
```
 | 
```
@abstractmethod
defset(self, messages: List[ChatMessage]) -> None:
"""Set chat history."""

```
 |  
| --- | --- |  
###  aset [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseMemory.aset "Permanent link")

```
aset(messages: []) -> None

```

Set chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
69
70
71
```
 | 
```
async defaset(self, messages: List[ChatMessage]) -> None:
"""Set chat history."""
    await asyncio.to_thread(self.set, messages)

```
 |  
| --- | --- |  
###  reset `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseMemory.reset "Permanent link")

```
reset() -> None

```

Reset chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
73
74
75
```
 | 
```
@abstractmethod
defreset(self) -> None:
"""Reset chat history."""

```
 |  
| --- | --- |  
###  areset [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseMemory.areset "Permanent link")

```
areset() -> None

```

Reset chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
77
78
79
```
 | 
```
async defareset(self) -> None:
"""Reset chat history."""
    await asyncio.to_thread(self.reset)

```
 |  
| --- | --- |  
##  BaseChatStoreMemory [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseChatStoreMemory "Permanent link")
Bases: 
Base class for storing multi-tenant chat history.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `chat_store`  |   |  Simple chat store. Async methods provide same functionality as sync methods in this class.  |  `<dynamic>`  |  
|  `chat_store_key`  |  `'chat_history'`  |  
Source code in `llama-index-core/llama_index/core/memory/types.py`  
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
```
 | 
```
classBaseChatStoreMemory(BaseMemory):
"""Base class for storing multi-tenant chat history."""

    chat_store: SerializeAsAny[BaseChatStore] = Field(default_factory=SimpleChatStore)
    chat_store_key: str = Field(default=DEFAULT_CHAT_STORE_KEY)

    @field_serializer("chat_store")
    defserialize_courses_in_order(self, chat_store: BaseChatStore) -> dict:
        res = chat_store.model_dump()
        res.update({"class_name": chat_store.class_name()})
        return res

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "BaseChatStoreMemory"

    @classmethod
    @abstractmethod
    deffrom_defaults(
        cls,
        chat_history: Optional[List[ChatMessage]] = None,
        llm: Optional[LLM] = None,
        **kwargs: Any,
    ) -> "BaseChatStoreMemory":
"""Create a chat memory from defaults."""

    defget_all(self) -> List[ChatMessage]:
"""Get all chat history."""
        return self.chat_store.get_messages(self.chat_store_key)

    async defaget_all(self) -> List[ChatMessage]:
"""Get all chat history."""
        return await self.chat_store.aget_messages(self.chat_store_key)

    defget(self, input: Optional[str] = None, **kwargs: Any) -> List[ChatMessage]:
"""Get chat history."""
        return self.chat_store.get_messages(self.chat_store_key, **kwargs)

    async defaget(
        self, input: Optional[str] = None, **kwargs: Any
    ) -> List[ChatMessage]:
"""Get chat history."""
        return await self.chat_store.aget_messages(self.chat_store_key, **kwargs)

    defput(self, message: ChatMessage) -> None:
"""Put chat history."""
        # ensure everything is serialized
        self.chat_store.add_message(self.chat_store_key, message)

    async defaput(self, message: ChatMessage) -> None:
"""Put chat history."""
        # ensure everything is serialized
        await self.chat_store.async_add_message(self.chat_store_key, message)

    defset(self, messages: List[ChatMessage]) -> None:
"""Set chat history."""
        self.chat_store.set_messages(self.chat_store_key, messages)

    async defaset(self, messages: List[ChatMessage]) -> None:
"""Set chat history."""
        # ensure everything is serialized
        await self.chat_store.aset_messages(self.chat_store_key, messages)

    defreset(self) -> None:
"""Reset chat history."""
        self.chat_store.delete_messages(self.chat_store_key)

    async defareset(self) -> None:
"""Reset chat history."""
        await self.chat_store.adelete_messages(self.chat_store_key)

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseChatStoreMemory.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
94
95
96
97
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "BaseChatStoreMemory"

```
 |  
| --- | --- |  
###  from_defaults `abstractmethod` `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseChatStoreMemory.from_defaults "Permanent link")

```
from_defaults(
    chat_history: Optional[[]] = None,
    llm: Optional[] = None,
    **kwargs: 
) -> 

```

Create a chat memory from defaults.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
 99
100
101
102
103
104
105
106
107
```
 | 
```
@classmethod
@abstractmethod
deffrom_defaults(
    cls,
    chat_history: Optional[List[ChatMessage]] = None,
    llm: Optional[LLM] = None,
    **kwargs: Any,
) -> "BaseChatStoreMemory":
"""Create a chat memory from defaults."""

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseChatStoreMemory.get_all "Permanent link")

```
get_all() -> []

```

Get all chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
109
110
111
```
 | 
```
defget_all(self) -> List[ChatMessage]:
"""Get all chat history."""
    return self.chat_store.get_messages(self.chat_store_key)

```
 |  
| --- | --- |  
###  aget_all [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseChatStoreMemory.aget_all "Permanent link")

```
aget_all() -> []

```

Get all chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
113
114
115
```
 | 
```
async defaget_all(self) -> List[ChatMessage]:
"""Get all chat history."""
    return await self.chat_store.aget_messages(self.chat_store_key)

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseChatStoreMemory.get "Permanent link")

```
get(
    input: Optional[] = None, **kwargs: 
) -> []

```

Get chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
117
118
119
```
 | 
```
defget(self, input: Optional[str] = None, **kwargs: Any) -> List[ChatMessage]:
"""Get chat history."""
    return self.chat_store.get_messages(self.chat_store_key, **kwargs)

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseChatStoreMemory.aget "Permanent link")

```
aget(
    input: Optional[] = None, **kwargs: 
) -> []

```

Get chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
121
122
123
124
125
```
 | 
```
async defaget(
    self, input: Optional[str] = None, **kwargs: Any
) -> List[ChatMessage]:
"""Get chat history."""
    return await self.chat_store.aget_messages(self.chat_store_key, **kwargs)

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseChatStoreMemory.put "Permanent link")

```
put(message: ) -> None

```

Put chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
127
128
129
130
```
 | 
```
defput(self, message: ChatMessage) -> None:
"""Put chat history."""
    # ensure everything is serialized
    self.chat_store.add_message(self.chat_store_key, message)

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseChatStoreMemory.aput "Permanent link")

```
aput(message: ) -> None

```

Put chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
132
133
134
135
```
 | 
```
async defaput(self, message: ChatMessage) -> None:
"""Put chat history."""
    # ensure everything is serialized
    await self.chat_store.async_add_message(self.chat_store_key, message)

```
 |  
| --- | --- |  
###  set [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseChatStoreMemory.set "Permanent link")

```
set(messages: []) -> None

```

Set chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
137
138
139
```
 | 
```
defset(self, messages: List[ChatMessage]) -> None:
"""Set chat history."""
    self.chat_store.set_messages(self.chat_store_key, messages)

```
 |  
| --- | --- |  
###  aset [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseChatStoreMemory.aset "Permanent link")

```
aset(messages: []) -> None

```

Set chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
141
142
143
144
```
 | 
```
async defaset(self, messages: List[ChatMessage]) -> None:
"""Set chat history."""
    # ensure everything is serialized
    await self.chat_store.aset_messages(self.chat_store_key, messages)

```
 |  
| --- | --- |  
###  reset [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseChatStoreMemory.reset "Permanent link")

```
reset() -> None

```

Reset chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
146
147
148
```
 | 
```
defreset(self) -> None:
"""Reset chat history."""
    self.chat_store.delete_messages(self.chat_store_key)

```
 |  
| --- | --- |  
###  areset [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseChatStoreMemory.areset "Permanent link")

```
areset() -> None

```

Reset chat history.
Source code in `llama-index-core/llama_index/core/memory/types.py`  
| 
```
150
151
152
```
 | 
```
async defareset(self) -> None:
"""Reset chat history."""
    await self.chat_store.adelete_messages(self.chat_store_key)

```
 |  
| --- | --- |
