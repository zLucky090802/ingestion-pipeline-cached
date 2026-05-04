# Tablestore
##  TablestoreChatStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/tablestore/#llama_index.storage.chat_store.tablestore.TablestoreChatStore "Permanent link")
Bases: 
Tablestore Chat Store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `tablestore_client`  |  `OTSClient`  |  External tablestore(ots) client. If this parameter is set, the following endpoint/instance_name/access_key_id/access_key_secret will be ignored.  |  `None`  |  
|  `endpoint`  |  Tablestore instance endpoint.  |  `None`  |  
|  `instance_name`  |  Tablestore instance name.  |  `None`  |  
|  `access_key_id`  |  Aliyun access key id.  |  `None`  |  
|  `access_key_secret`  |  Aliyun access key secret.  |  `None`  |  
|  `table_name`  |  Tablestore table name.  |  `'llama_index_chat_store_v1'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `TablestoreChatStore`  |  A Tablestore chat store object.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-tablestore/llama_index/storage/chat_store/tablestore/base.py`  
| 
```
 27
 28
 29
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
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
```
 | 
```
classTablestoreChatStore(BaseChatStore):
"""
    Tablestore Chat Store.

    Args:
        tablestore_client (OTSClient, optional): External tablestore(ots) client.
                If this parameter is set, the following endpoint/instance_name/access_key_id/access_key_secret will be ignored.
        endpoint (str, optional): Tablestore instance endpoint.
        instance_name (str, optional): Tablestore instance name.
        access_key_id (str, optional): Aliyun access key id.
        access_key_secret (str, optional): Aliyun access key secret.
        table_name (str, optional): Tablestore table name.

    Returns:
        TablestoreChatStore: A Tablestore chat store object.

    """

    table_name: str
    _primary_key: str = "session_id"
    _history_column: str = "history"
    _tablestore_client: tablestore.OTSClient

    def__init__(
        self,
        tablestore_client: Optional[tablestore.OTSClient] = None,
        endpoint: Optional[str] = None,
        instance_name: Optional[str] = None,
        access_key_id: Optional[str] = None,
        access_key_secret: Optional[str] = None,
        table_name: str = "llama_index_chat_store_v1",
        **kwargs: Any,
    ) -> None:
        super().__init__(
            table_name=table_name,
        )
        if not tablestore_client:
            self._tablestore_client = tablestore.OTSClient(
                endpoint,
                access_key_id,
                access_key_secret,
                instance_name,
                retry_policy=tablestore.WriteRetryPolicy(),
                **kwargs,  # pass additional arguments
            )
        else:
            self._tablestore_client = tablestore_client

    defcreate_table_if_not_exist(self) -> None:
"""Create table if not exist."""
        table_list = self._tablestore_client.list_table()
        if self.table_name in table_list:
            logger.info(
                f"Tablestore chat store table[{self.table_name}] already exists"
            )
            return
        logger.info(
            f"Tablestore chat store table[{self.table_name}] does not exist, try to create the table."
        )

        table_meta = tablestore.TableMeta(
            self.table_name, [(self._primary_key, "STRING")]
        )
        reserved_throughput = tablestore.ReservedThroughput(
            tablestore.CapacityUnit(0, 0)
        )
        self._tablestore_client.create_table(
            table_meta, tablestore.TableOptions(), reserved_throughput
        )
        logger.info(
            f"Tablestore create chat store table[{self.table_name}] successfully."
        )

    defclear_store(self):
"""Delete all messages."""
        keys = self.get_keys()
        for key in keys:
            self.delete_messages(key)

    @classmethod
    defclass_name(self) -> str:
        return "TablestoreChatStore"

    defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""
        Assign all provided messages to the row with the given key.
        Any pre-existing messages for that key will be overwritten.

        Args:
            key (str): The key specifying a row.
            messages (List[ChatMessage]): The messages to assign to the key.

        Returns:
            None

        """
        primary_key = [(self._primary_key, key)]
        attribute_columns = [
            (
                self._history_column,
                json.dumps(_messages_to_dict(messages), ensure_ascii=False),
            ),
        ]
        row = tablestore.Row(primary_key, attribute_columns)
        self._tablestore_client.put_row(self.table_name, row)

    defget_messages(self, key: str) -> List[ChatMessage]:
"""
        Retrieve all messages for the given key.

        Args:
            key (str): The key specifying a row.

        Returns:
            List[ChatMessage]: The messages associated with the key.

        """
        primary_key = [(self._primary_key, key)]
        _, row, _ = self._tablestore_client.get_row(
            self.table_name, primary_key, None, None, 1
        )
        history = {}
        if row is not None:
            for col in row.attribute_columns:
                key = col[0]
                val = col[1]
                if key == self._history_column:
                    history = json.loads(val)
                    continue
        return [_dict_to_message(message) for message in history]

    defadd_message(self, key: str, message: ChatMessage) -> None:
"""
        Add a message to the end of the chat history for the given key.
        Creates a new row if the key does not exist.

        Args:
            key (str): The key specifying a row.
            message (ChatMessage): The message to add to the chat history.

        Returns:
            None

        """
        current_messages = self.get_messages(key)
        current_messages.append(message)
        self.set_messages(key, current_messages)

    defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""
        Deletes the entire chat history for the given key (i.e. the row).

        Args:
            key (str): The key specifying a row.

        Returns:
            Optional[List[ChatMessage]]: The messages that were deleted. None if the
                deletion failed.

        """
        messages_to_delete = self.get_messages(key)
        primary_key = [(self._primary_key, key)]
        self._tablestore_client.delete_row(self.table_name, primary_key, None)
        return messages_to_delete

    defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""
        Deletes the message at the given index for the given key.

        Args:
            key (str): The key specifying a row.
            idx (int): The index of the message to delete.

        Returns:
            Optional[ChatMessage]: The message that was deleted. None if the index
                did not exist.

        """
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
"""
        Deletes the last message in the chat history for the given key.

        Args:
            key (str): The key specifying a row.

        Returns:
            Optional[ChatMessage]: The message that was deleted. None if the chat history
                was empty.

        """
        return self.delete_message(key, -1)

    defget_keys(self) -> List[str]:
"""
        Retrieve all keys in the table.

        Returns:
            List[str]: The keys in the table.

        """
        keys = []
        inclusive_start_primary_key = [(self._primary_key, tablestore.INF_MIN)]
        exclusive_end_primary_key = [(self._primary_key, tablestore.INF_MAX)]
        limit = 5000
        columns_to_get = []
        (
            consumed,
            next_start_primary_key,
            row_list,
            next_token,
        ) = self._tablestore_client.get_range(
            self.table_name,
            tablestore.Direction.FORWARD,
            inclusive_start_primary_key,
            exclusive_end_primary_key,
            columns_to_get,
            limit,
            max_version=1,
        )
        if row_list:
            for row in row_list:
                keys.append(row.primary_key[0][1])
        while next_start_primary_key is not None:
            inclusive_start_primary_key = next_start_primary_key
            (
                consumed,
                next_start_primary_key,
                row_list,
                next_token,
            ) = self._tablestore_client.get_range(
                self.table_name,
                tablestore.Direction.FORWARD,
                inclusive_start_primary_key,
                exclusive_end_primary_key,
                columns_to_get,
                limit,
                max_version=1,
            )
            if row_list:
                for row in row_list:
                    keys.append(row.primary_key[0][1])

        return keys

```
 |  
