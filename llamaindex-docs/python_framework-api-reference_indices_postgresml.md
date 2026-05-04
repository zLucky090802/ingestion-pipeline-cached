# Postgresml
##  PostgresMLIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/postgresml/#llama_index.indices.managed.postgresml.PostgresMLIndex "Permanent link")
Bases: `BaseManagedIndex`
PostgresML Index.
The PostgresML index implements a managed index that uses PostgresML as the backend. PostgresML performs a lot of the functions in traditional indexes in the backend: - breaks down a document into chunks (nodes) - Creates the embedding for each chunk (node) - Performs the search for the top k most similar nodes to a query - Optionally can perform text-generation or chat completion
Source code in `llama-index-integrations/indices/llama-index-indices-managed-postgresml/llama_index/indices/managed/postgresml/base.py`  
| 
```
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
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
```
 | 
```
classPostgresMLIndex(BaseManagedIndex):
"""
    PostgresML Index.

    The PostgresML index implements a managed index that uses PostgresML as the backend.
    PostgresML performs a lot of the functions in traditional indexes in the backend:
    - breaks down a document into chunks (nodes)
    - Creates the embedding for each chunk (node)
    - Performs the search for the top k most similar nodes to a query
    - Optionally can perform text-generation or chat completion
    """

    def__init__(
        self,
        collection_name: str,
        pipeline_name: Optional[str] = None,
        pipeline_schema: Optional[Dict[str, Any]] = None,
        pgml_database_url: Optional[str] = None,
        show_progress: bool = True,
        upsert_parallel_batches: int = 1,
        nodes: Optional[Sequence[BaseNode]] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize the PostgresML SDK."""
        self.show_progress = show_progress
        self.upsert_parallel_batches = upsert_parallel_batches

        index_struct = PostgresMLIndexStruct(
            index_id=collection_name,
            summary="PostgresML Index",
        )

        super().__init__(
            show_progress=show_progress,
            index_struct=index_struct,
            **kwargs,
        )

        # Create our Collection and Pipeline
        self.collection = Collection(collection_name, pgml_database_url)
        if pipeline_name is None:
            pipeline_name = "v1"
        if pipeline_schema is None:
            pipeline_schema = {
                "content": {
                    "splitter": {
                        "model": "recursive_character",
                        "parameters": {"chunk_size": 1500},
                    },
                    "semantic_search": {
                        "model": "intfloat/e5-small-v2",
                        "parameters": {"prompt": "passage: "},
                    },
                }
            }
        self.pipeline = Pipeline(pipeline_name, pipeline_schema)

        # We must wrap self.collection.add_pipeline() with this async function
        # This is a limitation of the pyo3 async implementation
        async defadd_pipeline():
            await self.collection.add_pipeline(self.pipeline)

        run_async_tasks([add_pipeline()])

        if nodes:
            self._insert(nodes)

    def_insert(
        self,
        nodes: Sequence[BaseNode],
        **insert_kwargs: Any,
    ) -> None:
"""Insert a set of documents (each a node)."""
        documents = [
            {
                "id": node.node_id,
                "content": node.get_content(),
                "metadata": node.metadata,
            }
            for node in nodes
        ]

        args = {"parallel_batches": self.upsert_parallel_batches, **insert_kwargs}

        # We must wrap self.collection.upsert_documents() with this async function
        # This is a limitation of the pyo3 async implementation
        async defupsert_documents():
            await self.collection.upsert_documents(documents, args)

        run_async_tasks([upsert_documents()])

    defadd_documents(
        self,
        docs: Sequence[Document],
        **insert_kwargs: Any,
    ) -> None:
        nodes = [TextNode(**doc.dict()) for doc in docs]
        self._insert(nodes, **insert_kwargs)

    defdelete_ref_doc(self, ref_doc_id: str) -> None:
        # We must wrap self.collection.delete_documents() with this async function
        # This is a limitation of the pyo3 async implementation
        async defdelete_documents():
            await self.collection.delete_documents({"id": {"$eq": ref_doc_id}})

        run_async_tasks([delete_documents()])

    defupdate_ref_doc(self, document: Document) -> None:
        node = TextNode(**document.dict())
        self._insert([node], merge=True)

    defas_retriever(self, **kwargs: Any) -> BaseRetriever:
"""Return a Retriever for this managed index."""
        fromllama_index.indices.managed.postgresml.retrieverimport (
            PostgresMLRetriever,
        )

        return PostgresMLRetriever(self, **kwargs)

    defas_query_engine(self, **kwargs: Any) -> BaseQueryEngine:
        fromllama_index.indices.managed.postgresml.retrieverimport (
            PostgresMLRetriever,
        )
        fromllama_index.indices.managed.postgresml.queryimport (
            PostgresMLQueryEngine,
        )

        return PostgresMLQueryEngine(PostgresMLRetriever(self, **kwargs), **kwargs)

    @classmethod
    deffrom_documents(
        cls: Type[IndexType],
        documents: Sequence[Document],
        collection_name: Optional[str] = None,
        pipeline_name: Optional[str] = None,
        pipeline_schema: Optional[Dict[str, Any]] = None,
        pgml_database_url: Optional[str] = None,
        show_progress: bool = False,
        upsert_parallel_batches: int = 1,
        **kwargs: Any,
    ) -> IndexType:
"""Build a PostgresML index from a sequence of documents."""
        if collection_name is None:
            raise Exception("collection_name is a required argument")
        nodes = [TextNode(**doc.dict()) for doc in documents]
        return cls(
            collection_name,
            pipeline_name=pipeline_name,
            pipeline_schema=pipeline_schema,
            pgml_database_url=pgml_database_url,
            nodes=nodes,
            show_progress=show_progress,
            upsert_parallel_batches=upsert_parallel_batches,
            **kwargs,
        )

```
 |  
