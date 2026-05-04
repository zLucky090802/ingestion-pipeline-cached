# Agent Classes[#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#agent-classes "Permanent link")
##  AgentContext [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.AgentContext "Permanent link")
Bases: `Protocol`
Minimal context interface for agent take_step implementations.
This protocol defines the subset of Context that agents actually use, allowing for both full workflow Context and lightweight alternatives.
Source code in `llama-index-core/llama_index/core/agent/workflow/agent_context.py`  
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
```
 | 
```
@runtime_checkable
classAgentContext(Protocol):
"""
    Minimal context interface for agent take_step implementations.

    This protocol defines the subset of Context that agents actually use,
    allowing for both full workflow Context and lightweight alternatives.
    """

    @property
    defstore(self) -> StateStore[Any]:
"""Access the key-value store for agent state."""
        ...

    @property
    defis_running(self) -> bool:
"""Check if the workflow is actively running (for event writing)."""
        ...

    defwrite_event_to_stream(self, event: Any) -> None:
"""Write an event to the output stream."""
        ...

```
 |  
| --- | --- |  
###  store `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.AgentContext.store "Permanent link")

```
store: StateStore[]

```

Access the key-value store for agent state.
###  is_running `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.AgentContext.is_running "Permanent link")

```
is_running: 

```

Check if the workflow is actively running (for event writing).
###  write_event_to_stream [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.AgentContext.write_event_to_stream "Permanent link")

```
write_event_to_stream(event: ) -> None

```

Write an event to the output stream.
Source code in `llama-index-core/llama_index/core/agent/workflow/agent_context.py`  
| 
```
34
35
36
```
 | 
```
defwrite_event_to_stream(self, event: Any) -> None:
"""Write an event to the output stream."""
    ...

```
 |  
| --- | --- |  
##  SimpleAgentContext `dataclass` [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.SimpleAgentContext "Permanent link")
Lightweight context for agents used outside workflows.
This implementation satisfies the AgentContext protocol with minimal overhead, suitable for use in `LLM.predict_and_call` and similar non-workflow scenarios where a full Context is not needed.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `store`  |  `InMemoryStateStore[DictState]`  |  `<workflows.context.state_store.InMemoryStateStore object at 0x7f00a8743a10>`  |  
|  `is_running`  |  `bool`  |  `False`  |  
Source code in `llama-index-core/llama_index/core/agent/workflow/agent_context.py`  
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
```
 | 
```
@dataclass(frozen=True)
classSimpleAgentContext:
"""
    Lightweight context for agents used outside workflows.

    This implementation satisfies the AgentContext protocol with minimal
    overhead, suitable for use in `LLM.predict_and_call` and similar
    non-workflow scenarios where a full Context is not needed.
    """

    store: InMemoryStateStore[DictState] = field(default_factory=_default_store)
    is_running: bool = False

    defwrite_event_to_stream(self, event: Any) -> None:
"""No-op - events are discarded in non-workflow usage."""

```
 |  
| --- | --- |  
###  write_event_to_stream [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.SimpleAgentContext.write_event_to_stream "Permanent link")

```
write_event_to_stream(event: ) -> None

```

No-op - events are discarded in non-workflow usage.
Source code in `llama-index-core/llama_index/core/agent/workflow/agent_context.py`  
| 
```
defwrite_event_to_stream(self, event: Any) -> None:
"""No-op - events are discarded in non-workflow usage."""

```
 |  
| --- |  
##  AgentWorkflow [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.AgentWorkflow "Permanent link")
Bases: `Workflow`, `PromptMixin`
A workflow for managing multiple agents with handoffs.
Source code in `llama-index-core/llama_index/core/agent/workflow/multi_agent_workflow.py`  
| 
```
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
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
870
871
872
873
874
875
876
877
878
879
880
881
882
883
884
885
886
887
888
```
 | 
```
classAgentWorkflow(Workflow, PromptMixin, metaclass=AgentWorkflowMeta):
"""A workflow for managing multiple agents with handoffs."""

    def__init__(
        self,
        agents: List[BaseWorkflowAgent],
        initial_state: Optional[Dict] = None,
        root_agent: Optional[str] = None,
        handoff_prompt: Optional[Union[str, BasePromptTemplate]] = None,
        handoff_output_prompt: Optional[Union[str, BasePromptTemplate]] = None,
        state_prompt: Optional[Union[str, BasePromptTemplate]] = None,
        timeout: Optional[float] = None,
        output_cls: Optional[Type[BaseModel]] = None,
        structured_output_fn: Optional[
            Callable[[List[ChatMessage]], Dict[str, Any]]
        ] = None,
        early_stopping_method: Literal["force", "generate"] = "force",
        **workflow_kwargs: Any,
    ):
        super().__init__(timeout=timeout, **workflow_kwargs)
        self.early_stopping_method = early_stopping_method
        if not agents:
            raise ValueError("At least one agent must be provided")

        # Raise an error if any agent has no name or no description
        if len(agents)  1 and any(
            agent.name == DEFAULT_AGENT_NAME for agent in agents
        ):
            raise ValueError("All agents must have a name in a multi-agent workflow")

        if len(agents)  1 and any(
            agent.description == DEFAULT_AGENT_DESCRIPTION for agent in agents
        ):
            raise ValueError(
                "All agents must have a description in a multi-agent workflow"
            )

        if any(agent.initial_state for agent in agents):
            raise ValueError(
                "Initial state is not supported per-agent in AgentWorkflow"
            )

        self.agents = {cfg.name: cfg for cfg in agents}
        if len(agents) == 1:
            root_agent = agents[0].name
        elif root_agent is None:
            raise ValueError("Exactly one root agent must be provided")
        else:
            root_agent = root_agent

        if root_agent not in self.agents:
            raise ValueError(f"Root agent {root_agent} not found in provided agents")

        self.root_agent = root_agent
        self.initial_state = initial_state or {}

        handoff_prompt = handoff_prompt or DEFAULT_HANDOFF_PROMPT
        if isinstance(handoff_prompt, str):
            handoff_prompt = PromptTemplate(handoff_prompt)
            if "{agent_info}" not in handoff_prompt.get_template():
                raise ValueError("Handoff prompt must contain {agent_info}")
        self.handoff_prompt = handoff_prompt

        handoff_output_prompt = handoff_output_prompt or DEFAULT_HANDOFF_OUTPUT_PROMPT
        if isinstance(handoff_output_prompt, str):
            handoff_output_prompt = PromptTemplate(handoff_output_prompt)
            if (
                "{to_agent}" not in handoff_output_prompt.get_template()
                or "{reason}" not in handoff_output_prompt.get_template()
            ):
                raise ValueError(
                    "Handoff output prompt must contain {to_agent} and {reason}"
                )
        self.handoff_output_prompt = handoff_output_prompt

        state_prompt = state_prompt or DEFAULT_STATE_PROMPT
        if isinstance(state_prompt, str):
            state_prompt = PromptTemplate(state_prompt)
            if (
                "{state}" not in state_prompt.get_template()
                or "{msg}" not in state_prompt.get_template()
            ):
                raise ValueError("State prompt must contain {state} and {msg}")
        self.state_prompt = state_prompt

        self.output_cls = output_cls
        self.structured_output_fn = structured_output_fn
        if output_cls is not None and structured_output_fn is not None:
            self.structured_output_fn = None

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {
            "handoff_prompt": self.handoff_prompt,
            "handoff_output_prompt": self.handoff_output_prompt,
            "state_prompt": self.state_prompt,
        }

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {agent.name: agent for agent in self.agents.values()}

    def_update_prompts(self, prompts_dict: PromptDictType) -> None:
"""Update prompts."""
        if "handoff_prompt" in prompts_dict:
            self.handoff_prompt = prompts_dict["handoff_prompt"]
        if "handoff_output_prompt" in prompts_dict:
            self.handoff_output_prompt = prompts_dict["handoff_output_prompt"]
        if "state_prompt" in prompts_dict:
            self.state_prompt = prompts_dict["state_prompt"]

    def_ensure_tools_are_async(
        self, tools: Sequence[BaseTool]
    ) -> Sequence[AsyncBaseTool]:
"""Ensure all tools are async."""
        return [adapt_to_async_tool(tool) for tool in tools]

    def_get_handoff_tool(
        self, current_agent: BaseWorkflowAgent
    ) -> Optional[AsyncBaseTool]:
"""Creates a handoff tool for the given agent."""
        # Do not create a handoff tool if there is only one agent
        if len(self.agents) == 1:
            return None

        agent_info = {cfg.name: cfg.description for cfg in self.agents.values()}

        # Filter out agents that the current agent cannot handoff to
        configs_to_remove = []
        for name in agent_info:
            if name == current_agent.name:
                configs_to_remove.append(name)
            elif (
                current_agent.can_handoff_to is not None
                and name not in current_agent.can_handoff_to
            ):
                configs_to_remove.append(name)

        for name in configs_to_remove:
            agent_info.pop(name)

        if not agent_info:
            return None

        fn_tool_prompt = self.handoff_prompt.format(agent_info=str(agent_info))
        return FunctionTool.from_defaults(
            async_fn=handoff, description=fn_tool_prompt, return_direct=True
        )

    async defget_tools(
        self, agent_name: str, input_str: Optional[str] = None
    ) -> Sequence[AsyncBaseTool]:
"""Get tools for the given agent."""
        agent_tools = self.agents[agent_name].tools or []
        tools = [*agent_tools]
        retriever = self.agents[agent_name].tool_retriever
        if retriever is not None:
            retrieved_tools = await retriever.aretrieve(input_str or "")
            tools.extend(retrieved_tools)

        if (
            self.agents[agent_name].can_handoff_to
            or self.agents[agent_name].can_handoff_to is None
        ):
            handoff_tool = self._get_handoff_tool(self.agents[agent_name])
            if handoff_tool:
                tools.append(handoff_tool)

        return self._ensure_tools_are_async(cast(List[BaseTool], tools))

    async def_init_context(self, ctx: Context, ev: StartEvent) -> None:
"""Initialize the context once, if needed."""
        if not await ctx.store.get("memory", default=None):
            default_memory = ev.get("memory", default=None)
            default_memory = default_memory or ChatMemoryBuffer.from_defaults(
                llm=self.agents[self.root_agent].llm or Settings.llm
            )
            await ctx.store.set("memory", default_memory)
        if not await ctx.store.get("agents", default=None):
            await ctx.store.set("agents", list(self.agents.keys()))
        if not await ctx.store.get("can_handoff_to", default=None):
            await ctx.store.set(
                "can_handoff_to",
                {
                    agent: agent_cfg.can_handoff_to
                    for agent, agent_cfg in self.agents.items()
                },
            )
        if not await ctx.store.get("state", default=None):
            await ctx.store.set("state", self.initial_state)
        if not await ctx.store.get("current_agent_name", default=None):
            await ctx.store.set("current_agent_name", self.root_agent)
        if not await ctx.store.get("handoff_output_prompt", default=None):
            await ctx.store.set(
                "handoff_output_prompt", self.handoff_output_prompt.get_template()
            )
        if not await ctx.store.get("max_iterations", default=None):
            max_iterations = (
                ev.get("max_iterations", default=None) or DEFAULT_MAX_ITERATIONS
            )
            await ctx.store.set("max_iterations", max_iterations)

        if not await ctx.store.get("early_stopping_method", default=None):
            early_stopping_method = (
                ev.get("early_stopping_method", default=None)
                or self.early_stopping_method
            )
            await ctx.store.set("early_stopping_method", early_stopping_method)

        # Reset the number of iterations
        await ctx.store.set("num_iterations", 0)

        # always set to false initially
        await ctx.store.set("formatted_input_with_state", False)

    async def_get_llm_response(
        self,
        ctx: Context,
        llm_input: List[ChatMessage],
        agent: BaseWorkflowAgent,
    ) -> "ChatResponse":
"""Get LLM response, respecting agent's streaming settings."""
        if agent.streaming:
            response_stream = await agent.llm.astream_chat(llm_input)
            last_response = None
            async for last_response in response_stream:
                raw = (
                    last_response.raw.model_dump()
                    if isinstance(last_response.raw, BaseModel)
                    else last_response.raw
                )
                if ctx.is_running:
                    ctx.write_event_to_stream(
                        AgentStream(
                            delta=last_response.delta or "",
                            response=last_response.message.content or "",
                            raw=raw,
                            current_agent_name=agent.name,
                            thinking_delta=last_response.additional_kwargs.get(
                                "thinking_delta", None
                            ),
                        )
                    )
            if last_response is None:
                raise ValueError("Got empty streaming response")
            return last_response
        else:
            return await agent.llm.achat(llm_input)

    async def_call_tool(
        self,
        ctx: Context,
        tool: AsyncBaseTool,
        tool_input: dict,
    ) -> ToolOutput:
"""Call the given tool with the given input."""
        try:
            if (
                isinstance(tool, FunctionTool)
                and tool.requires_context
                and tool.ctx_param_name is not None
            ):
                new_tool_input = {**tool_input}
                new_tool_input[tool.ctx_param_name] = ctx
                tool_output = await tool.acall(**new_tool_input)
            else:
                tool_output = await tool.acall(**tool_input)
        except Exception as e:
            event_exception = _get_waiting_for_event_exception()
            if event_exception and isinstance(e, event_exception):
                raise
            tool_output = ToolOutput(
                content=str(e),
                tool_name=tool.metadata.get_name(),
                raw_input=tool_input,
                raw_output=str(e),
                is_error=True,
                exception=e,
            )

        return tool_output

    @step
    async definit_run(self, ctx: Context, ev: AgentWorkflowStartEvent) -> AgentInput:
"""Sets up the workflow and validates inputs."""
        await self._init_context(ctx, ev)

        user_msg: Optional[Union[str, ChatMessage]] = ev.get("user_msg")
        chat_history: Optional[List[ChatMessage]] = ev.get("chat_history", [])

        # Convert string user_msg to ChatMessage
        if isinstance(user_msg, str):
            user_msg = ChatMessage(role="user", content=user_msg)

        # Add messages to memory
        memory: BaseMemory = await ctx.store.get("memory")

        # First set chat history if it exists
        if chat_history:
            await memory.aset(chat_history)

        # Then add user message if it exists
        if user_msg:
            await memory.aput(user_msg)
            content_str = "\n".join(
                [
                    block.text
                    for block in user_msg.blocks
                    if isinstance(block, TextBlock)
                ]
            )
            await ctx.store.set("user_msg_str", content_str)
        elif chat_history and not all(
            message.role == "system" for message in chat_history
        ):
            # If no user message, use the last message from chat history as user_msg_str
            user_hist: List[ChatMessage] = [
                msg for msg in chat_history if msg.role == "user"
            ]
            content_str = "\n".join(
                [
                    block.text
                    for block in user_hist[-1].blocks
                    if isinstance(block, TextBlock)
                ]
            )
            await ctx.store.set("user_msg_str", content_str)
        else:
            raise ValueError("Must provide either user_msg or chat_history")

        # Get all messages from memory
        input_messages = await memory.aget()

        # send to the current agent
        current_agent_name: str = await ctx.store.get("current_agent_name")
        return AgentInput(input=input_messages, current_agent_name=current_agent_name)

    @step
    async defsetup_agent(self, ctx: Context, ev: AgentInput) -> AgentSetup:
"""Main agent handling logic."""
        current_agent_name = ev.current_agent_name
        agent = self.agents[current_agent_name]
        llm_input = [*ev.input]

        if agent.system_prompt:
            llm_input = [
                ChatMessage(role="system", content=agent.system_prompt),
                *llm_input,
            ]

        state = await ctx.store.get("state", default=None)
        formatted_input_with_state = await ctx.store.get(
            "formatted_input_with_state", default=False
        )
        if state and not formatted_input_with_state:
            # update last message with current state
            for block in llm_input[-1].blocks[::-1]:
                if isinstance(block, TextBlock):
                    block.text = self.state_prompt.format(state=state, msg=block.text)
                    break
            await ctx.store.set("formatted_input_with_state", True)

        return AgentSetup(
            input=llm_input,
            current_agent_name=ev.current_agent_name,
        )

    @step
    async defrun_agent_step(self, ctx: Context, ev: AgentSetup) -> AgentOutput:
"""Run the agent."""
        memory: BaseMemory = await ctx.store.get("memory")
        agent = self.agents[ev.current_agent_name]
        user_msg_str = await ctx.store.get("user_msg_str")
        tools = await self.get_tools(ev.current_agent_name, user_msg_str or "")

        agent_output = await agent.take_step(
            ctx,
            ev.input,
            tools,
            memory,
        )

        ctx.write_event_to_stream(agent_output)
        return agent_output

    async def_generate_early_stopping_response(
        self, ctx: Context, ev: AgentOutput, max_iterations: int
    ) -> StopEvent:
