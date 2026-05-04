# Vercel ai gateway
##  VercelAIGateway [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/vercel_ai_gateway/#llama_index.llms.vercel_ai_gateway.VercelAIGateway "Permanent link")
Bases: 
Vercel AI Gateway LLM.
To instantiate the `VercelAIGateway` class, you will need to provide authentication credentials. You can authenticate in the following ways (in order of precedence):
  1. Pass an API key or OIDC token directly to the `api_key` parameter
  2. Set the `VERCEL_AI_GATEWAY_API_KEY` environment variable
  3. Set the `VERCEL_OIDC_TOKEN` environment variable


If you haven't obtained an API key or OIDC token yet, you can visit the Vercel AI Gateway docs at (https://vercel.com/ai-gateway) for instructions. Once you have your credentials, you can use the `VercelAIGateway` class to interact with the LLM for tasks like chatting, streaming, and completing prompts.
Examples:
`pip install llama-index-llms-vercel-ai-gateway`

```
fromllama_index.llms.vercel_ai_gatewayimport VercelAIGateway

# Using API key directly
llm = VercelAIGateway(
    api_key="<your-api-key>",
    max_tokens=64000,
    context_window=200000,
    model="anthropic/claude-4-sonnet",
)

# Using OIDC token directly
llm = VercelAIGateway(
    api_key="<your-oidc-token>",
    max_tokens=64000,
    context_window=200000,
    model="anthropic/claude-4-sonnet",
)

# Using environment variables (VERCEL_AI_GATEWAY_API_KEY or VERCEL_OIDC_TOKEN)
llm = VercelAIGateway(
    max_tokens=64000,
    context_window=200000,
    model="anthropic/claude-4-sonnet",
)

# Customizing headers (overrides default http-referer and x-title)
llm = VercelAIGateway(
    api_key="<your-api-key>",
    model="anthropic/claude-4-sonnet",
    default_headers={
        "http-referer": "https://myapp.com/",
        "x-title": "My App"
    }
)

response = llm.complete("Hello World!")
print(str(response))

```

Source code in `llama-index-integrations/llms/llama-index-llms-vercel-ai-gateway/llama_index/llms/vercel_ai_gateway/base.py`  
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
```
 | 
```
classVercelAIGateway(OpenAILike):
"""
    Vercel AI Gateway LLM.

    To instantiate the `VercelAIGateway` class, you will need to provide authentication credentials.
    You can authenticate in the following ways (in order of precedence):

    1. Pass an API key or OIDC token directly to the `api_key` parameter
    2. Set the `VERCEL_AI_GATEWAY_API_KEY` environment variable
    3. Set the `VERCEL_OIDC_TOKEN` environment variable

    If you haven't obtained an API key or OIDC token yet, you can visit the Vercel AI Gateway docs
    at (https://vercel.com/ai-gateway) for instructions. Once you have your credentials, you can use
    the `VercelAIGateway` class to interact with the LLM for tasks like chatting, streaming, and
    completing prompts.

    Examples:
        `pip install llama-index-llms-vercel-ai-gateway`

        ```python
        from llama_index.llms.vercel_ai_gateway import VercelAIGateway

        # Using API key directly
        llm = VercelAIGateway(
            api_key="<your-api-key>",
            max_tokens=64000,
            context_window=200000,
            model="anthropic/claude-4-sonnet",


        # Using OIDC token directly
        llm = VercelAIGateway(
            api_key="<your-oidc-token>",
            max_tokens=64000,
            context_window=200000,
            model="anthropic/claude-4-sonnet",


        # Using environment variables (VERCEL_AI_GATEWAY_API_KEY or VERCEL_OIDC_TOKEN)
        llm = VercelAIGateway(
            max_tokens=64000,
            context_window=200000,
            model="anthropic/claude-4-sonnet",


        # Customizing headers (overrides default http-referer and x-title)
        llm = VercelAIGateway(
            api_key="<your-api-key>",
            model="anthropic/claude-4-sonnet",
            default_headers={
                "http-referer": "https://myapp.com/",
                "x-title": "My App"



        response = llm.complete("Hello World!")
        print(str(response))
        ```

    """

    model: str = Field(
        description="The model to use through Vercel AI Gateway. From your Vercel dashboard, go to the AI Gateway tab and select the Model List tab on the left dropdown to see the available models."
    )
    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description="The maximum number of context tokens for the model. From your Vercel dashboard, go to the AI Gateway tab and select the Model List tab on the left dropdown to see the available models and their context window sizes.",
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
        default_headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> None:
        additional_kwargs = additional_kwargs or {}

        api_base = get_from_param_or_env(
            "api_base", api_base, "VERCEL_AI_GATEWAY_API_BASE"
        )

        # Check for API key from multiple sources in order of precedence:
        if api_key is None:
            try:
                api_key = get_from_param_or_env(
                    "api_key", None, "VERCEL_AI_GATEWAY_API_KEY"
                )
            except ValueError:
                try:
                    api_key = get_from_param_or_env(
                        "oidc_token", None, "VERCEL_OIDC_TOKEN"
                    )
                except ValueError:
                    pass

        # Set up required Vercel AI Gateway headers
        gateway_headers = {
            "http-referer": "https://www.llamaindex.ai/",
            "x-title": "LlamaIndex",
        }

        if default_headers:
            gateway_headers.update(default_headers)

        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_base=api_base,
            api_key=api_key,
            additional_kwargs=additional_kwargs,
            max_retries=max_retries,
            default_headers=gateway_headers,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "VercelAIGateway_LLM"

```
 |  
| --- | --- |  
options: members: - VercelAIGateway
