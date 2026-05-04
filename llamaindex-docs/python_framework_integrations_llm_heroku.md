[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/llm/heroku/#_top)
LlamaIndex Framework
Integrations
[Heroku LLM Managed Inference ](https://developers.llamaindex.ai/python/framework/integrations/llm/heroku/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Heroku LLM Managed Inference 
The `llama-index-llms-heroku` package contains LlamaIndex integrations for building applications with models on Heroku’s Managed Inference platform. This integration allows you to easily connect to and use AI models deployed on Heroku’s infrastructure.
## Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/framework/integrations/llm/heroku/#installation)

```


%pip install llama-index-llms-heroku


```

## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/framework/integrations/llm/heroku/#setup)
### 1. Create a Heroku App
[Section titled “1. Create a Heroku App”](https://developers.llamaindex.ai/python/framework/integrations/llm/heroku/#1-create-a-heroku-app)
First, create an app in Heroku:
Terminal window
```


herokucreate $APP_NAME


```

### 2. Create and Attach AI Models
[Section titled “2. Create and Attach AI Models”](https://developers.llamaindex.ai/python/framework/integrations/llm/heroku/#2-create-and-attach-ai-models)
Create and attach a chat model to your app:
Terminal window
```


herokuai:models:create-a $APP_NAME claude-3-5-haiku


```

### 3. Export Configuration Variables
[Section titled “3. Export Configuration Variables”](https://developers.llamaindex.ai/python/framework/integrations/llm/heroku/#3-export-configuration-variables)
Export the required configuration variables:
Terminal window
```


export INFERENCE_KEY=$(herokuconfig:getINFERENCE_KEY-a $APP_NAME)




export INFERENCE_MODEL_ID=$(herokuconfig:getINFERENCE_MODEL_ID-a $APP_NAME)




export INFERENCE_URL=$(herokuconfig:getINFERENCE_URL-a $APP_NAME)


```

## Usage
[Section titled “Usage”](https://developers.llamaindex.ai/python/framework/integrations/llm/heroku/#usage)
### Basic Usage
[Section titled “Basic Usage”](https://developers.llamaindex.ai/python/framework/integrations/llm/heroku/#basic-usage)

```


from llama_index.llms.heroku import Heroku




from llama_index.core.llms import ChatMessage, MessageRole




# Initialize the Heroku LLM



llm = Heroku()




# Create chat messages



messages = [




ChatMessage(




role=MessageRole.SYSTEM, content="You are a helpful assistant."





ChatMessage(




role=MessageRole.USER,




content="What are the most popular house pets in North America?",






# Get response



response = llm.chat(messages)




print(response)


```

### Using Environment Variables
[Section titled “Using Environment Variables”](https://developers.llamaindex.ai/python/framework/integrations/llm/heroku/#using-environment-variables)
The integration automatically reads from environment variables:

```


import os




# Set environment variables



os.environ["INFERENCE_KEY"] ="your-inference-key"




os.environ["INFERENCE_URL"] ="https://us.inference.heroku.com"




os.environ["INFERENCE_MODEL_ID"] ="claude-3-5-haiku"




# Initialize without parameters



llm = Heroku()


```

### Using Parameters
[Section titled “Using Parameters”](https://developers.llamaindex.ai/python/framework/integrations/llm/heroku/#using-parameters)
You can also pass parameters directly:

```


import os





llm = Heroku(




model=os.getenv("INFERENCE_MODEL_ID", "claude-3-5-haiku"),




api_key=os.getenv("INFERENCE_KEY", "your-inference-key"),




inference_url=os.getenv(




"INFERENCE_URL", "https://us.inference.heroku.com"





max_tokens=1024,



```

## Available Models
[Section titled “Available Models”](https://developers.llamaindex.ai/python/framework/integrations/llm/heroku/#available-models)
For a complete list of available models, see the [Heroku Managed Inference documentation](https://devcenter.heroku.com/articles/heroku-inference#available-models).
## Error Handling
[Section titled “Error Handling”](https://developers.llamaindex.ai/python/framework/integrations/llm/heroku/#error-handling)
The integration includes proper error handling for common issues:
  * Missing API key
  * Invalid inference URL
  * Missing model configuration


## Additional Information
[Section titled “Additional Information”](https://developers.llamaindex.ai/python/framework/integrations/llm/heroku/#additional-information)
For more information about Heroku Managed Inference, visit the [official documentation](https://devcenter.heroku.com/articles/heroku-inference).
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


