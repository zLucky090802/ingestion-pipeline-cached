# Voyageai
##  VoyageEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/voyageai/#llama_index.embeddings.voyageai.VoyageEmbedding "Permanent link")
Bases: 
Class for Voyage embeddings.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model_name`  |  Model for embedding. Defaults to "voyage-01".  |  _required_  |  
|  `voyage_api_key`  |  `Optional[str]`  |  Voyage API key. Defaults to None. You can either specify the key here or store it as an environment variable.  |  `None`  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-voyageai/llama_index/embeddings/voyageai/base.py`  
| 
```
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
492
493
494
495
```
 | 
```
classVoyageEmbedding(MultiModalEmbedding):
"""
    Class for Voyage embeddings.

    Args:
        model_name (str): Model for embedding.
            Defaults to "voyage-01".

        voyage_api_key (Optional[str]): Voyage API key. Defaults to None.
            You can either specify the key here or store it as an environment variable.

    """

    _client: voyageai.Client = PrivateAttr(None)
    _aclient: voyageai.AsyncClient = PrivateAttr()
    truncation: Optional[bool] = None
    output_dtype: Optional[str] = None
    output_dimension: Optional[int] = None

    def__init__(
        self,
        model_name: str,
        voyage_api_key: Optional[str] = None,
        embed_batch_size: Optional[int] = None,
        truncation: Optional[bool] = None,
        output_dtype: Optional[str] = None,
        output_dimension: Optional[int] = None,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ):
        if model_name in [
            "voyage-01",
            "voyage-lite-01",
            "voyage-lite-01-instruct",
            "voyage-02",
            "voyage-2",
            "voyage-lite-02-instruct",
            "voyage-large-2",
            "voyage-large-2-instruct",
            "voyage-multilingual-2",
            "voyage-3",
            "voyage-3-lite",
        ]:
            logger.warning(
                f"{model_name} is not the latest model by Voyage AI. Please note that `model_name` "
                "will be a required argument in the future. We recommend setting it explicitly. Please see "
                "https://docs.voyageai.com/docs/embeddings for the latest models offered by Voyage AI."
            )

        if embed_batch_size is None:
            embed_batch_size = MAX_BATCH_SIZE

        super().__init__(
            model_name=model_name,
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            **kwargs,
        )

        self._client = voyageai.Client(api_key=voyage_api_key)
        self._aclient = voyageai.AsyncClient(api_key=voyage_api_key)
        self.truncation = truncation
        self.output_dtype = output_dtype
        self.output_dimension = output_dimension

    @classmethod
    defclass_name(cls) -> str:
        return "VoyageEmbedding"

    @staticmethod
    def_validate_image_format(file_type: str) -> bool:
"""Validate image format."""
        return file_type.lower() in SUPPORTED_IMAGE_FORMATS

    @staticmethod
    def_validate_video_format(file_type: str) -> bool:
"""Validate video format."""
        return file_type.lower() in SUPPORTED_VIDEO_FORMATS

    @classmethod
    def_texts_to_content(cls, input_strs: List[str]) -> List[dict]:
        return [{"content": [{"type": "text", "text": x}]} for x in input_strs]

    def_build_batches(
        self, texts: List[str]
    ) -> Generator[Tuple[List[str], int], None, None]:
"""Generate batches of texts based on token limits."""
        max_tokens_per_batch = VOYAGE_TOTAL_TOKEN_LIMITS.get(self.model_name, 120_000)
        index = 0

        while index  len(texts):
            batch: List[str] = []
            batch_tokens = 0
            while (
                index  len(texts)
                and len(batch)  min(self.embed_batch_size, MAX_BATCH_SIZE)
                and batch_tokens  max_tokens_per_batch
            ):
                n_tokens = len(
                    self._client.tokenize([texts[index]], model=self.model_name)[0]
                )
                if batch_tokens + n_tokens  max_tokens_per_batch and len(batch)  0:
                    break
                batch_tokens += n_tokens
                batch.append(texts[index])
                index += 1

            yield batch, len(batch)

    def_image_to_content(self, image_input: Union[str, Path, BytesIO]) -> Image:
"""Convert an image to a base64 Data URL."""
        if isinstance(image_input, (str, Path)):
            image = Image.open(str(image_input))
            # If it's a string or Path, assume it's a file path
            image_path = str(image_input)
            file_extension = os.path.splitext(image_path)[1][1:].lower()
        elif isinstance(image_input, BytesIO):
            # If it's a BytesIO, use it directly
            image = Image.open(image_input)
            file_extension = image.format.lower()
            image_input.seek(0)  # Reset the BytesIO stream to the beginning
        else:
            raise ValueError("Unsupported input type. Must be a file path or BytesIO.")

        if self._validate_image_format(file_extension):
            return image
        else:
            raise ValueError(f"Unsupported image format: {file_extension}")

    def_embed_image(
        self, image_path: ImageType, input_type: Optional[str] = None
    ) -> List[float]:
"""Embed images using VoyageAI."""
        if self.model_name not in MULTIMODAL_MODELS:
            raise ValueError(
                f"{self.model_name} is not a valid multi-modal embedding model. Supported models are {MULTIMODAL_MODELS}"
            )
        processed_image = self._image_to_content(image_path)
        return self._client.multimodal_embed(
            model=self.model_name,
            inputs=[[processed_image]],
            input_type=input_type,
            truncation=self.truncation if self.truncation is not None else True,
        ).embeddings[0]

    async def_aembed_image(
        self, image_path: ImageType, input_type: Optional[str] = None
    ) -> List[float]:
"""Embed images using VoyageAI."""
        if self.model_name not in MULTIMODAL_MODELS:
            raise ValueError(
                f"{self.model_name} is not a valid multi-modal embedding model. Supported models are {MULTIMODAL_MODELS}"
            )
        processed_image = self._image_to_content(image_path)
        return (
            await self._aclient.multimodal_embed(
                model=self.model_name,
                inputs=[[processed_image]],
                input_type=input_type,
                truncation=self.truncation if self.truncation is not None else True,
            )
        ).embeddings[0]

    def_get_image_embedding(self, img_file_path: ImageType) -> Embedding:
        return self._embed_image(img_file_path)

    async def_aget_image_embedding(self, img_file_path: ImageType) -> Embedding:
        return await self._aembed_image(img_file_path)

    def_video_to_content(self, video_input: Union[str, Path]) -> Any:
"""Convert a video file path to a Video object for embedding."""
        if not VIDEO_SUPPORT:
            raise ImportError(
                "Video support requires voyageai>=0.3.6. "
                "Please upgrade: pip install 'voyageai>=0.3.6'"
            )

        if not isinstance(video_input, (str, Path)):
            raise ValueError("Video input must be a file path (str or Path).")

        video_path = str(video_input)
        file_extension = os.path.splitext(video_path)[1][1:].lower()

        if not self._validate_video_format(file_extension):
            raise ValueError(
                f"Unsupported video format: {file_extension}. "
                f"Supported formats: {SUPPORTED_VIDEO_FORMATS}"
            )

        return Video.from_path(video_path, model=self.model_name)  # type: ignore[union-attr]

    defget_video_embedding(
        self, video_path: Union[str, Path], input_type: Optional[str] = None
    ) -> List[float]:
"""
        Get embedding for a video file.

        Only supported with voyage-multimodal-3.5 model.
        Requires voyageai>=0.3.6 for video support.

        Args:
            video_path: Path to the video file (max 20MB).
            input_type: Optional input type for the embedding.

        Returns:
            List of floats representing the video embedding.

        """
        if self.model_name not in VIDEO_MODELS:
            raise ValueError(
                f"{self.model_name} does not support video embeddings. "
                f"Supported models: {VIDEO_MODELS}"
            )

        video = self._video_to_content(video_path)
        return self._client.multimodal_embed(
            model=self.model_name,
            inputs=[[video]],
            input_type=input_type,
            truncation=self.truncation if self.truncation is not None else True,
        ).embeddings[0]

    async defaget_video_embedding(
        self, video_path: Union[str, Path], input_type: Optional[str] = None
    ) -> List[float]:
"""
        Asynchronously get embedding for a video file.

        Only supported with voyage-multimodal-3.5 model.

        Args:
            video_path: Path to the video file (max 20MB).
            input_type: Optional input type for the embedding.

        Returns:
            List of floats representing the video embedding.

        """
        if self.model_name not in VIDEO_MODELS:
            raise ValueError(
                f"{self.model_name} does not support video embeddings. "
                f"Supported models: {VIDEO_MODELS}"
            )

        video = self._video_to_content(video_path)
        return (
            await self._aclient.multimodal_embed(
                model=self.model_name,
                inputs=[[video]],
                input_type=input_type,
                truncation=self.truncation if self.truncation is not None else True,
            )
        ).embeddings[0]

    defget_video_embeddings(
        self, video_paths: List[Union[str, Path]], input_type: Optional[str] = None
    ) -> List[List[float]]:
"""
        Get embeddings for multiple video files.

        Only supported with voyage-multimodal-3.5 model.

        Args:
            video_paths: List of paths to video files (each max 20MB).
            input_type: Optional input type for the embeddings.

        Returns:
            List of embeddings, one for each video.

        """
        if self.model_name not in VIDEO_MODELS:
            raise ValueError(
                f"{self.model_name} does not support video embeddings. "
                f"Supported models: {VIDEO_MODELS}"
            )

        videos = [[self._video_to_content(path)] for path in video_paths]
        return self._client.multimodal_embed(
            model=self.model_name,
            inputs=videos,
            input_type=input_type,
            truncation=self.truncation if self.truncation is not None else True,
        ).embeddings

    async defaget_video_embeddings(
        self, video_paths: List[Union[str, Path]], input_type: Optional[str] = None
    ) -> List[List[float]]:
"""
        Asynchronously get embeddings for multiple video files.

        Only supported with voyage-multimodal-3.5 model.

        Args:
            video_paths: List of paths to video files (each max 20MB).
            input_type: Optional input type for the embeddings.

        Returns:
            List of embeddings, one for each video.

        """
        if self.model_name not in VIDEO_MODELS:
            raise ValueError(
                f"{self.model_name} does not support video embeddings. "
                f"Supported models: {VIDEO_MODELS}"
            )

        videos = [[self._video_to_content(path)] for path in video_paths]
        return (
            await self._aclient.multimodal_embed(
                model=self.model_name,
                inputs=videos,
                input_type=input_type,
                truncation=self.truncation if self.truncation is not None else True,
            )
        ).embeddings

    def_embed(self, texts: List[str], input_type: str) -> List[List[float]]:
"""Embed texts with dynamic batching based on token limits."""
        embeddings: List[List[float]] = []

        for batch, _ in self._build_batches(texts):
            if self.model_name in CONTEXT_MODELS:
                r = self._client.contextualized_embed(
                    inputs=[batch],
                    model=self.model_name,
                    input_type=input_type,
                    output_dtype=self.output_dtype,
                    output_dimension=self.output_dimension,
                ).results
                embeddings.extend(r[0].embeddings)
            elif self.model_name in MULTIMODAL_MODELS:
                batch_embeddings = self._client.multimodal_embed(
                    inputs=self._texts_to_content(batch),
                    model=self.model_name,
                    input_type=input_type,
                    truncation=self.truncation if self.truncation is not None else True,
                ).embeddings
                embeddings.extend(batch_embeddings)
            else:
                batch_embeddings = self._client.embed(
                    batch,
                    model=self.model_name,
                    input_type=input_type,
                    truncation=self.truncation,
                    output_dtype=self.output_dtype,
                    output_dimension=self.output_dimension,
                ).embeddings
                embeddings.extend(batch_embeddings)

        return embeddings

    async def_aembed(self, texts: List[str], input_type: str) -> List[List[float]]:
"""Asynchronously embed texts with dynamic batching based on token limits."""
        embeddings: List[List[float]] = []

        for batch, _ in self._build_batches(texts):
            if self.model_name in CONTEXT_MODELS:
                ar = await self._aclient.contextualized_embed(
                    inputs=[batch],
                    model=self.model_name,
                    input_type=input_type,
                    output_dtype=self.output_dtype,
                    output_dimension=self.output_dimension,
                )
                r = ar.results
                embeddings.extend(r[0].embeddings)
            elif self.model_name in MULTIMODAL_MODELS:
                r = await self._aclient.multimodal_embed(
                    inputs=self._texts_to_content(batch),
                    model=self.model_name,
                    input_type=input_type,
                    truncation=self.truncation if self.truncation is not None else True,
                )
                embeddings.extend(r.embeddings)
            else:
                r = await self._aclient.embed(
                    batch,
                    model=self.model_name,
                    input_type=input_type,
                    truncation=self.truncation,
                    output_dtype=self.output_dtype,
                    output_dimension=self.output_dimension,
                )
                embeddings.extend(r.embeddings)

        return embeddings

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        return self._embed([query], input_type="query")[0]

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""The asynchronous version of _get_query_embedding."""
        r = await self._aembed([query], input_type="query")
        return r[0]

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        return self._embed([text], input_type="document")[0]

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Asynchronously get text embedding."""
        r = await self._aembed([text], input_type="document")
        return r[0]

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get text embeddings."""
        return self._embed(texts, input_type="document")

    async def_aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Asynchronously get text embeddings."""
        return await self._aembed(texts, input_type="document")

    defget_general_text_embedding(
        self, text: str, input_type: Optional[str] = None
    ) -> List[float]:
"""Get general text embedding with input_type."""
        return self._embed([text], input_type=input_type)[0]

    async defaget_general_text_embedding(
        self, text: str, input_type: Optional[str] = None
    ) -> List[float]:
"""Asynchronously get general text embedding with input_type."""
        r = await self._aembed([text], input_type=input_type)
        return r[0]

```
 |  
