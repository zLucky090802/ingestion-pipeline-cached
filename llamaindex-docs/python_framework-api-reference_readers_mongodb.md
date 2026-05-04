# Mongodb
##  SimpleMongoReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/mongodb/#llama_index.readers.mongodb.SimpleMongoReader "Permanent link")
Bases: 
Simple mongo reader.
Concatenates each Mongo doc into Document used by LlamaIndex.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `host`  |  Mongo host.  |  `None`  |  
|  `port`  |  Mongo port.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-mongodb/llama_index/readers/mongodb/base.py`  
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
```
 | 
```
classSimpleMongoReader(BaseReader):
"""
    Simple mongo reader.

    Concatenates each Mongo doc into Document used by LlamaIndex.

    Args:
        host (str): Mongo host.
        port (int): Mongo port.

    """

    def__init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        uri: Optional[str] = None,
    ) -> None:
"""Initialize with parameters."""
        try:
            frompymongoimport MongoClient, AsyncMongoClient
            frompymongo.driver_infoimport DriverInfo
        except ImportError as err:
            raise ImportError(
                "`pymongo` package not found, please run `pip install pymongo`"
            ) fromerr

        if uri:
            client_args = (uri,)
        elif host and port:
            client_args = (host, port)
        else:
            raise ValueError("Either `host` and `port` or `uri` must be provided.")

        self.client = MongoClient(*client_args)
        self.async_client = AsyncMongoClient(*client_args)

        # append_metadata was added in PyMongo 4.14.0, but is a valid database name on earlier versions
        if callable(self.client.append_metadata):
            self.client.append_metadata(
                DriverInfo(name="llama-index", version=version("llama-index"))
            )
        if callable(self.async_client.append_metadata):
            self.async_client.append_metadata(
                DriverInfo(name="llama-index", version=version("llama-index"))
            )

    deflazy_load_data(
        self,
        db_name: str,
        collection_name: str,
        field_names: List[str] = ["text"],
        separator: str = "",
        query_dict: Optional[Dict] = None,
        max_docs: int = 0,
        metadata_names: Optional[List[str]] = None,
        field_extractors: Optional[Dict[str, Callable[..., str]]] = None,
    ) -> Iterable[Document]:
"""
        Lazy load data from MongoDB.

        Args:
            db_name (str): name of the database.
            collection_name (str): name of the collection.
            field_names(List[str]): names of the fields to be concatenated.
                Defaults to ["text"]
            separator (str): separator to be used between fields.
                Defaults to ""
            query_dict (Optional[Dict]): query to filter documents. Read more
                at [docs](https://docs.mongodb.com/manual/reference/method/db.collection.find/)
                Defaults to empty dict
            max_docs (int): maximum number of documents to load.
                Defaults to 0 (no limit)
            metadata_names (Optional[List[str]]): names of the fields to be added
                to the metadata attribute of the Document. Defaults to None
            field_extractors (Optional[Dict[str, Callable[..., str]]]): a dictionary
                of functions to use when extracting a field from a document.
                Defaults to None

        Yields:
            Document: a document object with the concatenated text and metadata.

        Raises:
            ValueError: if a field is not found in a document.

        """
        db = self.client[db_name]
        cursor = db[collection_name].find(
            filter=query_dict or {},
            limit=max_docs,
            projection=dict.fromkeys(field_names + (metadata_names or []), 1),
        )

        field_extractors = field_extractors or {}

        for item in cursor:
            try:
                texts = [
                    field_extractors.get(name, str)(item[name]) for name in field_names
                ]
            except KeyError as err:
                raise ValueError(
                    f"{err.args[0]} field not found in Mongo document."
                ) fromerr

            text = separator.join(texts)

            if metadata_names is None:
                yield Document(text=text, id_=str(item["_id"]))
            else:
                try:
                    metadata = {name: item.get(name) for name in metadata_names}
                    metadata["collection"] = collection_name
                except KeyError as err:
                    raise ValueError(
                        f"{err.args[0]} field not found in Mongo document."
                    ) fromerr
                yield Document(text=text, id_=str(item["_id"]), metadata=metadata)

    async defalazy_load_data(
        self,
        db_name: str,
        collection_name: str,
        field_names: List[str] = ["text"],
        separator: str = "",
        query_dict: Optional[Dict] = None,
        max_docs: int = 0,
        metadata_names: Optional[List[str]] = None,
        field_extractors: Optional[Dict[str, Callable[..., str]]] = None,
    ):
"""
        Asynchronously lazy load data from a MongoDB collection.

        Args:
            db_name (str): The name of the database to connect to.
            collection_name (str): The name of the collection to query.
            field_names (List[str]): The fields to concatenate into the document's text. Defaults to ["text"].
            separator (str): The separator to use between concatenated fields. Defaults to "".
            query_dict (Optional[Dict]): A dictionary to filter documents. Defaults to None.
            max_docs (int): The maximum number of documents to load. Defaults to 0 (no limit).
            metadata_names (Optional[List[str]]): The fields to include in the document's metadata. Defaults to None.
            field_extractors (Optional[Dict[str, Callable[..., str]]]): A dictionary of field-specific extractor functions. Defaults to None.

        Yields:
            Document: An asynchronous generator of Document objects with concatenated text and optional metadata.

        Raises:
            ValueError: If the async_client is not initialized or if a specified field is not found in a document.

        """
        db = self.async_client[db_name]
        cursor = db[collection_name].find(
            filter=query_dict or {},
            limit=max_docs,
            projection=dict.fromkeys(field_names + (metadata_names or []), 1),
        )

        field_extractors = field_extractors or {}

        async for item in cursor:
            try:
                texts = [
                    field_extractors.get(name, str)(item[name]) for name in field_names
                ]
            except KeyError as err:
                raise ValueError(
                    f"{err.args[0]} field not found in Mongo document."
                ) fromerr

            text = separator.join(texts)

            if metadata_names is None:
                yield Document(text=text, id_=str(item["_id"]))
            else:
                try:
                    metadata = {name: item.get(name) for name in metadata_names}
                    metadata["collection"] = collection_name
                except KeyError as err:
                    raise ValueError(
                        f"{err.args[0]} field not found in Mongo document."
                    ) fromerr
                yield Document(text=text, id_=str(item["_id"]), metadata=metadata)

```
 |  
