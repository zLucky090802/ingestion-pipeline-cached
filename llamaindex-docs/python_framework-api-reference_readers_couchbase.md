# Couchbase
##  CouchbaseReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/couchbase/#llama_index.readers.couchbase.CouchbaseReader "Permanent link")
Bases: 
Couchbase document loader.
Loads data from a Couchbase cluster into Document used by LlamaIndex.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `client`  |  `Optional[Any]`  |  A Couchbase client to use. If not provided, the client will be created based on the connection_string and database credentials.  |  `None`  |  
|  `connection_string`  |  `Optional[str]`  |  The connection string to the Couchbase cluster.  |  `None`  |  
|  `db_username`  |  `Optional[str]`  |  The username to connect to the Couchbase cluster.  |  `None`  |  
|  `db_password`  |  `Optional[str]`  |  The password to connect to the Couchbase cluster.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-couchbase/llama_index/readers/couchbase/base.py`  
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
```
 | 
```
classCouchbaseReader(BaseReader):
"""
    Couchbase document loader.

    Loads data from a Couchbase cluster into Document used by LlamaIndex.

    Args:
        client(Optional[Any]): A Couchbase client to use.
            If not provided, the client will be created based on the connection_string
            and database credentials.
        connection_string (Optional[str]): The connection string to the Couchbase cluster.
        db_username (Optional[str]): The username to connect to the Couchbase cluster.
        db_password (Optional[str]): The password to connect to the Couchbase cluster.

    """

    def__init__(
        self,
        client: Optional[Any] = None,
        connection_string: Optional[str] = None,
        db_username: Optional[str] = None,
        db_password: Optional[str] = None,
    ) -> None:
"""Initialize Couchbase document loader."""
        import_err_msg = "`couchbase` package not found, please run `pip install --upgrade couchbase`"
        try:
            fromcouchbase.authimport PasswordAuthenticator
            fromcouchbase.clusterimport Cluster
            fromcouchbase.optionsimport ClusterOptions
        except ImportError:
            raise ImportError(import_err_msg)

        if not client:
            if not connection_string or not db_username or not db_password:
                raise ValueError(
                    "You need to pass either a couchbase client or connection_string and credentials must be provided."
                )
            else:
                auth = PasswordAuthenticator(
                    db_username,
                    db_password,
                )

                self._client: Cluster = Cluster(connection_string, ClusterOptions(auth))
        else:
            self._client = client

    deflazy_load_data(
        self,
        query: str,
        text_fields: Optional[List[str]] = None,
        metadata_fields: Optional[List[str]] = [],
    ) -> Iterable[Document]:
"""
        Load data from the Couchbase cluster lazily.

        Args:
            query (str): The SQL++ query to execute.
            text_fields (Optional[List[str]]): The columns to write into the
                `text` field of the document. By default, all columns are
                written.
            metadata_fields (Optional[List[str]]): The columns to write into the
                `metadata` field of the document. By default, no columns are written.

        """
        fromdatetimeimport timedelta

        if not query:
            raise ValueError("Query must be provided.")

        # Ensure connection to Couchbase cluster
        self._client.wait_until_ready(timedelta(seconds=5))

        # Run SQL++ Query
        result = self._client.query(query)
        for row in result:
            if not text_fields:
                text_fields = list(row.keys())

            metadata = {field: row[field] for field in metadata_fields}

            document = "\n".join(
                f"{k}: {v}" for k, v in row.items() if k in text_fields
            )

            yield (Document(text=document, metadata=metadata))

    defload_data(
        self,
        query: str,
        text_fields: Optional[List[str]] = None,
        metadata_fields: Optional[List[str]] = None,
    ) -> List[Document]:
"""
        Load data from the Couchbase cluster.

        Args:
            query (str): The SQL++ query to execute.
            text_fields (Optional[List[str]]): The columns to write into the
                `text` field of the document. By default, all columns are
                written.
            metadata_fields (Optional[List[str]]): The columns to write into the
                `metadata` field of the document. By default, no columns are written.

        """
        return list(self.lazy_load_data(query, text_fields, metadata_fields))

```
 |  
| --- | --- |  
###  lazy_load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/couchbase/#llama_index.readers.couchbase.CouchbaseReader.lazy_load_data "Permanent link")

```
lazy_load_data(
    query: ,
    text_fields: Optional[[]] = None,
    metadata_fields: Optional[[]] = [],
) -> Iterable[]

```

Load data from the Couchbase cluster lazily.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The SQL++ query to execute.  |  _required_  |  
|  `text_fields`  |  `Optional[List[str]]`  |  The columns to write into the `text` field of the document. By default, all columns are written.  |  `None`  |  
|  `metadata_fields`  |  `Optional[List[str]]`  |  The columns to write into the `metadata` field of the document. By default, no columns are written.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-couchbase/llama_index/readers/couchbase/base.py`  
| 
```
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
```
 | 
```
deflazy_load_data(
    self,
    query: str,
    text_fields: Optional[List[str]] = None,
    metadata_fields: Optional[List[str]] = [],
) -> Iterable[Document]:
"""
    Load data from the Couchbase cluster lazily.

    Args:
        query (str): The SQL++ query to execute.
        text_fields (Optional[List[str]]): The columns to write into the
            `text` field of the document. By default, all columns are
            written.
        metadata_fields (Optional[List[str]]): The columns to write into the
            `metadata` field of the document. By default, no columns are written.

    """
    fromdatetimeimport timedelta

    if not query:
        raise ValueError("Query must be provided.")

    # Ensure connection to Couchbase cluster
    self._client.wait_until_ready(timedelta(seconds=5))

    # Run SQL++ Query
    result = self._client.query(query)
    for row in result:
        if not text_fields:
            text_fields = list(row.keys())

        metadata = {field: row[field] for field in metadata_fields}

        document = "\n".join(
            f"{k}: {v}" for k, v in row.items() if k in text_fields
        )

        yield (Document(text=document, metadata=metadata))

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/couchbase/#llama_index.readers.couchbase.CouchbaseReader.load_data "Permanent link")

```
load_data(
    query: ,
    text_fields: Optional[[]] = None,
    metadata_fields: Optional[[]] = None,
) -> []

```

Load data from the Couchbase cluster.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The SQL++ query to execute.  |  _required_  |  
|  `text_fields`  |  `Optional[List[str]]`  |  The columns to write into the `text` field of the document. By default, all columns are written.  |  `None`  |  
|  `metadata_fields`  |  `Optional[List[str]]`  |  The columns to write into the `metadata` field of the document. By default, no columns are written.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-couchbase/llama_index/readers/couchbase/base.py`  
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
```
 | 
```
defload_data(
    self,
    query: str,
    text_fields: Optional[List[str]] = None,
    metadata_fields: Optional[List[str]] = None,
) -> List[Document]:
"""
    Load data from the Couchbase cluster.

    Args:
        query (str): The SQL++ query to execute.
        text_fields (Optional[List[str]]): The columns to write into the
            `text` field of the document. By default, all columns are
            written.
        metadata_fields (Optional[List[str]]): The columns to write into the
            `metadata` field of the document. By default, no columns are written.

    """
    return list(self.lazy_load_data(query, text_fields, metadata_fields))

```
 |  
| --- | --- |  
options: members: - CouchbaseReader
