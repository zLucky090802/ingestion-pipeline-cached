# Box
##  BoxReaderBase [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/box/#llama_index.readers.box.BoxReaderBase "Permanent link")
Bases: , , 
Source code in `llama-index-integrations/readers/llama-index-readers-box/llama_index/readers/box/BoxReader/base.py`  
| 
```
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
```
 | 
```
classBoxReaderBase(BaseReader, ResourcesReaderMixin, FileSystemReaderMixin):
    _box_client: BoxClient

    @classmethod
    defclass_name(cls) -> str:
        return "BoxReader"

    def__init__(
        self,
        box_client: BoxClient,
    ):
        self._box_client = add_extra_header_to_box_client(box_client)

    @abstractmethod
    defload_data(
        self,
        *args,
        **kwargs,
    ) -> List[Document]:
        pass

    defload_resource(self, box_file_id: str) -> List[Document]:
"""
        Load data from a specific resource.

        Args:
            resource (str): The resource identifier.

        Returns:
            List[Document]: A list of documents loaded from the resource.

        """
        return self.load_data(file_ids=[box_file_id])

    defget_resource_info(self, box_file_id: str) -> Dict:
"""
        Get information about a specific resource.

        Args:
            resource_id (str): The resource identifier.

        Returns:
            Dict: A dictionary of information about the resource.

        """
        # Connect to Box
        box_check_connection(self._box_client)

        resource = get_box_files_details(
            box_client=self._box_client, file_ids=[box_file_id]
        )

        return resource[0].to_dict()

    deflist_resources(
        self,
        folder_id: Optional[str] = None,
        file_ids: Optional[List[str]] = None,
        is_recursive: bool = False,
    ) -> List[str]:
"""
        Lists the IDs of Box files based on the specified folder or file IDs.

        This method retrieves a list of Box file identifiers based on the provided
        parameters. You can either specify a list of file IDs or a folder ID with an
        optional `is_recursive` flag to include files from sub-folders as well.

        Args:
            folder_id (Optional[str], optional): The ID of the Box folder to list files
                from. If provided, along with `is_recursive` set to True, retrieves data
                from sub-folders as well. Defaults to None.
            file_ids (Optional[List[str]], optional): A list of Box file IDs to retrieve.
                If provided, this takes precedence over `folder_id`. Defaults to None.
            is_recursive (bool, optional): If True and `folder_id` is provided, retrieves
                resource IDs from sub-folders within the specified folder. Defaults to False.

        Returns:
            List[str]: A list containing the IDs of the retrieved Box files.

        """
        # Connect to Box
        box_check_connection(self._box_client)

        # Get the file resources
        box_files: List[File] = []
        if file_ids is not None:
            box_files.extend(
                get_box_files_details(box_client=self._box_client, file_ids=file_ids)
            )
        elif folder_id is not None:
            box_files.extend(
                get_box_folder_files_details(
                    box_client=self._box_client,
                    folder_id=folder_id,
                    is_recursive=is_recursive,
                )
            )
        return [file.id for file in box_files]

    defread_file_content(self, input_file: Path, **kwargs) -> bytes:
        file_id = input_file.name
        return get_file_content_by_id(box_client=self._box_client, box_file_id=file_id)

    defsearch_resources(
        self,
        query: Optional[str] = None,
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
    ) -> List[str]:
"""
        Searches for Box resources based on specified criteria and returns a list of their IDs.

        This method utilizes the Box API search functionality to find resources
        matching the provided parameters. It then returns a list containing the IDs
        of the found resources.

        Args:
            query (Optional[str], optional): A search query string. Defaults to None.
            scope (Optional[SearchForContentScope], optional): The scope of the search.
                Defaults to None.
            file_extensions (Optional[List[str]], optional): A list of file extensions
                to filter by. Defaults to None.
            created_at_range (Optional[List[str]], optional): A list representing a date
                range for file creation time. Defaults to None.
            updated_at_range (Optional[List[str]], optional): A list representing a date
                range for file update time. Defaults to None.
            size_range (Optional[List[int]], optional): A list representing a size range
                for files. Defaults to None.
            owner_user_ids (Optional[List[str]], optional): A list of user IDs to filter
                by owner. Defaults to None.
            recent_updater_user_ids (Optional[List[str]], optional): A list of user IDs to
                filter by recent updater. Defaults to None.
            ancestor_folder_ids (Optional[List[str]], optional): A list of folder IDs to
                search within. Defaults to None.
            content_types (Optional[List[SearchForContentContentTypes]], optional): A list
                of content types to filter by. Defaults to None.
            limit (Optional[int], optional): The maximum number of results to return.
                Defaults to None.
            offset (Optional[int], optional): The number of results to skip before
                starting to collect. Defaults to None.

        Returns:
            List[str]: A list of Box resource IDs matching the search criteria.

        """
        # Connect to Box
        box_check_connection(self._box_client)

        box_files = search_files(
            box_client=self._box_client,
            query=query,
            scope=scope,
            file_extensions=file_extensions,
            created_at_range=created_at_range,
            updated_at_range=updated_at_range,
            size_range=size_range,
            owner_user_ids=owner_user_ids,
            recent_updater_user_ids=recent_updater_user_ids,
            ancestor_folder_ids=ancestor_folder_ids,
            content_types=content_types,
            limit=limit,
            offset=offset,
        )
        return [box_file.id for box_file in box_files]

    defsearch_resources_by_metadata(
        self,
        from_: str,
        ancestor_folder_id: str,
        query: Optional[str] = None,
        query_params: Optional[Dict[str, str]] = None,
        limit: Optional[int] = None,
        marker: Optional[str] = None,
    ) -> List[str]:
"""
        Searches for Box resources based on metadata and returns a list of their IDs.

        This method utilizes the Box API search functionality to find resources
        matching the provided metadata query. It then returns a list containing the IDs
        of the found resources.

        Args:
            box_client (BoxClient): An authenticated Box client object used
                for interacting with the Box API.
            from_ (str): The metadata template key to search from.
            ancestor_folder_id (str): The ID of the Box folder to search within.
            query (Optional[str], optional): A search query string. Defaults to None.
            query_params (Optional[Dict[str, str]], optional): Additional query parameters
                to filter the search results. Defaults to None.
            limit (Optional[int], optional): The maximum number of results to return.
                Defaults to None.
            marker (Optional[str], optional): The marker for the start of the next page of
                results. Defaults to None.

        Returns:
            List[str]: A list of Box resource IDs matching the search criteria.

        """
        # Connect to Box
        box_check_connection(self._box_client)

        box_files = search_files_by_metadata(
            box_client=self._box_client,
            from_=from_,
            ancestor_folder_id=ancestor_folder_id,
            query=query,
            query_params=query_params,
            limit=limit,
            marker=marker,
        )
        return [box_file.id for box_file in box_files]

```
 |  
