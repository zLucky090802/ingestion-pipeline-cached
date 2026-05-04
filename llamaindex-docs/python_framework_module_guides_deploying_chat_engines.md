[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines/#_top)
LlamaIndex Framework
Component Guides
Deploying
Chat Engines
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Chat Engine
## Concept
[Section titled “Concept”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines/#concept)
Chat engine is a high-level interface for having a conversation with your data (multiple back-and-forth instead of a single question & answer). Think ChatGPT, but augmented with your knowledge base.
Conceptually, it is a **stateful** analogy of a [Query Engine](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine). By keeping track of the conversation history, it can answer questions with past context in mind.
## Usage Pattern
[Section titled “Usage Pattern”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines/#usage-pattern)
Get started with:

```


chat_engine = index.as_chat_engine()




response = chat_engine.chat("Tell me a joke.")


```

To stream response:

```


chat_engine = index.as_chat_engine()




streaming_response = chat_engine.stream_chat("Tell me a joke.")




for token in streaming_response.response_gen:




print(token, end="")


```

More details in the complete [usage pattern guide](https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines/usage_pattern).
## Modules
[Section titled “Modules”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines/#modules)
In our [modules section](https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines/modules), you can find corresponding tutorials to see the available chat engines in action.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


