# Litellm
##  LiteLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/litellm/#llama_index.llms.litellm.LiteLLM "Permanent link")
Bases: `FunctionCallingLLM`
LiteLLM.
Examples:
`pip install llama-index-llms-litellm`

```
importos
fromllama_index.core.llmsimport ChatMessage
fromllama_index.llms.litellmimport LiteLLM

# Set environment variables
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
os.environ["COHERE_API_KEY"] = "your-cohere-api-key"

# Define a chat message
message = ChatMessage(role="user", content="Hey! how's it going?")

# Initialize LiteLLM with the desired model
llm = LiteLLM(model="gpt-3.5-turbo")

# Call the chat method with the message
chat_response = llm.chat([message])

# Print the response
print(chat_response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-litellm/llama_index/llms/litellm/base.py`  
| 
```
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
```
 | 
```
classLiteLLM(FunctionCallingLLM):
"""
    LiteLLM.

    Examples:
        `pip install llama-index-llms-litellm`

        ```python
        import os
        from llama_index.core.llms import ChatMessage
        from llama_index.llms.litellm import LiteLLM

        # Set environment variables
        os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
        os.environ["COHERE_API_KEY"] = "your-cohere-api-key"

        # Define a chat message
        message = ChatMessage(role="user", content="Hey! how's it going?")

        # Initialize LiteLLM with the desired model
        llm = LiteLLM(model="gpt-3.5-turbo")

        # Call the chat method with the message
        chat_response = llm.chat([message])

        # Print the response
        print(chat_response)
        ```

    """

    model: str = Field(
        default=DEFAULT_LITELLM_MODEL,
        description=(
            "The LiteLLM model to use. "
            "For complete list of providers https://docs.litellm.ai/docs/providers"
        ),
    )
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        description="The temperature to use during generation.",
        ge=0.0,
        le=1.0,
    )
    max_tokens: Optional[int] = Field(
        description="The maximum number of tokens to generate.",
        gt=0,
    )
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional kwargs for the LLM API.",
        # for all inputs https://docs.litellm.ai/docs/completion/input
    )
    max_retries: int = Field(
        default=10, description="The maximum number of API retries."
    )

    _custom_llm_provider: Optional[str] = PrivateAttr(default=None)

    def__init__(
        self,
        model: str = DEFAULT_LITELLM_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: Optional[int] = None,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        max_retries: int = 10,
        api_key: Optional[str] = None,
        api_type: Optional[str] = None,
        api_base: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        **kwargs: Any,
    ) -> None:
        if "custom_llm_provider" in kwargs:
            if (
                kwargs["custom_llm_provider"] != "ollama"
                and kwargs["custom_llm_provider"] != "vllm"
            ):  # don't check keys for local models
                validate_litellm_api_key(api_key, api_type)
        else:  # by default assume it's a hosted endpoint
            validate_litellm_api_key(api_key, api_type)

        additional_kwargs = additional_kwargs or {}
        if api_key is not None:
            additional_kwargs["api_key"] = api_key
        if api_type is not None:
            additional_kwargs["api_type"] = api_type
        if api_base is not None:
            additional_kwargs["api_base"] = api_base

        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            additional_kwargs=additional_kwargs,
            max_retries=max_retries,
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
            **kwargs,
        )

        self._custom_llm_provider = kwargs.get("custom_llm_provider")

    def_get_model_name(self) -> str:
        model_name = self.model
        if "ft-" in model_name:  # legacy fine-tuning
            model_name = model_name.split(":")[0]
        elif model_name.startswith("ft:"):
            model_name = model_name.split(":")[1]

        return model_name

    @classmethod
    defclass_name(cls) -> str:
        return "litellm_llm"

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=openai_modelname_to_contextsize(self._get_model_name()),
            num_output=self.max_tokens or -1,
            is_chat_model=True,
            is_function_calling_model=is_function_calling_model(
                self._get_model_name(), self._custom_llm_provider
            ),
            model_name=self.model,
        )

    def_prepare_chat_with_tools(
        self,
        tools: List[BaseTool],
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
            "parallel_tool_calls": allow_parallel_tool_calls,
            "tool_choice": "required" if tool_required else "auto",
            **kwargs,
        }

    def_validate_chat_with_tools_response(
        self,
        response: ChatResponse,
        tools: List[BaseTool],
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
            if tool_call["type"] != "function" or "function" not in tool_call:
                raise ValueError(f"Invalid tool call of type {tool_call['type']}")

            function = tool_call.get("function", {})
            tool_name = function.get("name")
            arguments = function.get("arguments")

            # this should handle both complete and partial jsons
            try:
                if arguments:  # If arguments is not empty/None
                    argument_dict = json.loads(arguments)
                else:  # If arguments is None or empty string
                    argument_dict = {}
            except (ValueError, TypeError, JSONDecodeError):
                argument_dict = {}

            if tool_name:  # Only require tool_name, not arguments
                tool_selections.append(
                    ToolSelection(
                        tool_id=tool_call.get("id") or str(uuid.uuid4()),
                        tool_name=tool_name,
                        tool_kwargs=argument_dict,
                    )
                )
        if len(tool_selections) == 0 and error_on_no_tool_call:
            raise ValueError("No valid tool calls found.")

        return tool_selections

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        if self._is_chat_model:
            chat_fn = self._chat
        else:
            chat_fn = completion_to_chat_decorator(self._complete)
        return chat_fn(messages, **kwargs)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        if self._is_chat_model:
            stream_chat_fn = self._stream_chat
        else:
            stream_chat_fn = stream_completion_to_chat_decorator(self._stream_complete)
        return stream_chat_fn(messages, **kwargs)

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        # litellm assumes all llms are chat llms
        if self._is_chat_model:
            complete_fn = chat_to_completion_decorator(self._chat)
        else:
            complete_fn = self._complete

        return complete_fn(prompt, **kwargs)

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        if self._is_chat_model:
            stream_complete_fn = stream_chat_to_completion_decorator(self._stream_chat)
        else:
            stream_complete_fn = self._stream_complete
        return stream_complete_fn(prompt, **kwargs)

    @property
    def_is_chat_model(self) -> bool:
        # litellm assumes all llms are chat llms
        return True

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if self._custom_llm_provider:
            base_kwargs["custom_llm_provider"] = self._custom_llm_provider
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
        if not self._is_chat_model:
            raise ValueError("This model is not a chat model.")

        message_dicts = to_openai_message_dicts(messages)
        all_kwargs = self._get_all_kwargs(**kwargs)
        if "max_tokens" in all_kwargs and all_kwargs["max_tokens"] is None:
            all_kwargs.pop(
                "max_tokens"
            )  # don't send max_tokens == None, this throws errors for Non OpenAI providers

        response = completion_with_retry(
            is_chat_model=self._is_chat_model,
            max_retries=self.max_retries,
            messages=message_dicts,
            stream=False,
            **all_kwargs,
        )
        message_dict = response["choices"][0]["message"]
        message = from_litellm_message(message_dict)

        return ChatResponse(
            message=message,
            raw=response,
            additional_kwargs=self._get_response_token_counts(response),
        )

    def_stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        if not self._is_chat_model:
            raise ValueError("This model is not a chat model.")

        message_dicts = to_openai_message_dicts(messages)
        all_kwargs = self._get_all_kwargs(**kwargs)
        if "max_tokens" in all_kwargs and all_kwargs["max_tokens"] is None:
            all_kwargs.pop(
                "max_tokens"
            )  # don't send max_tokens == None, this throws errors for Non OpenAI providers

        defgen() -> ChatResponseGen:
            content = ""
            tool_calls: List[dict] = []
            for response in completion_with_retry(
                is_chat_model=self._is_chat_model,
                max_retries=self.max_retries,
                messages=message_dicts,
                stream=True,
                **all_kwargs,
            ):
                delta = response["choices"][0]["delta"]
                role = delta.get("role") or MessageRole.ASSISTANT
                content_delta = delta.get("content", "") or ""
                content += content_delta

                # Handle tool_calls delta
                tool_call_delta = delta.get("tool_calls", None)
                if tool_call_delta is not None and len(tool_call_delta)  0:
                    # Pass the entire list of tool call deltas
                    tool_calls = update_tool_calls(tool_calls, tool_call_delta)

                additional_kwargs = {}
                if tool_calls:
                    additional_kwargs["tool_calls"] = tool_calls

                yield ChatResponse(
                    message=ChatMessage(
                        role=role,
                        content=content,
                        additional_kwargs=additional_kwargs,
                    ),
                    delta=content_delta,
                    raw=response,
                    additional_kwargs=self._get_response_token_counts(response),
                )

        return gen()

    def_complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        raise NotImplementedError("litellm assumes all llms are chat llms.")

    def_stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        raise NotImplementedError("litellm assumes all llms are chat llms.")

    def_get_max_token_for_prompt(self, prompt: str) -> int:
        try:
            importtiktoken
        except ImportError:
            raise ImportError(
                "Please install tiktoken to use the max_tokens=None feature."
            )
        context_window = self.metadata.context_window
        try:
            encoding = tiktoken.encoding_for_model(self._get_model_name())
        except KeyError:
            encoding = encoding = tiktoken.get_encoding(
                "cl100k_base"
            )  # default to using cl10k_base
        tokens = encoding.encode(prompt)
        max_token = context_window - len(tokens)
        if max_token <= 0:
            raise ValueError(
                f"The prompt is too long for the model. "
                f"Please use a prompt that is less than {context_window} tokens."
            )
        return max_token

    def_get_response_token_counts(self, raw_response: Any) -> dict:
"""Get the token usage reported by the response."""
        if not isinstance(raw_response, dict):
            return {}

        usage = raw_response.get("usage", {})
        return {
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
        }

    # ===== Async Endpoints =====
    @llm_chat_callback()
    async defachat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
        achat_fn: Callable[..., Awaitable[ChatResponse]]
        if self._is_chat_model:
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
        if self._is_chat_model:
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
        if self._is_chat_model:
            acomplete_fn = achat_to_completion_decorator(self._achat)
        else:
            acomplete_fn = self._acomplete
        return await acomplete_fn(prompt, **kwargs)

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        if self._is_chat_model:
            astream_complete_fn = astream_chat_to_completion_decorator(
                self._astream_chat
            )
        else:
            astream_complete_fn = self._astream_complete
        return await astream_complete_fn(prompt, **kwargs)

    async def_achat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        if not self._is_chat_model:
            raise ValueError("This model is not a chat model.")

        message_dicts = to_openai_message_dicts(messages)
        all_kwargs = self._get_all_kwargs(**kwargs)
        response = await acompletion_with_retry(
            is_chat_model=self._is_chat_model,
            max_retries=self.max_retries,
            messages=message_dicts,
            stream=False,
            **all_kwargs,
        )
        message_dict = response["choices"][0]["message"]
        message = from_litellm_message(message_dict)

        return ChatResponse(
            message=message,
            raw=response,
            additional_kwargs=self._get_response_token_counts(response),
        )

    async def_astream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        if not self._is_chat_model:
            raise ValueError("This model is not a chat model.")

        message_dicts = to_openai_message_dicts(messages)
        all_kwargs = self._get_all_kwargs(**kwargs)

        async defgen() -> ChatResponseAsyncGen:
            content = ""
            tool_calls: List[dict] = []
            async for response in await acompletion_with_retry(
                is_chat_model=self._is_chat_model,
                max_retries=self.max_retries,
                messages=message_dicts,
                stream=True,
                **all_kwargs,
            ):
                delta = response["choices"][0]["delta"]
                role = delta.get("role") or MessageRole.ASSISTANT
                content_delta = delta.get("content", "") or ""
                content += content_delta

                # Handle tool_calls delta
                tool_call_delta = delta.get("tool_calls", None)
                if tool_call_delta is not None and len(tool_call_delta)  0:
                    # Pass the entire list of tool call deltas
                    tool_calls = update_tool_calls(tool_calls, tool_call_delta)

                additional_kwargs = {}
                if tool_calls:
                    additional_kwargs["tool_calls"] = tool_calls

                yield ChatResponse(
                    message=ChatMessage(
                        role=role,
                        content=content,
                        additional_kwargs=additional_kwargs,
                    ),
                    delta=content_delta,
                    raw=response,
                    additional_kwargs=self._get_response_token_counts(response),
                )

        return gen()

    async def_acomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        raise NotImplementedError("litellm assumes all llms are chat llms.")

    async def_astream_complete(
        self, prompt: str, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        raise NotImplementedError("litellm assumes all llms are chat llms.")

```
 |  
