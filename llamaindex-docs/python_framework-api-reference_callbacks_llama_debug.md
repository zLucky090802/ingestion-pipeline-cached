# Llama debug
##  LlamaDebugHandler [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/llama_debug/#llama_index.core.callbacks.llama_debug.LlamaDebugHandler "Permanent link")
Bases: `PythonicallyPrintingBaseHandler`
Callback handler that keeps track of debug info.
NOTE: this is a beta feature. The usage within our codebase, and the interface may change.
This handler simply keeps track of event starts/ends, separated by event types. You can use this callback handler to keep track of and debug events.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `event_starts_to_ignore`  |  `Optional[List[CBEventType[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.schema.CBEventType "CBEventType \(llama_index.core.callbacks.schema.CBEventType\)")]]`  |  list of event types to ignore when tracking event starts.  |  `None`  |  
|  `event_ends_to_ignore`  |  `Optional[List[CBEventType[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.schema.CBEventType "CBEventType \(llama_index.core.callbacks.schema.CBEventType\)")]]`  |  list of event types to ignore when tracking event ends.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/callbacks/llama_debug.py`  
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
```
 | 
```
classLlamaDebugHandler(PythonicallyPrintingBaseHandler):
"""
    Callback handler that keeps track of debug info.

    NOTE: this is a beta feature. The usage within our codebase, and the interface
    may change.

    This handler simply keeps track of event starts/ends, separated by event types.
    You can use this callback handler to keep track of and debug events.

    Args:
        event_starts_to_ignore (Optional[List[CBEventType]]): list of event types to
            ignore when tracking event starts.
        event_ends_to_ignore (Optional[List[CBEventType]]): list of event types to
            ignore when tracking event ends.

    """

    def__init__(
        self,
        event_starts_to_ignore: Optional[List[CBEventType]] = None,
        event_ends_to_ignore: Optional[List[CBEventType]] = None,
        print_trace_on_end: bool = True,
        logger: Optional[logging.Logger] = None,
    ) -> None:
"""Initialize the llama debug handler."""
        self._event_pairs_by_type: Dict[CBEventType, List[CBEvent]] = defaultdict(list)
        self._event_pairs_by_id: Dict[str, List[CBEvent]] = defaultdict(list)
        self._sequential_events: List[CBEvent] = []
        self._cur_trace_id: Optional[str] = None
        self._trace_map: Dict[str, List[str]] = defaultdict(list)
        self.print_trace_on_end = print_trace_on_end
        event_starts_to_ignore = (
            event_starts_to_ignore if event_starts_to_ignore else []
        )
        event_ends_to_ignore = event_ends_to_ignore if event_ends_to_ignore else []
        super().__init__(
            event_starts_to_ignore=event_starts_to_ignore,
            event_ends_to_ignore=event_ends_to_ignore,
            logger=logger,
        )

    defon_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
"""
        Store event start data by event type.

        Args:
            event_type (CBEventType): event type to store.
            payload (Optional[Dict[str, Any]]): payload to store.
            event_id (str): event id to store.
            parent_id (str): parent event id.

        """
        event = CBEvent(event_type, payload=payload, id_=event_id)
        self._event_pairs_by_type[event.event_type].append(event)
        self._event_pairs_by_id[event.id_].append(event)
        self._sequential_events.append(event)
        return event.id_

    defon_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
"""
        Store event end data by event type.

        Args:
            event_type (CBEventType): event type to store.
            payload (Optional[Dict[str, Any]]): payload to store.
            event_id (str): event id to store.

        """
        event = CBEvent(event_type, payload=payload, id_=event_id)
        self._event_pairs_by_type[event.event_type].append(event)
        self._event_pairs_by_id[event.id_].append(event)
        self._sequential_events.append(event)
        self._trace_map = defaultdict(list)

    defget_events(self, event_type: Optional[CBEventType] = None) -> List[CBEvent]:
"""Get all events for a specific event type."""
        if event_type is not None:
            return self._event_pairs_by_type[event_type]

        return self._sequential_events

    def_get_event_pairs(self, events: List[CBEvent]) -> List[List[CBEvent]]:
"""Helper function to pair events according to their ID."""
        event_pairs: Dict[str, List[CBEvent]] = defaultdict(list)
        for event in events:
            event_pairs[event.id_].append(event)

        return sorted(
            event_pairs.values(),
            key=lambda x: datetime.strptime(x[0].time, TIMESTAMP_FORMAT),
        )

    def_get_time_stats_from_event_pairs(
        self, event_pairs: List[List[CBEvent]]
    ) -> EventStats:
"""Calculate time-based stats for a set of event pairs."""
        if not event_pairs:
            return EventStats(total_secs=0.0, average_secs=0.0, total_count=0)

        total_secs = 0.0
        for event_pair in event_pairs:
            start_time = datetime.strptime(event_pair[0].time, TIMESTAMP_FORMAT)
            end_time = datetime.strptime(event_pair[-1].time, TIMESTAMP_FORMAT)
            total_secs += (end_time - start_time).total_seconds()

        return EventStats(
            total_secs=total_secs,
            average_secs=total_secs / len(event_pairs),
            total_count=len(event_pairs),
        )

    defget_event_pairs(
        self, event_type: Optional[CBEventType] = None
    ) -> List[List[CBEvent]]:
"""Pair events by ID, either all events or a specific type."""
        if event_type is not None:
            return self._get_event_pairs(self._event_pairs_by_type[event_type])

        return self._get_event_pairs(self._sequential_events)

    defget_llm_inputs_outputs(self) -> List[List[CBEvent]]:
"""Get the exact LLM inputs and outputs."""
        return self._get_event_pairs(self._event_pairs_by_type[CBEventType.LLM])

    defget_event_time_info(
        self, event_type: Optional[CBEventType] = None
    ) -> EventStats:
        event_pairs = self.get_event_pairs(event_type)
        return self._get_time_stats_from_event_pairs(event_pairs)

    defflush_event_logs(self) -> None:
"""Clear all events from memory."""
        self._event_pairs_by_type = defaultdict(list)
        self._event_pairs_by_id = defaultdict(list)
        self._sequential_events = []

    defstart_trace(self, trace_id: Optional[str] = None) -> None:
"""Launch a trace."""
        self._trace_map = defaultdict(list)
        self._cur_trace_id = trace_id

    defend_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
"""Shutdown the current trace."""
        self._trace_map = trace_map or defaultdict(list)
        if self.print_trace_on_end:
            self.print_trace_map()

    def_print_trace_map(self, cur_event_id: str, level: int = 0) -> None:
"""Recursively print trace map to terminal for debugging."""
        event_pair = self._event_pairs_by_id[cur_event_id]
        if event_pair:
            time_stats = self._get_time_stats_from_event_pairs([event_pair])
            indent = " " * level * 2
            self._print(
                f"{indent}|_{event_pair[0].event_type} -> {time_stats.total_secs} seconds",
            )

        child_event_ids = self._trace_map[cur_event_id]
        for child_event_id in child_event_ids:
            self._print_trace_map(child_event_id, level=level + 1)

    defprint_trace_map(self) -> None:
"""Print simple trace map to terminal for debugging of the most recent trace."""
        self._print("*" * 10)
        self._print(f"Trace: {self._cur_trace_id}")
        self._print_trace_map(BASE_TRACE_EVENT, level=1)
        self._print("*" * 10)

    @property
    defevent_pairs_by_type(self) -> Dict[CBEventType, List[CBEvent]]:
        return self._event_pairs_by_type

    @property
    defevents_pairs_by_id(self) -> Dict[str, List[CBEvent]]:
        return self._event_pairs_by_id

    @property
    defsequential_events(self) -> List[CBEvent]:
        return self._sequential_events

```
 |  
