[Skip to content](https://developers.llamaindex.ai/python/framework/getting_started/installation/#_top)
LlamaIndex Framework
Getting Started
[Installation and Setup](https://developers.llamaindex.ai/python/framework/getting_started/installation/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Installation and Setup
The LlamaIndex ecosystem is structured using a collection of namespaced python packages.
What this means for users is that `pip install llama-index` comes with a core starter bundle of packages, and additional integrations can be installed as needed.
A complete list of packages and available integrations is available on [LlamaHub](https://llamahub.ai/).
## Quickstart Installation from Pip
[Section titled “Quickstart Installation from Pip”](https://developers.llamaindex.ai/python/framework/getting_started/installation/#quickstart-installation-from-pip)
To get started quickly, you can install with:
Terminal window
```


pipinstallllama-index


```

This is a starter bundle of packages, containing
  * `llama-index-core`
  * `llama-index-llms-openai`
  * `llama-index-embeddings-openai`
  * `llama-index-readers-file`


**NOTE:** `llama-index-core` comes pre-bundled with NLTK and tiktoken files to avoid downloads and network calls at runtime.
### Important: OpenAI Environment Setup
[Section titled “Important: OpenAI Environment Setup”](https://developers.llamaindex.ai/python/framework/getting_started/installation/#important-openai-environment-setup)
By default, we use the OpenAI `gpt-3.5-turbo` model for text generation and `text-embedding-ada-002` for retrieval and embeddings. In order to use this, you must have an OPENAI_API_KEY set up as an environment variable. You can obtain an API key by logging into your OpenAI account and [creating a new API key](https://platform.openai.com/account/api-keys).
[Check out our OpenAI Starter Example](https://developers.llamaindex.ai/python/framework/getting_started/starter_example)
## Custom Installation from Pip
[Section titled “Custom Installation from Pip”](https://developers.llamaindex.ai/python/framework/getting_started/installation/#custom-installation-from-pip)
If you aren’t using OpenAI, or want a more selective installation, you can install individual packages as needed.
For example, for a local setup with Ollama and HuggingFace embeddings, the installation might look like:
Terminal window
```


pipinstallllama-index-corellama-index-readers-filellama-index-llms-ollamallama-index-embeddings-huggingface


```

[Check out our Starter Example with Local Models](https://developers.llamaindex.ai/python/framework/getting_started/starter_example_local)
A full guide to using and configuring LLMs is available [here](https://developers.llamaindex.ai/python/framework/module_guides/models/llms).
A full guide to using and configuring embedding models is available [here](https://developers.llamaindex.ai/python/framework/module_guides/models/embeddings).
## Installation from Source
[Section titled “Installation from Source”](https://developers.llamaindex.ai/python/framework/getting_started/installation/#installation-from-source)
Git clone this repository: `git clone https://github.com/run-llama/llama_index.git`. Then do the following:
  * [Install poetry](https://python-poetry.org/docs/#installation) - this will help you manage package dependencies
  * If you need to run shell commands using Poetry but the shell plugin is not installed, add the plugin by running: 

```

poetry self add poetry-plugin-shell

```

  * `poetry shell` - this command creates a virtual environment, which keeps installed packages contained to this project
  * `pip install -e llama-index-core` - this will install the core package
  * (Optional) `poetry install --with dev,docs` - this will install all dependencies needed for most local development


From there, you can install integrations as needed with `pip`, For example:
Terminal window
```


pipinstall-ellama-index-integrations/readers/llama-index-readers-file




pipinstall-ellama-index-integrations/llms/llama-index-llms-ollama


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


