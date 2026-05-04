# Google genai
##  GoogleGenAI [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/google_genai/#llama_index.llms.google_genai.GoogleGenAI "Permanent link")
Bases: `FunctionCallingLLM`
Google GenAI LLM.
Examples:
`pip install llama-index-llms-google-genai`

```
fromllama_index.llms.google_genaiimport GoogleGenAI

llm = GoogleGenAI(model="gemini-3-flash-preview", api_key="YOUR_API_KEY")
resp = llm.complete("Write a poem about a magic backpack")
print(resp)

```

Source code in `llama-index-integrations/llms/llama-index-llms-google-genai/llama_index/llms/google_genai/base.py`  
| 
```
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
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
870
871
```
 | 
```
classGoogleGenAI(FunctionCallingLLM):
"""
    Google GenAI LLM.

    Examples:
        `pip install llama-index-llms-google-genai`

        ```python
        from llama_index.llms.google_genai import GoogleGenAI

        llm = GoogleGenAI(model="gemini-3-flash-preview", api_key="YOUR_API_KEY")
        resp = llm.complete("Write a poem about a magic backpack")
        print(resp)
        ```

    """

    model: str = Field(default=DEFAULT_MODEL, description="The Gemini model to use.")
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        description="The temperature to use during generation.",
        ge=0.0,
        le=2.0,
    )
    context_window: Optional[int] = Field(
        default=None,
        description="The context window of the model. If not provided, the default context window 200000 will be used.",
    )
    max_retries: int = Field(
        default=3,
        description="The maximum number of API retries.",
        ge=0,
    )
    is_function_calling_model: bool = Field(
        default=True, description="Whether the model is a function calling model."
    )
    cached_content: Optional[str] = Field(
        default=None,
        description="Cached content to use for the model.",
    )
    built_in_tool: Optional[types.Tool] = Field(
        default=None,
        description="Google GenAI tool to use for the model to augment responses.",
    )
    file_mode: Literal["inline", "fileapi", "hybrid"] = Field(
        default="hybrid",
        description="Whether to use inline-only, FileAPI-only or both for handling files.",
    )

    _max_tokens: int = PrivateAttr()
    _client: google.genai.Client = PrivateAttr()
    _generation_config: types.GenerateContentConfigDict = PrivateAttr()
    _model_meta: types.Model = PrivateAttr()

    def__init__(
        self,
        model: str = DEFAULT_MODEL,
        api_key: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        context_window: Optional[int] = None,
        max_retries: int = 3,
        vertexai_config: Optional[VertexAIConfig] = None,
        http_options: Optional[types.HttpOptions] = None,
        debug_config: Optional[google.genai.client.DebugConfig] = None,
        generation_config: Optional[types.GenerateContentConfig] = None,
        callback_manager: Optional[CallbackManager] = None,
        is_function_calling_model: bool = True,
        cached_content: Optional[str] = None,
        built_in_tool: Optional[types.Tool] = None,
        file_mode: Literal["inline", "fileapi", "hybrid"] = "hybrid",
        **kwargs: Any,
    ):
        if temperature is None:
            if "gemini-3" in model:
                temperature = 1.0
            else:
                temperature = DEFAULT_TEMPERATURE
        # API keys are optional. The API can be authorised via OAuth (detected
        # environmentally) or by the GOOGLE_API_KEY environment variable.
        api_key = api_key or os.getenv("GOOGLE_API_KEY", None)
        vertexai = (
            vertexai_config is not None
            or os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "false") != "false"
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
            package_v = version("llama-index-llms-google-genai")
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

        client = google.genai.Client(**config_params)

        # only get model meta data if max_tokens or context_window is not specified
        if max_tokens is None or context_window is None:
            model_meta = client.models.get(model=model)
        else:
            model_meta = None

        super().__init__(
            model=model,
            temperature=temperature,
            context_window=context_window,
            callback_manager=callback_manager,
            is_function_calling_model=is_function_calling_model,
            max_retries=max_retries,
            cached_content=cached_content,
            built_in_tool=built_in_tool,
            file_mode=file_mode,
            **kwargs,
        )

        self.model = model
        self._client = client
        self._model_meta = model_meta
        # store this as a dict and not as a pydantic model so we can more easily
        # merge it later
        if generation_config:
            self._generation_config = generation_config.model_dump()
            if cached_content:
                self._generation_config.setdefault("cached_content", cached_content)
            if built_in_tool is not None:
                if self._generation_config.get("tools") is None:
                    self._generation_config["tools"] = []
                if isinstance(self._generation_config["tools"], list):
                    if len(self._generation_config["tools"])  0:
                        raise ValueError(
                            "Providing multiple Google GenAI tools or mixing with custom tools is not supported."
                        )
                self._generation_config["tools"].append(built_in_tool)
        else:
            config_kwargs = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
                "cached_content": cached_content,
            }
            if built_in_tool:
                config_kwargs["tools"] = [built_in_tool]

            self._generation_config = types.GenerateContentConfig(
                **config_kwargs
            ).model_dump()
        self._max_tokens = (
            max_tokens or model_meta.output_token_limit or DEFAULT_NUM_OUTPUTS
        )

    @classmethod
    defclass_name(cls) -> str:
        return "GenAI"

    @property
    defmetadata(self) -> LLMMetadata:
        if self.context_window is None:
            base = self._model_meta.input_token_limit or 200000
            total_tokens = base + self._max_tokens
        else:
            total_tokens = self.context_window

        return LLMMetadata(
            context_window=total_tokens,
            num_output=self._max_tokens,
            model_name=self.model,
            is_chat_model=True,
            is_function_calling_model=self.is_function_calling_model,
        )

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        chat_fn = chat_to_completion_decorator(self._chat)
        return chat_fn(prompt, **kwargs)

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        chat_fn = achat_to_completion_decorator(self._achat)
        return await chat_fn(prompt, **kwargs)

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        chat_fn = stream_chat_to_completion_decorator(self._stream_chat)
        return chat_fn(prompt, **kwargs)

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        chat_fn = astream_chat_to_completion_decorator(self.astream_chat)
        return await chat_fn(prompt, **kwargs)

    @llm_retry_decorator
    def_chat(self, messages: Sequence[ChatMessage], **kwargs: Any):
        generation_config = {
            **(self._generation_config or {}),
            **kwargs.pop("generation_config", {}),
        }
        params = {**kwargs, "generation_config": generation_config}
        next_msg, chat_kwargs, file_api_names = asyncio.run(
            prepare_chat_params(
                self.model, messages, self.file_mode, self._client, **params
            )
        )
        chat = self._client.chats.create(**chat_kwargs)
        try:
            response = chat.send_message(
                next_msg.parts if isinstance(next_msg, types.Content) else next_msg
            )
        finally:
            if self.file_mode in ("fileapi", "hybrid"):
                delete_uploaded_files(file_api_names, self._client)

        return chat_from_gemini_response(response, [])

    @llm_retry_decorator
    async def_achat(self, messages: Sequence[ChatMessage], **kwargs: Any):
        generation_config = {
            **(self._generation_config or {}),
            **kwargs.pop("generation_config", {}),
        }
        params = {**kwargs, "generation_config": generation_config}
        next_msg, chat_kwargs, file_api_names = await prepare_chat_params(
            self.model, messages, self.file_mode, self._client, **params
        )
        chat = self._client.aio.chats.create(**chat_kwargs)
        try:
            response = await chat.send_message(
                next_msg.parts if isinstance(next_msg, types.Content) else next_msg
            )
        finally:
            if self.file_mode in ("fileapi", "hybrid"):
                await adelete_uploaded_files(file_api_names, self._client)

        return chat_from_gemini_response(response, [])

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        return self._chat(messages, **kwargs)

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        return await self._achat(messages, **kwargs)

    def_stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        generation_config = {
            **(self._generation_config or {}),
            **kwargs.pop("generation_config", {}),
        }
        params = {**kwargs, "generation_config": generation_config}
        next_msg, chat_kwargs, file_api_names = asyncio.run(
            prepare_chat_params(
                self.model, messages, self.file_mode, self._client, **params
            )
        )
        chat = self._client.chats.create(**chat_kwargs)
        response = chat.send_message_stream(
            next_msg.parts if isinstance(next_msg, types.Content) else next_msg
        )

        defgen() -> ChatResponseGen:
            try:
                content = []
                thought_signatures = []
                for r in response:
                    if candidates := r.candidates:
                        if not candidates:
                            continue

                        top_candidate = candidates[0]
                        if response_content := top_candidate.content:
                            if parts := response_content.parts:
                                content_delta = parts[0].text

                                llama_resp = chat_from_gemini_response(
                                    r,
                                    existing_content=content,
                                    thought_signatures=thought_signatures,
                                )
                                llama_resp.delta = (
                                    llama_resp.delta or content_delta or ""
                                )

                                yield llama_resp
            finally:
                if self.file_mode in ("fileapi", "hybrid"):
                    delete_uploaded_files(file_api_names, self._client)

        return gen()

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        return self._stream_chat(messages, **kwargs)

    async def_astream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        generation_config = {
            **(self._generation_config or {}),
            **kwargs.pop("generation_config", {}),
        }
        params = {**kwargs, "generation_config": generation_config}
        next_msg, chat_kwargs, file_api_names = await prepare_chat_params(
            self.model, messages, self.file_mode, self._client, **params
        )
        chat = self._client.aio.chats.create(**chat_kwargs)

        async defgen() -> ChatResponseAsyncGen:
            try:
                content = []
                thought_signatures = []
                async for r in await chat.send_message_stream(
                    next_msg.parts if isinstance(next_msg, types.Content) else next_msg
                ):
                    if candidates := r.candidates:
                        if not candidates:
                            continue

                        top_candidate = candidates[0]
                        if response_content := top_candidate.content:
                            if parts := response_content.parts:
                                content_delta = parts[0].text

                                llama_resp = chat_from_gemini_response(
                                    r,
                                    existing_content=content,
                                    thought_signatures=thought_signatures,
                                )
                                llama_resp.delta = (
                                    llama_resp.delta or content_delta or ""
                                )

                                yield llama_resp
            finally:
                if self.file_mode in ("fileapi", "hybrid"):
                    await adelete_uploaded_files(file_api_names, self._client)

        return gen()

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        return await self._astream_chat(messages, **kwargs)

    def_prepare_chat_with_tools(
        self,
        tools: Sequence["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        tool_required: bool = False,
        tool_choice: Optional[Union[str, dict]] = None,
        strict: Optional[bool] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
"""Predict and call the tool."""
        if tool_choice is None:
            tool_choice = "any" if tool_required else "auto"

        if tool_choice == "auto":
            tool_mode = types.FunctionCallingConfigMode.AUTO
        elif tool_choice == "none":
            tool_mode = types.FunctionCallingConfigMode.NONE
        else:
            tool_mode = types.FunctionCallingConfigMode.ANY

        function_calling_config = types.FunctionCallingConfig(mode=tool_mode)

        if tool_choice not in ["auto", "none"]:
            if isinstance(tool_choice, dict):
                raise ValueError("Gemini does not support tool_choice as a dict")

            # assume that the user wants a tool call to be made
            # if the tool choice is not in the list of tools, then we will make a tool call to all tools
            # otherwise, we will make a tool call to the tool choice
            tool_names = [tool.metadata.name for tool in tools if tool.metadata.name]
            if tool_choice not in tool_names:
                function_calling_config.allowed_function_names = tool_names
            else:
                function_calling_config.allowed_function_names = [tool_choice]

        tool_config = types.ToolConfig(
            function_calling_config=function_calling_config,
        )

        tool_declarations = []
        for tool in tools:
            if tool.metadata.fn_schema:
                function_declaration = convert_schema_to_function_declaration(
                    self._client, tool
                )
                tool_declarations.append(function_declaration)

        if isinstance(user_msg, str):
            user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)

        messages = chat_history or []
        if user_msg:
            messages.append(user_msg)

        return {
            "messages": messages,
            "tools": (
                [types.Tool(function_declarations=tool_declarations)]
                if tool_declarations
                else None
            ),
            "tool_config": tool_config,
            **kwargs,
        }

    defget_tool_calls_from_response(
        self,
        response: ChatResponse,
        error_on_no_tool_call: bool = True,
        **kwargs: Any,
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
            tool_selections.append(
                ToolSelection(
                    tool_id=tool_call.tool_name,
                    tool_name=tool_call.tool_name,
                    tool_kwargs=cast(Dict[str, Any], tool_call.tool_kwargs),
                )
            )

        return tool_selections

    @dispatcher.span
    defstructured_predict_without_function_calling(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Model:
"""Structured predict."""
        llm_kwargs = llm_kwargs or {}

        messages = prompt.format_messages(**prompt_args)
        contents_and_names = [
            asyncio.run(chat_message_to_gemini(message, self.file_mode, self._client))
            for message in messages
        ]
        contents = [it[0] for it in contents_and_names]
        file_api_names = [name for it in contents_and_names for name in it[1]]

        response = self._client.models.generate_content(
            model=self.model,
            contents=contents,
            **{
                **llm_kwargs,
                **{
                    "config": {
                        "response_mime_type": "application/json",
                        "response_schema": output_cls,
                    }
                },
            },
        )

        if self.file_mode in ("fileapi", "hybrid"):
            delete_uploaded_files(file_api_names, self._client)

        if isinstance(response.parsed, BaseModel):
            return response.parsed
        else:
            raise ValueError("Response is not a BaseModel")

    @dispatcher.span
    defstructured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Model:
"""Structured predict."""
        llm_kwargs = llm_kwargs or {}

        if self.pydantic_program_mode == PydanticProgramMode.DEFAULT:
            generation_config = {
                **(self._generation_config or {}),
                **llm_kwargs.pop("generation_config", {}),
            }

            # set the specific types needed for the response
            generation_config["response_mime_type"] = "application/json"
            generation_config["response_schema"] = output_cls

            messages = prompt.format_messages(**prompt_args)
            contents_and_names = [
                asyncio.run(
                    chat_message_to_gemini(message, self.file_mode, self._client)
                )
                for message in messages
            ]
            contents = [it[0] for it in contents_and_names]
            file_api_names = [name for it in contents_and_names for name in it[1]]

            response = self._client.models.generate_content(
                model=self.model,
                contents=contents,
                config=generation_config,
            )

            if self.file_mode in ("fileapi", "hybrid"):
                delete_uploaded_files(file_api_names, self._client)

            if isinstance(response.parsed, BaseModel):
                return response.parsed
            else:
                # Try to parse the response text as JSON into the output_cls
                return output_cls.model_validate_json(response.text)

        else:
            return super().structured_predict(
                output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
            )

    @dispatcher.span
    async defastructured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Model:
"""Structured predict."""
        llm_kwargs = llm_kwargs or {}

        if self.pydantic_program_mode == PydanticProgramMode.DEFAULT:
            generation_config = {
                **(self._generation_config or {}),
                **llm_kwargs.pop("generation_config", {}),
            }

            # set the specific types needed for the response
            generation_config["response_mime_type"] = "application/json"
            generation_config["response_schema"] = output_cls

            messages = prompt.format_messages(**prompt_args)
            contents_and_names = await asyncio.gather(
                *[
                    chat_message_to_gemini(message, self.file_mode, self._client)
                    for message in messages
                ]
            )
            contents = [it[0] for it in contents_and_names]
            file_api_names = [name for it in contents_and_names for name in it[1]]

            response = await self._client.aio.models.generate_content(
                model=self.model,
                contents=contents,
                config=generation_config,
            )

            if self.file_mode in ("fileapi", "hybrid"):
                await adelete_uploaded_files(file_api_names, self._client)

            if isinstance(response.parsed, BaseModel):
                return response.parsed
            else:
                # Try to parse the response text as JSON into the output_cls
                return output_cls.model_validate_json(response.text)

        else:
            return super().structured_predict(
                output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
            )

    @dispatcher.span
    defstream_structured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Generator[Union[Model, FlexibleModel], None, None]:
"""Stream structured predict."""
        llm_kwargs = llm_kwargs or {}

        if self.pydantic_program_mode == PydanticProgramMode.DEFAULT:
            generation_config = {
                **(self._generation_config or {}),
                **llm_kwargs.pop("generation_config", {}),
            }

            # set the specific types needed for the response
            generation_config["response_mime_type"] = "application/json"
            generation_config["response_schema"] = output_cls

            messages = prompt.format_messages(**prompt_args)
            contents_and_names = [
                asyncio.run(
                    chat_message_to_gemini(message, self.file_mode, self._client)
                )
                for message in messages
            ]
            contents = [it[0] for it in contents_and_names]
            file_api_names = [name for it in contents_and_names for name in it[1]]

            defgen() -> Generator[Union[Model, FlexibleModel], None, None]:
                flexible_model = create_flexible_model(output_cls)
                response_gen = self._client.models.generate_content_stream(
                    model=self.model,
                    contents=contents,
                    config=generation_config,
                )

                current_json = ""
                for chunk in response_gen:
                    if chunk.parsed:
                        yield chunk.parsed
                    elif chunk.candidates:
                        streaming_model, current_json = handle_streaming_flexible_model(
                            current_json,
                            chunk.candidates[0],
                            output_cls,
                            flexible_model,
                        )
                        if streaming_model:
                            yield streaming_model

                if self.file_mode in ("fileapi", "hybrid"):
                    delete_uploaded_files(file_api_names, self._client)

            return gen()
        else:
            return super().stream_structured_predict(
                output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
            )

    @dispatcher.span
    async defastream_structured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> AsyncGenerator[Union[Model, FlexibleModel], None]:
"""Stream structured predict."""
        llm_kwargs = llm_kwargs or {}

        if self.pydantic_program_mode == PydanticProgramMode.DEFAULT:
            generation_config = {
                **(self._generation_config or {}),
                **llm_kwargs.pop("generation_config", {}),
            }

            # set the specific types needed for the response
            generation_config["response_mime_type"] = "application/json"
            generation_config["response_schema"] = output_cls

            messages = prompt.format_messages(**prompt_args)
            contents_and_names = await asyncio.gather(
                *[
                    chat_message_to_gemini(message, self.file_mode, self._client)
                    for message in messages
                ]
            )
            contents = [it[0] for it in contents_and_names]
            file_api_names = [name for it in contents_and_names for name in it[1]]

            async defgen() -> AsyncGenerator[Union[Model, FlexibleModel], None]:
                flexible_model = create_flexible_model(output_cls)
                response_gen = await self._client.aio.models.generate_content_stream(
                    model=self.model,
                    contents=contents,
                    config=generation_config,
                )

                current_json = ""
                async for chunk in response_gen:
                    if chunk.parsed:
                        yield chunk.parsed
                    elif chunk.candidates:
                        streaming_model, current_json = handle_streaming_flexible_model(
                            current_json,
                            chunk.candidates[0],
                            output_cls,
                            flexible_model,
                        )
                        if streaming_model:
                            yield streaming_model

                if self.file_mode in ("fileapi", "hybrid"):
                    await adelete_uploaded_files(file_api_names, self._client)

            return gen()
        else:
            return await super().astream_structured_predict(
                output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
            )

```
 |  
