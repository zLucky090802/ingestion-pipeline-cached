# Qdrant
##  QdrantReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/qdrant/#llama_index.readers.qdrant.QdrantReader "Permanent link")
Bases: 
Qdrant reader.
Retrieve documents from existing Qdrant collections.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `location`  |  `Optional[str]`  |  If `:memory:` - use in-memory Qdrant instance. If `str` - use it as a `url` parameter. If `None` - use default values for `host` and `port`.  |  `None`  |  
|  `url`  |  `Optional[str]`  |  either host or str of "Optional[scheme], host, Optional[port], Optional[prefix]". Default: `None`  |  `None`  |  
|  `port`  |  `Optional[int]`  |  Port of the REST API interface. Default: 6333  |  `6333`  |  
|  `grpc_port`  |  Port of the gRPC interface. Default: 6334  |  `6334`  |  
|  `prefer_grpc`  |  `bool`  |  If `true` - use gPRC interface whenever possible in custom methods.  |  `False`  |  
|  `https`  |  `Optional[bool]`  |  If `true` - use HTTPS(SSL) protocol. Default: `false`  |  `None`  |  
|  `api_key`  |  `Optional[str]`  |  API key for authentication in Qdrant Cloud. Default: `None`  |  `None`  |  
|  `prefix`  |  `Optional[str]`  |  If not `None` - add `prefix` to the REST URL path. Example: `service/v1` will result in `http://localhost:6333/service/v1/{qdrant-endpoint}` for REST API. Default: `None`  |  `None`  |  
|  `timeout`  |  `Optional[float]`  |  Timeout for REST and gRPC API requests. Default: 5.0 seconds for REST and unlimited for gRPC  |  `None`  |  
|  `host`  |  `Optional[str]`  |  Host name of Qdrant service. If url and host are None, set to 'localhost'. Default: `None`  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-qdrant/llama_index/readers/qdrant/base.py`  
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
```
 | 
