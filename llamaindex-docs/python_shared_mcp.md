[Skip to content](https://developers.llamaindex.ai/python/shared/mcp/#_top)
# MCP Documentation Search
Connect to our hosted MCP server to search LlamaIndex documentation
As part of the LlamaIndex documentation, we serve a hosted MCP server that allows any agent to search the LlamaIndex documentation.
The hosted MCP server is available at the following URL:

```

https://developers.llamaindex.ai/mcp

```

The server ships with the following tools:
  1. `search_docs` — a basic lexical search using BM25
  2. `grep_docs` — exact search using regex
  3. `read_doc` — provides an interface to read the entire contents of any given page path


## Configure your Agent
[Section titled “Configure your Agent”](https://developers.llamaindex.ai/python/shared/mcp/#configure-your-agent)
### Cursor
[Section titled “Cursor”](https://developers.llamaindex.ai/python/shared/mcp/#cursor)
You can [click to install to cursor directly](cursor://anysphere.cursor-deeplink/mcp/install?name=llama-index-docs&config=eyJ1cmwiOiJodHRwczovL2RldmVsb3BlcnMubGxhbWFpbmRleC5haS9tY3AifQ%3D%3D) or add the following to your `mcp.json` configuration:

```



"mcpServers": {




"llama_index_docs": {




"url": "https://developers.llamaindex.ai/mcp"





```

### Claude Code
[Section titled “Claude Code”](https://developers.llamaindex.ai/python/shared/mcp/#claude-code)
Add the documentation search tools to your Claude Code agent with a single command:
Terminal window
```


claudemcpaddllama-index-docs--transporthttphttps://developers.llamaindex.ai/mcp


```

### OpenAI Codex
[Section titled “OpenAI Codex”](https://developers.llamaindex.ai/python/shared/mcp/#openai-codex)
Add the documentation search tools to your OpenAI Codex agent by adding the following section to your `config.toml`:
Terminal window
```

[mcp_servers.llama_index_docs]



url="https://developers.llamaindex.ai/mcp"


```

### LlamaIndex Agents
[Section titled “LlamaIndex Agents”](https://developers.llamaindex.ai/python/shared/mcp/#llamaindex-agents)
Install llama-index and the MCP tools package:
Terminal window
```


pipinstallllama-indexllama-index-tools-mcp


```

And then directly use the MCP tools in your agent:

```


from llama_index.core.agent import FunctionAgent, ToolCall, ToolCallResult




from llama_index.llms.openai import OpenAI




from llama_index.tools.mcp import McpToolSpec, BasicMCPClient






asyncdefmain():




client = BasicMCPClient("https://developers.llamaindex.ai/mcp")




tool_spec = McpToolSpec(client=client)




tools =await tool_spec.to_tool_list_async()





agent = FunctionAgent(




llm=OpenAI(model="gpt-4.1", api_key="sk-..."),




tools=tools,




system_prompt="You are a helpful assistant that has access to tools to search the LlamaIndex documentation."






whileTrue:




query =input("Query: ")




handler = agent.run(query)




asyncfor ev in handler.stream_events():




ifisinstance(ev, ToolCall):




print(f"Calling tool {ev.tool_name} with input {ev.tool_kwargs}")




ifisinstance(ev, ToolCallResult):




print(f"Tool {ev.tool_name} returned {ev.tool_output}")





resp =await handler




print("")




print(resp)




print("=================")





if__name__=="__main__":




import asyncio




asyncio.run(main())


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


