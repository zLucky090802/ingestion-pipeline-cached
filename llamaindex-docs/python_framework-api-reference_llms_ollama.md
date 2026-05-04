# Ollama
##  Ollama [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/ollama/#llama_index.llms.ollama.Ollama "Permanent link")
Bases: `FunctionCallingLLM`
Ollama LLM.
Visit https://ollama.com/ to download and install Ollama.
Run `ollama serve` to start a server.
Run `ollama pull <name>` to download a model to run.
Examples:
`pip install llama-index-llms-ollama`

```
fromllama_index.llms.ollamaimport Ollama

llm = Ollama(model="llama2", request_timeout=60.0)

response = llm.complete("What is the capital of France?")
print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-ollama/llama_index/llms/ollama/base.py`  
| 
```
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
```
 | 
```
classOllama(FunctionCallingLLM):
"""
    Ollama LLM.

    Visit https://ollama.com/ to download and install Ollama.

    Run `ollama serve` to start a server.

    Run `ollama pull <name>` to download a model to run.

    Examples:
        `pip install llama-index-llms-ollama`

        ```python
        from llama_index.llms.ollama import Ollama

        llm = Ollama(model="llama2", request_timeout=60.0)

        response = llm.complete("What is the capital of France?")
        print(response)
        ```

    """

    base_url: str = Field(
        default="http://localhost:11434",
        description="Base url the model is hosted under.",
    )
    model: str = Field(description="The Ollama model to use.")
    temperature: Optional[float] = Field(
        default=None,
        description="The temperature to use for sampling.",
    )
    context_window: int = Field(
        default=-1,
        description="The maximum number of context tokens for the model.",
    )
    request_timeout: float = Field(
        default=DEFAULT_REQUEST_TIMEOUT,
        description="The timeout for making http request to Ollama API server",
    )
    prompt_key: str = Field(
        default="prompt", description="The key to use for the prompt in API calls."
    )
    json_mode: bool = Field(
        default=False,
        description="Whether to use JSON mode for the Ollama API.",
    )
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional model parameters for the Ollama API.",
    )
    is_function_calling_model: bool = Field(
        default=True,
        description="Whether the model is a function calling model.",
    )
    keep_alive: Optional[Union[float, str]] = Field(
        default="5m",
        description="controls how long the model will stay loaded into memory following the request(default: 5m)",
    )
    thinking: Optional[Union[bool, Literal["low", "medium", "high"]]] = Field(
        default=None,
        description="Whether to enable or disable thinking in the model. For some models, like gpt-oss, allow 'low', 'medium', or 'high' to tune the trace length.",
    )
    headers: Optional[Dict[str, str]] = Field(
        default=None,
        description="Custom HTTP headers for Ollama API requests (e.g. Authorization).",
    )

    _client: Optional[Client] = PrivateAttr()
    _async_client: Optional[AsyncClient] = PrivateAttr()

    def__init__(
        self,
        model: str,
        base_url: str = "http://localhost:11434",
        temperature: Optional[float] = None,
        context_window: int = -1,
        request_timeout: Optional[float] = DEFAULT_REQUEST_TIMEOUT,
        prompt_key: str = "prompt",
        json_mode: bool = False,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        client: Optional[Client] = None,
        async_client: Optional[AsyncClient] = None,
        is_function_calling_model: bool = True,
        keep_alive: Optional[Union[float, str]] = None,
        thinking: Optional[Union[bool, Literal["low", "medium", "high"]]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            model=model,
            base_url=base_url,
            temperature=temperature,
            context_window=context_window,
            request_timeout=request_timeout,
            prompt_key=prompt_key,
            json_mode=json_mode,
            additional_kwargs=additional_kwargs or {},
            is_function_calling_model=is_function_calling_model,
            keep_alive=keep_alive,
            thinking=thinking,
            headers=headers,
            **kwargs,
        )

        self._client = client
        self._async_client = async_client

    @classmethod
    defclass_name(cls) -> str:
        return "Ollama_llm"

    @property
    defmetadata(self) -> LLMMetadata:
"""LLM metadata."""
        return LLMMetadata(
            context_window=self.get_context_window(),
            num_output=DEFAULT_NUM_OUTPUTS,
            model_name=self.model,
            is_chat_model=True,  # Ollama supports chat API for all models
            # TODO: Detect if selected model is a function calling model?
            is_function_calling_model=self.is_function_calling_model,
        )

    @property
    defclient(self) -> Client:
        if self._client is None:
            self._client = Client(
                host=self.base_url,
                timeout=self.request_timeout,
                headers=self.headers or {},
            )
        return self._client

    @property
    defasync_client(self) -> AsyncClient:
        if self._async_client is None:
            self._async_client = AsyncClient(
                host=self.base_url,
                timeout=self.request_timeout,
                headers=self.headers or {},
            )
        return self._async_client

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "temperature": self.temperature,
            "num_ctx": self.get_context_window(),
        }
        return {
            **base_kwargs,
            **self.additional_kwargs,
        }

    defget_context_window(self) -> int:
        if self.context_window == -1:
            # Try to get the context window from the model info if not set
            info = self.client.show(self.model).modelinfo
            for key, value in info.items():
                if "context_length" in key:
                    self.context_window = int(value)
                    break

        # If the context window is still -1, use the default context window
        return (
            self.context_window if self.context_window != -1 else DEFAULT_CONTEXT_WINDOW
        )

    def_convert_to_ollama_messages(self, messages: Sequence[ChatMessage]) -> Dict:
        ollama_messages = []
        unique_tool_calls = []
        for message in messages:
            cur_ollama_message = {
                "role": message.role.value,
                "content": "",
            }
            for block in message.blocks:
                if isinstance(block, TextBlock):
                    cur_ollama_message["content"] += block.text
                elif isinstance(block, ImageBlock):
                    if "images" not in cur_ollama_message:
                        cur_ollama_message["images"] = []
                    cur_ollama_message["images"].append(
                        block.resolve_image(as_base64=True).read().decode("utf-8")
                    )
                elif isinstance(block, ThinkingBlock):
                    if block.content:
                        cur_ollama_message["thinking"] = block.content
                elif isinstance(block, ToolCallBlock):
                    if "tool_calls" not in cur_ollama_message:
                        cur_ollama_message["tool_calls"] = [
                            {
                                "function": {
                                    "name": block.tool_name,
                                    "arguments": block.tool_kwargs,
                                }
                            }
                        ]
                    else:
                        cur_ollama_message["tool_calls"].extend(
                            [
                                {
                                    "function": {
                                        "name": block.tool_name,
                                        "arguments": block.tool_kwargs,
                                    }
                                }
                            ]
                        )
                    unique_tool_calls.append((block.tool_name, str(block.tool_kwargs)))
                else:
                    raise ValueError(f"Unsupported block type: {type(block)}")

            # keep this code for compatibility with older chat histories
            if "tool_calls" in message.additional_kwargs:
                if (
                    "tool_calls" not in cur_ollama_message
                    or cur_ollama_message["tool_calls"] == []
                ):
                    cur_ollama_message["tool_calls"] = message.additional_kwargs[
                        "tool_calls"
                    ]
                else:
                    for tool_call in message.additional_kwargs["tool_calls"]:
                        if (
                            tool_call.get("name", ""),
                            str(tool_call.get("arguments", {})),
                        ) not in unique_tool_calls:
                            cur_ollama_message["tool_calls"].append(tool_call)

            ollama_messages.append(cur_ollama_message)

        return ollama_messages

    def_get_response_token_counts(self, raw_response: dict) -> dict:
"""Get the token usage reported by the response."""
        try:
            prompt_tokens = raw_response["prompt_eval_count"]
            completion_tokens = raw_response["eval_count"]
            total_tokens = prompt_tokens + completion_tokens
        except KeyError:
            return {}
        except TypeError:
            return {}
        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
        }

    def_prepare_chat_with_tools(
        self,
        tools: List["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,  # doesn't appear to be supported by Ollama
        tool_required: bool = False,  # not yet supported https://github.com/ollama/ollama/blob/main/docs/openai.md#supported-request-fields
        **kwargs: Any,
    ) -> Dict[str, Any]:
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
            argument_dict = tool_call.tool_kwargs

            tool_selections.append(
                ToolSelection(
                    # tool ids not provided by Ollama
                    tool_id=tool_call.tool_name,
                    tool_name=tool_call.tool_name,
                    tool_kwargs=cast(Dict[str, Any], argument_dict),
                )
            )

        return tool_selections

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        ollama_messages = self._convert_to_ollama_messages(messages)

        tools = kwargs.pop("tools", None)
        think = kwargs.pop("think", None) or self.thinking
        format = kwargs.pop("format", "json" if self.json_mode else None)

        response = self.client.chat(
            model=self.model,
            messages=ollama_messages,
            stream=False,
            format=format,
            tools=tools,
            think=think,
            options=self._model_kwargs,
            keep_alive=self.keep_alive,
        )

        response = dict(response)

        blocks: List[TextBlock | ThinkingBlock | ToolCallBlock] = []

        tool_calls = response["message"].get("tool_calls", []) or []
        thinking = response["message"].get("thinking", None)
        if thinking:
            blocks.append(ThinkingBlock(content=thinking))
        blocks.append(TextBlock(text=response["message"].get("content", "")))
        if tool_calls:
            for tool_call in tool_calls:
                blocks.append(
                    ToolCallBlock(
                        tool_name=str(tool_call.get("function", {}).get("name", "")),
                        tool_kwargs=tool_call.get("function", {}).get("arguments", {}),
                    )
                )
        token_counts = self._get_response_token_counts(response)
        if token_counts:
            response["usage"] = token_counts

        return ChatResponse(
            message=ChatMessage(
                blocks=blocks,
                role=response["message"].get("role", MessageRole.ASSISTANT),
            ),
            raw=response,
        )

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        ollama_messages = self._convert_to_ollama_messages(messages)

        tools = kwargs.pop("tools", None)
        think = kwargs.pop("think", None) or self.thinking
        format = kwargs.pop("format", "json" if self.json_mode else None)

        defgen() -> ChatResponseGen:
            response = self.client.chat(
                model=self.model,
                messages=ollama_messages,
                stream=True,
                format=format,
                tools=tools,
                think=think,
                options=self._model_kwargs,
                keep_alive=self.keep_alive,
            )

            response_txt = ""
            thinking_txt = ""
            seen_tool_calls = set()
            all_tool_calls = []

            for r in response:
                if r["message"]["content"] is None:
                    continue

                r = dict(r)

                response_txt += r["message"].get("content", "") or ""
                thinking_txt += r["message"].get("thinking", "") or ""

                new_tool_calls = [dict(t) for t in r["message"].get("tool_calls") or []]
                for tool_call in new_tool_calls:
                    if (
                        str(tool_call["function"]["name"]),
                        str(tool_call["function"]["arguments"]),
                    ) in seen_tool_calls:
                        continue
                    seen_tool_calls.add(
                        (
                            str(tool_call["function"]["name"]),
                            str(tool_call["function"]["arguments"]),
                        )
                    )
                    all_tool_calls.append(tool_call)
                token_counts = self._get_response_token_counts(r)
                if token_counts:
                    r["usage"] = token_counts

                output_blocks: List[ToolCallBlock | ThinkingBlock | TextBlock] = [
                    TextBlock(text=response_txt)
                ]
                if thinking_txt:
                    output_blocks.insert(0, ThinkingBlock(content=thinking_txt))
                if all_tool_calls:
                    for tool_call in all_tool_calls:
                        output_blocks.append(
                            ToolCallBlock(
                                tool_name=tool_call.get("function", {}).get("name", ""),
                                tool_kwargs=tool_call.get("function", {}).get(
                                    "arguments", {}
                                ),
                            )
                        )

                yield ChatResponse(
                    message=ChatMessage(
                        blocks=output_blocks,
                        role=r["message"].get("role", MessageRole.ASSISTANT),
                    ),
                    delta=r["message"].get("content", ""),
                    raw=r,
                    additional_kwargs={
                        "thinking_delta": r["message"].get("thinking", None),
                    },
                )

        return gen()

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        ollama_messages = self._convert_to_ollama_messages(messages)

        tools = kwargs.pop("tools", None)
        think = kwargs.pop("think", None) or self.thinking
        format = kwargs.pop("format", "json" if self.json_mode else None)

        async defgen() -> ChatResponseAsyncGen:
            response = await self.async_client.chat(
                model=self.model,
                messages=ollama_messages,
                stream=True,
                format=format,
                tools=tools,
                think=think,
                options=self._model_kwargs,
                keep_alive=self.keep_alive,
            )

            response_txt = ""
            thinking_txt = ""
            seen_tool_calls = set()
            all_tool_calls = []

            async for r in response:
                if r["message"]["content"] is None:
                    continue

                r = dict(r)

                response_txt += r["message"].get("content", "") or ""
                thinking_txt += r["message"].get("thinking", "") or ""

                new_tool_calls = [dict(t) for t in r["message"].get("tool_calls") or []]
                for tool_call in new_tool_calls:
                    if (
                        str(tool_call["function"]["name"]),
                        str(tool_call["function"]["arguments"]),
                    ) in seen_tool_calls:
                        continue
                    seen_tool_calls.add(
                        (
                            str(tool_call["function"]["name"]),
                            str(tool_call["function"]["arguments"]),
                        )
                    )
                    all_tool_calls.append(tool_call)
                token_counts = self._get_response_token_counts(r)
                if token_counts:
                    r["usage"] = token_counts

                output_blocks: List[ThinkingBlock | ToolCallBlock | TextBlock] = [
                    TextBlock(text=response_txt)
                ]
                if thinking_txt:
                    output_blocks.insert(0, ThinkingBlock(content=thinking_txt))
                if all_tool_calls:
                    for tool_call in all_tool_calls:
                        output_blocks.append(
                            ToolCallBlock(
                                tool_name=tool_call.get("function", {}).get("name", ""),
                                tool_kwargs=tool_call.get("function", {}).get(
                                    "arguments", {}
                                ),
                            )
                        )

                yield ChatResponse(
                    message=ChatMessage(
                        blocks=output_blocks,
                        role=r["message"].get("role", MessageRole.ASSISTANT),
                    ),
                    delta=r["message"].get("content", ""),
                    raw=r,
                    additional_kwargs={
                        "thinking_delta": r["message"].get("thinking", None),
                    },
                )

        return gen()

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        ollama_messages = self._convert_to_ollama_messages(messages)

        tools = kwargs.pop("tools", None)
        think = kwargs.pop("think", None) or self.thinking
        format = kwargs.pop("format", "json" if self.json_mode else None)

        response = await self.async_client.chat(
            model=self.model,
            messages=ollama_messages,
            stream=False,
            format=format,
            tools=tools,
            think=think,
            options=self._model_kwargs,
            keep_alive=self.keep_alive,
        )

        response = dict(response)

        blocks: List[TextBlock | ThinkingBlock | ToolCallBlock] = []

        tool_calls = response["message"].get("tool_calls", []) or []
        thinking = response["message"].get("thinking", None)
        if thinking:
            blocks.append(ThinkingBlock(content=thinking))
        blocks.append(TextBlock(text=response["message"].get("content", "")))
        if tool_calls:
            for tool_call in tool_calls:
                blocks.append(
                    ToolCallBlock(
                        tool_name=tool_call.get("function", {}).get("name", ""),
                        tool_kwargs=tool_call.get("function", {}).get("arguments", {}),
                    )
                )
        token_counts = self._get_response_token_counts(response)
        if token_counts:
            response["usage"] = token_counts

        return ChatResponse(
            message=ChatMessage(
                blocks=blocks,
                role=response["message"].get("role", MessageRole.ASSISTANT),
            ),
            raw=response,
        )

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        return chat_to_completion_decorator(self.chat)(prompt, **kwargs)

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        return await achat_to_completion_decorator(self.achat)(prompt, **kwargs)

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        return stream_chat_to_completion_decorator(self.stream_chat)(prompt, **kwargs)

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        return await astream_chat_to_completion_decorator(self.astream_chat)(
            prompt, **kwargs
        )

    @dispatcher.span
    defstructured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Model:
        if self.pydantic_program_mode == PydanticProgramMode.DEFAULT:
            llm_kwargs = llm_kwargs or {}
            llm_kwargs["format"] = output_cls.model_json_schema()

            messages = prompt.format_messages(**prompt_args)
            response = self.chat(messages, **llm_kwargs)

            return output_cls.model_validate_json(response.message.content or "")
        else:
            return super().structured_predict(
                output_cls, prompt, llm_kwargs, **prompt_args
            )

    @dispatcher.span
    async defastructured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Model:
        if self.pydantic_program_mode == PydanticProgramMode.DEFAULT:
            llm_kwargs = llm_kwargs or {}
            llm_kwargs["format"] = output_cls.model_json_schema()

            messages = prompt.format_messages(**prompt_args)
            response = await self.achat(messages, **llm_kwargs)

            return output_cls.model_validate_json(response.message.content or "")
        else:
            return await super().astructured_predict(
                output_cls, prompt, llm_kwargs, **prompt_args
            )

    @dispatcher.span
    defstream_structured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> Generator[Union[Model, FlexibleModel], None, None]:
"""
        Stream structured predictions as they are generated.

        Args:
            output_cls: The Pydantic class to parse responses into
            prompt: The prompt template to use
            llm_kwargs: Optional kwargs for the LLM
            **prompt_args: Args to format the prompt with

        Returns:
            Generator yielding partial objects as they are generated

        """
        if self.pydantic_program_mode == PydanticProgramMode.DEFAULT:

            defgen(
                output_cls: Type[Model],
                prompt: PromptTemplate,
                llm_kwargs: Dict[str, Any],
                prompt_args: Dict[str, Any],
            ) -> Generator[Union[Model, FlexibleModel], None, None]:
                llm_kwargs = llm_kwargs or {}
                llm_kwargs["format"] = output_cls.model_json_schema()

                messages = prompt.format_messages(**prompt_args)
                response_gen = self.stream_chat(messages, **llm_kwargs)

                cur_objects = None
                for response in response_gen:
                    try:
                        objects = process_streaming_objects(
                            response,
                            output_cls,
                            cur_objects=cur_objects,
                            allow_parallel_tool_calls=False,
                            flexible_mode=True,
                        )
                        cur_objects = (
                            objects if isinstance(objects, list) else [objects]
                        )
                        yield objects
                    except Exception:
                        continue

            return gen(output_cls, prompt, llm_kwargs, prompt_args)
        else:
            return super().stream_structured_predict(
                output_cls, prompt, llm_kwargs, **prompt_args
            )

    @dispatcher.span
    async defastream_structured_predict(
        self,
        output_cls: Type[Model],
        prompt: PromptTemplate,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        **prompt_args: Any,
    ) -> AsyncGenerator[Union[Model, FlexibleModel], None]:
"""Async version of stream_structured_predict."""
        if self.pydantic_program_mode == PydanticProgramMode.DEFAULT:

            async defgen(
                output_cls: Type[Model],
                prompt: PromptTemplate,
                llm_kwargs: Dict[str, Any],
                prompt_args: Dict[str, Any],
            ) -> AsyncGenerator[Union[Model, FlexibleModel], None]:
                llm_kwargs = llm_kwargs or {}
                llm_kwargs["format"] = output_cls.model_json_schema()

                messages = prompt.format_messages(**prompt_args)
                response_gen = await self.astream_chat(messages, **llm_kwargs)

                cur_objects = None
                async for response in response_gen:
                    try:
                        objects = process_streaming_objects(
                            response,
                            output_cls,
                            cur_objects=cur_objects,
                            allow_parallel_tool_calls=False,
                            flexible_mode=True,
                        )
                        cur_objects = (
                            objects if isinstance(objects, list) else [objects]
                        )
                        yield objects
                    except Exception:
                        continue

            return gen(output_cls, prompt, llm_kwargs, prompt_args)
        else:
            # Fall back to non-streaming structured predict
            return await super().astream_structured_predict(
                output_cls, prompt, llm_kwargs, **prompt_args
            )

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/ollama/#llama_index.llms.ollama.Ollama.metadata "Permanent link")

```
metadata: 

