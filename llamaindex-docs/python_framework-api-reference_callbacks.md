# Core Callback Classes[#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#core-callback-classes "Permanent link")
##  CallbackManager [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "Permanent link")
Bases: , 
Callback manager that handles callbacks for events within LlamaIndex.
The callback manager provides a way to call handlers on event starts/ends.
Additionally, the callback manager traces the current stack of events. It does this by using a few key attributes. - trace_stack - The current stack of events that have not ended yet. When an event ends, it's removed from the stack. Since this is a contextvar, it is unique to each thread/task. - trace_map - A mapping of event ids to their children events. On the start of events, the bottom of the trace stack is used as the current parent event for the trace map. - trace_id - A simple name for the current trace, usually denoting the entrypoint (query, index_construction, insert, etc.)
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `handlers`  |  `List[BaseCallbackHandler[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base_handler.BaseCallbackHandler "BaseCallbackHandler \(llama_index.core.callbacks.base_handler.BaseCallbackHandler\)")]`  |  list of handlers to use.  |  `None`  |  
Usage
with callback_manager.event(CBEventType.QUERY) as event: event.on_start(payload={key, val}) ... event.on_end(payload={key, val})
Source code in `llama-index-core/llama_index/core/callbacks/base.py`  
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
```
 | 
```
classCallbackManager(BaseCallbackHandler, ABC):
"""
    Callback manager that handles callbacks for events within LlamaIndex.

    The callback manager provides a way to call handlers on event starts/ends.

    Additionally, the callback manager traces the current stack of events.
    It does this by using a few key attributes.
    - trace_stack - The current stack of events that have not ended yet.
                    When an event ends, it's removed from the stack.
                    Since this is a contextvar, it is unique to each
                    thread/task.
    - trace_map - A mapping of event ids to their children events.
                  On the start of events, the bottom of the trace stack
                  is used as the current parent event for the trace map.
    - trace_id - A simple name for the current trace, usually denoting the
                 entrypoint (query, index_construction, insert, etc.)

    Args:
        handlers (List[BaseCallbackHandler]): list of handlers to use.

    Usage:
        with callback_manager.event(CBEventType.QUERY) as event:
            event.on_start(payload={key, val})

            event.on_end(payload={key, val})

    """

    def__init__(self, handlers: Optional[List[BaseCallbackHandler]] = None):
"""Initialize the manager with a list of handlers."""
        fromllama_index.coreimport global_handler

        handlers = handlers or []

        # add eval handlers based on global defaults
        if global_handler is not None:
            new_handler = global_handler
            # go through existing handlers, check if any are same type as new handler
            # if so, error
            for existing_handler in handlers:
                if isinstance(existing_handler, type(new_handler)):
                    raise ValueError(
                        "Cannot add two handlers of the same type "
                        f"{type(new_handler)} to the callback manager."
                    )
            handlers.append(new_handler)

        # if we passed in no handlers, use the global default
        if len(handlers) == 0:
            fromllama_index.core.settingsimport Settings

            # hidden var access to prevent recursion in getter
            cb_manager = Settings._callback_manager
            if cb_manager is not None:
                handlers = cb_manager.handlers

        self.handlers: List[BaseCallbackHandler] = handlers
        self._trace_map: Dict[str, List[str]] = defaultdict(list)

    defon_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
"""Run handlers when an event starts and return id of event."""
        event_id = event_id or str(uuid.uuid4())

        # if no trace is running, start a default trace
        try:
            parent_id = parent_id or global_stack_trace.get()[-1]
        except IndexError:
            self.start_trace("llama-index")
            parent_id = global_stack_trace.get()[-1]
        parent_id = cast(str, parent_id)
        self._trace_map[parent_id].append(event_id)
        for handler in self.handlers:
            if event_type not in handler.event_starts_to_ignore:
                handler.on_event_start(
                    event_type,
                    payload,
                    event_id=event_id,
                    parent_id=parent_id,
                    **kwargs,
                )

        if event_type not in LEAF_EVENTS:
            # copy the stack trace to prevent conflicts with threads/coroutines
            current_trace_stack = global_stack_trace.get().copy()
            current_trace_stack.append(event_id)
            global_stack_trace.set(current_trace_stack)

        return event_id

    defon_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
