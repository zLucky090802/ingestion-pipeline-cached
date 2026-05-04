# Azurecosmosmongovcore
##  AzureCosmosMongoVCoreChatStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosmongovcore/#llama_index.storage.chat_store.azurecosmosmongovcore.AzureCosmosMongoVCoreChatStore "Permanent link")
Bases: , 
Creates an Azure Cosmos DB NoSql Chat Store.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosmongovcore/llama_index/storage/chat_store/azurecosmosmongovcore/base.py`  
| 
```
 32
 33
 34
 35
 36
 37
 38
 39
 40
 41
 42
 43
 44
 45
 46
 47
 48
 49
 50
 51
 52
 53
 54
 55
 56
 57
 58
 59
 60
 61
 62
 63
 64
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
```
 | 
```
classAzureCosmosMongoVCoreChatStore(BaseChatStore, ABC):
"""Creates an Azure Cosmos DB NoSql Chat Store."""

    _mongo_client = MongoClient
    _database = Database
    _collection = Collection

    def__init__(
        self,
        mongo_client: MongoClient,
        uri: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        db_name: Optional[str] = None,
        collection_name: Optional[str] = None,
    ):
        super().__init__(
            mongo_client=mongo_client,
            uri=uri,
            host=host,
            port=port,
            db_name=db_name,
        )

        self._mongo_client = mongo_client
        self._uri = uri
        self._host = host
        self._port = port
        self._database = self._mongo_client[db_name]
        self._collection = self._mongo_client[db_name][collection_name]

    @classmethod
    deffrom_connection_string(
        cls,
        connection_string: str,
        db_name: Optional[str] = None,
        collection_name: Optional[str] = None,
    ):
"""Creates an instance of AzureCosmosMongoVCoreChatStore using a connection string."""
        # Parse the MongoDB URI
        parsed_uri = urllib.parse.urlparse(connection_string)
        # Extract username and password, and perform url_encoding
        username = urllib.parse.quote_plus(parsed_uri.username)
        password = urllib.parse.quote_plus(parsed_uri.password)

        encoded_conn_string = f"mongodb+srv://{username}:{password}@{parsed_uri.hostname}/?{parsed_uri.query}"
        mongo_client = MongoClient(encoded_conn_string, appname=APP_NAME)

        return cls(
            mongo_client=mongo_client,
            db_name=db_name,
            collection_name=collection_name,
        )

    @classmethod
    deffrom_host_and_port(
        cls,
        host: str,
        port: int,
        db_name: Optional[str] = None,
        collection_name: Optional[str] = None,
    ) -> "AzureCosmosMongoVCoreChatStore":