"""Generate a final response when max iterations is reached with early_stopping_method='generate'."""
        memory: BaseMemory = await ctx.store.get("memory")
        agent = self.agents[ev.current_agent_name]
        messages = await memory.aget()

        early_stopping_prompt = DEFAULT_EARLY_STOPPING_PROMPT.format(
            max_iterations=max_iterations
        )

        llm_input = [*messages]
        if agent.system_prompt:
            llm_input = [
                ChatMessage(role="system", content=agent.system_prompt),
                *llm_input,
            ]
        llm_input.append(ChatMessage(role="system", content=early_stopping_prompt))

        response = await self._get_llm_response(ctx, llm_input, agent)
        await memory.aput(response.message)

        output = AgentOutput(
            response=response.message,
            tool_calls=[],
            raw=response.raw,
            current_agent_name=agent.name,
        )

        cur_tool_calls: List[ToolCallResult] = await ctx.store.get(
            "current_tool_calls", default=[]
        )
        output.tool_calls.extend(cur_tool_calls)  # type: ignore[arg-type]
        await ctx.store.set("current_tool_calls", [])

        ctx.write_event_to_stream(output)
        return StopEvent(result=output)

    @step
    async defparse_agent_output(
        self, ctx: Context, ev: AgentOutput
    ) -> Union[StopEvent, AgentInput, ToolCall, None]:
        max_iterations = await ctx.store.get(
            "max_iterations", default=DEFAULT_MAX_ITERATIONS
        )
        num_iterations = await ctx.store.get("num_iterations", default=0)
        num_iterations += 1
        await ctx.store.set("num_iterations", num_iterations)

        if num_iterations >= max_iterations:
            early_stopping_method = await ctx.store.get(
                "early_stopping_method", default="force"
            )
            if early_stopping_method == "generate":
                return await self._generate_early_stopping_response(
                    ctx, ev, max_iterations
                )
            else:
                raise WorkflowRuntimeError(
                    f"Max iterations of {max_iterations} reached! Either something went wrong, or you can "
                    "increase the max iterations with `.run(.., max_iterations=...)` "
                    "or use `early_stopping_method='generate'` to generate a final response instead."
                )

        memory: BaseMemory = await ctx.store.get("memory")

        if ev.retry_messages:
            # Retry with the given messages to let the LLM fix potential errors
            history = await memory.aget()
            user_msg_str = await ctx.store.get("user_msg_str")
            agent_name: str = await ctx.store.get("current_agent_name")

            return AgentInput(
                input=[
                    *history,
                    ChatMessage(role="user", content=user_msg_str),
                    *ev.retry_messages,
                ],
                current_agent_name=agent_name,
            )

        if not ev.tool_calls:
            agent = self.agents[ev.current_agent_name]
            memory = await ctx.store.get("memory")
            # important: messages should always be fetched after calling finalize, otherwise they do not contain the agent's response
            output = await agent.finalize(ctx, ev, memory)
            messages = await memory.aget()

            cur_tool_calls: List[ToolCallResult] = await ctx.store.get(
                "current_tool_calls", default=[]
            )
            output.tool_calls.extend(cur_tool_calls)  # type: ignore
            await ctx.store.set("current_tool_calls", [])

            if self.structured_output_fn is not None:
                try:
                    if inspect.iscoroutinefunction(self.structured_output_fn):
                        output.structured_response = await self.structured_output_fn(
                            messages
                        )
                    else:
                        output.structured_response = cast(
                            Dict[str, Any], self.structured_output_fn(messages)
                        )
                    ctx.write_event_to_stream(
                        AgentStreamStructuredOutput(output=output.structured_response)
                    )
                except Exception as e:
                    warnings.warn(
                        f"There was a problem with the generation of the structured output: {e}",
                        stacklevel=2,
                    )
            if self.output_cls is not None:
                try:
                    llm_input = [*messages]
                    if agent.system_prompt:
                        llm_input = [
                            ChatMessage(role="system", content=agent.system_prompt),
                            *llm_input,
                        ]
                    output.structured_response = await generate_structured_response(
                        messages=llm_input, llm=agent.llm, output_cls=self.output_cls
                    )
                    ctx.write_event_to_stream(
                        AgentStreamStructuredOutput(output=output.structured_response)
                    )
                except Exception as e:
                    warnings.warn(
                        f"There was a problem with the generation of the structured output: {e}",
                        stacklevel=2,
                    )

            return StopEvent(result=output)

        await ctx.store.set("num_tool_calls", len(ev.tool_calls))

        for tool_call in ev.tool_calls:
            ctx.send_event(
                ToolCall(
                    tool_name=tool_call.tool_name,
                    tool_kwargs=tool_call.tool_kwargs,
                    tool_id=tool_call.tool_id,
                )
            )

        return None

    @step
    async defcall_tool(self, ctx: Context, ev: ToolCall) -> ToolCallResult:
"""Calls the tool and handles the result."""
        ctx.write_event_to_stream(
            ToolCall(
                tool_name=ev.tool_name,
                tool_kwargs=ev.tool_kwargs,
                tool_id=ev.tool_id,
            )
        )

        current_agent_name = await ctx.store.get("current_agent_name")
        tools = await self.get_tools(current_agent_name, ev.tool_name)
        tools_by_name = {tool.metadata.name: tool for tool in tools}
        if ev.tool_name not in tools_by_name:
            tool = None
            result = ToolOutput(
                content=f"Tool {ev.tool_name} not found. Please select a tool that is available.",
                tool_name=ev.tool_name,
                raw_input=ev.tool_kwargs,
                raw_output=None,
                is_error=True,
            )
        else:
            tool = tools_by_name[ev.tool_name]
            result = await self._call_tool(ctx, tool, ev.tool_kwargs)

        result_ev = ToolCallResult(
            tool_name=ev.tool_name,
            tool_kwargs=ev.tool_kwargs,
            tool_id=ev.tool_id,
            tool_output=result,
            return_direct=tool.metadata.return_direct if tool else False,
        )

        ctx.write_event_to_stream(result_ev)
        return result_ev

    @step
    async defaggregate_tool_results(
        self, ctx: Context, ev: ToolCallResult
    ) -> Union[AgentInput, StopEvent, None]:
"""Aggregate tool results and return the next agent input."""
        num_tool_calls = await ctx.store.get("num_tool_calls", default=0)
        if num_tool_calls == 0:
            raise ValueError("No tool calls found, cannot aggregate results.")

        tool_call_results: list[ToolCallResult] = ctx.collect_events(  # type: ignore
            ev, expected=[ToolCallResult] * num_tool_calls
        )
        if not tool_call_results:
            return None

        memory: BaseMemory = await ctx.store.get("memory")
        agent_name: str = await ctx.store.get("current_agent_name")
        agent: BaseWorkflowAgent = self.agents[agent_name]

        # track tool calls made during a .run() call
        cur_tool_calls: List[ToolCallResult] = await ctx.store.get(
            "current_tool_calls", default=[]
        )
        cur_tool_calls.extend(tool_call_results)
        await ctx.store.set("current_tool_calls", cur_tool_calls)

        await agent.handle_tool_call_results(ctx, tool_call_results, memory)

        # set the next agent, if needed
        # the handoff tool sets this
        next_agent_name = await ctx.store.get("next_agent", default=None)
        if next_agent_name:
            await ctx.store.set("current_agent_name", next_agent_name)
            await ctx.store.set("next_agent", None)

        if any(
            tool_call_result.return_direct and not tool_call_result.tool_output.is_error
            for tool_call_result in tool_call_results
        ):
            # if any tool calls return directly and it's not an error tool call, take the first one
            return_direct_tool = next(
                tool_call_result
                for tool_call_result in tool_call_results
                if tool_call_result.return_direct
                and not tool_call_result.tool_output.is_error
            )

            # always finalize the agent, even if we're just handing off
            result = AgentOutput(
                response=ChatMessage(
                    role="assistant",
                    content=return_direct_tool.tool_output.content or "",
                ),
                tool_calls=[
                    ToolSelection(
                        tool_id=t.tool_id,
                        tool_name=t.tool_name,
                        tool_kwargs=t.tool_kwargs,
                    )
                    for t in cur_tool_calls
                ],
                raw=return_direct_tool.tool_output.raw_output,
                current_agent_name=agent.name,
            )
            result = await agent.finalize(ctx, result, memory)

            # we don't want to stop the system if we're just handing off
            if return_direct_tool.tool_name != "handoff":
                await ctx.store.set("current_tool_calls", [])
                return StopEvent(result=result)

        user_msg_str = await ctx.store.get("user_msg_str")
        input_messages = await memory.aget(input=user_msg_str)

        # get this again, in case it changed
        agent_name = await ctx.store.get("current_agent_name")
        agent = self.agents[agent_name]

        return AgentInput(input=input_messages, current_agent_name=agent.name)

    # TODO: Remove the deprecated agent-specific overload. The agent params
    # (user_msg, chat_history, memory, etc.) should be passed as kwargs that
    # flow through Workflow.run() → AgentWorkflowStartEvent construction
    # automatically, matching the standard Workflow.run(ctx, start_event,
    # **kwargs) signature. At that point this entire override can be deleted.

    @overload
    @deprecated(
        "Use the standard workflow signature instead: "
        "workflow.run(user_msg='hello') or "
        "workflow.run(ctx=ctx, start_event=event, user_msg='hello'). "
        "This positional signature will be removed in a future version.",
        category=None,
    )
    defrun(
        self,
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        memory: Optional[BaseMemory] = None,
        ctx: Optional[Context] = None,
        max_iterations: Optional[int] = None,
        early_stopping_method: Optional[Literal["force", "generate"]] = None,
        start_event: Optional[AgentWorkflowStartEvent] = None,
        **kwargs: Any,
    ) -> WorkflowHandler: ...

    @overload
    defrun(
        self,
        ctx: Optional[Context] = None,
        start_event: Optional[StartEvent] = None,
        **kwargs: Any,
    ) -> WorkflowHandler: ...

    defrun(self, *args: Any, **kwargs: Any) -> WorkflowHandler:
        user_msg: Optional[Union[str, ChatMessage]] = None
        chat_history: Optional[List[ChatMessage]] = None
        memory: Optional[BaseMemory] = None
        ctx: Optional[Context] = None
        start_event: Optional[StartEvent] = None

        if args:
            first = args[0]
            if isinstance(first, Context):
                ctx = first
                if len(args)  1 and isinstance(args[1], StartEvent):
                    start_event = args[1]
            else:
                user_msg = first
                if len(args)  1:
                    chat_history = args[1]
                if len(args)  2:
                    memory = args[2]
                if len(args)  3:
                    ctx = args[3]

        user_msg = kwargs.pop("user_msg", None) or user_msg
        chat_history = kwargs.pop("chat_history", None) or chat_history
        memory = kwargs.pop("memory", None) or memory
        ctx = kwargs.pop("ctx", None) or ctx
        max_iterations: Optional[int] = kwargs.pop("max_iterations", None)
        early_stopping_method: Optional[Literal["force", "generate"]] = kwargs.pop(
            "early_stopping_method", None
        )
        start_event = kwargs.pop("start_event", None) or start_event
        run_id = kwargs.pop("run_id", None)

        if ctx is not None and ctx.is_running:
            return super().run(
                ctx=ctx,
                run_id=run_id,
                **kwargs,
            )
        else:
            if start_event is None or isinstance(start_event, AgentWorkflowStartEvent):
                start_event = start_event or AgentWorkflowStartEvent(
                    user_msg=user_msg,
                    chat_history=chat_history,
                    memory=memory,
                    max_iterations=max_iterations,
                    early_stopping_method=early_stopping_method,
                    **kwargs,
                )
            return super().run(
                start_event=start_event,
                ctx=ctx,
                run_id=run_id,
            )

    @classmethod
    deffrom_tools_or_functions(
        cls,
        tools_or_functions: List[Union[BaseTool, Callable]],
        llm: Optional[LLM] = None,
        system_prompt: Optional[str] = None,
        state_prompt: Optional[Union[str, BasePromptTemplate]] = None,
        initial_state: Optional[dict] = None,
        output_cls: Optional[Type[BaseModel]] = None,
        structured_output_fn: Optional[
            Callable[[List[ChatMessage]], Dict[str, Any]]
        ] = None,
        timeout: Optional[float] = None,
        verbose: bool = False,
    ) -> "AgentWorkflow":
"""
        Initializes an AgentWorkflow from a list of tools or functions.

        The workflow will be initialized with a single agent that uses the provided tools or functions.

        If the LLM is a function calling model, the workflow will use the FunctionAgent.
        Otherwise, it will use the ReActAgent.
        """
        llm = llm or Settings.llm
        agent_cls = (
            FunctionAgent if llm.metadata.is_function_calling_model else ReActAgent
        )

        tools = [
            FunctionTool.from_defaults(fn=tool)
            if not isinstance(tool, BaseTool)
            else tool
            for tool in tools_or_functions
        ]
        return cls(
            agents=[
                agent_cls(
                    name="Agent",
                    description="A single agent that uses the provided tools or functions.",
                    tools=tools,
                    llm=llm,
                    system_prompt=system_prompt,
                )
            ],
            output_cls=output_cls,
            structured_output_fn=structured_output_fn,
            state_prompt=state_prompt,
            initial_state=initial_state,
            timeout=timeout,
            verbose=verbose,
        )

```
 |  
| --- | --- |  
###  get_tools [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.AgentWorkflow.get_tools "Permanent link")

```
get_tools(
    agent_name: , input_str: Optional[] = None
) -> Sequence[]

```

Get tools for the given agent.
Source code in `llama-index-core/llama_index/core/agent/workflow/multi_agent_workflow.py`  
| 
```
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
```
 | 
```
async defget_tools(
    self, agent_name: str, input_str: Optional[str] = None
) -> Sequence[AsyncBaseTool]:
"""Get tools for the given agent."""
    agent_tools = self.agents[agent_name].tools or []
    tools = [*agent_tools]
    retriever = self.agents[agent_name].tool_retriever
    if retriever is not None:
        retrieved_tools = await retriever.aretrieve(input_str or "")
        tools.extend(retrieved_tools)

    if (
        self.agents[agent_name].can_handoff_to
        or self.agents[agent_name].can_handoff_to is None
    ):
        handoff_tool = self._get_handoff_tool(self.agents[agent_name])
        if handoff_tool:
            tools.append(handoff_tool)

    return self._ensure_tools_are_async(cast(List[BaseTool], tools))

```
 |  
| --- | --- |  
###  init_run [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.AgentWorkflow.init_run "Permanent link")

```
init_run(
    ctx: Context, ev: AgentWorkflowStartEvent
) -> 

```

Sets up the workflow and validates inputs.
Source code in `llama-index-core/llama_index/core/agent/workflow/multi_agent_workflow.py`  
| 
```
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
@step
async definit_run(self, ctx: Context, ev: AgentWorkflowStartEvent) -> AgentInput:
"""Sets up the workflow and validates inputs."""
    await self._init_context(ctx, ev)

    user_msg: Optional[Union[str, ChatMessage]] = ev.get("user_msg")
    chat_history: Optional[List[ChatMessage]] = ev.get("chat_history", [])

    # Convert string user_msg to ChatMessage
    if isinstance(user_msg, str):
        user_msg = ChatMessage(role="user", content=user_msg)

    # Add messages to memory
    memory: BaseMemory = await ctx.store.get("memory")

    # First set chat history if it exists
    if chat_history:
        await memory.aset(chat_history)

    # Then add user message if it exists
    if user_msg:
        await memory.aput(user_msg)
        content_str = "\n".join(
            [
                block.text
                for block in user_msg.blocks
                if isinstance(block, TextBlock)
            ]
        )
        await ctx.store.set("user_msg_str", content_str)
    elif chat_history and not all(
        message.role == "system" for message in chat_history
    ):
        # If no user message, use the last message from chat history as user_msg_str
        user_hist: List[ChatMessage] = [
            msg for msg in chat_history if msg.role == "user"
        ]
        content_str = "\n".join(
            [
                block.text
                for block in user_hist[-1].blocks
                if isinstance(block, TextBlock)
            ]
        )
        await ctx.store.set("user_msg_str", content_str)
    else:
        raise ValueError("Must provide either user_msg or chat_history")

    # Get all messages from memory
    input_messages = await memory.aget()

    # send to the current agent
    current_agent_name: str = await ctx.store.get("current_agent_name")
    return AgentInput(input=input_messages, current_agent_name=current_agent_name)

```
 |  
| --- | --- |  
###  setup_agent [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.AgentWorkflow.setup_agent "Permanent link")

```
setup_agent(ctx: Context, ev: ) -> 

