# Chat memory buffer
##  ChatMemoryBuffer [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/chat_memory_buffer/#llama_index.core.memory.chat_memory_buffer.ChatMemoryBuffer "Permanent link")
Bases: 
Deprecated: Please use `llama_index.core.memory.Memory` instead.
Simple buffer for storing chat history.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `token_limit`  |  _required_  |  
|  `tokenizer_fn`  |  `Callable[list, List]`  |  `<dynamic>`  |  
Source code in `llama-index-core/llama_index/core/memory/chat_memory_buffer.py`  
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
```
 | 
```
classChatMemoryBuffer(BaseChatStoreMemory):
"""
    Deprecated: Please use `llama_index.core.memory.Memory` instead.

    Simple buffer for storing chat history.
    """

    token_limit: int
    tokenizer_fn: Callable[[str], List] = Field(
        default_factory=get_tokenizer,
        exclude=True,
    )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "ChatMemoryBuffer"

    @model_validator(mode="before")
    @classmethod
    defvalidate_memory(cls, values: dict) -> dict:
        # Validate token limit
        token_limit = values.get("token_limit", -1)
        if token_limit  1:
            raise ValueError("Token limit must be set and greater than 0.")

        # Validate tokenizer -- this avoids errors when loading from json/dict
        tokenizer_fn = values.get("tokenizer_fn")
        if tokenizer_fn is None:
            values["tokenizer_fn"] = get_tokenizer()

        return values

    @classmethod
    deffrom_defaults(
        cls,
        chat_history: Optional[List[ChatMessage]] = None,
        llm: Optional[LLM] = None,
        chat_store: Optional[BaseChatStore] = None,
        chat_store_key: str = DEFAULT_CHAT_STORE_KEY,
        token_limit: Optional[int] = None,
        tokenizer_fn: Optional[Callable[[str], List]] = None,
        **kwargs: Any,
    ) -> "ChatMemoryBuffer":
"""Create a chat memory buffer from an LLM."""
        if kwargs:
            raise ValueError(f"Unexpected kwargs: {kwargs}")

        if llm is not None:
            context_window = llm.metadata.context_window
            token_limit = token_limit or int(context_window * DEFAULT_TOKEN_LIMIT_RATIO)
        elif token_limit is None:
            token_limit = DEFAULT_TOKEN_LIMIT

        if chat_history is not None:
            chat_store = chat_store or SimpleChatStore()
            chat_store.set_messages(chat_store_key, chat_history)

        return cls(
            token_limit=token_limit,
            tokenizer_fn=tokenizer_fn or get_tokenizer(),
            chat_store=chat_store or SimpleChatStore(),
            chat_store_key=chat_store_key,
        )

    defto_string(self) -> str:
"""Convert memory to string."""
        return self.json()

    @classmethod
    deffrom_string(cls, json_str: str) -> "ChatMemoryBuffer":
"""Create a chat memory buffer from a string."""
        dict_obj = json.loads(json_str)
        return cls.from_dict(dict_obj)

    defto_dict(self, **kwargs: Any) -> dict:
"""Convert memory to dict."""
        return self.dict()

    @classmethod
    deffrom_dict(cls, data: Dict[str, Any], **kwargs: Any) -> "ChatMemoryBuffer":
        fromllama_index.core.storage.chat_store.loadingimport load_chat_store

        # NOTE: this handles backwards compatibility with the old chat history
        if "chat_history" in data:
            chat_history = data.pop("chat_history")
            simple_store = SimpleChatStore(store={DEFAULT_CHAT_STORE_KEY: chat_history})
            data["chat_store"] = simple_store
        elif "chat_store" in data:
            chat_store_dict = data.pop("chat_store")
            chat_store = load_chat_store(chat_store_dict)
            data["chat_store"] = chat_store

        return cls(**data)

    defget(
        self, input: Optional[str] = None, initial_token_count: int = 0, **kwargs: Any
    ) -> List[ChatMessage]:
