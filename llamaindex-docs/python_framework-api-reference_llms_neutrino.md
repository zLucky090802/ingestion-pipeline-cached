# Neutrino
##  Neutrino [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/neutrino/#llama_index.llms.neutrino.Neutrino "Permanent link")
Bases: 
Neutrino LLM.
Examples:
`pip install llama-index-llms-neutrino`
You can create an API key at: [platform.neutrinoapp.com](https://platform.neutrinoapp.com/)

```
importos

os.environ["NEUTRINO_API_KEY"] = "<your-neutrino-api-key>"

```

A router is a collection of LLMs that you can route queries to. You can create a router in the Neutrino [dashboard](https://platform.neutrinoapp.com/) or use the default router, which includes all supported models.
You can treat a router as a LLM.

```
fromllama_index.llms.neutrinoimport Neutrino

llm = Neutrino(
    # api_key="<your-neutrino-api-key>",
    # router="<your-router-id>"  # (or 'default')
)

response = llm.complete("In short, a Neutrino is")
print(f"Optimal model: {response.raw['model']}")
print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-neutrino/llama_index/llms/neutrino/base.py`  
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
```
 | 
```
classNeutrino(OpenAILike):
"""
    Neutrino LLM.

    Examples:
        `pip install llama-index-llms-neutrino`

        You can create an API key at: <a href="https://platform.neutrinoapp.com/">platform.neutrinoapp.com</a>

        ```python
        import os

        os.environ["NEUTRINO_API_KEY"] = "<your-neutrino-api-key>"
        ```

        A router is a collection of LLMs that you can route queries to. You can create a router in the Neutrino <a href="https://platform.neutrinoapp.com/">dashboard</a> or use the default router,
        which includes all supported models.

        You can treat a router as a LLM.

        ```python
        from llama_index.llms.neutrino import Neutrino

        llm = Neutrino(
            # api_key="<your-neutrino-api-key>",
            # router="<your-router-id>"  # (or 'default')


        response = llm.complete("In short, a Neutrino is")
        print(f"Optimal model: {response.raw['model']}")
        print(response)
        ```

    """

    model: str = Field(
        description="The Neutrino router to use. See https://docs.neutrinoapp.com/router for details."
    )
    context_window: int = Field(
        default=MAX_CONTEXT_WINDOW,
        description="The maximum number of context tokens for the model. Defaults to the largest supported model (Claude).",
        gt=0,
    )
    is_chat_model: bool = Field(
        default=True,
        description=LLMMetadata.model_fields["is_chat_model"].description,
    )

    def__init__(
        self,
        model: Optional[str] = None,
        router: str = DEFAULT_ROUTER,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_NUM_OUTPUTS,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        max_retries: int = 5,
        api_base: Optional[str] = DEFAULT_API_BASE,
        api_key: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        additional_kwargs = additional_kwargs or {}

        api_base = get_from_param_or_env("api_base", api_base, "NEUTRINO_API_BASE")
        api_key = get_from_param_or_env("api_key", api_key, "NEUTRINO_API_KEY")

        model = model or router

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
        return "Neutrino_LLM"

```
 |  
| --- | --- |  
options: members: - Neutrino
