# Slack
##  SlackToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/slack/#llama_index.tools.slack.SlackToolSpec "Permanent link")
Bases: 
Slack tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-slack/llama_index/tools/slack/base.py`  
| 
```
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
```
 | 
```
classSlackToolSpec(BaseToolSpec):
"""Slack tool spec."""

    spec_functions = ["load_data", "send_message", "fetch_channels"]

    def__init__(
        self,
        slack_token: Optional[str] = None,
        ssl: Optional[SSLContext] = None,
        earliest_date: Optional[datetime] = None,
        latest_date: Optional[datetime] = None,
    ) -> None:
"""Initialize with parameters."""
        self.reader = SlackReader(
            slack_token=slack_token,
            ssl=ssl,
            earliest_date=earliest_date,
            latest_date=latest_date,
        )

    defload_data(
        self,
        channel_ids: List[str],
        reverse_chronological: bool = True,
    ) -> List[Document]:
"""Load data from the input directory."""
        return self.reader.load_data(
            channel_ids=channel_ids,
            reverse_chronological=reverse_chronological,
        )

    defsend_message(
        self,
        channel_id: str,
        message: str,
    ) -> None:
"""Send a message to a channel given the channel ID."""
        slack_client = self.reader._client
        try:
            msg_result = slack_client.chat_postMessage(
                channel=channel_id,
                text=message,
            )
            logger.info(msg_result)
        except Exception as e:
            logger.error(e)
            raise

    deffetch_channels(
        self,
    ) -> List[str]:
"""Fetch a list of relevant channels."""
        slack_client = self.reader._client
        try:
            msg_result = slack_client.conversations_list()
            logger.info(msg_result)
        except Exception as e:
            logger.error(e)
            raise

        return msg_result["channels"]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/slack/#llama_index.tools.slack.SlackToolSpec.load_data "Permanent link")

```
load_data(
    channel_ids: [],
    reverse_chronological:  = True,
) -> []

```

Load data from the input directory.
Source code in `llama-index-integrations/tools/llama-index-tools-slack/llama_index/tools/slack/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    channel_ids: List[str],
    reverse_chronological: bool = True,
) -> List[Document]:
"""Load data from the input directory."""
    return self.reader.load_data(
        channel_ids=channel_ids,
        reverse_chronological=reverse_chronological,
    )

```
 |  
| --- | --- |  
###  send_message [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/slack/#llama_index.tools.slack.SlackToolSpec.send_message "Permanent link")

```
send_message(channel_id: , message: ) -> None

```

Send a message to a channel given the channel ID.
Source code in `llama-index-integrations/tools/llama-index-tools-slack/llama_index/tools/slack/base.py`  
| 
```
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
```
 | 
```
defsend_message(
    self,
    channel_id: str,
    message: str,
) -> None:
"""Send a message to a channel given the channel ID."""
    slack_client = self.reader._client
    try:
        msg_result = slack_client.chat_postMessage(
            channel=channel_id,
            text=message,
        )
        logger.info(msg_result)
    except Exception as e:
        logger.error(e)
        raise

```
 |  
| --- | --- |  
###  fetch_channels [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/slack/#llama_index.tools.slack.SlackToolSpec.fetch_channels "Permanent link")

```
fetch_channels() -> []

```

Fetch a list of relevant channels.
Source code in `llama-index-integrations/tools/llama-index-tools-slack/llama_index/tools/slack/base.py`  
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
```
 | 
```
deffetch_channels(
    self,
) -> List[str]:
"""Fetch a list of relevant channels."""
    slack_client = self.reader._client
    try:
        msg_result = slack_client.conversations_list()
        logger.info(msg_result)
    except Exception as e:
        logger.error(e)
        raise

    return msg_result["channels"]

```
 |  
| --- | --- |  
options: members: - SlackToolSpec