```

Main agent handling logic.
Source code in `llama-index-core/llama_index/core/agent/workflow/multi_agent_workflow.py`  
| 
```
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
```
 | 
```
@step
async defsetup_agent(self, ctx: Context, ev: AgentInput) -> AgentSetup:
"""Main agent handling logic."""
    current_agent_name = ev.current_agent_name
    agent = self.agents[current_agent_name]
    llm_input = [*ev.input]

    if agent.system_prompt:
        llm_input = [
            ChatMessage(role="system", content=agent.system_prompt),
            *llm_input,
        ]

    state = await ctx.store.get("state", default=None)
    formatted_input_with_state = await ctx.store.get(
        "formatted_input_with_state", default=False
    )
    if state and not formatted_input_with_state:
        # update last message with current state
        for block in llm_input[-1].blocks[::-1]:
            if isinstance(block, TextBlock):
                block.text = self.state_prompt.format(state=state, msg=block.text)
                break
        await ctx.store.set("formatted_input_with_state", True)

    return AgentSetup(
        input=llm_input,
        current_agent_name=ev.current_agent_name,
    )

```
 |  
| --- | --- |  
###  run_agent_step [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.AgentWorkflow.run_agent_step "Permanent link")

```
run_agent_step(ctx: Context, ev: ) -> 

```

Run the agent.
Source code in `llama-index-core/llama_index/core/agent/workflow/multi_agent_workflow.py`  
| 
```
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
```
 | 
```
@step
async defrun_agent_step(self, ctx: Context, ev: AgentSetup) -> AgentOutput:
"""Run the agent."""
    memory: BaseMemory = await ctx.store.get("memory")
    agent = self.agents[ev.current_agent_name]
    user_msg_str = await ctx.store.get("user_msg_str")
    tools = await self.get_tools(ev.current_agent_name, user_msg_str or "")

    agent_output = await agent.take_step(
        ctx,
        ev.input,
        tools,
        memory,
    )

    ctx.write_event_to_stream(agent_output)
    return agent_output

```
 |  
| --- | --- |  
###  call_tool [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.AgentWorkflow.call_tool "Permanent link")

```
call_tool(ctx: Context, ev: ) -> 

```

Calls the tool and handles the result.
Source code in `llama-index-core/llama_index/core/agent/workflow/multi_agent_workflow.py`  
| 
```
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
```
 | 
```
@step
async defcall_tool(self, ctx: Context, ev: ToolCall) -> ToolCallResult:
"""Calls the tool and handles the result."""
    ctx.write_event_to_stream(
        ToolCall(
            tool_name=ev.tool_name,
            tool_kwargs=ev.tool_kwargs,
            tool_id=ev.tool_id,
        )
    )

    current_agent_name = await ctx.store.get("current_agent_name")
    tools = await self.get_tools(current_agent_name, ev.tool_name)
    tools_by_name = {tool.metadata.name: tool for tool in tools}
    if ev.tool_name not in tools_by_name:
        tool = None
        result = ToolOutput(
            content=f"Tool {ev.tool_name} not found. Please select a tool that is available.",
            tool_name=ev.tool_name,
            raw_input=ev.tool_kwargs,
            raw_output=None,
            is_error=True,
        )
    else:
        tool = tools_by_name[ev.tool_name]
        result = await self._call_tool(ctx, tool, ev.tool_kwargs)

    result_ev = ToolCallResult(
        tool_name=ev.tool_name,
        tool_kwargs=ev.tool_kwargs,
        tool_id=ev.tool_id,
        tool_output=result,
        return_direct=tool.metadata.return_direct if tool else False,
    )

    ctx.write_event_to_stream(result_ev)
    return result_ev

```
 |  
| --- | --- |  
###  aggregate_tool_results [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.AgentWorkflow.aggregate_tool_results "Permanent link")

```
aggregate_tool_results(
    ctx: Context, ev: 
) -> Union[, StopEvent, None]

```

Aggregate tool results and return the next agent input.
Source code in `llama-index-core/llama_index/core/agent/workflow/multi_agent_workflow.py`  
| 
```
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
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
```
 | 
```
@step
async defaggregate_tool_results(
    self, ctx: Context, ev: ToolCallResult
) -> Union[AgentInput, StopEvent, None]:
"""Aggregate tool results and return the next agent input."""
    num_tool_calls = await ctx.store.get("num_tool_calls", default=0)
    if num_tool_calls == 0:
        raise ValueError("No tool calls found, cannot aggregate results.")

    tool_call_results: list[ToolCallResult] = ctx.collect_events(  # type: ignore
        ev, expected=[ToolCallResult] * num_tool_calls
    )
    if not tool_call_results:
        return None

    memory: BaseMemory = await ctx.store.get("memory")
    agent_name: str = await ctx.store.get("current_agent_name")
    agent: BaseWorkflowAgent = self.agents[agent_name]

    # track tool calls made during a .run() call
    cur_tool_calls: List[ToolCallResult] = await ctx.store.get(
        "current_tool_calls", default=[]
    )
    cur_tool_calls.extend(tool_call_results)
    await ctx.store.set("current_tool_calls", cur_tool_calls)

    await agent.handle_tool_call_results(ctx, tool_call_results, memory)

    # set the next agent, if needed
    # the handoff tool sets this
    next_agent_name = await ctx.store.get("next_agent", default=None)
    if next_agent_name:
        await ctx.store.set("current_agent_name", next_agent_name)
        await ctx.store.set("next_agent", None)

    if any(
        tool_call_result.return_direct and not tool_call_result.tool_output.is_error
        for tool_call_result in tool_call_results
    ):
        # if any tool calls return directly and it's not an error tool call, take the first one
        return_direct_tool = next(
            tool_call_result
            for tool_call_result in tool_call_results
            if tool_call_result.return_direct
            and not tool_call_result.tool_output.is_error
        )

        # always finalize the agent, even if we're just handing off
        result = AgentOutput(
            response=ChatMessage(
                role="assistant",
                content=return_direct_tool.tool_output.content or "",
            ),
            tool_calls=[
                ToolSelection(
                    tool_id=t.tool_id,
                    tool_name=t.tool_name,
                    tool_kwargs=t.tool_kwargs,
                )
                for t in cur_tool_calls
            ],
            raw=return_direct_tool.tool_output.raw_output,
            current_agent_name=agent.name,
        )
        result = await agent.finalize(ctx, result, memory)

        # we don't want to stop the system if we're just handing off
        if return_direct_tool.tool_name != "handoff":
            await ctx.store.set("current_tool_calls", [])
            return StopEvent(result=result)

    user_msg_str = await ctx.store.get("user_msg_str")
    input_messages = await memory.aget(input=user_msg_str)

    # get this again, in case it changed
    agent_name = await ctx.store.get("current_agent_name")
    agent = self.agents[agent_name]

    return AgentInput(input=input_messages, current_agent_name=agent.name)

```
 |  
| --- | --- |  
###  from_tools_or_functions `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.AgentWorkflow.from_tools_or_functions "Permanent link")

```
from_tools_or_functions(
    tools_or_functions: [Union[, Callable]],
    llm: Optional[] = None,
    system_prompt: Optional[] = None,
    state_prompt: Optional[
        Union[, ]
    ] = None,
    initial_state: Optional[] = None,
    output_cls: Optional[[BaseModel]] = None,
    structured_output_fn: Optional[
        Callable[[[]], [, ]]
    ] = None,
    timeout: Optional[float] = None,
    verbose:  = False,
) -> 

```

Initializes an AgentWorkflow from a list of tools or functions.
The workflow will be initialized with a single agent that uses the provided tools or functions.
If the LLM is a function calling model, the workflow will use the FunctionAgent. Otherwise, it will use the ReActAgent.
Source code in `llama-index-core/llama_index/core/agent/workflow/multi_agent_workflow.py`  
| 
```
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
870
871
872
873
874
875
876
877
878
879
880
881
882
883
884
885
886
887
888
```
 | 
```
@classmethod
deffrom_tools_or_functions(
    cls,
    tools_or_functions: List[Union[BaseTool, Callable]],
    llm: Optional[LLM] = None,
    system_prompt: Optional[str] = None,
    state_prompt: Optional[Union[str, BasePromptTemplate]] = None,
    initial_state: Optional[dict] = None,
    output_cls: Optional[Type[BaseModel]] = None,
    structured_output_fn: Optional[
        Callable[[List[ChatMessage]], Dict[str, Any]]
    ] = None,
    timeout: Optional[float] = None,
    verbose: bool = False,
) -> "AgentWorkflow":
"""
    Initializes an AgentWorkflow from a list of tools or functions.

    The workflow will be initialized with a single agent that uses the provided tools or functions.

    If the LLM is a function calling model, the workflow will use the FunctionAgent.
    Otherwise, it will use the ReActAgent.
    """
    llm = llm or Settings.llm
    agent_cls = (
        FunctionAgent if llm.metadata.is_function_calling_model else ReActAgent
    )

    tools = [
        FunctionTool.from_defaults(fn=tool)
        if not isinstance(tool, BaseTool)
        else tool
        for tool in tools_or_functions
    ]
    return cls(
        agents=[
            agent_cls(
                name="Agent",
                description="A single agent that uses the provided tools or functions.",
                tools=tools,
                llm=llm,
                system_prompt=system_prompt,
            )
        ],
        output_cls=output_cls,
        structured_output_fn=structured_output_fn,
        state_prompt=state_prompt,
        initial_state=initial_state,
        timeout=timeout,
        verbose=verbose,
    )

```
 |  
| --- | --- |  
##  BaseWorkflowAgent [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.BaseWorkflowAgent "Permanent link")
Bases: `Workflow`, `BaseModel`, `PromptMixin`
Base class for all agents, combining config and logic.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `name`  |  The name of the agent  |  `'Agent'`  |  
|  `description`  |  The description of what the agent does and is responsible for  |  `'An agent that can perform a task'`  |  
|  `system_prompt`  |  `str | None`  |  The system prompt for the agent  |  `None`  |  
|  `tools`  |  `List[BaseTool[](https://developers.llamaindex.ai/python/framework-api-reference/tools/#llama_index.core.tools.types.BaseTool "BaseTool \(llama_index.core.tools.BaseTool\)") | Callable] | None`  |  The tools that the agent can use  |  `None`  |  
|  `tool_retriever`  |  `ObjectRetriever[](https://developers.llamaindex.ai/python/framework-api-reference/objects/#llama_index.core.objects.ObjectRetriever "ObjectRetriever \(llama_index.core.objects.ObjectRetriever\)") | None`  |  The tool retriever for the agent, can be provided instead of tools  |  `None`  |  
|  `can_handoff_to`  |  `List[str] | None`  |  The agent names that this agent can hand off to  |  `None`  |  
|  `llm`  |  The LLM that the agent uses  |  `<dynamic>`  |  
|  `initial_state`  |  `Dict[str, Any]`  |  The initial state of the agent, can be used by accessed under `await ctx.store.get('state')`  |  `<class 'dict'>`  |  
|  `state_prompt`  |   |  The prompt to use to update the state of the agent  |  `'Current state:\n{state}\n\nCurrent message:\n{msg}\n'`  |  
|  `output_cls`  |  `Type[BaseModel] | None`  |  Output class for the agent. If you set this field to a non-null value, `structured_output_fn` will be ignored.  |  `None`  |  
|  `structured_output_fn`  |  `Callable[list, Dict[str, Any]] | None`  |  Custom function to generate structured output from the agent's run. It has to take a list of ChatMessage instances (derived from the memory) and output a BaseModel subclass instance. If you set `output_cls` to a non-null value, this field will be ignored.  |  `None`  |  
|  `streaming`  |  `bool`  |  Whether to stream the agent's output to the event stream. Useful for long-running agents, but not every LLM will support streaming.  |  `True`  |  
|  `early_stopping_method`  |  `Literal['force', 'generate']`  |  Method to handle max iterations. 'force' raises an error (default). 'generate' makes one final LLM call to generate a response.  |  `'force'`  |  
Source code in `llama-index-core/llama_index/core/agent/workflow/base_agent.py`  
| 
```
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
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
```
 | 
