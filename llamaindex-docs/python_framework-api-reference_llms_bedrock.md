# Bedrock
##  Bedrock [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/bedrock/#llama_index.llms.bedrock.Bedrock "Permanent link")
Bases: 
Bedrock LLM.
Examples:
`pip install llama-index-llms-bedrock`

```
fromllama_index.llms.bedrockimport Bedrock

llm = Bedrock(
    model="amazon.titan-text-express-v1",
    aws_access_key_id="AWS Access Key ID to use",
    aws_secret_access_key="AWS Secret Access Key to use",
    aws_session_token="AWS Session Token to use",
    region_name="AWS Region to use, eg. us-east-1",
)

resp = llm.complete("Paul Graham is ")
print(resp)

```

Source code in `llama-index-integrations/llms/llama-index-llms-bedrock/llama_index/llms/bedrock/base.py`  
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
```
 | 
```
@deprecated.deprecated(
    reason=(
        "Should use `llama-index-llms-bedrock-converse` instead, the converse API is the recommended way to use Bedrock.\n"
        "See: https://docs.llamaindex.ai/en/stable/examples/llm/bedrock_converse/"
    )
)
classBedrock(LLM):
"""
    Bedrock LLM.

    Examples:
        `pip install llama-index-llms-bedrock`

        ```python
        from llama_index.llms.bedrock import Bedrock

        llm = Bedrock(
            model="amazon.titan-text-express-v1",
            aws_access_key_id="AWS Access Key ID to use",
            aws_secret_access_key="AWS Secret Access Key to use",
            aws_session_token="AWS Session Token to use",
            region_name="AWS Region to use, eg. us-east-1",


        resp = llm.complete("Paul Graham is ")
        print(resp)
        ```

    """

    model: str = Field(description="The modelId of the Bedrock model to use.")
    temperature: float = Field(description="The temperature to use for sampling.")
    max_tokens: int = Field(description="The maximum number of tokens to generate.")
    context_size: int = Field("The maximum number of tokens available for input.")
    profile_name: Optional[str] = Field(
        description="The name of aws profile to use. If not given, then the default profile is used."
    )
    aws_access_key_id: Optional[str] = Field(
        description="AWS Access Key ID to use", exclude=True
    )
    aws_secret_access_key: Optional[str] = Field(
        description="AWS Secret Access Key to use", exclude=True
    )
    aws_session_token: Optional[str] = Field(
        description="AWS Session Token to use", exclude=True
    )
    region_name: Optional[str] = Field(
        description="AWS region name to use. Uses region configured in AWS CLI if not passed",
        exclude=True,
    )
    botocore_session: Optional[Any] = Field(
        description="Use this Botocore session instead of creating a new default one.",
        exclude=True,
    )
    botocore_config: Optional[Any] = Field(
        description="Custom configuration object to use instead of the default generated one.",
        exclude=True,
    )
    max_retries: int = Field(
        default=10, description="The maximum number of API retries.", gt=0
    )
    timeout: float = Field(
        default=60.0,
        description="The timeout for the Bedrock API request in seconds. It will be used for both connect and read timeouts.",
    )
    guardrail_identifier: Optional[str] = (
        Field(
            description="The unique identifier of the guardrail that you want to use. If you don’t provide a value, no guardrail is applied to the invocation."
        ),
    )
    guardrail_version: Optional[str] = (
        Field(
            description="The version number for the guardrail. The value can also be DRAFT"
        ),
    )
    trace: Optional[str] = (
        Field(
            description="Specifies whether to enable or disable the Bedrock trace. If enabled, you can see the full Bedrock trace."
        ),
    )
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional kwargs for the bedrock invokeModel request.",
    )

    _client: Any = PrivateAttr()
    _provider: Provider = PrivateAttr()

    def__init__(
        self,
        model: str,
        temperature: Optional[float] = DEFAULT_TEMPERATURE,
        max_tokens: Optional[int] = 512,
        context_size: Optional[int] = None,
        profile_name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        region_name: Optional[str] = None,
        botocore_session: Optional[Any] = None,
        client: Optional[Any] = None,
        timeout: Optional[float] = 60.0,
        max_retries: Optional[int] = 10,
        botocore_config: Optional[Any] = None,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        guardrail_identifier: Optional[str] = None,
        guardrail_version: Optional[str] = None,
        trace: Optional[str] = None,
        provider_type: Optional[ProviderType] = None,
        **kwargs: Any,
    ) -> None:
        if context_size is None and model not in BEDROCK_FOUNDATION_LLMS:
            raise ValueError(
                "`context_size` argument not provided and"
                " model provided refers to a non-foundation model."
                " Please specify the context_size"
            )

        session_kwargs = {
            "profile_name": profile_name,
            "region_name": region_name,
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "aws_session_token": aws_session_token,
            "botocore_session": botocore_session,
        }
        config = None
        try:
            importboto3
            frombotocore.configimport Config

            config = (
                Config(
                    retries={"max_attempts": max_retries, "mode": "standard"},
                    connect_timeout=timeout,
                    read_timeout=timeout,
                    user_agent_extra="x-client-framework:llama_index",
                )
                if botocore_config is None
                else botocore_config
            )
            session = boto3.Session(**session_kwargs)
        except ImportError:
            raise ImportError(
                "boto3 package not found, install with'pip install boto3'"
            )

        additional_kwargs = additional_kwargs or {}
        callback_manager = callback_manager or CallbackManager([])
        context_size = context_size or BEDROCK_FOUNDATION_LLMS[model]

        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            context_size=context_size,
            profile_name=profile_name,
            timeout=timeout,
            max_retries=max_retries,
            botocore_config=config,
            additional_kwargs=additional_kwargs,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region_name,
            botocore_session=botocore_session,
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
            guardrail_identifier=guardrail_identifier,
            guardrail_version=guardrail_version,
            trace=trace,
        )
        if provider_type is not None:
            self._provider = get_provider_by_type(provider_type)
        else:
            self._provider = get_provider(model)
        self.messages_to_prompt = (
            messages_to_prompt
            or self._provider.messages_to_prompt
            or self.messages_to_prompt
        )
        self.completion_to_prompt = (
            completion_to_prompt
            or self._provider.completion_to_prompt
            or self.completion_to_prompt
        )
        # Prior to general availability, custom boto3 wheel files were
        # distributed that used the bedrock service to invokeModel.
        # This check prevents any services still using those wheel files
        # from breaking
        if client is not None:
            self._client = client
        elif "bedrock-runtime" in session.get_available_services():
            self._client = session.client("bedrock-runtime", config=config)
        else:
            self._client = session.client("bedrock", config=config)

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "Bedrock_LLM"

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=self.context_size,
            num_output=self.max_tokens,
            is_chat_model=self.model in CHAT_ONLY_MODELS,
            model_name=self.model,
        )

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "temperature": self.temperature,
            self._provider.max_tokens_key: self.max_tokens,
        }
        if type(self._provider) is AnthropicProvider and self.system_prompt:
            base_kwargs["system"] = self.system_prompt
        return {
            **base_kwargs,
            **self.additional_kwargs,
        }

    def_get_all_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        return {
            **self._model_kwargs,
            **kwargs,
        }

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        if not formatted:
            prompt = self.completion_to_prompt(prompt)
        all_kwargs = self._get_all_kwargs(**kwargs)
        request_body = self._provider.get_request_body(prompt, all_kwargs)
        request_body_str = json.dumps(request_body)
        response = completion_with_retry(
            client=self._client,
            model=self.model,
            request_body=request_body_str,
            max_retries=self.max_retries,
            guardrail_identifier=self.guardrail_identifier,
            guardrail_version=self.guardrail_version,
            trace=self.trace,
            **all_kwargs,
        )
        response_body = response["body"].read()
        response_headers = response["ResponseMetadata"]["HTTPHeaders"]
        response_body = json.loads(response_body)
        return CompletionResponse(
            text=self._provider.get_text_from_response(response_body),
            raw=response_body,
            additional_kwargs=self._get_response_token_counts(response_headers),
        )

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        if self.model in BEDROCK_FOUNDATION_LLMS and self.model not in STREAMING_MODELS:
            raise ValueError(f"Model {self.model} does not support streaming")

        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        all_kwargs = self._get_all_kwargs(**kwargs)
        request_body = self._provider.get_request_body(prompt, all_kwargs)
        request_body_str = json.dumps(request_body)
        response = completion_with_retry(
            client=self._client,
            model=self.model,
            request_body=request_body_str,
            max_retries=self.max_retries,
            stream=True,
            guardrail_identifier=self.guardrail_identifier,
            guardrail_version=self.guardrail_version,
            trace=self.trace,
            **all_kwargs,
        )
        response_body = response["body"]
        response_headers = response["ResponseMetadata"]["HTTPHeaders"]

        defgen() -> CompletionResponseGen:
            content = ""
            for r in response_body:
                r = json.loads(r["chunk"]["bytes"])
                content_delta = self._provider.get_text_from_stream_response(r)
                content += content_delta
                yield CompletionResponse(
                    text=content,
                    delta=content_delta,
                    raw=r,
                    additional_kwargs=self._get_response_token_counts(response_headers),
                )

        return gen()

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        prompt = self.messages_to_prompt(messages)
        completion_response = self.complete(prompt, formatted=True, **kwargs)
        return completion_response_to_chat_response(completion_response)

    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        prompt = self.messages_to_prompt(messages)
        completion_response = self.stream_complete(prompt, formatted=True, **kwargs)
        return stream_completion_response_to_chat_response(completion_response)

    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