| --- | --- |  
###  get_tool_calls_from_response [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/google_genai/#llama_index.llms.google_genai.GoogleGenAI.get_tool_calls_from_response "Permanent link")

```
get_tool_calls_from_response(
    response: ,
    error_on_no_tool_call:  = True,
    **kwargs: 
) -> []

```

Predict and call the tool.
Source code in `llama-index-integrations/llms/llama-index-llms-google-genai/llama_index/llms/google_genai/base.py`  
| 
```
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
```
 | 
```
defget_tool_calls_from_response(
    self,
    response: ChatResponse,
    error_on_no_tool_call: bool = True,
    **kwargs: Any,
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
        tool_selections.append(
            ToolSelection(
                tool_id=tool_call.tool_name,
                tool_name=tool_call.tool_name,
                tool_kwargs=cast(Dict[str, Any], tool_call.tool_kwargs),
            )
        )

    return tool_selections

```
 |  
| --- | --- |  
###  structured_predict_without_function_calling [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/google_genai/#llama_index.llms.google_genai.GoogleGenAI.structured_predict_without_function_calling "Permanent link")

```
structured_predict_without_function_calling(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> 

```

Structured predict.
Source code in `llama-index-integrations/llms/llama-index-llms-google-genai/llama_index/llms/google_genai/base.py`  
| 
```
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
```
 | 
