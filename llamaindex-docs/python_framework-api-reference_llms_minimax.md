# Minimax
##  MiniMax [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/minimax/#llama_index.llms.minimax.MiniMax "Permanent link")
Bases: 
MiniMax LLM.
MiniMax offers powerful language models with up to 204,800 tokens context window through an OpenAI-compatible API.
Examples:
`pip install llama-index-llms-minimax`

```
fromllama_index.llms.minimaximport MiniMax

# Set up the MiniMax class with the required model and API key
llm = MiniMax(model="MiniMax-M2.7", api_key="your_api_key")

# Call the complete method with a query
response = llm.complete("Explain the importance of low latency LLMs")

print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-minimax/llama_index/llms/minimax/base.py`  
| 
```
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
```
 | 
```
classMiniMax(OpenAILike):
"""
    MiniMax LLM.

    MiniMax offers powerful language models with up to 204,800 tokens context window
    through an OpenAI-compatible API.

    Examples:
        `pip install llama-index-llms-minimax`

        ```python
        from llama_index.llms.minimax import MiniMax

        # Set up the MiniMax class with the required model and API key
        llm = MiniMax(model="MiniMax-M2.7", api_key="your_api_key")

        # Call the complete method with a query
        response = llm.complete("Explain the importance of low latency LLMs")

        print(response)
        ```

    """

    def__init__(
        self,
        model: str = DEFAULT_MODEL,
        api_key: Optional[str] = None,
        api_base: str = DEFAULT_API_BASE,
        temperature: float = 1.0,
        **openai_llm_kwargs: Any,
    ) -> None:
        api_key = api_key or os.environ.get("MINIMAX_API_KEY", None)
        if api_key is None:
            raise ValueError(
                "MiniMax API key is required. Either pass `api_key` or set the "
                "`MINIMAX_API_KEY` environment variable."
            )
        context_window = openai_llm_kwargs.pop(
            "context_window", get_context_window(model)
        )
        super().__init__(
            model=model,
            api_key=api_key,
            api_base=api_base,
            temperature=temperature,
            is_chat_model=openai_llm_kwargs.pop("is_chat_model", True),
            is_function_calling_model=openai_llm_kwargs.pop(
                "is_function_calling_model", model in FUNCTION_CALLING_MODELS
            ),
            context_window=context_window,
            **openai_llm_kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "MiniMax"

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/minimax/#llama_index.llms.minimax.MiniMax.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-minimax/llama_index/llms/minimax/base.py`  
| 
```
65
66
67
68
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "MiniMax"

```
 |  
| --- | --- |  
options: members: - MiniMax
