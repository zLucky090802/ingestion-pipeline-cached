[Skip to content](https://developers.llamaindex.ai/python/framework/use_cases/prompting/#_top)
LlamaIndex Framework
Use Cases
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Prompting
Prompting LLMs is a fundamental unit of any LLM application. You can build an entire application entirely around prompting, or orchestrate with other modules (e.g. retrieval) to build RAG, agents, and more.
LlamaIndex supports LLM abstractions and simple-to-advanced prompt abstractions to make complex prompt workflows possible.
## LLM Integrations
[Section titled “LLM Integrations”](https://developers.llamaindex.ai/python/framework/use_cases/prompting/#llm-integrations)
LlamaIndex supports 40+ LLM integrations, from proprietary model providers like OpenAI, Anthropic to open-source models/model providers like Mistral, Ollama, Replicate. It provides all the tools to standardize interface around common LLM usage patterns, including but not limited to async, streaming, function calling.
Here’s the [full module guide for LLMs](https://developers.llamaindex.ai/python/framework/module_guides/models/llms).
## Prompts
[Section titled “Prompts”](https://developers.llamaindex.ai/python/framework/use_cases/prompting/#prompts)
LlamaIndex has robust prompt abstractions that capture all the common interaction patterns with LLMs.
Here’s the [full module guide for prompts](https://developers.llamaindex.ai/python/framework/module_guides/models/prompts).
### Table Stakes
[Section titled “Table Stakes”](https://developers.llamaindex.ai/python/framework/use_cases/prompting/#table-stakes)
  * [Text Completion Prompts](https://developers.llamaindex.ai/python/examples/customization/prompts/completion_prompts)


### Advanced
[Section titled “Advanced”](https://developers.llamaindex.ai/python/framework/use_cases/prompting/#advanced)
  * [Variable Mappings, Functions, Partials](https://developers.llamaindex.ai/python/examples/prompts/advanced_prompts)
  * [RichPromptTemplate Features](https://developers.llamaindex.ai/python/examples/prompts/rich_prompt_template_features)


## Prompt Chains and Pipelines
[Section titled “Prompt Chains and Pipelines”](https://developers.llamaindex.ai/python/framework/use_cases/prompting/#prompt-chains-and-pipelines)
LlamaIndex has robust abstractions for creating sequential prompt chains, as well as general DAGs to orchestrate prompts with any other component. This allows you to build complex workflows, including RAG with multi-hop query understanding layers, as well as agents.
These pipelines are integrated with [observability partners](https://developers.llamaindex.ai/python/framework/module_guides/observability) out of the box.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


