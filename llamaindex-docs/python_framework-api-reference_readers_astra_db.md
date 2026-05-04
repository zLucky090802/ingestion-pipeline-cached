# Astra db
##  AstraDBReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/astra_db/#llama_index.readers.astra_db.AstraDBReader "Permanent link")
Bases: 
Astra DB reader.
Retrieve documents from an Astra DB Instance.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection_name`  |  collection name to use. If not existing, it will be created.  |  _required_  |  
|  `token`  |  The Astra DB Application Token to use.  |  _required_  |  
|  `api_endpoint`  |  The Astra DB JSON API endpoint for your database.  |  _required_  |  
|  `embedding_dimension`  |  Length of the embedding vectors in use.  |  _required_  |  
|  `namespace`  |  `Optional[str]`  |  The namespace to use. If not provided, 'default_keyspace'  |  `None`  |  
|  `client`  |  `Optional[Any]`  |  Astra DB client to use. If not provided, one will be created.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-astra-db/llama_index/readers/astra_db/base.py`  
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
```
 | 
```
classAstraDBReader(BaseReader):
"""
    Astra DB reader.

    Retrieve documents from an Astra DB Instance.

    Args:
        collection_name (str): collection name to use. If not existing, it will be created.
        token (str): The Astra DB Application Token to use.
        api_endpoint (str): The Astra DB JSON API endpoint for your database.
        embedding_dimension (int): Length of the embedding vectors in use.
        namespace (Optional[str]): The namespace to use. If not provided, 'default_keyspace'
        client (Optional[Any]): Astra DB client to use. If not provided, one will be created.

    """

    def__init__(
        self,
        *,
        collection_name: str,
        token: str,
        api_endpoint: str,
        embedding_dimension: int,
        namespace: Optional[str] = None,
        client: Optional[Any] = None,
    ) -> None:
"""Initialize with parameters."""
        import_err_msg = (
            "`astrapy` package not found, please run `pip install --upgrade astrapy`"
        )

        # Try to import astrapy for use
        try:
            fromastrapy.dbimport AstraDB
        except ImportError:
            raise ImportError(import_err_msg)

        if client is not None:
            self._client = client.copy()
            self._client.set_caller(
                caller_name=getattr(llama_index, "__name__", "llama_index"),
                caller_version=getattr(llama_index.core, "__version__", None),
            )
        else:
            # Build the Astra DB object
            self._client = AstraDB(
                api_endpoint=api_endpoint,
                token=token,
                namespace=namespace,
                caller_name=getattr(llama_index, "__name__", "llama_index"),
                caller_version=getattr(llama_index.core, "__version__", None),
            )

        self._collection = self._client.create_collection(
            collection_name=collection_name, dimension=embedding_dimension
        )

    defload_data(self, vector: List[float], limit: int = 10, **kwargs: Any) -> Any:
"""
        Load data from Astra DB.

        Args:
            vector (Any): Query
            limit (int): Number of results to return.
            kwargs (Any): Additional arguments to pass to the Astra DB query.

        Returns:
            List[Document]: A list of documents.

        """
        results = self._collection.vector_find(
            vector,
            limit=limit,
            fields=["*"],
            **kwargs,
        )

        documents: List[Document] = []
        for result in results:
            document = Document(
                doc_id=result["_id"],
                text=result["content"],
                embedding=result["$vector"],
            )

            documents.append(document)

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/astra_db/#llama_index.readers.astra_db.AstraDBReader.load_data "Permanent link")

```
load_data(
    vector: [float], limit:  = 10, **kwargs: 
) -> 

```

Load data from Astra DB.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `vector`  |  Query  |  _required_  |  
|  `limit`  |  Number of results to return.  |  
|  `kwargs`  |  Additional arguments to pass to the Astra DB query.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  List[Document]: A list of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-astra-db/llama_index/readers/astra_db/base.py`  
| 
```
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
```
 | 
```
defload_data(self, vector: List[float], limit: int = 10, **kwargs: Any) -> Any:
"""
    Load data from Astra DB.

    Args:
        vector (Any): Query
        limit (int): Number of results to return.
        kwargs (Any): Additional arguments to pass to the Astra DB query.

    Returns:
        List[Document]: A list of documents.

    """
    results = self._collection.vector_find(
        vector,
        limit=limit,
        fields=["*"],
        **kwargs,
    )

    documents: List[Document] = []
    for result in results:
        document = Document(
            doc_id=result["_id"],
            text=result["content"],
            embedding=result["$vector"],
        )

        documents.append(document)

    return documents

```
 |  
| --- | --- |  
options: members: - AstraDBReader
