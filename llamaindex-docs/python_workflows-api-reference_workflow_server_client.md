# Client
##  WorkflowClient [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/client/#llama_agents.client.WorkflowClient "Permanent link")
Python client for interacting with a `WorkflowServer`.
Provides methods for listing workflows, running them synchronously or asynchronously, streaming events, and sending events for human-in-the-loop workflows.
Example:

```
from llama_agents.client import WorkflowClient
from workflows.events import StartEvent

client = WorkflowClient(base_url="http://localhost:8080")

# Run synchronously
result = await client.run_workflow("greet", start_event=StartEvent(name="Ada"))
print(result.result)

# Run async and stream events
handler = await client.run_workflow_nowait("greet")
stream = client.get_workflow_events(handler.handler_id)
async for event in stream:
    print(event.type, event.value)

```

Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `base_url`  |  `str | None`  |  Base URL of the workflow server (e.g. `"http://localhost:8080"`).  |  `None`  |  
|  `httpx_client`  |  `AsyncClient | None`  |  Pre-configured `httpx.AsyncClient`. Use this for custom auth headers, timeouts, or transport configuration.  |  `None`  |  
Provide exactly one of `base_url` or `httpx_client`.
Source code in `llama_agents/client/client.py`  
| 
```
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
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
```
 | 
