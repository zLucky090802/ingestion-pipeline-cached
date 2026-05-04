# Reka
##  RekaLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/reka/#llama_index.llms.reka.RekaLLM "Permanent link")
Bases: `CustomLLM`
Reka LLM integration for LlamaIndex.
Source code in `llama-index-integrations/llms/llama-index-llms-reka/llama_index/llms/reka/base.py`  
| 
```
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
```
 | 
```
classRekaLLM(CustomLLM):
"""Reka LLM integration for LlamaIndex."""

    model: str = Field(default=DEFAULT_REKA_MODEL, description="The Reka model to use.")
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        description="The temperature to use for sampling.",
        gte=0.0,
        lte=1.0,
    )
    max_tokens: int = Field(
        default=DEFAULT_REKA_MAX_TOKENS,
        description="The maximum number of tokens to generate.",
        gt=0,
    )
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional keyword arguments for Reka API calls.",
    )

    _client: Reka = PrivateAttr()
    _aclient: AsyncReka = PrivateAttr()

    def__init__(
        self,
        model: str = DEFAULT_REKA_MODEL,
        api_key: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_REKA_MAX_TOKENS,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
"""
        Initialize the RekaLLM instance.

        Args:
            model (str): The Reka model to use, choose from ['reka-flash', 'reka-core', 'reka-edge'].
            api_key (Optional[str]): The API key for Reka.
            temperature (float): The temperature to use for sampling.
            max_tokens (int): The maximum number of tokens to generate.
            additional_kwargs (Optional[Dict[str, Any]]): Additional keyword arguments for Reka API calls.
            callback_manager (Optional[CallbackManager]): A callback manager for handling callbacks.

        Raises:
            ValueError: If the Reka API key is not provided and not set in the environment.

        Example:
            >>> reka_llm = RekaLLM(
            ...     model="reka-flash",
            ...     api_key="your-api-key-here",
            ...     temperature=0.7,
            ...     max_tokens=100
            ... )

        """
        additional_kwargs = additional_kwargs or {}
        callback_manager = callback_manager or CallbackManager([])

        api_key = api_key or os.getenv("REKA_API_KEY")
        if not api_key:
            raise ValueError(
                "Reka API key is required. Please provide it as an argument or set the REKA_API_KEY environment variable."
            )

        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            additional_kwargs=additional_kwargs,
            callback_manager=callback_manager,
        )
        self._client = Reka(api_key=api_key)
        self._aclient = AsyncReka(api_key=api_key)

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=DEFAULT_REKA_CONTEXT_WINDOW,
            num_output=self.max_tokens,
            model_name=self.model,
            is_chat_model=True,
        )

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        return {**base_kwargs, **self.additional_kwargs}

    def_get_all_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        return {**self._model_kwargs, **kwargs}

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
"""
        Send a chat request to the Reka API.

        Args:
            messages (Sequence[ChatMessage]): A sequence of chat messages.
            **kwargs: Additional keyword arguments for the API call.

        Returns:
            ChatResponse: The response from the Reka API.

        Raises:
            ValueError: If there's an error with the Reka API call.

        Example:
            >>> reka_llm = RekaLLM(api_key="your-api-key-here")
            >>> messages = [
            ...     ChatMessage(role=MessageRole.SYSTEM, content="You are a helpful assistant."),
            ...     ChatMessage(role=MessageRole.USER, content="What's the capital of France?")
            ... ]
            >>> response = reka_llm.chat(messages)
            >>> print(response.message.content)

        """
        all_kwargs = self._get_all_kwargs(**kwargs)
        reka_messages = process_messages_for_reka(messages)

        try:
            response = self._client.chat.create(messages=reka_messages, **all_kwargs)
            return ChatResponse(
                message=ChatMessage(
                    role=MessageRole.ASSISTANT,
                    content=response.responses[0].message.content,
                ),
                raw=response.__dict__,
            )
        except ApiError as e:
            raise ValueError(f"Reka API error: {e.status_code}{e.body}")

    @llm_completion_callback()
    defcomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
"""
        Send a completion request to the Reka API.

        Args:
            prompt (str): The prompt for completion.
            **kwargs: Additional keyword arguments for the API call.

        Returns:
            CompletionResponse: The response from the Reka API.

        Raises:
            ValueError: If there's an error with the Reka API call.

        Example:
            >>> reka_llm = RekaLLM(api_key="your-api-key-here")
            >>> response = reka_llm.complete("The capital of France is")
            >>> print(response.text)

        """
        all_kwargs = self._get_all_kwargs(**kwargs)
        try:
            response = self._client.chat.create(
                messages=[{"role": "user", "content": prompt}], **all_kwargs
            )
            return CompletionResponse(
                text=response.responses[0].message.content,
                raw=response.__dict__,
            )
        except ApiError as e:
            raise ValueError(f"Reka API error: {e.status_code}{e.body}")

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
"""
        Send a streaming chat request to the Reka API.

        Args:
            messages (Sequence[ChatMessage]): A sequence of chat messages.
            **kwargs: Additional keyword arguments for the API call.

        Returns:
            ChatResponseGen: A generator yielding chat responses.

        Raises:
            ValueError: If there's an error with the Reka API call.

        Example:
            >>> reka_llm = RekaLLM(api_key="your-api-key-here")
            >>> messages = [
            ...     ChatMessage(role=MessageRole.SYSTEM, content="You are a helpful assistant."),
            ...     ChatMessage(role=MessageRole.USER, content="Tell me a short story.")
            ... ]
            >>> for chunk in reka_llm.stream_chat(messages):
            ...     print(chunk.delta, end="", flush=True)

        """
        all_kwargs = self._get_all_kwargs(**kwargs)
        reka_messages = process_messages_for_reka(messages)

        try:
            stream = self._client.chat.create_stream(
                messages=reka_messages, **all_kwargs
            )
        except ApiError as e:
            raise ValueError(f"Reka API error: {e.status_code}{e.body}")

        defgen() -> ChatResponseGen:
            prev_content = ""
            for chunk in stream:
                content = chunk.responses[0].chunk.content
                content_delta = content[len(prev_content) :]
                prev_content = content
                yield ChatResponse(
                    message=ChatMessage(
                        role=MessageRole.ASSISTANT,
                        content=content,
                    ),
                    delta=content_delta,
                    raw=chunk.__dict__,
                )

        return gen()

    @llm_completion_callback()
    defstream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
"""
        Send a streaming completion request to the Reka API.

        Args:
            prompt (str): The prompt for completion.
            **kwargs: Additional keyword arguments for the API call.

        Returns:
            CompletionResponseGen: A generator yielding completion responses.

        Raises:
            ValueError: If there's an error with the Reka API call.

        Example:
            >>> reka_llm = RekaLLM(api_key="your-api-key-here")
            >>> prompt = "Write a haiku about programming:"
            >>> for chunk in reka_llm.stream_complete(prompt):
            ...     print(chunk.delta, end="", flush=True)

        """
        all_kwargs = self._get_all_kwargs(**kwargs)
        try:
            stream = self._client.chat.create_stream(
                messages=[{"role": "user", "content": prompt}], **all_kwargs
            )
        except ApiError as e:
            raise ValueError(f"Reka API error: {e.status_code}{e.body}")

        defgen() -> CompletionResponseGen:
            prev_text = ""
            for chunk in stream:
                text = chunk.responses[0].chunk.content
                text_delta = text[len(prev_text) :]
                prev_text = text
                yield CompletionResponse(
                    text=text,
                    delta=text_delta,
                    raw=chunk.__dict__,
                )

        return gen()

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
"""
        Send an asynchronous chat request to the Reka API.

        Args:
            messages (Sequence[ChatMessage]): A sequence of chat messages.
            **kwargs: Additional keyword arguments for the API call.

        Returns:
            ChatResponse: The response from the Reka API.

        Raises:
            ValueError: If there's an error with the Reka API call.

        Example:
            >>> import asyncio
            >>> from llama_index.llms.reka import RekaLLM
            >>> from llama_index.core.base.llms.types import ChatMessage, MessageRole

            >>> async def main():
            ...     reka_llm = RekaLLM(api_key="your-api-key-here")
            ...     messages = [
            ...         ChatMessage(role=MessageRole.SYSTEM, content="You are a helpful assistant."),
            ...         ChatMessage(role=MessageRole.USER, content="What's the meaning of life?")
            ...     ]
            ...     response = await reka_llm.achat(messages)
            ...     print(response.message.content)

            >>> asyncio.run(main())

        """
        all_kwargs = self._get_all_kwargs(**kwargs)
        reka_messages = process_messages_for_reka(messages)

        try:
            response = await self._aclient.chat.create(
                messages=reka_messages, **all_kwargs
            )
            return ChatResponse(
                message=ChatMessage(
                    role=MessageRole.ASSISTANT,
                    content=response.responses[0].message.content,
                ),
                raw=response.__dict__,
            )
        except ApiError as e:
            raise ValueError(f"Reka API error: {e.status_code}{e.body}")

    @llm_completion_callback()
    async defacomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
"""
        Send an asynchronous completion request to the Reka API.

        Args:
            prompt (str): The prompt for completion.
            **kwargs: Additional keyword arguments for the API call.

        Returns:
            CompletionResponse: The response from the Reka API.

        Raises:
            ValueError: If there's an error with the Reka API call.

        Example:
            >>> import asyncio
            >>> from llama_index.llms.reka import RekaLLM

            >>> async def main():
            ...     reka_llm = RekaLLM(api_key="your-api-key-here")
            ...     prompt = "The capital of France is"
            ...     response = await reka_llm.acomplete(prompt)
            ...     print(response.text)

            >>> asyncio.run(main())

        """
        all_kwargs = self._get_all_kwargs(**kwargs)
        try:
            response = await self._aclient.chat.create(
                messages=[{"role": "user", "content": prompt}], **all_kwargs
            )
            return CompletionResponse(
                text=response.responses[0].message.content,
                raw=response.__dict__,
            )
        except ApiError as e:
            raise ValueError(f"Reka API error: {e.status_code}{e.body}")

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
"""
        Send an asynchronous streaming chat request to the Reka API.

        Args:
            messages (Sequence[ChatMessage]): A sequence of chat messages.
            **kwargs: Additional keyword arguments for the API call.

        Returns:
            ChatResponseAsyncGen: An asynchronous generator yielding chat responses.

        Raises:
            ValueError: If there's an error with the Reka API call.

        Example:
            >>> import asyncio
            >>> from llama_index.llms.reka import RekaLLM
            >>> from llama_index.core.base.llms.types import ChatMessage, MessageRole

            >>> async def main():
            ...     reka_llm = RekaLLM(api_key="your-api-key-here")
            ...     messages = [
            ...         ChatMessage(role=MessageRole.SYSTEM, content="You are a helpful assistant."),
            ...         ChatMessage(role=MessageRole.USER, content="Tell me a short story about a robot.")
            ...     ]
            ...     async for chunk in await reka_llm.astream_chat(messages):
            ...         print(chunk.delta, end="", flush=True)
            ...     print()  # New line after the story is complete

            >>> asyncio.run(main())

        """
        all_kwargs = self._get_all_kwargs(**kwargs)
        reka_messages = process_messages_for_reka(messages)

        try:
            stream = self._aclient.chat.create_stream(
                messages=reka_messages, **all_kwargs
            )
        except ApiError as e:
            raise ValueError(f"Reka API error: {e.status_code}{e.body}")

        async defgen() -> ChatResponseAsyncGen:
            prev_content = ""
            async for chunk in stream:
                content = chunk.responses[0].chunk.content
                content_delta = content[len(prev_content) :]
                prev_content = content
                yield ChatResponse(
                    message=ChatMessage(
                        role=MessageRole.ASSISTANT,
                        content=content,
                    ),
                    delta=content_delta,
                    raw=chunk.__dict__,
                )

        return gen()

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
"""
        Send an asynchronous streaming completion request to the Reka API.

        Args:
            prompt (str): The prompt for completion.
            **kwargs: Additional keyword arguments for the API call.

        Returns:
            CompletionResponseAsyncGen: An asynchronous generator yielding completion responses.

        Raises:
            ValueError: If there's an error with the Reka API call.

        Example:
            >>> import asyncio
            >>> from llama_index.llms.reka import RekaLLM

            >>> async def main():
            ...     reka_llm = RekaLLM(api_key="your-api-key-here")
            ...     prompt = "Write a haiku about artificial intelligence:"
            ...     async for chunk in await reka_llm.astream_complete(prompt):
            ...         print(chunk.delta, end="", flush=True)
            ...     print()  # New line after the haiku is complete

            >>> asyncio.run(main())

        """
        all_kwargs = self._get_all_kwargs(**kwargs)
        try:
            stream = self._aclient.chat.create_stream(
                messages=[{"role": "user", "content": prompt}], **all_kwargs
            )
        except ApiError as e:
            raise ValueError(f"Reka API error: {e.status_code}{e.body}")

        async defgen() -> CompletionResponseAsyncGen:
            prev_text = ""
            async for chunk in stream:
                text = chunk.responses[0].chunk.content
                text_delta = text[len(prev_text) :]
                prev_text = text
                yield CompletionResponse(
                    text=text,
                    delta=text_delta,
                    raw=chunk.__dict__,
                )

        return gen()

```
 |  
