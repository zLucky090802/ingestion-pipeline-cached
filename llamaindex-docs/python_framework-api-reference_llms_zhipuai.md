# Zhipuai
##  ZhipuAI [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/zhipuai/#llama_index.llms.zhipuai.ZhipuAI "Permanent link")
Bases: `FunctionCallingLLM`
ZhipuAI LLM.
Visit https://open.bigmodel.cn to get more information about ZhipuAI.
Examples:
`pip install llama-index-llms-zhipuai`

```
fromllama_index.llms.zhipuaiimport ZhipuAI

llm = ZhipuAI(model="glm-4", api_key="YOUR API KEY")

response = llm.complete("who are you?")
print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-zhipuai/llama_index/llms/zhipuai/base.py`  
| 
```
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
classZhipuAI(FunctionCallingLLM):
"""
    ZhipuAI LLM.

    Visit https://open.bigmodel.cn to get more information about ZhipuAI.

    Examples:
        `pip install llama-index-llms-zhipuai`

        ```python
        from llama_index.llms.zhipuai import ZhipuAI

        llm = ZhipuAI(model="glm-4", api_key="YOUR API KEY")

        response = llm.complete("who are you?")
        print(response)
        ```

    """

    model: str = Field(description="The ZhipuAI model to use.")
    api_key: Optional[str] = Field(
        default=None,
        description="The API key to use for the ZhipuAI API.",
    )
    temperature: float = Field(
        default=0.95,
        description="The temperature to use for sampling.",
        ge=0.0,
        le=1.0,
    )
    max_tokens: int = Field(
        default=1024,
        description="The maximum number of tokens for model output.",
        gt=0,
        le=4096,
    )
    timeout: float = Field(
        default=DEFAULT_REQUEST_TIMEOUT,
        description="The timeout for making http request to ZhipuAI API server",
    )
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the ZhipuAI API."
    )
    _client: Optional[ZhipuAIClient] = PrivateAttr()

    def__init__(
        self,
        model: str,
        api_key: str,
        temperature: float = 0.95,
        max_tokens: int = 1024,
        timeout: float = DEFAULT_REQUEST_TIMEOUT,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        additional_kwargs = additional_kwargs or {}
        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
            additional_kwargs=additional_kwargs,
            **kwargs,
        )

        self._client = ZhipuAIClient(api_key=api_key)

    @classmethod
    defclass_name(cls) -> str:
        return "ZhipuAI"

    @property
    defmetadata(self) -> LLMMetadata:
"""LLM metadata."""
        return LLMMetadata(
            context_window=glm_model_to_context_size(self.model),
            num_output=DEFAULT_NUM_OUTPUTS,
            model_name=self.model,
            is_chat_model=True,
            is_function_calling_model=is_function_calling_model(self.model),
        )

    @property
    defmodel_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        return {
            **base_kwargs,
            **self.additional_kwargs,
        }

    def_convert_to_llm_messages(self, messages: Sequence[ChatMessage]) -> List:
        return [
            {
                "role": message.role.value,
                "content": message.content or "",
            }
            for message in messages
        ]

    def_prepare_chat_with_tools(
        self,
        tools: List["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        tool_required: bool = False,  # unsupported, docs say for tool_choice, "currently only supports auto."
        **kwargs: Any,
    ) -> Dict[str, Any]:
        tool_specs = [
            tool.metadata.to_openai_tool(skip_length_check=True) for tool in tools
        ]

        if isinstance(user_msg, str):
            user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)

        messages = chat_history or []
        if user_msg:
            messages.append(user_msg)

        return {
            "messages": messages,
            "tools": tool_specs or None,
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
            return []

        tool_selections = []
        for tool_call in tool_calls:
            tool_selections.append(
                ToolSelection(
                    tool_id=tool_call.id,
                    tool_name=tool_call.function.name,
                    tool_kwargs=json.loads(tool_call.function.arguments),
                )
            )

        return tool_selections

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        messages_dict = self._convert_to_llm_messages(messages)
        raw_response = self._client.chat.completions.create(
            model=self.model,
            messages=messages_dict,
            stream=False,
            tools=kwargs.get("tools"),
            tool_choice=kwargs.get("tool_choice"),
            stop=kwargs.get("stop"),
            timeout=self.timeout,
            extra_body=self.model_kwargs,
        )
        tool_calls = raw_response.choices[0].message.tool_calls or []
        return ChatResponse(
            message=ChatMessage(
                content=raw_response.choices[0].message.content,
                role=raw_response.choices[0].message.role,
                additional_kwargs={"tool_calls": tool_calls},
            ),
            raw=raw_response,
        )

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        messages_dict = self._convert_to_llm_messages(messages)
        raw_response = self._client.chat.asyncCompletions.create(
            model=self.model,
            messages=messages_dict,
            tools=kwargs.get("tools"),
            tool_choice=kwargs.get("tool_choice"),
            stop=kwargs.get("stop"),
            timeout=self.timeout,
            extra_body=self.model_kwargs,
        )
        task_id = raw_response.id
        task_status = raw_response.task_status
        get_count = 0
        while task_status not in [SUCCESS, FAILED] and get_count  self.timeout:
            task_result = self._client.chat.asyncCompletions.retrieve_completion_result(
                task_id
            )
            raw_response = task_result
            task_status = raw_response.task_status
            get_count += 1
            await asyncio.sleep(1)
        tool_calls = raw_response.choices[0].message.tool_calls or []
        return ChatResponse(
            message=ChatMessage(
                content=raw_response.choices[0].message.content,
                role=raw_response.choices[0].message.role,
                additional_kwargs={"tool_calls": tool_calls},
            ),
            raw=raw_response,
        )

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        messages_dict = self._convert_to_llm_messages(messages)

        defgen() -> ChatResponseGen:
            raw_response = self._client.chat.completions.create(
                model=self.model,
                messages=messages_dict,
                stream=True,
                tools=kwargs.get("tools"),
                tool_choice=kwargs.get("tool_choice"),
                stop=kwargs.get("stop"),
                timeout=self.timeout,
                extra_body=self.model_kwargs,
            )
            response_txt = ""
            for chunk in raw_response:
                if chunk.choices[0].delta.content is None:
                    continue
                response_txt += chunk.choices[0].delta.content
                tool_calls = chunk.choices[0].delta.tool_calls
                yield ChatResponse(
                    message=ChatMessage(
                        content=response_txt,
                        role=chunk.choices[0].delta.role,
                        additional_kwargs={"tool_calls": tool_calls},
                    ),
                    delta=chunk.choices[0].delta.content,
                    raw=chunk,
                )

        return gen()

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        messages_dict = self._convert_to_llm_messages(messages)

        async defgen() -> ChatResponseAsyncGen:
            # TODO async interfaces don't support streaming
            # needs to find a more suitable implementation method
            raw_response = self._client.chat.completions.create(
                model=self.model,
                messages=messages_dict,
                stream=True,
                tools=kwargs.get("tools"),
                tool_choice=kwargs.get("tool_choice"),
                stop=kwargs.get("stop"),
                timeout=self.timeout,
                extra_body=self.model_kwargs,
            )
            response_txt = ""
            while True:
                chunk = await asyncio.to_thread(async_llm_generate, raw_response)
                if not chunk:
                    break
                if chunk.choices[0].delta.content is None:
                    continue
                response_txt += chunk.choices[0].delta.content
                tool_calls = chunk.choices[0].delta.tool_calls
                yield ChatResponse(
                    message=ChatMessage(
                        content=response_txt,
                        role=chunk.choices[0].delta.role,
                        additional_kwargs={"tool_calls": tool_calls},
                    ),
                    delta=chunk.choices[0].delta.content,
                    raw=chunk,
                )

        return gen()

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        return chat_to_completion_decorator(self.chat)(prompt, **kwargs)

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        return await achat_to_completion_decorator(self.achat)(prompt, **kwargs)

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        return stream_chat_to_completion_decorator(self.stream_chat)(prompt, **kwargs)

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        return await astream_chat_to_completion_decorator(self.astream_chat)(
            prompt, **kwargs
        )

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/zhipuai/#llama_index.llms.zhipuai.ZhipuAI.metadata "Permanent link")

```
metadata: 

```

LLM metadata.
###  get_tool_calls_from_response [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/zhipuai/#llama_index.llms.zhipuai.ZhipuAI.get_tool_calls_from_response "Permanent link")

```
get_tool_calls_from_response(
    response: ,
    error_on_no_tool_call:  = True,
    **kwargs: 
) -> []

```

Predict and call the tool.
Source code in `llama-index-integrations/llms/llama-index-llms-zhipuai/llama_index/llms/zhipuai/base.py`  
| 
```
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
        return []

    tool_selections = []
    for tool_call in tool_calls:
        tool_selections.append(
            ToolSelection(
                tool_id=tool_call.id,
                tool_name=tool_call.function.name,
                tool_kwargs=json.loads(tool_call.function.arguments),
            )
        )

    return tool_selections

```
 |  
| --- | --- |  
options: members: - ZhipuAI
