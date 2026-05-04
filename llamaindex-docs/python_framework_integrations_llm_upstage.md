[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/llm/upstage/#_top)
LlamaIndex Framework
Integrations
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Upstage 
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-llms-upstage llama-index


```

## Basic Usage
[Section titled “Basic Usage”](https://developers.llamaindex.ai/python/framework/integrations/llm/upstage/#basic-usage)
#### Call `complete` with a prompt
[Section titled “Call complete with a prompt”](https://developers.llamaindex.ai/python/framework/integrations/llm/upstage/#call-complete-with-a-prompt)

```


import os





os.environ["UPSTAGE_API_KEY"] ="YOUR_API_KEY"


```


```


from llama_index.llms.upstage import Upstage





llm = Upstage(




model="solar-mini",




# api_key="YOUR_API_KEY"  # uses UPSTAGE_API_KEY env var by default






resp = llm.complete("Paul Graham is ")


```


```


print(resp)


```


```

Paul Graham is a computer scientist, entrepreneur, and essayist. He is best known as the co-founder of the venture capital firm Y Combinator, which has funded and incubated many successful startups. He is also the author of several influential essays on entrepreneurship, startup culture, and technology.

```

#### Call `chat` with a list of messages
[Section titled “Call chat with a list of messages”](https://developers.llamaindex.ai/python/framework/integrations/llm/upstage/#call-chat-with-a-list-of-messages)

```


from llama_index.core.llms import ChatMessage





messages = [




ChatMessage(




role="system", content="You are a pirate with a colorful personality"





ChatMessage(role="user", content="What is your name"),





resp = llm.chat(messages)


```


```


print(resp)


```


```

assistant: I am Captain Redbeard, the fearless pirate!

```

## Streaming
[Section titled “Streaming”](https://developers.llamaindex.ai/python/framework/integrations/llm/upstage/#streaming)
Using `stream_complete` endpoint

```


resp = llm.stream_complete("Paul Graham is ")


```


```


forin resp:




print(r.delta, end="")


```


```

Paul Graham is a computer scientist, entrepreneur, and essayist. He is best known for co-founding the startup accelerator Y Combinator, which has helped launch some of the most successful tech companies in the world, including Airbnb, Dropbox, and Stripe. He is also the author of several influential essays on startup culture and entrepreneurship, including "How to Start a Startup" and "Hackers & Painters."

```

Using `stream_chat` endpoint

```


from llama_index.core.llms import ChatMessage





messages = [




ChatMessage(




role="system", content="You are a pirate with a colorful personality"





ChatMessage(role="user", content="What is your name"),





resp = llm.stream_chat(messages)


```


```


forin resp:




print(r.delta, end="")


```


```

I am Captain Redbeard, the fearless pirate!

```

## Function Calling
[Section titled “Function Calling”](https://developers.llamaindex.ai/python/framework/integrations/llm/upstage/#function-calling)
Upstage models have native support for function calling. This conveniently integrates with LlamaIndex tool abstractions, letting you plug in any arbitrary Python function to the LLM.

```


from pydantic import BaseModel




from llama_index.core.tools import FunctionTool






classSong(BaseModel):




"""A song with name and artist"""





name: str




artist: str






defgenerate_song(name: str, artist: str) -> Song:




"""Generates a song with provided name and artist."""




return Song(name=name, artist=artist)






tool = FunctionTool.from_defaults(fn=generate_song)


```


```


from llama_index.llms.upstage import Upstage





llm = Upstage()




response = llm.predict_and_call([tool], "Generate a song")




print(str(response))


```


```

name='My Song' artist='John Doe'

```

We can also do multiple function calling.

```


llm = Upstage()




response = llm.predict_and_call(




[tool],




"Generate five songs from the Beatles",




allow_parallel_tool_calls=True,





forin response.sources:




print(f"Name: {s.tool_name}, Input: {s.raw_input}, Output: {str(s)}")


```


```

Name: generate_song, Input: {'args': (), 'kwargs': {'name': 'Beatles', 'artist': 'Beatles'}}, Output: name='Beatles' artist='Beatles'

```

## Async
[Section titled “Async”](https://developers.llamaindex.ai/python/framework/integrations/llm/upstage/#async)

```


from llama_index.llms.upstage import Upstage





llm = Upstage()


```


```


resp =await llm.acomplete("Paul Graham is ")


```


```


print(resp)


```


```

Paul Graham is a computer scientist, entrepreneur, and essayist. He is best known as the co-founder of the startup accelerator Y Combinator, which has helped launch and fund many successful tech companies. He is also the author of several influential essays on startups, entrepreneurship, and technology, including "How to Start a Startup" and "Hackers & Painters."

```


```


resp =await llm.astream_complete("Paul Graham is ")


```


```


asyncfor delta in resp:




print(delta.delta, end="")


```


```

Paul Graham is a computer scientist, entrepreneur, and essayist. He is best known as the co-founder of the startup accelerator Y Combinator, which has helped launch some of the most successful tech companies in the world, including Airbnb, Dropbox, and Stripe. Graham is also a prolific writer, and his essays on topics such as startup advice, artificial intelligence, and the future of work have been widely read and influential in the tech industry.

```

Async function calling is also supported.

```


llm = Upstage()




response =await llm.apredict_and_call([tool], "Generate a song")




print(str(response))


```


```

name='My Song' artist='Me'

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


