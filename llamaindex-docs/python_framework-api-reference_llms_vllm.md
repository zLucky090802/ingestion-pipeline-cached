# Vllm
##  Vllm [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/vllm/#llama_index.llms.vllm.Vllm "Permanent link")
Bases: 
Vllm LLM.
This class runs a vLLM model locally.
Examples:
`pip install llama-index-llms-vllm`

```
fromllama_index.llms.vllmimport Vllm

# specific functions to format for mistral instruct
defmessages_to_prompt(messages):
    prompt = "\n".join([str(x) for x in messages])
    return f"<s>[INST] {prompt} [/INST] </s>\n"

defcompletion_to_prompt(completion):
    return f"<s>[INST] {completion} [/INST] </s>\n"

llm = Vllm(
    model="mistralai/Mistral-7B-Instruct-v0.1",
    tensor_parallel_size=4,
    max_new_tokens=256,
    vllm_kwargs={"swap_space": 1, "gpu_memory_utilization": 0.5},
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
)

llm.complete(
    "What is a black hole?"
)

```

Source code in `llama-index-integrations/llms/llama-index-llms-vllm/llama_index/llms/vllm/base.py`  
| 
```
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
```
 | 
```
classVllm(LLM):
r"""
    Vllm LLM.

    This class runs a vLLM model locally.

    Examples:
        `pip install llama-index-llms-vllm`


        ```python
        from llama_index.llms.vllm import Vllm

        # specific functions to format for mistral instruct
        def messages_to_prompt(messages):
            prompt = "\n".join([str(x) for x in messages])
            return f"<s>[INST] {prompt} [/INST] </s>\n"

        def completion_to_prompt(completion):
            return f"<s>[INST] {completion} [/INST] </s>\n"

        llm = Vllm(
            model="mistralai/Mistral-7B-Instruct-v0.1",
            tensor_parallel_size=4,
            max_new_tokens=256,
            vllm_kwargs={"swap_space": 1, "gpu_memory_utilization": 0.5},
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,


        llm.complete(
            "What is a black hole?"

        ```

    """

    model: Optional[str] = Field(description="The HuggingFace Model to use.")

    temperature: float = Field(description="The temperature to use for sampling.")

    tensor_parallel_size: Optional[int] = Field(
        default=1,
        description="The number of GPUs to use for distributed execution with tensor parallelism.",
    )

    trust_remote_code: Optional[bool] = Field(
        default=True,
        description="Trust remote code (e.g., from HuggingFace) when downloading the model and tokenizer.",
    )

    n: int = Field(
        default=1,
        description="Number of output sequences to return for the given prompt.",
    )

    best_of: Optional[int] = Field(
        default=None,
        description="Number of output sequences that are generated from the prompt.",
    )

    presence_penalty: float = Field(
        default=0.0,
        description="Float that penalizes new tokens based on whether they appear in the generated text so far.",
    )

    frequency_penalty: float = Field(
        default=0.0,
        description="Float that penalizes new tokens based on their frequency in the generated text so far.",
    )

    top_p: float = Field(
        default=1.0,
        description="Float that controls the cumulative probability of the top tokens to consider.",
    )

    top_k: int = Field(
        default=-1,
        description="Integer that controls the number of top tokens to consider.",
    )

    stop: Optional[List[str]] = Field(
        default=None,
        description="List of strings that stop the generation when they are generated.",
    )

    ignore_eos: bool = Field(
        default=False,
        description="Whether to ignore the EOS token and continue generating tokens after the EOS token is generated.",
    )

    max_new_tokens: int = Field(
        default=512,
        description="Maximum number of tokens to generate per output sequence.",
    )

    logprobs: Optional[int] = Field(
        default=None,
        description="Number of log probabilities to return per output token.",
    )

    dtype: str = Field(
        default="auto",
        description="The data type for the model weights and activations.",
    )

    download_dir: Optional[str] = Field(
        default=None,
        description="Directory to download and load the weights. (Default to the default cache dir of huggingface)",
    )

    vllm_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Holds any model parameters valid for `vllm.LLM` call not explicitly specified.",
    )

    api_url: str = Field(description="The api url for vllm server")

    is_chat_model: bool = Field(
        default=False,
        description=LLMMetadata.model_fields["is_chat_model"].description,
    )

    _client: Any = PrivateAttr()

    def__init__(
        self,
        model: str = "facebook/opt-125m",
        temperature: float = 1.0,
        tensor_parallel_size: int = 1,
        trust_remote_code: bool = False,
        n: int = 1,
        best_of: Optional[int] = None,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        top_p: float = 1.0,
        top_k: int = -1,
        stop: Optional[List[str]] = None,
        ignore_eos: bool = False,
        max_new_tokens: int = 512,
        logprobs: Optional[int] = None,
        dtype: str = "auto",
        download_dir: Optional[str] = None,
        vllm_kwargs: Dict[str, Any] = {},
        api_url: Optional[str] = "",
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        is_chat_model: Optional[bool] = False,
    ) -> None:
        callback_manager = callback_manager or CallbackManager([])
        super().__init__(
            model=model,
            temperature=temperature,
            n=n,
            best_of=best_of,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            top_p=top_p,
            top_k=top_k,
            stop=stop,
            ignore_eos=ignore_eos,
            max_new_tokens=max_new_tokens,
            logprobs=logprobs,
            dtype=dtype,
            download_dir=download_dir,
            vllm_kwargs=vllm_kwargs,
            api_url=api_url,
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
            is_chat_model=is_chat_model,
        )
        if not api_url:
            try:
                fromvllmimport LLM as VLLModel
            except ImportError:
                raise ImportError(
                    "Could not import vllm python package. "
                    "Please install it with `pip install vllm`."
                )
            self._client = VLLModel(
                model=model,
                tensor_parallel_size=tensor_parallel_size,
                trust_remote_code=trust_remote_code,
                dtype=dtype,
                download_dir=download_dir,
                **vllm_kwargs,
            )
        else:
            self._client = None

    @classmethod
    defclass_name(cls) -> str:
        return "Vllm"

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(model_name=self.model, is_chat_model=self.is_chat_model)

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "temperature": self.temperature,
            "max_tokens": self.max_new_tokens,
            "n": self.n,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "best_of": self.best_of,
            "ignore_eos": self.ignore_eos,
            "stop": self.stop,
            "logprobs": self.logprobs,
            "top_k": self.top_k,
            "top_p": self.top_p,
        }
        return {**base_kwargs}

    @atexit.register
    defclose():
        importtorch
        importgc

        if torch.cuda.is_available():
            gc.collect()
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

    def_get_all_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        return {
            **self._model_kwargs,
            **kwargs,
        }

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        kwargs = kwargs if kwargs else {}
        prompt = self.messages_to_prompt(messages)
        completion_response = self.complete(prompt, **kwargs)
        return completion_response_to_chat_response(completion_response)

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        kwargs = kwargs if kwargs else {}
        params = {**self._model_kwargs, **kwargs}

        fromvllmimport SamplingParams

        # build sampling parameters
        sampling_params = SamplingParams(**params)
        outputs = self._client.generate([prompt], sampling_params)
        return CompletionResponse(text=outputs[0].outputs[0].text)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        raise (ValueError("Not Implemented"))

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        raise (ValueError("Not Implemented"))

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        kwargs = kwargs if kwargs else {}
        return self.chat(messages, **kwargs)

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        kwargs = kwargs if kwargs else {}
        return self.complete(prompt, **kwargs)

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        raise (ValueError("Not Implemented"))

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        raise (ValueError("Not Implemented"))

```
 |  
| --- | --- |  
##  VllmServer [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/vllm/#llama_index.llms.vllm.VllmServer "Permanent link")
Bases: 
Vllm LLM.
This class connects to a vLLM server (non-openai versions).
If using the OpenAI-API vLLM server, please see the `OpenAILike` LLM class.
Examples:
`pip install llama-index-llms-vllm`

```
fromllama_index.llms.vllmimport VllmServer

# specific functions to format for mistral instruct
defmessages_to_prompt(messages):
    prompt = "\n".join([str(x) for x in messages])
    return f"<s>[INST] {prompt} [/INST] </s>\n"

defcompletion_to_prompt(completion):
    return f"<s>[INST] {completion} [/INST] </s>\n"

llm = VllmServer(
    api_url=api_url,
    max_new_tokens=256,
    temperature=0.1,
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
)

llm.complete(
    "What is a black hole?"
)

```

Source code in `llama-index-integrations/llms/llama-index-llms-vllm/llama_index/llms/vllm/base.py`  
| 
```
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
```
 | 
```
classVllmServer(Vllm):
r"""
    Vllm LLM.

    This class connects to a vLLM server (non-openai versions).

    If using the OpenAI-API vLLM server, please see the `OpenAILike` LLM class.

    Examples:
        `pip install llama-index-llms-vllm`


        ```python
        from llama_index.llms.vllm import VllmServer

        # specific functions to format for mistral instruct
        def messages_to_prompt(messages):
            prompt = "\n".join([str(x) for x in messages])
            return f"<s>[INST] {prompt} [/INST] </s>\n"

        def completion_to_prompt(completion):
            return f"<s>[INST] {completion} [/INST] </s>\n"

        llm = VllmServer(
            api_url=api_url,
            max_new_tokens=256,
            temperature=0.1,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,


        llm.complete(
            "What is a black hole?"

        ```

    """

    openai_like: bool = Field(
        default=False,
        description="Treat the endpoint as OpenAI-compatible chat/completions API (streaming supported).",
    )
    api_headers: Dict[str, str] = Field(
        default_factory=dict,
        description="Additional headers to send to the vLLM server.",
    )
    timeout: float = Field(
        default=60.0, description="Request timeout (seconds) for server calls."
    )

    def__init__(
        self,
        model: str = "facebook/opt-125m",
        api_url: str = "http://localhost:8000",
        temperature: float = 1.0,
        tensor_parallel_size: Optional[int] = 1,
        trust_remote_code: Optional[bool] = True,
        n: int = 1,
        best_of: Optional[int] = None,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        top_p: float = 1.0,
        top_k: int = -1,
        stop: Optional[List[str]] = None,
        ignore_eos: bool = False,
        max_new_tokens: int = 512,
        logprobs: Optional[int] = None,
        dtype: str = "auto",
        download_dir: Optional[str] = None,
        messages_to_prompt: Optional[Callable] = None,
        completion_to_prompt: Optional[Callable] = None,
        vllm_kwargs: Dict[str, Any] = {},
        callback_manager: Optional[CallbackManager] = None,
        output_parser: Optional[BaseOutputParser] = None,
        openai_like: bool = False,
        api_headers: Optional[Dict[str, str]] = None,
        timeout: float = 60.0,
    ) -> None:
        messages_to_prompt = messages_to_prompt or generic_messages_to_prompt
        completion_to_prompt = completion_to_prompt or (lambda x: x)
        callback_manager = callback_manager or CallbackManager([])

        super().__init__(
            model=model,
            temperature=temperature,
            n=n,
            best_of=best_of,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            top_p=top_p,
            top_k=top_k,
            stop=stop,
            ignore_eos=ignore_eos,
            max_new_tokens=max_new_tokens,
            logprobs=logprobs,
            dtype=dtype,
            download_dir=download_dir,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            vllm_kwargs=vllm_kwargs,
            api_url=api_url,
            callback_manager=callback_manager,
            output_parser=output_parser,
        )
        self._client = None
        self.openai_like = openai_like
        self.api_headers = api_headers or {}
        self.timeout = timeout

    @classmethod
    defclass_name(cls) -> str:
        return "VllmServer"

    def__del__(self) -> None: ...

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        kwargs = kwargs if kwargs else {}
        params = {**self._model_kwargs, **kwargs}

        if self.openai_like:
            payload = self._build_openai_payload(prompt, params, chat=False)
            response = post_openai_chat_request(
                self.api_url,
                payload,
                headers=self.api_headers,
                timeout=self.timeout,
                stream=False,
            )
            text = get_openai_chat_response(response)
            return CompletionResponse(text=text)

        sampling_params = dict(**params)
        sampling_params["prompt"] = prompt
        response = post_http_request(
            self.api_url,
            sampling_params,
            stream=False,
            headers=self.api_headers,
            timeout=self.timeout,
        )
        output = get_response(response)
        return CompletionResponse(text=output[0])

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        kwargs = kwargs if kwargs else {}
        params = {**self._model_kwargs, **kwargs}

        if self.openai_like:
            payload = self._build_openai_payload(prompt, params, chat=False)
            response = post_openai_chat_request(
                self.api_url,
                payload,
                headers=self.api_headers,
                timeout=self.timeout,
                stream=True,
            )

            defgen() -> CompletionResponseGen:
                accum = ""
                for delta in get_openai_streaming_deltas(response):
                    accum += delta
                    yield CompletionResponse(text=accum, delta=delta)

            return gen()

        sampling_params = dict(**params)
        sampling_params["prompt"] = prompt
        response = post_http_request(
            self.api_url,
            sampling_params,
            stream=True,
            headers=self.api_headers,
            timeout=self.timeout,
        )

        defgen() -> CompletionResponseGen:
            prev_prefix_len = len(prompt)
            for chunk in response.iter_lines(
                chunk_size=8192, decode_unicode=False, delimiter=b"\0"
            ):
                if not chunk:
                    continue
                data = json.loads(chunk.decode("utf-8"))
                increasing_concat = data["text"][0]
                pref = prev_prefix_len
                prev_prefix_len = len(increasing_concat)
                yield CompletionResponse(
                    text=increasing_concat, delta=increasing_concat[pref:]
                )

        return gen()

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        kwargs = kwargs if kwargs else {}
        return self.complete(prompt, **kwargs)

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        kwargs = kwargs if kwargs else {}
        params = {**self._model_kwargs, **kwargs}

        # build sampling parameters
        sampling_params = dict(**params)
        sampling_params["prompt"] = prompt

        async defgen() -> CompletionResponseAsyncGen:
            for message in self.stream_complete(prompt, **kwargs):
                yield message

        return gen()

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        prompt = self.messages_to_prompt(messages)
        completion_response = self.stream_complete(prompt, **kwargs)
        return stream_completion_response_to_chat_response(completion_response)

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        async defgen() -> ChatResponseAsyncGen:
            for message in self.stream_chat(messages, **kwargs):
                yield message

        return gen()

    def_messages_to_prompt_text(self, messages: Sequence[ChatMessage]) -> str:
        # Convert chat messages to a plain text prompt for OpenAI-like chat completion.
        # This keeps parity with existing message->prompt formatting.
        return self.messages_to_prompt(messages)

    def_build_openai_payload(
        self,
        prompt: str,
        params: Dict[str, Any],
        chat: bool,
        messages: Optional[Sequence[ChatMessage]] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "temperature": params.get("temperature", self.temperature),
            "top_p": params.get("top_p", self.top_p),
            "n": params.get("n", self.n),
            "max_tokens": params.get("max_new_tokens", self.max_new_tokens),
        }

        # Map stop sequences if provided
        if params.get("stop"):
            payload["stop"] = params["stop"]

        if messages:
            payload["messages"] = [
                {
                    "role": msg.role.value if hasattr(msg.role, "value") else msg.role,
                    "content": msg.content,
                }
                for msg in messages
            ]
        else:
            payload["messages"] = [{"role": "user", "content": prompt}]
        return payload

```
 |  
| --- | --- |  
options: members: - Vllm - VllmServer
