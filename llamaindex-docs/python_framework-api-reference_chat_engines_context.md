# Context
##  CondensePlusContextChatEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.CondensePlusContextChatEngine "Permanent link")
Bases: 
Condensed Conversation & Context Chat Engine.
First condense a conversation and latest user message to a standalone question Then build a context for the standalone question from a retriever, Then pass the context along with prompt and user message to LLM to generate a response.
Source code in `llama-index-core/llama_index/core/chat_engine/condense_plus_context.py`  
| 
```
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
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
```
 | 
```
classCondensePlusContextChatEngine(BaseChatEngine):
"""
    Condensed Conversation & Context Chat Engine.

    First condense a conversation and latest user message to a standalone question
    Then build a context for the standalone question from a retriever,
    Then pass the context along with prompt and user message to LLM to generate a response.
    """

    def__init__(
        self,
        retriever: BaseRetriever,
        llm: LLM,
        memory: BaseMemory,
        context_prompt: Optional[Union[str, PromptTemplate]] = None,
        context_refine_prompt: Optional[Union[str, PromptTemplate]] = None,
        condense_prompt: Optional[Union[str, PromptTemplate]] = None,
        system_prompt: Optional[str] = None,
        skip_condense: bool = False,
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
        callback_manager: Optional[CallbackManager] = None,
        verbose: bool = False,
    ):
        self._retriever = retriever
        self._llm = llm
        self._memory = memory

        context_prompt = context_prompt or DEFAULT_CONTEXT_PROMPT_TEMPLATE
        if isinstance(context_prompt, str):
            context_prompt = PromptTemplate(context_prompt)
        self._context_prompt_template = context_prompt

        context_refine_prompt = (
            context_refine_prompt or DEFAULT_CONTEXT_REFINE_PROMPT_TEMPLATE
        )
        if isinstance(context_refine_prompt, str):
            context_refine_prompt = PromptTemplate(context_refine_prompt)
        self._context_refine_prompt_template = context_refine_prompt

        condense_prompt = condense_prompt or DEFAULT_CONDENSE_PROMPT_TEMPLATE
        if isinstance(condense_prompt, str):
            condense_prompt = PromptTemplate(condense_prompt)
        self._condense_prompt_template = condense_prompt

        self._system_prompt = system_prompt
        self._skip_condense = skip_condense
        self._node_postprocessors = node_postprocessors or []
        self.callback_manager = callback_manager or CallbackManager([])
        for node_postprocessor in self._node_postprocessors:
            node_postprocessor.callback_manager = self.callback_manager

        self._token_counter = TokenCounter()
        self._verbose = verbose

    @classmethod
    deffrom_defaults(
        cls,
        retriever: BaseRetriever,
        llm: Optional[LLM] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        memory: Optional[BaseMemory] = None,
        system_prompt: Optional[str] = None,
        context_prompt: Optional[Union[str, PromptTemplate]] = None,
        context_refine_prompt: Optional[Union[str, PromptTemplate]] = None,
        condense_prompt: Optional[Union[str, PromptTemplate]] = None,
        skip_condense: bool = False,
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> "CondensePlusContextChatEngine":
"""Initialize a CondensePlusContextChatEngine from default parameters."""
        llm = llm or Settings.llm

        chat_history = chat_history or []
        memory = memory or Memory.from_defaults(
            chat_history=chat_history, token_limit=llm.metadata.context_window - 256
        )

        return cls(
            retriever=retriever,
            llm=llm,
            memory=memory,
            context_prompt=context_prompt,
            context_refine_prompt=context_refine_prompt,
            condense_prompt=condense_prompt,
            skip_condense=skip_condense,
            callback_manager=Settings.callback_manager,
            node_postprocessors=node_postprocessors,
            system_prompt=system_prompt,
            verbose=verbose,
        )

    def_condense_question(
        self, chat_history: List[ChatMessage], latest_message: str
    ) -> str:
"""Condense a conversation history and latest user message to a standalone question."""
        if self._skip_condense or len(chat_history) == 0:
            return latest_message

        chat_history_str = messages_to_history_str(chat_history)
        logger.debug(chat_history_str)

        llm_input = self._condense_prompt_template.format(
            chat_history=chat_history_str, question=latest_message
        )

        return str(self._llm.complete(llm_input))

    async def_acondense_question(
        self, chat_history: List[ChatMessage], latest_message: str
    ) -> str:
"""Condense a conversation history and latest user message to a standalone question."""
        if self._skip_condense or len(chat_history) == 0:
            return latest_message

        chat_history_str = messages_to_history_str(chat_history)
        logger.debug(chat_history_str)

        llm_input = self._condense_prompt_template.format(
            chat_history=chat_history_str, question=latest_message
        )

        return str(await self._llm.acomplete(llm_input))

    def_get_nodes(self, message: str) -> List[NodeWithScore]:
"""Generate context information from a message."""
        nodes = self._retriever.retrieve(message)
        for postprocessor in self._node_postprocessors:
            nodes = postprocessor.postprocess_nodes(
                nodes, query_bundle=QueryBundle(message)
            )

        return nodes

    async def_aget_nodes(self, message: str) -> List[NodeWithScore]:
"""Generate context information from a message."""
        nodes = await self._retriever.aretrieve(message)
        for postprocessor in self._node_postprocessors:
            nodes = await postprocessor.apostprocess_nodes(
                nodes, query_bundle=QueryBundle(message)
            )

        return nodes

    def_get_response_synthesizer(
        self, chat_history: List[ChatMessage], streaming: bool = False
    ) -> CompactAndRefine:
        system_prompt = self._system_prompt or ""
        qa_messages = get_prefix_messages_with_context(
            self._context_prompt_template,
            system_prompt,
            [],
            chat_history,
            self._llm.metadata.system_role,
        )
        refine_messages = get_prefix_messages_with_context(
            self._context_refine_prompt_template,
            system_prompt,
            [],
            chat_history,
            self._llm.metadata.system_role,
        )

        return get_response_synthesizer(
            self._llm,
            self.callback_manager,
            qa_messages,
            refine_messages,
            streaming,
            qa_function_mappings=self._context_prompt_template.function_mappings,
            refine_function_mappings=self._context_refine_prompt_template.function_mappings,
        )

    def_run_c3(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        streaming: bool = False,
    ) -> Tuple[CompactAndRefine, ToolOutput, List[NodeWithScore]]:
        if chat_history is not None:
            self._memory.set(chat_history)

        chat_history = self._memory.get(input=message)

        # Condense conversation history and latest message to a standalone question
        condensed_question = self._condense_question(chat_history, message)  # type: ignore
        logger.info(f"Condensed question: {condensed_question}")
        if self._verbose:
            print(f"Condensed question: {condensed_question}")

        # get the context nodes using the condensed question
        context_nodes = self._get_nodes(condensed_question)
        context_source = ToolOutput(
            tool_name="retriever",
            content=str(context_nodes),
            raw_input={"message": condensed_question},
            raw_output=context_nodes,
        )

        # build the response synthesizer
        response_synthesizer = self._get_response_synthesizer(
            chat_history, streaming=streaming
        )

        return response_synthesizer, context_source, context_nodes

    async def_arun_c3(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        streaming: bool = False,
    ) -> Tuple[CompactAndRefine, ToolOutput, List[NodeWithScore]]:
        if chat_history is not None:
            await self._memory.aset(chat_history)

        chat_history = await self._memory.aget(input=message)

        # Condense conversation history and latest message to a standalone question
        condensed_question = await self._acondense_question(chat_history, message)  # type: ignore
        logger.info(f"Condensed question: {condensed_question}")
        if self._verbose:
            print(f"Condensed question: {condensed_question}")

        # get the context nodes using the condensed question
        context_nodes = await self._aget_nodes(condensed_question)
        context_source = ToolOutput(
            tool_name="retriever",
            content=str(context_nodes),
            raw_input={"message": condensed_question},
            raw_output=context_nodes,
        )

        # build the response synthesizer
        response_synthesizer = self._get_response_synthesizer(
            chat_history, streaming=streaming
        )

        return response_synthesizer, context_source, context_nodes

    @trace_method("chat")
    defchat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> AgentChatResponse:
        synthesizer, context_source, context_nodes = self._run_c3(message, chat_history)

        response = synthesizer.synthesize(message, context_nodes)

        user_message = ChatMessage(content=message, role=MessageRole.USER)
        assistant_message = ChatMessage(
            content=str(response), role=MessageRole.ASSISTANT
        )
        self._memory.put(user_message)
        self._memory.put(assistant_message)

        return AgentChatResponse(
            response=str(response),
            sources=[context_source],
            source_nodes=context_nodes,
        )

    @trace_method("chat")
    defstream_chat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> StreamingAgentChatResponse:
        synthesizer, context_source, context_nodes = self._run_c3(
            message, chat_history, streaming=True
        )

        response = synthesizer.synthesize(message, context_nodes)
        assert isinstance(response, StreamingResponse)

        self._memory.put(ChatMessage(content=message, role=MessageRole.USER))

        defwrapped_gen(response: StreamingResponse) -> ChatResponseGen:
            full_response = ""
            for token in response.response_gen:
                full_response += token
                yield ChatResponse(
                    message=ChatMessage(
                        content=full_response, role=MessageRole.ASSISTANT
                    ),
                    delta=token,
                )

        chat_response = StreamingAgentChatResponse(
            chat_stream=wrapped_gen(response),
            sources=[context_source],
            source_nodes=context_nodes,
        )
        thread = Thread(
            target=chat_response.write_response_to_history, args=(self._memory,)
        )
        chat_response.write_response_to_history_thread = thread
        thread.start()
        return chat_response

    @trace_method("chat")
    async defachat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> AgentChatResponse:
        synthesizer, context_source, context_nodes = await self._arun_c3(
            message, chat_history
        )

        response = await synthesizer.asynthesize(message, context_nodes)

        user_message = ChatMessage(content=message, role=MessageRole.USER)
        assistant_message = ChatMessage(
            content=str(response), role=MessageRole.ASSISTANT
        )
        await self._memory.aput(user_message)
        await self._memory.aput(assistant_message)

        return AgentChatResponse(
            response=str(response),
            sources=[context_source],
            source_nodes=context_nodes,
        )

    @trace_method("chat")
    async defastream_chat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> StreamingAgentChatResponse:
        synthesizer, context_source, context_nodes = await self._arun_c3(
            message, chat_history, streaming=True
        )

        response = await synthesizer.asynthesize(message, context_nodes)
        assert isinstance(response, AsyncStreamingResponse)

        await self._memory.aput(ChatMessage(content=message, role=MessageRole.USER))

        async defwrapped_gen(response: AsyncStreamingResponse) -> ChatResponseAsyncGen:
            full_response = ""
            async for token in response.async_response_gen():
                full_response += token
                yield ChatResponse(
                    message=ChatMessage(
                        content=full_response, role=MessageRole.ASSISTANT
                    ),
                    delta=token,
                )

        chat_response = StreamingAgentChatResponse(
            achat_stream=wrapped_gen(response),
            sources=[context_source],
            source_nodes=context_nodes,
        )
        chat_response.awrite_response_to_history_task = asyncio.create_task(
            chat_response.awrite_response_to_history(self._memory)
        )
        return chat_response

    defreset(self) -> None:
        # Clear chat history
        self._memory.reset()

    @property
    defchat_history(self) -> List[ChatMessage]:
"""Get chat history."""
        return self._memory.get_all()

```
 |  