| --- | --- |  
###  chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/reka/#llama_index.llms.reka.RekaLLM.chat "Permanent link")

```
chat(
    messages: Sequence[], **kwargs: 
) -> 

```

Send a chat request to the Reka API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  A sequence of chat messages.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments for the API call.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `ChatResponse`  |   |  The response from the Reka API.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If there's an error with the Reka API call.  |  
Example
> > > reka_llm = RekaLLM(api_key="your-api-key-here") messages = [ ... ChatMessage(role=MessageRole.SYSTEM, content="You are a helpful assistant."), ... ChatMessage(role=MessageRole.USER, content="What's the capital of France?") ... ] response = reka_llm.chat(messages) print(response.message.content)
Source code in `llama-index-integrations/llms/llama-index-llms-reka/llama_index/llms/reka/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
"""
    Send a chat request to the Reka API.

    Args:
        messages (Sequence[ChatMessage]): A sequence of chat messages.
        **kwargs: Additional keyword arguments for the API call.

    Returns:
        ChatResponse: The response from the Reka API.

    Raises:
        ValueError: If there's an error with the Reka API call.

    Example:
        >>> reka_llm = RekaLLM(api_key="your-api-key-here")
        >>> messages = [
        ...     ChatMessage(role=MessageRole.SYSTEM, content="You are a helpful assistant."),
        ...     ChatMessage(role=MessageRole.USER, content="What's the capital of France?")
        ... ]
        >>> response = reka_llm.chat(messages)
        >>> print(response.message.content)

    """
    all_kwargs = self._get_all_kwargs(**kwargs)
    reka_messages = process_messages_for_reka(messages)

    try:
        response = self._client.chat.create(messages=reka_messages, **all_kwargs)
        return ChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT,
                content=response.responses[0].message.content,
            ),
            raw=response.__dict__,
        )
    except ApiError as e:
        raise ValueError(f"Reka API error: {e.status_code}{e.body}")

```
 |  
