# Signnow
##  SignNowMCPToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/signnow/#llama_index.tools.signnow.SignNowMCPToolSpec "Permanent link")
Bases: 
Thin wrapper over McpToolSpec: - creates BasicMCPClient for STDIO spawn, - dynamically pulls tools from SignNow MCP server, - sugar factories: from_env.
See McpToolSpec.to_tool_list() / .to_tool_list_async() for getting FunctionTool.
Source code in `llama-index-integrations/tools/llama-index-tools-signnow/llama_index/tools/signnow/base.py`  
| 
```
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
```
 | 
```
classSignNowMCPToolSpec(BaseToolSpec):
"""
    Thin wrapper over McpToolSpec:
    - creates BasicMCPClient for STDIO spawn,
    - dynamically pulls tools from SignNow MCP server,
    - sugar factories: from_env.

    See McpToolSpec.to_tool_list() / .to_tool_list_async() for getting FunctionTool.
    """

    # Follow BaseToolSpec typing contract
    spec_functions: List[Union[str, Tuple[str, str]]] = []

    def__init__(
        self,
        client: ClientSession,
        allowed_tools: Optional[List[str]] = None,
        include_resources: bool = False,
    ) -> None:
        self._mcp_spec = McpToolSpec(
            client=client,
            allowed_tools=allowed_tools,
            include_resources=include_resources,
        )

    @classmethod
    deffrom_env(
        cls,
        *,
        allowed_tools: Optional[Iterable[str]] = None,
        include_resources: bool = False,
        env_overrides: Optional[Mapping[str, str]] = None,
        bin: Optional[str] = None,
        cmd: str = "serve",
        args: Optional[Sequence[str]] = None,
        require_in_path: bool = True,
    ) -> "SignNowMCPToolSpec":
"""
        Spawn STDIO: 'sn-mcp serve' with provided environment overrides merged
        on top of the current process environment.

        Supported variables (see server README):
          SIGNNOW_TOKEN (token-based auth)

          SIGNNOW_USER_EMAIL, SIGNNOW_PASSWORD, SIGNNOW_API_BASIC_TOKEN (credential-based auth)
          SIGNNOW_APP_BASE, SIGNNOW_API_BASE (optional, defaults can be used)

        Parameters
        ----------
          - bin: binary/command to spawn (default None → uses SIGNNOW_MCP_BIN or 'sn-mcp')
          - cmd: subcommand (default 'serve')
          - args: additional arguments for the server
          - require_in_path: validate presence of binary in PATH if not absolute

        """
        # Build env and filter to expected keys
        env_all = _merge_env(env_overrides)
        filtered = {k: v for k, v in env_all.items() if k in EXPECTED_SIGNNOW_KEYS}

        _validate_auth(filtered)

        # Resolve binary to absolute if possible
        resolved_bin = _resolve_sn_mcp_bin(bin, require_in_path=require_in_path)

        cmd_args: List[str] = [cmd]
        if args:
            cmd_args.extend(args)

        client = BasicMCPClient(resolved_bin, args=cmd_args, env=filtered)
        return cls(
            client=client,
            allowed_tools=list(allowed_tools) if allowed_tools else None,
            include_resources=include_resources,
        )

    async defto_tool_list_async(self) -> List[FunctionTool]:
"""Delegate to underlying `McpToolSpec` with error handling."""
        result = await self._mcp_spec.to_tool_list_async()
        return cast(List[FunctionTool], result)

    defto_tool_list(
        self,
        spec_functions: Optional[List[Union[str, Tuple[str, str]]]] = None,
        func_to_metadata_mapping: Optional[Dict[str, ToolMetadata]] = None,
    ) -> List[FunctionTool]:
"""Delegate to underlying `McpToolSpec` (sync) with error handling."""
        # We discover tools dynamically via MCP; provided parameters are ignored.
        result = self._mcp_spec.to_tool_list()
        return cast(List[FunctionTool], result)

```
 |  
| --- | --- |  
###  from_env `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/signnow/#llama_index.tools.signnow.SignNowMCPToolSpec.from_env "Permanent link")

```
from_env(
    *,
    allowed_tools: Optional[Iterable[]] = None,
    include_resources:  = False,
    env_overrides: Optional[Mapping[, ]] = None,
    bin: Optional[] = None,
    cmd:  = "serve",
    args: Optional[Sequence[]] = None,
    require_in_path:  = True
) -> 

```

