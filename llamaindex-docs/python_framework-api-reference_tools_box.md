# Box
##  BoxSearchToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/box/#llama_index.tools.box.BoxSearchToolSpec "Permanent link")
Bases: 
Provides functionalities for searching Box resources.
This class allows you to search for Box resources based on various criteria specified using the `BoxSearchOptions` class. It utilizes the Box API search functionality and returns a list of `Document` objects containing information about the found resources.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `spec_functions`  |  `list`  |  A list of supported functions (always "box_search").  |  
| `_box_client`  |  `BoxClient`  |  An instance of BoxClient for interacting with Box API.  |  
| `_options`  |   |  An instance of BoxSearchOptions containing search options.  |  
Methods:  
| Name  | Description  |  
| --- | --- |  
|   |  str) -> List[Document]: Performs a search for Box resources based on the provided query and configured search options. Returns a list of `Document` objects representing the found resources.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-box/llama_index/tools/box/search/base.py`  
| 
```
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
```
 | 
```
classBoxSearchToolSpec(BaseToolSpec):
"""
    Provides functionalities for searching Box resources.

    This class allows you to search for Box resources based on various criteria
    specified using the `BoxSearchOptions` class. It utilizes the Box API search
    functionality and returns a list of `Document` objects containing information
    about the found resources.

    Attributes:
        spec_functions (list): A list of supported functions (always "box_search").
        _box_client (BoxClient): An instance of BoxClient for interacting with Box API.
        _options (BoxSearchOptions): An instance of BoxSearchOptions containing search options.

    Methods:
        box_search(query: str) -> List[Document]:
            Performs a search for Box resources based on the provided query and configured
            search options. Returns a list of `Document` objects representing the found resources.

    """

    spec_functions = ["box_search"]

    _box_client: BoxClient
    _options: BoxSearchOptions

    def__init__(
        self, box_client: BoxClient, options: BoxSearchOptions = BoxSearchOptions()
    ) -> None:
"""
        Initializes a `BoxSearchToolSpec` instance.

        Args:
            box_client (BoxClient): An authenticated Box API client.
            options (BoxSearchOptions, optional): An instance of `BoxSearchOptions` containing search options.
                Defaults to `BoxSearchOptions()`.

        """
        self._box_client = add_extra_header_to_box_client(box_client)
        self._options = options

    defbox_search(
        self,
        query: str,
    ) -> List[Document]:
"""
        Searches for Box resources based on the provided query and configured search options.

        This method utilizes the Box API search functionality to find resources matching the provided
        query and search options specified in the `BoxSearchOptions` object. It returns a list of
        `Document` objects containing information about the found resources.

        Args:
            query (str): The search query to use for searching Box resources.

        Returns:
            List[Document]: A list of `Document` objects representing the found Box resources.

        """
        box_check_connection(self._box_client)

        box_files = search_files(
            box_client=self._box_client,
            query=query,
            scope=self._options.scope,
            file_extensions=self._options.file_extensions,
            created_at_range=self._options.created_at_range,
            updated_at_range=self._options.updated_at_range,
            size_range=self._options.size_range,
            owner_user_ids=self._options.owner_user_ids,
            recent_updater_user_ids=self._options.recent_updater_user_ids,
            ancestor_folder_ids=self._options.ancestor_folder_ids,
            content_types=self._options.content_types,
            limit=self._options.limit,
            offset=self._options.offset,
        )

        box_files = get_box_files_details(
            box_client=self._box_client, file_ids=[file.id for file in box_files]
        )

        docs: List[Document] = []

        for file in box_files:
            doc = box_file_to_llama_document(file)
            docs.append(doc)

        return docs

```
 |  
| --- | --- |  
###  box_search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/box/#llama_index.tools.box.BoxSearchToolSpec.box_search "Permanent link")

```
box_search(query: ) -> []

