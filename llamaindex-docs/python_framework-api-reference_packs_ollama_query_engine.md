# Ollama query engine
##  OllamaQueryEnginePack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/ollama_query_engine/#llama_index.packs.ollama_query_engine.OllamaQueryEnginePack "Permanent link")
Bases: 
Source code in `llama-index-packs/llama-index-packs-ollama-query-engine/llama_index/packs/ollama_query_engine/base.py`  
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
```
 | 
```
classOllamaQueryEnginePack(BaseLlamaPack):
    def__init__(
        self,
        model: str,
        base_url: str = DEFAULT_OLLAMA_BASE_URL,
        documents: List[Document] = None,
    ) -> None:
        self._model = model
        self._base_url = base_url
        self.llm = Ollama(model=self._model, base_url=self._base_url)

        Settings.llm = self.llm
        Settings.embed_model = OllamaEmbedding(
            model_name=self._model, base_url=self._base_url
        )
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
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/ollama_query_engine/#llama_index.packs.ollama_query_engine.OllamaQueryEnginePack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-ollama-query-engine/llama_index/packs/ollama_query_engine/base.py`  
| 
```
32
33
34
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {"llm": self.llm, "index": self.index}

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/ollama_query_engine/#llama_index.packs.ollama_query_engine.OllamaQueryEnginePack.run "Permanent link")

```
run(query_str: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-ollama-query-engine/llama_index/packs/ollama_query_engine/base.py`  
| 
```
36
37
38
39
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
options: members: - OllamaQueryEnginePack
