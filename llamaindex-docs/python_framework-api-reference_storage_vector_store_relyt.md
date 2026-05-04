# Relyt
##  RelytVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/relyt/#llama_index.vector_stores.relyt.RelytVectorStore "Permanent link")
Bases: 
Relyt Vector Store.
Examples:
`pip install llama-index-vector-stores-relyt`

```
fromllama_index.vector_stores.relytimport RelytVectorStore

# Setup relyt client
frompgvecto_rs.sdkimport PGVectoRs
importos

URL = "postgresql+psycopg://{username}:{password}@{host}:{port}/{db_name}".format(
    port=os.getenv("RELYT_PORT", "5432"),
    host=os.getenv("RELYT_HOST", "localhost"),
    username=os.getenv("RELYT_USER", "postgres"),
    password=os.getenv("RELYT_PASS", "mysecretpassword"),
    db_name=os.getenv("RELYT_NAME", "postgres"),
)

client = PGVectoRs(
    db_url=URL,
    collection_name="example",
    dimension=1536,  # Using OpenAI’s text-embedding-ada-002
)

# Initialize RelytVectorStore
vector_store = RelytVectorStore(client=client)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-relyt/llama_index/vector_stores/relyt/base.py`  
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
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
```
 | 
```
classRelytVectorStore(BasePydanticVectorStore):
"""
    Relyt Vector Store.

    Examples:
        `pip install llama-index-vector-stores-relyt`

        ```python
        from llama_index.vector_stores.relyt import RelytVectorStore

        # Setup relyt client
        from pgvecto_rs.sdk import PGVectoRs
        import os

        URL = "postgresql+psycopg://{username}:{password}@{host}:{port}/{db_name}".format(
            port=os.getenv("RELYT_PORT", "5432"),
            host=os.getenv("RELYT_HOST", "localhost"),
            username=os.getenv("RELYT_USER", "postgres"),
            password=os.getenv("RELYT_PASS", "mysecretpassword"),
            db_name=os.getenv("RELYT_NAME", "postgres"),


        client = PGVectoRs(
            db_url=URL,
            collection_name="example",
            dimension=1536,  # Using OpenAI’s text-embedding-ada-002


        # Initialize RelytVectorStore
        vector_store = RelytVectorStore(client=client)
        ```

    """

    stores_text: bool = True

    _client: "PGVectoRs" = PrivateAttr()
    _collection_name: str = PrivateAttr()

    def__init__(self, client: "PGVectoRs", collection_name: str) -> None:
        super().__init__()

        self._client: PGVectoRs = client
        self._collection_name = collection_name
        self.init_index()

    @classmethod
    defclass_name(cls) -> str:
        return "RelytStore"

    definit_index(self):
        index_name = f"idx_{self._collection_name}_embedding"
        with self._client._engine.connect() as conn:
            with conn.begin():
                index_query = text(
                    f"""
                        SELECT 1
                        FROM pg_indexes
                        WHERE indexname = '{index_name}';

                )
                result = conn.execute(index_query).scalar()
                if not result:
                    index_statement = text(
                        f"""
                            CREATE INDEX {index_name}
                            ON collection_{self._collection_name}
                            USING vectors (embedding vector_l2_ops)
                            WITH (options = $$
                            optimizing.optimizing_threads = 30
                            segment.max_growing_segment_size = 2000
                            segment.max_sealed_segment_size = 30000000
                            [indexing.hnsw]

                            ef_construction=500


                    )
                    conn.execute(index_statement)

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

    defdrop(self) -> None:
        self._client.drop()

    # TODO: the more filter type(le, ne, ge ...) will add later, after the base api supported,
    #  now only support eq filter for meta information
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
options: members: - RelytVectorStore
