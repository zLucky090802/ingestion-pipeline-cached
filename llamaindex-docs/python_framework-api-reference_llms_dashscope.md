# Dashscope
##  DashScope [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/dashscope/#llama_index.llms.dashscope.DashScope "Permanent link")
Bases: `FunctionCallingLLM`
DashScope LLM.
Examples:
`pip install llama-index-llms-dashscope`

```
fromllama_index.llms.dashscopeimport DashScope, DashScopeGenerationModels

dashscope_llm = DashScope(model_name=DashScopeGenerationModels.QWEN_MAX)
response = llm.complete("What is the meaning of life?")
print(response.text)

```

Source code in `llama-index-integrations/llms/llama-index-llms-dashscope/llama_index/llms/dashscope/base.py`  
| 
```
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
```
 | 
```
classDashScope(FunctionCallingLLM):
"""
    DashScope LLM.

    Examples:
        `pip install llama-index-llms-dashscope`

        ```python
        from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels

        dashscope_llm = DashScope(model_name=DashScopeGenerationModels.QWEN_MAX)
        response = llm.complete("What is the meaning of life?")
        print(response.text)
        ```

    """

""" In Pydantic V2, protected_namespaces is a configuration option used to prevent certain namespace keywords
      (such as model_, etc.) from being used as field names. so we need to disable it here.
    """
    model_config = ConfigDict(protected_namespaces=())

    model_name: str = Field(
        default=DashScopeGenerationModels.QWEN_MAX,
        description="The DashScope model to use.",
    )
    max_tokens: Optional[int] = Field(
        description="The maximum number of tokens to generate.",
        default=DEFAULT_NUM_OUTPUTS,
        gt=0,
    )
    incremental_output: Optional[bool] = Field(
        description="Control stream output, If False, the subsequent \
                                                            output will include the content that has been \
                                                            output previously.",
        default=True,
    )
    enable_search: Optional[bool] = Field(
        description="The model has a built-in Internet search service. \
                                                            This parameter controls whether the model refers to \
                                                            the Internet search results when generating text.",
        default=False,
    )
    stop: Optional[Any] = Field(
        description="str, list of str or token_id, list of token id. It will automatically \
                                             stop when the generated content is about to contain the specified string \
                                             or token_ids, and the generated content does not contain \
                                             the specified content.",
        default=None,
    )
    temperature: Optional[float] = Field(
        description="The temperature to use during generation.",
        default=DEFAULT_TEMPERATURE,
        ge=0.0,
        le=2.0,
    )
    top_k: Optional[int] = Field(
        description="Sample counter when generate.", default=None
    )
    top_p: Optional[float] = Field(
        description="Sample probability threshold when generate."
    )
    seed: Optional[int] = Field(
        description="Random seed when generate.", default=1234, ge=0
    )
    repetition_penalty: Optional[float] = Field(
        description="Penalty for repeated words in generated text; \
                                                             1.0 is no penalty, values greater than 1 discourage \
                                                             repetition.",
        default=None,
    )
    api_key: str = Field(
        default=None, description="The DashScope API key.", exclude=True
    )
    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description="The maximum number of context tokens for the model.",
        gt=0,
    )
    is_function_calling_model: bool = Field(
        default=True,
        description="Whether the model is a function calling model.",
    )

    def__init__(
        self,
        model_name: Optional[str] = DashScopeGenerationModels.QWEN_MAX,
        max_tokens: Optional[int] = DEFAULT_NUM_OUTPUTS,
        incremental_output: Optional[int] = True,
        enable_search: Optional[bool] = False,
        stop: Optional[Any] = None,
        temperature: Optional[float] = DEFAULT_TEMPERATURE,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        seed: Optional[int] = 1234,
        api_key: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
        is_function_calling_model: Optional[bool] = True,
        context_window: Optional[int] = DEFAULT_CONTEXT_WINDOW,
        **kwargs: Any,
    ):
        super().__init__(
            model_name=model_name,
            max_tokens=max_tokens,
            incremental_output=incremental_output,
            enable_search=enable_search,
            stop=stop,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            seed=seed,
            api_key=api_key,
            callback_manager=callback_manager,
            is_function_calling_model=is_function_calling_model,
            context_window=context_window,
            kwargs=kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "DashScope_LLM"

    @property
    defmetadata(self) -> LLMMetadata:
"""LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.max_tokens,
            model_name=self.model_name,
            is_chat_model=True,
            is_function_calling_model=self.is_function_calling_model,
        )

    def_prepare_chat_with_tools(
        self,
        tools: Sequence["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        tool_required: bool = False,  # doesn't seem to be supported by dashscope - https://github.com/dashscope/dashscope-sdk-python
        **kwargs: Any,
    ) -> Dict[str, Any]:
        tools_spec = [self._convert_tool_to_dashscope_format(tool) for tool in tools]

        messages = []
        if chat_history:
            messages.extend(chat_history)
        if user_msg:
            if isinstance(user_msg, str):
                messages.append(ChatMessage(role="user", content=user_msg))
            else:
                messages.append(user_msg)
        return {
            "messages": messages,
            "tools": tools_spec,
            "stream": True,
            **kwargs,
        }

    def_convert_tool_to_dashscope_format(self, tool: "BaseTool") -> Dict:
        params = tool.metadata.get_parameters_dict()
        properties, required_fields, param_type = (
            params["properties"],
            params.get("required", []),
            params.get("type"),
        )

        return {
            "type": "function",
            "function": {
                "name": tool.metadata.name,
                "description": tool.metadata.description,
                "parameters": {
                    "type": param_type,
                    "properties": properties,
                },
                "required": required_fields,
            },
        }

    defget_tool_calls_from_response(
        self,
        response: "ChatResponse",
        error_on_no_tool_call: bool = True,
        **kwargs: Any,
    ) -> List[ToolSelection]:
        tool_calls = response.message.additional_kwargs.get("tool_calls", [])
        if len(tool_calls)  1:
            if error_on_no_tool_call:
                raise ValueError(
                    f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
                )
            else:
                return []

        tool_selections = []
        for tool_call in tool_calls:
            argument_dict = (
                json.loads(tool_call["function"]["arguments"])
                if isinstance(tool_call["function"]["arguments"], str)
                else tool_call["function"]["arguments"]
            )
            tool_selections.append(
                ToolSelection(
                    tool_id=tool_call["id"],
                    tool_name=tool_call["function"]["name"],
                    tool_kwargs=argument_dict,
                )
            )

        return tool_selections

    def_get_default_parameters(self) -> Dict:
        params: Dict[Any, Any] = {}
        if self.max_tokens is not None:
            params["max_tokens"] = self.max_tokens
        params["incremental_output"] = self.incremental_output
        params["enable_search"] = self.enable_search
        if self.stop is not None:
            params["stop"] = self.stop
        if self.temperature is not None:
            params["temperature"] = self.temperature

        if self.top_k is not None:
            params["top_k"] = self.top_k

        if self.top_p is not None:
            params["top_p"] = self.top_p
        if self.seed is not None:
            params["seed"] = self.seed

        return params

    def_get_input_parameters(
        self, prompt: str, **kwargs: Any
    ) -> Tuple[ChatMessage, Dict]:
        parameters = self._get_default_parameters()
        parameters.update(kwargs)
        parameters["stream"] = False
        # we only use message response
        parameters["result_format"] = "message"
        message = ChatMessage(
            role=MessageRole.USER.value,
            content=prompt,
        )
        return message, parameters

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        message, parameters = self._get_input_parameters(prompt=prompt, **kwargs)
        parameters.pop("incremental_output", None)
        parameters.pop("stream", None)
        messages = chat_message_to_dashscope_messages([message])
        response = call_with_messages(
            model=self.model_name,
            messages=messages,
            api_key=self.api_key,
            parameters=parameters,
        )
        return dashscope_response_to_completion_response(response)

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        message, parameters = self._get_input_parameters(prompt=prompt, **kwargs)
        parameters.pop("incremental_output", None)
        parameters.pop("stream", None)
        messages = chat_message_to_dashscope_messages([message])
        response = await acall_with_messages(
            model=self.model_name,
            messages=messages,
            api_key=self.api_key,
            parameters=parameters,
        )
        return dashscope_response_to_completion_response(response)

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        message, parameters = self._get_input_parameters(prompt=prompt, kwargs=kwargs)
        parameters["incremental_output"] = True
        parameters["stream"] = True
        responses = call_with_messages(
            model=self.model_name,
            messages=chat_message_to_dashscope_messages([message]),
            api_key=self.api_key,
            parameters=parameters,
        )

        defgen() -> CompletionResponseGen:
            content = ""
            for response in responses:
                if response.status_code == HTTPStatus.OK:
                    top_choice = response.output.choices[0]
                    incremental_output = top_choice["message"]["content"]
                    if not incremental_output:
                        incremental_output = ""

                    content += incremental_output
                    yield CompletionResponse(
                        text=content, delta=incremental_output, raw=response
                    )
                else:
                    yield CompletionResponse(text="", raw=response)
                    return

        return gen()

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        parameters = self._get_default_parameters()
        parameters.update({**kwargs})
        parameters.pop("stream", None)
        parameters.pop("incremental_output", None)
        parameters["result_format"] = "message"  # only use message format.
        response = call_with_messages(
            model=self.model_name,
            messages=chat_message_to_dashscope_messages(messages),
            api_key=self.api_key,
            parameters=parameters,
        )
        return dashscope_response_to_chat_response(response)

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        parameters = self._get_default_parameters()
        parameters.update({**kwargs})
        parameters.pop("stream", None)
        parameters.pop("incremental_output", None)
        parameters["result_format"] = "message"  # only use message format.
        response = await acall_with_messages(
            model=self.model_name,
            messages=chat_message_to_dashscope_messages(messages),
            api_key=self.api_key,
            parameters=parameters,
        )
        return dashscope_response_to_chat_response(response)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        parameters = self._get_default_parameters()
        parameters.update({**kwargs})
        parameters["stream"] = True
        parameters["incremental_output"] = True
        parameters["result_format"] = "message"  # only use message format.
        response = call_with_messages(
            model=self.model_name,
            messages=chat_message_to_dashscope_messages(messages),
            api_key=self.api_key,
            parameters=parameters,
        )

        defgen() -> ChatResponseGen:
            content = ""
            for r in response:
                if r.status_code == HTTPStatus.OK:
                    top_choice = r.output.choices[0]
                    incremental_output = top_choice["message"]["content"]
                    role = top_choice["message"]["role"]
                    content += incremental_output
                    yield ChatResponse(
                        message=ChatMessage(role=role, content=content),
                        delta=incremental_output,
                        raw=r,
                    )
                else:
                    yield ChatResponse(message=ChatMessage(), raw=response)
                    return

        return gen()

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
"""Asynchronously stream completion results from DashScope."""
        message, parameters = self._get_input_parameters(prompt=prompt, **kwargs)
        parameters["incremental_output"] = True
        parameters["stream"] = True
        dashscope_messages = chat_message_to_dashscope_messages([message])
        async_responses = astream_call_with_messages(
            model=self.model_name,
            messages=dashscope_messages,
            api_key=self.api_key,
            parameters=parameters,
        )

        async defgen() -> AsyncGenerator[CompletionResponse, None]:
            content = ""
            async for response in async_responses:
                if response.status_code == HTTPStatus.OK:
                    top_choice = response.output.choices[0]
                    incremental_output = top_choice["message"]["content"] or ""
                    content += incremental_output
                    yield CompletionResponse(
                        text=content,
                        delta=incremental_output,
                        raw=response,
                    )
                else:
                    yield CompletionResponse(text="", raw=response)
                    return

        return gen()

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
"""Asynchronously stream chat results from DashScope."""
        parameters = self._get_default_parameters()
        tools = kwargs.pop("tools", None)

        parameters.update(kwargs)
        parameters["incremental_output"] = True
        parameters["result_format"] = "message"
        parameters["stream"] = True

        dashscope_messages = chat_message_to_dashscope_messages(messages)

        async_responses = astream_call_with_messages(
            model=self.model_name,
            messages=dashscope_messages,
            format=format,
            tools=tools,
            api_key=self.api_key,
            parameters=parameters,
        )

        async defgen() -> AsyncGenerator[ChatResponse, None]:
            content = ""
            all_tool_calls = {}
            async for response in async_responses:
                if response.status_code == HTTPStatus.OK:
                    top_choice = response.output.choices[0]
                    role = top_choice["message"]["role"]
                    incremental_output = top_choice["message"].get("content", "")
                    tool_calls = top_choice["message"].get("tool_calls", [])
                    content += incremental_output

                    for tool_call in tool_calls:
                        index = tool_call["index"]
                        if index is None:
                            continue
                        if index not in all_tool_calls:
                            all_tool_calls[index] = tool_call
                        else:
                            function_args = str(
                                tool_call["function"].get("arguments", "").strip()
                            )
                            if function_args:
                                all_tool_calls[index]["function"]["arguments"] += (
                                    function_args
                                )
                    yield ChatResponse(
                        message=ChatMessage(
                            role=role,
                            content=content,
                            additional_kwargs={
                                "tool_calls": list(all_tool_calls.values())
                            },
                        ),
                        delta=incremental_output,
                        raw=response,
                    )
                else:
                    yield ChatResponse(message=ChatMessage(), raw=response)
                    return

        return gen()

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/dashscope/#llama_index.llms.dashscope.DashScope.metadata "Permanent link")

```
metadata: 

