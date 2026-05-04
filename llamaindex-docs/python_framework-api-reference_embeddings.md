# Index
##  BaseEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.BaseEmbedding "Permanent link")
Bases: , `DispatcherSpanMixin`
Base class for embeddings.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model_name`  |  The name of the embedding model.  |  `'unknown'`  |  
|  `embed_batch_size`  |  The batch size for embedding calls.  |  
|  `callback_manager`  |   |  `<llama_index.core.callbacks.base.CallbackManager object at 0x7f00a8c2ae50>`  |  
|  `num_workers`  |  `int | None`  |  The number of workers to use for async embedding calls.  |  `None`  |  
|  `embeddings_cache`  |  `Any | None`  |  Cache for the embeddings: if None, the embeddings are not cached  |  `None`  |  
|  `rate_limiter`  |  `Any | None`  |  Rate limiter instance to throttle API calls.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/base/embeddings/base.py`  
| 
```
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
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
```
 | 
```
classBaseEmbedding(TransformComponent, DispatcherSpanMixin):
"""Base class for embeddings."""

    model_config = ConfigDict(
        protected_namespaces=("pydantic_model_",), arbitrary_types_allowed=True
    )
    model_name: str = Field(
        default="unknown", description="The name of the embedding model."
    )
    embed_batch_size: int = Field(
        default=DEFAULT_EMBED_BATCH_SIZE,
        description="The batch size for embedding calls.",
        gt=0,
        le=2048,
    )
    callback_manager: CallbackManager = Field(
        default_factory=lambda: CallbackManager([]), exclude=True
    )
    num_workers: Optional[int] = Field(
        default=None,
        description="The number of workers to use for async embedding calls.",
    )
    # Use Any to avoid import loops
    embeddings_cache: Optional[Any] = Field(
        default=None,
        description="Cache for the embeddings: if None, the embeddings are not cached",
    )
    # Expected type: BaseRateLimiter (from llama_index.core.rate_limiter)
    rate_limiter: Optional[Any] = Field(
        default=None,
        description="Rate limiter instance to throttle API calls.",
        exclude=True,
    )

    @model_validator(mode="after")
    defcheck_base_embeddings_class(self) -> Self:
        fromllama_index.core.storage.kvstore.typesimport BaseKVStore

        if self.callback_manager is None:
            self.callback_manager = CallbackManager([])
        if self.embeddings_cache is not None and not isinstance(
            self.embeddings_cache, BaseKVStore
        ):
            raise TypeError("embeddings_cache must be of type BaseKVStore")
        return self

    @abstractmethod
    def_get_query_embedding(self, query: str) -> Embedding:
"""
        Embed the input query synchronously.

        Subclasses should implement this method. Reference get_query_embedding's
        docstring for more information.
        """

    @abstractmethod
    async def_aget_query_embedding(self, query: str) -> Embedding:
"""
        Embed the input query asynchronously.

        Subclasses should implement this method. Reference get_query_embedding's
        docstring for more information.
        """

    @dispatcher.span
    defget_query_embedding(self, query: str) -> Embedding:
"""
        Embed the input query.

        When embedding a query, depending on the model, a special instruction
        can be prepended to the raw query string. For example, "Represent the
        question for retrieving supporting documents: ". If you're curious,
        other examples of predefined instructions can be found in
        embeddings/huggingface_utils.py.
        """
        model_dict = self.to_dict()
        model_dict.pop("api_key", None)
        dispatcher.event(
            EmbeddingStartEvent(
                model_dict=model_dict,
            )
        )
        with self.callback_manager.event(
            CBEventType.EMBEDDING, payload={EventPayload.SERIALIZED: self.to_dict()}
        ) as event:
            if not self.embeddings_cache:
                if self.rate_limiter is not None:
                    self.rate_limiter.acquire()
                query_embedding = self._get_query_embedding(query)
            elif self.embeddings_cache is not None:
                cached_emb = self.embeddings_cache.get(
                    key=query, collection="embeddings"
                )
                if cached_emb is not None:
                    cached_key = next(iter(cached_emb.keys()))
                    query_embedding = cached_emb[cached_key]
                else:
                    if self.rate_limiter is not None:
                        self.rate_limiter.acquire()
                    query_embedding = self._get_query_embedding(query)
                    self.embeddings_cache.put(
                        key=query,
                        val={str(uuid.uuid4()): query_embedding},
                        collection="embeddings",
                    )
            event.on_end(
                payload={
                    EventPayload.CHUNKS: [query],
                    EventPayload.EMBEDDINGS: [query_embedding],
                },
            )
        dispatcher.event(
            EmbeddingEndEvent(
                chunks=[query],
                embeddings=[query_embedding],
            )
        )
        return query_embedding

    @dispatcher.span
    async defaget_query_embedding(self, query: str) -> Embedding:
"""Get query embedding."""
        model_dict = self.to_dict()
        model_dict.pop("api_key", None)
        dispatcher.event(
            EmbeddingStartEvent(
                model_dict=model_dict,
            )
        )
        with self.callback_manager.event(
            CBEventType.EMBEDDING, payload={EventPayload.SERIALIZED: self.to_dict()}
        ) as event:
            if not self.embeddings_cache:
                if self.rate_limiter is not None:
                    await self.rate_limiter.async_acquire()
                query_embedding = await self._aget_query_embedding(query)
            elif self.embeddings_cache is not None:
                cached_emb = await self.embeddings_cache.aget(
                    key=query, collection="embeddings"
                )
                if cached_emb is not None:
                    cached_key = next(iter(cached_emb.keys()))
                    query_embedding = cached_emb[cached_key]
                else:
                    if self.rate_limiter is not None:
                        await self.rate_limiter.async_acquire()
                    query_embedding = await self._aget_query_embedding(query)
                    await self.embeddings_cache.aput(
                        key=query,
                        val={str(uuid.uuid4()): query_embedding},
                        collection="embeddings",
                    )

            event.on_end(
                payload={
                    EventPayload.CHUNKS: [query],
                    EventPayload.EMBEDDINGS: [query_embedding],
                },
            )
        dispatcher.event(
            EmbeddingEndEvent(
                chunks=[query],
                embeddings=[query_embedding],
            )
        )
        return query_embedding

    defget_agg_embedding_from_queries(
        self,
        queries: List[str],
        agg_fn: Optional[Callable[..., Embedding]] = None,
    ) -> Embedding:
"""Get aggregated embedding from multiple queries."""
        query_embeddings = [self.get_query_embedding(query) for query in queries]
        agg_fn = agg_fn or mean_agg
        return agg_fn(query_embeddings)

    async defaget_agg_embedding_from_queries(
        self,
        queries: List[str],
        agg_fn: Optional[Callable[..., Embedding]] = None,
    ) -> Embedding:
"""Async get aggregated embedding from multiple queries."""
        query_embeddings = [await self.aget_query_embedding(query) for query in queries]
        agg_fn = agg_fn or mean_agg
        return agg_fn(query_embeddings)

    @abstractmethod
    def_get_text_embedding(self, text: str) -> Embedding:
"""
        Embed the input text synchronously.

        Subclasses should implement this method. Reference get_text_embedding's
        docstring for more information.
        """

    async def_aget_text_embedding(self, text: str) -> Embedding:
"""
        Embed the input text asynchronously.

        Subclasses can implement this method if there is a true async
        implementation. Reference get_text_embedding's docstring for more
        information.
        """
        # Default implementation just falls back on _get_text_embedding
        return self._get_text_embedding(text)

    def_get_text_embeddings(self, texts: List[str]) -> List[Embedding]:
"""
        Embed the input sequence of text synchronously.

        Subclasses can implement this method if batch queries are supported.
        """
        # Default implementation just loops over _get_text_embedding
        return [self._get_text_embedding(text) for text in texts]

    async def_aget_text_embeddings(self, texts: List[str]) -> List[Embedding]:
"""
        Embed the input sequence of text asynchronously.

        Subclasses can implement this method if batch queries are supported.
        """
        return await asyncio.gather(
            *[self._aget_text_embedding(text) for text in texts]
        )

    async def_aget_text_embeddings_rate_limited(
        self, texts: List[str]
    ) -> List[Embedding]:
"""Acquire rate limiter before delegating to _aget_text_embeddings."""
        if self.rate_limiter is not None:
            await self.rate_limiter.async_acquire()
        return await self._aget_text_embeddings(texts)

    def_get_text_embeddings_cached(self, texts: List[str]) -> List[Embedding]:
"""
        Get text embeddings from cache. If not in cache, generate them.
        """
        if self.embeddings_cache is None:
            raise ValueError("embeddings_cache must be defined")

        embeddings: List[Optional[Embedding]] = [None for i in range(len(texts))]
        # Tuples of (index, text) to be able to keep same order of embeddings
        non_cached_texts: List[Tuple[int, str]] = []
        for i, txt in enumerate(texts):
            cached_emb = self.embeddings_cache.get(key=txt, collection="embeddings")
            if cached_emb is not None:
                cached_key = next(iter(cached_emb.keys()))
                embeddings[i] = cached_emb[cached_key]
            else:
                non_cached_texts.append((i, txt))
        if len(non_cached_texts)  0:
            text_embeddings = self._get_text_embeddings(
                [x[1] for x in non_cached_texts]
            )
            for j, text_embedding in enumerate(text_embeddings):
                orig_i = non_cached_texts[j][0]
                embeddings[orig_i] = text_embedding

                self.embeddings_cache.put(
                    key=texts[orig_i],
                    val={str(uuid.uuid4()): text_embedding},
                    collection="embeddings",
                )
        return cast(List[Embedding], embeddings)

    async def_aget_text_embeddings_cached(self, texts: List[str]) -> List[Embedding]:
"""
        Asynchronously get text embeddings from cache. If not in cache, generate them.
        """
        if self.embeddings_cache is None:
            raise ValueError("embeddings_cache must be defined")

        embeddings: List[Optional[Embedding]] = [None for i in range(len(texts))]
        # Tuples of (index, text) to be able to keep same order of embeddings
        non_cached_texts: List[Tuple[int, str]] = []
        for i, txt in enumerate(texts):
            cached_emb = await self.embeddings_cache.aget(
                key=txt, collection="embeddings"
            )
            if cached_emb is not None:
                cached_key = next(iter(cached_emb.keys()))
                embeddings[i] = cached_emb[cached_key]
            else:
                non_cached_texts.append((i, txt))

        if len(non_cached_texts)  0:
            text_embeddings = await self._aget_text_embeddings(
                [x[1] for x in non_cached_texts]
            )
            for j, text_embedding in enumerate(text_embeddings):
                orig_i = non_cached_texts[j][0]
                embeddings[orig_i] = text_embedding
                await self.embeddings_cache.aput(
                    key=texts[orig_i],
                    val={str(uuid.uuid4()): text_embedding},
                    collection="embeddings",
                )
        return cast(List[Embedding], embeddings)

    @dispatcher.span
    defget_text_embedding(self, text: str) -> Embedding:
"""
        Embed the input text.

        When embedding text, depending on the model, a special instruction
        can be prepended to the raw text string. For example, "Represent the
        document for retrieval: ". If you're curious, other examples of
        predefined instructions can be found in embeddings/huggingface_utils.py.
        """
        model_dict = self.to_dict()
        model_dict.pop("api_key", None)
        dispatcher.event(
            EmbeddingStartEvent(
                model_dict=model_dict,
            )
        )
        with self.callback_manager.event(
            CBEventType.EMBEDDING, payload={EventPayload.SERIALIZED: self.to_dict()}
        ) as event:
            if not self.embeddings_cache:
                if self.rate_limiter is not None:
                    self.rate_limiter.acquire()
                text_embedding = self._get_text_embedding(text)
            elif self.embeddings_cache is not None:
                cached_emb = self.embeddings_cache.get(
                    key=text, collection="embeddings"
                )
                if cached_emb is not None:
                    cached_key = next(iter(cached_emb.keys()))
                    text_embedding = cached_emb[cached_key]
                else:
                    if self.rate_limiter is not None:
                        self.rate_limiter.acquire()
                    text_embedding = self._get_text_embedding(text)
                    self.embeddings_cache.put(
                        key=text,
                        val={str(uuid.uuid4()): text_embedding},
                        collection="embeddings",
                    )

            event.on_end(
                payload={
                    EventPayload.CHUNKS: [text],
                    EventPayload.EMBEDDINGS: [text_embedding],
                }
            )
        dispatcher.event(
            EmbeddingEndEvent(
                chunks=[text],
                embeddings=[text_embedding],
            )
        )
        return text_embedding

    @dispatcher.span
    async defaget_text_embedding(self, text: str) -> Embedding:
"""Async get text embedding."""
        model_dict = self.to_dict()
        model_dict.pop("api_key", None)
        dispatcher.event(
            EmbeddingStartEvent(
                model_dict=model_dict,
            )
        )
        with self.callback_manager.event(
            CBEventType.EMBEDDING, payload={EventPayload.SERIALIZED: self.to_dict()}
        ) as event:
            if not self.embeddings_cache:
                if self.rate_limiter is not None:
                    await self.rate_limiter.async_acquire()
                text_embedding = await self._aget_text_embedding(text)
            elif self.embeddings_cache is not None:
                cached_emb = await self.embeddings_cache.aget(
                    key=text, collection="embeddings"
                )
                if cached_emb is not None:
                    cached_key = next(iter(cached_emb.keys()))
                    text_embedding = cached_emb[cached_key]
                else:
                    if self.rate_limiter is not None:
                        await self.rate_limiter.async_acquire()
                    text_embedding = await self._aget_text_embedding(text)
                    await self.embeddings_cache.aput(
                        key=text,
                        val={str(uuid.uuid4()): text_embedding},
                        collection="embeddings",
                    )

            event.on_end(
                payload={
                    EventPayload.CHUNKS: [text],
                    EventPayload.EMBEDDINGS: [text_embedding],
                }
            )
        dispatcher.event(
            EmbeddingEndEvent(
                chunks=[text],
                embeddings=[text_embedding],
            )
        )
        return text_embedding

    @dispatcher.span
    defget_text_embedding_batch(
        self,
        texts: List[str],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[Embedding]:
"""Get a list of text embeddings, with batching."""
        cur_batch: List[str] = []
        result_embeddings: List[Embedding] = []

        queue_with_progress = enumerate(
            get_tqdm_iterable(texts, show_progress, "Generating embeddings")
        )

        model_dict = self.to_dict()
        model_dict.pop("api_key", None)
        for idx, text in queue_with_progress:
            cur_batch.append(text)
            if idx == len(texts) - 1 or len(cur_batch) == self.embed_batch_size:
                # flush
                dispatcher.event(
                    EmbeddingStartEvent(
                        model_dict=model_dict,
                    )
                )
                with self.callback_manager.event(
                    CBEventType.EMBEDDING,
                    payload={EventPayload.SERIALIZED: self.to_dict()},
                ) as event:
                    if self.rate_limiter is not None:
                        self.rate_limiter.acquire()
                    if not self.embeddings_cache:
                        embeddings = self._get_text_embeddings(cur_batch)
                    elif self.embeddings_cache is not None:
                        embeddings = self._get_text_embeddings_cached(cur_batch)
                    result_embeddings.extend(embeddings)
                    event.on_end(
                        payload={
                            EventPayload.CHUNKS: cur_batch,
                            EventPayload.EMBEDDINGS: embeddings,
                        },
                    )
                dispatcher.event(
                    EmbeddingEndEvent(
                        chunks=cur_batch,
                        embeddings=embeddings,
                    )
                )
                cur_batch = []

        return result_embeddings

    @dispatcher.span
    async defaget_text_embedding_batch(
        self,
        texts: List[str],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[Embedding]:
"""Asynchronously get a list of text embeddings, with batching."""
        num_workers = self.num_workers

        model_dict = self.to_dict()
        model_dict.pop("api_key", None)

        cur_batch: List[str] = []
        embeddings_coroutines: List[Coroutine] = []
        callback_payloads: List[Tuple[str, List[str]]] = []

        # for idx, text in queue_with_progress:
        for idx, text in enumerate(texts):
            cur_batch.append(text)
            if idx == len(texts) - 1 or len(cur_batch) == self.embed_batch_size:
                # flush
                dispatcher.event(
                    EmbeddingStartEvent(
                        model_dict=model_dict,
                    )
                )
                event_id = self.callback_manager.on_event_start(
                    CBEventType.EMBEDDING,
                    payload={EventPayload.SERIALIZED: self.to_dict()},
                )
                callback_payloads.append((event_id, cur_batch))

                if not self.embeddings_cache:
                    embeddings_coroutines.append(
                        self._aget_text_embeddings_rate_limited(cur_batch)
                    )
                elif self.embeddings_cache is not None:
                    embeddings_coroutines.append(
                        self._aget_text_embeddings_cached(cur_batch)
                    )

                cur_batch = []

        # flatten the results of asyncio.gather, which is a list of embeddings lists
        if len(embeddings_coroutines)  0:
            if num_workers and num_workers  1:
                nested_embeddings = await run_jobs(
                    embeddings_coroutines,
                    show_progress=show_progress,
                    workers=self.num_workers,
                    desc="Generating embeddings",
                )
            elif show_progress:
                try:
                    fromtqdm.asyncioimport tqdm_asyncio

                    nested_embeddings = await tqdm_asyncio.gather(
                        *embeddings_coroutines,
                        total=len(embeddings_coroutines),
                        desc="Generating embeddings",
                    )
                except ImportError:
                    nested_embeddings = await asyncio.gather(*embeddings_coroutines)
            else:
                nested_embeddings = await asyncio.gather(*embeddings_coroutines)
        else:
            nested_embeddings = []

        result_embeddings = [
            embedding for embeddings in nested_embeddings for embedding in embeddings
        ]

        for (event_id, text_batch), embeddings in zip(
            callback_payloads, nested_embeddings
        ):
            dispatcher.event(
                EmbeddingEndEvent(
                    chunks=text_batch,
                    embeddings=embeddings,
                )
            )
            self.callback_manager.on_event_end(
                CBEventType.EMBEDDING,
                payload={
                    EventPayload.CHUNKS: text_batch,
                    EventPayload.EMBEDDINGS: embeddings,
                },
                event_id=event_id,
            )

        return result_embeddings

    defsimilarity(
        self,
        embedding1: Embedding,
        embedding2: Embedding,
        mode: SimilarityMode = SimilarityMode.DEFAULT,
    ) -> float:
"""Get embedding similarity."""
        return similarity(embedding1=embedding1, embedding2=embedding2, mode=mode)

    def__call__(self, nodes: Sequence[BaseNode], **kwargs: Any) -> Sequence[BaseNode]:
        embeddings = self.get_text_embedding_batch(
            [node.get_content(metadata_mode=MetadataMode.EMBED) for node in nodes],
            **kwargs,
        )

        for node, embedding in zip(nodes, embeddings):
            node.embedding = embedding

        return nodes

    async defacall(
        self, nodes: Sequence[BaseNode], **kwargs: Any
    ) -> Sequence[BaseNode]:
        embeddings = await self.aget_text_embedding_batch(
            [node.get_content(metadata_mode=MetadataMode.EMBED) for node in nodes],
            **kwargs,
        )

        for node, embedding in zip(nodes, embeddings):
            node.embedding = embedding

        return nodes

```
 |  