| --- | --- |  
###  chat_history `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.CondensePlusContextChatEngine.chat_history "Permanent link")

```
chat_history: []

```

Get chat history.
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.CondensePlusContextChatEngine.from_defaults "Permanent link")

```
from_defaults(
    retriever: ,
    llm: Optional[] = None,
    chat_history: Optional[[]] = None,
    memory: Optional[] = None,
    system_prompt: Optional[] = None,
    context_prompt: Optional[
        Union[, ]
    ] = None,
    context_refine_prompt: Optional[
        Union[, ]
    ] = None,
    condense_prompt: Optional[
        Union[, ]
    ] = None,
    skip_condense:  = False,
    node_postprocessors: Optional[
        []
    ] = None,
    verbose:  = False,
    **kwargs: 
) -> 

```

Initialize a CondensePlusContextChatEngine from default parameters.
Source code in `llama-index-core/llama_index/core/chat_engine/condense_plus_context.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    retriever: BaseRetriever,
    llm: Optional[LLM] = None,
    chat_history: Optional[List[ChatMessage]] = None,
    memory: Optional[BaseMemory] = None,
    system_prompt: Optional[str] = None,
    context_prompt: Optional[Union[str, PromptTemplate]] = None,
    context_refine_prompt: Optional[Union[str, PromptTemplate]] = None,
    condense_prompt: Optional[Union[str, PromptTemplate]] = None,
    skip_condense: bool = False,
    node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
    verbose: bool = False,
    **kwargs: Any,
) -> "CondensePlusContextChatEngine":
"""Initialize a CondensePlusContextChatEngine from default parameters."""
    llm = llm or Settings.llm

    chat_history = chat_history or []
    memory = memory or Memory.from_defaults(
        chat_history=chat_history, token_limit=llm.metadata.context_window - 256
    )

    return cls(
        retriever=retriever,
        llm=llm,
        memory=memory,
        context_prompt=context_prompt,
        context_refine_prompt=context_refine_prompt,
        condense_prompt=condense_prompt,
        skip_condense=skip_condense,
        callback_manager=Settings.callback_manager,
        node_postprocessors=node_postprocessors,
        system_prompt=system_prompt,
        verbose=verbose,
    )

```
 |  
| --- | --- |  
##  CondenseQuestionChatEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.CondenseQuestionChatEngine "Permanent link")
Bases: 
Condense Question Chat Engine.
First generate a standalone question from conversation context and last message, then query the query engine for a response.
Source code in `llama-index-core/llama_index/core/chat_engine/condense_question.py`  
| 
```
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
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
```
 | 
```
classCondenseQuestionChatEngine(BaseChatEngine):
"""
    Condense Question Chat Engine.

    First generate a standalone question from conversation context and last message,
    then query the query engine for a response.
    """

    def__init__(
        self,
        query_engine: BaseQueryEngine,
        condense_question_prompt: BasePromptTemplate,
        memory: BaseMemory,
        llm: LLM,
        verbose: bool = False,
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
        self._query_engine = query_engine
        self._condense_question_prompt = condense_question_prompt
        self._memory = memory
        self._llm = llm
        self._verbose = verbose
        self.callback_manager = callback_manager or CallbackManager([])

    @classmethod
    deffrom_defaults(
        cls,
        query_engine: BaseQueryEngine,
        condense_question_prompt: Optional[BasePromptTemplate] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        memory: Optional[BaseMemory] = None,
        memory_cls: Type[BaseMemory] = Memory,
        verbose: bool = False,
        system_prompt: Optional[str] = None,
        prefix_messages: Optional[List[ChatMessage]] = None,
        llm: Optional[LLM] = None,
        **kwargs: Any,
    ) -> "CondenseQuestionChatEngine":
"""Initialize a CondenseQuestionChatEngine from default parameters."""
        condense_question_prompt = condense_question_prompt or DEFAULT_PROMPT

        llm = llm or Settings.llm

        chat_history = chat_history or []
        memory = memory or memory_cls.from_defaults(
            chat_history=chat_history, token_limit=llm.metadata.context_window - 256
        )

        if system_prompt is not None:
            raise NotImplementedError(
                "system_prompt is not supported for CondenseQuestionChatEngine."
            )
        if prefix_messages is not None:
            raise NotImplementedError(
                "prefix_messages is not supported for CondenseQuestionChatEngine."
            )

        return cls(
            query_engine,
            condense_question_prompt,
            memory,
            llm,
            verbose=verbose,
            callback_manager=Settings.callback_manager,
        )

    def_condense_question(
        self, chat_history: List[ChatMessage], last_message: str
    ) -> str:
"""
        Generate standalone question from conversation context and last message.
        """
        if not chat_history:
            # Keep the question as is if there's no conversation context.
            return last_message

        chat_history_str = messages_to_history_str(chat_history)
        logger.debug(chat_history_str)

        return self._llm.predict(
            self._condense_question_prompt,
            question=last_message,
            chat_history=chat_history_str,
        )

    async def_acondense_question(
        self, chat_history: List[ChatMessage], last_message: str
    ) -> str:
"""
        Generate standalone question from conversation context and last message.
        """
        if not chat_history:
            # Keep the question as is if there's no conversation context.
            return last_message

        chat_history_str = messages_to_history_str(chat_history)
        logger.debug(chat_history_str)

        return await self._llm.apredict(
            self._condense_question_prompt,
            question=last_message,
            chat_history=chat_history_str,
        )

    def_get_tool_output_from_response(
        self, query: str, response: RESPONSE_TYPE
    ) -> ToolOutput:
        if isinstance(response, (StreamingResponse, AsyncStreamingResponse)):
            return ToolOutput(
                content="",
                tool_name="query_engine",
                raw_input={"query": query},
                raw_output=response,
            )
        else:
            return ToolOutput(
                content=str(response),
                tool_name="query_engine",
                raw_input={"query": query},
                raw_output=response,
            )

    @trace_method("chat")
    defchat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> AgentChatResponse:
        chat_history = chat_history or self._memory.get(input=message)

        # Generate standalone question from conversation context and last message
        condensed_question = self._condense_question(chat_history, message)

        log_str = f"Querying with: {condensed_question}"
        logger.info(log_str)
        if self._verbose:
            print(log_str)

        # TODO: right now, query engine uses class attribute to configure streaming,
        #       we are moving towards separate streaming and non-streaming methods.
        #       In the meanwhile, use this hack to toggle streaming.
        fromllama_index.core.query_engine.retriever_query_engineimport (
            RetrieverQueryEngine,
        )

        if isinstance(self._query_engine, RetrieverQueryEngine):
            is_streaming = self._query_engine._response_synthesizer._streaming
            self._query_engine._response_synthesizer._streaming = False

        # Query with standalone question
        try:
            query_response = self._query_engine.query(condensed_question)
        finally:
            # NOTE: reset streaming flag
            if isinstance(self._query_engine, RetrieverQueryEngine):
                self._query_engine._response_synthesizer._streaming = is_streaming

        tool_output = self._get_tool_output_from_response(
            condensed_question, query_response
        )

        # Record response
        self._memory.put(ChatMessage(role=MessageRole.USER, content=message))
        self._memory.put(
            ChatMessage(role=MessageRole.ASSISTANT, content=str(query_response))
        )

        return AgentChatResponse(response=str(query_response), sources=[tool_output])

    @trace_method("chat")
    defstream_chat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> StreamingAgentChatResponse:
        chat_history = chat_history or self._memory.get(input=message)

        # Generate standalone question from conversation context and last message
        condensed_question = self._condense_question(chat_history, message)

        log_str = f"Querying with: {condensed_question}"
        logger.info(log_str)
        if self._verbose:
            print(log_str)

        # TODO: right now, query engine uses class attribute to configure streaming,
        #       we are moving towards separate streaming and non-streaming methods.
        #       In the meanwhile, use this hack to toggle streaming.
        fromllama_index.core.query_engine.retriever_query_engineimport (
            RetrieverQueryEngine,
        )

        if isinstance(self._query_engine, RetrieverQueryEngine):
            is_streaming = self._query_engine._response_synthesizer._streaming
            self._query_engine._response_synthesizer._streaming = True

        # Query with standalone question
        try:
            query_response = self._query_engine.query(condensed_question)
        finally:
            # NOTE: reset streaming flag
            if isinstance(self._query_engine, RetrieverQueryEngine):
                self._query_engine._response_synthesizer._streaming = is_streaming

        tool_output = self._get_tool_output_from_response(
            condensed_question, query_response
        )

        # Record response
        if (
            isinstance(query_response, StreamingResponse)
            and query_response.response_gen is not None
        ):
            # override the generator to include writing to chat history
            self._memory.put(ChatMessage(role=MessageRole.USER, content=message))
            response = StreamingAgentChatResponse(
                chat_stream=response_gen_from_query_engine(query_response.response_gen),
                sources=[tool_output],
            )
            thread = Thread(
                target=response.write_response_to_history,
                args=(self._memory,),
            )
            response.write_response_to_history_thread = thread
            thread.start()
        else:
            raise ValueError("Streaming is not enabled. Please use chat() instead.")
        return response

    @trace_method("chat")
    async defachat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> AgentChatResponse:
        chat_history = chat_history or await self._memory.aget(input=message)

        # Generate standalone question from conversation context and last message
        condensed_question = await self._acondense_question(chat_history, message)

        log_str = f"Querying with: {condensed_question}"
        logger.info(log_str)
        if self._verbose:
            print(log_str)

        # TODO: right now, query engine uses class attribute to configure streaming,
        #       we are moving towards separate streaming and non-streaming methods.
        #       In the meanwhile, use this hack to toggle streaming.
        fromllama_index.core.query_engine.retriever_query_engineimport (
            RetrieverQueryEngine,
        )

        if isinstance(self._query_engine, RetrieverQueryEngine):
            is_streaming = self._query_engine._response_synthesizer._streaming
            self._query_engine._response_synthesizer._streaming = False

        # Query with standalone question
        try:
            query_response = await self._query_engine.aquery(condensed_question)
        finally:
            # NOTE: reset streaming flag
            if isinstance(self._query_engine, RetrieverQueryEngine):
                self._query_engine._response_synthesizer._streaming = is_streaming

        tool_output = self._get_tool_output_from_response(
            condensed_question, query_response
        )

        # Record response
        await self._memory.aput(ChatMessage(role=MessageRole.USER, content=message))
        await self._memory.aput(
            ChatMessage(role=MessageRole.ASSISTANT, content=str(query_response))
        )

        return AgentChatResponse(response=str(query_response), sources=[tool_output])

    @trace_method("chat")
    async defastream_chat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> StreamingAgentChatResponse:
        chat_history = chat_history or await self._memory.aget(input=message)

        # Generate standalone question from conversation context and last message
        condensed_question = await self._acondense_question(chat_history, message)

        log_str = f"Querying with: {condensed_question}"
        logger.info(log_str)
        if self._verbose:
            print(log_str)

        # TODO: right now, query engine uses class attribute to configure streaming,
        #       we are moving towards separate streaming and non-streaming methods.
        #       In the meanwhile, use this hack to toggle streaming.
        fromllama_index.core.query_engine.retriever_query_engineimport (
            RetrieverQueryEngine,
        )

        if isinstance(self._query_engine, RetrieverQueryEngine):
            is_streaming = self._query_engine._response_synthesizer._streaming
            self._query_engine._response_synthesizer._streaming = True

        # Query with standalone question
        try:
            query_response = await self._query_engine.aquery(condensed_question)
        finally:
            # NOTE: reset streaming flag
            if isinstance(self._query_engine, RetrieverQueryEngine):
                self._query_engine._response_synthesizer._streaming = is_streaming

        tool_output = self._get_tool_output_from_response(
            condensed_question, query_response
        )

        # Record response
        if isinstance(query_response, AsyncStreamingResponse):
            # override the generator to include writing to chat history
            # TODO: query engine does not support async generator yet
            await self._memory.aput(ChatMessage(role=MessageRole.USER, content=message))
            response = StreamingAgentChatResponse(
                achat_stream=aresponse_gen_from_query_engine(
                    query_response.async_response_gen()
                ),
                sources=[tool_output],
            )
            response.awrite_response_to_history_task = asyncio.create_task(
                response.awrite_response_to_history(self._memory)
            )

        else:
            raise ValueError("Streaming is not enabled. Please use achat() instead.")
        return response

    defreset(self) -> None:
        # Clear chat history
        self._memory.reset()

    @property
    defchat_history(self) -> List[ChatMessage]:
"""Get chat history."""
        return self._memory.get_all()

```
 |  
