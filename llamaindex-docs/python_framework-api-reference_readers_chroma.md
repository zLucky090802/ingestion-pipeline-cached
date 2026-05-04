# Chroma
##  ChromaReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/chroma/#llama_index.readers.chroma.ChromaReader "Permanent link")
Bases: 
Chroma reader.
Retrieve documents from existing persisted Chroma collections.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collection_name`  |  Name of the persisted collection.  |  _required_  |  
|  `persist_directory`  |  `Optional[str]`  |  Directory where the collection is persisted.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-chroma/llama_index/readers/chroma/base.py`  
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
```
 | 
```
classChromaReader(BaseReader):
"""
    Chroma reader.

    Retrieve documents from existing persisted Chroma collections.

    Args:
        collection_name: Name of the persisted collection.
        persist_directory: Directory where the collection is persisted.

    """

    def__init__(
        self,
        collection_name: str,
        persist_directory: Optional[str] = None,
        chroma_api_impl: str = "rest",
        chroma_db_impl: Optional[str] = None,
        host: str = "localhost",
        port: int = 8000,
    ) -> None:
"""Initialize with parameters."""
        import_err_msg = (
            "`chromadb` package not found, please run `pip install chromadb`"
        )
        try:
            importchromadb
        except ImportError:
            raise ImportError(import_err_msg)

        if collection_name is None:
            raise ValueError("Please provide a collection name.")
        # from chromadb.config import Settings

        if persist_directory is not None:
            self._client = chromadb.PersistentClient(
                path=persist_directory if persist_directory else "./chroma",
            )
        elif (host is not None) or (port is not None):
            self._client = chromadb.HttpClient(
                host=host,
                port=port,
            )

        self._collection = self._client.get_collection(collection_name)

    defcreate_documents(self, results: Any) -> List[Document]:
"""
        Create documents from the results.

        Args:
            results: Results from the query.

        Returns:
            List of documents.

        """
        documents = []
        for result in zip(
            results["ids"][0],
            results["documents"][0],
            results["embeddings"][0],
            results["metadatas"][0],
        ):
            document = Document(
                id_=result[0],
                text=result[1],
                embedding=result[2],
                metadata=result[3],
            )
            documents.append(document)

        return documents

    defload_data(
        self,
        query_embedding: Optional[List[float]] = None,
        limit: int = 10,
        where: Optional[dict] = None,
        where_document: Optional[dict] = None,
        query: Optional[Union[str, List[str]]] = None,
    ) -> Any:
"""
        Load data from the collection.

        Args:
            limit: Number of results to return.
            where: Filter results by metadata. {"metadata_field": "is_equal_to_this"}
            where_document: Filter results by document. {"$contains":"search_string"}

        Returns:
            List of documents.

        """
        where = where or {}
        where_document = where_document or {}
        if query_embedding is not None:
            results = self._collection.search(
                query_embedding=query_embedding,
                n_results=limit,
                where=where,
                where_document=where_document,
                include=["metadatas", "documents", "distances", "embeddings"],
            )
            return self.create_documents(results)
        elif query is not None:
            query = query if isinstance(query, list) else [query]
            results = self._collection.query(
                query_texts=query,
                n_results=limit,
                where=where,
                where_document=where_document,
                include=["metadatas", "documents", "distances", "embeddings"],
            )
            return self.create_documents(results)
        else:
            raise ValueError("Please provide either query embedding or query.")

```
 |  
| --- | --- |  
###  create_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/chroma/#llama_index.readers.chroma.ChromaReader.create_documents "Permanent link")

```
create_documents(results: ) -> []

```

Create documents from the results.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `results`  |  Results from the query.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-chroma/llama_index/readers/chroma/base.py`  
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
```
 | 
```
defcreate_documents(self, results: Any) -> List[Document]:
"""
    Create documents from the results.

    Args:
        results: Results from the query.

    Returns:
        List of documents.

    """
    documents = []
    for result in zip(
        results["ids"][0],
        results["documents"][0],
        results["embeddings"][0],
        results["metadatas"][0],
    ):
        document = Document(
            id_=result[0],
            text=result[1],
            embedding=result[2],
            metadata=result[3],
        )
        documents.append(document)

    return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/chroma/#llama_index.readers.chroma.ChromaReader.load_data "Permanent link")

```
load_data(
    query_embedding: Optional[[float]] = None,
    limit:  = 10,
    where: Optional[] = None,
    where_document: Optional[] = None,
    query: Optional[Union[, []]] = None,
) -> 

```

Load data from the collection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `limit`  |  Number of results to return.  |  
|  `where`  |  `Optional[dict]`  |  Filter results by metadata. {"metadata_field": "is_equal_to_this"}  |  `None`  |  
|  `where_document`  |  `Optional[dict]`  |  Filter results by document. {"$contains":"search_string"}  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-chroma/llama_index/readers/chroma/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    query_embedding: Optional[List[float]] = None,
    limit: int = 10,
    where: Optional[dict] = None,
    where_document: Optional[dict] = None,
    query: Optional[Union[str, List[str]]] = None,
) -> Any:
"""
    Load data from the collection.

    Args:
        limit: Number of results to return.
        where: Filter results by metadata. {"metadata_field": "is_equal_to_this"}
        where_document: Filter results by document. {"$contains":"search_string"}

    Returns:
        List of documents.

    """
    where = where or {}
    where_document = where_document or {}
    if query_embedding is not None:
        results = self._collection.search(
            query_embedding=query_embedding,
            n_results=limit,
            where=where,
            where_document=where_document,
            include=["metadatas", "documents", "distances", "embeddings"],
        )
        return self.create_documents(results)
    elif query is not None:
        query = query if isinstance(query, list) else [query]
        results = self._collection.query(
            query_texts=query,
            n_results=limit,
            where=where,
            where_document=where_document,
            include=["metadatas", "documents", "distances", "embeddings"],
        )
        return self.create_documents(results)
    else:
        raise ValueError("Please provide either query embedding or query.")

```
 |  
| --- | --- |  
options: members: - ChromaReader
