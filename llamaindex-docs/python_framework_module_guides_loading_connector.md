[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/loading/connector/#_top)
LlamaIndex Framework
Component Guides
Loading
Connector
[Data Connectors (LlamaHub)](https://developers.llamaindex.ai/python/framework/module_guides/loading/connector/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Data Connectors (LlamaHub)
## Concept
[Section titled “Concept”](https://developers.llamaindex.ai/python/framework/module_guides/loading/connector/#concept)
A data connector (aka `Reader`) ingest data from different data sources and data formats into a simple `Document` representation (text and simple metadata).
## LlamaHub
[Section titled “LlamaHub”](https://developers.llamaindex.ai/python/framework/module_guides/loading/connector/#llamahub)
Our data connectors are offered through [LlamaHub](https://llamahub.ai/) 🦙. LlamaHub is an open-source repository containing data loaders that you can easily plug and play into any LlamaIndex application.
## Usage Pattern
[Section titled “Usage Pattern”](https://developers.llamaindex.ai/python/framework/module_guides/loading/connector/#usage-pattern)
Get started with:

```


from llama_index.core import download_loader





from llama_index.readers.google import GoogleDocsReader





loader = GoogleDocsReader()




documents = loader.load_data(document_ids=[...])


```

See the full [usage pattern guide](https://developers.llamaindex.ai/python/framework/module_guides/loading/connector/usage_pattern) for more details.
## Modules
[Section titled “Modules”](https://developers.llamaindex.ai/python/framework/module_guides/loading/connector/#modules)
Some sample data connectors:
  * local file directory (`SimpleDirectoryReader`). Can support parsing a wide range of file types: `.pdf`, `.jpg`, `.png`, `.docx`, etc.
  * [Notion](https://developers.notion.com/) (`NotionPageReader`)
  * [Google Docs](https://developers.google.com/docs/api) (`GoogleDocsReader`)
  * [Slack](https://api.slack.com/) (`SlackReader`)
  * [Discord](https://discord.com/developers/docs/intro) (`DiscordReader`)
  * [Apify Actors](https://llamahub.ai/l/readers/llama-index-readers-apify) (`ApifyActor`). Can crawl the web, scrape webpages, extract text content, download files including `.pdf`, `.jpg`, `.png`, `.docx`, etc.


See the [modules guide](https://developers.llamaindex.ai/python/framework/module_guides/loading/connector/modules) for more details.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


