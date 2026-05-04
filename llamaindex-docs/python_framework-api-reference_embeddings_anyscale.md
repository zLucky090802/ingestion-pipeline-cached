# Anyscale
##  AnyscaleEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/anyscale/#llama_index.embeddings.anyscale.AnyscaleEmbedding "Permanent link")
Bases: 
Anyscale class for embeddings.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model`  |  Model for embedding. Defaults to "thenlper/gte-large"  |  `DEFAULT_MODEL`  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-anyscale/llama_index/embeddings/anyscale/base.py`  
| 
```
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
```
 | 
```
classAnyscaleEmbedding(BaseEmbedding):
"""
    Anyscale class for embeddings.

    Args:
        model (str): Model for embedding.
            Defaults to "thenlper/gte-large"

    """

    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the OpenAI API."
    )

    api_key: str = Field(description="The Anyscale API key.")
    api_base: str = Field(description="The base URL for Anyscale API.")
    api_version: str = Field(description="The version for OpenAI API.")

    max_retries: int = Field(default=10, description="Maximum number of retries.", ge=0)
    timeout: float = Field(default=60.0, description="Timeout for each request.", ge=0)
    default_headers: Optional[Dict[str, str]] = Field(
        default=None, description="The default headers for API requests."
    )
    reuse_client: bool = Field(
        default=True,
        description=(
            "Reuse the Anyscale client between requests. When doing anything with large "
            "volumes of async API calls, setting this to false can improve stability."
        ),
    )

    _query_engine: Optional[str] = PrivateAttr()
    _text_engine: Optional[str] = PrivateAttr()
    _client: Optional[OpenAI] = PrivateAttr()
    _aclient: Optional[AsyncOpenAI] = PrivateAttr()
    _http_client: Optional[httpx.Client] = PrivateAttr()

    def__init__(
        self,
        model: str = DEFAULT_MODEL,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = DEFAULT_API_BASE,
        api_version: Optional[str] = None,
        max_retries: int = 10,
        timeout: float = 60.0,
        reuse_client: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        default_headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
        **kwargs: Any,
    ) -> None:
        additional_kwargs = additional_kwargs or {}

        api_key, api_base, api_version = resolve_anyscale_credentials(
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
        )

        if "model_name" in kwargs:
            model_name = kwargs.pop("model_name")
        else:
            model_name = model

        super().__init__(
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            model_name=model_name,
            additional_kwargs=additional_kwargs,
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
            max_retries=max_retries,
            reuse_client=reuse_client,
            timeout=timeout,
            default_headers=default_headers,
            **kwargs,
        )

        self._query_engine = model_name
        self._text_engine = model_name
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

    def_create_retry_decorator(self):
"""Create a retry decorator using the instance's max_retries."""
        return create_retry_decorator(
            max_retries=self.max_retries,
            random_exponential=True,
            stop_after_delay_seconds=60,
            min_seconds=1,
            max_seconds=20,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "AnyscaleEmbedding"

    def_get_credential_kwargs(self) -> Dict[str, Any]:
        return {
            "api_key": self.api_key,
            "base_url": self.api_base,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "default_headers": self.default_headers,
            "http_client": self._http_client,
        }

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        client = self._get_client()
        retry_decorator = self._create_retry_decorator()

        @retry_decorator
        def_retryable_get_embedding():
            return get_embedding(
                client,
                query,
                engine=self._query_engine,
                **self.additional_kwargs,
            )

        return _retryable_get_embedding()

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""The asynchronous version of _get_query_embedding."""
        aclient = self._get_aclient()
        retry_decorator = self._create_retry_decorator()

        @retry_decorator
        async def_retryable_aget_embedding():
            return await aget_embedding(
                aclient,
                query,
                engine=self._query_engine,
                **self.additional_kwargs,
            )

        return await _retryable_aget_embedding()

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        client = self._get_client()
        retry_decorator = self._create_retry_decorator()

        @retry_decorator
        def_retryable_get_embedding():
            return get_embedding(
                client,
                text,
                engine=self._text_engine,
                **self.additional_kwargs,
            )

        return _retryable_get_embedding()

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Asynchronously get text embedding."""
        aclient = self._get_aclient()
        retry_decorator = self._create_retry_decorator()

        @retry_decorator
        async def_retryable_aget_embedding():
            return await aget_embedding(
                aclient,
                text,
                engine=self._text_engine,
                **self.additional_kwargs,
            )

        return await _retryable_aget_embedding()

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""
        Get text embeddings.

        By default, this is a wrapper around _get_text_embedding.
        Can be overridden for batch queries.

        """
        client = self._get_client()
        retry_decorator = self._create_retry_decorator()

        @retry_decorator
        def_retryable_get_embeddings():
            return get_embeddings(
                client,
                texts,
                engine=self._text_engine,
                **self.additional_kwargs,
            )

        return _retryable_get_embeddings()

    async def_aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Asynchronously get text embeddings."""
        aclient = self._get_aclient()
        retry_decorator = self._create_retry_decorator()

        @retry_decorator
        async def_retryable_aget_embeddings():
            return await aget_embeddings(
                aclient,
                texts,
                engine=self._text_engine,
                **self.additional_kwargs,
            )

        return await _retryable_aget_embeddings()

```
 |  
| --- | --- |  
options: members: - AnyscaleEmbedding
