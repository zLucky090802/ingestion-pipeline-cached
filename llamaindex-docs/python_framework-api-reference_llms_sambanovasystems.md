# Sambanovasystems
##  SambaNovaCloud [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/sambanovasystems/#llama_index.llms.sambanovasystems.SambaNovaCloud "Permanent link")
Bases: 
SambaNova Cloud models.
Setup
To use, you should have the environment variables: `SAMBANOVA_URL` set with your SambaNova Cloud URL. `SAMBANOVA_API_KEY` set with your SambaNova Cloud API Key. http://cloud.sambanova.ai/. Additionally, download the following packages: `pip install llama-index-llms-sambanovasystems` `pip install sseclient-py`
Examples: 

```
SambaNovaCloud(
    sambanova_url = SambaNova cloud endpoint URL,
    sambanova_api_key = set with your SambaNova cloud API key,
    model = model name,
    max_tokens = max number of tokens to generate,
    temperature = model temperature,
    top_p = model top p,
    top_k = model top k,
    stream_options = include usage to get generation metrics
)

```

Key init args — completion params: model: str The name of the model to use, e.g., Meta-Llama-3-70B-Instruct. streaming: bool Whether to use streaming handler when using non streaming methods max_tokens: int max tokens to generate temperature: float model temperature top_p: float model top p top_k: int model top k stream_options: dict stream options, include usage to get generation metrics Key init args — client params: sambanova_url: str SambaNova Cloud Url sambanova_api_key: str SambaNova Cloud api key Instantiate: 

```
fromllama_index.llms.sambanovacloudimport SambaNovaCloud
llm = SambaNovaCloud(
    sambanova_url = SambaNova cloud endpoint URL,
    sambanova_api_key = set with your SambaNova cloud API key,
    model = model name,
    max_tokens = max number of tokens to generate,
    temperature = model temperature,
    top_p = model top p,
    top_k = model top k,
    stream_options = include usage to get generation metrics
    context_window = model context window
)

```

Complete: 

```
prompt = "Tell me about Naruto Uzumaki in one sentence"
response = llm.complete(prompt)

```

Chat: 

```
messages = [
    ChatMessage(role=MessageRole.SYSTEM, content=("You're a helpful assistant")),
    ChatMessage(role=MessageRole.USER, content="Tell me about Naruto Uzumaki in one sentence")
]
response = llm.chat(messages)

```

Stream: 

```
prompt = "Tell me about Naruto Uzumaki in one sentence"
messages = [
    ChatMessage(role=MessageRole.SYSTEM, content=("You're a helpful assistant")),
    ChatMessage(role=MessageRole.USER, content="Tell me about Naruto Uzumaki in one sentence")
]
for chunk in llm.stream_complete(prompt):
    print(chunk.text)
for chunk in llm.stream_chat(messages):
    print(chunk.message.content)

```

Async: 

```
prompt = "Tell me about Naruto Uzumaki in one sentence"
asyncio.run(llm.acomplete(prompt))
messages = [
    ChatMessage(role=MessageRole.SYSTEM, content=("You're a helpful assistant")),
    ChatMessage(role=MessageRole.USER, content="Tell me about Naruto Uzumaki in one sentence")
]
asyncio.run(llm.achat(chat_text_msgs))

```

Response metadata and usage 

```
messages = [
    ChatMessage(role=MessageRole.SYSTEM, content=("You're a helpful assistant")),
    ChatMessage(role=MessageRole.USER, content="Tell me about Naruto Uzumaki in one sentence")
]
metadata_and_usage = llm.chat(messages).message.additional_kwargs
print(metadata_and_usage)

```

Source code in `llama-index-integrations/llms/llama-index-llms-sambanovasystems/llama_index/llms/sambanovasystems/base.py`  
| 
```
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
```
 | 
