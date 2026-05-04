# Azure inference
##  AzureAICompletionsModel [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/azure_inference/#llama_index.llms.azure_inference.AzureAICompletionsModel "Permanent link")
Bases: `FunctionCallingLLM`
Azure AI model inference for LLM.
Examples:

```
fromllama_index.coreimport Settings
fromllama_index.core.llmsimport ChatMessage
fromllama_index.llms.azure_inferenceimport AzureAICompletionsModel

llm = AzureAICompletionsModel(
    endpoint="https://[your-endpoint].inference.ai.azure.com",
    credential="your-api-key",
    temperature=0
)

# If using Microsoft Entra ID authentication, you can create the
# client as follows:
#
# from azure.identity import DefaultAzureCredential
#
# llm = AzureAICompletionsModel(
#     endpoint="https://[your-endpoint].inference.ai.azure.com",
#     credential=DefaultAzureCredential()
# )
#
# # If you plan to use asynchronous calling, make sure to use the async
# # credentials as follows:
#
# from azure.identity.aio import DefaultAzureCredential as DefaultAzureCredentialAsync
#
# llm = AzureAICompletionsModel(
#     endpoint="https://[your-endpoint].inference.ai.azure.com",
#     credential=DefaultAzureCredentialAsync()
# )

resp = llm.chat(
    messages=ChatMessage(role="user", content="Who is Paul Graham?")
)

print(resp)

# Once the client is instantiated, you can set the context to use the model
Settings.llm = llm

```

Source code in `llama-index-integrations/llms/llama-index-llms-azure-inference/llama_index/llms/azure_inference/base.py`  
| 
```
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
```
 | 
