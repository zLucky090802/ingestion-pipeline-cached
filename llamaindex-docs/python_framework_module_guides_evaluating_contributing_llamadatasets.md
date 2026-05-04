[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/evaluating/contributing_llamadatasets/#_top)
LlamaIndex Framework
Component Guides
Evaluating
[Contributing A `LabelledRagDataset`](https://developers.llamaindex.ai/python/framework/module_guides/evaluating/contributing_llamadatasets/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Contributing A `LabelledRagDataset`
Building a more robust RAG system requires a diversified evaluation suite. That is why we launched `LlamaDatasets` in [llama-hub](https://llamahub.ai). In this page, we discuss how you can contribute the first kind of `LlamaDataset` made available in llama-hub, that is, `LabelledRagDataset`.
Contributing a `LabelledRagDataset` involves two high level steps. Generally speaking, you must create the `LabelledRagDataset`, save it as a json and submit both this json file and the source text files to our [llama-datasets repository](https://github.com/run-llama/llama_datasets). Additionally, you’ll have to make a pull request, to upload required metadata of the dataset to our [llama-hub repository](https://github.com/run-llama/llama-hub).
To help make the submission process a lot smoother, we’ve prepared a template notebook that you can follow to create a `LabelledRagDataset` from scratch (or convert a similarly structured question-answering dataset into one) and perform other required steps to make your submission. Please refer to the “LlamaDataset Submission Template Notebook” linked below.
## Contributing Other llama-datasets
[Section titled “Contributing Other llama-datasets”](https://developers.llamaindex.ai/python/framework/module_guides/evaluating/contributing_llamadatasets/#contributing-other-llama-datasets)
The general process for contributing any of our other llama-datasets such as the `LabelledEvaluatorDataset` is the same as for the `LabelledRagDataset` previously described. Submission templates for these other datasets are coming soon!
## Submission Example
[Section titled “Submission Example”](https://developers.llamaindex.ai/python/framework/module_guides/evaluating/contributing_llamadatasets/#submission-example)
Read the full [submission example Notebook](https://developers.llamaindex.ai/python/examples/llama_dataset/ragdataset_submission_template).
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