```

LLM metadata.
###  astream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/dashscope/#llama_index.llms.dashscope.DashScope.astream_complete "Permanent link")

```
astream_complete(
    prompt: , formatted:  = False, **kwargs: 
) -> CompletionResponseGen

```

Asynchronously stream completion results from DashScope.
Source code in `llama-index-integrations/llms/llama-index-llms-dashscope/llama_index/llms/dashscope/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
async defastream_complete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponseGen:
"""Asynchronously stream completion results from DashScope."""
    message, parameters = self._get_input_parameters(prompt=prompt, **kwargs)
    parameters["incremental_output"] = True
    parameters["stream"] = True
    dashscope_messages = chat_message_to_dashscope_messages([message])
    async_responses = astream_call_with_messages(
        model=self.model_name,
        messages=dashscope_messages,
        api_key=self.api_key,
        parameters=parameters,
    )

    async defgen() -> AsyncGenerator[CompletionResponse, None]:
        content = ""
        async for response in async_responses:
            if response.status_code == HTTPStatus.OK:
                top_choice = response.output.choices[0]
                incremental_output = top_choice["message"]["content"] or ""
                content += incremental_output
                yield CompletionResponse(
                    text=content,
                    delta=incremental_output,
                    raw=response,
                )
            else:
                yield CompletionResponse(text="", raw=response)
                return

    return gen()