```
@dispatcher.span
defstructured_predict_without_function_calling(
    self,
    output_cls: Type[Model],
    prompt: PromptTemplate,
    llm_kwargs: Optional[Dict[str, Any]] = None,
    **prompt_args: Any,
) -> Model:
"""Structured predict."""
    llm_kwargs = llm_kwargs or {}

    messages = prompt.format_messages(**prompt_args)
    contents_and_names = [
        asyncio.run(chat_message_to_gemini(message, self.file_mode, self._client))
        for message in messages
    ]
    contents = [it[0] for it in contents_and_names]
    file_api_names = [name for it in contents_and_names for name in it[1]]

    response = self._client.models.generate_content(
        model=self.model,
        contents=contents,
        **{
            **llm_kwargs,
            **{
                "config": {
                    "response_mime_type": "application/json",
                    "response_schema": output_cls,
                }
            },
        },
    )

    if self.file_mode in ("fileapi", "hybrid"):
        delete_uploaded_files(file_api_names, self._client)

    if isinstance(response.parsed, BaseModel):
        return response.parsed
    else:
        raise ValueError("Response is not a BaseModel")

```
 |  
| --- | --- |  
###  structured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/google_genai/#llama_index.llms.google_genai.GoogleGenAI.structured_predict "Permanent link")

