[Skip to content](https://developers.llamaindex.ai/python/llamaagents/workflows/branches_and_loops/#_top)
LlamaAgents
Agent Workflows
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Branches and loops
A key feature of Workflows is their enablement of branching and looping logic, more simply and flexibly than graph-based approaches.
## Loops in workflows
[Section titled “Loops in workflows”](https://developers.llamaindex.ai/python/llamaagents/workflows/branches_and_loops/#loops-in-workflows)
To create a loop, we’ll take a `LoopingWorkflow` that randomly loops. It will have a single event that we’ll call `LoopEvent` (but it can have any arbitrary name).

```


from workflows.events import Event





classLoopEvent(Event):




num_loops: int


```

Now we’ll `import random` and modify our `step_one` function to randomly decide either to loop or to continue:

```


import random




from workflows import Workflow, step




from workflows.events import StartEvent, StopEvent





classLoopingWorkflow(Workflow):




@step




asyncdefprepare_input(self, ev: StartEvent) -> LoopEvent:




num_loops = random.randint(0, 10)




return LoopEvent(num_loops=num_loops)





@step




asyncdefloop_step(self, ev: LoopEvent) -> LoopEvent | StopEvent:




if ev.num_loops <=0:




return StopEvent(result="Done looping!")





return LoopEvent(num_loops=ev.num_loops-1)


```

Let’s visualize this:
You can create a loop from any step to any other step by defining the appropriate event types and return types.
## Branches in workflows
[Section titled “Branches in workflows”](https://developers.llamaindex.ai/python/llamaagents/workflows/branches_and_loops/#branches-in-workflows)
Closely related to looping is branching. As you’ve already seen, you can conditionally return different events. Let’s see a workflow that branches into two different paths:

```


import random




from workflows import Workflow, step




from workflows.events import Event, StartEvent, StopEvent





classBranchA1Event(Event):




payload: str






classBranchA2Event(Event):




payload: str






classBranchB1Event(Event):




payload: str






classBranchB2Event(Event):




payload: str






classBranchWorkflow(Workflow):




@step




asyncdefstart(self, ev: StartEvent) -> BranchA1Event | BranchB1Event:




if random.randint(0, 1) ==0:




print("Go to branch A")




return BranchA1Event(payload="Branch A")




else:




print("Go to branch B")




return BranchB1Event(payload="Branch B")





@step




asyncdefstep_a1(self, ev: BranchA1Event) -> BranchA2Event:




print(ev.payload)




return BranchA2Event(payload=ev.payload)





@step




asyncdefstep_b1(self, ev: BranchB1Event) -> BranchB2Event:




print(ev.payload)




return BranchB2Event(payload=ev.payload)





@step




asyncdefstep_a2(self, ev: BranchA2Event) -> StopEvent:




print(ev.payload)




return StopEvent(result="Branch A complete.")





@step




asyncdefstep_b2(self, ev: BranchB2Event) -> StopEvent:




print(ev.payload)




return StopEvent(result="Branch B complete.")


```

Our imports are the same as before, but we’ve created 4 new event types. `start` randomly decides to take one branch or another, and then multiple steps in each branch complete the workflow. Let’s visualize this:
You can of course combine branches and loops in any order to fulfill the needs of your application. Later in this tutorial you’ll learn how to run multiple branches in parallel using `send_event` and synchronize them using `collect_events`.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


