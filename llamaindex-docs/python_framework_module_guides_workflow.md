[Skip to content](https://developers.llamaindex.ai/python/llamaagents/workflows/#_top)
LlamaAgents
Agent Workflows
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Introduction
## What is a workflow?
[Section titled “What is a workflow?”](https://developers.llamaindex.ai/python/llamaagents/workflows/#what-is-a-workflow)
A workflow is an event-driven, step-based way to control the execution flow of an application.
Your application is divided into sections called Steps which are triggered by Events, and themselves emit Events which trigger further steps. By combining steps and events, you can create arbitrarily complex flows that encapsulate logic and make your application more maintainable and easier to understand. A step can be anything from a single line of code to a complex agent. They can have arbitrary inputs and outputs, which are passed around by Events.
## Why workflows?
[Section titled “Why workflows?”](https://developers.llamaindex.ai/python/llamaagents/workflows/#why-workflows)
As generative AI applications become more complex, it becomes harder to manage the flow of data and control the execution of the application. Workflows provide a way to manage this complexity by breaking the application into smaller, more manageable pieces.
Other frameworks and LlamaIndex itself have attempted to solve this problem previously with directed acyclic graphs (DAGs) but these have a number of limitations that workflows do not:
  * Logic like loops and branches needed to be encoded into the edges of graphs, which made them hard to read and understand.
  * Passing data between nodes in a DAG created complexity around optional and default values and which parameters should be passed.
  * DAGs did not feel natural to developers trying to developing complex, looping, branching AI applications.


The event-based pattern and vanilla python approach of Workflows resolves these problems.
## Getting Started
[Section titled “Getting Started”](https://developers.llamaindex.ai/python/llamaagents/workflows/#getting-started)
As an illustrative example, let’s consider a naive workflow where a joke is generated and then critiqued.

```


from workflows import Workflow, step




from workflows.events import (




Event,




StartEvent,




StopEvent,





# `pip install llama-index-llms-openai` if you don't already have it



from llama_index.llms.openai import OpenAI






classJokeEvent(Event):




joke: str






classJokeFlow(Workflow):




llm = OpenAI(model="gpt-4.1")





@step




asyncdefgenerate_joke(self, ev: StartEvent) -> JokeEvent:




topic = ev.topic





prompt =f"Write your best joke about {topic}."




response =awaitself.llm.acomplete(prompt)




return JokeEvent(joke=str(response))





@step




asyncdefcritique_joke(self, ev: JokeEvent) -> StopEvent:




joke = ev.joke





prompt =f"Give a thorough analysis and critique of the following joke: {joke}"




response =awaitself.llm.acomplete(prompt)




return StopEvent(result=str(response))






w = JokeFlow(timeout=60, verbose=False)




result =await w.run(topic="pirates")




print(str(result))


```

There’s a few moving pieces here, so let’s go through this piece by piece.
### Defining Workflow Events
[Section titled “Defining Workflow Events”](https://developers.llamaindex.ai/python/llamaagents/workflows/#defining-workflow-events)

```


classJokeEvent(Event):




joke: str


```

Events are user-defined pydantic objects. You control the attributes and any other auxiliary methods. In this case, our workflow relies on a single user-defined event, the `JokeEvent`.
### Setting up the Workflow Class
[Section titled “Setting up the Workflow Class”](https://developers.llamaindex.ai/python/llamaagents/workflows/#setting-up-the-workflow-class)

```


classJokeFlow(Workflow):




llm = OpenAI(model="gpt-4.1")



```

Our workflow is implemented by subclassing the `Workflow` class. For simplicity, we attached a static `OpenAI` llm instance.
### Workflow Entry Points
[Section titled “Workflow Entry Points”](https://developers.llamaindex.ai/python/llamaagents/workflows/#workflow-entry-points)

```


classJokeFlow(Workflow):






@step




asyncdefgenerate_joke(self, ev: StartEvent) -> JokeEvent:




topic = ev.topic





prompt =f"Write your best joke about {topic}."




response =awaitself.llm.acomplete(prompt)




return JokeEvent(joke=str(response))




```

Here, we come to the entry-point of our workflow. While most events are use-defined, there are two special-case events, the `StartEvent` and the `StopEvent` that the framework provides out of the box. Here, the `StartEvent` signifies where to send the initial workflow input.
The `StartEvent` is a bit of a special object since it can hold arbitrary attributes. Here, we accessed the topic with `ev.topic`, which would raise an error if it wasn’t there. You could also do `ev.get("topic")` to handle the case where the attribute might not be there without raising an error.
For further type safety, you can also subclass the `StartEvent`.
At this point, you may have noticed that we haven’t explicitly told the workflow what events are handled by which steps. Instead, the `@step` decorator is used to infer the input and output types of each step. Furthermore, these inferred input and output types are also used to verify for you that the workflow is valid before running!
### Workflow Exit Points
[Section titled “Workflow Exit Points”](https://developers.llamaindex.ai/python/llamaagents/workflows/#workflow-exit-points)

```


classJokeFlow(Workflow):






@step




asyncdefcritique_joke(self, ev: JokeEvent) -> StopEvent:




joke = ev.joke





prompt =f"Give a thorough analysis and critique of the following joke: {joke}"




response =awaitself.llm.acomplete(prompt)




return StopEvent(result=str(response))




```

Here, we have our second, and last step, in the workflow. We know its the last step because the special `StopEvent` is returned. When the workflow encounters a returned `StopEvent`, it immediately stops the workflow and returns whatever we passed in the `result` parameter.
In this case, the result is a string, but it could be a dictionary, list, or any other object.
You can also subclass the `StopEvent` class for further type safety.
### Running the Workflow
[Section titled “Running the Workflow”](https://developers.llamaindex.ai/python/llamaagents/workflows/#running-the-workflow)

```


w = JokeFlow(timeout=60, verbose=False)




result =await w.run(topic="pirates")




print(str(result))


```

Lastly, we create and run the workflow. There are some settings like timeouts (in seconds) and verbosity to help with debugging.
The `.run()` method is async, so we use await here to wait for the result. The keyword arguments passed to `run()` will become fields of the special `StartEvent` that will be automatically emitted and start the workflow. As we have seen, in this case `topic` will be accessed from the step with `ev.topic`.
## Examples
[Section titled “Examples”](https://developers.llamaindex.ai/python/llamaagents/workflows/#examples)
To help you become more familiar with the workflow concept and its features, LlamaIndex documentation offers example notebooks that you can run for hands-on learning:
  * [Common Workflow Patterns](https://developers.llamaindex.ai/python/examples/workflow/workflows_cookbook/) walks you through common usage patterns like looping and state management using simple workflows. It’s usually a great place to start.
  * [RAG + Reranking](https://developers.llamaindex.ai/python/examples/workflow/rag/) shows how to implement a real-world use case with a fairly simple workflow that performs both ingestion and querying.
  * [Citation Query Engine](https://developers.llamaindex.ai/python/examples/workflow/citation_query_engine/) similar to RAG + Reranking, the notebook focuses on how to implement intermediate steps in between retrieval and generation. A good example of how to use the [`Context`](https://developers.llamaindex.ai/python/llamaagents/workflows/#working-with-global-context-state) object in a workflow.
  * [Corrective RAG](https://developers.llamaindex.ai/python/examples/workflow/corrective_rag_pack/) adds some more complexity on top of a RAG workflow, showcasing how to query a web search engine after an evaluation step.
  * [Utilizing Concurrency](https://developers.llamaindex.ai/python/examples/workflow/parallel_execution/) explains how to manage the parallel execution of steps in a workflow, something that’s important to know as your workflows grow in complexity.


RAG applications are easy to understand and offer a great opportunity to learn the basics of workflows. However, more complex agentic scenarios involving tool calling, memory, and routing are where workflows excel.
The examples below highlight some of these use-cases.
  * [ReAct Agent](https://developers.llamaindex.ai/python/examples/workflow/react_agent/) is obviously the perfect example to show how to implement tools in a workflow.
  * [Function Calling Agent](https://developers.llamaindex.ai/python/examples/workflow/function_calling_agent/) is a great example of how to use the LlamaIndex framework primitives in a workflow, keeping it small and tidy even in complex scenarios like function calling.
  * [CodeAct Agent](https://developers.llamaindex.ai/python/examples/agent/from_scratch_code_act_agent/) is a great example of how to create a CodeAct Agent from scratch.
  * [Human In The Loop: Story Crafting](https://developers.llamaindex.ai/python/examples/workflow/human_in_the_loop_story_crafting/) is a powerful example showing how workflow runs can be interactive and stateful. In this case, to collect input from a human.
  * [Reliable Structured Generation](https://developers.llamaindex.ai/python/examples/workflow/reflection/) shows how to implement loops in a workflow, in this case to improve structured output through reflection.
  * [Query Planning with Workflows](https://developers.llamaindex.ai/python/examples/workflow/planning_workflow/) is an example of a workflow that plans a query by breaking it down into smaller items, and executing those smaller items. It highlights how to stream events from a workflow, execute steps in parallel, and looping until a condition is met.
  * [Checkpointing Workflows](https://developers.llamaindex.ai/python/examples/workflow/checkpointing_workflows/) is a more exhaustive demonstration of how to make full use of `WorkflowCheckpointer` to checkpoint Workflow runs.


Last but not least, a few more advanced use cases that demonstrate how workflows can be extremely handy if you need to quickly implement prototypes, for example from literature:
  * [Advanced Text-to-SQL](https://developers.llamaindex.ai/python/examples/workflow/advanced_text_to_sql/)
  * [Multi-Step Query Engine](https://developers.llamaindex.ai/python/examples/workflow/multi_step_query_engine/)
  * [Multi-Strategy Workflow](https://developers.llamaindex.ai/python/examples/workflow/multi_strategy_workflow/)
  * [Router Query Engine](https://developers.llamaindex.ai/python/examples/workflow/router_query_engine/)
  * [Self Discover Workflow](https://developers.llamaindex.ai/python/examples/workflow/self_discover_workflow/)
  * [Sub-Question Query Engine](https://developers.llamaindex.ai/python/examples/workflow/sub_question_query_engine/)


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


