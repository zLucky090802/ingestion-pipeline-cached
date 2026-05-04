# Metal
##  MetalReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/metal/#llama_index.readers.metal.MetalReader "Permanent link")
Bases: 
Metal reader.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  Metal API key.  |  _required_  |  
|  `client_id`  |  Metal client ID.  |  _required_  |  
|  `index_id`  |  Metal index ID.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-metal/llama_index/readers/metal/base.py`  
| 
```
 7
 8
 9
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
```
 | 
```
classMetalReader(BaseReader):
"""
    Metal reader.

    Args:
        api_key (str): Metal API key.
        client_id (str): Metal client ID.
        index_id (str): Metal index ID.

    """

    def__init__(self, api_key: str, client_id: str, index_id: str):
        import_err_msg = (
            "`metal_sdk` package not found, please run `pip install metal_sdk`"
        )
        try:
            importmetal_sdk  # noqa
        except ImportError:
            raise ImportError(import_err_msg)
        frommetal_sdk.metalimport Metal

"""Initialize with parameters."""
        self._api_key = api_key
        self._client_id = client_id
        self._index_id = index_id
        self.metal_client = Metal(api_key, client_id, index_id)

    defload_data(
        self,
        limit: int,
        query_embedding: Optional[List[float]] = None,
        filters: Optional[Dict[str, Any]] = None,
        separate_documents: bool = True,
        **query_kwargs: Any,
    ) -> List[Document]:
"""
        Load data from Metal.

        Args:
            query_embedding (Optional[List[float]]): Query embedding for search.
            limit (int): Number of results to return.
            filters (Optional[Dict[str, Any]]): Filters to apply to the search.
            separate_documents (Optional[bool]): Whether to return separate
                documents per retrieved entry. Defaults to True.
            **query_kwargs: Keyword arguments to pass to the search.

        Returns:
            List[Document]: A list of documents.

        """
        payload = {
            "embedding": query_embedding,
            "filters": filters,
        }
        response = self.metal_client.search(payload, limit=limit, **query_kwargs)

        documents = []
        for item in response["data"]:
            text = item["text"] or (item["metadata"] and item["metadata"]["text"])
            documents.append(Document(text=text))

        if not separate_documents:
            text_list = [doc.get_content() for doc in documents]
            text = "\n\n".join(text_list)
            documents = [Document(text=text)]

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/metal/#llama_index.readers.metal.MetalReader.load_data "Permanent link")

```
load_data(
    limit: ,
    query_embedding: Optional[[float]] = None,
    filters: Optional[[, ]] = None,
    separate_documents:  = True,
    **query_kwargs: 
) -> []

```

Load data from Metal.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_embedding`  |  `Optional[List[float]]`  |  Query embedding for search.  |  `None`  |  
|  `limit`  |  Number of results to return.  |  _required_  |  
|  `filters`  |  `Optional[Dict[str, Any]]`  |  Filters to apply to the search.  |  `None`  |  
|  `separate_documents`  |  `Optional[bool]`  |  Whether to return separate documents per retrieved entry. Defaults to True.  |  `True`  |  
|  `**query_kwargs`  |  Keyword arguments to pass to the search.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-metal/llama_index/readers/metal/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    limit: int,
    query_embedding: Optional[List[float]] = None,
    filters: Optional[Dict[str, Any]] = None,
    separate_documents: bool = True,
    **query_kwargs: Any,
) -> List[Document]:
"""
    Load data from Metal.

    Args:
        query_embedding (Optional[List[float]]): Query embedding for search.
        limit (int): Number of results to return.
        filters (Optional[Dict[str, Any]]): Filters to apply to the search.
        separate_documents (Optional[bool]): Whether to return separate
            documents per retrieved entry. Defaults to True.
        **query_kwargs: Keyword arguments to pass to the search.

    Returns:
        List[Document]: A list of documents.

    """
    payload = {
        "embedding": query_embedding,
        "filters": filters,
    }
    response = self.metal_client.search(payload, limit=limit, **query_kwargs)

    documents = []
    for item in response["data"]:
        text = item["text"] or (item["metadata"] and item["metadata"]["text"])
        documents.append(Document(text=text))

    if not separate_documents:
        text_list = [doc.get_content() for doc in documents]
        text = "\n\n".join(text_list)
        documents = [Document(text=text)]

    return documents

```
 |  
| --- | --- |  
options: members: - MetalReader
