# Groq
##  Groq [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/groq/#llama_index.llms.groq.Groq "Permanent link")
Bases: 
Groq LLM.
Examples:
`pip install llama-index-llms-groq`

```
fromllama_index.llms.groqimport Groq

# Set up the Groq class with the required model and API key
llm = Groq(model="llama3-70b-8192", api_key="your_api_key")

# Call the complete method with a query
response = llm.complete("Explain the importance of low latency LLMs")

print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-groq/llama_index/llms/groq/base.py`  
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
```
 | 
```
classGroq(OpenAILike):
"""
    Groq LLM.

    Examples:
        `pip install llama-index-llms-groq`

        ```python
        from llama_index.llms.groq import Groq

        # Set up the Groq class with the required model and API key
        llm = Groq(model="llama3-70b-8192", api_key="your_api_key")

        # Call the complete method with a query
        response = llm.complete("Explain the importance of low latency LLMs")

        print(response)
        ```

    """

    def__init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        api_base: str = "https://api.groq.com/openai/v1",
        is_chat_model: bool = True,
        is_function_calling_model: bool = True,
        **kwargs: Any,
    ) -> None:
        api_key = api_key or os.environ.get("GROQ_API_KEY", None)
        super().__init__(
            model=model,
            api_key=api_key,
            api_base=api_base,
            is_chat_model=is_chat_model,
            is_function_calling_model=is_function_calling_model,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "Groq"

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/groq/#llama_index.llms.groq.Groq.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-groq/llama_index/llms/groq/base.py`  
| 
```
47
48
49
50
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "Groq"

```
 |  
| --- | --- |  
options: members: - Groq
