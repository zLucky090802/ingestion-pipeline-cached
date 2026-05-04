[Skip to content](https://developers.llamaindex.ai/python/framework/community/integrations/trulens/#_top)
LlamaIndex Framework
Open Source Community
Integrations
[Evaluating and Tracking with TruLens](https://developers.llamaindex.ai/python/framework/community/integrations/trulens/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Evaluating and Tracking with TruLens
This page covers how to use [TruLens](https://trulens.org) to evaluate and track LLM apps built on Llama-Index.
## What is TruLens?
[Section titled “What is TruLens?”](https://developers.llamaindex.ai/python/framework/community/integrations/trulens/#what-is-trulens)
TruLens is an [opensource](https://github.com/truera/trulens) package that provides instrumentation and evaluation tools for large language model (LLM) based applications. This includes feedback function evaluations of relevance, sentiment and more, plus in-depth tracing including cost and latency.
As you iterate on new versions of your LLM application, you can compare their performance across all of the different quality metrics you’ve set up. You’ll also be able to view evaluations at a record level, and explore the app metadata for each record.
### Installation and Setup
[Section titled “Installation and Setup”](https://developers.llamaindex.ai/python/framework/community/integrations/trulens/#installation-and-setup)
Adding TruLens is simple, just install it from pypi!
Terminal window
```


pipinstalltrulens-eval


```


```


from trulens_eval import TruLlama


```

## Try it out!
[Section titled “Try it out!”](https://developers.llamaindex.ai/python/framework/community/integrations/trulens/#try-it-out)
[llama_index_quickstart.ipynb](https://github.com/truera/trulens/blob/trulens-eval-0.20.3/trulens_eval/examples/quickstart/llama_index_quickstart.ipynb)
## Read more
[Section titled “Read more”](https://developers.llamaindex.ai/python/framework/community/integrations/trulens/#read-more)
  * [Build and Evaluate LLM Apps with LlamaIndex and TruLens](https://medium.com/llamaindex-blog/build-and-evaluate-llm-apps-with-llamaindex-and-trulens-6749e030d83c)


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