```

Searches for Box resources based on the provided query and configured search options.
This method utilizes the Box API search functionality to find resources matching the provided query and search options specified in the `BoxSearchOptions` object. It returns a list of `Document` objects containing information about the found resources.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The search query to use for searching Box resources.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of `Document` objects representing the found Box resources.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-box/llama_index/tools/box/search/base.py`  
| 
```
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
```
 | 
```
defbox_search(
    self,
    query: str,
) -> List[Document]:
"""
    Searches for Box resources based on the provided query and configured search options.

    This method utilizes the Box API search functionality to find resources matching the provided
    query and search options specified in the `BoxSearchOptions` object. It returns a list of
    `Document` objects containing information about the found resources.

    Args:
        query (str): The search query to use for searching Box resources.

    Returns:
        List[Document]: A list of `Document` objects representing the found Box resources.

    """
    box_check_connection(self._box_client)

    box_files = search_files(
        box_client=self._box_client,
        query=query,
        scope=self._options.scope,
        file_extensions=self._options.file_extensions,
        created_at_range=self._options.created_at_range,
        updated_at_range=self._options.updated_at_range,
        size_range=self._options.size_range,
        owner_user_ids=self._options.owner_user_ids,
        recent_updater_user_ids=self._options.recent_updater_user_ids,
        ancestor_folder_ids=self._options.ancestor_folder_ids,
        content_types=self._options.content_types,
        limit=self._options.limit,
        offset=self._options.offset,
    )

    box_files = get_box_files_details(
        box_client=self._box_client, file_ids=[file.id for file in box_files]
    )

    docs: List[Document] = []

    for file in box_files:
        doc = box_file_to_llama_document(file)
        docs.append(doc)

    return docs

```
 |  
| --- | --- |  
##  BoxSearchOptions [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/box/#llama_index.tools.box.BoxSearchOptions "Permanent link")
Represents options for searching Box resources.
This class provides a way to specify various criteria for filtering search results when using the `BoxSearchToolSpec` class. You can define parameters like search scope, file extensions, date ranges (created/updated at), size range, owner IDs, and more to refine your search.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `scope`  |  `Optional[SearchForContentScope]`  |  The scope of the search (e.g., all content, trashed content).  |  
| `file_extensions`  |  `Optional[List[str]]`  |  A list of file extensions to filter by.  |  
| `created_at_range`  |  `Optional[List[str]]`  |  A list representing a date range for file creation time (format: YYYY-MM-DD).  |  
| `updated_at_range`  |  `Optional[List[str]]`  |  A list representing a date range for file update time (format: YYYY-MM-DD).  |  
| `size_range`  |  `Optional[List[int]]`  |  A list representing a range for file size (in bytes).  |  
| `owner_user_ids`  |  `Optional[List[str]]`  |  A list of user IDs to filter by owner.  |  
| `recent_updater_user_ids`  |  `Optional[List[str]]`  |  A list of user IDs to filter by recent updater.  |  
| `ancestor_folder_ids`  |  `Optional[List[str]]`  |  A list of folder IDs to search within.  |  
| `content_types`  |  `Optional[List[SearchForContentContentTypes]]`  |  A list of content types to filter by.  |  
| `limit`  |  `Optional[int]`  |  The maximum number of search results to return.  |  
| `offset`  |  `Optional[int]`  |  The offset to start results from (for pagination).  |  
Source code in `llama-index-integrations/tools/llama-index-tools-box/llama_index/tools/box/search/base.py`  
| 
```
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
```
 | 