| --- | --- |  
###  create_table_if_not_exist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/tablestore/#llama_index.storage.chat_store.tablestore.TablestoreChatStore.create_table_if_not_exist "Permanent link")

```
create_table_if_not_exist() -> None

```

Create table if not exist.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-tablestore/llama_index/storage/chat_store/tablestore/base.py`  
| 
```
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
```
 | 
```
defcreate_table_if_not_exist(self) -> None:
"""Create table if not exist."""
    table_list = self._tablestore_client.list_table()
    if self.table_name in table_list:
        logger.info(
            f"Tablestore chat store table[{self.table_name}] already exists"
        )
        return
    logger.info(
        f"Tablestore chat store table[{self.table_name}] does not exist, try to create the table."
    )

    table_meta = tablestore.TableMeta(
        self.table_name, [(self._primary_key, "STRING")]
    )
    reserved_throughput = tablestore.ReservedThroughput(
        tablestore.CapacityUnit(0, 0)
    )
    self._tablestore_client.create_table(
        table_meta, tablestore.TableOptions(), reserved_throughput
    )
    logger.info(
        f"Tablestore create chat store table[{self.table_name}] successfully."
    )

```
 |  
| --- | --- |  
###  clear_store [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/tablestore/#llama_index.storage.chat_store.tablestore.TablestoreChatStore.clear_store "Permanent link")

```
clear_store()

