# Ondemand loader
Ad-hoc data loader tool.
Tool that wraps any data loader, and is able to load data on-demand.
##  OnDemandLoaderTool [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/ondemand_loader/#llama_index.core.tools.ondemand_loader_tool.OnDemandLoaderTool "Permanent link")
Bases: 
On-demand data loader tool.
Loads data with by calling the provided loader function, stores in index, and queries for relevant data with a natural language query string.
Source code in `llama-index-core/llama_index/core/tools/ondemand_loader_tool.py`  
| 
```
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
160
161
162
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
classOnDemandLoaderTool(AsyncBaseTool):
"""
    On-demand data loader tool.

    Loads data with by calling the provided loader function,
    stores in index, and queries for relevant data with a
    natural language query string.

    """

    def__init__(
        self,
        loader: Callable[..., List[Document]],
        index_cls: Type[BaseIndex],
        index_kwargs: Dict,
        metadata: ToolMetadata,
        use_query_str_in_loader: bool = False,
        query_str_kwargs_key: str = "query_str",
    ) -> None:
"""Init params."""
        self._loader = loader
        self._index_cls = index_cls
        self._index_kwargs = index_kwargs
        self._use_query_str_in_loader = use_query_str_in_loader
        self._metadata = metadata
        self._query_str_kwargs_key = query_str_kwargs_key

    @property
    defmetadata(self) -> ToolMetadata:
        return self._metadata

    @classmethod
    deffrom_defaults(
        cls,
        reader: BaseReader,
        index_cls: Optional[Type[BaseIndex]] = None,
        index_kwargs: Optional[Dict] = None,
        use_query_str_in_loader: bool = False,
        query_str_kwargs_key: str = "query_str",
        name: Optional[str] = None,
        description: Optional[str] = None,
        fn_schema: Optional[Type[BaseModel]] = None,
    ) -> "OnDemandLoaderTool":
"""From defaults."""
        # NOTE: fn_schema should be specified if you want to use as langchain Tool

        index_cls = index_cls or VectorStoreIndex
        index_kwargs = index_kwargs or {}
        if description is None:
            description = f"Tool to load data from {reader.__class__.__name__}"
        if fn_schema is None:
            fn_schema = create_schema_from_function(
                name or "LoadData",
                reader.load_data,
                [(query_str_kwargs_key, str, None)],
            )

        metadata = ToolMetadata(name=name, description=description, fn_schema=fn_schema)
        return cls(
            loader=reader.load_data,
            index_cls=index_cls,
            index_kwargs=index_kwargs,
            use_query_str_in_loader=use_query_str_in_loader,
            query_str_kwargs_key=query_str_kwargs_key,
            metadata=metadata,
        )

    @classmethod
    deffrom_tool(
        cls,
        tool: FunctionTool,
        index_cls: Optional[Type[BaseIndex]] = None,
        index_kwargs: Optional[Dict] = None,
        use_query_str_in_loader: bool = False,
        query_str_kwargs_key: str = "query_str",
        name: Optional[str] = None,
        description: Optional[str] = None,
        return_direct: bool = False,
        fn_schema: Optional[Type[BaseModel]] = None,
    ) -> "OnDemandLoaderTool":
"""From defaults."""
        # NOTE: fn_schema should be specified if you want to use as langchain Tool

        index_cls = index_cls or VectorStoreIndex
        index_kwargs = index_kwargs or {}
        if description is None:
            description = f"Tool to load data from {tool.__class__.__name__}"
        if fn_schema is None:
            fn_schema = create_schema_from_function(
                name or "LoadData", tool._fn, [(query_str_kwargs_key, str, None)]
            )
        metadata = ToolMetadata(
            name=name,
            description=description,
            fn_schema=fn_schema,
            return_direct=return_direct,
        )
        return cls(
            loader=tool._fn,
            index_cls=index_cls,
            index_kwargs=index_kwargs,
            use_query_str_in_loader=use_query_str_in_loader,
            query_str_kwargs_key=query_str_kwargs_key,
            metadata=metadata,
        )

    def_parse_args(self, *args: Any, **kwargs: Any) -> Tuple[str, List[Document]]:
        if self._query_str_kwargs_key not in kwargs:
            raise ValueError(
                "Missing query_str in kwargs with parameter name: "
                f"{self._query_str_kwargs_key}"
            )
        if self._use_query_str_in_loader:
            query_str = kwargs[self._query_str_kwargs_key]
        else:
            query_str = kwargs.pop(self._query_str_kwargs_key)

        docs = self._loader(*args, **kwargs)

        return query_str, docs

    defcall(self, *args: Any, **kwargs: Any) -> ToolOutput:
"""Call."""
        query_str, docs = self._parse_args(*args, **kwargs)

        index = self._index_cls.from_documents(docs, **self._index_kwargs)
        # TODO: add query kwargs
        query_engine = index.as_query_engine()
        response = query_engine.query(query_str)
        return ToolOutput(
            content=str(response),
            tool_name=self.metadata.get_name(),
            raw_input={"query": query_str},
            raw_output=response,
        )

    async defacall(self, *args: Any, **kwargs: Any) -> ToolOutput:
"""Async Call."""
        query_str, docs = self._parse_args(*args, **kwargs)

        index = self._index_cls.from_documents(docs, **self._index_kwargs)
        # TODO: add query kwargs
        query_engine = index.as_query_engine()
        response = await query_engine.aquery(query_str)
        return ToolOutput(
            content=str(response),
            tool_name=self.metadata.get_name(),
            raw_input={"query": query_str},
            raw_output=response,
        )

```
 |  