"""Get chat history."""
        chat_history = self.get_all()

        if initial_token_count  self.token_limit:
            raise ValueError("Initial token count exceeds token limit")

        message_count = len(chat_history)

        cur_messages = chat_history[-message_count:]
        token_count = self._token_count_for_messages(cur_messages) + initial_token_count

        while token_count  self.token_limit and message_count  1:
            message_count -= 1
            while message_count  1 and chat_history[-message_count].role in (
                MessageRole.TOOL,
                MessageRole.ASSISTANT,
            ):
                # we cannot have an assistant message at the start of the chat history
                # if after removal of the first, we have an assistant message,
                # we need to remove the assistant message too
                #
                # all tool messages should be preceded by an assistant message
                # if we remove a tool message, we need to remove the assistant message too
                message_count -= 1

            cur_messages = chat_history[-message_count:]
            token_count = (
                self._token_count_for_messages(cur_messages) + initial_token_count
            )

        # catch one message longer than token limit, return the most recent message
        # this allows the LLM to raise an error about the message being too long,
        # rather than having a silent/less obvious failure mode
        if token_count  self.token_limit or message_count <= 0:
            return chat_history[-1:]

        return chat_history[-message_count:]

    async defaget(
        self, input: Optional[str] = None, initial_token_count: int = 0, **kwargs: Any
    ) -> List[ChatMessage]:
"""Get chat history."""
        return await asyncio.to_thread(
            self.get, input=input, initial_token_count=initial_token_count, **kwargs
        )

    def_token_count_for_messages(self, messages: List[ChatMessage]) -> int:
        if len(messages) <= 0:
            return 0

        msg_str = " ".join(str(m.content) for m in messages)
        return len(self.tokenizer_fn(msg_str))

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/chat_memory_buffer/#llama_index.core.memory.chat_memory_buffer.ChatMemoryBuffer.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-core/llama_index/core/memory/chat_memory_buffer.py`  
| 
```
32
33
34
35
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "ChatMemoryBuffer"

```
 |  
| --- | --- |  
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/chat_memory_buffer/#llama_index.core.memory.chat_memory_buffer.ChatMemoryBuffer.from_defaults "Permanent link")

```
from_defaults(
    chat_history: Optional[[]] = None,
    llm: Optional[] = None,
    chat_store: Optional[] = None,
    chat_store_key:  = DEFAULT_CHAT_STORE_KEY,
    token_limit: Optional[] = None,
    tokenizer_fn: Optional[Callable[[], ]] = None,
    **kwargs: 
) -> 

```

Create a chat memory buffer from an LLM.
Source code in `llama-index-core/llama_index/core/memory/chat_memory_buffer.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    chat_history: Optional[List[ChatMessage]] = None,
    llm: Optional[LLM] = None,
    chat_store: Optional[BaseChatStore] = None,
    chat_store_key: str = DEFAULT_CHAT_STORE_KEY,
    token_limit: Optional[int] = None,
    tokenizer_fn: Optional[Callable[[str], List]] = None,
    **kwargs: Any,
) -> "ChatMemoryBuffer":
"""Create a chat memory buffer from an LLM."""
    if kwargs:
        raise ValueError(f"Unexpected kwargs: {kwargs}")

    if llm is not None:
        context_window = llm.metadata.context_window
        token_limit = token_limit or int(context_window * DEFAULT_TOKEN_LIMIT_RATIO)
    elif token_limit is None:
        token_limit = DEFAULT_TOKEN_LIMIT

    if chat_history is not None:
        chat_store = chat_store or SimpleChatStore()
        chat_store.set_messages(chat_store_key, chat_history)

    return cls(
        token_limit=token_limit,
        tokenizer_fn=tokenizer_fn or get_tokenizer(),
        chat_store=chat_store or SimpleChatStore(),
        chat_store_key=chat_store_key,
    )

```
 |  
| --- | --- |  
###  to_string [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/chat_memory_buffer/#llama_index.core.memory.chat_memory_buffer.ChatMemoryBuffer.to_string "Permanent link")