| --- | --- |  
###  chat_history `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.CondenseQuestionChatEngine.chat_history "Permanent link")

```
chat_history: []

```

Get chat history.
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.CondenseQuestionChatEngine.from_defaults "Permanent link")

```
from_defaults(
    query_engine: ,
    condense_question_prompt: Optional[
        
    ] = None,
    chat_history: Optional[[]] = None,
    memory: Optional[] = None,
    memory_cls: [] = ,
    verbose:  = False,
    system_prompt: Optional[] = None,
    prefix_messages: Optional[[]] = None,
    llm: Optional[] = None,
    **kwargs: 
) -> 

```

Initialize a CondenseQuestionChatEngine from default parameters.
Source code in `llama-index-core/llama_index/core/chat_engine/condense_question.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    query_engine: BaseQueryEngine,
    condense_question_prompt: Optional[BasePromptTemplate] = None,
    chat_history: Optional[List[ChatMessage]] = None,
    memory: Optional[BaseMemory] = None,
    memory_cls: Type[BaseMemory] = Memory,
    verbose: bool = False,
    system_prompt: Optional[str] = None,
    prefix_messages: Optional[List[ChatMessage]] = None,
    llm: Optional[LLM] = None,
    **kwargs: Any,
) -> "CondenseQuestionChatEngine":
"""Initialize a CondenseQuestionChatEngine from default parameters."""
    condense_question_prompt = condense_question_prompt or DEFAULT_PROMPT

    llm = llm or Settings.llm

    chat_history = chat_history or []
    memory = memory or memory_cls.from_defaults(
        chat_history=chat_history, token_limit=llm.metadata.context_window - 256
    )

    if system_prompt is not None:
        raise NotImplementedError(
            "system_prompt is not supported for CondenseQuestionChatEngine."
        )
    if prefix_messages is not None:
        raise NotImplementedError(
            "prefix_messages is not supported for CondenseQuestionChatEngine."
        )

    return cls(
        query_engine,
        condense_question_prompt,
        memory,
        llm,
        verbose=verbose,
        callback_manager=Settings.callback_manager,
    )

```
 |  
| --- | --- |  
##  ContextChatEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.ContextChatEngine "Permanent link")
Bases: 
Context Chat Engine.
Uses a retriever to retrieve a context, set the context in the system prompt, and then uses an LLM to generate a response, for a fluid chat experience.
Source code in `llama-index-core/llama_index/core/chat_engine/context.py`  
| 
```
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
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
```
 | 