| --- | --- |  
###  on_event_start [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/llama_debug/#llama_index.core.callbacks.llama_debug.LlamaDebugHandler.on_event_start "Permanent link")

```
on_event_start(
    event_type: ,
    payload: Optional[[, ]] = None,
    event_id:  = "",
    parent_id:  = "",
    **kwargs: 
) -> 

```

Store event start data by event type.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `event_type`  |   |  event type to store.  |  _required_  |  
|  `payload`  |  `Optional[Dict[str, Any]]`  |  payload to store.  |  `None`  |  
|  `event_id`  |  event id to store.  |  
|  `parent_id`  |  parent event id.  |  
Source code in `llama-index-core/llama_index/core/callbacks/llama_debug.py`  
| 
```
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
```
 | 
```
defon_event_start(
    self,
    event_type: CBEventType,
    payload: Optional[Dict[str, Any]] = None,
    event_id: str = "",
    parent_id: str = "",
    **kwargs: Any,
) -> str:
"""
    Store event start data by event type.

    Args:
        event_type (CBEventType): event type to store.
        payload (Optional[Dict[str, Any]]): payload to store.
        event_id (str): event id to store.
        parent_id (str): parent event id.

    """
    event = CBEvent(event_type, payload=payload, id_=event_id)
    self._event_pairs_by_type[event.event_type].append(event)
    self._event_pairs_by_id[event.id_].append(event)
    self._sequential_events.append(event)
    return event.id_

```
 |  
