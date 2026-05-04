[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/mcp/convert_existing/#_top)
LlamaIndex Framework
Component Guides
[Converting Existing LlamaIndex Workflows & Tools to MCP](https://developers.llamaindex.ai/python/framework/module_guides/mcp/convert_existing/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Converting Existing LlamaIndex Workflows & Tools to MCP
Convert your LlamaIndex tools and workflows into MCP servers for broader ecosystem compatibility.
## Converting Workflows
[Section titled “Converting Workflows”](https://developers.llamaindex.ai/python/framework/module_guides/mcp/convert_existing/#converting-workflows)
Use `workflow_as_mcp` to convert any LlamaIndex Workflow into an [FastMCP](https://github.com/jlowin/fastmcp) server:

```


from workflows import Context, Workflow, step




from workflows.events import StartEvent, StopEvent




from llama_index.tools.mcp.utils import workflow_as_mcp






classQueryEvent(StartEvent):




query: str






classSimpleWorkflow(Workflow):




@step




defprocess_query(self, ctx: Context, ev: QueryEvent) -> StopEvent:




result =f"Processed: {ev.query}"




return StopEvent(result=result)





# Convert to MCP server



workflow = SimpleWorkflow()




mcp = workflow_as_mcp(workflow, start_event_model=QueryEvent)


```

If you were using [FastMCP](https://github.com/jlowin/fastmcp) directly, it would look something like this:

```


from fastmcp import FastMCP




# Workflow definition





mcp = FastMCP("Demo 🚀")




workflow = SimpleWorkflow()





@mcp.tool



asyncdefrun_my_workflow(input_args: QueryEvent) -> str:




"""Add two numbers"""




if isintance(input_args, dict):




input_args = QueryEvent.model_validate(input_args)




result =await workflow.run(start_event=input_args)




returnstr(result)






if__name__=="__main__":




mcp.run()


```

## Converting Individual Tools
[Section titled “Converting Individual Tools”](https://developers.llamaindex.ai/python/framework/module_guides/mcp/convert_existing/#converting-individual-tools)
We can also use FastMCP to directly convert existing functions and tools input MCP endpoints:

```


from fastmcp import FastMCP




from llama_index.tools.notion import NotionToolSpec




# Get tools from ToolSpec



tool_spec = NotionToolSpec(integration_token="your_token")




tools = tool_spec.to_tool_list()




# Create MCP server



mcp_server = FastMCP("Tool Server")




# Register tools



for tool in tools:




mcp_server.tool(




name=tool.metadata.name, description=tool.metadata.description




)(tool.real_fn)


```

## Running MCP Server
[Section titled “Running MCP Server”](https://developers.llamaindex.ai/python/framework/module_guides/mcp/convert_existing/#running-mcp-server)
You can launch your server from the CLI (which is also great for debugging!):
Terminal window
```

# Install MCP CLI



pipinstall"mcp[cli]"




# Run server



mcprunyour-server.py


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


