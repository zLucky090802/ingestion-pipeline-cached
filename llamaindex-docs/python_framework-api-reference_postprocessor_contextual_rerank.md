# Contextual rerank
##  ContextualRerank [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/contextual_rerank/#llama_index.postprocessor.contextual_rerank.ContextualRerank "Permanent link")
Bases: 
Contextual Reranking model.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model`  |  str = Field(description="Contextual Reranking model name. Default is 'ctxl-rerank-en-v1-instruct'.")  |  `'ctxl-rerank-en-v1-instruct'`  |  
|  `top_n`  |  int = Field(description="Top N nodes to return.")  |  
|  `base_url`  |  `Optional[str]`  |  Optional[str] = Field(description="Contextual base url.", default=None)  |  `None`  |  
Source code in `llama-index-integrations/postprocessor/llama-index-postprocessor-contextual-rerank/llama_index/postprocessor/contextual_rerank/base.py`  
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
```
 | 
```
classContextualRerank(BaseNodePostprocessor):
"""
    Contextual Reranking model.

    Args:
        model: str = Field(description="Contextual Reranking model name. Default is 'ctxl-rerank-en-v1-instruct'.")
        top_n: int = Field(description="Top N nodes to return.")
        base_url: Optional[str] = Field(description="Contextual base url.", default=None)

    """

    model: str = Field(description="Contextual Reranking model name.")
    top_n: int = Field(description="Top N nodes to return.")
    base_url: Optional[str] = Field(description="Contextual base url.", default=None)

    _client: Any = PrivateAttr()

    def__init__(
        self,
        top_n: int = 2,
        model: str = "ctxl-rerank-en-v1-instruct",
        api_key: Optional[str] = None,
        client: Optional[Any] = None,
        base_url: Optional[str] = None,
    ):
        super().__init__(top_n=top_n, model=model)
        try:
            api_key = api_key or os.environ["CONTEXTUAL_API_KEY"]
        except IndexError:
            raise ValueError(
                "Must pass in contextual api key or "
                "specify via CONTEXTUAL_API_KEY environment variable "
            )
        try:
            fromcontextualimport ContextualAI
        except ImportError:
            raise ImportError(
                "Cannot import Contextual client package, please `pip install contextual-client`."
            )

        if client is not None:
            self._client = client
        else:
            try:
                self._client = ContextualAI(api_key=api_key, base_url=base_url)
            except Exception as e:
                raise ValueError(f"Failed to create Contextual client: {e}")

    @classmethod
    defclass_name(cls) -> str:
        return "ContextualRerank"

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
        dispatcher.event(
            ReRankStartEvent(
                query=query_bundle, nodes=nodes, top_n=self.top_n, model_name=self.model
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
                EventPayload.MODEL_NAME: self.model,
                EventPayload.QUERY_STR: query_bundle.query_str,
                EventPayload.TOP_K: self.top_n,
            },
        ) as event:
            texts = [
                node.node.get_content(metadata_mode=MetadataMode.EMBED)
                for node in nodes
            ]
            results = self._client.rerank.create(
                model=self.model,
                top_n=self.top_n,
                query=query_bundle.query_str,
                documents=texts,
            )

            new_nodes = []
            for result in results.results:
                new_node_with_score = NodeWithScore(
                    node=nodes[result.index].node, score=result.relevance_score
                )
                new_nodes.append(new_node_with_score)
            event.on_end(payload={EventPayload.NODES: new_nodes})

        dispatcher.event(ReRankEndEvent(nodes=new_nodes))
        return new_nodes

```
 |  
| --- | --- |  
options: members: - ContextualRerank
