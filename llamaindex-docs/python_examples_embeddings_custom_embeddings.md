[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/custom_embeddings/#_top)
LlamaIndex Framework
Integrations
Embeddings
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Custom Embeddings 
LlamaIndex supports embeddings from OpenAI, Azure, and Langchain. But if this isn’t enough, you can also implement any embeddings model!
The example below uses Instructor Embeddings ([install/setup details here](https://huggingface.co/hkunlp/instructor-large)), and implements a custom embeddings class. Instructor embeddings work by providing text, as well as “instructions” on the domain of the text to embed. This is helpful when embedding text from a very specific and specialized topic.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


!pip install llama-index


```


```

# Install dependencies


# !pip install InstructorEmbedding torch transformers sentence-transformers

```


```


import openai




import os





os.environ["OPENAI_API_KEY"] ="YOUR_API_KEY"




openai.api_key = os.environ["OPENAI_API_KEY"]


```

## Custom Embeddings Implementation
[Section titled “Custom Embeddings Implementation”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/custom_embeddings/#custom-embeddings-implementation)

```


from typing import Any, List




from InstructorEmbedding importINSTRUCTOR





from llama_index.core.bridge.pydantic import PrivateAttr




from llama_index.core.embeddings import BaseEmbedding






classInstructorEmbeddings(BaseEmbedding):




_model: INSTRUCTOR= PrivateAttr()




_instruction: str= PrivateAttr()





def__init__(




self,




instructor_model_name: str="hkunlp/instructor-large",




instruction: str="Represent a document for semantic search:",




**kwargs: Any,




) -> None:




super().__init__(**kwargs)




self._model = INSTRUCTOR(instructor_model_name)




self._instruction = instruction





@classmethod




defclass_name(cls) -> str:




return"instructor"





asyncdef_aget_query_embedding(self, query: str) -> List[float]:




returnself._get_query_embedding(query)





asyncdef_aget_text_embedding(self, text: str) -> List[float]:




returnself._get_text_embedding(text)





def_get_query_embedding(self, query: str) -> List[float]:




embeddings =self._model.encode([[self._instruction, query]])




return embeddings[0]





def_get_text_embedding(self, text: str) -> List[float]:




embeddings =self._model.encode([[self._instruction, text]])




return embeddings[0]





def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:




embeddings =self._model.encode(




[[self._instruction, text] for text in texts]





return embeddings


```

## Usage Example
[Section titled “Usage Example”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/custom_embeddings/#usage-example)

```


from llama_index.core import SimpleDirectoryReader, VectorStoreIndex




from llama_index.core import Settings


```

#### Download Data
[Section titled “Download Data”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/custom_embeddings/#download-data)

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```

#### Load Documents
[Section titled “Load Documents”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/custom_embeddings/#load-documents)

```


documents = SimpleDirectoryReader("./data/paul_graham/").load_data()


```


```


embed_model = InstructorEmbeddings(embed_batch_size=2)





Settings.embed_model = embed_model




Settings.chunk_size =512




# if running for the first time, will download model weights first!



index = VectorStoreIndex.from_documents(documents)


```


```

load INSTRUCTOR_Transformer


max_seq_length  512

```


```


response = index.as_query_engine().query("What did the author do growing up?")




print(response)


```


```

The author wrote short stories and also worked on programming, specifically on an IBM 1401 computer in 9th grade. They used an early version of Fortran and had to type programs on punch cards. Later on, they got a microcomputer, a TRS-80, and started programming more extensively, writing simple games and a word processor. They initially planned to study philosophy in college but eventually switched to AI.

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


