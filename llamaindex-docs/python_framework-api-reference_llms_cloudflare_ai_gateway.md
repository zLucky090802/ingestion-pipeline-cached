# Cloudflare ai gateway
##  CloudflareAIGateway [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cloudflare_ai_gateway/#llama_index.llms.cloudflare_ai_gateway.CloudflareAIGateway "Permanent link")
Bases: 
Cloudflare AI Gateway LLM.
This class intercepts requests to multiple LLM providers and routes them through Cloudflare AI Gateway for automatic fallback and load balancing.
The key concept is that you provide multiple LLM instances (from different providers), and this class intercepts their requests, transforms them for AI Gateway, and delegates the actual LLM functionality to the first available provider.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `llms`  |   |  List of LLM instances to use (will be tried in order)  |  _required_  |  
|  `account_id`  |  `Optional[str]`  |  Your Cloudflare account ID  |  `None`  |  
|  `gateway`  |  `Optional[str]`  |  The name of your AI Gateway  |  `None`  |  
|  `api_key`  |  `Optional[str]`  |  Your Cloudflare API key (optional if using binding)  |  `None`  |  
|  `binding`  |  `Optional[Any]`  |  Cloudflare AI Gateway binding (alternative to account_id/gateway/api_key)  |  `None`  |  
|  `options`  |  `Optional[CloudflareAIGatewayOptions[](https://developers.llamaindex.ai/python/framework-api-reference/llms/cloudflare_ai_gateway/#llama_index.llms.cloudflare_ai_gateway.CloudflareAIGatewayOptions "CloudflareAIGatewayOptions \(llama_index.llms.cloudflare_ai_gateway.base.CloudflareAIGatewayOptions\)")]`  |  Request-level options for AI Gateway  |  `None`  |  
|  `max_retries`  |  Maximum number of retries for API calls  |  
|  `timeout`  |  `float`  |  Timeout for API requests in seconds  |  `60.0`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.CallbackManager\)")]`  |  Callback manager for observability  |  `None`  |  
|  `default_headers`  |  `Optional[Dict[str, str]]`  |  Default headers for API requests  |  `None`  |  
|  `http_client`  |  `Optional[Client]`  |  Custom httpx client  |  `None`  |  
|  `async_http_client`  |  `Optional[AsyncClient]`  |  Custom async httpx client  |  `None`  |  
Source code in `llama-index-integrations/llms/llama-index-llms-cloudflare-ai-gateway/llama_index/llms/cloudflare_ai_gateway/base.py`  
| 
```
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
```
 | 
