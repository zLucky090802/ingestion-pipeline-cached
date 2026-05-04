[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/querying/structured_outputs/pydantic_program/#_top)
LlamaIndex Framework
Component Guides
Querying
Structured Outputs
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Pydantic Programs
A pydantic program is a generic abstraction that takes in an input string and converts it to a structured Pydantic object type.
Because this abstraction is so generic, it encompasses a broad range of LLM workflows. The programs are composable and be for more generic or specific use cases.
There’s a few general types of Pydantic Programs:
  * **Text Completion Pydantic Programs** : These convert input text into a user-specified structured object through a text completion API + output parsing.
  * **Function Calling Pydantic Programs** : These convert input text into a user-specified structured object through an LLM function calling API.
  * **Prepackaged Pydantic Programs** : These convert input text into prespecified structured objects.


## Text Completion Pydantic Programs
[Section titled “Text Completion Pydantic Programs”](https://developers.llamaindex.ai/python/framework/module_guides/querying/structured_outputs/pydantic_program/#text-completion-pydantic-programs)
See the example notebook on [LLM Text Completion programs](https://developers.llamaindex.ai/python/examples/output_parsing/llm_program)
## Function Calling Pydantic Programs
[Section titled “Function Calling Pydantic Programs”](https://developers.llamaindex.ai/python/framework/module_guides/querying/structured_outputs/pydantic_program/#function-calling-pydantic-programs)
  * [Function Calling Pydantic Program](https://developers.llamaindex.ai/python/examples/output_parsing/function_program)
  * [OpenAI Pydantic Program](https://developers.llamaindex.ai/python/examples/output_parsing/openai_pydantic_program)
  * [Guidance Pydantic Program](https://developers.llamaindex.ai/python/examples/output_parsing/guidance_pydantic_program)
  * [Guidance Sub-Question Generator](https://developers.llamaindex.ai/python/examples/output_parsing/guidance_sub_question)


## Prepackaged Pydantic Programs
[Section titled “Prepackaged Pydantic Programs”](https://developers.llamaindex.ai/python/framework/module_guides/querying/structured_outputs/pydantic_program/#prepackaged-pydantic-programs)


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