```
classSambaNovaCloud(LLM):
"""
    SambaNova Cloud models.

    Setup:
        To use, you should have the environment variables:
        `SAMBANOVA_URL` set with your SambaNova Cloud URL.
        `SAMBANOVA_API_KEY` set with your SambaNova Cloud API Key.
        http://cloud.sambanova.ai/.
        Additionally, download the following packages:
        `pip install llama-index-llms-sambanovasystems`
        `pip install sseclient-py`
    Examples:
    ```python
    SambaNovaCloud(
        sambanova_url = SambaNova cloud endpoint URL,
        sambanova_api_key = set with your SambaNova cloud API key,
        model = model name,
        max_tokens = max number of tokens to generate,
        temperature = model temperature,
        top_p = model top p,
        top_k = model top k,
        stream_options = include usage to get generation metrics

    ```
    Key init args — completion params:
        model: str
            The name of the model to use, e.g., Meta-Llama-3-70B-Instruct.
        streaming: bool
            Whether to use streaming handler when using non streaming methods
        max_tokens: int
            max tokens to generate
        temperature: float
            model temperature
        top_p: float
            model top p
        top_k: int
            model top k
        stream_options: dict
            stream options, include usage to get generation metrics
    Key init args — client params:
        sambanova_url: str
            SambaNova Cloud Url
        sambanova_api_key: str
            SambaNova Cloud api key
    Instantiate:
            ```python
            from llama_index.llms.sambanovacloud import SambaNovaCloud
            llm = SambaNovaCloud(
                sambanova_url = SambaNova cloud endpoint URL,
                sambanova_api_key = set with your SambaNova cloud API key,
                model = model name,
                max_tokens = max number of tokens to generate,
                temperature = model temperature,
                top_p = model top p,
                top_k = model top k,
                stream_options = include usage to get generation metrics
                context_window = model context window


    Complete:
            ```python
            prompt = "Tell me about Naruto Uzumaki in one sentence"
            response = llm.complete(prompt)

    Chat:
            ```python
            messages = [
                ChatMessage(role=MessageRole.SYSTEM, content=("You're a helpful assistant")),
                ChatMessage(role=MessageRole.USER, content="Tell me about Naruto Uzumaki in one sentence")

            response = llm.chat(messages)

    Stream:
        ```python
        prompt = "Tell me about Naruto Uzumaki in one sentence"
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=("You're a helpful assistant")),
            ChatMessage(role=MessageRole.USER, content="Tell me about Naruto Uzumaki in one sentence")

        for chunk in llm.stream_complete(prompt):
            print(chunk.text)
        for chunk in llm.stream_chat(messages):
            print(chunk.message.content)
        ```
    Async:
        ```python
        prompt = "Tell me about Naruto Uzumaki in one sentence"
        asyncio.run(llm.acomplete(prompt))
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=("You're a helpful assistant")),
            ChatMessage(role=MessageRole.USER, content="Tell me about Naruto Uzumaki in one sentence")

        asyncio.run(llm.achat(chat_text_msgs))
        ```
    Response metadata and usage
        ```python
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=("You're a helpful assistant")),
            ChatMessage(role=MessageRole.USER, content="Tell me about Naruto Uzumaki in one sentence")

        metadata_and_usage = llm.chat(messages).message.additional_kwargs
        print(metadata_and_usage)
        ```
    """

    model_config = ConfigDict(
        protected_namespaces=("pydantic_model_",), arbitrary_types_allowed=True
    )

    sambanova_url: str = Field(description="SambaNova Cloud Url")

    sambanova_api_key: SecretStr = Field(description="SambaNova Cloud api key")

    model: str = Field(
        default="Meta-Llama-3.1-8B-Instruct",
        description="The name of the model",
    )

    streaming: bool = Field(
        default=False,
        description="Whether to use streaming handler when using non streaming methods",
    )

    context_window: int = Field(default=4096, description="context window")

    max_tokens: int = Field(default=1024, description="max tokens to generate")

    temperature: float = Field(default=0.7, description="model temperature")

    top_p: Optional[float] = Field(default=None, description="model top p")

    top_k: Optional[int] = Field(default=None, description="model top k")

    stream_options: dict = Field(
        default_factory=lambda: {"include_usage": True},
        description="stream options, include usage to get generation metrics",
    )

    @classmethod
    defclass_name(cls) -> str:
        return "SambaNovaCloud"

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.max_tokens,
            is_chat_model=True,
            model_name=self.model,
        )

    def__init__(self, **kwargs: Any) -> None:
"""Init and validate environment variables."""
        kwargs["sambanova_url"] = get_from_param_or_env(
            "sambanova_api_key",
            kwargs.get("sambanova_api_key"),
            "SAMBANOVA_URL",
            default="https://api.sambanova.ai/v1/chat/completions",
        )
        kwargs["sambanova_api_key"] = get_from_param_or_env(
            "sambanova_api_key", kwargs.get("sambanova_api_key"), "SAMBANOVA_API_KEY"
        )
        super().__init__(**kwargs)

    def_handle_request(
        self, messages_dicts: List[Dict], stop: Optional[List[str]] = None
    ) -> Dict[str, Any]:
"""
        Performs a post request to the LLM API.

        Args:
            messages_dicts: List of role / content dicts to use as input.
            stop: list of stop tokens
        Returns:
            A response dict.

        """
        data = {
            "messages": messages_dicts,
            "max_tokens": self.max_tokens,
            "stop": stop,
            "model": self.model,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
        }
        http_session = requests.Session()
        response = http_session.post(
            self.sambanova_url,
            headers={
                "Authorization": f"Bearer {self.sambanova_api_key.get_secret_value()}",
                "Content-Type": "application/json",
            },
            json=data,
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"Sambanova /complete call failed with status code "
                f"{response.status_code}.",
                f"{response.text}.",
            )
        response_dict = response.json()
        if response_dict.get("error"):
            raise RuntimeError(
                f"Sambanova /complete call failed with status code "
                f"{response.status_code}.",
                f"{response_dict}.",
            )
        return response_dict

    async def_handle_request_async(
        self, messages_dicts: List[Dict], stop: Optional[List[str]] = None
    ) -> Dict[str, Any]:
"""
        Performs a async post request to the LLM API.

        Args:
            messages_dicts: List of role / content dicts to use as input.
            stop: list of stop tokens
        Returns:
            A response dict.

        """
        data = {
            "messages": messages_dicts,
            "max_tokens": self.max_tokens,
            "stop": stop,
            "model": self.model,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.sambanova_url,
                headers={
                    "Authorization": f"Bearer {self.sambanova_api_key.get_secret_value()}",
                    "Content-Type": "application/json",
                },
                json=data,
            ) as response:
                if response.status != 200:
                    raise RuntimeError(
                        f"Sambanova /complete call failed with status code {response.status}.",
                        f"{awaitresponse.text()}.",
                    )
                response_dict = await response.json()
                if response_dict.get("error"):
                    raise RuntimeError(
                        f"Sambanova /complete call failed with status code {response.status}.",
                        f"{response_dict}.",
                    )
                return response_dict

    def_handle_streaming_request(
        self, messages_dicts: List[Dict], stop: Optional[List[str]] = None
    ) -> Iterator[Dict]:
"""
        Performs an streaming post request to the LLM API.

        Args:
            messages_dicts: List of role / content dicts to use as input.
            stop: list of stop tokens
        Yields:
            An iterator of response dicts.

        """
        try:
            importsseclient
        except ImportError:
            raise ImportError(
                "could not import sseclient library"
                "Please install it with `pip install sseclient-py`."
            )
        data = {
            "messages": messages_dicts,
            "max_tokens": self.max_tokens,
            "stop": stop,
            "model": self.model,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "stream": True,
            "stream_options": self.stream_options,
        }
        http_session = requests.Session()
        response = http_session.post(
            self.sambanova_url,
            headers={
                "Authorization": f"Bearer {self.sambanova_api_key.get_secret_value()}",
                "Content-Type": "application/json",
            },
            json=data,
            stream=True,
        )

        client = sseclient.SSEClient(response)

        if response.status_code != 200:
            raise RuntimeError(
                f"Sambanova /complete call failed with status code "
                f"{response.status_code}."
                f"{response.text}."
            )

        for event in client.events():
            if event.event == "error_event":
                raise RuntimeError(
                    f"Sambanova /complete call failed with status code "
                    f"{response.status_code}."
                    f"{event.data}."
                )

            try:
                # check if the response is a final event
                # in that case event data response is '[DONE]'
                if event.data != "[DONE]":
                    if isinstance(event.data, str):
                        data = json.loads(event.data)
                    else:
                        raise RuntimeError(
                            f"Sambanova /complete call failed with status code "
                            f"{response.status_code}."
                            f"{event.data}."
                        )
                    if data.get("error"):
                        raise RuntimeError(
                            f"Sambanova /complete call failed with status code "
                            f"{response.status_code}."
                            f"{event.data}."
                        )
                    yield data
            except Exception as e:
                raise RuntimeError(
                    f"Error getting content chunk raw streamed response: {e}"
                    f"data: {event.data}"
                )

    async def_handle_streaming_request_async(
        self, messages_dicts: List[Dict], stop: Optional[List[str]] = None
    ) -> AsyncIterator[Dict]:
"""
        Performs an async streaming post request to the LLM API.

        Args:
            messages_dicts: List of role / content dicts to use as input.
            stop: list of stop tokens
        Yields:
            An iterator of response dicts.

        """
        data = {
            "messages": messages_dicts,
            "max_tokens": self.max_tokens,
            "stop": stop,
            "model": self.model,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "stream": True,
            "stream_options": self.stream_options,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.sambanova_url,
                headers={
                    "Authorization": f"Bearer {self.sambanova_api_key.get_secret_value()}",
                    "Content-Type": "application/json",
                },
                json=data,
            ) as response:
                if response.status != 200:
                    raise RuntimeError(
                        f"Sambanova /complete call failed with status code "
                        f"{response.status}. {awaitresponse.text()}"
                    )

                async for line in response.content:
                    if line:
                        event = line.decode("utf-8").strip()

                    if event.startswith("data:"):
                        event = event[len("data:") :].strip()
                        if event == "[DONE]":
                            break
                    elif len(event) == 0:
                        continue

                    try:
                        data = json.loads(event)
                        if data.get("error"):
                            raise RuntimeError(
                                f"Sambanova /complete call failed: {data['error']}"
                            )
                        yield data
                    except json.JSONDecodeError:
                        raise RuntimeError(
                            f"Sambanova /complete call failed to decode response: {event}"
                        )
                    except Exception as e:
                        raise RuntimeError(
                            f"Error processing response: {e} data: {event}"
                        )

    @llm_chat_callback()
    defchat(
        self,
        messages: Sequence[ChatMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ChatResponse:
"""
        Calls the chat implementation of the SambaNovaCloud model.

        Args:
            messages: the prompt composed of a list of messages.
            stop: a list of strings on which the model should stop generating.
                  If generation stops due to a stop token, the stop token itself
                  SHOULD BE INCLUDED as part of the output. This is not enforced
                  across models right now, but it's a good practice to follow since
                  it makes it much easier to parse the output of the model
                  downstream and understand why generation stopped.

        Returns:
            ChatResponse with model generation

        """
        messages_dicts = _create_message_dicts(messages)

        response = self._handle_request(messages_dicts, stop)
        message = ChatMessage(
            role=MessageRole.ASSISTANT,
            content=response["choices"][0]["message"]["content"],
            additional_kwargs={
                "id": response["id"],
                "finish_reason": response["choices"][0]["finish_reason"],
                "usage": response.get("usage"),
                "model_name": response["model"],
                "system_fingerprint": response["system_fingerprint"],
                "created": response["created"],
            },
        )
        return ChatResponse(message=message)

    @llm_chat_callback()
    defstream_chat(
        self,
        messages: Sequence[ChatMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ChatResponseGen:
"""
        Streams the chat output of the SambaNovaCloud model.

        Args:
            messages: the prompt composed of a list of messages.
            stop: a list of strings on which the model should stop generating.
                  If generation stops due to a stop token, the stop token itself
                  SHOULD BE INCLUDED as part of the output. This is not enforced
                  across models right now, but it's a good practice to follow since
                  it makes it much easier to parse the output of the model
                  downstream and understand why generation stopped.

        Yields:
            ChatResponseGen with model partial generation

        """
        messages_dicts = _create_message_dicts(messages)

        finish_reason = None
        content = ""
        role = MessageRole.ASSISTANT

        for partial_response in self._handle_streaming_request(messages_dicts, stop):
            if len(partial_response["choices"])  0:
                content_delta = partial_response["choices"][0]["delta"]["content"]
                content += content_delta
                additional_kwargs = {
                    "id": partial_response["id"],
                    "finish_reason": partial_response["choices"][0].get(
                        "finish_reason"
                    ),
                }
            else:
                additional_kwargs = {
                    "id": partial_response["id"],
                    "finish_reason": finish_reason,
                    "usage": partial_response.get("usage"),
                    "model_name": partial_response["model"],
                    "system_fingerprint": partial_response["system_fingerprint"],
                    "created": partial_response["created"],
                }

            # yield chunk
            yield ChatResponse(
                message=ChatMessage(
                    role=role, content=content, additional_kwargs=additional_kwargs
                ),
                delta=content_delta,
                raw=partial_response,
            )

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        complete_fn = chat_to_completion_decorator(self.chat)
        return complete_fn(prompt, **kwargs)

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        stream_complete_fn = stream_chat_to_completion_decorator(self.stream_chat)
        return stream_complete_fn(prompt, **kwargs)

    ### Async ###
    @llm_chat_callback()
    async defachat(
        self,
        messages: Sequence[ChatMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ChatResponse:
"""
        Calls the async chat implementation of the SambaNovaCloud model.

        Args:
            messages: the prompt composed of a list of messages.
            stop: a list of strings on which the model should stop generating.
                  If generation stops due to a stop token, the stop token itself
                  SHOULD BE INCLUDED as part of the output. This is not enforced
                  across models right now, but it's a good practice to follow since
                  it makes it much easier to parse the output of the model
                  downstream and understand why generation stopped.

        Returns:
            ChatResponse with async model generation

        """
        messages_dicts = _create_message_dicts(messages)
        response = await self._handle_request_async(messages_dicts, stop)
        message = ChatMessage(
            role=MessageRole.ASSISTANT,
            content=response["choices"][0]["message"]["content"],
            additional_kwargs={
                "id": response["id"],
                "finish_reason": response["choices"][0]["finish_reason"],
                "usage": response.get("usage"),
                "model_name": response["model"],
                "system_fingerprint": response["system_fingerprint"],
                "created": response["created"],
            },
        )
        return ChatResponse(message=message)

    @llm_chat_callback()
    async defastream_chat(
        self,
        messages: Sequence[ChatMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ChatResponseAsyncGen:
        raise NotImplementedError(
            "SambaNovaCloud does not currently support async streaming."
        )

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        acomplete_fn = achat_to_completion_decorator(self.achat)
        return await acomplete_fn(prompt, **kwargs)

    @llm_completion_callback()
    defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        raise NotImplementedError(
            "SambaNovaCloud does not currently support async streaming."
        )

```
 |  
| --- | --- |  
###  chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/sambanovasystems/#llama_index.llms.sambanovasystems.SambaNovaCloud.chat "Permanent link")

```
chat(
    messages: Sequence[],
    stop: Optional[[]] = None,
    **kwargs: 
) -> 

```

Calls the chat implementation of the SambaNovaCloud model.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  the prompt composed of a list of messages.  |  _required_  |  
|  `stop`  |  `Optional[List[str]]`  |  a list of strings on which the model should stop generating. If generation stops due to a stop token, the stop token itself SHOULD BE INCLUDED as part of the output. This is not enforced across models right now, but it's a good practice to follow since it makes it much easier to parse the output of the model downstream and understand why generation stopped.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  ChatResponse with model generation  |  
Source code in `llama-index-integrations/llms/llama-index-llms-sambanovasystems/llama_index/llms/sambanovasystems/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
defchat(
    self,
    messages: Sequence[ChatMessage],
    stop: Optional[List[str]] = None,
    **kwargs: Any,
) -> ChatResponse:
"""
    Calls the chat implementation of the SambaNovaCloud model.

    Args:
        messages: the prompt composed of a list of messages.
        stop: a list of strings on which the model should stop generating.
              If generation stops due to a stop token, the stop token itself
              SHOULD BE INCLUDED as part of the output. This is not enforced
              across models right now, but it's a good practice to follow since
              it makes it much easier to parse the output of the model
              downstream and understand why generation stopped.

    Returns:
        ChatResponse with model generation

    """
    messages_dicts = _create_message_dicts(messages)

    response = self._handle_request(messages_dicts, stop)
    message = ChatMessage(
        role=MessageRole.ASSISTANT,
        content=response["choices"][0]["message"]["content"],
        additional_kwargs={
            "id": response["id"],
            "finish_reason": response["choices"][0]["finish_reason"],
            "usage": response.get("usage"),
            "model_name": response["model"],
            "system_fingerprint": response["system_fingerprint"],
            "created": response["created"],
        },
    )
    return ChatResponse(message=message)

```
 |  
| --- | --- |  
###  stream_chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/sambanovasystems/#llama_index.llms.sambanovasystems.SambaNovaCloud.stream_chat "Permanent link")

```
stream_chat(
    messages: Sequence[],
    stop: Optional[[]] = None,
    **kwargs: 
) -> ChatResponseGen

```

Streams the chat output of the SambaNovaCloud model.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  the prompt composed of a list of messages.  |  _required_  |  
|  `stop`  |  `Optional[List[str]]`  |  a list of strings on which the model should stop generating. If generation stops due to a stop token, the stop token itself SHOULD BE INCLUDED as part of the output. This is not enforced across models right now, but it's a good practice to follow since it makes it much easier to parse the output of the model downstream and understand why generation stopped.  |  `None`  |  
Yields:  
| Type  | Description  |  
| --- | --- |  
|  `ChatResponseGen`  |  ChatResponseGen with model partial generation  |  
Source code in `llama-index-integrations/llms/llama-index-llms-sambanovasystems/llama_index/llms/sambanovasystems/base.py`  
| 
```
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
@llm_chat_callback()
defstream_chat(
    self,
    messages: Sequence[ChatMessage],
    stop: Optional[List[str]] = None,
    **kwargs: Any,
) -> ChatResponseGen:
"""
    Streams the chat output of the SambaNovaCloud model.

    Args:
        messages: the prompt composed of a list of messages.
        stop: a list of strings on which the model should stop generating.
              If generation stops due to a stop token, the stop token itself
              SHOULD BE INCLUDED as part of the output. This is not enforced
              across models right now, but it's a good practice to follow since
              it makes it much easier to parse the output of the model
              downstream and understand why generation stopped.

    Yields:
        ChatResponseGen with model partial generation

    """
    messages_dicts = _create_message_dicts(messages)

    finish_reason = None
    content = ""
    role = MessageRole.ASSISTANT

    for partial_response in self._handle_streaming_request(messages_dicts, stop):
        if len(partial_response["choices"])  0:
            content_delta = partial_response["choices"][0]["delta"]["content"]
            content += content_delta
            additional_kwargs = {
                "id": partial_response["id"],
                "finish_reason": partial_response["choices"][0].get(
                    "finish_reason"
                ),
            }
        else:
            additional_kwargs = {
                "id": partial_response["id"],
                "finish_reason": finish_reason,
                "usage": partial_response.get("usage"),
                "model_name": partial_response["model"],
                "system_fingerprint": partial_response["system_fingerprint"],
                "created": partial_response["created"],
            }

        # yield chunk
        yield ChatResponse(
            message=ChatMessage(
                role=role, content=content, additional_kwargs=additional_kwargs
            ),
            delta=content_delta,
            raw=partial_response,
        )

```
 |  
| --- | --- |  
###  achat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/sambanovasystems/#llama_index.llms.sambanovasystems.SambaNovaCloud.achat "Permanent link")

```
achat(
    messages: Sequence[],
    stop: Optional[[]] = None,
    **kwargs: 
) -> 

```

Calls the async chat implementation of the SambaNovaCloud model.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  the prompt composed of a list of messages.  |  _required_  |  
|  `stop`  |  `Optional[List[str]]`  |  a list of strings on which the model should stop generating. If generation stops due to a stop token, the stop token itself SHOULD BE INCLUDED as part of the output. This is not enforced across models right now, but it's a good practice to follow since it makes it much easier to parse the output of the model downstream and understand why generation stopped.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  ChatResponse with async model generation  |  
Source code in `llama-index-integrations/llms/llama-index-llms-sambanovasystems/llama_index/llms/sambanovasystems/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
async defachat(
    self,
    messages: Sequence[ChatMessage],
    stop: Optional[List[str]] = None,
    **kwargs: Any,
) -> ChatResponse:
"""
    Calls the async chat implementation of the SambaNovaCloud model.

    Args:
        messages: the prompt composed of a list of messages.
        stop: a list of strings on which the model should stop generating.
              If generation stops due to a stop token, the stop token itself
              SHOULD BE INCLUDED as part of the output. This is not enforced
              across models right now, but it's a good practice to follow since
              it makes it much easier to parse the output of the model
              downstream and understand why generation stopped.

    Returns:
        ChatResponse with async model generation

    """
    messages_dicts = _create_message_dicts(messages)
    response = await self._handle_request_async(messages_dicts, stop)
    message = ChatMessage(
        role=MessageRole.ASSISTANT,
        content=response["choices"][0]["message"]["content"],
        additional_kwargs={
            "id": response["id"],
            "finish_reason": response["choices"][0]["finish_reason"],
            "usage": response.get("usage"),
            "model_name": response["model"],
            "system_fingerprint": response["system_fingerprint"],
            "created": response["created"],
        },
    )
    return ChatResponse(message=message)

```
 |  
| --- | --- |  
##  SambaStudio [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/sambanovasystems/#llama_index.llms.sambanovasystems.SambaStudio "Permanent link")
Bases: 
SambaStudio model.
Setup
To use, you should have the environment variables: `SAMBASTUDIO_URL` set with your SambaStudio deployed endpoint URL. `SAMBASTUDIO_API_KEY` set with your SambaStudio deployed endpoint Key. https://docs.sambanova.ai/sambastudio/latest/index.html Examples: 

```
SambaStudio(
    sambastudio_url = set with your SambaStudio deployed endpoint URL,
    sambastudio_api_key = set with your SambaStudio deployed endpoint Key.
    model = model or expert name (set for CoE endpoints),
    max_tokens = max number of tokens to generate,
    temperature = model temperature,
    context_window = model context window,
    top_p = model top p,
    top_k = model top k,
    do_sample = whether to do sample
    process_prompt = whether to process prompt
        (set for CoE generic v1 and v2 endpoints)
    stream_options = include usage to get generation metrics
    special_tokens = start, start_role, end_role, end special tokens
        (set for CoE generic v1 and v2 endpoints when process prompt
         set to false or for StandAlone v1 and v2 endpoints)
    model_kwargs: Optional = Extra Key word arguments to pass to the model.
)

```

Key init args — completion params: model: str The name of the model to use, e.g., Meta-Llama-3-70B-Instruct-4096 (set for CoE endpoints). streaming: bool Whether to use streaming max_tokens: inthandler when using non streaming methods max tokens to generate context_window: int model context window temperature: float model temperature top_p: float model top p top_k: int model top k do_sample: bool whether to do sample process_prompt: whether to process prompt (set for CoE generic v1 and v2 endpoints) stream_options: dict stream options, include usage to get generation metrics special_tokens: dict start, start_role, end_role and end special tokens (set for CoE generic v1 and v2 endpoints when process prompt set to false or for StandAlone v1 and v2 endpoints) default to llama3 special tokens model_kwargs: dict Extra Key word arguments to pass to the model. Key init args — client params: sambastudio_url: str SambaStudio endpoint URL sambastudio_api_key: str SambaStudio endpoint api key Instantiate: 

```
fromllama_index.llms.sambanovaimport SambaStudio
llm = SambaStudio=(
    sambastudio_url = set with your SambaStudio deployed endpoint URL,
    sambastudio_api_key = set with your SambaStudio deployed endpoint Key.
    model = model or expert name (set for CoE endpoints),
    max_tokens = max number of tokens to generate,
    temperature = model temperature,
    context_window = model context window,
    top_p = model top p,
    top_k = model top k,
    do_sample = whether to do sample
    process_prompt = whether to process prompt
        (set for CoE generic v1 and v2 endpoints)
    stream_options = include usage to get generation metrics
    special_tokens = start, start_role, end_role, and special tokens
        (set for CoE generic v1 and v2 endpoints when process prompt
         set to false or for StandAlone v1 and v2 endpoints)
    model_kwargs: Optional = Extra Key word arguments to pass to the model.
)

```

Complete: 

```
prompt = "Tell me about Naruto Uzumaki in one sentence"
response = llm.complete(prompt)

```

Chat: 

```
messages = [
    ChatMessage(role=MessageRole.SYSTEM, content=("You're a helpful assistant")),
    ChatMessage(role=MessageRole.USER, content="Tell me about Naruto Uzumaki in one sentence")
]
response = llm.chat(messages)

```

Stream: 

```
prompt = "Tell me about Naruto Uzumaki in one sentence"
messages = [
    ChatMessage(role=MessageRole.SYSTEM, content=("You're a helpful assistant")),
    ChatMessage(role=MessageRole.USER, content="Tell me about Naruto Uzumaki in one sentence")
]
for chunk in llm.stream_complete(prompt):
    print(chunk.text)
for chunk in llm.stream_chat(messages):
    print(chunk.message.content)

```

Async: 

```
prompt = "Tell me about Naruto Uzumaki in one sentence"
asyncio.run(llm.acomplete(prompt))
messages = [
    ChatMessage(role=MessageRole.SYSTEM, content=("You're a helpful assistant")),
    ChatMessage(role=MessageRole.USER, content="Tell me about Naruto Uzumaki in one sentence")
]
asyncio.run(llm.achat(chat_text_msgs))

```

Response metadata and usage 

```
messages = [
    ChatMessage(role=MessageRole.SYSTEM, content=("You're a helpful assistant")),
    ChatMessage(role=MessageRole.USER, content="Tell me about Naruto Uzumaki in one sentence")
]
metadata_and_usage = llm.chat(messages).message.additional_kwargs
print(metadata_and_usage)

```

Source code in `llama-index-integrations/llms/llama-index-llms-sambanovasystems/llama_index/llms/sambanovasystems/base.py`  
| 
```
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
 676
 677
 678
 679
 680
 681
 682
 683
 684
 685
 686
 687
 688
 689
 690
 691
 692
 693
 694
 695
 696
 697
 698
 699
 700
 701
 702
 703
 704
 705
 706
 707
 708
 709
 710
 711
 712
 713
 714
 715
 716
 717
 718
 719
 720
 721
 722
 723
 724
 725
 726
 727
 728
 729
 730
 731
 732
 733
 734
 735
 736
 737
 738
 739
 740
 741
 742
 743
 744
 745
 746
 747
 748
 749
 750
 751
 752
 753
 754
 755
 756
 757
 758
 759
 760
 761
 762
 763
 764
 765
 766
 767
 768
 769
 770
 771
 772
 773
 774
 775
 776
 777
 778
 779
 780
 781
 782
 783
 784
 785
 786
 787
 788
 789
 790
 791
 792
 793
 794
 795
 796
 797
 798
 799
 800
 801
 802
 803
 804
 805
 806
 807
 808
 809
 810
 811
 812
 813
 814
 815
 816
 817
 818
 819
 820
 821
 822
 823
 824
 825
 826
 827
 828
 829
 830
 831
 832
 833
 834
 835
 836
 837
 838
 839
 840
 841
 842
 843
 844
 845
 846
 847
 848
 849
 850
 851
 852
 853
 854
 855
 856
 857
 858
 859
 860
 861
 862
 863
 864
 865
 866
 867
 868
 869
 870
 871
 872
 873
 874
 875
 876
 877
 878
 879
 880
 881
 882
 883
 884
 885
 886
 887
 888
 889
 890
 891
 892
 893
 894
 895
 896
 897
 898
 899
 900
 901
 902
 903
 904
 905
 906
 907
 908
 909
 910
 911
 912
 913
 914
 915
 916
 917
 918
 919
 920
 921
 922
 923
 924
 925
 926
 927
 928
 929
 930
 931
 932
 933
 934
 935
 936
 937
 938
 939
 940
 941
 942
 943
 944
 945
 946
 947
 948
 949
 950
 951
 952
 953
 954
 955
 956
 957
 958
 959
 960
 961
 962
 963
 964
 965
 966
 967
 968
 969
 970
 971
 972
 973
 974
 975
 976
 977
 978
 979
 980
 981
 982
 983
 984
 985
 986
 987
 988
 989
 990
 991
 992
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
1003
1004
1005
1006
1007
1008
1009
1010
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
1023
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
1039
1040
1041
1042
1043
1044
1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
1056
1057
1058
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
1071
1072
1073
1074
1075
1076
1077
1078
1079
1080
1081
1082
1083
1084
1085
1086
1087
1088
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
1113
1114
1115
1116
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
1136
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
1153
1154
1155
1156
1157
1158
1159
1160
1161
1162
1163
1164
1165
1166
1167
1168
1169
1170
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
1188
1189
1190
1191
1192
1193
1194
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
1206
1207
1208
1209
1210
1211
1212
1213
1214
1215
1216
1217
1218
1219
1220
1221
1222
1223
1224
1225
1226
1227
1228
1229
1230
1231
1232
1233
1234
1235
1236
1237
1238
1239
1240
1241
1242
1243
1244
1245
1246
1247
1248
1249
1250
1251
1252
1253
1254
1255
1256
1257
1258
1259
1260
1261
1262
1263
1264
1265
1266
1267
1268
1269
1270
1271
1272
1273
1274
1275
1276
1277
1278
1279
1280
1281
1282
1283
1284
1285
1286
1287
1288
1289
1290
1291
1292
1293
1294
1295
1296
1297
1298
1299
1300
1301
1302
1303
1304
1305
1306
1307
1308
1309
1310
1311
1312
1313
1314
1315
1316
1317
1318
1319
1320
1321
1322
1323
1324
1325
1326
1327
1328
1329
1330
1331
1332
1333
1334
1335
1336
1337
1338
1339
1340
1341
1342
1343
1344
1345
1346
1347
1348
1349
1350
1351
1352
1353
1354
1355
1356
1357
1358
1359
1360
1361
1362
1363
1364
1365
1366
1367
1368
1369
1370
1371
1372
1373
1374
1375
1376
1377
1378
1379
1380
1381
1382
1383
1384
1385
1386
1387
1388
1389
1390
1391
1392
1393
1394
1395
1396
1397
1398
1399
1400
1401
1402
1403
1404
1405
1406
1407
1408
1409
1410
1411
1412
1413
1414
1415
1416
1417
1418
1419
1420
1421
1422
1423
1424
1425
1426
1427
1428
1429
1430
1431
1432
1433
1434
1435
1436
1437
1438
1439
1440
1441
1442
1443
1444
1445
1446
1447
1448
1449
1450
1451
1452
1453
1454
1455
1456
1457
1458
1459
1460
1461
1462
1463
1464
1465
1466
1467
1468
1469
1470
1471
1472
1473
1474
1475
1476
1477
1478
1479
1480
1481
1482
1483
1484
1485
1486
1487
1488
1489
1490
1491
1492
1493
1494
1495
1496
1497
1498
1499
1500
1501
1502
1503
1504
1505
1506
1507
1508
1509
1510
1511
1512
1513
1514
1515
1516
1517
1518
1519
1520
1521
1522
1523
1524
1525
1526
1527
1528
1529
1530
1531
1532
1533
1534
1535
1536
1537
1538
1539
1540
1541
1542
1543
1544
1545
1546
1547
1548
1549
1550
1551
1552
1553
1554
1555
1556
1557
1558
1559
1560
1561
1562
1563
1564
1565
1566
1567
1568
1569
1570
1571
1572
1573
1574
1575
1576
1577
1578
1579
1580
1581
1582
1583
1584
1585
1586
1587
1588
1589
1590
1591
1592
1593
1594
1595
1596
1597
```
 | 
```
classSambaStudio(LLM):
"""
    SambaStudio model.

    Setup:
        To use, you should have the environment variables:
        ``SAMBASTUDIO_URL`` set with your SambaStudio deployed endpoint URL.
        ``SAMBASTUDIO_API_KEY`` set with your SambaStudio deployed endpoint Key.
        https://docs.sambanova.ai/sambastudio/latest/index.html
        Examples:
            ```python
            SambaStudio(
                sambastudio_url = set with your SambaStudio deployed endpoint URL,
                sambastudio_api_key = set with your SambaStudio deployed endpoint Key.
                model = model or expert name (set for CoE endpoints),
                max_tokens = max number of tokens to generate,
                temperature = model temperature,
                context_window = model context window,
                top_p = model top p,
                top_k = model top k,
                do_sample = whether to do sample
                process_prompt = whether to process prompt
                    (set for CoE generic v1 and v2 endpoints)
                stream_options = include usage to get generation metrics
                special_tokens = start, start_role, end_role, end special tokens
                    (set for CoE generic v1 and v2 endpoints when process prompt
                     set to false or for StandAlone v1 and v2 endpoints)
                model_kwargs: Optional = Extra Key word arguments to pass to the model.


    Key init args — completion params:
        model: str
            The name of the model to use, e.g., Meta-Llama-3-70B-Instruct-4096
            (set for CoE endpoints).
        streaming: bool
            Whether to use streaming
        max_tokens: inthandler when using non streaming methods
            max tokens to generate
        context_window: int
            model context window
        temperature: float
            model temperature
        top_p: float
            model top p
        top_k: int
            model top k
        do_sample: bool
            whether to do sample
        process_prompt:
            whether to process prompt (set for CoE generic v1 and v2 endpoints)
        stream_options: dict
            stream options, include usage to get generation metrics
        special_tokens: dict
            start, start_role, end_role and end special tokens
            (set for CoE generic v1 and v2 endpoints when process prompt set to false
             or for StandAlone v1 and v2 endpoints) default to llama3 special tokens
        model_kwargs: dict
            Extra Key word arguments to pass to the model.
    Key init args — client params:
        sambastudio_url: str
            SambaStudio endpoint URL
        sambastudio_api_key: str
            SambaStudio endpoint api key
    Instantiate:
        ```python
        from llama_index.llms.sambanova import SambaStudio
        llm = SambaStudio=(
            sambastudio_url = set with your SambaStudio deployed endpoint URL,
            sambastudio_api_key = set with your SambaStudio deployed endpoint Key.
            model = model or expert name (set for CoE endpoints),
            max_tokens = max number of tokens to generate,
            temperature = model temperature,
            context_window = model context window,
            top_p = model top p,
            top_k = model top k,
            do_sample = whether to do sample
            process_prompt = whether to process prompt
                (set for CoE generic v1 and v2 endpoints)
            stream_options = include usage to get generation metrics
            special_tokens = start, start_role, end_role, and special tokens
                (set for CoE generic v1 and v2 endpoints when process prompt
                 set to false or for StandAlone v1 and v2 endpoints)
            model_kwargs: Optional = Extra Key word arguments to pass to the model.

        ```
    Complete:
        ```python
        prompt = "Tell me about Naruto Uzumaki in one sentence"
        response = llm.complete(prompt)
        ```
    Chat:
        ```python
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=("You're a helpful assistant")),
            ChatMessage(role=MessageRole.USER, content="Tell me about Naruto Uzumaki in one sentence")

        response = llm.chat(messages)
        ```
    Stream:
        ```python
        prompt = "Tell me about Naruto Uzumaki in one sentence"
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=("You're a helpful assistant")),
            ChatMessage(role=MessageRole.USER, content="Tell me about Naruto Uzumaki in one sentence")

        for chunk in llm.stream_complete(prompt):
            print(chunk.text)
        for chunk in llm.stream_chat(messages):
            print(chunk.message.content)
        ```
    Async:
        ```python
        prompt = "Tell me about Naruto Uzumaki in one sentence"
        asyncio.run(llm.acomplete(prompt))
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=("You're a helpful assistant")),
            ChatMessage(role=MessageRole.USER, content="Tell me about Naruto Uzumaki in one sentence")

        asyncio.run(llm.achat(chat_text_msgs))
        ```
    Response metadata and usage
        ```python
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=("You're a helpful assistant")),
            ChatMessage(role=MessageRole.USER, content="Tell me about Naruto Uzumaki in one sentence")

        metadata_and_usage = llm.chat(messages).message.additional_kwargs
        print(metadata_and_usage)
        ```
    """

    model_config = ConfigDict(
        protected_namespaces=("pydantic_model_",), arbitrary_types_allowed=True
    )

    sambastudio_url: str = Field(description="SambaStudio Url")

    sambastudio_api_key: SecretStr = Field(description="SambaStudio api key")

    base_url: str = Field(
        default="", exclude=True, description="SambaStudio non streaming Url"
    )

    streaming_url: str = Field(
        default="", exclude=True, description="SambaStudio streaming Url"
    )

    model: Optional[str] = Field(
        default=None,
        description="The name of the model or expert to use (for CoE endpoints)",
    )

    streaming: bool = Field(
        default=False,
        description="Whether to use streaming handler when using non streaming methods",
    )

    context_window: int = Field(default=4096, description="context window")

    max_tokens: int = Field(default=1024, description="max tokens to generate")

    temperature: Optional[float] = Field(default=0.7, description="model temperature")

    top_p: Optional[float] = Field(default=None, description="model top p")

    top_k: Optional[int] = Field(default=None, description="model top k")

    do_sample: Optional[bool] = Field(
        default=None, description="whether to do sampling"
    )

    process_prompt: Optional[bool] = Field(
        default=True,
        description="whether process prompt (for CoE generic v1 and v2 endpoints)",
    )

    stream_options: dict = Field(
        default_factory=lambda: {"include_usage": True},
        description="stream options, include usage to get generation metrics",
    )

    special_tokens: dict = Field(
        default={
            "start": "<|begin_of_text|>",
            "start_role": "<|begin_of_text|><|start_header_id|>{role}<|end_header_id|>",
            "end_role": "<|eot_id|>",
            "end": "<|start_header_id|>assistant<|end_header_id|>\n",
        },
        description="start, start_role, end_role and end special tokens (set for CoE generic v1 and v2 endpoints when process prompt set to false or for StandAlone v1 and v2 endpoints) default to llama3 special tokens",
    )

    model_kwargs: Optional[Dict[str, Any]] = Field(
        default=None, description="Key word arguments to pass to the model."
    )

    @classmethod
    defclass_name(cls) -> str:
        return "SambaStudio"

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.max_tokens,
            is_chat_model=True,
            model_name=self.model,
        )

    def__init__(self, **kwargs: Any) -> None:
"""Init and validate environment variables."""
        kwargs["sambastudio_url"] = get_from_param_or_env(
            "sambastudio_url", kwargs.get("sambastudio_url"), "SAMBASTUDIO_URL"
        )
        kwargs["sambastudio_api_key"] = get_from_param_or_env(
            "sambastudio_api_key",
            kwargs.get("sambastudio_api_key"),
            "SAMBASTUDIO_API_KEY",
        )
        kwargs["sambastudio_url"], kwargs["streaming_url"] = self._get_sambastudio_urls(
            kwargs["sambastudio_url"]
        )
        super().__init__(**kwargs)

    def_messages_to_string(self, messages: Sequence[ChatMessage]) -> str:
"""
        Convert a sequence of ChatMessages to:
        - dumped json string with Role / content dict structure when process_prompt is true,
        - string with special tokens if process_prompt is false for generic V1 and V2 endpoints.

        Args:
            messages: sequence of ChatMessages
        Returns:
            str: string to send as model input depending on process_prompt param

        """
        if self.process_prompt:
            messages_dict: Dict[str, Any] = {
                "conversation_id": "sambaverse-conversation-id",
                "messages": [],
            }
            for message in messages:
                messages_dict["messages"].append(
                    {
                        "role": message.role,
                        "content": message.content,
                    }
                )
            messages_string = json.dumps(messages_dict)
        else:
            messages_string = self.special_tokens["start"]
            for message in messages:
                messages_string += self.special_tokens["start_role"].format(
                    role=self._get_role(message)
                )
                messages_string += f" {message.content} "
                messages_string += self.special_tokens["end_role"]
            messages_string += self.special_tokens["end"]

        return messages_string

    def_get_sambastudio_urls(self, url: str) -> Tuple[str, str]:
"""
        Get streaming and non streaming URLs from the given URL.

        Args:
            url: string with sambastudio base or streaming endpoint url
        Returns:
            base_url: string with url to do non streaming calls
            streaming_url: string with url to do streaming calls

        """
        if "chat/completions" in url:
            base_url = url
            stream_url = url
        else:
            if "stream" in url:
                base_url = url.replace("stream/", "")
                stream_url = url
            else:
                base_url = url
                if "generic" in url:
                    stream_url = "generic/stream".join(url.split("generic"))
                else:
                    raise ValueError("Unsupported URL")
        return base_url, stream_url

    def_handle_request(
        self,
        messages: Sequence[ChatMessage],
        stop: Optional[List[str]] = None,
        streaming: Optional[bool] = False,
    ) -> Response:
"""
        Performs a post request to the LLM API.

        Args:
        messages_dicts: List of role / content dicts to use as input.
        stop: list of stop tokens
        streaming: whether to do a streaming call
        Returns:
            A request Response object

        """
        # create request payload for openai compatible API
        if "chat/completions" in self.sambastudio_url:
            messages_dicts = _create_message_dicts(messages)
            data = {
                "messages": messages_dicts,
                "max_tokens": self.max_tokens,
                "stop": stop,
                "model": self.model,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "top_k": self.top_k,
                "stream": streaming,
                "stream_options": self.stream_options,
            }
            data = {key: value for key, value in data.items() if value is not None}
            headers = {
                "Authorization": f"Bearer "
                f"{self.sambastudio_api_key.get_secret_value()}",
                "Content-Type": "application/json",
            }

        # create request payload for generic v1 API
        elif "api/v2/predict/generic" in self.sambastudio_url:
            items = [{"id": "item0", "value": self._messages_to_string(messages)}]
            params: Dict[str, Any] = {
                "select_expert": self.model,
                "process_prompt": self.process_prompt,
                "max_tokens_to_generate": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "top_k": self.top_k,
                "do_sample": self.do_sample,
            }
            if self.model_kwargs is not None:
                params = {**params, **self.model_kwargs}
            params = {key: value for key, value in params.items() if value is not None}
            data = {"items": items, "params": params}
            headers = {"key": self.sambastudio_api_key.get_secret_value()}

        # create request payload for generic v1 API
        elif "api/predict/generic" in self.sambastudio_url:
            params = {
                "select_expert": self.model,
                "process_prompt": self.process_prompt,
                "max_tokens_to_generate": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "top_k": self.top_k,
                "do_sample": self.do_sample,
            }
            if self.model_kwargs is not None:
                params = {**params, **self.model_kwargs}
            params = {
                key: {"type": type(value).__name__, "value": str(value)}
                for key, value in params.items()
                if value is not None
            }
            if streaming:
                data = {
                    "instance": self._messages_to_string(messages),
                    "params": params,
                }
            else:
                data = {
                    "instances": [self._messages_to_string(messages)],
                    "params": params,
                }
            headers = {"key": self.sambastudio_api_key.get_secret_value()}

        else:
            raise ValueError(
                f"Unsupported URL{self.sambastudio_url}"
                "only openai, generic v1 and generic v2 APIs are supported"
            )

        http_session = requests.Session()
        if streaming:
            response = http_session.post(
                self.streaming_url, headers=headers, json=data, stream=True
            )
        else:
            response = http_session.post(
                self.base_url, headers=headers, json=data, stream=False
            )
        if response.status_code != 200:
            raise RuntimeError(
                f"Sambanova /complete call failed with status code "
                f"{response.status_code}."
                f"{response.text}."
            )
        return response

    async def_handle_request_async(
        self,
        messages: Sequence[ChatMessage],
        stop: Optional[List[str]] = None,
        streaming: Optional[bool] = False,
    ) -> Response:
"""
        Performs an async post request to the LLM API.

        Args:
        messages_dicts: List of role / content dicts to use as input.
        stop: list of stop tokens
        streaming: whether to do a streaming call
        Returns:
            A request Response object

        """
        # create request payload for openai compatible API
        if "chat/completions" in self.sambastudio_url:
            messages_dicts = _create_message_dicts(messages)
            data = {
                "messages": messages_dicts,
                "max_tokens": self.max_tokens,
                "stop": stop,
                "model": self.model,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "top_k": self.top_k,
                "stream": streaming,
                "stream_options": self.stream_options,
            }
            data = {key: value for key, value in data.items() if value is not None}
            headers = {
                "Authorization": f"Bearer "
                f"{self.sambastudio_api_key.get_secret_value()}",
                "Content-Type": "application/json",
            }

        # create request payload for generic v1 API
        elif "api/v2/predict/generic" in self.sambastudio_url:
            items = [{"id": "item0", "value": self._messages_to_string(messages)}]
            params: Dict[str, Any] = {
                "select_expert": self.model,
                "process_prompt": self.process_prompt,
                "max_tokens_to_generate": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "top_k": self.top_k,
                "do_sample": self.do_sample,
            }
            if self.model_kwargs is not None:
                params = {**params, **self.model_kwargs}
            params = {key: value for key, value in params.items() if value is not None}
            data = {"items": items, "params": params}
            headers = {"key": self.sambastudio_api_key.get_secret_value()}

        # create request payload for generic v1 API
        elif "api/predict/generic" in self.sambastudio_url:
            params = {
                "select_expert": self.model,
                "process_prompt": self.process_prompt,
                "max_tokens_to_generate": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "top_k": self.top_k,
                "do_sample": self.do_sample,
            }
            if self.model_kwargs is not None:
                params = {**params, **self.model_kwargs}
            params = {
                key: {"type": type(value).__name__, "value": str(value)}
                for key, value in params.items()
                if value is not None
            }
            if streaming:
                data = {
                    "instance": self._messages_to_string(messages),
                    "params": params,
                }
            else:
                data = {
                    "instances": [self._messages_to_string(messages)],
                    "params": params,
                }
            headers = {"key": self.sambastudio_api_key.get_secret_value()}

        else:
            raise ValueError(
                f"Unsupported URL{self.sambastudio_url}"
                "only openai, generic v1 and generic v2 APIs are supported"
            )

        async with aiohttp.ClientSession() as session:
            if streaming:
                url = self.streaming_url
            else:
                url = self.base_url

            async with session.post(
                url,
                headers=headers,
                json=data,
            ) as response:
                if response.status != 200:
                    raise RuntimeError(
                        f"Sambanova /complete call failed with status code "
                        f"{response.status}."
                        f"{response.text}."
                    )
                response_dict = await response.json()
                if response_dict.get("error"):
                    raise RuntimeError(
                        f"Sambanova /complete call failed with status code {response.status}.",
                        f"{response_dict}.",
                    )
                return response_dict

    def_process_response(self, response: Response) -> ChatMessage:
"""
        Process a non streaming response from the api.

        Args:
            response: A request Response object
        Returns:
            generation: a ChatMessage with model generation

        """
        # Extract json payload form response
        try:
            response_dict = response.json()
        except Exception as e:
            raise RuntimeError(
                f"Sambanova /complete call failed couldn't get JSON response {e}"
                f"response: {response.text}"
            )

        # process response payload for openai compatible API
        if "chat/completions" in self.sambastudio_url:
            content = response_dict["choices"][0]["message"]["content"]
            response_metadata = {
                "finish_reason": response_dict["choices"][0]["finish_reason"],
                "usage": response_dict.get("usage"),
                "model_name": response_dict["model"],
                "system_fingerprint": response_dict["system_fingerprint"],
                "created": response_dict["created"],
            }

        # process response payload for generic v2 API
        elif "api/v2/predict/generic" in self.sambastudio_url:
            content = response_dict["items"][0]["value"]["completion"]
            response_metadata = response_dict["items"][0]

        # process response payload for generic v1 API
        elif "api/predict/generic" in self.sambastudio_url:
            content = response_dict["predictions"][0]["completion"]
            response_metadata = response_dict

        else:
            raise ValueError(
                f"Unsupported URL{self.sambastudio_url}"
                "only openai, generic v1 and generic v2 APIs are supported"
            )

        return ChatMessage(
            content=content,
            additional_kwargs=response_metadata,
            role=MessageRole.ASSISTANT,
        )

    def_process_stream_response(self, response: Response) -> Iterator[ChatMessage]:
"""
        Process a streaming response from the api.

        Args:
            response: An iterable request Response object
        Yields:
            generation: an Iterator[ChatMessage] with model partial generation

        """
        try:
            importsseclient
        except ImportError:
            raise ImportError(
                "could not import sseclient library"
                "Please install it with `pip install sseclient-py`."
            )

        # process response payload for openai compatible API
        if "chat/completions" in self.sambastudio_url:
            finish_reason = ""
            content = ""
            client = sseclient.SSEClient(response)
            for event in client.events():
                if event.event == "error_event":
                    raise RuntimeError(
                        f"Sambanova /complete call failed with status code "
                        f"{response.status_code}."
                        f"{event.data}."
                    )
                try:
                    # check if the response is not a final event ("[DONE]")
                    if event.data != "[DONE]":
                        if isinstance(event.data, str):
                            data = json.loads(event.data)
                        else:
                            raise RuntimeError(
                                f"Sambanova /complete call failed with status code "
                                f"{response.status_code}."
                                f"{event.data}."
                            )
                        if data.get("error"):
                            raise RuntimeError(
                                f"Sambanova /complete call failed with status code "
                                f"{response.status_code}."
                                f"{event.data}."
                            )
                        if len(data["choices"])  0:
                            finish_reason = data["choices"][0].get("finish_reason")
                            content += data["choices"][0]["delta"]["content"]
                            id = data["id"]
                            metadata = {}
                        else:
                            content += ""
                            id = data["id"]
                            metadata = {
                                "finish_reason": finish_reason,
                                "usage": data.get("usage"),
                                "model_name": data["model"],
                                "system_fingerprint": data["system_fingerprint"],
                                "created": data["created"],
                            }
                        if data.get("usage") is not None:
                            content += ""
                            id = data["id"]
                            metadata = {
                                "finish_reason": finish_reason,
                                "usage": data.get("usage"),
                                "model_name": data["model"],
                                "system_fingerprint": data["system_fingerprint"],
                                "created": data["created"],
                            }
                        yield ChatMessage(
                            role=MessageRole.ASSISTANT,
                            content=content,
                            additional_kwargs=metadata,
                        )

                except Exception as e:
                    raise RuntimeError(
                        f"Error getting content chunk raw streamed response: {e}"
                        f"data: {event.data}"
                    )

        # process response payload for generic v2 API
        elif "api/v2/predict/generic" in self.sambastudio_url:
            content = ""
            for line in response.iter_lines():
                try:
                    data = json.loads(line)
                    content += data["result"]["items"][0]["value"]["stream_token"]
                    id = data["result"]["items"][0]["id"]
                    if data["result"]["items"][0]["value"]["is_last_response"]:
                        metadata = {
                            "finish_reason": data["result"]["items"][0]["value"].get(
                                "stop_reason"
                            ),
                            "prompt": data["result"]["items"][0]["value"].get("prompt"),
                            "usage": {
                                "prompt_tokens_count": data["result"]["items"][0][
                                    "value"
                                ].get("prompt_tokens_count"),
                                "completion_tokens_count": data["result"]["items"][0][
                                    "value"
                                ].get("completion_tokens_count"),
                                "total_tokens_count": data["result"]["items"][0][
                                    "value"
                                ].get("total_tokens_count"),
                                "start_time": data["result"]["items"][0]["value"].get(
                                    "start_time"
                                ),
                                "end_time": data["result"]["items"][0]["value"].get(
                                    "end_time"
                                ),
                                "model_execution_time": data["result"]["items"][0][
                                    "value"
                                ].get("model_execution_time"),
                                "time_to_first_token": data["result"]["items"][0][
                                    "value"
                                ].get("time_to_first_token"),
                                "throughput_after_first_token": data["result"]["items"][
                                    0
                                ]["value"].get("throughput_after_first_token"),
                                "batch_size_used": data["result"]["items"][0][
                                    "value"
                                ].get("batch_size_used"),
                            },
                        }
                    else:
                        metadata = {}
                    yield ChatMessage(
                        role=MessageRole.ASSISTANT,
                        content=content,
                        additional_kwargs=metadata,
                    )

                except Exception as e:
                    raise RuntimeError(
                        f"Error getting content chunk raw streamed response: {e}"
                        f"line: {line}"
                    )

        # process response payload for generic v1 API
        elif "api/predict/generic" in self.sambastudio_url:
            content = ""
            for line in response.iter_lines():
                try:
                    data = json.loads(line)
                    content += data["result"]["responses"][0]["stream_token"]
                    id = None
                    if data["result"]["responses"][0]["is_last_response"]:
                        metadata = {
                            "finish_reason": data["result"]["responses"][0].get(
                                "stop_reason"
                            ),
                            "prompt": data["result"]["responses"][0].get("prompt"),
                            "usage": {
                                "prompt_tokens_count": data["result"]["responses"][
                                    0
                                ].get("prompt_tokens_count"),
                                "completion_tokens_count": data["result"]["responses"][
                                    0
                                ].get("completion_tokens_count"),
                                "total_tokens_count": data["result"]["responses"][
                                    0
                                ].get("total_tokens_count"),
                                "start_time": data["result"]["responses"][0].get(
                                    "start_time"
                                ),
                                "end_time": data["result"]["responses"][0].get(
                                    "end_time"
                                ),
                                "model_execution_time": data["result"]["responses"][
                                    0
                                ].get("model_execution_time"),
                                "time_to_first_token": data["result"]["responses"][
                                    0
                                ].get("time_to_first_token"),
                                "throughput_after_first_token": data["result"][
                                    "responses"
                                ][0].get("throughput_after_first_token"),
                                "batch_size_used": data["result"]["responses"][0].get(
                                    "batch_size_used"
                                ),
                            },
                        }
                    else:
                        metadata = {}
                    yield ChatMessage(
                        role=MessageRole.ASSISTANT,
                        content=content,
                        additional_kwargs=metadata,
                    )

                except Exception as e:
                    raise RuntimeError(
                        f"Error getting content chunk raw streamed response: {e}"
                        f"line: {line}"
                    )

        else:
            raise ValueError(
                f"Unsupported URL{self.sambastudio_url}"
                "only openai, generic v1 and generic v2 APIs are supported"
            )

    async def_process_response_async(
        self, response_dict: Dict[str, Any]
    ) -> ChatMessage:
"""
        Process a non streaming response from the api.

        Args:
            response: A request Response object
        Returns:
            generation: a ChatMessage with model generation

        """
        # process response payload for openai compatible API
        if "chat/completions" in self.sambastudio_url:
            content = response_dict["choices"][0]["message"]["content"]
            response_metadata = {
                "finish_reason": response_dict["choices"][0]["finish_reason"],
                "usage": response_dict.get("usage"),
                "model_name": response_dict["model"],
                "system_fingerprint": response_dict["system_fingerprint"],
                "created": response_dict["created"],
            }

        # process response payload for generic v2 API
        elif "api/v2/predict/generic" in self.sambastudio_url:
            content = response_dict["items"][0]["value"]["completion"]
            response_metadata = response_dict["items"][0]

        # process response payload for generic v1 API
        elif "api/predict/generic" in self.sambastudio_url:
            content = response_dict["predictions"][0]["completion"]
            response_metadata = response_dict

        else:
            raise ValueError(
                f"Unsupported URL{self.sambastudio_url}"
                "only openai, generic v1 and generic v2 APIs are supported"
            )

        return ChatMessage(
            content=content,
            additional_kwargs=response_metadata,
            role=MessageRole.ASSISTANT,
        )

    @llm_chat_callback()
    defchat(
        self,
        messages: Sequence[ChatMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ChatResponse:
"""
        Calls the chat implementation of the SambaStudio model.

        Args:
            messages: the prompt composed of a list of messages.
            stop: a list of strings on which the model should stop generating.
                  If generation stops due to a stop token, the stop token itself
                  SHOULD BE INCLUDED as part of the output. This is not enforced
                  across models right now, but it's a good practice to follow since
                  it makes it much easier to parse the output of the model
                  downstream and understand why generation stopped.

        Returns:
            ChatResponse with model generation

        """
        # if self.streaming:
        #     stream_iter = self._stream(
        #         messages, stop=stop, **kwargs
        #     )
        #     if stream_iter:
        #         return generate_from_stream(stream_iter)
        response = self._handle_request(messages, stop, streaming=False)
        message = self._process_response(response)

        return ChatResponse(message=message)

    @llm_chat_callback()
    defstream_chat(
        self,
        messages: Sequence[ChatMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ChatResponseGen:
"""
        Stream the output of the SambaStudio model.

        Args:
            messages: the prompt composed of a list of messages.
            stop: a list of strings on which the model should stop generating.
                  If generation stops due to a stop token, the stop token itself
                  SHOULD BE INCLUDED as part of the output. This is not enforced
                  across models right now, but it's a good practice to follow since
                  it makes it much easier to parse the output of the model
                  downstream and understand why generation stopped.

        Yields:
            chunk: ChatResponseGen with model partial generation

        """
        response = self._handle_request(messages, stop, streaming=True)
        for ai_message_chunk in self._process_stream_response(response):
            chunk = ChatResponse(message=ai_message_chunk)
            yield chunk

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        complete_fn = chat_to_completion_decorator(self.chat)
        return complete_fn(prompt, **kwargs)

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        stream_complete_fn = stream_chat_to_completion_decorator(self.stream_chat)
        return stream_complete_fn(prompt, **kwargs)

    @llm_chat_callback()
    async defachat(
        self,
        messages: Sequence[ChatMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ChatResponse:
"""
        Calls the chat implementation of the SambaStudio model.

        Args:
            messages: the prompt composed of a list of messages.
            stop: a list of strings on which the model should stop generating.
                  If generation stops due to a stop token, the stop token itself
                  SHOULD BE INCLUDED as part of the output. This is not enforced
                  across models right now, but it's a good practice to follow since
                  it makes it much easier to parse the output of the model
                  downstream and understand why generation stopped.

        Returns:
            ChatResponse with model generation

        """
        response_dict = await self._handle_request_async(
            messages, stop, streaming=False
        )
        message = await self._process_response_async(response_dict)
        return ChatResponse(message=message)

    @llm_chat_callback()
    async defastream_chat(
        self,
        messages: Sequence[ChatMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ChatResponseAsyncGen:
        raise NotImplementedError(
            "SambaStudio does not currently support async streaming."
        )

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        acomplete_fn = achat_to_completion_decorator(self.achat)
        return await acomplete_fn(prompt, **kwargs)

    @llm_completion_callback()
    defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        raise NotImplementedError(
            "SambaStudio does not currently support async streaming."
        )

```
 |  