```
classWorkflowClient:
"""Python client for interacting with a ``WorkflowServer``.

    Provides methods for listing workflows, running them synchronously or
    asynchronously, streaming events, and sending events for
    human-in-the-loop workflows.

    Example:

        from llama_agents.client import WorkflowClient
        from workflows.events import StartEvent

        client = WorkflowClient(base_url="http://localhost:8080")

        # Run synchronously
        result = await client.run_workflow("greet", start_event=StartEvent(name="Ada"))
        print(result.result)

        # Run async and stream events
        handler = await client.run_workflow_nowait("greet")
        stream = client.get_workflow_events(handler.handler_id)
        async for event in stream:
            print(event.type, event.value)

    Args:
        base_url: Base URL of the workflow server (e.g. ``"http://localhost:8080"``).
        httpx_client: Pre-configured ``httpx.AsyncClient``. Use this for
            custom auth headers, timeouts, or transport configuration.

    Provide exactly one of ``base_url`` or ``httpx_client``.
    """

    @overload
    def__init__(self, *, httpx_client: httpx.AsyncClient): ...
    @overload
    def__init__(
        self,
        *,
        base_url: str,
    ): ...

    def__init__(
        self,
        *,
        httpx_client: httpx.AsyncClient | None = None,
        base_url: str | None = None,
    ):
        if httpx_client is None and base_url is None:
            raise ValueError("Either httpx_client or base_url must be provided")
        if httpx_client is not None and base_url is not None:
            raise ValueError("Only one of httpx_client or base_url must be provided")
        self.httpx_client = httpx_client
        self.base_url = base_url

    @asynccontextmanager
    async def_get_client(self) -> AsyncIterator[httpx.AsyncClient]:
        if self.httpx_client:
            yield self.httpx_client
        else:
            async with httpx.AsyncClient(base_url=self.base_url or "") as client:
                yield client

    async defis_healthy(self) -> HealthResponse:
"""Check whether the workflow server is healthy.

        Raises:
            httpx.HTTPStatusError: If the server returns an error status.
        """
        async with self._get_client() as client:
            response = await client.get("/health")
            _raise_for_status_with_body(response)
            return HealthResponse.model_validate(response.json())

    async deflist_workflows(self) -> WorkflowsListResponse:
"""List the names of all workflows registered on the server."""
        async with self._get_client() as client:
            response = await client.get("/workflows")

            _raise_for_status_with_body(response)

            return WorkflowsListResponse.model_validate(response.json())

    async defrun_workflow(
        self,
        workflow_name: str,
        handler_id: str | None = None,
        start_event: StartEvent | dict[str, Any] | None = None,
        context: Context | dict[str, Any] | None = None,
    ) -> HandlerData:
"""Run the workflow and block until completion.

        Args:
            workflow_name: Name of the registered workflow to run.
            start_event: Input event for the workflow. Can be a ``StartEvent``
                instance or a plain dict.
            context: Workflow context to restore, for continuing a previous run.
            handler_id: Handler identifier to continue from a previous
                completed run.

        Returns:
            HandlerData: Handler metadata including the final result.
        """
        if start_event is not None:
            try:
                start_event = _serialize_event(start_event, bare=True)
            except Exception as e:
                raise ValueError(
                    f"Impossible to serialize the start event because of: {e}"
                )
        if isinstance(context, Context):
            try:
                context = context.to_dict()
            except Exception as e:
                raise ValueError(f"Impossible to serialize the context because of: {e}")
        request_body: dict[str, Any] = {
            "start_event": start_event
            if start_event is not None
            else _serialize_event(StartEvent(), bare=True),
            "context": context if context is not None else {},
        }
        if handler_id:
            request_body["handler_id"] = handler_id
        async with self._get_client() as client:
            response = await client.post(
                f"/workflows/{workflow_name}/run", json=request_body
            )

            _raise_for_status_with_body(response)

            return HandlerData.model_validate(response.json())

    async defrun_workflow_nowait(
        self,
        workflow_name: str,
        handler_id: str | None = None,
        start_event: StartEvent | dict[str, Any] | None = None,
        context: Context | dict[str, Any] | None = None,
    ) -> HandlerData:
"""Start the workflow without waiting for completion.

        Use the returned ``handler_id`` to stream events, poll for results,
        or send events.

        Args:
            workflow_name: Name of the registered workflow to run.
            start_event: Input event for the workflow. Can be a ``StartEvent``
                instance or a plain dict.
            context: Workflow context to restore, for continuing a previous run.
            handler_id: Handler identifier to continue from a previous
                completed run.

        Returns:
            HandlerData: Handler metadata including the ``handler_id``.
        """
        if start_event is not None:
            try:
                start_event = _serialize_event(start_event)
            except Exception as e:
                raise ValueError(
                    f"Impossible to serialize the start event because of: {e}"
                )
        if isinstance(context, Context):
            try:
                context = context.to_dict()
            except Exception as e:
                raise ValueError(f"Impossible to serialize the context because of: {e}")
        request_body: dict[str, Any] = {
            "start_event": start_event
            if start_event is not None
            else _serialize_event(StartEvent()),
            "context": context if context is not None else {},
        }
        if handler_id:
            request_body["handler_id"] = handler_id
        async with self._get_client() as client:
            response = await client.post(
                f"/workflows/{workflow_name}/run-nowait", json=request_body
            )

            _raise_for_status_with_body(response)

            return HandlerData.model_validate(response.json())

    defget_workflow_events(
        self,
        handler_id: str,
        include_internal_events: bool = False,
        after_sequence: int | Literal["now"] = -1,
        max_reconnect_attempts: int = 3,
    ) -> EventStream:
"""Stream events as they are produced by the workflow.

        Returns an ``EventStream`` whose ``last_sequence`` property tracks
        the sequence number of the most recently yielded event. Uses SSE
        and automatically reconnects from the last received event on
        connection drops.

        Example:

            stream = client.get_workflow_events(handler_id)
            async for event in stream:
                print(event.type, stream.last_sequence)

        Args:
            handler_id: ID of the handler running the workflow.
            include_internal_events: Include internal dispatch events.
                Defaults to ``False``.
            after_sequence: Where to start streaming. ``-1`` (default) streams
                all events from the beginning. ``"now"`` skips existing events
                and only delivers new ones. An integer ``N`` streams events
                after sequence ``N``.
            max_reconnect_attempts: Maximum reconnect attempts on connection
                drop. Defaults to ``3``.
        """
        queue: asyncio.Queue[_QueueItem] = asyncio.Queue()
        stream = EventStream(queue, None, after_sequence)

        async defreader() -> None:
            incl_inter = "true" if include_internal_events else "false"
            url = f"/events/{handler_id}"
            last_sequence: int | Literal["now"] = after_sequence
            attempts = 0
            try:
                while True:
                    async with self._get_client() as client:
                        try:
                            async with client.stream(
                                "GET",
                                url,
                                params={
                                    "sse": "true",
                                    "include_internal": incl_inter,
                                    "after_sequence": str(last_sequence),
                                },
                                headers={"Connection": "keep-alive"},
                                timeout=None,
                            ) as response:
                                if response.status_code == 404:
                                    raise ValueError("Handler not found")
                                elif response.status_code == 204:
                                    await queue.put(_QueuedDone())
                                    return

                                _raise_for_status_with_body(response)

                                # Reset attempts on successful connection
                                attempts = 0

                                # Parse SSE stream: "id: N\ndata: {...}\n\n"
                                current_id: str | None = None
                                async for line in response.aiter_lines():
                                    stripped = line.strip()
                                    if not stripped:
                                        # Empty line = end of SSE event
                                        continue
                                    if stripped.startswith("id:"):
                                        current_id = stripped[3:].strip()
                                    elif stripped.startswith("data:"):
                                        data = stripped[5:].strip()
                                        event = EventEnvelopeWithMetadata.model_validate_json(
                                            data
                                        )
                                        if current_id is not None:
                                            try:
                                                last_sequence = int(current_id)
                                            except ValueError:
                                                pass
                                        await queue.put(
                                            _QueuedEvent(
                                                sequence=last_sequence,
                                                event=event,
                                            )
                                        )
                                        current_id = None

                            # Stream ended normally (server closed connection)
                            await queue.put(_QueuedDone())
                            return

                        except httpx.TimeoutException:
                            raise TimeoutError(
                                f"Timeout waiting for events from handler {handler_id}"
                            )
                        except (httpx.RequestError, ConnectionError):
                            attempts += 1
                            if attempts  max_reconnect_attempts:
                                raise ConnectionError(
                                    f"Failed to connect to event stream after {max_reconnect_attempts} attempts"
                                )
                            # Retry from last received sequence
            except asyncio.CancelledError:
                await queue.put(_QueuedDone())
            except BaseException as exc:
                await queue.put(_QueuedError(exc))

        stream._task = asyncio.create_task(reader())
        return stream

    async defsend_event(
        self,
        handler_id: str,
        event: Event | dict[str, Any],
        step: str | None = None,
    ) -> SendEventResponse:
"""Send an event to a running workflow.

        Useful for human-in-the-loop workflows that wait for external input.

        Args:
            handler_id: ID of the handler running the workflow.
            event: Event to send, as an ``Event`` instance or a dict.
            step: Target a specific workflow step. When ``None``, the event
                is broadcast to all waiting steps.
        """
        try:
            serialized_event: dict[str, Any] = _serialize_event(event)
        except Exception as e:
            raise ValueError(f"Error while serializing the provided event: {e}")
        request_body: dict[str, Any] = {"event": serialized_event}
        if step:
            request_body["step"] = step
        async with self._get_client() as client:
            response = await client.post(f"/events/{handler_id}", json=request_body)
            _raise_for_status_with_body(response)

            return SendEventResponse.model_validate(response.json())

    async defget_result(self, handler_id: str) -> HandlerData:
"""
        Deprecated. Use get_handler instead.
        """
        return await self.get_handler(handler_id)

    async defget_handlers(
        self,
        status: list[Status] | None = None,
        workflow_name: list[str] | None = None,
    ) -> HandlersListResponse:
"""List all workflow handlers.

        Args:
            status: Filter by handler status (e.g. ``"running"``,
                ``"completed"``).
            workflow_name: Filter by workflow name.
        """
        async with self._get_client() as client:
            response = await client.get(
                "/handlers",
                params={
                    "status": status,
                    "workflow_name": workflow_name,
                },
            )
            _raise_for_status_with_body(response)

            return HandlersListResponse.model_validate(response.json())

    async defget_handler(self, handler_id: str) -> HandlerData:
"""Get a workflow handler by ID.

        Returns handler metadata including status, result (if completed),
        and timestamps.

        Args:
            handler_id: ID of the handler.
        """
        async with self._get_client() as client:
            response = await client.get(f"/handlers/{handler_id}")
            _raise_for_status_with_body(response)

            return HandlerData.model_validate(response.json())

    async defcancel_handler(
        self, handler_id: str, purge: bool = False
    ) -> CancelHandlerResponse:
"""Cancel a running workflow.

        Args:
            handler_id: ID of the handler to cancel.
            purge: Also remove the handler from the persistence store.
                Defaults to ``False``.
        """
        async with self._get_client() as client:
            response = await client.post(
                f"/handlers/{handler_id}/cancel",
                params={"purge": "true" if purge else "false"},
            )
            _raise_for_status_with_body(response)

            return CancelHandlerResponse.model_validate(response.json())

```
 |  
