# Huggingface api
##  HuggingFaceInferenceAPI [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/huggingface_api/#llama_index.llms.huggingface_api.HuggingFaceInferenceAPI "Permanent link")
Bases: `FunctionCallingLLM`
Wrapper on the Hugging Face's Inference API.
Overview of the design: - Synchronous uses InferenceClient, asynchronous uses AsyncInferenceClient - chat uses the conversational task: https://huggingface.co/tasks/conversational - complete uses the text generation task: https://huggingface.co/tasks/text-generation
Note: some models that support the text generation task can leverage Hugging Face's optimized deployment toolkit called text-generation-inference (TGI). Use InferenceClient.get_model_status to check if TGI is being used.
Relevant links: - General Docs: https://huggingface.co/docs/api-inference/index - API Docs: https://huggingface.co/docs/huggingface_hub/main/en/package_reference/inference_client - Source: https://github.com/huggingface/huggingface_hub/tree/main/src/huggingface_hub/inference
Source code in `llama-index-integrations/llms/llama-index-llms-huggingface-api/llama_index/llms/huggingface_api/base.py`  
| 
```
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
```
 | 
```
classHuggingFaceInferenceAPI(FunctionCallingLLM):
"""
    Wrapper on the Hugging Face's Inference API.

    Overview of the design:
    - Synchronous uses InferenceClient, asynchronous uses AsyncInferenceClient
    - chat uses the conversational task: https://huggingface.co/tasks/conversational
    - complete uses the text generation task: https://huggingface.co/tasks/text-generation

    Note: some models that support the text generation task can leverage Hugging
    Face's optimized deployment toolkit called text-generation-inference (TGI).
    Use InferenceClient.get_model_status to check if TGI is being used.

    Relevant links:
    - General Docs: https://huggingface.co/docs/api-inference/index
    - API Docs: https://huggingface.co/docs/huggingface_hub/main/en/package_reference/inference_client
    - Source: https://github.com/huggingface/huggingface_hub/tree/main/src/huggingface_hub/inference
    """

    @classmethod
    defclass_name(cls) -> str:
        return "HuggingFaceInferenceAPI"

    model: Optional[str] = Field(
        default=None,
        description=(
            "The model to run inference with. Can be a model id hosted on the Hugging"
            " Face Hub, e.g. bigcode/starcoder or a URL to a deployed Inference"
            " Endpoint. Defaults to None, in which case a recommended model is"
            " automatically selected for the task (see Field below)."
        ),
    )

    # TODO: deprecate this field
    model_name: Optional[str] = Field(
        default=None,
        description=(
            "The model to run inference with. Can be a model id hosted on the Hugging"
            " Face Hub, e.g. bigcode/starcoder or a URL to a deployed Inference"
            " Endpoint. Defaults to None, in which case a recommended model is"
            " automatically selected for the task (see Field below)."
        ),
    )
    provider: str = Field(
        default="auto",
        description=(
            "Name of the provider to use for inference. Can be 'black-forest-labs',"
            " 'cerebras', 'cohere', 'fal-ai', 'fireworks-ai', 'hf-inference',"
            " 'hyperbolic', 'nebius', 'novita', 'openai', 'replicate', 'sambanova'"
            " or 'together'. defaults to hf-inference (Hugging Face Serverless Inference API)."
            " If model is a URL or `base_url` is passed, then `provider` is not used."
        ),
    )
    token: Union[str, bool, None] = Field(
        default=None,
        description=(
            "Hugging Face token. Will default to the locally saved token. Pass "
            "token=False if you don’t want to send your token to the server."
        ),
    )
    timeout: Optional[float] = Field(
        default=None,
        description=(
            "The maximum number of seconds to wait for a response from the server."
            " Loading a new model in Inference API can take up to several minutes."
            " Defaults to None, meaning it will loop until the server is available."
        ),
    )
    headers: Dict[str, str] = Field(
        default=None,
        description=(
            "Additional headers to send to the server. By default only the"
            " authorization and user-agent headers are sent. Values in this dictionary"
            " will override the default values."
        ),
    )
    cookies: Dict[str, str] = Field(
        default=None, description="Additional cookies to send to the server."
    )
    task: Optional[str] = Field(
        default=None,
        description=(
            "Optional task to pick Hugging Face's recommended model, used when"
            " model_name is left as default of None."
        ),
    )

    _sync_client: InferenceClient = PrivateAttr()
    _async_client: AsyncInferenceClient = PrivateAttr()
    _get_model_info: Callable[..., ModelInfo] = PrivateAttr()

    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description=(
            LLMMetadata.model_fields["context_window"].description
            + " This may be looked up in a model's `config.json`."
        ),
    )
    num_output: int = Field(
        default=DEFAULT_NUM_OUTPUTS,
        description=LLMMetadata.model_fields["num_output"].description,
    )
    temperature: float = Field(
        default=0.1,
        description="The temperature to use for the model.",
        gt=0.0,
    )
    is_chat_model: bool = Field(
        default=True,
        description="Controls whether the chat or text generation methods are used.",
    )
    is_function_calling_model: bool = Field(
        default=False,
        description="Controls whether the function calling methods are used.",
    )

    def__init__(self, **kwargs: Any) -> None:
        model_name = kwargs.get("model_name") or kwargs.get("model")
        if model_name is None:
            task = kwargs.get("task", "")
            # NOTE: task being None or empty string leads to ValueError,
            # which ensures model is present
            kwargs["model_name"] = InferenceClient.get_recommended_model(task=task)
            logger.debug(
                f"Using Hugging Face's recommended model {kwargs['model_name']}"
                f" given task {task}."
            )

        if kwargs.get("task") is None:
            task = "conversational"
            kwargs["task"] = task
        else:
            task = kwargs["task"].lower()

        if kwargs.get("is_function_calling_model", False):
            print(
                "Function calling is currently not supported for Hugging Face Inference API, setting is_function_calling_model to False"
            )
            kwargs["is_function_calling_model"] = False

        super().__init__(**kwargs)  # Populate pydantic Fields
        self._sync_client = InferenceClient(**self._get_inference_client_kwargs())
        self._async_client = AsyncInferenceClient(**self._get_inference_client_kwargs())

        # set context window if not provided, if we can get the endpoint info
        try:
            info = self._sync_client.get_endpoint_info()
            if "max_input_tokens" in info and kwargs.get("context_window") is None:
                self.context_window = info["max_input_tokens"]
        except Exception:
            pass

    def_get_inference_client_kwargs(self) -> Dict[str, Any]:
"""Extract the Hugging Face InferenceClient construction parameters."""
        return {
            "model": self.model_name or self.model,
            "provider": self.provider,
            "token": self.token,
            "timeout": self.timeout,
            "headers": self.headers,
            "cookies": self.cookies,
        }

    def_get_model_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        base_kwargs = {
            "model": self.model_name or self.model,
            "max_tokens": self.num_output,
            "temperature": self.temperature,
        }
        return {**base_kwargs, **kwargs}

    def_to_huggingface_messages(
        self, messages: Sequence[ChatMessage]
    ) -> List[Dict[str, Any]]:
        hf_dicts = []
        for m in messages:
            hf_dicts.append(
                {"role": m.role.value, "content": m.content if m.content else ""}
            )
            if m.additional_kwargs.get("tool_calls", []):
                tool_call_dicts = []
                for tool_call in m.additional_kwargs["tool_calls"]:
                    function_dict = {
                        "name": tool_call.id,
                        "arguments": tool_call.function.arguments,
                    }
                    tool_call_dicts.append(
                        {"type": "function", "function": function_dict}
                    )

                hf_dicts[-1]["tool_calls"] = tool_call_dicts

            if m.role == MessageRole.TOOL:
                hf_dicts[-1]["name"] = m.additional_kwargs.get("tool_call_id")

        return hf_dicts

    def_parse_streaming_tool_calls(
        self, tool_call_strs: List[str]
    ) -> List[Union[ToolSelection, str]]:
        tool_calls = []
        # Try to parse into complete objects, otherwise keep as strings
        for tool_call_str in tool_call_strs:
            try:
                tool_call_dict = json.loads(tool_call_str)
                args = tool_call_dict["function"]
                name = args.pop("_name")
                tool_calls.append(
                    ChatCompletionOutputToolCall(
                        id=name,
                        type="function",
                        function=ChatCompletionOutputFunctionDefinition(
                            arguments=args,
                            name=name,
                        ),
                    )
                )
            except Exception as e:
                tool_calls.append(tool_call_str)

        return tool_calls

    defget_model_info(self, **kwargs: Any) -> "ModelInfo":
"""Get metadata on the current model from Hugging Face."""
        model_name = self.model_name or self.model
        return model_info(model_name, **kwargs)

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            is_chat_model=self.is_chat_model,
            is_function_calling_model=self.is_function_calling_model,
            model_name=self.model_name or self.model,
        )

    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        if self.task == "conversational" or self.task is None:
            model_kwargs = self._get_model_kwargs(**kwargs)

            output: ChatCompletionOutput = self._sync_client.chat_completion(
                messages=self._to_huggingface_messages(messages),
                **model_kwargs,
            )

            content = output.choices[0].message.content or ""
            tool_calls = output.choices[0].message.tool_calls or []
            additional_kwargs = {"tool_calls": tool_calls} if tool_calls else {}

            return ChatResponse(
                message=ChatMessage(
                    role=MessageRole.ASSISTANT,
                    content=content,
                    additional_kwargs=additional_kwargs,
                ),
                raw=output,
            )
        else:
            # try and use text generation
            prompt = self.messages_to_prompt(messages)
            completion = self.complete(prompt, formatted=True, **kwargs)
            return completion_response_to_chat_response(completion)

    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        if self.task == "conversational":
            chat_resp = self.chat(
                messages=[ChatMessage(role=MessageRole.USER, content=prompt)], **kwargs
            )
            return chat_response_to_completion_response(chat_resp)

        model_kwargs = self._get_model_kwargs(**kwargs)
        model_kwargs["max_new_tokens"] = model_kwargs["max_tokens"]
        del model_kwargs["max_tokens"]

        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        return CompletionResponse(
            text=self._sync_client.text_generation(prompt, **model_kwargs)
        )

    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        if self.task == "conversational" or self.task is None:
            model_kwargs = self._get_model_kwargs(**kwargs)

            defgen() -> ChatResponseGen:
                response = ""
                tool_call_strs = []
                cur_index = -1
                for chunk in self._sync_client.chat_completion(
                    messages=self._to_huggingface_messages(messages),
                    stream=True,
                    **model_kwargs,
                ):
                    chunk: ChatCompletionStreamOutput = chunk

                    delta = chunk.choices[0].delta.content or ""
                    response += delta
                    tool_call_delta = chunk.choices[0].delta.tool_calls
                    if tool_call_delta:
                        if tool_call_delta.index != cur_index:
                            cur_index = tool_call_delta.index
                            tool_call_strs.append(tool_call_delta.function.arguments)
                        else:
                            tool_call_strs[cur_index] += (
                                tool_call_delta.function.arguments
                            )

                    tool_calls = self._parse_streaming_tool_calls(tool_call_strs)
                    additional_kwargs = {"tool_calls": tool_calls} if tool_calls else {}
                    yield ChatResponse(
                        message=ChatMessage(
                            role=MessageRole.ASSISTANT,
                            content=response,
                            additional_kwargs=additional_kwargs,
                        ),
                        delta=delta,
                        raw=chunk,
                    )

            return gen()
        else:
            prompt = self.messages_to_prompt(messages)
            completion_stream = self.stream_complete(prompt, formatted=True, **kwargs)
            return stream_completion_response_to_chat_response(completion_stream)

    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        if self.task == "conversational":
            chat_gen = self.stream_chat(
                messages=[ChatMessage(role=MessageRole.USER, content=prompt)], **kwargs
            )
            return stream_chat_response_to_completion_response(chat_gen)

        model_kwargs = self._get_model_kwargs(**kwargs)
        model_kwargs["max_new_tokens"] = model_kwargs["max_tokens"]
        del model_kwargs["max_tokens"]

        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        defgen() -> CompletionResponseGen:
            response = ""
            for delta in self._sync_client.text_generation(
                prompt, stream=True, **model_kwargs
            ):
                response += delta
                yield CompletionResponse(text=response, delta=delta)

        return gen()

    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        if self.task == "conversational" or self.task is None:
            model_kwargs = self._get_model_kwargs(**kwargs)

            output: ChatCompletionOutput = await self._async_client.chat_completion(
                messages=self._to_huggingface_messages(messages),
                **model_kwargs,
            )

            content = output.choices[0].message.content or ""
            tool_calls = output.choices[0].message.tool_calls or []
            additional_kwargs = {"tool_calls": tool_calls} if tool_calls else {}

            return ChatResponse(
                message=ChatMessage(
                    role=MessageRole.ASSISTANT,
                    content=content,
                    additional_kwargs=additional_kwargs,
                ),
                raw=output,
            )
        else:
            # try and use text generation
            prompt = self.messages_to_prompt(messages)
            completion = await self.acomplete(prompt, formatted=True, **kwargs)
            return completion_response_to_chat_response(completion)

    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        if self.task == "conversational":
            chat_resp = await self.achat(
                messages=[ChatMessage(role=MessageRole.USER, content=prompt)], **kwargs
            )
            return chat_response_to_completion_response(chat_resp)

        model_kwargs = self._get_model_kwargs(**kwargs)
        model_kwargs["max_new_tokens"] = model_kwargs["max_tokens"]
        del model_kwargs["max_tokens"]

        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        return CompletionResponse(
            text=await self._async_client.text_generation(prompt, **model_kwargs)
        )

    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        if self.task == "conversational" or self.task is None:
            model_kwargs = self._get_model_kwargs(**kwargs)

            async defgen() -> ChatResponseAsyncGen:
                response = ""
                tool_call_strs = []
                cur_index = -1
                async for chunk in await self._async_client.chat_completion(
                    messages=self._to_huggingface_messages(messages),
                    stream=True,
                    **model_kwargs,
                ):
                    if chunk.choices[0].finish_reason is not None:
                        break

                    chunk: ChatCompletionStreamOutput = chunk

                    delta = chunk.choices[0].delta.content or ""
                    response += delta
                    tool_call_delta = chunk.choices[0].delta.tool_calls
                    if tool_call_delta:
                        if tool_call_delta.index != cur_index:
                            cur_index = tool_call_delta.index
                            tool_call_strs.append(tool_call_delta.function.arguments)
                        else:
                            tool_call_strs[cur_index] += (
                                tool_call_delta.function.arguments
                            )

                    tool_calls = self._parse_streaming_tool_calls(tool_call_strs)

                    additional_kwargs = {"tool_calls": tool_calls} if tool_calls else {}

                    yield ChatResponse(
                        message=ChatMessage(
                            role=MessageRole.ASSISTANT,
                            content=response,
                            additional_kwargs=additional_kwargs,
                        ),
                        delta=delta,
                        raw=chunk,
                    )

                await self._async_client.close()

            return gen()
        else:
            prompt = self.messages_to_prompt(messages)
            completion_stream = await self.astream_complete(
                prompt, formatted=True, **kwargs
            )
            return astream_completion_response_to_chat_response(completion_stream)

    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        if self.task == "conversational":
            chat_gen = await self.astream_chat(
                messages=[ChatMessage(role=MessageRole.USER, content=prompt)], **kwargs
            )
            return astream_chat_response_to_completion_response(chat_gen)

        model_kwargs = self._get_model_kwargs(**kwargs)
        model_kwargs["max_new_tokens"] = model_kwargs["max_tokens"]
        del model_kwargs["max_tokens"]

        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        async defgen() -> CompletionResponseAsyncGen:
            response = ""
            async for delta in await self._async_client.text_generation(
                prompt, stream=True, **model_kwargs
            ):
                response += delta
                yield CompletionResponse(text=response, delta=delta)

            await self._async_client.close()

        return gen()

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
        }

    def_validate_chat_with_tools_response(
        self,
        response: ChatResponse,
        tools: List["BaseTool"],
        allow_parallel_tool_calls: bool = False,
        **kwargs: Any,
    ) -> ChatResponse:
"""Validate the response from chat_with_tools."""
        if not allow_parallel_tool_calls and response.message.additional_kwargs.get(
            "tool_calls", []
        ):
            response.additional_kwargs["tool_calls"] = (
                response.message.additional_kwargs["tool_calls"][0]
            )

        return response

    defget_tool_calls_from_response(
        self,
        response: "ChatResponse",
        error_on_no_tool_call: bool = True,
    ) -> List[ToolSelection]:
"""Predict and call the tool."""
        tool_calls: List[ChatCompletionOutputToolCall] = (
            response.message.additional_kwargs.get("tool_calls", [])
        )
        if len(tool_calls)  1:
            if error_on_no_tool_call:
                raise ValueError(
                    f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
                )
            else:
                return []

        tool_selections = []
        for tool_call in tool_calls:
            # while streaming, tool_call is a string
            if isinstance(tool_call, str):
                continue

            tool_selections.append(
                ToolSelection(
                    tool_id=tool_call.id,
                    tool_name=tool_call.function.name,
                    tool_kwargs=tool_call.function.arguments,
                )
            )

        return tool_selections

```
 |  
