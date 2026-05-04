# Alephalpha
##  AlephAlpha [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/alephalpha/#llama_index.llms.alephalpha.AlephAlpha "Permanent link")
Bases: 
Aleph Alpha LLMs.
Source code in `llama-index-integrations/llms/llama-index-llms-alephalpha/llama_index/llms/alephalpha/base.py`  
| 
```
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
```
 | 
```
classAlephAlpha(LLM):
"""Aleph Alpha LLMs."""

    model: str = Field(
        default=DEFAULT_ALEPHALPHA_MODEL, description="The Aleph Alpha model to use."
    )
    token: str = Field(default=None, description="The Aleph Alpha API token.")
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        description="The temperature to use for sampling.",
        ge=0.0,
        le=1.0,
    )
    max_tokens: int = Field(
        default=DEFAULT_ALEPHALPHA_MAX_TOKENS,
        description="The maximum number of tokens to generate.",
        gt=0,
    )
    base_url: Optional[str] = Field(
        default=DEFAULT_ALEPHALPHA_HOST, description="The hostname of the API base_url."
    )
    timeout: Optional[float] = Field(
        default=None, description="The timeout to use in seconds.", ge=0
    )
    max_retries: int = Field(
        default=10, description="The maximum number of API retries.", ge=0
    )
    hosting: Optional[str] = Field(default=None, description="The hosting to use.")
    nice: bool = Field(default=False, description="Whether to be nice to the API.")
    verify_ssl: bool = Field(default=True, description="Whether to verify SSL.")
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the Aleph Alpha API."
    )
    repetition_penalties_include_prompt: bool = Field(
        default=True,
        description="Whether presence penalty or frequency penalty are updated from the prompt",
    )
    repetition_penalties_include_completion: bool = Field(
        default=True,
        description="Whether presence penalty or frequency penalty are updated from the completion.",
    )
    sequence_penalty: float = Field(
        default=0.7,
        description="The sequence penalty to use. Increasing the sequence penalty reduces the likelihood of reproducing token sequences that already appear in the prompt",
        ge=0.0,
        le=1.0,
    )
    sequence_penalty_min_length: int = Field(
        default=3,
        description="Minimal number of tokens to be considered as sequence. Must be greater or equal 2.",
        ge=2,
    )
    stop_sequences: List[str] = Field(
        default=["\n\n"], description="The stop sequences to use."
    )
    log_probs: Optional[int] = Field(
        default=None,
        description="Number of top log probabilities to return for each token generated.",
        ge=0,
    )
    top_p: Optional[float] = Field(
        default=None,
        description="Nucleus sampling parameter controlling the cumulative probability threshold.",
        ge=0.0,
        le=1.0,
    )
    echo: Optional[bool] = Field(
        default=False, description="Echo the prompt in the completion."
    )
    penalty_exceptions: Optional[List[str]] = Field(
        default=None,
        description="List of strings that may be generated without penalty, regardless of other penalty settings.",
    )
    n: Optional[int] = Field(
        default=1,
        description="The number of completions to return. Useful for generating multiple alternatives.",
    )

    _client: Optional[Client] = PrivateAttr()
    _aclient: Optional[AsyncClient] = PrivateAttr()

    def__init__(
        self,
        model: str = DEFAULT_ALEPHALPHA_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_ALEPHALPHA_MAX_TOKENS,
        base_url: Optional[str] = DEFAULT_ALEPHALPHA_HOST,
        timeout: Optional[float] = None,
        max_retries: int = 10,
        token: Optional[str] = None,
        hosting: Optional[str] = None,
        nice: bool = False,
        verify_ssl: bool = True,
        log_probs: Optional[int] = None,
        top_p: Optional[float] = None,
        echo: Optional[bool] = False,
        penalty_exceptions: Optional[List[str]] = None,
        n: Optional[int] = 1,
        additional_kwargs: Optional[Dict[str, Any]] = None,
    ) -> None:
        additional_kwargs = additional_kwargs or {}

        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            additional_kwargs=additional_kwargs,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            hosting=hosting,
            nice=nice,
            verify_ssl=verify_ssl,
        )

        self.token = get_from_param_or_env("aa_token", token, "AA_TOKEN", "")

        self.log_probs = log_probs
        self.top_p = top_p
        self.echo = echo
        self.penalty_exceptions = penalty_exceptions
        self.n = n

        self._client = None
        self._aclient = None

    @classmethod
    defclass_name(cls) -> str:
        return "AlephAlpha"

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=alephalpha_modelname_to_contextsize(self.model),
            num_output=self.max_tokens,
            is_chat_model=False,  # The Aleph Alpha API does not support chat yet
            model_name=self.model,
        )

    @property
    deftokenizer(self) -> Tokenizer:
        client = self._get_client()
        return client.tokenizer(model=self.model)

    @property
    def_model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "model": self.model,
            "temperature": self.temperature,
            "maximum_tokens": self.max_tokens,
        }
        return {
            **base_kwargs,
            **self.additional_kwargs,
        }

    @property
    def_completion_kwargs(self) -> Dict[str, Any]:
        completion_kwargs = {
            "maximum_tokens": self.max_tokens,
            "temperature": self.temperature,
            "log_probs": self.log_probs,
            "top_p": self.top_p,
            "echo": self.echo,
            "penalty_exceptions": self.penalty_exceptions,
            "n": self.n,
            "repetition_penalties_include_prompt": self.repetition_penalties_include_prompt,
            "repetition_penalties_include_completion": self.repetition_penalties_include_completion,
            "sequence_penalty": self.sequence_penalty,
            "sequence_penalty_min_length": self.sequence_penalty_min_length,
            "stop_sequences": self.stop_sequences,
        }

        return {k: v for k, v in completion_kwargs.items() if v is not None}

    def_get_all_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        return {
            **self._model_kwargs,
            **kwargs,
        }

    def_get_credential_kwargs(self) -> Dict[str, Any]:
        return {
            "token": self.token,
            "host": self.base_url,
            "hosting": self.hosting,
            "request_timeout_seconds": self.timeout,
            "total_retries": self.max_retries,
            "nice": self.nice,
            "verify_ssl": self.verify_ssl,
        }

    def_get_client(self) -> Client:
        if self._client is None:
            self._client = Client(**self._get_credential_kwargs())
        return self._client

    def_get_aclient(self) -> AsyncClient:
        if self._aclient is None:
            self._aclient = AsyncClient(**self._get_credential_kwargs())
        return self._aclient

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        raise NotImplementedError("Aleph Alpha does not currently support chat.")

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        client = self._get_client()
        all_kwargs = {
            "prompt": Prompt.from_text(prompt),
            **self._completion_kwargs,
            **kwargs,
        }
        request = CompletionRequest(**all_kwargs)
        response = client.complete(request=request, model=self.model)
        completion = response.completions[0].completion if response.completions else ""
        return process_response(response, completion)

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        client = self._get_aclient()
        all_kwargs = {
            "prompt": Prompt.from_text(prompt),
            **self._completion_kwargs,
            **kwargs,
        }
        request = CompletionRequest(**all_kwargs)
        async with client as aclient:
            response = await aclient.complete(request=request, model=self.model)
            completion = (
                response.completions[0].completion if response.completions else ""
            )
            return process_response(response, completion)

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        raise NotImplementedError("Aleph Alpha does not currently support streaming.")

    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        raise NotImplementedError("Aleph Alpha does not currently support chat.")

    defachat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        raise NotImplementedError("Aleph Alpha does not currently support chat.")

    defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        raise NotImplementedError("Aleph Alpha does not currently support chat.")

    defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        raise NotImplementedError("Aleph Alpha does not currently support streaming.")

```
 |  
| --- | --- |  
options: members: - AlephAlpha
