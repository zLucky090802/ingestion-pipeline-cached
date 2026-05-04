# Llamafile
##  Llamafile [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/llamafile/#llama_index.llms.llamafile.Llamafile "Permanent link")
Bases: `CustomLLM`
llamafile lets you distribute and run large language models with a single file.
To get started, see: https://github.com/Mozilla-Ocho/llamafile
To use this class, you will need to first:
  1. Download a llamafile.
  2. Make the downloaded file executable: `chmod +x path/to/model.llamafile`
  3. Start the llamafile in server mode:
`./path/to/model.llamafile --server --nobrowser`

Source code in `llama-index-integrations/llms/llama-index-llms-llamafile/llama_index/llms/llamafile/base.py`  
| 
```
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
```
 | 
```
classLlamafile(CustomLLM):
"""
    llamafile lets you distribute and run large language models with a
    single file.

    To get started, see: https://github.com/Mozilla-Ocho/llamafile

    To use this class, you will need to first:

    1. Download a llamafile.
    2. Make the downloaded file executable: `chmod +x path/to/model.llamafile`
    3. Start the llamafile in server mode:

        `./path/to/model.llamafile --server --nobrowser`
    """

    base_url: str = Field(
        default="http://localhost:8080",
        description="Base url where the llamafile server is listening.",
    )

    request_timeout: float = Field(
        default=DEFAULT_REQUEST_TIMEOUT,
        description="The timeout for making http request to llamafile API server",
    )

    #
    # Generation options
    #
    temperature: float = Field(
        default=0.8,
        description="The temperature to use for sampling.",
        ge=0.0,
        le=1.0,
    )

    seed: int = Field(default=0, description="Random seed")

    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional options to pass in requests to the llamafile API.",
    )

    @classmethod
    defclass_name(cls) -> str:
        return "llamafile_llm"

    @property
    defmetadata(self) -> LLMMetadata:
"""LLM metadata."""
        return LLMMetadata(
            is_chat_model=True,  # llamafile has OpenAI-compatible chat API for all models
        )

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "temperature": self.temperature,
            "seed": self.seed,
        }
        return {
            **base_kwargs,
            **self.additional_kwargs,
        }

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        payload = {
            "messages": [
                {
                    "role": message.role.value,
                    "content": message.content,
                    **message.additional_kwargs,
                }
                for message in messages
            ],
            "options": self._model_kwargs,
            "stream": False,
            **kwargs,
        }

        with httpx.Client(timeout=Timeout(self.request_timeout)) as client:
            response = client.post(
                url=f"{self.base_url}/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            raw = response.json()
            choice = raw["choices"][0]
            message = choice["message"]

            return ChatResponse(
                message=ChatMessage(
                    content=message.get("content"),
                    role=MessageRole(message.get("role")),
                    additional_kwargs=get_additional_kwargs(
                        message, ("content", "role")
                    ),
                ),
                raw=raw,
                additional_kwargs=get_additional_kwargs(raw, ("choice",)),
            )

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        payload = {
            "messages": [
                {
                    "role": message.role.value,
                    "content": message.content,
                    **message.additional_kwargs,
                }
                for message in messages
            ],
            "options": self._model_kwargs,
            "stream": True,
            **kwargs,
        }

        with httpx.Client(timeout=Timeout(self.request_timeout)) as client:
            with client.stream(
                method="POST",
                url=f"{self.base_url}/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                },
                json=payload,
            ) as response:
                response.raise_for_status()

                with io.StringIO() as buff:
                    for line in response.iter_lines():
                        if line:
                            chunk = self._get_streaming_chunk_content(line)
                            choice = chunk.pop("choices")[0]
                            delta_message = choice["delta"]

                            # default to 'assistant' if response does not contain 'role'
                            role = delta_message.get("role", MessageRole.ASSISTANT)

                            # The last message has no content
                            delta_content = delta_message.get("content", None)
                            if delta_content:
                                buff.write(delta_content)
                            else:
                                delta_content = ""

                            yield ChatResponse(
                                message=ChatMessage(
                                    content=buff.getvalue(),
                                    role=MessageRole(role),
                                    additional_kwargs=get_additional_kwargs(
                                        delta_message, ("content", "role")
                                    ),
                                ),
                                delta=delta_content,
                                raw=chunk,
                                additional_kwargs=get_additional_kwargs(
                                    chunk, ("choices",)
                                ),
                            )

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        payload = {
            "prompt": prompt,
            "stream": False,
            **self._model_kwargs,
            **kwargs,
        }

        with httpx.Client(timeout=Timeout(self.request_timeout)) as client:
            response = client.post(
                url=f"{self.base_url}/completion",
                headers={
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            raw = response.json()
            text = raw.get("content")
            return CompletionResponse(
                text=text,
                raw=raw,
                additional_kwargs=get_additional_kwargs(raw, ("response",)),
            )

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        payload = {
            "prompt": prompt,
            "stream": True,
            **self._model_kwargs,
            **kwargs,
        }

        with httpx.Client(timeout=Timeout(self.request_timeout)) as client:
            with client.stream(
                method="POST",
                url=f"{self.base_url}/completion",
                headers={
                    "Content-Type": "application/json",
                },
                json=payload,
            ) as response:
                response.raise_for_status()

                with io.StringIO() as buff:
                    for line in response.iter_lines():
                        if line:
                            chunk = self._get_streaming_chunk_content(line)
                            delta = chunk.get("content")
                            buff.write(delta)
                            yield CompletionResponse(
                                delta=delta,
                                text=buff.getvalue(),
                                raw=chunk,
                                additional_kwargs=get_additional_kwargs(
                                    chunk, ("content",)
                                ),
                            )

    def_get_streaming_chunk_content(self, chunk: str) -> Dict:
"""
        Extract json from chunks received from llamafile API streaming calls.

        When streaming is turned on, llamafile server returns lines like:

        'data: {"content":" They","multimodal":true,"slot_id":0,"stop":false}'

        Here, we convert this to a dict and return the value of the 'content'
        field
        """
        if chunk.startswith("data:"):
            cleaned = chunk.lstrip("data: ")
            return json.loads(cleaned)
        else:
            raise ValueError(
                f"Received chunk with unexpected format during streaming: '{chunk}'"
            )

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/llamafile/#llama_index.llms.llamafile.Llamafile.metadata "Permanent link")

```
metadata: 

```

LLM metadata.
options: members: - Llamafile
