[Skip to content](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth-env/#_top)
LlamaAgents
llamactl Reference
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# auth env
Manage environments (distinct control plane API URLs). Environments determine which profiles are shown and where auth/project actions apply.
## Usage
[Section titled “Usage”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth-env/#usage)
Terminal window
```


llamactlauthenv [COMMAND] [options]


```

Commands:
  * `list`: List known environments and mark the current one
  * `add <API_URL> [--interactive/--no-interactive]`: Probe the server and upsert the environment
  * `switch [API_URL] [--interactive/--no-interactive]`: Select the current environment (prompts if omitted)
  * `delete [API_URL] [--interactive/--no-interactive]`: Remove an environment and its associated profiles


Notes:
  * Probing reads `requires_auth` and `min_llamactl_version` from the server version endpoint.
  * Switching environment filters profiles shown by `llamactl auth list` and used by other commands.


## Commands
[Section titled “Commands”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth-env/#commands)
### List
[Section titled “List”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth-env/#list)
Terminal window
```


llamactlauthenvlist


```

Shows a table of environments with API URL, whether auth is required, and the current marker.
### Add
[Section titled “Add”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth-env/#add)
Terminal window
```


llamactlauthenvadd<API_URL>


```

Probes the server at `<API_URL>` and stores discovered settings. Interactive mode can prompt for the URL.
### Switch
[Section titled “Switch”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth-env/#switch)
Terminal window
```


llamactlauthenvswitch [API_URL]


```

Sets the current environment. If omitted in interactive mode, you’ll be prompted to select one.
### Delete
[Section titled “Delete”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth-env/#delete)
Terminal window
```


llamactlauthenvdelete [API_URL]


```

Deletes an environment and all associated profiles. If the deleted environment was current, the current environment is reset to the default.
## See also
[Section titled “See also”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth-env/#see-also)
  * Profiles and tokens: [`llamactl auth`](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth/)
  * Getting started: [Introduction](https://developers.llamaindex.ai/python/llamaagents/llamactl/getting-started/)
  * Deployments: [`llamactl deployments`](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-deployments/)


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


