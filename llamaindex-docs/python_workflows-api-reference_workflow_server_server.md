# Server
##  WorkflowServer [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/server/#llama_agents.server.WorkflowServer "Permanent link")

```
WorkflowServer(*, middleware: [Middleware] | None = None, exception_handlers: Mapping[, ] | None = None, workflow_store: AbstractWorkflowStore | None = None, persistence_backoff: [float] = [0.5, 3], runtime: Runtime | None = None, idle_timeout: float = 60.0, sse_heartbeat_interval: float | None = 25.0, accept_context_api:  = False)

```

HTTP server that exposes workflows as REST APIs.
Wraps one or more `Workflow` instances behind an HTTP API with endpoints for running workflows, streaming events, and sending human-in-the-loop input. Includes a built-in debugging UI served at the root path.
Example:

```
from workflows import Workflow, step
from workflows.events import StartEvent, StopEvent
from llama_agents.server import WorkflowServer

class GreetingWorkflow(Workflow):
    @step
    async def greet(self, ev: StartEvent) -> StopEvent:
        name = ev.get("name", "World")
        return StopEvent(result=f"Hello, {name}!")

server = WorkflowServer()
server.add_workflow("greet", GreetingWorkflow())

# Run with: python -m workflows.server my_server.py
# Or programmatically:
# await server.serve(host="0.0.0.0", port=8080)

```

The ASGI application is available as `server.app` for embedding in a larger application or mounting behind a reverse proxy.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `middleware`  |  `list[Middleware] | None`  |  Starlette middleware to apply to the ASGI app. Defaults to a permissive CORS configuration. Passing a custom list replaces the default entirely.  |  `None`  |  
|  `exception_handlers`  |  `Mapping[Any, Any] | None`  |  Starlette exception handlers mapping exception types to handler callables. Defaults to JSON error responses with logging. Passing a custom mapping replaces the default entirely.  |  `None`  |  
|  `workflow_store`  |  `AbstractWorkflowStore | None`  |  Persistence backend for handler state, events, and ticks. Defaults to `MemoryWorkflowStore`. Use `SqliteWorkflowStore` or `PostgresWorkflowStore` for durable persistence across restarts.  |  `None`  |  
|  `persistence_backoff`  |  `list[float]`  |  Retry delays (in seconds) when writing handler state to the store fails. Each entry is a sleep duration before the next attempt. Defaults to `[0.5, 3]` (two retries).  |  `[0.5, 3]`  |  
|  `runtime`  |  `Runtime | None`  |  Custom workflow runtime. When `None` (the default), the server builds a runtime stack that handles persistence and idle-release automatically. Only override this if you need a custom execution backend.  |  `None`  |  
|  `idle_timeout`  |  `float`  |  Seconds to wait after a workflow becomes idle before releasing it from memory. The workflow is automatically reloaded when new events arrive. Defaults to `60.0`.  |  `60.0`  |  
|  `sse_heartbeat_interval`  |  `float | None`  |  Seconds between SSE keep-alive comments (`: heartbeat`) on idle connections. Defaults to `25.0`. Set to `None` to disable heartbeats. Only applies to SSE mode; NDJSON streams are unaffected.  |  `25.0`  |  
|  `accept_context_api`  |  `bool`  |  Allow the `"context"` field in run request bodies. Defaults to `False`. Context deserialization can instantiate arbitrary Pydantic objects via `importlib`, so only enable this on trusted networks.  |  `False`  |  
Source code in `llama_agents/server/server.py`  
| 
```
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
```
 | 
