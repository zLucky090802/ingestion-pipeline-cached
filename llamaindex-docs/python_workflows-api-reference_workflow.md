# Workflow
##  Workflow [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow/#workflows.workflow.Workflow "Permanent link")
Event-driven orchestrator to define and run application flows using typed steps.
A `Workflow` is composed of `@step`-decorated callables that accept and emit typed [Event](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.Event "            Event")s. Steps can be declared as instance methods or as free functions registered via the decorator.
Key features: - Validation of step signatures and event graph before running - Typed start/stop events - Streaming of intermediate events - Optional human-in-the-loop events - Retry policies per step - Resource injection
Examples:
Basic usage:

```
fromworkflowsimport Workflow, step
fromworkflows.eventsimport StartEvent, StopEvent

classMyFlow(Workflow):
    @step
    async defstart(self, ev: StartEvent) -> StopEvent:
        return StopEvent(result="done")

result = await MyFlow(timeout=60).run(topic="Pirates")

```

Custom start/stop events and streaming:

```
handler = MyFlow().run()
async for ev in handler.stream_events():
    ...
result = await handler

```

See Also

Source code in `workflows/workflow.py`  
| 
```
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
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
```
 | 
```
classWorkflow(metaclass=WorkflowMeta):
"""
    Event-driven orchestrator to define and run application flows using typed steps.

    A `Workflow` is composed of `@step`-decorated callables that accept and emit
    typed [Event][workflows.events.Event]s. Steps can be declared as instance
    methods or as free functions registered via the decorator.

    Key features:
    - Validation of step signatures and event graph before running
    - Typed start/stop events
    - Streaming of intermediate events
    - Optional human-in-the-loop events
    - Retry policies per step
    - Resource injection

    Examples:
        Basic usage:

        ```python
        from workflows import Workflow, step
        from workflows.events import StartEvent, StopEvent

        class MyFlow(Workflow):
            @step
            async def start(self, ev: StartEvent) -> StopEvent:
                return StopEvent(result="done")

        result = await MyFlow(timeout=60).run(topic="Pirates")
        ```

        Custom start/stop events and streaming:

        ```python
        handler = MyFlow().run()
        async for ev in handler.stream_events():

        result = await handler
        ```

    See Also:
        - [step][workflows.decorators.step]
        - [Event][workflows.events.Event]
        - [Context][workflows.context.context.Context]
        - [WorkflowHandler][workflows.handler.WorkflowHandler]
        - [RetryPolicy][workflows.retry_policy.RetryPolicy]
    """

    # Populated by the metaclass; declared here for type checkers.
    _step_functions: dict[str, StepFunction]
    _step_functions_version: int = 0

    _runtime: Runtime
    _workflow_name: str | None

    def__init__(
        self,
        timeout: float | None = 45.0,
        disable_validation: bool = False,
        verbose: bool = False,
        resource_manager: ResourceManager | None = None,
        num_concurrent_runs: int | None = None,
        runtime: Runtime | None = None,
        workflow_name: str | None = None,
        skip_graph_checks: set[WorkflowGraphCheck] | None = None,
    ) -> None:
"""
        Initialize a workflow instance.

        Args:
            timeout (float | None): Max seconds to wait for completion. `None`
                disables the timeout.
            disable_validation (bool): Skip pre-run validation of the event graph
                (not recommended).
            verbose (bool): If True, print step activity.
            resource_manager (ResourceManager | None): Custom resource manager
                for dependency injection.
            num_concurrent_runs (int | None): Limit on concurrent `run()` calls.
            runtime (Runtime | None): Optional runtime to use for this workflow.
                If not provided, uses the current context-scoped runtime or
                falls back to basic_runtime.
            workflow_name (str | None): Optional explicit name for this workflow.
                If not provided, a module-qualified name is computed from
                the class's `__module__` and `__qualname__` attributes.
            skip_graph_checks (set[str] | None): Optional set of graph validation
                checks to skip (e.g. "reachability", "terminal_event"). Use to
                allow intentional patterns that would otherwise fail validation.
        """
        # Configuration
        self._timeout = timeout
        self._verbose = verbose
        self._disable_validation = disable_validation
        self._num_concurrent_runs = num_concurrent_runs
        # Store explicit name (None means use computed name)
        self._workflow_name = workflow_name
        # Detect StartEvent issues before StopEvent for clearer guidance
        self._start_event_class = self._ensure_start_event_class()
        self._stop_event_class = self._ensure_stop_event_class()
        self._events = self._ensure_events_collected()
        # Resource management
        self._resource_manager = resource_manager or ResourceManager()
        # Instrumentation
        self._dispatcher = dispatcher
        self._runtime_locked = False
        # Validation cache: set after first successful _validate(); skip re-validation on run() until invalidated.
        # _validated_version tracks which _step_functions_version was validated so add_step() invalidates the cache.
        self._validation_result: bool | None = None
        self._validated_version: int = -1
        checks = skip_graph_checks or set()
        valid_checks = set(get_args(WorkflowGraphCheck))
        unknown = checks - valid_checks
        if unknown:
            raise WorkflowValidationError(
                f"Unknown graph check names: {', '.join(sorted(unknown))}. "
                f"Valid names are: {', '.join(sorted(valid_checks))}"
            )
        self._skip_graph_checks: set[WorkflowGraphCheck] = checks

        # Runtime registration: explicit > context-scoped > basic_runtime
        fromworkflows.plugins._contextimport get_current_runtime

        if runtime is not None:
            self._runtime = runtime
        else:
            # get_current_runtime() falls back to basic_runtime
            self._runtime = get_current_runtime()

        # Wrap with verbose decorator if requested
        if self._verbose:
            fromworkflows.runtime.verboseimport VerboseDecorator

            self._runtime = VerboseDecorator(self._runtime)

        # Register with runtime for tracking (no-op for BasicRuntime)
        self._runtime.track_workflow(self)

    def_validate_valid_step_message(self, step: str, message: Event) -> None:
"""Validate that a step name exists in the workflow."""
        if step not in self._get_steps():
            raise WorkflowRuntimeError(f"Step {step} does not exist")

        step_func = self._get_steps()[step]
        step_config = step_func._step_config
        if type(message) not in step_config.accepted_events:
            raise WorkflowRuntimeError(
                f"Step {step} does not accept event of type {type(message)}"
            )

    @property
    defruntime(self) -> Runtime:
"""The runtime this workflow is registered with."""
        return self._runtime

    def_switch_runtime(self, new_runtime: Runtime) -> None:
        if new_runtime is self._runtime:
            return
        if self._runtime_locked:
            raise RuntimeError(
                "Cannot reassign runtime after workflow has been launched"
            )
        old = self._runtime
        old.untrack_workflow(self)
        self._runtime = new_runtime
        new_runtime.track_workflow(self)

    @property
    defworkflow_name(self) -> str:
"""
        The workflow name.

        If an explicit name was provided at construction, returns that.
        Otherwise, returns a module-qualified name based on the class's
        __module__ and __qualname__ attributes.

        Examples:
            - Explicit: `Workflow(workflow_name="my-workflow")` → `"my-workflow"`
            - Module-level class: `"mymodule.MyWorkflow"`
            - Nested class: `"mymodule.Outer.Inner"`
            - Function-scoped: `"mymodule.func.<locals>.LocalWorkflow"`
        """
        if self._workflow_name is not None:
            return self._workflow_name
        cls = self.__class__
        return f"{cls.__module__}.{cls.__qualname__}"

    def_switch_workflow_name(self, name: str) -> None:
        if self._runtime_locked and name != self._workflow_name:
            raise RuntimeError(
                "Cannot change workflow_name after workflow has been launched"
            )
        self._workflow_name = name

    def_ensure_start_event_class(self) -> type[StartEvent]:
"""
        Returns the StartEvent type used in this workflow.

        It works by inspecting the events received by the step methods.
        """
        start_events_found: set[type[StartEvent]] = set()
        for step_func in self._get_steps().values():
            step_config: StepConfig = step_func._step_config
            for event_type in step_config.accepted_events:
                if issubclass(event_type, StartEvent):
                    start_events_found.add(event_type)

        num_found = len(start_events_found)
        if num_found == 0:
            cls_name = self.__class__.__name__
            msg = (
                "At least one Event of type StartEvent must be received by any step. "
                f"(Workflow '{cls_name}' has no @step that accepts StartEvent.)"
            )
            raise WorkflowConfigurationError(msg)
        elif num_found  1:
            cls_name = self.__class__.__name__
            msg = (
                f"Only one type of StartEvent is allowed per workflow, found {num_found}: {start_events_found} "
                f"in workflow '{cls_name}'."
            )
            raise WorkflowConfigurationError(msg)
        else:
            return start_events_found.pop()

    @property
    defstart_event_class(self) -> type[StartEvent]:
"""The `StartEvent` subclass accepted by this workflow.

        Determined by inspecting step input types.
        """
        return self._start_event_class

    @property
    defevents(self) -> list[type[Event]]:
"""Returns all known events emitted by this workflow.

        Determined by inspecting step input/output types.
        """
        return self._events

    def_ensure_events_collected(self) -> list[type[Event]]:
"""Returns all known events emitted by this workflow.

        Determined by inspecting step input/output types.
        """
        events_found: set[type[Event]] = set()
        for step_func in self._get_steps().values():
            step_config: StepConfig = step_func._step_config

            # Do not collect events from the done step
            if step_func.__name__ == "_done":
                continue

            for event_type in step_config.return_types:
                if issubclass(event_type, Event):
                    events_found.add(event_type)
            for event_type in step_config.accepted_events:
                if issubclass(event_type, Event):
                    events_found.add(event_type)

        return list(events_found)

    def_ensure_stop_event_class(self) -> type[RunResultT]:
"""
        Returns the StopEvent type used in this workflow.

        It works by inspecting the events returned.
        """
        stop_events_found: set[type[StopEvent]] = set()
        for step_func in self._get_steps().values():
            step_config: StepConfig = step_func._step_config
            for event_type in step_config.return_types:
                if issubclass(event_type, StopEvent):
                    stop_events_found.add(event_type)

        num_found = len(stop_events_found)
        if num_found == 0:
            cls_name = self.__class__.__name__
            msg = (
                "At least one Event of type StopEvent must be returned by any step. "
                f"(Workflow '{cls_name}' has no @step that returns StopEvent.)"
            )
            raise WorkflowConfigurationError(msg)
        elif num_found  1:
            cls_name = self.__class__.__name__
            msg = (
                f"Only one type of StopEvent is allowed per workflow, found {num_found}: {stop_events_found} "
                f"in workflow '{cls_name}'."
            )
            raise WorkflowConfigurationError(msg)
        else:
            return stop_events_found.pop()

    @property
    defstop_event_class(self) -> type[RunResultT]:
"""The `StopEvent` subclass produced by this workflow.

        Determined by inspecting step return annotations.
        """
        return self._stop_event_class

    @classmethod
    def_get_steps_from_class(cls) -> dict[str, StepFunction]:
"""Returns all the steps, whether defined as methods or free functions."""
        return {**get_steps_from_class(cls), **cls._step_functions}

    @classmethod
    defadd_step(cls, func: StepFunction) -> None:
"""
        Adds a free function as step for this workflow instance.

        It raises an exception if a step with the same name was already added to the workflow.
        """
        step_config: StepConfig | None = getattr(func, "_step_config", None)
        if not step_config:
            msg = f"Step function {func.__name__} is missing the `@step` decorator."
            raise WorkflowValidationError(msg)

        if func.__name__ in cls._get_steps_from_class():
            msg = f"A step {func.__name__} is already part of this workflow, please choose another name."
            raise WorkflowValidationError(msg)

        cls._step_functions[func.__name__] = func
        cls._step_functions_version += 1

    def_get_steps(self) -> dict[str, StepFunction]:
"""Returns all the steps, whether defined as methods or free functions."""
        return {**get_steps_from_instance(self), **self.__class__._step_functions}

    def_get_start_event_instance(
        self, start_event: StartEvent | None, **kwargs: Any
    ) -> StartEvent:
        if start_event is not None:
            # start_event was used wrong
            if not isinstance(start_event, StartEvent):
                msg = "The 'start_event' argument must be an instance of 'StartEvent'."
                raise ValueError(msg)

            # start_event is ok but point out that additional kwargs will be ignored in this case
            if kwargs:
                msg = (
                    "Keyword arguments are not supported when 'run()' is invoked with the 'start_event' parameter."
                    f" These keyword arguments will be ignored: {kwargs}"
                )
                logger.warning(msg)
            return start_event

        # Old style start event creation, with kwargs used to create an instance of self._start_event_class
        try:
            return self._start_event_class(**kwargs)
        except ValidationError as e:
            ev_name = self._start_event_class.__name__
            msg = f"Failed creating a start event of type '{ev_name}' with the keyword arguments: {kwargs}"
            logger.debug(e)
            raise WorkflowRuntimeError(msg)

    defrun(
        self,
        ctx: Context | None = None,
        start_event: StartEvent | None = None,
        **kwargs: Any,
    ) -> WorkflowHandler:
"""Run the workflow and return a handler for results and streaming.

        This schedules the workflow execution in the background and returns a
        [WorkflowHandler][workflows.handler.WorkflowHandler] that can be awaited
        for the final result or used to stream intermediate events.

        You may pass either a concrete `start_event` instance or keyword
        arguments that will be used to construct the inferred
        [StartEvent][workflows.events.StartEvent] subclass.

        Args:
            ctx (Context | None): Optional context to resume or share state
                across runs. If omitted, a fresh context is created.
            start_event (StartEvent | None): Optional explicit start event.
            **kwargs (Any): Keyword args to initialize the start event when
                `start_event` is not provided.

        Returns:
            WorkflowHandler: A future-like object to await the final result and
            stream events.

        Raises:
            WorkflowValidationError: If validation fails and validation is
                enabled.
            WorkflowRuntimeError: If the start event cannot be created from kwargs.
            WorkflowTimeoutError: If execution exceeds the configured timeout.

        Examples:
            ```python
            # Create and run with kwargs
            handler = MyFlow().run(topic="Pirates")

            # Stream events
            async for ev in handler.stream_events():


            # Await final result
            result = await handler


            If you subclassed the start event, you can also directly pass it in:

            ```python
            result = await my_workflow.run(start_event=MyStartEvent(topic="Pirates"))

        """
        fromworkflows.contextimport Context

        if not self._runtime_locked:
            # don't allow switching runtime after a workflow has been launched
            self._runtime_locked = True

        # Validate the workflow
        self._validate()

        # Extract run_id before passing remaining kwargs to start event
        run_id = kwargs.pop("run_id", None)

        # If a previous context is provided, pass its serialized form
        ctx = ctx if ctx is not None else Context(self)
        # TODO(v3) - remove dependency on is running for choosing whether to send a StartEvent.
        # Is not an easily synchronously queryable property.
        start_event_instance: StartEvent | None = (
            None
            if ctx.is_running
            else self._get_start_event_instance(start_event, **kwargs)
        )
        return ctx._workflow_run(
            workflow=self, start_event=start_event_instance, run_id=run_id
        )

    def_validate_graph_structure(self) -> None:
"""Check that all steps are reachable from input events and only output events are terminal.

        Delegates to the pure ``validate_graph`` function in the representation
        package and raises a single ``WorkflowValidationError`` listing every
        problem found.
        """
        from.representation.validateimport validate_graph

        step_configs = {
            name: func._step_config for name, func in self._get_steps().items()
        }
        errors = validate_graph(
            steps=step_configs,
            start_event_class=self._start_event_class,
            skip_checks=self._skip_graph_checks,
        )
        if errors:
            detail = "\n".join(
                f"  - [{e.check}] {e.message}\n{e.hint}" for e in errors
            )
            raise WorkflowValidationError(f"Graph validation failed:\n{detail}")

    def_validate_resource_configs(self) -> list[str]:
"""Validate all resource configs (including nested ones) by loading them."""
        errors: list[str] = []
        seen: set[str] = set()

        # Stack-based traversal of all resources and their dependencies
        stack: list[_ResourceValidationContext] = []
        for step_func in self._get_steps().values():
            step_name = step_func.__name__
            for res_def in step_func._step_config.resources:
                res_def.resource.set_type_annotation(res_def.type_annotation)
                stack.append(
                    _ResourceValidationContext(
                        resource=res_def.resource,
                        step_name=step_name,
                        param_name=res_def.name,
                        resource_chain=[res_def.resource.name],
                    )
                )

        while stack:
            ctx = stack.pop()
            if ctx.resource.name in seen:
                continue
            seen.add(ctx.resource.name)

            # Add dependencies to stack
            for _dep_param, dep, type_ann in ctx.resource.get_dependencies():
                dep.set_type_annotation(type_ann)
                stack.append(ctx.with_dependency(dep))

            # Validate if it's a config
            if isinstance(ctx.resource, _ResourceConfig):
                try:
                    ctx.resource.call()
                except Exception as e:
                    errors.append(f"In {ctx.format_location()}: {e}")

        return errors

    async def_validate_resources(self) -> list[str]:
"""Validate all resources by resolving them (catches circular deps)."""
        errors: list[str] = []
        for step_func in self._get_steps().values():
            step_name = step_func.__name__
            for res_def in step_func._step_config.resources:
                res_def.resource.set_type_annotation(res_def.type_annotation)
                try:
                    await self._resource_manager.get(res_def.resource)
                except Exception as e:
                    location = f"step '{step_name}', parameter '{res_def.name}'"
                    errors.append(f"In {location}: {e}")
        return errors

    defvalidate(
        self,
        *,
        validate_resource_configs: bool = True,
        validate_resources: bool = False,
    ) -> bool:
"""
        Validate the workflow to ensure it's well-formed.

        This method validates the event graph and optionally validates resources:
        - Event production/consumption (set-based checks)
        - Graph structure: all steps reachable from an input event (StartEvent or HumanResponseEvent),
          and only output events (StopEvent, InputRequiredEvent) may be terminal
        - Resource configs (JSON files with Pydantic validation) are validated by default
        - Resource factories are not validated by default (may require env vars)
        - Circular resource dependencies are caught when validate_resources=True

        Validation result is cached after the first successful run(); subsequent run() calls
        skip re-validation. Calling validate() explicitly always re-runs all checks.

        Args:
            validate_resource_configs: If True (default), validate that resource
                config files exist and contain valid data for their Pydantic models.
            validate_resources: If False (default), skip resolving resource factories
                during validation. Set to True to also validate that resource
                factories can be resolved and detect circular dependencies
                (may require environment variables or external connections).

        Returns:
            True if the workflow uses human-in-the-loop, False otherwise.
        """
        return self._validate(
            validate_resource_configs=validate_resource_configs,
            validate_resources=validate_resources,
            force=True,  # Explicit validate() call should always run
        )

    def_validate(
        self,
        *,
        validate_resource_configs: bool = True,
        validate_resources: bool = False,
        force: bool = False,
    ) -> bool:
        if self._disable_validation and not force:
            return False
        stale = self._validated_version != self.__class__._step_functions_version
        if not force and not stale and self._validation_result is not None:
            return self._validation_result

        # Ensure at least one step is configured before inspecting events
        if not self._get_steps():
            cls_name = self.__class__.__name__
            msg = (
                f"Workflow '{cls_name}' has no configured steps. "
                "Did you forget to annotate methods with @step or to register "
                "free-function steps via @step(workflow=...)?"
            )
            raise WorkflowConfigurationError(msg)

        # Recompute StartEvent and StopEvent classes here to support dynamic changes
        # and to surface StartEvent errors before StopEvent during validation.
        self._start_event_class = self._ensure_start_event_class()
        self._stop_event_class = self._ensure_stop_event_class()

        produced_events: set[type] = {self._start_event_class}
        consumed_events: set[type] = set()

        # Collect steps that incorrectly accept StopEvent
        steps_accepting_stop_event: list[str] = []

        for name, step_func in self._get_steps().items():
            step_config: StepConfig = step_func._step_config

            # Check that no user-defined step accepts StopEvent (only _done step should)
            if name != "_done":
                for event_type in step_config.accepted_events:
                    if issubclass(event_type, StopEvent):
                        steps_accepting_stop_event.append(name)
                        break

            for event_type in step_config.accepted_events:
                consumed_events.add(event_type)

            for event_type in step_config.return_types:
                if event_type is type(None):
                    # some events may not trigger other events
                    continue

                produced_events.add(event_type)

        # Raise error if any steps incorrectly accept StopEvent
        if steps_accepting_stop_event:
            step_names = "', '".join(steps_accepting_stop_event)
            plural = "" if len(steps_accepting_stop_event) == 1 else "s"
            msg = f"Step{plural} '{step_names}' cannot accept StopEvent. StopEvent signals the end of the workflow. Use a different Event type instead."
            raise WorkflowValidationError(msg)

        # Check if no StopEvent is produced
        stop_ok = False
        for ev in produced_events:
            if issubclass(ev, StopEvent):
                stop_ok = True
                break
        if not stop_ok:
            msg = "No event of type StopEvent is produced."
            raise WorkflowValidationError(msg)

        # Check if all consumed events are produced (except specific built-in events)
        unconsumed_events = consumed_events - produced_events
        unconsumed_events = {
            x
            for x in unconsumed_events
            if not issubclass(x, (InputRequiredEvent, HumanResponseEvent, StopEvent))
        }
        if unconsumed_events:
            names = ", ".join(ev.__name__ for ev in unconsumed_events)
            raise WorkflowValidationError(
                f"The following events are consumed but never produced: {names}"
            )

        # Check if there are any unused produced events (except specific built-in events)
        unused_events = produced_events - consumed_events
        unused_events = {
            x
            for x in unused_events
            if not issubclass(
                x, (InputRequiredEvent, HumanResponseEvent, self._stop_event_class)
            )
        }
        if unused_events:
            names = ", ".join(ev.__name__ for ev in unused_events)
            raise WorkflowValidationError(
                f"The following events are produced but never consumed: {names}"
            )

        # Graph structural checks: reachability from input events, terminal events
        self._validate_graph_structure()

        # Resource validation
        if validate_resource_configs:
            if errors := self._validate_resource_configs():
                raise WorkflowValidationError(
                    "Resource config validation failed:\n"
                    + "\n".join(f"  - {e}" for e in errors)
                )

        if validate_resources:
            errors = asyncio.run(self._validate_resources())
            if errors:
                raise WorkflowValidationError(
                    "Resource validation failed:\n"
                    + "\n".join(f"  - {e}" for e in errors)
                )

        # Check if the workflow uses human-in-the-loop; cache result for subsequent run() calls
        self._validation_result = (
            InputRequiredEvent in produced_events
            or HumanResponseEvent in consumed_events
        )
        self._validated_version = self.__class__._step_functions_version
        return self._validation_result

```
 |  
