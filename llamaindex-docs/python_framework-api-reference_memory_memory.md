# Memory
##  ChatMemoryBuffer [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatMemoryBuffer "Permanent link")
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
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatMemoryBuffer.class_name "Permanent link")

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
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatMemoryBuffer.from_defaults "Permanent link")

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
###  to_string [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatMemoryBuffer.to_string "Permanent link")

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
###  from_string `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatMemoryBuffer.from_string "Permanent link")

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
###  to_dict [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatMemoryBuffer.to_dict "Permanent link")

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
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatMemoryBuffer.get "Permanent link")

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
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatMemoryBuffer.aget "Permanent link")

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
##  ChatSummaryMemoryBuffer [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatSummaryMemoryBuffer "Permanent link")
Bases: 
Deprecated: Please use `llama_index.core.memory.Memory` instead.
Buffer for storing chat history that uses the full text for the latest {token_limit}.
All older messages are iteratively summarized using the {llm} provided, with the max number of tokens defined by the {llm}.
User can specify whether initial tokens (usually a system prompt) should be counted as part of the {token_limit} using the parameter {count_initial_tokens}.
This buffer is useful to retain the most important information from a long chat history, while limiting the token count and latency of each request to the LLM.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `token_limit`  |  _required_  |  
|  `count_initial_tokens`  |  `bool`  |  `False`  |  
|  `llm`  |  `Annotated[LLM[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.LLM "LLM \(llama_index.core.llms.llm.LLM\)"), SerializeAsAny] | None`  |  `None`  |  
|  `summarize_prompt`  |  `str | None`  |  `None`  |  
|  `tokenizer_fn`  |  `Callable[list, List]`  |  `<dynamic>`  |  
|  `chat_store`  |   |  Simple chat store. Async methods provide same functionality as sync methods in this class.  |  `<dynamic>`  |  
|  `chat_store_key`  |  `'chat_history'`  |  
Source code in `llama-index-core/llama_index/core/memory/chat_summary_memory_buffer.py`  
| 
```
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
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
```
 | 
```
classChatSummaryMemoryBuffer(BaseMemory):
"""
    Deprecated: Please use `llama_index.core.memory.Memory` instead.

    Buffer for storing chat history that uses the full text for the latest
    {token_limit}.

    All older messages are iteratively summarized using the {llm} provided, with
    the max number of tokens defined by the {llm}.

    User can specify whether initial tokens (usually a system prompt)
    should be counted as part of the {token_limit}
    using the parameter {count_initial_tokens}.

    This buffer is useful to retain the most important information from a
    long chat history, while limiting the token count and latency
    of each request to the LLM.
    """

    token_limit: int
    count_initial_tokens: bool = False
    llm: Optional[SerializeAsAny[LLM]] = None
    summarize_prompt: Optional[str] = None
    tokenizer_fn: Callable[[str], List] = Field(
        default_factory=get_tokenizer,
        exclude=True,
    )

    chat_store: SerializeAsAny[BaseChatStore] = Field(default_factory=SimpleChatStore)
    chat_store_key: str = Field(default=DEFAULT_CHAT_STORE_KEY)

    _token_count: int = PrivateAttr(default=0)

    @field_serializer("chat_store")
    defserialize_courses_in_order(self, chat_store: BaseChatStore) -> dict:
        res = chat_store.model_dump()
        res.update({"class_name": chat_store.class_name()})
        return res

    @model_validator(mode="before")
    @classmethod
    defvalidate_memory(cls, values: dict) -> dict:
"""Validate the memory."""
        # Validate token limits
        token_limit = values.get("token_limit", -1)
        if token_limit  1:
            raise ValueError(
                "Token limit for full-text messages must be set and greater than 0."
            )

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
        summarize_prompt: Optional[str] = None,
        count_initial_tokens: bool = False,
        **kwargs: Any,
    ) -> "ChatSummaryMemoryBuffer":
"""
        Create a chat memory buffer from an LLM
        and an initial list of chat history messages.
        """
        if kwargs:
            raise ValueError(f"Unexpected keyword arguments: {kwargs}")

        if llm is not None:
            context_window = llm.metadata.context_window
            token_limit = token_limit or int(context_window * DEFAULT_TOKEN_LIMIT_RATIO)
        elif token_limit is None:
            token_limit = DEFAULT_TOKEN_LIMIT

        chat_store = chat_store or SimpleChatStore()

        if chat_history is not None:
            chat_store.set_messages(chat_store_key, chat_history)

        summarize_prompt = summarize_prompt or SUMMARIZE_PROMPT
        return cls(
            llm=llm,
            token_limit=token_limit,
            # TODO: Check if we can get the tokenizer from the llm
            tokenizer_fn=tokenizer_fn or get_tokenizer(),
            summarize_prompt=summarize_prompt,
            chat_store=chat_store,
            chat_store_key=chat_store_key,
            count_initial_tokens=count_initial_tokens,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "ChatSummaryMemoryBuffer"

    defto_string(self) -> str:
"""Convert memory to string."""
        return self.json()

    defto_dict(self, **kwargs: Any) -> dict:
"""Convert memory to dict."""
        return self.dict()

    @classmethod
    deffrom_string(cls, json_str: str, **kwargs: Any) -> "ChatSummaryMemoryBuffer":
"""Create a chat memory buffer from a string."""
        dict_obj = json.loads(json_str)
        return cls.from_dict(dict_obj, **kwargs)

    @classmethod
    deffrom_dict(
        cls, data: Dict[str, Any], **kwargs: Any
    ) -> "ChatSummaryMemoryBuffer":
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

        # NOTE: The llm will have to be set manually in kwargs
        if "llm" in data:
            data.pop("llm")

        return cls(**data, **kwargs)

    defget(
        self, input: Optional[str] = None, initial_token_count: int = 0, **kwargs: Any
    ) -> List[ChatMessage]:
"""Get chat history."""
        chat_history = self.get_all()
        if len(chat_history) == 0:
            return []

        # Give the user the choice whether to count the system prompt or not
        if self.count_initial_tokens:
            if initial_token_count  self.token_limit:
                raise ValueError("Initial token count exceeds token limit")
            self._token_count = initial_token_count

        (
            chat_history_full_text,
            chat_history_to_be_summarized,
        ) = self._split_messages_summary_or_full_text(chat_history)

        if self.llm is None or len(chat_history_to_be_summarized) == 0:
            # Simply remove the message that don't fit the buffer anymore
            updated_history = chat_history_full_text
        else:
            updated_history = [
                self._summarize_oldest_chat_history(chat_history_to_be_summarized),
                *chat_history_full_text,
            ]

        self.reset()
        self._token_count = 0
        self.set(updated_history)

        return updated_history

    defget_all(self) -> List[ChatMessage]:
"""Get all chat history."""
        return self.chat_store.get_messages(self.chat_store_key)

    defput(self, message: ChatMessage) -> None:
"""Put chat history."""
        # ensure everything is serialized
        self.chat_store.add_message(self.chat_store_key, message)

    async defaput(self, message: ChatMessage) -> None:
"""Put chat history."""
        await self.chat_store.async_add_message(self.chat_store_key, message)

    defset(self, messages: List[ChatMessage]) -> None:
"""Set chat history."""
        self.chat_store.set_messages(self.chat_store_key, messages)

    defreset(self) -> None:
"""Reset chat history."""
        self.chat_store.delete_messages(self.chat_store_key)

    defget_token_count(self) -> int:
"""Returns the token count of the memory buffer (excluding the last assistant response)."""
        return self._token_count

    def_token_count_for_messages(self, messages: List[ChatMessage]) -> int:
"""Get token count for list of messages."""
        if len(messages) <= 0:
            return 0

        msg_str = " ".join(str(m.content) for m in messages)
        return len(self.tokenizer_fn(msg_str))

    def_split_messages_summary_or_full_text(
        self, chat_history: List[ChatMessage]
    ) -> Tuple[List[ChatMessage], List[ChatMessage]]:
"""
        Determine which messages will be included as full text,
        and which will have to be summarized by the llm.
        """
        chat_history_full_text: List[ChatMessage] = []
        message_count = len(chat_history)
        while (
            message_count  0
            and self.get_token_count()
            + self._token_count_for_messages([chat_history[-1]])
            <= self.token_limit
        ):
            # traverse the history in reverse order, when token limit is about to be
            # exceeded, we stop, so remaining messages are summarized
            self._token_count += self._token_count_for_messages([chat_history[-1]])
            chat_history_full_text.insert(0, chat_history.pop())
            message_count -= 1

        chat_history_to_be_summarized = chat_history.copy()
        self._handle_assistant_and_tool_messages(
            chat_history_full_text, chat_history_to_be_summarized
        )

        return chat_history_full_text, chat_history_to_be_summarized

    def_summarize_oldest_chat_history(
        self, chat_history_to_be_summarized: List[ChatMessage]
    ) -> ChatMessage:
"""
        Use the llm to summarize the messages that do not fit into the
        buffer.
        """
        assert self.llm is not None

        # Only summarize if there is new information to be summarized
        if (
            len(chat_history_to_be_summarized) == 1
            and chat_history_to_be_summarized[0].role == MessageRole.SYSTEM
        ):
            return chat_history_to_be_summarized[0]

        summarize_prompt = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content=self.summarize_prompt,
            )
        ]
        summarize_prompt.append(
            ChatMessage(
                role=MessageRole.USER,
                content=self._get_prompt_to_summarize(chat_history_to_be_summarized),
            )
        )
        # TODO: Maybe it is better to pass a list of history to llm
        r = self.llm.chat(summarize_prompt)
        return ChatMessage(
            role=MessageRole.SYSTEM,
            content=r.message.content,
        )

    def_get_prompt_to_summarize(
        self, chat_history_to_be_summarized: List[ChatMessage]
    ) -> str:
"""Ask the LLM to summarize the chat history so far."""
        # TODO: This probably works better when question/answers are considered together.
        prompt = '"Transcript so far: '
        for msg in chat_history_to_be_summarized:
            if not isinstance(msg.content, str):
                continue

            prompt += msg.role + ": "
            if msg.content:
                prompt += msg.content + "\n\n"
            else:
                prompt += (
                    "\n".join(
                        [
                            f"Calling a function: {call!s}"
                            for call in msg.additional_kwargs.get("tool_calls", [])
                        ]
                    )
                    + "\n\n"
                )
        prompt += '"\n\n'
        return prompt

    def_handle_assistant_and_tool_messages(
        self,
        chat_history_full_text: List[ChatMessage],
        chat_history_to_be_summarized: List[ChatMessage],
    ) -> None:
"""
        To avoid breaking API's, we need to ensure the following.

        - the first message cannot be ASSISTANT
        - ASSISTANT/TOOL should be considered in pairs
        Therefore, we switch messages to summarized list until the first message is
        not an ASSISTANT or TOOL message.
        """
        while chat_history_full_text and chat_history_full_text[0].role in (
            MessageRole.ASSISTANT,
            MessageRole.TOOL,
        ):
            chat_history_to_be_summarized.append(chat_history_full_text.pop(0))

```
 |  
