# Arango db
##  SimpleArangoDBReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/arango_db/#llama_index.readers.arango_db.SimpleArangoDBReader "Permanent link")
Bases: 
Simple arangodb reader. Concatenates each ArangoDB doc into Document used by LlamaIndex.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `host`  |  `Optional[Union[str, List[str]]]`  |  (Union[str, List[str]]) list of urls or url for connecting to the db  |  `None`  |  
|  `client`  |  `Optional[Any]`  |  (Any) ArangoDB client  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-arango-db/llama_index/readers/arango_db/base.py`  
| 
```

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
classSimpleArangoDBReader(BaseReader):
"""
    Simple arangodb reader.
    Concatenates each ArangoDB doc into Document used by LlamaIndex.

    Args:
        host: (Union[str, List[str]]) list of urls or url for connecting to the db
        client: (Any) ArangoDB client

    """

    def__init__(
        self, host: Optional[Union[str, List[str]]] = None, client: Optional[Any] = None
    ) -> None:
"""Initialize with parameters."""
        try:
            fromarangoimport ArangoClient
        except ImportError as err:
            raise ImportError(
                "`arango` package not found, please run `pip install python-arango`"
            ) fromerr

        host = host or "http://127.0.0.1:8529"
        self.client = client or ArangoClient(hosts=host)
        self.client = cast(ArangoClient, self.client)

    def_flatten(self, texts: List[Union[str, List[str]]]) -> List[str]:
        result = []
        for text in texts:
            result += text if isinstance(text, list) else [text]
        return result

    deflazy_load(
        self,
        username: str,
        password: str,
        db_name: str,
        collection_name: str,
        field_names: List[str] = ["text"],
        separator: str = " ",
        query_dict: Optional[Dict] = {},
        max_docs: int = None,
        metadata_names: Optional[List[str]] = None,
    ) -> Iterator[Document]:
"""
        Lazy load data from ArangoDB.

        Args:
            username (str): for credentials.
            password (str): for credentials.
            db_name (str): name of the database.
            collection_name (str): name of the collection.
            field_names(List[str]): names of the fields to be concatenated.
                Defaults to ["text"]
            separator (str): separator to be used between fields.
                Defaults to " "
            query_dict (Optional[Dict]): query to filter documents. Read more
            at [docs](https://docs.python-arango.com/en/main/specs.html#arango.collection.StandardCollection.find)
                Defaults to empty dict
            max_docs (int): maximum number of documents to load.
                Defaults to None (no limit)
            metadata_names (Optional[List[str]]): names of the fields to be added
                to the metadata attribute of the Document. Defaults to None
        Returns:
            List[Document]: A list of documents.

        """
        db = self.client.db(name=db_name, username=username, password=password)
        collection = db.collection(collection_name)
        cursor = collection.find(filters=query_dict, limit=max_docs)
        for item in cursor:
            try:
                texts = [str(item[name]) for name in field_names]
            except KeyError as err:
                raise ValueError(
                    f"{err.args[0]} field not found in arangodb document."
                ) fromerr
            texts = self._flatten(texts)
            text = separator.join(texts)

            if metadata_names is None:
                yield Document(text=text)
            else:
                try:
                    metadata = {name: item[name] for name in metadata_names}
                except KeyError as err:
                    raise ValueError(
                        f"{err.args[0]} field not found in arangodb document."
                    ) fromerr
                yield Document(text=text, metadata=metadata)

    defload_data(
        self,
        username: str,
        password: str,
        db_name: str,
        collection_name: str,
        field_names: List[str] = ["text"],
        separator: str = " ",
        query_dict: Optional[Dict] = {},
        max_docs: int = None,
        metadata_names: Optional[List[str]] = None,
    ) -> List[Document]:
"""
        Load data from the ArangoDB.

        Args:
            username (str): for credentials.
            password (str): for credentials.
            db_name (str): name of the database.
            collection_name (str): name of the collection.
            field_names(List[str]): names of the fields to be concatenated.
                Defaults to ["text"]
            separator (str): separator to be used between fields.
                Defaults to ""
            query_dict (Optional[Dict]): query to filter documents. Read more
            at [docs](https://docs.python-arango.com/en/main/specs.html#arango.collection.StandardCollection.find)
                Defaults to empty dict
            max_docs (int): maximum number of documents to load.
                Defaults to 0 (no limit)
            metadata_names (Optional[List[str]]): names of the fields to be added
                to the metadata attribute of the Document. Defaults to None
        Returns:
            List[Document]: A list of documents.

        """
        return list(
            self.lazy_load(
                username,
                password,
                db_name,
                collection_name,
                field_names,
                separator,
                query_dict,
                max_docs,
                metadata_names,
            )
        )

```
 |  
| --- | --- |  
###  lazy_load [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/arango_db/#llama_index.readers.arango_db.SimpleArangoDBReader.lazy_load "Permanent link")

```
lazy_load(
    username: ,
    password: ,
    db_name: ,
    collection_name: ,
    field_names: [] = ["text"],
    separator:  = " ",
    query_dict: Optional[] = {},
    max_docs:  = None,
    metadata_names: Optional[[]] = None,
) -> Iterator[]

