# Milvus
##  MilvusReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/milvus/#llama_index.readers.milvus.MilvusReader "Permanent link")
Bases: 
Milvus reader.
Source code in `llama-index-integrations/readers/llama-index-readers-milvus/llama_index/readers/milvus/base.py`  
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
```
 | 
```
classMilvusReader(BaseReader):
"""Milvus reader."""

    def__init__(
        self,
        host: str = "localhost",
        port: int = 19530,
        user: str = "",
        password: str = "",
        use_secure: bool = False,
    ):
"""Initialize with parameters."""
        import_err_msg = (
            "`pymilvus` package not found, please run `pip install pymilvus`"
        )
        try:
            importpymilvus  # noqa
        except ImportError:
            raise ImportError(import_err_msg)

        frompymilvusimport MilvusException

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.use_secure = use_secure
        self.collection = None

        self.default_search_params = {
            "IVF_FLAT": {"metric_type": "IP", "params": {"nprobe": 10}},
            "IVF_SQ8": {"metric_type": "IP", "params": {"nprobe": 10}},
            "IVF_PQ": {"metric_type": "IP", "params": {"nprobe": 10}},
            "HNSW": {"metric_type": "IP", "params": {"ef": 10}},
            "RHNSW_FLAT": {"metric_type": "IP", "params": {"ef": 10}},
            "RHNSW_SQ": {"metric_type": "IP", "params": {"ef": 10}},
            "RHNSW_PQ": {"metric_type": "IP", "params": {"ef": 10}},
            "IVF_HNSW": {"metric_type": "IP", "params": {"nprobe": 10, "ef": 10}},
            "ANNOY": {"metric_type": "IP", "params": {"search_k": 10}},
            "AUTOINDEX": {"metric_type": "IP", "params": {}},
        }
        try:
            self._create_connection_alias()
        except MilvusException:
            raise

    defload_data(
        self,
        query_vector: List[float],
        collection_name: str,
        expr: Any = None,
        search_params: Optional[dict] = None,
        limit: int = 10,
    ) -> List[Document]:
"""
        Load data from Milvus.

        Args:
            collection_name (str): Name of the Milvus collection.
            query_vector (List[float]): Query vector.
            limit (int): Number of results to return.

        Returns:
            List[Document]: A list of documents.

        """
        frompymilvusimport Collection, MilvusException

        try:
            self.collection = Collection(collection_name, using=self.alias)
        except MilvusException:
            raise

        assert self.collection is not None
        try:
            self.collection.load()
        except MilvusException:
            raise
        if search_params is None:
            search_params = self._create_search_params()

        res = self.collection.search(
            [query_vector],
            "embedding",
            param=search_params,
            expr=expr,
            output_fields=["doc_id", "text"],
            limit=limit,
        )

        documents = []
        # TODO: In future append embedding when more efficient
        for hit in res[0]:
            document = Document(
                id_=hit.entity.get("doc_id"),
                text=hit.entity.get("text"),
            )

            documents.append(document)

        return documents

    def_create_connection_alias(self) -> None:
        frompymilvusimport connections

        self.alias = None
        # Attempt to reuse an open connection
        for x in connections.list_connections():
            addr = connections.get_connection_addr(x[0])
            if (
                x[1]
                and ("address" in addr)
                and (addr["address"] == f"{self.host}:{self.port}")
            ):
                self.alias = x[0]
                break

        # Connect to the Milvus instance using the passed in Environment variables
        if self.alias is None:
            self.alias = uuid4().hex
            connections.connect(
                alias=self.alias,
                host=self.host,
                port=self.port,
                user=self.user,  # type: ignore
                password=self.password,  # type: ignore
                secure=self.use_secure,
            )

    def_create_search_params(self) -> Dict[str, Any]:
        assert self.collection is not None
        index = self.collection.indexes[0]._index_params
        search_params = self.default_search_params[index["index_type"]]
        search_params["metric_type"] = index["metric_type"]
        return search_params

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/milvus/#llama_index.readers.milvus.MilvusReader.load_data "Permanent link")

```
load_data(
    query_vector: [float],
    collection_name: ,
    expr:  = None,
    search_params: Optional[] = None,
    limit:  = 10,
) -> []

```

Load data from Milvus.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection_name`  |  Name of the Milvus collection.  |  _required_  |  
|  `query_vector`  |  `List[float]`  |  Query vector.  |  _required_  |  
|  `limit`  |  Number of results to return.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-milvus/llama_index/readers/milvus/base.py`  
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
```
 | 
```
defload_data(
    self,
    query_vector: List[float],
    collection_name: str,
    expr: Any = None,
    search_params: Optional[dict] = None,
    limit: int = 10,
) -> List[Document]:
"""
    Load data from Milvus.

    Args:
        collection_name (str): Name of the Milvus collection.
        query_vector (List[float]): Query vector.
        limit (int): Number of results to return.

    Returns:
        List[Document]: A list of documents.

    """
    frompymilvusimport Collection, MilvusException

    try:
        self.collection = Collection(collection_name, using=self.alias)
    except MilvusException:
        raise

    assert self.collection is not None
    try:
        self.collection.load()
    except MilvusException:
        raise
    if search_params is None:
        search_params = self._create_search_params()

    res = self.collection.search(
        [query_vector],
        "embedding",
        param=search_params,
        expr=expr,
        output_fields=["doc_id", "text"],
        limit=limit,
    )

    documents = []
    # TODO: In future append embedding when more efficient
    for hit in res[0]:
        document = Document(
            id_=hit.entity.get("doc_id"),
            text=hit.entity.get("text"),
        )

        documents.append(document)

    return documents

```
 |  
| --- | --- |  
options: members: - MilvusReader
