# Awadb
##  AwadbReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/awadb/#llama_index.readers.awadb.AwadbReader "Permanent link")
Bases: 
Awadb reader.
Retrieves documents through an existing awadb client. These documents can then be used in a downstream LlamaIndex data structure.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `client`  |  `client`  |  An awadb client.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-awadb/llama_index/readers/awadb/base.py`  
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
```
 | 
```
classAwadbReader(BaseReader):
"""
    Awadb reader.

    Retrieves documents through an existing awadb client.
    These documents can then be used in a downstream LlamaIndex data structure.

    Args:
        client (awadb.client): An awadb client.

    """

    def__init__(self, client: Any):
"""Initialize with parameters."""
        import_err_msg = "`awadb` package not found, please run `pip install awadb`"
        try:
            pass
        except ImportError:
            raise ImportError(import_err_msg)

        self.awadb_client = client

    defload_data(
        self,
        query: np.ndarray,
        k: int = 4,
        separate_documents: bool = True,
    ) -> List[Document]:
"""
        Load data from Faiss.

        Args:
            query (np.ndarray): A 2D numpy array of query vectors.
            k (int): Number of nearest neighbors to retrieve. Defaults to 4.
            separate_documents (Optional[bool]): Whether to return separate
                documents. Defaults to True.

        Returns:
            List[Document]: A list of documents.

        """
        results = self.awadb_client.Search(
            query,
            k,
            text_in_page_content=None,
            meta_filter=None,
            not_include_fields=None,
        )
        documents = []
        for item_detail in results[0]["ResultItems"]:
            documents.append(Document(text=item_detail["embedding_text"]))

        if not separate_documents:
            # join all documents into one
            text_list = [doc.get_content() for doc in documents]
            text = "\n\n".join(text_list)
            documents = [Document(text=text)]

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/awadb/#llama_index.readers.awadb.AwadbReader.load_data "Permanent link")

```
load_data(
    query: ndarray,
    k:  = 4,
    separate_documents:  = True,
) -> []

```

Load data from Faiss.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  `ndarray`  |  A 2D numpy array of query vectors.  |  _required_  |  
|  Number of nearest neighbors to retrieve. Defaults to 4.  |  
|  `separate_documents`  |  `Optional[bool]`  |  Whether to return separate documents. Defaults to True.  |  `True`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-awadb/llama_index/readers/awadb/base.py`  
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
```
 | 
```
defload_data(
    self,
    query: np.ndarray,
    k: int = 4,
    separate_documents: bool = True,
) -> List[Document]:
"""
    Load data from Faiss.

    Args:
        query (np.ndarray): A 2D numpy array of query vectors.
        k (int): Number of nearest neighbors to retrieve. Defaults to 4.
        separate_documents (Optional[bool]): Whether to return separate
            documents. Defaults to True.

    Returns:
        List[Document]: A list of documents.

    """
    results = self.awadb_client.Search(
        query,
        k,
        text_in_page_content=None,
        meta_filter=None,
        not_include_fields=None,
    )
    documents = []
    for item_detail in results[0]["ResultItems"]:
        documents.append(Document(text=item_detail["embedding_text"]))

    if not separate_documents:
        # join all documents into one
        text_list = [doc.get_content() for doc in documents]
        text = "\n\n".join(text_list)
        documents = [Document(text=text)]

    return documents

```
 |  
| --- | --- |  
options: members: - AwadbReader
