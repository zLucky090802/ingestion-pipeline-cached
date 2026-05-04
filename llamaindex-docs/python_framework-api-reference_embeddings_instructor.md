# Instructor
##  InstructorEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/instructor/#llama_index.embeddings.instructor.InstructorEmbedding "Permanent link")
Bases: 
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-instructor/llama_index/embeddings/instructor/base.py`  
| 
```
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
```
 | 
```
classInstructorEmbedding(BaseEmbedding):
    query_instruction: Optional[str] = Field(
        description="Instruction to prepend to query text."
    )
    text_instruction: Optional[str] = Field(
        description="Instruction to prepend to text."
    )
    cache_folder: Optional[str] = Field(
        description="Cache folder for huggingface files."
    )

    _model: Any = PrivateAttr()

    def__init__(
        self,
        model_name: str = DEFAULT_INSTRUCT_MODEL,
        query_instruction: Optional[str] = None,
        text_instruction: Optional[str] = None,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        cache_folder: Optional[str] = None,
        device: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
    ):
        super().__init__(
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            model_name=model_name,
            query_instruction=query_instruction,
            text_instruction=text_instruction,
            cache_folder=cache_folder,
        )
        self._model = INSTRUCTOR(model_name, cache_folder=cache_folder, device=device)

    @classmethod
    defclass_name(cls) -> str:
        return "InstructorEmbedding"

    def_format_query_text(self, query_text: str) -> List[str]:
"""Format query text."""
        instruction = self.query_instruction

        if instruction is None:
            instruction = get_query_instruct_for_model_name(self.model_name)

        return [instruction, query_text]

    def_format_text(self, text: str) -> List[str]:
"""Format text."""
        instruction = self.text_instruction

        if instruction is None:
            instruction = get_text_instruct_for_model_name(self.model_name)

        return [instruction, text]

    def_embed(self, instruct_sentence_pairs: List[List[str]]) -> List[List[float]]:
"""Embed sentences."""
        return self._model.encode(instruct_sentence_pairs).tolist()

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        query_pair = self._format_query_text(query)
        return self._embed([query_pair])[0]

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""Get query embedding async."""
        return self._get_query_embedding(query)

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Get text embedding async."""
        return self._get_text_embedding(text)

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        text_pair = self._format_text(text)
        return self._embed([text_pair])[0]

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get text embeddings."""
        text_pairs = [self._format_text(text) for text in texts]
        return self._embed(text_pairs)

```
 |  
| --- | --- |  
options: members: - InstructorEmbedding
