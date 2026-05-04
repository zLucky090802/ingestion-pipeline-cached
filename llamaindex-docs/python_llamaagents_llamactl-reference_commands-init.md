[Skip to content](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-init/#_top)
LlamaAgents
llamactl Reference
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# init
Create a new app from a starter template, or update an existing app to the latest template version.
## Usage
[Section titled “Usage”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-init/#usage)
Terminal window
```


llamactlinit [--template <id>] [--dir <path>] [--force]




llamactlinit--update


```

## Templates
[Section titled “Templates”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-init/#templates)
  * basic-ui: A basic starter workflow with a React Vite UI
  * extraction-review: Extraction Agent with Review UI (Llama Cloud integration; review/correct extracted results)


If omitted, you will be prompted to choose interactively.
## Options
[Section titled “Options”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-init/#options)
  * `--update`: Update the current app to the latest template version. Ignores other options.
  * `--template <id>`: Template to use (`basic-ui`, `extraction-review`).
  * `--dir <path>`: Directory to create the new app in. Defaults to the template name.
  * `--force`: Overwrite the directory if it already exists.


## What it does
[Section titled “What it does”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-init/#what-it-does)
  * Copies the selected template into the target directory using [`copier`](https://copier.readthedocs.io/en/stable/)
  * Adds assistant docs: `AGENTS.md` and symlinks `CLAUDE.md`/`GEMINI.md`
  * initializes a Git repository if `git` is available
  * Prints next steps to run locally and deploy


## Examples
[Section titled “Examples”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-init/#examples)
  * Interactive flow:


Terminal window
```


llamactlinit


```

  * Non‑interactive creation:


Terminal window
```


llamactlinit--templatebasic-ui--dirmy-app


```

  * Overwrite an existing directory:


Terminal window
```


llamactlinit--templatebasic-ui--dir./basic-ui--force


```

  * Update an existing app to the latest template:


Terminal window
```


llamactlinit--update


```

See also: [Getting Started guide](https://developers.llamaindex.ai/python/llamaagents/llamactl/getting-started/).
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


