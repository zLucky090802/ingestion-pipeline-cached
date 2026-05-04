# Openai like
##  OpenAILike [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai_like/#llama_index.llms.openai_like.OpenAILike "Permanent link")
Bases: 
OpenaAILike LLM.
OpenAILike is a thin wrapper around the OpenAI model that makes it compatible with 3rd party tools that provide an openai-compatible api.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model`  |  The model to use for the api.  |  `DEFAULT_OPENAI_MODEL`  |  
|  `api_base`  |  The base url to use for the api. Defaults to "https://api.openai.com/v1".  |  `None`  |  
|  `is_chat_model`  |  `bool`  |  Whether the model uses the chat or completion endpoint. Defaults to False.  |  _required_  |  
|  `is_function_calling_model`  |  `bool`  |  Whether the model supports OpenAI function calling/tools over the API. Defaults to False.  |  _required_  |  
|  `api_key`  |  The api key to use for the api. Set this to some random string if your API does not require an api key.  |  `None`  |  
|  `context_window`  |  The context window to use for the api. Set this to your model's context window for the best experience. Defaults to 3900.  |  _required_  |  
|  `max_tokens`  |  The max number of tokens to generate. Defaults to None.  |  `None`  |  
|  `temperature`  |  `float`  |  The temperature to use for the api. Default is 0.1.  |  `DEFAULT_TEMPERATURE`  |  
|  `additional_kwargs`  |  `dict`  |  Specify additional parameters to the request body.  |  `None`  |  
|  `max_retries`  |  How many times to retry the API call if it fails. Defaults to 3.  |  
|  `timeout`  |  `float`  |  How long to wait, in seconds, for an API call before failing. Defaults to 60.0.  |  `60.0`  |  
|  `reuse_client`  |  `bool`  |  Reuse the OpenAI client between requests. Defaults to True.  |  `True`  |  
|  `default_headers`  |  `dict`  |  Override the default headers for API requests. Defaults to None.  |  `None`  |  
|  `http_client`  |  `Client`  |  Pass in your own httpx.Client instance. Defaults to None.  |  `None`  |  
|  `async_http_client`  |  `AsyncClient`  |  Pass in your own httpx.AsyncClient instance. Defaults to None.  |  `None`  |  
Examples:
`pip install llama-index-llms-openai-like`

```
fromllama_index.llms.openai_likeimport OpenAILike

llm = OpenAILike(
    model="my model",
    api_base="https://hostname.com/v1",
    api_key="fake",
    context_window=128000,
    is_chat_model=True,
    is_function_calling_model=False,
)

response = llm.complete("Hello World!")
print(str(response))

