[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/mcp/llamacloud_mcp/#_top)
LlamaIndex Framework
Component Guides
[LlamaCloud MCP Servers & Tools](https://developers.llamaindex.ai/python/framework/module_guides/mcp/llamacloud_mcp/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# LlamaCloud MCP Servers & Tools
LlamaIndex provides official MCP servers that integrate with LlamaCloud services like LlamaCloud Indexes and LlamaExtract.
The [`llamacloud-mcp`](https://github.com/run-llama/llamacloud-mcp) Python package provides an alternative implementation that supports both query and extraction capabilities, using LlamaCloud indexes as knowledge bases and LlamaExtract agents for structured extraction.
## Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/framework/module_guides/mcp/llamacloud_mcp/#installation)
Terminal window
```


pipinstallllamacloud-mcp




*# or*




uvxllamacloud-mcp@latest


```

## Claude Usage
[Section titled “Claude Usage”](https://developers.llamaindex.ai/python/framework/module_guides/mcp/llamacloud_mcp/#claude-usage)
To use with an MCP host like claude-code, you can set your configuration file like so:

```



"mcpServers": {




"llama_index_docs_server": {




"command": "uvx",




"args": [




"llamacloud-mcp@latest",




"--index",




"your-index-name:Description of your index",




"--index",




"your-other-index-name:Description of your other index",




"--extract-agent",




"extract-agent-name:Description of your extract agent",




"--project-name",




"<Your LlamaCloud Project Name>",




"--org-id",




"<Your LlamaCloud Org ID>",




"--api-key",




"<Your LlamaCloud API Key>"






"filesystem": {




"command": "npx",




"args": [




"-y",




"@modelcontextprotocol/server-filesystem",




"<your directory you want filesystem tool to have access to>"






```

## General Usage
[Section titled “General Usage”](https://developers.llamaindex.ai/python/framework/module_guides/mcp/llamacloud_mcp/#general-usage)
By default, the MCP server is launched with the `stdio` transport. This is useful for hosts like Claude Desktop that support MCP servers via stdin/stdout, but you can also launch the server with the `streamable-http` or `sse` transport, which is useful for hosts that support MCP servers via HTTP.
You can launch the server directly from the command line:
Terminal window
```


llamacloud-mcp--index"index-name:Description"--extract-agent"name:description"--org-idYOUR_ORG_ID--project-idYOUR_PROJECT_ID--api-keyYOUR_API_KEY--transportstreamable-http


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


