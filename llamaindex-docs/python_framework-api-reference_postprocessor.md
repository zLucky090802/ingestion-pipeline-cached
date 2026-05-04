# Index
##  BaseNodePostprocessor [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/#llama_index.core.postprocessor.types.BaseNodePostprocessor "Permanent link")
Bases: , `DispatcherSpanMixin`, 
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `callback_manager`  |   |  Callback manager that handles callbacks for events within LlamaIndex. The callback manager provides a way to call handlers on event starts/ends. Additionally, the callback manager traces the current stack of events. It does this by using a few key attributes. - trace_stack - The current stack of events that have not ended yet. When an event ends, it's removed from the stack. Since this is a contextvar, it is unique to each thread/task. - trace_map - A mapping of event ids to their children events. On the start of events, the bottom of the trace stack is used as the current parent event for the trace map. - trace_id - A simple name for the current trace, usually denoting the entrypoint (query, index_construction, insert, etc.) Args: handlers (List[BaseCallbackHandler]): list of handlers to use. Usage: with callback_manager.event(CBEventType.QUERY) as event: event.on_start(payload={key, val}) ... event.on_end(payload={key, val})  |  `<dynamic>`  |  
Source code in `llama-index-core/llama_index/core/postprocessor/types.py`  
| 
```
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
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
```
 | 
```
classBaseNodePostprocessor(BaseComponent, DispatcherSpanMixin, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    callback_manager: CallbackManager = Field(
        default_factory=CallbackManager, exclude=True
    )

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        # set by default since most postprocessors don't require prompts
        return {}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt modules."""
        return {}

    # implement class_name so users don't have to worry about it when extending
    @classmethod
    defclass_name(cls) -> str:
        return "BaseNodePostprocessor"

    defpostprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
        query_str: Optional[str] = None,
    ) -> List[NodeWithScore]:
"""Postprocess nodes."""
        if query_str is not None and query_bundle is not None:
            raise ValueError("Cannot specify both query_str and query_bundle")
        elif query_str is not None:
            query_bundle = QueryBundle(query_str)
        else:
            pass
        return self._postprocess_nodes(nodes, query_bundle)

    @abstractmethod
    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
"""Postprocess nodes."""

    async defapostprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
        query_str: Optional[str] = None,
    ) -> List[NodeWithScore]:
"""Postprocess nodes (async)."""
        if query_str is not None and query_bundle is not None:
            raise ValueError("Cannot specify both query_str and query_bundle")
        elif query_str is not None:
            query_bundle = QueryBundle(query_str)
        else:
            pass
        return await self._apostprocess_nodes(nodes, query_bundle)

    async def_apostprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
"""Postprocess nodes (async)."""
        return await asyncio.to_thread(self._postprocess_nodes, nodes, query_bundle)

```
 |  
| --- | --- |  
###  postprocess_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/#llama_index.core.postprocessor.types.BaseNodePostprocessor.postprocess_nodes "Permanent link")

```
postprocess_nodes(
    nodes: [],
    query_bundle: Optional[] = None,
    query_str: Optional[] = None,
) -> []

```

Postprocess nodes.
Source code in `llama-index-core/llama_index/core/postprocessor/types.py`  
| 
```
35
36
37
38
39
40
41
42
43
44
45
46
47
48
```
 | 
```
defpostprocess_nodes(
    self,
    nodes: List[NodeWithScore],
    query_bundle: Optional[QueryBundle] = None,
    query_str: Optional[str] = None,
) -> List[NodeWithScore]:
"""Postprocess nodes."""
    if query_str is not None and query_bundle is not None:
        raise ValueError("Cannot specify both query_str and query_bundle")
    elif query_str is not None:
        query_bundle = QueryBundle(query_str)
    else:
        pass
    return self._postprocess_nodes(nodes, query_bundle)

```
 |  
| --- | --- |  
###  apostprocess_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/#llama_index.core.postprocessor.types.BaseNodePostprocessor.apostprocess_nodes "Permanent link")

```
apostprocess_nodes(
    nodes: [],
    query_bundle: Optional[] = None,
    query_str: Optional[] = None,
) -> []

```

Postprocess nodes (async).
Source code in `llama-index-core/llama_index/core/postprocessor/types.py`  
| 
```
58
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
```
 | 
```
async defapostprocess_nodes(
    self,
    nodes: List[NodeWithScore],
    query_bundle: Optional[QueryBundle] = None,
    query_str: Optional[str] = None,
) -> List[NodeWithScore]:
"""Postprocess nodes (async)."""
    if query_str is not None and query_bundle is not None:
        raise ValueError("Cannot specify both query_str and query_bundle")
    elif query_str is not None:
        query_bundle = QueryBundle(query_str)
    else:
        pass
    return await self._apostprocess_nodes(nodes, query_bundle)

```
 |  
| --- | --- |  
options: members: - BaseNodePostprocessor
