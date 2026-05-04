# Fusion retriever
##  HybridFusionRetrieverPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/fusion_retriever/#llama_index.packs.fusion_retriever.HybridFusionRetrieverPack "Permanent link")
Bases: 
Hybrid fusion retriever pack.
Ensembles vector and bm25 retrievers using fusion.
Source code in `llama-index-packs/llama-index-packs-fusion-retriever/llama_index/packs/fusion_retriever/hybrid_fusion/base.py`  
| 
```
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
```
 | 
```
classHybridFusionRetrieverPack(BaseLlamaPack):
"""
    Hybrid fusion retriever pack.

    Ensembles vector and bm25 retrievers using fusion.

    """

    def__init__(
        self,
        nodes: List[TextNode] = None,
        chunk_size: int = 256,
        mode: str = "reciprocal_rerank",
        vector_similarity_top_k: int = 2,
        bm25_similarity_top_k: int = 2,
        fusion_similarity_top_k: int = 2,
        num_queries: int = 4,
        documents: List[Document] = None,
        cache_dir: str = None,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        Settings.chunk_size = chunk_size
        if cache_dir is not None and os.path.exists(cache_dir):
            # Load from cache
            fromllama_indeximport StorageContext, load_index_from_storage

            # rebuild storage context
            storage_context = StorageContext.from_defaults(persist_dir=cache_dir)
            # load index
            index = load_index_from_storage(storage_context)
        elif documents is not None:
            index = VectorStoreIndex.from_documents(documents=documents)
        else:
            index = VectorStoreIndex(nodes)

        if cache_dir is not None and not os.path.exists(cache_dir):
            index.storage_context.persist(persist_dir=cache_dir)

        self.vector_retriever = index.as_retriever(
            similarity_top_k=vector_similarity_top_k
        )

        self.bm25_retriever = BM25Retriever.from_defaults(
            docstore=index.docstore, similarity_top_k=bm25_similarity_top_k
        )
        self.fusion_retriever = QueryFusionRetriever(
            [self.vector_retriever, self.bm25_retriever],
            similarity_top_k=fusion_similarity_top_k,
            num_queries=num_queries,  # set this to 1 to disable query generation
            mode=mode,
            use_async=True,
            verbose=True,
            # query_gen_prompt="...",  # we could override the query generation prompt here
        )

        self.query_engine = RetrieverQueryEngine.from_args(self.fusion_retriever)

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "vector_retriever": self.vector_retriever,
            "bm25_retriever": self.bm25_retriever,
            "fusion_retriever": self.fusion_retriever,
            "query_engine": self.query_engine,
        }

    defretrieve(self, query_str: str) -> Any:
"""Retrieve."""
        return self.fusion_retriever.retrieve(query_str)

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/fusion_retriever/#llama_index.packs.fusion_retriever.HybridFusionRetrieverPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-fusion-retriever/llama_index/packs/fusion_retriever/hybrid_fusion/base.py`  
| 
```
73
74
75
76
77
78
79
80
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "vector_retriever": self.vector_retriever,
        "bm25_retriever": self.bm25_retriever,
        "fusion_retriever": self.fusion_retriever,
        "query_engine": self.query_engine,
    }

```
 |  
| --- | --- |  
###  retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/fusion_retriever/#llama_index.packs.fusion_retriever.HybridFusionRetrieverPack.retrieve "Permanent link")

```
retrieve(query_str: ) -> 

```

Retrieve.
Source code in `llama-index-packs/llama-index-packs-fusion-retriever/llama_index/packs/fusion_retriever/hybrid_fusion/base.py`  
| 
```
82
83
84
```
 | 
```
defretrieve(self, query_str: str) -> Any:
"""Retrieve."""
    return self.fusion_retriever.retrieve(query_str)

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/fusion_retriever/#llama_index.packs.fusion_retriever.HybridFusionRetrieverPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-fusion-retriever/llama_index/packs/fusion_retriever/hybrid_fusion/base.py`  
| 
```
86
87
88
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
##  QueryRewritingRetrieverPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/fusion_retriever/#llama_index.packs.fusion_retriever.QueryRewritingRetrieverPack "Permanent link")
Bases: 
Query rewriting retriever pack.
Given input nodes, build a vector index.
Then rewrite the query into multiple queries and rerank the results.
Source code in `llama-index-packs/llama-index-packs-fusion-retriever/llama_index/packs/fusion_retriever/query_rewrite/base.py`  
| 
```
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
```
 | 
```
classQueryRewritingRetrieverPack(BaseLlamaPack):
"""
    Query rewriting retriever pack.

    Given input nodes, build a vector index.

    Then rewrite the query into multiple queries and
    rerank the results.

    """

    def__init__(
        self,
        nodes: List[TextNode] = None,
        chunk_size: int = 256,
        mode: str = "reciprocal_rerank",
        vector_similarity_top_k: int = 2,
        fusion_similarity_top_k: int = 2,
        num_queries: int = 4,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        Settings.chunk_size = chunk_size
        index = VectorStoreIndex(nodes)
        self.vector_retriever = index.as_retriever(
            similarity_top_k=vector_similarity_top_k
        )

        self.fusion_retriever = QueryFusionRetriever(
            [self.vector_retriever],
            similarity_top_k=fusion_similarity_top_k,
            num_queries=num_queries,  # set this to 1 to disable query generation
            mode=mode,
            use_async=True,
            verbose=True,
            # query_gen_prompt="...",  # we could override the query generation prompt here
        )

        self.query_engine = RetrieverQueryEngine.from_args(self.fusion_retriever)

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "vector_retriever": self.vector_retriever,
            "fusion_retriever": self.fusion_retriever,
            "query_engine": self.query_engine,
        }

    defretrieve(self, query_str: str) -> Any:
"""Retrieve."""
        return self.fusion_retriever.retrieve(query_str)

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/fusion_retriever/#llama_index.packs.fusion_retriever.QueryRewritingRetrieverPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-fusion-retriever/llama_index/packs/fusion_retriever/query_rewrite/base.py`  
| 
```
53
54
55
56
57
58
59
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "vector_retriever": self.vector_retriever,
        "fusion_retriever": self.fusion_retriever,
        "query_engine": self.query_engine,
    }

```
 |  
| --- | --- |  
###  retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/fusion_retriever/#llama_index.packs.fusion_retriever.QueryRewritingRetrieverPack.retrieve "Permanent link")

```
retrieve(query_str: ) -> 

```

Retrieve.
Source code in `llama-index-packs/llama-index-packs-fusion-retriever/llama_index/packs/fusion_retriever/query_rewrite/base.py`  
| 
```
61
62
63
```
 | 
```
defretrieve(self, query_str: str) -> Any:
"""Retrieve."""
    return self.fusion_retriever.retrieve(query_str)

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/fusion_retriever/#llama_index.packs.fusion_retriever.QueryRewritingRetrieverPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-fusion-retriever/llama_index/packs/fusion_retriever/query_rewrite/base.py`  
| 
```
65
66
67
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - HybridFusionRetrieverPack - QueryRewritingRetrieverPack
