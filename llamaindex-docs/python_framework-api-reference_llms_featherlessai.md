# Featherlessai
##  FeatherlessLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/featherlessai/#llama_index.llms.featherlessai.FeatherlessLLM "Permanent link")
Bases: 
Featherless LLM.
Examples:
`pip install llama-index-llms-featherlessai`

```
fromllama_index.llms.featherlessaiimport FeatherlessLLM
# set api key in env or in llm
# import os
# os.environ["FEATHERLESS_API_KEY"] = "your api key"
llm = FeatherlessLLM(
    model="Qwen/Qwen3-32B", api_key="your_api_key"
)
resp = llm.complete("Who is Paul Graham?")
print(resp)

```

Source code in `llama-index-integrations/llms/llama-index-llms-featherlessai/llama_index/llms/featherlessai/base.py`  
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
```
 | 
```
classFeatherlessLLM(OpenAILike):
"""
    Featherless LLM.

    Examples:
        `pip install llama-index-llms-featherlessai`
        ```python
        from llama_index.llms.featherlessai import FeatherlessLLM
        # set api key in env or in llm
        # import os
        # os.environ["FEATHERLESS_API_KEY"] = "your api key"
        llm = FeatherlessLLM(
            model="Qwen/Qwen3-32B", api_key="your_api_key"

        resp = llm.complete("Who is Paul Graham?")
        print(resp)
        ```

    """

    def__init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        api_base: str = "https://api.featherless.ai/v1",
        is_chat_model: bool = True,
        context_window: Optional[int] = None,
        is_function_calling_model: bool = False,
        **kwargs: Any,
    ) -> None:
        api_key = api_key or os.environ.get("FEATHERLESS_API_KEY", None)
        super().__init__(
            model=model,
            api_key=api_key,
            api_base=api_base,
            is_chat_model=is_chat_model,
            context_window=context_window,
            is_function_calling_model=is_function_calling_model,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "FeatherlessLLM"

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/featherlessai/#llama_index.llms.featherlessai.FeatherlessLLM.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-featherlessai/llama_index/llms/featherlessai/base.py`  
| 
```
48
49
50
51
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "FeatherlessLLM"

```
 |  
| --- | --- |  
options: members: - FeatherlessLLM