| --- | --- |  
###  validate_memory `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatSummaryMemoryBuffer.validate_memory "Permanent link")

```
validate_memory(values: ) -> 

```

Validate the memory.
Source code in `llama-index-core/llama_index/core/memory/chat_summary_memory_buffer.py`  
| 
```
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
```
 | 
```
@model_validator(mode="before")
@classmethod
defvalidate_memory(cls, values: dict) -> dict:
"""Validate the memory."""
    # Validate token limits
    token_limit = values.get("token_limit", -1)
    if token_limit  1:
        raise ValueError(
            "Token limit for full-text messages must be set and greater than 0."
        )

    # Validate tokenizer -- this avoids errors when loading from json/dict
    tokenizer_fn = values.get("tokenizer_fn")
    if tokenizer_fn is None:
        values["tokenizer_fn"] = get_tokenizer()

    return values

```
 |  
| --- | --- |  
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatSummaryMemoryBuffer.from_defaults "Permanent link")

```
from_defaults(
    chat_history: Optional[[]] = None,
    llm: Optional[] = None,
    chat_store: Optional[] = None,
    chat_store_key:  = DEFAULT_CHAT_STORE_KEY,
    token_limit: Optional[] = None,
    tokenizer_fn: Optional[Callable[[], ]] = None,
    summarize_prompt: Optional[] = None,
    count_initial_tokens:  = False,
    **kwargs: 
) -> 

```

Create a chat memory buffer from an LLM and an initial list of chat history messages.
Source code in `llama-index-core/llama_index/core/memory/chat_summary_memory_buffer.py`  
| 
```
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
    summarize_prompt: Optional[str] = None,
    count_initial_tokens: bool = False,
    **kwargs: Any,
) -> "ChatSummaryMemoryBuffer":
"""
    Create a chat memory buffer from an LLM
    and an initial list of chat history messages.
    """
    if kwargs:
        raise ValueError(f"Unexpected keyword arguments: {kwargs}")

    if llm is not None:
        context_window = llm.metadata.context_window
        token_limit = token_limit or int(context_window * DEFAULT_TOKEN_LIMIT_RATIO)
    elif token_limit is None:
        token_limit = DEFAULT_TOKEN_LIMIT

    chat_store = chat_store or SimpleChatStore()

    if chat_history is not None:
        chat_store.set_messages(chat_store_key, chat_history)

    summarize_prompt = summarize_prompt or SUMMARIZE_PROMPT
    return cls(
        llm=llm,
        token_limit=token_limit,
        # TODO: Check if we can get the tokenizer from the llm
        tokenizer_fn=tokenizer_fn or get_tokenizer(),
        summarize_prompt=summarize_prompt,
        chat_store=chat_store,
        chat_store_key=chat_store_key,
        count_initial_tokens=count_initial_tokens,
    )

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatSummaryMemoryBuffer.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-core/llama_index/core/memory/chat_summary_memory_buffer.py`  
| 
```
126
127
128
129
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "ChatSummaryMemoryBuffer"

```
 |  
| --- | --- |  
###  to_string [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatSummaryMemoryBuffer.to_string "Permanent link")

```
to_string() -> 

```

Convert memory to string.
Source code in `llama-index-core/llama_index/core/memory/chat_summary_memory_buffer.py`  
| 
```
131
132
133
```
 | 
```
defto_string(self) -> str:
"""Convert memory to string."""
    return self.json()

```
 |  
| --- | --- |  
###  to_dict [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatSummaryMemoryBuffer.to_dict "Permanent link")

```
to_dict(**kwargs: ) -> 

```

Convert memory to dict.
Source code in `llama-index-core/llama_index/core/memory/chat_summary_memory_buffer.py`  
| 
```
135
136
137
```
 | 
```
defto_dict(self, **kwargs: Any) -> dict:
"""Convert memory to dict."""
    return self.dict()

```
 |  
| --- | --- |  
###  from_string `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatSummaryMemoryBuffer.from_string "Permanent link")

```
from_string(
    json_str: , **kwargs: 
) -> 

```

Create a chat memory buffer from a string.
Source code in `llama-index-core/llama_index/core/memory/chat_summary_memory_buffer.py`  
| 
```
139
140
141
142
143
```
 | 
```
@classmethod
deffrom_string(cls, json_str: str, **kwargs: Any) -> "ChatSummaryMemoryBuffer":
"""Create a chat memory buffer from a string."""
    dict_obj = json.loads(json_str)
    return cls.from_dict(dict_obj, **kwargs)

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatSummaryMemoryBuffer.get "Permanent link")

```
get(
    input: Optional[] = None,
    initial_token_count:  = 0,
    **kwargs: 
) -> []

```

Get chat history.
Source code in `llama-index-core/llama_index/core/memory/chat_summary_memory_buffer.py`  
| 
```
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
```
 | 
```
defget(
    self, input: Optional[str] = None, initial_token_count: int = 0, **kwargs: Any
) -> List[ChatMessage]:
"""Get chat history."""
    chat_history = self.get_all()
    if len(chat_history) == 0:
        return []

    # Give the user the choice whether to count the system prompt or not
    if self.count_initial_tokens:
        if initial_token_count  self.token_limit:
            raise ValueError("Initial token count exceeds token limit")
        self._token_count = initial_token_count

    (
        chat_history_full_text,
        chat_history_to_be_summarized,
    ) = self._split_messages_summary_or_full_text(chat_history)

    if self.llm is None or len(chat_history_to_be_summarized) == 0:
        # Simply remove the message that don't fit the buffer anymore
        updated_history = chat_history_full_text
    else:
        updated_history = [
            self._summarize_oldest_chat_history(chat_history_to_be_summarized),
            *chat_history_full_text,
        ]

    self.reset()
    self._token_count = 0
    self.set(updated_history)

    return updated_history

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatSummaryMemoryBuffer.get_all "Permanent link")

```
get_all() -> []

```

Get all chat history.
Source code in `llama-index-core/llama_index/core/memory/chat_summary_memory_buffer.py`  
| 
```
201
202
203
```
 | 
```
defget_all(self) -> List[ChatMessage]:
"""Get all chat history."""
    return self.chat_store.get_messages(self.chat_store_key)

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatSummaryMemoryBuffer.put "Permanent link")

```
put(message: ) -> None

```

Put chat history.
Source code in `llama-index-core/llama_index/core/memory/chat_summary_memory_buffer.py`  
| 
```
205
206
207
208
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
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatSummaryMemoryBuffer.aput "Permanent link")

```
aput(message: ) -> None

```

Put chat history.
Source code in `llama-index-core/llama_index/core/memory/chat_summary_memory_buffer.py`  
| 
```
210
211
212
```
 | 
```
async defaput(self, message: ChatMessage) -> None:
"""Put chat history."""
    await self.chat_store.async_add_message(self.chat_store_key, message)

```
 |  
| --- | --- |  
###  set [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatSummaryMemoryBuffer.set "Permanent link")

```
set(messages: []) -> None

```

Set chat history.
Source code in `llama-index-core/llama_index/core/memory/chat_summary_memory_buffer.py`  
| 
```
214
215
216
```
 | 
```
defset(self, messages: List[ChatMessage]) -> None:
"""Set chat history."""
    self.chat_store.set_messages(self.chat_store_key, messages)

```
 |  
| --- | --- |  
###  reset [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatSummaryMemoryBuffer.reset "Permanent link")

```
reset() -> None

```

Reset chat history.
Source code in `llama-index-core/llama_index/core/memory/chat_summary_memory_buffer.py`  
| 
```
218
219
220
```
 | 
```
defreset(self) -> None:
"""Reset chat history."""
    self.chat_store.delete_messages(self.chat_store_key)

```
 |  
| --- | --- |  
###  get_token_count [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.ChatSummaryMemoryBuffer.get_token_count "Permanent link")

```
get_token_count() -> 

```

Returns the token count of the memory buffer (excluding the last assistant response).
Source code in `llama-index-core/llama_index/core/memory/chat_summary_memory_buffer.py`  
| 
```
222
223
224
```
 | 
```
defget_token_count(self) -> int:
"""Returns the token count of the memory buffer (excluding the last assistant response)."""
    return self._token_count

```
 |  
| --- | --- |  
##  BaseMemory [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemory "Permanent link")
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
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemory.class_name "Permanent link")

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
###  from_defaults `abstractmethod` `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemory.from_defaults "Permanent link")

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
###  get `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemory.get "Permanent link")

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
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemory.aget "Permanent link")

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
###  get_all `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemory.get_all "Permanent link")

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
###  aget_all [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemory.aget_all "Permanent link")

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
###  put `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemory.put "Permanent link")

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
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemory.aput "Permanent link")

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
###  put_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemory.put_messages "Permanent link")

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
###  aput_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemory.aput_messages "Permanent link")

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
###  set `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemory.set "Permanent link")

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
###  aset [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemory.aset "Permanent link")

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
###  reset `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemory.reset "Permanent link")

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
###  areset [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemory.areset "Permanent link")

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
##  VectorMemory [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.VectorMemory "Permanent link")
Bases: 
Deprecated: Please use `llama_index.core.memory.Memory` instead.
Memory backed by a vector index.
NOTE: This class requires the `delete_nodes` method to be implemented by the vector store underlying the vector index. At time of writing (May 2024), Chroma, Qdrant and SimpleVectorStore all support delete_nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `vector_index`  |  _required_  |  
|  `retriever_kwargs`  |  `Dict[str, Any]`  |  dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs dict(iterable) -> new dictionary initialized as if via: d = {} for k, v in iterable: d[k] = v dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list. For example: dict(one=1, two=2)  |  `<class 'dict'>`  |  
|  `batch_by_user_message`  |  `bool`  |  `True`  |  
|  `cur_batch_textnode`  |   |  The super node for the current active user-message batch.  |  `TextNode(id_='0e701367-0283-433a-8703-a5e70ea3036c', embedding=None, metadata={'sub_dicts': []}, excluded_embed_metadata_keys=['sub_dicts'], excluded_llm_metadata_keys=['sub_dicts'], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='', mimetype='text/plain', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}')`  |  
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
| 
```
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
```
 | 
