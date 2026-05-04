# Zhipuai
##  ZhipuAIEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/zhipuai/#llama_index.embeddings.zhipuai.ZhipuAIEmbedding "Permanent link")
Bases: 
ZhipuAI LLM.
Visit https://open.bigmodel.cn to get more information about ZhipuAI.
Examples:
`pip install llama-index-embeddings-zhipuai`

```
fromllama_index.embeddings.zhipuaiimport ZhipuAIEmbedding

embedding = ZhipuAIEmbedding(model="embedding-2", api_key="YOUR API KEY")

response = embedding.get_general_text_embedding("who are you?")
print(response)

```

Source code in `llama-index-integrations/embeddings/llama-index-embeddings-zhipuai/llama_index/embeddings/zhipuai/base.py`  
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
```
 | 
```
classZhipuAIEmbedding(BaseEmbedding):
"""
    ZhipuAI LLM.

    Visit https://open.bigmodel.cn to get more information about ZhipuAI.

    Examples:
        `pip install llama-index-embeddings-zhipuai`

        ```python
        from llama_index.embeddings.zhipuai import ZhipuAIEmbedding

        embedding = ZhipuAIEmbedding(model="embedding-2", api_key="YOUR API KEY")

        response = embedding.get_general_text_embedding("who are you?")
        print(response)
        ```

    """

    model: str = Field(description="The ZhipuAI model to use.")
    api_key: Optional[str] = Field(
        default=None,
        description="The API key to use for the ZhipuAI API.",
    )
    dimensions: Optional[int] = Field(
        default=1024,
        description=(
            "The number of dimensions the resulting output embeddings should have. "
            "Only supported in embedding-3 and later models. embedding-2 is fixed at 1024."
        ),
    )
    timeout: Optional[float] = Field(
        default=None,
        description="The timeout to use for the ZhipuAI API.",
    )
    _client: Optional[ZhipuAIClient] = PrivateAttr()

    def__init__(
        self,
        model: str,
        api_key: str,
        dimensions: Optional[int] = 1024,
        timeout: Optional[int] = None,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            model=model,
            dimensions=dimensions,
            timeout=timeout,
            callback_manager=callback_manager,
            **kwargs,
        )

        self._client = ZhipuAIClient(api_key=api_key)

    @classmethod
    defclass_name(cls) -> str:
        return "ZhipuAIEmbedding"

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        return self.get_general_text_embedding(query)

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""The asynchronous version of _get_query_embedding."""
        return await self.aget_general_text_embedding(query)

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        return self.get_general_text_embedding(text)

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Asynchronously get text embedding."""
        return await self.aget_general_text_embedding(text)

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get text embeddings."""
        embeddings_list: List[List[float]] = []
        for text in texts:
            embeddings = self.get_general_text_embedding(text)
            embeddings_list.append(embeddings)
        return embeddings_list

    async def_aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Asynchronously get text embeddings."""
        return await asyncio.gather(
            *[self.aget_general_text_embedding(text) for text in texts]
        )

    defget_general_text_embedding(self, text: str) -> List[float]:
"""Get ZhipuAI embeddings."""
        response = self._client.embeddings.create(
            model=self.model,
            input=text,
            dimensions=self.dimensions,
            timeout=self.timeout,
        )
        return response.data[0].embedding

    async defaget_general_text_embedding(self, text: str) -> List[float]:
"""Asynchronously get ZhipuAI embeddings."""
        response = await asyncio.to_thread(
            self._client.embeddings.create,
            model=self.model,
            input=text,
            dimensions=self.dimensions,
            timeout=self.timeout,
        )
        return response.data[0].embedding

```
 |  
| --- | --- |  
###  get_general_text_embedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/zhipuai/#llama_index.embeddings.zhipuai.ZhipuAIEmbedding.get_general_text_embedding "Permanent link")

```
get_general_text_embedding(text: ) -> [float]

```

Get ZhipuAI embeddings.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-zhipuai/llama_index/embeddings/zhipuai/base.py`  
| 
```
100
101
102
103
104
105
106
107
108
```
 | 
```
defget_general_text_embedding(self, text: str) -> List[float]:
"""Get ZhipuAI embeddings."""
    response = self._client.embeddings.create(
        model=self.model,
        input=text,
        dimensions=self.dimensions,
        timeout=self.timeout,
    )
    return response.data[0].embedding

```
 |  
| --- | --- |  
###  aget_general_text_embedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/zhipuai/#llama_index.embeddings.zhipuai.ZhipuAIEmbedding.aget_general_text_embedding "Permanent link")

```
aget_general_text_embedding(text: ) -> [float]

```

Asynchronously get ZhipuAI embeddings.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-zhipuai/llama_index/embeddings/zhipuai/base.py`  
| 
```
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
```
 | 
```
async defaget_general_text_embedding(self, text: str) -> List[float]:
"""Asynchronously get ZhipuAI embeddings."""
    response = await asyncio.to_thread(
        self._client.embeddings.create,
        model=self.model,
        input=text,
        dimensions=self.dimensions,
        timeout=self.timeout,
    )
    return response.data[0].embedding

```
 |  
| --- | --- |  
options: members: - ZhipuAIEmbedding