| --- | --- |  
###  get_query_embedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.BaseEmbedding.get_query_embedding "Permanent link")

```
get_query_embedding(query: ) -> Embedding

```

Embed the input query.
When embedding a query, depending on the model, a special instruction can be prepended to the raw query string. For example, "Represent the question for retrieving supporting documents: ". If you're curious, other examples of predefined instructions can be found in embeddings/huggingface_utils.py.
Source code in `llama-index-core/llama_index/core/base/embeddings/base.py`  
| 
```
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
```
 | 
```
@dispatcher.span
defget_query_embedding(self, query: str) -> Embedding:
"""
    Embed the input query.

    When embedding a query, depending on the model, a special instruction
    can be prepended to the raw query string. For example, "Represent the
    question for retrieving supporting documents: ". If you're curious,
    other examples of predefined instructions can be found in
    embeddings/huggingface_utils.py.
    """
    model_dict = self.to_dict()
    model_dict.pop("api_key", None)
    dispatcher.event(
        EmbeddingStartEvent(
            model_dict=model_dict,
        )
    )
    with self.callback_manager.event(
        CBEventType.EMBEDDING, payload={EventPayload.SERIALIZED: self.to_dict()}
    ) as event:
        if not self.embeddings_cache:
            if self.rate_limiter is not None:
                self.rate_limiter.acquire()
            query_embedding = self._get_query_embedding(query)
        elif self.embeddings_cache is not None:
            cached_emb = self.embeddings_cache.get(
                key=query, collection="embeddings"
            )
            if cached_emb is not None:
                cached_key = next(iter(cached_emb.keys()))
                query_embedding = cached_emb[cached_key]
            else:
                if self.rate_limiter is not None:
                    self.rate_limiter.acquire()
                query_embedding = self._get_query_embedding(query)
                self.embeddings_cache.put(
                    key=query,
                    val={str(uuid.uuid4()): query_embedding},
                    collection="embeddings",
                )
        event.on_end(
            payload={
                EventPayload.CHUNKS: [query],
                EventPayload.EMBEDDINGS: [query_embedding],
            },
        )
    dispatcher.event(
        EmbeddingEndEvent(
            chunks=[query],
            embeddings=[query_embedding],
        )
    )
    return query_embedding

```
 |  