"""Initializes AzureCosmosMongoVCoreChatStore from an endpoint url and key."""
        mongo_client = MongoClient(host=host, port=port, appname=APP_NAME)

        return cls(
            mongo_client=mongo_client,
            host=host,
            port=port,
            db_name=db_name,
            collection_name=collection_name,
        )

    defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Set messages for a key."""
        self._collection.updateOne(
            {"_id": key},
            {"$set": {"messages": _messages_to_dict(messages)}},
            upsert=True,
        )

    defget_messages(self, key: str) -> List[ChatMessage]:
"""Get messages for a key."""
        response = self._collection.find_one({"_id": key})
        if response is not None:
            message_history = response["messages"]
        else:
            message_history = []
        return [_dict_to_message(message) for message in message_history]

    defadd_message(self, key: str, message: ChatMessage) -> None:
"""Add a message for a key."""
        current_messages = _messages_to_dict(self.get_messages(key))
        current_messages.append(_message_to_dict(message))

        self._collection.insert_one(
            {
                "id": key,
                "messages": current_messages,
            }
        )

    defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Delete messages for a key."""
        messages_to_delete = self.get_messages(key)
        self._collection.delete_one({"_id": key})
        return messages_to_delete

    defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
        current_messages = self.get_messages(key)
        try:
            message_to_delete = current_messages[idx]
            del current_messages[idx]
            self.set_messages(key, current_messages)
            return message_to_delete
        except IndexError:
            logger.error(
                IndexError(f"No message exists at index, {idx}, for key {key}")
            )
            return None

    defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete last message for a key."""
        return self.delete_message(key, -1)

    defget_keys(self) -> List[str]:
"""Get all keys."""
        return [doc["id"] for doc in self._collection.find({}, {"id": 1})]

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "AzureCosmosMongoVCoreChatStore"

```
 |  
| --- | --- |  
###  from_connection_string `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosmongovcore/#llama_index.storage.chat_store.azurecosmosmongovcore.AzureCosmosMongoVCoreChatStore.from_connection_string "Permanent link")

```
from_connection_string(
    connection_string: ,
    db_name: Optional[] = None,
    collection_name: Optional[] = None,
)

```

Creates an instance of AzureCosmosMongoVCoreChatStore using a connection string.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosmongovcore/llama_index/storage/chat_store/azurecosmosmongovcore/base.py`  
| 
```
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
```
 | 
```
@classmethod
deffrom_connection_string(
    cls,
    connection_string: str,
    db_name: Optional[str] = None,
    collection_name: Optional[str] = None,
):
"""Creates an instance of AzureCosmosMongoVCoreChatStore using a connection string."""
    # Parse the MongoDB URI
    parsed_uri = urllib.parse.urlparse(connection_string)
    # Extract username and password, and perform url_encoding
    username = urllib.parse.quote_plus(parsed_uri.username)
    password = urllib.parse.quote_plus(parsed_uri.password)

    encoded_conn_string = f"mongodb+srv://{username}:{password}@{parsed_uri.hostname}/?{parsed_uri.query}"
    mongo_client = MongoClient(encoded_conn_string, appname=APP_NAME)

    return cls(
        mongo_client=mongo_client,
        db_name=db_name,
        collection_name=collection_name,
    )

```
 |  
| --- | --- |  
###  from_host_and_port `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosmongovcore/#llama_index.storage.chat_store.azurecosmosmongovcore.AzureCosmosMongoVCoreChatStore.from_host_and_port "Permanent link")

```
from_host_and_port(
    host: ,
    port: ,
    db_name: Optional[] = None,
    collection_name: Optional[] = None,
) -> 

```

Initializes AzureCosmosMongoVCoreChatStore from an endpoint url and key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosmongovcore/llama_index/storage/chat_store/azurecosmosmongovcore/base.py`  
| 
```
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
```
 | 
```
@classmethod
deffrom_host_and_port(
    cls,
    host: str,
    port: int,
    db_name: Optional[str] = None,
    collection_name: Optional[str] = None,
) -> "AzureCosmosMongoVCoreChatStore":
"""Initializes AzureCosmosMongoVCoreChatStore from an endpoint url and key."""
    mongo_client = MongoClient(host=host, port=port, appname=APP_NAME)

    return cls(
        mongo_client=mongo_client,
        host=host,
        port=port,
        db_name=db_name,
        collection_name=collection_name,
    )

```
 |  
| --- | --- |  
###  set_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosmongovcore/#llama_index.storage.chat_store.azurecosmosmongovcore.AzureCosmosMongoVCoreChatStore.set_messages "Permanent link")

```
set_messages(key: , messages: []) -> None

```

Set messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosmongovcore/llama_index/storage/chat_store/azurecosmosmongovcore/base.py`  
| 
```
105
106
107
108
109
110
111
```
 | 
```
defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Set messages for a key."""
    self._collection.updateOne(
        {"_id": key},
        {"$set": {"messages": _messages_to_dict(messages)}},
        upsert=True,
    )

```
 |  
| --- | --- |  
###  get_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosmongovcore/#llama_index.storage.chat_store.azurecosmosmongovcore.AzureCosmosMongoVCoreChatStore.get_messages "Permanent link")

```
get_messages(key: ) -> []

```

Get messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosmongovcore/llama_index/storage/chat_store/azurecosmosmongovcore/base.py`  
| 
```
113
114
115
116
117
118
119
120
```
 | 
