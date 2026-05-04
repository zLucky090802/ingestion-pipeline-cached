# Azurecosmosnosql
##  AzureCosmosNoSqlChatStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosnosql/#llama_index.storage.chat_store.azurecosmosnosql.AzureCosmosNoSqlChatStore "Permanent link")
Bases: 
Creates an Azure Cosmos DB NoSql Chat Store.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosnosql/llama_index/storage/chat_store/azurecosmosnosql/base.py`  
| 
```
 30
 31
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
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
```
 | 
```
classAzureCosmosNoSqlChatStore(BaseChatStore):
"""Creates an Azure Cosmos DB NoSql Chat Store."""

    _cosmos_client = CosmosClient
    _database = DatabaseProxy
    _container = ContainerProxy

    def__init__(
        self,
        cosmos_client: CosmosClient,
        chat_db_name: str = DEFAULT_CHAT_DATABASE,
        chat_container_name: str = DEFAULT_CHAT_CONTAINER,
        cosmos_container_properties: Dict[str, Any] = None,
        cosmos_database_properties: Dict[str, Any] = None,
        **kwargs,
    ):
        super().__init__(
            cosmos_client=cosmos_client,
            chat_db_name=chat_db_name,
            chat_container_name=chat_container_name,
            cosmos_container_properties=cosmos_container_properties,
            cosmos_database_properties=cosmos_database_properties,
        )

        self._cosmos_client = cosmos_client

        # Create the database if it already doesn't exist
        self._database = self._cosmos_client.create_database_if_not_exists(
            id=chat_db_name,
            offer_throughput=cosmos_database_properties.get("offer_throughput"),
            session_token=cosmos_database_properties.get("session_token"),
            initial_headers=cosmos_database_properties.get("initial_headers"),
            etag=cosmos_database_properties.get("etag"),
            match_condition=cosmos_database_properties.get("match_condition"),
        )

        # Create the collection if it already doesn't exist
        self._container = self._database.create_container_if_not_exists(
            id=chat_container_name,
            partition_key=cosmos_container_properties["partition_key"],
            indexing_policy=cosmos_container_properties.get("indexing_policy"),
            default_ttl=cosmos_container_properties.get("default_ttl"),
            offer_throughput=cosmos_container_properties.get("offer_throughput"),
            unique_key_policy=cosmos_container_properties.get("unique_key_policy"),
            conflict_resolution_policy=cosmos_container_properties.get(
                "conflict_resolution_policy"
            ),
            analytical_storage_ttl=cosmos_container_properties.get(
                "analytical_storage_ttl"
            ),
            computed_properties=cosmos_container_properties.get("computed_properties"),
            etag=cosmos_container_properties.get("etag"),
            match_condition=cosmos_container_properties.get("match_condition"),
            session_token=cosmos_container_properties.get("session_token"),
            initial_headers=cosmos_container_properties.get("initial_headers"),
        )

    @classmethod
    deffrom_connection_string(
        cls,
        connection_string: str,
        chat_db_name: str = DEFAULT_CHAT_DATABASE,
        chat_container_name: str = DEFAULT_CHAT_CONTAINER,
        cosmos_container_properties: Dict[str, Any] = None,
        cosmos_database_properties: Dict[str, Any] = None,
    ):
"""Creates an instance of Azure Cosmos DB NoSql Chat Store using a connection string."""
        cosmos_client = CosmosClient.from_connection_string(connection_string)

        return cls(
            cosmos_client,
            chat_db_name,
            chat_container_name,
            cosmos_container_properties,
            cosmos_database_properties,
        )

    @classmethod
    deffrom_account_and_key(
        cls,
        endpoint: str,
        key: str,
        chat_db_name: str = DEFAULT_CHAT_DATABASE,
        chat_container_name: str = DEFAULT_CHAT_CONTAINER,
        cosmos_container_properties: Dict[str, Any] = None,
        cosmos_database_properties: Dict[str, Any] = None,
    ) -> "AzureCosmosNoSqlChatStore":
"""Initializes AzureCosmosNoSqlChatStore from an endpoint url and key."""
        cosmos_client = CosmosClient(endpoint, key)
        return cls(
            cosmos_client,
            chat_db_name,
            chat_container_name,
            cosmos_container_properties,
            cosmos_database_properties,
        )

    @classmethod
    deffrom_aad_token(
        cls,
        endpoint: str,
        chat_db_name: str = DEFAULT_CHAT_DATABASE,
        chat_container_name: str = DEFAULT_CHAT_CONTAINER,
        cosmos_container_properties: Dict[str, Any] = None,
        cosmos_database_properties: Dict[str, Any] = None,
    ) -> "AzureCosmosNoSqlChatStore":