| --- | --- |  
###  chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/sambanovasystems/#llama_index.llms.sambanovasystems.SambaStudio.chat "Permanent link")

```
chat(
    messages: Sequence[],
    stop: Optional[[]] = None,
    **kwargs: 
) -> 

```

Calls the chat implementation of the SambaStudio model.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  the prompt composed of a list of messages.  |  _required_  |  
|  `stop`  |  `Optional[List[str]]`  |  a list of strings on which the model should stop generating. If generation stops due to a stop token, the stop token itself SHOULD BE INCLUDED as part of the output. This is not enforced across models right now, but it's a good practice to follow since it makes it much easier to parse the output of the model downstream and understand why generation stopped.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  ChatResponse with model generation  |  
Source code in `llama-index-integrations/llms/llama-index-llms-sambanovasystems/llama_index/llms/sambanovasystems/base.py`  
| 
```
1468
1469
1470
1471
1472
1473
1474
1475
1476
1477
1478
1479
1480
1481
1482
1483
1484
1485
1486
1487
1488
1489
1490
1491
1492
1493
1494
1495
1496
1497
1498
1499
1500
```
 | 
```
@llm_chat_callback()
defchat(
    self,
    messages: Sequence[ChatMessage],
    stop: Optional[List[str]] = None,
    **kwargs: Any,
) -> ChatResponse:
"""
    Calls the chat implementation of the SambaStudio model.

    Args:
        messages: the prompt composed of a list of messages.
        stop: a list of strings on which the model should stop generating.
              If generation stops due to a stop token, the stop token itself
              SHOULD BE INCLUDED as part of the output. This is not enforced
              across models right now, but it's a good practice to follow since
              it makes it much easier to parse the output of the model
              downstream and understand why generation stopped.

    Returns:
        ChatResponse with model generation

    """
    # if self.streaming:
    #     stream_iter = self._stream(
    #         messages, stop=stop, **kwargs
    #     )
    #     if stream_iter:
    #         return generate_from_stream(stream_iter)
    response = self._handle_request(messages, stop, streaming=False)
    message = self._process_response(response)

    return ChatResponse(message=message)

```
 |  