| --- | --- |  
###  complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/reka/#llama_index.llms.reka.RekaLLM.complete "Permanent link")

```
complete(prompt: , **kwargs: ) -> 

```

Send a completion request to the Reka API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  The prompt for completion.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments for the API call.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `CompletionResponse`  |   |  The response from the Reka API.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If there's an error with the Reka API call.  |  
Example
> > > reka_llm = RekaLLM(api_key="your-api-key-here") response = reka_llm.complete("The capital of France is") print(response.text)
Source code in `llama-index-integrations/llms/llama-index-llms-reka/llama_index/llms/reka/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defcomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
"""
    Send a completion request to the Reka API.

    Args:
        prompt (str): The prompt for completion.
        **kwargs: Additional keyword arguments for the API call.

    Returns:
        CompletionResponse: The response from the Reka API.

    Raises:
        ValueError: If there's an error with the Reka API call.

    Example:
        >>> reka_llm = RekaLLM(api_key="your-api-key-here")
        >>> response = reka_llm.complete("The capital of France is")
        >>> print(response.text)

    """
    all_kwargs = self._get_all_kwargs(**kwargs)
    try:
        response = self._client.chat.create(
            messages=[{"role": "user", "content": prompt}], **all_kwargs
        )
        return CompletionResponse(
            text=response.responses[0].message.content,
            raw=response.__dict__,
        )
    except ApiError as e:
        raise ValueError(f"Reka API error: {e.status_code}{e.body}")

```
 |  
