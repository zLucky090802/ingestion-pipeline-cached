[Skip to content](https://developers.llamaindex.ai/python/llamaagents/workflows/unbound_functions/#_top)
LlamaAgents
Agent Workflows
[Workflows from unbound functions](https://developers.llamaindex.ai/python/llamaagents/workflows/unbound_functions/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Workflows from unbound functions
Throughout these docs, we have been showing workflows defined as classes. However, this is not the only way to define a workflow: you can also define the steps in your workflow through independent or “unbound” functions and assign them to a workflow using the `@step()` decorator. Let’s see how that works.
First we create an empty class to hold the steps:

```


from workflows import Workflow





classTestWorkflow(Workflow):




pass


```

Now we can add steps to the workflow by defining functions and decorating them with the `@step()` decorator:

```


from workflows import step




from workflows.events import StartEvent, StopEvent





@step(workflow=TestWorkflow)




defsome_step(ev: StartEvent) -> StopEvent:




return StopEvent()


```

In this example, we’re adding a starting step to the `TestWorkflow` class. The `@step()` decorator takes the `workflow` argument, which is the class to which the step will be added. The function signature is the same as for a regular step, with the exception of the `workflow` argument.
You can also add steps this way to any existing workflow class! This can be handy if you just need one extra step in your workflow and don’t want to subclass an entire workflow to do it.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


