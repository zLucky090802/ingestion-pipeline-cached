# Modelscope
##  ModelScopeEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/modelscope/#llama_index.embeddings.modelscope.ModelScopeEmbedding "Permanent link")
Bases: 
ModelScope Embedding.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-modelscope/llama_index/embeddings/modelscope/base.py`  
| 
```
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
```
 | 
```
classModelScopeEmbedding(BaseEmbedding):
"""ModelScope Embedding."""

    model_name: str = Field(
        default=DEFAULT_MODELSCOPE_MODEL,
        description=(
            "The model name to use from ModelScope. "
            "Unused if `model` is passed in directly."
        ),
    )
    model_revision: str = Field(
        default=DEFAULT_MODELSCOPE_MODEL_REVISION,
        description=(
            "The model revision to use from ModelScope. "
            "Unused if `model` is passed in directly."
        ),
    )
    task_name: str = Field(
        default=DEFAULT_MODELSCOPE_TASK,
        description=(
            "The ModelScope task type, for embedding use default sentence_embedding."
        ),
    )
    sequence_length: int = Field(
        default=128,
        description="The maximum length of the input sequence. Defaults to 128.",
    )
    model_kwargs: dict = Field(
        default_factory=dict,
        description="The kwargs to pass to the model during initialization.",
    )
    generate_kwargs: dict = Field(
        default_factory=dict,
        description="The kwargs to pass to the model during generation.",
    )

    _pipeline: Any = PrivateAttr()

    def__init__(
        self,
        model_name: str = DEFAULT_MODELSCOPE_MODEL,
        model_revision: str = DEFAULT_MODELSCOPE_MODEL_REVISION,
        task_name: str = DEFAULT_MODELSCOPE_TASK,
        sequence_length: int = DEFAULT_MODELSCOPE_SEQUENCE_LENGTH,
        model: Optional[Any] = None,
        model_kwargs: Optional[dict] = None,
        generate_kwargs: Optional[dict] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
    ) -> None:
"""Initialize params."""
        model_kwargs = model_kwargs or {}
        if model:
            pipeline = model
        else:
            pipeline = pipeline_builder(
                task=task_name,
                model=model_name,
                model_revision=model_revision,
                sequence_length=sequence_length,
            )

        super().__init__(
            model_kwargs=model_kwargs or {},
            generate_kwargs=generate_kwargs or {},
            pydantic_program_mode=pydantic_program_mode,
        )
        self._pipeline = pipeline

    def_get_query_embedding(self, query: str) -> Embedding:
"""Get the embedding for a query."""
        return output_to_embedding(self._pipeline(sentence_to_input(query)))

    async def_aget_query_embedding(self, query: str) -> Embedding:
"""Get the embedding for a query."""
        return output_to_embedding(self._pipeline(sentence_to_input(query)))

    def_get_text_embedding(self, text: str) -> Embedding:
"""Get the embedding for a text."""
        return output_to_embedding(self._pipeline(sentence_to_input(text)))

    def_get_text_embeddings(self, texts: List[str]) -> List[Embedding]:
"""Get the embeddings for a list of texts."""
        return outputs_to_embeddings(self._pipeline(sentences_to_input(texts)))

```
 |  
| --- | --- |  
options: members: - ModelScopeEmbedding
