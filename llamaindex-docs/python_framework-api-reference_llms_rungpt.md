# Rungpt
##  RunGptLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/rungpt/#llama_index.llms.rungpt.RunGptLLM "Permanent link")
Bases: 
RunGPT LLM.
The opengpt of Jina AI models.
Examples:
`pip install llama-index-llms-rungpt`

```
fromllama_index.llms.rungptimport RunGptLLM

llm = RunGptLLM(model="rungpt", endpoint="0.0.0.0:51002")

response = llm.complete("What public transportation might be available in a city?")
print(str(response))

```

Source code in `llama-index-integrations/llms/llama-index-llms-rungpt/llama_index/llms/rungpt/base.py`  
| 
```
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
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
333
334
335
336
```
 | 
```
classRunGptLLM(LLM):
"""
    RunGPT LLM.

    The opengpt of Jina AI models.

    Examples:
        `pip install llama-index-llms-rungpt`

        ```python
        from llama_index.llms.rungpt import RunGptLLM

        llm = RunGptLLM(model="rungpt", endpoint="0.0.0.0:51002")

        response = llm.complete("What public transportation might be available in a city?")
        print(str(response))
        ```

    """

    model: Optional[str] = Field(
        default=DEFAULT_RUNGPT_MODEL, description="The rungpt model to use."
    )
    endpoint: str = Field(description="The endpoint of serving address.")
    temperature: float = Field(
        default=DEFAULT_RUNGPT_TEMP,
        description="The temperature to use for sampling.",
        ge=0.0,
        le=1.0,
    )
    max_tokens: int = Field(
        default=DEFAULT_NUM_OUTPUTS,
        description="Max tokens model generates.",
        gt=0,
    )
    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description="The maximum number of context tokens for the model.",
        gt=0,
    )
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the Replicate API."
    )
    base_url: str = Field(
        description="The address of your target model served by rungpt."
    )

    def__init__(
        self,
        model: Optional[str] = DEFAULT_RUNGPT_MODEL,
        endpoint: str = "0.0.0.0:51002",
        temperature: float = DEFAULT_RUNGPT_TEMP,
        max_tokens: Optional[int] = DEFAULT_NUM_OUTPUTS,
        context_window: int = DEFAULT_CONTEXT_WINDOW,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
    ):
        if endpoint.startswith("http://"):
            base_url = endpoint
        else:
            base_url = "http://" + endpoint
        super().__init__(
            model=model,
            endpoint=endpoint,
            temperature=temperature,
            max_tokens=max_tokens,
            context_window=context_window,
            additional_kwargs=additional_kwargs or {},
            callback_manager=callback_manager or CallbackManager([]),
            base_url=base_url,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "RunGptLLM"

    @property
    defmetadata(self) -> LLMMetadata:
"""LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.max_tokens,
            model_name=self._model,
        )

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        try:
            importrequests
        except ImportError:
            raise ImportError(
                "Could not import requests library."
                "Please install requests with `pip install requests`"
            )
        response_gpt = requests.post(
            self.base_url + "/generate",
            json=self._request_pack("complete", prompt, **kwargs),
            stream=False,
        ).json()

        return CompletionResponse(
            text=response_gpt["choices"][0]["text"],
            additional_kwargs=response_gpt["usage"],
            raw=response_gpt,
        )

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        try:
            importrequests
        except ImportError:
            raise ImportError(
                "Could not import requests library."
                "Please install requests with `pip install requests`"
            )
        response_gpt = requests.post(
            self.base_url + "/generate_stream",
            json=self._request_pack("complete", prompt, **kwargs),
            stream=True,
        )
        try:
            importsseclient
        except ImportError:
            raise ImportError(
                "Could not import sseclient-py library."
                "Please install requests with `pip install sseclient-py`"
            )
        client = sseclient.SSEClient(response_gpt)
        response_iter = client.events()

        defgen() -> CompletionResponseGen:
            text = ""
            for item in response_iter:
                item_dict = dict(item.data)
                delta = item_dict["choices"][0]["text"]
                additional_kwargs = item_dict["usage"]
                text = text + self._space_handler(delta)
                yield CompletionResponse(
                    text=text,
                    delta=delta,
                    raw=item_dict,
                    additional_kwargs=additional_kwargs,
                )

        return gen()

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        message_list = self._message_wrapper(messages)
        try:
            importrequests
        except ImportError:
            raise ImportError(
                "Could not import requests library."
                "Please install requests with `pip install requests`"
            )
        response_gpt = requests.post(
            self.base_url + "/chat",
            json=self._request_pack("chat", message_list, **kwargs),
            stream=False,
        ).json()
        chat_message, _ = self._message_unpacker(response_gpt)
        return ChatResponse(message=chat_message, raw=response_gpt)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        message_list = self._message_wrapper(messages)
        try:
            importrequests
        except ImportError:
            raise ImportError(
                "Could not import requests library."
                "Please install requests with `pip install requests`"
            )
        response_gpt = requests.post(
            self.base_url + "/chat_stream",
            json=self._request_pack("chat", message_list, **kwargs),
            stream=True,
        )
        try:
            importsseclient
        except ImportError:
            raise ImportError(
                "Could not import sseclient-py library."
                "Please install requests with `pip install sseclient-py`"
            )
        client = sseclient.SSEClient(response_gpt)
        chat_iter = client.events()

        defgen() -> ChatResponseGen:
            content = ""
            for item in chat_iter:
                item_dict = dict(item.data)
                chat_message, delta = self._message_unpacker(item_dict)
                content = content + self._space_handler(delta)
                chat_message.content = content
                yield ChatResponse(message=chat_message, raw=item_dict, delta=delta)

        return gen()

    @llm_chat_callback()
    async defachat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
        return self.chat(messages, **kwargs)

    @llm_chat_callback()
    async defastream_chat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponseAsyncGen:
        async defgen() -> ChatResponseAsyncGen:
            for message in self.stream_chat(messages, **kwargs):
                yield message

        # NOTE: convert generator to async generator
        return gen()

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        return self.complete(prompt, **kwargs)

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        async defgen() -> CompletionResponseAsyncGen:
            for message in self.stream_complete(prompt, **kwargs):
                yield message

        return gen()

    def_message_wrapper(self, messages: Sequence[ChatMessage]) -> List[Dict[str, Any]]:
        message_list = []
        for message in messages:
            role = message.role.value
            content = message.content
            message_list.append({"role": role, "content": content})
        return message_list

    def_message_unpacker(
        self, response_gpt: Dict[str, Any]
    ) -> Tuple[ChatMessage, str]:
        message = response_gpt["choices"][0]["message"]
        additional_kwargs = response_gpt["usage"]
        role = message["role"]
        content = message["content"]
        key = MessageRole.SYSTEM
        for r in MessageRole:
            if r.value == role:
                key = r
        chat_message = ChatMessage(
            role=key, content=content, additional_kwargs=additional_kwargs
        )
        return chat_message, content

    def_request_pack(
        self, mode: str, prompt: Union[str, List[Dict[str, Any]]], **kwargs: Any
    ) -> Optional[Dict[str, Any]]:
        if mode == "complete":
            return {
                "prompt": prompt,
                "max_tokens": kwargs.pop("max_tokens", self.max_tokens),
                "temperature": kwargs.pop("temperature", self.temperature),
                "top_k": kwargs.pop("top_k", 50),
                "top_p": kwargs.pop("top_p", 0.95),
                "repetition_penalty": kwargs.pop("repetition_penalty", 1.2),
                "do_sample": kwargs.pop("do_sample", False),
                "echo": kwargs.pop("echo", True),
                "n": kwargs.pop("n", 1),
                "stop": kwargs.pop("stop", "."),
            }
        elif mode == "chat":
            return {
                "messages": prompt,
                "max_tokens": kwargs.pop("max_tokens", self.max_tokens),
                "temperature": kwargs.pop("temperature", self.temperature),
                "top_k": kwargs.pop("top_k", 50),
                "top_p": kwargs.pop("top_p", 0.95),
                "repetition_penalty": kwargs.pop("repetition_penalty", 1.2),
                "do_sample": kwargs.pop("do_sample", False),
                "echo": kwargs.pop("echo", True),
                "n": kwargs.pop("n", 1),
                "stop": kwargs.pop("stop", "."),
            }
        return None

    def_space_handler(self, word: str) -> str:
        if word.isalnum():
            return " " + word
        return word

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/rungpt/#llama_index.llms.rungpt.RunGptLLM.metadata "Permanent link")

```
metadata: 

```

LLM metadata.
options: members: - RunGptLLM