```
structured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> 

```

Structured predict.
Source code in `llama-index-integrations/llms/llama-index-llms-google-genai/llama_index/llms/google_genai/base.py`  
| 
```
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
```
 | 
```
@dispatcher.span
defstructured_predict(
    self,
    output_cls: Type[Model],
    prompt: PromptTemplate,
    llm_kwargs: Optional[Dict[str, Any]] = None,
    **prompt_args: Any,
) -> Model:
"""Structured predict."""
    llm_kwargs = llm_kwargs or {}

    if self.pydantic_program_mode == PydanticProgramMode.DEFAULT:
        generation_config = {
            **(self._generation_config or {}),
            **llm_kwargs.pop("generation_config", {}),
        }

        # set the specific types needed for the response
        generation_config["response_mime_type"] = "application/json"
        generation_config["response_schema"] = output_cls

        messages = prompt.format_messages(**prompt_args)
        contents_and_names = [
            asyncio.run(
                chat_message_to_gemini(message, self.file_mode, self._client)
            )
            for message in messages
        ]
        contents = [it[0] for it in contents_and_names]
        file_api_names = [name for it in contents_and_names for name in it[1]]

        response = self._client.models.generate_content(
            model=self.model,
            contents=contents,
            config=generation_config,
        )

        if self.file_mode in ("fileapi", "hybrid"):
            delete_uploaded_files(file_api_names, self._client)

        if isinstance(response.parsed, BaseModel):
            return response.parsed
        else:
            # Try to parse the response text as JSON into the output_cls
            return output_cls.model_validate_json(response.text)

    else:
        return super().structured_predict(
            output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
        )

```
 |  
