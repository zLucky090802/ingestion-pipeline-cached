# Meta
##  LlamaLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/meta/#llama_index.llms.meta.LlamaLLM "Permanent link")
Bases: 
Llama LLM.
Examples:
`pip install llama-index-llms-meta`

```
fromllama_index.llms.metaimport LlamaLLM

# set api key in env or in llm
# import os
# os.environ["LLAMA_API_KEY"] = "your api key"

llm = LlamaLLM(
    model="Llama-3.3-8B-Instruct", api_key="your_api_key"
)

resp = llm.complete("Who is Paul Graham?")
print(resp)

```

Source code in `llama-index-integrations/llms/llama-index-llms-meta/llama_index/llms/meta/base.py`  
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
classLlamaLLM(OpenAILike):
"""
    Llama LLM.

    Examples:
        `pip install llama-index-llms-meta`

        ```python
        from llama_index.llms.meta import LlamaLLM

        # set api key in env or in llm
        # import os
        # os.environ["LLAMA_API_KEY"] = "your api key"

        llm = LlamaLLM(
            model="Llama-3.3-8B-Instruct", api_key="your_api_key"


        resp = llm.complete("Who is Paul Graham?")
        print(resp)
        ```

    """

    def__init__(
        self,
        model: str = "Llama-3.3-8B-Instruct",
        api_key: Optional[str] = None,
        api_base: str = "https://api.llama.com/compat/v1",
        is_chat_model: bool = True,
        # Slightly lower to account for tokenization defaults
        context_window: int = 120000,
        **kwargs: Any,
    ) -> None:
        api_key = api_key or os.environ.get("LLAMA_API_KEY", None)
        super().__init__(
            model=model,
            api_key=api_key,
            api_base=api_base,
            is_chat_model=is_chat_model,
            context_window=context_window,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "LlamaLLM"

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/meta/#llama_index.llms.meta.LlamaLLM.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-meta/llama_index/llms/meta/base.py`  
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
    return "LlamaLLM"

```
 |  
| --- | --- |  
options: members: - LlamaLLM
