# Models
##  EventEnvelopeWithMetadata [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/models/#llama_agents.client.EventEnvelopeWithMetadata "Permanent link")
Bases: `BaseModel`
Client readable representation of an Event. Includes class metadata in order to support matching event types semantically in an extendable manner (e.g. "StartEvent", "StopEvent", etc.).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `value`  |  `dict[str, Any]`  |  _required_  |  
|  `qualified_name`  |  `str | None`  |  _required_  |  
|  `type`  |  _required_  |  
|  `types`  |  `list[str] | None`  |  _required_  |  
Source code in `llama_agents/client/protocol/serializable_events.py`  
| 
```
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
```
 | 
```
classEventEnvelopeWithMetadata(BaseModel):
"""
    Client readable representation of an Event. Includes class metadata in order to support
    matching event types semantically in an extendable manner (e.g. "StartEvent", "StopEvent", etc.).
    """

    value: dict[str, Any]

    # deprecated, use type instead
    qualified_name: str | None

    # New metadata
    type: str
    types: list[str] | None

    defload_event(self, registry: list[type[Event]] = []) -> Event:
"""
        Attempts to load the event data as a python class based on the envelope metadata.
        Looks up the event from the registry, if provided. Falls back to the qualified_name, attempting to load from the module path.
        """
        registry_lookup = {e.__name__: e for e in registry}
        as_event_envelope = EventEnvelope(
            value=self.value, type=self.type, qualified_name=self.qualified_name
        ).model_dump()
        return EventEnvelope.parse(
            client_data=as_event_envelope, registry=registry_lookup
        )

    @classmethod
    deffrom_event(
        cls, event: Event, include_qualified_name: bool = True
    ) -> EventEnvelopeWithMetadata:
"""
        Build a backward-compatible envelope for an Event, preserving existing
        fields (e.g., qualified_name, value) while adding metadata useful for
        type-safe clients.

        """
        # Start with the existing JSON-serializable structure
        value = event.model_dump(mode="json")

        envelope = EventEnvelopeWithMetadata(
            value=value,
            qualified_name=_get_qualified_name(type(event))
            if include_qualified_name
            else None,
            types=_get_event_subtypes(type(event)),
            type=type(event).__name__,
        )
        return envelope

```
 |  
| --- | --- |  
###  load_event [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/models/#llama_agents.client.EventEnvelopeWithMetadata.load_event "Permanent link")

```
load_event(registry: [[]] = []) -> 

```

Attempts to load the event data as a python class based on the envelope metadata. Looks up the event from the registry, if provided. Falls back to the qualified_name, attempting to load from the module path.
Source code in `llama_agents/client/protocol/serializable_events.py`  
| 
```
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
```
 | 
```
defload_event(self, registry: list[type[Event]] = []) -> Event:
"""
    Attempts to load the event data as a python class based on the envelope metadata.
    Looks up the event from the registry, if provided. Falls back to the qualified_name, attempting to load from the module path.
    """
    registry_lookup = {e.__name__: e for e in registry}
    as_event_envelope = EventEnvelope(
        value=self.value, type=self.type, qualified_name=self.qualified_name
    ).model_dump()
    return EventEnvelope.parse(
        client_data=as_event_envelope, registry=registry_lookup
    )

```
 |  
| --- | --- |  
###  from_event `classmethod` [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/models/#llama_agents.client.EventEnvelopeWithMetadata.from_event "Permanent link")

```
from_event(event: , include_qualified_name:  = True) -> 

```

Build a backward-compatible envelope for an Event, preserving existing fields (e.g., qualified_name, value) while adding metadata useful for type-safe clients.
Source code in `llama_agents/client/protocol/serializable_events.py`  
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
```
 | 
```
@classmethod
deffrom_event(
    cls, event: Event, include_qualified_name: bool = True
) -> EventEnvelopeWithMetadata:
"""
    Build a backward-compatible envelope for an Event, preserving existing
    fields (e.g., qualified_name, value) while adding metadata useful for
    type-safe clients.

    """
    # Start with the existing JSON-serializable structure
    value = event.model_dump(mode="json")

    envelope = EventEnvelopeWithMetadata(
        value=value,
        qualified_name=_get_qualified_name(type(event))
        if include_qualified_name
        else None,
        types=_get_event_subtypes(type(event)),
        type=type(event).__name__,
    )
    return envelope

```
 |  
| --- | --- |  
##  HandlerData [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/models/#llama_agents.client.HandlerData "Permanent link")
Bases: `BaseModel`
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `handler_id`  |  _required_  |  
|  `workflow_name`  |  _required_  |  
|  `run_id`  |  `str | None`  |  _required_  |  
|  `error`  |  `str | None`  |  _required_  |  
|  `result`  |  `EventEnvelopeWithMetadata[](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/models/#llama_agents.client.EventEnvelopeWithMetadata "            EventEnvelopeWithMetadata \(llama_agents.client.protocol.serializable_events.EventEnvelopeWithMetadata\)") | None`  |  _required_  |  
|  `status`  |  `Literal['running', 'completed', 'failed', 'cancelled']`  |  _required_  |  
|  `started_at`  |  _required_  |  
|  `updated_at`  |  `str | None`  |  _required_  |  
|  `completed_at`  |  `str | None`  |  _required_  |  
Source code in `llama_agents/client/protocol/__init__.py`  
| 
```
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
```
 | 
```
classHandlerData(BaseModel):
    handler_id: str
    workflow_name: str
    run_id: str | None
    error: str | None
    result: EventEnvelopeWithMetadata | None
    status: Status
    started_at: str
    updated_at: str | None
    completed_at: str | None

```
 |  
| --- | --- |  
##  HandlersListResponse [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/models/#llama_agents.client.HandlersListResponse "Permanent link")
Bases: `BaseModel`
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `handlers`  |  `list[HandlerData[](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/models/#llama_agents.client.HandlerData "            HandlerData \(llama_agents.client.protocol.HandlerData\)")]`  |  _required_  |  
Source code in `llama_agents/client/protocol/__init__.py`  
| 
```
classHandlersListResponse(BaseModel):
    handlers: list[HandlerData]

```
 |  
| --- |  
##  SendEventResponse [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/models/#llama_agents.client.SendEventResponse "Permanent link")
Bases: `BaseModel`
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `status`  |  `Literal['sent']`  |  _required_  |  
Source code in `llama_agents/client/protocol/__init__.py`  
| 
```
classSendEventResponse(BaseModel):
    status: Literal["sent"]

```
 |  
| --- |  
##  CancelHandlerResponse [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/models/#llama_agents.client.CancelHandlerResponse "Permanent link")
Bases: `BaseModel`
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `status`  |  `Literal['deleted', 'cancelled']`  |  _required_  |  
Source code in `llama_agents/client/protocol/__init__.py`  
| 
```
classCancelHandlerResponse(BaseModel):
    status: Literal["deleted", "cancelled"]

```
 |  
| --- |
