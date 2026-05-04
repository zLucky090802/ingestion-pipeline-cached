[Skip to content](https://developers.llamaindex.ai/python/examples/agent/multi_document_agents-v1/#_top)
# Multi-Document Agents (V1) 
In this guide, you learn towards setting up a multi-document agent over the LlamaIndex documentation.
This is an extension of V0 multi-document agents with the additional features:
  * Reranking during document (tool) retrieval
  * Query planning tool that the agent can use to plan


We do this with the following architecture:
  * setup a “document agent” over each Document: each doc agent can do QA/summarization within its doc
  * setup a top-level agent over this set of document agents. Do tool retrieval and then do CoT over the set of tools to answer a question.


If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-core




%pip install llama-index-agent-openai




%pip install llama-index-readers-file




%pip install llama-index-postprocessor-cohere-rerank




%pip install llama-index-llms-openai




%pip install llama-index-embeddings-openai




%pip install unstructured[html]


```


```


%load_ext autoreload




%autoreload 2


```

## Setup and Download Data
[Section titled “Setup and Download Data”](https://developers.llamaindex.ai/python/examples/agent/multi_document_agents-v1/#setup-and-download-data)
In this section, we’ll load in the LlamaIndex documentation.
**NOTE:** This command will take a while to run, it will download the entire LlamaIndex documentation. In my testing, this took about 15 minutes.

```


domain ="docs.llamaindex.ai"




docs_url ="https://docs.llamaindex.ai/en/latest/"




!wget -e robots=off --recursive --no-clobber --page-requisites --html-extension --convert-links --restrict-file-names=windows --domains {domain} --no-parent {docs_url}


```


```


from llama_index.readers.file import UnstructuredReader





reader = UnstructuredReader()


```


```


from pathlib import Path





all_files_gen = Path("./docs.llamaindex.ai/").rglob("*")




all_files = [f.resolve() forin all_files_gen]


```


```


all_html_files = [f forin all_files if f.suffix.lower() ==".html"]


```


```


len(all_html_files)


```


```


useful_files = [





forin all_html_files




if"understanding"instr(x).split(".")[-2]




or"examples"instr(x).split(".")[-2]





print(len(useful_files))


```


```


from llama_index.core import Document





# TODO: set to higher value if you want more docs to be indexed




doc_limit =100





docs = []




for idx, f inenumerate(useful_files):




if idx  doc_limit:




break




print(f"Idx {idx}/{len(useful_files)}")




loaded_docs = reader.load_data(file=f, split_documents=True)





loaded_doc = Document(




text="\n\n".join([d.get_content() forin loaded_docs]),




metadata={"path": str(f)},





print(loaded_doc.metadata["path"])




docs.append(loaded_doc)


```


```


print(len(docs))


```

Define Global LLM + Embeddings

```


import os





os.environ["OPENAI_API_KEY"] ="sk-..."


```


```


from llama_index.llms.openai import OpenAI




from llama_index.embeddings.openai import OpenAIEmbedding




from llama_index.core import Settings





llm = OpenAI(model="gpt-4o")




Settings.llm = llm




Settings.embed_model = OpenAIEmbedding(




model="text-embedding-3-small", embed_batch_size=256



```

## Building Multi-Document Agents
[Section titled “Building Multi-Document Agents”](https://developers.llamaindex.ai/python/examples/agent/multi_document_agents-v1/#building-multi-document-agents)
In this section we show you how to construct the multi-document agent. We first build a document agent for each document, and then define the top-level parent agent with an object index.
### Build Document Agent for each Document
[Section titled “Build Document Agent for each Document”](https://developers.llamaindex.ai/python/examples/agent/multi_document_agents-v1/#build-document-agent-for-each-document)
In this section we define “document agents” for each document.
We define both a vector index (for semantic search) and summary index (for summarization) for each document. The two query engines are then converted into tools that are passed to an OpenAI function calling agent.
This document agent can dynamically choose to perform semantic search or summarization within a given document.
We create a separate document agent for each city.

```


from llama_index.core.agent.workflow import FunctionAgent, ReActAgent




from llama_index.core import (




load_index_from_storage,




StorageContext,




VectorStoreIndex,





from llama_index.core import SummaryIndex




from llama_index.core.tools import QueryEngineTool




from llama_index.core.node_parser import SentenceSplitter




import os




from tqdm.notebook import tqdm




import pickle






asyncdefbuild_agent_per_doc(nodes, file_base):




vi_out_path =f"./data/llamaindex_docs/{file_base}"




summary_out_path =f"./data/llamaindex_docs/{file_base}_summary.pkl"




ifnot os.path.exists(vi_out_path):




Path("./data/llamaindex_docs/").mkdir(parents=True, exist_ok=True)




# build vector index




vector_index = VectorStoreIndex(nodes)




vector_index.storage_context.persist(persist_dir=vi_out_path)




else:




vector_index = load_index_from_storage(




StorageContext.from_defaults(persist_dir=vi_out_path),






# build summary index




summary_index = SummaryIndex(nodes)





# define query engines




vector_query_engine = vector_index.as_query_engine(llm=llm)




summary_query_engine = summary_index.as_query_engine(




response_mode="tree_summarize", llm=llm






# extract a summary




ifnot os.path.exists(summary_out_path):




Path(summary_out_path).parent.mkdir(parents=True, exist_ok=True)




summary =str(




await summary_query_engine.aquery(




"Extract a concise 1-2 line summary of this document"






pickle.dump(summary, open(summary_out_path, "wb"))




else:




summary = pickle.load(open(summary_out_path, "rb"))





# define tools




query_engine_tools = [




QueryEngineTool.from_defaults(




query_engine=vector_query_engine,




name=f"vector_tool_{file_base}",




description=f"Useful for questions related to specific facts",





QueryEngineTool.from_defaults(




query_engine=summary_query_engine,




name=f"summary_tool_{file_base}",




description=f"Useful for summarization questions",







# build agent




function_llm = OpenAI(model="gpt-4")




agent = FunctionAgent(




tools=query_engine_tools,




llm=function_llm,




system_prompt=f"""\




You are a specialized agent designed to answer queries about the `{file_base}.html` part of the LlamaIndex docs.




You must ALWAYS use at least one of the tools provided when answering a question; do NOT rely on prior knowledge.\




""",






return agent, summary






asyncdefbuild_agents(docs):




node_parser = SentenceSplitter()





# Build agents dictionary




agents_dict = {}




extra_info_dict = {}





# # this is for the baseline




# all_nodes = []





for idx, doc inenumerate(tqdm(docs)):




nodes = node_parser.get_nodes_from_documents([doc])




# all_nodes.extend(nodes)





# ID will be base + parent




file_path = Path(doc.metadata["path"])




file_base =str(file_path.parent.stem) +"_"+str(file_path.stem)




agent, summary =await build_agent_per_doc(nodes, file_base)





agents_dict[file_base] = agent




extra_info_dict[file_base] = {"summary": summary, "nodes": nodes}





return agents_dict, extra_info_dict


```


```


agents_dict, extra_info_dict =await build_agents(docs)


```

### Build Retriever-Enabled OpenAI Agent
[Section titled “Build Retriever-Enabled OpenAI Agent”](https://developers.llamaindex.ai/python/examples/agent/multi_document_agents-v1/#build-retriever-enabled-openai-agent)
We build a top-level agent that can orchestrate across the different document agents to answer any user query.
This agent will use a tool retriever to retrieve the most relevant tools for the query.
**Improvements from V0** : We make the following improvements compared to the “base” version in V0.
  * Adding in reranking: we use Cohere reranker to better filter the candidate set of documents.
  * Adding in a query planning tool: we add an explicit query planning tool that’s dynamically created based on the set of retrieved tools.



```


from typing import Callable




from llama_index.core.tools import FunctionTool






defget_agent_tool_callable(agent: FunctionAgent) -> Callable:




asyncdefquery_agent(query: str) -> str:




response =await agent.run(query)




returnstr(response)





return query_agent





# define tool for each document agent



all_tools = []




for file_base, agent in agents_dict.items():




summary = extra_info_dict[file_base]["summary"]




async_fn = get_agent_tool_callable(agent)




doc_tool = FunctionTool.from_defaults(




async_fn,




name=f"tool_{file_base}",




description=summary,





all_tools.append(doc_tool)


```


```


print(all_tools[0].metadata)


```


```

ToolMetadata(description='The document provides a series of tutorials on building agentic LLM applications using LlamaIndex, covering key steps such as building RAG pipelines, agents, and workflows, along with techniques for data ingestion, indexing, querying, and application evaluation.', name='tool_understanding_index', fn_schema=<class 'llama_index.core.tools.utils.tool_understanding_index'>, return_direct=False)

```


```

# define an "object" index and retriever over these tools



from llama_index.core import VectorStoreIndex




from llama_index.core.objects import (




ObjectIndex,




ObjectRetriever,





from llama_index.postprocessor.cohere_rerank import CohereRerank




from llama_index.core.query_engine import SubQuestionQueryEngine




from llama_index.core.schema import QueryBundle




from llama_index.llms.openai import OpenAI






llm = OpenAI(model_name="gpt-4o")





obj_index = ObjectIndex.from_objects(




all_tools,




index_cls=VectorStoreIndex,





vector_node_retriever = obj_index.as_node_retriever(




similarity_top_k=10,






# define a custom object retriever that adds in a query planning tool



classCustomObjectRetriever(ObjectRetriever):




def__init__(




self,




retriever,




object_node_mapping,




node_postprocessors=None,




llm=None,





self._retriever = retriever




self._object_node_mapping = object_node_mapping




self._llm = llm or OpenAI("gpt-4o")




self._node_postprocessors = node_postprocessors or []





defretrieve(self, query_bundle):




ifisinstance(query_bundle, str):




query_bundle = QueryBundle(query_str=query_bundle)





nodes =self._retriever.retrieve(query_bundle)




for processor inself._node_postprocessors:




nodes = processor.postprocess_nodes(




nodes, query_bundle=query_bundle





tools = [self._object_node_mapping.from_node(n.node) forin nodes]





sub_agent = FunctionAgent(




name="compare_tool",




description=f"""\




Useful for any queries that involve comparing multiple documents. ALWAYS use this tool for comparison queries - make sure to call this \



tool with the original query. Do NOT use the other tools for any queries involving multiple documents.



""",




tools=tools,




llm=self._llm,




system_prompt="""You are an expert at comparing documents. Given a query, use the tools provided to compare the documents and return a summary of the results.""",






asyncdefquery_sub_agent(query: str) -> str:




response =await sub_agent.run(query)




returnstr(response)





sub_question_tool = FunctionTool.from_defaults(




query_sub_agent,




name=sub_agent.name,




description=sub_agent.description,





return tools + [sub_question_tool]


```


```

# wrap it with ObjectRetriever to return objects



custom_obj_retriever = CustomObjectRetriever(




vector_node_retriever,




obj_index.object_node_mapping,




node_postprocessors=[CohereRerank(top_n=5, model="rerank-v3.5")],




llm=llm,



```


```


tmps = custom_obj_retriever.retrieve("hello")




# should be 5 + 1 -- 5 from reranker, 1 from subquestion



print(len(tmps))


```


```


from llama_index.core.agent.workflow import ReActAgent, FunctionAgent





top_agent = FunctionAgent(




tool_retriever=custom_obj_retriever,




system_prompt=""" \



You are an agent designed to answer queries about the documentation.



Please always use the tools provided to answer a question. Do not rely on prior knowledge.\





""",




llm=llm,





# top_agent = ReActAgent(


#     tool_retriever=custom_obj_retriever,


#     system_prompt=""" \


# You are an agent designed to answer queries about the documentation.


# Please always use the tools provided to answer a question. Do not rely on prior knowledge.\



# """,


#     llm=llm,


```

### Define Baseline Vector Store Index
[Section titled “Define Baseline Vector Store Index”](https://developers.llamaindex.ai/python/examples/agent/multi_document_agents-v1/#define-baseline-vector-store-index)
As a point of comparison, we define a “naive” RAG pipeline which dumps all docs into a single vector index collection.
We set the top_k = 4

```


all_nodes = [




n for extra_info in extra_info_dict.values() forin extra_info["nodes"]



```


```


base_index = VectorStoreIndex(all_nodes)




base_query_engine = base_index.as_query_engine(similarity_top_k=4)


```

## Running Example Queries
[Section titled “Running Example Queries”](https://developers.llamaindex.ai/python/examples/agent/multi_document_agents-v1/#running-example-queries)
Let’s run some example queries, ranging from QA / summaries over a single document to QA / summarization over multiple documents.

```


from llama_index.core.agent.workflow import (




AgentStream,




ToolCall,




ToolCallResult,






handler = top_agent.run(




"What can you build with LlamaIndex?",





asyncfor ev in handler.stream_events():




ifisinstance(ev, ToolCallResult):




print(




f"\nCalling tool {ev.tool_name} with args {ev.tool_kwargs}\n Got response: {str(ev.tool_output)[:200]}"





elifisinstance(ev, ToolCall):




print(f"\nTool call: {ev.tool_name} with args {ev.tool_kwargs}")




# Print the stream of the agent




# elif isinstance(ev, AgentStream):




#     print(ev.delta, end="", flush=True)





response =await handler


```


```

Tool call: tool_SimpleIndexDemoLlama2_index with args {'query': 'What can you build with LlamaIndex?'}



Tool call: tool_apps_index with args {'query': 'What can you build with LlamaIndex?'}



Tool call: tool_putting_it_all_together_index with args {'query': 'What can you build with LlamaIndex?'}



Tool call: tool_llamacloud_index with args {'query': 'What can you build with LlamaIndex?'}



Calling tool tool_SimpleIndexDemoLlama2_index with args {'query': 'What can you build with LlamaIndex?'}



Got response: With LlamaIndex, you can build a VectorStoreIndex. This involves setting up the necessary environment, loading documents into the index, and then querying the index for information. You need to instal




Tool call: tool_using_llms_index with args {'query': 'What can you build with LlamaIndex?'}



Calling tool tool_llamacloud_index with args {'query': 'What can you build with LlamaIndex?'}



Got response: With LlamaIndex, you can build a system that connects to your data stores, automatically indexes them, and then queries the data. This is done by integrating LlamaCloud into your project. The system a




Calling tool tool_apps_index with args {'query': 'What can you build with LlamaIndex?'}



Got response: With LlamaIndex, you can build a full-stack web application. You can integrate it into a backend server like Flask, package it into a Docker container, or use it directly in a framework such as Stream




Calling tool tool_putting_it_all_together_index with args {'query': 'What can you build with LlamaIndex?'}



Got response: With LlamaIndex, you can build a variety of applications and tools. This includes:




1. Chatbots: You can use LlamaIndex to create interactive chatbots.


2. Agents: LlamaIndex can be used to build intel



Calling tool tool_using_llms_index with args {'query': 'What can you build with LlamaIndex?'}



Got response: With LlamaIndex, you can build a variety of applications by leveraging the various Language Model (LLM) integrations it supports. These include OpenAI, Anthropic, Mistral, DeepSeek, Hugging Face, and


```


```

# print the final response string



print(str(response))


```


```

With LlamaIndex, you can build various applications and tools, including:



1. **VectorStoreIndex**: Set up and query a VectorStoreIndex by loading documents and configuring the environment as per the documentation.



2. **Full-Stack Web Applications**: Integrate LlamaIndex into backend servers like Flask, Docker containers, or frameworks like Streamlit or CopilotKit. Resources include guides for TypeScript+React, Delphic starter template, and Flask, Streamlit, CopilotKit, and Docker integration examples.



3. **Chatbots, Agents, and Unified Query Framework**: Create interactive chatbots, intelligent agents, and a unified query framework for handling different query types. LlamaIndex also supports property graphs and full-stack web applications.



4. **Data Management with LlamaCloud**: Build systems that connect to data stores, automatically index data, and efficiently query it by integrating LlamaCloud into your project.



5. **LLM Integrations**: Utilize various Language Model (LLM) integrations such as OpenAI, Anthropic, Mistral, DeepSeek, and Hugging Face. LlamaIndex provides a unified interface to access different LLMs, enabling you to select models based on their strengths and price points. You can use multi-modal LLMs for chat messages with text, images, and audio inputs, and even call tools and functions directly through API calls.



These capabilities make LlamaIndex a versatile tool for building a wide range of applications and systems.

```


```

# access the tool calls


# print(response.tool_calls)

```


```

# baseline



response = base_query_engine.query(




"What can you build with LlamaIndex?",





print(str(response))


```


```

With LlamaIndex, you can build a variety of applications and systems, including a full-stack web application, a chatbot, and a unified query framework over multiple indexes. You can also perform semantic searches, summarization queries, and queries over structured data like SQL or Pandas DataFrames. Additionally, LlamaIndex supports routing over heterogeneous data sources and compare/contrast queries. It provides tools and templates to help you integrate these capabilities into production-ready applications.

```


```


response =await top_agent.run("Compare workflows to query engines")




print(str(response))


```


```

Workflows and query engines serve different purposes in an application context:



1. Workflows:



- Workflows are designed to manage the execution flow of an application by dividing it into sections triggered by events.




- They are event-driven and step-based, allowing for the management of application complexity by breaking it into smaller, more manageable pieces.




- Workflows focus on controlling the flow of application execution through steps and events.




2. Query Engines:



- Query engines are tools used to process queries against a database or data source to retrieve specific information.




- They are primarily used for querying and retrieving data from databases.




- Query engines are focused on the retrieval, postprocessing, and response synthesis stages of querying.




In summary, workflows are more about controlling the flow of application execution, while query engines are specifically designed for querying and retrieving data from databases.

```


```


response =await top_agent.run(




"Can you compare the compact and tree_summarize response synthesizer response modes at a very high-level?"





print(str(response))


```


```

The compact response synthesizer mode aims to produce concise and condensed responses, focusing on delivering the most relevant information in a brief format. On the other hand, the tree_summarize response synthesizer mode is designed to create structured and summarized responses, organizing information in a comprehensive manner.



In summary, the compact mode provides brief and straightforward responses, while the tree_summarize mode offers more detailed and organized output for a comprehensive summary.

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