```
classBaseWorkflowAgent(
    Workflow, BaseModel, PromptMixin, metaclass=BaseWorkflowAgentMeta
):
"""Base class for all agents, combining config and logic."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(default=DEFAULT_AGENT_NAME, description="The name of the agent")
    description: str = Field(
        default=DEFAULT_AGENT_DESCRIPTION,
        description="The description of what the agent does and is responsible for",
    )
    system_prompt: Optional[str] = Field(
        default=None, description="The system prompt for the agent"
    )
    tools: Optional[List[Union[BaseTool, Callable]]] = Field(
        default=None, description="The tools that the agent can use"
    )
    tool_retriever: Optional[ObjectRetriever] = Field(
        default=None,
        description="The tool retriever for the agent, can be provided instead of tools",
    )
    can_handoff_to: Optional[List[str]] = Field(
        default=None, description="The agent names that this agent can hand off to"
    )
    llm: LLM = Field(
        default_factory=get_default_llm, description="The LLM that the agent uses"
    )
    initial_state: Dict[str, Any] = Field(
        default_factory=dict,
        description="The initial state of the agent, can be used by accessed under `await ctx.store.get('state')`",
    )
    state_prompt: Union[str, BasePromptTemplate] = Field(
        default=DEFAULT_STATE_PROMPT,
        description="The prompt to use to update the state of the agent",
        validate_default=True,
    )
    output_cls: Optional[Type[BaseModel]] = Field(
        description="Output class for the agent. If you set this field to a non-null value, `structured_output_fn` will be ignored.",
        default=None,
        exclude=True,
    )
    structured_output_fn: Optional[Callable[[List[ChatMessage]], Dict[str, Any]]] = (
        Field(
            description="Custom function to generate structured output from the agent's run. It has to take a list of ChatMessage instances (derived from the memory) and output a BaseModel subclass instance. If you set `output_cls` to a non-null value, this field will be ignored.",
            default=None,
        )
    )
    streaming: bool = Field(
        default=True,
        description="Whether to stream the agent's output to the event stream. Useful for long-running agents, but not every LLM will support streaming.",
    )
    early_stopping_method: Literal["force", "generate"] = Field(
        default="force",
        description="Method to handle max iterations. 'force' raises an error (default). 'generate' makes one final LLM call to generate a response.",
    )

    def__init__(
        self,
        name: str = DEFAULT_AGENT_NAME,
        description: str = DEFAULT_AGENT_DESCRIPTION,
        system_prompt: Optional[str] = None,
        tools: Optional[List[Union[BaseTool, Callable]]] = None,
        tool_retriever: Optional[ObjectRetriever] = None,
        can_handoff_to: Optional[List[str]] = None,
        llm: Optional[LLM] = None,
        initial_state: Optional[Dict[str, Any]] = None,
        state_prompt: Optional[Union[str, BasePromptTemplate]] = None,
        output_cls: Optional[Type[BaseModel]] = None,
        structured_output_fn: Optional[Callable[[List[ChatMessage]], BaseModel]] = None,
        streaming: bool = True,
        early_stopping_method: Literal["force", "generate"] = "force",
        timeout: Optional[float] = None,
        verbose: bool = False,
        **kwargs: Any,
    ):
        # Filter out workflow-specific kwargs
        workflow_kwargs = {k: v for k, v in kwargs.items() if k in WORKFLOW_KWARGS}
        model_kwargs = {k: v for k, v in kwargs.items() if k not in WORKFLOW_KWARGS}

        # Initialize BaseModel with the Pydantic fields
        if isinstance(state_prompt, str):
            state_prompt = PromptTemplate(state_prompt)
        elif state_prompt is None:
            state_prompt = DEFAULT_STATE_PROMPT

        if output_cls is not None and structured_output_fn is not None:
            structured_output_fn = None

        BaseModel.__init__(
            self,
            name=name,
            description=description,
            system_prompt=system_prompt,
            tools=tools,
            tool_retriever=tool_retriever,
            can_handoff_to=can_handoff_to,
            llm=llm or get_default_llm(),
            initial_state=initial_state or {},
            state_prompt=state_prompt,
            output_cls=output_cls,
            structured_output_fn=structured_output_fn,
            streaming=streaming,
            early_stopping_method=early_stopping_method,
            **model_kwargs,
        )

        # Initialize Workflow with workflow-specific parameters
        Workflow.__init__(self, timeout=timeout, verbose=verbose, **workflow_kwargs)

    defvalidate(self, **kwargs: Any) -> bool:  # type: ignore[override]
"""
        Validate the workflow to ensure it's well-formed.

        Explicitly delegates to Workflow.validate to resolve the method conflict
        between Workflow.validate (instance method) and BaseModel.validate (classmethod).
        """
        return Workflow.validate(self, **kwargs)

    @field_validator("tools", mode="before")
    defvalidate_tools(
        cls, v: Optional[Sequence[Union[BaseTool, Callable]]]
    ) -> Optional[Sequence[BaseTool]]:
"""
        Validate tools.

        If tools are not of type BaseTool, they will be converted to FunctionTools.
        This assumes the inputs are tools or callable functions.
        """
        if v is None:
            return None

        validated_tools: List[BaseTool] = []
        for tool in v:
            if not isinstance(tool, BaseTool):
                validated_tools.append(FunctionTool.from_defaults(tool))
            else:
                validated_tools.append(tool)

        for tool in validated_tools:
            if tool.metadata.name == "handoff":
                raise ValueError(
                    "'handoff' is a reserved tool name. Please use a different name."
                )

        return validated_tools  # type: ignore[return-value]

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {}

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt sub-modules."""
        return {}

    def_update_prompts(self, prompts_dict: PromptDictType) -> None:
"""Update prompts."""

    @abstractmethod
    async deftake_step(
        self,
        ctx: AgentContext,
        llm_input: List[ChatMessage],
        tools: Sequence[AsyncBaseTool],
        memory: BaseMemory,
    ) -> AgentOutput:
"""Take a single step with the agent."""

    @abstractmethod
    async defhandle_tool_call_results(
        self, ctx: Context, results: List[ToolCallResult], memory: BaseMemory
    ) -> None:
"""Handle tool call results."""

    @abstractmethod
    async deffinalize(
        self, ctx: Context, output: AgentOutput, memory: BaseMemory
    ) -> AgentOutput:
"""Finalize the agent's execution."""

    def_ensure_tools_are_async(
        self, tools: Sequence[BaseTool]
    ) -> Sequence[AsyncBaseTool]:
"""Ensure all tools are async."""
        return [adapt_to_async_tool(tool) for tool in tools]

    async defget_tools(
        self, input_str: Optional[str] = None
    ) -> Sequence[AsyncBaseTool]:
"""Get tools for the given agent."""
        tools = [*self.tools] if self.tools else []
        if self.tool_retriever is not None:
            retrieved_tools = await self.tool_retriever.aretrieve(input_str or "")
            tools.extend(retrieved_tools)

        return self._ensure_tools_are_async(cast(List[BaseTool], tools))

    async def_init_context(self, ctx: Context, ev: AgentWorkflowStartEvent) -> None:
"""Initialize the context once, if needed."""
        if not await ctx.store.get("memory", default=None):
            default_memory = ev.get("memory", default=None)
            default_memory = default_memory or ChatMemoryBuffer.from_defaults(
                llm=self.llm or Settings.llm
            )
            await ctx.store.set("memory", default_memory)
        if not await ctx.store.get("state", default=None):
            await ctx.store.set("state", self.initial_state.copy())

        if not await ctx.store.get("max_iterations", default=None):
            max_iterations = (
                ev.get("max_iterations", default=None) or DEFAULT_MAX_ITERATIONS
            )
            await ctx.store.set("max_iterations", max_iterations)

        if not await ctx.store.get("early_stopping_method", default=None):
            early_stopping_method = (
                ev.get("early_stopping_method", default=None)
                or self.early_stopping_method
            )
            await ctx.store.set("early_stopping_method", early_stopping_method)

        # Reset the number of iterations
        await ctx.store.set("num_iterations", 0)

        # always set to false initially
        await ctx.store.set("formatted_input_with_state", False)

    async def_get_llm_response(
        self, ctx: Context, llm_input: List[ChatMessage], llm: Optional[LLM] = None
    ) -> ChatResponse:
"""Get LLM response, respecting streaming settings."""
        target_llm = llm or self.llm

        if self.streaming:
            response_stream = await target_llm.astream_chat(llm_input)
            last_response = None
            async for last_response in response_stream:
                raw = (
                    last_response.raw.model_dump()
                    if isinstance(last_response.raw, BaseModel)
                    else last_response.raw
                )
                if ctx.is_running:
                    ctx.write_event_to_stream(
                        AgentStream(
                            delta=last_response.delta or "",
                            response=last_response.message.content or "",
                            raw=raw,
                            current_agent_name=self.name,
                            thinking_delta=last_response.additional_kwargs.get(
                                "thinking_delta", None
                            ),
                        )
                    )
            if last_response is None:
                raise ValueError("Got empty streaming response")
            return last_response
        else:
            return await target_llm.achat(llm_input)

    async def_call_tool(
        self,
        ctx: Context,
        tool: AsyncBaseTool,
        tool_input: dict,
    ) -> ToolOutput:
"""Call the given tool with the given input."""
        try:
            if (
                isinstance(tool, FunctionTool)
                and tool.requires_context
                and tool.ctx_param_name is not None
            ):
                new_tool_input = {**tool_input}
                new_tool_input[tool.ctx_param_name] = ctx
                tool_output = await tool.acall(**new_tool_input)
            else:
                tool_output = await tool.acall(**tool_input)
        except Exception as e:
            # raise to wait
            waiting_for_event_exception = _get_waiting_for_event_exception()
            if waiting_for_event_exception and isinstance(
                e, waiting_for_event_exception
            ):
                raise
            tool_output = ToolOutput(
                content=str(e),
                tool_name=tool.metadata.get_name(),
                raw_input=tool_input,
                raw_output=str(e),
                is_error=True,
                exception=e,
            )

        return tool_output

    @step
    async definit_run(self, ctx: Context, ev: AgentWorkflowStartEvent) -> AgentInput:
"""Sets up the workflow and validates inputs."""
        await self._init_context(ctx, ev)

        user_msg: Optional[Union[str, ChatMessage]] = ev.get("user_msg")
        chat_history: Optional[List[ChatMessage]] = ev.get("chat_history", [])

        # Convert string user_msg to ChatMessage
        if isinstance(user_msg, str):
            user_msg = ChatMessage(role="user", content=user_msg)

        # Add messages to memory
        memory: BaseMemory = await ctx.store.get("memory")

        # First set chat history if it exists
        if chat_history:
            await memory.aset(chat_history)

        # Then add user message if it exists
        if user_msg:
            await memory.aput(user_msg)
            content_str = "\n".join(
                [
                    block.text
                    for block in user_msg.blocks
                    if isinstance(block, TextBlock)
                ]
            )
            await ctx.store.set("user_msg_str", content_str)
        elif chat_history and not all(
            message.role == "system" for message in chat_history
        ):
            # If no user message, use the last message from chat history as user_msg_str
            user_hist: List[ChatMessage] = [
                msg for msg in chat_history if msg.role == "user"
            ]
            content_str = "\n".join(
                [
                    block.text
                    for block in user_hist[-1].blocks
                    if isinstance(block, TextBlock)
                ]
            )
            await ctx.store.set("user_msg_str", content_str)
        else:
            raise ValueError("Must provide either user_msg or chat_history")

        # Get all messages from memory
        input_messages = await memory.aget()

        # send to the current agent
        return AgentInput(input=input_messages, current_agent_name=self.name)

    @step
    async defsetup_agent(self, ctx: Context, ev: AgentInput) -> AgentSetup:
"""Main agent handling logic."""
        llm_input = [*ev.input]

        if self.system_prompt:
            llm_input = [
                ChatMessage(role="system", content=self.system_prompt),
                *llm_input,
            ]

        state = await ctx.store.get("state", default=None)
        formatted_input_with_state = await ctx.store.get(
            "formatted_input_with_state", default=False
        )
        if state and not formatted_input_with_state:
            # update last message with current state
            for block in llm_input[-1].blocks[::-1]:
                if isinstance(block, TextBlock):
                    block.text = self.state_prompt.format(state=state, msg=block.text)
                    break
            await ctx.store.set("formatted_input_with_state", True)

        return AgentSetup(
            input=llm_input,
            current_agent_name=ev.current_agent_name,
        )

    @step
    async defrun_agent_step(self, ctx: Context, ev: AgentSetup) -> AgentOutput:
"""Run the agent."""
        memory: BaseMemory = await ctx.store.get("memory")
        user_msg_str = await ctx.store.get("user_msg_str")
        tools = await self.get_tools(user_msg_str or "")

        agent_output = await self.take_step(
            ctx,
            ev.input,
            tools,
            memory,
        )

        ctx.write_event_to_stream(agent_output)
        return agent_output

    async def_generate_early_stopping_response(
        self, ctx: Context, max_iterations: int
    ) -> StopEvent:
"""Generate a final response when max iterations is reached with early_stopping_method='generate'."""
        memory: BaseMemory = await ctx.store.get("memory")
        messages = await memory.aget()

        early_stopping_prompt = DEFAULT_EARLY_STOPPING_PROMPT.format(
            max_iterations=max_iterations
        )

        llm_input = [*messages]
        if self.system_prompt:
            llm_input = [
                ChatMessage(role="system", content=self.system_prompt),
                *llm_input,
            ]
        llm_input.append(ChatMessage(role="system", content=early_stopping_prompt))

        response = await self._get_llm_response(ctx, llm_input)
        await memory.aput(response.message)

        output = AgentOutput(
            response=response.message,
            tool_calls=[],
            raw=response.raw,
            current_agent_name=self.name,
        )

        cur_tool_calls: List[ToolCallResult] = await ctx.store.get(
            "current_tool_calls", default=[]
        )
        output.tool_calls.extend(cur_tool_calls)  # type: ignore[arg-type]
        await ctx.store.set("current_tool_calls", [])

        ctx.write_event_to_stream(output)
        return StopEvent(result=output)

    @step
    async defparse_agent_output(
        self, ctx: Context, ev: AgentOutput
    ) -> Union[StopEvent, AgentInput, ToolCall, None]:
        max_iterations = await ctx.store.get(
            "max_iterations", default=DEFAULT_MAX_ITERATIONS
        )
        num_iterations = await ctx.store.get("num_iterations", default=0)
        num_iterations += 1
        await ctx.store.set("num_iterations", num_iterations)

        if num_iterations >= max_iterations:
            early_stopping_method = await ctx.store.get(
                "early_stopping_method", default="force"
            )
            if early_stopping_method == "generate":
                return await self._generate_early_stopping_response(ctx, max_iterations)
            else:
                raise WorkflowRuntimeError(
                    f"Max iterations of {max_iterations} reached! Either something went wrong, or you can "
                    "increase the max iterations with `.run(.., max_iterations=...)` "
                    "or use `early_stopping_method='generate'` to generate a final response instead."
                )

        memory: BaseMemory = await ctx.store.get("memory")

        if ev.retry_messages:
            # Retry with the given messages to let the LLM fix potential errors
            history = await memory.aget()
            user_msg_str = await ctx.store.get("user_msg_str")

            return AgentInput(
                input=[
                    *history,
                    ChatMessage(role="user", content=user_msg_str),
                    *ev.retry_messages,
                ],
                current_agent_name=self.name,
            )

        if not ev.tool_calls:
            # important: messages should always be fetched after calling finalize, otherwise they do not contain the agent's response
            output = await self.finalize(ctx, ev, memory)
            messages = await memory.aget()
            cur_tool_calls: List[ToolCallResult] = await ctx.store.get(
                "current_tool_calls", default=[]
            )
            output.tool_calls.extend(cur_tool_calls)  # type: ignore

            if self.structured_output_fn is not None:
                try:
                    if inspect.iscoroutinefunction(self.structured_output_fn):
                        output.structured_response = await self.structured_output_fn(
                            messages
                        )
                    else:
                        output.structured_response = cast(
                            Dict[str, Any], self.structured_output_fn(messages)
                        )
                    ctx.write_event_to_stream(
                        AgentStreamStructuredOutput(output=output.structured_response)
                    )
                except Exception as e:
                    warnings.warn(
                        f"There was a problem with the generation of the structured output: {e}",
                        stacklevel=2,
                    )
            if self.output_cls is not None:
                try:
                    llm_input = [*messages]
                    if self.system_prompt:
                        llm_input = [
                            ChatMessage(role="system", content=self.system_prompt),
                            *llm_input,
                        ]
                    output.structured_response = await generate_structured_response(
                        messages=llm_input, llm=self.llm, output_cls=self.output_cls
                    )
                    ctx.write_event_to_stream(
                        AgentStreamStructuredOutput(output=output.structured_response)
                    )
                except Exception as e:
                    warnings.warn(
                        f"There was a problem with the generation of the structured output: {e}",
                        stacklevel=2,
                    )

            await ctx.store.set("current_tool_calls", [])

            return StopEvent(result=output)

        await ctx.store.set("num_tool_calls", len(ev.tool_calls))

        for tool_call in ev.tool_calls:
            ctx.send_event(
                ToolCall(
                    tool_name=tool_call.tool_name,
                    tool_kwargs=tool_call.tool_kwargs,
                    tool_id=tool_call.tool_id,
                )
            )

        return None

    @step
    async defcall_tool(self, ctx: Context, ev: ToolCall) -> ToolCallResult:
"""Calls the tool and handles the result."""
        ctx.write_event_to_stream(
            ToolCall(
                tool_name=ev.tool_name,
                tool_kwargs=ev.tool_kwargs,
                tool_id=ev.tool_id,
            )
        )

        tools = await self.get_tools(ev.tool_name)
        tools_by_name = {tool.metadata.name: tool for tool in tools}
        if ev.tool_name not in tools_by_name:
            tool = None
            result = ToolOutput(
                content=f"Tool {ev.tool_name} not found. Please select a tool that is available.",
                tool_name=ev.tool_name,
                raw_input=ev.tool_kwargs,
                raw_output=None,
                is_error=True,
            )
        else:
            tool = tools_by_name[ev.tool_name]
            result = await self._call_tool(ctx, tool, ev.tool_kwargs)

        result_ev = ToolCallResult(
            tool_name=ev.tool_name,
            tool_kwargs=ev.tool_kwargs,
            tool_id=ev.tool_id,
            tool_output=result,
            return_direct=tool.metadata.return_direct if tool else False,
        )

        ctx.write_event_to_stream(result_ev)
        return result_ev

    @step
    async defaggregate_tool_results(
        self, ctx: Context, ev: ToolCallResult
    ) -> Union[AgentInput, StopEvent, None]:
"""Aggregate tool results and return the next agent input."""
        num_tool_calls = await ctx.store.get("num_tool_calls", default=0)
        if num_tool_calls == 0:
            raise ValueError("No tool calls found, cannot aggregate results.")

        tool_call_results: list[ToolCallResult] = ctx.collect_events(  # type: ignore
            ev, expected=[ToolCallResult] * num_tool_calls
        )
        if not tool_call_results:
            return None

        memory: BaseMemory = await ctx.store.get("memory")

        # track tool calls made during a .run() call
        cur_tool_calls: List[ToolCallResult] = await ctx.store.get(
            "current_tool_calls", default=[]
        )
        cur_tool_calls.extend(tool_call_results)
        await ctx.store.set("current_tool_calls", cur_tool_calls)

        await self.handle_tool_call_results(ctx, tool_call_results, memory)

        if any(
            tool_call_result.return_direct and not tool_call_result.tool_output.is_error
            for tool_call_result in tool_call_results
        ):
            # if any tool calls return directly and it's not an error tool call, take the first one
            return_direct_tool = next(
                tool_call_result
                for tool_call_result in tool_call_results
                if tool_call_result.return_direct
                and not tool_call_result.tool_output.is_error
            )

            # always finalize the agent, even if we're just handing off
            result = AgentOutput(
                response=ChatMessage(
                    role="assistant",
                    content=return_direct_tool.tool_output.content or "",
                ),
                tool_calls=[
                    ToolSelection(
                        tool_id=t.tool_id,
                        tool_name=t.tool_name,
                        tool_kwargs=t.tool_kwargs,
                    )
                    for t in cur_tool_calls
                ],
                raw=return_direct_tool.tool_output.raw_output,
                current_agent_name=self.name,
            )
            result = await self.finalize(ctx, result, memory)
            # we don't want to stop the system if we're just handing off
            if return_direct_tool.tool_name != "handoff":
                await ctx.store.set("current_tool_calls", [])
                return StopEvent(result=result)

        user_msg_str = await ctx.store.get("user_msg_str")
        input_messages = await memory.aget(input=user_msg_str)

        return AgentInput(input=input_messages, current_agent_name=self.name)

    # TODO: Remove the deprecated agent-specific overload. The agent params
    # (user_msg, chat_history, memory, etc.) should be passed as kwargs that
    # flow through Workflow.run() → AgentWorkflowStartEvent construction
    # automatically, matching the standard Workflow.run(ctx, start_event,
    # **kwargs) signature. At that point this entire override can be deleted.

    @overload
    @deprecated(
        "Use the standard workflow signature instead: "
        "agent.run(user_msg='hello') or "
        "agent.run(ctx=ctx, start_event=event, user_msg='hello'). "
        "This positional signature will be removed in a future version.",
        category=None,
    )
    defrun(
        self,
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        memory: Optional[BaseMemory] = None,
        ctx: Optional[Context] = None,
        max_iterations: Optional[int] = None,
        early_stopping_method: Optional[Literal["force", "generate"]] = None,
        start_event: Optional[AgentWorkflowStartEvent] = None,
        **kwargs: Any,
    ) -> WorkflowHandler: ...

    @overload
    defrun(
        self,
        ctx: Optional[Context] = None,
        start_event: Optional[StartEvent] = None,
        **kwargs: Any,
    ) -> WorkflowHandler: ...

    defrun(self, *args: Any, **kwargs: Any) -> WorkflowHandler:
        user_msg: Optional[Union[str, ChatMessage]] = None
        chat_history: Optional[List[ChatMessage]] = None
        memory: Optional[BaseMemory] = None
        ctx: Optional[Context] = None
        start_event: Optional[StartEvent] = None

        if args:
            first = args[0]
            if isinstance(first, Context):
                ctx = first
                if len(args)  1 and isinstance(args[1], StartEvent):
                    start_event = args[1]
            else:
                user_msg = first
                if len(args)  1:
                    chat_history = args[1]
                if len(args)  2:
                    memory = args[2]
                if len(args)  3:
                    ctx = args[3]

        user_msg = kwargs.pop("user_msg", None) or user_msg
        chat_history = kwargs.pop("chat_history", None) or chat_history
        memory = kwargs.pop("memory", None) or memory
        ctx = kwargs.pop("ctx", None) or ctx
        max_iterations: Optional[int] = kwargs.pop("max_iterations", None)
        early_stopping_method: Optional[Literal["force", "generate"]] = kwargs.pop(
            "early_stopping_method", None
        )
        start_event = kwargs.pop("start_event", None) or start_event
        run_id = kwargs.pop("run_id", None)

        if ctx is not None and ctx.is_running:
            return super().run(
                ctx=ctx,
                run_id=run_id,
                **kwargs,
            )
        else:
            if start_event is None or isinstance(start_event, AgentWorkflowStartEvent):
                start_event = start_event or AgentWorkflowStartEvent(
                    user_msg=user_msg,
                    chat_history=chat_history,
                    memory=memory,
                    max_iterations=max_iterations,
                    early_stopping_method=early_stopping_method,
                    **kwargs,
                )
            return super().run(
                start_event=start_event,
                ctx=ctx,
                run_id=run_id,
            )

```
 |  
