# Solr
##  SolrReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/solr/#llama_index.readers.solr.SolrReader "Permanent link")
Bases: 
Read documents from a Solr index.
These documents can then be used in a downstream Llama Index data structure.
Source code in `llama-index-integrations/readers/llama-index-readers-solr/llama_index/readers/solr/base.py`  
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
```
 | 
```
classSolrReader(BasePydanticReader):
"""
    Read documents from a Solr index.

    These documents can then be used in a downstream Llama Index data structure.
    """

    endpoint: str = Field(description="Full endpoint, including collection info.")
    _client: Any = PrivateAttr()

    def__init__(
        self,
        endpoint: str,
    ):
"""Initialize with parameters."""
        super().__init__(endpoint=endpoint)
        self._client = pysolr.Solr(endpoint)

    defload_data(
        self,
        query: dict[str, Any],
        field: str,
        id_field: str = "id",
        metadata_fields: Optional[list[str]] = None,
        embedding: Optional[str] = None,
    ) -> list[Document]:
r"""
        Read data from the Solr index. At least one field argument must be specified.

        Args:
            query (dict): The Solr query parameters.
                - "q" is required.
                - "rows" should be specified or will default to 10 by Solr.
                - If "fl" is provided, it is respected exactly as given.
                  If "fl" is NOT provided, a default `fl` is constructed from
                  {id_field, field, embedding?, metadata_fields?}.
            field (str): Field in Solr to retrieve as document text.
            id_field (str): Field in Solr to retrieve as the document identifier. Defaults to "id".
            metadata_fields (list[str], optional): Fields to include as metadata. Defaults to None.
            embedding (str, optional): Field to use for embeddings. Defaults to None.

        Raises:
            ValueError: If the HTTP call to Solr fails.

        Returns:
            list[Document]: A list of retrieved documents where field is populated.

        """
        if "q" not in query:
            raise ValueError("Query parameters must include a 'q' field for the query.")

        fl_default = {}
        if "fl" not in query:
            fields = [id_field, field]
            if embedding:
                fields.append(embedding)
            if metadata_fields:
                fields.extend(metadata_fields)
            fl_default = {"fl": ",".join(fields)}

        try:
            query_params = {
                **query,
                **fl_default,
            }
            results = self._client.search(**query_params)
        except Exception as e:  # pragma: no cover
            raise ValueError(f"Failed to query Solr endpoint: {e!s}") frome

        documents: list[Document] = []
        for doc in results.docs:
            if field not in doc:
                continue

            doc_kwargs: dict[str, Any] = {
                "id_": str(doc[id_field]),
                "text": doc[field],
                **({"embedding": doc.get(embedding)} if embedding else {}),
                "metadata": {
                    metadata_field: doc[metadata_field]
                    for metadata_field in (metadata_fields or [])
                    if metadata_field in doc
                },
            }
            documents.append(Document(**doc_kwargs))
        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/solr/#llama_index.readers.solr.SolrReader.load_data "Permanent link")

```
load_data(
    query: [, ],
    field: ,
    id_field:  = "id",
    metadata_fields: Optional[[]] = None,
    embedding: Optional[] = None,
) -> []

```

Read data from the Solr index. At least one field argument must be specified.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  `dict`  |  The Solr query parameters. - "q" is required. - "rows" should be specified or will default to 10 by Solr. - If "fl" is provided, it is respected exactly as given. If "fl" is NOT provided, a default `fl` is constructed from {id_field, field, embedding?, metadata_fields?}.  |  _required_  |  
|  `field`  |  Field in Solr to retrieve as document text.  |  _required_  |  
|  `id_field`  |  Field in Solr to retrieve as the document identifier. Defaults to "id".  |  `'id'`  |  
|  `metadata_fields`  |  `list[str]`  |  Fields to include as metadata. Defaults to None.  |  `None`  |  
|  `embedding`  |  Field to use for embeddings. Defaults to None.  |  `None`  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If the HTTP call to Solr fails.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  list[Document]: A list of retrieved documents where field is populated.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-solr/llama_index/readers/solr/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    query: dict[str, Any],
    field: str,
    id_field: str = "id",
    metadata_fields: Optional[list[str]] = None,
    embedding: Optional[str] = None,
) -> list[Document]:
r"""
    Read data from the Solr index. At least one field argument must be specified.

    Args:
        query (dict): The Solr query parameters.
            - "q" is required.
            - "rows" should be specified or will default to 10 by Solr.
            - If "fl" is provided, it is respected exactly as given.
              If "fl" is NOT provided, a default `fl` is constructed from
              {id_field, field, embedding?, metadata_fields?}.
        field (str): Field in Solr to retrieve as document text.
        id_field (str): Field in Solr to retrieve as the document identifier. Defaults to "id".
        metadata_fields (list[str], optional): Fields to include as metadata. Defaults to None.
        embedding (str, optional): Field to use for embeddings. Defaults to None.

    Raises:
        ValueError: If the HTTP call to Solr fails.

    Returns:
        list[Document]: A list of retrieved documents where field is populated.

    """
    if "q" not in query:
        raise ValueError("Query parameters must include a 'q' field for the query.")

    fl_default = {}
    if "fl" not in query:
        fields = [id_field, field]
        if embedding:
            fields.append(embedding)
        if metadata_fields:
            fields.extend(metadata_fields)
        fl_default = {"fl": ",".join(fields)}

    try:
        query_params = {
            **query,
            **fl_default,
        }
        results = self._client.search(**query_params)
    except Exception as e:  # pragma: no cover
        raise ValueError(f"Failed to query Solr endpoint: {e!s}") frome

    documents: list[Document] = []
    for doc in results.docs:
        if field not in doc:
            continue

        doc_kwargs: dict[str, Any] = {
            "id_": str(doc[id_field]),
            "text": doc[field],
            **({"embedding": doc.get(embedding)} if embedding else {}),
            "metadata": {
                metadata_field: doc[metadata_field]
                for metadata_field in (metadata_fields or [])
                if metadata_field in doc
            },
        }
        documents.append(Document(**doc_kwargs))
    return documents

```
 |  
| --- | --- |  
options: members: - SolrReader