```
to_string() -> 

```

Convert memory to string.
Source code in `llama-index-core/llama_index/core/memory/chat_memory_buffer.py`  
| 
```
84
85
86
```
 | 
```
defto_string(self) -> str:
"""Convert memory to string."""
    return self.json()

```
 |  
| --- | --- |  
###  from_string `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/chat_memory_buffer/#llama_index.core.memory.chat_memory_buffer.ChatMemoryBuffer.from_string "Permanent link")

```
from_string(json_str: ) -> 

```

Create a chat memory buffer from a string.
Source code in `llama-index-core/llama_index/core/memory/chat_memory_buffer.py`  
| 
```
88
89
90
91
92
```
 | 
```
@classmethod
deffrom_string(cls, json_str: str) -> "ChatMemoryBuffer":
"""Create a chat memory buffer from a string."""
    dict_obj = json.loads(json_str)
    return cls.from_dict(dict_obj)

```
 |  
| --- | --- |  
###  to_dict [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/chat_memory_buffer/#llama_index.core.memory.chat_memory_buffer.ChatMemoryBuffer.to_dict "Permanent link")

```
to_dict(**kwargs: ) -> 

```

Convert memory to dict.
Source code in `llama-index-core/llama_index/core/memory/chat_memory_buffer.py`  
| 
```
94
95
96
```
 | 
```
defto_dict(self, **kwargs: Any) -> dict:
"""Convert memory to dict."""
    return self.dict()

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/chat_memory_buffer/#llama_index.core.memory.chat_memory_buffer.ChatMemoryBuffer.get "Permanent link")

```
get(
    input: Optional[] = None,
    initial_token_count:  = 0,
    **kwargs: 
) -> []

```

Get chat history.
Source code in `llama-index-core/llama_index/core/memory/chat_memory_buffer.py`  
| 
```
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
```
 | 
```
defget(
    self, input: Optional[str] = None, initial_token_count: int = 0, **kwargs: Any
) -> List[ChatMessage]:
"""Get chat history."""
    chat_history = self.get_all()

    if initial_token_count  self.token_limit:
        raise ValueError("Initial token count exceeds token limit")

    message_count = len(chat_history)

    cur_messages = chat_history[-message_count:]
    token_count = self._token_count_for_messages(cur_messages) + initial_token_count

    while token_count  self.token_limit and message_count  1:
        message_count -= 1
        while message_count  1 and chat_history[-message_count].role in (
            MessageRole.TOOL,
            MessageRole.ASSISTANT,
        ):
            # we cannot have an assistant message at the start of the chat history
            # if after removal of the first, we have an assistant message,
            # we need to remove the assistant message too
            #
            # all tool messages should be preceded by an assistant message
            # if we remove a tool message, we need to remove the assistant message too
            message_count -= 1

        cur_messages = chat_history[-message_count:]
        token_count = (
            self._token_count_for_messages(cur_messages) + initial_token_count
        )

    # catch one message longer than token limit, return the most recent message
    # this allows the LLM to raise an error about the message being too long,
    # rather than having a silent/less obvious failure mode
    if token_count  self.token_limit or message_count <= 0:
        return chat_history[-1:]

    return chat_history[-message_count:]

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/chat_memory_buffer/#llama_index.core.memory.chat_memory_buffer.ChatMemoryBuffer.aget "Permanent link")

```
aget(
    input: Optional[] = None,
    initial_token_count:  = 0,
    **kwargs: 
) -> []

```

Get chat history.
Source code in `llama-index-core/llama_index/core/memory/chat_memory_buffer.py`  
| 
```
155
156
157
158
159
160
161
```
 | 
```
async defaget(
    self, input: Optional[str] = None, initial_token_count: int = 0, **kwargs: Any
) -> List[ChatMessage]:
"""Get chat history."""
    return await asyncio.to_thread(
        self.get, input=input, initial_token_count=initial_token_count, **kwargs
    )

```
 |  
| --- | --- |
