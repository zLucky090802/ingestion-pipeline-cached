# Mistral rs
##  MistralRS [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/mistral_rs/#llama_index.llms.mistral_rs.MistralRS "Permanent link")
Bases: `CustomLLM`
MistralRS LLM.
Examples:
Install `mistralrs` following instructions: https://github.com/EricLBuehler/mistral.rs/blob/master/mistralrs-pyo3/README.md#installation-from-pypi
Then `pip install llama-index-llms-mistral-rs`
This LLM provides automatic chat templating as an option. If you do not provide `messages_to_prompt`, mistral.rs will automatically determine one. You can specify a JINJA chat template by passing it in `model_kwargs` in the `chat_template` key.

```
fromllama_index.llms.mistral_rsimport MistralRS
frommistralrsimport Which

llm = MistralRS(
    which = Which.XLora(
        model_id=None,  # Automatically determine from ordering file
        tokenizer_json=None,
        repeat_last_n=64,
        xlora_model_id="lamm-mit/x-lora"
        order="xlora-paper-ordering.json", # Make sure you copy the ordering file from `mistral.rs/orderings`
        tgt_non_granular_index=None,
        arch=Architecture.Mistral,
    ),
    temperature=0.1,
    max_new_tokens=256,
    context_window=3900,
    generate_kwargs={},
    verbose=True,
)

response = llm.complete("Hello, how are you?")
print(str(response))

```

Source code in `llama-index-integrations/llms/llama-index-llms-mistral-rs/llama_index/llms/mistral_rs/base.py`  
| 
```
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
```
 | 