| --- | --- |  
###  is_healthy [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/client/#llama_agents.client.WorkflowClient.is_healthy "Permanent link")

```
is_healthy() -> HealthResponse

```

Check whether the workflow server is healthy.
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `HTTPStatusError`  |  If the server returns an error status.  |  
Source code in `llama_agents/client/client.py`  
| 
```
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
async defis_healthy(self) -> HealthResponse:
"""Check whether the workflow server is healthy.

    Raises:
        httpx.HTTPStatusError: If the server returns an error status.
    """
    async with self._get_client() as client:
        response = await client.get("/health")
        _raise_for_status_with_body(response)
        return HealthResponse.model_validate(response.json())

```
 |  
| --- | --- |  
###  list_workflows [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/client/#llama_agents.client.WorkflowClient.list_workflows "Permanent link")

```
list_workflows() -> WorkflowsListResponse

```

List the names of all workflows registered on the server.
Source code in `llama_agents/client/client.py`  
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
```
 | 
```
async deflist_workflows(self) -> WorkflowsListResponse:
"""List the names of all workflows registered on the server."""
    async with self._get_client() as client:
        response = await client.get("/workflows")

        _raise_for_status_with_body(response)

        return WorkflowsListResponse.model_validate(response.json())

```
 |  
| --- | --- |  
###  run_workflow [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/client/#llama_agents.client.WorkflowClient.run_workflow "Permanent link")

```
run_workflow(workflow_name: , handler_id:  | None = None, start_event:  | [, ] | None = None, context:  | [, ] | None = None) -> 