| --- | --- |  
###  load_resource [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/box/#llama_index.readers.box.BoxReaderBase.load_resource "Permanent link")

```
load_resource(box_file_id: ) -> []

```

Load data from a specific resource.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `resource`  |  The resource identifier.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents loaded from the resource.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-box/llama_index/readers/box/BoxReader/base.py`  
| 
```
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
```
 | 
```
defload_resource(self, box_file_id: str) -> List[Document]:
"""
    Load data from a specific resource.

    Args:
        resource (str): The resource identifier.

    Returns:
        List[Document]: A list of documents loaded from the resource.

    """
    return self.load_data(file_ids=[box_file_id])

```
 |  
| --- | --- |  
###  get_resource_info [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/box/#llama_index.readers.box.BoxReaderBase.get_resource_info "Permanent link")

```
get_resource_info(box_file_id: ) -> 

```

Get information about a specific resource.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `resource_id`  |  The resource identifier.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Dict`  |  `Dict`  |  A dictionary of information about the resource.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-box/llama_index/readers/box/BoxReader/base.py`  
| 
```
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
```
 | 
```
defget_resource_info(self, box_file_id: str) -> Dict:
"""
    Get information about a specific resource.

    Args:
        resource_id (str): The resource identifier.

    Returns:
        Dict: A dictionary of information about the resource.

    """
    # Connect to Box
    box_check_connection(self._box_client)

    resource = get_box_files_details(
        box_client=self._box_client, file_ids=[box_file_id]
    )

    return resource[0].to_dict()

```
 |  
| --- | --- |  
###  list_resources [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/box/#llama_index.readers.box.BoxReaderBase.list_resources "Permanent link")

```
list_resources(
    folder_id: Optional[] = None,
    file_ids: Optional[[]] = None,
    is_recursive:  = False,
) -> []

