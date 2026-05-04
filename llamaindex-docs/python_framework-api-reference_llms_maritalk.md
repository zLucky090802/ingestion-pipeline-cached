# Maritalk
##  Maritalk [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/maritalk/#llama_index.llms.maritalk.Maritalk "Permanent link")
Bases: 
Maritalk LLM.
Examples:
`pip install llama-index-llms-maritalk`

```
fromllama_index.core.llmsimport ChatMessage
fromllama_index.llms.maritalkimport Maritalk

# To customize your API key, do this
# otherwise it will lookup MARITALK_API_KEY from your env variable
# llm = Maritalk(api_key="<your_maritalk_api_key>")

llm = Maritalk()

# Call chat with a list of messages
messages = [
    ChatMessage(
        role="system",
        content="You are an assistant specialized in suggesting pet names. Given the animal, you must suggest 4 names.",
    ),
    ChatMessage(role="user", content="I have a dog."),
]

response = llm.chat(messages)
print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-maritalk/llama_index/llms/maritalk/base.py`  
| 
```
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
```
 | 
```
classMaritalk(LLM):
"""
    Maritalk LLM.

    Examples:
        `pip install llama-index-llms-maritalk`

        ```python
        from llama_index.core.llms import ChatMessage
        from llama_index.llms.maritalk import Maritalk

        # To customize your API key, do this
        # otherwise it will lookup MARITALK_API_KEY from your env variable
        # llm = Maritalk(api_key="<your_maritalk_api_key>")

        llm = Maritalk()

        # Call chat with a list of messages
        messages = [
            ChatMessage(
                role="system",
                content="You are an assistant specialized in suggesting pet names. Given the animal, you must suggest 4 names.",

            ChatMessage(role="user", content="I have a dog."),


        response = llm.chat(messages)
        print(response)
        ```

    """

    api_key: str = Field(
        default=None,
        description="Your MariTalk API key.",
    )

    model: str = Field(
        default="sabia-2-medium",
        description="Chose one of the available models:\n"
        "- `sabia-2-medium`\n"
        "- `sabia-2-small`\n"
        "- `maritalk-2024-01-08`",
    )

    temperature: float = Field(
        default=0.7,
        gt=0.0,
        lt=1.0,
        description="Run inference with this temperature. Must be in the"
        "closed interval [0.0, 1.0].",
    )

    max_tokens: int = Field(
        default=512,
        gt=0,
        description="The maximum number of tokens togenerate in the reply.",
    )

    do_sample: bool = Field(
        default=True,
        description="Whether or not to use sampling; use `True` to enable.",
    )

    top_p: float = Field(
        default=0.95,
        gt=0.0,
        lt=1.0,
        description="Nucleus sampling parameter controlling the size of"
        " the probability mass considered for sampling.",
    )

    _endpoint: str = PrivateAttr("https://chat.maritaca.ai/api/chat/inference")

    def__init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # If an API key is not provided during instantiation,
        # fall back to the MARITALK_API_KEY environment variable
        self.api_key = self.api_key or os.getenv("MARITALK_API_KEY")
        if not self.api_key:
            raise ValueError(
                "An API key must be provided or set in the "
                "'MARITALK_API_KEY' environment variable."
            )

    @classmethod
    defclass_name(cls) -> str:
        return "Maritalk"

    defparse_messages_for_model(
        self, messages: Sequence[ChatMessage]
    ) -> List[Dict[str, Union[str, List[Union[str, Dict[Any, Any]]]]]]:
"""
        Parses messages from LlamaIndex's format to the format expected by
        the MariTalk API.

        Parameters
        ----------
            messages (Sequence[ChatMessage]): A list of messages in LlamaIndex
            format to be parsed.

        Returns
        -------
            A list of messages formatted for the MariTalk API.

        """
        formatted_messages = []

        for message in messages:
            if message.role.value == MessageRole.USER:
                role = "user"
            elif message.role.value == MessageRole.ASSISTANT:
                role = "assistant"
            elif message.role.value == MessageRole.SYSTEM:
                role = "system"

            formatted_messages.append({"role": role, "content": message.content})
        return formatted_messages

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            model_name="maritalk",
            context_window=self.max_tokens,
            is_chat_model=True,
        )

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        # Prepare the data payload for the Maritalk API
        formatted_messages = self.parse_messages_for_model(messages)

        data = {
            "model": self.model,
            "messages": formatted_messages,
            "do_sample": self.do_sample,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            **kwargs,
        }

        headers = {"authorization": f"Key {self.api_key}"}

        response = requests.post(self._endpoint, json=data, headers=headers)

        if response.ok:
            answer = response.json().get("answer", "No answer found")
            return ChatResponse(
                message=ChatMessage(role=MessageRole.ASSISTANT, content=answer),
                raw=response.json(),
            )
        else:
            raise MaritalkHTTPError(response)

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        complete_fn = chat_to_completion_decorator(self.chat)
        return complete_fn(prompt, **kwargs)

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        try:
            importhttpx

            # Prepare the data payload for the Maritalk API
            formatted_messages = self.parse_messages_for_model(messages)

            data = {
                "model": self.model,
                "messages": formatted_messages,
                "do_sample": self.do_sample,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
                **kwargs,
            }

            headers = {"authorization": f"Key {self.api_key}"}

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self._endpoint, json=data, headers=headers, timeout=None
                )

            if response.status_code == 200:
                answer = response.json().get("answer", "No answer found")
                return ChatResponse(
                    message=ChatMessage(role=MessageRole.ASSISTANT, content=answer),
                    raw=response.json(),
                )
            else:
                raise MaritalkHTTPError(response)

        except ImportError:
            raise ImportError(
                "Could not import httpx python package. "
                "Please install it with `pip install httpx`."
            )

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        acomplete_fn = achat_to_completion_decorator(self.achat)
        return await acomplete_fn(prompt, **kwargs)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        # Prepare the data payload for the Maritalk API
        formatted_messages = self.parse_messages_for_model(messages)

        data = {
            "model": self.model,
            "messages": formatted_messages,
            "do_sample": self.do_sample,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": True,
            **kwargs,
        }

        headers = {"authorization": f"Key {self.api_key}"}

        defgen() -> ChatResponseGen:
            response = requests.post(
                self._endpoint, json=data, headers=headers, stream=True
            )
            if response.ok:
                content = ""
                for line in response.iter_lines():
                    if line.startswith(b"data: "):
                        response_data = line.replace(b"data: ", b"").decode("utf-8")
                        if response_data:
                            parsed_data = json.loads(response_data)
                            if "text" in parsed_data:
                                content_delta = parsed_data["text"]
                                content += content_delta
                                yield ChatResponse(
                                    message=ChatMessage(
                                        role=MessageRole.ASSISTANT, content=content
                                    ),
                                    delta=content_delta,
                                    raw=parsed_data,
                                )
            else:
                raise MaritalkHTTPError(response)

        return gen()

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        stream_complete_fn = stream_chat_to_completion_decorator(self.stream_chat)
        return stream_complete_fn(prompt, **kwargs)

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        try:
            importhttpx

            # Prepare the data payload for the Maritalk API
            formatted_messages = self.parse_messages_for_model(messages)

            data = {
                "model": self.model,
                "messages": formatted_messages,
                "do_sample": self.do_sample,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "stream": True,
                **kwargs,
            }

            headers = {"authorization": f"Key {self.api_key}"}

            async defgen() -> ChatResponseAsyncGen:
                async with httpx.AsyncClient() as client:
                    async with client.stream(
                        "POST",
                        self._endpoint,
                        data=json.dumps(data),
                        headers=headers,
                        timeout=None,
                    ) as response:
                        if response.status_code == 200:
                            content = ""
                            async for line in response.aiter_lines():
                                if line.startswith("data: "):
                                    response_data = line.replace("data: ", "")
                                    if response_data:
                                        parsed_data = json.loads(response_data)
                                        if "text" in parsed_data:
                                            content_delta = parsed_data["text"]
                                            content += content_delta
                                            yield ChatResponse(
                                                message=ChatMessage(
                                                    role=MessageRole.ASSISTANT,
                                                    content=content,
                                                ),
                                                delta=content_delta,
                                                raw=parsed_data,
                                            )
                        else:
                            raise MaritalkHTTPError(response)

            return gen()

        except ImportError:
            raise ImportError(
                "Could not import httpx python package. "
                "Please install it with `pip install httpx`."
            )

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        astream_complete_fn = astream_chat_to_completion_decorator(self.astream_chat)
        return await astream_complete_fn(prompt, **kwargs)

```
 |  
| --- | --- |  
###  parse_messages_for_model [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/maritalk/#llama_index.llms.maritalk.Maritalk.parse_messages_for_model "Permanent link")

```
parse_messages_for_model(
    messages: Sequence[],
) -> [
    [, Union[, [Union[, [, ]]]]]
]

```

Parses messages from LlamaIndex's format to the format expected by the MariTalk API.
##### Parameters[#](https://developers.llamaindex.ai/python/framework-api-reference/llms/maritalk/#llama_index.llms.maritalk.Maritalk.parse_messages_for_model--parameters "Permanent link")

```
messages (Sequence[ChatMessage]): A list of messages in LlamaIndex
format to be parsed.

```

##### Returns[#](https://developers.llamaindex.ai/python/framework-api-reference/llms/maritalk/#llama_index.llms.maritalk.Maritalk.parse_messages_for_model--returns "Permanent link")

```
A list of messages formatted for the MariTalk API.

```
Source code in `llama-index-integrations/llms/llama-index-llms-maritalk/llama_index/llms/maritalk/base.py`  
| 
```
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
```
 | 
```
defparse_messages_for_model(
    self, messages: Sequence[ChatMessage]
) -> List[Dict[str, Union[str, List[Union[str, Dict[Any, Any]]]]]]:
"""
    Parses messages from LlamaIndex's format to the format expected by
    the MariTalk API.

    Parameters
    ----------
        messages (Sequence[ChatMessage]): A list of messages in LlamaIndex
        format to be parsed.

    Returns
    -------
        A list of messages formatted for the MariTalk API.

    """
    formatted_messages = []

    for message in messages:
        if message.role.value == MessageRole.USER:
            role = "user"
        elif message.role.value == MessageRole.ASSISTANT:
            role = "assistant"
        elif message.role.value == MessageRole.SYSTEM:
            role = "system"

        formatted_messages.append({"role": role, "content": message.content})
    return formatted_messages

```
 |  
| --- | --- |  
options: members: - Maritalk
