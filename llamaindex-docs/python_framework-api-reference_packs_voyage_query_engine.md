# Voyage query engine
##  VoyageQueryEnginePack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/voyage_query_engine/#llama_index.packs.voyage_query_engine.VoyageQueryEnginePack "Permanent link")
Bases: 
Source code in `llama-index-packs/llama-index-packs-voyage-query-engine/llama_index/packs/voyage_query_engine/base.py`  
| 
```
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
```
 | 
```
classVoyageQueryEnginePack(BaseLlamaPack):
    def__init__(self, documents: List[Document]) -> None:
        llm = OpenAI(model="gpt-4")
        embed_model = VoyageEmbedding(
            model_name="voyage-01", voyage_api_key=os.environ["VOYAGE_API_KEY"]
        )

        self.llm = llm
        Settings.llm = self.llm
        Settings.embed_model = embed_model
        self.index = VectorStoreIndex.from_documents(documents)

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {"llm": self.llm, "index": self.index}

    defrun(self, query_str: str, **kwargs: Any) -> Any:
"""Run the pipeline."""
        query_engine = self.index.as_query_engine(**kwargs)
        return query_engine.query(query_str)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/voyage_query_engine/#llama_index.packs.voyage_query_engine.VoyageQueryEnginePack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-voyage-query-engine/llama_index/packs/voyage_query_engine/base.py`  
| 
```
23
24
25
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {"llm": self.llm, "index": self.index}

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/voyage_query_engine/#llama_index.packs.voyage_query_engine.VoyageQueryEnginePack.run "Permanent link")

```
run(query_str: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-voyage-query-engine/llama_index/packs/voyage_query_engine/base.py`  
| 
```
27
28
29
30
```
 | 
```
defrun(self, query_str: str, **kwargs: Any) -> Any:
"""Run the pipeline."""
    query_engine = self.index.as_query_engine(**kwargs)
    return query_engine.query(query_str)

```
 |  
| --- | --- |  
options: members: - VoyageQueryEnginePack