```
classBoxSearchOptions:
"""
    Represents options for searching Box resources.

    This class provides a way to specify various criteria for filtering search results
    when using the `BoxSearchToolSpec` class. You can define parameters like search
    scope, file extensions, date ranges (created/updated at), size range, owner IDs,
    and more to refine your search.

    Attributes:
        scope (Optional[SearchForContentScope]): The scope of the search (e.g., all
            content, trashed content).
        file_extensions (Optional[List[str]]): A list of file extensions to filter by.
        created_at_range (Optional[List[str]]): A list representing a date range for
            file creation time (format: YYYY-MM-DD).
        updated_at_range (Optional[List[str]]): A list representing a date range for
            file update time (format: YYYY-MM-DD).
        size_range (Optional[List[int]]): A list representing a range for file size (in bytes).
        owner_user_ids (Optional[List[str]]): A list of user IDs to filter by owner.
        recent_updater_user_ids (Optional[List[str]]): A list of user IDs to filter by
            recent updater.
        ancestor_folder_ids (Optional[List[str]]): A list of folder IDs to search within.
        content_types (Optional[List[SearchForContentContentTypes]]): A list of content
            types to filter by.
        limit (Optional[int]): The maximum number of search results to return.
        offset (Optional[int]): The offset to start results from (for pagination).

    """

    scope: Optional[SearchForContentScope] = None
    file_extensions: Optional[List[str]] = None
    created_at_range: Optional[List[str]] = None
    updated_at_range: Optional[List[str]] = None
    size_range: Optional[List[int]] = None
    owner_user_ids: Optional[List[str]] = None
    recent_updater_user_ids: Optional[List[str]] = None
    ancestor_folder_ids: Optional[List[str]] = None
    content_types: Optional[List[SearchForContentContentTypes]] = None
    limit: Optional[int] = None
    offset: Optional[int] = None

    def__init__(
        self,
        scope: Optional[SearchForContentScope] = None,
        file_extensions: Optional[List[str]] = None,
        created_at_range: Optional[List[str]] = None,
        updated_at_range: Optional[List[str]] = None,
        size_range: Optional[List[int]] = None,
        owner_user_ids: Optional[List[str]] = None,
        recent_updater_user_ids: Optional[List[str]] = None,
        ancestor_folder_ids: Optional[List[str]] = None,
        content_types: Optional[List[SearchForContentContentTypes]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> None:
        self.scope = scope
        self.file_extensions = file_extensions
        self.created_at_range = created_at_range
        self.updated_at_range = updated_at_range
        self.size_range = size_range
        self.owner_user_ids = owner_user_ids
        self.recent_updater_user_ids = recent_updater_user_ids
        self.ancestor_folder_ids = ancestor_folder_ids
        self.content_types = content_types
        self.limit = limit
        self.offset = offset

```
 |  
| --- | --- |  
##  BoxSearchByMetadataToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/box/#llama_index.tools.box.BoxSearchByMetadataToolSpec "Permanent link")
Bases: 
Provides functionalities for searching Box resources based on metadata.
This class allows you to search for Box resources based on metadata specified using the `BoxSearchByMetadataOptions` class. It utilizes the Box API search functionality and returns a list of `Document` objects containing information about the found resources.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `spec_functions`  |  `list`  |  A list of supported functions (always "search").  |  
| `_box_client`  |  `BoxClient`  |  An instance of BoxClient for interacting with Box API.  |  
| `_options`  |   |  An instance of BoxSearchByMetadataOptions containing search options.  |  
Methods:  
| Name  | Description  |  
| --- | --- |  
|   |  Optional[str] = None) -> List[Document]: Performs a search for Box resources based on the configured metadata options and optional query parameters. Returns a list of `Document` objects representing the found resources.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-box/llama_index/tools/box/search_by_metadata/base.py`  
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
```
 | 
