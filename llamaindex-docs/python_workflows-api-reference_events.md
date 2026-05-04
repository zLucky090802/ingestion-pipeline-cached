# Events
##  Event [#](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.Event "Permanent link")
Bases: `DictLikeModel`
Base class for all workflow events.
Events are light-weight, serializable payloads passed between steps. They support both attribute and mapping access to dynamic fields.
Examples:
Subclassing with typed fields:

```
frompydanticimport Field

classCustomEv(Event):
    score: int = Field(ge=0)

e = CustomEv(score=10)
print(e.score)

```

See Also

Source code in `workflows/events.py`  
| 
```
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
```
 | 
```
classEvent(DictLikeModel):
"""
    Base class for all workflow events.

    Events are light-weight, serializable payloads passed between steps.
    They support both attribute and mapping access to dynamic fields.

    Examples:
        Subclassing with typed fields:

        ```python
        from pydantic import Field

        class CustomEv(Event):
            score: int = Field(ge=0)

        e = CustomEv(score=10)
        print(e.score)
        ```

    See Also:
        - [StartEvent][workflows.events.StartEvent]
        - [StopEvent][workflows.events.StopEvent]
        - [InputRequiredEvent][workflows.events.InputRequiredEvent]
        - [HumanResponseEvent][workflows.events.HumanResponseEvent]
    """

    def__init__(self, **params: Any):
        super().__init__(**params)

```
 |  
| --- | --- |  
##  InputRequiredEvent [#](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.InputRequiredEvent "Permanent link")
Bases: 
Emitted when human input is required to proceed.
Automatically written to the event stream if returned from a step.
If returned from a step, it does not need to be consumed by other steps and will pass validation. It's expected that the caller will respond to this event and send back a [HumanResponseEvent](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.HumanResponseEvent "            HumanResponseEvent").
Use this directly or subclass it.
Typical flow: a step returns `InputRequiredEvent`, callers consume it from the stream and send back a [HumanResponseEvent](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.HumanResponseEvent "            HumanResponseEvent").
Examples:

```
fromworkflows.eventsimport InputRequiredEvent, HumanResponseEvent

classHITLWorkflow(Workflow):
    @step
    async defmy_step(self, ev: StartEvent) -> InputRequiredEvent:
        return InputRequiredEvent(prefix="What's your name? ")

    @step
    async defmy_step(self, ev: HumanResponseEvent) -> StopEvent:
        return StopEvent(result=ev.response)

```

Source code in `workflows/events.py`  
| 
```
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
```
 | 
```
classInputRequiredEvent(Event):
"""Emitted when human input is required to proceed.

    Automatically written to the event stream if returned from a step.

    If returned from a step, it does not need to be consumed by other steps and will pass validation.
    It's expected that the caller will respond to this event and send back a [HumanResponseEvent][workflows.events.HumanResponseEvent].

    Use this directly or subclass it.

    Typical flow: a step returns `InputRequiredEvent`, callers consume it from
    the stream and send back a [HumanResponseEvent][workflows.events.HumanResponseEvent].

    Examples:
        ```python
        from workflows.events import InputRequiredEvent, HumanResponseEvent

        class HITLWorkflow(Workflow):
            @step
            async def my_step(self, ev: StartEvent) -> InputRequiredEvent:
                return InputRequiredEvent(prefix="What's your name? ")

            @step
            async def my_step(self, ev: HumanResponseEvent) -> StopEvent:
                return StopEvent(result=ev.response)
        ```
    """

```
 |  
| --- | --- |  
##  HumanResponseEvent [#](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.HumanResponseEvent "Permanent link")
Bases: 
Carries a human's response for a prior input request.
If consumed by a step and not returned by another, it will still pass validation.
Examples:

```
fromworkflows.eventsimport InputRequiredEvent, HumanResponseEvent

classHITLWorkflow(Workflow):
    @step
    async defmy_step(self, ev: StartEvent) -> InputRequiredEvent:
        return InputRequiredEvent(prefix="What's your name? ")

    @step
    async defmy_step(self, ev: HumanResponseEvent) -> StopEvent:
        return StopEvent(result=ev.response)

```