"""Run handlers when an event ends."""
        event_id = event_id or str(uuid.uuid4())
        for handler in self.handlers:
            if event_type not in handler.event_ends_to_ignore:
                handler.on_event_end(event_type, payload, event_id=event_id, **kwargs)

        if event_type not in LEAF_EVENTS:
            # copy the stack trace to prevent conflicts with threads/coroutines
            current_trace_stack = global_stack_trace.get().copy()
            current_trace_stack.pop()
            global_stack_trace.set(current_trace_stack)

    defadd_handler(self, handler: BaseCallbackHandler) -> None:
"""Add a handler to the callback manager."""
        self.handlers.append(handler)

    defremove_handler(self, handler: BaseCallbackHandler) -> None:
"""Remove a handler from the callback manager."""
        self.handlers.remove(handler)

    defset_handlers(self, handlers: List[BaseCallbackHandler]) -> None:
"""Set handlers as the only handlers on the callback manager."""
        self.handlers = handlers

    @contextmanager
    defevent(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: Optional[str] = None,
    ) -> Generator["EventContext", None, None]:
"""
        Context manager for lanching and shutdown of events.

        Handles sending on_evnt_start and on_event_end to handlers for specified event.

        Usage:
            with callback_manager.event(CBEventType.QUERY, payload={key, val}) as event:

                event.on_end(payload={key, val})  # optional
        """
        # create event context wrapper
        event = EventContext(self, event_type, event_id=event_id)
        event.on_start(payload=payload)

        payload = None
        try:
            yield event
        except Exception as e:
            # data already logged to trace?
            if not hasattr(e, "event_added"):
                payload = {EventPayload.EXCEPTION: e}
                e.event_added = True  # type: ignore
                if not event.finished:
                    event.on_end(payload=payload)
            raise
        finally:
            # ensure event is ended
            if not event.finished:
                event.on_end(payload=payload)

    @contextmanager
    defas_trace(self, trace_id: str) -> Generator[None, None, None]:
"""Context manager tracer for lanching and shutdown of traces."""
        self.start_trace(trace_id=trace_id)

        try:
            yield
        except Exception as e:
            # event already added to trace?
            if not hasattr(e, "event_added"):
                self.on_event_start(
                    CBEventType.EXCEPTION, payload={EventPayload.EXCEPTION: e}
                )
                e.event_added = True  # type: ignore

            raise
        finally:
            # ensure trace is ended
            self.end_trace(trace_id=trace_id)

    defstart_trace(self, trace_id: Optional[str] = None) -> None:
"""Run when an overall trace is launched."""
        current_trace_stack_ids = global_stack_trace_ids.get().copy()
        if trace_id is not None:
            if len(current_trace_stack_ids) == 0:
                self._reset_trace_events()

                for handler in self.handlers:
                    handler.start_trace(trace_id=trace_id)

                current_trace_stack_ids = [trace_id]
            else:
                current_trace_stack_ids.append(trace_id)

        global_stack_trace_ids.set(current_trace_stack_ids)

    defend_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
"""Run when an overall trace is exited."""
        current_trace_stack_ids = global_stack_trace_ids.get().copy()
        if trace_id is not None and len(current_trace_stack_ids)  0:
            current_trace_stack_ids.pop()
            if len(current_trace_stack_ids) == 0:
                for handler in self.handlers:
                    handler.end_trace(trace_id=trace_id, trace_map=self._trace_map)
                current_trace_stack_ids = []

        global_stack_trace_ids.set(current_trace_stack_ids)

    def_reset_trace_events(self) -> None:
"""Helper function to reset the current trace."""
        self._trace_map = defaultdict(list)
        global_stack_trace.set([BASE_TRACE_EVENT])

    @property
    deftrace_map(self) -> Dict[str, List[str]]:
        return self._trace_map

    @classmethod
    def__get_pydantic_core_schema__(
        cls, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.any_schema()

    @classmethod
    def__get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> Dict[str, Any]:
        json_schema = handler(core_schema)
        return handler.resolve_ref_schema(json_schema)

```
 |  
| --- | --- |  
###  on_event_start [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager.on_event_start "Permanent link")

```
on_event_start(
    event_type: ,
    payload: Optional[[, ]] = None,
    event_id: Optional[] = None,
    parent_id: Optional[] = None,
    **kwargs: 
) -> 

```

Run handlers when an event starts and return id of event.
Source code in `llama-index-core/llama_index/core/callbacks/base.py`  
| 
```
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
```
 | 
```
defon_event_start(
    self,
    event_type: CBEventType,
    payload: Optional[Dict[str, Any]] = None,
    event_id: Optional[str] = None,
    parent_id: Optional[str] = None,
    **kwargs: Any,
) -> str:
"""Run handlers when an event starts and return id of event."""
    event_id = event_id or str(uuid.uuid4())

    # if no trace is running, start a default trace
    try:
        parent_id = parent_id or global_stack_trace.get()[-1]
    except IndexError:
        self.start_trace("llama-index")
        parent_id = global_stack_trace.get()[-1]
    parent_id = cast(str, parent_id)
    self._trace_map[parent_id].append(event_id)
    for handler in self.handlers:
        if event_type not in handler.event_starts_to_ignore:
            handler.on_event_start(
                event_type,
                payload,
                event_id=event_id,
                parent_id=parent_id,
                **kwargs,
            )

    if event_type not in LEAF_EVENTS:
        # copy the stack trace to prevent conflicts with threads/coroutines
        current_trace_stack = global_stack_trace.get().copy()
        current_trace_stack.append(event_id)
        global_stack_trace.set(current_trace_stack)

    return event_id

```
 |  
| --- | --- |  
###  on_event_end [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager.on_event_end "Permanent link")

```
on_event_end(
    event_type: ,
    payload: Optional[[, ]] = None,
    event_id: Optional[] = None,
    **kwargs: 
) -> None

```

Run handlers when an event ends.
Source code in `llama-index-core/llama_index/core/callbacks/base.py`  
| 
```
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
```
 | 
```
defon_event_end(
    self,
    event_type: CBEventType,
    payload: Optional[Dict[str, Any]] = None,
    event_id: Optional[str] = None,
    **kwargs: Any,
) -> None:
"""Run handlers when an event ends."""
    event_id = event_id or str(uuid.uuid4())
    for handler in self.handlers:
        if event_type not in handler.event_ends_to_ignore:
            handler.on_event_end(event_type, payload, event_id=event_id, **kwargs)

    if event_type not in LEAF_EVENTS:
        # copy the stack trace to prevent conflicts with threads/coroutines
        current_trace_stack = global_stack_trace.get().copy()
        current_trace_stack.pop()
        global_stack_trace.set(current_trace_stack)

```
 |  
| --- | --- |  
###  add_handler [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager.add_handler "Permanent link")

```
add_handler(handler: ) -> None

```

Add a handler to the callback manager.
Source code in `llama-index-core/llama_index/core/callbacks/base.py`  
| 
```
144
145
146
```
 | 
```
defadd_handler(self, handler: BaseCallbackHandler) -> None:
"""Add a handler to the callback manager."""
    self.handlers.append(handler)

```
 |  
| --- | --- |  
###  remove_handler [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager.remove_handler "Permanent link")

```
remove_handler(handler: ) -> None

```

Remove a handler from the callback manager.
Source code in `llama-index-core/llama_index/core/callbacks/base.py`  
| 
```
148
149
150
```
 | 
```
defremove_handler(self, handler: BaseCallbackHandler) -> None:
"""Remove a handler from the callback manager."""
    self.handlers.remove(handler)

```
 |  
| --- | --- |  
###  set_handlers [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager.set_handlers "Permanent link")

```
set_handlers(handlers: []) -> None

```

Set handlers as the only handlers on the callback manager.
Source code in `llama-index-core/llama_index/core/callbacks/base.py`  
| 
```
152
153
154
```
 | 
```
defset_handlers(self, handlers: List[BaseCallbackHandler]) -> None:
"""Set handlers as the only handlers on the callback manager."""
    self.handlers = handlers

```
 |  
| --- | --- |  
###  event [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager.event "Permanent link")

```
event(
    event_type: ,
    payload: Optional[[, ]] = None,
    event_id: Optional[] = None,
) -> Generator[, None, None]

```

Context manager for lanching and shutdown of events.
Handles sending on_evnt_start and on_event_end to handlers for specified event.
Usage
with callback_manager.event(CBEventType.QUERY, payload={key, val}) as event: ... event.on_end(payload={key, val}) # optional
Source code in `llama-index-core/llama_index/core/callbacks/base.py`  
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
```
 | 
```
@contextmanager
defevent(
    self,
    event_type: CBEventType,
    payload: Optional[Dict[str, Any]] = None,
    event_id: Optional[str] = None,
) -> Generator["EventContext", None, None]:
"""
    Context manager for lanching and shutdown of events.

    Handles sending on_evnt_start and on_event_end to handlers for specified event.

    Usage:
        with callback_manager.event(CBEventType.QUERY, payload={key, val}) as event:

            event.on_end(payload={key, val})  # optional
    """
    # create event context wrapper
    event = EventContext(self, event_type, event_id=event_id)
    event.on_start(payload=payload)

    payload = None
    try:
        yield event
    except Exception as e:
        # data already logged to trace?
        if not hasattr(e, "event_added"):
            payload = {EventPayload.EXCEPTION: e}
            e.event_added = True  # type: ignore
            if not event.finished:
                event.on_end(payload=payload)
        raise
    finally:
        # ensure event is ended
        if not event.finished:
            event.on_end(payload=payload)

```
 |  
| --- | --- |  
###  as_trace [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager.as_trace "Permanent link")

```
as_trace(trace_id: ) -> Generator[None, None, None]

```

Context manager tracer for lanching and shutdown of traces.
Source code in `llama-index-core/llama_index/core/callbacks/base.py`  
| 
```
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
```
 | 
```
@contextmanager
defas_trace(self, trace_id: str) -> Generator[None, None, None]:
"""Context manager tracer for lanching and shutdown of traces."""
    self.start_trace(trace_id=trace_id)

    try:
        yield
    except Exception as e:
        # event already added to trace?
        if not hasattr(e, "event_added"):
            self.on_event_start(
                CBEventType.EXCEPTION, payload={EventPayload.EXCEPTION: e}
            )
            e.event_added = True  # type: ignore

        raise
    finally:
        # ensure trace is ended
        self.end_trace(trace_id=trace_id)

```
 |  
| --- | --- |  
###  start_trace [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager.start_trace "Permanent link")

```
start_trace(trace_id: Optional[] = None) -> None

```

Run when an overall trace is launched.
Source code in `llama-index-core/llama_index/core/callbacks/base.py`  
| 
```
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
```
 | 
```
defstart_trace(self, trace_id: Optional[str] = None) -> None:
"""Run when an overall trace is launched."""
    current_trace_stack_ids = global_stack_trace_ids.get().copy()
    if trace_id is not None:
        if len(current_trace_stack_ids) == 0:
            self._reset_trace_events()

            for handler in self.handlers:
                handler.start_trace(trace_id=trace_id)

            current_trace_stack_ids = [trace_id]
        else:
            current_trace_stack_ids.append(trace_id)

    global_stack_trace_ids.set(current_trace_stack_ids)

```
 |  
| --- | --- |  
###  end_trace [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager.end_trace "Permanent link")

```
end_trace(
    trace_id: Optional[] = None,
    trace_map: Optional[[, []]] = None,
) -> None

```

Run when an overall trace is exited.
Source code in `llama-index-core/llama_index/core/callbacks/base.py`  
| 
```
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
```
 | 
```
defend_trace(
    self,
    trace_id: Optional[str] = None,
    trace_map: Optional[Dict[str, List[str]]] = None,
) -> None:
"""Run when an overall trace is exited."""
    current_trace_stack_ids = global_stack_trace_ids.get().copy()
    if trace_id is not None and len(current_trace_stack_ids)  0:
        current_trace_stack_ids.pop()
        if len(current_trace_stack_ids) == 0:
            for handler in self.handlers:
                handler.end_trace(trace_id=trace_id, trace_map=self._trace_map)
            current_trace_stack_ids = []

    global_stack_trace_ids.set(current_trace_stack_ids)

```
 |  
| --- | --- |  
##  EventContext [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.EventContext "Permanent link")
Simple wrapper to call callbacks on event starts and ends with an event type and id.
Source code in `llama-index-core/llama_index/core/callbacks/base.py`  
| 
```
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
```
 | 
```
classEventContext:
"""
    Simple wrapper to call callbacks on event starts and ends
    with an event type and id.
    """

    def__init__(
        self,
        callback_manager: CallbackManager,
        event_type: CBEventType,
        event_id: Optional[str] = None,
    ):
        self._callback_manager = callback_manager
        self._event_type = event_type
        self._event_id = event_id or str(uuid.uuid4())
        self.started = False
        self.finished = False

    defon_start(self, payload: Optional[Dict[str, Any]] = None, **kwargs: Any) -> None:
        if not self.started:
            self.started = True
            self._callback_manager.on_event_start(
                self._event_type, payload=payload, event_id=self._event_id, **kwargs
            )
        else:
            logger.warning(
                f"Event {self._event_type!s}: {self._event_id} already started!"
            )

    defon_end(self, payload: Optional[Dict[str, Any]] = None, **kwargs: Any) -> None:
        if not self.finished:
            self.finished = True
            self._callback_manager.on_event_end(
                self._event_type, payload=payload, event_id=self._event_id, **kwargs
            )

```
 |  
| --- | --- |  
options: members: - CallbackManager
##  BaseCallbackHandler [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base_handler.BaseCallbackHandler "Permanent link")
Bases: 
Base callback handler that can be used to track event starts and ends.
Source code in `llama-index-core/llama_index/core/callbacks/base_handler.py`  
| 
```
12
13
14
15
16
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
```
 | 
```
classBaseCallbackHandler(ABC):
"""Base callback handler that can be used to track event starts and ends."""

    def__init__(
        self,
        event_starts_to_ignore: List[CBEventType],
        event_ends_to_ignore: List[CBEventType],
    ) -> None:
"""Initialize the base callback handler."""
        self.event_starts_to_ignore = tuple(event_starts_to_ignore)
        self.event_ends_to_ignore = tuple(event_ends_to_ignore)

    @abstractmethod
    defon_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
"""Run when an event starts and return id of event."""

    @abstractmethod
    defon_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
"""Run when an event ends."""

    @abstractmethod
    defstart_trace(self, trace_id: Optional[str] = None) -> None:
"""Run when an overall trace is launched."""

    @abstractmethod
    defend_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
"""Run when an overall trace is exited."""

```
 |  
| --- | --- |  
###  on_event_start `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base_handler.BaseCallbackHandler.on_event_start "Permanent link")

```
on_event_start(
    event_type: ,
    payload: Optional[[, ]] = None,
    event_id:  = "",
    parent_id:  = "",
    **kwargs: 
) -> 

```

Run when an event starts and return id of event.
Source code in `llama-index-core/llama_index/core/callbacks/base_handler.py`  
| 
```
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
```
 | 
```
@abstractmethod
defon_event_start(
    self,
    event_type: CBEventType,
    payload: Optional[Dict[str, Any]] = None,
    event_id: str = "",
    parent_id: str = "",
    **kwargs: Any,
) -> str:
"""Run when an event starts and return id of event."""

```
 |  
| --- | --- |  
###  on_event_end `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base_handler.BaseCallbackHandler.on_event_end "Permanent link")

```
on_event_end(
    event_type: ,
    payload: Optional[[, ]] = None,
    event_id:  = "",
    **kwargs: 
) -> None

```

Run when an event ends.
Source code in `llama-index-core/llama_index/core/callbacks/base_handler.py`  
| 
```
35
36
37
38
39
40
41
42
43
```
 | 
```
@abstractmethod
defon_event_end(
    self,
    event_type: CBEventType,
    payload: Optional[Dict[str, Any]] = None,
    event_id: str = "",
    **kwargs: Any,
) -> None:
"""Run when an event ends."""

```
 |  
| --- | --- |  
###  start_trace `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base_handler.BaseCallbackHandler.start_trace "Permanent link")

```
start_trace(trace_id: Optional[] = None) -> None

```

Run when an overall trace is launched.
Source code in `llama-index-core/llama_index/core/callbacks/base_handler.py`  
| 
```
45
46
47
```
 | 
```
@abstractmethod
defstart_trace(self, trace_id: Optional[str] = None) -> None:
"""Run when an overall trace is launched."""

```
 |  
| --- | --- |  
###  end_trace `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base_handler.BaseCallbackHandler.end_trace "Permanent link")

```
end_trace(
    trace_id: Optional[] = None,
    trace_map: Optional[[, []]] = None,
) -> None

```

Run when an overall trace is exited.
Source code in `llama-index-core/llama_index/core/callbacks/base_handler.py`  
| 
```
49
50
51
52
53
54
55
```
 | 
```
@abstractmethod
defend_trace(
    self,
    trace_id: Optional[str] = None,
    trace_map: Optional[Dict[str, List[str]]] = None,
) -> None:
"""Run when an overall trace is exited."""

```
 |  
| --- | --- |  
options: members: - BaseCallbackHandler
Base schema for callback managers.
##  CBEventType [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.schema.CBEventType "Permanent link")
Bases: `str`, `Enum`
Callback manager event types.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `CHUNKING`  |  Logs for the before and after of text splitting.  |  
| `NODE_PARSING`  |  Logs for the documents and the nodes that they are parsed into.  |  
| `EMBEDDING`  |  Logs for the number of texts embedded.  |  
|  Logs for the template and response of LLM calls.  |  
| `QUERY`  |  Keeps track of the start and end of each query.  |  
| `RETRIEVE`  |  Logs for the nodes retrieved for a query.  |  
| `SYNTHESIZE`  |  Logs for the result for synthesize calls.  |  
|  Logs for the summary and level of summaries generated.  |  
| `SUB_QUESTION`  |  Logs for a generated sub question and answer.  |  
Source code in `llama-index-core/llama_index/core/callbacks/schema.py`  
| 
```
16
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
```
 | 
```
classCBEventType(str, Enum):
"""
    Callback manager event types.

    Attributes:
        CHUNKING: Logs for the before and after of text splitting.
        NODE_PARSING: Logs for the documents and the nodes that they are parsed into.
        EMBEDDING: Logs for the number of texts embedded.
        LLM: Logs for the template and response of LLM calls.
        QUERY: Keeps track of the start and end of each query.
        RETRIEVE: Logs for the nodes retrieved for a query.
        SYNTHESIZE: Logs for the result for synthesize calls.
        TREE: Logs for the summary and level of summaries generated.
        SUB_QUESTION: Logs for a generated sub question and answer.

    """

    CHUNKING = "chunking"
    NODE_PARSING = "node_parsing"
    EMBEDDING = "embedding"
    LLM = "llm"
    QUERY = "query"
    RETRIEVE = "retrieve"
    SYNTHESIZE = "synthesize"
    TREE = "tree"
    SUB_QUESTION = "sub_question"
    TEMPLATING = "templating"
    FUNCTION_CALL = "function_call"
    RERANKING = "reranking"
    EXCEPTION = "exception"
    AGENT_STEP = "agent_step"

```
 |  
| --- | --- |  
##  CBEvent `dataclass` [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.schema.CBEvent "Permanent link")
Generic class to store event information.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `event_type`  |   |  _required_  |  
|  `payload`  |  `Dict[str, Any] | None`  |  `None`  |  
|  `time`  |  
|  `id_`  |  
Source code in `llama-index-core/llama_index/core/callbacks/schema.py`  
| 
```
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
```
 | 
```
@dataclass
classCBEvent:
"""Generic class to store event information."""

    event_type: CBEventType
    payload: Optional[Dict[str, Any]] = None
    time: str = ""
    id_: str = ""

    def__post_init__(self) -> None:
"""Init time and id if needed."""
        if not self.time:
            self.time = datetime.now().strftime(TIMESTAMP_FORMAT)
        if not self.id_:
            self.id = str(uuid.uuid4())

```
 |  
| --- | --- |  
##  EventStats `dataclass` [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.schema.EventStats "Permanent link")
Time-based Statistics for events.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `total_secs`  |  `float`  |  _required_  |  
|  `average_secs`  |  `float`  |  _required_  |  
|  `total_count`  |  _required_  |  
Source code in `llama-index-core/llama_index/core/callbacks/schema.py`  
| 
```
 95
 96
 97
 98
 99
100
101
```
 | 
```
@dataclass
classEventStats:
"""Time-based Statistics for events."""

    total_secs: float
    average_secs: float
    total_count: int

```
 |  
| --- | --- |  
options: members: - CBEvent - CBEventType - EventPayload
