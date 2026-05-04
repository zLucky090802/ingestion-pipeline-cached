[Skip to content](https://developers.llamaindex.ai/python/llamaagents/workflows/drawing/#_top)
LlamaAgents
Agent Workflows
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Drawing a Workflow
Workflows can be visualized, using the power of type annotations in your step definitions.
There are two main ways to visualize your workflows.
## 1. Converting a Workflow to HTML
[Section titled “1. Converting a Workflow to HTML”](https://developers.llamaindex.ai/python/llamaagents/workflows/drawing/#1-converting-a-workflow-to-html)
First install:
Terminal window
```


pipinstallllama-index-utils-workflow


```

Then import and use:

```


from llama_index.utils.workflow import (




draw_all_possible_flows,




draw_most_recent_execution,





# Draw all



draw_all_possible_flows(MyWorkflow, filename="all_paths.html")




# Draw an execution



w = MyWorkflow()




handler = w.run(topic="Pirates")




await handler




draw_most_recent_execution(handler, filename="most_recent.html")


```

## 2. Using the `workflow-debugger`
[Section titled “2. Using the workflow-debugger”](https://developers.llamaindex.ai/python/llamaagents/workflows/drawing/#2-using-the-workflow-debugger)
Workflows ship with a [`WorkflowServer`](https://developers.llamaindex.ai/python/llamaagents/workflows/deployment) that allows you to convert workflows to API’s. As part of the `WorkflowServer`, a debugging UI is provided as the home `/` page.
Using this server app, you can visualize and run your workflows.
Setting up the server is straightforward:

```


import asyncio




from workflows import Workflow, step




from workflows.events import StartEvent, StopEvent




from workflows.server import WorkflowServer





classMyWorkflow(Workflow):




@step




asyncdefmy_step(self, ev: StartEvent) -> StopEvent:




return StopEvent(result="Done!")





asyncdefmain():




server = WorkflowServer()




server.add_workflow("my_workflow", MyWorkflow())




await server.serve("0.0.0.0", "8080")





if__name__=="__main__":




asyncio.run(main())


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