| --- | --- |  
###  runtime `property` [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow/#workflows.workflow.Workflow.runtime "Permanent link")

```
runtime: Runtime

```

The runtime this workflow is registered with.
###  workflow_name `property` [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow/#workflows.workflow.Workflow.workflow_name "Permanent link")

```
workflow_name: 

```

The workflow name.
If an explicit name was provided at construction, returns that. Otherwise, returns a module-qualified name based on the class's **module** and **qualname** attributes.
Examples:
  * Explicit: `Workflow(workflow_name="my-workflow")` → `"my-workflow"`
  * Module-level class: `"mymodule.MyWorkflow"`
  * Nested class: `"mymodule.Outer.Inner"`
  * Function-scoped: `"mymodule.func.<locals>.LocalWorkflow"`


###  start_event_class `property` [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow/#workflows.workflow.Workflow.start_event_class "Permanent link")

```
start_event_class: []

```

The `StartEvent` subclass accepted by this workflow.
Determined by inspecting step input types.
###  events `property` [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow/#workflows.workflow.Workflow.events "Permanent link")

```
events: [[]]

```

Returns all known events emitted by this workflow.
Determined by inspecting step input/output types.
###  stop_event_class `property` [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow/#workflows.workflow.Workflow.stop_event_class "Permanent link")

