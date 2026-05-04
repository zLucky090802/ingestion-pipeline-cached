# Portkey
##  Portkey [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/portkey/#llama_index.llms.portkey.Portkey "Permanent link")
Bases: `CustomLLM`
Portkey LLM.
Examples:
`pip install llama-index-llms-portkey`

```
# Importing necessary libraries and modules
fromllama_index.llms.portkeyimport Portkey
fromllama_index.core.llmsimport ChatMessage
importportkeyaspk

# Setting up Portkey API Key
importos
os.environ["PORTKEY_API_KEY"] = "YOUR_PORTKEY_API_KEY"

# Setting up Virtual Keys for OpenAI
openai_virtual_key_a = "YOUR_OPENAI_VIRTUAL_KEY_A"
openai_virtual_key_b = "YOUR_OPENAI_VIRTUAL_KEY_B"

# Creating an instance of Portkey with required configurations
portkey_client = Portkey(api_key=os.environ.get("PORTKEY_API_KEY"), mode="single")

# Configuring an LLM option for OpenAI with semantic caching
openai_llm = pk.LLMOptions(
    provider="openai",
    model="gpt-3.5-turbo",
    virtual_key=openai_virtual_key_a,
    cache_status="semantic",
)

# Adding the LLM option to the Portkey client
portkey_client.add_llms(openai_llm)

# Defining chat messages for testing
current_messages = [
    ChatMessage(role="system", content="You are a helpful assistant"),
    ChatMessage(role="user", content="What are the ingredients of a pizza?"),
]

# Testing Portkey Semantic Cache
response = portkey_client.chat(current_messages)
print(str(response))

```

Source code in `llama-index-integrations/llms/llama-index-llms-portkey/llama_index/llms/portkey/base.py`  
| 
```
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
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
```
 | 
