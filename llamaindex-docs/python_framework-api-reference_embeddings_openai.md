# Openai
##  OpenAIEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/openai/#llama_index.embeddings.openai.OpenAIEmbedding "Permanent link")
Bases: 
OpenAI class for embeddings.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `mode`  |  Mode for embedding. Defaults to OpenAIEmbeddingMode.TEXT_SEARCH_MODE. Options are:
  * OpenAIEmbeddingMode.SIMILARITY_MODE
  * OpenAIEmbeddingMode.TEXT_SEARCH_MODE

 |  `TEXT_SEARCH_MODE`  |  
|  `model`  |  Model for embedding. Defaults to OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002. Options are:
  * OpenAIEmbeddingModelType.DAVINCI
  * OpenAIEmbeddingModelType.CURIE
  * OpenAIEmbeddingModelType.BABBAGE
  * OpenAIEmbeddingModelType.ADA
  * OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002

 |  `TEXT_EMBED_ADA_002`  |  
|  `additional_kwargs`  |  `Dict[str, Any]`  |  Additional kwargs for the OpenAI API.  |  `<class 'dict'>`  |  
|  `api_key`  |  The OpenAI API key.  |  _required_  |  
|  `api_base`  |  `str | None`  |  The base URL for OpenAI API.  |  `'https://api.openai.com/v1'`  |  
|  `api_version`  |  `str | None`  |  The version for OpenAI API.  |  
|  `max_retries`  |  Maximum number of retries.  |  
|  `timeout`  |  `float`  |  Timeout for each request.  |  `60.0`  |  
|  `default_headers`  |  `Dict[str, str] | None`  |  The default headers for API requests.  |  `None`  |  
|  `reuse_client`  |  `bool`  |  Reuse the OpenAI client between requests. When doing anything with large volumes of async API calls, setting this to false can improve stability.  |  `True`  |  
|  `dimensions`  |  `int | None`  |  The number of dimensions on the output embedding vectors. Works only with v3 embedding models.  |  `None`  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-openai/llama_index/embeddings/openai/base.py`  
| 
```
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
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
```
 | 
```
classOpenAIEmbedding(BaseEmbedding):
"""
    OpenAI class for embeddings.

    Args:
        mode (str): Mode for embedding.
            Defaults to OpenAIEmbeddingMode.TEXT_SEARCH_MODE.
            Options are:

            - OpenAIEmbeddingMode.SIMILARITY_MODE
            - OpenAIEmbeddingMode.TEXT_SEARCH_MODE

        model (str): Model for embedding.
            Defaults to OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002.
            Options are:

            - OpenAIEmbeddingModelType.DAVINCI
            - OpenAIEmbeddingModelType.CURIE
            - OpenAIEmbeddingModelType.BABBAGE
            - OpenAIEmbeddingModelType.ADA
            - OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002

    """

    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the OpenAI API."
    )

    api_key: str = Field(description="The OpenAI API key.")
    api_base: Optional[str] = Field(
        default=DEFAULT_OPENAI_API_BASE, description="The base URL for OpenAI API."
    )
    api_version: Optional[str] = Field(
        default=DEFAULT_OPENAI_API_VERSION, description="The version for OpenAI API."
    )

    max_retries: int = Field(default=10, description="Maximum number of retries.", ge=0)
    timeout: float = Field(default=60.0, description="Timeout for each request.", ge=0)
    default_headers: Optional[Dict[str, str]] = Field(
        default=None, description="The default headers for API requests."
    )
    reuse_client: bool = Field(
        default=True,
        description=(
            "Reuse the OpenAI client between requests. When doing anything with large "
            "volumes of async API calls, setting this to false can improve stability."
        ),
    )
    dimensions: Optional[int] = Field(
        default=None,
        description=(
            "The number of dimensions on the output embedding vectors. "
            "Works only with v3 embedding models."
        ),
    )

    _query_engine: str = PrivateAttr()
    _text_engine: str = PrivateAttr()
    _client: Optional[OpenAI] = PrivateAttr()
    _aclient: Optional[AsyncOpenAI] = PrivateAttr()
    _http_client: Optional[httpx.Client] = PrivateAttr()
    _async_http_client: Optional[httpx.AsyncClient] = PrivateAttr()

    def__init__(
        self,
        mode: str = OpenAIEmbeddingMode.TEXT_SEARCH_MODE,
        model: str = OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002,
        embed_batch_size: int = 100,
        dimensions: Optional[int] = None,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        api_version: Optional[str] = None,
        max_retries: int = 10,
        timeout: float = 60.0,
        reuse_client: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        default_headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
        async_http_client: Optional[httpx.AsyncClient] = None,
        num_workers: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        additional_kwargs = additional_kwargs or {}
        if dimensions is not None:
            additional_kwargs["dimensions"] = dimensions

        api_key, api_base, api_version = self._resolve_credentials(
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
        )

        query_engine = get_engine(mode, model, _QUERY_MODE_MODEL_DICT)
        text_engine = get_engine(mode, model, _TEXT_MODE_MODEL_DICT)

        if "model_name" in kwargs:
            model_name = kwargs.pop("model_name")
            query_engine = text_engine = model_name
        else:
            model_name = model

        super().__init__(
            embed_batch_size=embed_batch_size,
            dimensions=dimensions,
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
            num_workers=num_workers,
            **kwargs,
        )
        self._query_engine = query_engine
        self._text_engine = text_engine

        self._client = None
        self._aclient = None
        self._http_client = http_client
        self._async_http_client = async_http_client

    def_resolve_credentials(
        self,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        api_version: Optional[str] = None,
    ) -> Tuple[Optional[str], str, str]:
        return resolve_openai_credentials(api_key, api_base, api_version)

    def_get_client(self) -> OpenAI:
        if not self.reuse_client:
            return OpenAI(**self._get_credential_kwargs())

        if self._client is None:
            self._client = OpenAI(**self._get_credential_kwargs())
        return self._client

    def_get_aclient(self) -> AsyncOpenAI:
        if not self.reuse_client:
            return AsyncOpenAI(**self._get_credential_kwargs(is_async=True))

        if self._aclient is None:
            self._aclient = AsyncOpenAI(**self._get_credential_kwargs(is_async=True))
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
        return "OpenAIEmbedding"

    def_get_credential_kwargs(self, is_async: bool = False) -> Dict[str, Any]:
        return {
            "api_key": self.api_key,
            "base_url": self.api_base,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "default_headers": self.default_headers,
            "http_client": self._async_http_client if is_async else self._http_client,
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
##  OpenAIEmbeddingMode [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/openai/#llama_index.embeddings.openai.OpenAIEmbeddingMode "Permanent link")
Bases: `str`, `Enum`
OpenAI embedding mode.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-openai/llama_index/embeddings/openai/base.py`  
| 
```
20
21
22
23
24
```
 | 
```
classOpenAIEmbeddingMode(str, Enum):
"""OpenAI embedding mode."""

    SIMILARITY_MODE = "similarity"
    TEXT_SEARCH_MODE = "text_search"

```
 |  
| --- | --- |  
##  OpenAIEmbeddingModelType [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/openai/#llama_index.embeddings.openai.OpenAIEmbeddingModelType "Permanent link")
Bases: `str`, `Enum`
OpenAI embedding model type.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-openai/llama_index/embeddings/openai/base.py`  
| 
```
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
```
 | 
```
classOpenAIEmbeddingModelType(str, Enum):
"""OpenAI embedding model type."""

    DAVINCI = "davinci"
    CURIE = "curie"
    BABBAGE = "babbage"
    ADA = "ada"
    TEXT_EMBED_ADA_002 = "text-embedding-ada-002"
    TEXT_EMBED_3_LARGE = "text-embedding-3-large"
    TEXT_EMBED_3_SMALL = "text-embedding-3-small"

```
 |  
| --- | --- |  
##  OpenAIEmbeddingModeModel [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/openai/#llama_index.embeddings.openai.OpenAIEmbeddingModeModel "Permanent link")
Bases: `str`, `Enum`
OpenAI embedding mode model.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-openai/llama_index/embeddings/openai/base.py`  
| 
```
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
```
 | 
```
classOpenAIEmbeddingModeModel(str, Enum):
"""OpenAI embedding mode model."""

    # davinci
    TEXT_SIMILARITY_DAVINCI = "text-similarity-davinci-001"
    TEXT_SEARCH_DAVINCI_QUERY = "text-search-davinci-query-001"
    TEXT_SEARCH_DAVINCI_DOC = "text-search-davinci-doc-001"

    # curie
    TEXT_SIMILARITY_CURIE = "text-similarity-curie-001"
    TEXT_SEARCH_CURIE_QUERY = "text-search-curie-query-001"
    TEXT_SEARCH_CURIE_DOC = "text-search-curie-doc-001"

    # babbage
    TEXT_SIMILARITY_BABBAGE = "text-similarity-babbage-001"
    TEXT_SEARCH_BABBAGE_QUERY = "text-search-babbage-query-001"
    TEXT_SEARCH_BABBAGE_DOC = "text-search-babbage-doc-001"

    # ada
    TEXT_SIMILARITY_ADA = "text-similarity-ada-001"
    TEXT_SEARCH_ADA_QUERY = "text-search-ada-query-001"
    TEXT_SEARCH_ADA_DOC = "text-search-ada-doc-001"

    # text-embedding-ada-002
    TEXT_EMBED_ADA_002 = "text-embedding-ada-002"

    # text-embedding-3-large
    TEXT_EMBED_3_LARGE = "text-embedding-3-large"

    # text-embedding-3-small
    TEXT_EMBED_3_SMALL = "text-embedding-3-small"

```
 |  
| --- | --- |  
options: members: - OpenAIEmbedding
