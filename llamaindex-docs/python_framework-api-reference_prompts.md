# Index
Prompt class.
##  ChatMessage [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.ChatMessage "Permanent link")
Bases: 
Chat message.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `role`  |   |  `<MessageRole.USER: 'user'>`  |  
|  `additional_kwargs`  |  `dict[str, Any]`  |  dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs dict(iterable) -> new dictionary initialized as if via: d = {} for k, v in iterable: d[k] = v dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list. For example: dict(one=1, two=2)  |  `<class 'dict'>`  |  
|  `blocks`  |  `list[Annotated[TextBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.TextBlock "TextBlock \(llama_index.core.base.llms.types.TextBlock\)") | ImageBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ImageBlock "ImageBlock \(llama_index.core.base.llms.types.ImageBlock\)") | AudioBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.AudioBlock "AudioBlock \(llama_index.core.base.llms.types.AudioBlock\)") | VideoBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.VideoBlock "VideoBlock \(llama_index.core.base.llms.types.VideoBlock\)") | DocumentBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.DocumentBlock "DocumentBlock \(llama_index.core.base.llms.types.DocumentBlock\)") | CachePoint[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CachePoint "CachePoint \(llama_index.core.base.llms.types.CachePoint\)") | CitableBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CitableBlock "CitableBlock \(llama_index.core.base.llms.types.CitableBlock\)") | CitationBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.CitationBlock "CitationBlock \(llama_index.core.base.llms.types.CitationBlock\)") | ThinkingBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ThinkingBlock "ThinkingBlock \(llama_index.core.base.llms.types.ThinkingBlock\)") | ToolCallBlock[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ToolCallBlock "ToolCallBlock \(llama_index.core.base.llms.types.ToolCallBlock\)"), FieldInfo]]`  |  Built-in mutable sequence. If no argument is given, the constructor creates a new empty list. The argument must be an iterable if specified.  |  `<dynamic>`  |  
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
1170
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
1188
1189
1190
1191
1192
1193
1194
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
1206
1207
1208
1209
1210
1211
1212
1213
1214
1215
1216
1217
1218
1219
1220
1221
1222
1223
1224
1225
1226
1227
1228
1229
1230
1231
1232
1233
1234
1235
1236
1237
1238
1239
1240
1241
1242
1243
1244
1245
1246
1247
1248
1249
1250
1251
1252
1253
1254
1255
1256
1257
1258
1259
1260
1261
1262
1263
1264
1265
1266
1267
1268
1269
1270
1271
1272
1273
1274
1275
1276
1277
1278
1279
1280
1281
```
 | 
```
classChatMessage(BaseRecursiveContentBlock):
"""Chat message."""

    role: MessageRole = MessageRole.USER
    additional_kwargs: dict[str, Any] = Field(default_factory=dict)
    blocks: list[ContentBlock] = Field(default_factory=list)

    def__init__(self, /, content: Any | None = None, **data: Any) -> None:
"""
        Keeps backward compatibility with the old `content` field.

        If content was passed and contained text, store a single TextBlock.
        If content was passed and it was a list, assume it's a list of content blocks and store it.
        """
        if content is not None:
            if isinstance(content, str):
                data["blocks"] = [TextBlock(text=content)]
            elif isinstance(content, list):
                data["blocks"] = content

        super().__init__(**data)

    @model_validator(mode="after")
    deflegacy_additional_kwargs_image(self) -> Self:
"""
        Provided for backward compatibility.

        If `additional_kwargs` contains an `images` key, assume the value is a list
        of ImageDocument and convert them into image blocks.
        """
        if documents := self.additional_kwargs.get("images"):
            documents = cast(list[ImageDocument], documents)
            for doc in documents:
                img_base64_bytes = doc.resolve_image(as_base64=True).read()
                self.blocks.append(ImageBlock(image=img_base64_bytes))
        return self

    @classmethod
    defnested_blocks_field_name(self) -> str:
        return "blocks"

    @property
    defcontent(self) -> str | None:
"""
        Keeps backward compatibility with the old `content` field.

        Returns:
            The cumulative content of the TextBlock blocks, None if there are none.

        """
        content_strs = []
        for block in self.blocks:
            if isinstance(block, TextBlock):
                content_strs.append(block.text)

        ct = "\n".join(content_strs) or None
        if ct is None and len(content_strs) == 1:
            return ""
        return ct

    @content.setter
    defcontent(self, content: str) -> None:
"""
        Keeps backward compatibility with the old `content` field.

        Raises:
            ValueError: if blocks contains more than a block, or a block that's not TextBlock.

        """
        if not self.blocks:
            self.blocks = [TextBlock(text=content)]
        elif len(self.blocks) == 1 and isinstance(self.blocks[0], TextBlock):
            self.blocks = [TextBlock(text=content)]
        else:
            raise ValueError(
                "ChatMessage contains multiple blocks, use 'ChatMessage.blocks' instead."
            )

    def__str__(self) -> str:
        return f"{self.role.value}: {self.content}"

    @classmethod
    deffrom_str(
        cls,
        content: str,
        role: Union[MessageRole, str] = MessageRole.USER,
        **kwargs: Any,
    ) -> Self:
        if isinstance(role, str):
            role = MessageRole(role)
        return cls(role=role, blocks=[TextBlock(text=content)], **kwargs)

    def_recursive_serialization(self, value: Any) -> Any:
        if isinstance(value, BaseModel):
            value.model_rebuild()  # ensures all fields are initialized and serializable
            return value.model_dump()  # type: ignore
        if isinstance(value, dict):
            return {
                key: self._recursive_serialization(value)
                for key, value in value.items()
            }
        if isinstance(value, list):
            return [self._recursive_serialization(item) for item in value]

        if isinstance(value, bytes):
            return base64.b64encode(value).decode("utf-8")

        return value

    @field_serializer("additional_kwargs", check_fields=False)
    defserialize_additional_kwargs(self, value: Any, _info: Any) -> Any:
        return self._recursive_serialization(value)

```
 |  
| --- | --- |  
###  content `property` `writable` [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.ChatMessage.content "Permanent link")

```
content:  | None

```

Keeps backward compatibility with the old `content` field.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `str | None`  |  The cumulative content of the TextBlock blocks, None if there are none.  |  
###  legacy_additional_kwargs_image [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.ChatMessage.legacy_additional_kwargs_image "Permanent link")

```
legacy_additional_kwargs_image() -> 

```

Provided for backward compatibility.
If `additional_kwargs` contains an `images` key, assume the value is a list of ImageDocument and convert them into image blocks.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
| 
```
1192
1193
1194
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
```
 | 
```
@model_validator(mode="after")
deflegacy_additional_kwargs_image(self) -> Self:
"""
    Provided for backward compatibility.

    If `additional_kwargs` contains an `images` key, assume the value is a list
    of ImageDocument and convert them into image blocks.
    """
    if documents := self.additional_kwargs.get("images"):
        documents = cast(list[ImageDocument], documents)
        for doc in documents:
            img_base64_bytes = doc.resolve_image(as_base64=True).read()
            self.blocks.append(ImageBlock(image=img_base64_bytes))
    return self

```
 |  
| --- | --- |  
##  MessageRole [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.MessageRole "Permanent link")
Bases: `str`, `Enum`
Message role.
Source code in `llama-index-core/llama_index/core/base/llms/types.py`  
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
```
 | 
```
classMessageRole(str, Enum):
"""Message role."""

    SYSTEM = "system"
    DEVELOPER = "developer"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"
    TOOL = "tool"
    CHATBOT = "chatbot"
    MODEL = "model"

```
 |  