```
stop_event_class: [RunResultT]

```

The `StopEvent` subclass produced by this workflow.
Determined by inspecting step return annotations.
###  __init__ [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow/#workflows.workflow.Workflow.__init__ "Permanent link")

```
__init__(timeout: float | None = 45.0, disable_validation:  = False, verbose:  = False, resource_manager: ResourceManager | None = None, num_concurrent_runs:  | None = None, runtime: Runtime | None = None, workflow_name:  | None = None, skip_graph_checks: [WorkflowGraphCheck] | None = None) -> None

```

Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `timeout`  |  `float | None`  |  Max seconds to wait for completion. `None` disables the timeout.  |  `45.0`  |  
|  `disable_validation`  |  `bool`  |  Skip pre-run validation of the event graph (not recommended).  |  `False`  |  
|  `verbose`  |  `bool`  |  If True, print step activity.  |  `False`  |  
|  `resource_manager`  |  `ResourceManager | None`  |  Custom resource manager for dependency injection.  |  `None`  |  
|  `num_concurrent_runs`  |  `int | None`  |  Limit on concurrent `run()` calls.  |  `None`  |  
|  `runtime`  |  `Runtime | None`  |  Optional runtime to use for this workflow. If not provided, uses the current context-scoped runtime or falls back to basic_runtime.  |  `None`  |  
|  `workflow_name`  |  `str | None`  |  Optional explicit name for this workflow. If not provided, a module-qualified name is computed from the class's `__module__` and `__qualname__` attributes.  |  `None`  |  
|  `skip_graph_checks`  |  `set[str] | None`  |  Optional set of graph validation checks to skip (e.g. "reachability", "terminal_event"). Use to allow intentional patterns that would otherwise fail validation.  |  `None`  |  
Source code in `workflows/workflow.py`  
| 
```
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
```
 | 
