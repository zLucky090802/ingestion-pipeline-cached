# Llm text completion
##  LLMTextCompletionProgram [#](https://developers.llamaindex.ai/python/framework-api-reference/program/llm_text_completion/#llama_index.core.program.llm_program.LLMTextCompletionProgram "Permanent link")
Bases: `BasePydanticProgram[](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/#llama_index.core.types.BasePydanticProgram "BasePydanticProgram \(llama_index.core.types.BasePydanticProgram\)")[Model]`
LLM Text Completion Program.
Uses generic LLM text completion + an output parser to generate a structured output.
Source code in `llama-index-core/llama_index/core/program/llm_program.py`  
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
```
 | 
```
classLLMTextCompletionProgram(BasePydanticProgram[Model]):
"""
    LLM Text Completion Program.

    Uses generic LLM text completion + an output parser to generate a structured output.

    """

    def__init__(
        self,
        output_parser: BaseOutputParser,
        output_cls: Type[Model],
        prompt: BasePromptTemplate,
        llm: LLM,
        verbose: bool = False,
    ) -> None:
        self._output_parser = output_parser
        self._output_cls = output_cls
        self._llm = llm
        self._prompt = prompt
        self._verbose = verbose

        self._prompt.output_parser = output_parser

    @classmethod
    deffrom_defaults(
        cls,
        output_parser: Optional[BaseOutputParser] = None,
        output_cls: Optional[Type[Model]] = None,
        prompt_template_str: Optional[str] = None,
        prompt: Optional[BasePromptTemplate] = None,
        llm: Optional[LLM] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> "LLMTextCompletionProgram[Model]":
        llm = llm or Settings.llm
        if prompt is None and prompt_template_str is None:
            raise ValueError("Must provide either prompt or prompt_template_str.")
        if prompt is not None and prompt_template_str is not None:
            raise ValueError("Must provide either prompt or prompt_template_str.")
        if prompt_template_str is not None:
            prompt = PromptTemplate(prompt_template_str)

        # decide default output class if not set
        if output_cls is None:
            if not isinstance(output_parser, PydanticOutputParser):
                raise ValueError("Output parser must be PydanticOutputParser.")
            output_cls = output_parser.output_cls
        else:
            if output_parser is None:
                output_parser = PydanticOutputParser(output_cls=output_cls)

        return cls(
            output_parser,
            output_cls,
            prompt=cast(PromptTemplate, prompt),
            llm=llm,
            verbose=verbose,
        )

    @property
    defoutput_cls(self) -> Type[Model]:
        return self._output_cls

    @property
    defprompt(self) -> BasePromptTemplate:
        return self._prompt

    @prompt.setter
    defprompt(self, prompt: BasePromptTemplate) -> None:
        self._prompt = prompt

    def__call__(
        self,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Model:
        llm_kwargs = llm_kwargs or {}
        if self._llm.metadata.is_chat_model:
            messages = self._prompt.format_messages(llm=self._llm, **kwargs)
            messages = self._llm._extend_messages(messages)
            chat_response = self._llm.chat(messages, **llm_kwargs)

            raw_output = chat_response.message.content or ""
        else:
            formatted_prompt = self._prompt.format(llm=self._llm, **kwargs)

            response = self._llm.complete(formatted_prompt, **llm_kwargs)

            raw_output = response.text

        output = self._output_parser.parse(raw_output)
        if not isinstance(output, self._output_cls):
            raise ValueError(
                f"Output parser returned {type(output)} but expected {self._output_cls}"
            )
        return output

    async defacall(
        self,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Model:
        llm_kwargs = llm_kwargs or {}
        if self._llm.metadata.is_chat_model:
            messages = self._prompt.format_messages(llm=self._llm, **kwargs)
            messages = self._llm._extend_messages(messages)
            chat_response = await self._llm.achat(messages, **llm_kwargs)

            raw_output = chat_response.message.content or ""
        else:
            formatted_prompt = self._prompt.format(llm=self._llm, **kwargs)

            response = await self._llm.acomplete(formatted_prompt, **llm_kwargs)

            raw_output = response.text

        output = self._output_parser.parse(raw_output)
        if not isinstance(output, self._output_cls):
            raise ValueError(
                f"Output parser returned {type(output)} but expected {self._output_cls}"
            )
        return output

```
 |  
| --- | --- |  
options: members: - LLMTextCompletionProgram