```
classMistralRS(CustomLLM):
r"""
    MistralRS LLM.

    Examples:
        Install `mistralrs` following instructions:
        https://github.com/EricLBuehler/mistral.rs/blob/master/mistralrs-pyo3/README.md#installation-from-pypi

        Then `pip install llama-index-llms-mistral-rs`

        This LLM provides automatic chat templating as an option. If you do not provide `messages_to_prompt`,
        mistral.rs will automatically determine one. You can specify a JINJA chat template by passing it in
        `model_kwargs` in the `chat_template` key.

        ```python
        from llama_index.llms.mistral_rs import MistralRS
        from mistralrs import Which

        llm = MistralRS(
            which = Which.XLora(
                model_id=None,  # Automatically determine from ordering file
                tokenizer_json=None,
                repeat_last_n=64,
                xlora_model_id="lamm-mit/x-lora"
                order="xlora-paper-ordering.json", # Make sure you copy the ordering file from `mistral.rs/orderings`
                tgt_non_granular_index=None,
                arch=Architecture.Mistral,

            temperature=0.1,
            max_new_tokens=256,
            context_window=3900,
            generate_kwargs={},
            verbose=True,


        response = llm.complete("Hello, how are you?")
        print(str(response))
        ```

    """

    model_url: Optional[str] = Field(description="local")
    model_path: Optional[str] = Field(description="local")
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        description="The temperature to use for sampling.",
        ge=0.0,
        le=1.0,
    )
    max_new_tokens: int = Field(
        default=DEFAULT_NUM_OUTPUTS,
        description="The maximum number of tokens to generate.",
        gt=0,
    )
    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description="The maximum number of context tokens for the model.",
        gt=0,
    )
    generate_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Kwargs used for generation."
    )
    model_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Kwargs used for model initialization."
    )
    _runner: "Runner" = PrivateAttr("Mistral.rs model runner.")
    _has_messages_to_prompt: bool = PrivateAttr("If `messages_to_prompt` is provided.")

    def__init__(
        self,
        which: "Which",
        temperature: float = DEFAULT_TEMPERATURE,
        max_new_tokens: int = DEFAULT_NUM_OUTPUTS,
        context_window: int = DEFAULT_CONTEXT_WINDOW,
        top_k: int = DEFAULT_TOPK,
        top_p: int = DEFAULT_TOPP,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        in_situ_quant: Optional[str] = None,
        max_seqs: int = DEFAULT_MAX_SEQS,
        token_source: str = "cache",
        prefix_cache_n: str = DEFAULT_PREFIX_CACHE_N,
        no_kv_cache: bool = False,
        chat_template: Optional[str] = None,
        top_logprobs: Optional[int] = None,
        callback_manager: Optional[CallbackManager] = None,
        generate_kwargs: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
    ) -> None:
        generate_kwargs = generate_kwargs or {}
        generate_kwargs.update(
            {
                "temperature": temperature,
                "max_tokens": max_new_tokens,
                "top_k": top_k,
                "top_p": top_p,
                "top_logprobs": top_logprobs,
                "logprobs": top_logprobs is not None,
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty,
            }
        )

        super().__init__(
            model_path="local",
            model_url="local",
            temperature=temperature,
            context_window=context_window,
            max_new_tokens=max_new_tokens,
            callback_manager=callback_manager,
            generate_kwargs=generate_kwargs,
            model_kwargs={},
            verbose=True,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )

        self._runner = Runner(
            which=which,
            token_source=token_source,
            max_seqs=max_seqs,
            prefix_cache_n=prefix_cache_n,
            no_kv_cache=no_kv_cache,
            chat_template=chat_template,
            in_situ_quant=in_situ_quant,
        )
        self._has_messages_to_prompt = messages_to_prompt is not None

    @classmethod
    defclass_name(cls) -> str:
        return "MistralRS"

    @property
    defmetadata(self) -> LLMMetadata:
"""LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.max_new_tokens,
            model_name=self.model_path,
        )

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        try:
            frommistralrsimport ChatCompletionRequest
        except ImportError as e:
            raise ValueError(
                "Missing `mistralrs` package. Install via `pip install mistralrs`."
            ) frome
        if self._has_messages_to_prompt:
            messages = self.messages_to_prompt(messages)
        else:
            messages = llama_index_to_mistralrs_messages(messages)
        self.generate_kwargs.update({"stream": False})

        request = ChatCompletionRequest(
            messages=messages,
            model="",
            logit_bias=None,
            **self.generate_kwargs,
        )

        response = self._runner.send_chat_completion_request(request)
        return CompletionResponse(
            text=response.choices[0].message.content,
            logprobs=extract_logprobs(response),
        )

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        try:
            frommistralrsimport ChatCompletionRequest
        except ImportError as e:
            raise ValueError(
                "Missing `mistralrs` package. Install via `pip install mistralrs`."
            ) frome
        if self._has_messages_to_prompt:
            messages = self.messages_to_prompt(messages)
        else:
            messages = llama_index_to_mistralrs_messages(messages)
        self.generate_kwargs.update({"stream": True})

        request = ChatCompletionRequest(
            messages=messages,
            model="",
            logit_bias=None,
            **self.generate_kwargs,
        )

        streamer = self._runner.send_chat_completion_request(request)

        defgen() -> CompletionResponseGen:
            text = ""
            for response in streamer:
                delta = response.choices[0].delta.content
                text += delta
                yield ChatResponse(
                    message=ChatMessage(
                        role=MessageRole.ASSISTANT,
                        content=delta,
                    ),
                    delta=delta,
                    logprobs=extract_logprobs_stream(response),
                )

        return gen()

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        try:
            frommistralrsimport ChatCompletionRequest
        except ImportError as e:
            raise ValueError(
                "Missing `mistralrs` package. Install via `pip install mistralrs`."
            ) frome
        self.generate_kwargs.update({"stream": False})
        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        request = ChatCompletionRequest(
            messages=prompt,
            model="",
            logit_bias=None,
            **self.generate_kwargs,
        )
        completion_response = self._runner.send_chat_completion_request(request)
        return CompletionResponse(
            text=completion_response.choices[0].message.content,
            logprobs=extract_logprobs(completion_response),
        )

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        try:
            frommistralrsimport ChatCompletionRequest
        except ImportError as e:
            raise ValueError(
                "Missing `mistralrs` package. Install via `pip install mistralrs`."
            ) frome
        self.generate_kwargs.update({"stream": True})
        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        request = ChatCompletionRequest(
            messages=prompt,
            model="",
            logit_bias=None,
            **self.generate_kwargs,
        )

        streamer = self._runner.send_chat_completion_request(request)

        defgen() -> CompletionResponseGen:
            text = ""
            for response in streamer:
                delta = response.choices[0].delta.content
                text += delta
                yield CompletionResponse(
                    delta=delta,
                    text=text,
                    logprobs=extract_logprobs_stream(response),
                )

        return gen()

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/mistral_rs/#llama_index.llms.mistral_rs.MistralRS.metadata "Permanent link")

```
metadata: 

```

LLM metadata.
options: members: - MistralRs