```

Run the workflow and block until completion.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `workflow_name`  |  Name of the registered workflow to run.  |  _required_  |  
|  `start_event`  |  `StartEvent[](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.StartEvent "            StartEvent \(workflows.events.StartEvent\)") | dict[str, Any] | None`  |  Input event for the workflow. Can be a `StartEvent` instance or a plain dict.  |  `None`  |  
|  `context`  |  `Context[](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.Context "            Context \(workflows.Context\)") | dict[str, Any] | None`  |  Workflow context to restore, for continuing a previous run.  |  `None`  |  
|  `handler_id`  |  `str | None`  |  Handler identifier to continue from a previous completed run.  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `HandlerData`  |   |  Handler metadata including the final result.  |  
Source code in `llama_agents/client/client.py`  
| 
```
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
```
 | 
```
async defrun_workflow(
    self,
    workflow_name: str,
    handler_id: str | None = None,
    start_event: StartEvent | dict[str, Any] | None = None,
    context: Context | dict[str, Any] | None = None,
) -> HandlerData:
"""Run the workflow and block until completion.

    Args:
        workflow_name: Name of the registered workflow to run.
        start_event: Input event for the workflow. Can be a ``StartEvent``
            instance or a plain dict.
        context: Workflow context to restore, for continuing a previous run.
        handler_id: Handler identifier to continue from a previous
            completed run.

    Returns:
        HandlerData: Handler metadata including the final result.
    """
    if start_event is not None:
        try:
            start_event = _serialize_event(start_event, bare=True)
        except Exception as e:
            raise ValueError(
                f"Impossible to serialize the start event because of: {e}"
            )
    if isinstance(context, Context):
        try:
            context = context.to_dict()
        except Exception as e:
            raise ValueError(f"Impossible to serialize the context because of: {e}")
    request_body: dict[str, Any] = {
        "start_event": start_event
        if start_event is not None
        else _serialize_event(StartEvent(), bare=True),
        "context": context if context is not None else {},
    }
    if handler_id:
        request_body["handler_id"] = handler_id
    async with self._get_client() as client:
        response = await client.post(
            f"/workflows/{workflow_name}/run", json=request_body
        )

        _raise_for_status_with_body(response)

        return HandlerData.model_validate(response.json())