"""Creates an AzureChatStore using an Azure Active Directory token."""
        fromazure.identityimport DefaultAzureCredential

        credential = DefaultAzureCredential()
        return cls._from_clients(
            endpoint,
            credential,
            chat_db_name,
            chat_container_name,
            cosmos_container_properties,
            cosmos_database_properties,
        )

    defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Set messages for a key."""
        if not self._container:
            raise ValueError("Container not initialized")
        self._container.upsert_item(
            body={
                "id": key,
                "messages": _messages_to_dict(messages),
            }
        )

    defget_messages(self, key: str) -> List[ChatMessage]:
"""Get messages for a key."""
        response = self._container.read_item(key)
        if response is not None:
            message_history = response["messages"]
        else:
            message_history = []
        return [_dict_to_message(message) for message in message_history]

    defadd_message(self, key: str, message: ChatMessage) -> None:
"""Add a message for a key."""
        current_messages = _messages_to_dict(self.get_messages(key))
        current_messages.append(_message_to_dict(message))

        self._container.create_item(
            body={
                "id": key,
                "messages": current_messages,
            }
        )

    defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Delete messages for a key."""
        messages_to_delete = self.get_messages(key)
        self._container.delete_item(key)
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
        items = self._container.read_all_items()
        return [item["id"] for item in items]

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "AzureCosmosNoSqlChatStore"

    @classmethod
    def_from_clients(
        cls,
        endpoint: str,
        credential: Any,
        chat_db_name: str = DEFAULT_CHAT_DATABASE,
        chat_container_name: str = DEFAULT_CHAT_CONTAINER,
        cosmos_container_properties: Dict[str, Any] = None,
        cosmos_database_properties: Dict[str, Any] = None,
    ) -> "AzureCosmosNoSqlChatStore":
"""Create cosmos db service clients."""
        cosmos_client = CosmosClient(url=endpoint, credential=credential)
        return cls(
            cosmos_client,
            chat_db_name,
            chat_container_name,
            cosmos_container_properties,
            cosmos_database_properties,
        )

```
 |  
| --- | --- |  
###  from_connection_string `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosnosql/#llama_index.storage.chat_store.azurecosmosnosql.AzureCosmosNoSqlChatStore.from_connection_string "Permanent link")

```
from_connection_string(
    connection_string: ,
    chat_db_name:  = DEFAULT_CHAT_DATABASE,
    chat_container_name:  = DEFAULT_CHAT_CONTAINER,
    cosmos_container_properties: [, ] = None,
    cosmos_database_properties: [, ] = None,
)

```

Creates an instance of Azure Cosmos DB NoSql Chat Store using a connection string.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosnosql/llama_index/storage/chat_store/azurecosmosnosql/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_connection_string(
    cls,
    connection_string: str,
    chat_db_name: str = DEFAULT_CHAT_DATABASE,
    chat_container_name: str = DEFAULT_CHAT_CONTAINER,
    cosmos_container_properties: Dict[str, Any] = None,
    cosmos_database_properties: Dict[str, Any] = None,
):
"""Creates an instance of Azure Cosmos DB NoSql Chat Store using a connection string."""
    cosmos_client = CosmosClient.from_connection_string(connection_string)

    return cls(
        cosmos_client,
        chat_db_name,
        chat_container_name,
        cosmos_container_properties,
        cosmos_database_properties,
    )

```
 |  
| --- | --- |  
###  from_account_and_key `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosnosql/#llama_index.storage.chat_store.azurecosmosnosql.AzureCosmosNoSqlChatStore.from_account_and_key "Permanent link")

```
from_account_and_key(
    endpoint: ,
    key: ,
    chat_db_name:  = DEFAULT_CHAT_DATABASE,
    chat_container_name:  = DEFAULT_CHAT_CONTAINER,
    cosmos_container_properties: [, ] = None,
    cosmos_database_properties: [, ] = None,
) -> 

```

Initializes AzureCosmosNoSqlChatStore from an endpoint url and key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosnosql/llama_index/storage/chat_store/azurecosmosnosql/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_account_and_key(
    cls,
    endpoint: str,
    key: str,
    chat_db_name: str = DEFAULT_CHAT_DATABASE,
    chat_container_name: str = DEFAULT_CHAT_CONTAINER,
    cosmos_container_properties: Dict[str, Any] = None,
    cosmos_database_properties: Dict[str, Any] = None,
) -> "AzureCosmosNoSqlChatStore":
"""Initializes AzureCosmosNoSqlChatStore from an endpoint url and key."""
    cosmos_client = CosmosClient(endpoint, key)
    return cls(
        cosmos_client,
        chat_db_name,
        chat_container_name,
        cosmos_container_properties,
        cosmos_database_properties,
    )

```
 |  
| --- | --- |  
###  from_aad_token `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosnosql/#llama_index.storage.chat_store.azurecosmosnosql.AzureCosmosNoSqlChatStore.from_aad_token "Permanent link")

```
from_aad_token(
    endpoint: ,
    chat_db_name:  = DEFAULT_CHAT_DATABASE,
    chat_container_name:  = DEFAULT_CHAT_CONTAINER,
    cosmos_container_properties: [, ] = None,
    cosmos_database_properties: [, ] = None,
) -> 

```