Source code in `workflows/events.py`  
| 
```
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
```
 | 
```
classHumanResponseEvent(Event):
"""Carries a human's response for a prior input request.

    If consumed by a step and not returned by another, it will still pass validation.

    Examples:
        ```python
        from workflows.events import InputRequiredEvent, HumanResponseEvent

        class HITLWorkflow(Workflow):
            @step
            async def my_step(self, ev: StartEvent) -> InputRequiredEvent:
                return InputRequiredEvent(prefix="What's your name? ")

            @step
            async def my_step(self, ev: HumanResponseEvent) -> StopEvent:
                return StopEvent(result=ev.response)
        ```
    """

```
 |  
| --- | --- |  
##  StartEvent [#](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.StartEvent "Permanent link")
Bases: 
Implicit entry event sent to kick off a `Workflow.run()`.
Source code in `workflows/events.py`  
| 
```
151
152
```
 | 
```
classStartEvent(Event):
"""Implicit entry event sent to kick off a `Workflow.run()`."""

```
 |  
| --- | --- |  
##  StopEvent [#](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.StopEvent "Permanent link")
Bases: 
Terminal event that signals the workflow has completed.
The `result` property contains the return value of the workflow run. When a custom stop event subclass is used, the workflow result is that event instance itself.
Examples:

```
# default stop event: result holds the value
return StopEvent(result={"answer": 42})

```

Subclassing to provide a custom result:
```python class MyStopEv(StopEvent): pass
@step async def my_step(self, ctx: Context, ev: StartEvent) -> MyStopEv: return MyStopEv(result={"answer": 42})
Source code in `workflows/events.py`  
| 
```
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
```
 | 
```
classStopEvent(Event):
"""Terminal event that signals the workflow has completed.

    The `result` property contains the return value of the workflow run. When a
    custom stop event subclass is used, the workflow result is that event
    instance itself.

    Examples:
        ```python
        # default stop event: result holds the value
        return StopEvent(result={"answer": 42})
        ```

        Subclassing to provide a custom result:

        ```python
        class MyStopEv(StopEvent):
            pass

        @step
        async def my_step(self, ctx: Context, ev: StartEvent) -> MyStopEv:
            return MyStopEv(result={"answer": 42})
    """

    _result: Any = PrivateAttr(default=None)

    def__init__(self, result: Any = None, **kwargs: Any) -> None:
        # forces the user to provide a result
        super().__init__(_result=result, **kwargs)

    def_get_result(self) -> Any:
"""This can be overridden by subclasses to return the desired result."""
        return self._result

    @property
    defresult(self) -> Any:
        return self._get_result()

    @model_serializer(mode="wrap")
    defcustom_model_dump(self, handler: Any) -> dict[str, Any]:
        data = handler(self)
        # include _result in serialization for base StopEvent
        if self._result is not None:
            data["result"] = self._result
        return data

    def__repr__(self) -> str:
        dict_items = {**self._data, **self.model_dump()}
        # Format as key=value pairs
        parts = [f"{k}={v!r}" for k, v in dict_items.items()]
        dict_str = ", ".join(parts)
        return f"{self.__class__.__name__}({dict_str})"

    def__str__(self) -> str:
        return str(self._result)

```
 |  
| --- | --- |  
##  WorkflowTimedOutEvent [#](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.WorkflowTimedOutEvent "Permanent link")
Bases: 
Published when a workflow exceeds its configured timeout.
This event is published to the event stream when a workflow times out, allowing consumers to understand why the workflow ended before the WorkflowTimeoutError exception is raised.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
Examples:

```
async for event in handler.stream_events():
    if isinstance(event, WorkflowTimedOutEvent):
        print(f"Workflow timed out after {event.timeout}s")
        print(f"Active steps: {event.active_steps}")

