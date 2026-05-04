# Txtai
##  TxtaiReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/txtai/#llama_index.readers.txtai.TxtaiReader "Permanent link")
Bases: 
txtai reader.
Retrieves documents through an existing in-memory txtai index. These documents can then be used in a downstream LlamaIndex data structure. If you wish use txtai itself as an index to to organize documents, insert documents, and perform queries on them, please use VectorStoreIndex with TxtaiVectorStore.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `txtai_index`  |  A txtai Index object (required)  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-txtai/llama_index/readers/txtai/base.py`  
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
```
 | 
```
classTxtaiReader(BaseReader):
"""
    txtai reader.

    Retrieves documents through an existing in-memory txtai index.
    These documents can then be used in a downstream LlamaIndex data structure.
    If you wish use txtai itself as an index to to organize documents,
    insert documents, and perform queries on them, please use VectorStoreIndex
    with TxtaiVectorStore.

    Args:
        txtai_index (txtai.ann.ANN): A txtai Index object (required)

    """

    def__init__(self, index: Any):
"""Initialize with parameters."""
        import_err_msg = """
            `txtai` package not found. For instructions on
            how to install `txtai` please visit
            https://neuml.github.io/txtai/install/
        """
        try:
            importtxtai  # noqa
        except ImportError:
            raise ImportError(import_err_msg)

        self._index = index

    defload_data(
        self,
        query: np.ndarray,
        id_to_text_map: Dict[str, str],
        k: int = 4,
        separate_documents: bool = True,
    ) -> List[Document]:
"""
        Load data from txtai index.

        Args:
            query (np.ndarray): A 2D numpy array of query vectors.
            id_to_text_map (Dict[str, str]): A map from ID's to text.
            k (int): Number of nearest neighbors to retrieve. Defaults to 4.
            separate_documents (Optional[bool]): Whether to return separate
                documents. Defaults to True.

        Returns:
            List[Document]: A list of documents.

        """
        search_result = self._index.search(query, k)
        documents = []
        for query_result in search_result:
            for doc_id, _ in query_result:
                doc_id = str(doc_id)
                if doc_id not in id_to_text_map:
                    raise ValueError(
                        f"Document ID {doc_id} not found in id_to_text_map."
                    )
                text = id_to_text_map[doc_id]
                documents.append(Document(text=text))

        if not separate_documents:
            # join all documents into one
            text_list = [doc.get_content() for doc in documents]
            text = "\n\n".join(text_list)
            documents = [Document(text=text)]

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/txtai/#llama_index.readers.txtai.TxtaiReader.load_data "Permanent link")

```
load_data(
    query: ndarray,
    id_to_text_map: [, ],
    k:  = 4,
    separate_documents:  = True,
) -> []

```

Load data from txtai index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  `ndarray`  |  A 2D numpy array of query vectors.  |  _required_  |  
|  `id_to_text_map`  |  `Dict[str, str]`  |  A map from ID's to text.  |  _required_  |  
|  Number of nearest neighbors to retrieve. Defaults to 4.  |  
|  `separate_documents`  |  `Optional[bool]`  |  Whether to return separate documents. Defaults to True.  |  `True`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-txtai/llama_index/readers/txtai/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    query: np.ndarray,
    id_to_text_map: Dict[str, str],
    k: int = 4,
    separate_documents: bool = True,
) -> List[Document]:
"""
    Load data from txtai index.

    Args:
        query (np.ndarray): A 2D numpy array of query vectors.
        id_to_text_map (Dict[str, str]): A map from ID's to text.
        k (int): Number of nearest neighbors to retrieve. Defaults to 4.
        separate_documents (Optional[bool]): Whether to return separate
            documents. Defaults to True.

    Returns:
        List[Document]: A list of documents.

    """
    search_result = self._index.search(query, k)
    documents = []
    for query_result in search_result:
        for doc_id, _ in query_result:
            doc_id = str(doc_id)
            if doc_id not in id_to_text_map:
                raise ValueError(
                    f"Document ID {doc_id} not found in id_to_text_map."
                )
            text = id_to_text_map[doc_id]
            documents.append(Document(text=text))

    if not separate_documents:
        # join all documents into one
        text_list = [doc.get_content() for doc in documents]
        text = "\n\n".join(text_list)
        documents = [Document(text=text)]

    return documents

```
 |  
| --- | --- |  
options: members: - TxtaiReader