```
classVectorMemory(BaseMemory):
"""
    Deprecated: Please use `llama_index.core.memory.Memory` instead.

    Memory backed by a vector index.

    NOTE: This class requires the `delete_nodes` method to be implemented
    by the vector store underlying the vector index. At time of writing (May 2024),
    Chroma, Qdrant and SimpleVectorStore all support delete_nodes.
    """

    vector_index: Any
    retriever_kwargs: Dict[str, Any] = Field(default_factory=dict)

    # Whether to combine a user message with all subsequent messages
    # until the next user message into a single message
    # This is on by default, ensuring that we always fetch contiguous blocks of user/response pairs.
    # Turning this off may lead to errors in the function calling API of the LLM.
    # If this is on, then any message that's not a user message will be combined with the last user message
    # in the vector store.
    batch_by_user_message: bool = True

    cur_batch_textnode: TextNode = Field(
        default_factory=_get_starter_node_for_new_batch,
        description="The super node for the current active user-message batch.",
    )

    @field_validator("vector_index")
    @classmethod
    defvalidate_vector_index(cls, value: Any) -> Any:
"""Validate vector index."""
        # NOTE: we can't import VectorStoreIndex directly due to circular imports,
        # which is why the type is Any
        fromllama_index.core.indices.vector_storeimport VectorStoreIndex

        if not isinstance(value, VectorStoreIndex):
            raise ValueError(
                f"Expected 'vector_index' to be an instance of VectorStoreIndex, got {type(value)}"
            )
        return value

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "VectorMemory"

    @classmethod
    deffrom_defaults(
        cls,
        vector_store: Optional[BasePydanticVectorStore] = None,
        embed_model: Optional[EmbedType] = None,
        index_kwargs: Optional[Dict] = None,
        retriever_kwargs: Optional[Dict] = None,
        **kwargs: Any,
    ) -> "VectorMemory":
"""
        Create vector memory.

        Args:
            vector_store (Optional[BasePydanticVectorStore]): vector store (note: delete_nodes must
                be implemented. At time of writing (May 2024), Chroma, Qdrant and
                SimpleVectorStore all support delete_nodes.
            embed_model (Optional[EmbedType]): embedding model
            index_kwargs (Optional[Dict]): kwargs for initializing the index
            retriever_kwargs (Optional[Dict]): kwargs for initializing the retriever

        """
        fromllama_index.core.indices.vector_storeimport VectorStoreIndex

        if kwargs:
            raise ValueError(f"Unexpected kwargs: {kwargs}")

        index_kwargs = index_kwargs or {}
        retriever_kwargs = retriever_kwargs or {}

        if vector_store is None:
            # initialize a blank in-memory vector store
            # NOTE: can't easily do that from `from_vector_store` at the moment.
            index = VectorStoreIndex.from_documents(
                [], embed_model=embed_model, **index_kwargs
            )
        else:
            index = VectorStoreIndex.from_vector_store(
                vector_store, embed_model=embed_model, **index_kwargs
            )
        return cls(vector_index=index, retriever_kwargs=retriever_kwargs)

    defget(
        self, input: Optional[str] = None, initial_token_count: int = 0, **kwargs: Any
    ) -> List[ChatMessage]:
"""Get chat history."""
        if input is None:
            return []

        # retrieve from index
        retriever = self.vector_index.as_retriever(**self.retriever_kwargs)
        nodes = retriever.retrieve(input or "")

        # retrieve underlying messages
        return [
            ChatMessage.model_validate(sub_dict)
            for node in nodes
            for sub_dict in node.metadata["sub_dicts"]
        ]

    defget_all(self) -> List[ChatMessage]:
"""Get all chat history."""
        # TODO: while we could implement get_all, would be hacky through metadata filtering
        # since vector stores don't easily support get()
        raise ValueError(
            "Vector memory does not support get_all method, can only retrieve based on input."
        )

    def_commit_node(self, override_last: bool = False) -> None:
"""Commit new node to vector store."""
        if self.cur_batch_textnode.text == "":
            return

        if override_last:
            # delete the last node
            # This is needed since we're updating the last node in the vector
            # index as its being updated. When a new user-message batch starts
            # we already will have the last user message group committed to the
            # vector store index and so we don't need to override_last (i.e. see
            # logic in self.put().)
            self.vector_index.delete_nodes([self.cur_batch_textnode.id_])

        self.vector_index.insert_nodes([self.cur_batch_textnode])

    defput(self, message: ChatMessage) -> None:
"""Put chat history."""
        if not self.batch_by_user_message or message.role in [
            MessageRole.USER,
            MessageRole.SYSTEM,
        ]:
            # if not batching by user message, commit to vector store immediately after adding
            self.cur_batch_textnode = _get_starter_node_for_new_batch()

        # update current batch textnode
        sub_dict = _stringify_chat_message(message)
        if self.cur_batch_textnode.text == "":
            self.cur_batch_textnode.text += sub_dict["content"] or ""
        else:
            self.cur_batch_textnode.text += " " + (sub_dict["content"] or "")
        self.cur_batch_textnode.metadata["sub_dicts"].append(sub_dict)
        self._commit_node(override_last=True)

    defset(self, messages: List[ChatMessage]) -> None:
"""Set chat history."""
        self.reset()
        for message in messages:
            self.put(message)

    defreset(self) -> None:
"""Reset chat history."""
        self.vector_index.vector_store.clear()

```
 |  
| --- | --- |  
###  validate_vector_index `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.VectorMemory.validate_vector_index "Permanent link")

```
validate_vector_index(value: ) -> 

```

Validate vector index.
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
| 
```
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
```
 | 
```
@field_validator("vector_index")
@classmethod
defvalidate_vector_index(cls, value: Any) -> Any:
"""Validate vector index."""
    # NOTE: we can't import VectorStoreIndex directly due to circular imports,
    # which is why the type is Any
    fromllama_index.core.indices.vector_storeimport VectorStoreIndex

    if not isinstance(value, VectorStoreIndex):
        raise ValueError(
            f"Expected 'vector_index' to be an instance of VectorStoreIndex, got {type(value)}"
        )
    return value

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.VectorMemory.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
| 
```
89
90
91
92
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "VectorMemory"

```
 |  
| --- | --- |  
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.VectorMemory.from_defaults "Permanent link")

```
from_defaults(
    vector_store: Optional[] = None,
    embed_model: Optional[EmbedType] = None,
    index_kwargs: Optional[] = None,
    retriever_kwargs: Optional[] = None,
    **kwargs: 
) -> 

```

Create vector memory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `vector_store`  |  `Optional[BasePydanticVectorStore[](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/#llama_index.core.vector_stores.types.BasePydanticVectorStore "BasePydanticVectorStore \(llama_index.core.vector_stores.types.BasePydanticVectorStore\)")]`  |  vector store (note: delete_nodes must be implemented. At time of writing (May 2024), Chroma, Qdrant and SimpleVectorStore all support delete_nodes.  |  `None`  |  
|  `embed_model`  |  `Optional[EmbedType]`  |  embedding model  |  `None`  |  
|  `index_kwargs`  |  `Optional[Dict]`  |  kwargs for initializing the index  |  `None`  |  
|  `retriever_kwargs`  |  `Optional[Dict]`  |  kwargs for initializing the retriever  |  `None`  |  
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    vector_store: Optional[BasePydanticVectorStore] = None,
    embed_model: Optional[EmbedType] = None,
    index_kwargs: Optional[Dict] = None,
    retriever_kwargs: Optional[Dict] = None,
    **kwargs: Any,
) -> "VectorMemory":
"""
    Create vector memory.

    Args:
        vector_store (Optional[BasePydanticVectorStore]): vector store (note: delete_nodes must
            be implemented. At time of writing (May 2024), Chroma, Qdrant and
            SimpleVectorStore all support delete_nodes.
        embed_model (Optional[EmbedType]): embedding model
        index_kwargs (Optional[Dict]): kwargs for initializing the index
        retriever_kwargs (Optional[Dict]): kwargs for initializing the retriever

    """
    fromllama_index.core.indices.vector_storeimport VectorStoreIndex

    if kwargs:
        raise ValueError(f"Unexpected kwargs: {kwargs}")

    index_kwargs = index_kwargs or {}
    retriever_kwargs = retriever_kwargs or {}

    if vector_store is None:
        # initialize a blank in-memory vector store
        # NOTE: can't easily do that from `from_vector_store` at the moment.
        index = VectorStoreIndex.from_documents(
            [], embed_model=embed_model, **index_kwargs
        )
    else:
        index = VectorStoreIndex.from_vector_store(
            vector_store, embed_model=embed_model, **index_kwargs
        )
    return cls(vector_index=index, retriever_kwargs=retriever_kwargs)

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.VectorMemory.get "Permanent link")

```
get(
    input: Optional[] = None,
    initial_token_count:  = 0,
    **kwargs: 
) -> []

```

Get chat history.
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
| 
```
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
```
 | 
```
defget(
    self, input: Optional[str] = None, initial_token_count: int = 0, **kwargs: Any
) -> List[ChatMessage]:
"""Get chat history."""
    if input is None:
        return []

    # retrieve from index
    retriever = self.vector_index.as_retriever(**self.retriever_kwargs)
    nodes = retriever.retrieve(input or "")

    # retrieve underlying messages
    return [
        ChatMessage.model_validate(sub_dict)
        for node in nodes
        for sub_dict in node.metadata["sub_dicts"]
    ]

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.VectorMemory.get_all "Permanent link")

```
get_all() -> []

```

Get all chat history.
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
| 
```
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
defget_all(self) -> List[ChatMessage]:
"""Get all chat history."""
    # TODO: while we could implement get_all, would be hacky through metadata filtering
    # since vector stores don't easily support get()
    raise ValueError(
        "Vector memory does not support get_all method, can only retrieve based on input."
    )

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.VectorMemory.put "Permanent link")

```
put(message: ) -> None

```

Put chat history.
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
| 
```
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
```
 | 
```
defput(self, message: ChatMessage) -> None:
"""Put chat history."""
    if not self.batch_by_user_message or message.role in [
        MessageRole.USER,
        MessageRole.SYSTEM,
    ]:
        # if not batching by user message, commit to vector store immediately after adding
        self.cur_batch_textnode = _get_starter_node_for_new_batch()

    # update current batch textnode
    sub_dict = _stringify_chat_message(message)
    if self.cur_batch_textnode.text == "":
        self.cur_batch_textnode.text += sub_dict["content"] or ""
    else:
        self.cur_batch_textnode.text += " " + (sub_dict["content"] or "")
    self.cur_batch_textnode.metadata["sub_dicts"].append(sub_dict)
    self._commit_node(override_last=True)

```
 |  
| --- | --- |  
###  set [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.VectorMemory.set "Permanent link")

```
set(messages: []) -> None

```

Set chat history.
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
| 
```
195
196
197
198
199
```
 | 
```
defset(self, messages: List[ChatMessage]) -> None:
"""Set chat history."""
    self.reset()
    for message in messages:
        self.put(message)

```
 |  
| --- | --- |  
###  reset [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.VectorMemory.reset "Permanent link")

```
reset() -> None

```

Reset chat history.
Source code in `llama-index-core/llama_index/core/memory/vector_memory.py`  
| 
```
201
202
203
```
 | 
```
defreset(self) -> None:
"""Reset chat history."""
    self.vector_index.vector_store.clear()

```
 |  