```
def__init__(
    self,
    timeout: float | None = 45.0,
    disable_validation: bool = False,
    verbose: bool = False,
    resource_manager: ResourceManager | None = None,
    num_concurrent_runs: int | None = None,
    runtime: Runtime | None = None,
    workflow_name: str | None = None,
    skip_graph_checks: set[WorkflowGraphCheck] | None = None,
) -> None:
"""
    Initialize a workflow instance.

    Args:
        timeout (float | None): Max seconds to wait for completion. `None`
            disables the timeout.
        disable_validation (bool): Skip pre-run validation of the event graph
            (not recommended).
        verbose (bool): If True, print step activity.
        resource_manager (ResourceManager | None): Custom resource manager
            for dependency injection.
        num_concurrent_runs (int | None): Limit on concurrent `run()` calls.
        runtime (Runtime | None): Optional runtime to use for this workflow.
            If not provided, uses the current context-scoped runtime or
            falls back to basic_runtime.
        workflow_name (str | None): Optional explicit name for this workflow.
            If not provided, a module-qualified name is computed from
            the class's `__module__` and `__qualname__` attributes.
        skip_graph_checks (set[str] | None): Optional set of graph validation
            checks to skip (e.g. "reachability", "terminal_event"). Use to
            allow intentional patterns that would otherwise fail validation.
    """
    # Configuration
    self._timeout = timeout
    self._verbose = verbose
    self._disable_validation = disable_validation
    self._num_concurrent_runs = num_concurrent_runs
    # Store explicit name (None means use computed name)
    self._workflow_name = workflow_name
    # Detect StartEvent issues before StopEvent for clearer guidance
    self._start_event_class = self._ensure_start_event_class()
    self._stop_event_class = self._ensure_stop_event_class()
    self._events = self._ensure_events_collected()
    # Resource management
    self._resource_manager = resource_manager or ResourceManager()
    # Instrumentation
    self._dispatcher = dispatcher
    self._runtime_locked = False
    # Validation cache: set after first successful _validate(); skip re-validation on run() until invalidated.
    # _validated_version tracks which _step_functions_version was validated so add_step() invalidates the cache.
    self._validation_result: bool | None = None
    self._validated_version: int = -1
    checks = skip_graph_checks or set()
    valid_checks = set(get_args(WorkflowGraphCheck))
    unknown = checks - valid_checks
    if unknown:
        raise WorkflowValidationError(
            f"Unknown graph check names: {', '.join(sorted(unknown))}. "
            f"Valid names are: {', '.join(sorted(valid_checks))}"
        )
    self._skip_graph_checks: set[WorkflowGraphCheck] = checks

    # Runtime registration: explicit > context-scoped > basic_runtime
    fromworkflows.plugins._contextimport get_current_runtime

    if runtime is not None:
        self._runtime = runtime
    else:
        # get_current_runtime() falls back to basic_runtime
        self._runtime = get_current_runtime()

    # Wrap with verbose decorator if requested
    if self._verbose:
        fromworkflows.runtime.verboseimport VerboseDecorator

        self._runtime = VerboseDecorator(self._runtime)

    # Register with runtime for tracking (no-op for BasicRuntime)
    self._runtime.track_workflow(self)

```
 |  