```
classCloudflareAIGateway(LLM):
"""
    Cloudflare AI Gateway LLM.

    This class intercepts requests to multiple LLM providers and routes them through
    Cloudflare AI Gateway for automatic fallback and load balancing.

    The key concept is that you provide multiple LLM instances (from different providers),
    and this class intercepts their requests, transforms them for AI Gateway, and
    delegates the actual LLM functionality to the first available provider.

    Args:
        llms: List of LLM instances to use (will be tried in order)
        account_id: Your Cloudflare account ID
        gateway: The name of your AI Gateway
        api_key: Your Cloudflare API key (optional if using binding)
        binding: Cloudflare AI Gateway binding (alternative to account_id/gateway/api_key)
        options: Request-level options for AI Gateway
        max_retries: Maximum number of retries for API calls
        timeout: Timeout for API requests in seconds
        callback_manager: Callback manager for observability
        default_headers: Default headers for API requests
        http_client: Custom httpx client
        async_http_client: Custom async httpx client
    """

    llms: List[LLM] = Field(
        description="List of LLM instances to use (will be tried in order)"
    )
    account_id: Optional[str] = Field(
        default=None, description="Your Cloudflare account ID"
    )
    gateway: Optional[str] = Field(
        default=None, description="The name of your AI Gateway"
    )
    api_key: Optional[str] = Field(default=None, description="Your Cloudflare API key")
    binding: Optional[Any] = Field(
        default=None, description="Cloudflare AI Gateway binding"
    )
    options: Optional[CloudflareAIGatewayOptions] = Field(
        default=None, description="Request-level options for AI Gateway"
    )
    max_retries: int = Field(
        default=3, description="Maximum number of retries for API calls", ge=0
    )
    timeout: float = Field(
        default=60.0, description="Timeout for API requests in seconds", ge=0
    )
    default_headers: Optional[Dict[str, str]] = Field(
        default=None, description="Default headers for API requests"
    )
    http_client: Optional[httpx.Client] = Field(
        default=None, description="Custom httpx client"
    )
    async_http_client: Optional[httpx.AsyncClient] = Field(
        default=None, description="Custom async httpx client"
    )

    _client: Optional[httpx.Client] = PrivateAttr()
    _aclient: Optional[httpx.AsyncClient] = PrivateAttr()
    _current_llm_index: int = PrivateAttr(default=0)
    _original_clients: Dict[int, Any] = PrivateAttr(default_factory=dict)
    _original_async_clients: Dict[int, Any] = PrivateAttr(default_factory=dict)

    def__init__(
        self,
        llms: List[LLM],
        account_id: Optional[str] = None,
        gateway: Optional[str] = None,
        api_key: Optional[str] = None,
        binding: Optional[Any] = None,
        options: Optional[CloudflareAIGatewayOptions] = None,
        max_retries: int = 3,
        timeout: float = 60.0,
        callback_manager: Optional[CallbackManager] = None,
        default_headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
        async_http_client: Optional[httpx.AsyncClient] = None,
        **kwargs: Any,
    ) -> None:
        # Validate configuration
        if not llms:
            raise ValueError("At least one LLM must be provided")

        if binding is None:
            if not account_id or not gateway:
                raise ValueError(
                    "Either binding or account_id+gateway must be provided"
                )
            if not api_key:
                raise ValueError("api_key is required when not using binding")

        super().__init__(
            llms=llms,
            account_id=account_id,
            gateway=gateway,
            api_key=api_key,
            binding=binding,
            options=options,
            max_retries=max_retries,
            timeout=timeout,
            callback_manager=callback_manager,
            default_headers=default_headers,
            http_client=http_client,
            async_http_client=async_http_client,
            **kwargs,
        )

        self._client = http_client
        self._aclient = async_http_client

        # Inject AI Gateway client into each LLM
        self._inject_ai_gateway_clients()

    def_inject_ai_gateway_clients(self) -> None:
"""Inject AI Gateway client into each LLM to intercept requests."""
        for i, llm in enumerate(self.llms):
            # Store original client if it exists
            if hasattr(llm, "_client") and llm._client is not None:
                self._original_clients[i] = llm._client
                llm._client = AIGatewayClientWrapper(self, llm._client, llm)

            # Store original async client if it exists
            if hasattr(llm, "_aclient") and llm._aclient is not None:
                self._original_async_clients[i] = llm._aclient
                llm._aclient = AIGatewayClientWrapper(self, llm._aclient, llm)

    def_get_client(self) -> httpx.Client:
"""Get HTTP client."""
        if self._client is None:
            self._client = httpx.Client(
                timeout=self.timeout,
                headers=self.default_headers,
            )
        return self._client

    def_get_aclient(self) -> httpx.AsyncClient:
"""Get async HTTP client."""
        if self._aclient is None:
            self._aclient = httpx.AsyncClient(
                timeout=self.timeout,
                headers=self.default_headers,
            )
        return self._aclient

    def_parse_options_to_headers(
        self, options: Optional[CloudflareAIGatewayOptions]
    ) -> Dict[str, str]:
"""Parse options to headers."""
        headers = {}

        if options is None:
            return headers

        if options.skip_cache:
            headers["cf-skip-cache"] = "true"

        if options.cache_ttl is not None:
            headers["cf-cache-ttl"] = str(options.cache_ttl)

        if options.metadata:
            headers["cf-aig-metadata"] = json.dumps(options.metadata)

        if options.collect_log is not None:
            headers["cf-aig-collect-log"] = str(options.collect_log).lower()

        if options.event_id:
            headers["cf-aig-event-id"] = options.event_id

        if options.request_timeout_ms is not None:
            headers["cf-aig-request-timeout-ms"] = str(options.request_timeout_ms)

        return headers

    def_get_current_llm(self) -> LLM:
"""Get the current LLM to use."""
        if not self.llms:
            raise CloudflareAIGatewayError("No LLMs configured")
        return self.llms[self._current_llm_index % len(self.llms)]

    def_try_next_llm(self) -> None:
"""Try the next LLM in the list."""
        self._current_llm_index += 1
        if self._current_llm_index >= len(self.llms):
            raise CloudflareAIGatewayError("All LLMs failed")

    def_make_ai_gateway_request(self, request_body: Dict[str, Any]) -> httpx.Response:
"""Make request to AI Gateway."""
        if self.binding is not None:
            # Use binding - this would need to be implemented based on the binding interface
            raise NotImplementedError("Binding support not yet implemented")
        else:
            # Use API
            headers = self._parse_options_to_headers(self.options)
            headers.update(
                {
                    "Content-Type": "application/json",
                    "cf-aig-authorization": f"Bearer {self.api_key}",
                }
            )

            url = (
                f"https://gateway.ai.cloudflare.com/v1/{self.account_id}/{self.gateway}"
            )

            client = self._get_client()
            response = client.post(url, json=request_body, headers=headers)

            # Handle response
            self._handle_ai_gateway_response(response)

            return response

    def_handle_ai_gateway_response(self, response: httpx.Response) -> None:
"""Handle AI Gateway response and check for errors."""
        if response.status_code == 400:
            try:
                result = response.json()
                if (
                    not result.get("success")
                    and result.get("error")
                    and result["error"][0].get("code") == 2001
                ):
                    raise CloudflareAIGatewayDoesNotExistError(
                        "This AI gateway does not exist"
                    )
            except (ValueError, KeyError, IndexError):
                pass
            raise CloudflareAIGatewayError(f"Bad request: {response.text}")

        elif response.status_code == 401:
            try:
                result = response.json()
                if (
                    not result.get("success")
                    and result.get("error")
                    and result["error"][0].get("code") == 2009
                ):
                    raise CloudflareAIGatewayUnauthorizedError(
                        "Your AI Gateway has authentication active, but you didn't provide a valid apiKey"
                    )
            except (ValueError, KeyError, IndexError):
                pass
            raise CloudflareAIGatewayError("Unauthorized")

        elif response.status_code != 200:
            raise CloudflareAIGatewayError(
                f"Request failed with status {response.status_code}: {response.text}"
            )

    @classmethod
    defclass_name(cls) -> str:
        return "CloudflareAIGateway"

    @property
    defmetadata(self) -> LLMMetadata:
"""Get LLM metadata from the current LLM."""
        current_llm = self._get_current_llm()
        return current_llm.metadata

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
"""Chat with the AI Gateway by delegating to the current LLM."""
        while True:
            try:
                current_llm = self._get_current_llm()
                return current_llm.chat(messages, **kwargs)
            except Exception as e:
                # Try next LLM on failure
                logger.warning(
                    f"It seems that the current LLM is not working with the AI Gateway. Error: {e}"
                )
                self._try_next_llm()
                continue

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
"""Stream chat with the AI Gateway by delegating to the current LLM."""
        while True:
            try:
                current_llm = self._get_current_llm()
                return current_llm.stream_chat(messages, **kwargs)
            except Exception as e:
                # Try next LLM on failure
                logger.warning(
                    f"It seems that the current LLM is not working with the AI Gateway. Error: {e}"
                )
                self._try_next_llm()
                continue

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
"""Complete a prompt using the AI Gateway by delegating to the current LLM."""
        while True:
            try:
                current_llm = self._get_current_llm()
                return current_llm.complete(prompt, formatted, **kwargs)
            except Exception as e:
                # Try next LLM on failure
                logger.warning(
                    f"It seems that the current LLM is not working with the AI Gateway. Error: {e}"
                )
                self._try_next_llm()
                continue

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
"""Stream complete a prompt using the AI Gateway by delegating to the current LLM."""
        while True:
            try:
                current_llm = self._get_current_llm()
                return current_llm.stream_complete(prompt, formatted, **kwargs)
            except Exception as e:
                # Try next LLM on failure
                logger.warning(
                    f"It seems that the current LLM is not working with the AI Gateway. Error: {e}"
                )
                self._try_next_llm()
                continue

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
"""Async chat with the AI Gateway by delegating to the current LLM."""
        while True:
            try:
                current_llm = self._get_current_llm()
                return await current_llm.achat(messages, **kwargs)
            except Exception as e:
                # Try next LLM on failure
                logger.warning(
                    f"It seems that the current LLM is not working with the AI Gateway. Error: {e}"
                )
                self._try_next_llm()
                continue

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
"""Async stream chat with the AI Gateway by delegating to the current LLM."""
        while True:
            try:
                current_llm = self._get_current_llm()
                return current_llm.astream_chat(messages, **kwargs)
            except Exception as e:
                # Try next LLM on failure
                logger.warning(
                    f"It seems that the current LLM is not working with the AI Gateway. Error: {e}"
                )
                self._try_next_llm()
                continue

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
"""Async complete a prompt using the AI Gateway by delegating to the current LLM."""
        while True:
            try:
                current_llm = self._get_current_llm()
                return await current_llm.acomplete(prompt, formatted, **kwargs)
            except Exception as e:
                # Try next LLM on failure
                logger.warning(
                    f"It seems that the current LLM is not working with the AI Gateway. Error: {e}"
                )
                self._try_next_llm()
                continue

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
"""Async stream complete a prompt using the AI Gateway by delegating to the current LLM."""
        while True:
            try:
                current_llm = self._get_current_llm()
                return current_llm.astream_complete(prompt, formatted, **kwargs)
            except Exception as e:
                # Try next LLM on failure
                logger.warning(
                    f"It seems that the current LLM is not working with the AI Gateway. Error: {e}"
                )
                self._try_next_llm()
                continue

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cloudflare_ai_gateway/#llama_index.llms.cloudflare_ai_gateway.CloudflareAIGateway.metadata "Permanent link")

```
metadata: 