| --- | --- |  
###  validate [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.BaseWorkflowAgent.validate "Permanent link")

```
validate(**kwargs: ) -> 

```

Validate the workflow to ensure it's well-formed.
Explicitly delegates to Workflow.validate to resolve the method conflict between Workflow.validate (instance method) and BaseModel.validate (classmethod).
Source code in `llama-index-core/llama_index/core/agent/workflow/base_agent.py`  
| 
```
196
197
198
199
200
201
202
203
```
 | 
```
defvalidate(self, **kwargs: Any) -> bool:  # type: ignore[override]
"""
    Validate the workflow to ensure it's well-formed.

    Explicitly delegates to Workflow.validate to resolve the method conflict
    between Workflow.validate (instance method) and BaseModel.validate (classmethod).
    """
    return Workflow.validate(self, **kwargs)

```
 |  
| --- | --- |  
###  validate_tools [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.BaseWorkflowAgent.validate_tools "Permanent link")

```
validate_tools(
    v: Optional[Sequence[Union[, Callable]]]
) -> Optional[Sequence[]]

```

Validate tools.
If tools are not of type BaseTool, they will be converted to FunctionTools. This assumes the inputs are tools or callable functions.
Source code in `llama-index-core/llama_index/core/agent/workflow/base_agent.py`  
| 
```
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
```
 | 
```
@field_validator("tools", mode="before")
defvalidate_tools(
    cls, v: Optional[Sequence[Union[BaseTool, Callable]]]
) -> Optional[Sequence[BaseTool]]:
"""
    Validate tools.

    If tools are not of type BaseTool, they will be converted to FunctionTools.
    This assumes the inputs are tools or callable functions.
    """
    if v is None:
        return None

    validated_tools: List[BaseTool] = []
    for tool in v:
        if not isinstance(tool, BaseTool):
            validated_tools.append(FunctionTool.from_defaults(tool))
        else:
            validated_tools.append(tool)

    for tool in validated_tools:
        if tool.metadata.name == "handoff":
            raise ValueError(
                "'handoff' is a reserved tool name. Please use a different name."
            )

    return validated_tools  # type: ignore[return-value]

```
 |  
| --- | --- |  
###  take_step `abstractmethod` `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.BaseWorkflowAgent.take_step "Permanent link")

```
take_step(
    ctx: ,
    llm_input: [],
    tools: Sequence[],
    memory: ,
) -> 

```

Take a single step with the agent.
Source code in `llama-index-core/llama_index/core/agent/workflow/base_agent.py`  
| 
```
244
245
246
247
248
249
250
251
252
```
 | 
```
@abstractmethod
async deftake_step(
    self,
    ctx: AgentContext,
    llm_input: List[ChatMessage],
    tools: Sequence[AsyncBaseTool],
    memory: BaseMemory,
) -> AgentOutput:
"""Take a single step with the agent."""

```
 |  
| --- | --- |  
###  handle_tool_call_results `abstractmethod` `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.BaseWorkflowAgent.handle_tool_call_results "Permanent link")

```
handle_tool_call_results(
    ctx: Context,
    results: [],
    memory: ,
) -> None

```

Handle tool call results.
Source code in `llama-index-core/llama_index/core/agent/workflow/base_agent.py`  
| 
```
254
255
256
257
258
```
 | 
```
@abstractmethod
async defhandle_tool_call_results(
    self, ctx: Context, results: List[ToolCallResult], memory: BaseMemory
) -> None:
"""Handle tool call results."""

```
 |  
| --- | --- |  
###  finalize `abstractmethod` `async` [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.BaseWorkflowAgent.finalize "Permanent link")

```
finalize(
    ctx: Context, output: , memory: 
) -> 

```

Finalize the agent's execution.
Source code in `llama-index-core/llama_index/core/agent/workflow/base_agent.py`  
| 
```
260
261
262
263
264
```
 | 
```
@abstractmethod
async deffinalize(
    self, ctx: Context, output: AgentOutput, memory: BaseMemory
) -> AgentOutput:
"""Finalize the agent's execution."""

```
 |  
| --- | --- |  
###  get_tools [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.BaseWorkflowAgent.get_tools "Permanent link")

```
get_tools(
    input_str: Optional[] = None,
) -> Sequence[]

```

Get tools for the given agent.
Source code in `llama-index-core/llama_index/core/agent/workflow/base_agent.py`  
| 
```
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
```
 | 
```
async defget_tools(
    self, input_str: Optional[str] = None
) -> Sequence[AsyncBaseTool]:
"""Get tools for the given agent."""
    tools = [*self.tools] if self.tools else []
    if self.tool_retriever is not None:
        retrieved_tools = await self.tool_retriever.aretrieve(input_str or "")
        tools.extend(retrieved_tools)

    return self._ensure_tools_are_async(cast(List[BaseTool], tools))

```
 |  
| --- | --- |  
###  init_run [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.BaseWorkflowAgent.init_run "Permanent link")

```
init_run(
    ctx: Context, ev: AgentWorkflowStartEvent
) -> 

```

Sets up the workflow and validates inputs.
Source code in `llama-index-core/llama_index/core/agent/workflow/base_agent.py`  
| 
```
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
```
 | 
```
@step
async definit_run(self, ctx: Context, ev: AgentWorkflowStartEvent) -> AgentInput:
"""Sets up the workflow and validates inputs."""
    await self._init_context(ctx, ev)

    user_msg: Optional[Union[str, ChatMessage]] = ev.get("user_msg")
    chat_history: Optional[List[ChatMessage]] = ev.get("chat_history", [])

    # Convert string user_msg to ChatMessage
    if isinstance(user_msg, str):
        user_msg = ChatMessage(role="user", content=user_msg)

    # Add messages to memory
    memory: BaseMemory = await ctx.store.get("memory")

    # First set chat history if it exists
    if chat_history:
        await memory.aset(chat_history)

    # Then add user message if it exists
    if user_msg:
        await memory.aput(user_msg)
        content_str = "\n".join(
            [
                block.text
                for block in user_msg.blocks
                if isinstance(block, TextBlock)
            ]
        )
        await ctx.store.set("user_msg_str", content_str)
    elif chat_history and not all(
        message.role == "system" for message in chat_history
    ):
        # If no user message, use the last message from chat history as user_msg_str
        user_hist: List[ChatMessage] = [
            msg for msg in chat_history if msg.role == "user"
        ]
        content_str = "\n".join(
            [
                block.text
                for block in user_hist[-1].blocks
                if isinstance(block, TextBlock)
            ]
        )
        await ctx.store.set("user_msg_str", content_str)
    else:
        raise ValueError("Must provide either user_msg or chat_history")

    # Get all messages from memory
    input_messages = await memory.aget()

    # send to the current agent
    return AgentInput(input=input_messages, current_agent_name=self.name)

```
 |  
| --- | --- |  
###  setup_agent [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.BaseWorkflowAgent.setup_agent "Permanent link")

```
setup_agent(ctx: Context, ev: ) -> 

```

Main agent handling logic.
Source code in `llama-index-core/llama_index/core/agent/workflow/base_agent.py`  
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
```
 | 
```
@step
async defsetup_agent(self, ctx: Context, ev: AgentInput) -> AgentSetup:
"""Main agent handling logic."""
    llm_input = [*ev.input]

    if self.system_prompt:
        llm_input = [
            ChatMessage(role="system", content=self.system_prompt),
            *llm_input,
        ]

    state = await ctx.store.get("state", default=None)
    formatted_input_with_state = await ctx.store.get(
        "formatted_input_with_state", default=False
    )
    if state and not formatted_input_with_state:
        # update last message with current state
        for block in llm_input[-1].blocks[::-1]:
            if isinstance(block, TextBlock):
                block.text = self.state_prompt.format(state=state, msg=block.text)
                break
        await ctx.store.set("formatted_input_with_state", True)

    return AgentSetup(
        input=llm_input,
        current_agent_name=ev.current_agent_name,
    )

```
 |  
| --- | --- |  
###  run_agent_step [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.BaseWorkflowAgent.run_agent_step "Permanent link")

```
run_agent_step(ctx: Context, ev: ) -> 

```

Run the agent.
Source code in `llama-index-core/llama_index/core/agent/workflow/base_agent.py`  
| 
```
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
```
 | 
```
@step
async defrun_agent_step(self, ctx: Context, ev: AgentSetup) -> AgentOutput:
"""Run the agent."""
    memory: BaseMemory = await ctx.store.get("memory")
    user_msg_str = await ctx.store.get("user_msg_str")
    tools = await self.get_tools(user_msg_str or "")

    agent_output = await self.take_step(
        ctx,
        ev.input,
        tools,
        memory,
    )

    ctx.write_event_to_stream(agent_output)
    return agent_output

```
 |  
| --- | --- |  
###  call_tool [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.BaseWorkflowAgent.call_tool "Permanent link")

```
call_tool(ctx: Context, ev: ) -> 

```

Calls the tool and handles the result.
Source code in `llama-index-core/llama_index/core/agent/workflow/base_agent.py`  
| 
```
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
```
 | 
```
@step
async defcall_tool(self, ctx: Context, ev: ToolCall) -> ToolCallResult:
"""Calls the tool and handles the result."""
    ctx.write_event_to_stream(
        ToolCall(
            tool_name=ev.tool_name,
            tool_kwargs=ev.tool_kwargs,
            tool_id=ev.tool_id,
        )
    )

    tools = await self.get_tools(ev.tool_name)
    tools_by_name = {tool.metadata.name: tool for tool in tools}
    if ev.tool_name not in tools_by_name:
        tool = None
        result = ToolOutput(
            content=f"Tool {ev.tool_name} not found. Please select a tool that is available.",
            tool_name=ev.tool_name,
            raw_input=ev.tool_kwargs,
            raw_output=None,
            is_error=True,
        )
    else:
        tool = tools_by_name[ev.tool_name]
        result = await self._call_tool(ctx, tool, ev.tool_kwargs)

    result_ev = ToolCallResult(
        tool_name=ev.tool_name,
        tool_kwargs=ev.tool_kwargs,
        tool_id=ev.tool_id,
        tool_output=result,
        return_direct=tool.metadata.return_direct if tool else False,
    )

    ctx.write_event_to_stream(result_ev)
    return result_ev

```
 |  
| --- | --- |  
###  aggregate_tool_results [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.BaseWorkflowAgent.aggregate_tool_results "Permanent link")

```
aggregate_tool_results(
    ctx: Context, ev: 
) -> Union[, StopEvent, None]

```

Aggregate tool results and return the next agent input.
Source code in `llama-index-core/llama_index/core/agent/workflow/base_agent.py`  
| 
```
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
724
```
 | 
```
@step
async defaggregate_tool_results(
    self, ctx: Context, ev: ToolCallResult
) -> Union[AgentInput, StopEvent, None]:
"""Aggregate tool results and return the next agent input."""
    num_tool_calls = await ctx.store.get("num_tool_calls", default=0)
    if num_tool_calls == 0:
        raise ValueError("No tool calls found, cannot aggregate results.")

    tool_call_results: list[ToolCallResult] = ctx.collect_events(  # type: ignore
        ev, expected=[ToolCallResult] * num_tool_calls
    )
    if not tool_call_results:
        return None

    memory: BaseMemory = await ctx.store.get("memory")

    # track tool calls made during a .run() call
    cur_tool_calls: List[ToolCallResult] = await ctx.store.get(
        "current_tool_calls", default=[]
    )
    cur_tool_calls.extend(tool_call_results)
    await ctx.store.set("current_tool_calls", cur_tool_calls)

    await self.handle_tool_call_results(ctx, tool_call_results, memory)

    if any(
        tool_call_result.return_direct and not tool_call_result.tool_output.is_error
        for tool_call_result in tool_call_results
    ):
        # if any tool calls return directly and it's not an error tool call, take the first one
        return_direct_tool = next(
            tool_call_result
            for tool_call_result in tool_call_results
            if tool_call_result.return_direct
            and not tool_call_result.tool_output.is_error
        )

        # always finalize the agent, even if we're just handing off
        result = AgentOutput(
            response=ChatMessage(
                role="assistant",
                content=return_direct_tool.tool_output.content or "",
            ),
            tool_calls=[
                ToolSelection(
                    tool_id=t.tool_id,
                    tool_name=t.tool_name,
                    tool_kwargs=t.tool_kwargs,
                )
                for t in cur_tool_calls
            ],
            raw=return_direct_tool.tool_output.raw_output,
            current_agent_name=self.name,
        )
        result = await self.finalize(ctx, result, memory)
        # we don't want to stop the system if we're just handing off
        if return_direct_tool.tool_name != "handoff":
            await ctx.store.set("current_tool_calls", [])
            return StopEvent(result=result)

    user_msg_str = await ctx.store.get("user_msg_str")
    input_messages = await memory.aget(input=user_msg_str)

    return AgentInput(input=input_messages, current_agent_name=self.name)

