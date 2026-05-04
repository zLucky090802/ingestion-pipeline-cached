# Agent search retriever
##  AgentSearchRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/agent_search_retriever/#llama_index.packs.agent_search_retriever.AgentSearchRetriever "Permanent link")
Bases: 
Retriever that uses the Agent Search API to retrieve documents.
Source code in `llama-index-packs/llama-index-packs-agent-search-retriever/llama_index/packs/agent_search_retriever/base.py`  
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
```
 | 
```
classAgentSearchRetriever(BaseRetriever):
"""Retriever that uses the Agent Search API to retrieve documents."""

    def__init__(
        self,
        search_provider: str = "agent-search",
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        similarity_top_k: int = 4,
    ) -> None:
        import_err_msg = (
            "`agent-search` package not found, please run `pip install agent-search`"
        )
        try:
            importagent_search  # noqa: F401
        except ImportError:
            raise ImportError(import_err_msg)

        fromagent_searchimport SciPhi

        self._client = SciPhi(api_base=api_base, api_key=api_key)
        self._search_provider = SearchProvider(search_provider)
        self._similarity_top_k = similarity_top_k
        super().__init__()

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        search_result = self._client.search(
            query_bundle.query_str, search_provider=self._search_provider.value
        )
        nodes = []
        found_texts = set()
        for result in search_result:
            if result["text"] in found_texts:
                continue
            found_texts.add(result["text"])

            metadata = {}
            metadata["url"] = result["url"]
            metadata["title"] = result["title"]
            nodes.append(
                NodeWithScore(
                    node=TextNode(
                        text=result["text"],
                        score=result["score"],
                        metadata=result["metadata"],
                    ),
                    score=result["score"],
                )
            )

        return nodes[: self._similarity_top_k]

```
 |  
| --- | --- |  
##  AgentSearchRetrieverPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/agent_search_retriever/#llama_index.packs.agent_search_retriever.AgentSearchRetrieverPack "Permanent link")
Bases: 
AgentSearchRetrieverPack for running an agent-search retriever.
Source code in `llama-index-packs/llama-index-packs-agent-search-retriever/llama_index/packs/agent_search_retriever/base.py`  
| 
```
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
85
86
87
88
89
90
91
92
93
94
```
 | 
```
classAgentSearchRetrieverPack(BaseLlamaPack):
"""AgentSearchRetrieverPack for running an agent-search retriever."""

    def__init__(
        self,
        similarity_top_k: int = 2,
        search_provider: str = "agent-search",
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
    ) -> None:
        self.retriever = AgentSearchRetriever(
            search_provider=search_provider,
            api_key=api_key,
            api_base=api_base,
            similarity_top_k=similarity_top_k,
        )
        super().__init__()

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "retriever": self.retriever,
        }

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        return self._retriever.retrieve(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/agent_search_retriever/#llama_index.packs.agent_search_retriever.AgentSearchRetrieverPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-agent-search-retriever/llama_index/packs/agent_search_retriever/base.py`  
| 
```
86
87
88
89
90
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "retriever": self.retriever,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/agent_search_retriever/#llama_index.packs.agent_search_retriever.AgentSearchRetrieverPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-agent-search-retriever/llama_index/packs/agent_search_retriever/base.py`  
| 
```
92
93
94
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return self._retriever.retrieve(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - AgentSearchRetrieverPack
