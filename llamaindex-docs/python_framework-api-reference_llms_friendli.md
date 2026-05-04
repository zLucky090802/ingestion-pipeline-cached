# Friendli
##  Friendli [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/friendli/#llama_index.llms.friendli.Friendli "Permanent link")
Bases: 
Friendli LLM.
Source code in `llama-index-integrations/llms/llama-index-llms-friendli/llama_index/llms/friendli/base.py`  
| 
```
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
```
 | 
```
classFriendli(LLM):
"""Friendli LLM."""

    model: str = Field(description="The friendli model to use.")
    max_tokens: int = Field(description="The maximum number of tokens to generate.")
    temperature: Optional[float] = Field(
        description="The temperature to use for sampling."
    )

    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the Friendli API."
    )

    _client: Any = PrivateAttr()
    _aclient: Any = PrivateAttr()

    def__init__(
        self,
        model: str = "mixtral-8x7b-instruct-v0-1",
        friendli_token: Optional[str] = None,
        max_tokens: int = 256,
        temperature: Optional[float] = 0.1,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
    ) -> None:
        additional_kwargs = additional_kwargs or {}
        callback_manager = callback_manager or CallbackManager([])

        super().__init__(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            additional_kwargs=additional_kwargs,
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )

        self._client = friendli.Friendli(token=friendli_token)
        self._aclient = friendli.AsyncFriendli(token=friendli_token)

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "Friendli_LLM"

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=friendli_modelname_to_contextsize(self.model),
            num_output=self.max_tokens,
            is_chat_model=True,
            model_name=self.model,
        )

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        return {**base_kwargs, **self.additional_kwargs}

    def_get_all_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        return {
            **self._model_kwargs,
            **kwargs,
        }

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        all_kwargs = self._get_all_kwargs(**kwargs)

        response = self._client.chat.completions.create(
            stream=False,
            **get_chat_request(messages),
            **all_kwargs,
        )
        return ChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT, content=response.choices[0].message.content
            ),
            raw=response.__dict__,
            additional_kwargs={"usage": response.usage.__dict__},
        )

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        all_kwargs = self._get_all_kwargs(**kwargs)

        response = self._client.completions.create(
            prompt=prompt,
            stream=False,
            **all_kwargs,
        )
        return CompletionResponse(
            text=response.choices[0].text,
            additional_kwargs={"usage": response.usage.__dict__},
            raw=response.__dict__,
        )

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        all_kwargs = self._get_all_kwargs(**kwargs)

        stream = self._client.chat.completions.create(
            stream=True,
            **get_chat_request(messages),
            **all_kwargs,
        )

        defgen() -> ChatResponseGen:
            content = ""
            for chunk in stream:
                content_delta = chunk.choices[0].delta.content or ""
                content += content_delta
                yield ChatResponse(
                    message=ChatMessage(role=MessageRole.ASSISTANT, content=content),
                    delta=content_delta,
                    raw=chunk.__dict__,
                )

        return gen()

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        all_kwargs = self._get_all_kwargs(**kwargs)

        stream = self._client.completions.create(
            prompt=prompt,
            stream=True,
            **all_kwargs,
        )

        defgen() -> CompletionResponseGen:
            content = ""
            for chunk in stream:
                content_delta = chunk.text
                content += content_delta
                yield CompletionResponse(
                    text=content,
                    delta=content_delta,
                    raw=chunk.__dict__,
                )

        return gen()

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        all_kwargs = self._get_all_kwargs(**kwargs)

        response = await self._aclient.chat.completions.create(
            stream=False,
            **get_chat_request(messages),
            **all_kwargs,
        )
        return ChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT, content=response.choices[0].message.content
            ),
            raw=response.__dict__,
            additional_kwargs={"usage": response.usage.__dict__},
        )

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        all_kwargs = self._get_all_kwargs(**kwargs)

        response = await self._aclient.completions.create(
            prompt=prompt,
            stream=False,
            **all_kwargs,
        )
        return CompletionResponse(
            text=response.choices[0].text,
            additional_kwargs={"usage": response.usage.__dict__},
            raw=response.__dict__,
        )

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        all_kwargs = self._get_all_kwargs(**kwargs)

        stream = await self._aclient.chat.completions.create(
            stream=True,
            **get_chat_request(messages),
            **all_kwargs,
        )

        async defgen() -> ChatResponseAsyncGen:
            content = ""
            async for chunk in stream:
                content_delta = chunk.choices[0].delta.content or ""
                content += content_delta
                yield ChatResponse(
                    message=ChatMessage(role=MessageRole.ASSISTANT, content=content),
                    delta=content_delta,
                    raw=chunk.__dict__,
                )

        return gen()

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        all_kwargs = self._get_all_kwargs(**kwargs)

        stream = await self._aclient.completions.create(
            prompt=prompt,
            stream=True,
            **all_kwargs,
        )

        async defgen() -> CompletionResponseAsyncGen:
            content = ""
            async for chunk in stream:
                content_delta = chunk.text
                content += content_delta
                yield CompletionResponse(
                    text=content,
                    delta=content_delta,
                    raw=chunk.__dict__,
                )

        return gen()

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/friendli/#llama_index.llms.friendli.Friendli.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-friendli/llama_index/llms/friendli/base.py`  
| 
```
76
77
78
79
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "Friendli_LLM"

```
 |  
| --- | --- |  
options: members: - Friendli
