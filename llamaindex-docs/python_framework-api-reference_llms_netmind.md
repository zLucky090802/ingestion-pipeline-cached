# Netmind
##  NetmindLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/netmind/#llama_index.llms.netmind.NetmindLLM "Permanent link")
Bases: 
Netmind LLM.
Examples:
`pip install llama-index-llms-netmind`

```
fromllama_index.llms.netmindimport NetmindLLM

# set api key in env or in llm
# import os
# os.environ["NETMIND_API_KEY"] = "your api key"

llm = NetmindLLM(
    model="meta-llama/Llama-3.3-70B-Instruct", api_key="your_api_key"
)

resp = llm.complete("Who is Paul Graham?")
print(resp)

```

Source code in `llama-index-integrations/llms/llama-index-llms-netmind/llama_index/llms/netmind/base.py`  
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
classNetmindLLM(OpenAILike):
"""
    Netmind LLM.

    Examples:
        `pip install llama-index-llms-netmind`

        ```python
        from llama_index.llms.netmind import NetmindLLM

        # set api key in env or in llm
        # import os
        # os.environ["NETMIND_API_KEY"] = "your api key"

        llm = NetmindLLM(
            model="meta-llama/Llama-3.3-70B-Instruct", api_key="your_api_key"


        resp = llm.complete("Who is Paul Graham?")
        print(resp)
        ```

    """

    def__init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        api_base: str = "https://api.netmind.ai/inference-api/openai/v1",
        is_chat_model: bool = True,
        **kwargs: Any,
    ) -> None:
        api_key = api_key or os.environ.get("NETMIND_API_KEY", None)
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
        return "NetmindLLM"

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/netmind/#llama_index.llms.netmind.NetmindLLM.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-netmind/llama_index/llms/netmind/base.py`  
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
    return "NetmindLLM"

```
 |  
| --- | --- |  
options: members: - NetmindLLM
