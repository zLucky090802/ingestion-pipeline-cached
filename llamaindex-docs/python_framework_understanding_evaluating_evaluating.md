[Skip to content](https://developers.llamaindex.ai/python/framework/understanding/evaluating/evaluating/#_top)
LlamaIndex Framework
Learn
Evaluating
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Evaluating
Evaluation and benchmarking are crucial concepts in LLM development. To improve the performance of an LLM app (RAG, agents), you must have a way to measure it.
LlamaIndex offers key modules to measure the quality of generated results. We also offer key modules to measure retrieval quality. You can learn more about how evaluation works in LlamaIndex in our [module guides](https://developers.llamaindex.ai/python/framework/module_guides/evaluating).
## Response Evaluation
[Section titled “Response Evaluation”](https://developers.llamaindex.ai/python/framework/understanding/evaluating/evaluating/#response-evaluation)
Does the response match the retrieved context? Does it also match the query? Does it match the reference answer or guidelines? Here’s a simple example that evaluates a single response for Faithfulness, i.e. whether the response is aligned to the context, such as being free from hallucinations:

```


from llama_index.core import VectorStoreIndex




from llama_index.llms.openai import OpenAI




from llama_index.core.evaluation import FaithfulnessEvaluator




# create llm



llm = OpenAI(model="gpt-4", temperature=0.0)




# build index




vector_index = VectorStoreIndex(...)




# define evaluator



evaluator = FaithfulnessEvaluator(llm=llm)




# query index



query_engine = vector_index.as_query_engine()




response = query_engine.query(




"What battles took place in New York City in the American Revolution?"





eval_result = evaluator.evaluate_response(response=response)




print(str(eval_result.passing))


```

The response contains both the response and the source from which the response was generated; the evaluator compares them and determines if the response is faithful to the source.
You can learn more in our module guides about [response evaluation](https://developers.llamaindex.ai/python/framework/module_guides/evaluating/usage_pattern).
## Retrieval Evaluation
[Section titled “Retrieval Evaluation”](https://developers.llamaindex.ai/python/framework/understanding/evaluating/evaluating/#retrieval-evaluation)
Are the retrieved sources relevant to the query? This is a simple example that evaluates a single retrieval:

```


from llama_index.core.evaluation import RetrieverEvaluator




# define retriever somewhere (e.g. from index)


# retriever = index.as_retriever(similarity_top_k=2)



retriever =...





retriever_evaluator = RetrieverEvaluator.from_metric_names(




["mrr", "hit_rate"], retriever=retriever





retriever_evaluator.evaluate(



query="query", expected_ids=["node_id1", "node_id2"]



```

This compares what was retrieved for the query to a set of nodes that were expected to be retrieved.
In reality you would want to evaluate a whole batch of retrievals; you can learn how do this in our module guide on [retrieval evaluation](https://developers.llamaindex.ai/python/framework/module_guides/evaluating/usage_pattern_retrieval).
## Related concepts
[Section titled “Related concepts”](https://developers.llamaindex.ai/python/framework/understanding/evaluating/evaluating/#related-concepts)
You may be interested in [analyzing the cost of your application](https://developers.llamaindex.ai/python/framework/understanding/evaluating/cost_analysis) if you are making calls to a hosted, remote LLM.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


