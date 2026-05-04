[Skip to content](https://developers.llamaindex.ai/python/llamaagents/cloud/click-to-deploy/#_top)
LlamaAgents
Cloud
[Click-to-Deploy from LlamaCloud](https://developers.llamaindex.ai/python/llamaagents/cloud/click-to-deploy/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Click-to-Deploy from LlamaCloud
LlamaAgents allows you to deploy document workflow agents directly from the [LlamaCloud UI](https://cloud.llamaindex.ai/) with a single click. Choose a pre-built starter template, configure secrets, and deploy—no command line required.
## Get started with starter templates
[Section titled “Get started with starter templates”](https://developers.llamaindex.ai/python/llamaagents/cloud/click-to-deploy/#get-started-with-starter-templates)
From the LlamaCloud dashboard, navigate to **Agents** in your project. If you have no deployments, you’ll see a “Jumpstart your Agent” section showing available starter templates.
Each starter template is a complete, working document workflow application that demonstrates how to combine LlamaCloud’s document primitives—[Parse](https://developers.llamaindex.ai/python/cloud/llamaparse/getting_started), [Extract](https://developers.llamaindex.ai/python/cloud/llamaextract/getting_started), and [Classify](https://developers.llamaindex.ai/python/cloud/llamaclassify/getting_started)—into a multi-step pipeline.
### Available starters
[Section titled “Available starters”](https://developers.llamaindex.ai/python/llamaagents/cloud/click-to-deploy/#available-starters)  
| Template  | Description  | Key Features  |  
| --- | --- | --- |  
| **SEC Insights**  | Classify financial PDFs and extract structured insights  | Parse → Classify → Extract pipeline for SEC filings  |  
| **Invoice + Contract Matching**  | Parse invoices and match with contracts, identifying discrepancies  | Multi-document reconciliation workflow  |  
### Deploy a starter
[Section titled “Deploy a starter”](https://developers.llamaindex.ai/python/llamaagents/cloud/click-to-deploy/#deploy-a-starter)
  1. Click on a starter template card to open the deployment dialog
  2. Enter a **name** for your deployment (letters, numbers, and dashes only)
  3. If the starter requires API keys (e.g., `OPENAI_API_KEY`), enter them in the **Required secrets** section
  4. Click **Deploy**


LlamaCloud will clone the template repository, build your application, and deploy it. This typically takes 1–3 minutes. Once deployed, your agent will appear in the deployments list with its status.
### View your agent
[Section titled “View your agent”](https://developers.llamaindex.ai/python/llamaagents/cloud/click-to-deploy/#view-your-agent)
Once deployment status shows **Running** , click **Visit** to open your agent’s UI. Most starters include a web interface where you can:
  * Upload documents for processing
  * View extracted data and classifications
  * Review and correct results (for extraction-review workflows)


Many starters also include sample data files. Click **Example Data** on the deployment card to download test documents.
## Customize your deployment
[Section titled “Customize your deployment”](https://developers.llamaindex.ai/python/llamaagents/cloud/click-to-deploy/#customize-your-deployment)
Starter templates are fully customizable. To modify the workflow logic, UI, or configuration:
### Fork and edit
[Section titled “Fork and edit”](https://developers.llamaindex.ai/python/llamaagents/cloud/click-to-deploy/#fork-and-edit)
  1. Click **Customize** on the deployment card, or select **Edit** from the dropdown menu
  2. Follow the link to **fork the repository on GitHub**
  3. Make your changes in your forked repository
  4. Update the deployment’s **Repository URL** to point to your fork
  5. Click **Update** to redeploy with your changes


### What you can customize
[Section titled “What you can customize”](https://developers.llamaindex.ai/python/llamaagents/cloud/click-to-deploy/#what-you-can-customize)
Every LlamaAgents deployment is a standard Python project with:
  * **Workflows** (`src/`): LlamaIndex Workflow definitions using Parse, Extract, Classify, and other LlamaCloud services
  * **UI** (`ui/`): React frontend using `@llamaindex/ui` hooks
  * **Configuration** (`pyproject.toml`): Workflow registration, environment settings, and build configuration


For details on the project structure, see [Configuration Reference](https://developers.llamaindex.ai/python/llamaagents/llamactl/configuration-reference).
## Manage deployments
[Section titled “Manage deployments”](https://developers.llamaindex.ai/python/llamaagents/cloud/click-to-deploy/#manage-deployments)
After deploying, you can manage your agent from the LlamaCloud UI:
### Update to latest version
[Section titled “Update to latest version”](https://developers.llamaindex.ai/python/llamaagents/cloud/click-to-deploy/#update-to-latest-version)
If you’ve pushed changes to your repository:
  1. Click the **⋮** menu on the deployment card
  2. Select **Update Version**
  3. Confirm to pull and deploy the latest commit from your configured branch


### Rollback
[Section titled “Rollback”](https://developers.llamaindex.ai/python/llamaagents/cloud/click-to-deploy/#rollback)
If a deployment update causes issues:
  1. Click the **⋮** menu and select **Rollback**
  2. Choose a previous release from the history list
  3. Click **Rollback** to restore that version


### Edit settings
[Section titled “Edit settings”](https://developers.llamaindex.ai/python/llamaagents/cloud/click-to-deploy/#edit-settings)
To change the source repository or branch:
  1. Select **Edit** from the deployment menu
  2. Update the **Repository URL** or **Branch**
  3. Click **Update**


### Delete
[Section titled “Delete”](https://developers.llamaindex.ai/python/llamaagents/cloud/click-to-deploy/#delete)
To remove a deployment:
  1. Select **Delete** from the deployment menu
  2. Confirm deletion


Deleting a deployment is permanent. All associated resources and data will be removed.
## Next steps
[Section titled “Next steps”](https://developers.llamaindex.ai/python/llamaagents/cloud/click-to-deploy/#next-steps)
Ready to dive into the code? Learn how to author and configure workflows in [Serving your Workflows](https://developers.llamaindex.ai/python/llamaagents/llamactl/workflow-api).
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


