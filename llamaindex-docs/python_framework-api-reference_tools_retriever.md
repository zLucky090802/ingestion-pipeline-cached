# Retriever
Retriever tool.
##  RetrieverTool [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/retriever/#llama_index.core.tools.retriever_tool.RetrieverTool "Permanent link")
Bases: 
Retriever tool.
A tool making use of a retriever.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `retriever`  |   |  A retriever.  |  _required_  |  
|  `metadata`  |   |  The associated metadata of the query engine.  |  _required_  |  
|  `node_postprocessors`  |  `Optional[List[BaseNodePostprocessor[](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/#llama_index.core.postprocessor.types.BaseNodePostprocessor "BaseNodePostprocessor \(llama_index.core.postprocessor.types.BaseNodePostprocessor\)")]]`  |  A list of node postprocessors.  |  `None`  |  
Source code in `llama-index-core/llama_index/core/tools/retriever_tool.py`  
| 
```
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
```
 | 
```
classRetrieverTool(AsyncBaseTool):
"""
    Retriever tool.

    A tool making use of a retriever.

    Args:
        retriever (BaseRetriever): A retriever.
        metadata (ToolMetadata): The associated metadata of the query engine.
        node_postprocessors (Optional[List[BaseNodePostprocessor]]): A list of
            node postprocessors.

    """

    def__init__(
        self,
        retriever: BaseRetriever,
        metadata: ToolMetadata,
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
    ) -> None:
        self._retriever = retriever
        self._metadata = metadata
        self._node_postprocessors = node_postprocessors or []

    @classmethod
    deffrom_defaults(
        cls,
        retriever: BaseRetriever,
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> "RetrieverTool":
        name = name or DEFAULT_NAME
        description = description or DEFAULT_DESCRIPTION

        metadata = ToolMetadata(name=name, description=description)
        return cls(
            retriever=retriever,
            metadata=metadata,
            node_postprocessors=node_postprocessors,
        )

    @property
    defretriever(self) -> BaseRetriever:
        return self._retriever

    @property
    defmetadata(self) -> ToolMetadata:
        return self._metadata

    defcall(self, *args: Any, **kwargs: Any) -> ToolOutput:
        query_str = ""
        if args is not None:
            query_str += ", ".join([str(arg) for arg in args]) + "\n"
        if kwargs is not None:
            query_str += (
                ", ".join([f"{k!s} is {v!s}" for k, v in kwargs.items()]) + "\n"
            )
        if query_str == "":
            raise ValueError("Cannot call query engine without inputs")

        docs = self._retriever.retrieve(query_str)
        docs = self._apply_node_postprocessors(docs, QueryBundle(query_str))
        content = ""
        for doc in docs:
            assert isinstance(doc.node, (Node, TextNode))
            node_copy = doc.node.model_copy()
            content += node_copy.get_content(MetadataMode.LLM) + "\n\n"
        return ToolOutput(
            content=content,
            tool_name=self.metadata.get_name(),
            raw_input={"input": query_str},
            raw_output=docs,
        )

    async defacall(self, *args: Any, **kwargs: Any) -> ToolOutput:
        query_str = ""
        if args is not None:
            query_str += ", ".join([str(arg) for arg in args]) + "\n"
        if kwargs is not None:
            query_str += (
                ", ".join([f"{k!s} is {v!s}" for k, v in kwargs.items()]) + "\n"
            )
        if query_str == "":
            raise ValueError("Cannot call query engine without inputs")
        docs = await self._retriever.aretrieve(query_str)
        content = ""
        docs = await self._async_apply_node_postprocessors(docs, QueryBundle(query_str))
        for doc in docs:
            assert isinstance(doc.node, (Node, TextNode))
            node_copy = doc.node.model_copy()
            content += node_copy.get_content(MetadataMode.LLM) + "\n\n"
        return ToolOutput(
            content=content,
            tool_name=self.metadata.get_name(),
            raw_input={"input": query_str},
            raw_output=docs,
        )

    defas_langchain_tool(self) -> "LlamaIndexTool":
        raise NotImplementedError("`as_langchain_tool` not implemented here.")

    def_apply_node_postprocessors(
        self, nodes: List[NodeWithScore], query_bundle: QueryBundle
    ) -> List[NodeWithScore]:
        for node_postprocessor in self._node_postprocessors:
            nodes = node_postprocessor.postprocess_nodes(
                nodes, query_bundle=query_bundle
            )
        return nodes

    async def_async_apply_node_postprocessors(
        self, nodes: List[NodeWithScore], query_bundle: QueryBundle
    ) -> List[NodeWithScore]:
        for node_postprocessor in self._node_postprocessors:
            nodes = await node_postprocessor.apostprocess_nodes(
                nodes, query_bundle=query_bundle
            )
        return nodes

```
 |  
| --- | --- |