| --- | --- |  
##  SimpleComposableMemory [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.SimpleComposableMemory "Permanent link")
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
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.SimpleComposableMemory.class_name "Permanent link")

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
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.SimpleComposableMemory.from_defaults "Permanent link")

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
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.SimpleComposableMemory.get "Permanent link")

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
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.SimpleComposableMemory.get_all "Permanent link")

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
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.SimpleComposableMemory.put "Permanent link")

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
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.SimpleComposableMemory.aput "Permanent link")

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
###  set [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.SimpleComposableMemory.set "Permanent link")

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
###  reset [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.SimpleComposableMemory.reset "Permanent link")

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
##  Memory [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.Memory "Permanent link")
Bases: 
A memory module that waterfalls into memory blocks.
Works by orchestrating around - a FIFO queue of messages - a list of memory blocks - various parameters (pressure size, token limit, etc.)
When the FIFO queue reaches the token limit, the oldest messages within the pressure size are ejected from the FIFO queue. The messages are then processed by each memory block.
When pulling messages from this memory, the memory blocks are processed in order, and the messages are injected into the system message or the latest user message.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `token_limit`  |  The overall token limit of the memory.  |  `30000`  |  
|  `token_flush_size`  |  The token size to use for flushing the FIFO queue.  |  `3000`  |  
|  `chat_history_token_ratio`  |  `float`  |  Minimum percentage ratio of total token limit reserved for chat history.  |  `0.7`  |  
|  `memory_blocks`  |  `List[BaseMemoryBlock[](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemoryBlock "BaseMemoryBlock \(llama_index.core.memory.memory.BaseMemoryBlock\)")]`  |  The list of memory blocks to use.  |  `<dynamic>`  |  
|  `memory_blocks_template`  |   |  The template to use for formatting the memory blocks.  |  `RichPromptTemplate(metadata={}, template_vars=['memory_blocks'], kwargs={}, output_parser=None, template_var_mappings=None, function_mappings=None, template_str='\n<memory>\n{% for (block_name, block_content) in memory_blocks %}\n<{{ block_name }}>\n  {% for block in block_content %}\n    {% if block.block_type == "text" %}\n{{ block.text }}\n    {% elif block.block_type == "image" %}\n      {% if block.url %}\n        {{ (block.url | string) | image }}\n      {% elif block.path %}\n        {{ (block.path | string) | image }}\n      {% endif %}\n    {% elif block.block_type == "audio" %}\n      {% if block.url %}\n        {{ (block.url | string) | audio }}\n      {% elif block.path %}\n        {{ (block.path | string) | audio }}\n      {% endif %}\n    {% endif %}\n  {% endfor %}\n</{{ block_name }}>\n{% endfor %}\n</memory>\n')`  |  
|  `insert_method`  |  `InsertMethod`  |  Whether to inject memory blocks into a system message or into the latest user message.  |  `<InsertMethod.SYSTEM: 'system'>`  |  
|  `image_token_size_estimate`  |  The token size estimate for images.  |  `256`  |  
|  `audio_token_size_estimate`  |  The token size estimate for audio.  |  `256`  |  
|  `video_token_size_estimate`  |  The token size estimate for video.  |  `256`  |  
|  `tokenizer_fn`  |  `Callable[list, List]`  |  The tokenizer function to use for token counting.  |  `<dynamic>`  |  
|  `sql_store`  |   |  The chat store to use for storing messages.  |  `SQLAlchemyChatStore(table_name='llama_index_memory', async_database_uri='sqlite+aiosqlite:///:memory:', db_schema=None)`  |  
|  `session_id`  |  The key to use for storing messages in the chat store.  |  `'db7fdd9d-6339-43ed-a276-7ab27e4eb293'`  |  
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
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
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
```
 | 
```
classMemory(BaseMemory):
"""
    A memory module that waterfalls into memory blocks.

    Works by orchestrating around
    - a FIFO queue of messages
    - a list of memory blocks
    - various parameters (pressure size, token limit, etc.)

    When the FIFO queue reaches the token limit, the oldest messages within the pressure size are ejected from the FIFO queue.
    The messages are then processed by each memory block.

    When pulling messages from this memory, the memory blocks are processed in order, and the messages are injected into the system message or the latest user message.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    token_limit: int = Field(
        default=DEFAULT_TOKEN_LIMIT,
        description="The overall token limit of the memory.",
    )
    token_flush_size: int = Field(
        default=DEFAULT_FLUSH_SIZE,
        description="The token size to use for flushing the FIFO queue.",
    )
    chat_history_token_ratio: float = Field(
        default=0.7,
        description="Minimum percentage ratio of total token limit reserved for chat history.",
    )
    memory_blocks: List[BaseMemoryBlock] = Field(
        default_factory=list,
        description="The list of memory blocks to use.",
    )
    memory_blocks_template: RichPromptTemplate = Field(
        default=DEFAULT_MEMORY_BLOCKS_TEMPLATE,
        description="The template to use for formatting the memory blocks.",
    )
    insert_method: InsertMethod = Field(
        default=InsertMethod.SYSTEM,
        description="Whether to inject memory blocks into a system message or into the latest user message.",
    )
    image_token_size_estimate: int = Field(
        default=256,
        description="The token size estimate for images.",
    )
    audio_token_size_estimate: int = Field(
        default=256,
        description="The token size estimate for audio.",
    )
    video_token_size_estimate: int = Field(
        default=256,
        description="The token size estimate for video.",
    )
    tokenizer_fn: Callable[[str], List] = Field(
        default_factory=get_tokenizer,
        exclude=True,
        description="The tokenizer function to use for token counting.",
    )
    sql_store: SQLAlchemyChatStore = Field(
        default_factory=get_default_chat_store,
        exclude=True,
        description="The chat store to use for storing messages.",
    )
    session_id: str = Field(
        default_factory=generate_chat_store_key,
        description="The key to use for storing messages in the chat store.",
    )

    @classmethod
    defclass_name(cls) -> str:
        return "Memory"

    @model_validator(mode="before")
    @classmethod
    defvalidate_memory(cls, values: dict) -> dict:
        # Validate token limit
        token_limit = values.get("token_limit", -1)
        if token_limit  1:
            raise ValueError("Token limit must be set and greater than 0.")

        tokenizer_fn = values.get("tokenizer_fn")
        if tokenizer_fn is None:
            values["tokenizer_fn"] = get_tokenizer()

        if values.get("token_flush_size", -1)  1:
            values["token_flush_size"] = int(token_limit * 0.1)
        elif values.get("token_flush_size", -1)  token_limit:
            values["token_flush_size"] = int(token_limit * 0.1)

        # validate all blocks have unique names
        block_names = [block.name for block in values.get("memory_blocks", [])]
        if len(block_names) != len(set(block_names)):
            raise ValueError("All memory blocks must have unique names.")

        return values

    @classmethod
    deffrom_defaults(  # type: ignore[override]
        cls,
        session_id: Optional[str] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        token_limit: int = DEFAULT_TOKEN_LIMIT,
        memory_blocks: Optional[List[BaseMemoryBlock[Any]]] = None,
        tokenizer_fn: Optional[Callable[[str], List]] = None,
        chat_history_token_ratio: float = 0.7,
        token_flush_size: int = DEFAULT_FLUSH_SIZE,
        memory_blocks_template: RichPromptTemplate = DEFAULT_MEMORY_BLOCKS_TEMPLATE,
        insert_method: InsertMethod = InsertMethod.SYSTEM,
        image_token_size_estimate: int = 256,
        audio_token_size_estimate: int = 256,
        video_token_size_estimate: int = 256,
        # SQLAlchemyChatStore parameters
        table_name: str = "llama_index_memory",
        async_database_uri: Optional[str] = None,
        async_engine: Optional[AsyncEngine] = None,
        db_schema: Optional[str] = None,
    ) -> "Memory":
"""Initialize Memory."""
        session_id = session_id or generate_chat_store_key()

        # If not using the SQLAlchemyChatStore, provide an error
        sql_store = SQLAlchemyChatStore(
            table_name=table_name,
            async_database_uri=async_database_uri,
            async_engine=async_engine,
            db_schema=db_schema,
        )

        if chat_history is not None:
            asyncio_run(sql_store.set_messages(session_id, chat_history))

        if token_flush_size  token_limit:
            token_flush_size = int(token_limit * 0.7)

        return cls(
            token_limit=token_limit,
            tokenizer_fn=tokenizer_fn or get_tokenizer(),
            sql_store=sql_store,
            session_id=session_id,
            memory_blocks=memory_blocks or [],
            chat_history_token_ratio=chat_history_token_ratio,
            token_flush_size=token_flush_size,
            memory_blocks_template=memory_blocks_template,
            insert_method=insert_method,
            image_token_size_estimate=image_token_size_estimate,
            audio_token_size_estimate=audio_token_size_estimate,
            video_token_size_estimate=video_token_size_estimate,
        )

    def_estimate_token_count(
        self,
        message_or_blocks: Union[
            str, ChatMessage, List[ChatMessage], List[ContentBlock]
        ],
    ) -> int:
"""Estimate token count for a message."""
        token_count = 0

        # Normalize the input to a list of ContentBlocks
        if isinstance(message_or_blocks, ChatMessage):
            blocks: List[
                Union[
                    TextBlock,
                    ImageBlock,
                    VideoBlock,
                    AudioBlock,
                    DocumentBlock,
                    CitableBlock,
                    CitationBlock,
                    ThinkingBlock,
                ]
            ] = []

            for block in message_or_blocks.blocks:
                if not isinstance(block, (CachePoint, ToolCallBlock)):
                    blocks.append(block)

            # Estimate the token count for the additional kwargs
            if message_or_blocks.additional_kwargs:
                token_count += len(
                    self.tokenizer_fn(str(message_or_blocks.additional_kwargs))
                )
        elif isinstance(message_or_blocks, List):
            # Type narrow the list
            messages: List[ChatMessage] = []

            if all(isinstance(item, ChatMessage) for item in message_or_blocks):
                messages = cast(List[ChatMessage], message_or_blocks)

                blocks = []
                for msg in messages:
                    for block in msg.blocks:
                        if not isinstance(block, (CachePoint, ToolCallBlock)):
                            blocks.append(block)

                # Estimate the token count for the additional kwargs
                token_count += sum(
                    len(self.tokenizer_fn(str(msg.additional_kwargs)))
                    for msg in messages
                    if msg.additional_kwargs
                )
            elif all(
                isinstance(
                    item,
                    (
                        TextBlock,
                        ImageBlock,
                        AudioBlock,
                        VideoBlock,
                        DocumentBlock,
                        CachePoint,
                    ),
                )
                for item in message_or_blocks
            ):
                blocks = []
                for item in message_or_blocks:
                    if not isinstance(item, CachePoint):
                        blocks.append(
                            cast(
                                Union[
                                    TextBlock,
                                    ImageBlock,
                                    AudioBlock,
                                    VideoBlock,
                                    DocumentBlock,
                                ],
                                item,
                            )
                        )
            else:
                raise ValueError(f"Invalid message type: {type(message_or_blocks)}")
        elif isinstance(message_or_blocks, str):
            blocks = [TextBlock(text=message_or_blocks)]
        else:
            raise ValueError(f"Invalid message type: {type(message_or_blocks)}")

        # Estimate the token count for each block
        for block in blocks:
            if isinstance(block, TextBlock):
                token_count += len(self.tokenizer_fn(block.text))
            elif isinstance(block, ImageBlock):
                token_count += self.image_token_size_estimate
            elif isinstance(block, VideoBlock):
                token_count += self.video_token_size_estimate
            elif isinstance(block, AudioBlock):
                token_count += self.audio_token_size_estimate

        return token_count

    async def_get_memory_blocks_content(
        self,
        chat_history: List[ChatMessage],
        input: Optional[Union[str, ChatMessage]] = None,
        **block_kwargs: Any,
    ) -> Dict[str, Any]:
"""Get content from memory blocks in priority order."""
        content_per_memory_block: Dict[str, Any] = {}

        block_input = chat_history
        if isinstance(input, str):
            block_input = [*chat_history, ChatMessage(role="user", content=input)]

        # Process memory blocks in priority order
        for memory_block in sorted(self.memory_blocks, key=lambda x: -x.priority):
            content = await memory_block.aget(
                block_input, session_id=self.session_id, **block_kwargs
            )

            # Handle different return types from memory blocks
            if content and isinstance(content, list):
                # Memory block returned content blocks
                content_per_memory_block[memory_block.name] = content
            elif content and isinstance(content, str):
                # Memory block returned a string
                content_per_memory_block[memory_block.name] = content
            elif not content:
                continue
            else:
                raise ValueError(
                    f"Invalid content type received from memory block {memory_block.name}: {type(content)}"
                )

        return content_per_memory_block

    async def_truncate_memory_blocks(
        self,
        content_per_memory_block: Dict[str, Any],
        memory_blocks_tokens: int,
        chat_history_tokens: int,
    ) -> Dict[str, Any]:
"""Truncate memory blocks if total token count exceeds limit."""
        if memory_blocks_tokens + chat_history_tokens <= self.token_limit:
            return content_per_memory_block

        tokens_to_truncate = (
            memory_blocks_tokens + chat_history_tokens - self.token_limit
        )
        truncated_content = content_per_memory_block.copy()

        # Truncate memory blocks based on priority
        for memory_block in sorted(
            self.memory_blocks, key=lambda x: x.priority
        ):  # Lower priority first
            # Skip memory blocks with priority 0, they should never be truncated
            if memory_block.priority == 0:
                continue

            if tokens_to_truncate <= 0:
                break

            # Truncate content and measure tokens saved
            content = truncated_content.get(memory_block.name, [])

            truncated_block_content = await memory_block.atruncate(
                content, tokens_to_truncate
            )

            # Calculate tokens saved
            original_tokens = self._estimate_token_count(content)

            if truncated_block_content is None:
                new_tokens = 0
            else:
                new_tokens = self._estimate_token_count(truncated_block_content)

            tokens_saved = original_tokens - new_tokens
            tokens_to_truncate -= tokens_saved

            # Update the content blocks
            if truncated_block_content is None:
                truncated_content[memory_block.name] = []
            else:
                truncated_content[memory_block.name] = truncated_block_content

        # handle case where we still have tokens to truncate
        # just remove the blocks starting from the least priority
        for memory_block in sorted(self.memory_blocks, key=lambda x: x.priority):
            if memory_block.priority == 0:
                continue

            if tokens_to_truncate <= 0:
                break

            # Truncate content and measure tokens saved
            content = truncated_content.pop(memory_block.name)
            tokens_to_truncate -= self._estimate_token_count(content)

        return truncated_content

    async def_format_memory_blocks(
        self, content_per_memory_block: Dict[str, Any]
    ) -> Tuple[List[Tuple[str, List[ContentBlock]]], List[ChatMessage]]:
"""Format memory blocks content into template data and chat messages."""
        memory_blocks_data: List[Tuple[str, List[ContentBlock]]] = []
        chat_message_data: List[ChatMessage] = []

        for block in self.memory_blocks:
            if block.name in content_per_memory_block:
                content = content_per_memory_block[block.name]

                # Skip empty memory blocks
                if not content:
                    continue

                if (
                    isinstance(content, list)
                    and content
                    and isinstance(content[0], ChatMessage)
                ):
                    chat_message_data.extend(content)
                elif isinstance(content, str):
                    memory_blocks_data.append((block.name, [TextBlock(text=content)]))
                else:
                    memory_blocks_data.append((block.name, content))

        return memory_blocks_data, chat_message_data

    def_insert_memory_content(
        self,
        chat_history: List[ChatMessage],
        memory_content: List[ContentBlock],
        chat_message_data: List[ChatMessage],
    ) -> List[ChatMessage]:
"""Insert memory content into chat history based on insert method."""
        result = chat_history.copy()

        # Process chat messages
        if chat_message_data:
            result = [*chat_message_data, *result]

        # Process template-based memory blocks
        if memory_content:
            if self.insert_method == InsertMethod.SYSTEM:
                # Find system message or create a new one
                system_idx = next(
                    (i for i, msg in enumerate(result) if msg.role == "system"), None
                )

                if system_idx is not None:
                    # Update existing system message
                    result[system_idx].blocks = [
                        *memory_content,
                        *result[system_idx].blocks,
                    ]
                else:
                    # Create new system message at the beginning
                    result.insert(0, ChatMessage(role="system", blocks=memory_content))
            elif self.insert_method == InsertMethod.USER:
                # Find the latest user message
                session_idx = next(
                    (i for i, msg in enumerate(reversed(result)) if msg.role == "user"),
                    None,
                )

                if session_idx is not None:
                    # Get actual index (since we enumerated in reverse)
                    actual_idx = len(result) - 1 - session_idx
                    # Update existing user message
                    result[actual_idx].blocks = [
                        *memory_content,
                        *result[actual_idx].blocks,
                    ]
                else:
                    result.append(ChatMessage(role="user", blocks=memory_content))

        return result

    async defaget(
        self, input: Optional[Union[str, ChatMessage]] = None, **block_kwargs: Any
    ) -> List[ChatMessage]:  # type: ignore[override]
"""Get messages with memory blocks included (async)."""
        # Get chat history efficiently
        chat_history = await self.sql_store.get_messages(
            self.session_id, status=MessageStatus.ACTIVE
        )
        chat_history_tokens = sum(
            self._estimate_token_count(message) for message in chat_history
        )

        # Get memory blocks content
        content_per_memory_block = await self._get_memory_blocks_content(
            chat_history, input=input, **block_kwargs
        )

        # Calculate memory blocks tokens
        memory_blocks_tokens = sum(
            self._estimate_token_count(content)
            for content in content_per_memory_block.values()
        )

        # Handle truncation if needed
        truncated_content = await self._truncate_memory_blocks(
            content_per_memory_block, memory_blocks_tokens, chat_history_tokens
        )

        # Format template-based memory blocks
        memory_blocks_data, chat_message_data = await self._format_memory_blocks(
            truncated_content
        )

        # Create messages from template content
        memory_content = []
        if memory_blocks_data:
            memory_block_messages = self.memory_blocks_template.format_messages(
                memory_blocks=memory_blocks_data
            )
            memory_content = (
                memory_block_messages[0].blocks if memory_block_messages else []
            )

        # Insert memory content into chat history
        return self._insert_memory_content(
            chat_history, memory_content, chat_message_data
        )

    async def_manage_queue(self) -> None:
"""
        Manage the FIFO queue.

        This function manages the memory queue using a waterfall approach:
        1. If the queue exceeds the token limit, it removes oldest messages first
        2. Removed messages are archived and passed to memory blocks
        3. It ensures conversation integrity by keeping related messages together
        4. It maintains at least one complete conversation turn
        """
        # Calculate if we need to waterfall
        current_queue = await self.sql_store.get_messages(
            self.session_id, status=MessageStatus.ACTIVE
        )

        # If current queue is empty, return
        if not current_queue:
            return

        tokens_in_current_queue = sum(
            self._estimate_token_count(message) for message in current_queue
        )

        # If we're over the token limit, initiate waterfall
        token_limit = self.token_limit * self.chat_history_token_ratio
        if tokens_in_current_queue  token_limit:
            # Process from oldest to newest, but efficiently with pop() operations
            reversed_queue = current_queue[::-1]  # newest first, oldest last

            # Calculate approximate number of messages to remove
            tokens_to_remove = tokens_in_current_queue - token_limit

            while tokens_to_remove  0:
                # If only one message left, keep it regardless of token count
                if len(reversed_queue) <= 1:
                    break

                # Collect messages to flush (up to flush size)
                messages_to_flush = []
                flushed_tokens = 0

                # Remove oldest messages (from end of reversed list) until reaching flush size
                while (
                    flushed_tokens  self.token_flush_size
                    and reversed_queue
                    and len(reversed_queue)  1
                ):
                    message = reversed_queue.pop()
                    messages_to_flush.append(message)
                    flushed_tokens += self._estimate_token_count(message)

                # Ensure we keep at least one message
                if not reversed_queue and messages_to_flush:
                    reversed_queue.append(messages_to_flush.pop())

                # We need to maintain conversation integrity
                # Messages should be removed in complete conversation turns
                chronological_view = reversed_queue[::-1]  # View in chronological order

                # Find the correct conversation boundary
                # We want the first message in our remaining queue to be a user message
                # and the last message to be from assistant or tool
                if chronological_view:
                    # Keep removing messages until first remaining message is from user
                    # This ensures we start with a user message
                    while (
                        chronological_view
                        and chronological_view[0].role != "user"
                        and len(reversed_queue)  1
                    ):
                        if reversed_queue:
                            messages_to_flush.append(reversed_queue.pop())
                            chronological_view = reversed_queue[::-1]
                        else:
                            break

                    # If we end up with an empty queue or only a non-user message,
                    # keep at least one full conversation turn
                    if (
                        not reversed_queue
                        or (
                            len(reversed_queue) == 1
                            and reversed_queue[0].role != "user"
                        )
                    ) and messages_to_flush:
                        # If reversed_queue has a non-user message, move it to messages_to_flush
                        if reversed_queue and reversed_queue[0].role != "user":
                            messages_to_flush.append(reversed_queue.pop(0))

                        # Find the most recent complete conversation turn in messages_to_flush
                        # A complete turn is: user message + all subsequent assistant/tool responses
                        # This correctly handles tool calling: user → assistant → tool → assistant
                        # Search from end to find the last user message
                        turn_start_idx = -1

                        for i in range(len(messages_to_flush) - 1, -1, -1):
                            if messages_to_flush[i].role == "user":
                                turn_start_idx = i
                                break

                        # If we found a user message, keep everything from that user to the end
                        if turn_start_idx >= 0:
                            turn_messages = messages_to_flush[turn_start_idx:]
                            # Keep only messages before the turn for flushing
                            messages_to_flush = messages_to_flush[:turn_start_idx]
                            # Add the complete turn back to the queue
                            reversed_queue = turn_messages[::-1] + reversed_queue
                        # else: No user message found - queue may remain empty (defensive)

                # Archive the flushed messages
                if messages_to_flush:
                    await self.sql_store.archive_oldest_messages(
                        self.session_id, n=len(messages_to_flush)
                    )

                    # Waterfall the flushed messages to memory blocks
                    await asyncio.gather(
                        *[
                            block.aput(
                                messages_to_flush,
                                from_short_term_memory=True,
                                session_id=self.session_id,
                            )
                            for block in self.memory_blocks
                        ]
                    )

                # Recalculate remaining tokens
                chronological_view = reversed_queue[::-1]
                tokens_in_current_queue = sum(
                    self._estimate_token_count(message)
                    for message in chronological_view
                )
                tokens_to_remove = tokens_in_current_queue - token_limit

                # Exit if we've flushed everything possible but still over limit
                if not messages_to_flush:
                    break

    async defaput(self, message: ChatMessage) -> None:
"""Add a message to the chat store and process waterfall logic if needed."""
        # Add the message to the chat store
        await self.sql_store.add_message(
            self.session_id, message, status=MessageStatus.ACTIVE
        )

        # Ensure the active queue is managed
        await self._manage_queue()

    async defaput_messages(self, messages: List[ChatMessage]) -> None:
"""Add a list of messages to the chat store and process waterfall logic if needed."""
        # Add the messages to the chat store
        await self.sql_store.add_messages(
            self.session_id, messages, status=MessageStatus.ACTIVE
        )

        # Ensure the active queue is managed
        await self._manage_queue()

    async defaset(self, messages: List[ChatMessage]) -> None:
"""Set the chat history."""
        await self.sql_store.set_messages(
            self.session_id, messages, status=MessageStatus.ACTIVE
        )

    async defaget_all(
        self, status: Optional[MessageStatus] = None
    ) -> List[ChatMessage]:
"""Get all messages."""
        return await self.sql_store.get_messages(self.session_id, status=status)

    async defareset(self, status: Optional[MessageStatus] = None) -> None:
"""Reset the memory."""
        await self.sql_store.delete_messages(self.session_id, status=status)

    # ---- Sync method wrappers ----

    defget(
        self, input: Optional[Union[str, ChatMessage]] = None, **block_kwargs: Any
    ) -> List[ChatMessage]:  # type: ignore[override]
"""Get messages with memory blocks included."""
        return asyncio_run(self.aget(input=input, **block_kwargs))

    defget_all(self, status: Optional[MessageStatus] = None) -> List[ChatMessage]:
"""Get all messages."""
        return asyncio_run(self.aget_all(status=status))

    defput(self, message: ChatMessage) -> None:
"""Add a message to the chat store and process waterfall logic if needed."""
        return asyncio_run(self.aput(message))

    defput_messages(self, messages: List[ChatMessage]) -> None:
"""Add a list of messages to the chat store and process waterfall logic if needed."""
        return asyncio_run(self.aput_messages(messages))

    defset(self, messages: List[ChatMessage]) -> None:
"""Set the chat history."""
        return asyncio_run(self.aset(messages))

    defreset(self) -> None:
"""Reset the memory."""
        return asyncio_run(self.areset())

```
 |  
| --- | --- |  
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.Memory.from_defaults "Permanent link")

```
from_defaults(
    session_id: Optional[] = None,
    chat_history: Optional[[]] = None,
    token_limit:  = DEFAULT_TOKEN_LIMIT,
    memory_blocks: Optional[
        [[]]
    ] = None,
    tokenizer_fn: Optional[Callable[[], ]] = None,
    chat_history_token_ratio: float = 0.7,
    token_flush_size:  = DEFAULT_FLUSH_SIZE,
    memory_blocks_template:  = DEFAULT_MEMORY_BLOCKS_TEMPLATE,
    insert_method: InsertMethod = SYSTEM,
    image_token_size_estimate:  = 256,
    audio_token_size_estimate:  = 256,
    video_token_size_estimate:  = 256,
    table_name:  = "llama_index_memory",
    async_database_uri: Optional[] = None,
    async_engine: Optional[AsyncEngine] = None,
    db_schema: Optional[] = None,
) -> 

```

Initialize Memory.
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
```
 | 
```
@classmethod
deffrom_defaults(  # type: ignore[override]
    cls,
    session_id: Optional[str] = None,
    chat_history: Optional[List[ChatMessage]] = None,
    token_limit: int = DEFAULT_TOKEN_LIMIT,
    memory_blocks: Optional[List[BaseMemoryBlock[Any]]] = None,
    tokenizer_fn: Optional[Callable[[str], List]] = None,
    chat_history_token_ratio: float = 0.7,
    token_flush_size: int = DEFAULT_FLUSH_SIZE,
    memory_blocks_template: RichPromptTemplate = DEFAULT_MEMORY_BLOCKS_TEMPLATE,
    insert_method: InsertMethod = InsertMethod.SYSTEM,
    image_token_size_estimate: int = 256,
    audio_token_size_estimate: int = 256,
    video_token_size_estimate: int = 256,
    # SQLAlchemyChatStore parameters
    table_name: str = "llama_index_memory",
    async_database_uri: Optional[str] = None,
    async_engine: Optional[AsyncEngine] = None,
    db_schema: Optional[str] = None,
) -> "Memory":
"""Initialize Memory."""
    session_id = session_id or generate_chat_store_key()

    # If not using the SQLAlchemyChatStore, provide an error
    sql_store = SQLAlchemyChatStore(
        table_name=table_name,
        async_database_uri=async_database_uri,
        async_engine=async_engine,
        db_schema=db_schema,
    )

    if chat_history is not None:
        asyncio_run(sql_store.set_messages(session_id, chat_history))

    if token_flush_size  token_limit:
        token_flush_size = int(token_limit * 0.7)

    return cls(
        token_limit=token_limit,
        tokenizer_fn=tokenizer_fn or get_tokenizer(),
        sql_store=sql_store,
        session_id=session_id,
        memory_blocks=memory_blocks or [],
        chat_history_token_ratio=chat_history_token_ratio,
        token_flush_size=token_flush_size,
        memory_blocks_template=memory_blocks_template,
        insert_method=insert_method,
        image_token_size_estimate=image_token_size_estimate,
        audio_token_size_estimate=audio_token_size_estimate,
        video_token_size_estimate=video_token_size_estimate,
    )

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.Memory.aget "Permanent link")

```
aget(
    input: Optional[Union[, ]] = None,
    **block_kwargs: 
) -> []

```

Get messages with memory blocks included (async).
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
```
 | 
```
async defaget(
    self, input: Optional[Union[str, ChatMessage]] = None, **block_kwargs: Any
) -> List[ChatMessage]:  # type: ignore[override]
"""Get messages with memory blocks included (async)."""
    # Get chat history efficiently
    chat_history = await self.sql_store.get_messages(
        self.session_id, status=MessageStatus.ACTIVE
    )
    chat_history_tokens = sum(
        self._estimate_token_count(message) for message in chat_history
    )

    # Get memory blocks content
    content_per_memory_block = await self._get_memory_blocks_content(
        chat_history, input=input, **block_kwargs
    )

    # Calculate memory blocks tokens
    memory_blocks_tokens = sum(
        self._estimate_token_count(content)
        for content in content_per_memory_block.values()
    )

    # Handle truncation if needed
    truncated_content = await self._truncate_memory_blocks(
        content_per_memory_block, memory_blocks_tokens, chat_history_tokens
    )

    # Format template-based memory blocks
    memory_blocks_data, chat_message_data = await self._format_memory_blocks(
        truncated_content
    )

    # Create messages from template content
    memory_content = []
    if memory_blocks_data:
        memory_block_messages = self.memory_blocks_template.format_messages(
            memory_blocks=memory_blocks_data
        )
        memory_content = (
            memory_block_messages[0].blocks if memory_block_messages else []
        )

    # Insert memory content into chat history
    return self._insert_memory_content(
        chat_history, memory_content, chat_message_data
    )

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.Memory.aput "Permanent link")

```
aput(message: ) -> None

```

Add a message to the chat store and process waterfall logic if needed.
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
794
795
796
797
798
799
800
801
802
```
 | 
```
async defaput(self, message: ChatMessage) -> None:
"""Add a message to the chat store and process waterfall logic if needed."""
    # Add the message to the chat store
    await self.sql_store.add_message(
        self.session_id, message, status=MessageStatus.ACTIVE
    )

    # Ensure the active queue is managed
    await self._manage_queue()

```
 |  
| --- | --- |  
###  aput_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.Memory.aput_messages "Permanent link")

```
aput_messages(messages: []) -> None

```

Add a list of messages to the chat store and process waterfall logic if needed.
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
804
805
806
807
808
809
810
811
812
```
 | 
```
async defaput_messages(self, messages: List[ChatMessage]) -> None:
"""Add a list of messages to the chat store and process waterfall logic if needed."""
    # Add the messages to the chat store
    await self.sql_store.add_messages(
        self.session_id, messages, status=MessageStatus.ACTIVE
    )

    # Ensure the active queue is managed
    await self._manage_queue()

```
 |  
| --- | --- |  
###  aset [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.Memory.aset "Permanent link")

```
aset(messages: []) -> None

```

Set the chat history.
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
814
815
816
817
818
```
 | 
```
async defaset(self, messages: List[ChatMessage]) -> None:
"""Set the chat history."""
    await self.sql_store.set_messages(
        self.session_id, messages, status=MessageStatus.ACTIVE
    )

```
 |  
| --- | --- |  
###  aget_all [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.Memory.aget_all "Permanent link")

```
aget_all(
    status: Optional[MessageStatus] = None,
) -> []

```

Get all messages.
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
820
821
822
823
824
```
 | 
```
async defaget_all(
    self, status: Optional[MessageStatus] = None
) -> List[ChatMessage]:
"""Get all messages."""
    return await self.sql_store.get_messages(self.session_id, status=status)

```
 |  
| --- | --- |  
###  areset [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.Memory.areset "Permanent link")

```
areset(status: Optional[MessageStatus] = None) -> None

```

Reset the memory.
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
826
827
828
```
 | 
```
async defareset(self, status: Optional[MessageStatus] = None) -> None:
"""Reset the memory."""
    await self.sql_store.delete_messages(self.session_id, status=status)

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.Memory.get "Permanent link")

```
get(
    input: Optional[Union[, ]] = None,
    **block_kwargs: 
) -> []

```

Get messages with memory blocks included.
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
832
833
834
835
836
```
 | 
```
defget(
    self, input: Optional[Union[str, ChatMessage]] = None, **block_kwargs: Any
) -> List[ChatMessage]:  # type: ignore[override]
"""Get messages with memory blocks included."""
    return asyncio_run(self.aget(input=input, **block_kwargs))

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.Memory.get_all "Permanent link")

```
get_all(
    status: Optional[MessageStatus] = None,
) -> []

```

Get all messages.
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
838
839
840
```
 | 
```
defget_all(self, status: Optional[MessageStatus] = None) -> List[ChatMessage]:
"""Get all messages."""
    return asyncio_run(self.aget_all(status=status))

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.Memory.put "Permanent link")

```
put(message: ) -> None

```

Add a message to the chat store and process waterfall logic if needed.
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
842
843
844
```
 | 
```
defput(self, message: ChatMessage) -> None:
"""Add a message to the chat store and process waterfall logic if needed."""
    return asyncio_run(self.aput(message))

```
 |  
| --- | --- |  
###  put_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.Memory.put_messages "Permanent link")

```
put_messages(messages: []) -> None

```

Add a list of messages to the chat store and process waterfall logic if needed.
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
846
847
848
```
 | 
```
defput_messages(self, messages: List[ChatMessage]) -> None:
"""Add a list of messages to the chat store and process waterfall logic if needed."""
    return asyncio_run(self.aput_messages(messages))

```
 |  
| --- | --- |  
###  set [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.Memory.set "Permanent link")

```
set(messages: []) -> None

```

Set the chat history.
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
850
851
852
```
 | 
```
defset(self, messages: List[ChatMessage]) -> None:
"""Set the chat history."""
    return asyncio_run(self.aset(messages))

```
 |  
| --- | --- |  
###  reset [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.Memory.reset "Permanent link")

```
reset() -> None

```

Reset the memory.
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
854
855
856
```
 | 
```
defreset(self) -> None:
"""Reset the memory."""
    return asyncio_run(self.areset())

```
 |  
| --- | --- |  
##  BaseMemoryBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemoryBlock "Permanent link")
Bases: `BaseModel`, `Generic[T]`
A base class for memory blocks.
Subclasses must implement the `aget` and `aput` methods. Optionally, subclasses can implement the `atruncate` method, which is used to reduce the size of the memory block.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `name`  |  The name/identifier of the memory block.  |  _required_  |  
|  `description`  |  `str | None`  |  A description of the memory block.  |  `None`  |  
|  `priority`  |  Priority of this memory block (0 = never truncate, 1 = highest priority, etc.).  |  
|  `accept_short_term_memory`  |  `bool`  |  Whether to accept puts from messages ejected from the short-term memory.  |  `True`  |  
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
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
```
 | 
```
classBaseMemoryBlock(BaseModel, Generic[T]):
"""
    A base class for memory blocks.

    Subclasses must implement the `aget` and `aput` methods.
    Optionally, subclasses can implement the `atruncate` method, which is used to reduce the size of the memory block.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(description="The name/identifier of the memory block.")
    description: Optional[str] = Field(
        default=None, description="A description of the memory block."
    )
    priority: int = Field(
        default=0,
        description="Priority of this memory block (0 = never truncate, 1 = highest priority, etc.).",
    )
    accept_short_term_memory: bool = Field(
        default=True,
        description="Whether to accept puts from messages ejected from the short-term memory.",
    )

    @abstractmethod
    async def_aget(
        self, messages: Optional[List[ChatMessage]] = None, **block_kwargs: Any
    ) -> T:
