[Skip to content](https://developers.llamaindex.ai/python/examples/node_postprocessor/llmreranker-gatsby/#_top)
# LLM Reranker Demonstration (Great Gatsby) 
This tutorial showcases how to do a two-stage pass for retrieval. Use embedding-based retrieval with a high top-k value in order to maximize recall and get a large set of candidate items. Then, use LLM-based retrieval to dynamically select the nodes that are actually relevant to the query.

```


%pip install llama-index-llms-openai


```


```


import nest_asyncio




nest_asyncio.apply()

```


```


import logging




import sys





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))




from llama_index.core import VectorStoreIndex, SimpleDirectoryReader




from llama_index.core.postprocessor import LLMRerank




from llama_index.llms.openai import OpenAI




from IPython.display import Markdown, display


```

## Load Data, Build Index
[Section titled “Load Data, Build Index”](https://developers.llamaindex.ai/python/examples/node_postprocessor/llmreranker-gatsby/#load-data-build-index)

```


from llama_index.core import Settings




# LLM (gpt-3.5-turbo)



Settings.llm = OpenAI(temperature=0, model="gpt-3.5-turbo")




Settings.chunk_size =512


```


```

# load documents



documents = SimpleDirectoryReader("../../../examples/gatsby/data").load_data()


```


```

documents

```


```


index = VectorStoreIndex.from_documents(




documents,



```


```

INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total LLM token usage: 0 tokens


> [build_index_from_nodes] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total embedding token usage: 49266 tokens


> [build_index_from_nodes] Total embedding token usage: 49266 tokens

```

## Retrieval
[Section titled “Retrieval”](https://developers.llamaindex.ai/python/examples/node_postprocessor/llmreranker-gatsby/#retrieval)

```


from llama_index.core.retrievers import VectorIndexRetriever




from llama_index.core import QueryBundle




import pandas as pd




from IPython.display import display, HTML






pd.set_option("display.max_colwidth", -1)






defget_retrieved_nodes(




query_str, vector_top_k=10, reranker_top_n=3, with_reranker=False





query_bundle = QueryBundle(query_str)




# configure retriever




retriever = VectorIndexRetriever(




index=index,




similarity_top_k=vector_top_k,





retrieved_nodes = retriever.retrieve(query_bundle)





if with_reranker:




# configure reranker




reranker = LLMRerank(




choice_batch_size=5,




top_n=reranker_top_n,





retrieved_nodes = reranker.postprocess_nodes(




retrieved_nodes, query_bundle






return retrieved_nodes






defpretty_print(df):




return display(HTML(df.to_html().replace("\\n", "<br>")))






defvisualize_retrieved_nodes(nodes) -> None:




result_dicts = []




for node in nodes:




result_dict = {"Score": node.score, "Text": node.node.get_text()}




result_dicts.append(result_dict)





pretty_print(pd.DataFrame(result_dicts))


```


```

/var/folders/1r/c3h91d9s49xblwfvz79s78_c0000gn/T/ipykernel_44297/3519340226.py:7: FutureWarning: Passing a negative integer is deprecated in version 1.0 and will not be supported in future version. Instead, use None to not limit the column width.



pd.set_option('display.max_colwidth', -1)


```


```


new_nodes = get_retrieved_nodes(




"Who was driving the car that hit Myrtle?",




vector_top_k=3,




with_reranker=False,



```


```

INFO:llama_index.token_counter.token_counter:> [retrieve] Total LLM token usage: 0 tokens


> [retrieve] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [retrieve] Total embedding token usage: 10 tokens


> [retrieve] Total embedding token usage: 10 tokens

```


```

visualize_retrieved_nodes(new_nodes)

```
  
| Score  | Text  |  
| --- | --- |  
| 0  | 0.828844  | and some garrulous man telling over and over whathad happened, until it became less and less real even to him and hecould tell it no longer, and Myrtle Wilson’s tragic achievement wasforgotten. Now I want to go back a little and tell what happened atthe garage after we left there the night before.They had difficulty in locating the sister, Catherine. She must havebroken her rule against drinking that night, for when she arrived shewas stupid with liquor and unable to understand that the ambulance hadalready gone to Flushing. When they convinced her of this, sheimmediately fainted, as if that was the intolerable part of theaffair. Someone, kind or curious, took her in his car and drove her inthe wake of her sister’s body.Until long after midnight a changing crowd lapped up against the frontof the garage, while George Wilson rocked himself back and forth onthe couch inside. For a while the door of the office was open, andeveryone who came into the garage glanced irresistibly through it.Finally someone said it was a shame, and closed the door. Michaelisand several other men were with him; first, four or five men, latertwo or three men. Still later Michaelis had to ask the last strangerto wait there fifteen minutes longer, while he went back to his ownplace and made a pot of coffee. After that, he stayed there alone withWilson until dawn.About three o’clock the quality of Wilson’s incoherent mutteringchanged—he grew quieter and began to talk about the yellow car. Heannounced that he had a way of finding out whom the yellow carbelonged to, and then he blurted out that a couple of months ago hiswife had come from the city with her face bruised and her noseswollen.But when he heard himself say this, he flinched and began to cry “Oh,my God!” again in his groaning voice. Michaelis made a clumsy  |  
| 1  | 0.827754  | she rushed out into the dusk, waving her hands andshouting—before he could move from his door the business was over.The “death car” as the newspapers called it, didn’t stop; it came outof the gathering darkness, wavered tragically for a moment, and thendisappeared around the next bend. Mavro Michaelis wasn’t even sure ofits colour—he told the first policeman that it was light green. Theother car, the one going toward New York, came to rest a hundred yardsbeyond, and its driver hurried back to where Myrtle Wilson, her lifeviolently extinguished, knelt in the road and mingled her thick darkblood with the dust.Michaelis and this man reached her first, but when they had torn openher shirtwaist, still damp with perspiration, they saw that her leftbreast was swinging loose like a flap, and there was no need to listenfor the heart beneath. The mouth was wide open and ripped a little atthe corners, as though she had choked a little in giving up thetremendous vitality she had stored so long.------------------------------------------------------------------------We saw the three or four automobiles and the crowd when we were stillsome distance away.“Wreck!” said Tom. “That’s good. Wilson’ll have a little business atlast.”He slowed down, but still without any intention of stopping, until, aswe came nearer, the hushed, intent faces of the people at the garagedoor made him automatically put on the brakes.“We’ll take a look,” he said doubtfully, “just a look.”I became aware now of a hollow, wailing sound which issued incessantlyfrom the garage, a sound which as we got out of the coupé and walkedtoward the door resolved itself into the words “Oh, my God!” utteredover and over in a gasping  |  
| 2  | 0.826390  | went on, “and left the car inmy garage. I don’t think anybody saw us, but of course I can’t besure.”I disliked him so much by this time that I didn’t find it necessary totell him he was wrong.“Who was the woman?” he inquired.“Her name was Wilson. Her husband owns the garage. How the devil didit happen?”“Well, I tried to swing the wheel—” He broke off, and suddenly Iguessed at the truth.“Was Daisy driving?”“Yes,” he said after a moment, “but of course I’ll say I was. You see,when we left New York she was very nervous and she thought it wouldsteady her to drive—and this woman rushed out at us just as we werepassing a car coming the other way. It all happened in a minute, butit seemed to me that she wanted to speak to us, thought we weresomebody she knew. Well, first Daisy turned away from the woman towardthe other car, and then she lost her nerve and turned back. The secondmy hand reached the wheel I felt the shock—it must have killed herinstantly.”“It ripped her open—”“Don’t tell me, old sport.” He winced. “Anyhow—Daisy stepped on it. Itried to make her stop, but she couldn’t, so I pulled on the emergencybrake. Then she fell over into my lap and I drove on.“She’ll be all right tomorrow,” he said presently. “I’m just going towait here and see if he tries to bother her about that unpleasantnessthis afternoon. She’s locked herself into her room, and if he triesany brutality she’s going to turn the light out and on again.”“He won’t touch  |  

```


new_nodes = get_retrieved_nodes(




"Who was driving the car that hit Myrtle?",




vector_top_k=10,




reranker_top_n=3,




with_reranker=True,



```


```

visualize_retrieved_nodes(new_nodes)

```
  
| Score  | Text  |  
| --- | --- |  
| 0  | 10.0  | went on, “and left the car inmy garage. I don’t think anybody saw us, but of course I can’t besure.”I disliked him so much by this time that I didn’t find it necessary totell him he was wrong.“Who was the woman?” he inquired.“Her name was Wilson. Her husband owns the garage. How the devil didit happen?”“Well, I tried to swing the wheel—” He broke off, and suddenly Iguessed at the truth.“Was Daisy driving?”“Yes,” he said after a moment, “but of course I’ll say I was. You see,when we left New York she was very nervous and she thought it wouldsteady her to drive—and this woman rushed out at us just as we werepassing a car coming the other way. It all happened in a minute, butit seemed to me that she wanted to speak to us, thought we weresomebody she knew. Well, first Daisy turned away from the woman towardthe other car, and then she lost her nerve and turned back. The secondmy hand reached the wheel I felt the shock—it must have killed herinstantly.”“It ripped her open—”“Don’t tell me, old sport.” He winced. “Anyhow—Daisy stepped on it. Itried to make her stop, but she couldn’t, so I pulled on the emergencybrake. Then she fell over into my lap and I drove on.“She’ll be all right tomorrow,” he said presently. “I’m just going towait here and see if he tries to bother her about that unpleasantnessthis afternoon. She’s locked herself into her room, and if he triesany brutality she’s going to turn the light out and on again.”“He won’t touch  |  

```


new_nodes = get_retrieved_nodes(




"What did Gatsby want Daisy to do in front of Tom?",




vector_top_k=3,




with_reranker=False,



```


```

INFO:llama_index.token_counter.token_counter:> [retrieve] Total LLM token usage: 0 tokens


> [retrieve] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [retrieve] Total embedding token usage: 14 tokens


> [retrieve] Total embedding token usage: 14 tokens

```


```

visualize_retrieved_nodes(new_nodes)

```


```

****Score****: 0.8647796939111776


****Node text****


: got to make your house into a pigsty in order to have any


friends—in the modern world.”



Angry as I was, as we all were, I was tempted to laugh whenever he


opened his mouth. The transition from libertine to prig was so


complete.



“I’ve got something to tell you, old sport—” began Gatsby. But Daisy


guessed at his intention.



“Please don’t!” she interrupted helplessly. “Please let’s all go


home. Why don’t we all go home?”



“That’s a good idea,” I got up. “Come on, Tom. Nobody wants a drink.”



“I want to know what Mr. Gatsby has to tell me.”



“Your wife doesn’t love you,” said Gatsby. “She’s never loved you.


She loves me.”



“You must be crazy!” exclaimed Tom automatically.



Gatsby sprang to his feet, vivid with excitement.



“She never loved you, do you hear?” he cried. “She only married you


because I was poor and she was tired of waiting for me. It was a


terrible mistake, but in her heart she never loved anyone except me!”



At this point Jordan and I tried to go, but Tom and Gatsby insisted


with competitive firmness that we remain—as though neither of them had


anything to conceal and it would be a privilege to partake vicariously


of their emotions.



“Sit down, Daisy,” Tom’s voice groped unsuccessfully for the paternal


note. “What’s been going on? I want to hear all about it.”



“I told you what’s been going on,” said Gatsby. “Going on for five


years—and you didn’t know.”



Tom turned to Daisy




****Score****: 0.8609230717744326


****Node text****


: to keep your


shoes dry?” There was a husky tenderness in his tone … “Daisy?”



“Please don’t.” Her voice was cold, but the rancour was gone from it.


She looked at Gatsby. “There, Jay,” she said—but her hand as she tried


to light a cigarette was trembling. Suddenly she threw the cigarette


and the burning match on the carpet.



“Oh, you want too much!” she cried to Gatsby. “I love you now—isn’t


that enough? I can’t help what’s past.” She began to sob


helplessly. “I did love him once—but I loved you too.”



Gatsby’s eyes opened and closed.



“You loved me too?” he repeated.



“Even that’s a lie,” said Tom savagely. “She didn’t know you were


alive. Why—there’s things between Daisy and me that you’ll never know,


things that neither of us can ever forget.”



The words seemed to bite physically into Gatsby.



“I want to speak to Daisy alone,” he insisted. “She’s all excited


now—”



“Even alone I can’t say I never loved Tom,” she admitted in a pitiful


voice. “It wouldn’t be true.”



“Of course it wouldn’t,” agreed Tom.



She turned to her husband.



“As if it mattered to you,” she said.



“Of course it matters. I’m going to take better care of you from now


on.”



“You don’t understand,” said Gatsby, with a touch of panic. “You’re


not going to take care of her any more.”



“I’m not?” Tom opened his eyes wide and




****Score****: 0.8555028907426916


****Node text****


: shadowed well with awnings, was dark and cool. Daisy and


Jordan lay upon an enormous couch, like silver idols weighing down


their own white dresses against the singing breeze of the fans.



“We can’t move,” they said together.



Jordan’s fingers, powdered white over their tan, rested for a moment


in mine.



“And Mr. Thomas Buchanan, the athlete?” I inquired.



Simultaneously I heard his voice, gruff, muffled, husky, at the hall


telephone.



Gatsby stood in the centre of the crimson carpet and gazed around with


fascinated eyes. Daisy watched him and laughed, her sweet, exciting


laugh; a tiny gust of powder rose from her bosom into the air.



“The rumour is,” whispered Jordan, “that that’s Tom’s girl on the


telephone.”



We were silent. The voice in the hall rose high with annoyance: “Very


well, then, I won’t sell you the car at all … I’m under no obligations


to you at all … and as for your bothering me about it at lunch time, I


won’t stand that at all!”



“Holding down the receiver,” said Daisy cynically.



“No, he’s not,” I assured her. “It’s a bona-fide deal. I happen to


know about it.”



Tom flung open the door, blocked out its space for a moment with his


thick body, and hurried into the room.



“Mr. Gatsby!” He put out his broad, flat hand with well-concealed


dislike. “I’m glad to see you, sir … Nick …”



“Make us a cold drink,” cried Daisy.



As he left the room again she got up and went over to Gatsby and


pulled his face

```


```


new_nodes = get_retrieved_nodes(




"What did Gatsby want Daisy to do in front of Tom?",




vector_top_k=10,




reranker_top_n=3,




with_reranker=True,



```


```

INFO:llama_index.token_counter.token_counter:> [retrieve] Total LLM token usage: 0 tokens


> [retrieve] Total LLM token usage: 0 tokens


INFO:llama_index.token_counter.token_counter:> [retrieve] Total embedding token usage: 14 tokens


> [retrieve] Total embedding token usage: 14 tokens


Doc: 2, Relevance: 10


No relevant documents found. Please provide a different question.

```


```

visualize_retrieved_nodes(new_nodes)

```


```

****Score****: 10.0


****Node text****


: to keep your


shoes dry?” There was a husky tenderness in his tone … “Daisy?”



“Please don’t.” Her voice was cold, but the rancour was gone from it.


She looked at Gatsby. “There, Jay,” she said—but her hand as she tried


to light a cigarette was trembling. Suddenly she threw the cigarette


and the burning match on the carpet.



“Oh, you want too much!” she cried to Gatsby. “I love you now—isn’t


that enough? I can’t help what’s past.” She began to sob


helplessly. “I did love him once—but I loved you too.”



Gatsby’s eyes opened and closed.



“You loved me too?” he repeated.



“Even that’s a lie,” said Tom savagely. “She didn’t know you were


alive. Why—there’s things between Daisy and me that you’ll never know,


things that neither of us can ever forget.”



The words seemed to bite physically into Gatsby.



“I want to speak to Daisy alone,” he insisted. “She’s all excited


now—”



“Even alone I can’t say I never loved Tom,” she admitted in a pitiful


voice. “It wouldn’t be true.”



“Of course it wouldn’t,” agreed Tom.



She turned to her husband.



“As if it mattered to you,” she said.



“Of course it matters. I’m going to take better care of you from now


on.”



“You don’t understand,” said Gatsby, with a touch of panic. “You’re


not going to take care of her any more.”



“I’m not?” Tom opened his eyes wide and

```

## Query Engine
[Section titled “Query Engine”](https://developers.llamaindex.ai/python/examples/node_postprocessor/llmreranker-gatsby/#query-engine)

```


query_engine = index.as_query_engine(




similarity_top_k=10,




node_postprocessors=[




LLMRerank(




choice_batch_size=5,




top_n=2,






response_mode="tree_summarize",





response = query_engine.query(




"What did the author do during his time at Y Combinator?",



```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