| --- | --- |  
###  stream_chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/reka/#llama_index.llms.reka.RekaLLM.stream_chat "Permanent link")

```
stream_chat(
    messages: Sequence[], **kwargs: 
) -> ChatResponseGen

```

Send a streaming chat request to the Reka API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  A sequence of chat messages.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments for the API call.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `ChatResponseGen`  |  `ChatResponseGen`  |  A generator yielding chat responses.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If there's an error with the Reka API call.  |  
Example
> > > reka_llm = RekaLLM(api_key="your-api-key-here") messages = [ ... ChatMessage(role=MessageRole.SYSTEM, content="You are a helpful assistant."), ... ChatMessage(role=MessageRole.USER, content="Tell me a short story.") ... ] for chunk in reka_llm.stream_chat(messages): ... print(chunk.delta, end="", flush=True)
Source code in `llama-index-integrations/llms/llama-index-llms-reka/llama_index/llms/reka/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
defstream_chat(
    self, messages: Sequence[ChatMessage], **kwargs: Any
) -> ChatResponseGen:
"""
    Send a streaming chat request to the Reka API.

    Args:
        messages (Sequence[ChatMessage]): A sequence of chat messages.
        **kwargs: Additional keyword arguments for the API call.

    Returns:
        ChatResponseGen: A generator yielding chat responses.

    Raises:
        ValueError: If there's an error with the Reka API call.

    Example:
        >>> reka_llm = RekaLLM(api_key="your-api-key-here")
        >>> messages = [
        ...     ChatMessage(role=MessageRole.SYSTEM, content="You are a helpful assistant."),
        ...     ChatMessage(role=MessageRole.USER, content="Tell me a short story.")
        ... ]
        >>> for chunk in reka_llm.stream_chat(messages):
        ...     print(chunk.delta, end="", flush=True)

    """
    all_kwargs = self._get_all_kwargs(**kwargs)
    reka_messages = process_messages_for_reka(messages)

    try:
        stream = self._client.chat.create_stream(
            messages=reka_messages, **all_kwargs
        )
    except ApiError as e:
        raise ValueError(f"Reka API error: {e.status_code}{e.body}")

    defgen() -> ChatResponseGen:
        prev_content = ""
        for chunk in stream:
            content = chunk.responses[0].chunk.content
            content_delta = content[len(prev_content) :]
            prev_content = content
            yield ChatResponse(
                message=ChatMessage(
                    role=MessageRole.ASSISTANT,
                    content=content,
                ),
                delta=content_delta,
                raw=chunk.__dict__,
            )

    return gen()

```
 |  