```
classContextChatEngine(BaseChatEngine):
"""
    Context Chat Engine.

    Uses a retriever to retrieve a context, set the context in the system prompt,
    and then uses an LLM to generate a response, for a fluid chat experience.
    """

    def__init__(
        self,
        retriever: BaseRetriever,
        llm: LLM,
        memory: BaseMemory,
        prefix_messages: List[ChatMessage],
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
        context_template: Optional[Union[str, PromptTemplate]] = None,
        context_refine_template: Optional[Union[str, PromptTemplate]] = None,
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
        self._retriever = retriever
        self._llm = llm
        self._memory = memory
        self._prefix_messages = prefix_messages
        self._node_postprocessors = node_postprocessors or []

        context_template = context_template or DEFAULT_CONTEXT_TEMPLATE
        if isinstance(context_template, str):
            context_template = PromptTemplate(context_template)
        self._context_template = context_template

        context_refine_template = context_refine_template or DEFAULT_REFINE_TEMPLATE
        if isinstance(context_refine_template, str):
            context_refine_template = PromptTemplate(context_refine_template)
        self._context_refine_template = context_refine_template

        self.callback_manager = callback_manager or CallbackManager([])
        for node_postprocessor in self._node_postprocessors:
            node_postprocessor.callback_manager = self.callback_manager

    @classmethod
    deffrom_defaults(
        cls,
        retriever: BaseRetriever,
        chat_history: Optional[List[ChatMessage]] = None,
        memory: Optional[BaseMemory] = None,
        system_prompt: Optional[str] = None,
        prefix_messages: Optional[List[ChatMessage]] = None,
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
        context_template: Optional[Union[str, PromptTemplate]] = None,
        context_refine_template: Optional[Union[str, PromptTemplate]] = None,
        llm: Optional[LLM] = None,
        **kwargs: Any,
    ) -> "ContextChatEngine":
"""Initialize a ContextChatEngine from default parameters."""
        llm = llm or Settings.llm

        chat_history = chat_history or []
        memory = memory or Memory.from_defaults(
            chat_history=chat_history, token_limit=llm.metadata.context_window - 256
        )

        if system_prompt is not None:
            if prefix_messages is not None:
                raise ValueError(
                    "Cannot specify both system_prompt and prefix_messages"
                )
            prefix_messages = [
                ChatMessage(content=system_prompt, role=llm.metadata.system_role)
            ]

        prefix_messages = prefix_messages or []
        node_postprocessors = node_postprocessors or []

        return cls(
            retriever,
            llm=llm,
            memory=memory,
            prefix_messages=prefix_messages,
            node_postprocessors=node_postprocessors,
            callback_manager=Settings.callback_manager,
            context_template=context_template,
            context_refine_template=context_refine_template,
        )

    def_get_nodes(self, message: str) -> List[NodeWithScore]:
"""Generate context information from a message."""
        nodes = self._retriever.retrieve(message)
        for postprocessor in self._node_postprocessors:
            nodes = postprocessor.postprocess_nodes(
                nodes, query_bundle=QueryBundle(message)
            )

        return nodes

    async def_aget_nodes(self, message: str) -> List[NodeWithScore]:
"""Generate context information from a message."""
        nodes = await self._retriever.aretrieve(message)
        for postprocessor in self._node_postprocessors:
            nodes = await postprocessor.apostprocess_nodes(
                nodes, query_bundle=QueryBundle(message)
            )

        return nodes

    def_get_response_synthesizer(
        self, chat_history: List[ChatMessage], streaming: bool = False
    ) -> CompactAndRefine:
        # Pull the system prompt from the prefix messages
        system_prompt = ""
        prefix_messages = self._prefix_messages
        if (
            len(self._prefix_messages) != 0
            and self._prefix_messages[0].role == MessageRole.SYSTEM
        ):
            system_prompt = str(self._prefix_messages[0].content)
            prefix_messages = self._prefix_messages[1:]

        # Get the messages for the QA and refine prompts
        qa_messages = get_prefix_messages_with_context(
            self._context_template,
            system_prompt,
            prefix_messages,
            chat_history,
            self._llm.metadata.system_role,
        )
        refine_messages = get_prefix_messages_with_context(
            self._context_refine_template,
            system_prompt,
            prefix_messages,
            chat_history,
            self._llm.metadata.system_role,
        )

        # Get the response synthesizer
        return get_response_synthesizer(
            self._llm,
            self.callback_manager,
            qa_messages,
            refine_messages,
            streaming,
            qa_function_mappings=self._context_template.function_mappings,
            refine_function_mappings=self._context_refine_template.function_mappings,
        )

    @trace_method("chat")
    defchat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        prev_chunks: Optional[List[NodeWithScore]] = None,
    ) -> AgentChatResponse:
        if chat_history is not None:
            self._memory.set(chat_history)

        # get nodes and postprocess them
        nodes = self._get_nodes(message)
        if len(nodes) == 0 and prev_chunks is not None:
            nodes = prev_chunks

        # Get the response synthesizer with dynamic prompts
        chat_history = self._memory.get(
            input=message,
        )
        synthesizer = self._get_response_synthesizer(chat_history)

        response = synthesizer.synthesize(message, nodes)
        user_message = ChatMessage(content=str(message), role=MessageRole.USER)
        ai_message = ChatMessage(content=str(response), role=MessageRole.ASSISTANT)

        self._memory.put(user_message)
        self._memory.put(ai_message)

        return AgentChatResponse(
            response=str(response),
            sources=[
                ToolOutput(
                    tool_name="retriever",
                    content=str(nodes),
                    raw_input={"message": message},
                    raw_output=nodes,
                )
            ],
            source_nodes=nodes,
        )

    @trace_method("chat")
    defstream_chat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        prev_chunks: Optional[List[NodeWithScore]] = None,
    ) -> StreamingAgentChatResponse:
        if chat_history is not None:
            self._memory.set(chat_history)

        # get nodes and postprocess them
        nodes = self._get_nodes(message)
        if len(nodes) == 0 and prev_chunks is not None:
            nodes = prev_chunks

        # Get the response synthesizer with dynamic prompts
        chat_history = self._memory.get(
            input=message,
        )
        synthesizer = self._get_response_synthesizer(chat_history, streaming=True)

        response = synthesizer.synthesize(message, nodes)
        assert isinstance(response, StreamingResponse)

        self._memory.put(ChatMessage(content=str(message), role=MessageRole.USER))

        defwrapped_gen(response: StreamingResponse) -> ChatResponseGen:
            full_response = ""
            for token in response.response_gen:
                full_response += token
                yield ChatResponse(
                    message=ChatMessage(
                        content=full_response, role=MessageRole.ASSISTANT
                    ),
                    delta=token,
                )

        chat_response = StreamingAgentChatResponse(
            chat_stream=wrapped_gen(response),
            sources=[
                ToolOutput(
                    tool_name="retriever",
                    content=str(nodes),
                    raw_input={"message": message},
                    raw_output=nodes,
                )
            ],
            source_nodes=nodes,
        )
        thread = Thread(
            target=chat_response.write_response_to_history, args=(self._memory,)
        )
        chat_response.write_response_to_history_thread = thread
        thread.start()
        return chat_response

    @trace_method("chat")
    async defachat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        prev_chunks: Optional[List[NodeWithScore]] = None,
    ) -> AgentChatResponse:
        if chat_history is not None:
            await self._memory.aset(chat_history)

        # get nodes and postprocess them
        nodes = await self._aget_nodes(message)
        if len(nodes) == 0 and prev_chunks is not None:
            nodes = prev_chunks

        # Get the response synthesizer with dynamic prompts
        chat_history = await self._memory.aget(
            input=message,
        )
        synthesizer = self._get_response_synthesizer(chat_history)

        response = await synthesizer.asynthesize(message, nodes)
        user_message = ChatMessage(content=str(message), role=MessageRole.USER)
        ai_message = ChatMessage(content=str(response), role=MessageRole.ASSISTANT)

        await self._memory.aput(user_message)
        await self._memory.aput(ai_message)

        return AgentChatResponse(
            response=str(response),
            sources=[
                ToolOutput(
                    tool_name="retriever",
                    content=str(nodes),
                    raw_input={"message": message},
                    raw_output=nodes,
                )
            ],
            source_nodes=nodes,
        )

    @trace_method("chat")
    async defastream_chat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        prev_chunks: Optional[List[NodeWithScore]] = None,
    ) -> StreamingAgentChatResponse:
        if chat_history is not None:
            await self._memory.aset(chat_history)
        # get nodes and postprocess them
        nodes = await self._aget_nodes(message)
        if len(nodes) == 0 and prev_chunks is not None:
            nodes = prev_chunks

        # Get the response synthesizer with dynamic prompts
        chat_history = await self._memory.aget(
            input=message,
        )
        synthesizer = self._get_response_synthesizer(chat_history, streaming=True)

        response = await synthesizer.asynthesize(message, nodes)
        assert isinstance(response, AsyncStreamingResponse)

        await self._memory.aput(
            ChatMessage(content=str(message), role=MessageRole.USER)
        )

        async defwrapped_gen(response: AsyncStreamingResponse) -> ChatResponseAsyncGen:
            full_response = ""
            async for token in response.async_response_gen():
                full_response += token
                yield ChatResponse(
                    message=ChatMessage(
                        content=full_response, role=MessageRole.ASSISTANT
                    ),
                    delta=token,
                )

        chat_response = StreamingAgentChatResponse(
            achat_stream=wrapped_gen(response),
            sources=[
                ToolOutput(
                    tool_name="retriever",
                    content=str(nodes),
                    raw_input={"message": message},
                    raw_output=nodes,
                )
            ],
            source_nodes=nodes,
        )
        chat_response.awrite_response_to_history_task = asyncio.create_task(
            chat_response.awrite_response_to_history(self._memory)
        )
        return chat_response

    defreset(self) -> None:
        self._memory.reset()

    @property
    defchat_history(self) -> List[ChatMessage]:
"""Get chat history."""
        return self._memory.get_all()

```
 |  
| --- | --- |  
###  chat_history `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.ContextChatEngine.chat_history "Permanent link")

```
chat_history: []

```

Get chat history.
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.ContextChatEngine.from_defaults "Permanent link")

```
from_defaults(
    retriever: ,
    chat_history: Optional[[]] = None,
    memory: Optional[] = None,
    system_prompt: Optional[] = None,
    prefix_messages: Optional[[]] = None,
    node_postprocessors: Optional[
        []
    ] = None,
    context_template: Optional[
        Union[, ]
    ] = None,
    context_refine_template: Optional[
        Union[, ]
    ] = None,
    llm: Optional[] = None,
    **kwargs: 
) -> 

```

Initialize a ContextChatEngine from default parameters.
Source code in `llama-index-core/llama_index/core/chat_engine/context.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    retriever: BaseRetriever,
    chat_history: Optional[List[ChatMessage]] = None,
    memory: Optional[BaseMemory] = None,
    system_prompt: Optional[str] = None,
    prefix_messages: Optional[List[ChatMessage]] = None,
    node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
    context_template: Optional[Union[str, PromptTemplate]] = None,
    context_refine_template: Optional[Union[str, PromptTemplate]] = None,
    llm: Optional[LLM] = None,
    **kwargs: Any,
) -> "ContextChatEngine":
"""Initialize a ContextChatEngine from default parameters."""
    llm = llm or Settings.llm

    chat_history = chat_history or []
    memory = memory or Memory.from_defaults(
        chat_history=chat_history, token_limit=llm.metadata.context_window - 256
    )

    if system_prompt is not None:
        if prefix_messages is not None:
            raise ValueError(
                "Cannot specify both system_prompt and prefix_messages"
            )
        prefix_messages = [
            ChatMessage(content=system_prompt, role=llm.metadata.system_role)
        ]

    prefix_messages = prefix_messages or []
    node_postprocessors = node_postprocessors or []

    return cls(
        retriever,
        llm=llm,
        memory=memory,
        prefix_messages=prefix_messages,
        node_postprocessors=node_postprocessors,
        callback_manager=Settings.callback_manager,
        context_template=context_template,
        context_refine_template=context_refine_template,
    )

```
 |  
