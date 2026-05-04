# Lmstudio
##  LMStudio [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/lmstudio/#llama_index.llms.lmstudio.LMStudio "Permanent link")
Bases: `CustomLLM`
Source code in `llama-index-integrations/llms/llama-index-llms-lmstudio/llama_index/llms/lmstudio/base.py`  
| 
```
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
```
 | 
```
classLMStudio(CustomLLM):
    base_url: str = Field(
        default="http://localhost:1234/v1",
        description="Base url the model is hosted under.",
    )

    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description="The maximum number of context tokens for the model.",
        gt=0,
    )

    model_name: str = Field(description="The model to use.")

    request_timeout: float = Field(
        default=DEFAULT_REQUEST_TIMEOUT,
        description="The timeout for making http request in seconds to LM Studio API server.",
    )
    num_output: int = Field(
        default=DEFAULT_NUM_OUTPUTS,
        description=LLMMetadata.model_fields["num_output"].description,
    )

    is_chat_model: bool = Field(
        default=True,
        description=(
            "LM Studio API supports chat."
            + LLMMetadata.model_fields["is_chat_model"].description
        ),
    )

    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        description=("The temperature to use for sampling."),
        ge=0.0,
        le=1.0,
    )

    timeout: float = Field(
        default=120, description=("The timeout to use in seconds."), ge=0
    )

    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description=("Additional kwargs to pass to the model.")
    )

    def_create_payload_from_messages(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> Dict[str, Any]:
        return {
            "model": self.model_name,
            "messages": [
                {
                    "role": message.role.value,
                    "content": message.content,
                    **(
                        message.additional_kwargs
                        if message.additional_kwargs is not None
                        else {}
                    ),
                }
                for message in messages
            ],
            "options": self._model_kwargs,
            "stream": False,
            **kwargs,
        }

    def_create_chat_response_from_http_response(
        self, response: httpx.Response
    ) -> ChatResponse:
        raw = response.json()
        message = raw["choices"][0]["message"]
        return ChatResponse(
            message=ChatMessage(
                content=message.get("content"),
                role=MessageRole(message.get("role")),
                additional_kwargs=get_additional_kwargs(message, ("content", "role")),
            ),
            raw=raw,
            additional_kwargs=get_additional_kwargs(raw, ("choices",)),
        )

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        payload = self._create_payload_from_messages(messages, **kwargs)
        with httpx.Client(timeout=Timeout(self.request_timeout)) as client:
            response = client.post(
                url=f"{self.base_url}/chat/completions",
                json=payload,
            )
            response.raise_for_status()
            return self._create_chat_response_from_http_response(response)

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        payload = self._create_payload_from_messages(messages, **kwargs)
        async with httpx.AsyncClient(timeout=Timeout(self.request_timeout)) as client:
            response = await client.post(
                url=f"{self.base_url}/chat/completions",
                json=payload,
            )
            response.raise_for_status()
            return self._create_chat_response_from_http_response(response)

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        complete_fn = chat_to_completion_decorator(self.chat)
        return complete_fn(prompt, **kwargs)

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
        payload = self._create_payload_from_messages(messages, stream=True, **kwargs)

        with httpx.Client(timeout=Timeout(self.request_timeout)) as client:
            with client.stream(
                method="POST",
                url=f"{self.base_url}/chat/completions",
                json=payload,
            ) as response:
                response.raise_for_status()
                text = ""
                for line in response.iter_lines():
                    if line:
                        line = line.strip()
                        if isinstance(line, bytes):
                            line = line.decode("utf-8")

                        if line.startswith("data: [DONE]"):
                            break

                        # Slice the line to remove the "data: " prefix
                        chunk = json.loads(line[5:])

                        delta = chunk["choices"][0].get("delta")

                        role = delta.get("role") or MessageRole.ASSISTANT
                        content_delta = delta.get("content") or ""
                        text += content_delta

                        yield ChatResponse(
                            message=ChatMessage(
                                content=text,
                                role=MessageRole(role),
                                additional_kwargs=get_additional_kwargs(
                                    chunk, ("choices",)
                                ),
                            ),
                            delta=content_delta,
                            raw=chunk,
                            additional_kwargs=get_additional_kwargs(
                                chunk, ("choices",)
                            ),
                        )

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        stream_complete_fn = stream_chat_to_completion_decorator(self.stream_chat)
        return stream_complete_fn(prompt, **kwargs)

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        astream_complete_fn = astream_chat_to_completion_decorator(self.astream_chat)
        return await astream_complete_fn(prompt, **kwargs)

    @property
    defmetadata(self) -> LLMMetadata:
"""LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model_name,
            is_chat_model=self.is_chat_model,
        )

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "temperature": self.temperature,
            "num_ctx": self.context_window,
        }
        return {
            **base_kwargs,
            **self.additional_kwargs,
        }

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/lmstudio/#llama_index.llms.lmstudio.LMStudio.metadata "Permanent link")

```
metadata: 

```

LLM metadata.
options: members: - LMStudio