```

Get LLM metadata from the current LLM.
###  chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cloudflare_ai_gateway/#llama_index.llms.cloudflare_ai_gateway.CloudflareAIGateway.chat "Permanent link")

```
chat(
    messages: Sequence[], **kwargs: 
) -> 

```

Chat with the AI Gateway by delegating to the current LLM.
Source code in `llama-index-integrations/llms/llama-index-llms-cloudflare-ai-gateway/llama_index/llms/cloudflare_ai_gateway/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
"""Chat with the AI Gateway by delegating to the current LLM."""
    while True:
        try:
            current_llm = self._get_current_llm()
            return current_llm.chat(messages, **kwargs)
        except Exception as e:
            # Try next LLM on failure
            logger.warning(
                f"It seems that the current LLM is not working with the AI Gateway. Error: {e}"
            )
            self._try_next_llm()
            continue

```
 |  
| --- | --- |  
###  stream_chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cloudflare_ai_gateway/#llama_index.llms.cloudflare_ai_gateway.CloudflareAIGateway.stream_chat "Permanent link")

```
stream_chat(
    messages: Sequence[], **kwargs: 
) -> ChatResponseGen

```

Stream chat with the AI Gateway by delegating to the current LLM.
Source code in `llama-index-integrations/llms/llama-index-llms-cloudflare-ai-gateway/llama_index/llms/cloudflare_ai_gateway/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
defstream_chat(
    self, messages: Sequence[ChatMessage], **kwargs: Any
) -> ChatResponseGen:
"""Stream chat with the AI Gateway by delegating to the current LLM."""
    while True:
        try:
            current_llm = self._get_current_llm()
            return current_llm.stream_chat(messages, **kwargs)
        except Exception as e:
            # Try next LLM on failure
            logger.warning(
                f"It seems that the current LLM is not working with the AI Gateway. Error: {e}"
            )
            self._try_next_llm()
            continue