| --- | --- |  
###  aget_query_embedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.BaseEmbedding.aget_query_embedding "Permanent link")

```
aget_query_embedding(query: ) -> Embedding

```

Get query embedding.
Source code in `llama-index-core/llama_index/core/base/embeddings/base.py`  
| 
```
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
```
 | 
```
@dispatcher.span
async defaget_query_embedding(self, query: str) -> Embedding:
"""Get query embedding."""
    model_dict = self.to_dict()
    model_dict.pop("api_key", None)
    dispatcher.event(
        EmbeddingStartEvent(
            model_dict=model_dict,
        )
    )
    with self.callback_manager.event(
        CBEventType.EMBEDDING, payload={EventPayload.SERIALIZED: self.to_dict()}
    ) as event:
        if not self.embeddings_cache:
            if self.rate_limiter is not None:
                await self.rate_limiter.async_acquire()
            query_embedding = await self._aget_query_embedding(query)
        elif self.embeddings_cache is not None:
            cached_emb = await self.embeddings_cache.aget(
                key=query, collection="embeddings"
            )
            if cached_emb is not None:
                cached_key = next(iter(cached_emb.keys()))
                query_embedding = cached_emb[cached_key]
            else:
                if self.rate_limiter is not None:
                    await self.rate_limiter.async_acquire()
                query_embedding = await self._aget_query_embedding(query)
                await self.embeddings_cache.aput(
                    key=query,
                    val={str(uuid.uuid4()): query_embedding},
                    collection="embeddings",
                )

        event.on_end(
            payload={
                EventPayload.CHUNKS: [query],
                EventPayload.EMBEDDINGS: [query_embedding],
            },
        )
    dispatcher.event(
        EmbeddingEndEvent(
            chunks=[query],
            embeddings=[query_embedding],
        )
    )
    return query_embedding

```
 |  