| --- | --- |  
###  add_step `classmethod` [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow/#workflows.workflow.Workflow.add_step "Permanent link")

```
add_step(func: StepFunction) -> None

```

Adds a free function as step for this workflow instance.
It raises an exception if a step with the same name was already added to the workflow.
Source code in `workflows/workflow.py`  
| 
```
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
```
 | 
```
@classmethod
defadd_step(cls, func: StepFunction) -> None:
"""
    Adds a free function as step for this workflow instance.

    It raises an exception if a step with the same name was already added to the workflow.
    """
    step_config: StepConfig | None = getattr(func, "_step_config", None)
    if not step_config:
        msg = f"Step function {func.__name__} is missing the `@step` decorator."
        raise WorkflowValidationError(msg)

    if func.__name__ in cls._get_steps_from_class():
        msg = f"A step {func.__name__} is already part of this workflow, please choose another name."
        raise WorkflowValidationError(msg)

    cls._step_functions[func.__name__] = func
    cls._step_functions_version += 1

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow/#workflows.workflow.Workflow.run "Permanent link")

```
run(ctx:  | None = None, start_event:  | None = None, **kwargs: ) -> 

```

Run the workflow and return a handler for results and streaming.
This schedules the workflow execution in the background and returns a [WorkflowHandler](https://developers.llamaindex.ai/python/workflows-api-reference/handler/#workflows.handler.WorkflowHandler "            WorkflowHandler") that can be awaited for the final result or used to stream intermediate events.
You may pass either a concrete `start_event` instance or keyword arguments that will be used to construct the inferred [StartEvent](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.StartEvent "            StartEvent") subclass.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ctx`  |  `Context[](https://developers.llamaindex.ai/python/workflows-api-reference/context/#workflows.context.Context "            Context \(workflows.context.Context\)") | None`  |  Optional context to resume or share state across runs. If omitted, a fresh context is created.  |  `None`  |  
|  `start_event`  |  `StartEvent[](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.StartEvent "            StartEvent \(workflows.events.StartEvent\)") | None`  |  Optional explicit start event.  |  `None`  |  
|  `**kwargs`  |  Keyword args to initialize the start event when `start_event` is not provided.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `WorkflowHandler`  |   |  A future-like object to await the final result and  |  
|   |  stream events.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|   |  If validation fails and validation is enabled.  |  
|   |  If the start event cannot be created from kwargs.  |  
|  `WorkflowTimeoutError`  |  If execution exceeds the configured timeout.  |  
Examples:

```
# Create and run with kwargs
handler = MyFlow().run(topic="Pirates")

# Stream events
async for ev in handler.stream_events():
    ...

# Await final result
result = await handler

```

If you subclassed the start event, you can also directly pass it in:

```
result = await my_workflow.run(start_event=MyStartEvent(topic="Pirates"))

```

Source code in `workflows/workflow.py`  
| 
```
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
```
 | 
```
defrun(
    self,
    ctx: Context | None = None,
    start_event: StartEvent | None = None,
    **kwargs: Any,
) -> WorkflowHandler:
"""Run the workflow and return a handler for results and streaming.

    This schedules the workflow execution in the background and returns a
    [WorkflowHandler][workflows.handler.WorkflowHandler] that can be awaited
    for the final result or used to stream intermediate events.

    You may pass either a concrete `start_event` instance or keyword
    arguments that will be used to construct the inferred
    [StartEvent][workflows.events.StartEvent] subclass.

    Args:
        ctx (Context | None): Optional context to resume or share state
            across runs. If omitted, a fresh context is created.
        start_event (StartEvent | None): Optional explicit start event.
        **kwargs (Any): Keyword args to initialize the start event when
            `start_event` is not provided.

    Returns:
        WorkflowHandler: A future-like object to await the final result and
        stream events.

    Raises:
        WorkflowValidationError: If validation fails and validation is
            enabled.
        WorkflowRuntimeError: If the start event cannot be created from kwargs.
        WorkflowTimeoutError: If execution exceeds the configured timeout.

    Examples:
        ```python
        # Create and run with kwargs
        handler = MyFlow().run(topic="Pirates")

        # Stream events
        async for ev in handler.stream_events():


        # Await final result
        result = await handler
        ```

        If you subclassed the start event, you can also directly pass it in:

        ```python
        result = await my_workflow.run(start_event=MyStartEvent(topic="Pirates"))
        ```
    """
    fromworkflows.contextimport Context

    if not self._runtime_locked:
        # don't allow switching runtime after a workflow has been launched
        self._runtime_locked = True

    # Validate the workflow
    self._validate()

    # Extract run_id before passing remaining kwargs to start event
    run_id = kwargs.pop("run_id", None)

    # If a previous context is provided, pass its serialized form
    ctx = ctx if ctx is not None else Context(self)
    # TODO(v3) - remove dependency on is running for choosing whether to send a StartEvent.
    # Is not an easily synchronously queryable property.
    start_event_instance: StartEvent | None = (
        None
        if ctx.is_running
        else self._get_start_event_instance(start_event, **kwargs)
    )
    return ctx._workflow_run(
        workflow=self, start_event=start_event_instance, run_id=run_id
    )

```
 |  