```
 |  
| --- | --- |  
###  complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cloudflare_ai_gateway/#llama_index.llms.cloudflare_ai_gateway.CloudflareAIGateway.complete "Permanent link")

```
complete(
    prompt: , formatted:  = False, **kwargs: 
) -> 

```

Complete a prompt using the AI Gateway by delegating to the current LLM.
Source code in `llama-index-integrations/llms/llama-index-llms-cloudflare-ai-gateway/llama_index/llms/cloudflare_ai_gateway/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defcomplete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponse:
"""Complete a prompt using the AI Gateway by delegating to the current LLM."""
    while True:
        try:
            current_llm = self._get_current_llm()
            return current_llm.complete(prompt, formatted, **kwargs)
        except Exception as e:
            # Try next LLM on failure
            logger.warning(
                f"It seems that the current LLM is not working with the AI Gateway. Error: {e}"
            )
            self._try_next_llm()
            continue

```
 |  
| --- | --- |  
###  stream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cloudflare_ai_gateway/#llama_index.llms.cloudflare_ai_gateway.CloudflareAIGateway.stream_complete "Permanent link")

```
stream_complete(
    prompt: , formatted:  = False, **kwargs: 
) -> CompletionResponseGen

```

Stream complete a prompt using the AI Gateway by delegating to the current LLM.
Source code in `llama-index-integrations/llms/llama-index-llms-cloudflare-ai-gateway/llama_index/llms/cloudflare_ai_gateway/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defstream_complete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponseGen:
"""Stream complete a prompt using the AI Gateway by delegating to the current LLM."""
    while True:
        try:
            current_llm = self._get_current_llm()
            return current_llm.stream_complete(prompt, formatted, **kwargs)
        except Exception as e:
            # Try next LLM on failure
            logger.warning(
                f"It seems that the current LLM is not working with the AI Gateway. Error: {e}"
            )
            self._try_next_llm()
            continue

