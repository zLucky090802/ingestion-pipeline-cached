# Isaacus
##  IsaacusEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/isaacus/#llama_index.embeddings.isaacus.IsaacusEmbedding "Permanent link")
Bases: 
Isaacus Embeddings Integration.
This class provides an interface to Isaacus' embedding API, featuring the Kanon 2 Embedder - the world's most accurate legal embedding model on the Massive Legal Embedding Benchmark (MLEB).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model`  |  The model to use. Defaults to "kanon-2-embedder".  |  `DEFAULT_ISAACUS_MODEL`  |  
|  `api_key`  |  The API key for Isaacus. Defaults to ISAACUS_API_KEY.  |  `None`  |  
|  `base_url`  |  The base URL for Isaacus API. Defaults to ISAACUS_BASE_URL.  |  `None`  |  
|  `dimensions`  |  The desired embedding dimensionality.  |  `None`  |  
|  `task`  |  Task type: "retrieval/query" or "retrieval/document".  |  `None`  |  
|  `overflow_strategy`  |  Strategy for handling overflow. Defaults to "drop_end".  |  `'drop_end'`  |  
|  `timeout`  |  `float`  |  Timeout for requests in seconds. Defaults to 60.0.  |  `60.0`  |  
|  `**kwargs`  |  Additional keyword arguments.  |  
Environment Variables
  * ISAACUS_API_KEY: The API key for Isaacus
  * ISAACUS_BASE_URL: The base URL for Isaacus API (optional)


Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If required environment variables are not set.  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-isaacus/llama_index/embeddings/isaacus/base.py`  
| 
```
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
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
```
 | 