```

Lists the IDs of Box files based on the specified folder or file IDs.
This method retrieves a list of Box file identifiers based on the provided parameters. You can either specify a list of file IDs or a folder ID with an optional `is_recursive` flag to include files from sub-folders as well.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `folder_id`  |  `Optional[str]`  |  The ID of the Box folder to list files from. If provided, along with `is_recursive` set to True, retrieves data from sub-folders as well. Defaults to None.  |  `None`  |  
|  `file_ids`  |  `Optional[List[str]]`  |  A list of Box file IDs to retrieve. If provided, this takes precedence over `folder_id`. Defaults to None.  |  `None`  |  
|  `is_recursive`  |  `bool`  |  If True and `folder_id` is provided, retrieves resource IDs from sub-folders within the specified folder. Defaults to False.  |  `False`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: A list containing the IDs of the retrieved Box files.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-box/llama_index/readers/box/BoxReader/base.py`  
| 
```
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
```
 | 
```
deflist_resources(
    self,
    folder_id: Optional[str] = None,
    file_ids: Optional[List[str]] = None,
    is_recursive: bool = False,
) -> List[str]:
"""
    Lists the IDs of Box files based on the specified folder or file IDs.

    This method retrieves a list of Box file identifiers based on the provided
    parameters. You can either specify a list of file IDs or a folder ID with an
    optional `is_recursive` flag to include files from sub-folders as well.

    Args:
        folder_id (Optional[str], optional): The ID of the Box folder to list files
            from. If provided, along with `is_recursive` set to True, retrieves data
            from sub-folders as well. Defaults to None.
        file_ids (Optional[List[str]], optional): A list of Box file IDs to retrieve.
            If provided, this takes precedence over `folder_id`. Defaults to None.
        is_recursive (bool, optional): If True and `folder_id` is provided, retrieves
            resource IDs from sub-folders within the specified folder. Defaults to False.

    Returns:
        List[str]: A list containing the IDs of the retrieved Box files.

    """
    # Connect to Box
    box_check_connection(self._box_client)

    # Get the file resources
    box_files: List[File] = []
    if file_ids is not None:
        box_files.extend(
            get_box_files_details(box_client=self._box_client, file_ids=file_ids)
        )
    elif folder_id is not None:
        box_files.extend(
            get_box_folder_files_details(
                box_client=self._box_client,
                folder_id=folder_id,
                is_recursive=is_recursive,
            )
        )
    return [file.id for file in box_files]

```
 |  
| --- | --- |  
###  search_resources [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/box/#llama_index.readers.box.BoxReaderBase.search_resources "Permanent link")

```
search_resources(
    query: Optional[] = None,
    scope: Optional[SearchForContentScope] = None,
    file_extensions: Optional[[]] = None,
    created_at_range: Optional[[]] = None,
    updated_at_range: Optional[[]] = None,
    size_range: Optional[[]] = None,
    owner_user_ids: Optional[[]] = None,
    recent_updater_user_ids: Optional[[]] = None,
    ancestor_folder_ids: Optional[[]] = None,
    content_types: Optional[
        [SearchForContentContentTypes]
    ] = None,
    limit: Optional[] = None,
    offset: Optional[] = None,
) -> []

```

