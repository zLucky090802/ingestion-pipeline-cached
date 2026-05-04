[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines/usage_pattern/#_top)
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
# Usage Pattern
## Get Started
[Section titled “Get Started”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines/usage_pattern/#get-started)
Build a chat engine from index:

```


chat_engine = index.as_chat_engine()


```

Have a conversation with your data:

```


response = chat_engine.chat("Tell me a joke.")


```

Reset chat history to start a new conversation:

```

chat_engine.reset()

```

Enter an interactive chat REPL:

```

chat_engine.chat_repl()

```

## Configuring a Chat Engine
[Section titled “Configuring a Chat Engine”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines/usage_pattern/#configuring-a-chat-engine)
Configuring a chat engine is very similar to configuring a query engine.
### High-Level API
[Section titled “High-Level API”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines/usage_pattern/#high-level-api)
You can directly build and configure a chat engine from an index in 1 line of code:

```


chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)


```

> Note: you can access different chat engines by specifying the `chat_mode` as a kwarg. `condense_question` corresponds to `CondenseQuestionChatEngine`, `react` corresponds to `ReActChatEngine`, `context` corresponds to a `ContextChatEngine`.
> Note: While the high-level API optimizes for ease-of-use, it does _NOT_ expose full range of configurability.
#### Available Chat Modes
[Section titled “Available Chat Modes”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines/usage_pattern/#available-chat-modes)
  * `best` - Turn the query engine into a tool, for use with a `ReAct` data agent or an `OpenAI` data agent, depending on what your LLM supports. `OpenAI` data agents require `gpt-3.5-turbo` or `gpt-4` as they use the function calling API from OpenAI.
  * `condense_question` - Look at the chat history and re-write the user message to be a query for the index. Return the response after reading the response from the query engine.
  * `context` - Retrieve nodes from the index using every user message. The retrieved text is inserted into the system prompt, so that the chat engine can either respond naturally or use the context from the query engine.
  * `condense_plus_context` - A combination of `condense_question` and `context`. Look at the chat history and re-write the user message to be a retrieval query for the index. The retrieved text is inserted into the system prompt, so that the chat engine can either respond naturally or use the context from the query engine.
  * `simple` - A simple chat with the LLM directly, no query engine involved.
  * `react` - Same as `best`, but forces a `ReAct` data agent.
  * `openai` - Same as `best`, but forces an `OpenAI` data agent.


### Low-Level Composition API
[Section titled “Low-Level Composition API”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines/usage_pattern/#low-level-composition-api)
You can use the low-level composition API if you need more granular control. Concretely speaking, you would explicitly construct `ChatEngine` object instead of calling `index.as_chat_engine(...)`.
> Note: You may need to look at API references or example notebooks.
Here’s an example where we configure the following:
  * configure the condense question prompt,
  * initialize the conversation with some existing history,
  * print verbose debug message.



```


from llama_index.core import PromptTemplate




from llama_index.core.llms import ChatMessage, MessageRole




from llama_index.core.chat_engine import CondenseQuestionChatEngine





custom_prompt = PromptTemplate(





Given a conversation (between Human and Assistant) and a follow up message from Human, \




rewrite the message to be a standalone question that captures all relevant context \



from the conversation.



<Chat History>


{chat_history}



<Follow Up Message>


{question}



<Standalone question>





# list of `ChatMessage` objects



custom_chat_history = [




ChatMessage(




role=MessageRole.USER,




content="Hello assistant, we are having a insightful discussion about Paul Graham today.",





ChatMessage(role=MessageRole.ASSISTANT, content="Okay, sounds good."),






query_engine = index.as_query_engine()




chat_engine = CondenseQuestionChatEngine.from_defaults(




query_engine=query_engine,




condense_question_prompt=custom_prompt,




chat_history=custom_chat_history,




verbose=True,



```

### Streaming
[Section titled “Streaming”](https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines/usage_pattern/#streaming)
To enable streaming, you simply need to call the `stream_chat` endpoint instead of the `chat` endpoint.
!!! warning This somewhat inconsistent with query engine (where you pass in a `streaming=True` flag). We are working on making the behavior more consistent!
**Synchronous (`stream_chat`):**

```


chat_engine = index.as_chat_engine()




streaming_response = chat_engine.stream_chat("Tell me a joke.")





for token in streaming_response.response_gen:




print(token, end="")


```

**Asynchronous (`astream_chat`):**
When using async frameworks (like FastAPI), use astream_chat. Note that you must await the call and iterate over the provided async streaming interface (e.g., async_response_gen() or achat_stream).

```


chat_engine = index.as_chat_engine()




streaming_response =await chat_engine.astream_chat("Tell me a joke.")





asyncfor token in streaming_response.async_response_gen():




print(token, end="")


```

See an [end-to-end tutorial](https://developers.llamaindex.ai/python/examples/customization/streaming/chat_engine_condense_question_stream_response)
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