| --- | --- |  
###  get_video_embedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/voyageai/#llama_index.embeddings.voyageai.VoyageEmbedding.get_video_embedding "Permanent link")

```
get_video_embedding(
    video_path: Union[, ],
    input_type: Optional[] = None,
) -> [float]

```

Get embedding for a video file.
Only supported with voyage-multimodal-3.5 model. Requires voyageai>=0.3.6 for video support.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `video_path`  |  `Union[str, Path]`  |  Path to the video file (max 20MB).  |  _required_  |  
|  `input_type`  |  `Optional[str]`  |  Optional input type for the embedding.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[float]`  |  List of floats representing the video embedding.  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-voyageai/llama_index/embeddings/voyageai/base.py`  
| 
```
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
```
 | 
```
defget_video_embedding(
    self, video_path: Union[str, Path], input_type: Optional[str] = None
) -> List[float]:
"""
    Get embedding for a video file.

    Only supported with voyage-multimodal-3.5 model.
    Requires voyageai>=0.3.6 for video support.

    Args:
        video_path: Path to the video file (max 20MB).
        input_type: Optional input type for the embedding.

    Returns:
        List of floats representing the video embedding.

    """
    if self.model_name not in VIDEO_MODELS:
        raise ValueError(
            f"{self.model_name} does not support video embeddings. "
            f"Supported models: {VIDEO_MODELS}"
        )

    video = self._video_to_content(video_path)
    return self._client.multimodal_embed(
        model=self.model_name,
        inputs=[[video]],
        input_type=input_type,
        truncation=self.truncation if self.truncation is not None else True,
    ).embeddings[0]

```
 |  
