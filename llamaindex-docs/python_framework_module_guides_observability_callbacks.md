[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/observability/callbacks/#_top)
LlamaIndex Framework
Component Guides
Observability
Callbacks
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Callbacks
## Concept
[Section titled “Concept”](https://developers.llamaindex.ai/python/framework/module_guides/observability/callbacks/#concept)
LlamaIndex provides callbacks to help debug, track, and trace the inner workings of the library. Using the callback manager, as many callbacks as needed can be added.
In addition to logging data related to events, you can also track the duration and number of occurrences of each event.
Furthermore, a trace map of events is also recorded, and callbacks can use this data however they want. For example, the `LlamaDebugHandler` will, by default, print the trace of events after most operations.
**Callback Event Types** While each callback may not leverage each event type, the following events are available to be tracked:
  * `CHUNKING` -> Logs for the before and after of text splitting.
  * `NODE_PARSING` -> Logs for the documents and the nodes that they are parsed into.
  * `EMBEDDING` -> Logs for the number of texts embedded.
  * `LLM` -> Logs for the template and response of LLM calls.
  * `QUERY` -> Keeps track of the start and end of each query.
  * `RETRIEVE` -> Logs for the nodes retrieved for a query.
  * `SYNTHESIZE` -> Logs for the result for synthesize calls.
  * `TREE` -> Logs for the summary and level of summaries generated.
  * `SUB_QUESTION` -> Log for a generated sub question and answer.


You can implement your own callback to track and trace these events, or use an existing callback.
## Modules
[Section titled “Modules”](https://developers.llamaindex.ai/python/framework/module_guides/observability/callbacks/#modules)
Currently supported callbacks are as follows:
  * [TokenCountingHandler](https://developers.llamaindex.ai/python/examples/observability/tokencountinghandler) -> Flexible token counting for prompt, completion, and embedding token usage. See [the migration details](https://developers.llamaindex.ai/python/framework/module_guides/observability/callbacks/token_counting_migration)
  * [LlamaDebugHanlder](https://developers.llamaindex.ai/python/examples/observability/llamadebughandler) -> Basic tracking and tracing for events. Example usage can be found in the notebook below.
  * [WandbCallbackHandler](https://developers.llamaindex.ai/python/examples/observability/wandbcallbackhandler) -> Tracking of events and traces using the Wandb Prompts frontend. More details are in the notebook below or at [Wandb](https://docs.wandb.ai/guides/prompts/quickstart)
  * [AimCallback](https://developers.llamaindex.ai/python/examples/observability/aimcallback) -> Tracking of LLM inputs and outputs. Example usage can be found in the notebook below.
  * [OpenInferenceCallbackHandler](https://developers.llamaindex.ai/python/examples/observability/openinferencecallback) -> Tracking of AI model inferences. Example usage can be found in the notebook below.
  * [OpenAIFineTuningHandler](https://github.com/jerryjliu/llama_index/blob/main/experimental/openai_fine_tuning/openai_fine_tuning.ipynb) -> Records all LLM inputs and outputs. Then, provides a function `save_finetuning_events()` to save inputs and outputs in a format suitable for fine-tuning with OpenAI.


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


