# Huggingface openvino
##  OpenVINOEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/huggingface_openvino/#llama_index.embeddings.huggingface_openvino.OpenVINOEmbedding "Permanent link")
Bases: 
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-huggingface-openvino/llama_index/embeddings/huggingface_openvino/base.py`  
| 
```
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
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
```
 | 
```
classOpenVINOEmbedding(BaseEmbedding):
    model_id_or_path: str = Field(description="Huggingface model id or local path.")
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
        model_id_or_path: str = "BAAI/bge-m3",
        pooling: str = "cls",
        max_length: Optional[int] = None,
        normalize: bool = True,
        query_instruction: Optional[str] = None,
        text_instruction: Optional[str] = None,
        model: Optional[Any] = None,
        tokenizer: Optional[Any] = None,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        callback_manager: Optional[CallbackManager] = None,
        model_kwargs: Dict[str, Any] = {},
        device: Optional[str] = "auto",
    ):
        try:
            fromhuggingface_hubimport HfApi
        except ImportError as e:
            raise ValueError(
                "Could not import huggingface_hub python package. "
                "Please install it with: "
                "`pip install -U huggingface_hub`."
            ) frome

        defrequire_model_export(
            model_id: str, revision: Any = None, subfolder: Any = None
        ) -> bool:
            model_dir = Path(model_id)
            if subfolder is not None:
                model_dir = model_dir / subfolder
            if model_dir.is_dir():
                return (
                    not (model_dir / "openvino_model.xml").exists()
                    or not (model_dir / "openvino_model.bin").exists()
                )
            hf_api = HfApi()
            try:
                model_info = hf_api.model_info(model_id, revision=revision or "main")
                normalized_subfolder = (
                    None if subfolder is None else Path(subfolder).as_posix()
                )
                model_files = [
                    file.rfilename
                    for file in model_info.siblings
                    if normalized_subfolder is None
                    or file.rfilename.startswith(normalized_subfolder)
                ]
                ov_model_path = (
                    "openvino_model.xml"
                    if subfolder is None
                    else f"{normalized_subfolder}/openvino_model.xml"
                )
                return (
                    ov_model_path not in model_files
                    or ov_model_path.replace(".xml", ".bin") not in model_files
                )
            except Exception:
                return True

        if require_model_export(model_id_or_path):
            # use remote model
            model = model or OVModelForFeatureExtraction.from_pretrained(
                model_id_or_path, export=True, device=device, **model_kwargs
            )
        else:
            # use local model
            model = model or OVModelForFeatureExtraction.from_pretrained(
                model_id_or_path, device=device, **model_kwargs
            )
        tokenizer = tokenizer or AutoTokenizer.from_pretrained(model_id_or_path)

        if max_length is None:
            try:
                max_length = int(model.config.max_position_embeddings)
            except Exception:
                raise ValueError(
                    "Unable to find max_length from model config. "
                    "Please provide max_length."
                )
            try:
                max_length = min(max_length, int(tokenizer.model_max_length))
            except Exception as exc:
                print(f"An error occurred while retrieving tokenizer max length: {exc}")

        if pooling not in ["cls", "mean"]:
            raise ValueError(f"Pooling {pooling} not supported.")

        super().__init__(
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager or CallbackManager([]),
            model_id_or_path=model_id_or_path,
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
        return "OpenVINOEmbedding"

    @staticmethod
    defcreate_and_save_openvino_model(
        model_name_or_path: str,
        output_path: str,
        export_kwargs: Optional[dict] = None,
    ) -> None:
        try:
            fromoptimum.intel.openvinoimport OVModelForFeatureExtraction
            fromtransformersimport AutoTokenizer
            fromoptimum.exporters.openvino.convertimport export_tokenizer

        except ImportError:
            raise ImportError(
                "OpenVINO Embedding requires transformers and optimum to be installed.\n"
                "Please install transformers with "
                "`pip install transformers optimum[openvino]`."
            )

        export_kwargs = export_kwargs or {}
        model = OVModelForFeatureExtraction.from_pretrained(
            model_name_or_path, export=True, compile=False, **export_kwargs
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)

        model.save_pretrained(output_path)
        tokenizer.save_pretrained(output_path)
        export_tokenizer(tokenizer, output_path)
        print(
            f"Saved OpenVINO model to {output_path}. Use it with "
            f"`embed_model = OpenVINOEmbedding(model_id_or_path='{output_path}')`."
        )

    def_mean_pooling(self, model_output: Any, attention_mask: Any) -> Any:
"""Mean Pooling - Take attention mask into account for correct averaging."""
        importtorch

        # First element of model_output contains all token embeddings
        token_embeddings = model_output[0]
        input_mask_expanded = (
            attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        )
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
            input_mask_expanded.sum(1), min=1e-9
        )

    def_cls_pooling(self, model_output: list) -> Any:
"""Use the CLS token as the pooling token."""
        return model_output[0][:, 0]

    def_embed(self, sentences: List[str]) -> List[List[float]]:
"""Embed sentences."""
        length = self._model.request.inputs[0].get_partial_shape()[1]
        if length.is_dynamic:
            encoded_input = self._tokenizer(
                sentences,
                padding=True,
                max_length=self.max_length,
                truncation=True,
                return_tensors="pt",
            )
        else:
            encoded_input = self._tokenizer(
                sentences,
                padding="max_length",
                max_length=length.get_length(),
                truncation=True,
                return_tensors="pt",
            )

        model_output = self._model(**encoded_input)

        if self.pooling == "cls":
            embeddings = self._cls_pooling(model_output)
        else:
            embeddings = self._mean_pooling(
                model_output, encoded_input["attention_mask"]
            )

        if self.normalize:
            importtorch

            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

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