| --- | --- |  
###  get_agg_embedding_from_queries [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.BaseEmbedding.get_agg_embedding_from_queries "Permanent link")

```
get_agg_embedding_from_queries(
    queries: [],
    agg_fn: Optional[Callable[..., Embedding]] = None,
) -> Embedding

```

Get aggregated embedding from multiple queries.
Source code in `llama-index-core/llama_index/core/base/embeddings/base.py`  
| 
```
239
240
241
242
243
244
245
246
247
```
 | 
```
defget_agg_embedding_from_queries(
    self,
    queries: List[str],
    agg_fn: Optional[Callable[..., Embedding]] = None,
) -> Embedding:
"""Get aggregated embedding from multiple queries."""
    query_embeddings = [self.get_query_embedding(query) for query in queries]
    agg_fn = agg_fn or mean_agg
    return agg_fn(query_embeddings)

```
 |  
| --- | --- |  
###  aget_agg_embedding_from_queries [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.BaseEmbedding.aget_agg_embedding_from_queries "Permanent link")

```
aget_agg_embedding_from_queries(
    queries: [],
    agg_fn: Optional[Callable[..., Embedding]] = None,
) -> Embedding

```

Async get aggregated embedding from multiple queries.
Source code in `llama-index-core/llama_index/core/base/embeddings/base.py`  
| 
```
249
250
251
252
253
254
255
256
257
```
 | 
```
async defaget_agg_embedding_from_queries(
    self,
    queries: List[str],
    agg_fn: Optional[Callable[..., Embedding]] = None,
) -> Embedding:
"""Async get aggregated embedding from multiple queries."""
    query_embeddings = [await self.aget_query_embedding(query) for query in queries]
    agg_fn = agg_fn or mean_agg
    return agg_fn(query_embeddings)

```
 |  
| --- | --- |  
###  get_text_embedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.BaseEmbedding.get_text_embedding "Permanent link")

```
get_text_embedding(text: ) -> Embedding

```

Embed the input text.
When embedding text, depending on the model, a special instruction can be prepended to the raw text string. For example, "Represent the document for retrieval: ". If you're curious, other examples of predefined instructions can be found in embeddings/huggingface_utils.py.
Source code in `llama-index-core/llama_index/core/base/embeddings/base.py`  
| 
```
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
```
 | 
```
@dispatcher.span
defget_text_embedding(self, text: str) -> Embedding:
"""
    Embed the input text.

    When embedding text, depending on the model, a special instruction
    can be prepended to the raw text string. For example, "Represent the
    document for retrieval: ". If you're curious, other examples of
    predefined instructions can be found in embeddings/huggingface_utils.py.
    """
    model_dict = self.to_dict()
    model_dict.pop("api_key", None)
    dispatcher.event(
        EmbeddingStartEvent(
            model_dict=model_dict,
        )
    )
    with self.callback_manager.event(
        CBEventType.EMBEDDING, payload={EventPayload.SERIALIZED: self.to_dict()}
    ) as event:
        if not self.embeddings_cache:
            if self.rate_limiter is not None:
                self.rate_limiter.acquire()
            text_embedding = self._get_text_embedding(text)
        elif self.embeddings_cache is not None:
            cached_emb = self.embeddings_cache.get(
                key=text, collection="embeddings"
            )
            if cached_emb is not None:
                cached_key = next(iter(cached_emb.keys()))
                text_embedding = cached_emb[cached_key]
            else:
                if self.rate_limiter is not None:
                    self.rate_limiter.acquire()
                text_embedding = self._get_text_embedding(text)
                self.embeddings_cache.put(
                    key=text,
                    val={str(uuid.uuid4()): text_embedding},
                    collection="embeddings",
                )

        event.on_end(
            payload={
                EventPayload.CHUNKS: [text],
                EventPayload.EMBEDDINGS: [text_embedding],
            }
        )
    dispatcher.event(
        EmbeddingEndEvent(
            chunks=[text],
            embeddings=[text_embedding],
        )
    )
    return text_embedding

```
 |  
| --- | --- |  
###  aget_text_embedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.BaseEmbedding.aget_text_embedding "Permanent link")