```
 |  
| --- | --- |  
###  run_workflow_nowait [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/client/#llama_agents.client.WorkflowClient.run_workflow_nowait "Permanent link")

```
run_workflow_nowait(workflow_name: , handler_id:  | None = None, start_event:  | [, ] | None = None, context:  | [, ] | None = None) -> 

```

Start the workflow without waiting for completion.
Use the returned `handler_id` to stream events, poll for results, or send events.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `workflow_name`  |  Name of the registered workflow to run.  |  _required_  |  
|  `start_event`  |  `StartEvent[](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.StartEvent "            StartEvent \(workflows.events.StartEvent\)") | dict[str, Any] | None`  |  Input event for the workflow. Can be a `StartEvent` instance or a plain dict.  |  `None`  |  
|  `context`  |  `Context[](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.Context "            Context \(workflows.Context\)") | dict[str, Any] | None`  |  Workflow context to restore, for continuing a previous run.  |  `None`  |  
|  `handler_id`  |  `str | None`  |  Handler identifier to continue from a previous completed run.  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `HandlerData`  |   |  Handler metadata including the `handler_id`.  |  
Source code in `llama_agents/client/client.py`  
| 
```
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
```
 | 
```
async defrun_workflow_nowait(
    self,
    workflow_name: str,
    handler_id: str | None = None,
    start_event: StartEvent | dict[str, Any] | None = None,
    context: Context | dict[str, Any] | None = None,
) -> HandlerData:
"""Start the workflow without waiting for completion.

    Use the returned ``handler_id`` to stream events, poll for results,
    or send events.

    Args:
        workflow_name: Name of the registered workflow to run.
        start_event: Input event for the workflow. Can be a ``StartEvent``
            instance or a plain dict.
        context: Workflow context to restore, for continuing a previous run.
        handler_id: Handler identifier to continue from a previous
            completed run.

    Returns:
        HandlerData: Handler metadata including the ``handler_id``.
    """
    if start_event is not None:
        try:
            start_event = _serialize_event(start_event)
        except Exception as e:
            raise ValueError(
                f"Impossible to serialize the start event because of: {e}"
            )
    if isinstance(context, Context):
        try:
            context = context.to_dict()
        except Exception as e:
            raise ValueError(f"Impossible to serialize the context because of: {e}")
    request_body: dict[str, Any] = {
        "start_event": start_event
        if start_event is not None
        else _serialize_event(StartEvent()),
        "context": context if context is not None else {},
    }
    if handler_id:
        request_body["handler_id"] = handler_id
    async with self._get_client() as client:
        response = await client.post(
            f"/workflows/{workflow_name}/run-nowait", json=request_body
        )

        _raise_for_status_with_body(response)

        return HandlerData.model_validate(response.json())

```
 |  
| --- | --- |  
###  get_workflow_events [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/client/#llama_agents.client.WorkflowClient.get_workflow_events "Permanent link")

```
get_workflow_events(handler_id: , include_internal_events:  = False, after_sequence:  | Literal['now'] = -1, max_reconnect_attempts:  = 3) -> 

```

Stream events as they are produced by the workflow.
Returns an `EventStream` whose `last_sequence` property tracks the sequence number of the most recently yielded event. Uses SSE and automatically reconnects from the last received event on connection drops.
Example:

```
stream = client.get_workflow_events(handler_id)
async for event in stream:
    print(event.type, stream.last_sequence)

