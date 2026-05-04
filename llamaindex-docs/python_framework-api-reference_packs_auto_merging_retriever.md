# Auto merging retriever
##  AutoMergingRetrieverPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/auto_merging_retriever/#llama_index.packs.auto_merging_retriever.AutoMergingRetrieverPack "Permanent link")
Bases: 
Auto-merging Retriever pack.
Build a hierarchical node graph from a set of documents, and run our auto-merging retriever.
Source code in `llama-index-packs/llama-index-packs-auto-merging-retriever/llama_index/packs/auto_merging_retriever/base.py`  
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
```
 | 
```
classAutoMergingRetrieverPack(BaseLlamaPack):
"""
    Auto-merging Retriever pack.

    Build a hierarchical node graph from a set of documents, and
    run our auto-merging retriever.

    """

    def__init__(
        self,
        docs: List[Document] = None,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        # create the sentence window node parser w/ default settings
        self.node_parser = HierarchicalNodeParser.from_defaults()
        nodes = self.node_parser.get_nodes_from_documents(docs)
        leaf_nodes = get_leaf_nodes(nodes)
        docstore = SimpleDocumentStore()

        # insert nodes into docstore
        docstore.add_documents(nodes)

        # define storage context (will include vector store by default too)
        storage_context = StorageContext.from_defaults(docstore=docstore)
        self.base_index = VectorStoreIndex(leaf_nodes, storage_context=storage_context)
        base_retriever = self.base_index.as_retriever(similarity_top_k=6)
        self.retriever = AutoMergingRetriever(
            base_retriever, storage_context, verbose=True
        )
        self.query_engine = RetrieverQueryEngine.from_args(self.retriever)

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "node_parser": self.node_parser,
            "retriever": self.retriever,
            "query_engine": self.query_engine,
        }

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/auto_merging_retriever/#llama_index.packs.auto_merging_retriever.AutoMergingRetrieverPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-auto-merging-retriever/llama_index/packs/auto_merging_retriever/base.py`  
| 
```
51
52
53
54
55
56
57
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "node_parser": self.node_parser,
        "retriever": self.retriever,
        "query_engine": self.query_engine,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/auto_merging_retriever/#llama_index.packs.auto_merging_retriever.AutoMergingRetrieverPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-auto-merging-retriever/llama_index/packs/auto_merging_retriever/base.py`  
| 
```
59
60
61
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - AutoMergingRetrieverPack
