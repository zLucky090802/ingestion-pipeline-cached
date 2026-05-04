# Sagemaker endpoint
##  SageMakerLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/sagemaker_endpoint/#llama_index.llms.sagemaker_endpoint.SageMakerLLM "Permanent link")
Bases: 
SageMaker LLM.
Examples:
`pip install llama-index-llms-sagemaker-endpoint`

```
fromllama_index.llms.sagemakerimport SageMakerLLM

# hooks for HuggingFaceH4/zephyr-7b-beta
# different models may require different formatting
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

# Additional setup for SageMakerLLM class
model_name = "HuggingFaceH4/zephyr-7b-beta"
api_key = "your_api_key"
region = "your_region"

llm = SageMakerLLM(
    model_name=model_name,
    api_key=api_key,
    region=region,
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
)

```

Source code in `llama-index-integrations/llms/llama-index-llms-sagemaker-endpoint/llama_index/llms/sagemaker_endpoint/base.py`  
| 
```
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
```
 | 
```
classSageMakerLLM(LLM):
r"""
    SageMaker LLM.

    Examples:
        `pip install llama-index-llms-sagemaker-endpoint`

        ```python
        from llama_index.llms.sagemaker import SageMakerLLM

        # hooks for HuggingFaceH4/zephyr-7b-beta
        # different models may require different formatting
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

        # Additional setup for SageMakerLLM class
        model_name = "HuggingFaceH4/zephyr-7b-beta"
        api_key = "your_api_key"
        region = "your_region"

        llm = SageMakerLLM(
            model_name=model_name,
            api_key=api_key,
            region=region,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,

        ```

    """

    endpoint_name: str = Field(description="SageMaker LLM endpoint name")
    endpoint_kwargs: Dict[str, Any] = Field(
        default={},
        description="Additional kwargs for the invoke_endpoint request.",
    )
    model_kwargs: Dict[str, Any] = Field(
        default={},
        description="kwargs to pass to the model.",
    )
    content_handler: BaseIOHandler = Field(
        default=DEFAULT_IO_HANDLER,
        description="used to serialize input, deserialize output, and remove a prefix.",
    )

    profile_name: Optional[str] = Field(
        description="The name of aws profile to use. If not given, then the default profile is used."
    )
    aws_access_key_id: Optional[str] = Field(description="AWS Access Key ID to use")
    aws_secret_access_key: Optional[str] = Field(
        description="AWS Secret Access Key to use"
    )
    aws_session_token: Optional[str] = Field(description="AWS Session Token to use")
    region_name: Optional[str] = Field(
        description="AWS region name to use. Uses region configured in AWS CLI if not passed"
    )
    max_retries: Optional[int] = Field(
        default=3,
        description="The maximum number of API retries.",
        ge=0,
    )
    timeout: Optional[float] = Field(
        default=60.0,
        description="The timeout, in seconds, for API requests.",
        ge=0,
    )
    _client: Any = PrivateAttr()
    _completion_to_prompt: Callable[[str, Optional[str]], str] = PrivateAttr()

    def__init__(
        self,
        endpoint_name: str,
        endpoint_kwargs: Optional[Dict[str, Any]] = {},
        model_kwargs: Optional[Dict[str, Any]] = {},
        content_handler: Optional[BaseIOHandler] = DEFAULT_IO_HANDLER,
        profile_name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        aws_region_name: Optional[str] = None,
        max_retries: Optional[int] = 3,
        timeout: Optional[float] = 60.0,
        temperature: Optional[float] = 0.5,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[
            Callable[[Sequence[ChatMessage]], str]
        ] = LLAMA_MESSAGES_TO_PROMPT,
        completion_to_prompt: Callable[
            [str, Optional[str]], str
        ] = LLAMA_COMPLETION_TO_PROMPT,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        **kwargs: Any,
    ) -> None:
        if not endpoint_name:
            raise ValueError(
                "Missing required argument:`endpoint_name`"
                " Please specify the endpoint_name"
            )
        endpoint_kwargs = endpoint_kwargs or {}
        model_kwargs = model_kwargs or {}
        model_kwargs["temperature"] = temperature
        content_handler = content_handler
        callback_manager = callback_manager or CallbackManager([])

        region_name = kwargs.pop("region_name", None)

        if region_name is not None:
            warnings.warn(
                "Kwarg `region_name` is deprecated and will be removed in a future version. "
                "Please use `aws_region_name` instead.",
                DeprecationWarning,
            )
            if not aws_region_name:
                aws_region_name = region_name

        super().__init__(
            endpoint_name=endpoint_name,
            endpoint_kwargs=endpoint_kwargs,
            model_kwargs=model_kwargs,
            content_handler=content_handler,
            profile_name=profile_name,
            region_name=aws_region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            timeout=timeout,
            max_retries=max_retries,
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )

        self._completion_to_prompt = completion_to_prompt

        self._client = get_aws_service_client(
            service_name="sagemaker-runtime",
            profile_name=profile_name,
            region_name=aws_region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            max_retries=max_retries,
            timeout=timeout,
        )

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        model_kwargs = {**self.model_kwargs, **kwargs}
        if not formatted:
            prompt = self._completion_to_prompt(prompt, self.system_prompt)

        request_body = self.content_handler.serialize_input(prompt, model_kwargs)
        response = self._client.invoke_endpoint(
            EndpointName=self.endpoint_name,
            Body=request_body,
            ContentType=self.content_handler.content_type,
            Accept=self.content_handler.accept,
            **self.endpoint_kwargs,
        )

        response["Body"] = self.content_handler.deserialize_output(response["Body"])
        text = self.content_handler.remove_prefix(response["Body"], prompt)

        return CompletionResponse(
            text=text,
            raw=response,
            additional_kwargs={
                "model_kwargs": model_kwargs,
                "endpoint_kwargs": self.endpoint_kwargs,
            },
        )

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        model_kwargs = {**self.model_kwargs, **kwargs}
        if not formatted:
            prompt = self._completion_to_prompt(prompt, self.system_prompt)

        request_body = self.content_handler.serialize_input(prompt, model_kwargs)

        defgen() -> CompletionResponseGen:
            raw_text = ""
            prev_clean_text = ""
            for response in self._client.invoke_endpoint_with_response_stream(
                EndpointName=self.endpoint_name,
                Body=request_body,
                ContentType=self.content_handler.content_type,
                Accept=self.content_handler.accept,
                **self.endpoint_kwargs,
            )["Body"]:
                delta = self.content_handler.deserialize_streaming_output(
                    response["PayloadPart"]["Bytes"]
                )
                raw_text += delta
                clean_text = self.content_handler.remove_prefix(raw_text, prompt)
                delta = clean_text[len(prev_clean_text) :]
                prev_clean_text = clean_text

                yield CompletionResponse(text=clean_text, delta=delta, raw=response)

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
        completion_response_gen = self.stream_complete(prompt, formatted=True, **kwargs)
        return stream_completion_response_to_chat_response(completion_response_gen)

    @llm_chat_callback()
    async defachat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
        raise NotImplementedError

    @llm_chat_callback()
    async defastream_chat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponseAsyncGen:
        raise NotImplementedError

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        raise NotImplementedError

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        raise NotImplementedError

    @classmethod
    defclass_name(cls) -> str:
        return "SageMakerLLM"

    @property
    defmetadata(self) -> LLMMetadata:
"""LLM metadata."""
        return LLMMetadata(
            model_name=self.endpoint_name,
        )

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/sagemaker_endpoint/#llama_index.llms.sagemaker_endpoint.SageMakerLLM.metadata "Permanent link")

```
metadata: 

```

LLM metadata.
options: members: - SageMakerLLM