| --- | --- |  
###  get_tool_calls_from_response [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/litellm/#llama_index.llms.litellm.LiteLLM.get_tool_calls_from_response "Permanent link")

```
get_tool_calls_from_response(
    response: ,
    error_on_no_tool_call:  = True,
) -> []

```

Predict and call the tool.
Source code in `llama-index-integrations/llms/llama-index-llms-litellm/llama_index/llms/litellm/base.py`  
| 
```
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
```
 | 
```
defget_tool_calls_from_response(
    self,
    response: "ChatResponse",
    error_on_no_tool_call: bool = True,
) -> List[ToolSelection]:
"""Predict and call the tool."""
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
        if tool_call["type"] != "function" or "function" not in tool_call:
            raise ValueError(f"Invalid tool call of type {tool_call['type']}")

        function = tool_call.get("function", {})
        tool_name = function.get("name")
        arguments = function.get("arguments")

        # this should handle both complete and partial jsons
        try:
            if arguments:  # If arguments is not empty/None
                argument_dict = json.loads(arguments)
            else:  # If arguments is None or empty string
                argument_dict = {}
        except (ValueError, TypeError, JSONDecodeError):
            argument_dict = {}

        if tool_name:  # Only require tool_name, not arguments
            tool_selections.append(
                ToolSelection(
                    tool_id=tool_call.get("id") or str(uuid.uuid4()),
                    tool_name=tool_name,
                    tool_kwargs=argument_dict,
                )
            )
    if len(tool_selections) == 0 and error_on_no_tool_call:
        raise ValueError("No valid tool calls found.")

    return tool_selections

```
 |  
| --- | --- |  
options: members: - LiteLLM
