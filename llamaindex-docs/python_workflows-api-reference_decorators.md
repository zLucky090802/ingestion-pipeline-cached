# Decorators
##  step [#](https://developers.llamaindex.ai/python/workflows-api-reference/decorators/#workflows.decorators.step "Permanent link")

```
step(func: Callable[, ]) -> StepFunction[, ]

```


```
step(*, workflow: ['Workflow'] | None = None, num_workers:  = 4, retry_policy:  | None = None, skip_graph_checks: [StepGraphCheck] | None = None) -> Callable[[Callable[, ]], StepFunction[, ]]

```


```
step(func: Callable[, ] | None = None, *, workflow: ['Workflow'] | None = None, num_workers:  = 4, retry_policy:  | None = None, skip_graph_checks: [StepGraphCheck] | None = None) -> Callable[[Callable[, ]], StepFunction[, ]] | StepFunction[, ]

```

Decorate a callable to declare it as a workflow step.
The decorator inspects the function signature to infer the accepted event type, return event types, optional `Context` parameter (optionally with a typed state model), and any resource injections via `typing.Annotated`.
When applied to free functions, provide the workflow class via `workflow=MyWorkflow`. For instance methods, the association is automatic.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `workflow`  |  `type[Workflow[](https://developers.llamaindex.ai/python/workflows-api-reference/workflow/#workflows.workflow.Workflow "            Workflow \(workflows.workflow.Workflow\)")] | None`  |  Workflow class to attach the free function step to. Not required for methods.  |  `None`  |  
|  `num_workers`  |  Number of workers for this step. Defaults to 4.  |  
|  `retry_policy`  |  `RetryPolicy[](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/#workflows.retry_policy.RetryPolicy "            RetryPolicy \(workflows.retry_policy.RetryPolicy\)") | None`  |  Optional retry policy for failures.  |  `None`  |  
|  `skip_graph_checks`  |  `list[str] | None`  |  Graph validation checks to skip for this step. Currently supports `"reachability"` to allow intentionally unreachable steps.  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Callable`  |  `Callable[[Callable[P, R]], StepFunction[P, R]] | StepFunction[P, R]`  |  The original function, annotated with internal step metadata.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|   |  If signature validation fails or when decorating a free function without specifying `workflow`.  |  
Examples:
Method step:

```
classMyFlow(Workflow):
    @step
    async defstart(self, ev: StartEvent) -> StopEvent:
        return StopEvent(result="done")

```

Free function step:

```
classMyWorkflow(Workflow):
    pass

@step(workflow=MyWorkflow)
async defgenerate(ev: StartEvent) -> NextEvent: ...

```

Source code in `workflows/decorators.py`  
| 
```
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
```
 | 
```
defstep(
    func: Callable[P, R] | None = None,
    *,
    workflow: type["Workflow"] | None = None,
    num_workers: int = 4,
    retry_policy: RetryPolicy | None = None,
    skip_graph_checks: list[StepGraphCheck] | None = None,
) -> Callable[[Callable[P, R]], StepFunction[P, R]] | StepFunction[P, R]:
"""
    Decorate a callable to declare it as a workflow step.

    The decorator inspects the function signature to infer the accepted event
    type, return event types, optional `Context` parameter (optionally with a
    typed state model), and any resource injections via `typing.Annotated`.

    When applied to free functions, provide the workflow class via
    `workflow=MyWorkflow`. For instance methods, the association is automatic.

    Args:
        workflow (type[Workflow] | None): Workflow class to attach the free
            function step to. Not required for methods.
        num_workers (int): Number of workers for this step. Defaults to 4.
        retry_policy (RetryPolicy | None): Optional retry policy for failures.
        skip_graph_checks (list[str] | None): Graph validation checks to skip
            for this step. Currently supports ``"reachability"`` to allow
            intentionally unreachable steps.

    Returns:
        Callable: The original function, annotated with internal step metadata.

    Raises:
        WorkflowValidationError: If signature validation fails or when decorating
            a free function without specifying `workflow`.

    Examples:
        Method step:

        ```python
        class MyFlow(Workflow):
            @step
            async def start(self, ev: StartEvent) -> StopEvent:
                return StopEvent(result="done")
        ```

        Free function step:

        ```python
        class MyWorkflow(Workflow):
            pass

        @step(workflow=MyWorkflow)
        async def generate(ev: StartEvent) -> NextEvent: ...
        ```
    """

    defdecorator(func: Callable[P, R]) -> StepFunction[P, R]:
        localns = _capture_decorator_localns()
        return _apply_step_decorator(
            func,
            num_workers=num_workers,
            retry_policy=retry_policy,
            workflow=workflow,
            localns=localns,
            skip_graph_checks=skip_graph_checks or [],
        )

    if func is not None:
        # The decorator was used without parentheses, like `@step`
        localns = _capture_callsite_localns()
        return _apply_step_decorator(
            func,
            num_workers=num_workers,
            retry_policy=retry_policy,
            workflow=workflow,
            localns=localns,
            skip_graph_checks=skip_graph_checks or [],
        )
    return decorator

```
 |  
| --- | --- |
