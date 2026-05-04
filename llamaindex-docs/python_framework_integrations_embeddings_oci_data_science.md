[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/oci_data_science/#_top)
LlamaIndex Framework
Integrations
Embeddings
[Oracle Cloud Infrastructure (OCI) Data Science Service ](https://developers.llamaindex.ai/python/framework/integrations/embeddings/oci_data_science/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Oracle Cloud Infrastructure (OCI) Data Science Service 
Oracle Cloud Infrastructure (OCI) [Data Science](https://www.oracle.com/artificial-intelligence/data-science) is a fully managed, serverless platform for data science teams to build, train, and manage machine learning models in Oracle Cloud Infrastructure.
It offers [AI Quick Actions](https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions.htm), which can be used to deploy embedding models in OCI Data Science. AI Quick Actions target users who want to quickly leverage the capabilities of AI. They aim to expand the reach of foundation models to a broader set of users by providing a streamlined, code-free, and efficient environment for working with foundation models. AI Quick Actions can be accessed from the Data Science Notebook.
Detailed documentation on how to deploy embedding models in OCI Data Science using AI Quick Actions is available [here](https://github.com/oracle-samples/oci-data-science-ai-samples/blob/main/ai-quick-actions/model-deployment-tips.md) and [here](https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions-model-deploy.htm).
This notebook explains how to use OCI’s Data Science embedding models with LlamaIndex.
## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/oci_data_science/#setup)
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-embeddings-oci-data-science


```


```


!pip install llama-index


```

You will also need to install the [oracle-ads](https://accelerated-data-science.readthedocs.io/en/latest/index.html) SDK.

```


!pip install -U oracle-ads


```

## Authentication
[Section titled “Authentication”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/oci_data_science/#authentication)
The authentication methods supported for LlamaIndex are equivalent to those used with other OCI services and follow the standard SDK authentication methods, specifically API Key, session token, instance principal, and resource principal. More details can be found [here](https://accelerated-data-science.readthedocs.io/en/latest/user_guide/cli/authentication.html). Make sure to have the required [policies](https://docs.oracle.com/en-us/iaas/data-science/using/model-dep-policies-auth.htm) to access the OCI Data Science Model Deployment endpoint. The [oracle-ads](https://accelerated-data-science.readthedocs.io/en/latest/index.html) helps to simplify the authentication within OCI Data Science.
## Basic Usage
[Section titled “Basic Usage”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/oci_data_science/#basic-usage)

```


import ads




from llama_index.embeddings.oci_data_science import OCIDataScienceEmbedding





ads.set_auth(auth="security_token", profile="<replace-with-your-profile>")





embedding = OCIDataScienceEmbedding(




endpoint="https://<MD_OCID>/predict",







e1 = embeddings.get_text_embedding("This is a test document")




print(e1)





e2 = embeddings.get_text_embedding_batch(




["This is a test document", "This is another test document"]





print(e2)


```

## Async
[Section titled “Async”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/oci_data_science/#async)

```


import ads




from llama_index.embeddings.oci_data_science import OCIDataScienceEmbedding





ads.set_auth(auth="security_token", profile="<replace-with-your-profile>")





embedding = OCIDataScienceEmbedding(




endpoint="https://<MD_OCID>/predict",






e1 =await embeddings.aget_text_embedding("This is a test document")




print(e1)





e2 =await embeddings.aget_text_embedding_batch(




["This is a test document", "This is another test document"]





print(e2)


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


