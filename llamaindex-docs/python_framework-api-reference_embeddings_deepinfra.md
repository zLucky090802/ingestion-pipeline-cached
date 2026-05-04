# Deepinfra
##  DeepInfraEmbeddingModel [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/deepinfra/#llama_index.embeddings.deepinfra.DeepInfraEmbeddingModel "Permanent link")
Bases: 
A wrapper class for accessing embedding models available via the DeepInfra API. This class allows for easy integration of DeepInfra embeddings into your projects, supporting both synchronous and asynchronous retrieval of text embeddings.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model_id`  |  Identifier for the model to be used for embeddings. Defaults to 'sentence-transformers/clip-ViT-B-32'.  |  `DEFAULT_MODEL_ID`  |  
|  `normalize`  |  `bool`  |  Flag to normalize embeddings post retrieval. Defaults to False.  |  `False`  |  
|  `api_token`  |  DeepInfra API token. If not provided,  |  `None`  |  
Examples:

```
>>> fromllama_index.embeddings.deepinfraimport DeepInfraEmbeddingModel
>>> model = DeepInfraEmbeddingModel()
>>> print(model.get_text_embedding("Hello, world!"))
[0.1, 0.2, 0.3, ...]

```

Source code in `llama-index-integrations/embeddings/llama-index-embeddings-deepinfra/llama_index/embeddings/deepinfra/base.py`  
| 
```
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
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
```
 | 
```
classDeepInfraEmbeddingModel(BaseEmbedding):
"""
    A wrapper class for accessing embedding models available via the DeepInfra API. This class allows for easy integration
    of DeepInfra embeddings into your projects, supporting both synchronous and asynchronous retrieval of text embeddings.

    Args:
        model_id (str): Identifier for the model to be used for embeddings. Defaults to 'sentence-transformers/clip-ViT-B-32'.
        normalize (bool): Flag to normalize embeddings post retrieval. Defaults to False.
        api_token (str): DeepInfra API token. If not provided,
        the token is fetched from the environment variable 'DEEPINFRA_API_TOKEN'.

    Examples:
        >>> from llama_index.embeddings.deepinfra import DeepInfraEmbeddingModel
        >>> model = DeepInfraEmbeddingModel()
        >>> print(model.get_text_embedding("Hello, world!"))
        [0.1, 0.2, 0.3, ...]

    """

"""model_id can be obtained from the DeepInfra website."""
    _model_id: str = PrivateAttr()
"""normalize flag to normalize embeddings post retrieval."""
    _normalize: bool = PrivateAttr()
"""api_token should be obtained from the DeepInfra website."""
    _api_token: str = PrivateAttr()
"""query_prefix is used to add a prefix to queries."""
    _query_prefix: str = PrivateAttr()
"""text_prefix is used to add a prefix to texts."""
    _text_prefix: str = PrivateAttr()

    def__init__(
        self,
        model_id: str = DEFAULT_MODEL_ID,
        normalize: bool = False,
        api_token: str = None,
        callback_manager: Optional[CallbackManager] = None,
        query_prefix: str = "",
        text_prefix: str = "",
        embed_batch_size: int = MAX_BATCH_SIZE,
    ) -> None:
"""
        Init params.
        """
        super().__init__(
            callback_manager=callback_manager, embed_batch_size=embed_batch_size
        )

        self._model_id = model_id
        self._normalize = normalize
        self._api_token = api_token or os.getenv(ENV_VARIABLE, None)
        self._query_prefix = query_prefix
        self._text_prefix = text_prefix

    def_post(self, data: List[str]) -> List[List[float]]:
"""
        Sends a POST request to the DeepInfra Inference API with the given data and returns the API response.
        Input data is chunked into batches to avoid exceeding the maximum batch size (1024).

        Args:
            data (List[str]): A list of strings to be embedded.

        Returns:
            dict: A dictionary containing embeddings from the API.

        """
        url = self.get_url()
        chunked_data = _chunk(data, self.embed_batch_size)
        embeddings = []
        for chunk in chunked_data:
            response = requests.post(
                url,
                json={
                    "inputs": chunk,
                },
                headers=self._get_headers(),
            )
            response.raise_for_status()
            embeddings.extend(response.json()["embeddings"])
        return embeddings

    defget_url(self):
"""
        Get DeepInfra API URL.
        """
        return f"{INFERENCE_URL}/{self._model_id}"

    async def_apost(self, data: List[str]) -> List[List[float]]:
"""
        Sends a POST request to the DeepInfra Inference API with the given data and returns the API response.
        Input data is chunked into batches to avoid exceeding the maximum batch size (1024).

        Args:
            data (List[str]): A list of strings to be embedded.
        Output:
            List[float]: A list of embeddings from the API.

        """
        url = self.get_url()
        chunked_data = _chunk(data, self.embed_batch_size)
        embeddings = []
        for chunk in chunked_data:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json={
                        "inputs": chunk,
                    },
                    headers=self._get_headers(),
                ) as resp:
                    response = await resp.json()
                    embeddings.extend(response["embeddings"])
        return embeddings

    def_get_query_embedding(self, query: str) -> List[float]:
"""
        Get query embedding.
        """
        return self._post(self._add_query_prefix([query]))[0]

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""
        Async get query embedding.
        """
        response = await self._apost(self._add_query_prefix([query]))
        return response[0]

    def_get_query_embeddings(self, queries: List[str]) -> List[List[float]]:
"""
        Get query embeddings.
        """
        return self._post(self._add_query_prefix(queries))

    async def_aget_query_embeddings(self, queries: List[str]) -> List[List[float]]:
"""
        Async get query embeddings.
        """
        return await self._apost(self._add_query_prefix(queries))

    def_get_text_embedding(self, text: str) -> List[float]:
"""
        Get text embedding.
        """
        return self._post(self._add_text_prefix([text]))[0]

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""
        Async get text embedding.
        """
        response = await self._apost(self._add_text_prefix([text]))
        return response[0]

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""
        Get text embedding.
        """
        return self._post(self._add_text_prefix(texts))

    async def_aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""
        Async get text embeddings.
        """
        return await self._apost(self._add_text_prefix(texts))

    def_add_query_prefix(self, queries: List[str]) -> List[str]:
"""
        Add query prefix to queries.
        """
        return (
            [self._query_prefix + query for query in queries]
            if self._query_prefix
            else queries
        )

    def_add_text_prefix(self, texts: List[str]) -> List[str]:
"""
        Add text prefix to texts.
        """
        return (
            [self._text_prefix + text for text in texts] if self._text_prefix else texts
        )

    def_get_headers(self) -> dict:
"""
        Get headers.
        """
        return {
            "Authorization": f"Bearer {self._api_token}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        }

```
 |  
| --- | --- |  
###  get_url [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/deepinfra/#llama_index.embeddings.deepinfra.DeepInfraEmbeddingModel.get_url "Permanent link")

```
get_url()

```

Get DeepInfra API URL.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-deepinfra/llama_index/embeddings/deepinfra/base.py`  
| 
```
106
107
108
109
110
```
 | 
```
defget_url(self):
"""
    Get DeepInfra API URL.
    """
    return f"{INFERENCE_URL}/{self._model_id}"

```
 |  
| --- | --- |  
options: members: - DeepInfraEmbeddingModel