| --- | --- |  
##  SimpleChatEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.SimpleChatEngine "Permanent link")
Bases: 
Simple Chat Engine.
Have a conversation with the LLM. This does not make use of a knowledge base.
Source code in `llama-index-core/llama_index/core/chat_engine/simple.py`  
| 
```
 17
 18
 19
 20
 21
 22
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
```
 | 
```
classSimpleChatEngine(BaseChatEngine):
"""
    Simple Chat Engine.

    Have a conversation with the LLM.
    This does not make use of a knowledge base.
    """

    def__init__(
        self,
        llm: LLM,
        memory: BaseMemory,
        prefix_messages: List[ChatMessage],
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
        self._llm = llm
        self._memory = memory
        self._prefix_messages = prefix_messages
        self.callback_manager = callback_manager or CallbackManager([])

    @classmethod
    deffrom_defaults(
        cls,
        chat_history: Optional[List[ChatMessage]] = None,
        memory: Optional[BaseMemory] = None,
        memory_cls: Type[BaseMemory] = Memory,
        system_prompt: Optional[str] = None,
        prefix_messages: Optional[List[ChatMessage]] = None,
        llm: Optional[LLM] = None,
        **kwargs: Any,
    ) -> "SimpleChatEngine":
"""Initialize a SimpleChatEngine from default parameters."""
        llm = llm or Settings.llm

        chat_history = chat_history or []
        memory = memory or memory_cls.from_defaults(
            chat_history=chat_history, token_limit=llm.metadata.context_window - 256
        )

        if system_prompt is not None:
            if prefix_messages is not None:
                raise ValueError(
                    "Cannot specify both system_prompt and prefix_messages"
                )
            prefix_messages = [
                ChatMessage(content=system_prompt, role=llm.metadata.system_role)
            ]

        prefix_messages = prefix_messages or []

        return cls(
            llm=llm,
            memory=memory,
            prefix_messages=prefix_messages,
            callback_manager=Settings.callback_manager,
        )

    @trace_method("chat")
    defchat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> AgentChatResponse:
        if chat_history is not None:
            self._memory.set(chat_history)
        self._memory.put(ChatMessage(content=message, role="user"))

        if hasattr(self._memory, "tokenizer_fn"):
            initial_token_count = len(
                self._memory.tokenizer_fn(
                    " ".join(
                        [
                            (m.content or "")
                            for m in self._prefix_messages
                            if isinstance(m.content, str)
                        ]
                    )
                )
            )
        else:
            initial_token_count = 0

        all_messages = self._prefix_messages + self._memory.get(
            initial_token_count=initial_token_count
        )

        chat_response = self._llm.chat(all_messages)
        ai_message = chat_response.message
        self._memory.put(ai_message)

        return AgentChatResponse(response=str(chat_response.message.content))

    @trace_method("chat")
    defstream_chat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> StreamingAgentChatResponse:
        if chat_history is not None:
            self._memory.set(chat_history)
        self._memory.put(ChatMessage(content=message, role="user"))

        if hasattr(self._memory, "tokenizer_fn"):
            initial_token_count = len(
                self._memory.tokenizer_fn(
                    " ".join(
                        [
                            (m.content or "")
                            for m in self._prefix_messages
                            if isinstance(m.content, str)
                        ]
                    )
                )
            )
        else:
            initial_token_count = 0

        all_messages = self._prefix_messages + self._memory.get(
            initial_token_count=initial_token_count
        )

        chat_response = StreamingAgentChatResponse(
            chat_stream=self._llm.stream_chat(all_messages)
        )
        thread = Thread(
            target=chat_response.write_response_to_history, args=(self._memory,)
        )
        chat_response.write_response_to_history_thread = thread
        thread.start()

        return chat_response

    @trace_method("chat")
    async defachat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> AgentChatResponse:
        if chat_history is not None:
            await self._memory.aset(chat_history)
        await self._memory.aput(ChatMessage(content=message, role="user"))

        if hasattr(self._memory, "tokenizer_fn"):
            initial_token_count = len(
                self._memory.tokenizer_fn(
                    " ".join(
                        [
                            (m.content or "")
                            for m in self._prefix_messages
                            if isinstance(m.content, str)
                        ]
                    )
                )
            )
        else:
            initial_token_count = 0

        all_messages = self._prefix_messages + (
            await self._memory.aget(initial_token_count=initial_token_count)
        )

        chat_response = await self._llm.achat(all_messages)
        ai_message = chat_response.message
        await self._memory.aput(ai_message)

        return AgentChatResponse(response=str(chat_response.message.content))

    @trace_method("chat")
    async defastream_chat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> StreamingAgentChatResponse:
        if chat_history is not None:
            await self._memory.aset(chat_history)
        await self._memory.aput(ChatMessage(content=message, role="user"))

        if hasattr(self._memory, "tokenizer_fn"):
            initial_token_count = len(
                self._memory.tokenizer_fn(
                    " ".join(
                        [
                            (m.content or "")
                            for m in self._prefix_messages
                            if isinstance(m.content, str)
                        ]
                    )
                )
            )
        else:
            initial_token_count = 0

        all_messages = self._prefix_messages + (
            await self._memory.aget(initial_token_count=initial_token_count)
        )

        chat_response = StreamingAgentChatResponse(
            achat_stream=await self._llm.astream_chat(all_messages)
        )
        chat_response.awrite_response_to_history_task = asyncio.create_task(
            chat_response.awrite_response_to_history(self._memory)
        )

        return chat_response

    defreset(self) -> None:
        self._memory.reset()

    @property
    defchat_history(self) -> List[ChatMessage]:
"""Get chat history."""
        return self._memory.get_all()

```
 |  
| --- | --- |  
###  chat_history `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.SimpleChatEngine.chat_history "Permanent link")

```
chat_history: []

```

Get chat history.
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.SimpleChatEngine.from_defaults "Permanent link")

```
from_defaults(
    chat_history: Optional[[]] = None,
    memory: Optional[] = None,
    memory_cls: [] = ,
    system_prompt: Optional[] = None,
    prefix_messages: Optional[[]] = None,
    llm: Optional[] = None,
    **kwargs: 
) -> 

```

Initialize a SimpleChatEngine from default parameters.
Source code in `llama-index-core/llama_index/core/chat_engine/simple.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    chat_history: Optional[List[ChatMessage]] = None,
    memory: Optional[BaseMemory] = None,
    memory_cls: Type[BaseMemory] = Memory,
    system_prompt: Optional[str] = None,
    prefix_messages: Optional[List[ChatMessage]] = None,
    llm: Optional[LLM] = None,
    **kwargs: Any,
) -> "SimpleChatEngine":
"""Initialize a SimpleChatEngine from default parameters."""
    llm = llm or Settings.llm

    chat_history = chat_history or []
    memory = memory or memory_cls.from_defaults(
        chat_history=chat_history, token_limit=llm.metadata.context_window - 256
    )

    if system_prompt is not None:
        if prefix_messages is not None:
            raise ValueError(
                "Cannot specify both system_prompt and prefix_messages"
            )
        prefix_messages = [
            ChatMessage(content=system_prompt, role=llm.metadata.system_role)
        ]

    prefix_messages = prefix_messages or []

    return cls(
        llm=llm,
        memory=memory,
        prefix_messages=prefix_messages,
        callback_manager=Settings.callback_manager,
    )

```
 |  
| --- | --- |  
##  MultiModalContextChatEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.MultiModalContextChatEngine "Permanent link")
Bases: 
Multimodal Context Chat Engine.
Assumes that retrieved text context fits within context window of LLM, along with images. This class closely relates to the non-multimodal version, ContextChatEngine.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `retriever`  |  `MultiModalVectorIndexRetriever`  |  A retriever object.  |  _required_  |  
|  `multi_modal_llm`  |  A multimodal LLM model.  |  _required_  |  
|  `memory`  |   |  Chat memory buffer to store the history.  |  _required_  |  
|  `system_prompt`  |  System prompt.  |  _required_  |  
|  `context_template`  |  `Optional[Union[str, PromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.PromptTemplate "PromptTemplate \(llama_index.core.prompts.PromptTemplate\)")]]`  |  Prompt Template to embed query and context.  |  `None`  |  
|  `node_postprocessors`  |  `Optional[List[BaseNodePostprocessor[](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/#llama_index.core.postprocessor.types.BaseNodePostprocessor "BaseNodePostprocessor \(llama_index.core.postprocessor.types.BaseNodePostprocessor\)")]]`  |  Node Postprocessors.  |  `None`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.base.CallbackManager\)")]`  |  A callback manager.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/chat_engine/multi_modal_context.py`  
| 
```
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
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
```
 | 
