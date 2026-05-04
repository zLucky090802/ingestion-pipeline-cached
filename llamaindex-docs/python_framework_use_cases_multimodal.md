[Skip to content](https://developers.llamaindex.ai/python/framework/use_cases/multimodal/#_top)
LlamaIndex Framework
Use Cases
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Multi-modal
LlamaIndex offers capabilities to not only build language-based applications but also **multi-modal** applications - combining language and images.
## Types of Multi-modal Use Cases
[Section titled “Types of Multi-modal Use Cases”](https://developers.llamaindex.ai/python/framework/use_cases/multimodal/#types-of-multi-modal-use-cases)
This space is actively being explored right now, but some fascinating use cases are popping up.
### RAG (Retrieval Augmented Generation)
[Section titled “RAG (Retrieval Augmented Generation)”](https://developers.llamaindex.ai/python/framework/use_cases/multimodal/#rag-retrieval-augmented-generation)
All the core RAG concepts: indexing, retrieval, and synthesis, can be extended into the image setting.
  * The input could be text or image.
  * The stored knowledge base can consist of text or images.
  * The inputs to response generation can be text or image.
  * The final response can be text or image.


Check out our guides below:
  * [Multi-modal retrieval with CLIP](https://developers.llamaindex.ai/python/examples/multi_modal/multi_modal_retrieval)
  * [Image to Image Retrieval](https://developers.llamaindex.ai/python/examples/multi_modal/image_to_image_retrieval)
  * [Structured Image Retrieval](https://developers.llamaindex.ai/python/examples/multi_modal/structured_image_retrieval)
  * [Chroma Multi-Modal](https://developers.llamaindex.ai/python/examples/multi_modal/chromamultimodaldemo)
  * [Gemini Multi-Modal](https://developers.llamaindex.ai/python/examples/multi_modal/gemini)


### Structured Outputs
[Section titled “Structured Outputs”](https://developers.llamaindex.ai/python/framework/use_cases/multimodal/#structured-outputs)
You can generate a `structured` output with the new OpenAI GPT4V via LlamaIndex. The user just needs to specify a Pydantic object to define the structure of the output.
Check out the guide below:
  * [Multi-Modal Pydantic Program](https://developers.llamaindex.ai/python/examples/multi_modal/multi_modal_pydantic)


### Retrieval-Augmented Image Captioning
[Section titled “Retrieval-Augmented Image Captioning”](https://developers.llamaindex.ai/python/framework/use_cases/multimodal/#retrieval-augmented-image-captioning)
Oftentimes understanding an image requires looking up information from a knowledge base. A flow here is retrieval-augmented image captioning - first caption the image with a multi-modal model, then refine the caption by retrieving it from a text corpus.
Check out our guides below:


### Agents
[Section titled “Agents”](https://developers.llamaindex.ai/python/framework/use_cases/multimodal/#agents)
Here are some initial works demonstrating agentic capabilities with GPT-4V.
  * [GPT-4V Experiments](https://developers.llamaindex.ai/python/examples/multi_modal/gpt4v_experiments_cot)


## Evaluations and Comparisons
[Section titled “Evaluations and Comparisons”](https://developers.llamaindex.ai/python/framework/use_cases/multimodal/#evaluations-and-comparisons)
These sections show comparisons between different multi-modal models for different use cases.
### LLaVa-13, Fuyu-8B, and MiniGPT-4 Multi-Modal LLM Models Comparison for Image Reasoning
[Section titled “LLaVa-13, Fuyu-8B, and MiniGPT-4 Multi-Modal LLM Models Comparison for Image Reasoning”](https://developers.llamaindex.ai/python/framework/use_cases/multimodal/#llava-13-fuyu-8b-and-minigpt-4-multi-modal-llm-models-comparison-for-image-reasoning)
These notebooks show how to use different Multi-Modal LLM models for image understanding/reasoning. The various model inferences are supported by Replicate or OpenAI GPT4-V API. We compared several popular Multi-Modal LLMs:
  * GPT4-V (OpenAI API)
  * LLava-13B (Replicate)
  * Fuyu-8B (Replicate)
  * MiniGPT-4 (Replicate)
  * CogVLM (Replicate)


Check out our guides below:
  * [Replicate Multi-Modal](https://developers.llamaindex.ai/python/examples/multi_modal/replicate_multi_modal)


### Simple Evaluation of Multi-Modal RAG
[Section titled “Simple Evaluation of Multi-Modal RAG”](https://developers.llamaindex.ai/python/framework/use_cases/multimodal/#simple-evaluation-of-multi-modal-rag)
In this notebook guide, we’ll demonstrate how to evaluate a Multi-Modal RAG system. As in the text-only case, we will consider the evaluation of Retrievers and Generators separately. As we alluded to in our blog on the topic of Evaluating Multi-Modal RAGs, our approach here involves the application of adapted versions of the usual techniques for evaluating both Retriever and Generator (used for the text-only case). These adapted versions are part of the llama-index library (i.e., evaluation module), and this notebook will walk you through how you can apply them to your evaluation use cases.
  * [Multi-Modal RAG Evaluation](https://developers.llamaindex.ai/python/examples/evaluation/multi_modal/multi_modal_rag_evaluation)


## Model Guides
[Section titled “Model Guides”](https://developers.llamaindex.ai/python/framework/use_cases/multimodal/#model-guides)
Here are notebook guides showing you how to interact with different multimodal model providers.
  * [OpenAI Multi-Modal](https://developers.llamaindex.ai/python/examples/multi_modal/openai_multi_modal)
  * [Replicate Multi-Modal](https://developers.llamaindex.ai/python/examples/multi_modal/replicate_multi_modal)


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


