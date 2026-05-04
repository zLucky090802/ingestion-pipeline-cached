# Multi modal
##  MultiModalLLMCompletionProgram [#](https://developers.llamaindex.ai/python/framework-api-reference/program/multi_modal/#llama_index.core.program.multi_modal_llm_program.MultiModalLLMCompletionProgram "Permanent link")
Bases: `BasePydanticProgram[](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/#llama_index.core.types.BasePydanticProgram "BasePydanticProgram \(llama_index.core.types.BasePydanticProgram\)")[BaseModel]`
Multi Modal LLM Completion Program.
Uses generic Multi Modal LLM completion + an output parser to generate a structured output.
Source code in `llama-index-core/llama_index/core/program/multi_modal_llm_program.py`  
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
```
 | 
```
classMultiModalLLMCompletionProgram(BasePydanticProgram[BaseModel]):
"""
    Multi Modal LLM Completion Program.

    Uses generic Multi Modal LLM completion + an output parser to generate a structured output.

    """

    def__init__(
        self,
        output_parser: PydanticOutputParser,
        prompt: BasePromptTemplate,
        multi_modal_llm: LLM,
        image_documents: Optional[List[Union[ImageBlock, ImageNode]]] = None,
        verbose: bool = False,
    ) -> None:
        self._output_parser = output_parser
        self._multi_modal_llm = multi_modal_llm
        self._prompt = prompt
        if image_documents and all(
            isinstance(doc, ImageNode) for doc in image_documents
        ):
            image_docs: Optional[List[ImageBlock]] = [
                image_node_to_image_block(cast(ImageNode, doc))
                for doc in image_documents
            ]
        else:
            image_docs = cast(Optional[List[ImageBlock]], image_documents)
        self._image_documents = image_docs
        self._verbose = verbose

        self._prompt.output_parser = output_parser

    @classmethod
    deffrom_defaults(
        cls,
        output_parser: Optional[PydanticOutputParser] = None,
        output_cls: Optional[Type[BaseModel]] = None,
        prompt_template_str: Optional[str] = None,
        prompt: Optional[PromptTemplate] = None,
        multi_modal_llm: Optional[LLM] = None,
        image_documents: Optional[List[Union[ImageBlock, ImageNode]]] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> "MultiModalLLMCompletionProgram":
        if multi_modal_llm is None:
            try:
                fromllama_index.llms.openaiimport (
                    OpenAIResponses,
                )  # pants: no-infer-dep

                multi_modal_llm = OpenAIResponses(model="gpt-4.1", temperature=0)
            except ImportError as e:
                raise ImportError(
                    "`llama-index-llms-openai` package cannot be found. "
                    "Please install it by using `pip install `llama-index-llms-openai`"
                )
        if prompt is None and prompt_template_str is None:
            raise ValueError("Must provide either prompt or prompt_template_str.")
        if prompt is not None and prompt_template_str is not None:
            raise ValueError("Must provide either prompt or prompt_template_str.")
        if prompt_template_str is not None:
            prompt = PromptTemplate(prompt_template_str)

        if output_parser is None:
            if output_cls is None:
                raise ValueError("Must provide either output_cls or output_parser.")
            output_parser = PydanticOutputParser(output_cls=output_cls)

        return cls(
            output_parser,
            prompt=cast(PromptTemplate, prompt),
            multi_modal_llm=multi_modal_llm,
            image_documents=image_documents or [],
            verbose=verbose,
        )

    @property
    defoutput_cls(self) -> Type[BaseModel]:
        return self._output_parser.output_cls

    @property
    defprompt(self) -> BasePromptTemplate:
        return self._prompt

    @prompt.setter
    defprompt(self, prompt: BasePromptTemplate) -> None:
        self._prompt = prompt

    def__call__(
        self,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        image_documents: Optional[List[Union[ImageBlock, ImageNode]]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> BaseModel:
        llm_kwargs = llm_kwargs or {}
        formatted_prompt = self._prompt.format(llm=self._multi_modal_llm, **kwargs)  # type: ignore

        if image_documents and all(
            isinstance(doc, ImageNode) for doc in image_documents
        ):
            image_docs: Optional[List[ImageBlock]] = [
                image_node_to_image_block(cast(ImageNode, doc))
                for doc in image_documents
            ]
        else:
            image_docs = cast(Optional[List[ImageBlock]], image_documents)

        blocks: List[Union[ImageBlock, TextBlock]] = (
            cast(Optional[List[Union[ImageBlock, TextBlock]]], image_docs)
            or cast(Optional[List[Union[ImageBlock, TextBlock]]], self._image_documents)
            or []
        )

        blocks.append(TextBlock(text=formatted_prompt))

        response = self._multi_modal_llm.chat(
            messages=[ChatMessage(role="user", blocks=blocks)],
            **llm_kwargs,
        )

        raw_output: str = response.message.content or ""
        if self._verbose:
            print_text(f"> Raw output: {raw_output}\n", color="llama_blue")

        return self._output_parser.parse(raw_output)

    async defacall(
        self,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        image_documents: Optional[List[Union[ImageBlock, ImageNode]]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> BaseModel:
        llm_kwargs = llm_kwargs or {}
        formatted_prompt = self._prompt.format(llm=self._multi_modal_llm, **kwargs)  # type: ignore

        if image_documents and all(
            isinstance(doc, ImageNode) for doc in image_documents
        ):
            image_docs: Optional[List[ImageBlock]] = [
                image_node_to_image_block(cast(ImageNode, doc))
                for doc in image_documents
            ]
        else:
            image_docs = cast(Optional[List[ImageBlock]], image_documents)

        blocks: List[Union[ImageBlock, TextBlock]] = (
            cast(Optional[List[Union[ImageBlock, TextBlock]]], image_docs)
            or cast(Optional[List[Union[ImageBlock, TextBlock]]], self._image_documents)
            or []
        )

        blocks.append(TextBlock(text=formatted_prompt))

        response = await self._multi_modal_llm.achat(
            messages=[ChatMessage(role="user", blocks=blocks)],
            **llm_kwargs,
        )

        raw_output: str = response.message.content or ""
        if self._verbose:
            print_text(f"> Raw output: {raw_output}\n", color="llama_blue")

        return self._output_parser.parse(raw_output)

```
 |  
| --- | --- |  
options: members: - MultiModalLLMCompletionProgram