```
classMultiModalContextChatEngine(BaseChatEngine):
"""
    Multimodal Context Chat Engine.

    Assumes that retrieved text context fits within context window of LLM, along with images.
    This class closely relates to the non-multimodal version, ContextChatEngine.

    Args:
        retriever (MultiModalVectorIndexRetriever): A retriever object.
        multi_modal_llm (LLM): A multimodal LLM model.
        memory (BaseMemory): Chat memory buffer to store the history.
        system_prompt (str): System prompt.
        context_template (Optional[Union[str, PromptTemplate]]): Prompt Template to embed query and context.
        node_postprocessors (Optional[List[BaseNodePostprocessor]]): Node Postprocessors.
        callback_manager (Optional[CallbackManager]): A callback manager.

    """

    def__init__(
        self,
        retriever: BaseRetriever,
        multi_modal_llm: LLM,
        memory: BaseMemory,
        system_prompt: str,
        context_template: Optional[Union[str, PromptTemplate]] = None,
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
        self._retriever = retriever
        self._multi_modal_llm = multi_modal_llm
        context_template = context_template or DEFAULT_TEXT_QA_PROMPT
        if isinstance(context_template, str):
            context_template = PromptTemplate(context_template)
        self._context_template = context_template

        self._memory = memory
        self._system_prompt = system_prompt

        self._node_postprocessors = node_postprocessors or []
        self.callback_manager = callback_manager or CallbackManager([])
        for node_postprocessor in self._node_postprocessors:
            node_postprocessor.callback_manager = self.callback_manager

    @classmethod
    deffrom_defaults(
        cls,
        retriever: BaseRetriever,
        chat_history: Optional[List[ChatMessage]] = None,
        memory: Optional[BaseMemory] = None,
        system_prompt: Optional[str] = None,
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
        context_template: Optional[Union[str, PromptTemplate]] = None,
        multi_modal_llm: Optional[LLM] = None,
        **kwargs: Any,
    ) -> "MultiModalContextChatEngine":
"""Initialize a MultiModalContextChatEngine from default parameters."""
        multi_modal_llm = multi_modal_llm or Settings.llm

        chat_history = chat_history or []
        memory = memory or Memory.from_defaults(
            chat_history=chat_history,
            token_limit=multi_modal_llm.metadata.context_window - 256,
        )

        system_prompt = system_prompt or ""
        node_postprocessors = node_postprocessors or []

        return cls(
            retriever,
            multi_modal_llm=multi_modal_llm,
            memory=memory,
            system_prompt=system_prompt,
            node_postprocessors=node_postprocessors,
            callback_manager=Settings.callback_manager,
            context_template=context_template,
        )

    def_apply_node_postprocessors(
        self, nodes: List[NodeWithScore], query_bundle: QueryBundle
    ) -> List[NodeWithScore]:
        for node_postprocessor in self._node_postprocessors:
            nodes = node_postprocessor.postprocess_nodes(
                nodes, query_bundle=query_bundle
            )
        return nodes

    async def_async_apply_node_postprocessors(
        self, nodes: List[NodeWithScore], query_bundle: QueryBundle
    ) -> List[NodeWithScore]:
        for node_postprocessor in self._node_postprocessors:
            nodes = await node_postprocessor.apostprocess_nodes(
                nodes, query_bundle=query_bundle
            )
        return nodes

    def_get_nodes(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        nodes = self._retriever.retrieve(query_bundle)
        return self._apply_node_postprocessors(nodes, query_bundle=query_bundle)

    async def_aget_nodes(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        nodes = await self._retriever.aretrieve(query_bundle)
        return await self._async_apply_node_postprocessors(
            nodes, query_bundle=query_bundle
        )

    defsynthesize(
        self,
        query_bundle: QueryBundle,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
        streaming: bool = False,
    ) -> RESPONSE_TYPE:
        image_nodes, text_nodes = _get_image_and_text_nodes(nodes)
        context_str = "\n\n".join(
            [r.get_content(metadata_mode=MetadataMode.LLM) for r in text_nodes]
        )
        fmt_prompt = self._context_template.format(
            context_str=context_str, query_str=query_bundle.query_str
        )

        blocks: List[Union[ImageBlock, TextBlock]] = [
            image_node_to_image_block(image_node.node)
            for image_node in image_nodes
            if isinstance(image_node.node, ImageNode)
        ]

        blocks.append(TextBlock(text=fmt_prompt))

        chat_history = self._memory.get(
            input=str(query_bundle),
        )

        if streaming:
            llm_stream = self._multi_modal_llm.stream_chat(
                [
                    ChatMessage(role="system", content=self._system_prompt),
                    *chat_history,
                    ChatMessage(role="user", blocks=blocks),
                ]
            )
            stream_tokens = stream_chat_response_to_tokens(llm_stream)
            return StreamingResponse(
                response_gen=stream_tokens,
                source_nodes=nodes,
                metadata={"text_nodes": text_nodes, "image_nodes": image_nodes},
            )
        else:
            llm_response = self._multi_modal_llm.chat(
                [
                    ChatMessage(role="system", content=self._system_prompt),
                    *chat_history,
                    ChatMessage(role="user", blocks=blocks),
                ]
            )
            output = llm_response.message.content or ""
            return Response(
                response=output,
                source_nodes=nodes,
                metadata={"text_nodes": text_nodes, "image_nodes": image_nodes},
            )

    async defasynthesize(
        self,
        query_bundle: QueryBundle,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
        streaming: bool = False,
    ) -> RESPONSE_TYPE:
        image_nodes, text_nodes = _get_image_and_text_nodes(nodes)
        context_str = "\n\n".join(
            [r.get_content(metadata_mode=MetadataMode.LLM) for r in text_nodes]
        )
        fmt_prompt = self._context_template.format(
            context_str=context_str, query_str=query_bundle.query_str
        )

        blocks: List[Union[ImageBlock, TextBlock]] = [
            image_node_to_image_block(image_node.node)
            for image_node in image_nodes
            if isinstance(image_node.node, ImageNode)
        ]

        blocks.append(TextBlock(text=fmt_prompt))

        chat_history = await self._memory.aget(
            input=str(query_bundle),
        )

        if streaming:
            llm_stream = await self._multi_modal_llm.astream_chat(
                [
                    ChatMessage(role="system", content=self._system_prompt),
                    *chat_history,
                    ChatMessage(role="user", blocks=blocks),
                ]
            )
            stream_tokens = await astream_chat_response_to_tokens(llm_stream)
            return AsyncStreamingResponse(
                response_gen=stream_tokens,
                source_nodes=nodes,
                metadata={"text_nodes": text_nodes, "image_nodes": image_nodes},
            )
        else:
            llm_response = await self._multi_modal_llm.achat(
                [
                    ChatMessage(role="system", content=self._system_prompt),
                    *chat_history,
                    ChatMessage(role="user", blocks=blocks),
                ]
            )
            output = llm_response.message.content or ""
            return Response(
                response=output,
                source_nodes=nodes,
                metadata={"text_nodes": text_nodes, "image_nodes": image_nodes},
            )

    @trace_method("chat")
    defchat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        prev_chunks: Optional[List[NodeWithScore]] = None,
    ) -> AgentChatResponse:
        if chat_history is not None:
            self._memory.set(chat_history)

        # get nodes and postprocess them
        nodes = self._get_nodes(_ensure_query_bundle(message))
        if len(nodes) == 0 and prev_chunks is not None:
            nodes = prev_chunks

        response = self.synthesize(
            _ensure_query_bundle(message), nodes=nodes, streaming=False
        )

        user_message = ChatMessage(content=str(message), role=MessageRole.USER)
        ai_message = ChatMessage(content=str(response), role=MessageRole.ASSISTANT)

        self._memory.put(user_message)
        self._memory.put(ai_message)

        return AgentChatResponse(
            response=str(response),
            sources=[
                ToolOutput(
                    tool_name="retriever",
                    content=str(nodes),
                    raw_input={"message": message},
                    raw_output=response.metadata,
                )
            ],
            source_nodes=response.source_nodes,
        )

    @trace_method("chat")
    defstream_chat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        prev_chunks: Optional[List[NodeWithScore]] = None,
    ) -> StreamingAgentChatResponse:
        if chat_history is not None:
            self._memory.set(chat_history)

        # get nodes and postprocess them
        nodes = self._get_nodes(_ensure_query_bundle(message))
        if len(nodes) == 0 and prev_chunks is not None:
            nodes = prev_chunks

        response = self.synthesize(
            _ensure_query_bundle(message), nodes=nodes, streaming=True
        )
        assert isinstance(response, StreamingResponse)

        self._memory.put(ChatMessage(content=str(message), role=MessageRole.USER))

        defwrapped_gen(response: StreamingResponse) -> ChatResponseGen:
            full_response = ""
            for token in response.response_gen:
                full_response += token
                yield ChatResponse(
                    message=ChatMessage(
                        content=full_response, role=MessageRole.ASSISTANT
                    ),
                    delta=token,
                )

        chat_response = StreamingAgentChatResponse(
            chat_stream=wrapped_gen(response),
            sources=[
                ToolOutput(
                    tool_name="retriever",
                    content=str(nodes),
                    raw_input={"message": message},
                    raw_output=response.metadata,
                )
            ],
            source_nodes=response.source_nodes,
        )
        thread = Thread(
            target=chat_response.write_response_to_history, args=(self._memory,)
        )
        chat_response.write_response_to_history_thread = thread
        thread.start()
        return chat_response

    @trace_method("chat")
    async defachat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        prev_chunks: Optional[List[NodeWithScore]] = None,
    ) -> AgentChatResponse:
        if chat_history is not None:
            await self._memory.aset(chat_history)

        # get nodes and postprocess them
        nodes = await self._aget_nodes(_ensure_query_bundle(message))
        if len(nodes) == 0 and prev_chunks is not None:
            nodes = prev_chunks

        response = await self.asynthesize(
            _ensure_query_bundle(message), nodes=nodes, streaming=False
        )

        user_message = ChatMessage(content=str(message), role=MessageRole.USER)
        ai_message = ChatMessage(content=str(response), role=MessageRole.ASSISTANT)

        await self._memory.aput(user_message)
        await self._memory.aput(ai_message)

        return AgentChatResponse(
            response=str(response),
            sources=[
                ToolOutput(
                    tool_name="retriever",
                    content=str(nodes),
                    raw_input={"message": message},
                    raw_output=response.metadata,
                )
            ],
            source_nodes=response.source_nodes,
        )

    @trace_method("chat")
    async defastream_chat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        prev_chunks: Optional[List[NodeWithScore]] = None,
    ) -> StreamingAgentChatResponse:
        if chat_history is not None:
            await self._memory.aset(chat_history)

        # get nodes and postprocess them
        nodes = await self._aget_nodes(_ensure_query_bundle(message))
        if len(nodes) == 0 and prev_chunks is not None:
            nodes = prev_chunks

        response = await self.asynthesize(
            _ensure_query_bundle(message), nodes=nodes, streaming=True
        )
        assert isinstance(response, AsyncStreamingResponse)

        await self._memory.aput(
            ChatMessage(content=str(message), role=MessageRole.USER)
        )

        async defwrapped_gen(response: AsyncStreamingResponse) -> ChatResponseAsyncGen:
            full_response = ""
            async for token in response.async_response_gen():
                full_response += token
                yield ChatResponse(
                    message=ChatMessage(
                        content=full_response, role=MessageRole.ASSISTANT
                    ),
                    delta=token,
                )

        chat_response = StreamingAgentChatResponse(
            achat_stream=wrapped_gen(response),
            sources=[
                ToolOutput(
                    tool_name="retriever",
                    content=str(nodes),
                    raw_input={"message": message},
                    raw_output=response.metadata,
                )
            ],
            source_nodes=response.source_nodes,
        )
        chat_response.awrite_response_to_history_task = asyncio.create_task(
            chat_response.awrite_response_to_history(self._memory)
        )
        return chat_response

    defreset(self) -> None:
        self._memory.reset()

    @property
    defchat_history(self) -> List[ChatMessage]:
"""Get chat history."""
        return self._memory.get_all()

```
 |  
