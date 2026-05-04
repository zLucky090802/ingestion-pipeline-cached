# Mistralai
##  MistralAIEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/mistralai/#llama_index.embeddings.mistralai.MistralAIEmbedding "Permanent link")
Bases: 
Class for MistralAI embeddings.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model_name`  |  Model for embedding. Defaults to "mistral-embed".  |  `'mistral-embed'`  |  
|  `api_key`  |  `Optional[str]`  |  API key to access the model. Defaults to None.  |  `None`  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-mistralai/llama_index/embeddings/mistralai/base.py`  
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
101
102
103
104
105
106
107
108
109
```
 | 
```
classMistralAIEmbedding(BaseEmbedding):
"""
    Class for MistralAI embeddings.

    Args:
        model_name (str): Model for embedding.
            Defaults to "mistral-embed".

        api_key (Optional[str]): API key to access the model. Defaults to None.

    """

    # Instance variables initialized via Pydantic's mechanism
    _client: Mistral = PrivateAttr()

    def__init__(
        self,
        model_name: str = "mistral-embed",
        api_key: Optional[str] = None,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ):
        super().__init__(
            model_name=model_name,
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            **kwargs,
        )
        api_key = get_from_param_or_env("api_key", api_key, "MISTRAL_API_KEY", "")

        if not api_key:
            raise ValueError(
                "You must provide an API key to use mistralai. "
                "You can either pass it in as an argument or set it `MISTRAL_API_KEY`."
            )
        self._client = Mistral(api_key=api_key)

    @classmethod
    defclass_name(cls) -> str:
        return "MistralAIEmbedding"

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        return (
            self._client.embeddings.create(model=self.model_name, inputs=[query])
            .data[0]
            .embedding
        )

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""The asynchronous version of _get_query_embedding."""
        return (
            (
                await self._client.embeddings.create_async(
                    model=self.model_name, inputs=[query]
                )
            )
            .data[0]
            .embedding
        )

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        return (
            self._client.embeddings.create(model=self.model_name, inputs=[text])
            .data[0]
            .embedding
        )

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Asynchronously get text embedding."""
        return (
            await self._client.embeddings.create(
                model=self.model_name,
                inputs=[text],
            )
            .data[0]
            .embedding
        )

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get text embeddings."""
        embedding_response = self._client.embeddings.create(
            model=self.model_name, inputs=texts
        ).data
        return [embed.embedding for embed in embedding_response]

    async def_aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Asynchronously get text embeddings."""
        embedding_response = await self._client.embeddings.create_async(
            model=self.model_name, inputs=texts
        )
        return [embed.embedding for embed in embedding_response.data]

```
 |  
| --- | --- |  
options: members: - MistralAIEmbedding
