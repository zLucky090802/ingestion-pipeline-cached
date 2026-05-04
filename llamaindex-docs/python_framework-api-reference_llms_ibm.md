# Ibm
##  WatsonxLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/ibm/#llama_index.llms.ibm.WatsonxLLM "Permanent link")
Bases: `FunctionCallingLLM`
IBM watsonx.ai large language models.
Example
`pip install llama-index-llms-ibm`

```
fromllama_index.llms.ibmimport WatsonxLLM

watsonx_llm = WatsonxLLM(
    model_id="ibm/granite-4-h-small",
    url="https://us-south.ml.cloud.ibm.com",
    apikey="*****",
    project_id="*****",
)

```

Source code in `llama-index-integrations/llms/llama-index-llms-ibm/llama_index/llms/ibm/base.py`  
| 
```
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
```
 | 
```
classWatsonxLLM(FunctionCallingLLM):
"""
    IBM watsonx.ai large language models.

    Example:
        `pip install llama-index-llms-ibm`

        ```python
        from llama_index.llms.ibm import WatsonxLLM

        watsonx_llm = WatsonxLLM(
            model_id="ibm/granite-4-h-small",
            url="https://us-south.ml.cloud.ibm.com",
            apikey="*****",
            project_id="*****",

        ```

    """

    model_id: Optional[str] = Field(
        default=None, description="Type of model to use.", frozen=True
    )
    deployment_id: Optional[str] = Field(
        default=None, description="Id of deployed model to use.", frozen=True
    )

    temperature: Optional[float] = Field(
        default=None,
        description="The temperature to use for sampling.",
    )
    max_new_tokens: Optional[int] = Field(
        default=None,
        description="The maximum number of tokens to generate.",
    )
    additional_params: Optional[Dict[str, Any]] = Field(
        default_factory=None,
        description="Additional generation params for the watsonx.ai models.",
    )

    project_id: Optional[str] = Field(
        default=None,
        description="ID of the Watson Studio project.",
        frozen=True,
    )

    space_id: Optional[str] = Field(
        default=None, description="ID of the Watson Studio space.", frozen=True
    )

    url: Optional[SecretStr] = Field(
        default=None,
        description="Url to the IBM watsonx.ai for IBM Cloud or the IBM watsonx.ai software instance.",
        frozen=True,
    )

    apikey: Optional[SecretStr] = Field(
        default=None,
        description="API key to the IBM watsonx.ai for IBM Cloud or the IBM watsonx.ai software instance.",
        frozen=True,
    )

    token: Optional[SecretStr] = Field(
        default=None,
        description="Token to the IBM watsonx.ai software instance.",
        frozen=True,
    )

    password: Optional[SecretStr] = Field(
        default=None,
        description="Password to the IBM watsonx.ai software instance.",
        frozen=True,
    )

    username: Optional[SecretStr] = Field(
        default=None,
        description="Username to the IBM watsonx.ai software instance.",
        frozen=True,
    )

    instance_id: Optional[SecretStr] = Field(
        default=None,
        description="Instance_id of the IBM watsonx.ai software instance.",
        frozen=True,
        deprecated="The `instance_id` parameter is deprecated and will no longer be utilized for logging to the IBM watsonx.ai software instance.",
    )

    version: Optional[SecretStr] = Field(
        default=None,
        description="Version of the IBM watsonx.ai software instance.",
        frozen=True,
    )

    verify: Union[str, bool, None] = Field(
        default=None,
        description="""
        User can pass as verify one of following:
        the path to a CA_BUNDLE file
        the path of directory with certificates of trusted CAs
        True - default path to truststore will be taken
        False - no verification will be made
        """,
        frozen=True,
    )

    validate_model: bool = Field(
        default=True, description="Model id validation", frozen=True
    )

    _model: ModelInference = PrivateAttr()
    _client: Optional[APIClient] = PrivateAttr()
    _model_info: Optional[Dict[str, Any]] = PrivateAttr()
    _deployment_info: Optional[Dict[str, Any]] = PrivateAttr()
    _context_window: Optional[int] = PrivateAttr()
    _text_generation_params: Dict[str, Any] | None = PrivateAttr()

    def__init__(
        self,
        model_id: Optional[str] = None,
        deployment_id: Optional[str] = None,
        temperature: Optional[float] = None,
        max_new_tokens: Optional[int] = None,
        additional_params: Optional[Dict[str, Any]] = None,
        project_id: Optional[str] = None,
        space_id: Optional[str] = None,
        url: Optional[str] = None,
        apikey: Optional[str] = None,
        token: Optional[str] = None,
        password: Optional[str] = None,
        username: Optional[str] = None,
        version: Optional[str] = None,
        verify: Union[str, bool, None] = None,
        api_client: Optional[APIClient] = None,
        validate_model: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
"""
        Initialize LLM and watsonx.ai ModelInference.
        """
        callback_manager = callback_manager or CallbackManager([])
        additional_params = additional_params or {}

        creds = (
            resolve_watsonx_credentials(
                url=url,
                apikey=apikey,
                token=token,
                username=username,
                password=password,
            )
            if not isinstance(api_client, APIClient)
            else {}
        )

        super().__init__(
            model_id=model_id,
            deployment_id=deployment_id,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            additional_params=additional_params,
            project_id=project_id,
            space_id=space_id,
            url=creds.get("url"),
            apikey=creds.get("apikey"),
            token=creds.get("token"),
            password=creds.get("password"),
            username=creds.get("username"),
            version=version,
            verify=verify,
            _client=api_client,
            validate_model=validate_model,
            callback_manager=callback_manager,
            **kwargs,
        )
        self._context_window = kwargs.get("context_window")

        generation_params = {}
        if self.temperature is not None:
            generation_params["temperature"] = self.temperature
        if self.max_new_tokens is not None:
            generation_params["max_new_tokens"] = self.max_new_tokens

        generation_params = {**generation_params, **additional_params}

        if generation_params:
            self._text_generation_params, _ = self._split_generation_params(
                generation_params
            )
        else:
            self._text_generation_params = None

        self._client = api_client
        self._model = ModelInference(
            model_id=model_id,
            deployment_id=deployment_id,
            credentials=(
                Credentials.from_dict(
                    {
                        key: value.get_secret_value() if value else None
                        for key, value in self._get_credential_kwargs().items()
                    },
                    _verify=self.verify,
                )
                if creds
                else None
            ),
            params=self._text_generation_params,
            project_id=self.project_id,
            space_id=self.space_id,
            api_client=api_client,
            validate=validate_model,
        )
        self._model_info = None
        self._deployment_info = None

    model_config = ConfigDict(protected_namespaces=(), validate_assignment=True)

    @property
    defmodel_info(self):
        if self._model.model_id and self._model_info is None:
            self._model_info = self._model.get_details()
        return self._model_info

    @property
    defdeployment_info(self):
        if self._model.deployment_id and self._deployment_info is None:
            self._deployment_info = self._model.get_details()
        return self._deployment_info

    @classmethod
    defclass_name(cls) -> str:
"""Get Class Name."""
        return "WatsonxLLM"

    def_get_credential_kwargs(self) -> Dict[str, SecretStr | None]:
        return {
            "url": self.url,
            "apikey": self.apikey,
            "token": self.token,
            "password": self.password,
            "username": self.username,
            "version": self.version,
        }

    @property
    defmetadata(self) -> LLMMetadata:
        if self.model_id and self._context_window is None:
            model_id = self.model_id
            self._context_window = self.model_info.get("model_limits", {}).get(
                "max_sequence_length"
            )
        elif self._context_window is None:
            model_id = self.deployment_info.get("entity", {}).get("base_model_id")
            self._context_window = (
                self._model._client.foundation_models.get_model_specs(model_id=model_id)
                .get("model_limits", {})
                .get("max_sequence_length")
            )

        return LLMMetadata(
            context_window=self._context_window or DEFAULT_CONTEXT_WINDOW,
            num_output=self.max_new_tokens or DEFAULT_MAX_TOKENS,
            model_name=self.model_id
            or self.deployment_info.get("entity", {}).get(
                "base_model_id", self._model.deployment_id
            ),
        )

    @property
    defsample_generation_text_params(self) -> Dict[str, Any]:
"""Example of Model generation text kwargs that a user can pass to the model."""
        return GenTextParamsMetaNames().get_example_values()

    @property
    defsample_chat_generation_params(self) -> Dict[str, Any]:
"""Example of Model chat generation kwargs that a user can pass to the model."""
        return GenChatParamsMetaNames().get_example_values()

    def_split_generation_params(
        self, data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any] | None, Dict[str, Any]]:
        params = {}
        kwargs = {}
        sample_generation_kwargs_keys = set(self.sample_generation_text_params.keys())
        sample_generation_kwargs_keys.add("prompt_variables")
        for key, value in data.items():
            if key in sample_generation_kwargs_keys:
                params.update({key: value})
            else:
                kwargs.update({key: value})
        return params if params else None, kwargs

    def_split_chat_generation_params(
        self, data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any] | None, Dict[str, Any]]:
        params = {}
        kwargs = {}
        sample_generation_kwargs_keys = set(self.sample_chat_generation_params.keys())
        for key, value in data.items():
            if key in sample_generation_kwargs_keys:
                params.update({key: value})
            else:
                kwargs.update({key: value})
        return params if params else None, kwargs

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        params, generation_kwargs = self._split_generation_params(kwargs)
        if "use_completions" in generation_kwargs:
            del generation_kwargs["use_completions"]
        response = self._model.generate(
            prompt=prompt,
            params=self._text_generation_params or params,
            **generation_kwargs,
        )

        return CompletionResponse(
            text=self._model._return_guardrails_stats(response).get("generated_text"),
            raw=response,
        )

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        params, generation_kwargs = self._split_generation_params(kwargs)
        if "use_completions" in generation_kwargs:
            del generation_kwargs["use_completions"]

        response = await self._model.agenerate(
            prompt=prompt,
            params=self._text_generation_params or params,
            **generation_kwargs,
        )

        return CompletionResponse(
            text=self._model._return_guardrails_stats(response).get("generated_text"),
            raw=response,
        )

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        params, generation_kwargs = self._split_generation_params(kwargs)

        stream_response = self._model.generate_text_stream(
            prompt=prompt,
            params=self._text_generation_params or params,
            **generation_kwargs,
        )

        defgen() -> CompletionResponseGen:
            content = ""
            if kwargs.get("raw_response"):
                for stream_delta in stream_response:
                    stream_delta_text = self._model._return_guardrails_stats(
                        stream_delta
                    ).get("generated_text", "")
                    content += stream_delta_text
                    yield CompletionResponse(
                        text=content, delta=stream_delta_text, raw=stream_delta
                    )
            else:
                for stream_delta in stream_response:
                    content += stream_delta
                    yield CompletionResponse(text=content, delta=stream_delta)

        return gen()

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        async defgen() -> CompletionResponseAsyncGen:
            for message in self.stream_complete(prompt, formatted=formatted, **kwargs):
                yield message

        # NOTE: convert generator to async generator
        return gen()

    def_chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        message_dicts = [to_watsonx_message_dict(message) for message in messages]

        params, generation_kwargs = self._split_chat_generation_params(kwargs)
        response = self._model.chat(
            messages=message_dicts,
            params=params,
            tools=generation_kwargs.get("tools"),
            tool_choice=generation_kwargs.get("tool_choice"),
            tool_choice_option=generation_kwargs.get("tool_choice_option"),
        )

        wx_message = response["choices"][0]["message"]
        message = from_watsonx_message(wx_message)

        return ChatResponse(
            message=message,
            raw=response,
        )

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        if kwargs.get("use_completions"):
            chat_fn = completion_to_chat_decorator(self.complete)
        else:
            chat_fn = self._chat

        return chat_fn(messages, **kwargs)

    async def_achat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        message_dicts = [to_watsonx_message_dict(message) for message in messages]

        params, generation_kwargs = self._split_chat_generation_params(kwargs)
        response = await self._model.achat(
            messages=message_dicts,
            params=params,
            tools=generation_kwargs.get("tools"),
            tool_choice=generation_kwargs.get("tool_choice"),
            tool_choice_option=generation_kwargs.get("tool_choice_option"),
        )

        wx_message = response["choices"][0]["message"]
        message = from_watsonx_message(wx_message)

        return ChatResponse(
            message=message,
            raw=response,
        )

    @llm_chat_callback()
    async defachat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
        if kwargs.get("use_completions"):
            achat_fn = acompletion_to_chat_decorator(self.acomplete)
        else:
            achat_fn = self._achat

        return await achat_fn(messages, **kwargs)

    def_stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        message_dicts = [to_watsonx_message_dict(message) for message in messages]

        params, generation_kwargs = self._split_chat_generation_params(kwargs)
        stream_response = self._model.chat_stream(
            messages=message_dicts,
            params=params,
            tools=generation_kwargs.get("tools"),
            tool_choice=generation_kwargs.get("tool_choice"),
            tool_choice_option=generation_kwargs.get("tool_choice_option"),
        )

        defstream_gen() -> ChatResponseGen:
            content = ""
            role = None
            tool_calls = []

            for response in stream_response:
                tools_available = False
                delta = ""
                additional_kwargs = {}
                if response["choices"]:
                    wx_message = response["choices"][0]["delta"]

                    role = wx_message.get("role") or role or MessageRole.ASSISTANT
                    delta = wx_message.get("content", "")
                    content += delta

                    if "tool_calls" in wx_message:
                        tools_available = True

                    if tools_available:
                        tool_calls = update_tool_calls(
                            tool_calls, wx_message["tool_calls"]
                        )
                        if tool_calls:
                            additional_kwargs["tool_calls"] = tool_calls

                yield ChatResponse(
                    message=ChatMessage(
                        role=role,
                        content=content,
                        additional_kwargs=additional_kwargs,
                    ),
                    delta=delta,
                    raw=response,
                    additional_kwargs=self._get_response_token_counts(response),
                )

        return stream_gen()

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        if kwargs.get("use_completions"):
            chat_stream_fn = stream_completion_to_chat_decorator(self.stream_complete)
        else:
            chat_stream_fn = self._stream_chat

        return chat_stream_fn(messages, **kwargs)

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        async defgen() -> ChatResponseAsyncGen:
            for message in self.stream_chat(messages, **kwargs):
                yield message

        # NOTE: convert generator to async generator
        return gen()

    def_prepare_chat_with_tools(
        self,
        tools: List["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        tool_required: bool = False,
        tool_choice: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
"""Predict and call the tool."""
        # watsonx uses the same openai tool format
        tool_specs = [tool.metadata.to_openai_tool() for tool in tools]

        if isinstance(user_msg, str):
            user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)

        messages = chat_history or []
        if user_msg:
            messages.append(user_msg)

        chat_with_tools_payload = {
            "messages": messages,
            "tools": tool_specs or None,
            **kwargs,
        }
        if tool_required and tool_choice is None:
            # NOTE: watsonx can only require a single tool
            tool_choice = tools[0].metadata.name if len(tools)  0 else None
        if tool_choice is not None:
            chat_with_tools_payload.update(
                {"tool_choice": {"type": "function", "function": {"name": tool_choice}}}
            )
        return chat_with_tools_payload

    defget_tool_calls_from_response(
        self,
        response: ChatResponse,
        error_on_no_tool_call: bool = True,
        **kwargs: Any,
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
            if not isinstance(tool_call, dict):
                raise ValueError("Invalid tool_call object")
            if tool_call.get("type") != "function":
                raise ValueError("Invalid tool type. Unsupported by watsonx.ai")

            # this should handle both complete and partial jsons
            try:
                argument_dict = parse_partial_json(
                    tool_call.get("function", {}).get("arguments")
                )
            except ValueError:
                argument_dict = {}

            tool_selections.append(
                ToolSelection(
                    tool_id=tool_call.get("id"),
                    tool_name=tool_call.get("function").get("name"),
                    tool_kwargs=argument_dict,
                )
            )

        return tool_selections

    def_get_response_token_counts(self, raw_response: Any) -> dict:
"""Get the token usage reported by the response."""
        if isinstance(raw_response, dict):
            usage = raw_response.get("usage", {})
            if not usage:
                return {}

            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            total_tokens = usage.get("total_tokens", 0)
        else:
            return {}

        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
        }

```
 |  
| --- | --- |  
###  sample_generation_text_params `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/ibm/#llama_index.llms.ibm.WatsonxLLM.sample_generation_text_params "Permanent link")

```
sample_generation_text_params: [, ]

```

Example of Model generation text kwargs that a user can pass to the model.
###  sample_chat_generation_params `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/ibm/#llama_index.llms.ibm.WatsonxLLM.sample_chat_generation_params "Permanent link")

```
sample_chat_generation_params: [, ]

```

Example of Model chat generation kwargs that a user can pass to the model.
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/ibm/#llama_index.llms.ibm.WatsonxLLM.class_name "Permanent link")

```
class_name() -> 

```

Get Class Name.
Source code in `llama-index-integrations/llms/llama-index-llms-ibm/llama_index/llms/ibm/base.py`  
| 
```
287
288
289
290
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get Class Name."""
    return "WatsonxLLM"

```
 |  
| --- | --- |  
###  get_tool_calls_from_response [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/ibm/#llama_index.llms.ibm.WatsonxLLM.get_tool_calls_from_response "Permanent link")

```
get_tool_calls_from_response(
    response: ,
    error_on_no_tool_call:  = True,
    **kwargs: 
) -> []

```

Predict and call the tool.
Source code in `llama-index-integrations/llms/llama-index-llms-ibm/llama_index/llms/ibm/base.py`  
| 
```
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
        if not isinstance(tool_call, dict):
            raise ValueError("Invalid tool_call object")
        if tool_call.get("type") != "function":
            raise ValueError("Invalid tool type. Unsupported by watsonx.ai")

        # this should handle both complete and partial jsons
        try:
            argument_dict = parse_partial_json(
                tool_call.get("function", {}).get("arguments")
            )
        except ValueError:
            argument_dict = {}

        tool_selections.append(
            ToolSelection(
                tool_id=tool_call.get("id"),
                tool_name=tool_call.get("function").get("name"),
                tool_kwargs=argument_dict,
            )
        )

    return tool_selections

```
 |  
| --- | --- |  
options: members: - WatsonxLLM
