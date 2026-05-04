[Skip to content](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-pkg/#_top)
LlamaAgents
llamactl Reference
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# pkg
The `pkg` command group lets you package and export your application for custom deployments. Currently it supports exporting a Dockerfile that can be built into an image with any OCI compliant image builder, such as `docker` or `podman`.
## Usage
[Section titled “Usage”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-pkg/#usage)
Terminal window
```


llamactlpkg [COMMAND] [options]


```

### Available Commands
[Section titled “Available Commands”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-pkg/#available-commands)
  * `container` – Generate a minimal, build-ready container file (e.g., `Dockerfile`) for your workflows.


## Command: `container`
[Section titled “Command: container”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-pkg/#command-container)
Terminal window
```


llamactlpkgcontainer [DEPLOYMENT_FILE] [options]


```

Generates a container build file from a given deployment file and user-specified options.
### Options
[Section titled “Options”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-pkg/#options)
  * `deployment_file` - Path to the deployment file. Defaults to the current directory (`.`)
  * `--python-version` - Python version for the base image. If not specified, it’s inferred from `.python-version` or `pyproject.toml`; defaults to **3.12** if none found.
  * `--port <int>` - Port to expose for the API server. Defaults to 4501.
  * `--dockerignore-path` - Path for the generated `.dockerignore` file. Defaults to `.dockerignore`.
  * `--overwrite` - Overwrite any existing output files. No default value.
  * `--exclude <path>` - Path(s) to exclude from the build (appended to `.dockerignore`). Can be used multiple times. No default value.
  * `--output-file` - Path and filename for the generated container build file. Defaults to `Dockerfile`.
  * `--help` - Show help for this command and exit. No default value.


### Notes
[Section titled “Notes”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-pkg/#notes)
  * The generated `.dockerignore` file automatically excludes common Python-related directories such as: 
    * Local virtual environments
    * Caches
    * Files that may contain sensitive data (e.g., `.env`)
  * The produced container file is **minimal by design**. It should work for most cases, but you may need to customize it for specific use cases.


### Examples
[Section titled “Examples”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-pkg/#examples)
**1. Create default`Dockerfile` and `.dockerignore`:**
Terminal window
```


llamactlpkgcontainer


```

**2. Generate a custom container file with specific name, Python version, and port:**
Terminal window
```


llamactlpkgcontainer--output-fileContainerfile--python-version3.14--port4502


```

**3. Exclude certain files or directories from the build:**
Terminal window
```


llamactlpkgcontainer--exclude.env.local--exclude.github/workflows/--exclude"*.pdf"


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


