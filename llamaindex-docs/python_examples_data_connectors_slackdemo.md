[Skip to content](https://developers.llamaindex.ai/python/examples/data_connectors/slackdemo/#_top)
# Slack Reader 
Demonstrates our Slack data connector
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index-readers-slack


```


```


!pip install llama-index


```


```


import logging




import sys





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


```


```


from llama_index.core import SummaryIndex




from llama_index.readers.slack import SlackReader




from IPython.display import Markdown, display




import os


```

Load data using Channel IDs

```


slack_token = os.getenv("SLACK_BOT_TOKEN")




channel_ids = ["<channel_id>"]




documents = SlackReader(slack_token=slack_token).load_data(




channel_ids=channel_ids



```

Load data using Channel Names/Regex Patterns

```


slack_token = os.getenv("SLACK_BOT_TOKEN")




channel_patterns = ["<channel_name>", "<regex_pattern>"]




slack_reader = SlackReader(slack_token=slack_token)




channel_ids = slack_reader.get_channel_ids(channel_patterns=channel_patterns)




documents = slack_reader.load_data(channel_ids=channel_ids)


```


```


index = SummaryIndex.from_documents(documents)


```


```

# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine()




response = query_engine.query("<query_text>")


```


```


display(Markdown(f"<b>{response}</b>"))


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


