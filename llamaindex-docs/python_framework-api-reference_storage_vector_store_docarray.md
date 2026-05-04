# Docarray
##  DocArrayHnswVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/docarray/#llama_index.vector_stores.docarray.DocArrayHnswVectorStore "Permanent link")
Bases: `DocArrayVectorStore`
Class representing a DocArray HNSW vector store.
This class is a lightweight Document Index implementation provided by Docarray. It stores vectors on disk in hnswlib, and stores all other data in SQLite.
Examples:
`pip install llama-index-vector-stores-docarray`

```
fromllama_index.vector_stores.docarrayimport DocArrayHnswVectorStore

# Initialize the DocArrayHnswVectorStore
vector_store = DocArrayHnswVectorStore(work_dir="hnsw_index", dim=1536)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-docarray/llama_index/vector_stores/docarray/hnsw.py`  
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
126
127
128
129
130
131
132
133
134
135
136
137
138
```
 | 
```
classDocArrayHnswVectorStore(DocArrayVectorStore):
"""
    Class representing a DocArray HNSW vector store.

    This class is a lightweight Document Index implementation provided by Docarray.
    It stores vectors on disk in hnswlib, and stores all other data in SQLite.

    Examples:
        `pip install llama-index-vector-stores-docarray`

        ```python
        from llama_index.vector_stores.docarray import DocArrayHnswVectorStore

        # Initialize the DocArrayHnswVectorStore
        vector_store = DocArrayHnswVectorStore(work_dir="hnsw_index", dim=1536)
        ```

    """

    def__init__(
        self,
        work_dir: str,
        dim: int = 1536,
        dist_metric: Literal["cosine", "ip", "l2"] = "cosine",
        max_elements: int = 1024,
        ef_construction: int = 200,
        ef: int = 10,
        M: int = 16,
        allow_replace_deleted: bool = True,
        num_threads: int = 1,
    ):
"""
        Initializes the DocArrayHnswVectorStore.

        Args:
            work_dir (str): The working directory.
            dim (int, optional): Dimensionality of the vectors. Default is 1536.
            dist_metric (Literal["cosine", "ip", "l2"], optional): The distance
                metric to use. Default is "cosine".
            max_elements (int, optional): defines the maximum number of elements
                that can be stored in the structure(can be increased/shrunk).
            ef_construction (int, optional): defines a construction time/accuracy
                trade-off. Default is 200.
            ef (int, optional): The size of the dynamic candidate list. Default is 10.
            M (int, optional): defines the maximum number of outgoing connections
                in the graph. Default is 16.
            allow_replace_deleted (bool, optional): Whether to allow replacing
                deleted elements. Default is True.
            num_threads (int, optional): Number of threads for index construction.
                Default is 1.

        """
        import_err_msg = """
                `docarray` package not found. Install the package via pip:
                `pip install docarray[hnswlib]`
        """
        try:
            importdocarray  # noqa
        except ImportError:
            raise ImportError(import_err_msg)

        self._work_dir = work_dir
        ref_docs_path = os.path.join(self._work_dir, "ref_docs.json")
        if os.path.exists(ref_docs_path):
            with open(ref_docs_path) as f:
                self._ref_docs = json.load(f)
        else:
            self._ref_docs = {}

        self._index, self._schema = self._init_index(
            dim=dim,
            dist_metric=dist_metric,
            max_elements=max_elements,
            ef_construction=ef_construction,
            ef=ef,
            M=M,
            allow_replace_deleted=allow_replace_deleted,
            num_threads=num_threads,
        )

    def_init_index(self, **kwargs: Any):  # type: ignore[no-untyped-def]
"""
        Initializes the HNSW document index.

        Args:
            **kwargs: Variable length argument list for the HNSW index.

        Returns:
            tuple: The HNSW document index and its schema.

        """
        fromdocarray.indeximport HnswDocumentIndex

        schema = self._get_schema(**kwargs)
        index = HnswDocumentIndex[schema]  # type: ignore[valid-type]
        return index(work_dir=self._work_dir), schema

    def_find_docs_to_be_removed(self, doc_id: str) -> List[str]:
"""
        Finds the documents to be removed from the vector store.

        Args:
            doc_id (str): Reference document ID that should be removed.

        Returns:
            List[str]: List of document IDs to be removed.

        """
        docs = self._ref_docs.get(doc_id, [])
        del self._ref_docs[doc_id]
        self._save_ref_docs()
        return docs

    def_save_ref_docs(self) -> None:
"""Saves reference documents."""
        with open(os.path.join(self._work_dir, "ref_docs.json"), "w") as f:
            json.dump(self._ref_docs, f)

    def_update_ref_docs(self, docs):  # type: ignore[no-untyped-def]
