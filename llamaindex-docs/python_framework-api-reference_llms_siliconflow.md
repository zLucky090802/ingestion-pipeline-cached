# Siliconflow
##  SiliconFlow [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/siliconflow/#llama_index.llms.siliconflow.SiliconFlow "Permanent link")
Bases: `FunctionCallingLLM`
SiliconFlow LLM.
Visit https://siliconflow.cn/ to get more information about SiliconFlow.
Examples:
`pip install llama-index-llms-siliconflow`

```
fromllama_index.llms.siliconflowimport SiliconFlow

llm = SiliconFlow(api_key="YOUR API KEY")

response = llm.complete("who are you?")
print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-siliconflow/llama_index/llms/siliconflow/base.py`  
| 
```
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
```
 | 
```
classSiliconFlow(FunctionCallingLLM):
"""
    SiliconFlow LLM.

    Visit https://siliconflow.cn/ to get more information about SiliconFlow.

    Examples:
        `pip install llama-index-llms-siliconflow`

        ```python
        from llama_index.llms.siliconflow import SiliconFlow

        llm = SiliconFlow(api_key="YOUR API KEY")

        response = llm.complete("who are you?")
        print(response)
        ```

    """

    model: str = Field(
        default="deepseek-ai/DeepSeek-V2.5",
        description="The name of the model to query.",
    )
    api_key: Optional[str] = Field(
        default=None,
        description="The API key to use for the SiliconFlow API.",
    )
    base_url: str = Field(
        default=DEFAULT_SILICONFLOW_API_URL,
        description="The base URL for the SiliconFlow API.",
    )
    temperature: float = Field(
        default=0.7,
        description="Determines the degree of randomness in the response.",
        ge=0.0,
        le=1.0,
    )
    max_tokens: int = Field(
        default=512,
        description="The maximum number of tokens to generate.",
    )
    frequency_penalty: float = Field(default=0.5)
    timeout: float = Field(
        default=DEFAULT_REQUEST_TIMEOUT,
        description="The timeout for making http request to ZhipuAI API server",
    )
    stop: Optional[str] = Field(
        default=None,
        description="Up to 4 sequences where the API will stop generating further tokens.",
    )
    max_retries: int = Field(
        default=3,
        description="The maximum number of API retries.",
        ge=0,
    )

    _headers: Any = PrivateAttr()

    def__init__(
        self,
        api_key: str,
        model: str = "deepseek-ai/DeepSeek-V2.5",
        base_url: str = DEFAULT_SILICONFLOW_API_URL,
        temperature: float = 0.7,
        max_tokens: int = 512,
        frequency_penalty: float = 0.5,
        timeout: float = DEFAULT_REQUEST_TIMEOUT,
        stop: Optional[str] = None,
        max_retries: int = 3,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            model=model,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens,
            frequency_penalty=frequency_penalty,
            timeout=timeout,
            stop=stop,
            max_retries=max_retries,
            **kwargs,
        )

        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    @classmethod
    defclass_name(cls) -> str:
        return "SiliconFlow"

    @property
    defmetadata(self) -> LLMMetadata:
"""LLM metadata."""
        return LLMMetadata(
            context_window=DEFAULT_CONTEXT_WINDOW,
            num_output=DEFAULT_NUM_OUTPUTS,
            model_name=self.model,
            is_chat_model=True,
            is_function_calling_model=is_function_calling_llm(self.model),
        )

    @property
    defmodel_kwargs(self) -> Dict[str, Any]:
        return {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "frequency_penalty": self.frequency_penalty,
            "stop": self.stop,
        }

    def_convert_to_llm_messages(self, messages: Sequence[ChatMessage]) -> List:
        return [
            {
                "role": message.role.value,
                "content": message.content or "",
            }
            for message in messages
        ]

    def_prepare_chat_with_tools(
        self,
        tools: List["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        tool_required: bool = False,  # unsupported by SiliconFlow - https://docs.siliconflow.cn/en/api-reference/chat-completions/chat-completions
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
        response: Union[ChatResponse, CompletionResponse],
        error_on_no_tool_call: bool = True,
        **kwargs: Any,
    ) -> List[ToolSelection]:
"""Predict and call the tool."""
        if isinstance(response, ChatResponse):
            tool_calls = response.message.additional_kwargs.get("tool_calls", [])
        else:
            tool_calls = response.additional_kwargs.get("tool_calls", [])
        if len(tool_calls)  1:
            if error_on_no_tool_call:
                raise ValueError(
                    f"Expected at least one tool call, but got {len(tool_calls)} "
                    "tool calls."
                )
            return []

        tool_selections = []
        for tool_call in tool_calls:
            tool_selections.append(
                ToolSelection(
                    tool_id=tool_call["id"],
                    tool_name=tool_call["function"]["name"],
                    tool_kwargs=json.loads(tool_call["function"]["arguments"]),
                )
            )

        return tool_selections

    @llm_chat_callback()
    @llm_retry_decorator
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        messages_dict = self._convert_to_llm_messages(messages)
        response_format = kwargs.get("response_format", {"type": "text"})
        with requests.Session() as session:
            input_json = {
                "model": self.model,
                "messages": messages_dict,
                "stream": False,
                "n": 1,
                "tools": kwargs.get("tools"),
                "response_format": response_format,
                **self.model_kwargs,
            }
            response = session.post(
                self.base_url,
                json=input_json,
                headers=self._headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            response_json = response.json()
            message: dict = response_json["choices"][0]["message"]
            return ChatResponse(
                message=ChatMessage(
                    content=message["content"],
                    role=message["role"],
                    additional_kwargs={"tool_calls": message.get("tool_calls")},
                ),
                raw=response_json,
            )

    @llm_chat_callback()
    @llm_retry_decorator
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        messages_dict = self._convert_to_llm_messages(messages)
        response_format = kwargs.get("response_format", {"type": "text"})
        async with aiohttp.ClientSession() as session:
            input_json = {
                "model": self.model,
                "messages": messages_dict,
                "stream": False,
                "n": 1,
                "tools": kwargs.get("tools"),
                "response_format": response_format,
                **self.model_kwargs,
            }

            async with session.post(
                self.base_url,
                json=input_json,
                headers=self._headers,
                timeout=self.timeout,
            ) as response:
                response_json = await response.json()
                message: dict = response_json["choices"][0]["message"]
                response.raise_for_status()
                return ChatResponse(
                    message=ChatMessage(
                        content=message["content"],
                        role=message["role"],
                        additional_kwargs={"tool_calls": message.get("tool_calls")},
                    ),
                    raw=response_json,
                )

    @llm_chat_callback()
    @llm_retry_decorator
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        messages_dict = self._convert_to_llm_messages(messages)
        response_format = kwargs.get("response_format", {"type": "text"})

        defgen() -> ChatResponseGen:
            with requests.Session() as session:
                input_json = {
                    "model": self.model,
                    "messages": messages_dict,
                    "stream": True,
                    "n": 1,
                    "tools": kwargs.get("tools"),
                    "response_format": response_format,
                    **self.model_kwargs,
                }
                response = session.post(
                    self.base_url,
                    json=input_json,
                    headers=self._headers,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                response_txt = ""
                response_role = "assistant"
                for line in response.iter_lines():
                    line = cast(bytes, line).decode("utf-8")
                    if line.startswith("data:"):
                        if line.strip() == "data: [DONE]":
                            break
                        chunk_json = json.loads(line[5:])
                        delta: dict = chunk_json["choices"][0]["delta"]
                        delta_txt = delta["content"] or ""
                        response_role = delta.get("role") or response_role
                        response_txt += delta_txt
                        tool_calls = delta.get("tool_calls")
                        yield ChatResponse(
                            message=ChatMessage(
                                content=response_txt,
                                role=response_role,
                                additional_kwargs={"tool_calls": tool_calls},
                            ),
                            delta=delta_txt,
                            raw=chunk_json,
                        )

        return gen()

    @llm_chat_callback()
    @llm_retry_decorator
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        messages_dict = self._convert_to_llm_messages(messages)
        response_format = kwargs.get("response_format", {"type": "text"})

        async defgen() -> ChatResponseAsyncGen:
            async with aiohttp.ClientSession(trust_env=True) as session:
                input_json = {
                    "model": self.model,
                    "messages": messages_dict,
                    "stream": True,
                    "n": 1,
                    "tools": kwargs.get("tools"),
                    "response_format": response_format,
                    **self.model_kwargs,
                }
                async with session.post(
                    self.base_url,
                    json=input_json,
                    headers=self._headers,
                    timeout=self.timeout,
                ) as response:
                    response.raise_for_status()
                    response_txt = ""
                    response_role = "assistant"
                    async for line in response.content.iter_any():
                        line = cast(bytes, line).decode("utf-8")
                        chunks = list(filter(None, line.split("data: ")))
                        for chunk in chunks:
                            if chunk.strip() == "[DONE]":
                                break
                            chunk_json = json.loads(chunk)
                            delta: dict = chunk_json["choices"][0]["delta"]
                            response_role = delta.get("role") or response_role
                            delta_txt = delta["content"] or ""
                            response_txt += delta_txt
                            tool_calls = delta.get("tool_calls")
                            yield ChatResponse(
                                message=ChatMessage(
                                    content=response_txt,
                                    role=response_role,
                                    additional_kwargs={"tool_calls": tool_calls},
                                ),
                                delta=delta_txt,
                                raw=line,
                            )

        return gen()

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

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/siliconflow/#llama_index.llms.siliconflow.SiliconFlow.metadata "Permanent link")

```
metadata: 

