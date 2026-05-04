# Text embeddings inference
##  TextEmbeddingsInference [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/text_embeddings_inference/#llama_index.embeddings.text_embeddings_inference.TextEmbeddingsInference "Permanent link")
Bases: 
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-text-embeddings-inference/llama_index/embeddings/text_embeddings_inference/base.py`  
| 
```
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
148
149
150
```
 | 
```
classTextEmbeddingsInference(BaseEmbedding):
    base_url: str = Field(
        default=DEFAULT_URL,
        description="Base URL for the text embeddings service.",
    )
    query_instruction: Optional[str] = Field(
        description="Instruction to prepend to query text."
    )
    text_instruction: Optional[str] = Field(
        description="Instruction to prepend to text."
    )
    timeout: float = Field(
        default=60.0,
        description="Timeout in seconds for the request.",
    )
    truncate_text: bool = Field(
        default=True,
        description="Whether to truncate text or not when generating embeddings.",
    )
    auth_token: Optional[Union[str, Callable[[str], str]]] = Field(
        default=None,
        description="Authentication token or authentication token generating function for authenticated requests",
    )
    endpoint: str = Field(
        default=DEFAULT_ENDPOINT,
        description="Endpoint for the text embeddings service.",
    )

    def__init__(
        self,
        model_name: str,
        base_url: str = DEFAULT_URL,
        text_instruction: Optional[str] = None,
        query_instruction: Optional[str] = None,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        timeout: float = 60.0,
        truncate_text: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        auth_token: Optional[Union[str, Callable[[str], str]]] = None,
        endpoint: str = DEFAULT_ENDPOINT,
    ):
        super().__init__(
            base_url=base_url,
            model_name=model_name,
            text_instruction=text_instruction,
            query_instruction=query_instruction,
            embed_batch_size=embed_batch_size,
            timeout=timeout,
            truncate_text=truncate_text,
            callback_manager=callback_manager,
            auth_token=auth_token,
            endpoint=endpoint,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "TextEmbeddingsInference"

    def_call_api(self, texts: List[str]) -> List[List[float]]:
        importhttpx

        headers = {"Content-Type": "application/json"}
        if self.auth_token is not None:
            if callable(self.auth_token):
                auth_token = self.auth_token(self.base_url)
            else:
                auth_token = self.auth_token
            headers["Authorization"] = f"Bearer {auth_token}"

        json_data = {"inputs": texts, "truncate": self.truncate_text}

        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}{self.endpoint}",
                headers=headers,
                json=json_data,
                timeout=self.timeout,
            )

        return response.json()

    async def_acall_api(self, texts: List[str]) -> List[List[float]]:
        importhttpx

        headers = {"Content-Type": "application/json"}
        if self.auth_token is not None:
            if callable(self.auth_token):
                auth_token = self.auth_token(self.base_url)
            else:
                auth_token = self.auth_token
            headers["Authorization"] = f"Bearer {auth_token}"
        json_data = {"inputs": texts, "truncate": self.truncate_text}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}{self.endpoint}",
                headers=headers,
                json=json_data,
                timeout=self.timeout,
            )

        return response.json()

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        query = format_query(query, self.model_name, self.query_instruction)
        return self._call_api([query])[0]

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        text = format_text(text, self.model_name, self.text_instruction)
        return self._call_api([text])[0]

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get text embeddings."""
        texts = [
            format_text(text, self.model_name, self.text_instruction) for text in texts
        ]
        return self._call_api(texts)

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""Get query embedding async."""
        query = format_query(query, self.model_name, self.query_instruction)
        return (await self._acall_api([query]))[0]

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Get text embedding async."""
        text = format_text(text, self.model_name, self.text_instruction)
        return (await self._acall_api([text]))[0]

    async def_aget_text_embeddings(self, texts: List[str]) -> List[Embedding]:
        texts = [
            format_text(text, self.model_name, self.text_instruction) for text in texts
        ]
        return await self._acall_api(texts)

```
 |  
| --- | --- |  
options: members: - TextEmbeddingsInference