| --- | --- |  
###  astructured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/google_genai/#llama_index.llms.google_genai.GoogleGenAI.astructured_predict "Permanent link")

```
astructured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> 

```

Structured predict.
Source code in `llama-index-integrations/llms/llama-index-llms-google-genai/llama_index/llms/google_genai/base.py`  
| 
```
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
```
 | 
```
@dispatcher.span
async defastructured_predict(
    self,
    output_cls: Type[Model],
    prompt: PromptTemplate,
    llm_kwargs: Optional[Dict[str, Any]] = None,
    **prompt_args: Any,
) -> Model:
"""Structured predict."""
    llm_kwargs = llm_kwargs or {}

    if self.pydantic_program_mode == PydanticProgramMode.DEFAULT:
        generation_config = {
            **(self._generation_config or {}),
            **llm_kwargs.pop("generation_config", {}),
        }

        # set the specific types needed for the response
        generation_config["response_mime_type"] = "application/json"
        generation_config["response_schema"] = output_cls

        messages = prompt.format_messages(**prompt_args)
        contents_and_names = await asyncio.gather(
            *[
                chat_message_to_gemini(message, self.file_mode, self._client)
                for message in messages
            ]
        )
        contents = [it[0] for it in contents_and_names]
        file_api_names = [name for it in contents_and_names for name in it[1]]

        response = await self._client.aio.models.generate_content(
            model=self.model,
            contents=contents,
            config=generation_config,
        )

        if self.file_mode in ("fileapi", "hybrid"):
            await adelete_uploaded_files(file_api_names, self._client)

        if isinstance(response.parsed, BaseModel):
            return response.parsed
        else:
            # Try to parse the response text as JSON into the output_cls
            return output_cls.model_validate_json(response.text)

    else:
        return super().structured_predict(
            output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
        )

```
 |  
