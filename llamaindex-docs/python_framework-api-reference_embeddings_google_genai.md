# Google genai
##  GoogleGenAIEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/google_genai/#llama_index.embeddings.google_genai.GoogleGenAIEmbedding "Permanent link")
Bases: 
Google GenAI embeddings.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model_name`  |  Model for embedding. Defaults to "gemini-embedding-2-preview".  |  `'gemini-embedding-2-preview'`  |  
|  `api_key`  |  `Optional[str]`  |  API key to access the model. Defaults to None.  |  `None`  |  
|  `embedding_config`  |  `Optional[EmbedContentConfigOrDict]`  |  Embedding config to access the model. Defaults to None.  |  `None`  |  
|  `vertexai_config`  |  `Optional[VertexAIConfig]`  |  Vertex AI config to access the model. Defaults to None.  |  `None`  |  
|  `http_options`  |  `Optional[HttpOptions]`  |  HTTP options to access the model. Defaults to None.  |  `None`  |  
|  `debug_config`  |  `Optional[DebugConfig]`  |  Debug config to access the model. Defaults to None.  |  `None`  |  
|  `embed_batch_size`  |  Batch size for embedding. Defaults to 100.  |  `DEFAULT_EMBED_BATCH_SIZE`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.base.CallbackManager\)")]`  |  Callback manager to access the model. Defaults to None.  |  `None`  |  
|  `retries`  |  Maximum number of retries for API calls. Defaults to 3.  |  
|  `timeout`  |  Timeout for API calls in seconds. Defaults to 10.  |  
|  `retry_min_seconds`  |  `float`  |  Minimum wait time between retries. Defaults to 1.  |  
|  `retry_max_seconds`  |  `float`  |  Maximum wait time between retries. Defaults to 10.  |  
|  `retry_exponential_base`  |  `float`  |  Base for exponential backoff calculation. Defaults to 2.  |  
Examples:
`pip install llama-index-embeddings-google-genai`

```
fromllama_index.embeddings.google_genaiimport GoogleGenAIEmbedding

embed_model = GoogleGenAIEmbedding(model_name="gemini-embedding-2-preview", api_key="...")

```

Source code in `llama-index-integrations/embeddings/llama-index-embeddings-google-genai/llama_index/embeddings/google_genai/base.py`  
| 
```
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
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
```
 | 