| --- | --- |  
###  aget_video_embedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/voyageai/#llama_index.embeddings.voyageai.VoyageEmbedding.aget_video_embedding "Permanent link")

```
aget_video_embedding(
    video_path: Union[, ],
    input_type: Optional[] = None,
) -> [float]

```

Asynchronously get embedding for a video file.
Only supported with voyage-multimodal-3.5 model.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `video_path`  |  `Union[str, Path]`  |  Path to the video file (max 20MB).  |  _required_  |  
|  `input_type`  |  `Optional[str]`  |  Optional input type for the embedding.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[float]`  |  List of floats representing the video embedding.  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-voyageai/llama_index/embeddings/voyageai/base.py`  
| 
```
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
```
 | 
```
async defaget_video_embedding(
    self, video_path: Union[str, Path], input_type: Optional[str] = None
) -> List[float]:
"""
    Asynchronously get embedding for a video file.

    Only supported with voyage-multimodal-3.5 model.

    Args:
        video_path: Path to the video file (max 20MB).
        input_type: Optional input type for the embedding.

    Returns:
        List of floats representing the video embedding.

    """
    if self.model_name not in VIDEO_MODELS:
        raise ValueError(
            f"{self.model_name} does not support video embeddings. "
            f"Supported models: {VIDEO_MODELS}"
        )

    video = self._video_to_content(video_path)
    return (
        await self._aclient.multimodal_embed(
            model=self.model_name,
            inputs=[[video]],
            input_type=input_type,
            truncation=self.truncation if self.truncation is not None else True,
        )
    ).embeddings[0]

```
 |  