| --- | --- |  
###  get_model_info [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/huggingface_api/#llama_index.llms.huggingface_api.HuggingFaceInferenceAPI.get_model_info "Permanent link")

```
get_model_info(**kwargs: ) -> ModelInfo

```

Get metadata on the current model from Hugging Face.
Source code in `llama-index-integrations/llms/llama-index-llms-huggingface-api/llama_index/llms/huggingface_api/base.py`  
| 
```
268
269
270
271
```
 | 
```
defget_model_info(self, **kwargs: Any) -> "ModelInfo":
"""Get metadata on the current model from Hugging Face."""
    model_name = self.model_name or self.model
    return model_info(model_name, **kwargs)

```
 |  
| --- | --- |  
###  get_tool_calls_from_response [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/huggingface_api/#llama_index.llms.huggingface_api.HuggingFaceInferenceAPI.get_tool_calls_from_response "Permanent link")

```
get_tool_calls_from_response(
    response: ,
    error_on_no_tool_call:  = True,
) -> []

```

Predict and call the tool.
Source code in `llama-index-integrations/llms/llama-index-llms-huggingface-api/llama_index/llms/huggingface_api/base.py`  
| 
```
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
```
 | 
```
defget_tool_calls_from_response(
    self,
    response: "ChatResponse",
    error_on_no_tool_call: bool = True,
) -> List[ToolSelection]:
"""Predict and call the tool."""
    tool_calls: List[ChatCompletionOutputToolCall] = (
        response.message.additional_kwargs.get("tool_calls", [])
    )
    if len(tool_calls)  1:
        if error_on_no_tool_call:
            raise ValueError(
                f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
            )
        else:
            return []

    tool_selections = []
    for tool_call in tool_calls:
        # while streaming, tool_call is a string
        if isinstance(tool_call, str):
            continue

        tool_selections.append(
            ToolSelection(
                tool_id=tool_call.id,
                tool_name=tool_call.function.name,
                tool_kwargs=tool_call.function.arguments,
            )
        )

    return tool_selections

```
 |  
| --- | --- |  
options: members: - HuggingFaceInferenceAPI