```

Source code in `llama-index-integrations/llms/llama-index-llms-openai-like/llama_index/llms/openai_like/base.py`  
| 
```
 23
 24
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
```
 | 
```
classOpenAILike(OpenAI):
"""
    OpenaAILike LLM.

    OpenAILike is a thin wrapper around the OpenAI model that makes it compatible with
    3rd party tools that provide an openai-compatible api.

    Args:
        model (str):
            The model to use for the api.
        api_base (str):
            The base url to use for the api.
            Defaults to "https://api.openai.com/v1".
        is_chat_model (bool):
            Whether the model uses the chat or completion endpoint.
            Defaults to False.
        is_function_calling_model (bool):
            Whether the model supports OpenAI function calling/tools over the API.
            Defaults to False.
        api_key (str):
            The api key to use for the api.
            Set this to some random string if your API does not require an api key.
        context_window (int):
            The context window to use for the api. Set this to your model's context window for the best experience.
            Defaults to 3900.
        max_tokens (int):
            The max number of tokens to generate.
            Defaults to None.
        temperature (float):
            The temperature to use for the api.
            Default is 0.1.
        additional_kwargs (dict):
            Specify additional parameters to the request body.
        max_retries (int):
            How many times to retry the API call if it fails.
            Defaults to 3.
        timeout (float):
            How long to wait, in seconds, for an API call before failing.
            Defaults to 60.0.
        reuse_client (bool):
            Reuse the OpenAI client between requests.
            Defaults to True.
        default_headers (dict):
            Override the default headers for API requests.
            Defaults to None.
        http_client (httpx.Client):
            Pass in your own httpx.Client instance.
            Defaults to None.
        async_http_client (httpx.AsyncClient):
            Pass in your own httpx.AsyncClient instance.
            Defaults to None.

    Examples:
        `pip install llama-index-llms-openai-like`

        ```python
        from llama_index.llms.openai_like import OpenAILike

        llm = OpenAILike(
            model="my model",
            api_base="https://hostname.com/v1",
            api_key="fake",
            context_window=128000,
            is_chat_model=True,
            is_function_calling_model=False,


        response = llm.complete("Hello World!")
        print(str(response))
        ```

    """

    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description=LLMMetadata.model_fields["context_window"].description,
    )
    is_chat_model: bool = Field(
        default=False,
        description=LLMMetadata.model_fields["is_chat_model"].description,
    )
    is_function_calling_model: bool = Field(
        default=False,
        description=LLMMetadata.model_fields["is_function_calling_model"].description,
    )
    should_use_structured_outputs: bool = Field(
        default=False,
        # https://platform.openai.com/docs/guides/structured-outputs
        description=(
            "Set True if the model supports structured output through response_format."
        ),
    )
    tokenizer: Union[Tokenizer, str, None] = Field(
        default=None,
        description=(
            "An instance of a tokenizer object that has an encode method, or the name"
            " of a tokenizer model from Hugging Face. If left as None, then this"
            " disables inference of max_tokens."
        ),
    )

    defmodel_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        if isinstance(self.tokenizer, str):
            try:
                importtransformers  # noqa: F401
            except ImportError:
                raise ImportError(
                    "The `transformers` package is required when passing a string "
                    "tokenizer name. Install it with: "
                    "`pip install llama-index-llms-openai-like[transformers]`"
                )

    @property
    defmetadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.max_tokens or -1,
            is_chat_model=self.is_chat_model,
            is_function_calling_model=self.is_function_calling_model,
            model_name=self.model,
        )

    @property
    def_tokenizer(self) -> Optional[Tokenizer]:
        if isinstance(self.tokenizer, str):
            fromtransformersimport AutoTokenizer

            return AutoTokenizer.from_pretrained(self.tokenizer)
        return self.tokenizer

    @classmethod
    defclass_name(cls) -> str:
        return "OpenAILike"

    def_should_use_structure_outputs(self) -> bool:
        return self.should_use_structured_outputs

    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
"""Complete the prompt."""
        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        return super().complete(prompt, **kwargs)

    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
"""Stream complete the prompt."""
        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        return super().stream_complete(prompt, **kwargs)

    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
"""Chat with the model."""
        if not self.metadata.is_chat_model:
            prompt = self.messages_to_prompt(messages)
            completion_response = self.complete(prompt, formatted=True, **kwargs)
            return completion_response_to_chat_response(completion_response)

        return super().chat(messages, **kwargs)

    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        if not self.metadata.is_chat_model:
            prompt = self.messages_to_prompt(messages)
            completion_response = self.stream_complete(prompt, formatted=True, **kwargs)
            return stream_completion_response_to_chat_response(completion_response)

        return super().stream_chat(messages, **kwargs)

    # -- Async methods --

    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
"""Complete the prompt."""
        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        return await super().acomplete(prompt, **kwargs)

    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
"""Stream complete the prompt."""
        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        return await super().astream_complete(prompt, **kwargs)

    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
"""Chat with the model."""
        if not self.metadata.is_chat_model:
            prompt = self.messages_to_prompt(messages)
            completion_response = await self.acomplete(prompt, formatted=True, **kwargs)
            return completion_response_to_chat_response(completion_response)

        return await super().achat(messages, **kwargs)

    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        if not self.metadata.is_chat_model:
            prompt = self.messages_to_prompt(messages)
            completion_response = await self.astream_complete(
                prompt, formatted=True, **kwargs
            )
            return async_stream_completion_response_to_chat_response(
                completion_response
            )

        return await super().astream_chat(messages, **kwargs)

