# Dynamodb
##  DynamoDBChatStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/dynamodb/#llama_index.storage.chat_store.dynamodb.DynamoDBChatStore "Permanent link")
Bases: 
DynamoDB Chat Store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `table_name`  |  The name of the preexisting DynamoDB table.  |  _required_  |  
|  `primary_key`  |  The primary/partition key to use for the table. Defaults to "SessionId".  |  `'SessionId'`  |  
|  `profile_name`  |  The AWS profile to use. If not specified, then the default AWS profile is used.  |  `None`  |  
|  `aws_access_key_id`  |  The AWS Access Key ID to use.  |  `None`  |  
|  `aws_secret_access_key`  |  The AWS Secret Access Key to use.  |  `None`  |  
|  `aws_session_token`  |  The AWS Session Token to use.  |  `None`  |  
|  `botocore_session`  |  Use this Botocore session instead of creating a new default one.  |  `None`  |  
|  `botocore_config`  |  Custom configuration object to use instead of the default generated one.  |  `None`  |  
|  `region_name`  |  The AWS region name to use. Uses the region configured in AWS CLI if not passed.  |  `None`  |  
|  `max_retries`  |  The maximum number of API retries. Defaults to 10.  |  
|  `timeout`  |  `float`  |  The timeout for API requests in seconds. Defaults to 60.0.  |  `60.0`  |  
|  `session_kwargs`  |  `Dict[str, Any]`  |  Additional kwargs for the `boto3.Session` object.  |  `None`  |  
|  `resource_kwargs`  |  `Dict[str, Any]`  |  Additional kwargs for the `boto3.Resource` object.  |  `None`  |  
|  `ttl_seconds`  |  `Optional[int]`  |  Time-to-live in seconds for items in the table. If set, items will expire after this many seconds. Defaults to None (no expiration).  |  `None`  |  
|  `ttl_attribute`  |  The name of the attribute to use for TTL. Defaults to "TTL".  |  `'TTL'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `DynamoDBChatStore`  |  A DynamoDB chat store object.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-dynamodb/llama_index/storage/chat_store/dynamodb/base.py`  
| 
```
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
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
```
 | 
