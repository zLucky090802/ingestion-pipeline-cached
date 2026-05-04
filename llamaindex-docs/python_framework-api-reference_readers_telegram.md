# Telegram
##  TelegramReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/telegram/#llama_index.readers.telegram.TelegramReader "Permanent link")
Bases: 
Telegram posts/chat messages/comments reader.
Read posts/chat messages/comments from Telegram channels or chats.
Before working with Telegram’s API, you need to get your own API ID and hash:

```
1. Login to your Telegram account with the phone number of the developer account to use.
2. Click under API Development tools.
3. A Create new application window will appear. Fill in your application details.            There is no need to enter any URL,            and only the first two fields (App title and Short name) can currently be changed later.
4. Click on Create application at the end.            Remember that your API hash is secret and Telegram won’t let you revoke it.            Don’t post it anywhere!

```

This API ID and hash is the one used by your application, not your phone number. You can use this API ID and hash with any phone number.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `session_name`  |  The file name of the session file to be used if a string is given (it may be a full path), or the Session instance to be used otherwise.  |  _required_  |  
|  `api_id`  |  The API ID you obtained from https://my.telegram.org.  |  _required_  |  
|  `api_hash`  |  The API hash you obtained from https://my.telegram.org.  |  _required_  |  
|  `phone_number`  |  The phone to which the code will be sent.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-telegram/llama_index/readers/telegram/base.py`  
| 
```
 12
 13
 14
 15
 16
 17
 18
 19
 20
 21
 22
 23
 24
 25
 26
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
```
 | 
```
classTelegramReader(BaseReader):
"""
    Telegram posts/chat messages/comments reader.

    Read posts/chat messages/comments from Telegram channels or chats.

    Before working with Telegram’s API, you need to get your own API ID and hash:

        1. Login to your Telegram account with the phone number of the developer account to use.
        2. Click under API Development tools.
        3. A Create new application window will appear. Fill in your application details.\
            There is no need to enter any URL,\
            and only the first two fields (App title and Short name) can currently be changed later.
        4. Click on Create application at the end.\
            Remember that your API hash is secret and Telegram won’t let you revoke it.\
            Don’t post it anywhere!

    This API ID and hash is the one used by your application, not your phone number.\
        You can use this API ID and hash with any phone number.

    Args:
        session_name (str): The file name of the session file to be used\
            if a string is given (it may be a full path),\
            or the Session instance to be used otherwise.
        api_id (int): The API ID you obtained from https://my.telegram.org.
        api_hash (str): The API hash you obtained from https://my.telegram.org.
        phone_number (str): The phone to which the code will be sent.

    """

    def__init__(
        self,
        session_name: str,
        api_id: int,
        api_hash: str,
        phone_number: str,
    ) -> None:
"""Initialize with parameters."""
        super().__init__()
        self.session_name = session_name
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    defload_data(
        self,
        entity_name: str,
        post_id: Optional[int] = None,
        limit: Optional[int] = None,
        start_date: Optional[datetime.datetime] = None,
        end_date: Optional[datetime.datetime] = None,
    ) -> List[Document]:
"""
        Load posts/chat messages/comments from Telegram channels or chats.

        Since Telethon is an asynchronous library,\
            you need to await coroutine functions to have them run\
            (or otherwise, run the loop until they are complete)

        Args:
            entity_name (str): The entity from whom to retrieve the message history.
            post_id (int): If set to a post ID, \
                the comments that reply to this ID will be returned.\
                Else will get posts/chat messages.
            limit (int): Number of messages to be retrieved.
            start_date (datetime.datetime): Start date of the time period.
            end_date (datetime.datetime): End date of the time period.

        """
        return self.loop.run_until_complete(
            self._load_data(
                entity_name=entity_name,
                post_id=post_id,
                limit=limit,
                start_date=start_date,
                end_date=end_date,
            )
        )

    async def_load_data(
        self,
        entity_name: str,
        post_id: Optional[int] = None,
        limit: Optional[int] = None,
        start_date: Optional[datetime.datetime] = None,
        end_date: Optional[datetime.datetime] = None,
    ) -> List[Document]:
"""
        Load posts/chat messages/comments from Telegram channels or chats.

        Args:
            entity_name (str): The entity from whom to retrieve the message history.
            post_id (int): If set to a post ID, \
                the comments that reply to this ID will be returned.\
                Else will get posts/chat messages.
            limit (int): Number of messages to be retrieved.
            start_date (datetime.datetime): Start date of the time period.
            end_date (datetime.datetime): End date of the time period.

        """
        importtelethon

        client = telethon.TelegramClient(self.session_name, self.api_id, self.api_hash)
        await client.start(phone=self.phone_number)

        results = []
        async with client:
            if end_date and start_date:
                # Asynchronously iterate over messages in between start_date and end_date
                async for message in client.iter_messages(
                    entity_name,
                    reply_to=post_id,
                    limit=limit,
                    offset_date=end_date,
                ):
                    if message.date  start_date:
                        break
                    if isinstance(message.text, str) and message.text != "":
                        results.append(Document(text=self._remove_links(message.text)))
            else:
                # Asynchronously iterate over messages
                async for message in client.iter_messages(
                    entity_name,
                    reply_to=post_id,
                    limit=limit,
                ):
                    if isinstance(message.text, str) and message.text != "":
                        results.append(Document(text=self._remove_links(message.text)))
        return results

    def_remove_links(self, string) -> str:
"""Removes all URLs from a given string, leaving only the base domain name."""

        defreplace_match(match):
            text = match.group(1)
            return text if text else ""

        url_pattern = r"https?://(?:www\.)?((?!www\.).)+?"
        return re.sub(url_pattern, replace_match, string)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/telegram/#llama_index.readers.telegram.TelegramReader.load_data "Permanent link")

```
load_data(
    entity_name: ,
    post_id: Optional[] = None,
    limit: Optional[] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> []

```

Load posts/chat messages/comments from Telegram channels or chats.
Since Telethon is an asynchronous library, you need to await coroutine functions to have them run (or otherwise, run the loop until they are complete)
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `entity_name`  |  The entity from whom to retrieve the message history.  |  _required_  |  
|  `post_id`  |  If set to a post ID, the comments that reply to this ID will be returned. Else will get posts/chat messages.  |  `None`  |  
|  `limit`  |  Number of messages to be retrieved.  |  `None`  |  
|  `start_date`  |  `datetime`  |  Start date of the time period.  |  `None`  |  
|  `end_date`  |  `datetime`  |  End date of the time period.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-telegram/llama_index/readers/telegram/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    entity_name: str,
    post_id: Optional[int] = None,
    limit: Optional[int] = None,
    start_date: Optional[datetime.datetime] = None,
    end_date: Optional[datetime.datetime] = None,
) -> List[Document]:
"""
    Load posts/chat messages/comments from Telegram channels or chats.

    Since Telethon is an asynchronous library,\
        you need to await coroutine functions to have them run\
        (or otherwise, run the loop until they are complete)

    Args:
        entity_name (str): The entity from whom to retrieve the message history.
        post_id (int): If set to a post ID, \
            the comments that reply to this ID will be returned.\
            Else will get posts/chat messages.
        limit (int): Number of messages to be retrieved.
        start_date (datetime.datetime): Start date of the time period.
        end_date (datetime.datetime): End date of the time period.

    """
    return self.loop.run_until_complete(
        self._load_data(
            entity_name=entity_name,
            post_id=post_id,
            limit=limit,
            start_date=start_date,
            end_date=end_date,
        )
    )

```
 |  
| --- | --- |  
options: members: - TelegramReader