```
classIsaacusEmbedding(BaseEmbedding):
"""
    Isaacus Embeddings Integration.

    This class provides an interface to Isaacus' embedding API, featuring the
    Kanon 2 Embedder - the world's most accurate legal embedding model on the
    Massive Legal Embedding Benchmark (MLEB).

    Args:
        model (str, optional): The model to use. Defaults to "kanon-2-embedder".
        api_key (str, optional): The API key for Isaacus. Defaults to ISAACUS_API_KEY.
        base_url (str, optional): The base URL for Isaacus API. Defaults to ISAACUS_BASE_URL.
        dimensions (int, optional): The desired embedding dimensionality.
        task (str, optional): Task type: "retrieval/query" or "retrieval/document".
        overflow_strategy (str, optional): Strategy for handling overflow. Defaults to "drop_end".
        timeout (float, optional): Timeout for requests in seconds. Defaults to 60.0.
        **kwargs: Additional keyword arguments.

    Environment Variables:
        - ISAACUS_API_KEY: The API key for Isaacus
        - ISAACUS_BASE_URL: The base URL for Isaacus API (optional)

    Raises:
        ValueError: If required environment variables are not set.

    """

    model: str = Field(
        default=DEFAULT_ISAACUS_MODEL,
        description="The model to use for embeddings.",
    )
    api_key: Optional[str] = Field(default=None, description="The API key for Isaacus.")
    base_url: Optional[str] = Field(
        default=None, description="The base URL for Isaacus API."
    )
    dimensions: Optional[int] = Field(
        default=None, description="The desired embedding dimensionality."
    )
    task: Optional[Literal["retrieval/query", "retrieval/document"]] = Field(
        default=None,
        description="Task type: 'retrieval/query' or 'retrieval/document'.",
    )
    overflow_strategy: Optional[Literal["drop_end"]] = Field(
        default="drop_end", description="Strategy for handling overflow."
    )
    timeout: float = Field(default=60.0, description="Timeout for requests in seconds.")

    _client: Any = PrivateAttr()
    _aclient: Any = PrivateAttr()

    def__init__(
        self,
        model: str = DEFAULT_ISAACUS_MODEL,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        dimensions: Optional[int] = None,
        task: Optional[Literal["retrieval/query", "retrieval/document"]] = None,
        overflow_strategy: Optional[Literal["drop_end"]] = "drop_end",
        timeout: float = 60.0,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
"""
        Initialize an instance of the IsaacusEmbedding class.

        Args:
            model (str, optional): The model to use. Defaults to "kanon-2-embedder".
            api_key (str, optional): The API key for Isaacus. Defaults to ISAACUS_API_KEY.
            base_url (str, optional): The base URL for Isaacus API.
            dimensions (int, optional): The desired embedding dimensionality.
            task (str, optional): Task type: "retrieval/query" or "retrieval/document".
            overflow_strategy (str, optional): Strategy for handling overflow.
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
                "ISAACUS_API_KEY",
            )
        except ValueError:
            raise ValueError(
                "API key is required. Set ISAACUS_API_KEY environment variable or pass api_key parameter."
            )

        # Get base URL from parameter or environment (optional)
        if base_url is None:
            try:
                base_url = get_from_param_or_env(
                    "base_url",
                    base_url,
                    "ISAACUS_BASE_URL",
                )
            except ValueError:
                base_url = DEFAULT_ISAACUS_API_BASE

        super().__init__(
            model_name=model,
            model=model,
            api_key=api_key,
            base_url=base_url,
            dimensions=dimensions,
            task=task,
            overflow_strategy=overflow_strategy,
            timeout=timeout,
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            **kwargs,
        )

        # Initialize Isaacus clients
        self._client = isaacus.Isaacus(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
        )
        self._aclient = isaacus.AsyncIsaacus(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "IsaacusEmbedding"

    def_prepare_request_params(
        self, text: str, task_override: Optional[str] = None
    ) -> dict:
"""Prepare request parameters for the Isaacus API."""
        params = {
            "model": self.model,
            "texts": text,
        }

        # Use task_override if provided, otherwise use instance task
        task_to_use = task_override if task_override is not None else self.task
        if task_to_use is not None:
            params["task"] = task_to_use

        if self.dimensions is not None:
            params["dimensions"] = self.dimensions

        if self.overflow_strategy is not None:
            params["overflow_strategy"] = self.overflow_strategy

        return params

    def_get_query_embedding(self, query: str) -> Embedding:
"""
        Get query embedding.

        For queries, we use the 'retrieval/query' task if no task is explicitly set.
        """
        return self._get_text_embedding(query, task_override="retrieval/query")

    def_get_text_embedding(
        self, text: str, task_override: Optional[str] = None
    ) -> Embedding:
"""Get text embedding."""
        try:
            params = self._prepare_request_params(text, task_override)
            response = self._client.embeddings.create(**params)

            # Extract the embedding from the response
            if response.embeddings and len(response.embeddings)  0:
                return response.embeddings[0].embedding
            else:
                raise ValueError("No embeddings returned from API")

        except Exception as e:
            logger.error(f"Error while embedding text: {e}")
            raise ValueError(f"Unable to embed text: {e}")

    def_get_text_embeddings(self, texts: List[str]) -> List[Embedding]:
"""
        Get embeddings for multiple texts.

        Note: The Isaacus API supports batch embedding, so we send all texts at once.
        """
        try:
            params = self._prepare_request_params(texts, task_override=self.task)
            response = self._client.embeddings.create(**params)

            # Extract embeddings from response, maintaining order
            embeddings = []
            for emb_obj in sorted(response.embeddings, key=lambda x: x.index):
                embeddings.append(emb_obj.embedding)

            return embeddings

        except Exception as e:
            logger.error(f"Error while embedding texts: {e}")
            raise ValueError(f"Unable to embed texts: {e}")

    async def_aget_query_embedding(self, query: str) -> Embedding:
"""
        Get query embedding asynchronously.

        For queries, we use the 'retrieval/query' task if no task is explicitly set.
        """
        return await self._aget_text_embedding(query, task_override="retrieval/query")

    async def_aget_text_embedding(
        self, text: str, task_override: Optional[str] = None
    ) -> Embedding:
"""Get text embedding asynchronously."""
        try:
            params = self._prepare_request_params(text, task_override)
            response = await self._aclient.embeddings.create(**params)

            # Extract the embedding from the response
            if response.embeddings and len(response.embeddings)  0:
                return response.embeddings[0].embedding
            else:
                raise ValueError("No embeddings returned from API")

        except Exception as e:
            logger.error(f"Error while embedding text: {e}")
            raise ValueError(f"Unable to embed text: {e}")

    async def_aget_text_embeddings(self, texts: List[str]) -> List[Embedding]:
"""
        Get embeddings for multiple texts asynchronously.

        Note: The Isaacus API supports batch embedding, so we send all texts at once.
        """
        try:
            params = self._prepare_request_params(texts, task_override=self.task)
            response = await self._aclient.embeddings.create(**params)

            # Extract embeddings from response, maintaining order
            embeddings = []
            for emb_obj in sorted(response.embeddings, key=lambda x: x.index):
                embeddings.append(emb_obj.embedding)

            return embeddings

        except Exception as e:
            logger.error(f"Error while embedding texts: {e}")
            raise ValueError(f"Unable to embed texts: {e}")

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/isaacus/#llama_index.embeddings.isaacus.IsaacusEmbedding.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-isaacus/llama_index/embeddings/isaacus/base.py`  
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
    return "IsaacusEmbedding"

```
 |  
| --- | --- |  
options: members: - IsaacusEmbedding
