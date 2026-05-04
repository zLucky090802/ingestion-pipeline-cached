# Nvidia triton
##  NvidiaTriton [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/nvidia_triton/#llama_index.llms.nvidia_triton.NvidiaTriton "Permanent link")
Bases: 
Nvidia Triton LLM.
Nvidia's Triton is an inference server that provides API access to hosted LLM models. This connector allows for llama_index to remotely interact with a Triton inference server over GRPC to accelerate inference operations.
[Triton Inference Server Github](https://github.com/triton-inference-server/server)
Examples:
`pip install llama-index-llms-nvidia-triton`

```
fromllama_index.llms.nvidia_tritonimport NvidiaTriton

# Ensure a Triton server instance is running and provide the correct URL for your Triton server instance
triton_url = "localhost:8001"

# Instantiate the NvidiaTriton class
triton_client = NvidiaTriton()

# Call the complete method with a prompt
resp = triton_client.complete("The tallest mountain in North America is ")
print(resp)

```

Source code in `llama-index-integrations/llms/llama-index-llms-nvidia-triton/llama_index/llms/nvidia_triton/base.py`  
| 
```
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
```
 | 
```
classNvidiaTriton(LLM):
"""
    Nvidia Triton LLM.

    Nvidia's Triton is an inference server that provides API access to hosted LLM models. This connector allows for llama_index to remotely interact with a Triton inference server over GRPC to
    accelerate inference operations.

    [Triton Inference Server Github](https://github.com/triton-inference-server/server)

    Examples:
        `pip install llama-index-llms-nvidia-triton`

        ```python
        from llama_index.llms.nvidia_triton import NvidiaTriton

        # Ensure a Triton server instance is running and provide the correct URL for your Triton server instance
        triton_url = "localhost:8001"

        # Instantiate the NvidiaTriton class
        triton_client = NvidiaTriton()

        # Call the complete method with a prompt
        resp = triton_client.complete("The tallest mountain in North America is ")
        print(resp)
        ```

    """

    server_url: str = Field(
        default=DEFAULT_SERVER_URL,
        description="The URL of the Triton inference server to use.",
    )
    model_name: str = Field(
        default=DEFAULT_MODEL,
        description="The name of the Triton hosted model this client should use",
    )
    temperature: Optional[float] = Field(
        default=DEFAULT_TEMPERATURE, description="Temperature to use for sampling"
    )
    top_p: Optional[float] = Field(
        default=DEFAULT_TOP_P, description="The top-p value to use for sampling"
    )
    top_k: Optional[float] = Field(
        default=DEFAULT_TOP_K, description="The top k value to use for sampling"
    )
    tokens: Optional[int] = Field(
        default=DEFAULT_MAX_TOKENS,
        description="The maximum number of tokens to generate.",
    )
    beam_width: Optional[int] = Field(
        default=DEFAULT_BEAM_WIDTH, description="Last n number of tokens to penalize"
    )
    repetition_penalty: Optional[float] = Field(
        default=DEFAULT_REPTITION_PENALTY,
        description="Last n number of tokens to penalize",
    )
    length_penalty: Optional[float] = Field(
        default=DEFAULT_LENGTH_PENALTY,
        description="The penalty to apply repeated tokens",
    )
    max_retries: Optional[int] = Field(
        default=DEFAULT_MAX_RETRIES,
        description="Maximum number of attempts to retry Triton client invocation before erroring",
    )
    timeout: Optional[float] = Field(
        default=DEFAULT_TIMEOUT,
        description="Maximum time (seconds) allowed for a Triton client call before erroring",
    )
    reuse_client: Optional[bool] = Field(
        default=DEFAULT_REUSE_CLIENT,
        description="True for reusing the same client instance between invocations",
    )
    triton_load_model_call: Optional[bool] = Field(
        default=DEFAULT_TRITON_LOAD_MODEL,
        description="True if a Triton load model API call should be made before using the client",
    )

    _client: Optional[GrpcTritonClient] = PrivateAttr()

    def__init__(
        self,
        server_url: str = DEFAULT_SERVER_URL,
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        top_p: float = DEFAULT_TOP_P,
        top_k: float = DEFAULT_TOP_K,
        tokens: Optional[int] = DEFAULT_MAX_TOKENS,
        beam_width: int = DEFAULT_BEAM_WIDTH,
        repetition_penalty: float = DEFAULT_REPTITION_PENALTY,
        length_penalty: float = DEFAULT_LENGTH_PENALTY,
        max_retries: int = DEFAULT_MAX_RETRIES,
        timeout: float = DEFAULT_TIMEOUT,
        reuse_client: bool = DEFAULT_REUSE_CLIENT,
        triton_load_model_call: bool = DEFAULT_TRITON_LOAD_MODEL,
        callback_manager: Optional[CallbackManager] = None,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        additional_kwargs = additional_kwargs or {}

        super().__init__(
            server_url=server_url,
            model=model,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            tokens=tokens,
            beam_width=beam_width,
            repetition_penalty=repetition_penalty,
            length_penalty=length_penalty,
            max_retries=max_retries,
            timeout=timeout,
            reuse_client=reuse_client,
            triton_load_model_call=triton_load_model_call,
            callback_manager=callback_manager,
            additional_kwargs=additional_kwargs,
            **kwargs,
        )

        try:
            self._client = GrpcTritonClient(server_url)
        except ImportError as err:
            raise ImportError(
                "Could not import triton client python package. "
                "Please install it with `pip install tritonclient`."
            ) fromerr

    @property
    def_get_model_default_parameters(self) -> Dict[str, Any]:
        return {
            "tokens": self.tokens,
            "top_k": self.top_k,
            "top_p": self.top_p,
            "temperature": self.temperature,
            "repetition_penalty": self.repetition_penalty,
            "length_penalty": self.length_penalty,
            "beam_width": self.beam_width,
        }

    @property
    def_invocation_params(self, **kwargs: Any) -> Dict[str, Any]:
        return {**self._get_model_default_parameters, **kwargs}

    @property
    def_identifying_params(self) -> Dict[str, Any]:
"""Get all the identifying parameters."""
        return {
            "server_url": self.server_url,
            "model_name": self.model_name,
        }

    def_get_client(self) -> Any:
"""Create or reuse a Triton client connection."""
        if not self.reuse_client:
            return GrpcTritonClient(self.server_url)

        if self._client is None:
            self._client = GrpcTritonClient(self.server_url)
        return self._client

    @property
    defmetadata(self) -> LLMMetadata:
"""Gather and return metadata about the user Triton configured LLM model."""
        return LLMMetadata(
            model_name=self.model_name,
        )

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        chat_fn = completion_to_chat_decorator(self.complete)
        return chat_fn(messages, **kwargs)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        chat_stream_fn = stream_completion_to_chat_decorator(self.stream_complete)
        return chat_stream_fn(messages, **kwargs)

    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        fromtritonclient.utilsimport InferenceServerException

        client = self._get_client()

        invocation_params = self._get_model_default_parameters
        invocation_params.update(kwargs)
        invocation_params["prompt"] = [[prompt]]
        model_params = self._identifying_params
        model_params.update(kwargs)
        request_id = str(random.randint(1, 9999999))  # nosec

        if self.triton_load_model_call:
            client.load_model(model_params["model_name"])

        result_queue = client.request_streaming(
            model_params["model_name"], request_id, **invocation_params
        )
        response = ""
        for token in result_queue:
            if isinstance(token, InferenceServerException):
                client.stop_stream(model_params["model_name"], request_id)
                raise token
            response += token

        return CompletionResponse(
            text=response,
        )

    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        fromtritonclient.utilsimport InferenceServerException

        client = self._get_client()

        invocation_params = self._get_model_default_parameters
        invocation_params.update(kwargs)
        invocation_params["prompt"] = [[prompt]]
        model_params = self._identifying_params
        model_params.update(kwargs)
        request_id = str(random.randint(1, 9999999))  # nosec

        if self.triton_load_model_call:
            client.load_model(model_params["model_name"])

        result_queue = client.request_streaming(
            model_params["model_name"], request_id, **invocation_params
        )

        defgen() -> CompletionResponseGen:
            text = ""
            for token in result_queue:
                if isinstance(token, InferenceServerException):
                    client.stop_stream(model_params["model_name"], request_id)
                    raise token
                text += token
                yield CompletionResponse(text=text, delta=token)

        return gen()

    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        raise NotImplementedError

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

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/nvidia_triton/#llama_index.llms.nvidia_triton.NvidiaTriton.metadata "Permanent link")

```
metadata: 

```

Gather and return metadata about the user Triton configured LLM model.
options: members: - NvidiaTriton
