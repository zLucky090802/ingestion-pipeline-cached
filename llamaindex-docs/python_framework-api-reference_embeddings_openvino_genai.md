# Openvino genai
##  OpenVINOGENAIEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/openvino_genai/#llama_index.embeddings.openvino_genai.OpenVINOGENAIEmbedding "Permanent link")
Bases: 
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-openvino-genai/llama_index/embeddings/openvino_genai/base.py`  
| 
```
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
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
```
 | 
```
classOpenVINOGENAIEmbedding(BaseEmbedding):
    model_path: str = Field(description="local path.")
    max_length: int = Field(description="Maximum length of input.")
    pooling: str = Field(description="Pooling strategy. One of ['cls', 'mean'].")
    normalize: bool = Field(default=True, description="Normalize embeddings or not.")
    query_instruction: Optional[str] = Field(
        description="Instruction to prepend to query text."
    )
    text_instruction: Optional[str] = Field(
        description="Instruction to prepend to text."
    )
    cache_folder: Optional[str] = Field(
        description="Cache folder for huggingface files.", default=None
    )

    _model: Any = PrivateAttr()
    _tokenizer: Any = PrivateAttr()
    _device: Any = PrivateAttr()

    def__init__(
        self,
        model_path: str,
        pooling: str = "cls",
        max_length: int = 2048,
        normalize: bool = True,
        query_instruction: Optional[str] = None,
        text_instruction: Optional[str] = None,
        model: Optional[Any] = None,
        tokenizer: Optional[Any] = None,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        callback_manager: Optional[CallbackManager] = None,
        device: Optional[str] = "CPU",
    ):
        try:
            importopenvino_genai
            importopenvinoasov

            core = ov.Core()

        except ImportError as e:
            raise ImportError(
                "Could not import openvino_genai python package. "
                "Please install it with: "
                "pip install -U openvino_genai"
            ) frome
        # use local model
        model = model or core.compile_model(
            Path(model_path) / "openvino_model.xml", device
        )
        tokenizer = tokenizer or openvino_genai.Tokenizer(model_path)

        if pooling not in ["cls", "mean"]:
            raise ValueError(f"Pooling {pooling} not supported.")

        super().__init__(
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager or CallbackManager([]),
            model_path=model_path,
            max_length=max_length,
            pooling=pooling,
            normalize=normalize,
            query_instruction=query_instruction,
            text_instruction=text_instruction,
        )
        self._device = device
        self._model = model
        self._tokenizer = tokenizer

    @classmethod
    defclass_name(cls) -> str:
        return "OpenVINOGENAIEmbedding"

    def_mean_pooling(self, model_output: Any, attention_mask: Any) -> Any:
"""Mean Pooling - Take attention mask into account for correct averaging."""
        token_embeddings = model_output[
            0
        ]  # First element of model_output contains all token embeddings
        input_mask_expanded = np.broadcast_to(
            np.expand_dims(attention_mask, axis=-1), token_embeddings.size()
        )
        return np.sum(token_embeddings * input_mask_expanded, 1) / np.clip(
            input_mask_expanded.sum(1), a_min=1e-9
        )

    def_cls_pooling(self, model_output: list) -> Any:
"""Use the CLS token as the pooling token."""
        return model_output[0][:, 0]

    def_embed(self, sentences: List[str]) -> List[List[float]]:
"""Embed sentences."""
        length = self._model.inputs[0].get_partial_shape()[1]
        if length.is_dynamic:
            features = self._tokenizer.encode(sentences)
        else:
            features = self._tokenizer.encode(
                sentences,
                pad_to_max_length=True,
                max_length=length.get_length(),
            )
        if "token_type_ids" in (input.any_name for input in self._model.inputs):
            token_type_ids = np.zeros(features.attention_mask.shape)
            model_input = {
                "input_ids": features.input_ids,
                "attention_mask": features.attention_mask,
                "token_type_ids": token_type_ids,
            }
        else:
            model_input = {
                "input_ids": features.input_ids,
                "attention_mask": features.attention_mask,
            }
        model_output = self._model(model_input)

        if self.pooling == "cls":
            embeddings = self._cls_pooling(model_output)
        else:
            embeddings = self._mean_pooling(model_output, model_input["attention_mask"])

        if self.normalize:
            norm = np.linalg.norm(embeddings, ord=2, axis=1, keepdims=True)
            embeddings = embeddings / norm

        return embeddings.tolist()

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        query = format_query(query, self.model_name, self.query_instruction)
        return self._embed([query])[0]

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""Get query embedding async."""
        return self._get_query_embedding(query)

    async def_aget_text_embedding(self, text: str) -> List[float]:
"""Get text embedding async."""
        return self._get_text_embedding(text)

    def_get_text_embedding(self, text: str) -> List[float]:
"""Get text embedding."""
        text = format_text(text, self.model_name, self.text_instruction)
        return self._embed([text])[0]

    def_get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
"""Get text embeddings."""
        texts = [
            format_text(text, self.model_name, self.text_instruction) for text in texts
        ]
        return self._embed(texts)

```
 |  
| --- | --- |  
options: members: - OpenVINOEmbedding
