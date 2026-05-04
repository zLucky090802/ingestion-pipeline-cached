[Skip to content](https://developers.llamaindex.ai/python/examples/prompts/emotion_prompt/#_top)
# EmotionPrompt in RAG 
Inspired by the “[Large Language Models Understand and Can Be Enhanced by Emotional Stimuli](https://arxiv.org/pdf/2307.11760.pdf)” by Li et al., in this guide we show you how to evaluate the effects of emotional stimuli on your RAG pipeline:
  1. Setup the RAG pipeline with a basic vector index with the core QA template.
  2. Create some candidate stimuli (inspired by Fig. 2 of the paper)
  3. For each candidate stimulit, prepend to QA prompt and evaluate.



```


%pip install llama-index-llms-openai




%pip install llama-index-readers-file pymupdf


```

## Setup Data
[Section titled “Setup Data”](https://developers.llamaindex.ai/python/examples/prompts/emotion_prompt/#setup-data)
We use the Llama 2 paper as the input data source for our RAG pipeline.

```


!mkdir -p llama_2_data  wget --user-agent "Mozilla""https://arxiv.org/pdf/2307.09288.pdf"-O "llama_2_data/llama2.pdf"


```


```


from llama_index.readers.file import PyMuPDFReader




from llama_index.core import Document




from llama_index.core.node_parser import SentenceSplitter





docs0 = PyMuPDFReader().load_data("./llama_2_data/llama2.pdf")




# combine all documents into one



doc_text ="\n\n".join([d.get_content() forin docs0])




docs = [Document(text=doc_text)]




# split the document into chunks of 1024 tokens



node_parser = SentenceSplitter(chunk_size=1024)




base_nodes = node_parser.get_nodes_from_documents(docs)


```

## Setup Vector Index over this Data
[Section titled “Setup Vector Index over this Data”](https://developers.llamaindex.ai/python/examples/prompts/emotion_prompt/#setup-vector-index-over-this-data)
We load this data into an in-memory vector store (embedded with OpenAI embeddings).
We’ll be aggressively optimizing the QA prompt for this RAG pipeline.

```


import os





os.environ["OPENAI_API_KEY"] ="sk-..."


```


```


from llama_index.core import Settings




from llama_index.llms.openai import OpenAI




from llama_index.embeddings.openai import OpenAIEmbedding






Settings.llm = OpenAI(model="gpt-4o-mini")




Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")


```


```


from llama_index.core import VectorStoreIndex





index = VectorStoreIndex(base_nodes)





query_engine = index.as_query_engine(similarity_top_k=2)


```

## Evaluation Setup
[Section titled “Evaluation Setup”](https://developers.llamaindex.ai/python/examples/prompts/emotion_prompt/#evaluation-setup)
#### Golden Dataset
[Section titled “Golden Dataset”](https://developers.llamaindex.ai/python/examples/prompts/emotion_prompt/#golden-dataset)
Here we load in a “golden” dataset.
**NOTE** : We pull this in from Dropbox. For details on how to generate a dataset please see our `DatasetGenerator` module.

```


!wget "https://www.dropbox.com/scl/fi/fh9vsmmm8vu0j50l3ss38/llama2_eval_qr_dataset.json?rlkey=kkoaez7aqeb4z25gzc06ak6kb&dl=1"-O llama2_eval_qr_dataset.json


```


```


from llama_index.core.evaluation import QueryResponseDataset




# optional



eval_dataset = QueryResponseDataset.from_json("./llama2_eval_qr_dataset.json")


```

#### Get Evaluator
[Section titled “Get Evaluator”](https://developers.llamaindex.ai/python/examples/prompts/emotion_prompt/#get-evaluator)

```


from llama_index.core.evaluation import CorrectnessEvaluator, BatchEvalRunner






evaluator_c = CorrectnessEvaluator()





evaluator_dict = {"correctness": evaluator_c}




batch_runner = BatchEvalRunner(evaluator_dict, workers=2, show_progress=True)


```

#### Define Correctness Eval Function
[Section titled “Define Correctness Eval Function”](https://developers.llamaindex.ai/python/examples/prompts/emotion_prompt/#define-correctness-eval-function)

```


import numpy as np




from llama_index.core.evaluation.eval_utils import aget_responses






asyncdefget_correctness(query_engine, eval_qa_pairs, batch_runner):




# then evaluate




# TODO: evaluate a sample of generated results




eval_qs = [q for q, _ in eval_qa_pairs]




eval_answers = [a for _, a in eval_qa_pairs]




pred_responses =await aget_responses(




eval_qs, query_engine, show_progress=True






eval_results =await batch_runner.aevaluate_responses(




eval_qs, responses=pred_responses, reference=eval_answers





avg_correctness = np.array(




[r.score forin eval_results["correctness"]]




).mean()




return avg_correctness


```

## Try Out Emotion Prompts
[Section titled “Try Out Emotion Prompts”](https://developers.llamaindex.ai/python/examples/prompts/emotion_prompt/#try-out-emotion-prompts)
We pul some emotion stimuli from the paper to try out.

```


emotion_stimuli_dict = {




"ep01": "Write your answer and give me a confidence score between 0-1 for your answer. ",




"ep02": "This is very important to my career. ",




"ep03": "You'd better be sure.",




# add more from the paper here!!






# NOTE: ep06 is the combination of ep01, ep02, ep03




emotion_stimuli_dict["ep06"] = (




emotion_stimuli_dict["ep01"]




+ emotion_stimuli_dict["ep02"]




+ emotion_stimuli_dict["ep03"]



```

#### Initialize base QA Prompt
[Section titled “Initialize base QA Prompt”](https://developers.llamaindex.ai/python/examples/prompts/emotion_prompt/#initialize-base-qa-prompt)

```


from llama_index.core.prompts import RichPromptTemplate





qa_tmpl_str ="""\



Context information is below.


---------------------



{{ context_str }}



---------------------



Given the context information and not prior knowledge, \



answer the query.



{{ emotion_str }}




Query: {{ query_str }}




Answer: \





qa_tmpl = RichPromptTemplate(qa_tmpl_str)


```

#### Prepend emotions
[Section titled “Prepend emotions”](https://developers.llamaindex.ai/python/examples/prompts/emotion_prompt/#prepend-emotions)

```


QA_PROMPT_KEY="response_synthesizer:text_qa_template"


```


```


asyncdefrun_and_evaluate(




query_engine, eval_qa_pairs, batch_runner, emotion_stimuli_str, qa_tmpl





"""Run and evaluate."""




new_qa_tmpl = qa_tmpl.partial_format(emotion_str=emotion_stimuli_str)





old_qa_tmpl = query_engine.get_prompts()[QA_PROMPT_KEY]




query_engine.update_prompts({QA_PROMPT_KEY: new_qa_tmpl})




avg_correctness =await get_correctness(




query_engine, eval_qa_pairs, batch_runner





query_engine.update_prompts({QA_PROMPT_KEY: old_qa_tmpl})




return avg_correctness


```


```

# try out ep01



correctness_ep01 =await run_and_evaluate(




query_engine,




eval_dataset.qr_pairs,




batch_runner,




emotion_stimuli_dict["ep01"],




qa_tmpl,



```


```

100%|██████████| 60/60 [00:17<00:00,  3.43it/s]


100%|██████████| 60/60 [00:44<00:00,  1.34it/s]

```


```


print(correctness_ep01)


```


```

4.283333333333333

```


```

# try out ep02



correctness_ep02 =await run_and_evaluate(




query_engine,




eval_dataset.qr_pairs,




batch_runner,




emotion_stimuli_dict["ep02"],




qa_tmpl,



```


```

100%|██████████| 60/60 [00:17<00:00,  3.49it/s]


100%|██████████| 60/60 [00:46<00:00,  1.28it/s]

```


```


print(correctness_ep02)


```


```

4.466666666666667

```


```

# try none



correctness_base =await run_and_evaluate(




query_engine, eval_dataset.qr_pairs, batch_runner, "", qa_tmpl



```


```

100%|██████████| 60/60 [00:12<00:00,  4.74it/s]


100%|██████████| 60/60 [00:45<00:00,  1.32it/s]

```


```


print(correctness_base)


```


```

4.533333333333333

```

From this, we can see that more emotional prompts seem to lead to better performance!
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


