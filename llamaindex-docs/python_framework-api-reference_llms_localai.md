# Localai
##  LocalAI [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/localai/#llama_index.llms.localai.LocalAI "Permanent link")
Bases: 
LocalAI LLM class.
Examples:
`pip install llama-index-llms-localai`

```
fromllama_index.llms.localaiimport LocalAI

llm = LocalAI(api_base="http://localhost:8080/v1")

response = llm.complete("Hello!")
print(str(response))

```

Source code in `llama-index-integrations/llms/llama-index-llms-localai/llama_index/llms/localai/base.py`  
| 
```
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
```
 | 
```
classLocalAI(OpenAI):
"""
    LocalAI LLM class.

    Examples:
        `pip install llama-index-llms-localai`

        ```python
        from llama_index.llms.localai import LocalAI

        llm = LocalAI(api_base="http://localhost:8080/v1")

        response = llm.complete("Hello!")
        print(str(response))
        ```

    """

    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description="The maximum number of context tokens for the model.",
        gt=0,
    )
    globally_use_chat_completions: Optional[bool] = Field(
        default=None,
        description=(
            "Set None (default) to per-invocation decide on using /chat/completions"
            " vs /completions endpoints with query keyword arguments,"
            " set False to universally use /completions endpoint,"
            " set True to universally use /chat/completions endpoint."
        ),
    )

    def__init__(
        self,
        api_key: Optional[str] = LOCALAI_DEFAULTS["api_key"],
        api_base: Optional[str] = LOCALAI_DEFAULTS["api_base"],
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            api_key=api_key,
            api_base=api_base,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
            **kwargs,
        )
        warnings.warn(
            (
                f"{type(self).__name__} subclass is deprecated in favor of"
                f" {OpenAILike.__name__} composition. The deprecation cycle"
                " will complete sometime in late December 2023."
            ),
            DeprecationWarning,
            stacklevel=2,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "LocalAI"

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.max_tokens or -1,
            is_chat_model=self._is_chat_model,
            is_function_calling_model=is_function_calling_model(
                model=self._get_model_name()
            ),
            model_name=self.model,
        )

    def_update_max_tokens(self, all_kwargs: Dict[str, Any], prompt: str) -> None:
        # This subclass only supports max_tokens via LocalAI(..., max_tokens=123)
        del all_kwargs, prompt  # Unused
        # do nothing

    @property
    def_is_chat_model(self) -> bool:
        if self.globally_use_chat_completions is not None:
            return self.globally_use_chat_completions
        raise NotImplementedError(
            "Inferring of when to use /chat/completions is unsupported by"
            f" {type(self).__name__}. Please either set 'globally_use_chat_completions'"
            " arg during construction, or pass the arg 'use_chat_completions' in your"
            " query, setting True for /chat/completions or False for /completions."
        )

```
 |  
| --- | --- |  
options: members: - LocalAI
