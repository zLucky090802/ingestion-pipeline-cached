[Skip to content](https://developers.llamaindex.ai/python/examples/multi_modal/structured_image_retrieval/#_top)
# Semi-structured Image Retrieval 
In this notebook we show you how to perform semi-structured retrieval over images.
Given a set of images, we can infer structured outputs from them using Gemini Pro Vision.
We can then index these structured outputs in a vector database. We then take full advantage of semantic search + metadata filter capabilities with **auto-retrieval** : this allows us to ask both structured and semantic questions over this data!
(An alternative is to put this data into a SQL database, letting you do text-to-SQL. These techniques are quite closely related).

```


%pip install llama-index-multi-modal-llms-gemini




%pip install llama-index-vector-stores-qdrant




%pip install llama-index-embeddings-gemini




%pip install llama-index-llms-gemini


```


```


!pip install llama-index 'google-generativeai>=0.3.0' matplotlib qdrant_client


```

## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/examples/multi_modal/structured_image_retrieval/#setup)
### Get Google API Key
[Section titled “Get Google API Key”](https://developers.llamaindex.ai/python/examples/multi_modal/structured_image_retrieval/#get-google-api-key)

```


import os





GOOGLE_API_KEY=""# add your GOOGLE API key here




os.environ["GOOGLE_API_KEY"] =GOOGLE_API_KEY


```

### Download Images
[Section titled “Download Images”](https://developers.llamaindex.ai/python/examples/multi_modal/structured_image_retrieval/#download-images)
We download the full SROIE v2 dataset from Kaggle [here](https://www.kaggle.com/datasets/urbikn/sroie-datasetv2).
This dataset consists of scanned receipt images. We ignore the ground-truth labels for now, and use the test set images to test out Gemini’s capabilities for structured output extraction.
### Get Image Files
[Section titled “Get Image Files”](https://developers.llamaindex.ai/python/examples/multi_modal/structured_image_retrieval/#get-image-files)
Now that the images are downloaded, we can get a list of the file names.

```


from pathlib import Path




import random




from typing import Optional


```


```


defget_image_files(




dir_path, sample: Optional[int] =10, shuffle: bool=False





dir_path = Path(dir_path)




image_paths = []




for image_path in dir_path.glob("*.jpg"):




image_paths.append(image_path)





random.shuffle(image_paths)




if sample:




return image_paths[:sample]




else:




return image_paths


```


```


image_files = get_image_files("SROIE2019/test/img", sample=100)


```

## Use Gemini to extract structured outputs
[Section titled “Use Gemini to extract structured outputs”](https://developers.llamaindex.ai/python/examples/multi_modal/structured_image_retrieval/#use-gemini-to-extract-structured-outputs)
Here we use Gemini to extract structured outputs.
  1. Define a ReceiptInfo pydantic class that captures the structured outputs we want to extract. We extract fields like `company`, `date`, `total`, and also `summary`.
  2. Define a `pydantic_gemini` function which will convert input documents into a response.


### Define a ReceiptInfo pydantic class
[Section titled “Define a ReceiptInfo pydantic class”](https://developers.llamaindex.ai/python/examples/multi_modal/structured_image_retrieval/#define-a-receiptinfo-pydantic-class)

```


from pydantic import BaseModel, Field






classReceiptInfo(BaseModel):




company: str= Field(..., description="Company name")




date: str= Field(..., description="Date field in DD/MM/YYYY format")




address: str= Field(..., description="Address")




total: float= Field(..., description="total amount")




currency: str= Field(




..., description="Currency of the country (in abbreviations)"





summary: str= Field(





description="Extracted text summary of the receipt, including items purchased, the type of store, the location, and any other notable salient features (what does the purchase seem to be for?).",



```

### Define a `pydantic_gemini` function
[Section titled “Define a pydantic_gemini function”](https://developers.llamaindex.ai/python/examples/multi_modal/structured_image_retrieval/#define-a-pydantic_gemini-function)

```


from llama_index.multi_modal_llms.gemini import GeminiMultiModal




from llama_index.core.program import MultiModalLLMCompletionProgram




from llama_index.core.output_parsers import PydanticOutputParser





prompt_template_str ="""\




Can you summarize the image and return a response \




with the following JSON format: \







asyncdefpydantic_gemini(output_class, image_documents, prompt_template_str):




gemini_llm = GeminiMultiModal(




api_key=GOOGLE_API_KEY, model_name="models/gemini-pro-vision"






llm_program = MultiModalLLMCompletionProgram.from_defaults(




output_parser=PydanticOutputParser(output_class),




image_documents=image_documents,




prompt_template_str=prompt_template_str,




multi_modal_llm=gemini_llm,




verbose=True,






response =await llm_program.acall()




return response


```

### Run over images
[Section titled “Run over images”](https://developers.llamaindex.ai/python/examples/multi_modal/structured_image_retrieval/#run-over-images)

```


from llama_index.core import SimpleDirectoryReader




from llama_index.core.async_utils import run_jobs






asyncdefaprocess_image_file(image_file):




# should load one file




print(f"Image file: {image_file}")




img_docs = SimpleDirectoryReader(input_files=[image_file]).load_data()




output =await pydantic_gemini(ReceiptInfo, img_docs, prompt_template_str)




return output






asyncdefaprocess_image_files(image_files):




"""Process metadata on image files."""





new_docs = []




tasks = []




for image_file in image_files:




task = aprocess_image_file(image_file)




tasks.append(task)





outputs =await run_jobs(tasks, show_progress=True, workers=5)




return outputs


```


```


outputs =await aprocess_image_files(image_files)


```


```


outputs[4]


```


```

ReceiptInfo(company='KEDAI BUKU NEW ACHIEVERS', date='15/09/2017', address='NO. 12 & 14, JALAN HIJAUAN JINANG 27/54 TAMAN ALAM MEGAH, SEKSYEN 27 40400 SHAH ALAM, SELANGOR D. E.', total=48.0, currency='MYR', summary='Purchase of books and school supplies at a bookstore.')

```

### Convert Structured Representation to `TextNode` objects
[Section titled “Convert Structured Representation to TextNode objects”](https://developers.llamaindex.ai/python/examples/multi_modal/structured_image_retrieval/#convert-structured-representation-to-textnode-objects)
Node objects are the core units that are indexed in vector stores in LlamaIndex. We define a simple converter function to map the `ReceiptInfo` objects to `TextNode` objects.

```


from llama_index.core.schema import TextNode




from typing import List






defget_nodes_from_objs(




objs: List[ReceiptInfo], image_files: List[str]



) -> TextNode:



"""Get nodes from objects."""




nodes = []




for image_file, obj inzip(image_files, objs):




node = TextNode(




text=obj.summary,




metadata={




"company": obj.company,




"date": obj.date,




"address": obj.address,




"total": obj.total,




"currency": obj.currency,




"image_file": str(image_file),





excluded_embed_metadata_keys=["image_file"],




excluded_llm_metadata_keys=["image_file"],





nodes.append(node)




return nodes


```


```


nodes = get_nodes_from_objs(outputs, image_files)


```


```


print(nodes[0].get_content(metadata_mode="all"))


```


```

company: UNIHAIKKA INTERNATIONAL SDN BHD


date: 13/09/2018


address: 12, Jalan Tampoi 7/4, Kawasan Perindustrian Tampoi, 81200 Johor Bahru, Johor


total: 8.85


currency: MYR


image_file: SROIE2019/test/img/X51007846371.jpg



The receipt is from a restaurant called Bar Wang Rice. The total amount is 8.85 MYR. The items purchased include chicken, vegetables, and a drink.

```

### Index these nodes in vector stores
[Section titled “Index these nodes in vector stores”](https://developers.llamaindex.ai/python/examples/multi_modal/structured_image_retrieval/#index-these-nodes-in-vector-stores)

```


import qdrant_client




from llama_index.vector_stores.qdrant import QdrantVectorStore




from llama_index.core import StorageContext




from llama_index.core import VectorStoreIndex




from llama_index.embeddings.gemini import GeminiEmbedding




from llama_index.llms.gemini import Gemini




from llama_index.core import Settings




# Create a local Qdrant vector store



client = qdrant_client.QdrantClient(path="qdrant_gemini")





vector_store = QdrantVectorStore(client=client, collection_name="collection")




# global settings



Settings.embed_model = GeminiEmbedding(




model_name="models/embedding-001", api_key=GOOGLE_API_KEY





Settings.llm = (Gemini(api_key=GOOGLE_API_KEY),)





storage_context = StorageContext.from_defaults(vector_store=vector_store)





index = VectorStoreIndex(




nodes=nodes,




storage_context=storage_context,



```

## Define Auto-Retriever
[Section titled “Define Auto-Retriever”](https://developers.llamaindex.ai/python/examples/multi_modal/structured_image_retrieval/#define-auto-retriever)
Now we can setup our auto-retriever, which can perform semi-structured queries: structured queries through inferring metadata filters, along with semantic search.
We setup our schema definition capturing the receipt info which is fed into the prompt.

```


from llama_index.core.vector_stores import MetadataInfo, VectorStoreInfo






vector_store_info = VectorStoreInfo(




content_info="Receipts",




metadata_info=[




MetadataInfo(




name="company",




description="The name of the store",




type="string",





MetadataInfo(




name="address",




description="The address of the store",




type="string",





MetadataInfo(




name="date",




description="The date of the purchase (in DD/MM/YYYY format)",




type="string",





MetadataInfo(




name="total",




description="The final amount",




type="float",





MetadataInfo(




name="currency",




description="The currency of the country the purchase was made (abbreviation)",




type="string",





```


```


from llama_index.core.retrievers import VectorIndexAutoRetriever





retriever = VectorIndexAutoRetriever(




index,




vector_store_info=vector_store_info,




similarity_top_k=2,




empty_query_top_k=10# if only metadata filters are specified, this is the limit




verbose=True,



```


```

# from PIL import Image



import requests




from io import BytesIO




import matplotlib.pyplot as plt




from IPython.display import Image






defdisplay_response(nodes: List[TextNode]):




"""Display response."""




for node in nodes:




print(node.get_content(metadata_mode="all"))




# img = Image.open(open(node.metadata["image_file"], 'rb'))




display(Image(filename=node.metadata["image_file"], width=200))


```

## Run Some Queries
[Section titled “Run Some Queries”](https://developers.llamaindex.ai/python/examples/multi_modal/structured_image_retrieval/#run-some-queries)
Let’s try out different types of queries!

```


nodes = retriever.retrieve(




"Tell me about some restaurant orders of noodles with total < 25"




display_response(nodes)

```


```

Using query str: restaurant orders of noodles


Using filters: [('total', '<', 25)]


company: Restoran Wan Sheng


date: 23-03-2018


address: No. 2, Jalan Temenggung 19/9, Seksyen 9, Bandar Mahkota Cheras, 43200 Cheras, Selangor


total: 6.7


currency: MYR


image_file: SROIE2019/test/img/X51005711443.jpg



Teh (B), Cham (B), Bunga Kekwa, Take Away

```


```

company: UNIHAIKKA INTERNATIONAL SDN BHD


date: 19/06/2018


address: 12, Jalan Tampoi 7/4, Kawasan Perindustrian Tampoi 81200 Johor Bahru, Johor


total: 8.45


currency: MYR


image_file: SROIE2019/test/img/X51007846392.jpg



The receipt is from a restaurant called Bar Wang Rice. The total amount is 8.45 MYR. The items purchased include 1 plate of fried noodles, 1 plate of chicken, and 1 plate of vegetables.

```


```


nodes = retriever.retrieve("Tell me about some grocery purchases")



display_response(nodes)

```


```

Using query str: grocery purchases


Using filters: []


company: GARDENIA BAKERIES (KL) SDN BHD


date: 24/09/2017


address: LOT 3, JALAN PELABUR 23/1, 40300 SHAH ALAM, SELANGOR


total: 38.55


currency: RM


image_file: SROIE2019/test/img/X51006556829.jpg



Purchase of groceries from a supermarket.

```


```

company: Segi Cash & Carry Sdn. Bhd


date: 02/02/2017


address: PT17920, SEKSYEN U9,


40150 SHAH ALAM,


SELANGOR DARUL EHSAN


total: 27.0


currency: RM


image_file: SROIE2019/test/img/X51006335818.jpg



Purchase of groceries at Segi Cash & Carry Sdn. Bhd. on 02/02/2017. The total amount of the purchase is RM27.

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


