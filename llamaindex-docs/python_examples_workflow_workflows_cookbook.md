[Skip to content](https://developers.llamaindex.ai/python/examples/workflow/workflows_cookbook/#_top)
# Workflows cookbook: walking through all features of Workflows 
First, we install our dependencies. Core contains most of what we need; OpenAI is to handle LLM access and utils-workflow provides the visualization capabilities we’ll use later on.

```


!pip install --upgrade llama-index-core llama-index-llms-openai llama-index-utils-workflow


```

Then we bring in the deps we just installed

```


from llama_index.core.workflow import (




Event,




StartEvent,




StopEvent,




Workflow,




step,




Context,





import random




from llama_index.core.workflow import draw_all_possible_flows




from llama_index.utils.workflow import draw_most_recent_execution




from llama_index.llms.openai import OpenAI


```

Set up our OpenAI key, so we can do actual LLM things.

```


import os





os.environ["OPENAI_API_KEY"] ="sk-proj-..."


```

## Workflow basics
[Section titled “Workflow basics”](https://developers.llamaindex.ai/python/examples/workflow/workflows_cookbook/#workflow-basics)
Let’s start with the basic possible workflow: it just starts, does one thing, and stops. There’s no reason to have a real workflow if your task is this simple, but we’re just demonstrating how they work.

```


from llama_index.llms.openai import OpenAI






classOpenAIGenerator(Workflow):




@step




asyncdefgenerate(self, ev: StartEvent) -> StopEvent:




llm = OpenAI(model="gpt-4o")




response =await llm.acomplete(ev.query)




return StopEvent(result=str(response))






w = OpenAIGenerator(timeout=10, verbose=False)




result =await w.run(query="What's LlamaIndex?")




print(result)


```


```

LlamaIndex, formerly known as GPT Index, is a data framework designed to facilitate the connection between large language models (LLMs) and external data sources. It provides tools to index various data types, such as documents, databases, and APIs, enabling LLMs to interact with and retrieve information from these sources more effectively. The framework supports the creation of indices that can be queried by LLMs, enhancing their ability to access and utilize external data in a structured manner. This capability is particularly useful for applications requiring the integration of LLMs with specific datasets or knowledge bases.

```

One of the neat things about Workflows is that we can use pyvis to visualize them. Let’s see what that looks like for this very simple flow.

```


draw_all_possible_flows(OpenAIGenerator, filename="trivial_workflow.html")


```

Not a lot to see here, yet! The start event goes to generate() and then straight to StopEvent.
## Loops and branches
[Section titled “Loops and branches”](https://developers.llamaindex.ai/python/examples/workflow/workflows_cookbook/#loops-and-branches)
Let’s go to a more interesting example, demonstrating our ability to loop:

```


classFailedEvent(Event):




error: str






classQueryEvent(Event):




query: str






classLoopExampleFlow(Workflow):




@step




asyncdefanswer_query(




self, ev: StartEvent | QueryEvent




) -> FailedEvent | StopEvent:




query = ev.query




# try to answer the query




random_number = random.randint(0, 1)




if random_number ==0:




return FailedEvent(error="Failed to answer the query.")




else:




return StopEvent(result="The answer to your query")





@step




asyncdefimprove_query(self, ev: FailedEvent) -> QueryEvent | StopEvent:




# improve the query or decide it can't be fixed




random_number = random.randint(0, 1)




if random_number ==0:




return QueryEvent(query="Here's a better query.")




else:




return StopEvent(result="Your query can't be fixed.")


```

We’re using random numbers to simulate LLM actions here so that we can get reliably interesting behavior.
answer_query() accepts a start event. It can then do 2 things:
  * it can answer the query and emit a StopEvent, which returns the result
  * it can decide the query was bad and emit a FailedEvent


improve_query() accepts a FailedEvent. It can also do 2 things:
  * it can decide the query can’t be improved and emit a StopEvent, which returns failure
  * it can present a better query and emit a QueryEvent, which creates a loop back to answer_query()


We can also visualize this more complicated workflow:

```


draw_all_possible_flows(LoopExampleFlow, filename="loop_workflow.html")


```


```

loop_workflow.html

```

We’ve set `verbose=True` here so we can see exactly what events were triggered. You can see it conveniently demonstrates looping and then answering.

```


l = LoopExampleFlow(timeout=10, verbose=True)




result =await l.run(query="What's LlamaIndex?")




print(result)


```


```

Running step answer_query


Step answer_query produced event FailedEvent


Running step improve_query


Step improve_query produced event StopEvent


Your query can't be fixed.

```

## Maintaining state between events
[Section titled “Maintaining state between events”](https://developers.llamaindex.ai/python/examples/workflow/workflows_cookbook/#maintaining-state-between-events)
There is a global state which allows you to keep arbitrary data or functions around for use by all event handlers.

```


classGlobalExampleFlow(Workflow):




@step




asyncdefsetup(self, ctx: Context, ev: StartEvent) -> QueryEvent:




# load our data here




await ctx.store.set("some_database", ["value1", "value2", "value3"])





return QueryEvent(query=ev.query)





@step




asyncdefquery(self, ctx: Context, ev: QueryEvent) -> StopEvent:




# use our data with our query




data =await ctx.store.get("some_database")





result =f"The answer to your query is {data[1]}"




return StopEvent(result=result)


```


```


g = GlobalExampleFlow(timeout=10, verbose=True)




result =await g.run(query="What's LlamaIndex?")




print(result)


```


```

Running step setup


Step setup produced event QueryEvent


Running step query


Step query produced event StopEvent


The answer to your query is value2

```

Of course, this flow is essentially still linear. A more realistic example would be if your start event could either be a query or a data population event, and you needed to wait. Let’s set that up to see what it looks like:

```


classWaitExampleFlow(Workflow):




@step




asyncdefsetup(self, ctx: Context, ev: StartEvent) -> StopEvent:




ifhasattr(ev, "data"):




await ctx.store.set("data", ev.data)





return StopEvent(result=None)





@step




asyncdefquery(self, ctx: Context, ev: StartEvent) -> StopEvent:




ifhasattr(ev, "query"):




# do we have any data?




ifhasattr(self, "data"):




data =await ctx.store.get("data")




return StopEvent(result=f"Got the data {data}")




else:




# there's non data yet




returnNone




else:




# this isn't a query




returnNone


```


```


w = WaitExampleFlow(verbose=True)




result =await w.run(query="Can I kick it?")




if result isNone:




print("No you can't")




print("---")




result =await w.run(data="Yes you can")




print("---")




result =await w.run(query="Can I kick it?")




print(result)


```


```

Running step query


Step query produced no event


Running step setup


Step setup produced event StopEvent


No you can't



Running step query


Step query produced no event


Running step setup


Step setup produced event StopEvent



Running step query


Step query produced event StopEvent


Running step setup


Step setup produced event StopEvent


Got the data Yes you can

```

Let’s visualize how this flow works:

```


draw_all_possible_flows(WaitExampleFlow, filename="wait_workflow.html")


```


```

wait_workflow.html

```

## Waiting for one or more events
[Section titled “Waiting for one or more events”](https://developers.llamaindex.ai/python/examples/workflow/workflows_cookbook/#waiting-for-one-or-more-events)
Because waiting for events is such a common pattern, the context object has a convenience function, `collect_events()`. It will capture events and store them, returning `None` until all the events it requires have been collected. Those events will be attached to the output of `collect_events` in the order that they were specified. Let’s see this in action:

```


classInputEvent(Event):




input: str






classSetupEvent(Event):




error: bool






classQueryEvent(Event):




query: str






classCollectExampleFlow(Workflow):




@step




asyncdefsetup(self, ctx: Context, ev: StartEvent) -> SetupEvent:




# generically start everything up




ifnothasattr(self, "setup") ornotself.setup:




self.setup =True




print("I got set up")




return SetupEvent(error=False)





@step




asyncdefcollect_input(self, ev: StartEvent) -> InputEvent:




ifhasattr(ev, "input"):




# perhaps validate the input




print("I got some input")




return InputEvent(input=ev.input)





@step




asyncdefparse_query(self, ev: StartEvent) -> QueryEvent:




ifhasattr(ev, "query"):




# parse the query in some way




print("I got a query")




return QueryEvent(query=ev.query)





@step




asyncdefrun_query(




self, ctx: Context, ev: InputEvent | SetupEvent | QueryEvent




) -> StopEvent |None:




ready = ctx.collect_events(ev, [QueryEvent, InputEvent, SetupEvent])




if ready isNone:




print("Not enough events yet")




returnNone





# run the query




print("Now I have all the events")




print(ready)





result =f"Ran query '{ready[0].query}' on input '{ready[1].input}'"




return StopEvent(result=result)


```


```


c = CollectExampleFlow()




result =await c.run(input="Here's some input", query="Here's my question")




print(result)


```


```

I got some input


I got a query


Not enough events yet


Not enough events yet


Now I have all the events


[QueryEvent(query="Here's my question"), InputEvent(input="Here's some input"), SetupEvent(error=False)]


Ran query 'Here's my question' on input 'Here's some input'

```

You can see each of the events getting triggered as well as the collection event repeatedly returning `None` until enough events have arrived. Let’s see what this looks like in a flow diagram:

```


draw_all_possible_flows(CollectExampleFlow, "collect_workflow.html")


```


```

collect_workflow.html

```

This concludes our tour of creating, running and visualizing workflows! Check out the [docs](https://docs.llamaindex.ai/en/stable/module_guides/workflow/) and [examples](https://docs.llamaindex.ai/en/stable/examples/workflow/function_calling_agent/) to learn more.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


