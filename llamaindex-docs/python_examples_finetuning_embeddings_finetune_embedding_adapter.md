[Skip to content](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding_adapter/#_top)
# Finetuning an Adapter on Top of any Black-Box Embedding Model 
We have capabilities in LlamaIndex allowing you to fine-tune an adapter on top of embeddings produced from any model (sentence_transformers, OpenAI, and more). 
This allows you to transform your embedding representations into a new latent space that’s optimized for retrieval over your specific data and queries. This can lead to small increases in retrieval performance that in turn translate to better performing RAG systems.
We do this via our `EmbeddingAdapterFinetuneEngine` abstraction. We fine-tune three types of adapters:
  * Linear
  * 2-Layer NN
  * Custom NN


## Generate Corpus
[Section titled “Generate Corpus”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding_adapter/#generate-corpus)
We use our helper abstractions, `generate_qa_embedding_pairs`, to generate our training and evaluation dataset. This function takes in any set of text nodes (chunks) and generates a structured dataset containing (question, context) pairs.

```


%pip install llama-index-embeddings-openai




%pip install llama-index-embeddings-adapter




%pip install llama-index-finetuning


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

Loading files ['../../../examples/data/10k/lyft_2021.pdf']


Loaded 238 docs





Parsing documents into nodes:   0%|          | 0/238 [00:00<?, ?it/s]




Parsed 349 nodes


Loading files ['../../../examples/data/10k/uber_2021.pdf']


Loaded 307 docs





Parsing documents into nodes:   0%|          | 0/307 [00:00<?, ?it/s]




Parsed 418 nodes

```

### Generate synthetic queries
[Section titled “Generate synthetic queries”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding_adapter/#generate-synthetic-queries)
Now, we use an LLM (gpt-3.5-turbo) to generate questions using each text chunk in the corpus as context.
Each pair of (generated question, text chunk used as context) becomes a datapoint in the finetuning dataset (either for training or evaluation).

```


from llama_index.finetuning import generate_qa_embedding_pairs




from llama_index.core.evaluation import EmbeddingQAFinetuneDataset


```


```


train_dataset = generate_qa_embedding_pairs(train_nodes)




val_dataset = generate_qa_embedding_pairs(val_nodes)





train_dataset.save_json("train_dataset.json")




val_dataset.save_json("val_dataset.json")


```


```

# [Optional] Load



train_dataset = EmbeddingQAFinetuneDataset.from_json("train_dataset.json")




val_dataset = EmbeddingQAFinetuneDataset.from_json("val_dataset.json")


```

## Run Embedding Finetuning
[Section titled “Run Embedding Finetuning”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding_adapter/#run-embedding-finetuning)
We then fine-tune our linear adapter on top of an existing embedding model. We import our new `EmbeddingAdapterFinetuneEngine` abstraction, which takes in an existing embedding model and a set of training parameters.
#### Fine-tune bge-small-en (default)
[Section titled “Fine-tune bge-small-en (default)”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding_adapter/#fine-tune-bge-small-en-default)

```


from llama_index.finetuning import EmbeddingAdapterFinetuneEngine




from llama_index.core.embeddings import resolve_embed_model




import torch





base_embed_model = resolve_embed_model("local:BAAI/bge-small-en")





finetune_engine = EmbeddingAdapterFinetuneEngine(




train_dataset,




base_embed_model,




model_output_path="model_output_test",




# bias=True,




epochs=4,




verbose=True,




# optimizer_class=torch.optim.SGD,




# optimizer_params={"lr": 0.01}



```


```

finetune_engine.finetune()

```


```


embed_model = finetune_engine.get_finetuned_model()




# alternatively import model



from llama_index.core.embeddings import LinearAdapterEmbeddingModel




# embed_model = LinearAdapterEmbeddingModel(base_embed_model, "model_output_test")

```

## Evaluate Finetuned Model
[Section titled “Evaluate Finetuned Model”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding_adapter/#evaluate-finetuned-model)
We compare the fine-tuned model against the base model, as well as against text-embedding-ada-002.
We evaluate with two ranking metrics:
  * **Hit-rate metric** : For each (query, context) pair, we retrieve the top-k documents with the query. It’s a hit if the results contain the ground-truth context.
  * **Mean Reciprocal Rank** : A slightly more granular ranking metric that looks at the “reciprocal rank” of the ground-truth context in the top-k retrieved set. The reciprocal rank is defined as 1/rank. Of course, if the results don’t contain the context, then the reciprocal rank is 0.



```


from llama_index.embeddings.openai import OpenAIEmbedding




from llama_index.core import VectorStoreIndex




from llama_index.core.schema import TextNode




from tqdm.notebook import tqdm




import pandas as pd





from eval_utils import evaluate, display_results


```


```


ada = OpenAIEmbedding()




ada_val_results = evaluate(val_dataset, ada)


```


```

Generating embeddings:   0%|          | 0/395 [00:00<?, ?it/s]




100%|████████████████████████████████████████████████████████████████| 790/790 [03:03<00:00,  4.30it/s]

```


```


display_results(["ada"], [ada_val_results])


```


```

.dataframe tbody tr th {



vertical-align: top;





.dataframe thead th {



text-align: right;



```
  
| retrievers  | hit_rate  | mrr  |  
| --- | --- | --- |  
| 0  | ada  | 0.870886  | 0.72884  |  

```


bge ="local:BAAI/bge-small-en"




bge_val_results = evaluate(val_dataset, bge)


```


```

Generating embeddings:   0%|          | 0/395 [00:00<?, ?it/s]




100%|████████████████████████████████████████████████████████████████| 790/790 [00:23<00:00, 33.76it/s]

```


```


display_results(["bge"], [bge_val_results])


```


```

.dataframe tbody tr th {



vertical-align: top;





.dataframe thead th {



text-align: right;



```
  
| retrievers  | hit_rate  | mrr  |  
| --- | --- | --- |  
| 0  | bge  | 0.787342  | 0.643038  |  

```


ft_val_results = evaluate(val_dataset, embed_model)


```


```

Generating embeddings:   0%|          | 0/395 [00:00<?, ?it/s]




100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 790/790 [00:21<00:00, 36.95it/s]

```


```


display_results(["ft"], [ft_val_results])


```


```

.dataframe tbody tr th {



vertical-align: top;





.dataframe thead th {



text-align: right;



```
  
| retrievers  | hit_rate  | mrr  |  
| --- | --- | --- |  
| 0  | ft  | 0.798734  | 0.662152  |  
Here we show all the results concatenated together.

```

display_results(



["ada", "bge", "ft"], [ada_val_results, bge_val_results, ft_val_results]



```


```

.dataframe tbody tr th {



vertical-align: top;





.dataframe thead th {



text-align: right;



```
  
| retrievers  | hit_rate  | mrr  |  
| --- | --- | --- |  
| 0  | ada  | 0.870886  | 0.730105  |  
| 1  | bge  | 0.787342  | 0.643038  |  
| 2  | ft  | 0.798734  | 0.662152  |  
## Fine-tune a Two-Layer Adapter
[Section titled “Fine-tune a Two-Layer Adapter”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding_adapter/#fine-tune-a-two-layer-adapter)
Let’s try fine-tuning a two-layer NN as well!
It’s a simple two-layer NN with a ReLU activation and a residual layer at the end.
We train for 25 epochs - longer than the linear adapter - and preserve checkpoints every 100 steps.

```

# requires torch dependency



from llama_index.core.embeddings.adapter_utils import TwoLayerNN





from llama_index.finetuning import EmbeddingAdapterFinetuneEngine




from llama_index.core.embeddings import resolve_embed_model




from llama_index.embeddings.adapter import AdapterEmbeddingModel


```


```


base_embed_model = resolve_embed_model("local:BAAI/bge-small-en")




adapter_model = TwoLayerNN(




384# input dimension




1024# hidden dimension




384# output dimension




bias=True,




add_residual=True,






finetune_engine = EmbeddingAdapterFinetuneEngine(




train_dataset,




base_embed_model,




model_output_path="model5_output_test",




model_checkpoint_path="model5_ck",




adapter_model=adapter_model,




epochs=25,




verbose=True,



```


```

finetune_engine.finetune()

```


```


embed_model_2layer = finetune_engine.get_finetuned_model(




adapter_cls=TwoLayerNN



```

### Evaluation Results
[Section titled “Evaluation Results”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding_adapter/#evaluation-results)
Run the same evaluation script used in the previous section to measure hit-rate/MRR within the two-layer model.

```

# load model from checkpoint in the midde



embed_model_2layer = AdapterEmbeddingModel(




base_embed_model,




"model5_output_test",




TwoLayerNN,



```


```


from eval_utils import evaluate, display_results


```


```


ft_val_results_2layer = evaluate(val_dataset, embed_model_2layer)


```


```

Generating embeddings:   0%|          | 0/395 [00:00<?, ?it/s]




100%|████████████████████████████████████████████████████████████████| 790/790 [00:21<00:00, 36.93it/s]

```


```

# comment out if you haven't run ada/bge yet


display_results(



["ada", "bge", "ft_2layer"],




[ada_val_results, bge_val_results, ft_val_results_2layer],





# uncomment if you just want to display the fine-tuned model's results


# display_results(["ft_2layer"], [ft_val_results_2layer])

```


```

.dataframe tbody tr th {



vertical-align: top;





.dataframe thead th {



text-align: right;



```
  
| retrievers  | hit_rate  | mrr  |  
| --- | --- | --- |  
| 0  | ada  | 0.870886  | 0.728840  |  
| 1  | bge  | 0.787342  | 0.643038  |  
| 2  | ft_2layer  | 0.798734  | 0.662848  |  

```

# load model from checkpoint in the midde



embed_model_2layer_s900 = AdapterEmbeddingModel(




base_embed_model,




"model5_ck/step_900",




TwoLayerNN,



```


```


ft_val_results_2layer_s900 = evaluate(val_dataset, embed_model_2layer_s900)


```


```

Generating embeddings:   0%|          | 0/395 [00:00<?, ?it/s]




100%|████████████████████████████████████████████████████████████████| 790/790 [00:19<00:00, 40.57it/s]

```


```

# comment out if you haven't run ada/bge yet


display_results(



["ada", "bge", "ft_2layer_s900"],




[ada_val_results, bge_val_results, ft_val_results_2layer_s900],





# uncomment if you just want to display the fine-tuned model's results


# display_results(["ft_2layer_s900"], [ft_val_results_2layer_s900])

```


```

.dataframe tbody tr th {



vertical-align: top;





.dataframe thead th {



text-align: right;



```
  
| retrievers  | hit_rate  | mrr  |  
| --- | --- | --- |  
| 0  | ada  | 0.870886  | 0.728840  |  
| 1  | bge  | 0.787342  | 0.643038  |  
| 2  | ft_2layer_s900  | 0.803797  | 0.667426  |  
## Try Your Own Custom Model
[Section titled “Try Your Own Custom Model”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding_adapter/#try-your-own-custom-model)
You can define your own custom adapter here! Simply subclass `BaseAdapter`, which is a light wrapper around the `nn.Module` class.
You just need to subclass `forward` and `get_config_dict`.
Just make sure you’re familiar with writing `PyTorch` code :)

```


from llama_index.core.embeddings.adapter_utils import BaseAdapter




import torch.nn.functional as F




from torch import nn, Tensor




from typing import Dict


```


```


classCustomNN(BaseAdapter):




"""Custom NN transformation.





Is a copy of our TwoLayerNN, showing it here for notebook purposes.





Args:




in_features (int): Input dimension.




hidden_features (int): Hidden dimension.




out_features (int): Output dimension.




bias (bool): Whether to use bias. Defaults to False.




activation_fn_str (str): Name of activation function. Defaults to "relu".







def__init__(




self,




in_features: int,




hidden_features: int,




out_features: int,




bias: bool=False,




add_residual: bool=False,




) -> None:




super(CustomNN, self).__init__()




self.in_features = in_features




self.hidden_features = hidden_features




self.out_features = out_features




self.bias = bias





self.linear1 = nn.Linear(in_features, hidden_features, bias=True)




self.linear2 = nn.Linear(hidden_features, out_features, bias=True)




self._add_residual = add_residual




# if add_residual, then add residual_weight (init to 0)




self.residual_weight = nn.Parameter(torch.zeros(1))





defforward(self, embed: Tensor) -> Tensor:




"""Forward pass (Wv).





Args:




embed (Tensor): Input tensor.






output1 =self.linear1(embed)




output1 = F.relu(output1)




output2 =self.linear2(output1)





ifself._add_residual:




output2 =self.residual_weight * output2 + embed





return output2





defget_config_dict(self) -> Dict:




"""Get config dict."""




return {




"in_features": self.in_features,




"hidden_features": self.hidden_features,




"out_features": self.out_features,




"bias": self.bias,




"add_residual": self._add_residual,



```


```


custom_adapter = CustomNN(




384# input dimension




1024# hidden dimension




384# output dimension




bias=True,




add_residual=True,






finetune_engine = EmbeddingAdapterFinetuneEngine(




train_dataset,




base_embed_model,




model_output_path="custom_model_output",




model_checkpoint_path="custom_model_ck",




adapter_model=custom_adapter,




epochs=25,




verbose=True,



```


```

finetune_engine.finetune()

```


```


embed_model_custom = finetune_engine.get_finetuned_model(




adapter_cls=CustomAdapter



```

### Evaluation Results
[Section titled “Evaluation Results”](https://developers.llamaindex.ai/python/examples/finetuning/embeddings/finetune_embedding_adapter/#evaluation-results-1)
Run the same evaluation script used in the previous section to measure hit-rate/MRR.

```

# [optional] load model manually


# embed_model_custom = AdapterEmbeddingModel(


#     base_embed_model,


#     "custom_model_ck/step_300",


#     TwoLayerNN,


```


```


from eval_utils import evaluate, display_results


```


```


ft_val_results_custom = evaluate(val_dataset, embed_model_custom)


```


```

Generating embeddings:   0%|          | 0/395 [00:00<?, ?it/s]




100%|████████████████████████████████████████████████████████████████| 790/790 [00:20<00:00, 37.77it/s]

```


```


display_results(["ft_custom"]x, [ft_val_results_custom])


```


```

.dataframe tbody tr th {



vertical-align: top;





.dataframe thead th {



text-align: right;



```
  
| retrievers  | hit_rate  | mrr  |  
| --- | --- | --- |  
| 0  | ft_custom  | 0.789873  | 0.645127  |  
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