| --- | --- |  
###  stream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/reka/#llama_index.llms.reka.RekaLLM.stream_complete "Permanent link")

```
stream_complete(
    prompt: , **kwargs: 
) -> CompletionResponseGen

```

Send a streaming completion request to the Reka API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  The prompt for completion.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments for the API call.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `CompletionResponseGen`  |  `CompletionResponseGen`  |  A generator yielding completion responses.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If there's an error with the Reka API call.  |  
Example
> > > reka_llm = RekaLLM(api_key="your-api-key-here") prompt = "Write a haiku about programming:" for chunk in reka_llm.stream_complete(prompt): ... print(chunk.delta, end="", flush=True)
Source code in `llama-index-integrations/llms/llama-index-llms-reka/llama_index/llms/reka/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defstream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
"""
    Send a streaming completion request to the Reka API.

    Args:
        prompt (str): The prompt for completion.
        **kwargs: Additional keyword arguments for the API call.

    Returns:
        CompletionResponseGen: A generator yielding completion responses.

    Raises:
        ValueError: If there's an error with the Reka API call.

    Example:
        >>> reka_llm = RekaLLM(api_key="your-api-key-here")
        >>> prompt = "Write a haiku about programming:"
        >>> for chunk in reka_llm.stream_complete(prompt):
        ...     print(chunk.delta, end="", flush=True)

    """
    all_kwargs = self._get_all_kwargs(**kwargs)
    try:
        stream = self._client.chat.create_stream(
            messages=[{"role": "user", "content": prompt}], **all_kwargs
        )
    except ApiError as e:
        raise ValueError(f"Reka API error: {e.status_code}{e.body}")

    defgen() -> CompletionResponseGen:
        prev_text = ""
        for chunk in stream:
            text = chunk.responses[0].chunk.content
            text_delta = text[len(prev_text) :]
            prev_text = text
            yield CompletionResponse(
                text=text,
                delta=text_delta,
                raw=chunk.__dict__,
            )

    return gen()

```
 |  
