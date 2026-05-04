# Llamafile
##  LlamafileEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/llamafile/#llama_index.embeddings.llamafile.LlamafileEmbedding "Permanent link")
Bases: 
Class for llamafile embeddings.
llamafile lets you distribute and run large language models with a single file.
To get started, see: https://github.com/Mozilla-Ocho/llamafile
To use this class, you will need to first:
  1. Download a llamafile.
  2. Make the downloaded file executable: `chmod +x path/to/model.llamafile`
  3. Start the llamafile in server mode with embeddings enabled:
`./path/to/model.llamafile --server --nobrowser --embedding`

Source code in `llama-index-integrations/embeddings/llama-index-embeddings-llamafile/llama_index/embeddings/llamafile/base.py`  
| 
```
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
```
 | 
```
classLlamafileEmbedding(BaseEmbedding):
"""
    Class for llamafile embeddings.

    llamafile lets you distribute and run large language models with a
    single file.

    To get started, see: https://github.com/Mozilla-Ocho/llamafile

    To use this class, you will need to first:

    1. Download a llamafile.
    2. Make the downloaded file executable: `chmod +x path/to/model.llamafile`
    3. Start the llamafile in server mode with embeddings enabled:

        `./path/to/model.llamafile --server --nobrowser --embedding`

    """

    base_url: str = Field(
        description="base url of the llamafile server", default="http://localhost:8080"
    )

    request_timeout: float = Field(
        default=DEFAULT_REQUEST_TIMEOUT,
        description="The timeout for making http request to llamafile API server",
    )

    def__init__(
        self,
        base_url: str = "http://localhost:8080",
        callback_manager: Optional[CallbackManager] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            base_url=base_url,
            callback_manager=callback_manager or CallbackManager([]),
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "LlamafileEmbedding"

    def_get_query_embedding(self, query: str) -> Embedding:
        return self._get_text_embedding(query)

    async def_aget_query_embedding(self, query: str) -> Embedding:
        return await self._aget_text_embedding(query)

    def_get_text_embedding(self, text: str) -> Embedding:
"""
        Embed the input text synchronously.
        """
        request_body = {
            "content": text,
        }

        with httpx.Client(timeout=Timeout(self.request_timeout)) as client:
            response = client.post(
                url=f"{self.base_url}/embedding",
                headers={"Content-Type": "application/json"},
                json=request_body,
            )
            response.encoding = "utf-8"
            response.raise_for_status()

            return response.json()["embedding"]

    async def_aget_text_embedding(self, text: str) -> Embedding:
"""
        Embed the input text asynchronously.
        """
        request_body = {
            "content": text,
        }

        async with httpx.AsyncClient(timeout=Timeout(self.request_timeout)) as client:
            response = await client.post(
                url=f"{self.base_url}/embedding",
                headers={"Content-Type": "application/json"},
                json=request_body,
            )
            response.encoding = "utf-8"
            response.raise_for_status()

            return response.json()["embedding"]

    def_get_text_embeddings(self, texts: List[str]) -> List[Embedding]:
"""
        Embed the input texts synchronously.
        """
        request_body = {
            "content": texts,
        }

        with httpx.Client(timeout=Timeout(self.request_timeout)) as client:
            response = client.post(
                url=f"{self.base_url}/embedding",
                headers={"Content-Type": "application/json"},
                json=request_body,
            )
            response.encoding = "utf-8"
            response.raise_for_status()

            return [output["embedding"] for output in response.json()["results"]]

    async def_aget_text_embeddings(self, texts: List[str]) -> Embedding:
"""
        Embed the input text asynchronously.
        """
        request_body = {
            "content": texts,
        }

        async with httpx.AsyncClient(timeout=Timeout(self.request_timeout)) as client:
            response = await client.post(
                url=f"{self.base_url}/embedding",
                headers={"Content-Type": "application/json"},
                json=request_body,
            )
            response.encoding = "utf-8"
            response.raise_for_status()

            return [output["embedding"] for output in response.json()["results"]]

```
 |  
| --- | --- |  
options: members: - LlamafileEmbedding
