[Skip to content](https://developers.llamaindex.ai/llamaparse/extract/#_top)
Guide
Extract
[Overview of Extract](https://developers.llamaindex.ai/llamaparse/extract/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Overview of Extract
Introduction to LlamaExtract, a tool for extracting structured data from unstructured documents, available as a web UI, Python SDK, and REST API.
## Overview
[Section titled “Overview”](https://developers.llamaindex.ai/llamaparse/extract/#overview)
LlamaExtract provides a simple API for extracting structured data from unstructured documents like PDFs, text files, and images.
LlamaExtract is available as a web UI, Python SDK and REST API.
### Is LlamaExtract right for me?
[Section titled “Is LlamaExtract right for me?”](https://developers.llamaindex.ai/llamaparse/extract/#is-llamaextract-right-for-me)
LlamaExtract is a great fit for when you need:
  * **Well-typed data for downstream tasks** : You want to extract data from documents and use it for downstream tasks like training a model, building a dashboard, entering into a database, etc. LlamaExtract guarantees that your data complies with the provided schema or provides helpful error messages when it doesn’t.
  * **Accurate data extraction** : We use the best in class LLM models to extract data from your documents.
  * **Iterative schema development** : You want to quickly iterate on your schema and get feedback on how well it works on your sample documents. Do you need to provide more examples to extract a certain field? Do you need to make a certain field optional?
  * **Support for multiple file types** : LlamaExtract supports a wide range of file types, including PDFs, text files, and images. Let us know if you need support for another file type!


## Quick Start
[Section titled “Quick Start”](https://developers.llamaindex.ai/llamaparse/extract/#quick-start)
### Using the web UI
[Section titled “Using the web UI”](https://developers.llamaindex.ai/llamaparse/extract/#using-the-web-ui)
The simplest way to try out LlamaExtract is to [use the web UI](https://developers.llamaindex.ai/llamaparse/extract/web_ui).
Just define your Extraction Configuration (schema and settings), drag and drop any supported document into LlamaParse and extract data from your documents.
### Get an API key
[Section titled “Get an API key”](https://developers.llamaindex.ai/llamaparse/extract/#get-an-api-key)
Once you’re ready to start coding, [get an API key](https://developers.llamaindex.ai/llamaparse/general/api_key) to use LlamaExtract with the Python SDK.
### Use our libraries
[Section titled “Use our libraries”](https://developers.llamaindex.ai/llamaparse/extract/#use-our-libraries)
We have a library available for Python and Typescript. This is the recommended way to use LlamaExtract for running extraction jobs at scale. Check out the [SDK quick start](https://developers.llamaindex.ai/llamaparse/extract/sdk) to get started.
### REST API
[Section titled “REST API”](https://developers.llamaindex.ai/llamaparse/extract/#rest-api)
If you are using a language other than Python, you can use the [REST API](https://developers.llamaindex.ai/llamaparse/extract/api).
### Tiers and versions
[Section titled “Tiers and versions”](https://developers.llamaindex.ai/llamaparse/extract/#tiers-and-versions)
LlamaExtract offers three primary **tiers** in the UI:
  * **Cost Effective** – best when you want lower cost and higher throughput for simpler extraction tasks.
  * **Agentic** – recommended default tier that balances quality, speed, and cost for most real‑world documents.
  * **Agentic Plus (coming soon)** – high‑fidelity tier for very complex or high‑stakes extractions.


LlamaExtract now runs on the **v2** APIs by default. If you need to use the **legacy Extract v1** experience, see [Using Extract v1](https://developers.llamaindex.ai/llamaparse/extract/#using-extract-v1) below.
When using the SDK or REST API directly, V2 decouples parse and extract tiers. Here is how V2 configurations map to V1 equivalents:  
| V2 extract `tier`  | V2 parse `tier`  | V1 equivalent (`extraction_mode`)  |  
| --- | --- | --- |  
| `cost_effective`  | `fast`  | `FAST`  |  
| `agentic`  | `agentic`  | `MULTIMODAL`  |  
| `agentic`  | `agentic_plus`  | `PREMIUM`  |  
### Using Extract v1
[Section titled “Using Extract v1”](https://developers.llamaindex.ai/llamaparse/extract/#using-extract-v1)
LlamaExtract v2 is the default and recommended experience. If you need to use the legacy **Extract v1** :
  * **Web UI** : Open the main LlamaCloud UI, go to **Settings → General** , and enable the **Extract v1** toggle for your workspace.
  * **Python SDK** : Use the `llama-cloud-services` package (shown as the “Python (legacy)” tab in our SDK examples). See the [SDK page](https://developers.llamaindex.ai/llamaparse/extract/sdk) for details.
  * **REST API** : The v1 endpoints are documented on the [REST API (v1 Legacy)](https://developers.llamaindex.ai/llamaparse/extract/v1/getting_started/api) page.


Extract v1 is legacy and may be deprecated in the future. We recommend migrating to v2 for new projects.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