```
def__init__(
    self,
    *,
    middleware: list[Middleware] | None = None,
    exception_handlers: Mapping[Any, Any] | None = None,
    workflow_store: AbstractWorkflowStore | None = None,
    persistence_backoff: list[float] = [0.5, 3],
    runtime: Runtime | None = None,
    idle_timeout: float = 60.0,
    sse_heartbeat_interval: float | None = 25.0,
    accept_context_api: bool = False,
):
"""Create a new workflow server.

    Args:
        middleware: Starlette middleware to apply to the ASGI app. Defaults
            to a permissive CORS configuration. Passing a custom list
            replaces the default entirely.
        exception_handlers: Starlette exception handlers mapping exception
            types to handler callables. Defaults to JSON error responses
            with logging. Passing a custom mapping replaces the default
            entirely.
        workflow_store: Persistence backend for handler state, events, and
            ticks. Defaults to ``MemoryWorkflowStore``. Use
            ``SqliteWorkflowStore`` or ``PostgresWorkflowStore`` for
            durable persistence across restarts.
        persistence_backoff: Retry delays (in seconds) when writing handler
            state to the store fails. Each entry is a sleep duration before
            the next attempt. Defaults to ``[0.5, 3]`` (two retries).
        runtime: Custom workflow runtime. When ``None`` (the default), the
            server builds a runtime stack that handles persistence and
            idle-release automatically. Only override this if you need a
            custom execution backend.
        idle_timeout: Seconds to wait after a workflow becomes idle before
            releasing it from memory. The workflow is automatically
            reloaded when new events arrive. Defaults to ``60.0``.
        sse_heartbeat_interval: Seconds between SSE keep-alive comments
            (``: heartbeat``) on idle connections. Defaults to ``25.0``.
            Set to ``None`` to disable heartbeats. Only applies to SSE
            mode; NDJSON streams are unaffected.
        accept_context_api: Allow the ``"context"`` field in run request
            bodies. Defaults to ``False``. Context deserialization can
            instantiate arbitrary Pydantic objects via ``importlib``, so
            only enable this on trusted networks.
    """
    self._workflow_store = (
        workflow_store if workflow_store is not None else MemoryWorkflowStore()
    )
    inner: Runtime = (
        runtime
        if runtime is not None
        else IdleReleaseDecorator(
            PersistenceDecorator(basic_runtime, store=self._workflow_store),
            store=self._workflow_store,
            idle_timeout=idle_timeout,
        )
    )
    self._runtime: ServerRuntimeDecorator = ServerRuntimeDecorator(
        inner,
        store=self._workflow_store,
        persistence_backoff=list(persistence_backoff),
    )
    self._service = _WorkflowService(
        runtime=self._runtime, store=self._workflow_store
    )

    self._api = _WorkflowAPI(
        self._service,
        middleware=middleware,
        exception_handlers=dict(exception_handlers) if exception_handlers else None,
        sse_heartbeat_interval=sse_heartbeat_interval,
        accept_context_api=accept_context_api,
    )
    self.app = self._api.app

```
 |  
| --- | --- |  
###  add_workflow [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/server/#llama_agents.server.WorkflowServer.add_workflow "Permanent link")

```
add_workflow(name: , workflow: , additional_events: [[]] | None = None) -> None

```

Register a workflow under the given name.
The workflow becomes available at `/workflows/{name}/run` and `/workflows/{name}/run-nowait`.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `name`  |  URL-safe name for the workflow.  |  _required_  |  
|  `workflow`  |   |  The workflow instance to serve.  |  _required_  |  
|  `additional_events`  |  `list[type[Event[](https://developers.llamaindex.ai/python/workflows-api-reference/events/#workflows.events.Event "            Event \(workflows.events.Event\)")]] | None`  |  Extra event types to expose in the debugger UI and `Send Event` functionality. Use this for events that aren't discoverable from step signatures alone (e.g. events consumed via `ctx.wait_for_event()`).  |  `None`  |  
Source code in `llama_agents/server/server.py`  
| 
```
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
```
 | 
```
defadd_workflow(
    self,
    name: str,
    workflow: Workflow,
    additional_events: list[type[Event]] | None = None,
) -> None:
"""Register a workflow under the given name.

    The workflow becomes available at ``/workflows/{name}/run`` and
    ``/workflows/{name}/run-nowait``.

    Args:
        name: URL-safe name for the workflow.
        workflow: The workflow instance to serve.
        additional_events: Extra event types to expose in the debugger UI
            and ``Send Event`` functionality. Use this for events that
            aren't discoverable from step signatures alone (e.g. events
            consumed via ``ctx.wait_for_event()``).
    """
    workflow._switch_workflow_name(name)
    workflow._switch_runtime(self._runtime)

    if additional_events is not None:
        self._api.register_additional_events(name, additional_events)

```
 |  