```
classPortkey(CustomLLM):
"""
    Portkey LLM.

    Examples:
        `pip install llama-index-llms-portkey`

        ```python
        # Importing necessary libraries and modules
        from llama_index.llms.portkey import Portkey
        from llama_index.core.llms import ChatMessage
        import portkey as pk

        # Setting up Portkey API Key
        import os
        os.environ["PORTKEY_API_KEY"] = "YOUR_PORTKEY_API_KEY"

        # Setting up Virtual Keys for OpenAI
        openai_virtual_key_a = "YOUR_OPENAI_VIRTUAL_KEY_A"
        openai_virtual_key_b = "YOUR_OPENAI_VIRTUAL_KEY_B"

        # Creating an instance of Portkey with required configurations
        portkey_client = Portkey(api_key=os.environ.get("PORTKEY_API_KEY"), mode="single")

        # Configuring an LLM option for OpenAI with semantic caching
        openai_llm = pk.LLMOptions(
            provider="openai",
            model="gpt-3.5-turbo",
            virtual_key=openai_virtual_key_a,
            cache_status="semantic",


        # Adding the LLM option to the Portkey client
        portkey_client.add_llms(openai_llm)

        # Defining chat messages for testing
        current_messages = [
            ChatMessage(role="system", content="You are a helpful assistant"),
            ChatMessage(role="user", content="What are the ingredients of a pizza?"),


        # Testing Portkey Semantic Cache
        response = portkey_client.chat(current_messages)
        print(str(response))
        ```

    """

    mode: Optional[Union["Modes", "ModesLiteral"]] = Field(
        description="The mode for using the Portkey integration"
    )

    model: Optional[str] = Field(default=DEFAULT_PORTKEY_MODEL)
    llm: "LLMOptions" = Field(description="LLM parameter", default_factory=dict)

    llms: List["LLMOptions"] = Field(description="LLM parameters", default_factory=list)

    _client: Any = PrivateAttr()

    def__init__(
        self,
        *,
        mode: Union["Modes", "ModesLiteral"],
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
    ) -> None:
"""
        Initialize a Portkey instance.

        Args:
            mode (Optional[Modes]): The mode for using the Portkey integration
            (default: Modes.SINGLE).
            api_key (Optional[str]): The API key to authenticate with Portkey.
            base_url (Optional[str]): The Base url to the self hosted rubeus \
                (the opensource version of portkey) or any other self hosted server.

        """
        try:
            importportkey
        except ImportError as exc:
            raise ImportError(IMPORT_ERROR_MESSAGE) fromexc

        super().__init__(
            base_url=base_url,
            api_key=api_key,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )
        if api_key is not None:
            portkey.api_key = api_key

        if base_url is not None:
            portkey.base_url = base_url

        portkey.mode = mode

        self._client = portkey
        self.model = None
        self.mode = mode

    @property
    defmetadata(self) -> LLMMetadata:
"""LLM metadata."""
        return generate_llm_metadata(self.llms[0])

    defadd_llms(
        self, llm_params: Union["LLMOptions", List["LLMOptions"]]
    ) -> "Portkey":
"""
        Adds the specified LLM parameters to the list of LLMs. This may be used for
        fallbacks or load-balancing as specified in the mode.

        Args:
            llm_params (Union[LLMOptions, List[LLMOptions]]): A single LLM parameter \
            set or a list of LLM parameter sets. Each set should be an instance of \
            LLMOptions with
            the specified attributes.
                > provider: Optional[ProviderTypes]
                > model: str
                > temperature: float
                > max_tokens: Optional[int]
                > max_retries: int
                > trace_id: Optional[str]
                > cache_status: Optional[CacheType]
                > cache: Optional[bool]
                > metadata: Dict[str, Any]
                > weight: Optional[float]
                > **kwargs : Other additional parameters that are supported by \
                    LLMOptions in portkey-ai

            NOTE: User may choose to pass additional params as well.

        Returns:
            self

        """
        try:
            fromportkeyimport LLMOptions
        except ImportError as exc:
            raise ImportError(IMPORT_ERROR_MESSAGE) fromexc
        if isinstance(llm_params, LLMOptions):
            llm_params = [llm_params]
        self.llms.extend(llm_params)
        if self.model is None:
            self.model = self.llms[0].model
        return self

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
"""Completion endpoint for LLM."""
        if self._is_chat_model:
            complete_fn = chat_to_completion_decorator(self._chat)
        else:
            complete_fn = self._complete
        return complete_fn(prompt, **kwargs)

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        if self._is_chat_model:
            chat_fn = self._chat
        else:
            chat_fn = completion_to_chat_decorator(self._complete)
        return chat_fn(messages, **kwargs)

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
"""Completion endpoint for LLM."""
        if self._is_chat_model:
            complete_fn = stream_chat_to_completion_decorator(self._stream_chat)
        else:
            complete_fn = self._stream_complete
        return complete_fn(prompt, **kwargs)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        if self._is_chat_model:
            stream_chat_fn = self._stream_chat
        else:
            stream_chat_fn = stream_completion_to_chat_decorator(self._stream_complete)
        return stream_chat_fn(messages, **kwargs)

    def_chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        try:
            fromportkeyimport Config, Message
        except ImportError as exc:
            raise ImportError(IMPORT_ERROR_MESSAGE) fromexc
        _messages = cast(
            List[Message],
            [{"role": i.role.value, "content": i.content} for i in messages],
        )
        config = Config(llms=self.llms)
        response = self._client.ChatCompletions.create(
            messages=_messages, config=config
        )
        self.llm = self._get_llm(response)

        message = response.choices[0].message
        return ChatResponse(message=message, raw=response)

    def_complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        try:
            fromportkeyimport Config
        except ImportError as exc:
            raise ImportError(IMPORT_ERROR_MESSAGE) fromexc

        config = Config(llms=self.llms)
        response = self._client.Completions.create(prompt=prompt, config=config)
        text = response.choices[0].text
        return CompletionResponse(text=text, raw=response)

    def_stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        try:
            fromportkeyimport Config, Message
        except ImportError as exc:
            raise ImportError(IMPORT_ERROR_MESSAGE) fromexc
        _messages = cast(
            List[Message],
            [{"role": i.role.value, "content": i.content} for i in messages],
        )
        config = Config(llms=self.llms)
        response = self._client.ChatCompletions.create(
            messages=_messages, config=config, stream=True, **kwargs
        )

        defgen() -> ChatResponseGen:
            content = ""
            function_call: Optional[dict] = {}
            for resp in response:
                if resp.choices is None:
                    continue
                delta = resp.choices[0].delta
                role = delta.get("role", "assistant")
                content_delta = delta.get("content", "") or ""
                content += content_delta

                function_call_delta = delta.get("function_call", None)
                if function_call_delta is not None:
                    if function_call is None:
                        function_call = function_call_delta
                        # ensure we do not add a blank function call
                        if (
                            function_call
                            and function_call.get("function_name", "") is None
                        ):
                            del function_call["function_name"]
                    else:
                        function_call["arguments"] += function_call_delta["arguments"]

                additional_kwargs = {}
                if function_call is not None:
                    additional_kwargs["function_call"] = function_call

                yield ChatResponse(
                    message=ChatMessage(
                        role=role,
                        content=content,
                        additional_kwargs=additional_kwargs,
                    ),
                    delta=content_delta,
                    raw=resp,
                )

        return gen()

    def_stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        try:
            fromportkeyimport Config
        except ImportError as exc:
            raise ImportError(IMPORT_ERROR_MESSAGE) fromexc

        config = Config(llms=self.llms)
        response = self._client.Completions.create(
            prompt=prompt, config=config, stream=True, **kwargs
        )

        defgen() -> CompletionResponseGen:
            text = ""
            for resp in response:
                delta = resp.choices[0].text or ""
                text += delta
                yield CompletionResponse(
                    delta=delta,
                    text=text,
                    raw=resp,
                )

        return gen()

    @property
    def_is_chat_model(self) -> bool:
"""
        Check if a given model is a chat-based language model.

        Returns:
            bool: True if the provided model is a chat-based language model,
            False otherwise.

        """
        return is_chat_model(self.model or "")

    def_get_llm(self, response: "PortkeyResponse") -> "LLMOptions":
        return get_llm(response, self.llms)

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/portkey/#llama_index.llms.portkey.Portkey.metadata "Permanent link")

```
metadata: 

```

LLM metadata.
###  add_llms [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/portkey/#llama_index.llms.portkey.Portkey.add_llms "Permanent link")

```
add_llms(
    llm_params: Union[LLMOptions, [LLMOptions]]
) -> 

```

Adds the specified LLM parameters to the list of LLMs. This may be used for fallbacks or load-balancing as specified in the mode.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `llm_params`  |  `Union[LLMOptions, List[LLMOptions]]`  |  A single LLM parameter set or a list of LLM parameter sets. Each set should be an instance of LLMOptions with  |  _required_  |  
|  `NOTE`  |  User may choose to pass additional params as well.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  self  |  
Source code in `llama-index-integrations/llms/llama-index-llms-portkey/llama_index/llms/portkey/base.py`  
| 
```
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
```
 | 
```
defadd_llms(
    self, llm_params: Union["LLMOptions", List["LLMOptions"]]
) -> "Portkey":
"""
    Adds the specified LLM parameters to the list of LLMs. This may be used for
    fallbacks or load-balancing as specified in the mode.

    Args:
        llm_params (Union[LLMOptions, List[LLMOptions]]): A single LLM parameter \
        set or a list of LLM parameter sets. Each set should be an instance of \
        LLMOptions with
        the specified attributes.
            > provider: Optional[ProviderTypes]
            > model: str
            > temperature: float
            > max_tokens: Optional[int]
            > max_retries: int
            > trace_id: Optional[str]
            > cache_status: Optional[CacheType]
            > cache: Optional[bool]
            > metadata: Dict[str, Any]
            > weight: Optional[float]
            > **kwargs : Other additional parameters that are supported by \
                LLMOptions in portkey-ai

        NOTE: User may choose to pass additional params as well.

    Returns:
        self

    """
    try:
        fromportkeyimport LLMOptions
    except ImportError as exc:
        raise ImportError(IMPORT_ERROR_MESSAGE) fromexc
    if isinstance(llm_params, LLMOptions):
        llm_params = [llm_params]
    self.llms.extend(llm_params)
    if self.model is None:
        self.model = self.llms[0].model
    return self

```
 |  
| --- | --- |  
###  complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/portkey/#llama_index.llms.portkey.Portkey.complete "Permanent link")

```
complete(
    prompt: , formatted:  = False, **kwargs: 
) -> 

```

Completion endpoint for LLM.
Source code in `llama-index-integrations/llms/llama-index-llms-portkey/llama_index/llms/portkey/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defcomplete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponse:
"""Completion endpoint for LLM."""
    if self._is_chat_model:
        complete_fn = chat_to_completion_decorator(self._chat)
    else:
        complete_fn = self._complete
    return complete_fn(prompt, **kwargs)

```
 |  
| --- | --- |  
###  stream_complete [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/portkey/#llama_index.llms.portkey.Portkey.stream_complete "Permanent link")

```
stream_complete(
    prompt: , formatted:  = False, **kwargs: 
) -> CompletionResponseGen

```

Completion endpoint for LLM.
Source code in `llama-index-integrations/llms/llama-index-llms-portkey/llama_index/llms/portkey/base.py`  
| 
```
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
```
 | 
```
@llm_completion_callback()
defstream_complete(
    self, prompt: str, formatted: bool = False, **kwargs: Any
) -> CompletionResponseGen:
"""Completion endpoint for LLM."""
    if self._is_chat_model:
        complete_fn = stream_chat_to_completion_decorator(self._stream_chat)
    else:
        complete_fn = self._stream_complete
    return complete_fn(prompt, **kwargs)

```
 |  
| --- | --- |  
options: members: - Portkey
