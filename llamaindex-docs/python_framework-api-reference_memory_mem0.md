# Mem0
##  Mem0Memory [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/mem0/#llama_index.memory.mem0.Mem0Memory "Permanent link")
Bases: `BaseMem0`
Source code in `llama-index-integrations/memory/llama-index-memory-mem0/llama_index/memory/mem0/base.py`  
| 
```
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
```
 | 
```
classMem0Memory(BaseMem0):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    primary_memory: SerializeAsAny[LlamaIndexMemory] = Field(
        description="Primary memory source for chat agent."
    )
    context: Mem0Context = Mem0Context()
    search_msg_limit: int = Field(
        default=5,
        description="Limit of chat history messages to use for context in search API",
    )

    def__init__(
        self, context: Optional[Union[Mem0Context, dict[str, Any]]] = None, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        if context is not None:
            if isinstance(context, dict):
                context = Mem0Context.model_validate(context)
            context.validate_provided_context()
            self.context = context

    @model_serializer
    defserialize_memory(self) -> Dict[str, Any]:
        # leaving out the two keys since they are causing serialization/deserialization problems
        return {
            "primary_memory": self.primary_memory.model_dump(
                exclude={
                    "memory_blocks_template",
                    "insert_method",
                }
            ),
            "search_msg_limit": self.search_msg_limit,
            "context": self.context.model_dump(),
        }

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "Mem0Memory"

    @classmethod
    deffrom_defaults(cls, **kwargs: Any) -> "Mem0Memory":
        raise NotImplementedError("Use either from_client or from_config")

    @classmethod
    deffrom_client(
        cls,
        context: Dict[str, Any],
        api_key: Optional[str] = None,
        host: Optional[str] = None,
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
        search_msg_limit: int = 5,
        **kwargs: Any,
    ):
        primary_memory = LlamaIndexMemory.from_defaults()

        try:
            mem0_ctx = Mem0Context.model_validate(context)
        except ValidationError as e:
            raise ValidationError(f"Context validation error: {e}")

        client = MemoryClient(
            api_key=api_key, host=host, org_id=org_id, project_id=project_id
        )
        return cls(
            primary_memory=primary_memory,
            context=mem0_ctx,
            client=client,
            search_msg_limit=search_msg_limit,
        )

    @classmethod
    deffrom_config(
        cls,
        context: Dict[str, Any],
        config: Dict[str, Any],
        search_msg_limit: int = 5,
        **kwargs: Any,
    ):
        primary_memory = LlamaIndexMemory.from_defaults()

        try:
            mem0_ctx = Mem0Context(**context)
        except Exception as e:
            raise ValidationError(f"Context validation error: {e}")

        client = Memory.from_config(config_dict=config)
        return cls(
            primary_memory=primary_memory,
            context=mem0_ctx,
            client=client,
            search_msg_limit=search_msg_limit,
        )

    defget(self, input: Optional[str] = None, **kwargs: Any) -> List[ChatMessage]:
"""Get chat history. With memory system message."""
        messages = self.primary_memory.get(input=input, **kwargs)
        input = convert_messages_to_string(messages, input, limit=self.search_msg_limit)
        ctx = self.context.model_dump()
        if len(ctx)  1:
            flt = self.context.build_filter()
            result = self.search(query=input, filters=flt)
        else:
            result = self.search(query=input, **ctx)

        search_results = result.get("results", [])

        system_message = convert_memory_to_system_message(search_results)

        # If system message is present
        if len(messages)  0 and messages[0].role == MessageRole.SYSTEM:
            assert messages[0].content is not None
            system_message = convert_memory_to_system_message(
                response=search_results, existing_system_message=messages[0]
            )
        messages.insert(0, system_message)
        return messages

    defget_all(self) -> List[ChatMessage]:
"""Returns all chat history."""
        return self.primary_memory.get_all()

    def_add_msgs_to_client_memory(self, messages: List[ChatMessage]) -> None:
"""Add new user and assistant messages to client memory."""
        self.add(
            messages=convert_chat_history_to_dict(messages),
            **self.context.model_dump(),
        )

    defput(self, message: ChatMessage) -> None:
"""Add message to chat history and client memory."""
        self._add_msgs_to_client_memory([message])
        self.primary_memory.put(message)

    defset(self, messages: List[ChatMessage]) -> None:
"""Set chat history and add new messages to client memory."""
        initial_chat_len = len(self.primary_memory.get_all())
        # Insert only new chat messages
        self._add_msgs_to_client_memory(messages[initial_chat_len:])
        self.primary_memory.set(messages)

    defreset(self) -> None:
"""Only reset chat history."""
        self.primary_memory.reset()

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/mem0/#llama_index.memory.mem0.Mem0Memory.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-integrations/memory/llama-index-memory-mem0/llama_index/memory/mem0/base.py`  
| 
```
137
138
139
140
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "Mem0Memory"

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/mem0/#llama_index.memory.mem0.Mem0Memory.get "Permanent link")

```
get(
    input: Optional[] = None, **kwargs: 
) -> []

