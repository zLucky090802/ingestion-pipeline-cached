# Ipex llm
##  IpexLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/ipex_llm/#llama_index.llms.ipex_llm.IpexLLM "Permanent link")
Bases: `CustomLLM`
IPEX-LLM.
Example
.. code-block:: python

```
from llama_index.llms.ipex_llm import IpexLLM
llm = IpexLLM(model_path="/path/to/llama/model")

```
Source code in `llama-index-integrations/llms/llama-index-llms-ipex-llm/llama_index/llms/ipex_llm/base.py`  
| 
```
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
```
 | 
```
classIpexLLM(CustomLLM):
r"""
    IPEX-LLM.

    Example:
        .. code-block:: python

            from llama_index.llms.ipex_llm import IpexLLM
            llm = IpexLLM(model_path="/path/to/llama/model")

    """

    model_name: str = Field(
        default=DEFAULT_HUGGINGFACE_MODEL,
        description=(
            "The model name to use from HuggingFace. "
            "Unused if `model` is passed in directly."
        ),
    )
    load_in_4bit: bool = Field(
        default=True,
        description=(
            "Whether to load model in 4bit.Unused if `load_in_low_bit` is not None."
        ),
    )
    load_in_low_bit: str = Field(
        default=None,
        description=(
            "Which low bit precisions to use when loading model. "
            "Example values: 'sym_int4', 'asym_int4', 'fp4', 'nf4', 'fp8', etc."
            "Will override `load_in_4bit` if this is specified."
        ),
    )
    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description="The maximum number of tokens available for input.",
        gt=0,
    )
    max_new_tokens: int = Field(
        default=DEFAULT_NUM_OUTPUTS,
        description="The maximum number of tokens to generate.",
        gt=0,
    )
    tokenizer_name: str = Field(
        default=DEFAULT_HUGGINGFACE_MODEL,
        description=(
            "The name of the tokenizer to use from HuggingFace. "
            "Unused if `tokenizer` is passed in directly."
        ),
    )
    device_map: str = Field(
        default="cpu", description="The device_map to use. Defaults to 'cpu'."
    )
    stopping_ids: List[int] = Field(
        default_factory=list,
        description=(
            "The stopping ids to use. "
            "Generation stops when these token IDs are predicted."
        ),
    )
    tokenizer_outputs_to_remove: list = Field(
        default_factory=list,
        description=(
            "The outputs to remove from the tokenizer. "
            "Sometimes huggingface tokenizers return extra inputs that cause errors."
        ),
    )
    tokenizer_kwargs: dict = Field(
        default_factory=dict, description="The kwargs to pass to the tokenizer."
    )
    model_kwargs: dict = Field(
        default_factory=dict,
        description="The kwargs to pass to the model during initialization.",
    )
    generate_kwargs: dict = Field(
        default_factory=dict,
        description="The kwargs to pass to the model during generation.",
    )
    is_chat_model: bool = Field(
        default=False,
        description=(
            LLMMetadata.__fields__["is_chat_model"].description
            + " Be sure to verify that you either pass an appropriate tokenizer "
            "that can convert prompts to properly formatted chat messages or a "
            "`messages_to_prompt` that does so."
        ),
    )

    _model: Any = PrivateAttr()
    _tokenizer: Any = PrivateAttr()
    _stopping_criteria: Any = PrivateAttr()

    def__init__(
        self,
        context_window: int = DEFAULT_CONTEXT_WINDOW,
        max_new_tokens: int = DEFAULT_NUM_OUTPUTS,
        tokenizer_name: str = DEFAULT_HUGGINGFACE_MODEL,
        model_name: str = DEFAULT_HUGGINGFACE_MODEL,
        load_in_4bit: Optional[bool] = True,
        load_in_low_bit: Optional[str] = None,
        model: Optional[Any] = None,
        tokenizer: Optional[Any] = None,
        device_map: str = "cpu",
        stopping_ids: Optional[List[int]] = None,
        tokenizer_kwargs: Optional[dict] = None,
        tokenizer_outputs_to_remove: Optional[list] = None,
        model_kwargs: Optional[dict] = None,
        generate_kwargs: Optional[dict] = None,
        is_chat_model: Optional[bool] = False,
        callback_manager: Optional[CallbackManager] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        low_bit_model: Optional[bool] = False,
    ) -> None:
"""
        Construct IpexLLM.

        Args:
            context_window: The maximum number of tokens available for input.
            max_new_tokens: The maximum number of tokens to generate.
            tokenizer_name: The name of the tokenizer to use from HuggingFace.
                        Unused if `tokenizer` is passed in directly.
            model_name: The model name to use from HuggingFace.
                        Unused if `model` is passed in directly.
            model: The HuggingFace model.
            tokenizer: The tokenizer.
            device_map: The device_map to use. Defaults to 'cpu'.
            stopping_ids: The stopping ids to use.
                        Generation stops when these token IDs are predicted.
            tokenizer_kwargs: The kwargs to pass to the tokenizer.
            tokenizer_outputs_to_remove: The outputs to remove from the tokenizer.
                        Sometimes huggingface tokenizers return extra inputs that cause errors.
            model_kwargs: The kwargs to pass to the model during initialization.
            generate_kwargs: The kwargs to pass to the model during generation.
            is_chat_model: Whether the model is `chat`
            callback_manager: Callback manager.
            messages_to_prompt: Function to convert messages to prompt.
            completion_to_prompt: Function to convert messages to prompt.
            pydantic_program_mode: DEFAULT.
            output_parser: BaseOutputParser.

        Returns:
            None.

        """
        model_kwargs = model_kwargs or {}

        if model:
            model = model
        else:
            model = self._load_model(
                low_bit_model, load_in_4bit, load_in_low_bit, model_name, model_kwargs
            )
        if device_map not in ["cpu", "xpu"] and not device_map.startswith("xpu:"):
            raise ValueError(
                "IpexLLMEmbedding currently only supports device to be 'cpu', 'xpu', "
                f"or 'xpu:<device_id>', but you have: {device_map}."
            )
        if "xpu" in device_map:
            model = model.to(device_map)

        # check context_window
        config_dict = model.config.to_dict()
        model_context_window = int(
            config_dict.get("max_position_embeddings", context_window)
        )
        if model_context_window and model_context_window  context_window:
            logger.warning(
                f"Supplied context_window {context_window} is greater "
                f"than the model's max input size {model_context_window}. "
                "Disable this warning by setting a lower context_window."
            )
            context_window = model_context_window

        tokenizer_kwargs = tokenizer_kwargs or {}
        if "max_length" not in tokenizer_kwargs:
            tokenizer_kwargs["max_length"] = context_window

        if tokenizer:
            tokenizer = tokenizer
        else:
            try:
                tokenizer = AutoTokenizer.from_pretrained(
                    tokenizer_name, **tokenizer_kwargs
                )
            except Exception:
                tokenizer = LlamaTokenizer.from_pretrained(
                    tokenizer_name, trust_remote_code=True
                )

        if tokenizer_name != model_name:
            logger.warning(
                f"The model `{model_name}` and tokenizer `{tokenizer_name}` "
                f"are from different paths, please ensure that they are compatible."
            )

        # setup stopping criteria
        stopping_ids_list = stopping_ids or []

        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        classStopOnTokens(StoppingCriteria):
            def__call__(
                self,
                input_ids: torch.LongTensor,
                scores: torch.FloatTensor,
                **kwargs: Any,
            ) -> bool:
                for stop_id in stopping_ids_list:
                    if input_ids[0][-1] == stop_id:
                        return True
                return False

        stopping_criteria = StoppingCriteriaList([StopOnTokens()])

        messages_to_prompt = messages_to_prompt or self._tokenizer_messages_to_prompt

        super().__init__(
            context_window=context_window,
            max_new_tokens=max_new_tokens,
            tokenizer_name=tokenizer_name,
            model_name=model_name,
            device_map=device_map,
            stopping_ids=stopping_ids or [],
            tokenizer_kwargs=tokenizer_kwargs or {},
            tokenizer_outputs_to_remove=tokenizer_outputs_to_remove or [],
            model_kwargs=model_kwargs or {},
            generate_kwargs=generate_kwargs or {},
            is_chat_model=is_chat_model,
            callback_manager=callback_manager,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )

        self._model = model
        self._tokenizer = tokenizer
        self._stopping_criteria = stopping_criteria

    @classmethod
    deffrom_model_id(
        cls,
        context_window: int = DEFAULT_CONTEXT_WINDOW,
        max_new_tokens: int = DEFAULT_NUM_OUTPUTS,
        tokenizer_name: str = DEFAULT_HUGGINGFACE_MODEL,
        model_name: str = DEFAULT_HUGGINGFACE_MODEL,
        load_in_4bit: Optional[bool] = True,
        load_in_low_bit: Optional[str] = None,
        model: Optional[Any] = None,
        tokenizer: Optional[Any] = None,
        device_map: str = "cpu",
        stopping_ids: Optional[List[int]] = None,
        tokenizer_kwargs: Optional[dict] = None,
        tokenizer_outputs_to_remove: Optional[list] = None,
        model_kwargs: Optional[dict] = None,
        generate_kwargs: Optional[dict] = None,
        is_chat_model: Optional[bool] = False,
        callback_manager: Optional[CallbackManager] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
    ):
        return cls(
            context_window=context_window,
            max_new_tokens=max_new_tokens,
            tokenizer_name=tokenizer_name,
            model_name=model_name,
            load_in_4bit=load_in_4bit,
            load_in_low_bit=load_in_low_bit,
            model=model,
            tokenizer=tokenizer,
            device_map=device_map,
            stopping_ids=stopping_ids,
            tokenizer_kwargs=tokenizer_kwargs,
            tokenizer_outputs_to_remove=tokenizer_outputs_to_remove,
            model_kwargs=model_kwargs,
            generate_kwargs=generate_kwargs,
            is_chat_model=is_chat_model,
            callback_manager=callback_manager,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
            low_bit_model=False,
        )

    @classmethod
    deffrom_model_id_low_bit(
        cls,
        context_window: int = DEFAULT_CONTEXT_WINDOW,
        max_new_tokens: int = DEFAULT_NUM_OUTPUTS,
        tokenizer_name: str = DEFAULT_HUGGINGFACE_MODEL,
        model_name: str = DEFAULT_HUGGINGFACE_MODEL,
        model: Optional[Any] = None,
        tokenizer: Optional[Any] = None,
        device_map: str = "cpu",
        stopping_ids: Optional[List[int]] = None,
        tokenizer_kwargs: Optional[dict] = None,
        tokenizer_outputs_to_remove: Optional[list] = None,
        model_kwargs: Optional[dict] = None,
        generate_kwargs: Optional[dict] = None,
        is_chat_model: Optional[bool] = False,
        callback_manager: Optional[CallbackManager] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
    ):
        return cls(
            context_window=context_window,
            max_new_tokens=max_new_tokens,
            tokenizer_name=tokenizer_name,
            model_name=model_name,
            model=model,
            tokenizer=tokenizer,
            device_map=device_map,
            stopping_ids=stopping_ids,
            tokenizer_kwargs=tokenizer_kwargs,
            tokenizer_outputs_to_remove=tokenizer_outputs_to_remove,
            model_kwargs=model_kwargs,
            generate_kwargs=generate_kwargs,
            is_chat_model=is_chat_model,
            callback_manager=callback_manager,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
            low_bit_model=True,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "IpexLLM"

    @property
    defmetadata(self) -> LLMMetadata:
"""LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.max_new_tokens,
            model_name=self.model_name,
            is_chat_model=self.is_chat_model,
        )

    def_load_model(
        self,
        low_bit_model: bool,
        load_in_4bit: bool,
        load_in_low_bit: str,
        model_name: str,
        model_kwargs: Any,
    ) -> Any:
"""Attempts to load a model with AutoModelForCausalLM and falls back to AutoModel on failure."""
        fromipex_llm.transformersimport AutoModelForCausalLM, AutoModel

        load_kwargs = {"use_cache": True, "trust_remote_code": True}

        if not low_bit_model:
            if load_in_low_bit is not None:
                load_function_name = "from_pretrained"
                load_kwargs["load_in_low_bit"] = load_in_low_bit
            else:
                load_function_name = "from_pretrained"
                load_kwargs["load_in_4bit"] = load_in_4bit
        else:
            load_function_name = "load_low_bit"

        try:
            # Attempt to load with AutoModelForCausalLM
            return self._load_model_general(
                AutoModelForCausalLM,
                load_function_name,
                model_name,
                load_kwargs,
                model_kwargs,
            )
        except Exception:
            # Fallback to AutoModel if there's an exception
            return self._load_model_general(
                AutoModel, load_function_name, model_name, load_kwargs, model_kwargs
            )

    def_load_model_general(
        self,
        model_class: Any,
        load_function_name: str,
        model_name: str,
        load_kwargs,
        model_kwargs: dict,
    ) -> Any:
"""General function to attempt to load a model."""
        try:
            load_function = getattr(model_class, load_function_name)
            return load_function(model_name, **{**load_kwargs, **model_kwargs})
        except Exception as e:
            logger.error(
                f"Failed to load model using {model_class.__name__}.{load_function_name}: {e}"
            )

    def_tokenizer_messages_to_prompt(self, messages: Sequence[ChatMessage]) -> str:
"""
        Use the tokenizer to convert messages to prompt. Fallback to generic.

        Args:
            messages: Sequence of ChatMessage.

        Returns:
            Str of response.

        """
        if hasattr(self._tokenizer, "apply_chat_template"):
            messages_dict = [
                {"role": message.role.value, "content": message.content}
                for message in messages
            ]
            tokens = self._tokenizer.apply_chat_template(messages_dict)
            return self._tokenizer.decode(tokens)

        return generic_messages_to_prompt(messages)

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        prompt = self.messages_to_prompt(messages)
        completion_response = self.complete(prompt, formatted=True, **kwargs)
        return completion_response_to_chat_response(completion_response)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        prompt = self.messages_to_prompt(messages)
        completion_response = self.stream_complete(prompt, formatted=True, **kwargs)
        return stream_completion_response_to_chat_response(completion_response)

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
"""
        Complete by LLM.

        Args:
            prompt: Prompt for completion.
            formatted: Whether the prompt is formatted by wrapper.
            kwargs: Other kwargs for complete.

        Returns:
            CompletionReponse after generation.

        """
        if not formatted:
            prompt = self.completion_to_prompt(prompt)
        input_ids = self._tokenizer(prompt, return_tensors="pt")
        input_ids = input_ids.to(self._model.device)
        # remove keys from the tokenizer if needed, to avoid HF errors
        for key in self.tokenizer_outputs_to_remove:
            if key in input_ids:
                input_ids.pop(key, None)
        tokens = self._model.generate(
            **input_ids,
            max_new_tokens=self.max_new_tokens,
            stopping_criteria=self._stopping_criteria,
            pad_token_id=self._tokenizer.pad_token_id,
            **self.generate_kwargs,
        )
        completion_tokens = tokens[0][input_ids["input_ids"].size(1) :]
        completion = self._tokenizer.decode(completion_tokens, skip_special_tokens=True)

        return CompletionResponse(text=completion, raw={"model_output": tokens})

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
"""
        Complete by LLM in stream.

        Args:
            prompt: Prompt for completion.
            formatted: Whether the prompt is formatted by wrapper.
            kwargs: Other kwargs for complete.

        Returns:
            CompletionReponse after generation.

        """
        fromtransformersimport TextIteratorStreamer

        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        input_ids = self._tokenizer.encode(prompt, return_tensors="pt")
        input_ids = input_ids.to(self._model.device)

        for key in self.tokenizer_outputs_to_remove:
            if key in input_ids:
                input_ids.pop(key, None)

        streamer = TextIteratorStreamer(
            self._tokenizer, skip_prompt=True, skip_special_tokens=True
        )
        generation_kwargs = dict(
            input_ids=input_ids,
            streamer=streamer,
            max_new_tokens=self.max_new_tokens,
            stopping_criteria=self._stopping_criteria,
            pad_token_id=self._tokenizer.pad_token_id,
            **self.generate_kwargs,
        )
        thread = Thread(target=self._model.generate, kwargs=generation_kwargs)
        thread.start()

        # create generator based off of streamer
        defgen() -> CompletionResponseGen:
            text = ""
            for x in streamer:
                text += x
                yield CompletionResponse(text=text, delta=x)

        return gen()

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/ipex_llm/#llama_index.llms.ipex_llm.IpexLLM.metadata "Permanent link")

```
metadata: 