```
classBoxSearchByMetadataToolSpec(BaseToolSpec):
"""
    Provides functionalities for searching Box resources based on metadata.

    This class allows you to search for Box resources based on metadata specified
    using the `BoxSearchByMetadataOptions` class. It utilizes the Box API search
    functionality and returns a list of `Document` objects containing information
    about the found resources.

    Attributes:
        spec_functions (list): A list of supported functions (always "search").
        _box_client (BoxClient): An instance of BoxClient for interacting with Box API.
        _options (BoxSearchByMetadataOptions): An instance of BoxSearchByMetadataOptions
            containing search options.

    Methods:
        search(query_params: Optional[str] = None) -> List[Document]:
            Performs a search for Box resources based on the configured metadata options
            and optional query parameters. Returns a list of `Document` objects representing
            the found resources.

    """

    spec_functions = ["search"]

    _box_client: BoxClient
    _options: BoxSearchByMetadataOptions

    def__init__(
        self, box_client: BoxClient, options: BoxSearchByMetadataOptions
    ) -> None:
"""
        Initializes a `BoxSearchByMetadataToolSpec` instance.

        Args:
            box_client (BoxClient): An authenticated Box API client.
            options (BoxSearchByMetadataToolSpec, optional): An instance of `BoxSearchByMetadataToolSpec` containing search options.
                Defaults to `BoxSearchByMetadataToolSpec()`.

        """
        self._box_client = add_extra_header_to_box_client(box_client)
        self._options = options

    defsearch(
        self,
        query_params: Optional[str] = None,
    ) -> List[Document]:
"""
        Searches for Box resources based on metadata and returns a list of documents.

        This method leverages the configured metadata options (`self._options`) to
        search for Box resources. It converts the provided JSON string (`query_params`)
        into a dictionary and uses it to refine the search based on additional
        metadata criteria. It retrieves matching Box files and then converts them
        into `Document` objects containing relevant information.

        Args:
            query_params (Optional[str]): An optional JSON string representing additional
                query parameters for filtering by metadata.

        Returns:
            List[Document]: A list of `Document` objects representing the found Box resources.

        """
        box_check_connection(self._box_client)

        # Box API accepts a dictionary of query parameters as a string, so we need to
        # convert the provided JSON string to a dictionary.
        params_dict = json.loads(query_params)

        box_files = search_files_by_metadata(
            box_client=self._box_client,
            from_=self._options.from_,
            ancestor_folder_id=self._options.ancestor_folder_id,
            query=self._options.query,
            query_params=params_dict,
            limit=self._options.limit,
        )

        box_files = get_box_files_details(
            box_client=self._box_client, file_ids=[file.id for file in box_files]
        )

        docs: List[Document] = []

        for file in box_files:
            doc = box_file_to_llama_document(file)
            docs.append(doc)

        return docs

```
 |  
| --- | --- |  
###  search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/box/#llama_index.tools.box.BoxSearchByMetadataToolSpec.search "Permanent link")

```
search(
    query_params: Optional[] = None,
) -> []

```

Searches for Box resources based on metadata and returns a list of documents.
This method leverages the configured metadata options (`self._options`) to search for Box resources. It converts the provided JSON string (`query_params`) into a dictionary and uses it to refine the search based on additional metadata criteria. It retrieves matching Box files and then converts them into `Document` objects containing relevant information.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_params`  |  `Optional[str]`  |  An optional JSON string representing additional query parameters for filtering by metadata.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of `Document` objects representing the found Box resources.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-box/llama_index/tools/box/search_by_metadata/base.py`  
| 
```
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
```
 | 
```
defsearch(
    self,
    query_params: Optional[str] = None,
) -> List[Document]:
"""
    Searches for Box resources based on metadata and returns a list of documents.

    This method leverages the configured metadata options (`self._options`) to
    search for Box resources. It converts the provided JSON string (`query_params`)
    into a dictionary and uses it to refine the search based on additional
    metadata criteria. It retrieves matching Box files and then converts them
    into `Document` objects containing relevant information.

    Args:
        query_params (Optional[str]): An optional JSON string representing additional
            query parameters for filtering by metadata.

    Returns:
        List[Document]: A list of `Document` objects representing the found Box resources.

    """
    box_check_connection(self._box_client)

    # Box API accepts a dictionary of query parameters as a string, so we need to
    # convert the provided JSON string to a dictionary.
    params_dict = json.loads(query_params)

    box_files = search_files_by_metadata(
        box_client=self._box_client,
        from_=self._options.from_,
        ancestor_folder_id=self._options.ancestor_folder_id,
        query=self._options.query,
        query_params=params_dict,
        limit=self._options.limit,
    )

    box_files = get_box_files_details(
        box_client=self._box_client, file_ids=[file.id for file in box_files]
    )

    docs: List[Document] = []

    for file in box_files:
        doc = box_file_to_llama_document(file)
        docs.append(doc)

    return docs

```
 |  