```
aget_text_embedding(text: ) -> Embedding

```

Async get text embedding.
Source code in `llama-index-core/llama_index/core/base/embeddings/base.py`  
| 
```
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
```
 | 
```
@dispatcher.span
async defaget_text_embedding(self, text: str) -> Embedding:
"""Async get text embedding."""
    model_dict = self.to_dict()
    model_dict.pop("api_key", None)
    dispatcher.event(
        EmbeddingStartEvent(
            model_dict=model_dict,
        )
    )
    with self.callback_manager.event(
        CBEventType.EMBEDDING, payload={EventPayload.SERIALIZED: self.to_dict()}
    ) as event:
        if not self.embeddings_cache:
            if self.rate_limiter is not None:
                await self.rate_limiter.async_acquire()
            text_embedding = await self._aget_text_embedding(text)
        elif self.embeddings_cache is not None:
            cached_emb = await self.embeddings_cache.aget(
                key=text, collection="embeddings"
            )
            if cached_emb is not None:
                cached_key = next(iter(cached_emb.keys()))
                text_embedding = cached_emb[cached_key]
            else:
                if self.rate_limiter is not None:
                    await self.rate_limiter.async_acquire()
                text_embedding = await self._aget_text_embedding(text)
                await self.embeddings_cache.aput(
                    key=text,
                    val={str(uuid.uuid4()): text_embedding},
                    collection="embeddings",
                )

        event.on_end(
            payload={
                EventPayload.CHUNKS: [text],
                EventPayload.EMBEDDINGS: [text_embedding],
            }
        )
    dispatcher.event(
        EmbeddingEndEvent(
            chunks=[text],
            embeddings=[text_embedding],
        )
    )
    return text_embedding

```
 |  
| --- | --- |  
###  get_text_embedding_batch [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.BaseEmbedding.get_text_embedding_batch "Permanent link")

```
get_text_embedding_batch(
    texts: [],
    show_progress:  = False,
    **kwargs: 
) -> [Embedding]

```

Get a list of text embeddings, with batching.
Source code in `llama-index-core/llama_index/core/base/embeddings/base.py`  
| 
```
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
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
```
 | 
```
@dispatcher.span
defget_text_embedding_batch(
    self,
    texts: List[str],
    show_progress: bool = False,
    **kwargs: Any,
) -> List[Embedding]:
"""Get a list of text embeddings, with batching."""
    cur_batch: List[str] = []
    result_embeddings: List[Embedding] = []

    queue_with_progress = enumerate(
        get_tqdm_iterable(texts, show_progress, "Generating embeddings")
    )

    model_dict = self.to_dict()
    model_dict.pop("api_key", None)
    for idx, text in queue_with_progress:
        cur_batch.append(text)
        if idx == len(texts) - 1 or len(cur_batch) == self.embed_batch_size:
            # flush
            dispatcher.event(
                EmbeddingStartEvent(
                    model_dict=model_dict,
                )
            )
            with self.callback_manager.event(
                CBEventType.EMBEDDING,
                payload={EventPayload.SERIALIZED: self.to_dict()},
            ) as event:
                if self.rate_limiter is not None:
                    self.rate_limiter.acquire()
                if not self.embeddings_cache:
                    embeddings = self._get_text_embeddings(cur_batch)
                elif self.embeddings_cache is not None:
                    embeddings = self._get_text_embeddings_cached(cur_batch)
                result_embeddings.extend(embeddings)
                event.on_end(
                    payload={
                        EventPayload.CHUNKS: cur_batch,
                        EventPayload.EMBEDDINGS: embeddings,
                    },
                )
            dispatcher.event(
                EmbeddingEndEvent(
                    chunks=cur_batch,
                    embeddings=embeddings,
                )
            )
            cur_batch = []

    return result_embeddings

```
 |  
| --- | --- |  
###  aget_text_embedding_batch [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.BaseEmbedding.aget_text_embedding_batch "Permanent link")

```
aget_text_embedding_batch(
    texts: [],
    show_progress:  = False,
    **kwargs: 
) -> [Embedding]

```

Asynchronously get a list of text embeddings, with batching.
Source code in `llama-index-core/llama_index/core/base/embeddings/base.py`  
| 
```
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
```
 | 
```
@dispatcher.span
async defaget_text_embedding_batch(
    self,
    texts: List[str],
    show_progress: bool = False,
    **kwargs: Any,
) -> List[Embedding]:
"""Asynchronously get a list of text embeddings, with batching."""
    num_workers = self.num_workers

    model_dict = self.to_dict()
    model_dict.pop("api_key", None)

    cur_batch: List[str] = []
    embeddings_coroutines: List[Coroutine] = []
    callback_payloads: List[Tuple[str, List[str]]] = []

    # for idx, text in queue_with_progress:
    for idx, text in enumerate(texts):
        cur_batch.append(text)
        if idx == len(texts) - 1 or len(cur_batch) == self.embed_batch_size:
            # flush
            dispatcher.event(
                EmbeddingStartEvent(
                    model_dict=model_dict,
                )
            )
            event_id = self.callback_manager.on_event_start(
                CBEventType.EMBEDDING,
                payload={EventPayload.SERIALIZED: self.to_dict()},
            )
            callback_payloads.append((event_id, cur_batch))

            if not self.embeddings_cache:
                embeddings_coroutines.append(
                    self._aget_text_embeddings_rate_limited(cur_batch)
                )
            elif self.embeddings_cache is not None:
                embeddings_coroutines.append(
                    self._aget_text_embeddings_cached(cur_batch)
                )

            cur_batch = []

    # flatten the results of asyncio.gather, which is a list of embeddings lists
    if len(embeddings_coroutines)  0:
        if num_workers and num_workers  1:
            nested_embeddings = await run_jobs(
                embeddings_coroutines,
                show_progress=show_progress,
                workers=self.num_workers,
                desc="Generating embeddings",
            )
        elif show_progress:
            try:
                fromtqdm.asyncioimport tqdm_asyncio

                nested_embeddings = await tqdm_asyncio.gather(
                    *embeddings_coroutines,
                    total=len(embeddings_coroutines),
                    desc="Generating embeddings",
                )
            except ImportError:
                nested_embeddings = await asyncio.gather(*embeddings_coroutines)
        else:
            nested_embeddings = await asyncio.gather(*embeddings_coroutines)
    else:
        nested_embeddings = []

    result_embeddings = [
        embedding for embeddings in nested_embeddings for embedding in embeddings
    ]

    for (event_id, text_batch), embeddings in zip(
        callback_payloads, nested_embeddings
    ):
        dispatcher.event(
            EmbeddingEndEvent(
                chunks=text_batch,
                embeddings=embeddings,
            )
        )
        self.callback_manager.on_event_end(
            CBEventType.EMBEDDING,
            payload={
                EventPayload.CHUNKS: text_batch,
                EventPayload.EMBEDDINGS: embeddings,
            },
            event_id=event_id,
        )

    return result_embeddings

```
 |  
