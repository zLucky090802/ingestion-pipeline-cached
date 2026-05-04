[Skip to content](https://developers.llamaindex.ai/python/llamaagents/workflows/resources/#_top)
LlamaAgents
Agent Workflows
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Resource Objects
Resources are external dependencies you can inject into the steps of a workflow.
As a simple example, look at `memory` from llama-index in the following workflow:

```


from typing import Annotated





from workflows import Workflow, step




from workflows.events import Event, StartEvent, StopEvent




from workflows.resource import Resource




from llama_index.core.llms import ChatMessage




from llama_index.core.memory import Memory






defget_memory(*args, **kwargs):




return Memory.from_defaults("user_id_123", token_limit=60000)






classSecondEvent(Event):




msg: str






classWorkflowWithResource(Workflow):




@step




asyncdeffirst_step(




self,




ev: StartEvent,




memory: Annotated[Memory, Resource(get_memory)],




) -> SecondEvent:




print("Memory before step 1", memory)




await memory.aput(




ChatMessage(role="user", content="This is the first step")





print("Memory after step 1", memory)




return SecondEvent(msg="This is an input for step 2")





@step




asyncdefsecond_step(




self, ev: SecondEvent, memory: Annotated[Memory, Resource(get_memory)]




) -> StopEvent:




print("Memory before step 2", memory)




await memory.aput(ChatMessage(role="user", content=ev.msg))




print("Memory after step 2", memory)




return StopEvent(result="Messages put into memory")


```

To inject a resource into a workflow step, you have to add a parameter to the step signature and define its type, using `Annotated` and invoke the `Resource()` wrapper passing a function or callable returning the actual Resource object. The return type of the wrapped function must match the declared type, ensuring consistency between what’s expected and what’s provided during execution. In the example above, `memory: Annotated[Memory, Resource(get_memory)` defines a resource of type `Memory` that will be provided by the `get_memory()` function and passed to the step in the `memory` parameter when the workflow runs.
Resources are shared among steps of a workflow, and the `Resource()` wrapper will invoke the factory function only once. In case this is not the desired behavior, passing `cache=False` to `Resource()` will inject different resource objects in different steps, invoking the factory function as many times.
## Config-backed Resources
[Section titled “Config-backed Resources”](https://developers.llamaindex.ai/python/llamaagents/workflows/resources/#config-backed-resources)
For configuration data stored in JSON files, use `ResourceConfig` instead of `Resource`. It automatically loads a JSON file and parses it into a Pydantic model.

```


from typing import Annotated




from pydantic import BaseModel




from workflows import Workflow, step




from workflows.events import StartEvent, StopEvent




from workflows.resource import ResourceConfig






classClassifierConfig(BaseModel):




categories: list[str]




threshold: float






classDocumentClassifier(Workflow):




@step




asyncdefclassify(




self,




ev: StartEvent,




config: Annotated[




ClassifierConfig,




ResourceConfig(config_file="classifier.json"),





) -> StopEvent:




# config is loaded from classifier.json and validated as ClassifierConfig




return StopEvent(result=f"Using threshold: {config.threshold}")


```

### Parameters
[Section titled “Parameters”](https://developers.llamaindex.ai/python/llamaagents/workflows/resources/#parameters)
  * `config_file`: Path to the JSON file containing the configuration.
  * `path_selector`: Optional ”.” delimited JSON path to extract a nested value from the json in the config file (e.g., `"settings.classifier"`).
  * `label`: Optional display name for workflow visualizations.
  * `description`: Optional description for workflow visualizations.


### Selecting nested values
[Section titled “Selecting nested values”](https://developers.llamaindex.ai/python/llamaagents/workflows/resources/#selecting-nested-values)
If your JSON file contains multiple configs, use `path_selector` to extract a specific section:

```

# Given config.json: {"classifier": {"categories": [...], "threshold": 0.8}, "other": {...}}


config: Annotated[



ClassifierConfig,




ResourceConfig(config_file="config.json", path_selector="classifier"),



```

### Labels and descriptions in visualizations
[Section titled “Labels and descriptions in visualizations”](https://developers.llamaindex.ai/python/llamaagents/workflows/resources/#labels-and-descriptions-in-visualizations)
When viewing workflows in the debugger or other visualization tools, `label` and `description` help identify configs:

```

config: Annotated[



ClassifierConfig,




ResourceConfig(




config_file="classifier.json",




label="Document Classifier",




description="Categories and confidence threshold for classification",




```

If no label is provided, the Pydantic model’s type name is used (e.g., “ClassifierConfig”).
## Chaining Resources
[Section titled “Chaining Resources”](https://developers.llamaindex.ai/python/llamaagents/workflows/resources/#chaining-resources)
Resources and ResourceConfigs can be chained together. A `Resource` factory function can declare dependencies on other resources using the same `Annotated` pattern:

```


from typing import Annotated




from pydantic import BaseModel




from workflows import Workflow, step




from workflows.events import StartEvent, StopEvent




from workflows.resource import Resource, ResourceConfig




from llama_index.llms.anthropic import Anthropic






classLLMConfig(BaseModel):




model: str




temperature: float




max_tokens: int






defget_llm(




config: Annotated[LLMConfig, ResourceConfig(config_file="llm.json")],



) -> Anthropic:



return Anthropic(




model=config.model,




temperature=config.temperature,




max_tokens=config.max_tokens,







classMyWorkflow(Workflow):




@step




asyncdefgenerate(




self,




ev: StartEvent,




llm: Annotated[Anthropic, Resource(get_llm)],




) -> StopEvent:




response =await llm.acomplete(ev.input)




return StopEvent(result=response.text)


```

The dependency chain is resolved automatically. In this example, when the workflow runs:
  1. `llm.json` is loaded and parsed into `LLMConfig`
  2. `get_llm` is called with that config to create the LLM client
  3. The resulting client is passed to the step


This pattern works with any combination of `Resource` and `ResourceConfig` dependencies.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