"""Chat asynchronously."""
        # TODO: do synchronous chat for now
        return self.chat(messages, **kwargs)

    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        raise NotImplementedError

    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        raise NotImplementedError

    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        raise NotImplementedError

    def_get_response_token_counts(self, headers: Any) -> dict:
"""Get the token usage reported by the response."""
        if not isinstance(headers, dict):
            return {}

        input_tokens = headers.get("x-amzn-bedrock-input-token-count", None)
        output_tokens = headers.get("x-amzn-bedrock-output-token-count", None)
        # NOTE: other model providers that use the OpenAI client may not report usage
        if (input_tokens and output_tokens) is None:
            return {}

        return {"prompt_tokens": input_tokens, "completion_tokens": output_tokens}

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/bedrock/#llama_index.llms.bedrock.Bedrock.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-bedrock/llama_index/llms/bedrock/base.py`  
| 
```
250
251
252
253
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "Bedrock_LLM"

```
 |  
| --- | --- |  
###  achat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/bedrock/#llama_index.llms.bedrock.Bedrock.achat "Permanent link")

```
achat(
    messages: Sequence[], **kwargs: 
) -> 

```

Chat asynchronously.
Source code in `llama-index-integrations/llms/llama-index-llms-bedrock/llama_index/llms/bedrock/base.py`  
| 
```
366
367
368
369
370
371
```
 | 
