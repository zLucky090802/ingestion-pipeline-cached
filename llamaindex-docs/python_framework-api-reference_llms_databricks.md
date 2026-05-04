# Databricks
##  Databricks [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/databricks/#llama_index.llms.databricks.Databricks "Permanent link")
Bases: 
Databricks LLM.
Examples:
`pip install llama-index-llms-databricks`

```
fromllama_index.llms.databricksimport Databricks

# Set up the Databricks class with the required model, API key and serving endpoint
llm = Databricks(model="databricks-dbrx-instruct", api_key="your_api_key", api_base="https://[your-work-space].cloud.databricks.com/serving-endpoints")

# Call the complete method with a query
response = llm.complete("Explain the importance of open source LLMs")

print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-databricks/llama_index/llms/databricks/base.py`  
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
52
53
54
55
56
57
```
 | 
```
classDatabricks(OpenAILike):
"""
    Databricks LLM.

    Examples:
        `pip install llama-index-llms-databricks`

        ```python
        from llama_index.llms.databricks import Databricks

        # Set up the Databricks class with the required model, API key and serving endpoint
        llm = Databricks(model="databricks-dbrx-instruct", api_key="your_api_key", api_base="https://[your-work-space].cloud.databricks.com/serving-endpoints")

        # Call the complete method with a query
        response = llm.complete("Explain the importance of open source LLMs")

        print(response)
        ```

    """

    def__init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        is_chat_model: bool = True,
        **kwargs: Any,
    ) -> None:
        api_key = api_key or os.environ.get("DATABRICKS_TOKEN", None)
        api_base = api_base or os.environ.get("DATABRICKS_SERVING_ENDPOINT", None)
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
        return "Databricks"

    def_get_model_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
"""Get the kwargs that need to be provided to the model invocation."""
        # Fix the input to work with the Databricks API
        if "tool_choice" in kwargs and "tools" not in kwargs:
            del kwargs["tool_choice"]

        return super()._get_model_kwargs(**kwargs)

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/databricks/#llama_index.llms.databricks.Databricks.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-databricks/llama_index/llms/databricks/base.py`  
| 
```
46
47
48
49
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "Databricks"

```
 |  
| --- | --- |  
options: members: - Databricks