```
classDynamoDBChatStore(BaseChatStore):
"""
    DynamoDB Chat Store.

    Args:
        table_name (str): The name of the preexisting DynamoDB table.
        primary_key (str, optional): The primary/partition key to use for the table.
            Defaults to "SessionId".
        profile_name (str, optional): The AWS profile to use. If not specified, then
            the default AWS profile is used.
        aws_access_key_id (str, optional): The AWS Access Key ID to use.
        aws_secret_access_key (str, optional): The AWS Secret Access Key to use.
        aws_session_token (str, optional): The AWS Session Token to use.
        botocore_session (Any, optional): Use this Botocore session instead of creating a new default one.
        botocore_config (Any, optional): Custom configuration object to use instead of the default generated one.
        region_name (str, optional): The AWS region name to use. Uses the region configured in AWS CLI if not passed.
        max_retries (int, optional): The maximum number of API retries. Defaults to 10.
        timeout (float, optional): The timeout for API requests in seconds. Defaults to 60.0.
        session_kwargs (Dict[str, Any], optional): Additional kwargs for the `boto3.Session` object.
        resource_kwargs (Dict[str, Any], optional): Additional kwargs for the `boto3.Resource` object.
        ttl_seconds (Optional[int], optional): Time-to-live in seconds for items in the table.
            If set, items will expire after this many seconds. Defaults to None (no expiration).
        ttl_attribute (str, optional): The name of the attribute to use for TTL.
            Defaults to "TTL".

    Returns:
        DynamoDBChatStore: A DynamoDB chat store object.

    """

    table_name: str = Field(description="DynamoDB table")
    primary_key: str = Field(
        default="SessionId", description="Primary/partition key to use for the table."
    )
    profile_name: Optional[str] = Field(
        description="AWS profile to use. If not specified, then the default AWS profile is used."
    )
    aws_access_key_id: Optional[str] = Field(
        description="AWS Access Key ID to use.", exclude=True
    )
    aws_secret_access_key: Optional[str] = Field(
        description="AWS Secret Access Key to use.", exclude=True
    )
    aws_session_token: Optional[str] = Field(
        description="AWS Session Token to use.", exclude=True
    )
    botocore_session: Optional[Any] = Field(
        description="Use this Botocore session instead of creating a new default one.",
        exclude=True,
    )
    botocore_config: Optional[Any] = Field(
        description="Custom configuration object to use instead of the default generated one.",
        exclude=True,
    )
    region_name: Optional[str] = Field(
        description="AWS region name to use. Uses the region configured in AWS CLI if not passed",
        exclude=True,
    )
    max_retries: int = Field(
        default=10, description="The maximum number of API retries.", gt=0
    )
    timeout: float = Field(
        default=60.0,
        description="The timeout for API requests in seconds.",
    )
    session_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional kwargs for the `boto3.Session` object.",
    )
    resource_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional kwargs for the `boto3.Resource` object.",
    )
    ttl_seconds: Optional[int] = Field(
        default=None,
        description="Time-to-live in seconds for items in the table. If set, items will expire after this many seconds.",
    )
    ttl_attribute: str = Field(
        default="TTL",
        description="The name of the attribute to use for TTL.",
    )

    _client: ServiceResource = PrivateAttr()
    _table: Any = PrivateAttr()
    _aclient: ServiceResource = PrivateAttr()
    _atable: Any = PrivateAttr()

    def__init__(
        self,
        table_name: str,
        primary_key: str = "SessionId",
        profile_name: Optional[str] = None,
        region_name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        botocore_session: Optional[Any] = None,
        botocore_config: Optional[Any] = None,
        max_retries: int = 10,
        timeout: float = 60.0,
        session_kwargs: Optional[Dict[str, Any]] = None,
        resource_kwargs: Optional[Dict[str, Any]] = None,
        ttl_seconds: Optional[int] = None,
        ttl_attribute: str = "TTL",
    ):
        session_kwargs = session_kwargs or {}
        resource_kwargs = resource_kwargs or {}

        super().__init__(
            table_name=table_name,
            primary_key=primary_key,
            profile_name=profile_name,
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            botocore_session=botocore_session,
            botocore_config=botocore_config,
            max_retries=max_retries,
            timeout=timeout,
            session_kwargs=session_kwargs,
            resource_kwargs=resource_kwargs,
            ttl_seconds=ttl_seconds,
            ttl_attribute=ttl_attribute,
        )

        session_kwargs = {
            "profile_name": profile_name,
            "region_name": region_name,
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "aws_session_token": aws_session_token,
            "botocore_session": botocore_session,
            **session_kwargs,
        }

        try:
            importboto3
            frombotocore.configimport Config

            config = (
                Config(
                    retries={"max_attempts": max_retries, "mode": "standard"},
                    connect_timeout=timeout,
                    read_timeout=timeout,
                )
                if botocore_config is None
                else botocore_config
            )
            session = boto3.Session(**session_kwargs)
        except ImportError:
            raise ImportError(
                "boto3 package not found, install with 'pip install boto3"
            )

        self._client = session.resource("dynamodb", config=config, **resource_kwargs)
        self._table = self._client.Table(table_name)

    async definit_async_table(self):
"""Initialize asynchronous table."""
        if self._atable is None:
            try:
                importaioboto3

                async_session = aioboto3.Session(**self.session_kwargs)
            except ImportError:
                raise ImportError(
                    "aioboto3 package not found, install with 'pip install aioboto3'"
                )

            async with async_session.resource(
                "dynamodb", config=self.botocore_config, **self.resource_kwargs
            ) as dynamodb:
                self._atable = await dynamodb.Table(self.table_name)

    @classmethod
    defclass_name(self) -> str:
        return "DynamoDBChatStore"

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
        item = {self.primary_key: key, "History": _messages_to_dict(messages)}

        # Add TTL if configured
        if self.ttl_seconds is not None:
            item[self.ttl_attribute] = int(time.time()) + self.ttl_seconds

        self._table.put_item(Item=item)

    async defaset_messages(self, key: str, messages: List[ChatMessage]) -> None:
        self.init_async_table()

        item = {self.primary_key: key, "History": _messages_to_dict(messages)}

        # Add TTL if configured
        if self.ttl_seconds is not None:
            item[self.ttl_attribute] = int(time.time()) + self.ttl_seconds

        await self._atable.put_item(Item=item)

    defget_messages(self, key: str) -> List[ChatMessage]:
"""
        Retrieve all messages for the given key.

        Args:
            key (str): The key specifying a row.

        Returns:
            List[ChatMessage]: The messages associated with the key.

        """
        response = self._table.get_item(Key={self.primary_key: key})

        if response and "Item" in response:
            message_history = response["Item"]["History"]
        else:
            message_history = []

        return [_dict_to_message(message) for message in message_history]

    async defaget_messages(self, key: str) -> List[ChatMessage]:
        self.init_async_table()
        response = await self._atable.get_item(Key={self.primary_key: key})

        if response and "Item" in response:
            message_history = response["Item"]["History"]
        else:
            message_history = []

        return [_dict_to_message(message) for message in message_history]

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
        current_messages = _messages_to_dict(self.get_messages(key))
        current_messages.append(_message_to_dict(message))

        item = {self.primary_key: key, "History": current_messages}

        # Add TTL if configured
        if self.ttl_seconds is not None:
            item[self.ttl_attribute] = int(time.time()) + self.ttl_seconds

        self._table.put_item(Item=item)

    async defasync_add_message(self, key: str, message: ChatMessage) -> None:
        self.init_async_table()
        current_messages = _messages_to_dict(await self.aget_messages(key))
        current_messages.append(_message_to_dict(message))

        item = {self.primary_key: key, "History": current_messages}

        # Add TTL if configured
        if self.ttl_seconds is not None:
            item[self.ttl_attribute] = int(time.time()) + self.ttl_seconds

        await self._atable.put_item(Item=item)

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
        self._table.delete_item(Key={self.primary_key: key})
        return messages_to_delete

    async defadelete_messages(self, key: str) -> Optional[List[ChatMessage]]:
        self.init_async_table()
        messages_to_delete = await self.aget_messages(key)
        await self._atable.delete_item(Key={self.primary_key: key})
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

    async defadelete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
        self.init_async_table()
        current_messages = await self.aget_messages(key)
        try:
            message_to_delete = current_messages[idx]
            del current_messages[idx]
            await self.aset_messages(key, current_messages)
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

    async defadelete_last_message(self, key: str) -> Optional[ChatMessage]:
        return self.adelete_message(key, -1)

    defget_keys(self) -> List[str]:
"""
        Retrieve all keys in the table.

        Returns:
            List[str]: The keys in the table.

        """
        response = self._table.scan(ProjectionExpression=self.primary_key)
        keys = [item[self.primary_key] for item in response["Items"]]
        while "LastEvaluatedKey" in response:
            response = self._table.scan(
                ProjectionExpression=self.primary_key,
                ExclusiveStartKey=response["LastEvaluatedKey"],
            )
            keys.extend([item[self.primary_key] for item in response["Items"]])
        return keys

    async defaget_keys(self) -> List[str]:
        self.init_async_table()
        response = await self._atable.scan(ProjectionExpression=self.primary_key)
        keys = [item[self.primary_key] for item in response["Items"]]
        while "LastEvaluatedKey" in response:
            response = await self._atable.scan(
                ProjectionExpression=self.primary_key,
                ExclusiveStartKey=response["LastEvaluatedKey"],
            )
            keys.extend([item[self.primary_key] for item in response["Items"]])
        return keys

```
 |  
