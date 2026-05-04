[Skip to content](https://developers.llamaindex.ai/python/llamaagents/workflows/observability/#_top)
LlamaAgents
Agent Workflows
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Observability
Observability is key for debugging workflows. Beyond just adding `print()` statements, `workflows` ship with an extensive instrumentation system that tracks the input and output of every workflow step.
Furthermore, you can leverage this instrumentation system to add observability to any function outside of workflow steps! More in-depth examples for all of this information can be found in the [examples folder for observability](https://github.com/run-llama/llama-agents/tree/main/examples/observability).
## OpenTelemetry Integration
[Section titled “OpenTelemetry Integration”](https://developers.llamaindex.ai/python/llamaagents/workflows/observability/#opentelemetry-integration)
Workflows integrate with OpenTelemetry for exporting traces. Install the `llama-index-observability-otel` package:
Terminal window
```


pipinstallllama-index-observability-otel


```

Then configure it in your application:

```


from llama_index.observability.otel import LlamaIndexOpenTelemetry




# Initialize with your span exporter



instrumentor = LlamaIndexOpenTelemetry(




span_exporter=your_span_exporter,




service_name_or_resource="your_service_name",





# Start registering traces


instrumentor.start_registering()

```

All workflow steps, LLM calls, and custom events are automatically captured and exported as OpenTelemetry spans with detailed attributes including:
  * Span names for each workflow step
  * Start and end times
  * Event attributes (input data, output data, etc.)
  * Nested span relationships showing execution flow


## Third-Party Observability Tools
[Section titled “Third-Party Observability Tools”](https://developers.llamaindex.ai/python/llamaagents/workflows/observability/#third-party-observability-tools)
Workflows integrate seamlessly with popular observability platforms:
### Arize Phoenix
[Section titled “Arize Phoenix”](https://developers.llamaindex.ai/python/llamaagents/workflows/observability/#arize-phoenix)
[Arize Phoenix](https://docs.arize.com/phoenix/integrations/frameworks/llamaindex/llamaindex-workflows-tracing) provides real-time tracing and visualization for your workflows.
You can read more in the [example notebook.](https://github.com/run-llama/llama-agents/blob/main/examples/observability/workflows_observablitiy_arize_phoenix.ipynb)
### Langfuse
[Section titled “Langfuse”](https://developers.llamaindex.ai/python/llamaagents/workflows/observability/#langfuse)
[Langfuse](https://github.com/langfuse/langfuse) directly integrates with the instrumentation system that ships with workflows.
You can read more in the [example notebook.](https://github.com/run-llama/llama-agents/blob/main/examples/observability/workflows_observablitiy_langfuse.ipynb)
### Opik
[Section titled “Opik”](https://developers.llamaindex.ai/python/llamaagents/workflows/observability/#opik)
[Opik](https://github.com/comet-ml/opik) can receive workflow traces through the same OpenTelemetry pipeline used by workflows.
To configure export to Opik, use the OpenTelemetry setup above and point your exporter to Opik’s OTLP endpoint. See the [Opik OpenTelemetry Python SDK guide](https://www.comet.com/docs/opik/integrations/opentelemetry-python-sdk).
## Custom Spans and Events
[Section titled “Custom Spans and Events”](https://developers.llamaindex.ai/python/llamaagents/workflows/observability/#custom-spans-and-events)
You can define custom spans and events using the LlamaIndex dispatcher to add fine-grained tracing to your code:

```


from llama_index_instrumentation import get_dispatcher




from llama_index_instrumentation.base import BaseEvent





dispatcher = get_dispatcher()




# Define custom events



classExampleEvent(BaseEvent):




data: str





classAnotherExampleEvent(BaseEvent):




print_statement: str




# Use the @dispatcher.span decorator


@dispatcher.span



defexample_fn(data: str) -> None:




dispatcher.event(ExampleEvent(data=data))




s ="This are example string data: "+ data




dispatcher.event(AnotherExampleEvent(print_statement=s))




print(s)


```

When you call instrumented functions, all spans and events are automatically captured by any configured tracing backend.
See complete examples in the [examples/observability](https://github.com/run-llama/llama-agents/tree/main/examples/observability) directory.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


