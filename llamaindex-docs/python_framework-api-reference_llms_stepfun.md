# Stepfun
##  StepFun [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/stepfun/#llama_index.llms.stepfun.StepFun "Permanent link")
Bases: 
The StepFun class is a subclass of OpenAILike and is used to interact with the StepFun model.
#### Parameters[#](https://developers.llamaindex.ai/python/framework-api-reference/llms/stepfun/#llama_index.llms.stepfun.StepFun--parameters "Permanent link")

```
model (str): The name of the Stepfun model to use. See https://platform.stepfun.com/docs/llm/modeloverview for options.
context_window (int): The maximum size of the context window for the model. See https://platform.stepfun.com/docs/llm/modeloverview for options.
is_chat_model (bool): Indicates whether the model is a chat model.

```

#### Attributes[#](https://developers.llamaindex.ai/python/framework-api-reference/llms/stepfun/#llama_index.llms.stepfun.StepFun--attributes "Permanent link")

```
model (str): The name of the Stepfun model to use.
context_window (int): The maximum size of the context window for the model.
is_chat_model (bool): Indicates whether the model is a chat model.

```
Source code in `llama-index-integrations/llms/llama-index-llms-stepfun/llama_index/llms/stepfun/base.py`  
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
```
 | 
```
classStepFun(OpenAILike):
"""
    The StepFun class is a subclass of OpenAILike and is used to interact with the StepFun model.

    Parameters
    ----------
        model (str): The name of the Stepfun model to use. See https://platform.stepfun.com/docs/llm/modeloverview for options.
        context_window (int): The maximum size of the context window for the model. See https://platform.stepfun.com/docs/llm/modeloverview for options.
        is_chat_model (bool): Indicates whether the model is a chat model.

    Attributes
    ----------
        model (str): The name of the Stepfun model to use.
        context_window (int): The maximum size of the context window for the model.
        is_chat_model (bool): Indicates whether the model is a chat model.

    """

    model: str = Field(
        description="The Stepfun model to use. See https://platform.stepfun.com/docs/llm/modeloverview for options."
    )
    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description="The maximum number of context tokens for the model. See https://platform.stepfun.com/docs/llm/modeloverview for options.",
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
"""
        Initialize the OpenAI API client.

        Args:
            model (str): The name of the model to use. Defaults to DEFAULT_MODEL.
            temperature (float): The temperature to use for the model. Defaults to DEFAULT_TEMPERATURE.
            max_tokens (int): The maximum number of tokens to generate. Defaults to DEFAULT_NUM_OUTPUTS.
            additional_kwargs (Optional[Dict[str, Any]]): Additional keyword arguments to pass to the model. Defaults to None.
            max_retries (int): The maximum number of retries to make when calling the API. Defaults to 5.
            api_base (Optional[str]): The base URL for the API. Defaults to DEFAULT_API_BASE.
            api_key (Optional[str]): The API key to use. Defaults to None.
            **kwargs (Any): Additional keyword arguments to pass to the model.

        Returns:
            None

        """
        additional_kwargs = additional_kwargs or {}

        api_base = get_from_param_or_env("api_base", api_base, "STEPFUN_API_BASE")
        api_key = get_from_param_or_env("api_key", api_key, "STEPFUN_API_KEY")

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
        return "Stpefun_LLM"

```
 |  
| --- | --- |  
options: members: - StepFun
