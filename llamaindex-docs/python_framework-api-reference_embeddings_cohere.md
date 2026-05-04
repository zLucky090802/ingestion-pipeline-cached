# Cohere
##  CohereEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/cohere/#llama_index.embeddings.cohere.CohereEmbedding "Permanent link")
Bases: 
CohereEmbedding uses the Cohere API to generate embeddings for text.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-cohere/llama_index/embeddings/cohere/base.py`  
| 
```
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
489
490
491
```
 | 
```
classCohereEmbedding(MultiModalEmbedding):
"""CohereEmbedding uses the Cohere API to generate embeddings for text."""

    # Instance variables initialized via Pydantic's mechanism
    api_key: str = Field(description="The Cohere API key.")
    base_url: Optional[str] = Field(
        default=None, description="The endpoint to use. Defaults to the Cohere API."
    )
    truncate: str = Field(description="Truncation type - START/ END/ NONE")
    input_type: Optional[str] = Field(
        default=None,
        description="Model Input type. If not provided, search_document and search_query are used when needed.",
    )
    embedding_type: str = Field(
        description="Embedding type. If not provided float embedding_type is used when needed."
    )
    max_retries: int = Field(
        default=DEFAULT_MAX_RETRIES,
        description="Maximum number of retries for API calls.",
    )

    _client: cohere.Client = PrivateAttr()
    _async_client: cohere.AsyncClient = PrivateAttr()
    _timeout: Optional[float] = PrivateAttr()
    _httpx_client: Optional[httpx.Client] = PrivateAttr()
    _httpx_async_client: Optional[httpx.AsyncClient] = PrivateAttr()

    def__init__(
        self,
        # deprecated
        cohere_api_key: Optional[str] = None,
        api_key: Optional[str] = None,
        model_name: str = "embed-english-v3.0",
        truncate: str = "END",
        input_type: Optional[str] = None,
        embedding_type: str = "float",
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        callback_manager: Optional[CallbackManager] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        httpx_client: Optional[httpx.Client] = None,
        httpx_async_client: Optional[httpx.AsyncClient] = None,
        num_workers: Optional[int] = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        **kwargs: Any,
    ):
"""
        A class representation for generating embeddings using the Cohere API.

        Args:
            truncate (str): A string indicating the truncation strategy to be applied to input text. Possible values
                        are 'START', 'END', or 'NONE'.
            input_type (Optional[str]): An optional string that specifies the type of input provided to the model.
                                    This is model-dependent and could be one of the following: 'search_query',
                                    'search_document', 'classification', or 'clustering'.
            model_name (str): The name of the model to be used for generating embeddings. The class ensures that
                          this model is supported and that the input type provided is compatible with the model.
            embed_batch_size (int): The batch size for embedding generation. Maximum allowed value is 96 (MAX_EMBED_BATCH_SIZE)
                                   due to Cohere API limitations. Defaults to DEFAULT_EMBED_BATCH_SIZE.

        """
        # Validate model_name and input_type
        if model_name not in VALID_MODEL_INPUT_TYPES:
            raise ValueError(f"{model_name} is not a valid model name")

        if input_type not in VALID_MODEL_INPUT_TYPES[model_name]:
            raise ValueError(
                f"{input_type} is not a valid input type for the provided model."
            )
        if embedding_type not in VALID_MODEL_EMBEDDING_TYPES[model_name]:
            raise ValueError(
                f"{embedding_type} is not a embedding type for the provided model."
            )

        if truncate not in VALID_TRUNCATE_OPTIONS:
            raise ValueError(f"truncate must be one of {VALID_TRUNCATE_OPTIONS}")

        # Validate embed_batch_size
        if embed_batch_size  MAX_EMBED_BATCH_SIZE:
            raise ValueError(
                f"embed_batch_size {embed_batch_size} exceeds the maximum allowed value of {MAX_EMBED_BATCH_SIZE} for Cohere API"
            )

        super().__init__(
            api_key=api_key or cohere_api_key,
            model_name=model_name,
            input_type=input_type,
            embedding_type=embedding_type,
            truncate=truncate,
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            num_workers=num_workers,
            max_retries=max_retries,
            **kwargs,
        )

        self.base_url = base_url

        self._client = None
        self._async_client = None
        self._timeout = timeout
        self._httpx_client = httpx_client
        self._httpx_async_client = httpx_async_client

    def_get_client(self) -> cohere.ClientV2:
        if self._client is None:
            self._client = cohere.ClientV2(
                api_key=self.api_key,
                client_name="llama_index",
                base_url=self.base_url,
                timeout=self._timeout,
                httpx_client=self._httpx_client,
            )

        return self._client

    def_get_async_client(self) -> cohere.AsyncClientV2:
        if self._async_client is None:
            self._async_client = cohere.AsyncClientV2(
                api_key=self.api_key,
                client_name="llama_index",
                base_url=self.base_url,
                timeout=self._timeout,
                httpx_client=self._httpx_async_client,
            )

        return self._async_client

    @classmethod
    defclass_name(cls) -> str:
        return "CohereEmbedding"

    def_image_to_base64_data_url(self, image_input: Union[str, Path, BytesIO]) -> str:
"""Convert an image to a base64 Data URL."""
        if isinstance(image_input, (str, Path)):
            # If it's a string or Path, assume it's a file path
            image_path = Path(image_input)
            file_extension = image_path.suffix.lower().replace(".", "")
            with open(image_path, "rb") as f:
                image_data = f.read()
        elif isinstance(image_input, BytesIO):
            # If it's a BytesIO, use it directly
            image = Image.open(image_input)
            file_extension = image.format.lower()
            image_input.seek(0)  # Reset the BytesIO stream to the beginning
            image_data = image_input.read()
        else:
            raise ValueError("Unsupported input type. Must be a file path or BytesIO.")

        if self._validate_image_format(file_extension):
            enc_img = base64.b64encode(image_data).decode("utf-8")
            return f"data:image/{file_extension};base64,{enc_img}"
        else:
            raise ValueError(f"Unsupported image format: {file_extension}")

    def_validate_image_format(self, file_type: str) -> bool:
