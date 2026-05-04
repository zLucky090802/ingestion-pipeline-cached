[Skip to content](https://developers.llamaindex.ai/python/framework/use_cases/q_and_a/#_top)
LlamaIndex Framework
Use Cases
[Question-Answering (RAG)](https://developers.llamaindex.ai/python/framework/use_cases/q_and_a/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Question-Answering (RAG)
One of the most common use-cases for LLMs is to answer questions over a set of data. This data is oftentimes in the form of unstructured documents (e.g. PDFs, HTML), but can also be semi-structured or structured.
The predominant framework for enabling QA with LLMs is Retrieval Augmented Generation (RAG). LlamaIndex offers simple-to-advanced RAG techniques to tackle simple-to-advanced questions over different volumes and types of data. You can choose to use either our prebuilt RAG abstractions (e.g. [query engines](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine)) or build custom RAG [workflows](https://developers.llamaindex.ai/python/framework/module_guides/workflow)(example [guide](https://developers.llamaindex.ai/python/examples/workflow/rag)).
## RAG over Unstructured Documents
[Section titled “RAG over Unstructured Documents”](https://developers.llamaindex.ai/python/framework/use_cases/q_and_a/#rag-over-unstructured-documents)
LlamaIndex can pull in unstructured text, PDFs, Notion and Slack documents and more and index the data within them.
The simplest queries involve either semantic search or summarization.
  * **Semantic search** : A query about specific information in a document that matches the query terms and/or semantic intent. This is typically executed with simple vector retrieval (top-k). [Example of semantic search](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/q_and_a#semantic-search)
  * **Summarization** : condensing a large amount of data into a short summary relevant to your current question. [Example of summarization](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/q_and_a#summarization)


## QA over Structured Data
[Section titled “QA over Structured Data”](https://developers.llamaindex.ai/python/framework/use_cases/q_and_a/#qa-over-structured-data)
If your data already exists in a SQL database, CSV file, or other structured format, LlamaIndex can query the data in these sources. This includes **text-to-SQL** (natural language to SQL operations) and also **text-to-Pandas** (natural language to Pandas operations).
  * [Text-to-Pandas Guide](https://developers.llamaindex.ai/python/examples/query_engine/pandas_query_engine)


## Advanced QA Topics
[Section titled “Advanced QA Topics”](https://developers.llamaindex.ai/python/framework/use_cases/q_and_a/#advanced-qa-topics)
As you scale to more complex questions / more data, there are many techniques in LlamaIndex to help you with better query understanding, retrieval, and integration of data sources.
  * **Querying Complex Documents** : Oftentimes your document representation is complex - your PDF may have text, tables, charts, images, headers/footers, and more. LlamaIndex provides advanced indexing/retrieval integrated with LlamaParse, our proprietary document parser. [Full cookbooks here](https://github.com/run-llama/llama_parse/tree/main/examples).
  * **Combine multiple sources** : is some of your data in Slack, some in PDFs, some in unstructured text? LlamaIndex can combine queries across an arbitrary number of sources and combine them. 
    * [Example of combining multiple sources](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/q_and_a#multi-document-queries)
  * **Route across multiple sources** : given multiple data sources, your application can first pick the best source and then “route” the question to that source. 
    * [Example of routing across multiple sources](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/q_and_a#routing-over-heterogeneous-data)
  * **Multi-document queries** : some questions have partial answers in multiple data sources which need to be questioned separately before they can be combined 
    * [Example of multi-document queries](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/q_and_a#multi-document-queries)
    * [Building a multi-document agent over the LlamaIndex docs](https://developers.llamaindex.ai/python/examples/agent/multi_document_agents-v1) - [Text to SQL](https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/sqlindexdemo)


## Resources
[Section titled “Resources”](https://developers.llamaindex.ai/python/framework/use_cases/q_and_a/#resources)
LlamaIndex has a lot of resources around QA / RAG. Here are some core resource guides to refer to.
**I’m a RAG beginner and want to learn the basics** : Take a look at our [“Learn” series of guides](https://developers.llamaindex.ai/python/framework/understanding).
**I’ve built RAG, and now I want to optimize it** : Take a look at our [“Advanced Topics” Guides](https://developers.llamaindex.ai/python/framework/optimizing/production_rag).
**I’m more advanced and want to build a custom RAG workflow** : Use LlamaIndex [workflows](https://developers.llamaindex.ai/python/framework/module_guides/workflow) to compose advanced, agentic RAG pipelines, like this [Corrective RAG](https://developers.llamaindex.ai/python/examples/workflow/corrective_rag_pack) workflow.
**I want to learn all about a particular module** : Here are the core module guides to help build simple-to-advanced QA/RAG systems:


## Further examples
[Section titled “Further examples”](https://developers.llamaindex.ai/python/framework/use_cases/q_and_a/#further-examples)
For further examples of Q&A use cases, see our [Q&A section in Putting it All Together](https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/q_and_a).
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