| --- | --- |  
###  stream_chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/sambanovasystems/#llama_index.llms.sambanovasystems.SambaStudio.stream_chat "Permanent link")

```
stream_chat(
    messages: Sequence[],
    stop: Optional[[]] = None,
    **kwargs: 
) -> ChatResponseGen

```

Stream the output of the SambaStudio model.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  the prompt composed of a list of messages.  |  _required_  |  
|  `stop`  |  `Optional[List[str]]`  |  a list of strings on which the model should stop generating. If generation stops due to a stop token, the stop token itself SHOULD BE INCLUDED as part of the output. This is not enforced across models right now, but it's a good practice to follow since it makes it much easier to parse the output of the model downstream and understand why generation stopped.  |  `None`  |  
Yields:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `chunk`  |  `ChatResponseGen`  |  ChatResponseGen with model partial generation  |  
Source code in `llama-index-integrations/llms/llama-index-llms-sambanovasystems/llama_index/llms/sambanovasystems/base.py`  
| 
```
1502
1503
1504
1505
1506
1507
1508
1509
1510
1511
1512
1513
1514
1515
1516
1517
1518
1519
1520
1521
1522
1523
1524
1525
1526
1527
1528
```
 | 
```
@llm_chat_callback()
defstream_chat(
    self,
    messages: Sequence[ChatMessage],
    stop: Optional[List[str]] = None,
    **kwargs: Any,
) -> ChatResponseGen:
"""
    Stream the output of the SambaStudio model.

    Args:
        messages: the prompt composed of a list of messages.
        stop: a list of strings on which the model should stop generating.
              If generation stops due to a stop token, the stop token itself
              SHOULD BE INCLUDED as part of the output. This is not enforced
              across models right now, but it's a good practice to follow since
              it makes it much easier to parse the output of the model
              downstream and understand why generation stopped.

    Yields:
        chunk: ChatResponseGen with model partial generation

    """
    response = self._handle_request(messages, stop, streaming=True)
    for ai_message_chunk in self._process_stream_response(response):
        chunk = ChatResponse(message=ai_message_chunk)
        yield chunk

```
 |  
