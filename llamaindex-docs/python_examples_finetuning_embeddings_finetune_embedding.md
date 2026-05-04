[Skip to content](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding/#_top)
# Finetune Embeddings 
In this notebook, we show users how to finetune their own embedding models.
We go through three main sections:
  1. Preparing the data (our `generate_qa_embedding_pairs` function makes this easy)
  2. Finetuning the model (using our `SentenceTransformersFinetuneEngine`)
  3. Evaluating the model on a validation knowledge corpus


## Generate Corpus
[Section titled “Generate Corpus”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding/#generate-corpus)
First, we create the corpus of text chunks by leveraging LlamaIndex to load some financial PDFs, and parsing/chunking into plain text chunks.

```


%pip install datasets




%pip install llama-index-llms-openai




%pip install llama-index-embeddings-openai




%pip install llama-index-finetuning




%pip install llama-index-readers-file




%pip install llama-index-embeddings-huggingface




%pip install "transformers[torch]"


```


```


import json





from llama_index.core import SimpleDirectoryReader




from llama_index.core.node_parser import SentenceSplitter




from llama_index.core.schema import MetadataMode


```

Download Data

```


!mkdir -p 'data/10k/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/10k/uber_2021.pdf'-O 'data/10k/uber_2021.pdf'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/10k/lyft_2021.pdf'-O 'data/10k/lyft_2021.pdf'


```


```


TRAIN_FILES= ["./data/10k/lyft_2021.pdf"]




VAL_FILES= ["./data/10k/uber_2021.pdf"]





TRAIN_CORPUS_FPATH="./data/train_corpus.json"




VAL_CORPUS_FPATH="./data/val_corpus.json"


```


```


defload_corpus(files, verbose=False):




if verbose:




print(f"Loading files {files}")





reader = SimpleDirectoryReader(input_files=files)




docs = reader.load_data()




if verbose:




print(f"Loaded {len(docs)} docs")





parser = SentenceSplitter()




nodes = parser.get_nodes_from_documents(docs, show_progress=verbose)





if verbose:




print(f"Parsed {len(nodes)} nodes")





return nodes


```

We do a very naive train/val split by having the Lyft corpus as the train dataset, and the Uber corpus as the val dataset.

```


train_nodes = load_corpus(TRAIN_FILES, verbose=True)




val_nodes = load_corpus(VAL_FILES, verbose=True)


```


```

Loading files ['./data/10k/lyft_2021.pdf']


Loaded 238 docs





Parsing nodes:   0%|          | 0/238 [00:00<?, ?it/s]




Parsed 344 nodes


Loading files ['./data/10k/uber_2021.pdf']


Loaded 307 docs





Parsing nodes:   0%|          | 0/307 [00:00<?, ?it/s]




Parsed 410 nodes

```

### Generate synthetic queries
[Section titled “Generate synthetic queries”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding/#generate-synthetic-queries)
Now, we use an LLM (gpt-3.5-turbo) to generate questions using each text chunk in the corpus as context.
Each pair of (generated question, text chunk used as context) becomes a datapoint in the finetuning dataset (either for training or evaluation).

```


from llama_index.finetuning import generate_qa_embedding_pairs




from llama_index.core.evaluation import EmbeddingQAFinetuneDataset


```


```


import os





OPENAI_API_KEY="sk-"




os.environ["OPENAI_API_KEY"] =OPENAI_API_KEY


```


```


from llama_index.llms.openai import OpenAI






train_dataset = generate_qa_embedding_pairs(




llm=OpenAI(model="gpt-3.5-turbo"),




nodes=train_nodes,




output_path="train_dataset.json",





val_dataset = generate_qa_embedding_pairs(




llm=OpenAI(model="gpt-3.5-turbo"),




nodes=val_nodes,




output_path="val_dataset.json",



```


```

100%|██████████| 344/344 [12:51<00:00,  2.24s/it]


100%|██████████| 410/410 [16:07<00:00,  2.36s/it]

```


```

# [Optional] Load



train_dataset = EmbeddingQAFinetuneDataset.from_json("train_dataset.json")




val_dataset = EmbeddingQAFinetuneDataset.from_json("val_dataset.json")


```

## Run Embedding Finetuning
[Section titled “Run Embedding Finetuning”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding/#run-embedding-finetuning)

```


from llama_index.finetuning import SentenceTransformersFinetuneEngine


```


```


finetune_engine = SentenceTransformersFinetuneEngine(




train_dataset,




model_id="BAAI/bge-small-en",




model_output_path="test_model",




val_dataset=val_dataset,



```


```

.gitattributes:   0%|          | 0.00/1.52k [00:00<?, ?B/s]





1_Pooling/config.json:   0%|          | 0.00/190 [00:00<?, ?B/s]





README.md:   0%|          | 0.00/90.8k [00:00<?, ?B/s]





config.json:   0%|          | 0.00/684 [00:00<?, ?B/s]





config_sentence_transformers.json:   0%|          | 0.00/124 [00:00<?, ?B/s]





model.safetensors:   0%|          | 0.00/133M [00:00<?, ?B/s]





pytorch_model.bin:   0%|          | 0.00/134M [00:00<?, ?B/s]





sentence_bert_config.json:   0%|          | 0.00/52.0 [00:00<?, ?B/s]





special_tokens_map.json:   0%|          | 0.00/125 [00:00<?, ?B/s]





tokenizer.json:   0%|          | 0.00/711k [00:00<?, ?B/s]





tokenizer_config.json:   0%|          | 0.00/366 [00:00<?, ?B/s]





vocab.txt:   0%|          | 0.00/232k [00:00<?, ?B/s]





modules.json:   0%|          | 0.00/349 [00:00<?, ?B/s]

```


```

finetune_engine.finetune()

```


```

Epoch:   0%|          | 0/2 [00:00<?, ?it/s]





Iteration:   0%|          | 0/69 [00:00<?, ?it/s]





Iteration:   0%|          | 0/69 [00:00<?, ?it/s]

```


```


embed_model = finetune_engine.get_finetuned_model()


```


```

embed_model

```


```

HuggingFaceEmbedding(model_name='test_model', embed_batch_size=10, callback_manager=<llama_index.callbacks.base.CallbackManager object at 0x2cc3d5cd0>, tokenizer_name='test_model', max_length=512, pooling=<Pooling.CLS: 'cls'>, normalize=True, query_instruction=None, text_instruction=None, cache_folder=None)

```

## Evaluate Finetuned Model
[Section titled “Evaluate Finetuned Model”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding/#evaluate-finetuned-model)
In this section, we evaluate 3 different embedding models:
  1. proprietary OpenAI embedding,
  2. open source `BAAI/bge-small-en`, and
  3. our finetuned embedding model.


We consider 2 evaluation approaches:
  1. a simple custom **hit rate** metric
  2. using `InformationRetrievalEvaluator` from sentence_transformers


We show that finetuning on synthetic (LLM-generated) dataset significantly improve upon an opensource embedding model.

```


from llama_index.embeddings.openai import OpenAIEmbedding




from llama_index.core import VectorStoreIndex




from llama_index.core.schema import TextNode




from tqdm.notebook import tqdm




import pandas as pd


```

### Define eval function
[Section titled “Define eval function”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding/#define-eval-function)
**Option 1** : We use a simple **hit rate** metric for evaluation:
  * for each (query, relevant_doc) pair,
  * we retrieve top-k documents with the query, and
  * it’s a **hit** if the results contain the relevant_doc.


This approach is very simple and intuitive, and we can apply it to both the proprietary OpenAI embedding as well as our open source and fine-tuned embedding models.

```


defevaluate(




dataset,




embed_model,




top_k=5,




verbose=False,





corpus = dataset.corpus




queries = dataset.queries




relevant_docs = dataset.relevant_docs





nodes = [TextNode(id_=id_, text=text) for id_, text in corpus.items()]




index = VectorStoreIndex(




nodes, embed_model=embed_model, show_progress=True





retriever = index.as_retriever(similarity_top_k=top_k)





eval_results = []




for query_id, query in tqdm(queries.items()):




retrieved_nodes = retriever.retrieve(query)




retrieved_ids = [node.node.node_id for node in retrieved_nodes]




expected_id = relevant_docs[query_id][0]




is_hit = expected_id in retrieved_ids  # assume 1 relevant doc





eval_result = {




"is_hit": is_hit,




"retrieved": retrieved_ids,




"expected": expected_id,




"query": query_id,





eval_results.append(eval_result)




return eval_results


```

**Option 2** : We use the `InformationRetrievalEvaluator` from sentence_transformers.
This provides a more comprehensive suite of metrics, but we can only run it against the sentencetransformers compatible models (open source and our finetuned model, _not_ the OpenAI embedding model).

```


from sentence_transformers.evaluation import InformationRetrievalEvaluator




from sentence_transformers import SentenceTransformer




from pathlib import Path






defevaluate_st(




dataset,




model_id,




name,





corpus = dataset.corpus




queries = dataset.queries




relevant_docs = dataset.relevant_docs





evaluator = InformationRetrievalEvaluator(




queries, corpus, relevant_docs, name=name





model = SentenceTransformer(model_id)




output_path ="results/"




Path(output_path).mkdir(exist_ok=True, parents=True)




return evaluator(model, output_path=output_path)


```

### Run Evals
[Section titled “Run Evals”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding/#run-evals)
#### OpenAI
[Section titled “OpenAI”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding/#openai)
Note: this might take a few minutes to run since we have to embed the corpus and queries

```


ada = OpenAIEmbedding()




ada_val_results = evaluate(val_dataset, ada)


```


```


df_ada = pd.DataFrame(ada_val_results)


```


```


hit_rate_ada = df_ada["is_hit"].mean()



hit_rate_ada

```


```

0.8779904306220095

```

### BAAI/bge-small-en
[Section titled “BAAI/bge-small-en”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding/#baaibge-small-en)

```


bge ="local:BAAI/bge-small-en"




bge_val_results = evaluate(val_dataset, bge)


```


```

Downloading (…)ab102/.gitattributes:   0%|          | 0.00/1.52k [00:00<?, ?B/s]





Downloading (…)_Pooling/config.json:   0%|          | 0.00/190 [00:00<?, ?B/s]





Downloading (…)2d2d7ab102/README.md:   0%|          | 0.00/78.9k [00:00<?, ?B/s]





Downloading (…)2d7ab102/config.json:   0%|          | 0.00/684 [00:00<?, ?B/s]





Downloading (…)ce_transformers.json:   0%|          | 0.00/124 [00:00<?, ?B/s]





Downloading model.safetensors:   0%|          | 0.00/133M [00:00<?, ?B/s]





Downloading pytorch_model.bin:   0%|          | 0.00/134M [00:00<?, ?B/s]





Downloading (…)nce_bert_config.json:   0%|          | 0.00/52.0 [00:00<?, ?B/s]





Downloading (…)cial_tokens_map.json:   0%|          | 0.00/125 [00:00<?, ?B/s]





Downloading (…)ab102/tokenizer.json:   0%|          | 0.00/711k [00:00<?, ?B/s]





Downloading (…)okenizer_config.json:   0%|          | 0.00/366 [00:00<?, ?B/s]





Downloading (…)2d2d7ab102/vocab.txt:   0%|          | 0.00/232k [00:00<?, ?B/s]





Downloading (…)d7ab102/modules.json:   0%|          | 0.00/229 [00:00<?, ?B/s]





Generating embeddings:   0%|          | 0/418 [00:00<?, ?it/s]






0%|          | 0/836 [00:00<?, ?it/s]


```


```


df_bge = pd.DataFrame(bge_val_results)


```


```


hit_rate_bge = df_bge["is_hit"].mean()



hit_rate_bge

```


```

0.7930622009569378

```


```


evaluate_st(val_dataset, "BAAI/bge-small-en", name="bge")


```


```

---------------------------------------------------------------------------



FileNotFoundError                         Traceback (most recent call last)



Cell In[59], line 1


----> 1 evaluate_st(val_dataset, "BAAI/bge-small-en", name='bge')




Cell In[49], line 15, in evaluate_st(dataset, model_id, name)



13 evaluator = InformationRetrievalEvaluator(queries, corpus, relevant_docs, name=name)




14 model = SentenceTransformer(model_id)



---> 15 return evaluator(model, output_path='results/')




File ~/Programming/gpt_index/.venv/lib/python3.10/site-packages/sentence_transformers/evaluation/InformationRetrievalEvaluator.py:104, in InformationRetrievalEvaluator.__call__(self, model, output_path, epoch, steps, *args, **kwargs)



102 csv_path = os.path.join(output_path, self.csv_file)




103 if not os.path.isfile(csv_path):



--> 104     fOut = open(csv_path, mode="w", encoding="utf-8")



105     fOut.write(",".join(self.csv_headers))




106     fOut.write("\n")





FileNotFoundError: [Errno 2] No such file or directory: 'results/Information-Retrieval_evaluation_bge_results.csv'

```

### Finetuned
[Section titled “Finetuned”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding/#finetuned)

```


finetuned ="local:test_model"




val_results_finetuned = evaluate(val_dataset, finetuned)


```


```


df_finetuned = pd.DataFrame(val_results_finetuned)


```


```


hit_rate_finetuned = df_finetuned["is_hit"].mean()



hit_rate_finetuned

```


```


evaluate_st(val_dataset, "test_model", name="finetuned")


```

### Summary of Results
[Section titled “Summary of Results”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding/#summary-of-results)
#### Hit rate
[Section titled “Hit rate”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding/#hit-rate)

```


df_ada["model"] ="ada"




df_bge["model"] ="bge"




df_finetuned["model"] ="fine_tuned"


```

We can see that fine-tuning our small open-source embedding model drastically improve its retrieval quality (even approaching the quality of the proprietary OpenAI embedding)!

```


df_all = pd.concat([df_ada, df_bge, df_finetuned])




df_all.groupby("model").mean("is_hit")


```

#### InformationRetrievalEvaluator
[Section titled “InformationRetrievalEvaluator”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding/#informationretrievalevaluator)

```


df_st_bge = pd.read_csv(




"results/Information-Retrieval_evaluation_bge_results.csv"





df_st_finetuned = pd.read_csv(




"results/Information-Retrieval_evaluation_finetuned_results.csv"



```

We can see that embedding finetuning improves metrics consistently across the suite of eval metrics

```


df_st_bge["model"] ="bge"




df_st_finetuned["model"] ="fine_tuned"




df_st_all = pd.concat([df_st_bge, df_st_finetuned])




df_st_all = df_st_all.set_index("model")



df_st_all

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


