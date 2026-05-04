# Asi
ASI LLM package.
##  ASI [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/asi/#llama_index.llms.asi.ASI "Permanent link")
Bases: 
ASI LLM - Integration for ASI models.
Currently supported models: - asi1-mini
Examples:
`pip install llama-index-llms-asi`

```
fromllama_index.llms.asiimport ASI

# Set up the ASI class with the required model and API key
llm = ASI(model="asi1-mini", api_key="your_api_key")

# Call the complete method with a query
response = llm.complete("Explain the importance of AI")

print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-asi/llama_index/llms/asi/base.py`  
| 
```
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
```
 | 
```
classASI(OpenAILike):
"""
    ASI LLM - Integration for ASI models.

    Currently supported models:
    - asi1-mini

    Examples:
        `pip install llama-index-llms-asi`

        ```python
        from llama_index.llms.asi import ASI

        # Set up the ASI class with the required model and API key
        llm = ASI(model="asi1-mini", api_key="your_api_key")

        # Call the complete method with a query
        response = llm.complete("Explain the importance of AI")

        print(response)
        ```

    """

    def__init__(
        self,
        model: str = DEFAULT_MODEL,
        api_key: Optional[str] = None,
        api_base: str = "https://api.asi1.ai/v1",
        is_chat_model: bool = True,
        is_function_calling_model: bool = False,
        **kwargs: Any,
    ) -> None:
"""
        Initialize the ASI LLM.

        Args:
            model (str): The ASI model to use.
            api_key (Optional[str]): The API key to use.
            api_base (str): The base URL for the ASI API.
            is_chat_model (bool): Whether the model supports chat.
            is_function_calling_model (bool): Whether the model supports
                function calling.
            **kwargs (Any): Additional arguments to pass to the OpenAILike
                constructor.

        """
        api_key = api_key or os.environ.get("ASI_API_KEY", None)
        if api_key is None:
            raise ValueError(
                "Must specify `api_key` or set environment variable `ASI_API_KEY`."
            )

        super().__init__(
            model=model,
            api_key=api_key,
            api_base=api_base,
            is_chat_model=is_chat_model,
            is_function_calling_model=is_function_calling_model,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "ASI"

    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
"""
        Override stream_chat to handle ASI's unique streaming format.

        ASI's streaming format includes many empty content chunks during
        the "thinking" phase before delivering the final response.

        This implementation filters out empty chunks and only yields
        chunks with actual content.
        """

        defgen() -> ChatResponseGen:
            raw_stream = super(OpenAILike, self).stream_chat(messages, **kwargs)
            accumulated_content = ""
            for chunk in raw_stream:
                delta_content = ""
                # Extract content from the chunk
                if hasattr(chunk, "raw") and chunk.raw:
                    # Check for content in choices array
                    if "choices" in chunk.raw and chunk.raw["choices"]:
                        choice = chunk.raw["choices"][0]
                        if isinstance(choice, dict):
                            if "delta" in choice and isinstance(choice["delta"], dict):
                                if (
                                    "content" in choice["delta"]
                                    and choice["delta"]["content"]
                                ):
                                    delta_content = choice["delta"]["content"]
                # Check for content in delta directly
                if not delta_content and hasattr(chunk, "delta"):
                    if hasattr(chunk.delta, "content") and chunk.delta.content:
                        delta_content = chunk.delta.content
                    elif isinstance(chunk.delta, str) and chunk.delta:
                        delta_content = chunk.delta
                if delta_content:
                    response = ChatResponse(
                        message=ChatMessage(
                            role=MessageRole.ASSISTANT,
                            content=accumulated_content + delta_content,
                        ),
                        delta=delta_content,
                        raw=chunk.raw if hasattr(chunk, "raw") else {},
                    )
                    accumulated_content += delta_content
                    yield response

        return gen()

    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
"""
        Override astream_chat to handle ASI's unique streaming format.

        ASI's streaming format includes many empty content chunks during
        the "thinking" phase before delivering the final response.

        This implementation filters out empty chunks and only yields
        chunks with actual content.
        """

        async defgen() -> ChatResponseAsyncGen:
            raw_stream = await super(OpenAILike, self).astream_chat(messages, **kwargs)
            accumulated_content = ""
            async for chunk in raw_stream:
                delta_content = ""
                # Extract content from the chunk
                if hasattr(chunk, "raw") and chunk.raw:
                    # Check for content in choices array
                    if "choices" in chunk.raw and chunk.raw["choices"]:
                        choice = chunk.raw["choices"][0]
                        if isinstance(choice, dict):
                            if "delta" in choice and isinstance(choice["delta"], dict):
                                if (
                                    "content" in choice["delta"]
                                    and choice["delta"]["content"]
                                ):
                                    delta_content = choice["delta"]["content"]
                # Check for content in delta directly
                if not delta_content and hasattr(chunk, "delta"):
                    if hasattr(chunk.delta, "content") and chunk.delta.content:
                        delta_content = chunk.delta.content
                    elif isinstance(chunk.delta, str) and chunk.delta:
                        delta_content = chunk.delta
                if delta_content:
                    response = ChatResponse(
                        message=ChatMessage(
                            role=MessageRole.ASSISTANT,
                            content=accumulated_content + delta_content,
                        ),
                        delta=delta_content,
                        raw=chunk.raw if hasattr(chunk, "raw") else {},
                    )
                    accumulated_content += delta_content
                    yield response

        # Return the async generator function as a coroutine to match OpenAI's pattern
        return gen()

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/asi/#llama_index.llms.asi.ASI.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-asi/llama_index/llms/asi/base.py`  
| 
```
80
81
82
83
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "ASI"

```
 |  
