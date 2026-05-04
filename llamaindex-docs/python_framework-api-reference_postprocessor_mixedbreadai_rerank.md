# Mixedbreadai rerank
##  MixedbreadAIRerank [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/mixedbreadai_rerank/#llama_index.postprocessor.mixedbreadai_rerank.MixedbreadAIRerank "Permanent link")
Bases: 
Class for reranking nodes using the mixedbread ai reranking API with models such as 'mixedbread-ai/mxbai-rerank-large-v1'.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `top_n`  |  Top N nodes to return. Defaults to 10.  |  
|  `model`  |  mixedbread ai model name. Defaults to "mixedbread-ai/mxbai-rerank-large-v1".  |  `'mixedbread-ai/mxbai-rerank-large-v1'`  |  
|  `api_key`  |  `Optional[str]`  |  mixedbread ai API key. Defaults to None.  |  `None`  |  
|  `max_retries`  |  `Optional[int]`  |  Maximum number of retries for API calls. Defaults to None.  |  `None`  |  
|  `timeout`  |  `Optional[float]`  |  Timeout for API calls.  |  `None`  |  
|  `httpx_client`  |  `Optional[Client]`  |  Custom HTTPX client for synchronous requests.  |  `None`  |  
|  `httpx_async_client`  |  `Optional[AsyncClient]`  |  Custom HTTPX client for asynchronous requests.  |  `None`  |  
Source code in `llama-index-integrations/postprocessor/llama-index-postprocessor-mixedbreadai-rerank/llama_index/postprocessor/mixedbreadai_rerank/base.py`  
| 
```
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
classMixedbreadAIRerank(BaseNodePostprocessor):
"""
    Class for reranking nodes using the mixedbread ai reranking API with models such as 'mixedbread-ai/mxbai-rerank-large-v1'.

    Args:
        top_n (int): Top N nodes to return. Defaults to 10.
        model (str): mixedbread ai model name. Defaults to "mixedbread-ai/mxbai-rerank-large-v1".
        api_key (Optional[str]): mixedbread ai API key. Defaults to None.
        max_retries (Optional[int]): Maximum number of retries for API calls. Defaults to None.
        timeout (Optional[float]): Timeout for API calls.
        httpx_client (Optional[httpx.Client]): Custom HTTPX client for synchronous requests.
        httpx_async_client (Optional[httpx.AsyncClient]): Custom HTTPX client for asynchronous requests.

    """

    model: str = Field(
        default="mixedbread-ai/mxbai-rerank-large-v1",
        description="mixedbread ai model name.",
        min_length=1,
    )
    top_n: int = Field(default=10, description="Top N nodes to return.", gt=0)

    _client: Mixedbread = PrivateAttr()
    _async_client: AsyncMixedbread = PrivateAttr()

    def__init__(
        self,
        top_n: int = 10,
        model: str = "mixedbread-ai/mxbai-rerank-large-v1",
        api_key: Optional[str] = None,
        max_retries: Optional[int] = None,
        timeout: Optional[float] = None,
        httpx_client: Optional[httpx.Client] = None,
        httpx_async_client: Optional[httpx.AsyncClient] = None,
    ):
        super().__init__(top_n=top_n, model=model)
        try:
            api_key = api_key or os.environ["MXBAI_API_KEY"]
        except KeyError:
            raise ValueError(
                "Must pass in mixedbread ai API key or "
                "specify via MXBAI_API_KEY environment variable"
            )

        self._client = Mixedbread(
            api_key=api_key,
            timeout=timeout,
            http_client=httpx_client,
            max_retries=max_retries if max_retries is not None else DEFAULT_MAX_RETRIES,
        )
        self._async_client = AsyncMixedbread(
            api_key=api_key,
            timeout=timeout,
            http_client=httpx_async_client,
            max_retries=max_retries if max_retries is not None else DEFAULT_MAX_RETRIES,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "MixedbreadAIRerank"

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
"""
        Postprocess nodes by reranking them using the mixedbread ai reranking API.

        Args:
            nodes (List[NodeWithScore]): List of nodes to rerank.
            query_bundle (Optional[QueryBundle]): Query bundle containing the query string.

        Returns:
            List[NodeWithScore]: Reranked list of nodes.

        """
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
            results = self._client.rerank(
                model=self.model,
                query=query_bundle.query_str,
                input=texts,
                top_k=self.top_n,
                return_input=False,
            )

            new_nodes = []
            for result in results.data:
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
options: members: - MixedbreadAIRerank
