[Skip to content](https://developers.llamaindex.ai/python/examples/query_engine/polars_query_engine/#_top)
# Polars Query Engine 
This guide shows you how to use our `PolarsQueryEngine`: convert natural language to Polars python code using LLMs.
The input to the `PolarsQueryEngine` is a Polars dataframe, and the output is a response. The LLM infers dataframe operations to perform in order to retrieve the result.
**WARNING:** This tool provides the LLM access to the `eval` function. Arbitrary code execution is possible on the machine running this tool. While some level of filtering is done on code, this tool is not recommended to be used in a production setting without heavy sandboxing or virtual machines.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


!pip install llama-index llama-index-experimental polars


```


```


import logging




import sys




from IPython.display import Markdown, display





import polars as pl




from llama_index.experimental.query_engine import PolarsQueryEngine






logging.basicConfig(stream=sys.stdout, level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


```

## Let’s start on a Toy DataFrame
[Section titled “Let’s start on a Toy DataFrame”](https://developers.llamaindex.ai/python/examples/query_engine/polars_query_engine/#lets-start-on-a-toy-dataframe)
Here let’s load a very simple dataframe containing city and population pairs, and run the `PolarsQueryEngine` on it.
By setting `verbose=True` we can see the intermediate generated instructions.

```

# Test on some sample data



df = pl.DataFrame(





"city": ["Toronto", "Tokyo", "Berlin"],




"population": [2930000, 13960000, 3645000],




```


```


query_engine = PolarsQueryEngine(df=df, verbose=True)


```


```


response = query_engine.query(




"What is the city with the highest population?",



```


```


display(Markdown(f"<b>{response}</b>"))


```


```

# get polars python instructions



print(response.metadata["polars_instruction_str"])


```

We can also take the step of using an LLM to synthesize a response.

```


query_engine = PolarsQueryEngine(df=df, verbose=True, synthesize_response=True)




response = query_engine.query(




"What is the city with the highest population? Give both the city and population",





print(str(response))


```

## Analyzing the Titanic Dataset
[Section titled “Analyzing the Titanic Dataset”](https://developers.llamaindex.ai/python/examples/query_engine/polars_query_engine/#analyzing-the-titanic-dataset)
The Titanic dataset is one of the most popular tabular datasets in introductory machine learning Source: <https://www.kaggle.com/c/titanic>
#### Download Data
[Section titled “Download Data”](https://developers.llamaindex.ai/python/examples/query_engine/polars_query_engine/#download-data)

```


!wget 'https://raw.githubusercontent.com/jerryjliu/llama_index/main/docs/examples/data/csv/titanic_train.csv'-O 'titanic_train.csv'


```


```


df = pl.read_csv("./titanic_train.csv")


```


```


query_engine = PolarsQueryEngine(df=df, verbose=True)


```


```


response = query_engine.query(




"What is the correlation between survival and age?",



```


```


display(Markdown(f"<b>{response}</b>"))


```

## Additional Steps
[Section titled “Additional Steps”](https://developers.llamaindex.ai/python/examples/query_engine/polars_query_engine/#additional-steps)
### Analyzing / Modifying prompts
[Section titled “Analyzing / Modifying prompts”](https://developers.llamaindex.ai/python/examples/query_engine/polars_query_engine/#analyzing--modifying-prompts)
Let’s look at the prompts!

```


from llama_index.core import PromptTemplate


```


```


query_engine = PolarsQueryEngine(df=df, verbose=True)




prompts = query_engine.get_prompts()




print(prompts["polars_prompt"].template)


```


```


print(prompts["response_synthesis_prompt"].template)


```

You can update prompts as well:

```


new_prompt = PromptTemplate(




You are working with a polars dataframe in Python.


The name of the dataframe is `df`.


This is the result of `print(df.head())`:


{df_str}



Follow these instructions:


{instruction_str}



Query: {query_str}




Expression: """





query_engine.update_prompts({"polars_prompt": new_prompt})


```

This is the instruction string (that you can customize by passing in `instruction_str` on initialization)

```


instruction_str ="""\



1. Convert the query to executable Python code using Polars.


2. The final line of code should be a Python expression that can be called with the `eval()` function.


3. The code should represent a solution to the query.


4. PRINT ONLY THE EXPRESSION.


5. Do not quote the expression.


```

### Implementing Query Engine using Query Pipeline Syntax
[Section titled “Implementing Query Engine using Query Pipeline Syntax”](https://developers.llamaindex.ai/python/examples/query_engine/polars_query_engine/#implementing-query-engine-using-query-pipeline-syntax)
If you want to learn to construct your own Polars Query Engine using our Query Pipeline syntax and the prompt components above, you can adapt the techniques from our Pandas Query Pipeline tutorial.
[Setting up a Pandas DataFrame query engine with Query Pipelines](https://docs.llamaindex.ai/en/stable/examples/pipeline/query_pipeline_pandas.html)
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


