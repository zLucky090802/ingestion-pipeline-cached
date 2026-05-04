# Huggingface
##  HuggingFaceLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/huggingface/#llama_index.llms.huggingface.HuggingFaceLLM "Permanent link")
Bases: `CustomLLM`
HuggingFace LLM.
Examples:
`pip install llama-index-llms-huggingface`

```
fromllama_index.llms.huggingfaceimport HuggingFaceLLM

defmessages_to_prompt(messages):
    prompt = ""
    for message in messages:
        if message.role == 'system':
        prompt += f"<|system|>\n{message.content}</s>\n"
        elif message.role == 'user':
        prompt += f"<|user|>\n{message.content}</s>\n"
        elif message.role == 'assistant':
        prompt += f"<|assistant|>\n{message.content}</s>\n"

    # ensure we start with a system prompt, insert blank if needed
    if not prompt.startswith("<|system|>\n"):
        prompt = "<|system|>\n</s>\n" + prompt

    # add final assistant prompt
    prompt = prompt + "<|assistant|>\n"

    return prompt

defcompletion_to_prompt(completion):
    return f"<|system|>\n</s>\n<|user|>\n{completion}</s>\n<|assistant|>\n"

importtorch
fromtransformersimport BitsAndBytesConfig
fromllama_index.core.promptsimport PromptTemplate
fromllama_index.llms.huggingfaceimport HuggingFaceLLM

# quantize to save memory
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)

llm = HuggingFaceLLM(
    model_name="HuggingFaceH4/zephyr-7b-beta",
    tokenizer_name="HuggingFaceH4/zephyr-7b-beta",
    context_window=3900,
    max_new_tokens=256,
    model_kwargs={"quantization_config": quantization_config},
    generate_kwargs={"temperature": 0.7, "top_k": 50, "top_p": 0.95},
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    device_map="auto",
)

response = llm.complete("What is the meaning of life?")
print(str(response))

```

Source code in `llama-index-integrations/llms/llama-index-llms-huggingface/llama_index/llms/huggingface/base.py`  
| 
```
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
```
 | 
