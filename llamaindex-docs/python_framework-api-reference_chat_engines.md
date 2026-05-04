# Index
##  ChatResponseMode [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.ChatResponseMode "Permanent link")
Bases: `str`, `Enum`
Flag toggling waiting/streaming in `Agent._chat`.
Source code in `llama-index-core/llama_index/core/chat_engine/types.py`  
| 
```
45
46
47
48
49
```
 | 
```
classChatResponseMode(str, Enum):
"""Flag toggling waiting/streaming in `Agent._chat`."""

    WAIT = "wait"
    STREAM = "stream"

```
 |  
| --- | --- |  
##  AgentChatResponse `dataclass` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.AgentChatResponse "Permanent link")
Agent chat response.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `response`  |  
|  `sources`  |  `List[ToolOutput[](https://developers.llamaindex.ai/python/framework-api-reference/tools/#llama_index.core.tools.types.ToolOutput "ToolOutput \(llama_index.core.tools.ToolOutput\)")]`  |  Built-in mutable sequence. If no argument is given, the constructor creates a new empty list. The argument must be an iterable if specified.  |  `<dynamic>`  |  
|  `source_nodes`  |  `List[NodeWithScore[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.NodeWithScore "NodeWithScore \(llama_index.core.schema.NodeWithScore\)")]`  |  Built-in mutable sequence. If no argument is given, the constructor creates a new empty list. The argument must be an iterable if specified.  |  `<dynamic>`  |  
|  `is_dummy_stream`  |  `bool`  |  `False`  |  
|  `metadata`  |  `Dict[str, Any] | None`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/chat_engine/types.py`  
| 
```
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
```
 | 
```
@dataclass
classAgentChatResponse:
"""Agent chat response."""

    response: str = ""
    sources: List[ToolOutput] = field(default_factory=list)
    source_nodes: List[NodeWithScore] = field(default_factory=list)
    is_dummy_stream: bool = False
    metadata: Optional[Dict[str, Any]] = None

    defset_source_nodes(self) -> None:
        if self.sources and not self.source_nodes:
            for tool_output in self.sources:
                if isinstance(tool_output.raw_output, (Response, StreamingResponse)):
                    self.source_nodes.extend(tool_output.raw_output.source_nodes)

    def__post_init__(self) -> None:
        self.set_source_nodes()

    def__str__(self) -> str:
        return self.response

    @property
    defresponse_gen(self) -> Generator[str, None, None]:
"""Used for fake streaming, i.e. with tool outputs."""
        if not self.is_dummy_stream:
            raise ValueError(
                "response_gen is only available for streaming responses. "
                "Set is_dummy_stream=True if you still want a generator."
            )

        for token in self.response.split(" "):
            yield token + " "
            time.sleep(0.1)

    async defasync_response_gen(self) -> AsyncGenerator[str, None]:
"""Used for fake streaming, i.e. with tool outputs."""
        if not self.is_dummy_stream:
            raise ValueError(
                "response_gen is only available for streaming responses. "
                "Set is_dummy_stream=True if you still want a generator."
            )

        for token in self.response.split(" "):
            yield token + " "
            await asyncio.sleep(0.1)

```
 |  
| --- | --- |  
###  response_gen `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.AgentChatResponse.response_gen "Permanent link")

```
response_gen: Generator[, None, None]

```

Used for fake streaming, i.e. with tool outputs.
###  async_response_gen [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.AgentChatResponse.async_response_gen "Permanent link")

```
async_response_gen() -> AsyncGenerator[, None]

```

Used for fake streaming, i.e. with tool outputs.
Source code in `llama-index-core/llama_index/core/chat_engine/types.py`  
| 
```
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
```
 | 
```
async defasync_response_gen(self) -> AsyncGenerator[str, None]:
"""Used for fake streaming, i.e. with tool outputs."""
    if not self.is_dummy_stream:
        raise ValueError(
            "response_gen is only available for streaming responses. "
            "Set is_dummy_stream=True if you still want a generator."
        )

    for token in self.response.split(" "):
        yield token + " "
        await asyncio.sleep(0.1)

```
 |  
