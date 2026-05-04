# Langchain
##  LangChainLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/langchain/#llama_index.llms.langchain.LangChainLLM "Permanent link")
Bases: 
Adapter for a LangChain LLM.
Examples:
`pip install llama-index-llms-langchain`

```
fromlangchain_openaiimport ChatOpenAI

fromllama_index.llms.langchainimport LangChainLLM

llm = LangChainLLM(llm=ChatOpenAI(...))

response_gen = llm.stream_complete("What is the meaning of life?")

for r in response_gen:
    print(r.delta, end="")

```

Source code in `llama-index-integrations/llms/llama-index-llms-langchain/llama_index/llms/langchain/base.py`  
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
```
 | 
```
classLangChainLLM(LLM):
"""
    Adapter for a LangChain LLM.

    Examples:
        `pip install llama-index-llms-langchain`

        ```python
        from langchain_openai import ChatOpenAI

        from llama_index.llms.langchain import LangChainLLM

        llm = LangChainLLM(llm=ChatOpenAI(...))

        response_gen = llm.stream_complete("What is the meaning of life?")

        for r in response_gen:
            print(r.delta, end="")
        ```

    """

    _llm: Any = PrivateAttr()

    def__init__(
        self,
        llm: "BaseLanguageModel",
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
    ) -> None:
        super().__init__(
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )
        self._llm = llm

    @classmethod
    defclass_name(cls) -> str:
        return "LangChainLLM"

    @property
    defllm(self) -> "BaseLanguageModel":
        return self._llm

    @property
    defmetadata(self) -> LLMMetadata:
        fromllama_index.llms.langchain.utilsimport get_llm_metadata

        return get_llm_metadata(self._llm)

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        fromllama_index.llms.langchain.utilsimport (
            from_lc_messages,
            to_lc_messages,
        )

        if not self.metadata.is_chat_model:
            prompt = self.messages_to_prompt(messages)
            completion_response = self.complete(prompt, formatted=True, **kwargs)
            return completion_response_to_chat_response(completion_response)

        lc_messages = to_lc_messages(messages)
        lc_message = self._llm.invoke(input=lc_messages, **kwargs)
        message = from_lc_messages([lc_message])[0]
        return ChatResponse(message=message)

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        output_str = self._llm.invoke(prompt, **kwargs)
        if isinstance(output_str, AIMessage):
            output_str = output_str.content
        return CompletionResponse(text=output_str)

    @llm_chat_callback()
    defstream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        if not self.metadata.is_chat_model:
            prompt = self.messages_to_prompt(messages)
            stream_completion = self.stream_complete(prompt, formatted=True, **kwargs)
            return stream_completion_response_to_chat_response(stream_completion)

        if hasattr(self._llm, "stream"):

            defgen() -> Generator[ChatResponse, None, None]:
                fromllama_index.llms.langchain.utilsimport (
                    from_lc_messages,
                    to_lc_messages,
                )

                lc_messages = to_lc_messages(messages)
                response_str = ""
                for message in self._llm.stream(lc_messages, **kwargs):
                    message = from_lc_messages([message])[0]
                    delta = message.content or ""
                    response_str += delta
                    yield ChatResponse(
                        message=ChatMessage(role=message.role, content=response_str),
                        delta=delta,
                    )

            return gen()

        else:
            fromllama_index.core.langchain_helpers.streamingimport (
                StreamingGeneratorCallbackHandler,
            )

            handler = StreamingGeneratorCallbackHandler()

            if not hasattr(self._llm, "streaming"):
                raise ValueError("LLM must support streaming.")
            if not hasattr(self._llm, "callbacks"):
                raise ValueError("LLM must support callbacks to use streaming.")

            self._llm.callbacks = [handler]  # type: ignore
            self._llm.streaming = True  # type: ignore

            thread = Thread(target=self.chat, args=[messages], kwargs=kwargs)
            thread.start()

            response_gen = handler.get_response_gen()

            defgen() -> Generator[ChatResponse, None, None]:
                text = ""
                for delta in response_gen:
                    text += delta
                    yield ChatResponse(
                        message=ChatMessage(text=text),
                        delta=delta,
                    )

            return gen()

    @llm_completion_callback()
    defstream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        fromllama_index.core.langchain_helpers.streamingimport (
            StreamingGeneratorCallbackHandler,
        )

        handler = StreamingGeneratorCallbackHandler()

        if not hasattr(self._llm, "streaming"):
            raise ValueError("LLM must support streaming.")
        if not hasattr(self._llm, "callbacks"):
            raise ValueError("LLM must support callbacks to use streaming.")

        self._llm.callbacks = [handler]  # type: ignore
        self._llm.streaming = True  # type: ignore

        thread = Thread(target=self.complete, args=[prompt], kwargs=kwargs)
        thread.start()

        response_gen = handler.get_response_gen()

        defgen() -> Generator[CompletionResponse, None, None]:
            text = ""
            for delta in response_gen:
                text += delta
                yield CompletionResponse(delta=delta, text=text)

        return gen()

    @llm_chat_callback()
    async defachat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        # TODO: Implement async chat
        return self.chat(messages, **kwargs)

    @llm_completion_callback()
    async defacomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        # TODO: Implement async complete
        return self.complete(prompt, formatted=formatted, **kwargs)

    @llm_chat_callback()
    async defastream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        # TODO: Implement async stream_chat

        async defgen() -> ChatResponseAsyncGen:
            for message in self.stream_chat(messages, **kwargs):
                yield message

        return gen()

    @llm_completion_callback()
    async defastream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        # TODO: Implement async stream_complete

        async defgen() -> CompletionResponseAsyncGen:
            for response in self.stream_complete(prompt, formatted=formatted, **kwargs):
                yield response

        return gen()

```
 |  
| --- | --- |  
options: members: - LangChainLLM
