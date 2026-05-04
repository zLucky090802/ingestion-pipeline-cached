# Timescale vector autoretrieval
##  TimescaleVectorAutoretrievalPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/timescale_vector_autoretrieval/#llama_index.packs.timescale_vector_autoretrieval.TimescaleVectorAutoretrievalPack "Permanent link")
Bases: 
Timescale Vector auto-retrieval pack.
Source code in `llama-index-packs/llama-index-packs-timescale-vector-autoretrieval/llama_index/packs/timescale_vector_autoretrieval/base.py`  
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
```
 | 
```
classTimescaleVectorAutoretrievalPack(BaseLlamaPack):
"""Timescale Vector auto-retrieval pack."""

    def__init__(
        self,
        service_url: str,
        table_name: str,
        time_partition_interval: timedelta,
        vector_store_info: VectorStoreInfo,
        nodes: Optional[List[TextNode]] = None,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        self._vector_store = TimescaleVectorStore.from_params(
            service_url=service_url,
            table_name=table_name,
            time_partition_interval=time_partition_interval,
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

        self.retriever = VectorIndexAutoRetriever(
            self._index, vector_store_info=vector_store_info
        )
        self.query_engine = RetrieverQueryEngine(self.retriever)

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
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/timescale_vector_autoretrieval/#llama_index.packs.timescale_vector_autoretrieval.TimescaleVectorAutoretrievalPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-timescale-vector-autoretrieval/llama_index/packs/timescale_vector_autoretrieval/base.py`  
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
###  retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/timescale_vector_autoretrieval/#llama_index.packs.timescale_vector_autoretrieval.TimescaleVectorAutoretrievalPack.retrieve "Permanent link")

```
retrieve(query_str: ) -> 

```

Retrieve.
Source code in `llama-index-packs/llama-index-packs-timescale-vector-autoretrieval/llama_index/packs/timescale_vector_autoretrieval/base.py`  
| 
```
65
66
67
```
 | 
```
defretrieve(self, query_str: str) -> Any:
"""Retrieve."""
    return self.retriever.retrieve(query_str)

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/timescale_vector_autoretrieval/#llama_index.packs.timescale_vector_autoretrieval.TimescaleVectorAutoretrievalPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-timescale-vector-autoretrieval/llama_index/packs/timescale_vector_autoretrieval/base.py`  
| 
```
69
70
71
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - TimescaleVectorAutoretrievalPack