| --- | --- |  
##  StreamingAgentChatResponse `dataclass` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.StreamingAgentChatResponse "Permanent link")
Streaming chat response to user and writing to chat history.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `response`  |  
|  `sources`  |  `List[ToolOutput[](https://developers.llamaindex.ai/python/framework-api-reference/tools/#llama_index.core.tools.types.ToolOutput "ToolOutput \(llama_index.core.tools.ToolOutput\)")]`  |  Built-in mutable sequence. If no argument is given, the constructor creates a new empty list. The argument must be an iterable if specified.  |  `<dynamic>`  |  
|  `chat_stream`  |  `Generator[ChatResponse, None, None] | None`  |  `None`  |  
|  `achat_stream`  |  `AsyncGenerator[ChatResponse, None] | None`  |  `None`  |  
|  `source_nodes`  |  `List[NodeWithScore[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.NodeWithScore "NodeWithScore \(llama_index.core.schema.NodeWithScore\)")]`  |  Built-in mutable sequence. If no argument is given, the constructor creates a new empty list. The argument must be an iterable if specified.  |  `<dynamic>`  |  
|  `unformatted_response`  |  
|  `queue`  |  `Queue`  |  Create a queue object with a given maximum size. If maxsize is <= 0, the queue size is infinite.  |  `<dynamic>`  |  
|  `aqueue`  |  `Queue | None`  |  `None`  |  
|  `is_function`  |  `bool | None`  |  `None`  |  
|  `new_item_event`  |  `Event | None`  |  `None`  |  
|  `is_function_false_event`  |  `Event | None`  |  `None`  |  
|  `is_function_not_none_thread_event`  |  `Event`  |  Class implementing event objects. Events manage a flag that can be set to true with the set() method and reset to false with the clear() method. The wait() method blocks until the flag is true. The flag is initially false.  |  `<threading.Event at 0x7f00aef0a0d0: unset>`  |  
|  `is_writing_to_memory`  |  `bool`  |  `True`  |  
|  `exception`  |  `Exception | None`  |  `None`  |  
|  `awrite_response_to_history_task`  |  `Task | None`  |  `None`  |  
|  `write_response_to_history_thread`  |  `Thread | None`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/chat_engine/types.py`  
| 
```
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
```
 | 
```
@dataclass
classStreamingAgentChatResponse:
"""Streaming chat response to user and writing to chat history."""

    response: str = ""
    sources: List[ToolOutput] = field(default_factory=list)
    chat_stream: Optional[ChatResponseGen] = None
    achat_stream: Optional[ChatResponseAsyncGen] = None
    source_nodes: List[NodeWithScore] = field(default_factory=list)
    unformatted_response: str = ""
    queue: Queue = field(default_factory=Queue)
    aqueue: Optional[asyncio.Queue] = None
    # flag when chat message is a function call
    is_function: Optional[bool] = None
    # flag when processing done
    is_done = False
    # signal when a new item is added to the queue
    new_item_event: Optional[asyncio.Event] = None
    # NOTE: async code uses two events rather than one since it yields
    # control when waiting for queue item
    # signal when the OpenAI functions stop executing
    is_function_false_event: Optional[asyncio.Event] = None
    # signal when an OpenAI function is being executed
    is_function_not_none_thread_event: Event = field(default_factory=Event)
    is_writing_to_memory: bool = True
    # Track if an exception occurred
    exception: Optional[Exception] = None
    awrite_response_to_history_task: Optional[asyncio.Task] = None
    write_response_to_history_thread: Optional[Thread] = None

    defset_source_nodes(self) -> None:
        if self.sources and not self.source_nodes:
            for tool_output in self.sources:
                if isinstance(tool_output.raw_output, (Response, StreamingResponse)):
                    self.source_nodes.extend(tool_output.raw_output.source_nodes)

    def__post_init__(self) -> None:
        self.set_source_nodes()

    def__str__(self) -> str:
        if self.is_done and not self.queue.empty() and not self.is_function:
            while self.queue.queue:
                delta = self.queue.queue.popleft()
                self.unformatted_response += delta
            self.response = self.unformatted_response.strip()
        return self.response

    def_ensure_async_setup(self) -> None:
        if self.aqueue is None:
            self.aqueue = asyncio.Queue()
        if self.new_item_event is None:
            self.new_item_event = asyncio.Event()
        if self.is_function_false_event is None:
            self.is_function_false_event = asyncio.Event()

    defput_in_queue(self, delta: Optional[str]) -> None:
        self.queue.put_nowait(delta)
        self.is_function_not_none_thread_event.set()

    defaput_in_queue(self, delta: Optional[str]) -> None:
        assert self.aqueue is not None
        assert self.new_item_event is not None

        self.aqueue.put_nowait(delta)
        self.new_item_event.set()

    @dispatcher.span
    defwrite_response_to_history(
        self,
        memory: BaseMemory,
        on_stream_end_fn: Optional[Callable] = None,
    ) -> None:
        if self.chat_stream is None:
            raise ValueError(
                "chat_stream is None. Cannot write to history without chat_stream."
            )

        # try/except to prevent hanging on error
        dispatcher.event(StreamChatStartEvent())
        try:
            final_text = ""
            for chat in self.chat_stream:
                self.is_function = is_function(chat.message)
                if chat.delta:
                    dispatcher.event(
                        StreamChatDeltaReceivedEvent(
                            delta=chat.delta,
                        )
                    )
                    self.put_in_queue(chat.delta)
                final_text += chat.delta or ""
            if self.is_function is not None:  # if loop has gone through iteration
                # NOTE: this is to handle the special case where we consume some of the
                # chat stream, but not all of it (e.g. in react agent)
                chat.message.content = final_text.strip()  # final message
                memory.put(chat.message)
        except Exception as e:
            dispatcher.event(StreamChatErrorEvent(exception=e))
            self.exception = e

            # This act as is_done events for any consumers waiting
            self.is_function_not_none_thread_event.set()

            # force the queue reader to see the exception
            self.put_in_queue("")
            raise
        dispatcher.event(StreamChatEndEvent())

        self.is_done = True

        # This act as is_done events for any consumers waiting
        self.is_function_not_none_thread_event.set()
        if on_stream_end_fn is not None and not self.is_function:
            on_stream_end_fn()

    @dispatcher.span
    async defawrite_response_to_history(
        self,
        memory: BaseMemory,
        on_stream_end_fn: Optional[Callable] = None,
    ) -> None:
        self._ensure_async_setup()
        assert self.aqueue is not None
        assert self.is_function_false_event is not None
        assert self.new_item_event is not None

        if self.achat_stream is None:
            raise ValueError(
                "achat_stream is None. Cannot asynchronously write to "
                "history without achat_stream."
            )

        # try/except to prevent hanging on error
        dispatcher.event(StreamChatStartEvent())
        try:
            final_text = ""
            async for chat in self.achat_stream:
                self.is_function = is_function(chat.message)
                if chat.delta:
                    dispatcher.event(
                        StreamChatDeltaReceivedEvent(
                            delta=chat.delta,
                        )
                    )
                    self.aput_in_queue(chat.delta)
                final_text += chat.delta or ""
                self.new_item_event.set()
                if self.is_function is False:
                    self.is_function_false_event.set()
            if self.is_function is not None:  # if loop has gone through iteration
                # NOTE: this is to handle the special case where we consume some of the
                # chat stream, but not all of it (e.g. in react agent)
                chat.message.content = final_text.strip()  # final message
                await memory.aput(chat.message)
        except Exception as e:
            dispatcher.event(StreamChatErrorEvent(exception=e))
            self.exception = e

            # These act as is_done events for any consumers waiting
            self.is_function_false_event.set()
            self.new_item_event.set()

            # force the queue reader to see the exception
            self.aput_in_queue("")
            raise
        dispatcher.event(StreamChatEndEvent())
        self.is_done = True

        # These act as is_done events for any consumers waiting
        self.is_function_false_event.set()
        self.new_item_event.set()
        if on_stream_end_fn is not None and not self.is_function:
            if iscoroutinefunction(
                on_stream_end_fn.func
                if isinstance(on_stream_end_fn, partial)
                else on_stream_end_fn
            ):
                await on_stream_end_fn()
            else:
                on_stream_end_fn()

    @property
    defresponse_gen(self) -> Generator[str, None, None]:
        try:
            yielded_once = False
            if self.is_writing_to_memory:
                while not self.is_done or not self.queue.empty():
                    if self.exception is not None:
                        raise self.exception

                    try:
                        delta = self.queue.get(block=False)
                        self.unformatted_response += delta
                        yield delta
                        yielded_once = True
                    except Empty:
                        time.sleep(0)
            else:
                if self.chat_stream is None:
                    raise ValueError("chat_stream is None!")

                for chat_response in self.chat_stream:
                    self.unformatted_response += chat_response.delta or ""
                    yield chat_response.delta or ""
                    yielded_once = True

            self.response = self.unformatted_response.strip()

            if not yielded_once:
                yield self.response
        finally:
            if self.write_response_to_history_thread is not None:
                self.write_response_to_history_thread.join()
                self.write_response_to_history_thread = None

    async defasync_response_gen(self) -> AsyncGenerator[str, None]:
        try:
            yielded_once = False
            self._ensure_async_setup()
            assert self.aqueue is not None

            if self.is_writing_to_memory:
                while True:
                    if not self.aqueue.empty() or not self.is_done:
                        if self.exception is not None:
                            raise self.exception

                        try:
                            delta = await asyncio.wait_for(
                                self.aqueue.get(), timeout=0.1
                            )
                        except asyncio.TimeoutError:
                            # Break only when the stream is done and the queue is empty
                            if self.is_done and self.aqueue.empty():
                                break
                            continue
                        if delta is not None:
                            self.unformatted_response += delta
                            yield delta
                            yielded_once = True
                    else:
                        break
            else:
                if self.achat_stream is None:
                    raise ValueError("achat_stream is None!")

                async for chat_response in self.achat_stream:
                    self.unformatted_response += chat_response.delta or ""
                    yield chat_response.delta or ""
                    yielded_once = True
            self.response = self.unformatted_response.strip()

            # edge case where the stream was exhausted before yielding anything
            if not yielded_once:
                yield self.response
        finally:
            if self.awrite_response_to_history_task:
                # Make sure that the background task ran to completion, retrieve any exceptions
                await self.awrite_response_to_history_task
                self.awrite_response_to_history_task = (
                    None  # No need to keep the reference to the finished task
                )

    defprint_response_stream(self) -> None:
        for token in self.response_gen:
            print(token, end="", flush=True)

    async defaprint_response_stream(self) -> None:
        async for token in self.async_response_gen():
            print(token, end="", flush=True)

