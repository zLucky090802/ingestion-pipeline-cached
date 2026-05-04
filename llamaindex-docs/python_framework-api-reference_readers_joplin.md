# Joplin
##  JoplinReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/joplin/#llama_index.readers.joplin.JoplinReader "Permanent link")
Bases: 
Reader that fetches notes from Joplin.
In order to use this reader, you need to have Joplin running with the Web Clipper enabled (look for "Web Clipper" in the app settings).
To get the access token, you need to go to the Web Clipper options and under "Advanced Options" you will find the access token. You may provide it as an argument or set the JOPLIN_ACCESS_TOKEN environment variable.
You can find more information about the Web Clipper service here: https://joplinapp.org/clipper/
Source code in `llama-index-integrations/readers/llama-index-readers-joplin/llama_index/readers/joplin/base.py`  
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
```
 | 
```
classJoplinReader(BaseReader):
"""
    Reader that fetches notes from Joplin.

    In order to use this reader, you need to have Joplin running with the
    Web Clipper enabled (look for "Web Clipper" in the app settings).

    To get the access token, you need to go to the Web Clipper options and
    under "Advanced Options" you will find the access token. You may provide
    it as an argument or set the JOPLIN_ACCESS_TOKEN environment variable.

    You can find more information about the Web Clipper service here:
    https://joplinapp.org/clipper/
    """

    def__init__(
        self,
        access_token: Optional[str] = None,
        parse_markdown: bool = True,
        port: int = 41184,
        host: str = "localhost",
    ) -> None:
"""
        Initialize a new instance of JoplinReader.

        Args:
            access_token (Optional[str]): The access token for Joplin's Web Clipper service.
                If not provided, the JOPLIN_ACCESS_TOKEN environment variable is used. Default is None.
            parse_markdown (bool): Whether to parse the markdown content of the notes using MarkdownReader. Default is True.
            port (int): The port on which Joplin's Web Clipper service is running. Default is 41184.
            host (str): The host on which Joplin's Web Clipper service is running. Default is "localhost".

        """
        self.parse_markdown = parse_markdown
        if parse_markdown:
            self.parser = MarkdownReader()

        access_token = access_token or self._get_token_from_env()
        base_url = f"http://{host}:{port}"
        self._get_note_url = (
            f"{base_url}/notes?token={access_token}"
            "&fields=id,parent_id,title,body,created_time,updated_time&page={page}"
        )
        self._get_folder_url = (
            f"{base_url}/folders/{{id}}?token={access_token}&fields=title"
        )
        self._get_tag_url = (
            f"{base_url}/notes/{{id}}/tags?token={access_token}&fields=title"
        )

    def_get_token_from_env(self) -> str:
        if "JOPLIN_ACCESS_TOKEN" in os.environ:
            return os.environ["JOPLIN_ACCESS_TOKEN"]
        else:
            raise ValueError(
                "You need to provide an access token to use the Joplin reader. You may"
                " provide it as an argument or set the JOPLIN_ACCESS_TOKEN environment"
                " variable."
            )

    def_get_notes(self) -> Iterator[Document]:
        has_more = True
        page = 1
        while has_more:
            req_note = urllib.request.Request(self._get_note_url.format(page=page))
            with urllib.request.urlopen(req_note) as response:
                json_data = json.loads(response.read().decode())
                for note in json_data["items"]:
                    metadata = {
                        "source": LINK_NOTE_TEMPLATE.format(id=note["id"]),
                        "folder": self._get_folder(note["parent_id"]),
                        "tags": self._get_tags(note["id"]),
                        "title": note["title"],
                        "created_time": self._convert_date(note["created_time"]),
                        "updated_time": self._convert_date(note["updated_time"]),
                    }
                    if self.parse_markdown:
                        yield from self.parser.load_data(
                            None, content=note["body"], extra_info=metadata
                        )
                    else:
                        yield Document(text=note["body"], extra_info=metadata)

                has_more = json_data["has_more"]
                page += 1

    def_get_folder(self, folder_id: str) -> str:
        req_folder = urllib.request.Request(self._get_folder_url.format(id=folder_id))
        with urllib.request.urlopen(req_folder) as response:
            json_data = json.loads(response.read().decode())
            return json_data["title"]

    def_get_tags(self, note_id: str) -> List[str]:
        req_tag = urllib.request.Request(self._get_tag_url.format(id=note_id))
        with urllib.request.urlopen(req_tag) as response:
            json_data = json.loads(response.read().decode())
            return ",".join([tag["title"] for tag in json_data["items"]])

    def_convert_date(self, date: int) -> str:
        return datetime.fromtimestamp(date / 1000).strftime("%Y-%m-%d %H:%M:%S")

    deflazy_load(self) -> Iterator[Document]:
        yield from self._get_notes()

    defload_data(self) -> List[Document]:
        return list(self.lazy_load())

```
 |  
| --- | --- |  
options: members: - JoplinReader
