# Heroku
##  HerokuEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/heroku/#llama_index.embeddings.heroku.HerokuEmbedding "Permanent link")
Bases: 
Heroku Managed Inference Embeddings Integration.
This class provides an interface to Heroku's Managed Inference API for embeddings. It connects to your Heroku app's embedding endpoint for embedding models. For more information about Heroku's embedding endpoint see: https://devcenter.heroku.com/articles/heroku-inference-api-model-cohere-embed-multilingual
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model`  |  The model to use. If not provided, will use EMBEDDING_MODEL_ID.  |  `None`  |  
|  `api_key`  |  The API key for Heroku embedding. Defaults to EMBEDDING_KEY.  |  `None`  |  
|  `base_url`  |  The base URL for embedding. Defaults to EMBEDDING_URL.  |  `None`  |  
|  `timeout`  |  `float`  |  Timeout for requests in seconds. Defaults to 60.0.  |  `60.0`  |  
|  `**kwargs`  |  Additional keyword arguments.  |  
Environment Variables
  * EMBEDDING_KEY: The API key for Heroku embedding
  * EMBEDDING_URL: The base URL for embedding endpoint
  * EMBEDDING_MODEL_ID: The model ID to use


Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If required environment variables are not set.  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-heroku/llama_index/embeddings/heroku/base.py`  
| 
```
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
```
 | 
```
classHerokuEmbedding(BaseEmbedding):
"""
    Heroku Managed Inference Embeddings Integration.

    This class provides an interface to Heroku's Managed Inference API for embeddings.
    It connects to your Heroku app's embedding endpoint for embedding models. For more
    information about Heroku's embedding endpoint
    see: https://devcenter.heroku.com/articles/heroku-inference-api-model-cohere-embed-multilingual

    Args:
        model (str, optional): The model to use. If not provided, will use EMBEDDING_MODEL_ID.
        api_key (str, optional): The API key for Heroku embedding. Defaults to EMBEDDING_KEY.
        base_url (str, optional): The base URL for embedding. Defaults to EMBEDDING_URL.
        timeout (float, optional): Timeout for requests in seconds. Defaults to 60.0.
        **kwargs: Additional keyword arguments.

    Environment Variables:
        - EMBEDDING_KEY: The API key for Heroku embedding
        - EMBEDDING_URL: The base URL for embedding endpoint
        - EMBEDDING_MODEL_ID: The model ID to use

    Raises:
        ValueError: If required environment variables are not set.

    """

    model: Optional[str] = Field(
        default=None, description="The model to use for embeddings."
    )
    api_key: Optional[str] = Field(
        default=None, description="The API key for Heroku embedding."
    )
    base_url: Optional[str] = Field(
        default=None, description="The base URL for embedding endpoint."
    )
    timeout: float = Field(default=60.0, description="Timeout for requests in seconds.")

    _client: httpx.Client = PrivateAttr()
    _aclient: httpx.AsyncClient = PrivateAttr()

    def__init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
"""
        Initialize an instance of the HerokuEmbedding class.

        Args:
            model (str, optional): The model to use. If not provided, will use EMBEDDING_MODEL_ID.
            api_key (str, optional): The API key for Heroku embedding. Defaults to EMBEDDING_KEY.
            base_url (str, optional): The base URL for embedding. Defaults to EMBEDDING_URL.
            timeout (float, optional): Timeout for requests in seconds. Defaults to 60.0.
            embed_batch_size (int, optional): Batch size for embedding calls. Defaults to DEFAULT_EMBED_BATCH_SIZE.
            callback_manager (Optional[CallbackManager], optional): Callback manager. Defaults to None.
            **kwargs: Additional keyword arguments.

        """
        # Get API key from parameter or environment
        try:
            api_key = get_from_param_or_env(
                "api_key",
                api_key,
                "EMBEDDING_KEY",
            )
        except ValueError:
            raise ValueError(
                "API key is required. Set EMBEDDING_KEY environment variable or pass api_key parameter."
            )

        # Get embedding URL from parameter or environment
        try:
            base_url = get_from_param_or_env(
                "base_url",
                base_url,
                "EMBEDDING_URL",
            )
        except ValueError:
            raise ValueError(
                "Embedding URL is required. Set EMBEDDING_URL environment variable or pass base_url parameter."
            )

        # Get model from parameter or environment
        try:
            model = get_from_param_or_env(
                "model",
                model,
                "EMBEDDING_MODEL_ID",
            )
        except ValueError:
            raise ValueError(
                "Model is required. Set EMBEDDING_MODEL_ID environment variable or pass model parameter."
            )

        super().__init__(
            model_name=model,
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            **kwargs,
        )

        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout

        # Initialize HTTP clients
        self._client = httpx.Client(
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "llama-index-embeddings-heroku",
            },
        )
        self._aclient = httpx.AsyncClient(
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "llama-index-embeddings-heroku",
            },
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "HerokuEmbedding"

    def_get_query_embedding(self, query: str) -> Embedding:
"""Get query embedding."""
        return self._get_text_embedding(query)

    def_get_text_embedding(self, text: str) -> Embedding:
"""Get text embedding."""
        try:
            response = self._client.post(
                f"{self.base_url}/v1/embeddings",
                json={
                    "input": text,
                    "model": self.model,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["data"][0]["embedding"]
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error while embedding text: {e}")
            raise ValueError(f"Unable to embed text: {e}")
        except Exception as e:
            logger.error(f"Error while embedding text: {e}")
            raise ValueError(f"Unable to embed text: {e}")

    async def_aget_query_embedding(self, query: str) -> Embedding:
"""Get query embedding asynchronously."""
        return await self._aget_text_embedding(query)

    async def_aget_text_embedding(self, text: str) -> Embedding:
"""Get text embedding asynchronously."""
        try:
            response = await self._aclient.post(
                f"{self.base_url}/v1/embeddings",
                json={
                    "input": text,
                    "model": self.model,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["data"][0]["embedding"]
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error while embedding text: {e}")
            raise ValueError(f"Unable to embed text: {e}")
        except Exception as e:
            logger.error(f"Error while embedding text: {e}")
            raise ValueError(f"Unable to embed text: {e}")

    def__del__(self) -> None:
"""Clean up resources."""
        if hasattr(self, "_client"):
            self._client.close()

    async defaclose(self) -> None:
"""Close async client."""
        if hasattr(self, "_aclient"):
            await self._aclient.aclose()

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/heroku/#llama_index.embeddings.heroku.HerokuEmbedding.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-heroku/llama_index/embeddings/heroku/base.py`  
| 
```
151
152
153
154
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "HerokuEmbedding"

```
 |  
| --- | --- |  
###  aclose [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/heroku/#llama_index.embeddings.heroku.HerokuEmbedding.aclose "Permanent link")

```
aclose() -> None

```

Close async client.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-heroku/llama_index/embeddings/heroku/base.py`  
| 
```
209
210
211
212
```
 | 
```
async defaclose(self) -> None:
"""Close async client."""
    if hasattr(self, "_aclient"):
        await self._aclient.aclose()

```
 |  
| --- | --- |  
options: members: - HerokuEmbedding
