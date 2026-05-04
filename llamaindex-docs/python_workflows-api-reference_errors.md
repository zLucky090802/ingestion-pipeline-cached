# Errors
##  WorkflowValidationError [#](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.WorkflowValidationError "Permanent link")
Bases: `Exception`
Raised when the workflow configuration or step signatures are invalid.
Source code in `workflows/errors.py`  
| 
```
classWorkflowValidationError(Exception):
"""Raised when the workflow configuration or step signatures are invalid."""

```
 |  
| --- |  
##  WorkflowTimeoutError [#](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.WorkflowTimeoutError "Permanent link")
Bases: `Exception`
Raised when a workflow run exceeds the configured timeout.
Source code in `workflows/errors.py`  
| 
```
classWorkflowTimeoutError(Exception):
"""Raised when a workflow run exceeds the configured timeout."""

```
 |  
| --- |  
##  WorkflowRuntimeError [#](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.WorkflowRuntimeError "Permanent link")
Bases: `Exception`
Raised for runtime errors during step execution or event routing.
Source code in `workflows/errors.py`  
| 
```
classWorkflowRuntimeError(Exception):
"""Raised for runtime errors during step execution or event routing."""

```
 |  
| --- |  
##  WorkflowDone [#](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.WorkflowDone "Permanent link")
Bases: `Exception`
Internal control-flow exception used to terminate workers at run end.
Source code in `workflows/errors.py`  
| 
```
classWorkflowDone(Exception):
"""Internal control-flow exception used to terminate workers at run end."""

```
 |  
| --- |  
##  WorkflowCancelledByUser [#](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.WorkflowCancelledByUser "Permanent link")
Bases: `Exception`
Raised when a run is cancelled via the handler or programmatically.
Source code in `workflows/errors.py`  
| 
```
classWorkflowCancelledByUser(Exception):
"""Raised when a run is cancelled via the handler or programmatically."""

```
 |  
| --- |  
##  WorkflowStepDoesNotExistError [#](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.WorkflowStepDoesNotExistError "Permanent link")
Bases: `Exception`
Raised when addressing a step that does not exist in the workflow.
Source code in `workflows/errors.py`  
| 
```
classWorkflowStepDoesNotExistError(Exception):
"""Raised when addressing a step that does not exist in the workflow."""

```
 |  
| --- |  
##  WorkflowConfigurationError [#](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.WorkflowConfigurationError "Permanent link")
Bases: `Exception`
Raised when a logical configuration error is detected pre-run.
Source code in `workflows/errors.py`  
| 
```
classWorkflowConfigurationError(Exception):
"""Raised when a logical configuration error is detected pre-run."""

```
 |  
| --- |  
##  ContextSerdeError [#](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.ContextSerdeError "Permanent link")
Bases: `Exception`
Raised when serializing/deserializing a `Context` fails.
Source code in `workflows/errors.py`  
| 
```
classContextSerdeError(Exception):
"""Raised when serializing/deserializing a `Context` fails."""

```
 |  
| --- |  
##  ContextStateError [#](https://developers.llamaindex.ai/python/workflows-api-reference/errors/#workflows.errors.ContextStateError "Permanent link")
Bases: `Exception`
Raised when a context method is called in the wrong state.
Context transitions between three states: - PreContext: Before workflow starts (configuration) - ExternalContext: During run, for handler/external code - InternalContext: During run, for step execution
Source code in `workflows/errors.py`  
| 
```
37
38
39
40
41
42
43
44
```
 | 
```
classContextStateError(Exception):
"""Raised when a context method is called in the wrong state.

    Context transitions between three states:
    - PreContext: Before workflow starts (configuration)
    - ExternalContext: During run, for handler/external code
    - InternalContext: During run, for step execution
    """

```
 |  
| --- | --- |