```
classGoogleGenAIEmbedding(BaseEmbedding):
"""
    Google GenAI embeddings.

    Args:
        model_name (str): Model for embedding.
            Defaults to "gemini-embedding-2-preview".
        api_key (Optional[str]): API key to access the model. Defaults to None.
        embedding_config (Optional[types.EmbedContentConfigOrDict]): Embedding config to access the model. Defaults to None.
        vertexai_config (Optional[VertexAIConfig]): Vertex AI config to access the model. Defaults to None.
        http_options (Optional[types.HttpOptions]): HTTP options to access the model. Defaults to None.
        debug_config (Optional[google.genai.client.DebugConfig]): Debug config to access the model. Defaults to None.
        embed_batch_size (int): Batch size for embedding. Defaults to 100.
        callback_manager (Optional[CallbackManager]): Callback manager to access the model. Defaults to None.
        retries (int): Maximum number of retries for API calls. Defaults to 3.
        timeout (int): Timeout for API calls in seconds. Defaults to 10.
        retry_min_seconds (float): Minimum wait time between retries. Defaults to 1.
        retry_max_seconds (float): Maximum wait time between retries. Defaults to 10.
        retry_exponential_base (float): Base for exponential backoff calculation. Defaults to 2.

    Examples:
        `pip install llama-index-embeddings-google-genai`

        ```python
        from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

        embed_model = GoogleGenAIEmbedding(model_name="gemini-embedding-2-preview", api_key="...")
        ```

    """

    _client: google.genai.Client = PrivateAttr()
    _embedding_config: types.EmbedContentConfigOrDict = PrivateAttr()

    embedding_config: Optional[types.EmbedContentConfigOrDict] = Field(
        default=None, description="""Used to override embedding config."""
    )
    retries: int = Field(default=3, description="Number of retries for embedding.")
    timeout: int = Field(default=10, description="Timeout for embedding.")
    retry_min_seconds: float = Field(
        default=1, description="Minimum wait time between retries."
    )
    retry_max_seconds: float = Field(
        default=10, description="Maximum wait time between retries."
    )
    retry_exponential_base: float = Field(
        default=2, description="Base for exponential backoff calculation."
    )

    def__init__(
        self,
        model_name: str = "gemini-embedding-2-preview",
        api_key: Optional[str] = None,
        embedding_config: Optional[types.EmbedContentConfigOrDict] = None,
        vertexai_config: Optional[VertexAIConfig] = None,
        http_options: Optional[types.HttpOptions] = None,
        debug_config: Optional[google.genai.client.DebugConfig] = None,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        callback_manager: Optional[CallbackManager] = None,
        retries: int = 3,
        timeout: int = 60,
        retry_min_seconds: float = 1,
        retry_max_seconds: float = 60,
        retry_exponential_base: float = 2,
        **kwargs: Any,
    ):
        super().__init__(
            model_name=model_name,
            embedding_config=embedding_config,
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            retries=retries,
            timeout=timeout,
            retry_min_seconds=retry_min_seconds,
            retry_max_seconds=retry_max_seconds,
            retry_exponential_base=retry_exponential_base,
            **kwargs,
        )

        # API keys are optional. The API can be authorised via OAuth (detected
        # environmentally) or by the GOOGLE_API_KEY environment variable.
        api_key = api_key or os.getenv("GOOGLE_API_KEY", None)
        vertexai = vertexai_config is not None or os.getenv(
            "GOOGLE_GENAI_USE_VERTEXAI", False
        )
        project = (vertexai_config or {}).get("project") or os.getenv(
            "GOOGLE_CLOUD_PROJECT", None
        )
        location = (vertexai_config or {}).get("location") or os.getenv(
            "GOOGLE_CLOUD_LOCATION", None
        )

        config_params: Dict[str, Any] = {
            "api_key": api_key,
        }

        if vertexai_config is not None:
            config_params.update(vertexai_config)
            config_params["api_key"] = None
            config_params["vertexai"] = True
        elif vertexai:
            config_params["project"] = project
            config_params["location"] = location
            config_params["api_key"] = None
            config_params["vertexai"] = True

        try:
            package_v = version("llama-index-embeddings-google-genai")
        except PackageNotFoundError:
            package_v = "0.0.0"
        client_hdr = {"x-goog-api-client": f"llamaindex/{package_v}"}

        if isinstance(http_options, dict):
            http_opts = http_options
        elif isinstance(http_options, types.HttpOptions):
            http_opts = http_options.to_json_dict()
        else:
            http_opts = {}
        http_opts["headers"] = http_opts.get("headers", {}) | client_hdr

        config_params["http_options"] = types.HttpOptions(**http_opts)

        if debug_config:
            config_params["debug_config"] = debug_config

        self._client = google.genai.Client(**config_params)

    @classmethod
    defclass_name(cls) -> str:
        return "GeminiEmbedding"

    def_embed_texts(
        self, texts: List[str], task_type: Optional[str] = None
    ) -> List[List[float]]:
"""Embed texts."""
        # Set the task type if it is not already set
        if task_type and not self.embedding_config:
            embedding_config = types.EmbedContentConfig(task_type=task_type)
        elif task_type and self.embedding_config:
            embedding_config = dict(self.embedding_config)
            embedding_config["task_type"] = task_type
        else:
            embedding_config = self.embedding_config

        # Create the embedding function with retry logic
        defembed_with_client() -> List[List[float]]:
            results = self._client.models.embed_content(
                model=self.model_name,
                contents=texts,
                config=embedding_config,
            )
            return [result.values for result in results.embeddings]

        # Apply the retry decorator
        retryable_embed = get_retryable_function(
            embed_with_client,
            max_retries=self.retries,
            min_seconds=self.retry_min_seconds,
            max_seconds=self.retry_max_seconds,
            exponential_base=self.retry_exponential_base,
        )

        return retryable_embed()

    async def_aembed_texts(
        self, texts: List[str], task_type: Optional[str] = None
    ) -> List[List[float]]:
"""Asynchronously embed texts."""
        # Set the task type if it is not already set
        if task_type and not self.embedding_config:
            embedding_config = types.EmbedContentConfig(task_type=task_type)
        elif task_type and self.embedding_config:
            embedding_config = dict(self.embedding_config)
            embedding_config["task_type"] = task_type
        else:
            embedding_config = self.embedding_config

        # Create the async embedding function with retry logic
        async defaembed_with_client() -> List[List[float]]:
            results = await self._client.aio.models.embed_content(
                model=self.model_name,
                contents=texts,
                config=embedding_config,
            )
            return [result.values for result in results.embeddings]

        # Apply the async retry helper
        return await get_retryable_async_function(
            aembed_with_client,
            max_retries=self.retries,
            min_seconds=self.retry_min_seconds,
            max_seconds=self.retry_max_seconds,
            exponential_base=self.retry_exponential_base,
        )

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        return self._embed_texts([query], task_type="RETRIEVAL_QUERY")[0]

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        return self._embed_texts([text], task_type="RETRIEVAL_DOCUMENT")[0]

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get text embeddings."""
        return self._embed_texts(texts, task_type="RETRIEVAL_DOCUMENT")

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""The asynchronous version of _get_query_embedding."""
        return (await self._aembed_texts([query], task_type="RETRIEVAL_QUERY"))[0]

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Asynchronously get text embedding."""
        return (await self._aembed_texts([text], task_type="RETRIEVAL_DOCUMENT"))[0]

    async def_aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Asynchronously get text embeddings."""
        return await self._aembed_texts(texts, task_type="RETRIEVAL_DOCUMENT")

```
 |  
| --- | --- |  
options: members: - GoogleGenAIEmbedding
