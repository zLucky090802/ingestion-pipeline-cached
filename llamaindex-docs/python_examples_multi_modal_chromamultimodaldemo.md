[Skip to content](https://developers.llamaindex.ai/python/examples/multi_modal/chromamultimodaldemo/#_top)
# Chroma Multi-Modal Demo with LlamaIndex 
> [Chroma](https://docs.trychroma.com/getting-started) is a AI-native open-source vector database focused on developer productivity and happiness. Chroma is licensed under Apache 2.0.


Chroma is fully-typed, fully-tested and fully-documented.
Install Chroma with:
Terminal window
```


pipinstallchromadb


```

Chroma runs in various modes. See below for examples of each integrated with LangChain.
  * `in-memory` - in a python script or jupyter notebook
  * `in-memory with persistence` - in a script or notebook and save/load to disk
  * `in a docker container` - as a server running your local machine or in the cloud


Like any other database, you can:
  * `.add`
  * `.get`
  * `.update`
  * `.upsert`
  * `.delete`
  * `.peek`
  * and `.query` runs the similarity search.


View full docs at [docs](https://docs.trychroma.com/reference/Collection).
## Basic Example
[Section titled “Basic Example”](https://developers.llamaindex.ai/python/examples/multi_modal/chromamultimodaldemo/#basic-example)
In this basic example, we take the a Paul Graham essay, split it into chunks, embed it using an open-source embedding model, load it into Chroma, and then query it.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-vector-stores-qdrant




%pip install llama-index-embeddings-huggingface




%pip install llama-index-vector-stores-chroma


```


```


!pip install llama-index


```

#### Creating a Chroma Index
[Section titled “Creating a Chroma Index”](https://developers.llamaindex.ai/python/examples/multi_modal/chromamultimodaldemo/#creating-a-chroma-index)

```


!pip install llama-index chromadb --quiet




!pip install chromadb==0.4.17




!pip install sentence-transformers




!pip install pydantic==1.10.11




!pip install open-clip-torch


```


```

# import



from llama_index.core import VectorStoreIndex, SimpleDirectoryReader




from llama_index.vector_stores.chroma import ChromaVectorStore




from llama_index.core import StorageContext




from llama_index.embeddings.huggingface import HuggingFaceEmbedding




from IPython.display import Markdown, display




import chromadb


```


```

# set up OpenAI



import os




import openai





OPENAI_API_KEY=""




openai.api_key =OPENAI_API_KEY




os.environ["OPENAI_API_KEY"] =OPENAI_API_KEY


```

## Download Images and Texts from Wikipedia
[Section titled “Download Images and Texts from Wikipedia”](https://developers.llamaindex.ai/python/examples/multi_modal/chromamultimodaldemo/#download-images-and-texts-from-wikipedia)

```


import requests






defget_wikipedia_images(title):




response = requests.get(




"https://en.wikipedia.org/w/api.php",




params={




"action": "query",




"format": "json",




"titles": title,




"prop": "imageinfo",




"iiprop": "url|dimensions|mime",




"generator": "images",




"gimlimit": "50",





).json()




image_urls = []




for page in response["query"]["pages"].values():




if page["imageinfo"][0]["url"].endswith(".jpg") or page["imageinfo"][





]["url"].endswith(".png"):




image_urls.append(page["imageinfo"][0]["url"])




return image_urls


```


```


from pathlib import Path




import urllib.request





image_uuid =0




MAX_IMAGES_PER_WIKI=20





wiki_titles = {




"Tesla Model X",




"Pablo Picasso",




"Rivian",




"The Lord of the Rings",




"The Matrix",




"The Simpsons",






data_path = Path("mixed_wiki")




ifnot data_path.exists():




Path.mkdir(data_path)





for title in wiki_titles:




response = requests.get(




"https://en.wikipedia.org/w/api.php",




params={




"action": "query",




"format": "json",




"titles": title,




"prop": "extracts",




"explaintext": True,





).json()




page =next(iter(response["query"]["pages"].values()))




wiki_text = page["extract"]





withopen(data_path /f"{title}.txt", "w") as fp:




fp.write(wiki_text)





images_per_wiki =0





# page_py = wikipedia.page(title)




list_img_urls = get_wikipedia_images(title)




# print(list_img_urls)





for url in list_img_urls:




if url.endswith(".jpg") or url.endswith(".png"):




image_uuid +=1




# image_file_name = title + "_" + url.split("/")[-1]





urllib.request.urlretrieve(




url, data_path /f"{image_uuid}.jpg"





images_per_wiki +=1




# Limit the number of images downloaded per wiki page to 15




if images_per_wiki MAX_IMAGES_PER_WIKI:




break




except:




print(str(Exception("No images found for Wikipedia page: ")) + title)




continue


```

## Set the embedding model
[Section titled “Set the embedding model”](https://developers.llamaindex.ai/python/examples/multi_modal/chromamultimodaldemo/#set-the-embedding-model)

```


from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction




# set defalut text and image embedding functions



embedding_function = OpenCLIPEmbeddingFunction()


```


```

/Users/haotianzhang/llama_index/venv/lib/python3.11/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html



from .autonotebook import tqdm as notebook_tqdm


```

## Build Chroma Multi-Modal Index with LlamaIndex
[Section titled “Build Chroma Multi-Modal Index with LlamaIndex”](https://developers.llamaindex.ai/python/examples/multi_modal/chromamultimodaldemo/#build-chroma-multi-modal-index-with-llamaindex)

```


from llama_index.core.indices import MultiModalVectorStoreIndex




from llama_index.vector_stores.qdrant import QdrantVectorStore




from llama_index.core import SimpleDirectoryReader, StorageContext




from chromadb.utils.data_loaders import ImageLoader





image_loader = ImageLoader()




# create client and a new collection



chroma_client = chromadb.EphemeralClient()




chroma_collection = chroma_client.create_collection(




"multimodal_collection",




embedding_function=embedding_function,




data_loader=image_loader,






# load documents



documents = SimpleDirectoryReader("./mixed_wiki/").load_data()




# set up ChromaVectorStore and load in data



vector_store = ChromaVectorStore(chroma_collection=chroma_collection)




storage_context = StorageContext.from_defaults(vector_store=vector_store)




index = VectorStoreIndex.from_documents(




documents,




storage_context=storage_context,



```

## Retrieve results from Multi-Modal Index
[Section titled “Retrieve results from Multi-Modal Index”](https://developers.llamaindex.ai/python/examples/multi_modal/chromamultimodaldemo/#retrieve-results-from-multi-modal-index)

```


retriever = index.as_retriever(similarity_top_k=50)




retrieval_results = retriever.retrieve("Picasso famous paintings")


```


```

# print(retrieval_results)



from llama_index.core.schema import ImageNode




from llama_index.core.response.notebook_utils import (




display_source_node,




display_image_uris,







image_results = []




MAX_RES=5




cnt =0




forin retrieval_results:




ifisinstance(r.node, ImageNode):




image_results.append(r.node.metadata["file_path"])




else:




if cnt MAX_RES:




display_source_node(r)




cnt +=1





display_image_uris(image_results, [3, 3], top_k=2)


```

**Node ID:** 13adcbba-fe8b-4d51-9139-fb1c55ffc6be**Similarity:** 0.774399292477267**Text:** == Artistic legacy == Picasso’s influence was and remains immense and widely acknowledged by his …
**Node ID:** 4100593e-6b6a-4b5f-8384-98d1c2468204**Similarity:** 0.7695965506408678**Text:** === Later works to final years: 1949–1973 === Picasso was one of 250 sculptors who exhibited in t…
**Node ID:** aeed9d43-f9c5-42a9-a7b9-1a3c005e3745**Similarity:** 0.7693110304140338**Text:** Pablo Ruiz Picasso (25 October 1881 – 8 April 1973) was a Spanish painter, sculptor, printmaker, …
**Node ID:** 5a6613b6-b599-4e40-92f2-231e10ed54f6**Similarity:** 0.7656537748231977**Text:** === The Basel vote === In the 1940s, a Swiss insurance company based in Basel had bought two pain…
**Node ID:** cc17454c-030d-4f86-a12e-342d0582f4d3**Similarity:** 0.7639671751819532**Text:** == Style and technique ==
Picasso was exceptionally prolific throughout his long lifetime. At hi…
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