Creates an AzureChatStore using an Azure Active Directory token.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosnosql/llama_index/storage/chat_store/azurecosmosnosql/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_aad_token(
    cls,
    endpoint: str,
    chat_db_name: str = DEFAULT_CHAT_DATABASE,
    chat_container_name: str = DEFAULT_CHAT_CONTAINER,
    cosmos_container_properties: Dict[str, Any] = None,
    cosmos_database_properties: Dict[str, Any] = None,
) -> "AzureCosmosNoSqlChatStore":
"""Creates an AzureChatStore using an Azure Active Directory token."""
    fromazure.identityimport DefaultAzureCredential

    credential = DefaultAzureCredential()
    return cls._from_clients(
        endpoint,
        credential,
        chat_db_name,
        chat_container_name,
        cosmos_container_properties,
        cosmos_database_properties,
    )

```
 |  
| --- | --- |  
###  set_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosnosql/#llama_index.storage.chat_store.azurecosmosnosql.AzureCosmosNoSqlChatStore.set_messages "Permanent link")

```
set_messages(key: , messages: []) -> None

```

Set messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosnosql/llama_index/storage/chat_store/azurecosmosnosql/base.py`  
| 
```
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
```
 | 
```
defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""Set messages for a key."""
    if not self._container:
        raise ValueError("Container not initialized")
    self._container.upsert_item(
        body={
            "id": key,
            "messages": _messages_to_dict(messages),
        }
    )

```
 |  
| --- | --- |  
###  get_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosnosql/#llama_index.storage.chat_store.azurecosmosnosql.AzureCosmosNoSqlChatStore.get_messages "Permanent link")

```
get_messages(key: ) -> []

```

Get messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosnosql/llama_index/storage/chat_store/azurecosmosnosql/base.py`  
| 
```
160
161
162
163
164
165
166
167
```
 | 
```
defget_messages(self, key: str) -> List[ChatMessage]:
"""Get messages for a key."""
    response = self._container.read_item(key)
    if response is not None:
        message_history = response["messages"]
    else:
        message_history = []
    return [_dict_to_message(message) for message in message_history]

```
 |  
| --- | --- |  
###  add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosnosql/#llama_index.storage.chat_store.azurecosmosnosql.AzureCosmosNoSqlChatStore.add_message "Permanent link")

```
add_message(key: , message: ) -> None

```

Add a message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosnosql/llama_index/storage/chat_store/azurecosmosnosql/base.py`  
| 
```
169
170
171
172
173
174
175
176
177
178
179
```
 | 
```
defadd_message(self, key: str, message: ChatMessage) -> None:
"""Add a message for a key."""
    current_messages = _messages_to_dict(self.get_messages(key))
    current_messages.append(_message_to_dict(message))

    self._container.create_item(
        body={
            "id": key,
            "messages": current_messages,
        }
    )

```
 |  
| --- | --- |  
###  delete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosnosql/#llama_index.storage.chat_store.azurecosmosnosql.AzureCosmosNoSqlChatStore.delete_messages "Permanent link")

```
delete_messages(key: ) -> Optional[[]]

```

Delete messages for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosnosql/llama_index/storage/chat_store/azurecosmosnosql/base.py`  
| 
```
181
182
183
184
185
```
 | 
```
defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""Delete messages for a key."""
    messages_to_delete = self.get_messages(key)
    self._container.delete_item(key)
    return messages_to_delete

```
 |  
| --- | --- |  
###  delete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosnosql/#llama_index.storage.chat_store.azurecosmosnosql.AzureCosmosNoSqlChatStore.delete_message "Permanent link")

```
delete_message(key: , idx: ) -> Optional[]

```

Delete specific message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosnosql/llama_index/storage/chat_store/azurecosmosnosql/base.py`  
| 
```
187
188
189
190
191
192
193
194
195
196
197
198
199
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
###  delete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosnosql/#llama_index.storage.chat_store.azurecosmosnosql.AzureCosmosNoSqlChatStore.delete_last_message "Permanent link")

```
delete_last_message(key: ) -> Optional[]

```

Delete last message for a key.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosnosql/llama_index/storage/chat_store/azurecosmosnosql/base.py`  
| 
```
201
202
203
```
 | 
```
defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""Delete last message for a key."""
    return self.delete_message(key, -1)

```
 |  
| --- | --- |  
###  get_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosnosql/#llama_index.storage.chat_store.azurecosmosnosql.AzureCosmosNoSqlChatStore.get_keys "Permanent link")

```
get_keys() -> []

```

Get all keys.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosnosql/llama_index/storage/chat_store/azurecosmosnosql/base.py`  
| 
```
205
206
207
208
```
 | 
```
defget_keys(self) -> List[str]:
"""Get all keys."""
    items = self._container.read_all_items()
    return [item["id"] for item in items]

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/azurecosmosnosql/#llama_index.storage.chat_store.azurecosmosnosql.AzureCosmosNoSqlChatStore.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-azurecosmosnosql/llama_index/storage/chat_store/azurecosmosnosql/base.py`  
| 
```
210
211
212
213
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "AzureCosmosNoSqlChatStore"

```
 |  
| --- | --- |  
options: members: - AzureCosmosNoSqlChatStore
