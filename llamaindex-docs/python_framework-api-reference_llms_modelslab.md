# Modelslab
##  ModelsLabLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/modelslab/#llama_index.llms.modelslab.ModelsLabLLM "Permanent link")
Bases: 
ModelsLab LLM integration for LlamaIndex.
Provides uncensored Llama 3.1 language models via ModelsLab's OpenAI-compatible API. Suitable for RAG pipelines, agents, and workflows requiring unrestricted language generation with a 128K token context window.
Models
  * `llama-3.1-8b-uncensored` — fast, efficient (default)
  * `llama-3.1-70b-uncensored` — higher quality, deeper reasoning


Examples:
`pip install llama-index-llms-modelslab`

```
fromllama_index.llms.modelslabimport ModelsLabLLM

# Set MODELSLAB_API_KEY env var or pass api_key directly
llm = ModelsLabLLM(
    model="llama-3.1-8b-uncensored",
    api_key="your-modelslab-api-key",
)

resp = llm.complete("Explain transformers in simple terms.")
print(resp)

```

Use in a RAG pipeline::

```
fromllama_index.coreimport VectorStoreIndex, SimpleDirectoryReader
fromllama_index.llms.modelslabimport ModelsLabLLM
fromllama_index.coreimport Settings

Settings.llm = ModelsLabLLM(model="llama-3.1-70b-uncensored")

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("What is the main topic?")

```

Get your API key at: https://modelslab.com API docs: https://docs.modelslab.com/uncensored-chat
Source code in `llama-index-integrations/llms/llama-index-llms-modelslab/llama_index/llms/modelslab/base.py`  
| 
```
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
81
82
83
84
85
86
87
88
```
 | 
```
classModelsLabLLM(OpenAILike):
"""
    ModelsLab LLM integration for LlamaIndex.

    Provides uncensored Llama 3.1 language models via ModelsLab's
    OpenAI-compatible API. Suitable for RAG pipelines, agents, and
    workflows requiring unrestricted language generation with a
    128K token context window.

    Models:
        - ``llama-3.1-8b-uncensored`` — fast, efficient (default)
        - ``llama-3.1-70b-uncensored`` — higher quality, deeper reasoning

    Examples:
        ``pip install llama-index-llms-modelslab``

        ```python
        from llama_index.llms.modelslab import ModelsLabLLM

        # Set MODELSLAB_API_KEY env var or pass api_key directly
        llm = ModelsLabLLM(
            model="llama-3.1-8b-uncensored",
            api_key="your-modelslab-api-key",


        resp = llm.complete("Explain transformers in simple terms.")
        print(resp)
        ```

        Use in a RAG pipeline::

        ```python
        from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
        from llama_index.llms.modelslab import ModelsLabLLM
        from llama_index.core import Settings

        Settings.llm = ModelsLabLLM(model="llama-3.1-70b-uncensored")

        documents = SimpleDirectoryReader("data").load_data()
        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine()
        response = query_engine.query("What is the main topic?")
        ```

    Get your API key at: https://modelslab.com
    API docs: https://docs.modelslab.com/uncensored-chat

    """

    def__init__(
        self,
        model: str = "llama-3.1-8b-uncensored",
        api_key: Optional[str] = None,
        api_base: str = MODELSLAB_API_BASE,
        is_chat_model: bool = True,
        is_function_calling_model: bool = False,
        context_window: int = 131072,
        **kwargs: Any,
    ) -> None:
        api_key = api_key or os.environ.get("MODELSLAB_API_KEY")
        if not api_key:
            raise ValueError(
                "ModelsLab API key not found. "
                "Set the MODELSLAB_API_KEY environment variable or pass api_key directly. "
                "Get your key at https://modelslab.com"
            )
        super().__init__(
            model=model,
            api_key=api_key,
            api_base=api_base,
            is_chat_model=is_chat_model,
            is_function_calling_model=is_function_calling_model,
            context_window=context_window,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "ModelsLabLLM"

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/modelslab/#llama_index.llms.modelslab.ModelsLabLLM.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-modelslab/llama_index/llms/modelslab/base.py`  
| 
```
85
86
87
88
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "ModelsLabLLM"

```
 |  
| --- | --- |  
options: members: - ModelsLabLLM
