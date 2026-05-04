# Alibabacloud aisearch rerank
##  AlibabaCloudAISearchRerank [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/alibabacloud_aisearch_rerank/#llama_index.postprocessor.alibabacloud_aisearch_rerank.AlibabaCloudAISearchRerank "Permanent link")
Bases: 
For further details, please visit `https://help.aliyun.com/zh/open-search/search-platform/developer-reference/ranker-api-details`.
Source code in `llama-index-integrations/postprocessor/llama-index-postprocessor-alibabacloud-aisearch-rerank/llama_index/postprocessor/alibabacloud_aisearch_rerank/base.py`  
| 
```
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
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
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
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
```
 | 
```
classAlibabaCloudAISearchRerank(BaseNodePostprocessor):
"""
    For further details, please visit `https://help.aliyun.com/zh/open-search/search-platform/developer-reference/ranker-api-details`.
    """

    _client: Client = PrivateAttr()

    aisearch_api_key: str = Field(default=None, exclude=True)
    endpoint: str = None

    service_id: str = "ops-bge-reranker-larger"
    workspace_name: str = "default"
    top_n: int = 3
    batch_size: int = 16

    def__init__(
        self, endpoint: str = None, aisearch_api_key: str = None, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.aisearch_api_key = get_from_param_or_env(
            "aisearch_api_key", aisearch_api_key, "AISEARCH_API_KEY"
        )
        self.endpoint = get_from_param_or_env("endpoint", endpoint, "AISEARCH_ENDPOINT")

        config = AISearchConfig(
            bearer_token=self.aisearch_api_key,
            endpoint=self.endpoint,
            protocol="http",
        )

        self._client = Client(config=config)

    @classmethod
    defclass_name(cls) -> str:
        return "AlibabaCloudAISearchRerank"

    @retry_decorator
    def_rerank_one_batch(
        self, query: str, texts: List[str]
    ) -> List[GetDocumentRankResponseBodyResultScores]:
        request = GetDocumentRankRequest(docs=texts, query=query)
        response: GetDocumentRankResponse = self._client.get_document_rank(
            workspace_name=self.workspace_name,
            service_id=self.service_id,
            request=request,
        )
        return response.body.result.scores

    def_rerank(
        self, query: str, texts: List[str], top_n: int
    ) -> List[GetDocumentRankResponseBodyResultScores]:
        scores = []
        for i in range(0, len(texts), self.batch_size):
            batch_scores = self._rerank_one_batch(query, texts[i : i + self.batch_size])
            for score in batch_scores:
                score.index = i + score.index
            scores.extend(batch_scores)
        scores.sort(key=lambda x: x.score, reverse=True)
        return scores[:top_n]

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
                model_name=self.service_id,
            )
        )

        if query_bundle is None:
            raise ValueError("Missing query bundle in extra info.")
        if len(nodes) == 0:
            return []

        with self.callback_manager.event(
            CBEventType.RERANKING,
            payload={
                EventPayload.NODES: nodes,
                EventPayload.MODEL_NAME: self.service_id,
                EventPayload.QUERY_STR: query_bundle.query_str,
                EventPayload.TOP_K: self.top_n,
            },
        ) as event:
            texts = [
                node.node.get_content(metadata_mode=MetadataMode.EMBED)
                for node in nodes
            ]
            results = self._rerank(
                query=query_bundle.query_str,
                texts=texts,
                top_n=self.top_n,
            )

            new_nodes = []
            for result in results:
                new_node_with_score = NodeWithScore(
                    node=nodes[result.index].node, score=result.score
                )
                new_nodes.append(new_node_with_score)
            event.on_end(payload={EventPayload.NODES: new_nodes})

        dispatcher.event(ReRankEndEvent(nodes=new_nodes))
        return new_nodes

```
 |  
| --- | --- |  
options: members: - AlibabaCloudAISearchRerank