```

Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `handler_id`  |  ID of the handler running the workflow.  |  _required_  |  
|  `include_internal_events`  |  `bool`  |  Include internal dispatch events. Defaults to `False`.  |  `False`  |  
|  `after_sequence`  |  `int | Literal['now']`  |  Where to start streaming. `-1` (default) streams all events from the beginning. `"now"` skips existing events and only delivers new ones. An integer `N` streams events after sequence `N`.  |  
|  `max_reconnect_attempts`  |  Maximum reconnect attempts on connection drop. Defaults to `3`.  |  
Source code in `llama_agents/client/client.py`  
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
```
 | 
```
defget_workflow_events(
    self,
    handler_id: str,
    include_internal_events: bool = False,
    after_sequence: int | Literal["now"] = -1,
    max_reconnect_attempts: int = 3,
) -> EventStream:
"""Stream events as they are produced by the workflow.

    Returns an ``EventStream`` whose ``last_sequence`` property tracks
    the sequence number of the most recently yielded event. Uses SSE
    and automatically reconnects from the last received event on
    connection drops.

    Example:

        stream = client.get_workflow_events(handler_id)
        async for event in stream:
            print(event.type, stream.last_sequence)

    Args:
        handler_id: ID of the handler running the workflow.
        include_internal_events: Include internal dispatch events.
            Defaults to ``False``.
        after_sequence: Where to start streaming. ``-1`` (default) streams
            all events from the beginning. ``"now"`` skips existing events
            and only delivers new ones. An integer ``N`` streams events
            after sequence ``N``.
        max_reconnect_attempts: Maximum reconnect attempts on connection
            drop. Defaults to ``3``.
    """
    queue: asyncio.Queue[_QueueItem] = asyncio.Queue()
    stream = EventStream(queue, None, after_sequence)

    async defreader() -> None:
        incl_inter = "true" if include_internal_events else "false"
        url = f"/events/{handler_id}"
        last_sequence: int | Literal["now"] = after_sequence
        attempts = 0
        try:
            while True:
                async with self._get_client() as client:
                    try:
                        async with client.stream(
                            "GET",
                            url,
                            params={
                                "sse": "true",
                                "include_internal": incl_inter,
                                "after_sequence": str(last_sequence),
                            },
                            headers={"Connection": "keep-alive"},
                            timeout=None,
                        ) as response:
                            if response.status_code == 404:
                                raise ValueError("Handler not found")
                            elif response.status_code == 204:
                                await queue.put(_QueuedDone())
                                return

                            _raise_for_status_with_body(response)

                            # Reset attempts on successful connection
                            attempts = 0

                            # Parse SSE stream: "id: N\ndata: {...}\n\n"
                            current_id: str | None = None
                            async for line in response.aiter_lines():
                                stripped = line.strip()
                                if not stripped:
                                    # Empty line = end of SSE event
                                    continue
                                if stripped.startswith("id:"):
                                    current_id = stripped[3:].strip()
                                elif stripped.startswith("data:"):
                                    data = stripped[5:].strip()
                                    event = EventEnvelopeWithMetadata.model_validate_json(
                                        data
                                    )
                                    if current_id is not None:
                                        try:
                                            last_sequence = int(current_id)
                                        except ValueError:
                                            pass
                                    await queue.put(
                                        _QueuedEvent(
                                            sequence=last_sequence,
                                            event=event,
                                        )
                                    )
                                    current_id = None

                        # Stream ended normally (server closed connection)
                        await queue.put(_QueuedDone())
                        return

                    except httpx.TimeoutException:
                        raise TimeoutError(
                            f"Timeout waiting for events from handler {handler_id}"
                        )
                    except (httpx.RequestError, ConnectionError):
                        attempts += 1
                        if attempts  max_reconnect_attempts:
                            raise ConnectionError(
                                f"Failed to connect to event stream after {max_reconnect_attempts} attempts"
                            )
                        # Retry from last received sequence
        except asyncio.CancelledError:
            await queue.put(_QueuedDone())
        except BaseException as exc:
            await queue.put(_QueuedError(exc))

    stream._task = asyncio.create_task(reader())
    return stream

```
 |  
