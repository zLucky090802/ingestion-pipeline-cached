# Promptlayer
##  PromptLayerHandler [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/promptlayer/#llama_index.callbacks.promptlayer.PromptLayerHandler "Permanent link")
Bases: 
Callback handler for sending to promptlayer.com.
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-promptlayer/llama_index/callbacks/promptlayer/base.py`  
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
```
 | 
```
classPromptLayerHandler(BaseCallbackHandler):
"""Callback handler for sending to promptlayer.com."""

    pl_tags: Optional[List[str]]
    return_pl_id: bool = False

    def__init__(self, pl_tags: List[str] = [], return_pl_id: bool = False) -> None:
        try:
            frompromptlayer.utilsimport get_api_key, promptlayer_api_request

            self._promptlayer_api_request = promptlayer_api_request
            self._promptlayer_api_key = get_api_key()
        except ImportError:
            raise ImportError(
                "Please install PromptLAyer with `pip install promptlayer`"
            )
        self.pl_tags = pl_tags
        self.return_pl_id = return_pl_id
        super().__init__(event_starts_to_ignore=[], event_ends_to_ignore=[])

    defstart_trace(self, trace_id: Optional[str] = None) -> None:
        return

    defend_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        return

    event_map: Dict[str, Dict[str, Any]] = {}

    defadd_event(self, event_id: str, **kwargs: Any) -> None:
        self.event_map[event_id] = {
            "kwargs": kwargs,
            "request_start_time": datetime.datetime.now().timestamp(),
        }

    defget_event(
        self,
        event_id: str,
    ) -> Dict[str, Any]:
        return self.event_map[event_id] or {}

    defon_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
        if event_type == CBEventType.LLM and payload is not None:
            self.add_event(
                event_id=event_id, **payload.get(EventPayload.SERIALIZED, {})
            )
        return event_id

    defon_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
        if event_type != CBEventType.LLM or payload is None:
            return
        request_end_time = datetime.datetime.now().timestamp()
        prompt = str(payload.get(EventPayload.PROMPT))
        completion = payload.get(EventPayload.COMPLETION)
        response = payload.get(EventPayload.RESPONSE)
        function_name = PROMPT_LAYER_CHAT_FUNCTION_NAME
        event_data = self.get_event(event_id=event_id)
        resp: Union[str, Dict]
        extra_args = {}
        resp = None
        if response:
            messages = cast(List[ChatMessage], payload.get(EventPayload.MESSAGES, []))
            resp = response.message.dict()
            assert isinstance(resp, dict)

            usage_dict: Dict[str, int] = {}
            try:
                usage = response.raw.get("usage", None)  # type: ignore

                if isinstance(usage, dict):
                    usage_dict = {
                        "prompt_tokens": usage.get("prompt_tokens", 0),
                        "completion_tokens": usage.get("completion_tokens", 0),
                        "total_tokens": usage.get("total_tokens", 0),
                    }
                elif isinstance(usage, BaseModel):
                    usage_dict = usage.dict()
            except Exception:
                pass

            extra_args = {
                "messages": [message.dict() for message in messages],
                "usage": usage_dict,
            }
            ## promptlayer needs tool_calls toplevel.
            if "tool_calls" in response.message.additional_kwargs:
                resp["tool_calls"] = [
                    tool_call.dict()
                    for tool_call in resp["additional_kwargs"]["tool_calls"]
                ]
                del resp["additional_kwargs"]["tool_calls"]
        if completion:
            function_name = PROMPT_LAYER_COMPLETION_FUNCTION_NAME
            resp = str(completion)
        if resp:
            _pl_request_id = self._promptlayer_api_request(
                function_name,
                "openai",
                [prompt],
                {
                    **extra_args,
                    **event_data["kwargs"],
                },
                self.pl_tags,
                [resp],
                event_data["request_start_time"],
                request_end_time,
                self._promptlayer_api_key,
                return_pl_id=self.return_pl_id,
            )

```
 |  
| --- | --- |  
options: members: - PromptLayerHandler
