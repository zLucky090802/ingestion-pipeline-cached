[Skip to content](https://developers.llamaindex.ai/python/llamaagents/llamactl/workflow-api/#_top)
LlamaAgents
llamactl
[Serving your Workflows](https://developers.llamaindex.ai/python/llamaagents/llamactl/workflow-api/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Serving your Workflows
LlamaAgents runs your LlamaIndex workflows locally and in the cloud. Author your workflows, add minimal configuration, and `llamactl` wraps them in an application server that exposes them as HTTP APIs.
## Learn the basics (LlamaIndex Workflows)
[Section titled “Learn the basics (LlamaIndex Workflows)”](https://developers.llamaindex.ai/python/llamaagents/llamactl/workflow-api/#learn-the-basics-llamaindex-workflows)
LlamaAgents is built on top of LlamaIndex workflows. If you’re new to workflows, start here: [LlamaIndex Workflows](https://developers.llamaindex.ai/python/llamaagents/workflows).
## Author a workflow (quick example)
[Section titled “Author a workflow (quick example)”](https://developers.llamaindex.ai/python/llamaagents/llamactl/workflow-api/#author-a-workflow-quick-example)
src/app/workflows.py
```


from llama_index.core.workflow import Workflow, step, StartEvent, StopEvent





classQuestionFlow(Workflow):




@step




asyncdefgenerate(self, ev: StartEvent) -> StopEvent:




question = ev.question




return StopEvent(result=f"Answer to {question}")





qa_workflow = QuestionFlow(timeout=120)


```

## Configure workflows for LlamaAgents to serve
[Section titled “Configure workflows for LlamaAgents to serve”](https://developers.llamaindex.ai/python/llamaagents/llamactl/workflow-api/#configure-workflows-for-llamaagents-to-serve)
The app server reads workflows configured in your `pyproject.toml` and makes them available under their configured names.
Define workflow instances in your code, then reference them in your config.
pyproject.toml
```


[project]




name = "app"



# ...



[tool.llamaagents.workflows]




answer-question = "app.workflows:qa_workflow"


```

## How serving works (local and cloud)
[Section titled “How serving works (local and cloud)”](https://developers.llamaindex.ai/python/llamaagents/llamactl/workflow-api/#how-serving-works-local-and-cloud)
  * `llamactl serve` discovers your config. See [`llamactl serve`](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-serve/).
  * The app server loads your workflows.
  * HTTP routes are exposed under `/deployments/{name}`. In development, `{name}` defaults to your Python project name and is configurable. On deploy, you can set a new name; a short random suffix may be appended to ensure uniqueness.
  * Workflow instances are registered under the specified name. For example, `POST /deployments/app/workflows/answer-question/run` runs the workflow above.
  * If you configure a UI, it runs alongside your API (proxied in dev, static in preview). For details, see [UI build and dev integration](https://developers.llamaindex.ai/python/llamaagents/llamactl/ui-build).


During development, the API is available at `http://localhost:4501`. After you deploy to LlamaCloud, it is available at `https://api.cloud.llamaindex.ai`.
### Authorization
[Section titled “Authorization”](https://developers.llamaindex.ai/python/llamaagents/llamactl/workflow-api/#authorization)
During local development, the API is unprotected. After deployment, your API uses the same authorization as LlamaCloud. Create an API token in the same project as the agent to make requests. For example:
Terminal window
```


curl'https://api.cloud.llamaindex.ai/deployments/app-xyz123/workflows/answer-question/run'\




-H'Authorization: Bearer llx-xxx'\




-H'Content-Type: application/json'\




--data'{"start_event": {"question": "What is the capital of France?"}}'


```

## Workflow HTTP API
[Section titled “Workflow HTTP API”](https://developers.llamaindex.ai/python/llamaagents/llamactl/workflow-api/#workflow-http-api)
When using a `WorkflowServer`, the app server exposes your workflows as an API. View the OpenAPI reference at `/deployments/<name>/docs`.
This API allows you to:
  * Retrieve details about registered workflows
  * Trigger runs of your workflows
  * Stream published events from your workflows, and retrieve final results from them
  * Send events to in-progress workflows (for example, HITL scenarios).


During development, visit `http://localhost:4501/debugger` to test and observe your workflows in a UI.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