```

LLM metadata.
###  get_tool_calls_from_response [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/ollama/#llama_index.llms.ollama.Ollama.get_tool_calls_from_response "Permanent link")

```
get_tool_calls_from_response(
    response: ,
    error_on_no_tool_call:  = True,
) -> []

```

Predict and call the tool.
Source code in `llama-index-integrations/llms/llama-index-llms-ollama/llama_index/llms/ollama/base.py`  
| 
```
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
        argument_dict = tool_call.tool_kwargs

        tool_selections.append(
            ToolSelection(
                # tool ids not provided by Ollama
                tool_id=tool_call.tool_name,
                tool_name=tool_call.tool_name,
                tool_kwargs=cast(Dict[str, Any], argument_dict),
            )
        )

    return tool_selections

```
 |  
| --- | --- |  
###  stream_structured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/ollama/#llama_index.llms.ollama.Ollama.stream_structured_predict "Permanent link")

```
stream_structured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> Generator[Union[, FlexibleModel], None, None]

```

Stream structured predictions as they are generated.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `output_cls`  |  `Type[Model]`  |  The Pydantic class to parse responses into  |  _required_  |  
|  `prompt`  |   |  The prompt template to use  |  _required_  |  
|  `llm_kwargs`  |  `Optional[Dict[str, Any]]`  |  Optional kwargs for the LLM  |  `None`  |  
|  `**prompt_args`  |  Args to format the prompt with  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `None`  |  Generator yielding partial objects as they are generated  |  
Source code in `llama-index-integrations/llms/llama-index-llms-ollama/llama_index/llms/ollama/base.py`  
| 
```
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
"""
    Stream structured predictions as they are generated.

    Args:
        output_cls: The Pydantic class to parse responses into
        prompt: The prompt template to use
        llm_kwargs: Optional kwargs for the LLM
        **prompt_args: Args to format the prompt with

    Returns:
        Generator yielding partial objects as they are generated

    """
    if self.pydantic_program_mode == PydanticProgramMode.DEFAULT:

        defgen(
            output_cls: Type[Model],
            prompt: PromptTemplate,
            llm_kwargs: Dict[str, Any],
            prompt_args: Dict[str, Any],
        ) -> Generator[Union[Model, FlexibleModel], None, None]:
            llm_kwargs = llm_kwargs or {}
            llm_kwargs["format"] = output_cls.model_json_schema()

            messages = prompt.format_messages(**prompt_args)
            response_gen = self.stream_chat(messages, **llm_kwargs)

            cur_objects = None
            for response in response_gen:
                try:
                    objects = process_streaming_objects(
                        response,
                        output_cls,
                        cur_objects=cur_objects,
                        allow_parallel_tool_calls=False,
                        flexible_mode=True,
                    )
                    cur_objects = (
                        objects if isinstance(objects, list) else [objects]
                    )
                    yield objects
                except Exception:
                    continue

        return gen(output_cls, prompt, llm_kwargs, prompt_args)
    else:
        return super().stream_structured_predict(
            output_cls, prompt, llm_kwargs, **prompt_args
        )

