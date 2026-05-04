# Xinference
##  Xinference [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/xinference/#llama_index.llms.xinference.Xinference "Permanent link")
Bases: `CustomLLM`
Xinference LLM.
Examples:
`pip install llama-index-llms-xinference`

```
fromllama_index.llms.xinferenceimport Xinference

# Set up Xinference with required parameters
llm = Xinference(
    model_name="xinference-1.0",
    app_id="ml",
    user_id="xinference",
    api_key="<YOUR XINFERENCE API KEY>"
    temperature=0.5,
    max_tokens=256,
)

# Call the complete function
response = llm.complete("Hello World!")
print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-xinference/llama_index/llms/xinference/base.py`  
| 
```
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
```
 | 
```
classXinference(CustomLLM):
"""
    Xinference LLM.

    Examples:
        `pip install llama-index-llms-xinference`

        ```python
        from llama_index.llms.xinference import Xinference

        # Set up Xinference with required parameters
        llm = Xinference(
            model_name="xinference-1.0",
            app_id="ml",
            user_id="xinference",
            api_key="<YOUR XINFERENCE API KEY>"
            temperature=0.5,
            max_tokens=256,


        # Call the complete function
        response = llm.complete("Hello World!")
        print(response)
        ```

    """

    model_uid: str = Field(description="The Xinference model to use.")
    endpoint: str = Field(description="The Xinference endpoint URL to use.")
    temperature: float = Field(
        description="The temperature to use for sampling.", ge=0.0, le=1.0
    )
    max_tokens: int = Field(
        description="The maximum new tokens to generate as answer.", gt=0
    )
    context_window: int = Field(
        description="The maximum number of context tokens for the model.", gt=0
    )
    model_description: Dict[str, Any] = Field(
        description="The model description from Xinference."
    )

    _generator: Any = PrivateAttr()

    def__init__(
        self,
        model_uid: str,
        endpoint: str,
        temperature: float = DEFAULT_XINFERENCE_TEMP,
        max_tokens: Optional[int] = None,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
    ) -> None:
        generator, context_window, model_description = self.load_model(
            model_uid, endpoint
        )
        if max_tokens is None:
            max_tokens = context_window // 4
        elif max_tokens  context_window:
            raise ValueError(
                f"received max_tokens {max_tokens} with context window {context_window}"
                "max_tokens can not exceed the context window of the model"
            )

        super().__init__(
            model_uid=model_uid,
            endpoint=endpoint,
            temperature=temperature,
            context_window=context_window,
            max_tokens=max_tokens,
            model_description=model_description,
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )
        self._generator = generator

    defload_model(self, model_uid: str, endpoint: str) -> Tuple[Any, int, dict]:
        try:
            fromxinference.clientimport RESTfulClient
        except ImportError:
            raise ImportError(
                "Could not import Xinference library."
                'Please install Xinference with `pip install "xinference[all]"`'
            )

        client = RESTfulClient(endpoint)

        try:
            assert isinstance(client, RESTfulClient)
        except AssertionError:
            raise RuntimeError(
                "Could not create RESTfulClient instance."
                "Please make sure Xinference endpoint is running at the correct port."
            )

        generator = client.get_model(model_uid)
        model_description = client.list_models()[model_uid]

        try:
            assert generator is not None
            assert model_description is not None
        except AssertionError:
            raise RuntimeError(
                "Could not get model from endpoint."
                "Please make sure Xinference endpoint is running at the correct port."
            )

        model = model_description["model_name"]
        if "context_length" in model_description:
            context_window = model_description["context_length"]
        else:
            warnings.warn(
"""
            Parameter `context_length` not found in model description,
            using `xinference_modelname_to_contextsize` that is no longer maintained.
            Please update Xinference to the newest version.

            )
            context_window = xinference_modelname_to_contextsize(model)

        return generator, context_window, model_description

    @classmethod
    defclass_name(cls) -> str:
        return "Xinference_llm"

    @property
    defmetadata(self) -> LLMMetadata:
"""LLM metadata."""
        assert isinstance(self.context_window, int)
        return LLMMetadata(
            context_window=int(self.context_window // TOKEN_RATIO),
            num_output=self.max_tokens,
            model_name=self.model_uid,
        )

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        assert self.context_window is not None
        base_kwargs = {
            "temperature": self.temperature,
            "max_length": self.context_window,
        }
        return {
            **base_kwargs,
            **self.model_description,
        }

    def_get_input_dict(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        return {"prompt": prompt, **self._model_kwargs, **kwargs}

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        assert self._generator is not None
        prompt = messages[-1].content if len(messages)  0 else ""
        history = [xinference_message_to_history(message) for message in messages[:-1]]
        response_text = self._generator.chat(
            prompt=prompt,
            chat_history=history,
            generate_config={
                "stream": False,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            },
        )["choices"][0]["message"]["content"]
        return ChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT,
                content=response_text,
            ),
            delta=None,
        )

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        assert self._generator is not None
        prompt = messages[-1].content if len(messages)  0 else ""
        history = [xinference_message_to_history(message) for message in messages[:-1]]
        response_iter = self._generator.chat(
            prompt=prompt,
            chat_history=history,
            generate_config={
                "stream": True,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            },
        )

        defgen() -> ChatResponseGen:
            text = ""
            for c in response_iter:
                delta = c["choices"][0]["delta"].get("content", "")
                text += delta
                yield ChatResponse(
                    message=ChatMessage(
                        role=MessageRole.ASSISTANT,
                        content=text,
                    ),
                    delta=delta,
                )

        return gen()

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        assert self._generator is not None
        response_text = self._generator.chat(
            prompt=prompt,
            chat_history=None,
            generate_config={
                "stream": False,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            },
        )["choices"][0]["message"]["content"]
        return CompletionResponse(
            delta=None,
            text=response_text,
        )

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        assert self._generator is not None
        response_iter = self._generator.chat(
            prompt=prompt,
            chat_history=None,
            generate_config={
                "stream": True,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            },
        )

        defgen() -> CompletionResponseGen:
            text = ""
            for c in response_iter:
                delta = c["choices"][0]["delta"].get("content", "")
                text += delta
                yield CompletionResponse(
                    delta=delta,
                    text=text,
                )

        return gen()

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/xinference/#llama_index.llms.xinference.Xinference.metadata "Permanent link")

```
metadata: 

```

LLM metadata.
options: members: - Xinference