```
classAzureAICompletionsModel(FunctionCallingLLM):
"""
    Azure AI model inference for LLM.

    Examples:
        ```python
        from llama_index.core import Settings
        from llama_index.core.llms import ChatMessage
        from llama_index.llms.azure_inference import AzureAICompletionsModel

        llm = AzureAICompletionsModel(
            endpoint="https://[your-endpoint].inference.ai.azure.com",
            credential="your-api-key",
            temperature=0


        # If using Microsoft Entra ID authentication, you can create the
        # client as follows:

        # from azure.identity import DefaultAzureCredential

        # llm = AzureAICompletionsModel(
        #     endpoint="https://[your-endpoint].inference.ai.azure.com",
        #     credential=DefaultAzureCredential()
        # )

        # # If you plan to use asynchronous calling, make sure to use the async
        # # credentials as follows:

        # from azure.identity.aio import DefaultAzureCredential as DefaultAzureCredentialAsync

        # llm = AzureAICompletionsModel(
        #     endpoint="https://[your-endpoint].inference.ai.azure.com",
        #     credential=DefaultAzureCredentialAsync()
        # )

        resp = llm.chat(
            messages=ChatMessage(role="user", content="Who is Paul Graham?")


        print(resp)

        # Once the client is instantiated, you can set the context to use the model
        Settings.llm = llm
        ```

    """

    model_config = ConfigDict(protected_namespaces=())
    model_name: Optional[str] = Field(
        default=None,
        description="The model id to use. Optional for endpoints running a single model.",
    )
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        description="The temperature to use for sampling.",
        ge=0.0,
        le=1.0,
    )
    max_tokens: Optional[int] = Field(
        default=None,
        description="The maximum number of tokens to generate.",
        gt=0,
    )
    seed: str = Field(default=None, description="The random seed to use for sampling.")
    model_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional kwargs model parameters.",
    )

    _client: ChatCompletionsClient = PrivateAttr()
    _async_client_class: Type[ChatCompletionsClientAsync] = PrivateAttr()
    _async_client_kwargs: Dict[str, Any] = PrivateAttr()
    _model_name: str = PrivateAttr(None)
    _model_type: str = PrivateAttr(None)
    _model_provider: str = PrivateAttr(None)

    def__init__(
        self,
        endpoint: str = None,
        credential: Union[str, AzureKeyCredential, "TokenCredential"] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: Optional[int] = None,
        model_name: Optional[str] = None,
        api_version: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        client_kwargs: Dict[str, Any] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        client_kwargs = dict(client_kwargs or {})
        callback_manager = callback_manager or CallbackManager([])

        endpoint = get_from_param_or_env(
            "endpoint", endpoint, "AZURE_INFERENCE_ENDPOINT", None
        )
        credential = get_from_param_or_env(
            "credential", credential, "AZURE_INFERENCE_CREDENTIAL", None
        )
        credential = (
            AzureKeyCredential(credential)
            if isinstance(credential, str)
            else credential
        )

        if not endpoint:
            raise ValueError(
                "You must provide an endpoint to use the Azure AI model inference LLM."
                "Pass the endpoint as a parameter or set the AZURE_INFERENCE_ENDPOINT"
                "environment variable."
            )

        if not credential:
            raise ValueError(
                "You must provide an credential to use the Azure AI model inference LLM."
                "Pass the credential as a parameter or set the AZURE_INFERENCE_CREDENTIAL"
            )

        if api_version:
            client_kwargs["api_version"] = api_version

        super().__init__(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
            **kwargs,
        )

        self._client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=credential,
            user_agent="llamaindex",
            **client_kwargs,
        )

        # Save async client config so each async request can create
        # and close its own short-lived client.
        self._async_client_class = ChatCompletionsClientAsync
        self._async_client_kwargs = dict(
            endpoint=endpoint,
            credential=credential,
            user_agent="llamaindex",
            **client_kwargs,
        )

    def_create_async_client(self) -> ChatCompletionsClientAsync:
        return self._async_client_class(**self._async_client_kwargs)

    @asynccontextmanager
    async def_get_request_async_client(
        self,
    ) -> AsyncIterator[ChatCompletionsClientAsync]:
        async with self._create_async_client() as async_client:
            yield async_client

    @classmethod
    defclass_name(cls) -> str:
        return "AzureAICompletionsModel"

    @property
    defmetadata(self) -> LLMMetadata:
        if not self._model_name:
            model_info = None
            try:
                # Get model info from the endpoint. This method may not be supported by all
                # endpoints.
                model_info = self._client.get_model_info()
            except HttpResponseError:
                logger.warning(
                    f"Endpoint '{self._client._config.endpoint}' does not support model metadata retrieval. "
                    "Failed to get model info for method `metadata()`."
                )
            finally:
                if model_info:
                    self._model_name = model_info.get("model_name", None)
                    self._model_type = model_info.get("model_type", None)
                    self._model_provider = model_info.get("model_provider_name", None)
                else:
                    self._model_name = self.model_name or "unknown"
                    self._model_type = "unknown"
                    self._model_provider = "unknown"

        return LLMMetadata(
            is_chat_model=self._model_type == "chat-completions",
            model_name=self._model_name,
            model_type=self._model_type,
            model_provider=self._model_provider,
        )

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if self.model_name:
            base_kwargs["model"] = self.model_name

        return {
            **base_kwargs,
            **self.model_kwargs,
        }

    def_get_all_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        return {
            **self._model_kwargs,
            **kwargs,
        }

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        messages = to_inference_message(messages)
        all_kwargs = self._get_all_kwargs(**kwargs)
        response = self._client.complete(messages=messages, **all_kwargs)

        response_message = from_inference_message(response.choices[0].message)

        return ChatResponse(
            message=response_message,
            raw=response.as_dict(),
        )

    def_to_azure_tool_choice(
        self, tool_required: bool
    ) -> Optional[
        Union[str, ChatCompletionsToolChoicePreset, ChatCompletionsNamedToolChoice]
    ]:
        if tool_required:
            return ChatCompletionsToolChoicePreset.REQUIRED
        else:
            return ChatCompletionsToolChoicePreset.AUTO

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
        messages = to_inference_message(messages)
        all_kwargs = self._get_all_kwargs(**kwargs)

        response = self._client.complete(messages=messages, stream=True, **all_kwargs)

        defgen() -> ChatResponseGen:
            content = ""
            role = MessageRole.ASSISTANT
            for chunk in response:
                content_delta = (
                    chunk.choices[0].delta.content if len(chunk.choices)  0 else None
                )
                if content_delta is None:
                    continue
                content += content_delta
                yield ChatResponse(
                    message=ChatMessage(role=role, content=content),
                    delta=content_delta,
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
        messages = to_inference_message(messages)
        all_kwargs = self._get_all_kwargs(**kwargs)
        async with self._get_request_async_client() as async_client:
            response = await async_client.complete(messages=messages, **all_kwargs)

        response_message = from_inference_message(response.choices[0].message)

        return ChatResponse(
            message=response_message,
            raw=response.as_dict(),
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
        messages = to_inference_message(messages)
        all_kwargs = self._get_all_kwargs(**kwargs)

        async defstream_gen() -> ChatResponseAsyncGen:
            async with self._get_request_async_client() as async_client:
                response = await async_client.complete(
                    messages=messages, stream=True, **all_kwargs
                )

                content = ""
                role = MessageRole.ASSISTANT
                async for chunk in response:
                    content_delta = (
                        chunk.choices[0].delta.content if chunk.choices else None
                    )
                    if content_delta is None:
                        continue
                    content += content_delta
                    yield ChatResponse(
                        message=ChatMessage(role=role, content=content),
                        delta=content_delta,
                        raw=chunk,
                    )

        return stream_gen()

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        astream_complete_fn = astream_chat_to_completion_decorator(self.astream_chat)
        return await astream_complete_fn(prompt, stream=True, **kwargs)

    defchat_with_tools(
        self,
        tools: List["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        tool_required: bool = False,
        **kwargs: Any,
    ) -> ChatResponse:
"""Predict and call the tool."""
        # Azure AI model inference uses the same openai tool format
        tool_specs = [
            tool.metadata.to_openai_tool(skip_length_check=True) for tool in tools
        ]

        if isinstance(user_msg, str):
            user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)

        messages = chat_history or []
        if user_msg:
            messages.append(user_msg)

        response = self.chat(
            messages,
            tools=tool_specs,
            tool_choice=self._to_azure_tool_choice(tool_required),
            **kwargs,
        )
        if not allow_parallel_tool_calls:
            force_single_tool_call(response)
        return response

    async defachat_with_tools(
        self,
        tools: List["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        tool_required: bool = False,
        **kwargs: Any,
    ) -> ChatResponse:
"""Predict and call the tool."""
        # Azure AI model inference uses the same openai tool format
        tool_specs = [
            tool.metadata.to_openai_tool(skip_length_check=True) for tool in tools
        ]

        if isinstance(user_msg, str):
            user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)

        messages = chat_history or []
        if user_msg:
            messages.append(user_msg)

        response = await self.achat(
            messages,
            tools=tool_specs,
            tool_choice=self._to_azure_tool_choice(tool_required),
            **kwargs,
        )
        if not allow_parallel_tool_calls:
            force_single_tool_call(response)
        return response

    defget_tool_calls_from_response(
        self,
        response: "AgentChatResponse",
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
            if not isinstance(tool_call, ChatCompletionsToolCall):
                raise ValueError("Invalid tool_call object")
            if tool_call.type != "function":
                raise ValueError(
                    "Invalid tool type. Only `function` is supported but `{tool_call.type}` was received."
                )
            argument_dict = json.loads(tool_call.function.arguments)

            tool_selections.append(
                ToolSelection(
                    tool_id=tool_call.id,
                    tool_name=tool_call.function.name,
                    tool_kwargs=argument_dict,
                )
            )

        return tool_selections

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
"""Prepare the arguments needed to let the LLM chat with tools."""
        chat_history = chat_history or []

        if isinstance(user_msg, str):
            user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)
            chat_history.append(user_msg)

        tool_dicts = [to_inference_tool(tool.metadata) for tool in tools]

        return {
            "messages": chat_history,
            "tools": tool_dicts or None,
            "tool_choice": self._to_azure_tool_choice(tool_required),
            **kwargs,
        }

```
 |  
| --- | --- |  
###  chat_with_tools [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/azure_inference/#llama_index.llms.azure_inference.AzureAICompletionsModel.chat_with_tools "Permanent link")

```
chat_with_tools(
    tools: [],
    user_msg: Optional[Union[, ]] = None,
    chat_history: Optional[[]] = None,
    verbose:  = False,
    allow_parallel_tool_calls:  = False,
    tool_required:  = False,
    **kwargs: 
) -> 

```

Predict and call the tool.
Source code in `llama-index-integrations/llms/llama-index-llms-azure-inference/llama_index/llms/azure_inference/base.py`  
| 
```
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
```
 | 
```
defchat_with_tools(
    self,
    tools: List["BaseTool"],
    user_msg: Optional[Union[str, ChatMessage]] = None,
    chat_history: Optional[List[ChatMessage]] = None,
    verbose: bool = False,
    allow_parallel_tool_calls: bool = False,
    tool_required: bool = False,
    **kwargs: Any,
) -> ChatResponse:
"""Predict and call the tool."""
    # Azure AI model inference uses the same openai tool format
    tool_specs = [
        tool.metadata.to_openai_tool(skip_length_check=True) for tool in tools
    ]

    if isinstance(user_msg, str):
        user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)

    messages = chat_history or []
    if user_msg:
        messages.append(user_msg)

    response = self.chat(
        messages,
        tools=tool_specs,
        tool_choice=self._to_azure_tool_choice(tool_required),
        **kwargs,
    )
    if not allow_parallel_tool_calls:
        force_single_tool_call(response)
    return response

```
 |  
| --- | --- |  
###  achat_with_tools [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/azure_inference/#llama_index.llms.azure_inference.AzureAICompletionsModel.achat_with_tools "Permanent link")

```
achat_with_tools(
    tools: [],
    user_msg: Optional[Union[, ]] = None,
    chat_history: Optional[[]] = None,
    verbose:  = False,
    allow_parallel_tool_calls:  = False,
    tool_required:  = False,
    **kwargs: 
) -> 

```

Predict and call the tool.
Source code in `llama-index-integrations/llms/llama-index-llms-azure-inference/llama_index/llms/azure_inference/base.py`  
| 
```
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
```
 | 
```
async defachat_with_tools(
    self,
    tools: List["BaseTool"],
    user_msg: Optional[Union[str, ChatMessage]] = None,
    chat_history: Optional[List[ChatMessage]] = None,
    verbose: bool = False,
    allow_parallel_tool_calls: bool = False,
    tool_required: bool = False,
    **kwargs: Any,
) -> ChatResponse:
"""Predict and call the tool."""
    # Azure AI model inference uses the same openai tool format
    tool_specs = [
        tool.metadata.to_openai_tool(skip_length_check=True) for tool in tools
    ]

    if isinstance(user_msg, str):
        user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)

    messages = chat_history or []
    if user_msg:
        messages.append(user_msg)

    response = await self.achat(
        messages,
        tools=tool_specs,
        tool_choice=self._to_azure_tool_choice(tool_required),
        **kwargs,
    )
    if not allow_parallel_tool_calls:
        force_single_tool_call(response)
    return response

```
 |  
| --- | --- |  
###  get_tool_calls_from_response [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/azure_inference/#llama_index.llms.azure_inference.AzureAICompletionsModel.get_tool_calls_from_response "Permanent link")

```
get_tool_calls_from_response(
    response: ,
    error_on_no_tool_call:  = True,
) -> []

```

Predict and call the tool.
Source code in `llama-index-integrations/llms/llama-index-llms-azure-inference/llama_index/llms/azure_inference/base.py`  
| 
```
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
```
 | 
```
defget_tool_calls_from_response(
    self,
    response: "AgentChatResponse",
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
        if not isinstance(tool_call, ChatCompletionsToolCall):
            raise ValueError("Invalid tool_call object")
        if tool_call.type != "function":
            raise ValueError(
                "Invalid tool type. Only `function` is supported but `{tool_call.type}` was received."
            )
        argument_dict = json.loads(tool_call.function.arguments)

        tool_selections.append(
            ToolSelection(
                tool_id=tool_call.id,
                tool_name=tool_call.function.name,
                tool_kwargs=argument_dict,
            )
        )

    return tool_selections

```
 |  
| --- | --- |  
options: members: - AzureAICompletionsModel