```
classQdrantReader(BaseReader):
"""
    Qdrant reader.

    Retrieve documents from existing Qdrant collections.

    Args:
        location:
            If `:memory:` - use in-memory Qdrant instance.
            If `str` - use it as a `url` parameter.
            If `None` - use default values for `host` and `port`.
        url:
            either host or str of
            "Optional[scheme], host, Optional[port], Optional[prefix]".
            Default: `None`
        port: Port of the REST API interface. Default: 6333
        grpc_port: Port of the gRPC interface. Default: 6334
        prefer_grpc: If `true` - use gPRC interface whenever possible in custom methods.
        https: If `true` - use HTTPS(SSL) protocol. Default: `false`
        api_key: API key for authentication in Qdrant Cloud. Default: `None`
        prefix:
            If not `None` - add `prefix` to the REST URL path.
            Example: `service/v1` will result in
            `http://localhost:6333/service/v1/{qdrant-endpoint}` for REST API.
            Default: `None`
        timeout:
            Timeout for REST and gRPC API requests.
            Default: 5.0 seconds for REST and unlimited for gRPC
        host: Host name of Qdrant service. If url and host are None, set to 'localhost'.
            Default: `None`

    """

    def__init__(
        self,
        location: Optional[str] = None,
        url: Optional[str] = None,
        port: Optional[int] = 6333,
        grpc_port: int = 6334,
        prefer_grpc: bool = False,
        https: Optional[bool] = None,
        api_key: Optional[str] = None,
        prefix: Optional[str] = None,
        timeout: Optional[float] = None,
        host: Optional[str] = None,
        path: Optional[str] = None,
    ):
"""Initialize with parameters."""
        import_err_msg = (
            "`qdrant-client` package not found, please run `pip install qdrant-client`"
        )
        try:
            importqdrant_client
        except ImportError:
            raise ImportError(import_err_msg)

        self._client = qdrant_client.QdrantClient(
            location=location,
            url=url,
            port=port,
            grpc_port=grpc_port,
            prefer_grpc=prefer_grpc,
            https=https,
            api_key=api_key,
            prefix=prefix,
            timeout=timeout,
            host=host,
            path=path,
        )

    defload_data(
        self,
        collection_name: str,
        query_vector: List[float],
        should_search_mapping: Optional[Dict[str, str]] = None,
        must_search_mapping: Optional[Dict[str, str]] = None,
        must_not_search_mapping: Optional[Dict[str, str]] = None,
        rang_search_mapping: Optional[Dict[str, Dict[str, float]]] = None,
        limit: int = 10,
    ) -> List[Document]:
"""
        Load data from Qdrant.

        Args:
            collection_name (str): Name of the Qdrant collection.
            query_vector (List[float]): Query vector.
            should_search_mapping (Optional[Dict[str, str]]): Mapping from field name
                to query string.
            must_search_mapping (Optional[Dict[str, str]]): Mapping from field name
                to query string.
            must_not_search_mapping (Optional[Dict[str, str]]): Mapping from field
                name to query string.
            rang_search_mapping (Optional[Dict[str, Dict[str, float]]]): Mapping from
                field name to range query.
            limit (int): Number of results to return.

        Example:
            reader = QdrantReader()
            reader.load_data(
                 collection_name="test_collection",
                 query_vector=[0.1, 0.2, 0.3],
                 should_search_mapping={"text_field": "text"},
                 must_search_mapping={"text_field": "text"},
                 must_not_search_mapping={"text_field": "text"},
                 # gte, lte, gt, lt supported
                 rang_search_mapping={"text_field": {"gte": 0.1, "lte": 0.2}},
                 limit=10


        Returns:
            List[Document]: A list of documents.

        """
        fromqdrant_client.http.modelsimport (
            FieldCondition,
            Filter,
            MatchText,
            MatchValue,
            Range,
        )
        fromqdrant_client.http.models.modelsimport Payload

        should_search_mapping = should_search_mapping or {}
        must_search_mapping = must_search_mapping or {}
        must_not_search_mapping = must_not_search_mapping or {}
        rang_search_mapping = rang_search_mapping or {}

        should_search_conditions = [
            FieldCondition(key=key, match=MatchText(text=value))
            for key, value in should_search_mapping.items()
            if should_search_mapping
        ]
        must_search_conditions = [
            FieldCondition(key=key, match=MatchValue(value=value))
            for key, value in must_search_mapping.items()
            if must_search_mapping
        ]
        must_not_search_conditions = [
            FieldCondition(key=key, match=MatchValue(value=value))
            for key, value in must_not_search_mapping.items()
            if must_not_search_mapping
        ]
        rang_search_conditions = [
            FieldCondition(
                key=key,
                range=Range(
                    gte=value.get("gte"),
                    lte=value.get("lte"),
                    gt=value.get("gt"),
                    lt=value.get("lt"),
                ),
            )
            for key, value in rang_search_mapping.items()
            if rang_search_mapping
        ]
        should_search_conditions.extend(rang_search_conditions)
        response = self._client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            query_filter=Filter(
                must=must_search_conditions,
                must_not=must_not_search_conditions,
                should=should_search_conditions,
            ),
            with_vectors=True,
            with_payload=True,
            limit=limit,
        )

        documents = []
        for point in response:
            payload = cast(Payload, point.payload)
            try:
                vector = cast(List[float], point.vector)
            except ValueError as e:
                raise ValueError("Could not cast vector to List[float].") frome
            document = Document(
                id_=payload.get("doc_id"),
                text=payload.get("text"),
                metadata=payload.get("metadata"),
                embedding=vector,
            )
            documents.append(document)

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/qdrant/#llama_index.readers.qdrant.QdrantReader.load_data "Permanent link")

```
load_data(
    collection_name: ,
    query_vector: [float],
    should_search_mapping: Optional[[, ]] = None,
    must_search_mapping: Optional[[, ]] = None,
    must_not_search_mapping: Optional[
        [, ]
    ] = None,
    rang_search_mapping: Optional[
        [, [, float]]
    ] = None,
    limit:  = 10,
) -> []

```

Load data from Qdrant.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection_name`  |  Name of the Qdrant collection.  |  _required_  |  
|  `query_vector`  |  `List[float]`  |  Query vector.  |  _required_  |  
|  `should_search_mapping`  |  `Optional[Dict[str, str]]`  |  Mapping from field name to query string.  |  `None`  |  
|  `must_search_mapping`  |  `Optional[Dict[str, str]]`  |  Mapping from field name to query string.  |  `None`  |  
|  `must_not_search_mapping`  |  `Optional[Dict[str, str]]`  |  Mapping from field name to query string.  |  `None`  |  
|  `rang_search_mapping`  |  `Optional[Dict[str, Dict[str, float]]]`  |  Mapping from field name to range query.  |  `None`  |  
|  `limit`  |  Number of results to return.  |  
Example
reader = QdrantReader() reader.load_data( collection_name="test_collection", query_vector=[0.1, 0.2, 0.3], should_search_mapping={"text_field": "text"}, must_search_mapping={"text_field": "text"}, must_not_search_mapping={"text_field": "text"}, # gte, lte, gt, lt supported rang_search_mapping={"text_field": {"gte": 0.1, "lte": 0.2}}, limit=10 )
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-qdrant/llama_index/readers/qdrant/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    collection_name: str,
    query_vector: List[float],
    should_search_mapping: Optional[Dict[str, str]] = None,
    must_search_mapping: Optional[Dict[str, str]] = None,
    must_not_search_mapping: Optional[Dict[str, str]] = None,
    rang_search_mapping: Optional[Dict[str, Dict[str, float]]] = None,
    limit: int = 10,
) -> List[Document]:
"""
    Load data from Qdrant.

    Args:
        collection_name (str): Name of the Qdrant collection.
        query_vector (List[float]): Query vector.
        should_search_mapping (Optional[Dict[str, str]]): Mapping from field name
            to query string.
        must_search_mapping (Optional[Dict[str, str]]): Mapping from field name
            to query string.
        must_not_search_mapping (Optional[Dict[str, str]]): Mapping from field
            name to query string.
        rang_search_mapping (Optional[Dict[str, Dict[str, float]]]): Mapping from
            field name to range query.
        limit (int): Number of results to return.

    Example:
        reader = QdrantReader()
        reader.load_data(
             collection_name="test_collection",
             query_vector=[0.1, 0.2, 0.3],
             should_search_mapping={"text_field": "text"},
             must_search_mapping={"text_field": "text"},
             must_not_search_mapping={"text_field": "text"},
             # gte, lte, gt, lt supported
             rang_search_mapping={"text_field": {"gte": 0.1, "lte": 0.2}},
             limit=10


    Returns:
        List[Document]: A list of documents.

    """
    fromqdrant_client.http.modelsimport (
        FieldCondition,
        Filter,
        MatchText,
        MatchValue,
        Range,
    )
    fromqdrant_client.http.models.modelsimport Payload

    should_search_mapping = should_search_mapping or {}
    must_search_mapping = must_search_mapping or {}
    must_not_search_mapping = must_not_search_mapping or {}
    rang_search_mapping = rang_search_mapping or {}

    should_search_conditions = [
        FieldCondition(key=key, match=MatchText(text=value))
        for key, value in should_search_mapping.items()
        if should_search_mapping
    ]
    must_search_conditions = [
        FieldCondition(key=key, match=MatchValue(value=value))
        for key, value in must_search_mapping.items()
        if must_search_mapping
    ]
    must_not_search_conditions = [
        FieldCondition(key=key, match=MatchValue(value=value))
        for key, value in must_not_search_mapping.items()
        if must_not_search_mapping
    ]
    rang_search_conditions = [
        FieldCondition(
            key=key,
            range=Range(
                gte=value.get("gte"),
                lte=value.get("lte"),
                gt=value.get("gt"),
                lt=value.get("lt"),
            ),
        )
        for key, value in rang_search_mapping.items()
        if rang_search_mapping
    ]
    should_search_conditions.extend(rang_search_conditions)
    response = self._client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        query_filter=Filter(
            must=must_search_conditions,
            must_not=must_not_search_conditions,
            should=should_search_conditions,
        ),
        with_vectors=True,
        with_payload=True,
        limit=limit,
    )

    documents = []
    for point in response:
        payload = cast(Payload, point.payload)
        try:
            vector = cast(List[float], point.vector)
        except ValueError as e:
            raise ValueError("Could not cast vector to List[float].") frome
        document = Document(
            id_=payload.get("doc_id"),
            text=payload.get("text"),
            metadata=payload.get("metadata"),
            embedding=vector,
        )
        documents.append(document)

    return documents

```
 |  
| --- | --- |  
options: members: - QdrantReader
