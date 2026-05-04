# Heroku
##  Heroku [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/heroku/#llama_index.llms.heroku.Heroku "Permanent link")
Bases: 
Heroku Managed Inference LLM Integration.
Source code in `llama-index-integrations/llms/llama-index-llms-heroku/llama_index/llms/heroku/base.py`  
| 
```
10
11
12
13
14
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
```
 | 
```
classHeroku(OpenAILike):
"""Heroku Managed Inference LLM Integration."""

    _client: Any = PrivateAttr()
    _aclient: Any = PrivateAttr()

    def__init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        inference_url: Optional[str] = None,
        max_tokens: Optional[int] = 1024,
        is_chat_model: bool = True,
        **kwargs: Any,
    ) -> None:
"""
        Initialize an instance of the Heroku class.

        This class provides an interface to Heroku's Managed Inference API.
        It connects to your Heroku app's inference endpoints for chat and completion models.

        Args:
            model (str, optional): The model to use. If not provided, will use INFERENCE_MODEL_ID.
            api_key (str, optional): The API key for Heroku inference. Defaults to INFERENCE_KEY.
            inference_url (str, optional): The base URL for inference. Defaults to INFERENCE_URL.
            max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 1024.
            **kwargs: Additional keyword arguments.

        Environment Variables:
            - INFERENCE_KEY: The API key for Heroku inference
            - INFERENCE_URL: The base URL for inference endpoints
            - INFERENCE_MODEL_ID: The model ID to use

        Raises:
            ValueError: If required environment variables are not set.

        """
        # Get API key from parameter or environment
        try:
            api_key = get_from_param_or_env(
                "api_key",
                api_key,
                "INFERENCE_KEY",
            )
        except ValueError:
            raise ValueError(
                "API key is required. Set INFERENCE_KEY environment variable or pass api_key parameter."
            )

        # Get inference URL from parameter or environment
        try:
            inference_url = get_from_param_or_env(
                "inference_url",
                inference_url,
                "INFERENCE_URL",
            )
        except ValueError:
            raise ValueError(
                "Inference URL is required. Set INFERENCE_URL environment variable or pass inference_url parameter."
            )

        # Get model from parameter or environment
        try:
            model = get_from_param_or_env(
                "model",
                model,
                "INFERENCE_MODEL_ID",
            )
        except ValueError:
            raise ValueError(
                "Model is required. Set INFERENCE_MODEL_ID environment variable or pass model parameter."
            )

        # Construct the base URL for the API
        base_url = f"{inference_url}/v1"

        super().__init__(
            model=model,
            api_key=api_key,
            api_base=base_url,
            max_tokens=max_tokens,
            is_chat_model=is_chat_model,
            default_headers={"User-Agent": "llama-index-llms-heroku"},
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "Heroku"

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/heroku/#llama_index.llms.heroku.Heroku.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-heroku/llama_index/llms/heroku/base.py`  
| 
```
96
97
98
99
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "Heroku"

```
 |  
| --- | --- |  
options: members: - Heroku
