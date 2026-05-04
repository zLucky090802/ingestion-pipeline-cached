# Superlinked
Superlinked retriever integration for LlamaIndex.
##  SuperlinkedRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/superlinked/#llama_index.retrievers.superlinked.SuperlinkedRetriever "Permanent link")
Bases: 
LlamaIndex retriever for Superlinked.
Provides an adapter that executes a Superlinked query and converts results into LlamaIndex `TextNode` instances with scores.
Source code in `llama-index-integrations/retrievers/llama-index-retrievers-superlinked/llama_index/retrievers/superlinked/retriever.py`  
| 
```
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
```
 | 
```
classSuperlinkedRetriever(BaseRetriever):
"""
    LlamaIndex retriever for Superlinked.

    Provides an adapter that executes a Superlinked query and converts results
    into LlamaIndex `TextNode` instances with scores.
    """

    def__init__(
        self,
        *,
        sl_client: App,
        sl_query: QueryDescriptor,
        page_content_field: str,
        query_text_param: str = "query_text",
        metadata_fields: Optional[List[str]] = None,
        top_k: int = 4,
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
"""
        Initialize the Superlinked retriever.

        Args:
            sl_client (Any): A Superlinked `App` instance.
            sl_query (Any): A Superlinked `QueryDescriptor` describing the query.
            page_content_field (str): Field name in the Superlinked result to use
                as the node text.
            query_text_param (str, optional): Parameter name in the Superlinked
                query for the user text. Defaults to "query_text".
            metadata_fields (Optional[List[str]], optional): If `None`, include
                all fields except `page_content_field`. Otherwise, include only
                the specified fields. Defaults to `None`.
            top_k (int, optional): Maximum number of nodes returned (a final cap
                is applied client-side). Defaults to `4`.
            callback_manager (Optional[CallbackManager], optional): LlamaIndex
                callback manager. Defaults to `None`.

        """
        self.sl_client = sl_client
        self.sl_query = sl_query
        self.page_content_field = page_content_field
        self.query_text_param = query_text_param
        self.metadata_fields = metadata_fields
        self.top_k = top_k

        # Initialize BaseRetriever
        super().__init__(callback_manager=callback_manager)

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""
        Execute the Superlinked query and map results to nodes.

        Args:
            query_bundle (QueryBundle): User query as a `QueryBundle`.

        Returns:
            List[NodeWithScore]: Retrieved nodes with associated scores.

        """
        user_query = getattr(query_bundle, "query_str", str(query_bundle))

        # Build query params, allowing overrides via retriever metadata if needed later
        query_params: dict[str, Any] = {self.query_text_param: user_query}

        try:
            result = self.sl_client.query(
                query_descriptor=self.sl_query, **query_params
            )
        except Exception:
            return []

        nodes: List[NodeWithScore] = []
        for entry in getattr(result, "entries", []) or []:
            fields = getattr(entry, "fields", None) or {}
            if self.page_content_field not in fields:
                continue

            text = fields[self.page_content_field]
            metadata: dict[str, Any] = {"id": getattr(entry, "id", None)}

            if self.metadata_fields is None:
                for key, val in fields.items():
                    if key != self.page_content_field:
                        metadata[key] = val
            else:
                for key in self.metadata_fields:
                    if key in fields:
                        metadata[key] = fields[key]

            # Determine score from Superlinked metadata if available
            score_value: float = 1.0
            entry_metadata = getattr(entry, "metadata", None)
            if entry_metadata is not None and hasattr(entry_metadata, "score"):
                try:
                    score_value = float(entry_metadata.score)
                except Exception:
                    score_value = 1.0

            node = TextNode(text=text, metadata=metadata)
            nodes.append(NodeWithScore(node=node, score=score_value))

        return nodes[: self.top_k]

```
 |  
| --- | --- |  
options: members: - SuperlinkedRetriever