| --- | --- |  
###  validate [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow/#workflows.workflow.Workflow.validate "Permanent link")

```
validate(*, validate_resource_configs:  = True, validate_resources:  = False) -> 

```

Validate the workflow to ensure it's well-formed.
This method validates the event graph and optionally validates resources: - Event production/consumption (set-based checks) - Graph structure: all steps reachable from an input event (StartEvent or HumanResponseEvent), and only output events (StopEvent, InputRequiredEvent) may be terminal - Resource configs (JSON files with Pydantic validation) are validated by default - Resource factories are not validated by default (may require env vars) - Circular resource dependencies are caught when validate_resources=True
Validation result is cached after the first successful run(); subsequent run() calls skip re-validation. Calling validate() explicitly always re-runs all checks.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `validate_resource_configs`  |  `bool`  |  If True (default), validate that resource config files exist and contain valid data for their Pydantic models.  |  `True`  |  
|  `validate_resources`  |  `bool`  |  If False (default), skip resolving resource factories during validation. Set to True to also validate that resource factories can be resolved and detect circular dependencies (may require environment variables or external connections).  |  `False`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `bool`  |  True if the workflow uses human-in-the-loop, False otherwise.  |  
Source code in `workflows/workflow.py`  
| 
```
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
```
 | 
```
defvalidate(
    self,
    *,
    validate_resource_configs: bool = True,
    validate_resources: bool = False,
) -> bool:
"""
    Validate the workflow to ensure it's well-formed.

    This method validates the event graph and optionally validates resources:
    - Event production/consumption (set-based checks)
    - Graph structure: all steps reachable from an input event (StartEvent or HumanResponseEvent),
      and only output events (StopEvent, InputRequiredEvent) may be terminal
    - Resource configs (JSON files with Pydantic validation) are validated by default
    - Resource factories are not validated by default (may require env vars)
    - Circular resource dependencies are caught when validate_resources=True

    Validation result is cached after the first successful run(); subsequent run() calls
    skip re-validation. Calling validate() explicitly always re-runs all checks.

    Args:
        validate_resource_configs: If True (default), validate that resource
            config files exist and contain valid data for their Pydantic models.
        validate_resources: If False (default), skip resolving resource factories
            during validation. Set to True to also validate that resource
            factories can be resolved and detect circular dependencies
            (may require environment variables or external connections).

    Returns:
        True if the workflow uses human-in-the-loop, False otherwise.
    """
    return self._validate(
        validate_resource_configs=validate_resource_configs,
        validate_resources=validate_resources,
        force=True,  # Explicit validate() call should always run
    )

```
 |  
| --- | --- |
