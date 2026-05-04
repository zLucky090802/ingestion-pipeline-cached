[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/mcp/#_top)
LlamaIndex Framework
Component Guides
[Model Context Protocol (MCP)](https://developers.llamaindex.ai/python/framework/module_guides/mcp/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Model Context Protocol (MCP)
Model Context Protocol (MCP) is an open-source standard protocol that allows Large Language Models (LLMs) to interact with external tools and data sources through structured API calls.
MCP serves as a standardization layer for AI applications to communicate effectively with external services such as tools, databases and predefined templates. Think of MCP as a “USB-C port” for AI applications - it provides a standardized way for various tools, platforms, and data sources to connect to AI models.
## Architecture
[Section titled “Architecture”](https://developers.llamaindex.ai/python/framework/module_guides/mcp/#architecture)
MCP operates through a client-server architecture:
  * **MCP Hosts** : Applications like Claude Desktop, IDEs, or AI tools that wish to access data via MCP
  * **MCP Clients** : Protocol clients that maintain 1:1 connections with MCP servers
  * **MCP Servers** : Lightweight services that expose capabilities (tools, resources, prompts) via the standardized protocol


## Core Capabilities
[Section titled “Core Capabilities”](https://developers.llamaindex.ai/python/framework/module_guides/mcp/#core-capabilities)
MCP supports three main types of capabilities:
  1. **Tools** : Functions that can be invoked with structured inputs
  2. **Resources** : Data sources that can be read (files, databases, etc.)
  3. **Prompts** : Reusable prompt templates with parameters


## With LlamaIndex
[Section titled “With LlamaIndex”](https://developers.llamaindex.ai/python/framework/module_guides/mcp/#with-llamaindex)
With LlamaIndex, there are a number of ways you can use MCP servers, which allows you to bring additional resources and functionality your agentic workflows.
  * **Use existing MCP servers tools with LlamaIndex workflows** : Get data from external resources that are served via existing MCP servers.
  * **Serve LlamaIndex workflows as MCP servers** : You can convert your own custom LlamaIndex workflows to MCP servers.
  * **Use LlamaCloud services within LlamaIndex workflows** : Run one of our MCP servers (both in Python and Typescript) that serve LlamaCloud functionality such as LlamaExtract or LlamaParse, within any other application that communicates with MCP servers, including LlamaIndex workflows


## Next Steps
[Section titled “Next Steps”](https://developers.llamaindex.ai/python/framework/module_guides/mcp/#next-steps)
  * [Using MCP Tools with LlamaIndex](https://developers.llamaindex.ai/python/framework/module_guides/mcp/llamaindex_mcp)
  * [Use LlamaCloud APIs as MCP Tools/Servers](https://developers.llamaindex.ai/python/framework/module_guides/mcp/llamacloud_mcp)
  * [Use any existing LlamaIndex workflow/tool as an MCP Tool/Server](https://developers.llamaindex.ai/python/framework/module_guides/mcp/convert_existing)


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


