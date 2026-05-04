# Index
Base reader class.
##  BaseReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.BaseReader "Permanent link")
Bases: 
Utilities for loading data from a directory.
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
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
```
 | 
```
classBaseReader(ABC):  # pragma: no cover
"""Utilities for loading data from a directory."""

    deflazy_load_data(self, *args: Any, **load_kwargs: Any) -> Iterable[Document]:
"""Load data from the input directory lazily."""
        raise NotImplementedError(
            f"{self.__class__.__name__} does not provide lazy_load_data method currently"
        )

    async defalazy_load_data(
        self, *args: Any, **load_kwargs: Any
    ) -> Iterable[Document]:
"""Load data from the input directory lazily."""
        # Threaded async - just calls the sync method with to_thread. Override in subclasses for real async implementations.
        return await asyncio.to_thread(self.lazy_load_data, *args, **load_kwargs)

    defload_data(self, *args: Any, **load_kwargs: Any) -> List[Document]:
"""Load data from the input directory."""
        return list(self.lazy_load_data(*args, **load_kwargs))

    async defaload_data(self, *args: Any, **load_kwargs: Any) -> List[Document]:
"""Load data from the input directory."""
        return await asyncio.to_thread(self.load_data, *args, **load_kwargs)

    defload_langchain_documents(self, **load_kwargs: Any) -> List["LCDocument"]:
"""Load data in LangChain document format."""
        docs = self.load_data(**load_kwargs)
        return [d.to_langchain_format() for d in docs]

```
 |  
| --- | --- |  
###  lazy_load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.BaseReader.lazy_load_data "Permanent link")

```
lazy_load_data(
    *args: , **load_kwargs: 
) -> Iterable[]

```

Load data from the input directory lazily.
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
22
23
24
25
26
```
 | 
```
deflazy_load_data(self, *args: Any, **load_kwargs: Any) -> Iterable[Document]:
"""Load data from the input directory lazily."""
    raise NotImplementedError(
        f"{self.__class__.__name__} does not provide lazy_load_data method currently"
    )

```
 |  
| --- | --- |  
###  alazy_load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.BaseReader.alazy_load_data "Permanent link")

```
alazy_load_data(
    *args: , **load_kwargs: 
) -> Iterable[]

```

Load data from the input directory lazily.
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
28
29
30
31
32
33
```
 | 
```
async defalazy_load_data(
    self, *args: Any, **load_kwargs: Any
) -> Iterable[Document]:
"""Load data from the input directory lazily."""
    # Threaded async - just calls the sync method with to_thread. Override in subclasses for real async implementations.
    return await asyncio.to_thread(self.lazy_load_data, *args, **load_kwargs)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.BaseReader.load_data "Permanent link")

```
load_data(*args: , **load_kwargs: ) -> []

```

Load data from the input directory.
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
35
36
37
```
 | 
```
defload_data(self, *args: Any, **load_kwargs: Any) -> List[Document]:
"""Load data from the input directory."""
    return list(self.lazy_load_data(*args, **load_kwargs))

```
 |  
| --- | --- |  
###  aload_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.BaseReader.aload_data "Permanent link")

```
aload_data(
    *args: , **load_kwargs: 
) -> []

```

Load data from the input directory.
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
39
40
41
```
 | 
```
async defaload_data(self, *args: Any, **load_kwargs: Any) -> List[Document]:
"""Load data from the input directory."""
    return await asyncio.to_thread(self.load_data, *args, **load_kwargs)

```
 |  
| --- | --- |  
###  load_langchain_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.BaseReader.load_langchain_documents "Permanent link")

```
load_langchain_documents(
    **load_kwargs: ,
) -> [Document]

```

Load data in LangChain document format.
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
43
44
45
46
```
 | 
```
defload_langchain_documents(self, **load_kwargs: Any) -> List["LCDocument"]:
"""Load data in LangChain document format."""
    docs = self.load_data(**load_kwargs)
    return [d.to_langchain_format() for d in docs]