```
classHuggingFaceLLM(CustomLLM):
r"""
    HuggingFace LLM.

    Examples:
        `pip install llama-index-llms-huggingface`

        ```python
        from llama_index.llms.huggingface import HuggingFaceLLM

        def messages_to_prompt(messages):
            prompt = ""
            for message in messages:
                if message.role == 'system':
                prompt += f"<|system|>\n{message.content}</s>\n"
                elif message.role == 'user':
                prompt += f"<|user|>\n{message.content}</s>\n"
                elif message.role == 'assistant':
                prompt += f"<|assistant|>\n{message.content}</s>\n"

            # ensure we start with a system prompt, insert blank if needed
            if not prompt.startswith("<|system|>\n"):
                prompt = "<|system|>\n</s>\n" + prompt

            # add final assistant prompt
            prompt = prompt + "<|assistant|>\n"

            return prompt

        def completion_to_prompt(completion):
            return f"<|system|>\n</s>\n<|user|>\n{completion}</s>\n<|assistant|>\n"

        import torch
        from transformers import BitsAndBytesConfig
        from llama_index.core.prompts import PromptTemplate
        from llama_index.llms.huggingface import HuggingFaceLLM

        # quantize to save memory
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,


        llm = HuggingFaceLLM(
            model_name="HuggingFaceH4/zephyr-7b-beta",
            tokenizer_name="HuggingFaceH4/zephyr-7b-beta",
            context_window=3900,
            max_new_tokens=256,
            model_kwargs={"quantization_config": quantization_config},
            generate_kwargs={"temperature": 0.7, "top_k": 50, "top_p": 0.95},
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            device_map="auto",


        response = llm.complete("What is the meaning of life?")
        print(str(response))
        ```

    """

    model_name: str = Field(
        default=DEFAULT_HUGGINGFACE_MODEL,
        description=(
            "The model name to use from HuggingFace. "
            "Unused if `model` is passed in directly."
        ),
    )
    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description=(LLMMetadata.model_fields["context_window"].description),
        gt=0,
    )
    max_new_tokens: int = Field(
        default=DEFAULT_NUM_OUTPUTS,
        description="The maximum number of tokens to generate.",
        gt=0,
    )
    system_prompt: str = Field(
        default="",
        description=(
            "The system prompt, containing any extra instructions or context. "
            "The model card on HuggingFace should specify if this is needed."
        ),
    )
    query_wrapper_prompt: PromptTemplate = Field(
        default=PromptTemplate("{query_str}"),
        description=(
            "The query wrapper prompt, containing the query placeholder. "
            "The model card on HuggingFace should specify if this is needed. "
            "Should contain a `{query_str}` placeholder."
        ),
    )
    tokenizer_name: str = Field(
        default=DEFAULT_HUGGINGFACE_MODEL,
        description=(
            "The name of the tokenizer to use from HuggingFace. "
            "Unused if `tokenizer` is passed in directly."
        ),
    )
    device_map: str = Field(
        default="auto", description="The device_map to use. Defaults to 'auto'."
    )
    stopping_ids: List[int] = Field(
        default_factory=list,
        description=(
            "The stopping ids to use. "
            "Generation stops when these token IDs are predicted."
        ),
    )
    tokenizer_outputs_to_remove: list = Field(
        default_factory=list,
        description=(
            "The outputs to remove from the tokenizer. "
            "Sometimes huggingface tokenizers return extra inputs that cause errors."
        ),
    )
    tokenizer_kwargs: dict = Field(
        default_factory=dict, description="The kwargs to pass to the tokenizer."
    )
    model_kwargs: dict = Field(
        default_factory=dict,
        description="The kwargs to pass to the model during initialization.",
    )
    generate_kwargs: dict = Field(
        default_factory=dict,
        description="The kwargs to pass to the model during generation.",
    )
    is_chat_model: bool = Field(
        default=False,
        description=(
            LLMMetadata.model_fields["is_chat_model"].description
            + " Be sure to verify that you either pass an appropriate tokenizer "
            "that can convert prompts to properly formatted chat messages or a "
            "`messages_to_prompt` that does so."
        ),
    )

    _model: Any = PrivateAttr()
    _tokenizer: Any = PrivateAttr()
    _stopping_criteria: Any = PrivateAttr()

    def__init__(
        self,
        context_window: int = DEFAULT_CONTEXT_WINDOW,
        max_new_tokens: int = DEFAULT_NUM_OUTPUTS,
        query_wrapper_prompt: Union[str, PromptTemplate] = "{query_str}",
        tokenizer_name: str = DEFAULT_HUGGINGFACE_MODEL,
        model_name: str = DEFAULT_HUGGINGFACE_MODEL,
        model: Optional[Any] = None,
        tokenizer: Optional[Any] = None,
        device_map: Optional[str] = "auto",
        stopping_ids: Optional[List[int]] = None,
        tokenizer_kwargs: Optional[dict] = None,
        tokenizer_outputs_to_remove: Optional[list] = None,
        model_kwargs: Optional[dict] = None,
        generate_kwargs: Optional[dict] = None,
        is_chat_model: Optional[bool] = False,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: str = "",
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
    ) -> None:
"""Initialize params."""
        model_kwargs = model_kwargs or {}
        model = model or AutoModelForCausalLM.from_pretrained(
            model_name, device_map=device_map, **model_kwargs
        )

        # check context_window
        config_dict = model.config.to_dict()
        model_context_window = int(
            config_dict.get("max_position_embeddings", context_window)
        )
        if model_context_window and model_context_window  context_window:
            logger.warning(
                f"Supplied context_window {context_window} is greater "
                f"than the model's max input size {model_context_window}. "
                "Disable this warning by setting a lower context_window."
            )
            context_window = model_context_window

        tokenizer_kwargs = tokenizer_kwargs or {}
        if "max_length" not in tokenizer_kwargs:
            tokenizer_kwargs["max_length"] = context_window

        tokenizer = tokenizer or AutoTokenizer.from_pretrained(
            tokenizer_name, **tokenizer_kwargs
        )

        if tokenizer.name_or_path != model.name_or_path:
            logger.warning(
                f"The model `{model.name_or_path}` and tokenizer `{tokenizer.name_or_path}` "
                f"are different, please ensure that they are compatible."
            )

        # setup stopping criteria
        stopping_ids_list = stopping_ids or []

        classStopOnTokens(StoppingCriteria):
            def__call__(
                self,
                input_ids: torch.LongTensor,
                scores: torch.FloatTensor,
                **kwargs: Any,
            ) -> bool:
                for stop_id in stopping_ids_list:
                    if input_ids[0][-1] == stop_id:
                        return True
                return False

        stopping_criteria = StoppingCriteriaList([StopOnTokens()])

        if isinstance(query_wrapper_prompt, str):
            query_wrapper_prompt = PromptTemplate(query_wrapper_prompt)

        messages_to_prompt = messages_to_prompt or self._tokenizer_messages_to_prompt

        super().__init__(
            context_window=context_window,
            max_new_tokens=max_new_tokens,
            query_wrapper_prompt=query_wrapper_prompt,
            tokenizer_name=tokenizer_name,
            model_name=model_name,
            device_map=device_map,
            stopping_ids=stopping_ids or [],
            tokenizer_kwargs=tokenizer_kwargs or {},
            tokenizer_outputs_to_remove=tokenizer_outputs_to_remove or [],
            model_kwargs=model_kwargs or {},
            generate_kwargs=generate_kwargs or {},
            is_chat_model=is_chat_model,
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )

        self._model = model
        self._tokenizer = tokenizer
        self._stopping_criteria = stopping_criteria

    @classmethod
    defclass_name(cls) -> str:
        return "HuggingFace_LLM"

    @property
    defmetadata(self) -> LLMMetadata:
"""LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.max_new_tokens,
            model_name=self.model_name,
            is_chat_model=self.is_chat_model,
        )

    def_tokenizer_messages_to_prompt(self, messages: Sequence[ChatMessage]) -> str:
"""Use the tokenizer to convert messages to prompt. Fallback to generic."""
        if hasattr(self._tokenizer, "apply_chat_template"):
            messages_dict = [
                {"role": message.role.value, "content": message.content}
                for message in messages
            ]
            return self._tokenizer.apply_chat_template(
                messages_dict, tokenize=False, add_generation_prompt=True
            )

        return generic_messages_to_prompt(messages)

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
"""Completion endpoint."""
        full_prompt = prompt
        if not formatted:
            if self.query_wrapper_prompt:
                full_prompt = self.query_wrapper_prompt.format(query_str=prompt)
            if self.completion_to_prompt:
                full_prompt = self.completion_to_prompt(full_prompt)
            elif self.system_prompt:
                full_prompt = f"{self.system_prompt}{full_prompt}"

        inputs = self._tokenizer(full_prompt, return_tensors="pt")
        inputs = inputs.to(self._model.device)

        # remove keys from the tokenizer if needed, to avoid HF errors
        for key in self.tokenizer_outputs_to_remove:
            if key in inputs:
                inputs.pop(key, None)

        tokens = self._model.generate(
            **inputs,
            max_new_tokens=self.max_new_tokens,
            stopping_criteria=self._stopping_criteria,
            **self.generate_kwargs,
        )
        completion_tokens = tokens[0][inputs["input_ids"].size(1) :]
        completion = self._tokenizer.decode(completion_tokens, skip_special_tokens=True)

        return CompletionResponse(text=completion, raw={"model_output": tokens})

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
"""Streaming completion endpoint."""
        fromtransformersimport TextIteratorStreamer

        full_prompt = prompt
        if not formatted:
            if self.query_wrapper_prompt:
                full_prompt = self.query_wrapper_prompt.format(query_str=prompt)
            if self.system_prompt:
                full_prompt = f"{self.system_prompt}{full_prompt}"

        inputs = self._tokenizer(full_prompt, return_tensors="pt")
        inputs = inputs.to(self._model.device)

        # remove keys from the tokenizer if needed, to avoid HF errors
        for key in self.tokenizer_outputs_to_remove:
            if key in inputs:
                inputs.pop(key, None)

        streamer = TextIteratorStreamer(
            self._tokenizer, skip_prompt=True, skip_special_tokens=True
        )
        generation_kwargs = dict(
            inputs,
            streamer=streamer,
            max_new_tokens=self.max_new_tokens,
            stopping_criteria=self._stopping_criteria,
            **self.generate_kwargs,
        )

        # generate in background thread
        # NOTE/TODO: token counting doesn't work with streaming
        thread = Thread(target=self._model.generate, kwargs=generation_kwargs)
        thread.start()

        # create generator based off of streamer
        defgen() -> CompletionResponseGen:
            text = ""
            for x in streamer:
                text += x
                yield CompletionResponse(text=text, delta=x)

        return gen()

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        prompt = self.messages_to_prompt(messages)
        completion_response = self.complete(prompt, formatted=True, **kwargs)
        return completion_response_to_chat_response(completion_response)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        prompt = self.messages_to_prompt(messages)
        completion_response = self.stream_complete(prompt, formatted=True, **kwargs)
        return stream_completion_response_to_chat_response(completion_response)

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/huggingface/#llama_index.llms.huggingface.HuggingFaceLLM.metadata "Permanent link")

```
metadata: 

```

LLM metadata.
###  complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/huggingface/#llama_index.llms.huggingface.HuggingFaceLLM.complete "Permanent link")

```
complete(
    prompt: , formatted:  = False, **kwargs: 
) -> 

```

Completion endpoint.
Source code in `llama-index-integrations/llms/llama-index-llms-huggingface/llama_index/llms/huggingface/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defcomplete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponse:
"""Completion endpoint."""
    full_prompt = prompt
    if not formatted:
        if self.query_wrapper_prompt:
            full_prompt = self.query_wrapper_prompt.format(query_str=prompt)
        if self.completion_to_prompt:
            full_prompt = self.completion_to_prompt(full_prompt)
        elif self.system_prompt:
            full_prompt = f"{self.system_prompt}{full_prompt}"

    inputs = self._tokenizer(full_prompt, return_tensors="pt")
    inputs = inputs.to(self._model.device)

    # remove keys from the tokenizer if needed, to avoid HF errors
    for key in self.tokenizer_outputs_to_remove:
        if key in inputs:
            inputs.pop(key, None)

    tokens = self._model.generate(
        **inputs,
        max_new_tokens=self.max_new_tokens,
        stopping_criteria=self._stopping_criteria,
        **self.generate_kwargs,
    )
    completion_tokens = tokens[0][inputs["input_ids"].size(1) :]
    completion = self._tokenizer.decode(completion_tokens, skip_special_tokens=True)

    return CompletionResponse(text=completion, raw={"model_output": tokens})

```
 |  
| --- | --- |  
###  stream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/huggingface/#llama_index.llms.huggingface.HuggingFaceLLM.stream_complete "Permanent link")

```
stream_complete(
    prompt: , formatted:  = False, **kwargs: 
) -> CompletionResponseGen

```

Streaming completion endpoint.
Source code in `llama-index-integrations/llms/llama-index-llms-huggingface/llama_index/llms/huggingface/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defstream_complete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponseGen:
"""Streaming completion endpoint."""
    fromtransformersimport TextIteratorStreamer

    full_prompt = prompt
    if not formatted:
        if self.query_wrapper_prompt:
            full_prompt = self.query_wrapper_prompt.format(query_str=prompt)
        if self.system_prompt:
            full_prompt = f"{self.system_prompt}{full_prompt}"

    inputs = self._tokenizer(full_prompt, return_tensors="pt")
    inputs = inputs.to(self._model.device)

    # remove keys from the tokenizer if needed, to avoid HF errors
    for key in self.tokenizer_outputs_to_remove:
        if key in inputs:
            inputs.pop(key, None)

    streamer = TextIteratorStreamer(
        self._tokenizer, skip_prompt=True, skip_special_tokens=True
    )
    generation_kwargs = dict(
        inputs,
        streamer=streamer,
        max_new_tokens=self.max_new_tokens,
        stopping_criteria=self._stopping_criteria,
        **self.generate_kwargs,
    )

    # generate in background thread
    # NOTE/TODO: token counting doesn't work with streaming
    thread = Thread(target=self._model.generate, kwargs=generation_kwargs)
    thread.start()

    # create generator based off of streamer
    defgen() -> CompletionResponseGen:
        text = ""
        for x in streamer:
            text += x
            yield CompletionResponse(text=text, delta=x)

    return gen()

```
 |  
| --- | --- |  
options: members: - HuggingFaceLLM
