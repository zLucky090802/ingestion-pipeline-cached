# Cometapi
##  CometAPI [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cometapi/#llama_index.llms.cometapi.CometAPI "Permanent link")
Bases: 
CometAPI LLM.
CometAPI provides access to various state-of-the-art LLM models including GPT series, Claude series, Gemini series, and more. To use CometAPI, you need to obtain an API key from https://api.cometapi.com/console/token.
Examples:
`pip install llama-index-llms-cometapi`

```
fromllama_index.llms.cometapiimport CometAPI

llm = CometAPI(
    api_key="<your-api-key>",
    max_tokens=256,
    context_window=4096,
    model="gpt-4o-mini",
)

response = llm.complete("Hello World!")
print(str(response))

```

Source code in `llama-index-integrations/llms/llama-index-llms-cometapi/llama_index/llms/cometapi/base.py`  
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
```
 | 
```
classCometAPI(OpenAILike):
"""
    CometAPI LLM.

    CometAPI provides access to various state-of-the-art LLM models including GPT series,
    Claude series, Gemini series, and more. To use CometAPI, you need to obtain an API key
    from https://api.cometapi.com/console/token.

    Examples:
        `pip install llama-index-llms-cometapi`

        ```python
        from llama_index.llms.cometapi import CometAPI

        llm = CometAPI(
            api_key="<your-api-key>",
            max_tokens=256,
            context_window=4096,
            model="gpt-4o-mini",


        response = llm.complete("Hello World!")
        print(str(response))
        ```

    """

    model: str = Field(
        description="The CometAPI model to use. See https://api.cometapi.com/pricing for available models."
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

        api_base = get_from_param_or_env("api_base", api_base, "COMETAPI_API_BASE")
        api_key = get_from_param_or_env("api_key", api_key, "COMETAPI_API_KEY")

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
        return "CometAPI_LLM"

```
 |  
| --- | --- |  
options: members: - CometAPI