Searches for Box resources based on specified criteria and returns a list of their IDs.
This method utilizes the Box API search functionality to find resources matching the provided parameters. It then returns a list containing the IDs of the found resources.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  `Optional[str]`  |  A search query string. Defaults to None.  |  `None`  |  
|  `scope`  |  `Optional[SearchForContentScope]`  |  The scope of the search. Defaults to None.  |  `None`  |  
|  `file_extensions`  |  `Optional[List[str]]`  |  A list of file extensions to filter by. Defaults to None.  |  `None`  |  
|  `created_at_range`  |  `Optional[List[str]]`  |  A list representing a date range for file creation time. Defaults to None.  |  `None`  |  
|  `updated_at_range`  |  `Optional[List[str]]`  |  A list representing a date range for file update time. Defaults to None.  |  `None`  |  
|  `size_range`  |  `Optional[List[int]]`  |  A list representing a size range for files. Defaults to None.  |  `None`  |  
|  `owner_user_ids`  |  `Optional[List[str]]`  |  A list of user IDs to filter by owner. Defaults to None.  |  `None`  |  
|  `recent_updater_user_ids`  |  `Optional[List[str]]`  |  A list of user IDs to filter by recent updater. Defaults to None.  |  `None`  |  
|  `ancestor_folder_ids`  |  `Optional[List[str]]`  |  A list of folder IDs to search within. Defaults to None.  |  `None`  |  
|  `content_types`  |  `Optional[List[SearchForContentContentTypes]]`  |  A list of content types to filter by. Defaults to None.  |  `None`  |  
|  `limit`  |  `Optional[int]`  |  The maximum number of results to return. Defaults to None.  |  `None`  |  
|  `offset`  |  `Optional[int]`  |  The number of results to skip before starting to collect. Defaults to None.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: A list of Box resource IDs matching the search criteria.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-box/llama_index/readers/box/BoxReader/base.py`  
| 
```
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
```
 | 
```
defsearch_resources(
    self,
    query: Optional[str] = None,
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
) -> List[str]:
"""
    Searches for Box resources based on specified criteria and returns a list of their IDs.

    This method utilizes the Box API search functionality to find resources
    matching the provided parameters. It then returns a list containing the IDs
    of the found resources.

    Args:
        query (Optional[str], optional): A search query string. Defaults to None.
        scope (Optional[SearchForContentScope], optional): The scope of the search.
            Defaults to None.
        file_extensions (Optional[List[str]], optional): A list of file extensions
            to filter by. Defaults to None.
        created_at_range (Optional[List[str]], optional): A list representing a date
            range for file creation time. Defaults to None.
        updated_at_range (Optional[List[str]], optional): A list representing a date
            range for file update time. Defaults to None.
        size_range (Optional[List[int]], optional): A list representing a size range
            for files. Defaults to None.
        owner_user_ids (Optional[List[str]], optional): A list of user IDs to filter
            by owner. Defaults to None.
        recent_updater_user_ids (Optional[List[str]], optional): A list of user IDs to
            filter by recent updater. Defaults to None.
        ancestor_folder_ids (Optional[List[str]], optional): A list of folder IDs to
            search within. Defaults to None.
        content_types (Optional[List[SearchForContentContentTypes]], optional): A list
            of content types to filter by. Defaults to None.
        limit (Optional[int], optional): The maximum number of results to return.
            Defaults to None.
        offset (Optional[int], optional): The number of results to skip before
            starting to collect. Defaults to None.

    Returns:
        List[str]: A list of Box resource IDs matching the search criteria.

    """
    # Connect to Box
    box_check_connection(self._box_client)

    box_files = search_files(
        box_client=self._box_client,
        query=query,
        scope=scope,
        file_extensions=file_extensions,
        created_at_range=created_at_range,
        updated_at_range=updated_at_range,
        size_range=size_range,
        owner_user_ids=owner_user_ids,
        recent_updater_user_ids=recent_updater_user_ids,
        ancestor_folder_ids=ancestor_folder_ids,
        content_types=content_types,
        limit=limit,
        offset=offset,
    )
    return [box_file.id for box_file in box_files]

```
 |  
| --- | --- |  
###  search_resources_by_metadata [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/box/#llama_index.readers.box.BoxReaderBase.search_resources_by_metadata "Permanent link")

```
search_resources_by_metadata(
    from_: ,
    ancestor_folder_id: ,
    query: Optional[] = None,
    query_params: Optional[[, ]] = None,
    limit: Optional[] = None,
    marker: Optional[] = None,
) -> []

```

Searches for Box resources based on metadata and returns a list of their IDs.
This method utilizes the Box API search functionality to find resources matching the provided metadata query. It then returns a list containing the IDs of the found resources.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `box_client`  |  `BoxClient`  |  An authenticated Box client object used for interacting with the Box API.  |  _required_  |  
|  `from_`  |  The metadata template key to search from.  |  _required_  |  
|  `ancestor_folder_id`  |  The ID of the Box folder to search within.  |  _required_  |  
|  `query`  |  `Optional[str]`  |  A search query string. Defaults to None.  |  `None`  |  
|  `query_params`  |  `Optional[Dict[str, str]]`  |  Additional query parameters to filter the search results. Defaults to None.  |  `None`  |  
|  `limit`  |  `Optional[int]`  |  The maximum number of results to return. Defaults to None.  |  `None`  |  
|  `marker`  |  `Optional[str]`  |  The marker for the start of the next page of results. Defaults to None.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: A list of Box resource IDs matching the search criteria.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-box/llama_index/readers/box/BoxReader/base.py`  
| 
```
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
```
 | 
