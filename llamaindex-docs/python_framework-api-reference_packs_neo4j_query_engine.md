# Neo4j query engine
##  Neo4jQueryEnginePack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/neo4j_query_engine/#llama_index.packs.neo4j_query_engine.Neo4jQueryEnginePack "Permanent link")
Bases: 
Neo4j Query Engine pack.
Source code in `llama-index-packs/llama-index-packs-neo4j-query-engine/llama_index/packs/neo4j_query_engine/base.py`  
| 
```
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
157
158
159
160
161
162
163
164
```
 | 
```
classNeo4jQueryEnginePack(BaseLlamaPack):
"""Neo4j Query Engine pack."""

    def__init__(
        self,
        username: str,
        password: str,
        url: str,
        database: str,
        docs: List[Document],
        query_engine_type: Optional[Neo4jQueryEngineType] = None,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        neo4j_graph_store = Neo4jGraphStore(
            username=username,
            password=password,
            url=url,
            database=database,
        )

        neo4j_storage_context = StorageContext.from_defaults(
            graph_store=neo4j_graph_store
        )

        # define LLM
        self.llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")
        Settings.llm = self.llm

        neo4j_index = KnowledgeGraphIndex.from_documents(
            documents=docs,
            storage_context=neo4j_storage_context,
            max_triplets_per_chunk=10,
            include_embeddings=True,
        )

        # create node parser to parse nodes from document
        node_parser = SentenceSplitter(chunk_size=512)

        # use transforms directly
        nodes = node_parser(docs)
        print(f"loaded nodes with {len(nodes)} nodes")

        # based on the nodes, create index
        vector_index = VectorStoreIndex(nodes=nodes)

        if query_engine_type == Neo4jQueryEngineType.KG_KEYWORD:
            # KG keyword-based entity retrieval
            self.query_engine = neo4j_index.as_query_engine(
                # setting to false uses the raw triplets instead of adding the text from the corresponding nodes
                include_text=False,
                retriever_mode="keyword",
                response_mode="tree_summarize",
            )

        elif query_engine_type == Neo4jQueryEngineType.KG_HYBRID:
            # KG hybrid entity retrieval
            self.query_engine = neo4j_index.as_query_engine(
                include_text=True,
                response_mode="tree_summarize",
                embedding_mode="hybrid",
                similarity_top_k=3,
                explore_global_knowledge=True,
            )

        elif query_engine_type == Neo4jQueryEngineType.RAW_VECTOR:
            # Raw vector index retrieval
            self.query_engine = vector_index.as_query_engine()

        elif query_engine_type == Neo4jQueryEngineType.RAW_VECTOR_KG_COMBO:
            fromllama_index.core.query_engineimport RetrieverQueryEngine

            # create neo4j custom retriever
            neo4j_vector_retriever = VectorIndexRetriever(index=vector_index)
            neo4j_kg_retriever = KGTableRetriever(
                index=neo4j_index, retriever_mode="keyword", include_text=False
            )
            neo4j_custom_retriever = CustomRetriever(
                neo4j_vector_retriever, neo4j_kg_retriever
            )

            # create neo4j response synthesizer
            neo4j_response_synthesizer = get_response_synthesizer(
                response_mode="tree_summarize"
            )

            # Custom combo query engine
            self.query_engine = RetrieverQueryEngine(
                retriever=neo4j_custom_retriever,
                response_synthesizer=neo4j_response_synthesizer,
            )

        elif query_engine_type == Neo4jQueryEngineType.KG_QE:
            # using KnowledgeGraphQueryEngine
            fromllama_index.core.query_engineimport KnowledgeGraphQueryEngine

            self.query_engine = KnowledgeGraphQueryEngine(
                storage_context=neo4j_storage_context,
                llm=self.llm,
                verbose=True,
            )

        elif query_engine_type == Neo4jQueryEngineType.KG_RAG_RETRIEVER:
            # using KnowledgeGraphRAGRetriever
            fromllama_index.core.query_engineimport RetrieverQueryEngine
            fromllama_index.core.retrieversimport KnowledgeGraphRAGRetriever

            neo4j_graph_rag_retriever = KnowledgeGraphRAGRetriever(
                storage_context=neo4j_storage_context,
                llm=self.llm,
                verbose=True,
            )

            self.query_engine = RetrieverQueryEngine.from_args(
                neo4j_graph_rag_retriever
            )

        else:
            # KG vector-based entity retrieval
            self.query_engine = neo4j_index.as_query_engine()

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {"llm": self.llm, "query_engine": self.query_engine}

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/neo4j_query_engine/#llama_index.packs.neo4j_query_engine.Neo4jQueryEnginePack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-neo4j-query-engine/llama_index/packs/neo4j_query_engine/base.py`  
| 
```
158
159
160
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {"llm": self.llm, "query_engine": self.query_engine}

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/neo4j_query_engine/#llama_index.packs.neo4j_query_engine.Neo4jQueryEnginePack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-neo4j-query-engine/llama_index/packs/neo4j_query_engine/base.py`  
| 
```
162
163
164
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - Neo4jQueryEnginePack
