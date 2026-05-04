# Helicone
##  Helicone [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/helicone/#llama_index.llms.helicone.Helicone "Permanent link")
Bases: 
Helicone (OpenAI-compatible) LLM.
Route OpenAI-compatible requests through Helicone for observability and control.
Authentication: - Set your Helicone API key via the `api_key` parameter or `HELICONE_API_KEY`. No OpenAI/third-party provider keys are required when using the AI Gateway.
Examples:
`pip install llama-index-llms-helicone`

```
fromllama_index.llms.heliconeimport Helicone
fromllama_index.llms.openai_like.baseimport ChatMessage

llm = Helicone(
    api_key="<helicone-api-key>",
    model="gpt-4o-mini",  # works across providers
)

message: ChatMessage = ChatMessage(role="user", content="Hello world!")

response = helicone.chat(messages=[message])
print(str(response))

```

Source code in `llama-index-integrations/llms/llama-index-llms-helicone/llama_index/llms/helicone/base.py`  
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
113
```
 | 
```
classHelicone(OpenAILike):
"""
    Helicone (OpenAI-compatible) LLM.

    Route OpenAI-compatible requests through Helicone for observability and control.

    Authentication:
    - Set your Helicone API key via the `api_key` parameter or `HELICONE_API_KEY`.
      No OpenAI/third-party provider keys are required when using the AI Gateway.

    Examples:
        `pip install llama-index-llms-helicone`

        ```python
        from llama_index.llms.helicone import Helicone
        from llama_index.llms.openai_like.base import ChatMessage

        llm = Helicone(
            api_key="<helicone-api-key>",
            model="gpt-4o-mini",  # works across providers


        message: ChatMessage = ChatMessage(role="user", content="Hello world!")

        response = helicone.chat(messages=[message])
        print(str(response))
        ```

    """

    model: str = Field(
        description=(
            "OpenAI-compatible model name routed via the Helicone AI Gateway. "
            "Learn more about [provider routing](https://docs.helicone.ai/gateway/provider-routing). "
            "All models are visible [here](https://www.helicone.ai/models)."
        )
    )
    api_base: Optional[str] = Field(
        default=DEFAULT_API_BASE,
        description=(
            "Base URL for the Helicone AI Gateway. Can also be set via the "
            "HELICONE_API_BASE environment variable. See the "
            "[Gateway overview](https://docs.helicone.ai/gateway/overview)."
        ),
    )
    api_key: Optional[str] = Field(
        description=(
            "Helicone API key used to authorize requests (Authorization: Bearer). "
            "Provide directly or set via HELICONE_API_KEY. Generate your API key "
            "in the [dashboard settings](https://us.helicone.ai/settings/api-keys). "
        ),
    )
    default_headers: Optional[Dict[str, str]] = Field(
        default=None,
        description=(
            "Additional HTTP headers to include with requests. The Helicone "
            "Authorization header is added automatically from api_key. See "
            "[custom properties](https://docs.helicone.ai/features/advanced-usage/custom-properties)/[headers](https://docs.helicone.ai/helicone-headers/header-directory)."
        ),
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
        default_headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> None:
        additional_kwargs = additional_kwargs or {}

        api_base = get_from_param_or_env("api_base", api_base, "HELICONE_API_BASE")
        api_key = get_from_param_or_env("api_key", api_key, "HELICONE_API_KEY")

        if default_headers:
            default_headers.update({"Authorization": f"Bearer {api_key}"})
        else:
            default_headers = {"Authorization": f"Bearer {api_key}"}

        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_base=api_base,
            default_headers=default_headers,
            additional_kwargs=additional_kwargs,
            max_retries=max_retries,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "Helicone_LLM"

```
 |  
| --- | --- |  
options: members: - Helicone
