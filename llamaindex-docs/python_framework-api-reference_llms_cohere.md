# Cohere
##  Cohere [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cohere/#llama_index.llms.cohere.Cohere "Permanent link")
Bases: `FunctionCallingLLM`
Cohere LLM.
Examples:
`pip install llama-index-llms-cohere`

```
fromllama_index.llms.cohereimport Cohere

llm = Cohere(model="command", api_key=api_key)
resp = llm.complete("Paul Graham is ")
print(resp)

```

Source code in `llama-index-integrations/llms/llama-index-llms-cohere/llama_index/llms/cohere/base.py`  
| 
```
 44
 45
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
```
 | 
```
classCohere(FunctionCallingLLM):
"""
    Cohere LLM.

    Examples:
        `pip install llama-index-llms-cohere`

        ```python
        from llama_index.llms.cohere import Cohere

        llm = Cohere(model="command", api_key=api_key)
        resp = llm.complete("Paul Graham is ")
        print(resp)
        ```

    """

    model: str = Field(description="The cohere model to use.")
    temperature: Optional[float] = Field(
        description="The temperature to use for sampling.", default=None
    )
    max_retries: int = Field(
        default=10, description="The maximum number of API retries."
    )
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the Cohere API."
    )
    max_tokens: int = Field(description="The maximum number of tokens to generate.")
    base_url: Optional[str] = Field(
        default=None, description="The endpoint to use. Defaults to the Cohere API."
    )
    _client: Any = PrivateAttr()
    _aclient: Any = PrivateAttr()

    def__init__(
        self,
        model: str = "command-r",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = 8192,
        timeout: Optional[float] = None,
        max_retries: int = 10,
        api_key: Optional[str] = None,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        base_url: Optional[str] = None,
    ) -> None:
        additional_kwargs = additional_kwargs or {}
        callback_manager = callback_manager or CallbackManager([])

        super().__init__(
            temperature=temperature,
            additional_kwargs=additional_kwargs,
            timeout=timeout,
            max_retries=max_retries,
            model=model,
            callback_manager=callback_manager,
            max_tokens=max_tokens,
            base_url=base_url,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )
        self._client = cohere.Client(
            api_key, base_url=self.base_url, client_name="llama_index"
        )
        self._aclient = cohere.AsyncClient(
            api_key, base_url=self.base_url, client_name="llama_index"
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "Cohere_LLM"

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=cohere_modelname_to_contextsize(self.model),
            num_output=self.max_tokens,
            is_chat_model=True,
            model_name=self.model,
            system_role=MessageRole.CHATBOT,
            is_function_calling_model=is_cohere_function_calling_model(self.model),
        )

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "model": self.model,
            "temperature": self.temperature,
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
        chat_history = chat_history or []

        if isinstance(user_msg, str):
            user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)

        if user_msg is not None:
            chat_history.append(user_msg)

        tools_cohere_format = format_to_cohere_tools(tools)
        return {
            "messages": chat_history,
            "tools": tools_cohere_format or [],
            # switch to tool_choice on V2
            **({"force_single_step": True} if tool_required else {}),
            **kwargs,
        }

    defget_tool_calls_from_response(
        self,
        response: "ChatResponse",
        error_on_no_tool_call: bool = False,
    ) -> List[ToolSelection]:
"""Predict and call the tool."""
        tool_calls: List[ToolCall] = (
            response.message.additional_kwargs.get("tool_calls", []) or []
        )

        if len(tool_calls)  1 and error_on_no_tool_call:
            raise ValueError(
                f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
            )

        tool_selections = []
        for tool_call in tool_calls:
            if not isinstance(tool_call, ToolCall):
                raise ValueError("Invalid tool_call object")
            tool_selections.append(
                ToolSelection(
                    tool_id=uuid.uuid4().hex[:],
                    tool_name=tool_call.name,
                    tool_kwargs=tool_call.parameters,
                )
            )

        return tool_selections

    defget_cohere_chat_request(
        self,
        messages: List[ChatMessage],
        *,
        connectors: Optional[List[Dict[str, str]]] = None,
        stop_sequences: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
"""
        Get the request for the Cohere chat API.

        Args:
            messages: The messages.
            connectors: The connectors.
            **kwargs: The keyword arguments.

        Returns:
            The request for the Cohere chat API.

        """
        additional_kwargs = messages[-1].additional_kwargs

        # cohere SDK will fail loudly if both connectors and documents are provided
        if additional_kwargs.get("documents", []) and documents and len(documents)  0:
            raise ValueError(
                "Received documents both as a keyword argument and as an prompt additional keyword argument. Please choose only one option."
            )

        messages, documents = remove_documents_from_messages(messages)

        tool_results: Optional[List[Dict[str, Any]]] = (
            _messages_to_cohere_tool_results_curr_chat_turn(messages)
            or kwargs.get("tool_results")
        )
        if not tool_results:
            tool_results = None

        chat_history = []
        temp_tool_results = []
        # if force_single_step is set to False, then only message is empty in request if there is tool call
        if not kwargs.get("force_single_step"):
            for i, message in enumerate(messages[:-1]):
                # If there are multiple tool messages, then we need to aggregate them into one single tool message to pass into chat history
                if message.role == MessageRole.TOOL:
                    temp_tool_results += _message_to_cohere_tool_results(messages, i)

                    if (i == len(messages) - 1) or messages[
                        i + 1
                    ].role != MessageRole.TOOL:
                        cohere_message = _get_message_cohere_format(
                            message, temp_tool_results
                        )
                        chat_history.append(cohere_message)
                        temp_tool_results = []
                else:
                    chat_history.append(_get_message_cohere_format(message, None))

            message_str = "" if tool_results else messages[-1].content

        else:
            message_str = ""
            # if force_single_step is set to True, then message is the last human message in the conversation
            for message in messages[:-1]:
                if message.role in (
                    MessageRole.CHATBOT,
                    MessageRole.ASSISTANT,
                ) and message.additional_kwargs.get("tool_calls"):
                    continue

                # If there are multiple tool messages, then we need to aggregate them into one single tool message to pass into chat history
                if message.role == MessageRole.TOOL:
                    temp_tool_results += _message_to_cohere_tool_results(messages, i)

                    if (i == len(messages) - 1) or messages[
                        i + 1
                    ].role != MessageRole.TOOL:
                        cohere_message = _get_message_cohere_format(
                            message, temp_tool_results
                        )
                        chat_history.append(cohere_message)
                        temp_tool_results = []
                else:
                    chat_history.append(_get_message_cohere_format(message, None))
            # Add the last human message in the conversation to the message string
            for message in messages[::-1]:
                if (message.role == MessageRole.USER) and (message.content):
                    message_str = message.content
                    break

        req = {
            "message": message_str,
            "chat_history": chat_history,
            "tool_results": tool_results,
            "documents": documents,
            "connectors": connectors,
            "stop_sequences": stop_sequences,
            **kwargs,
        }
        return {k: v for k, v in req.items() if v is not None}

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        all_kwargs = self._get_all_kwargs(**kwargs)

        chat_request = self.get_cohere_chat_request(messages=messages, **all_kwargs)

        if all_kwargs["model"] not in CHAT_MODELS:
            raise ValueError(f"{all_kwargs['model']} not supported for chat")

        if "stream" in all_kwargs:
            warnings.warn(
                "Parameter `stream` is not supported by the `chat` method."
                "Use the `stream_chat` method instead"
            )

        response = completion_with_retry(
            client=self._client, max_retries=self.max_retries, chat=True, **chat_request
        )
        if not isinstance(response, cohere.NonStreamedChatResponse):
            tool_calls = response.get("tool_calls")
            content = response.get("text")
            response_raw = response

        else:
            tool_calls = response.tool_calls
            content = response.text
            response_raw = response.__dict__

        return ChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT,
                content=content,
                additional_kwargs={"tool_calls": tool_calls},
            ),
            raw=response_raw,
        )

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        all_kwargs = self._get_all_kwargs(**kwargs)
        if "stream" in all_kwargs:
            warnings.warn(
                "Parameter `stream` is not supported by the `chat` method."
                "Use the `stream_chat` method instead"
            )

        response = completion_with_retry(
            client=self._client,
            max_retries=self.max_retries,
            chat=False,
            prompt=prompt,
            **all_kwargs,
        )

        return CompletionResponse(
            text=response.generations[0].text,
            raw=response.__dict__,
        )

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        all_kwargs = self._get_all_kwargs(**kwargs)
        all_kwargs["stream"] = True
        if all_kwargs["model"] not in CHAT_MODELS:
            raise ValueError(f"{all_kwargs['model']} not supported for chat")

        chat_request = self.get_cohere_chat_request(messages=messages, **all_kwargs)

        response = completion_with_retry(
            client=self._client, max_retries=self.max_retries, chat=True, **chat_request
        )

        defgen() -> ChatResponseGen:
            content = ""
            role = MessageRole.ASSISTANT
            for r in response:
                if "text" in r.__dict__:
                    content_delta = r.text
                else:
                    content_delta = ""
                content += content_delta
                yield ChatResponse(
                    message=ChatMessage(role=role, content=content),
                    delta=content_delta,
                    raw=r.__dict__,
                )

        return gen()

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        all_kwargs = self._get_all_kwargs(**kwargs)
        all_kwargs["stream"] = True

        response = completion_with_retry(
            client=self._client,
            max_retries=self.max_retries,
            chat=False,
            prompt=prompt,
            **all_kwargs,
        )

        defgen() -> CompletionResponseGen:
            content = ""
            for r in response:
                content_delta = r.text
                content += content_delta
                yield CompletionResponse(
                    text=content, delta=content_delta, raw=r._asdict()
                )

        return gen()

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        all_kwargs = self._get_all_kwargs(**kwargs)
        if all_kwargs["model"] not in CHAT_MODELS:
            raise ValueError(f"{all_kwargs['model']} not supported for chat")
        if "stream" in all_kwargs:
            warnings.warn(
                "Parameter `stream` is not supported by the `chat` method."
                "Use the `stream_chat` method instead"
            )

        chat_request = self.get_cohere_chat_request(messages=messages, **all_kwargs)

        response = await acompletion_with_retry(
            aclient=self._aclient,
            max_retries=self.max_retries,
            chat=True,
            **chat_request,
        )

        if not isinstance(response, cohere.NonStreamedChatResponse):
            tool_calls = response.get("tool_calls")
            content = response.get("text")
            response_raw = response

        else:
            tool_calls = response.tool_calls
            content = response.text
            response_raw = response.__dict__

        if not isinstance(response, cohere.NonStreamedChatResponse):
            tool_calls = response.get("tool_calls")
            content = response.get("text")
            response_raw = response

        else:
            tool_calls = response.tool_calls
            content = response.text
            response_raw = response.__dict__

        return ChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT,
                content=content,
                additional_kwargs={"tool_calls": tool_calls},
            ),
            raw=response_raw,
        )

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        all_kwargs = self._get_all_kwargs(**kwargs)
        if "stream" in all_kwargs:
            warnings.warn(
                "Parameter `stream` is not supported by the `chat` method."
                "Use the `stream_chat` method instead"
            )

        response = await acompletion_with_retry(
            aclient=self._aclient,
            max_retries=self.max_retries,
            chat=False,
            prompt=prompt,
            **all_kwargs,
        )

        return CompletionResponse(
            text=response.generations[0].text,
            raw=response.__dict__,
        )

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        all_kwargs = self._get_all_kwargs(**kwargs)
        all_kwargs["stream"] = True
        if all_kwargs["model"] not in CHAT_MODELS:
            raise ValueError(f"{all_kwargs['model']} not supported for chat")

        chat_request = self.get_cohere_chat_request(messages, **all_kwargs)

        response = completion_with_retry(
            client=self._client, max_retries=self.max_retries, chat=True, **chat_request
        )

        async defgen() -> ChatResponseAsyncGen:
            content = ""
            role = MessageRole.ASSISTANT
            async for r in response:
                if "text" in r.__dict__:
                    content_delta = r.text
                else:
                    content_delta = ""
                content += content_delta
                yield ChatResponse(
                    message=ChatMessage(role=role, content=content),
                    delta=content_delta,
                    raw=r.__dict__,
                )

        return gen()

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        all_kwargs = self._get_all_kwargs(**kwargs)
        all_kwargs["stream"] = True

        response = await acompletion_with_retry(
            aclient=self._aclient,
            max_retries=self.max_retries,
            chat=False,
            prompt=prompt,
            **all_kwargs,
        )

        async defgen() -> CompletionResponseAsyncGen:
            content = ""
            async for r in response:
                content_delta = r.text
                content += content_delta
                yield CompletionResponse(
                    text=content, delta=content_delta, raw=r._asdict()
                )

        return gen()

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cohere/#llama_index.llms.cohere.Cohere.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-cohere/llama_index/llms/cohere/base.py`  
| 
```
120
121
122
123
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "Cohere_LLM"

```
 |  