"""Pull the memory block (async)."""

    async defaget(
        self, messages: Optional[List[ChatMessage]] = None, **block_kwargs: Any
    ) -> T:
"""
        Pull the memory block (async).

        Returns:
            T: The memory block content. One of:
            - str: A simple text string to be inserted into the template.
            - List[ContentBlock]: A list of content blocks to be inserted into the template.
            - List[ChatMessage]: A list of chat messages to be directly appended to the chat history.

        """
        return await self._aget(messages, **block_kwargs)

    @abstractmethod
    async def_aput(self, messages: List[ChatMessage]) -> None:
"""Push to the memory block (async)."""

    async defaput(
        self,
        messages: List[ChatMessage],
        from_short_term_memory: bool = False,
        session_id: Optional[str] = None,
    ) -> None:
"""Push to the memory block (async)."""
        if from_short_term_memory and not self.accept_short_term_memory:
            return

        if session_id is not None:
            for message in messages:
                message.additional_kwargs["session_id"] = session_id

        await self._aput(messages)

    async defatruncate(self, content: T, tokens_to_truncate: int) -> Optional[T]:
"""
        Truncate the memory block content to the given token limit.

        By default, truncation will remove the entire block content.

        Args:
            content:
                The content of type T, depending on what the memory block returns.
            tokens_to_truncate:
                The number of tokens requested to truncate the content by.
                Blocks may or may not truncate to the exact number of tokens requested, but it
                can be used as a hint for the block to truncate.

        Returns:
            The truncated content of type T, or None if the content is completely truncated.

        """
        return None

