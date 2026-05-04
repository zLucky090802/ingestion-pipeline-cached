[Skip to content](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth/#_top)
LlamaAgents
llamactl Reference
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# auth
Authenticate and manage profiles for the current environment. Profiles store your control plane API URL, project, and optional API key.
## Usage
[Section titled “Usage”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth/#usage)
Terminal window
```


llamactlauth [COMMAND] [options]


```

Commands:
  * `token [--project-id ID] [--api-key KEY] [--interactive/--no-interactive]`: Create profile from API key; validates token and selects a project
  * `login`: Login via web browser (OIDC device flow) and create a profile
  * `list`: List login profiles in the current environment
  * `switch [NAME] [--interactive/--no-interactive]`: Set currently logged in user/token
  * `logout [NAME] [--interactive/--no-interactive]`: Delete a login and its local data
  * `project [PROJECT_ID] [--interactive/--no-interactive]`: Change the active project for the current profile


Notes:
  * Profiles are filtered by the current environment (`llamactl auth env switch`).
  * Non-interactive `token` requires both `--api-key` and `--project-id`.


## Commands
[Section titled “Commands”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth/#commands)
### Token
[Section titled “Token”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth/#token)
Terminal window
```


llamactlauthtoken [--project-id ID] [--api-key KEY] [--interactive/--no-interactive]


```

  * Interactive: Prompts for API key (masked), validates it by listing projects, then lets you choose a project. Creates an auto‑named profile and sets it current.
  * Non‑interactive: Requires both `--api-key` and `--project-id`.


### Login
[Section titled “Login”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth/#login)
Terminal window
```


llamactlauthlogin


```

Login via your browser using the OIDC device flow, select a project, and create a login profile set as current.
### List
[Section titled “List”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth/#list)
Terminal window
```


llamactlauthlist


```

Shows a table of profiles for the current environment with name and active project. The current profile is marked with `*`.
### Switch
[Section titled “Switch”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth/#switch)
Terminal window
```


llamactlauthswitch [NAME] [--interactive/--no-interactive]


```

Set the current profile. If `NAME` is omitted in interactive mode, you will be prompted to select one.
### Logout
[Section titled “Logout”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth/#logout)
Terminal window
```


llamactlauthlogout [NAME] [--interactive/--no-interactive]


```

Delete a profile. If the deleted profile is current, the current selection is cleared.
### Project
[Section titled “Project”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth/#project)
Terminal window
```


llamactlauthproject [PROJECT_ID] [--interactive/--no-interactive]


```

Change the active project for the current profile. In interactive mode, select from server projects. In environments that don’t require auth, you can also enter a project ID.
## See also
[Section titled “See also”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth/#see-also)
  * Environments: [`llamactl auth env`](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-auth-env/)
  * Getting started: [Introduction](https://developers.llamaindex.ai/python/llamaagents/llamactl/getting-started/)
  * Deployments: [`llamactl deployments`](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-deployments/)


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


