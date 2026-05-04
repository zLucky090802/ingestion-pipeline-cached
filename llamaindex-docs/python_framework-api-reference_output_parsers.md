# Index
##  BaseOutputParser [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/#llama_index.core.types.BaseOutputParser "Permanent link")
Bases: `DispatcherSpanMixin`, 
Output parser class.
Source code in `llama-index-core/llama_index/core/types.py`  
| 
```
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
```
 | 
```
classBaseOutputParser(DispatcherSpanMixin, ABC):
"""Output parser class."""

    @abstractmethod
    defparse(self, output: str) -> Any:
"""Parse, validate, and correct errors programmatically."""

    defformat(self, query: str) -> str:
"""Format a query with structured output formatting instructions."""
        return query

    def_format_message(self, message: ChatMessage) -> ChatMessage:
        text_blocks: list[tuple[int, TextBlock]] = [
            (idx, block)
            for idx, block in enumerate(message.blocks)
            if isinstance(block, TextBlock)
        ]

        # add text to the last text block, or add a new text block
        format_text = ""
        if text_blocks:
            format_idx = text_blocks[-1][0]
            format_text = text_blocks[-1][1].text

            if format_idx != -1:
                # this should always be a text block
                assert isinstance(message.blocks[format_idx], TextBlock)
                message.blocks[format_idx].text = self.format(format_text)  # type: ignore
        else:
            message.blocks.append(TextBlock(text=self.format(format_text)))

        return message

    defformat_messages(self, messages: List[ChatMessage]) -> List[ChatMessage]:
"""Format a list of messages with structured output formatting instructions."""
        # NOTE: apply output parser to either the first message if it's a system message
        #       or the last message
        if messages:
            if messages[0].role == MessageRole.SYSTEM:
                # get text from the last text blocks
                messages[0] = self._format_message(messages[0])
            else:
                messages[-1] = self._format_message(messages[-1])

        return messages

    @classmethod
    def__get_pydantic_core_schema__(
        cls, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.any_schema()

    @classmethod
    def__get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> Dict[str, Any]:
        json_schema = handler(core_schema)
        return handler.resolve_ref_schema(json_schema)

```
 |  
| --- | --- |  
###  parse `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/#llama_index.core.types.BaseOutputParser.parse "Permanent link")

```
parse(output: ) -> 

```

Parse, validate, and correct errors programmatically.
Source code in `llama-index-core/llama_index/core/types.py`  
| 
```
46
47
48
```
 | 
```
@abstractmethod
defparse(self, output: str) -> Any:
"""Parse, validate, and correct errors programmatically."""

```
 |  
| --- | --- |  
###  format [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/#llama_index.core.types.BaseOutputParser.format "Permanent link")

```
format(query: ) -> 

```

Format a query with structured output formatting instructions.
Source code in `llama-index-core/llama_index/core/types.py`  
| 
```
50
51
52
```
 | 
```
defformat(self, query: str) -> str:
"""Format a query with structured output formatting instructions."""
    return query

```
 |  
| --- | --- |  
###  format_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/#llama_index.core.types.BaseOutputParser.format_messages "Permanent link")

```
format_messages(
    messages: [],
) -> []

```

Format a list of messages with structured output formatting instructions.
Source code in `llama-index-core/llama_index/core/types.py`  
| 
```
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
defformat_messages(self, messages: List[ChatMessage]) -> List[ChatMessage]:
"""Format a list of messages with structured output formatting instructions."""
    # NOTE: apply output parser to either the first message if it's a system message
    #       or the last message
    if messages:
        if messages[0].role == MessageRole.SYSTEM:
            # get text from the last text blocks
            messages[0] = self._format_message(messages[0])
        else:
            messages[-1] = self._format_message(messages[-1])

    return messages

```
 |  
| --- | --- |  
##  BasePydanticProgram [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/#llama_index.core.types.BasePydanticProgram "Permanent link")
Bases: `DispatcherSpanMixin`, , `Generic[Model]`
A base class for LLM-powered function that return a pydantic model.
Note: this interface is not yet stable.
Source code in `llama-index-core/llama_index/core/types.py`  
| 
```
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
```
 | 
```
classBasePydanticProgram(DispatcherSpanMixin, ABC, Generic[Model]):
"""
    A base class for LLM-powered function that return a pydantic model.

    Note: this interface is not yet stable.
    """

    @property
    @abstractmethod
    defoutput_cls(self) -> Type[Model]:
        pass

    @abstractmethod
    def__call__(self, *args: Any, **kwargs: Any) -> Union[Model, List[Model]]:
        pass

    async defacall(self, *args: Any, **kwargs: Any) -> Union[Model, List[Model]]:
        return self(*args, **kwargs)

    defstream_call(
        self, *args: Any, **kwargs: Any
    ) -> Generator[
        Union[Model, List[Model], "FlexibleModel", List["FlexibleModel"]], None, None
    ]:
        raise NotImplementedError("stream_call is not supported by default.")

    async defastream_call(
        self, *args: Any, **kwargs: Any
    ) -> AsyncGenerator[
        Union[Model, List[Model], "FlexibleModel", List["FlexibleModel"]], None
    ]:
        raise NotImplementedError("astream_call is not supported by default.")

```
 |  
| --- | --- |  
##  PydanticProgramMode [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/#llama_index.core.types.PydanticProgramMode "Permanent link")
Bases: `str`, `Enum`
Pydantic program mode.
Source code in `llama-index-core/llama_index/core/types.py`  
| 
```
137
138
139
140
141
142
143
144
145
```
 | 
```
classPydanticProgramMode(str, Enum):
"""Pydantic program mode."""

    DEFAULT = "default"
    OPENAI = "openai"
    LLM = "llm"
    FUNCTION = "function"
    GUIDANCE = "guidance"
    LM_FORMAT_ENFORCER = "lm-format-enforcer"

```
 |  
| --- | --- |  
##  Thread [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/#llama_index.core.types.Thread "Permanent link")
Bases: `Thread`
A wrapper for threading.Thread that copies the current context and uses the copy to run the target.
Source code in `llama-index-core/llama_index/core/types.py`  
| 
```
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
classThread(threading.Thread):
"""
    A wrapper for threading.Thread that copies the current context and uses the copy to run the target.
    """

    def__init__(
        self,
        group: Optional[Any] = None,
        target: Optional[Callable[..., Any]] = None,
        name: Optional[str] = None,
        args: Tuple[Any, ...] = (),
        kwargs: Optional[Dict[str, Any]] = None,
        *,
        daemon: Optional[bool] = None,
    ) -> None:
        if target is not None:
            args = (
                partial(target, *args, **(kwargs if isinstance(kwargs, dict) else {})),
            )
        else:
            args = ()

        super().__init__(
            group=group,
            target=copy_context().run if target else None,
            name=name,
            args=args,
            daemon=daemon,
        )

```
 |  
| --- | --- |  
options: members: - BaseOutputParser
