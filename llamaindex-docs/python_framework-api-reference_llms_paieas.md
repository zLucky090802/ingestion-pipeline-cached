# Paieas
##  PaiEas [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/paieas/#llama_index.llms.paieas.PaiEas "Permanent link")
Bases: 
PaiEas is a thin wrapper around the OpenAILike model that makes it compatible with Aliyun PAI-EAS(Elastic Algorithm Service) that provide effective llm services.
Source code in `llama-index-integrations/llms/llama-index-llms-paieas/llama_index/llms/paieas/base.py`  
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
```
 | 
```
classPaiEas(OpenAILike):
"""
    PaiEas is a thin wrapper around the OpenAILike model that makes it compatible with
    Aliyun PAI-EAS(Elastic Algorithm Service) that provide effective llm services.
    """

    def__init__(
        self,
        model: str = DEFAULT_MODEL_NAME,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        is_chat_model: bool = True,
        **kwargs: Any,
    ) -> None:
        api_key = api_key or os.environ.get("PAIEAS_API_KEY", None)
        api_base = api_base or os.environ.get("PAIEAS_API_BASE", None)
        super().__init__(
            model=model,
            api_key=api_key,
            api_base=urljoin(api_base, "v1"),
            is_chat_model=is_chat_model,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "PaiEasLLM"

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/paieas/#llama_index.llms.paieas.PaiEas.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-paieas/llama_index/llms/paieas/base.py`  
| 
```
34
35
36
37
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "PaiEasLLM"

```
 |  
| --- | --- |  
options: members: - PaiEas
