[Skip to content](https://developers.llamaindex.ai/python/llamaagents/workflows/dbos/#_top)
LlamaAgents
Agent Workflows
[DBOS Durable Execution](https://developers.llamaindex.ai/python/llamaagents/workflows/dbos/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# DBOS Durable Execution
The [durable workflows](https://developers.llamaindex.ai/python/llamaagents/workflows/durable_workflows) page shows how to make workflows survive restarts and errors using manual context snapshots. The `llama-agents-dbos` package removes that manual work by plugging a [DBOS](https://www.dbos.dev/)-backed runtime into your workflows. Every step transition is persisted automatically, so a crashed workflow resumes exactly where it left off — no snapshot code required.
## Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/llamaagents/workflows/dbos/#installation)
Terminal window
```


pipinstallllama-agents-dbos


```

## Quick Start — Standalone Durable Workflow
[Section titled “Quick Start — Standalone Durable Workflow”](https://developers.llamaindex.ai/python/llamaagents/workflows/dbos/#quick-start--standalone-durable-workflow)
The simplest way to use DBOS is with SQLite (zero external dependencies). Define a workflow as usual, pass a `DBOSRuntime`, and your state is persisted automatically.

```


import asyncio





from dbos importDBOS




from llama_agents.dbos import DBOSRuntime




from pydantic import Field




from workflows import Context, Workflow, step




from workflows.events import Event, StartEvent, StopEvent





# 1. Configure DBOS — SQLite by default



DBOS(config={"name": "counter-example", "run_admin_server": False})





# 2. Define events and workflow (nothing DBOS-specific here)



classTick(Event):




count: int= Field(description="Current count")






classCounterResult(StopEvent):




final_count: int= Field(description="Final counter value")






classCounterWorkflow(Workflow):




@step




asyncdefstart(self, ctx: Context, ev: StartEvent) -> Tick:




await ctx.store.set("count", 0)




print("[Start] Initializing counter to 0")




return Tick(count=0)





@step




asyncdefincrement(self, ctx: Context, ev: Tick) -> Tick | CounterResult:




count = ev.count +1




await ctx.store.set("count", count)




print(f"[Tick {count:2d}] count = {count}")





if count >=20:




return CounterResult(final_count=count)





await asyncio.sleep(0.5)




return Tick(count=count)





# 3. Create runtime, attach to workflow, and launch



runtime = DBOSRuntime()




workflow = CounterWorkflow(runtime=runtime)






asyncdefmain() -> None:




await runtime.launch()




result =await workflow.run(run_id="counter-run-1")




print(f"Result: final_count = {result.final_count}")





asyncio.run(main())

```

If you kill the process mid-run (e.g. Ctrl+C at tick 8), calling `workflow.run(run_id="counter-run-1")` again will resume from tick 8 instead of restarting from zero.  
| Persists over `run` calls  | ✅  |  
| --- | --- |  
| Persists over process restarts  | ✅  |  
| Survives runtime errors  | ✅  |  
## Durable Workflow Server
[Section titled “Durable Workflow Server”](https://developers.llamaindex.ai/python/llamaagents/workflows/dbos/#durable-workflow-server)
`DBOSRuntime` integrates with `WorkflowServer` so every workflow you serve gets durable execution out of the box. The runtime provides both the persistence store and the server runtime:

```


import asyncio





from dbos importDBOS




from llama_agents.dbos import DBOSRuntime




from llama_agents.server import WorkflowServer




from pydantic import Field




from workflows import Context, Workflow, step




from workflows.events import Event, StartEvent, StopEvent





DBOS(config={"name": "quickstart", "run_admin_server": False})






classTick(Event):




count: int= Field(description="Current count")






classCounterResult(StopEvent):




final_count: int= Field(description="Final counter value")






classCounterWorkflow(Workflow):




"""Counts to 5, emitting stream events along the way."""





@step




asyncdefstart(self, ctx: Context, ev: StartEvent) -> Tick:




return Tick(count=0)





@step




asyncdeftick(self, ctx: Context, ev: Tick) -> Tick | CounterResult:




count = ev.count +1




ctx.write_event_to_stream(Tick(count=count))




print(f"  tick {count}")




await asyncio.sleep(0.5)




if count >=5:




return CounterResult(final_count=count)




return Tick(count=count)






asyncdefmain() -> None:




runtime = DBOSRuntime()





server = WorkflowServer(




workflow_store=runtime.create_workflow_store(),




runtime=runtime.build_server_runtime(),





server.add_workflow("counter", CounterWorkflow(runtime=runtime))





print("Serving on http://localhost:8000")




print("Try: curl -X POST http://localhost:8000/workflows/counter/run")




await server.start()





await server.serve(host="0.0.0.0", port=8000)




finally:




await server.stop()





asyncio.run(main())

```

The workflow debugger UI at `http://localhost:8000/` works exactly the same as with the default runtime — DBOS is transparent to the server layer.
## Idle Release
[Section titled “Idle Release”](https://developers.llamaindex.ai/python/llamaagents/workflows/dbos/#idle-release)
Long-running workflows that wait for external input (human-in-the-loop, webhooks, etc.) can sit idle in memory for extended periods. The `idle_timeout` parameter tells the DBOS runtime to release idle workflows from memory and resume them automatically when new events arrive:

```


import asyncio





from dbos importDBOS




from llama_agents.dbos import DBOSRuntime




from llama_agents.server import WorkflowServer




from pydantic import Field




from workflows import Context, Workflow, step




from workflows.events import (




HumanResponseEvent,




InputRequiredEvent,




StartEvent,




StopEvent,






DBOS(config={"name": "idle-release-demo", "run_admin_server": False})






classAskName(InputRequiredEvent):




prompt: str= Field(default="What is your name?")






classUserInput(HumanResponseEvent):




response: str= Field(default="")






classGreeterWorkflow(Workflow):




@step




asyncdefask(self, ctx: Context, ev: StartEvent) -> AskName:




return AskName()





@step




asyncdefgreet(self, ctx: Context, ev: UserInput) -> StopEvent:




return StopEvent(result={"greeting": f"Hello, {ev.response}!"})






asyncdefmain() -> None:




runtime = DBOSRuntime()





server = WorkflowServer(




workflow_store=runtime.create_workflow_store(),




# Release workflows after 30 seconds of inactivity




runtime=runtime.build_server_runtime(idle_timeout=30.0),





server.add_workflow("greeter", GreeterWorkflow(runtime=runtime))





await server.start()





await server.serve(host="0.0.0.0", port=8000)




finally:




await server.stop()





asyncio.run(main())

```

When the greeter workflow emits `AskName` and no input arrives within 30 seconds, the runtime releases it from memory. Once a `UserInput` event is sent (via `POST /events/{handler_id}`), the runtime transparently restores the workflow from the database and delivers the event. The caller never knows the workflow was released.
## Using Postgres for Multi-Replica Deployments
[Section titled “Using Postgres for Multi-Replica Deployments”](https://developers.llamaindex.ai/python/llamaagents/workflows/dbos/#using-postgres-for-multi-replica-deployments)
SQLite works well for single-process setups. For production deployments that need multiple server replicas, switch to Postgres. Each replica must have a unique `executor_id`:

```


from dbos importDBOS





DBOS(config={




"name": "my-app",




"system_database_url": "postgresql://user:pass@localhost:5432/mydb",




"run_admin_server": False,




"executor_id": "replica-1"# unique per replica



```

See the `examples/dbos/server_replicas.py` example for a complete multi-replica demo. For a deeper look at how replicas coordinate, see the [DBOS architecture overview](https://docs.dbos.dev/architecture).
For production multi-replica deployments, [DBOS Conductor](https://docs.dbos.dev/production/conductor) adds auto-scaling and monitoring dashboards on top of the core runtime.
## Execution Model
[Section titled “Execution Model”](https://developers.llamaindex.ai/python/llamaagents/workflows/dbos/#execution-model)
Understanding the DBOS execution model helps you write workflows that behave correctly across restarts and replicas.
### Replica ownership
[Section titled “Replica ownership”](https://developers.llamaindex.ai/python/llamaagents/workflows/dbos/#replica-ownership)
Each replica is identified by its `executor_id` and **owns** every workflow it starts. A workflow and all of its steps run in the same process — there is no distribution of individual steps across replicas. This means your steps can safely rely on local state like in-memory caches, local files, or process-level singletons. The trade-off is that a single workflow’s workload cannot be spread across multiple replicas.
### Journaling and replay
[Section titled “Journaling and replay”](https://developers.llamaindex.ai/python/llamaagents/workflows/dbos/#journaling-and-replay)
Step completions and stream events are journaled to the database. When a workflow resumes after a crash or an idle release, the runtime replays the journal to rebuild the workflow’s `Context` and `store`, then continues from the last recorded step.
Because recovery is replay-based, **steps may execute more than once** if they were interrupted before the journal entry was committed. Design steps to be idempotent where possible, or use the context store to track progress within a step (as shown in the [durable workflows](https://developers.llamaindex.ai/python/llamaagents/workflows/durable_workflows) page).
### Scaling and draining
[Section titled “Scaling and draining”](https://developers.llamaindex.ai/python/llamaagents/workflows/dbos/#scaling-and-draining)
Replica IDs and replica counts must be stable. If you scale down and remove a replica, any workflows that replica owned will be abandoned until that `executor_id` comes back. Before removing a replica, drain it by letting its in-flight workflows complete and not routing new work to it.
[DBOS Conductor](https://docs.dbos.dev/production/conductor) handles this automatically — it detects drained or timed-out replicas via heartbeats and re-assigns their in-flight workflows to healthy replicas.
### Code changes and versioning
[Section titled “Code changes and versioning”](https://developers.llamaindex.ai/python/llamaagents/workflows/dbos/#code-changes-and-versioning)
Since resumption is based on journal replay, changing a workflow’s code while historical runs are still in progress can cause non-determinism — for example, a step that now accepts a different set of events than when the run was originally started. To avoid this:
  * **Drain in-flight workflows** before deploying code changes, or
  * **Register the updated workflow under a new name** so that old runs continue against the original code and new runs use the updated version


A workflow’s name defaults to its module-qualified class name (e.g. `my_app.CounterWorkflow`). You can set it explicitly with the `workflow_name` parameter:

```


wf = CounterWorkflow(runtime=runtime, workflow_name="counter-v2")


```

When using a server, the name passed to `add_workflow` is the HTTP route name, independent of the workflow’s internal name:

```


server.add_workflow("counter-v2", CounterWorkflow(runtime=runtime, workflow_name="counter-v2"))


```

### Event streaming behavior
[Section titled “Event streaming behavior”](https://developers.llamaindex.ai/python/llamaagents/workflows/dbos/#event-streaming-behavior)
When using `handler.stream_events()` in-process (outside of a server), DBOS streams are replayed from the beginning on each call. This means you will receive all events the workflow has ever emitted, not just new ones.
The [workflow server](https://developers.llamaindex.ai/python/llamaagents/workflows/deployment) uses a cursor-based approach instead — its `GET /events/{handler_id}` endpoint tracks position so each consumer only receives events once.
### Crash recovery
[Section titled “Crash recovery”](https://developers.llamaindex.ai/python/llamaagents/workflows/dbos/#crash-recovery)
When a replica restarts, DBOS automatically detects and relaunches any incomplete workflows belonging to its `executor_id`. No manual intervention is required — the replica picks up where it left off by replaying its journal.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


