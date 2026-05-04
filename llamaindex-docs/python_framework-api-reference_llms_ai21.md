# Ai21
##  AI21 [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/ai21/#llama_index.llms.ai21.AI21 "Permanent link")
Bases: `FunctionCallingLLM`
AI21 Labs LLM.
Examples:
`pip install llama-index-llms-ai21`

```
fromllama_index.llms.ai21import AI21

llm = AI21(model="jamba-instruct", api_key=api_key)
resp = llm.complete("Paul Graham is ")
print(resp)

```

Source code in `llama-index-integrations/llms/llama-index-llms-ai21/llama_index/llms/ai21/base.py`  
| 
```
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
```
 | 
```
classAI21(FunctionCallingLLM):
"""
    AI21 Labs LLM.

    Examples:
        `pip install llama-index-llms-ai21`

        ```python
        from llama_index.llms.ai21 import AI21

        llm = AI21(model="jamba-instruct", api_key=api_key)
        resp = llm.complete("Paul Graham is ")
        print(resp)
        ```

    """

    model: str = Field(
        description="The AI21 model to use.", default=_DEFAULT_AI21_MODEL
    )
    max_tokens: int = Field(
        description="The maximum number of tokens to generate.",
        default=_DEFAULT_MAX_TOKENS,
        gt=0,
    )
    temperature: float = Field(
        description="The temperature to use for sampling.",
        default=_DEFAULT_TEMPERATURE,
        ge=0.0,
        le=1.0,
    )
    base_url: Optional[str] = Field(default=None, description="The base URL to use.")
    timeout: Optional[float] = Field(
        default=None, description="The timeout to use in seconds.", ge=0
    )

    max_retries: int = Field(
        default=10, description="The maximum number of API retries.", ge=0
    )

    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the anthropic API."
    )

    _client: Any = PrivateAttr()
    _async_client: Any = PrivateAttr()

    def__init__(
        self,
        model: str = _DEFAULT_AI21_MODEL,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        max_tokens: Optional[int] = _DEFAULT_MAX_TOKENS,
        max_retries: int = 10,
        default_headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        temperature: Optional[float] = _DEFAULT_TEMPERATURE,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
    ) -> None:
"""Initialize params."""
        additional_kwargs = additional_kwargs or {}
        callback_manager = callback_manager or CallbackManager([])
        super().__init__(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            additional_kwargs=additional_kwargs,
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )

        self._client = AI21Client(
            api_key=api_key,
            api_host=base_url,
            timeout_sec=timeout,
            num_retries=max_retries,
            headers=default_headers,
            via="llama-index",
        )

        self._async_client = AsyncAI21Client(
            api_key=api_key,
            api_host=base_url,
            timeout_sec=timeout,
            num_retries=max_retries,
            headers=default_headers,
            via="llama-index",
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get Class Name."""
        return "AI21_LLM"

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=ai21_model_to_context_size(self.model),
            num_output=self.max_tokens,
            model_name=self.model,
            is_function_calling_model=is_function_calling_model(
                model=self.model,
            ),
            is_chat_model=True,
        )

    @property
    deftokenizer(self) -> BaseTokenizer:
        return Tokenizer.get_tokenizer(_TOKENIZER_MAP.get(self.model))

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        return {**base_kwargs, **self.additional_kwargs}

    def_get_all_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        return {
            **self._model_kwargs,
            **kwargs,
        }

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        all_kwargs = self._get_all_kwargs(**kwargs)

        if self._is_j2_model():
            return self._j2_completion(prompt, formatted, **all_kwargs)

        completion_fn = chat_to_completion_decorator(self.chat)

        return completion_fn(prompt, **all_kwargs)

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        if self._is_j2_model():
            raise ValueError("Stream completion is not supported for J2 models.")

        all_kwargs = self._get_all_kwargs(**kwargs)
        completion_fn = stream_chat_to_completion_decorator(self.stream_chat)

        return completion_fn(prompt, **all_kwargs)

    def_prepare_chat_with_tools(
        self,
        tools: List["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        tool_required: bool = False,  # ai21 does not support configuring the tool_choice
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
            "tools": tool_specs,
            **kwargs,
        }

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        all_kwargs = self._get_all_kwargs(**kwargs)

        if self._is_j2_model():
            return self._j2_chat(messages, **all_kwargs)

        messages = [message_to_ai21_message(message) for message in messages]
        response = self._client.chat.completions.create(
            messages=messages,
            stream=False,
            **all_kwargs,
        )

        message = from_ai21_message_to_chat_message(response.choices[0].message)

        return ChatResponse(
            message=message,
            raw=response.to_dict(),
        )

    @llm_chat_callback()
    async defachat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
        all_kwargs = self._get_all_kwargs(**kwargs)

        if self._is_j2_model():
            return await self._j2_async_chat(messages, **all_kwargs)

        messages = [message_to_ai21_message(message) for message in messages]
        response = await self._async_client.chat.completions.create(
            messages=messages,
            stream=False,
            **all_kwargs,
        )

        message = from_ai21_message_to_chat_message(response.choices[0].message)

        return ChatResponse(
            message=message,
            raw=response.to_dict(),
        )

    @llm_chat_callback()
    async defastream_chat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponseAsyncGen:
        if self._is_j2_model():
            raise ValueError("Async Stream chat is not supported for J2 models.")

        all_kwargs = self._get_all_kwargs(**kwargs)
        messages = [message_to_ai21_message(message) for message in messages]
        response = await self._async_client.chat.completions.create(
            messages=messages,
            stream=True,
            **all_kwargs,
        )

        async defgen() -> ChatResponseAsyncGen:
            content = ""
            role = MessageRole.ASSISTANT

            async for r in response:
                if isinstance(r, ChatCompletionChunk):
                    content_delta = r.choices[0].delta.content

                    if content_delta is None:
                        content += ""
                    else:
                        content += r.choices[0].delta.content

                    yield ChatResponse(
                        message=ChatMessage(role=role, content=content),
                        delta=content_delta,
                        raw=r.to_dict(),
                    )

        return gen()

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        all_kwargs = self._get_all_kwargs(**kwargs)

        if self._is_j2_model():
            return await self._j2_async_complete(prompt, formatted, **all_kwargs)

        acomplete_fn = achat_to_completion_decorator(self.achat)
        return await acomplete_fn(prompt, **kwargs)

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        astream_complete_fn = astream_chat_to_completion_decorator(self.astream_chat)
        return await astream_complete_fn(prompt, **kwargs)

    def_j2_chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        system, messages = message_to_ai21_j2_message(messages)
        response = self._client.chat.create(
            system=system,
            messages=messages,
            stream=False,
            **kwargs,
        )

        return ChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT,
                content=response.outputs[0].text,
            ),
            raw=response.to_dict(),
        )

    async def_j2_async_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        system, messages = message_to_ai21_j2_message(messages)
        response = await self._async_client.chat.create(
            system=system,
            messages=messages,
            stream=False,
            **kwargs,
        )

        return ChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT,
                content=response.outputs[0].text,
            ),
            raw=response.to_dict(),
        )

    async def_j2_async_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        response = await self._async_client.completion.create(
            prompt=prompt,
            stream=False,
            **kwargs,
        )

        return CompletionResponse(
            text=response.completions[0].data.text,
            raw=response.to_dict(),
        )

    def_j2_completion(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        response = self._client.completion.create(
            prompt=prompt,
            stream=False,
            **kwargs,
        )

        return CompletionResponse(
            text=response.completions[0].data.text,
            raw=response.to_dict(),
        )

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        if self._is_j2_model():
            raise ValueError("Stream chat is not supported for J2 models.")

        all_kwargs = self._get_all_kwargs(**kwargs)
        messages = [message_to_ai21_message(message) for message in messages]
        response = self._client.chat.completions.create(
            messages=messages,
            stream=True,
            **all_kwargs,
        )

        defgen() -> ChatResponseGen:
            content = ""
            role = MessageRole.ASSISTANT

            for r in response:
                if isinstance(r, ChatCompletionChunk):
                    content_delta = r.choices[0].delta.content

                    if content_delta is None:
                        content += ""
                    else:
                        content += r.choices[0].delta.content

                    yield ChatResponse(
                        message=ChatMessage(role=role, content=content),
                        delta=content_delta,
                        raw=r.to_dict(),
                    )

        return gen()

    def_is_j2_model(self) -> bool:
        return "j2" in self.model

    def_parse_tool(self, tool_call: ToolCall) -> ToolSelection:
        if not isinstance(tool_call, ToolCall):
            raise ValueError("Invalid tool_call object")

        if tool_call.type != "function":
            raise ValueError(f"Unsupported tool call type: {tool_call.type}")

        try:
            argument_dict = parse_partial_json(tool_call.function.arguments)
        except ValueError:
            argument_dict = {}

        return ToolSelection(
            tool_id=tool_call.id,
            tool_name=tool_call.function.name,
            tool_kwargs=argument_dict,
        )

    defget_tool_calls_from_response(
        self,
        response: ChatResponse,
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

        return [self._parse_tool(tool_call) for tool_call in tool_calls]

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/ai21/#llama_index.llms.ai21.AI21.class_name "Permanent link")

```
class_name() -> 

```

Get Class Name.
Source code in `llama-index-integrations/llms/llama-index-llms-ai21/llama_index/llms/ai21/base.py`  
| 
```
151
152
153
154
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get Class Name."""
    return "AI21_LLM"

```
 |  
| --- | --- |  
options: members: - AI21
