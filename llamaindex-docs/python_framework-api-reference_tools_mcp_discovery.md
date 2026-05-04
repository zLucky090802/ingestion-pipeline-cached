# Mcp discovery
##  MCPDiscoveryTool [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp_discovery/#llama_index.tools.mcp_discovery.MCPDiscoveryTool "Permanent link")
Bases: 
MCP Discovery Tool.
This tool queries the MCP Discovery API for autonomous tool recommendations. It accepts a natural language description of the need and returns a human-readable list of recommended MCP servers with name, category, and description.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `api_url`  |  The URL of the MCP discovery API endpoint.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-mcp-discovery/llama_index/tools/mcp_discovery/base.py`  
| 
```
 7
 8
 9
10
11
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
80
81
82
83
```
 | 
```
classMCPDiscoveryTool(BaseToolSpec):
"""
    MCP Discovery Tool.

    This tool queries the MCP Discovery API for autonomous tool recommendations.
    It accepts a natural language description of the need and returns a
    human-readable list of recommended MCP servers with name, category, and description.

    Attributes:
        api_url: The URL of the MCP discovery API endpoint.

    """

    spec_functions = ["discover_tools"]

    def__init__(self, api_url: str) -> None:
"""
        Initialize the MCP Discovery Tool.

        Args:
            api_url: The URL of the MCP discovery API endpoint.

        """
        self.api_url = api_url

    async defdiscover_tools(self, user_request: str, limit: int = 5) -> str:
"""
        Discover tools based on a natural language request.

        This method allows an agent to discover needed tools without human intervention.
        It queries the MCP discovery API with the user's request and returns formatted
        tool recommendations.

        Args:
            user_request: Natural language description of the tool needed.
            limit: Maximum number of tool recommendations to return. Defaults to 5.

        Returns:
            A formatted string containing the discovered tools with their names,
            descriptions, and categories. Returns an error message if the request fails.

        Example:
            >>> tool = MCPDiscoveryTool(api_url="http://localhost:8000/api")
            >>> result = await tool.discover_tools("I need a math calculator", limit=3)
            >>> print(result)
            Found 2 tools:
            1. Name: math-calculator,
               Description: A tool for calculations,
               Category: math

        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url, json={"need": user_request, "limit": limit}
                ) as response:
                    data = await response.json()

            tools_json = data.get("recommendations", [])
            num = data.get("total_found", -1)

            if num == -1:
                tools = "Following tools are found:\n"
            else:
                tools = f"Found {num} tools:\n"

            if tools_json:
                for ind, i in enumerate(tools_json, start=1):
                    tools += f"{ind}. Name: {i.get('name')},\n"
                    tools += f"   Description: {i.get('description')},\n"
                    tools += f"   Category: {i.get('category')}\n\n"
                return tools.strip()

            return tools

        except Exception as e:
            return f"Error discovering tools: {e}"

```
 |  
| --- | --- |  
###  discover_tools [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp_discovery/#llama_index.tools.mcp_discovery.MCPDiscoveryTool.discover_tools "Permanent link")

```
discover_tools(user_request: , limit:  = 5) -> 

```

Discover tools based on a natural language request.
This method allows an agent to discover needed tools without human intervention. It queries the MCP discovery API with the user's request and returns formatted tool recommendations.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `user_request`  |  Natural language description of the tool needed.  |  _required_  |  
|  `limit`  |  Maximum number of tool recommendations to return. Defaults to 5.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  A formatted string containing the discovered tools with their names,  |  
|  descriptions, and categories. Returns an error message if the request fails.  |  
Example
> > > tool = MCPDiscoveryTool(api_url="http://localhost:8000/api") result = await tool.discover_tools("I need a math calculator", limit=3) print(result) Found 2 tools: 1. Name: math-calculator, Description: A tool for calculations, Category: math
Source code in `llama-index-integrations/tools/llama-index-tools-mcp-discovery/llama_index/tools/mcp_discovery/base.py`  
| 
```
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
```
 | 
```
async defdiscover_tools(self, user_request: str, limit: int = 5) -> str:
"""
    Discover tools based on a natural language request.

    This method allows an agent to discover needed tools without human intervention.
    It queries the MCP discovery API with the user's request and returns formatted
    tool recommendations.

    Args:
        user_request: Natural language description of the tool needed.
        limit: Maximum number of tool recommendations to return. Defaults to 5.

    Returns:
        A formatted string containing the discovered tools with their names,
        descriptions, and categories. Returns an error message if the request fails.

    Example:
        >>> tool = MCPDiscoveryTool(api_url="http://localhost:8000/api")
        >>> result = await tool.discover_tools("I need a math calculator", limit=3)
        >>> print(result)
        Found 2 tools:
        1. Name: math-calculator,
           Description: A tool for calculations,
           Category: math

    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.api_url, json={"need": user_request, "limit": limit}
            ) as response:
                data = await response.json()

        tools_json = data.get("recommendations", [])
        num = data.get("total_found", -1)

        if num == -1:
            tools = "Following tools are found:\n"
        else:
            tools = f"Found {num} tools:\n"

        if tools_json:
            for ind, i in enumerate(tools_json, start=1):
                tools += f"{ind}. Name: {i.get('name')},\n"
                tools += f"   Description: {i.get('description')},\n"
                tools += f"   Category: {i.get('category')}\n\n"
            return tools.strip()

        return tools

    except Exception as e:
        return f"Error discovering tools: {e}"

```
 |  
| --- | --- |  
options: members: - MCPDiscoveryTool
