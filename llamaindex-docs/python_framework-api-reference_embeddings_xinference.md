# Xinference
##  XinferenceEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/xinference/#llama_index.embeddings.xinference.XinferenceEmbedding "Permanent link")
Bases: 
Class for Xinference embeddings.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-xinference/llama_index/embeddings/xinference/base.py`  
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
```
 | 
```
classXinferenceEmbedding(BaseEmbedding):
"""Class for Xinference embeddings."""

    model_uid: str = Field(
        default="unknown",
        description="The Xinference model uid to use.",
    )
    base_url: str = Field(
        default="http://localhost:9997",
        description="The Xinference base url to use.",
    )
    timeout: float = Field(
        default=60.0,
        description="Timeout in seconds for the request.",
    )

    def__init__(
        self,
        model_uid: str,
        base_url: str = "http://localhost:9997",
        timeout: float = 60.0,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            model_uid=model_uid,
            base_url=base_url,
            timeout=timeout,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "XinferenceEmbedding"

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

    defget_general_text_embedding(self, prompt: str) -> List[float]:
"""Get Xinference embeddings."""
        headers = {"Content-Type": "application/json"}
        json_data = {"input": prompt, "model": self.model_uid}
        response = requests.post(
            url=f"{self.base_url}/v1/embeddings",
            headers=headers,
            json=json_data,
            timeout=self.timeout,
        )
        response.encoding = "utf-8"
        if response.status_code != 200:
            raise Exception(
                f"Xinference call failed with status code {response.status_code}."
                f"Details: {response.text}"
            )
        return response.json()["data"][0]["embedding"]

    async defaget_general_text_embedding(self, prompt: str) -> List[float]:
"""Asynchronously get Xinference embeddings."""
        headers = {"Content-Type": "application/json"}
        json_data = {"input": prompt, "model": self.model_uid}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"{self.base_url}/v1/embeddings",
                headers=headers,
                json=json_data,
                timeout=self.timeout,
            ) as response:
                if response.status != 200:
                    raise Exception(
                        f"Xinference call failed with status code {response.status}."
                    )
                data = await response.json()
                return data["data"][0]["embedding"]

```
 |  
| --- | --- |  
###  get_general_text_embedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/xinference/#llama_index.embeddings.xinference.XinferenceEmbedding.get_general_text_embedding "Permanent link")

```
get_general_text_embedding(prompt: ) -> [float]

```

Get Xinference embeddings.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-xinference/llama_index/embeddings/xinference/base.py`  
| 
```
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
```
 | 
```
defget_general_text_embedding(self, prompt: str) -> List[float]:
"""Get Xinference embeddings."""
    headers = {"Content-Type": "application/json"}
    json_data = {"input": prompt, "model": self.model_uid}
    response = requests.post(
        url=f"{self.base_url}/v1/embeddings",
        headers=headers,
        json=json_data,
        timeout=self.timeout,
    )
    response.encoding = "utf-8"
    if response.status_code != 200:
        raise Exception(
            f"Xinference call failed with status code {response.status_code}."
            f"Details: {response.text}"
        )
    return response.json()["data"][0]["embedding"]

```
 |  
| --- | --- |  
###  aget_general_text_embedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/xinference/#llama_index.embeddings.xinference.XinferenceEmbedding.aget_general_text_embedding "Permanent link")

```
aget_general_text_embedding(prompt: ) -> [float]

```

Asynchronously get Xinference embeddings.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-xinference/llama_index/embeddings/xinference/base.py`  
| 
```
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
```
 | 
```
async defaget_general_text_embedding(self, prompt: str) -> List[float]:
"""Asynchronously get Xinference embeddings."""
    headers = {"Content-Type": "application/json"}
    json_data = {"input": prompt, "model": self.model_uid}
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"{self.base_url}/v1/embeddings",
            headers=headers,
            json=json_data,
            timeout=self.timeout,
        ) as response:
            if response.status != 200:
                raise Exception(
                    f"Xinference call failed with status code {response.status}."
                )
            data = await response.json()
            return data["data"][0]["embedding"]

```
 |  
| --- | --- |  
options: members: - XinferenceEmbedding
