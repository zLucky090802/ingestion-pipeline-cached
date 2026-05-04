# Servam
##  Sarvam [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/servam/#llama_index.llms.sarvam.Sarvam "Permanent link")
Bases: 
Sarvam LLM.
To instantiate the `Sarvam` class, you will need to provide an API key. You can set the API key either as an environment variable `SARVAM_API_KEY` or directly in the class constructor. If setting it in the class constructor, it would look like this:
If you haven't signed up for an API key yet, you can do so on the Sarvam website at (https://sarvam.ai). Once you have your API key, you can use the `Sarvam` class to interact with the LLM for tasks like chatting, streaming, and completing prompts.
Examples:
`pip install llama-index-llms-sarvam`

```
fromllama_index.llms.sarvamimport Sarvam

llm = Sarvam(
    api_key="<your-api-key>",
    max_tokens=256,
    context_window=4096,
    model="sarvam-m",
)

response = llm.complete("Hello World!")
print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-sarvam/llama_index/llms/sarvam/base.py`  
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
classSarvam(OpenAILike):
"""
    Sarvam LLM.

    To instantiate the `Sarvam` class, you will need to provide an API key. You can set the API key either as an environment variable `SARVAM_API_KEY` or directly in the class
    constructor. If setting it in the class constructor, it would look like this:

    If you haven't signed up for an API key yet, you can do so on the Sarvam website at (https://sarvam.ai). Once you have your API key, you can use the `Sarvam` class to interact
    with the LLM for tasks like chatting, streaming, and completing prompts.

    Examples:
        `pip install llama-index-llms-sarvam`

        ```python
        from llama_index.llms.sarvam import Sarvam

        llm = Sarvam(
            api_key="<your-api-key>",
            max_tokens=256,
            context_window=4096,
            model="sarvam-m",


        response = llm.complete("Hello World!")
        print(response)
        ```

    """

    model: str = Field(description="The Sarvam model to use.")
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

        api_base = get_from_param_or_env("api_base", api_base, "SARVAM_API_BASE")
        api_key = get_from_param_or_env("api_key", api_key, "SARVAM_API_KEY")

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
        return "Sarvam_LLM"

```
 |  
| --- | --- |  
options: members: - Sarvam