```
 |  
| --- | --- |  
###  complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai_like/#llama_index.llms.openai_like.OpenAILike.complete "Permanent link")

```
complete(
    prompt: , formatted:  = False, **kwargs: 
) -> 

```

Complete the prompt.
Source code in `llama-index-integrations/llms/llama-index-llms-openai-like/llama_index/llms/openai_like/base.py`  
| 
```
161
162
163
164
165
166
167
168
```
 | 
```
defcomplete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponse:
"""Complete the prompt."""
    if not formatted:
        prompt = self.completion_to_prompt(prompt)

    return super().complete(prompt, **kwargs)

```
 |  
| --- | --- |  
###  stream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai_like/#llama_index.llms.openai_like.OpenAILike.stream_complete "Permanent link")

```
stream_complete(
    prompt: , formatted:  = False, **kwargs: 
) -> CompletionResponseGen

```

Stream complete the prompt.
Source code in `llama-index-integrations/llms/llama-index-llms-openai-like/llama_index/llms/openai_like/base.py`  
| 
```
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
defstream_complete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponseGen:
"""Stream complete the prompt."""
    if not formatted:
        prompt = self.completion_to_prompt(prompt)

    return super().stream_complete(prompt, **kwargs)

```
 |  
| --- | --- |  
###  chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai_like/#llama_index.llms.openai_like.OpenAILike.chat "Permanent link")

```
chat(
    messages: Sequence[], **kwargs: 
) -> 

```

Chat with the model.
Source code in `llama-index-integrations/llms/llama-index-llms-openai-like/llama_index/llms/openai_like/base.py`  
| 
```
179
180
181
182
183
184
185
186
```
 | 
```
defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
"""Chat with the model."""
    if not self.metadata.is_chat_model:
        prompt = self.messages_to_prompt(messages)
        completion_response = self.complete(prompt, formatted=True, **kwargs)
        return completion_response_to_chat_response(completion_response)

    return super().chat(messages, **kwargs)

```
 |  
| --- | --- |  
###  acomplete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai_like/#llama_index.llms.openai_like.OpenAILike.acomplete "Permanent link")

```
acomplete(
    prompt: , formatted:  = False, **kwargs: 
) -> 

```

Complete the prompt.
Source code in `llama-index-integrations/llms/llama-index-llms-openai-like/llama_index/llms/openai_like/base.py`  
| 
```
200
201
202
203
204
205
206
207
```
 | 
```
async defacomplete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponse:
"""Complete the prompt."""
    if not formatted:
        prompt = self.completion_to_prompt(prompt)

    return await super().acomplete(prompt, **kwargs)

```
 |  
| --- | --- |  
###  astream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai_like/#llama_index.llms.openai_like.OpenAILike.astream_complete "Permanent link")

```
astream_complete(
    prompt: , formatted:  = False, **kwargs: 
) -> CompletionResponseAsyncGen

```

Stream complete the prompt.
Source code in `llama-index-integrations/llms/llama-index-llms-openai-like/llama_index/llms/openai_like/base.py`  
| 
```
209
210
211
212
213
214
215
216
```
 | 
```
async defastream_complete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponseAsyncGen:
"""Stream complete the prompt."""
    if not formatted:
        prompt = self.completion_to_prompt(prompt)

    return await super().astream_complete(prompt, **kwargs)

```
 |  
| --- | --- |  
###  achat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/openai_like/#llama_index.llms.openai_like.OpenAILike.achat "Permanent link")

```
achat(
    messages: Sequence[], **kwargs: 
) -> 

```

Chat with the model.
Source code in `llama-index-integrations/llms/llama-index-llms-openai-like/llama_index/llms/openai_like/base.py`  
| 
```
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
```
 | 
```
async defachat(
    self, messages: Sequence[ChatMessage], **kwargs: Any
) -> ChatResponse:
"""Chat with the model."""
    if not self.metadata.is_chat_model:
        prompt = self.messages_to_prompt(messages)
        completion_response = await self.acomplete(prompt, formatted=True, **kwargs)
        return completion_response_to_chat_response(completion_response)

    return await super().achat(messages, **kwargs)

```
 |  
| --- | --- |  
options: members: - OpenAILike