| --- | --- |  
###  as_retriever [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/postgresml/#llama_index.indices.managed.postgresml.PostgresMLIndex.as_retriever "Permanent link")

```
as_retriever(**kwargs: ) -> 

```

Return a Retriever for this managed index.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-postgresml/llama_index/indices/managed/postgresml/base.py`  
| 
```
151
152
153
154
155
156
157
```
 | 
```
defas_retriever(self, **kwargs: Any) -> BaseRetriever:
"""Return a Retriever for this managed index."""
    fromllama_index.indices.managed.postgresml.retrieverimport (
        PostgresMLRetriever,
    )

    return PostgresMLRetriever(self, **kwargs)

```
 |  
| --- | --- |  
###  from_documents `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/postgresml/#llama_index.indices.managed.postgresml.PostgresMLIndex.from_documents "Permanent link")

```
from_documents(
    documents: Sequence[],
    collection_name: Optional[] = None,
    pipeline_name: Optional[] = None,
    pipeline_schema: Optional[[, ]] = None,
    pgml_database_url: Optional[] = None,
    show_progress:  = False,
    upsert_parallel_batches:  = 1,
    **kwargs: 
) -> IndexType

```

Build a PostgresML index from a sequence of documents.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-postgresml/llama_index/indices/managed/postgresml/base.py`  
| 
```
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
```
 | 
```
@classmethod
deffrom_documents(
    cls: Type[IndexType],
    documents: Sequence[Document],
    collection_name: Optional[str] = None,
    pipeline_name: Optional[str] = None,
    pipeline_schema: Optional[Dict[str, Any]] = None,
    pgml_database_url: Optional[str] = None,
    show_progress: bool = False,
    upsert_parallel_batches: int = 1,
    **kwargs: Any,
) -> IndexType:
"""Build a PostgresML index from a sequence of documents."""
    if collection_name is None:
        raise Exception("collection_name is a required argument")
    nodes = [TextNode(**doc.dict()) for doc in documents]
    return cls(
        collection_name,
        pipeline_name=pipeline_name,
        pipeline_schema=pipeline_schema,
        pgml_database_url=pgml_database_url,
        nodes=nodes,
        show_progress=show_progress,
        upsert_parallel_batches=upsert_parallel_batches,
        **kwargs,
    )

```
 |  
| --- | --- |  
##  PostgresMLRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/postgresml/#llama_index.indices.managed.postgresml.PostgresMLRetriever "Permanent link")
Bases: 
PostgresML Retriever.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index`  |   |  the PostgresML Index  |  _required_  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-postgresml/llama_index/indices/managed/postgresml/retriever.py`  
| 
```
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
```
 | 
```
classPostgresMLRetriever(BaseRetriever):
"""
    PostgresML Retriever.

    Args:
        index (PostgresMLIndex): the PostgresML Index

    """

    def__init__(
        self,
        index: PostgresMLIndex,
        callback_manager: Optional[CallbackManager] = None,
        pgml_query: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = 5,
        rerank: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> None:
"""Initialize params."""
        self._index = index
        self._pgml_query = pgml_query
        self._limit = limit
        self._rerank = rerank
        super().__init__(callback_manager)

    def_retrieve(
        self,
        query_bundle: Optional[QueryBundle] = None,
        **kwargs: Any,
    ) -> List[NodeWithScore]:
        return run_async_tasks([self._aretrieve(query_bundle, **kwargs)])[0]

    async def_aretrieve(
        self,
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
        async defdo_vector_search():
            if self._pgml_query:
                return await self._index.collection.vector_search(
                    self._pgml_query,
                    self._index.pipeline,
                )
            else:
                if not query_bundle:
                    raise Exception(
                        "Must provide either query or query_bundle to retrieve and aretrieve"
                    )
                if self._rerank is not None:
                    self._rerank = self._rerank | {"query": query_bundle.query_str}
                return await self._index.collection.vector_search(
                    {
                        "query": {
                            "fields": {
                                "content": {
                                    "query": query_bundle.query_str,
                                    "parameters": {"prompt": "query: "},
                                }
                            }
                        },
                        "rerank": self._rerank,
                        "limit": self._limit,
                    },
                    self._index.pipeline,
                )

        results = await do_vector_search()
        return [
            NodeWithScore(
                node=TextNode(
                    id_=r["document"]["id"],
                    text=r["chunk"],
                    metadata=r["document"]["metadata"],
                ),
                score=r["score"],
            )
            if self._rerank is None
            else NodeWithScore(
                node=TextNode(
                    id_=r["document"]["id"],
                    text=r["chunk"],
                    metadata=r["document"]["metadata"],
                ),
                score=r["rerank_score"],
            )
            for r in results
        ]

```
 |  
| --- | --- |  
options: members: - PostgresMLRetriever - PostgresmlIndex