```
 |  
| --- | --- |  
###  aget [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemoryBlock.aget "Permanent link")

```
aget(
    messages: Optional[[]] = None,
    **block_kwargs: 
) -> 

```

Pull the memory block (async).
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
|  The memory block content. One of:  |  
| 
  * str: A simple text string to be inserted into the template.

 |  
| 
  * List[ContentBlock]: A list of content blocks to be inserted into the template.

 |  
| 
  * List[ChatMessage]: A list of chat messages to be directly appended to the chat history.

 |  
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
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
```
 | 
```
async defaget(
    self, messages: Optional[List[ChatMessage]] = None, **block_kwargs: Any
) -> T:
"""
    Pull the memory block (async).

    Returns:
        T: The memory block content. One of:
        - str: A simple text string to be inserted into the template.
        - List[ContentBlock]: A list of content blocks to be inserted into the template.
        - List[ChatMessage]: A list of chat messages to be directly appended to the chat history.

    """
    return await self._aget(messages, **block_kwargs)

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemoryBlock.aput "Permanent link")

```
aput(
    messages: [],
    from_short_term_memory:  = False,
    session_id: Optional[] = None,
) -> None

```

Push to the memory block (async).
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
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
```
 | 
```
async defaput(
    self,
    messages: List[ChatMessage],
    from_short_term_memory: bool = False,
    session_id: Optional[str] = None,
) -> None:
"""Push to the memory block (async)."""
    if from_short_term_memory and not self.accept_short_term_memory:
        return

    if session_id is not None:
        for message in messages:
            message.additional_kwargs["session_id"] = session_id

    await self._aput(messages)

```
 |  
