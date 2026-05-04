# Simple composable memory
##  SimpleComposableMemory [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/simple_composable_memory/#llama_index.core.memory.simple_composable_memory.SimpleComposableMemory "Permanent link")
Bases: 
Deprecated: Please use `llama_index.core.memory.Memory` instead.
A simple composition of potentially several memory sources.
This composable memory considers one of the memory sources as the main one and the others as secondary. The secondary memory sources get added to the chat history only in either the system prompt or to the first user message within the chat history.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `primary_memory`  |   |  (BaseMemory) The main memory buffer for agent.  |  _required_  |  
|  `secondary_memory_sources`  |  `List[Annotated[BaseMemory[](https://developers.llamaindex.ai/python/framework-api-reference/memory/#llama_index.core.memory.types.BaseMemory "BaseMemory \(llama_index.core.memory.types.BaseMemory\)"), SerializeAsAny]]`  |  (List(BaseMemory)) Secondary memory sources. Retrieved messages from these sources get added to the system prompt message.  |  `<dynamic>`  |  
Source code in `llama-index-core/llama_index/core/memory/simple_composable_memory.py`  
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
```
 | 
```
classSimpleComposableMemory(BaseMemory):
"""
    Deprecated: Please use `llama_index.core.memory.Memory` instead.

    A simple composition of potentially several memory sources.

    This composable memory considers one of the memory sources as the main
    one and the others as secondary. The secondary memory sources get added to
    the chat history only in either the system prompt or to the first user
    message within the chat history.

    Args:
        primary_memory: (BaseMemory) The main memory buffer for agent.
        secondary_memory_sources: (List(BaseMemory)) Secondary memory sources.
            Retrieved messages from these sources get added to the system prompt message.

    """

    primary_memory: SerializeAsAny[BaseMemory] = Field(
        description="Primary memory source for chat agent.",
    )
    secondary_memory_sources: List[SerializeAsAny[BaseMemory]] = Field(
        default_factory=list, description="Secondary memory sources."
    )

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "SimpleComposableMemory"

    @classmethod
    deffrom_defaults(
        cls,
        primary_memory: Optional[BaseMemory] = None,
        secondary_memory_sources: Optional[List[BaseMemory]] = None,
        **kwargs: Any,
    ) -> "SimpleComposableMemory":
"""Create a simple composable memory from an LLM."""
        if kwargs:
            raise ValueError(f"Unexpected kwargs: {kwargs}")

        primary_memory = primary_memory or ChatMemoryBuffer.from_defaults()
        secondary_memory_sources = secondary_memory_sources or []

        return cls(
            primary_memory=primary_memory,
            secondary_memory_sources=secondary_memory_sources,
        )

    def_format_secondary_messages(
        self, secondary_chat_histories: List[List[ChatMessage]]
    ) -> str:
"""Formats retrieved historical messages into a single string."""
        # TODO: use PromptTemplate for this
        formatted_history = "\n\n" + DEFAULT_INTRO_HISTORY_MESSAGE + "\n"
        for ix, chat_history in enumerate(secondary_chat_histories):
            formatted_history += (
                f"\n=====Relevant messages from memory source {ix+1}=====\n\n"
            )
            for m in chat_history:
                formatted_history += f"\t{m.role.upper()}: {m.content}\n"
            formatted_history += (
                f"\n=====End of relevant messages from memory source {ix+1}======\n\n"
            )

        formatted_history += DEFAULT_OUTRO_HISTORY_MESSAGE
        return formatted_history

    defget(self, input: Optional[str] = None, **kwargs: Any) -> List[ChatMessage]:
"""Get chat history."""
        return self._compose_message_histories(input, **kwargs)

    def_compose_message_histories(
        self, input: Optional[str] = None, **kwargs: Any
    ) -> List[ChatMessage]:
"""Get chat history."""
        # get from primary
        messages = self.primary_memory.get(input=input, **kwargs)

        # get from secondary
        # TODO: remove any repeated messages in secondary and primary memory
        secondary_histories = []
        for mem in self.secondary_memory_sources:
            secondary_history = mem.get(input, **kwargs)
            secondary_history = [m for m in secondary_history if m not in messages]

            if len(secondary_history)  0:
                secondary_histories.append(secondary_history)

        # format secondary memory
        if len(secondary_histories)  0:
            single_secondary_memory_str = self._format_secondary_messages(
                secondary_histories
            )

            # add single_secondary_memory_str to chat_history
            if len(messages)  0 and messages[0].role == MessageRole.SYSTEM:
                assert messages[0].content is not None
                system_message = messages[0].content.split(
                    DEFAULT_INTRO_HISTORY_MESSAGE
                )[0]
                messages[0] = ChatMessage(
                    content=system_message.strip() + single_secondary_memory_str,
                    role=MessageRole.SYSTEM,
                )
            else:
                messages.insert(
                    0,
                    ChatMessage(
                        content="You are a helpful assistant."
                        + single_secondary_memory_str,
                        role=MessageRole.SYSTEM,
                    ),
                )
        return messages

    defget_all(self) -> List[ChatMessage]:
"""
        Get all chat history.

        Uses primary memory get_all only.
        """
        return self.primary_memory.get_all()

    defput(self, message: ChatMessage) -> None:
"""Put chat history."""
        self.primary_memory.put(message)
        for mem in self.secondary_memory_sources:
            mem.put(message)

    async defaput(self, message: ChatMessage) -> None:
"""Put chat history."""
        await self.primary_memory.aput(message)
        for mem in self.secondary_memory_sources:
            await mem.aput(message)

    defset(self, messages: List[ChatMessage]) -> None:
"""Set chat history."""
        self.primary_memory.set(messages)
        for mem in self.secondary_memory_sources:
            # finalize task often sets, but secondary memory is meant for
            # long-term memory rather than main chat memory buffer
            # so use put_messages instead
            mem.put_messages(messages)

    defreset(self) -> None:
"""Reset chat history."""
        self.primary_memory.reset()
        for mem in self.secondary_memory_sources:
            mem.reset()

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/simple_composable_memory/#llama_index.core.memory.simple_composable_memory.SimpleComposableMemory.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/memory/simple_composable_memory.py`  
| 
```
39
40
41
42
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "SimpleComposableMemory"

```
 |  
| --- | --- |  
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/simple_composable_memory/#llama_index.core.memory.simple_composable_memory.SimpleComposableMemory.from_defaults "Permanent link")

```
from_defaults(
    primary_memory: Optional[] = None,
    secondary_memory_sources: Optional[
        []
    ] = None,
    **kwargs: 
) -> 

```

Create a simple composable memory from an LLM.
Source code in `llama-index-core/llama_index/core/memory/simple_composable_memory.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    primary_memory: Optional[BaseMemory] = None,
    secondary_memory_sources: Optional[List[BaseMemory]] = None,
    **kwargs: Any,
) -> "SimpleComposableMemory":
"""Create a simple composable memory from an LLM."""
    if kwargs:
        raise ValueError(f"Unexpected kwargs: {kwargs}")

    primary_memory = primary_memory or ChatMemoryBuffer.from_defaults()
    secondary_memory_sources = secondary_memory_sources or []

    return cls(
        primary_memory=primary_memory,
        secondary_memory_sources=secondary_memory_sources,
    )

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/simple_composable_memory/#llama_index.core.memory.simple_composable_memory.SimpleComposableMemory.get "Permanent link")

```
get(
    input: Optional[] = None, **kwargs: 
) -> []

```

Get chat history.
Source code in `llama-index-core/llama_index/core/memory/simple_composable_memory.py`  
| 
```
82
83
84
```
 | 
```
defget(self, input: Optional[str] = None, **kwargs: Any) -> List[ChatMessage]:
"""Get chat history."""
    return self._compose_message_histories(input, **kwargs)

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/simple_composable_memory/#llama_index.core.memory.simple_composable_memory.SimpleComposableMemory.get_all "Permanent link")

```
get_all() -> []

```

Get all chat history.
Uses primary memory get_all only.
Source code in `llama-index-core/llama_index/core/memory/simple_composable_memory.py`  
| 
```
130
131
132
133
134
135
136
```
 | 
```
defget_all(self) -> List[ChatMessage]:
"""
    Get all chat history.

    Uses primary memory get_all only.
    """
    return self.primary_memory.get_all()

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/simple_composable_memory/#llama_index.core.memory.simple_composable_memory.SimpleComposableMemory.put "Permanent link")

```
put(message: ) -> None

```

Put chat history.
Source code in `llama-index-core/llama_index/core/memory/simple_composable_memory.py`  
| 
```
138
139
140
141
142
```
 | 
```
defput(self, message: ChatMessage) -> None:
"""Put chat history."""
    self.primary_memory.put(message)
    for mem in self.secondary_memory_sources:
        mem.put(message)

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/simple_composable_memory/#llama_index.core.memory.simple_composable_memory.SimpleComposableMemory.aput "Permanent link")

```
aput(message: ) -> None

```

Put chat history.
Source code in `llama-index-core/llama_index/core/memory/simple_composable_memory.py`  
| 
```
144
145
146
147
148
```
 | 
```
async defaput(self, message: ChatMessage) -> None:
"""Put chat history."""
    await self.primary_memory.aput(message)
    for mem in self.secondary_memory_sources:
        await mem.aput(message)

```
 |  
| --- | --- |  
###  set [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/simple_composable_memory/#llama_index.core.memory.simple_composable_memory.SimpleComposableMemory.set "Permanent link")

```
set(messages: []) -> None

```

Set chat history.
Source code in `llama-index-core/llama_index/core/memory/simple_composable_memory.py`  
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
```
 | 
```
defset(self, messages: List[ChatMessage]) -> None:
"""Set chat history."""
    self.primary_memory.set(messages)
    for mem in self.secondary_memory_sources:
        # finalize task often sets, but secondary memory is meant for
        # long-term memory rather than main chat memory buffer
        # so use put_messages instead
        mem.put_messages(messages)

```
 |  
| --- | --- |  
###  reset [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/simple_composable_memory/#llama_index.core.memory.simple_composable_memory.SimpleComposableMemory.reset "Permanent link")

```
reset() -> None

```

Reset chat history.
Source code in `llama-index-core/llama_index/core/memory/simple_composable_memory.py`  
| 
```
159
160
161
162
163
```
 | 
```
defreset(self) -> None:
"""Reset chat history."""
    self.primary_memory.reset()
    for mem in self.secondary_memory_sources:
        mem.reset()

```
 |  
| --- | --- |