| --- | --- |  
##  BasePromptTemplate [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "Permanent link")
Bases: `BaseModel`, 
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `metadata`  |  `Dict[str, Any]`  |  _required_  |  
|  `template_vars`  |  `List[str]`  |  _required_  |  
|  `kwargs`  |  `Dict[str, str]`  |  _required_  |  
|  `output_parser`  |  `BaseOutputParser[](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/#llama_index.core.types.BaseOutputParser "BaseOutputParser \(llama_index.core.types.BaseOutputParser\)") | None`  |  _required_  |  
|  `template_var_mappings`  |  `Dict[str, Any] | None`  |  Template variable mappings (Optional).  |  `<class 'dict'>`  |  
|  `function_mappings`  |  `Dict[str, Annotated[Callable, WithJsonSchema, WithJsonSchema, PlainSerializer]] | None`  |  Function mappings (Optional). This is a mapping from template variable names to functions that take in the current kwargs and return a string.  |  `<class 'dict'>`  |  
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
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
```
 | 
```
classBasePromptTemplate(BaseModel, ABC):  # type: ignore[no-redef]
    model_config = ConfigDict(arbitrary_types_allowed=True)
    metadata: Dict[str, Any]
    template_vars: List[str]
    kwargs: Dict[str, str]
    output_parser: Optional[BaseOutputParser]
    template_var_mappings: Optional[Dict[str, Any]] = Field(
        default_factory=dict,  # type: ignore
        description="Template variable mappings (Optional).",
    )
    function_mappings: Optional[Dict[str, AnnotatedCallable]] = Field(
        default_factory=dict,  # type: ignore
        description=(
            "Function mappings (Optional). This is a mapping from template "
            "variable names to functions that take in the current kwargs and "
            "return a string."
        ),
    )

    def_map_template_vars(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
"""For keys in template_var_mappings, swap in the right keys."""
        template_var_mappings = self.template_var_mappings or {}
        return {template_var_mappings.get(k, k): v for k, v in kwargs.items()}

    def_map_function_vars(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
"""
        For keys in function_mappings, compute values and combine w/ kwargs.

        Users can pass in functions instead of fixed values as format variables.
        For each function, we call the function with the current kwargs,
        get back the value, and then use that value in the template
        for the corresponding format variable.

        """
        function_mappings = self.function_mappings or {}
        # first generate the values for the functions
        new_kwargs = {}
        for k, v in function_mappings.items():
            # TODO: figure out what variables to pass into each function
            # is it the kwargs specified during query time? just the fixed kwargs?
            # all kwargs?
            new_kwargs[k] = v(**kwargs)

        # then, add the fixed variables only if not in new_kwargs already
        # (implying that function mapping will override fixed variables)
        for k, v in kwargs.items():
            if k not in new_kwargs:
                new_kwargs[k] = v

        return new_kwargs

    def_map_all_vars(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
"""
        Map both template and function variables.

        We (1) first call function mappings to compute functions,
        and then (2) call the template_var_mappings.

        """
        # map function
        new_kwargs = self._map_function_vars(kwargs)
        # map template vars (to point to existing format vars in string template)
        return self._map_template_vars(new_kwargs)

    @abstractmethod
    defpartial_format(self, **kwargs: Any) -> "BasePromptTemplate": ...

    @abstractmethod
    defformat(self, llm: Optional[BaseLLM] = None, **kwargs: Any) -> str: ...

    @abstractmethod
    defformat_messages(
        self, llm: Optional[BaseLLM] = None, **kwargs: Any
    ) -> List[ChatMessage]: ...

    @abstractmethod
    defget_template(self, llm: Optional[BaseLLM] = None) -> str: ...

```
 |  
| --- | --- |  
##  ChatPromptTemplate [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.ChatPromptTemplate "Permanent link")
Bases: 
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `message_templates`  |  `List[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  _required_  |  
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
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
```
 | 
```
classChatPromptTemplate(BasePromptTemplate):  # type: ignore[no-redef]
    message_templates: List[ChatMessage]

    def__init__(
        self,
        message_templates: Sequence[ChatMessage],
        prompt_type: str = PromptType.CUSTOM,
        output_parser: Optional[BaseOutputParser] = None,
        metadata: Optional[Dict[str, Any]] = None,
        template_var_mappings: Optional[Dict[str, Any]] = None,
        function_mappings: Optional[Dict[str, Callable]] = None,
        **kwargs: Any,
    ):
        if metadata is None:
            metadata = {}
        metadata["prompt_type"] = prompt_type

        template_vars = []
        for message_template in message_templates:
            template_vars.extend(message_template.get_template_vars())

        super().__init__(
            message_templates=message_templates,
            kwargs=kwargs,
            metadata=metadata,
            output_parser=output_parser,
            template_vars=template_vars,
            template_var_mappings=template_var_mappings,
            function_mappings=function_mappings,
        )

    @classmethod
    deffrom_messages(
        cls,
        message_templates: Union[List[Tuple[str, str]], List[ChatMessage]],
        **kwargs: Any,
    ) -> "ChatPromptTemplate":
"""From messages."""
        if isinstance(message_templates[0], tuple):
            message_templates = [
                ChatMessage.from_str(role=role, content=content)  # type: ignore[arg-type]
                for role, content in message_templates
            ]
        return cls(message_templates=message_templates, **kwargs)  # type: ignore[arg-type]

    defpartial_format(self, **kwargs: Any) -> "ChatPromptTemplate":
        prompt = deepcopy(self)
        prompt.kwargs.update(kwargs)
        return prompt

    defformat(
        self,
        llm: Optional[BaseLLM] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        **kwargs: Any,
    ) -> str:
        del llm  # unused
        messages = self.format_messages(**kwargs)

        if messages_to_prompt is not None:
            return messages_to_prompt(messages)

        return default_messages_to_prompt(messages)

    defformat_messages(
        self, llm: Optional[BaseLLM] = None, **kwargs: Any
    ) -> List[ChatMessage]:
        del llm  # unused
"""Format the prompt into a list of chat messages."""
        all_kwargs = {
            **self.kwargs,
            **kwargs,
        }
        mapped_all_kwargs = self._map_all_vars(all_kwargs)

        messages: List[ChatMessage] = []
        for message_template in self.message_templates:
            # Handle messages with multiple blocks
            if message_template.blocks:
                template_vars = message_template.get_template_vars()
                relevant_kwargs = {
                    k: v for k, v in mapped_all_kwargs.items() if k in template_vars
                }
                formatted_message = message_template.format_vars(**relevant_kwargs)
                messages.append(formatted_message)
            else:
                # Handle empty messages (if any)
                messages.append(message_template.model_copy())

        if self.output_parser is not None:
            messages = self.output_parser.format_messages(messages)

        return messages

    defget_template(self, llm: Optional[BaseLLM] = None) -> str:
        return default_messages_to_prompt(self.message_templates)

```
 |  
| --- | --- |  
###  from_messages `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.ChatPromptTemplate.from_messages "Permanent link")

```
from_messages(
    message_templates: Union[
        [Tuple[, ]], []
    ],
    **kwargs: 
) -> 

```

From messages.
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_messages(
    cls,
    message_templates: Union[List[Tuple[str, str]], List[ChatMessage]],
    **kwargs: Any,
) -> "ChatPromptTemplate":
"""From messages."""
    if isinstance(message_templates[0], tuple):
        message_templates = [
            ChatMessage.from_str(role=role, content=content)  # type: ignore[arg-type]
            for role, content in message_templates
        ]
    return cls(message_templates=message_templates, **kwargs)  # type: ignore[arg-type]

```
 |  
| --- | --- |  
##  LangchainPromptTemplate [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.LangchainPromptTemplate "Permanent link")
Bases: 
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `selector`  |  _required_  |  
|  `requires_langchain_llm`  |  `bool`  |  `False`  |  
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
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
```
 | 
```
classLangchainPromptTemplate(BasePromptTemplate):  # type: ignore[no-redef]
    selector: Any
    requires_langchain_llm: bool = False

    def__init__(
        self,
        template: Optional["LangchainTemplate"] = None,
        selector: Optional["LangchainSelector"] = None,
        output_parser: Optional[BaseOutputParser] = None,
        prompt_type: str = PromptType.CUSTOM,
        metadata: Optional[Dict[str, Any]] = None,
        template_var_mappings: Optional[Dict[str, Any]] = None,
        function_mappings: Optional[Dict[str, Callable]] = None,
        requires_langchain_llm: bool = False,
    ) -> None:
        try:
            fromllama_index.core.bridge.langchainimport (
                ConditionalPromptSelector as LangchainSelector,
            )
        except ImportError:
            raise ImportError(
                "Must install `llama_index[langchain]` to use LangchainPromptTemplate."
            )
        if selector is None:
            if template is None:
                raise ValueError("Must provide either template or selector.")
            selector = LangchainSelector(default_prompt=template)
        else:
            if template is not None:
                raise ValueError("Must provide either template or selector.")
            selector = selector

        kwargs = selector.default_prompt.partial_variables
        template_vars = selector.default_prompt.input_variables

        if metadata is None:
            metadata = {}
        metadata["prompt_type"] = prompt_type

        super().__init__(
            selector=selector,
            metadata=metadata,
            kwargs=kwargs,
            template_vars=template_vars,
            output_parser=output_parser,
            template_var_mappings=template_var_mappings,
            function_mappings=function_mappings,
            requires_langchain_llm=requires_langchain_llm,
        )

    defpartial_format(self, **kwargs: Any) -> "BasePromptTemplate":
"""Partially format the prompt."""
        fromllama_index.core.bridge.langchainimport (
            ConditionalPromptSelector as LangchainSelector,
        )

        mapped_kwargs = self._map_all_vars(kwargs)
        default_prompt = self.selector.default_prompt.partial(**mapped_kwargs)
        conditionals = [
            (condition, prompt.partial(**mapped_kwargs))
            for condition, prompt in self.selector.conditionals
        ]
        lc_selector = LangchainSelector(
            default_prompt=default_prompt, conditionals=conditionals
        )

        # copy full prompt object, replace selector
        lc_prompt = deepcopy(self)
        lc_prompt.selector = lc_selector
        return lc_prompt

    defformat(self, llm: Optional[BaseLLM] = None, **kwargs: Any) -> str:
"""Format the prompt into a string."""
        fromllama_index.llms.langchainimport LangChainLLM  # pants: no-infer-dep

        if llm is not None:
            # if llamaindex LLM is provided, and we require a langchain LLM,
            # then error. but otherwise if `requires_langchain_llm` is False,
            # then we can just use the default prompt
            if not isinstance(llm, LangChainLLM) and self.requires_langchain_llm:
                raise ValueError("Must provide a LangChainLLM.")
            elif not isinstance(llm, LangChainLLM):
                lc_template = self.selector.default_prompt
            else:
                lc_template = self.selector.get_prompt(llm=llm.llm)
        else:
            lc_template = self.selector.default_prompt

        # if there's mappings specified, make sure those are used
        mapped_kwargs = self._map_all_vars(kwargs)
        return lc_template.format(**mapped_kwargs)

    defformat_messages(
        self, llm: Optional[BaseLLM] = None, **kwargs: Any
    ) -> List[ChatMessage]:
"""Format the prompt into a list of chat messages."""
        fromllama_index.llms.langchainimport LangChainLLM  # pants: no-infer-dep
        fromllama_index.llms.langchain.utilsimport (
            from_lc_messages,
        )  # pants: no-infer-dep

        if llm is not None:
            # if llamaindex LLM is provided, and we require a langchain LLM,
            # then error. but otherwise if `requires_langchain_llm` is False,
            # then we can just use the default prompt
            if not isinstance(llm, LangChainLLM) and self.requires_langchain_llm:
                raise ValueError("Must provide a LangChainLLM.")
            elif not isinstance(llm, LangChainLLM):
                lc_template = self.selector.default_prompt
            else:
                lc_template = self.selector.get_prompt(llm=llm.llm)
        else:
            lc_template = self.selector.default_prompt

        # if there's mappings specified, make sure those are used
        mapped_kwargs = self._map_all_vars(kwargs)
        lc_prompt_value = lc_template.format_prompt(**mapped_kwargs)
        lc_messages = lc_prompt_value.to_messages()
        return from_lc_messages(lc_messages)

    defget_template(self, llm: Optional[BaseLLM] = None) -> str:
        fromllama_index.llms.langchainimport LangChainLLM  # pants: no-infer-dep

        if llm is not None:
            # if llamaindex LLM is provided, and we require a langchain LLM,
            # then error. but otherwise if `requires_langchain_llm` is False,
            # then we can just use the default prompt
            if not isinstance(llm, LangChainLLM) and self.requires_langchain_llm:
                raise ValueError("Must provide a LangChainLLM.")
            elif not isinstance(llm, LangChainLLM):
                lc_template = self.selector.default_prompt
            else:
                lc_template = self.selector.get_prompt(llm=llm.llm)
        else:
            lc_template = self.selector.default_prompt

        try:
            return str(lc_template.template)  # type: ignore
        except AttributeError:
            return str(lc_template)

```
 |  
| --- | --- |  
###  partial_format [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.LangchainPromptTemplate.partial_format "Permanent link")

```
partial_format(**kwargs: ) -> 

```

Partially format the prompt.
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
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
```
 | 
```
defpartial_format(self, **kwargs: Any) -> "BasePromptTemplate":
"""Partially format the prompt."""
    fromllama_index.core.bridge.langchainimport (
        ConditionalPromptSelector as LangchainSelector,
    )

    mapped_kwargs = self._map_all_vars(kwargs)
    default_prompt = self.selector.default_prompt.partial(**mapped_kwargs)
    conditionals = [
        (condition, prompt.partial(**mapped_kwargs))
        for condition, prompt in self.selector.conditionals
    ]
    lc_selector = LangchainSelector(
        default_prompt=default_prompt, conditionals=conditionals
    )

    # copy full prompt object, replace selector
    lc_prompt = deepcopy(self)
    lc_prompt.selector = lc_selector
    return lc_prompt

```
 |  
| --- | --- |  
###  format [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.LangchainPromptTemplate.format "Permanent link")

```
format(llm: Optional[BaseLLM] = None, **kwargs: ) -> 

```

Format the prompt into a string.
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
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
```
 | 
```
defformat(self, llm: Optional[BaseLLM] = None, **kwargs: Any) -> str:
"""Format the prompt into a string."""
    fromllama_index.llms.langchainimport LangChainLLM  # pants: no-infer-dep

    if llm is not None:
        # if llamaindex LLM is provided, and we require a langchain LLM,
        # then error. but otherwise if `requires_langchain_llm` is False,
        # then we can just use the default prompt
        if not isinstance(llm, LangChainLLM) and self.requires_langchain_llm:
            raise ValueError("Must provide a LangChainLLM.")
        elif not isinstance(llm, LangChainLLM):
            lc_template = self.selector.default_prompt
        else:
            lc_template = self.selector.get_prompt(llm=llm.llm)
    else:
        lc_template = self.selector.default_prompt

    # if there's mappings specified, make sure those are used
    mapped_kwargs = self._map_all_vars(kwargs)
    return lc_template.format(**mapped_kwargs)

```
 |  
| --- | --- |  
###  format_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.LangchainPromptTemplate.format_messages "Permanent link")

```
format_messages(
    llm: Optional[BaseLLM] = None, **kwargs: 
) -> []

```

Format the prompt into a list of chat messages.
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
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
```
 | 
```
defformat_messages(
    self, llm: Optional[BaseLLM] = None, **kwargs: Any
) -> List[ChatMessage]:
"""Format the prompt into a list of chat messages."""
    fromllama_index.llms.langchainimport LangChainLLM  # pants: no-infer-dep
    fromllama_index.llms.langchain.utilsimport (
        from_lc_messages,
    )  # pants: no-infer-dep

    if llm is not None:
        # if llamaindex LLM is provided, and we require a langchain LLM,
        # then error. but otherwise if `requires_langchain_llm` is False,
        # then we can just use the default prompt
        if not isinstance(llm, LangChainLLM) and self.requires_langchain_llm:
            raise ValueError("Must provide a LangChainLLM.")
        elif not isinstance(llm, LangChainLLM):
            lc_template = self.selector.default_prompt
        else:
            lc_template = self.selector.get_prompt(llm=llm.llm)
    else:
        lc_template = self.selector.default_prompt

    # if there's mappings specified, make sure those are used
    mapped_kwargs = self._map_all_vars(kwargs)
    lc_prompt_value = lc_template.format_prompt(**mapped_kwargs)
    lc_messages = lc_prompt_value.to_messages()
    return from_lc_messages(lc_messages)

```
 |  
| --- | --- |  
##  PromptTemplate [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.PromptTemplate "Permanent link")
Bases: 
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `template`  |  _required_  |  
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
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
```
 | 
```
classPromptTemplate(BasePromptTemplate):  # type: ignore[no-redef]
    template: str

    def__init__(
        self,
        template: str,
        prompt_type: str = PromptType.CUSTOM,
        output_parser: Optional[BaseOutputParser] = None,
        metadata: Optional[Dict[str, Any]] = None,
        template_var_mappings: Optional[Dict[str, Any]] = None,
        function_mappings: Optional[Dict[str, Callable]] = None,
        **kwargs: Any,
    ) -> None:
        if metadata is None:
            metadata = {}
        metadata["prompt_type"] = prompt_type

        template_vars = get_template_vars(template)

        super().__init__(
            template=template,
            template_vars=template_vars,
            kwargs=kwargs,
            metadata=metadata,
            output_parser=output_parser,
            template_var_mappings=template_var_mappings,
            function_mappings=function_mappings,
        )

    defpartial_format(self, **kwargs: Any) -> "PromptTemplate":
"""Partially format the prompt."""
        # NOTE: this is a hack to get around deepcopy failing on output parser
        output_parser = self.output_parser
        self.output_parser = None

        # get function and fixed kwargs, and add that to a copy
        # of the current prompt object
        prompt = deepcopy(self)
        prompt.kwargs.update(kwargs)

        # NOTE: put the output parser back
        prompt.output_parser = output_parser
        self.output_parser = output_parser
        return prompt

    defformat(
        self,
        llm: Optional[BaseLLM] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        **kwargs: Any,
    ) -> str:
"""Format the prompt into a string."""
        del llm  # unused
        all_kwargs = {
            **self.kwargs,
            **kwargs,
        }

        mapped_all_kwargs = self._map_all_vars(all_kwargs)
        prompt = format_string(self.template, **mapped_all_kwargs)

        if self.output_parser is not None:
            prompt = self.output_parser.format(prompt)

        if completion_to_prompt is not None:
            prompt = completion_to_prompt(prompt)

        return prompt

    defformat_messages(
        self, llm: Optional[BaseLLM] = None, **kwargs: Any
    ) -> List[ChatMessage]:
"""Format the prompt into a list of chat messages."""
        del llm  # unused
        prompt = self.format(**kwargs)
        return prompt_to_messages(prompt)

    defget_template(self, llm: Optional[BaseLLM] = None) -> str:
        return self.template

```
 |  
| --- | --- |  
###  partial_format [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.PromptTemplate.partial_format "Permanent link")

```
partial_format(**kwargs: ) -> 

```

Partially format the prompt.
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
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
```
 | 
```
defpartial_format(self, **kwargs: Any) -> "PromptTemplate":
"""Partially format the prompt."""
    # NOTE: this is a hack to get around deepcopy failing on output parser
    output_parser = self.output_parser
    self.output_parser = None

    # get function and fixed kwargs, and add that to a copy
    # of the current prompt object
    prompt = deepcopy(self)
    prompt.kwargs.update(kwargs)

    # NOTE: put the output parser back
    prompt.output_parser = output_parser
    self.output_parser = output_parser
    return prompt

```
 |  
| --- | --- |  
###  format [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.PromptTemplate.format "Permanent link")

```
format(
    llm: Optional[BaseLLM] = None,
    completion_to_prompt: Optional[
        Callable[[], ]
    ] = None,
    **kwargs: 
) -> 

```

Format the prompt into a string.
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
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
```
 | 
```
defformat(
    self,
    llm: Optional[BaseLLM] = None,
    completion_to_prompt: Optional[Callable[[str], str]] = None,
    **kwargs: Any,
) -> str:
"""Format the prompt into a string."""
    del llm  # unused
    all_kwargs = {
        **self.kwargs,
        **kwargs,
    }

    mapped_all_kwargs = self._map_all_vars(all_kwargs)
    prompt = format_string(self.template, **mapped_all_kwargs)

    if self.output_parser is not None:
        prompt = self.output_parser.format(prompt)

    if completion_to_prompt is not None:
        prompt = completion_to_prompt(prompt)

    return prompt

```
 |  
| --- | --- |  
###  format_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.PromptTemplate.format_messages "Permanent link")

```
format_messages(
    llm: Optional[BaseLLM] = None, **kwargs: 
) -> []

```

Format the prompt into a list of chat messages.
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
204
205
206
207
208
209
210
```
 | 
```
defformat_messages(
    self, llm: Optional[BaseLLM] = None, **kwargs: Any
) -> List[ChatMessage]:
"""Format the prompt into a list of chat messages."""
    del llm  # unused
    prompt = self.format(**kwargs)
    return prompt_to_messages(prompt)

```
 |  
| --- | --- |  
##  PromptType [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.PromptType "Permanent link")
Bases: `str`, `Enum`
Prompt type.
Source code in `llama-index-core/llama_index/core/prompts/prompt_type.py`  
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
```
 | 
```
classPromptType(str, Enum):
"""Prompt type."""

    # summarization
    SUMMARY = "summary"
    # tree insert node
    TREE_INSERT = "insert"
    # tree select query prompt
    TREE_SELECT = "tree_select"
    # tree select query prompt (multiple)
    TREE_SELECT_MULTIPLE = "tree_select_multiple"
    # question-answer
    QUESTION_ANSWER = "text_qa"
    # refine
    REFINE = "refine"
    # keyword extract
    KEYWORD_EXTRACT = "keyword_extract"
    # query keyword extract
    QUERY_KEYWORD_EXTRACT = "query_keyword_extract"

    # schema extract
    SCHEMA_EXTRACT = "schema_extract"

    # text to sql
    TEXT_TO_SQL = "text_to_sql"

    # text to graph query
    TEXT_TO_GRAPH_QUERY = "text_to_graph_query"

    # table context
    TABLE_CONTEXT = "table_context"

    # KG extraction prompt
    KNOWLEDGE_TRIPLET_EXTRACT = "knowledge_triplet_extract"

    # Simple Input prompt
    SIMPLE_INPUT = "simple_input"

    # Pandas prompt
    PANDAS = "pandas"

    # JSON path prompt
    JSON_PATH = "json_path"

    # Single select prompt
    SINGLE_SELECT = "single_select"

    # Multiple select prompt
    MULTI_SELECT = "multi_select"

    VECTOR_STORE_QUERY = "vector_store_query"

    # Sub question prompt
    SUB_QUESTION = "sub_question"

    # SQL response synthesis prompt
    SQL_RESPONSE_SYNTHESIS = "sql_response_synthesis"

    # SQL response synthesis prompt (v2)
    SQL_RESPONSE_SYNTHESIS_V2 = "sql_response_synthesis_v2"

    # Conversation
    CONVERSATION = "conversation"

    # Decompose query transform
    DECOMPOSE = "decompose"

    # Choice select
    CHOICE_SELECT = "choice_select"

    # custom (by default)
    CUSTOM = "custom"

    # RankGPT rerank
    RANKGPT_RERANK = "rankgpt_rerank"

```
 |  
| --- | --- |  
##  SelectorPromptTemplate [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.SelectorPromptTemplate "Permanent link")
Bases: 
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `default_template`  |   |  _required_  |  
|  `conditionals`  |  `Sequence[Tuple[Callable[list, bool], BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.base.BasePromptTemplate\)")]] | None`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
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
```
 | 
```
classSelectorPromptTemplate(BasePromptTemplate):  # type: ignore[no-redef]
    default_template: SerializeAsAny[BasePromptTemplate]
    conditionals: Optional[
        Sequence[Tuple[Callable[[BaseLLM], bool], BasePromptTemplate]]
    ] = None

    def__init__(
        self,
        default_template: BasePromptTemplate,
        conditionals: Optional[
            Sequence[Tuple[Callable[[BaseLLM], bool], BasePromptTemplate]]
        ] = None,
    ):
        metadata = default_template.metadata
        kwargs = default_template.kwargs
        template_vars = default_template.template_vars
        output_parser = default_template.output_parser
        super().__init__(
            default_template=default_template,
            conditionals=conditionals,
            metadata=metadata,
            kwargs=kwargs,
            template_vars=template_vars,
            output_parser=output_parser,
        )

    defselect(self, llm: Optional[BaseLLM] = None) -> BasePromptTemplate:
        # ensure output parser is up to date
        self.default_template.output_parser = self.output_parser

        if llm is None:
            return self.default_template

        if self.conditionals is not None:
            for condition, prompt in self.conditionals:
                if condition(llm):
                    # ensure output parser is up to date
                    prompt.output_parser = self.output_parser
                    return prompt

        return self.default_template

    defpartial_format(self, **kwargs: Any) -> "SelectorPromptTemplate":
        default_template = self.default_template.partial_format(**kwargs)
        if self.conditionals is None:
            conditionals = None
        else:
            conditionals = [
                (condition, prompt.partial_format(**kwargs))
                for condition, prompt in self.conditionals
            ]
        return SelectorPromptTemplate(
            default_template=default_template, conditionals=conditionals
        )

    defformat(self, llm: Optional[BaseLLM] = None, **kwargs: Any) -> str:
"""Format the prompt into a string."""
        prompt = self.select(llm=llm)
        return prompt.format(**kwargs)

    defformat_messages(
        self, llm: Optional[BaseLLM] = None, **kwargs: Any
    ) -> List[ChatMessage]:
"""Format the prompt into a list of chat messages."""
        prompt = self.select(llm=llm)
        return prompt.format_messages(**kwargs)

    defget_template(self, llm: Optional[BaseLLM] = None) -> str:
        prompt = self.select(llm=llm)
        return prompt.get_template(llm=llm)

```
 |  
| --- | --- |  
###  format [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.SelectorPromptTemplate.format "Permanent link")

```
format(llm: Optional[BaseLLM] = None, **kwargs: ) -> 

```

Format the prompt into a string.
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
369
370
371
372
```
 | 
```
defformat(self, llm: Optional[BaseLLM] = None, **kwargs: Any) -> str:
"""Format the prompt into a string."""
    prompt = self.select(llm=llm)
    return prompt.format(**kwargs)

```
 |  
| --- | --- |  
###  format_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.SelectorPromptTemplate.format_messages "Permanent link")

```
format_messages(
    llm: Optional[BaseLLM] = None, **kwargs: 
) -> []

```

Format the prompt into a list of chat messages.
Source code in `llama-index-core/llama_index/core/prompts/base.py`  
| 
```
374
375
376
377
378
379
```
 | 
```
defformat_messages(
    self, llm: Optional[BaseLLM] = None, **kwargs: Any
) -> List[ChatMessage]:
"""Format the prompt into a list of chat messages."""
    prompt = self.select(llm=llm)
    return prompt.format_messages(**kwargs)

```
 |  
| --- | --- |  
##  RichPromptTemplate [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.RichPromptTemplate "Permanent link")
Bases: 
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `template_str`  |  The template string for the prompt.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/prompts/rich.py`  
| 
```
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
```
 | 
```
classRichPromptTemplate(BasePromptTemplate):  # type: ignore[no-redef]
    template_str: str = Field(description="The template string for the prompt.")

    def__init__(
        self,
        template_str: str,
        metadata: Optional[Dict[str, Any]] = None,
        output_parser: Optional[BaseOutputParser] = None,
        template_vars: Optional[List[str]] = None,
        template_var_mappings: Optional[Dict[str, Any]] = None,
        function_mappings: Optional[Dict[str, Callable]] = None,
        **kwargs: Any,
    ):
        template_vars = template_vars or []
        if not template_vars:
            template_vars = Prompt(template_str).variables

        super().__init__(
            template_str=template_str,
            kwargs=kwargs or {},
            metadata=metadata or {},
            output_parser=output_parser,
            template_vars=template_vars,
            template_var_mappings=template_var_mappings,
            function_mappings=function_mappings,
        )

    @property
    defis_chat_template(self) -> bool:
        return "endchat" in self.template_str

    defpartial_format(self, **kwargs: Any) -> "RichPromptTemplate":
        prompt = deepcopy(self)
        prompt.kwargs.update(kwargs)
        return prompt

    defformat(
        self,
        llm: Optional[BaseLLM] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        **kwargs: Any,
    ) -> str:
        del llm  # unused

        if self.is_chat_template:
            messages = self.format_messages(**kwargs)

            if messages_to_prompt is not None:
                return messages_to_prompt(messages)

            return default_messages_to_prompt(messages)
        else:
            all_kwargs = {
                **self.kwargs,
                **kwargs,
            }
            mapped_all_kwargs = self._map_all_vars(all_kwargs)
            return Prompt(self.template_str).text(data=mapped_all_kwargs)

    defformat_messages(
        self, llm: Optional[BaseLLM] = None, **kwargs: Any
    ) -> List[ChatMessage]:
        del llm  # unused
"""Format the prompt into a list of chat messages."""
        all_kwargs = {
            **self.kwargs,
            **kwargs,
        }
        mapped_all_kwargs = self._map_all_vars(all_kwargs)

        banks_prompt = Prompt(self.template_str)
        banks_messages = banks_prompt.chat_messages(data=mapped_all_kwargs)

        llama_messages: list[ChatMessage] = []
        for bank_message in banks_messages:
            if isinstance(bank_message.content, str):
                llama_messages.append(
                    ChatMessage(role=bank_message.role, content=bank_message.content)
                )
            elif isinstance(bank_message.content, list):
                llama_blocks: list[ContentBlock] = []
                for bank_block in bank_message.content:
                    if bank_block.type == BanksContentBlockType.text:
                        llama_blocks.append(TextBlock(text=bank_block.text))
                    elif bank_block.type == BanksContentBlockType.image_url:
                        llama_blocks.append(ImageBlock(url=bank_block.image_url.url))
                    elif bank_block.type == BanksContentBlockType.audio:
                        llama_blocks.append(AudioBlock(url=bank_block.input_audio.data))
                    elif bank_block.type == BanksContentBlockType.video:
                        llama_blocks.append(VideoBlock(url=bank_block.input_video.data))
                    elif bank_block.type == BanksContentBlockType.document:
                        llama_blocks.append(
                            DocumentBlock(url=bank_block.input_document.data)
                        )
                    else:
                        raise ValueError(
                            f"Unsupported content block type: {bank_block.type}"
                        )

                llama_messages.append(
                    ChatMessage(role=bank_message.role, content=llama_blocks)
                )
            else:
                raise ValueError(
                    f"Unsupported message content type: {type(bank_message.content)}"
                )

        if self.output_parser is not None:
            llama_messages = self.output_parser.format_messages(llama_messages)

        return llama_messages

    defget_template(self, llm: Optional[BaseLLM] = None) -> str:
        return self.template_str

```
 |  
| --- | --- |  
##  display_prompt_dict [#](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.display_prompt_dict "Permanent link")

```
display_prompt_dict(prompts_dict: PromptDictType) -> None

```

Display prompt dict.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompts_dict`  |  `PromptDictType`  |  prompt dict  |  _required_  |  
Source code in `llama-index-core/llama_index/core/prompts/display_utils.py`  
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
```
 | 
```
defdisplay_prompt_dict(prompts_dict: PromptDictType) -> None:
"""
    Display prompt dict.

    Args:
        prompts_dict: prompt dict

    """
    fromIPython.displayimport Markdown, display

    for k, p in prompts_dict.items():
        text_md = f"**Prompt Key**: {k}<br>**Text:** <br>"
        display(Markdown(text_md))
        print(p.get_template())
        display(Markdown("<br><br>"))

```
 |  
| --- | --- |