```
 |  
| --- | --- |  
##  BaseChatEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.BaseChatEngine "Permanent link")
Bases: `DispatcherSpanMixin`, 
Base Chat Engine.
Source code in `llama-index-core/llama_index/core/chat_engine/types.py`  
| 
```
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
```
 | 
```
classBaseChatEngine(DispatcherSpanMixin, ABC):
"""Base Chat Engine."""

    @abstractmethod
    defreset(self) -> None:
"""Reset conversation state."""

    @abstractmethod
    defchat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> AGENT_CHAT_RESPONSE_TYPE:
"""Main chat interface."""

    @abstractmethod
    defstream_chat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> StreamingAgentChatResponse:
"""Stream chat interface."""

    @abstractmethod
    async defachat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> AGENT_CHAT_RESPONSE_TYPE:
"""Async version of main chat interface."""

    @abstractmethod
    async defastream_chat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> StreamingAgentChatResponse:
"""Async version of main chat interface."""

    defchat_repl(self) -> None:
"""Enter interactive chat REPL."""
        print("===== Entering Chat REPL =====")
        print('Type "exit" to exit.\n')
        self.reset()
        message = input("Human: ")
        while message != "exit":
            response = self.chat(message)
            print(f"Assistant: {response}\n")
            message = input("Human: ")

    defstreaming_chat_repl(self) -> None:
"""Enter interactive chat REPL with streaming responses."""
        print("===== Entering Chat REPL =====")
        print('Type "exit" to exit.\n')
        self.reset()
        message = input("Human: ")
        while message != "exit":
            response = self.stream_chat(message)
            print("Assistant: ", end="", flush=True)
            response.print_response_stream()
            print("\n")
            message = input("Human: ")

    @property
    @abstractmethod
    defchat_history(self) -> List[ChatMessage]:
        pass

```
 |  
| --- | --- |  
###  reset `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.BaseChatEngine.reset "Permanent link")

```
reset() -> None

```

Reset conversation state.
Source code in `llama-index-core/llama_index/core/chat_engine/types.py`  
| 
```
378
379
380
```
 | 
```
@abstractmethod
defreset(self) -> None:
"""Reset conversation state."""

```
 |  
| --- | --- |  
###  chat `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.BaseChatEngine.chat "Permanent link")

```
chat(
    message: ,
    chat_history: Optional[[]] = None,
) -> AGENT_CHAT_RESPONSE_TYPE

```

Main chat interface.
Source code in `llama-index-core/llama_index/core/chat_engine/types.py`  
| 
```
382
383
384
385
386
```
 | 
```
@abstractmethod
defchat(
    self, message: str, chat_history: Optional[List[ChatMessage]] = None
) -> AGENT_CHAT_RESPONSE_TYPE:
"""Main chat interface."""

```
 |  
