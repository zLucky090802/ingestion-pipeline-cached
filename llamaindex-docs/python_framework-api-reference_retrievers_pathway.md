# Pathway
##  PathwayRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/pathway/#llama_index.retrievers.pathway.PathwayRetriever "Permanent link")
Bases: 
Pathway retriever.
Pathway is an open data processing framework. It allows you to easily develop data transformation pipelines that work with live data sources and changing data.
This is the client that implements Retriever API for PathwayVectorServer.
Source code in `llama-index-integrations/retrievers/llama-index-retrievers-pathway/llama_index/retrievers/pathway/base.py`  
| 
```
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
```
 | 
```
classPathwayRetriever(BaseRetriever):
"""
    Pathway retriever.

    Pathway is an open data processing framework.
    It allows you to easily develop data transformation pipelines
    that work with live data sources and changing data.

    This is the client that implements Retriever API for PathwayVectorServer.
    """

    def__init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        url: Optional[str] = None,
        similarity_top_k: int = DEFAULT_SIMILARITY_TOP_K,
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
"""Initializing the Pathway retriever client."""
        self.client = _VectorStoreClient(host, port, url)
        self.similarity_top_k = similarity_top_k
        super().__init__(callback_manager)

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Retrieve."""
        rets = self.client(query=query_bundle.query_str, k=self.similarity_top_k)
        items = [
            NodeWithScore(
                node=TextNode(text=ret["text"], extra_info=ret["metadata"]),
                # Transform cosine distance into a similairty score
                # (higher is more similar)
                score=1 - ret["dist"],
            )
            for ret in rets
        ]
        return sorted(items, key=lambda x: x.score or 0.0, reverse=True)

```
 |  
| --- | --- |  
options: members: - PathwayRetriever
