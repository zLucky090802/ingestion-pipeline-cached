# Together
##  TogetherLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/together/#llama_index.llms.together.TogetherLLM "Permanent link")
Bases: 
Together LLM.
Examples:
`pip install llama-index-llms-together`

```
fromllama_index.llms.togetherimport TogetherLLM

# set api key in env or in llm
# import os
# os.environ["TOGETHER_API_KEY"] = "your api key"

llm = TogetherLLM(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1", api_key="your_api_key"
)

resp = llm.complete("Who is Paul Graham?")
print(resp)

```

Source code in `llama-index-integrations/llms/llama-index-llms-together/llama_index/llms/together/base.py`  
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
classTogetherLLM(OpenAILike):
"""
    Together LLM.

    Examples:
        `pip install llama-index-llms-together`

        ```python
        from llama_index.llms.together import TogetherLLM

        # set api key in env or in llm
        # import os
        # os.environ["TOGETHER_API_KEY"] = "your api key"

        llm = TogetherLLM(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1", api_key="your_api_key"


        resp = llm.complete("Who is Paul Graham?")
        print(resp)
        ```

    """

    def__init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        api_base: str = "https://api.together.xyz/v1",
        is_chat_model: bool = True,
        **kwargs: Any,
    ) -> None:
        api_key = api_key or os.environ.get("TOGETHER_API_KEY", None)
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
        return "TogetherLLM"

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/together/#llama_index.llms.together.TogetherLLM.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-together/llama_index/llms/together/base.py`  
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
    return "TogetherLLM"

```
 |  
| --- | --- |  
options: members: - TogetherLLM
