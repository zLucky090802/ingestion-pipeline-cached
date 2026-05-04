# Tool spec
Base tool spec class.
##  BaseToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/tool_spec/#llama_index.core.tools.tool_spec.base.BaseToolSpec "Permanent link")
Base tool spec class.
Source code in `llama-index-core/llama_index/core/tools/tool_spec/base.py`  
| 
```
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
114
115
```
 | 
```
classBaseToolSpec:
"""Base tool spec class."""

    # list of functions that you'd want to convert to spec
    spec_functions: List[SPEC_FUNCTION_TYPE]

    defget_fn_schema_from_fn_name(
        self, fn_name: str, spec_functions: Optional[List[SPEC_FUNCTION_TYPE]] = None
    ) -> Optional[Type[BaseModel]]:
"""
        NOTE: This function is deprecated and kept only for backwards compatibility.

        Return map from function name.

        Return type is Optional, meaning that the schema can be None.
        In this case, it's up to the downstream tool implementation to infer the schema.

        """
        return None

    defget_metadata_from_fn_name(
        self, fn_name: str, spec_functions: Optional[List[SPEC_FUNCTION_TYPE]] = None
    ) -> Optional[ToolMetadata]:
"""
        NOTE: This function is deprecated and kept only for backwards compatibility.

        Return map from function name.

        Return type is Optional, meaning that the schema can be None.
        In this case, it's up to the downstream tool implementation to infer the schema.

        """
        schema = self.get_fn_schema_from_fn_name(fn_name, spec_functions=spec_functions)
        if schema is None:
            return None

        func = getattr(self, fn_name)
        name = fn_name
        docstring = func.__doc__ or ""

        description = f"{name}{signature(func)}\n{docstring}"
        fn_schema = self.get_fn_schema_from_fn_name(
            fn_name, spec_functions=spec_functions
        )
        return ToolMetadata(name=name, description=description, fn_schema=fn_schema)

    defto_tool_list(
        self,
        spec_functions: Optional[List[SPEC_FUNCTION_TYPE]] = None,
        func_to_metadata_mapping: Optional[Dict[str, ToolMetadata]] = None,
    ) -> List[FunctionTool]:
"""Convert tool spec to list of tools."""
        spec_functions = spec_functions or self.spec_functions
        func_to_metadata_mapping = func_to_metadata_mapping or {}
        tool_list = []
        for func_spec in spec_functions:
            func_sync = None
            func_async = None
            if isinstance(func_spec, str):
                func = getattr(self, func_spec)
                if inspect.iscoroutinefunction(func):
                    func_async = func
                else:
                    func_sync = func
                metadata = func_to_metadata_mapping.get(func_spec, None)
                if metadata is None:
                    metadata = self.get_metadata_from_fn_name(func_spec)
            elif isinstance(func_spec, tuple) and len(func_spec) == 2:
                func_sync = getattr(self, func_spec[0])
                func_async = getattr(self, func_spec[1])
                metadata = func_to_metadata_mapping.get(func_spec[0], None)
                if metadata is None:
                    metadata = func_to_metadata_mapping.get(func_spec[1], None)
                    if metadata is None:
                        metadata = self.get_metadata_from_fn_name(func_spec[0])
            else:
                raise ValueError(
                    "spec_functions must be of type: List[Union[str, Tuple[str, str]]]"
                )

            tool = FunctionTool.from_defaults(
                fn=func_sync,
                async_fn=func_async,
                tool_metadata=metadata,
            )
            tool_list.append(tool)
        return tool_list

    async defto_tool_list_async(
        self,
        spec_functions: Optional[List[SPEC_FUNCTION_TYPE]] = None,
        func_to_metadata_mapping: Optional[Dict[str, ToolMetadata]] = None,
    ) -> List[FunctionTool]:
"""Asynchronously convert a tool spec to a list of tools."""
        return await asyncio.to_thread(
            self.to_tool_list, spec_functions, func_to_metadata_mapping
        )

```
 |  
| --- | --- |  
###  get_fn_schema_from_fn_name [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/tool_spec/#llama_index.core.tools.tool_spec.base.BaseToolSpec.get_fn_schema_from_fn_name "Permanent link")

```
get_fn_schema_from_fn_name(
    fn_name: ,
    spec_functions: Optional[
        [SPEC_FUNCTION_TYPE]
    ] = None,
) -> Optional[[BaseModel]]

```

NOTE: This function is deprecated and kept only for backwards compatibility.
Return map from function name.
Return type is Optional, meaning that the schema can be None. In this case, it's up to the downstream tool implementation to infer the schema.
Source code in `llama-index-core/llama_index/core/tools/tool_spec/base.py`  
| 
```
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
```
 | 
```
defget_fn_schema_from_fn_name(
    self, fn_name: str, spec_functions: Optional[List[SPEC_FUNCTION_TYPE]] = None
) -> Optional[Type[BaseModel]]:
"""
    NOTE: This function is deprecated and kept only for backwards compatibility.

    Return map from function name.

    Return type is Optional, meaning that the schema can be None.
    In this case, it's up to the downstream tool implementation to infer the schema.

    """
    return None

```
 |  
