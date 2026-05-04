# Mistralai
##  MistralAI [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/mistralai/#llama_index.llms.mistralai.MistralAI "Permanent link")
Bases: `FunctionCallingLLM`
MistralAI LLM.
Examples:
`pip install llama-index-llms-mistralai`

```
fromllama_index.llms.mistralaiimport MistralAI

# To customize your API key, do this
# otherwise it will lookup MISTRAL_API_KEY from your env variable
# llm = MistralAI(api_key="<api_key>")

# You can specify a custom endpoint by passing the `endpoint` variable or setting
# MISTRAL_ENDPOINT in your environment
# llm = MistralAI(endpoint="<endpoint>")

llm = MistralAI()

resp = llm.complete("Paul Graham is ")

print(resp)

```

Source code in `llama-index-integrations/llms/llama-index-llms-mistralai/llama_index/llms/mistralai/base.py`  
| 
```
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
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
```
 | 
```
classMistralAI(FunctionCallingLLM):
"""
    MistralAI LLM.

    Examples:
        `pip install llama-index-llms-mistralai`

        ```python
        from llama_index.llms.mistralai import MistralAI

        # To customize your API key, do this
        # otherwise it will lookup MISTRAL_API_KEY from your env variable
        # llm = MistralAI(api_key="<api_key>")

        # You can specify a custom endpoint by passing the `endpoint` variable or setting
        # MISTRAL_ENDPOINT in your environment
        # llm = MistralAI(endpoint="<endpoint>")

        llm = MistralAI()

        resp = llm.complete("Paul Graham is ")

        print(resp)
        ```

    """

    model: str = Field(
        default=DEFAULT_MISTRALAI_MODEL, description="The mistralai model to use."
    )
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        description="The temperature to use for sampling.",
        ge=0.0,
        le=1.0,
    )
    max_tokens: int = Field(
        default=DEFAULT_MISTRALAI_MAX_TOKENS,
        description="The maximum number of tokens to generate.",
        gt=0,
    )

    timeout: float = Field(
        default=120, description="The timeout to use in seconds.", ge=0
    )
    max_retries: int = Field(
        default=5, description="The maximum number of API retries.", ge=0
    )
    random_seed: Optional[int] = Field(
        default=None, description="The random seed to use for sampling."
    )
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the MistralAI API."
    )
    show_thinking: bool = Field(
        default=False,
        description="Whether to show thinking in the final response. Only available for reasoning models.",
    )

    _uses_azure: bool = PrivateAttr(default=False)
    _client: Mistral = PrivateAttr()
    _models: MistralModels = mistral_models

    def__init__(
        self,
        model: str = DEFAULT_MISTRALAI_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MISTRALAI_MAX_TOKENS,
        timeout: int = 120,
        max_retries: int = 5,
        safe_mode: bool = False,
        random_seed: Optional[int] = None,
        api_key: Optional[str] = None,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        endpoint: Optional[str] = None,
        azure_endpoint: Optional[str] = None,
        azure_api_key: Optional[str] = None,
        show_thinking: bool = False,
    ) -> None:
        additional_kwargs = additional_kwargs or {}
        callback_manager = callback_manager or CallbackManager([])

        api_key = get_from_param_or_env("api_key", api_key, "MISTRAL_API_KEY", "")

        if not api_key and not (azure_endpoint and azure_api_key):
            raise ValueError(
                "You must provide an API key to use mistralai. "
                "You can either pass it in as an argument or set it `MISTRAL_API_KEY`."
            )

        # Use the custom endpoint if provided, otherwise default to DEFAULT_MISTRALAI_ENDPOINT
        endpoint = get_from_param_or_env(
            "endpoint", endpoint, "MISTRAL_ENDPOINT", DEFAULT_MISTRALAI_ENDPOINT
        )

        super().__init__(
            temperature=temperature,
            max_tokens=max_tokens,
            additional_kwargs=additional_kwargs,
            timeout=timeout,
            max_retries=max_retries,
            safe_mode=safe_mode,
            random_seed=random_seed,
            model=model,
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
            show_thinking=show_thinking,
        )

        if azure_endpoint and azure_api_key:
            self._client = MistralAzure(
                azure_endpoint=azure_endpoint,
                azure_api_key=azure_api_key,
            )
            self._models = mistral_azure_models
            self._uses_azure = True
        else:
            self._client = Mistral(
                api_key=api_key,
                server_url=endpoint,
            )

    @classmethod
    defclass_name(cls) -> str:
        return "MistralAI_LLM"

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=mistralai_modelname_to_contextsize(self.model),
            num_output=self.max_tokens,
            is_chat_model=True,
            model_name=self.model,
            random_seed=self.random_seed,
            is_function_calling_model=is_mistralai_function_calling_model(self.model),
        )

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "random_seed": self.random_seed,
            "retries": self.max_retries,
            "timeout_ms": self.timeout * 1000,
        }
        # azure sdk does not support random_seed, so we pop it out if using azure
        if self._uses_azure:
            base_kwargs.pop("random_seed", None)
        return {
            **base_kwargs,
            **self.additional_kwargs,
        }

    def_get_all_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        return {
            **self._model_kwargs,
            **kwargs,
        }

    def_separate_thinking(
        self, response: Union[str, List["ContentChunk"]]
    ) -> Tuple[str, str]:
"""Separate the thinking from the response."""
        content = ""
        if isinstance(response, str):
            content = response
        else:
            for chunk in response:
                if isinstance(chunk, self._models.ThinkChunk):
                    for c in chunk.thinking:
                        if isinstance(c, self._models.TextChunk):
                            content += c.text + "\n"

        match = THINKING_REGEX.search(content)
        if match:
            return match.group(1), content.replace(match.group(0), "")

        match = THINKING_START_REGEX.search(content)
        if match:
            return match.group(0), ""

        return "", content

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        # convert messages to mistral ChatMessage

        messages = to_mistral_chatmessage(messages, models=self._models)
        all_kwargs = self._get_all_kwargs(**kwargs)
        response = self._client.chat.complete(messages=messages, **all_kwargs)
        blocks: List[TextBlock | ThinkingBlock | ToolCallBlock] = []

        if self.model in MISTRAL_AI_REASONING_MODELS:
            thinking_txt, response_txt = self._separate_thinking(
                response.choices[0].message.content or []
            )
            if thinking_txt:
                blocks.append(ThinkingBlock(content=thinking_txt))

            response_txt_think_show = ""
            if response.choices[0].message.content:
                if isinstance(response.choices[0].message.content, str):
                    response_txt_think_show = response.choices[0].message.content
                else:
                    for chunk in response.choices[0].message.content:
                        if isinstance(chunk, self._models.TextChunk):
                            response_txt_think_show += chunk.text + "\n"
                        if isinstance(chunk, self._models.ThinkChunk):
                            for c in chunk.thinking:
                                if isinstance(c, self._models.TextChunk):
                                    response_txt_think_show += c.text + "\n"

            response_txt = (
                response_txt if not self.show_thinking else response_txt_think_show
            )
        else:
            response_txt = response.choices[0].message.content

        blocks.append(TextBlock(text=response_txt))
        tool_calls = response.choices[0].message.tool_calls
        if tool_calls is not None:
            for tool_call in tool_calls:
                if isinstance(tool_call, self._models.ToolCall):
                    blocks.append(
                        ToolCallBlock(
                            tool_call_id=tool_call.id,
                            tool_kwargs=tool_call.function.arguments,
                            tool_name=tool_call.function.name,
                        )
                    )

        return ChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT,
                blocks=blocks,
            ),
            raw=dict(response),
        )

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        complete_fn = chat_to_completion_decorator(self.chat)
        return complete_fn(prompt, **kwargs)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        # convert messages to mistral ChatMessage

        messages = to_mistral_chatmessage(messages, models=self._models)
        all_kwargs = self._get_all_kwargs(**kwargs)

        response = self._client.chat.stream(messages=messages, **all_kwargs)

        defgen() -> ChatResponseGen:
            content = ""
            blocks: List[TextBlock | ThinkingBlock | ToolCallBlock] = []
            for chunk in response:
                delta = chunk.data.choices[0].delta
                role = delta.role or MessageRole.ASSISTANT

                # NOTE: Unlike openAI, we are directly injecting the tool calls
                if delta.tool_calls:
                    for tool_call in delta.tool_calls:
                        if isinstance(tool_call, self._models.ToolCall):
                            blocks.append(
                                ToolCallBlock(
                                    tool_call_id=tool_call.id,
                                    tool_name=tool_call.function.name,
                                    tool_kwargs=tool_call.function.arguments,
                                )
                            )

                content_delta = delta.content or ""
                content_delta_str = ""
                if isinstance(content_delta, str):
                    content_delta_str = content_delta
                else:
                    for chunk in content_delta:
                        if isinstance(chunk, self._models.TextChunk):
                            content_delta_str += chunk.text + "\n"
                        elif isinstance(chunk, self._models.ThinkChunk):
                            for c in chunk.thinking:
                                if isinstance(c, self._models.TextChunk):
                                    content_delta_str += c.text + "\n"
                        else:
                            continue

                content += content_delta_str

                # decide whether to include thinking in deltas/responses
                if self.model in MISTRAL_AI_REASONING_MODELS:
                    thinking_txt, response_txt = self._separate_thinking(content)

                    if thinking_txt:
                        blocks.append(ThinkingBlock(content=thinking_txt))

                    content = response_txt if not self.show_thinking else content

                    # If thinking hasn't ended, don't include it in the delta
                    if thinking_txt is None and not self.show_thinking:
                        content_delta = ""
                blocks.append(TextBlock(text=content))

                yield ChatResponse(
                    message=ChatMessage(
                        role=role,
                        blocks=blocks,
                    ),
                    delta=content_delta_str,
                    raw=chunk,
                )

        return gen()

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        stream_complete_fn = stream_chat_to_completion_decorator(self.stream_chat)
        return stream_complete_fn(prompt, **kwargs)

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        # convert messages to mistral ChatMessage

        messages = to_mistral_chatmessage(messages, models=self._models)
        all_kwargs = self._get_all_kwargs(**kwargs)
        response = await self._client.chat.complete_async(
            messages=messages, **all_kwargs
        )

        blocks: List[TextBlock | ThinkingBlock | ToolCallBlock] = []
        additional_kwargs = {}
        if self.model in MISTRAL_AI_REASONING_MODELS:
            thinking_txt, response_txt = self._separate_thinking(
                response.choices[0].message.content or []
            )
            if thinking_txt:
                blocks.append(ThinkingBlock(content=thinking_txt))

            response_txt_think_show = ""
            if response.choices[0].message.content:
                if isinstance(response.choices[0].message.content, str):
                    response_txt_think_show = response.choices[0].message.content
                else:
                    for chunk in response.choices[0].message.content:
                        if isinstance(chunk, self._models.TextChunk):
                            response_txt_think_show += chunk.text + "\n"
                        if isinstance(chunk, self._models.ThinkChunk):
                            for c in chunk.thinking:
                                if isinstance(c, self._models.TextChunk):
                                    response_txt_think_show += c.text + "\n"

            response_txt = (
                response_txt if not self.show_thinking else response_txt_think_show
            )
        else:
            response_txt = response.choices[0].message.content

        blocks.append(TextBlock(text=response_txt))

        tool_calls = response.choices[0].message.tool_calls
        if tool_calls is not None:
            for tool_call in tool_calls:
                if isinstance(tool_call, self._models.ToolCall):
                    blocks.append(
                        ToolCallBlock(
                            tool_call_id=tool_call.id,
                            tool_kwargs=tool_call.function.arguments,
                            tool_name=tool_call.function.name,
                        )
                    )
                else:
                    if isinstance(tool_call[1], (str, dict)):
                        blocks.append(
                            ToolCallBlock(
                                tool_kwargs=tool_call[1], tool_name=tool_call[0]
                            )
                        )
            additional_kwargs["tool_calls"] = (
                tool_calls  # keep this to avoid tool calls loss if tool call does not fall within the validation scenarios above
            )

        return ChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT,
                blocks=blocks,
                additional_kwargs=additional_kwargs,
            ),
            raw=dict(response),
        )

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        acomplete_fn = achat_to_completion_decorator(self.achat)
        return await acomplete_fn(prompt, **kwargs)

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        # convert messages to mistral ChatMessage

        messages = to_mistral_chatmessage(messages, models=self._models)
        all_kwargs = self._get_all_kwargs(**kwargs)

        response = await self._client.chat.stream_async(messages=messages, **all_kwargs)

        async defgen() -> ChatResponseAsyncGen:
            content = ""
            blocks: List[ThinkingBlock | TextBlock | ToolCallBlock] = []
            async for chunk in response:
                delta = chunk.data.choices[0].delta
                role = delta.role or MessageRole.ASSISTANT
                # NOTE: Unlike openAI, we are directly injecting the tool calls
                if delta.tool_calls:
                    for tool_call in delta.tool_calls:
                        if isinstance(tool_call, self._models.ToolCall):
                            blocks.append(
                                ToolCallBlock(
                                    tool_call_id=tool_call.id,
                                    tool_name=tool_call.function.name,
                                    tool_kwargs=tool_call.function.arguments,
                                )
                            )

                content_delta = delta.content or ""
                content_delta_str = ""
                if isinstance(content_delta, str):
                    content_delta_str = content_delta
                else:
                    for chunk in content_delta:
                        if isinstance(chunk, self._models.TextChunk):
                            content_delta_str += chunk.text + "\n"
                        elif isinstance(chunk, self._models.ThinkChunk):
                            for c in chunk.thinking:
                                if isinstance(c, self._models.TextChunk):
                                    content_delta_str += c.text + "\n"
                        else:
                            continue

                content += content_delta_str

                # decide whether to include thinking in deltas/responses
                if self.model in MISTRAL_AI_REASONING_MODELS:
                    thinking_txt, response_txt = self._separate_thinking(content)
                    if thinking_txt:
                        blocks.append(ThinkingBlock(content=thinking_txt))

                    content = response_txt if not self.show_thinking else content

                    # If thinking hasn't ended, don't include it in the delta
                    if thinking_txt is None and not self.show_thinking:
                        content_delta = ""

                blocks.append(TextBlock(text=content))

                yield ChatResponse(
                    message=ChatMessage(
                        role=role,
                        blocks=blocks,
                    ),
                    delta=content_delta_str,
                    raw=chunk,
                )

        return gen()

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        astream_complete_fn = astream_chat_to_completion_decorator(self.astream_chat)
        return await astream_complete_fn(prompt, **kwargs)

    def_prepare_chat_with_tools(
        self,
        tools: List["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        tool_required: bool = False,
        **kwargs: Any,
    ) -> Dict[str, Any]:
"""Prepare the chat with tools."""
        # misralai uses the same openai tool format
        tool_specs = [
            tool.metadata.to_openai_tool(skip_length_check=True) for tool in tools
        ]

        if isinstance(user_msg, str):
            user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)

        messages = chat_history or []
        if user_msg:
            messages.append(user_msg)

        return {
            "messages": messages,
            "tools": tool_specs or None,
            "tool_choice": "required" if tool_required else "auto",
            **kwargs,
        }

    def_validate_chat_with_tools_response(
        self,
        response: ChatResponse,
        tools: List["BaseTool"],
        allow_parallel_tool_calls: bool = False,
        **kwargs: Any,
    ) -> ChatResponse:
"""Validate the response from chat_with_tools."""
        if not allow_parallel_tool_calls:
            force_single_tool_call(response)
        return response

    defget_tool_calls_from_response(
        self,
        response: "ChatResponse",
        error_on_no_tool_call: bool = True,
    ) -> List[ToolSelection]:
"""Predict and call the tool."""
        tool_calls = [
            block
            for block in response.message.blocks
            if isinstance(block, ToolCallBlock)
        ]

        if len(tool_calls)  1:
            if error_on_no_tool_call:
                raise ValueError(
                    f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
                )
            else:
                return []

        tool_selections = []
        for tool_call in tool_calls:
            if isinstance(tool_call.tool_kwargs, str):
                argument_dict = json.loads(tool_call.tool_kwargs)
            else:
                argument_dict = tool_call.tool_kwargs

            tool_selections.append(
                ToolSelection(
                    tool_id=tool_call.tool_call_id or "",
                    tool_name=tool_call.tool_name,
                    tool_kwargs=argument_dict,
                )
            )

        return tool_selections

    deffill_in_middle(
        self, prompt: str, suffix: str, stop: Optional[List[str]] = None
    ) -> CompletionResponse:
        if not is_mistralai_code_model(self.model):
            raise ValueError(
                "Please provide code model from MistralAI. Currently supported code model is 'codestral-latest'."
            )

        if stop:
            response = self._client.fim.complete(
                model=self.model, prompt=prompt, suffix=suffix, stop=stop
            )
        else:
            response = self._client.fim.complete(
                model=self.model, prompt=prompt, suffix=suffix
            )

        return CompletionResponse(
            text=response.choices[0].message.content, raw=dict(response)
        )

```
 |  
