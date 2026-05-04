# Gigachat
##  GigaChatLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/gigachat/#llama_index.llms.gigachat.GigaChatLLM "Permanent link")
Bases: `CustomLLM`
GigaChat LLM Implementation.
Examples:
`pip install llama-index-llms-gigachat-ru`

```
fromllama_index.llms.gigachatimport GigaChatLLM

llm = GigaChatLLM(
    credentials="YOUR_GIGACHAT_SECRET",
    verify_ssl_certs=False,
)
resp = llm.complete("What is the capital of France?")
print(resp)

```

Source code in `llama-index-integrations/llms/llama-index-llms-gigachat/llama_index/llms/gigachat/base.py`  
| 
```
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
```
 | 
```
classGigaChatLLM(CustomLLM):
"""
    GigaChat LLM Implementation.

    Examples:
        `pip install llama-index-llms-gigachat-ru`

        ```python
        from llama_index.llms.gigachat import GigaChatLLM

        llm = GigaChatLLM(
            credentials="YOUR_GIGACHAT_SECRET",
            verify_ssl_certs=False,

        resp = llm.complete("What is the capital of France?")
        print(resp)
        ```

    """

    model: GigaChatModel = Field(default=GigaChatModel.GIGACHAT)
    base_url: Optional[str] = None
    auth_url: Optional[str] = None
    credentials: Optional[str] = None
    scope: Optional[str] = None
    access_token: Optional[str] = None
    profanity_check: Optional[bool] = None
    user: Optional[str] = None
    password: Optional[str] = None
    timeout: Optional[float] = None
    verify_ssl_certs: Optional[bool] = None
    verbose: Optional[bool] = None
    ca_bundle_file: Optional[str] = None
    cert_file: Optional[str] = None
    key_file: Optional[str] = None
    key_file_password: Optional[str] = None

    @property
    defcontext_window(self) -> int:
"""Get context window."""
        return CONTEXT_WINDOWS[self.model]

    @property
    defmetadata(self) -> LLMMetadata:
"""Get LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.context_window,
            model_name=self.model,
        )

    @llm_completion_callback()
    async defacomplete(
        self,
        prompt: str,
        formatted: bool = False,
        **kwargs: Any,
    ) -> CompletionResponse:
"""Get completion asynchronously."""
        async with GigaChat(**self._gigachat_kwargs) as giga:
            response = await giga.achat(
                Chat(
                    model=self.model,
                    messages=[Messages(role="user", content=prompt)],
                )
            )
        return CompletionResponse(
            text=response.choices[0].message.content,
        )

    @llm_completion_callback()
    defcomplete(
        self,
        prompt: str,
        formatted: bool = False,
        **kwargs: Any,
    ) -> CompletionResponse:
"""Get completion."""
        with GigaChat(**self._gigachat_kwargs) as giga:
            response = giga.chat(
                Chat(
                    model=self.model,
                    messages=[Messages(role="user", content=prompt)],
                )
            )
        return CompletionResponse(
            text=response.choices[0].message.content,
        )

    @llm_chat_callback()
    async defachat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
"""Get chat asynchronously."""
        async with GigaChat(**self._gigachat_kwargs) as giga:
            response = await giga.achat(
                Chat(
                    model=self.model,
                    messages=[
                        Messages(role=message.role, content=message.content)
                        for message in messages
                    ],
                )
            )
        return ChatResponse(
            message=ChatMessage(
                content=response.choices[0].message.content,
                role="assistant",
            ),
        )

    @llm_chat_callback()
    defchat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
"""Get chat."""
        with GigaChat(**self._gigachat_kwargs) as giga:
            response = giga.chat(
                Chat(
                    model=self.model,
                    messages=[
                        Messages(role=message.role, content=message.content)
                        for message in messages
                    ],
                )
            )
        return ChatResponse(
            message=ChatMessage(
                content=response.choices[0].message.content,
                role="assistant",
            ),
        )

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, **kwargs: Any
    ) -> AsyncGenerator[CompletionResponse, Any]:
"""Get streaming completion asynchronously."""

        async defgen() -> AsyncGenerator[CompletionResponse, Any]:
            async with GigaChat(**self._gigachat_kwargs) as giga:
                chat = Chat(
                    model=self.model,
                    messages=[Messages(role="user", content=prompt)],
                )

                response = ""
                async for token in giga.astream(chat):
                    delta = token.choices[0].delta.content
                    response += delta
                    yield CompletionResponse(text=response, delta=delta)

        return gen()

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
"""Get streaming completion."""

        defgen() -> Generator[CompletionResponse, Any, Any]:
            with GigaChat(**self._gigachat_kwargs) as giga:
                chat = Chat(
                    model=self.model,
                    messages=[Messages(role="user", content=prompt)],
                )

                response = ""
                for token in giga.stream(chat):
                    delta = token.choices[0].delta.content
                    response += delta
                    yield CompletionResponse(text=response, delta=delta)

        return gen()

    @property
    def_gigachat_kwargs(self) -> Dict[str, Union[str, bool, float]]:
"""Get GigaChat specific kwargs."""
        return {
            "base_url": self.base_url,
            "auth_url": self.auth_url,
            "credentials": self.credentials,
            "scope": self.scope,
            "access_token": self.access_token,
            "timeout": self.timeout,
            "verify_ssl_certs": self.verify_ssl_certs,
            "verbose": self.verbose,
            "ca_bundle_file": self.ca_bundle_file,
            "cert_file": self.cert_file,
            "key_file": self.key_file,
            "key_file_password": self.key_file_password,
        }

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "GigaChatLLM"

```
 |  
| --- | --- |  
###  context_window `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/gigachat/#llama_index.llms.gigachat.GigaChatLLM.context_window "Permanent link")

```
context_window: 

```

Get context window.
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/gigachat/#llama_index.llms.gigachat.GigaChatLLM.metadata "Permanent link")

```
metadata: 

```

Get LLM metadata.
###  acomplete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/gigachat/#llama_index.llms.gigachat.GigaChatLLM.acomplete "Permanent link")

```
acomplete(
    prompt: , formatted:  = False, **kwargs: 
) -> 

```

Get completion asynchronously.
Source code in `llama-index-integrations/llms/llama-index-llms-gigachat/llama_index/llms/gigachat/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
async defacomplete(
    self,
    prompt: str,
    formatted: bool = False,
    **kwargs: Any,
) -> CompletionResponse:
"""Get completion asynchronously."""
    async with GigaChat(**self._gigachat_kwargs) as giga:
        response = await giga.achat(
            Chat(
                model=self.model,
                messages=[Messages(role="user", content=prompt)],
            )
        )
    return CompletionResponse(
        text=response.choices[0].message.content,
    )

```
 |  
| --- | --- |  
###  complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/gigachat/#llama_index.llms.gigachat.GigaChatLLM.complete "Permanent link")

```
complete(
    prompt: , formatted:  = False, **kwargs: 
) -> 

```

Get completion.
Source code in `llama-index-integrations/llms/llama-index-llms-gigachat/llama_index/llms/gigachat/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defcomplete(
    self,
    prompt: str,
    formatted: bool = False,
    **kwargs: Any,
) -> CompletionResponse:
"""Get completion."""
    with GigaChat(**self._gigachat_kwargs) as giga:
        response = giga.chat(
            Chat(
                model=self.model,
                messages=[Messages(role="user", content=prompt)],
            )
        )
    return CompletionResponse(
        text=response.choices[0].message.content,
    )

```
 |  
| --- | --- |  
###  achat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/gigachat/#llama_index.llms.gigachat.GigaChatLLM.achat "Permanent link")

```
achat(
    messages: Sequence[], **kwargs: 
) -> 

```

Get chat asynchronously.
Source code in `llama-index-integrations/llms/llama-index-llms-gigachat/llama_index/llms/gigachat/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
async defachat(
    self,
    messages: Sequence[ChatMessage],
    **kwargs: Any,
) -> ChatResponse:
"""Get chat asynchronously."""
    async with GigaChat(**self._gigachat_kwargs) as giga:
        response = await giga.achat(
            Chat(
                model=self.model,
                messages=[
                    Messages(role=message.role, content=message.content)
                    for message in messages
                ],
            )
        )
    return ChatResponse(
        message=ChatMessage(
            content=response.choices[0].message.content,
            role="assistant",
        ),
    )

```
 |  
| --- | --- |  
###  chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/gigachat/#llama_index.llms.gigachat.GigaChatLLM.chat "Permanent link")

```
chat(
    messages: Sequence[], **kwargs: 
) -> 

```

Get chat.
Source code in `llama-index-integrations/llms/llama-index-llms-gigachat/llama_index/llms/gigachat/base.py`  
| 
```
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
```
 | 
```
@llm_chat_callback()
defchat(
    self,
    messages: Sequence[ChatMessage],
    **kwargs: Any,
) -> ChatResponse:
"""Get chat."""
    with GigaChat(**self._gigachat_kwargs) as giga:
        response = giga.chat(
            Chat(
                model=self.model,
                messages=[
                    Messages(role=message.role, content=message.content)
                    for message in messages
                ],
            )
        )
    return ChatResponse(
        message=ChatMessage(
            content=response.choices[0].message.content,
            role="assistant",
        ),
    )

```
 |  
| --- | --- |  
###  astream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/gigachat/#llama_index.llms.gigachat.GigaChatLLM.astream_complete "Permanent link")

```
astream_complete(
    prompt: , **kwargs: 
) -> AsyncGenerator[, ]

```

Get streaming completion asynchronously.
Source code in `llama-index-integrations/llms/llama-index-llms-gigachat/llama_index/llms/gigachat/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
async defastream_complete(
    self, prompt: str, **kwargs: Any
) -> AsyncGenerator[CompletionResponse, Any]:
"""Get streaming completion asynchronously."""

    async defgen() -> AsyncGenerator[CompletionResponse, Any]:
        async with GigaChat(**self._gigachat_kwargs) as giga:
            chat = Chat(
                model=self.model,
                messages=[Messages(role="user", content=prompt)],
            )

            response = ""
            async for token in giga.astream(chat):
                delta = token.choices[0].delta.content
                response += delta
                yield CompletionResponse(text=response, delta=delta)

    return gen()

```
 |  
| --- | --- |  
###  stream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/gigachat/#llama_index.llms.gigachat.GigaChatLLM.stream_complete "Permanent link")

```
stream_complete(
    prompt: , formatted:  = False, **kwargs: 
) -> CompletionResponseGen

```

Get streaming completion.
Source code in `llama-index-integrations/llms/llama-index-llms-gigachat/llama_index/llms/gigachat/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defstream_complete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponseGen:
"""Get streaming completion."""

    defgen() -> Generator[CompletionResponse, Any, Any]:
        with GigaChat(**self._gigachat_kwargs) as giga:
            chat = Chat(
                model=self.model,
                messages=[Messages(role="user", content=prompt)],
            )

            response = ""
            for token in giga.stream(chat):
                delta = token.choices[0].delta.content
                response += delta
                yield CompletionResponse(text=response, delta=delta)

    return gen()

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/gigachat/#llama_index.llms.gigachat.GigaChatLLM.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-gigachat/llama_index/llms/gigachat/base.py`  
| 
```
231
232
233
234
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "GigaChatLLM"

```
 |  
| --- | --- |  
options: members: - GigaChatLLM
