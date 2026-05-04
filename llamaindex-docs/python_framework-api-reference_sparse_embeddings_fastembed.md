# Fastembed
##  FastEmbedSparseEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/sparse_embeddings/fastembed/#llama_index.sparse_embeddings.fastembed.FastEmbedSparseEmbedding "Permanent link")
Bases: `BaseSparseEmbedding`
Qdrant FastEmbedding Sparse models. FastEmbed is a lightweight, fast, Python library built for embedding generation. See more documentation at: * https://github.com/qdrant/fastembed/ * https://qdrant.github.io/fastembed/.
To use this class, you must install the `fastembed` Python package.
`pip install fastembed` Example: from llama_index.sparse_embeddings.fastembed import FastEmbedSparseEmbedding fastembed = FastEmbedSparseEmbedding()
Source code in `llama-index-integrations/sparse_embeddings/llama-index-sparse-embeddings-fastembed/llama_index/sparse_embeddings/fastembed/base.py`  
| 
```
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
114
115
116
117
118
119
```
 | 
```
classFastEmbedSparseEmbedding(BaseSparseEmbedding):
"""
    Qdrant FastEmbedding Sparse models.
    FastEmbed is a lightweight, fast, Python library built for embedding generation.
    See more documentation at:
    * https://github.com/qdrant/fastembed/
    * https://qdrant.github.io/fastembed/.

    To use this class, you must install the `fastembed` Python package.

    `pip install fastembed`
    Example:
        from llama_index.sparse_embeddings.fastembed import FastEmbedSparseEmbedding
        fastembed = FastEmbedSparseEmbedding()
    """

    model_name: str = Field(
        "prithivida/Splade_PP_en_v1",
        description="Name of the FastEmbedding sparse model to use.\n"
        "Defaults to 'prithivida/Splade_PP_en_v1'.\n"
        "Find the list of supported models at "
        "https://qdrant.github.io/fastembed/examples/Supported_Models/",
    )

    max_length: int = Field(
        512,
        description="The maximum number of tokens. Defaults to 512.\n"
        "Unknown behavior for values > 512.",
    )

    cache_dir: Optional[str] = Field(
        None,
        description="The path to the cache directory.\n"
        "Defaults to `local_cache` in the parent directory",
    )

    threads: Optional[int] = Field(
        None,
        description="The number of threads single onnxruntime session can use.\n"
        "Defaults to None",
    )

    _model: SparseTextEmbedding = PrivateAttr()

    @classmethod
    defclass_name(self) -> str:
        return "FastEmbedSparseEmbedding"

    def__init__(
        self,
        model_name: Optional[str] = "prithivida/Splade_PP_en_v1",
        max_length: Optional[int] = 512,
        cache_dir: Optional[str] = None,
        threads: Optional[int] = None,
        providers: Optional[List[Any]] = None,
    ):
        super().__init__(
            model_name=model_name,
            max_length=max_length,
            cache_dir=cache_dir,
            threads=threads,
        )

        self._model = SparseTextEmbedding(
            model_name=model_name,
            max_length=max_length,
            cache_dir=cache_dir,
            threads=threads,
            providers=providers,
        )

    def_fastembed_to_dict(
        self, fastembed_results: List[FastEmbedSparseEmbedding]
    ) -> List[SparseEmbedding]:
"""Convert FastEmbedSparseEmbedding to SparseEmbedding dict."""
        results = []

        for embedding in fastembed_results:
            result_dict = {}
            for indice, value in zip(embedding.indices, embedding.values):
                result_dict[int(indice)] = float(value)
            results.append(result_dict)

        return results

    def_get_text_embedding(self, text: str) -> SparseEmbedding:
        results = self._model.passage_embed([text])
        return self._fastembed_to_dict(results)[0]

    async def_aget_text_embedding(self, text: str) -> SparseEmbedding:
        return self._get_text_embedding(text)

    def_get_text_embeddings(self, texts: List[str]) -> List[SparseEmbedding]:
        results = self._model.passage_embed(texts)
        return self._fastembed_to_dict(results)

    async def_aget_text_embeddings(self, texts: List[str]) -> List[SparseEmbedding]:
        return self._get_text_embeddings(texts)

    def_get_query_embedding(self, query: str) -> SparseEmbedding:
        results = self._model.query_embed(query)
        return self._fastembed_to_dict(results)[0]

    async def_aget_query_embedding(self, query: str) -> SparseEmbedding:
        return self._get_query_embedding(query)

```
 |  
| --- | --- |  
options: members: - FastEmbedEmbedding