| --- | --- |  
###  achat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/reka/#llama_index.llms.reka.RekaLLM.achat "Permanent link")

```
achat(
    messages: Sequence[], **kwargs: 
) -> 

```

Send an asynchronous chat request to the Reka API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  A sequence of chat messages.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments for the API call.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `ChatResponse`  |   |  The response from the Reka API.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If there's an error with the Reka API call.  |  
Example
> > > import asyncio from llama_index.llms.reka import RekaLLM from llama_index.core.base.llms.types import ChatMessage, MessageRole
>>> async def main(): ... reka_llm = RekaLLM(api_key="your-api-key-here") ... messages = [ ... ChatMessage(role=MessageRole.SYSTEM, content="You are a helpful assistant."), ... ChatMessage(role=MessageRole.USER, content="What's the meaning of life?") ... ] ... response = await reka_llm.achat(messages) ... print(response.message.content)
>>> asyncio.run(main())
Source code in `llama-index-integrations/llms/llama-index-llms-reka/llama_index/llms/reka/base.py`  
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
```
 | 
```
@llm_chat_callback()
async defachat(
    self, messages: Sequence[ChatMessage], **kwargs: Any
) -> ChatResponse:
"""
    Send an asynchronous chat request to the Reka API.

    Args:
        messages (Sequence[ChatMessage]): A sequence of chat messages.
        **kwargs: Additional keyword arguments for the API call.

    Returns:
        ChatResponse: The response from the Reka API.

    Raises:
        ValueError: If there's an error with the Reka API call.

    Example:
        >>> import asyncio
        >>> from llama_index.llms.reka import RekaLLM
        >>> from llama_index.core.base.llms.types import ChatMessage, MessageRole

        >>> async def main():
        ...     reka_llm = RekaLLM(api_key="your-api-key-here")
        ...     messages = [
        ...         ChatMessage(role=MessageRole.SYSTEM, content="You are a helpful assistant."),
        ...         ChatMessage(role=MessageRole.USER, content="What's the meaning of life?")
        ...     ]
        ...     response = await reka_llm.achat(messages)
        ...     print(response.message.content)

        >>> asyncio.run(main())

    """
    all_kwargs = self._get_all_kwargs(**kwargs)
    reka_messages = process_messages_for_reka(messages)

    try:
        response = await self._aclient.chat.create(
            messages=reka_messages, **all_kwargs
        )
        return ChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT,
                content=response.responses[0].message.content,
            ),
            raw=response.__dict__,
        )
    except ApiError as e:
        raise ValueError(f"Reka API error: {e.status_code}{e.body}")

