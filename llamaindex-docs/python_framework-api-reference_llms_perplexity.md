# Perplexity
##  Perplexity [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/perplexity/#llama_index.llms.perplexity.Perplexity "Permanent link")
Bases: 
Perplexity LLM.
Examples:
`pip install llama-index-llms-perplexity`

```
fromllama_index.llms.perplexityimport Perplexity
fromllama_index.core.llmsimport ChatMessage

pplx_api_key = "your-perplexity-api-key"

llm = Perplexity(
    api_key=pplx_api_key, model="sonar-pro", temperature=0.5
)

messages_dict = [
    {"role": "system", "content": "Be precise and concise."},
    {"role": "user", "content": "Tell me 5 sentences about Perplexity."},
]
messages = [ChatMessage(**msg) for msg in messages_dict]

response = llm.chat(messages)
print(str(response))

```

Source code in `llama-index-integrations/llms/llama-index-llms-perplexity/llama_index/llms/perplexity/base.py`  
| 
```
 29
 30
 31
 32
 33
 34
 35
 36
 37
 38
 39
 40
 41
 42
 43
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
```
 | 
```
classPerplexity(LLM):
"""
    Perplexity LLM.

    Examples:
        `pip install llama-index-llms-perplexity`

        ```python
        from llama_index.llms.perplexity import Perplexity
        from llama_index.core.llms import ChatMessage

        pplx_api_key = "your-perplexity-api-key"

        llm = Perplexity(
            api_key=pplx_api_key, model="sonar-pro", temperature=0.5


        messages_dict = [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": "Tell me 5 sentences about Perplexity."},

        messages = [ChatMessage(**msg) for msg in messages_dict]

        response = llm.chat(messages)
        print(str(response))
        ```

    """

    model: str = Field(
        default="sonar-pro",
        description="The Perplexity model to use.",
    )
    temperature: float = Field(description="The temperature to use during generation.")
    max_tokens: Optional[int] = Field(
        default=None,
        description="The maximum number of tokens to generate.",
    )
    context_window: Optional[int] = Field(
        default=None,
        description="The context window to use during generation.",
    )
    api_key: Optional[str] = Field(
        description="The Perplexity API key.",
        exclude=True,
    )
    api_base: str = Field(
        default="https://api.perplexity.ai",
        description="The base URL for Perplexity API.",
    )
    additional_kwargs: dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the Perplexity API."
    )
    max_retries: int = Field(
        default=10, description="The maximum number of API retries."
    )
    headers: dict[str, str] = Field(
        default_factory=dict, description="Headers for API requests."
    )
    enable_search_classifier: bool = Field(
        default=False,
        description="Whether to enable the search classifier. Default is False.",
    )
    is_chat_model: bool = Field(
        default=True,
        description="Whether this is a chat model or not. Default is True.",
    )
    timeout: float = Field(default=10.0, description="HTTP Timeout")

    def__init__(
        self,
        model: str = "sonar-pro",
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = "https://api.perplexity.ai",
        additional_kwargs: Optional[dict[str, Any]] = None,
        max_retries: int = 10,
        context_window: Optional[int] = None,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        enable_search_classifier: bool = False,
        timeout: float = 30.0,
        **kwargs: Any,
    ) -> None:
        api_key = api_key or getenv("PPLX_API_KEY")
        additional_kwargs = additional_kwargs or {}
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {api_key}",
        }
        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            additional_kwargs=additional_kwargs,
            max_retries=max_retries,
            callback_manager=callback_manager,
            api_key=api_key,
            api_base=api_base,
            headers=headers,
            context_window=context_window,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
            enable_search_classifier=enable_search_classifier,
            timeout=timeout,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "perplexity_llm"

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=(
                self.context_window
                if self.context_window is not None
                else self._get_context_window()
            ),
            num_output=self.max_tokens or -1,
            is_chat_model=self.is_chat_model,
            model_name=self.model,
        )

    def_get_context_window(self) -> int:
"""
        For latest model information, check:
        https://docs.perplexity.ai/guides/model-cards.
        """
        model_context_windows = {
            "sonar-deep-research": 127072,
            "sonar-reasoning-pro": 127072,
            "sonar-reasoning": 127072,
            "sonar": 127072,
            "r1-1776": 127072,
            "sonar-pro": 200000,
        }
        return model_context_windows.get(self.model, 127072)

    def_get_all_kwargs(self, **kwargs: Any) -> dict[str, Any]:
"""Get all data for the request as a dictionary."""
        base_kwargs = {
            "model": self.model,
            "temperature": self.temperature,
            "enable_search_classifier": self.enable_search_classifier,
        }
        if self.max_tokens is not None:
            base_kwargs["max_tokens"] = self.max_tokens
        return {**base_kwargs, **self.additional_kwargs, **kwargs}

    def_complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        url = f"{self.api_base}/chat/completions"
        messages = [{"role": "user", "content": prompt}]
        if self.system_prompt:
            messages.insert(0, {"role": "system", "content": self.system_prompt})
        payload = {
            "model": self.model,
            "messages": messages,
            **self._get_all_kwargs(**kwargs),
        }
        response = requests.post(
            url, json=payload, headers=self.headers, timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()
        return CompletionResponse(
            text=data["choices"][0]["message"]["content"], raw=data
        )

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        @retry(stop=stop_after_attempt(self.max_retries), wait=wait_fixed(1))
        def_complete_retry():
            return self._complete(prompt, **kwargs)

        return _complete_retry()

    def_chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        url = f"{self.api_base}/chat/completions"
        message_dicts = to_openai_message_dicts(messages)
        payload = {
            "model": self.model,
            "messages": message_dicts,
            **self._get_all_kwargs(**kwargs),
        }
        response = requests.post(
            url, json=payload, headers=self.headers, timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()
        message = ChatMessage(
            role="assistant", content=data["choices"][0]["message"]["content"]
        )
        return ChatResponse(message=message, raw=data)

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        @retry(stop=stop_after_attempt(self.max_retries), wait=wait_fixed(1))
        def_chat_retry():
            return self._chat(messages, **kwargs)

        return _chat_retry()

    async def_acomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        url = f"{self.api_base}/chat/completions"
        messages = [{"role": "user", "content": prompt}]
        if self.system_prompt:
            messages.insert(0, {"role": "system", "content": self.system_prompt})
        payload = {
            "model": self.model,
            "messages": messages,
            **self._get_all_kwargs(**kwargs),
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, json=payload, headers=self.headers, timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            return CompletionResponse(
                text=data["choices"][0]["message"]["content"], raw=data
            )

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        @retry(stop=stop_after_attempt(self.max_retries), wait=wait_fixed(1))
        async def_acomplete_retry(prompt, **kwargs):
            return await self._acomplete(prompt, **kwargs)

        return await _acomplete_retry(prompt, **kwargs)

    async def_achat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        message_dicts = to_openai_message_dicts(messages)
        payload = {
            "model": self.model,
            "messages": message_dicts,
            **self._get_all_kwargs(**kwargs),
        }

        url = f"{self.api_base}/chat/completions"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, json=payload, headers=self.headers, timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            message = ChatMessage(
                role="assistant", content=data["choices"][0]["message"]["content"]
            )
            return ChatResponse(message=message, raw=data)

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        @retry(stop=stop_after_attempt(self.max_retries), wait=wait_fixed(1))
        async def_achat_retry():
            return await self._achat(messages, **kwargs)

        return await _achat_retry()

    def_stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        url = f"{self.api_base}/chat/completions"
        messages = [{"role": "user", "content": prompt}]
        if self.system_prompt:
            messages.insert(0, {"role": "system", "content": self.system_prompt})
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            **self._get_all_kwargs(**kwargs),
        }

        @retry(stop=stop_after_attempt(self.max_retries), wait=wait_fixed(1))
        defmake_request():
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                stream=True,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response

        defgen() -> CompletionResponseGen:
            response = make_request()
            text = ""

            for line in response.iter_lines(decode_unicode=True):
                if line.startswith("data:"):
                    line = line[5:]  # Remove "data: " prefix
                    if line.strip() == "[DONE]":
                        break
                    try:
                        data = json.loads(line)
                        if "choices" in data and data["choices"]:
                            delta = data["choices"][0]["delta"].get("content", "")
                            if delta:
                                text += delta
                                yield CompletionResponse(
                                    delta=delta, text=text, raw=data
                                )
                    except json.JSONDecodeError:
                        continue  # Skip malformed JSON

        return gen()

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        return self._stream_complete(prompt, **kwargs)

    async def_astream_complete(
        self, prompt: str, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        url = f"{self.api_base}/chat/completions"
        messages = [{"role": "user", "content": prompt}]
        if self.system_prompt:
            messages.insert(0, {"role": "system", "content": self.system_prompt})
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            **self._get_all_kwargs(**kwargs),
        }

        @retry(stop=stop_after_attempt(self.max_retries), wait=wait_fixed(1))
        async defmake_request():
            async with aiohttp.ClientSession() as session:
                response = await session.post(
                    url, json=payload, headers=self.headers, timeout=self.timeout
                )
                response.raise_for_status()
                return response

        async defgen() -> CompletionResponseAsyncGen:
            response = await make_request()
            text = ""

            async for line in response.content:
                line_text = line.decode("utf-8").strip()
                if line_text.startswith("data:"):
                    line_text = line_text[5:]
                    if line_text.strip() == "[DONE]":
                        break
                    try:
                        data = json.loads(line_text)
                        if "choices" in data and data["choices"]:
                            delta = data["choices"][0]["delta"].get("content", "")
                            if delta:
                                text += delta
                                yield CompletionResponse(
                                    delta=delta, text=text, raw=data
                                )
                    except json.JSONDecodeError:
                        continue  # Skip malformed JSON

        return gen()

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        return await self._astream_complete(prompt, **kwargs)

    def_stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        url = f"{self.api_base}/chat/completions"
        message_dicts = to_openai_message_dicts(messages)
        payload = {
            "model": self.model,
            "messages": message_dicts,
            "stream": True,
            **self._get_all_kwargs(**kwargs),
        }

        @retry(stop=stop_after_attempt(self.max_retries), wait=wait_fixed(1))
        defmake_request():
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                stream=True,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response

        defgen() -> ChatResponseGen:
            response = make_request()
            text = ""

            for line in response.iter_lines(decode_unicode=True):
                if line.startswith("data:"):
                    line = line[5:]  # Remove "data: " prefix
                    if line.strip() == "[DONE]":
                        break
                    try:
                        data = json.loads(line)
                        if "choices" in data and data["choices"]:
                            delta = data["choices"][0]["delta"].get("content", "")
                            if delta:
                                text += delta
                                yield ChatResponse(
                                    message=ChatMessage(role="assistant", content=text),
                                    delta=delta,
                                    raw=data,
                                )
                    except json.JSONDecodeError:
                        continue  # Skip malformed JSON

        return gen()

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        return self._stream_chat(messages, **kwargs)

    async def_astream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        url = f"{self.api_base}/chat/completions"
        message_dicts = to_openai_message_dicts(messages)
        payload = {
            "model": self.model,
            "messages": message_dicts,
            "stream": True,
            **self._get_all_kwargs(**kwargs),
        }

        @retry(stop=stop_after_attempt(self.max_retries), wait=wait_fixed(1))
        async defmake_request():
            async with aiohttp.ClientSession() as session:
                response = await session.post(
                    url, json=payload, headers=self.headers, timeout=self.timeout
                )
                response.raise_for_status()
                return response

        async defgen():
            response = await make_request()
            text = ""

            async for line in response.content:
                line_text = line.decode("utf-8").strip()
                if line_text.startswith("data:"):
                    line_text = line_text[5:]
                    if line_text.strip() == "[DONE]":
                        break
                    try:
                        data = json.loads(line_text)
                        if "choices" in data and data["choices"]:
                            delta = data["choices"][0]["delta"].get("content", "")
                            if delta:
                                text += delta
                                yield ChatResponse(
                                    message=ChatMessage(role="assistant", content=text),
                                    delta=delta,
                                    raw=data,
                                )
                    except json.JSONDecodeError:
                        continue  # Skip malformed JSON

        return gen()

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        return await self._astream_chat(messages, **kwargs)

```
 |  
| --- | --- |  
options: members: - Perplexity