| --- | --- |  
###  lazy_load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/mongodb/#llama_index.readers.mongodb.SimpleMongoReader.lazy_load_data "Permanent link")

```
lazy_load_data(
    db_name: ,
    collection_name: ,
    field_names: [] = ["text"],
    separator:  = "",
    query_dict: Optional[] = None,
    max_docs:  = 0,
    metadata_names: Optional[[]] = None,
    field_extractors: Optional[
        [, Callable[..., ]]
    ] = None,
) -> Iterable[]

```

Lazy load data from MongoDB.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `db_name`  |  name of the database.  |  _required_  |  
|  `collection_name`  |  name of the collection.  |  _required_  |  
|  `field_names`  |  `List[str]`  |  names of the fields to be concatenated. Defaults to ["text"]  |  `['text']`  |  
|  `separator`  |  separator to be used between fields. Defaults to ""  |  
|  `query_dict`  |  `Optional[Dict]`  |  query to filter documents. Read more at [docs](https://docs.mongodb.com/manual/reference/method/db.collection.find/) Defaults to empty dict  |  `None`  |  
|  `max_docs`  |  maximum number of documents to load. Defaults to 0 (no limit)  |  
|  `metadata_names`  |  `Optional[List[str]]`  |  names of the fields to be added to the metadata attribute of the Document. Defaults to None  |  `None`  |  
|  `field_extractors`  |  `Optional[Dict[str, Callable[..., str]]]`  |  a dictionary of functions to use when extracting a field from a document. Defaults to None  |  `None`  |  
Yields:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Document`  |  `Iterable[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")]`  |  a document object with the concatenated text and metadata.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  if a field is not found in a document.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-mongodb/llama_index/readers/mongodb/base.py`  
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
```
 | 
```
deflazy_load_data(
    self,
    db_name: str,
    collection_name: str,
    field_names: List[str] = ["text"],
    separator: str = "",
    query_dict: Optional[Dict] = None,
    max_docs: int = 0,
    metadata_names: Optional[List[str]] = None,
    field_extractors: Optional[Dict[str, Callable[..., str]]] = None,
) -> Iterable[Document]:
"""
    Lazy load data from MongoDB.

    Args:
        db_name (str): name of the database.
        collection_name (str): name of the collection.
        field_names(List[str]): names of the fields to be concatenated.
            Defaults to ["text"]
        separator (str): separator to be used between fields.
            Defaults to ""
        query_dict (Optional[Dict]): query to filter documents. Read more
            at [docs](https://docs.mongodb.com/manual/reference/method/db.collection.find/)
            Defaults to empty dict
        max_docs (int): maximum number of documents to load.
            Defaults to 0 (no limit)
        metadata_names (Optional[List[str]]): names of the fields to be added
            to the metadata attribute of the Document. Defaults to None
        field_extractors (Optional[Dict[str, Callable[..., str]]]): a dictionary
            of functions to use when extracting a field from a document.
            Defaults to None

    Yields:
        Document: a document object with the concatenated text and metadata.

    Raises:
        ValueError: if a field is not found in a document.

    """
    db = self.client[db_name]
    cursor = db[collection_name].find(
        filter=query_dict or {},
        limit=max_docs,
        projection=dict.fromkeys(field_names + (metadata_names or []), 1),
    )

    field_extractors = field_extractors or {}

    for item in cursor:
        try:
            texts = [
                field_extractors.get(name, str)(item[name]) for name in field_names
            ]
        except KeyError as err:
            raise ValueError(
                f"{err.args[0]} field not found in Mongo document."
            ) fromerr

        text = separator.join(texts)

        if metadata_names is None:
            yield Document(text=text, id_=str(item["_id"]))
        else:
            try:
                metadata = {name: item.get(name) for name in metadata_names}
                metadata["collection"] = collection_name
            except KeyError as err:
                raise ValueError(
                    f"{err.args[0]} field not found in Mongo document."
                ) fromerr
            yield Document(text=text, id_=str(item["_id"]), metadata=metadata)

```
 |  
| --- | --- |  
###  alazy_load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/mongodb/#llama_index.readers.mongodb.SimpleMongoReader.alazy_load_data "Permanent link")

```
alazy_load_data(
    db_name: ,
    collection_name: ,
    field_names: [] = ["text"],
    separator:  = "",
    query_dict: Optional[] = None,
    max_docs:  = 0,
    metadata_names: Optional[[]] = None,
    field_extractors: Optional[
        [, Callable[..., ]]
    ] = None,
)

```

Asynchronously lazy load data from a MongoDB collection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `db_name`  |  The name of the database to connect to.  |  _required_  |  
|  `collection_name`  |  The name of the collection to query.  |  _required_  |  
|  `field_names`  |  `List[str]`  |  The fields to concatenate into the document's text. Defaults to ["text"].  |  `['text']`  |  
|  `separator`  |  The separator to use between concatenated fields. Defaults to "".  |  
|  `query_dict`  |  `Optional[Dict]`  |  A dictionary to filter documents. Defaults to None.  |  `None`  |  
|  `max_docs`  |  The maximum number of documents to load. Defaults to 0 (no limit).  |  
|  `metadata_names`  |  `Optional[List[str]]`  |  The fields to include in the document's metadata. Defaults to None.  |  `None`  |  
|  `field_extractors`  |  `Optional[Dict[str, Callable[..., str]]]`  |  A dictionary of field-specific extractor functions. Defaults to None.  |  `None`  |  
Yields:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Document`  |  An asynchronous generator of Document objects with concatenated text and optional metadata.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If the async_client is not initialized or if a specified field is not found in a document.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-mongodb/llama_index/readers/mongodb/base.py`  
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
```
 | 
```
async defalazy_load_data(
    self,
    db_name: str,
    collection_name: str,
    field_names: List[str] = ["text"],
    separator: str = "",
    query_dict: Optional[Dict] = None,
    max_docs: int = 0,
    metadata_names: Optional[List[str]] = None,
    field_extractors: Optional[Dict[str, Callable[..., str]]] = None,
):
"""
    Asynchronously lazy load data from a MongoDB collection.

    Args:
        db_name (str): The name of the database to connect to.
        collection_name (str): The name of the collection to query.
        field_names (List[str]): The fields to concatenate into the document's text. Defaults to ["text"].
        separator (str): The separator to use between concatenated fields. Defaults to "".
        query_dict (Optional[Dict]): A dictionary to filter documents. Defaults to None.
        max_docs (int): The maximum number of documents to load. Defaults to 0 (no limit).
        metadata_names (Optional[List[str]]): The fields to include in the document's metadata. Defaults to None.
        field_extractors (Optional[Dict[str, Callable[..., str]]]): A dictionary of field-specific extractor functions. Defaults to None.

    Yields:
        Document: An asynchronous generator of Document objects with concatenated text and optional metadata.

    Raises:
        ValueError: If the async_client is not initialized or if a specified field is not found in a document.

    """
    db = self.async_client[db_name]
    cursor = db[collection_name].find(
        filter=query_dict or {},
        limit=max_docs,
        projection=dict.fromkeys(field_names + (metadata_names or []), 1),
    )

    field_extractors = field_extractors or {}

    async for item in cursor:
        try:
            texts = [
                field_extractors.get(name, str)(item[name]) for name in field_names
            ]
        except KeyError as err:
            raise ValueError(
                f"{err.args[0]} field not found in Mongo document."
            ) fromerr

        text = separator.join(texts)

        if metadata_names is None:
            yield Document(text=text, id_=str(item["_id"]))
        else:
            try:
                metadata = {name: item.get(name) for name in metadata_names}
                metadata["collection"] = collection_name
            except KeyError as err:
                raise ValueError(
                    f"{err.args[0]} field not found in Mongo document."
                ) fromerr
            yield Document(text=text, id_=str(item["_id"]), metadata=metadata)

```
 |  
| --- | --- |  
options: members: - SimpleMongoReader