| --- | --- |  
###  similarity [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.BaseEmbedding.similarity "Permanent link")

```
similarity(
    embedding1: Embedding,
    embedding2: Embedding,
    mode: SimilarityMode = DEFAULT,
) -> float

```

Get embedding similarity.
Source code in `llama-index-core/llama_index/core/base/embeddings/base.py`  
| 
```
621
622
623
624
625
626
627
628
```
 | 
```
defsimilarity(
    self,
    embedding1: Embedding,
    embedding2: Embedding,
    mode: SimilarityMode = SimilarityMode.DEFAULT,
) -> float:
"""Get embedding similarity."""
    return similarity(embedding1=embedding1, embedding2=embedding2, mode=mode)

```
 |  
| --- | --- |  
##  MockEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.MockEmbedding "Permanent link")
Bases: 
Mock embedding.
Used for token prediction.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `embed_dim`  |  embedding dimension  |  _required_  |  
Source code in `llama-index-core/llama_index/core/embeddings/mock_embed_model.py`  
| 
```
10
11
12
13
14
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
```
 | 
```
classMockEmbedding(BaseEmbedding):
"""
    Mock embedding.

    Used for token prediction.

    Args:
        embed_dim (int): embedding dimension

    """

    embed_dim: int

    def__init__(self, embed_dim: int, **kwargs: Any) -> None:
"""Init params."""
        super().__init__(embed_dim=embed_dim, **kwargs)

    @classmethod
    defclass_name(cls) -> str:
        return "MockEmbedding"

    def_get_vector(self) -> List[float]:
        return [0.5] * self.embed_dim

    async def_aget_text_embedding(self, text: str) -> List[float]:
        return self._get_vector()

    async def_aget_query_embedding(self, query: str) -> List[float]:
        return self._get_vector()

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        return self._get_vector()

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        return self._get_vector()

```
 |  
| --- | --- |  
##  MockMultiModalEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.MockMultiModalEmbedding "Permanent link")
Bases: 
Multi-Modal Mock embedding.
Used to simulate a multi-modal embedding. The reason this is used beside MockEmbedding to satisfy MultiModalVectorStoreIndex image embedding checks.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `embed_dim`  |  embedding dimension  |  _required_  |  
Source code in `llama-index-core/llama_index/core/embeddings/mock_embed_model.py`  
| 
```
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
```
 | 
```
classMockMultiModalEmbedding(MultiModalEmbedding):
"""
    Multi-Modal Mock embedding.

    Used to simulate a multi-modal embedding.
    The reason this is used beside MockEmbedding to satisfy MultiModalVectorStoreIndex image embedding checks.

    Args:
        embed_dim (int): embedding dimension

    """

    embed_dim: int

    def__init__(self, embed_dim: int, **kwargs: Any) -> None:
"""Init params."""
        super().__init__(embed_dim=embed_dim, **kwargs)

    def_get_vector(self) -> List[float]:
        return [0.5] * self.embed_dim

    def_get_text_embedding(self, text: str) -> List[float]:
        return self._get_vector()

    def_get_image_embedding(self, img_file_path: ImageType) -> List[float]:
        return self._get_vector()

    async def_aget_image_embedding(self, img_file_path: ImageType) -> List[float]:
        return self._get_image_embedding(img_file_path)

    def_get_query_embedding(self, query: str) -> List[float]:
        return self._get_text_embedding(query)

    async def_aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)

```
 |  
| --- | --- |  
##  MultiModalEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.MultiModalEmbedding "Permanent link")
Bases: 
Base class for Multi Modal embeddings.
Source code in `llama-index-core/llama_index/core/embeddings/multi_modal_base.py`  
| 
```
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
```
 | 
```
classMultiModalEmbedding(BaseEmbedding):
"""Base class for Multi Modal embeddings."""

    @abstractmethod
    def_get_image_embedding(self, img_file_path: ImageType) -> Embedding:
"""
        Embed the input image synchronously.

        Subclasses should implement this method. Reference get_image_embedding's
        docstring for more information.
        """

    @abstractmethod
    async def_aget_image_embedding(self, img_file_path: ImageType) -> Embedding:
"""
        Embed the input image asynchronously.

        Subclasses should implement this method. Reference get_image_embedding's
        docstring for more information.
        """

    defget_image_embedding(self, img_file_path: ImageType) -> Embedding:
"""
        Embed the input image.
        """
        with self.callback_manager.event(
            CBEventType.EMBEDDING, payload={EventPayload.SERIALIZED: self.to_dict()}
        ) as event:
            image_embedding = self._get_image_embedding(img_file_path)

            event.on_end(
                payload={
                    EventPayload.CHUNKS: [img_file_path],
                    EventPayload.EMBEDDINGS: [image_embedding],
                },
            )
        return image_embedding

    async defaget_image_embedding(self, img_file_path: ImageType) -> Embedding:
"""Get image embedding."""
        with self.callback_manager.event(
            CBEventType.EMBEDDING, payload={EventPayload.SERIALIZED: self.to_dict()}
        ) as event:
            image_embedding = await self._aget_image_embedding(img_file_path)

            event.on_end(
                payload={
                    EventPayload.CHUNKS: [img_file_path],
                    EventPayload.EMBEDDINGS: [image_embedding],
                },
            )
        return image_embedding

    def_get_image_embeddings(self, img_file_paths: List[ImageType]) -> List[Embedding]:
"""
        Embed the input sequence of image synchronously.

        Subclasses can implement this method if batch queries are supported.
        """
        # Default implementation just loops over _get_image_embedding
        return [
            self._get_image_embedding(img_file_path) for img_file_path in img_file_paths
        ]

    async def_aget_image_embeddings(
        self, img_file_paths: List[ImageType]
    ) -> List[Embedding]:
"""
        Embed the input sequence of image asynchronously.

        Subclasses can implement this method if batch queries are supported.
        """
        return await asyncio.gather(
            *[
                self._aget_image_embedding(img_file_path)
                for img_file_path in img_file_paths
            ]
        )

    defget_image_embedding_batch(
        self, img_file_paths: List[ImageType], show_progress: bool = False
    ) -> List[Embedding]:
"""Get a list of image embeddings, with batching."""
        cur_batch: List[ImageType] = []
        result_embeddings: List[Embedding] = []

        queue_with_progress = enumerate(
            get_tqdm_iterable(
                img_file_paths, show_progress, "Generating image embeddings"
            )
        )

        for idx, img_file_path in queue_with_progress:
            cur_batch.append(img_file_path)
            if (
                idx == len(img_file_paths) - 1
                or len(cur_batch) == self.embed_batch_size
            ):
                # flush
                with self.callback_manager.event(
                    CBEventType.EMBEDDING,
                    payload={EventPayload.SERIALIZED: self.to_dict()},
                ) as event:
                    embeddings = self._get_image_embeddings(cur_batch)
                    result_embeddings.extend(embeddings)
                    event.on_end(
                        payload={
                            EventPayload.CHUNKS: cur_batch,
                            EventPayload.EMBEDDINGS: embeddings,
                        },
                    )
                cur_batch = []

        return result_embeddings

    async defaget_image_embedding_batch(
        self, img_file_paths: List[ImageType], show_progress: bool = False
    ) -> List[Embedding]:
"""Asynchronously get a list of image embeddings, with batching."""
        cur_batch: List[ImageType] = []
        callback_payloads: List[Tuple[str, List[ImageType]]] = []
        result_embeddings: List[Embedding] = []
        embeddings_coroutines: List[Coroutine] = []
        for idx, img_file_path in enumerate(img_file_paths):
            cur_batch.append(img_file_path)
            if (
                idx == len(img_file_paths) - 1
                or len(cur_batch) == self.embed_batch_size
            ):
                # flush
                event_id = self.callback_manager.on_event_start(
                    CBEventType.EMBEDDING,
                    payload={EventPayload.SERIALIZED: self.to_dict()},
                )
                callback_payloads.append((event_id, cur_batch))
                embeddings_coroutines.append(self._aget_image_embeddings(cur_batch))
                cur_batch = []

        # flatten the results of asyncio.gather, which is a list of embeddings lists
        nested_embeddings = []
        if show_progress:
            try:
                fromtqdm.asyncioimport tqdm_asyncio

                nested_embeddings = await tqdm_asyncio.gather(
                    *embeddings_coroutines,
                    total=len(embeddings_coroutines),
                    desc="Generating embeddings",
                )
            except ImportError:
                nested_embeddings = await asyncio.gather(*embeddings_coroutines)
        else:
            nested_embeddings = await asyncio.gather(*embeddings_coroutines)

        result_embeddings = [
            embedding for embeddings in nested_embeddings for embedding in embeddings
        ]

        for (event_id, image_batch), embeddings in zip(
            callback_payloads, nested_embeddings
        ):
            self.callback_manager.on_event_end(
                CBEventType.EMBEDDING,
                payload={
                    EventPayload.CHUNKS: image_batch,
                    EventPayload.EMBEDDINGS: embeddings,
                },
                event_id=event_id,
            )

        return result_embeddings

```
 |  
