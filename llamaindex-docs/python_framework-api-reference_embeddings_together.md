# Together
##  TogetherEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/together/#llama_index.embeddings.together.TogetherEmbedding "Permanent link")
Bases: 
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-together/llama_index/embeddings/together/base.py`  
| 
```
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
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
```
 | 
```
classTogetherEmbedding(BaseEmbedding):
    api_base: str = Field(
        default="https://api.together.xyz/v1",
        description="The base URL for the Together API.",
    )
    api_key: str = Field(
        default="",
        description="The API key for the Together API. If not set, will attempt to use the TOGETHER_API_KEY environment variable.",
    )

    def__init__(
        self,
        model_name: str,
        api_key: Optional[str] = None,
        api_base: str = "https://api.together.xyz/v1",
        **kwargs: Any,
    ) -> None:
        api_key = api_key or os.environ.get("TOGETHER_API_KEY", None)
        super().__init__(
            model_name=model_name,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )

    def_generate_embedding(self, text: str, model_api_string: str) -> Embedding:
"""
        Generate embeddings from Together API.

        Args:
            text: str. An input text sentence or document.
            model_api_string: str. An API string for a specific embedding model of your choice.

        Returns:
            embeddings: a list of float numbers. Embeddings correspond to your given text.

        """
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        session = requests.session()
        while True:
            response = session.post(
                self.api_base.strip("/") + "/embeddings",
                headers=headers,
                json={"input": text, "model": model_api_string},
            )
            if response.status_code != 200:
                if response.status_code == 429:
"""Rate limit exceeded, wait for reset"""
                    reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                    if reset_time  0:
                        time.sleep(reset_time)
                        continue
                    else:
"""Rate limit reset time has passed, retry immediately"""
                        continue

""" Handle other non-200 status codes """
                raise ValueError(
                    f"Request failed with status code {response.status_code}: {response.text}"
                )

            return response.json()["data"][0]["embedding"]

    async def_agenerate_embedding(self, text: str, model_api_string: str) -> Embedding:
"""
        Async generate embeddings from Together API.

        Args:
            text: str. An input text sentence or document.
            model_api_string: str. An API string for a specific embedding model of your choice.

        Returns:
            embeddings: a list of float numbers. Embeddings correspond to your given text.

        """
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        async with httpx.AsyncClient() as client:
            while True:
                response = await client.post(
                    self.api_base.strip("/") + "/embeddings",
                    headers=headers,
                    json={"input": text, "model": model_api_string},
                )
                if response.status_code != 200:
                    if response.status_code == 429:
"""Rate limit exceeded, wait for reset"""
                        reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                        if reset_time  0:
                            await asyncio.sleep(reset_time)
                            continue
                        else:
"""Rate limit reset time has passed, retry immediately"""
                            continue

""" Handle other non-200 status codes"""
                    raise ValueError(
                        f"Request failed with status code {response.status_code}: {response.text}"
                    )

                return response.json()["data"][0]["embedding"]

    def_get_text_embedding(self, text: str) -> Embedding:
"""Get text embedding."""
        return self._generate_embedding(text, self.model_name)

    def_get_query_embedding(self, query: str) -> Embedding:
"""Get query embedding."""
        return self._generate_embedding(query, self.model_name)

    def_get_text_embeddings(self, texts: List[str]) -> List[Embedding]:
"""Get text embeddings."""
        return [self._generate_embedding(text, self.model_name) for text in texts]

    async def_aget_text_embedding(self, text: str) -> Embedding:
"""Async get text embedding."""
        return await self._agenerate_embedding(text, self.model_name)

    async def_aget_query_embedding(self, query: str) -> Embedding:
"""Async get query embedding."""
        return await self._agenerate_embedding(query, self.model_name)

    async def_aget_text_embeddings(self, texts: List[str]) -> List[Embedding]:
"""Async get text embeddings."""
        return await asyncio.gather(
            *[self._agenerate_embedding(text, self.model_name) for text in texts]
        )

```
 |  
| --- | --- |  
options: members: - TogetherEmbedding
