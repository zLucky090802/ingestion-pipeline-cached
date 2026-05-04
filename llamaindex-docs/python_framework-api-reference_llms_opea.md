# Opea
##  OPEA [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/opea/#llama_index.llms.opea.OPEA "Permanent link")
Bases: 
Adapter for a OPEA LLM.
Examples:
`pip install llama-index-llms-opea`

```
fromllama_index.llms.opeaimport OPEA

llm = OPEA(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
    api_base="http://localhost:8080/v1",
)

```

Source code in `llama-index-integrations/llms/llama-index-llms-opea/llama_index/llms/opea/base.py`  
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
```
 | 
```
classOPEA(OpenAILike):
"""
    Adapter for a OPEA LLM.

    Examples:
        `pip install llama-index-llms-opea`

        ```python
        from llama_index.llms.opea import OPEA

        llm = OPEA(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct",
            api_base="http://localhost:8080/v1",

        ```

    """

    is_chat_model: bool = Field(
        default=True,
        description=LLMMetadata.model_fields["is_chat_model"].description,
    )

    @classmethod
    defclass_name(cls) -> str:
        return "OPEA"

```
 |  
| --- | --- |  
options: members: - OPEA
