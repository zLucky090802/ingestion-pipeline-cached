[Skip to content](https://developers.llamaindex.ai/python/framework/integrations/embeddings/heroku/#_top)
LlamaIndex Framework
Integrations
Embeddings
[Heroku LLM Managed Inference Embedding ](https://developers.llamaindex.ai/python/framework/integrations/embeddings/heroku/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Heroku LLM Managed Inference Embedding 
The `llama-index-embeddings-heroku` package contains LlamaIndex integrations for building applications with embeddings models on Heroku’s Managed Inference platform. This integration allows you to easily connect to and use AI models deployed on Heroku’s infrastructure.
## Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/heroku/#installation)

```


%pip install llama-index-embeddings-heroku


```

## Setup
[Section titled “Setup”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/heroku/#setup)
### 1. Create a Heroku App
[Section titled “1. Create a Heroku App”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/heroku/#1-create-a-heroku-app)
First, create an app in Heroku:
Terminal window
```


herokucreate $APP_NAME


```

### 2. Create and Attach AI Models
[Section titled “2. Create and Attach AI Models”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/heroku/#2-create-and-attach-ai-models)
Create and attach a chat model to your app:
Terminal window
```


herokuai:models:create-a $APP_NAME cohere-embed-multilingual--asEMBEDDING


```

### 3. Export Configuration Variables
[Section titled “3. Export Configuration Variables”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/heroku/#3-export-configuration-variables)
Export the required configuration variables:
Terminal window
```


export EMBEDDING_KEY=$(herokuconfig:getEMBEDDING_KEY-a $APP_NAME)




export EMBEDDING_MODEL_ID=$(herokuconfig:getEMBEDDING_MODEL_ID-a $APP_NAME)




export EMBEDDING_URL=$(herokuconfig:getEMBEDDING_URL-a $APP_NAME)


```

## Usage
[Section titled “Usage”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/heroku/#usage)
### Basic Usage
[Section titled “Basic Usage”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/heroku/#basic-usage)

```

# Initialize the Heroku LLM



from llama_index.embeddings.heroku import HerokuEmbedding




# Initialize the Heroku Embedding



embedding_model = HerokuEmbedding()




# Get a single embedding



embedding = embedding_model.get_text_embedding("Hello, world!")




print(f"Embedding dimension: {len(embedding)}")




# Get embeddings for multiple texts



texts = ["Hello", "world", "from", "Heroku"]




embeddings = embedding_model.get_text_embedding_batch(texts)




print(f"Number of embeddings: {len(embeddings)}")


```

### Using Environment Variables
[Section titled “Using Environment Variables”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/heroku/#using-environment-variables)
The integration automatically reads from environment variables:

```


import os




# Set environment variables



os.environ["EMBEDDING_KEY"] ="your-embedding-key"




os.environ["EMBEDDING_URL"] ="https://us.inference.heroku.com"




os.environ["EMBEDDING_MODEL_ID"] ="claude-3-5-haiku"




# Initialize without parameters



llm = HerokuEmbedding()


```

### Using Parameters
[Section titled “Using Parameters”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/heroku/#using-parameters)
You can also pass parameters directly:

```


import os




from llama_index.embeddings.heroku import HerokuEmbedding





embedding_model = HerokuEmbedding(




model=os.getenv("EMBEDDING_MODEL_ID", "cohere-embed-multilingual"),




api_key=os.getenv("EMBEDDING_KEY", "your-embedding-key"),




base_url=os.getenv("EMBEDDING_URL", "https://us.inference.heroku.com"),




timeout=60.0,






print(embedding_model.get_text_embedding("Hello Heroku!"))


```

## Available Models
[Section titled “Available Models”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/heroku/#available-models)
For a complete list of available models, see the [Heroku Managed Inference documentation](https://devcenter.heroku.com/articles/heroku-inference#available-models).
## Error Handling
[Section titled “Error Handling”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/heroku/#error-handling)
The integration includes proper error handling for common issues:
  * Missing API key
  * Invalid inference URL
  * Missing model configuration


## Additional Information
[Section titled “Additional Information”](https://developers.llamaindex.ai/python/framework/integrations/embeddings/heroku/#additional-information)
For more information about Heroku Managed Inference, visit the [official documentation](https://devcenter.heroku.com/articles/heroku-inference).
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


