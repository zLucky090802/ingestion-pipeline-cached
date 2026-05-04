# Apertis
##  Apertis [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/apertis/#llama_index.llms.apertis.Apertis "Permanent link")
Bases: 
Apertis LLM.
Apertis provides a unified API gateway to access multiple LLM providers including OpenAI, Anthropic, Google, and more through an OpenAI-compatible interface.
Supported Endpoints
  * `/v1/chat/completions` - OpenAI Chat Completions format (default)
  * `/v1/responses` - OpenAI Responses format compatible
  * `/v1/messages` - Anthropic format compatible


To instantiate the `Apertis` class, you will need an API key. You can set the API key either as an environment variable `APERTIS_API_KEY` or directly in the class constructor.
You can obtain an API key at https://api.apertis.ai/token
Examples:
`pip install llama-index-llms-apertis`

```
fromllama_index.llms.apertisimport Apertis

llm = Apertis(
    api_key="<your-api-key>",
    model="gpt-5.2",
)

response = llm.complete("Hello World!")
print(str(response))

```

Source code in `llama-index-integrations/llms/llama-index-llms-apertis/llama_index/llms/apertis/base.py`  
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
```
 | 
```
classApertis(OpenAILike):
"""
    Apertis LLM.

    Apertis provides a unified API gateway to access multiple LLM providers
    including OpenAI, Anthropic, Google, and more through an OpenAI-compatible
    interface.

    Supported Endpoints:
        - `/v1/chat/completions` - OpenAI Chat Completions format (default)
        - `/v1/responses` - OpenAI Responses format compatible
        - `/v1/messages` - Anthropic format compatible

    To instantiate the `Apertis` class, you will need an API key. You can set
    the API key either as an environment variable `APERTIS_API_KEY` or directly
    in the class constructor.

    You can obtain an API key at https://api.apertis.ai/token

    Examples:
        `pip install llama-index-llms-apertis`

        ```python
        from llama_index.llms.apertis import Apertis

        llm = Apertis(
            api_key="<your-api-key>",
            model="gpt-5.2",


        response = llm.complete("Hello World!")
        print(str(response))
        ```

    """

    model: str = Field(
        description="The model to use. Supports models from OpenAI, Anthropic, Google, and more."
    )
    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description="The maximum number of context tokens for the model.",
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
        **kwargs: Any,
    ) -> None:
        additional_kwargs = additional_kwargs or {}

        api_base = get_from_param_or_env("api_base", api_base, "APERTIS_API_BASE")
        api_key = get_from_param_or_env("api_key", api_key, "APERTIS_API_KEY")

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
        return "Apertis_LLM"

```
 |  
| --- | --- |  
options: members: - Apertis