| --- | --- |  
###  stream_chat `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.BaseChatEngine.stream_chat "Permanent link")

```
stream_chat(
    message: ,
    chat_history: Optional[[]] = None,
) -> 

```

Stream chat interface.
Source code in `llama-index-core/llama_index/core/chat_engine/types.py`  
| 
```
388
389
390
391
392
```
 | 
```
@abstractmethod
defstream_chat(
    self, message: str, chat_history: Optional[List[ChatMessage]] = None
) -> StreamingAgentChatResponse:
"""Stream chat interface."""

```
 |  
| --- | --- |  
###  achat `abstractmethod` `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.BaseChatEngine.achat "Permanent link")

```
achat(
    message: ,
    chat_history: Optional[[]] = None,
) -> AGENT_CHAT_RESPONSE_TYPE

```

Async version of main chat interface.
Source code in `llama-index-core/llama_index/core/chat_engine/types.py`  
| 
```
394
395
396
397
398
```
 | 
```
@abstractmethod
async defachat(
    self, message: str, chat_history: Optional[List[ChatMessage]] = None
) -> AGENT_CHAT_RESPONSE_TYPE:
"""Async version of main chat interface."""

```
 |  
| --- | --- |  
###  astream_chat `abstractmethod` `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.BaseChatEngine.astream_chat "Permanent link")

```
astream_chat(
    message: ,
    chat_history: Optional[[]] = None,
) -> 

```

Async version of main chat interface.
Source code in `llama-index-core/llama_index/core/chat_engine/types.py`  
| 
```
400
401
402
403
404
```
 | 
```
@abstractmethod
async defastream_chat(
    self, message: str, chat_history: Optional[List[ChatMessage]] = None
) -> StreamingAgentChatResponse:
"""Async version of main chat interface."""

```
 |  
| --- | --- |  
###  chat_repl [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.BaseChatEngine.chat_repl "Permanent link")

```
chat_repl() -> None

```

Enter interactive chat REPL.
Source code in `llama-index-core/llama_index/core/chat_engine/types.py`  
| 
```
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
```
 | 
```
defchat_repl(self) -> None:
"""Enter interactive chat REPL."""
    print("===== Entering Chat REPL =====")
    print('Type "exit" to exit.\n')
    self.reset()
    message = input("Human: ")
    while message != "exit":
        response = self.chat(message)
        print(f"Assistant: {response}\n")
        message = input("Human: ")

```
 |  
| --- | --- |  
###  streaming_chat_repl [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.BaseChatEngine.streaming_chat_repl "Permanent link")

```
streaming_chat_repl() -> None

```

Enter interactive chat REPL with streaming responses.
Source code in `llama-index-core/llama_index/core/chat_engine/types.py`  
| 
```
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
```
 | 
```
defstreaming_chat_repl(self) -> None:
"""Enter interactive chat REPL with streaming responses."""
    print("===== Entering Chat REPL =====")
    print('Type "exit" to exit.\n')
    self.reset()
    message = input("Human: ")
    while message != "exit":
        response = self.stream_chat(message)
        print("Assistant: ", end="", flush=True)
        response.print_response_stream()
        print("\n")
        message = input("Human: ")

```
 |  
