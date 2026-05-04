# Span types
Bases: `BaseModel`
Base data class representing a span.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `id_`  |  Id of span.  |  `'be9fe8a0-49a3-4816-96f7-3c3728e883fb'`  |  
|  `parent_id`  |  `str | None`  |  Id of parent span.  |  `None`  |  
|  `tags`  |  `Dict[str, Any]`  |  
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/span/base.py`  
| 
```
 7
 8
 9
10
11
12
13
```
 | 
```
classBaseSpan(BaseModel):
"""Base data class representing a span."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    id_: str = Field(default_factory=lambda: str(uuid4()), description="Id of span.")
    parent_id: Optional[str] = Field(default=None, description="Id of parent span.")
    tags: Dict[str, Any] = Field(default={})

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
