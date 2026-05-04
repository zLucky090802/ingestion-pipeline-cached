[Skip to content](https://developers.llamaindex.ai/python/examples/agent/memory/chat_memory_buffer/#_top)
# Chat Memory Buffer 
**NOTE:** This example of memory is deprecated in favor of the newer and more flexible `Memory` class. See the [latest docs](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/memory/).
The `ChatMemoryBuffer` is a memory buffer that simply stores the last X messages that fit into a token limit.
%pip install llama-index-core
## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/examples/agent/memory/chat_memory_buffer/#setup)

```


from llama_index.core.memory import ChatMemoryBuffer





memory = ChatMemoryBuffer.from_defaults(token_limit=40000)


```

## Using Standalone
[Section titled “Using Standalone”](https://developers.llamaindex.ai/python/examples/agent/memory/chat_memory_buffer/#using-standalone)

```


from llama_index.core.llms import ChatMessage





chat_history = [




ChatMessage(role="user", content="Hello, how are you?"),




ChatMessage(role="assistant", content="I'm doing well, thank you!"),





# put a list of messages


memory.put_messages(chat_history)



# put one message at a time


# memory.put_message(chat_history[0])

```


```

# Get the last X messages that fit into a token limit



history = memory.get()


```


```

# Get all messages



all_history = memory.get_all()


```


```

# clear the memory


memory.reset()

```

## Using with Agents
[Section titled “Using with Agents”](https://developers.llamaindex.ai/python/examples/agent/memory/chat_memory_buffer/#using-with-agents)
You can set the memory in any agent in the `.run()` method.

```


import os





os.environ["OPENAI_API_KEY"] ="sk-proj-..."


```


```


from llama_index.core.agent.workflow import ReActAgent, FunctionAgent




from llama_index.core.workflow import Context




from llama_index.llms.openai import OpenAI






memory = ChatMemoryBuffer.from_defaults(token_limit=40000)





agent = FunctionAgent(tools=[], llm=OpenAI(model="gpt-4o-mini"))




# context to hold the chat history/state



ctx = Context(agent)


```


```


resp =await agent.run("Hello, how are you?", ctx=ctx, memory=memory)


```


```


print(memory.get_all())


```


```

[ChatMessage(role=<MessageRole.USER: 'user'>, additional_kwargs={}, blocks=[TextBlock(block_type='text', text='Hello, how are you?')]), ChatMessage(role=<MessageRole.ASSISTANT: 'assistant'>, additional_kwargs={}, blocks=[TextBlock(block_type='text', text="Hello! I'm just a program, so I don't have feelings, but I'm here and ready to help you. How can I assist you today?")])]

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


