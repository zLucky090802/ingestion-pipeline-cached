[Skip to content](https://developers.llamaindex.ai/python/llamaagents/workflows/streaming/#_top)
LlamaAgents
Agent Workflows
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Streaming events
Workflows can be complex — they are designed to handle complex, branching, concurrent logic — which means they can take time to fully execute. To provide your user with a good experience, you may want to provide an indication of progress by streaming events as they occur. Workflows have built-in support for this on the `Context` object.
To get this done, let’s bring in all the deps we need:

```


import asyncio




from llama_index.llms.openai import OpenAI





from workflows import (




Workflow,




Context,




step,





from workflows.events import (




StartEvent,




StopEvent,




Event,



```

Let’s set up some events for a simple three-step workflow, plus an event to handle streaming our progress as we go:

```


classFirstEvent(Event):




first_output: str






classSecondEvent(Event):




second_output: str




response: str






classProgressEvent(Event):




msg: str


```

And define a workflow class that sends events:

```


classMyWorkflow(Workflow):




@step




asyncdefstep_one(self, ctx: Context, ev: StartEvent) -> FirstEvent:




ctx.write_event_to_stream(ProgressEvent(msg="Step one is happening"))




return FirstEvent(first_output="First step complete.")





@step




asyncdefstep_two(self, ctx: Context, ev: FirstEvent) -> SecondEvent:




llm = OpenAI(model="gpt-4o-mini")




generator =await llm.astream_complete(




"Please give me the first 3 paragraphs of Moby Dick, a book in the public domain."





full_resp =""




asyncfor response in generator:




# Allow the workflow to stream this piece of response




ctx.write_event_to_stream(ProgressEvent(msg=response.delta))




full_resp += response.delta





return SecondEvent(




second_output="Second step complete, full response attached",




response=full_resp,






@step




asyncdefstep_three(self, ctx: Context, ev: SecondEvent) -> StopEvent:




ctx.write_event_to_stream(ProgressEvent(msg="Step three is happening"))




return StopEvent(result="Workflow complete.")


```

In `step_one` and `step_three` we write individual events to the event stream. In `step_two` we use `astream_complete` to produce an iterable generator of the LLM’s response, then we produce an event for each chunk of data the LLM sends back to us — roughly one per word — before returning the final response to `step_three`.
To actually get this output, we need to run the workflow asynchronously and listen for the events, like this:

```


asyncdefmain():




w = MyWorkflow(timeout=30, verbose=True)




handler = w.run(first_input="Start the workflow.")





asyncfor ev in handler.stream_events():




ifisinstance(ev, ProgressEvent):




print(ev.msg)





final_result =await handler




print("Final result", final_result)






if__name__=="__main__":




asyncio.run(main())


```

`run` runs the workflow in the background, while `stream_events` will provide any event that gets written to the stream. It stops when the stream delivers a `StopEvent`, after which you can get the final result of the workflow as you normally would.
## Handling workflow termination
[Section titled “Handling workflow termination”](https://developers.llamaindex.ai/python/llamaagents/workflows/streaming/#handling-workflow-termination)
When a workflow ends abnormally (timeout, cancellation, or step failure), a specific `StopEvent` subclass is published to the stream before the exception is raised:
  * **`WorkflowTimedOutEvent`**- Published when the workflow exceeds its timeout. Contains`timeout` (seconds) and `active_steps` (list of step names that were running).
  * **`WorkflowCancelledEvent`**- Published when the workflow is cancelled by the user.
  * **`WorkflowFailedEvent`**- Published when a step fails permanently after exhausting retries. Contains`step_name` , `exception_type`, `exception_message`, `traceback`, `attempts`, and `elapsed_seconds`.



```


from workflows.events import (




WorkflowTimedOutEvent,




WorkflowCancelledEvent,




WorkflowFailedEvent,






asyncfor ev in handler.stream_events():




ifisinstance(ev, WorkflowTimedOutEvent):




print(f"Workflow timed out after {ev.timeout}s")




elifisinstance(ev, WorkflowCancelledEvent):




print("Workflow was cancelled")




elifisinstance(ev, WorkflowFailedEvent):




print(f"Step '{ev.step_name}' failed after {ev.attempts} attempts: {ev.exception_message}")


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


