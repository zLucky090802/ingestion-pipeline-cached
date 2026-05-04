# Azcognitive search
##  AzCognitiveSearchReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/azcognitive_search/#llama_index.readers.azcognitive_search.AzCognitiveSearchReader "Permanent link")
Bases: 
General reader for any Azure Cognitive Search index reader.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `service_name`  |  the name of azure cognitive search service.  |  _required_  |  
|  `search_key`  |  provide azure search access key directly.  |  _required_  |  
|  `index`  |  index name  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-azcognitive-search/llama_index/readers/azcognitive_search/base.py`  
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
```
 | 
```
classAzCognitiveSearchReader(BaseReader):
"""
    General reader for any Azure Cognitive Search index reader.

    Args:
        service_name (str): the name of azure cognitive search service.
        search_key (str): provide azure search access key directly.
        index (str): index name

    """

    def__init__(self, service_name: str, searck_key: str, index: str) -> None:
"""Initialize Azure cognitive search service using the search key."""
        importlogging

        logger = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
        logger.setLevel(logging.WARNING)

        azure_credential = AzureKeyCredential(searck_key)

        self.search_client = SearchClient(
            endpoint=f"https://{service_name}.search.windows.net",
            index_name=index,
            credential=azure_credential,
        )

    defload_data(
        self, query: str, content_field: str, filter: Optional[str] = None
    ) -> List[Document]:
"""
        Read data from azure cognitive search index.

        Args:
            query (str): search term in Azure Search index
            content_field (str): field name of the document content.
            filter (str): Filter expression. For example : 'sourcepage eq
                'employee_handbook-3.pdf' and sourcefile eq 'employee_handbook.pdf''

        Returns:
            List[Document]: A list of documents.

        """
        search_result = self.search_client.search(query, filter=filter)

        return [
            Document(
                text=result[content_field],
                extra_info={"id": result["id"], "score": result["@search.score"]},
            )
            for result in search_result
        ]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/azcognitive_search/#llama_index.readers.azcognitive_search.AzCognitiveSearchReader.load_data "Permanent link")

```
load_data(
    query: ,
    content_field: ,
    filter: Optional[] = None,
) -> []

```

Read data from azure cognitive search index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  search term in Azure Search index  |  _required_  |  
|  `content_field`  |  field name of the document content.  |  _required_  |  
|  `filter`  |  Filter expression. For example : 'sourcepage eq 'employee_handbook-3.pdf' and sourcefile eq 'employee_handbook.pdf''  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-azcognitive-search/llama_index/readers/azcognitive_search/base.py`  
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
```
 | 
```
defload_data(
    self, query: str, content_field: str, filter: Optional[str] = None
) -> List[Document]:
"""
    Read data from azure cognitive search index.

    Args:
        query (str): search term in Azure Search index
        content_field (str): field name of the document content.
        filter (str): Filter expression. For example : 'sourcepage eq
            'employee_handbook-3.pdf' and sourcefile eq 'employee_handbook.pdf''

    Returns:
        List[Document]: A list of documents.

    """
    search_result = self.search_client.search(query, filter=filter)

    return [
        Document(
            text=result[content_field],
            extra_info={"id": result["id"], "score": result["@search.score"]},
        )
        for result in search_result
    ]

```
 |  
| --- | --- |  
options: members: - AzCognitiveSearchReader
