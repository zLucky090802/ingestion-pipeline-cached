# Databricks
##  DatabricksEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/databricks/#llama_index.embeddings.databricks.DatabricksEmbedding "Permanent link")
Bases: 
Databricks class for text embedding.
Databricks adheres to the OpenAI API, so this integration aligns closely with the existing OpenAIEmbedding class.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model`  |  The unique ID of the embedding model as served by the Databricks endpoint.  |  _required_  |  
|  `endpoint`  |  `Optional[str]`  |  The url of the Databricks endpoint. Can be set as an environment variable (`DATABRICKS_SERVING_ENDPOINT`).  |  `None`  |  
|  `api_key`  |  `Optional[str]`  |  The Databricks API key to use. Can be set as an environment variable (`DATABRICKS_TOKEN`).  |  `None`  |  
Examples:
`pip install llama-index-embeddings-databricks`

```
importos
fromllama_index.coreimport Settings
fromllama_index.embeddings.databricksimport DatabricksEmbedding

# Set up the DatabricksEmbedding class with the required model, API key and serving endpoint
os.environ["DATABRICKS_TOKEN"] = "<MY TOKEN>"
os.environ["DATABRICKS_SERVING_ENDPOINT"] = "<MY ENDPOINT>"
embed_model  = DatabricksEmbedding(model="databricks-bge-large-en")
Settings.embed_model = embed_model

# Embed some text
embeddings = embed_model.get_text_embedding("The DatabricksEmbedding integration works great.")

```

Source code in `llama-index-integrations/embeddings/llama-index-embeddings-databricks/llama_index/embeddings/databricks/base.py`  
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
213
214
215
216
217
218
219
220
```
 | 
```
classDatabricksEmbedding(BaseEmbedding):
"""
    Databricks class for text embedding.

    Databricks adheres to the OpenAI API, so this integration aligns closely with the existing OpenAIEmbedding class.

    Args:
        model (str): The unique ID of the embedding model as served by the Databricks endpoint.
        endpoint (Optional[str]): The url of the Databricks endpoint. Can be set as an environment variable (`DATABRICKS_SERVING_ENDPOINT`).
        api_key (Optional[str]): The Databricks API key to use. Can be set as an environment variable (`DATABRICKS_TOKEN`).

    Examples:
        `pip install llama-index-embeddings-databricks`

        ```python
        import os
        from llama_index.core import Settings
        from llama_index.embeddings.databricks import DatabricksEmbedding

        # Set up the DatabricksEmbedding class with the required model, API key and serving endpoint
        os.environ["DATABRICKS_TOKEN"] = "<MY TOKEN>"
        os.environ["DATABRICKS_SERVING_ENDPOINT"] = "<MY ENDPOINT>"
        embed_model  = DatabricksEmbedding(model="databricks-bge-large-en")
        Settings.embed_model = embed_model

        # Embed some text
        embeddings = embed_model.get_text_embedding("The DatabricksEmbedding integration works great.")

        ```

    """

    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs as for the OpenAI API."
    )

    model: str = Field(
        description="The ID of a model hosted on the databricks endpoint."
    )
    api_key: str = Field(description="The Databricks API key.")
    endpoint: str = Field(description="The Databricks API endpoint.")

    max_retries: int = Field(default=10, description="Maximum number of retries.", ge=0)
    timeout: float = Field(default=60.0, description="Timeout for each request.", ge=0)
    default_headers: Optional[Dict[str, str]] = Field(
        default=None, description="The default headers for API requests."
    )
    reuse_client: bool = Field(
        default=True,
        description=(
            "Reuse the client between requests. When doing anything with large "
            "volumes of async API calls, setting this to false can improve stability."
        ),
    )

    _query_engine: str = PrivateAttr()
    _text_engine: str = PrivateAttr()
    _client: Optional[OpenAI] = PrivateAttr()
    _aclient: Optional[AsyncOpenAI] = PrivateAttr()
    _http_client: Optional[httpx.Client] = PrivateAttr()

    def__init__(
        self,
        model: str,
        endpoint: Optional[str] = None,
        embed_batch_size: int = 100,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        api_key: Optional[str] = None,
        max_retries: int = 10,
        timeout: float = 60.0,
        reuse_client: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        default_headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
        num_workers: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        additional_kwargs = additional_kwargs or {}

        api_key = get_from_param_or_env("api_key", api_key, "DATABRICKS_TOKEN")
        endpoint = get_from_param_or_env(
            "endpoint", endpoint, "DATABRICKS_SERVING_ENDPOINT"
        )

        super().__init__(
            model=model,
            endpoint=endpoint,
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            model_name=model,
            additional_kwargs=additional_kwargs,
            api_key=api_key,
            max_retries=max_retries,
            reuse_client=reuse_client,
            timeout=timeout,
            default_headers=default_headers,
            num_workers=num_workers,
            **kwargs,
        )

        self._client = None
        self._aclient = None
        self._http_client = http_client

    def_get_client(self) -> OpenAI:
        if not self.reuse_client:
            return OpenAI(**self._get_credential_kwargs())

        if self._client is None:
            self._client = OpenAI(**self._get_credential_kwargs())
        return self._client

    def_get_aclient(self) -> AsyncOpenAI:
        if not self.reuse_client:
            return AsyncOpenAI(**self._get_credential_kwargs())

        if self._aclient is None:
            self._aclient = AsyncOpenAI(**self._get_credential_kwargs())
        return self._aclient

    @classmethod
    defclass_name(cls) -> str:
        return "DatabricksEmbedding"

    def_get_credential_kwargs(self) -> Dict[str, Any]:
        return {
            "api_key": self.api_key,
            "base_url": self.endpoint,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "default_headers": self.default_headers,
            "http_client": self._http_client,
        }

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        client = self._get_client()
        return get_embedding(
            client,
            query,
            engine=self.model,
            **self.additional_kwargs,
        )

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""The asynchronous version of _get_query_embedding."""
        aclient = self._get_aclient()
        return await aget_embedding(
            aclient,
            query,
            engine=self.model,
            **self.additional_kwargs,
        )

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        client = self._get_client()
        return get_embedding(
            client,
            text,
            engine=self.model,
            **self.additional_kwargs,
        )

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Asynchronously get text embedding."""
        aclient = self._get_aclient()
        return await aget_embedding(
            aclient,
            text,
            engine=self.model,
            **self.additional_kwargs,
        )

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""
        Get text embeddings.

        By default, this is a wrapper around _get_text_embedding.
        Can be overridden for batch queries.

        """
        client = self._get_client()
        return get_embeddings(
            client,
            texts,
            engine=self.model,
            **self.additional_kwargs,
        )

    async def_aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Asynchronously get text embeddings."""
        aclient = self._get_aclient()
        return await aget_embeddings(
            aclient,
            texts,
            engine=self.model,
            **self.additional_kwargs,
        )

```
 |  
| --- | --- |  
options: members: - DatabricksEmbedding
