# Zulip
##  ZulipReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/zulip/#llama_index.readers.zulip.ZulipReader "Permanent link")
Bases: 
Zulip reader.
Source code in `llama-index-integrations/readers/llama-index-readers-zulip/llama_index/readers/zulip/base.py`  
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
```
 | 
```
classZulipReader(BaseReader):
"""Zulip reader."""

    def__init__(
        self,
        zulip_email: str,
        zulip_domain: str,
        earliest_date: Optional[datetime] = None,
        latest_date: Optional[datetime] = None,
    ) -> None:
        importzulip

"""Initialize with parameters."""
        # Read the Zulip token from the environment variable
        zulip_token = os.environ.get("ZULIP_TOKEN")

        if zulip_token is None:
            raise ValueError("ZULIP_TOKEN environment variable not set.")

        # Initialize Zulip client with provided parameters
        self.client = zulip.Client(
            api_key=zulip_token, email=zulip_email, site=zulip_domain
        )

    def_read_stream(self, stream_name: str, reverse_chronological: bool) -> str:
"""Read a stream."""
        params = {
            "narrow": [{"operator": "stream", "operand": stream_name}],
            "anchor": "newest",
            "num_before": 100,
            "num_after": 0,
        }
        response = self.client.get_messages(params)
        messages = response["messages"]
        if reverse_chronological:
            messages.reverse()
        return " ".join([message["content"] for message in messages])

    defload_data(
        self, streams: List[str], reverse_chronological: bool = True
    ) -> List[Document]:
"""Load data from the input streams."""
        # Load data logic here
        data = []
        for stream_name in streams:
            stream_content = self._read_stream(stream_name, reverse_chronological)
            data.append(
                Document(text=stream_content, extra_info={"stream": stream_name})
            )
        return data

    defget_all_streams(self) -> list:
        # Fetch all streams
        response = self.client.get_streams()
        streams_data = response["streams"]
        # Collect the stream IDs
        return [stream["name"] for stream in streams_data]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/zulip/#llama_index.readers.zulip.ZulipReader.load_data "Permanent link")

```
load_data(
    streams: [], reverse_chronological:  = True
) -> []

```

Load data from the input streams.
Source code in `llama-index-integrations/readers/llama-index-readers-zulip/llama_index/readers/zulip/base.py`  
| 
```
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
defload_data(
    self, streams: List[str], reverse_chronological: bool = True
) -> List[Document]:
"""Load data from the input streams."""
    # Load data logic here
    data = []
    for stream_name in streams:
        stream_content = self._read_stream(stream_name, reverse_chronological)
        data.append(
            Document(text=stream_content, extra_info={"stream": stream_name})
        )
    return data

```
 |  
| --- | --- |  
options: members: - ZulipReader
