[Skip to content](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-serve/#_top)
LlamaAgents
llamactl Reference
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# serve
Serve your app locally for development and testing. Reads configuration from your project (e.g., `pyproject.toml` or `llama_agents.yaml`) and starts the Python API server, optionally proxying your UI in dev.
See also: [Deployment Config Reference](https://developers.llamaindex.ai/python/llamaagents/llamactl/configuration-reference/) and [UI build and dev integration](https://developers.llamaindex.ai/python/llamaagents/llamactl/ui-build/).
## Usage
[Section titled “Usage”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-serve/#usage)
Terminal window
```


llamactlserve [DEPLOYMENT_FILE] [options]


```

  * `DEPLOYMENT_FILE` defaults to `.` (current directory). Provide a path to a specific deployment file or directory if needed.


## Options
[Section titled “Options”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-serve/#options)
  * `--no-install`: Skip installing Python and JS dependencies
  * `--no-reload`: Disable API server auto‑reload on code changes
  * `--no-open-browser`: Do not open the browser automatically
  * `--preview`: Build the UI to static files and serve them (production‑like)
  * `--port <int>`: Port for the API server
  * `--ui-port <int>`: Port for the UI proxy in dev


## Behavior
[Section titled “Behavior”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-serve/#behavior)
  * Prepares the server environment (installs dependencies unless `--no-install`)
  * In dev mode (default), proxies your UI dev server and reloads on change
  * In preview mode, builds the UI to static files and serves them without a proxy


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


