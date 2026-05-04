# Deeplake deepmemory retriever
##  DeepMemoryRetrieverPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/deeplake_deepmemory_retriever/#llama_index.packs.deeplake_deepmemory_retriever.DeepMemoryRetrieverPack "Permanent link")
Bases: 
DeepMemory retriever pack.
Source code in `llama-index-packs/llama-index-packs-deeplake-deepmemory-retriever/llama_index/packs/deeplake_deepmemory_retriever/base.py`  
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
68
69
```
 | 
```
classDeepMemoryRetrieverPack(BaseLlamaPack):
"""DeepMemory retriever pack."""

    def__init__(
        self,
        dataset_path: str = "llama_index",
        token: Optional[str] = None,
        read_only: Optional[bool] = False,
        overwrite: bool = False,
        verbose: bool = True,
        nodes: Optional[List[TextNode]] = None,
        top_k: int = 4,
        **kwargs: Any,
    ):
        self._vector_store = DeepLakeVectorStore(
            dataset_path=dataset_path,
            token=token,
            read_only=read_only,
            overwrite=overwrite,
            verbose=verbose,
        )

        if nodes is not None:
            self._storage_context = StorageContext.from_defaults(
                vector_store=self._vector_store
            )
            self._index = VectorStoreIndex(
                nodes, storage_context=self._storage_context, **kwargs
            )
        else:
            self._index = VectorStoreIndex.from_vector_store(
                self._vector_store, **kwargs
            )
            self._storage_context = self._index.storage_context

        self.retriever = self._index.as_retriever(
            similarity_top_k=top_k, vector_store_kwargs={"deep_memory": True}
        )
        self.query_engine = RetrieverQueryEngine.from_args(retriever=self.retriever)

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "vector_store": self._vector_store,
            "storage_context": self._storage_context,
            "index": self._index,
            "retriever": self.retriever,
            "query_engine": self.query_engine,
        }

    defretrieve(self, query_str: str) -> Any:
"""Retrieve."""
        return self.retriever.retrieve(query_str)

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/deeplake_deepmemory_retriever/#llama_index.packs.deeplake_deepmemory_retriever.DeepMemoryRetrieverPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-deeplake-deepmemory-retriever/llama_index/packs/deeplake_deepmemory_retriever/base.py`  
| 
```
53
54
55
56
57
58
59
60
61
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "vector_store": self._vector_store,
        "storage_context": self._storage_context,
        "index": self._index,
        "retriever": self.retriever,
        "query_engine": self.query_engine,
    }

```
 |  
| --- | --- |  
###  retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/deeplake_deepmemory_retriever/#llama_index.packs.deeplake_deepmemory_retriever.DeepMemoryRetrieverPack.retrieve "Permanent link")

```
retrieve(query_str: ) -> 

```

Retrieve.
Source code in `llama-index-packs/llama-index-packs-deeplake-deepmemory-retriever/llama_index/packs/deeplake_deepmemory_retriever/base.py`  
| 
```
63
64
65
```
 | 
```
defretrieve(self, query_str: str) -> Any:
"""Retrieve."""
    return self.retriever.retrieve(query_str)

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/deeplake_deepmemory_retriever/#llama_index.packs.deeplake_deepmemory_retriever.DeepMemoryRetrieverPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-deeplake-deepmemory-retriever/llama_index/packs/deeplake_deepmemory_retriever/base.py`  
| 
```
67
68
69
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - DeepMemoryRetrieverPack