| --- | --- |  
###  stream_structured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/google_genai/#llama_index.llms.google_genai.GoogleGenAI.stream_structured_predict "Permanent link")

```
stream_structured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> Generator[Union[, FlexibleModel], None, None]

```

Stream structured predict.
Source code in `llama-index-integrations/llms/llama-index-llms-google-genai/llama_index/llms/google_genai/base.py`  
| 
```
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
800
801
802
803
804
805
806
807
808
809
```
 | 
```
@dispatcher.span
defstream_structured_predict(
    self,
    output_cls: Type[Model],
    prompt: PromptTemplate,
    llm_kwargs: Optional[Dict[str, Any]] = None,
    **prompt_args: Any,
) -> Generator[Union[Model, FlexibleModel], None, None]:
"""Stream structured predict."""
    llm_kwargs = llm_kwargs or {}

    if self.pydantic_program_mode == PydanticProgramMode.DEFAULT:
        generation_config = {
            **(self._generation_config or {}),
            **llm_kwargs.pop("generation_config", {}),
        }

        # set the specific types needed for the response
        generation_config["response_mime_type"] = "application/json"
        generation_config["response_schema"] = output_cls

        messages = prompt.format_messages(**prompt_args)
        contents_and_names = [
            asyncio.run(
                chat_message_to_gemini(message, self.file_mode, self._client)
            )
            for message in messages
        ]
        contents = [it[0] for it in contents_and_names]
        file_api_names = [name for it in contents_and_names for name in it[1]]

        defgen() -> Generator[Union[Model, FlexibleModel], None, None]:
            flexible_model = create_flexible_model(output_cls)
            response_gen = self._client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=generation_config,
            )

            current_json = ""
            for chunk in response_gen:
                if chunk.parsed:
                    yield chunk.parsed
                elif chunk.candidates:
                    streaming_model, current_json = handle_streaming_flexible_model(
                        current_json,
                        chunk.candidates[0],
                        output_cls,
                        flexible_model,
                    )
                    if streaming_model:
                        yield streaming_model

            if self.file_mode in ("fileapi", "hybrid"):
                delete_uploaded_files(file_api_names, self._client)

        return gen()
    else:
        return super().stream_structured_predict(
            output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
        )

```
 |  
