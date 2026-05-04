# Cortex
##  Cortex [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cortex/#llama_index.llms.cortex.Cortex "Permanent link")
Bases: `CustomLLM`
Cortex LLM.
This class provides an interface to Snowflake's Cortex LLM service. HTTP errors from the API (including invalid model names) will raise requests.exceptions.HTTPError for synchronous methods or aiohttp.ClientResponseError for asynchronous methods.
This class provides an interface to Snowflake's Cortex LLM service. HTTP errors from the API (including invalid model names) will raise requests.exceptions.HTTPError for synchronous methods or aiohttp.ClientResponseError for asynchronous methods.
Examples:
`pip install llama-index-llms-cortex`

```
fromllama_index.llms.corteximport Cortex


llm = Cortex(
    model="llama3.2-1b",
    user=your_sf_user,
    account=your_sf_account,
    private_key_file=your_sf_private_key_file
)

completion_response = llm.complete(
    "write me a haiku about a snowflake",
    temperature=0.0
)
print(completion_response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-cortex/llama_index/llms/cortex/base.py`  
| 
```
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
```
 | 
```
classCortex(CustomLLM):
"""
    Cortex LLM.

    This class provides an interface to Snowflake's Cortex LLM service.
    HTTP errors from the API (including invalid model names) will raise
    requests.exceptions.HTTPError for synchronous methods or
    aiohttp.ClientResponseError for asynchronous methods.

    This class provides an interface to Snowflake's Cortex LLM service.
    HTTP errors from the API (including invalid model names) will raise
    requests.exceptions.HTTPError for synchronous methods or
    aiohttp.ClientResponseError for asynchronous methods.

    Examples:
        `pip install llama-index-llms-cortex`

        ```python
        from llama_index.llms.cortex import Cortex


        llm = Cortex(
            model="llama3.2-1b",
            user=your_sf_user,
            account=your_sf_account,
            private_key_file=your_sf_private_key_file


        completion_response = llm.complete(
            "write me a haiku about a snowflake",
            temperature=0.0

        print(completion_response)
        ```

    """

    user: str = Field(
        description="Snowflake user.",
        default=os.environ.get("SNOWFLAKE_USERNAME", None),
    )
    account: str = Field(
        description="Fully qualified snowflake account specified as <ORG_ID>-<ACCOUNT_ID>.",
        default=os.environ.get("SNOWFLAKE_ACCOUNT", None),
    )
    private_key_file: str = Field(
        description="Filepath to snowflake private key file.",
        default=os.environ.get("SNOWFLAKE_KEY_FILE", None),
    )
    context_window: int = Field(
        default=None,
        description="The maximum number of context tokens for the model.",
    )
    max_tokens: int = Field(
        default=None,
        description="The maximum number of tokens to generate in response.",
    )
    model: str = Field(default=DEFAULT_MODEL, description="The model to use.")

    jwt_token: str = Field(default=None, description="JWT token data or filepath")
    session: Optional[Any] = Field(default=None, description="Snowpark Session object.")

    def__init__(
        self,
        model: str = DEFAULT_MODEL,
        user: Optional[str] = None,
        account: Optional[str] = None,
        private_key_file: Optional[str] = None,
        jwt_token: Optional[str] = None,
        session: Optional[Any] = None,
        callback_manager: Optional[CallbackManager] = None,
        additional_kwargs: Optional[Dict[str, Any]] = None,
    ) -> None:
"""
        Implements all Snowflake Cortex LLMs.

        AUTHENTICATION:
        The recommended way to connect is to use a snowflake.snowpark.Session object.
        Environment variables SNOWFLAKE_ACCOUNT and SNOWFLAKE_USERNAME must be set or passed as params.

        Authentication methods (in order of precedence):
        1. Explicitly provided authentication (one of: private_key_file, jwt_token, or session)
        2. Environment variable SNOWFLAKE_KEY_FILE (legacy support)
        3. Default OAUTH token in SPCS environment

        If none of these methods are available, an assertion error is raised.

        """
        super().__init__(
            additional_kwargs=additional_kwargs or {},
            callback_manager=callback_manager,
        )

        # Set model specs first
        self.model = model
        specs = model_specs.get(self.model, {})
        self.context_window = specs.get("context_window") or DEFAULT_CONTEXT_WINDOW
        self.max_tokens = specs.get("max_output") or DEFAULT_MAX_TOKENS

        # Set user and account
        self.user = user or os.environ.get("SNOWFLAKE_USERNAME")
        self.account = account or os.environ.get("SNOWFLAKE_ACCOUNT")

        # Authentication logic - prioritize explicit authentication methods
        is_in_spcs = is_spcs_environment()
        env_key_file = os.environ.get("SNOWFLAKE_KEY_FILE")

        # Case 1: Explicit authentication provided
        if private_key_file:
            self.private_key_file = private_key_file
        elif jwt_token:
            if os.path.isfile(jwt_token):
                with open(jwt_token) as fp:
                    self.jwt_token = fp.read()
            else:
                self.jwt_token = jwt_token
        elif session:
            self.session = session

        # Case 2: Environment variable private key (legacy behavior)
        elif env_key_file and not is_in_spcs:
            self.private_key_file = env_key_file

        # Case 3: SPCS environment with default token
        elif is_in_spcs:
            self.jwt_token = get_default_spcs_token()

        # No valid authentication method found
        else:
            raise ValueError(
                "Authentication required. Please provide one of: private_key_file, jwt_token, session, "
                "set SNOWFLAKE_KEY_FILE environment variable, or run in SPCS environment."
            )
        if is_in_spcs and self.session:
            warnings.warn(
                "SPCS environment detected. If using the default auth token, please ensure you do NOT set values for 'user' and 'role' parameters or your auth may be rejected."
            )

    @property
    defmetadata(self) -> LLMMetadata:
"""Get LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.max_tokens,
            is_chat_model=True,
            model_name=self.model,
            is_function_calling_model=False,
        )

    @property
    defsnowflake_api_endpoint(self) -> str:
        if is_spcs_environment():
            return get_spcs_base_url()
        else:
            base_url = f"https://{self.account}.snowflakecomputing.com"
        return base_url

    @property
    defcortex_complete_endpoint(self) -> str:
        append = "/api/v2/cortex/inference:complete"
        return self.snowflake_api_endpoint + append

    @property
    defsnowflake_api_endpoint(self) -> str:
        if is_spcs_environment():
            return "https://" + get_spcs_base_url()
        else:
            base_url = f"https://{self.account}.snowflakecomputing.com"
        return base_url

    @property
    defcortex_complete_endpoint(self) -> str:
        append = "/api/v2/cortex/inference:complete"
        return self.snowflake_api_endpoint + append

    def_make_completion_payload(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> dict:
"""Create a payload for the completions."""
        temperature = kwargs.pop("temperature", DEFAULT_TEMP)
        top_p = kwargs.pop("top_p", DEFAULT_TOP_P)
        max_tokens = kwargs.pop("max_tokens", self.max_tokens)
        if not formatted:
            prompt = prompt.format(**kwargs)
        return {
            "url": self.cortex_complete_endpoint,
            "url": self.cortex_complete_endpoint,
            "headers": {
                "Authorization": self._generate_auth_header(),
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            },
            "json": {
                "model": self.model,
                "messages": [{"content": prompt}],
                "top_p": top_p,
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
        }

    def_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        api_response = requests.post(
            **self._make_completion_payload(prompt, formatted, **kwargs), stream=True
        )
        api_response.raise_for_status()
        api_response.raise_for_status()
        responses = []
        for line in api_response.iter_lines(decode_unicode=True):
            if line:
                responses.append(json.loads(line[len("data: ") :]))
        return CompletionResponse(
            text="".join(r["choices"][0]["delta"].get("content", "") for r in responses)
        )

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        return self._complete(prompt, formatted, **kwargs)

    async def_acomplete(self, prompt, formatted=False, **kwargs) -> CompletionResponse:
        async with aiohttp.ClientSession() as session:
            api_response = await session.post(
                **self._make_completion_payload(prompt, formatted, **kwargs)
            )
            await api_response.raise_for_status()
            await api_response.raise_for_status()
            responses = []
            async for line in api_response.content:
                line = line.decode()
                if line and (line != "\n"):
                    x = line.strip()[len("data: ") :].strip("\n")
                    responses.append(json.loads(x))
            return CompletionResponse(
                text="".join(
                    r["choices"][0]["delta"].get("content", "") for r in responses
                )
            )

    @llm_completion_callback()
    async defacomplete(self, prompt, formatted=False, **kwargs) -> CompletionResponse:
        return await self._acomplete(prompt, formatted, **kwargs)

    def_stream_complete(
        self, prompt, formatted=False, **kwargs
    ) -> CompletionResponseGen:
        api_response = requests.post(
            **self._make_completion_payload(prompt, formatted, **kwargs), stream=True
        )
        api_response.raise_for_status()
        api_response.raise_for_status()

        defgen() -> CompletionResponseGen:
            text = ""
            for line in api_response.iter_lines():
                if line:
                    line_json = json.loads(line[len("data: ") :])
                    line_delta = line_json["choices"][0]["delta"].get("content", "")
                    text += line_delta
                    yield CompletionResponse(text=text, delta=line_delta, raw=line_json)

        return gen()

    @llm_completion_callback()
    defstream_complete(
        self, prompt, formatted=False, **kwargs
    ) -> CompletionResponseGen:
        return self._stream_complete(prompt, formatted, **kwargs)

    async def_astream_complete(
        self, prompt, formatted=False, **kwargs
    ) -> CompletionResponseAsyncGen:
        async defgen() -> CompletionResponseAsyncGen:
            async with aiohttp.ClientSession() as session:
                api_response = await session.post(
                    **self._make_completion_payload(prompt, formatted, **kwargs)
                )
                text = ""
                async for line in api_response.content:
                    line = line.decode()
                    if line and (line != "\n") and line.startswith("data: "):
                        line_json = json.loads(line[len("data: ") :].strip("\n"))
                        line_delta = line_json["choices"][0]["delta"].get("content", "")
                        text += line_delta
                        yield CompletionResponse(
                            text=text, delta=line_delta, raw=line_json
                        )

        async defgen() -> CompletionResponseAsyncGen:
            async with aiohttp.ClientSession() as session:
                api_response = await session.post(
                    **self._make_completion_payload(prompt, formatted, **kwargs)
                )
                text = ""
                async for line in api_response.content:
                    line = line.decode()
                    if line and (line != "\n") and line.startswith("data: "):
                        line_json = json.loads(line[len("data: ") :].strip("\n"))
                        line_delta = line_json["choices"][0]["delta"].get("content", "")
                        text += line_delta
                        yield CompletionResponse(
                            text=text, delta=line_delta, raw=line_json
                        )

        return gen()

    def_generate_auth_header(self) -> str:
        # private key file has to be checked 2nd to last,
        # it can be set merely due to an env variable existing
        if self.jwt_token:
            return f"Bearer {self.jwt_token}"
        elif self.session:
            return f'Snowflake Token="{self.session.connection.rest.token}"'
        elif self.private_key_file:
            return f"Bearer {generate_sf_jwt(self.account,self.user,self.private_key_file)}"
        else:
            raise ValueError(
                "llama-index Cortex LLM Error: No authentication method set."
            )

    @llm_completion_callback()
    async defastream_complete(
        self, prompt, formatted=False, **kwargs
    ) -> CompletionResponseAsyncGen:
        return await self._astream_complete(prompt, formatted, **kwargs)

    def_make_chat_payload(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> dict:
"""Create a payload for a chat."""
        temperature = kwargs.pop("temperature", DEFAULT_TEMP)
        top_p = kwargs.pop("top_p", DEFAULT_TOP_P)
        max_tokens = kwargs.pop("max_tokens", self.max_tokens)
        jwt = self._generate_auth_header()
        return {
            "url": self.cortex_complete_endpoint,
            "url": self.cortex_complete_endpoint,
            "headers": {
                "Authorization": self._generate_auth_header(),
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            },
            "json": {
                "model": self.model,
                "messages": [
                    {"role": message.role.lower(), "content": message.content}
                    for message in messages
                ],
                "top_p": top_p,
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
        }

    def_chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        api_response = requests.post(
            **self._make_chat_payload(messages, **kwargs), stream=True
        )
        api_response.raise_for_status()
        api_response.raise_for_status()
        responses = []
        for line in api_response.iter_lines(decode_unicode=True):
            if line:
                responses.append(json.loads(line[len("data: ") :]))
        return ChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT,
                content="".join(
                    r["choices"][0]["delta"].get("content", "") for r in responses
                ),
            ),
        )

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        return self._chat(messages, **kwargs)

    async def_achat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        async with aiohttp.ClientSession() as session:
            api_response = await session.post(
                **self._make_chat_payload(messages, **kwargs)
            )
            await api_response.raise_for_status()
            await api_response.raise_for_status()
            responses = []
            async for line in api_response.content:
                line = line.decode()
                if line and (line != "\n"):
                    responses.append(json.loads(line[len("data: ") :].strip("\n")))
            return ChatResponse(
                message=ChatMessage(
                    role=MessageRole.ASSISTANT,
                    content="".join(
                        r["choices"][0]["delta"].get("content", "") for r in responses
                    ),
                ),
            )

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        return await self._achat(messages, **kwargs)

    def_stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        api_response = requests.post(
            **self._make_chat_payload(messages, **kwargs), stream=True
        )
        api_response.raise_for_status()
        api_response.raise_for_status()

        defgen() -> ChatResponseGen:
            text = ""
            for line in api_response.iter_lines():
                if line:
                    line_json = json.loads(line[len("data: ") :])
                    line_delta = line_json["choices"][0]["delta"].get("content", "")
                    text += line_delta
                    yield ChatResponse(
                        message=ChatMessage(role=MessageRole.ASSISTANT, content=text),
                        delta=line_delta,
                        raw=line_json,
                    )

        return gen()

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        return self._stream_chat(messages, **kwargs)

    async def_astream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        async with aiohttp.ClientSession() as session:
            api_response = await session.post(
                **self._make_chat_payload(messages, **kwargs)
            )
            await api_response.raise_for_status()
            await api_response.raise_for_status()
            # buffer data
            lines = []
            async for line in api_response.content:
                line = line.decode()
                if line and (line != "\n"):
                    lines.append(line)

        async defgen() -> ChatResponseAsyncGen:
            text = ""
            for line in lines:
                line_json = json.loads(line[len("data: ") :].strip("\n"))
                line_delta = line_json["choices"][0]["delta"].get("content", "")
                text += line_delta
                yield ChatResponse(
                    message=ChatMessage(role=MessageRole.ASSISTANT, content=text),
                    delta=line_delta,
                    raw=line_json,
                )

        return gen()

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        return await self._astream_chat(messages, **kwargs)

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cortex/#llama_index.llms.cortex.Cortex.metadata "Permanent link")

```
metadata: 

```

Get LLM metadata.
options: members: - Cortex
