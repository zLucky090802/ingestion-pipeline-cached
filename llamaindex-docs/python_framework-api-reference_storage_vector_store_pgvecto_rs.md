# Pgvecto rs
##  PGVectoRsStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/pgvecto_rs/#llama_index.vector_stores.pgvecto_rs.PGVectoRsStore "Permanent link")
Bases: 
PGVectoRs Vector Store.
Examples:
`pip install llama-index-vector-stores-pgvecto-rs`

```
fromllama_index.vector_stores.pgvecto_rsimport PGVectoRsStore

# Setup PGVectoRs client
frompgvecto_rs.sdkimport PGVectoRs
importos

URL = "postgresql+psycopg://{username}:{password}@{host}:{port}/{db_name}".format(
    port=os.getenv("DB_PORT", "5432"),
    host=os.getenv("DB_HOST", "localhost"),
    username=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASS", "mysecretpassword"),
    db_name=os.getenv("DB_NAME", "postgres"),
)

client = PGVectoRs(
    db_url=URL,
    collection_name="example",
    dimension=1536,  # Using OpenAI’s text-embedding-ada-002
)

# Initialize PGVectoRsStore
vector_store = PGVectoRsStore(client=client)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-pgvecto-rs/llama_index/vector_stores/pgvecto_rs/base.py`  
| 
```
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
```
 | 
```
classPGVectoRsStore(BasePydanticVectorStore):
"""
    PGVectoRs Vector Store.

    Examples:
        `pip install llama-index-vector-stores-pgvecto-rs`

        ```python
        from llama_index.vector_stores.pgvecto_rs import PGVectoRsStore

        # Setup PGVectoRs client
        from pgvecto_rs.sdk import PGVectoRs
        import os

        URL = "postgresql+psycopg://{username}:{password}@{host}:{port}/{db_name}".format(
            port=os.getenv("DB_PORT", "5432"),
            host=os.getenv("DB_HOST", "localhost"),
            username=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", "mysecretpassword"),
            db_name=os.getenv("DB_NAME", "postgres"),


        client = PGVectoRs(
            db_url=URL,
            collection_name="example",
            dimension=1536,  # Using OpenAI’s text-embedding-ada-002


        # Initialize PGVectoRsStore
        vector_store = PGVectoRsStore(client=client)
        ```

    """

    stores_text: bool = True

    _client: "PGVectoRs" = PrivateAttr()

    def__init__(self, client: "PGVectoRs") -> None:
        super().__init__()
        self._client: PGVectoRs = client

    @classmethod
    defclass_name(cls) -> str:
        return "PGVectoRsStore"

    @property
    defclient(self) -> Any:
        return self._client

    defadd(
        self,
        nodes: List[BaseNode],
    ) -> List[str]:
        records = [
            Record(
                id=node.id_,
                text=node.get_content(metadata_mode=MetadataMode.NONE),
                meta=node_to_metadata_dict(node, remove_text=True),
                embedding=node.get_embedding(),
            )
            for node in nodes
        ]

        self._client.insert(records)
        return [node.id_ for node in nodes]

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        self._client.delete(meta_contains({"ref_doc_id": ref_doc_id}))

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        results = self._client.search(
            embedding=query.query_embedding,
            top_k=query.similarity_top_k,
            filter=(
                meta_contains(
                    {pair.key: pair.value for pair in query.filters.legacy_filters()}
                )
                if query.filters is not None
                else None
            ),
        )

        nodes = [
            metadata_dict_to_node(record.meta, text=record.text)
            for record, _ in results
        ]

        return VectorStoreQueryResult(
            nodes=nodes,
            similarities=[score for _, score in results],
            ids=[str(record.id) for record, _ in results],
        )

```
 |  
| --- | --- |  
options: members: - PGVectoRsStore