| --- | --- |  
###  get_image_embedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.MultiModalEmbedding.get_image_embedding "Permanent link")

```
get_image_embedding(img_file_path: ImageType) -> Embedding

```

Embed the input image.
Source code in `llama-index-core/llama_index/core/embeddings/multi_modal_base.py`  
| 
```
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
```
 | 
```
defget_image_embedding(self, img_file_path: ImageType) -> Embedding:
"""
    Embed the input image.
    """
    with self.callback_manager.event(
        CBEventType.EMBEDDING, payload={EventPayload.SERIALIZED: self.to_dict()}
    ) as event:
        image_embedding = self._get_image_embedding(img_file_path)

        event.on_end(
            payload={
                EventPayload.CHUNKS: [img_file_path],
                EventPayload.EMBEDDINGS: [image_embedding],
            },
        )
    return image_embedding

```
 |  
| --- | --- |  
###  aget_image_embedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.MultiModalEmbedding.aget_image_embedding "Permanent link")

```
aget_image_embedding(img_file_path: ImageType) -> Embedding

```

Get image embedding.
Source code in `llama-index-core/llama_index/core/embeddings/multi_modal_base.py`  
| 
```
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
```
 | 
```
async defaget_image_embedding(self, img_file_path: ImageType) -> Embedding:
"""Get image embedding."""
    with self.callback_manager.event(
        CBEventType.EMBEDDING, payload={EventPayload.SERIALIZED: self.to_dict()}
    ) as event:
        image_embedding = await self._aget_image_embedding(img_file_path)

        event.on_end(
            payload={
                EventPayload.CHUNKS: [img_file_path],
                EventPayload.EMBEDDINGS: [image_embedding],
            },
        )
    return image_embedding

```
 |  
| --- | --- |  
###  get_image_embedding_batch [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.MultiModalEmbedding.get_image_embedding_batch "Permanent link")

```
get_image_embedding_batch(
    img_file_paths: [ImageType],
    show_progress:  = False,
) -> [Embedding]

```

Get a list of image embeddings, with batching.
Source code in `llama-index-core/llama_index/core/embeddings/multi_modal_base.py`  
| 
```
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
```
 | 
```
defget_image_embedding_batch(
    self, img_file_paths: List[ImageType], show_progress: bool = False
) -> List[Embedding]:
"""Get a list of image embeddings, with batching."""
    cur_batch: List[ImageType] = []
    result_embeddings: List[Embedding] = []

    queue_with_progress = enumerate(
        get_tqdm_iterable(
            img_file_paths, show_progress, "Generating image embeddings"
        )
    )

    for idx, img_file_path in queue_with_progress:
        cur_batch.append(img_file_path)
        if (
            idx == len(img_file_paths) - 1
            or len(cur_batch) == self.embed_batch_size
        ):
            # flush
            with self.callback_manager.event(
                CBEventType.EMBEDDING,
                payload={EventPayload.SERIALIZED: self.to_dict()},
            ) as event:
                embeddings = self._get_image_embeddings(cur_batch)
                result_embeddings.extend(embeddings)
                event.on_end(
                    payload={
                        EventPayload.CHUNKS: cur_batch,
                        EventPayload.EMBEDDINGS: embeddings,
                    },
                )
            cur_batch = []

    return result_embeddings

```
 |  
| --- | --- |  
###  aget_image_embedding_batch [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.MultiModalEmbedding.aget_image_embedding_batch "Permanent link")

```
aget_image_embedding_batch(
    img_file_paths: [ImageType],
    show_progress:  = False,
) -> [Embedding]

```

Asynchronously get a list of image embeddings, with batching.
Source code in `llama-index-core/llama_index/core/embeddings/multi_modal_base.py`  
| 
```
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
```
 | 
```
async defaget_image_embedding_batch(
    self, img_file_paths: List[ImageType], show_progress: bool = False
) -> List[Embedding]:
"""Asynchronously get a list of image embeddings, with batching."""
    cur_batch: List[ImageType] = []
    callback_payloads: List[Tuple[str, List[ImageType]]] = []
    result_embeddings: List[Embedding] = []
    embeddings_coroutines: List[Coroutine] = []
    for idx, img_file_path in enumerate(img_file_paths):
        cur_batch.append(img_file_path)
        if (
            idx == len(img_file_paths) - 1
            or len(cur_batch) == self.embed_batch_size
        ):
            # flush
            event_id = self.callback_manager.on_event_start(
                CBEventType.EMBEDDING,
                payload={EventPayload.SERIALIZED: self.to_dict()},
            )
            callback_payloads.append((event_id, cur_batch))
            embeddings_coroutines.append(self._aget_image_embeddings(cur_batch))
            cur_batch = []

    # flatten the results of asyncio.gather, which is a list of embeddings lists
    nested_embeddings = []
    if show_progress:
        try:
            fromtqdm.asyncioimport tqdm_asyncio

            nested_embeddings = await tqdm_asyncio.gather(
                *embeddings_coroutines,
                total=len(embeddings_coroutines),
                desc="Generating embeddings",
            )
        except ImportError:
            nested_embeddings = await asyncio.gather(*embeddings_coroutines)
    else:
        nested_embeddings = await asyncio.gather(*embeddings_coroutines)

    result_embeddings = [
        embedding for embeddings in nested_embeddings for embedding in embeddings
    ]

    for (event_id, image_batch), embeddings in zip(
        callback_payloads, nested_embeddings
    ):
        self.callback_manager.on_event_end(
            CBEventType.EMBEDDING,
            payload={
                EventPayload.CHUNKS: image_batch,
                EventPayload.EMBEDDINGS: embeddings,
            },
            event_id=event_id,
        )

    return result_embeddings

```
 |  
