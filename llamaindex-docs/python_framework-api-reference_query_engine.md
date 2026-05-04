# Index
Base query engine.
##  BaseQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/query_engine/#llama_index.core.base.base_query_engine.BaseQueryEngine "Permanent link")
Bases: `PromptMixin`, `DispatcherSpanMixin`
Base query engine.
Source code in `llama-index-core/llama_index/core/base/base_query_engine.py`  
| 
```
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
```
 | 
```
classBaseQueryEngine(PromptMixin, DispatcherSpanMixin):
"""Base query engine."""

    def__init__(
        self,
        callback_manager: Optional[CallbackManager],
    ) -> None:
        self.callback_manager = callback_manager or CallbackManager([])

    def_get_prompts(self) -> Dict[str, Any]:
"""Get prompts."""
        return {}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""

    @dispatcher.span
    defquery(self, str_or_query_bundle: QueryType) -> RESPONSE_TYPE:
        dispatcher.event(QueryStartEvent(query=str_or_query_bundle))
        with self.callback_manager.as_trace("query"):
            if isinstance(str_or_query_bundle, str):
                str_or_query_bundle = QueryBundle(str_or_query_bundle)
            query_result = self._query(str_or_query_bundle)
        dispatcher.event(
            QueryEndEvent(query=str_or_query_bundle, response=query_result)
        )
        return query_result

    @dispatcher.span
    async defaquery(self, str_or_query_bundle: QueryType) -> RESPONSE_TYPE:
        dispatcher.event(QueryStartEvent(query=str_or_query_bundle))
        with self.callback_manager.as_trace("query"):
            if isinstance(str_or_query_bundle, str):
                str_or_query_bundle = QueryBundle(str_or_query_bundle)
            query_result = await self._aquery(str_or_query_bundle)
        dispatcher.event(
            QueryEndEvent(query=str_or_query_bundle, response=query_result)
        )
        return query_result

    defretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        raise NotImplementedError(
            "This query engine does not support retrieve, use query directly"
        )

    defsynthesize(
        self,
        query_bundle: QueryBundle,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
    ) -> RESPONSE_TYPE:
        raise NotImplementedError(
            "This query engine does not support synthesize, use query directly"
        )

    async defasynthesize(
        self,
        query_bundle: QueryBundle,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
    ) -> RESPONSE_TYPE:
        raise NotImplementedError(
            "This query engine does not support asynthesize, use aquery directly"
        )

    @abstractmethod
    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        pass

    @abstractmethod
    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        pass

```
 |  
| --- | --- |
