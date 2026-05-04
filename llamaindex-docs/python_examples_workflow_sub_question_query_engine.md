[Skip to content](https://developers.llamaindex.ai/python/examples/workflow/sub_question_query_engine/#_top)
# Sub Question Query Engine as a workflow 
LlamaIndex has a built-in Sub-Question Query Engine. Here, we replace it with a Workflow-based equivalent.
First we install our dependencies:
  * LlamaIndex core for most things
  * OpenAI LLM and embeddings for LLM actions
  * `llama-index-readers-file` to power the PDF reader in `SimpleDirectoryReader`



```


!pip install llama-index-core llama-index-llms-openai llama-index-embeddings-openai llama-index-readers-file llama-index-utils-workflow


```

Bring in our dependencies as imports:

```


import os, json




from llama_index.core import (




SimpleDirectoryReader,




VectorStoreIndex,




StorageContext,




load_index_from_storage,





from llama_index.core.tools import QueryEngineTool, ToolMetadata




from llama_index.core.workflow import (




step,




Context,




Workflow,




Event,




StartEvent,




StopEvent,





from llama_index.core.agent import ReActAgent




from llama_index.llms.openai import OpenAI




from llama_index.utils.workflow import draw_all_possible_flows


```

# Define the Sub Question Query Engine as a Workflow
[Section titled “Define the Sub Question Query Engine as a Workflow”](https://developers.llamaindex.ai/python/examples/workflow/sub_question_query_engine/#define-the-sub-question-query-engine-as-a-workflow)
  * Our StartEvent goes to `query()`, which takes care of several things:
    * Accepts and stores the original query
    * Stores the LLM to handle the queries
    * Stores the list of tools to enable sub-questions
    * Passes the original question to the LLM, asking it to split up the question into sub-questions
    * Fires off a `QueryEvent` for every sub-question generated
  * QueryEvents go to `sub_question()`, which instantiates a new ReAct agent with the full list of tools available and lets it select which one to use.
    * This is slightly better than the actual SQQE built-in to LlamaIndex, which cannot use multiple tools
    * Each QueryEvent generates an `AnswerEvent`
  * AnswerEvents go to `combine_answers()`.
    * This uses `self.collect_events()` to wait for every QueryEvent to return an answer.
    * All the answers are then combined into a final prompt for the LLM to consolidate them into a single response
    * A StopEvent is generated to return the final result



```


classQueryEvent(Event):




question: str






classAnswerEvent(Event):




question: str




answer: str






classSubQuestionQueryEngine(Workflow):




@step




asyncdefquery(self, ctx: Context, ev: StartEvent) -> QueryEvent:




ifhasattr(ev, "query"):




await ctx.store.set("original_query", ev.query)




print(f"Query is {await ctx.store.get('original_query')}")





ifhasattr(ev, "llm"):




await ctx.store.set("llm", ev.llm)





ifhasattr(ev, "tools"):




await ctx.store.set("tools", ev.tools)





response = (await ctx.store.get("llm")).complete(





Given a user question, and a list of tools, output a list of




relevant sub-questions, such that the answers to all the




sub-questions put together will answer the question. Respond




in pure JSON without any markdown, like this:





"sub_questions": [




"What is the population of San Francisco?",




"What is the budget of San Francisco?",




"What is the GDP of San Francisco?"






Here is the user question: {await ctx.store.get('original_query')}





And here is the list of tools: {await ctx.store.get('tools')}







print(f"Sub-questions are {response}")





response_obj = json.loads(str(response))




sub_questions = response_obj["sub_questions"]





await ctx.store.set("sub_question_count", len(sub_questions))





for question in sub_questions:




self.send_event(QueryEvent(question=question))





returnNone





@step




asyncdefsub_question(self, ctx: Context, ev: QueryEvent) -> AnswerEvent:




print(f"Sub-question is {ev.question}")





agent = ReActAgent.from_tools(




await ctx.store.get("tools"),




llm=await ctx.store.get("llm"),




verbose=True,





response = agent.chat(ev.question)





return AnswerEvent(question=ev.question, answer=str(response))





@step




asyncdefcombine_answers(




self, ctx: Context, ev: AnswerEvent




) -> StopEvent |None:




ready = ctx.collect_events(




ev, [AnswerEvent] *await ctx.store.get("sub_question_count")





if ready isNone:




returnNone





answers ="\n\n".join(





f"Question: {event.question}: \n Answer: {event.answer}"




for event in ready







prompt =f"""




You are given an overall question that has been split into sub-questions,




each of which has been answered. Combine the answers to all the sub-questions




into a single answer to the original question.





Original question: {await ctx.store.get('original_query')}





Sub-questions and answers:




{answers}






print(f"Final prompt is {prompt}")





response = (await ctx.store.get("llm")).complete(prompt)





print("Final response is", response)





return StopEvent(result=str(response))


```


```

draw_all_possible_flows(



SubQuestionQueryEngine, filename="sub_question_query_engine.html"



```


```

sub_question_query_engine.html

```

Visualizing this flow looks pretty linear, since it doesn’t capture that `query()` can generate multiple parallel `QueryEvents` which get collected into `combine_answers`.
# Download data to demo
[Section titled “Download data to demo”](https://developers.llamaindex.ai/python/examples/workflow/sub_question_query_engine/#download-data-to-demo)

```


!mkdir -p "./data/sf_budgets/"




!wget "https://www.dropbox.com/scl/fi/xt3squt47djba0j7emmjb/2016-CSF_Budget_Book_2016_FINAL_WEB_with-cover-page.pdf?rlkey=xs064cjs8cb4wma6t5pw2u2bl&dl=0"-O "./data/sf_budgets/2016 - CSF_Budget_Book_2016_FINAL_WEB_with-cover-page.pdf"




!wget "https://www.dropbox.com/scl/fi/jvw59g5nscu1m7f96tjre/2017-Proposed-Budget-FY2017-18-FY2018-19_1.pdf?rlkey=v988oigs2whtcy87ti9wti6od&dl=0"-O "./data/sf_budgets/2017 - 2017-Proposed-Budget-FY2017-18-FY2018-19_1.pdf"




!wget "https://www.dropbox.com/scl/fi/izknlwmbs7ia0lbn7zzyx/2018-o0181-18.pdf?rlkey=p5nv2ehtp7272ege3m9diqhei&dl=0"-O "./data/sf_budgets/2018 - 2018-o0181-18.pdf"




!wget "https://www.dropbox.com/scl/fi/1rstqm9rh5u5fr0tcjnxj/2019-Proposed-Budget-FY2019-20-FY2020-21.pdf?rlkey=3s2ivfx7z9bev1r840dlpbcgg&dl=0"-O "./data/sf_budgets/2019 - 2019-Proposed-Budget-FY2019-20-FY2020-21.pdf"




!wget "https://www.dropbox.com/scl/fi/7teuwxrjdyvgw0n8jjvk0/2021-AAO-FY20-21-FY21-22-09-11-2020-FINAL.pdf?rlkey=6br3wzxwj5fv1f1l8e69nbmhk&dl=0"-O "./data/sf_budgets/2021 - 2021-AAO-FY20-21-FY21-22-09-11-2020-FINAL.pdf"




!wget "https://www.dropbox.com/scl/fi/zhgqch4n6xbv9skgcknij/2022-AAO-FY2021-22-FY2022-23-FINAL-20210730.pdf?rlkey=h78t65dfaz3mqbpbhl1u9e309&dl=0"-O "./data/sf_budgets/2022 - 2022-AAO-FY2021-22-FY2022-23-FINAL-20210730.pdf"




!wget "https://www.dropbox.com/scl/fi/vip161t63s56vd94neqlt/2023-CSF_Proposed_Budget_Book_June_2023_Master_Web.pdf?rlkey=hemoce3w1jsuf6s2bz87g549i&dl=0"-O "./data/sf_budgets/2023 - 2023-CSF_Proposed_Budget_Book_June_2023_Master_Web.pdf"


```


```

--2024-08-07 18:21:11--  https://www.dropbox.com/scl/fi/xt3squt47djba0j7emmjb/2016-CSF_Budget_Book_2016_FINAL_WEB_with-cover-page.pdf?rlkey=xs064cjs8cb4wma6t5pw2u2bl&dl=0


Resolving www.dropbox.com (www.dropbox.com)... 162.125.1.18, 2620:100:6057:18::a27d:d12


Connecting to www.dropbox.com (www.dropbox.com)|162.125.1.18|:443... connected.


HTTP request sent, awaiting response... 302 Found


Location: https://ucca241228aca55dbf9fcd60ae81.dl.dropboxusercontent.com/cd/0/inline/CYOq1NGkhLkELMmygLIg_gyLPXsOO7xOLjc3jW-mb09kevMykGPogSQx_icUTBEfHshxiSainXTynZYnh5O6uZ4ITeGiMkpvjl1QqXkKI34Ea8WzLr4FEyzkwohAC2WCQAU/file# [following]


--2024-08-07 18:21:12--  https://ucca241228aca55dbf9fcd60ae81.dl.dropboxusercontent.com/cd/0/inline/CYOq1NGkhLkELMmygLIg_gyLPXsOO7xOLjc3jW-mb09kevMykGPogSQx_icUTBEfHshxiSainXTynZYnh5O6uZ4ITeGiMkpvjl1QqXkKI34Ea8WzLr4FEyzkwohAC2WCQAU/file


Resolving ucca241228aca55dbf9fcd60ae81.dl.dropboxusercontent.com (ucca241228aca55dbf9fcd60ae81.dl.dropboxusercontent.com)... 162.125.1.15, 2620:100:6016:15::a27d:10f


Connecting to ucca241228aca55dbf9fcd60ae81.dl.dropboxusercontent.com (ucca241228aca55dbf9fcd60ae81.dl.dropboxusercontent.com)|162.125.1.15|:443... connected.


HTTP request sent, awaiting response... 302 Found


Location: /cd/0/inline2/CYMeJ4nM2JL44i1kCE4kttRGFOk-_34sr37ALElZu9szHfn-VhihA7l4cjIIFKHNN1ajRfeYYspGW3zPK1BZShxO3O7SEaXnHpUwUaziUcoz6b5IkdtXww3M6tRf8K2MZB4pHMSwxiuKe_vw9jitwHNeHn-jVzVRMw9feenAHN21LDudw5PxmsvqXSLeHMAGgs_tjeo1o92vltmhL6FpHs2czHsQFlYuaFMzwecv2xAMzHUGCGOhfNkmg2af16lP2QKLKgWAPK4ttCePTv-Ivy2KQ_GYVKKXRFlYHkIwhCQ_JFOyrtl_n14xls76NyPZRSZWmygSHJ-HH6Hntqvi86XpgCF-N_dZJh_HhSxuAaZd2g/file [following]


--2024-08-07 18:21:13--  https://ucca241228aca55dbf9fcd60ae81.dl.dropboxusercontent.com/cd/0/inline2/CYMeJ4nM2JL44i1kCE4kttRGFOk-_34sr37ALElZu9szHfn-VhihA7l4cjIIFKHNN1ajRfeYYspGW3zPK1BZShxO3O7SEaXnHpUwUaziUcoz6b5IkdtXww3M6tRf8K2MZB4pHMSwxiuKe_vw9jitwHNeHn-jVzVRMw9feenAHN21LDudw5PxmsvqXSLeHMAGgs_tjeo1o92vltmhL6FpHs2czHsQFlYuaFMzwecv2xAMzHUGCGOhfNkmg2af16lP2QKLKgWAPK4ttCePTv-Ivy2KQ_GYVKKXRFlYHkIwhCQ_JFOyrtl_n14xls76NyPZRSZWmygSHJ-HH6Hntqvi86XpgCF-N_dZJh_HhSxuAaZd2g/file


Reusing existing connection to ucca241228aca55dbf9fcd60ae81.dl.dropboxusercontent.com:443.


HTTP request sent, awaiting response... 200 OK


Length: 29467998 (28M) [application/pdf]


Saving to: ‘./data/sf_budgets/2016 - CSF_Budget_Book_2016_FINAL_WEB_with-cover-page.pdf’



./data/sf_budgets/2 100%[===================>]  28.10M   173MB/s    in 0.2s



2024-08-07 18:21:14 (173 MB/s) - ‘./data/sf_budgets/2016 - CSF_Budget_Book_2016_FINAL_WEB_with-cover-page.pdf’ saved [29467998/29467998]



--2024-08-07 18:21:14--  https://www.dropbox.com/scl/fi/jvw59g5nscu1m7f96tjre/2017-Proposed-Budget-FY2017-18-FY2018-19_1.pdf?rlkey=v988oigs2whtcy87ti9wti6od&dl=0


Resolving www.dropbox.com (www.dropbox.com)... 162.125.1.18, 2620:100:6057:18::a27d:d12


Connecting to www.dropbox.com (www.dropbox.com)|162.125.1.18|:443... connected.


HTTP request sent, awaiting response... 302 Found


Location: https://uca6ee7d218771b609b8ecdf23d7.dl.dropboxusercontent.com/cd/0/inline/CYNMSJ2zt2I5765XfzleiddbUXb-TkZP91r9LuVw_6wBH0USNyLT6lclDE7x6I0-_WEaGM7zqqCipxx7Uyp5owmnwMx8JyfbHG3fZ4LSDYM6QzubFok7NSc0R2KRd3DX0qg/file# [following]


--2024-08-07 18:21:15--  https://uca6ee7d218771b609b8ecdf23d7.dl.dropboxusercontent.com/cd/0/inline/CYNMSJ2zt2I5765XfzleiddbUXb-TkZP91r9LuVw_6wBH0USNyLT6lclDE7x6I0-_WEaGM7zqqCipxx7Uyp5owmnwMx8JyfbHG3fZ4LSDYM6QzubFok7NSc0R2KRd3DX0qg/file


Resolving uca6ee7d218771b609b8ecdf23d7.dl.dropboxusercontent.com (uca6ee7d218771b609b8ecdf23d7.dl.dropboxusercontent.com)... 162.125.1.15, 2620:100:6016:15::a27d:10f


Connecting to uca6ee7d218771b609b8ecdf23d7.dl.dropboxusercontent.com (uca6ee7d218771b609b8ecdf23d7.dl.dropboxusercontent.com)|162.125.1.15|:443... connected.


HTTP request sent, awaiting response... 302 Found


Location: /cd/0/inline2/CYNJm2hH6OlYZdhW6cv8AuAYvgEiuyOY1KUwzlH1Nq4RrvmmOHg2ipVgEq88bfVDEC_xV0SegX6DL-4CUB_6_2AjHC7iS5VnZVxsjkbpQHTqEKr7OK6mAlsGNPQi--ocxwOsUbQNpLVNSjEc2zA98VZLpntTl3AoJEvl4wmpvBhNCs_ChiY2TDNcQGFDPH5AjvEEHImiNQqCzrOzoSpFh9Ut9NQty6vjADUHg1yXFcPa5R-ODch6hb4FgTCQZv7WYQJ7H_MRHVJyLoIyCX8bqwZAblnXC9SbUuIxdgmkiAB_wwjJKuFLV7YNNjJX5kg9spGoYnRv7gNDqUhjvXBwKW_IQxsYc1HjsaabrrRFjXntAw/file [following]


--2024-08-07 18:21:16--  https://uca6ee7d218771b609b8ecdf23d7.dl.dropboxusercontent.com/cd/0/inline2/CYNJm2hH6OlYZdhW6cv8AuAYvgEiuyOY1KUwzlH1Nq4RrvmmOHg2ipVgEq88bfVDEC_xV0SegX6DL-4CUB_6_2AjHC7iS5VnZVxsjkbpQHTqEKr7OK6mAlsGNPQi--ocxwOsUbQNpLVNSjEc2zA98VZLpntTl3AoJEvl4wmpvBhNCs_ChiY2TDNcQGFDPH5AjvEEHImiNQqCzrOzoSpFh9Ut9NQty6vjADUHg1yXFcPa5R-ODch6hb4FgTCQZv7WYQJ7H_MRHVJyLoIyCX8bqwZAblnXC9SbUuIxdgmkiAB_wwjJKuFLV7YNNjJX5kg9spGoYnRv7gNDqUhjvXBwKW_IQxsYc1HjsaabrrRFjXntAw/file


Reusing existing connection to uca6ee7d218771b609b8ecdf23d7.dl.dropboxusercontent.com:443.


HTTP request sent, awaiting response... 200 OK


Length: 13463517 (13M) [application/pdf]


Saving to: ‘./data/sf_budgets/2017 - 2017-Proposed-Budget-FY2017-18-FY2018-19_1.pdf’



./data/sf_budgets/2 100%[===================>]  12.84M  --.-KB/s    in 0.09s



2024-08-07 18:21:17 (136 MB/s) - ‘./data/sf_budgets/2017 - 2017-Proposed-Budget-FY2017-18-FY2018-19_1.pdf’ saved [13463517/13463517]



--2024-08-07 18:21:17--  https://www.dropbox.com/scl/fi/izknlwmbs7ia0lbn7zzyx/2018-o0181-18.pdf?rlkey=p5nv2ehtp7272ege3m9diqhei&dl=0


Resolving www.dropbox.com (www.dropbox.com)... 162.125.1.18, 2620:100:6057:18::a27d:d12


Connecting to www.dropbox.com (www.dropbox.com)|162.125.1.18|:443... connected.


HTTP request sent, awaiting response... 302 Found


Location: https://uc922ffad4a58390c4df80dcafbf.dl.dropboxusercontent.com/cd/0/inline/CYOEOqz8prU7eZPDzgM8fwVVcHoP1lWOLF--9VoNPtzVDSvDCXUDxR1CeN_VMzOp4JGTG6V-CeYm7oLwrrEIjuWThf5rHt8eLh52TF1nJ4-jVPrn7nAjFrealf436uezAs0/file# [following]


--2024-08-07 18:21:17--  https://uc922ffad4a58390c4df80dcafbf.dl.dropboxusercontent.com/cd/0/inline/CYOEOqz8prU7eZPDzgM8fwVVcHoP1lWOLF--9VoNPtzVDSvDCXUDxR1CeN_VMzOp4JGTG6V-CeYm7oLwrrEIjuWThf5rHt8eLh52TF1nJ4-jVPrn7nAjFrealf436uezAs0/file


Resolving uc922ffad4a58390c4df80dcafbf.dl.dropboxusercontent.com (uc922ffad4a58390c4df80dcafbf.dl.dropboxusercontent.com)... 162.125.1.15, 2620:100:6016:15::a27d:10f


Connecting to uc922ffad4a58390c4df80dcafbf.dl.dropboxusercontent.com (uc922ffad4a58390c4df80dcafbf.dl.dropboxusercontent.com)|162.125.1.15|:443... connected.


HTTP request sent, awaiting response... 302 Found


Location: /cd/0/inline2/CYNZxULkXqH5RXSO_Tu0-X2BLjKqLUg3ZAH3vZeEHw-ic156C2iVH3wjJtcm6mkh-RpMfru6d3ZBBNTpf_EWLTWBywklJbD4ZhRInyrnF6s5oK4NWS6UQ_7GBHy11itN5OKGF9U0090wCFaQeaPwFyLxwIjhg_gZdTc8smr1YFyESsFTIJTLPq8QjI5uPvYyug6Oidh8RxOP2N2f2mBKDRS2R8cazDZRDrAxhVeAuSXPGpYzQc0lBcsTJQ8ZAXuYKww0e_qlpyHmDv6tRVHpdFNh1dyKyikOHqtGd4p3pYjBr2Kwn-jzJ1zkZf_Fpc_H9vX0Xkk6P9U25oOGvSnmIUC3LFkfHB_CJTGNSZUh36w5cA/file [following]


--2024-08-07 18:21:18--  https://uc922ffad4a58390c4df80dcafbf.dl.dropboxusercontent.com/cd/0/inline2/CYNZxULkXqH5RXSO_Tu0-X2BLjKqLUg3ZAH3vZeEHw-ic156C2iVH3wjJtcm6mkh-RpMfru6d3ZBBNTpf_EWLTWBywklJbD4ZhRInyrnF6s5oK4NWS6UQ_7GBHy11itN5OKGF9U0090wCFaQeaPwFyLxwIjhg_gZdTc8smr1YFyESsFTIJTLPq8QjI5uPvYyug6Oidh8RxOP2N2f2mBKDRS2R8cazDZRDrAxhVeAuSXPGpYzQc0lBcsTJQ8ZAXuYKww0e_qlpyHmDv6tRVHpdFNh1dyKyikOHqtGd4p3pYjBr2Kwn-jzJ1zkZf_Fpc_H9vX0Xkk6P9U25oOGvSnmIUC3LFkfHB_CJTGNSZUh36w5cA/file


Reusing existing connection to uc922ffad4a58390c4df80dcafbf.dl.dropboxusercontent.com:443.


HTTP request sent, awaiting response... 200 OK


Length: 18487865 (18M) [application/pdf]


Saving to: ‘./data/sf_budgets/2018 - 2018-o0181-18.pdf’



./data/sf_budgets/2 100%[===================>]  17.63M  --.-KB/s    in 0.1s



2024-08-07 18:21:19 (149 MB/s) - ‘./data/sf_budgets/2018 - 2018-o0181-18.pdf’ saved [18487865/18487865]



--2024-08-07 18:21:19--  https://www.dropbox.com/scl/fi/1rstqm9rh5u5fr0tcjnxj/2019-Proposed-Budget-FY2019-20-FY2020-21.pdf?rlkey=3s2ivfx7z9bev1r840dlpbcgg&dl=0


Resolving www.dropbox.com (www.dropbox.com)... 162.125.1.18, 2620:100:6057:18::a27d:d12


Connecting to www.dropbox.com (www.dropbox.com)|162.125.1.18|:443... connected.


HTTP request sent, awaiting response... 302 Found


Location: https://uce28a421063a08c4ce431616623.dl.dropboxusercontent.com/cd/0/inline/CYNSfAOo0ymwbrL62gVbRB_NTvZpU2t5SZqnLuZDW-OaDOssaoY8SkQxPM9csoAq0-Y3Y8rYA1E6cDD44K1pSJcsuRSyoRRVLHRmXvWdayHKMK_PWAo08V3murDu9ZZAu4s/file# [following]


--2024-08-07 18:21:20--  https://uce28a421063a08c4ce431616623.dl.dropboxusercontent.com/cd/0/inline/CYNSfAOo0ymwbrL62gVbRB_NTvZpU2t5SZqnLuZDW-OaDOssaoY8SkQxPM9csoAq0-Y3Y8rYA1E6cDD44K1pSJcsuRSyoRRVLHRmXvWdayHKMK_PWAo08V3murDu9ZZAu4s/file


Resolving uce28a421063a08c4ce431616623.dl.dropboxusercontent.com (uce28a421063a08c4ce431616623.dl.dropboxusercontent.com)... 162.125.1.15, 2620:100:6016:15::a27d:10f


Connecting to uce28a421063a08c4ce431616623.dl.dropboxusercontent.com (uce28a421063a08c4ce431616623.dl.dropboxusercontent.com)|162.125.1.15|:443... connected.


HTTP request sent, awaiting response... 302 Found


Location: /cd/0/inline2/CYOFZQRiPKCvnUe8S4h3AQ8gmhPC0MW_0vNg2GTCzxiUPSVRSgUXDsH8XYOgKuU905goGB1ZmWgs00sNArASToS2iE6pJgGfqsk3DYELK3xYZJOwJ_AscWEAjoISiZQEPhi9-QyQpyeXAr5gxavu9eMq3XFNzo9SCUA-SWFIuSCU5Tf5_ZfW_uAU41NZE4dDVsdvaD7rG4Ouci6dp6c902A2dHsNs0O-wRZEEKKFZs5KeHNLvZkdTaUGxYcgQn8vwWgTbuvAz36XycX6Sdhdp32mFF73U30G5ZTUmqAvgYDMlUilhdcJLPhhbrUyhFUWcXrfluUHkK8LkjKCPl4ywKmr8oJGji5ZOwehdXWgrL7ALg/file [following]


--2024-08-07 18:21:20--  https://uce28a421063a08c4ce431616623.dl.dropboxusercontent.com/cd/0/inline2/CYOFZQRiPKCvnUe8S4h3AQ8gmhPC0MW_0vNg2GTCzxiUPSVRSgUXDsH8XYOgKuU905goGB1ZmWgs00sNArASToS2iE6pJgGfqsk3DYELK3xYZJOwJ_AscWEAjoISiZQEPhi9-QyQpyeXAr5gxavu9eMq3XFNzo9SCUA-SWFIuSCU5Tf5_ZfW_uAU41NZE4dDVsdvaD7rG4Ouci6dp6c902A2dHsNs0O-wRZEEKKFZs5KeHNLvZkdTaUGxYcgQn8vwWgTbuvAz36XycX6Sdhdp32mFF73U30G5ZTUmqAvgYDMlUilhdcJLPhhbrUyhFUWcXrfluUHkK8LkjKCPl4ywKmr8oJGji5ZOwehdXWgrL7ALg/file


Reusing existing connection to uce28a421063a08c4ce431616623.dl.dropboxusercontent.com:443.


HTTP request sent, awaiting response... 200 OK


Length: 13123938 (13M) [application/pdf]


Saving to: ‘./data/sf_budgets/2019 - 2019-Proposed-Budget-FY2019-20-FY2020-21.pdf’



./data/sf_budgets/2 100%[===================>]  12.52M  --.-KB/s    in 0.08s



2024-08-07 18:21:22 (161 MB/s) - ‘./data/sf_budgets/2019 - 2019-Proposed-Budget-FY2019-20-FY2020-21.pdf’ saved [13123938/13123938]



--2024-08-07 18:21:22--  https://www.dropbox.com/scl/fi/7teuwxrjdyvgw0n8jjvk0/2021-AAO-FY20-21-FY21-22-09-11-2020-FINAL.pdf?rlkey=6br3wzxwj5fv1f1l8e69nbmhk&dl=0


Resolving www.dropbox.com (www.dropbox.com)... 162.125.1.18, 2620:100:6057:18::a27d:d12


Connecting to www.dropbox.com (www.dropbox.com)|162.125.1.18|:443... connected.


HTTP request sent, awaiting response... 302 Found


Location: https://uc8421b1eeadb07bda3c7e093660.dl.dropboxusercontent.com/cd/0/inline/CYMRjMFyYInwu1LATw9fLxGctgY-zI7_0nI1zgKVeJJf55J9CxQivdYpDYLjkYlXCKv2t6rQ9NCns9A5jDEU3xiQ0Ycrd6VrPv7tiYSYvNY7pXMBiV2LvXu7ZDtQgBH1334/file# [following]


--2024-08-07 18:21:22--  https://uc8421b1eeadb07bda3c7e093660.dl.dropboxusercontent.com/cd/0/inline/CYMRjMFyYInwu1LATw9fLxGctgY-zI7_0nI1zgKVeJJf55J9CxQivdYpDYLjkYlXCKv2t6rQ9NCns9A5jDEU3xiQ0Ycrd6VrPv7tiYSYvNY7pXMBiV2LvXu7ZDtQgBH1334/file


Resolving uc8421b1eeadb07bda3c7e093660.dl.dropboxusercontent.com (uc8421b1eeadb07bda3c7e093660.dl.dropboxusercontent.com)... 162.125.1.15, 2620:100:6016:15::a27d:10f


Connecting to uc8421b1eeadb07bda3c7e093660.dl.dropboxusercontent.com (uc8421b1eeadb07bda3c7e093660.dl.dropboxusercontent.com)|162.125.1.15|:443... connected.


HTTP request sent, awaiting response... 302 Found


Location: /cd/0/inline2/CYOOkJRGOrBeY0GY5xS_84ayGgfFapr4kvbiFcnAUkvwENgCw8Z3qTT_G2oQpBq6h-RVzjOh4SPrgusfRfbEWg9ZxXwxyWPo5I4yJ7eVhhqTi2jZN42r_k1FWF4IjxgRhMA237BSrCcKkweLmMNm3oN4cFap5dw2fyesDaZg0xa-fRAEjF5MubgvXVAwNVmEvrL8M7Sm4s4VsguOPsytt9GqfPkuARDvYXGLfvZeCx4hRfqOaNXdeGyBSy3GUBKyf8bH3YTHw6wEBk8Yp2dG64Q8FJyUgAXkpn1wZpBQe0dnk5WdoWrKrtkL4RDbBPo1k0fDfKeuajw_h5BhtEAl5XVE-11C0IEzcse1D-19TNlSuQ/file [following]


--2024-08-07 18:21:24--  https://uc8421b1eeadb07bda3c7e093660.dl.dropboxusercontent.com/cd/0/inline2/CYOOkJRGOrBeY0GY5xS_84ayGgfFapr4kvbiFcnAUkvwENgCw8Z3qTT_G2oQpBq6h-RVzjOh4SPrgusfRfbEWg9ZxXwxyWPo5I4yJ7eVhhqTi2jZN42r_k1FWF4IjxgRhMA237BSrCcKkweLmMNm3oN4cFap5dw2fyesDaZg0xa-fRAEjF5MubgvXVAwNVmEvrL8M7Sm4s4VsguOPsytt9GqfPkuARDvYXGLfvZeCx4hRfqOaNXdeGyBSy3GUBKyf8bH3YTHw6wEBk8Yp2dG64Q8FJyUgAXkpn1wZpBQe0dnk5WdoWrKrtkL4RDbBPo1k0fDfKeuajw_h5BhtEAl5XVE-11C0IEzcse1D-19TNlSuQ/file


Reusing existing connection to uc8421b1eeadb07bda3c7e093660.dl.dropboxusercontent.com:443.


HTTP request sent, awaiting response... 200 OK


Length: 3129122 (3.0M) [application/pdf]


Saving to: ‘./data/sf_budgets/2021 - 2021-AAO-FY20-21-FY21-22-09-11-2020-FINAL.pdf’



./data/sf_budgets/2 100%[===================>]   2.98M  --.-KB/s    in 0.05s



2024-08-07 18:21:24 (66.3 MB/s) - ‘./data/sf_budgets/2021 - 2021-AAO-FY20-21-FY21-22-09-11-2020-FINAL.pdf’ saved [3129122/3129122]



--2024-08-07 18:21:24--  https://www.dropbox.com/scl/fi/zhgqch4n6xbv9skgcknij/2022-AAO-FY2021-22-FY2022-23-FINAL-20210730.pdf?rlkey=h78t65dfaz3mqbpbhl1u9e309&dl=0


Resolving www.dropbox.com (www.dropbox.com)... 162.125.1.18, 2620:100:6057:18::a27d:d12


Connecting to www.dropbox.com (www.dropbox.com)|162.125.1.18|:443... connected.


HTTP request sent, awaiting response... 302 Found


Location: https://uc769a7232da4f728018e664ed74.dl.dropboxusercontent.com/cd/0/inline/CYPqlj1-wREOG6CVYV9KgsQ4Pyu3rqHgdY_UD2MqZIAndb3fAaRZeCB8kTXrOnILu6iGZZcjERz2tqT2mMiIcM86nxXDH6_J7tva-D9ZOwLROXr64weKF_NFuWTHcenrINM/file# [following]


--2024-08-07 18:21:26--  https://uc769a7232da4f728018e664ed74.dl.dropboxusercontent.com/cd/0/inline/CYPqlj1-wREOG6CVYV9KgsQ4Pyu3rqHgdY_UD2MqZIAndb3fAaRZeCB8kTXrOnILu6iGZZcjERz2tqT2mMiIcM86nxXDH6_J7tva-D9ZOwLROXr64weKF_NFuWTHcenrINM/file


Resolving uc769a7232da4f728018e664ed74.dl.dropboxusercontent.com (uc769a7232da4f728018e664ed74.dl.dropboxusercontent.com)... 162.125.1.15, 2620:100:6016:15::a27d:10f


Connecting to uc769a7232da4f728018e664ed74.dl.dropboxusercontent.com (uc769a7232da4f728018e664ed74.dl.dropboxusercontent.com)|162.125.1.15|:443... connected.


HTTP request sent, awaiting response... 302 Found


Location: /cd/0/inline2/CYNbMKpeTmC_in9_57ZDTlkiMBzRJiPbEXNEcIxLjRQJHTQEYhPcMmdqHcWdoP9Fxi1LYMKQDt1DUW1ZJYX1TxpLjIDxFyezLCprT2JfhkCROToyraIBrDpXPFgMEbBxNJIsBT1x70oL7BXSbW-pKomX6OKsy_nAP1B5jDVxhXOZtJwW8xFJwkvhNo71Aam2bT1wENAWKLdZOcVz4WRIdDI7e4Ri5FZ27Sjy2RCojgcFYusbpMWZFrxui-ssQzHsXvD1ZrZpKjyUXMIq_pdkbonY0V-8Iuq7PudclrjCIsDU2fD0bqo2MLdXw69PDLy2m5uVohTgcM0qCykha7dfGiP3BWfBpEM0PbmcfHx_IDqWDw/file [following]


--2024-08-07 18:21:27--  https://uc769a7232da4f728018e664ed74.dl.dropboxusercontent.com/cd/0/inline2/CYNbMKpeTmC_in9_57ZDTlkiMBzRJiPbEXNEcIxLjRQJHTQEYhPcMmdqHcWdoP9Fxi1LYMKQDt1DUW1ZJYX1TxpLjIDxFyezLCprT2JfhkCROToyraIBrDpXPFgMEbBxNJIsBT1x70oL7BXSbW-pKomX6OKsy_nAP1B5jDVxhXOZtJwW8xFJwkvhNo71Aam2bT1wENAWKLdZOcVz4WRIdDI7e4Ri5FZ27Sjy2RCojgcFYusbpMWZFrxui-ssQzHsXvD1ZrZpKjyUXMIq_pdkbonY0V-8Iuq7PudclrjCIsDU2fD0bqo2MLdXw69PDLy2m5uVohTgcM0qCykha7dfGiP3BWfBpEM0PbmcfHx_IDqWDw/file


Reusing existing connection to uc769a7232da4f728018e664ed74.dl.dropboxusercontent.com:443.


HTTP request sent, awaiting response... 200 OK


Length: 3233272 (3.1M) [application/pdf]


Saving to: ‘./data/sf_budgets/2022 - 2022-AAO-FY2021-22-FY2022-23-FINAL-20210730.pdf’



./data/sf_budgets/2 100%[===================>]   3.08M  --.-KB/s    in 0.05s



2024-08-07 18:21:28 (61.4 MB/s) - ‘./data/sf_budgets/2022 - 2022-AAO-FY2021-22-FY2022-23-FINAL-20210730.pdf’ saved [3233272/3233272]



--2024-08-07 18:21:28--  https://www.dropbox.com/scl/fi/vip161t63s56vd94neqlt/2023-CSF_Proposed_Budget_Book_June_2023_Master_Web.pdf?rlkey=hemoce3w1jsuf6s2bz87g549i&dl=0


Resolving www.dropbox.com (www.dropbox.com)... 162.125.1.18, 2620:100:6057:18::a27d:d12


Connecting to www.dropbox.com (www.dropbox.com)|162.125.1.18|:443... connected.


HTTP request sent, awaiting response... 302 Found


Location: https://uc3fa3b8bc2f92ed126eb3788d35.dl.dropboxusercontent.com/cd/0/inline/CYOKIz5n4gWk1Ywf1Ovmc-Dua40rRvPhK4YtffCdTlHM3tOiFbzgN6pyDNBx0vNo5fnHFEr5ilQwYHekMrlKykqII8thu9wiDbfAifKojwVXbgxJ1-Bqz6GXkPlLPp4rXkw/file# [following]


--2024-08-07 18:21:29--  https://uc3fa3b8bc2f92ed126eb3788d35.dl.dropboxusercontent.com/cd/0/inline/CYOKIz5n4gWk1Ywf1Ovmc-Dua40rRvPhK4YtffCdTlHM3tOiFbzgN6pyDNBx0vNo5fnHFEr5ilQwYHekMrlKykqII8thu9wiDbfAifKojwVXbgxJ1-Bqz6GXkPlLPp4rXkw/file


Resolving uc3fa3b8bc2f92ed126eb3788d35.dl.dropboxusercontent.com (uc3fa3b8bc2f92ed126eb3788d35.dl.dropboxusercontent.com)... 162.125.1.15, 2620:100:6016:15::a27d:10f


Connecting to uc3fa3b8bc2f92ed126eb3788d35.dl.dropboxusercontent.com (uc3fa3b8bc2f92ed126eb3788d35.dl.dropboxusercontent.com)|162.125.1.15|:443... connected.


HTTP request sent, awaiting response... 302 Found


Location: /cd/0/inline2/CYOKgVW-_SqOvVicBez1JsKaYs81mU1xzB4gynkTKGfcI9xEPnjv2pLp8NTtEuaREbjOoLQBNeBO9bLhjMMPubNVHYnWl8KSMk_nJ4WNWlIlK0UjNllsYqOzvtAD6gSDFlYt21i_WaYBOFR6wjOI4ZM69i6uREONYUBODDZ_tfdcbv5rfX87wGP8eZ47KeO9nBUwvpMNhj9Tby7bBuI0qVaIrjREqzYMap1VNN68SXOoDJbF2bdCS6O55U2vL9CvSXjuehi-fWcaEKisFhQCIGT-PyzNY1F2Vd3zl5DH-aqeEInObuL26LGOgAIEbU6c0PHHq10-GKWo40fv2ECnrTxXLD89T5dhJQJ9mCamCA_COg/file [following]


--2024-08-07 18:21:30--  https://uc3fa3b8bc2f92ed126eb3788d35.dl.dropboxusercontent.com/cd/0/inline2/CYOKgVW-_SqOvVicBez1JsKaYs81mU1xzB4gynkTKGfcI9xEPnjv2pLp8NTtEuaREbjOoLQBNeBO9bLhjMMPubNVHYnWl8KSMk_nJ4WNWlIlK0UjNllsYqOzvtAD6gSDFlYt21i_WaYBOFR6wjOI4ZM69i6uREONYUBODDZ_tfdcbv5rfX87wGP8eZ47KeO9nBUwvpMNhj9Tby7bBuI0qVaIrjREqzYMap1VNN68SXOoDJbF2bdCS6O55U2vL9CvSXjuehi-fWcaEKisFhQCIGT-PyzNY1F2Vd3zl5DH-aqeEInObuL26LGOgAIEbU6c0PHHq10-GKWo40fv2ECnrTxXLD89T5dhJQJ9mCamCA_COg/file


Reusing existing connection to uc3fa3b8bc2f92ed126eb3788d35.dl.dropboxusercontent.com:443.


HTTP request sent, awaiting response... 200 OK


Length: 10550407 (10M) [application/pdf]


Saving to: ‘./data/sf_budgets/2023 - 2023-CSF_Proposed_Budget_Book_June_2023_Master_Web.pdf’



./data/sf_budgets/2 100%[===================>]  10.06M  --.-KB/s    in 0.09s



2024-08-07 18:21:31 (110 MB/s) - ‘./data/sf_budgets/2023 - 2023-CSF_Proposed_Budget_Book_June_2023_Master_Web.pdf’ saved [10550407/10550407]

```

# Load data and run the workflow
[Section titled “Load data and run the workflow”](https://developers.llamaindex.ai/python/examples/workflow/sub_question_query_engine/#load-data-and-run-the-workflow)
Just like using the built-in Sub-Question Query Engine, we create our query tools and instantiate an LLM and pass them in.
Each tool is its own query engine based on a single (very lengthy) San Francisco budget document, each of which is 300+ pages. To save time on repeated runs, we persist our generated indexes to disk.

```


from google.colab import userdata





os.environ["OPENAI_API_KEY"] = userdata.get("openai-key")





folder ="./data/sf_budgets/"




files = os.listdir(folder)





query_engine_tools = []




forfilein files:




year =file.split(" - ")[0]




index_persist_path =f"./storage/budget-{year}/"





if os.path.exists(index_persist_path):




storage_context = StorageContext.from_defaults(




persist_dir=index_persist_path





index = load_index_from_storage(storage_context)




else:




documents = SimpleDirectoryReader(




input_files=[folder +file]




).load_data()




index = VectorStoreIndex.from_documents(documents)




index.storage_context.persist(index_persist_path)





engine = index.as_query_engine()




query_engine_tools.append(




QueryEngineTool(




query_engine=engine,




metadata=ToolMetadata(




name=f"budget_{year}",




description=f"Information about San Francisco's budget in {year}",








engine = SubQuestionQueryEngine(timeout=120, verbose=True)




llm = OpenAI(model="gpt-4o")




result =await engine.run(




llm=llm,




tools=query_engine_tools,




query="How has the total amount of San Francisco's budget changed from 2016 to 2023?",






print(result)


```


```

Running step query


Query is How has the total amount of San Francisco's budget changed from 2016 to 2023?


Sub-questions are {



"sub_questions": [




"What was the total amount of San Francisco's budget in 2016?",




"What was the total amount of San Francisco's budget in 2017?",




"What was the total amount of San Francisco's budget in 2018?",




"What was the total amount of San Francisco's budget in 2019?",




"What was the total amount of San Francisco's budget in 2020?",




"What was the total amount of San Francisco's budget in 2021?",




"What was the total amount of San Francisco's budget in 2022?",




"What was the total amount of San Francisco's budget in 2023?"





Step query produced no event


Running step sub_question


Sub-question is What was the total amount of San Francisco's budget in 2016?


> Running step 61365946-614c-4895-8fc3-0968f2d63387. Step input: What was the total amount of San Francisco's budget in 2016?


[1;3;38;5;200mThought: The current language of the user is English. I need to use a tool to help me answer the question.


Action: budget_2016


Action Input: {'input': "total amount of San Francisco's budget in 2016"}


[0m[1;3;34mObservation: The total amount of San Francisco's budget in 2016 was $9.6 billion.


[0m> Running step a85aa30e-a980-4897-a52e-e82b8fb25c72. Step input: None


[1;3;38;5;200mThought: I can answer without using any more tools. I'll use the user's language to answer.


Answer: The total amount of San Francisco's budget in 2016 was $9.6 billion.


[0mStep sub_question produced event AnswerEvent


Running step sub_question


Sub-question is What was the total amount of San Francisco's budget in 2017?


> Running step 5d14466c-1400-4a26-ac42-021e7143d3b1. Step input: What was the total amount of San Francisco's budget in 2017?


[1;3;38;5;200mThought: The current language of the user is English. I need to use a tool to help me answer the question.


Action: budget_2017


Action Input: {'input': "total amount of San Francisco's budget in 2017"}


[0m[1;3;34mObservation: $10,106.9 million


[0m> Running step 586a5fab-95ee-44e9-9a35-fcf19993b13e. Step input: None


[1;3;38;5;200mThought: I have the information needed to answer the question.


Answer: The total amount of San Francisco's budget in 2017 was $10,106.9 million.


[0mStep sub_question produced event AnswerEvent


Running step sub_question


Sub-question is What was the total amount of San Francisco's budget in 2018?


> Running step d39f64d0-65f6-4571-95ad-d28a16198ea5. Step input: What was the total amount of San Francisco's budget in 2018?


[1;3;38;5;200mThought: The current language of the user is English. I need to use a tool to help me answer the question.


Action: budget_2018


Action Input: {'input': "total amount of San Francisco's budget in 2018"}


[0m[1;3;34mObservation: The total amount of San Francisco's budget in 2018 was $12,659,306,000.


[0m> Running step 3f67feee-489c-4b9e-8f27-37f0d48e3b0d. Step input: None


[1;3;38;5;200mThought: I can answer without using any more tools. I'll use the user's language to answer.


Answer: The total amount of San Francisco's budget in 2018 was $12,659,306,000.


[0mStep sub_question produced event AnswerEvent


Running step sub_question


Sub-question is What was the total amount of San Francisco's budget in 2019?


> Running step d5ac0866-b02c-4c4c-94c6-f0e047ebb0fe. Step input: What was the total amount of San Francisco's budget in 2019?


[1;3;38;5;200mThought: The current language of the user is English. I need to use a tool to help me answer the question.


Action: budget_2019


Action Input: {'input': "total amount of San Francisco's budget in 2019"}


[0m[1;3;34mObservation: $12.3 billion


[0m> Running step 3b62859b-bbd3-4dce-b284-f9b398e370c2. Step input: None


[1;3;38;5;200mThought: I can answer without using any more tools. I'll use the user's language to answer.


Answer: The total amount of San Francisco's budget in 2019 was $12.3 billion.


[0mStep sub_question produced event AnswerEvent


Running step sub_question


Sub-question is What was the total amount of San Francisco's budget in 2020?


> Running step 41f6ed9f-d695-43df-8743-39dfcc3d919d. Step input: What was the total amount of San Francisco's budget in 2020?


[1;3;38;5;200mThought: The user is asking for the total amount of San Francisco's budget in 2020. I do not have a tool specifically for the 2020 budget. I will check the available tools to see if they provide any relevant information or if I can infer the 2020 budget from adjacent years.


Action: budget_2021


Action Input: {'input': "What was the total amount of San Francisco's budget in 2020?"}


[0m[1;3;34mObservation: The total amount of San Francisco's budget in 2020 was $15,373,192 (in thousands of dollars).


[0m> Running step ea39f7c6-e942-4a41-8963-f37d4a27d559. Step input: None


[1;3;38;5;200mThought: I now have the information needed to answer the user's question about the total amount of San Francisco's budget in 2020.


Answer: The total amount of San Francisco's budget in 2020 was $15,373,192 (in thousands of dollars).


[0mStep sub_question produced event AnswerEvent


Running step sub_question


Sub-question is What was the total amount of San Francisco's budget in 2021?


> Running step 6662fd06-e86a-407c-bb89-4828f63caa72. Step input: What was the total amount of San Francisco's budget in 2021?


[1;3;38;5;200mThought: The current language of the user is English. I need to use a tool to help me answer the question.


Action: budget_2021


Action Input: {'input': "total amount of San Francisco's budget in 2021"}


[0m[1;3;34mObservation: The total amount of San Francisco's budget in 2021 is $14,166,496,000.


[0m> Running step 5d0cf9da-2c14-407c-8ae5-5cd638c1fb5c. Step input: None


[1;3;38;5;200mThought: I can answer without using any more tools. I'll use the user's language to answer.


Answer: The total amount of San Francisco's budget in 2021 was $14,166,496,000.


[0mStep sub_question produced event AnswerEvent


Running step sub_question


Sub-question is What was the total amount of San Francisco's budget in 2022?


> Running step 62fa9a5f-f40b-489d-9773-5ee4e4eaba9e. Step input: What was the total amount of San Francisco's budget in 2022?


[1;3;38;5;200mThought: The current language of the user is English. I need to use a tool to help me answer the question.


Action: budget_2022


Action Input: {'input': "total amount of San Francisco's budget in 2022"}


[0m[1;3;34mObservation: $14,550,060


[0m> Running step 7a2d5623-cc75-4c9d-8c58-3dbc2faf163d. Step input: None


[1;3;38;5;200mThought: I can answer without using any more tools. I'll use the user's language to answer.


Answer: The total amount of San Francisco's budget in 2022 was $14,550,060.


[0mStep sub_question produced event AnswerEvent


Running step sub_question


Sub-question is What was the total amount of San Francisco's budget in 2023?


> Running step 839eb994-b4e2-4019-a170-9471c1e0d764. Step input: What was the total amount of San Francisco's budget in 2023?


[1;3;38;5;200mThought: The current language of the user is: English. I need to use a tool to help me answer the question.


Action: budget_2023


Action Input: {'input': "total amount of San Francisco's budget in 2023"}


[0m[1;3;34mObservation: $14.6 billion


[0m> Running step 38779f6c-d0c7-4c95-b5c4-0b170c5ed0d5. Step input: None


[1;3;38;5;200mThought: I can answer without using any more tools. I'll use the user's language to answer.


Answer: The total amount of San Francisco's budget in 2023 was $14.6 billion.


[0mStep sub_question produced event AnswerEvent


Running step combine_answers


Step combine_answers produced no event


Running step combine_answers


Step combine_answers produced no event


Running step combine_answers


Step combine_answers produced no event


Running step combine_answers


Step combine_answers produced no event


Running step combine_answers


Step combine_answers produced no event


Running step combine_answers


Step combine_answers produced no event


Running step combine_answers


Step combine_answers produced no event


Running step combine_answers


Final prompt is



You are given an overall question that has been split into sub-questions,




each of which has been answered. Combine the answers to all the sub-questions




into a single answer to the original question.





Original question: How has the total amount of San Francisco's budget changed from 2016 to 2023?





Sub-questions and answers:




Question: What was the total amount of San Francisco's budget in 2016?:




Answer: The total amount of San Francisco's budget in 2016 was $9.6 billion.




Question: What was the total amount of San Francisco's budget in 2017?:



Answer: The total amount of San Francisco's budget in 2017 was $10,106.9 million.




Question: What was the total amount of San Francisco's budget in 2018?:



Answer: The total amount of San Francisco's budget in 2018 was $12,659,306,000.




Question: What was the total amount of San Francisco's budget in 2019?:



Answer: The total amount of San Francisco's budget in 2019 was $12.3 billion.




Question: What was the total amount of San Francisco's budget in 2020?:



Answer: The total amount of San Francisco's budget in 2020 was $15,373,192 (in thousands of dollars).




Question: What was the total amount of San Francisco's budget in 2021?:



Answer: The total amount of San Francisco's budget in 2021 was $14,166,496,000.




Question: What was the total amount of San Francisco's budget in 2022?:



Answer: The total amount of San Francisco's budget in 2022 was $14,550,060.




Question: What was the total amount of San Francisco's budget in 2023?:



Answer: The total amount of San Francisco's budget in 2023 was $14.6 billion.




Final response is From 2016 to 2023, the total amount of San Francisco's budget has seen significant changes. In 2016, the budget was $9.6 billion. It increased to $10,106.9 million in 2017 and further to $12,659,306,000 in 2018. In 2019, the budget was $12.3 billion. The budget saw a substantial rise in 2020, reaching $15,373,192 (in thousands of dollars), which translates to approximately $15.4 billion. In 2021, the budget was $14,166,496,000, and in 2022, it was $14,550,060. By 2023, the budget had increased to $14.6 billion. Overall, from 2016 to 2023, San Francisco's budget grew from $9.6 billion to $14.6 billion.


Step combine_answers produced event StopEvent


From 2016 to 2023, the total amount of San Francisco's budget has seen significant changes. In 2016, the budget was $9.6 billion. It increased to $10,106.9 million in 2017 and further to $12,659,306,000 in 2018. In 2019, the budget was $12.3 billion. The budget saw a substantial rise in 2020, reaching $15,373,192 (in thousands of dollars), which translates to approximately $15.4 billion. In 2021, the budget was $14,166,496,000, and in 2022, it was $14,550,060. By 2023, the budget had increased to $14.6 billion. Overall, from 2016 to 2023, San Francisco's budget grew from $9.6 billion to $14.6 billion.

```

Our debug output is lengthy! You can see the sub-questions being generated and then `sub_question()` being repeatedly invoked, each time generating a brief log of ReAct agent thoughts and actions to answer each smaller question.
You can see `combine_answers` running multiple times; these were triggered by each `AnswerEvent` but before all 8 `AnswerEvents` were collected. On its final run it generates a full prompt, combines the answers and returns the result.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


