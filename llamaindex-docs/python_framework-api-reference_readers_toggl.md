# Toggl
##  TogglReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/toggl/#llama_index.readers.toggl.TogglReader "Permanent link")
Bases: 
Source code in `llama-index-integrations/readers/llama-index-readers-toggl/llama_index/readers/toggl/base.py`  
| 
```
 11
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
```
 | 
```
classTogglReader(BaseReader):
    def__init__(
        self, api_token: str, user_agent: str = "llama_index_toggl_reader"
    ) -> None:
"""Initialize with parameters."""
        super().__init__()
        self.api_token = api_token
        self.user_agent = user_agent
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    defload_data(
        self,
        workspace_id: str,
        project_id: str,
        start_date: Optional[datetime.datetime] = None,
        end_date: Optional[datetime.datetime] = datetime.datetime.now(),
        out_format: TogglOutFormat = TogglOutFormat.json,
    ) -> List[Document]:
"""
        Load data from Toggl.

        Args:
            workspace_id (str): The workspace ID.
            project_id (str): The project ID.
            start_date (Optional[datetime.datetime]): The start date.
            end_date (Optional[datetime.datetime]): The end date.
            out_format (TogglOutFormat): The output format.

        """
        return self.loop.run_until_complete(
            self.aload_data(workspace_id, project_id, start_date, end_date, out_format)
        )

    async defaload_data(
        self,
        workspace_id: str,
        project_id: str,
        start_date: Optional[datetime.datetime],
        end_date: Optional[datetime.datetime],
        out_format: TogglOutFormat,
    ) -> List[Document]:
"""Load time entries from Toggl."""
        fromtoggl.api_clientimport TogglClientApi

        client = TogglClientApi(
            {
                "token": self.api_token,
                "workspace_id": workspace_id,
                "user_agent": self.user_agent,
            }
        )
        project_times = client.get_project_times(project_id, start_date, end_date)
        raw_items = [
            TogglTrackItem.model_validate(raw_item)
            for raw_item in project_times["data"]
        ]
        items = []
        for item in raw_items:
            if out_format == TogglOutFormat.json:
                text = item.model_dump_json()
            elif out_format == TogglOutFormat.markdown:
                text = f"""# {item.description}
                    **Start:** {item.start:%Y-%m-%d %H:%M:%S%z}
                    **End:** {item.end:%Y-%m-%d %H:%M:%S%z}
                    **Duration:** {self.milliseconds_to_postgresql_interval(item.dur)}
                    **Tags:** {",".join(item.tags)}

            doc = Document(text=text)
            doc.metadata = {**doc.metadata, **item.dict()}
            items.append(doc)
        return items

    defmilliseconds_to_postgresql_interval(self, milliseconds):
        seconds, milliseconds = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        interval = ""
        if days  0:
            interval += f"{days}d"
        if hours  0:
            interval += f"{hours}h"
        if minutes  0:
            interval += f"{minutes}m"
        if seconds  0 or milliseconds  0:
            interval += f"{seconds}s"
        if milliseconds  0:
            interval += f"{milliseconds}ms"

        return interval

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/toggl/#llama_index.readers.toggl.TogglReader.load_data "Permanent link")

```
load_data(
    workspace_id: ,
    project_id: ,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = (),
    out_format: TogglOutFormat = ,
) -> []

```

Load data from Toggl.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `workspace_id`  |  The workspace ID.  |  _required_  |  
|  `project_id`  |  The project ID.  |  _required_  |  
|  `start_date`  |  `Optional[datetime]`  |  The start date.  |  `None`  |  
|  `end_date`  |  `Optional[datetime]`  |  The end date.  |  `now()`  |  
|  `out_format`  |  `TogglOutFormat`  |  The output format.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-toggl/llama_index/readers/toggl/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    workspace_id: str,
    project_id: str,
    start_date: Optional[datetime.datetime] = None,
    end_date: Optional[datetime.datetime] = datetime.datetime.now(),
    out_format: TogglOutFormat = TogglOutFormat.json,
) -> List[Document]:
"""
    Load data from Toggl.

    Args:
        workspace_id (str): The workspace ID.
        project_id (str): The project ID.
        start_date (Optional[datetime.datetime]): The start date.
        end_date (Optional[datetime.datetime]): The end date.
        out_format (TogglOutFormat): The output format.

    """
    return self.loop.run_until_complete(
        self.aload_data(workspace_id, project_id, start_date, end_date, out_format)
    )

```
 |  
| --- | --- |  
###  aload_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/toggl/#llama_index.readers.toggl.TogglReader.aload_data "Permanent link")

```
aload_data(
    workspace_id: ,
    project_id: ,
    start_date: Optional[datetime],
    end_date: Optional[datetime],
    out_format: TogglOutFormat,
) -> []

```

Load time entries from Toggl.
Source code in `llama-index-integrations/readers/llama-index-readers-toggl/llama_index/readers/toggl/base.py`  
| 
```
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
```
 | 
```
async defaload_data(
    self,
    workspace_id: str,
    project_id: str,
    start_date: Optional[datetime.datetime],
    end_date: Optional[datetime.datetime],
    out_format: TogglOutFormat,
) -> List[Document]:
"""Load time entries from Toggl."""
    fromtoggl.api_clientimport TogglClientApi

    client = TogglClientApi(
        {
            "token": self.api_token,
            "workspace_id": workspace_id,
            "user_agent": self.user_agent,
        }
    )
    project_times = client.get_project_times(project_id, start_date, end_date)
    raw_items = [
        TogglTrackItem.model_validate(raw_item)
        for raw_item in project_times["data"]
    ]
    items = []
    for item in raw_items:
        if out_format == TogglOutFormat.json:
            text = item.model_dump_json()
        elif out_format == TogglOutFormat.markdown:
            text = f"""# {item.description}
                **Start:** {item.start:%Y-%m-%d %H:%M:%S%z}
                **End:** {item.end:%Y-%m-%d %H:%M:%S%z}
                **Duration:** {self.milliseconds_to_postgresql_interval(item.dur)}
                **Tags:** {",".join(item.tags)}

        doc = Document(text=text)
        doc.metadata = {**doc.metadata, **item.dict()}
        items.append(doc)
    return items

```
 |  
| --- | --- |  
options: members: - TogglReader
