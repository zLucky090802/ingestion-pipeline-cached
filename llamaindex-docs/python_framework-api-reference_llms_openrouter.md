# Openrouter
##  OpenRouter [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openrouter/#llama_index.llms.openrouter.OpenRouter "Permanent link")
Bases: 
OpenRouter LLM.
To instantiate the `OpenRouter` class, you will need to provide an API key. You can set the API key either as an environment variable `OPENROUTER_API_KEY` or directly in the class constructor. If setting it in the class constructor, it would look like this:
If you haven't signed up for an API key yet, you can do so on the OpenRouter website at (https://openrouter.ai). Once you have your API key, you can use the `OpenRouter` class to interact with the LLM for tasks like chatting, streaming, and completing prompts.
Examples:
`pip install llama-index-llms-openrouter`

```
fromllama_index.llms.openrouterimport OpenRouter

llm = OpenRouter(
    api_key="<your-api-key>",
    max_tokens=256,
    context_window=4096,
    model="gryphe/mythomax-l2-13b",
)

response = llm.complete("Hello World!")
print(str(response))

```

Source code in `llama-index-integrations/llms/llama-index-llms-openrouter/llama_index/llms/openrouter/base.py`  
| 
```
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
```
 | 
```
classOpenRouter(OpenAILike):
"""
    OpenRouter LLM.

    To instantiate the `OpenRouter` class, you will need to provide an API key. You can set the API key either as an environment variable `OPENROUTER_API_KEY` or directly in the class
    constructor. If setting it in the class constructor, it would look like this:

    If you haven't signed up for an API key yet, you can do so on the OpenRouter website at (https://openrouter.ai). Once you have your API key, you can use the `OpenRouter` class to interact
    with the LLM for tasks like chatting, streaming, and completing prompts.

    Examples:
        `pip install llama-index-llms-openrouter`

        ```python
        from llama_index.llms.openrouter import OpenRouter

        llm = OpenRouter(
            api_key="<your-api-key>",
            max_tokens=256,
            context_window=4096,
            model="gryphe/mythomax-l2-13b",


        response = llm.complete("Hello World!")
        print(str(response))
        ```

    """

    model: str = Field(
        description="The OpenRouter model to use. See https://openrouter.ai/models for options."
    )
    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description="The maximum number of context tokens for the model. See https://openrouter.ai/models for options.",
        gt=0,
    )
    is_chat_model: bool = Field(
        default=True,
        description=LLMMetadata.model_fields["is_chat_model"].description,
    )

    def__init__(
        self,
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_NUM_OUTPUTS,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        max_retries: int = 5,
        api_base: Optional[str] = DEFAULT_API_BASE,
        api_key: Optional[str] = None,
        order: Optional[List[str]] = None,
        allow_fallbacks: Optional[bool] = None,
        **kwargs: Any,
    ) -> None:
        additional_kwargs = additional_kwargs or {}

        if order is not None or allow_fallbacks is not None:
            provider_settings: Dict[str, Any] = {}
            if order is not None:
                provider_settings["order"] = order
            if allow_fallbacks is not None:
                provider_settings["allow_fallbacks"] = allow_fallbacks

            extra_body = additional_kwargs.get("extra_body")
            if extra_body is None:
                extra_body = {}
                additional_kwargs["extra_body"] = extra_body

            existing_provider = extra_body.get("provider")
            if existing_provider is None:
                existing_provider = {}
            elif not isinstance(existing_provider, dict):
                raise ValueError(
                    "additional_kwargs['extra_body']['provider'] must be a dict if provided."
                )

            extra_body["provider"] = {**existing_provider, **provider_settings}

        api_base = get_from_param_or_env("api_base", api_base, "OPENROUTER_API_BASE")
        api_key = get_from_param_or_env("api_key", api_key, "OPENROUTER_API_KEY")

        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_base=api_base,
            api_key=api_key,
            additional_kwargs=additional_kwargs,
            max_retries=max_retries,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "OpenRouter_LLM"

```
 |  
| --- | --- |  
options: members: - OpenRouter