| --- | --- |  
###  get_video_embeddings [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/voyageai/#llama_index.embeddings.voyageai.VoyageEmbedding.get_video_embeddings "Permanent link")

```
get_video_embeddings(
    video_paths: [Union[, ]],
    input_type: Optional[] = None,
) -> [[float]]

```

Get embeddings for multiple video files.
Only supported with voyage-multimodal-3.5 model.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `video_paths`  |  `List[Union[str, Path]]`  |  List of paths to video files (each max 20MB).  |  _required_  |  
|  `input_type`  |  `Optional[str]`  |  Optional input type for the embeddings.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[List[float]]`  |  List of embeddings, one for each video.  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-voyageai/llama_index/embeddings/voyageai/base.py`  
| 
```
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
```
 | 
```
defget_video_embeddings(
    self, video_paths: List[Union[str, Path]], input_type: Optional[str] = None
) -> List[List[float]]:
"""
    Get embeddings for multiple video files.

    Only supported with voyage-multimodal-3.5 model.

    Args:
        video_paths: List of paths to video files (each max 20MB).
        input_type: Optional input type for the embeddings.

    Returns:
        List of embeddings, one for each video.

    """
    if self.model_name not in VIDEO_MODELS:
        raise ValueError(
            f"{self.model_name} does not support video embeddings. "
            f"Supported models: {VIDEO_MODELS}"
        )

    videos = [[self._video_to_content(path)] for path in video_paths]
    return self._client.multimodal_embed(
        model=self.model_name,
        inputs=videos,
        input_type=input_type,
        truncation=self.truncation if self.truncation is not None else True,
    ).embeddings

```
 |  