| --- | --- |  
##  BoxSearchByMetadataOptions [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/box/#llama_index.tools.box.BoxSearchByMetadataOptions "Permanent link")
Represents options for searching Box resources based on metadata.
This class provides a way to specify parameters for searching Box resources using metadata. You can define the starting point for the search (`from_`), the ancestor folder ID to search within (`ancestor_folder_id`), an optional search query (`query`), and a limit on the number of returned results (`limit`).
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `from_`  |  The starting point for the search, such as "folder" or "file".  |  
| `ancestor_folder_id`  |  The ID of the ancestor folder to search within.  |  
| `query`  |  `Optional[str]`  |  An optional search query string to refine the search based on metadata.  |  
| `limit`  |  `Optional[int]`  |  The maximum number of search results to return.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-box/llama_index/tools/box/search_by_metadata/base.py`  
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
```
 | 
```
classBoxSearchByMetadataOptions:
"""
    Represents options for searching Box resources based on metadata.

    This class provides a way to specify parameters for searching Box resources
    using metadata. You can define the starting point for the search (`from_`), the
    ancestor folder ID to search within (`ancestor_folder_id`), an optional search
    query (`query`), and a limit on the number of returned results (`limit`).

    Attributes:
        from_ (str): The starting point for the search, such as "folder" or "file".
        ancestor_folder_id (str): The ID of the ancestor folder to search within.
        query (Optional[str]): An optional search query string to refine the search
            based on metadata.
        limit (Optional[int]): The maximum number of search results to return.

    """

    from_: str
    ancestor_folder_id: str
    query: Optional[str] = (None,)
    limit: Optional[int] = None

    def__init__(
        self,
        from_: str,
        ancestor_folder_id: str,
        query: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> None:
        self.from_ = from_
        self.ancestor_folder_id = ancestor_folder_id
        self.query = query
        self.limit = limit

```
 |  
| --- | --- |  
##  BoxTextExtractToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/box/#llama_index.tools.box.BoxTextExtractToolSpec "Permanent link")
Bases: 
Box Text Extraction Tool Specification.
This class provides a specification for extracting text content from Box files and creating Document objects. It leverages the Box API to retrieve the text representation (if available) of specified Box files.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `_box_client`  |  `BoxClient`  |  An instance of the Box client for interacting with the Box API.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-box/llama_index/tools/box/text_extract/base.py`  
| 
```
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
```
 | 
```
classBoxTextExtractToolSpec(BaseToolSpec):
"""
    Box Text Extraction Tool Specification.

    This class provides a specification for extracting text content from Box files
    and creating Document objects. It leverages the Box API to retrieve the
    text representation (if available) of specified Box files.

    Attributes:
        _box_client (BoxClient): An instance of the Box client for interacting
            with the Box API.

    """

    spec_functions = ["extract"]
    _box_client: BoxClient

    def__init__(self, box_client: BoxClient) -> None:
"""
        Initializes the Box Text Extraction Tool Specification with the
        provided Box client instance.

        Args:
            box_client (BoxClient): The Box client instance.

        """
        self._box_client = add_extra_header_to_box_client(box_client)

    defextract(
        self,
        file_id: str,
    ) -> Document:
"""
        Extracts text content from Box files and creates Document objects.

        This method utilizes the Box API to retrieve the text representation
        (if available) of the specified Box files. It then creates Document
        objects containing the extracted text and file metadata.

        Args:
            file_id (str): A of Box file ID
                to extract text from.

        Returns:
            List[Document]: A list of Document objects containing the extracted
                text content and file metadata.

        """
        # Connect to Box
        box_check_connection(self._box_client)

        # get payload information
        box_file = get_box_files_details(
            box_client=self._box_client, file_ids=[file_id]
        )[0]

        box_file = get_text_representation(
            box_client=self._box_client,
            box_files=[box_file],
        )[0]

        doc = box_file_to_llama_document(box_file)
        doc.text = box_file.text_representation if box_file.text_representation else ""
        return doc

```
 |  
| --- | --- |  
###  extract [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/box/#llama_index.tools.box.BoxTextExtractToolSpec.extract "Permanent link")

```
extract(file_id: ) -> 

```

Extracts text content from Box files and creates Document objects.
This method utilizes the Box API to retrieve the text representation (if available) of the specified Box files. It then creates Document objects containing the extracted text and file metadata.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file_id`  |  A of Box file ID to extract text from.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of Document objects containing the extracted text content and file metadata.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-box/llama_index/tools/box/text_extract/base.py`  
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
```
 | 
```
defextract(
    self,
    file_id: str,
) -> Document:
"""
    Extracts text content from Box files and creates Document objects.

    This method utilizes the Box API to retrieve the text representation
    (if available) of the specified Box files. It then creates Document
    objects containing the extracted text and file metadata.

    Args:
        file_id (str): A of Box file ID
            to extract text from.

    Returns:
        List[Document]: A list of Document objects containing the extracted
            text content and file metadata.

    """
    # Connect to Box
    box_check_connection(self._box_client)

    # get payload information
    box_file = get_box_files_details(
        box_client=self._box_client, file_ids=[file_id]
    )[0]

    box_file = get_text_representation(
        box_client=self._box_client,
        box_files=[box_file],
    )[0]

    doc = box_file_to_llama_document(box_file)
    doc.text = box_file.text_representation if box_file.text_representation else ""
    return doc

```
 |  
| --- | --- |  
##  BoxAIPromptToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/box/#llama_index.tools.box.BoxAIPromptToolSpec "Permanent link")
Bases: 
Generates AI prompts based on a Box file.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `box_client`  |  `BoxClient`  |  A BoxClient instance for interacting with Box API.  |  _required_  |  
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `spec_functions`  |  `list`  |  A list of supported functions.  |  
| `_box_client`  |  `BoxClient`  |  An instance of BoxClient for interacting with Box API.  |  
Methods:  
| Name  | Description  |  
| --- | --- |  
|   |  Generates an AI prompt based on a Box file.  |  
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file_id`  |  The ID of the Box file.  |  _required_  |  
|  `ai_prompt`  |  The base AI prompt to use.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Document`  |  A Document object containing the generated AI prompt.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-box/llama_index/tools/box/ai_prompt/base.py`  
| 
```
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
classBoxAIPromptToolSpec(BaseToolSpec):
"""
    Generates AI prompts based on a Box file.

    Args:
        box_client (BoxClient): A BoxClient instance for interacting with Box API.

    Attributes:
        spec_functions (list): A list of supported functions.
        _box_client (BoxClient): An instance of BoxClient for interacting with Box API.

    Methods:
        ai_prompt(file_id, ai_prompt): Generates an AI prompt based on a Box file.

    Args:
        file_id (str): The ID of the Box file.
        ai_prompt (str): The base AI prompt to use.

    Returns:
        Document: A Document object containing the generated AI prompt.

    """

    spec_functions = ["ai_prompt"]

    _box_client: BoxClient

    def__init__(self, box_client: BoxClient) -> None:
"""
        Initializes the BoxAIPromptToolSpec with a BoxClient instance.

        Args:
            box_client (BoxClient): The BoxClient instance to use for interacting with the Box API.

        """
        self._box_client = add_extra_header_to_box_client(box_client)

    defai_prompt(
        self,
        file_id: str,
        ai_prompt: str,
    ) -> Document:
"""
        Generates an AI prompt based on a Box file.

        Retrieves the specified Box file, constructs an AI prompt using the provided base prompt,
        and returns a Document object containing the generated prompt and file metadata.

        Args:
            file_id (str): The ID of the Box file to process.
            ai_prompt (str): The base AI prompt to use as a template.

        Returns:
            Document: A Document object containing the generated AI prompt and file metadata.

        """
        # Connect to Box
        box_check_connection(self._box_client)

        # get box files information
        box_file = get_box_files_details(
            box_client=self._box_client, file_ids=[file_id]
        )[0]

        box_file = get_ai_response_from_box_files(
            box_client=self._box_client,
            box_files=[box_file],
            ai_prompt=ai_prompt,
        )[0]

        doc = box_file_to_llama_document(box_file)
        doc.text = box_file.ai_response if box_file.ai_response else ""
        doc.metadata["ai_prompt"] = box_file.ai_prompt
        doc.metadata["ai_response"] = (
            box_file.ai_response if box_file.ai_response else ""
        )

        return doc

```
 |  
| --- | --- |  
###  ai_prompt [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/box/#llama_index.tools.box.BoxAIPromptToolSpec.ai_prompt "Permanent link")

```
ai_prompt(file_id: , ai_prompt: ) -> 

```

Generates an AI prompt based on a Box file.
Retrieves the specified Box file, constructs an AI prompt using the provided base prompt, and returns a Document object containing the generated prompt and file metadata.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file_id`  |  The ID of the Box file to process.  |  _required_  |  
|  `ai_prompt`  |  The base AI prompt to use as a template.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Document`  |   |  A Document object containing the generated AI prompt and file metadata.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-box/llama_index/tools/box/ai_prompt/base.py`  
| 
```
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
defai_prompt(
    self,
    file_id: str,
    ai_prompt: str,
) -> Document:
"""
    Generates an AI prompt based on a Box file.

    Retrieves the specified Box file, constructs an AI prompt using the provided base prompt,
    and returns a Document object containing the generated prompt and file metadata.

    Args:
        file_id (str): The ID of the Box file to process.
        ai_prompt (str): The base AI prompt to use as a template.

    Returns:
        Document: A Document object containing the generated AI prompt and file metadata.

    """
    # Connect to Box
    box_check_connection(self._box_client)

    # get box files information
    box_file = get_box_files_details(
        box_client=self._box_client, file_ids=[file_id]
    )[0]

    box_file = get_ai_response_from_box_files(
        box_client=self._box_client,
        box_files=[box_file],
        ai_prompt=ai_prompt,
    )[0]

    doc = box_file_to_llama_document(box_file)
    doc.text = box_file.ai_response if box_file.ai_response else ""
    doc.metadata["ai_prompt"] = box_file.ai_prompt
    doc.metadata["ai_response"] = (
        box_file.ai_response if box_file.ai_response else ""
    )

    return doc

```
 |  
| --- | --- |  
##  BoxAIExtractToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/box/#llama_index.tools.box.BoxAIExtractToolSpec "Permanent link")
Bases: 
Extracts AI generated content from a Box file.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `box_client`  |  `BoxClient`  |  A BoxClient instance for interacting with Box API.  |  _required_  |  
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `spec_functions`  |  `list`  |  A list of supported functions.  |  
| `_box_client`  |  `BoxClient`  |  An instance of BoxClient for interacting with Box API.  |  
Methods:  
| Name  | Description  |  
| --- | --- |  
|   |  Extracts AI generated content from a Box file.  |  
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file_id`  |  The ID of the Box file.  |  _required_  |  
|  `ai_prompt`  |  The AI prompt to use for extraction.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Document`  |  A Document object containing the extracted AI content.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-box/llama_index/tools/box/ai_extract/base.py`  
| 
```
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
```
 | 
```
classBoxAIExtractToolSpec(BaseToolSpec):
"""
    Extracts AI generated content from a Box file.

    Args:
        box_client (BoxClient): A BoxClient instance for interacting with Box API.

    Attributes:
        spec_functions (list): A list of supported functions.
        _box_client (BoxClient): An instance of BoxClient for interacting with Box API.

    Methods:
        ai_extract(file_id, ai_prompt): Extracts AI generated content from a Box file.

    Args:
        file_id (str): The ID of the Box file.
        ai_prompt (str): The AI prompt to use for extraction.

    Returns:
        Document: A Document object containing the extracted AI content.

    """

    spec_functions = ["ai_extract"]

    _box_client: BoxClient

    def__init__(self, box_client: BoxClient) -> None:
