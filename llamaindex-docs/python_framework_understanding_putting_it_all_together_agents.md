[Skip to content](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/agents/#_top)
LlamaIndex Framework
Learn
Putting It All Together
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Agents
Putting together an agent in LlamaIndex can be done by defining a set of tools and providing them to our ReActAgent or FunctionAgent implementation. We’re using it here with OpenAI, but it can be used with any sufficiently capable LLM.
In general, FunctionAgent should be preferred for LLMs that have built-in function calling/tools in their API, like Openai, Anthropic, Gemini, etc.

```


from llama_index.core.tools import FunctionTool




from llama_index.llms.openai import OpenAI




from llama_index.core.agent.workflow import ReActAgent, FunctionAgent





# define sample Tool



defmultiply(a: int, b: int) -> int:




"""Multiply two integers and returns the result integer"""




return* b





# initialize llm



llm = OpenAI(model="gpt-4o")




# initialize agent



agent = FunctionAgent(




tools=[multiply],




system_prompt="You are an agent that can invoke a tool for multiplication when assisting a user.",



```

These tools can be Python functions as shown above, or they can be LlamaIndex query engines:

```


from llama_index.core.tools import QueryEngineTool





query_engine_tools = [




QueryEngineTool.from_defaults(




query_engine=sql_agent,




name="sql_agent",




description="Agent that can execute SQL queries.",







agent = FunctionAgent(




tools=query_engine_tools,




system_prompt="You are an agent that can invoke an agent for text-to-SQL execution.",



```

You can learn more in our [Agent Module Guide](https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents) or in our [end-to-end agent tutorial](https://developers.llamaindex.ai/python/framework/understanding/agent).
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


