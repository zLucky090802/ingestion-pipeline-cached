[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/llm/palm/#_top)
LlamaIndex Framework
Integrations
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# PaLM 
In this short notebook, we show how to use the PaLM LLM from Google in LlamaIndex: <https://ai.google/discover/palm2/>.
We use the `text-bison-001` model by default.
### Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/framework/integrations/llm/palm/#setup)
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-llms-palm


```


```


!pip install llama-index


```


```


!pip install -q google-generativeai


```


```

[1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip available: [0m[31;49m22.3.1[0m[39;49m -> [0m[32;49m23.1.2[0m


[1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m

```


```


import pprint




import google.generativeai as palm


```


```


palm_api_key =""


```


```


palm.configure(api_key=palm_api_key)


```

### Define Model
[Section titled “Define Model”](https://developers.llamaindex.ai/python/framework/integrations/llm/palm/#define-model)

```


models = [





forin palm.list_models()




if"generateText"in m.supported_generation_methods





model = models[0].name




print(model)


```


```

models/text-bison-001

```

### Start using our `PaLM` LLM abstraction!
[Section titled “Start using our PaLM LLM abstraction!”](https://developers.llamaindex.ai/python/framework/integrations/llm/palm/#start-using-our-palm-llm-abstraction)

```


from llama_index.llms.palm import PaLM





model = PaLM(api_key=palm_api_key)


```


```

model.complete(prompt)

```


```

CompletionResponse(text='1 house has 3 cats * 4 mittens / cat = 12 mittens.\n3 houses have 12 mittens / house * 3 houses = 36 mittens.\n1 hat needs 4m of yarn. 36 hats need 4m / hat * 36 hats = 144m of yarn.\n1 mitten needs 7m of yarn. 36 mittens need 7m / mitten * 36 mittens = 252m of yarn.\nIn total 144m of yarn was needed for hats and 252m of yarn was needed for mittens, so 144m + 252m = 396m of yarn was needed.\n\nThe answer: 396', additional_kwargs={}, raw={'output': '1 house has 3 cats * 4 mittens / cat = 12 mittens.\n3 houses have 12 mittens / house * 3 houses = 36 mittens.\n1 hat needs 4m of yarn. 36 hats need 4m / hat * 36 hats = 144m of yarn.\n1 mitten needs 7m of yarn. 36 mittens need 7m / mitten * 36 mittens = 252m of yarn.\nIn total 144m of yarn was needed for hats and 252m of yarn was needed for mittens, so 144m + 252m = 396m of yarn was needed.\n\nThe answer: 396', 'safety_ratings': [{'category': <HarmCategory.HARM_CATEGORY_DEROGATORY: 1>, 'probability': <HarmProbability.NEGLIGIBLE: 1>}, {'category': <HarmCategory.HARM_CATEGORY_TOXICITY: 2>, 'probability': <HarmProbability.NEGLIGIBLE: 1>}, {'category': <HarmCategory.HARM_CATEGORY_VIOLENCE: 3>, 'probability': <HarmProbability.NEGLIGIBLE: 1>}, {'category': <HarmCategory.HARM_CATEGORY_SEXUAL: 4>, 'probability': <HarmProbability.NEGLIGIBLE: 1>}, {'category': <HarmCategory.HARM_CATEGORY_MEDICAL: 5>, 'probability': <HarmProbability.NEGLIGIBLE: 1>}, {'category': <HarmCategory.HARM_CATEGORY_DANGEROUS: 6>, 'probability': <HarmProbability.NEGLIGIBLE: 1>}]}, delta=None)

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