| --- | --- |  
###  get_tool_calls_from_response [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cohere/#llama_index.llms.cohere.Cohere.get_tool_calls_from_response "Permanent link")

```
get_tool_calls_from_response(
    response: ,
    error_on_no_tool_call:  = False,
) -> []

```

Predict and call the tool.
Source code in `llama-index-integrations/llms/llama-index-llms-cohere/llama_index/llms/cohere/base.py`  
| 
```
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
```
 | 
```
defget_tool_calls_from_response(
    self,
    response: "ChatResponse",
    error_on_no_tool_call: bool = False,
) -> List[ToolSelection]:
"""Predict and call the tool."""
    tool_calls: List[ToolCall] = (
        response.message.additional_kwargs.get("tool_calls", []) or []
    )

    if len(tool_calls)  1 and error_on_no_tool_call:
        raise ValueError(
            f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
        )

    tool_selections = []
    for tool_call in tool_calls:
        if not isinstance(tool_call, ToolCall):
            raise ValueError("Invalid tool_call object")
        tool_selections.append(
            ToolSelection(
                tool_id=uuid.uuid4().hex[:],
                tool_name=tool_call.name,
                tool_kwargs=tool_call.parameters,
            )
        )

    return tool_selections

```
 |  
| --- | --- |  
###  get_cohere_chat_request [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cohere/#llama_index.llms.cohere.Cohere.get_cohere_chat_request "Permanent link")