| --- | --- |  
###  get_tool_calls_from_response [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/mistralai/#llama_index.llms.mistralai.MistralAI.get_tool_calls_from_response "Permanent link")

```
get_tool_calls_from_response(
    response: ,
    error_on_no_tool_call:  = True,
) -> []

```

Predict and call the tool.
Source code in `llama-index-integrations/llms/llama-index-llms-mistralai/llama_index/llms/mistralai/base.py`  
| 
```
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
```
 | 
```
defget_tool_calls_from_response(
    self,
    response: "ChatResponse",
    error_on_no_tool_call: bool = True,
) -> List[ToolSelection]:
"""Predict and call the tool."""
    tool_calls = [
        block
        for block in response.message.blocks
        if isinstance(block, ToolCallBlock)
    ]

    if len(tool_calls)  1:
        if error_on_no_tool_call:
            raise ValueError(
                f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
            )
        else:
            return []

    tool_selections = []
    for tool_call in tool_calls:
        if isinstance(tool_call.tool_kwargs, str):
            argument_dict = json.loads(tool_call.tool_kwargs)
        else:
            argument_dict = tool_call.tool_kwargs

        tool_selections.append(
            ToolSelection(
                tool_id=tool_call.tool_call_id or "",
                tool_name=tool_call.tool_name,
                tool_kwargs=argument_dict,
            )
        )

    return tool_selections

```
 |  
| --- | --- |  
options: members: - MistralAI
