# Event types
Bases: `BaseModel`
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `timestamp`  |  `datetime`  |  `datetime.datetime(2026, 3, 26, 16, 17, 15, 871718)`  |  
|  `id_`  |  `'ad518095-5b2d-4688-b26b-c1650cc69d5b'`  |  
|  `span_id`  |  `str | None`  |  Return a value for the context variable for the current context. If there is no value for the variable in the current context, the method will: * return the value of the default argument of the method, if provided; or * return the default value for the context variable, if it was created with one; or * raise a LookupError.  |  `<built-in method get of _contextvars.ContextVar object at 0x7f00c2192ed0>`  |  
|  `tags`  |  `Dict[str, Any]`  |  
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/base/event.py`  
| 
```
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
```
 | 
```
classBaseEvent(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        # copy_on_model_validation = "deep"  # not supported in Pydantic V2...
    )
    timestamp: datetime = Field(default_factory=lambda: datetime.now())
    id_: str = Field(default_factory=lambda: str(uuid4()))
    span_id: Optional[str] = Field(default_factory=active_span_id.get)  # type: ignore
    tags: Dict[str, Any] = Field(default={})

    @classmethod
    defclass_name(cls) -> str:
"""Return class name."""
        return "BaseEvent"

    defdict(self, **kwargs: Any) -> Dict[str, Any]:
"""Keep for backwards compatibility."""
        return self.model_dump(**kwargs)

    defmodel_dump(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().model_dump(**kwargs)
        data["class_name"] = self.class_name()
        return data

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.base.BaseEvent.class_name "Permanent link")

```
class_name() -> 

```