| --- | --- |  
###  get_metadata_from_fn_name [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/tool_spec/#llama_index.core.tools.tool_spec.base.BaseToolSpec.get_metadata_from_fn_name "Permanent link")

```
get_metadata_from_fn_name(
    fn_name: ,
    spec_functions: Optional[
        [SPEC_FUNCTION_TYPE]
    ] = None,
) -> Optional[]

```

NOTE: This function is deprecated and kept only for backwards compatibility.
Return map from function name.
Return type is Optional, meaning that the schema can be None. In this case, it's up to the downstream tool implementation to infer the schema.
Source code in `llama-index-core/llama_index/core/tools/tool_spec/base.py`  
| 
```
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
```
 | 
```
defget_metadata_from_fn_name(
    self, fn_name: str, spec_functions: Optional[List[SPEC_FUNCTION_TYPE]] = None
) -> Optional[ToolMetadata]:
"""
    NOTE: This function is deprecated and kept only for backwards compatibility.

    Return map from function name.

    Return type is Optional, meaning that the schema can be None.
    In this case, it's up to the downstream tool implementation to infer the schema.

    """
    schema = self.get_fn_schema_from_fn_name(fn_name, spec_functions=spec_functions)
    if schema is None:
        return None

    func = getattr(self, fn_name)
    name = fn_name
    docstring = func.__doc__ or ""

    description = f"{name}{signature(func)}\n{docstring}"
    fn_schema = self.get_fn_schema_from_fn_name(
        fn_name, spec_functions=spec_functions
    )
    return ToolMetadata(name=name, description=description, fn_schema=fn_schema)

```
 |  
| --- | --- |  
###  to_tool_list [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/tool_spec/#llama_index.core.tools.tool_spec.base.BaseToolSpec.to_tool_list "Permanent link")

```
to_tool_list(
    spec_functions: Optional[
        [SPEC_FUNCTION_TYPE]
    ] = None,
    func_to_metadata_mapping: Optional[
        [, ]
    ] = None,
) -> []

```

Convert tool spec to list of tools.
Source code in `llama-index-core/llama_index/core/tools/tool_spec/base.py`  
| 
```
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
```
 | 
```
defto_tool_list(
    self,
    spec_functions: Optional[List[SPEC_FUNCTION_TYPE]] = None,
    func_to_metadata_mapping: Optional[Dict[str, ToolMetadata]] = None,
) -> List[FunctionTool]:
"""Convert tool spec to list of tools."""
    spec_functions = spec_functions or self.spec_functions
    func_to_metadata_mapping = func_to_metadata_mapping or {}
    tool_list = []
    for func_spec in spec_functions:
        func_sync = None
        func_async = None
        if isinstance(func_spec, str):
            func = getattr(self, func_spec)
            if inspect.iscoroutinefunction(func):
                func_async = func
            else:
                func_sync = func
            metadata = func_to_metadata_mapping.get(func_spec, None)
            if metadata is None:
                metadata = self.get_metadata_from_fn_name(func_spec)
        elif isinstance(func_spec, tuple) and len(func_spec) == 2:
            func_sync = getattr(self, func_spec[0])
            func_async = getattr(self, func_spec[1])
            metadata = func_to_metadata_mapping.get(func_spec[0], None)
            if metadata is None:
                metadata = func_to_metadata_mapping.get(func_spec[1], None)
                if metadata is None:
                    metadata = self.get_metadata_from_fn_name(func_spec[0])
        else:
            raise ValueError(
                "spec_functions must be of type: List[Union[str, Tuple[str, str]]]"
            )

        tool = FunctionTool.from_defaults(
            fn=func_sync,
            async_fn=func_async,
            tool_metadata=metadata,
        )
        tool_list.append(tool)
    return tool_list

```
 |  
| --- | --- |  
###  to_tool_list_async [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/tool_spec/#llama_index.core.tools.tool_spec.base.BaseToolSpec.to_tool_list_async "Permanent link")

```
to_tool_list_async(
    spec_functions: Optional[
        [SPEC_FUNCTION_TYPE]
    ] = None,
    func_to_metadata_mapping: Optional[
        [, ]
    ] = None,
) -> []

```

Asynchronously convert a tool spec to a list of tools.
Source code in `llama-index-core/llama_index/core/tools/tool_spec/base.py`  
| 
```
107
108
109
110
111
112
113
114
115
```
 | 
```
async defto_tool_list_async(
    self,
    spec_functions: Optional[List[SPEC_FUNCTION_TYPE]] = None,
    func_to_metadata_mapping: Optional[Dict[str, ToolMetadata]] = None,
) -> List[FunctionTool]:
"""Asynchronously convert a tool spec to a list of tools."""
    return await asyncio.to_thread(
        self.to_tool_list, spec_functions, func_to_metadata_mapping
    )

```
 |  
| --- | --- |  
options: members: - BaseToolSpec