| --- | --- |  
###  stream_chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/asi/#llama_index.llms.asi.ASI.stream_chat "Permanent link")

```
stream_chat(
    messages: Sequence[ChatMessage], **kwargs: 
) -> ChatResponseGen

```

Override stream_chat to handle ASI's unique streaming format.
ASI's streaming format includes many empty content chunks during the "thinking" phase before delivering the final response.
This implementation filters out empty chunks and only yields chunks with actual content.
Source code in `llama-index-integrations/llms/llama-index-llms-asi/llama_index/llms/asi/base.py`  
| 
```
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
```
 | 
```
defstream_chat(
    self, messages: Sequence[ChatMessage], **kwargs: Any
) -> ChatResponseGen:
"""
    Override stream_chat to handle ASI's unique streaming format.

    ASI's streaming format includes many empty content chunks during
    the "thinking" phase before delivering the final response.

    This implementation filters out empty chunks and only yields
    chunks with actual content.
    """

    defgen() -> ChatResponseGen:
        raw_stream = super(OpenAILike, self).stream_chat(messages, **kwargs)
        accumulated_content = ""
        for chunk in raw_stream:
            delta_content = ""
            # Extract content from the chunk
            if hasattr(chunk, "raw") and chunk.raw:
                # Check for content in choices array
                if "choices" in chunk.raw and chunk.raw["choices"]:
                    choice = chunk.raw["choices"][0]
                    if isinstance(choice, dict):
                        if "delta" in choice and isinstance(choice["delta"], dict):
                            if (
                                "content" in choice["delta"]
                                and choice["delta"]["content"]
                            ):
                                delta_content = choice["delta"]["content"]
            # Check for content in delta directly
            if not delta_content and hasattr(chunk, "delta"):
                if hasattr(chunk.delta, "content") and chunk.delta.content:
                    delta_content = chunk.delta.content
                elif isinstance(chunk.delta, str) and chunk.delta:
                    delta_content = chunk.delta
            if delta_content:
                response = ChatResponse(
                    message=ChatMessage(
                        role=MessageRole.ASSISTANT,
                        content=accumulated_content + delta_content,
                    ),
                    delta=delta_content,
                    raw=chunk.raw if hasattr(chunk, "raw") else {},
                )
                accumulated_content += delta_content
                yield response

    return gen()

```
 |  
| --- | --- |  
###  astream_chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/asi/#llama_index.llms.asi.ASI.astream_chat "Permanent link")

```
astream_chat(
    messages: Sequence[ChatMessage], **kwargs: 
) -> ChatResponseAsyncGen

```

Override astream_chat to handle ASI's unique streaming format.
ASI's streaming format includes many empty content chunks during the "thinking" phase before delivering the final response.
This implementation filters out empty chunks and only yields chunks with actual content.
Source code in `llama-index-integrations/llms/llama-index-llms-asi/llama_index/llms/asi/base.py`  
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
```
 | 
```
async defastream_chat(
    self, messages: Sequence[ChatMessage], **kwargs: Any
) -> ChatResponseAsyncGen:
"""
    Override astream_chat to handle ASI's unique streaming format.

    ASI's streaming format includes many empty content chunks during
    the "thinking" phase before delivering the final response.

    This implementation filters out empty chunks and only yields
    chunks with actual content.
    """

    async defgen() -> ChatResponseAsyncGen:
        raw_stream = await super(OpenAILike, self).astream_chat(messages, **kwargs)
        accumulated_content = ""
        async for chunk in raw_stream:
            delta_content = ""
            # Extract content from the chunk
            if hasattr(chunk, "raw") and chunk.raw:
                # Check for content in choices array
                if "choices" in chunk.raw and chunk.raw["choices"]:
                    choice = chunk.raw["choices"][0]
                    if isinstance(choice, dict):
                        if "delta" in choice and isinstance(choice["delta"], dict):
                            if (
                                "content" in choice["delta"]
                                and choice["delta"]["content"]
                            ):
                                delta_content = choice["delta"]["content"]
            # Check for content in delta directly
            if not delta_content and hasattr(chunk, "delta"):
                if hasattr(chunk.delta, "content") and chunk.delta.content:
                    delta_content = chunk.delta.content
                elif isinstance(chunk.delta, str) and chunk.delta:
                    delta_content = chunk.delta
            if delta_content:
                response = ChatResponse(
                    message=ChatMessage(
                        role=MessageRole.ASSISTANT,
                        content=accumulated_content + delta_content,
                    ),
                    delta=delta_content,
                    raw=chunk.raw if hasattr(chunk, "raw") else {},
                )
                accumulated_content += delta_content
                yield response

    # Return the async generator function as a coroutine to match OpenAI's pattern
    return gen()

```
 |  
| --- | --- |  
options: members: - ASI