| --- | --- |  
###  on_event_end [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/llama_debug/#llama_index.core.callbacks.llama_debug.LlamaDebugHandler.on_event_end "Permanent link")

```
on_event_end(
    event_type: ,
    payload: Optional[[, ]] = None,
    event_id:  = "",
    **kwargs: 
) -> None

```

Store event end data by event type.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `event_type`  |   |  event type to store.  |  _required_  |  
|  `payload`  |  `Optional[Dict[str, Any]]`  |  payload to store.  |  `None`  |  
|  `event_id`  |  event id to store.  |  
Source code in `llama-index-core/llama_index/core/callbacks/llama_debug.py`  
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
```
 | 
```
defon_event_end(
    self,
    event_type: CBEventType,
    payload: Optional[Dict[str, Any]] = None,
    event_id: str = "",
    **kwargs: Any,
) -> None:
"""
    Store event end data by event type.

    Args:
        event_type (CBEventType): event type to store.
        payload (Optional[Dict[str, Any]]): payload to store.
        event_id (str): event id to store.

    """
    event = CBEvent(event_type, payload=payload, id_=event_id)
    self._event_pairs_by_type[event.event_type].append(event)
    self._event_pairs_by_id[event.id_].append(event)
    self._sequential_events.append(event)
    self._trace_map = defaultdict(list)

```
 |  
| --- | --- |  
###  get_events [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/llama_debug/#llama_index.core.callbacks.llama_debug.LlamaDebugHandler.get_events "Permanent link")

```
get_events(
    event_type: Optional[] = None,
) -> []

```

Get all events for a specific event type.
Source code in `llama-index-core/llama_index/core/callbacks/llama_debug.py`  
| 
```
105
106
107
108
109
110
```
 | 
```
defget_events(self, event_type: Optional[CBEventType] = None) -> List[CBEvent]:
"""Get all events for a specific event type."""
    if event_type is not None:
        return self._event_pairs_by_type[event_type]

    return self._sequential_events

```
 |  
| --- | --- |  
###  get_event_pairs [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/llama_debug/#llama_index.core.callbacks.llama_debug.LlamaDebugHandler.get_event_pairs "Permanent link")

```
get_event_pairs(
    event_type: Optional[] = None,
) -> [[]]