| --- | --- |  
###  atruncate [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemoryBlock.atruncate "Permanent link")

```
atruncate(
    content: , tokens_to_truncate: 
) -> Optional[]

```

Truncate the memory block content to the given token limit.
By default, truncation will remove the entire block content.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `content`  |  The content of type T, depending on what the memory block returns.  |  _required_  |  
|  `tokens_to_truncate`  |  The number of tokens requested to truncate the content by. Blocks may or may not truncate to the exact number of tokens requested, but it can be used as a hint for the block to truncate.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Optional[T]`  |  The truncated content of type T, or None if the content is completely truncated.  |  
Source code in `llama-index-core/llama_index/core/memory/memory.py`  
| 
```
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
```
 | 
```
async defatruncate(self, content: T, tokens_to_truncate: int) -> Optional[T]:
"""
    Truncate the memory block content to the given token limit.

    By default, truncation will remove the entire block content.

    Args:
        content:
            The content of type T, depending on what the memory block returns.
        tokens_to_truncate:
            The number of tokens requested to truncate the content by.
            Blocks may or may not truncate to the exact number of tokens requested, but it
            can be used as a hint for the block to truncate.

    Returns:
        The truncated content of type T, or None if the content is completely truncated.

    """
    return None

```
 |  
| --- | --- |  
##  StaticMemoryBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.StaticMemoryBlock "Permanent link")
Bases: `BaseMemoryBlock[](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemoryBlock "BaseMemoryBlock \(llama_index.core.memory.memory.BaseMemoryBlock\)")[List[ContentBlock]]`
A memory block that returns static text.
This block is useful for including constant information or instructions in the context without relying on external processing.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `name`  |  The name of the memory block.  |  `'StaticContent'`  |  
|  `static_content`  |  `List[Annotated[TextBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.TextBlock "TextBlock \(llama_index.core.base.llms.types.TextBlock\)") | ImageBlock | AudioBlock | VideoBlock | DocumentBlock | CachePoint | CitableBlock | CitationBlock | ThinkingBlock | ToolCallBlock, FieldInfo]]`  |  Static text or content to be returned by this memory block.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/memory/memory_blocks/static.py`  
| 
```
 8
 9
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
```
 | 
```
classStaticMemoryBlock(BaseMemoryBlock[List[ContentBlock]]):
"""
    A memory block that returns static text.

    This block is useful for including constant information or instructions
    in the context without relying on external processing.
    """

    name: str = Field(
        default="StaticContent", description="The name of the memory block."
    )
    static_content: Union[List[ContentBlock]] = Field(
        description="Static text or content to be returned by this memory block."
    )

    @field_validator("static_content", mode="before")
    @classmethod
    defvalidate_static_content(
        cls, v: Union[str, List[ContentBlock]]
    ) -> List[ContentBlock]:
        if isinstance(v, str):
            v = [TextBlock(text=v)]
        return v

    async def_aget(
        self, messages: Optional[List[ChatMessage]] = None, **block_kwargs: Any
    ) -> List[ContentBlock]:
"""Return the static text, potentially filtered by conditions."""
        return self.static_content

    async def_aput(self, messages: List[ChatMessage]) -> None:
"""No-op for static blocks as they don't change."""

```
 |  
| --- | --- |  
##  VectorMemoryBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.VectorMemoryBlock "Permanent link")
Bases: `BaseMemoryBlock[](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemoryBlock "BaseMemoryBlock \(llama_index.core.memory.memory.BaseMemoryBlock\)")[str]`
A memory block that retrieves relevant information from a vector store.
This block stores conversation history in a vector store and retrieves relevant information based on the most recent messages.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `name`  |  The name of the memory block.  |  `'RetrievedMessages'`  |  
|  `vector_store`  |   |  The vector store to use for retrieval.  |  _required_  |  
|  `embed_model`  |   |  The embedding model to use for encoding queries and documents.  |  `<dynamic>`  |  
|  `similarity_top_k`  |  Number of top results to return.  |  
|  `retrieval_context_window`  |  Maximum number of messages to include for context when retrieving.  |  
|  `format_template`  |   |  Template for formatting the retrieved information.  |  `RichPromptTemplate(metadata={}, template_vars=['text'], kwargs={}, output_parser=None, template_var_mappings=None, function_mappings=None, template_str='{{ text }}')`  |  
|  `node_postprocessors`  |  `List[BaseNodePostprocessor[](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/#llama_index.core.postprocessor.types.BaseNodePostprocessor "BaseNodePostprocessor \(llama_index.core.postprocessor.types.BaseNodePostprocessor\)")]`  |  List of node postprocessors to apply to the retrieved nodes containing messages.  |  `<dynamic>`  |  
|  `query_kwargs`  |  `Dict[str, Any]`  |  Additional keyword arguments for the vector store query.  |  `<class 'dict'>`  |  
Source code in `llama-index-core/llama_index/core/memory/memory_blocks/vector.py`  
| 
```
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
```
 | 