```

LLM metadata.
###  complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/ipex_llm/#llama_index.llms.ipex_llm.IpexLLM.complete "Permanent link")

```
complete(
    prompt: , formatted:  = False, **kwargs: 
) -> 

```

Complete by LLM.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  Prompt for completion.  |  _required_  |  
|  `formatted`  |  `bool`  |  Whether the prompt is formatted by wrapper.  |  `False`  |  
|  `kwargs`  |  Other kwargs for complete.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  CompletionReponse after generation.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-ipex-llm/llama_index/llms/ipex_llm/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defcomplete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponse:
"""
    Complete by LLM.

    Args:
        prompt: Prompt for completion.
        formatted: Whether the prompt is formatted by wrapper.
        kwargs: Other kwargs for complete.

    Returns:
        CompletionReponse after generation.

    """
    if not formatted:
        prompt = self.completion_to_prompt(prompt)
    input_ids = self._tokenizer(prompt, return_tensors="pt")
    input_ids = input_ids.to(self._model.device)
    # remove keys from the tokenizer if needed, to avoid HF errors
    for key in self.tokenizer_outputs_to_remove:
        if key in input_ids:
            input_ids.pop(key, None)
    tokens = self._model.generate(
        **input_ids,
        max_new_tokens=self.max_new_tokens,
        stopping_criteria=self._stopping_criteria,
        pad_token_id=self._tokenizer.pad_token_id,
        **self.generate_kwargs,
    )
    completion_tokens = tokens[0][input_ids["input_ids"].size(1) :]
    completion = self._tokenizer.decode(completion_tokens, skip_special_tokens=True)

    return CompletionResponse(text=completion, raw={"model_output": tokens})

```
 |  
