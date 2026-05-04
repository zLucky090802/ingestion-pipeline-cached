# Deeplake multimodal retrieval
##  DeepLakeMultimodalRetrieverPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/deeplake_multimodal_retrieval/#llama_index.packs.deeplake_multimodal_retrieval.DeepLakeMultimodalRetrieverPack "Permanent link")
Bases: 
DeepLake Multimodal retriever pack.
Source code in `llama-index-packs/llama-index-packs-deeplake-multimodal-retrieval/llama_index/packs/deeplake_multimodal_retrieval/base.py`  
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
```
 | 
```
classDeepLakeMultimodalRetrieverPack(BaseLlamaPack):
"""DeepLake Multimodal retriever pack."""

    def__init__(
        self,
        dataset_path: str = "llama_index",
        token: Optional[str] = None,
        read_only: Optional[bool] = False,
        overwrite: bool = False,
        verbose: bool = True,
        nodes: Optional[List[BaseNode]] = None,
        top_k: int = 4,
        **kwargs: Any,
    ):
        # text vector store
        self._text_vectorstore = DeepLakeVectorStore(
            dataset_path=dataset_path + "_text",
            token=token,
            read_only=read_only,
            overwrite=overwrite,
            verbose=verbose,
        )

        # image vector store
        self._image_vectorstore = DeepLakeVectorStore(
            dataset_path=dataset_path + "_image",
            token=token,
            read_only=read_only,
            overwrite=overwrite,
            verbose=verbose,
        )

        if nodes is not None:
            self._storage_context = StorageContext.from_defaults(
                vector_store=self._text_vectorstore
            )
            self._index = MultiModalVectorStoreIndex(
                nodes,
                storage_context=self._storage_context,
                image_vector_store=self._image_vectorstore,
            )
        else:
            self._storage_context = StorageContext.from_defaults(
                vector_store=self._text_vectorstore
            )
            self._index = MultiModalVectorStoreIndex.from_vector_store(
                self._text_vectorstore,
                image_vector_store=self._image_vectorstore,
            )
        self.retriever = self._index.as_retriever(
            similarity_top_k=top_k, vector_store_kwargs={"deep_memory": True}
        )
        self.query_engine = SimpleMultiModalQueryEngine(self.retriever)

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "text_vectorstore": self._text_vectorstore,
            "image_vectorstore": self._image_vectorstore,
            "storage_context": self._storage_context,
            "index": self._index,
            "retriever": self.retriever,
            "query_engine": self.query_engine,
        }

    defretrieve(self, query_str: str) -> Any:
"""Retrieve."""
        return self.query_engine.retrieve(query_str)

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/deeplake_multimodal_retrieval/#llama_index.packs.deeplake_multimodal_retrieval.DeepLakeMultimodalRetrieverPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-deeplake-multimodal-retrieval/llama_index/packs/deeplake_multimodal_retrieval/base.py`  
| 
```
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
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "text_vectorstore": self._text_vectorstore,
        "image_vectorstore": self._image_vectorstore,
        "storage_context": self._storage_context,
        "index": self._index,
        "retriever": self.retriever,
        "query_engine": self.query_engine,
    }

```
 |  
| --- | --- |  
###  retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/deeplake_multimodal_retrieval/#llama_index.packs.deeplake_multimodal_retrieval.DeepLakeMultimodalRetrieverPack.retrieve "Permanent link")

```
retrieve(query_str: ) -> 

```

Retrieve.
Source code in `llama-index-packs/llama-index-packs-deeplake-multimodal-retrieval/llama_index/packs/deeplake_multimodal_retrieval/base.py`  
| 
```
78
79
80
```
 | 
```
defretrieve(self, query_str: str) -> Any:
"""Retrieve."""
    return self.query_engine.retrieve(query_str)

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/deeplake_multimodal_retrieval/#llama_index.packs.deeplake_multimodal_retrieval.DeepLakeMultimodalRetrieverPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-deeplake-multimodal-retrieval/llama_index/packs/deeplake_multimodal_retrieval/base.py`  
| 
```
82
83
84
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - DeepLakeMultimodalRetrieverPack
