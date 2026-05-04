# Pipeshift
##  Pipeshift [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/pipeshift/#llama_index.llms.pipeshift.Pipeshift "Permanent link")
Bases: 
Pipeshift LLM.
Examples:
`pip install llama-index-llms-pipeshift`

```
fromllama_index.llms.pipeshiftimport Pipeshift

# set api key in env or in llm
# import os
# os.environ["PIPESHIFT_API_KEY"] = "your api key"

llm = Pipeshift(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct", api_key="your_api_key"
)

resp = llm.complete("How fast is porsche gt3 rs?")
print(resp)

```

Source code in `llama-index-integrations/llms/llama-index-llms-pipeshift/llama_index/llms/pipeshift/base.py`  
| 
```
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
69
70
71
72
73
74
75
76
77
78
79
80
```
 | 
```
classPipeshift(OpenAILike):
"""
    Pipeshift LLM.

    Examples:
        `pip install llama-index-llms-pipeshift`

        ```python
        from llama_index.llms.pipeshift import Pipeshift

        # set api key in env or in llm
        # import os
        # os.environ["PIPESHIFT_API_KEY"] = "your api key"

        llm = Pipeshift(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct", api_key="your_api_key"


        resp = llm.complete("How fast is porsche gt3 rs?")
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
        api_key = api_key or os.environ.get("PIPESHIFT_API_KEY", None)
        try:
            validate_api_key_and_model(api_key, model)
            super().__init__(
                model=model,
                api_key=api_key,
                api_base=api_base,
                is_chat_model=is_chat_model,
                **kwargs,
            )
        except ValueError as e:
            raise ValueError(e)

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "Pipeshift"

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/pipeshift/#llama_index.llms.pipeshift.Pipeshift.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-pipeshift/llama_index/llms/pipeshift/base.py`  
| 
```
77
78
79
80
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "Pipeshift"

```
 |  
| --- | --- |  
options: members: - Pipeshift
