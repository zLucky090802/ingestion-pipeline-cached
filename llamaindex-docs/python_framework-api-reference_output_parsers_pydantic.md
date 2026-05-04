# Pydantic
Output parsers.
##  BaseOutputParser [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/pydantic/#llama_index.core.output_parsers.BaseOutputParser "Permanent link")
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
###  parse `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/pydantic/#llama_index.core.output_parsers.BaseOutputParser.parse "Permanent link")

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
###  format [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/pydantic/#llama_index.core.output_parsers.BaseOutputParser.format "Permanent link")

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
###  format_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/pydantic/#llama_index.core.output_parsers.BaseOutputParser.format_messages "Permanent link")

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
##  PydanticOutputParser [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/pydantic/#llama_index.core.output_parsers.PydanticOutputParser "Permanent link")
Bases: , `Generic[Model]`
Pydantic Output Parser.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `output_cls`  |  `BaseModel`  |  Pydantic output class.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/output_parsers/pydantic.py`  
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
```
 | 
```
classPydanticOutputParser(BaseOutputParser, Generic[Model]):
"""
    Pydantic Output Parser.

    Args:
        output_cls (BaseModel): Pydantic output class.

    """

    def__init__(
        self,
        output_cls: Type[Model],
        excluded_schema_keys_from_format: Optional[List] = None,
        pydantic_format_tmpl: str = PYDANTIC_FORMAT_TMPL,
    ) -> None:
"""Init params."""
        self._output_cls = output_cls
        self._excluded_schema_keys_from_format = excluded_schema_keys_from_format or []
        self._pydantic_format_tmpl = pydantic_format_tmpl

    @property
    defoutput_cls(self) -> Type[Model]:
        return self._output_cls

    @property
    defformat_string(self) -> str:
"""Format string."""
        return self.get_format_string(escape_json=True)

    defget_format_string(self, escape_json: bool = True) -> str:
"""Format string."""
        schema_dict = self._output_cls.model_json_schema()
        for key in self._excluded_schema_keys_from_format:
            del schema_dict[key]

        schema_str = json.dumps(schema_dict, ensure_ascii=False)
        output_str = self._pydantic_format_tmpl.format(schema=schema_str)
        if escape_json:
            return output_str.replace("{", "{{").replace("}", "}}")
        else:
            return output_str

    defparse(self, text: str) -> Any:
"""Parse, validate, and correct errors programmatically."""
        json_str = extract_json_str(text)
        return self._output_cls.model_validate_json(json_str)

    defformat(self, query: str) -> str:
"""Format a query with structured output formatting instructions."""
        return query + "\n\n" + self.get_format_string(escape_json=True)

```
 |  
| --- | --- |  
###  format_string `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/pydantic/#llama_index.core.output_parsers.PydanticOutputParser.format_string "Permanent link")

```
format_string: 

```

Format string.
###  get_format_string [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/pydantic/#llama_index.core.output_parsers.PydanticOutputParser.get_format_string "Permanent link")

```
get_format_string(escape_json:  = True) -> 

```

Format string.
Source code in `llama-index-core/llama_index/core/output_parsers/pydantic.py`  
| 
```
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
```
 | 
```
defget_format_string(self, escape_json: bool = True) -> str:
"""Format string."""
    schema_dict = self._output_cls.model_json_schema()
    for key in self._excluded_schema_keys_from_format:
        del schema_dict[key]

    schema_str = json.dumps(schema_dict, ensure_ascii=False)
    output_str = self._pydantic_format_tmpl.format(schema=schema_str)
    if escape_json:
        return output_str.replace("{", "{{").replace("}", "}}")
    else:
        return output_str

```
 |  
| --- | --- |  
###  parse [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/pydantic/#llama_index.core.output_parsers.PydanticOutputParser.parse "Permanent link")

```
parse(text: ) -> 

```

Parse, validate, and correct errors programmatically.
Source code in `llama-index-core/llama_index/core/output_parsers/pydantic.py`  
| 
```
60
61
62
63
```
 | 
```
defparse(self, text: str) -> Any:
"""Parse, validate, and correct errors programmatically."""
    json_str = extract_json_str(text)
    return self._output_cls.model_validate_json(json_str)

```
 |  
| --- | --- |  
###  format [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/pydantic/#llama_index.core.output_parsers.PydanticOutputParser.format "Permanent link")

```
format(query: ) -> 

```

Format a query with structured output formatting instructions.
Source code in `llama-index-core/llama_index/core/output_parsers/pydantic.py`  
| 
```
65
66
67
```
 | 
```
defformat(self, query: str) -> str:
"""Format a query with structured output formatting instructions."""
    return query + "\n\n" + self.get_format_string(escape_json=True)

```
 |  
| --- | --- |  
##  SelectionOutputParser [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/pydantic/#llama_index.core.output_parsers.SelectionOutputParser "Permanent link")
Bases: 
Source code in `llama-index-core/llama_index/core/output_parsers/selection.py`  
| 
```
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
```
 | 
```
classSelectionOutputParser(BaseOutputParser):
    REQUIRED_KEYS = frozenset(Answer.__annotations__)

    def_filter_dict(self, json_dict: dict) -> dict:
"""Filter recursively until a dictionary matches all REQUIRED_KEYS."""
        output_dict = json_dict
        for key, val in json_dict.items():
            if key in self.REQUIRED_KEYS:
                continue
            elif isinstance(val, dict):
                output_dict = self._filter_dict(val)
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, dict):
                        output_dict = self._filter_dict(item)

        return output_dict

    def_format_output(self, output: List[dict]) -> List[dict]:
        output_json = []
        for json_dict in output:
            valid = True
            for key in self.REQUIRED_KEYS:
                if key not in json_dict:
                    valid = False
                    break

            if not valid:
                json_dict = self._filter_dict(json_dict)

            output_json.append(json_dict)

        return output_json

    defparse(self, output: str) -> Any:
        json_string = _marshal_llm_to_json(output)
        try:
            json_obj = json.loads(json_string)
        except json.JSONDecodeError as e_json:
            try:
                importyaml

                # NOTE: parsing again with pyyaml
                #       pyyaml is less strict, and allows for trailing commas
                #       right now we rely on this since guidance program generates
                #       trailing commas
                json_obj = yaml.safe_load(json_string)
            except yaml.YAMLError as e_yaml:
                raise OutputParserException(
                    f"Got invalid JSON object. Error: {e_json}{e_yaml}. "
                    f"Got JSON string: {json_string}"
                )
            except NameError as exc:
                raise ImportError("Please pip install PyYAML.") fromexc

        if isinstance(json_obj, dict):
            json_obj = [json_obj]

        if not isinstance(json_obj, list):
            raise ValueError(f"Failed to convert output to JSON: {output!r}")

        json_output = self._format_output(json_obj)
        answers = [Answer.from_dict(json_dict) for json_dict in json_output]
        return StructuredOutput(raw_output=output, parsed_output=answers)

    defformat(self, prompt_template: str) -> str:
        return prompt_template + "\n\n" + _escape_curly_braces(FORMAT_STR)

```
 |  
| --- | --- |  
options: members: - PydanticOutputParser