| --- | --- |  
###  chat_history `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.MultiModalContextChatEngine.chat_history "Permanent link")

```
chat_history: []

```

Get chat history.
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.MultiModalContextChatEngine.from_defaults "Permanent link")

```
from_defaults(
    retriever: ,
    chat_history: Optional[[]] = None,
    memory: Optional[] = None,
    system_prompt: Optional[] = None,
    node_postprocessors: Optional[
        []
    ] = None,
    context_template: Optional[
        Union[, ]
    ] = None,
    multi_modal_llm: Optional[] = None,
    **kwargs: 
) -> 

```

Initialize a MultiModalContextChatEngine from default parameters.
Source code in `llama-index-core/llama_index/core/chat_engine/multi_modal_context.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    retriever: BaseRetriever,
    chat_history: Optional[List[ChatMessage]] = None,
    memory: Optional[BaseMemory] = None,
    system_prompt: Optional[str] = None,
    node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
    context_template: Optional[Union[str, PromptTemplate]] = None,
    multi_modal_llm: Optional[LLM] = None,
    **kwargs: Any,
) -> "MultiModalContextChatEngine":
"""Initialize a MultiModalContextChatEngine from default parameters."""
    multi_modal_llm = multi_modal_llm or Settings.llm

    chat_history = chat_history or []
    memory = memory or Memory.from_defaults(
        chat_history=chat_history,
        token_limit=multi_modal_llm.metadata.context_window - 256,
    )

    system_prompt = system_prompt or ""
    node_postprocessors = node_postprocessors or []

    return cls(
        retriever,
        multi_modal_llm=multi_modal_llm,
        memory=memory,
        system_prompt=system_prompt,
        node_postprocessors=node_postprocessors,
        callback_manager=Settings.callback_manager,
        context_template=context_template,
    )

```
 |  
| --- | --- |  
##  MultiModalCondensePlusContextChatEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.MultiModalCondensePlusContextChatEngine "Permanent link")
Bases: 
Multi-Modal Condensed Conversation & Context Chat Engine.
First condense a conversation and latest user message to a standalone question Then build a context for the standalone question from a retriever, Then pass the context along with prompt and user message to LLM to generate a response.
Source code in `llama-index-core/llama_index/core/chat_engine/multi_modal_condense_plus_context.py`  
| 
```
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
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
```
 | 