```
get_cohere_chat_request(
    messages: [],
    *,
    connectors: Optional[[[, ]]] = None,
    stop_sequences: Optional[[]] = None,
    **kwargs: 
) -> [, ]

```

Get the request for the Cohere chat API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `List[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  The messages.  |  _required_  |  
|  `connectors`  |  `Optional[List[Dict[str, str]]]`  |  The connectors.  |  `None`  |  
|  `**kwargs`  |  The keyword arguments.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Any]`  |  The request for the Cohere chat API.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-cohere/llama_index/llms/cohere/base.py`  
| 
```
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
```
 | 
```
defget_cohere_chat_request(
    self,
    messages: List[ChatMessage],
    *,
    connectors: Optional[List[Dict[str, str]]] = None,
    stop_sequences: Optional[List[str]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
"""
    Get the request for the Cohere chat API.

    Args:
        messages: The messages.
        connectors: The connectors.
        **kwargs: The keyword arguments.

    Returns:
        The request for the Cohere chat API.

    """
    additional_kwargs = messages[-1].additional_kwargs

    # cohere SDK will fail loudly if both connectors and documents are provided
    if additional_kwargs.get("documents", []) and documents and len(documents)  0:
        raise ValueError(
            "Received documents both as a keyword argument and as an prompt additional keyword argument. Please choose only one option."
        )

    messages, documents = remove_documents_from_messages(messages)

    tool_results: Optional[List[Dict[str, Any]]] = (
        _messages_to_cohere_tool_results_curr_chat_turn(messages)
        or kwargs.get("tool_results")
    )
    if not tool_results:
        tool_results = None

    chat_history = []
    temp_tool_results = []
    # if force_single_step is set to False, then only message is empty in request if there is tool call
    if not kwargs.get("force_single_step"):
        for i, message in enumerate(messages[:-1]):
            # If there are multiple tool messages, then we need to aggregate them into one single tool message to pass into chat history
            if message.role == MessageRole.TOOL:
                temp_tool_results += _message_to_cohere_tool_results(messages, i)

                if (i == len(messages) - 1) or messages[
                    i + 1
                ].role != MessageRole.TOOL:
                    cohere_message = _get_message_cohere_format(
                        message, temp_tool_results
                    )
                    chat_history.append(cohere_message)
                    temp_tool_results = []
            else:
                chat_history.append(_get_message_cohere_format(message, None))

        message_str = "" if tool_results else messages[-1].content

    else:
        message_str = ""
        # if force_single_step is set to True, then message is the last human message in the conversation
        for message in messages[:-1]:
            if message.role in (
                MessageRole.CHATBOT,
                MessageRole.ASSISTANT,
            ) and message.additional_kwargs.get("tool_calls"):
                continue

            # If there are multiple tool messages, then we need to aggregate them into one single tool message to pass into chat history
            if message.role == MessageRole.TOOL:
                temp_tool_results += _message_to_cohere_tool_results(messages, i)

                if (i == len(messages) - 1) or messages[
                    i + 1
                ].role != MessageRole.TOOL:
                    cohere_message = _get_message_cohere_format(
                        message, temp_tool_results
                    )
                    chat_history.append(cohere_message)
                    temp_tool_results = []
            else:
                chat_history.append(_get_message_cohere_format(message, None))
        # Add the last human message in the conversation to the message string
        for message in messages[::-1]:
            if (message.role == MessageRole.USER) and (message.content):
                message_str = message.content
                break

    req = {
        "message": message_str,
        "chat_history": chat_history,
        "tool_results": tool_results,
        "documents": documents,
        "connectors": connectors,
        "stop_sequences": stop_sequences,
        **kwargs,
    }
    return {k: v for k, v in req.items() if v is not None}

```
 |  
| --- | --- |  
options: members: - Cohere
