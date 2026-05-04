# Tldw
##  TldwRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/tldw/#llama_index.retrievers.tldw.TldwRetriever "Permanent link")
Bases: 
A retriever that searches for relevant video moments from the TL;DW collection.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  The API key for authentication.  |  _required_  |  
|  `collection_id`  |  The ID of the video collection to search within.  |  _required_  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.base.CallbackManager\)")]`  |  Optional callback manager for logging and event handling.  |  `None`  |  
Source code in `llama-index-integrations/retrievers/llama-index-retrievers-tldw/llama_index/retrievers/tldw/base.py`  
| 
```
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
```
 | 
```
classTldwRetriever(BaseRetriever):
r"""
    A retriever that searches for relevant video moments from the TL;DW collection.

    Args:
        api_key (str): The API key for authentication.
        collection_id (str): The ID of the video collection to search within.
        callback_manager (Optional[CallbackManager]): Optional callback manager for logging and event handling.

    """

    def__init__(
        self,
        api_key: str,
        collection_id: str,
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
        self._api_key = api_key
        self._collection_id = collection_id
        super().__init__(
            callback_manager=callback_manager,
        )

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
        }
        res = requests.post(
            f"{API_ENDPOINT}/search",
            headers=headers,
            json={
                "collection_id": self._collection_id,
                "search_term": query_bundle.query_str,
            },
        )
        search_results = SearchResult.model_validate(res.json())

        # Return individual fragments as nodes
        return [
            NodeWithScore(
                node=TextNode(
                    text=fragment.description,
                    metadata={
                        "scene_index": idx,
                        "media_id": scene.media_id,
                        "start_ms": fragment.start_ms,
                        "end_ms": fragment.end_ms,
                        "scene_start_ms": scene.start_ms,
                        "scene_end_ms": scene.end_ms,
                    },
                ),
                score=fragment.similarity,
            )
            for idx, scene in enumerate(search_results.scenes)
            for fragment in scene.fragments
        ]

```
 |  
| --- | --- |  
options: members: - TldwRetriever
