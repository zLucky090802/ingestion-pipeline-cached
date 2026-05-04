[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/oci_genai/#_top)
LlamaIndex Framework
Integrations
Embeddings
[Oracle Cloud Infrastructure Generative AI ](https://developers.llamaindex.ai/python/framework/integrations/embeddings/oci_genai/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Oracle Cloud Infrastructure Generative AI 
Oracle Cloud Infrastructure (OCI) Generative AI is a fully managed service that provides a set of state-of-the-art, customizable large language models (LLMs) that cover a wide range of use cases, and which is available through a single API. Using the OCI Generative AI service you can access ready-to-use pretrained models, or create and host your own fine-tuned custom models based on your own data on dedicated AI clusters. Detailed documentation of the service and API is available and .
This notebook explains how to use OCI’s Genrative AI embedding models with LlamaIndex.
## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/oci_genai/#setup)
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-embeddings-oci-genai


```


```


!pip install llama-index


```

You will also need to install the OCI sdk

```


!pip install -U oci


```

## Basic Usage
[Section titled “Basic Usage”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/oci_genai/#basic-usage)

```


from llama_index.embeddings.oci_genai import OCIGenAIEmbeddings





embedding = OCIGenAIEmbeddings(




model_name="cohere.embed-english-light-v3.0",




service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",




compartment_id="MY_OCID",






e1 = embedding.get_text_embedding("This is a test document")




print(e1[-5:])





e2 = embedding.get_query_embedding("This is a test document")




print(e2[-5:])





docs = ["This is a test document", "This is another test document"]




e3 = embedding.get_text_embedding_batch(docs)




print(e3)


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


