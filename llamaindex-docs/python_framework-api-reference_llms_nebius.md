# Nebius
##  NebiusLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/nebius/#llama_index.llms.nebius.NebiusLLM "Permanent link")
Bases: 
Nebius AI Studio LLM class.
Examples:
`pip install llama-index-llms-nebius`

```
fromllama_index.llms.nebiusimport NebiusLLM

# set api key in env or in llm
# import os
# os.environ["NEBIUS_API_KEY"] = "your api key"

llm = NebiusLLM(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1", api_key="your_api_key"
)

resp = llm.complete("Who is Paul Graham?")
print(resp)

```

Source code in `llama-index-integrations/llms/llama-index-llms-nebius/llama_index/llms/nebius/base.py`  
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
```
 | 
```
classNebiusLLM(OpenAILike):
"""
    Nebius AI Studio LLM class.

    Examples:
        `pip install llama-index-llms-nebius`

        ```python
        from llama_index.llms.nebius import NebiusLLM

        # set api key in env or in llm
        # import os
        # os.environ["NEBIUS_API_KEY"] = "your api key"

        llm = NebiusLLM(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1", api_key="your_api_key"


        resp = llm.complete("Who is Paul Graham?")
        print(resp)
        ```

    """

    def__init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        api_base: str = DEFAULT_API_BASE,
        is_chat_model: bool = True,
        **kwargs: Any,
    ) -> None:
        api_key = api_key or os.environ.get("NEBIUS_API_KEY", None)
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
        return "NebiusLLM"

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/nebius/#llama_index.llms.nebius.NebiusLLM.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-nebius/llama_index/llms/nebius/base.py`  
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
    return "NebiusLLM"

```
 |  
| --- | --- |  
options: members: - NebiusLLM