```

Pair events by ID, either all events or a specific type.
Source code in `llama-index-core/llama_index/core/callbacks/llama_debug.py`  
| 
```
142
143
144
145
146
147
148
149
```
 | 
```
defget_event_pairs(
    self, event_type: Optional[CBEventType] = None
) -> List[List[CBEvent]]:
"""Pair events by ID, either all events or a specific type."""
    if event_type is not None:
        return self._get_event_pairs(self._event_pairs_by_type[event_type])

    return self._get_event_pairs(self._sequential_events)

```
 |  
| --- | --- |  
###  get_llm_inputs_outputs [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/llama_debug/#llama_index.core.callbacks.llama_debug.LlamaDebugHandler.get_llm_inputs_outputs "Permanent link")

```
get_llm_inputs_outputs() -> [[]]

```

Get the exact LLM inputs and outputs.
Source code in `llama-index-core/llama_index/core/callbacks/llama_debug.py`  
| 
```
151
152
153
```
 | 
```
defget_llm_inputs_outputs(self) -> List[List[CBEvent]]:
"""Get the exact LLM inputs and outputs."""
    return self._get_event_pairs(self._event_pairs_by_type[CBEventType.LLM])

```
 |  
| --- | --- |  
###  flush_event_logs [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/llama_debug/#llama_index.core.callbacks.llama_debug.LlamaDebugHandler.flush_event_logs "Permanent link")

```
flush_event_logs() -> None

```

Clear all events from memory.
Source code in `llama-index-core/llama_index/core/callbacks/llama_debug.py`  
| 
```
161
162
163
164
165
```
 | 
```
defflush_event_logs(self) -> None:
"""Clear all events from memory."""
    self._event_pairs_by_type = defaultdict(list)
    self._event_pairs_by_id = defaultdict(list)
    self._sequential_events = []

```
 |  
| --- | --- |  
###  start_trace [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/llama_debug/#llama_index.core.callbacks.llama_debug.LlamaDebugHandler.start_trace "Permanent link")

```
start_trace(trace_id: Optional[] = None) -> None

```

Launch a trace.
Source code in `llama-index-core/llama_index/core/callbacks/llama_debug.py`  
| 
```
167
168
169
170
```
 | 
```
defstart_trace(self, trace_id: Optional[str] = None) -> None:
"""Launch a trace."""
    self._trace_map = defaultdict(list)
    self._cur_trace_id = trace_id

```
 |  
| --- | --- |  
###  end_trace [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/llama_debug/#llama_index.core.callbacks.llama_debug.LlamaDebugHandler.end_trace "Permanent link")

```
end_trace(
    trace_id: Optional[] = None,
    trace_map: Optional[[, []]] = None,
) -> None

```

Shutdown the current trace.
Source code in `llama-index-core/llama_index/core/callbacks/llama_debug.py`  
| 
```
172
173
174
175
176
177
178
179
180
```
 | 
```
defend_trace(
    self,
    trace_id: Optional[str] = None,
    trace_map: Optional[Dict[str, List[str]]] = None,
) -> None:
"""Shutdown the current trace."""
    self._trace_map = trace_map or defaultdict(list)
    if self.print_trace_on_end:
        self.print_trace_map()

```
 |  
| --- | --- |  
###  print_trace_map [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/llama_debug/#llama_index.core.callbacks.llama_debug.LlamaDebugHandler.print_trace_map "Permanent link")

```
print_trace_map() -> None

```

Print simple trace map to terminal for debugging of the most recent trace.
Source code in `llama-index-core/llama_index/core/callbacks/llama_debug.py`  
| 
```
196
197
198
199
200
201
```
 | 
```
defprint_trace_map(self) -> None:
"""Print simple trace map to terminal for debugging of the most recent trace."""
    self._print("*" * 10)
    self._print(f"Trace: {self._cur_trace_id}")
    self._print_trace_map(BASE_TRACE_EVENT, level=1)
    self._print("*" * 10)

```
 |  
| --- | --- |  
options: members: - LlamaDebugHandler
