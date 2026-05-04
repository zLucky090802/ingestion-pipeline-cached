# Llama api
##  LlamaAPI [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/llama_api/#llama_index.llms.llama_api.LlamaAPI "Permanent link")
Bases: 
LlamaAPI LLM.
Examples:
`pip install llama-index-llms-llama-api`

```
fromllama_index.llms.llama_apiimport LlamaAPI

# Obtain an API key from https://www.llama-api.com/
api_key = "your-api-key"

llm = LlamaAPI(model="llama3.1-8b", context_window=128000, is_function_calling_model=True, api_key=api_key)

# Call the complete method with a prompt
resp = llm.complete("Paul Graham is ")

print(resp)

```

Source code in `llama-index-integrations/llms/llama-index-llms-llama-api/llama_index/llms/llama_api/base.py`  
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
```
 | 
```
classLlamaAPI(OpenAILike):
"""
    LlamaAPI LLM.

    Examples:
        `pip install llama-index-llms-llama-api`

        ```python
        from llama_index.llms.llama_api import LlamaAPI

        # Obtain an API key from https://www.llama-api.com/
        api_key = "your-api-key"

        llm = LlamaAPI(model="llama3.1-8b", context_window=128000, is_function_calling_model=True, api_key=api_key)

        # Call the complete method with a prompt
        resp = llm.complete("Paul Graham is ")

        print(resp)
        ```

    """

    model: str = Field(
        default="llama3.1-8b",
        description=LLMMetadata.model_fields["model_name"].description,
    )

    api_base: str = Field(
        default="https://api.llmapi.com/",
        description="The base URL for OpenAI API.",
    )

    is_chat_model: bool = Field(
        default=True,
        description=LLMMetadata.model_fields["is_chat_model"].description,
    )
    is_function_calling_model: bool = Field(
        default=False,
        description=LLMMetadata.model_fields["is_function_calling_model"].description,
    )

    @classmethod
    defclass_name(cls) -> str:
        return "llama_api_llm"

```
 |  
| --- | --- |  
options: members: - LlamaAPI
