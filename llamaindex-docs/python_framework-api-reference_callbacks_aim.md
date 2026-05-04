# Aim
##  AimCallback [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/aim/#llama_index.callbacks.aim.AimCallback "Permanent link")
Bases: 
AimCallback callback class.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `repo (`  |  obj:`str`, optional): Aim repository path or Repo object to which Run object is bound. If skipped, default Repo is used.  |  _required_  |  
|  `experiment_name (`  |  obj:`str`, optional): Sets Run's `experiment` property. 'default' if not specified. Can be used later to query runs/sequences.  |  _required_  |  
|  `system_tracking_interval (`  |  obj:`int`, optional): Sets the tracking interval in seconds for system usage metrics (CPU, Memory, etc.). Set to `None` to disable system metrics tracking.  |  _required_  |  
|  `log_system_params (`  |  obj:`bool`, optional): Enable/Disable logging of system params such as installed packages, git info, environment variables, etc.  |  _required_  |  
|  `capture_terminal_logs (`  |  obj:`bool`, optional): Enable/Disable terminal stdout logging.  |  _required_  |  
|  `event_starts_to_ignore`  |  `Optional[List[CBEventType[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.schema.CBEventType "CBEventType \(llama_index.core.callbacks.schema.CBEventType\)")]]`  |  list of event types to ignore when tracking event starts.  |  `None`  |  
|  `event_ends_to_ignore`  |  `Optional[List[CBEventType[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.schema.CBEventType "CBEventType \(llama_index.core.callbacks.schema.CBEventType\)")]]`  |  list of event types to ignore when tracking event ends.  |  `None`  |  
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-aim/llama_index/callbacks/aim/base.py`  
| 
```
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
```
 | 
```
classAimCallback(BaseCallbackHandler):
"""
    AimCallback callback class.

    Args:
        repo (:obj:`str`, optional):
            Aim repository path or Repo object to which Run object is bound.
            If skipped, default Repo is used.
        experiment_name (:obj:`str`, optional):
            Sets Run's `experiment` property. 'default' if not specified.
            Can be used later to query runs/sequences.
        system_tracking_interval (:obj:`int`, optional):
            Sets the tracking interval in seconds for system usage
            metrics (CPU, Memory, etc.). Set to `None` to disable
            system metrics tracking.
        log_system_params (:obj:`bool`, optional):
            Enable/Disable logging of system params such as installed packages,
            git info, environment variables, etc.
        capture_terminal_logs (:obj:`bool`, optional):
            Enable/Disable terminal stdout logging.
        event_starts_to_ignore (Optional[List[CBEventType]]):
            list of event types to ignore when tracking event starts.
        event_ends_to_ignore (Optional[List[CBEventType]]):
            list of event types to ignore when tracking event ends.

    """

    def__init__(
        self,
        repo: Optional[str] = None,
        experiment_name: Optional[str] = None,
        system_tracking_interval: Optional[int] = 1,
        log_system_params: Optional[bool] = True,
        capture_terminal_logs: Optional[bool] = True,
        event_starts_to_ignore: Optional[List[CBEventType]] = None,
        event_ends_to_ignore: Optional[List[CBEventType]] = None,
        run_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        if Run is None:
            raise ModuleNotFoundError(
                "Please install aim to use the AimCallback: 'pip install aim'"
            )

        event_starts_to_ignore = (
            event_starts_to_ignore if event_starts_to_ignore else []
        )
        event_ends_to_ignore = event_ends_to_ignore if event_ends_to_ignore else []
        super().__init__(
            event_starts_to_ignore=event_starts_to_ignore,
            event_ends_to_ignore=event_ends_to_ignore,
        )

        self.repo = repo
        self.experiment_name = experiment_name
        self.system_tracking_interval = system_tracking_interval
        self.log_system_params = log_system_params
        self.capture_terminal_logs = capture_terminal_logs
        self._run: Optional[Any] = None
        self._run_hash = None

        self._llm_response_step = 0

        self.setup(run_params)

    defon_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
"""
        Args:
            event_type (CBEventType): event type to store.
            payload (Optional[Dict[str, Any]]): payload to store.
            event_id (str): event id to store.
            parent_id (str): parent event id.

        """
        return ""

    defon_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
"""
        Args:
            event_type (CBEventType): event type to store.
            payload (Optional[Dict[str, Any]]): payload to store.
            event_id (str): event id to store.

        """
        if not self._run:
            raise ValueError("AimCallback failed to init properly.")

        if event_type is CBEventType.LLM and payload:
            if EventPayload.PROMPT in payload:
                llm_input = str(payload[EventPayload.PROMPT])
                llm_output = str(payload[EventPayload.COMPLETION])
            else:
                message = payload.get(EventPayload.MESSAGES, [])
                llm_input = "\n".join([str(x) for x in message])
                llm_output = str(payload[EventPayload.RESPONSE])

            self._run.track(
                Text(llm_input),
                name="prompt",
                step=self._llm_response_step,
                context={"event_id": event_id},
            )

            self._run.track(
                Text(llm_output),
                name="response",
                step=self._llm_response_step,
                context={"event_id": event_id},
            )

            self._llm_response_step += 1
        elif event_type is CBEventType.CHUNKING and payload:
            for chunk_id, chunk in enumerate(payload[EventPayload.CHUNKS]):
                self._run.track(
                    Text(chunk),
                    name="chunk",
                    step=self._llm_response_step,
                    context={"chunk_id": chunk_id, "event_id": event_id},
                )

    @property
    defexperiment(self) -> Run:
        if not self._run:
            self.setup()
        return self._run

    defsetup(self, args: Optional[Dict[str, Any]] = None) -> None:
        if not self._run:
            if self._run_hash:
                self._run = Run(
                    self._run_hash,
                    repo=self.repo,
                    system_tracking_interval=self.system_tracking_interval,
                    log_system_params=self.log_system_params,
                    capture_terminal_logs=self.capture_terminal_logs,
                )
            else:
                self._run = Run(
                    repo=self.repo,
                    experiment=self.experiment_name,
                    system_tracking_interval=self.system_tracking_interval,
                    log_system_params=self.log_system_params,
                    capture_terminal_logs=self.capture_terminal_logs,
                )
                self._run_hash = self._run.hash

        # Log config parameters
        if args:
            try:
                for key in args:
                    self._run.set(key, args[key], strict=False)
            except Exception as e:
                logger.warning(f"Aim could not log config parameters -> {e}")

    def__del__(self) -> None:
        if self._run and self._run.active:
            self._run.close()

    defstart_trace(self, trace_id: Optional[str] = None) -> None:
        pass

    defend_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        pass

```
 |  
| --- | --- |  
###  on_event_start [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/aim/#llama_index.callbacks.aim.AimCallback.on_event_start "Permanent link")

```
on_event_start(
    event_type: ,
    payload: Optional[[, ]] = None,
    event_id:  = "",
    parent_id:  = "",
    **kwargs: 
) -> 

```

Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `event_type`  |   |  event type to store.  |  _required_  |  
|  `payload`  |  `Optional[Dict[str, Any]]`  |  payload to store.  |  `None`  |  
|  `event_id`  |  event id to store.  |  
|  `parent_id`  |  parent event id.  |  
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-aim/llama_index/callbacks/aim/base.py`  
| 
```
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
    Args:
        event_type (CBEventType): event type to store.
        payload (Optional[Dict[str, Any]]): payload to store.
        event_id (str): event id to store.
        parent_id (str): parent event id.

    """
    return ""

```
 |  
| --- | --- |  
###  on_event_end [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/aim/#llama_index.callbacks.aim.AimCallback.on_event_end "Permanent link")

```
on_event_end(
    event_type: ,
    payload: Optional[[, ]] = None,
    event_id:  = "",
    **kwargs: 
) -> None

```

Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `event_type`  |   |  event type to store.  |  _required_  |  
|  `payload`  |  `Optional[Dict[str, Any]]`  |  payload to store.  |  `None`  |  
|  `event_id`  |  event id to store.  |  
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-aim/llama_index/callbacks/aim/base.py`  
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
139
140
141
142
143
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
    Args:
        event_type (CBEventType): event type to store.
        payload (Optional[Dict[str, Any]]): payload to store.
        event_id (str): event id to store.

    """
    if not self._run:
        raise ValueError("AimCallback failed to init properly.")

    if event_type is CBEventType.LLM and payload:
        if EventPayload.PROMPT in payload:
            llm_input = str(payload[EventPayload.PROMPT])
            llm_output = str(payload[EventPayload.COMPLETION])
        else:
            message = payload.get(EventPayload.MESSAGES, [])
            llm_input = "\n".join([str(x) for x in message])
            llm_output = str(payload[EventPayload.RESPONSE])

        self._run.track(
            Text(llm_input),
            name="prompt",
            step=self._llm_response_step,
            context={"event_id": event_id},
        )

        self._run.track(
            Text(llm_output),
            name="response",
            step=self._llm_response_step,
            context={"event_id": event_id},
        )

        self._llm_response_step += 1
    elif event_type is CBEventType.CHUNKING and payload:
        for chunk_id, chunk in enumerate(payload[EventPayload.CHUNKS]):
            self._run.track(
                Text(chunk),
                name="chunk",
                step=self._llm_response_step,
                context={"chunk_id": chunk_id, "event_id": event_id},
            )

```
 |  
| --- | --- |  
options: members: - AimCallback
