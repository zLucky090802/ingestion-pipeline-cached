# Clarifai
##  Clarifai [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/clarifai/#llama_index.llms.clarifai.Clarifai "Permanent link")
Bases: 
Clarifai LLM.
Examples:
`pip install llama-index-llms-clarifai`

```
fromllama_index.llms.clarifaiimport Clarifai

llm = Clarifai(
    user_id="clarifai",
    app_id="ml",
    model_name="llama2-7b-alternative-4k",
    model_url=(
        "https://clarifai.com/clarifai/ml/models/llama2-7b-alternative-4k"
)

response = llm.complete("Hello World!")
print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-clarifai/llama_index/llms/clarifai/base.py`  
| 
```
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
```
 | 
```
classClarifai(LLM):
"""
    Clarifai LLM.

    Examples:
        `pip install llama-index-llms-clarifai`

        ```python
        from llama_index.llms.clarifai import Clarifai

        llm = Clarifai(
            user_id="clarifai",
            app_id="ml",
            model_name="llama2-7b-alternative-4k",
            model_url=(
                "https://clarifai.com/clarifai/ml/models/llama2-7b-alternative-4k"


        response = llm.complete("Hello World!")
        print(response)
        ```

    """

    model_url: Optional[str] = Field(
        description=f"Full URL of the model. e.g. `{EXAMPLE_URL}`"
    )
    model_version_id: Optional[str] = Field(description="Model Version ID.")
    app_id: Optional[str] = Field(description="Clarifai application ID of the model.")
    user_id: Optional[str] = Field(description="Clarifai user ID of the model.")
    pat: Optional[str] = Field(
        description="Personal Access Tokens(PAT) to validate requests."
    )

    _model: Any = PrivateAttr()
    _is_chat_model: bool = PrivateAttr()

    def__init__(
        self,
        model_name: Optional[str] = None,
        model_url: Optional[str] = None,
        model_version_id: Optional[str] = "",
        app_id: Optional[str] = None,
        user_id: Optional[str] = None,
        pat: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 512,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
    ):
        if pat is None and os.environ.get("CLARIFAI_PAT") is not None:
            pat = os.environ.get("CLARIFAI_PAT")

        if not pat and os.environ.get("CLARIFAI_PAT") is None:
            raise ValueError(
                "Set `CLARIFAI_PAT` as env variable or pass `pat` as constructor argument"
            )

        if model_url is not None and model_name is not None:
            raise ValueError("You can only specify one of model_url or model_name.")
        if model_url is None and model_name is None:
            raise ValueError("You must specify one of model_url or model_name.")

        model = None
        if model_name is not None:
            if app_id is None or user_id is None:
                raise ValueError(
                    f"Missing one app ID or user ID of the model: {app_id=}, {user_id=}"
                )
            else:
                model = Model(
                    user_id=user_id,
                    app_id=app_id,
                    model_id=model_name,
                    model_version={"id": model_version_id},
                    pat=pat,
                )

        if model_url is not None:
            model = Model(model_url, pat=pat)
            model_name = model.id

        is_chat_model = False
        if "chat" in model.app_id or "chat" in model.id:
            is_chat_model = True

        additional_kwargs = additional_kwargs or {}

        super().__init__(
            temperature=temperature,
            max_tokens=max_tokens,
            additional_kwargs=additional_kwargs,
            callback_manager=callback_manager,
            model_name=model_name,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )
        self._model = model
        self._is_chat_model = is_chat_model

    @classmethod
    defclass_name(cls) -> str:
        return "ClarifaiLLM"

    @property
    defmetadata(self) -> LLMMetadata:
"""LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.max_tokens,
            model_name=self._model,
            is_chat_model=self._is_chat_model,
        )

    # TODO: When the Clarifai python SDK supports inference params, add here.
    defchat(
        self,
        messages: Sequence[ChatMessage],
        inference_params: Optional[Dict] = {},
        **kwargs: Any,
    ) -> ChatResponse:
"""Chat endpoint for LLM."""
        prompt = "".join([str(m) for m in messages])
        try:
            response = (
                self._model.predict_by_bytes(
                    input_bytes=prompt.encode(encoding="UTF-8"),
                    input_type="text",
                    inference_params=inference_params,
                )
                .outputs[0]
                .data.text.raw
            )
        except Exception as e:
            raise Exception(f"Prediction failed: {e}")
        return ChatResponse(message=ChatMessage(content=response))

    defcomplete(
        self,
        prompt: str,
        formatted: bool = False,
        inference_params: Optional[Dict] = {},
        **kwargs: Any,
    ) -> CompletionResponse:
"""Completion endpoint for LLM."""
        try:
            response = (
                self._model.predict_by_bytes(
                    input_bytes=prompt.encode(encoding="utf-8"),
                    input_type="text",
                    inference_params=inference_params,
                )
                .outputs[0]
                .data.text.raw
            )
        except Exception as e:
            raise Exception(f"Prediction failed: {e}")
        return CompletionResponse(text=response)

    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        raise NotImplementedError(
            "Clarifai does not currently support streaming completion."
        )

    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        raise NotImplementedError(
            "Clarifai does not currently support streaming completion."
        )

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        raise NotImplementedError("Currently not supported.")

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        return self.complete(prompt, **kwargs)

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        raise NotImplementedError("Currently not supported.")

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        raise NotImplementedError("Clarifai does not currently support this function.")

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/clarifai/#llama_index.llms.clarifai.Clarifai.metadata "Permanent link")

```
metadata: 

```

LLM metadata.
###  chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/clarifai/#llama_index.llms.clarifai.Clarifai.chat "Permanent link")

```
chat(
    messages: Sequence[],
    inference_params: Optional[] = {},
    **kwargs: 
) -> 

```

Chat endpoint for LLM.
Source code in `llama-index-integrations/llms/llama-index-llms-clarifai/llama_index/llms/clarifai/base.py`  
| 
```
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
```
 | 
```
defchat(
    self,
    messages: Sequence[ChatMessage],
    inference_params: Optional[Dict] = {},
    **kwargs: Any,
) -> ChatResponse:
"""Chat endpoint for LLM."""
    prompt = "".join([str(m) for m in messages])
    try:
        response = (
            self._model.predict_by_bytes(
                input_bytes=prompt.encode(encoding="UTF-8"),
                input_type="text",
                inference_params=inference_params,
            )
            .outputs[0]
            .data.text.raw
        )
    except Exception as e:
        raise Exception(f"Prediction failed: {e}")
    return ChatResponse(message=ChatMessage(content=response))

```
 |  
| --- | --- |  
###  complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/clarifai/#llama_index.llms.clarifai.Clarifai.complete "Permanent link")

```
complete(
    prompt: ,
    formatted:  = False,
    inference_params: Optional[] = {},
    **kwargs: 
) -> 

```

Completion endpoint for LLM.
Source code in `llama-index-integrations/llms/llama-index-llms-clarifai/llama_index/llms/clarifai/base.py`  
| 
```
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
```
 | 
```
defcomplete(
    self,
    prompt: str,
    formatted: bool = False,
    inference_params: Optional[Dict] = {},
    **kwargs: Any,
) -> CompletionResponse:
"""Completion endpoint for LLM."""
    try:
        response = (
            self._model.predict_by_bytes(
                input_bytes=prompt.encode(encoding="utf-8"),
                input_type="text",
                inference_params=inference_params,
            )
            .outputs[0]
            .data.text.raw
        )
    except Exception as e:
        raise Exception(f"Prediction failed: {e}")
    return CompletionResponse(text=response)

```
 |  
| --- | --- |  
options: members: - Clarifai
