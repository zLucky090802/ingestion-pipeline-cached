# Query engine
##  QueryEngineTool [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/query_engine/#llama_index.core.tools.query_engine.QueryEngineTool "Permanent link")
Bases: 
Query engine tool.
A tool making use of a query engine.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_engine`  |   |  A query engine.  |  _required_  |  
|  `metadata`  |   |  The associated metadata of the query engine.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/tools/query_engine.py`  
| 
```
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
```
 | 
```
classQueryEngineTool(AsyncBaseTool):
"""
    Query engine tool.

    A tool making use of a query engine.

    Args:
        query_engine (BaseQueryEngine): A query engine.
        metadata (ToolMetadata): The associated metadata of the query engine.

    """

    def__init__(
        self,
        query_engine: BaseQueryEngine,
        metadata: ToolMetadata,
        resolve_input_errors: bool = True,
    ) -> None:
        self._query_engine = query_engine
        self._metadata = metadata
        self._resolve_input_errors = resolve_input_errors

    @classmethod
    deffrom_defaults(
        cls,
        query_engine: BaseQueryEngine,
        name: Optional[str] = None,
        description: Optional[str] = None,
        return_direct: bool = False,
        resolve_input_errors: bool = True,
    ) -> "QueryEngineTool":
        name = name or DEFAULT_NAME
        description = description or DEFAULT_DESCRIPTION

        metadata = ToolMetadata(
            name=name, description=description, return_direct=return_direct
        )
        return cls(
            query_engine=query_engine,
            metadata=metadata,
            resolve_input_errors=resolve_input_errors,
        )

    @property
    defquery_engine(self) -> BaseQueryEngine:
        return self._query_engine

    @property
    defmetadata(self) -> ToolMetadata:
        return self._metadata

    defcall(self, *args: Any, **kwargs: Any) -> ToolOutput:
        query_str = self._get_query_str(*args, **kwargs)
        response = self._query_engine.query(query_str)
        return ToolOutput(
            content=str(response),
            tool_name=self.metadata.get_name(),
            raw_input={"input": query_str},
            raw_output=response,
        )

    async defacall(self, *args: Any, **kwargs: Any) -> ToolOutput:
        query_str = self._get_query_str(*args, **kwargs)
        response = await self._query_engine.aquery(query_str)
        return ToolOutput(
            content=str(response),
            tool_name=self.metadata.get_name(),
            raw_input={"input": query_str},
            raw_output=response,
        )

    defas_langchain_tool(self) -> "LlamaIndexTool":
        fromllama_index.core.langchain_helpers.agents.toolsimport (
            IndexToolConfig,
            LlamaIndexTool,
        )

        tool_config = IndexToolConfig(
            query_engine=self.query_engine,
            name=self.metadata.get_name(),
            description=self.metadata.description,
        )
        return LlamaIndexTool.from_tool_config(tool_config=tool_config)

    def_get_query_str(self, *args: Any, **kwargs: Any) -> str:
        if args is not None and len(args)  0:
            query_str = str(args[0])
        elif kwargs is not None and "input" in kwargs:
            # NOTE: this assumes our default function schema of `input`
            query_str = kwargs["input"]
        elif kwargs is not None and self._resolve_input_errors:
            query_str = str(kwargs)
        else:
            raise ValueError(
                "Cannot call query engine without specifying `input` parameter."
            )
        return query_str

```
 |  
| --- | --- |
