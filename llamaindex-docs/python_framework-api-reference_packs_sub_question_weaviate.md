# Sub question weaviate
##  WeaviateSubQuestionPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/sub_question_weaviate/#llama_index.packs.sub_question_weaviate.WeaviateSubQuestionPack "Permanent link")
Bases: 
Weaviate Sub-Question query engine pack.
Source code in `llama-index-packs/llama-index-packs-sub-question-weaviate/llama_index/packs/sub_question_weaviate/base.py`  
| 
```
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
```
 | 
```
classWeaviateSubQuestionPack(BaseLlamaPack):
"""Weaviate Sub-Question query engine pack."""

    def__init__(
        self,
        collection_name: str,
        host: str,
        auth_client_secret: str,
        nodes: Optional[List[TextNode]] = None,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        fromweaviateimport Client

        self.client: Client = Client(host, auth_client_secret=auth_client_secret)

        weaviate_client = self.client
        weaviate_collection = weaviate_client.get_or_create_collection(collection_name)

        self._vector_store = WeaviateVectorStore(
            weaviate_collection=weaviate_collection
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

        self.retriever = self._index.as_retriever()

        query_engine = self._index.as_query_engine()
        query_engine_tools = [
            QueryEngineTool(
                query_engine=query_engine, metadata=ToolMetadata(name="Vector Index")
            )
        ]
        self.query_engine = SubQuestionQueryEngine.from_defaults(
            query_engine_tools=query_engine_tools
        )

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
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/sub_question_weaviate/#llama_index.packs.sub_question_weaviate.WeaviateSubQuestionPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-sub-question-weaviate/llama_index/packs/sub_question_weaviate/base.py`  
| 
```
62
63
64
65
66
67
68
69
70
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
###  retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/sub_question_weaviate/#llama_index.packs.sub_question_weaviate.WeaviateSubQuestionPack.retrieve "Permanent link")

```
retrieve(query_str: ) -> 

```

Retrieve.
Source code in `llama-index-packs/llama-index-packs-sub-question-weaviate/llama_index/packs/sub_question_weaviate/base.py`  
| 
```
72
73
74
```
 | 
```
defretrieve(self, query_str: str) -> Any:
"""Retrieve."""
    return self.retriever.retrieve(query_str)

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/sub_question_weaviate/#llama_index.packs.sub_question_weaviate.WeaviateSubQuestionPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-sub-question-weaviate/llama_index/packs/sub_question_weaviate/base.py`  
| 
```
76
77
78
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - WeaviateSubQuestionPack