```
classVectorMemoryBlock(BaseMemoryBlock[str]):
"""
    A memory block that retrieves relevant information from a vector store.

    This block stores conversation history in a vector store and retrieves
    relevant information based on the most recent messages.
    """

    name: str = Field(
        default="RetrievedMessages", description="The name of the memory block."
    )
    vector_store: BasePydanticVectorStore = Field(
        description="The vector store to use for retrieval."
    )
    embed_model: BaseEmbedding = Field(
        default_factory=get_default_embed_model,
        description="The embedding model to use for encoding queries and documents.",
    )
    similarity_top_k: int = Field(
        default=2, description="Number of top results to return."
    )
    retrieval_context_window: int = Field(
        default=5,
        description="Maximum number of messages to include for context when retrieving.",
    )
    format_template: BasePromptTemplate = Field(
        default=DEFAULT_RETRIEVED_TEXT_TEMPLATE,
        description="Template for formatting the retrieved information.",
    )
    node_postprocessors: List[BaseNodePostprocessor] = Field(
        default_factory=list,
        description="List of node postprocessors to apply to the retrieved nodes containing messages.",
    )
    query_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional keyword arguments for the vector store query.",
    )

    @field_validator("vector_store", mode="before")
    defvalidate_vector_store(cls, v: Any) -> "BasePydanticVectorStore":
        if not isinstance(v, BasePydanticVectorStore):
            raise ValueError("vector_store must be a BasePydanticVectorStore")
        if not v.stores_text:
            raise ValueError(
                "vector_store must store text to be used as a retrieval memory block"
            )

        return v

    @field_validator("format_template", mode="before")
    @classmethod
    defvalidate_format_template(cls, v: Any) -> "BasePromptTemplate":
        if isinstance(v, str):
            if "{{" in v and "}}" in v:
                v = RichPromptTemplate(v)
            else:
                v = PromptTemplate(v)

        return v

    def_get_text_from_messages(self, messages: List[ChatMessage]) -> str:
"""Get the text from the messages."""
        text = ""
        for i, message in enumerate(messages):
            for block in message.blocks:
                if isinstance(block, TextBlock):
                    text += block.text
            if len(messages)  1 and i != len(messages) - 1:
                text += " "
        return text

    async def_aget(
        self,
        messages: Optional[List[ChatMessage]] = None,
        session_id: Optional[str] = None,
        **block_kwargs: Any,
    ) -> str:
"""Retrieve relevant information based on recent messages."""
        if not messages or len(messages) == 0:
            return ""

        # Use the last message or a context window of messages for the query
        if (
            self.retrieval_context_window  1
            and len(messages) >= self.retrieval_context_window
        ):
            context = messages[-self.retrieval_context_window :]
        else:
            context = messages

        query_text = self._get_text_from_messages(context)
        if not query_text:
            return ""

        # Handle filtering by session_id
        if session_id is not None:
            filter = MetadataFilter(key="session_id", value=session_id)
            if "filters" in self.query_kwargs and isinstance(
                self.query_kwargs["filters"], MetadataFilters
            ):
                # only add session_id filter if it does not exist in the filters list
                session_id_filter_exists = False
                for metadata_filter in self.query_kwargs["filters"].filters:
                    if (
                        isinstance(metadata_filter, MetadataFilter)
                        and metadata_filter.key == "session_id"
                    ):
                        session_id_filter_exists = True
                        break
                if not session_id_filter_exists:
                    self.query_kwargs["filters"].filters.append(filter)
            else:
                self.query_kwargs["filters"] = MetadataFilters(filters=[filter])

        # Create and execute the query
        query_embedding = await self.embed_model.aget_query_embedding(query_text)
        query = VectorStoreQuery(
            query_str=query_text,
            query_embedding=query_embedding,
            similarity_top_k=self.similarity_top_k,
            **self.query_kwargs,
        )

        results = await self.vector_store.aquery(query)
        nodes_with_scores = [
            NodeWithScore(node=node, score=score)
            for node, score in zip(results.nodes or [], results.similarities or [])
        ]
        if not nodes_with_scores:
            return ""

        # Apply postprocessors
        for postprocessor in self.node_postprocessors:
            nodes_with_scores = await postprocessor.apostprocess_nodes(
                nodes_with_scores, query_str=query_text
            )

        # Format the results
        retrieved_text = "\n\n".join([node.get_content() for node in nodes_with_scores])
        return self.format_template.format(text=retrieved_text)

    async def_aput(self, messages: List[ChatMessage]) -> None:
"""Store messages in the vector store for future retrieval."""
        if not messages:
            return

        # Format messages with role, text content, and additional info
        texts = []
        session_id = None
        for message in messages:
            text = self._get_text_from_messages([message])
            if not text:
                continue

            # special case for session_id
            if "session_id" in message.additional_kwargs:
                session_id = message.additional_kwargs.pop("session_id")

            if message.additional_kwargs:
                text += f"\nAdditional Info: ({message.additional_kwargs!s})"

            text = f"<message role='{message.role.value}'>{text}</message>"
            texts.append(text)

        if not texts:
            return

        # Get embeddings
        text_node = TextNode(text="\n".join(texts), metadata={"session_id": session_id})
        text_node.embedding = await self.embed_model.aget_text_embedding(text_node.text)

        # Add to vector store, one node per entire message batch
        await self.vector_store.async_add([text_node])

```
 |  
| --- | --- |  
##  FactExtractionMemoryBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.FactExtractionMemoryBlock "Permanent link")
Bases: `BaseMemoryBlock[](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemoryBlock "BaseMemoryBlock \(llama_index.core.memory.memory.BaseMemoryBlock\)")[str]`
A memory block that extracts key facts from conversation history using an LLM.
This block identifies and stores discrete facts disclosed during the conversation, structuring them in XML format for easy parsing and retrieval.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `name`  |  The name of the memory block.  |  `'ExtractedFacts'`  |  
|  `llm`  |  The LLM to use for fact extraction.  |  `<dynamic>`  |  
|  `facts`  |  `List[str]`  |  List of extracted facts from the conversation.  |  `<dynamic>`  |  
|  `max_facts`  |  The maximum number of facts to store.  |  
|  `fact_extraction_prompt_template`  |   |  Template for the fact extraction prompt.  |  `RichPromptTemplate(metadata={}, template_vars=['existing_facts'], kwargs={}, output_parser=None, template_var_mappings=None, function_mappings=None, template_str='You are a precise fact extraction system designed to identify key information from conversations.\n\nINSTRUCTIONS:\n1. Review the conversation segment provided prior to this message\n2. Extract specific, concrete facts the user has disclosed or important information discovered\n3. Focus on factual information like preferences, personal details, requirements, constraints, or context\n4. Format each fact as a separate <fact> XML tag\n5. Do not include opinions, summaries, or interpretations - only extract explicit information\n6. Do not duplicate facts that are already in the existing facts list\n\n<existing_facts>\n{{ existing_facts }}\n</existing_facts>\n\nReturn ONLY the extracted facts in this exact format:\n<facts>\n  <fact>Specific fact 1</fact>\n  <fact>Specific fact 2</fact>\n  <!-- More facts as needed -->\n</facts>\n\nIf no new facts are present, return: <facts></facts>')`  |  
|  `fact_condense_prompt_template`  |   |  Template for the fact condense prompt.  |  `RichPromptTemplate(metadata={}, template_vars=['existing_facts', 'max_facts'], kwargs={}, output_parser=None, template_var_mappings=None, function_mappings=None, template_str='You are a precise fact condensing system designed to identify key information from conversations.\n\nINSTRUCTIONS:\n1. Review the current list of existing facts\n2. Condense the facts into a more concise list, less than {{ max_facts }} facts\n3. Focus on factual information like preferences, personal details, requirements, constraints, or context\n4. Format each fact as a separate <fact> XML tag\n5. Do not include opinions, summaries, or interpretations - only extract explicit information\n6. Do not duplicate facts that are already in the existing facts list\n\n<existing_facts>\n{{ existing_facts }}\n</existing_facts>\n\nReturn ONLY the condensed facts in this exact format:\n<facts>\n  <fact>Specific fact 1</fact>\n  <fact>Specific fact 2</fact>\n  <!-- More facts as needed -->\n</facts>\n\nIf no new facts are present, return: <facts></facts>')`  |  
Source code in `llama-index-core/llama_index/core/memory/memory_blocks/fact.py`  
| 
```
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
```
 | 
```
classFactExtractionMemoryBlock(BaseMemoryBlock[str]):
"""
    A memory block that extracts key facts from conversation history using an LLM.

    This block identifies and stores discrete facts disclosed during the conversation,
    structuring them in XML format for easy parsing and retrieval.
    """

    name: str = Field(
        default="ExtractedFacts", description="The name of the memory block."
    )
    llm: LLM = Field(
        default_factory=get_default_llm,
        description="The LLM to use for fact extraction.",
    )
    facts: List[str] = Field(
        default_factory=list,
        description="List of extracted facts from the conversation.",
    )
    max_facts: int = Field(
        default=50, description="The maximum number of facts to store."
    )
    fact_extraction_prompt_template: BasePromptTemplate = Field(
        default=DEFAULT_FACT_EXTRACT_PROMPT,
        description="Template for the fact extraction prompt.",
    )
    fact_condense_prompt_template: BasePromptTemplate = Field(
        default=DEFAULT_FACT_CONDENSE_PROMPT,
        description="Template for the fact condense prompt.",
    )

    @field_validator("fact_extraction_prompt_template", mode="before")
    @classmethod
    defvalidate_fact_extraction_prompt_template(
        cls, v: Union[str, BasePromptTemplate]
    ) -> BasePromptTemplate:
        if isinstance(v, str):
            if "{{" in v and "}}" in v:
                v = RichPromptTemplate(v)
            else:
                v = PromptTemplate(v)
        return v

    async def_aget(
        self, messages: Optional[List[ChatMessage]] = None, **block_kwargs: Any
    ) -> str:
"""Return the current facts as formatted text."""
        if not self.facts:
            return ""

        return "\n".join([f"<fact>{fact}</fact>" for fact in self.facts])

    async def_aput(self, messages: List[ChatMessage]) -> None:
"""Extract facts from new messages and add them to the facts list."""
        # Skip if no messages
        if not messages:
            return

        # Format existing facts for the prompt
        existing_facts_text = ""
        if self.facts:
            existing_facts_text = "\n".join(
                [f"<fact>{fact}</fact>" for fact in self.facts]
            )

        # Create the prompt
        prompt_messages = self.fact_extraction_prompt_template.format_messages(
            existing_facts=existing_facts_text,
        )

        # Get the facts extraction
        response = await self.llm.achat(messages=[*messages, *prompt_messages])

        # Parse the XML response to extract facts
        facts_text = response.message.content or ""
        new_facts = self._parse_facts_xml(facts_text)

        # Add new facts to the list, avoiding exact-match duplicates
        for fact in new_facts:
            if fact not in self.facts:
                self.facts.append(fact)

        # Condense the facts if they exceed the max_facts
        if len(self.facts)  self.max_facts:
            existing_facts_text = "\n".join(
                [f"<fact>{fact}</fact>" for fact in self.facts]
            )

            prompt_messages = self.fact_condense_prompt_template.format_messages(
                existing_facts=existing_facts_text,
                max_facts=self.max_facts,
            )
            response = await self.llm.achat(messages=[*messages, *prompt_messages])
            new_facts = self._parse_facts_xml(response.message.content or "")
            self.facts = new_facts

    def_parse_facts_xml(self, xml_text: str) -> List[str]:
"""Parse facts from XML format."""
        facts = []

        # Extract content between <fact> tags
        pattern = r"<fact>(.*?)</fact>"
        matches = re.findall(pattern, xml_text, re.DOTALL)

        # Clean up extracted facts
        for match in matches:
            fact = match.strip()
            if fact:
                facts.append(fact)

        return facts

```
 |  
| --- | --- |  
options: members: - Memory - BaseMemoryBlock - InsertMethod - StaticMemoryBlock - VectorMemoryBlock - FactExtractionMemoryBlock
