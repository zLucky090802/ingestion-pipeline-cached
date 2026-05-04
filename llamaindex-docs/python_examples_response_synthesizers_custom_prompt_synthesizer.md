[Skip to content](https://developers.llamaindex.ai/python/examples/response_synthesizers/custom_prompt_synthesizer/#_top)
# Pydantic Tree Summarize 
In this notebook, we demonstrate how to use tree summarize with structured outputs. Specifically, tree summarize is used to output pydantic objects.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


!pip install llama-index


```


```


import os




import openai


```


```


os.environ["OPENAI_API_KEY"] ="sk-..."




openai.api_key = os.environ["OPENAI_API_KEY"]


```

## Download Data
[Section titled “Download Data”](https://developers.llamaindex.ai/python/examples/response_synthesizers/custom_prompt_synthesizer/#download-data)

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```

## Load Data
[Section titled “Load Data”](https://developers.llamaindex.ai/python/examples/response_synthesizers/custom_prompt_synthesizer/#load-data)

```


from llama_index.core import SimpleDirectoryReader


```


```


reader = SimpleDirectoryReader(




input_files=["./data/paul_graham/paul_graham_essay.txt"]



```


```


docs = reader.load_data()


```


```


text = docs[0].text


```

## Define Custom Prompt
[Section titled “Define Custom Prompt”](https://developers.llamaindex.ai/python/examples/response_synthesizers/custom_prompt_synthesizer/#define-custom-prompt)

```


from llama_index.core import PromptTemplate


```


```


# NOTE: we add an extra tone_name variable here




qa_prompt_tmpl = (




"Context information is below.\n"




"---------------------\n"




"{context_str}\n"




"---------------------\n"




"Given the context information and not prior knowledge, "




"answer the query.\n"




"Please also write the answer in the style of {tone_name}.\n"




"Query: {query_str}\n"




"Answer: "





qa_prompt = PromptTemplate(qa_prompt_tmpl)





refine_prompt_tmpl = (




"The original query is as follows: {query_str}\n"




"We have provided an existing answer: {existing_answer}\n"




"We have the opportunity to refine the existing answer "




"(only if needed) with some more context below.\n"




"------------\n"




"{context_msg}\n"




"------------\n"




"Given the new context, refine the original answer to better "




"answer the query. "




"Please also write the answer in the style of {tone_name}.\n"




"If the context isn't useful, return the original answer.\n"




"Refined Answer: "





refine_prompt = PromptTemplate(refine_prompt_tmpl)


```

## Try out Response Synthesis with Custom Prompt
[Section titled “Try out Response Synthesis with Custom Prompt”](https://developers.llamaindex.ai/python/examples/response_synthesizers/custom_prompt_synthesizer/#try-out-response-synthesis-with-custom-prompt)
We try out a few different response synthesis strategies with the custom prompt.

```


from llama_index.core.response_synthesizers import TreeSummarize, Refine




from llama_index.core.types import BaseModel




from typing import List


```


```


summarizer = TreeSummarize(verbose=True, summary_template=qa_prompt)


```


```


response = summarizer.get_response(




"who is Paul Graham?", [text], tone_name="a Shakespeare play"



```


```

5 text chunks after repacking


1 text chunks after repacking

```


```


print(str(response))


```


```

Paul Graham, a noble and esteemed gentleman, is a man of many talents and accomplishments. He hath traversed the realms of art, entrepreneurship, and writing, leaving a lasting impact on each. With his brush, he hath brought life to canvases, capturing the essence of what he saw. In the realm of technology, he hath revolutionized the way we do business, founding Viaweb and bringing the power of the web to entrepreneurs and artists alike. His wisdom and guidance hath shaped the future of technology and entrepreneurship through his co-founding of Y Combinator. But above all, Paul Graham is a visionary, a trailblazer, and a true Renaissance man, whose intellectual curiosity and quest for lasting creation hath inspired generations to come.

```


```


summarizer = Refine(




verbose=True, text_qa_template=qa_prompt, refine_template=refine_prompt



```


```


response = summarizer.get_response(




"who is Paul Graham?", [text], tone_name="a haiku"



```


```

> Refine context: made a living from a combination of modelling a...


> Refine context: to have studied art, because the main goal of a...


> Refine context: I had been intimately involved with building th...


> Refine context: I didn't understand what he meant, but graduall...

```


```


print(str(response))


```


```

Paul Graham, a web pioneer,


Co-founded Y Combinator,


But stepped down to ensure,


Long-term success and more.

```


```

# try with pydantic model



classBiography(BaseModel):




"""Data model for a biography."""





name: str




best_known_for: List[str]




extra_info: str


```


```


summarizer = TreeSummarize(




verbose=True, summary_template=qa_prompt, output_cls=Biography



```


```


response = summarizer.get_response(




"who is Paul Graham?", [text], tone_name="a business memo"



```


```

5 text chunks after repacking


1 text chunks after repacking

```


```


print(str(response))


```


```

name='Paul Graham' best_known_for=['Co-founder of Y Combinator', 'Writer', 'Investor'] extra_info="Paul Graham is a renowned entrepreneur, writer, and investor. He is best known as the co-founder of Y Combinator, a highly successful startup accelerator. Graham has played a significant role in shaping the startup ecosystem and has been instrumental in the success of numerous startups. He is also a prolific writer, known for his insightful essays on a wide range of topics, including technology, startups, and entrepreneurship. Graham's writings have been widely read and have had a profound impact on the tech community. In addition to his work with Y Combinator and his writing, Graham is also an active investor, providing seed funding and mentorship to early-stage startups. His contributions to the startup world have earned him a reputation as one of the most influential figures in the industry."

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