Return class name.
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/base/event.py`  
| 
```
20
21
22
23
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Return class name."""
    return "BaseEvent"

```
 |  
| --- | --- |  
##  dict [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.base.BaseEvent.dict "Permanent link")

```
dict(**kwargs: ) -> [, ]

```

Keep for backwards compatibility.
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/base/event.py`  
| 
```
25
26
27
```
 | 
```
defdict(self, **kwargs: Any) -> Dict[str, Any]:
"""Keep for backwards compatibility."""
    return self.model_dump(**kwargs)

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
AgentChatWithStepEndEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `response`  |  `AgentChatResponse[](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.AgentChatResponse "AgentChatResponse


  
      dataclass
   \(llama_index.core.chat_engine.types.AgentChatResponse\)") | StreamingAgentChatResponse[](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.StreamingAgentChatResponse "StreamingAgentChatResponse


  
      dataclass
   \(llama_index.core.chat_engine.types.StreamingAgentChatResponse\)") | None`  |  Agent chat response.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/agent.py`  
| 
```
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
classAgentChatWithStepEndEvent(BaseEvent):
"""
    AgentChatWithStepEndEvent.

    Args:
        response (Optional[AGENT_CHAT_RESPONSE_TYPE]): Agent chat response.

    """

    response: Optional[AGENT_CHAT_RESPONSE_TYPE]

    @model_validator(mode="before")
    @classmethod
    defvalidate_response(cls: Any, values: Any) -> Any:
"""Validate response."""
        response = values.get("response")
        if response is None:
            pass
        elif not isinstance(response, AgentChatResponse) and not isinstance(
            response, StreamingAgentChatResponse
        ):
            raise ValueError(
                "response must be of type AgentChatResponse or StreamingAgentChatResponse"
            )

        return values

    @field_validator("response", mode="before")
    @classmethod
    defvalidate_response_type(cls: Any, response: Any) -> Any:
"""Validate response type."""
        if response is None:
            return response
        if not isinstance(response, AgentChatResponse) and not isinstance(
            response, StreamingAgentChatResponse
        ):
            raise ValueError(
                "response must be of type AgentChatResponse or StreamingAgentChatResponse"
            )
        return response

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "AgentChatWithStepEndEvent"

```
 |  
| --- | --- |  
##  validate_response `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.agent.AgentChatWithStepEndEvent.validate_response "Permanent link")

```
validate_response(values: ) -> 

```

Validate response.
Source code in `llama-index-core/llama_index/core/instrumentation/events/agent.py`  
| 
```
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
```
 | 
```
@model_validator(mode="before")
@classmethod
defvalidate_response(cls: Any, values: Any) -> Any:
"""Validate response."""
    response = values.get("response")
    if response is None:
        pass
    elif not isinstance(response, AgentChatResponse) and not isinstance(
        response, StreamingAgentChatResponse
    ):
        raise ValueError(
            "response must be of type AgentChatResponse or StreamingAgentChatResponse"
        )

    return values

```
 |  
| --- | --- |  
##  validate_response_type `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.agent.AgentChatWithStepEndEvent.validate_response_type "Permanent link")

```
validate_response_type(response: ) -> 

```

Validate response type.
Source code in `llama-index-core/llama_index/core/instrumentation/events/agent.py`  
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
```
 | 
```
@field_validator("response", mode="before")
@classmethod
defvalidate_response_type(cls: Any, response: Any) -> Any:
"""Validate response type."""
    if response is None:
        return response
    if not isinstance(response, AgentChatResponse) and not isinstance(
        response, StreamingAgentChatResponse
    ):
        raise ValueError(
            "response must be of type AgentChatResponse or StreamingAgentChatResponse"
        )
    return response

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.agent.AgentChatWithStepEndEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/agent.py`  
| 
```
109
110
111
112
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "AgentChatWithStepEndEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
AgentChatWithStepStartEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `user_msg`  |  User input message.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/agent.py`  
| 
```
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
classAgentChatWithStepStartEvent(BaseEvent):
"""
    AgentChatWithStepStartEvent.

    Args:
        user_msg (str): User input message.

    """

    user_msg: str

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "AgentChatWithStepStartEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.agent.AgentChatWithStepStartEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/agent.py`  
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
defclass_name(cls) -> str:
"""Class name."""
    return "AgentChatWithStepStartEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
AgentRunStepEndEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `step_output`  |  Task step output.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/agent.py`  
| 
```
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
```
 | 
```
classAgentRunStepEndEvent(BaseEvent):
"""
    AgentRunStepEndEvent.

    Args:
        step_output (Any): Task step output.

    """

    step_output: Any

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "AgentRunStepEndEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.agent.AgentRunStepEndEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/agent.py`  
| 
```
45
46
47
48
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "AgentRunStepEndEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
AgentRunStepStartEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `task_id`  |  Task ID.  |  _required_  |  
|  `step`  |  `Any | None`  |  Task step.  |  _required_  |  
|  `input`  |  `str | None`  |  Optional input.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/agent.py`  
| 
```
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
```
 | 
```
classAgentRunStepStartEvent(BaseEvent):
"""
    AgentRunStepStartEvent.

    Args:
        task_id (str): Task ID.
        step (Optional[Any]): Task step.
        input (Optional[str]): Optional input.

    """

    task_id: str
    step: Optional[Any]
    input: Optional[str]

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "AgentRunStepStartEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.agent.AgentRunStepStartEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/agent.py`  
| 
```
28
29
30
31
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "AgentRunStepStartEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
AgentToolCallEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `arguments`  |  Arguments.  |  _required_  |  
|  `tool`  |   |  Tool metadata.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/agent.py`  
| 
```
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
```
 | 
```
classAgentToolCallEvent(BaseEvent):
"""
    AgentToolCallEvent.

    Args:
        arguments (str): Arguments.
        tool (ToolMetadata): Tool metadata.

    """

    arguments: str
    tool: ToolMetadata

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "AgentToolCallEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.agent.AgentToolCallEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/agent.py`  
| 
```
128
129
130
131
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "AgentToolCallEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
StreamChatDeltaReceivedEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `delta`  |  Delta received from the stream chat.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/chat_engine.py`  
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
59
60
61
62
63
```
 | 
```
classStreamChatDeltaReceivedEvent(BaseEvent):
"""
    StreamChatDeltaReceivedEvent.

    Args:
        delta (str): Delta received from the stream chat.

    """

    delta: str

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "StreamChatDeltaReceivedEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.chat_engine.StreamChatDeltaReceivedEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/chat_engine.py`  
| 
```
60
61
62
63
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "StreamChatDeltaReceivedEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
StreamChatEndEvent.
Fired at the end of writing to the stream chat-engine queue.
Source code in `llama-index-core/llama_index/core/instrumentation/events/chat_engine.py`  
| 
```
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
```
 | 
```
classStreamChatEndEvent(BaseEvent):
"""
    StreamChatEndEvent.

    Fired at the end of writing to the stream chat-engine queue.
    """

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "StreamChatEndEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.chat_engine.StreamChatEndEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/chat_engine.py`  
| 
```
24
25
26
27
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "StreamChatEndEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
StreamChatErrorEvent.
Fired when an exception is raised during the stream chat-engine operation.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `exception`  |  `Exception`  |  Exception raised during the stream chat operation.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/chat_engine.py`  
| 
```
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
```
 | 
```
classStreamChatErrorEvent(BaseEvent):
"""
    StreamChatErrorEvent.

    Fired when an exception is raised during the stream chat-engine operation.

    Args:
        exception (Exception): Exception raised during the stream chat operation.

    """

    exception: Exception

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "StreamChatErrorEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.chat_engine.StreamChatErrorEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/chat_engine.py`  
| 
```
43
44
45
46
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "StreamChatErrorEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
StreamChatStartEvent.
Fired at the start of writing to the stream chat-engine queue.
Source code in `llama-index-core/llama_index/core/instrumentation/events/chat_engine.py`  
| 
```
 4
 5
 6
 7
 8
 9
10
11
12
13
14
```
 | 
```
classStreamChatStartEvent(BaseEvent):
"""
    StreamChatStartEvent.

    Fired at the start of writing to the stream chat-engine queue.
    """

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "StreamChatStartEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.chat_engine.StreamChatStartEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/chat_engine.py`  
| 
```
11
12
13
14
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "StreamChatStartEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
EmbeddingEndEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `chunks`  |  `List[str]`  |  List of chunks.  |  _required_  |  
|  `embeddings`  |  `List[List[float]]`  |  List of embeddings.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/embedding.py`  
| 
```
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
```
 | 
```
classEmbeddingEndEvent(BaseEvent):
"""
    EmbeddingEndEvent.

    Args:
        chunks (List[str]): List of chunks.
        embeddings (List[List[float]]): List of embeddings.

    """

    chunks: List[str]
    embeddings: List[List[float]]

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "EmbeddingEndEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.embedding.EmbeddingEndEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/embedding.py`  
| 
```
38
39
40
41
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "EmbeddingEndEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
EmbeddingStartEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model_dict`  |  `dict`  |  Model dictionary containing details about the embedding model.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/embedding.py`  
| 
```
 7
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
```
 | 
```
classEmbeddingStartEvent(BaseEvent):
"""
    EmbeddingStartEvent.

    Args:
        model_dict (dict): Model dictionary containing details about the embedding model.

    """

    model_config = ConfigDict(protected_namespaces=("pydantic_model_",))
    model_dict: dict

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "EmbeddingStartEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.embedding.EmbeddingStartEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/embedding.py`  
| 
```
19
20
21
22
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "EmbeddingStartEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
LLMChatEndEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `List[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  List of chat messages.  |  _required_  |  
|  `response`  |  `ChatResponse[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatResponse "ChatResponse \(llama_index.core.base.llms.types.ChatResponse\)") | None`  |  Last chat response.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/llm.py`  
| 
```
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
classLLMChatEndEvent(BaseEvent):
"""
    LLMChatEndEvent.

    Args:
        messages (List[ChatMessage]): List of chat messages.
        response (Optional[ChatResponse]): Last chat response.

    """

    messages: List[ChatMessage]
    response: Optional[ChatResponse]

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "LLMChatEndEvent"

    defmodel_dump(self, **kwargs: Any) -> Dict[str, Any]:
        if self.response is not None and isinstance(self.response.raw, BaseModel):
            self.response.raw = self.response.raw.model_dump()

        return super().model_dump(**kwargs)

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.llm.LLMChatEndEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/llm.py`  
| 
```
237
238
239
240
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "LLMChatEndEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
LLMChatStartEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `List[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  List of chat messages.  |  _required_  |  
|  `additional_kwargs`  |  `dict`  |  Additional keyword arguments.  |  _required_  |  
|  `model_dict`  |  `dict`  |  Model dictionary.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/llm.py`  
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
194
195
196
```
 | 
```
classLLMChatStartEvent(BaseEvent):
"""
    LLMChatStartEvent.

    Args:
        messages (List[ChatMessage]): List of chat messages.
        additional_kwargs (dict): Additional keyword arguments.
        model_dict (dict): Model dictionary.

    """

    model_config = ConfigDict(protected_namespaces=("pydantic_model_",))
    messages: List[ChatMessage]
    additional_kwargs: dict
    model_dict: dict

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "LLMChatStartEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.llm.LLMChatStartEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/llm.py`  
| 
```
193
194
195
196
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "LLMChatStartEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
LLMCompletionEndEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  The prompt to be completed.  |  _required_  |  
|  `response`  |   |  Completion response.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/llm.py`  
| 
```
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
```
 | 
```
classLLMCompletionEndEvent(BaseEvent):
"""
    LLMCompletionEndEvent.

    Args:
        prompt (str): The prompt to be completed.
        response (CompletionResponse): Completion response.

    """

    prompt: str
    response: CompletionResponse

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "LLMCompletionEndEvent"

    defmodel_dump(self, **kwargs: Any) -> Dict[str, Any]:
        if isinstance(self.response.raw, BaseModel):
            self.response.raw = self.response.raw.model_dump()

        return super().model_dump(**kwargs)

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.llm.LLMCompletionEndEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/llm.py`  
| 
```
165
166
167
168
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "LLMCompletionEndEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
LLMCompletionStartEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  The prompt to be completed.  |  _required_  |  
|  `additional_kwargs`  |  `dict`  |  Additional keyword arguments.  |  _required_  |  
|  `model_dict`  |  `dict`  |  Model dictionary.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/llm.py`  
| 
```
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
classLLMCompletionStartEvent(BaseEvent):
"""
    LLMCompletionStartEvent.

    Args:
        prompt (str): The prompt to be completed.
        additional_kwargs (dict): Additional keyword arguments.
        model_dict (dict): Model dictionary.

    """

    model_config = ConfigDict(protected_namespaces=("pydantic_model_",))
    prompt: str
    additional_kwargs: dict
    model_dict: dict

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "LLMCompletionStartEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.llm.LLMCompletionStartEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/llm.py`  
| 
```
121
122
123
124
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "LLMCompletionStartEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
LLMPredictEndEvent.
The result of an llm.predict() call.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `output`  |  Output.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/llm.py`  
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
```
 | 
```
classLLMPredictEndEvent(BaseEvent):
"""
    LLMPredictEndEvent.

    The result of an llm.predict() call.

    Args:
        output (str): Output.

    """

    output: str

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "LLMPredictEndEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.llm.LLMPredictEndEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/llm.py`  
| 
```
44
45
46
47
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "LLMPredictEndEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
LLMPredictStartEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `template`  |   |  Prompt template.  |  _required_  |  
|  `template_args`  |  `dict | None`  |  Prompt template arguments.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/llm.py`  
| 
```
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
```
 | 
```
classLLMPredictStartEvent(BaseEvent):
"""
    LLMPredictStartEvent.

    Args:
        template (BasePromptTemplate): Prompt template.
        template_args (Optional[dict]): Prompt template arguments.

    """

    template: SerializeAsAny[BasePromptTemplate]
    template_args: Optional[dict]

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "LLMPredictStartEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.llm.LLMPredictStartEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/llm.py`  
| 
```
25
26
27
28
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "LLMPredictStartEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
QueryEndEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  Query as a string or query bundle.  |  _required_  |  
|  `response`  |  `Response[](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Response "Response


  
      dataclass
   \(llama_index.core.base.response.schema.Response\)") | StreamingResponse | AsyncStreamingResponse | PydanticResponse`  |  Response.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/query.py`  
| 
```
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
classQueryEndEvent(BaseEvent):
"""
    QueryEndEvent.

    Args:
        query (QueryType): Query as a string or query bundle.
        response (RESPONSE_TYPE): Response.

    """

    query: QueryType
    response: RESPONSE_TYPE

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "QueryEndEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.query.QueryEndEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/query.py`  
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
"""Class name."""
    return "QueryEndEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
QueryStartEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  Query as a string or query bundle.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/query.py`  
| 
```
 6
 7
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
```
 | 
```
classQueryStartEvent(BaseEvent):
"""
    QueryStartEvent.

    Args:
        query (QueryType): Query as a string or query bundle.

    """

    query: QueryType

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "QueryStartEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.query.QueryStartEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/query.py`  
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
"""Class name."""
    return "QueryStartEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
RetrievalEndEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `str_or_query_bundle`  |   |  Query bundle.  |  _required_  |  
|  `nodes`  |  `List[NodeWithScore[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.NodeWithScore "NodeWithScore \(llama_index.core.schema.NodeWithScore\)")]`  |  List of nodes with scores.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/retrieval.py`  
| 
```
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
classRetrievalEndEvent(BaseEvent):
"""
    RetrievalEndEvent.

    Args:
        str_or_query_bundle (QueryType): Query bundle.
        nodes (List[NodeWithScore]): List of nodes with scores.

    """

    str_or_query_bundle: QueryType
    nodes: List[NodeWithScore]

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "RetrievalEndEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.retrieval.RetrievalEndEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/retrieval.py`  
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
"""Class name."""
    return "RetrievalEndEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
RetrievalStartEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `str_or_query_bundle`  |   |  Query bundle.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/retrieval.py`  
| 
```
 6
 7
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
```
 | 
```
classRetrievalStartEvent(BaseEvent):
"""
    RetrievalStartEvent.

    Args:
        str_or_query_bundle (QueryType): Query bundle.

    """

    str_or_query_bundle: QueryType

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "RetrievalStartEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.retrieval.RetrievalStartEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/retrieval.py`  
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
"""Class name."""
    return "RetrievalStartEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
GetResponseEndEvent.
Source code in `llama-index-core/llama_index/core/instrumentation/events/synthesis.py`  
| 
```
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
```
 | 
```
classGetResponseEndEvent(BaseEvent):
"""GetResponseEndEvent."""

    # TODO: consumes the first chunk of generators??
    # response: RESPONSE_TEXT_TYPE

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "GetResponseEndEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.synthesis.GetResponseEndEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/synthesis.py`  
| 
```
69
70
71
72
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "GetResponseEndEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
GetResponseStartEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_str`  |  Query string.  |  _required_  |  
|  `text_chunks`  |  `List[str]`  |  List of text chunks.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/synthesis.py`  
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
```
 | 
```
classGetResponseStartEvent(BaseEvent):
"""
    GetResponseStartEvent.

    Args:
        query_str (str): Query string.
        text_chunks (List[str]): List of text chunks.

    """

    query_str: str
    text_chunks: List[str]

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "GetResponseStartEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.synthesis.GetResponseStartEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/synthesis.py`  
| 
```
57
58
59
60
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "GetResponseStartEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
SynthesizeEndEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  Query as a string or query bundle.  |  _required_  |  
|  `response`  |  `Response[](https://developers.llamaindex.ai/python/framework-api-reference/storage/storage_context/#llama_index.core.Response "Response


  
      dataclass
   \(llama_index.core.base.response.schema.Response\)") | StreamingResponse | AsyncStreamingResponse | PydanticResponse`  |  Response.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/synthesis.py`  
| 
```
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
```
 | 
```
classSynthesizeEndEvent(BaseEvent):
"""
    SynthesizeEndEvent.

    Args:
        query (QueryType): Query as a string or query bundle.
        response (RESPONSE_TYPE): Response.

    """

    query: QueryType
    response: RESPONSE_TYPE

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "SynthesizeEndEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.synthesis.SynthesizeEndEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/synthesis.py`  
| 
```
38
39
40
41
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "SynthesizeEndEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseEvent`
SynthesizeStartEvent.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  Query as a string or query bundle.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/instrumentation/events/synthesis.py`  
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
```
 | 
```
classSynthesizeStartEvent(BaseEvent):
"""
    SynthesizeStartEvent.

    Args:
        query (QueryType): Query as a string or query bundle.

    """

    query: QueryType

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "SynthesizeStartEvent"

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/event_types/#llama_index.core.instrumentation.events.synthesis.SynthesizeStartEvent.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-core/llama_index/core/instrumentation/events/synthesis.py`  
| 
```
19
20
21
22
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "SynthesizeStartEvent"

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