```
 |  
| --- | --- |  
###  astream_structured_predict [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/ollama/#llama_index.llms.ollama.Ollama.astream_structured_predict "Permanent link")

```
astream_structured_predict(
    output_cls: [],
    prompt: ,
    llm_kwargs: Optional[[, ]] = None,
    **prompt_args: 
) -> AsyncGenerator[Union[, FlexibleModel], None]

```

Async version of stream_structured_predict.
Source code in `llama-index-integrations/llms/llama-index-llms-ollama/llama_index/llms/ollama/base.py`  
| 
```
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
"""Async version of stream_structured_predict."""
    if self.pydantic_program_mode == PydanticProgramMode.DEFAULT:

        async defgen(
            output_cls: Type[Model],
            prompt: PromptTemplate,
            llm_kwargs: Dict[str, Any],
            prompt_args: Dict[str, Any],
        ) -> AsyncGenerator[Union[Model, FlexibleModel], None]:
            llm_kwargs = llm_kwargs or {}
            llm_kwargs["format"] = output_cls.model_json_schema()

            messages = prompt.format_messages(**prompt_args)
            response_gen = await self.astream_chat(messages, **llm_kwargs)

            cur_objects = None
            async for response in response_gen:
                try:
                    objects = process_streaming_objects(
                        response,
                        output_cls,
                        cur_objects=cur_objects,
                        allow_parallel_tool_calls=False,
                        flexible_mode=True,
                    )
                    cur_objects = (
                        objects if isinstance(objects, list) else [objects]
                    )
                    yield objects
                except Exception:
                    continue

        return gen(output_cls, prompt, llm_kwargs, prompt_args)
    else:
        # Fall back to non-streaming structured predict
        return await super().astream_structured_predict(
            output_cls, prompt, llm_kwargs, **prompt_args
        )

```
 |  
| --- | --- |  
options: members: - Ollama
