# Xinference rerank
##  XinferenceRerank [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/xinference_rerank/#llama_index.postprocessor.xinference_rerank.XinferenceRerank "Permanent link")
Bases: 
Class for Xinference Rerank.
Source code in `llama-index-integrations/postprocessor/llama-index-postprocessor-xinference-rerank/llama_index/postprocessor/xinference_rerank/base.py`  
| 
```
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
85
86
87
88
89
90
91
```
 | 
```
classXinferenceRerank(BaseNodePostprocessor):
"""Class for Xinference Rerank."""

    top_n: int = Field(
        default=5,
        description="The number of nodes to return.",
    )
    model: str = Field(
        default="bge-reranker-base",
        description="The Xinference model uid to use.",
    )
    base_url: str = Field(
        default="http://localhost:9997",
        description="The Xinference base url to use.",
    )

    @classmethod
    defclass_name(cls) -> str:
        return "XinferenceRerank"

    defget_query_str(self, query):
        return query.query_str if isinstance(query, QueryBundle) else query

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
        dispatcher.event(
            ReRankStartEvent(
                query=query_bundle,
                nodes=nodes,
                top_n=self.top_n,
                model_name=self.model,
            )
        )
        if query_bundle is None:
            raise ValueError("Missing query bundle.")
        if len(nodes) == 0:
            return []
        with self.callback_manager.event(
            CBEventType.RERANKING,
            payload={
                EventPayload.NODES: nodes,
                EventPayload.MODEL_NAME: self.model,
                EventPayload.QUERY_STR: self.get_query_str(query_bundle),
                EventPayload.TOP_K: self.top_n,
            },
        ) as event:
            headers = {"Content-Type": "application/json"}
            json_data = {
                "model": self.model,
                "query": self.get_query_str(query_bundle),
                "documents": [
                    node.node.get_content(metadata_mode=MetadataMode.EMBED)
                    for node in nodes
                ],
            }
            response = requests.post(
                url=f"{self.base_url}/v1/rerank", headers=headers, json=json_data
            )
            response.encoding = "utf-8"
            if response.status_code != 200:
                raise Exception(
                    f"Xinference call failed with status code {response.status_code}."
                    f"Details: {response.text}"
                )
            rerank_nodes = [
                NodeWithScore(
                    node=nodes[result["index"]].node, score=result["relevance_score"]
                )
                for result in response.json()["results"][: self.top_n]
            ]
            event.on_end(payload={EventPayload.NODES: rerank_nodes})
        dispatcher.event(ReRankEndEvent(nodes=rerank_nodes))
        return rerank_nodes

```
 |  
| --- | --- |  
options: members: - XinferenceRerank