| --- | --- |  
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/ondemand_loader/#llama_index.core.tools.ondemand_loader_tool.OnDemandLoaderTool.from_defaults "Permanent link")

```
from_defaults(
    reader: ,
    index_cls: Optional[[]] = None,
    index_kwargs: Optional[] = None,
    use_query_str_in_loader:  = False,
    query_str_kwargs_key:  = "query_str",
    name: Optional[] = None,
    description: Optional[] = None,
    fn_schema: Optional[[BaseModel]] = None,
) -> 

```

From defaults.
Source code in `llama-index-core/llama_index/core/tools/ondemand_loader_tool.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    reader: BaseReader,
    index_cls: Optional[Type[BaseIndex]] = None,
    index_kwargs: Optional[Dict] = None,
    use_query_str_in_loader: bool = False,
    query_str_kwargs_key: str = "query_str",
    name: Optional[str] = None,
    description: Optional[str] = None,
    fn_schema: Optional[Type[BaseModel]] = None,
) -> "OnDemandLoaderTool":
"""From defaults."""
    # NOTE: fn_schema should be specified if you want to use as langchain Tool

    index_cls = index_cls or VectorStoreIndex
    index_kwargs = index_kwargs or {}
    if description is None:
        description = f"Tool to load data from {reader.__class__.__name__}"
    if fn_schema is None:
        fn_schema = create_schema_from_function(
            name or "LoadData",
            reader.load_data,
            [(query_str_kwargs_key, str, None)],
        )

    metadata = ToolMetadata(name=name, description=description, fn_schema=fn_schema)
    return cls(
        loader=reader.load_data,
        index_cls=index_cls,
        index_kwargs=index_kwargs,
        use_query_str_in_loader=use_query_str_in_loader,
        query_str_kwargs_key=query_str_kwargs_key,
        metadata=metadata,
    )

```
 |  
| --- | --- |  
###  from_tool `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/ondemand_loader/#llama_index.core.tools.ondemand_loader_tool.OnDemandLoaderTool.from_tool "Permanent link")

```
from_tool(
    tool: ,
    index_cls: Optional[[]] = None,
    index_kwargs: Optional[] = None,
    use_query_str_in_loader:  = False,
    query_str_kwargs_key:  = "query_str",
    name: Optional[] = None,
    description: Optional[] = None,
    return_direct:  = False,
    fn_schema: Optional[[BaseModel]] = None,
) -> 

```

From defaults.
Source code in `llama-index-core/llama_index/core/tools/ondemand_loader_tool.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_tool(
    cls,
    tool: FunctionTool,
    index_cls: Optional[Type[BaseIndex]] = None,
    index_kwargs: Optional[Dict] = None,
    use_query_str_in_loader: bool = False,
    query_str_kwargs_key: str = "query_str",
    name: Optional[str] = None,
    description: Optional[str] = None,
    return_direct: bool = False,
    fn_schema: Optional[Type[BaseModel]] = None,
) -> "OnDemandLoaderTool":
"""From defaults."""
    # NOTE: fn_schema should be specified if you want to use as langchain Tool

    index_cls = index_cls or VectorStoreIndex
    index_kwargs = index_kwargs or {}
    if description is None:
        description = f"Tool to load data from {tool.__class__.__name__}"
    if fn_schema is None:
        fn_schema = create_schema_from_function(
            name or "LoadData", tool._fn, [(query_str_kwargs_key, str, None)]
        )
    metadata = ToolMetadata(
        name=name,
        description=description,
        fn_schema=fn_schema,
        return_direct=return_direct,
    )
    return cls(
        loader=tool._fn,
        index_cls=index_cls,
        index_kwargs=index_kwargs,
        use_query_str_in_loader=use_query_str_in_loader,
        query_str_kwargs_key=query_str_kwargs_key,
        metadata=metadata,
    )

```
 |  
| --- | --- |  
###  call [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/ondemand_loader/#llama_index.core.tools.ondemand_loader_tool.OnDemandLoaderTool.call "Permanent link")

```
call(*args: , **kwargs: ) -> 

```

Call.
Source code in `llama-index-core/llama_index/core/tools/ondemand_loader_tool.py`  
| 
```
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
```
 | 
```
defcall(self, *args: Any, **kwargs: Any) -> ToolOutput:
"""Call."""
    query_str, docs = self._parse_args(*args, **kwargs)

    index = self._index_cls.from_documents(docs, **self._index_kwargs)
    # TODO: add query kwargs
    query_engine = index.as_query_engine()
    response = query_engine.query(query_str)
    return ToolOutput(
        content=str(response),
        tool_name=self.metadata.get_name(),
        raw_input={"query": query_str},
        raw_output=response,
    )

```
 |  
| --- | --- |  
###  acall [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/ondemand_loader/#llama_index.core.tools.ondemand_loader_tool.OnDemandLoaderTool.acall "Permanent link")

```
acall(*args: , **kwargs: ) -> 

```

Async Call.
Source code in `llama-index-core/llama_index/core/tools/ondemand_loader_tool.py`  
| 
```
156
157
158
159
160
161
162
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
async defacall(self, *args: Any, **kwargs: Any) -> ToolOutput:
"""Async Call."""
    query_str, docs = self._parse_args(*args, **kwargs)

    index = self._index_cls.from_documents(docs, **self._index_kwargs)
    # TODO: add query kwargs
    query_engine = index.as_query_engine()
    response = await query_engine.aquery(query_str)
    return ToolOutput(
        content=str(response),
        tool_name=self.metadata.get_name(),
        raw_input={"query": query_str},
        raw_output=response,
    )

```
 |  
| --- | --- |  
options: members: - OnDemandLoaderTool
