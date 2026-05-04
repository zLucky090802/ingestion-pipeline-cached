[Skip to content](https://developers.llamaindex.ai/python/llamaagents/workflows/concurrent_execution/#_top)
LlamaAgents
Agent Workflows
[Concurrent execution of workflows](https://developers.llamaindex.ai/python/llamaagents/workflows/concurrent_execution/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Concurrent execution of workflows
In addition to looping, branching, and streaming, workflows can run steps concurrently. This is useful when you have multiple steps that can be run independently of each other and they have time-consuming operations that they `await`, allowing other steps to run in parallel.
## Emitting multiple events
[Section titled “Emitting multiple events”](https://developers.llamaindex.ai/python/llamaagents/workflows/concurrent_execution/#emitting-multiple-events)
To emit multiple events to trigger multiple steps, you can use `ctx.send_event()`:

```


import asyncio




import random




from workflows import Workflow, Context, step




from workflows.events import Event, StartEvent, StopEvent





classStepTwoEvent(Event):




query: str





classParallelFlow(Workflow):




@step




asyncdefstart(self, ctx: Context, ev: StartEvent) -> StepTwoEvent |None:




ctx.send_event(StepTwoEvent(query="Query 1"))




ctx.send_event(StepTwoEvent(query="Query 2"))




ctx.send_event(StepTwoEvent(query="Query 3"))





@step(num_workers=4)




asyncdefstep_two(self, ev: StepTwoEvent) -> StopEvent:




print("Running slow query ", ev.query)




await asyncio.sleep(random.randint(0, 5))





return StopEvent(result=ev.query)


```

In this example, our `start` step emits 3 `StepTwoEvent`s. The `step_two` step is decorated with `num_workers=4`, which tells the workflow to run up to 4 instances of this step concurrently (this is the default).
## Collecting events
[Section titled “Collecting events”](https://developers.llamaindex.ai/python/llamaagents/workflows/concurrent_execution/#collecting-events)
If you execute the previous example, you’ll note that the workflow stops after whichever query is first to complete. Sometimes that’s useful, but other times you’ll want to wait for all your slow operations to complete before moving on to another step. You can do this using `collect_events`:

```


import asyncio




import random




from workflows import Workflow, Context, step




from workflows.events import Event, StartEvent, StopEvent





classStepTwoEvent(Event):




query: str





classStepThreeEvent(Event):




result: str





classConcurrentFlow(Workflow):




@step




asyncdefstart(self, ctx: Context, ev: StartEvent) -> StepTwoEvent |None:




ctx.send_event(StepTwoEvent(query="Query 1"))




ctx.send_event(StepTwoEvent(query="Query 2"))




ctx.send_event(StepTwoEvent(query="Query 3"))





@step(num_workers=4)




asyncdefstep_two(self, ctx: Context, ev: StepTwoEvent) -> StepThreeEvent:




print("Running query ", ev.query)




await asyncio.sleep(random.randint(1, 5))




return StepThreeEvent(result=ev.query)





@step




asyncdefstep_three(




self, ctx: Context, ev: StepThreeEvent




) -> StopEvent |None:




# wait until we receive 3 events




result = ctx.collect_events(ev, [StepThreeEvent] *3)




if result isNone:




returnNone





# do something with all 3 results together




print(result)




return StopEvent(result="Done")


```

The `collect_events` method lives on the `Context` and takes the event that triggered the step and an array of event types to wait for. In this case, we are awaiting 3 events of the same `StepThreeEvent` type.
The `step_three` step is fired every time a `StepThreeEvent` is received, but `collect_events` will return `None` until all 3 events have been received. At that point, the step will continue and you can do something with all 3 results together.
The `result` returned from `collect_events` is an array of the events that were collected, in the order that they were received.
## Multiple event types
[Section titled “Multiple event types”](https://developers.llamaindex.ai/python/llamaagents/workflows/concurrent_execution/#multiple-event-types)
Of course, you do not need to wait for the same type of event. You can wait for any combination of events you like, such as in this example:

```


import asyncio




from workflows import Workflow, Context, step




from workflows.events import Event, StartEvent, StopEvent





classStepAEvent(Event):




query: str





classStepBEvent(Event):




query: str





classStepCEvent(Event):




query: str





classStepACompleteEvent(Event):




result: str





classStepBCompleteEvent(Event):




result: str





classStepCCompleteEvent(Event):




result: str






classConcurrentFlow(Workflow):




@step




asyncdefstart(




self, ctx: Context, ev: StartEvent




) -> StepAEvent | StepBEvent | StepCEvent |None:




ctx.send_event(StepAEvent(query="Query 1"))




ctx.send_event(StepBEvent(query="Query 2"))




ctx.send_event(StepCEvent(query="Query 3"))





@step




asyncdefstep_a(self, ctx: Context, ev: StepAEvent) -> StepACompleteEvent:




print("Doing something A-ish")




return StepACompleteEvent(result=ev.query)





@step




asyncdefstep_b(self, ctx: Context, ev: StepBEvent) -> StepBCompleteEvent:




print("Doing something B-ish")




return StepBCompleteEvent(result=ev.query)





@step




asyncdefstep_c(self, ctx: Context, ev: StepCEvent) -> StepCCompleteEvent:




print("Doing something C-ish")




return StepCCompleteEvent(result=ev.query)





@step




asyncdefstep_three(




self,




ctx: Context,




ev: StepACompleteEvent | StepBCompleteEvent | StepCCompleteEvent,




) -> StopEvent:




print("Received event ", ev.result)





# wait until we receive 3 events





ctx.collect_events(





[StepCCompleteEvent, StepACompleteEvent, StepBCompleteEvent],





isNone





returnNone





# do something with all 3 results together




return StopEvent(result="Done")


```

There are several changes we’ve made to handle multiple event types:
  * `start` is now declared as emitting 3 different event types
  * `step_three` is now declared as accepting 3 different event types
  * `collect_events` now takes an array of the event types to wait for


Note that the order of the event types in the array passed to `collect_events` is important. The events will be returned in the order they are passed to `collect_events`, regardless of when they were received.
The visualization of this workflow is quite pleasing:
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