```

LLM metadata.
###  get_tool_calls_from_response [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/siliconflow/#llama_index.llms.siliconflow.SiliconFlow.get_tool_calls_from_response "Permanent link")

```
get_tool_calls_from_response(
    response: Union[, ],
    error_on_no_tool_call:  = True,
    **kwargs: 
) -> []

```

Predict and call the tool.
Source code in `llama-index-integrations/llms/llama-index-llms-siliconflow/llama_index/llms/siliconflow/base.py`  
| 
```
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
```
 | 
```
defget_tool_calls_from_response(
    self,
    response: Union[ChatResponse, CompletionResponse],
    error_on_no_tool_call: bool = True,
    **kwargs: Any,
) -> List[ToolSelection]:
"""Predict and call the tool."""
    if isinstance(response, ChatResponse):
        tool_calls = response.message.additional_kwargs.get("tool_calls", [])
    else:
        tool_calls = response.additional_kwargs.get("tool_calls", [])
    if len(tool_calls)  1:
        if error_on_no_tool_call:
            raise ValueError(
                f"Expected at least one tool call, but got {len(tool_calls)} "
                "tool calls."
            )
        return []

    tool_selections = []
    for tool_call in tool_calls:
        tool_selections.append(
            ToolSelection(
                tool_id=tool_call["id"],
                tool_name=tool_call["function"]["name"],
                tool_kwargs=json.loads(tool_call["function"]["arguments"]),
            )
        )

    return tool_selections

```
 |  
| --- | --- |  
options: members: - SiliconFlow
