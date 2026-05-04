# Vectara rag
##  VectaraRagPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/vectara_rag/#llama_index.packs.vectara_rag.VectaraRagPack "Permanent link")
Bases: 
Vectara RAG pack.
Source code in `llama-index-packs/llama-index-packs-vectara-rag/llama_index/packs/vectara_rag/base.py`  
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
```
 | 
```
classVectaraRagPack(BaseLlamaPack):
"""Vectara RAG pack."""

    def__init__(
        self,
        nodes: Optional[List[TextNode]] = None,
        similarity_top_k: int = 5,
        **kwargs: Any,
    ):
        self._index = VectaraIndex(nodes)
        vectara_kwargs = kwargs.get("vectara_kwargs", {})
        if "summary_enabled" not in vectara_kwargs:
            vectara_kwargs["summary_enabled"] = True
        self._query_engine = self._index.as_query_engine(
            similarity_top_k=similarity_top_k,
            **kwargs,
        )

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "index": self._index,
            "query_engine": self._query_engine,
        }

    defretrieve(self, query_str: str) -> Any:
"""Retrieve."""
        return self._query_engine.retrieve(query_str)

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        return self._query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/vectara_rag/#llama_index.packs.vectara_rag.VectaraRagPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-vectara-rag/llama_index/packs/vectara_rag/base.py`  
| 
```
28
29
30
31
32
33
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "index": self._index,
        "query_engine": self._query_engine,
    }

```
 |  
| --- | --- |  
###  retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/vectara_rag/#llama_index.packs.vectara_rag.VectaraRagPack.retrieve "Permanent link")

```
retrieve(query_str: ) -> 

```

Retrieve.
Source code in `llama-index-packs/llama-index-packs-vectara-rag/llama_index/packs/vectara_rag/base.py`  
| 
```
35
36
37
```
 | 
```
defretrieve(self, query_str: str) -> Any:
"""Retrieve."""
    return self._query_engine.retrieve(query_str)

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/vectara_rag/#llama_index.packs.vectara_rag.VectaraRagPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-vectara-rag/llama_index/packs/vectara_rag/base.py`  
| 
```
39
40
41
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return self._query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - VectaraRagPack
