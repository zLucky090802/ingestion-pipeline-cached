# Deepseek
##  DeepSeek [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/deepseek/#llama_index.llms.deepseek.DeepSeek "Permanent link")
Bases: 
DeepSeek LLM.
Examples:
`pip install llama-index-llms-deepseek`

```
fromllama_index.llms.deepseekimport DeepSeek

# Set up the DeepSeek class with the required model and API key
llm = DeepSeek(model="deepseek-chat", api_key="your_api_key")

# Call the complete method with a query
response = llm.complete("Explain the importance of low latency LLMs")

print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-deepseek/llama_index/llms/deepseek/base.py`  
| 
```
 8
 9
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
```
 | 
```
classDeepSeek(OpenAILike):
"""
    DeepSeek LLM.

    Examples:
        `pip install llama-index-llms-deepseek`

        ```python
        from llama_index.llms.deepseek import DeepSeek

        # Set up the DeepSeek class with the required model and API key
        llm = DeepSeek(model="deepseek-chat", api_key="your_api_key")

        # Call the complete method with a query
        response = llm.complete("Explain the importance of low latency LLMs")

        print(response)
        ```

    """

    def__init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        api_base: str = "https://api.deepseek.com",
        **openai_llm_kwargs: Any,
    ) -> None:
        api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", None)
        context_window = openai_llm_kwargs.pop(
            "context_window", get_context_window(model)
        )
        super().__init__(
            model=model,
            api_key=api_key,
            api_base=api_base,
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
        return "DeepSeek"

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/deepseek/#llama_index.llms.deepseek.DeepSeek.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-deepseek/llama_index/llms/deepseek/base.py`  
| 
```
52
53
54
55
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "DeepSeek"

```
 |  
| --- | --- |  
options: members: - DeepSeek