| --- | --- |  
###  stream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/ipex_llm/#llama_index.llms.ipex_llm.IpexLLM.stream_complete "Permanent link")

```
stream_complete(
    prompt: , formatted:  = False, **kwargs: 
) -> CompletionResponseGen

```

Complete by LLM in stream.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  Prompt for completion.  |  _required_  |  
|  `formatted`  |  `bool`  |  Whether the prompt is formatted by wrapper.  |  `False`  |  
|  `kwargs`  |  Other kwargs for complete.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `CompletionResponseGen`  |  CompletionReponse after generation.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-ipex-llm/llama_index/llms/ipex_llm/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defstream_complete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponseGen:
"""
    Complete by LLM in stream.

    Args:
        prompt: Prompt for completion.
        formatted: Whether the prompt is formatted by wrapper.
        kwargs: Other kwargs for complete.

    Returns:
        CompletionReponse after generation.

    """
    fromtransformersimport TextIteratorStreamer

    if not formatted:
        prompt = self.completion_to_prompt(prompt)

    input_ids = self._tokenizer.encode(prompt, return_tensors="pt")
    input_ids = input_ids.to(self._model.device)

    for key in self.tokenizer_outputs_to_remove:
        if key in input_ids:
            input_ids.pop(key, None)

    streamer = TextIteratorStreamer(
        self._tokenizer, skip_prompt=True, skip_special_tokens=True
    )
    generation_kwargs = dict(
        input_ids=input_ids,
        streamer=streamer,
        max_new_tokens=self.max_new_tokens,
        stopping_criteria=self._stopping_criteria,
        pad_token_id=self._tokenizer.pad_token_id,
        **self.generate_kwargs,
    )
    thread = Thread(target=self._model.generate, kwargs=generation_kwargs)
    thread.start()

    # create generator based off of streamer
    defgen() -> CompletionResponseGen:
        text = ""
        for x in streamer:
            text += x
            yield CompletionResponse(text=text, delta=x)

    return gen()

```
 |  
| --- | --- |  
options: members: - IpexLLM
