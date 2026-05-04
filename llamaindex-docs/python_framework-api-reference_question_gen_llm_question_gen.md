# Llm question gen
##  LLMQuestionGenerator [#](https://developers.llamaindex.ai/python/framework-api-reference/question_gen/llm_question_gen/#llama_index.core.question_gen.LLMQuestionGenerator "Permanent link")
Bases: 
Source code in `llama-index-core/llama_index/core/question_gen/llm_generators.py`  
| 
```
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
```
 | 
```
classLLMQuestionGenerator(BaseQuestionGenerator):
    def__init__(
        self,
        llm: LLM,
        prompt: BasePromptTemplate,
    ) -> None:
        self._llm = llm
        self._prompt = prompt

        if self._prompt.output_parser is None:
            raise ValueError("Prompt should have output parser.")

    @classmethod
    deffrom_defaults(
        cls,
        llm: Optional[LLM] = None,
        prompt_template_str: Optional[str] = None,
        output_parser: Optional[BaseOutputParser] = None,
    ) -> "LLMQuestionGenerator":
        # optionally initialize defaults
        llm = llm or Settings.llm
        prompt_template_str = prompt_template_str or DEFAULT_SUB_QUESTION_PROMPT_TMPL
        output_parser = output_parser or SubQuestionOutputParser()

        # construct prompt
        prompt = PromptTemplate(
            template=prompt_template_str,
            output_parser=output_parser,
            prompt_type=PromptType.SUB_QUESTION,
        )
        return cls(llm, prompt)

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {"question_gen_prompt": self._prompt}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "question_gen_prompt" in prompts:
            output_parser = prompts["question_gen_prompt"].output_parser
            if output_parser is None:
                output_parser = SubQuestionOutputParser()
            self._prompt = PromptTemplate(
                prompts["question_gen_prompt"].get_template(llm=self._llm),
                output_parser=output_parser,
            )

    defgenerate(
        self, tools: Sequence[ToolMetadata], query: QueryBundle
    ) -> List[SubQuestion]:
        tools_str = build_tools_text(tools)
        query_str = query.query_str
        prediction = self._llm.predict(
            prompt=self._prompt,
            tools_str=tools_str,
            query_str=query_str,
        )

        assert self._prompt.output_parser is not None
        parse = self._prompt.output_parser.parse(prediction)
        parse = cast(StructuredOutput, parse)
        return parse.parsed_output

    async defagenerate(
        self, tools: Sequence[ToolMetadata], query: QueryBundle
    ) -> List[SubQuestion]:
        tools_str = build_tools_text(tools)
        query_str = query.query_str
        prediction = await self._llm.apredict(
            prompt=self._prompt,
            tools_str=tools_str,
            query_str=query_str,
        )

        assert self._prompt.output_parser is not None
        parse = self._prompt.output_parser.parse(prediction)
        parse = cast(StructuredOutput, parse)
        return parse.parsed_output

```
 |  
| --- | --- |  
options: members: - LLMQuestionGenerator - SubQuestionOutputParser
