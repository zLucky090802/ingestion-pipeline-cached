# Lmformatenforcer
##  LMFormatEnforcerPydanticProgram [#](https://developers.llamaindex.ai/python/framework-api-reference/program/lmformatenforcer/#llama_index.program.lmformatenforcer.LMFormatEnforcerPydanticProgram "Permanent link")
Bases: `BaseLLMFunctionProgram`
A lm-format-enforcer-based function that returns a pydantic model.
In LMFormatEnforcerPydanticProgram, prompt_template_str can also have a {json_schema} parameter that will be automatically filled by the json_schema of output_cls. Note: this interface is not yet stable.
Source code in `llama-index-integrations/program/llama-index-program-lmformatenforcer/llama_index/program/lmformatenforcer/base.py`  
| 
```
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
```
 | 
```
classLMFormatEnforcerPydanticProgram(BaseLLMFunctionProgram):
"""
    A lm-format-enforcer-based function that returns a pydantic model.

    In LMFormatEnforcerPydanticProgram, prompt_template_str can also have a {json_schema} parameter
    that will be automatically filled by the json_schema of output_cls.
    Note: this interface is not yet stable.
    """

    def__init__(
        self,
        output_cls: Type[BaseModel],
        prompt_template_str: str,
        llm: Optional[Union[LlamaCPP, HuggingFaceLLM]] = None,
        verbose: bool = False,
    ):
        try:
            importlmformatenforcer
        except ImportError as e:
            raise ImportError(
                "lm-format-enforcer package not found."
                "please run `pip install lm-format-enforcer`"
            ) frome

        if llm is None:
            try:
                fromllama_index.core.llmsimport LlamaCPP

                llm = LlamaCPP()
            except ImportError as e:
                raise ImportError(
                    "llama.cpp package not found."
                    "please run `pip install llama-cpp-python`"
                ) frome

        self.llm = llm

        self._prompt_template_str = prompt_template_str
        self._output_cls = output_cls
        self._verbose = verbose
        json_schema_parser = lmformatenforcer.JsonSchemaParser(self.output_cls.schema())
        self._token_enforcer_fn = build_lm_format_enforcer_function(
            self.llm, json_schema_parser
        )

    @classmethod
    deffrom_defaults(
        cls,
        output_cls: Type[BaseModel],
        prompt_template_str: Optional[str] = None,
        prompt: Optional[PromptTemplate] = None,
        llm: Optional[Union["LlamaCPP", "HuggingFaceLLM"]] = None,
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
            llm=llm,
            **kwargs,
        )

    @property
    defoutput_cls(self) -> Type[BaseModel]:
        return self._output_cls

    def__call__(
        self,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> BaseModel:
        llm_kwargs = llm_kwargs or {}
        # While the format enforcer is active, any calls to the llm will have the format enforced.
        with activate_lm_format_enforcer(self.llm, self._token_enforcer_fn):
            json_schema_str = json.dumps(self.output_cls.schema())
            full_str = self._prompt_template_str.format(
                *args, **kwargs, json_schema=json_schema_str
            )
            output = self.llm.complete(full_str, **llm_kwargs)
            text = output.text
            return self.output_cls.parse_raw(text)

```
 |  
| --- | --- |  
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/program/lmformatenforcer/#llama_index.program.lmformatenforcer.LMFormatEnforcerPydanticProgram.from_defaults "Permanent link")

```
from_defaults(
    output_cls: [BaseModel],
    prompt_template_str: Optional[] = None,
    prompt: Optional[] = None,
    llm: Optional[Union[, ]] = None,
    **kwargs: 
) -> BaseLLMFunctionProgram

```

From defaults.
Source code in `llama-index-integrations/program/llama-index-program-lmformatenforcer/llama_index/program/lmformatenforcer/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    output_cls: Type[BaseModel],
    prompt_template_str: Optional[str] = None,
    prompt: Optional[PromptTemplate] = None,
    llm: Optional[Union["LlamaCPP", "HuggingFaceLLM"]] = None,
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
        llm=llm,
        **kwargs,
    )

```
 |  
| --- | --- |  
options: members: - LMFormatEnforcerPydanticProgram
