[Skip to content](https://developers.llamaindex.ai/python/framework/understanding/#_top)
LlamaIndex Framework
Learn
[Building an LLM application](https://developers.llamaindex.ai/python/framework/understanding/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Building an LLM application
Welcome to Understanding LlamaIndex. This is a series of short, bite-sized tutorials on every stage of building an agentic LLM application to get you acquainted with how to use LlamaIndex before diving into more advanced and subtle strategies. If you’re an experienced programmer new to LlamaIndex, this is the place to start.
## Key steps in building an agentic LLM application
[Section titled “Key steps in building an agentic LLM application”](https://developers.llamaindex.ai/python/framework/understanding/#key-steps-in-building-an-agentic-llm-application)
This tutorial has three main parts: **Building a RAG pipeline** , **Building an agent** , and **Building Workflows** , with some smaller sections before and after. Here’s what to expect:
  * : hit the ground running by getting started working with LLMs. We’ll show you how to use any of our [dozens of supported LLMs](https://developers.llamaindex.ai/python/framework/module_guides/models/llms/modules), whether via remote API calls or running locally on your machine.
  * : agents are LLM-powered knowledge workers that can interact with the world via a set of tools. Those tools can retrieve information (such as RAG, see below) or take action. This tutorial includes:
    * **[Building a single agent](https://developers.llamaindex.ai/python/framework/understanding/agent)** : We show you how to build a simple agent that can interact with the world via a set of tools.
    * **[Using existing tools](https://developers.llamaindex.ai/python/framework/understanding/agent/tools)** : LlamaIndex provides a registry of pre-built agent tools at [LlamaHub](https://llamahub.ai/) that you can incorporate into your agents.
    * : agents can maintain state, which is important for building more complex applications.
    * **[Streaming output and events](https://developers.llamaindex.ai/python/framework/understanding/agent/streaming)** : providing visibility and feedback to the user is important, and streaming allows you to do that.
    * : getting human feedback to your agent can be critical.
    * **[Multi-agent systems with AgentWorkflow](https://developers.llamaindex.ai/python/framework/understanding/agent/multi_agent)** : combining multiple agents to collaborate is a powerful technique for building more complex systems; this section shows you how to do so.
  * : Workflows are a lower-level, event-driven abstraction for building agentic applications. They’re the base layer you should be using to build any advanced agentic application. You can use the pre-built abstractions you learned above, or build agents completely from scratch. This tutorial covers:
    * **[Building a simple workflow](https://developers.llamaindex.ai/python/llamaagents/workflows)** : a simple workflow that shows you how to use the `Workflow` class to build a basic agentic application.
    * **[Looping and branching](https://developers.llamaindex.ai/python/llamaagents/workflows/branches_and_loops)** : these core control flow patterns are the building blocks of more complex workflows.
    * **[Concurrent execution](https://developers.llamaindex.ai/python/llamaagents/workflows/concurrent_execution)** : you can run steps in parallel to split up work efficiently.
    * : your agents can emit user-facing events just like the agents you built above.
    * **[Stateful workflows](https://developers.llamaindex.ai/python/llamaagents/workflows/managing_state)** : workflows can maintain state, which is important for building more complex applications.
    * : workflows can be traced and debugged using various integrations like Arize Pheonix, OpenTelemetry, and more.
  * **[Adding RAG to your agents](https://developers.llamaindex.ai/python/framework/understanding/rag)** : Retrieval-Augmented Generation (RAG) is a key technique for getting your data to an LLM, and a component of more sophisticated agentic systems. We’ll show you how to enhance your agents with a full-featured RAG pipeline that can answer questions about your data. This includes:
    * **[Loading& Ingestion](https://developers.llamaindex.ai/python/framework/understanding/rag/loading)**: Getting your data from wherever it lives, whether that’s unstructured text, PDFs, databases, or APIs to other applications. LlamaIndex has hundreds of connectors to every data source over at [LlamaHub](https://llamahub.ai/).
    * **[Indexing and Embedding](https://developers.llamaindex.ai/python/framework/understanding/rag/indexing)** : Once you’ve got your data there are an infinite number of ways to structure access to that data to ensure your applications is always working with the most relevant data. LlamaIndex has a huge number of these strategies built-in and can help you select the best ones.
    * : You will probably find it more efficient to store your data in indexed form, or pre-processed summaries provided by an LLM, often in a specialized database known as a `Vector Store` (see below). You can also store your indexes, metadata and more.
    * : Every indexing strategy has a corresponding querying strategy and there are lots of ways to improve the relevance, speed and accuracy of what you retrieve and what the LLM does with it before returning it to you, including turning it into structured responses such as an API.
  * **[Putting it all together](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together)** : whether you are building question & answering, chatbots, an API, or an autonomous agent, we show you how to get your application into production.
  * **[Tracing and debugging](https://developers.llamaindex.ai/python/framework/understanding/tracing_and_debugging/tracing_and_debugging)** : also called **observability** , it’s especially important with LLM applications to be able to look into the inner workings of what’s going on to help you debug problems and spot places to improve.
  * : every strategy has pros and cons and a key part of building, shipping and evolving your application is evaluating whether your change has improved your application in terms of accuracy, performance, clarity, cost and more. Reliably evaluating your changes is a crucial part of LLM application development.


## Let’s get started!
[Section titled “Let’s get started!”](https://developers.llamaindex.ai/python/framework/understanding/#lets-get-started)
Ready to dive in? Head to [using LLMs](https://developers.llamaindex.ai/python/framework/understanding/using_llms).
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


