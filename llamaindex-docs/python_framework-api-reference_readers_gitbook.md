# Gitbook
##  SimpleGitbookReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gitbook/#llama_index.readers.gitbook.SimpleGitbookReader "Permanent link")
Bases: 
Simple gitbook reader.
Convert each gitbook page into Document used by LlamaIndex.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_token`  |  Gitbook API Token.  |  _required_  |  
|  `api_url`  |  Gitbook API Endpoint.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-gitbook/llama_index/readers/gitbook/base.py`  
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
```
 | 
```
classSimpleGitbookReader(BaseReader):
"""
    Simple gitbook reader.

    Convert each gitbook page into Document used by LlamaIndex.

    Args:
        api_token (str): Gitbook API Token.
        api_url (str): Gitbook API Endpoint.

    """

    def__init__(self, api_token: str, api_url: str = None) -> None:
"""Initialize with parameters."""
        self.client = GitbookClient(api_token, api_url)

    defload_data(
        self,
        space_id: str,
        metadata_names: Optional[List[str]] = None,
        show_progress=False,
    ) -> List[Document]:
"""
        Load data from the input directory.

        Args:
            space_id (str): Gitbook space id
            metadata_names (Optional[List[str]]): names of the fields to be added
                to the metadata attribute of the Document.
                only 'path', 'title', 'description', 'parent' are available
                Defaults to None
            show_progress (bool, optional): Show progress bar. Defaults to False

        Returns:
            List[Document]: A list of documents.

        """
        if metadata_names:
            invalid_fields = set(metadata_names) - VALID_METADATA_FIELDS
            if invalid_fields:
                raise ValueError(
                    f"Invalid metadata fields: {', '.join(invalid_fields)}"
                )

        documents = []
        pages = self.client.list_pages(space_id)

        if show_progress:
            fromtqdmimport tqdm

            iterator = tqdm(pages, desc="Downloading pages")
        else:
            iterator = pages

        for page in iterator:
            id = page.get("id")
            content = self.client.get_page_markdown(space_id, id)
            if not content:
                print(f"Warning: No content found for page ID {id}. Skipping...")
                continue

            if metadata_names is None:
                documents.append(
                    Document(text=content, id_=id, metadata={"path": page.get("path")})
                )
            else:
                try:
                    metadata = {name: page.get(name) for name in metadata_names}
                except KeyError as err:
                    raise ValueError(
                        f"{err.args[0]} field is not available. Choose from {', '.join(VALID_METADATA_FIELDS)}"
                    ) fromerr
                documents.append(Document(text=content, id_=id, metadata=metadata))

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gitbook/#llama_index.readers.gitbook.SimpleGitbookReader.load_data "Permanent link")

```
load_data(
    space_id: ,
    metadata_names: Optional[[]] = None,
    show_progress=False,
) -> []

```

Load data from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `space_id`  |  Gitbook space id  |  _required_  |  
|  `metadata_names`  |  `Optional[List[str]]`  |  names of the fields to be added to the metadata attribute of the Document. only 'path', 'title', 'description', 'parent' are available Defaults to None  |  `None`  |  
|  `show_progress`  |  `bool`  |  Show progress bar. Defaults to False  |  `False`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-gitbook/llama_index/readers/gitbook/base.py`  
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
```
 | 
```
defload_data(
    self,
    space_id: str,
    metadata_names: Optional[List[str]] = None,
    show_progress=False,
) -> List[Document]:
"""
    Load data from the input directory.

    Args:
        space_id (str): Gitbook space id
        metadata_names (Optional[List[str]]): names of the fields to be added
            to the metadata attribute of the Document.
            only 'path', 'title', 'description', 'parent' are available
            Defaults to None
        show_progress (bool, optional): Show progress bar. Defaults to False

    Returns:
        List[Document]: A list of documents.

    """
    if metadata_names:
        invalid_fields = set(metadata_names) - VALID_METADATA_FIELDS
        if invalid_fields:
            raise ValueError(
                f"Invalid metadata fields: {', '.join(invalid_fields)}"
            )

    documents = []
    pages = self.client.list_pages(space_id)

    if show_progress:
        fromtqdmimport tqdm

        iterator = tqdm(pages, desc="Downloading pages")
    else:
        iterator = pages

    for page in iterator:
        id = page.get("id")
        content = self.client.get_page_markdown(space_id, id)
        if not content:
            print(f"Warning: No content found for page ID {id}. Skipping...")
            continue

        if metadata_names is None:
            documents.append(
                Document(text=content, id_=id, metadata={"path": page.get("path")})
            )
        else:
            try:
                metadata = {name: page.get(name) for name in metadata_names}
            except KeyError as err:
                raise ValueError(
                    f"{err.args[0]} field is not available. Choose from {', '.join(VALID_METADATA_FIELDS)}"
                ) fromerr
            documents.append(Document(text=content, id_=id, metadata=metadata))

    return documents

```
 |  
| --- | --- |  
options: members: - SimpleGitbookReader
