# Steamship
##  SteamshipFileReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/steamship/#llama_index.readers.steamship.SteamshipFileReader "Permanent link")
Bases: 
Reads persistent Steamship Files and converts them to Documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  `Optional[str]`  |  Steamship API key. Defaults to STEAMSHIP_API_KEY value if not provided.  |  `None`  |  
Note
Requires install of `steamship` package and an active Steamship API Key. To get a Steamship API Key, visit: https://steamship.com/account/api. Once you have an API Key, expose it via an environment variable named `STEAMSHIP_API_KEY` or pass it as an init argument (`api_key`).
Source code in `llama-index-integrations/readers/llama-index-readers-steamship/llama_index/readers/steamship/base.py`  
| 
```
 9
10
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
```
 | 
```
classSteamshipFileReader(BaseReader):
"""
    Reads persistent Steamship Files and converts them to Documents.

    Args:
        api_key: Steamship API key. Defaults to STEAMSHIP_API_KEY value if not provided.

    Note:
        Requires install of `steamship` package and an active Steamship API Key.
        To get a Steamship API Key, visit: https://steamship.com/account/api.
        Once you have an API Key, expose it via an environment variable named
        `STEAMSHIP_API_KEY` or pass it as an init argument (`api_key`).

    """

    def__init__(self, api_key: Optional[str] = None) -> None:
"""Initialize the Reader."""
        try:
            importsteamship  # noqa

            self.api_key = api_key
        except ImportError:
            raise ImportError(
                "`steamship` must be installed to use the SteamshipFileReader.\n"
                "Please run `pip install --upgrade steamship."
            )

    defload_data(
        self,
        workspace: str,
        query: Optional[str] = None,
        file_handles: Optional[List[str]] = None,
        collapse_blocks: bool = True,
        join_str: str = "\n\n",
    ) -> List[Document]:
"""
        Load data from persistent Steamship Files into Documents.

        Args:
            workspace: the handle for a Steamship workspace
                (see: https://docs.steamship.com/workspaces/index.html)
            query: a Steamship tag query for retrieving files
                (ex: 'filetag and value("import-id")="import-001"')
            file_handles: a list of Steamship File handles
                (ex: `smooth-valley-9kbdr`)
            collapse_blocks: whether to merge individual File Blocks into a
                single Document, or separate them.
            join_str: when collapse_blocks is True, this is how the block texts
                will be concatenated.

        Note:
            The collection of Files from both `query` and `file_handles` will be
            combined. There is no (current) support for deconflicting the collections
            (meaning that if a file appears both in the result set of the query and
            as a handle in file_handles, it will be loaded twice).

        """
        fromsteamshipimport File, Steamship

        client = Steamship(workspace=workspace, api_key=self.api_key)
        files = []
        if query:
            files_from_query = File.query(client=client, tag_filter_query=query).files
            files.extend(files_from_query)

        if file_handles:
            files.extend([File.get(client=client, handle=h) for h in file_handles])

        docs = []
        for file in files:
            metadata = {"source": file.handle}

            for tag in file.tags:
                metadata[tag.kind] = tag.value

            if collapse_blocks:
                text = join_str.join([b.text for b in file.blocks])
                docs.append(Document(text=text, id_=file.handle, metadata=metadata))
            else:
                docs.extend(
                    [
                        Document(text=b.text, id_=file.handle, metadata=metadata)
                        for b in file.blocks
                    ]
                )

        return docs

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/steamship/#llama_index.readers.steamship.SteamshipFileReader.load_data "Permanent link")

```
load_data(
    workspace: ,
    query: Optional[] = None,
    file_handles: Optional[[]] = None,
    collapse_blocks:  = True,
    join_str:  = "\n\n",
) -> []

```

Load data from persistent Steamship Files into Documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `workspace`  |  the handle for a Steamship workspace (see: https://docs.steamship.com/workspaces/index.html)  |  _required_  |  
|  `query`  |  `Optional[str]`  |  a Steamship tag query for retrieving files (ex: 'filetag and value("import-id")="import-001"')  |  `None`  |  
|  `file_handles`  |  `Optional[List[str]]`  |  a list of Steamship File handles (ex: `smooth-valley-9kbdr`)  |  `None`  |  
|  `collapse_blocks`  |  `bool`  |  whether to merge individual File Blocks into a single Document, or separate them.  |  `True`  |  
|  `join_str`  |  when collapse_blocks is True, this is how the block texts will be concatenated.  |  `'\n\n'`  |  
Note
The collection of Files from both `query` and `file_handles` will be combined. There is no (current) support for deconflicting the collections (meaning that if a file appears both in the result set of the query and as a handle in file_handles, it will be loaded twice).
Source code in `llama-index-integrations/readers/llama-index-readers-steamship/llama_index/readers/steamship/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    workspace: str,
    query: Optional[str] = None,
    file_handles: Optional[List[str]] = None,
    collapse_blocks: bool = True,
    join_str: str = "\n\n",
) -> List[Document]:
"""
    Load data from persistent Steamship Files into Documents.

    Args:
        workspace: the handle for a Steamship workspace
            (see: https://docs.steamship.com/workspaces/index.html)
        query: a Steamship tag query for retrieving files
            (ex: 'filetag and value("import-id")="import-001"')
        file_handles: a list of Steamship File handles
            (ex: `smooth-valley-9kbdr`)
        collapse_blocks: whether to merge individual File Blocks into a
            single Document, or separate them.
        join_str: when collapse_blocks is True, this is how the block texts
            will be concatenated.

    Note:
        The collection of Files from both `query` and `file_handles` will be
        combined. There is no (current) support for deconflicting the collections
        (meaning that if a file appears both in the result set of the query and
        as a handle in file_handles, it will be loaded twice).

    """
    fromsteamshipimport File, Steamship

    client = Steamship(workspace=workspace, api_key=self.api_key)
    files = []
    if query:
        files_from_query = File.query(client=client, tag_filter_query=query).files
        files.extend(files_from_query)

    if file_handles:
        files.extend([File.get(client=client, handle=h) for h in file_handles])

    docs = []
    for file in files:
        metadata = {"source": file.handle}

        for tag in file.tags:
            metadata[tag.kind] = tag.value

        if collapse_blocks:
            text = join_str.join([b.text for b in file.blocks])
            docs.append(Document(text=text, id_=file.handle, metadata=metadata))
        else:
            docs.extend(
                [
                    Document(text=b.text, id_=file.handle, metadata=metadata)
                    for b in file.blocks
                ]
            )

    return docs

```
 |  
| --- | --- |  
options: members: - SteamshipFileReader