| --- | --- |  
###  send_event [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/client/#llama_agents.client.WorkflowClient.send_event "Permanent link")

```
send_event(handler_id: , event:  | [, ], step:  | None = None) -> 

```

Send an event to a running workflow.
Useful for human-in-the-loop workflows that wait for external input.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `handler_id`  |  ID of the handler running the workflow.  |  _required_  |  
|  `event`  |  `Event[](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.Event "            Event \(workflows.events.Event\)") | dict[str, Any]`  |  Event to send, as an `Event` instance or a dict.  |  _required_  |  
|  `step`  |  `str | None`  |  Target a specific workflow step. When `None`, the event is broadcast to all waiting steps.  |  `None`  |  
Source code in `llama_agents/client/client.py`  
| 
```
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
```
 | 
```
async defsend_event(
    self,
    handler_id: str,
    event: Event | dict[str, Any],
    step: str | None = None,
) -> SendEventResponse:
"""Send an event to a running workflow.

    Useful for human-in-the-loop workflows that wait for external input.

    Args:
        handler_id: ID of the handler running the workflow.
        event: Event to send, as an ``Event`` instance or a dict.
        step: Target a specific workflow step. When ``None``, the event
            is broadcast to all waiting steps.
    """
    try:
        serialized_event: dict[str, Any] = _serialize_event(event)
    except Exception as e:
        raise ValueError(f"Error while serializing the provided event: {e}")
    request_body: dict[str, Any] = {"event": serialized_event}
    if step:
        request_body["step"] = step
    async with self._get_client() as client:
        response = await client.post(f"/events/{handler_id}", json=request_body)
        _raise_for_status_with_body(response)

        return SendEventResponse.model_validate(response.json())

```
 |  
| --- | --- |  
###  get_handlers [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/client/#llama_agents.client.WorkflowClient.get_handlers "Permanent link")

```
get_handlers(status: [Status] | None = None, workflow_name: [] | None = None) -> 

```

List all workflow handlers.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `status`  |  `list[Status] | None`  |  Filter by handler status (e.g. `"running"`, `"completed"`).  |  `None`  |  
|  `workflow_name`  |  `list[str] | None`  |  Filter by workflow name.  |  `None`  |  
Source code in `llama_agents/client/client.py`  
| 
```
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
488
489
490
491
492
493
494
495
```
 | 
```
async defget_handlers(
    self,
    status: list[Status] | None = None,
    workflow_name: list[str] | None = None,
) -> HandlersListResponse:
"""List all workflow handlers.

    Args:
        status: Filter by handler status (e.g. ``"running"``,
            ``"completed"``).
        workflow_name: Filter by workflow name.
    """
    async with self._get_client() as client:
        response = await client.get(
            "/handlers",
            params={
                "status": status,
                "workflow_name": workflow_name,
            },
        )
        _raise_for_status_with_body(response)

        return HandlersListResponse.model_validate(response.json())

```
 |  
| --- | --- |  
###  get_handler [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/client/#llama_agents.client.WorkflowClient.get_handler "Permanent link")

```
get_handler(handler_id: ) -> 

```

Get a workflow handler by ID.
Returns handler metadata including status, result (if completed), and timestamps.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `handler_id`  |  ID of the handler.  |  _required_  |  
Source code in `llama_agents/client/client.py`  
| 
```
497
498
499
500
501
502
503
504
505
506
507
508
509
510
```
 | 
```
async defget_handler(self, handler_id: str) -> HandlerData:
"""Get a workflow handler by ID.

    Returns handler metadata including status, result (if completed),
    and timestamps.

    Args:
        handler_id: ID of the handler.
    """
    async with self._get_client() as client:
        response = await client.get(f"/handlers/{handler_id}")
        _raise_for_status_with_body(response)

        return HandlerData.model_validate(response.json())

```
 |  
| --- | --- |  
###  cancel_handler [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/client/#llama_agents.client.WorkflowClient.cancel_handler "Permanent link")

```
cancel_handler(handler_id: , purge:  = False) -> 

```

