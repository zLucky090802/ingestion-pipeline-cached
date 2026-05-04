# Oci genai
##  OCIGenAI [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/oci_genai/#llama_index.llms.oci_genai.OCIGenAI "Permanent link")
Bases: `FunctionCallingLLM`
OCI large language models with function calling support.
Source code in `llama-index-integrations/llms/llama-index-llms-oci-genai/llama_index/llms/oci_genai/base.py`  
| 
```
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
```
 | 
```
classOCIGenAI(FunctionCallingLLM):
"""OCI large language models with function calling support."""

    model: str = Field(description="Id of the OCI Generative AI model to use.")
    temperature: float = Field(description="The temperature to use for sampling.")
    max_tokens: int = Field(description="The maximum number of tokens to generate.")
    context_size: int = Field("The maximum number of tokens available for input.")

    service_endpoint: Optional[str] = Field(
        default=None,
        description="service endpoint url.",
    )

    compartment_id: Optional[str] = Field(
        default=None,
        description="OCID of compartment.",
    )

    auth_type: Optional[str] = Field(
        description="Authentication type, can be: API_KEY, SECURITY_TOKEN, INSTANCE_PRINCIPAL, RESOURCE_PRINCIPAL. If not specified, API_KEY will be used",
        default="API_KEY",
    )

    auth_profile: Optional[str] = Field(
        description="The name of the profile in ~/.oci/config. If not specified , DEFAULT will be used",
        default="DEFAULT",
    )

    auth_file_location: Optional[str] = Field(
        description="Path to the config file. If not specified, ~/.oci/config will be used",
        default="~/.oci/config",
    )

    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional kwargs for the OCI Generative AI request.",
    )

    _client: Any = PrivateAttr()
    _provider: str = PrivateAttr()
    _serving_mode: str = PrivateAttr()
    _completion_generator: str = PrivateAttr()
    _chat_generator: str = PrivateAttr()

    def__init__(
        self,
        model: str,
        temperature: Optional[float] = DEFAULT_TEMPERATURE,
        max_tokens: Optional[int] = 512,
        context_size: Optional[int] = None,
        service_endpoint: Optional[str] = None,
        compartment_id: Optional[str] = None,
        auth_type: Optional[str] = "API_KEY",
        auth_profile: Optional[str] = "DEFAULT",
        auth_file_location: Optional[str] = "~/.oci/config",
        client: Optional[Any] = None,
        provider: Optional[str] = None,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
    ) -> None:
"""
        Initializes the OCIGenAI class.

        Args:
            model (str): The Id of the model to be used for generating embeddings, e.g., "meta.llama-2-70b-chat".

            temperature (Optional[float]): The temperature to use for sampling. Default specified in lama_index.core.constants.DEFAULT_TEMPERATURE.

            max_tokens (Optional[int]): The maximum number of tokens to generate. Default is 512.

            context_size (Optional[int]): The maximum number of tokens available for input. If not specified, the default context size for the model will be used.

            service_endpoint (str): service endpoint url, e.g., "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"

            compartment_id (str): OCID of the compartment.

            auth_type (Optional[str]): Authentication type, can be: API_KEY (default), SECURITY_TOKEN, INSTANCEAL, RESOURCE_PRINCIPAL. If not specified, API_KEY will be used

            auth_profile (Optional[str]): The name of the profile in ~/.oci/config. If not specified , DEFAULT will be used

            auth_file_location (Optional[str]): Path to the config file, If not specified, ~/.oci/config will be used.

            client (Optional[Any]): An optional OCI client object. If not provided, the client will be created using the
                                    provided service endpoint and authentifcation method.

            provider (Optional[str]): Provider name of the model. If not specified, the provider will be derived from the model name.

            additional_kwargs (Optional[Dict[str, Any]]): Additional kwargs for the LLM.

        """
        context_size = get_context_size(model, context_size)

        additional_kwargs = additional_kwargs or {}
        callback_manager = callback_manager or CallbackManager([])

        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            context_size=context_size,
            service_endpoint=service_endpoint,
            compartment_id=compartment_id,
            auth_type=auth_type,
            auth_profile=auth_profile,
            auth_file_location=auth_file_location,
            additional_kwargs=additional_kwargs,
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )

        self._client = client or create_client(
            auth_type, auth_profile, auth_file_location, service_endpoint
        )

        self._provider = get_provider(model, provider)

        self._serving_mode = get_serving_mode(model)

        self._completion_generator = get_completion_generator()

        self._chat_generator = get_chat_generator()

    @classmethod
    defclass_name(cls) -> str:
        return "OCIGenAI_LLM"

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=self.context_size,
            num_output=self.max_tokens,
            is_chat_model=self.model in CHAT_MODELS,
            model_name=self.model,
        )

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
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
        complete_fn = chat_to_completion_decorator(self.chat)
        return complete_fn(prompt, **kwargs)

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        stream_complete_fn = stream_chat_to_completion_decorator(self.stream_chat)
        return stream_complete_fn(prompt, **kwargs)

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        oci_params = self._provider.messages_to_oci_params(messages)
        oci_params["is_stream"] = False
        tools = kwargs.pop("tools", None)
        all_kwargs = self._get_all_kwargs(**kwargs)
        chat_params = {**all_kwargs, **oci_params}

        if tools:
            chat_params["tools"] = [
                self._provider.convert_to_oci_tool(tool) for tool in tools
            ]

        request = self._chat_generator(
            compartment_id=self.compartment_id,
            serving_mode=self._serving_mode,
            chat_request=self._provider.oci_chat_request(**chat_params),
        )

        response = self._client.chat(request)

        generation_info = self._provider.chat_generation_info(response)

        llm_output = {
            "model_id": response.data.model_id,
            "model_version": response.data.model_version,
            "request_id": response.request_id,
            "content-length": response.headers["content-length"],
        }

        return ChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT,
                content=self._provider.chat_response_to_text(response),
                additional_kwargs=generation_info,
            ),
            raw=response.__dict__,
        )

    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        oci_params = self._provider.messages_to_oci_params(messages)
        oci_params["is_stream"] = True
        tools = kwargs.pop("tools", None)
        all_kwargs = self._get_all_kwargs(**kwargs)
        chat_params = {**all_kwargs, **oci_params}
        if tools:
            chat_params["tools"] = [
                self._provider.convert_to_oci_tool(tool) for tool in tools
            ]

        request = self._chat_generator(
            compartment_id=self.compartment_id,
            serving_mode=self._serving_mode,
            chat_request=self._provider.oci_chat_request(**chat_params),
        )

        response = self._client.chat(request)

        defgen() -> ChatResponseGen:
            content = ""
            tool_calls_accumulated = []

            for event in response.data.events():
                content_delta = self._provider.chat_stream_to_text(
                    json.loads(event.data)
                )
                content += content_delta

                try:
                    event_data = json.loads(event.data)

                    tool_calls_data = None
                    for key in ["toolCalls", "tool_calls", "functionCalls"]:
                        if key in event_data:
                            tool_calls_data = event_data[key]
                            break

                    if tool_calls_data:
                        new_tool_calls = _format_oci_tool_calls(tool_calls_data)
                        for tool_call in new_tool_calls:
                            existing = next(
                                (
                                    t
                                    for t in tool_calls_accumulated
                                    if t["name"] == tool_call["name"]
                                ),
                                None,
                            )
                            if existing:
                                existing.update(tool_call)
                            else:
                                tool_calls_accumulated.append(tool_call)

                    generation_info = self._provider.chat_stream_generation_info(
                        event_data
                    )
                    if tool_calls_accumulated:
                        generation_info["tool_calls"] = tool_calls_accumulated

                    yield ChatResponse(
                        message=ChatMessage(
                            role=MessageRole.ASSISTANT,
                            content=content,
                            additional_kwargs=generation_info,
                        ),
                        delta=content_delta,
                        raw=event.__dict__,
                    )

                except json.JSONDecodeError:
                    yield ChatResponse(
                        message=ChatMessage(
                            role=MessageRole.ASSISTANT, content=content
                        ),
                        delta=content_delta,
                        raw=event.__dict__,
                    )

                except Exception as e:
                    print(f"Error processing stream chunk: {e}")
                    yield ChatResponse(
                        message=ChatMessage(
                            role=MessageRole.ASSISTANT, content=content
                        ),
                        delta=content_delta,
                        raw=event.__dict__,
                    )

        return gen()

    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        raise NotImplementedError("Async chat is not implemented yet.")

    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        raise NotImplementedError("Async complete is not implemented yet.")

    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        raise NotImplementedError("Async stream chat is not implemented yet.")

    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        raise NotImplementedError("Async stream complete is not implemented yet.")

    # Function tooling integration methods
    def_prepare_chat_with_tools(
        self,
        tools: Sequence["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        tool_required: bool = False,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        tool_specs = tools

        if isinstance(user_msg, str):
            user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)

        messages = chat_history or []
        if user_msg:
            messages.append(user_msg)

        oci_params = self._provider.messages_to_oci_params(messages)
        chat_params = self._get_all_kwargs(**kwargs)

        return {
            "messages": messages,
            "tools": tool_specs,
            **({"tool_choice": "REQUIRED"} if tool_required else {}),
            **oci_params,
            **chat_params,
        }

    def_validate_chat_with_tools_response(
        self,
        response: ChatResponse,
        tools: List["BaseTool"],
        allow_parallel_tool_calls: bool = False,
        **kwargs: Any,
    ) -> ChatResponse:
"""Validate the response from chat_with_tools."""
        if not allow_parallel_tool_calls:
            force_single_tool_call(response)
        return response

    defget_tool_calls_from_response(
        self,
        response: "ChatResponse",
        error_on_no_tool_call: bool = True,
        **kwargs: Any,
    ) -> List[ToolSelection]:
"""Predict and call the tool."""
        tool_calls = response.message.additional_kwargs.get("tool_calls", [])

        if len(tool_calls)  1:
            if error_on_no_tool_call:
                raise ValueError(
                    f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
                )
            else:
                return []

        tool_selections = []
        for tool_call in tool_calls:
            validate_tool_call(tool_call)
            argument_dict = (
                json.loads(tool_call["input"])
                if isinstance(tool_call["input"], str)
                else tool_call["input"]
            )

            tool_selections.append(
                ToolSelection(
                    tool_id=tool_call["toolUseId"],
                    tool_name=tool_call["name"],
                    tool_kwargs=argument_dict,
                )
            )

        return tool_selections

```
 |  
