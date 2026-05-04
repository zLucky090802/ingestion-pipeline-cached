# Cerebras
##  Cerebras [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cerebras/#llama_index.llms.cerebras.Cerebras "Permanent link")
Bases: 
Cerebras LLM.
Examples:
`pip install llama-index-llms-cerebras`

```
fromllama_index.llms.cerebrasimport Cerebras

# Set up the Cerebras class with the required model and API key
llm = Cerebras(model="llama-3.3-70b", api_key="your_api_key")

# Call the complete method with a query
response = llm.complete("Why is fast inference important?")

print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-cerebras/llama_index/llms/cerebras/base.py`  
| 
```
 7
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
```
 | 
```
classCerebras(OpenAILike):
"""
    Cerebras LLM.

    Examples:
        `pip install llama-index-llms-cerebras`

        ```python
        from llama_index.llms.cerebras import Cerebras

        # Set up the Cerebras class with the required model and API key
        llm = Cerebras(model="llama-3.3-70b", api_key="your_api_key")

        # Call the complete method with a query
        response = llm.complete("Why is fast inference important?")

        print(response)
        ```

    """

    def__init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        api_base: str = os.environ.get("CEREBRAS_BASE_URL", None)
        or "https://api.cerebras.ai/v1/",
        is_chat_model: bool = True,
        **kwargs: Any,
    ) -> None:
        api_key = api_key or os.environ.get("CEREBRAS_API_KEY", None)

        assert api_key is not None, (
            "API Key not specified! Please set `CEREBRAS_API_KEY`!"
        )

        super().__init__(
            model=model,
            api_key=api_key,
            api_base=api_base,
            is_chat_model=is_chat_model,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "Cerebras"

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cerebras/#llama_index.llms.cerebras.Cerebras.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-cerebras/llama_index/llms/cerebras/base.py`  
| 
```
51
52
53
54
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "Cerebras"

```
 |  
| --- | --- |  
options: members: - Cerebras