| --- | --- |  
###  init_async_table [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/dynamodb/#llama_index.storage.chat_store.dynamodb.DynamoDBChatStore.init_async_table "Permanent link")

```
init_async_table()

```

Initialize asynchronous table.
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-dynamodb/llama_index/storage/chat_store/dynamodb/base.py`  
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
200
201
202
```
 | 
```
async definit_async_table(self):
"""Initialize asynchronous table."""
    if self._atable is None:
        try:
            importaioboto3

            async_session = aioboto3.Session(**self.session_kwargs)
        except ImportError:
            raise ImportError(
                "aioboto3 package not found, install with 'pip install aioboto3'"
            )

        async with async_session.resource(
            "dynamodb", config=self.botocore_config, **self.resource_kwargs
        ) as dynamodb:
            self._atable = await dynamodb.Table(self.table_name)

```
 |  
| --- | --- |  
###  set_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/dynamodb/#llama_index.storage.chat_store.dynamodb.DynamoDBChatStore.set_messages "Permanent link")

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
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-dynamodb/llama_index/storage/chat_store/dynamodb/base.py`  
| 
```
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
    item = {self.primary_key: key, "History": _messages_to_dict(messages)}

    # Add TTL if configured
    if self.ttl_seconds is not None:
        item[self.ttl_attribute] = int(time.time()) + self.ttl_seconds

    self._table.put_item(Item=item)