| --- | --- |  
###  get_tool_calls_from_response [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/oci_genai/#llama_index.llms.oci_genai.OCIGenAI.get_tool_calls_from_response "Permanent link")

```
get_tool_calls_from_response(
    response: ,
    error_on_no_tool_call:  = True,
    **kwargs: 
) -> [ToolSelection]

```

Predict and call the tool.
Source code in `llama-index-integrations/llms/llama-index-llms-oci-genai/llama_index/llms/oci_genai/base.py`  
| 
```
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
```
 | 
```
defget_tool_calls_from_response(
    self,
    response: "ChatResponse",
    error_on_no_tool_call: bool = True,
    **kwargs: Any,
) -> List[ToolSelection]:
"""Predict and call the tool."""
    tool_calls = response.message.additional_kwargs.get("tool_calls", [])

    if len(tool_calls)  1:
        if error_on_no_tool_call:
            raise ValueError(
                f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
            )
        else:
            return []

    tool_selections = []
    for tool_call in tool_calls:
        validate_tool_call(tool_call)
        argument_dict = (
            json.loads(tool_call["input"])
            if isinstance(tool_call["input"], str)
            else tool_call["input"]
        )

        tool_selections.append(
            ToolSelection(
                tool_id=tool_call["toolUseId"],
                tool_name=tool_call["name"],
                tool_kwargs=argument_dict,
            )
        )

    return tool_selections

```
 |  
| --- | --- |  
options: members: - OCIGenAI
