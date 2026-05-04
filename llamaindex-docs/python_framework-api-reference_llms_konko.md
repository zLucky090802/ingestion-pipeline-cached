# Konko
##  Konko [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/konko/#llama_index.llms.konko.Konko "Permanent link")
Bases: 
Konko LLM.
Examples:
`pip install llama-index-llms-konko`

```
importos
fromllama_index.llms.konkoimport Konko
fromllama_index.core.llmsimport ChatMessage

# Set up the Konko LLM with the desired model
llm = Konko(model="meta-llama/llama-2-13b-chat")

# Set the Konko API key
os.environ["KONKO_API_KEY"] = "<your-api-key>"

# Create a ChatMessage object
message = ChatMessage(role="user", content="Explain Big Bang Theory briefly")

# Call the chat method with the ChatMessage object
response = llm.chat([message])

# Print the response
print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-konko/llama_index/llms/konko/base.py`  
| 
```
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
653
654
655
656
657
658
```
 | 
```
classKonko(LLM):
"""
    Konko LLM.

    Examples:
        `pip install llama-index-llms-konko`

        ```python
        import os
        from llama_index.llms.konko import Konko
        from llama_index.core.llms import ChatMessage

        # Set up the Konko LLM with the desired model
        llm = Konko(model="meta-llama/llama-2-13b-chat")

        # Set the Konko API key
        os.environ["KONKO_API_KEY"] = "<your-api-key>"

        # Create a ChatMessage object
        message = ChatMessage(role="user", content="Explain Big Bang Theory briefly")

        # Call the chat method with the ChatMessage object
        response = llm.chat([message])

        # Print the response
        print(response)
        ```

    """

    model: str = Field(
        default=DEFAULT_KONKO_MODEL, description="The konko model to use."
    )
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        description="The temperature to use during generation.",
        ge=0.0,
        le=1.0,
    )
    max_tokens: Optional[int] = Field(
        default=DEFAULT_NUM_OUTPUTS,
        description="The maximum number of tokens to generate.",
        gt=0,
    )
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the konko API."
    )
    max_retries: int = Field(
        default=10, description="The maximum number of API retries.", ge=0
    )

    konko_api_key: str = Field(default=None, description="The konko API key.")
    openai_api_key: str = Field(default=None, description="The Openai API key.")
    api_type: str = Field(default=None, description="The konko API type.")
    model_info_dict: Dict[str, ModelInfo]

    def__init__(
        self,
        model: str = DEFAULT_KONKO_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: Optional[int] = DEFAULT_NUM_OUTPUTS,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        max_retries: int = 10,
        konko_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        api_type: Optional[str] = None,
        api_base: Optional[str] = None,
        api_version: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        model_info_dict: Optional[Dict[str, ModelInfo]] = None,
        **kwargs: Any,
    ) -> None:
        additional_kwargs = additional_kwargs or {}
        (
            konko_api_key,
            openai_api_key,
            api_type,
            api_base,
            api_version,
        ) = resolve_konko_credentials(
            konko_api_key=konko_api_key,
            openai_api_key=openai_api_key,
            api_type=api_type,
            api_base=api_base,
            api_version=api_version,
        )
        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            additional_kwargs=additional_kwargs,
            max_retries=max_retries,
            callback_manager=callback_manager,
            konko_api_key=konko_api_key,
            openai_api_key=openai_api_key,
            api_type=api_type,
            api_version=api_version,
            api_base=api_base,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
            model_info_dict=self._create_model_info_dict(),
            **kwargs,
        )

    def_get_model_name(self) -> str:
        return self.model

    @classmethod
    defclass_name(cls) -> str:
        return "Konko_LLM"

    def_create_model_info_dict(self) -> Dict[str, ModelInfo]:
        models_info_dict = {}
        if is_openai_v1():
            models = konko.models.list().data
            for model in models:
                model_info = ModelInfo(
                    name=model.name,
                    max_context_length=model.max_context_length,
                    is_chat_model=model.is_chat,
                )
                models_info_dict[model.name] = model_info
        else:
            models = konko.Model.list().data
            for model in models:
                model_info = ModelInfo(
                    name=model["name"],
                    max_context_length=model["max_context_length"],
                    is_chat_model=model["is_chat"],
                )
                models_info_dict[model["name"]] = model_info

        return models_info_dict

    def_get_model_info(self) -> ModelInfo:
        model_name = self._get_model_name()
        model_info = self.model_info_dict.get(model_name)
        if model_info is None:
            raise ValueError(
                f"Unknown model: {model_name}. Please provide a valid Konko model name. "
                "Known models are: " + ", ".join(self.model_info_dict.keys())
            )
        return model_info

    def_is_chat_model(self) -> bool:
"""
        Check if the specified model is a chat model.

        Args:
        - model_id (str): The ID of the model to check.

        Returns:
        - bool: True if the model is a chat model, False otherwise.

        Raises:
        - ValueError: If the model_id is not found in the list of models.

        """
        model_info = self._get_model_info()
        return model_info.is_chat_model

    @property
    defmetadata(self) -> LLMMetadata:
        model_info = self._get_model_info()
        return LLMMetadata(
            context_window=model_info.max_context_length,
            num_output=self.max_tokens,
            is_chat_model=model_info.is_chat_model,
            model_name=self.model,
        )

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        if self._is_chat_model():
            chat_fn = self._chat
        else:
            chat_fn = completion_to_chat_decorator(self._complete)
        return chat_fn(messages, **kwargs)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        if self._is_chat_model():
            stream_chat_fn = self._stream_chat
        else:
            stream_chat_fn = stream_completion_to_chat_decorator(self._stream_complete)
        return stream_chat_fn(messages, **kwargs)

    @property
    def_credential_kwargs(self) -> Dict[str, Any]:
        return {
            "konko_api_key": self.konko_api_key,
            "api_type": self.api_type,
            "openai_api_key": self.openai_api_key,
        }

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        return {
            **base_kwargs,
            **self.additional_kwargs,
        }

    def_get_all_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        return {
            **self._model_kwargs,
            **kwargs,
        }

    def_chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        if not self._is_chat_model():
            raise ValueError("This model is not a chat model.")

        message_dicts = to_openai_message_dicts(messages)
        all_kwargs = self._get_all_kwargs(**kwargs)
        response = completion_with_retry(
            is_chat_model=self._is_chat_model(),
            max_retries=self.max_retries,
            messages=message_dicts,
            stream=False,
            **all_kwargs,
        )
        if is_openai_v1():
            message_dict = response.choices[0].message
        else:
            message_dict = response["choices"][0]["message"]
        message = from_openai_message_dict(message_dict)

        return ChatResponse(
            message=message,
            raw=response,
            additional_kwargs=self._get_response_token_counts(response),
        )

    def_stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        if not self._is_chat_model():
            raise ValueError("This model is not a chat model.")

        message_dicts = to_openai_message_dicts(messages)
        all_kwargs = self._get_all_kwargs(**kwargs)

        defgen() -> ChatResponseGen:
            content = ""
            for response in completion_with_retry(
                is_chat_model=self._is_chat_model(),
                max_retries=self.max_retries,
                messages=message_dicts,
                stream=True,
                **all_kwargs,
            ):
                if is_openai_v1():
                    if len(response.choices) == 0 and response.prompt_annotations:
                        continue
                    delta = (
                        response.choices[0].delta if len(response.choices)  0 else {}
                    )
                    role_value = delta.role
                    content_delta = delta.content or ""
                else:
                    if "choices" not in response or len(response["choices"]) == 0:
                        continue
                    delta = response["choices"][0].get("delta", {})
                    role_value = delta["role"]
                    content_delta = delta["content"] or ""

                role = role_value if role_value is not None else "assistant"
                content += content_delta
                yield ChatResponse(
                    message=ChatMessage(
                        role=role,
                        content=content,
                    ),
                    delta=content_delta,
                    raw=response,
                    additional_kwargs=self._get_response_token_counts(response),
                )

        return gen()

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        if self._is_chat_model():
            complete_fn = chat_to_completion_decorator(self._chat)
        else:
            complete_fn = self._complete
        return complete_fn(prompt, **kwargs)

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        if self._is_chat_model():
            stream_complete_fn = stream_chat_to_completion_decorator(self._stream_chat)
        else:
            stream_complete_fn = self._stream_complete
        return stream_complete_fn(prompt, **kwargs)

    def_get_response_token_counts(self, raw_response: Any) -> dict:
"""Get the token usage reported by the response."""
        if not isinstance(raw_response, dict):
            return {}

        usage = raw_response.get("usage", {})
        # NOTE: other model providers that use the OpenAI client may not report usage
        if usage is None:
            return {}

        return {
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
        }

    def_complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        if self._is_chat_model():
            raise ValueError("This model is a chat model.")

        all_kwargs = self._get_all_kwargs(**kwargs)
        if self.max_tokens is None:
            # NOTE: non-chat completion endpoint requires max_tokens to be set
            max_tokens = self._get_max_token_for_prompt(prompt)
            all_kwargs["max_tokens"] = max_tokens

        response = completion_with_retry(
            is_chat_model=self._is_chat_model(),
            max_retries=self.max_retries,
            prompt=prompt,
            stream=False,
            **all_kwargs,
        )
        if is_openai_v1():
            text = response.choices[0].text
        else:
            text = response["choices"][0]["text"]

        return CompletionResponse(
            text=text,
            raw=response,
            additional_kwargs=self._get_response_token_counts(response),
        )

    def_stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        if self._is_chat_model():
            raise ValueError("This model is a chat model.")

        all_kwargs = self._get_all_kwargs(**kwargs)
        if self.max_tokens is None:
            # NOTE: non-chat completion endpoint requires max_tokens to be set
            max_tokens = self._get_max_token_for_prompt(prompt)
            all_kwargs["max_tokens"] = max_tokens

        defgen() -> CompletionResponseGen:
            text = ""
            for response in completion_with_retry(
                is_chat_model=self._is_chat_model(),
                max_retries=self.max_retries,
                prompt=prompt,
                stream=True,
                **all_kwargs,
            ):
                if is_openai_v1():
                    if len(response.choices)  0:
                        delta = response.choices[0].text
                    else:
                        delta = ""
                else:
                    if len(response["choices"])  0:
                        delta = response["choices"][0].text
                    else:
                        delta = ""
                text += delta
                yield CompletionResponse(
                    delta=delta,
                    text=text,
                    raw=response,
                    additional_kwargs=self._get_response_token_counts(response),
                )

        return gen()

    def_get_max_token_for_prompt(self, prompt: str) -> int:
        try:
            importtiktoken
        except ImportError:
            raise ImportError(
                "Please install tiktoken to use the max_tokens=None feature."
            )
        context_window = self.metadata.context_window
        encoding = tiktoken.encoding_for_model(self._get_model_name())
        tokens = encoding.encode(prompt)
        max_token = context_window - len(tokens)
        if max_token <= 0:
            raise ValueError(
                f"The prompt is too long for the model. "
                f"Please use a prompt that is less than {context_window} tokens."
            )
        return max_token

    # ===== Async Endpoints =====
    @llm_chat_callback()
    async defachat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
        achat_fn: Callable[..., Awaitable[ChatResponse]]
        if self._is_chat_model():
            achat_fn = self._achat
        else:
            achat_fn = acompletion_to_chat_decorator(self._acomplete)
        return await achat_fn(messages, **kwargs)

    @llm_chat_callback()
    async defastream_chat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponseAsyncGen:
        astream_chat_fn: Callable[..., Awaitable[ChatResponseAsyncGen]]
        if self._is_chat_model():
            astream_chat_fn = self._astream_chat
        else:
            astream_chat_fn = astream_completion_to_chat_decorator(
                self._astream_complete
            )
        return await astream_chat_fn(messages, **kwargs)

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        if self._is_chat_model():
            acomplete_fn = achat_to_completion_decorator(self._achat)
        else:
            acomplete_fn = self._acomplete
        return await acomplete_fn(prompt, **kwargs)

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        if self._is_chat_model():
            astream_complete_fn = astream_chat_to_completion_decorator(
                self._astream_chat
            )
        else:
            astream_complete_fn = self._astream_complete
        return await astream_complete_fn(prompt, **kwargs)

    async def_achat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        if not self._is_chat_model():
            raise ValueError("This model is not a chat model.")

        message_dicts = to_openai_message_dicts(messages)
        all_kwargs = self._get_all_kwargs(**kwargs)
        response = await acompletion_with_retry(
            is_chat_model=self._is_chat_model(),
            max_retries=self.max_retries,
            messages=message_dicts,
            stream=False,
            **all_kwargs,
        )
        if is_openai_v1:  # type: ignore
            message_dict = response.choices[0].message
        else:
            message_dict = response["choices"][0]["message"]
        message = from_openai_message_dict(message_dict)

        return ChatResponse(
            message=message,
            raw=response,
            additional_kwargs=self._get_response_token_counts(response),
        )

    async def_astream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        if not self._is_chat_model():
            raise ValueError("This model is not a chat model.")

        message_dicts = to_openai_message_dicts(messages)
        all_kwargs = self._get_all_kwargs(**kwargs)

        async defgen() -> ChatResponseAsyncGen:
            content = ""
            _function_call: Optional[dict] = None
            async for response in await acompletion_with_retry(
                is_chat_model=self._is_chat_model(),
                max_retries=self.max_retries,
                messages=message_dicts,
                stream=True,
                **all_kwargs,
            ):
                if is_openai_v1():
                    if len(response.choices)  0:
                        delta = response.choices[0].delta
                    else:
                        delta = {}
                    role = delta.role
                    content_delta = delta.content
                else:
                    if len(response["choices"])  0:
                        delta = response["choices"][0].delta
                    else:
                        delta = {}
                    role = delta["role"]
                    content_delta = delta["content"]
                content += content_delta

                yield ChatResponse(
                    message=ChatMessage(
                        role=role,
                        content=content,
                    ),
                    delta=content_delta,
                    raw=response,
                    additional_kwargs=self._get_response_token_counts(response),
                )

        return gen()

    async def_acomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        if self._is_chat_model():
            raise ValueError("This model is a chat model.")

        all_kwargs = self._get_all_kwargs(**kwargs)
        if self.max_tokens is None:
            # NOTE: non-chat completion endpoint requires max_tokens to be set
            max_tokens = self._get_max_token_for_prompt(prompt)
            all_kwargs["max_tokens"] = max_tokens

        response = await acompletion_with_retry(
            is_chat_model=self._is_chat_model(),
            max_retries=self.max_retries,
            prompt=prompt,
            stream=False,
            **all_kwargs,
        )
        if is_openai_v1():
            text = response.choices[0].text
        else:
            text = response["choices"][0]["text"]
        return CompletionResponse(
            text=text,
            raw=response,
            additional_kwargs=self._get_response_token_counts(response),
        )

    async def_astream_complete(
        self, prompt: str, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        if self._is_chat_model():
            raise ValueError("This model is a chat model.")

        all_kwargs = self._get_all_kwargs(**kwargs)
        if self.max_tokens is None:
            # NOTE: non-chat completion endpoint requires max_tokens to be set
            max_tokens = self._get_max_token_for_prompt(prompt)
            all_kwargs["max_tokens"] = max_tokens

        async defgen() -> CompletionResponseAsyncGen:
            text = ""
            async for response in await acompletion_with_retry(
                is_chat_model=self._is_chat_model(),
                max_retries=self.max_retries,
                prompt=prompt,
                stream=True,
                **all_kwargs,
            ):
                if is_openai_v1():
                    if len(response.choices)  0:
                        delta = response.choices[0].text
                    else:
                        delta = ""
                else:
                    if len(response["choices"])  0:
                        delta = response["choices"][0].text
                    else:
                        delta = ""
                text += delta
                yield CompletionResponse(
                    delta=delta,
                    text=text,
                    raw=response,
                    additional_kwargs=self._get_response_token_counts(response),
                )

        return gen()

```
 |  
| --- | --- |  
options: members: - Konko