```
 |  
| --- | --- |  
###  achat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cloudflare_ai_gateway/#llama_index.llms.cloudflare_ai_gateway.CloudflareAIGateway.achat "Permanent link")

```
achat(
    messages: Sequence[], **kwargs: 
) -> 

```

Async chat with the AI Gateway by delegating to the current LLM.
Source code in `llama-index-integrations/llms/llama-index-llms-cloudflare-ai-gateway/llama_index/llms/cloudflare_ai_gateway/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
async defachat(
    self, messages: Sequence[ChatMessage], **kwargs: Any
) -> ChatResponse:
"""Async chat with the AI Gateway by delegating to the current LLM."""
    while True:
        try:
            current_llm = self._get_current_llm()
            return await current_llm.achat(messages, **kwargs)
        except Exception as e:
            # Try next LLM on failure
            logger.warning(
                f"It seems that the current LLM is not working with the AI Gateway. Error: {e}"
            )
            self._try_next_llm()
            continue

```
 |  
| --- | --- |  
###  astream_chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cloudflare_ai_gateway/#llama_index.llms.cloudflare_ai_gateway.CloudflareAIGateway.astream_chat "Permanent link")

```
astream_chat(
    messages: Sequence[], **kwargs: 
) -> ChatResponseAsyncGen

```

Async stream chat with the AI Gateway by delegating to the current LLM.
Source code in `llama-index-integrations/llms/llama-index-llms-cloudflare-ai-gateway/llama_index/llms/cloudflare_ai_gateway/base.py`  
| 
```
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
@llm_chat_callback()
async defastream_chat(
    self, messages: Sequence[ChatMessage], **kwargs: Any
) -> ChatResponseAsyncGen:
"""Async stream chat with the AI Gateway by delegating to the current LLM."""
    while True:
        try:
            current_llm = self._get_current_llm()
            return current_llm.astream_chat(messages, **kwargs)
        except Exception as e:
            # Try next LLM on failure
            logger.warning(
                f"It seems that the current LLM is not working with the AI Gateway. Error: {e}"
            )
            self._try_next_llm()
            continue

```
 |  
| --- | --- |  
###  acomplete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cloudflare_ai_gateway/#llama_index.llms.cloudflare_ai_gateway.CloudflareAIGateway.acomplete "Permanent link")

```
acomplete(
    prompt: , formatted:  = False, **kwargs: 
) -> 

```

Async complete a prompt using the AI Gateway by delegating to the current LLM.
Source code in `llama-index-integrations/llms/llama-index-llms-cloudflare-ai-gateway/llama_index/llms/cloudflare_ai_gateway/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
async defacomplete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponse:
"""Async complete a prompt using the AI Gateway by delegating to the current LLM."""
    while True:
        try:
            current_llm = self._get_current_llm()
            return await current_llm.acomplete(prompt, formatted, **kwargs)
        except Exception as e:
            # Try next LLM on failure
            logger.warning(
                f"It seems that the current LLM is not working with the AI Gateway. Error: {e}"
            )
            self._try_next_llm()
            continue

