# Octoai
##  OctoAI [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/octoai/#llama_index.llms.octoai.OctoAI "Permanent link")
Bases: 
Source code in `llama-index-integrations/llms/llama-index-llms-octoai/llama_index/llms/octoai/base.py`  
| 
```
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
```
 | 
```
classOctoAI(LLM):
    model: str = Field(
        default=DEFAULT_OCTOAI_MODEL, description="The model to use with OctoAI"
    )
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        description="The temperature to use during generation.",
        ge=0.0,
        le=1.0,
    )
    max_tokens: Optional[int] = Field(
        description="The maximum number of tokens to generate.",
        gt=0,
    )
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the OctoAI SDK."
    )

    def__init__(
        self,
        model: str = DEFAULT_OCTOAI_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: Optional[int] = None,
        timeout: int = 120,
        token: Optional[str] = None,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        callback_manager: Optional[CallbackManager] = None,
        # base class
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[MessagesToPromptCallable] = None,
        completion_to_prompt: Optional[CompletionToPromptCallable] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
    ) -> None:
        additional_kwargs = additional_kwargs or {}
        callback_manager = callback_manager or CallbackManager([])

        super().__init__(
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            additional_kwargs=additional_kwargs,
        )

        token = get_from_param_or_env("token", token, "OCTOAI_TOKEN", "")

        if not token:
            raise ValueError(
                "You must provide an API token to use OctoAI. "
                "You can either pass it in as an argument or set it `OCTOAI_TOKEN`."
                "To generate a token in your OctoAI account settings: https://octoai.cloud/settings`."
            )

        try:
            self._client = Client(api_key=token, timeout=timeout)
        except ImportError as err:
            raise ImportError(
                "Could not import OctoAI python package. "
                "Please install it with `pip install octoai-sdk`."
            ) fromerr

    @property
    defmetadata(self) -> LLMMetadata:
"""Get LLM metadata."""
        return LLMMetadata(
            context_window=octoai_modelname_to_contextsize(self.model),
            num_output=self.max_tokens or -1,
            is_chat_model=True,
            model_name=self.model,
        )

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "model": self.model,
            "temperature": self.temperature,
        }
        if self.max_tokens:
            base_kwargs["max_tokens"] = self.max_tokens

        return {
            **base_kwargs,
            **self.additional_kwargs,
        }

    def_get_all_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        return {
            **self._model_kwargs,
            **kwargs,
        }

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        response = self._client.text_gen.create_chat_completion(
            messages=to_octoai_messages(messages), **self._get_all_kwargs(**kwargs)
        )

        return ChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT, content=response.choices[0].message.content
            ),
            raw=dict(response),
        )

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        streaming_response = self._client.text_gen.create_chat_completion_stream(
            messages=to_octoai_messages(messages),
            **self._get_all_kwargs(**kwargs),
        )

        defgen() -> ChatResponseGen:
            content = ""
            role = MessageRole.ASSISTANT
            for completion in streaming_response:
                content_delta = completion.choices[0].delta.content
                if content_delta is None:
                    continue
                content += content_delta

                yield ChatResponse(
                    message=ChatMessage(role=role, content=content),
                    delta=content_delta,
                    raw=completion,
                )

        return gen()

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

    # ===== Async Endpoints =====
    @llm_chat_callback()
    async defachat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
        raise NotImplementedError

    @llm_chat_callback()
    async defastream_chat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponseAsyncGen:
        raise NotImplementedError

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        raise NotImplementedError

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        raise NotImplementedError

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/octoai/#llama_index.llms.octoai.OctoAI.metadata "Permanent link")

```
metadata: 

```

Get LLM metadata.
options: members: - OctoAI
