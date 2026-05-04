[Skip to content](https://developers.llamaindex.ai/python/llamaagents/llamactl/ui-hooks/#_top)
LlamaAgents
llamactl
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Workflow React Hooks
Our React library, `@llamaindex/ui`, is the recommended way to integrate your UI with a LlamaAgents workflow server and LlamaCloud. It comes pre-installed in any of our templates containing a UI. The library provides both React hooks for custom integrations and standard components.
### Workflows Hooks
[Section titled “Workflows Hooks”](https://developers.llamaindex.ai/python/llamaagents/llamactl/ui-hooks/#workflows-hooks)
Our React hooks provide an idiomatic way to observe and interact with your LlamaAgents workflows remotely from a frontend client.
There are 4 hooks you can use:
  1. **useWorkflow** : Get actions for a specific workflow (create handlers, run to completion).
  2. **useHandler** : Get state and actions for a single handler (stream events, send events).
  3. **useHandlers** : List and monitor handlers with optional filtering.
  4. **useWorkflows** : List all available workflows.


### Client setup
[Section titled “Client setup”](https://developers.llamaindex.ai/python/llamaagents/llamactl/ui-hooks/#client-setup)
Configure the hooks with a workflow client. Wrap your app with an `ApiProvider` that points to your deployment:

```


import { ApiProvider, type ApiClients, createWorkflowsClient } from"@llamaindex/ui";





constdeploymentName=




(import.metaasany).env?.VITE_LLAMA_DEPLOY_DEPLOYMENT_NAME||"default";





constclients:ApiClients= {




workflowsClient: createWorkflowsClient({




baseUrl: `/deployments/${deploymentName}`,







exportfunctionProviders({ children }:children:React.ReactNode }) {




returnApiProviderclients={clients}>{children}</ApiProvider>;



```

### List available workflows
[Section titled “List available workflows”](https://developers.llamaindex.ai/python/llamaagents/llamactl/ui-hooks/#list-available-workflows)
Use `useWorkflows` to list all workflows available in the deployment:

```


import { useWorkflows } from"@llamaindex/ui";





exportfunctionWorkflowList() {




conststate, sync=useWorkflows();





if (state.loading) returndiv>Loading…</div>;





return (




div




buttononClick={() =>sync()}>Refresh</button





{Object.values(state.workflows).map((w) => (




likey={w.name}>{w.name}</li





</ul




</div




```

### Start a run
[Section titled “Start a run”](https://developers.llamaindex.ai/python/llamaagents/llamactl/ui-hooks/#start-a-run)
Start a workflow by name with `useWorkflow`. Call `createHandler` with a JSON input payload to get back a handler state immediately.

```


import { useState } from"react";




import { useWorkflow } from"@llamaindex/ui";





exportfunctionCreateHandler() {




constworkflow=useWorkflow("stream");




const [handlerId, setHandlerId] =useStatestring|null>(null);





asyncfunctionhandleClick() {




consthandlerState=await workflow.createHandler({});




setHandlerId(handlerState.handler_id);






return (




div




buttononClick={handleClick}>Create Handler</button




{handlerId div>Created: {handlerId}</div>}




</div




```

### Watch a run and stream events
[Section titled “Watch a run and stream events”](https://developers.llamaindex.ai/python/llamaagents/llamactl/ui-hooks/#watch-a-run-and-stream-events)
Subscribe to a handler’s live event stream using `subscribeToEvents`:

```


import { useEffect, useState } from"react";




import { useWorkflow, useHandler, WorkflowEvent, isStopEvent } from"@llamaindex/ui";





exportfunctionStreamEvents() {




constworkflow=useWorkflow("stream");




const [handlerId, setHandlerId] =useStatestring|null>(null);




consthandler=useHandler(handlerId);




const [events, setEvents] =useStateWorkflowEvent[]>([]);





asyncfunctionstart() {




setEvents([]);




consth=await workflow.createHandler({});




setHandlerId(h.handler_id);






useEffect(() => {




if (!handlerId) return;




constsub= handler.subscribeToEvents({




onData: (event) =>setEvents((prev) => [...prev, event]),





return () => sub.unsubscribe();




}, [handlerId]);





conststop= events.find(isStopEvent);





return (




div




buttononClick={start}>Start & Stream</button




{handlerId div>Status: {handler.state.status}</div>}




{stop pre>{JSON.stringify(stop.data, null, 2)}</pre>}




{!stop  events.length0div>{events.length} events received</div>}




</div




```

### Monitor multiple workflow runs
[Section titled “Monitor multiple workflow runs”](https://developers.llamaindex.ai/python/llamaagents/llamactl/ui-hooks/#monitor-multiple-workflow-runs)
Use `useHandlers` to query and monitor a filtered list of workflow handlers. This is useful for progress indicators or “Recent runs” views.

```


import { useHandlers } from"@llamaindex/ui";





exportfunctionRecentRuns() {




conststate, sync=useHandlers({




query: { status: ["running", "completed"] },






if (state.loading) returndiv>Loading…</div>;





consthandlers= Object.values(state.handlers);





return (




div




buttononClick={() =>sync()}>Refresh</button





{handlers.map((h) => (




likey={h.handler_id}>




{h.handler_id.slice(0, 8)}… — {h.status}




</li





</ul




</div




```

The `sync` option controls whether to fetch handlers on mount. Call `sync()` manually to refresh the list from the server at any time.
### Hook Reference
[Section titled “Hook Reference”](https://developers.llamaindex.ai/python/llamaagents/llamactl/ui-hooks/#hook-reference)  
| Hook  | Purpose  | Key Methods/Properties  |  
| --- | --- | --- |  
| `useWorkflow(name)`  | Work with a specific workflow  |  `createHandler(input)`, `runToCompletion(input)`, `state.graph`  |  
| `useHandler(handlerId)`  | Work with a specific handler  |  `sendEvent(event)`, `subscribeToEvents(callbacks)`, `sync()`, `state.status`, `state.result`  |  
| `useHandlers({ query, sync })`  | List/filter handlers  |  `sync()`, `setHandler(h)`, `actions(id)`, `state.handlers`  |  
| `useWorkflows({ sync })`  | List all workflows  |  `sync()`, `state.workflows`  |  
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