```
 |  
| --- | --- |  
###  acomplete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/reka/#llama_index.llms.reka.RekaLLM.acomplete "Permanent link")

```
acomplete(prompt: , **kwargs: ) -> 

```

Send an asynchronous completion request to the Reka API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  The prompt for completion.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments for the API call.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `CompletionResponse`  |   |  The response from the Reka API.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If there's an error with the Reka API call.  |  
Example
> > > import asyncio from llama_index.llms.reka import RekaLLM
>>> async def main(): ... reka_llm = RekaLLM(api_key="your-api-key-here") ... prompt = "The capital of France is" ... response = await reka_llm.acomplete(prompt) ... print(response.text)
>>> asyncio.run(main())
Source code in `llama-index-integrations/llms/llama-index-llms-reka/llama_index/llms/reka/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
async defacomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
"""
    Send an asynchronous completion request to the Reka API.

    Args:
        prompt (str): The prompt for completion.
        **kwargs: Additional keyword arguments for the API call.

    Returns:
        CompletionResponse: The response from the Reka API.

    Raises:
        ValueError: If there's an error with the Reka API call.

    Example:
        >>> import asyncio
        >>> from llama_index.llms.reka import RekaLLM

        >>> async def main():
        ...     reka_llm = RekaLLM(api_key="your-api-key-here")
        ...     prompt = "The capital of France is"
        ...     response = await reka_llm.acomplete(prompt)
        ...     print(response.text)

        >>> asyncio.run(main())

    """
    all_kwargs = self._get_all_kwargs(**kwargs)
    try:
        response = await self._aclient.chat.create(
            messages=[{"role": "user", "content": prompt}], **all_kwargs
        )
        return CompletionResponse(
            text=response.responses[0].message.content,
            raw=response.__dict__,
        )
    except ApiError as e:
        raise ValueError(f"Reka API error: {e.status_code}{e.body}")

```
 |  
| --- | --- |  
###  astream_chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/reka/#llama_index.llms.reka.RekaLLM.astream_chat "Permanent link")

```
astream_chat(
    messages: Sequence[], **kwargs: 
) -> ChatResponseAsyncGen

```

Send an asynchronous streaming chat request to the Reka API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  A sequence of chat messages.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments for the API call.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `ChatResponseAsyncGen`  |  `ChatResponseAsyncGen`  |  An asynchronous generator yielding chat responses.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If there's an error with the Reka API call.  |  
Example
> > > import asyncio from llama_index.llms.reka import RekaLLM from llama_index.core.base.llms.types import ChatMessage, MessageRole
>>> async def main(): ... reka_llm = RekaLLM(api_key="your-api-key-here") ... messages = [ ... ChatMessage(role=MessageRole.SYSTEM, content="You are a helpful assistant."), ... ChatMessage(role=MessageRole.USER, content="Tell me a short story about a robot.") ... ] ... async for chunk in await reka_llm.astream_chat(messages): ... print(chunk.delta, end="", flush=True) ... print() # New line after the story is complete
>>> asyncio.run(main())
Source code in `llama-index-integrations/llms/llama-index-llms-reka/llama_index/llms/reka/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
async defastream_chat(
    self, messages: Sequence[ChatMessage], **kwargs: Any
) -> ChatResponseAsyncGen:
"""
    Send an asynchronous streaming chat request to the Reka API.

    Args:
        messages (Sequence[ChatMessage]): A sequence of chat messages.
        **kwargs: Additional keyword arguments for the API call.

    Returns:
        ChatResponseAsyncGen: An asynchronous generator yielding chat responses.

    Raises:
        ValueError: If there's an error with the Reka API call.

    Example:
        >>> import asyncio
        >>> from llama_index.llms.reka import RekaLLM
        >>> from llama_index.core.base.llms.types import ChatMessage, MessageRole

        >>> async def main():
        ...     reka_llm = RekaLLM(api_key="your-api-key-here")
        ...     messages = [
        ...         ChatMessage(role=MessageRole.SYSTEM, content="You are a helpful assistant."),
        ...         ChatMessage(role=MessageRole.USER, content="Tell me a short story about a robot.")
        ...     ]
        ...     async for chunk in await reka_llm.astream_chat(messages):
        ...         print(chunk.delta, end="", flush=True)
        ...     print()  # New line after the story is complete

        >>> asyncio.run(main())

    """
    all_kwargs = self._get_all_kwargs(**kwargs)
    reka_messages = process_messages_for_reka(messages)

    try:
        stream = self._aclient.chat.create_stream(
            messages=reka_messages, **all_kwargs
        )
    except ApiError as e:
        raise ValueError(f"Reka API error: {e.status_code}{e.body}")

    async defgen() -> ChatResponseAsyncGen:
        prev_content = ""
        async for chunk in stream:
            content = chunk.responses[0].chunk.content
            content_delta = content[len(prev_content) :]
            prev_content = content
            yield ChatResponse(
                message=ChatMessage(
                    role=MessageRole.ASSISTANT,
                    content=content,
                ),
                delta=content_delta,
                raw=chunk.__dict__,
            )

    return gen()