```

Lazy load data from ArangoDB.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `username`  |  for credentials.  |  _required_  |  
|  `password`  |  for credentials.  |  _required_  |  
|  `db_name`  |  name of the database.  |  _required_  |  
|  `collection_name`  |  name of the collection.  |  _required_  |  
|  `field_names`  |  `List[str]`  |  names of the fields to be concatenated. Defaults to ["text"]  |  `['text']`  |  
|  `separator`  |  separator to be used between fields. Defaults to " "  |  `' '`  |  
|  `query_dict`  |  `Optional[Dict]`  |  query to filter documents. Read more  |  
|  `at [docs](https`  |  //docs.python-arango.com/en/main/specs.html#arango.collection.StandardCollection.find) Defaults to empty dict  |  _required_  |  
|  `max_docs`  |  maximum number of documents to load. Defaults to None (no limit)  |  `None`  |  
|  `metadata_names`  |  `Optional[List[str]]`  |  names of the fields to be added to the metadata attribute of the Document. Defaults to None  |  `None`  |  
Returns: List[Document]: A list of documents.
Source code in `llama-index-integrations/readers/llama-index-readers-arango-db/llama_index/readers/arango_db/base.py`  
| 
```
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
```
 | 
```
deflazy_load(
    self,
    username: str,
    password: str,
    db_name: str,
    collection_name: str,
    field_names: List[str] = ["text"],
    separator: str = " ",
    query_dict: Optional[Dict] = {},
    max_docs: int = None,
    metadata_names: Optional[List[str]] = None,
) -> Iterator[Document]:
"""
    Lazy load data from ArangoDB.

    Args:
        username (str): for credentials.
        password (str): for credentials.
        db_name (str): name of the database.
        collection_name (str): name of the collection.
        field_names(List[str]): names of the fields to be concatenated.
            Defaults to ["text"]
        separator (str): separator to be used between fields.
            Defaults to " "
        query_dict (Optional[Dict]): query to filter documents. Read more
        at [docs](https://docs.python-arango.com/en/main/specs.html#arango.collection.StandardCollection.find)
            Defaults to empty dict
        max_docs (int): maximum number of documents to load.
            Defaults to None (no limit)
        metadata_names (Optional[List[str]]): names of the fields to be added
            to the metadata attribute of the Document. Defaults to None
    Returns:
        List[Document]: A list of documents.

    """
    db = self.client.db(name=db_name, username=username, password=password)
    collection = db.collection(collection_name)
    cursor = collection.find(filters=query_dict, limit=max_docs)
    for item in cursor:
        try:
            texts = [str(item[name]) for name in field_names]
        except KeyError as err:
            raise ValueError(
                f"{err.args[0]} field not found in arangodb document."
            ) fromerr
        texts = self._flatten(texts)
        text = separator.join(texts)

        if metadata_names is None:
            yield Document(text=text)
        else:
            try:
                metadata = {name: item[name] for name in metadata_names}
            except KeyError as err:
                raise ValueError(
                    f"{err.args[0]} field not found in arangodb document."
                ) fromerr
            yield Document(text=text, metadata=metadata)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/arango_db/#llama_index.readers.arango_db.SimpleArangoDBReader.load_data "Permanent link")

```
load_data(
    username: ,
    password: ,
    db_name: ,
    collection_name: ,
    field_names: [] = ["text"],
    separator:  = " ",
    query_dict: Optional[] = {},
    max_docs:  = None,
    metadata_names: Optional[[]] = None,
) -> []

```

Load data from the ArangoDB.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `username`  |  for credentials.  |  _required_  |  
|  `password`  |  for credentials.  |  _required_  |  
|  `db_name`  |  name of the database.  |  _required_  |  
|  `collection_name`  |  name of the collection.  |  _required_  |  
|  `field_names`  |  `List[str]`  |  names of the fields to be concatenated. Defaults to ["text"]  |  `['text']`  |  
|  `separator`  |  separator to be used between fields. Defaults to ""  |  `' '`  |  
|  `query_dict`  |  `Optional[Dict]`  |  query to filter documents. Read more  |  
|  `at [docs](https`  |  //docs.python-arango.com/en/main/specs.html#arango.collection.StandardCollection.find) Defaults to empty dict  |  _required_  |  
|  `max_docs`  |  maximum number of documents to load. Defaults to 0 (no limit)  |  `None`  |  
|  `metadata_names`  |  `Optional[List[str]]`  |  names of the fields to be added to the metadata attribute of the Document. Defaults to None  |  `None`  |  
Returns: List[Document]: A list of documents.
Source code in `llama-index-integrations/readers/llama-index-readers-arango-db/llama_index/readers/arango_db/base.py`  
| 
```
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
defload_data(
    self,
    username: str,
    password: str,
    db_name: str,
    collection_name: str,
    field_names: List[str] = ["text"],
    separator: str = " ",
    query_dict: Optional[Dict] = {},
    max_docs: int = None,
    metadata_names: Optional[List[str]] = None,
) -> List[Document]:
"""
    Load data from the ArangoDB.

    Args:
        username (str): for credentials.
        password (str): for credentials.
        db_name (str): name of the database.
        collection_name (str): name of the collection.
        field_names(List[str]): names of the fields to be concatenated.
            Defaults to ["text"]
        separator (str): separator to be used between fields.
            Defaults to ""
        query_dict (Optional[Dict]): query to filter documents. Read more
        at [docs](https://docs.python-arango.com/en/main/specs.html#arango.collection.StandardCollection.find)
            Defaults to empty dict
        max_docs (int): maximum number of documents to load.
            Defaults to 0 (no limit)
        metadata_names (Optional[List[str]]): names of the fields to be added
            to the metadata attribute of the Document. Defaults to None
    Returns:
        List[Document]: A list of documents.

    """
    return list(
        self.lazy_load(
            username,
            password,
            db_name,
            collection_name,
            field_names,
            separator,
            query_dict,
            max_docs,
            metadata_names,
        )
    )

```
 |  
| --- | --- |  
options: members: - SimpleArangoDBReader