```
 |  
| --- | --- |  
##  CodeActAgent [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.CodeActAgent "Permanent link")
Bases: 
A workflow agent that can execute code.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `scratchpad_key`  |  `'scratchpad'`  |  
|  `code_execute_fn`  |  `Callable | Awaitable`  |  The function to execute code. Required in order to execute code generated by the agent. The function protocol is as follows: async def code_execute_fn(code: str) -> Dict[str, Any]  |  _required_  |  
|  `code_act_system_prompt`  |  `str | BasePromptTemplate[](https://developers.llamaindex.ai/python/framework-api-reference/prompts/#llama_index.core.prompts.BasePromptTemplate "BasePromptTemplate \(llama_index.core.prompts.BasePromptTemplate\)")`  |  The system prompt for the code act agent.  |  `'You are a helpful AI assistant that can write and execute Python code to solve problems.\n\nYou will be given a task to perform. You should output:\n- Python code wrapped in <execute>...</execute> tags that provides the solution to the task, or a step towards the solution. Any output you want to extract from the code should be printed to the console.\n- Text to be shown directly to the user, if you want to ask for more information or provide the final answer.\n- If the previous code execution can be used to respond to the user, then respond directly (typically you want to avoid mentioning anything related to the code execution in your response).\n\n## Response Format:\nExample of proper code format:\n<execute>\nimport math\n\ndef calculate_area(radius):\n    return math.pi * radius**2\n\n# Calculate the area for radius = 5\narea = calculate_area(5)\nprint(f"The area of the circle is {area:.2f} square units")\n</execute>\n\nIn addition to the Python Standard Library and any functions you have already written, you can use the following functions:\n{tool_descriptions}\n\nVariables defined at the top level of previous code snippets can be also be referenced in your code.\n\n## Final Answer Guidelines:\n- When providing a final answer, focus on directly answering the user\'s question\n- Avoid referencing the code you generated unless specifically asked\n- Present the results clearly and concisely as if you computed them directly\n- If relevant, you can briefly mention general methods used, but don\'t include code snippets in the final answer\n- Structure your response like you\'re directly answering the user\'s query, not explaining how you solved it\n\nReminder: Always place your Python code between <execute>...</execute> tags when you want to run code. You can include explanations and other content outside these tags.\n'`  |  
Source code in `llama-index-core/llama_index/core/agent/workflow/codeact_agent.py`  
| 
```
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
```
 | 
```
classCodeActAgent(BaseWorkflowAgent):
"""
    A workflow agent that can execute code.
    """

    scratchpad_key: str = "scratchpad"

    code_execute_fn: Union[Callable, Awaitable] = Field(
        description=(
            "The function to execute code. Required in order to execute code generated by the agent.\n"
            "The function protocol is as follows: async def code_execute_fn(code: str) -> Dict[str, Any]"
        ),
    )

    code_act_system_prompt: Union[str, BasePromptTemplate] = Field(
        default=DEFAULT_CODE_ACT_PROMPT,
        description="The system prompt for the code act agent.",
        validate_default=True,
    )

    def__init__(
        self,
        code_execute_fn: Union[Callable, Awaitable],
        name: str = "code_act_agent",
        description: str = "A workflow agent that can execute code.",
        system_prompt: Optional[str] = None,
        tools: Optional[List[Union[BaseTool, Callable]]] = None,
        tool_retriever: Optional[ObjectRetriever] = None,
        can_handoff_to: Optional[List[str]] = None,
        llm: Optional[LLM] = None,
        code_act_system_prompt: Union[
            str, BasePromptTemplate
        ] = DEFAULT_CODE_ACT_PROMPT,
        streaming: bool = True,
    ):
        tools = tools or []
        tools.append(  # type: ignore
            FunctionTool.from_defaults(code_execute_fn, name=EXECUTE_TOOL_NAME)  # type: ignore
        )
        if isinstance(code_act_system_prompt, str):
            if system_prompt:
                code_act_system_prompt += "\n" + system_prompt
            code_act_system_prompt = PromptTemplate(code_act_system_prompt)
        elif isinstance(code_act_system_prompt, BasePromptTemplate):
            if system_prompt:
                code_act_system_str = code_act_system_prompt.get_template()
                code_act_system_str += "\n" + system_prompt
            code_act_system_prompt = PromptTemplate(code_act_system_str)

        super().__init__(
            name=name,
            description=description,
            system_prompt=system_prompt,
            tools=tools,
            tool_retriever=tool_retriever,
            can_handoff_to=can_handoff_to,
            llm=llm,
            code_act_system_prompt=code_act_system_prompt,
            code_execute_fn=code_execute_fn,
            streaming=streaming,
        )

    def_get_tool_fns(self, tools: Sequence[BaseTool]) -> List[Callable]:
"""Get the tool functions while validating that they are valid tools for the CodeActAgent."""
        callables = []
        for tool in tools:
            if (
                tool.metadata.name == "handoff"
                or tool.metadata.name == EXECUTE_TOOL_NAME
            ):
                continue

            if isinstance(tool, FunctionTool):
                if tool.requires_context:
                    raise ValueError(
                        f"Tool {tool.metadata.name} requires context. "
                        "CodeActAgent only supports tools that do not require context."
                    )

                callables.append(tool.real_fn)
            else:
                raise ValueError(
                    f"Tool {tool.metadata.name} is not a FunctionTool. "
                    "CodeActAgent only supports Functions and FunctionTools."
                )

        return callables

    def_extract_code_from_response(self, response_text: str) -> Optional[str]:
"""
        Extract code from the LLM response using XML-style <execute> tags.

        Args:
            response_text: The LLM response text

        Returns:
            Extracted code or None if no code found

        """
        # Match content between <execute> and </execute> tags
        execute_pattern = r"<execute>(.*?)</execute>"
        execute_matches = re.findall(execute_pattern, response_text, re.DOTALL)

        if execute_matches:
            return "\n\n".join([x.strip() for x in execute_matches])

        return None

    def_get_tool_descriptions(self, tools: Sequence[BaseTool]) -> str:
"""
        Generate tool descriptions for the system prompt using tool metadata.

        Args:
            tools: List of available tools

        Returns:
            Tool descriptions as a string

        """
        tool_descriptions = []

        tool_fns = self._get_tool_fns(tools)
        for fn in tool_fns:
            signature = inspect.signature(fn)
            fn_name: str = fn.__name__
            docstring: Optional[str] = inspect.getdoc(fn)

            tool_description = f"def {fn_name}{signature!s}:"
            if docstring:
                tool_description += f'\n  """\n{docstring}\n  """\n'

            tool_description += "\n  ...\n"
            tool_descriptions.append(tool_description)

        return "\n\n".join(tool_descriptions)

    async def_get_response(
        self, current_llm_input: List[ChatMessage], tools: Sequence[BaseTool]
    ) -> ChatResponse:
        if any(tool.metadata.name == "handoff" for tool in tools):
            if not isinstance(self.llm, FunctionCallingLLM):
                raise ValueError("llm must be a function calling LLM to use handoff")

            tools = [tool for tool in tools if tool.metadata.name == "handoff"]
            return await self.llm.achat_with_tools(
                tools=tools, chat_history=current_llm_input
            )
        else:
            return await self.llm.achat(current_llm_input)

    async def_get_streaming_response(
        self,
        ctx: AgentContext,
        current_llm_input: List[ChatMessage],
        tools: Sequence[BaseTool],
    ) -> Tuple[ChatResponse, str]:
        if any(tool.metadata.name == "handoff" for tool in tools):
            if not isinstance(self.llm, FunctionCallingLLM):
                raise ValueError("llm must be a function calling LLM to use handoff")

            tools = [tool for tool in tools if tool.metadata.name == "handoff"]
            response = await self.llm.astream_chat_with_tools(
                tools=tools, chat_history=current_llm_input
            )
        else:
            response = await self.llm.astream_chat(current_llm_input)

        last_chat_response = ChatResponse(message=ChatMessage())
        full_response_text = ""

        # Process streaming response
        async for last_chat_response in response:
            delta = last_chat_response.delta or ""
            full_response_text += delta

            # Create a raw object for the event stream
            raw = (
                last_chat_response.raw.model_dump()
                if isinstance(last_chat_response.raw, BaseModel)
                else last_chat_response.raw
            )

            # Write delta to the event stream
            ctx.write_event_to_stream(
                AgentStream(
                    delta=delta,
                    response=full_response_text,
                    # We'll add the tool call after processing the full response
                    tool_calls=[],
                    raw=raw,
                    current_agent_name=self.name,
                    thinking_delta=last_chat_response.additional_kwargs.get(
                        "thinking_delta", None
                    ),
                )
            )

        return last_chat_response, full_response_text

    async deftake_step(
        self,
        ctx: AgentContext,
        llm_input: List[ChatMessage],
        tools: Sequence[BaseTool],
        memory: BaseMemory,
    ) -> AgentOutput:
"""Take a single step with the code act agent."""
        if not self.code_execute_fn:
            raise ValueError("code_execute_fn must be provided for CodeActAgent")

        # Get current scratchpad
        scratchpad: List[ChatMessage] = await ctx.store.get(
            self.scratchpad_key, default=[]
        )
        current_llm_input = [*llm_input, *scratchpad]

        # Create a system message with tool descriptions
        tool_descriptions = self._get_tool_descriptions(tools)
        system_prompt = self.code_act_system_prompt.format(
            tool_descriptions=tool_descriptions
        )

        # Add or overwrite system message
        has_system = False
        for i, msg in enumerate(current_llm_input):
            if msg.role.value == "system":
                current_llm_input[i] = ChatMessage(role="system", content=system_prompt)
                has_system = True
                break

        if not has_system:
            current_llm_input.insert(
                0, ChatMessage(role="system", content=system_prompt)
            )

        # Write the input to the event stream
        ctx.write_event_to_stream(
            AgentInput(input=current_llm_input, current_agent_name=self.name)
        )

        if self.streaming:
            chat_response, full_response_text = await self._get_streaming_response(
                ctx, current_llm_input, tools
            )
        else:
            chat_response = await self._get_response(current_llm_input, tools)
            full_response_text = chat_response.message.content or ""

        # Extract code from the response
        code = self._extract_code_from_response(full_response_text)

        # Create a tool call for executing the code if code was found
        tool_calls = []
        if code:
            tool_id = str(uuid.uuid4())

            tool_calls = [
                ToolSelection(
                    tool_id=tool_id,
                    tool_name=EXECUTE_TOOL_NAME,
                    tool_kwargs={"code": code},
                )
            ]

        if isinstance(self.llm, FunctionCallingLLM):
            extra_tool_calls = self.llm.get_tool_calls_from_response(
                chat_response, error_on_no_tool_call=False
            )
            tool_calls.extend(extra_tool_calls)

        # Add the response to the scratchpad
        message = ChatMessage(role="assistant", content=full_response_text)
        scratchpad.append(message)
        await ctx.store.set(self.scratchpad_key, scratchpad)

        # Create the raw object for the output
        raw = (
            chat_response.raw.model_dump()
            if isinstance(chat_response.raw, BaseModel)
            else chat_response.raw
        )

        return AgentOutput(
            response=message,
            tool_calls=tool_calls,
            raw=raw,
            current_agent_name=self.name,
        )

    async defhandle_tool_call_results(
        self, ctx: Context, results: List[ToolCallResult], memory: BaseMemory
    ) -> None:
"""Handle tool call results for code act agent."""
        scratchpad: List[ChatMessage] = await ctx.store.get(
            self.scratchpad_key, default=[]
        )

        # handle code execution and handoff
        for tool_call_result in results:
            # Format the output as a tool response message
            if tool_call_result.tool_name == EXECUTE_TOOL_NAME:
                code_result = f"Result of executing the code given:\n\n{tool_call_result.tool_output.content}"
                scratchpad.append(
                    ChatMessage(
                        role="user",
                        content=code_result,
                    )
                )
            elif tool_call_result.tool_name == "handoff":
                scratchpad.append(
                    ChatMessage(
                        role="tool",
                        blocks=tool_call_result.tool_output.blocks,
                        additional_kwargs={"tool_call_id": tool_call_result.tool_id},
                    )
                )
            else:
                raise ValueError(f"Unknown tool name: {tool_call_result.tool_name}")

        await ctx.store.set(self.scratchpad_key, scratchpad)

    async deffinalize(
        self, ctx: Context, output: AgentOutput, memory: BaseMemory
    ) -> AgentOutput:
"""
        Finalize the code act agent.

        Adds all in-progress messages to memory.
        """
        scratchpad: List[ChatMessage] = await ctx.store.get(
            self.scratchpad_key, default=[]
        )
        await memory.aput_messages(scratchpad)

        # reset scratchpad
        await ctx.store.set(self.scratchpad_key, [])

        return output

```
 |  
| --- | --- |  
###  take_step [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.CodeActAgent.take_step "Permanent link")

```
take_step(
    ctx: ,
    llm_input: [],
    tools: Sequence[],
    memory: ,
) -> 

```

Take a single step with the code act agent.
Source code in `llama-index-core/llama_index/core/agent/workflow/codeact_agent.py`  
| 
```
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
```
 | 
```
async deftake_step(
    self,
    ctx: AgentContext,
    llm_input: List[ChatMessage],
    tools: Sequence[BaseTool],
    memory: BaseMemory,
) -> AgentOutput:
"""Take a single step with the code act agent."""
    if not self.code_execute_fn:
        raise ValueError("code_execute_fn must be provided for CodeActAgent")

    # Get current scratchpad
    scratchpad: List[ChatMessage] = await ctx.store.get(
        self.scratchpad_key, default=[]
    )
    current_llm_input = [*llm_input, *scratchpad]

    # Create a system message with tool descriptions
    tool_descriptions = self._get_tool_descriptions(tools)
    system_prompt = self.code_act_system_prompt.format(
        tool_descriptions=tool_descriptions
    )

    # Add or overwrite system message
    has_system = False
    for i, msg in enumerate(current_llm_input):
        if msg.role.value == "system":
            current_llm_input[i] = ChatMessage(role="system", content=system_prompt)
            has_system = True
            break

    if not has_system:
        current_llm_input.insert(
            0, ChatMessage(role="system", content=system_prompt)
        )

    # Write the input to the event stream
    ctx.write_event_to_stream(
        AgentInput(input=current_llm_input, current_agent_name=self.name)
    )

    if self.streaming:
        chat_response, full_response_text = await self._get_streaming_response(
            ctx, current_llm_input, tools
        )
    else:
        chat_response = await self._get_response(current_llm_input, tools)
        full_response_text = chat_response.message.content or ""

    # Extract code from the response
    code = self._extract_code_from_response(full_response_text)

    # Create a tool call for executing the code if code was found
    tool_calls = []
    if code:
        tool_id = str(uuid.uuid4())

        tool_calls = [
            ToolSelection(
                tool_id=tool_id,
                tool_name=EXECUTE_TOOL_NAME,
                tool_kwargs={"code": code},
            )
        ]

    if isinstance(self.llm, FunctionCallingLLM):
        extra_tool_calls = self.llm.get_tool_calls_from_response(
            chat_response, error_on_no_tool_call=False
        )
        tool_calls.extend(extra_tool_calls)

    # Add the response to the scratchpad
    message = ChatMessage(role="assistant", content=full_response_text)
    scratchpad.append(message)
    await ctx.store.set(self.scratchpad_key, scratchpad)

    # Create the raw object for the output
    raw = (
        chat_response.raw.model_dump()
        if isinstance(chat_response.raw, BaseModel)
        else chat_response.raw
    )

    return AgentOutput(
        response=message,
        tool_calls=tool_calls,
        raw=raw,
        current_agent_name=self.name,
    )

```
 |  
| --- | --- |  
###  handle_tool_call_results [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.CodeActAgent.handle_tool_call_results "Permanent link")

```
handle_tool_call_results(
    ctx: Context,
    results: [],
    memory: ,
) -> None

```

Handle tool call results for code act agent.
Source code in `llama-index-core/llama_index/core/agent/workflow/codeact_agent.py`  
| 
```
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
```
 | 
```
async defhandle_tool_call_results(
    self, ctx: Context, results: List[ToolCallResult], memory: BaseMemory
) -> None:
"""Handle tool call results for code act agent."""
    scratchpad: List[ChatMessage] = await ctx.store.get(
        self.scratchpad_key, default=[]
    )

    # handle code execution and handoff
    for tool_call_result in results:
        # Format the output as a tool response message
        if tool_call_result.tool_name == EXECUTE_TOOL_NAME:
            code_result = f"Result of executing the code given:\n\n{tool_call_result.tool_output.content}"
            scratchpad.append(
                ChatMessage(
                    role="user",
                    content=code_result,
                )
            )
        elif tool_call_result.tool_name == "handoff":
            scratchpad.append(
                ChatMessage(
                    role="tool",
                    blocks=tool_call_result.tool_output.blocks,
                    additional_kwargs={"tool_call_id": tool_call_result.tool_id},
                )
            )
        else:
            raise ValueError(f"Unknown tool name: {tool_call_result.tool_name}")

    await ctx.store.set(self.scratchpad_key, scratchpad)

```
 |  
| --- | --- |  
###  finalize [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.CodeActAgent.finalize "Permanent link")

```
finalize(
    ctx: Context, output: , memory: 
) -> 

```

Finalize the code act agent.
Adds all in-progress messages to memory.
Source code in `llama-index-core/llama_index/core/agent/workflow/codeact_agent.py`  
| 
```
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
```
 | 
```
async deffinalize(
    self, ctx: Context, output: AgentOutput, memory: BaseMemory
) -> AgentOutput:
"""
    Finalize the code act agent.

    Adds all in-progress messages to memory.
    """
    scratchpad: List[ChatMessage] = await ctx.store.get(
        self.scratchpad_key, default=[]
    )
    await memory.aput_messages(scratchpad)

    # reset scratchpad
    await ctx.store.set(self.scratchpad_key, [])

    return output

```
 |  
| --- | --- |  
##  FunctionAgent [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.FunctionAgent "Permanent link")
Bases: 
Function calling agent implementation.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `scratchpad_key`  |  `'scratchpad'`  |  
|  `initial_tool_choice`  |  `str | None`  |  The tool to try and force to call on the first iteration of the agent.  |  `None`  |  
|  `allow_parallel_tool_calls`  |  `bool`  |  If True, the agent will call multiple tools in parallel. If False, the agent will call tools sequentially.  |  `True`  |  
Source code in `llama-index-core/llama_index/core/agent/workflow/function_agent.py`  
| 
```
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
```
 | 
```
classFunctionAgent(BaseWorkflowAgent):
"""Function calling agent implementation."""

    scratchpad_key: str = "scratchpad"
    initial_tool_choice: Optional[str] = Field(
        default=None,
        description="The tool to try and force to call on the first iteration of the agent.",
    )
    allow_parallel_tool_calls: bool = Field(
        default=True,
        description="If True, the agent will call multiple tools in parallel. If False, the agent will call tools sequentially.",
    )

    async def_get_response(
        self, current_llm_input: List[ChatMessage], tools: Sequence[AsyncBaseTool]
    ) -> ChatResponse:
        chat_kwargs = {
            "chat_history": current_llm_input,
            "allow_parallel_tool_calls": self.allow_parallel_tool_calls,
            "tools": tools,
        }

        # Only add tool choice if set and if its the first response
        if (
            self.initial_tool_choice is not None
            and current_llm_input[-1].role == "user"
        ):
            chat_kwargs["tool_choice"] = self.initial_tool_choice

        return await self.llm.achat_with_tools(  # type: ignore
            **chat_kwargs
        )

    async def_get_streaming_response(
        self,
        ctx: AgentContext,
        current_llm_input: List[ChatMessage],
        tools: Sequence[AsyncBaseTool],
    ) -> ChatResponse:
        chat_kwargs = {
            "chat_history": current_llm_input,
            "tools": tools,
            "allow_parallel_tool_calls": self.allow_parallel_tool_calls,
        }

        # Only add tool choice if set and if its the first response
        if (
            self.initial_tool_choice is not None
            and current_llm_input[-1].role == "user"
        ):
            chat_kwargs["tool_choice"] = self.initial_tool_choice

        response = await self.llm.astream_chat_with_tools(  # type: ignore
            **chat_kwargs
        )
        # last_chat_response will be used later, after the loop.
        # We initialize it so it's valid even when 'response' is empty
        last_chat_response = ChatResponse(message=ChatMessage())
        async for last_chat_response in response:
            tool_calls = self.llm.get_tool_calls_from_response(  # type: ignore
                last_chat_response, error_on_no_tool_call=False
            )
            raw = (
                last_chat_response.raw.model_dump()
                if isinstance(last_chat_response.raw, BaseModel)
                else last_chat_response.raw
            )
            ctx.write_event_to_stream(
                AgentStream(
                    delta=last_chat_response.delta or "",
                    response=last_chat_response.message.content or "",
                    tool_calls=tool_calls or [],
                    raw=raw,
                    current_agent_name=self.name,
                    thinking_delta=last_chat_response.additional_kwargs.get(
                        "thinking_delta", None
                    ),
                )
            )

        return last_chat_response

    async deftake_step(
        self,
        ctx: AgentContext,
        llm_input: List[ChatMessage],
        tools: Sequence[AsyncBaseTool],
        memory: BaseMemory,
    ) -> AgentOutput:
"""Take a single step with the function calling agent."""
        if not self.llm.metadata.is_function_calling_model:
            raise ValueError("LLM must be a FunctionCallingLLM")

        scratchpad: List[ChatMessage] = await ctx.store.get(
            self.scratchpad_key, default=[]
        )
        current_llm_input = [*llm_input, *scratchpad]

        ctx.write_event_to_stream(
            AgentInput(input=current_llm_input, current_agent_name=self.name)
        )

        if self.streaming:
            last_chat_response = await self._get_streaming_response(
                ctx, current_llm_input, tools
            )
        else:
            last_chat_response = await self._get_response(current_llm_input, tools)

        tool_calls = self.llm.get_tool_calls_from_response(  # type: ignore
            last_chat_response, error_on_no_tool_call=False
        )

        # only add to scratchpad if we didn't select the handoff tool
        scratchpad.append(last_chat_response.message)
        await ctx.store.set(self.scratchpad_key, scratchpad)

        raw = (
            last_chat_response.raw.model_dump()
            if isinstance(last_chat_response.raw, BaseModel)
            else last_chat_response.raw
        )
        return AgentOutput(
            response=last_chat_response.message,
            tool_calls=tool_calls or [],
            raw=raw,
            current_agent_name=self.name,
        )

    async defhandle_tool_call_results(
        self, ctx: Context, results: List[ToolCallResult], memory: BaseMemory
    ) -> None:
"""Handle tool call results for function calling agent."""
        scratchpad: List[ChatMessage] = await ctx.store.get(
            self.scratchpad_key, default=[]
        )

        for tool_call_result in results:
            scratchpad.append(
                ChatMessage(
                    role="tool",
                    blocks=tool_call_result.tool_output.blocks,
                    additional_kwargs={"tool_call_id": tool_call_result.tool_id},
                )
            )

            if (
                tool_call_result.return_direct
                and tool_call_result.tool_name != "handoff"
            ):
                scratchpad.append(
                    ChatMessage(
                        role="assistant",
                        content=str(tool_call_result.tool_output.content),
                        additional_kwargs={"tool_call_id": tool_call_result.tool_id},
                    )
                )
                break

        await ctx.store.set(self.scratchpad_key, scratchpad)

    async deffinalize(
        self, ctx: Context, output: AgentOutput, memory: BaseMemory
    ) -> AgentOutput:
"""
        Finalize the function calling agent.

        Adds all in-progress messages to memory.
        """
        scratchpad: List[ChatMessage] = await ctx.store.get(
            self.scratchpad_key, default=[]
        )
        await memory.aput_messages(scratchpad)

        # reset scratchpad
        await ctx.store.set(self.scratchpad_key, [])

        return output

```
 |  
| --- | --- |  
###  take_step [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.FunctionAgent.take_step "Permanent link")

```
take_step(
    ctx: ,
    llm_input: [],
    tools: Sequence[],
    memory: ,
) -> 

```

Take a single step with the function calling agent.
Source code in `llama-index-core/llama_index/core/agent/workflow/function_agent.py`  
| 
```
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
```
 | 
```
async deftake_step(
    self,
    ctx: AgentContext,
    llm_input: List[ChatMessage],
    tools: Sequence[AsyncBaseTool],
    memory: BaseMemory,
) -> AgentOutput:
"""Take a single step with the function calling agent."""
    if not self.llm.metadata.is_function_calling_model:
        raise ValueError("LLM must be a FunctionCallingLLM")

    scratchpad: List[ChatMessage] = await ctx.store.get(
        self.scratchpad_key, default=[]
    )
    current_llm_input = [*llm_input, *scratchpad]

    ctx.write_event_to_stream(
        AgentInput(input=current_llm_input, current_agent_name=self.name)
    )

    if self.streaming:
        last_chat_response = await self._get_streaming_response(
            ctx, current_llm_input, tools
        )
    else:
        last_chat_response = await self._get_response(current_llm_input, tools)

    tool_calls = self.llm.get_tool_calls_from_response(  # type: ignore
        last_chat_response, error_on_no_tool_call=False
    )

    # only add to scratchpad if we didn't select the handoff tool
    scratchpad.append(last_chat_response.message)
    await ctx.store.set(self.scratchpad_key, scratchpad)

    raw = (
        last_chat_response.raw.model_dump()
        if isinstance(last_chat_response.raw, BaseModel)
        else last_chat_response.raw
    )
    return AgentOutput(
        response=last_chat_response.message,
        tool_calls=tool_calls or [],
        raw=raw,
        current_agent_name=self.name,
    )

```
 |  
| --- | --- |  
###  handle_tool_call_results [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.FunctionAgent.handle_tool_call_results "Permanent link")

```
handle_tool_call_results(
    ctx: Context,
    results: [],
    memory: ,
) -> None

```

Handle tool call results for function calling agent.
Source code in `llama-index-core/llama_index/core/agent/workflow/function_agent.py`  
| 
```
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
```
 | 
```
async defhandle_tool_call_results(
    self, ctx: Context, results: List[ToolCallResult], memory: BaseMemory
) -> None:
"""Handle tool call results for function calling agent."""
    scratchpad: List[ChatMessage] = await ctx.store.get(
        self.scratchpad_key, default=[]
    )

    for tool_call_result in results:
        scratchpad.append(
            ChatMessage(
                role="tool",
                blocks=tool_call_result.tool_output.blocks,
                additional_kwargs={"tool_call_id": tool_call_result.tool_id},
            )
        )

        if (
            tool_call_result.return_direct
            and tool_call_result.tool_name != "handoff"
        ):
            scratchpad.append(
                ChatMessage(
                    role="assistant",
                    content=str(tool_call_result.tool_output.content),
                    additional_kwargs={"tool_call_id": tool_call_result.tool_id},
                )
            )
            break

    await ctx.store.set(self.scratchpad_key, scratchpad)

```
 |  
| --- | --- |  
###  finalize [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.FunctionAgent.finalize "Permanent link")

```
finalize(
    ctx: Context, output: , memory: 
) -> 

```

Finalize the function calling agent.
Adds all in-progress messages to memory.
Source code in `llama-index-core/llama_index/core/agent/workflow/function_agent.py`  
| 
```
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
```
 | 
```
async deffinalize(
    self, ctx: Context, output: AgentOutput, memory: BaseMemory
) -> AgentOutput:
"""
    Finalize the function calling agent.

    Adds all in-progress messages to memory.
    """
    scratchpad: List[ChatMessage] = await ctx.store.get(
        self.scratchpad_key, default=[]
    )
    await memory.aput_messages(scratchpad)

    # reset scratchpad
    await ctx.store.set(self.scratchpad_key, [])

    return output

```
 |  
| --- | --- |  
##  ReActAgent [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.ReActAgent "Permanent link")
Bases: 
React agent implementation.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `reasoning_key`  |  `'current_reasoning'`  |  
|  `output_parser`  |  `ReActOutputParser`  |  The react output parser  |  `<llama_index.core.agent.react.output_parser.ReActOutputParser object at 0x7f00a8743a10>`  |  
|  `formatter`  |  `ReActChatFormatter`  |  The react chat formatter to format the reasoning steps and chat history into an llm input.  |  `<dynamic>`  |  
Source code in `llama-index-core/llama_index/core/agent/workflow/react_agent.py`  
| 
```
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
```
 | 
```
classReActAgent(BaseWorkflowAgent):
"""React agent implementation."""

    reasoning_key: str = "current_reasoning"
    output_parser: ReActOutputParser = Field(
        default_factory=ReActOutputParser, description="The react output parser"
    )
    formatter: ReActChatFormatter = Field(
        default_factory=default_formatter,
        description="The react chat formatter to format the reasoning steps and chat history into an llm input.",
    )

    @model_validator(mode="after")
    defvalidate_formatter(self) -> "ReActAgent":
"""Validate the formatter."""
        if (
            self.formatter.context
            and self.system_prompt
            and self.system_prompt not in self.formatter.context
        ):
            self.formatter.context = (
                self.system_prompt + "\n\n" + self.formatter.context.strip()
            )
        elif not self.formatter.context and self.system_prompt:
            self.formatter.context = self.system_prompt

        if self.formatter.context and "{context}" not in self.formatter.system_header:
            self.formatter.system_header = CONTEXT_REACT_CHAT_SYSTEM_HEADER

        return self

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        # TODO: the ReAct formatter does not explicitly specify PromptTemplate
        # objects, but wrap it in this to obey the interface
        react_header = self.formatter.system_header
        return {"react_header": PromptTemplate(react_header)}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "react_header" in prompts:
            react_header = prompts["react_header"]
            if isinstance(react_header, str):
                react_header = PromptTemplate(react_header)
            self.formatter.system_header = react_header.format()

    async def_get_response(self, current_llm_input: List[ChatMessage]) -> ChatResponse:
        return await self.llm.achat(current_llm_input)

    async def_get_streaming_response(
        self, ctx: AgentContext, current_llm_input: List[ChatMessage]
    ) -> ChatResponse:
        response = await self.llm.astream_chat(
            current_llm_input,
        )

        # last_chat_response will be used later, after the loop.
        # We initialize it so it's valid even when 'response' is empty
        last_chat_response = ChatResponse(message=ChatMessage())
        async for last_chat_response in response:
            raw = (
                last_chat_response.raw.model_dump()
                if isinstance(last_chat_response.raw, BaseModel)
                else last_chat_response.raw
            )
            # some code paths (namely react agent via llm.predict_and_call for non function calling llms) pass through a context without starting the workflow.
            # They do so in order to conform to the interface, and share state between tools, however the events are discarded and not exposed to the caller,
            # so just don't write events if the context is not running.
            if ctx.is_running:
                ctx.write_event_to_stream(
                    AgentStream(
                        delta=last_chat_response.delta or "",
                        response=last_chat_response.message.content or "",
                        raw=raw,
                        current_agent_name=self.name,
                        thinking_delta=last_chat_response.additional_kwargs.get(
                            "thinking_delta", None
                        ),
                    )
                )

        return last_chat_response

    async deftake_step(
        self,
        ctx: AgentContext,
        llm_input: List[ChatMessage],
        tools: Sequence[AsyncBaseTool],
        memory: BaseMemory,
    ) -> AgentOutput:
"""Take a single step with the React agent."""
        # remove system prompt, since the react prompt will be combined with it
        if llm_input[0].role == "system":
            system_prompt = llm_input[0].content or ""
            llm_input = llm_input[1:]
        else:
            system_prompt = ""

        output_parser = self.output_parser
        react_chat_formatter = self.formatter

        # Format initial chat input
        current_reasoning: list[BaseReasoningStep] = await ctx.store.get(
            self.reasoning_key, default=[]
        )
        input_chat = react_chat_formatter.format(
            tools,
            chat_history=llm_input,
            current_reasoning=current_reasoning,
        )
        # some code paths (namely react agent via llm.predict_and_call for non function calling llms) pass through a context without starting the workflow.
        # They do so in order to conform to the interface, and share state between tools, however the events are discarded and not exposed to the caller,
        # so just don't write events if the context is not running.
        if ctx.is_running:
            ctx.write_event_to_stream(
                AgentInput(input=input_chat, current_agent_name=self.name)
            )

        # Initial LLM call
        if self.streaming:
            last_chat_response = await self._get_streaming_response(ctx, input_chat)
        else:
            last_chat_response = await self._get_response(input_chat)

        # Parse reasoning step and check if done
        message_content = last_chat_response.message.content
        if not message_content:
            error_msg = (
                "FAILURE: Your previous response was empty.\n"
                "You must output a thought and an action/answer.\n\n"
                "Please follow this structure exactly:\n"
                "Thought: <what you are thinking>\n"
                "Action: <tool_name>\n"
                "Action Input: <json_params>\n\n"
                "OR:\n\n"
                "Thought: <what you are thinking>\n"
                "Answer: <your final response to the user>"
            )
            raw = (
                last_chat_response.raw.model_dump()
                if isinstance(last_chat_response.raw, BaseModel)
                else last_chat_response.raw
            )

            return AgentOutput(
                response=last_chat_response.message,
                raw=raw,
                current_agent_name=self.name,
                retry_messages=[
                    last_chat_response.message,
                    ChatMessage(role="user", content=error_msg),
                ],
            )

        try:
            reasoning_step = output_parser.parse(message_content, is_streaming=False)
        except ValueError as e:
            error_msg = (
                f"Error while parsing the output: {e!s}\n\n"
                "The output should be in one of the following formats:\n"
                "1. To call a tool:\n"
                "```\n"
                "Thought: <thought>\n"
                "Action: <action>\n"
                "Action Input: <action_input>\n"
                "```\n"
                "2. To answer the question:\n"
                "```\n"
                "Thought: <thought>\n"
                "Answer: <answer>\n"
                "```\n"
            )

            raw = (
                last_chat_response.raw.model_dump()
                if isinstance(last_chat_response.raw, BaseModel)
                else last_chat_response.raw
            )
            # Return with retry messages to let the LLM fix the error
            return AgentOutput(
                response=last_chat_response.message,
                raw=raw,
                current_agent_name=self.name,
                retry_messages=[
                    last_chat_response.message,
                    ChatMessage(role="user", content=error_msg),
                ],
            )

        # add to reasoning if not a handoff
        current_reasoning.append(reasoning_step)
        await ctx.store.set(self.reasoning_key, current_reasoning)

        # If response step, we're done
        raw = (
            last_chat_response.raw.model_dump()
            if isinstance(last_chat_response.raw, BaseModel)
            else last_chat_response.raw
        )
        if reasoning_step.is_done:
            return AgentOutput(
                response=last_chat_response.message,
                raw=raw,
                current_agent_name=self.name,
            )

        reasoning_step = cast(ActionReasoningStep, reasoning_step)
        if not isinstance(reasoning_step, ActionReasoningStep):
            raise ValueError(f"Expected ActionReasoningStep, got {reasoning_step}")

        # Create tool call
        tool_calls = [
            ToolSelection(
                tool_id=str(uuid.uuid4()),
                tool_name=reasoning_step.action,
                tool_kwargs=reasoning_step.action_input,
            )
        ]

        return AgentOutput(
            response=last_chat_response.message,
            tool_calls=tool_calls,
            raw=raw,
            current_agent_name=self.name,
        )

    async defhandle_tool_call_results(
        self, ctx: Context, results: List[ToolCallResult], memory: BaseMemory
    ) -> None:
"""Handle tool call results for React agent."""
        current_reasoning: list[BaseReasoningStep] = await ctx.store.get(
            self.reasoning_key, default=[]
        )
        for tool_call_result in results:
            obs_step = ObservationReasoningStep(
                observation=str(tool_call_result.tool_output.content),
                return_direct=tool_call_result.return_direct,
            )
            current_reasoning.append(obs_step)

            if (
                tool_call_result.return_direct
                and tool_call_result.tool_name != "handoff"
            ):
                current_reasoning.append(
                    ResponseReasoningStep(
                        thought=obs_step.observation,
                        response=obs_step.observation,
                        is_streaming=False,
                    )
                )
                break

        await ctx.store.set(self.reasoning_key, current_reasoning)

    async deffinalize(
        self, ctx: Context, output: AgentOutput, memory: BaseMemory
    ) -> AgentOutput:
"""Finalize the React agent."""
        current_reasoning: list[BaseReasoningStep] = await ctx.store.get(
            self.reasoning_key, default=[]
        )

        if len(current_reasoning)  0 and isinstance(
            current_reasoning[-1], ResponseReasoningStep
        ):
            reasoning_str = "\n".join([x.get_content() for x in current_reasoning])

            if reasoning_str:
                reasoning_msg = ChatMessage(role="assistant", content=reasoning_str)
                await memory.aput(reasoning_msg)
                await ctx.store.set(self.reasoning_key, [])

            # Find the text block in the response to modify it directly
            text_block = None
            for block in output.response.blocks:
                if isinstance(block, TextBlock):
                    text_block = block
                    break

            # remove "Answer:" from the response (now checking text_block.text)
            if text_block and "Answer:" in text_block.text:
                start_idx = text_block.text.find("Answer:")
                if start_idx != -1:
                    # Modify the .text attribute of the block, NOT response.content
                    text_block.text = text_block.text[
                        start_idx + len("Answer:") :
                    ].strip()

            # clear scratchpad
            await ctx.store.set(self.reasoning_key, [])

        return output

