# Litellm
##  LiteLLMEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/litellm/#llama_index.embeddings.litellm.LiteLLMEmbedding "Permanent link")
Bases: 
Embedding class using the LiteLLM unified API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model_name`  |  Name of the embedding model to use. Examples include: - "text-embedding-3-small" - "text-embedding-3-large" - Any OpenAI-compatible embedding model exposed through LiteLLM.  |  _required_  |  
|  `api_key`  |  `Optional[str]`  |  API key for direct OpenAI-compatible requests. Not required when using a LiteLLM proxy with configured credentials.  |  _required_  |  
|  `api_base`  |  `Optional[str]`  |  Base URL of a LiteLLM proxy server  |  _required_  |  
|  `dimensions`  |  `Optional[int]`  |  Output embedding dimensionality. Supported for text-embedding-3 models.  |  _required_  |  
|  `timeout`  |  Timeout (in seconds) for embedding requests. Defaults to 60.  |  _required_  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-litellm/llama_index/embeddings/litellm/base.py`  
| 
```
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
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
```
 | 
```
classLiteLLMEmbedding(BaseEmbedding):
"""
    Embedding class using the LiteLLM unified API.

    Args:
        model_name (str): Name of the embedding model to use.
            Examples include:
            - "text-embedding-3-small"
            - "text-embedding-3-large"
            - Any OpenAI-compatible embedding model exposed through LiteLLM.

        api_key (Optional[str]): API key for direct OpenAI-compatible requests.
            Not required when using a LiteLLM proxy with configured credentials.

        api_base (Optional[str]): Base URL of a LiteLLM proxy server

        dimensions (Optional[int]): Output embedding dimensionality.
            Supported for text-embedding-3 models.

        timeout (int): Timeout (in seconds) for embedding requests.
            Defaults to 60.

    """

    model_name: str = Field(description="The name of the embedding model.")
    api_key: Optional[str] = Field(
        default=None,
        description="OpenAI key. If not provided, the proxy server must be configured with the key.",
    )
    api_base: Optional[str] = Field(
        default=None, description="The base URL of the LiteLLM proxy."
    )
    dimensions: Optional[int] = Field(
        default=None,
        description=(
            "The number of dimensions the resulting output embeddings should have. "
            "Only supported in text-embedding-3 and later models."
        ),
    )
    timeout: Optional[int] = Field(
        default=60, description="Timeout for each request.", ge=0
    )

    @classmethod
    defclass_name(cls) -> str:
        return "lite-llm"

    async def_aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)

    async def_aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)

    def_get_query_embedding(self, query: str) -> List[float]:
        embeddings = get_embeddings(
            api_key=self.api_key,
            api_base=self.api_base,
            model_name=self.model_name,
            dimensions=self.dimensions,
            timeout=self.timeout,
            input=[query],
        )
        return embeddings[0]

    def_get_text_embedding(self, text: str) -> List[float]:
        embeddings = get_embeddings(
            api_key=self.api_key,
            api_base=self.api_base,
            model_name=self.model_name,
            dimensions=self.dimensions,
            timeout=self.timeout,
            input=[text],
        )
        return embeddings[0]

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        return get_embeddings(
            api_key=self.api_key,
            api_base=self.api_base,
            model_name=self.model_name,
            dimensions=self.dimensions,
            timeout=self.timeout,
            input=texts,
        )

```
 |  
| --- | --- |  
options: members: - LiteLLMEmbedding
