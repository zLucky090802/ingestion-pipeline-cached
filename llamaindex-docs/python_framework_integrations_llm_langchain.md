[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/llm/langchain/#_top)
LlamaIndex Framework
Integrations
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# LangChain LLM 

```


%pip install llama-index-llms-langchain


```


```


from langchain.llms import OpenAI


```


```


from llama_index.llms.langchain import LangChainLLM


```


```


llm = LangChainLLM(llm=OpenAI())


```


```


response_gen = llm.stream_complete("Hi this is")


```


```


for delta in response_gen:




print(delta.delta, end="")


```


```


a test




Hello! Welcome to the test. What would you like to learn about?

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


