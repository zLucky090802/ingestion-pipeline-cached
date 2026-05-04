[Skip to content](https://developers.llamaindex.ai/python/framework/community/faq/llms/#_top)
LlamaIndex Framework
Open Source Community
[Large Language Models](https://developers.llamaindex.ai/python/framework/community/faq/llms/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Large Language Models
##### FAQ
[Section titled “FAQ”](https://developers.llamaindex.ai/python/framework/community/faq/llms/#faq)
  1. [How to use a custom/local embedding model?](https://developers.llamaindex.ai/python/framework/community/faq/llms/#1-how-to-define-a-custom-llm)
  2. [How to use a local hugging face embedding model?](https://developers.llamaindex.ai/python/framework/community/faq/llms/#2-how-to-use-a-different-openai-model)
  3. [How can I customize my prompt](https://developers.llamaindex.ai/python/framework/community/faq/llms/#3-how-can-i-customize-my-prompt)
  4. [Is it required to fine-tune my model?](https://developers.llamaindex.ai/python/framework/community/faq/llms/#4-is-it-required-to-fine-tune-my-model)
  5. [I want to the LLM answer in Chinese/Italian/French but only answers in English, how to proceed?](https://developers.llamaindex.ai/python/framework/community/faq/llms/#5-i-want-to-the-llm-answer-in-chineseitalianfrench-but-only-answers-in-english-how-to-proceed)
  6. [Is LlamaIndex GPU accelerated?](https://developers.llamaindex.ai/python/framework/community/faq/llms/#6-is-llamaindex-gpu-accelerated)


##### 1. How to define a custom LLM?
[Section titled “1. How to define a custom LLM?”](https://developers.llamaindex.ai/python/framework/community/faq/llms/#1-how-to-define-a-custom-llm)
You can access [Usage Custom](https://developers.llamaindex.ai/python/framework/module_guides/models/llms/usage_custom#example-using-a-custom-llm-model---advanced) to define a custom LLM.
##### 2. How to use a different OpenAI model?
[Section titled “2. How to use a different OpenAI model?”](https://developers.llamaindex.ai/python/framework/community/faq/llms/#2-how-to-use-a-different-openai-model)
To use a different OpenAI model you can access [Configure Model](https://developers.llamaindex.ai/python/examples/llm/openai) to set your own custom model.
##### 3. How can I customize my prompt?
[Section titled “3. How can I customize my prompt?”](https://developers.llamaindex.ai/python/framework/community/faq/llms/#3-how-can-i-customize-my-prompt)
You can access [Prompts](https://developers.llamaindex.ai/python/framework/module_guides/models/prompts) to learn how to customize your prompts.
##### 4. Is it required to fine-tune my model?
[Section titled “4. Is it required to fine-tune my model?”](https://developers.llamaindex.ai/python/framework/community/faq/llms/#4-is-it-required-to-fine-tune-my-model)
No. there’s isolated modules which might provide better results, but isn’t required, you can use llamaindex without needing to fine-tune the model.
##### 5. I want to the LLM answer in Chinese/Italian/French but only answers in English, how to proceed?
[Section titled “5. I want to the LLM answer in Chinese/Italian/French but only answers in English, how to proceed?”](https://developers.llamaindex.ai/python/framework/community/faq/llms/#5-i-want-to-the-llm-answer-in-chineseitalianfrench-but-only-answers-in-english-how-to-proceed)
To the LLM answer in another language more accurate you can update the prompts to enforce more the output language.

```


response = query_engine.query("Rest of your query... \nRespond in Italian")


```

Alternatively:

```


from llama_index.core import Settings




from llama_index.llms.openai import OpenAI





llm = OpenAI(system_prompt="Always respond in Italian.")




# set a global llm



Settings.llm = llm





query_engine = load_index_from_storage(




storage_context,



).as_query_engine()

```

##### 6. Is LlamaIndex GPU accelerated?
[Section titled “6. Is LlamaIndex GPU accelerated?”](https://developers.llamaindex.ai/python/framework/community/faq/llms/#6-is-llamaindex-gpu-accelerated)
Yes, you can run a language model (LLM) on a GPU when running it locally. You can find an example of setting up LLMs with GPU support in the [llama2 setup](https://developers.llamaindex.ai/python/examples/vector_stores/simpleindexdemollama-local) documentation.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


