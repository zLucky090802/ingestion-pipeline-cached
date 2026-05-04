[Skip to content](https://developers.llamaindex.ai/python/examples/evaluation/deepeval/#_top)
# 🚀 DeepEval - Open Source Evals with Tracing 
This code tutorial shows how you can easily trace and evaluate your LlamaIndex Agents. You can read more about the DeepEval framework here: <https://docs.confident-ai.com/docs/getting-started>
LlamaIndex integration with DeepEval allows you to trace your LlamaIndex Agents and evaluate them using DeepEval’s default metrics. Read more about the integration here: <https://deepeval.com/integrations/frameworks/langchain>
Feel free to check out our repository here on GitHub: <https://github.com/confident-ai/deepeval>
### Quickstart
[Section titled “Quickstart”](https://developers.llamaindex.ai/python/examples/evaluation/deepeval/#quickstart)
Install the following packages:

```


!pip install -q -q llama-index




!pip install -U -q deepeval


```

This step is optional and only if you want a server-hosted dashboard! (Psst I think you should!)

```


!deepeval login


```

### End-to-End Evals
[Section titled “End-to-End Evals”](https://developers.llamaindex.ai/python/examples/evaluation/deepeval/#end-to-end-evals)
`deepeval` allows you to evaluate LlamaIndex applications end-to-end in under a minute.
Create a `FunctionAgent` with a list of metrics you wish to use, and pass it to your LlamaIndex application’s `run` method.

```


import asyncio





from llama_index.llms.openai import OpenAI




import llama_index.core.instrumentation as instrument





from deepeval.integrations.llama_index import (




instrument_llama_index,




FunctionAgent,





from deepeval.metrics import AnswerRelevancyMetric




instrument_llama_index(instrument.get_dispatcher())





defmultiply(a: float, b: float) -> float:




"""Useful for multiplying two numbers."""




return* b






answer_relevancy_metric = AnswerRelevancyMetric()





agent = FunctionAgent(




tools=[multiply],




llm=OpenAI(model="gpt-4o-mini"),




system_prompt="You are a helpful assistant that can perform calculations.",




metrics=[answer_relevancy_metric],







asyncdefllm_app(input: str):




returnawait agent.run(input)






asyncio.run(llm_app("What is 2 * 3?"))


```

Evaluations are supported for LlamaIndex `FunctionAgent`, `ReActAgent` and `CodeActAgent`. Only metrics with LLM parameters input and output are eligible for evaluation.
#### Synchronous
[Section titled “Synchronous”](https://developers.llamaindex.ai/python/examples/evaluation/deepeval/#synchronous)
Create a `FunctionAgent` with a list of metrics you wish to use, and pass it to your LlamaIndex application’s run method.

```


from deepeval.dataset import EvaluationDataset, Golden





dataset = EvaluationDataset(




goldens=[Golden(input="What is 3 * 12?"), Golden(input="What is 4 * 13?")]






for golden in dataset.evals_iterator():




task = asyncio.create_task(llm_app(golden.input))




dataset.evaluate(task)


```

### Asynchronous
[Section titled “Asynchronous”](https://developers.llamaindex.ai/python/examples/evaluation/deepeval/#asynchronous)

```


from deepeval.dataset import EvaluationDataset, Golden




import asyncio





dataset = EvaluationDataset(




goldens=[Golden(input="What's 7 * 8?"), Golden(input="What's 7 * 6?")]






for golden in dataset.evals_iterator():




task = asyncio.create_task(llm_app(golden.input))




dataset.evaluate(task)


```

#### ⚠️ Warning: DeepEval runs using event loops for managing asynchronous operations.
[Section titled “⚠️ Warning: DeepEval runs using event loops for managing asynchronous operations.”](https://developers.llamaindex.ai/python/examples/evaluation/deepeval/#%EF%B8%8F-warning-deepeval-runs-using-event-loops-for-managing-asynchronous-operations)
Jupyter notebooks already maintain their own event loop, which may lead to unexpected behavior, hangs, or runtime errors when running DeepEval examples directly in a notebook cell.
Recommendation: To avoid such issues, run your DeepEval examples in a standalone Python script (.py file) instead of within Jupyter Notebook.
### Examples
[Section titled “Examples”](https://developers.llamaindex.ai/python/examples/evaluation/deepeval/#examples)
Here are some examples scripts.

```

# Synchronous (End-to-End Evals)



import os




import deepeval




import asyncio





from llama_index.llms.openai import OpenAI




import llama_index.core.instrumentation as instrument





from deepeval.integrations.llama_index import instrument_llama_index




from deepeval.integrations.llama_index import FunctionAgent




from deepeval.metrics import AnswerRelevancyMetric




from deepeval.dataset import EvaluationDataset, Golden





from dotenv import load_dotenv




load_dotenv()




deepeval.login(os.getenv("CONFIDENT_API_KEY"))



instrument_llama_index(instrument.get_dispatcher())





defmultiply(a: float, b: float) -> float:




"""Useful for multiplying two numbers."""




return* b






answer_relevancy_metric = AnswerRelevancyMetric()




agent = FunctionAgent(




tools=[multiply],




llm=OpenAI(model="gpt-4o-mini"),




system_prompt="You are a helpful assistant that can perform calculations.",




metrics=[answer_relevancy_metric],







asyncdefllm_app(input: str):




returnawait agent.run(input)






dataset = EvaluationDataset(




goldens=[Golden(input="What is 3 * 12?"), Golden(input="What is 4 * 13?")]





for golden in dataset.evals_iterator():




task = asyncio.create_task(llm_app(golden.input))




dataset.evaluate(task)


```


```

# Asynchronous (End-to-End Evals)



import os




from deepeval.integrations.llama_index import instrument_llama_index




import llama_index.core.instrumentation as instrument




from deepeval.integrations.llama_index import FunctionAgent




from llama_index.llms.openai import OpenAI




import asyncio




import time





import deepeval




from deepeval.metrics import AnswerRelevancyMetric




from deepeval.dataset import EvaluationDataset, Golden




from dotenv import load_dotenv




load_dotenv()




# Don't forget to setup tracing



deepeval.login(os.getenv("CONFIDENT_API_KEY"))



instrument_llama_index(instrument.get_dispatcher())





defmultiply(a: float, b: float) -> float:




"""Useful for multiplying two numbers."""




return* b






answer_relevancy_metric = AnswerRelevancyMetric()




agent = FunctionAgent(




tools=[multiply],




llm=OpenAI(model="gpt-4o-mini"),




system_prompt="You are a helpful assistant that can perform calculations.",




metrics=[answer_relevancy_metric],






goldens = [Golden(input="What's 7 * 8?"), Golden(input="What's 7 * 6?")]






asyncdefllm_app(golden: Golden):




await agent.run(golden.input)






defmain():




dataset = EvaluationDataset(goldens=goldens)




for golden in dataset.evals_iterator():




task = asyncio.create_task(llm_app(golden))




dataset.evaluate(task)






if__name__=="__main__":




main()


```


```


import os




from deepeval.integrations.llama_index import instrument_llama_index




import llama_index.core.instrumentation as instrument




from deepeval.integrations.llama_index import FunctionAgent




from llama_index.llms.openai import OpenAI




import asyncio





import deepeval




from dotenv import load_dotenv




load_dotenv()



# Don't forget to setup tracing



deepeval.login(os.getenv("CONFIDENT_API_KEY"))



instrument_llama_index(instrument.get_dispatcher())





defmultiply(a: float, b: float) -> float:




"""Useful for multiplying two numbers."""




return* b






agent = FunctionAgent(




tools=[multiply],




llm=OpenAI(model="gpt-4o-mini"),




system_prompt="You are a helpful assistant that can perform calculations.",




metric_collection="test_collection_1",







asyncdefllm_app(golden: Golden):




await agent.run(golden.input)






asyncio.run(llm_app(Golden(input="What is 3 * 12?")))


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


