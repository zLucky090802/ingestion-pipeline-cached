# Zep
##  ZepReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/zep/#llama_index.readers.zep.ZepReader "Permanent link")
Bases: 
Zep document vector store reader.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_url`  |  Zep API URL  |  _required_  |  
|  `api_key`  |  Zep API key, optional  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-zep/llama_index/readers/zep/base.py`  
| 
```
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
74
75
76
77
```
 | 
```
classZepReader(BaseReader):
"""
    Zep document vector store reader.

    Args:
        api_url (str): Zep API URL
        api_key (str): Zep API key, optional

    """

    def__init__(self, api_url: str, api_key: Optional[str] = None):
"""Initialize with parameters."""
        fromzep_pythonimport ZepClient

        self._api_url = api_url
        self._api_key = api_key
        self._client = ZepClient(base_url=api_url, api_key=api_key)

    defload_data(
        self,
        collection_name: str,
        query: Optional[str] = None,
        vector: Optional[List[float]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        top_k: Optional[int] = 5,
        separate_documents: Optional[bool] = True,
        include_values: Optional[bool] = True,
    ) -> List[Document]:
"""
        Load data from Zep.

        Args:
            collection_name (str): Name of the Zep collection.
            query (Optional[str]): Query string. Required if vector is None.
            vector (Optional[List[float]]): Query vector. Required if query is None.
            metadata (Optional[Dict[str, Any]]): Metadata to filter on.
            top_k (Optional[int]): Number of results to return. Defaults to 5.
            separate_documents (Optional[bool]): Whether to return separate
                documents per retrieved entry. Defaults to True.
            include_values (Optional[bool]): Whether to include the embedding in
                the response. Defaults to True.

        Returns:
            List[Document]: A list of documents.

        """
        if query is None and vector is None:
            raise ValueError("Either query or vector must be specified.")

        collection = self._client.document.get_collection(name=collection_name)
        response = collection.search(
            text=query, embedding=vector, limit=top_k, metadata=metadata
        )

        documents = [
            (
                Document(text=d.content, embedding=d.embedding)
                if include_values
                else Document(text=d.content)
            )
            for d in response
        ]

        if not separate_documents:
            text_list = [d.get_text() for d in documents]
            text = "\n\n".join(text_list)
            documents = [Document(text=text)]

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/zep/#llama_index.readers.zep.ZepReader.load_data "Permanent link")

```
load_data(
    collection_name: ,
    query: Optional[] = None,
    vector: Optional[[float]] = None,
    metadata: Optional[[, ]] = None,
    top_k: Optional[] = 5,
    separate_documents: Optional[] = True,
    include_values: Optional[] = True,
) -> []

```

Load data from Zep.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection_name`  |  Name of the Zep collection.  |  _required_  |  
|  `query`  |  `Optional[str]`  |  Query string. Required if vector is None.  |  `None`  |  
|  `vector`  |  `Optional[List[float]]`  |  Query vector. Required if query is None.  |  `None`  |  
|  `metadata`  |  `Optional[Dict[str, Any]]`  |  Metadata to filter on.  |  `None`  |  
|  `top_k`  |  `Optional[int]`  |  Number of results to return. Defaults to 5.  |  
|  `separate_documents`  |  `Optional[bool]`  |  Whether to return separate documents per retrieved entry. Defaults to True.  |  `True`  |  
|  `include_values`  |  `Optional[bool]`  |  Whether to include the embedding in the response. Defaults to True.  |  `True`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-zep/llama_index/readers/zep/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    collection_name: str,
    query: Optional[str] = None,
    vector: Optional[List[float]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    top_k: Optional[int] = 5,
    separate_documents: Optional[bool] = True,
    include_values: Optional[bool] = True,
) -> List[Document]:
"""
    Load data from Zep.

    Args:
        collection_name (str): Name of the Zep collection.
        query (Optional[str]): Query string. Required if vector is None.
        vector (Optional[List[float]]): Query vector. Required if query is None.
        metadata (Optional[Dict[str, Any]]): Metadata to filter on.
        top_k (Optional[int]): Number of results to return. Defaults to 5.
        separate_documents (Optional[bool]): Whether to return separate
            documents per retrieved entry. Defaults to True.
        include_values (Optional[bool]): Whether to include the embedding in
            the response. Defaults to True.

    Returns:
        List[Document]: A list of documents.

    """
    if query is None and vector is None:
        raise ValueError("Either query or vector must be specified.")

    collection = self._client.document.get_collection(name=collection_name)
    response = collection.search(
        text=query, embedding=vector, limit=top_k, metadata=metadata
    )

    documents = [
        (
            Document(text=d.content, embedding=d.embedding)
            if include_values
            else Document(text=d.content)
        )
        for d in response
    ]

    if not separate_documents:
        text_list = [d.get_text() for d in documents]
        text = "\n\n".join(text_list)
        documents = [Document(text=text)]

    return documents

```
 |  
| --- | --- |  
options: members: - ZepReader