Spawn STDIO: 'sn-mcp serve' with provided environment overrides merged on top of the current process environment.
Supported variables (see server README): SIGNNOW_TOKEN (token-based auth) OR SIGNNOW_USER_EMAIL, SIGNNOW_PASSWORD, SIGNNOW_API_BASIC_TOKEN (credential-based auth) SIGNNOW_APP_BASE, SIGNNOW_API_BASE (optional, defaults can be used)
##### Parameters[#](https://developers.llamaindex.ai/python/framework-api-reference/tools/signnow/#llama_index.tools.signnow.SignNowMCPToolSpec.from_env--parameters "Permanent link")
  * bin: binary/command to spawn (default None → uses SIGNNOW_MCP_BIN or 'sn-mcp')
  * cmd: subcommand (default 'serve')
  * args: additional arguments for the server
  * require_in_path: validate presence of binary in PATH if not absolute

Source code in `llama-index-integrations/tools/llama-index-tools-signnow/llama_index/tools/signnow/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_env(
    cls,
    *,
    allowed_tools: Optional[Iterable[str]] = None,
    include_resources: bool = False,
    env_overrides: Optional[Mapping[str, str]] = None,
    bin: Optional[str] = None,
    cmd: str = "serve",
    args: Optional[Sequence[str]] = None,
    require_in_path: bool = True,
) -> "SignNowMCPToolSpec":
"""
    Spawn STDIO: 'sn-mcp serve' with provided environment overrides merged
    on top of the current process environment.

    Supported variables (see server README):
      SIGNNOW_TOKEN (token-based auth)

      SIGNNOW_USER_EMAIL, SIGNNOW_PASSWORD, SIGNNOW_API_BASIC_TOKEN (credential-based auth)
      SIGNNOW_APP_BASE, SIGNNOW_API_BASE (optional, defaults can be used)

    Parameters
    ----------
      - bin: binary/command to spawn (default None → uses SIGNNOW_MCP_BIN or 'sn-mcp')
      - cmd: subcommand (default 'serve')
      - args: additional arguments for the server
      - require_in_path: validate presence of binary in PATH if not absolute

    """
    # Build env and filter to expected keys
    env_all = _merge_env(env_overrides)
    filtered = {k: v for k, v in env_all.items() if k in EXPECTED_SIGNNOW_KEYS}

    _validate_auth(filtered)

    # Resolve binary to absolute if possible
    resolved_bin = _resolve_sn_mcp_bin(bin, require_in_path=require_in_path)

    cmd_args: List[str] = [cmd]
    if args:
        cmd_args.extend(args)

    client = BasicMCPClient(resolved_bin, args=cmd_args, env=filtered)
    return cls(
        client=client,
        allowed_tools=list(allowed_tools) if allowed_tools else None,
        include_resources=include_resources,
    )

```
 |  
| --- | --- |  
###  to_tool_list_async [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/signnow/#llama_index.tools.signnow.SignNowMCPToolSpec.to_tool_list_async "Permanent link")

```
to_tool_list_async() -> []

```

Delegate to underlying `McpToolSpec` with error handling.
Source code in `llama-index-integrations/tools/llama-index-tools-signnow/llama_index/tools/signnow/base.py`  
| 
```
141
142
143
144
```
 | 
```
async defto_tool_list_async(self) -> List[FunctionTool]:
"""Delegate to underlying `McpToolSpec` with error handling."""
    result = await self._mcp_spec.to_tool_list_async()
    return cast(List[FunctionTool], result)

```
 |  
| --- | --- |  
###  to_tool_list [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/signnow/#llama_index.tools.signnow.SignNowMCPToolSpec.to_tool_list "Permanent link")

```
to_tool_list(
    spec_functions: Optional[
        [Union[, Tuple[, ]]]
    ] = None,
    func_to_metadata_mapping: Optional[
        [, ]
    ] = None,
) -> []

```

Delegate to underlying `McpToolSpec` (sync) with error handling.
Source code in `llama-index-integrations/tools/llama-index-tools-signnow/llama_index/tools/signnow/base.py`  
| 
```
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
defto_tool_list(
    self,
    spec_functions: Optional[List[Union[str, Tuple[str, str]]]] = None,
    func_to_metadata_mapping: Optional[Dict[str, ToolMetadata]] = None,
) -> List[FunctionTool]:
"""Delegate to underlying `McpToolSpec` (sync) with error handling."""
    # We discover tools dynamically via MCP; provided parameters are ignored.
    result = self._mcp_spec.to_tool_list()
    return cast(List[FunctionTool], result)

```
 |  
| --- | --- |  
options: members: - SignNowMCPToolSpec