| --- | --- |  
###  aget_video_embeddings [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/voyageai/#llama_index.embeddings.voyageai.VoyageEmbedding.aget_video_embeddings "Permanent link")

```
aget_video_embeddings(
    video_paths: [Union[, ]],
    input_type: Optional[] = None,
) -> [[float]]

```

Asynchronously get embeddings for multiple video files.
Only supported with voyage-multimodal-3.5 model.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `video_paths`  |  `List[Union[str, Path]]`  |  List of paths to video files (each max 20MB).  |  _required_  |  
|  `input_type`  |  `Optional[str]`  |  Optional input type for the embeddings.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[List[float]]`  |  List of embeddings, one for each video.  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-voyageai/llama_index/embeddings/voyageai/base.py`  
| 
```
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
```
 | 
```
async defaget_video_embeddings(
    self, video_paths: List[Union[str, Path]], input_type: Optional[str] = None
) -> List[List[float]]:
"""
    Asynchronously get embeddings for multiple video files.

    Only supported with voyage-multimodal-3.5 model.

    Args:
        video_paths: List of paths to video files (each max 20MB).
        input_type: Optional input type for the embeddings.

    Returns:
        List of embeddings, one for each video.

    """
    if self.model_name not in VIDEO_MODELS:
        raise ValueError(
            f"{self.model_name} does not support video embeddings. "
            f"Supported models: {VIDEO_MODELS}"
        )

    videos = [[self._video_to_content(path)] for path in video_paths]
    return (
        await self._aclient.multimodal_embed(
            model=self.model_name,
            inputs=videos,
            input_type=input_type,
            truncation=self.truncation if self.truncation is not None else True,
        )
    ).embeddings

```
 |  
| --- | --- |  
###  get_general_text_embedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/voyageai/#llama_index.embeddings.voyageai.VoyageEmbedding.get_general_text_embedding "Permanent link")

```
get_general_text_embedding(
    text: , input_type: Optional[] = None
) -> [float]

```

Get general text embedding with input_type.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-voyageai/llama_index/embeddings/voyageai/base.py`  
| 
```
484
485
486
487
488
```
 | 
```
defget_general_text_embedding(
    self, text: str, input_type: Optional[str] = None
) -> List[float]:
"""Get general text embedding with input_type."""
    return self._embed([text], input_type=input_type)[0]

```
 |  
| --- | --- |  
###  aget_general_text_embedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/voyageai/#llama_index.embeddings.voyageai.VoyageEmbedding.aget_general_text_embedding "Permanent link")

```
aget_general_text_embedding(
    text: , input_type: Optional[] = None
) -> [float]

```

Asynchronously get general text embedding with input_type.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-voyageai/llama_index/embeddings/voyageai/base.py`  
| 
```
490
491
492
493
494
495
```
 | 
```
async defaget_general_text_embedding(
    self, text: str, input_type: Optional[str] = None
) -> List[float]:
"""Asynchronously get general text embedding with input_type."""
    r = await self._aembed([text], input_type=input_type)
    return r[0]

```
 |  
| --- | --- |  
options: members: - VoyageEmbedding