| --- | --- |  
##  ChatMode [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.ChatMode "Permanent link")
Bases: `str`, `Enum`
Chat Engine Modes.
Source code in `llama-index-core/llama_index/core/chat_engine/types.py`  
| 
```
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
485
486
487
```
 | 
```
classChatMode(str, Enum):
"""Chat Engine Modes."""

    SIMPLE = "simple"
"""Corresponds to `SimpleChatEngine`.

    Chat with LLM, without making use of a knowledge base.
    """

    CONDENSE_QUESTION = "condense_question"
"""Corresponds to `CondenseQuestionChatEngine`.

    First generate a standalone question from conversation context and last message,
    then query the query engine for a response.
    """

    CONTEXT = "context"
"""Corresponds to `ContextChatEngine`.

    First retrieve text from the index using the user's message, then use the context
    in the system prompt to generate a response.
    """

    CONDENSE_PLUS_CONTEXT = "condense_plus_context"
"""Corresponds to `CondensePlusContextChatEngine`.

    First condense a conversation and latest user message to a standalone question.
    Then build a context for the standalone question from a retriever,
    Then pass the context along with prompt and user message to LLM to generate a response.
    """

    REACT = "react"
"""Corresponds to `ReActAgent`.

    Use a ReAct agent loop with query engine tools.

    NOTE: Deprecated and unsupported.
    """

    OPENAI = "openai"
"""Corresponds to `OpenAIAgent`.

    Use an OpenAI function calling agent loop.

    NOTE: Deprecated and unsupported.
    """

    BEST = "best"
"""Select the best chat engine based on the current LLM.

    Corresponds to `condense_plus_context`
    """

```
 |  
| --- | --- |  
###  SIMPLE `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.ChatMode.SIMPLE "Permanent link")

```
SIMPLE = 'simple'

```

Corresponds to `SimpleChatEngine`.
Chat with LLM, without making use of a knowledge base.
###  CONDENSE_QUESTION `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.ChatMode.CONDENSE_QUESTION "Permanent link")

```
CONDENSE_QUESTION = 'condense_question'

```

Corresponds to `CondenseQuestionChatEngine`.
First generate a standalone question from conversation context and last message, then query the query engine for a response.
###  CONTEXT `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.ChatMode.CONTEXT "Permanent link")

```
CONTEXT = 'context'

```

Corresponds to `ContextChatEngine`.
First retrieve text from the index using the user's message, then use the context in the system prompt to generate a response.
###  CONDENSE_PLUS_CONTEXT `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.ChatMode.CONDENSE_PLUS_CONTEXT "Permanent link")

```
CONDENSE_PLUS_CONTEXT = 'condense_plus_context'

```

Corresponds to `CondensePlusContextChatEngine`.
First condense a conversation and latest user message to a standalone question. Then build a context for the standalone question from a retriever, Then pass the context along with prompt and user message to LLM to generate a response.
###  REACT `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.ChatMode.REACT "Permanent link")

```
REACT = 'react'

```

Corresponds to `ReActAgent`.
Use a ReAct agent loop with query engine tools.
NOTE: Deprecated and unsupported.
###  OPENAI `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.ChatMode.OPENAI "Permanent link")

```
OPENAI = 'openai'

```

Corresponds to `OpenAIAgent`.
Use an OpenAI function calling agent loop.
NOTE: Deprecated and unsupported.
###  BEST `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.ChatMode.BEST "Permanent link")

```
BEST = 'best'

```

Select the best chat engine based on the current LLM.
Corresponds to `condense_plus_context`
##  is_function [#](https://developers.llamaindex.ai/python/framework-api-reference/chat_engines/#llama_index.core.chat_engine.types.is_function "Permanent link")

```
is_function(message: ) -> 

```

Utility for ChatMessage responses from OpenAI models.
Source code in `llama-index-core/llama_index/core/chat_engine/types.py`  
| 
```
37
38
39
40
41
42
```
 | 
```
defis_function(message: ChatMessage) -> bool:
"""Utility for ChatMessage responses from OpenAI models."""
    return (
        "tool_calls" in message.additional_kwargs
        and len(message.additional_kwargs["tool_calls"])  0
    )

```
 |  
| --- | --- |
