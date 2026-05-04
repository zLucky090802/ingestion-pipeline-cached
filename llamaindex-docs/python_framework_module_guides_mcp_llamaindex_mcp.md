[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/mcp/llamaindex_mcp/#_top)
LlamaIndex Framework
Component Guides
[Using MCP Tools with LlamaIndex](https://developers.llamaindex.ai/python/framework/module_guides/mcp/llamaindex_mcp/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Using MCP Tools with LlamaIndex
LlamaIndex provides robust support for consuming MCP servers through the `llama-index-tools-mcp` package.
## Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/framework/module_guides/mcp/llamaindex_mcp/#installation)
Terminal window
```


pipinstallllama-index-tools-mcp


```

## Basic Usage
[Section titled “Basic Usage”](https://developers.llamaindex.ai/python/framework/module_guides/mcp/llamaindex_mcp/#basic-usage)
The most common usage will be converting an MCP server into a list of `llama-index` tool definitions:

```


from llama_index.tools.mcp import BasicMCPClient, McpToolSpec




# Connect to MCP server



mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")




mcp_tool_spec = McpToolSpec(client=mcp_client)




# Get tools



tools =await mcp_tool_spec.to_tool_list_async()


```

## Using with Agents
[Section titled “Using with Agents”](https://developers.llamaindex.ai/python/framework/module_guides/mcp/llamaindex_mcp/#using-with-agents)
Once you have a list of tools, you can plug this into any existing agent:

```


from llama_index.core.agent.workflow import FunctionAgent




from llama_index.llms.openai import OpenAI





agent = FunctionAgent(




tools=tools,




llm=OpenAI(model="gpt-5-mini"),




system_prompt="You are a helpful assistant.",






response =await agent.run("Your query here")


```

You can read more about agents in the [Agents Guide](https://developers.llamaindex.ai/python/framework/understanding/agent).
## Connection Types
[Section titled “Connection Types”](https://developers.llamaindex.ai/python/framework/module_guides/mcp/llamaindex_mcp/#connection-types)
The `BasicMCPClient` supports multiple transport methods:

```

# Server-Sent Events



sse_client = BasicMCPClient("https://example.com/sse")




# Streamable HTTP



http_client = BasicMCPClient("https://example.com/mcp")




# Local process



local_client = BasicMCPClient("python", args=["server.py"])


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


