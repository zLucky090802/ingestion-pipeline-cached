# Guidance
##  GuidanceQuestionGenerator [#](https://developers.llamaindex.ai/python/framework-api-reference/question_gen/guidance/#llama_index.question_gen.guidance.GuidanceQuestionGenerator "Permanent link")
Bases: 
Source code in `llama-index-integrations/question_gen/llama-index-question-gen-guidance/llama_index/question_gen/guidance/base.py`  
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
```
 | 
```
classGuidanceQuestionGenerator(BaseQuestionGenerator):
    def__init__(
        self,
        program: GuidancePydanticProgram,
        verbose: bool = False,
    ) -> None:
        self._program = program
        self._verbose = verbose

    @classmethod
    deffrom_defaults(
        cls,
        prompt_template_str: str = DEFAULT_GUIDANCE_SUB_QUESTION_PROMPT_TMPL,
        guidance_llm: Optional["GuidanceLLM"] = None,
        verbose: bool = False,
    ) -> "GuidanceQuestionGenerator":
        program = GuidancePydanticProgram(
            output_cls=SubQuestionList,
            guidance_llm=guidance_llm,
            prompt_template_str=prompt_template_str,
            verbose=verbose,
        )

        return cls(program, verbose)

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""

    defgenerate(
        self, tools: Sequence[ToolMetadata], query: QueryBundle
    ) -> List[SubQuestion]:
        tools_str = build_tools_text(tools)
        query_str = query.query_str
        question_list = self._program(
            tools_str=tools_str,
            query_str=query_str,
        )
        question_list = cast(SubQuestionList, question_list)
        return question_list.items

    async defagenerate(
        self, tools: Sequence[ToolMetadata], query: QueryBundle
    ) -> List[SubQuestion]:
        # TODO: currently guidance does not support async calls
        return self.generate(tools=tools, query=query)

```
 |  
| --- | --- |  
options: members: - GuidanceQuestionGenerator
