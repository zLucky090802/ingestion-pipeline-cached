# Yi
##  Yi [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/yi/#llama_index.llms.yi.Yi "Permanent link")
Bases: 
Yi LLM.
Examples:
`pip install llama-index-llms-yi`

```
fromllama_index.llms.yiimport Yi

# get api key from: https://platform.01.ai/
llm = Yi(model="yi-large", api_key="YOUR_API_KEY")

response = llm.complete("Hi, who are you?")
print(response)

```

Source code in `llama-index-integrations/llms/llama-index-llms-yi/llama_index/llms/yi/base.py`  
| 
```
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
```
 | 
```
classYi(OpenAI):
"""
    Yi LLM.

    Examples:
        `pip install llama-index-llms-yi`

        ```python
        from llama_index.llms.yi import Yi

        # get api key from: https://platform.01.ai/
        llm = Yi(model="yi-large", api_key="YOUR_API_KEY")

        response = llm.complete("Hi, who are you?")
        print(response)
        ```

    """

    model: str = Field(default=DEFAULT_YI_MODEL, description="The Yi model to use.")
    context_window: int = Field(
        default=yi_modelname_to_context_size(DEFAULT_YI_MODEL),
        description=LLMMetadata.model_fields["context_window"].description,
    )
    is_chat_model: bool = Field(
        default=True,
        description=LLMMetadata.model_fields["is_chat_model"].description,
    )
    is_function_calling_model: bool = Field(
        default=False,
        description=LLMMetadata.model_fields["is_function_calling_model"].description,
    )
    tokenizer: Union[Tokenizer, str, None] = Field(
        default=None,
        description=(
            "An instance of a tokenizer object that has an encode method, or the name"
            " of a tokenizer model from Hugging Face. If left as None, then this"
            " disables inference of max_tokens."
        ),
    )

    def__init__(
        self,
        model: str = DEFAULT_YI_MODEL,
        api_key: Optional[str] = None,
        api_base: Optional[str] = DEFAULT_YI_ENDPOINT,
        **kwargs: Any,
    ) -> None:
        api_key = api_key or os.environ.get("YI_API_KEY", None)
        super().__init__(
            model=model,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
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
            return AutoTokenizer.from_pretrained(self.tokenizer)
        return self.tokenizer

    @classmethod
    defclass_name(cls) -> str:
        return "Yi_LLM"

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
###  complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/yi/#llama_index.llms.yi.Yi.complete "Permanent link")

```
complete(
    prompt: , formatted:  = False, **kwargs: 
) -> 

```

Complete the prompt.
Source code in `llama-index-integrations/llms/llama-index-llms-yi/llama_index/llms/yi/base.py`  
| 
```
118
119
120
121
122
123
124
125
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
###  stream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/yi/#llama_index.llms.yi.Yi.stream_complete "Permanent link")

```
stream_complete(
    prompt: , formatted:  = False, **kwargs: 
) -> CompletionResponseGen

```

Stream complete the prompt.
Source code in `llama-index-integrations/llms/llama-index-llms-yi/llama_index/llms/yi/base.py`  
| 
```
127
128
129
130
131
132
133
134
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
###  chat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/yi/#llama_index.llms.yi.Yi.chat "Permanent link")

```
chat(
    messages: Sequence[], **kwargs: 
) -> 

```

Chat with the model.
Source code in `llama-index-integrations/llms/llama-index-llms-yi/llama_index/llms/yi/base.py`  
| 
```
136
137
138
139
140
141
142
143
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
###  acomplete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/yi/#llama_index.llms.yi.Yi.acomplete "Permanent link")

```
acomplete(
    prompt: , formatted:  = False, **kwargs: 
) -> 

```

Complete the prompt.
Source code in `llama-index-integrations/llms/llama-index-llms-yi/llama_index/llms/yi/base.py`  
| 
```
157
158
159
160
161
162
163
164
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
###  astream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/yi/#llama_index.llms.yi.Yi.astream_complete "Permanent link")

```
astream_complete(
    prompt: , formatted:  = False, **kwargs: 
) -> CompletionResponseAsyncGen

```

Stream complete the prompt.
Source code in `llama-index-integrations/llms/llama-index-llms-yi/llama_index/llms/yi/base.py`  
| 
```
166
167
168
169
170
171
172
173
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
###  achat [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/yi/#llama_index.llms.yi.Yi.achat "Permanent link")

```
achat(
    messages: Sequence[], **kwargs: 
) -> 

```

Chat with the model.
Source code in `llama-index-integrations/llms/llama-index-llms-yi/llama_index/llms/yi/base.py`  
| 
```
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
options: members: - Yi
