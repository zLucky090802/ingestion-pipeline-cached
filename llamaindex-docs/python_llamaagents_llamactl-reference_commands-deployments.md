[Skip to content](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-deployments/#_top)
LlamaAgents
llamactl Reference
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# deployments
Deploy your app to the cloud and manage existing deployments. These commands operate on the project configured in your profile.
## Usage
[Section titled “Usage”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-deployments/#usage)
Terminal window
```


llamactldeployments [COMMAND] [options]


```

Commands:
  * `list`: List deployments for the configured project
  * `get [DEPLOYMENT_ID] [--non-interactive]`: Show details; opens a live monitor unless `--non-interactive`
  * `create`: Interactively create a new deployment
  * `edit [DEPLOYMENT_ID]`: Interactively edit a deployment
  * `delete [DEPLOYMENT_ID] [--confirm]`: Delete a deployment; `--confirm` skips the prompt
  * `update [DEPLOYMENT_ID]`: Pull latest code from the configured branch and redeploy


Notes:
  * If `DEPLOYMENT_ID` is omitted, you’ll be prompted to select one.
  * All commands accept global options (profile, host, etc.).


## Commands
[Section titled “Commands”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-deployments/#commands)
### List
[Section titled “List”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-deployments/#list)
Terminal window
```


llamactldeploymentslist


```

Shows a table of deployments with name, id, status, repo, deployment file, git ref, and secrets summary.
### Get
[Section titled “Get”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-deployments/#get)
Terminal window
```


llamactldeploymentsget [DEPLOYMENT_ID] [--non-interactive]


```

  * Default behavior opens a live monitor with status and streaming logs.
  * Use `--non-interactive` to print details to the console instead of opening the monitor.


### Create (interactive)
[Section titled “Create (interactive)”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-deployments/#create-interactive)
Terminal window
```


llamactldeploymentscreate


```

Starts an interactive flow to create a deployment. You can provide values like repository, branch, deployment file path, and secrets. (Flags such as `--repo-url`, `--name`, `--deployment-file-path`, `--git-ref`, `--personal-access-token` exist but creation is currently interactive.)
### Edit (interactive)
[Section titled “Edit (interactive)”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-deployments/#edit-interactive)
Terminal window
```


llamactldeploymentsedit [DEPLOYMENT_ID]


```

Opens an interactive form to update deployment settings.
### Delete
[Section titled “Delete”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-deployments/#delete)
Terminal window
```


llamactldeploymentsdelete [DEPLOYMENT_ID] [--confirm]


```

Deletes a deployment. Without `--confirm`, you’ll be asked to confirm.
### Update
[Section titled “Update”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-deployments/#update)
Terminal window
```


llamactldeploymentsupdate [DEPLOYMENT_ID]


```

Refreshes the deployment to the latest commit on the configured branch and shows the resulting Git SHA change.
## See also
[Section titled “See also”](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-deployments/#see-also)
  * Getting started: [Introduction](https://developers.llamaindex.ai/python/llamaagents/llamactl/getting-started/)
  * Configure names, env, and UI: [Deployment Config Reference](https://developers.llamaindex.ai/python/llamaagents/llamactl/configuration-reference/)
  * Local dev server: [`llamactl serve`](https://developers.llamaindex.ai/python/llamaagents/llamactl-reference/commands-serve/)


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