Cancel a running workflow.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `handler_id`  |  ID of the handler to cancel.  |  _required_  |  
|  `purge`  |  `bool`  |  Also remove the handler from the persistence store. Defaults to `False`.  |  `False`  |  
Source code in `llama_agents/client/client.py`  
| 
```
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
```
 | 
```
async defcancel_handler(
    self, handler_id: str, purge: bool = False
) -> CancelHandlerResponse:
"""Cancel a running workflow.

    Args:
        handler_id: ID of the handler to cancel.
        purge: Also remove the handler from the persistence store.
            Defaults to ``False``.
    """
    async with self._get_client() as client:
        response = await client.post(
            f"/handlers/{handler_id}/cancel",
            params={"purge": "true" if purge else "false"},
        )
        _raise_for_status_with_body(response)

        return CancelHandlerResponse.model_validate(response.json())

```
 |  
| --- | --- |  
##  EventStream [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/client/#llama_agents.client.EventStream "Permanent link")
Async iterator over workflow events that exposes the current stream position.
Returned by `WorkflowClient.get_workflow_events()`. Use `last_sequence` to capture the cursor for resuming later::

```
stream = client.get_workflow_events(handler_id)
async for event in stream:
    print(event.type, stream.last_sequence)

# Resume from where we left off:
stream = client.get_workflow_events(
    handler_id, after_sequence=stream.last_sequence
)

```
Source code in `llama_agents/client/client.py`  
| 
```
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
```
 | 
```
classEventStream:
"""Async iterator over workflow events that exposes the current stream position.

    Returned by ``WorkflowClient.get_workflow_events()``. Use
    ``last_sequence`` to capture the cursor for resuming later::

        stream = client.get_workflow_events(handler_id)
        async for event in stream:
            print(event.type, stream.last_sequence)

        # Resume from where we left off:
        stream = client.get_workflow_events(
            handler_id, after_sequence=stream.last_sequence

    """

    def__init__(
        self,
        queue: asyncio.Queue[_QueueItem],
        task: asyncio.Task[None] | None,
        initial_sequence: int | Literal["now"],
    ) -> None:
        self._queue = queue
        self._task = task
        self._last_sequence: int | Literal["now"] = initial_sequence
        self._iter_started = False

    @property
    deflast_sequence(self) -> int | Literal["now"]:
"""The sequence number of the most recently yielded event, or the
        initial ``after_sequence`` value if no events have been yielded yet."""
        return self._last_sequence

    def__aiter__(self) -> AsyncIterator[EventEnvelopeWithMetadata]:
        if self._iter_started:
            raise RuntimeError("EventStream can only be iterated once")
        self._iter_started = True
        return self._iterate()

    async def_iterate(self) -> AsyncGenerator[EventEnvelopeWithMetadata, None]:
        try:
            while True:
                item = await self._queue.get()
                if isinstance(item, _QueuedDone):
                    return
                if isinstance(item, _QueuedError):
                    raise item.error
                self._last_sequence = item.sequence
                yield item.event
        finally:
            await self.aclose()

    async defaclose(self) -> None:
"""Cancel the background reader and release resources."""
        if self._task is None:
            return
        task, self._task = self._task, None
        task.cancel()
        try:
            await task
        except (asyncio.CancelledError, Exception):
            pass

```
 |  
| --- | --- |  
###  last_sequence `property` [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/client/#llama_agents.client.EventStream.last_sequence "Permanent link")

```
last_sequence:  | Literal['now']

```

The sequence number of the most recently yielded event, or the initial `after_sequence` value if no events have been yielded yet.
###  aclose [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/client/#llama_agents.client.EventStream.aclose "Permanent link")

```
aclose() -> None

```

Cancel the background reader and release resources.
Source code in `llama_agents/client/client.py`  
| 
```
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
```
 | 
```
async defaclose(self) -> None:
"""Cancel the background reader and release resources."""
    if self._task is None:
        return
    task, self._task = self._task, None
    task.cancel()
    try:
        await task
    except (asyncio.CancelledError, Exception):
        pass

```
 |  
| --- | --- |