```
 |  
| --- | --- |  
##  BasePydanticReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.BasePydanticReader "Permanent link")
Bases: , 
Serialiable Data Loader with Pydantic.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `is_remote`  |  `bool`  |  Whether the data is loaded from a remote API or a local file.  |  `False`  |  
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
49
50
51
52
53
54
55
56
```
 | 
```
classBasePydanticReader(BaseReader, BaseComponent):
"""Serialiable Data Loader with Pydantic."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    is_remote: bool = Field(
        default=False,
        description="Whether the data is loaded from a remote API or a local file.",
    )

```
 |  
| --- | --- |  
##  ResourcesReaderMixin [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ResourcesReaderMixin "Permanent link")
Bases: 
Mixin for readers that provide access to different types of resources.
Resources refer to specific data entities that can be accessed by the reader. Examples of resources include files for a filesystem reader, channel IDs for a Slack reader, or pages for a Notion reader.
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
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
```
 | 
```
classResourcesReaderMixin(ABC):  # pragma: no cover
"""
    Mixin for readers that provide access to different types of resources.

    Resources refer to specific data entities that can be accessed by the reader.
    Examples of resources include files for a filesystem reader, channel IDs for a Slack reader, or pages for a Notion reader.
    """

    @abstractmethod
    deflist_resources(self, *args: Any, **kwargs: Any) -> List[str]:
"""
        List of identifiers for the specific type of resources available in the reader.

        Returns:
            List[str]: List of identifiers for the specific type of resources available in the reader.

        """

    async defalist_resources(self, *args: Any, **kwargs: Any) -> List[str]:
"""
        List of identifiers for the specific type of resources available in the reader asynchronously.

        Returns:
            List[str]: A list of resources based on the reader type, such as files for a filesystem reader,
            channel IDs for a Slack reader, or pages for a Notion reader.

        """
        return await asyncio.to_thread(self.list_resources, *args, **kwargs)

    defget_permission_info(self, resource_id: str, *args: Any, **kwargs: Any) -> Dict:
"""
        Get a dictionary of information about the permissions of a specific resource.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} does not provide get_permission_info method currently"
        )

    async defaget_permission_info(
        self, resource_id: str, *args: Any, **kwargs: Any
    ) -> Dict:
"""
        Get a dictionary of information about the permissions of a specific resource asynchronously.
        """
        return await asyncio.to_thread(
            self.get_permission_info, resource_id, *args, **kwargs
        )

    @abstractmethod
    defget_resource_info(self, resource_id: str, *args: Any, **kwargs: Any) -> Dict:
"""
        Get a dictionary of information about a specific resource.

        Args:
            resource (str): The resource identifier.

        Returns:
            Dict: A dictionary of information about the resource.

        """

    async defaget_resource_info(
        self, resource_id: str, *args: Any, **kwargs: Any
    ) -> Dict:
"""
        Get a dictionary of information about a specific resource asynchronously.

        Args:
            resource (str): The resource identifier.

        Returns:
            Dict: A dictionary of information about the resource.

        """
        return await asyncio.to_thread(
            self.get_resource_info, resource_id, *args, **kwargs
        )

    deflist_resources_with_info(self, *args: Any, **kwargs: Any) -> Dict[str, Dict]:
"""
        Get a dictionary of information about all resources.

        Returns:
            Dict[str, Dict]: A dictionary of information about all resources.

        """
        return {
            resource: self.get_resource_info(resource, *args, **kwargs)
            for resource in self.list_resources(*args, **kwargs)
        }

    async defalist_resources_with_info(
        self, *args: Any, **kwargs: Any
    ) -> Dict[str, Dict]:
"""
        Get a dictionary of information about all resources asynchronously.

        Returns:
            Dict[str, Dict]: A dictionary of information about all resources.

        """
        return {
            resource: await self.aget_resource_info(resource, *args, **kwargs)
            for resource in await self.alist_resources(*args, **kwargs)
        }

    @abstractmethod
    defload_resource(
        self, resource_id: str, *args: Any, **kwargs: Any
    ) -> List[Document]:
"""
        Load data from a specific resource.

        Args:
            resource (str): The resource identifier.

        Returns:
            List[Document]: A list of documents loaded from the resource.

        """

    async defaload_resource(
        self, resource_id: str, *args: Any, **kwargs: Any
    ) -> List[Document]:
"""Read file from filesystem and return documents asynchronously."""
        return await asyncio.to_thread(self.load_resource, resource_id, *args, **kwargs)

    defload_resources(
        self, resource_ids: List[str], *args: Any, **kwargs: Any
    ) -> List[Document]:
"""
        Similar to load_data, but only for specific resources.

        Args:
            resource_ids (List[str]): List of resource identifiers.

        Returns:
            List[Document]: A list of documents loaded from the resources.

        """
        return [
            doc
            for resource in resource_ids
            for doc in self.load_resource(resource, *args, **kwargs)
        ]

    async defaload_resources(
        self, resource_ids: List[str], *args: Any, **kwargs: Any
    ) -> Dict[str, List[Document]]:
"""
        Similar ato load_data, but only for specific resources.

        Args:
            resource_ids (List[str]): List of resource identifiers.

        Returns:
            Dict[str, List[Document]]: A dictionary of documents loaded from the resources.

        """
        return {
            resource: await self.aload_resource(resource, *args, **kwargs)
            for resource in resource_ids
        }

```
 |  
| --- | --- |  
###  list_resources `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ResourcesReaderMixin.list_resources "Permanent link")

```
list_resources(*args: , **kwargs: ) -> []

```

List of identifiers for the specific type of resources available in the reader.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: List of identifiers for the specific type of resources available in the reader.  |  
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
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
@abstractmethod
deflist_resources(self, *args: Any, **kwargs: Any) -> List[str]:
"""
    List of identifiers for the specific type of resources available in the reader.

    Returns:
        List[str]: List of identifiers for the specific type of resources available in the reader.

    """

```
 |  
| --- | --- |  
###  alist_resources [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ResourcesReaderMixin.alist_resources "Permanent link")

```
alist_resources(*args: , **kwargs: ) -> []

```

List of identifiers for the specific type of resources available in the reader asynchronously.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: A list of resources based on the reader type, such as files for a filesystem reader,  |  
|  `List[str]`  |  channel IDs for a Slack reader, or pages for a Notion reader.  |  
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
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
async defalist_resources(self, *args: Any, **kwargs: Any) -> List[str]:
"""
    List of identifiers for the specific type of resources available in the reader asynchronously.

    Returns:
        List[str]: A list of resources based on the reader type, such as files for a filesystem reader,
        channel IDs for a Slack reader, or pages for a Notion reader.

    """
    return await asyncio.to_thread(self.list_resources, *args, **kwargs)

```
 |  
| --- | --- |  
###  get_permission_info [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ResourcesReaderMixin.get_permission_info "Permanent link")

```
get_permission_info(
    resource_id: , *args: , **kwargs: 
) -> 

```

Get a dictionary of information about the permissions of a specific resource.
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
88
89
90
91
92
93
94
```
 | 
```
defget_permission_info(self, resource_id: str, *args: Any, **kwargs: Any) -> Dict:
"""
    Get a dictionary of information about the permissions of a specific resource.
    """
    raise NotImplementedError(
        f"{self.__class__.__name__} does not provide get_permission_info method currently"
    )

```
 |  
| --- | --- |  
###  aget_permission_info [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ResourcesReaderMixin.aget_permission_info "Permanent link")

```
aget_permission_info(
    resource_id: , *args: , **kwargs: 
) -> 

```

Get a dictionary of information about the permissions of a specific resource asynchronously.
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
 96
 97
 98
 99
100
101
102
103
104
```
 | 
```
async defaget_permission_info(
    self, resource_id: str, *args: Any, **kwargs: Any
) -> Dict:
"""
    Get a dictionary of information about the permissions of a specific resource asynchronously.
    """
    return await asyncio.to_thread(
        self.get_permission_info, resource_id, *args, **kwargs
    )

```
 |  
| --- | --- |  
###  get_resource_info `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ResourcesReaderMixin.get_resource_info "Permanent link")

```
get_resource_info(
    resource_id: , *args: , **kwargs: 
) -> 

```

Get a dictionary of information about a specific resource.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `resource`  |  The resource identifier.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Dict`  |  `Dict`  |  A dictionary of information about the resource.  |  
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
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
```
 | 
```
@abstractmethod
defget_resource_info(self, resource_id: str, *args: Any, **kwargs: Any) -> Dict:
"""
    Get a dictionary of information about a specific resource.

    Args:
        resource (str): The resource identifier.

    Returns:
        Dict: A dictionary of information about the resource.

    """

```
 |  
| --- | --- |  
###  aget_resource_info [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ResourcesReaderMixin.aget_resource_info "Permanent link")

```
aget_resource_info(
    resource_id: , *args: , **kwargs: 
) -> 

```

Get a dictionary of information about a specific resource asynchronously.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `resource`  |  The resource identifier.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Dict`  |  `Dict`  |  A dictionary of information about the resource.  |  
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
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
```
 | 
```
async defaget_resource_info(
    self, resource_id: str, *args: Any, **kwargs: Any
) -> Dict:
"""
    Get a dictionary of information about a specific resource asynchronously.

    Args:
        resource (str): The resource identifier.

    Returns:
        Dict: A dictionary of information about the resource.

    """
    return await asyncio.to_thread(
        self.get_resource_info, resource_id, *args, **kwargs
    )

```
 |  
| --- | --- |  
###  list_resources_with_info [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ResourcesReaderMixin.list_resources_with_info "Permanent link")

```
list_resources_with_info(
    *args: , **kwargs: 
) -> [, ]

```

Get a dictionary of information about all resources.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Dict]`  |  Dict[str, Dict]: A dictionary of information about all resources.  |  
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
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
deflist_resources_with_info(self, *args: Any, **kwargs: Any) -> Dict[str, Dict]:
"""
    Get a dictionary of information about all resources.

    Returns:
        Dict[str, Dict]: A dictionary of information about all resources.

    """
    return {
        resource: self.get_resource_info(resource, *args, **kwargs)
        for resource in self.list_resources(*args, **kwargs)
    }

```
 |  
| --- | --- |  
###  alist_resources_with_info [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ResourcesReaderMixin.alist_resources_with_info "Permanent link")

```
alist_resources_with_info(
    *args: , **kwargs: 
) -> [, ]

```

Get a dictionary of information about all resources asynchronously.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, Dict]`  |  Dict[str, Dict]: A dictionary of information about all resources.  |  
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
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
```
 | 
```
async defalist_resources_with_info(
    self, *args: Any, **kwargs: Any
) -> Dict[str, Dict]:
"""
    Get a dictionary of information about all resources asynchronously.

    Returns:
        Dict[str, Dict]: A dictionary of information about all resources.

    """
    return {
        resource: await self.aget_resource_info(resource, *args, **kwargs)
        for resource in await self.alist_resources(*args, **kwargs)
    }

```
 |  
| --- | --- |  
###  load_resource `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ResourcesReaderMixin.load_resource "Permanent link")

```
load_resource(
    resource_id: , *args: , **kwargs: 
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
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
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
```
 | 
```
@abstractmethod
defload_resource(
    self, resource_id: str, *args: Any, **kwargs: Any
) -> List[Document]:
"""
    Load data from a specific resource.

    Args:
        resource (str): The resource identifier.

    Returns:
        List[Document]: A list of documents loaded from the resource.

    """

```
 |  
| --- | --- |  
###  aload_resource [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ResourcesReaderMixin.aload_resource "Permanent link")

```
aload_resource(
    resource_id: , *args: , **kwargs: 
) -> []

```

Read file from filesystem and return documents asynchronously.
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
179
180
181
182
183
```
 | 
```
async defaload_resource(
    self, resource_id: str, *args: Any, **kwargs: Any
) -> List[Document]:
"""Read file from filesystem and return documents asynchronously."""
    return await asyncio.to_thread(self.load_resource, resource_id, *args, **kwargs)

```
 |  
| --- | --- |  
###  load_resources [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ResourcesReaderMixin.load_resources "Permanent link")

```
load_resources(
    resource_ids: [], *args: , **kwargs: 
) -> []

```

Similar to load_data, but only for specific resources.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `resource_ids`  |  `List[str]`  |  List of resource identifiers.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents loaded from the resources.  |  
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
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
```
 | 
```
defload_resources(
    self, resource_ids: List[str], *args: Any, **kwargs: Any
) -> List[Document]:
"""
    Similar to load_data, but only for specific resources.

    Args:
        resource_ids (List[str]): List of resource identifiers.

    Returns:
        List[Document]: A list of documents loaded from the resources.

    """
    return [
        doc
        for resource in resource_ids
        for doc in self.load_resource(resource, *args, **kwargs)
    ]

```
 |  
| --- | --- |  
###  aload_resources [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ResourcesReaderMixin.aload_resources "Permanent link")

```
aload_resources(
    resource_ids: [], *args: , **kwargs: 
) -> [, []]

```

Similar ato load_data, but only for specific resources.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `resource_ids`  |  `List[str]`  |  List of resource identifiers.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Dict[str, List[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")]]`  |  Dict[str, List[Document]]: A dictionary of documents loaded from the resources.  |  
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
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
```
 | 
```
async defaload_resources(
    self, resource_ids: List[str], *args: Any, **kwargs: Any
) -> Dict[str, List[Document]]:
"""
    Similar ato load_data, but only for specific resources.

    Args:
        resource_ids (List[str]): List of resource identifiers.

    Returns:
        Dict[str, List[Document]]: A dictionary of documents loaded from the resources.

    """
    return {
        resource: await self.aload_resource(resource, *args, **kwargs)
        for resource in resource_ids
    }

```
 |  
| --- | --- |  
##  ReaderConfig [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ReaderConfig "Permanent link")
Bases: 
Represents a reader and it's input arguments.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `reader`  |   |  Reader to use.  |  _required_  |  
|  `reader_args`  |  `List[Any]`  |  Reader args.  |  `<dynamic>`  |  
|  `reader_kwargs`  |  `Dict[str, Any]`  |  Reader kwargs.  |  `<class 'dict'>`  |  
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
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
```
 | 
```
classReaderConfig(BaseComponent):  # pragma: no cover
"""Represents a reader and it's input arguments."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    reader: BasePydanticReader = Field(..., description="Reader to use.")
    reader_args: List[Any] = Field(default_factory=list, description="Reader args.")
    reader_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Reader kwargs."
    )

    @classmethod
    defclass_name(cls) -> str:
"""Get the name identifier of the class."""
        return "ReaderConfig"

    defto_dict(self, **kwargs: Any) -> Dict[str, Any]:
"""Convert the class to a dictionary."""
        return {
            "loader": self.reader.to_dict(**kwargs),
            "reader_args": self.reader_args,
            "reader_kwargs": self.reader_kwargs,
            "class_name": self.class_name(),
        }

    defread(self) -> List[Document]:
"""Call the loader with the given arguments."""
        return self.reader.load_data(*self.reader_args, **self.reader_kwargs)

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ReaderConfig.class_name "Permanent link")

```
class_name() -> 

```

Get the name identifier of the class.
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
233
234
235
236
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get the name identifier of the class."""
    return "ReaderConfig"

```
 |  
| --- | --- |  
###  to_dict [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ReaderConfig.to_dict "Permanent link")

```
to_dict(**kwargs: ) -> [, ]

```

Convert the class to a dictionary.
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
238
239
240
241
242
243
244
245
```
 | 
```
defto_dict(self, **kwargs: Any) -> Dict[str, Any]:
"""Convert the class to a dictionary."""
    return {
        "loader": self.reader.to_dict(**kwargs),
        "reader_args": self.reader_args,
        "reader_kwargs": self.reader_kwargs,
        "class_name": self.class_name(),
    }

```
 |  
| --- | --- |  
###  read [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.ReaderConfig.read "Permanent link")

```
read() -> []

```

Call the loader with the given arguments.
Source code in `llama-index-core/llama_index/core/readers/base.py`  
| 
```
247
248
249
```
 | 
```
defread(self) -> List[Document]:
"""Call the loader with the given arguments."""
    return self.reader.load_data(*self.reader_args, **self.reader_kwargs)

```
 |  
| --- | --- |  
options: members: - BaseReader - BasePydanticReader
