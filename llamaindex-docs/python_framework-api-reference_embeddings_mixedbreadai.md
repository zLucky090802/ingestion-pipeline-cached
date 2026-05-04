# Mixedbreadai
##  MixedbreadAIEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/mixedbreadai/#llama_index.embeddings.mixedbreadai.MixedbreadAIEmbedding "Permanent link")
Bases: 
Class to get embeddings using the mixedbread ai embedding API with models such as 'mixedbread-ai/mxbai-embed-large-v1'.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  `Optional[str]`  |  mixedbread ai API key. Defaults to None.  |  `None`  |  
|  `model_name`  |  Model for embedding. Defaults to "mixedbread-ai/mxbai-embed-large-v1".  |  `'mixedbread-ai/mxbai-embed-large-v1'`  |  
|  `encoding_format`  |  `EncodingFormat`  |  Encoding format for embeddings. Defaults to "float".  |  `'float'`  |  
|  `normalized`  |  `bool`  |  Whether to normalize the embeddings. Defaults to True.  |  `True`  |  
|  `dimensions`  |  `Optional[int]`  |  Number of dimensions for embeddings. Only applicable for models with matryoshka support.  |  `None`  |  
|  `prompt`  |  `Optional[str]`  |  An optional prompt to provide context to the model.  |  `None`  |  
|  `embed_batch_size`  |  `Optional[int]`  |  The batch size for embedding calls. Defaults to 128.  |  `None`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.base.CallbackManager\)")]`  |  Manager for handling callbacks.  |  `None`  |  
|  `timeout`  |  `Optional[float]`  |  Timeout for API calls.  |  `None`  |  
|  `max_retries`  |  `Optional[int]`  |  Maximum number of retries for API calls.  |  `None`  |  
|  `httpx_client`  |  `Optional[Client]`  |  Custom HTTPX client.  |  `None`  |  
|  `httpx_async_client`  |  `Optional[AsyncClient]`  |  Custom asynchronous HTTPX client.  |  `None`  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-mixedbreadai/llama_index/embeddings/mixedbreadai/base.py`  
| 
```
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
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
```
 | 
```
classMixedbreadAIEmbedding(BaseEmbedding):
"""
    Class to get embeddings using the mixedbread ai embedding API with models such as 'mixedbread-ai/mxbai-embed-large-v1'.

    Args:
        api_key (Optional[str]): mixedbread ai API key. Defaults to None.
        model_name (str): Model for embedding. Defaults to "mixedbread-ai/mxbai-embed-large-v1".
        encoding_format (EncodingFormat): Encoding format for embeddings. Defaults to "float".
        normalized (bool): Whether to normalize the embeddings. Defaults to True.
        dimensions (Optional[int]): Number of dimensions for embeddings. Only applicable for models with matryoshka support.
        prompt (Optional[str]): An optional prompt to provide context to the model.
        embed_batch_size (Optional[int]): The batch size for embedding calls. Defaults to 128.
        callback_manager (Optional[CallbackManager]): Manager for handling callbacks.
        timeout (Optional[float]): Timeout for API calls.
        max_retries (Optional[int]): Maximum number of retries for API calls.
        httpx_client (Optional[httpx.Client]): Custom HTTPX client.
        httpx_async_client (Optional[httpx.AsyncClient]): Custom asynchronous HTTPX client.

    """

    api_key: str = Field(description="The mixedbread ai API key.", min_length=1)
    model_name: str = Field(
        default="mixedbread-ai/mxbai-embed-large-v1",
        description="Model to use for embeddings.",
        min_length=1,
    )
    encoding_format: EncodingFormat = Field(
        default="float", description="Encoding format for the embeddings."
    )
    normalized: bool = Field(
        default=True, description="Whether to normalize the embeddings."
    )
    dimensions: Optional[int] = Field(
        default=None,
        description="Number of dimensions for embeddings. Only applicable for models with matryoshka support.",
        gt=0,
    )
    prompt: Optional[str] = Field(
        default=None,
        description="An optional prompt to provide context to the model.",
        min_length=1,
    )
    embed_batch_size: int = Field(
        default=128, description="The batch size for embedding calls.", gt=0, le=256
    )

    _client: Mixedbread = PrivateAttr()
    _async_client: AsyncMixedbread = PrivateAttr()

    def__init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "mixedbread-ai/mxbai-embed-large-v1",
        encoding_format: EncodingFormat = "float",
        normalized: bool = True,
        dimensions: Optional[int] = None,
        prompt: Optional[str] = None,
        embed_batch_size: Optional[int] = None,
        callback_manager: Optional[CallbackManager] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        httpx_client: Optional[httpx.Client] = None,
        httpx_async_client: Optional[httpx.AsyncClient] = None,
        **kwargs: Any,
    ):
        if embed_batch_size is None:
            embed_batch_size = 128  # Default batch size for mixedbread ai

        try:
            api_key = api_key or os.environ["MXBAI_API_KEY"]
        except KeyError:
            raise ValueError(
                "Must pass in mixedbread ai API key or "
                "specify via MXBAI_API_KEY environment variable "
            )

        super().__init__(
            api_key=api_key,
            model_name=model_name,
            encoding_format=encoding_format,
            normalized=normalized,
            dimensions=dimensions,
            prompt=prompt,
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            **kwargs,
        )

        self._client = Mixedbread(
            api_key=api_key,
            timeout=timeout,
            http_client=httpx_client,
            max_retries=max_retries if max_retries is not None else DEFAULT_MAX_RETRIES,
        )
        self._async_client = AsyncMixedbread(
            api_key=api_key,
            timeout=timeout,
            http_client=httpx_async_client,
            max_retries=max_retries if max_retries is not None else DEFAULT_MAX_RETRIES,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "MixedbreadAIEmbedding"

    def_get_embedding(self, texts: List[str]) -> List[List[float]]:
"""
        Get embeddings for a list of texts using the mixedbread ai API.

        Args:
            texts (List[str]): List of texts to embed.

        Returns:
            List[List[float]]: List of embeddings.

        """
        response = self._client.embed(
            model=self.model_name,
            input=texts,
            encoding_format=self.encoding_format,
            normalized=self.normalized,
            dimensions=self.dimensions,
            prompt=self.prompt,
        )
        return [item.embedding for item in response.data]

    async def_aget_embedding(self, texts: List[str]) -> List[List[float]]:
"""
        Asynchronously get embeddings for a list of texts using the mixedbread ai API.

        Args:
            texts (List[str]): List of texts to embed.

        Returns:
            List[List[float]]: List of embeddings.

        """
        response = await self._async_client.embed(
            model=self.model_name,
            input=texts,
            encoding_format=self.encoding_format,
            normalized=self.normalized,
            dimensions=self.dimensions,
            prompt=self.prompt,
        )
        return [item.embedding for item in response.data]

    def_get_query_embedding(self, query: str) -> List[float]:
"""
        Get embedding for a query using the mixedbread ai API.

        Args:
            query (str): Query text.

        Returns:
            List[float]: Embedding for the query.

        """
        return self._get_embedding([query])[0]

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""
        Asynchronously get embedding for a query using the mixedbread ai API.

        Args:
            query (str): Query text.

        Returns:
            List[float]: Embedding for the query.

        """
        r = await self._aget_embedding([query])
        return r[0]

    def_get_text_embedding(self, text: str) -> List[float]:
"""
        Get embedding for a text using the mixedbread ai API.

        Args:
            text (str): Text to embed.

        Returns:
            List[float]: Embedding for the text.

        """
        return self._get_embedding([text])[0]

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""
        Asynchronously get embedding for a text using the mixedbread ai API.

        Args:
            text (str): Text to embed.

        Returns:
            List[float]: Embedding for the text.

        """
        r = await self._aget_embedding([text])
        return r[0]

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""
        Get embeddings for multiple texts using the mixedbread ai API.

        Args:
            texts (List[str]): List of texts to embed.

        Returns:
            List[List[float]]: List of embeddings.

        """
        return self._get_embedding(texts)

    async def_aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""
        Asynchronously get embeddings for multiple texts using the mixedbread ai API.

        Args:
            texts (List[str]): List of texts to embed.

        Returns:
            List[List[float]]: List of embeddings.

        """
        return await self._aget_embedding(texts)

```
 |  
| --- | --- |  
options: members: - MixedbreadAIEmbedding