| --- | --- |  
###  get_workflows [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/server/#llama_agents.server.WorkflowServer.get_workflows "Permanent link")

```
get_workflows() -> [, ]

```

Return registered workflows as a dict by name. Only available after start().
Source code in `llama_agents/server/server.py`  
| 
```
163
164
165
166
167
168
169
```
 | 
```
defget_workflows(self) -> dict[str, Workflow]:
"""Return registered workflows as a dict by name. Only available after start()."""
    return {
        n: wf
        for n in self._service.get_workflow_names()
        if (wf := self._service.get_workflow(n)) is not None
    }

```
 |  
| --- | --- |  
###  start [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/server/#llama_agents.server.WorkflowServer.start "Permanent link")

```
start() -> 

```

Resumes previously running workflows, if they were not complete at last shutdown.
Idle workflows are not resumed - they remain released and will be loaded on-demand when events arrive for them.
Source code in `llama_agents/server/server.py`  
| 
```
175
176
177
178
179
180
181
182
```
 | 
```
async defstart(self) -> WorkflowServer:
"""Resumes previously running workflows, if they were not complete at last shutdown.

    Idle workflows are not resumed - they remain released and will be
    loaded on-demand when events arrive for them.
    """
    await self._service.start()
    return self

```
 |  
| --- | --- |  
###  contextmanager [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/server/#llama_agents.server.WorkflowServer.contextmanager "Permanent link")

```
contextmanager() -> AsyncGenerator[, None]

```

Use this server as a context manager to start and stop it
Source code in `llama_agents/server/server.py`  
| 
```
184
185
186
187
188
189
190
191
```
 | 
```
@asynccontextmanager
async defcontextmanager(self) -> AsyncGenerator[WorkflowServer, None]:
"""Use this server as a context manager to start and stop it"""
    await self.start()
    try:
        yield self
    finally:
        await self.stop()

```
 |  
| --- | --- |  
###  stop [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/server/#llama_agents.server.WorkflowServer.stop "Permanent link")

```
stop() -> None

```

Gracefully shut down all running workflow handlers.
Source code in `llama_agents/server/server.py`  
| 
```
193
194
195
```
 | 
```
async defstop(self) -> None:
"""Gracefully shut down all running workflow handlers."""
    await self._service.stop()

```
 |  
| --- | --- |  
###  serve [#](https://developers.llamaindex.ai/python/workflows-api-reference/workflow_server/server/#llama_agents.server.WorkflowServer.serve "Permanent link")

```
serve(host:  = 'localhost', port:  = 80, uvicorn_config: [, ] | None = None) -> None

```

Start the HTTP server and block until shutdown.
Calls `start()` internally before serving.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `host`  |  Bind address. Defaults to `"localhost"`.  |  `'localhost'`  |  
|  `port`  |  Bind port. Defaults to `80`.  |  
|  `uvicorn_config`  |  `dict[str, Any] | None`  |  Additional keyword arguments forwarded to `uvicorn.Config` (e.g. `root_path`, `log_level`).  |  `None`  |  
Source code in `llama_agents/server/server.py`  
| 
```
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
```
 | 
```
async defserve(
    self,
    host: str = "localhost",
    port: int = 80,
    uvicorn_config: dict[str, Any] | None = None,
) -> None:
"""Start the HTTP server and block until shutdown.

    Calls ``start()`` internally before serving.

    Args:
        host: Bind address. Defaults to ``"localhost"``.
        port: Bind port. Defaults to ``80``.
        uvicorn_config: Additional keyword arguments forwarded to
            ``uvicorn.Config`` (e.g. ``root_path``, ``log_level``).
    """
    uvicorn_config = uvicorn_config or {}

    config = uvicorn.Config(self.app, host=host, port=port, **uvicorn_config)
    server = uvicorn.Server(config)
    logger.info(
        f"Starting Workflow server at http://{host}:{port}{uvicorn_config.get('root_path','/')}"
    )

    await server.serve()

```
 |  
| --- | --- |