```
defsearch_resources_by_metadata(
    self,
    from_: str,
    ancestor_folder_id: str,
    query: Optional[str] = None,
    query_params: Optional[Dict[str, str]] = None,
    limit: Optional[int] = None,
    marker: Optional[str] = None,
) -> List[str]:
"""
    Searches for Box resources based on metadata and returns a list of their IDs.

    This method utilizes the Box API search functionality to find resources
    matching the provided metadata query. It then returns a list containing the IDs
    of the found resources.

    Args:
        box_client (BoxClient): An authenticated Box client object used
            for interacting with the Box API.
        from_ (str): The metadata template key to search from.
        ancestor_folder_id (str): The ID of the Box folder to search within.
        query (Optional[str], optional): A search query string. Defaults to None.
        query_params (Optional[Dict[str, str]], optional): Additional query parameters
            to filter the search results. Defaults to None.
        limit (Optional[int], optional): The maximum number of results to return.
            Defaults to None.
        marker (Optional[str], optional): The marker for the start of the next page of
            results. Defaults to None.

    Returns:
        List[str]: A list of Box resource IDs matching the search criteria.

    """
    # Connect to Box
    box_check_connection(self._box_client)

    box_files = search_files_by_metadata(
        box_client=self._box_client,
        from_=from_,
        ancestor_folder_id=ancestor_folder_id,
        query=query,
        query_params=query_params,
        limit=limit,
        marker=marker,
    )
    return [box_file.id for box_file in box_files]

```
 |  
| --- | --- |  
##  BoxReaderAIExtract [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/box/#llama_index.readers.box.BoxReaderAIExtract "Permanent link")
Bases: 
A reader class for loading data from Box files using Box AI Extract.
This class inherits from the `BaseReader` class and specializes in processing data from Box files using Box AI Extract. It utilizes the provided BoxClient object to interact with the Box API and extracts data based on a specified AI prompt.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `_box_client`  |  `BoxClient`  |  An authenticated Box client object used for interacting with the Box API.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-box/llama_index/readers/box/BoxReaderAIExtraction/base.py`  
| 
```
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
```
 | 
```
classBoxReaderAIExtract(BoxReaderBase):
"""
    A reader class for loading data from Box files using Box AI Extract.

    This class inherits from the `BaseReader` class and specializes in
    processing data from Box files using Box AI Extract. It utilizes the
    provided BoxClient object to interact with the Box API and extracts
    data based on a specified AI prompt.

    Attributes:
        _box_client (BoxClient): An authenticated Box client object used
            for interacting with the Box API.

    """

    _box_client: BoxClient

    @classmethod
    defclass_name(cls) -> str:
        return "BoxReaderAIExtract"

    def__init__(self, box_client: BoxClient):
        super().__init__(box_client=box_client)

    defload_data(
        self,
        ai_prompt: str,
        file_ids: Optional[List[str]] = None,
        folder_id: Optional[str] = None,
        is_recursive: bool = False,
    ) -> List[Document]:
"""
        Extracts data from Box files using Box AI and creates Document objects.

        This method utilizes the Box AI Extract functionality to extract data
        based on the provided AI prompt from the specified Box files. It then
        creates Document objects containing the extracted data along with
        file metadata.

        Args:
            ai_prompt (str): The AI prompt that specifies what data to extract
                from the files.
            file_ids (Optional[List[str]], optional): A list of Box file IDs
                to extract data from. If provided, folder_id is ignored.
                Defaults to None.
            folder_id (Optional[str], optional): The ID of the Box folder to
                extract data from. If provided, along with is_recursive set to
                True, retrieves data from sub-folders as well. Defaults to None.
            is_recursive (bool, optional): If True and folder_id is provided,
                extracts data from sub-folders within the specified folder.
                Defaults to False.

        Returns:
            List[Document]: A list of Document objects containing the extracted
                data and file metadata.

        """
        # check if the box client is authenticated
        box_check_connection(self._box_client)

        docs: List[Document] = []
        box_files: List[File] = []

        # get payload information
        if file_ids is not None:
            box_files.extend(
                get_box_files_details(box_client=self._box_client, file_ids=file_ids)
            )
        elif folder_id is not None:
            box_files.extend(
                get_box_folder_files_details(
                    box_client=self._box_client,
                    folder_id=folder_id,
                    is_recursive=is_recursive,
                )
            )

        box_files = get_files_ai_extract_data(
            box_client=self._box_client,
            box_files=box_files,
            ai_prompt=ai_prompt,
        )

        for file in box_files:
            doc = box_file_to_llama_document(file)
            doc.text = file.ai_response if file.ai_response else ""
            doc.metadata["ai_prompt"] = file.ai_prompt
            doc.metadata["ai_response"] = file.ai_response
            docs.append(doc)
        return docs

    defload_resource(self, box_file_id: str, ai_prompt: str) -> List[Document]:
"""
        Load data from a specific resource.

        Args:
            resource (str): The resource identifier.

        Returns:
            List[Document]: A list of documents loaded from the resource.

        """
        return self.load_data(file_ids=[box_file_id], ai_prompt=ai_prompt)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/box/#llama_index.readers.box.BoxReaderAIExtract.load_data "Permanent link")

```
load_data(
    ai_prompt: ,
    file_ids: Optional[[]] = None,
    folder_id: Optional[] = None,
    is_recursive:  = False,
) -> []

```

Extracts data from Box files using Box AI and creates Document objects.
This method utilizes the Box AI Extract functionality to extract data based on the provided AI prompt from the specified Box files. It then creates Document objects containing the extracted data along with file metadata.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ai_prompt`  |  The AI prompt that specifies what data to extract from the files.  |  _required_  |  
|  `file_ids`  |  `Optional[List[str]]`  |  A list of Box file IDs to extract data from. If provided, folder_id is ignored. Defaults to None.  |  `None`  |  
|  `folder_id`  |  `Optional[str]`  |  The ID of the Box folder to extract data from. If provided, along with is_recursive set to True, retrieves data from sub-folders as well. Defaults to None.  |  `None`  |  
|  `is_recursive`  |  `bool`  |  If True and folder_id is provided, extracts data from sub-folders within the specified folder. Defaults to False.  |  `False`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of Document objects containing the extracted data and file metadata.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-box/llama_index/readers/box/BoxReaderAIExtraction/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    ai_prompt: str,
    file_ids: Optional[List[str]] = None,
    folder_id: Optional[str] = None,
    is_recursive: bool = False,
) -> List[Document]:
"""
    Extracts data from Box files using Box AI and creates Document objects.

    This method utilizes the Box AI Extract functionality to extract data
    based on the provided AI prompt from the specified Box files. It then
    creates Document objects containing the extracted data along with
    file metadata.

    Args:
        ai_prompt (str): The AI prompt that specifies what data to extract
            from the files.
        file_ids (Optional[List[str]], optional): A list of Box file IDs
            to extract data from. If provided, folder_id is ignored.
            Defaults to None.
        folder_id (Optional[str], optional): The ID of the Box folder to
            extract data from. If provided, along with is_recursive set to
            True, retrieves data from sub-folders as well. Defaults to None.
        is_recursive (bool, optional): If True and folder_id is provided,
            extracts data from sub-folders within the specified folder.
            Defaults to False.

    Returns:
        List[Document]: A list of Document objects containing the extracted
            data and file metadata.

    """
    # check if the box client is authenticated
    box_check_connection(self._box_client)

    docs: List[Document] = []
    box_files: List[File] = []

    # get payload information
    if file_ids is not None:
        box_files.extend(
            get_box_files_details(box_client=self._box_client, file_ids=file_ids)
        )
    elif folder_id is not None:
        box_files.extend(
            get_box_folder_files_details(
                box_client=self._box_client,
                folder_id=folder_id,
                is_recursive=is_recursive,
            )
        )

    box_files = get_files_ai_extract_data(
        box_client=self._box_client,
        box_files=box_files,
        ai_prompt=ai_prompt,
    )

    for file in box_files:
        doc = box_file_to_llama_document(file)
        doc.text = file.ai_response if file.ai_response else ""
        doc.metadata["ai_prompt"] = file.ai_prompt
        doc.metadata["ai_response"] = file.ai_response
        docs.append(doc)
    return docs

```
 |  
| --- | --- |  
###  load_resource [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/box/#llama_index.readers.box.BoxReaderAIExtract.load_resource "Permanent link")

```
load_resource(
    box_file_id: , ai_prompt: 
) -> []

```

Load data from a specific resource.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `resource`  |  The resource identifier.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents loaded from the resource.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-box/llama_index/readers/box/BoxReaderAIExtraction/base.py`  
| 
```
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
```
 | 
```
defload_resource(self, box_file_id: str, ai_prompt: str) -> List[Document]:
"""
    Load data from a specific resource.

    Args:
        resource (str): The resource identifier.

    Returns:
        List[Document]: A list of documents loaded from the resource.

    """
    return self.load_data(file_ids=[box_file_id], ai_prompt=ai_prompt)

```
 |  
| --- | --- |  
options: members: - BoxReader - BoxReaderAIExtract - BoxReaderAIPrompt - BoxReaderTextExtraction
