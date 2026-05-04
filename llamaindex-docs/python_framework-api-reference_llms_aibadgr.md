# Aibadgr
##  AIBadgr [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/aibadgr/#llama_index.llms.aibadgr.AIBadgr "Permanent link")
Bases: 
AI Badgr LLM (Budget/Utility, OpenAI-compatible).
AI Badgr provides OpenAI-compatible API endpoints with tier-based model naming. Use tier names (basic, normal, premium) or power-user model names (phi-3-mini, mistral-7b, llama3-8b-instruct). OpenAI model names are also accepted and mapped automatically.
Examples:
`pip install llama-index-llms-aibadgr`

```
fromllama_index.llms.aibadgrimport AIBadgr

# Set up the AIBadgr class with the required model and API key
llm = AIBadgr(model="premium", api_key="your_api_key")

# Call the complete method with a query
response = llm.complete("Explain the importance of low latency LLMs")

print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-aibadgr/llama_index/llms/aibadgr/base.py`  
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
classAIBadgr(OpenAILike):
"""
    AI Badgr LLM (Budget/Utility, OpenAI-compatible).

    AI Badgr provides OpenAI-compatible API endpoints with tier-based model naming.
    Use tier names (basic, normal, premium) or power-user model names
    (phi-3-mini, mistral-7b, llama3-8b-instruct). OpenAI model names are also
    accepted and mapped automatically.

    Examples:
        `pip install llama-index-llms-aibadgr`

        ```python
        from llama_index.llms.aibadgr import AIBadgr

        # Set up the AIBadgr class with the required model and API key
        llm = AIBadgr(model="premium", api_key="your_api_key")

        # Call the complete method with a query
        response = llm.complete("Explain the importance of low latency LLMs")

        print(response)
        ```

    """

    def__init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        api_base: str = "https://aibadgr.com/api/v1",
        is_chat_model: bool = True,
        **kwargs: Any,
    ) -> None:
        api_key = api_key or os.environ.get("AIBADGR_API_KEY", None)
        api_base = os.environ.get("AIBADGR_BASE_URL", api_base)
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
        return "AIBadgr"

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/aibadgr/#llama_index.llms.aibadgr.AIBadgr.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-aibadgr/llama_index/llms/aibadgr/base.py`  
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
    return "AIBadgr"

```
 |  
| --- | --- |  
options: members: - AIBadgr