```
async defachat(
    self, messages: Sequence[ChatMessage], **kwargs: Any
) -> ChatResponse:
"""Chat asynchronously."""
    # TODO: do synchronous chat for now
    return self.chat(messages, **kwargs)

```
 |  
| --- | --- |  
##  completion_response_to_chat_response [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/bedrock/#llama_index.llms.bedrock.completion_response_to_chat_response "Permanent link")

```
completion_response_to_chat_response(
    completion_response: ,
) -> 

```

Convert a completion response to a chat response.
Source code in `llama-index-core/llama_index/core/base/llms/generic_utils.py`  
| 
```
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
```
 | 
```
defcompletion_response_to_chat_response(
    completion_response: CompletionResponse,
) -> ChatResponse:
"""Convert a completion response to a chat response."""
    return ChatResponse(
        message=ChatMessage(
            role=MessageRole.ASSISTANT,
            content=completion_response.text,
            additional_kwargs=completion_response.additional_kwargs,
        ),
        raw=completion_response.raw,
    )

```
 |  
| --- | --- |  
##  completion_with_retry [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/bedrock/#llama_index.llms.bedrock.completion_with_retry "Permanent link")

```
completion_with_retry(
    client: ,
    model: ,
    request_body: ,
    max_retries: ,
    stream:  = False,
    guardrail_identifier: Optional[] = None,
    guardrail_version: Optional[] = None,
    trace: Optional[] = None,
    **kwargs: 
) -> 

```

Use tenacity to retry the completion call.
Source code in `llama-index-integrations/llms/llama-index-llms-bedrock/llama_index/llms/bedrock/utils.py`  
| 
```
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
```
 | 
```
defcompletion_with_retry(
    client: Any,
    model: str,
    request_body: str,
    max_retries: int,
    stream: bool = False,
    guardrail_identifier: Optional[str] = None,
    guardrail_version: Optional[str] = None,
    trace: Optional[str] = None,
    **kwargs: Any,
) -> Any:
"""Use tenacity to retry the completion call."""
    retry_decorator = _create_retry_decorator(client=client, max_retries=max_retries)

    @retry_decorator
    def_completion_with_retry(**kwargs: Any) -> Any:
        if stream:
            if guardrail_identifier is None or guardrail_version is None:
                return client.invoke_model_with_response_stream(
                    modelId=model,
                    body=request_body,
                )
            else:
                return client.invoke_model_with_response_stream(
                    modelId=model,
                    body=request_body,
                    guardrailIdentifier=guardrail_identifier,
                    guardrailVersion=guardrail_version,
                    trace=trace,
                )
        else:
            if guardrail_identifier is None or guardrail_version is None:
                return client.invoke_model(modelId=model, body=request_body)
            else:
                return client.invoke_model(
                    modelId=model,
                    body=request_body,
                    guardrailIdentifier=guardrail_identifier,
                    guardrailVersion=guardrail_version,
                    trace=trace,
                )

    return _completion_with_retry(**kwargs)

```
 |  
| --- | --- |  
options: members: - Bedrock