```
defget_messages(self, key: str) -> List[ChatMessage]:
"""Get messages for a key."""
    response = self._collection.find_one({"_id": key})
    if response is not None:
        message_history = response["messages"]
    else:
        message_history = []
    return [_dict_to_message(message) for message in message_history]

```
 |  
| --- | --- |  
###  add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosmongovcore/#llama_index.storage.chat_store.azurecosmosmongovcore.AzureCosmosMongoVCoreChatStore.add_message "Permanent link")

```
add_message(key: , message: ) -> None

```

Add a message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosmongovcore/llama_index/storage/chat_store/azurecosmosmongovcore/base.py`  
| 
```
122
123
124
125
126
127
128
129
130
131
132
```
 | 
```
defadd_message(self, key: str, message: ChatMessage) -> None:
"""Add a message for a key."""
    current_messages = _messages_to_dict(self.get_messages(key))
    current_messages.append(_message_to_dict(message))

    self._collection.insert_one(
        {
            "id": key,
            "messages": current_messages,
        }
    )

```
 |  
| --- | --- |  
###  delete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosmongovcore/#llama_index.storage.chat_store.azurecosmosmongovcore.AzureCosmosMongoVCoreChatStore.delete_messages "Permanent link")

```
delete_messages(key: ) -> Optional[[]]

```

Delete messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosmongovcore/llama_index/storage/chat_store/azurecosmosmongovcore/base.py`  
| 
```
134
135
136
137
138
```
 | 
```
defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Delete messages for a key."""
    messages_to_delete = self.get_messages(key)
    self._collection.delete_one({"_id": key})
    return messages_to_delete

```
 |  
| --- | --- |  
###  delete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosmongovcore/#llama_index.storage.chat_store.azurecosmosmongovcore.AzureCosmosMongoVCoreChatStore.delete_message "Permanent link")

```
delete_message(key: , idx: ) -> Optional[]

```

Delete specific message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosmongovcore/llama_index/storage/chat_store/azurecosmosmongovcore/base.py`  
| 
```
140
141
142
143
144
145
146
147
148
149
150
151
152
```
 | 
```
defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""Delete specific message for a key."""
    current_messages = self.get_messages(key)
    try:
        message_to_delete = current_messages[idx]
        del current_messages[idx]
        self.set_messages(key, current_messages)
        return message_to_delete
    except IndexError:
        logger.error(
            IndexError(f"No message exists at index, {idx}, for key {key}")
        )
        return None

```
 |  
| --- | --- |  
###  delete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosmongovcore/#llama_index.storage.chat_store.azurecosmosmongovcore.AzureCosmosMongoVCoreChatStore.delete_last_message "Permanent link")

```
delete_last_message(key: ) -> Optional[]

```

Delete last message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosmongovcore/llama_index/storage/chat_store/azurecosmosmongovcore/base.py`  
| 
```
154
155
156
```
 | 
```
defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete last message for a key."""
    return self.delete_message(key, -1)

```
 |  
| --- | --- |  
###  get_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosmongovcore/#llama_index.storage.chat_store.azurecosmosmongovcore.AzureCosmosMongoVCoreChatStore.get_keys "Permanent link")

```
get_keys() -> []

```

Get all keys.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosmongovcore/llama_index/storage/chat_store/azurecosmosmongovcore/base.py`  
| 
```
158
159
160
```
 | 
```
defget_keys(self) -> List[str]:
"""Get all keys."""
    return [doc["id"] for doc in self._collection.find({}, {"id": 1})]

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosmongovcore/#llama_index.storage.chat_store.azurecosmosmongovcore.AzureCosmosMongoVCoreChatStore.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosmongovcore/llama_index/storage/chat_store/azurecosmosmongovcore/base.py`  
| 
```
162
163
164
165
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "AzureCosmosMongoVCoreChatStore"

```
 |  
| --- | --- |  
options: members: - AzureCosmosNoSqlChatStore
