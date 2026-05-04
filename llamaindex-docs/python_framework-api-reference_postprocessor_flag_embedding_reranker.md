# Flag embedding reranker
##  FlagEmbeddingReranker [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/flag_embedding_reranker/#llama_index.postprocessor.flag_embedding_reranker.FlagEmbeddingReranker "Permanent link")
Bases: 
Flag Embedding Reranker.
Source code in `llama-index-integrations/postprocessor/llama-index-postprocessor-flag-embedding-reranker/llama_index/postprocessor/flag_embedding_reranker/base.py`  
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
 92
 93
 94
 95
 96
 97
 98
 99
100
```
 | 
```
classFlagEmbeddingReranker(BaseNodePostprocessor):
"""Flag Embedding Reranker."""

    model: str = Field(description="BAAI Reranker model name.")
    top_n: int = Field(description="Number of nodes to return sorted by score.")
    use_fp16: bool = Field(description="Whether to use fp16 for inference.")
    _model: Any = PrivateAttr()

    def__init__(
        self,
        top_n: int = 2,
        model: str = "BAAI/bge-reranker-large",
        use_fp16: bool = False,
    ) -> None:
        super().__init__(top_n=top_n, model=model, use_fp16=use_fp16)
        try:
            fromFlagEmbeddingimport FlagReranker
        except ImportError:
            raise ImportError(
                "Cannot import FlagReranker package, please install it: ",
                "pip install git+https://github.com/FlagOpen/FlagEmbedding.git",
            )
        self._model = FlagReranker(
            model,
            use_fp16=use_fp16,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "FlagEmbeddingReranker"

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
            raise ValueError("Missing query bundle in extra info.")
        if len(nodes) == 0:
            return []

        query_and_nodes = [
            (
                query_bundle.query_str,
                node.node.get_content(metadata_mode=MetadataMode.EMBED),
            )
            for node in nodes
        ]

        with self.callback_manager.event(
            CBEventType.RERANKING,
            payload={
                EventPayload.NODES: nodes,
                EventPayload.MODEL_NAME: self.model,
                EventPayload.QUERY_STR: query_bundle.query_str,
                EventPayload.TOP_K: self.top_n,
            },
        ) as event:
            scores = self._model.compute_score(query_and_nodes)

            # a single node passed into compute_score returns a float
            if isinstance(scores, float):
                scores = [scores]

            assert len(scores) == len(nodes)

            for node, score in zip(nodes, scores):
                node.score = score

            new_nodes = sorted(nodes, key=lambda x: -x.score if x.score else 0)[
                : self.top_n
            ]
            event.on_end(payload={EventPayload.NODES: new_nodes})

        dispatcher.event(ReRankEndEvent(nodes=new_nodes))
        return new_nodes

```
 |  
| --- | --- |  
options: members: - FlagEmbeddingReranker
