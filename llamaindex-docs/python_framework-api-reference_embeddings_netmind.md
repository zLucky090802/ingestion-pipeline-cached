# Netmind
##  NetmindEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/netmind/#llama_index.embeddings.netmind.NetmindEmbedding "Permanent link")
Bases: 
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-netmind/llama_index/embeddings/netmind/base.py`  
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
```
 | 
```
classNetmindEmbedding(BaseEmbedding):
    api_base: str = Field(
        default="https://api.netmind.ai/inference-api/openai/v1",
        description="The base URL for the Netmind API.",
    )
    api_key: str = Field(
        default="",
        description="The API key for the Netmind API. If not set, will attempt to use the NETMIND_API_KEY environment variable.",
    )
    timeout: float = Field(
        default=120, description="The timeout for the API request in seconds.", ge=0
    )
    max_retries: int = Field(
        default=3,
        description="The maximum number of retries for the API request.",
        ge=0,
    )

    def__init__(
        self,
        model_name: str,
        timeout: Optional[float] = 120,
        max_retries: Optional[int] = 3,
        api_key: Optional[str] = None,
        api_base: str = "https://api.netmind.ai/inference-api/openai/v1",
        **kwargs: Any,
    ) -> None:
        api_key = api_key or os.environ.get("NETMIND_API_KEY", None)
        super().__init__(
            model_name=model_name,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )
        self._client = OpenAI(
            api_key=api_key,
            base_url=self.api_base,
            timeout=timeout,
            max_retries=max_retries,
        )
        self._aclient = AsyncOpenAI(
            api_key=api_key,
            base_url=self.api_base,
            timeout=timeout,
            max_retries=max_retries,
        )

    def_get_text_embedding(self, text: str) -> Embedding:
"""Get text embedding."""
        return (
            self._client.embeddings.create(
                input=[text],
                model=self.model_name,
            )
            .data[0]
            .embedding
        )

    def_get_query_embedding(self, query: str) -> Embedding:
"""Get query embedding."""
        return (
            self._client.embeddings.create(
                input=[query],
                model=self.model_name,
            )
            .data[0]
            .embedding
        )

    def_get_text_embeddings(self, texts: List[str]) -> List[Embedding]:
"""Get text embeddings."""
        data = self._client.embeddings.create(
            input=texts,
            model=self.model_name,
        ).data
        return [d.embedding for d in data]

    async def_aget_text_embedding(self, text: str) -> Embedding:
"""Async get text embedding."""
        return (
            (await self._aclient.embeddings.create(input=[text], model=self.model_name))
            .data[0]
            .embedding
        )

    async def_aget_query_embedding(self, query: str) -> Embedding:
"""Async get query embedding."""
        return (
            (
                await self._aclient.embeddings.create(
                    input=[query], model=self.model_name
                )
            )
            .data[0]
            .embedding
        )

    async def_aget_text_embeddings(self, texts: List[str]) -> List[Embedding]:
"""Async get text embeddings."""
        data = (
            await self._aclient.embeddings.create(
                input=texts,
                model=self.model_name,
            )
        ).data
        return [d.embedding for d in data]

```
 |  
| --- | --- |  
options: members: - NetmindEmbedding