| --- | --- |  
###  achat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/sambanovasystems/#llama_index.llms.sambanovasystems.SambaStudio.achat "Permanent link")

```
achat(
    messages: Sequence[],
    stop: Optional[[]] = None,
    **kwargs: 
) -> 

```

Calls the chat implementation of the SambaStudio model.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `messages`  |  `Sequence[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  the prompt composed of a list of messages.  |  _required_  |  
|  `stop`  |  `Optional[List[str]]`  |  a list of strings on which the model should stop generating. If generation stops due to a stop token, the stop token itself SHOULD BE INCLUDED as part of the output. This is not enforced across models right now, but it's a good practice to follow since it makes it much easier to parse the output of the model downstream and understand why generation stopped.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  ChatResponse with model generation  |  
Source code in `llama-index-integrations/llms/llama-index-llms-sambanovasystems/llama_index/llms/sambanovasystems/base.py`  
| 
```
1544
1545
1546
1547
1548
1549
1550
1551
1552
1553
1554
1555
1556
1557
1558
1559
1560
1561
1562
1563
1564
1565
1566
1567
1568
1569
1570
1571
```
 | 
```
@llm_chat_callback()
async defachat(
    self,
    messages: Sequence[ChatMessage],
    stop: Optional[List[str]] = None,
    **kwargs: Any,
) -> ChatResponse:
"""
    Calls the chat implementation of the SambaStudio model.

    Args:
        messages: the prompt composed of a list of messages.
        stop: a list of strings on which the model should stop generating.
              If generation stops due to a stop token, the stop token itself
              SHOULD BE INCLUDED as part of the output. This is not enforced
              across models right now, but it's a good practice to follow since
              it makes it much easier to parse the output of the model
              downstream and understand why generation stopped.

    Returns:
        ChatResponse with model generation

    """
    response_dict = await self._handle_request_async(
        messages, stop, streaming=False
    )
    message = await self._process_response_async(response_dict)
    return ChatResponse(message=message)

```
 |  
| --- | --- |  
options: members: - SambaNovaCloud - SambaStudio
