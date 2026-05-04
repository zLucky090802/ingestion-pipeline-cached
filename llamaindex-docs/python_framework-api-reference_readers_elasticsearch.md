# Elasticsearch
##  ElasticsearchReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/elasticsearch/#llama_index.readers.elasticsearch.ElasticsearchReader "Permanent link")
Bases: 
Read documents from an Elasticsearch/Opensearch index.
These documents can then be used in a downstream Llama Index data structure.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `endpoint`  |  URL (http/https) of cluster  |  _required_  |  
|  `index`  |  Name of the index (required)  |  _required_  |  
|  `httpx_client_args`  |  `dict`  |  Optional additional args to pass to the `httpx.Client`  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-elasticsearch/llama_index/readers/elasticsearch/base.py`  
| 
```
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
```
 | 
```
classElasticsearchReader(BasePydanticReader):
"""
    Read documents from an Elasticsearch/Opensearch index.

    These documents can then be used in a downstream Llama Index data structure.

    Args:
        endpoint (str): URL (http/https) of cluster
        index (str): Name of the index (required)
        httpx_client_args (dict): Optional additional args to pass to the `httpx.Client`

    """

    is_remote: bool = True
    endpoint: str
    index: str
    httpx_client_args: Optional[dict] = None

    _client: Any = PrivateAttr()

    def__init__(
        self, endpoint: str, index: str, httpx_client_args: Optional[dict] = None
    ):
"""Initialize with parameters."""
        super().__init__(
            endpoint=endpoint, index=index, httpx_client_args=httpx_client_args
        )
        import_err_msg = """
            `httpx` package not found. Install via `pip install httpx`
        """
        try:
            importhttpx
        except ImportError:
            raise ImportError(import_err_msg)
        self._client = httpx.Client(base_url=endpoint, **(httpx_client_args or {}))

    @classmethod
    defclass_name(cls) -> str:
        return "ElasticsearchReader"

    defload_data(
        self,
        field: str,
        query: Optional[dict] = None,
        embedding_field: Optional[str] = None,
        metadata_fields: Optional[List[str]] = None,
    ) -> List[Document]:
"""
        Read data from the Elasticsearch index.

        Args:
            field (str): Field in the document to retrieve text from
            query (Optional[dict]): Elasticsearch JSON query DSL object.
                For example:
                {"query": {"match": {"message": {"query": "this is a test"}}}}
            embedding_field (Optional[str]): If there are embeddings stored in
                this index, this field can be used
                to set the embedding field on the returned Document list.
            metadata_fields (Optional[List[str]]): Fields used as metadata. Default
                is all fields in the document except those specified by the
                field and embedding_field parameters.

        Returns:
            List[Document]: A list of documents.

        """
        res = self._client.post(f"{self.index}/_search", json=query).json()
        documents = []
        for hit in res["hits"]["hits"]:
            doc_id = hit["_id"]
            value = hit["_source"][field]
            embedding = hit["_source"].get(embedding_field or "", None)
            if metadata_fields:
                metadata = {
                    k: v for k, v in hit["_source"].items() if k in metadata_fields
                }
            else:
                hit["_source"].pop(field)
                hit["_source"].pop(embedding_field or "", None)
                metadata = hit["_source"]
            documents.append(
                Document(id_=doc_id, text=value, metadata=metadata, embedding=embedding)
            )
        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/elasticsearch/#llama_index.readers.elasticsearch.ElasticsearchReader.load_data "Permanent link")

```
load_data(
    field: ,
    query: Optional[] = None,
    embedding_field: Optional[] = None,
    metadata_fields: Optional[[]] = None,
) -> []

```

Read data from the Elasticsearch index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `field`  |  Field in the document to retrieve text from  |  _required_  |  
|  `query`  |  `Optional[dict]`  |  Elasticsearch JSON query DSL object. For example: {"query": {"match": {"message": {"query": "this is a test"}}}}  |  `None`  |  
|  `embedding_field`  |  `Optional[str]`  |  If there are embeddings stored in this index, this field can be used to set the embedding field on the returned Document list.  |  `None`  |  
|  `metadata_fields`  |  `Optional[List[str]]`  |  Fields used as metadata. Default is all fields in the document except those specified by the field and embedding_field parameters.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-elasticsearch/llama_index/readers/elasticsearch/base.py`  
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
96
97
98
```
 | 
```
defload_data(
    self,
    field: str,
    query: Optional[dict] = None,
    embedding_field: Optional[str] = None,
    metadata_fields: Optional[List[str]] = None,
) -> List[Document]:
"""
    Read data from the Elasticsearch index.

    Args:
        field (str): Field in the document to retrieve text from
        query (Optional[dict]): Elasticsearch JSON query DSL object.
            For example:
            {"query": {"match": {"message": {"query": "this is a test"}}}}
        embedding_field (Optional[str]): If there are embeddings stored in
            this index, this field can be used
            to set the embedding field on the returned Document list.
        metadata_fields (Optional[List[str]]): Fields used as metadata. Default
            is all fields in the document except those specified by the
            field and embedding_field parameters.

    Returns:
        List[Document]: A list of documents.

    """
    res = self._client.post(f"{self.index}/_search", json=query).json()
    documents = []
    for hit in res["hits"]["hits"]:
        doc_id = hit["_id"]
        value = hit["_source"][field]
        embedding = hit["_source"].get(embedding_field or "", None)
        if metadata_fields:
            metadata = {
                k: v for k, v in hit["_source"].items() if k in metadata_fields
            }
        else:
            hit["_source"].pop(field)
            hit["_source"].pop(embedding_field or "", None)
            metadata = hit["_source"]
        documents.append(
            Document(id_=doc_id, text=value, metadata=metadata, embedding=embedding)
        )
    return documents

```
 |  
| --- | --- |  
options: members: - ElasticsearchReader
