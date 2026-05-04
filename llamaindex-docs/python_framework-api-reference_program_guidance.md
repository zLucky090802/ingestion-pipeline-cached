# Guidance
##  GuidancePydanticProgram [#](https://developers.llamaindex.ai/python/framework-api-reference/program/guidance/#llama_index.program.guidance.GuidancePydanticProgram "Permanent link")
Bases: `BaseLLMFunctionProgram['GuidanceLLM']`
A guidance-based function that returns a pydantic model.
Note: this interface is not yet stable.
Source code in `llama-index-integrations/program/llama-index-program-guidance/llama_index/program/guidance/base.py`  
| 
```
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
```
 | 
```
classGuidancePydanticProgram(BaseLLMFunctionProgram["GuidanceLLM"]):
"""
    A guidance-based function that returns a pydantic model.

    Note: this interface is not yet stable.
    """

    def__init__(
        self,
        output_cls: Type[BaseModel],
        prompt_template_str: str,
        guidance_llm: Optional["GuidanceLLM"] = None,
        verbose: bool = False,
    ):
        if not guidance_llm:
            llm = guidance_llm
        else:
            llm = OpenAI("gpt-3.5-turbo")

        full_str = prompt_template_str + "\n"
        self._full_str = full_str
        self._guidance_program = partial(self.program, llm=llm, silent=not verbose)
        self._output_cls = output_cls
        self._verbose = verbose

    defprogram(
        self,
        llm: "GuidanceLLM",
        silent: bool,
        tools_str: str,
        query_str: str,
        **kwargs: dict,
    ) -> "GuidanceLLM":
"""A wrapper to execute the program with new guidance version."""
        given_query = self._full_str.replace("{{tools_str}}", tools_str).replace(
            "{{query_str}}", query_str
        )
        with user():
            llm = llm + given_query

        with assistant():
            llm = llm + gen(stop=".")

        return llm  # noqa: RET504

    @classmethod
    deffrom_defaults(
        cls,
        output_cls: Type[BaseModel],
        prompt_template_str: Optional[str] = None,
        prompt: Optional[PromptTemplate] = None,
        llm: Optional["GuidanceLLM"] = None,
        **kwargs: Any,
    ) -> "BaseLLMFunctionProgram":
"""From defaults."""
        if prompt is None and prompt_template_str is None:
            raise ValueError("Must provide either prompt or prompt_template_str.")
        if prompt is not None and prompt_template_str is not None:
            raise ValueError("Must provide either prompt or prompt_template_str.")
        if prompt is not None:
            prompt_template_str = prompt.template
        prompt_template_str = cast(str, prompt_template_str)
        return cls(
            output_cls,
            prompt_template_str,
            guidance_llm=llm,
            **kwargs,
        )

    @property
    defoutput_cls(self) -> Type[BaseModel]:
        return self._output_cls

    def__call__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> BaseModel:
        executed_program = self._guidance_program(**kwargs)
        response = str(executed_program)

        return parse_pydantic_from_guidance_program(
            response=response, cls=self._output_cls
        )

```
 |  
| --- | --- |  
###  program [#](https://developers.llamaindex.ai/python/framework-api-reference/program/guidance/#llama_index.program.guidance.GuidancePydanticProgram.program "Permanent link")

```
program(
    llm: Model,
    silent: ,
    tools_str: ,
    query_str: ,
    **kwargs: 
) -> Model

```

A wrapper to execute the program with new guidance version.
Source code in `llama-index-integrations/program/llama-index-program-guidance/llama_index/program/guidance/base.py`  
| 
```
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
```
 | 
```
defprogram(
    self,
    llm: "GuidanceLLM",
    silent: bool,
    tools_str: str,
    query_str: str,
    **kwargs: dict,
) -> "GuidanceLLM":
"""A wrapper to execute the program with new guidance version."""
    given_query = self._full_str.replace("{{tools_str}}", tools_str).replace(
        "{{query_str}}", query_str
    )
    with user():
        llm = llm + given_query

    with assistant():
        llm = llm + gen(stop=".")

    return llm  # noqa: RET504

```
 |  
| --- | --- |  
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/program/guidance/#llama_index.program.guidance.GuidancePydanticProgram.from_defaults "Permanent link")

```
from_defaults(
    output_cls: [BaseModel],
    prompt_template_str: Optional[] = None,
    prompt: Optional[] = None,
    llm: Optional[Model] = None,
    **kwargs: 
) -> BaseLLMFunctionProgram

```

From defaults.
Source code in `llama-index-integrations/program/llama-index-program-guidance/llama_index/program/guidance/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    output_cls: Type[BaseModel],
    prompt_template_str: Optional[str] = None,
    prompt: Optional[PromptTemplate] = None,
    llm: Optional["GuidanceLLM"] = None,
    **kwargs: Any,
) -> "BaseLLMFunctionProgram":
"""From defaults."""
    if prompt is None and prompt_template_str is None:
        raise ValueError("Must provide either prompt or prompt_template_str.")
    if prompt is not None and prompt_template_str is not None:
        raise ValueError("Must provide either prompt or prompt_template_str.")
    if prompt is not None:
        prompt_template_str = prompt.template
    prompt_template_str = cast(str, prompt_template_str)
    return cls(
        output_cls,
        prompt_template_str,
        guidance_llm=llm,
        **kwargs,
    )

```
 |  
| --- | --- |  
options: members: - GuidancePydanticProgram