```
classMultiModalCondensePlusContextChatEngine(BaseChatEngine):
"""
    Multi-Modal Condensed Conversation & Context Chat Engine.

    First condense a conversation and latest user message to a standalone question
    Then build a context for the standalone question from a retriever,
    Then pass the context along with prompt and user message to LLM to generate a response.
    """

    def__init__(
        self,
        retriever: BaseRetriever,
        multi_modal_llm: LLM,
        memory: BaseMemory,
        context_prompt: Optional[Union[str, PromptTemplate]] = None,
        condense_prompt: Optional[Union[str, PromptTemplate]] = None,
        system_prompt: Optional[str] = None,
        skip_condense: bool = False,
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
        callback_manager: Optional[CallbackManager] = None,
        verbose: bool = False,
    ):
        self._retriever = retriever
        self._multi_modal_llm = multi_modal_llm
        self._memory = memory

        context_prompt = context_prompt or DEFAULT_TEXT_QA_PROMPT
        if isinstance(context_prompt, str):
            context_prompt = PromptTemplate(context_prompt)
        self._context_prompt_template = context_prompt

        condense_prompt = condense_prompt or DEFAULT_CONDENSE_PROMPT_TEMPLATE
        if isinstance(condense_prompt, str):
            condense_prompt = PromptTemplate(condense_prompt)
        self._condense_prompt_template = condense_prompt

        self._system_prompt = system_prompt
        self._skip_condense = skip_condense
        self._node_postprocessors = node_postprocessors or []
        self.callback_manager = callback_manager or CallbackManager([])
        for node_postprocessor in self._node_postprocessors:
            node_postprocessor.callback_manager = self.callback_manager

        self._verbose = verbose

    @classmethod
    deffrom_defaults(
        cls,
        retriever: BaseRetriever,
        multi_modal_llm: Optional[LLM] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        memory: Optional[BaseMemory] = None,
        system_prompt: Optional[str] = None,
        context_prompt: Optional[Union[str, PromptTemplate]] = None,
        condense_prompt: Optional[Union[str, PromptTemplate]] = None,
        skip_condense: bool = False,
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> "MultiModalCondensePlusContextChatEngine":
"""Initialize a MultiModalCondensePlusContextChatEngine from default parameters."""
        multi_modal_llm = multi_modal_llm or Settings.llm

        chat_history = chat_history or []
        memory = memory or Memory.from_defaults(
            chat_history=chat_history,
            token_limit=multi_modal_llm.metadata.context_window - 256,
        )

        return cls(
            retriever=retriever,
            multi_modal_llm=multi_modal_llm,
            memory=memory,
            context_prompt=context_prompt,
            condense_prompt=condense_prompt,
            skip_condense=skip_condense,
            callback_manager=Settings.callback_manager,
            node_postprocessors=node_postprocessors,
            system_prompt=system_prompt,
            verbose=verbose,
        )

    def_condense_question(
        self, chat_history: List[ChatMessage], latest_message: str
    ) -> str:
"""Condense a conversation history and latest user message to a standalone question."""
        if self._skip_condense or len(chat_history) == 0:
            return latest_message

        chat_history_str = messages_to_history_str(chat_history)
        logger.debug(chat_history_str)

        llm_input = self._condense_prompt_template.format(
            chat_history=chat_history_str, question=latest_message
        )

        return str(self._multi_modal_llm.complete(llm_input))

    async def_acondense_question(
        self, chat_history: List[ChatMessage], latest_message: str
    ) -> str:
"""Condense a conversation history and latest user message to a standalone question."""
        if self._skip_condense or len(chat_history) == 0:
            return latest_message

        chat_history_str = messages_to_history_str(chat_history)
        logger.debug(chat_history_str)

        llm_input = self._condense_prompt_template.format(
            chat_history=chat_history_str, question=latest_message
        )

        return str(await self._multi_modal_llm.acomplete(llm_input))

    def_get_nodes(self, message: str) -> List[NodeWithScore]:
"""Generate context information from a message."""
        nodes = self._retriever.retrieve(message)
        for postprocessor in self._node_postprocessors:
            nodes = postprocessor.postprocess_nodes(
                nodes, query_bundle=QueryBundle(message)
            )

        return nodes

    async def_aget_nodes(self, message: str) -> List[NodeWithScore]:
"""Generate context information from a message."""
        nodes = await self._retriever.aretrieve(message)
        for postprocessor in self._node_postprocessors:
            nodes = await postprocessor.apostprocess_nodes(
                nodes, query_bundle=QueryBundle(message)
            )

        return nodes

    def_run_c2(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
    ) -> Tuple[ToolOutput, List[NodeWithScore]]:
        if chat_history is not None:
            self._memory.set(chat_history)

        chat_history = self._memory.get(input=message)

        # Condense conversation history and latest message to a standalone question
        condensed_question = self._condense_question(chat_history, message)  # type: ignore
        logger.info(f"Condensed question: {condensed_question}")
        if self._verbose:
            print(f"Condensed question: {condensed_question}")

        # get the context nodes using the condensed question
        context_nodes = self._get_nodes(condensed_question)
        context_source = ToolOutput(
            tool_name="retriever",
            content=str(context_nodes),
            raw_input={"message": condensed_question},
            raw_output=context_nodes,
        )

        return context_source, context_nodes

    async def_arun_c2(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
    ) -> Tuple[ToolOutput, List[NodeWithScore]]:
        if chat_history is not None:
            await self._memory.aset(chat_history)

        chat_history = await self._memory.aget(input=message)

        # Condense conversation history and latest message to a standalone question
        condensed_question = await self._acondense_question(chat_history, message)  # type: ignore
        logger.info(f"Condensed question: {condensed_question}")
        if self._verbose:
            print(f"Condensed question: {condensed_question}")

        # get the context nodes using the condensed question
        context_nodes = await self._aget_nodes(condensed_question)
        context_source = ToolOutput(
            tool_name="retriever",
            content=str(context_nodes),
            raw_input={"message": condensed_question},
            raw_output=context_nodes,
        )

        return context_source, context_nodes

    defsynthesize(
        self,
        query_str: str,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
        streaming: bool = False,
    ) -> RESPONSE_TYPE:
        image_nodes, text_nodes = _get_image_and_text_nodes(nodes)
        context_str = "\n\n".join(
            [r.get_content(metadata_mode=MetadataMode.LLM) for r in text_nodes]
        )
        fmt_prompt = self._context_prompt_template.format(
            context_str=context_str, query_str=query_str
        )

        blocks: List[Union[ImageBlock, TextBlock]] = [
            image_node_to_image_block(image_node.node)
            for image_node in image_nodes
            if isinstance(image_node.node, ImageNode)
        ]

        blocks.append(TextBlock(text=fmt_prompt))

        chat_history = self._memory.get(
            input=query_str,
        )

        if streaming:
            llm_stream = self._multi_modal_llm.stream_chat(
                [
                    ChatMessage(role="system", content=self._system_prompt),
                    *chat_history,
                    ChatMessage(role="user", blocks=blocks),
                ]
            )
            stream_tokens = stream_chat_response_to_tokens(llm_stream)
            return StreamingResponse(
                response_gen=stream_tokens,
                source_nodes=nodes,
                metadata={"text_nodes": text_nodes, "image_nodes": image_nodes},
            )
        else:
            llm_response = self._multi_modal_llm.chat(
                [
                    ChatMessage(role="system", content=self._system_prompt),
                    *chat_history,
                    ChatMessage(role="user", blocks=blocks),
                ]
            )
            output = llm_response.message.content or ""
            return Response(
                response=output,
                source_nodes=nodes,
                metadata={"text_nodes": text_nodes, "image_nodes": image_nodes},
            )

    async defasynthesize(
        self,
        query_str: str,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
        streaming: bool = False,
    ) -> RESPONSE_TYPE:
        image_nodes, text_nodes = _get_image_and_text_nodes(nodes)
        context_str = "\n\n".join(
            [r.get_content(metadata_mode=MetadataMode.LLM) for r in text_nodes]
        )
        fmt_prompt = self._context_prompt_template.format(
            context_str=context_str, query_str=query_str
        )

        blocks: List[Union[ImageBlock, TextBlock]] = [
            image_node_to_image_block(image_node.node)
            for image_node in image_nodes
            if isinstance(image_node.node, ImageNode)
        ]

        blocks.append(TextBlock(text=fmt_prompt))

        chat_history = await self._memory.aget(
            input=query_str,
        )

        if streaming:
            llm_stream = await self._multi_modal_llm.astream_chat(
                [
                    ChatMessage(role="system", content=self._system_prompt),
                    *chat_history,
                    ChatMessage(role="user", blocks=blocks),
                ]
            )
            stream_tokens = await astream_chat_response_to_tokens(llm_stream)
            return AsyncStreamingResponse(
                response_gen=stream_tokens,
                source_nodes=nodes,
                metadata={"text_nodes": text_nodes, "image_nodes": image_nodes},
            )
        else:
            llm_response = await self._multi_modal_llm.achat(
                [
                    ChatMessage(role="system", content=self._system_prompt),
                    *chat_history,
                    ChatMessage(role="user", blocks=blocks),
                ]
            )
            output = llm_response.message.content or ""
            return Response(
                response=output,
                source_nodes=nodes,
                metadata={"text_nodes": text_nodes, "image_nodes": image_nodes},
            )

    @trace_method("chat")
    defchat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> AgentChatResponse:
        context_source, context_nodes = self._run_c2(message, chat_history)

        response = self.synthesize(message, nodes=context_nodes, streaming=False)

        user_message = ChatMessage(content=str(message), role=MessageRole.USER)
        assistant_message = ChatMessage(
            content=str(response), role=MessageRole.ASSISTANT
        )
        self._memory.put(user_message)
        self._memory.put(assistant_message)

        assert context_source.tool_name == "retriever"
        # re-package raw_outputs here to provide image nodes and text nodes separately
        context_source.raw_output = response.metadata

        return AgentChatResponse(
            response=str(response),
            sources=[context_source],
            source_nodes=context_nodes,
        )

    @trace_method("chat")
    defstream_chat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> StreamingAgentChatResponse:
        context_source, context_nodes = self._run_c2(message, chat_history)

        response = self.synthesize(message, nodes=context_nodes, streaming=True)
        assert isinstance(response, StreamingResponse)

        self._memory.put(ChatMessage(content=str(message), role=MessageRole.USER))

        defwrapped_gen(response: StreamingResponse) -> ChatResponseGen:
            full_response = ""
            for token in response.response_gen:
                full_response += token
                yield ChatResponse(
                    message=ChatMessage(
                        content=full_response, role=MessageRole.ASSISTANT
                    ),
                    delta=token,
                )

        assert context_source.tool_name == "retriever"
        # re-package raw_outputs here to provide image nodes and text nodes separately
        context_source.raw_output = response.metadata

        chat_response = StreamingAgentChatResponse(
            chat_stream=wrapped_gen(response),
            sources=[context_source],
            source_nodes=context_nodes,
        )
        thread = Thread(
            target=chat_response.write_response_to_history, args=(self._memory,)
        )
        chat_response.write_response_to_history_thread = thread
        thread.start()
        return chat_response

    @trace_method("chat")
    async defachat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> AgentChatResponse:
        context_source, context_nodes = await self._arun_c2(message, chat_history)

        response = await self.asynthesize(message, nodes=context_nodes, streaming=False)

        user_message = ChatMessage(content=str(message), role=MessageRole.USER)
        assistant_message = ChatMessage(
            content=str(response), role=MessageRole.ASSISTANT
        )
        await self._memory.aput(user_message)
        await self._memory.aput(assistant_message)

        assert context_source.tool_name == "retriever"
        # re-package raw_outputs here to provide image nodes and text nodes separately
        context_source.raw_output = response.metadata

        return AgentChatResponse(
            response=str(response),
            sources=[context_source],
            source_nodes=context_nodes,
        )

    @trace_method("chat")
    async defastream_chat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> StreamingAgentChatResponse:
        context_source, context_nodes = await self._arun_c2(message, chat_history)

        response = await self.asynthesize(message, nodes=context_nodes, streaming=True)
        assert isinstance(response, AsyncStreamingResponse)

        await self._memory.aput(
            ChatMessage(content=str(message), role=MessageRole.USER)
        )

        async defwrapped_gen(response: AsyncStreamingResponse) -> ChatResponseAsyncGen:
            full_response = ""
            async for token in response.async_response_gen():
                full_response += token
                yield ChatResponse(
                    message=ChatMessage(
                        content=full_response, role=MessageRole.ASSISTANT
                    ),
                    delta=token,
                )

        assert context_source.tool_name == "retriever"
        # re-package raw_outputs here to provide image nodes and text nodes separately
        context_source.raw_output = response.metadata

        chat_response = StreamingAgentChatResponse(
            achat_stream=wrapped_gen(response),
            sources=[context_source],
            source_nodes=context_nodes,
        )
        chat_response.awrite_response_to_history_task = asyncio.create_task(
            chat_response.awrite_response_to_history(self._memory)
        )
        return chat_response

    defreset(self) -> None:
        # Clear chat history
        self._memory.reset()

    @property
    defchat_history(self) -> List[ChatMessage]:
"""Get chat history."""
        return self._memory.get_all()

```
 |  
| --- | --- |  
###  chat_history `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.MultiModalCondensePlusContextChatEngine.chat_history "Permanent link")

```
chat_history: []

```

Get chat history.
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/context/#llama_index.core.chat_engine.MultiModalCondensePlusContextChatEngine.from_defaults "Permanent link")

```
from_defaults(
    retriever: ,
    multi_modal_llm: Optional[] = None,
    chat_history: Optional[[]] = None,
    memory: Optional[] = None,
    system_prompt: Optional[] = None,
    context_prompt: Optional[
        Union[, ]
    ] = None,
    condense_prompt: Optional[
        Union[, ]
    ] = None,
    skip_condense:  = False,
    node_postprocessors: Optional[
        []
    ] = None,
    verbose:  = False,
    **kwargs: 
) -> 

```

Initialize a MultiModalCondensePlusContextChatEngine from default parameters.
Source code in `llama-index-core/llama_index/core/chat_engine/multi_modal_condense_plus_context.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    retriever: BaseRetriever,
    multi_modal_llm: Optional[LLM] = None,
    chat_history: Optional[List[ChatMessage]] = None,
    memory: Optional[BaseMemory] = None,
    system_prompt: Optional[str] = None,
    context_prompt: Optional[Union[str, PromptTemplate]] = None,
    condense_prompt: Optional[Union[str, PromptTemplate]] = None,
    skip_condense: bool = False,
    node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
    verbose: bool = False,
    **kwargs: Any,
) -> "MultiModalCondensePlusContextChatEngine":
"""Initialize a MultiModalCondensePlusContextChatEngine from default parameters."""
    multi_modal_llm = multi_modal_llm or Settings.llm

    chat_history = chat_history or []
    memory = memory or Memory.from_defaults(
        chat_history=chat_history,
        token_limit=multi_modal_llm.metadata.context_window - 256,
    )

    return cls(
        retriever=retriever,
        multi_modal_llm=multi_modal_llm,
        memory=memory,
        context_prompt=context_prompt,
        condense_prompt=condense_prompt,
        skip_condense=skip_condense,
        callback_manager=Settings.callback_manager,
        node_postprocessors=node_postprocessors,
        system_prompt=system_prompt,
        verbose=verbose,
    )

```
 |  
| --- | --- |  
options: members: - ContextChatEngine