| --- | --- |  
##  Pooling [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.Pooling "Permanent link")
Bases: `str`, `Enum`
Enum of possible pooling choices with pooling behaviors.
Source code in `llama-index-core/llama_index/core/embeddings/pooling.py`  
| 
```
10
11
12
13
14
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
```
 | 
```
classPooling(str, Enum):
"""Enum of possible pooling choices with pooling behaviors."""

    CLS = "cls"
    MEAN = "mean"

    def__call__(self, array: np.ndarray) -> np.ndarray:
        if self == self.CLS:
            return Pooling.cls_pooling(array)
        return Pooling.mean_pooling(array)

    @classmethod
    @overload
    defcls_pooling(cls, array: np.ndarray) -> np.ndarray: ...

    @classmethod
    @overload
    # TODO: Remove this `type: ignore` after the false positive problem
    #  is addressed in mypy: https://github.com/python/mypy/issues/15683 .
    defcls_pooling(cls, array: "torch.Tensor") -> "torch.Tensor":  # type: ignore
        ...

    @classmethod
    defcls_pooling(
        cls, array: "Union[np.ndarray, torch.Tensor]"
    ) -> "Union[np.ndarray, torch.Tensor]":
        if len(array.shape) == 3:
            return array[:, 0]
        if len(array.shape) == 2:
            return array[0]
        raise NotImplementedError(f"Unhandled shape {array.shape}.")

    @classmethod
    defmean_pooling(cls, array: np.ndarray) -> np.ndarray:
        if len(array.shape) == 3:
            return array.mean(axis=1)
        if len(array.shape) == 2:
            return array.mean(axis=0)
        raise NotImplementedError(f"Unhandled shape {array.shape}.")

```
 |  
| --- | --- |  
##  resolve_embed_model [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/#llama_index.core.embeddings.resolve_embed_model "Permanent link")

```
resolve_embed_model(
    embed_model: Optional[EmbedType] = None,
    callback_manager: Optional[] = None,
) -> 

```

Resolve embed model.
Source code in `llama-index-core/llama_index/core/embeddings/utils.py`  
| 
```
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
```
 | 
```
defresolve_embed_model(
    embed_model: Optional[EmbedType] = None,
    callback_manager: Optional[CallbackManager] = None,
) -> BaseEmbedding:
"""Resolve embed model."""
    fromllama_index.core.settingsimport Settings

    try:
        fromllama_index.core.bridge.langchainimport Embeddings as LCEmbeddings
    except ImportError:
        LCEmbeddings = None  # type: ignore

    if embed_model == "default":
        if os.getenv("IS_TESTING"):
            embed_model = MockEmbedding(embed_dim=8)
            embed_model.callback_manager = callback_manager or Settings.callback_manager
            return embed_model

        try:
            fromllama_index.embeddings.openaiimport (
                OpenAIEmbedding,
            )  # pants: no-infer-dep

            fromllama_index.embeddings.openai.utilsimport (
                validate_openai_api_key,
            )  # pants: no-infer-dep

            embed_model = OpenAIEmbedding()
            validate_openai_api_key(embed_model.api_key)  # type: ignore
        except ImportError:
            raise ImportError(
                "`llama-index-embeddings-openai` package not found, "
                "please run `pip install llama-index-embeddings-openai`"
            )
        except ValueError as e:
            raise ValueError(
                "\n******\n"
                "Could not load OpenAI embedding model. "
                "If you intended to use OpenAI, please check your OPENAI_API_KEY.\n"
                "Original error:\n"
                f"{e!s}"
                "\nConsider using embed_model='local'.\n"
                "Visit our documentation for more embedding options: "
                "https://developers.llamaindex.ai/python/framework/module_guides/"
                "models/embeddings/"
                "\n******"
            )
    # for image multi-modal embeddings
    elif isinstance(embed_model, str) and embed_model.startswith("clip"):
        try:
            fromllama_index.embeddings.clipimport ClipEmbedding  # pants: no-infer-dep

            clip_model_name = (
                embed_model.split(":")[1] if ":" in embed_model else "ViT-B/32"
            )
            embed_model = ClipEmbedding(model_name=clip_model_name)
        except ImportError as e:
            raise ImportError(
                "`llama-index-embeddings-clip` package not found, "
                "please run `pip install llama-index-embeddings-clip` and `pip install git+https://github.com/openai/CLIP.git`"
            )

    if isinstance(embed_model, str):
        try:
            fromllama_index.embeddings.huggingfaceimport (
                HuggingFaceEmbedding,
            )  # pants: no-infer-dep

            splits = embed_model.split(":", 1)
            is_local = splits[0]
            model_name = splits[1] if len(splits)  1 else None
            if is_local != "local":
                raise ValueError(
                    "embed_model must start with str 'local' or of type BaseEmbedding"
                )

            cache_folder = os.path.join(get_cache_dir(), "models")
            os.makedirs(cache_folder, exist_ok=True)

            embed_model = HuggingFaceEmbedding(
                model_name=model_name, cache_folder=cache_folder
            )
        except ImportError:
            raise ImportError(
                "`llama-index-embeddings-huggingface` package not found, "
                "please run `pip install llama-index-embeddings-huggingface`"
            )

    if LCEmbeddings is not None and isinstance(embed_model, LCEmbeddings):
        try:
            fromllama_index.embeddings.langchainimport (
                LangchainEmbedding,
            )  # pants: no-infer-dep

            embed_model = LangchainEmbedding(embed_model)
        except ImportError as e:
            raise ImportError(
                "`llama-index-embeddings-langchain` package not found, "
                "please run `pip install llama-index-embeddings-langchain`"
            )

    if embed_model is None:
        print("Embeddings have been explicitly disabled. Using MockEmbedding.")
        embed_model = MockEmbedding(embed_dim=1)

    assert isinstance(embed_model, BaseEmbedding)

    embed_model.callback_manager = callback_manager or Settings.callback_manager

    return embed_model

```
 |  
| --- | --- |  
options: members: - BaseEmbedding - resolve_embed_model