"""Validate image format."""
        return file_type.lower() in SUPPORTED_IMAGE_FORMATS

    def_embed(
        self,
        texts: Optional[List[str]] = None,
        input_type: str = "search_document",
    ) -> List[List[float]]:
"""Embed sentences using Cohere."""
        client = self._get_client()

        if self.model_name not in (V3_MODELS + V4_MODELS):
            input_type = None
        else:
            input_type = self.input_type or input_type

        retry_decorator = _create_retry_decorator(max_retries=self.max_retries)

        @retry_decorator
        def_embed_with_retry() -> List[List[float]]:
            result = client.embed(
                texts=texts,
                input_type=input_type,
                embedding_types=[self.embedding_type],
                model=self.model_name,
                truncate=self.truncate,
            ).embeddings
            return getattr(result, self.embedding_type, None)

        return _embed_with_retry()

    async def_aembed(
        self,
        texts: Optional[List[str]] = None,
        input_type: str = "search_document",
    ) -> List[List[float]]:
"""Embed sentences using Cohere."""
        async_client = self._get_async_client()

        if self.model_name not in (V3_MODELS + V4_MODELS):
            input_type = None
        else:
            input_type = self.input_type or input_type

        retry_decorator = _create_retry_decorator(max_retries=self.max_retries)

        @retry_decorator
        async def_aembed_with_retry() -> List[List[float]]:
            result = (
                await async_client.embed(
                    texts=texts,
                    input_type=input_type,
                    embedding_types=[self.embedding_type],
                    model=self.model_name,
                    truncate=self.truncate,
                )
            ).embeddings
            return getattr(result, self.embedding_type, None)

        return await _aembed_with_retry()

    def_embed_image(
        self, image_paths: List[ImageType], input_type: str
    ) -> List[List[float]]:
"""Embed images using Cohere."""
        if self.model_name not in (V3_MODELS + V4_MODELS):
            raise ValueError(
                f"{self.model_name} is not a valid multi-modal embedding model. Supported models are {V3_MODELS+V4_MODELS}"
            )

        client = self._get_client()
        processed_images = [
            self._image_to_base64_data_url(image_path) for image_path in image_paths
        ]

        inputs = [
            {"content": [{"type": "image_url", "image_url": {"url": processed_image}}]}
            for processed_image in processed_images
        ]

        retry_decorator = _create_retry_decorator(max_retries=self.max_retries)

        @retry_decorator
        def_embed_image_with_retry() -> List[List[float]]:
            embeddings = client.embed(
                inputs=inputs,
                input_type=input_type,
                embedding_types=[self.embedding_type],
                model=self.model_name,
                truncate=self.truncate,
            ).embeddings
            return getattr(embeddings, self.embedding_type, None)

        return _embed_image_with_retry()

    async def_aembed_image(
        self,
        image_paths: List[ImageType],
        input_type: str,
    ) -> List[List[float]]:
"""Embed images using Cohere."""
        if self.model_name not in (V3_MODELS + V4_MODELS):
            raise ValueError(
                f"{self.model_name} is not a valid multi-modal embedding model. Supported models are {V3_MODELS+V4_MODELS}"
            )

        async_client = self._get_async_client()
        processed_images = [
            self._image_to_base64_data_url(image_path) for image_path in image_paths
        ]

        inputs = [
            {"content": [{"type": "image_url", "image_url": {"url": processed_image}}]}
            for processed_image in processed_images
        ]

        retry_decorator = _create_retry_decorator(max_retries=self.max_retries)

        @retry_decorator
        async def_aembed_image_with_retry() -> List[List[float]]:
            embeddings = (
                await async_client.embed(
                    inputs=inputs,
                    input_type=input_type,
                    embedding_types=[self.embedding_type],
                    model=self.model_name,
                    truncate=self.truncate,
                )
            ).embeddings
            return getattr(embeddings, self.embedding_type, None)

        return await _aembed_image_with_retry()

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding. For query embeddings, input_type='search_query'."""
        return self._embed([query], input_type="search_query")[0]

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""Get query embedding async. For query embeddings, input_type='search_query'."""
        return (await self._aembed([query], input_type="search_query"))[0]

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        return self._embed([text], input_type="search_document")[0]

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Get text embedding async."""
        return (await self._aembed([text], input_type="search_document"))[0]

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get text embeddings."""
        return self._embed(texts, input_type="search_document")

    async def_aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get text embeddings."""
        return await self._aembed(texts, input_type="search_document")

    def_get_image_embedding(self, img_file_path: ImageType) -> Embedding:
"""Get image embedding."""
        return self._embed_image([img_file_path], "image")[0]

    async def_aget_image_embedding(self, img_file_path: ImageType) -> Embedding:
"""Get image embedding async."""
        return (await self._aembed_image([img_file_path], "image"))[0]

    def_get_image_embeddings(
        self, img_file_paths: List[ImageType]
    ) -> List[List[float]]:
"""Get image embeddings."""
        return self._embed_image(img_file_paths, "image")

    async def_aget_image_embeddings(
        self, img_file_paths: List[ImageType]
    ) -> List[List[float]]:
"""Get image embeddings async."""
        return await self._aembed_image(img_file_paths, "image")

```
 |  
| --- | --- |  
options: members: - CohereEmbedding
