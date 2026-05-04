# Fastembed
##  FastEmbedEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/fastembed/#llama_index.embeddings.fastembed.FastEmbedEmbedding "Permanent link")
Bases: 
Qdrant FastEmbedding models. FastEmbed is a lightweight, fast, Python library built for embedding generation. See more documentation at: * https://github.com/qdrant/fastembed/ * https://qdrant.github.io/fastembed/.
To use this class, you must install the `fastembed` Python package.
`pip install fastembed` Example: from llama_index.embeddings.fastembed import FastEmbedEmbedding fastembed = FastEmbedEmbedding()
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-fastembed/llama_index/embeddings/fastembed/base.py`  
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
```
 | 
```
classFastEmbedEmbedding(BaseEmbedding):
"""
    Qdrant FastEmbedding models.
    FastEmbed is a lightweight, fast, Python library built for embedding generation.
    See more documentation at:
    * https://github.com/qdrant/fastembed/
    * https://qdrant.github.io/fastembed/.

    To use this class, you must install the `fastembed` Python package.

    `pip install fastembed`
    Example:
        from llama_index.embeddings.fastembed import FastEmbedEmbedding
        fastembed = FastEmbedEmbedding()
    """

    model_config = ConfigDict(
        protected_namespaces=("pydantic_model_",),
        arbitrary_types_allowed=True,
        use_attribute_docstrings=True,
    )

    model_name: str = Field(
        default="BAAI/bge-small-en-v1.5",
        description=(
            "Name of the FastEmbedding model to use. "
            "Find the list of supported models at "
            "https://qdrant.github.io/fastembed/examples/Supported_Models/"
        ),
    )

    cache_dir: Optional[str] = Field(
        default=None,
        description="The path to the cache directory. Defaults to fastembed_cache in the system's temp directory.",
    )

    threads: Optional[int] = Field(
        default=None,
        description="The number of threads single onnxruntime session can use. Defaults to None.",
    )

    doc_embed_type: Literal["default", "passage"] = Field(
        default="default",
        description="Type of embedding method to use for documents. Available options are 'default' and 'passage'.",
    )

    providers: Optional[List[str]] = Field(
        default=None, description="The ONNX providers to use for the embedding model."
    )

    _model: "TextEmbedding" = PrivateAttr()

    def__init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
        cache_dir: Optional[str] = None,
        threads: Optional[int] = None,
        doc_embed_type: Literal["default", "passage"] = "default",
        providers: Optional[List[str]] = None,
        **kwargs: Any,
    ):
        super().__init__(
            model_name=model_name,
            threads=threads,
            doc_embed_type=doc_embed_type,
            providers=providers,
            cache_dir=cache_dir,
            **kwargs,
        )

        try:
            fromfastembedimport TextEmbedding
        except ImportError as e:
            raise ImportError(
                "Could not import FastEmbed. "
                "Please install it with `pip install fastembed` or "
                "`pip install fastembed-gpu` for GPU support"
            ) frome

        self._model = TextEmbedding(
            model_name=model_name,
            cache_dir=cache_dir,
            threads=threads,
            providers=providers,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "FastEmbedEmbedding"

    def_get_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embeddings([text])[0]

    async def_aget_text_embedding(self, text: str) -> List[float]:
        return await asyncio.to_thread(self._get_text_embedding, text)

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        embeddings: List[np.ndarray]
        if self.doc_embed_type == "passage":
            embeddings = list(self._model.passage_embed(texts))
        else:
            embeddings = list(self._model.embed(texts))
        return [embedding.tolist() for embedding in embeddings]

    async def_aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        return await asyncio.to_thread(self._get_text_embeddings, texts)

    def_get_query_embedding(self, query: str) -> List[float]:
        query_embeddings: list[np.ndarray] = list(self._model.query_embed(query))
        return query_embeddings[0].tolist()

    async def_aget_query_embedding(self, query: str) -> List[float]:
        return await asyncio.to_thread(self._get_query_embedding, query)

```
 |  
| --- | --- |  
options: members: - FastEmbedEmbedding