```
 |  
| --- | --- |  
###  get_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/dynamodb/#llama_index.storage.chat_store.dynamodb.DynamoDBChatStore.get_messages "Permanent link")

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
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-dynamodb/llama_index/storage/chat_store/dynamodb/base.py`  
| 
```
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
    response = self._table.get_item(Key={self.primary_key: key})

    if response and "Item" in response:
        message_history = response["Item"]["History"]
    else:
        message_history = []

    return [_dict_to_message(message) for message in message_history]

```
 |  
| --- | --- |  
###  add_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/dynamodb/#llama_index.storage.chat_store.dynamodb.DynamoDBChatStore.add_message "Permanent link")

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
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-dynamodb/llama_index/storage/chat_store/dynamodb/base.py`  
| 
```
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
282
283
284
285
286
287
288
289
290
291
292
293
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
    current_messages = _messages_to_dict(self.get_messages(key))
    current_messages.append(_message_to_dict(message))

    item = {self.primary_key: key, "History": current_messages}

    # Add TTL if configured
    if self.ttl_seconds is not None:
        item[self.ttl_attribute] = int(time.time()) + self.ttl_seconds

    self._table.put_item(Item=item)

```
 |  
| --- | --- |  
###  delete_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/dynamodb/#llama_index.storage.chat_store.dynamodb.DynamoDBChatStore.delete_messages "Permanent link")

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
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-dynamodb/llama_index/storage/chat_store/dynamodb/base.py`  
| 
```
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
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
    self._table.delete_item(Key={self.primary_key: key})
    return messages_to_delete

```
 |  
| --- | --- |  
###  delete_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/dynamodb/#llama_index.storage.chat_store.dynamodb.DynamoDBChatStore.delete_message "Permanent link")

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
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-dynamodb/llama_index/storage/chat_store/dynamodb/base.py`  
| 
```
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
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
###  delete_last_message [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/dynamodb/#llama_index.storage.chat_store.dynamodb.DynamoDBChatStore.delete_last_message "Permanent link")

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
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-dynamodb/llama_index/storage/chat_store/dynamodb/base.py`  
| 
```
369
370
371
372
373
374
375
376
377
378
379
380
381
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
###  get_keys [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/chat_store/dynamodb/#llama_index.storage.chat_store.dynamodb.DynamoDBChatStore.get_keys "Permanent link")

```
get_keys() -> []

```

Retrieve all keys in the table.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: The keys in the table.  |  
Source code in `llama-index-integrations/storage/chat_store/llama-index-storage-chat-store-dynamodb/llama_index/storage/chat_store/dynamodb/base.py`  
| 
```
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
```
 | 
```
defget_keys(self) -> List[str]:
"""
    Retrieve all keys in the table.

    Returns:
        List[str]: The keys in the table.

    """
    response = self._table.scan(ProjectionExpression=self.primary_key)
    keys = [item[self.primary_key] for item in response["Items"]]
    while "LastEvaluatedKey" in response:
        response = self._table.scan(
            ProjectionExpression=self.primary_key,
            ExclusiveStartKey=response["LastEvaluatedKey"],
        )
        keys.extend([item[self.primary_key] for item in response["Items"]])
    return keys

```
 |  
| --- | --- |  
options: members: - DynamoDBChatStore