"""
        Updates reference documents.

        Args:
            docs (List): List of documents to update.

        """
        for doc in docs:
            if doc.metadata["doc_id"] not in self._ref_docs:
                self._ref_docs[doc.metadata["doc_id"]] = []
            self._ref_docs[doc.metadata["doc_id"]].append(doc.id)
        self._save_ref_docs()

```
 |  
| --- | --- |  
##  DocArrayInMemoryVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/docarray/#llama_index.vector_stores.docarray.DocArrayInMemoryVectorStore "Permanent link")
Bases: `DocArrayVectorStore`
Class representing a DocArray In-Memory vector store.
This class is a document index provided by Docarray that stores documents in memory.
Examples:
`pip install llama-index-vector-stores-docarray`

```
fromllama_index.vector_stores.docarrayimport DocArrayInMemoryVectorStore

# Create an instance of DocArrayInMemoryVectorStore
vector_store = DocArrayInMemoryVectorStore()

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-docarray/llama_index/vector_stores/docarray/in_memory.py`  
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
```
 | 
```
classDocArrayInMemoryVectorStore(DocArrayVectorStore):
"""
    Class representing a DocArray In-Memory vector store.

    This class is a document index provided by Docarray that stores documents in memory.

    Examples:
        `pip install llama-index-vector-stores-docarray`

        ```python
        from llama_index.vector_stores.docarray import DocArrayInMemoryVectorStore

        # Create an instance of DocArrayInMemoryVectorStore
        vector_store = DocArrayInMemoryVectorStore()
        ```

    """

    def__init__(
        self,
        index_path: Optional[str] = None,
        metric: Literal[
            "cosine_sim", "euclidian_dist", "sgeuclidean_dist"
        ] = "cosine_sim",
    ):
"""
        Initializes the DocArrayInMemoryVectorStore.

        Args:
            index_path (Optional[str]): The path to the index file.
            metric (Literal["cosine_sim", "euclidian_dist", "sgeuclidean_dist"]):
                The distance metric to use. Default is "cosine_sim".

        """
        import_err_msg = """
                `docarray` package not found. Install the package via pip:
                `pip install docarray`
        """
        try:
            importdocarray  # noqa
        except ImportError:
            raise ImportError(import_err_msg)

        self._ref_docs = None  # type: ignore[assignment]
        self._index_file_path = index_path
        self._index, self._schema = self._init_index(metric=metric)

    def_init_index(self, **kwargs: Any):  # type: ignore[no-untyped-def]
"""
        Initializes the in-memory exact nearest neighbour index.

        Args:
            **kwargs: Variable length argument list.

        Returns:
            tuple: The in-memory exact nearest neighbour index and its schema.

        """
        fromdocarray.indeximport InMemoryExactNNIndex

        schema = self._get_schema(**kwargs)
        index = InMemoryExactNNIndex[schema]  # type: ignore[valid-type]
        params = {"index_file_path": self._index_file_path}
        return index(**params), schema  # type: ignore[arg-type]

    def_find_docs_to_be_removed(self, doc_id: str) -> List[str]:
"""
        Finds the documents to be removed from the vector store.

        Args:
            doc_id (str): Reference document ID that should be removed.

        Returns:
            List[str]: List of document IDs to be removed.

        """
        query = {"metadata__doc_id": {"$eq": doc_id}}
        docs = self._index.filter(query)
        return [doc.id for doc in docs]

    defpersist(
        self, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
    ) -> None:
"""
        Persists the in-memory vector store to a file.

        Args:
            persist_path (str): The path to persist the index.
            fs (fsspec.AbstractFileSystem, optional): Filesystem to persist to.
                (doesn't apply)

        """
        index_path = persist_path or self._index_file_path
        self._index.persist(index_path)

```
 |  
| --- | --- |  
###  persist [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/docarray/#llama_index.vector_stores.docarray.DocArrayInMemoryVectorStore.persist "Permanent link")

```
persist(
    persist_path: ,
    fs: Optional[AbstractFileSystem] = None,
) -> None

```

Persists the in-memory vector store to a file.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `persist_path`  |  The path to persist the index.  |  _required_  |  
|  `AbstractFileSystem`  |  Filesystem to persist to. (doesn't apply)  |  `None`  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-docarray/llama_index/vector_stores/docarray/in_memory.py`  
| 
```
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
```
 | 
```
defpersist(
    self, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
) -> None:
"""
    Persists the in-memory vector store to a file.

    Args:
        persist_path (str): The path to persist the index.
        fs (fsspec.AbstractFileSystem, optional): Filesystem to persist to.
            (doesn't apply)

    """
    index_path = persist_path or self._index_file_path
    self._index.persist(index_path)

```
 |  
| --- | --- |  
options: members: - DocArrayHnswVectorStore - DocArrayInMemoryVectorStore
