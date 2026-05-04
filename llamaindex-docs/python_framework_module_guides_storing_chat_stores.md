[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#_top)
LlamaIndex Framework
Component Guides
Storing
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Chat Stores
A chat store serves as a centralized interface to store your chat history. Chat history is unique compared to other storage formats, since the order of messages is important for maintaining an overall conversation.
Chat stores can organize sequences of chat messages by keys (like `user_ids` or other unique identifiable strings), and handle `delete`, `insert`, and `get` operations.
## SimpleChatStore
[Section titled “SimpleChatStore”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#simplechatstore)
The most basic chat store is `SimpleChatStore`, which stores messages in memory and can save to/from disk, or can be serialized and stored elsewhere.
Typically, you will instantiate a chat store and give it to a memory module. Memory modules that use chat stores will default to using `SimpleChatStore` if not provided.

```


from llama_index.core.storage.chat_store import SimpleChatStore




from llama_index.core.memory import ChatMemoryBuffer





chat_store = SimpleChatStore()





chat_memory = ChatMemoryBuffer.from_defaults(




token_limit=3000,




chat_store=chat_store,




chat_store_key="user1",



```

Once you have the memory created, you might include it in an agent or chat engine:

```


agent = FunctionAgent(tools=tools, llm=llm)




await agent.run("...", memory=memory)



# OR



chat_engine = index.as_chat_engine(memory=memory)


```

To save the chat store for later, you can either save/load from disk

```


chat_store.persist(persist_path="chat_store.json")




loaded_chat_store = SimpleChatStore.from_persist_path(




persist_path="chat_store.json"



```

Or you can convert to/from a string, saving the string somewhere else along the way

```


chat_store_string = chat_store.json()




loaded_chat_store = SimpleChatStore.parse_raw(chat_store_string)


```

## UpstashChatStore
[Section titled “UpstashChatStore”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#upstashchatstore)
Using `UpstashChatStore`, you can store your chat history remotely using Upstash Redis, which offers a serverless Redis solution, making it ideal for applications that require scalable and efficient chat storage. This chat store supports both synchronous and asynchronous operations.
### Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#installation)
Terminal window
```


pipinstallllama-index-storage-chat-store-upstash


```

### Usage
[Section titled “Usage”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#usage)

```


from llama_index.storage.chat_store.upstash import UpstashChatStore




from llama_index.core.memory import ChatMemoryBuffer





chat_store = UpstashChatStore(




redis_url="YOUR_UPSTASH_REDIS_URL",




redis_token="YOUR_UPSTASH_REDIS_TOKEN",




ttl=300# Optional: Time to live in seconds






chat_memory = ChatMemoryBuffer.from_defaults(




token_limit=3000,




chat_store=chat_store,




chat_store_key="user1",



```

UpstashChatStore supports both synchronous and asynchronous operations. Here’s an example of using async methods:

```


import asyncio




from llama_index.core.llms import ChatMessage






asyncdefmain():




# Add messages




messages = [




ChatMessage(content="Hello", role="user"),




ChatMessage(content="Hi there!", role="assistant"),





await chat_store.async_set_messages("conversation1", messages)





# Retrieve messages




retrieved_messages =await chat_store.async_get_messages("conversation1")




print(retrieved_messages)





# Delete last message




deleted_message =await chat_store.async_delete_last_message(




"conversation1"





print(f"Deleted message: {deleted_message}")





asyncio.run(main())

```

## RedisChatStore
[Section titled “RedisChatStore”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#redischatstore)
Using `RedisChatStore`, you can store your chat history remotely, without having to worry about manually persisting and loading the chat history.

```


from llama_index.storage.chat_store.redis import RedisChatStore




from llama_index.core.memory import ChatMemoryBuffer





chat_store = RedisChatStore(redis_url="redis://localhost:6379", ttl=300)





chat_memory = ChatMemoryBuffer.from_defaults(




token_limit=3000,




chat_store=chat_store,




chat_store_key="user1",



```

## AzureChatStore
[Section titled “AzureChatStore”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#azurechatstore)
Using `AzureChatStore`, you can store your chat history remotely in Azure Table Storage or CosmosDB, without having to worry about manually persisting and loading the chat history.

```

pip install llama-index


pip install llama-index-llms-azure-openai


pip install llama-index-storage-chat-store-azure

```


```


from llama_index.core.chat_engine import SimpleChatEngine




from llama_index.core.memory import ChatMemoryBuffer




from llama_index.storage.chat_store.azure import AzureChatStore





chat_store = AzureChatStore.from_account_and_key(




account_name="",




account_key="",




chat_table_name="ChatUser",






memory = ChatMemoryBuffer.from_defaults(




token_limit=3000,




chat_store=chat_store,




chat_store_key="conversation1",






chat_engine = SimpleChatEngine(




memory=memory, llm=Settings.llm, prefix_messages=[]






response = chat_engine.chat("Hello.")


```

## DynamoDBChatStore
[Section titled “DynamoDBChatStore”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#dynamodbchatstore)
Using `DynamoDBChatStore`, you can store your chat history in AWS DynamoDB.
### Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#installation-1)
Terminal window
```


pipinstallllama-index-storage-chat-store-dynamodb


```

### Usage
[Section titled “Usage”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#usage-1)
Ensure you have a DynamoDB table created with the appropriate schema. By default, here is an example:

```


import boto3




# Get the service resource.



dynamodb = boto3.resource("dynamodb")




# Create the DynamoDB table.



table = dynamodb.create_table(




TableName="EXAMPLE_TABLE",




KeySchema=[{"AttributeName": "SessionId", "KeyType": "HASH"}],




AttributeDefinitions=[




{"AttributeName": "SessionId", "AttributeType": "S"}





BillingMode="PAY_PER_REQUEST",



```

You can then use the `DynamoDBChatStore` class to persist and retrieve chat histories:

```


import os




from llama_index.core.llms import ChatMessage, MessageRole




from llama_index.storage.chat_store.dynamodb.base import DynamoDBChatStore




# Initialize DynamoDB chat store



chat_store = DynamoDBChatStore(




table_name="EXAMPLE_TABLE", profile_name=os.getenv("AWS_PROFILE")





# A chat history, which doesn't exist yet, returns an empty array.



print(chat_store.get_messages("123"))



# >>> []



# Initializing a chat history with a key of "SessionID = 123"



messages = [




ChatMessage(role=MessageRole.USER, content="Who are you?"),




ChatMessage(




role=MessageRole.ASSISTANT, content="I am your helpful AI assistant."






chat_store.set_messages(key="123", messages=messages)




print(chat_store.get_messages("123"))



# >>> [ChatMessage(role=<MessageRole.USER: 'user'>, content='Who are you?', additional_kwargs={}),


#      ChatMessage(role=<MessageRole.ASSISTANT: 'assistant'>, content='I am your helpful AI assistant.', additional_kwargs={})]]



# Appending a message to an existing chat history



message = ChatMessage(role=MessageRole.USER, content="What can you do?")




chat_store.add_message(key="123", message=message)




print(chat_store.get_messages("123"))



# >>> [ChatMessage(role=<MessageRole.USER: 'user'>, content='Who are you?', additional_kwargs={}),


#      ChatMessage(role=<MessageRole.ASSISTANT: 'assistant'>, content='I am your helpful AI assistant.', additional_kwargs={})],


#      ChatMessage(role=<MessageRole.USER: 'user'>, content='What can you do?', additional_kwargs={})]

```

## PostgresChatStore
[Section titled “PostgresChatStore”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#postgreschatstore)
Using `PostgresChatStore`, you can store your chat history remotely, without having to worry about manually persisting and loading the chat history.

```


from llama_index.storage.chat_store.postgres import PostgresChatStore




from llama_index.core.memory import ChatMemoryBuffer





chat_store = PostgresChatStore.from_uri(




uri="postgresql+asyncpg://postgres:password@127.0.0.1:5432/database",






chat_memory = ChatMemoryBuffer.from_defaults(




token_limit=3000,




chat_store=chat_store,




chat_store_key="user1",



```

## TablestoreChatStore
[Section titled “TablestoreChatStore”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#tablestorechatstore)
Using `TablestoreChatStore`, you can store your chat history remotely, without having to worry about manually persisting and loading the chat history.
#### Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#installation-2)
Terminal window
```


pipinstallllama-index-storage-chat-store-tablestore


```

#### Usage
[Section titled “Usage”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#usage-2)

```


from llama_index.storage.chat_store.tablestore import TablestoreChatStore




from llama_index.core.memory import ChatMemoryBuffer




# 1. create tablestore vector store



chat_store = TablestoreChatStore(




endpoint="<end_point>",




instance_name="<instance_name>",




access_key_id="<access_key_id>",




access_key_secret="<access_key_secret>",




# You need to create a table for the first use


chat_store.create_table_if_not_exist()




chat_memory = ChatMemoryBuffer.from_defaults(




token_limit=3000,




chat_store=chat_store,




chat_store_key="user1",



```

## Google AlloyDB ChatStore
[Section titled “Google AlloyDB ChatStore”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#google-alloydb-chatstore)
Using `AlloyDBChatStore`, you can store your chat history in AlloyDB, without having to worry about manually persisting and loading the chat history.
This tutorial demonstrates the synchronous interface. All synchronous methods have corresponding asynchronous methods.
#### Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#installation-3)
Terminal window
```


pipinstallllama-index




pipinstallllama-index-alloydb-pg




pipinstallllama-index-llms-vertex


```

#### Usage
[Section titled “Usage”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#usage-3)

```


from llama_index.core.chat_engine import SimpleChatEngine




from llama_index.core.memory import ChatMemoryBuffer




from llama_index_alloydb_pg import AlloyDBChatStore, AlloyDBEngine




from llama_index.llms.vertex import Vertex




import asyncio




# Replace with your own AlloyDB info



engine = AlloyDBEngine.from_instance(




project_id=PROJECT_ID,




region=REGION,




cluster=CLUSTER,




instance=INSTANCE,




database=DATABASE,




user=USER,




password=PASSWORD,






engine.init_chat_store_table(table_name=TABLE_NAME)





chat_store = AlloyDBChatStore.create_sync(




engine=engine,




table_name=TABLE_NAME,






memory = ChatMemoryBuffer.from_defaults(




token_limit=3000,




chat_store=chat_store,




chat_store_key="user1",






llm = Vertex(model="gemini-1.5-flash-002", project=PROJECT_ID)





chat_engine = SimpleChatEngine(memory=memory, llm=llm, prefix_messages=[])





response = chat_engine.chat("Hello.")





print(response)


```

## Google Cloud SQL for PostgreSQL ChatStore
[Section titled “Google Cloud SQL for PostgreSQL ChatStore”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#google-cloud-sql-for-postgresql-chatstore)
Using `PostgresChatStore`, you can store your chat history in Cloud SQL for Postgres, without having to worry about manually persisting and loading the chat history.
This tutorial demonstrates the synchronous interface. All synchronous methods have corresponding asynchronous methods.
#### Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#installation-4)
Terminal window
```


pipinstallllama-index




pipinstallllama-index-cloud-sql-pg




pipinstallllama-index-llms-vertex


```

#### Usage
[Section titled “Usage”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#usage-4)

```


from llama_index.core.chat_engine import SimpleChatEngine




from llama_index.core.memory import ChatMemoryBuffer




from llama_index_cloud_sql_pg import PostgresChatStore, PostgresEngine




from llama_index.llms.vertex import Vertex




import asyncio




# Replace with your own Cloud SQL info



engine = PostgresEngine.from_instance(




project_id=PROJECT_ID,




region=REGION,




instance=INSTANCE,




database=DATABASE,




user=USER,




password=PASSWORD,






engine.init_chat_store_table(table_name=TABLE_NAME)





chat_store = PostgresChatStore.create_sync(




engine=engine,




table_name=TABLE_NAME,






memory = ChatMemoryBuffer.from_defaults(




token_limit=3000,




chat_store=chat_store,




chat_store_key="user1",






llm = Vertex(model="gemini-1.5-flash-002", project=PROJECT_ID)





chat_engine = SimpleChatEngine(memory=memory, llm=llm, prefix_messages=[])





response = chat_engine.chat("Hello.")





print(response)


```

## YugabyteDBChatStore
[Section titled “YugabyteDBChatStore”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#yugabytedbchatstore)
Using `YugabyteDBChatStore`, you can store your chat history remotely, without having to worry about manually persisting and loading the chat history.
### Prerequisites
[Section titled “Prerequisites”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#prerequisites)
Before using this integration, you’ll need to have a YugabyteDB instance running. You can set up a local YugabyteDB instance by following the [YugaByteDB Quick Start Guide](https://docs.yugabyte.com/preview/quick-start/macos/).
### Installation
[Section titled “Installation”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#installation-5)
Terminal window
```


pipinstallllama-index-storage-chat-store-yugabytedb


```

### Usage
[Section titled “Usage”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#usage-5)

```


from llama_index.storage.chat_store.yugabytedb import YugabyteDBChatStore




from llama_index.core.memory import ChatMemoryBuffer





chat_store = YugabyteDBChatStore.from_uri(




uri="yugabytedb+psycopg2://yugabyte:password@127.0.0.1:5433/yugabyte?load_balance=true",






chat_memory = ChatMemoryBuffer.from_defaults(




token_limit=3000,




chat_store=chat_store,




chat_store_key="user1",



```

#### Connection String Parameters
[Section titled “Connection String Parameters”](https://developers.llamaindex.ai/python/framework/module_guides/storing/chat_stores/#connection-string-parameters)
The connection string passed to `YugabyteDBChatStore.from_uri()` supports various parameters that can be used to configure the connection to your YugabyteDB cluster. You can find a complete list of supported parameters in the [YugabyteDB psycopg2 Driver Documentation](https://docs.yugabyte.com/preview/drivers-orms/python/yugabyte-psycopg2/#step-2-set-up-the-database-connection).
The YugabyteDB specific parameters include:
  * `load_balance`: Enable/disable load balancing (default: false)
  * `topology_keys`: Specify preferred nodes for connection routing
  * `yb_servers_refresh_interval`: Interval (in seconds) to refresh the list of available servers
  * `fallback_to_topology_keys_only`: Whether to only connect to nodes specified in topology_keys
  * `failed_host_ttl_seconds`: Time (in seconds) to wait before trying to connect to failed nodes


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


