[Skip to content](https://developers.llamaindex.ai/python/framework/use_cases/agents/#_top)
LlamaIndex Framework
Use Cases
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Agents
An “agent” is an automated reasoning and decision engine. It takes in a user input/query and can make internal decisions for executing that query in order to return the correct result. The key agent components can include, but are not limited to:
  * Breaking down a complex question into smaller ones
  * Choosing an external Tool to use + coming up with parameters for calling the Tool
  * Planning out a set of tasks
  * Storing previously completed tasks in a memory module


LlamaIndex provides a comprehensive framework for building agentic systems with varying degrees of complexity:
  * **If you want to build agents quickly** : Use our prebuilt [agent](https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents) and [tool](https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/tools) architectures to rapidly setup agentic systems.
  * **If you want full control over your agentic system** : Build and deploy custom agentic workflows from scratch using our [Workflows](https://developers.llamaindex.ai/python/framework/module_guides/workflow).


## Use Cases
[Section titled “Use Cases”](https://developers.llamaindex.ai/python/framework/use_cases/agents/#use-cases)
The scope of possible use cases for agents is vast and ever-expanding. That said, here are some practical use cases that can deliver immediate value.
  * **Agentic RAG** : Build a context-augmented research assistant over your data that not only answers simple questions, but complex research tasks. Our [getting started guide](https://developers.llamaindex.ai/python/framework/getting_started/starter_example) is a great place to start.
  * **Report Generation** : Generate a multimodal report using a multi-agent researcher + writer workflow + LlamaParse. [Notebook](https://github.com/run-llama/llama_cloud_services/examples/parse/multimodal/multimodal_report_generation_agent.ipynb).
  * **Customer Support** : Check out starter template for building a [multi-agent concierge with workflows](https://github.com/run-llama/multi-agent-concierge/).


Others:
  * **Productivity Assistant** : Build an agent that can operate over common workflow tools like email, calendar. Check out our [GSuite agent tutorial](https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/tools/llama-index-tools-google/examples/advanced_tools_usage.ipynb).
  * **Coding Assistant** : Build an agent that can operate over code. Check out our [code interpreter tutorial](https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/tools/llama-index-tools-code-interpreter/examples/code_interpreter.ipynb).


## Resources
[Section titled “Resources”](https://developers.llamaindex.ai/python/framework/use_cases/agents/#resources)
**Prebuilt Agents and Tools**
The following component guides are the central hubs for getting started in building with agents:


**Custom Agentic Workflows**
LlamaIndex Workflows allow you to build very custom, agentic workflows through a core event-driven orchestration foundation.
  * [Workflows Documentation](https://developers.llamaindex.ai/python/llamaagents/workflows)
  * [Building a ReAct agent workflow](https://developers.llamaindex.ai/python/examples/workflow/react_agent)
  * [Deploying Workflows](https://developers.llamaindex.ai/python/llamaagents/llamactl/getting-started/)


**Building with Agentic Ingredients**
If you want to leverage core agentic ingredients in your workflow, LlamaIndex has robust abstractions for every agent sub-ingredient.
  * **Query Planning** : [Routing](https://developers.llamaindex.ai/python/framework/module_guides/querying/router), [Sub-Questions](https://developers.llamaindex.ai/python/examples/query_engine/sub_question_query_engine), [Query Transformations](https://developers.llamaindex.ai/python/framework/optimizing/advanced_retrieval/query_transformations).
  * **Function Calling and Tool Use** : Check out our [OpenAI](https://developers.llamaindex.ai/python/examples/llm/openai), [Mistral](https://developers.llamaindex.ai/python/examples/llm/mistralai) guides as examples.


## Ecosystem
[Section titled “Ecosystem”](https://developers.llamaindex.ai/python/framework/use_cases/agents/#ecosystem)
  * **Community-Built Agents** : We offer a collection of 40+ agent tools for use with your agent in [LlamaHub](https://llamahub.ai/) 🦙.


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