```
 |  
| --- | --- |  
###  astream_chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/dashscope/#llama_index.llms.dashscope.DashScope.astream_chat "Permanent link")

```
astream_chat(
    messages: Sequence[], **kwargs: 
) -> ChatResponseGen

```

Asynchronously stream chat results from DashScope.
Source code in `llama-index-integrations/llms/llama-index-llms-dashscope/llama_index/llms/dashscope/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
async defastream_chat(
    self, messages: Sequence[ChatMessage], **kwargs: Any
) -> ChatResponseGen:
"""Asynchronously stream chat results from DashScope."""
    parameters = self._get_default_parameters()
    tools = kwargs.pop("tools", None)

    parameters.update(kwargs)
    parameters["incremental_output"] = True
    parameters["result_format"] = "message"
    parameters["stream"] = True

    dashscope_messages = chat_message_to_dashscope_messages(messages)

    async_responses = astream_call_with_messages(
        model=self.model_name,
        messages=dashscope_messages,
        format=format,
        tools=tools,
        api_key=self.api_key,
        parameters=parameters,
    )

    async defgen() -> AsyncGenerator[ChatResponse, None]:
        content = ""
        all_tool_calls = {}
        async for response in async_responses:
            if response.status_code == HTTPStatus.OK:
                top_choice = response.output.choices[0]
                role = top_choice["message"]["role"]
                incremental_output = top_choice["message"].get("content", "")
                tool_calls = top_choice["message"].get("tool_calls", [])
                content += incremental_output

                for tool_call in tool_calls:
                    index = tool_call["index"]
                    if index is None:
                        continue
                    if index not in all_tool_calls:
                        all_tool_calls[index] = tool_call
                    else:
                        function_args = str(
                            tool_call["function"].get("arguments", "").strip()
                        )
                        if function_args:
                            all_tool_calls[index]["function"]["arguments"] += (
                                function_args
                            )
                yield ChatResponse(
                    message=ChatMessage(
                        role=role,
                        content=content,
                        additional_kwargs={
                            "tool_calls": list(all_tool_calls.values())
                        },
                    ),
                    delta=incremental_output,
                    raw=response,
                )
            else:
                yield ChatResponse(message=ChatMessage(), raw=response)
                return

    return gen()

```
 |  
| --- | --- |  
##  DashScopeGenerationModels [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/dashscope/#llama_index.llms.dashscope.DashScopeGenerationModels "Permanent link")
DashScope Qwen serial models.
Source code in `llama-index-integrations/llms/llama-index-llms-dashscope/llama_index/llms/dashscope/base.py`  
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
```
 | 
```
classDashScopeGenerationModels:
"""DashScope Qwen serial models."""

    QWEN_TURBO = "qwen-turbo"
    QWEN_PLUS = "qwen-plus"
    QWEN_MAX = "qwen-max"
    QWEN_MAX_1201 = "qwen-max-1201"
    QWEN_MAX_LONGCONTEXT = "qwen-max-longcontext"

```
 |  
| --- | --- |  
options: members: - DashScope
