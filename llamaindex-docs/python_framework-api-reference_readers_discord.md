# Discord
##  DiscordReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/discord/#llama_index.readers.discord.DiscordReader "Permanent link")
Bases: 
Discord reader.
Reads conversations from channels.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `discord_token`  |  `Optional[str]`  |  Discord token. If not provided, we assume the environment variable `DISCORD_TOKEN` is set.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-discord/llama_index/readers/discord/base.py`  
| 
```
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
```
 | 
```
classDiscordReader(BasePydanticReader):
"""
    Discord reader.

    Reads conversations from channels.

    Args:
        discord_token (Optional[str]): Discord token. If not provided, we
            assume the environment variable `DISCORD_TOKEN` is set.

    """

    is_remote: bool = True
    discord_token: str

    def__init__(self, discord_token: Optional[str] = None) -> None:
"""Initialize with parameters."""
        try:
            importdiscord  # noqa: F401
        except ImportError:
            raise ImportError(
                "`discord.py` package not found, please run `pip install discord.py`"
            )
        if discord_token is None:
            discord_token = os.environ["DISCORD_TOKEN"]
            if discord_token is None:
                raise ValueError(
                    "Must specify `discord_token` or set environment "
                    "variable `DISCORD_TOKEN`."
                )

        super().__init__(discord_token=discord_token)

    @classmethod
    defclass_name(cls) -> str:
"""Get the name identifier of the class."""
        return "DiscordReader"

    def_read_channel(
        self, channel_id: int, limit: Optional[int] = None, oldest_first: bool = True
    ) -> List[Document]:
"""Read channel."""
        return asyncio.get_event_loop().run_until_complete(
            read_channel(
                self.discord_token, channel_id, limit=limit, oldest_first=oldest_first
            )
        )

    defload_data(
        self,
        channel_ids: List[int],
        limit: Optional[int] = None,
        oldest_first: bool = True,
    ) -> List[Document]:
"""
        Load data from the input directory.

        Args:
            channel_ids (List[int]): List of channel ids to read.
            limit (Optional[int]): Maximum number of messages to read.
            oldest_first (bool): Whether to read oldest messages first.
                Defaults to `True`.

        Returns:
            List[Document]: List of documents.

        """
        results: List[Document] = []
        for channel_id in channel_ids:
            if not isinstance(channel_id, int):
                raise ValueError(
                    f"Channel id {channel_id} must be an integer, "
                    f"not {type(channel_id)}."
                )
            channel_documents = self._read_channel(
                channel_id, limit=limit, oldest_first=oldest_first
            )
            results += channel_documents
        return results

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/discord/#llama_index.readers.discord.DiscordReader.class_name "Permanent link")

```
class_name() -> 

```

Get the name identifier of the class.
Source code in `llama-index-integrations/readers/llama-index-readers-discord/llama_index/readers/discord/base.py`  
| 
```
123
124
125
126
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get the name identifier of the class."""
    return "DiscordReader"

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/discord/#llama_index.readers.discord.DiscordReader.load_data "Permanent link")

```
load_data(
    channel_ids: [],
    limit: Optional[] = None,
    oldest_first:  = True,
) -> []

```

Load data from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `channel_ids`  |  `List[int]`  |  List of channel ids to read.  |  _required_  |  
|  `limit`  |  `Optional[int]`  |  Maximum number of messages to read.  |  `None`  |  
|  `oldest_first`  |  `bool`  |  Whether to read oldest messages first. Defaults to `True`.  |  `True`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-discord/llama_index/readers/discord/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    channel_ids: List[int],
    limit: Optional[int] = None,
    oldest_first: bool = True,
) -> List[Document]:
"""
    Load data from the input directory.

    Args:
        channel_ids (List[int]): List of channel ids to read.
        limit (Optional[int]): Maximum number of messages to read.
        oldest_first (bool): Whether to read oldest messages first.
            Defaults to `True`.

    Returns:
        List[Document]: List of documents.

    """
    results: List[Document] = []
    for channel_id in channel_ids:
        if not isinstance(channel_id, int):
            raise ValueError(
                f"Channel id {channel_id} must be an integer, "
                f"not {type(channel_id)}."
            )
        channel_documents = self._read_channel(
            channel_id, limit=limit, oldest_first=oldest_first
        )
        results += channel_documents
    return results

```
 |  
| --- | --- |  
options: members: - DiscordReader
