# Deepinfra
##  DeepInfraLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/deepinfra/#llama_index.llms.deepinfra.DeepInfraLLM "Permanent link")
Bases: `FunctionCallingLLM`
DeepInfra LLM.
Examples:
`pip install llama-index-llms-deepinfra`

```
fromllama_index.llms.deepinfraimport DeepInfraLLM

llm = DeepInfraLLM(
    model="mistralai/Mixtral-8x22B-Instruct-v0.1", # Default model name
    api_key = "your-deepinfra-api-key",
    temperature=0.5,
    max_tokens=50,
    additional_kwargs={"top_p": 0.9},
)

response = llm.complete("Hello World!")
print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-deepinfra/llama_index/llms/deepinfra/base.py`  
| 
```
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
```
 | 
```
classDeepInfraLLM(FunctionCallingLLM):
"""
    DeepInfra LLM.

    Examples:
        `pip install llama-index-llms-deepinfra`

        ```python
        from llama_index.llms.deepinfra import DeepInfraLLM

        llm = DeepInfraLLM(
            model="mistralai/Mixtral-8x22B-Instruct-v0.1", # Default model name
            api_key = "your-deepinfra-api-key",
            temperature=0.5,
            max_tokens=50,
            additional_kwargs={"top_p": 0.9},


        response = llm.complete("Hello World!")
        print(response)
        ```

    """

    model: str = Field(
        default=DEFAULT_MODEL_NAME, description="The DeepInfra model to use."
    )

    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        description="The temperature to use during generation.",
        ge=0.0,
        le=1.0,
    )
    max_tokens: Optional[int] = Field(
        default=DEFAULT_MAX_TOKENS,
        description="The maximum number of tokens to generate.",
        gt=0,
    )

    timeout: Optional[float] = Field(
        default=None, description="The timeout to use in seconds.", ge=0
    )
    max_retries: int = Field(
        default=10, description="The maximum number of API retries.", ge=0
    )

    _api_key: Optional[str] = PrivateAttr()

    generate_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional keyword arguments for generation."
    )

    _client: DeepInfraClient = PrivateAttr()

    def__init__(
        self,
        model: str = DEFAULT_MODEL_NAME,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: Optional[int] = DEFAULT_MAX_TOKENS,
        max_retries: int = 10,
        api_base: str = API_BASE,
        timeout: Optional[float] = None,
        api_key: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
    ) -> None:
        additional_kwargs = additional_kwargs or {}
        callback_manager = callback_manager or CallbackManager([])

        super().__init__(
            model=model,
            api_base=api_base,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
            additional_kwargs=additional_kwargs,
            max_retries=max_retries,
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )
        self._api_key = get_from_param_or_env("api_key", api_key, ENV_VARIABLE)
        self._client = DeepInfraClient(
            api_key=self._api_key,
            api_base=api_base,
            timeout=timeout,
            max_retries=max_retries,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "DeepInfra_LLM"

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            num_output=self.max_tokens,
            is_chat_model=self._is_chat_model,
            model=self.model,
            model_name=self.model,
            is_function_calling_model=self._client.is_function_calling_model(
                self.model
            ),
        )

    @property
    def_is_chat_model(self) -> bool:
        return True

    # Synchronous Methods
    @llm_completion_callback()
    defcomplete(self, prompt: str, **kwargs) -> CompletionResponse:
"""
        Generate completion for the given prompt.

        Args:
            prompt (str): The input prompt to generate completion for.
            **kwargs: Additional keyword arguments for the API request.

        Returns:
            str: The generated text completion.

        """
        payload = self._build_payload(prompt=prompt, **kwargs)
        result = self._client.request(INFERENCE_ENDPOINT, payload)
        return CompletionResponse(text=maybe_extract_from_json(result), raw=result)

    @llm_completion_callback()
    defstream_complete(self, prompt: str, **kwargs) -> CompletionResponseGen:
"""
        Generate a synchronous streaming completion for the given prompt.

        Args:
            prompt (str): The input prompt to generate completion for.
            **kwargs: Additional keyword arguments for the API request.

        Yields:
            CompletionResponseGen: The streaming text completion.

        """
        payload = self._build_payload(prompt=prompt, **kwargs)

        content = ""
        for response_dict in self._client.request_stream(INFERENCE_ENDPOINT, payload):
            content_delta = maybe_extract_from_json(response_dict)
            content += content_delta
            yield CompletionResponse(
                text=content, delta=content_delta, raw=response_dict
            )

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs) -> ChatResponse:
"""
        Generate a chat response for the given messages.

        Args:
            messages (Sequence[ChatMessage]): A sequence of chat messages.
            **kwargs: Additional keyword arguments for the API request.

        Returns:
            ChatResponse: The chat response containing a sequence of messages.

        """
        messages = chat_messages_to_list(messages)
        payload = self._build_payload(messages=messages, **kwargs)
        result = self._client.request(CHAT_API_ENDPOINT, payload)
        mo = result["choices"][-1]["message"]
        additional_kwargs = {
            "tool_calls": mo.get("tool_calls", []) or [],
        }
        return ChatResponse(
            message=ChatMessage(
                role=mo["role"],
                content=mo["content"],
                additional_kwargs=additional_kwargs,
            ),
            raw=result,
        )

    @llm_chat_callback()
    defstream_chat(
        self, chat_messages: Sequence[ChatMessage], **kwargs
    ) -> ChatResponseGen:
"""
        Generate a synchronous streaming chat response for the given messages.

        Args:
            messages (Sequence[ChatMessage]): A sequence of chat messages.
            **kwargs: Additional keyword arguments for the API request.

        Yields:
            ChatResponseGen: The chat response containing a sequence of messages.

        """
        messages = chat_messages_to_list(chat_messages)
        payload = self._build_payload(messages=messages, **kwargs)

        content = ""
        role = MessageRole.ASSISTANT
        for response_dict in self._client.request_stream(CHAT_API_ENDPOINT, payload):
            delta = response_dict["choices"][-1]["delta"]
"""
            Check if the delta contains content.

            if delta.get("content", None):
                content_delta = delta["content"]
                content += delta["content"]
                message = ChatMessage(
                    role=role,
                    content=content,
                )
                yield ChatResponse(
                    message=message, raw=response_dict, delta=content_delta
                )

    # Asynchronous Methods
    @llm_completion_callback()
    async defacomplete(self, prompt: str, **kwargs) -> CompletionResponse:
"""
        Asynchronously generate completion for the given prompt.

        Args:
            prompt (str): The input prompt to generate completion for.
            **kwargs: Additional keyword arguments for the API request.

        Returns:
            CompletionResponse: The generated text completion.

        """
        payload = self._build_payload(prompt=prompt, **kwargs)

        result = await self._client.arequest(INFERENCE_ENDPOINT, payload)
        return CompletionResponse(text=maybe_extract_from_json(result), raw=result)

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, **kwargs
    ) -> CompletionResponseAsyncGen:
"""
        Asynchronously generate a streaming completion for the given prompt.

        Args:
            prompt (str): The input prompt to generate completion for.
            **kwargs: Additional keyword arguments for the API request.

        Yields:
            CompletionResponseAsyncGen: The streaming text completion.

        """
        payload = self._build_payload(prompt=prompt, **kwargs)

        async defgen():
            content = ""
            async for response_dict in self._client.arequest_stream(
                INFERENCE_ENDPOINT, payload
            ):
                content_delta = maybe_extract_from_json(response_dict)
                content += content_delta
                yield CompletionResponse(
                    text=content, delta=content_delta, raw=response_dict
                )

        return gen()

    @llm_chat_callback()
    async defachat(
        self, chat_messages: Sequence[ChatMessage], **kwargs
    ) -> ChatResponse:
"""
        Asynchronously generate a chat response for the given messages.

        Args:
            messages (Sequence[ChatMessage]): A sequence of chat messages.
            **kwargs: Additional keyword arguments for the API request.

        Returns:
            ChatResponse: The chat response containing a sequence of messages.

        """
        messages = chat_messages_to_list(chat_messages)
        payload = self._build_payload(messages=messages, **kwargs)

        result = await self._client.arequest(CHAT_API_ENDPOINT, payload)
        mo = result["choices"][-1]["message"]
        additional_kwargs = {"tool_calls": mo.get("tool_calls", []) or []}
        return ChatResponse(
            message=ChatMessage(
                role=mo["role"],
                content=mo["content"],
                additional_kwargs=additional_kwargs,
            ),
            raw=result,
        )

    @llm_chat_callback()
    async defastream_chat(
        self, chat_messages: Sequence[ChatMessage], **kwargs
    ) -> ChatResponseAsyncGen:
"""
        Asynchronously generate a streaming chat response for the given messages.

        Args:
            messages (Sequence[ChatMessage]): A sequence of chat messages.
            **kwargs: Additional keyword arguments for the API request.

        Yields:
            ChatResponseAsyncGen: The chat response containing a sequence of messages.

        """
        messages = chat_messages_to_list(chat_messages)
        payload = self._build_payload(messages=messages, **kwargs)

        async defgen():
            content = ""
            role = MessageRole.ASSISTANT
            async for response_dict in self._client.arequest_stream(
                CHAT_API_ENDPOINT, payload
            ):
                delta = response_dict["choices"][-1]["delta"]
"""
                Check if the delta contains content.

                if delta.get("content", None):
                    content_delta = delta["content"]
                    content += delta["content"]
                    message = ChatMessage(
                        role=role,
                        content=content,
                    )
                    yield ChatResponse(
                        message=message, raw=response_dict, delta=content_delta
                    )

        return gen()

    def_prepare_chat_with_tools(
        self,
        tools: List["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        tool_required: bool = False,  # unsupported by deepinfra https://deepinfra.com/docs/advanced/function_calling - tool_choice only takes "auto" or "none", (not "required", so sadly can't require it)
        tool_choice: Union[str, dict] = "auto",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        tool_specs = [tool.metadata.to_openai_tool() for tool in tools]
        if isinstance(user_msg, str):
            user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)

        messages = chat_history or []
        if user_msg:
            messages.append(user_msg)

        return {
            "messages": messages,
            "tools": tool_specs or None,
            "tool_choice": TOOL_CHOICE,
            **kwargs,
        }

    def_validate_chat_with_tools_response(
        self,
        response: "ChatResponse",
        tools: List["BaseTool"],
        allow_parallel_tool_calls: bool = False,
        **kwargs: Any,
    ) -> ChatResponse:
        if not allow_parallel_tool_calls:
            force_single_tool_call(response)
        return response

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
        for tool_call_dict in tool_calls:
            tool_call = ToolCallMessage.parse_obj(tool_call_dict)
            argument_dict = json.loads(tool_call.function.arguments)

            tool_selections.append(
                ToolSelection(
                    tool_id=tool_call.id,
                    tool_name=tool_call.function.name,
                    tool_kwargs=argument_dict,
                )
            )

        return tool_selections

    # Utility Methods
    defget_model_endpoint(self) -> str:
"""
        Get DeepInfra model endpoint.
        """
        return f"{INFERENCE_ENDPOINT}/{self.model}"

    def_build_payload(self, **kwargs) -> Dict[str, Any]:
"""
        Build the payload for the API request.
        The temperature and max_tokens parameters explicitly override
        the corresponding values in generate_kwargs.
        Any provided kwargs override all other parameters, including temperature and max_tokens.

        Args:
            prompt (str): The input prompt to generate completion for.
            stream (bool): Whether to stream the response.
            **kwargs: Additional keyword arguments for the API request.

        Returns:
            Dict[str, Any]: The API request payload.

        """
        return {
            **self.generate_kwargs,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "model": self.model,
            **kwargs,
        }

```
 |  
| --- | --- |  
###  complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/deepinfra/#llama_index.llms.deepinfra.DeepInfraLLM.complete "Permanent link")

```
complete(prompt: , **kwargs) -> 

```

Generate completion for the given prompt.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  The input prompt to generate completion for.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments for the API request.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |   |  The generated text completion.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-deepinfra/llama_index/llms/deepinfra/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defcomplete(self, prompt: str, **kwargs) -> CompletionResponse:
"""
    Generate completion for the given prompt.

    Args:
        prompt (str): The input prompt to generate completion for.
        **kwargs: Additional keyword arguments for the API request.

    Returns:
        str: The generated text completion.

    """
    payload = self._build_payload(prompt=prompt, **kwargs)
    result = self._client.request(INFERENCE_ENDPOINT, payload)
    return CompletionResponse(text=maybe_extract_from_json(result), raw=result)

```
 |  
| --- | --- |  
###  stream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/deepinfra/#llama_index.llms.deepinfra.DeepInfraLLM.stream_complete "Permanent link")

```
stream_complete(
    prompt: , **kwargs
) -> CompletionResponseGen

```

Generate a synchronous streaming completion for the given prompt.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  The input prompt to generate completion for.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments for the API request.  |  
Yields:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `CompletionResponseGen`  |  `CompletionResponseGen`  |  The streaming text completion.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-deepinfra/llama_index/llms/deepinfra/base.py`  
| 
```
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
@llm_completion_callback()
defstream_complete(self, prompt: str, **kwargs) -> CompletionResponseGen:
"""
    Generate a synchronous streaming completion for the given prompt.

    Args:
        prompt (str): The input prompt to generate completion for.
        **kwargs: Additional keyword arguments for the API request.

    Yields:
        CompletionResponseGen: The streaming text completion.

    """
    payload = self._build_payload(prompt=prompt, **kwargs)

    content = ""
    for response_dict in self._client.request_stream(INFERENCE_ENDPOINT, payload):
        content_delta = maybe_extract_from_json(response_dict)
        content += content_delta
        yield CompletionResponse(
            text=content, delta=content_delta, raw=response_dict
        )

```
 |  
| --- | --- |  
###  chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/deepinfra/#llama_index.llms.deepinfra.DeepInfraLLM.chat "Permanent link")

```
chat(
    messages: Sequence[], **kwargs
) -> 

```

Generate a chat response for the given messages.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  A sequence of chat messages.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments for the API request.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `ChatResponse`  |   |  The chat response containing a sequence of messages.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-deepinfra/llama_index/llms/deepinfra/base.py`  
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
```
 | 
```
@llm_chat_callback()
defchat(self, messages: Sequence[ChatMessage], **kwargs) -> ChatResponse:
"""
    Generate a chat response for the given messages.

    Args:
        messages (Sequence[ChatMessage]): A sequence of chat messages.
        **kwargs: Additional keyword arguments for the API request.

    Returns:
        ChatResponse: The chat response containing a sequence of messages.

    """
    messages = chat_messages_to_list(messages)
    payload = self._build_payload(messages=messages, **kwargs)
    result = self._client.request(CHAT_API_ENDPOINT, payload)
    mo = result["choices"][-1]["message"]
    additional_kwargs = {
        "tool_calls": mo.get("tool_calls", []) or [],
    }
    return ChatResponse(
        message=ChatMessage(
            role=mo["role"],
            content=mo["content"],
            additional_kwargs=additional_kwargs,
        ),
        raw=result,
    )

```
 |  
| --- | --- |  
###  stream_chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/deepinfra/#llama_index.llms.deepinfra.DeepInfraLLM.stream_chat "Permanent link")

```
stream_chat(
    chat_messages: Sequence[], **kwargs
) -> ChatResponseGen

```

Generate a synchronous streaming chat response for the given messages.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  A sequence of chat messages.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments for the API request.  |  
Yields:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `ChatResponseGen`  |  `ChatResponseGen`  |  The chat response containing a sequence of messages.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-deepinfra/llama_index/llms/deepinfra/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
defstream_chat(
    self, chat_messages: Sequence[ChatMessage], **kwargs
) -> ChatResponseGen:
"""
    Generate a synchronous streaming chat response for the given messages.

    Args:
        messages (Sequence[ChatMessage]): A sequence of chat messages.
        **kwargs: Additional keyword arguments for the API request.

    Yields:
        ChatResponseGen: The chat response containing a sequence of messages.

    """
    messages = chat_messages_to_list(chat_messages)
    payload = self._build_payload(messages=messages, **kwargs)

    content = ""
    role = MessageRole.ASSISTANT
    for response_dict in self._client.request_stream(CHAT_API_ENDPOINT, payload):
        delta = response_dict["choices"][-1]["delta"]
"""
        Check if the delta contains content.
        """
        if delta.get("content", None):
            content_delta = delta["content"]
            content += delta["content"]
            message = ChatMessage(
                role=role,
                content=content,
            )
            yield ChatResponse(
                message=message, raw=response_dict, delta=content_delta
            )

```
 |  
| --- | --- |  
###  acomplete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/deepinfra/#llama_index.llms.deepinfra.DeepInfraLLM.acomplete "Permanent link")

```
acomplete(prompt: , **kwargs) -> 

```

Asynchronously generate completion for the given prompt.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  The input prompt to generate completion for.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments for the API request.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `CompletionResponse`  |   |  The generated text completion.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-deepinfra/llama_index/llms/deepinfra/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
async defacomplete(self, prompt: str, **kwargs) -> CompletionResponse:
"""
    Asynchronously generate completion for the given prompt.

    Args:
        prompt (str): The input prompt to generate completion for.
        **kwargs: Additional keyword arguments for the API request.

    Returns:
        CompletionResponse: The generated text completion.

    """
    payload = self._build_payload(prompt=prompt, **kwargs)

    result = await self._client.arequest(INFERENCE_ENDPOINT, payload)
    return CompletionResponse(text=maybe_extract_from_json(result), raw=result)

```
 |  
| --- | --- |  
###  astream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/deepinfra/#llama_index.llms.deepinfra.DeepInfraLLM.astream_complete "Permanent link")

```
astream_complete(
    prompt: , **kwargs
) -> CompletionResponseAsyncGen

```

Asynchronously generate a streaming completion for the given prompt.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  The input prompt to generate completion for.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments for the API request.  |  
Yields:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `CompletionResponseAsyncGen`  |  `CompletionResponseAsyncGen`  |  The streaming text completion.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-deepinfra/llama_index/llms/deepinfra/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
async defastream_complete(
    self, prompt: str, **kwargs
) -> CompletionResponseAsyncGen:
"""
    Asynchronously generate a streaming completion for the given prompt.

    Args:
        prompt (str): The input prompt to generate completion for.
        **kwargs: Additional keyword arguments for the API request.

    Yields:
        CompletionResponseAsyncGen: The streaming text completion.

    """
    payload = self._build_payload(prompt=prompt, **kwargs)

    async defgen():
        content = ""
        async for response_dict in self._client.arequest_stream(
            INFERENCE_ENDPOINT, payload
        ):
            content_delta = maybe_extract_from_json(response_dict)
            content += content_delta
            yield CompletionResponse(
                text=content, delta=content_delta, raw=response_dict
            )

    return gen()

```
 |  
| --- | --- |  
###  achat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/deepinfra/#llama_index.llms.deepinfra.DeepInfraLLM.achat "Permanent link")

```
achat(
    chat_messages: Sequence[], **kwargs
) -> 

```

Asynchronously generate a chat response for the given messages.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  A sequence of chat messages.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments for the API request.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `ChatResponse`  |   |  The chat response containing a sequence of messages.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-deepinfra/llama_index/llms/deepinfra/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
async defachat(
    self, chat_messages: Sequence[ChatMessage], **kwargs
) -> ChatResponse:
"""
    Asynchronously generate a chat response for the given messages.

    Args:
        messages (Sequence[ChatMessage]): A sequence of chat messages.
        **kwargs: Additional keyword arguments for the API request.

    Returns:
        ChatResponse: The chat response containing a sequence of messages.

    """
    messages = chat_messages_to_list(chat_messages)
    payload = self._build_payload(messages=messages, **kwargs)

    result = await self._client.arequest(CHAT_API_ENDPOINT, payload)
    mo = result["choices"][-1]["message"]
    additional_kwargs = {"tool_calls": mo.get("tool_calls", []) or []}
    return ChatResponse(
        message=ChatMessage(
            role=mo["role"],
            content=mo["content"],
            additional_kwargs=additional_kwargs,
        ),
        raw=result,
    )

```
 |  
| --- | --- |  
###  astream_chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/deepinfra/#llama_index.llms.deepinfra.DeepInfraLLM.astream_chat "Permanent link")

```
astream_chat(
    chat_messages: Sequence[], **kwargs
) -> ChatResponseAsyncGen

```

Asynchronously generate a streaming chat response for the given messages.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  A sequence of chat messages.  |  _required_  |  
|  `**kwargs`  |  Additional keyword arguments for the API request.  |  
Yields:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `ChatResponseAsyncGen`  |  `ChatResponseAsyncGen`  |  The chat response containing a sequence of messages.  |  
Source code in `llama-index-integrations/llms/llama-index-llms-deepinfra/llama_index/llms/deepinfra/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
async defastream_chat(
    self, chat_messages: Sequence[ChatMessage], **kwargs
) -> ChatResponseAsyncGen:
"""
    Asynchronously generate a streaming chat response for the given messages.

    Args:
        messages (Sequence[ChatMessage]): A sequence of chat messages.
        **kwargs: Additional keyword arguments for the API request.

    Yields:
        ChatResponseAsyncGen: The chat response containing a sequence of messages.

    """
    messages = chat_messages_to_list(chat_messages)
    payload = self._build_payload(messages=messages, **kwargs)

    async defgen():
        content = ""
        role = MessageRole.ASSISTANT
        async for response_dict in self._client.arequest_stream(
            CHAT_API_ENDPOINT, payload
        ):
            delta = response_dict["choices"][-1]["delta"]
"""
            Check if the delta contains content.

            if delta.get("content", None):
                content_delta = delta["content"]
                content += delta["content"]
                message = ChatMessage(
                    role=role,
                    content=content,
                )
                yield ChatResponse(
                    message=message, raw=response_dict, delta=content_delta
                )

    return gen()

```
 |  
| --- | --- |  
###  get_model_endpoint [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/deepinfra/#llama_index.llms.deepinfra.DeepInfraLLM.get_model_endpoint "Permanent link")

```
get_model_endpoint() -> 

```

Get DeepInfra model endpoint.
Source code in `llama-index-integrations/llms/llama-index-llms-deepinfra/llama_index/llms/deepinfra/base.py`  
| 
```
463
464
465
466
467
```
 | 
```
defget_model_endpoint(self) -> str:
"""
    Get DeepInfra model endpoint.
    """
    return f"{INFERENCE_ENDPOINT}/{self.model}"

```
 |  
| --- | --- |  
options: members: - DeepInfraLLM