| --- | --- |  
###  astream_structured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/google_genai/#llama_index.llms.google_genai.GoogleGenAI.astream_structured_predict "Permanent link")

```
astream_structured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> AsyncGenerator[Union[, FlexibleModel], None]

```

Stream structured predict.
Source code in `llama-index-integrations/llms/llama-index-llms-google-genai/llama_index/llms/google_genai/base.py`  
| 
```
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
870
871
```
 | 
```
@dispatcher.span
async defastream_structured_predict(
    self,
    output_cls: Type[Model],
    prompt: PromptTemplate,
    llm_kwargs: Optional[Dict[str, Any]] = None,
    **prompt_args: Any,
) -> AsyncGenerator[Union[Model, FlexibleModel], None]:
"""Stream structured predict."""
    llm_kwargs = llm_kwargs or {}

    if self.pydantic_program_mode == PydanticProgramMode.DEFAULT:
        generation_config = {
            **(self._generation_config or {}),
            **llm_kwargs.pop("generation_config", {}),
        }

        # set the specific types needed for the response
        generation_config["response_mime_type"] = "application/json"
        generation_config["response_schema"] = output_cls

        messages = prompt.format_messages(**prompt_args)
        contents_and_names = await asyncio.gather(
            *[
                chat_message_to_gemini(message, self.file_mode, self._client)
                for message in messages
            ]
        )
        contents = [it[0] for it in contents_and_names]
        file_api_names = [name for it in contents_and_names for name in it[1]]

        async defgen() -> AsyncGenerator[Union[Model, FlexibleModel], None]:
            flexible_model = create_flexible_model(output_cls)
            response_gen = await self._client.aio.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=generation_config,
            )

            current_json = ""
            async for chunk in response_gen:
                if chunk.parsed:
                    yield chunk.parsed
                elif chunk.candidates:
                    streaming_model, current_json = handle_streaming_flexible_model(
                        current_json,
                        chunk.candidates[0],
                        output_cls,
                        flexible_model,
                    )
                    if streaming_model:
                        yield streaming_model

            if self.file_mode in ("fileapi", "hybrid"):
                await adelete_uploaded_files(file_api_names, self._client)

        return gen()
    else:
        return await super().astream_structured_predict(
            output_cls, prompt, llm_kwargs=llm_kwargs, **prompt_args
        )

```
 |  
| --- | --- |  
options: members: - Gemini