```
 |  
| --- | --- |  
###  astream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cloudflare_ai_gateway/#llama_index.llms.cloudflare_ai_gateway.CloudflareAIGateway.astream_complete "Permanent link")

```
astream_complete(
    prompt: , formatted:  = False, **kwargs: 
) -> CompletionResponseAsyncGen

```

Async stream complete a prompt using the AI Gateway by delegating to the current LLM.
Source code in `llama-index-integrations/llms/llama-index-llms-cloudflare-ai-gateway/llama_index/llms/cloudflare_ai_gateway/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
async defastream_complete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponseAsyncGen:
"""Async stream complete a prompt using the AI Gateway by delegating to the current LLM."""
    while True:
        try:
            current_llm = self._get_current_llm()
            return current_llm.astream_complete(prompt, formatted, **kwargs)
        except Exception as e:
            # Try next LLM on failure
            logger.warning(
                f"It seems that the current LLM is not working with the AI Gateway. Error: {e}"
            )
            self._try_next_llm()
            continue

```
 |  
| --- | --- |  
##  CloudflareAIGatewayError [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cloudflare_ai_gateway/#llama_index.llms.cloudflare_ai_gateway.CloudflareAIGatewayError "Permanent link")
Bases: `Exception`
Base exception for Cloudflare AI Gateway errors.
Source code in `llama-index-integrations/llms/llama-index-llms-cloudflare-ai-gateway/llama_index/llms/cloudflare_ai_gateway/base.py`  
| 
```
36
37
38
39
```
 | 
```
classCloudflareAIGatewayError(Exception):
"""Base exception for Cloudflare AI Gateway errors."""

    pass

```
 |  
| --- | --- |  
##  CloudflareAIGatewayUnauthorizedError [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cloudflare_ai_gateway/#llama_index.llms.cloudflare_ai_gateway.CloudflareAIGatewayUnauthorizedError "Permanent link")
Bases: 
Raised when AI Gateway authentication fails.
Source code in `llama-index-integrations/llms/llama-index-llms-cloudflare-ai-gateway/llama_index/llms/cloudflare_ai_gateway/base.py`  
| 
```
42
43
44
45
```
 | 
```
classCloudflareAIGatewayUnauthorizedError(CloudflareAIGatewayError):
"""Raised when AI Gateway authentication fails."""

    pass

```
 |  
| --- | --- |  
##  CloudflareAIGatewayDoesNotExistError [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cloudflare_ai_gateway/#llama_index.llms.cloudflare_ai_gateway.CloudflareAIGatewayDoesNotExistError "Permanent link")
Bases: 
Raised when AI Gateway does not exist.
Source code in `llama-index-integrations/llms/llama-index-llms-cloudflare-ai-gateway/llama_index/llms/cloudflare_ai_gateway/base.py`  
| 
```
48
49
50
51
```
 | 
```
classCloudflareAIGatewayDoesNotExistError(CloudflareAIGatewayError):
"""Raised when AI Gateway does not exist."""

    pass

```
 |  
| --- | --- |  
##  CloudflareAIGatewayOptions [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/cloudflare_ai_gateway/#llama_index.llms.cloudflare_ai_gateway.CloudflareAIGatewayOptions "Permanent link")
Bases: `BaseModel`
Options for Cloudflare AI Gateway requests.
Source code in `llama-index-integrations/llms/llama-index-llms-cloudflare-ai-gateway/llama_index/llms/cloudflare_ai_gateway/base.py`  
| 
```
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
```
 | 
```
classCloudflareAIGatewayOptions(BaseModel):
"""Options for Cloudflare AI Gateway requests."""

    cache_key: Optional[str] = Field(default=None, description="Custom cache key")
    cache_ttl: Optional[int] = Field(
        default=None, ge=0, description="Cache time-to-live in seconds"
    )
    skip_cache: bool = Field(default=False, description="Bypass caching")
    metadata: Optional[Dict[str, Union[str, int, bool, None]]] = Field(
        default=None, description="Custom metadata for the request"
    )
    collect_log: Optional[bool] = Field(
        default=None, description="Enable/disable log collection"
    )
    event_id: Optional[str] = Field(default=None, description="Custom event identifier")
    request_timeout_ms: Optional[int] = Field(
        default=None, ge=0, description="Request timeout in milliseconds"
    )

```
 |  
| --- | --- |  
options: members: - CloudflareAIGateway