```

Get chat history. With memory system message.
Source code in `llama-index-integrations/memory/llama-index-memory-mem0/llama_index/memory/mem0/base.py`  
| 
```
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
```
 | 
```
defget(self, input: Optional[str] = None, **kwargs: Any) -> List[ChatMessage]:
"""Get chat history. With memory system message."""
    messages = self.primary_memory.get(input=input, **kwargs)
    input = convert_messages_to_string(messages, input, limit=self.search_msg_limit)
    ctx = self.context.model_dump()
    if len(ctx)  1:
        flt = self.context.build_filter()
        result = self.search(query=input, filters=flt)
    else:
        result = self.search(query=input, **ctx)

    search_results = result.get("results", [])

    system_message = convert_memory_to_system_message(search_results)

    # If system message is present
    if len(messages)  0 and messages[0].role == MessageRole.SYSTEM:
        assert messages[0].content is not None
        system_message = convert_memory_to_system_message(
            response=search_results, existing_system_message=messages[0]
        )
    messages.insert(0, system_message)
    return messages

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/mem0/#llama_index.memory.mem0.Mem0Memory.get_all "Permanent link")

```
get_all() -> []

```

Returns all chat history.
Source code in `llama-index-integrations/memory/llama-index-memory-mem0/llama_index/memory/mem0/base.py`  
| 
```
221
222
223
```
 | 
```
defget_all(self) -> List[ChatMessage]:
"""Returns all chat history."""
    return self.primary_memory.get_all()

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/mem0/#llama_index.memory.mem0.Mem0Memory.put "Permanent link")

```
put(message: ) -> None

```

Add message to chat history and client memory.
Source code in `llama-index-integrations/memory/llama-index-memory-mem0/llama_index/memory/mem0/base.py`  
| 
```
232
233
234
235
```
 | 
```
defput(self, message: ChatMessage) -> None:
"""Add message to chat history and client memory."""
    self._add_msgs_to_client_memory([message])
    self.primary_memory.put(message)

```
 |  
| --- | --- |  
###  set [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/mem0/#llama_index.memory.mem0.Mem0Memory.set "Permanent link")

```
set(messages: []) -> None

```

Set chat history and add new messages to client memory.
Source code in `llama-index-integrations/memory/llama-index-memory-mem0/llama_index/memory/mem0/base.py`  
| 
```
237
238
239
240
241
242
```
 | 
```
defset(self, messages: List[ChatMessage]) -> None:
"""Set chat history and add new messages to client memory."""
    initial_chat_len = len(self.primary_memory.get_all())
    # Insert only new chat messages
    self._add_msgs_to_client_memory(messages[initial_chat_len:])
    self.primary_memory.set(messages)

```
 |  
| --- | --- |  
###  reset [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/mem0/#llama_index.memory.mem0.Mem0Memory.reset "Permanent link")

```
reset() -> None

```

Only reset chat history.
Source code in `llama-index-integrations/memory/llama-index-memory-mem0/llama_index/memory/mem0/base.py`  
| 
```
244
245
246
```
 | 
```
defreset(self) -> None:
"""Only reset chat history."""
    self.primary_memory.reset()

```
 |  
| --- | --- |  
options: members: - Mem0Memory
