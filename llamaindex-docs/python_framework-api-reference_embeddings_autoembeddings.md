# Autoembeddings
##  ChonkieAutoEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/autoembeddings/#llama_index.embeddings.autoembeddings.ChonkieAutoEmbedding "Permanent link")
Bases: 
Autoembeddings from chonkie.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model_name`  |  The name of the model to use.  |  _required_  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-autoembeddings/llama_index/embeddings/autoembeddings/base.py`  
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
```
 | 
```
classChonkieAutoEmbedding(BaseEmbedding):
"""
    Autoembeddings from chonkie.

    Args:
        model_name (str): The name of the model to use.

    """

    model_name: str
    embedder: Optional[chonkie.BaseEmbeddings] = None

    def__init__(self, model_name: str) -> None:
        super().__init__(model_name=model_name)
        self.embedder = AutoEmbeddings.get_embeddings(self.model_name)

    @classmethod
    defclass_name(cls) -> str:
        return "ChonkieAutoEmbedding"

    def_get_embedding(self, text: str) -> List[float]:
        embed = self.embedder.embed(text)
        return embed.tolist()

    async def_aget_embedding(self, text: str) -> List[float]:
        return self._get_embedding(text)

    def_get_embeddings(self, texts: List[str]) -> List[List[float]]:
        embeds = self.embedder.embed_batch(texts)
        return [e.tolist() for e in embeds]

    async def_aget_embeddings(
        self,
        texts: List[str],
    ) -> List[List[float]]:
        return self._get_embeddings(texts)

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        return self._get_embedding(query)

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        return await self._aget_embedding(query)

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        return self._get_embedding(text)

```
 |  
| --- | --- |  
options: members: - AutoEmbeddings
