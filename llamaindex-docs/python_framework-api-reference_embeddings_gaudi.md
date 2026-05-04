# Gaudi
##  GaudiEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/gaudi/#llama_index.embeddings.gaudi.GaudiEmbedding "Permanent link")
Bases: 
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-gaudi/llama_index/embeddings/gaudi/base.py`  
| 
```
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
```
 | 
```
classGaudiEmbedding(BaseEmbedding):
    max_length: int = Field(
        default=DEFAULT_HUGGINGFACE_LENGTH, description="Maximum length of input.", gt=0
    )
    normalize: bool = Field(default=True, description="Normalize embeddings or not.")
    query_instruction: Optional[str] = Field(
        description="Instruction to prepend to query text."
    )
    text_instruction: Optional[str] = Field(
        description="Instruction to prepend to text."
    )

    _model: Any = PrivateAttr()

    def__init__(
        self,
        model_name: str = DEFAULT_HUGGINGFACE_EMBEDDING_MODEL,
        max_length: Optional[int] = DEFAULT_HUGGINGFACE_LENGTH,
        normalize: bool = True,
        query_instruction: Optional[str] = None,
        text_instruction: Optional[str] = None,
        tokenizer: Optional[Any] = None,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        callback_manager: Optional[CallbackManager] = None,
        **model_kwargs,
    ) -> None:
        model = GaudiSentenceTransformer(
            model_name,
            cache_folder=get_cache_dir(),
            # prompts={
            #    "query": query_instruction
            #    or get_query_instruct_for_model_name(model_name),
            #    "text": text_instruction
            #    or get_text_instruct_for_model_name(model_name),
            # },
            **model_kwargs,
        )
        super().__init__(
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            max_length=max_length,
            normalize=normalize,
            query_instruction=query_instruction,
            text_instruction=text_instruction,
        )
        self._model = model

    @classmethod
    defclass_name(cls) -> str:
        return "GaudiEmbedding"

    def_embed(
        self,
        sentences: List[str],
        prompt_name: Optional[str] = None,
    ) -> List[List[float]]:
"""Embed sentences."""
        return self._model.encode(
            sentences,
            batch_size=self.embed_batch_size,
            prompt_name=prompt_name,
            normalize_embeddings=self.normalize,
        ).tolist()

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        return self._embed(query, prompt_name=None)

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""Get query embedding async."""
        return self._get_query_embedding(query)

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Get text embedding async."""
        return self._get_text_embedding(text)

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        return self._embed(text, prompt_name=None)

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get text embeddings."""
        return self._embed(texts, prompt_name=None)

```
 |  
| --- | --- |  
options: members: - GaudiEmbedding