"""
        Initializes the BoxAIExtractToolSpec with a BoxClient instance.

        Args:
            box_client (BoxClient): The BoxClient instance to use for interacting with the Box API.

        """
        self._box_client = add_extra_header_to_box_client(box_client)

    defai_extract(
        self,
        file_id: str,
        ai_prompt: str,
    ) -> Document:
"""
        Extracts AI generated content from a Box file using the provided AI prompt.

        Args:
            file_id (str): The ID of the Box file to process.
            ai_prompt (str): The AI prompt to use for content extraction.

        Returns:
            Document: A Document object containing the extracted AI content,
            including metadata about the original Box file.

        """
        # Connect to Box
        box_check_connection(self._box_client)

        # get payload information
        box_file = get_box_files_details(
            box_client=self._box_client, file_ids=[file_id]
        )[0]

        box_file = get_files_ai_extract_data(
            box_client=self._box_client,
            box_files=[box_file],
            ai_prompt=ai_prompt,
        )[0]

        doc = box_file_to_llama_document(box_file)
        doc.text = box_file.ai_response if box_file.ai_response else ""
        doc.metadata["ai_prompt"] = box_file.ai_prompt
        doc.metadata["ai_response"] = box_file.ai_response

        return doc

```
 |  
| --- | --- |  
###  ai_extract [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/box/#llama_index.tools.box.BoxAIExtractToolSpec.ai_extract "Permanent link")

```
ai_extract(file_id: , ai_prompt: ) -> 

```

Extracts AI generated content from a Box file using the provided AI prompt.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file_id`  |  The ID of the Box file to process.  |  _required_  |  
|  `ai_prompt`  |  The AI prompt to use for content extraction.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Document`  |   |  A Document object containing the extracted AI content,  |  
|   |  including metadata about the original Box file.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-box/llama_index/tools/box/ai_extract/base.py`  
| 
```
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
```
 | 
```
defai_extract(
    self,
    file_id: str,
    ai_prompt: str,
) -> Document:
"""
    Extracts AI generated content from a Box file using the provided AI prompt.

    Args:
        file_id (str): The ID of the Box file to process.
        ai_prompt (str): The AI prompt to use for content extraction.

    Returns:
        Document: A Document object containing the extracted AI content,
        including metadata about the original Box file.

    """
    # Connect to Box
    box_check_connection(self._box_client)

    # get payload information
    box_file = get_box_files_details(
        box_client=self._box_client, file_ids=[file_id]
    )[0]

    box_file = get_files_ai_extract_data(
        box_client=self._box_client,
        box_files=[box_file],
        ai_prompt=ai_prompt,
    )[0]

    doc = box_file_to_llama_document(box_file)
    doc.text = box_file.ai_response if box_file.ai_response else ""
    doc.metadata["ai_prompt"] = box_file.ai_prompt
    doc.metadata["ai_response"] = box_file.ai_response

    return doc

```
 |  
| --- | --- |  
options: members: - BoxAIExtractToolSpec - BoxAIPromptToolSpec - BoxSearchByMetadataToolSpec - BoxSearchToolSpec - BoxTextExtractToolSpec
