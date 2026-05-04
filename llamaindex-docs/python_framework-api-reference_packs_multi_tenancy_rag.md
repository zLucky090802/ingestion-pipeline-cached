# Multi tenancy rag
##  MultiTenancyRAGPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/multi_tenancy_rag/#llama_index.packs.multi_tenancy_rag.MultiTenancyRAGPack "Permanent link")
Bases: 
Source code in `llama-index-packs/llama-index-packs-multi-tenancy-rag/llama_index/packs/multi_tenancy_rag/base.py`  
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
```
 | 
```
classMultiTenancyRAGPack(BaseLlamaPack):
    def__init__(self) -> None:
        llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
        self.llm = llm
        Settings.llm = self.llm
        self.index = VectorStoreIndex.from_documents(documents=[])

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {"llm": self.llm, "index": self.index}

    defadd(self, documents: List[Document], user: Any) -> None:
"""Insert Documents of a user into index."""
        # Add metadata to documents
        for document in documents:
            document.metadata["user"] = user
        # Create Nodes using IngestionPipeline
        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(chunk_size=512, chunk_overlap=20),
            ]
        )
        nodes = pipeline.run(documents=documents, num_workers=4)
        # Insert nodes into the index
        self.index.insert_nodes(nodes)

    defrun(self, query_str: str, user: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        # Define retriever to filter out nodes for user and query
        retriever = VectorIndexRetriever(
            index=self.index,
            filters=MetadataFilters(
                filters=[
                    ExactMatchFilter(
                        key="user",
                        value=user,
                    )
                ]
            ),
            **kwargs,
        )
        # Define response synthesizer
        response_synthesizer = get_response_synthesizer(response_mode="compact")
        # Define Query Engine
        query_engine = RetrieverQueryEngine(
            retriever=retriever, response_synthesizer=response_synthesizer
        )
        return query_engine.query(query_str)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/multi_tenancy_rag/#llama_index.packs.multi_tenancy_rag.MultiTenancyRAGPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-multi-tenancy-rag/llama_index/packs/multi_tenancy_rag/base.py`  
| 
```
21
22
23
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {"llm": self.llm, "index": self.index}

```
 |  
| --- | --- |  
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/multi_tenancy_rag/#llama_index.packs.multi_tenancy_rag.MultiTenancyRAGPack.add "Permanent link")

```
add(documents: [], user: ) -> None

```

Insert Documents of a user into index.
Source code in `llama-index-packs/llama-index-packs-multi-tenancy-rag/llama_index/packs/multi_tenancy_rag/base.py`  
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
```
 | 
```
defadd(self, documents: List[Document], user: Any) -> None:
"""Insert Documents of a user into index."""
    # Add metadata to documents
    for document in documents:
        document.metadata["user"] = user
    # Create Nodes using IngestionPipeline
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=512, chunk_overlap=20),
        ]
    )
    nodes = pipeline.run(documents=documents, num_workers=4)
    # Insert nodes into the index
    self.index.insert_nodes(nodes)

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/multi_tenancy_rag/#llama_index.packs.multi_tenancy_rag.MultiTenancyRAGPack.run "Permanent link")

```
run(query_str: , user: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-multi-tenancy-rag/llama_index/packs/multi_tenancy_rag/base.py`  
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
```
 | 
```
defrun(self, query_str: str, user: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    # Define retriever to filter out nodes for user and query
    retriever = VectorIndexRetriever(
        index=self.index,
        filters=MetadataFilters(
            filters=[
                ExactMatchFilter(
                    key="user",
                    value=user,
                )
            ]
        ),
        **kwargs,
    )
    # Define response synthesizer
    response_synthesizer = get_response_synthesizer(response_mode="compact")
    # Define Query Engine
    query_engine = RetrieverQueryEngine(
        retriever=retriever, response_synthesizer=response_synthesizer
    )
    return query_engine.query(query_str)

```
 |  
| --- | --- |  
options: members: - MultiTenancyRAGPack
