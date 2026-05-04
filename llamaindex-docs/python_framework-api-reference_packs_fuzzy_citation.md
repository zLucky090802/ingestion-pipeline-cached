# Fuzzy citation
##  FuzzyCitationEnginePack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/fuzzy_citation/#llama_index.packs.fuzzy_citation.FuzzyCitationEnginePack "Permanent link")
Bases: 
Source code in `llama-index-packs/llama-index-packs-fuzzy-citation/llama_index/packs/fuzzy_citation/base.py`  
| 
```
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
```
 | 
```
classFuzzyCitationEnginePack(BaseLlamaPack):
    def__init__(
        self, query_engine: BaseQueryEngine, threshold: int = DEFAULT_THRESHOLD
    ) -> None:
"""Init params."""
        try:
            fromthefuzzimport fuzz  # noqa: F401
        except ImportError:
            raise ImportError(
                "Please run `pip install thefuzz` to use the fuzzy citation engine."
            )

        self.query_engine = FuzzyCitationQueryEngine(
            query_engine=query_engine, threshold=threshold
        )

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "query_engine": self.query_engine,
            "query_engine_cls": FuzzyCitationQueryEngine,
        }

    defrun(self, query_str: str, **kwargs: Any) -> RESPONSE_TYPE:
"""Run the pipeline."""
        return self.query_engine.query(query_str)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/fuzzy_citation/#llama_index.packs.fuzzy_citation.FuzzyCitationEnginePack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-fuzzy-citation/llama_index/packs/fuzzy_citation/base.py`  
| 
```
129
130
131
132
133
134
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "query_engine": self.query_engine,
        "query_engine_cls": FuzzyCitationQueryEngine,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/fuzzy_citation/#llama_index.packs.fuzzy_citation.FuzzyCitationEnginePack.run "Permanent link")

```
run(query_str: , **kwargs: ) -> RESPONSE_TYPE

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-fuzzy-citation/llama_index/packs/fuzzy_citation/base.py`  
| 
```
136
137
138
```
 | 
```
defrun(self, query_str: str, **kwargs: Any) -> RESPONSE_TYPE:
"""Run the pipeline."""
    return self.query_engine.query(query_str)

```
 |  
| --- | --- |  
options: members: - FuzzyCitationEnginePack