```
 |  
| --- | --- |  
###  validate_formatter [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.ReActAgent.validate_formatter "Permanent link")

```
validate_formatter() -> 

```

Validate the formatter.
Source code in `llama-index-core/llama_index/core/agent/workflow/react_agent.py`  
| 
```
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
```
 | 
```
@model_validator(mode="after")
defvalidate_formatter(self) -> "ReActAgent":
"""Validate the formatter."""
    if (
        self.formatter.context
        and self.system_prompt
        and self.system_prompt not in self.formatter.context
    ):
        self.formatter.context = (
            self.system_prompt + "\n\n" + self.formatter.context.strip()
        )
    elif not self.formatter.context and self.system_prompt:
        self.formatter.context = self.system_prompt

    if self.formatter.context and "{context}" not in self.formatter.system_header:
        self.formatter.system_header = CONTEXT_REACT_CHAT_SYSTEM_HEADER

    return self

```
 |  
| --- | --- |  
###  take_step [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.ReActAgent.take_step "Permanent link")

```
take_step(
    ctx: ,
    llm_input: [],
    tools: Sequence[],
    memory: ,
) -> 

```

Take a single step with the React agent.
Source code in `llama-index-core/llama_index/core/agent/workflow/react_agent.py`  
| 
```
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
```
 | 
```
async deftake_step(
    self,
    ctx: AgentContext,
    llm_input: List[ChatMessage],
    tools: Sequence[AsyncBaseTool],
    memory: BaseMemory,
) -> AgentOutput:
"""Take a single step with the React agent."""
    # remove system prompt, since the react prompt will be combined with it
    if llm_input[0].role == "system":
        system_prompt = llm_input[0].content or ""
        llm_input = llm_input[1:]
    else:
        system_prompt = ""

    output_parser = self.output_parser
    react_chat_formatter = self.formatter

    # Format initial chat input
    current_reasoning: list[BaseReasoningStep] = await ctx.store.get(
        self.reasoning_key, default=[]
    )
    input_chat = react_chat_formatter.format(
        tools,
        chat_history=llm_input,
        current_reasoning=current_reasoning,
    )
    # some code paths (namely react agent via llm.predict_and_call for non function calling llms) pass through a context without starting the workflow.
    # They do so in order to conform to the interface, and share state between tools, however the events are discarded and not exposed to the caller,
    # so just don't write events if the context is not running.
    if ctx.is_running:
        ctx.write_event_to_stream(
            AgentInput(input=input_chat, current_agent_name=self.name)
        )

    # Initial LLM call
    if self.streaming:
        last_chat_response = await self._get_streaming_response(ctx, input_chat)
    else:
        last_chat_response = await self._get_response(input_chat)

    # Parse reasoning step and check if done
    message_content = last_chat_response.message.content
    if not message_content:
        error_msg = (
            "FAILURE: Your previous response was empty.\n"
            "You must output a thought and an action/answer.\n\n"
            "Please follow this structure exactly:\n"
            "Thought: <what you are thinking>\n"
            "Action: <tool_name>\n"
            "Action Input: <json_params>\n\n"
            "OR:\n\n"
            "Thought: <what you are thinking>\n"
            "Answer: <your final response to the user>"
        )
        raw = (
            last_chat_response.raw.model_dump()
            if isinstance(last_chat_response.raw, BaseModel)
            else last_chat_response.raw
        )

        return AgentOutput(
            response=last_chat_response.message,
            raw=raw,
            current_agent_name=self.name,
            retry_messages=[
                last_chat_response.message,
                ChatMessage(role="user", content=error_msg),
            ],
        )

    try:
        reasoning_step = output_parser.parse(message_content, is_streaming=False)
    except ValueError as e:
        error_msg = (
            f"Error while parsing the output: {e!s}\n\n"
            "The output should be in one of the following formats:\n"
            "1. To call a tool:\n"
            "```\n"
            "Thought: <thought>\n"
            "Action: <action>\n"
            "Action Input: <action_input>\n"
            "```\n"
            "2. To answer the question:\n"
            "```\n"
            "Thought: <thought>\n"
            "Answer: <answer>\n"
            "```\n"
        )

        raw = (
            last_chat_response.raw.model_dump()
            if isinstance(last_chat_response.raw, BaseModel)
            else last_chat_response.raw
        )
        # Return with retry messages to let the LLM fix the error
        return AgentOutput(
            response=last_chat_response.message,
            raw=raw,
            current_agent_name=self.name,
            retry_messages=[
                last_chat_response.message,
                ChatMessage(role="user", content=error_msg),
            ],
        )

    # add to reasoning if not a handoff
    current_reasoning.append(reasoning_step)
    await ctx.store.set(self.reasoning_key, current_reasoning)

    # If response step, we're done
    raw = (
        last_chat_response.raw.model_dump()
        if isinstance(last_chat_response.raw, BaseModel)
        else last_chat_response.raw
    )
    if reasoning_step.is_done:
        return AgentOutput(
            response=last_chat_response.message,
            raw=raw,
            current_agent_name=self.name,
        )

    reasoning_step = cast(ActionReasoningStep, reasoning_step)
    if not isinstance(reasoning_step, ActionReasoningStep):
        raise ValueError(f"Expected ActionReasoningStep, got {reasoning_step}")

    # Create tool call
    tool_calls = [
        ToolSelection(
            tool_id=str(uuid.uuid4()),
            tool_name=reasoning_step.action,
            tool_kwargs=reasoning_step.action_input,
        )
    ]

    return AgentOutput(
        response=last_chat_response.message,
        tool_calls=tool_calls,
        raw=raw,
        current_agent_name=self.name,
    )

```
 |  
| --- | --- |  
###  handle_tool_call_results [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.ReActAgent.handle_tool_call_results "Permanent link")

```
handle_tool_call_results(
    ctx: Context,
    results: [],
    memory: ,
) -> None

```

Handle tool call results for React agent.
Source code in `llama-index-core/llama_index/core/agent/workflow/react_agent.py`  
| 
```
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
async defhandle_tool_call_results(
    self, ctx: Context, results: List[ToolCallResult], memory: BaseMemory
) -> None:
"""Handle tool call results for React agent."""
    current_reasoning: list[BaseReasoningStep] = await ctx.store.get(
        self.reasoning_key, default=[]
    )
    for tool_call_result in results:
        obs_step = ObservationReasoningStep(
            observation=str(tool_call_result.tool_output.content),
            return_direct=tool_call_result.return_direct,
        )
        current_reasoning.append(obs_step)

        if (
            tool_call_result.return_direct
            and tool_call_result.tool_name != "handoff"
        ):
            current_reasoning.append(
                ResponseReasoningStep(
                    thought=obs_step.observation,
                    response=obs_step.observation,
                    is_streaming=False,
                )
            )
            break

    await ctx.store.set(self.reasoning_key, current_reasoning)

```
 |  
| --- | --- |  
###  finalize [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.ReActAgent.finalize "Permanent link")

```
finalize(
    ctx: Context, output: , memory: 
) -> 

```

Finalize the React agent.
Source code in `llama-index-core/llama_index/core/agent/workflow/react_agent.py`  
| 
```
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
```
 | 
```
async deffinalize(
    self, ctx: Context, output: AgentOutput, memory: BaseMemory
) -> AgentOutput:
"""Finalize the React agent."""
    current_reasoning: list[BaseReasoningStep] = await ctx.store.get(
        self.reasoning_key, default=[]
    )

    if len(current_reasoning)  0 and isinstance(
        current_reasoning[-1], ResponseReasoningStep
    ):
        reasoning_str = "\n".join([x.get_content() for x in current_reasoning])

        if reasoning_str:
            reasoning_msg = ChatMessage(role="assistant", content=reasoning_str)
            await memory.aput(reasoning_msg)
            await ctx.store.set(self.reasoning_key, [])

        # Find the text block in the response to modify it directly
        text_block = None
        for block in output.response.blocks:
            if isinstance(block, TextBlock):
                text_block = block
                break

        # remove "Answer:" from the response (now checking text_block.text)
        if text_block and "Answer:" in text_block.text:
            start_idx = text_block.text.find("Answer:")
            if start_idx != -1:
                # Modify the .text attribute of the block, NOT response.content
                text_block.text = text_block.text[
                    start_idx + len("Answer:") :
                ].strip()

        # clear scratchpad
        await ctx.store.set(self.reasoning_key, [])

    return output

```
 |  
| --- | --- |  
##  AgentInput [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.AgentInput "Permanent link")
Bases: `Event`
LLM input.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `input`  |  `list[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.llms.ChatMessage\)")]`  |  _required_  |  
|  `current_agent_name`  |  _required_  |  
Source code in `llama-index-core/llama_index/core/agent/workflow/workflow_events.py`  
| 
```
24
25
26
27
28
```
 | 
```
classAgentInput(Event):
"""LLM input."""

    input: list[ChatMessage]
    current_agent_name: str

```
 |  
| --- | --- |  
##  AgentSetup [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.AgentSetup "Permanent link")
Bases: `Event`
Agent setup.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `input`  |  `list[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.llms.ChatMessage\)")]`  |  _required_  |  
|  `current_agent_name`  |  _required_  |  
Source code in `llama-index-core/llama_index/core/agent/workflow/workflow_events.py`  
| 
```
31
32
33
34
35
```
 | 
```
classAgentSetup(Event):
"""Agent setup."""

    input: list[ChatMessage]
    current_agent_name: str

```
 |  
| --- | --- |  
##  AgentStream [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.AgentStream "Permanent link")
Bases: `Event`
Agent stream.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `delta`  |  _required_  |  
|  `response`  |  _required_  |  
|  `current_agent_name`  |  _required_  |  
|  `tool_calls`  |  `list[ToolSelection[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.ToolSelection "ToolSelection \(llama_index.core.tools.ToolSelection\)")]`  |  Built-in mutable sequence. If no argument is given, the constructor creates a new empty list. The argument must be an iterable if specified.  |  `<dynamic>`  |  
|  `raw`  |  `Any | None`  |  `None`  |  
|  `thinking_delta`  |  `str | None`  |  `None`  |  
Source code in `llama-index-core/llama_index/core/agent/workflow/workflow_events.py`  
| 
```
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
classAgentStream(Event):
"""Agent stream."""

    delta: str
    response: str
    current_agent_name: str
    tool_calls: list[ToolSelection] = Field(default_factory=list)
    raw: Optional[Any] = Field(default=None, exclude=True)
    thinking_delta: Optional[str] = Field(default=None)

```
 |  
| --- | --- |  
##  AgentOutput [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.AgentOutput "Permanent link")
Bases: `Event`
LLM output.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `response`  |   |  _required_  |  
|  `structured_response`  |  `Dict[str, Any] | None`  |  `None`  |  
|  `current_agent_name`  |  _required_  |  
|  `raw`  |  `Any | None`  |  `None`  |  
|  `tool_calls`  |  `list[ToolSelection[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.llms.llm.ToolSelection "ToolSelection \(llama_index.core.tools.ToolSelection\)")]`  |  Built-in mutable sequence. If no argument is given, the constructor creates a new empty list. The argument must be an iterable if specified.  |  `<dynamic>`  |  
|  `retry_messages`  |  `list[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.llms.ChatMessage\)")]`  |  Built-in mutable sequence. If no argument is given, the constructor creates a new empty list. The argument must be an iterable if specified.  |  `<dynamic>`  |  
Source code in `llama-index-core/llama_index/core/agent/workflow/workflow_events.py`  
| 
```
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
```
 | 
```
classAgentOutput(Event):
"""LLM output."""

    response: ChatMessage
    structured_response: Optional[Dict[str, Any]] = Field(default=None)
    current_agent_name: str
    raw: Optional[Any] = Field(default=None, exclude=True)
    tool_calls: list[ToolSelection] = Field(default_factory=list)
    retry_messages: list[ChatMessage] = Field(default_factory=list)

    defget_pydantic_model(self, model: Type[BaseModel]) -> Optional[BaseModel]:
        if self.structured_response is None:
            return self.structured_response
        try:
            return model.model_validate(self.structured_response)
        except ValidationError as e:
            warnings.warn(
                f"Conversion of structured response to Pydantic model failed because:\n\n{e.title}\n\nPlease check the model you provided.",
                PydanticConversionWarning,
                stacklevel=2,
            )
            return None

    def__str__(self) -> str:
        return self.response.content or ""

```
 |  
| --- | --- |  
##  ToolCall [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.ToolCall "Permanent link")
Bases: `Event`
All tool calls are surfaced.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `tool_name`  |  _required_  |  
|  `tool_kwargs`  |  `dict`  |  _required_  |  
|  `tool_id`  |  _required_  |  
Source code in `llama-index-core/llama_index/core/agent/workflow/workflow_events.py`  
| 
```
 98
 99
100
101
102
103
```
 | 
```
classToolCall(Event):
"""All tool calls are surfaced."""

    tool_name: str
    tool_kwargs: dict
    tool_id: str

```
 |  
| --- | --- |  
##  ToolCallResult [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.ToolCallResult "Permanent link")
Bases: `Event`
Tool call result.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `tool_name`  |  _required_  |  
|  `tool_kwargs`  |  `dict`  |  _required_  |  
|  `tool_id`  |  _required_  |  
|  `tool_output`  |   |  _required_  |  
|  `return_direct`  |  `bool`  |  _required_  |  
Source code in `llama-index-core/llama_index/core/agent/workflow/workflow_events.py`  
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
```
 | 
```
classToolCallResult(Event):
"""Tool call result."""

    tool_name: str
    tool_kwargs: dict
    tool_id: str
    tool_output: ToolOutput
    return_direct: bool

```
 |  
| --- | --- |  
##  AgentStreamStructuredOutput [#](https://developers.llamaindex.ai/python/framework-api-reference/agent/#llama_index.core.agent.workflow.AgentStreamStructuredOutput "Permanent link")
Bases: `Event`
Stream the structured output
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `output`  |  `Dict[str, Any]`  |  _required_  |  
Source code in `llama-index-core/llama_index/core/agent/workflow/workflow_events.py`  
| 
```
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
```
 | 
```
classAgentStreamStructuredOutput(Event):
"""Stream the structured output"""

    output: Dict[str, Any]

    defget_pydantic_model(self, model: Type[BaseModel]) -> Optional[BaseModel]:
        if self.output is None:
            return self.output
        try:
            return model.model_validate(self.output)
        except ValidationError as e:
            warnings.warn(
                f"Conversion of structured response to Pydantic model failed because:\n\n{e.title}\n\nPlease check the model you provided.",
                PydanticConversionWarning,
                stacklevel=2,
            )
            return None

    def__str__(self) -> str:
        return json.dumps(self.output, indent=4)

```
 |  
| --- | --- |  
options: members: - AgentWorkflow - BaseWorkflowAgent - FunctionAgent - ReActAgent - CodeActAgent - AgentInput - AgentStream - AgentOutput - ToolCall - ToolCallResult