```

Delete all messages.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-tablestore/llama_index/storage/chat_store/tablestore/base.py`  
| 
```
100
101
102
103
104
```
 | 
```
defclear_store(self):
"""Delete all messages."""
    keys = self.get_keys()
    for key in keys:
        self.delete_messages(key)

```
 |  
| --- | --- |  
###  set_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/tablestore/#llama_index.storage.chat_store.tablestore.TablestoreChatStore.set_messages "Permanent link")

```
set_messages(key: , messages: []) -> None

```

Assign all provided messages to the row with the given key. Any pre-existing messages for that key will be overwritten.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key specifying a row.  |  _required_  |  
|  `messages`  |  `List[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  The messages to assign to the key.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `None`  |  None  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-tablestore/llama_index/storage/chat_store/tablestore/base.py`  
| 
```
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
```
 | 
```
defset_messages(self, key: str, messages: List[ChatMessage]) -> None:
"""
    Assign all provided messages to the row with the given key.
    Any pre-existing messages for that key will be overwritten.

    Args:
        key (str): The key specifying a row.
        messages (List[ChatMessage]): The messages to assign to the key.

    Returns:
        None

    """
    primary_key = [(self._primary_key, key)]
    attribute_columns = [
        (
            self._history_column,
            json.dumps(_messages_to_dict(messages), ensure_ascii=False),
        ),
    ]
    row = tablestore.Row(primary_key, attribute_columns)
    self._tablestore_client.put_row(self.table_name, row)

```
 |  
| --- | --- |  
###  get_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/tablestore/#llama_index.storage.chat_store.tablestore.TablestoreChatStore.get_messages "Permanent link")

```
get_messages(key: ) -> []

```

Retrieve all messages for the given key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key specifying a row.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  List[ChatMessage]: The messages associated with the key.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-tablestore/llama_index/storage/chat_store/tablestore/base.py`  
| 
```
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
```
 | 
```
defget_messages(self, key: str) -> List[ChatMessage]:
"""
    Retrieve all messages for the given key.

    Args:
        key (str): The key specifying a row.

    Returns:
        List[ChatMessage]: The messages associated with the key.

    """
    primary_key = [(self._primary_key, key)]
    _, row, _ = self._tablestore_client.get_row(
        self.table_name, primary_key, None, None, 1
    )
    history = {}
    if row is not None:
        for col in row.attribute_columns:
            key = col[0]
            val = col[1]
            if key == self._history_column:
                history = json.loads(val)
                continue
    return [_dict_to_message(message) for message in history]

```
 |  
| --- | --- |  
###  add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/tablestore/#llama_index.storage.chat_store.tablestore.TablestoreChatStore.add_message "Permanent link")

```
add_message(key: , message: ) -> None

```

Add a message to the end of the chat history for the given key. Creates a new row if the key does not exist.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key specifying a row.  |  _required_  |  
|  `message`  |   |  The message to add to the chat history.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `None`  |  None  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-tablestore/llama_index/storage/chat_store/tablestore/base.py`  
| 
```
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
```
 | 
```
defadd_message(self, key: str, message: ChatMessage) -> None:
"""
    Add a message to the end of the chat history for the given key.
    Creates a new row if the key does not exist.

    Args:
        key (str): The key specifying a row.
        message (ChatMessage): The message to add to the chat history.

    Returns:
        None

    """
    current_messages = self.get_messages(key)
    current_messages.append(message)
    self.set_messages(key, current_messages)

```
 |  
| --- | --- |  
###  delete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/tablestore/#llama_index.storage.chat_store.tablestore.TablestoreChatStore.delete_messages "Permanent link")

```
delete_messages(key: ) -> Optional[[]]

```