```

Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `timeout`  |  `float`  |  _required_  |  
|  `active_steps`  |  `list[str]`  |  _required_  |  
Source code in `workflows/events.py`  
| 
```
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
```
 | 
```
classWorkflowTimedOutEvent(StopEvent):
"""Published when a workflow exceeds its configured timeout.

    This event is published to the event stream when a workflow times out,
    allowing consumers to understand why the workflow ended before the
    WorkflowTimeoutError exception is raised.

    Attributes:
        timeout: The timeout duration in seconds that was exceeded.
        active_steps: List of step names that were still active when the timeout occurred.

    Examples:
        ```python
        async for event in handler.stream_events():
            if isinstance(event, WorkflowTimedOutEvent):
                print(f"Workflow timed out after {event.timeout}s")
                print(f"Active steps: {event.active_steps}")
        ```
    """

    timeout: float
    active_steps: list[str]

```
 |  
| --- | --- |  
##  WorkflowCancelledEvent [#](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.WorkflowCancelledEvent "Permanent link")
Bases: 
Published when a workflow is cancelled by the user.
This event is published to the event stream when a workflow is cancelled via the handler or programmatically, allowing consumers to understand why the workflow ended before the WorkflowCancelledByUser exception is raised.
Examples:

```
async for event in handler.stream_events():
    if isinstance(event, WorkflowCancelledEvent):
        print("Workflow was cancelled by user")

```

Source code in `workflows/events.py`  
| 
```
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
```
 | 
```
classWorkflowCancelledEvent(StopEvent):
"""Published when a workflow is cancelled by the user.

    This event is published to the event stream when a workflow is cancelled
    via the handler or programmatically, allowing consumers to understand why
    the workflow ended before the WorkflowCancelledByUser exception is raised.

    Examples:
        ```python
        async for event in handler.stream_events():
            if isinstance(event, WorkflowCancelledEvent):
                print("Workflow was cancelled by user")
        ```
    """

```
 |  
| --- | --- |  
##  WorkflowFailedEvent [#](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.WorkflowFailedEvent "Permanent link")
Bases: 
Published when a workflow step fails permanently.
This event is published to the event stream when a step fails and all retries are exhausted, allowing consumers to understand why the workflow ended before the exception is raised.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
Examples:

```
async for event in handler.stream_events():
    if isinstance(event, WorkflowFailedEvent):
        print(f"Step '{event.step_name}' failed after {event.attempts} attempts")
        print(f"Total time: {event.elapsed_seconds:.2f}s")
        print(event.traceback)

```

Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `step_name`  |  _required_  |  
|  `exception_type`  |  _required_  |  
|  `exception_message`  |  _required_  |  
|  `traceback`  |  _required_  |  
|  `attempts`  |  _required_  |  
|  `elapsed_seconds`  |  `float`  |  _required_  |  
Source code in `workflows/events.py`  
| 
```
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
```
 | 
```
classWorkflowFailedEvent(StopEvent):
"""Published when a workflow step fails permanently.

    This event is published to the event stream when a step fails and all
    retries are exhausted, allowing consumers to understand why the workflow
    ended before the exception is raised.

    Attributes:
        step_name: The name of the step that failed.
        exception_type: The fully qualified type name of the exception that caused the failure.
        exception_message: The string representation of the exception message.
        traceback: The formatted stack trace of the exception.
        attempts: The total number of attempts made before giving up.
        elapsed_seconds: Time in seconds from first attempt to final failure.

    Examples:
        ```python
        async for event in handler.stream_events():
            if isinstance(event, WorkflowFailedEvent):
                print(f"Step '{event.step_name}' failed after {event.attempts} attempts")
                print(f"Total time: {event.elapsed_seconds:.2f}s")
                print(event.traceback)
        ```
    """

    step_name: str
    exception_type: str
    exception_message: str
    traceback: str
    attempts: int
    elapsed_seconds: float

```
 |  
| --- | --- |