```
 |  
| --- | --- |  
###  astream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/reka/#llama_index.llms.reka.RekaLLM.astream_complete "Permanent link")

```
astream_complete(
    prompt: , **kwargs: 
) -> CompletionResponseAsyncGen

```

Send an asynchronous streaming completion request to the Reka API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  The prompt for completion.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments for the API call.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `CompletionResponseAsyncGen`  |  `CompletionResponseAsyncGen`  |  An asynchronous generator yielding completion responses.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If there's an error with the Reka API call.  |  
Example
> > > import asyncio from llama_index.llms.reka import RekaLLM
>>> async def main(): ... reka_llm = RekaLLM(api_key="your-api-key-here") ... prompt = "Write a haiku about artificial intelligence:" ... async for chunk in await reka_llm.astream_complete(prompt): ... print(chunk.delta, end="", flush=True) ... print() # New line after the haiku is complete
>>> asyncio.run(main())
Source code in `llama-index-integrations/llms/llama-index-llms-reka/llama_index/llms/reka/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
async defastream_complete(
    self, prompt: str, **kwargs: Any
) -> CompletionResponseAsyncGen:
"""
    Send an asynchronous streaming completion request to the Reka API.

    Args:
        prompt (str): The prompt for completion.
        **kwargs: Additional keyword arguments for the API call.

    Returns:
        CompletionResponseAsyncGen: An asynchronous generator yielding completion responses.

    Raises:
        ValueError: If there's an error with the Reka API call.

    Example:
        >>> import asyncio
        >>> from llama_index.llms.reka import RekaLLM

        >>> async def main():
        ...     reka_llm = RekaLLM(api_key="your-api-key-here")
        ...     prompt = "Write a haiku about artificial intelligence:"
        ...     async for chunk in await reka_llm.astream_complete(prompt):
        ...         print(chunk.delta, end="", flush=True)
        ...     print()  # New line after the haiku is complete

        >>> asyncio.run(main())

    """
    all_kwargs = self._get_all_kwargs(**kwargs)
    try:
        stream = self._aclient.chat.create_stream(
            messages=[{"role": "user", "content": prompt}], **all_kwargs
        )
    except ApiError as e:
        raise ValueError(f"Reka API error: {e.status_code}{e.body}")

    async defgen() -> CompletionResponseAsyncGen:
        prev_text = ""
        async for chunk in stream:
            text = chunk.responses[0].chunk.content
            text_delta = text[len(prev_text) :]
            prev_text = text
            yield CompletionResponse(
                text=text,
                delta=text_delta,
                raw=chunk.__dict__,
            )

    return gen()

```
 |  
| --- | --- |  
options: members: - RekaAI