Deletes the entire chat history for the given key (i.e. the row).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key specifying a row.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Optional[List[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]]`  |  Optional[List[ChatMessage]]: The messages that were deleted. None if the deletion failed.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-tablestore/llama_index/storage/chat_store/tablestore/base.py`  
| 
```
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
```
 | 
```
defdelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
"""
    Deletes the entire chat history for the given key (i.e. the row).

    Args:
        key (str): The key specifying a row.

    Returns:
        Optional[List[ChatMessage]]: The messages that were deleted. None if the
            deletion failed.

    """
    messages_to_delete = self.get_messages(key)
    primary_key = [(self._primary_key, key)]
    self._tablestore_client.delete_row(self.table_name, primary_key, None)
    return messages_to_delete

```
 |  
| --- | --- |  
###  delete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/tablestore/#llama_index.storage.chat_store.tablestore.TablestoreChatStore.delete_message "Permanent link")

```
delete_message(key: , idx: ) -> Optional[]

```

Deletes the message at the given index for the given key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key specifying a row.  |  _required_  |  
|  `idx`  |  The index of the message to delete.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Optional[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  Optional[ChatMessage]: The message that was deleted. None if the index did not exist.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-tablestore/llama_index/storage/chat_store/tablestore/base.py`  
| 
```
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
```
 | 
```
defdelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
"""
    Deletes the message at the given index for the given key.

    Args:
        key (str): The key specifying a row.
        idx (int): The index of the message to delete.

    Returns:
        Optional[ChatMessage]: The message that was deleted. None if the index
            did not exist.

    """
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
###  delete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/tablestore/#llama_index.storage.chat_store.tablestore.TablestoreChatStore.delete_last_message "Permanent link")

```
delete_last_message(key: ) -> Optional[]

```

Deletes the last message in the chat history for the given key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `key`  |  The key specifying a row.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Optional[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.base.llms.types.ChatMessage\)")]`  |  Optional[ChatMessage]: The message that was deleted. None if the chat history was empty.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-tablestore/llama_index/storage/chat_store/tablestore/base.py`  
| 
```
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
```
 | 
```
defdelete_last_message(self, key: str) -> Optional[ChatMessage]:
"""
    Deletes the last message in the chat history for the given key.

    Args:
        key (str): The key specifying a row.

    Returns:
        Optional[ChatMessage]: The message that was deleted. None if the chat history
            was empty.

    """
    return self.delete_message(key, -1)

```
 |  
| --- | --- |  
###  get_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/tablestore/#llama_index.storage.chat_store.tablestore.TablestoreChatStore.get_keys "Permanent link")

```
get_keys() -> []

```

Retrieve all keys in the table.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: The keys in the table.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-tablestore/llama_index/storage/chat_store/tablestore/base.py`  
| 
```
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
```
 | 
```
defget_keys(self) -> List[str]:
"""
    Retrieve all keys in the table.

    Returns:
        List[str]: The keys in the table.

    """
    keys = []
    inclusive_start_primary_key = [(self._primary_key, tablestore.INF_MIN)]
    exclusive_end_primary_key = [(self._primary_key, tablestore.INF_MAX)]
    limit = 5000
    columns_to_get = []
    (
        consumed,
        next_start_primary_key,
        row_list,
        next_token,
    ) = self._tablestore_client.get_range(
        self.table_name,
        tablestore.Direction.FORWARD,
        inclusive_start_primary_key,
        exclusive_end_primary_key,
        columns_to_get,
        limit,
        max_version=1,
    )
    if row_list:
        for row in row_list:
            keys.append(row.primary_key[0][1])
    while next_start_primary_key is not None:
        inclusive_start_primary_key = next_start_primary_key
        (
            consumed,
            next_start_primary_key,
            row_list,
            next_token,
        ) = self._tablestore_client.get_range(
            self.table_name,
            tablestore.Direction.FORWARD,
            inclusive_start_primary_key,
            exclusive_end_primary_key,
            columns_to_get,
            limit,
            max_version=1,
        )
        if row_list:
            for row in row_list:
                keys.append(row.primary_key[0][1])

    return keys

```
 |  
| --- | --- |  
options: members: - TablestoreChatStore
