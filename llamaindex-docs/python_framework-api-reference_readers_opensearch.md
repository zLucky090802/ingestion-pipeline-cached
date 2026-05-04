# Opensearch
##  OpensearchReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/opensearch/#llama_index.readers.opensearch.OpensearchReader "Permanent link")
Bases: 
Read documents from an Opensearch index.
These documents can then be used in a downstream Llama Index data structure.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `endpoint`  |  URL (http/https) of cluster without port  |  _required_  |  
|  `index`  |  Name of the index (required)  |  _required_  |  
|  `basic_auth`  |  basic authentication username password  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-opensearch/llama_index/readers/opensearch/base.py`  
| 
```
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
```
 | 
```
classOpensearchReader(BaseReader):
"""
    Read documents from an Opensearch index.

    These documents can then be used in a downstream Llama Index data structure.

    Args:
        endpoint (str): URL (http/https) of cluster without port
        index (str): Name of the index (required)
        basic_auth (set): basic authentication username password

    """

    def__init__(
        self, host: str, port: int, index: str, basic_auth: Optional[set] = None
    ):
"""Initialize with parameters."""
        fromopensearchpyimport OpenSearch

        self._opster_client = OpenSearch(
            hosts=[{"host": host, "port": port}],
            http_compress=True,  # enables gzip compression for request bodies
            http_auth=basic_auth,
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )
        self._index = index

    defload_data(
        self,
        field: str,
        query: Optional[dict] = None,
        embedding_field: Optional[str] = None,
    ) -> List[Document]:
"""
        Read data from the Opensearch index.

        Args:
            field (str): Field in the document to retrieve text from
            query (Optional[dict]): Opensearch JSON query DSL object.
                For example:
                { "query" : {"match": {"message": {"query": "this is a test"}}}}
            embedding_field (Optional[str]): If there are embeddings stored in
                this index, this field can be used
                to set the embedding field on the returned Document list.


        Returns:
            List[Document]: A list of documents.

        """
        res = self._opster_client.search(body=query, index=self._index)
        documents = []
        for hit in res["hits"]["hits"]:
            value = hit["_source"][field]
            _ = hit["_source"].pop(field)
            embedding = hit["_source"].get(embedding_field or "", None)
            documents.append(
                Document(text=value, extra_info=hit["_source"], embedding=embedding)
            )
        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/opensearch/#llama_index.readers.opensearch.OpensearchReader.load_data "Permanent link")

```
load_data(
    field: ,
    query: Optional[] = None,
    embedding_field: Optional[] = None,
) -> []

```

Read data from the Opensearch index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `field`  |  Field in the document to retrieve text from  |  _required_  |  
|  `query`  |  `Optional[dict]`  |  Opensearch JSON query DSL object. For example: { "query" : {"match": {"message": {"query": "this is a test"}}}}  |  `None`  |  
|  `embedding_field`  |  `Optional[str]`  |  If there are embeddings stored in this index, this field can be used to set the embedding field on the returned Document list.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-opensearch/llama_index/readers/opensearch/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    field: str,
    query: Optional[dict] = None,
    embedding_field: Optional[str] = None,
) -> List[Document]:
"""
    Read data from the Opensearch index.

    Args:
        field (str): Field in the document to retrieve text from
        query (Optional[dict]): Opensearch JSON query DSL object.
            For example:
            { "query" : {"match": {"message": {"query": "this is a test"}}}}
        embedding_field (Optional[str]): If there are embeddings stored in
            this index, this field can be used
            to set the embedding field on the returned Document list.


    Returns:
        List[Document]: A list of documents.

    """
    res = self._opster_client.search(body=query, index=self._index)
    documents = []
    for hit in res["hits"]["hits"]:
        value = hit["_source"][field]
        _ = hit["_source"].pop(field)
        embedding = hit["_source"].get(embedding_field or "", None)
        documents.append(
            Document(text=value, extra_info=hit["_source"], embedding=embedding)
        )
    return documents

```
 |  
| --- | --- |  
options: members: - OpensearchReader
